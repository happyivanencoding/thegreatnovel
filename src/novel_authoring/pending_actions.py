"""Durable author actions that resume after targeted context deepening."""

from __future__ import annotations

import json
import uuid
from typing import Any

from novel_authoring.db.database import Database
from novel_authoring.utils import json_dumps, utc_now


class PendingAuthorActionError(RuntimeError):
    pass


_ACTIVE_STATUSES = ("WAITING_FOR_CONTEXT", "CONTEXT_READY", "RESUMING")


def author_action_key(
    book_id: str,
    edition_id: str,
    chapter_id: str | None,
    action_type: str,
) -> str:
    return ":".join(
        (book_id, edition_id, chapter_id or "current-boundary", action_type.strip().upper())
    )


def _decode(row: Any) -> dict[str, Any]:
    item = dict(row)
    for key in (
        "innovation_json",
        "selected_author_tasks_json",
        "request_json",
        "required_context_json",
    ):
        raw = item.pop(key, "{}")
        try:
            item[key.removesuffix("_json")] = json.loads(str(raw))
        except json.JSONDecodeError:
            item[key.removesuffix("_json")] = {} if key != "selected_author_tasks_json" else []
    return item


def ensure_pending_author_action(
    database: Database,
    *,
    action_type: str,
    book_id: str,
    edition_id: str,
    chapter_id: str | None,
    target_chapter_ordinal: int | None,
    author_goal: str,
    innovation: dict[str, Any],
    selected_author_tasks: list[str],
    requested_stage: str,
    request_payload: dict[str, Any],
    required_context: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    key = author_action_key(book_id, edition_id, chapter_id, action_type)
    with database.connect() as connection:
        existing = connection.execute(
            "SELECT * FROM pending_author_actions WHERE action_key=? "
            "AND status IN ('WAITING_FOR_CONTEXT', 'CONTEXT_READY', 'RESUMING')",
            (key,),
        ).fetchone()
        if existing is not None:
            return _decode(existing), True
        now = utc_now()
        pending_id = f"author-action-{uuid.uuid4().hex}"
        connection.execute(
            "INSERT INTO pending_author_actions("
            "pending_action_id, action_key, action_type, book_id, edition_id, chapter_id, "
            "target_chapter_ordinal, author_goal, innovation_json, "
            "selected_author_tasks_json, requested_stage, request_json, "
            "required_context_json, status, created_at, updated_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
            "'WAITING_FOR_CONTEXT', ?, ?, 1)",
            (
                pending_id,
                key,
                action_type.strip().upper(),
                book_id,
                edition_id,
                chapter_id,
                target_chapter_ordinal,
                author_goal,
                json_dumps(innovation),
                json_dumps(selected_author_tasks),
                requested_stage,
                json_dumps(request_payload),
                json_dumps(required_context),
                now,
                now,
            ),
        )
        row = connection.execute(
            "SELECT * FROM pending_author_actions WHERE pending_action_id=?",
            (pending_id,),
        ).fetchone()
    if row is None:
        raise PendingAuthorActionError("保存作者操作失败")
    return _decode(row), False


def attach_deepening_operation(
    database: Database,
    pending_action_id: str,
    deepening_operation_id: str,
    required_context: dict[str, Any],
) -> dict[str, Any]:
    with database.connect() as connection:
        connection.execute(
            "UPDATE pending_author_actions SET deepening_operation_id=?, "
            "required_context_json=?, updated_at=?, version=version+1 "
            "WHERE pending_action_id=? AND status='WAITING_FOR_CONTEXT'",
            (
                deepening_operation_id,
                json_dumps(required_context),
                utc_now(),
                pending_action_id,
            ),
        )
        row = connection.execute(
            "SELECT * FROM pending_author_actions WHERE pending_action_id=?",
            (pending_action_id,),
        ).fetchone()
    if row is None:
        raise PendingAuthorActionError("作者操作不存在")
    return _decode(row)


def list_pending_author_actions(
    database: Database,
    book_id: str,
    edition_id: str | None = None,
    *,
    include_finished: bool = False,
) -> list[dict[str, Any]]:
    clauses = ["book_id=?"]
    parameters: list[object] = [book_id]
    if edition_id is not None:
        clauses.append("edition_id=?")
        parameters.append(edition_id)
    if not include_finished:
        clauses.append("status IN ('WAITING_FOR_CONTEXT', 'CONTEXT_READY', 'RESUMING')")
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT * FROM pending_author_actions WHERE "
            + " AND ".join(clauses)
            + " ORDER BY created_at DESC",
            tuple(parameters),
        ).fetchall()
    return [_decode(row) for row in rows]


def set_pending_author_action_status(
    database: Database,
    pending_action_id: str,
    status: str,
    *,
    resumed_handoff_id: str | None = None,
) -> dict[str, Any]:
    normalized = status.strip().upper()
    if normalized not in {
        "WAITING_FOR_CONTEXT",
        "CONTEXT_READY",
        "RESUMING",
        "COMPLETED",
        "FAILED",
        "CANCELLED",
    }:
        raise PendingAuthorActionError("作者操作状态无效")
    completed_at = utc_now() if normalized in {"COMPLETED", "FAILED", "CANCELLED"} else None
    with database.connect() as connection:
        connection.execute(
            "UPDATE pending_author_actions SET status=?, resumed_handoff_id=COALESCE(?, "
            "resumed_handoff_id), completed_at=COALESCE(?, completed_at), updated_at=?, "
            "version=version+1 WHERE pending_action_id=?",
            (normalized, resumed_handoff_id, completed_at, utc_now(), pending_action_id),
        )
        row = connection.execute(
            "SELECT * FROM pending_author_actions WHERE pending_action_id=?",
            (pending_action_id,),
        ).fetchone()
    if row is None:
        raise PendingAuthorActionError("作者操作不存在")
    return _decode(row)


def author_activity_view(item: dict[str, Any]) -> dict[str, Any]:
    action = str(item["action_type"])
    ordinal = item.get("target_chapter_ordinal")
    if action == "CONTINUE":
        title = f"续写第{ordinal}章" if ordinal else "续写下一章"
    else:
        title = f"改写第{ordinal}章" if ordinal else "改写章节"
    status = str(item["status"])
    context_done = status in {"CONTEXT_READY", "RESUMING", "COMPLETED"}
    resumed = bool(item.get("resumed_handoff_id"))
    return {
        **item,
        "title": title,
        "author_status": {
            "WAITING_FOR_CONTEXT": "正在补齐本次创作所需的历史上下文",
            "CONTEXT_READY": "上下文已补齐，正在恢复原操作",
            "RESUMING": "正在准备 AI 创作任务",
            "COMPLETED": "创作任务已准备好",
            "FAILED": "任务需要处理",
            "CANCELLED": "任务已取消",
        }.get(status, status),
        "timeline": [
            {"label": "检查当前世界", "state": "done"},
            {"label": "补齐相关历史", "state": "done" if context_done else "active"},
            {"label": "恢复原创作要求", "state": "done" if resumed else "pending"},
            {"label": "准备 AI 创作任务", "state": "done" if resumed else "pending"},
            {"label": "等待作者确认", "state": "pending"},
        ],
    }


__all__ = [
    "PendingAuthorActionError",
    "attach_deepening_operation",
    "author_activity_view",
    "author_action_key",
    "ensure_pending_author_action",
    "list_pending_author_actions",
    "set_pending_author_action_status",
]
