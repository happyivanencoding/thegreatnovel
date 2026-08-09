"""Read-only chapter-aware Story Game State projections."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from novel_authoring.canon.projection import CanonProjection, projection_from_connection
from novel_authoring.db.database import Database
from novel_authoring.edition import EditionWorkflowError, edition_chapters
from novel_authoring.runtime_baseline.models import (
    BaselineCategory,
    RuntimeBaseline,
    RuntimeBaselineEntry,
)
from novel_authoring.storage.layout import BookLayout

_LAYER_LABELS = {
    "CANON": "正史",
    "SOURCE_BASELINE": "来源参考",
    "SOFT_REFERENCE": "软理解参考",
}


def _json_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if not value:
        return {}
    try:
        parsed = json.loads(str(value))
    except (TypeError, ValueError):
        return {}
    return dict(parsed) if isinstance(parsed, dict) else {}


def _workspace_root(connection: sqlite3.Connection, book_id: str) -> Path | None:
    row = connection.execute(
        "SELECT workspace_root FROM books WHERE book_id=?", (book_id,)
    ).fetchone()
    if row is None:
        return None
    return Path(str(row["workspace_root"])).expanduser().resolve()


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def _baseline_root(workspace_root: Path, book_id: str, edition_id: str) -> Path:
    if (workspace_root / "book.yaml").is_file():
        return (
            BookLayout(workspace_root.parent).for_book(book_id).edition(edition_id).analysis
            / "runtime_baseline"
        )
    return workspace_root / "editions" / edition_id / "analysis" / "runtime_baseline"


def _read_runtime_baseline(
    connection: sqlite3.Connection, book_id: str, edition_id: str
) -> RuntimeBaseline | None:
    workspace_root = _workspace_root(connection, book_id)
    if workspace_root is None:
        return None
    root = _baseline_root(workspace_root, book_id, edition_id)
    pointer = _read_json(root / "latest.json")
    if not isinstance(pointer, dict):
        return None
    raw_manifest = pointer.get("manifest")
    if not isinstance(raw_manifest, str) or not raw_manifest.strip():
        return None
    manifest_path = Path(raw_manifest).expanduser()
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    manifest_path = manifest_path.resolve()
    if not manifest_path.is_file():
        return None
    try:
        manifest = _read_json(manifest_path)
        if not isinstance(manifest, dict):
            return None
        model_manifest = RuntimeBaseline.model_validate(
            {"manifest": manifest, "entries": []}
        ).manifest
        entries: list[RuntimeBaselineEntry] = []
        version_root = manifest_path.parent
        filenames = {
            BaselineCategory.CHARACTER: "characters.json",
            BaselineCategory.CAPABILITY: "capabilities.json",
            BaselineCategory.ITEM: "items.json",
            BaselineCategory.EQUIPMENT: "equipment.json",
            BaselineCategory.RESOURCE: "resources.json",
            BaselineCategory.KNOWLEDGE: "knowledge.json",
            BaselineCategory.RULE: "rules.json",
            BaselineCategory.EXCEPTION: "exceptions.json",
            BaselineCategory.PROMISE: "promises.json",
        }
        for filename in filenames.values():
            payload = _read_json(version_root / filename)
            if not isinstance(payload, list):
                continue
            entries.extend(RuntimeBaselineEntry.model_validate(item) for item in payload)
        return RuntimeBaseline(manifest=model_manifest, entries=entries)
    except (TypeError, ValueError):
        return None


def _is_character(value: dict[str, Any]) -> bool:
    raw = " ".join(
        str(value.get(key) or "")
        for key in ("entity_type", "node_type", "type", "category", "character_type")
    ).lower()
    return any(
        token in raw
        for token in ("character", "person", "protagonist", "companion", "trader", "craftsman")
    )


def _is_faction(value: dict[str, Any]) -> bool:
    raw = " ".join(
        str(value.get(key) or "") for key in ("entity_type", "node_type", "type", "category")
    ).lower()
    return "faction" in raw or "组织" in raw or "势力" in raw


def _name(value: dict[str, Any], fallback: str) -> str:
    for key in ("name", "character_name", "entity_name", "title", "label", "item_name"):
        candidate = value.get(key)
        if candidate is not None and str(candidate).strip():
            return str(candidate)
    return fallback


def _owner_matches(value: dict[str, Any], character_id: str) -> bool:
    return any(
        str(value.get(key) or "") == character_id
        for key in (
            "owner_id",
            "character_id",
            "holder_id",
            "user_id",
            "carrier_id",
            "from_entity_id",
        )
    )


def _public_attributes(value: dict[str, Any]) -> list[dict[str, str]]:
    excluded = {
        "_event_id",
        "_event_seq",
        "_source_kind",
        "_source_id",
        "_edition_id",
        "name",
        "character_id",
        "entity_id",
        "resource_id",
        "capability_id",
        "relationship_id",
        "edge_id",
    }
    result: list[dict[str, str]] = []
    for key, raw in value.items():
        if str(key) in excluded or raw is None or isinstance(raw, (dict, list)):
            continue
        result.append({"label": str(key), "value": str(raw)})
    return result[:24]


def _record(
    record_id: str,
    value: dict[str, Any],
    *,
    layer: str,
    fallback_name: str,
    category: str,
) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "name": _name(value, fallback_name),
        "category": category,
        "layer": layer,
        "status": str(value.get("status") or ("CANON" if layer == "CANON" else layer)),
        "statement": str(
            value.get("statement")
            or value.get("description")
            or value.get("reason")
            or value.get("goal")
            or ""
        ),
        "attributes": _public_attributes(value),
        "raw": value,
    }


def _baseline_entries(
    baseline: RuntimeBaseline | None, category: BaselineCategory, character_id: str
) -> list[RuntimeBaselineEntry]:
    if baseline is None:
        return []
    result: list[RuntimeBaselineEntry] = []
    for entry in baseline.entries:
        if entry.category is not category:
            continue
        owner_id = entry.attributes.get("owner_id") or entry.attributes.get("character_id")
        if entry.subject_id == character_id or owner_id == character_id:
            result.append(entry)
    return result


def _chapter_rows(
    connection: sqlite3.Connection, book_id: str, edition_id: str
) -> list[dict[str, Any]]:
    try:
        return edition_chapters(connection, book_id, edition_id)
    except (EditionWorkflowError, KeyError, LookupError, sqlite3.Error, ValueError):
        rows = connection.execute(
            "SELECT * FROM chapters WHERE book_id=? ORDER BY ordinal, chapter_id", (book_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def _chapter_anchors(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapters: list[dict[str, Any]],
) -> dict[int, int]:
    anchors: dict[int, int] = {}
    for chapter in chapters:
        row = connection.execute(
            "SELECT MAX(event_end_seq) AS event_end_seq FROM canon_commits "
            "WHERE book_id=? AND edition_id=? AND chapter_id=?",
            (book_id, edition_id, str(chapter["chapter_id"])),
        ).fetchone()
        if row is not None and row["event_end_seq"] is not None:
            anchors[int(chapter["ordinal"])] = int(row["event_end_seq"])
    return anchors


def _soft_atlas(workspace_root: Path | None, book_id: str, edition_id: str) -> dict[str, Any]:
    if workspace_root is None:
        return {"available": False, "layer": "SOFT_REFERENCE", "graphs": {}}
    if (workspace_root / "book.yaml").is_file():
        atlas_root = (
            BookLayout(workspace_root.parent).for_book(book_id).edition(edition_id).analysis
            / "story_atlas"
            / "versions"
        )
    else:
        atlas_root = (
            workspace_root / "editions" / edition_id / "analysis" / "story_atlas" / "versions"
        )
    candidates = [path for path in atlas_root.iterdir()] if atlas_root.is_dir() else []
    candidates = [path for path in candidates if path.is_dir()]
    if not candidates:
        return {"available": False, "layer": "SOFT_REFERENCE", "graphs": {}}
    selected = max(candidates, key=lambda path: path.name)
    graphs: dict[str, Any] = {}
    for graph_type in ("characters", "factions", "resources_and_items", "plot_threads"):
        payload = _read_json(selected / "graphs" / f"{graph_type}.json")
        if not isinstance(payload, dict):
            continue
        graphs[graph_type] = {
            "graph_type": graph_type,
            "atlas_version": payload.get("atlas_version"),
            "nodes": payload.get("nodes", []),
            "edges": payload.get("edges", []),
            "layer": "SOFT_REFERENCE",
        }
    return {
        "available": bool(graphs),
        "layer": "SOFT_REFERENCE",
        "version": selected.name,
        "graphs": graphs,
        "warning": "这是 Story Atlas 的软理解参考，不等于当前角色的正史状态。",
    }


def _character_options(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    soft: dict[str, Any],
) -> list[dict[str, Any]]:
    options: dict[str, dict[str, Any]] = {}

    def add(record_id: str, name: str, layer: str, description: str = "") -> None:
        if record_id and record_id not in options:
            options[record_id] = {
                "character_id": record_id,
                "name": name,
                "layer": layer,
                "layer_label": _LAYER_LABELS.get(layer, "参考资料"),
                "description": description,
                "is_selectable": True,
            }

    for record_id, value in projection.character_states.items():
        payload = dict(value)
        add(
            str(payload.get("character_id") or record_id),
            _name(payload, str(payload.get("character_id") or record_id)),
            "CANON",
        )
    for record_id, value in projection.entities.items():
        payload = dict(value)
        if _is_character(payload):
            add(
                str(record_id),
                _name(payload, str(record_id)),
                "CANON",
                str(payload.get("description") or ""),
            )
    if baseline is not None:
        for entry in baseline.entries:
            if entry.category is BaselineCategory.CHARACTER:
                add(
                    str(entry.subject_id or entry.entry_id),
                    entry.name,
                    "SOURCE_BASELINE",
                    entry.statement,
                )
    for node in soft.get("graphs", {}).get("characters", {}).get("nodes", []):
        if isinstance(node, dict):
            add(
                str(node.get("node_id") or ""),
                str(node.get("name") or node.get("node_id") or ""),
                "SOFT_REFERENCE",
                str(node.get("description") or ""),
            )
    return list(options.values())


def _selected_character(
    options: list[dict[str, Any]], character_id: str | None
) -> dict[str, Any] | None:
    if character_id:
        exact = next((item for item in options if item["character_id"] == character_id), None)
        if exact is not None:
            return exact
    return options[0] if options else None


def _character_state(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    selected: dict[str, Any] | None,
) -> dict[str, Any]:
    if selected is None:
        return {
            "available": False,
            "status": "EMPTY",
            "status_label": "暂无可选人物",
            "message": "当前没有可读取的人物记录；系统不会凭空创建人物状态。",
        }
    character_id = str(selected["character_id"])
    state = next(
        (
            dict(value)
            for value in projection.character_states.values()
            if str(value.get("character_id") or "") == character_id
            or str(value.get("entity_id") or "") == character_id
        ),
        None,
    )
    entity = dict(projection.entities.get(character_id, {}))
    baseline_entry = next(
        (
            entry
            for entry in (baseline.entries if baseline is not None else [])
            if entry.category is BaselineCategory.CHARACTER
            and str(entry.subject_id or entry.entry_id) == character_id
        ),
        None,
    )
    if state is None:
        return {
            "available": False,
            "status": selected["layer"],
            "status_label": "只有参考资料",
            "character_id": character_id,
            "name": selected["name"],
            "description": selected.get("description")
            or (baseline_entry.statement if baseline_entry else ""),
            "attributes": [],
            "message": (
                "当前角色还没有逐章正史状态；下面的资料只能作为参考，"
                "不能当作当前背包或数值。"
            ),
        }
    return {
        "available": True,
        "status": "CANON",
        "status_label": "正史状态",
        "character_id": character_id,
        "name": selected["name"],
        "description": str(entity.get("description") or ""),
        "attributes": _public_attributes(state),
        "message": "以下内容来自选定章节时间点之前已经提交的正史事件。",
        "raw": state,
    }


def _projection_items(
    projection: CanonProjection,
    selected: dict[str, Any] | None,
    state: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if selected is None:
        return [], []
    character_id = str(selected["character_id"])
    inventory: list[dict[str, Any]] = []
    equipment: list[dict[str, Any]] = []
    for record_id, value in projection.resources.items():
        payload = dict(value)
        if not _owner_matches(payload, character_id):
            continue
        record = _record(
            str(record_id),
            payload,
            layer="CANON",
            fallback_name=str(record_id),
            category="resource",
        )
        is_equipment = any(
            str(payload.get(key) or "").lower() in {"equipment", "weapon", "armor", "vehicle"}
            for key in ("resource_type", "category", "item_type", "type")
        ) or any(key in payload for key in ("slot", "equipment_slot"))
        (equipment if is_equipment else inventory).append(record)
    for key in ("resources", "inventory", "items"):
        raw = state.get(key)
        if not isinstance(raw, dict):
            continue
        for item_id, item_value in raw.items():
            payload = item_value if isinstance(item_value, dict) else {"quantity": item_value}
            inventory.append(
                _record(
                    f"state:{key}:{item_id}",
                    {"name": str(item_id), **payload},
                    layer="CANON",
                    fallback_name=str(item_id),
                    category="resource",
                )
            )
    raw_equipment = state.get("equipment")
    if isinstance(raw_equipment, dict):
        for item_id, item_value in raw_equipment.items():
            payload = item_value if isinstance(item_value, dict) else {"value": item_value}
            equipment.append(
                _record(
                    f"state:equipment:{item_id}",
                    {"name": str(item_id), **payload},
                    layer="CANON",
                    fallback_name=str(item_id),
                    category="equipment",
                )
            )
    return inventory, equipment


def _abilities(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    selected: dict[str, Any] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if selected is None:
        return [], []
    character_id = str(selected["character_id"])
    canon = [
        _record(
            str(record_id),
            dict(value),
            layer="CANON",
            fallback_name=str(record_id),
            category="capability",
        )
        for record_id, value in projection.capabilities.items()
        if _owner_matches(dict(value), character_id)
    ]
    source: list[dict[str, Any]] = []
    for entry in _baseline_entries(baseline, BaselineCategory.CAPABILITY, character_id):
        source.append(
            {
                "record_id": f"baseline:{entry.entry_id}",
                "name": entry.name,
                "category": "capability",
                "layer": "SOURCE_BASELINE",
                "status": entry.status.value,
                "status_label": "来源参考",
                "statement": entry.statement,
                "attributes": [
                    {"label": key, "value": value} for key, value in entry.attributes.items()
                ],
            }
        )
    return canon, source


def _knowledge(
    projection: CanonProjection, selected: dict[str, Any] | None
) -> list[dict[str, Any]]:
    if selected is None:
        return []
    character_id = str(selected["character_id"])
    return [
        _record(
            str(record_id),
            dict(value),
            layer="CANON",
            fallback_name=str(record_id),
            category="knowledge",
        )
        for record_id, value in projection.knowledge.items()
        if str(value.get("character_id") or value.get("from_entity_id") or "") == character_id
    ]


def _relationships(
    projection: CanonProjection, selected: dict[str, Any] | None
) -> list[dict[str, Any]]:
    if selected is None:
        return []
    character_id = str(selected["character_id"])
    result: list[dict[str, Any]] = []
    for record_id, value in projection.relationships.items():
        payload = dict(value)
        if character_id not in {
            str(payload.get("from_entity_id") or ""),
            str(payload.get("to_entity_id") or ""),
            str(payload.get("character_id") or ""),
        }:
            continue
        result.append(
            _record(
                str(record_id),
                payload,
                layer="CANON",
                fallback_name=str(record_id),
                category="relationship",
            )
        )
    return result


def _soft_relationships(
    soft: dict[str, Any], selected: dict[str, Any] | None
) -> list[dict[str, Any]]:
    graph = soft.get("graphs", {}).get("characters", {})
    nodes = {
        str(node.get("node_id")): str(node.get("name") or node.get("node_id"))
        for node in graph.get("nodes", [])
        if isinstance(node, dict)
    }
    selected_id = str(selected["character_id"]) if selected else ""
    result: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict) or selected_id not in {
            str(edge.get("from_id") or ""),
            str(edge.get("to_id") or ""),
        }:
            continue
        result.append(
            {
                "record_id": str(edge.get("edge_id") or ""),
                "from_name": nodes.get(
                    str(edge.get("from_id") or ""), str(edge.get("from_id") or "")
                ),
                "to_name": nodes.get(str(edge.get("to_id") or ""), str(edge.get("to_id") or "")),
                "label": str(edge.get("label") or "关系参考"),
                "layer": "SOFT_REFERENCE",
                "status": str(edge.get("information_status") or "UNKNOWN"),
            }
        )
    return result


def build_story_game_state(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_id: str | None = None,
    character_id: str | None = None,
) -> dict[str, Any]:
    """Build a historical, chapter-aware game-like state without persisting it."""

    with database.connect() as connection:
        chapters = _chapter_rows(connection, book_id, edition_id)
        selected_chapter = next(
            (item for item in chapters if chapter_id and str(item["chapter_id"]) == chapter_id),
            chapters[-1] if chapters else None,
        )
        anchors = _chapter_anchors(connection, book_id, edition_id, chapters)
        ordinal = int(selected_chapter["ordinal"]) if selected_chapter is not None else None
        after_event_seq = anchors.get(ordinal) if ordinal is not None else None
        before_event_seq = (
            max(
                (value for key, value in anchors.items() if ordinal is not None and key < ordinal),
                default=0,
            )
            if ordinal is not None
            else 0
        )
        projection = CanonProjection(book_id=book_id, edition_id=edition_id)
        availability = "NO_CANON_EVENT_ANCHOR"
        if after_event_seq is not None:
            projection = projection_from_connection(
                connection,
                book_id,
                edition_id=edition_id,
                through_event_seq=after_event_seq,
            )
            availability = "CANON_EVENT_PROJECTION"
        baseline = _read_runtime_baseline(connection, book_id, edition_id)
        workspace_root = _workspace_root(connection, book_id)
        soft = _soft_atlas(workspace_root, book_id, edition_id)

    options = _character_options(projection, baseline, soft)
    selected = _selected_character(options, character_id)
    selected_state = _character_state(projection, baseline, selected)
    raw_state_value = selected_state.get("raw")
    raw_state: dict[str, Any] = raw_state_value if isinstance(raw_state_value, dict) else {}
    inventory, equipment = _projection_items(projection, selected, raw_state)
    canon_abilities, source_abilities = _abilities(projection, baseline, selected)
    knowledge = _knowledge(projection, selected)
    relationships = _relationships(projection, selected)
    soft_relationships = _soft_relationships(soft, selected)
    factions = [
        {
            "node_id": node.get("node_id"),
            "name": node.get("name"),
            "description": node.get("description"),
            "layer": "SOFT_REFERENCE",
        }
        for node in soft.get("graphs", {}).get("factions", {}).get("nodes", [])
        if isinstance(node, dict)
    ]
    return {
        "availability": availability,
        "availability_label": "已建立正史时间点"
        if availability == "CANON_EVENT_PROJECTION"
        else "尚无正史时间点",
        "message": (
            "当前内容按选定章节的正史事件投影。任务和作者意图在下方独立展示。"
            if availability == "CANON_EVENT_PROJECTION"
            else "当前章节没有可追溯的正史事件锚点；系统不会拿最新状态冒充本章状态。"
        ),
        "chapter": (
            {
                "chapter_id": str(selected_chapter["chapter_id"]),
                "ordinal": ordinal,
                "title": str(selected_chapter["title"]),
            }
            if selected_chapter is not None
            else None
        ),
        "timepoint": {
            "before_event_seq": before_event_seq or None,
            "after_event_seq": after_event_seq,
            "historical": after_event_seq is not None,
        },
        "characters": options,
        "selected_character_id": selected["character_id"] if selected else None,
        "character": selected_state,
        "inventory": inventory,
        "equipment": equipment,
        "abilities": canon_abilities,
        "source_ability_references": source_abilities,
        "knowledge": knowledge,
        "relationships": relationships,
        "soft_relationships": soft_relationships,
        "factions": factions,
        "soft_reference": soft,
        "safety": {
            "canon_mutation_allowed": False,
            "author_command_required": True,
            "message": "状态面板是投影；拖拽和编辑只提交 Author Command，不直接改正史。",
        },
        "technical": {
            "edition_id": edition_id,
            "through_event_seq": after_event_seq,
            "projection_record_counts": {
                "character_states": len(projection.character_states),
                "resources": len(projection.resources),
                "capabilities": len(projection.capabilities),
                "knowledge": len(projection.knowledge),
                "relationships": len(projection.relationships),
            },
        },
    }


__all__ = ["build_story_game_state"]
