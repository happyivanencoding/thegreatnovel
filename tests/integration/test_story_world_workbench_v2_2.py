from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.author_control.book_profile import (
    PROFILE_DIMENSIONS,
    ProfileEditOperation,
    ProfileStrength,
    create_book_profile_refresh_proposal,
    edit_book_profile,
    load_effective_book_profile,
    resolve_book_profile_refresh_proposal,
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
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.edition import create_edition
from novel_authoring.ingest.service import ingest_book
from novel_authoring.planning.candidates import prepare_handoff_candidate_task
from novel_authoring.web.app import create_app
from novel_authoring.workflows.handoffs import claim_handoff


def _v22_book(
    tmp_path: Path, *, chapter_count: int = 23
) -> tuple[Database, list[dict[str, object]]]:
    source = tmp_path / "source"
    source.mkdir()
    source_text = "\n\n".join(
        f"第{ordinal}章 边界{ordinal}\n\n这是第{ordinal}章的原文，只描述本章可见事实。"
        for ordinal in range(1, chapter_count + 1)
    )
    (source / "story.md").write_text(source_text, encoding="utf-8")
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="story-world-v22",
        title="Story World Workbench V2.2 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "story-world-v22" / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = [
            dict(row)
            for row in connection.execute(
                "SELECT chapter_id, ordinal, title FROM chapters "
                "WHERE book_id='story-world-v22' ORDER BY ordinal"
            ).fetchall()
        ]
        spans = {
            str(row["chapter_id"]): str(row["span_id"])
            for row in connection.execute(
                "SELECT chapter_id, MIN(span_id) AS span_id FROM source_spans "
                "WHERE book_id='story-world-v22' AND chapter_id IS NOT NULL "
                "GROUP BY chapter_id"
            ).fetchall()
        }
    character_delta = SourceChapterStateDelta(
        delta_id="v22-character-hero",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[0]["chapter_id"]),
        chapter_ordinal=1,
        category=SourceStateCategory.CHARACTER_STATE,
        operation=SourceStateOperation.ADD,
        subject_id="character:hero",
        statement="主角在第一章登场。",
        source_span_ids=[spans[str(chapters[0]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "主角", "current_location": "边界一"},
    )
    item_delta = SourceChapterStateDelta(
        delta_id="v22-item-key",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ACQUIRE,
        subject_id="character:hero",
        object_id="item:boundary-key",
        statement="主角在第二章取得边界钥匙。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={
            "name": "边界钥匙",
            "owner_id": "character:hero",
            "quantity": 1,
        },
    )
    character_update = SourceChapterStateDelta(
        delta_id="v22-character-hero-update",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.CHARACTER_STATE,
        operation=SourceStateOperation.UPDATE,
        subject_id="character:hero",
        statement="主角击败临时目标后更新经验。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "临时目标", "experience": 1},
    )
    relationship_delta = SourceChapterStateDelta(
        delta_id="v22-relationship-ally",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.RELATIONSHIP,
        operation=SourceStateOperation.RELATIONSHIP_CHANGE,
        subject_id="character:hero",
        object_id="hero-ally-cooperation",
        statement="主角与盟友建立一次有条件合作。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={
            "counterparty_id": "character:ally",
            "relationship_state": "CONDITIONAL_COOPERATION",
        },
    )
    ability_delta = SourceChapterStateDelta(
        delta_id="v22-ability-observe",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[0]["chapter_id"]),
        chapter_ordinal=1,
        category=SourceStateCategory.CAPABILITY,
        operation=SourceStateOperation.LEARN,
        subject_id="character:hero",
        object_id="capability:observe-boundary",
        statement="主角学会观察边界。",
        source_span_ids=[spans[str(chapters[0]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "观察边界", "owner_id": "character:hero"},
    )
    record_source_chapter_deltas(
        database,
        "story-world-v22",
        "base",
        [
            character_delta,
            item_delta,
            ability_delta,
            character_update,
            relationship_delta,
        ],
    )
    for chapter, status, count in (
        (chapters[0], SourceStateCoverageStatus.COMPLETE_WITH_CHANGES, 2),
        (chapters[1], SourceStateCoverageStatus.COMPLETE_WITH_CHANGES, 3),
        (chapters[2], SourceStateCoverageStatus.COMPLETE_NO_CHANGE, 0),
    ):
        record_source_state_coverage(
            database,
            book_id="story-world-v22",
            edition_id="base",
            chapter_id=str(chapter["chapter_id"]),
            chapter_ordinal=int(chapter["ordinal"]),
            status=status,
            verified_delta_count=count,
        )
    return database, chapters


def test_chapter_world_state_separates_coverage_delta_and_future_facts(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path)

    chapter_one = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[0]["chapter_id"]),
        character_id="character:hero",
    )
    chapter_two = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[1]["chapter_id"]),
        character_id="character:hero",
    )
    chapter_three = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[2]["chapter_id"]),
        character_id="character:hero",
    )

    assert chapter_one["view"] == "AFTER_CHAPTER"
    assert chapter_one["selected_character_id"] == "character:hero"
    assert chapter_one["characters"][0]["name"] == "主角"
    assert "边界钥匙" not in json.dumps(chapter_one, ensure_ascii=False)
    assert any(item["name"] == "观察边界" for item in chapter_one["abilities"])
    assert any(item["name"] == "边界钥匙" for item in chapter_two["inventory"])
    assert chapter_two["characters"][0]["name"] == "主角"
    relationship_edge = chapter_two["relationship_graph"]["edges"][0]
    assert relationship_edge["from_id"] == "character:hero"
    assert relationship_edge["to_id"] == "character:ally"
    assert relationship_edge["label"] == "hero-ally-cooperation"
    assert relationship_edge["layer"] == "SOURCE_VERIFIED"
    assert chapter_three["availability"] == "SOURCE_CHAPTER_STATE_PROJECTION"
    assert chapter_three["coverage_status"] == "COMPLETE_NO_CHANGE"
    assert chapter_three["state_changed"] is False
    assert chapter_three["chapter_delta"]["confirmed"] == []
    assert chapter_three["coverage_summary"] == {
        "total": 23,
        "analyzed": 3,
        "with_changes": 2,
        "no_changes": 1,
        "ready": 0,
        "running": 0,
        "partial": 0,
        "failed": 0,
        "not_started": 20,
        "percentage": 13.0,
    }


