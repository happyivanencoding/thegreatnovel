"""Author Control command service and its durable non-Canon read model."""

from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from novel_authoring.author_control.models import (
    HORIZON_LABELS,
    LIFECYCLE_LABELS,
    AuthorControlHorizon,
    AuthorIntent,
    AuthorIntentStatus,
    AuthorStateCommand,
    AuthorTask,
    AuthorTaskLifecycle,
    CommandResolution,
    CommandResult,
    PlannedStateChange,
)
from novel_authoring.author_control.source_state import (
    SourceStateCoverageStatus,
    source_state_chapter_coverage,
    source_state_coverage_summary,
    upsert_source_state_coverage,
)
from novel_authoring.db.database import Database
from novel_authoring.utils import utc_now


def _table_exists(connection: sqlite3.Connection, name: str) -> bool:
    return (
        connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
        ).fetchone()
        is not None
    )


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _payload(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if not value:
        return {}
    try:
        parsed = json.loads(str(value))
    except (TypeError, ValueError):
        return {}
    return dict(parsed) if isinstance(parsed, dict) else {}


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("章节序号必须是整数") from exc


def _horizon(value: Any) -> AuthorControlHorizon:
    try:
        return AuthorControlHorizon(str(value or AuthorControlHorizon.MID).upper())
    except ValueError as exc:
        raise ValueError("horizon 必须是 SHORT、MID 或 LONG") from exc


def _lifecycle(value: Any) -> AuthorTaskLifecycle:
    try:
        return AuthorTaskLifecycle(str(value or AuthorTaskLifecycle.BACKLOG).upper())
    except ValueError as exc:
        raise ValueError("任务状态无效") from exc


def _scope_check(connection: sqlite3.Connection, book_id: str, edition_id: str) -> None:
    book = connection.execute("SELECT 1 FROM books WHERE book_id=?", (book_id,)).fetchone()
    if book is None:
        raise ValueError("book 不存在")
    edition = connection.execute(
        "SELECT 1 FROM editions WHERE book_id=? AND edition_id=?", (book_id, edition_id)
    ).fetchone()
    if edition is None:
        raise ValueError("edition 不存在")


def _history(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    object_type: str,
    object_id: str,
    action_type: str,
    before: Any,
    after: Any,
) -> str:
    history_id = f"history-{uuid.uuid4().hex}"
    connection.execute(
        """
        INSERT INTO author_control_history(
            history_id, book_id, edition_id, object_type, object_id,
            action_type, before_json, after_json, created_at, version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """,
        (
            history_id,
            book_id,
            edition_id,
            object_type,
            object_id,
            action_type,
            _json(before),
            _json(after),
            utc_now(),
        ),
    )
    return history_id


def _resolution(
    result: CommandResult,
    code: str,
    message: str,
    *,
    allowed_actions: list[str] | None = None,
    planned_change: PlannedStateChange | None = None,
    intent: AuthorIntent | None = None,
    task: AuthorTask | None = None,
    handoff: dict[str, Any] | None = None,
    history_id: str | None = None,
) -> CommandResolution:
    return CommandResolution(
        result=result,
        code=code,
        message=message,
        allowed_actions=allowed_actions or [],
        planned_change=planned_change,
        intent=intent,
        task=task,
        handoff=handoff,
        history_id=history_id,
        canon_changed=False,
    )


def _intent_from_row(row: sqlite3.Row) -> AuthorIntent:
    return AuthorIntent(
        intent_id=str(row["intent_id"]),
        book_id=str(row["book_id"]),
        edition_id=str(row["edition_id"]),
        intent_type=str(row["intent_type"]),
        subject_type=str(row["subject_type"]),
        subject_id=None if row["subject_id"] is None else str(row["subject_id"]),
        title=str(row["title"]),
        description=str(row["description"] or ""),
        horizon=_horizon(row["horizon"]),
        priority=int(row["priority"]),
        status=AuthorIntentStatus(str(row["status"])),
        target_chapter_id=(
            None if row["target_chapter_id"] is None else str(row["target_chapter_id"])
        ),
        payload=_payload(row["payload_json"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
        version=int(row["version"]),
    )


def _task_from_row(row: sqlite3.Row) -> AuthorTask:
    return AuthorTask(
        task_id=str(row["task_id"]),
        book_id=str(row["book_id"]),
        edition_id=str(row["edition_id"]),
        title=str(row["title"]),
        task_type=str(row["task_type"]),
        description=str(row["description"] or ""),
        horizon=_horizon(row["horizon"]),
        lifecycle_status=_lifecycle(row["lifecycle_status"]),
        priority=int(row["priority"]),
        subject_type=None if row["subject_type"] is None else str(row["subject_type"]),
        subject_id=None if row["subject_id"] is None else str(row["subject_id"]),
        context_chapter_id=(
            None if row["context_chapter_id"] is None else str(row["context_chapter_id"])
        ),
        context_chapter_ordinal=(
            None if row["context_chapter_ordinal"] is None else int(row["context_chapter_ordinal"])
        ),
        due_chapter_ordinal=(
            None if row["due_chapter_ordinal"] is None else int(row["due_chapter_ordinal"])
        ),
        payload=_payload(row["payload_json"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
        version=int(row["version"]),
    )


def execute_author_intent(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    intent_type: str,
    subject_type: str,
    title: str,
    description: str = "",
    horizon: AuthorControlHorizon | str = AuthorControlHorizon.MID,
    priority: int = 100,
    subject_id: str | None = None,
    target_chapter_id: str | None = None,
    payload: dict[str, Any] | None = None,
) -> CommandResolution:
    """Persist an author intent and an audit row; never append a Canon event."""

    clean_title = title.strip()
    if not clean_title:
        raise ValueError("作者意图需要标题")
    selected_horizon = _horizon(horizon)
    now = utc_now()
    intent_id = f"intent-{uuid.uuid4().hex}"
    value = dict(payload or {})
    database.initialize()
    with database.connect() as connection:
        _scope_check(connection, book_id, edition_id)
        connection.execute(
            """
            INSERT INTO author_control_intents(
                intent_id, book_id, edition_id, intent_type, subject_type, subject_id,
                title, description, horizon, priority, status, target_chapter_id,
                payload_json, created_at, updated_at, version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PLANNED', ?, ?, ?, ?, 1)
            """,
            (
                intent_id,
                book_id,
                edition_id,
                intent_type,
                subject_type,
                subject_id,
                clean_title,
                description.strip(),
                selected_horizon.value,
                int(priority),
                target_chapter_id,
                _json(value),
                now,
                now,
            ),
        )
        row = connection.execute(
            "SELECT * FROM author_control_intents WHERE intent_id=?", (intent_id,)
        ).fetchone()
        if row is None:
            raise RuntimeError("作者意图写入后无法读取")
        intent = _intent_from_row(row)
        history_id = _history(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            object_type="INTENT",
            object_id=intent_id,
            action_type="CREATE",
            before={},
            after=intent.model_dump(mode="json"),
        )
    return _resolution(
        CommandResult.PLANNED,
        "AUTHOR_INTENT_RECORDED",
        "作者意图已记录到规划层，尚未改变正史。",
        intent=intent,
        history_id=history_id,
        planned_change=PlannedStateChange(
            change_type="AUTHOR_INTENT",
            target_layer="AUTHOR_CONTROL",
            subject_type=subject_type,
            subject_id=subject_id,
            description=clean_title,
        ),
    )


def execute_author_task(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    title: str,
    task_type: str = "AUTHOR_TASK",
    description: str = "",
    horizon: AuthorControlHorizon | str = AuthorControlHorizon.MID,
    lifecycle_status: AuthorTaskLifecycle | str = AuthorTaskLifecycle.BACKLOG,
    priority: int = 100,
    subject_type: str | None = None,
    subject_id: str | None = None,
    context_chapter_id: str | None = None,
    context_chapter_ordinal: int | None = None,
    due_chapter_ordinal: int | None = None,
    payload: dict[str, Any] | None = None,
) -> CommandResolution:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("作者任务需要标题")
    selected_horizon = _horizon(horizon)
    selected_status = _lifecycle(lifecycle_status)
    now = utc_now()
    task_id = f"task-{uuid.uuid4().hex}"
    value = dict(payload or {})
    database.initialize()
    with database.connect() as connection:
        _scope_check(connection, book_id, edition_id)
        connection.execute(
            """
            INSERT INTO author_control_tasks(
                task_id, book_id, edition_id, title, task_type, description, horizon,
                lifecycle_status, priority, subject_type, subject_id, context_chapter_id,
                context_chapter_ordinal, due_chapter_ordinal, payload_json,
                created_at, updated_at, version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (
                task_id,
                book_id,
                edition_id,
                clean_title,
                task_type,
                description.strip(),
                selected_horizon.value,
                selected_status.value,
                int(priority),
                subject_type,
                subject_id,
                context_chapter_id,
                context_chapter_ordinal,
                due_chapter_ordinal,
                _json(value),
                now,
                now,
            ),
        )
        row = connection.execute(
            "SELECT * FROM author_control_tasks WHERE task_id=?", (task_id,)
        ).fetchone()
        if row is None:
            raise RuntimeError("作者任务写入后无法读取")
        task = _task_from_row(row)
        history_id = _history(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            object_type="TASK",
            object_id=task_id,
            action_type="CREATE",
            before={},
            after=task.model_dump(mode="json"),
        )
    return _resolution(
        CommandResult.PLANNED,
        "AUTHOR_TASK_RECORDED",
        "作者任务已记录到规划层，尚未改变正史。",
        task=task,
        history_id=history_id,
        planned_change=PlannedStateChange(
            change_type="AUTHOR_TASK",
            target_layer="AUTHOR_CONTROL",
            subject_type=subject_type or "TASK",
            subject_id=subject_id,
            description=clean_title,
        ),
    )


def _update_task(
    database: Database,
    book_id: str,
    edition_id: str,
    task_id: str,
    changes: dict[str, Any],
) -> CommandResolution:
    database.initialize()
    allowed = {
        "title",
        "description",
        "horizon",
        "lifecycle_status",
        "priority",
        "due_chapter_ordinal",
        "payload",
    }
    if not set(changes).issubset(allowed):
        raise ValueError("任务更新包含不支持的字段")
    if "title" in changes and not str(changes["title"]).strip():
        raise ValueError("任务标题不能为空")
    if "horizon" in changes:
        changes["horizon"] = _horizon(changes["horizon"]).value
    if "lifecycle_status" in changes:
        changes["lifecycle_status"] = _lifecycle(changes["lifecycle_status"]).value
    if "priority" in changes:
        changes["priority"] = int(changes["priority"])
    if "due_chapter_ordinal" in changes:
        changes["due_chapter_ordinal"] = _optional_int(changes["due_chapter_ordinal"])
    if "payload" in changes:
        changes["payload_json"] = _json(changes.pop("payload"))
    if not changes:
        raise ValueError("没有可更新的任务字段")
    with database.connect() as connection:
        _scope_check(connection, book_id, edition_id)
        row = connection.execute(
            "SELECT * FROM author_control_tasks WHERE task_id=? AND book_id=? AND edition_id=?",
            (task_id, book_id, edition_id),
        ).fetchone()
        if row is None:
            raise ValueError("作者任务不存在")
        before = _task_from_row(row)
        assignments = [f"{key}=?" for key in changes]
        values: list[Any] = [
            _json(value) if key == "payload" else value for key, value in changes.items()
        ]
        assignments.extend(["updated_at=?", "version=version+1"])
        values.append(utc_now())
        values.extend([task_id, book_id, edition_id])
        connection.execute(
            f"UPDATE author_control_tasks SET {', '.join(assignments)} "
            "WHERE task_id=? AND book_id=? AND edition_id=?",
            tuple(values),
        )
        updated_row = connection.execute(
            "SELECT * FROM author_control_tasks WHERE task_id=?", (task_id,)
        ).fetchone()
        if updated_row is None:
            raise RuntimeError("任务更新后无法读取")
        task = _task_from_row(updated_row)
        history_id = _history(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            object_type="TASK",
            object_id=task_id,
            action_type="UPDATE",
            before=before.model_dump(mode="json"),
            after=task.model_dump(mode="json"),
        )
    return _resolution(
        CommandResult.PLANNED,
        "AUTHOR_TASK_UPDATED",
        "作者任务已更新，仍停留在规划层。",
        task=task,
        history_id=history_id,
        planned_change=PlannedStateChange(
            change_type="AUTHOR_TASK_UPDATE",
            target_layer="AUTHOR_CONTROL",
            subject_type="TASK",
            subject_id=task_id,
            description=task.title,
        ),
    )


def _current_state_rejection(
    command: AuthorStateCommand, *, nonexistent: bool
) -> CommandResolution:
    item_id = str(command.payload.get("item_id") or "") or None
    if nonexistent:
        message = "这个物品没有出现在选定章节的正史状态中，不能拖入当前背包。"
        code = "CURRENT_ITEM_EVIDENCE_MISSING"
    else:
        message = "当前背包/装备属于历史状态，修改它必须先创建改写请求或未来意图。"
        code = "CURRENT_STATE_REQUIRES_REVISION"
    return _resolution(
        CommandResult.REJECTED,
        code,
        message,
        allowed_actions=["CREATE_FUTURE_ITEM", "CREATE_REVISION_REQUEST"],
        planned_change=PlannedStateChange(
            change_type="CURRENT_STATE_MUTATION",
            target_layer="CURRENT_CANON_PROJECTION",
            subject_type="ITEM",
            subject_id=item_id,
            description=message,
            requires_revision=True,
        ),
    )


def _item_is_current(
    database: Database, book_id: str, edition_id: str, command: AuthorStateCommand
) -> bool:
    from novel_authoring.author_control.projections import build_story_game_state

    state = build_story_game_state(
        database,
        book_id,
        edition_id,
        chapter_id=command.chapter_id,
        character_id=command.character_id,
    )
    wanted = str(command.payload.get("item_id") or "")
    return any(
        wanted in {str(item.get("record_id") or ""), str(item.get("name") or "")}
        for item in [*state.get("inventory", []), *state.get("equipment", [])]
    )


def _request_source_state_hydration(
    database: Database,
    book_id: str,
    edition_id: str,
    command: AuthorStateCommand,
) -> CommandResolution:
    """Queue source reading work; a GET or command never mutates Canon."""

    chapter_id = str(command.chapter_id or command.payload.get("chapter_id") or "").strip()
    if not chapter_id:
        raise ValueError("补齐章节状态需要 chapter_id")
    database.initialize()
    with database.connect() as connection:
        _scope_check(connection, book_id, edition_id)
        chapter = connection.execute(
            "SELECT chapter_id, ordinal, title FROM chapters WHERE book_id=? AND chapter_id=?",
            (book_id, chapter_id),
        ).fetchone()
        if chapter is None:
            raise ValueError("章节不存在")
        coverage = source_state_chapter_coverage(
            connection,
            book_id,
            edition_id,
            chapter_id,
            chapter_ordinal=int(chapter["ordinal"]),
        )
        existing = connection.execute(
            """
            SELECT * FROM author_control_tasks
            WHERE book_id=? AND edition_id=? AND task_type='SOURCE_STATE_HYDRATION'
              AND context_chapter_id=? AND lifecycle_status NOT IN ('DONE', 'CANCELLED')
            ORDER BY updated_at DESC, task_id DESC LIMIT 1
            """,
            (book_id, edition_id, chapter_id),
        ).fetchone()
    if coverage.complete:
        return _resolution(
            CommandResult.PLANNED,
            "SOURCE_STATE_HYDRATION_ALREADY_COMPLETE",
            f"第{int(chapter['ordinal'])}章已经完成原文状态分析，不会重复排队。",
            allowed_actions=["REANALYZE_SOURCE_STATE"],
            planned_change=PlannedStateChange(
                change_type="SOURCE_STATE_HYDRATION",
                target_layer="SOURCE_STATE_COVERAGE",
                subject_type="SOURCE_CHAPTER_STATE",
                subject_id=chapter_id,
                description="章节状态已覆盖",
            ),
        )
    if existing is not None:
        task = _task_from_row(existing)
        task, handoff = _ensure_source_state_hydration_handoff(
            database, book_id, edition_id, task, chapter_id
        )
        return _resolution(
            CommandResult.PLANNED,
            "SOURCE_STATE_HYDRATION_ALREADY_QUEUED",
            f"第{int(chapter['ordinal'])}章的故事状态补齐任务已经在队列中。",
            allowed_actions=["PROCESS_SOURCE_STATE_HYDRATION"],
            task=task,
            handoff=handoff,
            planned_change=PlannedStateChange(
                change_type="SOURCE_STATE_HYDRATION",
                target_layer="AUTHOR_CONTROL",
                subject_type="SOURCE_CHAPTER_STATE",
                subject_id=chapter_id,
                description=task.title,
            ),
        )
    resolution = execute_author_task(
        database,
        book_id,
        edition_id,
        title=f"补齐第{int(chapter['ordinal'])}章的故事状态",
        task_type="SOURCE_STATE_HYDRATION",
        description=(
            f"读取第{int(chapter['ordinal'])}章《{chapter['title']}》并建立 Source State Delta。"
            "只允许使用本章真实 source span；SOURCE_PARTIAL/UNKNOWN 不得作为当前状态。"
        ),
        horizon=AuthorControlHorizon.SHORT,
        priority=10,
        subject_type="SOURCE_CHAPTER_STATE",
        subject_id=chapter_id,
        context_chapter_id=chapter_id,
        context_chapter_ordinal=int(chapter["ordinal"]),
        due_chapter_ordinal=int(chapter["ordinal"]),
        payload={
            "chapter_id": chapter_id,
            "chapter_ordinal": int(chapter["ordinal"]),
            "source_state_action": "READ_SOURCE_AND_RECORD_DELTAS",
        },
    )
    if resolution.task is None:
        raise RuntimeError("Source State hydration task 创建失败")
    task, handoff = _ensure_source_state_hydration_handoff(
        database, book_id, edition_id, resolution.task, chapter_id
    )
    return _resolution(
        CommandResult.PLANNED,
        "SOURCE_STATE_HYDRATION_HANDOFF_READY",
        "章节状态任务已准备为 Codex handoff；完成结构化导入后会自动回写任务状态。",
        allowed_actions=["OPEN_HANDOFF", "COPY_CODEX_INSTRUCTION", "COLLECT_RESULT"],
        task=task,
        handoff=handoff,
        history_id=resolution.history_id,
        planned_change=resolution.planned_change,
    )


def _ensure_source_state_hydration_handoff(
    database: Database,
    book_id: str,
    edition_id: str,
    task: AuthorTask,
    chapter_id: str,
) -> tuple[AuthorTask, dict[str, Any]]:
    payload = dict(task.payload)
    handoff_id = str(payload.get("handoff_id") or "").strip()
    if not handoff_id:
        from novel_authoring.workflows.handoffs import create_source_state_hydration_handoff

        created = create_source_state_hydration_handoff(
            database,
            book_id,
            edition_id=edition_id,
            chapter_id=chapter_id,
            task_id=task.task_id,
        )
        handoff_id = str(created["handoff_id"])
        with database.connect() as connection:
            upsert_source_state_coverage(
                connection,
                book_id=book_id,
                edition_id=edition_id,
                chapter_id=chapter_id,
                chapter_ordinal=int(task.context_chapter_ordinal or 0),
                status=SourceStateCoverageStatus.READY_FOR_CODEX,
                task_id=task.task_id,
                handoff_id=handoff_id,
            )
        payload.update(
            {
                "handoff_id": handoff_id,
                "hydration_status": "READY_FOR_CODEX",
                "task_directory": created.get("task_directory"),
            }
        )
        updated = _update_task(
            database, book_id, edition_id, task.task_id, {"payload": payload}
        )
        task = updated.task or task
    else:
        with database.connect() as connection:
            row = connection.execute(
                "SELECT status, task_directory FROM workflow_handoffs WHERE handoff_id=? "
                "AND book_id=? AND edition_id=?",
                (handoff_id, book_id, edition_id),
            ).fetchone()
        if row is not None:
            payload.setdefault("task_directory", str(row["task_directory"]))
            payload.setdefault("hydration_status", str(row["status"]))
    status = str(payload.get("hydration_status") or "READY_FOR_CODEX")
    directory = str(payload.get("task_directory") or "")
    return task, {
        "handoff_id": handoff_id,
        "status": status,
        "task_id": task.task_id,
        "chapter_id": chapter_id,
        "task_directory": directory,
        "instruction_url": (
            f"/api/books/{book_id}/editions/{edition_id}/handoffs/"
            f"{handoff_id}/instruction"
        ),
        "result_url": (
            f"/api/books/{book_id}/editions/{edition_id}/handoffs/"
            f"{handoff_id}/result"
        ),
        "collect_url": (
            f"/api/books/{book_id}/editions/{edition_id}/source-state-hydration/"
            f"{handoff_id}/collect"
        ),
    }


def _request_source_state_batch_hydration(
    database: Database,
    book_id: str,
    edition_id: str,
    command: AuthorStateCommand,
) -> CommandResolution:
    payload = dict(command.payload)
    chunk_size = max(10, min(20, int(payload.get("chunk_size", 15))))
    start_ordinal = max(1, int(payload.get("start_ordinal", 1)))
    end_ordinal = _optional_int(payload.get("end_ordinal"))
    volume_title = str(payload.get("volume_title") or "").strip()
    database.initialize()
    with database.connect() as connection:
        _scope_check(connection, book_id, edition_id)
        clauses = ["book_id=?", "ordinal>=?"]
        parameters: list[Any] = [book_id, start_ordinal]
        if end_ordinal is not None:
            clauses.append("ordinal<=?")
            parameters.append(end_ordinal)
        if volume_title:
            clauses.append("volume_title=?")
            parameters.append(volume_title)
        chapters = connection.execute(
            "SELECT chapter_id, ordinal, title FROM chapters WHERE "
            + " AND ".join(clauses)
            + " ORDER BY ordinal, chapter_id",
            tuple(parameters),
        ).fetchall()
    if not chapters:
        raise ValueError("批量补齐范围内没有章节")
    batch_id = f"source-state-batch-{uuid.uuid4().hex}"
    queued: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for chapter in chapters:
        resolution = _request_source_state_hydration(
            database,
            book_id,
            edition_id,
            AuthorStateCommand(
                command_type="REQUEST_SOURCE_STATE_HYDRATION",
                chapter_id=str(chapter["chapter_id"]),
            ),
        )
        entry = {
            "chapter_id": str(chapter["chapter_id"]),
            "chapter_ordinal": int(chapter["ordinal"]),
            "title": str(chapter["title"]),
            "code": resolution.code,
            "handoff": resolution.handoff,
        }
        (skipped if resolution.handoff is None else queued).append(entry)
    chunks = [
        queued[index : index + chunk_size]
        for index in range(0, len(queued), chunk_size)
    ]
    with database.connect() as connection:
        coverage = source_state_coverage_summary(connection, book_id, edition_id)
    return _resolution(
        CommandResult.PLANNED,
        "SOURCE_STATE_BATCH_HYDRATION_READY",
        f"已按每组 {chunk_size} 章准备 {len(queued)} 个逐章 handoff；"
        f"{len(skipped)} 章已有覆盖或已跳过。",
        allowed_actions=["PROCESS_SOURCE_STATE_HYDRATION_CHUNKS", "COLLECT_RESULTS"],
        handoff={
            "batch_id": batch_id,
            "status": "READY_FOR_CODEX" if queued else "COMPLETE",
            "chunk_size": chunk_size,
            "chunks": chunks,
            "skipped": skipped,
            "coverage": coverage,
        },
        planned_change=PlannedStateChange(
            change_type="SOURCE_STATE_BATCH_HYDRATION",
            target_layer="SOURCE_STATE_COVERAGE",
            subject_type="SOURCE_CHAPTER_RANGE",
            subject_id=batch_id,
            description=f"批量补齐 {len(chapters)} 章的原文状态",
        ),
    )


def complete_source_state_hydration_task(
    database: Database, handoff_id: str, *, result: dict[str, Any]
) -> AuthorTask | None:
    """Close the linked planning task after the source ledger import succeeds."""

    database.initialize()
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM author_control_tasks WHERE task_type='SOURCE_STATE_HYDRATION'"
            " AND json_extract(payload_json, '$.handoff_id')=? "
            "ORDER BY updated_at DESC LIMIT 1",
            (handoff_id,),
        ).fetchone()
        if row is None:
            return None
        task = _task_from_row(row)
        if task.lifecycle_status is AuthorTaskLifecycle.DONE:
            return task
        before = task.model_dump(mode="json")
        payload = dict(task.payload)
        payload["hydration_status"] = "COMPLETED"
        result_deltas = [
            item for item in result.get("deltas", []) if isinstance(item, dict)
        ]
        payload["imported_delta_count"] = len(result_deltas)
        uncertain_count = len(result.get("uncertain_findings", []))
        verified_count = sum(
            1
            for item in result_deltas
            if item.get("verification_status") == "SOURCE_VERIFIED"
        )
        uncertain_count += len(result_deltas) - verified_count
        coverage_status = (
            SourceStateCoverageStatus.COMPLETE_WITH_CHANGES
            if verified_count
            else SourceStateCoverageStatus.COMPLETE_NO_CHANGE
        )
        upsert_source_state_coverage(
            connection,
            book_id=task.book_id,
            edition_id=task.edition_id,
            chapter_id=str(task.context_chapter_id or ""),
            chapter_ordinal=int(task.context_chapter_ordinal or 0),
            status=coverage_status,
            verified_delta_count=verified_count,
            uncertain_finding_count=uncertain_count,
            task_id=task.task_id,
            handoff_id=handoff_id,
        )
        connection.execute(
            "UPDATE author_control_tasks SET lifecycle_status='DONE', payload_json=?, "
            "updated_at=?, version=version+1 WHERE task_id=?",
            (_json(payload), utc_now(), task.task_id),
        )
        updated_row = connection.execute(
            "SELECT * FROM author_control_tasks WHERE task_id=?", (task.task_id,)
        ).fetchone()
        if updated_row is None:
            raise RuntimeError("Source State hydration task 完成后无法读取")
        updated = _task_from_row(updated_row)
        _history(
            connection,
            book_id=task.book_id,
            edition_id=task.edition_id,
            object_type="TASK",
            object_id=task.task_id,
            action_type="SOURCE_STATE_HYDRATION_COMPLETED",
            before=before,
            after=updated.model_dump(mode="json"),
        )
        return updated


def execute_author_command(
    database: Database,
    book_id: str,
    edition_id: str,
    command: AuthorStateCommand,
) -> CommandResolution:
    """Resolve a UI command into an author-control record or a safe rejection."""

    command_type = command.command_type.strip().upper()
    payload = dict(command.payload)
    if command_type in {
        "DROP_ITEM",
        "MOVE_ITEM",
        "EQUIP_ITEM",
        "SET_CURRENT_STATE",
        "UPDATE_CURRENT_STATE",
    }:
        destination = str(payload.get("destination") or payload.get("target_layer") or "").upper()
        if destination in {"CURRENT_INVENTORY", "CURRENT_EQUIPMENT", "CURRENT_STATE"}:
            return _current_state_rejection(
                command,
                nonexistent=not _item_is_current(database, book_id, edition_id, command),
            )
        return _resolution(
            CommandResult.REJECTED,
            "AUTHOR_COMMAND_REQUIRES_EXPLICIT_INTENT",
            "拖拽只表达作者意图；请选择未来任务或创建改写请求。",
            allowed_actions=["CREATE_FUTURE_ITEM", "CREATE_REVISION_REQUEST", "CREATE_TASK"],
        )
    if command_type in {"CREATE_TASK", "CREATE_AUTHOR_TASK"}:
        return execute_author_task(
            database,
            book_id,
            edition_id,
            title=str(payload.get("title") or ""),
            task_type=str(payload.get("task_type") or "AUTHOR_TASK"),
            description=str(payload.get("description") or ""),
            horizon=payload.get("horizon", AuthorControlHorizon.MID),
            lifecycle_status=payload.get("lifecycle_status", AuthorTaskLifecycle.BACKLOG),
            priority=int(payload.get("priority", 100)),
            subject_type=(str(payload["subject_type"]) if payload.get("subject_type") else None),
            subject_id=(str(payload["subject_id"]) if payload.get("subject_id") else None),
            context_chapter_id=command.chapter_id,
            context_chapter_ordinal=_optional_int(payload.get("chapter_ordinal")),
            due_chapter_ordinal=_optional_int(payload.get("due_chapter_ordinal")),
            payload=payload,
        )
    if command_type in {"MOVE_TASK", "MOVE_TASK_HORIZON", "UPDATE_TASK"}:
        task_id = str(payload.get("task_id") or "")
        if not task_id:
            raise ValueError("移动任务需要 task_id")
        changes = {
            key: payload[key]
            for key in (
                "title",
                "description",
                "horizon",
                "lifecycle_status",
                "priority",
                "due_chapter_ordinal",
                "payload",
            )
            if key in payload
        }
        if command_type == "MOVE_TASK_HORIZON":
            changes = {"horizon": payload.get("horizon")}
        return _update_task(database, book_id, edition_id, task_id, changes)
    if command_type == "REQUEST_SOURCE_STATE_HYDRATION":
        return _request_source_state_hydration(database, book_id, edition_id, command)
    if command_type == "REQUEST_SOURCE_STATE_BATCH_HYDRATION":
        return _request_source_state_batch_hydration(
            database, book_id, edition_id, command
        )
    if command_type == "CREATE_FUTURE_ITEM":
        name = str(payload.get("name") or payload.get("title") or "").strip()
        if not name:
            raise ValueError("未来物品意图需要 name")
        return execute_author_intent(
            database,
            book_id,
            edition_id,
            intent_type="FUTURE_ITEM",
            subject_type="ITEM",
            subject_id=str(payload.get("item_id") or f"future-item-{uuid.uuid4().hex}"),
            title=name,
            description=str(payload.get("description") or ""),
            horizon=payload.get("horizon", AuthorControlHorizon.MID),
            priority=int(payload.get("priority", 100)),
            target_chapter_id=command.chapter_id,
            payload=payload,
        )
    if command_type == "CREATE_RELATIONSHIP_INTENT":
        from_id = str(payload.get("from_entity_id") or payload.get("from_id") or "").strip()
        to_id = str(payload.get("to_entity_id") or payload.get("to_id") or "").strip()
        if not from_id or not to_id:
            raise ValueError("关系意图需要 from_entity_id 和 to_entity_id")
        title = str(payload.get("title") or f"{from_id} 与 {to_id} 的关系推进")
        return execute_author_intent(
            database,
            book_id,
            edition_id,
            intent_type="RELATIONSHIP_GOAL",
            subject_type="RELATIONSHIP",
            subject_id=str(
                payload.get("relationship_id") or f"relationship-goal-{uuid.uuid4().hex}"
            ),
            title=title,
            description=str(payload.get("description") or ""),
            horizon=payload.get("horizon", AuthorControlHorizon.MID),
            priority=int(payload.get("priority", 100)),
            target_chapter_id=command.chapter_id,
            payload={**payload, "from_entity_id": from_id, "to_entity_id": to_id},
        )
    if command_type == "CREATE_REVISION_REQUEST":
        return execute_author_intent(
            database,
            book_id,
            edition_id,
            intent_type="REVISION_REQUEST",
            subject_type=str(payload.get("subject_type") or "STATE"),
            subject_id=str(payload.get("subject_id") or "") or None,
            title=str(payload.get("title") or "申请改写当前状态"),
            description=str(payload.get("description") or ""),
            horizon=payload.get("horizon", AuthorControlHorizon.SHORT),
            priority=int(payload.get("priority", 10)),
            target_chapter_id=command.chapter_id,
            payload=payload,
        )
    raise ValueError(f"不支持的 Author Command：{command.command_type}")


def author_control_view(database: Database, book_id: str, edition_id: str) -> dict[str, Any]:
    """Return tasks/intents as a separate author-control projection."""

    with database.connect() as connection:
        if not _table_exists(connection, "author_control_tasks"):
            return {
                "storage_status": "NOT_INITIALIZED",
                "storage_status_label": "作者控制存储尚未初始化",
                "tasks": [],
                "intents": [],
                "portfolio": {key: [] for key in ("SHORT", "MID", "LONG")},
            }
        task_rows = connection.execute(
            """
            SELECT * FROM author_control_tasks
            WHERE book_id=? AND edition_id=?
            ORDER BY priority, updated_at DESC, task_id
            """,
            (book_id, edition_id),
        ).fetchall()
        intent_rows = connection.execute(
            """
            SELECT * FROM author_control_intents
            WHERE book_id=? AND edition_id=?
            ORDER BY priority, updated_at DESC, intent_id
            """,
            (book_id, edition_id),
        ).fetchall()
    tasks: list[dict[str, Any]] = []
    portfolio: dict[str, list[dict[str, Any]]] = {key: [] for key in ("SHORT", "MID", "LONG")}
    for row in task_rows:
        task = _task_from_row(row).model_dump(mode="json")
        task["horizon_label"] = HORIZON_LABELS[task["horizon"]]
        task["lifecycle_status_label"] = LIFECYCLE_LABELS[task["lifecycle_status"]]
        tasks.append(task)
        portfolio[str(task["horizon"])].append(task)
    intents = []
    for row in intent_rows:
        intent = _intent_from_row(row).model_dump(mode="json")
        intent["horizon_label"] = HORIZON_LABELS[intent["horizon"]]
        intents.append(intent)
    return {
        "storage_status": "READY",
        "storage_status_label": "作者控制存储已就绪",
        "tasks": tasks,
        "intents": intents,
        "portfolio": portfolio,
        "summary": {
            "task_count": len(tasks),
            "intent_count": len(intents),
            "active_task_count": sum(1 for task in tasks if task["lifecycle_status"] == "ACTIVE"),
        },
        "safety": {
            "canon_changed_by_commands": False,
            "message": "任务和意图只进入作者控制层；正式状态仍需现有工作流、校验和作者批准。",
        },
    }


__all__ = [
    "author_control_view",
    "complete_source_state_hydration_task",
    "execute_author_command",
    "execute_author_intent",
    "execute_author_task",
]
