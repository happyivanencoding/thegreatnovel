"""Deterministic consistency checks for declared progression candidate claims."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProgressionConsistencyResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valid: bool
    hard_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    verified_progression_impact: dict[str, Any] = Field(default_factory=dict)
    evidence: list[str] = Field(default_factory=list)
    canon_conflicts: list[str] = Field(default_factory=list)
    timeline_conflicts: list[str] = Field(default_factory=list)
    knowledge_violations: list[str] = Field(default_factory=list)
    missing_causal_sources: list[str] = Field(default_factory=list)
    capability_violations: list[str] = Field(default_factory=list)


def _mapping(value: object) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _mapping_list(value: object) -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        return [dict(item) for item in value.values() if isinstance(item, Mapping)]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [dict(item) for item in value if isinstance(item, Mapping)]
    return []


def _strings(value: object) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _tokens(items: Sequence[Mapping[str, Any]]) -> set[str]:
    result: set[str] = set()
    for item in items:
        for key in (
            "id",
            "resource_id",
            "object_id",
            "capability_id",
            "opportunity_id",
            "stage_id",
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


def _stage_target(value: str) -> str:
    parts = [item.strip() for item in re.split(r"(?:->|→|=>|至|到)", value) if item.strip()]
    return parts[-1] if parts else value.strip()


def _forward_introductions(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in _mapping_list(candidate.get("novelty_provenance"))
        if str(item.get("provenance")) == "FORWARD_NOVELTY"
        and str(item.get("novelty_boundary")) != "RETROACTIVE_UNSUPPORTED_INVENTION"
        and str(item.get("introduction_event") or "").strip()
        and str(item.get("causal_source") or "").strip()
        and str(item.get("new_state_if_committed") or "").strip()
    ]


def _forward_matches(claim: str, introductions: Sequence[Mapping[str, Any]]) -> bool:
    normalized = claim.casefold()
    return any(
        normalized in " ".join(str(value).casefold() for value in item.values())
        or any(
            token in normalized
            for token in re.findall(
                r"[\w\u4e00-\u9fff]{2,}",
                str(item.get("new_state_if_committed") or "").casefold(),
            )
        )
        for item in introductions
    )


def _claims_successful_ownership(claim: str) -> bool:
    normalized = claim.casefold()
    return any(
        word in normalized
        for word in ("获得", "拥有", "消耗", "使用", "炼化", "acquire", "owned", "consume", "use")
    )


class ProgressionConsistencyValidator:
    """Validate claims against a frozen Kernel Context without mutating state."""

    def validate(
        self,
        context: Mapping[str, Any],
        candidate: Mapping[str, Any],
    ) -> ProgressionConsistencyResult:
        effective = _mapping(context.get("effective_contracts"))
        contract = _mapping(effective.get("progression"))
        impact = _mapping(candidate.get("progression_impact"))
        chapter_state = _mapping(context.get("chapter_state"))
        progression_state = _mapping(chapter_state.get("progression_state"))
        declared_claims = any(
            impact.get(name)
            for name in (
                "axis_advanced",
                "progression_delta_type",
                "stage_change",
                "branch_change",
                "resource_change",
                "ability_unlock",
                "growth_cost",
            )
        )
        if not contract:
            return ProgressionConsistencyResult(
                valid=True,
                warnings=(
                    [
                        "没有 Effective Progression Contract；成长声明保持 "
                        "UNVERIFIED，Legacy 流程不阻断。"
                    ]
                    if declared_claims
                    else []
                ),
                verified_progression_impact={"status": "NOT_APPLICABLE"},
            )

        hard: list[str] = []
        warnings: list[str] = []
        evidence: list[str] = []
        canon: list[str] = []
        timeline: list[str] = []
        knowledge: list[str] = []
        missing_causal: list[str] = []
        capability: list[str] = []
        verified: dict[str, Any] = {
            "axis_advanced": [],
            "progression_delta_type": [],
            "stage_change": None,
            "resource_changes": [],
            "ability_unlocks": [],
            "ability_showcases": [],
            "growth_costs": [],
            "world_expansion": [],
        }

        allowed_delta_types = {str(item) for item in contract.get("allowed_delta_types", [])}
        for delta_type in _strings(impact.get("progression_delta_type")):
            if delta_type not in allowed_delta_types:
                message = f"Progression Delta {delta_type} 不在 Effective Contract 允许范围"
                hard.append(message)
                capability.append(message)
            else:
                verified["progression_delta_type"].append(delta_type)
                evidence.append(f"allowed_delta_type:{delta_type}")

        primary_axis = _mapping(contract.get("primary_axis"))
        state_axis = _mapping(progression_state.get("primary_axis_state"))
        stage_definitions = _mapping_list(primary_axis.get("stage_definitions"))
        stage_by_token: dict[str, dict[str, Any]] = {}
        for stage in stage_definitions:
            for value in (stage.get("stage_id"), stage.get("name")):
                if value:
                    stage_by_token[str(value).casefold()] = stage
        current_stage_value = str(state_axis.get("current_stage") or "").strip()
        current_stage = stage_by_token.get(current_stage_value.casefold())
        stage_change = str(impact.get("stage_change") or "").strip()
        valid_stage_change = False
        if stage_change:
            target_value = _stage_target(stage_change)
            target_stage = stage_by_token.get(target_value.casefold())
            if target_stage is None:
                message = f"目标成长阶段不属于当前 Growth Axis：{target_value}"
                hard.append(message)
                timeline.append(message)
            elif current_stage is None:
                message = "当前成长阶段为 UNKNOWN，不能声明成功阶段跃迁"
                hard.append(message)
                timeline.append(message)
            else:
                allowed_next = {
                    str(item)
                    for item in current_stage.get("next_stage_candidates", [])
                }
                stage_order = [str(item) for item in primary_axis.get("stage_order", [])]
                current_id = str(current_stage.get("stage_id") or "")
                if not allowed_next and current_id in stage_order:
                    index = stage_order.index(current_id)
                    if index + 1 < len(stage_order):
                        allowed_next.add(stage_order[index + 1])
                target_id = str(target_stage.get("stage_id") or "")
                if target_id not in allowed_next:
                    message = f"非法阶段跃迁：{current_id} -> {target_id}"
                    hard.append(message)
                    timeline.append(message)
                elif str(target_stage.get("status") or "AVAILABLE") != "AVAILABLE":
                    message = f"目标阶段当前不可进入：{target_id}"
                    hard.append(message)
                    timeline.append(message)
                else:
                    valid_stage_change = True
                    verified["stage_change"] = {
                        "from": current_id,
                        "to": target_id,
                    }
                    evidence.append(f"legal_stage_transition:{current_id}->{target_id}")

        chapter_intent = str(candidate.get("chapter_intent") or "")
        breakthrough_claimed = bool(stage_change) or chapter_intent == "BREAKTHROUGH"
        if breakthrough_claimed:
            readiness = str(
                progression_state.get("next_breakthrough_readiness") or "UNKNOWN"
            )
            if readiness not in {"GATE_SATISFIED", "READY_TO_ATTEMPT"}:
                message = f"突破门槛尚未满足：readiness={readiness}"
                hard.append(message)
                capability.append(message)
            else:
                evidence.append(f"breakthrough_readiness:{readiness}")

        resource_items = _mapping_list(chapter_state.get("resource_state"))
        owned_tokens = _tokens(resource_items)
        opportunity = _mapping(chapter_state.get("opportunity_surface"))
        opportunity_tokens = _tokens(_mapping_list(opportunity.get("items")))
        introductions = _forward_introductions(candidate)
        resource_claims = _strings(impact.get("resource_change"))
        for claim in resource_claims:
            if _matches(claim, owned_tokens):
                verified["resource_changes"].append(
                    {"claim": claim, "source": "CURRENT_OWNED_RESOURCE"}
                )
                evidence.append(f"owned_resource:{claim}")
            elif _matches(claim, opportunity_tokens):
                if _claims_successful_ownership(claim):
                    message = f"Opportunity 不能直接视为已拥有资源：{claim}"
                    hard.append(message)
                    capability.append(message)
                else:
                    verified["resource_changes"].append(
                        {"claim": claim, "source": "OPPORTUNITY_ONLY"}
                    )
                    evidence.append(f"opportunity_not_owned:{claim}")
            elif _forward_matches(claim, introductions):
                verified["resource_changes"].append(
                    {"claim": claim, "source": "VALID_FORWARD_INTRODUCTION"}
                )
                evidence.append(f"forward_resource:{claim}")
            else:
                message = f"资源变化没有当前持有状态或合法 Forward Introduction：{claim}"
                hard.append(message)
                missing_causal.append(message)

        known_abilities = _tokens(_mapping_list(chapter_state.get("capability_state")))
        unlock_rules = _mapping_list(contract.get("ability_unlock_model"))
        ability_claims = _strings(impact.get("ability_unlock"))
        knowledge_items = _mapping_list(chapter_state.get("knowledge_state"))
        knowledge_tokens = _tokens(knowledge_items)
        causal_sources = _strings(candidate.get("causal_sources"))
        for claim in ability_claims:
            if _matches(claim, known_abilities):
                message = f"能力已存在，不能倒写为本章新解锁：{claim}"
                hard.append(message)
                canon.append(message)
                continue
            matching_rules = [
                rule
                for rule in unlock_rules
                if _matches(
                    claim,
                    {
                        str(rule.get("unlock_id") or "").casefold(),
                        str(rule.get("condition") or "").casefold(),
                        str(rule.get("effect") or "").casefold(),
                    }
                    - {""},
                )
            ]
            forward = _forward_matches(claim, introductions)
            if not matching_rules:
                message = f"能力解锁不符合 AbilityUnlockModel：{claim}"
                hard.append(message)
                capability.append(message)
                continue
            rule = matching_rules[0]
            mode = str(rule.get("mode") or "")
            condition = str(rule.get("condition") or "").strip()
            if bool(rule.get("provenance_required", True)) and not (
                forward
                or any(
                    _matches(
                        source,
                        owned_tokens
                        | knowledge_tokens
                        | known_abilities
                        | ({current_stage_value.casefold()} if current_stage_value else set()),
                    )
                    for source in causal_sources
                )
            ):
                message = f"能力解锁缺少 provenance：{claim}"
                hard.append(message)
                missing_causal.append(message)
            elif mode == "KNOWLEDGE" and not (
                forward or (knowledge_tokens and _matches(condition, knowledge_tokens))
            ):
                message = f"知识边界不足以支持能力解锁：{claim}"
                hard.append(message)
                knowledge.append(message)
            elif mode == "RESOURCE" and not (
                forward or (owned_tokens and _matches(condition, owned_tokens))
            ):
                message = f"能力解锁所需资源未满足：{claim}"
                hard.append(message)
                capability.append(message)
            elif mode == "STAGE" and current_stage is None and not valid_stage_change:
                message = f"能力解锁所需阶段为 UNKNOWN：{claim}"
                hard.append(message)
                capability.append(message)
            else:
                verified["ability_unlocks"].append(
                    {"claim": claim, "unlock_id": rule.get("unlock_id"), "mode": mode}
                )
                evidence.append(f"ability_unlock_rule:{rule.get('unlock_id')}")

        verified_unlock_tokens = _tokens(verified["ability_unlocks"])
        for claim in _strings(impact.get("ability_showcase")):
            if _matches(claim, known_abilities):
                verified["ability_showcases"].append(
                    {"claim": claim, "source": "CURRENT_CAPABILITY"}
                )
                evidence.append(f"current_ability_showcase:{claim}")
            elif _matches(claim, verified_unlock_tokens):
                verified["ability_showcases"].append(
                    {"claim": claim, "source": "VERIFIED_SAME_CHAPTER_UNLOCK"}
                )
                evidence.append(f"new_ability_showcase:{claim}")
            else:
                message = f"能力展示超出当前章节 Capability Boundary：{claim}"
                hard.append(message)
                capability.append(message)

        costs = _strings(impact.get("growth_cost"))
        if (valid_stage_change or ability_claims or introductions) and not (
            costs or str(candidate.get("required_cost") or "").strip()
        ):
            message = "阶段、能力或未来资源变化缺少 Growth Cost"
            hard.append(message)
            capability.append(message)
        else:
            verified["growth_costs"] = costs

        world_state = _mapping(chapter_state.get("world_expansion_state"))
        world_claims = _strings(candidate.get("world_expansion_impact"))
        next_stages = _mapping_list(world_state.get("next_stage_candidates"))
        next_tokens = _tokens(next_stages)
        current_world = _mapping(world_state.get("current_stage"))
        world_bridge_tokens = _tokens([current_world]) | {
            item.casefold()
            for item in _strings(world_state.get("transition_conditions"))
        }
        for claim in world_claims:
            claims_transition = any(
                word in claim.casefold()
                for word in ("进入", "打开", "扩张", "抵达", "跃迁", "enter", "expand", "advance")
            )
            if not claims_transition:
                warnings.append(f"世界扩张声明仅视为铺垫：{claim}")
                continue
            if not world_state:
                message = f"没有可验证的 World Expansion State：{claim}"
                hard.append(message)
                timeline.append(message)
            elif not _matches(claim, next_tokens):
                message = f"世界层级跳跃不属于 next candidates：{claim}"
                hard.append(message)
                timeline.append(message)
            elif not any(
                _matches(source, world_bridge_tokens) for source in causal_sources
            ):
                message = f"世界扩张缺少当前状态到下一层的因果桥梁：{claim}"
                hard.append(message)
                missing_causal.append(message)
            else:
                verified["world_expansion"].append(claim)
                evidence.append(
                    "world_transition:"
                    f"{current_world.get('stage_id', 'UNKNOWN')}->{claim}"
                )

        for delta_type in verified["progression_delta_type"]:
            if delta_type in {"LOCK_OUT", "SACRIFICE", "TRANSFORM"} and not (
                costs or str(candidate.get("required_cost") or "").strip()
            ):
                message = f"{delta_type} 必须记录不可逆代价"
                hard.append(message)
                capability.append(message)

        verified["axis_advanced"] = [
            axis
            for axis in _strings(impact.get("axis_advanced"))
            if axis == str(primary_axis.get("axis_id") or "")
            or axis in {
                str(item.get("axis_id") or "")
                for item in _mapping_list(contract.get("secondary_axes"))
            }
        ]
        unknown_axes = set(_strings(impact.get("axis_advanced"))) - set(
            verified["axis_advanced"]
        )
        for axis in sorted(unknown_axes):
            message = f"候选引用未知 Growth Axis：{axis}"
            hard.append(message)
            capability.append(message)

        deduplicated_hard = list(dict.fromkeys(hard))
        return ProgressionConsistencyResult(
            valid=not deduplicated_hard,
            hard_errors=deduplicated_hard,
            warnings=list(dict.fromkeys(warnings)),
            verified_progression_impact=verified,
            evidence=list(dict.fromkeys(evidence)),
            canon_conflicts=list(dict.fromkeys(canon)),
            timeline_conflicts=list(dict.fromkeys(timeline)),
            knowledge_violations=list(dict.fromkeys(knowledge)),
            missing_causal_sources=list(dict.fromkeys(missing_causal)),
            capability_violations=list(dict.fromkeys(capability)),
        )


__all__ = ["ProgressionConsistencyResult", "ProgressionConsistencyValidator"]
