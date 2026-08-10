"""Strict contracts for author control commands and their projections."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AuthorControlHorizon(StrEnum):
    SHORT = "SHORT"
    MID = "MID"
    LONG = "LONG"


class AuthorTaskLifecycle(StrEnum):
    BACKLOG = "BACKLOG"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class AuthorIntentStatus(StrEnum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CommandResult(StrEnum):
    PLANNED = "PLANNED"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    REJECTED = "REJECTED"


class AuthorStateCommand(BaseModel):
    """A UI action that may become an intent/task, never an implicit Canon edit."""

    model_config = ConfigDict(extra="forbid")

    command_type: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    chapter_id: str | None = None
    character_id: str | None = None


class PlannedStateChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    change_type: str = Field(min_length=1)
    target_layer: str = Field(min_length=1)
    subject_type: str = Field(min_length=1)
    subject_id: str | None = None
    description: str = ""
    requires_revision: bool = False


class AuthorIntent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent_id: str = Field(min_length=1)
    book_id: str = Field(min_length=1)
    edition_id: str = Field(min_length=1)
    intent_type: str = Field(min_length=1)
    subject_type: str = Field(min_length=1)
    subject_id: str | None = None
    title: str = Field(min_length=1)
    description: str = ""
    horizon: AuthorControlHorizon = AuthorControlHorizon.MID
    priority: int = 100
    status: AuthorIntentStatus = AuthorIntentStatus.PLANNED
    target_chapter_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(min_length=1)
    updated_at: str = Field(min_length=1)
    version: int = 1


class AuthorTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(min_length=1)
    book_id: str = Field(min_length=1)
    edition_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    task_type: str = "AUTHOR_TASK"
    description: str = ""
    horizon: AuthorControlHorizon = AuthorControlHorizon.MID
    lifecycle_status: AuthorTaskLifecycle = AuthorTaskLifecycle.BACKLOG
    priority: int = 100
    subject_type: str | None = None
    subject_id: str | None = None
    context_chapter_id: str | None = None
    context_chapter_ordinal: int | None = None
    due_chapter_ordinal: int | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(min_length=1)
    updated_at: str = Field(min_length=1)
    version: int = 1


class CommandResolution(BaseModel):
    """Author-facing result with an explicit safety outcome."""

    model_config = ConfigDict(extra="forbid")

    result: CommandResult
    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    allowed_actions: list[str] = Field(default_factory=list)
    planned_change: PlannedStateChange | None = None
    intent: AuthorIntent | None = None
    task: AuthorTask | None = None
    handoff: dict[str, Any] | None = None
    history_id: str | None = None
    canon_changed: bool = False


HORIZON_LABELS: dict[str, str] = {
    AuthorControlHorizon.SHORT.value: "短期",
    AuthorControlHorizon.MID.value: "中期",
    AuthorControlHorizon.LONG.value: "长期",
}
LIFECYCLE_LABELS: dict[str, str] = {
    AuthorTaskLifecycle.BACKLOG.value: "待处理",
    AuthorTaskLifecycle.ACTIVE.value: "进行中",
    AuthorTaskLifecycle.BLOCKED.value: "受阻",
    AuthorTaskLifecycle.DONE.value: "已完成",
    AuthorTaskLifecycle.CANCELLED.value: "已取消",
}


__all__ = [
    "AuthorControlHorizon",
    "AuthorIntent",
    "AuthorIntentStatus",
    "AuthorStateCommand",
    "AuthorTask",
    "AuthorTaskLifecycle",
    "CommandResolution",
    "CommandResult",
    "HORIZON_LABELS",
    "LIFECYCLE_LABELS",
    "PlannedStateChange",
]
