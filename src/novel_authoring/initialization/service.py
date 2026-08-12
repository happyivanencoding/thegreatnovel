# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.db.database import Database
from novel_authoring.edition import edition_chapters, resolve_edition_id
from novel_authoring.readiness import (
    ContinuationBoundaryReadiness,
    evaluate_continuation_boundary,
)
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.manifest import authority_path, manifest_hash
from novel_authoring.storage.operations import ensure_operation
from novel_authoring.utils import json_dumps, sha256_file, stable_id, utc_now


class InitializationError(RuntimeError):
    """A deterministic initialization contract or state error."""


class InitializationState(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    SOURCE_MAPPED = "SOURCE_MAPPED"
    ARC_EXTRACTION_RUNNING = "ARC_EXTRACTION_RUNNING"
    ENTITY_RESOLUTION_RUNNING = "ENTITY_RESOLUTION_RUNNING"
    SYNTHESIS_RUNNING = "SYNTHESIS_RUNNING"
    ATLAS_VALIDATION_RUNNING = "ATLAS_VALIDATION_RUNNING"
    METRIC_BOOTSTRAP_RUNNING = "METRIC_BOOTSTRAP_RUNNING"
    VISUAL_RENDERING_RUNNING = "VISUAL_RENDERING_RUNNING"
    READY_WITH_GAPS = "READY_WITH_GAPS"
    READY = "READY"
    BLOCKED = "BLOCKED"
    STALE = "STALE"


class InitializationDepth(StrEnum):
    QUICK = "QUICK"
    BALANCED = "BALANCED"
    FULL = "FULL"


class InitializationBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ChapterCoverage(InitializationBase):
    ordinal: int = Field(ge=1)
    raw_heading: str
    logical_heading: str
    chapter_id: str
    source_span_ids: list[str] = Field(default_factory=list)
    content_sha256: str
    char_count: int = Field(ge=0)
    inferred_volume: str | None = None
    assigned_arc_id: str
    analysis_status: str = "PENDING"


class ArcRecord(InitializationBase):
    arc_id: str
    ordinal: int = Field(ge=1)
    start_chapter: int = Field(ge=1)
    end_chapter: int = Field(ge=1)
    chapter_ids: list[str]
    source_span_ids: list[str]
    char_count: int = Field(ge=0)
    inferred_volume: str | None = None
    boundary_reason: str
    status: str = "PENDING"
    semantic_chapter_ids: list[str] = Field(default_factory=list)
    continuity_chapter_ids: list[str] = Field(default_factory=list)
    operation_id: str | None = None
    operation_input_path: str | None = None
    reused_from_arc_id: str | None = None
    reused_semantic_chapter_ids: list[str] = Field(default_factory=list)
    reused_continuity_chapter_ids: list[str] = Field(default_factory=list)
    scheduled_semantic_chapter_ids: list[str] = Field(default_factory=list)
    scheduled_continuity_chapter_ids: list[str] = Field(default_factory=list)
    reused_output_path: str | None = None


class ArcManifest(InitializationBase):
    schema_version: str = "arc-manifest-v1"
    initialization_id: str
    book_id: str
    edition_id: str
    arcs: list[ArcRecord]
    max_chapters_per_arc: int = 20
    char_limit: int = Field(default=80_000, ge=1)


class SourceCoverage(InitializationBase):
    schema_version: str = "source-coverage-v1"
    book_id: str
    edition_id: str
    source_manifest_sha256: str
    effective_chapter_count: int = Field(ge=0)
    covered_chapter_count: int = Field(ge=0)
    chapter_coverage: float = Field(ge=0, le=1)
    chapters: list[ChapterCoverage]
    diagnostics: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def counts_match(self) -> SourceCoverage:
        if self.covered_chapter_count > self.effective_chapter_count:
            raise ValueError("covered_chapter_count 不能超过 effective_chapter_count")
        return self


class ArcExtractionOutput(InitializationBase):
    """Strict top-level Arc output; semantic payloads remain evidence-bearing dicts."""

    schema_version: str = "arc-extraction-v1"
    initialization_id: str
    arc_id: str
    source_evidence: list[dict[str, Any]] = Field(default_factory=list)
    characters: list[dict[str, Any]] = Field(default_factory=list)
    aliases: list[dict[str, Any]] = Field(default_factory=list)
    factions: list[dict[str, Any]] = Field(default_factory=list)
    relationships: list[dict[str, Any]] = Field(default_factory=list)
    abilities: list[dict[str, Any]] = Field(default_factory=list)
    ability_evolution: list[dict[str, Any]] = Field(default_factory=list)
    items: list[dict[str, Any]] = Field(default_factory=list)
    resources: list[dict[str, Any]] = Field(default_factory=list)
    production_chains: list[dict[str, Any]] = Field(default_factory=list)
    regions: list[dict[str, Any]] = Field(default_factory=list)
    region_connections: list[dict[str, Any]] = Field(default_factory=list)
    world_rules: list[dict[str, Any]] = Field(default_factory=list)
    rule_exceptions: list[dict[str, Any]] = Field(default_factory=list)
    major_events: list[dict[str, Any]] = Field(default_factory=list)
    promises: list[dict[str, Any]] = Field(default_factory=list)
    hooks: list[dict[str, Any]] = Field(default_factory=list)
    main_threads: list[dict[str, Any]] = Field(default_factory=list)
    secondary_threads: list[dict[str, Any]] = Field(default_factory=list)
    protagonist_decisions: list[dict[str, Any]] = Field(default_factory=list)
    leverage_events: list[dict[str, Any]] = Field(default_factory=list)
    payoff_events: list[dict[str, Any]] = Field(default_factory=list)
    pressure_events: list[dict[str, Any]] = Field(default_factory=list)
    stage_transition_signals: list[dict[str, Any]] = Field(default_factory=list)
    chapter_continuity_deltas: list[dict[str, Any]] = Field(default_factory=list)
    chapter_semantic_features: list[dict[str, Any]] = Field(default_factory=list)
    unresolved_questions: list[dict[str, Any]] = Field(default_factory=list)
    contradictions: list[dict[str, Any]] = Field(default_factory=list)

    @model_validator(mode="after")
    def evidence_boundary(self) -> ArcExtractionOutput:
        collections = (
            "characters",
            "factions",
            "relationships",
            "abilities",
            "items",
            "resources",
            "regions",
            "world_rules",
            "major_events",
            "promises",
            "hooks",
            "main_threads",
            "secondary_threads",
            "protagonist_decisions",
            "leverage_events",
            "payoff_events",
            "pressure_events",
            "contradictions",
        )
        for collection in collections:
            for item in getattr(self, collection):
                if "information_status" not in item:
                    raise ValueError(f"{collection} 的记录必须显式标记 information_status")
                status = str(item["information_status"]).upper()
                spans = item.get("source_span_ids") or item.get("source_evidence") or []
                if status == "CANON" and not spans:
                    raise ValueError(f"{collection} 的 CANON 记录必须有 source_span_ids")
                if status == "INFERENCE":
                    missing = [
                        key
                        for key in (
                            "reasoning_summary",
                            "confidence",
                            "counter_evidence",
                            "unknown_boundary",
                        )
                        if key not in item
                    ]
                    if missing:
                        raise ValueError(f"{collection} 的 INFERENCE 记录缺少 {missing}")
                    if not spans:
                        raise ValueError(f"{collection} 的 INFERENCE 记录必须有 source_span_ids")
        return self


class EntityResolutionResult(InitializationBase):
    schema_version: str = "entity-resolution-v1"
    initialization_id: str
    entity_resolution_map: list[dict[str, Any]] = Field(default_factory=list)
    alias_conflicts: list[dict[str, Any]] = Field(default_factory=list)
    unresolved_identity_candidates: list[dict[str, Any]] = Field(default_factory=list)
    identified_major_entities: int = Field(default=0, ge=0)
    resolved_major_entities: int = Field(default=0, ge=0)


class InitializationReadiness(InitializationBase):
    status: str
    chapter_coverage: float = Field(ge=0, le=1)
    arc_coverage: float = Field(ge=0, le=1)
    source_mapping_coverage: float = Field(default=0.0, ge=0, le=1)
    arc_output_coverage: float = Field(default=0.0, ge=0, le=1)
    chapter_semantic_feature_coverage: float = Field(default=0.0, ge=0, le=1)
    continuity_index_coverage: float = Field(default=0.0, ge=0, le=1)
    metric_observation_coverage: float = Field(default=0.0, ge=0, le=1)
    recent_detailed_metric_coverage: float = Field(default=0.0, ge=0, le=1)
    current_chapter_metric_coverage: float = Field(default=0.0, ge=0, le=1)
    metric_bootstrap_status: str = "NOT_READY"
    metric_authority: str = "PROVISIONAL"
    metric_bootstrap: dict[str, Any] = Field(default_factory=dict)
    canon_evidence_coverage: float = Field(ge=0, le=1)
    entity_resolution_coverage: float = Field(ge=0, le=1)
    core_graphs_complete: bool = False
    protagonist_confirmed: bool = False
    current_thread_confirmed: bool = False
    continuation_boundary: ContinuationBoundaryReadiness | None = None
    blocking_reasons: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    review_queue: list[str] = Field(default_factory=list)


class InitializationManifest(InitializationBase):
    schema_version: str = "novel-initialization-v1"
    initialization_id: str
    book_id: str
    edition_id: str
    source_manifest_sha256: str
    effective_content_sha256: str
    created_at: str
    pipeline: list[str]
    state: InitializationState
    source_coverage_path: str
    arc_manifest_path: str
    contract_hashes: dict[str, str]
    chapter_count: int = Field(ge=0)
    arc_count: int = Field(ge=0)
    current_core_requirements: list[str]
    future_can_remain_incomplete: bool = True
    initialization_depth: InitializationDepth = InitializationDepth.FULL
    analysis_plan: dict[str, Any] = Field(default_factory=dict)
    deep_chapter_ids: list[str] = Field(default_factory=list)
    lightweight_chapter_ids: list[str] = Field(default_factory=list)
    uncovered_semantic_chapter_ids: list[str] = Field(default_factory=list)
    current_boundary_window: list[str] = Field(default_factory=list)
    capabilities: dict[str, bool] = Field(default_factory=dict)
    upgrade_from_initialization_id: str | None = None
    reused_arc_ids: list[str] = Field(default_factory=list)
    scheduled_arc_ids: list[str] = Field(default_factory=list)
    requested_action: str | None = None
    structural_index_path: str = "structural_index.json"


_VOLUME_HEADING = re.compile(r"第\s*([0-9零一二三四五六七八九十百千]+)\s*卷")
_RECALL_TERM = re.compile(
    r"[\u4e00-\u9fffA-Za-z0-9]{2,12}(?:能力|规则|组织|联盟|城市|基地|物品|资源|关系|线索)"
)
_CHANGE_MARKERS = re.compile(r"获得|失去|升级|突破|死亡|背叛|揭示|发现|决定|改变|转折")
_RISK_MARKERS = re.compile(r"危险|死亡|失败|代价|受伤|追杀|危机|倒计时|期限")
_PAYOFF_MARKERS = re.compile(r"兑现|成功|胜利|奖励|完成|解决|真相")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_dumps(value, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _book_workspace(database: Database, book_id: str) -> Path:
    row = database.scalar("SELECT workspace_root FROM books WHERE book_id=?", (book_id,))
    if row is None:
        raise InitializationError(f"未知 book_id：{book_id}")
    return Path(str(row)).resolve()


def initialization_root(
    database: Database,
    book_id: str,
    edition_id: str | None = None,
    initialization_id: str | None = None,
) -> Path:
    database.initialize()
    selected = resolve_edition_id(database, book_id, edition_id)
    book_root = _book_workspace(database, book_id)
    if (book_root / "book.yaml").is_file():
        root = BookLayout(book_root.parent).for_book(book_id).edition(selected).initialization
    else:
        root = book_root / "editions" / selected / "initialization"
    if initialization_id:
        root = root / initialization_id
    return root


def _source_manifest_hash(database: Database, book_id: str) -> str:
    root = _book_workspace(database, book_id)
    path = authority_path(root)
    return manifest_hash(path) if path.is_file() else ""


def _infer_volume(row: dict[str, Any]) -> str | None:
    value = row.get("volume_title")
    if value:
        return str(value)
    heading = str(row.get("raw_heading") or row.get("title") or "")
    matched = _VOLUME_HEADING.search(heading)
    return matched.group(0) if matched else None


def _chapter_rows(database: Database, book_id: str, edition_id: str) -> list[dict[str, Any]]:
    with database.connect() as connection:
        return [dict(row) for row in edition_chapters(connection, book_id, edition_id)]


def calculate_source_coverage(
    database: Database, book_id: str, edition_id: str | None = None
) -> dict[str, Any]:
    """Calculate source/span coverage from database intervals, not declarations."""
    database.initialize()
    selected = resolve_edition_id(database, book_id, edition_id)
    chapters = _chapter_rows(database, book_id, selected)
    anomalies: list[str] = []
    ordinals = [int(item["ordinal"]) for item in chapters]
    if ordinals != list(range(1, len(ordinals) + 1)):
        anomalies.append("章节 source ordinal 不连续或重复")
    missing_spans: list[str] = []
    duplicate_spans: list[str] = []
    with database.connect() as connection:
        spans = connection.execute(
            "SELECT span_id, chapter_id, document_id, start_char, end_char, text_sha256 "
            "FROM source_spans WHERE book_id=? ORDER BY document_id, start_char, span_id",
            (book_id,),
        ).fetchall()
    span_rows = [dict(row) for row in spans]
    spans_by_chapter: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in span_rows:
        spans_by_chapter[str(row.get("chapter_id") or "")].append(row)
    for item in chapters:
        chapter_id = str(item["chapter_id"])
        related = spans_by_chapter.get(chapter_id, [])
        if not related:
            missing_spans.append(chapter_id)
        if len(related) > 1:
            duplicate_spans.append(chapter_id)
        if related and str(related[0].get("text_sha256")) != str(item.get("content_sha256")):
            anomalies.append(f"chapter {chapter_id} content hash 与 source span 不一致")
    by_document: dict[str, list[tuple[int, int]]] = {}
    for row in span_rows:
        by_document.setdefault(str(row["document_id"]), []).append(
            (int(row["start_char"]), int(row["end_char"]))
        )
    document_diagnostics: list[dict[str, Any]] = []
    whole_source_ok = True
    for document_id, intervals in by_document.items():
        intervals = sorted(intervals)
        overlap = any(
            end > next_start
            for (_, end), (next_start, _) in zip(intervals, intervals[1:], strict=False)
        )
        start = intervals[0][0] if intervals else 0
        end = max((item[1] for item in intervals), default=0)
        union = 0
        cursor = start
        for left, right in intervals:
            if left > cursor:
                whole_source_ok = False
            cursor = max(cursor, right)
            union = cursor - start
        if overlap:
            anomalies.append(f"document {document_id} source span 存在重叠")
            whole_source_ok = False
        document_diagnostics.append(
            {
                "document_id": document_id,
                "start_char": start,
                "end_char": end,
                "covered_char_count": union,
                "interval_count": len(intervals),
                "coverage": 1.0 if end == start else union / max(1, end - start),
                "overlap": overlap,
            }
        )
    return {
        "book_id": book_id,
        "edition_id": selected,
        "source_manifest_sha256": _source_manifest_hash(database, book_id),
        "effective_chapter_count": len(chapters),
        "covered_chapter_count": len(chapters) - len(missing_spans),
        "chapter_coverage": (
            (len(chapters) - len(missing_spans)) / len(chapters) if chapters else 0.0
        ),
        "whole_source_coverage": 1.0 if whole_source_ok and not missing_spans else 0.0,
        "missing_source_spans": missing_spans,
        "duplicate_source_spans": duplicate_spans,
        "anomalies": sorted(set(anomalies)),
        "documents": document_diagnostics,
        "status": (
            "BLOCKED"
            if missing_spans or duplicate_spans or not whole_source_ok
            else ("FULL_WITH_ANOMALIES" if anomalies else "FULL")
        ),
    }


def _propose_arcs(
    book_id: str,
    edition_id: str,
    initialization_id: str,
    chapters: list[dict[str, Any]],
    *,
    char_limit: int,
    max_chapters: int = 20,
) -> list[ArcRecord]:
    if not chapters:
        return []
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    current_volume: str | None = None
    for row in chapters:
        volume = _infer_volume(row)
        chars = len(str(row.get("content") or ""))
        force_volume = bool(current and volume and current_volume and volume != current_volume)
        force_size = bool(
            current and (len(current) >= max_chapters or current_chars + chars > char_limit)
        )
        if force_volume or force_size:
            groups.append(current)
            current = []
            current_chars = 0
            current_volume = volume
        if not current:
            current_volume = volume
        current.append(row)
        current_chars += chars
    if current:
        groups.append(current)
    arcs: list[ArcRecord] = []
    for index, group in enumerate(groups, start=1):
        first, last = group[0], group[-1]
        source_spans = [
            str(item.get("source_span_id")) for item in group if item.get("source_span_id")
        ]
        arc_id = stable_id(
            "init-arc",
            book_id,
            edition_id,
            initialization_id,
            str(first["ordinal"]),
            str(last["ordinal"]),
        )
        reason = (
            "volume boundary"
            if len({str(_infer_volume(item)) for item in group}) > 1
            else "chapter window"
        )
        arcs.append(
            ArcRecord(
                arc_id=arc_id,
                ordinal=index,
                start_chapter=int(first["ordinal"]),
                end_chapter=int(last["ordinal"]),
                chapter_ids=[str(item["chapter_id"]) for item in group],
                source_span_ids=source_spans,
                char_count=sum(len(str(item.get("content") or "")) for item in group),
                inferred_volume=_infer_volume(first),
                boundary_reason=reason,
            )
        )
    return arcs


def _event(root: Path, event_type: str, payload: dict[str, Any]) -> None:
    path = root / "events.jsonl"
    event = {"event_type": event_type, "created_at": utc_now(), **payload}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json_dumps(event) + "\n")


def _eta_range_label(seconds: float) -> str:
    minutes = max(5.0, seconds / 60.0)
    lower = max(5, int((minutes * 0.75) // 5) * 5)
    upper = max(lower + 5, int((minutes * 1.25 + 4.999) // 5) * 5)
    return f"大约 {lower}—{upper} 分钟"


def _arc_schema() -> dict[str, Any]:
    schema = ArcExtractionOutput.model_json_schema()
    schema["additionalProperties"] = False
    return schema


def _arc_operation_id(initialization_id: str, arc_id: str) -> str:
    return f"{initialization_id}-arc-{arc_id}"


def arc_output_path(
    root: Path,
    initialization_id: str,
    book_id: str,
    edition_id: str,
    arc_id: str,
) -> Path:
    """Resolve an Arc result in the canonical operation workspace."""

    book_root = next(
        (candidate for candidate in (root, *root.parents) if (candidate / "book.yaml").is_file()),
        None,
    )
    if book_root is None:
        return root / "arc_outputs" / arc_id / "output.json"
    edition = BookLayout(book_root.parent).for_book(book_id).edition(edition_id)
    return edition.operation(_arc_operation_id(initialization_id, arc_id)).output / "output.json"


def _chapter_structure_record(row: dict[str, Any], arc_id: str) -> dict[str, Any]:
    content = str(row.get("content") or "")
    terms = sorted(set(_RECALL_TERM.findall(content)))[:30]
    change_count = len(_CHANGE_MARKERS.findall(content))
    risk_count = len(_RISK_MARKERS.findall(content))
    payoff_count = len(_PAYOFF_MARKERS.findall(content))
    recall_hints = [
        {
            "term": term,
            "category": next(
                (
                    label
                    for suffix, label in (
                        ("能力", "ABILITY_CANDIDATE"),
                        ("规则", "RULE_CANDIDATE"),
                        ("组织", "FACTION_CANDIDATE"),
                        ("联盟", "FACTION_CANDIDATE"),
                        ("城市", "LOCATION_CANDIDATE"),
                        ("基地", "LOCATION_CANDIDATE"),
                        ("物品", "ITEM_CANDIDATE"),
                        ("资源", "RESOURCE_CANDIDATE"),
                        ("关系", "RELATIONSHIP_CANDIDATE"),
                        ("线索", "THREAD_CANDIDATE"),
                    )
                    if term.endswith(suffix)
                ),
                "ENTITY_CANDIDATE",
            ),
            "status": "RECALL_HINT",
            "information_status": None,
            "first_occurrence": False,
            "source_span_ids": ([str(row["source_span_id"])] if row.get("source_span_id") else []),
        }
        for term in terms
    ]
    return {
        "chapter_id": str(row["chapter_id"]),
        "ordinal": int(row["ordinal"]),
        "heading": str(row.get("raw_heading") or row.get("title") or ""),
        "arc_id": arc_id,
        "char_count": len(content),
        "source_span_ids": ([str(row["source_span_id"])] if row.get("source_span_id") else []),
        "change_marker_count": change_count,
        "risk_marker_count": risk_count,
        "payoff_marker_count": payoff_count,
        "selection_score": (change_count * 3 + risk_count * 2 + payoff_count * 2 + len(terms)),
        "recall_hints": recall_hints,
        "candidate_mentions": recall_hints,
        "semantic_status": "UNKNOWN",
        "unknown_boundary": "尚未执行该章节的 Codex 语义分析",
    }


def _select_deep_chapters(
    depth: InitializationDepth,
    chapters: list[dict[str, Any]],
    arcs: list[ArcRecord],
    structural_records: list[dict[str, Any]],
) -> tuple[set[str], dict[str, list[str]]]:
    all_ids = [str(item["chapter_id"]) for item in chapters]
    reasons: dict[str, set[str]] = defaultdict(set)

    def include(rows: list[dict[str, Any]], reason: str) -> None:
        for row in rows:
            reasons[str(row["chapter_id"])].add(reason)

    if depth is InitializationDepth.FULL:
        include(chapters, "FULL_ALL_CHAPTERS")
    else:
        opening = 3 if depth is InitializationDepth.QUICK else 5
        latest = 5 if depth is InitializationDepth.QUICK else 12
        include(chapters[:opening], "OPENING_FOUNDATION")
        include(chapters[-latest:], "CURRENT_BOUNDARY_WINDOW")
        by_id = {str(item["chapter_id"]): item for item in chapters}
        for arc in arcs:
            include(
                [by_id[arc.chapter_ids[0]], by_id[arc.chapter_ids[-1]]],
                "ARC_BOUNDARY",
            )
        ranked = sorted(
            structural_records,
            key=lambda item: (-int(item["selection_score"]), int(item["ordinal"])),
        )
        fraction = 0.10 if depth is InitializationDepth.QUICK else 0.20
        high_change_count = max(1, round(len(chapters) * fraction))
        include(
            [by_id[str(item["chapter_id"])] for item in ranked[:high_change_count]],
            "HIGH_CHANGE_SIGNAL",
        )
        if depth is InitializationDepth.BALANCED:
            current_arc = arcs[-1]
            include([by_id[item] for item in current_arc.chapter_ids], "CURRENT_ARC")
            active_terms = {
                str(hint["term"])
                for item in structural_records[-5:]
                for hint in item["recall_hints"]
            }
            # Two bounded passes provide deterministic dependency tracing without
            # pretending recall hints are semantic facts.
            for _ in range(2):
                matched = [
                    item
                    for item in structural_records
                    if any(str(hint["term"]) in active_terms for hint in item["recall_hints"])
                ]
                include(
                    [by_id[str(item["chapter_id"])] for item in matched],
                    "ACTIVE_DEPENDENCY_RECALL",
                )
                expanded = {str(hint["term"]) for item in matched for hint in item["recall_hints"]}
                if expanded <= active_terms:
                    break
                active_terms.update(expanded)
    selected = set(reasons)
    if depth is InitializationDepth.FULL:
        selected = set(all_ids)
    return selected, {key: sorted(value) for key, value in reasons.items()}


def _select_literary_chapters(
    depth: InitializationDepth,
    chapters: list[dict[str, Any]],
    arcs: list[ArcRecord],
    structural_records: list[dict[str, Any]],
) -> set[str]:
    if depth is InitializationDepth.FULL:
        return {str(item["chapter_id"]) for item in chapters}
    by_id = {str(item["chapter_id"]): item for item in structural_records}
    selected = {
        str(item["chapter_id"])
        for item in [
            *chapters[: (2 if depth is InitializationDepth.QUICK else 3)],
            *chapters[-(3 if depth is InitializationDepth.QUICK else 5) :],
        ]
    }
    for arc in arcs:
        representative = max(
            arc.chapter_ids,
            key=lambda chapter_id: int(by_id[chapter_id]["selection_score"]),
        )
        selected.add(representative)
    if depth is InitializationDepth.BALANCED and arcs:
        current_arc = arcs[-1]
        ranked_current = sorted(
            current_arc.chapter_ids,
            key=lambda chapter_id: -int(by_id[chapter_id]["selection_score"]),
        )
        selected.update(ranked_current[:2])
    return selected


_DEPTH_ORDER = {
    InitializationDepth.QUICK: 1,
    InitializationDepth.BALANCED: 2,
    InitializationDepth.FULL: 3,
}


def _reusable_arc_outputs(
    database: Database,
    book_id: str,
    edition_id: str,
    prior_initialization_id: str | None,
    source_manifest_sha256: str,
    effective_content_sha256: str,
    arcs: list[ArcRecord],
) -> dict[str, tuple[str, dict[str, Any], set[str]]]:
    if not prior_initialization_id:
        return {}
    prior = latest_initialization(
        database,
        book_id,
        edition_id,
        initialization_id=prior_initialization_id,
    )
    if prior is None:
        return {}
    prior_manifest = InitializationManifest.model_validate(prior["manifest"])
    if (
        prior_manifest.source_manifest_sha256 != source_manifest_sha256
        or prior_manifest.effective_content_sha256 != effective_content_sha256
    ):
        raise InitializationError("初始化升级不能复用已漂移的 Source 或 Edition")
    prior_root = Path(str(prior["root"]))
    prior_arcs = ArcManifest.model_validate(_read_json(prior_root / "arc_manifest.json"))
    by_chapters = {tuple(item.chapter_ids): item for item in prior_arcs.arcs}
    reusable: dict[str, tuple[str, dict[str, Any], set[str]]] = {}
    for arc in arcs:
        previous = by_chapters.get(tuple(arc.chapter_ids))
        if previous is None:
            continue
        output_path = arc_output_path(
            prior_root,
            prior_arcs.initialization_id,
            book_id,
            edition_id,
            previous.arc_id,
        )
        if not output_path.is_file():
            continue
        try:
            output = ArcExtractionOutput.model_validate(_read_json(output_path))
        except (OSError, json.JSONDecodeError, ValueError):
            continue
        literary_analyzed = {
            str(item.get("chapter_id"))
            for item in output.chapter_semantic_features
            if item.get("chapter_id")
            and str(item.get("analysis_status", "PENDING")).upper()
            not in {"PENDING", "UNKNOWN", "NOT_ANALYZED"}
        }
        continuity_analyzed = {
            str(item.get("chapter_id"))
            for item in output.chapter_continuity_deltas
            if item.get("chapter_id")
            and str(item.get("status") or item.get("analysis_status") or "").upper()
            in {"COMPLETE", "COMPLETE_NO_CHANGE", "UNKNOWN"}
        }
        required = set(arc.semantic_chapter_ids) | set(arc.continuity_chapter_ids)
        reused_ids = {
            chapter_id
            for chapter_id in required
            if (chapter_id not in arc.semantic_chapter_ids or chapter_id in literary_analyzed)
            and (chapter_id not in arc.continuity_chapter_ids or chapter_id in continuity_analyzed)
        }
        if not reused_ids:
            continue
        payload = output.model_dump(mode="json")
        reusable[arc.arc_id] = (previous.arc_id, payload, reused_ids)
    return reusable


def _completed_chapter_layers(
    database: Database,
    book_id: str,
    edition_id: str,
) -> dict[str, set[str]]:
    completed: dict[str, set[str]] = {
        "CONTINUITY": set(),
        "LITERARY": set(),
        "BOUNDARY": set(),
    }
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT r.chapter_id, r.analysis_layer, r.source_revision, c.version "
            "FROM chapter_analysis_records r JOIN chapters c ON c.chapter_id=r.chapter_id "
            "WHERE r.book_id=? AND r.edition_id=? "
            "AND r.status IN ('COMPLETE','COMPLETE_NO_CHANGE','UNKNOWN')",
            (book_id, edition_id),
        ).fetchall()
    for row in rows:
        layer = str(row["analysis_layer"])
        if layer not in completed:
            continue
        if str(row["source_revision"]) != f"chapter-v{int(row['version'])}":
            continue
        completed[layer].add(str(row["chapter_id"]))
    return completed


def create_initialization(
    database: Database,
    book_id: str,
    *,
    edition_id: str | None = None,
    char_limit: int = 80_000,
    max_chapters_per_arc: int = 20,
    depth: InitializationDepth = InitializationDepth.FULL,
    upgrade_from_initialization_id: str | None = None,
    additional_deep_chapter_ids: set[str] | None = None,
    requested_action: str | None = None,
) -> dict[str, Any]:
    """Create a frozen, source-complete initialization task package.

    This function only maps and packages source material. It deliberately does
    not claim semantic completion and does not create Canon events.
    """
    if char_limit < 1 or max_chapters_per_arc < 1 or max_chapters_per_arc > 20:
        raise InitializationError("Arc 限制无效：章节数必须 1—20，字符上限必须为正数")
    depth = InitializationDepth(depth)
    database.initialize()
    selected = resolve_edition_id(database, book_id, edition_id)
    chapters = _chapter_rows(database, book_id, selected)
    if not chapters:
        raise InitializationError("当前 edition 没有有效章节，无法初始化")
    source_diagnostic = calculate_source_coverage(database, book_id, selected)
    if source_diagnostic["status"] == "BLOCKED":
        raise InitializationError(
            "Source Coverage 阻断：" + "; ".join(source_diagnostic["anomalies"])
        )
    source_hash = _source_manifest_hash(database, book_id)
    effective_hash = hashlib.sha256(
        "".join(str(item.get("content_sha256") or "") for item in chapters).encode("utf-8")
    ).hexdigest()
    initialization_id = stable_id(
        "novel-initialization", book_id, selected, source_hash, effective_hash, utc_now()
    )
    root = initialization_root(database, book_id, selected, initialization_id)
    root.mkdir(parents=True, exist_ok=False)
    for name in (
        "entity_resolution",
        "synthesis",
        "metrics",
        "visuals",
        "reports",
    ):
        (root / name).mkdir()
    arcs = _propose_arcs(
        book_id,
        selected,
        initialization_id,
        chapters,
        char_limit=char_limit,
        max_chapters=max_chapters_per_arc,
    )
    arc_by_chapter = {chapter_id: arc for arc in arcs for chapter_id in arc.chapter_ids}
    structural_records = [
        _chapter_structure_record(row, arc_by_chapter[str(row["chapter_id"])].arc_id)
        for row in chapters
    ]
    first_seen_terms: set[str] = set()
    for record in structural_records:
        for hint in record["recall_hints"]:
            term = str(hint["term"])
            hint["first_occurrence"] = term not in first_seen_terms
            first_seen_terms.add(term)
    deep_chapter_ids, selection_reasons = _select_deep_chapters(
        depth, chapters, arcs, structural_records
    )
    literary_chapter_ids = _select_literary_chapters(
        depth, chapters, arcs, structural_records
    )
    if depth is InitializationDepth.QUICK:
        literary_chapter_ids = set(deep_chapter_ids)
    known_chapter_ids = {str(row["chapter_id"]) for row in chapters}
    requested_ids = set(additional_deep_chapter_ids or set())
    unknown_requested = requested_ids - known_chapter_ids
    if unknown_requested:
        raise InitializationError("补齐范围包含未知章节：" + ", ".join(sorted(unknown_requested)))
    for chapter_id in requested_ids:
        selection_reasons.setdefault(chapter_id, []).append(
            requested_action or "AUTHOR_SELECTED_DEEPENING"
        )
    deep_chapter_ids.update(requested_ids)
    literary_chapter_ids.update(requested_ids)
    arcs = [
        arc.model_copy(
            update={
                "semantic_chapter_ids": [
                    chapter_id
                    for chapter_id in arc.chapter_ids
                    if chapter_id in literary_chapter_ids
                ],
                "continuity_chapter_ids": (
                    list(arc.chapter_ids)
                    if depth is InitializationDepth.FULL
                    else [
                        chapter_id
                        for chapter_id in arc.chapter_ids
                        if chapter_id in deep_chapter_ids
                    ]
                ),
            }
        )
        for arc in arcs
    ]
    arc_by_chapter = {chapter_id: arc for arc in arcs for chapter_id in arc.chapter_ids}
    reusable_outputs = _reusable_arc_outputs(
        database,
        book_id,
        selected,
        upgrade_from_initialization_id,
        source_hash,
        effective_hash,
        arcs,
    )
    completed_layers = _completed_chapter_layers(database, book_id, selected)
    coverage_items: list[ChapterCoverage] = []
    for row in chapters:
        arc = arc_by_chapter[str(row["chapter_id"])]
        coverage_items.append(
            ChapterCoverage(
                ordinal=int(row["ordinal"]),
                raw_heading=str(row.get("raw_heading") or ""),
                logical_heading=str(row.get("title") or row.get("raw_heading") or ""),
                chapter_id=str(row["chapter_id"]),
                source_span_ids=([str(row["source_span_id"])] if row.get("source_span_id") else []),
                content_sha256=str(row.get("content_sha256") or ""),
                char_count=len(str(row.get("content") or "")),
                inferred_volume=_infer_volume(row),
                assigned_arc_id=arc.arc_id,
                analysis_status=(
                    "PENDING"
                    if str(row["chapter_id"])
                    in set(arc.continuity_chapter_ids) | set(arc.semantic_chapter_ids)
                    else "UNKNOWN"
                ),
            )
        )
    coverage = SourceCoverage(
        book_id=book_id,
        edition_id=selected,
        source_manifest_sha256=source_hash,
        effective_chapter_count=len(chapters),
        covered_chapter_count=len(coverage_items),
        chapter_coverage=1.0,
        chapters=coverage_items,
        diagnostics=source_diagnostic,
    )
    manifest = InitializationManifest(
        initialization_id=initialization_id,
        book_id=book_id,
        edition_id=selected,
        source_manifest_sha256=source_hash,
        effective_content_sha256=effective_hash,
        created_at=utc_now(),
        pipeline=[
            "Source Coverage",
            "Arc Segmentation",
            "Arc Extraction",
            "Entity Resolution",
            "Cross-Arc Synthesis",
            "Contradiction Audit",
            "Narrative DNA",
            "Current Story Atlas",
            "Future Possibility Space",
            "Semantic Metric Bootstrap",
            "Visual Asset Rendering",
        ],
        state=InitializationState.SOURCE_MAPPED,
        source_coverage_path="source_coverage.json",
        arc_manifest_path="arc_manifest.json",
        contract_hashes={},
        chapter_count=len(chapters),
        arc_count=len(arcs),
        current_core_requirements=[
            "protagonist state",
            "current world rules",
            "current ability boundaries",
            "active main thread",
            "continuation boundary",
        ],
        initialization_depth=depth,
        analysis_plan={
            "strategy": depth.value,
            "layers": [
                "SOURCE_STRUCTURE",
                "CONTINUITY_INDEX",
                "LITERARY_PROFILE",
                "CURRENT_BOUNDARY_DEEP",
            ],
            "selection_reasons": selection_reasons,
            "continuity_index_chapter_ids": [
                chapter_id for arc in arcs for chapter_id in arc.continuity_chapter_ids
            ],
            "literary_profile_chapter_ids": [
                chapter_id for arc in arcs for chapter_id in arc.semantic_chapter_ids
            ],
            "semantic_outputs_are_provisional_until_validated": True,
            "unselected_chapters_remain_unknown": True,
        },
        deep_chapter_ids=[
            str(row["chapter_id"])
            for row in chapters
            if str(row["chapter_id"]) in literary_chapter_ids
        ],
        lightweight_chapter_ids=[str(row["chapter_id"]) for row in chapters],
        uncovered_semantic_chapter_ids=[
            str(row["chapter_id"])
            for row in chapters
            if str(row["chapter_id"]) not in literary_chapter_ids
        ],
        current_boundary_window=[
            str(row["chapter_id"])
            for row in chapters[-(5 if depth is InitializationDepth.QUICK else 10) :]
        ],
        capabilities={
            "browse_structure": True,
            "view_partial_profile": False,
            "plan_next": False,
            "continue_from_current_boundary": False,
            "rewrite_selected_chapter": False,
            "inspect_global_world_state": False,
        },
        upgrade_from_initialization_id=upgrade_from_initialization_id,
        requested_action=requested_action,
    )
    _write_json(root / "source_coverage.json", coverage.model_dump(mode="json"))
    _write_json(
        root / "structural_index.json",
        {
            "schema_version": "structural-index-v1",
            "book_id": book_id,
            "edition_id": selected,
            "initialization_id": initialization_id,
            "source_coverage": 1.0,
            "semantic_authority": "RECALL_HINT_ONLY",
            "chapters": structural_records,
        },
    )
    arc_manifest = ArcManifest(
        initialization_id=initialization_id,
        book_id=book_id,
        edition_id=selected,
        arcs=arcs,
        max_chapters_per_arc=max_chapters_per_arc,
        char_limit=char_limit,
    )
    schema_path = root / "arc_schema.json"
    _write_json(schema_path, _arc_schema())
    (root / "events.jsonl").write_text("", encoding="utf-8")
    prepared_arcs: list[ArcRecord] = []
    reused_arc_ids: list[str] = []
    scheduled_arc_ids: list[str] = []
    current_boundary_ids = set(manifest.current_boundary_window)

    def execution_priority(arc: ArcRecord) -> tuple[int, int]:
        chapter_ids = set(arc.chapter_ids)
        if chapter_ids & current_boundary_ids:
            return (0, -arc.ordinal)
        arc_reasons = {
            reason
            for chapter_id in chapter_ids
            for reason in selection_reasons.get(chapter_id, [])
        }
        if "CURRENT_ARC" in arc_reasons:
            return (1, -arc.ordinal)
        if "ACTIVE_DEPENDENCY_RECALL" in arc_reasons:
            return (2, -arc.ordinal)
        if chapter_ids & requested_ids:
            return (3, -arc.ordinal)
        if arc.ordinal == 1:
            return (4, arc.ordinal)
        if arc.semantic_chapter_ids:
            return (5, -arc.ordinal)
        return (6, -arc.ordinal)

    execution_arcs = sorted(arcs, key=execution_priority)
    for execution_index, arc in enumerate(execution_arcs, start=1):
        required_chapter_ids = set(arc.continuity_chapter_ids) | set(arc.semantic_chapter_ids)
        if not required_chapter_ids:
            prepared_arcs.append(arc)
            continue
        reusable = reusable_outputs.get(arc.arc_id)
        reused_output_path: Path | None = None
        previous_arc_id: str | None = None
        reused_ids: set[str] = set()
        if reusable is not None:
            previous_arc_id, payload, reused_ids = reusable
            payload["initialization_id"] = initialization_id
            payload["arc_id"] = arc.arc_id
        reused_continuity = (set(arc.continuity_chapter_ids) & completed_layers["CONTINUITY"]) | (
            reused_ids & set(arc.continuity_chapter_ids)
        )
        reused_literary = (set(arc.semantic_chapter_ids) & completed_layers["LITERARY"]) | (
            reused_ids & set(arc.semantic_chapter_ids)
        )
        scheduled_continuity = set(arc.continuity_chapter_ids) - reused_continuity
        scheduled_literary = set(arc.semantic_chapter_ids) - reused_literary
        task_chapter_ids = [
            chapter_id
            for chapter_id in arc.chapter_ids
            if chapter_id in scheduled_continuity | scheduled_literary
        ]
        if not task_chapter_ids:
            output_path = arc_output_path(
                root,
                initialization_id,
                book_id,
                selected,
                arc.arc_id,
            )
            reused_payload = (
                payload
                if reusable is not None
                else ArcExtractionOutput(
                    initialization_id=initialization_id,
                    arc_id=arc.arc_id,
                ).model_dump(mode="json")
            )
            _write_json(output_path, reused_payload)
            prepared_arcs.append(
                arc.model_copy(
                    update={
                        "status": "REUSED",
                        "reused_from_arc_id": previous_arc_id,
                        "reused_semantic_chapter_ids": sorted(reused_literary),
                        "reused_continuity_chapter_ids": sorted(reused_continuity),
                        "scheduled_semantic_chapter_ids": [],
                        "scheduled_continuity_chapter_ids": [],
                    }
                )
            )
            reused_arc_ids.append(arc.arc_id)
            continue
        if reusable is not None:
            reused_output_path = root / "reused_arc_outputs" / f"{arc.arc_id}.json"
            _write_json(reused_output_path, payload)
        operation_id = _arc_operation_id(initialization_id, arc.arc_id)
        operation = ensure_operation(
            database,
            book_id,
            selected,
            operation_id,
            "INITIALIZATION_ARC",
            {
                "initialization_id": initialization_id,
                "arc_id": arc.arc_id,
                "initialization_depth": depth.value,
                "chapter_ids": task_chapter_ids,
                "execution_priority": execution_index,
            },
        )
        arc_task = operation.input if operation is not None else root / "arc_tasks" / arc.arc_id
        (arc_task / "chapters").mkdir(parents=True)
        arc_chapters = [row for row in chapters if str(row["chapter_id"]) in set(task_chapter_ids)]
        chapter_lines: list[str] = []
        for row in arc_chapters:
            # Keep filenames short: Windows workspaces can already be deeply
            # nested, and the stable chapter id is preserved in the manifest.
            chapter_path = arc_task / "chapters" / f"chapter-{int(row['ordinal']):04d}.md"
            chapter_text = f"# {row.get('raw_heading') or row.get('title') or row['ordinal']}\n\n{row.get('content') or ''}\n"
            chapter_path.write_text(chapter_text, encoding="utf-8")
            chapter_lines.append(
                f"- 第 {row['ordinal']} 章 · `{row['chapter_id']}` · `{chapter_path.name}`"
            )
        _write_json(
            arc_task / "source_manifest.json",
            {
                "initialization_id": initialization_id,
                "arc_id": arc.arc_id,
                "chapter_ids": task_chapter_ids,
                "arc_all_chapter_ids": arc.chapter_ids,
                "arc_required_semantic_chapter_ids": arc.semantic_chapter_ids,
                "arc_required_continuity_chapter_ids": arc.continuity_chapter_ids,
                "scheduled_semantic_chapter_ids": sorted(scheduled_literary),
                "scheduled_continuity_chapter_ids": sorted(scheduled_continuity),
                "reused_semantic_chapter_ids": sorted(reused_literary),
                "reused_continuity_chapter_ids": sorted(reused_continuity),
                "source_span_ids": [
                    str(row["source_span_id"]) for row in arc_chapters if row.get("source_span_id")
                ],
                "initialization_depth": depth.value,
                "execution_priority": execution_index,
                "content_hashes": [str(row.get("content_sha256") or "") for row in arc_chapters],
            },
        )
        _write_json(arc_task / "output_schema.json", _arc_schema())
        _write_json(
            arc_task / "status.json",
            {
                "initialization_id": initialization_id,
                "arc_id": arc.arc_id,
                "state": "PENDING",
                "updated_at": utc_now(),
                "source_frozen": True,
            },
        )
        input_text = (
            "$initialize-existing-novel\n\n"
            f"初始化 {initialization_id} 的 Arc {arc.arc_id}。\n"
            "请只读取本目录 chapters/ 和 source_manifest.json，按 output_schema.json 输出 output.json。\n"
            "CANON 必须有真实 source_span_ids；INFERENCE 必须有 reasoning_summary、confidence、counter_evidence 和 unknown_boundary。\n"
            "CONTINUITY_INDEX 必须逐章输出 chapter_continuity_deltas；不得用整批摘要代替。"
            "每章只能是 COMPLETE、COMPLETE_NO_CHANGE 或 UNKNOWN，确认变化必须带 source_span_ids。\n"
            f"文学深分析只处理这些章节：{', '.join(sorted(scheduled_literary)) or '无'}。\n"
            "不得修改 book、Canon、正史或远端；未知保持 unknown，不要为了完整而猜测。\n\n"
            "本 Arc 章节：\n" + "\n".join(chapter_lines) + "\n"
        )
        (arc_task / "input.md").write_text(input_text, encoding="utf-8")
        prepared_arcs.append(
            arc.model_copy(
                update={
                    "operation_id": operation_id,
                    "operation_input_path": str(arc_task),
                    "reused_from_arc_id": previous_arc_id,
                    "reused_semantic_chapter_ids": sorted(reused_literary),
                    "reused_continuity_chapter_ids": sorted(reused_continuity),
                    "scheduled_semantic_chapter_ids": sorted(scheduled_literary),
                    "scheduled_continuity_chapter_ids": sorted(scheduled_continuity),
                    "reused_output_path": (str(reused_output_path) if reused_output_path else None),
                }
            )
        )
        scheduled_arc_ids.append(arc.arc_id)
    prepared_arcs.sort(key=lambda item: item.ordinal)
    arc_manifest = arc_manifest.model_copy(update={"arcs": prepared_arcs})
    _write_json(root / "arc_manifest.json", arc_manifest.model_dump(mode="json"))
    manifest.reused_arc_ids = reused_arc_ids
    manifest.scheduled_arc_ids = scheduled_arc_ids
    manifest.contract_hashes = {
        "arc_schema.json": sha256_file(schema_path),
        "source_coverage.json": sha256_file(root / "source_coverage.json"),
        "arc_manifest.json": sha256_file(root / "arc_manifest.json"),
    }
    _write_json(root / "initialization_manifest.json", manifest.model_dump(mode="json"))
    _write_json(
        root / "status.json",
        {
            "initialization_id": initialization_id,
            "state": InitializationState.SOURCE_MAPPED.value,
            "readiness": "BLOCKED",
            "source_coverage": coverage.chapter_coverage,
            "chapter_coverage": 0.0,
            "updated_at": utc_now(),
            "completed_arc_ids": reused_arc_ids,
            "pending_arc_ids": scheduled_arc_ids,
            "failed_arc_ids": [],
            "warnings": ["语义 Arc 输出尚未由 Codex 桌面端完成"],
            "initialization_depth": depth.value,
            "structural_index_status": "COMPLETE",
            "semantic_status": "PENDING",
            "progress": {
                "reused_arc_count": len(reused_arc_ids),
                "reused_chapter_count": sum(
                    len(arc.reused_semantic_chapter_ids) for arc in prepared_arcs
                ),
                "scheduled_arc_count": len(scheduled_arc_ids),
                "remaining_arc_count": len(scheduled_arc_ids),
                "observed_seconds_per_arc": None,
                "estimated_remaining_seconds": None,
            },
        },
    )
    _event(root, "SOURCE_MAPPED", {"chapter_count": len(chapters), "arc_count": len(arcs)})
    return {
        "initialization_id": initialization_id,
        "book_id": book_id,
        "edition_id": selected,
        "root": str(root),
        "state": InitializationState.SOURCE_MAPPED.value,
        "chapter_count": len(chapters),
        "arc_count": len(arcs),
        "chapter_coverage": 1.0,
        "source_coverage": 1.0,
        "arc_ids": [arc.arc_id for arc in arcs],
        "source_manifest_sha256": source_hash,
        "initialization_depth": depth.value,
        "deep_chapter_count": len(literary_chapter_ids),
        "lightweight_chapter_count": len(chapters),
        "uncovered_semantic_chapter_count": len(chapters) - len(literary_chapter_ids),
        "upgrade_from_initialization_id": upgrade_from_initialization_id,
        "reused_arc_count": len(reused_arc_ids),
        "scheduled_arc_count": len(scheduled_arc_ids),
        "requested_action": requested_action,
    }


def _latest_directory(root: Path) -> Path | None:
    if not root.is_dir():
        return None
    candidates = [
        path
        for path in root.iterdir()
        if path.is_dir() and (path / "initialization_manifest.json").is_file()
    ]
    return (
        sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]
        if candidates
        else None
    )


def latest_initialization(
    database: Database,
    book_id: str,
    edition_id: str | None = None,
    initialization_id: str | None = None,
) -> dict[str, Any] | None:
    root = initialization_root(database, book_id, edition_id)
    selected = (
        initialization_root(database, book_id, edition_id, initialization_id)
        if initialization_id
        else _latest_directory(root)
    )
    if selected is None:
        return None
    try:
        manifest = _read_json(selected / "initialization_manifest.json")
        status = _read_json(selected / "status.json")
    except (OSError, json.JSONDecodeError) as exc:
        raise InitializationError(f"初始化状态文件无法读取：{selected}") from exc
    return {"root": str(selected), "manifest": manifest, "status": status}


def _validate_arc_output_evidence(
    database: Database,
    book_id: str,
    arc: ArcRecord,
    output: ArcExtractionOutput,
) -> None:
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT span_id FROM source_spans WHERE book_id=? AND chapter_id IN ({})".format(
                ",".join("?" for _ in arc.chapter_ids)
            ),
            (book_id, *arc.chapter_ids),
        ).fetchall()
    valid = {str(row["span_id"]) for row in rows}
    for field_name in type(output).model_fields:
        value = getattr(output, field_name)
        if not isinstance(value, list):
            continue
        for item in value:
            if not isinstance(item, dict):
                continue
            status = str(item.get("information_status") or "").upper()
            if status not in {"CANON", "INFERENCE"}:
                continue
            spans = {str(span_id) for span_id in (item.get("source_span_ids") or [])}
            invalid = spans - valid
            if invalid:
                raise ValueError(
                    f"Arc {arc.arc_id} 引用了不属于该 Book/Arc 的 source span: "
                    + ", ".join(sorted(invalid))
                )
    continuity_by_chapter = {
        str(item.get("chapter_id")): item
        for item in output.chapter_continuity_deltas
        if item.get("chapter_id")
    }
    missing_continuity = set(arc.scheduled_continuity_chapter_ids) - set(continuity_by_chapter)
    if missing_continuity:
        raise ValueError(
            f"Arc {arc.arc_id} 缺少逐章 ChapterContinuityDelta: "
            + ", ".join(sorted(missing_continuity))
        )
    change_fields = (
        "characters_present",
        "character_state_changes",
        "location_changes",
        "items_acquired",
        "items_lost",
        "items_transferred",
        "ability_changes",
        "relationship_changes",
        "knowledge_changes",
        "world_rule_changes",
        "rule_exceptions",
        "thread_advances",
        "promises_created",
        "promises_paid",
        "hooks_created",
        "hooks_advanced",
        "faction_changes",
    )
    for chapter_id in arc.scheduled_continuity_chapter_ids:
        delta = continuity_by_chapter[chapter_id]
        status = str(delta.get("status") or delta.get("analysis_status") or "").upper()
        if status not in {"COMPLETE", "COMPLETE_NO_CHANGE", "UNKNOWN"}:
            raise ValueError(f"章节 {chapter_id} 的 Continuity 状态无效：{status}")
        changes = [
            item
            for field_name in change_fields
            for item in (delta.get(field_name) or [])
            if isinstance(item, dict)
        ]
        if status == "COMPLETE" and not changes:
            raise ValueError(f"章节 {chapter_id} 标记 COMPLETE 但没有逐项变化")
        if status == "COMPLETE_NO_CHANGE" and changes:
            raise ValueError(f"章节 {chapter_id} 标记无变化但仍包含确认变化")
        for item in changes:
            if not item.get("source_span_ids"):
                raise ValueError(f"章节 {chapter_id} 的确认变化缺少 source_span_ids")
    literary_ids = {
        str(item.get("chapter_id"))
        for item in output.chapter_semantic_features
        if item.get("chapter_id")
    }
    missing_literary = set(arc.scheduled_semantic_chapter_ids) - literary_ids
    if missing_literary:
        raise ValueError(
            f"Arc {arc.arc_id} 缺少代表章节文学分析: " + ", ".join(sorted(missing_literary))
        )


def _sync_chapter_analysis_records(
    database: Database,
    root: Path,
    arc_manifest: ArcManifest,
    outputs: list[ArcExtractionOutput],
) -> None:
    now = utc_now()
    output_by_arc = {item.arc_id: item for item in outputs}
    with database.connect() as connection:
        chapter_rows = connection.execute(
            "SELECT chapter_id, ordinal, version FROM chapters WHERE book_id=?",
            (arc_manifest.book_id,),
        ).fetchall()
        chapter_meta = {
            str(row["chapter_id"]): (int(row["ordinal"]), f"chapter-v{int(row['version'])}")
            for row in chapter_rows
        }
        max_ordinal = max((item[0] for item in chapter_meta.values()), default=0)

        def upsert(
            chapter_id: str,
            layer: str,
            status: str,
            payload: dict[str, Any],
            result_path: str,
        ) -> None:
            metadata = chapter_meta.get(chapter_id)
            if metadata is None:
                return
            ordinal, source_revision = metadata
            record_id = (
                f"chapter-analysis:{arc_manifest.book_id}:{arc_manifest.edition_id}:"
                f"{chapter_id}:{layer}:{source_revision}"
            )
            connection.execute(
                "INSERT INTO chapter_analysis_records("
                "record_id, book_id, edition_id, chapter_id, analysis_layer, status, "
                "source_revision, result_path, result_json, created_at, updated_at, version"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1) "
                "ON CONFLICT(book_id, edition_id, chapter_id, analysis_layer, source_revision) "
                "DO UPDATE SET status=excluded.status, result_path=excluded.result_path, "
                "result_json=excluded.result_json, updated_at=excluded.updated_at, "
                "version=chapter_analysis_records.version+1",
                (
                    record_id,
                    arc_manifest.book_id,
                    arc_manifest.edition_id,
                    chapter_id,
                    layer,
                    status,
                    source_revision,
                    result_path,
                    json_dumps(payload),
                    now,
                    now,
                ),
            )
            if layer == "CONTINUITY" and ordinal > max_ordinal - 20:
                upsert(chapter_id, "BOUNDARY", status, payload, result_path)

        for arc in arc_manifest.arcs:
            output = output_by_arc.get(arc.arc_id)
            if output is None:
                continue
            result_path = str(
                arc_output_path(
                    root,
                    arc_manifest.initialization_id,
                    arc_manifest.book_id,
                    arc_manifest.edition_id,
                    arc.arc_id,
                )
            )
            for delta in output.chapter_continuity_deltas:
                chapter_id = str(delta.get("chapter_id") or "")
                if chapter_id:
                    status = str(
                        delta.get("status") or delta.get("analysis_status") or "UNKNOWN"
                    ).upper()
                    upsert(chapter_id, "CONTINUITY", status, delta, result_path)
            for feature in output.chapter_semantic_features:
                chapter_id = str(feature.get("chapter_id") or "")
                if chapter_id:
                    status = str(feature.get("analysis_status") or "COMPLETE").upper()
                    upsert(chapter_id, "LITERARY", status, feature, result_path)


