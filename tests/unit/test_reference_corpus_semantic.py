from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from novel_authoring.progression.models import PayoffChannel, ReaderExperience
from novel_authoring.reference_corpus.semantic import (
    SemanticCorpusError,
    compile_semantic_corpus,
    retrieve_metadata_candidates,
    source_diversity_guard,
    validate_semantic_corpus,
)
from novel_authoring.reference_corpus.semantic_models import (
    BookDnaCard,
    EvidenceScope,
    SemanticMaturity,
    SemanticStatus,
    SpanKind,
)
from novel_authoring.serial_kernel.models import NarrativeDrive


def _evidence(source_book_id: str, index: int = 1) -> dict[str, object]:
    return {
        "evidence_id": f"ev-{source_book_id}-{index}",
        "source_book_id": source_book_id,
        "source_id": f"source-{source_book_id}",
        "distill_id": f"distill-{source_book_id}",
        "segment_id": "segment-0001",
        "line_start": 1,
        "line_end": 3,
        "observation_summary": "短证据摘要，不保存来源正文。",
    }


def _common(source_book_ids: list[str], *, card_id: str) -> dict[str, object]:
    return {
        "schema_version": "reference-corpus-card-v1",
        "card_id": card_id,
        "source_book_id": source_book_ids[0],
        "knowledge_level": "BOOK_OBSERVATION",
        "status": "REFERENCE_ONLY",
        "source_book_ids": source_book_ids,
        "evidence_refs": [_evidence(source_book_ids[0])],
        "creative_problem_tags": ["pure-upside", "breakthrough"],
        "reader_experiences": [ReaderExperience.BREAKTHROUGH.value],
        "narrative_drives": [NarrativeDrive.POWER_PROGRESSION.value],
        "payoff_channels": [PayoffChannel.POWER_BREAKTHROUGH.value],
        "evidence_scope": EvidenceScope.SINGLE_BOOK.value,
        "maturity": SemanticMaturity.PILOT.value,
        "category_ids": ["玄幻"],
        "depends_on": [],
    }


def _book_dna_payload(source_book_id: str = "book-01") -> dict[str, object]:
    value = _common([source_book_id], card_id=f"dna-{source_book_id}")
    value.update(
        {
            "card_type": "book-dna",
            "source_book_id": source_book_id,
            "title": "测试书",
            "category": "玄幻",
            "rewrite_required": False,
            "rewrite_reason": "通过 targeted semantic audit，无需重写。",
            "sampling_strategy": "纵向五窗口加 payoff、transition、novelty 窗口",
            "coverage_mode": "LONGITUDINAL_SNAPSHOT",
            "sample_window_count": 8,
            "coverage_stages": ["OPENING", "EARLY", "MID", "LATE", "END"],
            "reader_promise": "读者期待能力不断打开新的行动可能。",
            "repeatable_reader_loop": "获得线索或能力，立即验证，再进入下一种未知。",
            "core_progression_grammar": "以能力解锁和可见验证为主，不强制成本。",
            "payoff_grammar": "突破可完整兑现为更强、更自由的纯收益。",
            "action_space_expansion": "以前不能做的探索现在可做。",
            "advantage_special_capability": "主角拥有不对称的能力入口。",
            "world_expansion_grammar": "通过探索和知识层扩大世界。",
            "novelty_recombination": "旧能力进入新场景后获得新用途。",
            "character_desire_agency": "主角有自选的好奇与探索目标。",
            "social_relationship_dynamics": "关系通过认可和协作变化。",
            "resource_economy": "资源释放后扩大选择空间，不立即制造新稀缺。",
            "optional_constraints_costs": "NOT_MATERIAL：当前窗口未见改变选择的即时成本。",
            "long_form_sustainability": "用新能力、新区域和新谜题切换阶段。",
            "failure_fatigue_risks": ["INFERRED_RISK：重复验证可能造成疲劳。"],
            "transferable_variables": ["突破可见度", "行动空间扩张", "探索窗口"],
            "transfer_boundary": "只迁移变量，不迁移来源身份、事件、专名或句式。",
            "anti_bias_checks": {
                "Payoff Removal": "PASS",
                "Constraint Subtraction": "PASS",
                "Professional Operations Replacement": "PASS",
                "Governance Default": "PASS",
                "Responsibility Default": "PASS",
                "Cost Necessity": "PASS",
                "Pure Upside": "PASS",
            },
        }
    )
    return value


def test_pure_upside_book_dna_and_existing_enums_are_valid() -> None:
    card = BookDnaCard.model_validate(_book_dna_payload())
    assert card.optional_constraints_costs.startswith("NOT_MATERIAL")
    assert card.reader_experiences == [ReaderExperience.BREAKTHROUGH]
    assert card.narrative_drives == [NarrativeDrive.POWER_PROGRESSION]
    assert card.payoff_channels == [PayoffChannel.POWER_BREAKTHROUGH]
    assert card.status is SemanticStatus.REFERENCE_ONLY


