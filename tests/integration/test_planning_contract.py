from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from novel_authoring.author_control.book_profile import (
    PROFILE_DIMENSIONS,
    ProfileEditOperation,
    ProfileStrength,
    edit_book_profile,
)
from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.author_control.source_state import (
    SourceChapterStateDelta,
    SourceStateCategory,
    SourceStateCoverageStatus,
    SourceStateOperation,
    SourceStateVerification,
    record_source_chapter_deltas,
    record_source_state_coverage,
)
from novel_authoring.canon.projection import rebuild_projection
from novel_authoring.config import Settings, load_settings
from novel_authoring.db.database import Database
from novel_authoring.drafting.service import import_draft_output, prepare_draft_task
from novel_authoring.ingest.service import ingest_book
from novel_authoring.metrics.engine import MetricInputBundle, diagnose_bundle, persist_results
from novel_authoring.planning.boundary import PlanningError, build_boundary_packet
from novel_authoring.planning.candidates import (
    import_candidate_output,
    prepare_candidate_task,
)
from novel_authoring.planning.contracts import build_chapter_contract
from novel_authoring.planning.models import ChapterContract
from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.service import (
    ProgressionContractType,
    confirm_contract,
    create_contract_proposal,
)
from novel_authoring.utils import json_dumps, sha256_file, utc_now
from novel_authoring.validation.service import validate_draft
from novel_authoring.web.workbench import _candidate_cards
from novel_authoring.workflows.approval import approve_draft
from novel_authoring.workflows.directives import add_directive
from novel_authoring.workflows.exporting import export_book

FIXTURE = Path(__file__).parents[1] / "fixtures" / "合成求生小说.md"


def setup_planning_book(tmp_path: Path) -> tuple[Database, Path, Settings]:
    source_root = tmp_path / "中文小说"
    source_root.mkdir()
    (source_root / FIXTURE.name).write_bytes(FIXTURE.read_bytes())
    workspace = tmp_path / "workspace"
    settings = load_settings()
    ingest_book(
        book_id="planning-book",
        title="合成求生小说",
        source_root=source_root,
        workspace_root=workspace,
        settings=settings,
    )
    database = Database(workspace / "planning-book" / "state.sqlite3")
    with database.connect() as connection:
        for index, (thread_id, goal, progress) in enumerate(
            [
                ("station-defense", "守住气象站", 0.7),
                ("radio-caller", "确认无线电呼叫者身份", 0.4),
                ("wind-rule", "理解午夜风向规则", 0.5),
            ],
            1,
        ):
            connection.execute(
                """
                INSERT INTO threads(
                    thread_id, book_id, goal, stakes, phase,
                    introduced_chapter, last_advanced_chapter,
                    importance, reader_visibility, progress,
                    dependencies_json, status, payload_json, created_at
                ) VALUES (?, 'planning-book', ?, ?, 'escalation', '1', ?, ?, 0.9, ?, '[]',
                          'CANON', ?, ?)
                """,
                (
                    thread_id,
                    goal,
                    f"线程 {index} 失败会改变后续选择",
                    str(index),
                    1 - index * 0.1,
                    progress,
                    json_dumps(
                        {
                            "deadline_urgency": 80 - index * 10,
                            "payoff_readiness": progress * 100,
                            "goal_blockage": (1 - progress) * 100,
                            "diversity_bonus": 40 + index * 10,
                        }
                    ),
                    utc_now(),
                ),
            )
    bundle = MetricInputBundle.model_validate(
        {
            "pressure": {
                "threat": 70,
                "scarcity": 60,
                "deadline": 80,
                "uncertainty": 50,
                "social_conflict": 20,
                "failure_accumulation": 30,
            },
            "narrative_debt": {
                "importance": 0.8,
                "reader_visibility": 0.9,
                "promise_progress": 0.4,
                "age_chapters": 3,
                "target_max_age": 5,
                "reminder_count": 1,
            },
            "progress": {
                "permanent_growth": 40,
                "world_state_change": 50,
                "relationship_change": 20,
                "knowledge_change": 70,
                "goal_advance": 60,
                "strategy_expansion": 30,
            },
            "payoff": {
                "maturity": 70,
                "impact": 60,
                "causality": 90,
                "after_value": 70,
                "repetition_fatigue": 10,
                "structural_fit": 80,
                "future_damage": 10,
            },
            "repetition_history": [{"distance": 5, "similarity": 0.2}],
            "risk_credibility": {
                "realized_cost_rate": 60,
                "consequence_clarity": 80,
                "opposition_effectiveness": 60,
                "protection_limit_visibility": 70,
                "information_limits": 80,
            },
        }
    )
    persist_results(
        database,
        "planning-book",
        diagnose_bundle(bundle, settings.metrics),
        settings.metrics,
    )
    return database, workspace, settings


