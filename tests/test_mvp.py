from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from fastapi.testclient import TestClient

import story_mvp.app as app_module
import story_mvp.gbrain as gbrain_module
from story_mvp.app import app
from story_mvp.chapter_context import (
    MINIMAL_AUTHORITY_RULE,
    ChapterContextPacket,
    compact_growth_genome_for_chapter,
    build_chapter_context,
    render_event_contract,
    render_growth_benefit_projection,
)
from story_mvp.gbrain import GBrainQueryError, NOVEL_GBRAIN_SCOPE, query_gbrain, resolve_command_prefix
from story_mvp.gbrain_retrieval import (
    CHAPTER_FINAL_RESULT_LIMIT,
    CREATIVE_PLANNING_FINAL_RESULT_LIMIT,
    EMPTY_RESULT,
    FINAL_RESULT_LIMIT,
    PLANNING_CANDIDATE_INSPECTION_LIMIT,
    RAW_RESULT_LIMIT,
    QUERY_RECALL_LIMIT,
    WORLD_COORDINATE_REFERENCE_SLUG,
    _forbidden_terms,
    active_inspiration_allowed,
    build_retrieval_brief,
    dedupe_query_hits_by_slug,
    default_effective_query,
    extract_hard_constraints,
    parse_query_results,
    retrieve_gbrain,
)
from story_mvp.hybrid_runtime import (
    build_curator_context,
    count_specialist_patches,
    extract_final_chapter_artifact,
    extract_last_transition_context,
    extract_opening_strategy,
    extract_primary_draft,
    extract_primary_fact_summary,
    drop_growth_hierarchy,
)
from story_mvp.prompts import (
    DEFAULT_DIRECTOR_TEMPLATE,
    DEFAULT_PROMPT_TEMPLATES,
    DEFAULT_STATE_DELTA_TEMPLATE,
    DIRECTOR_CHAPTER_BUDGET_RULE,
    DIRECTOR_REPETITION_RULE,
    CreativeApprovalError,
    OPENING_THREE_CHAPTER_CONTRACT,
    PROMPT_MODES,
    PROSE_REALIZATION_CONTRACT,
    RESULT_STOP_RULE,
    REQUIRED_OUTLINE_FIELDS,
    SINGLE_WRITER_RUNTIME_NOTE,
    STAGE_CHANGE_PLANNING_RULE,
    WRITER_AUDIT_RULE,
    HardGateError,
    canon_index_has_labels,
    generate_prompt,
    parse_outline_fields,
    parse_canon_index,
    render_canon_index,
    sanitize_chapter_template,
    validate_current_outline,
)
from story_mvp.references import load_validated_references
from story_mvp.storage import (
    compact_open_promises,
    compact_recent_summaries,
    compose_book_content,
    create_book,
    parse_book_sections,
    read_book_payload,
    text_to_prompt_templates,
    validate_book_content_for_save,
)


client = TestClient(app)

APPROVED_CREATIVE_STATE = {
    "fantasy_seed": {"origin": "author_edited", "status": "author_approved"},
    "world_vision": {"origin": "author_edited", "status": "author_approved"},
    "proposal": {"origin": "author_edited", "status": "author_approved"},
}


OUTLINE = "\n".join(f"{field}：内容" for field in REQUIRED_OUTLINE_FIELDS)


def approved_creative_inputs() -> dict[str, object]:
    return {
        "creative_state": APPROVED_CREATIVE_STATE,
        "fantasy_seed": "APPROVED_FANTASY_SEED",
        "world_vision": "APPROVED_WORLD_VISION",
        "proposal_context": "APPROVED_STORY_PROGRAM",
    }

#: 匹配多 Writer 职责标记；「Writer Audit」是三标题响应合同，必须保留，不能误伤。
#: lookahead 口径与 prompts._MULTI_WRITER_HEADING_PATTERN / _MULTI_WRITER_LINE_PATTERN 统一。
_WRITER_ABC_PATTERN = re.compile(r"Writer\s*[ABC](?![0-9A-Za-z])")


def test_new_book_has_creative_artifacts_and_fixed_state(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    assert {path.name for path in book_dir.iterdir()} == {
        "BOOK.md",
        "PROMPTS.md",
        "PROPOSAL.md",
        "FANTASY_SEED.md",
        "WORLD_VISION.md",
        "CREATIVE_STATE.json",
        "chapters",
    }
    assert (book_dir / "chapters").is_dir()
    payload = read_book_payload("demo", tmp_path)
    assert set(payload["prompt_templates"]) == {
        "idea",
        "fantasy_seed",
        "world_vision",
        "outline",
        "chapter_prep",
        "chapter",
        "review",
        "context_curator",
        "primary_writer",
        "specialist_opening",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
        "chapter_integrator",
    }
    assert set(payload["sections"]) == {"design", "long_plan", "small_plan", "status"}
    assert len(payload["design_sections"]) == 13
    assert "growth_genome" in payload["design_sections"]
    assert "## 0. 本书成长基因图" in payload["book_content"]
    assert payload["creative_state"] == {
        "fantasy_seed": {"origin": "empty", "status": "empty"},
        "world_vision": {"origin": "empty", "status": "empty"},
        "proposal": {"origin": "empty", "status": "empty"},
    }
    assert set(payload["creative_artifacts"]) == {"fantasy_seed", "world_vision", "proposal"}


def test_prompt_template_parser_ignores_unsupported_top_level_sections() -> None:
    parsed = text_to_prompt_templates(
        "# 新书/总纲规划\n\nOUTLINE\n\n"
        "# retired template\n\nOLD CONTENT\n\n"
        "# 当前章执行小纲\n\nCHAPTER PREP\n"
    )

    assert parsed["outline"] == "OUTLINE"
    assert parsed["chapter_prep"] == "CHAPTER PREP"
    assert all("OLD CONTENT" not in value for value in parsed.values())


def test_book_save_contract_rejects_inline_or_missing_top_level_heading(tmp_path: Path) -> None:
    malformed = (
        "模型说明。# 小说总体设计画像\n\n设计\n\n"
        "# 当前中期规划窗口\n\n规划\n\n"
        "# 未来十章逐章小纲\n\n十章\n\n"
        "# 当前状态、未兑现承诺与作者备注\n\n状态\n"
    )
    with pytest.raises(ValueError, match="小说总体设计画像"):
        validate_book_content_for_save(malformed)
    book_dir = create_book("demo", tmp_path)
    before = (book_dir / "BOOK.md").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="小说总体设计画像"):
        app_module.write_book("demo", malformed, tmp_path)
    assert (book_dir / "BOOK.md").read_text(encoding="utf-8") == before


def test_outline_ui_discards_model_preamble_before_book_headings() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "const firstHeadingIndex = source.indexOf(firstHeading);" in js
    assert "if (firstHeadingIndex >= 0) source = source.slice(firstHeadingIndex);" in js


def test_new_book_has_no_database_or_old_system_directory(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    names = {path.name.lower() for path in book_dir.rglob("*")}
    assert not any(name.endswith((".db", ".sqlite", ".sqlite3")) for name in names)
    assert not {"edition", "atlas", "novel_authoring"} & names


def test_legacy_long_plan_heading_is_read_and_new_heading_is_written() -> None:
    legacy = "# 小说总体设计画像\n\n设计\n\n# 未来100章大型剧情块\n\n旧版剧情\n\n# 未来十章逐章小纲\n\n十章\n\n# 当前状态、未兑现承诺与作者备注\n\n状态\n"
    sections = parse_book_sections(legacy)
    assert sections["long_plan"] == "旧版剧情"
    rewritten = compose_book_content(sections)
    assert "# 当前中期规划窗口" in rewritten
    assert "# 未来100章大型剧情块" not in rewritten


def test_old_book_without_creative_files_still_loads_and_legacy_proposal_is_not_approved(tmp_path: Path) -> None:
    book_dir = tmp_path / "old-book"
    book_dir.mkdir()
    (book_dir / "BOOK.md").write_text("# 小说总体设计画像\n\n旧书", encoding="utf-8")
    (book_dir / "PROMPTS.md").write_text("", encoding="utf-8")
    (book_dir / "PROPOSAL.md").write_text("旧书 Proposal", encoding="utf-8")
    (book_dir / "chapters").mkdir()

    payload = read_book_payload("old-book", tmp_path)

    assert payload["creative_state"]["proposal"] == {
        "origin": "legacy_unknown",
        "status": "draft",
    }
    assert payload["creative_state"]["fantasy_seed"] == {"origin": "empty", "status": "empty"}
    assert not (book_dir / "FANTASY_SEED.md").exists()
    assert not (book_dir / "WORLD_VISION.md").exists()
    assert not (book_dir / "CREATIVE_STATE.json").exists()


def test_creative_state_sources_and_explicit_approval_api(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    local_client = TestClient(app)
    assert local_client.post("/api/books", json={"book_id": "creative"}).status_code == 201

    generated = local_client.put(
        "/api/books/creative/fantasy-seed",
        json={"content": "MODEL_GENERATED_SEED", "origin": "model_generated"},
    )
    assert generated.status_code == 200
    assert generated.json()["creative_state"]["fantasy_seed"] == {
        "origin": "model_generated",
        "status": "draft",
    }

    selected = local_client.put(
        "/api/books/creative/world-vision",
        json={"content": "MODEL_SELECTED_WORLD", "origin": "model_selected"},
    )
    assert selected.status_code == 200
    assert selected.json()["creative_state"]["world_vision"] == {
        "origin": "model_selected",
        "status": "draft",
    }
    proposal = local_client.put(
        "/api/books/creative/proposal",
        json={"content": "MODEL_SELECTED_PROGRAM", "origin": "model_selected"},
    )
    assert proposal.json()["creative_state"]["proposal"] == {
        "origin": "model_selected",
        "status": "draft",
    }

    cannot_approve_in_put = local_client.put(
        "/api/books/creative/proposal",
        json={"content": "FORGED_APPROVAL", "origin": "author_approved"},
    )
    assert cannot_approve_in_put.status_code == 422

    approved_seed = local_client.post("/api/books/creative/fantasy-seed/approve")
    assert approved_seed.json()["creative_state"]["fantasy_seed"]["status"] == "author_approved"
    approved_world = local_client.post("/api/books/creative/world-vision/approve")
    assert approved_world.json()["creative_state"]["world_vision"]["status"] == "author_approved"
    approved_proposal = local_client.post("/api/books/creative/proposal/approve")
    assert approved_proposal.json()["creative_state"]["proposal"]["status"] == "author_approved"

    edited = local_client.put(
        "/api/books/creative/fantasy-seed",
        json={"content": "AUTHOR_EDITED_AFTER_APPROVAL"},
    )
    assert edited.json()["creative_state"]["fantasy_seed"] == {
        "origin": "author_edited",
        "status": "draft",
    }
    edited_world = local_client.put(
        "/api/books/creative/world-vision",
        json={"content": "AUTHOR_EDITED_WORLD_AFTER_APPROVAL"},
    )
    assert edited_world.json()["creative_state"]["world_vision"] == {
        "origin": "author_edited",
        "status": "draft",
    }
    edited_proposal = local_client.put(
        "/api/books/creative/proposal",
        json={"content": "AUTHOR_EDITED_PROGRAM_AFTER_APPROVAL"},
    )
    assert edited_proposal.json()["creative_state"]["proposal"] == {
        "origin": "author_edited",
        "status": "draft",
    }


def test_creative_prompt_approval_boundaries_and_outline_authority(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    local_client = TestClient(app)
    assert local_client.post("/api/books", json={"book_id": "gates"}).status_code == 201
    base = {
        "book_id": "gates",
        "template": "VISIBLE_TEMPLATE",
        "creative_direction": "AUTHOR_DIRECTION",
        "fantasy_seed": "SEED",
        "world_vision": "WORLD",
        "proposal_context": "PROGRAM",
    }

    assert local_client.post("/api/prompt", json={**base, "mode": "fantasy_seed"}).status_code == 200
    world_blocked = local_client.post("/api/prompt", json={**base, "mode": "world_vision"})
    assert world_blocked.status_code == 422
    assert world_blocked.json()["detail"]["missing_artifacts"] == ["fantasy_seed"]
    program_blocked = local_client.post("/api/prompt", json={**base, "mode": "idea"})
    assert program_blocked.status_code == 422

    for artifact, path in (
        ("fantasy_seed", "fantasy-seed"),
        ("world_vision", "world-vision"),
        ("proposal", "proposal"),
    ):
        saved = local_client.put(
            f"/api/books/gates/{path}",
            json={"content": artifact.upper(), "origin": "model_generated"},
        )
        assert saved.status_code == 200
        assert saved.json()["creative_state"][artifact]["status"] == "draft"

    assert local_client.post("/api/prompt", json={**base, "mode": "outline"}).status_code == 422
    for path in ("fantasy-seed", "world-vision", "proposal"):
        assert local_client.post(f"/api/books/gates/{path}/approve").status_code == 200
    final = local_client.post("/api/prompt", json={**base, "mode": "outline"})
    assert final.status_code == 200
    assert "VISIBLE_TEMPLATE" in final.json()["prompt"]


def test_fantasy_seed_and_world_vision_inputs_are_isolated() -> None:
    fantasy = generate_prompt(
        mode="fantasy_seed",
        template=DEFAULT_PROMPT_TEMPLATES["fantasy_seed"],
        book_content="BOOK_MARKER",
        creative_direction="DIRECTION_MARKER",
        gbrain_inspiration="GBRAIN_MARKER",
        selected_references=[{"program_id": "REFERENCE_MARKER"}],
    )
    for marker in ("BOOK_MARKER", "GBRAIN_MARKER", "REFERENCE_MARKER"):
        assert marker not in fantasy
    for marker in (
        "### 核心幻想",
        "### 主角最强欲望",
        "### 力量占有欲",
        "### 第一次标志性奇观",
        "### 长期增长发动机",
        "### 第一次主动兑现",
        "### 早期兑现（约10章）",
        "### 稳定循环（约30章）",
        "### 中期里程碑",
        "### 远期升格方向",
    ):
        assert marker in fantasy

    world = generate_prompt(
        mode="world_vision",
        template=DEFAULT_PROMPT_TEMPLATES["world_vision"],
        book_content="BOOK_MARKER",
        creative_direction="DIRECTION_MARKER",
        fantasy_seed="APPROVED_SEED_MARKER",
        gbrain_inspiration="GBRAIN_MARKER",
        selected_references=[{"program_id": "REFERENCE_MARKER"}],
        creative_state={"fantasy_seed": {"origin": "author_edited", "status": "author_approved"}},
    )
    assert "APPROVED_SEED_MARKER" in world
    assert "GBRAIN_MARKER" in world
    for marker in ("BOOK_MARKER", "REFERENCE_MARKER"):
        assert marker not in world
    for marker in (
        "世界最震撼的三幅画面",
        "力量的升格方向",
        "世界资源、利益与机会结构",
        "持续冲突来源",
        "第一次决定性兑现",
        "早期成长锚点与长期升格",
        "早期兑现",
        "稳定循环",
        "中期里程碑",
        "远期升格方向",
    ):
        assert marker in world


def test_model_selected_story_program_is_not_outline_authority() -> None:
    state = {
        "fantasy_seed": {"origin": "author_edited", "status": "author_approved"},
        "world_vision": {"origin": "author_edited", "status": "author_approved"},
        "proposal": {"origin": "model_selected", "status": "draft"},
    }
    with pytest.raises(CreativeApprovalError) as error:
        generate_prompt(
            mode="outline",
            template="OUTLINE",
            book_content="BOOK",
            fantasy_seed="SEED",
            world_vision="WORLD",
            proposal_context="SELECTED_PROGRAM",
            creative_state=state,
        )
    assert error.value.missing_artifacts == ["proposal"]


def test_only_validated_reference_programs_are_loaded(tmp_path: Path) -> None:
    valid = {"program_id": "valid", "status": "VALIDATED", "story_phase": "one"}
    draft = {"program_id": "draft", "status": "DRAFT", "story_phase": "two"}
    (tmp_path / "valid.yaml").write_text(yaml.safe_dump(valid), encoding="utf-8")
    (tmp_path / "draft.yaml").write_text(yaml.safe_dump(draft), encoding="utf-8")
    loaded = load_validated_references(tmp_path)
    assert [item["program_id"] for item in loaded] == ["valid"]


def test_prompt_is_built_from_submitted_visible_inputs() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="VISIBLE TEMPLATE",
        book_content="VISIBLE IDEA",
        selected_references=[{"program_id": "visible-program", "output_state": "visible state"}],
        **approved_creative_inputs(),
    )
    assert "VISIBLE TEMPLATE" in prompt
    assert "VISIBLE IDEA" in prompt
    assert "visible-program" in prompt
    assert "hidden" not in prompt


def test_outline_uses_only_the_author_edited_proposal_context() -> None:
    prompt = generate_prompt(
        mode="outline",
        template=DEFAULT_PROMPT_TEMPLATES["outline"],
        book_content="BOOK_DIRECTION",
        proposal_context="## 候选1：保留方案\nSELECTED_IDEA_ALPHA",
        creative_state=APPROVED_CREATIVE_STATE,
        fantasy_seed="APPROVED_SEED",
        world_vision="APPROVED_WORLD",
    )
    assert "SELECTED_IDEA_ALPHA" in prompt
    assert "UNSELECTED_IDEA_BETA" not in prompt
    assert "已批准的三份创意产物高于产品默认模板" in prompt


def test_outline_without_author_approval_is_blocked_even_with_proposal_text() -> None:
    with pytest.raises(CreativeApprovalError) as error:
        generate_prompt(
            mode="outline",
            template="OUTLINE TEMPLATE",
            book_content="BOOK_DIRECTION",
            proposal_context="MODEL_SELECTED_BUT_NOT_APPROVED",
        )
    assert set(error.value.missing_artifacts) == {"fantasy_seed", "world_vision", "proposal"}
    assert "模型生成或模型选择不等于作者批准" in str(error.value)


def test_chapter_prep_builds_eight_field_contract_from_the_selected_plan() -> None:
    plan = """## 第1章：仓库门口的急单
具体剧情：主角在夜班仓库接到临时调度。
结果 / 状态变化：他拿到第一张可验证的路线单。
叙事功能：把职业优势落到现场。
结尾推动：下一章必须去第二个仓库核对记录。"""
    prompt = generate_prompt(
        mode="chapter_prep",
        template=DEFAULT_PROMPT_TEMPLATES["chapter_prep"],
        book_content="# 小说总体设计画像\n\n## 7. 叙事结构\n连续推进\n\n# 当前状态、未兑现承诺与作者备注\n\n当前状态：夜班开始。",
        current_long_block="第1—10章：冷链路线验证",
        current_chapter_plan=plan,
        previous_chapter_text="# 第1章正文\n\n上一章最后一句：门锁响了。",
        recent_summaries="最近摘要：主角刚失去公司担保。",
    )
    assert plan in prompt
    assert "上一章最后一句：门锁响了" in prompt
    for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ):
        assert f"{field}：" in prompt

    fixture = "\n".join(f"{field}：fixture" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    validate_current_outline(fixture)


def test_parse_outline_fields_accepts_existing_inline_format() -> None:
    values = parse_outline_fields(OUTLINE)
    assert values == {field: "内容" for field in REQUIRED_OUTLINE_FIELDS}


def test_parse_outline_fields_accepts_all_multiline_format() -> None:
    outline = "\n".join(
        f"{field}：\n{field}第一行\n{field}第二行"
        for field in REQUIRED_OUTLINE_FIELDS
    )
    values = parse_outline_fields(outline)
    assert values["触发事件"] == "触发事件第一行\n触发事件第二行"
    assert values["结尾推动力"] == "结尾推动力第一行\n结尾推动力第二行"
    validate_current_outline(outline)


def test_parse_outline_fields_accepts_mixed_inline_and_multiline_format() -> None:
    outline = "\n".join(
        (
            "触发事件：同行内容",
            "推动事件的人：",
            "多行推动者内容",
            "主角行动：同行行动",
            "对手或世界反应：",
            "多行反应第一行",
            "多行反应第二行",
            "直接结果：同行结果",
            "状态变化：",
            "多行状态",
            "叙事功能：同行功能",
            "结尾推动力：",
            "多行推动力",
        )
    )
    values = parse_outline_fields(outline)
    assert values["触发事件"] == "同行内容"
    assert values["推动事件的人"] == "多行推动者内容"
    assert values["对手或世界反应"] == "多行反应第一行\n多行反应第二行"
    assert values["结尾推动力"] == "多行推动力"
    validate_current_outline(outline)


def test_parse_outline_fields_still_rejects_missing_or_empty_fields() -> None:
    missing = "\n".join(
        f"{field}：内容"
        for field in REQUIRED_OUTLINE_FIELDS
        if field != "直接结果"
    )
    with pytest.raises(HardGateError) as missing_error:
        validate_current_outline(missing)
    assert missing_error.value.missing_fields == ["直接结果"]

    empty = "\n".join(
        f"{field}：" if field == "直接结果" else f"{field}：内容"
        for field in REQUIRED_OUTLINE_FIELDS
    )
    with pytest.raises(HardGateError) as empty_error:
        validate_current_outline(empty)
    assert empty_error.value.missing_fields == ["直接结果"]


def test_parse_outline_fields_does_not_swallow_markdown_section_after_last_field() -> None:
    outline = OUTLINE + "\n\n## 专项建议\nOpening：启用；只作为运行建议。"
    values = parse_outline_fields(outline)
    assert values["结尾推动力"] == "内容"
    assert "Opening" not in values["结尾推动力"]
    validate_current_outline(outline)


def test_real_parallel_pilot_multiline_response_is_a_fixed_parser_regression() -> None:
    response_path = (
        Path(__file__).parents[1]
        / "books"
        / "real-exp-prose-execution-parallel-v1"
        / "candidate-c"
        / "chapter-03"
        / "director_response.md"
    )
    response = response_path.read_text(encoding="utf-8")
    values = parse_outline_fields(response)
    validate_current_outline(response)
    assert values["触发事件"].startswith("沈砚沿带冷风的上行斜缝")
    assert values["结尾推动力"].startswith("就在第一批人和一小片土地完成接入")
    assert "专项建议" not in values["结尾推动力"]
    assert "沈砚沿带冷风的上行斜缝" in render_event_contract(response)


def test_chapter_prep_chapter_two_uses_chapter_two_plan_and_chapter_one_prose() -> None:
    prompt = generate_prompt(
        mode="chapter_prep",
        template="CHAPTER PREP TEMPLATE",
        book_content="BOOK",
        current_chapter_plan="## 第2章：第二章计划\nCHAPTER_TWO_PLAN_MARKER",
        previous_chapter_text="# 第1章正文\n\nCHAPTER_ONE_FORMAL_PROSE_MARKER",
    )
    assert "CHAPTER_TWO_PLAN_MARKER" in prompt
    assert "CHAPTER_ONE_FORMAL_PROSE_MARKER" in prompt
    assert "CHAPTER_ONE_PLAN_MARKER" not in prompt


def test_director_prompt_contains_chapter_budget_boundary() -> None:
    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="BOOK",
        chapter_number=1,
        current_long_block="CURRENT_BLOCK",
        current_chapter_plan="CURRENT_CHAPTER_PLAN",
    )
    assert DIRECTOR_CHAPTER_BUDGET_RULE in prompt


def test_director_prompt_uses_recent_three_summaries_and_soft_repetition_rule() -> None:
    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="BOOK",
        chapter_number=4,
        current_long_block="CURRENT_BLOCK",
        current_chapter_plan="CURRENT_CHAPTER_PLAN",
        recent_summaries=(
            "第1章：OLD_SUMMARY\n"
            "第2章：SECOND_SUMMARY\n"
            "第3章：THIRD_SUMMARY\n"
            "第4章：FOURTH_SUMMARY"
        ),
    )
    assert DIRECTOR_REPETITION_RULE in prompt
    assert "最近 1—3 章摘要" in prompt
    assert "第1章：OLD_SUMMARY" not in prompt
    for marker in ("第2章：SECOND_SUMMARY", "第3章：THIRD_SUMMARY", "第4章：FOURTH_SUMMARY"):
        assert marker in prompt
    for field in REQUIRED_OUTLINE_FIELDS:
        assert prompt.count(f"{field}：") == 1


