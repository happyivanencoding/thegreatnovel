from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from novel_authoring.config import load_settings
from novel_authoring.contracts.draft import DraftOutput
from novel_authoring.db.database import Database
from novel_authoring.drafting.service import import_draft_output
from novel_authoring.library_catalog import build_library_catalog, studio_access
from novel_authoring.original.models import (
    CoreInnovationCandidate,
    CoreInnovationProposal,
    OriginalBootstrapProposal,
)
from novel_authoring.original.service import (
    OriginalWorkflowError,
    approve_original_first_chapter,
    compare_original_proposals,
    confirm_original_foundation,
    confirm_original_reader_experience,
    create_original_book,
    import_original_bootstrap_proposal,
    import_original_core_innovation_proposal,
    original_overview,
    prepare_original_bootstrap,
    resolve_original_proposal_version,
    select_first_chapter_candidate,
    select_original_core_innovation,
    validate_original_draft,
)
from novel_authoring.planning.models import ChapterContract
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookKind, BookRegistry, CreationMode
from novel_authoring.utils import json_dumps
from novel_authoring.web.app import create_app
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    HandoffWorkflowError,
    claim_handoff,
    complete_handoff,
    create_continuation_handoff,
    get_handoff,
    start_handoff,
    update_handoff_status,
)

BOOK_ID = "original-test"


def innovation_payload() -> dict[str, Any]:
    return {
        "schema_version": "core-innovation-v1",
        "information_status": "PROPOSAL",
        "innovation_candidates": [
            {
                "innovation_id": f"innovation-{index}",
                "title": f"核心机制 {index}",
                "one_sentence_hook": f"同一承诺通过机制 {index} 持续产生新选择。",
                "core_mechanism": f"机制杠杆 {index}",
                "protagonist_special_rule": f"主角的特殊规则 {index}",
                "choice_generation": f"选择空间来源 {index}",
                "progression_generation": f"成长空间来源 {index}",
                "payoff_generation": f"兑现方式 {index}",
                "limitation": f"限制与代价 {index}",
                "expansion_grammar": f"行动空间沿机制 {index} 扩展",
                "long_form_capacity": f"可以持续产生新瓶颈与组合 {index}",
                "novelty_source": f"新颖性来源 {index}",
                "repetition_risk": f"重复风险 {index}",
                "fit_with_reader_promise": f"与已确认阅读承诺的契合点 {index}",
            }
            for index in range(1, 4)
        ],
        "kernel_contracts": {},
    }


def proposal_payload() -> dict[str, Any]:
    return {
        "schema_version": "original-bootstrap-v3",
        "information_status": "PROPOSAL",
        "core_innovation_intent": {
            "selected_primary_innovation_id": "innovation-1",
            "optional_mix_notes": "吸收机制 2 的一个选择特征",
        },
        "title_candidates": ["无情之城", "昨日情绪档案", "被删除的悲伤"],
        "expanded_premise": "城市每天删除一种情感，失忆档案员决定找回它们。",
        "foundation_candidates": [
            {
                "candidate_id": f"foundation-{index}",
                "title": f"基础框架 {index}",
                "core_reading_promise": f"让每次找回情感都迫使主角承担选择 {index}",
                "protagonist": "林默",
                "protagonist_goal": "找回被删除的情感",
                "main_conflict": f"城市记忆局以秩序之名阻止调查 {index}",
                "world_mechanism": "午夜删除一种情感，并留下可追踪的物理空洞",
                "growth_loop": "调查空洞、主动选择、承担记忆代价",
                "long_term_possibility": "逐步逼近城市共识的多种可能来源",
                "risk": "世界机制压过人物选择",
                "premise_relationship": "直接展开 premise，不预设幕后答案",
                "author_facing_pitch": "主角在具体压力中用已选机制做出代价明确的选择。",
                "opening_situation": "清晨档案室出现异常空洞，主角必须立即决定是否介入。",
                "typical_choice": "在保护现有生活与测试核心机制之间做出不可逆选择。",
                "innovation_fit": "这个承载方式让核心机制直接改变人物行动。",
            }
            for index in range(1, 4)
        ],
        "protagonist": "林默",
        "protagonist_goal": "找回被删除的情感",
        "protagonist_conflict": "每次找回都会失去一段私人记忆",
        "protagonist_cost": "私人记忆",
        "protagonist_growth": "从记录者变成愿意承担后果的行动者",
        "world_rules": [
            "午夜删除一种情感",
            "被删除的情感会留下可追踪的物理空洞",
        ],
        "foundation_settings": [
            {
                "setting_id": "setting-world-rule",
                "category": "WORLD_RULE",
                "statement": "午夜删除一种情感",
                "strength": "CORE",
            },
            {
                "setting_id": "setting-style",
                "category": "STYLE",
                "statement": "整体采用冷峻克制的文风",
                "strength": "PREFERENCE",
            },
            {
                "setting_id": "setting-controller",
                "category": "WORLD_DESIGN",
                "statement": "删除机制是否由组织控制",
                "strength": "OPEN",
            },
        ],
        "characters": ["林默", "许栀"],
        "factions": ["城市记忆局"],
        "routes": [
            {
                "route_id": f"route-{index}",
                "title": f"路线 {index}",
                "direction": f"以不同关系入口追查删除机制 {index}",
                "central_pressure": f"秩序与私人记忆的冲突 {index}",
                "opportunity": f"打开新的城市层级 {index}",
                "risk": f"路线风险 {index}",
                "commitments": [f"主角必须主动追查路线 {index}"],
                "open_alternatives": [f"保留路线 {index} 的幕后来源"],
            }
            for index in range(1, 4)
        ],
        "recommended_route_id": "route-2",
        "recommendation_reason": "人物代价与世界机制结合最紧密",
        "progression_grammar": ["通过新的可验证选择获得新的行动能力"],
        "expansion_grammar": ["从当前环境向更大的问题空间自然扩展，不预设固定层数"],
        "payoff_grammar": ["先兑现当前机制，再暴露更高瓶颈与组合可能"],
        "first_phase": {
            "opening_pressure": "异常空洞在公开场合出现，主角必须承担立即后果。",
            "first_concrete_goal": "阻止下一次删除并找到第一位保留者",
            "first_resource_bottleneck": "调查时间与可用记忆不足",
            "first_progression_opportunity": "首次确认核心机制可以改变行动条件",
            "first_payoff": "主角用有限能力取得第一条真实线索",
            "first_meaningful_escalation": "对手开始针对主角的选择设置反制",
            "stage_climax": "主角在公开压力下完成一次不可逆选择",
            "after_climax_change": "主角失去原有安全位置并获得新的行动权限",
        },
        "first_phase_objective": "阻止下一次删除并找到第一位保留者",
        "rolling_planning": {
            "short": ["找到第一处情绪空洞"],
            "mid": ["进入城市记忆局的边缘系统"],
            "long": ["保留城市共识来源的多种可能解释"],
        },
        "book_profile_draft": {
            dimension: {
                "summary": f"{dimension} 的原创基础设计",
                "core_commitments": ["保持人物选择与代价绑定"],
                "preferences": ["优先服务核心阅读承诺"],
                "open_questions": ["保留可演化空间"],
                "risks": ["避免设定压过人物"],
            }
            for dimension in (
                "worldbuilding",
                "characters",
                "plot",
                "style",
                "narrative",
                "dialogue",
                "pacing",
                "themes",
                "continuity",
            )
        },
        "first_chapter_candidates": [
            {
                "candidate_id": f"chapter-{index}",
                "title": f"首章候选 {index}",
                "opening_situation": f"清晨档案室出现异常空洞 {index}",
                "hook": f"一份不存在的档案留下主角签名 {index}",
                "chapter_goal": "找到情绪空洞的第一条可行动线索",
                "central_choice": "是否隐瞒异常并私下调查",
                "conflict": "同僚要求立即封存异常档案",
                "protagonist_action": "主角主动带走非法档案",
                "cost": "主角失去一段童年记忆",
                "irreversible_change": "主角成为记忆局的内部调查对象",
                "ending_turn": f"主角发现非法档案上有自己的旧签名 {index}",
                "distinctiveness": f"候选 {index} 使用不同空间与关系压力",
                "primary_function": "setup",
            }
            for index in range(1, 4)
        ],
        "open_questions": ["谁设计了删除机制"],
        "hidden_truth_candidates": [
            {
                "candidate_id": "hidden-source",
                "title": "删除源头",
                "statement": "删除机制可能源于城市居民的共同选择",
                "confidence": 0.55,
            }
        ],
        "risks": ["设定解谜压过人物能动性"],
        "avoid_cliches": ["万能幕后组织"],
    }


