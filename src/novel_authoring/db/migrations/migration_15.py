"""Schema migration 15: progression contracts and scheduler overrides."""

SQL = r"""
CREATE TABLE IF NOT EXISTS progression_contract_versions (
    contract_record_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    contract_type TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    status TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    effective_from_boundary INTEGER,
    source TEXT NOT NULL,
    author_notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, contract_type, version_number)
);
CREATE INDEX IF NOT EXISTS idx_progression_contract_scope
    ON progression_contract_versions(
        book_id, edition_id, contract_type, status, version_number DESC
    );
CREATE UNIQUE INDEX IF NOT EXISTS idx_progression_contract_effective
    ON progression_contract_versions(book_id, edition_id, contract_type)
    WHERE status='EFFECTIVE';

CREATE TABLE IF NOT EXISTS serial_scheduler_overrides (
    override_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    chapter_ordinal INTEGER NOT NULL,
    primary_intent TEXT NOT NULL,
    secondary_intents_json TEXT NOT NULL DEFAULT '[]',
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, chapter_ordinal)
);
CREATE INDEX IF NOT EXISTS idx_scheduler_override_scope
    ON serial_scheduler_overrides(book_id, edition_id, chapter_ordinal DESC);
"""

__all__ = ["SQL"]