def test_stage_change_planning_rule_is_in_outline_and_review() -> None:
    assert STAGE_CHANGE_PLANNING_RULE in DEFAULT_PROMPT_TEMPLATES["outline"]
    assert STAGE_CHANGE_PLANNING_RULE in DEFAULT_PROMPT_TEMPLATES["review"]
    for marker in (
        "事件推进和阶段推进",
        "主角主动目标改变或升级",
        "章末推动力不默认等于新危险",
        "不是固定频率、评分项或 Hard Gate",
    ):
        assert marker in STAGE_CHANGE_PLANNING_RULE


def test_writer_result_stop_rule_is_rendered_once_in_single_and_hybrid_writer_prompts() -> None:
    single = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="BOOK",
        current_outline=OUTLINE,
    )
    assert single.count(RESULT_STOP_RULE) == 1

    hybrid = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="BOOK",
        current_outline=OUTLINE,
        primary_draft="PRIMARY_DRAFT",
    )
    assert hybrid.count(RESULT_STOP_RULE) == 1

    integrator = generate_prompt(
        mode="chapter_integrator",
        template="",
        book_content="BOOK",
        current_outline=OUTLINE,
        primary_draft="PRIMARY_DRAFT",
    )
    assert integrator.count(RESULT_STOP_RULE) == 1


def test_opening_three_chapter_rules_are_conditionally_rendered_in_active_prompts() -> None:
    assert OPENING_THREE_CHAPTER_CONTRACT in DEFAULT_PROMPT_TEMPLATES["outline"]
    assert "具体的人正在面对什么问题" in OPENING_THREE_CHAPTER_CONTRACT
    assert "普通读者用一句朴素的话暂时知道主角现在能做什么" in OPENING_THREE_CHAPTER_CONTRACT
    assert "世界尺度 → 当前时代/大秩序/大危机" not in OPENING_THREE_CHAPTER_CONTRACT

    director = generate_prompt(
        mode="director",
        template="",
        book_content="BOOK",
        chapter_number=1,
    )
    prep = generate_prompt(
        mode="chapter_prep",
        template=DEFAULT_PROMPT_TEMPLATES["chapter_prep"],
        book_content="BOOK",
        chapter_number=2,
    )
    writer = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="BOOK",
        chapter_number=3,
        current_outline=OUTLINE,
    )
    hybrid = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="BOOK",
        chapter_number=3,
        current_outline=OUTLINE,
        primary_draft="PRIMARY_DRAFT",
    )
    for prompt in (director, prep, writer, hybrid):
        assert prompt.count(OPENING_THREE_CHAPTER_CONTRACT) == 1

    default_chapter = generate_prompt(
        mode="director",
        template="",
        book_content="BOOK",
        chapter_number=0,
    )
    assert OPENING_THREE_CHAPTER_CONTRACT not in default_chapter

    later_writer = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="BOOK",
        chapter_number=4,
        current_outline=OUTLINE,
    )
    assert OPENING_THREE_CHAPTER_CONTRACT not in later_writer


def test_clipboard_code_uses_prompt_textarea_value() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "navigator.clipboard.writeText(text)" in js
    assert 'const text = $("prompt-text").value;' in js


def test_prompt_generation_and_response_do_not_write_book_before_save(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client.post("/api/books", json={"book_id": "demo"})
    before = (tmp_path / "demo" / "BOOK.md").read_text(encoding="utf-8")
    response = client.post(
        "/api/prompt",
        json={
            "mode": "fantasy_seed",
            "template": "template",
            "book_content": "page-visible-book",
            "creative_direction": "author direction",
            "selected_references": [],
        },
    )
    assert response.status_code == 200
    assert (tmp_path / "demo" / "BOOK.md").read_text(encoding="utf-8") == before


def test_empty_eight_outline_fields_block_chapter_prompt() -> None:
    empty = "\n".join(f"{field}：" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    try:
        generate_prompt(
            mode="chapter",
            template="template",
            book_content="book",
            current_outline=empty,
        )
    except HardGateError as error:
        assert len(error.missing_fields) == 8
    else:
        raise AssertionError("empty outline fields must block chapter prompt")


def test_non_empty_eight_outline_fields_allow_chapter_prompt() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="template",
        book_content="book",
        current_outline=outline,
    )
    assert "template" in prompt
    assert "结尾推动力：内容" in prompt


def test_chapter_prompt_includes_rhythm_profile_without_full_plan_or_strengths() -> None:
    book = """# 小说总体设计画像

## 7. 叙事结构
视角 marker

## 8. 文风与可操作参数
文风 marker

## 9. 对话特点
对话 marker

## 10. 节奏结构
RHYTHM_MARKER_ALPHA

## 12. 当前设计最强点与最弱点
STRENGTHS_MARKER_BETA

# 未来100章大型剧情块
FULL_PLAN_MARKER_GAMMA
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=book,
        current_outline=outline,
    )
    assert "RHYTHM_MARKER_ALPHA" in prompt
    assert "FULL_PLAN_MARKER_GAMMA" not in prompt
    assert "STRENGTHS_MARKER_BETA" not in prompt


def test_chapter_prompt_uses_formal_body_as_status_authority() -> None:
    book = """# 小说总体设计画像

## 7. 叙事结构
NARRATIVE_MARKER

## 8. 文风与可操作参数
PROSE_MARKER

## 9. 对话特点
DIALOGUE_MARKER

## 10. 节奏结构
RHYTHM_MARKER

# 当前状态、未兑现承诺与作者备注
STATUS_MARKER
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=book,
        current_outline=outline,
    )
    assert prompt.count("STATUS_MARKER") == 1
    for marker in (
        "已批准的正式前文；已经发生事实的最高来源",
        "是正式正文的压缩索引",
        "与正式正文冲突时以正式正文为准",
        "只决定尚未发生的内容",
        "Curator 负责在 Curator Audit 中暴露",
        "Primary 不承担冲突报告或其它 pipeline bookkeeping",
    ):
        assert marker in prompt


def test_legacy_chapter_template_receives_prose_contract_once() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="LEGACY CHAPTER TEMPLATE",
        book_content="",
        current_outline=outline,
    )
    assert "# Story MVP Prose Realization Contract" in prompt
    assert prompt.count(PROSE_REALIZATION_CONTRACT) == 1


def test_default_chapter_prompt_has_no_source_style_leakage() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=outline,
    )
    for marker in (
        "《第一序列》", "《将夜》", "《诡秘之主》", "模仿《", "仿写《",
        ".agents/skills/novel-prose-realization",
    ):
        assert marker not in prompt


def test_chapter_contract_is_compressed_without_generic_prose_sections() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=outline,
    )
    # 重复的通用 prose 说明与多 Writer 职责已被删除
    for marker in (
        "## Scene controls",
        "## Diction and sentence realization",
        "## Writers",
        "Writer A — Scene Draft",
        "锚点→动作→反应→条件改变",
    ):
        assert marker not in prompt
    # 只保留真正影响当前动作的短执行投影
    for marker in (
        "连续性应通过自然动作和场景表现",
        "不要为了证明物品归属、数量或交易完成而重复盘点已经清楚的事实",
        "chapter-NNNN.md",
        "不是禁词表、固定句长或硬性风格评分",
    ):
        assert marker in prompt
    # 未引入新风格门禁
    for marker in ("句长评分", "AI 检测", "词汇黑名单"):
        assert marker not in prompt
    for marker in (
        "《第一序列》", "《将夜》", "《诡秘之主》",
        "会说话的肘子", "猫腻", "爱潜水的乌贼", "C:\\dev\\tgn-story-mvp",
    ):
        assert marker not in prompt


def test_chapter_template_is_single_writer_direct_writing() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["chapter"]
    assert "本次为单 Writer 直接写作" in template
    assert "直接写出可提交的正式正文" in template
    assert "选择性展开" in template
    assert not _WRITER_ABC_PATTERN.search(template)
    for marker in ("串行写作协议", "SUBAGENT_MODE"):
        assert marker not in template


def test_outline_template_requests_executable_prose_profile() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["outline"]
    assert "已批准的三份创意产物高于产品默认模板" in template
    assert "内部因果必须可信，但可信不等于现代程序真实" in template
    assert "核心幻想、力量占有欲、主角欲望" in template
    assert "代价或余波（可选）" in template
    assert "本批核心幻想兑现" in template
    assert "不要求每章都成长或结算" in template


def test_approved_chapter_gets_correct_numbered_markdown_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    created = client.post("/api/books", json={"book_id": "demo"})
    assert created.status_code == 201
    saved = client.post(
        "/api/books/demo/chapters",
        json={"chapter_number": 7, "content": "chapter body"},
    )
    assert saved.status_code == 200
    assert saved.json()["file"] == "chapter-0007.md"
    assert (tmp_path / "demo" / "chapters" / "chapter-0007.md").read_text(encoding="utf-8") == "chapter body"
    read_saved = client.get("/api/books/demo/chapters/7")
    read_missing = client.get("/api/books/demo/chapters/6")
    assert read_saved.status_code == 200
    assert read_saved.json()["content"] == "chapter body"
    assert read_missing.status_code == 200
    assert read_missing.json()["content"] == ""
    duplicate = client.post(
        "/api/books/demo/chapters",
        json={"chapter_number": 7, "content": "replacement body"},
    )
    assert duplicate.status_code == 400
    assert "已经存在" in duplicate.json()["detail"]
    assert (tmp_path / "demo" / "chapters" / "chapter-0007.md").read_text(encoding="utf-8") == "chapter body"


def test_gbrain_query_calls_public_cli_and_preserves_stdout(monkeypatch) -> None:
    calls: dict[str, object] = {}

    monkeypatch.setattr(gbrain_module.shutil, "which", lambda name: "gbrain.CMD")

    def fake_run(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="[0.9] slug -- raw result", stderr="")

    monkeypatch.setattr(gbrain_module.subprocess, "run", fake_run)
    assert query_gbrain("方向查询") == "[0.9] slug -- raw result"
    assert calls["command"][:2] == ["gbrain.CMD", "query"]
    assert "方向查询" in calls["command"]
    assert "--limit" in calls["command"]
    assert "8" in calls["command"]
    assert "--detail" in calls["command"]
    assert "--scope" in calls["command"]
    assert NOVEL_GBRAIN_SCOPE in calls["command"]
    assert calls["kwargs"]["capture_output"] is True


def test_gbrain_get_calls_public_cli(monkeypatch) -> None:
    calls: dict[str, object] = {}
    monkeypatch.setattr(gbrain_module.shutil, "which", lambda name: "gbrain.CMD")

    def fake_run(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="---\ntype: concept\n---\n\n## Mechanism\n\nfull page", stderr="")

    monkeypatch.setattr(gbrain_module.subprocess, "run", fake_run)
    assert "## Mechanism" in gbrain_module.get_gbrain("mechanisms/example")
    assert calls["command"] == ["gbrain.CMD", "get", "mechanisms/example"]


def test_gbrain_query_uses_bun_cli_when_path_command_is_missing(tmp_path: Path, monkeypatch) -> None:
    cli_file = tmp_path / "src" / "cli.ts"
    cli_file.parent.mkdir()
    cli_file.write_text("// test cli", encoding="utf-8")
    monkeypatch.setattr(gbrain_module, "HERMES_CLI", cli_file)

    def fake_which(name: str):
        return {"gbrain": None, "bun": "bun.exe"}.get(name)

    monkeypatch.setattr(gbrain_module.shutil, "which", fake_which)
    assert resolve_command_prefix() == ["bun.exe", "run", str(cli_file)]


def test_failed_gbrain_query_is_returned_as_error_without_fake_result(monkeypatch) -> None:
    def fail_query(**_kwargs):
        raise GBrainQueryError("真实 CLI 失败")

    monkeypatch.setattr(app_module, "retrieve_gbrain", fail_query)
    response = client.post("/api/gbrain/query", json={"mode": "idea"})
    assert response.status_code == 502
    assert response.json()["detail"] == "真实 CLI 失败"
    assert "result" not in response.json()


def test_story_program_uses_approved_creative_inputs_and_optional_gbrain() -> None:
    prompt = generate_prompt(
        mode="idea",
        template="IDEA TEMPLATE",
        book_content="",
        creative_direction="都市异能，信息差优势",
        gbrain_inspiration="[0.9] mechanism -- 长线换发动机",
        selected_references=[{"program_id": "manual-reference"}],
        creative_state={"world_vision": {"origin": "author_edited", "status": "author_approved"}},
        fantasy_seed="SEED_MARKER",
        world_vision="WORLD_MARKER",
    )
    assert "都市异能，信息差优势" in prompt
    assert "长线换发动机" in prompt
    assert "GBrain Inspiration Results（可选，只借鉴长期故事结构" in prompt
    assert "SEED_MARKER" in prompt
    assert "WORLD_MARKER" in prompt
    assert "manual-reference" in prompt


def test_world_vision_accepts_optional_gbrain_without_replacing_seed() -> None:
    prompt = generate_prompt(
        mode="world_vision",
        template="WORLD TEMPLATE",
        book_content="",
        creative_direction="玄幻成长",
        fantasy_seed="APPROVED_SEED_MARKER",
        gbrain_inspiration="WORLD_FANTASY_MARKER",
        creative_state={"fantasy_seed": {"origin": "author_edited", "status": "author_approved"}},
    )
    assert "APPROVED_SEED_MARKER" in prompt
    assert "WORLD_FANTASY_MARKER" in prompt
    assert "不能覆盖已批准 Fantasy Seed" in prompt


def test_gbrain_result_enters_outline_prompt() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="OUTLINE TEMPLATE",
        book_content="BOOK CONTENT",
        creative_direction="AUTHOR_DIRECTION_ALPHA",
        gbrain_inspiration="Book DNA：阶段回报窗口",
        **approved_creative_inputs(),
    )
    assert "AUTHOR_DIRECTION_ALPHA" in prompt
    assert "阶段回报窗口" in prompt


def test_gbrain_result_enters_review_prompt() -> None:
    prompt = generate_prompt(
        mode="review",
        template="REVIEW TEMPLATE",
        book_content="# 小说总体设计画像\n\n## 0. 本书成长基因图\n\n知识 → 职业 → 世界入口",
        creative_direction="求生建造",
        gbrain_inspiration="Contrast：从个人套利转为组织能力",
        actual_summaries="实际十章内容",
    )
    assert "求生建造" in prompt
    assert "组织能力" in prompt
    assert "知识 → 职业 → 世界入口" in prompt


def test_review_prompt_discusses_growth_loop_variation() -> None:
    prompt = generate_prompt(
        mode="review",
        template=DEFAULT_PROMPT_TEMPLATES["review"],
        book_content="# 小说总体设计画像\n\n## 0. 本书成长基因图\n\n规则理解 × 关系网络",
    )
    assert "本书成长基因图" in prompt
    assert "核心幻想是否仍在兑现" in prompt
    assert "一级成长是否仍是主轴" in prompt
    assert "幻想盈余是否为正" in prompt
    assert "冲突是否过度理性化" in prompt
    assert "世界是否被程序化" in prompt


def test_outline_prompt_has_exact_book_headings_and_concrete_formats() -> None:
    prompt = generate_prompt(
        mode="outline",
        template=DEFAULT_PROMPT_TEMPLATES["outline"],
        book_content="BOOK",
        **approved_creative_inputs(),
    )
    for heading in (
        "# 小说总体设计画像",
        "# 当前中期规划窗口",
        "# 未来十章逐章小纲",
        "# 当前状态、未兑现承诺与作者备注",
    ):
        assert heading in prompt
    assert "## 0. 本书成长基因图" in prompt
    assert "已批准幻想不变量" in prompt
    assert "主角核心欲望与超越" in prompt
    assert "一级成长主轴" in prompt
    assert "核心优势阶段升格" in prompt
    assert "主循环" in prompt
    assert "成本节奏" in prompt
    assert "POWER_BREAKTHROUGH" not in prompt
    assert "不强制每块失去或承担什么" in prompt
    assert "每块必须公开验证" not in prompt
    assert "通常约 4—10 块" in prompt
    assert all(f"## {number}." in prompt for number in range(1, 13))
    assert "完整输出当前窗口的所有剧情块" in prompt
    assert "覆盖第1章到本窗口预计终点" in prompt
    assert "规划范围：预计第1—N章" in prompt
    assert "窗口终点：" in prompt
    assert "具体发生" in prompt
    assert "Outline Story Anchor Density" in prompt
    assert "Director 可以直接执行的故事骨架" in prompt
    assert "通常 3—5 个锚点" in prompt
    assert "只有很短的剧情块可以 2 个" in prompt
    assert "这只是内容密度参考，不是 Hard Gate" in prompt
    assert "锚点是故事转折，不是场景分镜或操作步骤" in prompt
    assert "提高故事确定性，不是提高施工步骤确定性" in prompt
    assert "推进、转折或结算当前剧情块中的某个故事锚点" in prompt
    assert "不要为了填章数，把一个锚点拆成连续几章" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt
    assert "第一章开篇策略" in prompt
    assert "本批核心幻想兑现" in prompt
    assert "不要求每章都成长或结算" in prompt


def test_long_form_pacing_uses_soft_anchors_and_dynamic_outline_window() -> None:
    fantasy = generate_prompt(
        mode="fantasy_seed",
        template=DEFAULT_PROMPT_TEMPLATES["fantasy_seed"],
        book_content="",
        creative_direction="DIRECTION",
    )
    assert "### 早期兑现（约10章）" in fantasy
    assert "### 稳定循环（约30章）" in fantasy
    assert "### 中期里程碑" in fantasy
    assert "### 远期升格方向" in fantasy
    assert "不是第10章的固定期限" in fantasy

    world = generate_prompt(
        mode="world_vision",
        template=DEFAULT_PROMPT_TEMPLATES["world_vision"],
        book_content="",
        fantasy_seed="旧版 Seed：### 10章超越\n### 30章超越\n### 100章超越",
        creative_state={"fantasy_seed": {"status": "author_approved"}},
    )
    assert "## 早期成长锚点与长期升格" in world
    assert "兼容解释为" in world
    assert "不要因为 legacy 字段名里写着100" in world

    story = generate_prompt(
        mode="idea",
        template=DEFAULT_PROMPT_TEMPLATES["idea"],
        book_content="",
        **approved_creative_inputs(),
    )
    assert "### 早期锚点、中期里程碑与远期升格" in story
    assert "大型阶段不分配固定章节额度" in story
    assert "横向开发" not in story
    assert "不把远期升格强塞进固定百章窗口" in story

    outline = generate_prompt(
        mode="outline",
        template=DEFAULT_PROMPT_TEMPLATES["outline"],
        book_content="BOOK",
        **approved_creative_inputs(),
    )
    assert "# 当前中期规划窗口" in outline
    assert "规划范围：预计第1—N章" in outline
    assert "当前中期规划窗口只展开 Story Program" in outline
    assert "通常约 4—10 块" in outline
    assert "世界坐标与度量尺" in outline
    assert "严格的 T0 快照" in outline
    assert "第一章第一场事件发生前一刻已经真实成立的事实" in outline
    assert "模型已经规划过”不等于“故事已经发生过" in outline
    assert "Current State 与 Future Plan 在时间上必须互斥" in outline
    assert "# 未来100章大型剧情块" not in outline


def test_review_prompt_uses_the_concrete_small_outline_format() -> None:
    prompt = generate_prompt(
        mode="review",
        template=DEFAULT_PROMPT_TEMPLATES["review"],
        book_content="BOOK",
    )
    assert "## 下一批十章总体事件链" in prompt
    assert "3—6 句话" in prompt
    assert "具体剧情：用 2—4 句" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt
    assert "第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点" in prompt


def test_chapter_prompt_does_not_start_a_gbrain_query(monkeypatch) -> None:
    def unexpected_query(_query: str) -> str:
        raise AssertionError("chapter prompt must not query GBrain")

    monkeypatch.setattr(app_module, "retrieve_gbrain", unexpected_query)
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    response = client.post(
        "/api/prompt",
        json={
            "mode": "chapter",
            "template": "CHAPTER TEMPLATE",
            "book_content": "BOOK",
            "current_long_block": "CURRENT_LONG_BLOCK_DELTA",
            "previous_chapter_text": "# 第1章正文\n\n上一章最后一句：门外有人敲门。",
            "current_outline": outline,
            "gbrain_inspiration": "本十章已选灵感",
        },
    )
    assert response.status_code == 200
    assert "本十章已选灵感" in response.json()["prompt"]
    assert "上一章最后一句：门外有人敲门" in response.json()["prompt"]


