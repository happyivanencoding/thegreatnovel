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
from novel_authoring.original import service as original_service
from novel_authoring.original.models import (
    CoreInnovationCandidate,
    CoreInnovationProposal,
    FoundationDevelopmentProposal,
    OriginalCreativeSemantics,
    OriginalReaderKernelProposal,
    StoryFoundationProposal,
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
    import_original_foundation_development,
    import_original_reader_kernel_proposal,
    original_overview,
    prepare_original_bootstrap,
    prepare_original_reader_experience,
    resolve_original_proposal_version,
    select_first_chapter_candidate,
    select_original_core_innovation,
    select_original_foundation,
    validate_original_draft,
)
from novel_authoring.planning.models import ChapterContract
from novel_authoring.progression.context import build_kernel_planning_context
from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.models import (
    ContractStatus,
    ReaderExperience,
)
from novel_authoring.progression.service import (
    ProgressionContractType,
    list_contract_records,
)
from novel_authoring.serial_kernel.models import NarrativeDrive
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


def creative_semantics_payload(
    *, existing_signature_mechanism: str = "每日一次、不可撤销的受限行动机会"
) -> dict[str, Any]:
    return {
        "signature_fantasy": "普通人在压力中把有限机会变成不断扩大的主动权",
        "existing_signature_mechanism": existing_signature_mechanism,
        "open_design_space": ["如何让每次选择保持新鲜", "既有成果如何组合并持续回收"],
        "payoff_texture": ["具体选择带来的反差", "旧成果在新压力中的回收"],
        "novelty_focus": ["有限机会产生的不同用途与组合"],
        "realism_anchors": ["人物的资源判断与行动后果保持直观"],
        "complexity_boundaries": ["不增加与既有机制竞争的第二套异常系统"],
        "repeatable_reader_loop": ["压力出现", "选择有限机会", "立即兑现", "打开新局势"],
        "anti_drift": ["把故事改写成调查另一套独立世界规则"],
    }


