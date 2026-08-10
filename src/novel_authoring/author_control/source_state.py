"""Chapter-aware source state ledger and read-only projection helpers.

This module deliberately lives beside Author Control.  Source state is a
verified reading of the immutable book, not a Canon event stream and not an
author command.  The ledger can therefore be hydrated chapter by chapter
without changing the book or the Canon projection.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from collections.abc import Iterable
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.db.database import Database
from novel_authoring.utils import utc_now


class SourceStateCategory(StrEnum):
    CHARACTER_STATE = "CHARACTER_STATE"
    LOCATION = "LOCATION"
    ITEM = "ITEM"
    EQUIPMENT = "EQUIPMENT"
    RESOURCE = "RESOURCE"
    CAPABILITY = "CAPABILITY"
    KNOWLEDGE = "KNOWLEDGE"
    RELATIONSHIP = "RELATIONSHIP"
    FACTION = "FACTION"
    WORLD_RULE = "WORLD_RULE"
    TASK_OR_PROMISE = "TASK_OR_PROMISE"


class SourceStateOperation(StrEnum):
    ADD = "ADD"
    REMOVE = "REMOVE"
    UPDATE = "UPDATE"
    TRANSFER = "TRANSFER"
    ACQUIRE = "ACQUIRE"
    LOSE = "LOSE"
    EQUIP = "EQUIP"
    UNEQUIP = "UNEQUIP"
    LEARN = "LEARN"
    REVEAL = "REVEAL"
    HIDE = "HIDE"
    RELATIONSHIP_CHANGE = "RELATIONSHIP_CHANGE"
    LOCATION_CHANGE = "LOCATION_CHANGE"


class SourceStateVerification(StrEnum):
    SOURCE_VERIFIED = "SOURCE_VERIFIED"
    SOURCE_PARTIAL = "SOURCE_PARTIAL"
    UNKNOWN = "UNKNOWN"


_OBJECT_ID_CATEGORIES = {
    SourceStateCategory.ITEM,
    SourceStateCategory.EQUIPMENT,
    SourceStateCategory.RESOURCE,
    SourceStateCategory.CAPABILITY,
    SourceStateCategory.KNOWLEDGE,
    SourceStateCategory.RELATIONSHIP,
}


def derive_state_key(
    category: SourceStateCategory, subject_id: str, object_id: str | None
) -> str:
    """Return a readable business identity; this is not a content hash."""

    if category is SourceStateCategory.CHARACTER_STATE:
        return f"character:{subject_id}"
    if category is SourceStateCategory.LOCATION:
        return f"location-state:{subject_id}"
    if category is SourceStateCategory.ITEM:
        return f"item:{object_id or subject_id}"
    if category is SourceStateCategory.EQUIPMENT:
        return f"equipment:{object_id or subject_id}"
    if category is SourceStateCategory.RESOURCE:
        return f"resource:{object_id or subject_id}"
    if category is SourceStateCategory.CAPABILITY:
        return f"capability:{object_id or subject_id}"
    if category is SourceStateCategory.KNOWLEDGE:
        return f"knowledge:{subject_id}:{object_id or subject_id}"
    if category is SourceStateCategory.RELATIONSHIP:
        return f"relationship:{object_id or subject_id}"
    if category is SourceStateCategory.FACTION:
        return f"faction:{object_id or subject_id}"
    if category is SourceStateCategory.WORLD_RULE:
        return f"rule:{object_id or subject_id}"
    return f"promise:{object_id or subject_id}"


class SourceEvidenceLocator(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_span_id: str = Field(min_length=1)
    note: str = ""


class SourceChapterStateDelta(BaseModel):
    """One auditable source-derived state change at a chapter boundary."""

    model_config = ConfigDict(extra="forbid")

    delta_id: str = Field(default_factory=lambda: f"source-delta-{uuid.uuid4().hex}")
    book_id: str = Field(min_length=1)
    edition_id: str = Field(default="base", min_length=1)
    chapter_id: str = Field(min_length=1)
    chapter_ordinal: int = Field(ge=1)
    category: SourceStateCategory
    operation: SourceStateOperation
    subject_id: str = Field(min_length=1)
    object_id: str | None = None
    state_key: str | None = None
    statement: str = Field(min_length=1)
    source_span_ids: list[str] = Field(default_factory=list)
    evidence_locator: list[SourceEvidenceLocator] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0, le=1)
    verification_status: SourceStateVerification = SourceStateVerification.UNKNOWN
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=utc_now)
    version: int = 1

    @model_validator(mode="after")
    def validate_evidence(self) -> SourceChapterStateDelta:
        span_ids = set(self.source_span_ids)
        locator_ids = {item.source_span_id for item in self.evidence_locator}
        if self.verification_status is SourceStateVerification.SOURCE_VERIFIED and not (
            span_ids or locator_ids
        ):
            raise ValueError("SOURCE_VERIFIED 状态必须带有 source span 证据")
        if locator_ids - span_ids:
            self.source_span_ids = [*self.source_span_ids, *sorted(locator_ids - span_ids)]
        derived = derive_state_key(self.category, self.subject_id, self.object_id)
        if self.state_key and self.state_key != derived:
            raise ValueError("state_key 必须与 category/subject_id/object_id 的业务身份一致")
        self.state_key = derived
        return self


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _payload(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(str(value or "{}"))
    except (TypeError, ValueError):
        return {}
    return dict(parsed) if isinstance(parsed, dict) else {}


def _source_span_ids(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def _locator(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def source_delta_from_row(row: sqlite3.Row) -> SourceChapterStateDelta:
    return SourceChapterStateDelta(
        delta_id=str(row["delta_id"]),
        book_id=str(row["book_id"]),
        edition_id=str(row["edition_id"]),
        chapter_id=str(row["chapter_id"]),
        chapter_ordinal=int(row["chapter_ordinal"]),
        category=SourceStateCategory(str(row["category"])),
        operation=SourceStateOperation(str(row["operation"])),
        subject_id=str(row["subject_id"]),
        object_id=None if row["object_id"] is None else str(row["object_id"]),
        state_key=str(row["state_key"] or "") or None,
        statement=str(row["statement"]),
        source_span_ids=_source_span_ids(
            _json_load(row["source_span_ids_json"])
        ),
        evidence_locator=[
            SourceEvidenceLocator.model_validate(item)
            for item in _locator(_json_load(row["evidence_locator_json"]))
        ],
        confidence=float(row["confidence"]),
        verification_status=SourceStateVerification(str(row["verification_status"])),
        payload=_payload(row["payload_json"]),
        created_at=str(row["created_at"]),
        version=int(row["version"]),
    )


def _json_load(value: Any) -> Any:
    try:
        return json.loads(str(value or "[]"))
    except (TypeError, ValueError):
        return []


def _validate_source_evidence(
    connection: sqlite3.Connection, delta: SourceChapterStateDelta
) -> None:
    if not delta.source_span_ids:
        return
    placeholders = ",".join("?" for _ in delta.source_span_ids)
    rows = connection.execute(
        "SELECT span_id, chapter_id FROM source_spans "
        f"WHERE book_id=? AND span_id IN ({placeholders})",
        (delta.book_id, *delta.source_span_ids),
    ).fetchall()
    found = {str(row["span_id"]): str(row["chapter_id"] or "") for row in rows}
    missing = set(delta.source_span_ids) - set(found)
    if missing:
        raise ValueError(f"Source State 使用了不存在的 source span：{sorted(missing)}")
    wrong_chapter = [
        span_id for span_id, chapter_id in found.items() if chapter_id != delta.chapter_id
    ]
    if wrong_chapter:
        raise ValueError("Source State evidence 必须属于声明的 chapter_id")


def record_source_chapter_deltas(
    database: Database,
    book_id: str,
    edition_id: str,
    deltas: Iterable[SourceChapterStateDelta],
) -> list[SourceChapterStateDelta]:
    """Persist validated source deltas without touching Canon tables."""

    values: list[SourceChapterStateDelta] = []
    for delta in deltas:
        # A name-only observation remains auditable, but cannot become a
        # verified object state without a stable object identity.
        if (
            delta.verification_status is SourceStateVerification.SOURCE_VERIFIED
            and delta.category in _OBJECT_ID_CATEGORIES
            and not delta.object_id
        ):
            delta = delta.model_copy(
                update={"verification_status": SourceStateVerification.SOURCE_PARTIAL}
            )
        values.append(delta)
    database.initialize()
    with database.connect() as connection:
        book = connection.execute("SELECT 1 FROM books WHERE book_id=?", (book_id,)).fetchone()
        if book is None:
            raise ValueError("book 不存在")
        earliest_new_ordinal: int | None = None
        chapter_rows = {
            str(row["chapter_id"]): int(row["ordinal"])
            for row in connection.execute(
                "SELECT chapter_id, ordinal FROM chapters WHERE book_id=?", (book_id,)
            ).fetchall()
        }
        for delta in values:
            if delta.book_id != book_id or delta.edition_id != edition_id:
                raise ValueError("Source State delta 的 book/edition scope 不匹配")
            if delta.chapter_id not in chapter_rows:
                raise ValueError(f"章节不存在：{delta.chapter_id}")
            if chapter_rows[delta.chapter_id] != delta.chapter_ordinal:
                raise ValueError("Source State delta 的 chapter_ordinal 与章节不一致")
            _validate_source_evidence(connection, delta)
            existing = connection.execute(
                "SELECT * FROM source_state_deltas WHERE delta_id=?",
                (delta.delta_id,),
            ).fetchone()
            if existing is not None:
                existing_delta = source_delta_from_row(existing)
                if existing_delta.model_dump(mode="json") != delta.model_dump(mode="json"):
                    raise ValueError(f"Source State delta 已存在且内容不同：{delta.delta_id}")
                continue
            connection.execute(
                """
                INSERT INTO source_state_deltas(
                    delta_id, book_id, edition_id, chapter_id, chapter_ordinal,
                    category, operation, subject_id, object_id, state_key, statement,
                    source_span_ids_json, evidence_locator_json, confidence,
                    verification_status, payload_json, created_at, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    delta.delta_id,
                    delta.book_id,
                    delta.edition_id,
                    delta.chapter_id,
                    delta.chapter_ordinal,
                    delta.category.value,
                    delta.operation.value,
                    delta.subject_id,
                    delta.object_id,
                    delta.state_key,
                    delta.statement,
                    _json(delta.source_span_ids),
                    _json([item.model_dump(mode="json") for item in delta.evidence_locator]),
                    delta.confidence,
                    delta.verification_status.value,
                    _json(delta.payload),
                    delta.created_at,
                    delta.version,
                ),
            )
            earliest_new_ordinal = (
                delta.chapter_ordinal
                if earliest_new_ordinal is None
                else min(earliest_new_ordinal, delta.chapter_ordinal)
            )
        if earliest_new_ordinal is not None:
            # A late-arriving earlier delta invalidates every cache at or after
            # that boundary.  The ledger remains the only authority and the
            # next projection call deterministically rebuilds the cache.
            connection.execute(
                "DELETE FROM source_state_snapshots "
                "WHERE book_id=? AND edition_id=? AND chapter_ordinal>=?",
                (book_id, edition_id, earliest_new_ordinal),
            )
    return values


