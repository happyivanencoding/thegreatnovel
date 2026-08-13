"""Versioned author-review lifecycle for progression kernel contracts."""

from __future__ import annotations

import json
import sqlite3
import uuid
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict

from novel_authoring.db.database import Database
from novel_authoring.progression.models import (
    ContractStatus,
    GenreContract,
    PayoffChannelProfile,
    ProgressionContract,
    ReaderExperienceContract,
    WorldExpansionContract,
)
from novel_authoring.serial_kernel.models import (
    MarketCategoryMetadata,
    NarrativeDriveContract,
)
from novel_authoring.utils import json_dumps, utc_now


class ProgressionContractType(StrEnum):
    READER_EXPERIENCE = "READER_EXPERIENCE"
    MARKET_CATEGORY = "MARKET_CATEGORY"
    NARRATIVE_DRIVE = "NARRATIVE_DRIVE"
    GENRE = "GENRE"
    PROGRESSION = "PROGRESSION"
    WORLD_EXPANSION = "WORLD_EXPANSION"
    PAYOFF_CHANNEL = "PAYOFF_CHANNEL"


ContractModel = (
    ReaderExperienceContract
    | GenreContract
    | ProgressionContract
    | WorldExpansionContract
    | PayoffChannelProfile
    | MarketCategoryMetadata
    | NarrativeDriveContract
)

_CONTRACT_MODELS: dict[ProgressionContractType, type[BaseModel]] = {
    ProgressionContractType.READER_EXPERIENCE: ReaderExperienceContract,
    ProgressionContractType.MARKET_CATEGORY: MarketCategoryMetadata,
    ProgressionContractType.NARRATIVE_DRIVE: NarrativeDriveContract,
    ProgressionContractType.GENRE: GenreContract,
    ProgressionContractType.PROGRESSION: ProgressionContract,
    ProgressionContractType.WORLD_EXPANSION: WorldExpansionContract,
    ProgressionContractType.PAYOFF_CHANNEL: PayoffChannelProfile,
}


class ContractRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_record_id: str
    book_id: str
    edition_id: str
    contract_type: ProgressionContractType
    version_number: int
    status: ContractStatus
    payload: dict[str, Any]
    effective_from_boundary: int | None = None
    source: str
    author_notes: str = ""
    created_at: str
    updated_at: str


