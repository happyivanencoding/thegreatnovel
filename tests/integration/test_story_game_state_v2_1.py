from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.author_control.source_state import (
    SourceChapterStateDelta,
    SourceStateCategory,
    SourceStateOperation,
    SourceStateVerification,
    build_source_state_projection,
    record_source_chapter_deltas,
)
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.web.app import create_app
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    claim_handoff,
    get_handoff,
    update_handoff_status,
    validate_result_file,
)


def _four_chapter_book(tmp_path: Path) -> tuple[Database, list[str], list[str]]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "story.md").write_text(
        "第1章 起点\n\n海风从门缝里吹进来。\n\n"
        "第2章 交换\n\n两个人在仓库里交换了物资。\n\n"
        "第3章 装备\n\n旧武器被重新装配。\n\n"
        "第4章 新局面\n\n队伍继续向前。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="story-game-state-v2-1",
        title="Story Game State V2.1 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "story-game-state-v2-1" / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = connection.execute(
            "SELECT chapter_id, ordinal FROM chapters "
            "WHERE book_id=? ORDER BY ordinal",
            ("story-game-state-v2-1",),
        ).fetchall()
        spans = connection.execute(
            "SELECT chapter_id, span_id FROM source_spans "
            "WHERE book_id=? ORDER BY chapter_id, span_id",
            ("story-game-state-v2-1",),
        ).fetchall()
    chapter_ids = [str(row["chapter_id"]) for row in chapters]
    span_by_chapter = {str(row["chapter_id"]): str(row["span_id"]) for row in spans}
    return database, chapter_ids, [span_by_chapter[chapter_id] for chapter_id in chapter_ids]