def test_span_kind_is_explicit() -> None:
    assert SpanKind.CONTIGUOUS_ARC.value == "CONTIGUOUS_ARC"
    assert SpanKind.LONGITUDINAL_TRAJECTORY.value == "LONGITUDINAL_TRAJECTORY"


def _write_frontmatter(
    path: Path,
    payload: dict[str, object],
    body: str = "\n中文语义投影。\n",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n" + yaml.safe_dump(payload, allow_unicode=True, sort_keys=False) + "---\n" + body,
        encoding="utf-8",
        newline="\n",
    )


def _make_compile_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "corpus"
    for relative in (
        "books",
        "book-dna",
        "arcs",
        "observations",
        "mechanisms",
        "contrasts",
        "syntheses/categories",
        "syntheses/cross-category",
        "selection",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)
    for index in range(1, 27):
        source_book_id = f"book-{index:02d}"
        payload = _common([source_book_id], card_id=f"book-card-{index:02d}")
        payload.update(
            {
                "card_type": "reference-book",
                "title": f"测试书{index}",
                "category": "玄幻",
                "distill_id": f"distill-{index:02d}",
                "summary": "仅作为来源索引，不包含正文。",
            }
        )
        _write_frontmatter(root / "books" / f"book-{index:02d}.md", payload)
    _write_frontmatter(root / "book-dna" / "dna-book-01.md", _book_dna_payload("book-01"))
    return root


def test_compile_machine_package_and_dependency_stale_status(tmp_path: Path) -> None:
    root = _make_compile_fixture(tmp_path)
    result = compile_semantic_corpus(root)
    assert result["card_count"] == 27
    package = json.loads((root / "machine/corpus-package.json").read_text(encoding="utf-8"))
    assert package["canon_committed"] is False
    assert package["edition_activated"] is False
    assert (root / "machine/cards.jsonl").is_file()
    manifest_path = next((root / "machine/manifests").glob("*.json"))
    assert manifest_path.read_text(encoding="utf-8")


def test_semantic_validation_rejects_raw_text_leakage(tmp_path: Path) -> None:
    root = _make_compile_fixture(tmp_path)
    (root / "raw").mkdir()
    (root / "book-dna" / "leak.md").write_text(
        "---\n"
        + yaml.safe_dump(_book_dna_payload("book-01"), allow_unicode=True)
        + "---\n"
        + "原文" * 500,
        encoding="utf-8",
    )
    result = validate_semantic_corpus(root)
    assert result["valid"] is False
    assert any("完整正文目录" in error or "长段来源正文" in error for error in result["errors"])


def test_metadata_retrieval_and_source_diversity_guard(tmp_path: Path) -> None:
    root = _make_compile_fixture(tmp_path)
    compile_semantic_corpus(root)
    records = retrieve_metadata_candidates(
        root,
        creative_problem="pure-upside",
        reader_experiences=[ReaderExperience.BREAKTHROUGH.value],
        narrative_drives=[NarrativeDrive.POWER_PROGRESSION.value],
        payoff_channels=[PayoffChannel.POWER_BREAKTHROUGH.value],
        max_cards=3,
    )
    assert records
    assert source_diversity_guard(records)
    with pytest.raises(ValueError):
        retrieve_metadata_candidates(root, max_cards=2)


def test_source_diversity_guard_detects_same_source_overflow() -> None:
    records = [{"source_book_ids": ["book-01"]} for _ in range(3)]
    assert source_diversity_guard(records) is False


def test_invalid_machine_package_is_not_silently_accepted(tmp_path: Path) -> None:
    root = _make_compile_fixture(tmp_path)
    compile_semantic_corpus(root)
    (root / "machine/cards.jsonl").write_text("{\"card_type\": \"not-real\"}\n", encoding="utf-8")
    result = validate_semantic_corpus(root)
    assert result["valid"] is False
    assert any("machine/cards.jsonl" in error for error in result["errors"])
    with pytest.raises(SemanticCorpusError):
        retrieve_metadata_candidates(root, max_cards=3)


def test_retrieval_query_fixture_has_broad_creative_problem_coverage() -> None:
    fixture = Path(__file__).parents[1] / "fixtures" / "reference_corpus_queries.yaml"
    queries = yaml.safe_load(fixture.read_text(encoding="utf-8"))
    assert isinstance(queries, list)
    assert len(queries) >= 30
    assert len({item["query_id"] for item in queries}) == len(queries)
    problems = " ".join(item["creative_problem"] for item in queries)
    for phrase in ("开篇", "突破", "资源", "世界扩张", "探索", "谜团", "长篇", "结尾"):
        assert phrase in problems
    assert all(
        3 <= len(item["expected_card_families"]) <= 4
        and "keyword_only" in item["forbidden_failure_modes"]
        for item in queries
    )
