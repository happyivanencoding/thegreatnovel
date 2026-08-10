"""Schema migration 12: chapter coverage and versioned book profiles."""

SQL = r"""
CREATE TABLE IF NOT EXISTS source_state_chapter_coverage (
    coverage_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    chapter_id TEXT NOT NULL REFERENCES chapters(chapter_id),
    chapter_ordinal INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'NOT_STARTED',
    verified_delta_count INTEGER NOT NULL DEFAULT 0,
    uncertain_finding_count INTEGER NOT NULL DEFAULT 0,
    task_id TEXT,
    handoff_id TEXT,
    started_at TEXT,
    completed_at TEXT,
    error_message TEXT,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, chapter_id)
);
CREATE INDEX IF NOT EXISTS idx_source_state_coverage_scope
    ON source_state_chapter_coverage(book_id, edition_id, chapter_ordinal, status);

INSERT OR IGNORE INTO source_state_chapter_coverage(
    coverage_id, book_id, edition_id, chapter_id, chapter_ordinal, status,
    verified_delta_count, uncertain_finding_count, completed_at, updated_at, version
)
SELECT
    'source-coverage:' || d.book_id || ':' || d.edition_id || ':' || d.chapter_id,
    d.book_id,
    d.edition_id,
    d.chapter_id,
    d.chapter_ordinal,
    CASE
        WHEN SUM(CASE WHEN d.verification_status='SOURCE_VERIFIED' THEN 1 ELSE 0 END) > 0
            THEN 'COMPLETE_WITH_CHANGES'
        ELSE 'PARTIAL'
    END,
    SUM(CASE WHEN d.verification_status='SOURCE_VERIFIED' THEN 1 ELSE 0 END),
    SUM(CASE WHEN d.verification_status<>'SOURCE_VERIFIED' THEN 1 ELSE 0 END),
    MAX(d.created_at),
    MAX(d.created_at),
    1
FROM source_state_deltas d
GROUP BY d.book_id, d.edition_id, d.chapter_id, d.chapter_ordinal;

INSERT OR IGNORE INTO source_state_chapter_coverage(
    coverage_id, book_id, edition_id, chapter_id, chapter_ordinal, status,
    verified_delta_count, uncertain_finding_count, task_id, handoff_id,
    completed_at, updated_at, version
)
SELECT
    'source-coverage:' || t.book_id || ':' || t.edition_id || ':' || t.context_chapter_id,
    t.book_id,
    t.edition_id,
    t.context_chapter_id,
    t.context_chapter_ordinal,
    CASE
        WHEN EXISTS(
            SELECT 1 FROM source_state_deltas d
            WHERE d.book_id=t.book_id AND d.edition_id=t.edition_id
              AND d.chapter_id=t.context_chapter_id
              AND d.verification_status='SOURCE_VERIFIED'
        ) THEN 'COMPLETE_WITH_CHANGES'
        ELSE 'COMPLETE_NO_CHANGE'
    END,
    (
        SELECT COUNT(*) FROM source_state_deltas d
        WHERE d.book_id=t.book_id AND d.edition_id=t.edition_id
          AND d.chapter_id=t.context_chapter_id
          AND d.verification_status='SOURCE_VERIFIED'
    ),
    (
        SELECT COUNT(*) FROM source_state_deltas d
        WHERE d.book_id=t.book_id AND d.edition_id=t.edition_id
          AND d.chapter_id=t.context_chapter_id
          AND d.verification_status<>'SOURCE_VERIFIED'
    ),
    t.task_id,
    json_extract(t.payload_json, '$.handoff_id'),
    t.updated_at,
    t.updated_at,
    1
FROM author_control_tasks t
WHERE t.task_type='SOURCE_STATE_HYDRATION'
  AND t.lifecycle_status='DONE'
  AND t.context_chapter_id IS NOT NULL;

UPDATE source_state_chapter_coverage
SET status = CASE
        WHEN verified_delta_count > 0 THEN 'COMPLETE_WITH_CHANGES'
        ELSE 'COMPLETE_NO_CHANGE'
    END,
    task_id = (
        SELECT t.task_id FROM author_control_tasks t
        WHERE t.book_id=source_state_chapter_coverage.book_id
          AND t.edition_id=source_state_chapter_coverage.edition_id
          AND t.context_chapter_id=source_state_chapter_coverage.chapter_id
          AND t.task_type='SOURCE_STATE_HYDRATION'
          AND t.lifecycle_status='DONE'
        ORDER BY t.updated_at DESC LIMIT 1
    ),
    handoff_id = (
        SELECT json_extract(t.payload_json, '$.handoff_id')
        FROM author_control_tasks t
        WHERE t.book_id=source_state_chapter_coverage.book_id
          AND t.edition_id=source_state_chapter_coverage.edition_id
          AND t.context_chapter_id=source_state_chapter_coverage.chapter_id
          AND t.task_type='SOURCE_STATE_HYDRATION'
          AND t.lifecycle_status='DONE'
        ORDER BY t.updated_at DESC LIMIT 1
    )
WHERE EXISTS (
    SELECT 1 FROM author_control_tasks t
    WHERE t.book_id=source_state_chapter_coverage.book_id
      AND t.edition_id=source_state_chapter_coverage.edition_id
      AND t.context_chapter_id=source_state_chapter_coverage.chapter_id
      AND t.task_type='SOURCE_STATE_HYDRATION'
      AND t.lifecycle_status='DONE'
);

CREATE TABLE IF NOT EXISTS book_profile_versions (
    profile_version_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    version_number INTEGER NOT NULL,
    baseline_json TEXT NOT NULL DEFAULT '{}',
    author_edits_json TEXT NOT NULL DEFAULT '[]',
    reason TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, version_number)
);
CREATE INDEX IF NOT EXISTS idx_book_profile_versions_scope
    ON book_profile_versions(book_id, edition_id, version_number DESC);

CREATE TABLE IF NOT EXISTS book_profile_refresh_proposals (
    proposal_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    source_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    proposed_baseline_json TEXT NOT NULL DEFAULT '{}',
    summary TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_book_profile_proposals_scope
    ON book_profile_refresh_proposals(book_id, edition_id, status, created_at DESC);
"""

__all__ = ["SQL"]