def innovation_payload() -> dict[str, Any]:
    return {
        "schema_version": "core-innovation-v2",
        "information_status": "PROPOSAL",
        "innovation_candidates": [
            {
                "innovation_id": f"innovation-{index}",
                "title": f"核心机制 {index}",
                "plain_language_pitch": f"保留每日受限机会，并用方案 {index} 让选择持续变化。",
                "concrete_example": (
                    f"主角在一次压力中选择用途 {index}；"
                    "这不是故事基础、Canon 或必然事件。"
                ),
                "reader_anticipation": f"读者会期待下一次有限机会如何与旧成果组合 {index}。",
                "unresolved_design_choices": [
                    f"有限机会怎样产生不同选择 {index}",
                    f"已有成果怎样在后续压力中回收 {index}",
                ],
                "core_mechanism": f"保留每日一次、不可撤销的受限行动机会；变化来自方案 {index}",
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


def proposal_payload(*, progression_enabled: bool = True) -> dict[str, Any]:
    bundle = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "仅用于结构化合同测试的开放 premise。",
            genre_hint="肉身进化",
            contract_prefix=BOOK_ID,
        )
    )
    assert bundle.progression is not None
    progression = (
        bundle.progression.model_copy(
            update={"progression_contract_id": f"{BOOK_ID}-progression"}
        ).model_dump(mode="json")
        if progression_enabled
        else None
    )
    return {
        "schema_version": "foundation-development-v1",
        "information_status": "PROPOSAL",
        "core_innovation_intent": {
            "selected_primary_innovation_id": "innovation-1",
            "optional_mix_notes": "吸收机制 2 的一个选择特征",
        },
        "title_candidates": ["无情之城", "昨日情绪档案", "被删除的悲伤"],
        "expanded_premise": "城市每天删除一种情感，失忆档案员决定找回它们。",
        "selected_foundation_id": "foundation-1",
        "selected_foundation": {
                "candidate_id": "foundation-1",
                "title": "基础框架 1",
                "core_reading_promise": "让每次找回情感都迫使主角承担选择 1",
                "protagonist": "林默",
                "protagonist_competence": "能够识别情绪空洞",
                "protagonist_weakness": "私人记忆会被机制侵蚀",
                "protagonist_goal": "找回被删除的情感",
                "main_conflict": "城市记忆局以秩序之名阻止调查 1",
                "world_carrier": "情绪被删除后留下可追踪的物理空洞",
                "first_stage_objective": "阻止下一次删除",
                "risk_structure": "每次调查都会损失私人记忆",
                "social_configuration": "档案员、保留者与记忆局形成三方压力",
                "resource_structure": "调查时间、可信证人与可用记忆均有限",
                "premise_relationship": "直接展开 premise，不预设幕后答案",
                "author_facing_pitch": "主角在压力中承担代价明确的选择。",
                "opening_situation": "档案室出现异常空洞，主角决定是否介入。",
                "typical_choice": "在安全与测试核心机制之间不可逆选择。",
                "innovation_fit": "让核心机制直接改变人物行动，不新增第二核心。",
            },
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
        "progression_grammar": ["压力出现后选择有限机会，并由结果获得新的行动能力"],
        "expansion_grammar": ["兑现当前结果后打开新局势，不预设固定层数"],
        "payoff_grammar": ["立即兑现当前结果，再暴露更高瓶颈与组合可能"],
        "first_phase": {
            "selected_foundation_id": "foundation-1",
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
        "kernel_contract_proposals": {
            "genre": bundle.genre.model_copy(
                update={
                    "genre_contract_id": f"{BOOK_ID}-genre",
                    "reader_experience_contract_id": f"{BOOK_ID}-reader-experience",
                }
            ).model_dump(mode="json"),
            "progression": progression,
            "world_expansion": bundle.world_expansion.model_copy(
                update={"ladder_id": f"{BOOK_ID}-world-expansion"}
            ).model_dump(mode="json"),
            "payoff_channel": bundle.payoff_channels.model_dump(mode="json"),
        },
    }


def foundation_payload() -> dict[str, Any]:
    development = proposal_payload()
    candidates = []
    for index in range(1, 4):
        item = dict(development["selected_foundation"])
        if index > 1:
            item.update(
                {
                    "candidate_id": f"foundation-{index}",
                    "title": f"基础框架 {index}",
                    "core_reading_promise": f"让选择承担不同压力 {index}",
                    "main_conflict": f"冲突表现 {index}",
                    "world_carrier": f"世界承载 {index}",
                    "first_stage_objective": f"第一阶段目标 {index}",
                    "risk_structure": f"压力结构 {index}",
                    "social_configuration": f"关系进入方式 {index}",
                    "resource_structure": f"资源循环 {index}",
                    "author_facing_pitch": f"主角会反复进行具体故事活动 {index}。",
                    "opening_situation": f"开局压力 {index}",
                    "typical_choice": f"在压力 {index} 下使用既有机制作出取舍。",
                    "innovation_fit": f"用承载方式 {index} 兑现核心玩法，不新增第二核心。",
                }
            )
        candidates.append(item)
    return {
        "schema_version": "story-foundation-v1",
        "information_status": "PROPOSAL",
        "core_innovation_intent": development["core_innovation_intent"],
        "foundation_candidates": candidates,
        "kernel_contracts": {},
    }


def complete_reader_kernel_handoff(
    database: Database,
    book_id: str = BOOK_ID,
    *,
    progression_enabled: bool = True,
    import_result: bool = True,
) -> str:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT handoff_id FROM workflow_handoffs WHERE handoff_type=? "
            "ORDER BY created_at DESC LIMIT 1",
            ("ORIGINAL_READER_INTERPRETATION",),
        ).fetchone()
    assert row is not None
    handoff_id = str(row["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads((task_directory / "input" / "task.json").read_text(encoding="utf-8"))
    ids = task["original_reader_interpretation"]["contract_ids"]
    interpreted = interpret_reader_experience(
        "仅用于测试的开放 premise。", genre_hint="生存升级 / 资源管理"
    )
    reader = interpreted.reader_contract.model_copy(
        update={
            "contract_id": ids["reader_experience_contract_id"],
            "primary_narrative_drive": "SURVIVAL_RESOURCE",
            "secondary_narrative_drives": ["RESOURCE_OPPORTUNITY"],
            "drive_priority_order": ["SURVIVAL_RESOURCE", "RESOURCE_OPPORTUNITY"],
        }
    )
    market = interpreted.narrative_drive.market_category.model_copy(
        update={"metadata_id": ids["market_category_metadata_id"]}
    )
    drive = interpreted.narrative_drive.drive_contract.model_copy(
        update={
            "drive_contract_id": ids["narrative_drive_contract_id"],
            "primary_drive": NarrativeDrive.SURVIVAL_RESOURCE,
            "secondary_drives": [NarrativeDrive.RESOURCE_OPPORTUNITY],
            "progression_engine_enabled": progression_enabled,
        }
    )
    proposal = OriginalReaderKernelProposal(
        summary="封闭环境中的资源选择持续制造生存压力与成长机会。",
        reader_experience=reader,
        market_category=market,
        narrative_drive=drive,
        creative_semantics=OriginalCreativeSemantics.model_validate(
            creative_semantics_payload()
        ),
        semantic_evidence=[
            "生存压力来自不可逆选择",
            "资源机会来自每日受限行动",
            "成长引擎扩大后续行动可能性",
        ],
        uncertainties=["长期幕后来源仍待 Core Innovation 设计"],
        author_attention_points=["确认生存是否为主要驱动力"],
    )
    artifact = task_directory / "artifacts" / "reader_kernel" / "proposal.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(
        json_dumps(proposal.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    claim = claim_handoff(database, handoff_id, "test-worker")
    token = str(claim["claim_token"])
    update_handoff_status(database, handoff_id, HandoffStatus.RUNNING, claim_token=token)
    frozen = get_handoff(database, handoff_id)
    update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.COMPLETED,
        claim_token=token,
        result={
            "handoff_id": handoff_id,
            "handoff_type": "ORIGINAL_READER_INTERPRETATION",
            "requested_stage": "READER_KERNEL_PROPOSAL",
            "completed_stage": "READER_KERNEL_PROPOSED",
            "book_id": book_id,
            "edition_id": "base",
            "status": "COMPLETED",
            "artifact_paths": ["artifacts/reader_kernel/proposal.json"],
            "canon_committed": False,
            "edition_activated": False,
            "base_event_seq": int(frozen["base_event_seq"]),
            "base_projection_hash": str(frozen["base_projection_hash"]),
        },
    )
    if import_result:
        import_original_reader_kernel_proposal(database, book_id, handoff_id)
    return handoff_id


def create_original(
    tmp_path: Path, *, semantic_ready: bool = True
) -> tuple[BookLayout, Database]:
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
    database = Database(Path(str(created["database"])))
    if semantic_ready:
        complete_reader_kernel_handoff(database)
    return layout, database


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
    proposal_data = foundation_payload()
    proposal_data["kernel_contracts"] = original_request["progression_kernel"]
    selected_core = original_request["progression_kernel"]["core_innovation"]
    proposal_data["core_innovation_intent"] = {
        "selected_primary_innovation_id": selected_core[
            "selected_primary_innovation_id"
        ],
        "optional_mix_notes": selected_core.get("optional_mix_notes", ""),
    }
    proposal = StoryFoundationProposal.model_validate(proposal_data)
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
            item["candidate_id"] for item in foundation_payload()["foundation_candidates"]
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


def complete_development_handoff(
    database: Database, *, progression_enabled: bool = True
) -> str:
    selected = select_original_foundation(database, BOOK_ID, "foundation-1")
    development_handoff_id = str(selected["handoff"]["handoff_id"])
    frozen_handoff = get_handoff(database, development_handoff_id)
    original_request = json.loads(
        (
            Path(str(frozen_handoff["task_directory"]))
            / "input"
            / "original_request.json"
        ).read_text(encoding="utf-8")
    )
    development_data = proposal_payload(progression_enabled=progression_enabled)
    development_data["kernel_contracts"] = original_request["progression_kernel"]
    development_data["core_innovation_intent"] = {
        "selected_primary_innovation_id": original_request["progression_kernel"][
            "core_innovation"
        ]["selected_primary_innovation_id"],
        "optional_mix_notes": original_request["progression_kernel"]["core_innovation"].get(
            "optional_mix_notes", ""
        ),
    }
    selected_foundation = original_request["selected_story_foundation"]
    development_data["selected_foundation_id"] = selected_foundation[
        "selected_foundation_id"
    ]
    development_data["selected_foundation"] = selected_foundation["selected_candidate"]
    development_data["first_phase"]["selected_foundation_id"] = selected_foundation[
        "selected_foundation_id"
    ]
    development = FoundationDevelopmentProposal.model_validate(development_data)
    artifact = (
        Path(str(frozen_handoff["task_directory"]))
        / "artifacts"
        / "foundation_development"
        / "proposal.json"
    )
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(
        json_dumps(development.model_dump(mode="json"), indent=2), encoding="utf-8"
    )
    claim = claim_handoff(database, development_handoff_id, "test-worker")
    token = str(claim["claim_token"])
    update_handoff_status(
        database, development_handoff_id, HandoffStatus.RUNNING, claim_token=token
    )
    frozen = get_handoff(database, development_handoff_id)
    update_handoff_status(
        database,
        development_handoff_id,
        HandoffStatus.COMPLETED,
        claim_token=token,
        result={
            "handoff_id": development_handoff_id,
            "handoff_type": "ORIGINAL_BOOK_BOOTSTRAP",
            "requested_stage": "FOUNDATION_DEVELOPMENT_PROPOSAL",
            "completed_stage": "FOUNDATION_DEVELOPED",
            "book_id": BOOK_ID,
            "edition_id": "base",
            "status": "COMPLETED",
            "artifact_paths": ["artifacts/foundation_development/proposal.json"],
            "canon_committed": False,
            "edition_activated": False,
            "base_event_seq": int(frozen["base_event_seq"]),
            "base_projection_hash": str(frozen["base_projection_hash"]),
        },
    )
    import_original_foundation_development(database, BOOK_ID, development_handoff_id)
    return development_handoff_id


def accept_foundation(
    database: Database, *, progression_enabled: bool = True
) -> dict[str, Any]:
    handoff_id = complete_bootstrap_handoff(database)
    import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)
    complete_development_handoff(database, progression_enabled=progression_enabled)
    proposal = proposal_payload(progression_enabled=progression_enabled)
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
    layout, database = create_original(tmp_path, semantic_ready=False)
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
    assert handoff_count == 1
    assert record.original_state == "READER_EXPERIENCE_GENERATING"
    handoff = get_handoff(
        database,
        str(
            next(
                item
                for item in original_overview(database, BOOK_ID)["handoffs"]
                if item["handoff_type"] == "ORIGINAL_READER_INTERPRETATION"
            )["handoff_id"]
        ),
    )
    task = json.loads(
        (Path(str(handoff["task_directory"])) / "input" / "task.json").read_text(
            encoding="utf-8"
        )
    )
    assert task["executor_skill"] == "interpret-original-reader-kernel"
    assert task["business_input_files"] == ["original_request.json"]
    assert len(catalog.entries) == 1
    assert catalog.entries[0].href == f"/books/{BOOK_ID}/original"
    assert catalog.entries[0].state == "READER_EXPERIENCE_GENERATING"
    assert catalog.entries[0].handoff_id == handoff["handoff_id"]
    assert studio_access(layout, record).access_level.value == "ONBOARDING"


def test_completed_reader_semantic_handoff_imports_review_only_contracts(
    tmp_path: Path,
) -> None:
    _, database = create_original(tmp_path, semantic_ready=False)
    complete_reader_kernel_handoff(database, import_result=False)

    overview = original_overview(database, BOOK_ID)
    records = list_contract_records(database, book_id=BOOK_ID, edition_id="base")
    reader_contracts = {
        record.contract_type: record
        for record in records
        if record.contract_type
        in {
            ProgressionContractType.READER_EXPERIENCE,
            ProgressionContractType.MARKET_CATEGORY,
            ProgressionContractType.NARRATIVE_DRIVE,
        }
    }
    with database.connect() as connection:
        chapter_count, canon_count = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM chapters), "
                "(SELECT COUNT(*) FROM canon_commits)"
            ).fetchone()
        )

    assert overview["original_state"] == "READER_EXPERIENCE_REVIEW"
    assert set(overview["reader_experience"]["reader_experience"]["experience_priorities"]) == {
        item.value for item in ReaderExperience
    }
    assert set(reader_contracts) == {
        ProgressionContractType.READER_EXPERIENCE,
        ProgressionContractType.MARKET_CATEGORY,
        ProgressionContractType.NARRATIVE_DRIVE,
    }
    assert {record.status for record in reader_contracts.values()} == {
        ContractStatus.NEEDS_REVIEW
    }
    assert (chapter_count, canon_count) == (0, 0)


