from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.author_control.book_profile import PROFILE_DIMENSIONS
from novel_authoring.domain.models import ContinuationMode, NarrativeFunction
from novel_authoring.metrics.gates import HardGateInput
from novel_authoring.planning.innovation import (
    CandidateInnovationPreview,
    InnovationCommitments,
    InnovationControl,
    InnovationDiagnostics,
    InnovationTrace,
    NarrativePortfolioSnapshot,
)


class BoundaryChapter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chapter_id: str
    ordinal: int
    heading: str
    content: str
    source_span_id: str


class EarlierSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chapter_id: str
    ordinal: int
    heading: str
    summary: str


class ContinuationBoundaryPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    book_id: str
    edition_id: str = "base"
    base_event_seq: int
    base_projection_hash: str
    current_position: dict[str, Any]
    recent_full_chapters: list[BoundaryChapter]
    earlier_summaries: list[EarlierSummary]
    relevant_source_spans: list[dict[str, Any]] = Field(default_factory=list)
    canon_facts: dict[str, dict[str, Any]]
    character_states: dict[str, dict[str, Any]]
    knowledge_boundaries: dict[str, dict[str, Any]]
    active_threads: list[dict[str, Any]]
    promises: dict[str, dict[str, Any]]
    resources: dict[str, dict[str, Any]]
    capabilities: dict[str, dict[str, Any]]
    relationships: dict[str, dict[str, Any]]
    recent_payoffs: dict[str, dict[str, Any]]
    recent_structures: list[dict[str, Any]]
    style_profiles: list[dict[str, Any]]
    author_directives: list[dict[str, Any]]
    rhythm_features: list[dict[str, Any]] = Field(default_factory=list)
    rhythm_diagnostics: dict[str, Any] = Field(default_factory=dict)
    hook_diagnostics: dict[str, Any] = Field(default_factory=dict)
    story_atlas_anchor: dict[str, Any] = Field(default_factory=dict)
    batch_anchor: dict[str, Any] = Field(default_factory=dict)
    active_author_truths: list[dict[str, Any]] = Field(default_factory=list)
    reveal_agenda: dict[str, Any] = Field(default_factory=dict)
    innovation_control: InnovationControl = Field(default_factory=InnovationControl)
    innovation_diagnostics: InnovationDiagnostics | None = None
    narrative_portfolio: NarrativePortfolioSnapshot | None = None
    warnings: list[str] = Field(default_factory=list)


class CandidateScoreInputs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    thread_need_fit: float | None = Field(default=None, ge=0, le=100)
    pressure_curve_fit: float | None = Field(default=None, ge=0, le=100)
    debt_utility: float | None = Field(default=None, ge=0, le=100)
    progress_gain: float | None = Field(default=None, ge=0, le=100)
    payoff_or_setup_utility: float | None = Field(default=None, ge=0, le=100)
    agency_gain: float | None = Field(default=None, ge=0, le=100)
    risk_fit: float | None = Field(default=None, ge=0, le=100)
    structural_diversity: float | None = Field(default=None, ge=0, le=100)
    style_fit: float | None = Field(default=None, ge=0, le=100)
    repetition_fatigue: float | None = Field(default=None, ge=0, le=100)
    future_damage: float | None = Field(default=None, ge=0, le=100)


class CandidateLens(StrEnum):
    CONTINUITY_ACTIVE_THREAD = "CONTINUITY_ACTIVE_THREAD"
    EARNED_OPPORTUNITY = "EARNED_OPPORTUNITY"
    FORWARD_EXPANSION = "FORWARD_EXPANSION"


class ReaderPromiseService(StrEnum):
    SERVED = "SERVED"
    PARTIALLY_SERVED = "PARTIALLY_SERVED"
    NOT_RELEVANT = "NOT_RELEVANT"
    CONTRADICTED = "CONTRADICTED"


class ReaderPromiseAlignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    promise_id: str
    priority: str
    service: ReaderPromiseService
    evidence: list[str] = Field(default_factory=list)


