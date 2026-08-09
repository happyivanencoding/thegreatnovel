"""Schema migration 10: chapter-aware source state deltas."""

SQL = r"""
CREATE TABLE IF NOT EXISTS source_state_deltas (
    delta_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    chapter_id TEXT NOT NULL,
    chapter_ordinal INTEGER NOT NULL,
    category TEXT NOT NULL,
    operation TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    object_id TEXT,
    statement TEXT NOT NULL,
    source_span_ids_json TEXT NOT NULL DEFAULT '[]',
    evidence_locator_json TEXT NOT NULL DEFAULT '[]',
    confidence REAL NOT NULL DEFAULT 0,
    verification_status TEXT NOT NULL DEFAULT 'UNKNOWN',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, delta_id)
);
CREATE INDEX IF NOT EXISTS idx_source_state_deltas_chapter
    ON source_state_deltas(book_id, edition_id, chapter_ordinal, category, created_at);
CREATE INDEX IF NOT EXISTS idx_source_state_deltas_subject
    ON source_state_deltas(book_id, edition_id, subject_id, chapter_ordinal);
"""

__all__ = ["SQL"]
