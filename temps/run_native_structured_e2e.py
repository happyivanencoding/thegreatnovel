from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Mapping, Sequence

WORKTREE = Path(r"C:\dev\tgn-story-mvp-native-e2e")
SOURCE_ROOT = Path(r"C:\dev\tgn-story-mvp")
OUT_ROOT = WORKTREE / "books" / "real-exp-native-structured-e2e-20260830-v1"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

sys.path.insert(0, str(WORKTREE / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    ActionSurfaceRegistry,
    AtomicAuthorityContractBuilder,
    AuthoritySource,
    DirectorStructuredDecision,
    EntityKind,
    EntityRecord,
    EntityRegistry,
    FrozenAuthorityArtifact,
    NarrativeFunctionRegistry,
    freeze_canon_artifact,
    freeze_human_artifact,
    freeze_power_artifact,
    freeze_reader_release_artifact,
    freeze_world_artifact,
)
from run_atomic_authority_ir_v1_static import sample_specs  # noqa: E402


MODEL = {
    "director": ("gpt-5.6-luna", "high"),
    "curator": ("gpt-5.6-luna", "high"),
    "primary": ("gpt-5.6-terra", "high"),
    "reviser": ("gpt-5.6-luna", "high"),
}

MISSION_LABELS = (
    "触发事件",
    "推动事件的人",
    "主角行动",
    "对手或世界反应",
    "直接结果",
    "状态变化",
    "叙事功能",
    "结尾推动力",
)


NATIVE_CONFIG: dict[str, dict[str, Any]] = {
    "jiuchui_ch14": {
        "actions": {
            "trial_entry_closes_under_claim": {
                "fields": ["trigger_event"], "kinds": ["event"],
                "description": "炉钟与入口关闭把公开追索压进开炉试",
                "template": "百炉会炉钟响起，开炉试入口即将封闭；{counterparties}围绕{objects}的公开追索同时压到场内。",
            },
            "offer_buyout": {
                "fields": ["event_driver"], "kinds": ["action"],
                "description": "阮青蜃提出买断回潮楔并以追索施压",
                "template": "{actor}提出买断{objects}，并以既有追索继续施压。",
            },
            "offer_independent_grain_contract": {
                "fields": ["event_driver"], "kinds": ["action"],
                "description": "少东家提出独立的粮路合作",
                "template": "{actor}提出围绕{objects}的独立有价合作。",
            },
            "lock_redirect_release_tide_once": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "只完成一次锁潮、改向、释放",
                "template": "{actor}让{objects}只完成一次真实的锁潮、改向和释放，用结果证明它能改变一整段潮势方向。",
            },
            "refuse_wedge_sale": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "拒绝出售回潮楔",
                "template": "{actor}拒绝把{objects}卖给{counterparties}。",
            },
            "accept_independent_cooperation": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "接受独立合作但不恢复旧主从",
                "template": "{actor}接受{counterparties}提出的{objects}合作，但保留独立定价和自主选择。",
            },
            "publicly_prove_direction_change_value": {
                "fields": ["world_reaction", "direct_result"], "kinds": ["public_proof"],
                "description": "同一公开表现被懂行者校准并触发重新定价",
                "template": "{actor}用{objects}完成公开表现，懂行者按成炉正常值校准后，现场对他的器物和能力重新定价。",
            },
            "retain_autonomous_use": {
                "fields": ["direct_result"], "kinds": ["ownership_transition"],
                "description": "回潮楔自主使用权得到公开保留",
                "template": "{actor}保住{objects}的自主使用权，不把它交回追索者。",
            },
            "confirm_entitlement": {
                "fields": ["direct_result"], "kinds": ["resource_transition"],
                "description": "取得个人矿利份额确认，但不是现金到账",
                "template": "{actor}取得{objects}的公开份额确认，但这不是现金到账。",
            },
            "transition_relationship": {
                "fields": ["state_change"], "kinds": ["relationship_transition"],
                "description": "与少东家从旧主从转为独立有价合作",
                "template": "{actor}与{counterparties}结束旧主从关系，转为有明确报酬和损失边界的独立合作。",
            },
            "require_residual_pressure_dissipation_before_reuse": {
                "fields": ["state_change"], "kinds": ["ability_boundary"],
                "description": "本章使用后必须散尽残压才能再用",
                "template": "{objects}完成本章一次改向后必须先散尽残压，不能连续硬压。",
            },
            "depart_with_grain_convoy": {
                "fields": ["ending_drive"], "kinds": ["ending"],
                "description": "随粮队向旧关出发",
                "template": "{actor}随粮队向旧关出发，粮路合作立即进入执行。",
            },
            "deliver_before_event": {
                "fields": ["ending_drive"], "kinds": ["deadline"],
                "description": "第一批货必须在下一次十二日地潮前送到",
                "template": "{actor}必须在下一次十二日地潮前把第一批货送到旧关。",
            },
        },
        "narratives": {
            "function.public_repricing": "完成古器、矿利和旧关系的第一次公共重估，让主角从被动保住已有之物转向主动选择财富与自由。",
            "function.direction_not_force": "兑现回潮楔‘改变方向’而不是单纯增大力量的核心价值，并把能力价值转成现实利益选择。",
        },
    },
    "jiuchui_ch16": {
        "actions": {
            "early_tide_hits_resources": {
                "fields": ["trigger_event"], "kinds": ["event"],
                "description": "提前地潮同时威胁粮道、新井、水路和外层",
                "template": "提前到来的地潮同时冲击三座新潮井、粮道和砺骨部迁徙水路，现场无法继续平均救援。",
            },
            "choose_resource_tradeoff": {
                "fields": ["event_driver"], "kinds": ["action"],
                "description": "主角明确选择保粮、井、水路并接受外层损失",
                "template": "{actor}明确选择保住三座新潮井、粮道和迁徙取水窗口，并接受旧关外层被舍弃的不可逆损失。",
            },
            "stabilize_routes": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "本体稳定粮道和迁徙水路",
                "template": "{actor}以本体力量稳定粮道和迁徙水路。",
            },
            "carry_and_fix_item_at_node": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "分身携带回潮楔并固定在第二潮压节点",
                "template": "{actor}携回潮楔进入第二个潮压节点，并把回潮楔固定在那里。",
            },
            "redirect_tide_and_sacrifice": {
                "fields": ["state_change"], "kinds": ["state_transition"],
                "description": "潮势改向并毁弃旧关外层",
                "template": "改向后的潮势冲入{objects}，被选择放弃的旧关外层因此彻底毁弃。",
            },
            "outer_pass_collapse_reaction": {
                "fields": ["world_reaction"], "kinds": ["direct_result"],
                "description": "改向后的地潮按选择冲毁旧关外层，现场结果公开可见",
                "template": "改向后的地潮冲毁{objects}，此前的资源取舍立刻变成公开、不可逆的结果。",
            },
            "preserve_resources": {
                "fields": ["direct_result"], "kinds": ["direct_result"],
                "description": "粮道、三井和迁徙水路得到保全",
                "template": "{actor}最终保住粮道、三座新潮井和砺骨部的迁徙取水窗口。",
            },
            "retain_possession": {
                "fields": ["direct_result"], "kinds": ["ownership_transition"],
                "description": "回潮楔仍归主角持有",
                "template": "回潮楔在这次公共使用后仍归{actor}持有，没有被转交。",
            },
            "require_residual_pressure_dissipation_before_reuse": {
                "fields": ["state_change"], "kinds": ["ability_boundary"],
                "description": "回潮楔再次使用前必须散尽残压",
                "template": "{objects}本次释放后残压仍需散尽，再次使用前不能连续硬压。",
            },
            "keep_early_tide_cause_unknown": {
                "fields": ["state_change"], "kinds": ["unknown_boundary"],
                "description": "地潮提前原因仍未知",
                "template": "{objects}仍保持未知，本章不得补出原因。",
            },
            "enter_observation_point": {
                "fields": ["ending_drive"], "kinds": ["ending"],
                "description": "进入暴露的观测点继续判断下一轮潮势",
                "template": "{actor}必须进入暴露的旧关内侧观测点，确认下一轮潮势指向并争取撤离时间。",
            },
        },
        "narratives": {
            "function.public_resource_tradeoff": "把复合能力从个人救急推进到公共资源与迁徙路线选择，用明确牺牲证明主角能改变更大的现实结果。",
            "function.composite_power_payoff": "兑现本体与分身两个真实位置的复合作用，同时留下不可逆外层损失和下一行动入口。",
        },
    },
    "shadow_ch4": {
        "actions": {
            "du_heng_enters_with_unfamiliar_footwork": {
                "fields": ["trigger_event"], "kinds": ["event"],
                "description": "杜衡用陌生步点在连续比试中压迫主角",
                "template": "{actor}在连续比试中用陌生步点逼近{counterparties}，试图逼出后撤惯性。",
            },
            "press_with_unfamiliar_footwork": {
                "fields": ["event_driver"], "kinds": ["action"],
                "description": "杜衡持续改变步点并逼近",
                "template": "{actor}持续改变步点和变向，压缩{counterparties}原本熟悉的选择。",
            },
            "defeat_under_fatigue": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "疲劳中观察落脚和变向，抓一次空隙反击取胜",
                "template": "{actor}在疲劳中不抢先出刃，观察{objects}的落脚和变向，抓住一次真实空隙以影刃反击并击败对手。",
            },
            "reveal_ability": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "回客舍后让陆绾确认分影真实存在",
                "template": "{actor}主动向{counterparties}展示{objects}的真实存在。",
            },
            "confirm_public_rank": {
                "fields": ["world_reaction"], "kinds": ["direct_result"],
                "description": "试官确认仍是一阶但连续实战稳定",
                "template": "{actor}确认{counterparties}仍处于{objects}，但连续公开实战的价值已经上调。",
            },
            "win_public_rank": {
                "fields": ["direct_result"], "kinds": ["direct_result"],
                "description": "赢得公开名次",
                "template": "{actor}取得{objects}认可的公开名次。",
            },
            "receive_contract": {
                "fields": ["direct_result"], "kinds": ["ownership_transition"],
                "description": "拿到铜羽随队契约",
                "template": "{actor}正式拿到{objects}，离乡与跨城护送的机会落到手里。",
            },
            "receive_partial_prepayment": {
                "fields": ["direct_result"], "kinds": ["resource_transition"],
                "description": "收到第一笔预付钱而非全部后续报酬",
                "template": "{actor}收到{objects}；这里只是第一笔预付，不等于后续报酬全部结清。",
            },
            "partner_decides同行": {
                "fields": ["state_change"], "kinds": ["relationship_transition"],
                "description": "陆绾确认分影后决定与药队同行",
                "template": "{counterparties}确认分影真实存在后，决定与{actor}及药队同行。",
            },
            "depart_next_day_via_changed_route": {
                "fields": ["ending_drive"], "kinds": ["deadline"],
                "description": "次日商队药队出发，安全路线关闭，只能绕折日峡",
                "template": "{actor}次日必须随药队出发；原安全路线已经关闭，只能绕行折日峡。",
            },
        },
        "narratives": {
            "function.stage_payoff_departure": "把连续公开战斗兑现成名次、契约、第一笔钱和离乡入口，并把下一阶段推入荒野。",
            "function.power_to_life_change": "让分影的训练收益转成公开战果、关系变化和现实人生选择，而不是只停在能力展示。",
        },
    },
    "shadow_ch9": {
        "actions": {
            "clone_injury_returns_and_disables": {
                "fields": ["trigger_event"], "kinds": ["event"],
                "description": "影身归体后撞击与疲劳集中结算，主角短暂失去行动力",
                "template": "分影归体带回的撞击、伤势和疲劳集中落到{actor}身上，使他短暂失去行动力。",
            },
            "treat_and_question_motive": {
                "fields": ["event_driver"], "kinds": ["action"],
                "description": "陆绾处理伤势并追问取兵救人的动机",
                "template": "{actor}处理{objects}并直接追问{counterparties}此前的双线选择。",
            },
            "rival_checks_double_line_choice": {
                "fields": ["event_driver"], "kinds": ["action"],
                "description": "顾斜阳根据撤离见证确认两条行动线",
                "template": "{actor}根据撤离见证核对{counterparties}在两条行动线上的临场选择。",
            },
            "accept_treatment": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "接受陆绾处理伤口",
                "template": "{actor}接受{counterparties}处理{objects}。",
            },
            "admit_mixed_motive": {
                "fields": ["protagonist_action"], "kinds": ["action"],
                "description": "承认既想要乌沉短兵也不想陆绾死",
                "template": "{actor}向{counterparties}承认：自己既想拿到{objects}，也不愿她死在石城。",
            },
            "admit_wants_weapon_and_partner_survival": {
                "fields": ["direct_result"], "kinds": ["direct_result"],
                "description": "混合欲望成为明确事实",
                "template": "{actor}明确承认自己既想拿到{objects}，也不想让{counterparties}死在石城里。",
            },
            "rival_confirms_double_line_choice": {
                "fields": ["world_reaction"], "kinds": ["direct_result"],
                "description": "顾斜阳确认双线行动不是预设动作",
                "template": "{actor}确认{counterparties}在两条行动线上都作过真实临场选择。",
            },
            "establish_bounded_cooperation": {
                "fields": ["state_change"], "kinds": ["relationship_transition"],
                "description": "与陆绾建立带明确风险边界的合作",
                "template": "{counterparties}明确划出分影使用的风险边界，与{actor}的信任转为有边界的合作。",
            },
            "rival_reprices_competitor": {
                "fields": ["state_change"], "kinds": ["relationship_transition"],
                "description": "顾斜阳把主角从陌生竞争者重新估价为具体高价值竞争者",
                "template": "{counterparties}不再把{actor}当作陌生的普通竞争者，而开始按一个具体、高价值的竞争者重新估价。",
            },
            "remain_injured": {
                "fields": ["state_change"], "kinds": ["state_transition"],
                "description": "伤势未完全恢复",
                "template": "{actor}的{objects}仍未完全恢复，短时间内继续限制行动。",
            },
            "record_triggers_escort_value_reevaluation": {
                "fields": ["ending_drive"], "kinds": ["ending"],
                "description": "撤离记录被带回，触发更高层级护卫价值重新评估",
                "template": "{actor}把{objects}带回，触发对{counterparties}护卫价值的重新评估，但更高入口尚未到账。",
            },
        },
        "narratives": {
            "function.relationship_cost_aftershock": "把分影的身体代价转成关系边界和私人欲望暴露，让战斗余波真正改变人物。",
            "function.rival_repricing": "让双线行动的代价与欲望同时被关系人物和竞争者看见，推动下一层护卫价值重新评估。",
        },
    },
}