class NarrativeDriveAlignment(BaseModel):
    """Generic drive trace alongside, never instead of, specialized impacts."""

    model_config = ConfigDict(extra="forbid")

    primary_drive: str | None = None
    primary_drive_effect: str = ""
    secondary_drive_effects: dict[str, str] = Field(default_factory=dict)
    drives_advanced: list[str] = Field(default_factory=list)
    drives_paid_off: list[str] = Field(default_factory=list)
    drives_deferred: list[str] = Field(default_factory=list)
    drive_conflicts: list[str] = Field(default_factory=list)
    drive_balance: str = "UNKNOWN"
    evidence: list[str] = Field(default_factory=list)


class SchedulerAlignment(BaseModel):
    """Candidate response to the frozen scheduler recommendation."""

    model_config = ConfigDict(extra="forbid")

    recommended_primary_intent: str | None = None
    candidate_primary_intent: str | None = None
    alignment: str = "UNKNOWN"
    deviation_reason: str = ""
    debts_served: list[str] = Field(default_factory=list)
    anticipations_served: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_override_reason(self) -> SchedulerAlignment:
        if (
            self.recommended_primary_intent
            and self.candidate_primary_intent
            and self.recommended_primary_intent != self.candidate_primary_intent
            and not self.deviation_reason.strip()
        ):
            raise ValueError("Candidate 偏离 Scheduler Recommendation 时必须说明原因")
        return self


class ProgressComponent(StrEnum):
    PERMANENT_GROWTH = "permanent_growth"
    WORLD_STATE_CHANGE = "world_state_change"
    RELATIONSHIP_CHANGE = "relationship_change"
    KNOWLEDGE_CHANGE = "knowledge_change"
    GOAL_ADVANCE = "goal_advance"
    STRATEGY_EXPANSION = "strategy_expansion"


class ProgressComponentEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    component: ProgressComponent
    value: float = Field(ge=0, le=100)
    evidence: list[str] = Field(min_length=1)


class ProgressPreview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    components: list[ProgressComponentEvidence] = Field(min_length=6, max_length=6)
    metric_run_id: str | None = None

    @model_validator(mode="after")
    def validate_components(self) -> ProgressPreview:
        expected = set(ProgressComponent)
        actual = {item.component for item in self.components}
        if actual != expected:
            raise ValueError("Progress Preview 必须提供六个唯一分量")
        return self

    @property
    def values(self) -> dict[str, float]:
        return {item.component.value: item.value for item in self.components}


class ProgressionImpact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    axis_advanced: list[str] = Field(default_factory=list)
    progression_delta_type: list[str] = Field(default_factory=list)
    stage_change: str | None = None
    branch_change: str | None = None
    bottleneck_change: str | None = None
    resource_change: list[str] = Field(default_factory=list)
    ability_unlock: list[str] = Field(default_factory=list)
    ability_showcase: list[str] = Field(default_factory=list)
    growth_cost: list[str] = Field(default_factory=list)
    new_ceiling_visibility: list[str] = Field(default_factory=list)
    future_progression_space: list[str] = Field(default_factory=list)


class NoveltyProvenance(StrEnum):
    EXISTING_RUNTIME = "EXISTING_RUNTIME"
    SOURCE_EARNED = "SOURCE_EARNED"
    FORWARD_NOVELTY = "FORWARD_NOVELTY"
    AUTHOR_DIRECTED = "AUTHOR_DIRECTED"
    DISTILLED_INSPIRATION = "DISTILLED_INSPIRATION"


class NoveltyBoundary(StrEnum):
    FORWARD_CANON_COMPATIBLE = "FORWARD_CANON_COMPATIBLE"
    RETROACTIVE_UNSUPPORTED_INVENTION = "RETROACTIVE_UNSUPPORTED_INVENTION"


