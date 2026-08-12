from __future__ import annotations

import uuid
from typing import Any

from novel_authoring.author_control.service import execute_author_intent
from novel_authoring.edition import (
    EditionPurpose,
    create_edition,
    get_edition,
    resolve_edition_id,
)
from novel_authoring.planning.innovation import resolve_innovation_control
from novel_authoring.utils import stable_id, utc_now
from novel_authoring.workflows.handoffs import (
    HandoffType,
    create_continuation_handoff,
    create_revision_handoff,
)


def _record_workflow_goal(
    database: Any, book_id: str, request: Any, handoff: dict[str, Any]
) -> dict[str, Any] | None:
    goal = str(request.author_goal or "").strip()
    if not goal:
        return None
    selected_edition = resolve_edition_id(database, book_id, request.edition_id)
    with database.connect() as connection:
        existing = connection.execute(
            "SELECT * FROM author_control_intents WHERE book_id=? AND edition_id=? "
            "AND intent_type='WORKFLOW_GOAL' AND description=? "
            "AND status IN ('PLANNED', 'ACTIVE') ORDER BY updated_at DESC LIMIT 1",
            (book_id, selected_edition, goal),
        ).fetchone()
    if existing is not None:
        return dict(existing)
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
    selected_edition = resolve_edition_id(database, book_id, request.edition_id)
    handoff_id = stable_id(
        "handoff",
        book_id,
        selected_edition,
        HandoffType.CONTINUATION.value,
        request.requested_stage,
        utc_now(),
    )
    author_intent = _record_workflow_goal(
        database, book_id, request, {"handoff_id": handoff_id}
    )
    handoff = create_continuation_handoff(
        database,
        book_id,
        handoff_id=handoff_id,
        edition_id=request.edition_id,
        requested_stage=request.requested_stage,
        require_complete_metrics=request.require_complete_metrics,
        innovation_control=control,
        innovation_source=source,
        context_chapter_id=request.context_chapter_id,
        author_goal=request.author_goal,
        author_task_ids=request.author_task_ids,
    )
    handoff["author_intent"] = author_intent
    return handoff


def prepare_revision(database: Any, book_id: str, request: Any) -> dict[str, Any]:
    if request.revision_mode is None:
        raise ValueError("请先选择修订当前路线或另开故事路线")
    parent_id = resolve_edition_id(database, book_id, request.edition_id)
    parent = get_edition(database, book_id, parent_id)
    fork_ordinal: int | None = None
    if request.context_chapter_id:
        with database.connect() as connection:
            chapter = connection.execute(
                "SELECT ordinal FROM chapters WHERE book_id=? AND chapter_id=?",
                (book_id, request.context_chapter_id),
            ).fetchone()
        if chapter is None:
            raise ValueError("改写目标章节不存在")
        fork_ordinal = int(chapter["ordinal"])
    purpose = EditionPurpose(request.revision_mode)
    if purpose is EditionPurpose.ALTERNATE_ROUTE and fork_ordinal is None:
        raise ValueError("另开故事路线前必须选择分叉章节")
    edition_id = f"edition-{uuid.uuid4().hex[:12]}"
    default_name = (
        f"{parent.display_name} · 第{fork_ordinal}章备选路线"
        if purpose is EditionPurpose.ALTERNATE_ROUTE
        else f"{parent.display_name} · 第{fork_ordinal or '当前'}章修订"
    )
    created_edition = create_edition(
        database,
        book_id,
        edition_id,
        str(request.edition_display_name or default_name).strip(),
        parent_edition_id=parent_id,
        edition_purpose=purpose,
        fork_chapter_ordinal=(fork_ordinal if purpose is EditionPurpose.ALTERNATE_ROUTE else None),
        created_by_action=(
            "ALTERNATE_ROUTE" if purpose is EditionPurpose.ALTERNATE_ROUTE else "REWRITE_CHAPTER"
        ),
    )
    control, source = resolve_innovation_control(
        database,
        book_id,
        level=request.innovation_level,
        focus=request.innovation_focus,
        save_as_book_default=request.save_as_book_default,
    )
    handoff_id = stable_id(
        "handoff",
        book_id,
        created_edition.edition_id,
        HandoffType.REVISION.value,
        request.requested_stage,
        utc_now(),
    )
    author_intent = _record_workflow_goal(
        database, book_id, request, {"handoff_id": handoff_id}
    )
    handoff = create_revision_handoff(
        database,
        book_id,
        handoff_id=handoff_id,
        edition_id=created_edition.edition_id,
        requested_stage=request.requested_stage,
        require_complete_metrics=request.require_complete_metrics,
        innovation_control=control,
        innovation_source=source,
        context_chapter_id=request.context_chapter_id,
        author_goal=request.author_goal,
        author_task_ids=request.author_task_ids,
    )
    handoff["author_intent"] = author_intent
    handoff["created_edition"] = created_edition.model_dump(mode="json")
    return handoff