def create_original(tmp_path: Path) -> tuple[BookLayout, Database]:
    layout = BookLayout(tmp_path / "library")
    created = create_original_book(
        layout,
        {
            "premise": "城市每天删除一种情感",
            "tone_style": "冷峻、克制",
            "pov": "第三人称限知",
            "must_include": ["每次收益必须伴随代价"],
            "forbidden": ["天降外挂"],
        },
        book_id=BOOK_ID,
    )
    return layout, Database(Path(str(created["database"])))


def complete_core_innovation_handoff(database: Database) -> str:
    reader_result = confirm_original_reader_experience(database, BOOK_ID)
    handoff_id = str(reader_result["handoff"]["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    original_request = json.loads(
        (
            Path(str(handoff["task_directory"]))
            / "input"
            / "original_request.json"
        ).read_text(
            encoding="utf-8"
        )
    )
    proposal_data = innovation_payload()
    proposal_data["kernel_contracts"] = original_request["progression_kernel"]
    proposal = CoreInnovationProposal.model_validate(proposal_data)
    artifact = (
        Path(str(handoff["task_directory"]))
        / "artifacts"
        / "core_innovation"
        / "proposal.json"
    )
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json_dumps(proposal.model_dump(mode="json"), indent=2), encoding="utf-8")
    claim = claim_handoff(database, handoff_id, "test-worker")
    token = str(claim["claim_token"])
    update_handoff_status(database, handoff_id, HandoffStatus.RUNNING, claim_token=token)
    frozen = get_handoff(database, handoff_id)
    result = {
        "handoff_id": handoff_id,
        "handoff_type": "ORIGINAL_BOOK_BOOTSTRAP",
        "requested_stage": "CORE_INNOVATION_PROPOSAL",
        "completed_stage": "CORE_INNOVATION_PROPOSED",
        "book_id": BOOK_ID,
        "edition_id": "base",
        "status": "COMPLETED",
        "task_ids": [],
        "candidate_ids": [],
        "innovation_ids": [
            item["innovation_id"] for item in innovation_payload()["innovation_candidates"]
        ],
        "selected_candidate_id": None,
        "contract_id": None,
        "draft_id": None,
        "campaign_id": None,
        "revision_unit_ids": [],
        "artifact_paths": ["artifacts/core_innovation/proposal.json"],
        "validation_summary": {"valid": True, "proposal_only": True},
        "warnings": [],
        "next_action": "作者审阅并确认基础框架",
        "canon_committed": False,
        "edition_activated": False,
        "base_event_seq": int(frozen["base_event_seq"]),
        "base_projection_hash": str(frozen["base_projection_hash"]),
        "metric_run_ids": [],
        "metric_bundle_hash": None,
        "completed_at": "2026-08-11T00:00:00Z",
    }
    updated = update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.COMPLETED,
        claim_token=token,
        result=result,
    )
    assert updated["status"] == "COMPLETED"
    return handoff_id


