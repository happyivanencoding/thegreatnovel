from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.author_control.book_profile import (
    ProfileEditOperation,
    ProfileStrength,
)
from novel_authoring.author_control.models import (
    AuthorControlHorizon,
    AuthorIntentStatus,
    AuthorTaskLifecycle,
)
from novel_authoring.author_control.reveal import AgendaBucket, KnowledgeState, RevealDepth
from novel_authoring.author_control.truth import TruthCompatibilityEvidenceInput
from novel_authoring.metrics.models import MetricComponentStatus, ObservationSourceKind
from novel_authoring.original.models import OriginalCreativeSemantics
from novel_authoring.planning.innovation import InnovationFocus, InnovationLevel
from novel_authoring.progression.interpretation import (
    ReaderExperienceAdjustment,
    ReaderExperienceStrength,
)
from novel_authoring.serial_kernel.models import NarrativeDrive


class AuthorInputRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope_type: str = "CHAPTER"
    scope_id: str
    metric_id: str
    component_id: str
    value: Any | None = None
    status: MetricComponentStatus = MetricComponentStatus.AVAILABLE
    source_kind: ObservationSourceKind = ObservationSourceKind.AUTHOR_INPUT
    confidence: float | None = Field(default=None, ge=0, le=1)
    reason: str
    chapter_id: str | None = None
    effective_content_sha256: str | None = None
    projection_hash: str | None = None
    registry_hash: str | None = None
    config_hash: str | None = None
    expected_active_observation_id: str | None = None
    evidence_links: list[dict[str, Any]] = Field(default_factory=list)


class DraftContentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str = Field(min_length=1)
    expected_content_sha256: str | None = None


class HandoffRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requested_stage: str
    edition_id: str | None = None
    context_chapter_id: str | None = None
    author_goal: str | None = Field(default=None, max_length=2000)
    author_task_ids: list[str] = Field(default_factory=list, max_length=20)
    require_complete_metrics: bool = False
    innovation_level: InnovationLevel | None = None
    innovation_focus: list[InnovationFocus] | None = None
    save_as_book_default: bool = False
    revision_mode: Literal["AUTHOR_REVISION", "ALTERNATE_ROUTE"] | None = None
    edition_display_name: str | None = Field(default=None, max_length=120)


class EditionActivationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmed: bool


class RetractRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope_type: str = "CHAPTER"
    scope_id: str
    reason: str = "作者撤回"
    expected_active_observation_id: str | None = None


class RecomputeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope_type: str = "CHAPTER"
    scope_id: str
    requested_metric_ids: list[str] | None = None
    effective_content_sha256: str | None = None
    projection_hash: str | None = None
    registry_hash: str | None = None
    config_hash: str | None = None
    expected_effective_observation_ids: dict[str, str] = Field(default_factory=dict)


class UserResponseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    response: dict[str, Any]


class OriginalProposalImportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handoff_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")


class OriginalReaderExperienceConfirmationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    adjustment: ReaderExperienceAdjustment = ReaderExperienceAdjustment.CONFIRM
    priority_overrides: dict[str, ReaderExperienceStrength] = Field(default_factory=dict)
    primary_drive: NarrativeDrive
    secondary_drives: list[NarrativeDrive] = Field(default_factory=list, max_length=4)
    progression_engine_enabled: bool
    creative_semantics: OriginalCreativeSemantics


class OriginalCoreInnovationSelectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selected_primary_innovation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    optional_mix_notes: str = ""


class OriginalFoundationSelectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selected_foundation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")


class OriginalProposalVersionResolutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["REPLACE_CURRENT", "KEEP_CURRENT", "REJECT"]


class OriginalCandidateSelectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")


class OriginalDraftActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    draft_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    confirmation: str = ""


class AtlasActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_type: str
    target_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    expected_atlas_id: str | None = None
    expected_atlas_version: int | None = Field(default=None, ge=1)
    expected_manifest_hash: str | None = None


class AuthorIntentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent_type: str
    subject_type: str
    subject_id: str | None = None
    title: str
    description: str = ""
    horizon: AuthorControlHorizon = AuthorControlHorizon.MID
    priority: int = 100
    status: AuthorIntentStatus = AuthorIntentStatus.PLANNED
    target_chapter_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class AuthorTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    task_type: str = "AUTHOR_TASK"
    description: str = ""
    horizon: AuthorControlHorizon = AuthorControlHorizon.MID
    lifecycle_status: AuthorTaskLifecycle = AuthorTaskLifecycle.BACKLOG
    priority: int = 100
    subject_type: str | None = None
    subject_id: str | None = None
    context_chapter_id: str | None = None
    context_chapter_ordinal: int | None = None
    due_chapter_ordinal: int | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class BookProfileEditRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension: str
    operation: ProfileEditOperation = ProfileEditOperation.ADD
    content: str = ""
    strength: ProfileStrength = ProfileStrength.SUGGESTION
    reason: str = "作者编辑"


class BookProfileProposalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: str = "AUTHOR_REANALYSIS"
    proposed_baseline: dict[str, Any] | None = None
    summary: str = ""


class BookProfileProposalResolutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: str
    edited_baseline: dict[str, Any] | None = None


class ProfileReanalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_chapter_id: str | None = None


class KernelContractDiscoveryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_chapter_id: str | None = Field(
        default=None, pattern=r"^[A-Za-z0-9._:-]+$"
    )


class TruthCompatibilityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence: list[TruthCompatibilityEvidenceInput] = Field(default_factory=list)


class AuthorTruthUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    changes: dict[str, Any]


class OpenCreativeQuestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    question: str = Field(min_length=1)
    subject_type: str | None = None
    subject_id: str | None = None
    horizon: Literal["SHORT", "MID", "LONG"] = "LONG"


class SecretCandidateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    truth_type: str = "CUSTOM"
    subject_type: str | None = None
    subject_id: str | None = None
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    source: str = "INITIALIZATION_INFERRED"


class SecretCandidateResolutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: str
    effective_from_chapter: int | None = Field(default=None, ge=1)
    compatibility_evidence: list[dict[str, Any]] = Field(default_factory=list)


class KnowledgeUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    state: KnowledgeState
    chapter_ordinal: int | None = Field(default=None, ge=0)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    mode: str = "AUTHOR_PLANNING"
    character_id: str | None = None


class RevealAgendaOverrideRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_id: str
    chapter_ordinal: int = Field(ge=1)
    agenda_bucket: AgendaBucket
    reveal_depth: RevealDepth | None = None
    reason: str = "作者手动调整本章揭示安排"


class HiddenItemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    category: Literal["ITEM", "EQUIPMENT", "RESOURCE"] = "ITEM"
    description: str = ""
    effective_from_chapter: int = Field(ge=1)
    location_id: str | None = None
    owner_id: str | None = None
    horizon: Literal["SHORT", "MID", "LONG"] = "MID"
    priority: int = Field(default=100, ge=0)
    reveal_depth: RevealDepth = RevealDepth.HINT
    target_chapter_min: int | None = Field(default=None, ge=1)
    target_chapter_max: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def valid_reveal_window(self) -> HiddenItemRequest:
        if self.target_chapter_min is None and self.target_chapter_max is not None:
            raise ValueError("填写揭示窗口结束章时必须同时填写起始章")
        if (
            self.target_chapter_min is not None
            and self.target_chapter_max is not None
            and self.target_chapter_max < self.target_chapter_min
        ):
            raise ValueError("揭示窗口结束章不得早于起始章")
        return self


class ProgressionContractConfirmationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    effective_from_boundary: int = Field(ge=0)
    author_notes: str = "作者在成长工作台确认"
