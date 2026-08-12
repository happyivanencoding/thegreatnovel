from __future__ import annotations

from novel_authoring.progression.models import (
    AbilityUnlockMode,
    AbilityUnlockRule,
    BreakthroughGate,
    BreakthroughGateType,
    BreakthroughModel,
    ContractStatus,
    ExpansionStage,
    GrowthAxis,
    GrowthAxisType,
    OpportunityInformationStatus,
    OpportunityStatus,
    OpportunitySurface,
    OpportunitySurfaceItem,
    ProgressionContract,
    ProgressionDeltaType,
    ProgressionEvidence,
    ProgressionStageDefinition,
    ProgressionSubject,
    ProgressionTopology,
    QualitativeReadiness,
    WorldExpansionContract,
    WorldExpansionType,
)
from novel_authoring.progression.projections import (
    AxisObservation,
    project_progression_state,
    project_world_expansion_state,
)
from novel_authoring.progression.resources import (
    evaluate_resource_gate,
    project_opportunity_surface,
)


def progression_contract(**overrides: object) -> ProgressionContract:
    payload: dict[str, object] = {
        "progression_contract_id": "progression-body",
        "progression_subject": ProgressionSubject.CHARACTER,
        "primary_axis": GrowthAxis(
            axis_id="body-axis",
            name="肉身蜕变",
            axis_type=GrowthAxisType.BODY_EVOLUTION,
            current_stage_schema="定性生命阶段",
            stage_order=["tempered", "renewed"],
            stage_definitions=[
                ProgressionStageDefinition(
                    stage_id="tempered",
                    name="初次锻体",
                    next_stage_candidates=["renewed"],
                ),
                ProgressionStageDefinition(stage_id="renewed", name="生命重构"),
            ],
            progress_measure="正文证明的身体性质变化",
        ),
        "topology": [ProgressionTopology.LINEAR],
        "allowed_delta_types": [ProgressionDeltaType.ADVANCE],
        "stage_model": "非数字生命阶段",
        "breakthrough_model": BreakthroughModel(
            gates=[
                BreakthroughGate(
                    gate_id="body-gate",
                    gate_type=BreakthroughGateType.BODY_TRANSFORMATION,
                    requirement="身体转化成立",
                    evidence_requirements=["正文事件"],
                )
            ]
        ),
        "ability_unlock_model": [
            AbilityUnlockRule(
                unlock_id="body-unlock",
                mode=AbilityUnlockMode.STAGE,
                condition="阶段变化成立",
                effect="身体能力改变行动",
            )
        ],
        "verification_modes": ["事件验证"],
        "next_ceiling_model": "更高生命层级",
        "upper_ceiling_visibility": "PARTIAL",
        "progression_promises": ["成长改变行动可能性"],
        "status": ContractStatus.NEEDS_REVIEW,
    }
    payload.update(overrides)
    return ProgressionContract.model_validate(payload)


def world_state(chapter: int, *, ability: str | None = None) -> dict[str, object]:
    return {
        "chapter": {"chapter_id": f"chapter-{chapter}", "ordinal": chapter},
        "resources": [{"name": "星火"}],
        "inventory": [],
        "equipment": [],
        "abilities": [] if ability is None else [{"name": ability}],
        "chapter_delta": {
            "confirmed": [
                {
                    "category": "CAPABILITY",
                    "statement": f"第{chapter}章确认变化",
                }
            ]
        },
    }


def test_progression_state_is_chapter_aware_without_future_leakage() -> None:
    contract = progression_contract(
        status=ContractStatus.EFFECTIVE,
        effective_from_boundary=1,
    )
    early = project_progression_state(
        world_state(10),
        contract,
        subject_id="protagonist",
        axis_observations={
            "body-axis": AxisObservation(
                current_stage="tempered",
                readiness=QualitativeReadiness.ACCUMULATING,
                evidence=["chapter-10-span-2"],
            )
        },
    )
    late = project_progression_state(
        world_state(30, ability="星体呼吸"),
        contract,
        subject_id="protagonist",
        axis_observations={
            "body-axis": AxisObservation(
                current_stage="renewed",
                readiness=QualitativeReadiness.NEAR_GATE,
                evidence=["chapter-30-span-4"],
            )
        },
    )

    assert early is not None and late is not None
    assert early.chapter_ordinal == 10
    assert early.primary_axis_state.current_stage == "tempered"
    assert "星体呼吸" not in early.unlocked_abilities
    assert late.primary_axis_state.current_stage == "renewed"
    assert "星体呼吸" in late.unlocked_abilities