def _hydration_book(tmp_path: Path) -> tuple[Database, list[str], list[str]]:
    source = tmp_path / "hydration-source"
    source.mkdir()
    (source / "story.md").write_text(
        "第1章 灯塔\n\n海风把旧门吹开。\n\n"
        "第2章 潮声\n\n潮声从远处传来。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "hydration-workspace"
    ingest_book(
        book_id="story-game-state-v2",
        title="Story Game State V2.1 hydration 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "story-game-state-v2" / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = connection.execute(
            "SELECT chapter_id, ordinal FROM chapters "
            "WHERE book_id=? ORDER BY ordinal",
            ("story-game-state-v2",),
        ).fetchall()
        spans = connection.execute(
            "SELECT chapter_id, span_id FROM source_spans "
            "WHERE book_id=? ORDER BY chapter_id, span_id",
            ("story-game-state-v2",),
        ).fetchall()
    chapter_ids = [str(row["chapter_id"]) for row in chapters]
    span_by_chapter = {str(row["chapter_id"]): str(row["span_id"]) for row in spans}
    return database, chapter_ids, [span_by_chapter[chapter_id] for chapter_id in chapter_ids]


def _verified_delta(
    chapter_id: str,
    chapter_ordinal: int,
    span_id: str,
    *,
    category: SourceStateCategory,
    operation: SourceStateOperation,
    subject_id: str,
    object_id: str | None = None,
    payload: dict[str, object] | None = None,
    statement: str = "本章确认了状态变化。",
) -> SourceChapterStateDelta:
    return SourceChapterStateDelta(
        book_id="story-game-state-v2-1",
        edition_id="base",
        chapter_id=chapter_id,
        chapter_ordinal=chapter_ordinal,
        category=category,
        operation=operation,
        subject_id=subject_id,
        object_id=object_id,
        statement=statement,
        source_span_ids=[span_id],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload=payload or {},
    )


def test_source_state_replay_preserves_objects_and_operation_semantics(tmp_path: Path) -> None:
    database, chapter_ids, spans = _four_chapter_book(tmp_path)
    su = "character:su-mu"
    lin = "character:lin-yu-wei"
    deltas = [
        _verified_delta(
            chapter_ids[0],
            1,
            spans[0],
            category=SourceStateCategory.ITEM,
            operation=SourceStateOperation.ADD,
            subject_id=su,
            object_id="item-a",
            payload={"name": "物品 A", "quantity": 1},
        ),
        _verified_delta(
            chapter_ids[0],
            1,
            spans[0],
            category=SourceStateCategory.ITEM,
            operation=SourceStateOperation.ADD,
            subject_id=su,
            object_id="item-b",
            payload={"name": "物品 B", "quantity": 2},
        ),
        _verified_delta(
            chapter_ids[0],
            1,
            spans[0],
            category=SourceStateCategory.ITEM,
            operation=SourceStateOperation.ADD,
            subject_id=su,
            object_id="item-c",
            payload={"name": "物品 C", "quantity": 3},
        ),
    ]
    for index in range(3):
        deltas.append(
            _verified_delta(
                chapter_ids[0],
                1,
                spans[0],
                category=SourceStateCategory.CAPABILITY,
                operation=SourceStateOperation.ADD,
                subject_id=su,
                object_id=f"capability-{index}",
                payload={"name": f"能力 {index}"},
            )
        )
    deltas.extend(
        [
            _verified_delta(
                chapter_ids[1],
                2,
                spans[1],
                category=SourceStateCategory.ITEM,
                operation=SourceStateOperation.LOSE,
                subject_id=su,
                object_id="item-b",
                statement="物品 B 已经消耗。",
            ),
            _verified_delta(
                chapter_ids[1],
                2,
                spans[1],
                category=SourceStateCategory.ITEM,
                operation=SourceStateOperation.EQUIP,
                subject_id=su,
                object_id="item-a",
                payload={"slot": "主手"},
            ),
            _verified_delta(
                chapter_ids[2],
                3,
                spans[2],
                category=SourceStateCategory.ITEM,
                operation=SourceStateOperation.UNEQUIP,
                subject_id=su,
                object_id="item-a",
            ),
            _verified_delta(
                chapter_ids[3],
                4,
                spans[3],
                category=SourceStateCategory.ITEM,
                operation=SourceStateOperation.TRANSFER,
                subject_id=su,
                object_id="item-a",
                payload={"to_subject_id": lin},
            ),
        ]
    )
    record_source_chapter_deltas(database, "story-game-state-v2-1", "base", deltas)

    with database.connect() as connection:
        first = build_source_state_projection(
            connection,
            "story-game-state-v2-1",
            "base",
            chapter_id=chapter_ids[0],
            chapter_ordinal=1,
        )
        statements: list[str] = []
        connection.set_trace_callback(statements.append)
        second = build_source_state_projection(
            connection,
            "story-game-state-v2-1",
            "base",
            chapter_id=chapter_ids[1],
            chapter_ordinal=2,
        )
        connection.set_trace_callback(None)
        third = build_source_state_projection(
            connection,
            "story-game-state-v2-1",
            "base",
            chapter_id=chapter_ids[2],
            chapter_ordinal=3,
        )
        fourth = build_source_state_projection(
            connection,
            "story-game-state-v2-1",
            "base",
            chapter_id=chapter_ids[3],
            chapter_ordinal=4,
        )

    assert len(first["records"]["ITEM"]) == 3
    assert any(
        "chapter_ordinal>1" in statement and "chapter_ordinal<=2" in statement
        for statement in statements
    )
    assert len(first["records"]["CAPABILITY"]) == 3
    assert {item["state_key"] for item in first["records"]["ITEM"]} == {
        "item:item-a",
        "item:item-b",
        "item:item-c",
    }
    assert {item["state_key"] for item in second["records"]["ITEM"]} == {
        "item:item-a",
        "item:item-c",
    }
    item_a_second = next(
        item for item in second["records"]["ITEM"] if item["state_key"] == "item:item-a"
    )
    assert item_a_second["equipped"] is True
    assert item_a_second["slot"] == "主手"
    item_a_third = next(
        item for item in third["records"]["ITEM"] if item["state_key"] == "item:item-a"
    )
    assert item_a_third["equipped"] is False
    item_a_fourth = next(
        item for item in fourth["records"]["ITEM"] if item["state_key"] == "item:item-a"
    )
    assert item_a_fourth["current_holder_id"] == lin
    assert item_a_fourth["first_acquired_chapter_ordinal"] == 1

    late_delta = _verified_delta(
        chapter_ids[1],
        2,
        spans[1],
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ADD,
        subject_id=su,
        object_id="item-late",
        payload={"name": "迟到的物品"},
    )
    record_source_chapter_deltas(database, "story-game-state-v2-1", "base", [late_delta])
    with database.connect() as connection:
        rebuilt = build_source_state_projection(
            connection,
            "story-game-state-v2-1",
            "base",
            chapter_id=chapter_ids[3],
            chapter_ordinal=4,
        )
    assert any(item["state_key"] == "item:item-late" for item in rebuilt["records"]["ITEM"])


def test_missing_object_identity_is_not_operationally_verified(tmp_path: Path) -> None:
    database, chapter_ids, spans = _four_chapter_book(tmp_path)
    delta = _verified_delta(
        chapter_ids[0],
        1,
        spans[0],
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ADD,
        subject_id="character:su-mu",
        payload={"name": "只有名字的物品"},
    )
    stored = record_source_chapter_deltas(database, "story-game-state-v2-1", "base", [delta])
    assert stored[0].verification_status is SourceStateVerification.SOURCE_PARTIAL
    with database.connect() as connection:
        projection = build_source_state_projection(
            connection,
            "story-game-state-v2-1",
            "base",
            chapter_id=chapter_ids[0],
            chapter_ordinal=1,
        )
        row = connection.execute(
            "SELECT verification_status, state_key FROM source_state_deltas"
        ).fetchone()
    assert projection["records"].get("ITEM", []) == []
    assert projection["uncertain_delta_count"] == 1
    assert row["verification_status"] == SourceStateVerification.SOURCE_PARTIAL.value
    assert row["state_key"] == "item:character:su-mu"


def test_hydration_collect_imports_delta_and_completes_task_without_canon(
    tmp_path: Path,
) -> None:
    database, chapter_ids, hydration_spans = _hydration_book(tmp_path)
    chapter_one_span = hydration_spans[0]
    app = create_app(database, book_id="story-game-state-v2")
    client = TestClient(app)
    queued = client.post(
        "/api/books/story-game-state-v2/editions/base/author-commands",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={"command_type": "REQUEST_SOURCE_STATE_HYDRATION", "chapter_id": chapter_ids[0]},
    )
    assert queued.status_code == 200
    body = queued.json()
    assert body["code"] == "SOURCE_STATE_HYDRATION_HANDOFF_READY"
    handoff_id = body["handoff"]["handoff_id"]
    handoff = get_handoff(database, handoff_id)
    claim = claim_handoff(database, handoff_id, "pytest-codex")
    update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.RUNNING,
        claim_token=claim["claim_token"],
    )
    delta = SourceChapterStateDelta(
        book_id="story-game-state-v2",
        edition_id="base",
        chapter_id=chapter_ids[0],
        chapter_ordinal=1,
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ADD,
        subject_id="character:hero",
        object_id="hydrated-lantern",
        statement="本章确认英雄获得一盏灯。",
        source_span_ids=[chapter_one_span],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "验证后的灯", "quantity": 1, "use": "照明"},
    )
    result = {
        "handoff_id": handoff_id,
        "handoff_type": "SOURCE_STATE_HYDRATION",
        "status": "COMPLETED",
        "book_id": "story-game-state-v2",
        "edition_id": "base",
        "chapter_id": chapter_ids[0],
        "chapter_ordinal": 1,
        "deltas": [delta.model_dump(mode="json")],
        "uncertain_findings": [],
        "canon_committed": False,
        "edition_activated": False,
    }
    Path(str(handoff["result_path"])).write_text(
        json.dumps(result, ensure_ascii=False), encoding="utf-8"
    )
    collected = client.post(
        f"/api/books/story-game-state-v2/editions/base/source-state-hydration/{handoff_id}/collect",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )
    assert collected.status_code == 200
    assert collected.json()["status"] == HandoffStatus.COMPLETED.value
    validated = validate_result_file(database, handoff_id)
    assert validated["validation_summary"]["imported_delta_count"] == 1
    state = client.get(
        f"/api/books/story-game-state-v2/editions/base/chapters/{chapter_ids[0]}/game-state"
        "?character_id=character:hero"
    ).json()
    assert any(item["name"] == "验证后的灯" for item in state["inventory"])
    with database.connect() as connection:
        task = connection.execute(
            "SELECT lifecycle_status FROM author_control_tasks "
            "WHERE task_type='SOURCE_STATE_HYDRATION'"
        ).fetchone()
        assert connection.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM canon_commits").fetchone()[0] == 0
    assert task["lifecycle_status"] == "DONE"