def test_chapter_prompt_uses_relevant_design_without_full_image_or_plan() -> None:
    book = """# 小说总体设计画像

## 0. 本书成长基因图
GENOME_MARKER_ALPHA；循环在中期换挡。

## 1. 核心类型与读者承诺
主角成长型虚构世界；读者期待能力改变行动空间。

## 2. 世界观结构
WORLD_RULE_ALPHA：两套规则互相咬合。

## 3. 世界如何持续制造剧情压力
WORLD_PRESSURE_BETA：环境压力和敌人试探会推动主角行动。

## 4. 主角模型、人物弧与核心矛盾
PROTAGONIST_STYLE_BETA：发现信息 → 小规模验证 → 隐藏优势。

## 5. 配角与关系系统
RELATION_MARKER_GAMMA：长期关系会改变主角选择。

## 7. 叙事结构
贴近主角第三人称，必要时使用他人反应。

## 8. 文风与可操作参数
短段落、高信息密度、对话用于博弈。

## 9. 对话特点
角色说话都带有交易目的。

## 12. 当前设计最强点与最弱点
强点是资源到身份的因果链。

# 未来100章大型剧情块
FULL_PLAN_SHOULD_NOT_ENTER

# 当前状态、未兑现承诺与作者备注
当前在第一章前。
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=book,
        current_long_block="CURRENT_LONG_BLOCK_DELTA",
        current_outline=outline,
    )
    assert "GENOME_MARKER_ALPHA" in prompt
    assert "WORLD_RULE_ALPHA" in prompt
    assert "WORLD_PRESSURE_BETA" in prompt
    assert "PROTAGONIST_STYLE_BETA" in prompt
    assert "RELATION_MARKER_GAMMA" in prompt
    assert "CURRENT_LONG_BLOCK_DELTA" in prompt
    assert "FULL_PLAN_SHOULD_NOT_ENTER" not in prompt
    assert "## 12. 当前设计最强点与最弱点" not in prompt
    assert "MVP_PRODUCT_DIRECTION" not in prompt
    assert "诡秘之主" not in prompt
    # §0—§5 相关设计经由 BOOK CONTRACT 进入，不再被标为「已经发生，不得修改」
    assert "BOOK CONTRACT——长期设计与稳定方向，不等于已经发生" in prompt
    assert "已经发生，不得修改" not in prompt


def test_page_shows_editable_gbrain_query_and_results() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="creative-direction"' in page.text
    assert 'id="gbrain-query"' in page.text
    assert 'id="gbrain-results"' in page.text
    assert 'id="gbrain-raw-results"' in page.text
    assert 'id="gbrain-rejections"' in page.text
    assert 'id="gbrain-count"' in page.text
    assert 'id="chapter-body-for-save"' in page.text
    assert 'id="chapter-fact-summary"' in page.text
    assert 'id="extract-chapter-body"' in page.text
    assert 'id="design-growth_genome"' in page.text
    assert "当前中期规划窗口（完整 Markdown）" in page.text
    assert 'id="creative-direction" value=""' in page.text
    assert "例如：传统仙侠；资源→战斗→身份" in page.text
    assert "GBrain 范围：修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选" in page.text
    assert "从 GBrain 取灵感" in page.text
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "function gbrainContextPayload" in js
    assert "query_override" in js
    assert "raw_stdout" in js
    assert "POWER_BREAKTHROUGH" not in js
    assert "秘境" not in js
    assert "历史建设" not in js
    assert "都市职业" not in js
    assert "BOOK-aware Retrieval Brief" in page.text
    assert "/api/gbrain/brief" in js
    assert 'long_plan: "# 当前中期规划窗口"' in js
    assert '"# 未来100章大型剧情块": "long_plan"' in js


def test_default_retrieval_query_uses_context_instead_of_generic_prefix() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("function gbrainContextPayload")
    end = js.index("async function setDefaultGbrainQuery", start)
    context_body = js[start:end]
    assert 'book_content: composeBookContent()' in context_body
    assert 'current_long_block' in context_body
    assert 'fantasy_seed' in context_body
    assert 'world_vision' in context_body
    assert 'proposal_context' in context_body
    assert 'current_outline' in context_body
    assert 'recent_summaries' in context_body
    assert 'state.gbrainDefaultBrief = payload.retrieval_brief || ""' in js
    assert 'const manualOverride = query === state.gbrainDefaultBrief ? "" : query;' in js
    assert "主角成长型虚构世界小说" not in js[start:]


def test_current_chapter_prep_controls_and_exact_plan_parser_are_visible() -> None:
    page = client.get("/")
    assert page.status_code == 200
    for marker in (
        'id="load-current-chapter-plan"',
        'id="generate-chapter-prep"',
        'id="current-chapter-plan"',
        'id="apply-chapter-prep"',
        'value="chapter_prep"',
        "未来十章中没有找到第 ${chapterNumber} 章",
    ):
        assert marker in page.text or marker in Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "function parseChapterPlanEntry" in js
    assert "第\\s*(\\d+)\\s*章" in js
    assert "## 第N章：标题" in page.text
    assert "current_chapter_plan: $(\"current-chapter-plan\").value" in js
    assert 'chapter_number: Number($("chapter-number").value)' in js
    assert "const fieldLabels = new Set();" in js
    assert "else if (afterField && trimmed)" in js
    assert 'applyResponseToEditor($("codex-response"), $("current-outline"));' in js


def test_workflow_ui_and_executor_controls_are_visible() -> None:
    page = client.get("/")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    for marker in (
        'id="workflow-panel"',
        'id="workflow-stages"',
        'id="refresh-workflow"',
        'id="executor-mode"',
        'id="codex-task-wrapper"',
        'id="openai-executor-status"',
        'id="settings-button"',
        'id="settings-dialog"',
        'id="settings-api-url"',
        'id="settings-api-key"',
        'id="settings-api-name"',
        'id="save-settings"',
    ):
        assert marker in page.text
    for marker in (
        "/api/books/",
        "/workflow",
        "/api/executors/openai",
        "story-mvp-workflow apply",
        "function refreshWorkflow",
    ):
        assert marker in js


def test_gbrain_results_and_reference_selection_are_invalidated_on_context_changes() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("function invalidateGbrainResults")
    end = js.index("async function requestJson", start)
    invalidation = js[start:end]
    for marker in (
        '$("gbrain-results").value = ""',
        '$("gbrain-raw-results").value = ""',
        '$("gbrain-rejections").value = ""',
        '$("gbrain-count").textContent = "raw 0 / accepted 0 / rejected 0"',
        'GBrain：上下文已变化，请重新查询',
    ):
        assert marker in invalidation
    assert "function clearReferenceSelection" in js
    populate_start = js.index("function populateBook")
    populate_end = js.index("async function refreshBookList", populate_start)
    assert "invalidateGbrainResults(\"切换小说\")" in js[populate_start:populate_end]
    assert "clearReferenceSelection()" in js[populate_start:populate_end]
    mode_start = js.index("async function handlePromptModeChange")
    mode_end = js.index("async function activatePromptMode", mode_start)
    assert "invalidateGbrainResults(\"切换 Prompt 模式\")" in js[mode_start:mode_end]
    assert '"creative-direction", "current-long-block", "current-outline", "recent-summaries"' in js


REAL_COLD_CHAIN_BOOK = """# 小说总体设计画像

## 0. 本书成长基因图
现代都市职业成长；冷链调度；返程空载；仓库时间窗；司机信用；结算与责任。

## 1. 核心类型与读者承诺
现实世界职业成长。

## 2. 世界观结构
司机、仓库、门店、订单和时间窗。

# 当前状态、未兑现承诺与作者备注
现实世界；没有超自然；没有修炼；没有战斗升级；没有副本或异世界。
"""

REAL_COLD_CHAIN_OUTLINE = """触发事件：主角被收走车队权限并接到急单。
推动事件的人：采购和车队负责人。
主角行动：翻出三个月返程空载记录，寻找第一段现实路线。
对手或世界反应：车辆能到第一城，但没有第二城预约号。
直接结果：第一段路线出现，第二段无法直送。
状态变化：主角失去公司担保但保留个人记录。
叙事功能：把职业优势落到现场行动。
结尾推动力：继续寻找夜班仓库节点。
"""

REAL_WORLD_SUPERPOWER_BOOK = """# 小说总体设计画像

## 0. 本书成长基因图
现代都市；现实世界；现实社会结构；存在少量异能；主角拥有异常感知能力。

## 1. 核心类型与读者承诺
职业调查、信息差、人际关系、资源、身份与组织博弈。

## 2. 世界观结构
真实公司、警察、医院、学校、互联网、金融、交通、劳动合同和法律制度；异能不改变社会基础设施。

# 当前状态、未兑现承诺与作者备注
不使用修炼体系；没有境界升级；没有灵气；没有宗门；没有武道等级；没有学院试炼；没有副本；没有遗迹探索；没有异世界穿越。
"""

REAL_WORLD_BOOK = """# 小说总体设计画像
现代都市；现实世界；现实社会结构；没有超自然；没有异能；没有修炼体系。
"""

XIANXIA_BOOK = """# 小说总体设计画像
仙侠世界；修炼体系；境界突破；宗门资源。
"""

REAL_URBAN_FULL_HYBRID_BOOK = """# 小说总体设计画像

## 0. 本书成长基因图
现代都市男频成长爽文。现实社会结构仍然是主要基底，故事主要发生在当代现实城市，公司、大学、医院、警察、互联网、房地产、金融、交通和商业体系都正常存在；这个世界同时存在灵气复苏，一部分人可以修炼，修炼拥有明确境界，城市中存在公开或半公开的宗门、武馆和异常事务机构，部分高阶空间异常会形成副本，某些副本与异世界相连。

## 1. 核心类型与读者承诺
主角通过工作、人际关系、信息差和第一次修炼机会进入更大的世界；异能、修炼、境界、灵气、宗门、武道等级、副本和异世界入口共同组成现代社会与超自然成长体系的咬合。

## 2. 世界观结构
现代社会结构与异常组织、修炼资源、空间入口和不同能力阶段并行运行。
"""

REAL_URBAN_ONLY_OTHERWORLD_BOOK = """# 小说总体设计画像
现代都市；现实世界；存在异能；存在修炼；存在境界；存在宗门；存在副本；存在异世界入口。
本书不使用修炼体系。
"""

REAL_URBAN_ONLY_NO_OTHERWORLD_BOOK = """# 小说总体设计画像
现代都市；现实世界；存在异能；存在修炼；存在境界；存在宗门；存在副本。
本书不使用异世界。
"""

SUPERPOWER_PAGE = """---
type: concept
---

## Mechanism

主角通过一种别人无法获得的信息渠道发现隐藏事实，异常能力只提供信息，不直接解决现实中的执行、关系和责任问题。

## Failure Modes

如果异能直接代替调查、谈判和行动，故事会退化成自动答案机。

## Transfer Boundary

保留信息差与使用限制；具体能力实现服从当前 BOOK。
"""

CULTIVATION_PAGE = """---
type: concept
---

## Mechanism

主角通过吸收灵气修炼功法，不断突破新的境界，并依靠宗门资源成长。

## Transfer Boundary

保留修炼突破，不迁移具体来源故事。
"""

REAL_WORLD_MECHANISM_PAGE = """---
type: concept
---

## Mechanism

主角通过公司记录、医院流程和访谈把异常线索转成可验证的调查行动。

## Transfer Boundary

