from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(r"C:\dev\tgn-story-mvp")
OUT = ROOT / "books" / "real-exp-atomic-authority-ir-20260829-v1" / "phase-a-static-ir"

sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    AtomicAuthorityContractBuilder,
    AuthorityFact,
    EntityRegistry,
    PatchKind,
    PatchOperation,
    PreservationProvenance,
    ProtectionHint,
    RepairTarget,
    bind_primary_realization,
    build_primary_preservation_map,
    freeze_canon_artifact,
    freeze_human_artifact,
    freeze_mission_artifact,
    freeze_power_artifact,
    freeze_reader_release_artifact,
    freeze_world_artifact,
    save_json,
    split_paragraphs,
    validate_primary_preservation,
)


def authority_ref(name: str) -> list[str]:
    return [name]


FREEZE_BY_SOURCE = {
    "frozen_mission": ("mission", freeze_mission_artifact),
    "canon": ("canon", freeze_canon_artifact),
    "world_authority": ("world", freeze_world_artifact),
    "power_authority": ("power", freeze_power_artifact),
    "human_authority": ("human", freeze_human_artifact),
    "reader_release": ("reader_release", freeze_reader_release_artifact),
}


def frozen_artifact_from_fragment(
    fragment: Mapping[str, Any],
    *,
    artifact_suffix: str,
):
    source = str(fragment["source"])
    try:
        prefix, factory = FREEZE_BY_SOURCE[source]
    except KeyError as exc:
        raise ValueError(f"unsupported fixture source={source!r}") from exc
    return factory(
        f"{prefix}:fixture:{artifact_suffix}",
        fragment.get("facts", []),
    )


def registry_payload(
    chapter_id: str,
    protagonist_name: str,
    entities: Sequence[tuple[str, str, str, Sequence[str], str]],
) -> dict[str, Any]:
    rows = [
        {
            "entity_id": "PROTAGONIST_001",
            "kind": "character",
            "display_name": protagonist_name,
            "aliases": ["他", "本体", "主角"],
            "authority_refs": authority_ref("canon.protagonist"),
        }
    ]
    for entity_id, kind, display_name, aliases, parent in entities:
        row = {
            "entity_id": entity_id,
            "kind": kind,
            "display_name": display_name,
            "aliases": list(aliases),
            "authority_refs": authority_ref(f"authority.entity.{entity_id}"),
        }
        if parent:
            row["parent_entity_id"] = parent
        rows.append(row)
    return {
        "schema_version": "entity-registry-v1",
        "chapter_id": chapter_id,
        "protagonist_id": "PROTAGONIST_001",
        "entities": rows,
    }


def fact(
    fact_id: str,
    slot_id: str,
    source_ref: str,
    kind: str,
    mode: str,
    phase: str,
    *,
    actor_id: str = "",
    action_id: str = "",
    object_ids: Sequence[str] = (),
    counterparty_ids: Sequence[str] = (),
    from_state: str = "",
    to_state: str = "",
    value: Any = None,
    terminal: bool = False,
    condition_fact_ids: Sequence[str] = (),
    depends_on_fact_ids: Sequence[str] = (),
    condition_slots: Sequence[str] = (),
    depends_on_slots: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "fact_id": fact_id,
        "slot_id": slot_id,
        "source_ref": source_ref,
        "kind": kind,
        "mode": mode,
        "phase": phase,
        "actor_id": actor_id,
        "action_id": action_id,
        "object_ids": list(object_ids),
        "counterparty_ids": list(counterparty_ids),
        "from_state": from_state,
        "to_state": to_state,
        "value": value,
        "terminal": terminal,
        "condition_fact_ids": list(condition_fact_ids),
        "depends_on_fact_ids": list(depends_on_fact_ids),
        "condition_slots": list(condition_slots),
        "depends_on_slots": list(depends_on_slots),
        "metadata": dict(metadata or {}),
    }


