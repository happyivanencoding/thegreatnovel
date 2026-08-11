from __future__ import annotations

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
from novel_authoring.original.models import OriginalBootstrapProposal
from novel_authoring.original.service import (
    OriginalWorkflowError,
    approve_original_first_chapter,
    compare_original_proposals,
    confirm_original_foundation,
    create_original_book,
    import_original_bootstrap_proposal,
    prepare_original_bootstrap,
    resolve_original_proposal_version,
    select_first_chapter_candidate,
    validate_original_draft,
)
from novel_authoring.planning.models import ChapterContract
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookKind, BookRegistry, CreationMode
from novel_authoring.utils import json_dumps
from novel_authoring.web.app import create_app
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    claim_handoff,
    create_continuation_handoff,
    get_handoff,
    update_handoff_status,
)

BOOK_ID = "original-test"


def proposal_payload() -> dict[str, Any]:
    return {
        "schema_version": "original-bootstrap-v2",
        "information_status": "PROPOSAL",
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


def complete_bootstrap_handoff(database: Database) -> str:
    handoff_id = str(prepare_original_bootstrap(database, BOOK_ID)["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    proposal = OriginalBootstrapProposal.model_validate(proposal_payload())
    artifact = (
        Path(str(handoff["task_directory"])) / "artifacts" / "story_foundation" / "proposal.json"
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
        "requested_stage": "ORIGINAL_BOOK_BOOTSTRAP",
        "completed_stage": "FOUNDATION_PROPOSED",
        "book_id": BOOK_ID,
        "edition_id": "base",
        "status": "COMPLETED",
        "task_ids": [],
        "candidate_ids": [
            item["candidate_id"] for item in proposal_payload()["foundation_candidates"]
        ],
        "selected_candidate_id": None,
        "contract_id": None,
        "draft_id": None,
        "campaign_id": None,
        "revision_unit_ids": [],
        "artifact_paths": ["artifacts/story_foundation/proposal.json"],
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
    catalog = build_library_catalog(layout, tmp_path / "book")

    assert record.book_kind is BookKind.AUTHOR
    assert record.creation_mode is CreationMode.ORIGINAL
    assert tuple(counts) == (0, 0, 1)
    assert len(catalog.entries) == 1
    assert catalog.entries[0].href == f"/books/{BOOK_ID}/original"
    assert studio_access(layout, record).access_level.value == "ONBOARDING"


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

    assert before == (0, 0, 0)
    assert after[0] >= 6
    assert after[1:] == (0, 0)
    assert {row["horizon"] for row in intents} == {"SHORT", "MID", "LONG"}
    accepted = Path(str(result["accepted_path"])).read_text(encoding="utf-8")
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
        original = client.get(created.json()["original_url"])
        created_payload = created.json()
        handoff_id = str(created_payload["handoff"]["handoff_id"])
        book_id = str(created_payload["book_id"])
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
    assert "AI 任务" in original.text
    assert instruction.status_code == 200
    assert instruction.json()["instruction"]
    assert f'data-copy-instruction="{instruction_url}"' in original.text
    assert f'href="/api/handoffs/{handoff_id}/instruction"' not in original.text
