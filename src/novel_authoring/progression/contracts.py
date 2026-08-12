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
    GenreContract,
    GrowthAxis,
    GrowthAxisType,
    ProgressionContract,
    ProgressionDeltaType,
    ProgressionSubject,
    ProgressionTopology,
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


def progression_contract_from_genre(
    contract: GenreContract,
    *,
    progression_contract_id: str,
    progression_subject: ProgressionSubject,
    growth_object: str,
    axis_type: GrowthAxisType = GrowthAxisType.CUSTOM,
    topology: list[ProgressionTopology] | None = None,
) -> ProgressionContract:
    """Compile structural capabilities without branching on Adapter identity."""

    capabilities = contract.capabilities
    gates: list[BreakthroughGate] = []
    if capabilities.has_resource_gate:
        gates.append(
            BreakthroughGate(
                gate_id="resource-gate",
                gate_type=BreakthroughGateType.RESOURCE_GATE,
                requirement="取得并实际满足作者确认的成长资源条件",
                evidence_requirements=["章节资源状态与来源证据"],
            )
        )
    if capabilities.has_knowledge_gate:
        gates.append(
            BreakthroughGate(
                gate_id="knowledge-gate",
                gate_type=BreakthroughGateType.KNOWLEDGE_GATE,
                requirement="真正理解并能运用所需知识",
                evidence_requirements=["知识获得与行为改变证据"],
            )
        )
    if not gates:
        gates.append(
            BreakthroughGate(
                gate_id="structural-gate",
                gate_type=BreakthroughGateType.CUSTOM,
                requirement="满足作者确认的下一次可能性变化条件",
                evidence_requirements=["可回指的状态变化证据"],
            )
        )
    unlocks = (
        [
            AbilityUnlockRule(
                unlock_id="contract-unlock",
                mode=(
                    AbilityUnlockMode.KNOWLEDGE
                    if capabilities.has_knowledge_gate
                    else AbilityUnlockMode.CUSTOM
                ),
                condition="满足合同门槛并建立可回指来源",
                effect="新增解决问题的方法或进入空间",
            )
        ]
        if capabilities.has_ability_unlock
        else []
    )
    selected_topology = topology or [ProgressionTopology.ACCUMULATIVE]
    return ProgressionContract(
        progression_contract_id=progression_contract_id,
        progression_subject=progression_subject,
        primary_axis=GrowthAxis(
            axis_id="primary-growth-axis",
            name=growth_object,
            axis_type=axis_type,
            current_stage_schema="作者确认的定性成长阶段",
            progress_measure="成长是否扩大行动、进入、理解或影响的可能性",
            unlock_effects=["改变可采取的解决方法"],
            bottlenecks=[gate.requirement for gate in gates],
            evidence_requirements=[
                evidence for gate in gates for evidence in gate.evidence_requirements
            ],
            visibility=UpperCeilingVisibility.PARTIAL,
        ),
        topology=selected_topology,
        allowed_delta_types=[
            ProgressionDeltaType.ADVANCE,
            ProgressionDeltaType.UNLOCK,
            ProgressionDeltaType.CONVERT,
            ProgressionDeltaType.TRANSFORM,
        ],
        stage_model="可命名或不命名的定性阶段，不要求数字等级",
        breakthrough_model=BreakthroughModel(gates=gates),
        ability_unlock_model=unlocks,
        resource_economy=contract.genre_native_resource_types,
        growth_costs=contract.genre_native_conflicts,
        verification_modes=(
            contract.genre_native_scene_types
            if capabilities.has_verification_requirement
            else ["通过事件后果确认成长成立"]
        ),
        next_ceiling_model=contract.world_expansion_expectation
        or "由已获得信息逐步显露更高可能性",
        upper_ceiling_visibility=UpperCeilingVisibility.PARTIAL,
        progression_promises=[
            promise.statement
            for promise in contract.genre_promises
            if promise.strength.value != "DISABLED"
        ],
        author_constraints=contract.forbidden_drift_patterns,
        status=ContractStatus.NEEDS_REVIEW,
    )


__all__ = ["progression_contract_from_derived", "progression_contract_from_genre"]
