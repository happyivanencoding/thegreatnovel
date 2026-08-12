"""Read-only, chapter-aware progression projections."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.progression.models import (
    AxisProgressionState,
    ContractStatus,
    GrowthAxis,
    ProgressionContract,
    ProgressionStateView,
    QualitativeReadiness,
    UpperCeilingVisibility,
    WorldExpansionContract,
    WorldExpansionStateView,
)


class AxisObservation(BaseModel):
    """Evidence-backed semantic observation supplied at the selected chapter."""

    model_config = ConfigDict(extra="forbid")

    current_stage: str | None = None
    current_substage: str | None = None
    available_branches: list[str] = Field(default_factory=list)
    locked_branches: list[str] = Field(default_factory=list)
    readiness: QualitativeReadiness = QualitativeReadiness.UNKNOWN
    evidence: list[str] = Field(default_factory=list)
    pending_showcases: list[str] = Field(default_factory=list)
    recent_breakthrough: dict[str, object] | None = None
    progression_debts: list[str] = Field(default_factory=list)


def _chapter(world_state: Mapping[str, Any]) -> tuple[str, int]:
    chapter = world_state.get("chapter")
    if not isinstance(chapter, Mapping) or not chapter.get("chapter_id"):
        raise ValueError("Progression projection 必须显式绑定 chapter_id")
    return str(chapter["chapter_id"]), int(chapter.get("ordinal") or 0)


def _record_names(world_state: Mapping[str, Any], collections: tuple[str, ...]) -> list[str]:
    names: list[str] = []
    for collection in collections:
        values = world_state.get(collection, [])
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, Mapping):
                continue
            name = value.get("name") or value.get("title") or value.get("statement")
            if name:
                names.append(str(name))
    return list(dict.fromkeys(names))


def _axis_state(
    axis: GrowthAxis,
    observation: AxisObservation | None,
) -> AxisProgressionState:
    value = observation or AxisObservation()
    stage_map = {stage.stage_id: stage for stage in axis.stage_definitions}
    if value.current_stage is not None and stage_map and value.current_stage not in stage_map:
        raise ValueError(f"Axis observation 引用了未知阶段：{value.current_stage}")
    next_stages = (
        stage_map[value.current_stage].next_stage_candidates
        if value.current_stage is not None and value.current_stage in stage_map
        else []
    )
    return AxisProgressionState(
        axis_id=axis.axis_id,
        current_stage=value.current_stage,
        current_substage=value.current_substage,
        available_branches=value.available_branches,
        locked_branches=value.locked_branches,
        next_known_stage=next_stages,
        next_stage_visibility=(axis.visibility if next_stages else UpperCeilingVisibility.UNKNOWN),
        current_bottlenecks=axis.bottlenecks,
        readiness=value.readiness,
        evidence=value.evidence,
    )


def project_progression_state(
    world_state: Mapping[str, Any],
    contract: ProgressionContract,
    *,
    subject_id: str,
    axis_observations: Mapping[str, AxisObservation] | None = None,
) -> ProgressionStateView | None:
    """Project only from the supplied chapter slice and evidence observations."""

    chapter_id, chapter_ordinal = _chapter(world_state)
    if contract.status is not ContractStatus.EFFECTIVE:
        return None
    if (
        contract.effective_from_boundary is not None
        and chapter_ordinal < contract.effective_from_boundary
    ):
        return None
    observations = axis_observations or {}
    required_resources = list(
        dict.fromkeys(
            resource
            for gate in contract.breakthrough_model.gates
            for resource in gate.required_resources
        )
    )
    available_resources = _record_names(
        world_state,
        ("resources", "inventory", "equipment"),
    )
    available_keys = {value.casefold() for value in available_resources}
    missing_resources = [
        value for value in required_resources if value.casefold() not in available_keys
    ]
    primary_observation = observations.get(contract.primary_axis.axis_id)
    secondary_observations = [
        observations.get(axis.axis_id) for axis in contract.secondary_axes
    ]
    confirmed_delta = world_state.get("chapter_delta", {}).get("confirmed", [])
    recent_growth_events = (
        [dict(item) for item in confirmed_delta if isinstance(item, Mapping)]
        if isinstance(confirmed_delta, list)
        else []
    )
    ability_names = _record_names(world_state, ("abilities",))
    pending_showcases = [
        value
        for observation in [primary_observation, *secondary_observations]
        if observation is not None
        for value in observation.pending_showcases
    ]
    debts = [
        value
        for observation in [primary_observation, *secondary_observations]
        if observation is not None
        for value in observation.progression_debts
    ]
    recent_breakthrough = next(
        (
            observation.recent_breakthrough
            for observation in [primary_observation, *secondary_observations]
            if observation is not None and observation.recent_breakthrough is not None
        ),
        None,
    )
    readiness = (
        QualitativeReadiness.MISSING_RESOURCE
        if missing_resources
        else (
            primary_observation.readiness
            if primary_observation is not None
            else QualitativeReadiness.UNKNOWN
        )
    )
    ceiling = contract.next_ceiling_model
    return ProgressionStateView(
        subject_id=subject_id,
        subject_type=contract.progression_subject,
        chapter_id=chapter_id,
        chapter_ordinal=chapter_ordinal,
        primary_axis_state=_axis_state(contract.primary_axis, primary_observation),
        secondary_axis_states=[
            _axis_state(axis, observation)
            for axis, observation in zip(
                contract.secondary_axes,
                secondary_observations,
                strict=True,
            )
        ],
        topology_state=contract.topology,
        required_resources=required_resources,
        available_resources=available_resources,
        missing_resources=missing_resources,
        recent_growth_events=recent_growth_events,
        unlocked_abilities=ability_names,
        pending_ability_showcases=pending_showcases,
        recent_breakthrough=recent_breakthrough,
        next_breakthrough_readiness=readiness,
        growth_costs_active=contract.growth_costs,
        known_higher_ceiling=(
            [ceiling]
            if contract.upper_ceiling_visibility
            in {UpperCeilingVisibility.VISIBLE, UpperCeilingVisibility.PARTIAL}
            else []
        ),
        unknown_ceiling_hints=(
            [ceiling]
            if contract.upper_ceiling_visibility is UpperCeilingVisibility.HINTED
            else []
        ),
        progression_debts=list(dict.fromkeys(debts)),
    )


def project_world_expansion_state(
    world_state: Mapping[str, Any],
    contract: WorldExpansionContract,
    *,
    current_stage_id: str | None = None,
) -> WorldExpansionStateView | None:
    chapter_id, chapter_ordinal = _chapter(world_state)
    if contract.status is not ContractStatus.EFFECTIVE:
        return None
    if (
        contract.effective_from_boundary is not None
        and chapter_ordinal < contract.effective_from_boundary
    ):
        return None
    stages = {stage.stage_id: stage for stage in contract.stages}
    selected_id = current_stage_id or contract.current_stage_id
    if selected_id not in stages:
        raise ValueError("World Expansion observation 引用了未知阶段")
    current = stages[selected_id]
    next_stages = sorted(
        (stage for stage in contract.stages if stage.order > current.order),
        key=lambda stage: stage.order,
    )[:2]
    return WorldExpansionStateView(
        chapter_id=chapter_id,
        chapter_ordinal=chapter_ordinal,
        current_stage=current,
        next_stage_candidates=next_stages,
        transition_conditions=[
            condition for stage in next_stages for condition in stage.transition_conditions
        ],
    )


__all__ = [
    "AxisObservation",
    "project_progression_state",
    "project_world_expansion_state",
]