def candidate_payload(
    local_id: str,
    thread_id: str,
    *,
    score: float,
    variant: int,
) -> dict[str, Any]:
    structures = [
        (
            "午夜风暴迫近",
            "修复气象站机械门",
            "主角用时间换取防御控制",
            "断电与门体损坏",
            "放弃监听一次无线电",
            "紧张后的有限掌控",
            "远方呼叫者改变联络频率",
            "狭窄维修层与屋顶",
            "气象站可守但无线电线索延后",
        ),
        (
            "无线电主动发来坐标",
            "交叉验证地图与呼叫内容",
            "主角设置错误信息测试对方",
            "暴露位置与信任风险",
            "消耗最后一段电量",
            "怀疑转为审慎合作",
            "呼叫者交付可验证情报",
            "控制室与远端声音双场景",
            "获得路线但确认对方仍隐瞒身份",
        ),
        (
            "同伴在门外留下求援记号",
            "谈判换取共同值守",
            "主角以钥匙权限设置合作条件",
            "关系背叛与物资分配风险",
            "让出一半安全空间",
            "孤立转为带条件的互信",
            "新同伴承担第一次守夜",
            "门内门外的对峙空间",
            "关系改变但地下秘密仍未解决",
        ),
    ]
    structure = structures[variant]
    character_keys = load_settings().metrics["character_fit"]["weights"]
    style_keys = load_settings().metrics["style_fit"]["weights"]
    return {
        "local_id": local_id,
        "title": f"候选 {variant + 1}",
        "summary": "产生一个可追溯的下一章状态变化",
        "primary_thread_id": thread_id,
        "primary_function": ["progress", "discovery", "relationship_shift"][variant],
        "secondary_functions": ["choice"],
        "reader_question": "主角会如何用有限资源换取下一步控制？",
        "event_source": structure[0],
        "solution_method": structure[1],
        "protagonist_strategy": structure[2],
        "risk_form": structure[3],
        "opportunity_cost": structure[4],
        "emotional_outcome": structure[5],
        "social_feedback": structure[6],
        "scene_topology": structure[7],
        "ending_state": structure[8],
        "state_changes": [structure[8]],
        "causal_sources": ["前三章已建立的风向、钥匙与无线电"],
        "promises_to_advance": [thread_id],
        "promises_to_pay": [],
        "required_irreversible_change": structure[8],
        "required_cost": structure[4],
        "must_not_resolve": ["无线电呼叫者的最终身份"],
        "profile_alignment": {
            "dimensions": [
                {
                    "dimension": dimension,
                    "alignment": "符合当前 Effective Profile",
                    "evidence": ["候选结构与本维度要求一致"],
                }
                for dimension, _, _ in PROFILE_DIMENSIONS
            ],
            "constraint_checks": [],
        },
        "canon_constraints": ["钥匙仍是生锈钥匙", "电量已经用于无线电"],
        "knowledge_constraints": ["林岚不知道呼叫者身份"],
        "forbidden_repetitions": ["再次只靠查看面板推进"],
        "commit_updates": ["thread_status", "resource_stock", "character_state"],
        "pressure_before": 70,
        "pressure_target_after": 55,
        "score_inputs": {
            "thread_need_fit": score,
            "pressure_curve_fit": score,
            "debt_utility": score,
            "progress_gain": score,
            "payoff_or_setup_utility": score,
            "agency_gain": score,
            "risk_fit": score,
            "structural_diversity": 0,
            "style_fit": 90,
            "repetition_fatigue": 10,
            "future_damage": 5,
        },
        "score_evidence": {
            key: [f"{key} 的合成证据：{thread_id}"]
            for key in (
                "thread_need_fit",
                "pressure_curve_fit",
                "debt_utility",
                "progress_gain",
                "payoff_or_setup_utility",
                "agency_gain",
                "risk_fit",
                "style_fit",
                "repetition_fatigue",
                "future_damage",
            )
        },
        "gate_input": {
            "character_fit_inputs": dict.fromkeys(character_keys, 90),
            "style_fit_inputs": dict.fromkeys(style_keys, 90),
        },
    }


