"""Explicit authoring readiness contracts.

Readiness is computed from structured, evidence-bearing records.  Field names or
free-form prose never make an authoring capability ready by themselves.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ReadinessModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CurrentProtagonistReadiness(ReadinessModel):
    entity_id: str | None = None
    confirmed: bool = False
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    current_state_available: bool = False


class ActiveMainThreadReadiness(ReadinessModel):
    thread_id: str
    confirmed: bool
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    status: str


class CurrentWorldBoundariesReadiness(ReadinessModel):
    confirmed_rules: list[dict[str, Any]] = Field(default_factory=list)
    unresolved_rules: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class CurrentCharacterStateReadiness(ReadinessModel):
    inventory_ready: bool = False
    abilities_ready: bool = False
    relationships_ready: bool = False
    knowledge_ready: bool = False


class CurrentNarrativeStateReadiness(ReadinessModel):
    active_promises: list[dict[str, Any]] = Field(default_factory=list)
    active_hooks: list[dict[str, Any]] = Field(default_factory=list)
    reveal_agenda_ready: bool = False


class ContinuationBoundaryReadiness(ReadinessModel):
    book_id: str
    edition_id: str
    target_chapter_ordinal: int = Field(ge=1)
    current_protagonist: CurrentProtagonistReadiness
    active_main_threads: list[ActiveMainThreadReadiness] = Field(default_factory=list)
    current_world_boundaries: CurrentWorldBoundariesReadiness
    current_character_state: CurrentCharacterStateReadiness
    current_narrative_state: CurrentNarrativeStateReadiness
    blocking_gaps: list[str] = Field(default_factory=list)
    ready_for_continuation: bool = False


class RevisionRangeReadiness(ReadinessModel):
    book_id: str
    edition_id: str
    target_chapter_ids: list[str]
    ready: bool
    required_deepening_chapter_ids: list[str] = Field(default_factory=list)
    affected_future_range: dict[str, int | None] = Field(default_factory=dict)
    affected_characters: list[str] = Field(default_factory=list)
    affected_items_and_abilities: list[str] = Field(default_factory=list)
    affected_relationships: list[str] = Field(default_factory=list)
    affected_knowledge: list[str] = Field(default_factory=list)
    affected_world_rules: list[str] = Field(default_factory=list)
    affected_threads: list[str] = Field(default_factory=list)
    blocking_gaps: list[str] = Field(default_factory=list)


def _as_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _item_id(item: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = str(item.get(key) or "").strip()
        if value:
            return value
    return None


def _status_is_current(item: dict[str, Any]) -> bool:
    status = str(item.get("status") or item.get("phase") or "ACTIVE").upper()
    return status not in {"ARCHIVED", "CLOSED", "RESOLVED", "REJECTED", "INACTIVE"}


def _applicable(item: dict[str, Any], target_ordinal: int) -> bool:
    start = item.get("effective_from_chapter") or item.get("chapter_ordinal")
    end = item.get("effective_until_chapter")
    try:
        if start is not None and int(start) >= target_ordinal:
            return False
        if end is not None and int(end) < target_ordinal - 1:
            return False
    except (TypeError, ValueError):
        return False
    return True


def _validated_evidence(
    connection: sqlite3.Connection,
    book_id: str,
    item: dict[str, Any],
    target_ordinal: int,
) -> list[dict[str, Any]]:
    raw_ids = item.get("source_span_ids") or []
    span_ids = (
        [str(value) for value in raw_ids if str(value).strip()] if isinstance(raw_ids, list) else []
    )
    raw_evidence = item.get("source_evidence") or []
    if isinstance(raw_evidence, list):
        for evidence in raw_evidence:
            if isinstance(evidence, str) and evidence.strip():
                span_ids.append(evidence)
            elif isinstance(evidence, dict):
                span_id = str(evidence.get("source_span_id") or evidence.get("span_id") or "")
                if span_id:
                    span_ids.append(span_id)
    if not span_ids:
        return []
    placeholders = ",".join("?" for _ in span_ids)
    rows = connection.execute(
        "SELECT s.span_id, s.chapter_id, c.ordinal FROM source_spans s "
        "LEFT JOIN chapters c ON c.chapter_id=s.chapter_id "
        f"WHERE s.book_id=? AND s.span_id IN ({placeholders})",
        (book_id, *span_ids),
    ).fetchall()
    return [
        {
            "source_span_id": str(row["span_id"]),
            "chapter_id": None if row["chapter_id"] is None else str(row["chapter_id"]),
            "chapter_ordinal": None if row["ordinal"] is None else int(row["ordinal"]),
        }
        for row in rows
        if row["ordinal"] is None or int(row["ordinal"]) < target_ordinal
    ]


def _evidence_bearing(
    connection: sqlite3.Connection,
    book_id: str,
    items: list[dict[str, Any]],
    target_ordinal: int,
) -> list[tuple[dict[str, Any], list[dict[str, Any]]]]:
    result = []
    for item in items:
        evidence = _validated_evidence(connection, book_id, item, target_ordinal)
        if evidence and _applicable(item, target_ordinal):
            result.append((item, evidence))
    return result


def evaluate_continuation_boundary(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    target_chapter_ordinal: int,
    graphs: dict[str, Any] | None,
) -> ContinuationBoundaryReadiness:
    graph = graphs if isinstance(graphs, dict) else {}
    characters = _evidence_bearing(
        connection, book_id, _as_dicts(graph.get("characters")), target_chapter_ordinal
    )
    protagonist_item: dict[str, Any] | None = None
    protagonist_evidence: list[dict[str, Any]] = []
    for item, evidence in characters:
        role_value = item.get("roles")
        roles: list[Any] = list(role_value) if isinstance(role_value, list) else []
        explicit = (
            item.get("is_protagonist") is True
            or str(item.get("role") or "").upper()
            in {
                "PROTAGONIST",
                "主角",
            }
            or any(str(role).upper() in {"PROTAGONIST", "主角"} for role in roles)
        )
        if explicit and _item_id(item, "entity_id", "character_id", "id"):
            protagonist_item = item
            protagonist_evidence = evidence
            break
    current_state = protagonist_item.get("current_state") if protagonist_item else None
    current_state_available = isinstance(current_state, dict) and any(
        value not in (None, "", [], {}) for value in current_state.values()
    )
    protagonist = CurrentProtagonistReadiness(
        entity_id=(
            None
            if protagonist_item is None
            else _item_id(protagonist_item, "entity_id", "character_id", "id")
        ),
        confirmed=protagonist_item is not None and bool(protagonist_evidence),
        evidence=protagonist_evidence,
        current_state_available=current_state_available,
    )

    thread_items = _as_dicts(graph.get("plot_threads")) or _as_dicts(graph.get("main_threads"))
    threads: list[ActiveMainThreadReadiness] = []
    for item, evidence in _evidence_bearing(
        connection, book_id, thread_items, target_chapter_ordinal
    ):
        thread_id = _item_id(item, "thread_id", "id")
        has_content = bool(
            str(item.get("goal") or item.get("summary") or item.get("title") or "").strip()
        )
        if thread_id and has_content and _status_is_current(item):
            threads.append(
                ActiveMainThreadReadiness(
                    thread_id=thread_id,
                    confirmed=True,
                    evidence=evidence,
                    status=str(item.get("status") or item.get("phase") or "ACTIVE"),
                )
            )

    rules = _evidence_bearing(
        connection, book_id, _as_dicts(graph.get("world_rules")), target_chapter_ordinal
    )
    exceptions = _evidence_bearing(
        connection, book_id, _as_dicts(graph.get("rule_exceptions")), target_chapter_ordinal
    )
    world = CurrentWorldBoundariesReadiness(
        confirmed_rules=[item for item, _ in rules],
        unresolved_rules=[
            item
            for item in _as_dicts(graph.get("unresolved_rules"))
            if _applicable(item, target_chapter_ordinal)
        ],
        evidence=[evidence for _, values in [*rules, *exceptions] for evidence in values],
    )

    def has_evidence(key: str) -> bool:
        return bool(
            _evidence_bearing(
                connection, book_id, _as_dicts(graph.get(key)), target_chapter_ordinal
            )
        )

    character_state = CurrentCharacterStateReadiness(
        inventory_ready=has_evidence("resources") or has_evidence("items"),
        abilities_ready=has_evidence("abilities"),
        relationships_ready=has_evidence("relationships"),
        knowledge_ready=has_evidence("knowledge_changes") or has_evidence("knowledge"),
    )
    promises = [
        item
        for item, _ in _evidence_bearing(
            connection, book_id, _as_dicts(graph.get("promises")), target_chapter_ordinal
        )
        if _status_is_current(item)
    ]
    hooks = [
        item
        for item, _ in _evidence_bearing(
            connection, book_id, _as_dicts(graph.get("hooks")), target_chapter_ordinal
        )
        if _status_is_current(item)
    ]
    narrative = CurrentNarrativeStateReadiness(
        active_promises=promises,
        active_hooks=hooks,
        reveal_agenda_ready=graph.get("reveal_agenda_ready") is True,
    )
    gaps: list[str] = []
    if not protagonist.confirmed:
        gaps.append("当前主角缺少明确实体与真实章节证据")
    elif not protagonist.current_state_available:
        gaps.append("当前主角状态尚未建立")
    if not threads:
        gaps.append("当前主线程缺少有效内容、状态或证据")
    if not world.confirmed_rules:
        gaps.append("当前适用的世界规则边界尚未确认")
    for ready, label in (
        (character_state.inventory_ready, "当前物品状态"),
        (character_state.abilities_ready, "当前能力边界"),
        (character_state.relationships_ready, "当前关系状态"),
        (character_state.knowledge_ready, "当前人物认知状态"),
        (narrative.reveal_agenda_ready, "当前揭示安排"),
    ):
        if not ready:
            gaps.append(f"{label}尚未确认")
    return ContinuationBoundaryReadiness(
        book_id=book_id,
        edition_id=edition_id,
        target_chapter_ordinal=target_chapter_ordinal,
        current_protagonist=protagonist,
        active_main_threads=threads,
        current_world_boundaries=world,
        current_character_state=character_state,
        current_narrative_state=narrative,
        blocking_gaps=gaps,
        ready_for_continuation=not gaps,
    )


_REVISION_IMPACT_FIELDS: dict[str, tuple[str, ...]] = {
    "affected_characters": ("characters_present", "character_state_changes"),
    "affected_items_and_abilities": (
        "items_acquired",
        "items_lost",
        "items_transferred",
        "ability_changes",
    ),
    "affected_relationships": ("relationship_changes",),
    "affected_knowledge": ("knowledge_changes",),
    "affected_world_rules": ("world_rule_changes", "rule_exceptions"),
    "affected_threads": (
        "thread_advances",
        "promises_created",
        "promises_paid",
        "hooks_created",
        "hooks_advanced",
    ),
}


def _impact_references(delta: dict[str, Any], fields: tuple[str, ...]) -> set[str]:
    references: set[str] = set()
    for field_name in fields:
        values = delta.get(field_name)
        if not isinstance(values, list):
            continue
        for item in values:
            if isinstance(item, str) and item.strip():
                references.add(item.strip())
                continue
            if not isinstance(item, dict):
                continue
            for key in (
                "entity_id",
                "character_id",
                "item_id",
                "ability_id",
                "relationship_id",
                "knowledge_id",
                "rule_id",
                "thread_id",
                "promise_id",
                "hook_id",
                "id",
                "name",
                "title",
            ):
                value = str(item.get(key) or "").strip()
                if value:
                    references.add(value)
    return references


def evaluate_revision_range(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    edition_id: str,
    target_chapter_ids: list[str],
) -> RevisionRangeReadiness:
    """Evaluate whether a revision range has reusable continuity evidence.

    The target chapters and their immediate neighbours must have current-source
    continuity records.  Structured references are then followed through later
    analysed chapters to expose the known future impact range.
    """

    if not target_chapter_ids:
        raise ValueError("改写范围不能为空")
    placeholders = ",".join("?" for _ in target_chapter_ids)
    target_rows = connection.execute(
        "SELECT chapter_id, ordinal, version FROM chapters "
        f"WHERE book_id=? AND chapter_id IN ({placeholders}) ORDER BY ordinal",
        (book_id, *target_chapter_ids),
    ).fetchall()
    found_ids = {str(row["chapter_id"]) for row in target_rows}
    missing_targets = [item for item in target_chapter_ids if item not in found_ids]
    if missing_targets:
        raise ValueError("改写目标章节不存在：" + "、".join(missing_targets))

    target_ordinals = {int(row["ordinal"]) for row in target_rows}
    min_target = min(target_ordinals)
    max_target = max(target_ordinals)
    required_ordinals = target_ordinals | {
        ordinal for ordinal in (min_target - 1, max_target + 1) if ordinal >= 1
    }
    ordinal_placeholders = ",".join("?" for _ in required_ordinals)
    required_rows = connection.execute(
        "SELECT chapter_id, ordinal, version FROM chapters "
        f"WHERE book_id=? AND ordinal IN ({ordinal_placeholders}) ORDER BY ordinal",
        (book_id, *sorted(required_ordinals)),
    ).fetchall()
    required_meta = {
        str(row["chapter_id"]): (int(row["ordinal"]), f"chapter-v{int(row['version'])}")
        for row in required_rows
    }
    required_ids = list(required_meta)
    record_placeholders = ",".join("?" for _ in required_ids)
    rows = connection.execute(
        "SELECT chapter_id, status, source_revision, result_json "
        "FROM chapter_analysis_records WHERE book_id=? AND edition_id=? "
        "AND analysis_layer='CONTINUITY' "
        f"AND chapter_id IN ({record_placeholders})",
        (book_id, edition_id, *required_ids),
    ).fetchall()
    current_records: dict[str, tuple[str, dict[str, Any]]] = {}
    for row in rows:
        chapter_id = str(row["chapter_id"])
        if row["source_revision"] != required_meta[chapter_id][1]:
            continue
        try:
            result = json.loads(str(row["result_json"] or "{}"))
        except json.JSONDecodeError:
            result = {}
        current_records[chapter_id] = (str(row["status"]).upper(), result)

    required_deepening = [
        chapter_id
        for chapter_id in required_ids
        if chapter_id not in current_records or current_records[chapter_id][0] == "UNKNOWN"
    ]
    affected: dict[str, set[str]] = {
        output_field: set() for output_field in _REVISION_IMPACT_FIELDS
    }
    for _, delta in current_records.values():
        for output_field, delta_fields in _REVISION_IMPACT_FIELDS.items():
            affected[output_field].update(_impact_references(delta, delta_fields))

    future_start: int | None = None
    future_end: int | None = None
    all_references = set().union(*affected.values()) if affected else set()
    if all_references:
        future_rows = connection.execute(
            "SELECT c.ordinal, r.status, r.source_revision, r.result_json, c.version "
            "FROM chapter_analysis_records r "
            "JOIN chapters c ON c.chapter_id=r.chapter_id "
            "WHERE r.book_id=? AND r.edition_id=? AND r.analysis_layer='CONTINUITY' "
            "AND c.ordinal>? ORDER BY c.ordinal",
            (book_id, edition_id, max_target),
        ).fetchall()
        for row in future_rows:
            if row["source_revision"] != f"chapter-v{int(row['version'])}":
                continue
            try:
                delta = json.loads(str(row["result_json"] or "{}"))
            except json.JSONDecodeError:
                continue
            future_references = set().union(
                *(_impact_references(delta, fields) for fields in _REVISION_IMPACT_FIELDS.values())
            )
            if all_references & future_references:
                ordinal = int(row["ordinal"])
                future_start = ordinal if future_start is None else min(future_start, ordinal)
                future_end = ordinal if future_end is None else max(future_end, ordinal)

    gaps: list[str] = []
    if required_deepening:
        gaps.append("目标章节及相邻章节的连续性证据尚未完整")
    if any(status == "UNKNOWN" for status, _ in current_records.values()):
        gaps.append("改写范围中仍有无法确认的历史变化")
    return RevisionRangeReadiness(
        book_id=book_id,
        edition_id=edition_id,
        target_chapter_ids=target_chapter_ids,
        ready=not gaps,
        required_deepening_chapter_ids=required_deepening,
        affected_future_range={"start": future_start, "end": future_end},
        affected_characters=sorted(affected["affected_characters"]),
        affected_items_and_abilities=sorted(affected["affected_items_and_abilities"]),
        affected_relationships=sorted(affected["affected_relationships"]),
        affected_knowledge=sorted(affected["affected_knowledge"]),
        affected_world_rules=sorted(affected["affected_world_rules"]),
        affected_threads=sorted(affected["affected_threads"]),
        blocking_gaps=gaps,
    )


ChapterAnalysisLayer = Literal["CONTINUITY", "LITERARY", "BOUNDARY"]


__all__ = [
    "ChapterAnalysisLayer",
    "ContinuationBoundaryReadiness",
    "RevisionRangeReadiness",
    "evaluate_continuation_boundary",
    "evaluate_revision_range",
]
