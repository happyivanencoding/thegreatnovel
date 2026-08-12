"""Progression contract compilation helpers."""

from __future__ import annotations

from novel_authoring.progression.models import (
    AbilityUnlockMode,
    AbilityUnlockRule,
    BreakthroughGate,
    BreakthroughGateType,
    BreakthroughModel,
    ContractStatus,
    DerivedAdapterSpec,
    GrowthAxis,
    GrowthAxisType,
    ProgressionContract,
    ProgressionDeltaType,
    UpperCeilingVisibility,
)


def progression_contract_from_derived(
    spec: DerivedAdapterSpec,
    *,
    progression_contract_id: str,
) -> ProgressionContract:
    """Compile a custom grammar without forcing it into a built-in stage ladder."""

    gates = spec.growth_gates or ["由作者确认下一次可能性变化的真实条件"]
    return ProgressionContract(
        progression_contract_id=progression_contract_id,
        progression_subject=spec.progression_subject,
        primary_axis=GrowthAxis(
            axis_id="custom-primary-axis",
            name=spec.growth_object,
            axis_type=GrowthAxisType.CUSTOM,
            current_stage_schema="作者定义的定性状态，不伪造数值进度",
            progress_measure="；".join(spec.reader_visible_progress),
            unlock_effects=[spec.unlock_logic],
            costs=spec.growth_costs,
            bottlenecks=gates,
            evidence_requirements=spec.verification_modes,
            visibility=UpperCeilingVisibility.HINTED,
        ),
        topology=spec.progression_topology,
        allowed_delta_types=spec.delta_types,
        stage_model="自定义阶段图；允许无数字、分支和不可逆锁死",
        breakthrough_model=BreakthroughModel(
            gates=[
                BreakthroughGate(
                    gate_id=f"custom-gate-{index}",
                    gate_type=(
                        BreakthroughGateType.CHOICE_GATE
                        if ProgressionDeltaType.LOCK_OUT in spec.delta_types
                        else BreakthroughGateType.CUSTOM
                    ),
                    requirement=requirement,
                    evidence_requirements=spec.verification_modes,
                    irreversible=(
                        ProgressionDeltaType.SACRIFICE in spec.delta_types
                        or ProgressionDeltaType.LOCK_OUT in spec.delta_types
                    ),
                )
                for index, requirement in enumerate(gates, start=1)
            ]
        ),
        ability_unlock_model=[
            AbilityUnlockRule(
                unlock_id="custom-unlock",
                mode=(
                    AbilityUnlockMode.IRREVERSIBLE_CHOICE
                    if ProgressionDeltaType.LOCK_OUT in spec.delta_types
                    else AbilityUnlockMode.CUSTOM
                ),
                condition=spec.unlock_logic,
                effect="；".join(spec.reader_visible_progress),
            )
        ],
        resource_economy=spec.growth_resources,
        growth_costs=spec.growth_costs,
        verification_modes=spec.verification_modes,
        next_ceiling_model=spec.long_term_ceiling_logic,
        upper_ceiling_visibility=UpperCeilingVisibility.HINTED,
        progression_promises=spec.payoff_logic,
        author_constraints=["不得替换为未经作者确认的内置成长套路"],
        status=ContractStatus.NEEDS_REVIEW,
    )


__all__ = ["progression_contract_from_derived"]