def write_candidates(
    workspace: Path,
    task_id: str,
    candidates: list[dict[str, Any]],
) -> Path:
    path = workspace / "planning-book" / "agent_outputs" / task_id / "output.json"
    path.write_text(
        json.dumps(
            {"task_id": task_id, "candidates": candidates, "notes": []},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def enable_progression_kernel(database: Database, *, boundary: int) -> None:
    bundle = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "主角持续变强、突破阶段，并以能力、资源和世界扩张推进故事。",
            genre_hint="成长冒险",
            contract_prefix="planning-kernel",
        )
    )
    progression_payload = {
        "progression_contract_id": "planning-body-progression",
        "progression_subject": "CHARACTER",
        "primary_axis": {
            "axis_id": "body-axis",
            "name": "身体重塑",
            "axis_type": "BODY_EVOLUTION",
            "current_stage_schema": "定性身体阶段",
            "stage_order": ["tempered", "renewed"],
            "stage_definitions": [
                {
                    "stage_id": "tempered",
                    "name": "初次锻体",
                    "next_stage_candidates": ["renewed"],
                },
                {"stage_id": "renewed", "name": "生命重构"},
            ],
            "progress_measure": "正文证明的身体性质变化",
        },
        "topology": ["LINEAR"],
        "allowed_delta_types": ["ADVANCE"],
        "stage_model": "非数字生命阶段",
        "breakthrough_model": {
            "gates": [
                {
                    "gate_id": "body-gate",
                    "gate_type": "RESOURCE_GATE",
                    "requirement": "消耗已持有的边界钥匙",
                    "evidence_requirements": ["正文事件与资源变化"],
                    "required_resources": ["边界钥匙"],
                }
            ]
        },
        "ability_unlock_model": [],
        "resource_economy": ["边界钥匙"],
        "growth_costs": ["身体损伤"],
        "verification_modes": ["事件验证"],
        "next_ceiling_model": "更高生命层级",
        "upper_ceiling_visibility": "PARTIAL",
        "progression_promises": ["成长改变行动可能性"],
        "status": "NEEDS_REVIEW",
    }
    for contract_type, payload in (
        (ProgressionContractType.READER_EXPERIENCE, bundle.reader_experience),
        (ProgressionContractType.MARKET_CATEGORY, bundle.market_category),
        (ProgressionContractType.NARRATIVE_DRIVE, bundle.narrative_drive),
        (ProgressionContractType.GENRE, bundle.genre),
        (ProgressionContractType.PROGRESSION, progression_payload),
        (ProgressionContractType.WORLD_EXPANSION, bundle.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, bundle.payoff_channels),
    ):
        assert payload is not None
        proposal = create_contract_proposal(
            database,
            book_id="planning-book",
            edition_id="base",
            contract_type=contract_type,
            payload=payload,
            source="TEST_AUTHOR_PROPOSAL",
        )
        confirm_contract(
            database,
            proposal.contract_record_id,
            effective_from_boundary=boundary,
        )


def seed_progression_source_state(database: Database) -> None:
    with database.connect() as connection:
        chapter = connection.execute(
            "SELECT chapter_id, ordinal FROM chapters WHERE book_id='planning-book' "
            "ORDER BY ordinal DESC LIMIT 1"
        ).fetchone()
        assert chapter is not None
        span = connection.execute(
            "SELECT span_id FROM source_spans WHERE book_id='planning-book' "
            "AND chapter_id=? ORDER BY start_line LIMIT 1",
            (chapter["chapter_id"],),
        ).fetchone()
        assert span is not None
    common = {
        "book_id": "planning-book",
        "edition_id": "base",
        "chapter_id": str(chapter["chapter_id"]),
        "chapter_ordinal": int(chapter["ordinal"]),
        "source_span_ids": [str(span["span_id"])],
        "confidence": 1.0,
        "verification_status": SourceStateVerification.SOURCE_VERIFIED,
    }
    record_source_chapter_deltas(
        database,
        "planning-book",
        "base",
        [
            SourceChapterStateDelta(
                delta_id="planning-character-progression",
                category=SourceStateCategory.CHARACTER_STATE,
                operation=SourceStateOperation.ADD,
                subject_id="character:hero",
                statement="主角已处于初次锻体阶段，并已满足尝试下一阶段的条件。",
                payload={
                    "name": "主角",
                    "progression": {
                        "axis_id": "body-axis",
                        "stage_id": "tempered",
                        "readiness": "READY_TO_ATTEMPT",
                    },
                },
                **common,
            ),
            SourceChapterStateDelta(
                delta_id="planning-resource-boundary-key",
                category=SourceStateCategory.RESOURCE,
                operation=SourceStateOperation.ACQUIRE,
                subject_id="character:hero",
                object_id="resource:boundary-key",
                statement="主角持有一枚边界钥匙。",
                payload={
                    "name": "边界钥匙",
                    "owner_id": "character:hero",
                    "quantity": 1,
                },
                **common,
            ),
        ],
    )
    record_source_state_coverage(
        database,
        book_id="planning-book",
        edition_id="base",
        chapter_id=str(chapter["chapter_id"]),
        chapter_ordinal=int(chapter["ordinal"]),
        status=SourceStateCoverageStatus.COMPLETE_WITH_CHANGES,
        verified_delta_count=2,
    )


