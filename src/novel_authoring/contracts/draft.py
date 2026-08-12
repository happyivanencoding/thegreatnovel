from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.author_control.reveal import RevealTrace
from novel_authoring.planning.innovation import (
    InnovationControl,
    InnovationDirectionAlignment,
    InnovationTrace,
)
from novel_authoring.planning.models import ProgressionImpact

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
    evidence_quotes: list[str] = Field(min_length=1)


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


class DraftOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    contract_id: str
    chapter_title: str
    prose_markdown: str = Field(min_length=1)
    state_changes: list[DraftStateChange] = Field(min_length=1)
    contract_evidence: dict[str, list[str]]
    knowledge_claims: list[KnowledgeClaim] = Field(default_factory=list)
    reveal_trace: RevealTrace = Field(default_factory=RevealTrace)
    character_fit_inputs: dict[str, float]
    style_fit_inputs: dict[str, float]
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
    notes: list[str] = Field(default_factory=list)
