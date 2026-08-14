from __future__ import annotations

# Test fixtures contain long inline frontmatter examples.
# ruff: noqa: E501
import json
from pathlib import Path

import pytest

from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.reference_corpus.service import (
    EXPECTED_CATEGORIES,
    ReferenceCorpusError,
    build_inventory,
    create_scaffold,
    load_inventory,
    load_selection,
    propose_selection,
    validate_card_frontmatter,
    validate_corpus,
    validate_schema_pack,
    validate_selection,
    write_inventory,
    write_selection_proposal,
)


def _write_book(path: Path, *, chapters: int = 4) -> None:
    content = "\n\n".join(f"第{i}章 标题\n正文证据 {i}" for i in range(1, chapters + 1))
    path.write_text(content + "\n", encoding="utf-8")


def _scaffold(tmp_path: Path) -> tuple[Path, Path]:
    raw = tmp_path / "中文 raw root"
    corpus = tmp_path / "派生 reference-corpus"
    raw.mkdir()
    create_scaffold(corpus, raw)
    return raw, corpus


def test_inventory_supports_chinese_paths_and_excludes_derived_root(tmp_path: Path) -> None:
    raw = tmp_path / "原始小说"
    derived = raw / "reference-corpus"
    category = raw / "01_玄幻"
    category.mkdir(parents=True)
    derived.mkdir()
    _write_book(category / "带 空格 的书.txt")
    _write_book(category / "另一本.txt", chapters=5)
    _write_book(derived / "不应成为类别.txt")

    manifest = build_inventory(raw, derived)

    assert [item.category_id for item in manifest.actual_categories] == ["01_玄幻"]
    assert len(manifest.files) == 2
    assert manifest.files[0].extension == ".txt"
    assert any("排除 corpus-root" in warning for warning in manifest.warnings)


def test_inventory_does_not_modify_source_and_flags_duplicate_titles(tmp_path: Path) -> None:
    raw, corpus = _scaffold(tmp_path)
    category = raw / "01_玄幻"
    category.mkdir()
    first = category / "同名_正文全集.txt"
    second = category / "同名全本.txt"
    _write_book(first)
    _write_book(second, chapters=5)
    before = first.read_bytes()

    manifest = build_inventory(raw, corpus)

    assert first.read_bytes() == before
    assert all(any("normalized title 重复" in warning for warning in item.warnings) for item in manifest.files)


def test_proposed_selection_has_two_per_category_when_inventory_is_complete(tmp_path: Path) -> None:
    raw, corpus = _scaffold(tmp_path)
    for index, definition in enumerate(EXPECTED_CATEGORIES, start=1):
        category = raw / definition.category_id
        category.mkdir()
        _write_book(category / f"书 A {index}.txt", chapters=4 + index)
        _write_book(category / f"书 B {index}.txt", chapters=8 + index)
    manifest = build_inventory(raw, corpus)
    proposal = propose_selection(manifest)

    assert proposal.status == "PROPOSED"
    assert proposal.selected_book_count == 26
    assert all(len(category.recommendations) == 2 for category in proposal.categories)
    result = validate_selection(manifest, proposal)
    assert result["valid"] is True


def test_supplemental_representatives_fill_26_without_relabeling(tmp_path: Path) -> None:
    raw, corpus = _scaffold(tmp_path)
    for category_id in ("01_玄幻", "02_仙侠"):
        category = raw / category_id
        category.mkdir()
        for index in range(15):
            _write_book(category / f"代表书 {index}.txt", chapters=4 + index)

    proposal = propose_selection(build_inventory(raw, corpus))

    assert proposal.selected_book_count == 26
    assert proposal.target_book_count == 26
    assert len(proposal.supplemental_recommendations) == 22
    assert {item.category for item in proposal.supplemental_recommendations} <= {
        "01_玄幻",
        "02_仙侠",
    }


def test_selection_reports_blocker_when_category_has_fewer_than_two_books(tmp_path: Path) -> None:
    raw, corpus = _scaffold(tmp_path)
    category = raw / "01_玄幻"
    category.mkdir()
    _write_book(category / "唯一一本.txt")
    proposal = propose_selection(build_inventory(raw, corpus))

    blocked = next(item for item in proposal.categories if item.category_id == "01_玄幻")
    assert blocked.status == "BLOCKED"
    assert blocked.blocker and "少于两本" in blocked.blocker
    assert proposal.status == "PROPOSED"


def test_selection_round_trip_and_confirmed_alignment(tmp_path: Path) -> None:
    raw, corpus = _scaffold(tmp_path)
    category = raw / "01_玄幻"
    category.mkdir()
    _write_book(category / "甲.txt")
    _write_book(category / "乙.txt", chapters=5)
    manifest = build_inventory(raw, corpus)
    write_inventory(manifest, corpus)
    proposal = propose_selection(manifest)
    write_selection_proposal(proposal)

    loaded_inventory = load_inventory(corpus / "selection/inventory.json")
    loaded_proposal = load_selection(corpus / "selection/pilot-selection.proposed.yaml")
    result = validate_selection(loaded_inventory, loaded_proposal)

    assert result["valid"] is False
    assert any("BLOCKER" in error for error in result["errors"])
    assert loaded_proposal.status == "PROPOSED"


def test_schema_pack_and_card_frontmatter_boundaries(tmp_path: Path) -> None:
    _raw, corpus = _scaffold(tmp_path)
    pack_result = validate_schema_pack(corpus / "schema-pack/novel-reference-corpus-v1/pack.yaml")
    assert pack_result["valid"] is True
    card = validate_card_frontmatter(
        """---\ncard_id: book-1-dna\ncard_type: book-dna\nknowledge_level: BOOK_OBSERVATION\nsource_book_id: book-1\nlocator: chapter-1/segment-1\n---\n\n摘要\n"""
    )
    assert card.knowledge_level is CardKnowledgeLevel.BOOK_OBSERVATION
    with pytest.raises(ReferenceCorpusError):
        validate_card_frontmatter(
            """---\ncard_id: bad\ncard_type: corpus-synthesis\nknowledge_level: BOOK_OBSERVATION\nsource_book_id: book-1\nlocator: chapter-1\n---\n"""
        )


def test_validate_rejects_raw_leakage_without_gbrain(tmp_path: Path) -> None:
    _raw, corpus = _scaffold(tmp_path)
    (corpus / "raw").mkdir()
    (corpus / "books" / "copied.txt").write_text("完整正文", encoding="utf-8")

    result = validate_corpus(corpus)

    assert result["valid"] is False
    assert any("完整正文目录" in error or "来源正文文件" in error for error in result["errors"])
    assert json.loads(json.dumps(result, ensure_ascii=False))["corpus_root"] == str(corpus.resolve())
