"""Strict machine contracts for Reference Corpus Semantic Distillation V1.

The models deliberately reuse TheGreatNovel's existing reader-experience,
narrative-drive, and payoff-channel enums.  They describe reference-only
knowledge; they do not own Canon, author intent, candidate approval, or prose.
"""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.progression.models import PayoffChannel, ReaderExperience
from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.serial_kernel.models import NarrativeDrive

_CHINESE_TEXT_RE = re.compile(r"[\u3400-\u9fff]")


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


class AntiBiasChecks(BaseModel):
    """Fixed semantic gates for a single-book DNA card.

    The field names are part of the V1 contract.  They intentionally use
    machine-safe snake_case names instead of the old human-readable labels.
    """

    model_config = ConfigDict(extra="forbid")

    payoff_removal: Literal["PASS", "FAIL", "UNKNOWN"]
    constraint_subtraction: Literal["PASS", "FAIL", "UNKNOWN"]
    professional_operations_replacement: Literal["PASS", "FAIL", "UNKNOWN"]
    governance_default: Literal["PASS", "FAIL", "UNKNOWN"]
    responsibility_default: Literal["PASS", "FAIL", "UNKNOWN"]
    cost_necessity: Literal["PASS", "FAIL", "UNKNOWN"]
    pure_upside: Literal["PASS", "FAIL", "UNKNOWN"]

    def values(self) -> tuple[str, ...]:
        return tuple(str(value) for value in self.model_dump(mode="json").values())


_COVERAGE_LIMIT_MARKERS = (
    "覆盖",
    "范围",
    "样本",
    "证据",
    "限制",
    "局部",
    "未见",
    "未覆盖",
    "不足",
    "未知",
    "不确定",
    "coverage",
    "sample",
    "evidence",
    "limitation",
    "unknown",
)


def _mentions_coverage_limit(reason: str) -> bool:
    lowered = reason.casefold()
    return any(marker.casefold() in lowered for marker in _COVERAGE_LIMIT_MARKERS)


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
    anti_bias_checks: AntiBiasChecks

    @model_validator(mode="after")
    def validate_book_identity(self) -> BookDnaCard:
        if self.source_book_id not in self.source_book_ids:
            raise ValueError("Book DNA 的 source_book_id 必须属于 source_book_ids")
        results = self.anti_bias_checks.values()
        if "FAIL" in results and not (
            self.rewrite_required or self.status is SemanticStatus.STALE
        ):
            raise ValueError("AntiBiasChecks 存在 FAIL 时必须 rewrite_required 或标记 STALE")
        if "UNKNOWN" in results and not _mentions_coverage_limit(self.rewrite_reason):
            raise ValueError("AntiBiasChecks 存在 UNKNOWN 时 rewrite_reason 必须说明覆盖限制")
        return self


class ProseSceneWindow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    window_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    scene_function: Literal[
        "OPENING",
        "ORDINARY",
        "DIALOGUE",
        "ACTION",
        "PAYOFF",
        "AFTERMATH",
        "EXPOSITION",
        "EMOTION",
        "LATE",
        "ENDING",
        "UNKNOWN",
        "NOT_APPLICABLE",
    ]
    segment_id: str = Field(pattern=r"^segment-[0-9]{4,}$")
    line_start: int = Field(ge=1)
    line_end: int = Field(ge=1)
    evidence_summary: str = Field(min_length=1, max_length=320)

    @model_validator(mode="after")
    def validate_line_range(self) -> ProseSceneWindow:
        if self.line_end < self.line_start:
            raise ValueError("Prose DNA sample window 的 line_end 不得小于 line_start")
        return self


