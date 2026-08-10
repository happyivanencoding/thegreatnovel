"""Reader/character knowledge and author-controlled reveal planning."""

from __future__ import annotations

import json
import sqlite3
import uuid
from enum import StrEnum
from typing import Any, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.author_control.truth import (
    CompatibilityStatus,
    TruthStatus,
    get_author_truth,
    list_author_truths,
)
from novel_authoring.db.database import Database
from novel_authoring.edition import edition_chapters
from novel_authoring.utils import stable_id, utc_now


class KnowledgeState(StrEnum):
    UNKNOWN = "UNKNOWN"
    HINTED = "HINTED"
    SUSPECTED = "SUSPECTED"
    PARTIALLY_REVEALED = "PARTIALLY_REVEALED"
    KNOWN = "KNOWN"
    MISLEADING_BELIEF = "MISLEADING_BELIEF"
    CONFIRMED = "CONFIRMED"


class RevealTarget(StrEnum):
    READER = "READER"
    CHARACTER = "CHARACTER"
    FACTION = "FACTION"
    PUBLIC_WORLD = "PUBLIC_WORLD"


class RevealDepth(StrEnum):
    HINT = "HINT"
    STRONG_HINT = "STRONG_HINT"
    PARTIAL_REVEAL = "PARTIAL_REVEAL"
    FALSE_LEAD = "FALSE_LEAD"
    CONFIRMATION = "CONFIRMATION"
    FULL_REVEAL = "FULL_REVEAL"


class RevealHorizon(StrEnum):
    SHORT = "SHORT"
    MID = "MID"
    LONG = "LONG"


