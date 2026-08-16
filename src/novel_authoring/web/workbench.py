"""Read-only query layer for the author-facing Novel Workbench.

The Workbench is a projection of the existing Book Library and Edition data.
It deliberately keeps chapter navigation on the query side: loading a
chapter never rebuilds, persists, approves, activates, or rolls back any
authoritative state.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from novel_authoring.author_control.book_profile import (
    PROFILE_DIMENSIONS,
    load_effective_book_profile,
)
from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.author_control.reveal import (
    TruthLens,
    build_reveal_agenda,
    build_secret_board,
    project_truth_lens,
    truth_knowledge_view,
)
from novel_authoring.author_control.service import author_control_view
from novel_authoring.author_control.truth import (
    list_open_creative_questions,
    list_secret_candidates,
)
from novel_authoring.canon.projection import load_projection_from_connection
from novel_authoring.edition import edition_chapters
from novel_authoring.progression.workspace import attach_progression_workspace
from novel_authoring.serial_kernel import narrative_drive_label

_EDITION_PURPOSE_LABELS = {
    "SOURCE_BASE": "来源底稿",
    "AUTHOR_REVISION": "当前路线修订",
    "ALTERNATE_ROUTE": "故事备选路线",
}


def _author_edition_groups(editions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = (
        ("CURRENT", "当前正式版本"),
        ("CANDIDATE", "正在修订"),
        ("ALTERNATE", "备选路线"),
        ("ARCHIVED", "已归档"),
    )
    groups: list[dict[str, Any]] = []
    for role, label in specs:
        items = []
        for item in editions:
            if str(item.get("official_role")) != role:
                continue
            ordinal = item.get("fork_chapter_ordinal")
            items.append(
                {
                    **item,
                    "purpose_label": _EDITION_PURPOSE_LABELS.get(
                        str(item.get("edition_purpose")), "待确认用途"
                    ),
                    "source_label": ("来源版本" if ordinal is None else f"从第 {ordinal} 章分开"),
                    "updated_label": item.get("activated_at") or item.get("created_at"),
                }
            )
        if items:
            groups.append({"role": role, "label": label, "items": items})
    return groups


WORKBENCH_MODES: tuple[str, ...] = (
    "home",
    "continue",
    "rewrite",
    "plan",
    "analysis",
    "continuity",
    "state",
    "growth",
    "truth",
)
WORKBENCH_RIGHT_TABS: tuple[str, ...] = ("prose", "state", "next")
WORKBENCH_STATE_TABS: tuple[str, ...] = (
    "overview",
    "characters",
    "inventory",
    "equipment",
    "abilities",
    "knowledge",
    "locations",
    "factions",
    "relationships",
    "world_rules",
    "tasks",
)
WORKBENCH_STATE_SCOPES: tuple[str, ...] = ("character", "global")

STATE_TAB_ITEMS = (
    ("overview", "本章变化", "◈", "chapter_delta"),
    ("characters", "人物", "♙", "characters"),
    ("inventory", "背包", "▦", "inventory"),
    ("equipment", "装备", "◫", "equipment"),
    ("abilities", "能力", "✦", "abilities"),
    ("knowledge", "认知边界", "◎", "knowledge_topics"),
    ("locations", "地点", "⌖", "locations"),
    ("factions", "势力", "⬡", "factions"),
    ("relationships", "关系", "⌘", "relationships"),
    ("world_rules", "世界规则", "§", "world_rules"),
    ("tasks", "剧情进展", "✓", "plot_status"),
)

STATE_LENS_LABELS = {
    "AUTHOR": "作者镜头",
    "READER": "读者镜头",
    "CHARACTER": "人物镜头",
}

STATE_SOURCE_LABELS = {
    "CANON": "◆ 正史确认",
    "SOURCE_VERIFIED": "✓ 原文确认",
    "SOURCE_BASELINE": "✓ 原文确认",
    "AUTHOR_INTENT": "✎ 作者规划",
    "PROVISIONAL": "△ 草稿推演",
    "SOFT_REFERENCE": "◇ 软参考",
    "UNKNOWN": "○ 尚无证据",
}

STATE_CATEGORY_LABELS = {
    "character_state": "人物",
    "item": "物品",
    "equipment": "装备",
    "resource": "资源",
    "capability": "能力",
    "knowledge": "认知",
    "location": "地点",
    "faction": "势力",
    "relationship": "关系",
    "world_rule": "世界规则",
    "task_or_promise": "剧情进展",
    "thread": "剧情线",
    "promise": "承诺",
}

MODE_LABELS = {
    "home": "工作台",
    "continue": "续写",
    "rewrite": "改写",
    "plan": "规划",
    "analysis": "分析",
    "continuity": "连续性审查",
    "state": "状态",
    "truth": "真相与揭示",
}
RIGHT_TAB_LABELS = {
    "prose": "正文",
    "state": "章末状态",
    "next": "下一章接续包",
}
STATUS_LABELS = {
    "ACTIVE": "使用中",
    "READY": "可用",
    "READY_WITH_GAPS": "可用但有待补齐",
    "NOT_STARTED": "尚未开始",
    "STALE": "需要刷新",
    "BLOCKED": "暂时受阻",
    "SOURCE": "原文（只读）",
    "CANON": "正史",
    "DRAFT": "草稿",
    "VALIDATED": "已校验草稿",
    "VALIDATED_DRAFT": "已校验草稿",
    "PROVISIONAL": "临时状态",
    "PROVISIONAL_DRAFT_ONLY": "草稿临时状态",
    "SOURCE_READ_ONLY": "原文只读",
    "NOT_RUN": "尚未运行",
    "NOT_RUN_OR_WARNING": "尚未完成或有提示",
    "PASS": "通过",
    "NO_CANON_EVENT_ANCHOR": "尚无正史锚点",
    "SOURCE_ONLY": "仅有原文",
    "EMPTY": "暂无数据",
    "NOT_AVAILABLE": "暂不可用",
    "PROVISIONAL_DRAFT_CONTEXT": "草稿临时上下文",
    "CANON_EVENT_PROJECTION": "已建立正史状态截面",
    "PROVISIONAL_DRAFT_DELTA": "草稿临时变化",
    "CANON_EVENT_DELTA": "已记录正史变化",
    "SOURCE_CHAPTER_STATE_PROJECTION_MISSING": "尚未建立历史章节状态",
}
SOURCE_COVERAGE_LABELS = {
    "NOT_STARTED": "尚未分析",
    "READY_FOR_CODEX": "等待 AI 处理",
    "RUNNING": "正在分析",
    "PARTIAL": "部分完成",
    "COMPLETE_NO_CHANGE": "已分析 · 无确认变化",
    "COMPLETE_WITH_CHANGES": "已分析 · 有确认变化",
    "FAILED": "分析失败",
}
COLLECTION_LABELS = {
    "facts": "事实",
    "timeline": "时间线",
    "entities": "实体",
    "character_states": "人物状态",
    "knowledge": "知识边界",
    "relationships": "关系",
    "resources": "资源",
    "capabilities": "能力",
    "threads": "剧情线",
    "promises": "伏笔承诺",
    "payoffs": "伏笔回收",
    "repetition": "重复风险",
    "style_profiles": "文风画像",
    "committed_chapters": "已确认章节",
}
CHANGE_KIND_LABELS = {
    "ADDED": "新增",
    "REMOVED": "移除",
    "CHANGED": "更新",
    "CHANGE": "变化",
}
STATE_COLLECTIONS = (
    ("character_states", "人物状态"),
    ("resources", "资源"),
    ("capabilities", "能力"),
    ("knowledge", "知识边界"),
    ("relationships", "关系"),
    ("threads", "剧情线"),
    ("promises", "伏笔承诺"),
    ("payoffs", "伏笔回收"),
)

_PROJECTION_COLLECTIONS = (
    "facts",
    "timeline",
    "entities",
    "character_states",
    "knowledge",
    "relationships",
    "resources",
    "capabilities",
    "threads",
    "promises",
    "payoffs",
    "repetition",
    "style_profiles",
    "committed_chapters",
)


def _human_label(value: Any, labels: dict[str, str], fallback: str = "待确认") -> str:
    raw = str(value or "")
    return labels.get(raw, fallback)


def _status_label(value: Any) -> str:
    return _human_label(value, STATUS_LABELS)


def _normalise_choice(value: Any, allowed: tuple[str, ...], fallback: str) -> str:
    candidate = str(value or "")
    return candidate if candidate in allowed else fallback


def _contains_cjk(value: Any) -> bool:
    return any("\u3400" <= character <= "\u9fff" for character in str(value or ""))


def _short_statement(value: Any, limit: int = 30) -> str:
    text = " ".join(str(value or "").split())
    if not text:
        return ""
    for separator in ("。", "；", "，"):
        head = text.split(separator, 1)[0].strip()
        if 4 <= len(head) <= limit:
            return head
    return text if len(text) <= limit else f"{text[:limit]}…"


def _author_record_name(record: dict[str, Any], fallback: str = "状态记录") -> str:
    name = str(record.get("name") or record.get("topic_name") or "").strip()
    if name and _contains_cjk(name) and ":" not in name:
        return name
    statement = _short_statement(
        record.get("statement") or record.get("description") or record.get("evidence_excerpt")
    )
    if statement and _contains_cjk(statement):
        return statement
    category = str(record.get("category") or "").lower()
    return {
        "character_state": "未命名人物",
        "character": "未命名人物",
        "item": "未命名物品",
        "equipment": "未命名装备",
        "resource": "未命名资源",
        "capability": "未命名能力",
        "knowledge": "未命名认知主题",
        "location": "未命名地点",
        "faction": "未命名势力",
        "relationship": "未命名关系",
        "world_rule": "未命名世界规则",
        "task_or_promise": "未命名剧情进展",
    }.get(category, fallback)


def _record_presentation(record: dict[str, Any], *, fallback: str = "状态记录") -> dict[str, Any]:
    result = dict(record)
    layer = str(result.get("current_layer") or result.get("layer") or "UNKNOWN")
    category = str(result.get("category") or "").lower()
    result["author_name"] = _author_record_name(result, fallback)
    result["author_category_label"] = str(
        result.get("category_label") or STATE_CATEGORY_LABELS.get(category) or fallback
    )
    result["source_label"] = STATE_SOURCE_LABELS.get(layer, "○ 边界待确认")
    result["recent_chapter_ordinal"] = (
        result.get("recent_confirmed_chapter_ordinal")
        or result.get("evidence_chapter_ordinal")
        or result.get("chapter_ordinal")
    )
    result["card_summary"] = _short_statement(
        result.get("description") or result.get("statement"), 42
    )
    if "history" in result:
        history: list[dict[str, Any]] = []
        for entry in result.get("history", []):
            presented = dict(entry)
            presented["author_name"] = _author_record_name(presented, result["author_name"])
            presented["source_label"] = STATE_SOURCE_LABELS.get(
                str(presented.get("layer") or "UNKNOWN"), "○ 边界待确认"
            )
            history.append(presented)
        result["history"] = history
    return result


def _record_value(record: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = record.get(key)
        if value not in (None, "", "UNKNOWN"):
            return value
    raw_value = record.get("raw")
    raw = raw_value if isinstance(raw_value, dict) else {}
    payload_value = raw.get("payload")
    payload = payload_value if isinstance(payload_value, dict) else {}
    for key in keys:
        value = payload.get(key)
        if value not in (None, "", "UNKNOWN"):
            return value
    attributes = record.get("attributes")
    if isinstance(attributes, list):
        for item in attributes:
            if not isinstance(item, dict):
                continue
            if str(item.get("key") or item.get("label") or "") in keys:
                value = item.get("value")
                if value not in (None, "", "UNKNOWN"):
                    return value
    return None


def _character_focus(state: dict[str, Any], recent_changes: list[dict[str, Any]]) -> dict[str, Any]:
    author_attributes = [
        item
        for item in state.get("attributes", [])
        if isinstance(item, dict) and item.get("author_visible")
    ]
    return {
        "location": _record_value(state, ("current_location", "location", "location_id"))
        or "本章尚未明确",
        "goal": _record_value(state, ("current_goal", "goal", "objective")) or "本章尚未明确",
        "body": _record_value(state, ("health", "body", "injury", "condition")) or "未见明确异常",
        "mood": _record_value(state, ("mood", "emotion", "mental_state")) or "本章尚未明确",
        "risk": _record_value(state, ("risk", "danger", "threat"))
        or ("本章状态有变化" if recent_changes else "本章无新增风险证据"),
        "stats": author_attributes[:8],
    }


def _relationship_author_label(record: dict[str, Any]) -> str:
    value = str(
        _record_value(
            record,
            ("relationship_state", "relation_type", "relationship_type", "label", "type"),
        )
        or ""
    )
    labels = {
        "CONDITIONAL_COOPERATION": "有条件合作",
        "COOPERATIVE_ACQUAINTANCES": "合作熟人",
        "RECIPROCAL_INFORMATION_TRADE": "互惠信息交易",
        "COOPERATION": "合作",
        "ALLY": "盟友",
        "ALLIANCE": "同盟",
        "HOSTILE": "敌对",
        "ENEMY": "敌对",
        "DEPENDENCE": "依赖",
        "TRADE": "交易",
        "RIVALRY": "竞争",
        "INTIMATE": "亲密",
        "CONCLUDED": "关系已收束",
    }
    if value.upper() in labels:
        return labels[value.upper()]
    if value and _contains_cjk(value):
        return value
    statement = _short_statement(record.get("statement") or record.get("description"), 16)
    return statement or "关系"


def _is_lens_visible(record: dict[str, Any], lens: str) -> bool:
    return lens == "AUTHOR" or record.get("visible") is not False


def _active_plot_record(record: dict[str, Any]) -> bool:
    raw_value = record.get("raw")
    raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
    payload_value = raw.get("payload")
    payload: dict[str, Any] = payload_value if isinstance(payload_value, dict) else {}
    state = str(
        next(
            (
                payload[key]
                for key in ("task_state", "lifecycle_status", "state", "status")
                if payload.get(key) not in (None, "", "UNKNOWN")
            ),
            _record_value(record, ("task_state", "lifecycle_status", "state", "status"))
            or "ACTIVE",
        )
    ).upper()
    return state not in {"COMPLETED", "DONE", "CLOSED", "CANCELLED", "RESOLVED"}


def _state_presentation(
    state: dict[str, Any],
    previous: dict[str, Any] | None,
    *,
    scope: str,
    lens_projection: dict[str, Any],
) -> dict[str, Any]:
    selected_id = str(state.get("selected_character_id") or "")
    characters = []
    for character in state.get("characters", []):
        item = dict(character)
        item["category"] = "character"
        item["author_name"] = _author_record_name(item, "未命名人物")
        item["source_label"] = STATE_SOURCE_LABELS.get(
            str(item.get("layer") or "UNKNOWN"), "○ 边界待确认"
        )
        characters.append(item)
    state["characters"] = characters
    character_names = {
        str(item.get("character_id")): str(item.get("author_name")) for item in characters
    }

    workspaces: list[dict[str, Any]] = []
    for workspace in state.get("character_workspaces", []):
        item = dict(workspace)
        item["author_name"] = character_names.get(
            str(item.get("character_id")), _author_record_name(item, "未命名人物")
        )
        item["recent_changes"] = [
            _record_presentation(change) for change in item.get("recent_changes", [])
        ]
        item["focus"] = _character_focus(item.get("state", {}), item["recent_changes"])
        for key in ("inventory", "equipment", "abilities", "relationships"):
            item[key] = [
                _record_presentation(record)
                for record in item.get(key, [])
                if _is_lens_visible(record, str(lens_projection["lens"]))
            ]
        workspaces.append(item)
    state["character_workspaces"] = workspaces
    state["selected_character_workspace"] = next(
        (item for item in workspaces if str(item.get("character_id")) == selected_id),
        None,
    )

    scoped_keys = {
        "inventory": "all_inventory",
        "equipment": "all_equipment",
        "abilities": "all_abilities",
        "relationships": "all_relationships",
    }
    for key, global_key in scoped_keys.items():
        source = state.get(global_key, []) if scope == "global" else state.get(key, [])
        state[f"visible_{key}"] = [
            _record_presentation(record)
            for record in source
            if _is_lens_visible(record, str(lens_projection["lens"]))
        ]
    for key in ("locations", "factions", "world_rules", "tasks", "threads", "promises"):
        state[key] = [
            _record_presentation(record)
            for record in state.get(key, [])
            if _is_lens_visible(record, str(lens_projection["lens"]))
        ]

    chapter_ordinal = int((state.get("chapter") or {}).get("ordinal") or 0)
    for item in state["locations"]:
        recent = int(item.get("recent_chapter_ordinal") or 0)
        item["recency_filter"] = (
            "current"
            if item.get("changed_this_chapter")
            else "recent"
            if recent and chapter_ordinal - recent <= 5
            else "known"
        )
    for item in state["factions"]:
        item["state_label"] = {
            "ACTIVE": "正在活动",
            "INACTIVE": "暂未活动",
            "DISSOLVED": "已经解散",
            "HOSTILE": "公开敌对",
            "FRIENDLY": "公开友好",
            "NEUTRAL": "公开中立",
        }.get(str(item.get("state") or "UNKNOWN").upper(), "公开状态尚未确认")
        item["goal_truth"] = next(
            (
                topic
                for topic in item.get("author_truth_topics", [])
                if str((topic.get("truth") or {}).get("truth_type") or "").upper() == "FACTION_GOAL"
            ),
            None,
        )

    for item in state["visible_relationships"]:
        item["from_name"] = character_names.get(
            str(item.get("from_entity_id") or ""), "未命名关系方"
        )
        item["to_name"] = character_names.get(str(item.get("to_entity_id") or ""), "未命名关系方")
        item["relationship_label"] = _relationship_author_label(item)

    faction_records: dict[str, dict[str, Any]] = {}
    for faction in state["factions"]:
        for identifier_key in ("faction_id", "object_id", "record_id", "id"):
            identifier = faction.get(identifier_key)
            if identifier:
                faction_records[str(identifier)] = faction
    character_records = {
        str(character.get("character_id")): character
        for character in characters
        if character.get("character_id")
    }
    graph = dict(state.get("relationship_graph") or {})
    relationship_records = {
        str(item.get("record_id") or ""): item
        for item in state["visible_relationships"]
        if item.get("record_id")
    }
    graph_nodes = []
    for node in graph.get("nodes", []):
        presented_node = dict(node)
        node_id = str(presented_node.get("node_id") or "")
        inspector = (
            faction_records.get(node_id)
            if presented_node.get("node_type") == "FACTION"
            else character_records.get(node_id)
        )
        if inspector is not None:
            presented_node["name"] = inspector["author_name"]
            presented_node["inspector"] = inspector
        graph_nodes.append(presented_node)
    graph["nodes"] = graph_nodes
    graph["edges"] = [
        {
            **edge,
            "label": relationship_records.get(str(edge.get("edge_id") or ""), {}).get(
                "relationship_label", edge.get("label") or "关系"
            ),
            "inspector": relationship_records.get(
                str(edge.get("edge_id") or ""), edge.get("inspector") or edge
            ),
        }
        for edge in graph.get("edges", [])
    ]
    state["relationship_graph"] = graph

    grouped: dict[str, dict[str, Any]] = {}
    for record in state.get("chapter_delta", {}).get("confirmed", []):
        presented = _record_presentation(record)
        key = str(presented.get("category") or "other")
        group = grouped.setdefault(
            key,
            {
                "key": key,
                "label": presented["author_category_label"],
                "items": [],
            },
        )
        group["items"].append(presented)
    state["delta_groups"] = list(grouped.values())

    scoped_count_key = "global" if scope == "global" else "selected_character"
    state["state_scope"] = scope
    state["scope_label"] = "全局" if scope == "global" else "选中人物"
    state["visible_scope_counts"] = {
        **state.get("scope_counts", {}).get(scoped_count_key, {}),
        "inventory": len(state["visible_inventory"]),
        "equipment": len(state["visible_equipment"]),
        "abilities": len(state["visible_abilities"]),
        "relationships": len(state["visible_relationships"]),
    }

    previous_counts: dict[str, int] = {}
    if previous is not None:
        previous_key = "global" if scope == "global" else "selected_character"
        previous_counts = dict(
            previous.get("scope_counts", {}).get(previous_key, previous.get("counts", {}))
        )
    comparison = []
    for key, label in (
        ("characters", "人物"),
        ("inventory", "背包"),
        ("equipment", "装备"),
        ("abilities", "能力"),
        ("relationships", "关系"),
    ):
        current_value = int(state["visible_scope_counts"].get(key, 0) or 0)
        previous_value = int(previous_counts.get(key, 0) or 0)
        comparison.append(
            {
                "key": key,
                "label": label,
                "current": current_value,
                "previous": previous_value,
                "difference": current_value - previous_value,
            }
        )
    state["comparison"] = comparison
    state["previous_chapter"] = None if previous is None else previous.get("chapter")

    matrix = state.get("knowledge_matrix", [])
    edges = state.get("knowledge_visibility_edges", [])
    state["knowledge_by_character"] = []
    for character in characters:
        character_id = str(character.get("character_id") or "")
        cells = [
            _record_presentation({**cell, "category": "knowledge"})
            for cell in edges
            if str(cell.get("knower_id") or "") == character_id
        ]
        state["knowledge_by_character"].append(
            {
                **character,
                "topics": cells,
                "evidence_count": sum(bool(item.get("source_span_ids")) for item in cells),
                "known_count": sum(item.get("state") != "UNKNOWN" for item in cells),
            }
        )
    state["knowledge_by_topic"] = []
    for topic in state.get("knowledge_topics", []):
        topic_id = str(topic.get("topic_id") or "")
        topic_edges = [item for item in edges if str(item.get("topic_id") or "") == topic_id]
        presented_topic = _record_presentation(
            {**topic, "category": "knowledge"}, fallback="认知主题"
        )
        state["knowledge_by_topic"].append(
            {
                **presented_topic,
                "known_by": [
                    {
                        **item,
                        "knower_name": character_names.get(
                            str(item.get("knower_id") or ""), "未命名人物"
                        ),
                    }
                    for item in topic_edges
                    if item.get("state") != "UNKNOWN"
                ],
                "evidence_count": sum(bool(item.get("source_span_ids")) for item in topic_edges),
            }
        )
    state["knowledge_matrix_payload"] = matrix

    lens_topics = []
    for topic in lens_projection.get("topics", []):
        item = dict(topic)
        truth = dict(item.get("truth") or {})
        truth["author_name"] = _author_record_name(
            {**truth, "category": "world_rule"}, "未命名真相"
        )
        truth["status_label"] = {
            "ACTIVE": "当前成立",
            "ACTIVE_TRUTH": "当前成立",
            "CONFLICTING": "与已发生正文冲突",
            "RETIRED": "已结束",
            "REVEALED": "已经揭示",
            "PROVISIONAL_TRUTH": "作者暂定",
            "IDEA": "作者构想",
            "DRAFT": "作者草案",
        }.get(str(truth.get("status") or "").upper(), "作者已记录")
        reader = item.get("reader")
        if isinstance(reader, dict):
            item["reader"] = {
                **reader,
                "state_label": {
                    "UNKNOWN": "读者尚未知",
                    "HINTED": "读者已有暗示",
                    "PARTIAL": "读者部分知情",
                    "KNOWN": "读者已经知道",
                }.get(str(reader.get("state") or "UNKNOWN").upper(), "读者边界待确认"),
            }
        item["truth"] = truth
        lens_topics.append(item)
    state["lens"] = {
        "value": lens_projection["lens"],
        "label": STATE_LENS_LABELS[str(lens_projection["lens"])],
        "character_name": character_names.get(selected_id, "所选人物"),
        "topics": lens_topics,
        "projection_only": True,
    }
    state["current_plot_status"] = [
        record
        for record in [*state["threads"], *state["promises"], *state["tasks"]]
        if _active_plot_record(record)
    ]
    return state


def _value_count(value: Any) -> int:
    if isinstance(value, (dict, list, tuple, set)):
        return len(value)
    return 1 if value else 0


def _state_cards(state: Any) -> list[dict[str, Any]]:
    if not isinstance(state, dict):
        return []
    cards: list[dict[str, Any]] = []
    for collection, label in STATE_COLLECTIONS:
        count = _value_count(state.get(collection))
        if count:
            cards.append({"label": label, "count": count, "summary": f"{count} 项记录"})
    return cards


def _change_view(change: Any) -> dict[str, Any]:
    item = dict(change) if isinstance(change, dict) else {"value": change}
    payload_value = item.get("payload")
    payload: dict[str, Any] = payload_value if isinstance(payload_value, dict) else {}
    kind = item.get("kind") or payload.get("status") or "CHANGE"
    description = (
        item.get("description")
        or payload.get("description")
        or payload.get("name")
        or item.get("record_id")
        or item.get("collection")
        or "本章有一项状态变化"
    )
    collection = item.get("collection")
    return {
        **item,
        "kind_label": _human_label(kind, CHANGE_KIND_LABELS, "变化"),
        "summary": str(description),
        "collection_label": COLLECTION_LABELS.get(str(collection), "章节状态")
        if collection
        else "章节状态",
    }


def _delta_author_summary(delta: dict[str, Any]) -> str:
    status = str(delta.get("status") or "")
    if status == "SOURCE_CHAPTER_STATE_PROJECTION_MISSING":
        return "目前无法确认这一章具体改变了哪些人物、资源或剧情线；系统不会用最新状态冒充历史。"
    count = int(delta.get("change_count") or len(delta.get("changes") or []))
    if status == "PROVISIONAL_DRAFT_DELTA":
        return f"这是草稿携带的临时变化，共 {count} 项；它还没有写入正史。"
    if count:
        return f"已从可追溯的章节状态中识别出 {count} 项变化。"
    return "已找到章节状态截面，但当前没有登记可见变化。"


def _projection_author_summary(availability: str, label: str) -> str:
    if availability == "SOURCE_CHAPTER_STATE_PROJECTION_MISSING":
        return (
            f"{('章前' if label == 'BEFORE_CHAPTER' else '章后')}状态暂不可回溯："
            "当前只有原文，还没有逐章建立历史状态记录。"
        )
    if availability == "PROVISIONAL_DRAFT_ONLY":
        return "这是草稿的临时章末状态，只用于检查，不代表已经写入正史。"
    return "已找到可追溯的正史状态截面，可以作为本章的历史锚点查看。"


def _book_row(connection: sqlite3.Connection, book_id: str) -> dict[str, Any]:
    row = connection.execute("SELECT * FROM books WHERE book_id=?", (book_id,)).fetchone()
    if row is None:
        raise ValueError("book 不存在")
    return dict(row)


def _edition_row(connection: sqlite3.Connection, book_id: str, edition_id: str) -> dict[str, Any]:
    row = connection.execute(
        "SELECT * FROM editions WHERE book_id=? AND edition_id=?",
        (book_id, edition_id),
    ).fetchone()
    if row is None:
        raise ValueError("edition 不存在")
    return dict(row)


def _base_chapters_without_edition(
    connection: sqlite3.Connection, book_id: str
) -> list[dict[str, Any]]:
    """Read imported base chapters from a deferred library add without mutating it."""

    rows = connection.execute(
        """
        SELECT c.*, d.status AS document_status, d.relative_path
        FROM chapters c JOIN source_documents d ON d.document_id=c.document_id
        WHERE c.book_id=? AND c.edition_id='base' AND d.status!='GENERATED_CANON'
        ORDER BY c.ordinal, c.created_at, c.chapter_id
        """,
        (book_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _read_json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if not value:
        return {}
    try:
        parsed = json.loads(str(value))
    except (TypeError, ValueError):
        return {"raw": str(value)}
    return parsed if isinstance(parsed, dict) else {"raw": parsed}


def _profile_data(
    database: Any, book_id: str, edition_id: str, selected_node: str
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    profile = load_effective_book_profile(database, book_id, edition_id)
    items = [
        {
            "id": str(item["dimension"]),
            "label": str(item["label"]),
            "filename": str(item["filename"]),
            "available": bool(item["available"]),
            "relative_path": f"book_profil/{item['filename']}",
            "author_edit_count": int(item["author_edit_count"]),
            "effective_source": str(item["effective_source"]),
        }
        for item in profile["dimensions"]
    ]
    selected: dict[str, Any] = {
        "id": selected_node,
        "label": "作者画像",
        "available": False,
        "content": "",
        "relative_path": "",
    }
    for dimension in profile["dimensions"]:
        if dimension["dimension"] == selected_node:
            selected = {
                **dimension,
                "id": dimension["dimension"],
            }
    manifest = {
        "profile_version_id": profile["profile_version_id"],
        "version_number": profile["version_number"],
        "edition_id": edition_id,
        "inherited_from_edition_id": profile["inherited_from_edition_id"],
        "hard_constraints": profile["hard_constraints"],
        "history": profile["history"],
        "proposals": profile["proposals"],
    }
    return items, selected, manifest


def _draft_rows(
    connection: sqlite3.Connection, book_id: str, edition_id: str
) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT d.*, c.target_chapter_ordinal, c.contract_json
        FROM drafts d
        LEFT JOIN chapter_contracts c
          ON c.book_id=d.book_id AND c.edition_id=d.edition_id
         AND c.contract_id=d.contract_id
        WHERE d.book_id=? AND d.edition_id=?
        ORDER BY COALESCE(c.target_chapter_ordinal, 0), d.created_at DESC, d.draft_id DESC
        """,
        (book_id, edition_id),
    ).fetchall()
    report_rows = connection.execute(
        """
        SELECT vr.draft_id, vr.validator, vr.severity, vr.passed,
               vr.report_json, vr.run_id
        FROM validation_reports vr
        JOIN drafts d ON d.draft_id=vr.draft_id
                     AND d.validation_run_id=vr.run_id
        WHERE d.book_id=? AND d.edition_id=?
        ORDER BY vr.draft_id, vr.validator
        """,
        (book_id, edition_id),
    ).fetchall()
    reports_by_draft: dict[str, list[sqlite3.Row]] = {}
    for report in report_rows:
        reports_by_draft.setdefault(str(report["draft_id"]), []).append(report)
    result: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        target = item.get("target_chapter_ordinal")
        item["target_chapter_ordinal"] = None if target is None else int(target)
        item["display_status"] = (
            "VALIDATED_DRAFT" if str(item.get("status")) == "VALIDATED" else str(item.get("status"))
        )
        item["display_status_label"] = _status_label(item["display_status"])
        item["contract_payload"] = _read_json(item.get("contract_json"))
        item["output"] = _read_json(item.get("output_json"))
        path = Path(str(item.get("file_path") or ""))
        try:
            item["content"] = path.read_text(encoding="utf-8")[:500_000] if path.is_file() else ""
        except OSError:
            item["content"] = ""
        item["validation_reports"] = [
            {
                **dict(report),
                "passed": bool(report["passed"]),
                "report": _read_json(report["report_json"]),
            }
            for report in reports_by_draft.get(str(item["draft_id"]), [])
        ]
        item["validation_warning_count"] = sum(
            1 for report in item["validation_reports"] if not report["passed"]
        )
        result.append(item)
    return result