def test_completed_zero_delta_chapter_is_not_requeued_and_batch_is_chunked(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path)
    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    endpoint = "/api/books/story-world-v22/editions/base/author-commands"
    headers = {"X-CSRF-Token": app.state.csrf_token}

    single = client.post(
        endpoint,
        headers=headers,
        json={
            "command_type": "REQUEST_SOURCE_STATE_HYDRATION",
            "chapter_id": str(chapters[2]["chapter_id"]),
        },
    )
    assert single.status_code == 200
    assert single.json()["code"] == "SOURCE_STATE_HYDRATION_ALREADY_COMPLETE"
    assert single.json()["handoff"] is None

    batch = client.post(
        endpoint,
        headers=headers,
        json={
            "command_type": "REQUEST_SOURCE_STATE_BATCH_HYDRATION",
            "payload": {"start_ordinal": 1, "end_ordinal": 23, "chunk_size": 15},
        },
    )
    assert batch.status_code == 200
    handoff = batch.json()["handoff"]
    assert [len(chunk) for chunk in handoff["chunks"]] == [15, 5]
    assert len(handoff["skipped"]) == 3
    assert all(
        entry["handoff"]["status"] == "READY_FOR_CODEX"
        for chunk in handoff["chunks"]
        for entry in chunk
    )
    first_handoff = handoff["chunks"][0][0]["handoff"]
    task_directory = Path(first_handoff["task_directory"])
    schema_path = task_directory / "input" / "output_schema.json"
    if not schema_path.is_file():
        schema_path = task_directory / "output_schema.json"
    hydration_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "SourceChapterStateDelta" in hydration_schema["$defs"]
    assert hydration_schema["properties"]["deltas"]["items"] == {
        "$ref": "#/$defs/SourceChapterStateDelta"
    }
    with database.connect() as connection:
        ready = connection.execute(
            "SELECT COUNT(*) FROM source_state_chapter_coverage "
            "WHERE book_id='story-world-v22' AND edition_id='base' "
            "AND status='READY_FOR_CODEX'"
        ).fetchone()[0]
    assert ready == 20


def test_global_book_profile_versions_are_edition_aware_and_author_controlled(
    tmp_path: Path,
) -> None:
    database, _chapters = _v22_book(tmp_path, chapter_count=3)
    base = edit_book_profile(
        database,
        "story-world-v22",
        "base",
        dimension="worldbuilding",
        operation=ProfileEditOperation.ADD,
        content="世界规则必须通过角色可见代价呈现。",
        strength=ProfileStrength.MUST,
        reason="作者确认世界观约束",
    )
    assert len(base["dimensions"]) == len(PROFILE_DIMENSIONS) == 9
    assert base["version_number"] == 1
    assert base["hard_constraints"]["must"][0]["content"].startswith("世界规则")

    create_edition(database, "story-world-v22", "revision-a", "改写 A")
    inherited = load_effective_book_profile(database, "story-world-v22", "revision-a")
    assert inherited["inherited_from_edition_id"] == "base"
    assert "世界规则必须" in next(
        item["content"]
        for item in inherited["dimensions"]
        if item["dimension"] == "worldbuilding"
    )
    edit_book_profile(
        database,
        "story-world-v22",
        "revision-a",
        dimension="style",
        operation=ProfileEditOperation.ADD,
        content="改写版采用更紧凑的短句。",
        strength=ProfileStrength.PREFER,
    )
    unchanged_base = load_effective_book_profile(database, "story-world-v22", "base")
    assert "改写版采用" not in next(
        item["content"]
        for item in unchanged_base["dimensions"]
        if item["dimension"] == "style"
    )

    proposed_baseline = deepcopy(unchanged_base["baseline"])
    proposed_baseline["themes"]["content"] = "生存选择必须留下伦理余波。"
    proposal = create_book_profile_refresh_proposal(
        database,
        "story-world-v22",
        "base",
        source_type="MAJOR_ARC_COMPLETE",
        proposed_baseline=proposed_baseline,
        summary="大弧结束后的画像刷新建议",
    )
    pending = load_effective_book_profile(database, "story-world-v22", "base")
    assert pending["version_number"] == 1
    assert pending["proposals"][0]["status"] == "PENDING"
    accepted = resolve_book_profile_refresh_proposal(
        database,
        "story-world-v22",
        "base",
        proposal["proposal_id"],
        action="ACCEPT",
    )
    assert accepted["version_number"] == 2
    assert accepted["author_edits"] == unchanged_base["author_edits"]
    assert accepted["history"][0]["reason"].startswith("接受 Profile proposal")