class RevealPlanStatus(StrEnum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class AgendaBucket(StrEnum):
    MUST_REVEAL = "MUST_REVEAL"
    SHOULD_HINT = "SHOULD_HINT"
    KEEP_HIDDEN = "KEEP_HIDDEN"
    OPTIONAL = "OPTIONAL"


class TruthLens(StrEnum):
    AUTHOR = "AUTHOR"
    READER = "READER"
    CHARACTER = "CHARACTER"


class SecretLifecycle(StrEnum):
    PLANNED = "PLANNED"
    ACTIVE_HIDDEN = "ACTIVE_HIDDEN"
    HINTING = "HINTING"
    PARTIAL_REVEAL = "PARTIAL_REVEAL"
    PAYOFF_READY = "PAYOFF_READY"
    REVEALED = "REVEALED"
    AFTERMATH = "AFTERMATH"
    RETIRED = "RETIRED"


class RevealPlanInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_id: str = Field(min_length=1)
    target: RevealTarget = RevealTarget.READER
    target_entity_id: str | None = None
    strategy: str = ""
    target_chapter_min: int = Field(ge=1)
    target_chapter_max: int | None = Field(default=None, ge=1)
    horizon: RevealHorizon = RevealHorizon.MID
    priority: int = Field(default=100, ge=0)
    status: RevealPlanStatus = RevealPlanStatus.PLANNED
    required_preconditions: list[str] = Field(default_factory=list)
    forbidden_conditions: list[str] = Field(default_factory=list)
    reveal_depth: RevealDepth

    @model_validator(mode="after")
    def validate_target_and_window(self) -> RevealPlanInput:
        if (
            self.target_chapter_max is not None
            and self.target_chapter_max < self.target_chapter_min
        ):
            raise ValueError("target_chapter_max 不得早于 target_chapter_min")
        if self.target in {RevealTarget.CHARACTER, RevealTarget.FACTION} and not (
            self.target_entity_id or ""
        ).strip():
            raise ValueError("CHARACTER / FACTION RevealPlan 必须指定 target_entity_id")
        return self


class RevealEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_id: str
    reveal_plan_id: str | None = None
    target: RevealTarget
    target_entity_id: str | None = None
    depth: RevealDepth
    evidence_quote: str = Field(min_length=1)
    expected_knowledge_change: KnowledgeState

    @model_validator(mode="after")
    def target_entity_required(self) -> RevealEvent:
        if self.target in {RevealTarget.CHARACTER, RevealTarget.FACTION} and not (
            self.target_entity_id or ""
        ).strip():
            raise ValueError("角色或势力揭示事件必须指定 target_entity_id")
        return self


class PlannedReveal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_id: str
    agenda_bucket: AgendaBucket
    depth: RevealDepth | None = None


class KnowledgeTransition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_id: str
    target: RevealTarget
    target_entity_id: str | None = None
    before: KnowledgeState
    after: KnowledgeState


class RevealTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    planned: list[PlannedReveal] = Field(default_factory=list)
    realized: list[RevealEvent] = Field(default_factory=list)
    knowledge_transitions: list[KnowledgeTransition] = Field(default_factory=list)


_KNOWLEDGE_RANK = {
    KnowledgeState.UNKNOWN: 0,
    KnowledgeState.MISLEADING_BELIEF: 1,
    KnowledgeState.HINTED: 2,
    KnowledgeState.SUSPECTED: 3,
    KnowledgeState.PARTIALLY_REVEALED: 4,
    KnowledgeState.KNOWN: 5,
    KnowledgeState.CONFIRMED: 6,
}

_DEPTH_STATE = {
    RevealDepth.HINT: KnowledgeState.HINTED,
    RevealDepth.STRONG_HINT: KnowledgeState.SUSPECTED,
    RevealDepth.PARTIAL_REVEAL: KnowledgeState.PARTIALLY_REVEALED,
    RevealDepth.FALSE_LEAD: KnowledgeState.MISLEADING_BELIEF,
    RevealDepth.CONFIRMATION: KnowledgeState.CONFIRMED,
    RevealDepth.FULL_REVEAL: KnowledgeState.CONFIRMED,
}


def _knowledge_regresses(before: KnowledgeState, after: KnowledgeState) -> bool:
    if after is KnowledgeState.MISLEADING_BELIEF:
        return before in {KnowledgeState.KNOWN, KnowledgeState.CONFIRMED}
    if before is KnowledgeState.MISLEADING_BELIEF:
        return after is KnowledgeState.UNKNOWN
    return _KNOWLEDGE_RANK[after] < _KNOWLEDGE_RANK[before]


def _loads(value: Any, fallback: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(str(value))
    except (TypeError, ValueError):
        return fallback


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _plan_from_row(row: sqlite3.Row | dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    item["required_preconditions"] = list(
        _loads(item.pop("required_preconditions_json", "[]"), [])
    )
    item["forbidden_conditions"] = list(
        _loads(item.pop("forbidden_conditions_json", "[]"), [])
    )
    return item


def _knowledge_from_row(row: sqlite3.Row | dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    item["provisional"] = bool(item["provisional"])
    item["evidence"] = list(_loads(item.pop("evidence_json", "[]"), []))
    return item


def _chapter_boundary(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int | None,
) -> tuple[int, str | None]:
    chapters = edition_chapters(connection, book_id, edition_id)
    current = max((int(item["ordinal"]) for item in chapters), default=0)
    selected = current if chapter_ordinal is None else chapter_ordinal
    if selected < 0:
        raise ValueError("Knowledge chapter_ordinal 不得小于 0")
    chapter_id = next(
        (
            str(item["chapter_id"])
            for item in chapters
            if int(item["ordinal"]) == selected
        ),
        None,
    )
    if 0 < selected <= current and chapter_id is None:
        raise ValueError(f"Edition 中不存在第 {selected} 章")
    return selected, chapter_id


def _latest_reader_row(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    truth_id: str,
    chapter_ordinal: int,
    include_provisional: bool = False,
) -> sqlite3.Row | None:
    provisional_clause = "" if include_provisional else " AND provisional=0"
    return cast(
        sqlite3.Row | None,
        connection.execute(
        "SELECT * FROM reader_knowledge_edges WHERE book_id=? AND edition_id=? "
        "AND truth_id=? AND as_of_chapter_ordinal<=?"
        f"{provisional_clause} ORDER BY as_of_chapter_ordinal DESC, created_at DESC, "
        "edge_id DESC LIMIT 1",
        (book_id, edition_id, truth_id, chapter_ordinal),
        ).fetchone(),
    )


def _latest_character_row(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    truth_id: str,
    character_id: str,
    chapter_ordinal: int,
    include_provisional: bool = False,
) -> sqlite3.Row | None:
    provisional_clause = "" if include_provisional else " AND provisional=0"
    return cast(
        sqlite3.Row | None,
        connection.execute(
        "SELECT * FROM truth_character_knowledge WHERE book_id=? AND edition_id=? "
        "AND truth_id=? AND character_id=? AND as_of_chapter_ordinal<=?"
        f"{provisional_clause} ORDER BY as_of_chapter_ordinal DESC, created_at DESC, "
        "edge_id DESC LIMIT 1",
        (book_id, edition_id, truth_id, character_id, chapter_ordinal),
        ).fetchone(),
    )


def _latest_reader_rows(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int,
    include_provisional: bool = False,
) -> dict[str, dict[str, Any]]:
    provisional_clause = "" if include_provisional else " AND provisional=0"
    rows = connection.execute(
        "SELECT * FROM reader_knowledge_edges WHERE book_id=? AND edition_id=? "
        "AND as_of_chapter_ordinal<=?"
        f"{provisional_clause} ORDER BY as_of_chapter_ordinal DESC, created_at DESC, "
        "edge_id DESC",
        (book_id, edition_id, chapter_ordinal),
    ).fetchall()
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        latest.setdefault(str(row["truth_id"]), _knowledge_from_row(row))
    return latest


def _latest_character_rows(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int,
    include_provisional: bool = False,
) -> dict[tuple[str, str], dict[str, Any]]:
    provisional_clause = "" if include_provisional else " AND provisional=0"
    rows = connection.execute(
        "SELECT * FROM truth_character_knowledge WHERE book_id=? AND edition_id=? "
        "AND as_of_chapter_ordinal<=?"
        f"{provisional_clause} ORDER BY as_of_chapter_ordinal DESC, created_at DESC, "
        "edge_id DESC",
        (book_id, edition_id, chapter_ordinal),
    ).fetchall()
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row["truth_id"]), str(row["character_id"]))
        latest.setdefault(key, _knowledge_from_row(row))
    return latest


def _append_reader_in_transaction(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    truth_id: str,
    state: KnowledgeState,
    chapter_ordinal: int | None,
    evidence: list[dict[str, Any]],
    provenance: str,
    provisional: bool,
    as_of_chapter_id: str | None = None,
    reveal_event_id: str | None = None,
    allow_regression: bool = False,
) -> dict[str, Any]:
    selected_ordinal, resolved_chapter_id = _chapter_boundary(
        connection, book_id, edition_id, chapter_ordinal
    )
    chapter_id = as_of_chapter_id or resolved_chapter_id
    row = _latest_reader_row(
        connection,
        book_id=book_id,
        edition_id=edition_id,
        truth_id=truth_id,
        chapter_ordinal=selected_ordinal,
        include_provisional=provisional,
    )
    before = KnowledgeState.UNKNOWN if row is None else KnowledgeState(str(row["state"]))
    if not allow_regression and _knowledge_regresses(before, state):
        raise ValueError("Reader Knowledge 不能在非 Revision 流程中倒退")
    edge_id = f"reader-knowledge-{uuid.uuid4().hex}"
    first = (
        selected_ordinal
        if state is not KnowledgeState.UNKNOWN
        and (row is None or row["first_exposed_chapter"] is None)
        else int(row["first_exposed_chapter"])
        if row is not None and row["first_exposed_chapter"] is not None
        else None
    )
    now = utc_now()
    authority_status = "PROVISIONAL" if provisional else provenance
    connection.execute(
        "INSERT INTO reader_knowledge_edges("
        "edge_id, book_id, edition_id, truth_id, state, as_of_chapter_id, "
        "as_of_chapter_ordinal, first_exposed_chapter, last_advanced_chapter, "
        "evidence_json, provenance, authority_status, provisional, reveal_event_id, "
        "supersedes_edge_id, created_at, updated_at, version"
        ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
        (
            edge_id,
            book_id,
            edition_id,
            truth_id,
            state.value,
            chapter_id,
            selected_ordinal,
            first,
            selected_ordinal,
            _dumps(evidence),
            provenance,
            authority_status,
            int(provisional),
            reveal_event_id,
            None if row is None else str(row["edge_id"]),
            now,
            now,
        ),
    )
    return {
        "before": before.value,
        "after": state.value,
        "edge_id": edge_id,
        "as_of_chapter_id": chapter_id,
        "as_of_chapter_ordinal": selected_ordinal,
        "supersedes_edge_id": None if row is None else str(row["edge_id"]),
    }


def _append_character_in_transaction(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    truth_id: str,
    character_id: str,
    state: KnowledgeState,
    chapter_ordinal: int | None,
    evidence: list[dict[str, Any]],
    provenance: str,
    provisional: bool,
    as_of_chapter_id: str | None = None,
    reveal_event_id: str | None = None,
    allow_regression: bool = False,
) -> dict[str, Any]:
    selected_ordinal, resolved_chapter_id = _chapter_boundary(
        connection, book_id, edition_id, chapter_ordinal
    )
    chapter_id = as_of_chapter_id or resolved_chapter_id
    row = _latest_character_row(
        connection,
        book_id=book_id,
        edition_id=edition_id,
        truth_id=truth_id,
        character_id=character_id,
        chapter_ordinal=selected_ordinal,
        include_provisional=provisional,
    )
    before = KnowledgeState.UNKNOWN if row is None else KnowledgeState(str(row["state"]))
    if not allow_regression and _knowledge_regresses(before, state):
        raise ValueError("Character Knowledge 不能在非 Revision 流程中倒退")
    edge_id = f"character-knowledge-{uuid.uuid4().hex}"
    first = (
        selected_ordinal
        if state is not KnowledgeState.UNKNOWN
        and (row is None or row["first_exposed_chapter"] is None)
        else int(row["first_exposed_chapter"])
        if row is not None and row["first_exposed_chapter"] is not None
        else None
    )
    now = utc_now()
    authority_status = "PROVISIONAL" if provisional else provenance
    connection.execute(
        "INSERT INTO truth_character_knowledge("
        "edge_id, book_id, edition_id, truth_id, character_id, state, "
        "as_of_chapter_id, as_of_chapter_ordinal, first_exposed_chapter, "
        "last_advanced_chapter, evidence_json, provenance, authority_status, "
        "provisional, reveal_event_id, supersedes_edge_id, created_at, updated_at, version"
        ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
        (
            edge_id,
            book_id,
            edition_id,
            truth_id,
            character_id,
            state.value,
            chapter_id,
            selected_ordinal,
            first,
            selected_ordinal,
            _dumps(evidence),
            provenance,
            authority_status,
            int(provisional),
            reveal_event_id,
            None if row is None else str(row["edge_id"]),
            now,
            now,
        ),
    )
    return {
        "before": before.value,
        "after": state.value,
        "edge_id": edge_id,
        "as_of_chapter_id": chapter_id,
        "as_of_chapter_ordinal": selected_ordinal,
        "supersedes_edge_id": None if row is None else str(row["edge_id"]),
    }


def set_reader_knowledge(
    database: Database,
    book_id: str,
    edition_id: str,
    truth_id: str,
    *,
    state: KnowledgeState | str,
    chapter_ordinal: int | None = None,
    evidence: list[dict[str, Any]] | None = None,
    mode: str = "AUTHOR_PLANNING",
) -> dict[str, Any]:
    """Set reader knowledge without pretending an unsupported historic reveal happened."""

    database.initialize()
    selected = KnowledgeState(str(state).upper())
    selected_mode = mode.strip().upper()
    if selected_mode not in {"AUTHOR_PLANNING", "SOURCE_EVIDENCE", "REVISION"}:
        raise ValueError(
            "Reader Knowledge 修正必须选择 AUTHOR_PLANNING、SOURCE_EVIDENCE 或 REVISION"
        )
    if selected_mode == "SOURCE_EVIDENCE" and not evidence:
        raise ValueError("SOURCE_EVIDENCE 模式必须提供证据")
    get_author_truth(database, book_id, edition_id, truth_id)
    with database.connect() as connection:
        result = _append_reader_in_transaction(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            truth_id=truth_id,
            state=selected,
            chapter_ordinal=chapter_ordinal,
            evidence=evidence or [],
            provenance=selected_mode,
            provisional=selected_mode == "AUTHOR_PLANNING",
            allow_regression=selected_mode == "REVISION",
        )
    return result | {"provisional": selected_mode == "AUTHOR_PLANNING"}


def set_character_truth_knowledge(
    database: Database,
    book_id: str,
    edition_id: str,
    truth_id: str,
    character_id: str,
    *,
    state: KnowledgeState | str,
    chapter_ordinal: int | None = None,
    evidence: list[dict[str, Any]] | None = None,
    mode: str = "AUTHOR_PLANNING",
) -> dict[str, Any]:
    database.initialize()
    selected = KnowledgeState(str(state).upper())
    selected_mode = mode.strip().upper()
    if selected_mode not in {"AUTHOR_PLANNING", "SOURCE_EVIDENCE", "REVISION"}:
        raise ValueError("Character Knowledge 修正模式无效")
    if selected_mode == "SOURCE_EVIDENCE" and not evidence:
        raise ValueError("SOURCE_EVIDENCE 模式必须提供证据")
    get_author_truth(database, book_id, edition_id, truth_id)
    with database.connect() as connection:
        result = _append_character_in_transaction(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            truth_id=truth_id,
            character_id=character_id,
            state=selected,
            chapter_ordinal=chapter_ordinal,
            evidence=evidence or [],
            provenance=selected_mode,
            provisional=selected_mode == "AUTHOR_PLANNING",
            allow_regression=selected_mode == "REVISION",
        )
    return result | {"provisional": selected_mode == "AUTHOR_PLANNING"}


def create_reveal_plan(
    database: Database,
    book_id: str,
    edition_id: str,
    payload: RevealPlanInput | dict[str, Any],
) -> dict[str, Any]:
    database.initialize()
    data = (
        payload
        if isinstance(payload, RevealPlanInput)
        else RevealPlanInput.model_validate(payload)
    )
    truth = get_author_truth(database, book_id, edition_id, data.truth_id)
    if truth["status"] not in {
        TruthStatus.ACTIVE_TRUTH.value,
        TruthStatus.PROVISIONAL_TRUTH.value,
        TruthStatus.REVEALED.value,
    }:
        raise ValueError("当前 Truth 状态不能建立 RevealPlan")
    reveal_plan_id = f"reveal-plan-{uuid.uuid4().hex}"
    now = utc_now()
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO reveal_plans("
            "reveal_plan_id, book_id, edition_id, truth_id, target, target_entity_id, "
            "strategy, target_chapter_min, target_chapter_max, horizon, priority, "
            "status, required_preconditions_json, forbidden_conditions_json, "
            "reveal_depth, created_at, updated_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
            (
                reveal_plan_id,
                book_id,
                edition_id,
                data.truth_id,
                data.target.value,
                data.target_entity_id,
                data.strategy.strip(),
                data.target_chapter_min,
                data.target_chapter_max,
                data.horizon.value,
                data.priority,
                data.status.value,
                _dumps(data.required_preconditions),
                _dumps(data.forbidden_conditions),
                data.reveal_depth.value,
                now,
                now,
            ),
        )
        connection.execute(
            "UPDATE planning_aggregates SET status='STALE', stale_reason=?, "
            "invalidated_at=?, version=version+1 WHERE book_id=? AND edition_id=? "
            "AND status='ACTIVE'",
            (
                f"Reveal Plan {reveal_plan_id} 已更新",
                now,
                book_id,
                edition_id,
            ),
        )
    return {
        "reveal_plan_id": reveal_plan_id,
        **data.model_dump(mode="json"),
    }


def list_reveal_plans(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    truth_id: str | None = None,
) -> list[dict[str, Any]]:
    database.initialize()
    sql = "SELECT * FROM reveal_plans WHERE book_id=? AND edition_id=?"
    params: list[Any] = [book_id, edition_id]
    if truth_id:
        sql += " AND truth_id=?"
        params.append(truth_id)
    sql += " ORDER BY target_chapter_min, priority, created_at, reveal_plan_id"
    with database.connect() as connection:
        rows = connection.execute(sql, tuple(params)).fetchall()
    return [_plan_from_row(row) for row in rows]


def override_reveal_agenda(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    truth_id: str,
    chapter_ordinal: int,
    agenda_bucket: AgendaBucket | str,
    reveal_depth: RevealDepth | str | None = None,
    reason: str = "作者手动调整本章揭示安排",
) -> dict[str, Any]:
    database.initialize()
    get_author_truth(database, book_id, edition_id, truth_id)
    bucket = AgendaBucket(str(agenda_bucket).upper())
    depth = None if reveal_depth is None else RevealDepth(str(reveal_depth).upper())
    if bucket is AgendaBucket.SHOULD_HINT and depth not in {
        None,
        RevealDepth.HINT,
        RevealDepth.STRONG_HINT,
        RevealDepth.FALSE_LEAD,
    }:
        raise ValueError("给出线索只能使用 HINT / STRONG_HINT / FALSE_LEAD")
    if bucket is AgendaBucket.KEEP_HIDDEN:
        depth = None
    override_id = stable_id(
        "reveal-agenda", book_id, edition_id, truth_id, str(chapter_ordinal)
    )
    now = utc_now()
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO reveal_agenda_overrides("
            "override_id, book_id, edition_id, truth_id, chapter_ordinal, agenda_bucket, "
            "reveal_depth, reason, created_at, updated_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1) "
            "ON CONFLICT(book_id, edition_id, truth_id, chapter_ordinal) DO UPDATE SET "
            "agenda_bucket=excluded.agenda_bucket, reveal_depth=excluded.reveal_depth, "
            "reason=excluded.reason, updated_at=excluded.updated_at, "
            "version=reveal_agenda_overrides.version+1",
            (
                override_id,
                book_id,
                edition_id,
                truth_id,
                chapter_ordinal,
                bucket.value,
                None if depth is None else depth.value,
                reason.strip(),
                now,
                now,
            ),
        )
        connection.execute(
            "UPDATE planning_aggregates SET status='STALE', stale_reason=?, "
            "invalidated_at=?, version=version+1 WHERE book_id=? AND edition_id=? "
            "AND status='ACTIVE'",
            (f"第{chapter_ordinal}章 Reveal Agenda 已调整", now, book_id, edition_id),
        )
    return {
        "override_id": override_id,
        "truth_id": truth_id,
        "chapter_ordinal": chapter_ordinal,
        "agenda_bucket": bucket.value,
        "reveal_depth": None if depth is None else depth.value,
        "knowledge_changed": False,
    }


def _default_bucket(plan: dict[str, Any], chapter_ordinal: int) -> AgendaBucket:
    minimum = int(plan["target_chapter_min"])
    maximum = (
        minimum
        if plan["target_chapter_max"] is None
        else int(plan["target_chapter_max"])
    )
    depth = RevealDepth(str(plan["reveal_depth"]))
    if chapter_ordinal < minimum:
        return AgendaBucket.KEEP_HIDDEN
    if chapter_ordinal > maximum:
        if depth in {
            RevealDepth.PARTIAL_REVEAL,
            RevealDepth.CONFIRMATION,
            RevealDepth.FULL_REVEAL,
        }:
            return AgendaBucket.MUST_REVEAL
        return AgendaBucket.KEEP_HIDDEN
    if depth in {RevealDepth.HINT, RevealDepth.STRONG_HINT, RevealDepth.FALSE_LEAD}:
        return AgendaBucket.SHOULD_HINT
    return AgendaBucket.MUST_REVEAL


def build_reveal_agenda(
    database: Database,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int,
) -> dict[str, Any]:
    database.initialize()
    truths = list_author_truths(
        database,
        book_id,
        edition_id,
        chapter_ordinal=chapter_ordinal,
        include_future=False,
    )
    plans = list_reveal_plans(database, book_id, edition_id)
    plan_by_truth: dict[str, list[dict[str, Any]]] = {}
    for plan in plans:
        if plan["status"] not in {
            RevealPlanStatus.PLANNED.value,
            RevealPlanStatus.ACTIVE.value,
        }:
            continue
        plan_by_truth.setdefault(str(plan["truth_id"]), []).append(plan)
    with database.connect() as connection:
        overrides = {
            str(row["truth_id"]): dict(row)
            for row in connection.execute(
                "SELECT * FROM reveal_agenda_overrides WHERE book_id=? AND edition_id=? "
                "AND chapter_ordinal=?",
                (book_id, edition_id, chapter_ordinal),
            ).fetchall()
        }
        reader_rows = _latest_reader_rows(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            chapter_ordinal=chapter_ordinal,
        )
        character_rows = _latest_character_rows(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            chapter_ordinal=chapter_ordinal,
        )
    buckets: dict[str, list[dict[str, Any]]] = {
        AgendaBucket.MUST_REVEAL.value: [],
        AgendaBucket.SHOULD_HINT.value: [],
        AgendaBucket.KEEP_HIDDEN.value: [],
        AgendaBucket.OPTIONAL.value: [],
    }
    for truth in truths:
        if truth["status"] != TruthStatus.ACTIVE_TRUTH.value or truth[
            "compatibility_status"
        ] not in {
            CompatibilityStatus.COMPATIBLE.value,
            CompatibilityStatus.COMPATIBLE_WITH_GAPS.value,
        }:
            continue
        truth_id = str(truth["truth_id"])
        truth_plans = plan_by_truth.get(truth_id, [])
        eligible_plans = [
            plan
            for plan in truth_plans
            if int(plan["target_chapter_min"]) <= chapter_ordinal
        ]
        selected_plan = (
            max(
                eligible_plans,
                key=lambda plan: (
                    int(plan["target_chapter_min"]),
                    -int(plan["priority"]),
                    str(plan["reveal_plan_id"]),
                ),
            )
            if eligible_plans
            else truth_plans[0]
            if truth_plans
            else None
        )
        if selected_plan is None:
            bucket = AgendaBucket.KEEP_HIDDEN
            depth: str | None = None
            source = "DEFAULT_CONCEALMENT"
        else:
            bucket = _default_bucket(selected_plan, chapter_ordinal)
            depth = str(selected_plan["reveal_depth"])
            source = "REVEAL_PLAN"
        override = overrides.get(truth_id)
        if override is not None:
            bucket = AgendaBucket(str(override["agenda_bucket"]))
            depth = None if override["reveal_depth"] is None else str(override["reveal_depth"])
            source = "AUTHOR_OVERRIDE"
        reader = reader_rows.get(truth_id, {"state": KnowledgeState.UNKNOWN.value})
        target_entity_id = (
            None if selected_plan is None else selected_plan.get("target_entity_id")
        )
        character = (
            None
            if target_entity_id is None
            else character_rows.get((truth_id, str(target_entity_id)))
        )
        item = {
            "truth_id": truth_id,
            "title": truth["title"],
            "statement": truth["statement"],
            "truth_type": truth["truth_type"],
            "agenda_bucket": bucket.value,
            "reveal_depth": depth,
            "reader_state": reader["state"],
            "target_character_state": (
                KnowledgeState.UNKNOWN.value if character is None else character["state"]
            ),
            "behavioral_constraint": truth["status"] == TruthStatus.ACTIVE_TRUTH.value,
            "reveal_permission": bucket is not AgendaBucket.KEEP_HIDDEN,
            "can_reveal": bucket
            in {AgendaBucket.MUST_REVEAL, AgendaBucket.SHOULD_HINT, AgendaBucket.OPTIONAL},
            "must_hint": bucket is AgendaBucket.SHOULD_HINT,
            "must_reveal": bucket is AgendaBucket.MUST_REVEAL,
            "keep_hidden": bucket is AgendaBucket.KEEP_HIDDEN,
            "source": source,
            "plan": selected_plan,
            "priority": 100 if selected_plan is None else int(selected_plan["priority"]),
        }
        buckets[bucket.value].append(item)
    for values in buckets.values():
        values.sort(key=lambda item: (item["priority"], item["title"], item["truth_id"]))
    full_or_partial = sum(
        1
        for item in buckets[AgendaBucket.MUST_REVEAL.value]
        if item["reveal_depth"]
        in {
            RevealDepth.PARTIAL_REVEAL.value,
            RevealDepth.CONFIRMATION.value,
            RevealDepth.FULL_REVEAL.value,
        }
    )
    hints = len(buckets[AgendaBucket.SHOULD_HINT.value])
    return {
        "book_id": book_id,
        "edition_id": edition_id,
        "chapter_ordinal": chapter_ordinal,
        "must_reveal": buckets[AgendaBucket.MUST_REVEAL.value],
        "should_hint": buckets[AgendaBucket.SHOULD_HINT.value],
        "keep_hidden": buckets[AgendaBucket.KEEP_HIDDEN.value],
        "optional": buckets[AgendaBucket.OPTIONAL.value],
        "counts": {
            "must_reveal": len(buckets[AgendaBucket.MUST_REVEAL.value]),
            "should_hint": hints,
            "keep_hidden": len(buckets[AgendaBucket.KEEP_HIDDEN.value]),
            "optional": len(buckets[AgendaBucket.OPTIONAL.value]),
        },
        "reveal_budget": {
            "partial_or_full_guideline": "0–1",
            "hint_guideline": "1–3",
            "planned_partial_or_full": full_or_partial,
            "planned_hints": hints,
            "status": "OVER_BUDGET" if full_or_partial > 1 or hints > 3 else "WITHIN_GUIDELINE",
            "hard_gate": False,
        },
        "debt_integration": {
            "engine": "Narrative Debt / Promise",
            "separate_reveal_debt_engine": False,
            "secret_obligations": [
                {
                    "truth_id": item["truth_id"],
                    "horizon": (item["plan"] or {}).get("horizon"),
                    "target_window": [
                        (item["plan"] or {}).get("target_chapter_min"),
                        (item["plan"] or {}).get("target_chapter_max"),
                    ],
                    "debt_type": "SECRET_REVEAL",
                }
                for item in (
                    buckets[AgendaBucket.MUST_REVEAL.value]
                    + buckets[AgendaBucket.SHOULD_HINT.value]
                )
            ],
        },
        "rule": "Hidden Truth 是行为约束，不等于揭示许可；拖动 Agenda 不改变任何 Knowledge。",
    }


def _secret_lifecycle(
    truth: dict[str, Any],
    reader_state: KnowledgeState,
    plans: list[dict[str, Any]],
    chapter_ordinal: int,
) -> SecretLifecycle:
    if truth["status"] == TruthStatus.RETIRED.value:
        return SecretLifecycle.RETIRED
    if truth["status"] == TruthStatus.IDEA.value:
        return SecretLifecycle.PLANNED
    if reader_state in {KnowledgeState.CONFIRMED, KnowledgeState.KNOWN}:
        return SecretLifecycle.REVEALED
    if reader_state is KnowledgeState.PARTIALLY_REVEALED:
        return SecretLifecycle.PARTIAL_REVEAL
    if reader_state in {
        KnowledgeState.HINTED,
        KnowledgeState.SUSPECTED,
        KnowledgeState.MISLEADING_BELIEF,
    }:
        return SecretLifecycle.HINTING
    if any(
        int(plan["target_chapter_min"]) <= chapter_ordinal
        and RevealDepth(str(plan["reveal_depth"]))
        in {
            RevealDepth.PARTIAL_REVEAL,
            RevealDepth.CONFIRMATION,
            RevealDepth.FULL_REVEAL,
        }
        for plan in plans
    ):
        return SecretLifecycle.PAYOFF_READY
    return SecretLifecycle.ACTIVE_HIDDEN


def build_secret_board(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_ordinal: int,
    horizon: RevealHorizon | str | None = None,
) -> dict[str, Any]:
    selected_horizon = None if horizon is None else RevealHorizon(str(horizon).upper())
    truths = list_author_truths(
        database,
        book_id,
        edition_id,
        chapter_ordinal=chapter_ordinal,
        include_future=False,
    )
    plans = list_reveal_plans(database, book_id, edition_id)
    plan_by_truth: dict[str, list[dict[str, Any]]] = {}
    for plan in plans:
        if selected_horizon is not None and plan["horizon"] != selected_horizon.value:
            continue
        plan_by_truth.setdefault(str(plan["truth_id"]), []).append(plan)
    with database.connect() as connection:
        reader = {
            truth_id: KnowledgeState(str(item["state"]))
            for truth_id, item in _latest_reader_rows(
                connection,
                book_id=book_id,
                edition_id=edition_id,
                chapter_ordinal=chapter_ordinal,
            ).items()
        }
        reveal_history: dict[str, list[dict[str, Any]]] = {}
        for row in connection.execute(
            "SELECT truth_id, depth, chapter_ordinal, target, target_entity_id "
            "FROM reveal_events WHERE book_id=? AND edition_id=? AND status='CANON' "
            "AND chapter_ordinal<=? ORDER BY chapter_ordinal, created_at, reveal_event_id",
            (book_id, edition_id, chapter_ordinal),
        ).fetchall():
            reveal_history.setdefault(str(row["truth_id"]), []).append(dict(row))
    columns: dict[str, list[dict[str, Any]]] = {
        item.value: [] for item in SecretLifecycle
    }
    secret_types = {
        "CHARACTER_SECRET",
        "CHARACTER_IDENTITY",
        "ITEM_SECRET",
        "ABILITY_SECRET",
        "LOCATION_SECRET",
        "FACTION_SECRET",
        "FACTION_GOAL",
        "FACTION_RELATIONSHIP",
        "WORLD_RULE_SECRET",
        "RELATIONSHIP_SECRET",
        "PLOT_TRUTH",
        "CAUSE",
        "MOTIVE",
    }
    for truth in truths:
        if truth["truth_type"] not in secret_types:
            continue
        truth_plans = plan_by_truth.get(str(truth["truth_id"]), [])
        if selected_horizon is not None and not truth_plans:
            continue
        state = reader.get(str(truth["truth_id"]), KnowledgeState.UNKNOWN)
        lifecycle = _secret_lifecycle(truth, state, truth_plans, chapter_ordinal)
        history = reveal_history.get(str(truth["truth_id"]), [])
        hint_events = [
            event
            for event in history
            if event["depth"] in {"HINT", "STRONG_HINT", "FALSE_LEAD"}
            and event["target"] in {"READER", "PUBLIC_WORLD"}
        ]
        payoff_events = [
            event
            for event in history
            if event["depth"]
            in {"PARTIAL_REVEAL", "CONFIRMATION", "FULL_REVEAL"}
            and event["target"] in {"READER", "PUBLIC_WORLD"}
        ]
        future_payoff = any(
            int(plan["target_chapter_min"]) > chapter_ordinal
            and plan["reveal_depth"]
            in {"PARTIAL_REVEAL", "CONFIRMATION", "FULL_REVEAL"}
            and plan["status"]
            in {RevealPlanStatus.PLANNED.value, RevealPlanStatus.ACTIVE.value}
            for plan in truth_plans
        )
        chapters_since_hint = (
            None
            if not hint_events
            else chapter_ordinal - int(hint_events[-1]["chapter_ordinal"])
        )
        overdeferred = len(hint_events) >= 5 and not payoff_events and not future_payoff
        debt_status = (
            "PAID"
            if payoff_events
            else "INTENTIONAL_CONCEALMENT"
            if future_payoff
            else "OVERDEFERRED_SECRET"
            if overdeferred
            else "TRACKED"
        )
        columns[lifecycle.value].append(
            {
                **truth,
                "secret_id": truth["truth_id"],
                "current_reader_state": state.value,
                "reveal_status": lifecycle.value,
                "reveal_plan": truth_plans,
                "horizons": sorted({plan["horizon"] for plan in truth_plans}),
                "foreshadowing_status": (
                    "STARTED" if state is not KnowledgeState.UNKNOWN else "NOT_STARTED"
                ),
                "payoff_value": max(
                    (101 - int(plan["priority"]) for plan in truth_plans), default=0
                ),
                "narrative_debt": {
                    "debt_type": "SECRET_REVEAL",
                    "status": debt_status,
                    "hint_count": len(hint_events),
                    "chapters_since_hint": chapters_since_hint,
                    "payoff_count": len(payoff_events),
                    "overdeferred": overdeferred,
                    "separate_engine": False,
                },
            }
        )
    return {
        "chapter_ordinal": chapter_ordinal,
        "horizon": None if selected_horizon is None else selected_horizon.value,
        "columns": columns,
        "counts": {key: len(value) for key, value in columns.items()},
        "debt_summary": {
            "engine": "Narrative Debt / Promise",
            "overdeferred": sum(
                1
                for values in columns.values()
                for item in values
                if item["narrative_debt"]["overdeferred"]
            ),
            "separate_reveal_debt_engine": False,
        },
    }


def truth_knowledge_view(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_ordinal: int,
    truth_id: str | None = None,
) -> dict[str, Any]:
    truths = list_author_truths(
        database,
        book_id,
        edition_id,
        chapter_ordinal=chapter_ordinal,
        include_future=False,
    )
    if truth_id is not None:
        truths = [item for item in truths if item["truth_id"] == truth_id]
    truth_ids = [str(item["truth_id"]) for item in truths]
    with database.connect() as connection:
        reader = _latest_reader_rows(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            chapter_ordinal=chapter_ordinal,
        )
        character_rows = _latest_character_rows(
            connection,
            book_id=book_id,
            edition_id=edition_id,
            chapter_ordinal=chapter_ordinal,
        )
        compatibility_rows = connection.execute(
            "SELECT * FROM truth_compatibility_evidence WHERE book_id=? "
            "AND edition_id=? AND active=1 "
            "ORDER BY chapter_ordinal, created_at, evidence_id",
            (book_id, edition_id),
        ).fetchall()
    compatibility: dict[str, list[dict[str, Any]]] = {}
    for row in compatibility_rows:
        row_truth_id = str(row["truth_id"])
        if row_truth_id in truth_ids:
            compatibility.setdefault(row_truth_id, []).append(dict(row))
    characters: dict[str, list[dict[str, Any]]] = {}
    for (row_truth_id, _character_id), row in character_rows.items():
        if row_truth_id not in truth_ids:
            continue
        characters.setdefault(row_truth_id, []).append(row)
    for values in characters.values():
        values.sort(key=lambda item: (str(item["character_id"]), str(item["edge_id"])))
    topics = []
    plans = list_reveal_plans(database, book_id, edition_id)
    for truth in truths:
        tid = str(truth["truth_id"])
        topics.append(
            {
                "truth": truth,
                "author_state": "KNOWN",
                "reader": reader.get(
                    tid,
                    {
                        "truth_id": tid,
                        "state": KnowledgeState.UNKNOWN.value,
                        "provisional": False,
                        "evidence": [],
                    },
                ),
                "characters": characters.get(tid, []),
                "reveal_plans": [item for item in plans if item["truth_id"] == tid],
                "compatibility_evidence": compatibility.get(tid, []),
            }
        )
    return {"chapter_ordinal": chapter_ordinal, "topics": topics}


def project_truth_lens(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_ordinal: int,
    lens: TruthLens | str = TruthLens.AUTHOR,
    character_id: str | None = None,
    include_future: bool = False,
) -> dict[str, Any]:
    selected = TruthLens(str(lens).upper())
    if selected is TruthLens.CHARACTER and not character_id:
        raise ValueError("CHARACTER Lens 必须指定 character_id")
    knowledge = truth_knowledge_view(
        database, book_id, edition_id, chapter_ordinal=chapter_ordinal
    )
    visible: list[dict[str, Any]] = []

    def projected_truth(
        truth: dict[str, Any], state: KnowledgeState, label: str
    ) -> dict[str, Any]:
        if state in {KnowledgeState.KNOWN, KnowledgeState.CONFIRMED}:
            return truth
        return {
            "truth_id": truth["truth_id"],
            "truth_type": "REDACTED_KNOWLEDGE_TOPIC",
            "title": f"{label}已接触的未确认主题",
            "statement": "答案仍未揭露；这里只显示截至本章可感知的认知层级。",
            "description": "",
            "status": "KNOWLEDGE_PROJECTION",
            "compatibility_status": "REDACTED",
            "redacted": True,
        }

    for topic in knowledge["topics"]:
        if selected is TruthLens.AUTHOR:
            visible.append(topic)
        elif selected is TruthLens.READER:
            reader_state = KnowledgeState(str(topic["reader"]["state"]))
            if reader_state is not KnowledgeState.UNKNOWN:
                visible.append(
                    {
                        "truth": projected_truth(topic["truth"], reader_state, "读者"),
                        "author_state": "REDACTED",
                        "reader": topic["reader"],
                        "characters": [],
                        "reveal_plans": [],
                        "projection_state": reader_state.value,
                    }
                )
        else:
            matches = [
                item
                for item in topic["characters"]
                if item["character_id"] == character_id
                and item["state"] != KnowledgeState.UNKNOWN.value
            ]
            if matches:
                character_state = KnowledgeState(str(matches[0]["state"]))
                visible.append(
                    {
                        "truth": projected_truth(
                            topic["truth"], character_state, "该角色"
                        ),
                        "author_state": "REDACTED",
                        "reader": {"state": "REDACTED", "evidence": []},
                        "characters": [matches[0]],
                        "reveal_plans": [],
                        "selected_character_knowledge": matches[0],
                        "projection_state": character_state.value,
                    }
                )
    future = (
        [
            item
            for item in list_author_truths(
                database,
                book_id,
                edition_id,
                chapter_ordinal=chapter_ordinal,
                include_future=True,
            )
            if int(item["effective_from_chapter"]) > chapter_ordinal
        ]
        if selected is TruthLens.AUTHOR and include_future
        else []
    )
    return {
        "lens": selected.value,
        "character_id": character_id,
        "chapter_ordinal": chapter_ordinal,
        "topics": visible,
        "future_truths": future,
        "projection_only": True,
    }


def build_planning_truth_context(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_ordinal: int,
) -> dict[str, Any]:
    agenda = build_reveal_agenda(database, book_id, edition_id, chapter_ordinal)
    truths = [
        item
        for item in list_author_truths(
            database,
            book_id,
            edition_id,
            chapter_ordinal=chapter_ordinal,
            include_future=False,
        )
        if item["status"] == TruthStatus.ACTIVE_TRUTH.value
        and item["compatibility_status"]
        in {
            CompatibilityStatus.COMPATIBLE.value,
            CompatibilityStatus.COMPATIBLE_WITH_GAPS.value,
        }
    ]
    return {
        "target_chapter_ordinal": chapter_ordinal,
        "active_author_truths": truths,
        "reveal_agenda": agenda,
        "behavioral_rule": (
            "Active Author Truth 可约束人物选择、资源部署与势力行动；只有 Reveal Agenda "
            "授权的深度可以进入读者可见正文。KEEP_HIDDEN 不得直接说明答案。"
        ),
        "candidate_contract": {
            "required_fields": ["truth_alignment", "reveal_impact"],
            "keep_hidden_is_hard_boundary": True,
            "hint_requires_readable_clue": True,
            "hint_must_not_confirm_identity": True,
        },
    }


def apply_canon_reveal_trace_in_transaction(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    chapter_id: str,
    chapter_ordinal: int,
    draft_id: str,
    commit_id: str,
    reveal_trace: RevealTrace,
    approved_character_knowledge: set[tuple[str, str]],
) -> list[str]:
    """Commit realized knowledge only; Author Truth never enters Canon events."""

    event_ids: list[str] = []
    transitions = {
        (item.truth_id, item.target.value, item.target_entity_id): item
        for item in reveal_trace.knowledge_transitions
    }
    for event in reveal_trace.realized:
        truth = connection.execute(
            "SELECT status FROM author_truths WHERE truth_id=? AND book_id=? "
            "AND edition_id=?",
            (event.truth_id, book_id, edition_id),
        ).fetchone()
        if truth is None:
            raise ValueError(f"RevealEvent 引用了不存在的 Author Truth：{event.truth_id}")
        expected = _DEPTH_STATE[event.depth]
        if event.expected_knowledge_change is not expected:
            raise ValueError("RevealEvent expected_knowledge_change 必须与揭示深度精确对应")
        if event.reveal_plan_id:
            plan = connection.execute(
                "SELECT truth_id FROM reveal_plans WHERE reveal_plan_id=? AND book_id=? "
                "AND edition_id=?",
                (event.reveal_plan_id, book_id, edition_id),
            ).fetchone()
            if plan is None or str(plan["truth_id"]) != event.truth_id:
                raise ValueError("RevealEvent 的 reveal_plan_id 与 truth_id 不匹配")
        if event.target is RevealTarget.CHARACTER:
            assert event.target_entity_id is not None
            if (event.truth_id, event.target_entity_id) not in approved_character_knowledge:
                raise ValueError(
                    "角色获得 Author Truth 必须同时声明可审计的 knowledge StateChange"
                )
        reveal_event_id = f"reveal-event-{uuid.uuid4().hex}"
        evidence = [
            {
                "chapter_id": chapter_id,
                "chapter_ordinal": chapter_ordinal,
                "draft_id": draft_id,
                "commit_id": commit_id,
                "quote": event.evidence_quote,
                "depth": event.depth.value,
            }
        ]
        if event.target in {RevealTarget.READER, RevealTarget.PUBLIC_WORLD}:
            change = _append_reader_in_transaction(
                connection,
                book_id=book_id,
                edition_id=edition_id,
                truth_id=event.truth_id,
                state=event.expected_knowledge_change,
                chapter_ordinal=chapter_ordinal,
                evidence=evidence,
                provenance="CANON_REVEAL",
                provisional=False,
                as_of_chapter_id=chapter_id,
                reveal_event_id=reveal_event_id,
            )
        elif event.target is RevealTarget.CHARACTER:
            assert event.target_entity_id is not None
            change = _append_character_in_transaction(
                connection,
                book_id=book_id,
                edition_id=edition_id,
                truth_id=event.truth_id,
                character_id=event.target_entity_id,
                state=event.expected_knowledge_change,
                chapter_ordinal=chapter_ordinal,
                evidence=evidence,
                provenance="CANON_REVEAL",
                provisional=False,
                as_of_chapter_id=chapter_id,
                reveal_event_id=reveal_event_id,
            )
        else:
            change = {
                "before": KnowledgeState.UNKNOWN.value,
                "after": event.expected_knowledge_change.value,
            }
        declared = transitions.get(
            (event.truth_id, event.target.value, event.target_entity_id)
        )
        if declared is None:
            raise ValueError("每个 realized RevealEvent 都必须声明 KnowledgeTransition")
        if declared.before.value != change["before"] or declared.after.value != change["after"]:
            raise ValueError("KnowledgeTransition 与章节边界的真实知识变化不一致")
        connection.execute(
            "INSERT INTO reveal_events("
            "reveal_event_id, book_id, edition_id, truth_id, reveal_plan_id, target, "
            "target_entity_id, depth, evidence_quote, expected_knowledge_state, "
            "realized_knowledge_state, chapter_id, "
            "chapter_ordinal, draft_id, commit_id, status, created_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CANON', ?, 1)",
            (
                reveal_event_id,
                book_id,
                edition_id,
                event.truth_id,
                event.reveal_plan_id,
                event.target.value,
                event.target_entity_id,
                event.depth.value,
                event.evidence_quote,
                event.expected_knowledge_change.value,
                change["after"],
                chapter_id,
                chapter_ordinal,
                draft_id,
                commit_id,
                utc_now(),
            ),
        )
        event_ids.append(reveal_event_id)
        if event.depth in {RevealDepth.CONFIRMATION, RevealDepth.FULL_REVEAL} and event.target in {
            RevealTarget.READER,
            RevealTarget.PUBLIC_WORLD,
        }:
            connection.execute(
                "UPDATE author_truths SET status='REVEALED', updated_at=?, "
                "version=version+1 WHERE truth_id=?",
                (utc_now(), event.truth_id),
            )
    return event_ids


__all__ = [
    "AgendaBucket",
    "KnowledgeState",
    "KnowledgeTransition",
    "PlannedReveal",
    "RevealDepth",
    "RevealEvent",
    "RevealHorizon",
    "RevealPlanInput",
    "RevealPlanStatus",
    "RevealTarget",
    "RevealTrace",
    "SecretLifecycle",
    "TruthLens",
    "apply_canon_reveal_trace_in_transaction",
    "build_planning_truth_context",
    "build_reveal_agenda",
    "build_secret_board",
    "create_reveal_plan",
    "list_reveal_plans",
    "override_reveal_agenda",
    "project_truth_lens",
    "set_character_truth_knowledge",
    "set_reader_knowledge",
    "truth_knowledge_view",
]
