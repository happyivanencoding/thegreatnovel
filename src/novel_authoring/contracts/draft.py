from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.author_control.reveal import RevealTrace
from novel_authoring.continuation_quality import ProgressionDelta, ReaderVisibleClaim
from novel_authoring.planning.innovation import (
    InnovationControl,
    InnovationDirectionAlignment,
    InnovationTrace,
)
from novel_authoring.planning.models import (
    ChapterExperienceSignature,
    PlanningReferenceProvenance,
    ProgressionImpact,
)

StateChangeKind = Literal[
    "fact",
    "timeline",
    "character_state",
    "knowledge",
    "relationship",
    "resource",
    "capability",
    "thread",
    "promise",
    "payoff",
    "repetition",
    "style",
]


class DraftStateChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: StateChangeKind
    record_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    payload: dict[str, Any]
    # Evidence is compiled from the prose.  An empty list is a hard failure for
    # an actual StateChange; contract locator evidence remains soft.
    evidence_quotes: list[str] = Field(default_factory=list)


class DraftCreativeStateChange(BaseModel):
    """The small state-change declaration an executor may submit."""

    model_config = ConfigDict(extra="forbid")

    kind: StateChangeKind
    record_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    payload: dict[str, Any] = Field(default_factory=dict)


class KnowledgeClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    character_id: str
    fact_id: str
    basis: Literal["already_known", "learned_in_draft"]


class RealizedKernelEvidence(BaseModel):
    """Evidence binding a realized Kernel claim to approved-state candidates."""

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(min_length=1)
    state_change_record_ids: list[str] = Field(min_length=1)
    evidence_quotes: list[str] = Field(min_length=1)


class RealizedKernelTrace(BaseModel):
    """What the draft actually realizes; validators compare it with the contract."""

    model_config = ConfigDict(extra="forbid")

    expected_contract_id: str
    primary_intent: str | None = None
    reader_promises_served: list[str] = Field(default_factory=list)
    narrative_drives_advanced: list[str] = Field(default_factory=list)
    progression_impact: ProgressionImpact = Field(default_factory=ProgressionImpact)
    resource_changes: list[str] = Field(default_factory=list)
    world_expansion_changes: list[str] = Field(default_factory=list)
    payoff_channels_realized: list[str] = Field(default_factory=list)
    debts_advanced: list[str] = Field(default_factory=list)
    debts_paid: list[str] = Field(default_factory=list)
    evidence: list[RealizedKernelEvidence] = Field(default_factory=list)


class ChapterRealizationBrief(BaseModel):
    """Soft expression guidance frozen before prose generation.

    The range is advisory.  It never becomes a word-count hard gate and does
    not authorize a new Canon event outside the Chapter Contract.
    """

    model_config = ConfigDict(extra="forbid")

    target_word_range: tuple[int, int] = (0, 0)
    target_scene_count: int = Field(default=1, ge=1)
    dramatization_targets: list[str] = Field(default_factory=list)
    realization_scope: str = "CONTRACT_BOUND"
    contract_realization_status: Literal["SUFFICIENT", "UNDERSPECIFIED", "UNKNOWN"] = "UNKNOWN"
    adaptive: bool = True
    micro_event_rule: str = (
        "允许只改变人物感知、动作或场面反应的 realization-only micro-event；"
        "不得改变 Contract、Canon、Knowledge、Resource 或 Capability。"
    )


class DraftCreativeOutput(BaseModel):
    """LLM-facing prose output; system audits are intentionally absent."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    contract_id: str
    chapter_title: str
    prose_markdown: str = Field(min_length=1)
    state_changes: list[DraftCreativeStateChange] = Field(min_length=1)
    reader_visible_claims: list[ReaderVisibleClaim] = Field(default_factory=list)
    progression_deltas: list[ProgressionDelta] = Field(default_factory=list)
    knowledge_claims: list[KnowledgeClaim] = Field(default_factory=list)
    reveal_trace: RevealTrace = Field(default_factory=RevealTrace)
    promises_advanced: list[str] = Field(default_factory=list)
    promises_paid: list[str] = Field(default_factory=list)
    new_major_hooks: int = Field(default=0, ge=0)
    notes: list[str] = Field(default_factory=list)


class DraftOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    contract_id: str
    chapter_title: str
    prose_markdown: str = Field(min_length=1)
    state_changes: list[DraftStateChange] = Field(min_length=1)
    reader_visible_claims: list[ReaderVisibleClaim] = Field(default_factory=list)
    progression_deltas: list[ProgressionDelta] = Field(default_factory=list)
    contract_evidence: dict[str, list[str]] = Field(default_factory=dict)
    knowledge_claims: list[KnowledgeClaim] = Field(default_factory=list)
    reveal_trace: RevealTrace = Field(default_factory=RevealTrace)
    character_fit_inputs: dict[str, float] = Field(default_factory=dict)
    style_fit_inputs: dict[str, float] = Field(default_factory=dict)
    character_bottom_line_violations: list[str] = Field(default_factory=list)
    style_boundary_violations: list[str] = Field(default_factory=list)
    promises_advanced: list[str] = Field(default_factory=list)
    promises_paid: list[str] = Field(default_factory=list)
    new_major_hooks: int = Field(default=0, ge=0)
    structure_tags: list[str] = Field(default_factory=list)
    innovation_control: InnovationControl | None = None
    innovation_trace: InnovationTrace | None = None
    direction_alignment: InnovationDirectionAlignment | None = None
    realized_kernel_trace: RealizedKernelTrace | None = None
    chapter_experience_signature: ChapterExperienceSignature | None = None
    realization_diagnostics: dict[str, Any] = Field(default_factory=dict)
    realization_repair_count: int = Field(default=0, ge=0, le=1)
    reference_provenance: PlanningReferenceProvenance = Field(
        default_factory=PlanningReferenceProvenance
    )
    # Existing hand-authored DraftOutput fixtures retain their strict evidence
    # semantics.  The new compiler sets COMPILED_SOFT for normal continuation.
    evidence_policy: Literal["STRICT_LEGACY", "COMPILED_SOFT"] = "STRICT_LEGACY"
    semantic_review_status: Literal["NOT_REQUESTED", "UNKNOWN", "REVIEWED"] = "UNKNOWN"
    deterministic_measurements: dict[str, Any] = Field(default_factory=dict)
    contract_surface_coverage: dict[str, Any] = Field(default_factory=dict)
    publication_review_findings: list[dict[str, Any]] = Field(default_factory=list)
    intentional_short_chapter: bool = False
    notes: list[str] = Field(default_factory=list)
