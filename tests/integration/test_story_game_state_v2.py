from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from novel_authoring.author_control.source_state import (
    SourceChapterStateDelta,
    SourceStateCategory,
    SourceStateOperation,
    SourceStateVerification,
    record_source_chapter_deltas,
)
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.planning.aggregates import build_planning_aggregate
from novel_authoring.web.app import create_app


def _book_with_source_baseline(tmp_path: Path) -> tuple[Database, list[str], str]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "story.md").write_text(
        "第1章 灯塔\n\n海风把旧门吹开。\n\n"
        "第2章 潮声\n\n英雄拿到M500转轮手枪，学会额外攻击。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="story-game-state-v2",
        title="Story Game State V2 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "story-game-state-v2" / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = connection.execute(
            "SELECT chapter_id, ordinal, start_line, end_line FROM chapters "
            "WHERE book_id=? ORDER BY ordinal",
            ("story-game-state-v2",),
        ).fetchall()
        spans = connection.execute(
            "SELECT span_id, chapter_id, start_line, end_line FROM source_spans "
            "WHERE book_id=? ORDER BY chapter_id",
            ("story-game-state-v2",),
        ).fetchall()
    span_by_chapter = {str(row["chapter_id"]): dict(row) for row in spans}

    def evidence(chapter: dict[str, object]) -> dict[str, object]:
        span = span_by_chapter[str(chapter["chapter_id"])]
        return {
            "source_id": "source-story-game-state-v2",
            "segment_id": f"segment-{int(chapter['ordinal']):04d}",
            "start_line": int(span["start_line"]),
            "end_line": int(span["end_line"]),
            "chapter_id": str(chapter["chapter_id"]),
            "source_span_ids": [str(span["span_id"])],
            "mapping_status": "EXACT",
            "direct_text_confirmed": True,
        }

    baseline_root = database.path.parent / "editions" / "base" / "analysis" / "runtime_baseline"
    version_root = baseline_root / "versions" / "v2-test"
    version_root.mkdir(parents=True)
    manifest = {
        "baseline_id": "v2-test",
        "book_id": "story-game-state-v2",
        "edition_id": "base",
        "boundary_chapter": 2,
        "created_at": "2026-08-09T00:00:00+00:00",
        "entry_counts": {"character": 1, "item": 1, "capability": 1, "knowledge": 1},
    }
    (version_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
    )
    (baseline_root / "latest.json").write_text(
        json.dumps({"manifest": str(version_root / "manifest.json")}, ensure_ascii=False),
        encoding="utf-8",
    )
    chapter_two = dict(chapters[1])
    (version_root / "characters.json").write_text(
        json.dumps(
            [
                {
                    "entry_id": "character-hero",
                    "category": "character",
                    "subject_id": "character:hero",
                    "name": "英雄",
                    "statement": "英雄会评估规则与资源再行动。",
                    "status": "SOURCE_VERIFIED",
                    "source_scope": "SELF_BOOK",
                    "source_kind": "SOURCE_TEXT",
                    "evidence": [evidence(chapter_two)],
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    common = {
        "source_scope": "SELF_BOOK",
        "source_kind": "SOURCE_TEXT",
        "evidence": [evidence(chapter_two)],
        "status": "SOURCE_VERIFIED",
    }
    (version_root / "items.json").write_text(
        json.dumps(
            [
                {
                    **common,
                    "entry_id": "item-m500",
                    "category": "item",
                    "subject_id": "character:hero",
                    "name": "M500转轮手枪",
                    "statement": "M500转轮手枪已被发现并保存。",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (version_root / "capabilities.json").write_text(
        json.dumps(
            [
                {
                    **common,
                    "entry_id": "capability-extra-attack",
                    "category": "capability",
                    "subject_id": "character:hero",
                    "name": "额外攻击",
                    "statement": "英雄已经学会额外攻击。",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (version_root / "knowledge.json").write_text(
        json.dumps(
            [
                {
                    **common,
                    "entry_id": "knowledge-tide",
                    "category": "knowledge",
                    "subject_id": "threat:tide",
                    "name": "潮声坐标",
                    "statement": "潮声里出现了坐标，但谁知道它仍未确认。",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return database, [str(row["chapter_id"]) for row in chapters], str(
        span_by_chapter[str(chapters[0]["chapter_id"])] ["span_id"]
    )


def test_source_only_baseline_is_chapter_aware_and_never_canon(tmp_path: Path) -> None:
    database, chapter_ids, chapter_one_span = _book_with_source_baseline(tmp_path)
    app = create_app(database, book_id="story-game-state-v2")
    client = TestClient(app)

    early = client.get(
        f"/api/books/story-game-state-v2/editions/base/chapters/{chapter_ids[0]}/game-state"
    )
    assert early.status_code == 200
    early_body = early.json()
    assert early_body["availability"] == "SOURCE_STATE_HYDRATION_REQUIRED"
    assert early_body["inventory"] == []
    assert early_body["source_state"]["hydration"]["required"] is True
    assert "M500转轮手枪" not in json.dumps(early_body, ensure_ascii=False)

    current = client.get(
        f"/api/books/story-game-state-v2/editions/base/chapters/{chapter_ids[1]}/game-state"
        "?character_id=character:hero"
    )
    assert current.status_code == 200
    body = current.json()
    assert body["availability"] == "SOURCE_CHAPTER_STATE_PROJECTION"
    assert body["character"]["status"] == "SOURCE_VERIFIED"
    assert body["character"]["status_label"] == "✓ 原文已确认"
    assert any(item["name"] == "M500转轮手枪" for item in body["inventory"])
    assert any(item["name"] == "额外攻击" for item in body["abilities"])
    assert all(item["status"] == "SOURCE_VERIFIED" for item in body["inventory"])
    assert body["knowledge"][0]["knowledge_state"] == "UNKNOWN"

    with database.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM canon_commits").fetchone()[0] == 0

    queued = client.post(
        "/api/books/story-game-state-v2/editions/base/author-commands",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={
            "command_type": "REQUEST_SOURCE_STATE_HYDRATION",
            "chapter_id": chapter_ids[0],
        },
    )
    assert queued.status_code == 200
    assert queued.json()["task"]["task_type"] == "SOURCE_STATE_HYDRATION"
    refreshed = client.get(
        f"/api/books/story-game-state-v2/editions/base/chapters/{chapter_ids[0]}/game-state"
    ).json()
    assert refreshed["source_state"]["hydration"]["queued"] is True

    unsafe = client.post(
        "/api/books/story-game-state-v2/editions/base/author-commands",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={
            "command_type": "DROP_ITEM",
            "chapter_id": chapter_ids[1],
            "character_id": "character:hero",
            "payload": {"item_id": "baseline:item-m500", "destination": "CURRENT_INVENTORY"},
        },
    )
    assert unsafe.status_code == 200
    assert unsafe.json()["code"] == "CURRENT_STATE_REQUIRES_REVISION"

    delta = SourceChapterStateDelta(
        book_id="story-game-state-v2",
        edition_id="base",
        chapter_id=chapter_ids[0],
        chapter_ordinal=1,
        category=SourceStateCategory.CAPABILITY,
        operation=SourceStateOperation.ADD,
        subject_id="character:hero",
        statement="第一章已确认基础能力。",
        source_span_ids=[chapter_one_span],
        confidence=1,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
    )
    record_source_chapter_deltas(database, "story-game-state-v2", "base", [delta])
    with database.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM source_state_deltas").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0


def test_source_state_verified_requires_evidence_and_planning_reads_author_control(
    tmp_path: Path,
) -> None:
    database, chapter_ids, _ = _book_with_source_baseline(tmp_path)
    with pytest.raises(ValueError, match="source span"):
        SourceChapterStateDelta(
            book_id="story-game-state-v2",
            edition_id="base",
            chapter_id=chapter_ids[0],
            chapter_ordinal=1,
            category=SourceStateCategory.ITEM,
            operation=SourceStateOperation.ADD,
            subject_id="character:hero",
            statement="没有证据的物品不应进入当前状态。",
            verification_status=SourceStateVerification.SOURCE_VERIFIED,
        )

    from novel_authoring.author_control.service import execute_author_task

    task = execute_author_task(
        database,
        "story-game-state-v2",
        "base",
        title="确认下一章资源代价",
        task_type="AUTHOR_TASK",
        horizon="SHORT",
        priority=3,
        context_chapter_id=chapter_ids[1],
        context_chapter_ordinal=2,
    )
    assert task.task is not None
    aggregate = build_planning_aggregate(database, "story-game-state-v2", edition_id="base")
    policy = aggregate["author_policy"]["author_control"]
    assert policy["tasks"][0]["task_id"] == task.task.task_id
    assert policy["target_hits"]["task_count"] == 1