def complete_foundation_handoff(database: Database) -> str:
    handoff = prepare_original_bootstrap(database, BOOK_ID)
    handoff_id = str(handoff["handoff_id"])
    frozen_handoff = get_handoff(database, handoff_id)
    original_request = json.loads(
        (
            Path(str(frozen_handoff["task_directory"]))
            / "input"
            / "original_request.json"
        ).read_text(encoding="utf-8")
    )
    proposal_data = proposal_payload()
    proposal_data["kernel_contracts"] = original_request["progression_kernel"]
    proposal = OriginalBootstrapProposal.model_validate(proposal_data)
    artifact = (
        Path(str(frozen_handoff["task_directory"]))
        / "artifacts"
        / "story_foundation"
        / "proposal.json"
    )
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json_dumps(proposal.model_dump(mode="json"), indent=2), encoding="utf-8")
    claim = claim_handoff(database, handoff_id, "test-worker")
    token = str(claim["claim_token"])
    update_handoff_status(database, handoff_id, HandoffStatus.RUNNING, claim_token=token)
    frozen = get_handoff(database, handoff_id)
    result = {
        "handoff_id": handoff_id,
        "handoff_type": "ORIGINAL_BOOK_BOOTSTRAP",
        "requested_stage": "STORY_FOUNDATION_PROPOSAL",
        "completed_stage": "FOUNDATION_PROPOSED",
        "book_id": BOOK_ID,
        "edition_id": "base",
        "status": "COMPLETED",
        "task_ids": [],
        "candidate_ids": [
            item["candidate_id"] for item in proposal_payload()["foundation_candidates"]
        ],
        "innovation_ids": [],
        "selected_candidate_id": None,
        "contract_id": None,
        "draft_id": None,
        "campaign_id": None,
        "revision_unit_ids": [],
        "artifact_paths": ["artifacts/story_foundation/proposal.json"],
        "validation_summary": {"valid": True, "proposal_only": True},
        "warnings": [],
        "next_action": "作者审阅并确认故事基础",
        "canon_committed": False,
        "edition_activated": False,
        "base_event_seq": int(frozen["base_event_seq"]),
        "base_projection_hash": str(frozen["base_projection_hash"]),
        "metric_run_ids": [],
        "metric_bundle_hash": None,
        "completed_at": "2026-08-11T00:00:00Z",
    }
    updated = update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.COMPLETED,
        claim_token=token,
        result=result,
    )
    assert updated["status"] == "COMPLETED"
    return handoff_id


def complete_bootstrap_handoff(database: Database) -> str:
    with database.connect() as connection:
        selected = connection.execute(
            "SELECT selected_primary_innovation_id FROM original_states WHERE book_id=?",
            (BOOK_ID,),
        ).fetchone()
    if selected is None or not selected["selected_primary_innovation_id"]:
        innovation_handoff_id = complete_core_innovation_handoff(database)
        import_original_core_innovation_proposal(database, BOOK_ID, innovation_handoff_id)
        selection = select_original_core_innovation(
            database,
            BOOK_ID,
            {
                "selected_primary_innovation_id": "innovation-1",
                "optional_mix_notes": "吸收机制 2 的一个选择特征",
            },
        )
        assert selection["handoff"]["status"]["status"] == "READY_FOR_CODEX"
    return complete_foundation_handoff(database)


def accept_foundation(database: Database) -> dict[str, Any]:
    handoff_id = complete_bootstrap_handoff(database)
    import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)
    proposal = proposal_payload()
    return confirm_original_foundation(
        database,
        BOOK_ID,
        {
            "confirmed": True,
            "selected_title": "无情之城",
            "selected_foundation_id": "foundation-1",
            "selected_route_id": "route-2",
            "world_rules": proposal["world_rules"],
            "first_phase_objective": proposal["first_phase_objective"],
        },
    )


def test_original_book_requires_no_source_and_has_one_author_card(tmp_path: Path) -> None:
    layout, database = create_original(tmp_path)
    record = BookRegistry(layout).record(BOOK_ID)
    with database.connect() as connection:
        counts = connection.execute(
            "SELECT (SELECT COUNT(*) FROM source_documents), "
            "(SELECT COUNT(*) FROM chapters), (SELECT COUNT(*) FROM editions)"
        ).fetchone()
        handoff_count = connection.execute(
            "SELECT COUNT(*) FROM workflow_handoffs"
        ).fetchone()[0]
    catalog = build_library_catalog(layout, tmp_path / "book")

    assert record.book_kind is BookKind.AUTHOR
    assert record.creation_mode is CreationMode.ORIGINAL
    assert tuple(counts) == (0, 0, 1)
    assert handoff_count == 0
    assert record.original_state == "READER_EXPERIENCE_REVIEW"
    assert len(catalog.entries) == 1
    assert catalog.entries[0].href == f"/books/{BOOK_ID}/original"
    assert studio_access(layout, record).access_level.value == "ONBOARDING"


