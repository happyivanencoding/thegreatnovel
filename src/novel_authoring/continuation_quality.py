"""Generic continuation-quality contracts.

These models describe claims made at the creative edge and the deterministic
checks that can be performed before the existing Canon approval boundary.
They do not own Canon, chapter state, or a second persistence layer.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


class ReaderClaimKind(StrEnum):
    STATE = "STATE"
    ENTITY_STATE = "ENTITY_STATE"
    QUANTITY = "QUANTITY"
    LOCATION = "LOCATION"
    OWNERSHIP = "OWNERSHIP"
    CAPABILITY = "CAPABILITY"
    CAPABILITY_STATE = "CAPABILITY_STATE"
    CAPABILITY_USE = "CAPABILITY_USE"
    KNOWLEDGE = "KNOWLEDGE"
    KNOWLEDGE_STATE = "KNOWLEDGE_STATE"
    RELATIONSHIP = "RELATIONSHIP"
    RELATIONSHIP_STATE = "RELATIONSHIP_STATE"
    TEMPORAL = "TEMPORAL"
    TEMPORAL_STATE = "TEMPORAL_STATE"
    WORLD = "WORLD"
    WORLD_STATE = "WORLD_STATE"
    AGENCY = "AGENCY"
    CUSTOM = "CUSTOM"


class ReaderClaimStatus(StrEnum):
    DECLARED = "DECLARED"
    OBSERVED = "OBSERVED"
    UNOBSERVED = "UNOBSERVED"
    CONFLICT = "CONFLICT"


class ReaderVisibleClaim(BaseModel):
    """A high-value reader-visible assertion supplied by the creative edge.

    ``value`` represents a stable observation.  ``before_value`` and
    ``after_value`` represent an explicit transition.  The claim is not a
    Canon fact until its normal StateChange has passed the existing approval
    workflow.
    """

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    subject_ref: str = Field(min_length=1)
    predicate: str = Field(min_length=1)
    value: Any | None = None
    value_type: str = "UNSPECIFIED"
    before_value: Any | None = None
    after_value: Any | None = None
    claim_kind: ReaderClaimKind = ReaderClaimKind.STATE
    temporal_scope: str = "CURRENT"
    evidence_quote: str = ""
    transition_source: str = ""
    confidence: float | None = Field(default=None, ge=0, le=1)
    status: ReaderClaimStatus = ReaderClaimStatus.DECLARED

    @model_validator(mode="after")
    def require_observable_value(self) -> ReaderVisibleClaim:
        if self.value is None and self.before_value is None and self.after_value is None:
            raise ValueError("ReaderVisibleClaim 必须提供 value 或 before/after")
        if (self.before_value is None) != (self.after_value is None):
            raise ValueError("ReaderVisibleClaim 的 before_value 与 after_value 必须成对出现")
        return self


class ReferenceApplication(BaseModel):
    """Creative-edge evidence that a frozen reference was actually applied."""

    model_config = ConfigDict(extra="forbid")

    summary: str = ""
    applied_dimensions: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    conflict: bool = False


class ProgressionDeltaKind(StrEnum):
    REUSE = "REUSE"
    SHOWCASE = "SHOWCASE"
    MASTERY = "MASTERY"
    UNLOCK = "UNLOCK"
    UPGRADE = "UPGRADE"
    BREAKTHROUGH = "BREAKTHROUGH"
    STAGE_TRANSITION = "STAGE_TRANSITION"
    LOSS = "LOSS"
    TRADEOFF = "TRADEOFF"
    NEW_CAPABILITY = "NEW_CAPABILITY"
    RESOURCE_CHANGE = "RESOURCE_CHANGE"
    KNOWLEDGE_UPDATE = "KNOWLEDGE_UPDATE"
    RELATIONSHIP_SHIFT = "RELATIONSHIP_SHIFT"
    WORLD_STATE_CHANGE = "WORLD_STATE_CHANGE"
    CUSTOM = "CUSTOM"


class ProgressionDelta(BaseModel):
    """Before/after evidence for any progression axis, not only combat power."""

    model_config = ConfigDict(extra="forbid")

    delta_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    subject_ref: str = Field(
        min_length=1,
        validation_alias=AliasChoices("subject_ref", "subject_id"),
    )
    axis: str = Field(
        min_length=1,
        validation_alias=AliasChoices("axis", "axis_id"),
    )
    kind: ProgressionDeltaKind = Field(
        validation_alias=AliasChoices("kind", "delta_type")
    )
    before_state: str = ""
    after_state: str = ""
    reader_visible_delta: str = ""
    opened_actions: list[str] = Field(default_factory=list)
    new_action_opened: str = ""
    scope_change: str = ""
    reliability_change: str = ""
    cost_change: str = ""
    evidence_quotes: list[str] = Field(default_factory=list)
    source: str = ""


class UsageConstraint(BaseModel):
    """A generic bounded-use rule attached to a resource/capability change.

    A chapter boundary is not a reset.  ``reset_condition`` must be satisfied
    by an explicit state change or event context before the counter can fall.
    """

    model_config = ConfigDict(extra="forbid")

    constraint_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    subject_ref: str = Field(
        min_length=1,
        validation_alias=AliasChoices("subject_ref", "subject_id"),
    )
    action: str = Field(
        min_length=1,
        validation_alias=AliasChoices("action", "action_type"),
    )
    period: str = Field(
        default="CUSTOM",
        validation_alias=AliasChoices("period", "period_kind"),
    )
    period_key: str = Field(
        default="",
        validation_alias=AliasChoices("period_key", "period_id"),
    )
    limit: int | None = Field(default=None, ge=0)
    used_before: int = Field(default=0, ge=0)
    uses: int = Field(default=1, ge=0)
    used_after: int | None = Field(default=None, ge=0)
    used_count: int | None = Field(default=None, ge=0)
    remaining_count: int | None = Field(default=None, ge=0)
    reset_condition: str = ""
    last_used_at: str = ""
    source_contract_id: str = ""
    resource_ref: str = Field(
        default="",
        validation_alias=AliasChoices("resource_ref", "resource_id"),
    )
    resource_cost: float | None = Field(default=None, ge=0)
    evidence_quote: str = ""

    @property
    def subject_id(self) -> str:
        return self.subject_ref

    @property
    def action_type(self) -> str:
        return self.action

    @property
    def period_kind(self) -> str:
        return self.period

    @property
    def period_id(self) -> str:
        return self.period_key


class QualityIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    severity: Literal["ERROR", "WARNING"] = "ERROR"
    location: str = "continuation_quality"


STRUCTURAL_EXPERIENCE_FIELDS: tuple[str, ...] = (
    "opposition_source",
    "primary_subject",
    "choice_type",
    "cost_type",
    "protagonist_strategy",
    "solution_method",
    "payoff_channel",
    "progression_delta_type",
    "reader_visible_delta",
    "event_source",
    "social_feedback",
    "relationship_delta",
    "knowledge_delta",
    "world_scale_delta",
    "scene_topology",
    "emotional_outcome",
    "ending_action",
    "ending_mode",
)


def _normalized(value: object) -> str:
    return " ".join(str(value or "").casefold().split())


def progression_delta_issues(
    deltas: list[ProgressionDelta], *, location: str = "progression_deltas"
) -> list[QualityIssue]:
    """Validate the distinction between reuse/showcase and actual growth."""

    issues: list[QualityIssue] = []
    for delta in deltas:
        before = _normalized(delta.before_state)
        after = _normalized(delta.after_state)
        if delta.kind in {ProgressionDeltaKind.REUSE, ProgressionDeltaKind.SHOWCASE}:
            if before and after and before != after:
                issues.append(
                    QualityIssue(
                        code="PROGRESSION_REUSE_CHANGES_STATE",
                        message=(
                            f"{delta.delta_id} 声明为 {delta.kind.value}，但 before/after 已变化；"
                            "请改为 UPGRADE、BREAKTHROUGH 或其他实际变化类型。"
                        ),
                        location=f"{location}:{delta.delta_id}",
                    )
                )
            if not delta.reader_visible_delta:
                issues.append(
                    QualityIssue(
                        code="PROGRESSION_REUSE_NOT_READER_VISIBLE",
                        message=f"{delta.delta_id} 的复用/展示没有读者可见变化。",
                        severity="WARNING",
                        location=f"{location}:{delta.delta_id}",
                    )
                )
        elif delta.kind in {
            ProgressionDeltaKind.UPGRADE,
            ProgressionDeltaKind.BREAKTHROUGH,
            ProgressionDeltaKind.STAGE_TRANSITION,
            ProgressionDeltaKind.MASTERY,
            ProgressionDeltaKind.UNLOCK,
            ProgressionDeltaKind.NEW_CAPABILITY,
        }:
            missing = [
                name
                for name, value in (
                    ("before_state", before),
                    ("after_state", after),
                    ("reader_visible_delta", _normalized(delta.reader_visible_delta)),
                )
                if not value
            ]
            if missing:
                issues.append(
                    QualityIssue(
                        code="PROGRESSION_DELTA_INCOMPLETE",
                        message=f"{delta.delta_id} 的成长变化缺少：{', '.join(missing)}。",
                        location=f"{location}:{delta.delta_id}",
                    )
                )
            if delta.kind is ProgressionDeltaKind.BREAKTHROUGH and not (
                delta.opened_actions
                or delta.new_action_opened
                or delta.scope_change
                or delta.reliability_change
            ):
                issues.append(
                    QualityIssue(
                        code="BREAKTHROUGH_ACTION_SPACE_UNCHANGED",
                        message=(
                            f"{delta.delta_id} 声明突破，但没有新增行动空间、"
                            "范围或可靠性证据。"
                        ),
                        location=f"{location}:{delta.delta_id}",
                    )
                )
        if delta.kind is ProgressionDeltaKind.TRADEOFF and not delta.cost_change:
            issues.append(
                QualityIssue(
                    code="PROGRESSION_TRADEOFF_COST_MISSING",
                    message=f"{delta.delta_id} 声明 trade-off，但没有 cost_change。",
                    location=f"{location}:{delta.delta_id}",
                )
            )
    return issues


def usage_constraint_issues(
    constraint: UsageConstraint,
    *,
    resource_quantity: float | None = None,
    reset_observed: bool = False,
    location: str = "usage_constraints",
) -> list[QualityIssue]:
    """Check bounded use without treating a new chapter as an implicit reset."""

    issues: list[QualityIssue] = []
    used_after = (
        constraint.used_after
        if constraint.used_after is not None
        else (
            constraint.used_count
            if constraint.used_count is not None
            else constraint.used_before + constraint.uses
        )
    )
    period = constraint.period.upper()
    limit = constraint.limit
    if period == "ONE_TIME":
        limit = 1 if limit is None else limit
    if used_after < constraint.used_before and not reset_observed:
        issues.append(
            QualityIssue(
                code="USAGE_RESET_UNDECLARED",
                message=(
                    f"{constraint.constraint_id} 的 {period} 使用次数下降，"
                    "但没有观察到满足 reset_condition 的显式状态变化。"
                ),
                location=f"{location}:{constraint.constraint_id}",
            )
        )
    if limit is not None and used_after > limit and not reset_observed:
        issues.append(
            QualityIssue(
                code="PERIODIC_USAGE_LIMIT_EXCEEDED",
                message=(
                    f"{constraint.constraint_id} 在 {period} 周期内使用 {used_after} 次，"
                    f"超过 limit={limit}；新章节不会自动重置。"
                ),
                location=f"{location}:{constraint.constraint_id}",
            )
        )
    if (
        limit is not None
        and constraint.remaining_count is not None
        and constraint.remaining_count != max(0, limit - used_after)
    ):
        issues.append(
            QualityIssue(
                code="USAGE_REMAINING_COUNT_MISMATCH",
                message=(
                    f"{constraint.constraint_id} 的 remaining_count 与 limit-used_count 不一致。"
                ),
                location=f"{location}:{constraint.constraint_id}",
            )
        )
    if (
        period == "RESOURCE_GATED"
        and constraint.resource_cost is not None
        and resource_quantity is not None
        and constraint.resource_cost > resource_quantity
    ):
        issues.append(
            QualityIssue(
                code="USAGE_RESOURCE_GATE_EXCEEDED",
                message=(
                    f"{constraint.constraint_id} 需要资源 {constraint.resource_cost:g}，"
                    f"但当前只有 {resource_quantity:g}。"
                ),
                location=f"{location}:{constraint.constraint_id}",
            )
        )
    return issues


def structural_overlap(
    candidate: Mapping[str, object], recent: Mapping[str, object]
) -> dict[str, object]:
    """Compare structural experience dimensions instead of surface labels."""

    same = [
        field
        for field in STRUCTURAL_EXPERIENCE_FIELDS
        if _normalized(candidate.get(field))
        and _normalized(candidate.get(field)) == _normalized(recent.get(field))
    ]
    critical = {
        "opposition_source",
        "choice_type",
        "cost_type",
        "payoff_channel",
        "progression_delta_type",
    }
    critical_same = sorted(critical.intersection(same))
    progression_blank = not _normalized(
        candidate.get("progression_delta_type")
    ) and not _normalized(recent.get("progression_delta_type"))
    core_same = (
        _normalized(candidate.get("primary_subject"))
        and _normalized(candidate.get("primary_subject"))
        == _normalized(recent.get("primary_subject"))
        and _normalized(candidate.get("solution_method"))
        and _normalized(candidate.get("solution_method"))
        == _normalized(recent.get("solution_method"))
        and _normalized(candidate.get("payoff_channel"))
        and _normalized(candidate.get("payoff_channel"))
        == _normalized(recent.get("payoff_channel"))
        and _normalized(candidate.get("ending_action") or candidate.get("ending_mode"))
        == _normalized(recent.get("ending_action") or recent.get("ending_mode"))
        and _normalized(candidate.get("opposition_source"))
        == _normalized(recent.get("opposition_source"))
        and progression_blank
    )
    repeated = core_same or len(critical_same) >= 3 or (
        {"opposition_source", "choice_type", "payoff_channel"}.issubset(same)
    )
    return {
        "same_dimensions": same,
        "critical_same_dimensions": critical_same,
        "different_dimensions": [
            field for field in STRUCTURAL_EXPERIENCE_FIELDS if field not in same
        ],
        "repeated": repeated,
    }


__all__ = [
    "STRUCTURAL_EXPERIENCE_FIELDS",
    "ProgressionDelta",
    "ProgressionDeltaKind",
    "QualityIssue",
    "ReaderClaimKind",
    "ReaderClaimStatus",
    "ReaderVisibleClaim",
    "ReferenceApplication",
    "UsageConstraint",
    "progression_delta_issues",
    "structural_overlap",
    "usage_constraint_issues",
]
