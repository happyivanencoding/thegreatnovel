"""Soft diagnostics for long-running narrative drive balance."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.serial_kernel.models import NarrativeDrive


class NarrativeDriveDriftStatus(StrEnum):
    CLEAR = "CLEAR"
    SOFT_MISS = "SOFT_MISS"
    PRIMARY_DRIVE_DRIFT = "PRIMARY_DRIVE_DRIFT"
    SECONDARY_REPLACEMENT = "SECONDARY_REPLACEMENT"
    DRIVE_MIX_IMBALANCE = "DRIVE_MIX_IMBALANCE"
    AUTHOR_EVOLUTION = "AUTHOR_EVOLUTION"
    CONTRACT_CONTRADICTION = "CONTRACT_CONTRADICTION"


class NarrativeDriveStructureEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_drive: NarrativeDrive
    primary_drive_affects_causality: bool = False
    primary_drive_state_changed: bool = False
    primary_drive_only_in_exposition: bool = False
    consecutive_primary_misses: int = Field(default=0, ge=0)
    secondary_drive_replaces_primary: bool = False
    unrelated_to_all_confirmed_drives: bool = False
    drive_mix_long_term_imbalanced: bool = False
    contradicts_primary_drive: bool = False
    author_changed_contract: bool = False
    evidence: list[str] = Field(default_factory=list)


class NarrativeDriveDriftDiagnostic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: NarrativeDriveDriftStatus
    warning: bool = False
    hard_failure: bool = False
    reasons: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


def diagnose_narrative_drive_drift(
    value: NarrativeDriveStructureEvidence,
) -> NarrativeDriveDriftDiagnostic:
    """A single quiet chapter is legal; confirmed replacement is explicit."""

    if value.author_changed_contract:
        return NarrativeDriveDriftDiagnostic(
            status=NarrativeDriveDriftStatus.AUTHOR_EVOLUTION,
            reasons=["作者已显式改变 Narrative Drive Contract"],
            evidence=value.evidence,
        )
    if value.contradicts_primary_drive:
        return NarrativeDriveDriftDiagnostic(
            status=NarrativeDriveDriftStatus.CONTRACT_CONTRADICTION,
            warning=True,
            hard_failure=True,
            reasons=["候选明确违背已确认的 Primary Drive 承诺"],
            evidence=value.evidence,
        )
    if value.secondary_drive_replaces_primary:
        return NarrativeDriveDriftDiagnostic(
            status=NarrativeDriveDriftStatus.SECONDARY_REPLACEMENT,
            warning=True,
            reasons=["Secondary Drive 正在未经确认地取代 Primary Drive"],
            evidence=value.evidence,
        )
    if value.drive_mix_long_term_imbalanced:
        return NarrativeDriveDriftDiagnostic(
            status=NarrativeDriveDriftStatus.DRIVE_MIX_IMBALANCE,
            warning=True,
            reasons=["已确认的 Drive Mix 长期失衡"],
            evidence=value.evidence,
        )
    if value.consecutive_primary_misses >= 3 or value.primary_drive_only_in_exposition:
        return NarrativeDriveDriftDiagnostic(
            status=NarrativeDriveDriftStatus.PRIMARY_DRIVE_DRIFT,
            warning=True,
            reasons=["Primary Drive 连续多章没有推动事件或只停留在设定说明"],
            evidence=value.evidence,
        )
    if value.unrelated_to_all_confirmed_drives or not (
        value.primary_drive_affects_causality or value.primary_drive_state_changed
    ):
        return NarrativeDriveDriftDiagnostic(
            status=NarrativeDriveDriftStatus.SOFT_MISS,
            reasons=["本章未直接服务 Primary Drive；单章缺席不是硬失败"],
            evidence=value.evidence,
        )
    return NarrativeDriveDriftDiagnostic(
        status=NarrativeDriveDriftStatus.CLEAR,
        evidence=value.evidence,
    )


__all__ = [
    "NarrativeDriveDriftDiagnostic",
    "NarrativeDriveDriftStatus",
    "NarrativeDriveStructureEvidence",
    "diagnose_narrative_drive_drift",
]