def test_core_innovation_precedes_foundation_and_freezes_author_intent(tmp_path: Path) -> None:
    assert set(CoreInnovationCandidate.model_fields) == {
        "innovation_id",
        "title",
        "one_sentence_hook",
        "core_mechanism",
        "protagonist_special_rule",
        "choice_generation",
        "progression_generation",
        "payoff_generation",
        "limitation",
        "expansion_grammar",
        "long_form_capacity",
        "novelty_source",
        "repetition_risk",
        "fit_with_reader_promise",
    }
    _, database = create_original(tmp_path)
    with pytest.raises(OriginalWorkflowError, match="Core Innovation"):
        prepare_original_bootstrap(database, BOOK_ID)

    core_handoff_id = complete_core_innovation_handoff(database)
    core_imported = import_original_core_innovation_proposal(
        database, BOOK_ID, core_handoff_id
    )
    assert core_imported["canon_changed"] is False
    overview = original_overview(database, BOOK_ID)
    assert overview["original_state"] == "CORE_INNOVATION_REVIEW"
    assert overview["innovation_proposal"] is not None
    candidates = overview["innovation_proposal"]["innovation_candidates"]
    assert len(candidates) == 3
    assert len({item["innovation_id"] for item in candidates}) == 3
    assert all(item["core_mechanism"] for item in candidates)

    selected = select_original_core_innovation(
        database,
        BOOK_ID,
        {
            "selected_primary_innovation_id": candidates[0]["innovation_id"],
            "optional_mix_notes": "吸收机制 2 的一个选择特征",
        },
    )
    assert selected["canon_changed"] is False
    assert selected["innovation_intent"]["selected_primary_innovation_id"] == candidates[0][
        "innovation_id"
    ]
    with pytest.raises(OriginalWorkflowError, match="已冻结"):
        select_original_core_innovation(
            database,
            BOOK_ID,
            {
                "selected_primary_innovation_id": candidates[1]["innovation_id"],
                "optional_mix_notes": "尝试替换已选机制",
            },
        )
    foundation_handoff = get_handoff(database, str(selected["handoff"]["handoff_id"]))
    assert foundation_handoff["requested_stage"] == "STORY_FOUNDATION_PROPOSAL"
    foundation_request = json.loads(
        (Path(str(foundation_handoff["task_directory"])) / "input" / "original_request.json")
        .read_text(encoding="utf-8")
    )
    assert foundation_request["progression_kernel"]["foundation_rules"] == [
        "故事基础候选必须共享已确认的 Reader Experience 与 Primary Narrative Drive",
        "故事基础候选必须在同一核心创意下提供不同的故事承载方式",
        "不得把市场分类、setting skin 或社会议题替换成新的核心机制",
    ]
    assert (
        foundation_request["progression_kernel"]["core_innovation"][
            "selected_primary_innovation_id"
        ]
        == candidates[0]["innovation_id"]
    )
    with database.connect() as connection:
        state = connection.execute(
            "SELECT selected_primary_innovation_id, optional_mix_notes, state "
            "FROM original_states WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
    assert state["selected_primary_innovation_id"] == candidates[0]["innovation_id"]
    assert state["optional_mix_notes"] == "吸收机制 2 的一个选择特征"
    assert state["state"] == "FOUNDATION_GENERATING"

    foundation_handoff_id = complete_foundation_handoff(database)
    foundation_imported = import_original_bootstrap_proposal(
        database, BOOK_ID, foundation_handoff_id
    )
    assert foundation_imported["proposal"]["core_innovation_intent"] == selected[
        "innovation_intent"
    ]
    with database.connect() as connection:
        counts = connection.execute(
            "SELECT (SELECT COUNT(*) FROM chapters), "
            "(SELECT COUNT(*) FROM canon_commits)"
        ).fetchone()
    assert tuple(counts) == (0, 0)


def test_original_foundation_stales_when_selected_author_intent_changes(
    tmp_path: Path,
) -> None:
    _, database = create_original(tmp_path)
    core_handoff_id = complete_core_innovation_handoff(database)
    import_original_core_innovation_proposal(database, BOOK_ID, core_handoff_id)
    selected = select_original_core_innovation(
        database,
        BOOK_ID,
        {
            "selected_primary_innovation_id": "innovation-1",
            "optional_mix_notes": "原始混合说明",
        },
    )
    foundation_handoff_id = str(selected["handoff"]["handoff_id"])
    with database.connect() as connection:
        connection.execute(
            "UPDATE original_states SET optional_mix_notes=? "
            "WHERE book_id=? AND edition_id='base'",
            ("冻结后被修改", BOOK_ID),
        )

    with pytest.raises(HandoffWorkflowError, match="original author intent changed"):
        start_handoff(database, foundation_handoff_id)
    assert get_handoff(database, foundation_handoff_id)["status"] == "STALE"


def test_original_bootstrap_fast_path_freezes_one_skill_and_thin_inputs(tmp_path: Path) -> None:
    _, database = create_original(tmp_path)
    confirmed = confirm_original_reader_experience(database, BOOK_ID)
    handoff_id = str(confirmed["handoff"]["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads(
        (task_directory / "input" / "task.json").read_text(encoding="utf-8")
    )

    assert task["executor_skill"] == "bootstrap-original-novel"
    assert task["business_input_files"] == [
        "original_request.json",
        "proposal_schema.json",
    ]
    assert all(
        (task_directory / "input" / name).is_file()
        for name in task["business_input_files"]
    )
    manifest = json.loads(
        (task_directory / "input" / "context_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["executor_skill"] == task["executor_skill"]
    assert manifest["business_input_files"] == task["business_input_files"]
    assert "metric_context.json" not in task["business_input_files"]
    assert "planning_aggregate" not in json.dumps(task["business_input_files"])
    assert task["current_atlas_id"] is None
    assert task["registry_hash"] == ""
    assert task["config_hash"] == ""
    output_schema = json.loads(
        (task_directory / "input" / "output_schema.json").read_text(encoding="utf-8")
    )
    assert "draft_id" not in output_schema["required"]
    assert "campaign_id" not in output_schema["required"]
    assert "metric_run_ids" not in output_schema["required"]
    prompt = (task_directory / "input" / "prompt.md").read_text(encoding="utf-8")
    assert prompt.startswith("$process-novel-handoff")
    assert prompt.count("process-novel-handoff") == 1
    assert "workflow start" in prompt
    assert "workflow complete" in prompt

    started = start_handoff(database, handoff_id)
    assert started["status"] == HandoffStatus.RUNNING.value
    assert started["executor_skill"] == "bootstrap-original-novel"
    assert started["business_input_files"] == task["business_input_files"]

    proposal = CoreInnovationProposal.model_validate(innovation_payload())
    artifact = task_directory / "artifacts" / "core_innovation" / "proposal.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json_dumps(proposal.model_dump(mode="json")), encoding="utf-8")
    frozen = get_handoff(database, handoff_id)
    result_path = Path(str(started["result_target"]))
    result = {
        "handoff_id": handoff_id,
        "handoff_type": "ORIGINAL_BOOK_BOOTSTRAP",
        "requested_stage": "CORE_INNOVATION_PROPOSAL",
        "completed_stage": "CORE_INNOVATION_PROPOSED",
        "book_id": BOOK_ID,
        "edition_id": "base",
        "status": "COMPLETED",
        "task_ids": [],
        "candidate_ids": [],
        "innovation_ids": [
            item["innovation_id"] for item in innovation_payload()["innovation_candidates"]
        ],
        "selected_candidate_id": None,
        "contract_id": None,
        "draft_id": None,
        "campaign_id": None,
        "revision_unit_ids": [],
        "artifact_paths": ["artifacts/core_innovation/proposal.json"],
        "validation_summary": {"valid": True, "proposal_only": True},
        "warnings": [],
        "next_action": "作者审阅并确认核心创意",
        "canon_committed": False,
        "edition_activated": False,
        "base_event_seq": int(frozen["base_event_seq"]),
        "base_projection_hash": str(frozen["base_projection_hash"]),
        "metric_run_ids": [],
        "metric_bundle_hash": None,
        "completed_at": "2026-08-12T00:00:00Z",
    }
    result_path.write_text(json_dumps(result), encoding="utf-8")
    completed = complete_handoff(database, handoff_id, str(started["claim_token"]), result_path)
    assert completed["status"] == HandoffStatus.COMPLETED.value
    assert get_handoff(database, handoff_id)["status"] == HandoffStatus.COMPLETED.value


def test_core_innovation_import_rejects_frozen_kernel_drift(tmp_path: Path) -> None:
    _, database = create_original(tmp_path)
    handoff_id = complete_core_innovation_handoff(database)
    handoff = get_handoff(database, handoff_id)
    artifact = (
        Path(str(handoff["task_directory"]))
        / "artifacts"
        / "core_innovation"
        / "proposal.json"
    )
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    payload["kernel_contracts"] = {"drifted": True}
    artifact.write_text(json_dumps(payload, indent=2), encoding="utf-8")

    with pytest.raises(OriginalWorkflowError, match="不得修改"):
        import_original_core_innovation_proposal(database, BOOK_ID, handoff_id)
    with database.connect() as connection:
        status = connection.execute(
            "SELECT status FROM original_innovation_versions "
            "WHERE book_id=? AND handoff_id=?",
            (BOOK_ID, handoff_id),
        ).fetchone()[0]
    assert status == "GENERATING"


def test_foundation_import_rejects_replacing_selected_innovation(tmp_path: Path) -> None:
    _, database = create_original(tmp_path)
    core_handoff_id = complete_core_innovation_handoff(database)
    import_original_core_innovation_proposal(database, BOOK_ID, core_handoff_id)
    select_original_core_innovation(
        database,
        BOOK_ID,
        {
            "selected_primary_innovation_id": "innovation-1",
            "optional_mix_notes": "",
        },
    )
    foundation_handoff_id = complete_foundation_handoff(database)
    handoff = get_handoff(database, foundation_handoff_id)
    artifact = (
        Path(str(handoff["task_directory"]))
        / "artifacts"
        / "story_foundation"
        / "proposal.json"
    )
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    payload["core_innovation_intent"]["selected_primary_innovation_id"] = "innovation-2"
    artifact.write_text(json_dumps(payload, indent=2), encoding="utf-8")

    with pytest.raises(OriginalWorkflowError, match="Core Innovation"):
        import_original_bootstrap_proposal(database, BOOK_ID, foundation_handoff_id)


def test_foundation_stays_proposal_until_author_confirms_impact(tmp_path: Path) -> None:
    layout, database = create_original(tmp_path)
    handoff_id = complete_bootstrap_handoff(database)
    imported = import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)
    assert imported["canon_changed"] is False
    with database.connect() as connection:
        before = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM author_truths), "
                "(SELECT COUNT(*) FROM chapters), (SELECT COUNT(*) FROM canon_commits)"
            ).fetchone()
        )
    with pytest.raises(OriginalWorkflowError, match="确认"):
        confirm_original_foundation(
            database,
            BOOK_ID,
            {
                "confirmed": False,
                "selected_title": "无情之城",
                "selected_foundation_id": "foundation-1",
                "selected_route_id": "route-2",
                "world_rules": proposal_payload()["world_rules"],
                "first_phase_objective": proposal_payload()["first_phase_objective"],
            },
        )
    result = confirm_original_foundation(
        database,
        BOOK_ID,
        {
            "confirmed": True,
            "selected_title": "无情之城",
            "title_override": "情绪失物招领处",
            "selected_foundation_id": "foundation-1",
            "selected_route_id": "route-2",
            "protagonist_goal_override": "先找回被删除的悲伤",
            "world_rules": proposal_payload()["world_rules"],
            "first_phase_objective": proposal_payload()["first_phase_objective"],
            "rolling_short_override": ["定位第一位情绪保留者"],
            "characters_override": ["林默：主动追索被删情感的人"],
            "factions_override": ["情绪保留者联盟"],
        },
    )
    with database.connect() as connection:
        after = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM author_truths), "
                "(SELECT COUNT(*) FROM chapters), (SELECT COUNT(*) FROM canon_commits)"
            ).fetchone()
        )
        intents = connection.execute(
            "SELECT horizon FROM author_control_intents ORDER BY horizon"
        ).fetchall()
        foundation_truths = [
            str(row[0])
            for row in connection.execute(
                "SELECT statement FROM author_truths ORDER BY truth_id"
            ).fetchall()
        ]

    assert before == (0, 0, 0)
    assert after[0] >= 6
    assert after[1:] == (0, 0)
    assert {row["horizon"] for row in intents} == {"SHORT", "MID", "LONG"}
    assert "林默：主动追索被删情感的人" in foundation_truths
    assert "情绪保留者联盟" in foundation_truths
    accepted = Path(str(result["accepted_path"])).read_text(encoding="utf-8")
    accepted_payload = json.loads(accepted)
    assert accepted_payload["apply_plan"]["core_innovation_intent"][
        "selected_primary_innovation_id"
    ] == "innovation-1"
    assert set(accepted_payload["apply_plan"]["growth_grammar"]) == {
        "progression",
        "expansion",
        "payoff",
    }
    assert accepted_payload["apply_plan"]["first_phase"]["first_concrete_goal"] == (
        "阻止下一次删除并找到第一位保留者"
    )
    assert "情绪失物招领处" in accepted
    assert "先找回被删除的悲伤" in accepted
    retry = confirm_original_foundation(
        database,
        BOOK_ID,
        {
            "confirmed": True,
            "selected_title": "无情之城",
            "title_override": "情绪失物招领处",
            "selected_foundation_id": "foundation-1",
            "selected_route_id": "route-2",
            "protagonist_goal_override": "先找回被删除的悲伤",
            "world_rules": proposal_payload()["world_rules"],
            "first_phase_objective": proposal_payload()["first_phase_objective"],
            "rolling_short_override": ["定位第一位情绪保留者"],
            "characters_override": ["林默：主动追索被删情感的人"],
            "factions_override": ["情绪保留者联盟"],
        },
    )
    assert retry["idempotent"] is True
    assert retry["apply_id"] == result["apply_id"]
    with pytest.raises(OriginalWorkflowError, match="不能再次覆盖"):
        confirm_original_foundation(
            database,
            BOOK_ID,
            {
                "confirmed": True,
                "selected_title": "无情之城",
                "selected_foundation_id": "foundation-1",
                "selected_route_id": "route-2",
                "world_rules": proposal_payload()["world_rules"],
                "first_phase_objective": proposal_payload()["first_phase_objective"],
            },
        )
    assert len(result["genesis"]["candidates"]) == 3
    assert {
        candidate["score_status"] for candidate in result["genesis"]["candidates"]
    } == {"NOT_COMPUTED"}
    assert studio_access(layout, BookRegistry(layout).record(BOOK_ID)).accessible


