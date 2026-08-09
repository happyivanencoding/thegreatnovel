from __future__ import annotations

from typing import Any

from novel_authoring.author_control.service import execute_author_intent
from novel_authoring.edition import resolve_edition_id
from novel_authoring.planning.innovation import resolve_innovation_control
from novel_authoring.workflows.handoffs import create_continuation_handoff, create_revision_handoff


def _record_workflow_goal(
    database: Any, book_id: str, request: Any, handoff: dict[str, Any]
) -> dict[str, Any] | None:
    goal = str(request.author_goal or "").strip()
    if not goal:
        return None
    selected_edition = resolve_edition_id(database, book_id, request.edition_id)
    resolution = execute_author_intent(
        database,
        book_id,
        selected_edition,
        intent_type="WORKFLOW_GOAL",
        subject_type="WORKFLOW",
        subject_id=str(handoff["handoff_id"]),
        title=f"工作流目标：{goal[:72]}",
        description=goal,
        horizon="MID",
        priority=80,
        target_chapter_id=request.context_chapter_id,
        payload={
            "source": "author_workflow",
            "handoff_id": handoff["handoff_id"],
            "author_task_ids": list(request.author_task_ids),
        },
    )
    return None if resolution.intent is None else resolution.intent.model_dump(mode="json")


def prepare_continuation(database: Any, book_id: str, request: Any) -> dict[str, Any]:
    control, source = resolve_innovation_control(
        database,
        book_id,
        level=request.innovation_level,
        focus=request.innovation_focus,
        save_as_book_default=request.save_as_book_default,
    )
    handoff = create_continuation_handoff(
        database,
        book_id,
        edition_id=request.edition_id,
        requested_stage=request.requested_stage,
        require_complete_metrics=request.require_complete_metrics,
        innovation_control=control,
        innovation_source=source,
        context_chapter_id=request.context_chapter_id,
        author_goal=request.author_goal,
        author_task_ids=request.author_task_ids,
    )
    handoff["author_intent"] = _record_workflow_goal(database, book_id, request, handoff)
    return handoff


def prepare_revision(database: Any, book_id: str, request: Any) -> dict[str, Any]:
    control, source = resolve_innovation_control(
        database,
        book_id,
        level=request.innovation_level,
        focus=request.innovation_focus,
        save_as_book_default=request.save_as_book_default,
    )
    handoff = create_revision_handoff(
        database,
        book_id,
        edition_id=request.edition_id,
        requested_stage=request.requested_stage,
        require_complete_metrics=request.require_complete_metrics,
        innovation_control=control,
        innovation_source=source,
        context_chapter_id=request.context_chapter_id,
        author_goal=request.author_goal,
        author_task_ids=request.author_task_ids,
    )
    handoff["author_intent"] = _record_workflow_goal(database, book_id, request, handoff)
    return handoff