def _candidate_cards(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    context_chapter_id: str | None,
    context_chapter_ordinal: int | None,
) -> list[dict[str, Any]]:
    task_id: str | None = None
    if context_chapter_id:
        handoffs = connection.execute(
            "SELECT task_manifest_path, result_json FROM workflow_handoffs "
            "WHERE book_id=? AND edition_id=? AND handoff_type='CONTINUATION' "
            "AND requested_stage='PLAN_ONLY' AND status='COMPLETED' "
            "AND result_json IS NOT NULL ORDER BY created_at DESC",
            (book_id, edition_id),
        ).fetchall()
        for handoff in handoffs:
            path = Path(str(handoff["task_manifest_path"] or ""))
            if not path.is_file():
                continue
            try:
                task = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if str(task.get("context_chapter_id") or "") != context_chapter_id:
                continue
            result_payload = _read_json(handoff["result_json"])
            candidate_ids = [
                str(item) for item in result_payload.get("candidate_ids", [])
            ]
            if not candidate_ids:
                continue
            placeholders = ",".join("?" for _ in candidate_ids)
            candidate_tasks = connection.execute(
                "SELECT DISTINCT task_id FROM candidate_plans "
                f"WHERE book_id=? AND edition_id=? AND candidate_id IN ({placeholders})",
                (book_id, edition_id, *candidate_ids),
            ).fetchall()
            if len(candidate_tasks) == 1:
                task_id = str(candidate_tasks[0]["task_id"])
                break
    else:
        latest = connection.execute(
            "SELECT task_id FROM candidate_plans WHERE book_id=? AND edition_id=? "
            "ORDER BY created_at DESC LIMIT 1",
            (book_id, edition_id),
        ).fetchone()
        if latest is not None:
            task_id = str(latest["task_id"])
    if task_id is None:
        return []
    rows = connection.execute(
        "SELECT * FROM candidate_plans WHERE book_id=? AND edition_id=? AND task_id=? "
        "ORDER BY CASE WHEN rank IS NULL THEN 999 ELSE rank END, candidate_id",
        (book_id, edition_id, task_id),
    ).fetchall()
    result: list[dict[str, Any]] = []
    agenda_labels = {
        "KEEP_HIDDEN": "继续隐藏",
        "SHOULD_HINT": "本章宜给线索",
        "MUST_REVEAL": "本章必须揭示",
    }
    depth_labels = {
        "HINT": "线索",
        "STRONG_HINT": "强线索",
        "PARTIAL_REVEAL": "部分揭示",
        "FULL_REVEAL": "完整揭示",
    }
    dimension_labels = {key: label for key, label, _ in PROFILE_DIMENSIONS}
    for row in rows:
        plan = _read_json(row["plan_json"])
        score = _read_json(row["score_json"])
        gate = _read_json(row["gate_report_json"])
        kernel_compilation = score.get("kernel_evidence_compilation")
        kernel_trace: dict[str, Any] = {
            "available": False,
            "completeness": "LEGACY_NO_EFFECTIVE_CONTRACT",
            "declared": {},
            "verified": {},
            "differences": [],
            "warnings": [],
            "evidence": [],
        }
        if isinstance(kernel_compilation, dict):
            declared = kernel_compilation.get("declared", {})
            verified = kernel_compilation.get("verified", {})
            verified = dict(verified) if isinstance(verified, dict) else {}
            verified_drive = verified.get("narrative_drive_alignment", {})
            if isinstance(verified_drive, dict) and verified_drive.get("primary_drive"):
                verified_drive = dict(verified_drive)
                verified_drive["primary_drive"] = narrative_drive_label(
                    str(verified_drive["primary_drive"])
                )
                verified["narrative_drive_alignment"] = verified_drive
            evidence: list[str] = []
            for item in kernel_compilation.get("verified_reader_promise_alignment", []):
                if isinstance(item, dict):
                    evidence.extend(str(value) for value in item.get("evidence", []))
            for item in kernel_compilation.get("verified_resource_impact", []):
                if isinstance(item, dict):
                    evidence.extend(str(value) for value in item.get("evidence", []))
            progress = kernel_compilation.get("verified_progress_components", {})
            if isinstance(progress, dict):
                evidence.extend(str(value) for value in progress.get("evidence", []))
            kernel_trace = {
                "available": True,
                "completeness": str(kernel_compilation.get("completeness") or "UNKNOWN"),
                "declared": dict(declared) if isinstance(declared, dict) else {},
                "verified": verified,
                "differences": [
                    str(item) for item in kernel_compilation.get("differences", [])
                ],
                "warnings": [str(item) for item in kernel_compilation.get("warnings", [])],
                "evidence": list(dict.fromkeys(evidence))[:12],
            }
        truth_alignment = list(plan.get("truth_alignment", []))
        reveal_impact = dict(plan.get("reveal_impact", {}))
        truth_effects = [
            {
                "truth_id": str(item.get("truth_id") or ""),
                "title": str(item.get("title") or item.get("truth_id") or "未命名真相"),
                "behavioral_effect": str(item.get("behavioral_effect") or "未说明行为约束"),
                "agenda_bucket": agenda_labels.get(
                    str(item.get("agenda_bucket") or "KEEP_HIDDEN"), "继续隐藏"
                ),
                "respected": bool(item.get("respected", False)),
            }
            for item in truth_alignment
            if isinstance(item, dict)
        ]
        truth_labels = {
            str(item["truth_id"]): str(item["title"]) for item in truth_effects if item["truth_id"]
        }

        secrets_used = [
            {
                "truth_id": str(value),
                "title": truth_labels.get(str(value), str(value)),
            }
            for value in reveal_impact.get("secrets_used", [])
        ]
        kept_hidden = [
            {
                "truth_id": str(value),
                "title": truth_labels.get(str(value), str(value)),
            }
            for value in reveal_impact.get("kept_hidden", [])
        ]

        reveal_previews: list[dict[str, Any]] = []
        for impact_key, impact_label in (
            ("hints", "线索"),
            ("partial_reveals", "部分揭示"),
            ("full_reveals", "完整揭示"),
        ):
            for item in reveal_impact.get(impact_key, []):
                if not isinstance(item, dict):
                    continue
                reveal_previews.append(
                    {
                        "kind": impact_label,
                        "truth_id": str(item.get("truth_id") or ""),
                        "depth": depth_labels.get(str(item.get("depth") or ""), "未注明深度"),
                        "clue": str(item.get("clue") or "未写明可读线索"),
                        "target": str(item.get("target") or "READER"),
                    }
                )
        narrative_drive_alignment = dict(plan.get("narrative_drive_alignment", {}))
        if narrative_drive_alignment.get("primary_drive"):
            narrative_drive_alignment["primary_drive"] = narrative_drive_label(
                str(narrative_drive_alignment["primary_drive"])
            )
        result.append(
            {
                "candidate_id": str(row["candidate_id"]),
                "context_chapter_id": context_chapter_id,
                "target_chapter_ordinal": (
                    context_chapter_ordinal + 1 if context_chapter_ordinal is not None else None
                ),
                "rank": row["rank"],
                "selection_status": str(row["selection_status"]),
                "title": str(plan.get("title") or row["candidate_id"]),
                "summary": str(plan.get("summary") or ""),
                "primary_function": plan.get("primary_function"),
                "reader_question": plan.get("reader_question"),
                "final_selection_score": score.get("final_selection_score")
                or score.get("score"),
                "score_available": (
                    str(score.get("score_status") or "COMPUTED") != "NOT_COMPUTED"
                    and isinstance(
                        score.get("final_selection_score") or score.get("score"),
                        (int, float),
                    )
                ),
                "gate_available": str(gate.get("gate_status") or "COMPUTED")
                != "NOT_RUN",
                "gate_passed": bool(gate.get("passed", False)),
                "hard_failures": list(gate.get("hard_failures", [])),
                "kernel_trace": kernel_trace,
                "author_control_trace": plan.get("author_control_trace", {}),
                "protagonist_choice": str(
                    plan.get("protagonist_strategy") or plan.get("solution_method") or ""
                ),
                "cost": str(plan.get("required_cost") or plan.get("opportunity_cost") or ""),
                "irreversible_change": str(plan.get("required_irreversible_change") or ""),
                "future_space": str(plan.get("ending_state") or ""),
                "main_risk": str(plan.get("risk_form") or ""),
                "plot_advances": list(plan.get("commit_updates", [])),
                "profile_alignment": {
                    **dict(plan.get("profile_alignment", {})),
                    "dimensions": [
                        {
                            **item,
                            "dimension": dimension_labels.get(
                                str(item.get("dimension") or ""),
                                str(item.get("dimension") or "未注明维度"),
                            ),
                        }
                        for item in dict(plan.get("profile_alignment", {})).get("dimensions", [])
                        if isinstance(item, dict)
                    ],
                },
                "state_changes": list(plan.get("state_changes", [])),
                "truth_effects": truth_effects,
                "reveal_previews": reveal_previews,
                "secrets_used": secrets_used,
                "kept_hidden": kept_hidden,
                "reader_knowledge_delta": list(reveal_impact.get("reader_knowledge_delta", [])),
                "character_knowledge_delta": list(
                    reveal_impact.get("character_knowledge_delta", [])
                ),
                "reader_promise_alignment": list(
                    plan.get("reader_promise_alignment", [])
                ),
                "narrative_drive_alignment": narrative_drive_alignment,
                "progression_impact": dict(plan.get("progression_impact", {})),
                "payoff_channel_impact": list(plan.get("payoff_channel_impact", [])),
                "world_expansion_impact": list(plan.get("world_expansion_impact", [])),
                "resource_opportunity_impact": list(
                    plan.get("resource_opportunity_impact", [])
                ),
                "anticipation_impact": list(plan.get("anticipation_impact", [])),
                "genre_drift_diagnostic": dict(
                    plan.get("genre_drift_diagnostic", {})
                ),
                "genre_evolution_diagnostic": dict(
                    plan.get("genre_evolution_diagnostic", {})
                ),
            }
        )
    return result