def test_completed_bootstrap_reconciles_on_status_check_without_new_handoff(
    tmp_path: Path,
) -> None:
    layout, database = create_original(tmp_path)
    handoff_id = complete_bootstrap_handoff(database)
    with database.connect() as connection:
        before_handoffs = connection.execute(
            "SELECT COUNT(*) FROM workflow_handoffs "
            "WHERE book_id=? AND handoff_type=? AND requested_stage=?",
            (BOOK_ID, "ORIGINAL_BOOK_BOOTSTRAP", "STORY_FOUNDATION_PROPOSAL"),
        ).fetchone()[0]
        before_version = connection.execute(
            "SELECT status FROM original_proposal_versions WHERE book_id=? AND handoff_id=?",
            (BOOK_ID, handoff_id),
        ).fetchone()[0]
    assert before_handoffs == 1
    assert before_version == "GENERATING"

    checked = prepare_original_bootstrap(database, BOOK_ID)
    assert checked["deduplicated"] is True
    assert checked["proposal_imported"] is True
    assert checked["handoff_id"] == handoff_id
    assert checked["proposal_status"] == "CURRENT"

    # A second import is a no-op and cannot downgrade CURRENT to READY.
    repeated = import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)
    assert repeated["proposal_status"] == "CURRENT"
    overview = original_overview(database, BOOK_ID)
    assert overview["original_state"] == "FOUNDATION_REVIEW"
    assert overview["proposal"] is not None
    assert overview["generating_proposal"] is None

    app = create_app(
        database,
        library_root=layout.library_root,
        discovery_root=tmp_path / "book",
    )
    with TestClient(app) as client:
        page = client.get(f"/books/{BOOK_ID}/original")
    assert page.status_code == 200
    assert "等待你确认故事方案" in page.text
    assert "正在生成故事方案" not in page.text
    with database.connect() as connection:
        after_handoffs = connection.execute(
            "SELECT COUNT(*) FROM workflow_handoffs "
            "WHERE book_id=? AND handoff_type=? AND requested_stage=?",
            (BOOK_ID, "ORIGINAL_BOOK_BOOTSTRAP", "STORY_FOUNDATION_PROPOSAL"),
        ).fetchone()[0]
        after_version = connection.execute(
            "SELECT status FROM original_proposal_versions WHERE book_id=? AND handoff_id=?",
            (BOOK_ID, handoff_id),
        ).fetchone()[0]
    assert after_handoffs == before_handoffs
    assert after_version == "CURRENT"


