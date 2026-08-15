"""Backend-neutral metadata query contracts for Reference Corpus V1.

The query seam deliberately returns compact, reference-only projections.  It
does not expose source prose, full evidence rows, Book DNA, or prose DNA to a
caller that asked for a planning or prose suggestion.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from novel_authoring.progression.models import PayoffChannel, ReaderExperience
from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.reference_corpus.semantic import (
    MACHINE_PACKAGE_VERSION,
    SemanticCorpusError,
    retrieve_metadata_candidates,
)
from novel_authoring.reference_corpus.semantic_models import (
    EvidenceScope,
    SemanticMaturity,
    SemanticStatus,
)
from novel_authoring.serial_kernel.models import NarrativeDrive
from novel_authoring.utils import sha256_file

QueryPurpose = Literal["PLANNING", "PROSE"]
QueryUsage = Literal["REFERENCE_ONLY"]
QueryStatus = Literal[
    "ENABLED",
    "ZERO_RESULTS",
    "UNAVAILABLE",
    "CORRUPT",
    "DISABLED",
]


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
    package_schema_version: str | None = None
    package_hash: str | None = None
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


def _query_echo(request: ReferenceCorpusQueryRequest) -> ReferenceCorpusQueryEcho:
    return ReferenceCorpusQueryEcho.model_validate(
        request.model_dump(
            mode="json",
            exclude={"purpose"},
        )
    )


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
    package_schema_version: str | None = None,
    package_hash: str | None = None,
) -> ReferenceCorpusQueryResponse:
    return ReferenceCorpusQueryResponse(
        schema_version="reference-corpus-query-v1",
        purpose=request.purpose,
        query=_query_echo(request),
        status=status,
        package_schema_version=package_schema_version,
        package_hash=package_hash,
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

    root = _root_from_config(corpus_root)
    if root is None:
        return _response(
            query,
            knowledge_gaps=["当前没有可用的 Reference Corpus machine package/path"],
            warnings=["soft-fail：Reference Corpus 未启用或未配置"],
            status="DISABLED",
        )
    if not root.is_dir():
        return _response(
            query,
            knowledge_gaps=["当前配置的 Reference Corpus path 不存在"],
            warnings=["soft-fail：Reference Corpus package/path 不存在"],
            status="UNAVAILABLE",
        )
    package_path = root / "machine" / "corpus-package.json"
    cards_path = root / "machine" / "cards.jsonl"
    if not package_path.is_file() or not cards_path.is_file():
        return _response(
            query,
            knowledge_gaps=["需要先 compile Reference Corpus machine package"],
            warnings=["soft-fail：machine package/path 不完整"],
            status="UNAVAILABLE",
        )
    package_schema_version: str | None = None
    package_hash: str | None = None
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
        if not isinstance(package, dict):
            raise ValueError("package 根节点不是 object")
        if package.get("schema_version") != MACHINE_PACKAGE_VERSION:
            raise ValueError("package schema_version 不正确")
        package_schema_version = str(package["schema_version"])
        package_hash = sha256_file(package_path)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        return _response(
            query,
            knowledge_gaps=["machine package 不能作为可靠的查询输入"],
            warnings=[f"corrupt package：{exc}"],
            status="CORRUPT",
        )

    families = _PLANNING_FAMILIES if query.purpose == "PLANNING" else _PROSE_FAMILIES
    legacy_tags = []
    # Keep old callers that passed a single ASCII tag working, while refusing
    # to turn a natural-language sentence into a machine tag.
    if (
        not query.creative_problem_tags
        and query.creative_problem
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", query.creative_problem.strip())
    ):
        legacy_tags = [query.creative_problem.strip()]
    try:
        records = retrieve_metadata_candidates(
            root,
            creative_problem_tags=query.creative_problem_tags or legacy_tags,
            reader_experiences=query.reader_experiences,
            narrative_drives=query.narrative_drives,
            payoff_channels=query.payoff_channels,
            scene_functions=query.scene_functions,
            card_families=families,
            max_cards=query.max_cards,
        )
        cards = [_compact_projection(record) for record in records]
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
            package_schema_version=package_schema_version,
            package_hash=package_hash,
        )
    if not cards:
        return _response(
            query,
            knowledge_gaps=["没有满足当前 purpose、metadata 和 source diversity 条件的卡片"],
            warnings=["soft-fail：query 返回 zero results"],
            status="ZERO_RESULTS",
            package_schema_version=package_schema_version,
            package_hash=package_hash,
        )
    return _response(
        query,
        cards=cards,
        status="ENABLED",
        package_schema_version=package_schema_version,
        package_hash=package_hash,
    )


query_corpus = query_reference_corpus


__all__ = [
    "CompactCard",
    "ContrastCardProjection",
    "CorpusSynthesisCardProjection",
    "MechanismCardProjection",
    "ProseControlCardProjection",
    "QueryRequest",
    "QueryResponse",
    "QueryStatus",
    "ReferenceCorpusQueryEcho",
    "ReferenceCorpusQueryRequest",
    "ReferenceCorpusQueryResponse",
    "SourceRefProjection",
    "query_corpus",
    "query_reference_corpus",
]
