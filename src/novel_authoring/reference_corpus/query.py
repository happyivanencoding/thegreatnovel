"""Backend-neutral metadata query contracts for Reference Corpus V1.

The query seam deliberately returns compact, reference-only projections.  It
does not expose source prose, full evidence rows, Book DNA, or prose DNA to a
caller that asked for a planning or prose suggestion.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from novel_authoring.progression.models import PayoffChannel, ReaderExperience
from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.reference_corpus.semantic import (
    SemanticCorpusError,
    retrieve_metadata_candidates,
    validate_machine_package,
)
from novel_authoring.reference_corpus.semantic_models import (
    EvidenceScope,
    SemanticMaturity,
    SemanticStatus,
)
from novel_authoring.serial_kernel.models import NarrativeDrive

QueryPurpose = Literal["PLANNING", "PROSE"]
QueryUsage = Literal["REFERENCE_ONLY"]
QueryStatus = Literal[
    "ENABLED",
    "ZERO_RESULTS",
    "UNAVAILABLE",
    "CORRUPT",
    "DISABLED",
]
QueryMatchTier = Literal["EXACT", "FALLBACK", "ZERO_RESULTS"]


class ReferenceCorpusQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    purpose: QueryPurpose
    creative_problem: str = ""
    creative_problem_tags: list[str] = Field(default_factory=list)
    reader_experiences: list[str] = Field(default_factory=list)
    narrative_drives: list[str] = Field(default_factory=list)
    payoff_channels: list[str] = Field(default_factory=list)
    scene_functions: list[str] = Field(default_factory=list)
    max_cards: int = Field(default=6, ge=3, le=8)


class ReferenceCorpusQueryEcho(BaseModel):
    model_config = ConfigDict(extra="forbid")

    creative_problem: str = ""
    creative_problem_tags: list[str] = Field(default_factory=list)
    reader_experiences: list[str] = Field(default_factory=list)
    narrative_drives: list[str] = Field(default_factory=list)
    payoff_channels: list[str] = Field(default_factory=list)
    scene_functions: list[str] = Field(default_factory=list)
    max_cards: int = Field(ge=3, le=8)


class SourceRefProjection(BaseModel):
    """Locator-only provenance; never contains observation_summary or prose."""

    model_config = ConfigDict(extra="forbid")

    source_book_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    distill_id: str = Field(min_length=1)
    segment_id: str = Field(min_length=1)
    line_start: int = Field(ge=1)
    line_end: int = Field(ge=1)


class _CompactCardBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    card_id: str = Field(min_length=1)
    knowledge_level: CardKnowledgeLevel
    status: SemanticStatus
    source_book_ids: list[str] = Field(min_length=1)
    category_ids: list[str] = Field(default_factory=list)
    creative_problem_tags: list[str] = Field(default_factory=list)
    reader_experiences: list[ReaderExperience] = Field(default_factory=list)
    narrative_drives: list[NarrativeDrive] = Field(default_factory=list)
    payoff_channels: list[PayoffChannel] = Field(default_factory=list)
    evidence_scope: EvidenceScope
    maturity: SemanticMaturity
    source_refs: list[SourceRefProjection] = Field(min_length=1)
    metadata_match_fields: list[str] = Field(default_factory=list)


class MechanismCardProjection(_CompactCardBase):
    card_type: Literal["mechanism-card"]
    creative_problem: str = Field(min_length=1)
    applicability_conditions: list[str] = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    reader_payoff: list[str] = Field(min_length=1)
    action_space_effect: list[str] = Field(min_length=1)
    variants: list[str] = Field(min_length=1)
    when_not_to_use: list[str] = Field(min_length=1)
    contrast_cases: list[str] = Field(min_length=1)
    failure_risks: list[str] = Field(min_length=1)
    failure_basis: list[str] = Field(min_length=1)


class ContrastSolutionProjection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solution_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    source_book_ids: list[str] = Field(min_length=1)
    description: str = Field(min_length=1)
    conditions: list[str] = Field(min_length=1)
    reader_experience_differences: list[str] = Field(min_length=1)
    tradeoffs: list[str] = Field(min_length=1)
    failure_risks: list[str] = Field(min_length=1)


class ContrastCardProjection(_CompactCardBase):
    card_type: Literal["contrast-card"]
    shared_creative_problem: str = Field(min_length=1)
    solutions: list[ContrastSolutionProjection] = Field(min_length=3)
    transfer_boundary: str = Field(min_length=1)


class CorpusSynthesisCardProjection(_CompactCardBase):
    card_type: Literal["corpus-synthesis"]
    synthesis_kind: Literal["CATEGORY", "CROSS_CATEGORY"]
    title: str = Field(min_length=1)
    shared_creative_problem: str = Field(min_length=1)
    shared_tendencies: list[str] = Field(min_length=1)
    major_divergences: list[str] = Field(min_length=1)
    distinctive_mechanisms: list[str] = Field(min_length=1)
    payoff_differences: list[str] = Field(min_length=1)
    progression_differences: list[str] = Field(min_length=1)
    world_expansion_differences: list[str] = Field(min_length=1)
    failure_fatigue_risks: list[str] = Field(min_length=1)
    what_sample_cannot_tell_us: list[str] = Field(min_length=1)
    transfer_boundary: str = Field(min_length=1)


class ProseControlCardProjection(_CompactCardBase):
    card_type: Literal["prose-control"]
    control_topic: str = Field(min_length=1)
    applicable_scene_functions: list[str] = Field(min_length=1)
    guidance: str = Field(min_length=1)
    variants: list[str] = Field(min_length=1)
    when_to_use: list[str] = Field(min_length=1)
    failure_signals: list[str] = Field(min_length=1)
    transfer_boundary: str = Field(min_length=1)


CompactCard = Annotated[
    MechanismCardProjection
    | ContrastCardProjection
    | CorpusSynthesisCardProjection
    | ProseControlCardProjection,
    Field(discriminator="card_type"),
]


COMPACT_CARD_ADAPTER: TypeAdapter[CompactCard] = TypeAdapter(CompactCard)


class ReferenceCorpusQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["reference-corpus-query-v1"]
    purpose: QueryPurpose
    query: ReferenceCorpusQueryEcho
    status: QueryStatus = "ENABLED"
    match_tier: QueryMatchTier | None = None
    original_query: ReferenceCorpusQueryEcho | None = None
    effective_query: ReferenceCorpusQueryEcho | None = None
    relaxed_fields: list[str] = Field(default_factory=list)
    zero_result_reason: str | None = None
    package_schema_version: str | None = None
    package_hash: str | None = None
    machine_bundle_hash: str | None = None
    cards: list[CompactCard] = Field(default_factory=list, max_length=8)
    knowledge_gaps: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    usage: QueryUsage = "REFERENCE_ONLY"
    usage_note: Literal["Corpus suggestion ≠ instruction"] = (
        "Corpus suggestion ≠ instruction"
    )


# Short aliases keep the seam easy to discover without introducing another
# contract or a service class.
QueryRequest = ReferenceCorpusQueryRequest
QueryResponse = ReferenceCorpusQueryResponse

_PLANNING_FAMILIES = ("mechanism-card", "contrast-card", "corpus-synthesis")
_PROSE_FAMILIES = ("prose-control",)
_RELAXABLE_QUERY_FIELDS = (
    "creative_problem_tags",
    "reader_experiences",
    "narrative_drives",
    "payoff_channels",
    "scene_functions",
)
_ORIGINAL_PLANNING_PREFIXES = (
    "CORE_INNOVATION_PROPOSAL",
    "FOUNDATION_DEVELOPMENT_PROPOSAL",
    "STORY_FOUNDATION_PROPOSAL",
)


def _query_echo(request: ReferenceCorpusQueryRequest) -> ReferenceCorpusQueryEcho:
    return ReferenceCorpusQueryEcho.model_validate(
        request.model_dump(
            mode="json",
            exclude={"purpose"},
        )
    )


def _query_echo_with_metadata(
    request: ReferenceCorpusQueryRequest,
    metadata: Mapping[str, list[str]],
) -> ReferenceCorpusQueryEcho:
    payload = _query_echo(request).model_dump(mode="json")
    for field in _RELAXABLE_QUERY_FIELDS:
        payload[field] = list(metadata[field])
    return ReferenceCorpusQueryEcho.model_validate(payload)


def _source_refs(record: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    raw_refs = record.get("evidence_refs", [])
    if isinstance(raw_refs, list):
        refs.extend(item for item in raw_refs if isinstance(item, dict))
    if record.get("card_type") == "contrast-card":
        for solution in record.get("solutions", []):
            if isinstance(solution, dict):
                refs.extend(
                    item
                    for item in solution.get("evidence_refs", [])
                    if isinstance(item, dict)
                )
    compact: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in refs:
        evidence_id = str(ref.get("evidence_id", ""))
        if evidence_id and evidence_id in seen:
            continue
        if evidence_id:
            seen.add(evidence_id)
        compact.append(
            {
                "source_book_id": str(ref["source_book_id"]),
                "source_id": str(ref["source_id"]),
                "distill_id": str(ref["distill_id"]),
                "segment_id": str(ref["segment_id"]),
                "line_start": int(ref["line_start"]),
                "line_end": int(ref["line_end"]),
            }
        )
    return compact


def _common_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "card_id": record["card_id"],
        "knowledge_level": record["knowledge_level"],
        "status": record["status"],
        "source_book_ids": record["source_book_ids"],
        "category_ids": record.get("category_ids", []),
        "creative_problem_tags": record.get("creative_problem_tags", []),
        "reader_experiences": record.get("reader_experiences", []),
        "narrative_drives": record.get("narrative_drives", []),
        "payoff_channels": record.get("payoff_channels", []),
        "evidence_scope": record["evidence_scope"],
        "maturity": record["maturity"],
        "source_refs": _source_refs(record),
        "metadata_match_fields": record.get("metadata_match_fields", []),
    }


def _compact_projection(record: dict[str, Any]) -> CompactCard:
    if record.get("status") != SemanticStatus.REFERENCE_ONLY.value:
        raise ValueError("query projection 只能包含 REFERENCE_ONLY cards")
    card_type = record.get("card_type")
    common = _common_projection(record)
    if card_type == "mechanism-card":
        payload = {
            **common,
            "card_type": card_type,
            "creative_problem": record["creative_problem"],
            "applicability_conditions": record["applicability_conditions"],
            "mechanism": record["mechanism"],
            "reader_payoff": record["reader_payoff"],
            "action_space_effect": record["action_space_effect"],
            "variants": record["variants"],
            "when_not_to_use": record["when_not_to_use"],
            "contrast_cases": record["contrast_cases"],
            "failure_risks": record["failure_risks"],
            "failure_basis": record["failure_basis"],
        }
    elif card_type == "contrast-card":
        solutions = []
        for solution in record["solutions"]:
            solutions.append(
                {
                    key: solution[key]
                    for key in (
                        "solution_id",
                        "label",
                        "source_book_ids",
                        "description",
                        "conditions",
                        "reader_experience_differences",
                        "tradeoffs",
                        "failure_risks",
                    )
                }
            )
        payload = {
            **common,
            "card_type": card_type,
            "shared_creative_problem": record["shared_creative_problem"],
            "solutions": solutions,
            "transfer_boundary": record["transfer_boundary"],
        }
    elif card_type == "corpus-synthesis":
        payload = {
            **common,
            "card_type": card_type,
            "synthesis_kind": record["synthesis_kind"],
            "title": record["title"],
            "shared_creative_problem": record["shared_creative_problem"],
            "shared_tendencies": record["shared_tendencies"],
            "major_divergences": record["major_divergences"],
            "distinctive_mechanisms": record["distinctive_mechanisms"],
            "payoff_differences": record["payoff_differences"],
            "progression_differences": record["progression_differences"],
            "world_expansion_differences": record["world_expansion_differences"],
            "failure_fatigue_risks": record["failure_fatigue_risks"],
            "what_sample_cannot_tell_us": record["what_sample_cannot_tell_us"],
            "transfer_boundary": record["transfer_boundary"],
        }
    elif card_type == "prose-control":
        payload = {
            **common,
            "card_type": card_type,
            "control_topic": record["control_topic"],
            "applicable_scene_functions": record["applicable_scene_functions"],
            "guidance": record["guidance"],
            "variants": record["variants"],
            "when_to_use": record["when_to_use"],
            "failure_signals": record["failure_signals"],
            "transfer_boundary": record["transfer_boundary"],
        }
    else:
        raise ValueError(f"不允许的 query card family：{card_type}")
    return COMPACT_CARD_ADAPTER.validate_python(payload)


def _response(
    request: ReferenceCorpusQueryRequest,
    *,
    cards: list[CompactCard] | None = None,
    knowledge_gaps: list[str] | None = None,
    warnings: list[str] | None = None,
    status: QueryStatus = "ENABLED",
    match_tier: QueryMatchTier | None = None,
    original_query: ReferenceCorpusQueryEcho | None = None,
    effective_query: ReferenceCorpusQueryEcho | None = None,
    relaxed_fields: list[str] | None = None,
    zero_result_reason: str | None = None,
    package_schema_version: str | None = None,
    package_hash: str | None = None,
    machine_bundle_hash: str | None = None,
) -> ReferenceCorpusQueryResponse:
    return ReferenceCorpusQueryResponse(
        schema_version="reference-corpus-query-v1",
        purpose=request.purpose,
        query=_query_echo(request),
        status=status,
        match_tier=match_tier,
        original_query=original_query,
        effective_query=effective_query,
        relaxed_fields=relaxed_fields or [],
        zero_result_reason=zero_result_reason,
        package_schema_version=package_schema_version,
        package_hash=package_hash,
        machine_bundle_hash=machine_bundle_hash,
        cards=cards or [],
        knowledge_gaps=knowledge_gaps or [],
        warnings=warnings or [],
    )


def _root_from_config(corpus_root: Path | str | None) -> Path | None:
    if corpus_root is not None:
        return Path(corpus_root).expanduser()
    try:
        from novel_authoring.config import load_settings

        configured = load_settings().reference_corpus_root
    except (OSError, TypeError, ValueError):
        configured = None
    if configured is not None:
        return configured.expanduser()
    env_root = os.environ.get("NOVEL_REFERENCE_CORPUS_ROOT")
    return Path(env_root).expanduser() if env_root else None


def reference_corpus_runtime_diagnostic(
    *, corpus_root: Path | str | None = None
) -> dict[str, Any]:
    """Return the small runtime status needed to diagnose the configured package."""

    root = _root_from_config(corpus_root)
    result: dict[str, Any] = {
        "status": "DISABLED",
        "configured_root": None if root is None else str(root),
        "query_ready": False,
        "machine_bundle_hash": None,
        "bundle_seal_valid": False,
        "card_count": 0,
        "warnings": [],
        "knowledge_gaps": [],
    }
    if root is None:
        result["warnings"] = ["soft-fail：Reference Corpus 未启用或未配置"]
        result["knowledge_gaps"] = ["当前没有可用的 Reference Corpus machine package/path"]
        return result
    validation = validate_machine_package(root)
    result.update(
        {
            "status": validation["status"],
            "query_ready": bool(validation.get("query_ready", False)),
            "machine_bundle_hash": validation.get("machine_bundle_hash"),
            "bundle_seal_valid": bool(validation.get("bundle_seal_valid", False)),
            "card_count": int(validation.get("card_count", 0)),
            "warnings": list(validation.get("warnings", [])),
            "knowledge_gaps": list(validation.get("knowledge_gaps", [])),
        }
    )
    return result


def query_reference_corpus(
    request: ReferenceCorpusQueryRequest | Mapping[str, Any],
    *,
    corpus_root: Path | str | None = None,
) -> ReferenceCorpusQueryResponse:
    """Run a deterministic metadata query with a soft-fail boundary."""

    try:
        query = (
            request
            if isinstance(request, ReferenceCorpusQueryRequest)
            else ReferenceCorpusQueryRequest.model_validate(request)
        )
    except ValidationError:
        raise

    original_query = _query_echo(query)

    root = _root_from_config(corpus_root)
    if root is None:
        return _response(
            query,
            knowledge_gaps=["当前没有可用的 Reference Corpus machine package/path"],
            warnings=["soft-fail：Reference Corpus 未启用或未配置"],
            status="DISABLED",
            match_tier="ZERO_RESULTS",
            original_query=original_query,
            effective_query=original_query,
            zero_result_reason="REFERENCE_CORPUS_DISABLED",
        )
    validation = validate_machine_package(root)
    if validation["status"] != "ENABLED":
        return _response(
            query,
            knowledge_gaps=list(validation.get("knowledge_gaps", [])),
            warnings=list(validation.get("warnings", [])),
            status=validation["status"],
            match_tier="ZERO_RESULTS",
            original_query=original_query,
            effective_query=original_query,
            zero_result_reason=f"REFERENCE_CORPUS_{validation['status']}",
            package_schema_version=validation.get("package_schema_version"),
            package_hash=validation.get("package_hash"),
            machine_bundle_hash=validation.get("machine_bundle_hash"),
        )

    package_schema_version = validation.get("package_schema_version")
    package_hash = validation.get("package_hash")
    machine_bundle_hash = validation.get("machine_bundle_hash")

    families = _PLANNING_FAMILIES if query.purpose == "PLANNING" else _PROSE_FAMILIES
    legacy_tags = []
    creative_problem_text = query.creative_problem.strip()
    is_safe_legacy_tag = bool(
        creative_problem_text
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", creative_problem_text)
    )
    # Keep old callers that passed a single ASCII tag working, while refusing
    # to turn a natural-language sentence into a machine tag.
    if (
        not query.creative_problem_tags
        and is_safe_legacy_tag
    ):
        legacy_tags = [creative_problem_text]

    metadata: dict[str, list[str]] = {
        "creative_problem_tags": list(query.creative_problem_tags or legacy_tags),
        "reader_experiences": list(query.reader_experiences),
        "narrative_drives": list(query.narrative_drives),
        "payoff_channels": list(query.payoff_channels),
        "scene_functions": list(query.scene_functions),
    }
    effective_query = _query_echo_with_metadata(query, metadata)
    has_natural_language_problem = bool(creative_problem_text) and not is_safe_legacy_tag
    has_structured_metadata = any(metadata.values())
    if (
        query.purpose == "PLANNING"
        and not has_structured_metadata
        and creative_problem_text.startswith(_ORIGINAL_PLANNING_PREFIXES)
    ):
        # The Original adapter has no chapter metadata yet, but its stage
        # prefix is a supported machine boundary.  Use the stable corpus tag
        # rather than treating the premise prose as a retrieval key.
        metadata["creative_problem_tags"] = ["long-form"]
        effective_query = _query_echo_with_metadata(query, metadata)
        has_structured_metadata = True
    if has_natural_language_problem and not has_structured_metadata:
        return _response(
            query,
            knowledge_gaps=["没有可用于 deterministic retrieval 的结构化 metadata"],
            warnings=["soft-fail：query 返回 zero results"],
            status="ZERO_RESULTS",
            match_tier="ZERO_RESULTS",
            original_query=original_query,
            effective_query=effective_query,
            zero_result_reason="NATURAL_LANGUAGE_CREATIVE_PROBLEM_NOT_METADATA",
            package_schema_version=package_schema_version,
            package_hash=package_hash,
            machine_bundle_hash=machine_bundle_hash,
        )

    def retrieve_cards(current_metadata: Mapping[str, list[str]]) -> list[CompactCard]:
        records = retrieve_metadata_candidates(
            root,
            creative_problem_tags=current_metadata["creative_problem_tags"],
            reader_experiences=current_metadata["reader_experiences"],
            narrative_drives=current_metadata["narrative_drives"],
            payoff_channels=current_metadata["payoff_channels"],
            scene_functions=current_metadata["scene_functions"],
            card_families=families,
            max_cards=query.max_cards,
        )
        return [_compact_projection(record) for record in records]

    try:
        cards = retrieve_cards(metadata)
        if cards:
            return _response(
                query,
                cards=cards,
                status="ENABLED",
                match_tier="EXACT",
                original_query=original_query,
                effective_query=effective_query,
                package_schema_version=package_schema_version,
                package_hash=package_hash,
                machine_bundle_hash=machine_bundle_hash,
            )

        relaxed_fields: list[str] = []
        for field in _RELAXABLE_QUERY_FIELDS:
            if not metadata[field]:
                continue
            metadata[field] = []
            relaxed_fields.append(field)
            effective_query = _query_echo_with_metadata(query, metadata)
            # A natural-language creative problem remains human context, not
            # a machine retrieval key.  Structured dimensions can still be
            # relaxed one at a time and each tier must actually retrieve before
            # the next dimension is cleared.
            cards = retrieve_cards(metadata)
            if cards:
                return _response(
                    query,
                    cards=cards,
                    status="ENABLED",
                    match_tier="FALLBACK",
                    original_query=original_query,
                    effective_query=effective_query,
                    relaxed_fields=relaxed_fields,
                    package_schema_version=package_schema_version,
                    package_hash=package_hash,
                    machine_bundle_hash=machine_bundle_hash,
                )
    except (
        OSError,
        UnicodeError,
        SemanticCorpusError,
        ValidationError,
        TypeError,
        ValueError,
    ) as exc:
        return _response(
            query,
            knowledge_gaps=["machine package cards 无法解析为当前 V1 contract"],
            warnings=[f"corrupt package：{exc}"],
            status="CORRUPT",
            match_tier="ZERO_RESULTS",
            original_query=original_query,
            effective_query=effective_query,
            zero_result_reason="REFERENCE_CORPUS_CORRUPT",
            package_schema_version=package_schema_version,
            package_hash=package_hash,
            machine_bundle_hash=machine_bundle_hash,
        )
    if not cards:
        zero_result_reason = (
            "NO_MATCH_WITHOUT_NATURAL_LANGUAGE_METADATA_FALLBACK"
            if has_natural_language_problem
            else (
                "NO_MATCH_AFTER_BOUNDED_FALLBACK"
                if has_structured_metadata
                else "NO_MATCH_FOR_EXACT_METADATA"
            )
        )
        return _response(
            query,
            knowledge_gaps=["没有满足当前 purpose、metadata 和 source diversity 条件的卡片"],
            warnings=["soft-fail：query 返回 zero results"],
            status="ZERO_RESULTS",
            match_tier="ZERO_RESULTS",
            original_query=original_query,
            effective_query=effective_query,
            relaxed_fields=relaxed_fields,
            zero_result_reason=zero_result_reason,
            package_schema_version=package_schema_version,
            package_hash=package_hash,
            machine_bundle_hash=machine_bundle_hash,
        )
    raise AssertionError("unreachable: query result must return exact or fallback cards")


query_corpus = query_reference_corpus


__all__ = [
    "CompactCard",
    "ContrastCardProjection",
    "CorpusSynthesisCardProjection",
    "MechanismCardProjection",
    "ProseControlCardProjection",
    "QueryRequest",
    "QueryResponse",
    "QueryMatchTier",
    "QueryStatus",
    "ReferenceCorpusQueryEcho",
    "ReferenceCorpusQueryRequest",
    "ReferenceCorpusQueryResponse",
    "SourceRefProjection",
    "reference_corpus_runtime_diagnostic",
    "query_corpus",
    "query_reference_corpus",
]