只迁移调查与责任链，不迁移来源故事。
"""


def _page(heading: str, content: str) -> str:
    return f"---\ntype: concept\n---\n\n## {heading}\n\n{content}\n\n## Transfer Boundary\n\n只迁移抽象结构，不迁移来源故事。"


HYBRID_PAGES = {
    "mechanisms/information-superpower": _page("Mechanism", "异能提供隐藏信息，但不直接解决调查、关系和责任。"),
    "mechanisms/cultivation-entry": _page("Mechanism", "现代社会中的第一次修炼方法通过资源、训练和风险形成成长。"),
    "mechanisms/realm-breakthrough": _page("Core Progression Grammar", "明确境界突破改变行动、资源需求和社会层级。"),
    "mechanisms/modern-sect-network": _page("Mechanism", "现代城市中的宗门通过师承、资源、身份和任务形成协作网络。"),
    "mechanisms/dungeon-loop": _page("Repeatable Reader Loop", "异常入口连接准备资源、局部规则、副本行动和现实社会回报。"),
    "mechanisms/other-world-gateway": _page("World Expansion Grammar", "现代城市中的稳定入口连接异世界，返回资源改变职业与组织关系。"),
    "mechanisms/urban-career-growth": _page("Mechanism", "公司记录、关系和现实职业行动把异常线索变成可验证结果。"),
    "prose-controls/action/action-before-interpretation": _page("Control", "先让位置、目标、操作和反馈发生，再补当前需要的规则。"),
    "syntheses/modern-social-pressure": _page("Shared Tendencies", "社会结构与成长机制共同改变主角的行动空间和关系。"),
}


def test_retrieval_brief_is_book_and_chapter_aware() -> None:
    brief = build_retrieval_brief(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        creative_direction="现代都市职业成长",
        current_long_block="冷链调度中把返程空载接到仓库时间窗。",
        current_outline=REAL_COLD_CHAIN_OUTLINE,
    )
    for marker in (
        "现代都市职业成长",
        "冷链调度",
        "返程空载",
        "仓库时间窗",
        "司机信用",
        "结算与责任",
        "主角被收走车队权限",
        "无超自然",
        "无修炼体系",
        "无战斗升级",
        "无副本",
        "无异世界",
    ):
        assert marker in brief
    assert "主角成长型虚构世界小说" not in brief


def test_real_world_does_not_imply_no_supernatural() -> None:
    constraints = extract_hard_constraints(REAL_WORLD_SUPERPOWER_BOOK)
    forbidden = _forbidden_terms(constraints)
    assert "现实世界" in constraints
    assert "无超自然" not in constraints
    assert "无修炼体系" in constraints
    assert "异能" not in forbidden
    assert "超自然" not in forbidden


def test_superpower_book_brief_preserves_setting_and_does_not_invent_no_supernatural() -> None:
    brief = build_retrieval_brief(
        mode="chapter",
        book_content=REAL_WORLD_SUPERPOWER_BOOK,
        creative_direction="现代都市男频成长小说",
        current_outline="主角用异常感知能力追查物品最近一次主动使用者。",
    )
    for marker in ("现代都市", "现实社会结构", "存在少量异能", "异常感知能力", "职业调查", "组织博弈"):
        assert marker in brief
    assert "明确硬约束：" in brief
    assert "无超自然" not in brief
    assert "无修炼体系" in brief


def test_real_world_superpower_keeps_superpower_mechanism() -> None:
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_SUPERPOWER_BOOK,
        query_func=lambda _query, **_kwargs: "[0.95] mechanisms/information-superpower -- 异能带来的信息差",
        page_func=lambda _slug: SUPERPOWER_PAGE,
    )
    assert result["accepted_count"] == 1
    assert "异能" in result["result"]
    assert "信息渠道" in result["result"]
    assert "自动答案机" in result["result"]


def test_real_world_superpower_still_rejects_cultivation() -> None:
    pages = {
        "mechanisms/information-superpower": SUPERPOWER_PAGE,
        "mechanisms/cultivation-breakthrough": CULTIVATION_PAGE,
    }
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_SUPERPOWER_BOOK,
        query_func=lambda _query, **_kwargs: "\n".join(
            [
                "[0.95] mechanisms/information-superpower -- 异能信息差",
                "[0.94] mechanisms/cultivation-breakthrough -- 修炼境界",
            ]
        ),
        page_func=pages.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == ["mechanisms/information-superpower"]
    assert any(
        item["slug"] == "mechanisms/cultivation-breakthrough"
        and item["reason"] == "与 BOOK 的明确硬约束冲突"
        for item in result["rejected"]
    )


def test_explicit_no_supernatural_rejects_superpower_in_pure_real_book() -> None:
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_BOOK,
        query_func=lambda _query, **_kwargs: "[0.95] mechanisms/information-superpower -- 异能信息差",
        page_func=lambda _slug: SUPERPOWER_PAGE,
    )
    assert result["accepted_count"] == 0
    assert result["result"] == EMPTY_RESULT
    assert result["rejected"][0]["reason"] == "与 BOOK 的明确硬约束冲突"


def test_pure_real_book_keeps_reality_mechanism_and_rejects_forbidden_surfaces() -> None:
    pages = {
        "mechanisms/urban-investigation": REAL_WORLD_MECHANISM_PAGE,
        "mechanisms/information-superpower": SUPERPOWER_PAGE,
        "mechanisms/cultivation-breakthrough": CULTIVATION_PAGE,
    }
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_BOOK,
        query_func=lambda _query, **_kwargs: "\n".join(
            [
                "[0.97] mechanisms/urban-investigation -- 现实职业调查",
                "[0.96] mechanisms/information-superpower -- 异能信息差",
                "[0.95] mechanisms/cultivation-breakthrough -- 修炼境界",
            ]
        ),
        page_func=pages.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == ["mechanisms/urban-investigation"]
    assert "公司记录" in result["result"]
    assert {item["slug"] for item in result["rejected"]} == {
        "mechanisms/information-superpower",
        "mechanisms/cultivation-breakthrough",
    }


def test_xianxia_without_negative_constraints_keeps_cultivation() -> None:
    constraints = extract_hard_constraints(XIANXIA_BOOK)
    assert "现实世界" not in constraints
    assert "无修炼体系" not in constraints
    result = retrieve_gbrain(
        mode="chapter",
        book_content=XIANXIA_BOOK,
        query_func=lambda _query, **_kwargs: "[0.95] mechanisms/cultivation-breakthrough -- 修炼境界",
        page_func=lambda _slug: CULTIVATION_PAGE,
    )
    assert result["accepted_count"] == 1
    assert "修炼" in result["result"]


def test_story_internal_cannot_return_to_old_cultivation_system_is_not_a_genre_ban() -> None:
    constraints = extract_hard_constraints("不可逆事件是：他从此无法回到原本的修炼体系，但也成为旧世界无法再定义的人。")
    assert "无修炼体系" not in constraints
    assert "无超自然" not in constraints


def test_unrelated_no_chance_clause_does_not_become_a_cultivation_genre_ban() -> None:
    constraints = extract_hard_constraints("他必须在一场本来没有胜算的冲突中活下来，否则连继续修炼和进入更高层世界的资格都没有。")
    assert "无修炼体系" not in constraints


def test_explicit_long_cultivation_ban_still_matches_within_one_clause() -> None:
    constraints = extract_hard_constraints("作者要求：不要在故事里使用任何形式的修炼体系。")
    assert "无修炼体系" in constraints


def test_three_fixture_spaces_keep_their_distinct_constraint_semantics() -> None:
    pure_real = extract_hard_constraints(REAL_WORLD_BOOK)
    superpower = extract_hard_constraints(REAL_WORLD_SUPERPOWER_BOOK)
    xianxia = extract_hard_constraints(XIANXIA_BOOK)
    assert "无超自然" in pure_real and "无超自然" not in superpower
    assert "无修炼体系" in pure_real and "无修炼体系" in superpower
    assert "无修炼体系" not in xianxia
    assert "现实世界" in pure_real and "现实世界" in superpower
    assert "现实世界" not in xianxia


def test_real_urban_setting_does_not_imply_any_mechanic_ban() -> None:
    constraints = extract_hard_constraints(REAL_URBAN_FULL_HYBRID_BOOK)
    assert constraints == ["现实世界"]
    assert _forbidden_terms(constraints) == ()


def test_real_urban_hybrid_brief_preserves_all_positive_mechanism_signals() -> None:
    brief = build_retrieval_brief(
        mode="chapter",
        book_content=REAL_URBAN_FULL_HYBRID_BOOK,
        creative_direction="现代都市超凡成长",
        current_outline="主角通过工作和第一次修炼机会进入异常组织，处理副本与异世界入口的现实后果。",
    )
    for marker in ("现代都市", "现实社会", "灵气复苏", "异能", "修炼", "境界", "宗门", "副本", "异世界"):
        assert marker in brief
    for marker in ("无超自然", "无修炼体系", "无副本", "无异世界"):
        assert marker not in brief


def test_real_urban_hybrid_accepts_cultivation_realm_sect_dungeon_and_other_world() -> None:
    slugs = [
        "mechanisms/cultivation-entry",
        "mechanisms/realm-breakthrough",
        "mechanisms/modern-sect-network",
        "mechanisms/dungeon-loop",
        "mechanisms/other-world-gateway",
    ]
    raw = "\n".join(f"[{0.99 - index / 100:.2f}] {slug} -- positive mechanism" for index, slug in enumerate(slugs))
    result = retrieve_gbrain(
        mode="chapter_prep",
        book_content=REAL_URBAN_FULL_HYBRID_BOOK,
        query_func=lambda _query, **_kwargs: raw,
        page_func=HYBRID_PAGES.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == slugs
    assert result["rejected"] == []


def test_real_urban_hybrid_accepts_superpower_career_prose_and_synthesis() -> None:
    slugs = [
        "mechanisms/information-superpower",
        "mechanisms/urban-career-growth",
        "prose-controls/action/action-before-interpretation",
        "syntheses/modern-social-pressure",
    ]
    raw = "\n".join(f"[{0.99 - index / 100:.2f}] {slug} -- positive mechanism" for index, slug in enumerate(slugs))
    result = retrieve_gbrain(
        mode="chapter_prep",
        book_content=REAL_URBAN_FULL_HYBRID_BOOK,
        query_func=lambda _query, **_kwargs: raw,
        page_func=HYBRID_PAGES.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == slugs
    assert result["rejected"] == []


def test_real_urban_only_explicitly_banned_other_world_is_rejected() -> None:
    raw = "\n".join(
        [
            "[0.99] mechanisms/information-superpower -- superpower",
            "[0.98] mechanisms/cultivation-entry -- cultivation",
            "[0.97] mechanisms/realm-breakthrough -- realm",
            "[0.96] mechanisms/modern-sect-network -- sect",
            "[0.95] mechanisms/dungeon-loop -- dungeon",
        ]
    )
    result = retrieve_gbrain(
        mode="chapter_prep",
        book_content=REAL_URBAN_ONLY_NO_OTHERWORLD_BOOK,
        query_func=lambda _query, **_kwargs: raw,
        page_func=HYBRID_PAGES.__getitem__,
    )
    assert result["accepted_count"] == 5
    assert "异能" in result["result"]
    assert "修炼" in result["result"]
    assert "副本" in result["result"]

    gateway = retrieve_gbrain(
        mode="chapter_prep",
        book_content=REAL_URBAN_ONLY_NO_OTHERWORLD_BOOK,
        query_func=lambda _query, **_kwargs: "[0.99] mechanisms/other-world-gateway -- gateway",
        page_func=HYBRID_PAGES.__getitem__,
    )
    assert gateway["accepted_count"] == 0
    assert gateway["rejected"][0]["reason"] == "与 BOOK 的现实模式冲突"

    # chapter 模式组合覆盖：hybrid BOOK × 硬约束过滤 × 上限 2；
    # 被 BOOK 显式禁止的 other-world slug 在 chapter 路径仍被拒绝。
    chapter_raw = "\n".join(
        [
            "[0.99] mechanisms/other-world-gateway -- gateway",
            "[0.98] mechanisms/cultivation-entry -- cultivation",
            "[0.97] mechanisms/realm-breakthrough -- realm",
            "[0.96] mechanisms/modern-sect-network -- sect",
        ]
    )
    chapter = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_URBAN_ONLY_NO_OTHERWORLD_BOOK,
        query_func=lambda _query, **_kwargs: chapter_raw,
        page_func=HYBRID_PAGES.__getitem__,
    )
    assert chapter["final_limit"] == CHAPTER_FINAL_RESULT_LIMIT
    assert chapter["accepted_count"] == CHAPTER_FINAL_RESULT_LIMIT
    assert [item["slug"] for item in chapter["accepted"]] == [
        "mechanisms/cultivation-entry",
        "mechanisms/realm-breakthrough",
    ]
    assert any(
        item["slug"] == "mechanisms/modern-sect-network" and item["reason"] == "超过最终数量上限"
        for item in chapter["rejected"]
    )
    assert any(
        item["slug"] == "mechanisms/other-world-gateway" and item["reason"] == "与 BOOK 的现实模式冲突"
        for item in chapter["rejected"]
    )


def test_real_urban_no_cultivation_does_not_ban_other_world() -> None:
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_URBAN_ONLY_OTHERWORLD_BOOK,
        query_func=lambda _query, **_kwargs: "[0.99] mechanisms/other-world-gateway -- gateway\n[0.98] mechanisms/cultivation-entry -- cultivation",
        page_func=HYBRID_PAGES.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == ["mechanisms/other-world-gateway"]
    assert result["rejected"][0]["slug"] == "mechanisms/cultivation-entry"
    assert result["rejected"][0]["reason"] == "与 BOOK 的现实模式冲突"


def test_planning_retrieval_uses_hidden_keyword_aliases_without_query_embedding(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    seen: list[str] = []

    def fake_query(query: str, **kwargs) -> str:
        seen.append(query)
        assert kwargs["limit"] == QUERY_RECALL_LIMIT
        assert kwargs["detail"] == "medium"
        assert "mechanisms" in kwargs["scope"]
        return "[0.99] mechanisms/world-desire-ladder-v3 -- world fantasy reader desire ladder"

    result = retrieve_gbrain(
        mode="world_vision",
        creative_direction="玄幻成长",
        fantasy_seed="已批准核心幻想：看见别人看不见的路",
        query_func=fake_query,
        page_func=lambda _slug: _page("Mechanism", "世界扩张每一层都新增读者想进入、想获得或想知道的具体欲望。"),
    )
    assert seen == [
        '"world fantasy" OR "world entry" OR "narrative compounding"',
        '"reader coordinates" OR "progression scale" OR "action space scale" OR "expectation ladder" OR "core advantage" OR "world compatibility" OR "power scale" OR "threat scale"',
    ]
    assert result["query_strategy"] == "planning_keyword_aliases"
    assert result["query_texts"] == seen
    assert "看见别人看不见的路" in result["retrieval_brief"]
    assert result["accepted_count"] == 1
    assert result["final_limit"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT


@pytest.mark.parametrize(
    ("outline", "expected", "unexpected"),
    [
        ("本章是三方高压谈判，通过称呼、拒答和报价改变筹码。", "dialogue negotiation", "action combat"),
        ("本章是狭窄石桥上的追逐战，必须写清站位、受力和落点。", "action combat", "dialogue negotiation"),
        ("本章第一次看见远超既有尺度的奇观，天穹与距离发生变化。", "scale anchored wonder", "dialogue negotiation"),
        ("多年后重逢，人物都很克制，用微反应表现想念。", "emotion relationship", "limited reveal"),
        ("主角发现旧物的真相，只能从线索和规则推断一部分。", "evidence first limited reveal", "dialogue negotiation"),
        ("主角第一次进入陌生空间，从入口和边界建立现场。", "action anchored grounding", "payoff power proof"),
        ("本章是低压日常，吃饭休息时让关系通过生活动作显出来。", "ordinary life prose", "action combat"),
    ],
)
def test_chapter_prose_control_keyword_fallback_tracks_scene_family(monkeypatch, outline, expected, unexpected) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    brief = build_retrieval_brief(mode="context_curator", current_outline=outline)
    effective, strategy = default_effective_query("context_curator", brief)
    assert strategy == "prose_control_keyword_aliases"
    assert expected in effective
    assert unexpected not in effective


def test_payoff_scene_no_key_fallback_adds_no_regular_prose_control(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    brief = build_retrieval_brief(
        mode="context_curator",
        current_outline="本章在众人面前完成公开能力证明，结果已经清楚，只需要让现场承认变化。",
    )
    effective, strategy = default_effective_query("context_curator", brief)
    assert effective == ""
    assert strategy == "prose_control_none"

    seen: list[str] = []
    result = retrieve_gbrain(
        mode="context_curator",
        current_outline="本章在众人面前完成公开能力证明，结果已经清楚，只需要让现场承认变化。",
        query_func=lambda query, **_kwargs: seen.append(query) or "",
        page_func=lambda _slug: "",
    )
    assert seen == []
    assert result["query_strategy"] == "prose_control_none"
    assert result["accepted_count"] == 0


def test_no_key_prose_fallback_prefers_reveal_over_incidental_action_terms(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    brief = build_retrieval_brief(
        mode="context_curator",
        current_outline="主角用灰粉、滴水和试压复现裂纹，再据此推断局部规律；只能确认这一部分，来源仍未知。",
    )
    effective, strategy = default_effective_query("context_curator", brief)
    assert strategy == "prose_control_keyword_aliases"
    assert "evidence first limited reveal" in effective


def test_no_key_prose_fallback_does_not_treat_repeated_stance_as_complex_action(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    brief = build_retrieval_brief(
        mode="context_curator",
        current_outline="两人围绕信任边界交换条件，人物几次改变站位观察对方；没有追逐、搜捕、围堵或路线变化。",
    )
    effective, strategy = default_effective_query("context_curator", brief)
    assert effective == ""
    assert strategy == "prose_control_none"


def test_chapter_prose_control_fallback_returns_one_primary_control(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    seen: list[str] = []
    raw = "\n".join([
        "[0.99] prose-controls/action-a -- action combat spatial clarity",
        "[0.98] prose-controls/action-b -- action combat spatial clarity",
        "[0.97] prose-controls/action-c -- action combat spatial clarity",
    ])

    def fake_query(query: str, **_kwargs) -> str:
        seen.append(query)
        return raw

    result = retrieve_gbrain(
        mode="context_curator",
        current_outline="追逐战，写清站位、距离、受力与落点。",
        query_func=fake_query,
        page_func=lambda slug: _page("Mechanism", f"{slug} 的动作写作控制。"),
    )
    assert seen == ['"action combat" OR "spatial clarity"']
    assert result["query_strategy"] == "prose_control_keyword_aliases"
    assert result["final_limit"] == 1
    assert result["accepted_count"] == 1


def test_chapter_prose_control_keeps_semantic_brief_when_embedding_query_is_available(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    brief = build_retrieval_brief(
        mode="context_curator",
        current_outline="高压谈判，通过称呼与拒答改变关系。",
    )
    effective, strategy = default_effective_query("context_curator", brief)
    assert effective == brief
    assert strategy == "semantic_brief"


def test_manual_chapter_gbrain_query_still_overrides_prose_fallback(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    seen: list[str] = []

    def fake_query(query: str, **_kwargs) -> str:
        seen.append(query)
        return "[0.99] prose-controls/manual -- manual"

    result = retrieve_gbrain(
        mode="context_curator",
        current_outline="高压谈判。",
        query_override="manual prose query",
        query_func=fake_query,
        page_func=lambda _slug: _page("Mechanism", "手工选择的正文控制。"),
    )
    assert seen == ["manual prose query"]
    assert result["query_strategy"] == "manual_override"


def test_planning_retrieval_keeps_full_chinese_brief_when_semantic_query_is_available(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    brief = build_retrieval_brief(
        mode="idea",
        creative_direction="玄幻成长",
        fantasy_seed="SEED_ALPHA",
        world_vision="WORLD_BETA",
    )
    effective, strategy = default_effective_query("idea", brief)
    assert effective == brief
    assert strategy == "semantic_brief"
    assert "SEED_ALPHA" in effective
    assert "WORLD_BETA" in effective


def test_story_program_keyword_fallback_merges_craft_and_reward_queries(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    seen: list[str] = []
    pages = {
        "mechanisms/plot": _page("Mechanism", "同一核心能力通过对手与目标变化切换故事发动机。"),
        "mechanisms/thread": _page("Mechanism", "长中短线允许沉睡并在新条件成熟时回流。"),
        "mechanisms/reward": _page("Mechanism", "高价值获得来自当前欲望与故事机会，并改变下一步行动。"),
    }
    def fake_query(query: str, **_kwargs) -> str:
        seen.append(query)
        if "plot engine variation" in query:
            return "[0.99] mechanisms/plot -- plot"
        return "[0.98] mechanisms/thread -- thread\n[0.97] mechanisms/reward -- reward"
    result = retrieve_gbrain(
        mode="idea",
        creative_direction="玄幻成长",
        world_vision="已批准世界幻想",
        query_func=fake_query,
        page_func=pages.__getitem__,
    )
    assert len(seen) == 3
    assert any("plot engine variation" in q for q in seen)
    assert any("reward opportunity" in q for q in seen)
    assert any("longitudinal thread" in q for q in seen)
    assert [item["slug"] for item in result["accepted"]] == [
        "mechanisms/plot", "mechanisms/thread", "mechanisms/reward"
    ]
    assert result["final_limit"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT


def test_world_vision_gbrain_brief_api_keeps_chinese_visible_and_alias_internal(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post(
        "/api/gbrain/brief",
        json={
            "mode": "world_vision",
            "creative_direction": "玄幻成长",
            "fantasy_seed": "已批准幻想：隐藏道路",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "已批准幻想：隐藏道路" in payload["retrieval_brief"]
    assert payload["effective_query"] == '"world fantasy" OR "world entry" OR "narrative compounding"'
    assert payload["query_strategy"] == "planning_keyword_aliases"


def test_gbrain_duplicate_chunks_do_not_consume_multiple_inspiration_slots() -> None:
    raw = "\n".join([
        "[0.99] mechanisms/same-page -- first chunk",
        "[0.98] mechanisms/same-page -- second chunk",
        "[0.97] mechanisms/other-page -- other chunk",
    ])
    parsed = parse_query_results(raw)
    unique = dedupe_query_hits_by_slug(parsed)
    assert [item["slug"] for item in unique] == ["mechanisms/same-page", "mechanisms/other-page"]

    result = retrieve_gbrain(
        mode="outline",
        query_override="manual test",
        query_func=lambda _query, **_kwargs: raw,
        page_func=lambda slug: _page("Mechanism", f"{slug} 的中文抽象机制。"),
    )
    assert result["raw_count"] == 3
    assert result["unique_raw_count"] == 2
    assert result["accepted_count"] == 2
    assert [item["slug"] for item in result["accepted"]] == ["mechanisms/same-page", "mechanisms/other-page"]


def test_query_result_parser_ignores_noise_and_preserves_order() -> None:
    parsed = parse_query_results(
        "杂项\n[0.9] mechanisms/example -- first snippet\ncontinuation noise\n"
        "[0.7] prose-controls/example -- second snippet\n"
    )
    assert [item["slug"] for item in parsed] == ["mechanisms/example", "prose-controls/example"]
    assert parsed[0]["score"] == 0.9
    assert parsed[1]["snippet"] == "second snippet"


def test_novel_source_filter_happens_before_candidate_limit_and_skips_unrelated_pages() -> None:
    raw = "\n".join(
        [
            "[0.99] 30_education/foo -- math",
            "[0.98] 99_system/foo -- system",
            "[0.97] 20_knowledge/foo -- finance",
            "[0.96] 30_education/bar -- education",
            "[0.95] 99_system/bar -- template",
            "[0.94] 20_knowledge/bar -- ai",
            "[0.93] 50_research/foo -- research",
            "[0.92] 99_system/baz -- system",
            "[0.80] arcs/novel-a -- arc",
            "[0.79] mechanisms/novel-b -- mechanism",
        ]
    )
    pages = {
        "arcs/novel-a": _page("Progression", "身份门槛转成关系与行动空间的持续扩张。"),
        "mechanisms/novel-b": _page("Mechanism", "受限优势经过现实行动，转成可验证的成长路径。"),
    }
    calls: list[str] = []

    def fake_query(_query: str, **kwargs) -> str:
        assert kwargs["limit"] == QUERY_RECALL_LIMIT
        assert kwargs["detail"] == "medium"
        assert "mechanisms" in kwargs["scope"]
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return pages[slug]

    result = retrieve_gbrain(mode="outline", book_content="都市成长故事", query_func=fake_query, page_func=fake_get)

    assert calls == ["arcs/novel-a", "mechanisms/novel-b"]
    assert [item["slug"] for item in result["accepted"]] == calls
    assert result["accepted_count"] == 2
    assert all(not slug.startswith(("30_education/", "20_knowledge/", "50_research/", "99_system/")) for slug in calls)
    assert all(
        any(item["slug"] == slug and "不自动使用" in item["reason"] for item in result["rejected"])
        for slug in (
            "30_education/foo",
            "20_knowledge/foo",
            "50_research/foo",
            "99_system/foo",
        )
    )


def test_raw_result_limit_applies_to_novel_candidates_only() -> None:
    non_novel_slugs = [f"30_education/item-{index}" for index in range(20)]
    novel_slugs = [f"mechanisms/novel-{index}" for index in range(10)]
    raw = "\n".join(
        [f"[{1 - index / 100:.2f}] {slug} -- snippet" for index, slug in enumerate(non_novel_slugs + novel_slugs)]
    )
    calls: list[str] = []

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return _page("Evidence", "不属于可提取的抽象区块。")

    result = retrieve_gbrain(
        mode="chapter",
        book_content="都市成长故事",
        query_func=lambda _query, **_kwargs: raw,
        page_func=fake_get,
    )

    assert calls == novel_slugs[:RAW_RESULT_LIMIT]
    assert result["accepted_count"] == 0
    assert sum(item["reason"] == "超过小说候选数量上限" for item in result["rejected"]) == len(novel_slugs) - RAW_RESULT_LIMIT
    assert all(
        any(item["slug"] == slug and "不自动使用" in item["reason"] for item in result["rejected"])
        for slug in non_novel_slugs
    )


def test_xuanhuan_arc_is_accepted_when_abstract_is_transferable() -> None:
    slug = "arcs/rcv0-xx-xuanhuan-xxx"
    result = retrieve_gbrain(
        mode="outline",
        book_content="现代都市超凡成长；现实社会结构；有限异常优势。",
        query_func=lambda _query, **_kwargs: f"[0.9] {slug} -- 玄幻成长 arc",
        page_func=lambda _slug: _page("Progression", "身份门槛推动关系建立，并逐步打开新的行动空间。"),
    )

    assert result["accepted_count"] == 1
    assert result["accepted"][0]["slug"] == slug


def test_chapter_filters_sources_and_builds_bundle_from_full_pages() -> None:
    raw = "\n".join(
        [
            "[0.99] arcs/old -- 修真 arc",
            "[0.98] book-dna/old -- 修炼 book",
            "[0.97] prose-dna/old -- 境界 prose",
            "[0.96] maps/progression -- map",
            "[0.95] prose-controls/action-neutral -- action snippet",
            "[0.94] syntheses/example-neutral -- synthesis snippet",
            "[0.93] mechanisms/example-neutral -- mechanism snippet",
        ]
    )
    calls: list[str] = []
    pages = {
        "prose-controls/action-neutral": _page("Control", "先让位置和操作发生，再补当前需要的规则和反馈。"),
        "syntheses/example-neutral": _page("Shared Tendencies", "阶段推进必须通过具体结果打开新的行动空间。"),
        "mechanisms/example-neutral": _page("Mechanism", "旧资源经过可验证转换，变成新的可用路径。"),
    }

    def fake_query(_query: str, **kwargs) -> str:
        assert kwargs["limit"] == QUERY_RECALL_LIMIT
        assert kwargs["detail"] == "medium"
        assert "mechanisms" in kwargs["scope"]
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return pages[slug]

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        current_outline=REAL_COLD_CHAIN_OUTLINE,
        query_func=fake_query,
        page_func=fake_get,
    )
    assert calls == ["prose-controls/action-neutral", "syntheses/example-neutral"]
    assert result["accepted_count"] == CHAPTER_FINAL_RESULT_LIMIT
    assert result["final_limit"] == CHAPTER_FINAL_RESULT_LIMIT
    assert [item["slug"] for item in result["accepted"]] == calls
    assert "先让位置和操作发生" in result["result"]
    assert "旧资源经过可验证转换" not in result["result"]
    assert "Evidence" not in result["result"]
    assert "source_book_id" not in result["result"]
    assert "修真" not in result["result"]
    assert any(
        item["slug"] == "mechanisms/example-neutral" and item["reason"] == "超过最终数量上限"
        for item in result["rejected"]
    )
    assert any(item["reason"].startswith("chapter 模式不自动使用 arcs") for item in result["rejected"])
    assert any(item["reason"].startswith("chapter 模式不自动使用 book-dna") for item in result["rejected"])
    assert any(item["reason"].startswith("chapter 模式不自动使用 prose-dna") for item in result["rejected"])
    assert any(item["reason"].startswith("chapter 模式不自动使用 maps") for item in result["rejected"])


def test_get_failure_does_not_fallback_to_query_snippet() -> None:
    def fake_query(_query: str, **_kwargs) -> str:
        return "[0.9] mechanisms/failing -- snippet must not enter bundle"

    def fake_get(_slug: str) -> str:
        raise GBrainQueryError("get failed")

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        query_func=fake_query,
        page_func=fake_get,
    )
    assert result["accepted_count"] == 0
    assert result["result"] == EMPTY_RESULT
    assert "snippet must not enter bundle" not in result["result"]
    assert result["rejected"] == [{"slug": "mechanisms/failing", "reason": "完整页面读取失败"}]


def test_query_override_is_effective_but_book_constraints_still_apply() -> None:
    seen: list[str] = []

    def fake_query(query: str, **_kwargs) -> str:
        seen.append(query)
        return "[0.9] book-dna/incompatible -- 修真"

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        query_override="作者当前可见的手工查询",
        query_func=fake_query,
        page_func=lambda _slug: _page("Mechanism", "不应读取"),
    )
    assert seen == ["作者当前可见的手工查询"]
    assert result["effective_query"] == "作者当前可见的手工查询"
    assert result["accepted_count"] == 0
    assert result["rejected"][0]["reason"].startswith("chapter 模式不自动使用 book-dna")


def test_all_incompatible_sources_return_successful_empty_result() -> None:
    called = False

    def fake_query(_query: str, **_kwargs) -> str:
        return "[0.9] book-dna/old -- old\n[0.8] arcs/old -- old"

    def fake_get(_slug: str) -> str:
        nonlocal called
        called = True
        return _page("Mechanism", "should not be read")

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        query_func=fake_query,
        page_func=fake_get,
    )
    assert result["status"] == "available"
    assert result["accepted_count"] == 0
    assert result["result"] == EMPTY_RESULT
    assert called is False


def test_application_and_final_limits_bound_overlong_cli_output() -> None:
    raw = "\n".join(f"[{1 - index / 100:.2f}] mechanisms/item-{index} -- snippet" for index in range(20))
    calls: list[str] = []

    def fake_query(_query: str, **kwargs) -> str:
        assert kwargs["limit"] == QUERY_RECALL_LIMIT
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return _page("Mechanism", f"抽象材料 {slug}")

    result = retrieve_gbrain(mode="idea", book_content="现实世界；无超自然", query_func=fake_query, page_func=fake_get)
    assert result["raw_count"] == 60
    assert result["unique_raw_count"] == 20
    assert result["requested_limit"] == PLANNING_CANDIDATE_INSPECTION_LIMIT
    assert result["final_limit"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    assert result["accepted_count"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    assert len(calls) == CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    assert sum(item["reason"] == "超过小说候选数量上限" for item in result["rejected"]) == 8


def test_planning_query_batches_round_robin_preserve_multiple_retrieval_intents(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def fake_query(query: str, **_kwargs) -> str:
        if "world fantasy" in query:
            return "\n".join(
                f"[{0.99 - index / 100:.2f}] mechanisms/general-{index} -- general"
                for index in range(8)
            )
        if "reader coordinates" in query:
            return (
                "[0.80] syntheses/reader-coordinates -- reader coordinates\n"
                "[0.70] mechanisms/world-compatibility -- compatibility"
            )
        return ""

    result = retrieve_gbrain(
        mode="world_vision",
        fantasy_seed="已批准幻想",
        query_func=fake_query,
        page_func=lambda slug: _page("Mechanism", f"{slug} 的可迁移抽象。"),
    )

    visible = [item["slug"] for item in result["raw_results"]]
    assert visible[:4] == [
        "mechanisms/general-0",
        "syntheses/reader-coordinates",
        "mechanisms/general-1",
        "mechanisms/world-compatibility",
    ]
    assert result["accepted_count"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    assert [item["slug"] for item in result["accepted"]] == visible[:3]
    assert result["requested_limit"] == PLANNING_CANDIDATE_INSPECTION_LIMIT


def test_world_vision_fixed_coordinate_reference_does_not_consume_three_creative_slots(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    raw = "\n".join(
        [
            f"[0.99] {WORLD_COORDINATE_REFERENCE_SLUG} -- reader coordinates",
            "[0.98] mechanisms/world-a -- world a",
            "[0.97] mechanisms/world-b -- world b",
            "[0.96] mechanisms/world-c -- world c",
        ]
    )
    pages = {
        WORLD_COORDINATE_REFERENCE_SLUG: (
            "---\nactive_inspiration: true\n---\n\n"
            "## Guidance\n\n每本书至少建立一把当前主尺，让读者能预测强弱、边界和下一档期待。"
        ),
        "mechanisms/world-a": _page("Mechanism", "世界入口改变行动空间。"),
        "mechanisms/world-b": _page("Mechanism", "世界欲望随地图自然扩大。"),
        "mechanisms/world-c": _page("Mechanism", "上一轮结果改变下一轮世界状态。"),
    }
    result = retrieve_gbrain(
        mode="world_vision",
        fantasy_seed="已批准幻想",
        query_override="manual world query",
        query_func=lambda _query, **_kwargs: raw,
        page_func=pages.__getitem__,
    )
    assert result["coordinate_reference_count"] == 1
    assert result["coordinate_reference"]["slug"] == WORLD_COORDINATE_REFERENCE_SLUG
    assert result["accepted_count"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    assert [item["slug"] for item in result["accepted"]] == [
        "mechanisms/world-a",
        "mechanisms/world-b",
        "mechanisms/world-c",
    ]
    assert "### Fixed Coordinate Reference" in result["result"]
    assert "不占 creative inspiration 名额" in result["result"]
    assert result["result"].count("### Inspiration ") == CREATIVE_PLANNING_FINAL_RESULT_LIMIT


@pytest.mark.parametrize("mode", ["idea", "outline"])
def test_world_coordinate_reference_does_not_reenter_downstream_creative_slots(mode: str) -> None:
    raw = "\n".join(
        [
            f"[0.99] {WORLD_COORDINATE_REFERENCE_SLUG} -- reader coordinates",
            "[0.98] mechanisms/plot-engine-variation-v3 -- plot",
            "[0.97] mechanisms/thread-collision-v3 -- thread",
            "[0.96] mechanisms/earned-high-value-acquisition-v3 -- reward",
        ]
    )
    pages = {
        WORLD_COORDINATE_REFERENCE_SLUG: _page("Guidance", "读者坐标。"),
        "mechanisms/plot-engine-variation-v3": _page("Mechanism", "换 Plot Engine。"),
        "mechanisms/thread-collision-v3": _page("Mechanism", "线程碰撞。"),
        "mechanisms/earned-high-value-acquisition-v3": _page("Mechanism", "高价值获得。"),
    }
    result = retrieve_gbrain(
        mode=mode,
        fantasy_seed="已批准幻想",
        world_vision="已批准世界",
        query_override="manual planning query",
        query_func=lambda _query, **_kwargs: raw,
        page_func=pages.__getitem__,
    )
    accepted_slugs = [item["slug"] for item in result["accepted"]]
    assert WORLD_COORDINATE_REFERENCE_SLUG not in accepted_slugs
    assert accepted_slugs[:3] == [
        "mechanisms/plot-engine-variation-v3",
        "mechanisms/thread-collision-v3",
        "mechanisms/earned-high-value-acquisition-v3",
    ]
    assert any(
        item["slug"] == WORLD_COORDINATE_REFERENCE_SLUG and "不重复占 downstream creative 名额" in item["reason"]
        for item in result["rejected"]
    )


def test_planning_multi_intent_query_tolerates_one_optional_query_failure(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def fake_query(query: str, **_kwargs) -> str:
        if "reader coordinates" in query:
            raise GBrainQueryError("secondary intent unavailable")
        return "[0.99] mechanisms/world-entry -- world entry"

    result = retrieve_gbrain(
        mode="world_vision",
        fantasy_seed="已批准幻想",
        query_func=fake_query,
        page_func=lambda _slug: _page("Mechanism", "世界入口改变下一步行动空间。"),
    )
    assert result["accepted_count"] == 1
    assert len(result["query_failures"]) == 1
    assert "reader coordinates" in result["query_failures"][0]["query"]


def test_planning_multi_intent_query_still_surfaces_total_gbrain_failure(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def fail_query(_query: str, **_kwargs) -> str:
        raise GBrainQueryError("gbrain unavailable")

    with pytest.raises(GBrainQueryError, match="gbrain unavailable"):
        retrieve_gbrain(
            mode="world_vision",
            fantasy_seed="已批准幻想",
            query_func=fail_query,
            page_func=lambda _slug: "",
        )


def test_story_program_uses_cross_book_patterns_while_outline_keeps_source_specific_arcs() -> None:
    raw = "\n".join([
        "[0.95] mechanisms/example -- pattern",
        "[0.90] book-dna/example -- broad",
        "[0.85] arcs/example -- longitudinal",
    ])
    calls: list[str] = []

    def fake_query(_query: str, **_kwargs) -> str:
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return _page("Mechanism", "经典成长材料的抽象转换。")

    story = retrieve_gbrain(mode="idea", book_content="都市成长故事", query_override="manual", query_func=fake_query, page_func=fake_get)
    assert [item["slug"] for item in story["accepted"]] == ["mechanisms/example"]
    assert story["query_scope"] == "contrasts,mechanisms,syntheses"

    outline = retrieve_gbrain(mode="outline", book_content="都市成长故事", query_override="manual", query_func=fake_query, page_func=fake_get)
    assert [item["slug"] for item in outline["accepted"]] == ["mechanisms/example", "book-dna/example", "arcs/example"]
    assert "arcs" in outline["query_scope"]


def test_brief_and_query_api_expose_filter_counts(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "retrieve_gbrain",
        lambda **_kwargs: {
            "status": "available",
            "scope": "修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选",
            "effective_query": "visible brief",
            "raw_count": 8,
            "accepted_count": 1,
            "rejected_count": 7,
            "requested_limit": 8,
            "final_limit": 5,
            "result": "FILTERED_BUNDLE",
            "raw_stdout": "RAW_STDOUT_MUST_STAY_OUTSIDE_PROMPT",
            "raw_results": [],
            "rejected": [],
        },
    )
    brief = client.post(
        "/api/gbrain/brief",
        json={"mode": "chapter", "book_content": REAL_COLD_CHAIN_BOOK, "current_outline": REAL_COLD_CHAIN_OUTLINE},
    )
    assert brief.status_code == 200
    assert "返程空载" in brief.json()["effective_query"]
    queried = client.post("/api/gbrain/query", json={"mode": "chapter"})
    assert queried.status_code == 200
    assert queried.json()["effective_query"] == "visible brief"
    assert queried.json()["raw_count"] == 8
    prompt = generate_prompt(mode="chapter", template="T", book_content="BOOK", current_outline=REAL_COLD_CHAIN_OUTLINE, gbrain_inspiration=queried.json()["result"])
    assert "FILTERED_BUNDLE" in prompt
    assert "RAW_STDOUT_MUST_STAY_OUTSIDE_PROMPT" not in prompt


def test_page_shows_twelve_design_sections_and_panorama_controls() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="expand-design"' in page.text
    assert 'id="collapse-design"' in page.text
    assert 'id="long-plan-panorama"' in page.text
    assert page.text.count('class="design-card"') == 13


def test_panorama_and_apply_contracts_refresh_without_book_write() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "function parseLongPlanBlocks" in js
    assert "function renderLongPlanPanorama" in js
    assert '$("section-long_plan").addEventListener("input", renderLongPlanPanorama)' in js
    apply_start = js.index("function applyOutlineToBook()")
    apply_end = js.index("async function saveBook()", apply_start)
    apply_body = js[apply_start:apply_end]
    assert "renderLongPlanPanorama()" in apply_body
    assert "designTitles" in apply_body
    assert "section-${key}" in apply_body
    assert "requestJson" not in apply_body


def test_default_prompt_templates_include_idea_mode() -> None:
    response = client.get("/api/prompt-templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert set(templates) == {
        "idea",
        "fantasy_seed",
        "world_vision",
        "outline",
        "chapter_prep",
        "chapter",
        "review",
        "context_curator",
        "primary_writer",
        "specialist_opening",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
        "chapter_integrator",
    }
    direction_doc = Path("docs/MVP_PRODUCT_DIRECTION.md")
    assert direction_doc.is_file()
    direction_text = direction_doc.read_text(encoding="utf-8")
    methodology_text = Path("docs/PIPELINE_METHODOLOGY_AND_VALUES.md").read_text(encoding="utf-8")
    assert "Growth Genome：整理，不创造" in methodology_text
    assert "Classic Patterns Are First-Class Citizens" in methodology_text
    assert "累积成长与可组合成长" in direction_text
    assert "Experiment Boundary" in direction_text
    assert all("成长" in templates[mode] for mode in ("idea", "fantasy_seed", "world_vision", "outline"))
    assert "已批准 Fantasy Seed" in templates["idea"]
    assert "已批准 World Vision" in templates["idea"]
    assert "成长组合" not in templates["idea"]
    assert "转换网络" not in templates["fantasy_seed"]
    assert "GBrain" not in templates["fantasy_seed"]
    assert "Reference Programs" not in templates["fantasy_seed"]
    assert "BOOK" not in templates["fantasy_seed"]
    assert "GBrain" in templates["world_vision"]
    assert "OPTIONAL INSPIRATION" in templates["world_vision"]
    assert "不得覆盖或改写已批准 Fantasy Seed" in templates["world_vision"]
    assert "Reference Programs" not in templates["world_vision"]
    assert "BOOK" not in templates["world_vision"]
    assert "已批准幻想不变量" in templates["outline"]
    assert "内部因果必须可信，但可信不等于现代程序真实" in templates["outline"]
    assert "本次为单 Writer 直接写作" in templates["chapter"]
    assert "选择性展开" in templates["chapter"]
    assert not _WRITER_ABC_PATTERN.search(templates["chapter"])
    for marker in ("串行写作协议", "SUBAGENT_MODE"):
        assert marker not in templates["chapter"]
    assert "如果本书需要且对当前故事重要" in templates["outline"]
    assert "第一章开篇策略" in templates["outline"]
    assert "## 0. 本书成长基因图" in templates["outline"]
    assert "POWER_BREAKTHROUGH" not in Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")


def test_compounding_growth_contract_is_limited_to_creative_chain() -> None:
    for mode in ("fantasy_seed", "world_vision", "idea"):
        template = DEFAULT_PROMPT_TEMPLATES[mode]
        assert "COMPOUNDING_GROWTH_DIRECTION" in template
        assert "后台创作约束，不是小说世界材质" in template
        assert "每轮结束重新归零" in template
        assert "Net New / Irreversible State / Action Space / Fantasy Compounding" in template
        assert "不要让“不可回滚、扩大行动空间、产生复利”本身变成人物追求、世界规则或主题" in template
        assert "不要为了证明复利主动堆路线、权限、网络、库存或组合组件" in template

    fantasy = DEFAULT_PROMPT_TEMPLATES["fantasy_seed"]
    assert "世界为什么会因此自然打开新的目标、敌人、地点或机会" in fantasy
    assert "多次使用以后哪些收益会被保留下来" in fantasy
    assert "留下第一笔以后仍可再次利用的能力、物品、关系、身份或其它具体积累" in fantasy
    assert "### 持续阻力与压力" not in fantasy

    world = DEFAULT_PROMPT_TEMPLATES["world_vision"]
    assert "## 世界资源、利益与机会结构" in world
    assert "过去获得真正进入下一轮" in world
    assert "至少保留若干与主角能力无关" in world
    assert "不要让所有资源都专门为金手指设计" in world
    assert "形成自己的构筑、体系、库存、网络、领地、技艺组合、个人规则或其它不可逆积累" not in world
    assert "## 世界阶层、利益与行动压力" not in world

    story_program = DEFAULT_PROMPT_TEMPLATES["idea"]
    for marker in (
        "当前最值得争取的机会 / 目标：",
        "核心优势怎样产生超额结果：",
        "阶段净新增：",
        "推向下一阶段的更大机会、欲望、竞争或压力：",
    ):
        assert marker in story_program
    assert "新的主动行动、对手新的针对方式、人物关系出现的新选择" in story_program
    assert "不要主动把它们整理成构筑、库存、权限树、路线网、节点网络或组合系统" in story_program
    assert "本阶段关键获得、占有与首次使用" in story_program
    assert "谁死了/活了、什么东西归谁、哪段关系改变、什么身份公开" in story_program
    assert "输出本身不要只写这些标签" in story_program
    assert "Relationship Reconfiguration" in story_program
    assert "谁过去能命令、忽视、利用、封锁、定价或支配他" in story_program
    assert "关系重构的价值在于让上一轮胜利自然生长出新的欲望、联盟、背叛、争夺和对手反应" in story_program
    assert "Relationship Reconfiguration" not in DEFAULT_PROMPT_TEMPLATES["world_vision"]
    assert "Relationship Reconfiguration" not in DEFAULT_PROMPT_TEMPLATES["outline"]
    assert "稳定控制、调用或从中取得复利收益的外部结构" not in story_program
    assert "二级收益：写本阶段" not in story_program
    assert "阶段净新增" not in DEFAULT_PROMPT_TEMPLATES["outline"]


def test_high_value_acquisition_guidance_lives_in_story_program_and_outline_only() -> None:
    for mode in ("idea", "outline"):
        template = DEFAULT_PROMPT_TEMPLATES[mode]
        assert "High-Value Acquisition / Reward Opportunity" in template
        assert "阶段可以没有新的标志性获得" in template
        assert "奖励类型与出现顺序由本书因果决定" in template
    assert "High-Value Acquisition / Reward Opportunity" not in DEFAULT_PROMPT_TEMPLATES["world_vision"]

    director = generate_prompt(mode="director", template="", book_content="", current_outline=REAL_COLD_CHAIN_OUTLINE)
    primary = generate_prompt(mode="primary_writer", template="", book_content="", current_outline=REAL_COLD_CHAIN_OUTLINE, curated_context="# Curated Chapter Context")
    assert "High-Value Acquisition / Reward Opportunity" not in director
    assert "High-Value Acquisition / Reward Opportunity" not in primary
    from story_mvp.gbrain_retrieval import PLANNING_KEYWORD_QUERIES
    assert "reward opportunity" in PLANNING_KEYWORD_QUERIES["idea"]
    assert "reward recontextualization" in PLANNING_KEYWORD_QUERIES["outline"]
    assert CREATIVE_PLANNING_FINAL_RESULT_LIMIT == 3


def test_chapter_page_defaults_to_curator_primary_and_keeps_repair_nodes_optional() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="writer-mode"' in page.text
    assert 'value="curator_primary" selected' in page.text
    assert 'value="hybrid_selective"' in page.text
    assert page.text.count('type="checkbox" checked') == 0
    assert 'id="state-model"' in page.text
    assert 'id="activate-repair-specialists"' in page.text
    for node_id in (
        "curator-response",
        "primary-writer-response",
        "opening-specialist-response",
        "dialogue-specialist-response",
        "action-specialist-response",
        "emotion-specialist-response",
        "integrator-response",
    ):
        assert f'id="{node_id}"' in page.text
    assert 'id="extract-integrator-body"' in page.text
    assert 'id="adopt-primary-draft"' in page.text


def test_growth_contract_is_present_in_idea_outline_and_review_prompts() -> None:
    idea = DEFAULT_PROMPT_TEMPLATES["idea"]
    for marker in (
        "### 核心优势与长期玩法",
        "### 长期故事主线",
        "主角一级成长",
        "阶段净新增",
        "世界扩张",
    ):
        assert marker in idea
    assert "### 成本节奏" not in idea
    assert "自然产生的后果或余波（如果有）" in idea
    outline = DEFAULT_PROMPT_TEMPLATES["outline"]
    for marker in ("### 一级成长主轴", "### 二级收益与反哺", "### 主循环", "### 成本节奏"):
        assert marker in outline
    assert "代价或余波（可选）" in outline
    assert "不强制每块失去或承担什么" in outline
    review = DEFAULT_PROMPT_TEMPLATES["review"]
    for marker in (
        "## 核心幻想是否仍在兑现",
        "## 一级成长是否仍是主轴",
        "## 幻想盈余是否为正",
        "## 冲突是否过度理性化",
        "## 世界是否被程序化",
    ):
        assert marker in review


def test_growth_projection_is_three_lines_and_not_an_outline_gate() -> None:
    stage_only = render_growth_benefit_projection(
        current_long_block=(
            "一级成长变化：砾角第一次完成贴壁进化。\n"
            "二级收益结算：获得一笔赏金和红根路线牌。\n"
            "反哺下一轮：路线牌让主角进入血统兽斗场。"
        )
    )
    assert "本章一级成长推进：\n未在本章计划中明确；不强制本章推进。" in stage_only
    assert "当前剧情块一级成长目标仅供参照：砾角第一次完成贴壁进化。" in stage_only
    assert "本章二级收益结算：\n未在本章计划中明确；不强制本章结算。" in stage_only
    assert "当前剧情块二级收益目标仅供参照：获得一笔赏金和红根路线牌。" in stage_only
    assert "本章反哺：\n未在本章计划中明确；不强制本章反哺。" in stage_only
    assert "当前剧情块反哺目标仅供参照：路线牌让主角进入血统兽斗场。" in stage_only
    explicit = render_growth_benefit_projection(
        current_long_block="一级成长变化：LONG_BLOCK_LEVEL_UP。\n二级收益结算：LONG_BLOCK_REWARD。",
        current_chapter_plan="一级成长变化：CHAPTER_PLAN_LEVEL_UP。\n二级收益结算：CHAPTER_PLAN_REWARD。",
        current_outline="反哺下一轮：OUTLINE_FEEDBACK。",
    )
    assert "本章一级成长推进：CHAPTER_PLAN_LEVEL_UP。" in explicit
    assert "本章二级收益结算：CHAPTER_PLAN_REWARD。" in explicit
    assert "本章反哺：OUTLINE_FEEDBACK。" in explicit
    assert "LONG_BLOCK_LEVEL_UP" not in explicit
    bold_plan = render_growth_benefit_projection(
        current_chapter_plan="**一级成长变化：**BOLD_CHAPTER_PLAN_LEVEL_UP。"
    )
    assert "本章一级成长推进：BOLD_CHAPTER_PLAN_LEVEL_UP。" in bold_plan
    empty = render_growth_benefit_projection()
    assert "本章一级成长推进：本章计划未明确；不强制本章推进。" in empty
    assert "本章二级收益结算：本章计划未明确；不强制本章结算。" in empty
    assert "本章反哺：本章计划未明确；不强制本章反哺。" in empty
    assert "本章不推进。" not in empty
    assert "本章不结算。" not in empty
    assert "本章反哺为空。" not in empty
    assert len(REQUIRED_OUTLINE_FIELDS) == 8
    assert "一级成长变化" not in REQUIRED_OUTLINE_FIELDS
    assert "二级收益结算" not in REQUIRED_OUTLINE_FIELDS


def test_compact_growth_genome_keeps_only_author_invariants_and_risks() -> None:
    book = """# 小说总体设计画像