def list_source_chapter_deltas(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    through_chapter_ordinal: int | None = None,
) -> list[SourceChapterStateDelta]:
    sql = (
        "SELECT * FROM source_state_deltas WHERE book_id=? AND edition_id=?"
    )
    parameters: list[Any] = [book_id, edition_id]
    if through_chapter_ordinal is not None:
        sql += " AND chapter_ordinal<=?"
        parameters.append(through_chapter_ordinal)
    sql += " ORDER BY chapter_ordinal, created_at, delta_id"
    return [
        source_delta_from_row(row)
        for row in connection.execute(sql, tuple(parameters)).fetchall()
    ]


def _delta_record(delta: SourceChapterStateDelta) -> dict[str, Any]:
    payload = dict(delta.payload)
    owner_id = str(
        payload.get("owner_id")
        or payload.get("holder_id")
        or payload.get("character_id")
        or delta.subject_id
    )
    return {
        "record_id": f"source:{delta.delta_id}",
        "state_key": delta.state_key,
        "name": str(payload.get("name") or delta.object_id or delta.subject_id),
        "category": delta.category.value.lower(),
        "layer": delta.verification_status.value,
        "status": delta.verification_status.value,
        "status_label": {
            SourceStateVerification.SOURCE_VERIFIED.value: "✓ 原文已确认",
            SourceStateVerification.SOURCE_PARTIAL.value: "原文有线索",
            SourceStateVerification.UNKNOWN.value: "尚未知",
        }[delta.verification_status.value],
        "statement": delta.statement,
        "description": str(payload.get("description") or delta.statement),
        "use": payload.get("use") or payload.get("usage"),
        "constraints": payload.get("constraints") or payload.get("constraint"),
        "related_ability_id": payload.get("related_ability_id"),
        "related_person_id": payload.get("related_person_id"),
        "related_relationship_id": payload.get("related_relationship_id"),
        "related_task_id": payload.get("related_task_id"),
        "related_plot_thread_id": payload.get("related_plot_thread_id"),
        "subject_id": delta.subject_id,
        "object_id": delta.object_id,
        "owner_id": owner_id,
        "current_holder_id": owner_id,
        "from_entity_id": payload.get("from_entity_id"),
        "to_entity_id": payload.get("to_entity_id"),
        "knower_id": payload.get("knower_id"),
        "topic_id": payload.get("topic_id") or delta.object_id,
        "topic_name": payload.get("topic_name") or payload.get("topic"),
        "knowledge_state": payload.get("knowledge_state") or payload.get("visibility_state"),
        "quantity": payload.get("quantity"),
        "equipped": bool(payload.get("equipped", False)),
        "slot": payload.get("slot") or payload.get("equipment_slot"),
        "visible": payload.get("visible", True),
        "visibility_status": "VISIBLE" if payload.get("visible", True) else "HIDDEN",
        "operation": delta.operation.value,
        "chapter_id": delta.chapter_id,
        "chapter_ordinal": delta.chapter_ordinal,
        "evidence_chapter_ordinal": delta.chapter_ordinal,
        "evidence_excerpt": " ".join(
            item.note for item in delta.evidence_locator if item.note
        ),
        "source_span_ids": list(delta.source_span_ids),
        "evidence_locator": [item.model_dump(mode="json") for item in delta.evidence_locator],
        "confidence": delta.confidence,
        "attributes": [
            {"label": str(key), "value": str(value)}
            for key, value in payload.items()
            if value is not None and not isinstance(value, (dict, list))
        ],
        "raw": delta.model_dump(mode="json"),
    }