def test_unseen_premise_is_frozen_for_semantic_read_without_python_fallback(
    tmp_path: Path,
) -> None:
    premise = "主角每说出一个从未有人说过的真句子，世界就失去一种旧的可能性。"
    layout = BookLayout(tmp_path / "library")
    created = create_original_book(layout, {"premise": premise}, book_id=BOOK_ID)
    database = Database(Path(str(created["database"])))
    handoff = get_handoff(database, str(created["reader_handoff"]["handoff_id"]))
    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads(
        (task_directory / "input" / "task.json").read_text(encoding="utf-8")
    )
    request = json.loads(
        (task_directory / "input" / "original_request.json").read_text(encoding="utf-8")
    )
    with database.connect() as connection:
        contract_count = connection.execute(
            "SELECT COUNT(*) FROM progression_contract_versions"
        ).fetchone()[0]

    assert request["premise"] == premise
    assert request["genre"] == ""
    assert task["executor_skill"] == "interpret-original-reader-kernel"
    assert task["business_input_files"] == ["original_request.json"]
    assert task["original_reader_interpretation"]["proposal_schema"]["title"] == (
        "OriginalReaderKernelProposal"
    )
    assert contract_count == 0


def test_reader_priority_edits_do_not_reinfer_primary_drive(tmp_path: Path) -> None:
    _, database = create_original(tmp_path)

    confirmed = confirm_original_reader_experience(
        database,
        BOOK_ID,
        priority_overrides={
            "PROGRESSION": "CORE",
            "BREAKTHROUGH": "CORE",
            "ARTIFACT_OR_ABILITY": "CORE",
        },
    )

    assert confirmed["reader_experience"]["payload"]["primary_narrative_drive"] == (
        "SURVIVAL_RESOURCE"
    )
    assert confirmed["narrative_drive"]["payload"]["primary_drive"] == (
        "SURVIVAL_RESOURCE"
    )
    assert confirmed["narrative_drive"]["payload"]["progression_engine_enabled"] is True


