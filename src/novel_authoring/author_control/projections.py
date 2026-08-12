"""Read-only chapter-aware Story Game State projections."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.author_control.source_state import (
    build_source_state_projection,
    source_state_coverage_summary,
)
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

_KNOWLEDGE_STATE_LABELS = {
    "KNOWN": "知道",
    "SEEN": "亲眼见过",
    "HEARD": "听说",
    "SUSPECTED": "怀疑",
    "MISUNDERSTOOD": "误解",
    "UNKNOWN": "尚未知",
}

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
    "role",
    "current_role",
    "goal",
    "current_goal",
    "faction",
    "faction_id",
    "affiliation",
}

_AUTHOR_ATTRIBUTE_LABELS = {
    "current_location": "当前地点",
    "location": "当前地点",
    "location_id": "当前地点",
    "current_goal": "当前目标",
    "goal": "当前目标",
    "objective": "当前目标",
    "health": "身体状态",
    "body": "身体状态",
    "injury": "伤势",
    "condition": "身体状态",
    "mood": "情绪",
    "emotion": "情绪",
    "mental_state": "心理状态",
    "risk": "风险",
    "danger": "风险",
    "threat": "威胁",
    "level": "等级",
    "experience": "经验",
    "experience_after": "当前经验",
    "experience_display": "经验进度",
    "remaining_to_next_level": "距离升级",
    "strength": "力量",
    "agility": "敏捷",
    "constitution": "体质",
    "spirit": "精神",
    "hunger": "饥饿",
    "armor": "护甲",
    "quantity": "数量",
    "use": "用途",
    "usage": "用途",
    "status": "状态",
}


class ChapterWorldStateView(BaseModel):
    """One read-only AFTER_CHAPTER world-state view from existing authorities."""

    model_config = ConfigDict(extra="forbid")

    book_id: str
    edition_id: str
    chapter: dict[str, Any] | None
    view: str = "AFTER_CHAPTER"
    coverage: dict[str, Any] | None = None
    coverage_summary: dict[str, int | float] = Field(default_factory=dict)
    coverage_status: str
    state_changed: bool
    counts: dict[str, int]
    characters: list[dict[str, Any]] = Field(default_factory=list)
    locations: list[dict[str, Any]] = Field(default_factory=list)
    inventory: list[dict[str, Any]] = Field(default_factory=list)
    equipment: list[dict[str, Any]] = Field(default_factory=list)
    resources: list[dict[str, Any]] = Field(default_factory=list)
    abilities: list[dict[str, Any]] = Field(default_factory=list)
    knowledge_topics: list[dict[str, Any]] = Field(default_factory=list)
    knowledge_visibility: list[dict[str, Any]] = Field(default_factory=list)
    knowledge_matrix: list[dict[str, Any]] = Field(default_factory=list)
    relationships: list[dict[str, Any]] = Field(default_factory=list)
    factions: list[dict[str, Any]] = Field(default_factory=list)
    world_rules: list[dict[str, Any]] = Field(default_factory=list)
    tasks: list[dict[str, Any]] = Field(default_factory=list)
    threads: list[dict[str, Any]] = Field(default_factory=list)
    promises: list[dict[str, Any]] = Field(default_factory=list)
    chapter_delta: dict[str, Any] = Field(default_factory=dict)
    author_intents: list[dict[str, Any]] = Field(default_factory=list)
    provisional_draft_overlay: list[dict[str, Any]] = Field(default_factory=list)
    progression_state: dict[str, Any] | None = None
    world_expansion: dict[str, Any] | None = None
    opportunity_surface: dict[str, Any] | None = None
    payoff_readiness: list[dict[str, Any]] = Field(default_factory=list)
    anticipation: dict[str, Any] | None = None


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


def _is_location(value: dict[str, Any]) -> bool:
    raw = " ".join(
        str(value.get(key) or "") for key in ("entity_type", "node_type", "type", "category")
    ).lower()
    return any(token in raw for token in ("location", "place", "site", "地点", "场所"))


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


def _public_attributes(value: dict[str, Any]) -> list[dict[str, Any]]:
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
    result: list[dict[str, Any]] = []
    for key, raw in value.items():
        if str(key) in excluded or raw is None or isinstance(raw, (dict, list)):
            continue
        raw_key = str(key)
        result.append(
            {
                "key": raw_key,
                "label": _AUTHOR_ATTRIBUTE_LABELS.get(raw_key, raw_key),
                "value": str(raw),
                "author_visible": raw_key in _AUTHOR_ATTRIBUTE_LABELS,
            }
        )
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
    suppress_mutable_statement: bool = False,
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
        "statement": "" if suppress_mutable_statement else entry.statement,
        "description": "" if suppress_mutable_statement else entry.statement,
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
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    source_projection: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    options: dict[str, dict[str, Any]] = {}
    source_activity: dict[str, int] = {}

    def add(record_id: str, name: str, layer: str, description: str = "") -> None:
        if not record_id:
            return
        if record_id in options:
            current = options[record_id]
            if current["name"] == record_id and name != record_id:
                current["name"] = name
            return
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
        suppress_baseline_state = (
            selected_ordinal is not None
            and selected_ordinal < baseline.manifest.boundary_chapter
        )
        for entry in baseline.entries:
            if entry.category is BaselineCategory.CHARACTER and _baseline_visible(
                entry, chapter_ordinals, selected_ordinal
            ):
                add(
                    str(entry.subject_id or entry.entry_id),
                    entry.name,
                    entry.status.value,
                    "" if suppress_baseline_state else entry.statement,
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
                        raw_payload_value = raw.get("payload")
                        raw_payload = (
                            raw_payload_value
                            if isinstance(raw_payload_value, dict)
                            else {}
                        )
                        candidates.extend(
                            [
                                record.get("from_entity_id"),
                                record.get("to_entity_id"),
                                raw_payload.get("from_entity_id"),
                                raw_payload.get("to_entity_id"),
                                raw_payload.get("related_person_id"),
                                raw_payload.get("counterparty_id"),
                            ]
                        )
                    for candidate in candidates:
                        character = str(candidate or "")
                        if character.startswith("character:"):
                            source_activity[character] = source_activity.get(character, 0) + 1
                            source_name = str(raw.get("character_name") or character)
                            if (
                                category == "CHARACTER_STATE"
                                and str(record.get("subject_id") or "") == character
                            ):
                                source_name = str(record.get("name") or source_name)
                            add(
                                character,
                                source_name,
                                "SOURCE_VERIFIED",
                            )
    return sorted(
        options.values(),
        key=lambda item: -source_activity.get(str(item["character_id"]), 0),
    )


def _selected_character(
    options: list[dict[str, Any]], character_id: str | None
) -> dict[str, Any] | None:
    if character_id:
        exact = next((item for item in options if item["character_id"] == character_id), None)
        if exact is not None:
            return exact
        return {
            "character_id": character_id,
            "name": "该人物（本章暂无证据）",
            "layer": "UNKNOWN",
            "layer_label": _LAYER_LABELS["UNKNOWN"],
            "status_label": _LAYER_LABELS["UNKNOWN"],
            "description": "所选人物在这一章边界还没有可回指的状态证据。",
            "is_selectable": False,
        }
    return options[0] if options else None


def _character_state(
    projection: CanonProjection,
    baseline: RuntimeBaseline | None,
    selected: dict[str, Any] | None,
    *,
    chapter_ordinals: dict[str, int],
    selected_ordinal: int | None,
    source_projection: dict[str, Any],
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
    source_character = next(
        (
            dict(record)
            for record in source_projection.get("records", {}).get("CHARACTER_STATE", [])
            if isinstance(record, dict)
            and record.get("status") == "SOURCE_VERIFIED"
            and str(record.get("subject_id") or "") == character_id
        ),
        None,
    )
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
        if source_character is not None:
            return {
                "available": True,
                "status": "SOURCE_VERIFIED",
                "status_label": _LAYER_LABELS["SOURCE_VERIFIED"],
                "layer": "SOURCE_VERIFIED",
                "character_id": character_id,
                "name": selected["name"],
                "description": source_character.get("description")
                or source_character.get("statement")
                or "",
                "attributes": source_character.get("attributes", []),
                "source": "Source State",
                "evidence": source_character.get("evidence_locator", []),
                "message": "这是截至所选章节、由本章及此前原文证据重放得到的角色状态。",
                "raw": source_character,
            }
        if baseline_entry is not None:
            suppress_baseline_state = (
                baseline is not None
                and selected_ordinal is not None
                and selected_ordinal < baseline.manifest.boundary_chapter
            )
            source = _baseline_record(
                baseline_entry,
                category="character",
                chapter_ordinals=chapter_ordinals,
                selected_ordinal=selected_ordinal,
                suppress_mutable_statement=suppress_baseline_state,
            )
            return {
                "available": True,
                "status": source["status"],
                "status_label": source["status_label"],
                "layer": source["layer"],
                "character_id": character_id,
                "name": selected["name"],
                "description": selected.get("description") or source["description"],
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
            "description": selected.get("description") or "",
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
    verified_source = [
        record
        for record in _source_records_for_character(
            source_projection, {"CAPABILITY"}, character_id
        )
        if record.get("status") == "SOURCE_VERIFIED"
    ]
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
            if (
                entry.status is BaselineStatus.SOURCE_VERIFIED
                and not verified_source
            ):
                canon.append(record)
    source.extend(verified_source)
    visible_keys = {
        str(item.get("state_key") or item.get("object_id") or item.get("record_id"))
        for item in canon
    }
    canon.extend(
        record
        for record in verified_source
        if str(record.get("state_key") or record.get("object_id") or record.get("record_id"))
        not in visible_keys
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
    *,
    extra_topics: list[dict[str, Any]] | None = None,
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
            "state_label": _KNOWLEDGE_STATE_LABELS[state],
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
    for item in extra_topics or []:
        topic_id = str(
            item.get("object_id")
            or item.get("state_key")
            or item.get("record_id")
            or item.get("name")
            or ""
        )
        if topic_id:
            topics.setdefault(
                topic_id,
                {
                    "topic_id": topic_id,
                    "name": str(item.get("name") or topic_id),
                    "layer": item.get("layer") or "UNKNOWN",
                    "topic_type": "ITEM",
                },
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
                    "state_label": (
                        _KNOWLEDGE_STATE_LABELS["UNKNOWN"]
                        if cell is None
                        else cell["state_label"]
                    ),
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
        "states": [
            {"value": state, "label": _KNOWLEDGE_STATE_LABELS[state]}
            for state in _KNOWLEDGE_STATES
        ],
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
        raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
        payload_value = raw.get("payload")
        payload: dict[str, Any] = payload_value if isinstance(payload_value, dict) else {}
        facts = {**raw, **payload, **record}
        details.append(
            {
                **record,
                "from_entity_id": facts.get("from_entity_id"),
                "to_entity_id": facts.get("to_entity_id"),
                "first_confirmed_chapter_ordinal": record.get(
                    "first_confirmed_chapter_ordinal", record.get("chapter_ordinal")
                ),
                "recent_confirmed_chapter_ordinal": record.get(
                    "recent_confirmed_chapter_ordinal", record.get("chapter_ordinal")
                ),
                "dimensions": {
                    name: str(facts.get(name) or "UNKNOWN").upper()
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
        raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
        payload_value = raw.get("payload")
        payload: dict[str, Any] = payload_value if isinstance(payload_value, dict) else {}
        facts = {**raw, **payload, **record}
        result.append(
            {
                **record,
                "state": payload.get("state") or raw.get("state") or "UNKNOWN",
                "public_goal": facts.get("public_goal")
                or facts.get("public_objective")
                or "UNKNOWN",
                "goal": facts.get("goal") or facts.get("objective") or "UNKNOWN",
                "key_people": facts.get("key_people") or facts.get("members") or [],
                "controlled_locations": facts.get("controlled_locations") or [],
                "resources": facts.get("resources") or [],
                "relationships": facts.get("relationships") or [],
                "attitude": facts.get("attitude") or "UNKNOWN",
                "action": facts.get("action") or "UNKNOWN",
                "known": facts.get("known") or [],
                "unknown": facts.get("unknown") or [],
                "current_layer": record.get("layer") or "UNKNOWN",
                "author_plan_separate": True,
            }
        )
    return result


def _location_details(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for record in records:
        raw_value = record.get("raw")
        raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
        payload_value = raw.get("payload")
        payload: dict[str, Any] = payload_value if isinstance(payload_value, dict) else {}
        facts = {**raw, **payload, **record}
        result.append(
            {
                **record,
                "public_status": payload.get("public_status")
                or payload.get("state")
                or raw.get("public_status")
                or raw.get("state")
                or "UNKNOWN",
                "recent_events": facts.get("recent_events") or facts.get("events") or [],
                "present_characters": facts.get("present_characters")
                or facts.get("characters")
                or [],
                "resources": facts.get("resources") or [],
                "constraints": facts.get("constraints") or facts.get("rules") or [],
                "related_factions": facts.get("related_factions")
                or facts.get("factions")
                or [],
                "known": facts.get("known") or [],
                "unknown": facts.get("unknown") or [],
            }
        )
    return result


def _source_category_records(
    source_projection: dict[str, Any], category: str
) -> list[dict[str, Any]]:
    records = source_projection.get("records", {})
    if not isinstance(records, dict):
        return []
    return [
        dict(record)
        for record in records.get(category, [])
        if isinstance(record, dict) and record.get("status") == "SOURCE_VERIFIED"
    ]


def _canon_records(
    values: dict[str, dict[str, Any]], *, category: str
) -> list[dict[str, Any]]:
    return [
        _record(
            str(record_id),
            dict(value),
            layer="CANON",
            fallback_name=str(record_id),
            category=category,
        )
        for record_id, value in values.items()
    ]


def _author_intents_at_chapter(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapter_id: str | None,
) -> list[dict[str, Any]]:
    rows = connection.execute(
        "SELECT * FROM author_control_intents "
        "WHERE book_id=? AND edition_id=? AND status IN ('PLANNED', 'ACTIVE') "
        "AND (target_chapter_id IS NULL OR target_chapter_id=?) "
        "ORDER BY priority, updated_at DESC, intent_id",
        (book_id, edition_id, chapter_id),
    ).fetchall()
    return [
        {
            **dict(row),
            "layer": "AUTHOR_INTENT",
            "layer_label": _LAYER_LABELS["AUTHOR_INTENT"],
            "payload": _json_object(row["payload_json"]),
        }
        for row in rows
    ]


def _provisional_overlay_at_chapter(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int | None,
) -> list[dict[str, Any]]:
    if chapter_ordinal is None:
        return []
    rows = connection.execute(
        "SELECT d.draft_id, d.status, d.revision, p.candidate_id, p.plan_json "
        "FROM drafts d "
        "JOIN chapter_contracts c ON c.book_id=d.book_id AND c.edition_id=d.edition_id "
        "AND c.contract_id=d.contract_id "
        "LEFT JOIN candidate_plans p ON p.book_id=d.book_id AND p.edition_id=d.edition_id "
        "AND p.candidate_id=d.candidate_id "
        "WHERE d.book_id=? AND d.edition_id=? AND c.target_chapter_ordinal=? "
        "AND d.status NOT IN ('COMMITTED', 'REJECTED') "
        "ORDER BY d.revision DESC, d.created_at DESC",
        (book_id, edition_id, chapter_ordinal),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        plan = _json_object(row["plan_json"])
        result.append(
            {
                "draft_id": str(row["draft_id"]),
                "candidate_id": row["candidate_id"],
                "status": str(row["status"]),
                "revision": int(row["revision"]),
                "state_changes": list(plan.get("state_changes", [])),
                "commit_updates": list(plan.get("commit_updates", [])),
                "layer": "PROVISIONAL",
                "layer_label": _LAYER_LABELS["PROVISIONAL"],
            }
        )
    return result


def _attach_who_knows(
    records: list[dict[str, Any]], matrix: list[dict[str, Any]]
) -> None:
    for record in records:
        identities = {
            str(value)
            for value in (
                record.get("object_id"),
                record.get("state_key"),
                record.get("record_id"),
                record.get("name"),
            )
            if value
        }
        record["who_knows"] = [
            dict(cell)
            for cell in matrix
            if str(cell.get("topic_id") or "") in identities
            or str(cell.get("topic_name") or "") in identities
        ]


def _record_identities(record: dict[str, Any]) -> set[str]:
    return {
        str(value)
        for value in (
            record.get("state_key"),
            record.get("object_id"),
            record.get("record_id"),
            record.get("name"),
        )
        if value
    }


def _attach_history(
    records: list[dict[str, Any]],
    history: list[dict[str, Any]],
    *,
    selected_ordinal: int | None,
) -> None:
    for record in records:
        identities = _record_identities(record)
        entries = [
            dict(entry)
            for entry in history
            if identities & _record_identities(entry)
        ]
        entries.sort(
            key=lambda item: (
                int(item.get("chapter_ordinal") or 0),
                str(item.get("record_id") or ""),
            )
        )
        record["history"] = entries
        record["changed_this_chapter"] = any(
            selected_ordinal is not None
            and int(item.get("chapter_ordinal") or 0) == selected_ordinal
            for item in entries
        )


def _extend_unique(
    target: list[dict[str, Any]], records: list[dict[str, Any]]
) -> None:
    seen = {
        (
            str(item.get("record_id") or item.get("state_key") or item.get("name") or ""),
            str(item.get("owner_id") or item.get("current_holder_id") or ""),
        )
        for item in target
    }
    for record in records:
        key = (
            str(record.get("record_id") or record.get("state_key") or record.get("name") or ""),
            str(record.get("owner_id") or record.get("current_holder_id") or ""),
        )
        if key in seen:
            continue
        target.append(record)
        seen.add(key)


def _character_recent_changes(
    character_id: str, chapter_delta: dict[str, Any]
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in chapter_delta.get("confirmed", []):
        if character_id in {
            str(item.get("subject_id") or ""),
            str(item.get("owner_id") or ""),
            str(item.get("current_holder_id") or ""),
            str(item.get("from_entity_id") or ""),
            str(item.get("to_entity_id") or ""),
        }:
            result.append(dict(item))
    return result


def _relationship_graph(
    characters: list[dict[str, Any]],
    factions: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    nodes = [
        {
            "node_id": str(item.get("character_id")),
            "name": str(item.get("name") or item.get("character_id")),
            "node_type": "CHARACTER",
            "layer": item.get("layer"),
        }
        for item in characters
        if item.get("character_id")
    ]
    nodes.extend(
        {
            "node_id": str(item.get("object_id") or item.get("record_id")),
            "name": str(item.get("name") or item.get("object_id") or item.get("record_id")),
            "node_type": "FACTION",
            "layer": item.get("layer"),
        }
        for item in factions
        if item.get("object_id") or item.get("record_id")
    )
    edges = [
        {
            "edge_id": str(item.get("record_id") or f"relationship-{index}"),
            "from_id": item.get("from_entity_id"),
            "to_id": item.get("to_entity_id"),
            "label": item.get("name") or item.get("statement") or "关系",
            "layer": item.get("current_layer") or item.get("layer"),
            "inspector": item,
        }
        for index, item in enumerate(relationships, start=1)
        if item.get("from_entity_id") and item.get("to_entity_id")
    ]
    return {"nodes": nodes, "edges": edges}


def build_story_game_state(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_id: str | None = None,
    character_id: str | None = None,
    include_global_scope: bool = False,
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
            materialize_snapshot=False,
        )
        coverage_summary = source_state_coverage_summary(
            connection, book_id, edition_id
        )
        workspace_root = _workspace_root(connection, book_id)
        soft = _soft_atlas(workspace_root, book_id, edition_id)
        selected_chapter_id = (
            None if selected_chapter is None else str(selected_chapter["chapter_id"])
        )
        author_intents = _author_intents_at_chapter(
            connection, book_id, edition_id, selected_chapter_id
        )
        provisional_overlay = _provisional_overlay_at_chapter(
            connection, book_id, edition_id, ordinal
        )

    options = _character_options(
        projection,
        baseline,
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
        source_projection=source_projection,
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
    knowledge_matrix = _knowledge_matrix(
        projection,
        source_projection,
        options,
        extra_topics=[*inventory, *equipment],
    )
    verified_history = list(source_projection.get("verified_history", []))
    _attach_who_knows(inventory, knowledge_matrix["matrix"])
    _attach_who_knows(equipment, knowledge_matrix["matrix"])
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
    source_factions = _source_category_records(source_projection, "FACTION")
    canon_factions = [
        _record(
            str(record_id),
            dict(value),
            layer="CANON",
            fallback_name=str(record_id),
            category="faction",
        )
        for record_id, value in projection.entities.items()
        if _is_faction(dict(value))
    ]
    factions = [*canon_factions, *source_factions]
    faction_inspector = _faction_details(factions)
    locations = [
        _record(
            str(record_id),
            dict(value),
            layer="CANON",
            fallback_name=str(record_id),
            category="location",
        )
        for record_id, value in projection.entities.items()
        if _is_location(dict(value))
    ]
    locations.extend(_source_category_records(source_projection, "LOCATION"))
    locations = _location_details(locations)
    resources = [
        *_canon_records(projection.resources, category="resource"),
        *_source_category_records(source_projection, "RESOURCE"),
    ]
    world_rules = [
        _record(
            str(record_id),
            dict(value),
            layer="CANON",
            fallback_name=str(record_id),
            category="world_rule",
        )
        for record_id, value in projection.facts.items()
        if "rule" in str(value.get("category") or value.get("fact_type") or "").lower()
        or "规则" in str(value.get("statement") or "")
    ]
    world_rules.extend(_source_category_records(source_projection, "WORLD_RULE"))
    source_tasks_and_promises = _source_category_records(
        source_projection, "TASK_OR_PROMISE"
    )

    def source_kind(record: dict[str, Any]) -> str:
        raw_value = record.get("raw")
        raw: dict[str, Any] = raw_value if isinstance(raw_value, dict) else {}
        payload_value = raw.get("payload")
        payload: dict[str, Any] = payload_value if isinstance(payload_value, dict) else {}
        return str(payload.get("kind") or payload.get("type") or "PROMISE").upper()

    tasks = [
        record for record in source_tasks_and_promises if source_kind(record) == "TASK"
    ]
    threads = _canon_records(projection.threads, category="thread")
    threads.extend(
        record for record in source_tasks_and_promises if source_kind(record) == "THREAD"
    )
    promises = _canon_records(projection.promises, category="promise")
    promises.extend(
        record
        for record in source_tasks_and_promises
        if source_kind(record) not in {"TASK", "THREAD"}
    )

    for collection in (
        inventory,
        equipment,
        canon_abilities,
        knowledge,
        relationship_inspector,
        faction_inspector,
        locations,
        resources,
        world_rules,
        tasks,
        threads,
        promises,
    ):
        _attach_history(collection, verified_history, selected_ordinal=ordinal)

    character_workspaces: list[dict[str, Any]] = []
    all_inventory: list[dict[str, Any]] = []
    all_equipment: list[dict[str, Any]] = []
    all_abilities: list[dict[str, Any]] = []
    all_relationships: list[dict[str, Any]] = []
    workspace_options = (
        list(options)
        if include_global_scope
        else ([] if selected is None else [selected])
    )
    if selected is not None and not any(
        item["character_id"] == selected["character_id"] for item in workspace_options
    ):
        workspace_options.append(selected)
    character_names = {
        str(item["character_id"]): str(item.get("name") or "未命名人物")
        for item in options
    }
    for option in workspace_options:
        option_id = str(option["character_id"])
        if selected is not None and option_id == str(selected["character_id"]):
            option_state = selected_state
            option_inventory = inventory
            option_equipment = equipment
            option_abilities = canon_abilities
            option_relationships = relationship_inspector
        else:
            option_state = _character_state(
                projection,
                baseline,
                option,
                chapter_ordinals=chapter_ordinals,
                selected_ordinal=ordinal,
                source_projection=source_projection,
            )
            option_raw_value = option_state.get("raw")
            option_raw = (
                option_raw_value if isinstance(option_raw_value, dict) else {}
            )
            option_inventory, option_equipment = _projection_items(
                projection,
                baseline,
                option,
                option_raw,
                chapter_ordinals=chapter_ordinals,
                selected_ordinal=ordinal,
                source_projection=source_projection,
            )
            option_abilities, _option_source_abilities = _abilities(
                projection,
                baseline,
                option,
                chapter_ordinals=chapter_ordinals,
                selected_ordinal=ordinal,
                source_projection=source_projection,
            )
            option_relationships = _relationship_details(
                _relationships(
                    projection,
                    option,
                    source_projection=source_projection,
                )
            )
            _attach_who_knows(option_inventory, knowledge_matrix["matrix"])
            _attach_who_knows(option_equipment, knowledge_matrix["matrix"])
            for collection in (
                option_inventory,
                option_equipment,
                option_abilities,
                option_relationships,
            ):
                _attach_history(collection, verified_history, selected_ordinal=ordinal)
        for record in [*option_inventory, *option_equipment, *option_abilities]:
            record["owner_name"] = character_names.get(option_id, option.get("name"))
        _extend_unique(all_inventory, option_inventory)
        _extend_unique(all_equipment, option_equipment)
        _extend_unique(all_abilities, option_abilities)
        _extend_unique(all_relationships, option_relationships)
        character_workspaces.append(
            {
                **option,
                "state": option_state,
                "inventory": option_inventory,
                "equipment": option_equipment,
                "abilities": option_abilities,
                "relationships": option_relationships,
                "recent_changes": _character_recent_changes(
                    option_id, source_projection.get("chapter_delta", {})
                ),
                "counts": {
                    "inventory": len(option_inventory),
                    "equipment": len(option_equipment),
                    "abilities": len(option_abilities),
                    "relationships": len(option_relationships),
                },
            }
        )
    scope_counts = {
        "global": {
            "characters": len(options),
            "inventory": len(all_inventory),
            "equipment": len(all_equipment),
            "abilities": len(all_abilities),
            "relationships": len(all_relationships),
        },
        "selected_character": {
            "characters": 1 if selected is not None else 0,
            "inventory": len(inventory),
            "equipment": len(equipment),
            "abilities": len(canon_abilities),
            "relationships": len(relationship_inspector),
        },
    }
    relationship_graph = _relationship_graph(options, factions, relationship_inspector)
    source_ready = bool(source_projection.get("available"))
    if after_event_seq is not None:
        availability = "CANON_EVENT_PROJECTION"
    elif source_ready:
        availability = "SOURCE_CHAPTER_STATE_PROJECTION"
    else:
        availability = "SOURCE_STATE_HYDRATION_REQUIRED"
    availability_labels = {
        "CANON_EVENT_PROJECTION": "正史已确认",
        "SOURCE_CHAPTER_STATE_PROJECTION": "章节原文状态",
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
    chapter_value = (
        {
            "chapter_id": str(selected_chapter["chapter_id"]),
            "ordinal": ordinal,
            "title": str(selected_chapter["title"]),
        }
        if selected_chapter is not None
        else None
    )
    world_state = ChapterWorldStateView(
        book_id=book_id,
        edition_id=edition_id,
        chapter=chapter_value,
        coverage=source_projection.get("coverage"),
        coverage_summary=coverage_summary,
        coverage_status=str(source_projection.get("coverage_status") or "NOT_STARTED"),
        state_changed=bool(source_projection.get("state_changed")),
        counts={
            "characters": len(options),
            "locations": len(locations),
            "inventory": len(inventory),
            "equipment": len(equipment),
            "resources": len(resources),
            "abilities": len(canon_abilities),
            "knowledge_topics": len(knowledge_matrix["topics"]),
            "relationships": len(relationship_inspector),
            "factions": len(faction_inspector),
            "world_rules": len(world_rules),
            "tasks": len(tasks),
            "threads": len(threads),
            "promises": len(promises),
        },
        characters=options,
        locations=locations,
        inventory=inventory,
        equipment=equipment,
        resources=resources,
        abilities=canon_abilities,
        knowledge_topics=knowledge_matrix["topics"],
        knowledge_visibility=knowledge_matrix["edges"],
        knowledge_matrix=knowledge_matrix["matrix"],
        relationships=relationship_inspector,
        factions=faction_inspector,
        world_rules=world_rules,
        tasks=tasks,
        threads=threads,
        promises=promises,
        chapter_delta=source_projection.get("chapter_delta", {}),
        author_intents=author_intents,
        provisional_draft_overlay=provisional_overlay,
    )
    state_payload = {
        **world_state.model_dump(mode="json"),
        "availability": availability,
        "availability_label": availability_labels[availability],
        "message": messages[availability],
        "chapter": chapter_value,
        "timepoint": {
            "before_event_seq": before_event_seq or None,
            "after_event_seq": after_event_seq,
            "historical": after_event_seq is not None,
            "source_projection_available": source_ready,
            "source_projection_status": source_projection.get("projection_status"),
        },
        "characters": options,
        "character_workspaces": character_workspaces,
        "selected_character_id": selected["character_id"] if selected else None,
        "character": selected_state,
        "inventory": inventory,
        "all_inventory": all_inventory,
        "equipment": equipment,
        "all_equipment": all_equipment,
        "abilities": canon_abilities,
        "all_abilities": all_abilities,
        "source_ability_references": source_abilities,
        "unknown_abilities": unknown_abilities,
        "knowledge": knowledge,
        "knowledge_states": [
            {"value": state, "label": _KNOWLEDGE_STATE_LABELS[state]}
            for state in _KNOWLEDGE_STATES
        ],
        "knowledge_topics": knowledge_matrix["topics"],
        "knowledge_visibility_edges": knowledge_matrix["edges"],
        "knowledge_matrix": knowledge_matrix["matrix"],
        "relationships": relationship_inspector,
        "all_relationships": all_relationships,
        "relationship_inspector": relationship_inspector,
        "relationship_graph": relationship_graph,
        "soft_relationships": soft_relationships,
        "factions": faction_inspector,
        "faction_inspector": faction_inspector,
        "scope_counts": scope_counts,
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
            "coverage": source_projection.get("coverage"),
            "coverage_summary": coverage_summary,
            "coverage_status": source_projection.get("coverage_status"),
            "state_changed": source_projection.get("state_changed", False),
            "chapter_delta": source_projection.get("chapter_delta", {}),
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
    from novel_authoring.progression.workspace import attach_progression_workspace

    return attach_progression_workspace(
        database,
        book_id=book_id,
        edition_id=edition_id,
        world_state=state_payload,
    )


__all__ = ["ChapterWorldStateView", "build_story_game_state"]