def build_source_state_projection(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    chapter_id: str | None,
    chapter_ordinal: int | None,
) -> dict[str, Any]:
    """Replay only verified source deltas up to the requested chapter."""

    deltas = list_source_chapter_deltas(
        connection,
        book_id,
        edition_id,
        through_chapter_ordinal=chapter_ordinal,
    )
    verified = [
        delta
        for delta in deltas
        if delta.verification_status is SourceStateVerification.SOURCE_VERIFIED
    ]
    uncertain = [
        delta
        for delta in deltas
        if delta.verification_status is not SourceStateVerification.SOURCE_VERIFIED
    ]
    records: dict[str, dict[str, dict[str, Any]]] = {}
    applied_delta_ids: set[str] = set()
    snapshot_ordinal: int | None = None
    if chapter_ordinal is not None:
        snapshot = connection.execute(
            "SELECT chapter_ordinal, projection_json FROM source_state_snapshots "
            "WHERE book_id=? AND edition_id=? AND chapter_ordinal<=? "
            "ORDER BY chapter_ordinal DESC LIMIT 1",
            (book_id, edition_id, chapter_ordinal),
        ).fetchone()
        if snapshot is not None:
            cached = _payload(snapshot["projection_json"])
            raw_records = cached.get("records")
            if isinstance(raw_records, dict):
                records = {
                    str(category): {
                        str(key): dict(value)
                        for key, value in values.items()
                        if isinstance(value, dict)
                    }
                    for category, values in raw_records.items()
                    if isinstance(values, dict)
                }
            applied_delta_ids = {str(item) for item in cached.get("applied_delta_ids", [])}
            snapshot_ordinal = int(snapshot["chapter_ordinal"])
    for delta in verified:
        if delta.delta_id in applied_delta_ids:
            continue
        _apply_delta(records, delta)
        applied_delta_ids.add(delta.delta_id)
    if chapter_ordinal is not None and verified:
        _write_source_snapshot(
            connection,
            book_id,
            edition_id,
            chapter_id=chapter_id,
            chapter_ordinal=chapter_ordinal,
            records=records,
            applied_delta_ids=applied_delta_ids,
        )
    selected_chapter_has_delta = any(
        delta.chapter_id == chapter_id for delta in verified
    )
    previous_chapter = max(
        (
            delta.chapter_ordinal
            for delta in verified
            if chapter_ordinal is None or delta.chapter_ordinal < chapter_ordinal
        ),
        default=None,
    )
    queued = _hydration_task(connection, book_id, edition_id, chapter_id)
    return {
        "available": bool(verified),
        "projection_status": "READY" if verified else "MISSING",
        "ledger_delta_count": len(deltas),
        "verified_delta_count": len(verified),
        "uncertain_delta_count": len(uncertain),
        "selected_chapter_has_delta": selected_chapter_has_delta,
        "previous_projection_chapter_ordinal": previous_chapter,
        "snapshot_chapter_ordinal": snapshot_ordinal,
        "records": {
            category: list(values.values()) for category, values in records.items()
        },
        "uncertain_records": [_delta_record(delta) for delta in uncertain],
        "hydration": {
            "required": not selected_chapter_has_delta,
            "queued": queued is not None,
            "task": queued,
            "handoff": None if queued is None else queued.get("handoff"),
            "progress": [] if queued is None else list(queued.get("progress", [])),
        },
        "layer": "SOURCE_VERIFIED",
    }


