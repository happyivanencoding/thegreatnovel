"""Author-facing state commands and read-only Story Game State projections.

The package is deliberately separate from Canon workflows.  Its writes are
author intent/task records; they do not append Canon events or approve drafts.
"""

from novel_authoring.author_control.models import (
    AuthorControlHorizon,
    AuthorIntent,
    AuthorStateCommand,
    AuthorTask,
    AuthorTaskLifecycle,
    CommandResolution,
    CommandResult,
    PlannedStateChange,
)
from novel_authoring.author_control.service import (
    author_control_view,
    execute_author_command,
    execute_author_intent,
    execute_author_task,
)
from novel_authoring.author_control.source_state import (
    SourceChapterStateDelta,
    SourceEvidenceLocator,
    SourceStateCategory,
    SourceStateOperation,
    SourceStateVerification,
    build_source_state_projection,
    record_source_chapter_deltas,
)

__all__ = [
    "AuthorControlHorizon",
    "AuthorIntent",
    "AuthorStateCommand",
    "AuthorTask",
    "AuthorTaskLifecycle",
    "CommandResolution",
    "CommandResult",
    "PlannedStateChange",
    "author_control_view",
    "execute_author_command",
    "execute_author_intent",
    "execute_author_task",
    "SourceChapterStateDelta",
    "SourceEvidenceLocator",
    "SourceStateCategory",
    "SourceStateOperation",
    "SourceStateVerification",
    "build_source_state_projection",
    "record_source_chapter_deltas",
]
