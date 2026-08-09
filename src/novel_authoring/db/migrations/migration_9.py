"""Schema migration 9: author-control intent and task projections."""

SQL = r"""
CREATE TABLE IF NOT EXISTS author_control_intents (
    intent_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    intent_type TEXT NOT NULL,
    subject_type TEXT NOT NULL,
    subject_id TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    horizon TEXT NOT NULL DEFAULT 'MID',
    priority INTEGER NOT NULL DEFAULT 100,
    status TEXT NOT NULL DEFAULT 'PLANNED',
    target_chapter_id TEXT,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_author_control_intents_scope
    ON author_control_intents(book_id, edition_id, status, horizon, priority, updated_at DESC);

CREATE TABLE IF NOT EXISTS author_control_tasks (
    task_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    title TEXT NOT NULL,
    task_type TEXT NOT NULL DEFAULT 'AUTHOR_TASK',
    description TEXT NOT NULL DEFAULT '',
    horizon TEXT NOT NULL DEFAULT 'MID',
    lifecycle_status TEXT NOT NULL DEFAULT 'BACKLOG',
    priority INTEGER NOT NULL DEFAULT 100,
    subject_type TEXT,
    subject_id TEXT,
    context_chapter_id TEXT,
    context_chapter_ordinal INTEGER,
    due_chapter_ordinal INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_author_control_tasks_scope
    ON author_control_tasks(
        book_id, edition_id, lifecycle_status, horizon, priority, updated_at DESC
    );

CREATE TABLE IF NOT EXISTS author_control_history (
    history_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    object_type TEXT NOT NULL,
    object_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    before_json TEXT NOT NULL DEFAULT '{}',
    after_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_author_control_history_object
    ON author_control_history(book_id, edition_id, object_type, object_id, created_at DESC);
"""

__all__ = ["SQL"]