def _record(row: Any) -> ContractRecord:
    return ContractRecord(
        contract_record_id=str(row["contract_record_id"]),
        book_id=str(row["book_id"]),
        edition_id=str(row["edition_id"]),
        contract_type=ProgressionContractType(str(row["contract_type"])),
        version_number=int(row["version_number"]),
        status=ContractStatus(str(row["status"])),
        payload=json.loads(str(row["payload_json"])),
        effective_from_boundary=(
            int(row["effective_from_boundary"])
            if row["effective_from_boundary"] is not None
            else None
        ),
        source=str(row["source"]),
        author_notes=str(row["author_notes"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _create_contract_proposal_in_connection(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    contract_type: ProgressionContractType,
    payload: ContractModel | dict[str, Any],
    source: str,
    status: ContractStatus = ContractStatus.NEEDS_REVIEW,
    author_notes: str = "",
) -> ContractRecord:
    if status is ContractStatus.EFFECTIVE:
        raise ValueError("Contract Proposal 不能绕过作者确认直接生效")
    model_type = _CONTRACT_MODELS[contract_type]
    validated = payload if isinstance(payload, model_type) else model_type.model_validate(payload)
    values = validated.model_dump(mode="json")
    if "status" in values:
        values["status"] = status.value
    now = utc_now()
    record_id = f"progression-contract-{uuid.uuid4().hex}"
    version_number = int(
        connection.execute(
            """
            SELECT COALESCE(MAX(version_number), 0) + 1
            FROM progression_contract_versions
            WHERE book_id=? AND edition_id=? AND contract_type=?
            """,
            (book_id, edition_id, contract_type.value),
        ).fetchone()[0]
    )
    connection.execute(
        """
        INSERT INTO progression_contract_versions(
            contract_record_id, book_id, edition_id, contract_type,
            version_number, status, payload_json, effective_from_boundary,
            source, author_notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?)
        """,
        (
            record_id,
            book_id,
            edition_id,
            contract_type.value,
            version_number,
            status.value,
            json_dumps(values),
            source,
            author_notes,
            now,
            now,
        ),
    )
    row = connection.execute(
        "SELECT * FROM progression_contract_versions WHERE contract_record_id=?",
        (record_id,),
    ).fetchone()
    if row is None:
        raise RuntimeError("Contract Proposal 持久化失败")
    return _record(row)


def create_contract_proposal(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    contract_type: ProgressionContractType,
    payload: ContractModel | dict[str, Any],
    source: str,
    status: ContractStatus = ContractStatus.NEEDS_REVIEW,
    author_notes: str = "",
) -> ContractRecord:
    database.initialize()
    with database.connect() as connection:
        return _create_contract_proposal_in_connection(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            contract_type=contract_type,
            payload=payload,
            source=source,
            status=status,
            author_notes=author_notes,
        )


def get_contract_record(database: Database, contract_record_id: str) -> ContractRecord | None:
    database.initialize()
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM progression_contract_versions WHERE contract_record_id=?",
            (contract_record_id,),
        ).fetchone()
    return None if row is None else _record(row)


def list_contract_records(
    database: Database,
    *,
    book_id: str,
    edition_id: str = "base",
) -> list[ContractRecord]:
    database.initialize()
    with database.connect() as connection:
        rows = connection.execute(
            """
            SELECT * FROM progression_contract_versions
            WHERE book_id=? AND edition_id=?
            ORDER BY contract_type, version_number DESC
            """,
            (book_id, edition_id),
        ).fetchall()
    return [_record(row) for row in rows]


def _confirm_contract_in_connection(
    connection: sqlite3.Connection,
    contract_record_id: str,
    *,
    effective_from_boundary: int,
    author_notes: str = "",
) -> ContractRecord:
    row = connection.execute(
        "SELECT * FROM progression_contract_versions WHERE contract_record_id=?",
        (contract_record_id,),
    ).fetchone()
    if row is None:
        raise ValueError("Contract Proposal 不存在")
    record = _record(row)
    if record.status in {ContractStatus.REJECTED, ContractStatus.SUPERSEDED}:
        raise ValueError("已拒绝或被替代的 Contract Proposal 不能确认")
    model_type = _CONTRACT_MODELS[record.contract_type]
    payload = dict(record.payload)
    if "status" in model_type.model_fields:
        payload["status"] = ContractStatus.EFFECTIVE.value
    if "effective_from_boundary" in model_type.model_fields:
        payload["effective_from_boundary"] = effective_from_boundary
    validated = model_type.model_validate(payload)
    now = utc_now()
    previous = connection.execute(
        """
        SELECT contract_record_id, payload_json
        FROM progression_contract_versions
        WHERE book_id=? AND edition_id=? AND contract_type=?
          AND status='EFFECTIVE' AND contract_record_id<>?
        """,
        (
            record.book_id,
            record.edition_id,
            record.contract_type.value,
            contract_record_id,
        ),
    ).fetchall()
    for previous_row in previous:
        old_payload = json.loads(str(previous_row["payload_json"]))
        if "status" in old_payload:
            old_payload["status"] = ContractStatus.SUPERSEDED.value
        connection.execute(
            """
            UPDATE progression_contract_versions
            SET status='SUPERSEDED', payload_json=?, updated_at=?, version=version+1
            WHERE contract_record_id=?
            """,
            (
                json_dumps(old_payload),
                now,
                str(previous_row["contract_record_id"]),
            ),
        )
    connection.execute(
        """
        UPDATE progression_contract_versions
        SET status='EFFECTIVE', payload_json=?, effective_from_boundary=?,
            author_notes=?, updated_at=?, version=version+1
        WHERE contract_record_id=?
        """,
        (
            json_dumps(validated.model_dump(mode="json")),
            effective_from_boundary,
            author_notes,
            now,
            contract_record_id,
        ),
    )
    confirmed_row = connection.execute(
        "SELECT * FROM progression_contract_versions WHERE contract_record_id=?",
        (contract_record_id,),
    ).fetchone()
    if confirmed_row is None:
        raise RuntimeError("Contract 确认失败")
    return _record(confirmed_row)


def confirm_contract(
    database: Database,
    contract_record_id: str,
    *,
    effective_from_boundary: int,
    author_notes: str = "",
) -> ContractRecord:
    database.initialize()
    with database.connect() as connection:
        confirmed = _confirm_contract_in_connection(
            connection,
            contract_record_id,
            effective_from_boundary=effective_from_boundary,
            author_notes=author_notes,
        )
    # The contract remains planning-only, but any frozen plan that predates
    # this author decision must not keep accepting candidate output.
    from novel_authoring.planning.aggregates import invalidate_planning_aggregates

    invalidate_planning_aggregates(database, confirmed.book_id, confirmed.edition_id)
    return confirmed


def _reject_contract_in_connection(
    connection: sqlite3.Connection, contract_record_id: str
) -> ContractRecord:
    row = connection.execute(
        "SELECT * FROM progression_contract_versions WHERE contract_record_id=?",
        (contract_record_id,),
    ).fetchone()
    if row is None:
        raise ValueError("Contract Proposal 不存在")
    record = _record(row)
    if record.status is ContractStatus.EFFECTIVE:
        raise ValueError("Effective Contract 需要新版本替代，不能直接拒绝")
    payload = dict(record.payload)
    if "status" in payload:
        payload["status"] = ContractStatus.REJECTED.value
    connection.execute(
        """
        UPDATE progression_contract_versions
        SET status='REJECTED', payload_json=?, updated_at=?, version=version+1
        WHERE contract_record_id=?
        """,
        (json_dumps(payload), utc_now(), contract_record_id),
    )
    rejected_row = connection.execute(
        "SELECT * FROM progression_contract_versions WHERE contract_record_id=?",
        (contract_record_id,),
    ).fetchone()
    if rejected_row is None:
        raise RuntimeError("Contract 拒绝失败")
    return _record(rejected_row)


def reject_contract(database: Database, contract_record_id: str) -> ContractRecord:
    database.initialize()
    with database.connect() as connection:
        return _reject_contract_in_connection(connection, contract_record_id)


def effective_contract_records(
    database: Database,
    *,
    book_id: str,
    edition_id: str = "base",
) -> dict[ProgressionContractType, ContractRecord]:
    return {
        record.contract_type: record
        for record in list_contract_records(
            database,
            book_id=book_id,
            edition_id=edition_id,
        )
        if record.status is ContractStatus.EFFECTIVE
    }


__all__ = [
    "ContractRecord",
    "ProgressionContractType",
    "confirm_contract",
    "create_contract_proposal",
    "effective_contract_records",
    "get_contract_record",
    "list_contract_records",
    "reject_contract",
]
