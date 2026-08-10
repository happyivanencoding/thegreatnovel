"""Read-only chapter-aware Story Game State projections."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from novel_authoring.author_control.source_state import build_source_state_projection
from novel_authoring.canon.projection import CanonProjection, projection_from_connection
from novel_authoring.db.database import Database
from novel_authoring.edition import EditionWorkflowError, edition_chapters
from novel_authoring.runtime_baseline.models import (
    BaselineCategory,
    BaselineStatus,
    RuntimeBaseline,
    RuntimeBaselineEntry,
)
from novel_authoring.storage.layout import BookLayout

_LAYER_LABELS = {
    "CANON": "正史已确认",
    "SOURCE_VERIFIED": "✓ 原文已确认",
    "SOURCE_PARTIAL": "原文有线索",
    "PROVISIONAL": "当前草稿",
    "AUTHOR_INTENT": "作者目标",
    "SOFT_REFERENCE": "小说画像参考",
    "UNKNOWN": "尚未知",
    "SOURCE_BASELINE": "✓ 原文已确认",
}

_KNOWLEDGE_STATES = (
    "KNOWN",
    "SEEN",
    "HEARD",
    "SUSPECTED",
    "MISUNDERSTOOD",
    "UNKNOWN",
)

_BASELINE_MUTABLE_KEYS = {
    "owner_id",
    "holder_id",
    "character_id",
    "quantity",
    "equipped",
    "slot",
    "equipment_slot",
    "location",
    "location_id",
    "status",
    "current",
    "availability",
    "injury",
    "relationship",
    "target",
    "faction_state",
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
        "layer_label": _LAYER_LABELS.get(layer, layer),
        "status": str(value.get("status") or ("CANON" if layer == "CANON" else layer)),
        "status_label": _LAYER_LABELS.get(
            str(value.get("status") or ("CANON" if layer == "CANON" else layer)),
            _LAYER_LABELS.get(layer, layer),
        ),
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


def _baseline_evidence_ordinals(
    entry: RuntimeBaselineEntry,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
) -> list[int]:
    """Return only evidence that is not from a future chapter."""

    values = sorted(
        {
            chapter_ordinals[str(evidence.chapter_id)]
            for evidence in entry.evidence
            if evidence.chapter_id and str(evidence.chapter_id) in chapter_ordinals
        }
    )
    if selected_ordinal is None:
        return values
    return [value for value in values if value <= selected_ordinal]


def _baseline_visible(
    entry: RuntimeBaselineEntry,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
) -> bool:
    if entry.status is BaselineStatus.UNKNOWN:
        return False
    return bool(_baseline_evidence_ordinals(entry, chapter_ordinals, selected_ordinal))


def _baseline_record(
    entry: RuntimeBaselineEntry,
    *,
    category: str,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
) -> dict[str, Any]:
    visible_evidence = [
        evidence
        for evidence in entry.evidence
        if evidence.chapter_id
        and str(evidence.chapter_id) in chapter_ordinals
        and (
            selected_ordinal is None
            or chapter_ordinals[str(evidence.chapter_id)] <= selected_ordinal
        )
    ]
    layer = entry.status.value
    # Runtime Baseline is a boundary snapshot.  Its mutable fields are not a
    # historical ledger and must not masquerade as chapter-N current state.
    safe_attributes = [
        {"label": str(key), "value": str(value)}
        for key, value in entry.attributes.items()
        if str(key) not in _BASELINE_MUTABLE_KEYS
    ]
    return {
        "record_id": f"baseline:{entry.entry_id}",
        "name": entry.name,
        "category": category,
        "layer": layer,
        "layer_label": _LAYER_LABELS[layer],
        "status": layer,
        "status_label": _LAYER_LABELS[layer],
        "statement": entry.statement,
        "description": entry.statement,
        "owner_id": entry.attributes.get("owner_id") or entry.attributes.get("character_id"),
        "current_holder_id": entry.attributes.get("owner_id")
        or entry.attributes.get("character_id"),
        "quantity": entry.attributes.get("quantity"),
        "equipped": entry.attributes.get("equipped", False),
        "slot": entry.attributes.get("slot") or entry.attributes.get("equipment_slot"),
        "use": entry.attributes.get("use") or entry.attributes.get("usage"),
        "constraints": entry.attributes.get("constraints"),
        "attributes": safe_attributes,
        "source": "Runtime Baseline",
        "baseline_entry_id": entry.entry_id,
        "subject_id": entry.subject_id,
        "source_span_ids": [
            span_id
            for evidence in visible_evidence
            for span_id in evidence.source_span_ids
        ],
        "evidence": [evidence.model_dump(mode="json") for evidence in visible_evidence],
        "last_confirmed": max(
            (chapter_ordinals[str(evidence.chapter_id)] for evidence in visible_evidence),
            default=None,
        ),
        "first_acquired_chapter_ordinal": min(
            (chapter_ordinals[str(evidence.chapter_id)] for evidence in visible_evidence),
            default=None,
        ),
        "recent_confirmed_chapter_ordinal": max(
            (chapter_ordinals[str(evidence.chapter_id)] for evidence in visible_evidence),
            default=None,
        ),
        "mutable_attributes_suppressed": True,
        "verification_note": (
            "当前状态只采用本书原文的 SOURCE_VERIFIED 证据。"
            if layer == "SOURCE_VERIFIED"
            else "原文有线索，但尚未达到可操作的 SOURCE_VERIFIED。"
        ),
    }


def _baseline_entries_at_chapter(
    baseline: RuntimeBaseline | None,
    category: BaselineCategory,
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    character_id: str | None = None,
    include_generic: bool = False,
) -> list[tuple[RuntimeBaselineEntry, dict[str, Any]]]:
    if baseline is None:
        return []
    result: list[tuple[RuntimeBaselineEntry, dict[str, Any]]] = []
    for entry in baseline.entries:
        if entry.category is not category or not _baseline_visible(
            entry, chapter_ordinals, selected_ordinal
        ):
            continue
        owner_id = entry.attributes.get("owner_id") or entry.attributes.get("character_id")
        if (
            character_id
            and not include_generic
            and entry.subject_id != character_id
            and owner_id != character_id
        ):
            continue
        result.append(
            (
                entry,
                _baseline_record(
                    entry,
                    category=category.value,
                    chapter_ordinals=chapter_ordinals,
                    selected_ordinal=selected_ordinal,
                ),
            )
        )
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
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    source_projection: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    options: dict[str, dict[str, Any]] = {}

    def add(record_id: str, name: str, layer: str, description: str = "") -> None:
        if record_id and record_id not in options:
            options[record_id] = {
                "character_id": record_id,
                "name": name,
                "layer": layer,
                "layer_label": _LAYER_LABELS.get(layer, "参考资料"),
                "status_label": _LAYER_LABELS.get(layer, layer),
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
            if entry.category is BaselineCategory.CHARACTER and _baseline_visible(
                entry, chapter_ordinals, selected_ordinal
            ):
                add(
                    str(entry.subject_id or entry.entry_id),
                    entry.name,
                    entry.status.value,
                    entry.statement,
                )
    if isinstance(source_projection, dict):
        source_records = source_projection.get("records", {})
        if isinstance(source_records, dict):
            for category in (
                "CHARACTER_STATE",
                "ITEM",
                "EQUIPMENT",
                "RESOURCE",
                "CAPABILITY",
                "KNOWLEDGE",
                "RELATIONSHIP",
            ):
                for record in source_records.get(category, []):
                    if not isinstance(record, dict):
                        continue
                    raw_value = record.get("raw")
                    raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
                    candidates = (
                        [record.get("subject_id")]
                        if category in {"CHARACTER_STATE", "KNOWLEDGE"}
                        else [
                            record.get("owner_id"),
                            raw.get("owner_id"),
                            record.get("subject_id"),
                        ]
                    )
                    if category == "RELATIONSHIP":
                        candidates.extend(
                            [raw.get("from_entity_id"), raw.get("to_entity_id")]
                        )
                    for candidate in candidates:
                        character = str(candidate or "")
                        if character:
                            add(
                                character,
                                str(raw.get("character_name") or character),
                                "SOURCE_VERIFIED",
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
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
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
            and _baseline_visible(entry, chapter_ordinals, selected_ordinal)
        ),
        None,
    )
    if state is None:
        if baseline_entry is not None:
            source = _baseline_record(
                baseline_entry,
                category="character",
                chapter_ordinals=chapter_ordinals,
                selected_ordinal=selected_ordinal,
            )
            return {
                "available": True,
                "status": source["status"],
                "status_label": source["status_label"],
                "layer": source["layer"],
                "character_id": character_id,
                "name": selected["name"],
                "description": selected.get("description") or baseline_entry.statement,
                "attributes": source["attributes"],
                "source": "Runtime Baseline",
                "evidence": source["evidence"],
                "message": (
                    "这是截至所选章节、由本书原文确认的角色状态；"
                    "逐章 Canon 状态尚未建立，未确认字段保持未知。"
                ),
            }
        return {
            "available": False,
            "status": selected["layer"],
            "status_label": _LAYER_LABELS.get(selected["layer"], "尚未知"),
            "character_id": character_id,
            "name": selected["name"],
            "description": selected.get("description")
            or (baseline_entry.statement if baseline_entry else ""),
            "attributes": [],
            "message": (
                "当前角色还没有可回指所选章节的状态证据；"
                "软理解参考不能当作当前背包或数值。"
            ),
        }
    return {
        "available": True,
        "status": "CANON",
        "status_label": _LAYER_LABELS["CANON"],
        "layer": "CANON",
        "character_id": character_id,
        "name": selected["name"],
        "description": str(entity.get("description") or ""),
        "attributes": _public_attributes(state),
        "message": "以下内容来自选定章节时间点之前已经提交的正史事件。",
        "raw": state,
    }


def _source_records_for_character(
    source_projection: dict[str, Any],
    categories: set[str],
    character_id: str,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    records = source_projection.get("records", {})
    if not isinstance(records, dict):
        return result
    for category in categories:
        for record in records.get(category, []):
            if not isinstance(record, dict):
                continue
            raw_value = record.get("raw")
            raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
            owner_id = str(
                record.get("owner_id")
                or raw.get("owner_id")
                or raw.get("character_id")
                or ""
            )
            if (
                str(record.get("subject_id") or "") not in {"", character_id}
                and owner_id != character_id
            ):
                continue
            result.append(dict(record))
    return result


def _projection_items(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    selected: dict[str, Any] | None,
    state: dict[str, Any],
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    source_projection: dict[str, Any],
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
    if baseline is not None or source_projection.get("available"):
        source_items = _source_records_for_character(
            source_projection, {"ITEM", "RESOURCE"}, character_id
        )
        source_equipment = _source_records_for_character(
            source_projection, {"EQUIPMENT"}, character_id
        )
        for record in [*source_items, *source_equipment]:
            if record.get("status") != "SOURCE_VERIFIED":
                continue
            target = (
                equipment
                if record.get("category") == "equipment" or record.get("equipped")
                else inventory
            )
            if not any(item.get("record_id") == record.get("record_id") for item in target):
                target.append(record)
        baseline_boundary_reached = baseline is not None and (
            selected_ordinal is None
            or selected_ordinal >= baseline.manifest.boundary_chapter
        )
        if baseline_boundary_reached:
            for entry, record in [
                *_baseline_entries_at_chapter(
                    baseline,
                    BaselineCategory.ITEM,
                    chapter_ordinals=chapter_ordinals,
                    selected_ordinal=selected_ordinal,
                    character_id=character_id,
                ),
                *_baseline_entries_at_chapter(
                    baseline,
                    BaselineCategory.RESOURCE,
                    chapter_ordinals=chapter_ordinals,
                    selected_ordinal=selected_ordinal,
                    character_id=character_id,
                ),
            ]:
                if entry.status is BaselineStatus.SOURCE_VERIFIED:
                    inventory.append(record)
            for entry, record in _baseline_entries_at_chapter(
                baseline,
                BaselineCategory.EQUIPMENT,
                chapter_ordinals=chapter_ordinals,
                selected_ordinal=selected_ordinal,
                character_id=character_id,
            ):
                if entry.status is BaselineStatus.SOURCE_VERIFIED:
                    equipment.append(record)
    return inventory, equipment


def _abilities(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    selected: dict[str, Any] | None,
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    source_projection: dict[str, Any],
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
    baseline_boundary_reached = baseline is not None and (
        selected_ordinal is None
        or selected_ordinal >= baseline.manifest.boundary_chapter
    )
    if baseline_boundary_reached:
        for entry, record in _baseline_entries_at_chapter(
            baseline,
            BaselineCategory.CAPABILITY,
            chapter_ordinals=chapter_ordinals,
            selected_ordinal=selected_ordinal,
            character_id=character_id,
        ):
            source.append(record)
            if entry.status is BaselineStatus.SOURCE_VERIFIED:
                canon.append(record)
    source.extend(
        record
        for record in _source_records_for_character(
            source_projection, {"CAPABILITY"}, character_id
        )
        if record.get("status") == "SOURCE_VERIFIED"
    )
    return canon, source


def _knowledge(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    selected: dict[str, Any] | None,
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    source_projection: dict[str, Any],
) -> list[dict[str, Any]]:
    if selected is None:
        return []
    character_id = str(selected["character_id"])
    result = [
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
    for record in _source_records_for_character(source_projection, {"KNOWLEDGE"}, character_id):
        if record.get("status") == "SOURCE_VERIFIED":
            result.append(record)
    baseline_boundary_reached = baseline is not None and (
        selected_ordinal is None
        or selected_ordinal >= baseline.manifest.boundary_chapter
    )
    if baseline_boundary_reached:
        for entry, record in _baseline_entries_at_chapter(
            baseline,
            BaselineCategory.KNOWLEDGE,
            chapter_ordinals=chapter_ordinals,
            selected_ordinal=selected_ordinal,
            character_id=None,
            include_generic=True,
        ):
            if entry.status is not BaselineStatus.SOURCE_VERIFIED:
                continue
            result.append(
                {
                    **record,
                    "knowledge_state": "UNKNOWN",
                    "knowledge_state_label": "尚未确认谁知道",
                    "who_knows": [],
                    "visibility_status": "UNKNOWN",
                }
            )
    return result


def _knowledge_matrix(
    projection: CanonProjection,
    source_projection: dict[str, Any],
    characters: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build an auditable knower × topic matrix without filling UNKNOWN by inference."""

    topics: dict[str, dict[str, Any]] = {}
    edges: dict[tuple[str, str], dict[str, Any]] = {}

    def add_edge(raw: dict[str, Any], *, layer: str, record_id: str) -> None:
        knower_id = str(
            raw.get("knower_id")
            or raw.get("character_id")
            or raw.get("from_entity_id")
            or raw.get("subject_id")
            or ""
        )
        topic_id = str(
            raw.get("topic_id")
            or raw.get("object_id")
            or raw.get("knowledge_id")
            or record_id
        )
        if not knower_id or not topic_id:
            return
        topic_name = str(
            raw.get("topic_name") or raw.get("name") or raw.get("topic") or topic_id
        )
        topics.setdefault(
            topic_id,
            {"topic_id": topic_id, "name": topic_name, "layer": layer},
        )
        state = str(
            raw.get("knowledge_state")
            or raw.get("visibility_state")
            or raw.get("state")
            or "KNOWN"
        ).upper()
        if state not in _KNOWLEDGE_STATES:
            state = "UNKNOWN"
        edges[(knower_id, topic_id)] = {
            "knower_id": knower_id,
            "topic_id": topic_id,
            "topic_name": topic_name,
            "state": state,
            "state_label": state,
            "layer": layer,
            "record_id": record_id,
            "evidence_chapter_ordinal": raw.get("chapter_ordinal"),
            "source_span_ids": list(raw.get("source_span_ids") or []),
            "source": raw.get("source") or layer,
        }

    for record_id, value in projection.knowledge.items():
        add_edge(dict(value), layer="CANON", record_id=str(record_id))
    source_records = source_projection.get("records", {})
    if isinstance(source_records, dict):
        for record in source_records.get("KNOWLEDGE", []):
            if not isinstance(record, dict) or record.get("status") != "SOURCE_VERIFIED":
                continue
            raw_value = record.get("raw")
            raw = raw_value if isinstance(raw_value, dict) else {}
            add_edge(
                {**raw, **record},
                layer="SOURCE_VERIFIED",
                record_id=str(
                    record.get("record_id")
                    or record.get("state_key")
                    or "source-knowledge"
                ),
            )
    names = {
        str(item.get("character_id")): str(item.get("name") or item.get("character_id"))
        for item in characters
        if item.get("character_id")
    }
    matrix: list[dict[str, Any]] = []
    for character_id, character_name in names.items():
        for topic_id, topic in topics.items():
            cell = edges.get((character_id, topic_id))
            matrix.append(
                {
                    "knower_id": character_id,
                    "knower_name": character_name,
                    "topic_id": topic_id,
                    "topic_name": topic["name"],
                    "state": "UNKNOWN" if cell is None else cell["state"],
                    "state_label": "UNKNOWN" if cell is None else cell["state_label"],
                    "layer": "UNKNOWN" if cell is None else cell["layer"],
                    "evidence_chapter_ordinal": None if cell is None else cell[
                        "evidence_chapter_ordinal"
                    ],
                    "source_span_ids": [] if cell is None else cell["source_span_ids"],
                    "record_id": None if cell is None else cell["record_id"],
                }
            )
    return {
        "topics": list(topics.values()),
        "edges": list(edges.values()),
        "matrix": matrix,
        "states": list(_KNOWLEDGE_STATES),
    }