def test_web_read_reconciles_completed_bootstrap_without_manual_import(tmp_path: Path) -> None:
    layout, database = create_original(tmp_path)
    handoff_id = complete_bootstrap_handoff(database)
    app = create_app(
        database,
        library_root=layout.library_root,
        discovery_root=tmp_path / "book",
    )

    with TestClient(app) as client:
        page = client.get(f"/books/{BOOK_ID}/original")

    assert page.status_code == 200
    assert "等待你确认故事方案" in page.text
    assert "正在生成故事方案" not in page.text
    with database.connect() as connection:
        handoff_count = connection.execute(
            "SELECT COUNT(*) FROM workflow_handoffs "
            "WHERE book_id=? AND handoff_type=? AND requested_stage=?",
            (BOOK_ID, "ORIGINAL_BOOK_BOOTSTRAP", "STORY_FOUNDATION_PROPOSAL"),
        ).fetchone()[0]
        version_status = connection.execute(
            "SELECT status FROM original_proposal_versions WHERE book_id=? AND handoff_id=?",
            (BOOK_ID, handoff_id),
        ).fetchone()[0]
    assert handoff_count == 1
    assert version_status == "CURRENT"


def test_foundation_transaction_rolls_back_all_partial_writes(tmp_path: Path) -> None:
    _, database = create_original(tmp_path)
    handoff_id = complete_bootstrap_handoff(database)
    imported = import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)
    proposal_version_id = str(imported["proposal_version_id"])
    collision_id = f"directive-{proposal_version_id}-foundation-1-must-1"
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO author_directives("
            "directive_id, book_id, edition_id, directive_type, content, mode, status, "
            "priority, source, created_at, version"
            ") VALUES (?, ?, 'base', 'requirement', '预置冲突', 'persistent', 'ACTIVE', "
            "100, 'TEST', 'now', 1)",
            (collision_id, BOOK_ID),
        )

    with pytest.raises(OriginalWorkflowError):
        confirm_original_foundation(
            database,
            BOOK_ID,
            {
                "confirmed": True,
                "selected_title": "无情之城",
                "selected_foundation_id": "foundation-1",
                "selected_route_id": "route-2",
                "world_rules": proposal_payload()["world_rules"],
                "first_phase_objective": proposal_payload()["first_phase_objective"],
            },
        )
    with database.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM author_truths").fetchone()[0] == 0
        assert (
            connection.execute("SELECT COUNT(*) FROM original_genesis_applies").fetchone()[0] == 0
        )
        state = connection.execute(
            "SELECT state, accepted_apply_id FROM original_states WHERE book_id=?",
            (BOOK_ID,),
        ).fetchone()
    assert tuple(state) == ("FOUNDATION_REVIEW", None)