def test_boundary_candidate_ranking_and_contract(tmp_path: Path) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    boundary = build_boundary_packet(database, "planning-book", recent_full_chapters=2)
    task = prepare_candidate_task(database, "planning-book", settings)
    task_id = str(task["task_id"])
    thread_ids = [item["thread_id"] for item in task["top_threads"]]
    candidates = [
        candidate_payload("candidate-a", thread_ids[0], score=90, variant=0),
        candidate_payload("candidate-b", thread_ids[1], score=85, variant=1),
        candidate_payload("candidate-c", thread_ids[2], score=65, variant=2),
    ]
    candidates[0].update(
        {
            "reader_promise_alignment": [
                {
                    "promise_id": "promise-growth",
                    "priority": "CORE",
                    "service": "SERVED",
                    "evidence": ["维修资源转化改变了下一步行动可能性"],
                }
            ],
            "genre_alignment": ["生存成长中的资源转化"],
            "progress_preview": {
                "components": [
                    {
                        "component": component,
                        "value": 90,
                        "evidence": [f"{component} 的章节状态变化"],
                    }
                    for component in (
                        "permanent_growth",
                        "world_state_change",
                        "relationship_change",
                        "knowledge_change",
                        "goal_advance",
                        "strategy_expansion",
                    )
                ]
            },
            "progression_impact": {
                "axis_advanced": ["生存能力"],
                "progression_delta_type": ["CONVERT"],
                "resource_change": ["维修材料转化为防御能力"],
                "future_progression_space": ["稳定气象站后探索外部区域"],
            },
            "resource_opportunity_impact": ["回收已铺垫维修材料"],
            "chapter_intent": "RESOURCE_CONVERSION",
            "anticipation_impact": ["兑现材料用途"],
        }
    )
    for key in (
        "reader_promise_alignment",
        "genre_alignment",
        "progression_impact",
        "resource_opportunity_impact",
        "chapter_intent",
        "anticipation_impact",
    ):
        candidates[1][key] = deepcopy(candidates[0][key])
    candidates[1]["progress_preview"] = {
        "components": [
            {**component, "value": 85}
            for component in candidates[0]["progress_preview"]["components"]
        ]
    }
    output_path = write_candidates(workspace, task_id, candidates)

    planned = import_candidate_output(
        database, "planning-book", task_id, settings, output_path
    )
    contract = build_chapter_contract(
        database, "planning-book", str(planned["selected_candidate_id"])
    )

    assert Path(str(boundary["markdown_path"])).exists()
    packet = json.loads(Path(str(boundary["json_path"])).read_text(encoding="utf-8"))
    assert len(packet["recent_full_chapters"]) == 2
    assert packet["relevant_source_spans"]
    assert packet["relevant_source_spans"][0]["ordinal"] == 1
    assert set(
        [
            "canon_facts",
            "character_states",
            "knowledge_boundaries",
            "active_threads",
            "promises",
            "resources",
            "capabilities",
            "relationships",
            "recent_payoffs",
            "recent_structures",
            "style_profiles",
            "author_directives",
            "narrative_portfolio",
        ]
    ) <= packet.keys()
    assert packet["narrative_portfolio"]["snapshot_id"]
    assert packet["innovation_diagnostics"]["portfolio_snapshot"] == packet[
        "narrative_portfolio"
    ]
    assert len(planned["candidates"]) == 3
    assert len(planned["same_choice_band"]) == 2
    assert sum(item["selection_status"] == "SELECTED" for item in planned["candidates"]) == 1
    assert all(min(item["structural_difference_counts"]) >= 3 for item in planned["candidates"])
    selected = next(
        item for item in planned["candidates"] if item["selection_status"] == "SELECTED"
    )
    assert selected["innovation_reward_breakdown"]["genre_promise_reward"][
        "total_reward"
    ] > 0

    contract_data = json.loads(Path(str(contract["path"])).read_text(encoding="utf-8"))
    assert contract_data["chapter"] == 4
    assert len(contract_data["secondary_functions"]) <= 2
    assert contract_data["required_irreversible_change"]
    assert contract_data["required_cost"]
    assert contract_data["chapter_intent"] == "RESOURCE_CONVERSION"
    assert contract_data["progression_impact"]["resource_change"]
    assert contract_data["boundary_packet_id"] == task["boundary_packet_id"]
    assert len(task["effective_book_profile"]["dimensions"]) == 9
    assert (
        contract_data["effective_book_profile"]["profile_version_id"]
        == task["effective_book_profile"]["profile_version_id"]
    )

    with sqlite3.connect(database.path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM candidate_plans").fetchone()[0] == 3
        assert connection.execute("SELECT COUNT(*) FROM chapter_contracts").fetchone()[0] == 1


def test_effective_kernel_candidate_claims_are_verified_before_contract(
    tmp_path: Path,
) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    enable_progression_kernel(database, boundary=4)
    task = prepare_candidate_task(database, "planning-book", settings)
    task_id = str(task["task_id"])
    candidates = [
        candidate_payload("kernel-a", "station-defense", score=99, variant=0),
        candidate_payload("kernel-b", "radio-caller", score=75, variant=1),
        candidate_payload("kernel-c", "wind-rule", score=65, variant=2),
    ]
    candidates[0]["narrative_drive_alignment"] = {
        "primary_drive": "INVENTED_DRIVE",
        "drives_advanced": ["INVENTED_DRIVE"],
        "evidence": ["模型自报的驱动力"],
    }
    output = write_candidates(workspace, task_id, candidates)

    result = import_candidate_output(
        database, "planning-book", task_id, settings, output
    )
    rejected = next(item for item in result["candidates"] if item["local_id"] == "kernel-a")
    assert rejected["selection_status"] == "REJECTED"
    assert any("Narrative Drive 不属于" in item for item in rejected["hard_failures"])

    selected_id = str(result["selected_candidate_id"])
    with database.connect() as connection:
        row = connection.execute(
            "SELECT plan_json, score_json, gate_report_json FROM candidate_plans "
            "WHERE candidate_id=?",
            (selected_id,),
        ).fetchone()
    assert row is not None
    declared = json.loads(str(row["plan_json"]))
    score = json.loads(str(row["score_json"]))
    gate = json.loads(str(row["gate_report_json"]))
    compilation = score["kernel_evidence_compilation"]
    assert compilation["verified"]["drive_drift"]["status"] == "SOFT_MISS"
    assert score["inputs"]["progress_gain"] != declared["score_inputs"]["progress_gain"]
    assert gate["kernel_evidence"]["candidate_local_id"] in {"kernel-b", "kernel-c"}

    contract_result = build_chapter_contract(database, "planning-book", selected_id)
    contract = json.loads(
        Path(str(contract_result["path"])).read_text(encoding="utf-8")
    )
    assert contract["kernel_verification_status"] in {"COMPLETE", "PARTIAL"}
    assert contract["declared_kernel_trace"]
    assert contract["verified_kernel_trace"]["evidence_compilation"]
    assert contract["declared_kernel_trace"] != contract["verified_kernel_trace"]
    with database.connect() as connection:
        cards = _candidate_cards(
            connection,
            "planning-book",
            "base",
            context_chapter_id=None,
            context_chapter_ordinal=3,
        )
    selected_card = next(item for item in cards if item["candidate_id"] == selected_id)
    assert selected_card["kernel_trace"]["available"] is True
    assert selected_card["kernel_trace"]["completeness"] in {"COMPLETE", "PARTIAL"}
    assert selected_card["kernel_trace"]["declared"]
    assert selected_card["kernel_trace"]["verified"]


def test_candidate_output_rejects_renamed_same_structure(tmp_path: Path) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    task = prepare_candidate_task(database, "planning-book", settings)
    task_id = str(task["task_id"])
    base = candidate_payload("one", "station-defense", score=80, variant=0)
    renamed = deepcopy(base)
    renamed["local_id"] = "two"
    renamed["title"] = "换了标题"
    third = candidate_payload("three", "radio-caller", score=70, variant=1)
    output = write_candidates(workspace, task_id, [base, renamed, third])

    with pytest.raises(PlanningError, match="结构维度不同"):
        import_candidate_output(database, "planning-book", task_id, settings, output)


def test_hard_gate_rejected_candidate_is_preserved_with_reason(tmp_path: Path) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    task = prepare_candidate_task(database, "planning-book", settings)
    task_id = str(task["task_id"])
    candidates = [
        candidate_payload("one", "station-defense", score=80, variant=0),
        candidate_payload("two", "radio-caller", score=70, variant=1),
        candidate_payload("three", "wind-rule", score=90, variant=2),
    ]
    candidates[2]["gate_input"]["knowledge_violations"] = ["主角提前知道呼叫者身份"]
    output = write_candidates(workspace, task_id, candidates)

    result = import_candidate_output(database, "planning-book", task_id, settings, output)

    rejected = next(item for item in result["candidates"] if not item["passed"])
    assert rejected["selection_status"] == "REJECTED"
    assert rejected["score"] == 0
    assert rejected["hard_failures"] == ["主角提前知道呼叫者身份"]


def test_profile_must_constraint_is_a_hard_gate(tmp_path: Path) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    profile = edit_book_profile(
        database,
        "planning-book",
        "base",
        dimension="themes",
        operation=ProfileEditOperation.ADD,
        content="每次安全收益都必须伴随明确代价。",
        strength=ProfileStrength.MUST,
    )
    edit_id = profile["hard_constraints"]["must"][0]["edit_id"]
    task = prepare_candidate_task(database, "planning-book", settings)
    candidates = [
        candidate_payload("one", "station-defense", score=80, variant=0),
        candidate_payload("two", "radio-caller", score=70, variant=1),
        candidate_payload("three", "wind-rule", score=99, variant=2),
    ]
    for candidate in candidates:
        candidate["profile_alignment"]["constraint_checks"] = [
            {"edit_id": edit_id, "passed": True, "evidence": "代价已写入候选结构"}
        ]
    candidates[2]["profile_alignment"]["constraint_checks"][0] = {
        "edit_id": edit_id,
        "passed": False,
        "evidence": "候选提供无代价收益",
    }
    output = write_candidates(workspace, str(task["task_id"]), candidates)

    result = import_candidate_output(
        database, "planning-book", str(task["task_id"]), settings, output
    )

    rejected = next(item for item in result["candidates"] if item["local_id"] == "three")
    assert rejected["selection_status"] == "REJECTED"
    assert rejected["score"] == 0
    assert rejected["hard_failures"] == [
        f"Profile 硬约束未通过 {edit_id}：候选提供无代价收益"
    ]


def test_full_synthetic_e2e_from_ingest_to_approval(tmp_path: Path) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    source_path = tmp_path / "中文小说" / FIXTURE.name
    source_hash = sha256_file(source_path)
    directive = add_directive(
        database,
        "planning-book",
        directive_type="requirement",
        content="主角必须主动选择",
    )
    build_boundary_packet(database, "planning-book", recent_full_chapters=3)
    task = prepare_candidate_task(database, "planning-book", settings)
    task_id = str(task["task_id"])
    threads = [item["thread_id"] for item in task["top_threads"]]
    candidate_path = write_candidates(
        workspace,
        task_id,
        [
            candidate_payload("e2e-a", threads[0], score=90, variant=0),
            candidate_payload("e2e-b", threads[1], score=75, variant=1),
            candidate_payload("e2e-c", threads[2], score=65, variant=2),
        ],
    )
    planned = import_candidate_output(
        database, "planning-book", task_id, settings, candidate_path
    )
    contract_result = build_chapter_contract(
        database, "planning-book", str(planned["selected_candidate_id"])
    )
    contract = ChapterContract.model_validate_json(
        Path(str(contract_result["path"])).read_text(encoding="utf-8")
    )
    draft_task = prepare_draft_task(database, "planning-book", contract.contract_id)
    draft_task_id = str(draft_task["task_id"])
    prose = "\n".join(
        [
            contract.required_irreversible_change,
            contract.required_cost,
            contract.ending_state,
            "线程状态完成更新，主角目标随之改变。",
            "资源库存完成更新，三份维修材料被正式登记。",
            "人物状态完成更新，他决定先加固机械门。",
        ]
    )
    draft_output = {
        "task_id": draft_task_id,
        "contract_id": contract.contract_id,
        "chapter_title": "合成端到端章节",
        "prose_markdown": prose,
        "state_changes": [
            {
                "kind": "thread",
                "record_id": contract.primary_thread,
                "payload": {
                    "goal": "守住气象站",
                    "stakes": "失守将失去安全据点",
                    "phase": "advanced",
                    "importance": 0.9,
                    "reader_visibility": 0.9,
                    "progress": 0.85,
                },
                "evidence_quotes": ["线程状态完成更新"],
            },
            {
                "kind": "resource",
                "record_id": "resource_repair_material",
                "payload": {
                    "owner_id": "hero",
                    "name": "维修材料",
                    "before_quantity": 0,
                    "delta": 3,
                    "after_quantity": 3,
                    "unit": "份",
                    "source": "气象站储物柜",
                },
                "evidence_quotes": ["三份维修材料被正式登记"],
            },
            {
                "kind": "character_state",
                "record_id": "state_hero_e2e",
                "payload": {
                    "character_id": "hero",
                    "goals": ["加固机械门"],
                    "plans": ["先修门再监听无线电"],
                },
                "evidence_quotes": ["他决定先加固机械门"],
            },
        ],
        "contract_evidence": {
            "required_irreversible_change": [contract.required_irreversible_change],
            "required_cost": [contract.required_cost],
            "ending_state": [contract.ending_state],
            "commit:thread_status": ["线程状态完成更新"],
            "commit:resource_stock": ["资源库存完成更新"],
            "commit:character_state": ["人物状态完成更新"],
        },
        "knowledge_claims": [],
        "character_fit_inputs": dict.fromkeys(
            settings.metrics["character_fit"]["weights"], 90
        ),
        "style_fit_inputs": dict.fromkeys(
            settings.metrics["style_fit"]["weights"], 90
        ),
        "character_bottom_line_violations": [],
        "style_boundary_violations": [],
        "promises_advanced": [contract.primary_thread],
        "promises_paid": [],
        "new_major_hooks": 0,
        "structure_tags": ["station-defense-repair"],
        "notes": ["固定合成 agent output，不调用远程模型"],
    }
    output_path = Path(str(draft_task["expected_output"]))
    output_path.write_text(json_dumps(draft_output, indent=2), encoding="utf-8")
    imported = import_draft_output(database, "planning-book", draft_task_id)
    draft_id = str(imported["draft_id"])
    assert validate_draft(database, "planning-book", draft_id, settings).passed
    committed = approve_draft(
        database,
        "planning-book",
        draft_id,
        confirmation="批准写入正史",
    )
    projection = rebuild_projection(database, "planning-book", persist=False)
    exported = export_book(database, "planning-book")
    next_boundary = build_boundary_packet(
        database, "planning-book", recent_full_chapters=3
    )
    next_packet = json.loads(
        Path(str(next_boundary["json_path"])).read_text(encoding="utf-8")
    )
    with database.connect() as connection:
        directive_status = connection.execute(
            "SELECT status FROM author_directives WHERE directive_id=?",
            (directive["directive_id"],),
        ).fetchone()[0]
        profile_proposal = connection.execute(
            "SELECT source_type, status FROM book_profile_refresh_proposals "
            "WHERE book_id='planning-book' ORDER BY created_at DESC LIMIT 1"
        ).fetchone()

    assert committed["status"] == "CANON_COMMITTED"
    assert tuple(profile_proposal) == ("CANON_COMMIT", "PENDING")
    assert directive_status == "CONSUMED"
    assert next_packet["author_directives"] == []
    assert "合成端到端章节" in next_packet["recent_full_chapters"][-1]["heading"]
    assert projection.committed_chapters
    assert contract.primary_thread in projection.threads
    assert Path(str(exported["manifest"])).is_file()
    assert sha256_file(source_path) == source_hash


def test_verified_kernel_trace_closes_through_approval_and_next_state(
    tmp_path: Path,
) -> None:
    database, workspace, settings = setup_planning_book(tmp_path)
    enable_progression_kernel(database, boundary=3)
    seed_progression_source_state(database)

    task = prepare_candidate_task(database, "planning-book", settings)
    old_aggregate_id = str(task["aggregate_id"])
    initial_kernel = json.loads(
        Path(str(task["kernel_context"])).read_text(encoding="utf-8")
    )
    assert initial_kernel["chapter_state"]["progression_state"][
        "primary_axis_state"
    ]["current_stage"] == "tempered"
    assert "边界钥匙" in initial_kernel["chapter_state"]["progression_state"][
        "available_resources"
    ]
    candidates = [
        candidate_payload("kernel-e2e-a", "station-defense", score=90, variant=0),
        candidate_payload("kernel-e2e-b", "radio-caller", score=75, variant=1),
        candidate_payload("kernel-e2e-c", "wind-rule", score=65, variant=2),
    ]
    candidates[0].update(
        {
            "reader_promise_alignment": [
                {
                    "promise_id": "continuous-growth",
                    "priority": "CORE",
                    "service": "SERVED",
                    "evidence": ["身体阶段从 tempered 进入 renewed"],
                }
            ],
            "narrative_drive_alignment": {
                "primary_drive": "POWER_PROGRESSION",
                "primary_drive_effect": "身体阶段改变可执行行动",
                "drives_advanced": ["POWER_PROGRESSION"],
                "evidence": ["tempered -> renewed"],
            },
            "progression_impact": {
                "axis_advanced": ["body-axis"],
                "progression_delta_type": ["ADVANCE"],
                "stage_change": "tempered -> renewed",
                "resource_change": ["消耗边界钥匙"],
                "growth_cost": ["身体损伤"],
            },
            "resource_opportunity_impact": ["消耗边界钥匙"],
            "chapter_intent": "BREAKTHROUGH",
            "scheduler_alignment": {
                "candidate_primary_intent": "BREAKTHROUGH",
                "alignment": "ACCEPTED",
            },
        }
    )
    candidate_path = write_candidates(
        workspace, str(task["task_id"]), candidates
    )
    planned = import_candidate_output(
        database,
        "planning-book",
        str(task["task_id"]),
        settings,
        candidate_path,
    )
    selected = next(
        item for item in planned["candidates"] if item["selection_status"] == "SELECTED"
    )
    assert selected["local_id"] == "kernel-e2e-a"
    contract_result = build_chapter_contract(
        database, "planning-book", str(planned["selected_candidate_id"])
    )
    contract = ChapterContract.model_validate_json(
        Path(str(contract_result["path"])).read_text(encoding="utf-8")
    )
    assert contract.declared_kernel_trace
    assert contract.verified_kernel_trace["progression_impact"]["stage_change"] == {
        "from": "tempered",
        "to": "renewed",
    }

    draft_task = prepare_draft_task(database, "planning-book", contract.contract_id)
    prose = "\n".join(
        [
            contract.required_irreversible_change,
            contract.required_cost,
            contract.ending_state,
            "线程状态完成更新，防守承诺向前推进。",
            "边界钥匙在重塑中彻底碎裂。",
            "他的旧躯壳崩解，身体阶段进入 renewed。",
            "人物状态完成更新，新的身体改变了行动边界。",
            "资源库存完成更新，钥匙余量归零。",
        ]
    )
    draft_output = {
        "task_id": draft_task["task_id"],
        "contract_id": contract.contract_id,
        "chapter_title": "身体重塑",
        "prose_markdown": prose,
        "state_changes": [
            {
                "kind": "thread",
                "record_id": contract.primary_thread,
                "payload": {
                    "goal": "守住气象站",
                    "stakes": "失守将失去安全据点",
                    "phase": "advanced",
                    "importance": 0.9,
                    "reader_visibility": 0.9,
                    "progress": 0.85,
                },
                "evidence_quotes": ["线程状态完成更新"],
            },
            {
                "kind": "resource",
                "record_id": "resource_boundary_key",
                "payload": {
                    "owner_id": "character:hero",
                    "name": "边界钥匙",
                    "before_quantity": 1,
                    "delta": -1,
                    "after_quantity": 0,
                    "unit": "枚",
                    "causal_source": "身体重塑消耗",
                },
                "evidence_quotes": ["边界钥匙在重塑中彻底碎裂"],
            },
            {
                "kind": "character_state",
                "record_id": "state_hero_renewed",
                "payload": {
                    "character_id": "character:hero",
                    "goals": ["验证重塑后的行动边界"],
                    "plans": ["先稳定新身体"],
                    "progression": {
                        "axis_id": "body-axis",
                        "stage_id": "renewed",
                        "readiness": "ACCUMULATING",
                    },
                },
                "evidence_quotes": ["身体阶段进入 renewed"],
            },
        ],
        "contract_evidence": {
            "required_irreversible_change": [contract.required_irreversible_change],
            "required_cost": [contract.required_cost],
            "ending_state": [contract.ending_state],
            "commit:thread_status": ["线程状态完成更新"],
            "commit:resource_stock": ["资源库存完成更新"],
            "commit:character_state": ["人物状态完成更新"],
        },
        "knowledge_claims": [],
        "character_fit_inputs": dict.fromkeys(
            settings.metrics["character_fit"]["weights"], 90
        ),
        "style_fit_inputs": dict.fromkeys(
            settings.metrics["style_fit"]["weights"], 90
        ),
        "promises_advanced": [contract.primary_thread],
        "promises_paid": [],
        "new_major_hooks": 0,
        "structure_tags": ["kernel-stage-transition"],
        "realized_kernel_trace": {
            "expected_contract_id": contract.contract_id,
            "primary_intent": "BREAKTHROUGH",
            "reader_promises_served": ["continuous-growth"],
            "narrative_drives_advanced": ["POWER_PROGRESSION"],
            "progression_impact": {
                "axis_advanced": ["body-axis"],
                "progression_delta_type": ["ADVANCE"],
                "stage_change": "tempered -> renewed",
                "resource_change": ["消耗边界钥匙"],
                "growth_cost": ["身体损伤"],
            },
            "resource_changes": ["消耗边界钥匙"],
            "evidence": [
                {
                    "claim": "body-axis tempered -> renewed",
                    "state_change_record_ids": [
                        "resource_boundary_key",
                        "state_hero_renewed",
                    ],
                    "evidence_quotes": [
                        "边界钥匙在重塑中彻底碎裂",
                        "身体阶段进入 renewed",
                    ],
                }
            ],
        },
        "notes": ["原创合成生产闭环证据"],
    }
    output_path = Path(str(draft_task["expected_output"]))
    output_path.write_text(json_dumps(draft_output, indent=2), encoding="utf-8")
    imported = import_draft_output(
        database, "planning-book", str(draft_task["task_id"])
    )
    draft_id = str(imported["draft_id"])
    validation = validate_draft(database, "planning-book", draft_id, settings)
    assert validation.passed
    comparison = next(
        report for report in validation.reports if report.validator == "Contract Validator"
    ).measurements["kernel_trace_comparison"]
    assert comparison["unexpected"] == {}
    assert comparison["underdelivered"] == {}
    before_approval = build_story_game_state(database, "planning-book", "base")
    assert before_approval["progression_state"]["primary_axis_state"][
        "current_stage"
    ] == "tempered"

    approve_draft(database, "planning-book", draft_id, confirmation="批准写入正史")
    with database.connect() as connection:
        committed_chapter = connection.execute(
            "SELECT chapter_id FROM canon_commits WHERE draft_id=?", (draft_id,)
        ).fetchone()
        old_aggregate = connection.execute(
            "SELECT status FROM planning_aggregates WHERE aggregate_id=?",
            (old_aggregate_id,),
        ).fetchone()
    assert committed_chapter is not None
    assert old_aggregate["status"] == "STALE"
    after = build_story_game_state(
        database,
        "planning-book",
        "base",
        chapter_id=str(committed_chapter["chapter_id"]),
    )
    assert after["progression_state"]["primary_axis_state"]["current_stage"] == (
        "renewed"
    )
    assert after["progression_state"]["recent_breakthrough"]["stage_id"] == (
        "renewed"
    )
    next_task = prepare_candidate_task(database, "planning-book", settings)
    assert next_task["aggregate_id"] != old_aggregate_id
    next_kernel = json.loads(
        Path(str(next_task["kernel_context"])).read_text(encoding="utf-8")
    )
    assert next_kernel["chapter_state"]["progression_state"]["primary_axis_state"][
        "current_stage"
    ] == "renewed"
