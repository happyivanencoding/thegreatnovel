"""Stable Source State identities and deterministic projection snapshots."""

SQL = """
ALTER TABLE source_state_deltas ADD COLUMN state_key TEXT NOT NULL DEFAULT '';

UPDATE source_state_deltas
SET state_key = CASE category
    WHEN 'CHARACTER_STATE' THEN 'character:' || subject_id
    WHEN 'LOCATION' THEN 'location-state:' || subject_id
    WHEN 'ITEM' THEN 'item:' || COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'EQUIPMENT' THEN 'equipment:' || COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'RESOURCE' THEN 'resource:' || COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'CAPABILITY' THEN 'capability:' || COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'KNOWLEDGE' THEN 'knowledge:' || subject_id || ':' ||
        COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'RELATIONSHIP' THEN 'relationship:' || COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'FACTION' THEN 'faction:' || COALESCE(NULLIF(object_id, ''), subject_id)
    WHEN 'WORLD_RULE' THEN 'rule:' || COALESCE(NULLIF(object_id, ''), subject_id)
    ELSE 'promise:' || COALESCE(NULLIF(object_id, ''), subject_id)
END
WHERE state_key = '';

CREATE INDEX IF NOT EXISTS idx_source_state_deltas_state_key
    ON source_state_deltas(book_id, edition_id, state_key, chapter_ordinal);

CREATE TABLE IF NOT EXISTS source_state_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    edition_id TEXT NOT NULL,
    chapter_id TEXT,
    chapter_ordinal INTEGER NOT NULL,
    projection_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    UNIQUE(book_id, edition_id, chapter_ordinal)
);
CREATE INDEX IF NOT EXISTS idx_source_state_snapshots_lookup
    ON source_state_snapshots(book_id, edition_id, chapter_ordinal);
"""
