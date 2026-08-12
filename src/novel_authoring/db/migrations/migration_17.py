"""Schema migration 17: staged original Genesis innovation proposals."""

SQL = r"""
CREATE TABLE IF NOT EXISTS original_innovation_versions (
    innovation_proposal_version_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    version_number INTEGER NOT NULL,
    status TEXT NOT NULL,
    premise TEXT NOT NULL,
    handoff_id TEXT,
    proposal_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    ready_at TEXT,
    archived_at TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, version_number)
);
CREATE INDEX IF NOT EXISTS idx_original_innovation_current
    ON original_innovation_versions(book_id, edition_id, status, version_number DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_original_innovation_single_current
    ON original_innovation_versions(book_id, edition_id)
    WHERE status='CURRENT';
CREATE UNIQUE INDEX IF NOT EXISTS idx_original_innovation_single_generating
    ON original_innovation_versions(book_id, edition_id)
    WHERE status='GENERATING';

ALTER TABLE original_states ADD COLUMN current_innovation_proposal_version_id TEXT;
ALTER TABLE original_states ADD COLUMN selected_primary_innovation_id TEXT;
ALTER TABLE original_states ADD COLUMN optional_mix_notes TEXT NOT NULL DEFAULT '';
"""

__all__ = ["SQL"]