def test_hydration_rejects_evidence_from_another_chapter(tmp_path: Path) -> None:
    database, chapter_ids, hydration_spans = _hydration_book(tmp_path)
    chapter_one_span, chapter_two_span = hydration_spans
    app = create_app(database, book_id="story-game-state-v2")
    client = TestClient(app)
    queued = client.post(
        "/api/books/story-game-state-v2/editions/base/author-commands",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={"command_type": "REQUEST_SOURCE_STATE_HYDRATION", "chapter_id": chapter_ids[0]},
    )
    handoff_id = queued.json()["handoff"]["handoff_id"]
    handoff = get_handoff(database, handoff_id)
    claim = claim_handoff(database, handoff_id, "pytest-codex")
    update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.RUNNING,
        claim_token=claim["claim_token"],
    )
    delta = SourceChapterStateDelta(
        book_id="story-game-state-v2",
        edition_id="base",
        chapter_id=chapter_ids[0],
        chapter_ordinal=1,
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ADD,
        subject_id="character:hero",
        object_id="wrong-evidence-item",
        statement="错误章节证据不应通过。",
        source_span_ids=[chapter_two_span],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
    )
    result = {
        "handoff_id": handoff_id,
        "handoff_type": "SOURCE_STATE_HYDRATION",
        "status": "COMPLETED",
        "book_id": "story-game-state-v2",
        "edition_id": "base",
        "chapter_id": chapter_ids[0],
        "chapter_ordinal": 1,
        "deltas": [delta.model_dump(mode="json")],
        "uncertain_findings": [],
        "canon_committed": False,
        "edition_activated": False,
    }
    Path(str(handoff["result_path"])).write_text(
        json.dumps(result, ensure_ascii=False), encoding="utf-8"
    )
    rejected = client.post(
        f"/api/books/story-game-state-v2/editions/base/source-state-hydration/{handoff_id}/collect",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )
    assert rejected.status_code == 409
    assert get_handoff(database, handoff_id)["status"] == HandoffStatus.FAILED.value
    with database.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM source_state_deltas").fetchone()[0] == 0
