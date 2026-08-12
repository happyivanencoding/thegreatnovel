from __future__ import annotations

from copy import deepcopy

from novel_authoring.progression.validation import ProgressionConsistencyValidator
from novel_authoring.serial_kernel.engines import ProgressionNarrativeEngineAdapter


def _context() -> dict[str, object]:
    return {
        "effective_contracts": {
            "progression": {
                "allowed_delta_types": ["ADVANCE", "UNLOCK"],
                "primary_axis": {
                    "axis_id": "body-axis",
                    "stage_order": ["stage-one", "stage-two", "stage-three"],
                    "stage_definitions": [
                        {
                            "stage_id": "stage-one",
                            "name": "初段",
                            "status": "AVAILABLE",
                            "next_stage_candidates": ["stage-two"],
                        },
                        {
                            "stage_id": "stage-two",
                            "name": "二段",
                            "status": "AVAILABLE",
                            "next_stage_candidates": ["stage-three"],
                        },
                        {
                            "stage_id": "stage-three",
                            "name": "三段",
                            "status": "AVAILABLE",
                            "next_stage_candidates": [],
                        },
                    ],
                },
                "secondary_axes": [],
                "ability_unlock_model": [
                    {
                        "unlock_id": "stone-skin",
                        "mode": "RESOURCE",
                        "condition": "消耗矿心",
                        "effect": "石肤",
                        "provenance_required": True,
                    }
                ],
            }
        },
        "chapter_state": {
            "progression_state": {
                "primary_axis_state": {"current_stage": "stage-one"},
                "next_breakthrough_readiness": "READY_TO_ATTEMPT",
            },
            "resource_state": [{"resource_id": "ore-heart", "name": "矿心"}],
            "capability_state": [],
            "knowledge_state": [{"statement": "已知矿心淬体方法"}],
            "opportunity_surface": {"items": []},
            "world_expansion_state": {
                "current_stage": {"stage_id": "inner", "name": "矿区内环"},
                "next_stage_candidates": [
                    {"stage_id": "outer", "name": "矿区外环"}
                ],
                "transition_conditions": ["穿过坍塌带"],
            },
        },
    }


def _candidate() -> dict[str, object]:
    return {
        "progression_impact": {
            "axis_advanced": ["body-axis"],
            "progression_delta_type": ["ADVANCE", "UNLOCK"],
            "stage_change": "stage-one -> stage-two",
            "resource_change": ["消耗矿心"],
            "ability_unlock": ["stone-skin"],
            "growth_cost": ["承受不可逆的筋骨损伤"],
        },
        "chapter_intent": "BREAKTHROUGH",
        "world_expansion_impact": ["进入矿区外环"],
        "causal_sources": ["矿心与既有淬体方法"],
        "required_cost": "筋骨损伤",
        "novelty_provenance": [],
    }


def test_progression_validator_accepts_legal_transition_with_owned_resource() -> None:
    result = ProgressionConsistencyValidator().validate(_context(), _candidate())

    assert result.valid is True
    assert result.hard_errors == []
    assert result.verified_progression_impact["stage_change"] == {
        "from": "stage-one",
        "to": "stage-two",
    }
    assert result.verified_progression_impact["ability_unlocks"][0][
        "unlock_id"
    ] == "stone-skin"
    assert result.verified_progression_impact["world_expansion"] == [
        "进入矿区外环"
    ]


def test_progression_validator_rejects_fake_breakthrough_and_opportunity_ownership() -> None:
    context = _context()
    chapter_state = context["chapter_state"]
    assert isinstance(chapter_state, dict)
    progression_state = chapter_state["progression_state"]
    assert isinstance(progression_state, dict)
    progression_state["next_breakthrough_readiness"] = "UNKNOWN"
    chapter_state["resource_state"] = []
    chapter_state["opportunity_surface"] = {
        "items": [{"opportunity_id": "ore-rumor", "subject": "矿心"}]
    }
    candidate = deepcopy(_candidate())
    impact = candidate["progression_impact"]
    assert isinstance(impact, dict)
    impact["stage_change"] = "stage-one -> stage-three"
    impact["ability_unlock"] = ["不存在的天赋"]
    impact["growth_cost"] = []
    candidate["required_cost"] = ""
    candidate["world_expansion_impact"] = ["进入天穹禁区"]

    result = ProgressionConsistencyValidator().validate(context, candidate)
    engine_result = ProgressionNarrativeEngineAdapter().validate_candidate(
        candidate, context
    )

    assert result.valid is False
    assert engine_result.valid is False
    combined = "\n".join(result.hard_errors)
    assert "非法阶段跃迁" in combined
    assert "readiness=UNKNOWN" in combined
    assert "Opportunity 不能直接视为已拥有资源" in combined
    assert "AbilityUnlockModel" in combined
    assert "Growth Cost" in combined
    assert "世界层级跳跃" in combined