class ProseObservations(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sentence_rhythm: str = Field(min_length=1, max_length=800)
    paragraph_rhythm: str = Field(min_length=1, max_length=800)
    narrative_distance: str = Field(min_length=1, max_length=800)
    concrete_vs_abstract: str = Field(min_length=1, max_length=800)
    dialogue: str = Field(min_length=1, max_length=800)
    character_voice: str = Field(min_length=1, max_length=800)
    interior_thought: str = Field(min_length=1, max_length=800)
    action_combat: str = Field(min_length=1, max_length=800)
    payoff_realization: str = Field(min_length=1, max_length=800)
    description: str = Field(min_length=1, max_length=800)
    transitions: str = Field(min_length=1, max_length=800)
    chapter_ending: str = Field(min_length=1, max_length=800)
    lexical_texture: str = Field(min_length=1, max_length=800)
    punctuation: str = Field(min_length=1, max_length=800)
    human_irregularity: str = Field(min_length=1, max_length=800)


class ProseSoftControls(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sentence_rhythm: str = Field(min_length=1, max_length=400)
    paragraph_rhythm: str = Field(min_length=1, max_length=400)
    dialogue_density: str = Field(min_length=1, max_length=400)
    narrative_distance: str = Field(min_length=1, max_length=400)
    interiority: str = Field(min_length=1, max_length=400)
    exposition_mode: str = Field(min_length=1, max_length=400)
    sensory_density: str = Field(min_length=1, max_length=400)
    humor_mode: str = Field(min_length=1, max_length=400)
    action_directness: str = Field(min_length=1, max_length=400)
    payoff_realization: str = Field(min_length=1, max_length=400)
    chapter_end_modes: str = Field(min_length=1, max_length=400)
    lexical_texture: str = Field(min_length=1, max_length=400)


class ProseDnaCard(SemanticCardBase):
    """One-book prose execution evidence; never a story-planning authority."""

    card_type: Literal["prose-dna"]
    source_book_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    sampling_strategy: str = Field(min_length=1, max_length=400)
    coverage_mode: Literal["SCENE_FUNCTION_WINDOWS"]
    sample_window_count: int = Field(ge=8)
    scene_functions: list[str] = Field(min_length=1)
    sample_windows: list[ProseSceneWindow] = Field(min_length=8)
    observations: ProseObservations
    soft_controls: ProseSoftControls
    source_style_leakage_check: Literal["PASS"]
    source_style_leakage_note: str = Field(min_length=1, max_length=400)
    transfer_boundary: str = Field(min_length=1, max_length=600)
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_prose_identity(self) -> ProseDnaCard:
        if self.source_book_id not in self.source_book_ids:
            raise ValueError("Prose DNA 的 source_book_id 必须属于 source_book_ids")
        if self.sample_window_count != len(self.sample_windows):
            raise ValueError("Prose DNA 的 sample_window_count 必须等于 sample_windows 数量")
        window_ids = [window.window_id for window in self.sample_windows]
        if len(window_ids) != len(set(window_ids)):
            raise ValueError("Prose DNA 的 window_id 不得重复")
        observed_functions = {window.scene_function for window in self.sample_windows}
        if not observed_functions <= set(self.scene_functions):
            raise ValueError("Prose DNA 的 scene_functions 必须覆盖 sample_windows 的场景功能")
        return self


class ProseControlCard(SemanticCardBase):
    """Cross-book, abstract prose guidance for reference-only retrieval."""

    card_type: Literal["prose-control"]
    control_topic: str = Field(min_length=1, max_length=160)
    applicable_scene_functions: list[str] = Field(min_length=1)
    guidance: str = Field(min_length=1, max_length=360)
    variants: list[str] = Field(min_length=1)
    when_to_use: list[str] = Field(min_length=1)
    failure_signals: list[str] = Field(min_length=1)
    transfer_boundary: str = Field(min_length=1, max_length=360)

    @model_validator(mode="after")
    def validate_prose_control(self) -> ProseControlCard:
        if self.maturity is not SemanticMaturity.PILOT:
            if len(set(self.source_book_ids)) < 4:
                raise ValueError("General Prose Control 至少需要 4 本 distinct books")
            if len(set(self.category_ids)) < 3:
                raise ValueError("General Prose Control 至少需要 3 个 distinct categories")
        text_fields = (
            self.control_topic,
            self.guidance,
            *self.variants,
            *self.when_to_use,
            *self.failure_signals,
            self.transfer_boundary,
        )
        if any(not _CHINESE_TEXT_RE.search(value) for value in text_fields):
            raise ValueError("Prose Control 的抽象内容必须使用中文")
        if any(len(value) > 360 for value in self.variants):
            raise ValueError("Prose Control 不得保存长引文或长段来源文本")
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
    | ProseDnaCard
    | ProseControlCard
    | ArcObservationCard
    | AtomicObservationCard
    | MechanismCard
    | ContrastCard
    | CorpusSynthesisCard,
    Field(discriminator="card_type"),
]


__all__ = [
    "ArcObservationCard",
    "AntiBiasChecks",
    "AtomicObservationCard",
    "BookDnaCard",
    "ContrastCard",
    "ContrastSolution",
    "CorpusSynthesisCard",
    "EvidenceRef",
    "EvidenceScope",
    "MechanismCard",
    "ProseDnaCard",
    "ProseControlCard",
    "ProseObservations",
    "ProseSceneWindow",
    "ProseSoftControls",
    "ReferenceBookCard",
    "SemanticCard",
    "SemanticMaturity",
    "SemanticStatus",
    "SpanKind",
]