## 0. 本书成长基因图
### 作者明确保留
AUTHOR_MARKER
### 一级成长收益
FULL_PRIMARY_MARKER
### 二级成长收益
FULL_SECONDARY_MARKER
### 反哺关系
FULL_FEEDBACK_MARKER
### 核心不变量
INVARIANT_MARKER
### 退化风险
RISK_MARKER
## 1. 核心类型与读者承诺
BOOK_MARKER
"""
    compact = compact_growth_genome_for_chapter(book)
    assert "AUTHOR_MARKER" in compact
    assert "INVARIANT_MARKER" in compact
    assert "RISK_MARKER" in compact
    for marker in ("FULL_PRIMARY_MARKER", "FULL_SECONDARY_MARKER", "FULL_FEEDBACK_MARKER"):
        assert marker not in compact


def test_compact_growth_genome_keeps_new_approved_fantasy_invariant() -> None:
    book = """# 小说总体设计画像
## 0. 本书成长基因图
### 已批准幻想不变量
FANTASY_INVARIANT_MARKER
### 一级成长主轴
FULL_PRIMARY_MARKER
### 核心不变量
INVARIANT_MARKER
### 退化风险
RISK_MARKER
## 1. 核心类型与读者承诺
BOOK_MARKER
"""
    compact = compact_growth_genome_for_chapter(book)
    assert "### 已批准幻想不变量" in compact
    assert "FANTASY_INVARIANT_MARKER" in compact
    assert "INVARIANT_MARKER" in compact
    assert "RISK_MARKER" in compact
    assert "FULL_PRIMARY_MARKER" not in compact


def test_curator_index_first_prefetch_keeps_relevant_detail_and_drops_unrelated_tail() -> None:
    unrelated = "无关旧设定段落。" * 90
    relevant = "陆砚必须面对谢三更的压价；这次真正冲突是路线控制权和入市资格。"
    book_contract = (
        "## 2. 世界观结构\n\n入口摘要。\n\n"
        + "\n\n".join(unrelated + str(index) for index in range(12))
        + "\n\n"
        + relevant
        + "\n\nUNRELATED_TAIL_MARKER"
    )
    packet = ChapterContextPacket(
        authority="AUTH",
        book_contract=book_contract,
        chapter_mission="主角行动：陆砚拒绝谢三更压价，并争夺路线控制权。",
        canon_context="## PERSISTENT CANON：\n陆砚已经掌握一条隐秘路线。",
        recent_prose="谢三更看着陆砚，没有立刻开价。",
        rolling_plan="PLAN",
        chapter_plan_context="当前章计划：谢三更提出交易，陆砚决定反向争价。",
        current_long_block="BLOCK",
        current_chapter_plan="PLAN",
        prose_profile="## 8. 文风与可操作参数\n直接、清楚。",
        optional_inspiration="",
        growth_benefit_projection="",
        growth_genome_compact="### 核心不变量\n主角主动争夺更大自由。",
    )

    context = build_curator_context(packet)

    assert "## 2. 世界观结构" in context.context_index
    assert relevant in context.book_contract
    assert "UNRELATED_TAIL_MARKER" not in context.book_contract
    assert "UNRELATED_TAIL_MARKER" not in context.context_index
    assert "其余段落未进入本章确定性预取" in context.book_contract


def test_open_promises_and_recent_summaries_are_deterministically_bounded() -> None:
    promises = "\n".join(
        ["- 同一个承诺", "2. 同一个承诺"]
        + [f"- 承诺{i}" for i in range(1, 15)]
    )
    compact = compact_open_promises(promises)
    promise_lines = [line for line in compact.splitlines() if line.startswith("- ")]
    assert len(promise_lines) == 12
    assert promise_lines.count("- 同一个承诺") == 1
    assert "承诺12" not in compact

    summaries = "\n".join(f"第{i}章：SUMMARY_{i}" for i in range(1, 6))
    recent = compact_recent_summaries(summaries)
    assert "SUMMARY_1" not in recent
    assert "SUMMARY_2" not in recent
    for marker in ("SUMMARY_3", "SUMMARY_4", "SUMMARY_5"):
        assert marker in recent


def test_single_and_curator_use_compact_genome_projection() -> None:
    book = """# 小说总体设计画像