class NoveltyDeclaration(BaseModel):
    """Provenance for a candidate's new state or creative opportunity."""

    model_config = ConfigDict(extra="forbid")

    provenance: NoveltyProvenance
    novelty_boundary: NoveltyBoundary = NoveltyBoundary.FORWARD_CANON_COMPATIBLE
    introduction_event: str = ""
    causal_source: str = ""
    new_state_if_committed: str = ""
    conflicts_checked: list[str] = Field(default_factory=list)
    retroactive_claim: bool = False

    @model_validator(mode="after")
    def validate_forward_boundary(self) -> NoveltyDeclaration:
        if self.provenance is NoveltyProvenance.FORWARD_NOVELTY:
            if self.retroactive_claim:
                raise ValueError("FORWARD_NOVELTY 不得声明为 retroactive invention")
            missing = [
                name
                for name, value in {
                    "introduction_event": self.introduction_event,
                    "causal_source": self.causal_source,
                    "new_state_if_committed": self.new_state_if_committed,
                }.items()
                if not value.strip()
            ]
            if missing:
                raise ValueError(
                    "FORWARD_NOVELTY 必须提供 introduction_event、causal_source、"
                    f"new_state_if_committed：{', '.join(missing)}"
                )
        return self


class AuthorTaskTraceHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    title: str
    effect: str
    strength: str


class AuthorIntentTraceHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent_id: str
    title: str
    effect: str
    strength: str


class AuthorControlTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author_task_hits: list[AuthorTaskTraceHit] = Field(default_factory=list)
    author_intent_hits: list[AuthorIntentTraceHit] = Field(default_factory=list)
    author_tasks_advanced: list[str] = Field(default_factory=list)
    author_intents_advanced: list[str] = Field(default_factory=list)
    author_goals_not_used: list[str] = Field(default_factory=list)
    unused_reasons: dict[str, str] = Field(default_factory=dict)


class ProfileDimensionAlignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension: str
    alignment: str
    evidence: list[str] = Field(default_factory=list)


class ProfileConstraintCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edit_id: str
    passed: bool
    evidence: str


class CandidateProfileAlignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimensions: list[ProfileDimensionAlignment] = Field(default_factory=list)
    constraint_checks: list[ProfileConstraintCheck] = Field(default_factory=list)

    @model_validator(mode="after")
    def dimensions_are_unique(self) -> CandidateProfileAlignment:
        names = [item.dimension for item in self.dimensions]
        allowed = {item[0] for item in PROFILE_DIMENSIONS}
        if len(names) != len(set(names)) or any(name not in allowed for name in names):
            raise ValueError("Profile alignment 维度必须唯一且属于九维画像")
        return self


class CandidateTruthAlignment(BaseModel):
    """How a proposal uses a frozen truth without inventing reveal permission."""

    model_config = ConfigDict(extra="forbid")

    truth_id: str
    title: str = ""
    behavioral_effect: str = Field(min_length=1)
    respected: bool = True
    agenda_bucket: str = "KEEP_HIDDEN"
    evidence: list[str] = Field(default_factory=list)


class CandidateRevealEventPreview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_id: str
    depth: str
    clue: str = ""
    target: str = "READER"
    target_entity_id: str | None = None
    reader_knowledge_delta: str = "UNCHANGED"
    character_knowledge_delta: dict[str, str] = Field(default_factory=dict)


class CandidateRevealImpact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    secrets_used: list[str] = Field(default_factory=list)
    hints: list[CandidateRevealEventPreview] = Field(default_factory=list)
    partial_reveals: list[CandidateRevealEventPreview] = Field(default_factory=list)
    full_reveals: list[CandidateRevealEventPreview] = Field(default_factory=list)
    kept_hidden: list[str] = Field(default_factory=list)
    reader_knowledge_delta: list[str] = Field(default_factory=list)
    character_knowledge_delta: list[str] = Field(default_factory=list)


class CandidateRevealImpactSubmission(BaseModel):
    """Creative reveal choices; KEEP_HIDDEN is compiled from the frozen agenda."""

    model_config = ConfigDict(extra="forbid")

    secrets_used: list[str] = Field(default_factory=list)
    hints: list[CandidateRevealEventPreview] = Field(default_factory=list)
    partial_reveals: list[CandidateRevealEventPreview] = Field(default_factory=list)
    full_reveals: list[CandidateRevealEventPreview] = Field(default_factory=list)
    reader_knowledge_delta: list[str] = Field(default_factory=list)
    character_knowledge_delta: list[str] = Field(default_factory=list)


