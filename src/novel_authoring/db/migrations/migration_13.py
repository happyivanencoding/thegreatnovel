"""Schema migration 13: author truth, knowledge and reveal planning."""

SQL = r"""
CREATE TABLE IF NOT EXISTS author_truths (
    truth_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    truth_type TEXT NOT NULL,
    subject_type TEXT NOT NULL,
    subject_id TEXT,
    object_type TEXT,
    object_id TEXT,
    title TEXT NOT NULL,
    statement TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'PROVISIONAL_TRUTH',
    confidence REAL NOT NULL DEFAULT 1.0,
    introduced_by TEXT NOT NULL DEFAULT 'AUTHOR_MANUAL',
    effective_from_chapter INTEGER NOT NULL,
    effective_until_chapter INTEGER,
    retroactive_scope TEXT NOT NULL DEFAULT 'FORWARD_ONLY',
    compatibility_status TEXT NOT NULL DEFAULT 'UNKNOWN',
    compatibility_summary TEXT NOT NULL DEFAULT '',
    must_remain_true INTEGER NOT NULL DEFAULT 1,
    tags_json TEXT NOT NULL DEFAULT '[]',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_author_truths_scope
    ON author_truths(book_id, edition_id, status, effective_from_chapter);
CREATE INDEX IF NOT EXISTS idx_author_truths_subject
    ON author_truths(book_id, edition_id, subject_type, subject_id);

CREATE TABLE IF NOT EXISTS truth_compatibility_evidence (
    evidence_id TEXT PRIMARY KEY,
    truth_id TEXT NOT NULL REFERENCES author_truths(truth_id) ON DELETE CASCADE,
    book_id TEXT NOT NULL,
    edition_id TEXT NOT NULL,
    verdict TEXT NOT NULL,
    chapter_id TEXT REFERENCES chapters(chapter_id),
    chapter_ordinal INTEGER,
    source_span_id TEXT REFERENCES source_spans(span_id),
    evidence_quote TEXT NOT NULL DEFAULT '',
    explanation TEXT NOT NULL DEFAULT '',
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_truth_compatibility_evidence_truth
    ON truth_compatibility_evidence(truth_id, chapter_ordinal, created_at);

CREATE TABLE IF NOT EXISTS reader_knowledge_edges (
    edge_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    truth_id TEXT NOT NULL REFERENCES author_truths(truth_id) ON DELETE CASCADE,
    state TEXT NOT NULL DEFAULT 'UNKNOWN',
    as_of_chapter_id TEXT REFERENCES chapters(chapter_id),
    as_of_chapter_ordinal INTEGER NOT NULL DEFAULT 0,
    first_exposed_chapter INTEGER,
    last_advanced_chapter INTEGER,
    evidence_json TEXT NOT NULL DEFAULT '[]',
    provenance TEXT NOT NULL DEFAULT 'AUTHOR_PLANNING',
    authority_status TEXT NOT NULL DEFAULT 'PROVISIONAL',
    provisional INTEGER NOT NULL DEFAULT 0,
    reveal_event_id TEXT,
    supersedes_edge_id TEXT REFERENCES reader_knowledge_edges(edge_id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_reader_knowledge_scope
    ON reader_knowledge_edges(
        book_id, edition_id, truth_id, as_of_chapter_ordinal DESC, created_at DESC
    );

CREATE TABLE IF NOT EXISTS truth_character_knowledge (
    edge_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    truth_id TEXT NOT NULL REFERENCES author_truths(truth_id) ON DELETE CASCADE,
    character_id TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'UNKNOWN',
    as_of_chapter_id TEXT REFERENCES chapters(chapter_id),
    as_of_chapter_ordinal INTEGER NOT NULL DEFAULT 0,
    first_exposed_chapter INTEGER,
    last_advanced_chapter INTEGER,
    evidence_json TEXT NOT NULL DEFAULT '[]',
    provenance TEXT NOT NULL DEFAULT 'AUTHOR_PLANNING',
    authority_status TEXT NOT NULL DEFAULT 'PROVISIONAL',
    provisional INTEGER NOT NULL DEFAULT 0,
    reveal_event_id TEXT,
    supersedes_edge_id TEXT REFERENCES truth_character_knowledge(edge_id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_truth_character_knowledge_scope
    ON truth_character_knowledge(
        book_id, edition_id, character_id, truth_id,
        as_of_chapter_ordinal DESC, created_at DESC
    );

CREATE TABLE IF NOT EXISTS reveal_plans (
    reveal_plan_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    truth_id TEXT NOT NULL REFERENCES author_truths(truth_id) ON DELETE CASCADE,
    target TEXT NOT NULL,
    target_entity_id TEXT,
    strategy TEXT NOT NULL DEFAULT '',
    target_chapter_min INTEGER NOT NULL,
    target_chapter_max INTEGER,
    horizon TEXT NOT NULL DEFAULT 'MID',
    priority INTEGER NOT NULL DEFAULT 100,
    status TEXT NOT NULL DEFAULT 'PLANNED',
    required_preconditions_json TEXT NOT NULL DEFAULT '[]',
    forbidden_conditions_json TEXT NOT NULL DEFAULT '[]',
    reveal_depth TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_reveal_plans_scope
    ON reveal_plans(book_id, edition_id, target_chapter_min, target_chapter_max, status);

CREATE TABLE IF NOT EXISTS reveal_agenda_overrides (
    override_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    truth_id TEXT NOT NULL REFERENCES author_truths(truth_id) ON DELETE CASCADE,
    reveal_plan_id TEXT REFERENCES reveal_plans(reveal_plan_id) ON DELETE CASCADE,
    chapter_ordinal INTEGER NOT NULL,
    agenda_bucket TEXT NOT NULL,
    reveal_depth TEXT,
    reason TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, truth_id, chapter_ordinal)
);
CREATE INDEX IF NOT EXISTS idx_reveal_agenda_overrides_scope
    ON reveal_agenda_overrides(book_id, edition_id, chapter_ordinal);

CREATE TABLE IF NOT EXISTS reveal_events (
    reveal_event_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    truth_id TEXT NOT NULL REFERENCES author_truths(truth_id),
    reveal_plan_id TEXT REFERENCES reveal_plans(reveal_plan_id),
    target TEXT NOT NULL,
    target_entity_id TEXT,
    depth TEXT NOT NULL,
    evidence_quote TEXT NOT NULL,
    expected_knowledge_state TEXT NOT NULL,
    realized_knowledge_state TEXT NOT NULL,
    chapter_id TEXT REFERENCES chapters(chapter_id),
    chapter_ordinal INTEGER NOT NULL,
    draft_id TEXT,
    commit_id TEXT,
    status TEXT NOT NULL DEFAULT 'PROVISIONAL',
    created_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_reveal_events_scope
    ON reveal_events(book_id, edition_id, truth_id, chapter_ordinal, status);

CREATE TABLE IF NOT EXISTS open_creative_questions (
    question_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    title TEXT NOT NULL,
    question TEXT NOT NULL,
    subject_type TEXT,
    subject_id TEXT,
    horizon TEXT NOT NULL DEFAULT 'LONG',
    status TEXT NOT NULL DEFAULT 'OPEN_QUESTION',
    resolved_truth_id TEXT REFERENCES author_truths(truth_id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS secret_candidates (
    candidate_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL DEFAULT 'base',
    title TEXT NOT NULL,
    statement TEXT NOT NULL,
    truth_type TEXT NOT NULL DEFAULT 'CUSTOM',
    subject_type TEXT,
    subject_id TEXT,
    evidence_json TEXT NOT NULL DEFAULT '[]',
    confidence REAL NOT NULL DEFAULT 0.5,
    source TEXT NOT NULL DEFAULT 'INITIALIZATION_INFERRED',
    status TEXT NOT NULL DEFAULT 'INFERRED_SECRET_CANDIDATE',
    resolved_truth_id TEXT REFERENCES author_truths(truth_id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_secret_candidates_scope
    ON secret_candidates(book_id, edition_id, status, created_at);

ALTER TABLE book_profile_refresh_proposals
    ADD COLUMN analysis_status TEXT NOT NULL DEFAULT 'PROPOSAL_READY';
ALTER TABLE book_profile_refresh_proposals ADD COLUMN handoff_id TEXT;
ALTER TABLE book_profile_refresh_proposals
    ADD COLUMN analysis_json TEXT NOT NULL DEFAULT '{}';
"""

__all__ = ["SQL"]