## 0. 本书成长基因图
### 作者明确保留
AUTHOR_MARKER
### 一级成长收益
FULL_PRIMARY_MARKER
### 二级成长收益
FULL_SECONDARY_MARKER
### 反哺关系
FULL_FEEDBACK_MARKER
### 核心不变量
INVARIANT_MARKER
### 退化风险
RISK_MARKER
## 1. 核心类型与读者承诺
BOOK_MARKER
# 当前状态、未兑现承诺与作者备注
STATUS_MARKER
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    single = generate_prompt(
        mode="chapter",
        template="SINGLE TEMPLATE",
        book_content=book,
        current_outline=outline,
    )
    curator = generate_prompt(
        mode="context_curator",
        template="",
        book_content=book,
        current_outline=outline,
    )
    for prompt in (single, curator):
        assert "AUTHOR_MARKER" in prompt
        assert "INVARIANT_MARKER" in prompt
        assert "RISK_MARKER" in prompt
        for marker in ("FULL_PRIMARY_MARKER", "FULL_SECONDARY_MARKER", "FULL_FEEDBACK_MARKER"):
            assert marker not in prompt


def test_curator_receives_growth_projection_writer_receives_only_curated_meaning() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    book = """# 小说总体设计画像
## 0. 本书成长基因图
FULL_GROWTH_HIERARCHY_MARKER
## 1. 核心类型与读者承诺
BOOK_MARKER
# 当前状态、未兑现承诺与作者备注
状态
"""
    current_block = "一级成长变化：本章完成第一次进化。\n二级收益结算：获得赏金。\n反哺下一轮：进入斗场。"
    curator = generate_prompt(
        mode="context_curator",
        template="",
        book_content=book,
        current_long_block=current_block,
        current_outline=outline,
    )
    assert "FULL_GROWTH_HIERARCHY_MARKER" not in curator
    assert "本章一级成长推进：\n未在本章计划中明确；不强制本章推进。" in curator
    assert "当前剧情块一级成长目标仅供参照：本章完成第一次进化。" in curator
    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content=book,
        current_long_block=current_block,
        current_outline=outline,
        curated_context="# Curated Chapter Context\n\n## Relevant Plan\n\n本章一级成长推进：本章完成第一次进化。",
    )
    assert "FULL_GROWTH_HIERARCHY_MARKER" not in primary
    assert "本章一级成长推进：本章完成第一次进化。" in primary
    assert "本章一级成长推进：\n未在本章计划中明确；不强制本章推进。" not in primary
    assert "当前剧情块一级成长目标仅供参照" not in primary
    assert "Growth Benefit Hierarchy：" not in primary
    assert "FULL_GROWTH_HIERARCHY_MARKER" not in drop_growth_hierarchy(
        "## 0. 本书成长基因图\nFULL_GROWTH_HIERARCHY_MARKER\n## 1. 核心类型与读者承诺\nBOOK_MARKER"
    )


def test_state_delta_does_not_receive_growth_hierarchy() -> None:
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content="# 小说总体设计画像\n## 0. 本书成长基因图\nFULL_GROWTH_HIERARCHY_MARKER\n# 当前状态、未兑现承诺与作者备注\n状态",
        chapter_number=1,
        chapter_prose="本章正式正文。",
    )
    assert "FULL_GROWTH_HIERARCHY_MARKER" not in prompt
    assert "一级成长收益" not in prompt
    assert "二级成长收益" not in prompt


def test_hybrid_runtime_extractors_are_deterministic() -> None:
    response = "# Primary Writer Audit\n\n无。\n# Primary Draft\n\n完整正文。\n# Primary Fact Summary\n\n事实摘要。"
    assert extract_primary_draft(response) == "完整正文。"
    assert extract_primary_fact_summary(response) == "事实摘要。"
    assert extract_primary_draft("# 正式正文\n\n新版完整正文。") == "新版完整正文。"
    assert extract_primary_draft("直接返回的纯正文。") == "直接返回的纯正文。"
    assert extract_final_chapter_artifact("# Writer Audit\n\n# 正式正文\n\n最终正文\n# 章节事实摘要\n\n最终事实") == (
        "最终正文",
        "最终事实",
    )
    assert extract_final_chapter_artifact("# Writer Audit\n\n没有正文") is None
    assert count_specialist_patches("# Proposed Patches\n## Patch 1\n## Patch 2") == 2
    long_text = "前文开头" + ("x" * 2500) + "\n\n前文最后动作"
    transition = extract_last_transition_context(long_text)
    assert "前文最后动作" in transition
    assert len(transition) <= 1800


def test_primary_writer_contract_is_body_only_without_pipeline_bookkeeping() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["primary_writer"]
    assert "# 正式正文" in template
    for marker in (
        "# Primary Writer Audit",
        "# Primary Draft",
        "# Primary Fact Summary",
    ):
        assert marker not in template
    assert "不要承担 pipeline bookkeeping" in template
    assert "不输出 Audit、事实摘要、状态更新、计划说明、质量自评或修改清单" in template


def test_old_book_gets_code_default_hybrid_templates_without_prompt_file_write(tmp_path: Path) -> None:
    book_dir = create_book("old-book", tmp_path)
    legacy_prompts = "# 男频爽文创意生成\n\nLEGACY IDEA\n\n# 新书/总纲规划\n\nLEGACY OUTLINE\n"
    prompts_path = book_dir / "PROMPTS.md"
    prompts_path.write_text(legacy_prompts, encoding="utf-8")
    before = prompts_path.read_bytes()
    payload = read_book_payload("old-book", tmp_path)
    assert payload["prompt_templates"]["context_curator"] == DEFAULT_PROMPT_TEMPLATES["context_curator"]
    assert payload["prompt_templates"]["specialist_emotion"] == DEFAULT_PROMPT_TEMPLATES["specialist_emotion"]
    assert payload["prompt_templates"]["idea"] == "LEGACY IDEA"
    assert prompts_path.read_bytes() == before


def test_context_curator_prompt_uses_tail_and_opening_strategy_only() -> None:
    book = """# 小说总体设计画像

## 0. 本书成长基因图
BOOK_CONTRACT_MARKER
## 1. 核心类型与读者承诺
CHARACTERS_MARKER
## 7. 叙事结构
### 第一章开篇策略
城市远景 → 具体现场 → 主角行动
## 8. 文风与可操作参数
PROSE_PROFILE_MARKER
## 11. 未来设计
FULL_BOOK_FUTURE_MARKER

# 当前状态、未兑现承诺与作者备注
当前状态：已在现场。
"""
    outline = "\n".join(f"{field}：本章{field}" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    previous = "前文开头" + ("y" * 2500) + "\n\n前文最后动作"
    prompt = generate_prompt(
        mode="context_curator",
        template="",
        book_content=book,
        current_long_block="CURRENT_BLOCK_MARKER",
        current_outline=outline,
        previous_chapter_text=previous,
        gbrain_inspiration="INSPIRATION_MARKER",
    )
    assert "CURRENT_BLOCK_MARKER" in prompt
    assert "INSPIRATION_MARKER" in prompt
    assert "城市远景 → 具体现场 → 主角行动" in prompt
    assert "前文最后动作" in prompt
    assert "前文开头" not in prompt
    assert "FULL_BOOK_FUTURE_MARKER" not in prompt


def test_outline_parser_drops_inline_model_preamble_before_first_required_field() -> None:
    response = (
        "我会先遵守 Director 边界。触发事件：顾长川领取身份牌。\n"
        "推动事件的人：执事。\n"
        "主角行动：顾长川收好身份牌。\n"
        "对手或世界反应：内门继续报到。\n"
        "直接结果：完成报到。\n"
        "状态变化：成为内门弟子。\n"
        "叙事功能：兑现晋升。\n"
        "结尾推动力：次日进入演武堂。"
    )
    validate_current_outline(response)
    parsed = parse_outline_fields(response)
    assert parsed["触发事件"] == "顾长川领取身份牌。"


def test_world_vision_owns_reader_coordinates_and_core_advantage_compatibility() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["world_vision"]
    assert "Reader-Facing World Coordinates" in template
    assert "读者可操作、可预测的世界事实" in template
    assert "什么条件下会发生什么可观察变化" in template
    assert "概念名、哲学解释和深层原因" in template
    assert "不能只用哲学定义、象征、意象或新造概念代替" in template
    assert "## 读者可用的世界坐标" in template
    assert "## 核心优势与普通规则怎样咬合" in template
    assert "如果主角把优势用于远高于当前层级的对象" in template
    assert "基础待遇与稀缺奖励" in template
    assert "不强造境界名" in template
    assert "不要把“眼前到底发生了什么、触发后会怎样、人物现在能不能做某件事”也一起藏起来" in template


def test_fantasy_seed_keeps_theme_emergent_and_future_play_concrete() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["fantasy_seed"]
    assert "Fantasy + Desire + Gameplay" in template
    assert "不负责替这个幻想寻找终极哲学意义" in template
    assert "### 远期升格方向" in template
    assert "更强、更不同、读者更想亲自看的具体用法" in template
    assert "不先定义更高世界“哲学上意味着什么”" in template


def test_world_vision_builds_independent_world_and_desire_economy_before_advantage() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["world_vision"]
    independent = template.index("## 没有主角时，这个世界怎样运转")
    desire = template.index("## 世界里真正值钱、值得想要的东西")
    coordinates = template.index("## 读者可用的世界坐标")
    advantage = template.index("## 核心优势与普通规则怎样咬合")
    assert independent < desire < coordinates < advantage
    assert "即使主角明天消失也仍会发生" in template
    assert "Desire Economy" in template
    assert "世界前台尺" in template
    assert "Action Space / Expectation Ladder / Mystery Depth / Impact" in template
    assert "读者体验/故事校准尺" in template
    assert "成长后具体多能做哪件以前做不到的事" in template
    assert "哪个已经出现的旧物、旧人、旧事实还有可回收的更深解释" in template
    assert "不能自动升级成世界 ontology" in template


def test_story_program_keeps_backstage_principles_but_outputs_concrete_acquisition() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["idea"]
    assert "Action Space、Net New、Irreversible State、World Entry、Reward Opportunity、Fantasy Compounding、资源反哺" in template
    assert "Expectation Ladder、Mystery Depth、Impact" in template
    assert "评价和约束故事的作者语言，不是生成世界的材质" in template
    assert "本阶段关键获得、占有与首次使用" in template
    assert "无新的标志性获得" in template
    assert "Expectation Ladder 的具体投影" in template
    assert "Mystery Depth 的锚点" in template
    assert "Impact 只作为后台尺度" in template
    assert "输出本身不要只写这些标签" in template


def test_outline_theme_is_derived_and_may_remain_unset() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["outline"]
    assert "Action Space / Expectation Ladder / Mystery Depth / Impact" in template
    assert "只投影到现有字段" in template
    assert "## 11. 主题、价值观与长期问题" in template
    assert "这里只后验总结" in template
    assert "直接写“暂不预设”" in template
    assert "不参与生成世界 ontology、资源体系、敌人设计、能力升格或终局" in template


def test_story_program_owns_core_advantage_choice_space_and_counterplay() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["idea"]
    assert "### 核心优势的选择空间与反制" in template
    assert "Contestable Choice" in template
    assert "题面不要预先写出明显正确答案" in template
    assert "真实价值、信息不完整、时机或对手干预" in template
    assert "不要求每次选择都附带惨痛代价" in template
    assert "不强制“单槽”" in template


def test_outline_releases_world_model_and_varies_early_core_gameplay() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["outline"]
    assert "Outline World Model Release" in template
    assert "作者在 World Vision 里知道某个概念，不等于读者已经知道" in template
    assert "可观察的触发、结果和行动含义" in template
    assert "不要用意象、哲学定义或专属术语代替规则本身" in template
    assert "Outline Core Gameplay Variation" in template
    assert "上一轮已证明有效的解法不要自动解决下一轮主要问题" in template
    assert "下一轮优先攻击它尚未解决的对象、关系、资源、目标或条件" in template
    assert "不要求机械让主角失败或每轮添加新代价" in template
    assert "前三章建立当前故事所需的最低可用坐标" in template
    assert "长期对手可暂时作为强弱标尺" in template


def test_director_does_not_own_world_model_creation() -> None:
    template = DEFAULT_DIRECTOR_TEMPLATE
    assert "属于上游 World Vision / Story Program / Outline 已批准事实" in template
    assert "不得为了让本章更具体而临时发明境界名、数值、货币、奖励、制度、能力限制或新世界规则" in template
    assert "Reader-Facing World Coordinates" not in template
    assert "Promotion Opens the World" not in template
    assert "Core Ability Attention Alignment" not in template


def test_curator_concretizes_only_from_upstream_world_facts() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["context_curator"]
    assert "资源、机会、路径/路线、位置、选择、资格、收益、行动空间" in template
    assert "BOOK / Canon / Plan 已经明确存在" in template
    assert "上游没有给出具体世界名词时" in template
    assert "不得为了“实体化”由 Curator 或 Writer 自己发明制度、价格、物品或待遇" in template
    assert "细节预算优先跟随 BOOK 核心幻想真正让读者关心的对象" in template


def test_context_curator_compiles_scene_prose_projection_instead_of_forwarding_controls() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["context_curator"]
    assert "## Scene Prose Projection" in template
    assert "写 `NONE`" in template
    assert "`NONE` 是正常结果，优先于弱投影" in template
    assert "重复 Reader-Facing Language、Opening Strategy、已选 Scene Skill" in template
    assert "只写 2—4 句自然中文" in template
    assert "不要把这六项逐项回显" in template
    assert "不要仅因为 Scene Family 有匹配 Control 就生成 Projection" in template
    assert "匹配卡本身不构成使用理由" in template
    assert "不得写 Control 名称" in template
    assert "动作、对白、物体变化或人物反应已经让意义成立时" in template
    assert "结果已经发生但现场仍读不出局面变化时" in template


def test_extract_primary_draft_drops_inline_model_preamble_before_body_heading() -> None:
    response = "我会按规范直接写作。# 正式正文\n\n顾长川拿起身份牌。"
    assert extract_primary_draft(response) == "顾长川拿起身份牌。"


def test_primary_writer_strips_legacy_relevant_prose_controls() -> None:
    outline = "\n".join(f"{field}：本章{field}" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    curated = """# Curated Chapter Context

## Relevant Plan
计划事实。
## Relevant Prose Controls
LEGACY_FULL_CONTROL_MUST_NOT_REACH_PRIMARY
## Opening Strategy
直接进入现场。
"""
    prompt = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="# 小说总体设计画像\n## 8. 文风与可操作参数\n简洁。",
        current_outline=outline,
        curated_context=curated,
    )
    assert "LEGACY_FULL_CONTROL_MUST_NOT_REACH_PRIMARY" not in prompt
    assert "直接进入现场" in prompt


def test_primary_writer_receives_scene_prose_projection_without_raw_gbrain() -> None:
    outline = "\n".join(f"{field}：本章{field}" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    curated = """# Curated Chapter Context

## Relevant Plan
计划事实。
## Scene Prose Projection
本场只展开门口没有给主角留座这一处身份变化；对方改口后停止解释关系意义。
## Scene Skill Selection
Primary: none
Secondary: none
"""
    prompt = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="# 小说总体设计画像\n## 8. 文风与可操作参数\n简洁直接。",
        current_outline=outline,
        previous_chapter_text="CANON_PROSE",
        curated_context=curated,
        gbrain_inspiration="RAW_PROSE_CONTROL_MUST_NOT_REACH_PRIMARY",
    )
    assert "## Scene Prose Projection" in prompt
    assert "本场只展开门口没有给主角留座" in prompt
    assert "RAW_PROSE_CONTROL_MUST_NOT_REACH_PRIMARY" not in prompt


def test_primary_writer_prompt_uses_curated_projection_and_explicit_fallback() -> None:
    outline = "\n".join(f"{field}：本章{field}" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    book = """# 小说总体设计画像
## 0. 本书成长基因图
BOOK_CONTRACT_MARKER
## 7. 叙事结构
PROSE_PROFILE_SHOULD_NOT_REPEAT
## 8. 文风与可操作参数
FULL_PROSE_PROFILE_MARKER
## 11. 尚未注入的未来区块
FULL_BOOK_CONTRACT_MARKER
# 当前状态、未兑现承诺与作者备注
当前状态：已发生事实。
"""
    curated = "# Curated Chapter Context\n\n## Relevant Plan\n\nCURATED_ONLY_MARKER"
    prompt = generate_prompt(
        mode="primary_writer",
        template="",
        book_content=book,
        current_long_block="RAW_LONG_BLOCK_MUST_NOT_REACH_PRIMARY",
        current_chapter_plan="RAW_CHAPTER_PLAN_MUST_NOT_REACH_PRIMARY",
        current_outline=outline,
        previous_chapter_text="CANON_PROSE_MARKER",
        curated_context=curated,
    )
    assert "AUTHORITY" in prompt
    assert "Chapter Mission" in prompt
    assert "正文可见最小事件合同" in prompt
    assert "CANON_PROSE_MARKER" in prompt
    assert "CANON INDEX——Curator 缺失时的事实 fallback" not in prompt
    assert "本章成长收益短投影——Curator 缺失时的规划 fallback" not in prompt
    assert "叙事功能：本章叙事功能" not in prompt
    assert "规划备注（planning note）" not in prompt
    assert "CURATED_ONLY_MARKER" in prompt
    assert "RAW_LONG_BLOCK_MUST_NOT_REACH_PRIMARY" not in prompt
    assert "RAW_CHAPTER_PLAN_MUST_NOT_REACH_PRIMARY" not in prompt
    assert "FULL_PROSE_PROFILE_MARKER" not in prompt
    assert "FULL_BOOK_CONTRACT_MARKER" not in prompt
    assert "事实目标，不是正文措辞" in prompt

    fallback = generate_prompt(
        mode="primary_writer",
        template="",
        book_content=book,
        current_outline=outline,
    )
    assert "Curator 未提供，使用完整上下文 fallback" in fallback
    assert "CANON INDEX——Curator 缺失时的事实 fallback" in fallback
    assert "本章成长收益短投影——Curator 缺失时的规划 fallback" in fallback


def test_specialists_receive_primary_draft_without_raw_gbrain_and_integrator_allows_missing() -> None:
    outline = "\n".join(f"{field}：本章{field}" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    book = "# 小说总体设计画像\n## 7. 叙事结构\n开篇策略\n# 当前状态、未兑现承诺与作者备注\n当前状态：现场"
    curated = """# Curated Chapter Context

## Relevant Characters and Relationships
CHARACTER_CONTEXT
## Relevant World Rules
WORLD_CONTEXT
## Relevant Plan
PLAN_CONTEXT
## Relevant Prose Controls
PROSE_CONTEXT
## Opening Strategy
OPENING_CONTEXT
"""
    primary = "PRIMARY_DRAFT_MARKER"
    for mode in (
        "specialist_opening",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
    ):
        prompt = generate_prompt(
            mode=mode,
            template="",
            book_content=book,
            current_long_block="RAW_LONG_BLOCK_MUST_NOT_REACH_SPECIALIST",
            current_chapter_plan="RAW_CHAPTER_PLAN_MUST_NOT_REACH_SPECIALIST",
            current_outline=outline,
            curated_context=curated,
            primary_draft=primary,
            gbrain_inspiration="RAW_GBRAIN_MARKER",
        )
        assert primary in prompt
        assert "RAW_GBRAIN_MARKER" not in prompt
        assert "RAW_LONG_BLOCK_MUST_NOT_REACH_SPECIALIST" not in prompt
        assert "RAW_CHAPTER_PLAN_MUST_NOT_REACH_SPECIALIST" not in prompt
        assert "本章成长收益短投影（规划提示，不是正文措辞）" not in prompt
        assert "叙事功能：本章叙事功能" not in prompt
        assert "规划备注（planning note）" not in prompt
        assert "单 Writer 职责" not in prompt
    integrator = generate_prompt(
        mode="chapter_integrator",
        template="",
        book_content=book,
        current_long_block="RAW_LONG_BLOCK_MUST_NOT_REACH_INTEGRATOR",
        current_chapter_plan="RAW_CHAPTER_PLAN_MUST_NOT_REACH_INTEGRATOR",
        current_outline=outline,
        curated_context=curated,
        primary_draft=primary,
        specialist_opening_response="OPENING_RESPONSE",
        specialist_action_response="ACTION_RESPONSE",
    )
    assert "PRIMARY_DRAFT_MARKER" in integrator
    assert "OPENING_RESPONSE" in integrator
    assert "ACTION_RESPONSE" in integrator
    assert "CURATED_ONLY_MARKER" not in integrator
    assert "RAW_LONG_BLOCK_MUST_NOT_REACH_INTEGRATOR" not in integrator
    assert "RAW_CHAPTER_PLAN_MUST_NOT_REACH_INTEGRATOR" not in integrator
    assert "CHARACTER_CONTEXT" in integrator
    assert "本章成长收益短投影（规划提示，不是正文措辞）" not in integrator
    assert "CANON INDEX（事实输入，不是正文措辞）" not in integrator
    assert "叙事功能：本章叙事功能" not in integrator
    assert "规划备注（planning note）" not in integrator
    assert "单 Writer 职责" not in integrator
    assert "Dialogue Specialist Response" in integrator
    assert "未提供" in integrator
    assert "不必全部采纳" in integrator


def test_outline_prompt_injects_book_content_once() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="OUTLINE TEMPLATE",
        book_content="UNIQUE BOOK CONTENT",
        **approved_creative_inputs(),
    )
    assert prompt.count("UNIQUE BOOK CONTENT") == 1


def test_apply_outline_to_book_is_browser_only() -> None:
    html = Path("src/story_mvp/templates/index.html").read_text(encoding="utf-8")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert 'id="apply-outline-to-book"' in html
    start = js.index("function applyOutlineToBook()")
    end = js.index("async function saveBook()", start)
    function_body = js[start:end]
    assert "requestJson" not in function_body
    assert "fetch(" not in function_body
    assert "/book" not in function_body


def test_proposal_source_is_explicit_and_editor_only() -> None:
    html = Path("src/story_mvp/templates/index.html").read_text(encoding="utf-8")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "proposalDraftActive" not in js
    assert "将 Codex 返回放入 Proposal 编辑区" in html
    assert "将 Proposal 应用到 BOOK 编辑区" in html
    assert "唯一 Proposal 来源" in html

    apply_start = js.index("function applyOutlineToBook()")
    apply_end = js.index("function extractChapterArtifact", apply_start)
    apply_body = js[apply_start:apply_end]
    assert 'const source = $("proposal-editor").value;' in apply_body
    assert '$("codex-response").value' not in apply_body
    assert "Proposal 编辑区中的" in apply_body

    save_start = js.index("async function saveProposal()")
    save_end = js.index("async function approveChapter", save_start)
    save_body = js[save_start:save_end]
    assert "saveCreativeArtifact(\"proposal\")" in save_body

    assert '$("apply-response").addEventListener("click"' in js
    assert 'applyResponseToEditor($("codex-response"), $("proposal-editor"));' in js
    assert '$("proposal-editor").value = $("codex-response").value' not in js
    assert '$("codex-response").addEventListener("input"' not in js
    assert "markCreativeEdited(artifact)" in js


def test_generate_prompt_does_not_clear_proposal_editor() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("async function generatePrompt()")
    end = js.index("async function generateIdeaPrompt", start)
    function_body = js[start:end]
    assert 'const payload = await requestJson("/api/prompt"' in function_body
    assert '$("prompt-text").value = payload.prompt;' in function_body
    assert "proposal-editor" not in function_body
    assert "codex-response" not in function_body
    assert "composeBookContent" not in function_body
    assert "saveBook" not in function_body


def test_previous_chapter_fetch_failure_is_visible_and_does_not_clear_context() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("async function refreshPreviousChapterText()")
    end = js.index("async function loadBook", start)
    function_body = js[start:end]
    assert "const chapters = [];" in function_body
    assert "target.value = chapters.join" in function_body
    assert "读取第${number}章连续性上下文失败：${error.message}" in function_body
    assert "catch {" not in function_body
    assert 'target.value = "";' not in function_body.split("const first", 1)[1]


def test_chapter_response_contract_saves_only_extracted_body() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("function extractChapterArtifact")
    end = js.index("async function saveBook", start)
    parser = js[start:end]
    assert 'const bodyHeading = "# 正式正文";' in parser
    assert 'const summaryHeading = "# 章节事实摘要";' in parser
    approve_start = js.index("async function approveChapter")
    approve_end = js.index("async function createBook", approve_start)
    approve = js[approve_start:approve_end]
    assert 'const chapterBody = $("chapter-body-for-save").value.trim();' in approve
    assert 'content: chapterBody' in approve
    assert 'content: $("codex-response").value' not in approve


def _full_eight_field_outline() -> str:
    return "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))


def test_default_chapter_prompt_has_no_writer_a_b_c() -> None:
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert not _WRITER_ABC_PATTERN.search(prompt)


def test_sanitize_chapter_template_strips_writer_heading_blocks_and_keeps_other_sections() -> None:
    legacy = "\n".join(
        [
            "## 串行写作协议",
            "必须串行调用 Writer A → Writer B → Writer C。",
            "### Writer A — Scene Draft",
            "第一稿职责。",
            "## 命名规则",
            "功能角色默认不命名。",
        ]
    )
    sanitized, changed = sanitize_chapter_template(legacy)
    assert changed is True
    assert "## 命名规则" in sanitized
    assert "功能角色默认不命名。" in sanitized
    assert not _WRITER_ABC_PATTERN.search(sanitized)
    assert "串行写作协议" not in sanitized


def test_sanitize_injects_single_writer_lines_by_contract_heading_state_not_adjacency() -> None:
    # 单 Writer 替换行的注入依据「最近保留的输出合同标题」状态，
    # 不依赖多 Writer 行与合同标题物理相邻（中间隔空行仍可注入）。
    legacy = "\n".join(
        [
            "# Writer Audit",
            "",
            "只写 SUBAGENT_MODE 和 Writer A/B/C 的中间稿问题。",
            "# 正式正文",
            "",
            "汇总 Writer B 终稿作为正式正文。",
        ]
    )
    sanitized, changed = sanitize_chapter_template(legacy)
    assert changed is True
    assert "Writer Audit 只报告实际存在的事项" in sanitized
    assert "无需要报告的冲突或实质调整" in sanitized
    # sanitize 只注入一行短句；完整 WRITER_AUDIT_RULE 全文由合同只注入一次。
    assert sanitized.count(WRITER_AUDIT_RULE) == 0
    prompt = generate_prompt(
        mode="chapter",
        template=legacy,
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert prompt.count(WRITER_AUDIT_RULE) == 1
    assert "2—5 个连续性问题" not in sanitized
    assert "2—5 个表达实现问题" not in sanitized
    assert "只放本次直接写作的完整小说正文。" in sanitized
    assert not _WRITER_ABC_PATTERN.search(sanitized)


def test_legacy_book_level_chapter_template_is_sanitized_to_single_writer() -> None:
    prompts_path = Path("books/real-exp-001/PROMPTS.md")
    prompts_md = prompts_path.read_text(encoding="utf-8")
    start = prompts_md.index("# 当前章节写作")
    end = prompts_md.index("# 十章复盘与下一批十章", start)
    legacy_template = prompts_md[start:end]
    assert "串行写作协议" in legacy_template
    prompt = generate_prompt(
        mode="chapter",
        template=legacy_template,
        book_content="",
        current_outline=_full_eight_field_outline(),
        previous_chapter_text="上一章最后一句：门锁响了。",
    )
    assert not _WRITER_ABC_PATTERN.search(prompt)
    assert "串行写作协议" not in prompt
    assert "SUBAGENT_MODE" not in prompt
    assert SINGLE_WRITER_RUNTIME_NOTE in prompt
    assert "门锁响了" in prompt
    assert "连续性优先" in prompt
    assert "# Writer Audit" in prompt
    assert "# 章节事实摘要" in prompt
    # 逐行净化：多 Writer 区块内的非多 Writer 内容必须幸存
    assert "前 3—10 章不要默认给所有功能角色正式名字" in prompt
    assert "已经建立的重要角色不得被机械改成身份称呼" in prompt
    assert "最终给作者的 Codex 返回必须使用以下三个一级标题" in prompt
    # 摘要长度约束在净化后旧模板路径仍然在场
    assert "只放 100—200 字事实摘要" in prompt
    # Audit 合同被替换为新「只报实际事项，无则写无」规则，不再强迫制造问题
    assert "Writer Audit 只报告实际存在的事项" in prompt
    assert "无需要报告的冲突或实质调整" in prompt
    # 完整 WRITER_AUDIT_RULE 全文只由 PROSE_REALIZATION_CONTRACT 注入一次，
    # sanitize 的 Audit 替换行只是一行短句，不得造成双注入。
    assert prompt.count(WRITER_AUDIT_RULE) == 1
    assert "2—5 个连续性问题" not in prompt
    assert "2—5 个表达实现问题" not in prompt
    # 净化只作用于 prompt 组装，PROMPTS.md 文件本身不被修改
    assert "串行写作协议" in prompts_path.read_text(encoding="utf-8")


def test_chapter_prompt_injects_minimal_authority_rule_once() -> None:
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert MINIMAL_AUTHORITY_RULE in prompt
    assert prompt.count(MINIMAL_AUTHORITY_RULE) == 1
    assert prompt.count("已批准的正式前文；已经发生事实的最高来源") == 1
    assert prompt.count(PROSE_REALIZATION_CONTRACT) == 1
    # 摘要长度约束的唯一权威来源：PROSE_REALIZATION_CONTRACT 的 Output boundary，
    # 默认模板路径与净化后旧模板路径因此一致（旧模板路径另见
    # test_legacy_book_level_chapter_template_is_sanitized_to_single_writer）。
    assert "`# 章节事实摘要` 只放 100—200 字事实摘要，不写入章节正文文件。" in prompt
    assert "只放 100—200 字事实摘要" in prompt


def test_narrative_function_stays_in_planning_and_is_not_exposed_to_writer() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "结尾推动力",
    )) + "\n叙事功能：本章完成第一次公开兑现"
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=outline,
    )
    assert "叙事功能：本章完成第一次公开兑现" not in prompt
    assert "规划备注（planning note）" not in prompt
    assert "正文可见最小事件合同" in prompt
    assert "事实目标，不是正文措辞" in prompt
    assert "场景上下文——推动事件的人：内容" in prompt