def _apply_delta(
    records: dict[str, dict[str, dict[str, Any]]], delta: SourceChapterStateDelta
) -> None:
    category = delta.category.value
    collection = records.setdefault(category, {})
    key = str(
        delta.state_key
        or derive_state_key(delta.category, delta.subject_id, delta.object_id)
    )
    if delta.operation in {SourceStateOperation.REMOVE, SourceStateOperation.LOSE}:
        collection.pop(key, None)
        return
    old = collection.get(key)
    payload = dict(delta.payload)
    if old is not None:
        old_raw_value = old.get("raw")
        old_raw: dict[str, Any] = old_raw_value if isinstance(old_raw_value, dict) else {}
        old_payload_value = old_raw.get("payload")
        old_payload: dict[str, Any] = (
            old_payload_value if isinstance(old_payload_value, dict) else {}
        )
        payload = {**old_payload, **payload}
    if delta.operation is SourceStateOperation.TRANSFER:
        new_owner = (
            payload.get("to_subject_id")
            or payload.get("new_owner_id")
            or payload.get("owner_id")
        )
        if new_owner:
            payload["owner_id"] = new_owner
            delta = delta.model_copy(update={"subject_id": str(new_owner)})
    if delta.operation is SourceStateOperation.EQUIP:
        payload["equipped"] = True
    elif delta.operation is SourceStateOperation.UNEQUIP:
        payload["equipped"] = False
    elif delta.operation is SourceStateOperation.REVEAL:
        payload["visible"] = True
    elif delta.operation is SourceStateOperation.HIDE:
        payload["visible"] = False
    delta = delta.model_copy(update={"payload": payload})
    record = _delta_record(delta)
    record["first_confirmed_chapter_ordinal"] = (
        old.get("first_confirmed_chapter_ordinal", old.get("chapter_ordinal"))
        if old is not None
        else delta.chapter_ordinal
    )
    record["first_acquired_chapter_ordinal"] = (
        old.get("first_acquired_chapter_ordinal")
        if old is not None and old.get("first_acquired_chapter_ordinal") is not None
        else delta.chapter_ordinal
        if delta.operation in {SourceStateOperation.ADD, SourceStateOperation.ACQUIRE}
        else None
    )
    record["recent_confirmed_chapter_ordinal"] = delta.chapter_ordinal
    collection[key] = record