def _relationships(
    projection: CanonProjection,
    selected: dict[str, Any] | None,
    *,
    source_projection: dict[str, Any],
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
    source_records = source_projection.get("records")
    if not isinstance(source_records, dict):
        return result
    for record in source_records.get("RELATIONSHIP", []):
        if not isinstance(record, dict) or record.get("status") != "SOURCE_VERIFIED":
            continue
        raw_value = record.get("raw")
        raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
        endpoints = {
            str(record.get("subject_id") or ""),
            str(raw.get("from_entity_id") or ""),
            str(raw.get("to_entity_id") or ""),
        }
        if character_id in endpoints:
            result.append(dict(record))
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


def _relationship_details(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    for record in records:
        raw_value = record.get("raw")
        raw = raw_value if isinstance(raw_value, dict) else {}
        details.append(
            {
                **record,
                "from_entity_id": record.get("from_entity_id") or raw.get("from_entity_id"),
                "to_entity_id": record.get("to_entity_id") or raw.get("to_entity_id"),
                "first_confirmed_chapter_ordinal": record.get(
                    "first_confirmed_chapter_ordinal", record.get("chapter_ordinal")
                ),
                "recent_confirmed_chapter_ordinal": record.get(
                    "recent_confirmed_chapter_ordinal", record.get("chapter_ordinal")
                ),
                "dimensions": {
                    name: str(raw.get(name) or record.get(name) or "UNKNOWN").upper()
                    for name in (
                        "trust",
                        "dependence",
                        "conflict",
                        "intimacy",
                        "power",
                        "fear",
                        "obligation",
                    )
                },
                "current_layer": record.get("layer") or "UNKNOWN",
                "author_intent_separate": True,
            }
        )
    return details


def _faction_details(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for record in records:
        raw_value = record.get("raw")
        raw = raw_value if isinstance(raw_value, dict) else {}
        result.append(
            {
                **record,
                "state": raw.get("state") or raw.get("status") or record.get("status"),
                "goal": raw.get("goal") or raw.get("objective") or "UNKNOWN",
                "key_people": raw.get("key_people") or raw.get("members") or [],
                "controlled_locations": raw.get("controlled_locations") or [],
                "resources": raw.get("resources") or [],
                "attitude": raw.get("attitude") or "UNKNOWN",
                "action": raw.get("action") or "UNKNOWN",
                "known": raw.get("known") or [],
                "unknown": raw.get("unknown") or [],
                "current_layer": record.get("layer") or "UNKNOWN",
                "author_plan_separate": True,
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
        chapter_ordinals = {
            str(item["chapter_id"]): int(item["ordinal"]) for item in chapters
        }
        ordinal = int(selected_chapter["ordinal"]) if selected_chapter is not None else None
        anchors = _chapter_anchors(connection, book_id, edition_id, chapters)
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
        source_projection = build_source_state_projection(
            connection,
            book_id,
            edition_id,
            chapter_id=(
                None if selected_chapter is None else str(selected_chapter["chapter_id"])
            ),
            chapter_ordinal=ordinal,
        )
        workspace_root = _workspace_root(connection, book_id)
        soft = _soft_atlas(workspace_root, book_id, edition_id)

    options = _character_options(
        projection,
        baseline,
        soft,
        chapter_ordinals=chapter_ordinals,
        selected_ordinal=ordinal,
        source_projection=source_projection,
    )
    selected = _selected_character(options, character_id)
    selected_state = _character_state(
        projection,
        baseline,
        selected,
        chapter_ordinals=chapter_ordinals,
        selected_ordinal=ordinal,
    )
    raw_state_value = selected_state.get("raw")
    raw_state: dict[str, Any] = raw_state_value if isinstance(raw_state_value, dict) else {}
    inventory, equipment = _projection_items(
        projection,
        baseline,
        selected,
        raw_state,
        chapter_ordinals=chapter_ordinals,
        selected_ordinal=ordinal,
        source_projection=source_projection,
    )
    canon_abilities, source_abilities = _abilities(
        projection,
        baseline,
        selected,
        chapter_ordinals=chapter_ordinals,
        selected_ordinal=ordinal,
        source_projection=source_projection,
    )
    knowledge = _knowledge(
        projection,
        baseline,
        selected,
        chapter_ordinals=chapter_ordinals,
        selected_ordinal=ordinal,
        source_projection=source_projection,
    )
    knowledge_matrix = _knowledge_matrix(projection, source_projection, options)
    for item in knowledge:
        topic_id = str(
            item.get("object_id")
            or item.get("topic_id")
            or item.get("state_key")
            or item.get("name")
        )
        item["who_knows"] = [
            dict(edge)
            for edge in knowledge_matrix["edges"]
            if str(edge.get("topic_id")) == topic_id
        ]
    relationships = _relationships(
        projection, selected, source_projection=source_projection
    )
    relationship_inspector = _relationship_details(relationships)
    soft_relationships = _soft_relationships(soft, selected)
    baseline_visible = [
        entry
        for entry in (baseline.entries if baseline is not None else [])
        if _baseline_visible(entry, chapter_ordinals, ordinal)
    ]
    unknown_abilities = [
        _baseline_record(
            entry,
            category="capability",
            chapter_ordinals=chapter_ordinals,
            selected_ordinal=ordinal,
        )
        for entry in (baseline.entries if baseline is not None else [])
        if entry.category is BaselineCategory.CAPABILITY
        and entry.status is BaselineStatus.UNKNOWN
        and baseline is not None
        and (ordinal is None or ordinal >= baseline.manifest.boundary_chapter)
        and selected is not None
        and (
            str(entry.subject_id or "") == str(selected["character_id"])
            or entry.attributes.get("character_id") == str(selected["character_id"])
        )
    ]
    source_factions = [
        dict(record)
        for record in source_projection.get("records", {}).get("FACTION", [])
        if isinstance(record, dict) and record.get("status") == "SOURCE_VERIFIED"
    ]
    factions = [
        {
            "node_id": node.get("node_id"),
            "name": node.get("name"),
            "description": node.get("description"),
            "layer": "SOFT_REFERENCE",
            "layer_label": _LAYER_LABELS["SOFT_REFERENCE"],
        }
        for node in soft.get("graphs", {}).get("factions", {}).get("nodes", [])
        if isinstance(node, dict)
    ]
    factions = [*source_factions, *factions]
    faction_inspector = _faction_details(factions)
    source_ready = bool(source_projection.get("available") or baseline_visible)
    if after_event_seq is not None:
        availability = "CANON_EVENT_PROJECTION"
    elif source_ready:
        availability = "SOURCE_CHAPTER_STATE_PROJECTION"
    else:
        availability = "SOURCE_STATE_HYDRATION_REQUIRED"
    availability_labels = {
        "CANON_EVENT_PROJECTION": "正史已确认",
        "SOURCE_CHAPTER_STATE_PROJECTION": "原文状态（部分）",
        "SOURCE_STATE_HYDRATION_REQUIRED": "正在补齐章节状态",
    }
    messages = {
        "CANON_EVENT_PROJECTION": (
            "当前内容按选定章节的正史事件投影；原文状态和作者规划仍以独立层展示。"
        ),
        "SOURCE_CHAPTER_STATE_PROJECTION": (
            "当前状态来自本书原文证据和 Source State 投影；尚未建立逐章正史状态的字段保持未知，"
            "不会把后续章节资料倒灌到本章。"
        ),
        "SOURCE_STATE_HYDRATION_REQUIRED": (
            "正在补齐这一章的故事状态；当前没有可回指本章的原文状态证据，"
            "系统不会拿最新章节状态冒充本章状态。"
        ),
    }
    return {
        "availability": availability,
        "availability_label": availability_labels[availability],
        "message": messages[availability],
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
            "source_projection_available": source_ready,
            "source_projection_status": source_projection.get("projection_status"),
        },
        "characters": options,
        "selected_character_id": selected["character_id"] if selected else None,
        "character": selected_state,
        "inventory": inventory,
        "equipment": equipment,
        "abilities": canon_abilities,
        "source_ability_references": source_abilities,
        "unknown_abilities": unknown_abilities,
        "knowledge": knowledge,
        "knowledge_states": list(_KNOWLEDGE_STATES),
        "knowledge_topics": knowledge_matrix["topics"],
        "knowledge_visibility_edges": knowledge_matrix["edges"],
        "knowledge_matrix": knowledge_matrix["matrix"],
        "relationships": relationships,
        "relationship_inspector": relationship_inspector,
        "soft_relationships": soft_relationships,
        "factions": factions,
        "faction_inspector": faction_inspector,
        "source_state": {
            "status": "READY" if source_ready else "MISSING",
            "status_label": "原文状态已建立" if source_ready else "正在补齐这一章的故事状态",
            "layer": "SOURCE_VERIFIED" if source_ready else "UNKNOWN",
            "layer_label": (
                _LAYER_LABELS["SOURCE_VERIFIED"]
                if source_ready
                else _LAYER_LABELS["UNKNOWN"]
            ),
            "message": messages[availability],
            "ledger": source_projection,
            "baseline": {
                "available": baseline is not None,
                "boundary_chapter": (
                    None if baseline is None else baseline.manifest.boundary_chapter
                ),
                "visible_entry_count": len(baseline_visible),
                "verified_entry_count": sum(
                    1
                    for entry in baseline_visible
                    if entry.status is BaselineStatus.SOURCE_VERIFIED
                ),
                "partial_entry_count": sum(
                    1 for entry in baseline_visible if entry.status is BaselineStatus.SOURCE_PARTIAL
                ),
            },
            "hydration": source_projection.get("hydration", {}),
        },
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
                "source_state_deltas": int(source_projection.get("ledger_delta_count", 0)),
                "source_verified_deltas": int(source_projection.get("verified_delta_count", 0)),
                "baseline_visible_entries": len(baseline_visible),
            },
        },
    }


__all__ = ["build_story_game_state"]
