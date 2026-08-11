"""Schema migration 14: Novel Studio product semantics and resumable workflows."""

SQL = r"""
ALTER TABLE editions ADD COLUMN edition_purpose TEXT NOT NULL DEFAULT 'AUTHOR_REVISION';
ALTER TABLE editions ADD COLUMN official_role TEXT NOT NULL DEFAULT 'CANDIDATE';
ALTER TABLE editions ADD COLUMN fork_chapter_ordinal INTEGER;
ALTER TABLE editions ADD COLUMN created_by_action TEXT NOT NULL DEFAULT 'MIGRATION';
ALTER TABLE editions ADD COLUMN purpose_review_required INTEGER NOT NULL DEFAULT 0;

UPDATE editions
SET edition_purpose='SOURCE_BASE', purpose_review_required=0
WHERE edition_id='base';
UPDATE editions
SET official_role='CURRENT'
WHERE status='ACTIVE';
UPDATE editions
SET official_role='ARCHIVED'
WHERE status='ARCHIVED';
UPDATE editions
SET official_role='CANDIDATE'
WHERE status IN ('DRAFT', 'VALIDATED');
UPDATE editions
SET edition_purpose='AUTHOR_REVISION', purpose_review_required=1
WHERE edition_id<>'base' AND created_by_action='MIGRATION';

CREATE INDEX IF NOT EXISTS idx_editions_book_role
    ON editions(book_id, official_role, created_at DESC);

CREATE TABLE IF NOT EXISTS chapter_analysis_records (
    record_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    chapter_id TEXT NOT NULL REFERENCES chapters(chapter_id),
    analysis_layer TEXT NOT NULL,
    status TEXT NOT NULL,
    source_revision TEXT NOT NULL,
    result_path TEXT,
    result_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, chapter_id, analysis_layer, source_revision)
);
CREATE INDEX IF NOT EXISTS idx_chapter_analysis_reuse
    ON chapter_analysis_records(book_id, edition_id, analysis_layer, status, chapter_id);

CREATE TABLE IF NOT EXISTS pending_author_actions (
    pending_action_id TEXT PRIMARY KEY,
    action_key TEXT NOT NULL,
    action_type TEXT NOT NULL,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    chapter_id TEXT,
    target_chapter_ordinal INTEGER,
    author_goal TEXT NOT NULL DEFAULT '',
    innovation_json TEXT NOT NULL DEFAULT '{}',
    selected_author_tasks_json TEXT NOT NULL DEFAULT '[]',
    requested_stage TEXT NOT NULL,
    request_json TEXT NOT NULL DEFAULT '{}',
    required_context_json TEXT NOT NULL DEFAULT '{}',
    deepening_operation_id TEXT,
    resumed_handoff_id TEXT,
    status TEXT NOT NULL DEFAULT 'WAITING_FOR_CONTEXT',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_pending_author_action_active
    ON pending_author_actions(action_key)
    WHERE status IN ('WAITING_FOR_CONTEXT', 'CONTEXT_READY', 'RESUMING');
CREATE INDEX IF NOT EXISTS idx_pending_author_action_scope
    ON pending_author_actions(book_id, edition_id, status, created_at DESC);

CREATE TABLE IF NOT EXISTS original_proposal_versions (
    proposal_version_id TEXT PRIMARY KEY,
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
CREATE INDEX IF NOT EXISTS idx_original_proposal_current
    ON original_proposal_versions(book_id, edition_id, status, version_number DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_original_proposal_single_current
    ON original_proposal_versions(book_id, edition_id)
    WHERE status='CURRENT';
CREATE UNIQUE INDEX IF NOT EXISTS idx_original_proposal_single_generating
    ON original_proposal_versions(book_id, edition_id)
    WHERE status='GENERATING';

CREATE TABLE IF NOT EXISTS original_genesis_applies (
    apply_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    proposal_version_id TEXT NOT NULL REFERENCES original_proposal_versions(proposal_version_id),
    selected_foundation_id TEXT NOT NULL,
    selected_route_id TEXT NOT NULL,
    selected_title TEXT NOT NULL,
    apply_plan_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'APPLIED',
    applied_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(proposal_version_id, selected_foundation_id)
);

CREATE TABLE IF NOT EXISTS original_states (
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    state TEXT NOT NULL,
    current_proposal_version_id TEXT REFERENCES original_proposal_versions(proposal_version_id),
    accepted_apply_id TEXT REFERENCES original_genesis_applies(apply_id),
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY(book_id, edition_id)
);

CREATE TABLE IF NOT EXISTS active_narrative_spines (
    spine_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    proposal_version_id TEXT REFERENCES original_proposal_versions(proposal_version_id),
    route_id TEXT NOT NULL,
    direction TEXT NOT NULL,
    central_pressure TEXT NOT NULL,
    opportunity TEXT NOT NULL,
    risk TEXT NOT NULL,
    commitments_json TEXT NOT NULL DEFAULT '[]',
    open_alternatives_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_active_narrative_spines_scope
    ON active_narrative_spines(book_id, edition_id, status, created_at DESC);

ALTER TABLE workflow_handoffs ADD COLUMN task_running_started_at TEXT;
ALTER TABLE workflow_handoffs ADD COLUMN task_completed_at TEXT;
ALTER TABLE workflow_handoffs ADD COLUMN active_processing_seconds REAL NOT NULL DEFAULT 0;
ALTER TABLE workflow_handoffs ADD COLUMN processed_chapter_count INTEGER NOT NULL DEFAULT 0;
ALTER TABLE workflow_handoffs ADD COLUMN processed_char_count INTEGER NOT NULL DEFAULT 0;
"""

__all__ = ["SQL"]