MANUAL_SIGNATURES: dict[str, dict[str, dict[str, Any]]] = {
    "jiuchui_ch14": {
        "trial_entry_closes_under_claim": {"actor_ids": ["ORG_HUNDRED_FURNACE_001"], "required_object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"], "exact_object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"], "required_counterparty_ids": ["CHAR_RIVAL_001"], "exact_counterparty_ids": ["CHAR_RIVAL_001"]},
        "offer_buyout": {"actor_ids": ["CHAR_RIVAL_001"], "required_object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
        "offer_independent_grain_contract": {"actor_ids": ["CHAR_PARTNER_001"], "required_object_ids": ["ROUTE_GRAIN_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
        "refuse_wedge_sale": {"actor_ids": ["PROTAGONIST_001"], "required_object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"], "required_counterparty_ids": ["CHAR_RIVAL_001"]},
        "accept_independent_cooperation": {"actor_ids": ["PROTAGONIST_001"], "required_object_ids": ["ROUTE_GRAIN_001"], "required_counterparty_ids": ["CHAR_PARTNER_001"]},
    },
    "jiuchui_ch16": {
        "early_tide_hits_resources": {"actor_ids": ["", "MYSTERY_EARLY_TIDE_001"], "required_object_ids": ["RESOURCE_WELLS_001", "ROUTE_GRAIN_001", "ROUTE_WATER_001"]},
        "choose_resource_tradeoff": {"actor_ids": ["PROTAGONIST_001"], "required_object_ids": ["RESOURCE_WELLS_001", "ROUTE_GRAIN_001", "ROUTE_WATER_001"]},
        "outer_pass_collapse_reaction": {"actor_ids": ["MYSTERY_EARLY_TIDE_001"], "required_object_ids": ["LOCATION_OUTER_PASS_001"], "exact_object_ids": ["LOCATION_OUTER_PASS_001"]},
        "keep_early_tide_cause_unknown": {"actor_ids": [""], "required_object_ids": ["MYSTERY_EARLY_TIDE_001"], "to_state": "unknown"},
    },
    "shadow_ch4": {
        "du_heng_enters_with_unfamiliar_footwork": {"actor_ids": ["CHAR_OPPONENT_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
        "press_with_unfamiliar_footwork": {"actor_ids": ["CHAR_OPPONENT_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
        "confirm_public_rank": {"actor_ids": ["ORG_COPPER_FEATHER_001"], "required_object_ids": ["TIER_FIRST_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
    },
    "shadow_ch9": {
        "clone_injury_returns_and_disables": {"actor_ids": ["PROTAGONIST_001"], "required_object_ids": ["ABILITY_SHADOW_CLONE_001", "STATE_INJURY_001"]},
        "treat_and_question_motive": {"actor_ids": ["CHAR_PARTNER_001"], "required_object_ids": ["STATE_INJURY_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
        "rival_checks_double_line_choice": {"actor_ids": ["CHAR_RIVAL_001"], "required_object_ids": ["RECORD_ESCORT_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
        "admit_mixed_motive": {"actor_ids": ["PROTAGONIST_001"], "required_object_ids": ["ITEM_UMBRA_WEAPON_001"], "required_counterparty_ids": ["CHAR_PARTNER_001"]},
        "rival_confirms_double_line_choice": {"actor_ids": ["CHAR_RIVAL_001"], "required_object_ids": ["RECORD_ESCORT_001"], "required_counterparty_ids": ["PROTAGONIST_001"]},
    },
}


def source_directory(name: str) -> Path:
    mapping = {
        "jiuchui_ch14": SOURCE_ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs" / "chapter-0014",
        "jiuchui_ch16": SOURCE_ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs" / "chapter-0016",
        "shadow_ch4": SOURCE_ROOT / "books" / "real-exp-current-pipeline-authority-reviser-0010-20260828-v1" / "runs" / "chapter-0004",
        "shadow_ch9": SOURCE_ROOT / "books" / "real-exp-current-pipeline-authority-reviser-0010-20260828-v1" / "runs" / "chapter-0009",
    }
    return mapping[name]


def clean_model_text(text: str) -> str:
    text = re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()
    return text


def parse_json_object(text: str) -> dict[str, Any]:
    clean = clean_model_text(text)
    if clean.startswith("```"):
        match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", clean, re.S)
        if match:
            clean = match.group(1)
    if not clean.startswith("{"):
        start = clean.find("{")
        end = clean.rfind("}")
        if start >= 0 and end > start:
            clean = clean[start : end + 1]
    payload = json.loads(clean)
    if not isinstance(payload, dict):
        raise ValueError("structured Director response is not a JSON object")
    return payload


def call_acp(prompt_path: Path, output_path: Path, *, model: str, effort: str) -> dict[str, Any]:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                [
                    "node",
                    str(RUNNER),
                    str(prompt_path),
                    str(output_path),
                    model,
                    effort,
                    str(WORKTREE),
                ],
                cwd=WORKTREE,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout after 1200s: {prompt_path}"
            time.sleep(2 + attempt * 2)
            continue
        if process.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
            except Exception as error:  # noqa: BLE001
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def parse_mission_fields(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for index, label in enumerate(MISSION_LABELS):
        next_labels = "|".join(re.escape(item) for item in MISSION_LABELS[index + 1 :])
        if next_labels:
            pattern = rf"(?ms)^{re.escape(label)}：\s*(.*?)(?=^(?:{next_labels})：|^## |\Z)"
        else:
            pattern = rf"(?ms)^{re.escape(label)}：\s*(.*?)(?=^## |\Z)"
        match = re.search(pattern, text)
        if match:
            result[label] = match.group(1).strip()
    return result


def replace_mission_values(prompt: str, old_mission: str, new_mission: str) -> str:
    old = parse_mission_fields(old_mission)
    new = parse_mission_fields(new_mission)
    for label in MISSION_LABELS:
        old_value = old.get(label)
        new_value = new.get(label)
        if old_value and new_value:
            prompt = prompt.replace(old_value, new_value)
    return prompt


def replace_h2_block(text: str, heading_prefix: str, replacement: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(headings):
        if match.group(1).strip().startswith(heading_prefix):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            return text[: match.end()] + "\n\n" + replacement.strip() + "\n\n" + text[end:]
    raise ValueError(f"H2 heading not found: {heading_prefix}")


def replace_primary_curated_context(prompt: str, curator_response: str) -> str:
    marker = "## Curated Chapter Context"
    start = prompt.find(marker)
    if start < 0:
        raise ValueError("Primary prompt missing Curated Chapter Context")
    return prompt[:start] + marker + "\n\n" + curator_response.strip() + "\n"


def body(text: str) -> str:
    clean = clean_model_text(text)
    if "# 正式正文" in clean:
        clean = clean.rsplit("# 正式正文", 1)[-1].strip()
    return clean


def control_timings(directory: Path) -> dict[str, float]:
    result = {}
    for node, filename in (
        ("director", "director_acp.json"),
        ("curator", "curator_acp.json"),
        ("primary", "primary_acp.json"),
        ("reviser", "authority_reviser_acp.json"),
    ):
        data = json.loads((directory / filename).read_text(encoding="utf-8"))
        result[node] = float(data.get("wall_seconds") or 0)
    result["total"] = sum(result.values())
    return result


def augment_registry(name: str, registry: EntityRegistry) -> EntityRegistry:
    entities = dict(registry.entities)
    if name == "jiuchui_ch14":
        entities["ROUTE_WATER_001"] = EntityRecord(
            entity_id="ROUTE_WATER_001",
            kind=EntityKind.ROUTE,
            display_name="砺骨部水路",
            aliases=("水路",),
            authority_refs=("world.route.water_right",),
        )
    return EntityRegistry(
        chapter_id=registry.chapter_id,
        protagonist_id=registry.protagonist_id,
        entities=entities,
    )


def frozen_nonmission_artifacts(spec: Mapping[str, Any]) -> tuple[FrozenAuthorityArtifact, ...]:
    factories = {
        "canon": freeze_canon_artifact,
        "world_authority": freeze_world_artifact,
        "power_authority": freeze_power_artifact,
        "human_authority": freeze_human_artifact,
        "reader_release": freeze_reader_release_artifact,
    }
    result: list[FrozenAuthorityArtifact] = []
    counts: dict[str, int] = {}
    for fragment in spec["fragments"]:
        source = str(fragment["source"])
        if source == "frozen_mission":
            continue
        counts[source] = counts.get(source, 0) + 1
        result.append(
            factories[source](
                f"{ {'canon':'canon','world_authority':'world','power_authority':'power','human_authority':'human','reader_release':'reader_release'}[source] }:native-e2e:{spec['name']}:{counts[source]}",
                fragment.get("facts", []),
            )
        )
    return tuple(result)


def prestate_table(artifacts: Sequence[FrozenAuthorityArtifact]) -> list[dict[str, str]]:
    rows = []
    for artifact in artifacts:
        for fact in artifact.facts:
            if fact.phase.value != "pre_chapter":
                continue
            state = fact.to_state or (str(fact.value) if fact.value is not None else "")
            if state:
                rows.append({"slot_id": fact.slot_id, "state": state, "source": artifact.source.value})
    return rows


def expected_mission_facts(spec: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        fact
        for fragment in spec["fragments"]
        if fragment["source"] == "frozen_mission"
        for fact in fragment["facts"]
    ]


def action_constraint(
    name: str,
    spec: Mapping[str, Any],
    action_id: str,
) -> dict[str, Any]:
    constraint: dict[str, Any] = {}
    expected = next(
        (
            item
            for item in expected_mission_facts(spec)
            if item.get("action_id") == action_id
        ),
        None,
    )
    if expected:
        constraint.update(
            {
                "actor_ids": [str(expected.get("actor_id", ""))],
                "required_object_ids": list(expected.get("object_ids", [])),
                "required_counterparty_ids": list(
                    expected.get("counterparty_ids", [])
                ),
                "exact_object_ids": list(expected.get("object_ids", [])),
                "exact_counterparty_ids": list(
                    expected.get("counterparty_ids", [])
                ),
                "from_state": str(expected.get("from_state", "")),
                "to_state": str(expected.get("to_state", "")),
            }
        )
    manual = MANUAL_SIGNATURES.get(name, {}).get(action_id, {})
    constraint.update(manual)
    return constraint


def normalize_native_payload(
    name: str,
    spec: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Canonicalize fields already owned by trusted Runtime action signatures.

    The model chooses the action IDs and chapter structure. For a catalog action
    whose exact actor/object/counterparty/pre/post state is already Frozen, the
    duplicated fields are Runtime-owned defaults. Normalization is recorded so
    it cannot hide how much correction the schema required.
    """

    normalized = json.loads(json.dumps(payload, ensure_ascii=False))
    changes: list[dict[str, Any]] = []
    for index, clause in enumerate(normalized.get("clauses", []), 1):
        action_id = str(clause.get("action_id", ""))
        constraint = action_constraint(name, spec, action_id)
        if not constraint:
            continue
        actor_ids = list(constraint.get("actor_ids", []))
        if len(actor_ids) == 1:
            expected = actor_ids[0]
            current = str(clause.get("actor_id", ""))
            if current != expected:
                changes.append({"clause": index, "field": "actor_id", "from": current, "to": expected})
            clause["actor_id"] = expected
        for source_key, target_key in (
            ("exact_object_ids", "object_ids"),
            ("exact_counterparty_ids", "counterparty_ids"),
        ):
            if source_key in constraint:
                expected_list = list(constraint[source_key])
                current_list = list(clause.get(target_key, []))
                if current_list != expected_list:
                    changes.append({"clause": index, "field": target_key, "from": current_list, "to": expected_list})
                clause[target_key] = expected_list
        for state_key in ("from_state", "to_state"):
            expected_state = str(constraint.get(state_key, ""))
            if expected_state:
                current_state = str(clause.get(state_key, ""))
                if current_state != expected_state:
                    changes.append({"clause": index, "field": state_key, "from": current_state, "to": expected_state})
                clause[state_key] = expected_state
        clause.pop("mode", None)
        clause.pop("terminal", None)
    return normalized, changes


def validate_action_catalog(
    name: str,
    spec: Mapping[str, Any],
    decision: DirectorStructuredDecision,
) -> list[str]:
    errors: list[str] = []
    config = NATIVE_CONFIG[name]["actions"]
    for index, clause in enumerate(decision.clauses, 1):
        action = config.get(clause.action_id)
        if action is None:
            errors.append(
                f"clause {index} action_id={clause.action_id!r} is not in Action Catalog"
            )
            continue
        if clause.field.value not in action["fields"]:
            errors.append(
                f"clause {index} action={clause.action_id} field={clause.field.value} "
                f"not in {action['fields']}"
            )
        if clause.kind.value not in action["kinds"]:
            errors.append(
                f"clause {index} action={clause.action_id} kind={clause.kind.value} "
                f"not in {action['kinds']}"
            )
        constraint = action_constraint(name, spec, clause.action_id)
        actor_ids = constraint.get("actor_ids")
        if actor_ids is not None and clause.actor_id not in actor_ids:
            errors.append(
                f"clause {index} action={clause.action_id} actor={clause.actor_id!r} "
                f"expected one of {actor_ids}"
            )
        required_objects = set(constraint.get("required_object_ids", []))
        if not required_objects.issubset(set(clause.object_ids)):
            errors.append(
                f"clause {index} action={clause.action_id} missing objects="
                f"{sorted(required_objects - set(clause.object_ids))}"
            )
        required_counterparties = set(
            constraint.get("required_counterparty_ids", [])
        )
        if not required_counterparties.issubset(set(clause.counterparty_ids)):
            errors.append(
                f"clause {index} action={clause.action_id} missing counterparties="
                f"{sorted(required_counterparties - set(clause.counterparty_ids))}"
            )
        for state_key in ("from_state", "to_state"):
            expected_state = str(constraint.get(state_key, ""))
            if expected_state and getattr(clause, state_key) != expected_state:
                errors.append(
                    f"clause {index} action={clause.action_id} {state_key}="
                    f"{getattr(clause, state_key)!r} expected={expected_state!r}"
                )
    return errors


def structural_match(expected: Mapping[str, Any], generated: Mapping[str, Any]) -> bool:
    if expected.get("kind") != generated.get("kind"):
        return False
    if expected.get("actor_id") and expected.get("actor_id") != generated.get("actor_id"):
        return False
    if expected.get("action_id") and expected.get("action_id") != generated.get("action_id"):
        return False
    if not set(expected.get("object_ids", [])).issubset(set(generated.get("object_ids", []))):
        return False
    if not set(expected.get("counterparty_ids", [])).issubset(set(generated.get("counterparty_ids", []))):
        return False
    if expected.get("from_state") and expected.get("from_state") != generated.get("from_state"):
        return False
    if expected.get("to_state") and expected.get("to_state") != generated.get("to_state"):
        return False
    if expected.get("phase") and expected.get("phase") != generated.get("phase"):
        return False
    if expected.get("mode") and expected.get("mode") != generated.get("mode"):
        return False
    if bool(expected.get("terminal", False)) != bool(generated.get("terminal", False)):
        return False
    return True


def structural_coverage(spec: Mapping[str, Any], decision: DirectorStructuredDecision, registry: EntityRegistry) -> dict[str, Any]:
    expected = expected_mission_facts(spec)
    generated = [fact.to_dict() for fact in decision.mission_facts(registry)]
    matches = []
    for item in expected:
        matched = next((fact for fact in generated if structural_match(item, fact)), None)
        matches.append({
            "expected_fact_id": item["fact_id"],
            "expected_action_id": item.get("action_id", ""),
            "matched": bool(matched),
            "matched_fact_id": matched.get("fact_id", "") if matched else "",
        })
    count = sum(item["matched"] for item in matches)
    return {
        "expected": len(expected),
        "matched": count,
        "coverage": round(count / max(1, len(expected)), 4),
        "rows": matches,
    }


def build_native_prompt(name: str, original_prompt: str, registry: EntityRegistry, artifacts: Sequence[FrozenAuthorityArtifact]) -> str:
    config = NATIVE_CONFIG[name]
    action_rows = []
    for action_id, payload in config["actions"].items():
        action_rows.append({
            "action_id": action_id,
            "allowed_fields": payload["fields"],
            "allowed_kinds": payload["kinds"],
            "meaning": payload["description"],
            "required_signature": action_constraint(name, next(item for item in sample_specs() if item["name"] == name), action_id),
        })
    schema = json.loads(
        (WORKTREE / "books" / "real-exp-atomic-authority-ir-20260829-v1" / "schemas" / "director-structured-decision-v1.schema.json").read_text(encoding="utf-8")
    )
    override = f"""

# EXPERIMENTAL OUTPUT OVERRIDE｜Native DirectorStructuredDecision v1

The creative task and all Frozen Authority above stay unchanged. For this experiment, do NOT output the human eight-field mission directly and do NOT output a second Sidecar. Make the chapter decision once as the canonical typed object below. Runtime will render the human mission deterministically from the same object.

Return exactly one JSON object and nothing else. No Markdown fence, no explanation, no `human_clause`, no `narrative_function`, no `specialty_suggestions`, no unknown keys.

Hard rules:
- `chapter_id` MUST equal `{registry.chapter_id}`.
- `protagonist_id` MUST equal `{registry.protagonist_id}`.
- Every entity ID must come from ENTITY REGISTRY.
- Every `action_id` must come from ACTION CATALOG and obey that row's allowed field/kind.
- If an ACTION CATALOG row has `required_signature`, use that actor/object/counterparty/from/to state exactly; Runtime owns the action signature, so do not improvise a different role assignment for the same action ID.
- `protagonist_action` may use `{registry.protagonist_id}` or a registered manifestation whose parent is that protagonist.
- For terminal resource / ownership / relationship / state / power transitions, use the exact known `from_state` from PRE-CHAPTER STATE when one exists. Do not guess a pre-state.
- Do not turn a deadline into completed current action.
- Do not turn entitlement into cash received.
- Do not turn battle-scale performance into a stable power transition.
- Omit `mode` and `terminal`; Runtime owns them from field/kind.
- Use `surface_note` only as an empty string; it is non-authoritative.
- `value` should normally be null. `metadata` should normally be {{}}.
- One important fact should appear once; do not duplicate semantic facts under several fields.
- The original Director job still applies: choose the most commercially valuable chapter realization allowed by the Plan/Canon, without inventing later rewards or mechanisms.

FIELD COUNT LIMITS:
- trigger_event: exactly 1
- event_driver: 1–3
- protagonist_action: 1–3
- world_reaction: 1–4
- direct_result: 1–5
- state_change: 1–5
- ending_drive: 1–2

ENTITY REGISTRY:
{json.dumps(registry.to_dict(), ensure_ascii=False, indent=2)}

PRE-CHAPTER STATE:
{json.dumps(prestate_table(artifacts), ensure_ascii=False, indent=2)}

ACTION CATALOG:
{json.dumps(action_rows, ensure_ascii=False, indent=2)}

NARRATIVE FUNCTION IDS:
{json.dumps(config['narratives'], ensure_ascii=False, indent=2)}

JSON SCHEMA:
{json.dumps(schema, ensure_ascii=False, indent=2)}
"""
    return original_prompt.rstrip() + override


def validate_rendered_projection_scope(
    name: str,
    mission: str,
    current_registry: EntityRegistry,
) -> list[str]:
    """Reject deterministic projection leakage from another book/sample.

    This does not judge prose quality. It only catches a surface template that
    literally names an entity/ability registered in another sample but absent
    from the current Registry, plus obvious renderer punctuation/internal-ID
    leakage.
    """

    current_surfaces = {
        entity.display_name
        for entity in current_registry.entities.values()
        if len(entity.display_name) >= 2
    }
    foreign_surfaces: set[str] = set()
    for spec in sample_specs():
        if spec["name"] == name:
            continue
        registry = EntityRegistry.from_dict(spec["registry"])
        for entity in registry.entities.values():
            surface = entity.display_name
            overlaps_current = any(
                surface in current or current in surface
                for current in current_surfaces
            )
            if len(surface) >= 2 and not overlaps_current:
                foreign_surfaces.add(surface)
    violations = [
        f"foreign registered surface leaked into mission: {surface}"
        for surface in sorted(foreign_surfaces)
        if surface in mission
    ]
    if "。；" in mission:
        violations.append("renderer emitted invalid punctuation sequence 。；")
    if re.search(r"\b(?:[a-z]+_[a-z0-9_]+|[A-Z][A-Z0-9_]{2,})\b", mission):
        violations.append("renderer leaked internal identifier into human Mission")
    return violations


def action_surfaces(name: str) -> ActionSurfaceRegistry:
    return ActionSurfaceRegistry.from_dict(
        {action_id: payload["template"] for action_id, payload in NATIVE_CONFIG[name]["actions"].items()}
    )


def narrative_surfaces(name: str) -> NarrativeFunctionRegistry:
    return NarrativeFunctionRegistry.from_dict(NATIVE_CONFIG[name]["narratives"])


def run_normal_director_fallback(directory: Path, output_dir: Path) -> tuple[str, float, dict[str, Any]]:
    prompt_path = output_dir / "fallback_director_prompt.md"
    acp_path = output_dir / "fallback_director_acp.json"
    prompt_path.write_text((directory / "director_prompt.md").read_text(encoding="utf-8"), encoding="utf-8")
    model, effort = MODEL["director"]
    data = call_acp(prompt_path, acp_path, model=model, effort=effort)
    text = clean_model_text(str(data.get("text", "")))
    (output_dir / "fallback_director_response.md").write_text(text + "\n", encoding="utf-8")
    return text, float(data.get("wall_seconds") or 0), data


def run_one(name: str, run_label: str, *, director_only: bool = False) -> dict[str, Any]:
    spec = next(item for item in sample_specs() if item["name"] == name)
    directory = source_directory(name)
    output_dir = OUT_ROOT / run_label / name
    output_dir.mkdir(parents=True, exist_ok=True)

    base_registry = EntityRegistry.from_dict(spec["registry"])
    registry = augment_registry(name, base_registry)
    artifacts = frozen_nonmission_artifacts(spec)
    original_director_prompt = (directory / "director_prompt.md").read_text(encoding="utf-8")
    native_prompt = build_native_prompt(name, original_director_prompt, registry, artifacts)
    native_prompt_path = output_dir / "native_director_prompt.md"
    native_acp_path = output_dir / "native_director_acp.json"
    native_prompt_path.write_text(native_prompt, encoding="utf-8")

    model, effort = MODEL["director"]
    native_data = call_acp(native_prompt_path, native_acp_path, model=model, effort=effort)
    native_text = clean_model_text(str(native_data.get("text", "")))
    (output_dir / "native_director_response.txt").write_text(native_text + "\n", encoding="utf-8")

    native_error = ""
    decision = None
    contract = None
    rendered_mission = ""
    coverage: dict[str, Any] = {"expected": 0, "matched": 0, "coverage": 0.0, "rows": []}
    normalization_changes: list[dict[str, Any]] = []
    try:
        raw_payload = parse_json_object(native_text)
        payload, normalization_changes = normalize_native_payload(name, spec, raw_payload)
        (output_dir / "native_director_raw_decision.json").write_text(
            json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output_dir / "native_runtime_normalizations.json").write_text(
            json.dumps(normalization_changes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output_dir / "native_director_decision.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        decision = DirectorStructuredDecision.from_dict(payload)
        signature_errors = validate_action_catalog(name, spec, decision)
        if signature_errors:
            raise ValueError("Action Catalog signature violations: " + " | ".join(signature_errors))
        contract = decision.build_contract(registry=registry, authority_artifacts=artifacts)
        rendered_mission = decision.render_human_mission(
            registry=registry,
            surfaces=action_surfaces(name),
            narrative_functions=narrative_surfaces(name),
        )
        projection_violations = validate_rendered_projection_scope(
            name, rendered_mission, registry
        )
        if projection_violations:
            raise ValueError(
                "Runtime dual-projection violations: "
                + " | ".join(projection_violations)
            )
        coverage = structural_coverage(spec, decision, registry)
        (output_dir / "native_atomic_contract.json").write_text(
            json.dumps(contract.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output_dir / "native_rendered_mission.md").write_text(rendered_mission + "\n", encoding="utf-8")
    except Exception as error:  # noqa: BLE001
        native_error = f"{type(error).__name__}: {error}"

    native_seconds = float(native_data.get("wall_seconds") or 0)
    fallback_used = bool(native_error or contract is None or not contract.preflight_eligible)
    fallback_seconds = 0.0
    if fallback_used:
        mission, fallback_seconds, _ = run_normal_director_fallback(directory, output_dir)
        director_source = "fallback_control_director"
    else:
        mission = rendered_mission
        director_source = "native_structured"

    old_mission = (directory / "director_response.md").read_text(encoding="utf-8").strip()
    control = control_timings(directory)
    row: dict[str, Any] = {
        "sample": name,
        "run": run_label,
        "director_source": director_source,
        "native_parse_or_build_error": native_error,
        "native_contract_preflight_eligible": bool(contract and contract.preflight_eligible),
        "native_contract_conflicts": list(contract.conflicts) if contract else [],
        "native_contract_unsupported": list(contract.unsupported) if contract else [],
        "native_structural_coverage": coverage,
        "runtime_normalization_count": len(normalization_changes),
        "runtime_normalizations": normalization_changes,
        "native_director_seconds": native_seconds,
        "fallback_director_seconds": fallback_seconds,
        "effective_director_seconds": round(native_seconds + fallback_seconds, 3),
        "control_director_seconds": control["director"],
        "control_curator_seconds": control["curator"],
        "control_primary_seconds": control["primary"],
        "control_reviser_seconds": control["reviser"],
        "control_total_seconds": control["total"],
        "native_mission_chars": len(mission),
        "control_mission_chars": len(old_mission),
    }
    (output_dir / "effective_director_mission.md").write_text(mission.strip() + "\n", encoding="utf-8")

    if director_only:
        return row

    curator_prompt = replace_mission_values(
        (directory / "curator_prompt.md").read_text(encoding="utf-8"),
        old_mission,
        mission,
    )
    curator_prompt_path = output_dir / "curator_prompt.md"
    curator_acp_path = output_dir / "curator_acp.json"
    curator_prompt_path.write_text(curator_prompt, encoding="utf-8")
    curator_model, curator_effort = MODEL["curator"]
    curator_data = call_acp(curator_prompt_path, curator_acp_path, model=curator_model, effort=curator_effort)
    curator_text = clean_model_text(str(curator_data.get("text", "")))
    (output_dir / "curator_response.md").write_text(curator_text + "\n", encoding="utf-8")
    curator_seconds = float(curator_data.get("wall_seconds") or 0)

    primary_prompt = replace_mission_values(
        (directory / "primary_prompt.md").read_text(encoding="utf-8"),
        old_mission,
        mission,
    )
    primary_prompt = replace_primary_curated_context(primary_prompt, curator_text)
    primary_prompt_path = output_dir / "primary_prompt.md"
    primary_acp_path = output_dir / "primary_acp.json"
    primary_prompt_path.write_text(primary_prompt, encoding="utf-8")
    primary_model, primary_effort = MODEL["primary"]
    primary_data = call_acp(primary_prompt_path, primary_acp_path, model=primary_model, effort=primary_effort)
    primary_text = clean_model_text(str(primary_data.get("text", "")))
    (output_dir / "primary_response.md").write_text(primary_text + "\n", encoding="utf-8")
    primary_seconds = float(primary_data.get("wall_seconds") or 0)

    reviser_prompt = (directory / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    reviser_prompt = replace_h2_block(reviser_prompt, "FROZEN CHAPTER MISSION", mission)
    reviser_prompt = replace_h2_block(reviser_prompt, "CURATOR", curator_text)
    reviser_prompt = replace_h2_block(reviser_prompt, "PRIMARY DRAFT", primary_text)
    reviser_prompt_path = output_dir / "authority_reviser_prompt.md"
    reviser_acp_path = output_dir / "authority_reviser_acp.json"
    reviser_prompt_path.write_text(reviser_prompt, encoding="utf-8")
    reviser_model, reviser_effort = MODEL["reviser"]
    reviser_data = call_acp(reviser_prompt_path, reviser_acp_path, model=reviser_model, effort=reviser_effort)
    reviser_text = clean_model_text(str(reviser_data.get("text", "")))
    (output_dir / "authority_reviser_response.md").write_text(reviser_text + "\n", encoding="utf-8")
    reviser_seconds = float(reviser_data.get("wall_seconds") or 0)

    primary_body = body(primary_text)
    final_body = body(reviser_text)
    control_final_body = body((directory / "authority_reviser_response.md").read_text(encoding="utf-8"))
    (output_dir / "primary_body.md").write_text(primary_body + "\n", encoding="utf-8")
    (output_dir / "final_body.md").write_text(final_body + "\n", encoding="utf-8")
    (output_dir / "control_final_body.md").write_text(control_final_body + "\n", encoding="utf-8")

    total = native_seconds + fallback_seconds + curator_seconds + primary_seconds + reviser_seconds
    row.update(
        {
            "curator_seconds": curator_seconds,
            "primary_seconds": primary_seconds,
            "reviser_seconds": reviser_seconds,
            "treatment_full_total_seconds": round(total, 3),
            "treatment_vs_control_seconds_saved": round(control["total"] - total, 3),
            "treatment_vs_control_percent_saved": round((1 - total / control["total"]) * 100, 2),
            "primary_chars": len(primary_body),
            "final_chars": len(final_body),
            "control_final_chars": len(control_final_body),
        }
    )
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-label", required=True)
    parser.add_argument("--director-only", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    out = OUT_ROOT / args.run_label
    out.mkdir(parents=True, exist_ok=True)

    names = list(NATIVE_CONFIG)
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_one, name, args.run_label, director_only=args.director_only): name
            for name in names
        }
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["sample"])
    control_total = sum(row["control_total_seconds"] for row in rows)
    director_control = sum(row["control_director_seconds"] for row in rows)
    director_treatment = sum(row["effective_director_seconds"] for row in rows)
    summary: dict[str, Any] = {
        "schema_version": "native-director-structured-e2e-v1",
        "run": args.run_label,
        "director_only": args.director_only,
        "samples": len(rows),
        "native_director_accepted": sum(row["director_source"] == "native_structured" for row in rows),
        "director_fallbacks": sum(row["director_source"] != "native_structured" for row in rows),
        "average_structural_coverage": round(
            sum(row["native_structural_coverage"]["coverage"] for row in rows) / len(rows), 4
        ),
        "control_director_total_seconds": round(director_control, 3),
        "treatment_director_total_seconds": round(director_treatment, 3),
        "director_seconds_saved": round(director_control - director_treatment, 3),
        "director_percent_saved": round((1 - director_treatment / director_control) * 100, 2),
        "control_e2e_total_seconds": round(control_total, 3),
        "rows": rows,
    }
    if not args.director_only:
        treatment_total = sum(row["treatment_full_total_seconds"] for row in rows)
        summary.update(
            {
                "treatment_full_e2e_total_seconds": round(treatment_total, 3),
                "full_e2e_seconds_saved": round(control_total - treatment_total, 3),
                "full_e2e_percent_saved": round((1 - treatment_total / control_total) * 100, 2),
            }
        )
    (out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
