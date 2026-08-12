from __future__ import annotations

import pytest

from novel_authoring.progression.contracts import progression_contract_from_derived
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
    PayoffChannel,
    ProgressionContract,
    ProgressionDeltaType,
    ProgressionStageDefinition,
    ProgressionSubject,
    ProgressionTopology,
    RuntimeGenreCapabilities,
    UpperCeilingVisibility,
)


def ordered_axis() -> GrowthAxis:
    return GrowthAxis(
        axis_id="body-axis",
        name="肉身蜕变",
        axis_type=GrowthAxisType.BODY_EVOLUTION,
        current_stage_schema="定性生命阶段",
        stage_order=["tempered", "renewed", "mythic"],
        stage_definitions=[
            ProgressionStageDefinition(
                stage_id="tempered",
                name="初次锻体",
                order=1,
                next_stage_candidates=["renewed"],
            ),
            ProgressionStageDefinition(
                stage_id="renewed",
                name="生命重构",
                order=2,
                next_stage_candidates=["mythic"],
            ),
            ProgressionStageDefinition(
                stage_id="mythic",
                name="神话身体",
                order=3,
            ),
        ],
        progress_measure="由身体能力、生命性质和可承受代价共同判断",
        evidence_requirements=["正文事件证明身体性质变化"],
    )


def progression_contract(**overrides: object) -> ProgressionContract:
    payload: dict[str, object] = {
        "progression_contract_id": "progression-body",
        "progression_subject": ProgressionSubject.CHARACTER,
        "primary_axis": ordered_axis(),
        "secondary_axes": [],
        "topology": [ProgressionTopology.LINEAR],
        "allowed_delta_types": [
            ProgressionDeltaType.ADVANCE,
            ProgressionDeltaType.TRANSFORM,
        ],
        "stage_model": "有序但非数字化的生命阶段",
        "breakthrough_model": BreakthroughModel(
            gates=[
                BreakthroughGate(
                    gate_id="body-resource-gate",
                    gate_type=BreakthroughGateType.BODY_TRANSFORMATION,
                    requirement="完成一次有来源的身体重构",
                    evidence_requirements=["资源来源", "转化事件", "身体后果"],
                )
            ]
        ),
        "ability_unlock_model": [
            AbilityUnlockRule(
                unlock_id="body-unlock",
                mode=AbilityUnlockMode.STAGE,
                condition="身体阶段变化成立",
                effect="身体能力改变解决问题的方式",
            )
        ],
        "growth_costs": ["身体转化具有恢复期"],
        "verification_modes": ["战斗、救援、探索或生存事件"],
        "next_ceiling_model": "更高生命层级保持部分可见",
        "upper_ceiling_visibility": UpperCeilingVisibility.PARTIAL,
        "progression_promises": ["成长会改变行动可能性"],
        "status": ContractStatus.NEEDS_REVIEW,
    }
    payload.update(overrides)
    return ProgressionContract.model_validate(payload)


def test_progression_contract_supports_ordered_non_numeric_stages() -> None:
    contract = progression_contract()

    assert contract.primary_axis.stage_order == ["tempered", "renewed", "mythic"]
    assert contract.primary_axis.stage_definitions[1].name == "生命重构"


def test_progression_topology_supports_branching_and_multiple_successors() -> None:
    branch_axis = GrowthAxis(
        axis_id="choice-axis",
        name="不可逆路线",
        axis_type=GrowthAxisType.IDENTITY,
        current_stage_schema="选择与锁死状态",
        stage_definitions=[
            ProgressionStageDefinition(
                stage_id="origin",
                name="尚未选择",
                next_stage_candidates=["route-a", "route-b"],
            ),
            ProgressionStageDefinition(stage_id="route-a", name="路线甲"),
            ProgressionStageDefinition(stage_id="route-b", name="路线乙"),
        ],
        progress_measure="已经选择和永久失去的路线",
    )
    contract = progression_contract(
        primary_axis=branch_axis,
        topology=[ProgressionTopology.BRANCHING, ProgressionTopology.TRADEOFF],
        allowed_delta_types=[
            ProgressionDeltaType.BRANCH,
            ProgressionDeltaType.SACRIFICE,
            ProgressionDeltaType.LOCK_OUT,
        ],
    )

    assert contract.primary_axis.stage_definitions[0].next_stage_candidates == [
        "route-a",
        "route-b",
    ]
    assert ProgressionDeltaType.LOCK_OUT in contract.allowed_delta_types


def test_progression_topology_supports_rebuild_and_transform() -> None:
    contract = progression_contract(
        topology=[ProgressionTopology.TRANSFORMATIVE],
        allowed_delta_types=[
            ProgressionDeltaType.REGRESS,
            ProgressionDeltaType.REBUILD,
            ProgressionDeltaType.TRANSFORM,
        ],
    )

    assert ProgressionDeltaType.REBUILD in contract.allowed_delta_types


def test_multiple_progression_axes_require_real_secondary_axis() -> None:
    knowledge_axis = GrowthAxis(
        axis_id="knowledge-axis",
        name="古代语言理解",
        axis_type=GrowthAxisType.KNOWLEDGE,
        current_stage_schema="已真正理解的语言与现实访问权限",
        progress_measure="可回指的理解证据与已打开现实层",
    )
    contract = progression_contract(
        secondary_axes=[knowledge_axis],
        topology=[ProgressionTopology.MULTI_AXIS],
    )
    assert contract.secondary_axes[0].axis_type is GrowthAxisType.KNOWLEDGE

    with pytest.raises(ValueError, match="secondary axis"):
        progression_contract(topology=[ProgressionTopology.MULTI_AXIS])


def test_stage_order_rejects_unknown_or_missing_stage_ids() -> None:
    with pytest.raises(ValueError, match="stage_order"):
        ordered_axis().model_copy(update={"stage_order": ["missing"]}).model_validate(
            {
                **ordered_axis().model_dump(mode="json"),
                "stage_order": ["missing"],
            }
        )


def test_ood_seed_compiles_to_valid_progression_contract() -> None:
    spec = DerivedAdapterSpec(
        spec_id="lost-futures",
        progression_subject=ProgressionSubject.CHARACTER,
        growth_object="现实可能性权柄",
        progression_topology=[
            ProgressionTopology.BRANCHING,
            ProgressionTopology.TRADEOFF,
        ],
        delta_types=[ProgressionDeltaType.SACRIFICE, ProgressionDeltaType.LOCK_OUT],
        growth_resources=["被放弃的未来"],
        growth_gates=["作出真正不可撤销的选择"],
        growth_costs=["永久失去一条人生路线"],
        verification_modes=["现实服从新获得的可能性权柄"],
        unlock_logic="不可逆选择把失去的未来转化为权柄",
        world_expansion_relation="选择扩大可触及的现实层",
        reader_visible_progress=["已失去未来", "已获得权柄", "锁死路线"],
        long_term_ceiling_logic="由可承担的不可逆后果决定",
        payoff_logic=["选择与现实改变形成因果闭环"],
        capabilities=RuntimeGenreCapabilities(
            has_progression_axis=True,
            has_verification_requirement=True,
            has_world_expansion=True,
        ),
        payoff_channels=[PayoffChannel.TRANSFORMATION],
    )

    contract = progression_contract_from_derived(
        spec,
        progression_contract_id="progression-lost-futures",
    )

    assert contract.progression_subject is ProgressionSubject.CHARACTER
    assert contract.topology == [
        ProgressionTopology.BRANCHING,
        ProgressionTopology.TRADEOFF,
    ]
    assert contract.breakthrough_model.gates[0].irreversible is True
