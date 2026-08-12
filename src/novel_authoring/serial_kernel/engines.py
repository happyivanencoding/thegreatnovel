"""Narrative engine adapter protocol and the first deep implementation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.progression.models import PayoffChannel
from novel_authoring.serial_kernel.models import (
    EngineImplementationDepth,
    NarrativeDrive,
    NarrativeEngineType,
)


class EngineIntentRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engine_type: NarrativeEngineType
    drive: NarrativeDrive
    intent: str
    priority: float = Field(ge=0, le=100)
    why_now: list[str] = Field(min_length=1)
    debt_ids: list[str] = Field(default_factory=list)
    reader_promises: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class EngineCandidateEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engine_type: NarrativeEngineType
    drives_advanced: list[NarrativeDrive] = Field(default_factory=list)
    effect: str = ""
    evidence: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class EngineValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


@runtime_checkable
class NarrativeEngineAdapter(Protocol):
    engine_type: NarrativeEngineType
    supported_drives: frozenset[NarrativeDrive]
    implementation_depth: EngineImplementationDepth

    def build_state(self, context: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def recommend_intents(
        self, context: Mapping[str, Any]
    ) -> Sequence[EngineIntentRecommendation]: ...

    def evaluate_candidate(
        self, candidate: Mapping[str, Any]
    ) -> EngineCandidateEvaluation: ...

    def produce_payoff_channels(
        self, context: Mapping[str, Any]
    ) -> Sequence[PayoffChannel]: ...

    def produce_debts(
        self, context: Mapping[str, Any]
    ) -> Sequence[Mapping[str, Any]]: ...

    def validate_candidate(
        self, candidate: Mapping[str, Any]
    ) -> EngineValidationResult: ...

    def render_author_summary(self, context: Mapping[str, Any]) -> str: ...


class ProgressionNarrativeEngineAdapter:
    """Expose existing PWK projections without becoming another authority."""

    engine_type = NarrativeEngineType.PROGRESSION
    supported_drives = frozenset(
        {
            NarrativeDrive.POWER_PROGRESSION,
            NarrativeDrive.KNOWLEDGE_PROGRESSION,
            NarrativeDrive.ABILITY_PROGRESSION,
            NarrativeDrive.BODY_EVOLUTION,
            NarrativeDrive.SEQUENCE_PROGRESSION,
            NarrativeDrive.STATUS_PROGRESSION,
        }
    )
    implementation_depth = EngineImplementationDepth.DEEP

    def build_state(self, context: Mapping[str, Any]) -> Mapping[str, Any]:
        value = context.get("progression_state")
        if isinstance(value, Mapping):
            return value
        return {
            "availability": "UNKNOWN",
            "source_layer": "CHAPTER_WORLD_STATE_PROJECTION",
            "reason": "当前章节没有可验证的 Progression State",
        }

    def recommend_intents(
        self, context: Mapping[str, Any]
    ) -> Sequence[EngineIntentRecommendation]:
        state = self.build_state(context)
        drive = NarrativeDrive(str(context.get("drive", "POWER_PROGRESSION")))
        promises = [str(item) for item in context.get("reader_promises", [])]
        debts = [str(item) for item in context.get("debt_ids", [])]
        evidence = [str(item) for item in context.get("evidence", [])]
        readiness = str(state.get("next_breakthrough_readiness", "UNKNOWN"))
        missing_resources = [str(item) for item in state.get("missing_resources", [])]
        pending_showcases = [
            str(item) for item in state.get("pending_ability_showcases", [])
        ]
        if readiness in {"GATE_SATISFIED", "READY_TO_ATTEMPT"}:
            intent, priority, reason = (
                "BREAKTHROUGH",
                86.0,
                "已确认门槛具备可验证的突破条件",
            )
        elif pending_showcases:
            intent, priority, reason = (
                "POWER_VERIFICATION",
                78.0,
                "已有能力仍缺少改变解决方法的场景验证",
            )
        elif missing_resources:
            intent, priority, reason = (
                "RESOURCE_OPPORTUNITY",
                72.0,
                "下一成长门槛缺少已确认资源",
            )
        else:
            intent, priority, reason = (
                "PROGRESSION_SETUP",
                58.0,
                "保持成长因果与下一层期待可见",
            )
        return [
            EngineIntentRecommendation(
                engine_type=self.engine_type,
                drive=drive,
                intent=intent,
                priority=priority,
                why_now=[reason],
                debt_ids=debts,
                reader_promises=promises,
                evidence=evidence,
                risks=(
                    ["资源门槛缺少证据，不能把机会写成已拥有"]
                    if missing_resources
                    else []
                ),
            )
        ]

    def evaluate_candidate(
        self, candidate: Mapping[str, Any]
    ) -> EngineCandidateEvaluation:
        impact = candidate.get("progression_impact")
        if not isinstance(impact, Mapping):
            impact = {}
        axis = [str(item) for item in impact.get("axis_advanced", [])]
        evidence = [str(item) for item in impact.get("evidence", [])]
        return EngineCandidateEvaluation(
            engine_type=self.engine_type,
            drives_advanced=(
                [NarrativeDrive.POWER_PROGRESSION] if axis else []
            ),
            effect="；".join(axis),
            evidence=evidence,
            warnings=([] if axis or evidence else ["候选尚未声明结构化成长影响"]),
        )

    def produce_payoff_channels(
        self, context: Mapping[str, Any]
    ) -> Sequence[PayoffChannel]:
        values: list[PayoffChannel] = []
        for value in context.get("payoff_channels", []):
            try:
                values.append(PayoffChannel(str(value)))
            except ValueError:
                continue
        return values

    def produce_debts(
        self, context: Mapping[str, Any]
    ) -> Sequence[Mapping[str, Any]]:
        values = context.get("progression_debts", [])
        return [item for item in values if isinstance(item, Mapping)]

    def validate_candidate(
        self, candidate: Mapping[str, Any]
    ) -> EngineValidationResult:
        evaluation = self.evaluate_candidate(candidate)
        return EngineValidationResult(
            valid=True,
            warnings=evaluation.warnings,
        )

    def render_author_summary(self, context: Mapping[str, Any]) -> str:
        state = self.build_state(context)
        readiness = str(state.get("next_breakthrough_readiness", "UNKNOWN"))
        missing = len(state.get("missing_resources", []))
        showcases = len(state.get("pending_ability_showcases", []))
        return f"成长准备度：{readiness}；缺少资源 {missing}；待验证能力 {showcases}"


class NarrativeEngineRegistry:
    def __init__(self) -> None:
        self._adapters: dict[NarrativeEngineType, NarrativeEngineAdapter] = {}
        self._depths: dict[NarrativeEngineType, EngineImplementationDepth] = {
            engine: EngineImplementationDepth.NOT_IMPLEMENTED_DEEPLY
            for engine in NarrativeEngineType
        }

    def register(self, adapter: NarrativeEngineAdapter) -> None:
        self._adapters[adapter.engine_type] = adapter
        self._depths[adapter.engine_type] = adapter.implementation_depth

    def get(self, engine_type: NarrativeEngineType) -> NarrativeEngineAdapter | None:
        return self._adapters.get(engine_type)

    def implementation_depth(
        self, engine_type: NarrativeEngineType
    ) -> EngineImplementationDepth:
        return self._depths[engine_type]

    def summary(self) -> dict[str, str]:
        return {engine.value: self._depths[engine].value for engine in NarrativeEngineType}


NARRATIVE_ENGINE_REGISTRY = NarrativeEngineRegistry()
NARRATIVE_ENGINE_REGISTRY.register(ProgressionNarrativeEngineAdapter())


__all__ = [
    "EngineCandidateEvaluation",
    "EngineIntentRecommendation",
    "EngineValidationResult",
    "NARRATIVE_ENGINE_REGISTRY",
    "NarrativeEngineAdapter",
    "NarrativeEngineRegistry",
    "ProgressionNarrativeEngineAdapter",
]