def test_regenerated_proposal_is_versioned_and_does_not_replace_accepted_foundation(
    tmp_path: Path,
) -> None:
    _, database = create_original(tmp_path)
    accepted = accept_foundation(database)
    first_apply_id = str(accepted["apply_id"])
    first = prepare_original_bootstrap(database, BOOK_ID)
    duplicate = prepare_original_bootstrap(database, BOOK_ID)
    assert duplicate["deduplicated"] is True
    assert duplicate["handoff_id"] == first["handoff_id"]

    regenerated_handoff = complete_bootstrap_handoff(database)
    assert regenerated_handoff == first["handoff_id"]
    imported = import_original_bootstrap_proposal(database, BOOK_ID, regenerated_handoff)
    assert imported["proposal_status"] == "READY"
    comparison = compare_original_proposals(database, BOOK_ID, str(imported["proposal_version_id"]))
    assert comparison["current_version_id"] != comparison["target_version_id"]

    replaced = resolve_original_proposal_version(
        database,
        BOOK_ID,
        str(imported["proposal_version_id"]),
        action="REPLACE_CURRENT",
    )
    assert replaced["current_changed"] is True
    assert replaced["accepted_foundation_changed"] is False
    with database.connect() as connection:
        state = connection.execute(
            "SELECT state, accepted_apply_id FROM original_states WHERE book_id=?",
            (BOOK_ID,),
        ).fetchone()
        canon_count = connection.execute("SELECT COUNT(*) FROM canon_commits").fetchone()[0]
    assert tuple(state) == ("FOUNDATION_READY", first_apply_id)
    assert canon_count == 0