def _arc_outputs(
    database: Database,
    root: Path,
    arc_manifest: ArcManifest,
) -> tuple[list[ArcExtractionOutput], list[str], list[str]]:
    completed: list[ArcExtractionOutput] = []
    failed: list[str] = []
    pending: list[str] = []
    for arc in arc_manifest.arcs:
        path = arc_output_path(
            root,
            arc_manifest.initialization_id,
            arc_manifest.book_id,
            arc_manifest.edition_id,
            arc.arc_id,
        )
        if not path.is_file():
            pending.append(arc.arc_id)
            continue
        try:
            value = ArcExtractionOutput.model_validate(_read_json(path))
            if (
                value.initialization_id != arc_manifest.initialization_id
                or value.arc_id != arc.arc_id
            ):
                raise ValueError("initialization_id/arc_id 不匹配")
            if arc.reused_output_path:
                reused_path = Path(arc.reused_output_path)
                reused = ArcExtractionOutput.model_validate(_read_json(reused_path))
                updates: dict[str, Any] = {}
                for field_name in type(value).model_fields:
                    current_items = getattr(value, field_name)
                    reused_items = getattr(reused, field_name)
                    if not isinstance(current_items, list) or not isinstance(reused_items, list):
                        continue
                    combined: list[Any] = []
                    seen: set[str] = set()
                    for item in [*reused_items, *current_items]:
                        key = json.dumps(item, ensure_ascii=False, sort_keys=True)
                        if key in seen:
                            continue
                        seen.add(key)
                        combined.append(item)
                    updates[field_name] = combined
                value = value.model_copy(update=updates)
            _validate_arc_output_evidence(
                database,
                arc_manifest.book_id,
                arc,
                value,
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failed.append(arc.arc_id)
            _write_json(
                path.parent / "validation_error.json",
                {"arc_id": arc.arc_id, "error": str(exc), "updated_at": utc_now()},
            )
            continue
        completed.append(value)
    return completed, pending, failed


def _analyzed_chapter_ids(outputs: list[ArcExtractionOutput]) -> set[str]:
    return {
        str(item["chapter_id"])
        for output in outputs
        for item in output.chapter_semantic_features
        if item.get("chapter_id")
        and str(item.get("analysis_status", "PENDING")).upper()
        not in {"PENDING", "UNKNOWN", "NOT_ANALYZED"}
    }


def _continuity_chapter_ids(outputs: list[ArcExtractionOutput]) -> set[str]:
    return {
        str(item["chapter_id"])
        for output in outputs
        for item in output.chapter_continuity_deltas
        if item.get("chapter_id")
        and str(item.get("status") or item.get("analysis_status") or "").upper()
        in {"COMPLETE", "COMPLETE_NO_CHANGE", "UNKNOWN"}
    }


def upgrade_initialization(
    database: Database,
    book_id: str,
    *,
    edition_id: str | None = None,
    depth: InitializationDepth,
    requested_action: str | None = None,
) -> dict[str, Any]:
    selected = resolve_edition_id(database, book_id, edition_id)
    current = latest_initialization(database, book_id, selected)
    if current is None:
        return create_initialization(
            database,
            book_id,
            edition_id=selected,
            depth=depth,
            requested_action=requested_action,
        )
    manifest = InitializationManifest.model_validate(current["manifest"])
    target = InitializationDepth(depth)
    if _DEPTH_ORDER[target] <= _DEPTH_ORDER[manifest.initialization_depth]:
        return {
            **current,
            "upgrade_status": "NO_CHANGE",
            "initialization_depth": manifest.initialization_depth.value,
        }
    root = Path(str(current["root"]))
    arc_manifest = ArcManifest.model_validate(_read_json(root / "arc_manifest.json"))
    _, pending, failed = _arc_outputs(database, root, arc_manifest)
    if pending or failed:
        return {
            **current,
            "upgrade_status": "RESUME_REQUIRED",
            "pending_arc_ids": pending,
            "failed_arc_ids": failed,
            "initialization_depth": manifest.initialization_depth.value,
        }
    return {
        **create_initialization(
            database,
            book_id,
            edition_id=selected,
            depth=target,
            upgrade_from_initialization_id=manifest.initialization_id,
            requested_action=requested_action,
        ),
        "upgrade_status": "UPGRADE_CREATED",
    }


def prepare_action_deepening(
    database: Database,
    book_id: str,
    *,
    edition_id: str | None = None,
    action: str,
    target_chapter_id: str | None = None,
    batch_limit: int = 12,
) -> dict[str, Any]:
    """Rank and schedule one bounded batch of action-relevant history."""

    if batch_limit < 1 or batch_limit > 30:
        raise InitializationError("定向补齐每批章节数必须为 1—30")
    selected = resolve_edition_id(database, book_id, edition_id)
    current = latest_initialization(database, book_id, selected)
    if current is None:
        raise InitializationError("尚未建立结构索引，不能准备按操作补齐")
    root = Path(str(current["root"]))
    manifest = InitializationManifest.model_validate(current["manifest"])
    arc_manifest = ArcManifest.model_validate(_read_json(root / "arc_manifest.json"))
    structural = _read_json(root / manifest.structural_index_path)
    chapters = list(structural.get("chapters") or [])
    by_id = {str(item["chapter_id"]): item for item in chapters}
    normalized_action = action.strip().upper()
    if normalized_action not in {"CONTINUE", "REWRITE"}:
        raise InitializationError("action 必须是 CONTINUE 或 REWRITE")

    scores: dict[str, float] = defaultdict(float)
    reasons: dict[str, set[str]] = defaultdict(set)

    def add(chapter_id: str, score: float, reason: str) -> None:
        if chapter_id in by_id:
            scores[chapter_id] += score
            reasons[chapter_id].add(reason)

    if normalized_action == "CONTINUE":
        focus_ids = list(manifest.current_boundary_window)
        for chapter_id in focus_ids:
            add(chapter_id, 120, "CURRENT_BOUNDARY")
        target_arc = arc_manifest.arcs[-1] if arc_manifest.arcs else None
        if target_arc is not None:
            for chapter_id in target_arc.chapter_ids:
                add(chapter_id, 65, "CURRENT_ARC")
        focus_rows = chapters[-5:]
    else:
        if target_chapter_id is None or target_chapter_id not in by_id:
            raise InitializationError("改写补齐需要有效 target_chapter_id")
        target = by_id[target_chapter_id]
        ordinal = int(target["ordinal"])
        focus_ids = [
            str(item["chapter_id"]) for item in chapters if abs(int(item["ordinal"]) - ordinal) <= 1
        ]
        for chapter_id in focus_ids:
            add(chapter_id, 140, "REVISION_RANGE")
        target_arc = next(arc for arc in arc_manifest.arcs if target_chapter_id in arc.chapter_ids)
        for chapter_id in target_arc.chapter_ids:
            add(chapter_id, 55, "TARGET_ARC")
        focus_rows = [target]

    focus_terms = {
        str(hint["term"])
        for item in focus_rows
        for hint in item.get("recall_hints") or []
        if hint.get("term")
    }
    latest_term_chapter: dict[str, str] = {}
    for item in chapters:
        chapter_id = str(item["chapter_id"])
        overlap = {
            str(hint["term"])
            for hint in item.get("recall_hints") or []
            if str(hint.get("term") or "") in focus_terms
        }
        if overlap:
            add(chapter_id, min(36, len(overlap) * 12), "DIRECT_ENTITY_OR_THREAD_MATCH")
            for term in overlap:
                latest_term_chapter[term] = chapter_id
        change_markers = int(item.get("change_marker_count") or 0)
        if change_markers:
            add(chapter_id, min(20, change_markers * 4), "STATE_CHANGE_SIGNAL")
    for chapter_id in latest_term_chapter.values():
        add(chapter_id, 25, "MOST_RECENT_RELEVANT_APPEARANCE")
    max_ordinal = max((int(item["ordinal"]) for item in chapters), default=1)
    for item in chapters:
        recency = int(item["ordinal"]) / max_ordinal
        if str(item["chapter_id"]) in scores:
            add(str(item["chapter_id"]), recency * 15, "CAUSAL_RECENCY")

    completed = _completed_chapter_layers(database, book_id, selected)["LITERARY"]
    ranked = sorted(
        (chapter_id for chapter_id in scores if chapter_id not in completed),
        key=lambda chapter_id: (
            -scores[chapter_id],
            -int(by_id[chapter_id]["ordinal"]),
        ),
    )
    if not ranked:
        return {
            "status": "ACTION_CONTEXT_READY",
            "action": normalized_action,
            "initialization_id": manifest.initialization_id,
            "required_chapter_ids": sorted(scores),
            "selected_chapter_ids": [],
            "missing_chapter_ids": [],
            "relevance": [],
        }
    selected_batch = ranked[:batch_limit]
    relevance = [
        {
            "chapter_id": chapter_id,
            "ordinal": int(by_id[chapter_id]["ordinal"]),
            "score": round(scores[chapter_id], 1),
            "reasons": sorted(reasons[chapter_id]),
        }
        for chapter_id in ranked
    ]
    _, pending, failed = _arc_outputs(database, root, arc_manifest)
    planned = set(manifest.deep_chapter_ids)
    if set(selected_batch) <= planned and (pending or failed):
        return {
            "status": "RESUME_EXISTING_INITIALIZATION",
            "action": normalized_action,
            "initialization_id": manifest.initialization_id,
            "required_chapter_ids": sorted(scores),
            "selected_chapter_ids": selected_batch,
            "missing_chapter_ids": ranked,
            "remaining_candidate_ids": ranked[batch_limit:],
            "pending_arc_ids": pending,
            "failed_arc_ids": failed,
            "batch_limit": batch_limit,
            "relevance": relevance,
        }
    created = create_initialization(
        database,
        book_id,
        edition_id=selected,
        depth=manifest.initialization_depth,
        upgrade_from_initialization_id=manifest.initialization_id,
        additional_deep_chapter_ids=set(selected_batch),
        requested_action=normalized_action,
    )
    return {
        **created,
        "status": "ACTION_DEEPENING_CREATED",
        "action": normalized_action,
        "required_chapter_ids": sorted(scores),
        "selected_chapter_ids": selected_batch,
        "missing_chapter_ids": ranked,
        "remaining_candidate_ids": ranked[batch_limit:],
        "batch_limit": batch_limit,
        "relevance": relevance,
    }


def _write_reports(
    root: Path,
    coverage: SourceCoverage,
    arc_manifest: ArcManifest,
    outputs: list[ArcExtractionOutput],
    readiness: InitializationReadiness,
) -> None:
    (root / "reports" / "source_coverage_report.md").write_text(
        "# Source Coverage Report\n\n"
        f"- Effective chapters: {coverage.effective_chapter_count}\n"
        f"- Source-mapped chapters: {coverage.covered_chapter_count}\n"
        f"- Source mapping coverage: {coverage.chapter_coverage:.1%}\n"
        f"- Arcs: {len(arc_manifest.arcs)}\n"
        "\nEvery effective chapter has exactly one assigned Arc and a source span when the ingest layer provides one.\n",
        encoding="utf-8",
    )
    (root / "reports" / "entity_resolution_report.md").write_text(
        "# Entity Resolution Report\n\n"
        "Entity resolution is conservative: aliases do not auto-merge by string similarity; unresolved candidates remain reviewable.\n",
        encoding="utf-8",
    )
    (root / "reports" / "contradiction_report.md").write_text(
        "# Contradiction Report\n\n"
        f"Arc outputs reviewed: {len(outputs)} / {len(arc_manifest.arcs)}.\n"
        "Cross-Arc contradiction audit is pending until entity resolution and synthesis artifacts exist.\n",
        encoding="utf-8",
    )
    (root / "reports" / "world_model_report.md").write_text(
        "# World Model Report\n\n"
        "This report is evidence-led. It never promotes an inference into Canon and keeps future possibility space separate from current facts.\n",
        encoding="utf-8",
    )
    (root / "reports" / "readiness_report.md").write_text(
        "# Readiness Report\n\n"
        f"- Status: {readiness.status}\n"
        f"- Chapter coverage: {readiness.chapter_coverage:.1%}\n"
        f"- Arc coverage: {readiness.arc_coverage:.1%}\n"
        f"- Source Mapping Coverage: {readiness.source_mapping_coverage:.1%}\n"
        f"- Arc Output Coverage: {readiness.arc_output_coverage:.1%}\n"
        f"- Chapter Semantic Feature Coverage: {readiness.chapter_semantic_feature_coverage:.1%}\n"
        f"- Metric Observation Coverage: {readiness.metric_observation_coverage:.1%}\n"
        f"- Recent Detailed Metric Coverage: {readiness.recent_detailed_metric_coverage:.1%}\n"
        f"- Current Chapter Metric Coverage: {readiness.current_chapter_metric_coverage:.1%}\n"
        f"- Metric Bootstrap Status: {readiness.metric_bootstrap_status}\n"
        f"- Canon evidence coverage: {readiness.canon_evidence_coverage:.1%}\n"
        f"- Entity resolution coverage: {readiness.entity_resolution_coverage:.1%}\n\n"
        "## Blocking reasons\n"
        + "\n".join(f"- {item}" for item in readiness.blocking_reasons)
        + "\n\n## Gaps\n"
        + "\n".join(f"- {item}" for item in readiness.gaps)
        + "\n",
        encoding="utf-8",
    )


def refresh_initialization(
    database: Database,
    book_id: str,
    *,
    edition_id: str | None = None,
    initialization_id: str | None = None,
) -> dict[str, Any]:
    """Recalculate initialization status from immutable coverage and output files."""
    selected = resolve_edition_id(database, book_id, edition_id)
    root = initialization_root(database, book_id, selected, initialization_id)
    if initialization_id is None:
        root = _latest_directory(root) or root
    if not (root / "initialization_manifest.json").is_file():
        raise InitializationError(f"初始化目录不存在：{root}")
    initialization_manifest = InitializationManifest.model_validate(
        _read_json(root / "initialization_manifest.json")
    )
    current_chapters = _chapter_rows(database, book_id, selected)
    current_effective_hash = hashlib.sha256(
        "".join(str(item.get("content_sha256") or "") for item in current_chapters).encode("utf-8")
    ).hexdigest()
    current_source_hash = _source_manifest_hash(database, book_id)
    if (
        initialization_manifest.source_manifest_sha256 != current_source_hash
        or initialization_manifest.effective_content_sha256 != current_effective_hash
    ):
        stale_capabilities = {
            key: False for key in initialization_manifest.capabilities
        }
        stale_status = {
            "initialization_id": initialization_manifest.initialization_id,
            "state": InitializationState.STALE.value,
            "readiness": "BLOCKED",
            "source_coverage": 0.0,
            "chapter_coverage": 0.0,
            "updated_at": utc_now(),
            "blocking_reasons": ["Source 或 effective Edition hash 已漂移，必须重新初始化"],
            "completed_arc_ids": [],
            "failed_arc_ids": [],
            "capabilities": stale_capabilities,
        }
        _write_json(root / "status.json", stale_status)
        _write_json(
            root / "initialization_manifest.json",
            initialization_manifest.model_copy(
                update={
                    "state": InitializationState.STALE,
                    "capabilities": stale_capabilities,
                }
            ).model_dump(mode="json"),
        )
        _event(root, InitializationState.STALE.value, stale_status)
        return {"root": str(root), "status": stale_status, "readiness": stale_status}
    coverage = SourceCoverage.model_validate(_read_json(root / "source_coverage.json"))
    arc_manifest = ArcManifest.model_validate(_read_json(root / "arc_manifest.json"))
    outputs, pending, failed = _arc_outputs(database, root, arc_manifest)
    analyzed_chapter_ids = _analyzed_chapter_ids(outputs)
    continuity_chapter_ids = _continuity_chapter_ids(outputs)
    _sync_chapter_analysis_records(database, root, arc_manifest, outputs)
    completed_layers = _completed_chapter_layers(database, book_id, selected)
    analyzed_chapter_ids.update(completed_layers["LITERARY"])
    continuity_chapter_ids.update(completed_layers["CONTINUITY"])
    evidence_total = 0
    evidence_valid = 0
    for output in outputs:
        for field_name in type(output).model_fields:
            value = getattr(output, field_name)
            if not isinstance(value, list):
                continue
            for item in value:
                if not isinstance(item, dict):
                    continue
                if str(item.get("information_status", "CANON")).upper() == "CANON":
                    evidence_total += 1
                    if item.get("source_span_ids") or item.get("source_evidence"):
                        evidence_valid += 1
    canon_evidence = evidence_valid / evidence_total if evidence_total else 0.0
    entity_file = root / "entity_resolution" / "entity_resolution_map.json"
    entity_result: EntityResolutionResult | None = None
    if entity_file.is_file():
        try:
            entity_result = EntityResolutionResult.model_validate(_read_json(entity_file))
        except (OSError, json.JSONDecodeError, ValueError):
            entity_result = None
    entity_cov = 0.0
    if entity_result and entity_result.identified_major_entities:
        entity_cov = min(
            1.0, entity_result.resolved_major_entities / entity_result.identified_major_entities
        )
    synthesis_file = root / "synthesis" / "current_world_model.md"
    graph_file = root / "synthesis" / "graphs.json"
    core_graphs = synthesis_file.is_file() and graph_file.is_file()
    graph_core = False
    protagonist_confirmed = False
    thread_confirmed = False
    graphs: dict[str, Any] = {}
    continuation_boundary: ContinuationBoundaryReadiness | None = None
    if graph_file.is_file():
        try:
            raw_graphs = _read_json(graph_file)
            if isinstance(raw_graphs, dict):
                graphs = raw_graphs
                required = {
                    "characters",
                    "factions",
                    "abilities",
                    "resources",
                    "regions",
                    "plot_threads",
                }
                graph_core = required.issubset(set(graphs))
                core_graphs = core_graphs and graph_core
        except (OSError, json.JSONDecodeError):
            core_graphs = False
    target_ordinal = max((item.ordinal for item in coverage.chapters), default=0) + 1
    with database.connect() as connection:
        continuation_boundary = evaluate_continuation_boundary(
            connection,
            book_id=book_id,
            edition_id=selected,
            target_chapter_ordinal=target_ordinal,
            graphs=graphs,
        )
    missing_boundary_continuity = sorted(
        set(initialization_manifest.current_boundary_window) - continuity_chapter_ids
    )
    boundary_gaps = list(continuation_boundary.blocking_gaps)
    if coverage.chapter_coverage < 1.0:
        boundary_gaps.append("Source Mapping 尚未完整覆盖当前 Edition")
    if missing_boundary_continuity:
        boundary_gaps.append(
            f"当前 Continuation Boundary 仍有 {len(missing_boundary_continuity)} 章未完成 Continuity"
        )
    if failed:
        boundary_gaps.append("初始化语义输出存在校验失败，当前边界不可放行")
    continuation_boundary = continuation_boundary.model_copy(
        update={
            "blocking_gaps": list(dict.fromkeys(boundary_gaps)),
            "ready_for_continuation": not boundary_gaps,
        }
    )
    protagonist_confirmed = (
        continuation_boundary.current_protagonist.confirmed
        and continuation_boundary.current_protagonist.current_state_available
    )
    thread_confirmed = bool(continuation_boundary.active_main_threads)
    chapter_coverage = (
        len(analyzed_chapter_ids) / coverage.effective_chapter_count
        if coverage.effective_chapter_count
        else 0.0
    )
    arc_coverage = len(outputs) / len(arc_manifest.arcs) if arc_manifest.arcs else 0.0
    source_mapping_coverage = coverage.chapter_coverage
    arc_output_coverage = arc_coverage
    chapter_semantic_feature_coverage = chapter_coverage
    continuity_index_coverage = (
        len(continuity_chapter_ids) / coverage.effective_chapter_count
        if coverage.effective_chapter_count
        else 0.0
    )
    try:
        from novel_authoring.initialization.metrics import metric_bootstrap_status

        metric_audit = metric_bootstrap_status(
            database,
            book_id,
            edition_id=selected,
            initialization_id=initialization_manifest.initialization_id,
        )
    except (InitializationError, OSError, ValueError) as exc:
        metric_audit = {
            "status": "NOT_READY",
            "errors": [f"Metric Bootstrap 审计失败：{exc}"],
            "coverage": {
                "metric_observation_coverage": 0.0,
                "recent_detailed_metric_coverage": 0.0,
                "current_chapter_metric_coverage": 0.0,
            },
        }
    metric_coverage = metric_audit.get("coverage", {})
    metric_observation_coverage = float(metric_coverage.get("metric_observation_coverage", 0.0))
    recent_detailed_metric_coverage = float(
        metric_coverage.get("recent_detailed_metric_coverage", 0.0)
    )
    current_chapter_metric_coverage = float(
        metric_coverage.get("current_chapter_metric_coverage", 0.0)
    )
    blockers: list[str] = []
    gaps: list[str] = []
    if chapter_coverage < 0.95:
        blockers.append("章节覆盖率低于 95%")
    if arc_coverage < 1.0:
        blockers.append("仍有 Arc 未完成语义提取")
    if (
        initialization_manifest.initialization_depth is InitializationDepth.FULL
        and continuity_index_coverage < 1.0
    ):
        blockers.append("全书逐章连续性索引尚未完成")
    elif continuity_index_coverage < 1.0:
        gaps.append("非阻塞历史章节仍保持 UNKNOWN / NOT_ANALYZED")
    if not core_graphs:
        blockers.append("当前核心 World Model/图谱尚未生成")
    if not protagonist_confirmed:
        blockers.append("主角当前状态尚未确认")
    if not thread_confirmed:
        blockers.append("当前主线程尚未确认")
    blockers.extend(continuation_boundary.blocking_gaps)
    if canon_evidence < 0.95 and outputs:
        gaps.append("CANON 记录的 source-span 证据覆盖不足")
    if pending:
        gaps.append(f"待处理 Arc：{len(pending)}")
    if failed:
        blockers.append(f"校验失败 Arc：{len(failed)}")
    if not entity_file.is_file():
        gaps.append("实体解析尚未写回")
    if metric_audit.get("status") != "COMPLETE":
        errors = metric_audit.get("errors") or ["严格 Semantic Metric Bootstrap 尚未完成"]
        blockers.append(f"Semantic Metric Bootstrap 未完成：{errors[0]}")
    partial_depth = initialization_manifest.initialization_depth is not InitializationDepth.FULL
    if partial_depth:
        blockers.append(
            f"{initialization_manifest.initialization_depth.value} 只提供渐进式访问；完整 READY 需要 FULL"
        )
    if (root / "synthesis" / "unresolved_assumptions.yaml").is_file():
        gaps.append("Future Possibility Space 仍保留未决假设")
    status = (
        "BLOCKED"
        if blockers
        else ("READY_WITH_GAPS" if gaps or chapter_coverage < 1.0 else "READY")
    )
    readiness = InitializationReadiness(
        status=status,
        chapter_coverage=chapter_coverage,
        arc_coverage=arc_coverage,
        source_mapping_coverage=source_mapping_coverage,
        arc_output_coverage=arc_output_coverage,
        chapter_semantic_feature_coverage=chapter_semantic_feature_coverage,
        continuity_index_coverage=continuity_index_coverage,
        metric_observation_coverage=metric_observation_coverage,
        recent_detailed_metric_coverage=recent_detailed_metric_coverage,
        current_chapter_metric_coverage=current_chapter_metric_coverage,
        metric_bootstrap_status=str(metric_audit.get("status", "NOT_READY")),
        metric_authority=("FULL" if not partial_depth else "PROVISIONAL"),
        metric_bootstrap=metric_audit,
        canon_evidence_coverage=canon_evidence,
        entity_resolution_coverage=entity_cov,
        core_graphs_complete=core_graphs,
        protagonist_confirmed=protagonist_confirmed,
        current_thread_confirmed=thread_confirmed,
        continuation_boundary=continuation_boundary,
        blocking_reasons=blockers,
        gaps=gaps,
        review_queue=sorted(set([*pending, *failed])),
    )
    metrics_ready = metric_audit.get("status") == "COMPLETE"
    if status == "READY":
        state = InitializationState.READY
    elif status == "READY_WITH_GAPS":
        state = InitializationState.READY_WITH_GAPS
    elif failed:
        state = InitializationState.BLOCKED
    elif not outputs:
        state = InitializationState.SOURCE_MAPPED
    elif pending:
        state = InitializationState.ARC_EXTRACTION_RUNNING
    elif not entity_file.is_file():
        state = InitializationState.ENTITY_RESOLUTION_RUNNING
    elif not core_graphs:
        state = InitializationState.SYNTHESIS_RUNNING
    elif not metrics_ready:
        state = InitializationState.METRIC_BOOTSTRAP_RUNNING
    else:
        state = InitializationState.ATLAS_VALIDATION_RUNNING
    capabilities = {
        **initialization_manifest.capabilities,
        "browse_structure": True,
        "view_partial_profile": chapter_coverage > 0.0,
        "plan_next": True,
        "continue_from_current_boundary": continuation_boundary.ready_for_continuation,
        "rewrite_selected_chapter": False,
        "inspect_global_world_state": (
            initialization_manifest.initialization_depth is InitializationDepth.FULL
            and status in {"READY", "READY_WITH_GAPS"}
        ),
    }
    with database.connect() as connection:
        samples = connection.execute(
            "SELECT active_processing_seconds, processed_chapter_count "
            "FROM workflow_handoffs WHERE book_id=? AND handoff_type='NOVEL_INITIALIZATION' "
            "AND status='COMPLETED' AND active_processing_seconds>0 "
            "ORDER BY task_completed_at DESC LIMIT 5",
            (book_id,),
        ).fetchall()
    seconds_per_chapter = [
        float(row["active_processing_seconds"]) / int(row["processed_chapter_count"])
        for row in samples
        if int(row["processed_chapter_count"] or 0) > 0
    ]
    observed_seconds_per_chapter = (
        sum(seconds_per_chapter) / len(seconds_per_chapter) if seconds_per_chapter else None
    )
    remaining_chapters = sum(
        len(
            set(arc.scheduled_continuity_chapter_ids)
            | set(arc.scheduled_semantic_chapter_ids)
        )
        for arc in arc_manifest.arcs
        if arc.arc_id in pending
    )
    estimated_remaining_seconds = (
        observed_seconds_per_chapter * remaining_chapters
        if observed_seconds_per_chapter is not None
        else None
    )
    status_payload = {
        "initialization_id": arc_manifest.initialization_id,
        "state": state.value,
        "readiness": readiness.model_dump(mode="json"),
        "source_coverage": coverage.chapter_coverage,
        "source_mapping_coverage": source_mapping_coverage,
        "arc_output_coverage": arc_output_coverage,
        "chapter_semantic_feature_coverage": chapter_semantic_feature_coverage,
        "metric_observation_coverage": metric_observation_coverage,
        "recent_detailed_metric_coverage": recent_detailed_metric_coverage,
        "current_chapter_metric_coverage": current_chapter_metric_coverage,
        "metric_bootstrap": metric_audit,
        "updated_at": utc_now(),
        "completed_arc_ids": [item.arc_id for item in outputs],
        "failed_arc_ids": failed,
        "pending_arc_ids": pending,
        "entity_count": (
            entity_result.resolved_major_entities
            if entity_result is not None
            else sum(len(item.characters) for item in outputs)
        ),
        "warnings": readiness.gaps,
        "initialization_depth": initialization_manifest.initialization_depth.value,
        "capabilities": capabilities,
        "uncovered_semantic_chapter_ids": [
            chapter_id
            for chapter_id in initialization_manifest.deep_chapter_ids
            if chapter_id not in analyzed_chapter_ids
        ]
        + list(initialization_manifest.uncovered_semantic_chapter_ids),
        "progress": {
            "reused_arc_count": len(initialization_manifest.reused_arc_ids),
            "completed_arc_count": len(outputs),
            "remaining_arc_count": len(pending),
            "observed_seconds_per_chapter": observed_seconds_per_chapter,
            "estimated_remaining_seconds": estimated_remaining_seconds,
            "eta_label": (
                "完成第一批分析后提供预计时间"
                if estimated_remaining_seconds is None
                else _eta_range_label(estimated_remaining_seconds)
            ),
        },
    }
    _write_json(root / "status.json", status_payload)
    _write_json(
        root / "initialization_manifest.json",
        initialization_manifest.model_copy(
            update={"state": state, "capabilities": capabilities}
        ).model_dump(mode="json"),
    )
    _write_reports(root, coverage, arc_manifest, outputs, readiness)
    _event(root, state.value, {"readiness": readiness.model_dump(mode="json")})
    return {
        "root": str(root),
        "status": status_payload,
        "readiness": readiness.model_dump(mode="json"),
    }