class CandidateCreativeProposal(BaseModel):
    """Only the creative decisions an executor is allowed to submit."""

    model_config = ConfigDict(extra="forbid")

    local_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str
    summary: str
    primary_thread_id: str
    primary_function: NarrativeFunction
    secondary_functions: list[NarrativeFunction] = Field(default_factory=list, max_length=2)
    reader_question: str
    event_source: str
    solution_method: str
    protagonist_strategy: str
    risk_form: str
    opportunity_cost: str
    emotional_outcome: str
    social_feedback: str
    scene_topology: str
    ending_state: str
    state_changes: list[str] = Field(min_length=1)
    causal_sources: list[str] = Field(min_length=1)
    promises_to_advance: list[str] = Field(default_factory=list)
    promises_to_pay: list[str] = Field(default_factory=list)
    required_irreversible_change: str
    required_cost: str = ""
    pressure_before: float | None = Field(default=None, ge=0, le=100)
    pressure_target_after: float | None = Field(default=None, ge=0, le=100)
    outcome_magnitude: str = ""
    action_space_delta: str = ""
    knowledge_delta: str = ""
    relationship_delta: str = ""
    world_scale_delta: str = ""
    core_promise_delivery: str = ""
    lens: CandidateLens = CandidateLens.CONTINUITY_ACTIVE_THREAD
    novelty_provenance: list[NoveltyDeclaration] = Field(default_factory=list)
    wildcard: bool = False
    innovation_preview: CandidateInnovationPreview | None = None
    reveal_impact: CandidateRevealImpactSubmission = Field(
        default_factory=CandidateRevealImpactSubmission
    )
    chapter_intent: str | None = None

    @model_validator(mode="after")
    def reject_retroactive_invention(self) -> CandidateCreativeProposal:
        if any(
            item.novelty_boundary is NoveltyBoundary.RETROACTIVE_UNSUPPORTED_INVENTION
            for item in self.novelty_provenance
        ):
            raise ValueError(
                "候选不得把未在 selected Edition 建立的状态声明为 retroactive invention"
            )
        return self


class PlanningReferenceProvenance(BaseModel):
    """Reference-only provenance carried through planning without becoming Canon."""

    model_config = ConfigDict(extra="forbid")

    reference_strategy_id: str | None = None
    snapshot_id: str | None = None
    snapshot_hash: str | None = None
    card_ids_used: list[str] = Field(default_factory=list)
    selected_solutions: list[str] = Field(default_factory=list)
    application_summary: str = ""
    match_tier: str = "EXACT"
    usage: str = "REFERENCE_ONLY"
    reuse_reason: str | None = None


class PlanningReferenceStrategy(BaseModel):
    """Bounded, reference-only choice made before candidate generation."""

    model_config = ConfigDict(extra="forbid")

    strategy_id: str
    snapshot_id: str | None = None
    snapshot_hash: str | None = None
    selected_card_ids: list[str] = Field(default_factory=list, max_length=3)
    selected_cards: list[dict[str, Any]] = Field(default_factory=list, max_length=3)
    selected_contrast_solutions: list[str] = Field(
        default_factory=list, max_length=3
    )
    application_summary: str = ""
    failure_modes: list[str] = Field(default_factory=list)
    match_tier: str = "EXACT"
    usage: str = "REFERENCE_ONLY"
    reuse_reason: str | None = None


class CandidateProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    local_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str
    summary: str
    primary_thread_id: str
    primary_function: NarrativeFunction
    secondary_functions: list[NarrativeFunction] = Field(default_factory=list, max_length=2)
    reader_question: str
    event_source: str
    solution_method: str
    protagonist_strategy: str
    risk_form: str
    opportunity_cost: str
    emotional_outcome: str
    social_feedback: str
    scene_topology: str
    ending_state: str
    state_changes: list[str] = Field(min_length=1)
    causal_sources: list[str] = Field(min_length=1)
    promises_to_advance: list[str] = Field(default_factory=list)
    promises_to_pay: list[str] = Field(default_factory=list)
    required_irreversible_change: str
    required_cost: str = ""
    must_not_resolve: list[str] = Field(default_factory=list)
    canon_constraints: list[str] = Field(default_factory=list)
    knowledge_constraints: list[str] = Field(default_factory=list)
    forbidden_repetitions: list[str] = Field(default_factory=list)
    style_constraints: dict[str, str] = Field(default_factory=dict)
    commit_updates: list[str] = Field(min_length=1)
    pressure_before: float = Field(ge=0, le=100)
    pressure_target_after: float = Field(ge=0, le=100)
    outcome_magnitude: str = ""
    action_space_delta: str = ""
    knowledge_delta: str = ""
    relationship_delta: str = ""
    world_scale_delta: str = ""
    core_promise_delivery: str = ""
    score_inputs: CandidateScoreInputs
    score_evidence: dict[str, list[str]]
    gate_input: HardGateInput
    lens: CandidateLens = CandidateLens.CONTINUITY_ACTIVE_THREAD
    novelty_provenance: list[NoveltyDeclaration] = Field(default_factory=list)
    wildcard: bool = False
    innovation_preview: CandidateInnovationPreview | None = None
    author_control_trace: AuthorControlTrace = Field(default_factory=AuthorControlTrace)
    profile_alignment: CandidateProfileAlignment = Field(
        default_factory=CandidateProfileAlignment
    )
    truth_alignment: list[CandidateTruthAlignment] = Field(default_factory=list)
    reveal_impact: CandidateRevealImpact = Field(default_factory=CandidateRevealImpact)
    reader_promise_alignment: list[ReaderPromiseAlignment] = Field(default_factory=list)
    genre_alignment: list[str] = Field(default_factory=list)
    narrative_drive_alignment: NarrativeDriveAlignment = Field(
        default_factory=NarrativeDriveAlignment
    )
    progress_preview: ProgressPreview | None = None
    progression_impact: ProgressionImpact = Field(default_factory=ProgressionImpact)
    payoff_channel_impact: list[str] = Field(default_factory=list)
    world_expansion_impact: list[str] = Field(default_factory=list)
    resource_opportunity_impact: list[str] = Field(default_factory=list)
    chapter_intent: str | None = None
    scheduler_alignment: SchedulerAlignment = Field(default_factory=SchedulerAlignment)
    progression_debt_impact: list[str] = Field(default_factory=list)
    anticipation_impact: list[str] = Field(default_factory=list)
    genre_drift_diagnostic: dict[str, Any] = Field(default_factory=dict)
    genre_evolution_diagnostic: dict[str, Any] = Field(default_factory=dict)
    narrative_drive_drift_diagnostic: dict[str, Any] = Field(default_factory=dict)
    reference_provenance: PlanningReferenceProvenance = Field(
        default_factory=PlanningReferenceProvenance
    )

    @model_validator(mode="after")
    def reject_retroactive_invention(self) -> CandidateProposal:
        if any(
            item.novelty_boundary is NoveltyBoundary.RETROACTIVE_UNSUPPORTED_INVENTION
            for item in self.novelty_provenance
        ):
            raise ValueError(
                "候选不得把未在 selected Edition 建立的状态声明为 retroactive invention"
            )
        return self


class CandidateOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    candidates: list[CandidateProposal] = Field(min_length=2, max_length=3)
    innovation_control: InnovationControl | None = None
    notes: list[str] = Field(default_factory=list)


class CandidateCreativeOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    candidates: list[CandidateCreativeProposal] = Field(min_length=2, max_length=3)
    notes: list[str] = Field(default_factory=list)


class ChapterExperienceSignature(BaseModel):
    """Soft, reusable description of how a chapter delivers its experience."""

    model_config = ConfigDict(extra="forbid")

    event_source: str = ""
    solution_method: str = ""
    protagonist_strategy: str = ""
    risk_form: str = ""
    emotional_outcome: str = ""
    social_feedback: str = ""
    scene_topology: str = ""
    ending_mode: str = ""
    outcome_magnitude: str = ""
    action_space_delta: str = ""
    knowledge_delta: str = ""
    relationship_delta: str = ""
    world_scale_delta: str = ""
    core_promise_delivery: str = ""


