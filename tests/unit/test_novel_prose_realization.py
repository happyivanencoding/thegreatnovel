import json
import re
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from novel_authoring.reference_corpus.semantic import compile_semantic_corpus
from novel_authoring.reference_corpus.semantic_models import ProseDnaCard


def _prose_payload(source_book_id: str = "book-01") -> dict[str, object]:
    evidence_refs = [
        {
            "evidence_id": f"prose-{source_book_id}-{index:02d}",
            "source_book_id": source_book_id,
            "source_id": f"source-{source_book_id}",
            "distill_id": f"distill-{source_book_id}",
            "segment_id": f"segment-{index:04d}",
            "line_start": index * 10,
            "line_end": index * 10 + 5,
            "observation_summary": "窗口只记录节奏、信息组织和场景功能，不保存原文。",
        }
        for index in range(1, 9)
    ]
    windows = [
        {
            "window_id": f"window-{index:02d}",
            "scene_function": function,
            "segment_id": f"segment-{index:04d}",
            "line_start": index * 10,
            "line_end": index * 10 + 5,
            "evidence_summary": "用动作和反应承载信息，保留来源定位，不复制句子。",
        }
        for index, function in enumerate(
            (
                "OPENING",
                "ORDINARY",
                "DIALOGUE",
                "ACTION",
                "PAYOFF",
                "AFTERMATH",
                "EXPOSITION",
                "ENDING",
            ),
            start=1,
        )
    ]
    observation_fields = (
        "sentence_rhythm",
        "paragraph_rhythm",
        "narrative_distance",
        "concrete_vs_abstract",
        "dialogue",
        "character_voice",
        "interior_thought",
        "action_combat",
        "payoff_realization",
        "description",
        "transitions",
        "chapter_ending",
        "lexical_texture",
        "punctuation",
        "human_irregularity",
    )
    control_fields = (
        "sentence_rhythm",
        "paragraph_rhythm",
        "dialogue_density",
        "narrative_distance",
        "interiority",
        "exposition_mode",
        "sensory_density",
        "humor_mode",
        "action_directness",
        "payoff_realization",
        "chapter_end_modes",
        "lexical_texture",
    )
    return {
        "schema_version": "reference-corpus-card-v1",
        "card_id": f"{source_book_id}-prose-dna-v1",
        "card_type": "prose-dna",
        "knowledge_level": "BOOK_OBSERVATION",
        "status": "REFERENCE_ONLY",
        "source_book_ids": [source_book_id],
        "evidence_refs": evidence_refs,
        "creative_problem_tags": ["prose-realization", "dialogue", "payoff-prose"],
        "reader_experiences": [],
        "narrative_drives": [],
        "payoff_channels": [],
        "evidence_scope": "SINGLE_BOOK",
        "maturity": "PILOT",
        "category_ids": ["玄幻"],
        "depends_on": ["book-card-01"],
        "source_book_id": source_book_id,
        "title": "测试书",
        "category": "玄幻",
        "sampling_strategy": "按场景功能与纵向阶段做有界窗口采样。",
        "coverage_mode": "SCENE_FUNCTION_WINDOWS",
        "sample_window_count": 8,
        "scene_functions": [window["scene_function"] for window in windows],
        "sample_windows": windows,
        "observations": {
            field: "观察到写法倾向，并给出软控制与证据边界。"
            for field in observation_fields
        },
        "soft_controls": {field: "作为软提示，当前书与作者意图优先。" for field in control_fields},
        "source_style_leakage_check": "PASS",
        "source_style_leakage_note": "只保留抽象变量，没有来源句式、人物口癖或签名比喻。",
        "transfer_boundary": "只迁移写法变量，不迁移人物、事件、专名、原句或作者身份。",
        "limitations": ["测试 fixture 只验证 schema，不代表完整文学覆盖。"],
    }


def _write_frontmatter(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        + yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)
        + "---\n\n中文 prose 观察。\n",
        encoding="utf-8",
        newline="\n",
    )