def test_chapter_context_packet_separates_canon_plan_profile_and_optional_inspiration() -> None:
    book = """# 小说总体设计画像

## 2. 世界观结构
WORLD_SETTING_MARKER

## 6. 某中段设计
SECTION_SIX_MARKER

## 10. 节奏结构
PROSE_PROFILE_MARKER

## 11. 某后置设计
SECTION_ELEVEN_MARKER

# 未来十章逐章小纲

## 第1章：小纲
具体剧情：待写。

# 当前状态、未兑现承诺与作者备注
CANON_STATUS_MARKER
"""
    outline = _full_eight_field_outline()
    packet = build_chapter_context(
        book_content=book,
        current_long_block="PLAN_BLOCK_MARKER",
        previous_chapter_text="CANON_PROSE_MARKER",
        current_outline=outline,
        recent_summaries="CANON_SUMMARY_MARKER",
        gbrain_inspiration="INSPIRATION_MARKER",
        selected_references=[{"program_id": "ref-alpha"}],
    )
    assert isinstance(packet, ChapterContextPacket)
    # 确定性：同一输入两次构建完全一致
    assert packet == build_chapter_context(
        book_content=book,
        current_long_block="PLAN_BLOCK_MARKER",
        previous_chapter_text="CANON_PROSE_MARKER",
        current_outline=outline,
        recent_summaries="CANON_SUMMARY_MARKER",
        gbrain_inspiration="INSPIRATION_MARKER",
        selected_references=[{"program_id": "ref-alpha"}],
    )
    assert packet.authority == MINIMAL_AUTHORITY_RULE
    assert "CANON_PROSE_MARKER" in packet.recent_prose
    assert "CANON_STATUS_MARKER" in packet.canon_context
    assert "CANON_SUMMARY_MARKER" in packet.canon_context
    # §0—§5 长期设计进入 BOOK CONTRACT，不再混入 CANON INDEX
    assert "WORLD_SETTING_MARKER" in packet.book_contract
    assert "WORLD_SETTING_MARKER" not in packet.canon_context
    assert "PLAN_BLOCK_MARKER" in packet.rolling_plan
    assert "第1章：小纲" in packet.rolling_plan
    assert "PROSE_PROFILE_MARKER" in packet.prose_profile
    assert "INSPIRATION_MARKER" in packet.optional_inspiration
    assert "ref-alpha" in packet.optional_inspiration
    assert "触发事件：内容" in packet.chapter_mission
    # 验收点 8：packet 各区块都不含 §6 中段设计与 §11 后置设计的内容
    for block in (
        packet.authority,
        packet.book_contract,
        packet.chapter_mission,
        packet.canon_context,
        packet.recent_prose,
        packet.rolling_plan,
        packet.prose_profile,
        packet.optional_inspiration,
    ):
        assert "SECTION_SIX_MARKER" not in block
        assert "SECTION_ELEVEN_MARKER" not in block

    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content=book,
        current_long_block="PLAN_BLOCK_MARKER",
        previous_chapter_text="CANON_PROSE_MARKER",
        current_outline=outline,
        recent_summaries="CANON_SUMMARY_MARKER",
        gbrain_inspiration="INSPIRATION_MARKER",
        selected_references=[{"program_id": "ref-alpha"}],
    )
    for label in ("AUTHORITY", "BOOK CONTRACT", "CHAPTER MISSION", "CANON PROSE", "CANON INDEX", "PLAN", "PROSE PROFILE", "OPTIONAL INSPIRATION"):
        assert label in prompt


def test_chapter_prompt_without_inspiration_still_generates_and_marks_optional_block() -> None:
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert "OPTIONAL INSPIRATION" in prompt
    assert "不得覆盖以上任何层级（含 BOOK CONTRACT、CANON PROSE、CANON INDEX、PLAN）" in prompt
    assert "允许空结果，不补位" in prompt


def test_chapter_mode_accepts_at_most_two_gbrain_inspirations() -> None:
    slugs = [f"mechanisms/item-{index}" for index in range(4)]
    raw = "\n".join(f"[{0.99 - index / 100:.2f}] {slug} -- snippet" for index, slug in enumerate(slugs))
    result = retrieve_gbrain(
        mode="chapter",
        book_content="现实世界；无超自然",
        query_func=lambda _query, **_kwargs: raw,
        page_func=lambda slug: _page("Mechanism", f"抽象机制 {slug}"),
    )
    assert CHAPTER_FINAL_RESULT_LIMIT == 2
    assert result["final_limit"] == CHAPTER_FINAL_RESULT_LIMIT
    assert result["accepted_count"] == CHAPTER_FINAL_RESULT_LIMIT
    assert [item["slug"] for item in result["accepted"]] == slugs[:2]
    assert any(item["reason"] == "超过最终数量上限" for item in result["rejected"])


def test_creative_planning_and_existing_modes_keep_their_intended_final_limits() -> None:
    raw = "\n".join(f"[{0.99 - index / 100:.2f}] mechanisms/item-{index} -- snippet" for index in range(7))
    for mode, expected_limit in (("world_vision", CREATIVE_PLANNING_FINAL_RESULT_LIMIT), ("idea", CREATIVE_PLANNING_FINAL_RESULT_LIMIT), ("outline", FINAL_RESULT_LIMIT), ("review", FINAL_RESULT_LIMIT)):
        result = retrieve_gbrain(
            mode=mode,
            book_content="都市成长故事",
            query_override="manual test",
            query_func=lambda _query, **_kwargs: raw,
            page_func=lambda _slug: _page("Mechanism", "抽象材料。"),
        )
        assert result["final_limit"] == expected_limit
        assert result["accepted_count"] == expected_limit


def test_explicit_inactive_gbrain_card_is_not_used_as_inspiration() -> None:
    page = """---
active_inspiration: false
---

## Mechanism

这是仍保留在 GBrain 的 HOLD Pilot。
"""
    assert active_inspiration_allowed(page) is False
    result = retrieve_gbrain(
        mode="outline",
        book_content="玄幻成长故事",
        query_override="manual test",
        query_func=lambda _query, **_kwargs: "[0.9] mechanisms/hold-pilot -- hold",
        page_func=lambda _slug: page,
    )
    assert result["accepted_count"] == 0
    assert result["rejected"][0]["reason"] == "卡片当前未启用为 active inspiration"


def test_book_contract_takes_future_design_from_real_book_and_canon_stays_factual() -> None:
    # 验收点 1：BOOK §0—§5 的未来设计进 BOOK CONTRACT，不进 CANON INDEX，
    # 且最终 prompt 不再把这些未来内容标为「已经发生」。
    book = Path("books/real-exp-001/BOOK.md").read_text(encoding="utf-8")
    packet = build_chapter_context(
        book_content=book,
        current_outline=_full_eight_field_outline(),
    )
    # 三个中文 marker 是 BOOK.md（books/real-exp-001/BOOK.md）的受保护锚点：
    # 作者修订长期设计文字时需同步更新这里的断言文本。
    future_markers = (
        "16—35章转为学院试炼和战斗构筑",
        "人物弧从底层修补工到学院试炼胜者",
        "先轻视主角、再承认",
    )
    for marker in future_markers:
        assert marker in packet.book_contract
        assert marker not in packet.canon_context

    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content=book,
        current_outline=_full_eight_field_outline(),
    )
    assert "已经发生，不得修改" not in prompt
    start = prompt.index("## BOOK CONTRACT——长期设计与稳定方向，不等于已经发生")
    end = prompt.index("## CHAPTER MISSION——", start)
    contract_block = prompt[start:end]
    assert future_markers[0] not in contract_block
    assert future_markers[1] in contract_block
    assert future_markers[2] in contract_block
    assert "传统奇幻成长爽文" in contract_block
    assert "主角每次学会新术式" in contract_block
    assert "学院内容变成解释设定" in contract_block
    # BOOK CONTRACT 区块不混入当前状态（已发生事实）
    assert "当前已完成第3章" not in contract_block


def test_canon_index_holds_status_and_summaries_and_canon_prose_stays_top_source() -> None:
    # 验收点 2：当前状态与最近摘要进 CANON INDEX；正式前文只进 recent_prose，
    # 且权威层级文案确认正式前文仍是最高事实来源。
    book = """# 小说总体设计画像

## 2. 世界观结构
CONTRACT_WORLD_MARKER

# 当前状态、未兑现承诺与作者备注
INDEX_STATUS_MARKER
"""
    packet = build_chapter_context(
        book_content=book,
        previous_chapter_text="CANON_PROSE_TOP_MARKER",
        current_outline=_full_eight_field_outline(),
        recent_summaries="INDEX_SUMMARY_MARKER",
    )
    assert "INDEX_STATUS_MARKER" in packet.canon_context
    assert "INDEX_SUMMARY_MARKER" in packet.canon_context
    assert "CANON_PROSE_TOP_MARKER" in packet.recent_prose
    assert "CANON_PROSE_TOP_MARKER" not in packet.canon_context
    assert "CANON_PROSE_TOP_MARKER" not in packet.book_contract
    assert "CONTRACT_WORLD_MARKER" in packet.book_contract
    assert "CONTRACT_WORLD_MARKER" not in packet.canon_context
    assert "已批准的正式前文；已经发生事实的最高来源" in MINIMAL_AUTHORITY_RULE
    assert "与正式正文冲突时以正式正文为准" in MINIMAL_AUTHORITY_RULE


def test_chapter_prompt_renders_six_authority_blocks_with_separated_semantics() -> None:
    # 验收点 3：六个权威标签都在场，且各自只承担自己的语义。
    book = """# 小说总体设计画像

## 0. 本书成长基因图
CONTRACT_GENOME_MARKER

## 7. 叙事结构
PROFILE_NARRATIVE_MARKER

# 当前状态、未兑现承诺与作者备注
INDEX_STATUS_MARKER
"""
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content=book,
        previous_chapter_text="CANON_PROSE_TOP_MARKER",
        current_outline=_full_eight_field_outline(),
        recent_summaries="INDEX_SUMMARY_MARKER",
    )
    for label in (
        "CANON PROSE",
        "BOOK CONTRACT",
        "CANON INDEX",
        "PLAN",
        "PROSE PROFILE",
        "OPTIONAL INSPIRATION",
    ):
        assert label in prompt
    titles = (
        "## AUTHORITY——",
        "## BOOK CONTRACT——",
        "## CHAPTER MISSION——",
        "## CANON PROSE——",
        "## CANON INDEX——",
        "## PLAN——",
        "## PROSE PROFILE——",
        "## OPTIONAL INSPIRATION——",
    )
    positions = {title: prompt.index(title) for title in titles}

    def _block(title: str) -> str:
        start = positions[title]
        later = [positions[other] for other in titles if positions[other] > start]
        end = min(later) if later else len(prompt)
        return prompt[start:end]

    contract_block = _block("## BOOK CONTRACT——")
    index_block = _block("## CANON INDEX——")
    assert "CONTRACT_GENOME_MARKER" in contract_block
    assert "INDEX_STATUS_MARKER" not in contract_block
    assert "INDEX_STATUS_MARKER" in index_block
    assert "INDEX_SUMMARY_MARKER" in index_block
    assert "CONTRACT_GENOME_MARKER" not in index_block
    assert "## 0. 本书成长基因图" not in index_block
    assert "CANON_PROSE_TOP_MARKER" in _block("## CANON PROSE——")
    assert "PROFILE_NARRATIVE_MARKER" in _block("## PROSE PROFILE——")


def test_default_chapter_prompt_audit_only_reports_actual_items() -> None:
    # 验收点 4：Audit 允许没有问题；不再强迫制造 2—5 个发现。
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert "Writer Audit 只报告实际存在的事项" in prompt
    assert "无需要报告的冲突或实质调整" in prompt
    assert "不要把正常的场景安排、遣词选择、句段变化或普通润色包装成问题" in prompt
    assert "2—5 个连续性问题" not in prompt
    assert "2—5 个表达实现问题" not in prompt
    # 三标题输出合同与摘要 100—200 字约束保留
    for heading in ("# Writer Audit", "# 正式正文", "# 章节事实摘要"):
        assert heading in prompt
    assert "只放 100—200 字事实摘要" in prompt


# ---------------------------------------------------------------------------
# State Delta Proposal v1 + Canon Index Normalization（任务 #2）
# ---------------------------------------------------------------------------


STATE_DELTA_STATUS_FIXTURE = """当前已完成第3章。

最近章节摘要：
第1章：林砚补上最小连接，挡住碎石雨。
第2章：
- 林砚修复完整火符；
- 完整火符卖给葛宁。

当前状态：
林砚在废弃升降井；手持八枚铜角。

未兑现承诺：
- 浮空城为什么持续下沉；
- 学院试炼尚未发生。
作者备注：前三章可接受；继续观察。"""

STATE_DELTA_BOOK = f"""# 小说总体设计画像

## 2. 世界观结构
CONTRACT_WORLD_MARKER

## 8. 文风与可操作参数
PROSE_STYLE_MARKER

# 未来100章大型剧情块
FULL_PLAN_MARKER

# 当前状态、未兑现承诺与作者备注
当前已完成第3章。

最近章节摘要：
BOOK_RECENT_SUMMARY_MARKER

当前状态：
林砚在废弃升降井。

未兑现承诺：
- 浮空城为什么持续下沉。

作者备注：前三章可接受；继续观察。
"""

LABELED_STATUS_BOOK = """# 小说总体设计画像

## 2. 世界观结构
CONTRACT_WORLD_MARKER

# 当前状态、未兑现承诺与作者备注
当前已完成第2章。

最近章节摘要：
BOOK_RECENT_SUMMARY_MARKER

当前状态：
现场状态标记。

未兑现承诺：
- 承诺标记。

作者备注：
作者备注标记。
"""


def test_authority_rule_is_three_dimensional_with_canon_prose_over_canon_index() -> None:
    # 验收点 1：已发生事实规则明确为 CANON PROSE > CANON INDEX，
    # 且权威改为三维度规则，不再是六级总排名。
    assert "已发生事实：CANON PROSE > CANON INDEX" in MINIMAL_AUTHORITY_RULE
    assert "未来创作意图：BOOK CONTRACT > PLAN > OPTIONAL INSPIRATION" in MINIMAL_AUTHORITY_RULE
    assert "表达控制：PROSE PROFILE 只控制表达方式，不能修改已发生事实或未来计划" in MINIMAL_AUTHORITY_RULE
    assert "跨维度冲突" in MINIMAL_AUTHORITY_RULE
    assert "权威层级（从高到低）" not in MINIMAL_AUTHORITY_RULE
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert "已发生事实：CANON PROSE > CANON INDEX" in prompt
    assert "PROSE PROFILE 只控制表达方式" in prompt


