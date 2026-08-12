"""Compile declared Kernel claims into inputs for existing gates and metrics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.metrics.formulas import payoff_score, progress, resource_pressure
from novel_authoring.planning.models import (
    CandidateProposal,
    NarrativeDriveAlignment,
    ReaderPromiseService,
)
from novel_authoring.progression.context import KernelPlanningContext
from novel_authoring.progression.diagnostics import (
    GenreStructureEvidence,
    diagnose_genre_change,
)
from novel_authoring.serial_kernel.diagnostics import (
    NarrativeDriveStructureEvidence,
    diagnose_narrative_drive_drift,
)
from novel_authoring.serial_kernel.engines import NARRATIVE_ENGINE_REGISTRY
from novel_authoring.serial_kernel.models import NarrativeDrive, NarrativeEngineType


class EvidenceCompleteness(StrEnum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


class KernelHardGateCompilation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canon_conflicts: list[str] = Field(default_factory=list)
    timeline_conflicts: list[str] = Field(default_factory=list)
    knowledge_violations: list[str] = Field(default_factory=list)
    missing_causal_sources: list[str] = Field(default_factory=list)
    payoff_cooldown_violations: list[str] = Field(default_factory=list)
    capability_violations: list[str] = Field(default_factory=list)
    author_constraint_violations: list[str] = Field(default_factory=list)

    @property
    def hard_failures(self) -> list[str]:
        return list(
            dict.fromkeys(
                [
                    *self.canon_conflicts,
                    *self.timeline_conflicts,
                    *self.knowledge_violations,
                    *self.missing_causal_sources,
                    *self.payoff_cooldown_violations,
                    *self.capability_violations,
                    *self.author_constraint_violations,
                ]
            )
        )


class KernelEvidenceCompilation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_local_id: str
    declared: dict[str, Any]
    verified: dict[str, Any]
    differences: list[str] = Field(default_factory=list)
    verified_reader_promise_alignment: list[dict[str, Any]] = Field(default_factory=list)
    verified_drive_alignment: dict[str, Any] = Field(default_factory=dict)
    verified_progression_impact: dict[str, Any] = Field(default_factory=dict)
    verified_world_expansion_impact: list[str] = Field(default_factory=list)
    verified_resource_impact: list[dict[str, Any]] = Field(default_factory=list)
    verified_anticipation_impact: list[str] = Field(default_factory=list)
    verified_progress_components: dict[str, Any] = Field(default_factory=dict)
    hard_gate_compilation: KernelHardGateCompilation
    soft_metric_compilation: dict[str, Any] = Field(default_factory=dict)
    completeness: EvidenceCompleteness
    warnings: list[str] = Field(default_factory=list)


def _tokens(items: object) -> set[str]:
    if isinstance(items, Mapping):
        values = [item for item in items.values() if isinstance(item, Mapping)]
    elif isinstance(items, Sequence) and not isinstance(items, (str, bytes)):
        values = [item for item in items if isinstance(item, Mapping)]
    else:
        values = []
    result: set[str] = set()
    for item in values:
        for key in (
            "id",
            "resource_id",
            "object_id",
            "opportunity_id",
            "name",
            "title",
            "subject",
            "statement",
        ):
            value = str(item.get(key) or "").strip().casefold()
            if value:
                result.add(value)
    return result


def _matches(value: str, tokens: set[str]) -> bool:
    normalized = value.casefold()
    return any(token in normalized or normalized in token for token in tokens)


def _declared_trace(candidate: CandidateProposal) -> dict[str, Any]:
    return {
        "reader_promise_alignment": [
            item.model_dump(mode="json") for item in candidate.reader_promise_alignment
        ],
        "narrative_drive_alignment": candidate.narrative_drive_alignment.model_dump(
            mode="json"
        ),
        "progression_impact": candidate.progression_impact.model_dump(mode="json"),
        "resource_impact": candidate.resource_opportunity_impact,
        "world_expansion_impact": candidate.world_expansion_impact,
        "payoff_channel_impact": candidate.payoff_channel_impact,
        "anticipation_impact": candidate.anticipation_impact,
        "genre_drift": candidate.genre_drift_diagnostic,
        "genre_evolution": candidate.genre_evolution_diagnostic,
        "scheduler_alignment": candidate.scheduler_alignment.model_dump(mode="json"),
    }


class KernelEvidenceCompiler:
    """Adapter-only compiler; scoring and gate authority remain in existing modules."""

    def compile(
        self,
        context: KernelPlanningContext,
        candidate: CandidateProposal,
        metrics_config: Mapping[str, Any] | None = None,
    ) -> KernelEvidenceCompilation:
        context_payload = context.model_dump(mode="json")
        adapter = NARRATIVE_ENGINE_REGISTRY.get(NarrativeEngineType.PROGRESSION)
        if adapter is None:
            raise RuntimeError("Progression Narrative Engine Adapter 未注册")
        engine_validation = adapter.validate_candidate(
            candidate.model_dump(mode="json"),
            context_payload,
        )
        gate_values = dict(engine_validation.hard_gate_compilation)
        author_failures: list[str] = []
        warnings = list(engine_validation.warnings)
        differences: list[str] = []

        genre = context.effective_contracts.genre or {}
        promise_by_id = {
            str(item.get("promise_id")): item
            for item in genre.get("genre_promises", [])
            if isinstance(item, Mapping) and item.get("promise_id")
        }
        verified_reader: list[dict[str, Any]] = []
        for claim in candidate.reader_promise_alignment:
            promise = promise_by_id.get(claim.promise_id)
            if promise is None:
                message = f"Reader Promise ID 不属于 Effective Contract：{claim.promise_id}"
                author_failures.append(message)
                differences.append(message)
                continue
            status = "VERIFIED"
            if claim.service in {
                ReaderPromiseService.SERVED,
                ReaderPromiseService.PARTIALLY_SERVED,
            } and not claim.evidence:
                status = "UNVERIFIED"
                message = f"Reader Promise 服务声明缺少证据：{claim.promise_id}"
                warnings.append(message)
                differences.append(message)
            if (
                str(promise.get("strength")) == "CORE"
                and claim.service is ReaderPromiseService.CONTRADICTED
            ):
                message = f"候选明确违背 CORE Reader Promise：{claim.promise_id}"
                author_failures.append(message)
                differences.append(message)
                status = "CONFLICT"
            verified_reader.append(
                {
                    **claim.model_dump(mode="json"),
                    "contract_strength": promise.get("strength"),
                    "verification_status": status,
                }
            )
        core_ids = {
            promise_id
            for promise_id, item in promise_by_id.items()
            if str(item.get("strength")) == "CORE"
        }
        served_ids = {
            item["promise_id"]
            for item in verified_reader
            if item["verification_status"] == "VERIFIED"
            and item["service"] in {"SERVED", "PARTIALLY_SERVED"}
        }
        if core_ids and not core_ids.intersection(served_ids):
            warnings.append("本候选未直接服务 CORE Reader Promise；单章缺席只记 Soft Miss。")

        drive_contract = context.effective_contracts.narrative_drive or {}
        primary_drive = str(drive_contract.get("primary_drive") or "")
        secondary_drives = {
            str(item) for item in drive_contract.get("secondary_drives", [])
        }
        active_drives = ({primary_drive} if primary_drive else set()) | secondary_drives
        declared_drive = candidate.narrative_drive_alignment
        referenced_drives = {
            item
            for item in [
                declared_drive.primary_drive,
                *declared_drive.secondary_drive_effects,
                *declared_drive.drives_advanced,
                *declared_drive.drives_paid_off,
                *declared_drive.drives_deferred,
            ]
            if item
        }
        unknown_drives = referenced_drives - active_drives
        for drive in sorted(unknown_drives):
            message = f"Narrative Drive 不属于 Effective Drive Mix：{drive}"
            author_failures.append(message)
            differences.append(message)
        progression_effect = engine_validation.verified_progression_impact
        progression_changed = any(
            progression_effect.get(name)
            for name in (
                "axis_advanced",
                "progression_delta_type",
                "stage_change",
                "resource_changes",
                "ability_unlocks",
                "world_expansion",
            )
        )
        verified_advanced = [
            drive
            for drive in declared_drive.drives_advanced
            if drive in active_drives
            and (
                drive != primary_drive
                or bool(declared_drive.evidence)
                or progression_changed
            )
        ]
        if declared_drive.primary_drive and declared_drive.primary_drive != primary_drive:
            message = (
                "Candidate Primary Drive 与 Effective Contract 不一致："
                f"{declared_drive.primary_drive} != {primary_drive}"
            )
            author_failures.append(message)
            differences.append(message)
        if primary_drive and primary_drive not in verified_advanced:
            warnings.append("Primary Drive 没有可验证的结构推进；单章只记 Soft Miss。")
        if primary_drive and primary_drive in declared_drive.drive_conflicts:
            message = f"候选明确冲突 Primary Drive：{primary_drive}"
            author_failures.append(message)
            differences.append(message)
        verified_drive = NarrativeDriveAlignment(
            primary_drive=primary_drive or None,
            primary_drive_effect=(
                declared_drive.primary_drive_effect
                if primary_drive in verified_advanced
                else ""
            ),
            secondary_drive_effects={
                drive: effect
                for drive, effect in declared_drive.secondary_drive_effects.items()
                if drive in secondary_drives
            },
            drives_advanced=verified_advanced,
            drives_paid_off=[
                drive for drive in declared_drive.drives_paid_off if drive in active_drives
            ],
            drives_deferred=[
                drive for drive in declared_drive.drives_deferred if drive in active_drives
            ],
            drive_conflicts=[
                drive for drive in declared_drive.drive_conflicts if drive in active_drives
            ],
            drive_balance=(
                declared_drive.drive_balance if not unknown_drives else "CONFLICT"
            ),
            evidence=(
                declared_drive.evidence
                if verified_advanced
                else engine_validation.evidence
            ),
        ).model_dump(mode="json")

        core_contradicted = any(
            item["contract_strength"] == "CORE" and item["service"] == "CONTRADICTED"
            for item in verified_reader
        )
        genre_evidence = GenreStructureEvidence(
            progression_gate_affects_causality=bool(
                progression_effect.get("stage_change")
                or progression_effect.get("progression_delta_type")
            ),
            extraordinary_resource_affects_choice=bool(
                progression_effect.get("resource_changes")
            ),
            ability_changes_solution=bool(progression_effect.get("ability_unlocks")),
            power_opens_space=bool(progression_effect.get("world_expansion")),
            mystery_changes_understanding=bool(candidate.reveal_impact.hints)
            or bool(candidate.reveal_impact.partial_reveals)
            or bool(candidate.reveal_impact.full_reveals),
            core_promise_preserved=not core_contradicted,
            secondary_replaces_primary=bool(
                primary_drive
                and declared_drive.drives_advanced
                and primary_drive not in declared_drive.drives_advanced
                and any(
                    drive in secondary_drives for drive in declared_drive.drives_advanced
                )
            ),
            contradicts_core_promise=core_contradicted,
            evidence=[
                *engine_validation.evidence,
                *[
                    proof
                    for item in verified_reader
                    for proof in item.get("evidence", [])
                ],
            ],
        )
        genre_diagnostics = diagnose_genre_change(genre_evidence)
        if genre_diagnostics.drift.hard_failure:
            author_failures.extend(genre_diagnostics.drift.reasons)
        try:
            drive_enum = NarrativeDrive(primary_drive)
        except ValueError:
            drive_diagnostic: dict[str, Any] = {
                "status": "UNKNOWN",
                "warning": False,
                "hard_failure": False,
                "reasons": ["没有可验证的 Effective Primary Drive"],
                "evidence": [],
            }
        else:
            verified_drive_changed = primary_drive in verified_advanced
            drive_result = diagnose_narrative_drive_drift(
                NarrativeDriveStructureEvidence(
                    primary_drive=drive_enum,
                    primary_drive_affects_causality=verified_drive_changed,
                    primary_drive_state_changed=verified_drive_changed,
                    secondary_drive_replaces_primary=genre_evidence.secondary_replaces_primary,
                    unrelated_to_all_confirmed_drives=not bool(verified_advanced),
                    contradicts_primary_drive=primary_drive
                    in declared_drive.drive_conflicts,
                    evidence=verified_drive["evidence"],
                )
            )
            drive_diagnostic = drive_result.model_dump(mode="json")
            if drive_result.hard_failure:
                author_failures.extend(drive_result.reasons)

        resource_tokens = _tokens(context.chapter_state.resource_state)
        opportunity = context.chapter_state.opportunity_surface or {}
        opportunity_tokens = _tokens(opportunity.get("items", []))
        verified_resources: list[dict[str, Any]] = []
        for resource_claim in candidate.resource_opportunity_impact:
            if _matches(resource_claim, resource_tokens):
                verified_resources.append(
                    {
                        "claim": resource_claim,
                        "source": "CURRENT_RESOURCE",
                        "status": "VERIFIED",
                    }
                )
            elif _matches(resource_claim, opportunity_tokens):
                status = "CONFLICT" if any(
                    word in resource_claim.casefold()
                    for word in ("已拥有", "直接使用", "消耗", "owned", "consume")
                ) else "VERIFIED_OPPORTUNITY_ONLY"
                verified_resources.append(
                    {
                        "claim": resource_claim,
                        "source": "OPPORTUNITY",
                        "status": status,
                    }
                )
                if status == "CONFLICT":
                    message = (
                        "Resource Impact 把 Opportunity 当作已拥有："
                        f"{resource_claim}"
                    )
                    gate_values.setdefault("capability_violations", []).append(message)
                    differences.append(message)
            else:
                verified_resources.append(
                    {
                        "claim": resource_claim,
                        "source": "UNKNOWN",
                        "status": "UNVERIFIED",
                    }
                )
                message = f"Resource Impact 缺少冻结状态引用：{resource_claim}"
                warnings.append(message)
                differences.append(message)

        recommendation = context.planning_state.scheduler_recommendation
        if recommendation is not None:
            recommended = recommendation.primary_intent.value
            alignment = candidate.scheduler_alignment
            if (
                alignment.recommended_primary_intent
                and alignment.recommended_primary_intent != recommended
            ):
                message = "Scheduler Alignment 引用了错误的冻结 Primary Intent"
                author_failures.append(message)
                differences.append(message)
            if not alignment.candidate_primary_intent:
                warnings.append("Candidate 未填写 Scheduler Alignment，保持 UNVERIFIED。")

        gate_values.setdefault("author_constraint_violations", []).extend(author_failures)
        gate = KernelHardGateCompilation.model_validate(gate_values)

        progression_values = {
            "permanent_growth": (
                100.0
                if progression_effect.get("stage_change")
                or progression_effect.get("ability_unlocks")
                else 60.0
                if progression_effect.get("axis_advanced")
                or progression_effect.get("progression_delta_type")
                else 0.0
            ),
            "world_state_change": (
                100.0
                if progression_effect.get("world_expansion")
                else 60.0
                if progression_effect.get("resource_changes")
                else 0.0
            ),
            "relationship_change": (
                100.0
                if candidate.primary_function.value == "relationship_shift"
                and bool(candidate.state_changes)
                else 0.0
            ),
            "knowledge_change": (
                100.0
                if candidate.reveal_impact.partial_reveals
                or candidate.reveal_impact.full_reveals
                else 60.0
                if candidate.reveal_impact.hints
                or candidate.primary_function.value == "discovery"
                else 0.0
            ),
            "goal_advance": (
                100.0
                if candidate.promises_to_pay
                else 70.0
                if candidate.promises_to_advance
                or bool(candidate.required_irreversible_change.strip())
                else 0.0
            ),
            "strategy_expansion": (
                100.0
                if progression_effect.get("ability_unlocks")
                else 75.0
                if progression_effect.get("resource_changes")
                or progression_effect.get("world_expansion")
                else 50.0
                if candidate.protagonist_strategy.strip() and candidate.state_changes
                else 0.0
            ),
        }
        progress_evidence = {
            component: (
                list(engine_validation.evidence)
                if value > 0
                else [f"no_verified_{component}_change"]
            )
            for component, value in progression_values.items()
        }
        metric_values: dict[str, Any] = {
            "progress": {
                "formula": "existing:progress",
                "components": progression_values,
                "evidence": progress_evidence,
                "completeness": "COMPLETE",
                "source": "KERNEL_VERIFIED_EVIDENCE",
                "score": None,
            }
        }
        score_overrides: dict[str, float] = {}
        score_sources: dict[str, dict[str, Any]] = {}
        if metrics_config is not None:
            progress_result = progress(
                progression_values,
                metrics_config["progress"],
            )
            metric_values["progress"]["score"] = progress_result.score
            score_overrides["progress_gain"] = progress_result.score
            score_sources["progress_gain"] = metric_values["progress"]

            progression_state = context.chapter_state.progression_state or {}
            missing_resources = progression_state.get("missing_resources", [])
            bottlenecks = progression_state.get("primary_axis_state", {}).get(
                "current_bottlenecks", []
            )
            resource_values = {
                "current_shortfall": 100.0 if missing_resources else 0.0,
                "cost_income_imbalance": (
                    100.0
                    if any(
                        word in item["claim"].casefold()
                        for item in verified_resources
                        for word in ("消耗", "付出", "consume", "spend")
                    )
                    else 0.0
                ),
                "recently_blocked_actions": 100.0 if bottlenecks else 0.0,
                "near_future_demand": 100.0 if missing_resources else 0.0,
                "reader_salience": (
                    100.0
                    if "RESOURCE_OPPORTUNITY"
                    in set(context.effective_contracts.reader_experience.get(
                        "experience_priorities", {}
                    ) if context.effective_contracts.reader_experience else {})
                    else 50.0
                    if missing_resources
                    else 0.0
                ),
            }
            resource_score = resource_pressure(
                resource_values,
                metrics_config["resource_pressure"],
            )
            metric_values["resource_pressure"] = {
                "formula": "existing:resource_pressure",
                "components": resource_values,
                "evidence": [
                    *[f"missing_resource:{item}" for item in missing_resources],
                    *[f"bottleneck:{item}" for item in bottlenecks],
                ],
                "completeness": "COMPLETE",
                "source": "KERNEL_VERIFIED_EVIDENCE",
                "score": resource_score,
            }

            debt_by_id = {
                str(item.get("debt_id")): item
                for item in context.planning_state.narrative_debts
                if item.get("debt_id")
            }
            served_debts = set(candidate.scheduler_alignment.debts_served)
            served_scores = [
                float(debt_by_id[debt_id].get("debt_score") or 0)
                for debt_id in served_debts
                if debt_id in debt_by_id
            ]
            debt_utility = min(100.0, max(served_scores, default=0.0))
            score_overrides["debt_utility"] = debt_utility
            score_sources["debt_utility"] = {
                "formula": "existing:narrative_debt",
                "score": debt_utility,
                "evidence": sorted(served_debts.intersection(debt_by_id)),
                "completeness": "COMPLETE",
                "source": "FROZEN_NARRATIVE_DEBT",
            }

            thread_ids = {
                str(item.get("thread_id") or item.get("id"))
                for item in context.planning_state.active_threads
                if item.get("thread_id") or item.get("id")
            }
            thread_fit = 100.0 if candidate.primary_thread_id in thread_ids else 0.0
            score_overrides["thread_need_fit"] = thread_fit
            score_sources["thread_need_fit"] = {
                "score": thread_fit,
                "evidence": [candidate.primary_thread_id],
                "completeness": "COMPLETE",
                "source": "FROZEN_ACTIVE_THREADS",
            }

            payoff_profile = context.effective_contracts.payoff_channel or {}
            enabled_channels = {
                str(channel)
                for channel, strength in payoff_profile.get("channels", {}).items()
                if str(strength) != "DISABLED"
            }
            verified_channels = [
                channel
                for channel in candidate.payoff_channel_impact
                if channel in enabled_channels
            ]
            unknown_channels = set(candidate.payoff_channel_impact) - set(
                verified_channels
            )
            if unknown_channels:
                warnings.append(
                    "Payoff Channel 未在 Effective Profile 启用："
                    + ", ".join(sorted(unknown_channels))
                )
            payoff_value = 0.0
            if verified_channels:
                anticipation_items = (
                    context.planning_state.anticipation_surface or {}
                ).get("items", [])
                maturity = max(
                    [
                        float(item.get("maturity") or 0) * 100
                        for item in anticipation_items
                        if isinstance(item, Mapping)
                    ],
                    default=0.0,
                )
                payoff_result = payoff_score(
                    maturity=maturity,
                    impact=max(progression_values.values()),
                    causality=100.0 if candidate.causal_sources else 0.0,
                    after_value=progression_values["strategy_expansion"],
                    repetition_fatigue_score=candidate.score_inputs.repetition_fatigue,
                    structural_fit=100.0 if candidate.promises_to_pay else 60.0,
                    future_damage=min(
                        100.0,
                        20.0
                        * len(
                            candidate.innovation_preview.expected_new_debts
                            if candidate.innovation_preview is not None
                            else []
                        ),
                    ),
                    config=metrics_config["payoff"],
                )
                payoff_value = payoff_result.score
                metric_values["payoff"] = {
                    "formula": "existing:payoff_score",
                    "components": payoff_result.inputs,
                    "evidence": verified_channels,
                    "completeness": "PARTIAL",
                    "source": "KERNEL_VERIFIED_PLUS_EXISTING_REPETITION_INPUT",
                    "score": payoff_value,
                }
            score_overrides["payoff_or_setup_utility"] = payoff_value
            score_sources["payoff_or_setup_utility"] = metric_values.get(
                "payoff",
                {
                    "score": 0.0,
                    "evidence": ["no_verified_payoff_channel"],
                    "completeness": "COMPLETE",
                    "source": "KERNEL_VERIFIED_EVIDENCE",
                },
            )
            score_overrides["agency_gain"] = (
                100.0
                if progression_changed and candidate.protagonist_strategy.strip()
                else 50.0
                if candidate.state_changes and candidate.protagonist_strategy.strip()
                else 0.0
            )
            score_overrides["risk_fit"] = (
                100.0
                if not gate.hard_failures
                and bool(
                    candidate.required_cost.strip()
                    or progression_effect.get("growth_costs")
                )
                else 0.0
            )
            score_overrides["future_damage"] = (
                100.0
                if gate.hard_failures
                else min(
                    100.0,
                    20.0
                    * len(
                        candidate.innovation_preview.expected_new_debts
                        if candidate.innovation_preview is not None
                        else []
                    ),
                )
            )
            for name in ("agency_gain", "risk_fit", "future_damage"):
                score_sources[name] = {
                    "score": score_overrides[name],
                    "evidence": list(engine_validation.evidence),
                    "completeness": "COMPLETE",
                    "source": "KERNEL_VERIFIED_EVIDENCE",
                }
            metric_values["candidate_score_overrides"] = {
                "values": score_overrides,
                "components": score_sources,
                "source": "KERNEL_EVIDENCE_COMPILER",
            }
        if gate.hard_failures:
            completeness = EvidenceCompleteness.CONFLICT
        elif warnings:
            completeness = EvidenceCompleteness.PARTIAL
        else:
            completeness = EvidenceCompleteness.COMPLETE
        verified_world = [
            str(item)
            for item in progression_effect.get("world_expansion", [])
        ]
        verified = {
            "reader_promise_alignment": verified_reader,
            "narrative_drive_alignment": verified_drive,
            "progression_impact": progression_effect,
            "resource_impact": verified_resources,
            "world_expansion_impact": verified_world,
            "scheduler_alignment": candidate.scheduler_alignment.model_dump(mode="json"),
            "genre_drift": genre_diagnostics.drift.model_dump(mode="json"),
            "genre_evolution": genre_diagnostics.evolution.model_dump(mode="json"),
            "drive_drift": drive_diagnostic,
        }
        return KernelEvidenceCompilation(
            candidate_local_id=candidate.local_id,
            declared=_declared_trace(candidate),
            verified=verified,
            differences=list(dict.fromkeys(differences)),
            verified_reader_promise_alignment=verified_reader,
            verified_drive_alignment=verified_drive,
            verified_progression_impact=progression_effect,
            verified_world_expansion_impact=verified_world,
            verified_resource_impact=verified_resources,
            verified_progress_components=metric_values["progress"],
            hard_gate_compilation=gate,
            soft_metric_compilation=metric_values,
            completeness=completeness,
            warnings=list(dict.fromkeys(warnings)),
        )


__all__ = [
    "EvidenceCompleteness",
    "KernelEvidenceCompilation",
    "KernelEvidenceCompiler",
    "KernelHardGateCompilation",
]