def test_core_innovation_precedes_foundation_and_freezes_author_intent(tmp_path: Path) -> None:
    assert set(CoreInnovationCandidate.model_fields) == {
        "innovation_id",
        "title",
        "plain_language_pitch",
        "concrete_example",
        "reader_anticipation",
        "unresolved_design_choices",
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
    signature_mechanism = creative_semantics_payload()["existing_signature_mechanism"]
    assert all(signature_mechanism in item["core_mechanism"] for item in candidates)
    assert len({tuple(item["unresolved_design_choices"]) for item in candidates}) == 3

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
    old_handoff_id = str(selected["handoff"]["handoff_id"])
    selected = select_original_core_innovation(
        database,
        BOOK_ID,
        {
            "selected_primary_innovation_id": candidates[1]["innovation_id"],
            "optional_mix_notes": "作者明确改选",
        },
    )
    assert get_handoff(database, old_handoff_id)["status"] == "STALE"
    foundation_handoff = get_handoff(database, str(selected["handoff"]["handoff_id"]))
    assert foundation_handoff["requested_stage"] == "STORY_FOUNDATION_PROPOSAL"
    foundation_request = json.loads(
        (Path(str(foundation_handoff["task_directory"])) / "input" / "original_request.json")
        .read_text(encoding="utf-8")
    )
    assert foundation_request["progression_kernel"]["foundation_rules"] == [
        "故事基础候选必须共享已确认的 Reader Experience、Primary Narrative Drive "
        "与 Creative Semantics",
        "故事基础候选必须用不同故事活动、压力、资源、关系与扩张方式承载同一核心玩法",
        "不得为追求候选差异新增未经 Seed、Creative Semantics 或 Core Intent "
        "需要的竞争性第二核心机制",
    ]
    assert foundation_request["progression_kernel"]["creative_semantics"] == (
        creative_semantics_payload()
    )
    assert (
        foundation_request["progression_kernel"]["core_innovation"][
            "selected_primary_innovation_id"
        ]
        == candidates[1]["innovation_id"]
    )
    with database.connect() as connection:
        state = connection.execute(
            "SELECT selected_primary_innovation_id, optional_mix_notes, state "
            "FROM original_states WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
    assert state["selected_primary_innovation_id"] == candidates[1]["innovation_id"]
    assert state["optional_mix_notes"] == "作者明确改选"
    assert state["state"] == "FOUNDATION_GENERATING"

    foundation_handoff_id = complete_foundation_handoff(database)
    foundation_imported = import_original_bootstrap_proposal(
        database, BOOK_ID, foundation_handoff_id
    )
    assert foundation_imported["proposal"]["core_innovation_intent"] == selected[
        "innovation_intent"
    ]
    foundation_candidates = foundation_imported["proposal"]["foundation_candidates"]
    assert len(
        {
            (
                item["typical_choice"],
                item["risk_structure"],
                item["resource_structure"],
                item["social_configuration"],
                item["world_carrier"],
            )
            for item in foundation_candidates
        }
    ) == 3
    assert all("不新增第二核心" in item["innovation_fit"] for item in foundation_candidates)

    development = select_original_foundation(
        database,
        BOOK_ID,
        foundation_candidates[0]["candidate_id"],
    )
    development_handoff = get_handoff(database, str(development["handoff"]["handoff_id"]))
    development_request = json.loads(
        (
            Path(str(development_handoff["task_directory"]))
            / "input"
            / "original_request.json"
        ).read_text(encoding="utf-8")
    )
    assert development_request["progression_kernel"]["creative_semantics"] == (
        creative_semantics_payload()
    )
    assert development_request["selected_story_foundation"]["selected_candidate"] == (
        foundation_candidates[0]
    )

    complete_development_handoff(database)
    developed = original_overview(database, BOOK_ID)["development_proposal"]
    assert developed["kernel_contracts"]["creative_semantics"] == (
        creative_semantics_payload()
    )
    grammar_text = json.dumps(
        {
            "progression": developed["progression_grammar"],
            "expansion": developed["expansion_grammar"],
            "payoff": developed["payoff_grammar"],
            "first_phase": developed["first_phase"],
        },
        ensure_ascii=False,
    )
    assert all(
        step in grammar_text
        for step in creative_semantics_payload()["repeatable_reader_loop"]
    )
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


def test_foundation_can_be_explicitly_reselected_before_final_confirmation(
    tmp_path: Path,
) -> None:
    layout, database = create_original(tmp_path)
    handoff_id = complete_bootstrap_handoff(database)
    import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)

    first = select_original_foundation(database, BOOK_ID, "foundation-1")
    first_handoff_id = str(first["handoff"]["handoff_id"])
    second = select_original_foundation(database, BOOK_ID, "foundation-2")

    assert get_handoff(database, first_handoff_id)["status"] == "STALE"
    assert second["selected_foundation_id"] == "foundation-2"
    with database.connect() as connection:
        state = connection.execute(
            "SELECT selected_primary_innovation_id, selected_foundation_id, "
            "accepted_apply_id FROM original_states WHERE book_id=?",
            (BOOK_ID,),
        ).fetchone()
        archived = connection.execute(
            "SELECT COUNT(*) FROM original_development_versions "
            "WHERE book_id=? AND status='ARCHIVED'",
            (BOOK_ID,),
        ).fetchone()[0]
        canon_count = connection.execute("SELECT COUNT(*) FROM canon_commits").fetchone()[0]
    assert state["selected_primary_innovation_id"] == "innovation-1"
    assert state["selected_foundation_id"] == "foundation-2"
    assert state["accepted_apply_id"] is None
    assert archived == 1
    assert canon_count == 0
    app = create_app(
        database,
        library_root=layout.library_root,
        discovery_root=tmp_path / "book",
    )
    with TestClient(app) as client:
        page = client.get(f"/books/{BOOK_ID}/original")
    assert "重新选择核心玩法" in page.text
    assert "换一个故事基础" in page.text
    assert "不会删除历史，也不会修改 Canon" in Path(
        "src/novel_authoring/web/static/original.js"
    ).read_text(encoding="utf-8")


def test_same_core_and_foundation_selection_reuse_existing_downstream(
    tmp_path: Path,
) -> None:
    _, database = create_original(tmp_path)
    handoff_id = complete_bootstrap_handoff(database)
    import_original_bootstrap_proposal(database, BOOK_ID, handoff_id)
    first = select_original_foundation(database, BOOK_ID, "foundation-1")
    development_handoff_id = str(first["handoff"]["handoff_id"])

    repeated_foundation = select_original_foundation(database, BOOK_ID, "foundation-1")
    repeated_core = select_original_core_innovation(
        database,
        BOOK_ID,
        {
            "selected_primary_innovation_id": "innovation-1",
            "optional_mix_notes": "吸收机制 2 的一个选择特征",
        },
    )
    with database.connect() as connection:
        foundation_tasks = connection.execute(
            "SELECT COUNT(*) FROM workflow_handoffs WHERE book_id=? "
            "AND requested_stage='STORY_FOUNDATION_PROPOSAL'",
            (BOOK_ID,),
        ).fetchone()[0]
        development_tasks = connection.execute(
            "SELECT COUNT(*) FROM workflow_handoffs WHERE book_id=? "
            "AND requested_stage='FOUNDATION_DEVELOPMENT_PROPOSAL'",
            (BOOK_ID,),
        ).fetchone()[0]

    assert repeated_foundation["idempotent"] is True
    assert repeated_foundation["handoff"]["handoff_id"] == development_handoff_id
    assert repeated_core["idempotent"] is True
    assert "foundation_proposal" in repeated_core
    assert foundation_tasks == 1
    assert development_tasks == 1
    assert get_handoff(database, development_handoff_id)["status"] == "READY_FOR_CODEX"


def test_replacing_foundation_proposal_invalidates_only_downstream_selection(
    tmp_path: Path,
) -> None:
    _, database = create_original(tmp_path)
    current_handoff_id = complete_bootstrap_handoff(database)
    current = import_original_bootstrap_proposal(database, BOOK_ID, current_handoff_id)
    selected = select_original_foundation(database, BOOK_ID, "foundation-1")
    development_handoff_id = str(selected["handoff"]["handoff_id"])

    unchanged = resolve_original_proposal_version(
        database,
        BOOK_ID,
        str(current["proposal_version_id"]),
        action="REPLACE_CURRENT",
    )
    assert unchanged["current_changed"] is False
    assert get_handoff(database, development_handoff_id)["status"] == "READY_FOR_CODEX"

    replacement_handoff_id = complete_foundation_handoff(database)
    replacement = import_original_bootstrap_proposal(
        database, BOOK_ID, replacement_handoff_id
    )
    changed = resolve_original_proposal_version(
        database,
        BOOK_ID,
        str(replacement["proposal_version_id"]),
        action="REPLACE_CURRENT",
    )
    with database.connect() as connection:
        state = connection.execute(
            "SELECT state, selected_primary_innovation_id, "
            "selected_foundation_proposal_version_id, selected_foundation_id, "
            "current_development_proposal_version_id FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
        canon_count = connection.execute("SELECT COUNT(*) FROM canon_commits").fetchone()[0]

    assert changed["downstream_invalidated"] is True
    assert tuple(state) == ("FOUNDATION_REVIEW", "innovation-1", None, None, None)
    assert get_handoff(database, development_handoff_id)["status"] == "STALE"
    assert canon_count == 0


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
        development_count = connection.execute(
            "SELECT COUNT(*) FROM original_development_versions"
        ).fetchone()[0]
    assert set(StoryFoundationProposal.model_fields) == {
        "schema_version",
        "information_status",
        "core_innovation_intent",
        "foundation_candidates",
        "kernel_contracts",
    }
    assert development_count == 0
    with pytest.raises(OriginalWorkflowError, match="Development"):
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
    development_handoff_id = complete_development_handoff(database)
    proposed_kernel = [
        record
        for record in list_contract_records(database, book_id=BOOK_ID, edition_id="base")
        if record.source == f"ORIGINAL_FOUNDATION_DEVELOPMENT:{development_handoff_id}"
    ]
    assert {record.contract_type for record in proposed_kernel} == {
        ProgressionContractType.GENRE,
        ProgressionContractType.PROGRESSION,
        ProgressionContractType.WORLD_EXPANSION,
        ProgressionContractType.PAYOFF_CHANNEL,
    }
    assert {record.status for record in proposed_kernel} == {ContractStatus.NEEDS_REVIEW}
    app = create_app(
        database,
        library_root=layout.library_root,
        discovery_root=tmp_path / "book",
    )
    with TestClient(app) as client:
        development_page = client.get(f"/books/{BOOK_ID}/original")
    assert 'data-selected-foundation-title="基础框架 1"' in development_page.text
    assert "第一次实质性局势升级" in development_page.text
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
    effective_kernel = {
        record.contract_type: record
        for record in list_contract_records(database, book_id=BOOK_ID, edition_id="base")
        if record.status is ContractStatus.EFFECTIVE
    }
    assert set(effective_kernel) == set(ProgressionContractType)
    assert {record.effective_from_boundary for record in effective_kernel.values()} == {1}
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


def test_progression_disabled_does_not_create_progression_contract(tmp_path: Path) -> None:
    _, database = create_original(tmp_path, semantic_ready=False)
    complete_reader_kernel_handoff(database, progression_enabled=False)

    result = accept_foundation(database, progression_enabled=False)
    records = list_contract_records(database, book_id=BOOK_ID, edition_id="base")

    assert result["original_state"] == "FOUNDATION_READY"
    assert all(
        record.contract_type is not ProgressionContractType.PROGRESSION
        for record in records
    )
    assert {
        record.contract_type
        for record in records
        if record.status is ContractStatus.EFFECTIVE
    } == set(ProgressionContractType) - {ProgressionContractType.PROGRESSION}


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
    with pytest.raises(OriginalWorkflowError, match="最终确认"):
        select_original_foundation(database, BOOK_ID, "foundation-2")
    with pytest.raises(OriginalWorkflowError, match="最终确认"):
        select_original_core_innovation(
            database,
            BOOK_ID,
            {
                "selected_primary_innovation_id": "innovation-2",
                "optional_mix_notes": "最终确认后不允许普通改选",
            },
        )
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

    with pytest.raises(OriginalWorkflowError, match="最终确认"):
        resolve_original_proposal_version(
            database,
            BOOK_ID,
            str(imported["proposal_version_id"]),
            action="REPLACE_CURRENT",
        )
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
    kernel_context = build_kernel_planning_context(
        database,
        book_id=BOOK_ID,
        edition_id="base",
        author_policy={},
    )
    assert kernel_context is not None
    effective = kernel_context.effective_contracts
    assert effective.reader_experience is not None
    assert effective.market_category is not None
    assert effective.narrative_drive is not None
    assert effective.genre is not None
    assert effective.progression is not None
    assert effective.world_expansion is not None
    assert effective.payoff_channel is not None
    assert effective.narrative_drive["primary_drive"] == "SURVIVAL_RESOURCE"
    assert effective.narrative_drive["progression_engine_enabled"] is True
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
        book_database = Database(BookLayout(library_root).for_book(book_id).database)
        complete_reader_kernel_handoff(book_database, book_id)
        confirmed = client.post(
            f"/api/books/{book_id}/original/reader-experience/confirm",
            headers={"X-CSRF-Token": token},
            json={
                "adjustment": "CONFIRM",
                "primary_drive": "SURVIVAL_RESOURCE",
                "secondary_drives": ["RESOURCE_OPPORTUNITY"],
                "progression_engine_enabled": True,
                "creative_semantics": creative_semantics_payload(),
            },
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
    assert "Semantic First Read" in reader_step.text
    assert "故事靠什么长期推进" in reader_step.text
    assert "长期推进" in reader_step.text
    assert "AI 任务" in original.text
    assert instruction.status_code == 200
    assert instruction.json()["instruction"]
    assert f'data-copy-instruction="{instruction_url}"' in original.text
    assert f'href="/api/handoffs/{handoff_id}/instruction"' not in original.text


def test_original_studio_renders_human_first_core_and_foundation_cards(
    tmp_path: Path,
) -> None:
    layout, database = create_original(tmp_path)
    core_handoff_id = complete_core_innovation_handoff(database)
    import_original_core_innovation_proposal(database, BOOK_ID, core_handoff_id)
    app = create_app(
        database,
        library_root=layout.library_root,
        discovery_root=tmp_path / "book",
    )

    with TestClient(app) as client:
        core_page = client.get(f"/books/{BOOK_ID}/original")

    assert core_page.status_code == 200
    assert "核心玩法" in core_page.text
    assert "保留每日受限机会" in core_page.text
    assert "具体示例（NON_CANON，仅供理解）" in core_page.text
    assert "为什么会期待下一次" in core_page.text
    assert "查看设计细节" in core_page.text

    selected = select_original_core_innovation(
        database,
        BOOK_ID,
        {
            "selected_primary_innovation_id": "innovation-1",
            "optional_mix_notes": "",
        },
    )
    assert selected["handoff"]["status"]["status"] == "READY_FOR_CODEX"
    foundation_handoff_id = complete_foundation_handoff(database)
    import_original_bootstrap_proposal(database, BOOK_ID, foundation_handoff_id)

    with TestClient(app) as client:
        foundation_page = client.get(f"/books/{BOOK_ID}/original")

    assert foundation_page.status_code == 200
    assert "主角在压力中承担代价明确的选择" in foundation_page.text
    assert "档案室出现异常空洞" in foundation_page.text
    assert "在安全与测试核心机制之间不可逆选择" in foundation_page.text
    assert "阻止下一次删除" in foundation_page.text
    assert "查看故事结构" in foundation_page.text


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
        assert before.text.count("标准") >= 20
        assert before.text.count("data-reader-experience-key=") == 20
        assert 'data-reader-strength="CORE"' in before.text
        assert "调整创作语义" in before.text
        assert before.text.count("data-creative-semantics-key=") == 9
        for label in ("战斗和爽点更强", "谜团更强", "团队更强", "关系更强", "职业更强"):
            assert label in before.text
        assert "const presets" not in (
            Path("src/novel_authoring/web/static/original.js").read_text(encoding="utf-8")
        )

        author_semantics = creative_semantics_payload()
        author_semantics.update(
            {
                "signature_fantasy": "作者改写后的核心幻想",
                "existing_signature_mechanism": "作者确认的既有机制",
                "open_design_space": ["作者开放空间"],
                "payoff_texture": ["作者兑现质感"],
                "novelty_focus": ["作者新奇度焦点"],
                "realism_anchors": ["作者可信锚点"],
                "complexity_boundaries": ["世界可以高度复杂，但不得创造竞争性第二主机制"],
                "repeatable_reader_loop": ["压力", "主动选择", "快速兑现", "更大局势"],
                "anti_drift": ["不得退回 AI 原始语义"],
            }
        )
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
                "primary_drive": "RESOURCE_OPPORTUNITY",
                "secondary_drives": ["MYSTERY_INVESTIGATION"],
                "progression_engine_enabled": True,
                "creative_semantics": author_semantics,
            },
        )
        assert confirmed.status_code == 200, confirmed.text
        reader = confirmed.json()["reader_experience"]["payload"]
        priorities = reader["experience_priorities"]
        assert priorities["RESOURCE_OPPORTUNITY"] == "VERY_HIGH"
        assert priorities["PROGRESSION"] == "LOW"
        assert priorities["POWER_VERIFICATION"] == "HIGH"
        assert reader["primary_narrative_drive"] == "RESOURCE_OPPORTUNITY"
        drive = confirmed.json()["narrative_drive"]["payload"]
        assert drive["primary_drive"] == "RESOURCE_OPPORTUNITY"
        assert "MYSTERY_INVESTIGATION" in drive["secondary_drives"]

        after = client.get(f"/books/{BOOK_ID}/original")
        assert after.status_code == 200
        assert 'data-reader-experience-confirmed' in after.text
        assert "资源机会" in after.text
        assert "已确认 · 阅读体验" in after.text
        assert "后续推理不得静默覆盖作者确认值" in after.text
        assert "已确认的创作语义" in after.text
        assert "作者改写后的核心幻想" in after.text
        assert "世界可以高度复杂" in after.text
        assert "data-creative-semantics-controls" not in after.text

    # The same effective contract is still the persisted source for the next read.
    overview = original_overview(database, BOOK_ID)
    display = overview["reader_experience_display"]
    displayed = {item["key"]: item["value_label"] for item in display["priorities"]}
    assert displayed["RESOURCE_OPPORTUNITY"] == "核心"
    assert displayed["PROGRESSION"] == "次要"
    assert displayed["POWER_VERIFICATION"] == "强化"
    assert overview["reader_experience"]["creative_semantics"] == author_semantics
    with database.connect() as connection:
        persisted = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
    assert persisted is not None
    assert json.loads(str(persisted["confirmed_creative_semantics_json"])) == author_semantics


def test_confirmed_creative_semantics_are_sqlite_authority_when_projection_drifts(
    tmp_path: Path,
) -> None:
    layout, database = create_original(tmp_path)
    author_semantics = creative_semantics_payload()
    author_semantics["signature_fantasy"] = "作者版本 B"
    author_semantics["anti_drift"] = ["作者防漂移边界"]
    confirmed = confirm_original_reader_experience(
        database,
        BOOK_ID,
        creative_semantics=author_semantics,
    )
    handoff_count = database.scalar(
        "SELECT COUNT(*) FROM workflow_handoffs WHERE book_id=? AND handoff_type=?",
        (BOOK_ID, "ORIGINAL_BOOK_BOOTSTRAP"),
    )
    retry = confirm_original_reader_experience(
        database,
        BOOK_ID,
        creative_semantics=author_semantics,
    )
    assert retry["idempotent"] is True
    assert database.scalar(
        "SELECT COUNT(*) FROM workflow_handoffs WHERE book_id=? AND handoff_type=?",
        (BOOK_ID, "ORIGINAL_BOOK_BOOTSTRAP"),
    ) == handoff_count

    proposal_path = (
        layout.for_book(BOOK_ID).edition("base").analysis
        / "original"
        / "reader_experience.json"
    )
    stale = json.loads(proposal_path.read_text(encoding="utf-8"))
    stale["creative_semantics"]["signature_fantasy"] = "AI 旧版本 A"
    proposal_path.write_text(json_dumps(stale, indent=2), encoding="utf-8")
    overview = original_overview(database, BOOK_ID)
    assert overview["reader_experience"]["creative_semantics"] == author_semantics
    request = json.loads(
        (
            Path(str(confirmed["handoff"]["task_directory"]))
            / "input"
            / "original_request.json"
        ).read_text(encoding="utf-8")
    )
    assert request["progression_kernel"]["creative_semantics"] == author_semantics

    proposal_path.unlink()
    assert original_overview(database, BOOK_ID)["reader_experience"][
        "creative_semantics"
    ] == author_semantics
    reader_handoffs_before = database.scalar(
        "SELECT COUNT(*) FROM workflow_handoffs WHERE book_id=? AND handoff_type=?",
        (BOOK_ID, "ORIGINAL_READER_INTERPRETATION"),
    )
    prepared_reader = prepare_original_reader_experience(database, BOOK_ID)
    assert prepared_reader["deduplicated"] is True
    assert database.scalar(
        "SELECT COUNT(*) FROM workflow_handoffs WHERE book_id=? AND handoff_type=?",
        (BOOK_ID, "ORIGINAL_READER_INTERPRETATION"),
    ) == reader_handoffs_before
    retry_without_projection = confirm_original_reader_experience(database, BOOK_ID)
    assert retry_without_projection["idempotent"] is True
    proposal_path.write_text('{"broken": true}', encoding="utf-8")
    retry_with_broken_projection = confirm_original_reader_experience(database, BOOK_ID)
    assert retry_with_broken_projection["idempotent"] is True

    changed = dict(author_semantics)
    changed["anti_drift"] = ["不同的 stale 请求"]
    with pytest.raises(OriginalWorkflowError, match="已确认"):
        confirm_original_reader_experience(
            database,
            BOOK_ID,
            creative_semantics=changed,
        )
    with database.connect() as connection:
        stored = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
    assert stored is not None
    assert json.loads(str(stored["confirmed_creative_semantics_json"])) == author_semantics


def test_reader_author_decision_rolls_back_together_on_database_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, database = create_original(tmp_path)
    original_confirm = original_service._confirm_contract_in_connection
    calls = 0

    def fail_second_confirmation(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise sqlite3.OperationalError("simulated drive confirmation failure")
        return original_confirm(*args, **kwargs)

    monkeypatch.setattr(
        original_service, "_confirm_contract_in_connection", fail_second_confirmation
    )
    with pytest.raises(sqlite3.OperationalError, match="simulated"):
        confirm_original_reader_experience(
            database,
            BOOK_ID,
            creative_semantics=creative_semantics_payload(),
        )
    records = list_contract_records(database, book_id=BOOK_ID, edition_id="base")
    assert not any(record.status is ContractStatus.EFFECTIVE for record in records)
    with database.connect() as connection:
        stored = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
    assert stored is not None
    assert stored["confirmed_creative_semantics_json"] is None


def test_projection_write_failure_does_not_rollback_reader_author_decision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, database = create_original(tmp_path)

    def fail_projection_write(path: Path, payload: Any) -> Path:
        raise OSError("simulated projection failure")

    monkeypatch.setattr(original_service, "_write_json", fail_projection_write)
    semantics = creative_semantics_payload()
    confirmed = confirm_original_reader_experience(
        database,
        BOOK_ID,
        creative_semantics=semantics,
    )
    assert "projection 写入失败" in confirmed["warning"]
    effective = {
        record.contract_type
        for record in list_contract_records(database, book_id=BOOK_ID, edition_id="base")
        if record.status is ContractStatus.EFFECTIVE
    }
    assert ProgressionContractType.READER_EXPERIENCE in effective
    assert ProgressionContractType.NARRATIVE_DRIVE in effective
    with database.connect() as connection:
        stored = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (BOOK_ID,),
        ).fetchone()
    assert stored is not None
    assert json.loads(str(stored["confirmed_creative_semantics_json"])) == semantics
