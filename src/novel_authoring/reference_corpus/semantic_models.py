"""Strict machine contracts for Reference Corpus Semantic Distillation V1.

The models deliberately reuse TheGreatNovel's existing reader-experience,
narrative-drive, and payoff-channel enums.  They describe reference-only
knowledge; they do not own Canon, author intent, candidate approval, or prose.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.progression.models import PayoffChannel, ReaderExperience
from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.serial_kernel.models import NarrativeDrive


class SemanticStatus(StrEnum):
    REFERENCE_ONLY = "REFERENCE_ONLY"
    STALE = "STALE"


class SemanticMaturity(StrEnum):
    PILOT = "PILOT"
    SUPPORTED = "SUPPORTED"
    BROAD = "BROAD"


class SpanKind(StrEnum):
    CONTIGUOUS_ARC = "CONTIGUOUS_ARC"
    LONGITUDINAL_TRAJECTORY = "LONGITUDINAL_TRAJECTORY"


class EvidenceScope(StrEnum):
    SINGLE_BOOK = "SINGLE_BOOK"
    PILOT_TWO_BOOK = "PILOT_TWO_BOOK"
    MULTI_BOOK = "MULTI_BOOK"
    MULTI_CATEGORY = "MULTI_CATEGORY"


class EvidenceRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    source_book_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    distill_id: str = Field(min_length=1)
    segment_id: str = Field(pattern=r"^segment-[0-9]{4,}$")
    line_start: int = Field(ge=1)
    line_end: int = Field(ge=1)
    observation_summary: str = Field(min_length=1, max_length=320)

    @model_validator(mode="after")
    def validate_line_range(self) -> EvidenceRef:
        if self.line_end < self.line_start:
            raise ValueError("evidence line_end 不得小于 line_start")
        return self


class SemanticCardBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["reference-corpus-card-v1"]
    card_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    knowledge_level: CardKnowledgeLevel
    status: SemanticStatus
    source_book_ids: list[str] = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)
    creative_problem_tags: list[str] = Field(default_factory=list)
    reader_experiences: list[ReaderExperience] = Field(default_factory=list)
    narrative_drives: list[NarrativeDrive] = Field(default_factory=list)
    payoff_channels: list[PayoffChannel] = Field(default_factory=list)
    evidence_scope: EvidenceScope
    maturity: SemanticMaturity
    category_ids: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_source_alignment(self) -> SemanticCardBase:
        referenced = {item.source_book_id for item in self.evidence_refs}
        declared = set(self.source_book_ids)
        if not referenced <= declared:
            raise ValueError("evidence_refs 的 source_book_id 必须属于 source_book_ids")
        if self.evidence_scope is EvidenceScope.SINGLE_BOOK and len(declared) != 1:
            raise ValueError("SINGLE_BOOK 卡只能声明一个 source_book_id")
        return self


class ReferenceBookCard(SemanticCardBase):
    card_type: Literal["reference-book"]
    source_book_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    distill_id: str = Field(min_length=1)
    summary: str = Field(min_length=1)


class BookDnaCard(SemanticCardBase):
    card_type: Literal["book-dna"]
    source_book_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    rewrite_required: bool
    rewrite_reason: str = Field(min_length=1)
    sampling_strategy: str = Field(min_length=1)
    coverage_mode: str = Field(min_length=1)
    sample_window_count: int = Field(ge=1)
    coverage_stages: list[str] = Field(min_length=1)
    reader_promise: str = Field(min_length=1)
    repeatable_reader_loop: str = Field(min_length=1)
    core_progression_grammar: str = Field(min_length=1)
    payoff_grammar: str = Field(min_length=1)
    action_space_expansion: str = Field(min_length=1)
    advantage_special_capability: str = Field(min_length=1)
    world_expansion_grammar: str = Field(min_length=1)
    novelty_recombination: str = Field(min_length=1)
    character_desire_agency: str = Field(min_length=1)
    social_relationship_dynamics: str = Field(min_length=1)
    resource_economy: str = Field(min_length=1)
    optional_constraints_costs: str = Field(min_length=1)
    long_form_sustainability: str = Field(min_length=1)
    failure_fatigue_risks: list[str] = Field(min_length=1)
    transferable_variables: list[str] = Field(min_length=1)
    transfer_boundary: str = Field(min_length=1)
    anti_bias_checks: dict[str, Literal["PASS", "FAIL", "UNKNOWN"]]

    @model_validator(mode="after")
    def validate_book_identity(self) -> BookDnaCard:
        if self.source_book_id not in self.source_book_ids:
            raise ValueError("Book DNA 的 source_book_id 必须属于 source_book_ids")
        return self


class ArcObservationCard(SemanticCardBase):
    card_type: Literal["arc-observation"]
    source_book_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    span_kind: SpanKind
    local_creative_problem: str = Field(min_length=1)
    setup: str = Field(min_length=1)
    promise: str = Field(min_length=1)
    protagonist_action: str = Field(min_length=1)
    action_space_change: str = Field(min_length=1)
    progression: str = Field(min_length=1)
    payoff: str = Field(min_length=1)
    verification: str = Field(min_length=1)
    novelty: str = Field(min_length=1)
    aftermath: str = Field(min_length=1)
    future_opening: str = Field(min_length=1)
    optional_pressure: str = Field(min_length=1)
    optional_cost: str = Field(min_length=1)


class AtomicObservationCard(SemanticCardBase):
    card_type: Literal["observation"]
    source_book_id: str = Field(min_length=1)
    observation_summary: str = Field(min_length=1)
    confidence: Literal["HIGH", "MEDIUM", "LOW", "UNKNOWN"]
    failure_basis: Literal[
        "OBSERVED_REPETITION",
        "OBSERVED_STRUCTURAL_WEAKNESS",
        "INFERRED_RISK",
        "NOT_APPLICABLE",
    ]
    transfer_boundary: str = Field(min_length=1)


class MechanismCard(SemanticCardBase):
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
    source_count: int = Field(ge=1)
    category_count: int = Field(ge=1)


class ContrastSolution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solution_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    label: str = Field(min_length=1)
    source_book_ids: list[str] = Field(min_length=1)
    description: str = Field(min_length=1)
    conditions: list[str] = Field(min_length=1)
    reader_experience_differences: list[str] = Field(min_length=1)
    tradeoffs: list[str] = Field(min_length=1)
    failure_risks: list[str] = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)


class ContrastCard(SemanticCardBase):
    card_type: Literal["contrast-card"]
    shared_creative_problem: str = Field(min_length=1)
    solutions: list[ContrastSolution] = Field(min_length=3)
    transfer_boundary: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_solution_sources(self) -> ContrastCard:
        source_ids = set(self.source_book_ids)
        for solution in self.solutions:
            if not set(solution.source_book_ids) <= source_ids:
                raise ValueError("Contrast solution 的来源必须属于卡片来源集合")
        return self


class CorpusSynthesisCard(SemanticCardBase):
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


SemanticCard = Annotated[
    ReferenceBookCard
    | BookDnaCard
    | ArcObservationCard
    | AtomicObservationCard
    | MechanismCard
    | ContrastCard
    | CorpusSynthesisCard,
    Field(discriminator="card_type"),
]


__all__ = [
    "ArcObservationCard",
    "AtomicObservationCard",
    "BookDnaCard",
    "ContrastCard",
    "ContrastSolution",
    "CorpusSynthesisCard",
    "EvidenceRef",
    "EvidenceScope",
    "MechanismCard",
    "ReferenceBookCard",
    "SemanticCard",
    "SemanticMaturity",
    "SemanticStatus",
    "SpanKind",
]