def _write_source_snapshot(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    chapter_id: str | None,
    chapter_ordinal: int,
    records: dict[str, dict[str, dict[str, Any]]],
    applied_delta_ids: set[str],
) -> None:
    connection.execute(
        """
        INSERT INTO source_state_snapshots(
            snapshot_id, book_id, edition_id, chapter_id, chapter_ordinal,
            projection_json, created_at, version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(book_id, edition_id, chapter_ordinal) DO UPDATE SET
            chapter_id=excluded.chapter_id,
            projection_json=excluded.projection_json,
            created_at=excluded.created_at,
            version=excluded.version
        """,
        (
            f"source-snapshot:{book_id}:{edition_id}:{chapter_ordinal}",
            book_id,
            edition_id,
            chapter_id,
            chapter_ordinal,
            _json({"records": records, "applied_delta_ids": sorted(applied_delta_ids)}),
            utc_now(),
        ),
    )


def _hydration_task(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapter_id: str | None,
) -> dict[str, Any] | None:
    if not chapter_id:
        return None
    table = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='author_control_tasks'"
    ).fetchone()
    if table is None:
        return None
    row = connection.execute(
        """
        SELECT task_id, title, task_type, description, horizon,
               lifecycle_status, context_chapter_id, context_chapter_ordinal,
               payload_json, updated_at
        FROM author_control_tasks
        WHERE book_id=? AND edition_id=? AND task_type='SOURCE_STATE_HYDRATION'
          AND context_chapter_id=? AND lifecycle_status NOT IN ('DONE', 'CANCELLED')
        ORDER BY updated_at DESC, task_id DESC LIMIT 1
        """,
        (book_id, edition_id, chapter_id),
    ).fetchone()
    if row is None:
        return None
    task_payload = _payload(row["payload_json"])
    handoff_id = str(task_payload.get("handoff_id") or "")
    handoff: dict[str, Any] | None = None
    if handoff_id:
        handoff_row = connection.execute(
            "SELECT handoff_id, status, task_directory FROM workflow_handoffs "
            "WHERE handoff_id=?",
            (handoff_id,),
        ).fetchone()
        if handoff_row is not None:
            handoff = {
                "handoff_id": str(handoff_row["handoff_id"]),
                "status": str(handoff_row["status"]),
                "task_directory": str(handoff_row["task_directory"]),
                "instruction_url": (
                    f"/api/books/{book_id}/editions/{edition_id}/handoffs/"
                    f"{handoff_id}/instruction"
                ),
                "result_url": (
                    f"/api/books/{book_id}/editions/{edition_id}/handoffs/"
                    f"{handoff_id}/result"
                ),
                "collect_url": (
                    f"/api/books/{book_id}/editions/{edition_id}/source-state-hydration/"
                    f"{handoff_id}/collect"
                ),
            }
    return {
        "task_id": str(row["task_id"]),
        "title": str(row["title"]),
        "task_type": str(row["task_type"]),
        "description": str(row["description"] or ""),
        "horizon": str(row["horizon"]),
        "lifecycle_status": str(row["lifecycle_status"]),
        "context_chapter_id": str(row["context_chapter_id"]),
        "context_chapter_ordinal": row["context_chapter_ordinal"],
        "payload": task_payload,
        "handoff": handoff,
        "progress": [
            {"key": "request", "label": "请求章节状态", "done": True},
            {
                "key": "handoff",
                "label": "准备 Codex handoff",
                "done": handoff is not None,
            },
            {
                "key": "reading",
                "label": "读取本章并生成结构化 Delta",
                "done": bool(handoff and handoff["status"] in {"RUNNING", "COMPLETED"}),
            },
            {
                "key": "import",
                "label": "Python 导入校验",
                "done": bool(handoff and handoff["status"] == "COMPLETED"),
            },
        ],
        "updated_at": str(row["updated_at"]),
    }


__all__ = [
    "SourceChapterStateDelta",
    "SourceEvidenceLocator",
    "SourceStateCategory",
    "SourceStateOperation",
    "SourceStateVerification",
    "build_source_state_projection",
    "derive_state_key",
    "list_source_chapter_deltas",
    "record_source_chapter_deltas",
]