def _make_reference_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "corpus"
    for relative in (
        "books",
        "book-dna",
        "prose-dna",
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
        _write_frontmatter(
            root / "books" / f"book-{index:02d}.md",
            {
                "schema_version": "reference-corpus-card-v1",
                "card_id": f"book-card-{index:02d}",
                "card_type": "reference-book",
                "knowledge_level": "BOOK_OBSERVATION",
                "status": "REFERENCE_ONLY",
                "source_book_ids": [source_book_id],
                "evidence_refs": [
                    {
                        "evidence_id": f"book-{index:02d}-evidence",
                        "source_book_id": source_book_id,
                        "source_id": f"source-{source_book_id}",
                        "distill_id": f"distill-{source_book_id}",
                        "segment_id": "segment-0001",
                        "line_start": 1,
                        "line_end": 3,
                        "observation_summary": "来源索引测试证据。",
                    }
                ],
                "evidence_scope": "SINGLE_BOOK",
                "maturity": "PILOT",
                "category_ids": ["玄幻"],
                "depends_on": [],
                "source_book_id": source_book_id,
                "title": f"测试书{index}",
                "category": "玄幻",
                "distill_id": f"distill-{source_book_id}",
                "summary": "仅作为来源索引，不包含正文。",
            },
        )
    return root


def test_prose_dna_is_strictly_separate_from_book_dna() -> None:
    card = ProseDnaCard.model_validate(_prose_payload())
    assert card.card_type == "prose-dna"
    assert card.sample_window_count == 8
    assert card.source_style_leakage_check == "PASS"

    invalid = {**_prose_payload(), "source_quote": "不应进入卡片"}
    with pytest.raises(ValidationError):
        ProseDnaCard.model_validate(invalid)


def test_prose_dna_machine_package_has_own_count(tmp_path: Path) -> None:
    root = _make_reference_fixture(tmp_path)
    _write_frontmatter(root / "prose-dna" / "book-01-prose.md", _prose_payload())
    result = compile_semantic_corpus(root)

    package = json.loads((root / "machine" / "corpus-package.json").read_text(encoding="utf-8"))
    assert result["card_count"] == 27
    assert package["counts"]["prose_dna"] == 1
    records = [
        json.loads(line)
        for line in (root / "machine" / "cards.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert [record["card_type"] for record in records].count("prose-dna") == 1


def _obvious_antipatterns(text: str) -> dict[str, int]:
    return {
        "mechanical_connectors": len(re.findall(r"此外|然而|总而言之|首先|随后", text)),
        "negative_parallel": len(re.findall(r"不仅(?:仅是)?[^。；\n]{0,30}(?:而是|而且)", text)),
        "triple_list": len(re.findall(r"[^。\n]{1,20}、[^。\n]{1,20}、[^。\n]{1,20}", text)),
    }


def test_antipattern_fixtures_are_structural_not_ai_scores() -> None:
    fixture_root = Path(__file__).parents[1] / "fixtures" / "novel_prose_antipatterns"
    ai_like = (fixture_root / "ai_like.md").read_text(encoding="utf-8")
    natural = (fixture_root / "natural.md").read_text(encoding="utf-8")
    mixed = (fixture_root / "mixed.md").read_text(encoding="utf-8")

    ai_flags = _obvious_antipatterns(ai_like)
    assert ai_flags["mechanical_connectors"] >= 3
    assert ai_flags["negative_parallel"] >= 1
    assert ai_flags["triple_list"] >= 1
    assert _obvious_antipatterns(natural) == {
        "mechanical_connectors": 0,
        "negative_parallel": 0,
        "triple_list": 0,
    }
    mixed_flags = _obvious_antipatterns(mixed)
    assert mixed_flags["mechanical_connectors"] >= 2
    assert mixed_flags["negative_parallel"] >= 1


def test_novel_like_naturalness_fixture_set_is_present() -> None:
    fixture_root = Path(__file__).parents[1] / "fixtures" / "novel_prose_antipatterns"
    required = {
        "payoff_explained_three_times.md",
        "dialogue_exposition_dump.md",
        "uniform_sentence_length.md",
        "paragraph_summary_endings.md",
        "natural_action_payoff.md",
    }
    assert required <= {path.name for path in fixture_root.glob("*.md")}
    assert "说明" in (fixture_root / "payoff_explained_three_times.md").read_text(
        encoding="utf-8"
    )
    assert "规矩" in (fixture_root / "dialogue_exposition_dump.md").read_text(encoding="utf-8")
    assert "石阶" in (fixture_root / "natural_action_payoff.md").read_text(encoding="utf-8")


def test_actual_draft_executor_wires_novel_prose_realization() -> None:
    skill_path = Path(__file__).parents[2] / ".agents" / "skills" / "continue-novel" / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    realization_ref = ".agents/skills/novel-prose-realization/SKILL.md"
    assert realization_ref in text
    authority_at = text.index("Chapter Contract > Canon > Current Scene Context > Prose Controls")
    naturalness_at = text.index("Novel Prose Naturalness Check")
    assert authority_at < naturalness_at
    assert "第二个 humanization handoff" in text
