"""Progression debt bridge to the existing deterministic debt formula."""

from __future__ import annotations

from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.metrics.formulas import narrative_debt
from novel_authoring.planning.innovation import (
    DebtResolutionMode,
    NarrativeDebt,
    NarrativeDebtStatus,
    NarrativeDebtType,
    NarrativeHorizon,
)


class ProgressionDebtInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    debt_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    debt_type: NarrativeDebtType
    question_or_promise: str
    horizon: NarrativeHorizon
    opened_chapter: int = Field(ge=0)
    current_chapter: int = Field(ge=0)
    target_max_age: int = Field(gt=0)
    importance: float = Field(ge=0, le=1)
    reader_visibility: float = Field(ge=0, le=1)
    promise_progress: float = Field(ge=0, le=1)
    reminder_count: int = Field(default=0, ge=0)
    source_event: str
    evidence: list[str] = Field(default_factory=list)
    allowed_resolution_modes: list[DebtResolutionMode] = Field(default_factory=list)


def score_progression_debt(
    value: ProgressionDebtInput,
    *,
    formula_config: Mapping[str, object],
) -> NarrativeDebt:
    """Use metrics.formulas.narrative_debt; this module adds no second formula."""

    result = narrative_debt(
        importance=value.importance,
        reader_visibility=value.reader_visibility,
        promise_progress=value.promise_progress,
        age_chapters=max(0, value.current_chapter - value.opened_chapter),
        target_max_age=value.target_max_age,
        reminder_count=value.reminder_count,
        config=formula_config,
    )
    status = (
        NarrativeDebtStatus.OVERDUE
        if result.score >= 110
        else NarrativeDebtStatus.PAYOFF_READY
        if result.score >= 80
        else NarrativeDebtStatus.ADVANCED
        if value.promise_progress > 0
        else NarrativeDebtStatus.OPEN
    )
    return NarrativeDebt(
        debt_id=value.debt_id,
        debt_type=value.debt_type,
        question_or_promise=value.question_or_promise,
        horizon=value.horizon,
        opened_chapter=value.opened_chapter,
        source_event=value.source_event,
        expected_payoff_window=f"within {value.target_max_age} chapters",
        maturity=result.threshold_interpretation,
        status=status,
        debt_score=result.score,
        metric_components=result.inputs,
        evidence=value.evidence,
        allowed_resolution_modes=value.allowed_resolution_modes,
    )


def can_resolve_power_showcase(mode: DebtResolutionMode) -> bool:
    """Power verification is event impact, not a combat quota."""

    return mode in set(DebtResolutionMode)


__all__ = [
    "ProgressionDebtInput",
    "can_resolve_power_showcase",
    "score_progression_debt",
]