def test_future_effective_contract_does_not_rewrite_history() -> None:
    contract = progression_contract(
        status=ContractStatus.EFFECTIVE,
        effective_from_boundary=20,
    )

    assert project_progression_state(
        world_state(10), contract, subject_id="protagonist"
    ) is None
    assert project_progression_state(
        world_state(20), contract, subject_id="protagonist"
    ) is not None


def test_missing_semantic_observation_remains_unknown_not_numeric() -> None:
    state = project_progression_state(
        world_state(5),
        progression_contract(status=ContractStatus.EFFECTIVE),
        subject_id="protagonist",
    )

    assert state is not None
    assert state.primary_axis_state.readiness is QualitativeReadiness.UNKNOWN
    assert "percent" not in str(state.model_dump(mode="json")).lower()


def test_opportunity_surface_never_claims_ownership() -> None:
    surface = OpportunitySurface(
        chapter_id="chapter-12",
        chapter_ordinal=12,
        items=[
            OpportunitySurfaceItem(
                opportunity_id="opportunity-ember",
                subject="某势力可能持有突破星火",
                progression_use="满足身体重构资源门槛",
                source="已铺垫的势力线索",
                information_status=OpportunityInformationStatus.SOFT_REFERENCE,
                status=OpportunityStatus.TRACKABLE,
            )
        ],
    )

    assert surface.projection_only is True
    assert not hasattr(surface.items[0], "owned")


def test_opportunity_surface_does_not_leak_future_evidence() -> None:
    surface = project_opportunity_surface(
        world_state(12),
        [
            OpportunitySurfaceItem(
                opportunity_id="future-ember",
                subject="未来才发现的星火",
                progression_use="突破",
                source="后续章节",
                information_status=OpportunityInformationStatus.SOFT_REFERENCE,
                status=OpportunityStatus.TRACKABLE,
                evidence=[
                    {
                        "statement": "第20章才确认星火地点",
                        "chapter_ordinal": 20,
                    }
                ],
            )
        ],
    )

    assert surface.items == []


def test_resource_gate_requires_state_and_evidence() -> None:
    gate = BreakthroughGate(
        gate_id="ember-gate",
        gate_type=BreakthroughGateType.RESOURCE_GATE,
        requirement="持有并消耗星火",
        required_resources=["星火"],
        evidence_requirements=["Source State 资源证据"],
    )
    without_proof = evaluate_resource_gate(gate, world_state(12))
    with_proof = evaluate_resource_gate(
        gate,
        world_state(12),
        evidence=[
            ProgressionEvidence(
                statement="章末仍持有星火",
                chapter_ordinal=12,
            )
        ],
    )

    assert without_proof.satisfied is False
    assert without_proof.errors == ["资源缺少章节证据：星火"]
    assert with_proof.satisfied is True


def test_world_expansion_supports_non_geographic_ladder() -> None:
    contract = WorldExpansionContract(
        ladder_id="occult-world",
        stages=[
            ExpansionStage(
                stage_id="ordinary",
                name="普通社会",
                order=1,
                expansion_types=[WorldExpansionType.SOCIAL],
                world_scope="可见日常社会",
                reader_question="异常从何而来？",
            ),
            ExpansionStage(
                stage_id="hidden",
                name="秘密组织",
                order=2,
                expansion_types=[
                    WorldExpansionType.MYSTERY,
                    WorldExpansionType.KNOWLEDGE,
                ],
                world_scope="非凡组织与知识权限",
                reader_question="谁在管理秘密？",
                transition_conditions=["获得可回指的秘密组织入口"],
            ),
            ExpansionStage(
                stage_id="ontological",
                name="高层存在",
                order=3,
                expansion_types=[WorldExpansionType.ONTOLOGICAL],
                world_scope="世界真相与存在层级",
                reader_question="世界为何允许晋升？",
            ),
        ],
        current_stage_id="ordinary",
        expansion_promises=["世界随知识和身份扩大"],
        stagnation_policy="长期无新空间只产生软诊断，不规定换地图频率",
        status=ContractStatus.EFFECTIVE,
    )
    state = project_world_expansion_state(world_state(8), contract)

    assert state is not None
    assert state.current_stage.stage_id == "ordinary"
    assert state.next_stage_candidates[0].stage_id == "hidden"
    assert WorldExpansionType.GEOGRAPHIC not in (
        state.next_stage_candidates[0].expansion_types
    )