def _draft_tree_items(drafts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only the newest visible draft for each target chapter."""

    latest: dict[int, dict[str, Any]] = {}
    for draft in drafts:
        ordinal = draft.get("target_chapter_ordinal")
        if ordinal is None or ordinal in latest:
            continue
        latest[int(ordinal)] = {
            "chapter_id": None,
            "draft_id": str(draft["draft_id"]),
            "ordinal": int(ordinal),
            "title": str(draft.get("chapter_title") or f"第{ordinal}章"),
            "status": str(draft["display_status"]),
            "status_label": str(
                draft.get("display_status_label") or _status_label(draft["display_status"])
            ),
            "warning_count": int(draft.get("validation_warning_count", 0)),
            "is_draft": True,
        }
    return [latest[key] for key in sorted(latest)]


def _chapter_tree_items(chapters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for chapter in chapters:
        document_status = str(chapter.get("document_status") or "SOURCE")
        status = "CANON" if document_status == "GENERATED_CANON" else "SOURCE"
        result.append(
            {
                "chapter_id": str(chapter["chapter_id"]),
                "draft_id": None,
                "ordinal": int(chapter["ordinal"]),
                "title": str(chapter["title"]),
                "status": status,
                "status_label": _status_label(status),
                "warning_count": 0,
                "is_draft": False,
            }
        )
    return result


def _selected_records(
    chapters: list[dict[str, Any]],
    drafts: list[dict[str, Any]],
    *,
    chapter_id: str | None,
    draft_id: str | None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    selected_draft = next(
        (draft for draft in drafts if draft_id and str(draft["draft_id"]) == draft_id), None
    )
    selected_chapter = next(
        (
            chapter
            for chapter in chapters
            if chapter_id and str(chapter["chapter_id"]) == chapter_id
        ),
        None,
    )
    if selected_chapter is None and selected_draft is not None:
        target = selected_draft.get("target_chapter_ordinal")
        selected_chapter = next(
            (
                chapter
                for chapter in chapters
                if target is not None and int(chapter["ordinal"]) == int(target)
            ),
            None,
        )
    if selected_chapter is None and selected_draft is None and chapters:
        selected_chapter = chapters[-1]
    return selected_chapter, selected_draft


def _commit_anchors(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapters: list[dict[str, Any]],
) -> dict[int, int]:
    rows = connection.execute(
        """
        SELECT chapter_id, MAX(event_end_seq) AS event_end_seq
        FROM canon_commits
        WHERE book_id=? AND edition_id=?
        GROUP BY chapter_id
        """,
        (book_id, edition_id),
    ).fetchall()
    event_seq_by_chapter = {
        str(row["chapter_id"]): int(row["event_end_seq"])
        for row in rows
        if row["event_end_seq"] is not None
    }
    return {
        int(chapter["ordinal"]): event_seq_by_chapter[str(chapter["chapter_id"])]
        for chapter in chapters
        if str(chapter.get("document_status")) == "GENERATED_CANON"
        and str(chapter["chapter_id"]) in event_seq_by_chapter
    }


def _projection_view(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    ordinal: int,
    event_seq: int | None,
    label: str,
) -> dict[str, Any]:
    if event_seq is None:
        reason = (
            "当前章节只有不可变 Source 章节；尚未建立逐章 Source-Derived Runtime "
            "State Projection，不能把最新状态冒充历史截面。"
        )
        return {
            "availability": "SOURCE_CHAPTER_STATE_PROJECTION_MISSING",
            "label": label,
            "anchor_chapter_ordinal": ordinal,
            "through_event_seq": None,
            "availability_label": _status_label("SOURCE_CHAPTER_STATE_PROJECTION_MISSING"),
            "author_summary": _projection_author_summary(
                "SOURCE_CHAPTER_STATE_PROJECTION_MISSING", label
            ),
            "reason": reason,
        }
    projection = load_projection_from_connection(
        connection,
        book_id,
        edition_id=edition_id,
        through_event_seq=event_seq,
    )
    state = projection.model_dump(mode="json")
    return {
        "availability": "CANON_EVENT_PROJECTION",
        "label": label,
        "anchor_chapter_ordinal": ordinal,
        "through_event_seq": event_seq,
        "projection_hash": projection.sha256(),
        "state": state,
        "availability_label": _status_label("CANON_EVENT_PROJECTION"),
        "author_summary": _projection_author_summary("CANON_EVENT_PROJECTION", label),
        "state_cards": _state_cards(state),
    }


def _projection_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_state = before.get("state")
    after_state = after.get("state")
    if not isinstance(before_state, dict) or not isinstance(after_state, dict):
        return {
            "status": "SOURCE_CHAPTER_STATE_PROJECTION_MISSING",
            "changes": [],
            "display_changes": [],
            "status_label": _status_label("SOURCE_CHAPTER_STATE_PROJECTION_MISSING"),
            "author_summary": _delta_author_summary(
                {"status": "SOURCE_CHAPTER_STATE_PROJECTION_MISSING"}
            ),
            "reason": after.get("reason") or before.get("reason"),
        }
    changes: list[dict[str, Any]] = []
    for collection in _PROJECTION_COLLECTIONS:
        old = before_state.get(collection) or {}
        new = after_state.get(collection) or {}
        if not isinstance(old, dict) or not isinstance(new, dict):
            continue
        for record_id in sorted(set(old) | set(new)):
            if record_id not in old:
                changes.append(
                    {
                        "collection": collection,
                        "record_id": record_id,
                        "kind": "ADDED",
                        "after": new[record_id],
                    }
                )
            elif record_id not in new:
                changes.append(
                    {
                        "collection": collection,
                        "record_id": record_id,
                        "kind": "REMOVED",
                        "before": old[record_id],
                    }
                )
            elif old[record_id] != new[record_id]:
                changes.append(
                    {
                        "collection": collection,
                        "record_id": record_id,
                        "kind": "CHANGED",
                        "before": old[record_id],
                        "after": new[record_id],
                    }
                )
    return {
        "status": "CANON_EVENT_DELTA",
        "changes": changes,
        "display_changes": [_change_view(change) for change in changes],
        "change_count": len(changes),
        "status_label": _status_label("CANON_EVENT_DELTA"),
        "author_summary": _delta_author_summary(
            {"status": "CANON_EVENT_DELTA", "change_count": len(changes)}
        ),
    }


def _validation_context(
    selected_draft: dict[str, Any] | None,
) -> dict[str, Any]:
    if selected_draft is None:
        return {
            "status": "SOURCE_READ_ONLY",
            "status_label": _status_label("SOURCE_READ_ONLY"),
            "hard_gate": "NOT_RUN",
            "hard_gate_label": _status_label("NOT_RUN"),
            "reports": [],
        }
    reports = selected_draft.get("validation_reports", [])
    return {
        "status": selected_draft.get("display_status", selected_draft.get("status")),
        "status_label": selected_draft.get(
            "display_status_label", _status_label(selected_draft.get("display_status"))
        ),
        "hard_gate": (
            "PASS" if reports and all(item["passed"] for item in reports) else "NOT_RUN_OR_WARNING"
        ),
        "hard_gate_label": _status_label(
            "PASS" if reports and all(item["passed"] for item in reports) else "NOT_RUN_OR_WARNING"
        ),
        "reports": reports,
    }


def _chapter_context(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapters: list[dict[str, Any]],
    selected_chapter: dict[str, Any] | None,
    selected_draft: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if selected_chapter is None and selected_draft is None:
        return None
    if selected_chapter is not None:
        ordinal_value = selected_chapter.get("ordinal")
    elif selected_draft is not None:
        ordinal_value = selected_draft.get("target_chapter_ordinal")
    else:
        return None
    if ordinal_value is None:
        return None
    ordinal = int(ordinal_value)
    anchors = _commit_anchors(connection, book_id, edition_id, chapters)
    before_seq = max(
        (seq for chapter_ordinal, seq in anchors.items() if chapter_ordinal < ordinal),
        default=None,
    )
    after_seq = max(
        (seq for chapter_ordinal, seq in anchors.items() if chapter_ordinal <= ordinal),
        default=None,
    )
    before = _projection_view(
        connection,
        book_id,
        edition_id,
        ordinal=ordinal,
        event_seq=before_seq,
        label="BEFORE_CHAPTER",
    )
    after = _projection_view(
        connection,
        book_id,
        edition_id,
        ordinal=ordinal,
        event_seq=after_seq,
        label="AFTER_CHAPTER",
    )
    delta = _projection_delta(before, after)
    provisional = selected_draft is not None
    if selected_draft is not None:
        output = _read_json(selected_draft.get("output_json"))
        state_changes = output.get("state_changes", [])
        if not isinstance(state_changes, list):
            state_changes = []
        if state_changes:
            delta = {
                "status": "PROVISIONAL_DRAFT_DELTA",
                "changes": state_changes,
                "display_changes": [_change_view(change) for change in state_changes],
                "change_count": len(state_changes),
                "status_label": _status_label("PROVISIONAL_DRAFT_DELTA"),
                "author_summary": _delta_author_summary(
                    {"status": "PROVISIONAL_DRAFT_DELTA", "change_count": len(state_changes)}
                ),
                "note": "这是 Draft 自带的 provisional state_changes，不是 Canon Event。",
            }
            after = {
                "availability": "PROVISIONAL_DRAFT_ONLY",
                "label": "PROVISIONAL_AFTER_CHAPTER",
                "anchor_chapter_ordinal": ordinal,
                "based_on": after,
                "state_changes": state_changes,
                "availability_label": _status_label("PROVISIONAL_DRAFT_ONLY"),
                "author_summary": _projection_author_summary(
                    "PROVISIONAL_DRAFT_ONLY", "PROVISIONAL_AFTER_CHAPTER"
                ),
            }
        elif after.get("availability") != "CANON_EVENT_PROJECTION":
            after = {
                **after,
                "availability": "PROVISIONAL_DRAFT_ONLY",
                "label": "PROVISIONAL_AFTER_CHAPTER",
                "availability_label": _status_label("PROVISIONAL_DRAFT_ONLY"),
                "author_summary": _projection_author_summary(
                    "PROVISIONAL_DRAFT_ONLY", "PROVISIONAL_AFTER_CHAPTER"
                ),
                "note": "Draft 正文存在，但没有可审计的 provisional state_changes。",
            }
    source_content = "" if selected_chapter is None else str(selected_chapter.get("content") or "")
    draft_content = "" if selected_draft is None else str(selected_draft.get("content") or "")
    if selected_draft is not None:
        status = str(selected_draft.get("display_status"))
    elif selected_chapter is not None:
        status = (
            "CANON"
            if str(selected_chapter.get("document_status")) == "GENERATED_CANON"
            else "SOURCE"
        )
    else:
        return None
    source_boundary = max(
        (
            int(chapter["ordinal"])
            for chapter in chapters
            if str(chapter.get("document_status")) != "GENERATED_CANON"
        ),
        default=0,
    )
    canon_boundary = max(anchors, default=0)
    narrative_context: dict[str, Any] = {"status": "NOT_AVAILABLE"}
    if selected_draft is not None:
        contract = selected_draft.get("contract_payload") or {}
        narrative_context = {
            "status": "PROVISIONAL_DRAFT_CONTEXT",
            "lens": contract.get("lens"),
            "narrative_portfolio": contract.get("narrative_portfolio", {}),
            "narrative_debt": contract.get("narrative_debt", {}),
            "innovation_control": selected_draft.get("output", {}).get("innovation_control")
            if isinstance(selected_draft.get("output"), dict)
            else None,
        }
    return {
        "book_id": book_id,
        "edition_id": edition_id,
        "chapter_id": None if selected_chapter is None else str(selected_chapter["chapter_id"]),
        "chapter_ordinal": ordinal,
        "chapter_status": status,
        "chapter_status_label": _status_label(status),
        "selected_chapter_anchor": ordinal,
        "read_only_navigation": True,
        "before_state": before,
        "chapter_delta": delta,
        "after_state": after,
        "source_content": source_content,
        "draft_content": draft_content,
        "validation": _validation_context(selected_draft),
        "narrative_context": narrative_context,
        "canonical_boundary": {
            "chapter_ordinal": canon_boundary,
            "event_seq": max(anchors.values(), default=0),
            "status": "CANON" if canon_boundary else "NO_CANON_EVENT_ANCHOR",
            "status_label": _status_label("CANON" if canon_boundary else "NO_CANON_EVENT_ANCHOR"),
        },
        "source_boundary": {
            "chapter_ordinal": source_boundary,
            "status": "SOURCE_ONLY" if source_boundary else "EMPTY",
            "status_label": _status_label("SOURCE_ONLY" if source_boundary else "EMPTY"),
        },
        "provisional": provisional,
        "provisional_label": "草稿临时状态" if provisional else "原文只读",
    }


def _public_chapter_context(context: dict[str, Any] | None) -> dict[str, Any] | None:
    if context is None:
        return None
    return context


def _continuation_package(selected_draft: dict[str, Any] | None) -> dict[str, Any]:
    if selected_draft is None:
        return {
            "available": False,
            "status": "NOT_AVAILABLE",
            "status_label": "尚未生成接续包",
            "author_summary": (
                "当前章节没有可直接读取的下一章接续包。先在工作流中准备续写任务，"
                "系统才会生成可审计的边界包和章节合同。"
            ),
        }
    contract = selected_draft.get("contract_payload")
    if not isinstance(contract, dict) or not contract:
        return {
            "available": False,
            "status": "NOT_AVAILABLE",
            "status_label": "接续包尚未完成",
            "author_summary": (
                "当前有草稿正文，但还没有可审计的章节合同；因此不能把它当作下一章接续依据。"
            ),
        }
    return {
        "available": True,
        "status": "PROVISIONAL_DRAFT_CONTEXT",
        "status_label": "草稿接续信息",
        "author_summary": "当前草稿带有章节合同，可用于继续检查，但仍需完成校验和作者批准。",
        "lens": contract.get("lens"),
        "portfolio": contract.get("narrative_portfolio", {}),
        "debt": contract.get("narrative_debt", {}),
    }


def build_workbench_context(
    database: Any,
    book_id: str,
    edition_id: str | None,
    *,
    chapter_id: str | None = None,
    draft_id: str | None = None,
    node: str = "overview",
    mode: str = "home",
    right_tab: str = "prose",
    state_tab: str = "overview",
    state_scope: str = "character",
    character_id: str | None = None,
    truth_lens: str = "AUTHOR",
    truth_id: str | None = None,
    include_future_truths: bool = False,
) -> dict[str, Any]:
    """Build one Workbench read model without initializing or mutating the DB."""

    active_mode = _normalise_choice(mode, WORKBENCH_MODES, "home")
    active_right_tab = _normalise_choice(right_tab, WORKBENCH_RIGHT_TABS, "prose")
    active_state_tab = _normalise_choice(state_tab, WORKBENCH_STATE_TABS, "overview")
    active_state_scope = _normalise_choice(state_scope, WORKBENCH_STATE_SCOPES, "character")
    with database.connect() as connection:
        book = _book_row(connection, book_id)
        selected_edition_id = edition_id or str(book.get("active_edition_id") or "base")
        edition_rows = connection.execute(
            "SELECT edition_id, display_name, status, parent_edition_id, "
            "edition_purpose, official_role, fork_chapter_ordinal, created_at, "
            "activated_at, purpose_review_required "
            "FROM editions WHERE book_id=? ORDER BY created_at, edition_id",
            (book_id,),
        ).fetchall()
        editions = [dict(row) for row in edition_rows]
        if not editions and selected_edition_id == "base":
            edition = {
                "edition_id": "base",
                "display_name": str(book.get("title") or book_id),
                "status": "ACTIVE",
                "parent_edition_id": None,
                "edition_purpose": "SOURCE_BASE",
                "official_role": "CURRENT",
                "fork_chapter_ordinal": None,
                "created_at": str(book.get("created_at") or ""),
                "activated_at": None,
                "purpose_review_required": False,
            }
            editions = [dict(edition)]
        else:
            edition = _edition_row(connection, book_id, selected_edition_id)
        edition = {**edition, "status_label": _status_label(edition.get("status"))}
        editions = [
            {**item, "status_label": _status_label(item.get("status"))} for item in editions
        ]
        raw_chapters = (
            _base_chapters_without_edition(connection, book_id)
            if not edition_rows and selected_edition_id == "base"
            else edition_chapters(connection, book_id, selected_edition_id)
        )
        drafts = _draft_rows(connection, book_id, selected_edition_id)
        selected_chapter, selected_draft = _selected_records(
            raw_chapters,
            drafts,
            chapter_id=chapter_id,
            draft_id=draft_id,
        )
        selected_anchor = None
        if selected_chapter is not None:
            selected_anchor = int(selected_chapter["ordinal"])
        elif selected_draft is not None:
            selected_anchor = selected_draft.get("target_chapter_ordinal")
        candidate_cards = _candidate_cards(
            connection,
            book_id,
            selected_edition_id,
            context_chapter_id=(
                None if selected_chapter is None else str(selected_chapter["chapter_id"])
            ),
            context_chapter_ordinal=(
                None if selected_chapter is None else int(selected_chapter["ordinal"])
            ),
        )
        selected_node = node
        valid_profile_nodes = {item[0] for item in PROFILE_DIMENSIONS}
        if selected_node not in valid_profile_nodes and selected_node not in {
            "overview",
            "chapter",
            "planning",
            "state",
            "growth",
            "truth",
            "truth-board",
            "secret-board",
            "reveal-agenda",
        }:
            selected_node = "overview"
        if (selected_chapter is not None or selected_draft is not None) and node == "chapter":
            selected_node = "chapter"
        if selected_node == "chapter" and selected_chapter is None and selected_draft is None:
            selected_node = "overview"
        chapter_context = (
            _chapter_context(
                connection,
                book_id,
                selected_edition_id,
                raw_chapters,
                selected_chapter,
                selected_draft,
            )
            if active_mode == "continuity" or selected_node == "chapter"
            else None
        )
        if chapter_context is not None:
            chapter_ordinal = int(chapter_context["chapter_ordinal"])
            chapter_context["next_chapter"] = next(
                (
                    {
                        "chapter_id": str(item["chapter_id"]),
                        "ordinal": int(item["ordinal"]),
                        "title": str(item["title"]),
                    }
                    for item in raw_chapters
                    if int(item["ordinal"]) == chapter_ordinal + 1
                ),
                None,
            )
    profile_items, selected_profile, profile_manifest = _profile_data(
        database, book_id, selected_edition_id, selected_node
    )
    chapter_items = _chapter_tree_items(raw_chapters)
    draft_items = _draft_tree_items(drafts)
    latest_chapter = chapter_items[-1] if chapter_items else None
    if selected_anchor is None and latest_chapter is not None:
        selected_anchor = int(latest_chapter["ordinal"])
    story_game_state: dict[str, Any] | None = None
    previous_story_game_state: dict[str, Any] | None = None
    author_control: dict[str, Any] | None = None
    truth_projection: dict[str, Any] | None = None
    truth_knowledge: dict[str, Any] | None = None
    reveal_agenda: dict[str, Any] | None = None
    secret_board: dict[str, Any] | None = None
    open_questions: list[dict[str, Any]] = []
    secret_candidates: list[dict[str, Any]] = []
    selected_lens = TruthLens(str(truth_lens).upper())
    state_chapter_id = None if selected_chapter is None else str(selected_chapter["chapter_id"])
    needs_story_state = (
        active_mode in {"state", "growth", "continuity", "truth"}
        or active_right_tab == "state"
    )
    needs_previous_state = active_mode in {"continuity", "truth"} or (
        active_mode == "state" and active_state_tab == "overview"
    )
    include_knowledge_matrix = active_mode == "state" and active_state_tab == "knowledge"
    if selected_chapter is not None and needs_story_state:
        story_game_state = build_story_game_state(
            database,
            book_id,
            selected_edition_id,
            chapter_id=state_chapter_id,
            character_id=character_id,
            include_global_scope=(active_mode == "state" and active_state_scope == "global"),
            include_knowledge_state=False,
            include_knowledge_matrix=include_knowledge_matrix,
            include_history=False,
        )
        if active_mode == "growth":
            story_game_state = attach_progression_workspace(
                database,
                book_id=book_id,
                edition_id=selected_edition_id,
                world_state=story_game_state,
            )
        story_game_state["coverage_status_label"] = SOURCE_COVERAGE_LABELS.get(
            str(story_game_state.get("coverage_status") or "NOT_STARTED"), "状态未知"
        )
        selected_ordinal = int(selected_chapter["ordinal"])
        previous_chapter = next(
            (item for item in raw_chapters if int(item["ordinal"]) == selected_ordinal - 1),
            None,
        )
        if previous_chapter is not None and needs_previous_state:
            previous_story_game_state = build_story_game_state(
                database,
                book_id,
                selected_edition_id,
                chapter_id=str(previous_chapter["chapter_id"]),
                character_id=character_id,
                include_global_scope=(active_mode == "state" and active_state_scope == "global"),
                include_knowledge_state=False,
                include_knowledge_matrix=include_knowledge_matrix,
                include_history=False,
            )
            previous_story_game_state["coverage_status_label"] = SOURCE_COVERAGE_LABELS.get(
                str(previous_story_game_state.get("coverage_status") or "NOT_STARTED"),
                "状态未知",
            )
    if active_mode == "state":
        if story_game_state is None:
            story_game_state = build_story_game_state(
                database,
                book_id,
                selected_edition_id,
                chapter_id=None,
                character_id=character_id,
                include_global_scope=active_state_scope == "global",
                include_knowledge_state=False,
                include_knowledge_matrix=include_knowledge_matrix,
                include_history=False,
            )
            story_game_state["coverage_status_label"] = SOURCE_COVERAGE_LABELS.get(
                str(story_game_state.get("coverage_status") or "NOT_STARTED"),
                "状态未知",
            )
        state_ordinal = int(
            (story_game_state.get("chapter") or {}).get("ordinal") or selected_anchor or 0
        )
        state_character_id = str(story_game_state.get("selected_character_id") or "")
        if selected_lens is TruthLens.CHARACTER and not state_character_id:
            state_lens_projection = {
                "lens": selected_lens.value,
                "topics": [],
            }
        else:
            state_lens_projection = project_truth_lens(
                database,
                book_id,
                selected_edition_id,
                chapter_ordinal=state_ordinal,
                lens=selected_lens,
                character_id=(state_character_id if selected_lens is TruthLens.CHARACTER else None),
                include_future=False,
            )
        state_truth_topics_value: Any = state_lens_projection.get("topics", [])
        state_truth_topics: list[dict[str, Any]] = [
            dict(topic) for topic in state_truth_topics_value if isinstance(topic, dict)
        ]
        for collection, subject_type, identifier_keys in (
            ("characters", "CHARACTER", ("character_id", "record_id", "id")),
            ("factions", "FACTION", ("faction_id", "object_id", "record_id", "id")),
            ("locations", "LOCATION", ("location_id", "object_id", "record_id", "id")),
            ("inventory", "ITEM", ("object_id", "item_id", "record_id", "id")),
            ("all_inventory", "ITEM", ("object_id", "item_id", "record_id", "id")),
            ("equipment", "ITEM", ("object_id", "item_id", "record_id", "id")),
            ("all_equipment", "ITEM", ("object_id", "item_id", "record_id", "id")),
            ("abilities", "ABILITY", ("object_id", "ability_id", "record_id", "id")),
            (
                "all_abilities",
                "ABILITY",
                ("object_id", "ability_id", "record_id", "id"),
            ),
            (
                "relationships",
                "RELATIONSHIP",
                ("object_id", "relationship_id", "record_id", "id"),
            ),
            (
                "all_relationships",
                "RELATIONSHIP",
                ("object_id", "relationship_id", "record_id", "id"),
            ),
            ("world_rules", "WORLD_RULE", ("object_id", "rule_id", "record_id", "id")),
        ):
            enriched: list[dict[str, Any]] = []
            for record in story_game_state.get(collection, []):
                entity_id = str(
                    next(
                        (
                            record[key]
                            for key in identifier_keys
                            if record.get(key) not in (None, "")
                        ),
                        "",
                    )
                )
                matching_topics = [
                    topic
                    for topic in state_truth_topics
                    if isinstance(topic.get("truth"), dict)
                    and str(topic["truth"].get("subject_type") or "").upper() == subject_type
                    and str(topic["truth"].get("subject_id") or "") == entity_id
                ]
                enriched.append(
                    {
                        **record,
                        "author_truth_topics": matching_topics,
                        "reveal_plans": [
                            plan
                            for topic in matching_topics
                            for plan in topic.get("reveal_plans", [])
                        ],
                        "reader": (
                            matching_topics[0].get("reader")
                            if len(matching_topics) == 1
                            else record.get("reader")
                        ),
                    }
                )
            story_game_state[collection] = enriched
        selected_character_record = next(
            (
                item
                for item in story_game_state.get("characters", [])
                if item.get("character_id") == story_game_state.get("selected_character_id")
            ),
            None,
        )
        if selected_character_record is not None:
            story_game_state["character"] = {
                **story_game_state.get("character", {}),
                "author_truth_topics": selected_character_record.get("author_truth_topics", []),
            }
        story_game_state = _state_presentation(
            story_game_state,
            previous_story_game_state,
            scope=active_state_scope,
            lens_projection=state_lens_projection,
        )
        current_state_ordinal = int((story_game_state.get("chapter") or {}).get("ordinal") or 0)
        story_game_state["chapter_navigation"] = {
            direction: next(
                (
                    {
                        "chapter_id": str(item["chapter_id"]),
                        "ordinal": int(item["ordinal"]),
                        "title": str(item["title"]),
                    }
                    for item in raw_chapters
                    if int(item["ordinal"])
                    == current_state_ordinal + (-1 if direction == "previous" else 1)
                ),
                None,
            )
            for direction in ("previous", "next")
        }
        author_control = author_control_view(database, book_id, selected_edition_id)
    truth_chapter_ordinal = int(selected_anchor or 0)
    if active_mode == "truth" or selected_node in {
        "truth",
        "truth-board",
        "secret-board",
        "reveal-agenda",
    }:
        truth_projection = project_truth_lens(
            database,
            book_id,
            selected_edition_id,
            chapter_ordinal=truth_chapter_ordinal,
            lens=selected_lens,
            character_id=(
                character_id
                or (
                    None
                    if story_game_state is None
                    else story_game_state.get("selected_character_id")
                )
            ),
            include_future=(selected_lens is TruthLens.AUTHOR and include_future_truths),
        )
        chapter_characters = (
            [] if story_game_state is None else story_game_state.get("characters", [])
        )
        for topic in truth_projection["topics"]:
            known_by_character = {
                str(item["character_id"]): item for item in topic.get("characters", [])
            }
            topic["character_matrix"] = [
                {
                    "character_id": str(character["character_id"]),
                    "name": str(character.get("name") or character["character_id"]),
                    "state": known_by_character.get(
                        str(character["character_id"]),
                        {"state": "UNKNOWN"},
                    )["state"],
                    "edge": known_by_character.get(str(character["character_id"])),
                }
                for character in chapter_characters
                if character.get("character_id")
            ]
        if truth_id is not None:
            truth_projection["topics"] = [
                topic
                for topic in truth_projection["topics"]
                if topic["truth"]["truth_id"] == truth_id
            ]
        if selected_lens is TruthLens.AUTHOR:
            truth_knowledge = truth_knowledge_view(
                database,
                book_id,
                selected_edition_id,
                chapter_ordinal=truth_chapter_ordinal,
                truth_id=truth_id,
            )
            reveal_agenda = build_reveal_agenda(
                database, book_id, selected_edition_id, truth_chapter_ordinal
            )
            secret_board = build_secret_board(
                database,
                book_id,
                selected_edition_id,
                chapter_ordinal=truth_chapter_ordinal,
            )
            open_questions = list_open_creative_questions(database, book_id, selected_edition_id)
            secret_candidates = list_secret_candidates(database, book_id, selected_edition_id)
    if selected_lens is not TruthLens.AUTHOR:
        candidate_cards = []
    return {
        "book": book,
        "book_id": book_id,
        "edition_id": selected_edition_id,
        "edition": edition,
        "editions": editions,
        "edition_groups": _author_edition_groups(editions),
        "chapter_items": chapter_items,
        "draft_items": draft_items,
        "candidate_cards": candidate_cards,
        "profile_items": profile_items,
        "profile_manifest": profile_manifest,
        "selected_profile": selected_profile,
        "selected_node": selected_node,
        "active_left_node": selected_node,
        "active_main_mode": active_mode,
        "active_right_tab": active_right_tab,
        "state_tab": active_state_tab,
        "state_scope": active_state_scope,
        "state_tab_items": STATE_TAB_ITEMS,
        "selected_character_id": (
            character_id
            if story_game_state is None
            else story_game_state.get("selected_character_id")
        ),
        "mode_labels": MODE_LABELS,
        "right_tab_labels": RIGHT_TAB_LABELS,
        "selected_chapter": selected_chapter,
        "selected_chapter_id": (
            None if selected_chapter is None else str(selected_chapter["chapter_id"])
        ),
        "selected_draft": selected_draft,
        "chapter_context": _public_chapter_context(chapter_context),
        "selected_chapter_anchor": selected_anchor,
        "latest_chapter": latest_chapter,
        "book_status": str(book.get("readiness_status") or "UNKNOWN"),
        "book_status_label": _status_label(book.get("readiness_status") or "UNKNOWN"),
        "continuation_package": _continuation_package(selected_draft),
        "story_game_state": story_game_state,
        "chapter_world_state": story_game_state,
        "progression_workspace": (
            None
            if story_game_state is None
            else story_game_state.get("progression_workspace")
        ),
        "previous_chapter_world_state": previous_story_game_state,
        "author_control": author_control,
        "truth_lens": selected_lens.value,
        "truth_id": truth_id,
        "include_future_truths": include_future_truths,
        "truth_projection": truth_projection,
        "truth_knowledge": truth_knowledge,
        "reveal_agenda": reveal_agenda,
        "secret_board": secret_board,
        "open_questions": open_questions,
        "secret_candidates": secret_candidates,
        "data_ownership": {
            "source": "Book Library source/ and immutable chapters",
            "distill": "book_profil/ author-facing derived view",
            "runtime": "existing Runtime Baseline + Canon Projection; query only",
            "draft": "existing Edition writing/drafts and drafts table",
            "canon": "existing append-only events and Canon Projection",
        },
    }


__all__ = [
    "PROFILE_DIMENSIONS",
    "WORKBENCH_MODES",
    "WORKBENCH_RIGHT_TABS",
    "WORKBENCH_STATE_TABS",
    "build_workbench_context",
]
