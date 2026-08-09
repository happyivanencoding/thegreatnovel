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

    values = list(deltas)
    database.initialize()
    with database.connect() as connection:
        book = connection.execute("SELECT 1 FROM books WHERE book_id=?", (book_id,)).fetchone()
        if book is None:
            raise ValueError("book 不存在")
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
                    category, operation, subject_id, object_id, statement,
                    source_span_ids_json, evidence_locator_json, confidence,
                    verification_status, payload_json, created_at, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    return {
        "record_id": f"source:{delta.delta_id}",
        "name": str(delta.payload.get("name") or delta.object_id or delta.subject_id),
        "category": delta.category.value.lower(),
        "layer": delta.verification_status.value,
        "status": delta.verification_status.value,
        "status_label": {
            SourceStateVerification.SOURCE_VERIFIED.value: "✓ 原文已确认",
            SourceStateVerification.SOURCE_PARTIAL.value: "原文有线索",
            SourceStateVerification.UNKNOWN.value: "尚未知",
        }[delta.verification_status.value],
        "statement": delta.statement,
        "subject_id": delta.subject_id,
        "object_id": delta.object_id,
        "operation": delta.operation.value,
        "chapter_id": delta.chapter_id,
        "chapter_ordinal": delta.chapter_ordinal,
        "source_span_ids": list(delta.source_span_ids),
        "evidence_locator": [item.model_dump(mode="json") for item in delta.evidence_locator],
        "confidence": delta.confidence,
        "attributes": [
            {"label": str(key), "value": str(value)}
            for key, value in delta.payload.items()
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
    for delta in verified:
        collection = records.setdefault(delta.category.value, {})
        if delta.operation in {
            SourceStateOperation.REMOVE,
            SourceStateOperation.LOSE,
            SourceStateOperation.UNEQUIP,
            SourceStateOperation.HIDE,
        }:
            collection.pop(delta.subject_id, None)
            continue
        collection[delta.subject_id] = _delta_record(delta)
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
        "records": {
            category: list(values.values()) for category, values in records.items()
        },
        "uncertain_records": [_delta_record(delta) for delta in uncertain],
        "hydration": {
            "required": not selected_chapter_has_delta,
            "queued": queued is not None,
            "task": queued,
        },
        "layer": "SOURCE_VERIFIED",
    }


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
    return {
        "task_id": str(row["task_id"]),
        "title": str(row["title"]),
        "task_type": str(row["task_type"]),
        "description": str(row["description"] or ""),
        "horizon": str(row["horizon"]),
        "lifecycle_status": str(row["lifecycle_status"]),
        "context_chapter_id": str(row["context_chapter_id"]),
        "context_chapter_ordinal": row["context_chapter_ordinal"],
        "payload": _payload(row["payload_json"]),
        "updated_at": str(row["updated_at"]),
    }


__all__ = [
    "SourceChapterStateDelta",
    "SourceEvidenceLocator",
    "SourceStateCategory",
    "SourceStateOperation",
    "SourceStateVerification",
    "build_source_state_projection",
    "list_source_chapter_deltas",
    "record_source_chapter_deltas",
]
