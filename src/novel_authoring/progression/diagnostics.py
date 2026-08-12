"""Structural genre drift and evolution diagnostics."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class GenreChangeStatus(StrEnum):
    CLEAR = "CLEAR"
    GENRE_SKIN_ONLY = "GENRE_SKIN_ONLY"
    GENRE_DRIFT = "GENRE_DRIFT"
    GENRE_EVOLUTION = "GENRE_EVOLUTION"
    GENRE_EXPANSION = "GENRE_EXPANSION"
    GENRE_REPLACEMENT = "GENRE_REPLACEMENT"


class GenreStructureEvidence(BaseModel):
    """Remove-the-skin test expressed as causal structure, not name matching."""

    model_config = ConfigDict(extra="forbid")

    progression_gate_affects_causality: bool = False
    extraordinary_resource_affects_choice: bool = False
    ability_changes_solution: bool = False
    power_opens_space: bool = False
    mystery_changes_understanding: bool = False
    core_promise_preserved: bool = True
    delivery_channel_changed: bool = False
    new_channel_added: bool = False
    secondary_replaces_primary: bool = False
    theme_replaces_core: bool = False
    contradicts_core_promise: bool = False
    consecutive_core_misses: int = Field(default=0, ge=0)
    evidence: list[str] = Field(default_factory=list)

    @property
    def has_genre_causality(self) -> bool:
        return any(
            (
                self.progression_gate_affects_causality,
                self.extraordinary_resource_affects_choice,
                self.ability_changes_solution,
                self.power_opens_space,
                self.mystery_changes_understanding,
            )
        )


class GenreDriftDiagnostic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GenreChangeStatus
    warning: bool = False
    hard_failure: bool = False
    penalty: float = Field(default=0, ge=0)
    reasons: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class GenreEvolutionDiagnostic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GenreChangeStatus
    core_promise_preserved: bool
    explanation: str
    evidence: list[str] = Field(default_factory=list)


class GenreChangeDiagnostics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drift: GenreDriftDiagnostic
    evolution: GenreEvolutionDiagnostic


def diagnose_genre_change(value: GenreStructureEvidence) -> GenreChangeDiagnostics:
    """Distinguish structural replacement from a new way to serve the same promise."""

    if value.contradicts_core_promise:
        status = GenreChangeStatus.GENRE_REPLACEMENT
        drift = GenreDriftDiagnostic(
            status=status,
            warning=True,
            hard_failure=True,
            penalty=6,
            reasons=["CONTRADICTS_CORE_PROMISE"],
            evidence=value.evidence,
        )
    elif value.secondary_replaces_primary or value.theme_replaces_core:
        status = GenreChangeStatus.GENRE_REPLACEMENT
        drift = GenreDriftDiagnostic(
            status=status,
            warning=True,
            penalty=5,
            reasons=["副类型或主题正在取代已确认的核心 Reader Promise"],
            evidence=value.evidence,
        )
    elif not value.has_genre_causality:
        status = GenreChangeStatus.GENRE_SKIN_ONLY
        drift = GenreDriftDiagnostic(
            status=status,
            warning=True,
            penalty=4,
            reasons=["移除表层专名后，成长资源、能力与世界层级均不影响因果"],
            evidence=value.evidence,
        )
    elif not value.core_promise_preserved or value.consecutive_core_misses >= 3:
        status = GenreChangeStatus.GENRE_DRIFT
        drift = GenreDriftDiagnostic(
            status=status,
            warning=True,
            penalty=min(4.0, float(value.consecutive_core_misses)),
            reasons=["核心 Reader Promise 已连续多章缺少实质服务"],
            evidence=value.evidence,
        )
    else:
        status = GenreChangeStatus.CLEAR
        drift = GenreDriftDiagnostic(status=status, evidence=value.evidence)

    if value.core_promise_preserved and value.delivery_channel_changed:
        evolution_status = GenreChangeStatus.GENRE_EVOLUTION
        explanation = "核心可能性扩张承诺保留，兑现主体或方式发生结构变化"
    elif value.core_promise_preserved and value.new_channel_added:
        evolution_status = GenreChangeStatus.GENRE_EXPANSION
        explanation = "新增满足渠道，但原核心 Reader Promise 仍然存在"
    else:
        evolution_status = GenreChangeStatus.CLEAR
        explanation = "未检测到需要单独标记的 Genre Evolution"
    return GenreChangeDiagnostics(
        drift=drift,
        evolution=GenreEvolutionDiagnostic(
            status=evolution_status,
            core_promise_preserved=value.core_promise_preserved,
            explanation=explanation,
            evidence=value.evidence,
        ),
    )


__all__ = [
    "GenreChangeDiagnostics",
    "GenreChangeStatus",
    "GenreDriftDiagnostic",
    "GenreEvolutionDiagnostic",
    "GenreStructureEvidence",
    "diagnose_genre_change",
]
