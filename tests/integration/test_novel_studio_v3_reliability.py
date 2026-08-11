from __future__ import annotations

import json
from pathlib import Path

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.initialization import InitializationDepth, create_initialization
from novel_authoring.initialization.models import ArcExtractionOutput
from novel_authoring.initialization.service import arc_output_path
from novel_authoring.pending_actions import (
    attach_deepening_operation,
    ensure_pending_author_action,
)
from novel_authoring.readiness import (
    evaluate_continuation_boundary,
    evaluate_revision_range,
)
from novel_authoring.utils import json_dumps, utc_now
from novel_authoring.web.app import _resume_pending_actions
from novel_authoring.web.schemas import HandoffRequest
from novel_authoring.workflows.handoffs import create_initialization_handoff


def _book(tmp_path: Path, *, chapter_count: int = 4) -> tuple[Database, str]:
    source = tmp_path / "s"
    source.mkdir()
    (source / "novel.md").write_text(
        "\n\n".join(
            f"# 第{ordinal}章 测试{ordinal}\n人物在第{ordinal}章作出选择。"
            for ordinal in range(1, chapter_count + 1)
        ),
        encoding="utf-8",
    )
    workspace = tmp_path / "w"
    book_id = "v3"
    ingest_book(
        book_id=book_id,
        title="Studio V3 测试",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
        confirm_order=True,
    )
    return Database(workspace / book_id / "state.sqlite3"), book_id


def test_continuation_readiness_does_not_search_free_form_strings(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    with database.connect() as connection:
        result = evaluate_continuation_boundary(
            connection,
            book_id=book_id,
            edition_id="base",
            target_chapter_ordinal=5,
            graphs={
                "summary": "主角已经确认，current thread 正在推进",
                "characters": [{"name": "主角", "current_state": {"goal": "前进"}}],
                "plot_threads": [{"thread_id": "thread-main", "summary": "主线"}],
            },
        )

    assert result.ready_for_continuation is False
    assert result.current_protagonist.confirmed is False
    assert result.active_main_threads == []
    assert "当前主角缺少明确实体与真实章节证据" in result.blocking_gaps


def test_revision_readiness_follows_structured_future_references(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    with database.connect() as connection:
        chapters = connection.execute(
            "SELECT chapter_id, ordinal, version FROM chapters WHERE book_id=? ORDER BY ordinal",
            (book_id,),
        ).fetchall()
        for row in chapters[:3]:
            payload = {
                "chapter_id": str(row["chapter_id"]),
                "status": "COMPLETE",
                "character_state_changes": [{"entity_id": "hero", "source_span_ids": ["evidence"]}],
                "thread_advances": [{"thread_id": "main-thread", "source_span_ids": ["evidence"]}],
            }
            connection.execute(
                "INSERT INTO chapter_analysis_records("
                "record_id, book_id, edition_id, chapter_id, analysis_layer, status, "
                "source_revision, result_json, created_at, updated_at, version"
                ") VALUES (?, ?, 'base', ?, 'CONTINUITY', 'COMPLETE', ?, ?, 'now', 'now', 1)",
                (
                    f"record-{row['ordinal']}",
                    book_id,
                    str(row["chapter_id"]),
                    f"chapter-v{int(row['version'])}",
                    json_dumps(payload),
                ),
            )
        readiness = evaluate_revision_range(
            connection,
            book_id=book_id,
            edition_id="base",
            target_chapter_ids=[str(chapters[1]["chapter_id"])],
        )

    assert readiness.ready is True
    assert readiness.required_deepening_chapter_ids == []
    assert readiness.affected_characters == ["hero"]
    assert readiness.affected_threads == ["main-thread"]
    assert readiness.affected_future_range == {"start": 3, "end": 3}


def test_pending_continuation_resumes_after_context_handoff_completes(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    initialization = create_initialization(
        database,
        book_id,
        edition_id="base",
        depth=InitializationDepth.QUICK,
    )
    root = Path(str(initialization["root"]))
    arc_manifest = json.loads((root / "arc_manifest.json").read_text(encoding="utf-8"))
    for arc in arc_manifest["arcs"]:
        output = ArcExtractionOutput(
            initialization_id=str(initialization["initialization_id"]),
            arc_id=str(arc["arc_id"]),
            chapter_semantic_features=[
                {"chapter_id": chapter_id, "analysis_status": "COMPLETE"}
                for chapter_id in arc["semantic_chapter_ids"]
            ],
            chapter_continuity_deltas=[
                {"chapter_id": chapter_id, "status": "COMPLETE_NO_CHANGE"}
                for chapter_id in arc["continuity_chapter_ids"]
            ],
        )
        path = arc_output_path(
            root,
            str(initialization["initialization_id"]),
            book_id,
            "base",
            str(arc["arc_id"]),
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json_dumps(output.model_dump(mode="json"), indent=2), encoding="utf-8")

    request = HandoffRequest(requested_stage="PLAN_ONLY", edition_id="base")
    pending, reused = ensure_pending_author_action(
        database,
        action_type="CONTINUE",
        book_id=book_id,
        edition_id="base",
        chapter_id=None,
        target_chapter_ordinal=5,
        author_goal="推进当前主线",
        innovation={},
        selected_author_tasks=[],
        requested_stage="PLAN_ONLY",
        request_payload=request.model_dump(mode="json"),
        required_context={},
    )
    duplicate, duplicate_reused = ensure_pending_author_action(
        database,
        action_type="CONTINUE",
        book_id=book_id,
        edition_id="base",
        chapter_id=None,
        target_chapter_ordinal=5,
        author_goal="不会覆盖第一次请求",
        innovation={},
        selected_author_tasks=[],
        requested_stage="PLAN_ONLY",
        request_payload=request.model_dump(mode="json"),
        required_context={},
    )
    assert reused is False
    assert duplicate_reused is True
    assert duplicate["pending_action_id"] == pending["pending_action_id"]

    deepening = create_initialization_handoff(
        database,
        book_id,
        edition_id="base",
        requested_stage="NOVEL_INITIALIZATION",
    )
    attach_deepening_operation(
        database,
        str(pending["pending_action_id"]),
        str(deepening["handoff_id"]),
        {
            "selected_chapter_ids": [
                str(chapter_id)
                for arc in arc_manifest["arcs"]
                for chapter_id in arc["semantic_chapter_ids"]
            ]
        },
    )
    with database.connect() as connection:
        connection.execute(
            "UPDATE workflow_handoffs SET status='COMPLETED' WHERE handoff_id=?",
            (str(deepening["handoff_id"]),),
        )
        connection.execute(
            "INSERT INTO rhythm_diagnostic_snapshots("
            "snapshot_id, book_id, edition_id, as_of_chapter, as_of_event_seq, "
            "projection_hash, config_hash, analyzer_versions_json, snapshot_json, created_at"
            ") VALUES ('rhythm-v3', ?, 'base', 4, 0, 'projection', 'config', '{}', '{}', ?)",
            (book_id, utc_now()),
        )

    activities = _resume_pending_actions(database, book_id)
    activity = next(
        item for item in activities if item["pending_action_id"] == pending["pending_action_id"]
    )
    assert activity["status"] == "COMPLETED"
    assert activity["resumed_handoff_id"]
    assert activity["author_status"] == "创作任务已准备好"
    with database.connect() as connection:
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM pending_author_actions WHERE action_key=?",
                (str(pending["action_key"]),),
            ).fetchone()[0]
            == 1
        )
