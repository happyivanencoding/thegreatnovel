"""Read-only reader anticipation surface derived from existing planning state."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.planning.innovation import NarrativeDebt, NarrativeDebtStatus
from novel_authoring.progression.models import (
    OpportunityStatus,
    OpportunitySurface,
    PayoffChannel,
    WorldExpansionStateView,
)


class AnticipationSource(StrEnum):
    NARRATIVE_DEBT = "NARRATIVE_DEBT"
    OPPORTUNITY = "OPPORTUNITY"
    REVEAL_AGENDA = "REVEAL_AGENDA"
    ACTIVE_THREAD = "ACTIVE_THREAD"
    WORLD_EXPANSION = "WORLD_EXPANSION"
    PAYOFF_READINESS = "PAYOFF_READINESS"


class AnticipationStatus(StrEnum):
    BUILDING = "BUILDING"
    MATURE = "MATURE"
    DELAYED = "DELAYED"
    SERVED = "SERVED"
    UNKNOWN = "UNKNOWN"


class AnticipationItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    anticipation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    subject: str = Field(min_length=1)
    source: AnticipationSource
    source_reference_id: str
    maturity: float | None = Field(default=None, ge=0, le=1)
    urgency: int = Field(default=1, ge=1, le=5)
    expected_payoff_channel: PayoffChannel
    expected_horizon: str
    last_served: int | None = Field(default=None, ge=0)
    risk_if_delayed: str
    status: AnticipationStatus = AnticipationStatus.BUILDING
    evidence: list[str] = Field(default_factory=list)


class AnticipationSurfaceView(BaseModel):
    """A projection that cannot create or update Canon."""

    model_config = ConfigDict(extra="forbid")

    chapter_id: str
    chapter_ordinal: int = Field(ge=0)
    items: list[AnticipationItem] = Field(default_factory=list)
    projection_only: bool = True
    canon_mutation_allowed: bool = False


def _debt_urgency(debt: NarrativeDebt) -> int:
    if debt.status is NarrativeDebtStatus.OVERDUE:
        return 5
    if debt.status is NarrativeDebtStatus.PAYOFF_READY:
        return 4
    if debt.debt_score is not None and debt.debt_score >= 40:
        return 3
    return 2


def _mapping_item(
    value: Mapping[str, Any],
    *,
    prefix: str,
    index: int,
    source: AnticipationSource,
    channel: PayoffChannel,
) -> AnticipationItem | None:
    subject = str(
        value.get("subject")
        or value.get("question")
        or value.get("statement")
        or value.get("name")
        or ""
    ).strip()
    if not subject:
        return None
    reference = str(
        value.get("id")
        or value.get("thread_id")
        or value.get("truth_id")
        or f"{prefix}-{index}"
    )
    return AnticipationItem(
        anticipation_id=f"anticipation-{prefix}-{index}",
        subject=subject,
        source=source,
        source_reference_id=reference,
        maturity=None,
        urgency=int(value.get("urgency") or 3),
        expected_payoff_channel=channel,
        expected_horizon=str(value.get("horizon") or "MID"),
        last_served=(
            int(value["last_served"]) if value.get("last_served") is not None else None
        ),
        risk_if_delayed=str(value.get("risk_if_delayed") or "读者期待继续积累"),
        evidence=[str(item) for item in value.get("evidence", [])]
        if isinstance(value.get("evidence"), list)
        else [],
    )


def build_anticipation_surface(
    *,
    chapter_id: str,
    chapter_ordinal: int,
    debts: Sequence[NarrativeDebt] = (),
    opportunities: OpportunitySurface | None = None,
    reveal_agenda: Sequence[Mapping[str, Any]] = (),
    active_threads: Sequence[Mapping[str, Any]] = (),
    world_expansion: WorldExpansionStateView | None = None,
    payoff_readiness: Sequence[Mapping[str, Any]] = (),
) -> AnticipationSurfaceView:
    items: list[AnticipationItem] = []
    for debt in debts:
        items.append(
            AnticipationItem(
                anticipation_id=f"anticipation-debt-{debt.debt_id}",
                subject=debt.question_or_promise,
                source=AnticipationSource.NARRATIVE_DEBT,
                source_reference_id=debt.debt_id,
                maturity=(
                    min(1.0, (debt.debt_score or 0) / 100)
                    if debt.debt_score is not None
                    else None
                ),
                urgency=_debt_urgency(debt),
                expected_payoff_channel=(
                    PayoffChannel.NEW_ABILITY
                    if debt.debt_type.value == "POWER_SHOWCASE"
                    else PayoffChannel.CUSTOM
                ),
                expected_horizon=debt.horizon.value,
                last_served=debt.last_advanced or None,
                risk_if_delayed="既有承诺继续累积债务",
                status=(
                    AnticipationStatus.DELAYED
                    if debt.status is NarrativeDebtStatus.OVERDUE
                    else AnticipationStatus.MATURE
                    if debt.status is NarrativeDebtStatus.PAYOFF_READY
                    else AnticipationStatus.BUILDING
                ),
                evidence=debt.evidence,
            )
        )
    if opportunities is not None:
        for opportunity in opportunities.items:
            items.append(
                AnticipationItem(
                    anticipation_id=f"anticipation-opportunity-{opportunity.opportunity_id}",
                    subject=opportunity.subject,
                    source=AnticipationSource.OPPORTUNITY,
                    source_reference_id=opportunity.opportunity_id,
                    urgency=(
                        4 if opportunity.status is OpportunityStatus.PREPARED else 3
                    ),
                    expected_payoff_channel=PayoffChannel.RESOURCE_GAIN,
                    expected_horizon="SHORT",
                    risk_if_delayed="已铺垫机会长期未回收",
                    evidence=[proof.statement for proof in opportunity.evidence],
                )
            )
    for prefix, values, source, channel in (
        (
            "reveal",
            reveal_agenda,
            AnticipationSource.REVEAL_AGENDA,
            PayoffChannel.MYSTERY_REVEAL,
        ),
        (
            "thread",
            active_threads,
            AnticipationSource.ACTIVE_THREAD,
            PayoffChannel.CUSTOM,
        ),
        (
            "payoff",
            payoff_readiness,
            AnticipationSource.PAYOFF_READINESS,
            PayoffChannel.CUSTOM,
        ),
    ):
        for index, value in enumerate(values, start=1):
            item = _mapping_item(
                value,
                prefix=prefix,
                index=index,
                source=source,
                channel=channel,
            )
            if item is not None:
                items.append(item)
    if world_expansion is not None and world_expansion.next_stage_candidates:
        next_stage = world_expansion.next_stage_candidates[0]
        items.append(
            AnticipationItem(
                anticipation_id=f"anticipation-world-{next_stage.stage_id}",
                subject=next_stage.reader_question,
                source=AnticipationSource.WORLD_EXPANSION,
                source_reference_id=next_stage.stage_id,
                urgency=3,
                expected_payoff_channel=PayoffChannel.WORLD_EXPANSION,
                expected_horizon="LONG",
                risk_if_delayed="世界长期没有打开新的可能性",
                evidence=world_expansion.transition_conditions,
            )
        )
    return AnticipationSurfaceView(
        chapter_id=chapter_id,
        chapter_ordinal=chapter_ordinal,
        items=sorted(items, key=lambda item: (-item.urgency, item.anticipation_id)),
    )


__all__ = [
    "AnticipationItem",
    "AnticipationSource",
    "AnticipationStatus",
    "AnticipationSurfaceView",
    "build_anticipation_surface",
]