def test_book_contract_cannot_override_facts_that_already_happened() -> None:
    # 验收点 2：BOOK CONTRACT 不得覆盖已发生事实。
    assert "已发生事实不能被 BOOK CONTRACT 或 PLAN 覆盖" in MINIMAL_AUTHORITY_RULE
    assert "不能修改已发生事实或未来计划" in MINIMAL_AUTHORITY_RULE


def test_writer_reports_drift_only_and_state_delta_does_not_check_drift() -> None:
    # BOOK CONTRACT drift 由 Curator 暴露，Primary 不做 pipeline bookkeeping；
    # state extraction 不检查或报告 drift。
    assert "Curator 负责在 Curator Audit 中暴露" in MINIMAL_AUTHORITY_RULE
    assert "Primary 不承担冲突报告" in MINIMAL_AUTHORITY_RULE
    assert "不得自动修改 BOOK CONTRACT" in MINIMAL_AUTHORITY_RULE
    assert "drift" not in DEFAULT_STATE_DELTA_TEMPLATE.lower()
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="NEW_CHAPTER_PROSE_MARKER",
    )
    assert "drift" not in prompt.lower()
    assert "不输出审计" in prompt


def test_parse_canon_index_reads_the_four_fields_from_real_status_format() -> None:
    # 验收点 4：状态区能解析 current_state / recent_summaries / open_promises / author_notes。
    fields = parse_canon_index(STATE_DELTA_STATUS_FIXTURE)
    assert set(fields) == {"current_state", "recent_summaries", "open_promises", "author_notes"}
    assert fields["current_state"].startswith("当前已完成第3章。")
    assert "林砚在废弃升降井；手持八枚铜角。" in fields["current_state"]
    assert "第1章：林砚补上最小连接，挡住碎石雨。" in fields["recent_summaries"]
    assert "- 完整火符卖给葛宁。" in fields["recent_summaries"]
    assert "浮空城为什么持续下沉" in fields["open_promises"]
    assert "学院试炼尚未发生" in fields["open_promises"]
    assert fields["author_notes"] == "前三章可接受；继续观察。"
    # 空输入与默认模板格式都不抛错，四键始终在场。
    assert set(parse_canon_index("")) == {
        "current_state", "recent_summaries", "open_promises", "author_notes"
    }
    default_fields = parse_canon_index("当前状态：\n\n未兑现承诺：\n\n作者备注：")
    assert set(default_fields) == {
        "current_state", "recent_summaries", "open_promises", "author_notes"
    }


def test_recent_summaries_are_injected_only_once_in_state_delta_and_chapter_prompts() -> None:
    # 验收点 5：页面显式 recent_summaries 与 BOOK 内摘要不会重复注入。
    explicit = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="PROSE_MARKER",
        recent_summaries="PAGE_SUMMARY_MARKER",
    )
    assert explicit.count("PAGE_SUMMARY_MARKER") == 1
    assert "BOOK_RECENT_SUMMARY_MARKER" not in explicit

    fallback = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="PROSE_MARKER",
    )
    assert fallback.count("BOOK_RECENT_SUMMARY_MARKER") == 1
    assert "本次只注入这一份" in fallback

    # chapter 模式同样只注入一份。
    chapter_explicit = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=LABELED_STATUS_BOOK,
        current_outline=_full_eight_field_outline(),
        recent_summaries="PAGE_SUMMARY_MARKER",
    )
    assert chapter_explicit.count("PAGE_SUMMARY_MARKER") == 1
    assert "BOOK_RECENT_SUMMARY_MARKER" not in chapter_explicit

    chapter_fallback = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=LABELED_STATUS_BOOK,
        current_outline=_full_eight_field_outline(),
    )
    assert chapter_fallback.count("BOOK_RECENT_SUMMARY_MARKER") == 1


def test_author_notes_are_marked_as_meta_control() -> None:
    # 验收点 6：AUTHOR NOTES 被标为元控制，不属于 Canon 事实。
    rendered = render_canon_index(parse_canon_index(STATE_DELTA_STATUS_FIXTURE))
    assert "作者元控制" in rendered
    assert "不属于 Canon 事实" in rendered
    assert "State Delta 不得自动修改或删除" in rendered
    assert "前三章可接受；继续观察。" in rendered
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="PROSE_MARKER",
    )
    assert "作者元控制" in prompt
    assert "前三章可接受；继续观察。" in prompt
    assert "AUTHOR NOTES 由代码逐字保留" in prompt


def test_state_delta_prompt_excludes_gbrain_references_full_plan_and_prose_profile() -> None:
    # 验收点 7：State Delta Prompt 不含 GBrain、Reference Programs、完整百章计划或 prose profile。
    assert "state_delta" in PROMPT_MODES
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="NEW_CHAPTER_PROSE_MARKER",
        chapter_fact_summary="FACT_SUMMARY_MARKER",
        previous_chapter_text="PREVIOUS_PROSE_MARKER",
        gbrain_inspiration="GBRAIN_MARKER",
        selected_references=[{"program_id": "REF_MARKER"}],
        current_long_block="LONG_BLOCK_MARKER",
    )
    for marker in (
        "GBRAIN_MARKER",
        "REF_MARKER",
        "FULL_PLAN_MARKER",
        "PROSE_STYLE_MARKER",
        "CONTRACT_WORLD_MARKER",
        "PREVIOUS_PROSE_MARKER",
        "LONG_BLOCK_MARKER",
        "GBrain Inspiration Results",
        "Reference Program 1",
    ):
        assert marker not in prompt
    assert "NEW_CHAPTER_PROSE_MARKER" in prompt


def test_state_delta_prompt_uses_formal_prose_directly_without_writer_summary() -> None:
    # Primary 不再做事实摘要；State Extraction 直接从正式正文提取。
    assert "本次正式正文是 State Delta 的最高事实来源" in DEFAULT_STATE_DELTA_TEMPLATE
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="NEW_CHAPTER_PROSE_MARKER",
        chapter_fact_summary="FACT_SUMMARY_MARKER",
    )
    assert "本次新正式章节正文（State Delta 的最高事实来源）" in prompt
    assert "NEW_CHAPTER_PROSE_MARKER" in prompt
    assert "FACT_SUMMARY_MARKER" not in prompt
    assert "# State Delta Audit" not in prompt
    for heading in (
        "# Proposed Active Scene State",
        "# Proposed Persistent Canon",
        "# Proposed Chapter Summary",
        "# Proposed Open Promises",
    ):
        assert heading in prompt
    assert "最多 12 条" in prompt
    assert "不要输出 JSON/YAML" in prompt


def test_state_extraction_compacts_existing_long_memory_before_llm_input() -> None:
    summaries = "\n".join(f"第{i}章：SUMMARY_{i}" for i in range(1, 6))
    promises = "\n".join(f"- PROMISE_{i}" for i in range(1, 16))
    book = f"""# 当前状态、未兑现承诺与作者备注
当前已完成第5章。

## ACTIVE SCENE STATE
当前地点：集市。

## PERSISTENT CANON
已证明能力：识路。

## RECENT SUMMARIES
{summaries}

## OPEN PROMISES
{promises}

## AUTHOR NOTES
继续观察。
"""
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=book,
        chapter_number=6,
        chapter_prose="第六章正式正文。",
    )

    assert "SUMMARY_1" not in prompt
    assert "SUMMARY_2" not in prompt
    for marker in ("SUMMARY_3", "SUMMARY_4", "SUMMARY_5"):
        assert marker in prompt
    assert "PROMISE_12" in prompt
    for marker in ("PROMISE_13", "PROMISE_14", "PROMISE_15"):
        assert marker not in prompt


def test_apply_canon_index_proposal_requires_heading_and_content() -> None:
    # 验收点 9：模型返回缺少 `# Proposed Canon Index`（或内容为空）时不修改页面。
    html = Path("src/story_mvp/templates/index.html").read_text(encoding="utf-8")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    for marker in (
        'id="generate-state-delta-prompt"',
        'id="state-delta-response"',
        'id="apply-canon-index-proposal"',
        "State Delta 不是章节门禁",
    ):
        assert marker in html
    start = js.index("function extractProposedCanonIndex")
    end = js.index("function applyCanonIndexProposal", start)
    extractor = js[start:end]
    # 精确化后：行首一级标题匹配 + 围栏代码块剥离 + 终止限定下一个一级标题。
    assert r"const heading = /^# Proposed Canon Index[ \t]*$/;" in extractor
    assert "if (start < 0) return null;" in extractor
    # 内容为空同样返回 null，不会应用空提案。
    assert "return content ? content : null;" in extractor
    apply_start = js.index("function applyCanonIndexProposal")
    apply_end = js.index("async function saveBook", apply_start)
    apply_body = js[apply_start:apply_end]
    assert "if (!proposed)" in apply_body
    assert "未修改 BOOK 状态编辑区" in apply_body


def test_apply_canon_index_proposal_is_browser_only_and_touches_status_editor_only() -> None:
    # 验收点 10：应用 Proposal 只修改页面状态编辑区，不调用 API。
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    apply_start = js.index("function applyCanonIndexProposal")
    apply_end = js.index("async function saveBook", apply_start)
    apply_body = js[apply_start:apply_end]
    assert '$("section-status").value = proposed;' in apply_body
    assert "requestJson" not in apply_body
    assert "fetch(" not in apply_body
    assert "PUT" not in apply_body
    assert "尚未写盘" in apply_body
    # 不触碰其它 BOOK 区块编辑区。
    for other in ('$("section-long_plan")', '$("section-small_plan")', '$("design-'):
        assert other not in apply_body


def test_save_book_remains_the_only_book_write_action() -> None:
    # 验收点 11：Save BOOK 仍是唯一写盘动作；State Delta 控件不调用保存 API。
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    save_start = js.index("async function saveBook")
    save_end = js.index("async function saveTemplates", save_start)
    save_body = js[save_start:save_end]
    assert 'method: "PUT"' in save_body
    assert "composeBookContent()" in save_body

    gen_start = js.index("async function generateStateDeltaPrompt")
    gen_end = js.index("async function copyPrompt", gen_start)
    gen_body = js[gen_start:gen_end]
    assert '"/api/prompt/state-delta"' in gen_body
    for marker in ("PUT", "/book", "/chapters", "saveBook"):
        assert marker not in gen_body


def test_state_delta_flow_does_not_write_book_or_chapters() -> None:
    # 验收点 12：State Delta 不修改 BOOK CONTRACT、PLAN 或章节文件；
    # 章节批准/保存也不自动触发 State Delta。
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    approve_start = js.index("async function approveChapter")
    approve_end = js.index("async function createBook", approve_start)
    approve_body = js[approve_start:approve_end]
    assert "state-delta" not in approve_body
    assert "generateStateDeltaPrompt" not in approve_body


def test_state_delta_prompt_generation_does_not_touch_files(tmp_path: Path, monkeypatch) -> None:
    # 验收点 12（API 层）：生成 State Delta Prompt 不写 BOOK、不写章节、不写 PROMPTS。
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client.post("/api/books", json={"book_id": "demo"})
    client.post(
        "/api/books/demo/chapters",
        json={"chapter_number": 1, "content": "chapter one body"},
    )
    book_path = tmp_path / "demo" / "BOOK.md"
    prompts_path = tmp_path / "demo" / "PROMPTS.md"
    before_book = book_path.read_text(encoding="utf-8")
    before_prompts = prompts_path.read_text(encoding="utf-8")
    before_chapters = sorted(
        path.name for path in (tmp_path / "demo" / "chapters").iterdir()
    )

    for url in ("/api/prompt/state-delta", "/api/prompt"):
        response = client.post(
            url,
            json={
                "mode": "state_delta",
                "book_content": STATE_DELTA_BOOK,
                "chapter_number": 4,
                "chapter_prose": "NEW_CHAPTER_PROSE_MARKER",
                "chapter_fact_summary": "FACT_SUMMARY_MARKER",
                "recent_summaries": "PAGE_SUMMARY_MARKER",
            },
        )
        assert response.status_code == 200
        prompt = response.json()["prompt"]
        assert "NEW_CHAPTER_PROSE_MARKER" in prompt
        assert "# Proposed Canon Index" in prompt

    assert book_path.read_text(encoding="utf-8") == before_book
    assert prompts_path.read_text(encoding="utf-8") == before_prompts
    assert sorted(path.name for path in (tmp_path / "demo" / "chapters").iterdir()) == before_chapters
    assert (tmp_path / "demo" / "chapters" / "chapter-0001.md").read_text(encoding="utf-8") == "chapter one body"


# ---------------------------------------------------------------------------
# 三维度代码评审修复项（任务 #4 修复阶段）
# ---------------------------------------------------------------------------


UNLABELED_STATUS_BOOK = """# 小说总体设计画像

# 当前状态、未兑现承诺与作者备注
当前已完成第3章。
林砚在废弃升降井休整。
旧格式自由文本状态。
"""


def test_state_delta_unlabeled_status_falls_back_to_raw_injection() -> None:
    # 修复 1：state_delta 无标签旧格式状态区原样注入，不被 parse 静默清空。
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=UNLABELED_STATUS_BOOK,
        chapter_number=4,
        chapter_prose="PROSE_MARKER",
    )
    assert "当前已完成第3章。" in prompt
    assert "旧格式自由文本状态。" in prompt
    assert "CURRENT STATE（已发生事实的压缩状态）" not in prompt

    # 无标签回退时页面显式摘要单独注入一份，不重复也不丢失。
    with_page = generate_prompt(
        mode="state_delta",
        template="",
        book_content=UNLABELED_STATUS_BOOK,
        chapter_number=4,
        chapter_prose="PROSE_MARKER",
        recent_summaries="PAGE_SUMMARY_MARKER",
    )
    assert with_page.count("PAGE_SUMMARY_MARKER") == 1
    assert "旧格式自由文本状态。" in with_page
    # 有标签状态区仍走标签路径（real-exp-001 路径不受影响）。
    labeled = generate_prompt(
        mode="state_delta",
        template="",
        book_content=STATE_DELTA_BOOK,
        chapter_number=4,
        chapter_prose="PROSE_MARKER",
    )
    assert "CURRENT STATE（已发生事实的压缩状态）" in labeled


def test_parse_canon_index_keeps_pre_label_lines_in_current_state() -> None:
    # 修复 3：首个标签前的无标签行并入 current_state（前导无标签行用例固化）。
    fields = parse_canon_index("当前已完成第2章。\n林砚刚到浮空城。\n\n当前状态：\n在集市门口。")
    assert fields["current_state"] == "当前已完成第2章。\n林砚刚到浮空城。\n在集市门口。"
    unlabeled_only = parse_canon_index("当前已完成第1章。\n状态行一。\n状态行二。")
    assert unlabeled_only["current_state"] == "当前已完成第1章。\n状态行一。\n状态行二。"
    # 确定性行为固化：内容行以标签+冒号开头会整体切换字段。
    switch = parse_canon_index("当前状态：\n林砚手持铜角。\n作者备注：继续观察。")
    assert switch["current_state"] == "林砚手持铜角。"
    assert switch["author_notes"] == "继续观察。"
    # 该约束在函数 docstring 与 State Delta 文案中显式记录。
    assert "内容行不应以" in (parse_canon_index.__doc__ or "")
    assert "各字段内容行不要以旧格式" in DEFAULT_STATE_DELTA_TEMPLATE


def test_canon_index_has_labels_requires_at_least_one_field_label() -> None:
    # 追加修复 C：仅含「当前已完成第N章。」无字段标签时判定为无标签。
    assert canon_index_has_labels("当前已完成第3章。\n自由文本状态。") is False
    assert canon_index_has_labels("") is False
    assert canon_index_has_labels("当前状态：\n在集市门口。") is True
    assert canon_index_has_labels("作者备注：尚可。") is True
    assert canon_index_has_labels(STATE_DELTA_STATUS_FIXTURE) is True
    # chapter 模式：仅完成行的状态区原样注入，不渲染「（未填写）」占位块。
    book = (
        "# 小说总体设计画像\n\n"
        "# 当前状态、未兑现承诺与作者备注\n"
        "当前已完成第1章。\n自由状态文本。"
    )
    packet = build_chapter_context(book_content=book)
    assert "自由状态文本。" in packet.canon_context
    assert "CURRENT STATE（已发生事实的压缩状态）" not in packet.canon_context


def test_chapter_prep_injects_recent_summaries_only_once() -> None:
    # 追加修复 A：页面显式摘要非空时，chapter_prep 扣除标签化状态区内嵌摘要。
    explicit = generate_prompt(
        mode="chapter_prep",
        template="PREP TEMPLATE",
        book_content=LABELED_STATUS_BOOK,
        recent_summaries="PAGE_SUMMARY_MARKER",
    )
    assert explicit.count("PAGE_SUMMARY_MARKER") == 1
    assert "BOOK_RECENT_SUMMARY_MARKER" not in explicit
    # 其余状态段仍注入。
    assert "现场状态标记。" in explicit
    assert "- 承诺标记。" in explicit
    # 页面摘要为空时保持注入 BOOK 内摘要。
    fallback = generate_prompt(
        mode="chapter_prep",
        template="PREP TEMPLATE",
        book_content=LABELED_STATUS_BOOK,
    )
    assert fallback.count("BOOK_RECENT_SUMMARY_MARKER") == 1


def test_state_delta_template_exclusion_lists_ten_chapter_plan_and_references() -> None:
    # 追加修复 B-1：排除声明补全十章计划与 Reference Programs。
    assert (
        "BOOK CONTRACT、完整百章计划、十章计划、prose profile、GBrain、"
        "Reference Programs 与前两章正文都不在本次输入中"
    ) in DEFAULT_STATE_DELTA_TEMPLATE


def test_authority_wording_is_dimension_based_not_rank_based() -> None:
    # 追加修复 B-2：两处「权威层级」残留改为三维度语义表述。
    assert "权威规则（按维度划分）与冲突处理" in PROSE_REALIZATION_CONTRACT
    assert "权威层级" not in PROSE_REALIZATION_CONTRACT
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content="",
        current_outline=_full_eight_field_outline(),
    )
    assert "## AUTHORITY——权威规则（按维度划分）与冲突处理" in prompt
    assert "权威层级" not in prompt


def test_extract_proposed_canon_index_ignores_code_blocks_and_keeps_subheadings() -> None:
    # 修复 2：代码块/Audit 中的引用不误提取；提案内 ## 子标题不被截断。
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("function extractProposedCanonIndex")
    end = js.index("function applyCanonIndexProposal", start)
    extractor = js[start:end]
    # 先剥离围栏代码块，代码块内或 Audit 中的引用不会命中。
    assert "response.replace(" in extractor
    assert "```" in extractor
    # 行首一级标题匹配；终止条件限定下一个一级标题（## 子标题不截断）。
    assert r"/^#(?!\#)/" in extractor
    # 两个守卫保留。
    assert "if (start < 0) return null;" in extractor
    assert "return content ? content : null;" in extractor


def test_state_delta_generation_rejects_invalid_chapter_number_or_empty_prose(tmp_path: Path, monkeypatch) -> None:
    # 修复 4：生成动作用 400 拦截；不是章节门禁，章节保存不受影响。
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client.post("/api/books", json={"book_id": "demo"})
    base = {"mode": "state_delta", "book_content": STATE_DELTA_BOOK}

    empty_prose = client.post(
        "/api/prompt/state-delta", json={**base, "chapter_number": 4, "chapter_prose": "   "}
    )
    assert empty_prose.status_code == 400
    zero_chapter = client.post(
        "/api/prompt/state-delta", json={**base, "chapter_number": 0, "chapter_prose": "PROSE"}
    )
    assert zero_chapter.status_code == 400
    negative_chapter = client.post(
        "/api/prompt/state-delta", json={**base, "chapter_number": -1, "chapter_prose": "PROSE"}
    )
    assert negative_chapter.status_code == 422  # PromptRequest.chapter_number ge=0
    # /api/prompt 入口同样拦截。
    assert client.post(
        "/api/prompt", json={**base, "chapter_number": 0, "chapter_prose": "PROSE"}
    ).status_code == 400
    # 合法输入仍正常生成。
    ok = client.post(
        "/api/prompt/state-delta", json={**base, "chapter_number": 4, "chapter_prose": "PROSE"}
    )
    assert ok.status_code == 200
    # 拦截不是章节门禁：无效生成请求之后章节保存照常可用。
    saved = client.post(
        "/api/books/demo/chapters", json={"chapter_number": 4, "content": "chapter four body"}
    )
    assert saved.status_code == 200


def test_generate_state_delta_prompt_front_guards_and_output_notice() -> None:
    # 修复 4（前端）+ 追加修复 E：空正文/无效章节号阻止生成；成功文案提示已替换输出区。
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    gen_start = js.index("async function generateStateDeltaPrompt")
    gen_end = js.index("async function copyPrompt", gen_start)
    gen_body = js[gen_start:gen_end]
    assert "需要正整数的当前章节编号" in gen_body
    assert "正式正文为空，无法生成 State Delta Prompt" in gen_body
    # 守卫在发起请求之前。
    assert gen_body.index("chapter-body-for-save") < gen_body.index("requestJson")
    assert 'executeOpenAI(payload.prompt, "state_delta")' in gen_body
    assert "独立 State 模型" in gen_body


def test_browser_state_delta_apply_uses_bounded_memory_windows() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "function compactPromiseWindow(text, maxEntries = 12)" in js
    assert "function compactRecentSummaryWindow(text, keep = 3)" in js
    start = js.index("function buildCanonMemoryStatus")
    end = js.index("function applyCanonIndexProposal", start)
    body = js[start:end]
    assert "compactRecentSummaryWindow" in body
    assert "compactPromiseWindow(proposed.open_promises)" in body


def test_recent_summaries_hint_warns_about_overriding_book_summaries() -> None:
    # 追加修复 D：页面摘要输入框附近提示会覆盖 BOOK 内嵌摘要。
    html = Path("src/story_mvp/templates/index.html").read_text(encoding="utf-8")
    start = html.index('id="recent-summaries"')
    end = html.index('id="actual-summaries"', start)
    region = html[start:end]
    assert "页面摘要会覆盖 BOOK 状态区内嵌摘要，生成章节 Prompt 前请先与 BOOK 同步" in region
