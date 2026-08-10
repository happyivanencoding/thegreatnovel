from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.canon.events import EventStatus, EventStore
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.domain.models import InformationStatus
from novel_authoring.ingest.service import ingest_book
from novel_authoring.web.app import create_app


def _book_with_historical_state(tmp_path: Path) -> tuple[Database, str]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "story.md").write_text(
        "第1章 雾中的车站\n\n苏牧握住短刀，决定守住车站。\n\n"
        "第2章 未抵达的消息\n\n无线电里传来一段杂音。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="author-control-book",
        title="作者控制测试",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "author-control-book" / "state.sqlite3")
    with database.connect() as connection:
        chapter = connection.execute(
            "SELECT chapter_id FROM chapters WHERE ordinal=1"
        ).fetchone()
    assert chapter is not None
    chapter_id = str(chapter["chapter_id"])
    store = EventStore(database)
    events = [
        store.append(
            book_id="author-control-book",
            event_type="ENTITY_CONFIRMED",
            aggregate_type="entity",
            aggregate_id="su-mu",
            payload={"entity_id": "su-mu", "name": "苏牧", "entity_type": "character"},
            source_kind="SOURCE_SPAN",
            source_id="chapter-1",
            status=EventStatus.COMMITTED,
            information_state=InformationStatus.CANON,
            canon_commit_id="SOURCE_IMPORT",
        ),
        store.append(
            book_id="author-control-book",
            event_type="CHARACTER_STATE_SET",
            aggregate_type="character",
            aggregate_id="su-mu-state-1",
            payload={
                "state_id": "su-mu-state-1",
                "character_id": "su-mu",
                "name": "苏牧",
                "goal": "守住车站",
                "resources": {"饮用水": {"quantity": 2, "unit": "瓶"}},
            },
            source_kind="SOURCE_SPAN",
            source_id="chapter-1",
            status=EventStatus.COMMITTED,
            information_state=InformationStatus.CANON,
            canon_commit_id="SOURCE_IMPORT",
        ),
        store.append(
            book_id="author-control-book",
            event_type="RESOURCE_SET",
            aggregate_type="resource",
            aggregate_id="short-knife",
            payload={
                "resource_id": "short-knife",
                "owner_id": "su-mu",
                "name": "短刀",
                "resource_type": "equipment",
                "slot": "weapon",
                "status": "ACTIVE",
            },
            source_kind="SOURCE_SPAN",
            source_id="chapter-1",
            status=EventStatus.COMMITTED,
            information_state=InformationStatus.CANON,
            canon_commit_id="SOURCE_IMPORT",
        ),
        store.append(
            book_id="author-control-book",
            event_type="CAPABILITY_SET",
            aggregate_type="capability",
            aggregate_id="rule-reading",
            payload={
                "capability_id": "rule-reading",
                "owner_id": "su-mu",
                "name": "规则阅读",
                "status": "ACTIVE",
            },
            source_kind="SOURCE_SPAN",
            source_id="chapter-1",
            status=EventStatus.COMMITTED,
            information_state=InformationStatus.CANON,
            canon_commit_id="SOURCE_IMPORT",
        ),
        store.append(
            book_id="author-control-book",
            event_type="KNOWLEDGE_EDGE_SET",
            aggregate_type="knowledge",
            aggregate_id="knowledge-station-rule",
            payload={
                "edge_id": "knowledge-station-rule",
                "character_id": "su-mu",
                "name": "车站规则",
                "knowledge_state": "KNOWN",
                "statement": "知道车站规则",
            },
            source_kind="SOURCE_SPAN",
            source_id="chapter-1",
            status=EventStatus.COMMITTED,
            information_state=InformationStatus.CANON,
            canon_commit_id="SOURCE_IMPORT",
        ),
        store.append(
            book_id="author-control-book",
            event_type="RELATIONSHIP_SET",
            aggregate_type="relationship",
            aggregate_id="su-lin",
            payload={
                "relationship_id": "su-lin",
                "from_entity_id": "su-mu",
                "to_entity_id": "lin-yu-wei",
                "name": "苏牧—林雨薇",
                "statement": "情报互换但债务未清",
            },
            source_kind="SOURCE_SPAN",
            source_id="chapter-1",
            status=EventStatus.COMMITTED,
            information_state=InformationStatus.CANON,
            canon_commit_id="SOURCE_IMPORT",
        ),
    ]
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO canon_commits(
                commit_id, book_id, draft_id, event_start_seq, event_end_seq,
                chapter_id, author_approval, committed_at, version, edition_id
            ) VALUES ('source-chapter-1', 'author-control-book', 'source-draft-1',
                      ?, ?, ?, 'SOURCE_IMPORT', 'now', 1, 'base')
            """,
            (events[0].event_seq, events[-1].event_seq, chapter_id),
        )
    return database, chapter_id


def _canon_snapshot(database: Database) -> dict[str, object]:
    with database.connect() as connection:
        return {
            "events": [tuple(row) for row in connection.execute(
                "SELECT event_id, event_seq, event_type FROM events ORDER BY event_seq"
            )],
            "commits": [tuple(row) for row in connection.execute(
                "SELECT commit_id, draft_id, event_end_seq FROM canon_commits ORDER BY commit_id"
            )],
            "projection": [tuple(row) for row in connection.execute(
                "SELECT book_id, through_event_seq, state_sha256 FROM projection_metadata"
            )],
        }


def test_story_game_state_is_historical_and_author_commands_do_not_touch_canon(
    tmp_path: Path,
) -> None:
    database, chapter_id = _book_with_historical_state(tmp_path)
    app = create_app(database, book_id="author-control-book")
    client = TestClient(app)
    csrf = app.state.csrf_token

    state = client.get(
        f"/api/books/author-control-book/editions/base/chapters/{chapter_id}/game-state"
        "?character_id=su-mu"
    )
    assert state.status_code == 200
    body = state.json()
    assert body["availability"] == "CANON_EVENT_PROJECTION"
    assert body["character"]["name"] == "苏牧"
    assert any(item["name"] == "短刀" for item in body["equipment"])
    assert any(item["name"] == "规则阅读" for item in body["abilities"])
    assert any(item["name"] == "车站规则" for item in body["knowledge"])
    assert any(item["name"] == "苏牧—林雨薇" for item in body["relationships"])

    page = client.get(
        f"/books/author-control-book/editions/base/workbench?mode=state&chapter_id={chapter_id}"
        "&character_id=su-mu"
    )
    assert page.status_code == 200
    assert "Chapter World State" in page.text
    assert "苏牧" in page.text
    assert "任务与剧情线" in page.text
    assert "Relationship Graph" in page.text

    before = _canon_snapshot(database)
    future_item = client.post(
        "/api/books/author-control-book/editions/base/author-commands",
        headers={"X-CSRF-Token": csrf},
        json={
            "command_type": "CREATE_FUTURE_ITEM",
            "chapter_id": chapter_id,
            "character_id": "su-mu",
            "payload": {"name": "未抵达的钥匙", "horizon": "MID"},
        },
    )
    assert future_item.status_code == 200
    assert future_item.json()["result"] == "PLANNED"
    assert future_item.json()["canon_changed"] is False

    task = client.post(
        "/api/books/author-control-book/editions/base/author-tasks",
        headers={"X-CSRF-Token": csrf},
        json={"title": "确认下一章资源代价", "horizon": "SHORT"},
    )
    assert task.status_code == 200
    task_body = task.json()
    assert task_body["result"] == "PLANNED"
    task_id = task_body["task"]["task_id"]
    moved = client.post(
        "/api/books/author-control-book/editions/base/author-commands",
        headers={"X-CSRF-Token": csrf},
        json={
            "command_type": "MOVE_TASK_HORIZON",
            "payload": {"task_id": task_id, "horizon": "LONG"},
        },
    )
    assert moved.status_code == 200
    assert moved.json()["task"]["horizon"] == "LONG"

    unsafe = client.post(
        "/api/books/author-control-book/editions/base/author-commands",
        headers={"X-CSRF-Token": csrf},
        json={
            "command_type": "DROP_ITEM",
            "chapter_id": chapter_id,
            "character_id": "su-mu",
            "payload": {"item_id": "not-in-history", "destination": "CURRENT_INVENTORY"},
        },
    )
    assert unsafe.status_code == 200
    assert unsafe.json()["result"] == "REJECTED"
    assert unsafe.json()["code"] == "CURRENT_ITEM_EVIDENCE_MISSING"
    assert "CREATE_FUTURE_ITEM" in unsafe.json()["allowed_actions"]
    assert _canon_snapshot(database) == before

    control = client.get(
        "/api/books/author-control-book/editions/base/author-control"
    )
    assert control.status_code == 200
    assert control.json()["summary"]["task_count"] == 1
    assert control.json()["intents"][0]["intent_type"] == "FUTURE_ITEM"