class ThreadPriority(BaseModel):
    model_config = ConfigDict(extra="forbid")

    thread_id: str
    goal: str
    score: float
    inputs: dict[str, float]
    evidence: list[str]


class ChapterContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str
    chapter: int
    mode: ContinuationMode
    boundary_packet_id: str
    continuation_boundary: dict[str, Any]
    candidate_id: str
    primary_thread: str
    primary_function: NarrativeFunction
    secondary_functions: list[NarrativeFunction] = Field(max_length=2)
    reader_question: str
    pressure: dict[str, float]
    payoff_plan: dict[str, Any]
    narrative_debt: dict[str, list[str] | int]
    progress: dict[str, str | float]
    required_irreversible_change: str
    required_cost: str
    canon_constraints: list[str]
    knowledge_constraints: list[str]
    must_not_resolve: list[str]
    forbidden_repetitions: list[str]
    style_constraints: dict[str, str]
    ending_state: str
    commit_updates: list[str] = Field(min_length=1)
    rhythm_constraints: dict[str, Any] = Field(default_factory=dict)
    lens: CandidateLens = CandidateLens.CONTINUITY_ACTIVE_THREAD
    novelty_provenance: list[NoveltyDeclaration] = Field(default_factory=list)
    innovation_control: InnovationControl = Field(default_factory=InnovationControl)
    innovation_preview: CandidateInnovationPreview | None = None
    innovation_commitments: InnovationCommitments = Field(
        default_factory=InnovationCommitments
    )
    narrative_portfolio: NarrativePortfolioSnapshot | None = None
    innovation_trace: InnovationTrace | None = None
    effective_book_profile: dict[str, Any] = Field(default_factory=dict)
    active_author_truths: list[dict[str, Any]] = Field(default_factory=list)
    reveal_agenda: dict[str, Any] = Field(default_factory=dict)
    truth_reveal_commitments: dict[str, Any] = Field(default_factory=dict)
    reader_promise_alignment: list[ReaderPromiseAlignment] = Field(default_factory=list)
    genre_alignment: list[str] = Field(default_factory=list)
    narrative_drive_alignment: NarrativeDriveAlignment = Field(
        default_factory=NarrativeDriveAlignment
    )
    progress_preview: ProgressPreview | None = None
    progression_impact: ProgressionImpact = Field(default_factory=ProgressionImpact)
    payoff_channel_impact: list[str] = Field(default_factory=list)
    world_expansion_impact: list[str] = Field(default_factory=list)
    resource_opportunity_impact: list[str] = Field(default_factory=list)
    chapter_intent: str | None = None
    scheduler_alignment: SchedulerAlignment = Field(default_factory=SchedulerAlignment)
    progression_debt_impact: list[str] = Field(default_factory=list)
    anticipation_impact: list[str] = Field(default_factory=list)
    genre_drift_diagnostic: dict[str, Any] = Field(default_factory=dict)
    genre_evolution_diagnostic: dict[str, Any] = Field(default_factory=dict)
    narrative_drive_drift_diagnostic: dict[str, Any] = Field(default_factory=dict)
    declared_kernel_trace: dict[str, Any] = Field(default_factory=dict)
    verified_kernel_trace: dict[str, Any] = Field(default_factory=dict)
    kernel_verification_status: str = "LEGACY_NO_EFFECTIVE_CONTRACT"
    experience_target: ChapterExperienceSignature = Field(
        default_factory=ChapterExperienceSignature
    )
    outcome_magnitude_target: str = ""
    action_space_delta_target: str = ""
    dramatization_targets: list[str] = Field(default_factory=list)
    realization_scope: str = "CONTRACT_BOUND"
    reference_provenance: PlanningReferenceProvenance = Field(
        default_factory=PlanningReferenceProvenance
    )