def sample_specs() -> list[dict[str, Any]]:
    fast_book = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
    second_book = ROOT / "books" / "real-exp-current-pipeline-authority-reviser-0010-20260828-v1" / "runs"

    fast14_registry = registry_payload(
        "JIUCHUI:CH014",
        "顾停舟",
        (
            ("ITEM_RETURN_TIDE_WEDGE_001", "item", "回潮楔", ("楔子", "古器"), ""),
            ("CHAR_RIVAL_001", "character", "阮青蜃", (), ""),
            ("CHAR_PARTNER_001", "character", "少东家", (), ""),
            ("ORG_HUNDRED_FURNACE_001", "organization", "百炉会", (), ""),
            ("RESOURCE_PERSONAL_MINING_SHARE_001", "resource", "个人矿利", ("矿利份额",), ""),
            ("ROUTE_GRAIN_001", "route", "粮路", ("粮道",), ""),
            ("LOCATION_OLD_PASS_001", "location", "旧关", (), ""),
            ("EVENT_NEXT_TIDE_001", "event", "下一次十二日地潮", (), ""),
        ),
    )
    fast14_fragments = [
        {
            "source": "canon",
            "facts": [
                fact(
                    "J14_CANON_WEDGE_POSSESSION",
                    "ownership:ITEM_RETURN_TIDE_WEDGE_001",
                    "canon.item.current_holder",
                    "ownership_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="possess",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    to_state="possessed_by_protagonist_disputed",
                ),
                fact(
                    "J14_CANON_MINING_SHARE_NONE",
                    "resource:RESOURCE_PERSONAL_MINING_SHARE_001",
                    "canon.resource.personal_mining_share",
                    "resource_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_without_entitlement",
                    object_ids=("RESOURCE_PERSONAL_MINING_SHARE_001",),
                    to_state="none",
                ),
                fact(
                    "J14_CANON_PARTNERSHIP_STATE",
                    "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
                    "canon.relationship.young_master",
                    "relationship_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_former_master_subordinate",
                    counterparty_ids=("CHAR_PARTNER_001",),
                    to_state="former_master_subordinate",
                ),
            ],
        },
        {
            "source": "power_authority",
            "facts": [
                fact(
                    "J14_POWER_SINGLE_USE_BOUNDARY",
                    "ability:ITEM_RETURN_TIDE_WEDGE_001:use_cycle",
                    "power.return_tide_wedge.single_use",
                    "ability_boundary",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="use_single_lock_redirect_release_cycle",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    value={"max_cycles_this_chapter": 1, "requires_cooldown_after": True},
                )
            ],
        },
        {
            "source": "frozen_mission",
            "facts": [
                fact(
                    "J14_MISSION_USE_WEDGE_ONCE",
                    "event:J14:wedge_use",
                    "mission.action.1",
                    "action",
                    "must_hold",
                    "during_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="lock_redirect_release_tide_once",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                ),
                fact(
                    "J14_RESULT_PUBLIC_PROOF",
                    "public_proof:J14:wedge",
                    "mission.world_reaction.1",
                    "public_proof",
                    "must_hold",
                    "during_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="publicly_prove_direction_change_value",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    depends_on_fact_ids=("J14_MISSION_USE_WEDGE_ONCE",),
                    metadata={
                        "performance_fact_id": "J14_MISSION_USE_WEDGE_ONCE",
                        "ruler": "qualified_furnace_expert",
                        "required_consequence": "behavioral_repricing",
                    },
                ),
                fact(
                    "J14_RESULT_WEDGE_AUTONOMY",
                    "ownership:ITEM_RETURN_TIDE_WEDGE_001",
                    "mission.direct_result.1",
                    "ownership_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="retain_autonomous_use",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    from_state="possessed_by_protagonist_disputed",
                    to_state="autonomous_use_retained_publicly",
                    terminal=True,
                ),
                fact(
                    "J14_RESULT_MINING_SHARE",
                    "resource:RESOURCE_PERSONAL_MINING_SHARE_001",
                    "mission.direct_result.2",
                    "resource_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="confirm_entitlement",
                    object_ids=("RESOURCE_PERSONAL_MINING_SHARE_001",),
                    from_state="none",
                    to_state="entitlement_confirmed_not_cash_received",
                    terminal=True,
                    metadata={"payment_state": "entitlement_confirmed"},
                ),
                fact(
                    "J14_STATE_PARTNERSHIP",
                    "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
                    "mission.state_change.1",
                    "relationship_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="transition_relationship",
                    counterparty_ids=("CHAR_PARTNER_001",),
                    from_state="former_master_subordinate",
                    to_state="paid_independent_cooperation",
                    terminal=True,
                ),
                fact(
                    "J14_STATE_WEDGE_COOLDOWN",
                    "ability:ITEM_RETURN_TIDE_WEDGE_001:cooldown",
                    "mission.state_change.2",
                    "ability_boundary",
                    "must_hold",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="require_residual_pressure_dissipation_before_reuse",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    to_state="cooldown_pending",
                ),
                fact(
                    "J14_ENDING_DEPART",
                    "ending:J14:departure",
                    "mission.ending.1",
                    "ending",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="depart_with_grain_convoy",
                    object_ids=("ROUTE_GRAIN_001", "LOCATION_OLD_PASS_001"),
                    terminal=True,
                ),
                fact(
                    "J14_DEADLINE_NEXT_TIDE",
                    "deadline:J14:grain_delivery",
                    "mission.ending.2",
                    "deadline",
                    "must_hold",
                    "post_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="deliver_before_event",
                    object_ids=("ROUTE_GRAIN_001", "EVENT_NEXT_TIDE_001"),
                    metadata={"relation": "before"},
                ),
            ],
        },
    ]

    fast16_registry = registry_payload(
        "JIUCHUI:CH016",
        "顾停舟",
        (
            ("CLONE_001", "manifestation", "分身", ("借身",), "PROTAGONIST_001"),
            ("ITEM_RETURN_TIDE_WEDGE_001", "item", "回潮楔", ("楔子",), ""),
            ("ROUTE_GRAIN_001", "route", "粮道", ("粮路",), ""),
            ("RESOURCE_WELLS_001", "resource", "三座新潮井", ("三座井",), ""),
            ("ROUTE_WATER_001", "route", "砺骨部迁徙水路", ("水路",), ""),
            ("LOCATION_SECOND_PRESSURE_NODE_001", "location", "第二个潮压节点", (), ""),
            ("LOCATION_OUTER_PASS_001", "location", "旧关外层", ("外层",), ""),
            ("LOCATION_OBSERVATION_POINT_001", "location", "旧关内侧观测点", ("观测点",), ""),
            ("MYSTERY_EARLY_TIDE_001", "mystery", "地潮提前原因", (), ""),
        ),
    )
    fast16_fragments = [
        {
            "source": "canon",
            "facts": [
                fact(
                    "J16_CANON_WEDGE_POSSESSION",
                    "ownership:ITEM_RETURN_TIDE_WEDGE_001",
                    "canon.item.current_holder",
                    "ownership_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="possess",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    to_state="possessed_by_protagonist",
                ),
                fact(
                    "J16_CANON_OUTER_PASS_USABLE",
                    "state:LOCATION_OUTER_PASS_001",
                    "canon.location.outer_pass",
                    "state_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="outer_pass_remains_usable",
                    object_ids=("LOCATION_OUTER_PASS_001",),
                    to_state="usable",
                ),
            ],
        },
        {
            "source": "power_authority",
            "facts": [
                fact(
                    "J16_POWER_CLONE_LIMIT",
                    "ability:CLONE_001:carried_power",
                    "power.clone.current_limit",
                    "ability_boundary",
                    "must_hold",
                    "pre_chapter",
                    actor_id="CLONE_001",
                    action_id="carry_stabilize_only",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    value={"allowed": ["stabilize"], "full_body_power": False},
                )
            ],
        },
        {
            "source": "frozen_mission",
            "facts": [
                fact(
                    "J16_ACTION_BODY_STABILIZE",
                    "event:J16:body_stabilize",
                    "mission.action.1",
                    "action",
                    "must_hold",
                    "during_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="stabilize_routes",
                    object_ids=("ROUTE_GRAIN_001", "ROUTE_WATER_001"),
                ),
                fact(
                    "J16_ACTION_CLONE_FIX_WEDGE",
                    "event:J16:clone_fix_wedge",
                    "mission.action.2",
                    "action",
                    "must_hold",
                    "during_chapter",
                    actor_id="CLONE_001",
                    action_id="carry_and_fix_item_at_node",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001", "LOCATION_SECOND_PRESSURE_NODE_001"),
                ),
                fact(
                    "J16_RESULT_RESOURCES_SAVED",
                    "result:J16:resources",
                    "mission.direct_result.1",
                    "direct_result",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="preserve_resources",
                    object_ids=("ROUTE_GRAIN_001", "RESOURCE_WELLS_001", "ROUTE_WATER_001"),
                    to_state="preserved",
                    terminal=True,
                ),
                fact(
                    "J16_RESULT_OUTER_PASS_SACRIFICED",
                    "state:LOCATION_OUTER_PASS_001",
                    "mission.direct_result.2",
                    "state_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="redirect_tide_and_sacrifice",
                    object_ids=("LOCATION_OUTER_PASS_001",),
                    from_state="usable",
                    to_state="destroyed",
                    terminal=True,
                ),
                fact(
                    "J16_RESULT_WEDGE_RETAINED",
                    "ownership:ITEM_RETURN_TIDE_WEDGE_001",
                    "mission.direct_result.3",
                    "ownership_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="retain_possession",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    from_state="possessed_by_protagonist",
                    to_state="possessed_by_protagonist",
                    terminal=True,
                ),
                fact(
                    "J16_STATE_WEDGE_COOLDOWN",
                    "ability:ITEM_RETURN_TIDE_WEDGE_001:cooldown",
                    "mission.direct_result.4",
                    "ability_boundary",
                    "must_hold",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="require_residual_pressure_dissipation_before_reuse",
                    object_ids=("ITEM_RETURN_TIDE_WEDGE_001",),
                    to_state="cooldown_pending",
                ),
                fact(
                    "J16_UNKNOWN_EARLY_TIDE_CAUSE",
                    "mystery:MYSTERY_EARLY_TIDE_001",
                    "mission.state_change.unknown.1",
                    "unknown_boundary",
                    "must_remain_unknown",
                    "chapter_end",
                    object_ids=("MYSTERY_EARLY_TIDE_001",),
                    to_state="unknown",
                ),
                fact(
                    "J16_ENDING_ENTER_OBSERVATION",
                    "ending:J16:observation",
                    "mission.ending.1",
                    "ending",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="enter_observation_point",
                    object_ids=("LOCATION_OBSERVATION_POINT_001",),
                    terminal=True,
                ),
            ],
        },
    ]

    second4_registry = registry_payload(
        "SHADOW:CH004",
        "顾临川",
        (
            ("CHAR_OPPONENT_001", "character", "杜衡", (), ""),
            ("CHAR_PARTNER_001", "character", "陆绾", (), ""),
            ("ORG_COPPER_FEATHER_001", "organization", "铜羽商盟", ("铜羽",), ""),
            ("CONTRACT_ESCORT_001", "contract", "铜羽随队契约", ("随队契约", "契券"), ""),
            ("RESOURCE_PREPAYMENT_001", "resource", "第一笔预付钱", ("预付款",), ""),
            ("ABILITY_SHADOW_CLONE_001", "ability", "分影", ("影身",), ""),
            ("TIER_FIRST_001", "power_tier", "正式一阶", ("一阶",), ""),
            ("ROUTE_CANYON_001", "route", "折日峡路线", ("折日峡",), ""),
            ("GROUP_MEDICINE_CONVOY_001", "group", "药队", (), ""),
        ),
    )
    second4_fragments = [
        {
            "source": "canon",
            "facts": [
                fact(
                    "S4_CANON_POWER_TIER",
                    "power:PROTAGONIST_001",
                    "canon.power.current",
                    "state_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_at_tier",
                    object_ids=("TIER_FIRST_001",),
                    to_state="TIER_FIRST_001",
                ),
                fact(
                    "S4_CANON_CONTRACT_NONE",
                    "ownership:CONTRACT_ESCORT_001",
                    "canon.contract.escort",
                    "ownership_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_without_contract",
                    object_ids=("CONTRACT_ESCORT_001",),
                    to_state="none",
                ),
                fact(
                    "S4_CANON_PREPAYMENT_NOT_PAID",
                    "resource:RESOURCE_PREPAYMENT_001",
                    "canon.resource.first_prepayment",
                    "resource_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_unpaid",
                    object_ids=("RESOURCE_PREPAYMENT_001",),
                    to_state="not_paid",
                ),
                fact(
                    "S4_CANON_PARTNER_RELATION",
                    "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
                    "canon.relationship.partner",
                    "relationship_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_ordinary_guard_relation",
                    counterparty_ids=("CHAR_PARTNER_001",),
                    to_state="ordinary_guard_relation",
                ),
            ],
        },
        {
            "source": "world_authority",
            "facts": [
                fact(
                    "S4_WORLD_CONTRACT_ENTRY",
                    "world:CONTRACT_ESCORT_001:entry_value",
                    "world.contract.cross_city_entry",
                    "state_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="contract_enables_cross_city_entry",
                    object_ids=("CONTRACT_ESCORT_001", "ORG_COPPER_FEATHER_001"),
                    value={"enables": ["lodging", "trade", "escort_entry"]},
                )
            ],
        },
        {
            "source": "power_authority",
            "facts": [
                fact(
                    "S4_POWER_REMAIN_TIER_ONE",
                    "power:PROTAGONIST_001",
                    "power.current.no_transition",
                    "ability_boundary",
                    "must_hold",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_at_stable_tier",
                    object_ids=("TIER_FIRST_001",),
                    from_state="TIER_FIRST_001",
                    to_state="TIER_FIRST_001",
                )
            ],
        },
        {
            "source": "frozen_mission",
            "facts": [
                fact(
                    "S4_ACTION_DEFEAT_DUHENG",
                    "event:S4:defeat_opponent",
                    "mission.action.1",
                    "action",
                    "must_hold",
                    "during_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="defeat_under_fatigue",
                    object_ids=("CHAR_OPPONENT_001",),
                ),
                fact(
                    "S4_RESULT_PUBLIC_RANK",
                    "result:S4:public_rank",
                    "mission.direct_result.1",
                    "direct_result",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="win_public_rank",
                    object_ids=("ORG_COPPER_FEATHER_001",),
                    terminal=True,
                ),
                fact(
                    "S4_RESULT_CONTRACT_RECEIVED",
                    "ownership:CONTRACT_ESCORT_001",
                    "mission.direct_result.2",
                    "resource_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="receive_contract",
                    object_ids=("CONTRACT_ESCORT_001",),
                    from_state="none",
                    to_state="received",
                    terminal=True,
                ),
                fact(
                    "S4_RESULT_FIRST_PREPAYMENT_RECEIVED",
                    "resource:RESOURCE_PREPAYMENT_001",
                    "mission.direct_result.3",
                    "resource_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="receive_partial_prepayment",
                    object_ids=("RESOURCE_PREPAYMENT_001",),
                    from_state="not_paid",
                    to_state="first_payment_received",
                    terminal=True,
                    metadata={"fulfillment": "explicit_partial", "amount": None},
                ),
                fact(
                    "S4_ACTION_REVEAL_CLONE_TO_PARTNER",
                    "knowledge:CHAR_PARTNER_001:ABILITY_SHADOW_CLONE_001",
                    "mission.action.2",
                    "action",
                    "must_hold",
                    "during_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="reveal_ability",
                    object_ids=("ABILITY_SHADOW_CLONE_001",),
                    counterparty_ids=("CHAR_PARTNER_001",),
                ),
                fact(
                    "S4_STATE_PARTNER_DECIDES_TRAVEL",
                    "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
                    "mission.state_change.1",
                    "relationship_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="partner_decides同行",
                    counterparty_ids=("CHAR_PARTNER_001",),
                    from_state="ordinary_guard_relation",
                    to_state="同行药队",
                    terminal=True,
                ),
                fact(
                    "S4_ENDING_DEPART_NEXT_DAY",
                    "ending:S4:departure",
                    "mission.ending.1",
                    "deadline",
                    "must_hold",
                    "post_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="depart_next_day_via_changed_route",
                    object_ids=("ROUTE_CANYON_001", "GROUP_MEDICINE_CONVOY_001"),
                    metadata={"timing": "next_day", "not_current_terminal_departure": True},
                ),
            ],
        },
        {
            "source": "reader_release",
            "facts": [
                fact(
                    "S4_READER_RELEASE_CONTRACT_VALUE",
                    "reader_release:S4:contract_entry",
                    "reader_release.chapter4.1",
                    "reader_release",
                    "must_hold",
                    "reader_knowledge",
                    action_id="reader_learns_contract_entry_value",
                    object_ids=("CONTRACT_ESCORT_001", "ORG_COPPER_FEATHER_001"),
                    depends_on_slots=(
                        "ownership:CONTRACT_ESCORT_001",
                        "world:CONTRACT_ESCORT_001:entry_value",
                    ),
                )
            ],
        },
    ]

    second9_registry = registry_payload(
        "SHADOW:CH009",
        "顾临川",
        (
            ("CHAR_PARTNER_001", "character", "陆绾", (), ""),
            ("CHAR_RIVAL_001", "character", "顾斜阳", (), ""),
            ("ITEM_UMBRA_WEAPON_001", "item", "乌沉短兵", ("短兵",), ""),
            ("ABILITY_SHADOW_CLONE_001", "ability", "分影", ("影身",), ""),
            ("STATE_INJURY_001", "resource", "伤势", ("伤口", "疲劳"), ""),
            ("RECORD_ESCORT_001", "item", "撤离记录", ("记录",), ""),
            ("ORG_COPPER_FEATHER_001", "organization", "铜羽商盟", ("铜羽",), ""),
        ),
    )
    second9_fragments = [
        {
            "source": "canon",
            "facts": [
                fact(
                    "S9_CANON_INJURY_ACUTE",
                    "state:STATE_INJURY_001",
                    "canon.state.injury",
                    "state_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_acutely_injured",
                    object_ids=("STATE_INJURY_001",),
                    to_state="acute",
                ),
                fact(
                    "S9_CANON_PARTNER_IMPLICIT_TRUST",
                    "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
                    "canon.relationship.partner",
                    "relationship_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_implicit_trust",
                    counterparty_ids=("CHAR_PARTNER_001",),
                    to_state="implicit_trust",
                ),
                fact(
                    "S9_CANON_RIVAL_UNKNOWN_COMPETITOR",
                    "relationship:PROTAGONIST_001:CHAR_RIVAL_001",
                    "canon.relationship.rival",
                    "relationship_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_unknown_competitor",
                    counterparty_ids=("CHAR_RIVAL_001",),
                    to_state="unknown_competitor",
                ),
            ],
        },
        {
            "source": "power_authority",
            "facts": [
                fact(
                    "S9_POWER_CLONE_DAMAGE_RETURNS",
                    "ability:ABILITY_SHADOW_CLONE_001:damage_return",
                    "power.clone.damage_return",
                    "ability_boundary",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="clone_damage_returns_to_body",
                    object_ids=("ABILITY_SHADOW_CLONE_001", "STATE_INJURY_001"),
                    value={"damage_is_real": True},
                )
            ],
        },
        {
            "source": "frozen_mission",
            "facts": [
                fact(
                    "S9_ACTION_ACCEPT_TREATMENT",
                    "event:S9:treatment",
                    "mission.action.1",
                    "action",
                    "must_hold",
                    "during_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="accept_treatment",
                    object_ids=("STATE_INJURY_001",),
                    counterparty_ids=("CHAR_PARTNER_001",),
                ),
                fact(
                    "S9_RESULT_ADMIT_MIXED_MOTIVE",
                    "result:S9:motive_admission",
                    "mission.direct_result.1",
                    "direct_result",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="admit_wants_weapon_and_partner_survival",
                    object_ids=("ITEM_UMBRA_WEAPON_001",),
                    counterparty_ids=("CHAR_PARTNER_001",),
                    terminal=True,
                ),
                fact(
                    "S9_STATE_PARTNER_BOUNDARY",
                    "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
                    "mission.state_change.1",
                    "relationship_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="establish_bounded_cooperation",
                    counterparty_ids=("CHAR_PARTNER_001",),
                    from_state="implicit_trust",
                    to_state="cooperation_with_explicit_risk_boundary",
                    terminal=True,
                ),
                fact(
                    "S9_STATE_RIVAL_REPRICES",
                    "relationship:PROTAGONIST_001:CHAR_RIVAL_001",
                    "mission.state_change.2",
                    "relationship_transition",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="rival_reprices_competitor",
                    counterparty_ids=("CHAR_RIVAL_001",),
                    from_state="unknown_competitor",
                    to_state="specific_high_value_competitor",
                    terminal=True,
                ),
                fact(
                    "S9_STATE_INJURY_PENDING",
                    "state:STATE_INJURY_001",
                    "mission.state_change.3",
                    "state_transition",
                    "must_hold",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="remain_injured",
                    object_ids=("STATE_INJURY_001",),
                    from_state="acute",
                    to_state="not_fully_recovered",
                ),
                fact(
                    "S9_ENDING_RECORD_REEVALUATION",
                    "ending:S9:record_reevaluation",
                    "mission.ending.1",
                    "ending",
                    "terminal",
                    "chapter_end",
                    actor_id="PROTAGONIST_001",
                    action_id="record_triggers_escort_value_reevaluation",
                    object_ids=("RECORD_ESCORT_001", "ORG_COPPER_FEATHER_001"),
                    terminal=True,
                ),
            ],
        },
        {
            "source": "human_authority",
            "facts": [
                fact(
                    "S9_HUMAN_MIXED_DESIRE_ALLOWED",
                    "human:PROTAGONIST_001:motive",
                    "human.mixed_motive",
                    "state_transition",
                    "must_hold",
                    "pre_chapter",
                    actor_id="PROTAGONIST_001",
                    action_id="may_want_gain_and_person_survival_together",
                    object_ids=("ITEM_UMBRA_WEAPON_001",),
                    counterparty_ids=("CHAR_PARTNER_001",),
                    value={"not_purified_into_selfless_rescue": True},
                )
            ],
        },
    ]

    return [
        {
            "name": "jiuchui_ch14",
            "source_dir": fast_book / "chapter-0014",
            "registry": fast14_registry,
            "fragments": fast14_fragments,
            "target_fact_ids": ("J14_RESULT_MINING_SHARE",),
            "evidence": {"J14_RESULT_MINING_SHARE": (107, 109, 146)},
            "hints": (
                (107, "矿利怎么分？", "same target paragraph carries protagonist's concrete money demand"),
                (139, "回潮楔也不是我的", "outside target; remains safe through locality lock"),
            ),
            "old_delta_ops": (),
        },
        {
            "name": "jiuchui_ch16",
            "source_dir": fast_book / "chapter-0016",
            "registry": fast16_registry,
            "fragments": fast16_fragments,
            "target_fact_ids": ("J16_ACTION_CLONE_FIX_WEDGE",),
            "evidence": {"J16_ACTION_CLONE_FIX_WEDGE": (42, 45, 48, 50)},
            "hints": (
                (42, "直奔第二井外侧", "same action locality; preserve movement pressure"),
                (73, "三座新潮井还在，粮道也被保了下来", "outside target; locked result payoff"),
            ),
            "old_delta_ops": (
                ("replace", 71, 71, "楔子收回袖中。"),
                ("replace", 86, 86, "石台露了出来。"),
                ("replace", 96, 96, "顾停舟转身。"),
            ),
        },
        {
            "name": "shadow_ch4",
            "source_dir": second_book / "chapter-0004",
            "registry": second4_registry,
            "fragments": second4_fragments,
            "target_fact_ids": ("S4_RESULT_FIRST_PREPAYMENT_RECEIVED",),
            "evidence": {"S4_RESULT_FIRST_PREPAYMENT_RECEIVED": (53, 56)},
            "hints": (
                (56, "路上做得好，后面的照契券算", "same payment paragraph retains future opportunity"),
                (92, "多一个能守住位置的人，路会好走一点", "outside target relationship value"),
            ),
            "old_delta_ops": (),
        },
        {
            "name": "shadow_ch9",
            "source_dir": second_book / "chapter-0009",
            "registry": second9_registry,
            "fragments": second9_fragments,
            "target_fact_ids": ("S9_STATE_PARTNER_BOUNDARY",),
            "evidence": {"S9_STATE_PARTNER_BOUNDARY": (39, 41, 45, 50, 114, 115)},
            "hints": (
                (45, "别拿影身当一条不用算代价的命", "same repair locality carries the relationship boundary"),
                (27, "我也不想看着你死在里面", "outside target mixed motive; locked"),
            ),
            "old_delta_ops": (),
        },
    ]


def body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.rsplit("# 正式正文", 1)[-1].strip()


def patch_from_tuple(raw: tuple[str, int, int, str]) -> PatchOperation:
    kind, start, end, payload = raw
    return PatchOperation(
        kind=PatchKind(kind),
        start=start,
        end=end,
        payload=payload,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for spec in sample_specs():
        directory = OUT / spec["name"]
        directory.mkdir(parents=True, exist_ok=True)
        registry = EntityRegistry.from_dict(spec["registry"])
        builder = AtomicAuthorityContractBuilder(registry)
        for index, fragment in enumerate(spec["fragments"], 1):
            builder.add_artifact(
                frozen_artifact_from_fragment(
                    fragment,
                    artifact_suffix=f"{spec['name']}:{index}",
                )
            )
        contract = builder.build()
        primary = body(spec["source_dir"] / "primary_response.md")
        paragraphs = split_paragraphs(primary)

        bindings = tuple(
            bind_primary_realization(
                fact_id=fact_id,
                paragraph_ids=tuple(paragraph_ids),
                primary_body=primary,
                note="location only; not hard authority",
            )
            for fact_id, paragraph_ids in spec["evidence"].items()
        )
        hints = tuple(
            ProtectionHint(
                paragraph_id=paragraph_id,
                exact_fragment=fragment,
                provenance=PreservationProvenance.CURATOR_LOCATION_HINT,
                note=note,
            )
            for paragraph_id, fragment, note in spec["hints"]
        )
        preservation = build_primary_preservation_map(
            contract=contract,
            primary_body=primary,
            evidence_bindings=bindings,
            repair_target=RepairTarget(
                fact_ids=tuple(spec["target_fact_ids"]),
                locality_radius=0,
            ),
            protection_hints=hints,
        )

        first_editable = min(preservation.editable_paragraph_ids)
        source_paragraph = paragraphs[first_editable - 1]
        protected_inside = next(
            (
                hint.exact_fragment
                for hint in hints
                if hint.paragraph_id == first_editable
            ),
            "",
        )
        safe_payload = source_paragraph
        if protected_inside and protected_inside not in safe_payload:
            safe_payload += protected_inside
        allowed_check = validate_primary_preservation(
            contract=contract,
            preservation=preservation,
            primary_body=primary,
            operations=(
                PatchOperation(
                    kind=PatchKind.REPLACE,
                    start=first_editable,
                    end=first_editable,
                    payload=safe_payload,
                ),
            ),
        )
        locked_target = next(
            paragraph_id
            for paragraph_id in range(1, len(paragraphs) + 1)
            if paragraph_id not in preservation.editable_paragraph_ids
        )
        forbidden_check = validate_primary_preservation(
            contract=contract,
            preservation=preservation,
            primary_body=primary,
            operations=(
                PatchOperation(
                    kind=PatchKind.REPLACE,
                    start=locked_target,
                    end=locked_target,
                    payload="unauthorized edit outside blocker locality",
                ),
            ),
        )
        old_delta_operations = tuple(
            patch_from_tuple(item) for item in spec["old_delta_ops"]
        )
        old_delta_check = (
            validate_primary_preservation(
                contract=contract,
                preservation=preservation,
                primary_body=primary,
                operations=old_delta_operations,
            )
            if old_delta_operations
            else {
                "pass": True,
                "violations": [],
                "note": "historical Delta was KEEP_ALL / no operation",
            }
        )

        save_json(directory / "entity_registry.json", registry.to_dict())
        save_json(
            directory / "authority_ir_input.json",
            {
                "schema_version": "atomic-authority-ir-v1",
                "registry": spec["registry"],
                "fragments": spec["fragments"],
            },
        )
        save_json(directory / "atomic_authority_contract.json", contract.to_dict())
        save_json(
            directory / "primary_preservation_map.json",
            preservation.to_dict(),
        )
        save_json(
            directory / "locality_checks.json",
            {
                "allowed_inside_window": allowed_check,
                "forbidden_outside_window": forbidden_check,
                "historical_delta_against_map": old_delta_check,
            },
        )

        rows.append(
            {
                "sample": spec["name"],
                "chapter_id": contract.chapter_id,
                "protagonist_id": registry.protagonist_id,
                "protagonist_display_name": registry.require(
                    registry.protagonist_id
                ).display_name,
                "hard_contract_preflight_eligible": contract.preflight_eligible,
                "hard_fact_count": len(contract.facts),
                "hard_sources": contract.to_dict()["hard_sources"],
                "contract_hash": contract.contract_hash,
                "paragraph_count": len(paragraphs),
                "editable_paragraph_count": len(
                    preservation.editable_paragraph_ids
                ),
                "locked_paragraph_count": len(
                    preservation.locked_paragraph_ids
                ),
                "editable_ratio": round(
                    len(preservation.editable_paragraph_ids) / len(paragraphs),
                    4,
                ),
                "curator_or_primary_hard_source": any(
                    source in {"curator", "primary", "primary_draft"}
                    for source in contract.to_dict()["hard_sources"]
                ),
                "allowed_local_edit_pass": allowed_check["pass"],
                "forbidden_outside_edit_blocked": not forbidden_check["pass"],
                "historical_delta_locality_pass": old_delta_check["pass"],
                "historical_delta_violations": old_delta_check.get(
                    "violations", []
                ),
            }
        )

    summary = {
        "schema_version": "atomic-authority-ir-v1-static-experiment",
        "samples": len(rows),
        "contracts_preflight_eligible": sum(
            row["hard_contract_preflight_eligible"] for row in rows
        ),
        "source_pure_contracts": sum(
            not row["curator_or_primary_hard_source"] for row in rows
        ),
        "locality_allowed_pass": sum(
            row["allowed_local_edit_pass"] for row in rows
        ),
        "outside_locality_blocked": sum(
            row["forbidden_outside_edit_blocked"] for row in rows
        ),
        "average_editable_ratio": round(
            sum(row["editable_ratio"] for row in rows) / len(rows), 4
        ),
        "rows": rows,
    }
    save_json(OUT / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