def test_first_chapter_uses_contract_validation_and_explicit_approval(tmp_path: Path) -> None:
    _, database = create_original(tmp_path)
    foundation = accept_foundation(database)
    selected = select_first_chapter_candidate(
        database, BOOK_ID, foundation["genesis"]["candidates"][0]["candidate_id"]
    )
    contract = ChapterContract.model_validate_json(
        Path(str(selected["contract"]["path"])).read_text(encoding="utf-8")
    )
    settings = load_settings()
    prose = "\n".join(
        [
            contract.required_irreversible_change,
            contract.required_cost,
            contract.ending_state,
            "线程状态完成更新，林默决定继续追查情绪空洞。",
            "人物状态完成更新，他主动带走了非法档案。",
        ]
    )
    draft_output = DraftOutput.model_validate(
        {
            "task_id": selected["draft_task"]["task_id"],
            "contract_id": contract.contract_id,
            "chapter_title": "被删除的清晨",
            "prose_markdown": prose,
            "state_changes": [
                {
                    "kind": "thread",
                    "record_id": contract.primary_thread,
                    "payload": {
                        "goal": "找回被删除的情感",
                        "stakes": "继续删除将令城市失去选择能力",
                        "phase": "advanced",
                        "importance": 1.0,
                        "reader_visibility": 1.0,
                        "progress": 0.2,
                    },
                    "evidence_quotes": ["线程状态完成更新"],
                },
                {
                    "kind": "character_state",
                    "record_id": "state-protagonist-genesis",
                    "payload": {
                        "character_id": "protagonist",
                        "goals": ["追查情绪空洞"],
                        "plans": ["带走非法档案"],
                    },
                    "evidence_quotes": ["人物状态完成更新"],
                },
            ],
            "contract_evidence": {
                "required_irreversible_change": [contract.required_irreversible_change],
                "required_cost": [contract.required_cost],
                "ending_state": [contract.ending_state],
                f"commit:thread_status:{contract.primary_thread}": ["线程状态完成更新"],
                "commit:character_state:protagonist": ["人物状态完成更新"],
            },
            "knowledge_claims": [],
            "reveal_trace": {
                "planned": [
                    {
                        "truth_id": item["truth_id"],
                        "agenda_bucket": item["agenda_bucket"],
                        "depth": item.get("reveal_depth"),
                    }
                    for key in ("must_reveal", "should_hint", "keep_hidden")
                    for item in contract.reveal_agenda.get(key, [])
                ],
                "realized": [],
                "knowledge_transitions": [],
            },
            "character_fit_inputs": dict.fromkeys(settings.metrics["character_fit"]["weights"], 90),
            "style_fit_inputs": dict.fromkeys(settings.metrics["style_fit"]["weights"], 90),
            "promises_advanced": [contract.primary_thread],
            "structure_tags": ["original-genesis-active-choice"],
            "notes": ["固定本地测试输出，不调用远程模型"],
        }
    )
    output_path = Path(str(selected["draft_task"]["expected_output"]))
    output_path.write_text(
        json_dumps(draft_output.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    imported = import_draft_output(database, BOOK_ID, str(selected["draft_task"]["task_id"]))
    draft_id = str(imported["draft_id"])
    validation = validate_original_draft(database, BOOK_ID, draft_id)
    assert validation["passed"] is True, validation
    with pytest.raises(RuntimeError, match="必须逐字"):
        approve_original_first_chapter(database, BOOK_ID, draft_id, "同意")
    approved = approve_original_first_chapter(database, BOOK_ID, draft_id, "批准写入正史")
    next_handoff = create_continuation_handoff(
        database,
        BOOK_ID,
        edition_id="base",
        requested_stage="PLAN_ONLY",
    )
    with sqlite3.connect(database.path) as connection:
        chapters = connection.execute(
            "SELECT ordinal, title FROM chapters WHERE book_id=?", (BOOK_ID,)
        ).fetchall()
        commits = connection.execute(
            "SELECT COUNT(*) FROM canon_commits WHERE book_id=?", (BOOK_ID,)
        ).fetchone()[0]

    assert approved["chapter"] == 1
    assert approved["status"] == "CANON_COMMITTED"
    assert chapters == [(1, "被删除的清晨")]
    assert commits == 1
    assert next_handoff["status"]["status"] == "READY_FOR_CODEX"


def test_original_web_entry_and_premise_form(tmp_path: Path) -> None:
    library_root = tmp_path / "library"
    database = Database(tmp_path / "fallback.sqlite3")
    database.initialize()
    app = create_app(
        database,
        library_root=library_root,
        discovery_root=tmp_path / "book",
    )
    with TestClient(app) as client:
        library = client.get("/library")
        form = client.get("/library/original/new")
        token = form.text.split('name="csrf-token" content="', 1)[1].split('"', 1)[0]
        created = client.post(
            "/api/library/original",
            headers={"X-CSRF-Token": token},
            json={"premise": "一座城市每天删除一种情感"},
        )
        created_payload = created.json()
        book_id = str(created_payload["book_id"])
        reader_step = client.get(created.json()["original_url"])
        confirmed = client.post(
            f"/api/books/{book_id}/original/reader-experience/confirm",
            headers={"X-CSRF-Token": token},
            json={"adjustment": "CONFIRM"},
        )
        original = client.get(created.json()["original_url"])
        handoff_id = str(confirmed.json()["handoff"]["handoff_id"])
        instruction_url = (
            f"/api/books/{book_id}/editions/base/handoffs/{handoff_id}/instruction"
        )
        instruction = client.get(instruction_url)

    assert library.status_code == 200
    assert "导入小说" in library.text
    assert "新建原创小说" in library.text
    assert "一句话创意" in form.text
    assert created.status_code == 200
    assert created.json()["source_required"] is False
    assert "阅读体验与主要驱动力" in reader_step.text
    assert "长期推进" in reader_step.text
    assert "AI 任务" in original.text
    assert instruction.status_code == 200
    assert instruction.json()["instruction"]
    assert f'data-copy-instruction="{instruction_url}"' in original.text
    assert f'href="/api/handoffs/{handoff_id}/instruction"' not in original.text


def test_reader_experience_strengths_are_editable_persisted_and_used_by_drive_proposal(
    tmp_path: Path,
) -> None:
    layout, database = create_original(tmp_path)
    app = create_app(
        Database(tmp_path / "fallback.sqlite3"),
        library_root=layout.library_root,
        discovery_root=tmp_path / "book",
    )
    with TestClient(app) as client:
        before = client.get(f"/books/{BOOK_ID}/original")
        assert before.status_code == 200
        assert before.text.count("标准") >= 12
        assert 'data-reader-strength="CORE"' in before.text
        for preset in (
            "PAYOFF_STRONGER",
            "MYSTERY_STRONGER",
            "TEAM_STRONGER",
            "RELATIONSHIP_STRONGER",
            "CAREER_STRONGER",
        ):
            assert f'data-reader-preset="{preset}"' in before.text

        confirmed = client.post(
            f"/api/books/{BOOK_ID}/original/reader-experience/confirm",
            headers={"X-CSRF-Token": client.app.state.csrf_token},
            json={
                "adjustment": "CONFIRM",
                "priority_overrides": {
                    "RESOURCE_OPPORTUNITY": "CORE",
                    "PROGRESSION": "SECONDARY",
                    "POWER_VERIFICATION": "STRONG",
                    "MYSTERY": "STRONG",
                },
            },
        )
        assert confirmed.status_code == 200, confirmed.text
        reader = confirmed.json()["reader_experience"]["payload"]
        priorities = reader["experience_priorities"]
        assert priorities["RESOURCE_OPPORTUNITY"] == "VERY_HIGH"
        assert priorities["PROGRESSION"] == "LOW"
        assert priorities["POWER_VERIFICATION"] == "HIGH"
        assert reader["primary_narrative_drive"] == "RESOURCE_OPPORTUNITY"
        drive = next(
            item["payload"]
            for item in confirmed.json()["created_contract_proposals"]
            if item["contract_type"] == "NARRATIVE_DRIVE"
        )
        assert drive["primary_drive"] == "RESOURCE_OPPORTUNITY"
        assert "MYSTERY_INVESTIGATION" in drive["secondary_drives"]

        after = client.get(f"/books/{BOOK_ID}/original")
        assert after.status_code == 200
        assert 'data-reader-experience-confirmed' in after.text
        assert "资源机会" in after.text
        assert "已确认 · 阅读体验" in after.text
        assert "后续推理不得静默覆盖作者确认值" in after.text

    # The same effective contract is still the persisted source for the next read.
    overview = original_overview(database, BOOK_ID)
    display = overview["reader_experience_display"]
    displayed = {item["key"]: item["value_label"] for item in display["priorities"]}
    assert displayed["RESOURCE_OPPORTUNITY"] == "核心"
    assert displayed["PROGRESSION"] == "次要"
    assert displayed["POWER_VERIFICATION"] == "强化"