def test_workflow_goal_is_frozen_before_handoff_candidate_task(tmp_path: Path) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO rhythm_diagnostic_snapshots(
                snapshot_id, book_id, edition_id, as_of_chapter, as_of_event_seq,
                projection_hash, config_hash, analyzer_versions_json, snapshot_json, created_at
            ) VALUES ('v22-rhythm', 'story-world-v22', 'base', 3, 0,
                      'projection', 'config', '{}', '{}', 'now')
            """
        )
    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    response = client.post(
        "/api/books/story-world-v22/handoffs/continuation",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={
            "edition_id": "base",
            "context_chapter_id": str(chapters[-1]["chapter_id"]),
            "requested_stage": "PLAN_ONLY",
            "author_goal": "推进钥匙线，并让资源代价可见。",
        },
    )
    assert response.status_code == 200
    handoff = response.json()
    intent_id = handoff["author_intent"]["intent_id"]
    with database.connect() as connection:
        row = connection.execute(
            "SELECT planning_aggregate_id FROM workflow_handoffs WHERE handoff_id=?",
            (handoff["handoff_id"],),
        ).fetchone()
        assert row is not None
        aggregate = connection.execute(
            "SELECT author_policy_json FROM planning_aggregates WHERE aggregate_id=?",
            (row["planning_aggregate_id"],),
        ).fetchone()
    assert aggregate is not None
    policy = json.loads(str(aggregate["author_policy_json"]))
    assert intent_id in {
        item["intent_id"] for item in policy["author_control"]["intents"]
    }

    claim_handoff(database, handoff["handoff_id"], "v22-test")
    prepared = prepare_handoff_candidate_task(
        database, "story-world-v22", handoff["handoff_id"]
    )
    task = json.loads(Path(str(prepared["task"])).read_text(encoding="utf-8"))
    assert task["author_goal"] == "推进钥匙线，并让资源代价可见。"
    assert intent_id in {
        item["intent_id"] for item in task["author_control"]["intents"]
    }
    assert len(task["effective_book_profile"]["dimensions"]) == 9
    assert Path(str(prepared["source_state_context"])).is_file()


def test_v22_workbench_renders_matrix_inspector_modal_and_stable_explorer(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    app = create_app(database, book_id="story-world-v22")
    page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=knowledge&chapter_id={chapters[1]['chapter_id']}"
        "&character_id=character:hero"
    )
    assert page.status_code == 200
    assert 'data-explorer-section="world-state"' in page.text
    assert 'class="wb-knowledge-table"' in page.text
    assert "人物 × 知识主题" in page.text
    assert "data-wb-inspector" in page.text
    assert "Who Knows" in page.text
    assert "这件物品属于哪一层？" in page.text
    assert "按全书批量准备状态任务" not in page.text

    zero_delta_page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=overview&chapter_id={chapters[2]['chapter_id']}"
        "&character_id=character:hero"
    )
    assert zero_delta_page.status_code == 200
    assert "已分析 · 无确认变化" in zero_delta_page.text
    assert "本章状态已分析，没有确认状态变化" in zero_delta_page.text
    assert "准备本章状态任务" not in zero_delta_page.text

    profile = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench?mode=analysis&node=worldbuilding"
    )
    assert profile.status_code == 200
    assert "全书画像 · 当前有效版本" in profile.text
    assert profile.text.count("data-profile-edit-form") == 1
    workbench_js_path = (
        Path(__file__).parents[2]
        / "src"
        / "novel_authoring"
        / "web"
        / "static"
        / "workbench.js"
    )
    workbench_js = workbench_js_path.read_text(encoding="utf-8")
    legacy_js = workbench_js_path.with_name("app.js").read_text(encoding="utf-8")
    assert "scrollIntoView" not in workbench_js
    assert "scrollIntoView" not in legacy_js
