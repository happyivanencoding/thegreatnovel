"""Chapter-pinned Progression Workspace built from existing read authorities."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from novel_authoring.db.database import Database
from novel_authoring.progression.anticipation import build_anticipation_surface
from novel_authoring.progression.models import (
    PayoffChannelProfile,
    ProgressionContract,
    WorldExpansionContract,
)
from novel_authoring.progression.projections import (
    AxisObservation,
    project_progression_state,
    project_world_expansion_state,
)
from novel_authoring.progression.resources import project_opportunity_surface
from novel_authoring.progression.service import (
    ProgressionContractType,
    effective_contract_records,
    list_contract_records,
)
from novel_authoring.serial_kernel.classification import (
    market_category_label,
    narrative_drive_label,
)


def _chapter(world_state: Mapping[str, Any]) -> tuple[str, int]:
    chapter = world_state.get("chapter")
    if not isinstance(chapter, Mapping) or not chapter.get("chapter_id"):
        raise ValueError("成长工作台必须显式绑定一个真实章节")
    return str(chapter["chapter_id"]), int(chapter.get("ordinal") or 0)


def _thread_inputs(world_state: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for collection in ("threads", "promises"):
        items = world_state.get(collection, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, Mapping):
                continue
            values.append(
                {
                    **dict(item),
                    "subject": (
                        item.get("subject")
                        or item.get("question")
                        or item.get("statement")
                        or item.get("title")
                        or item.get("name")
                    ),
                }
            )
    return values


def _nested_mappings(value: object) -> list[Mapping[str, Any]]:
    values: list[Mapping[str, Any]] = []
    pending = [value]
    while pending:
        current = pending.pop()
        if isinstance(current, Mapping):
            values.append(current)
            pending.extend(current.values())
        elif isinstance(current, list):
            pending.extend(current)
    return values


def _approved_kernel_observations(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    through_chapter_ordinal: int,
) -> tuple[dict[str, AxisObservation], str | None]:
    """Derive observations only from approved Canon-linked draft state changes."""

    with database.connect() as connection:
        rows = connection.execute(
            """
            SELECT d.output_json, ch.ordinal
            FROM canon_commits cc
            JOIN drafts d ON d.draft_id=cc.draft_id AND d.edition_id=cc.edition_id
            JOIN chapters ch ON ch.chapter_id=cc.chapter_id AND ch.edition_id=cc.edition_id
            WHERE cc.book_id=? AND cc.edition_id=? AND ch.ordinal<=?
            ORDER BY ch.ordinal, cc.committed_at
            """,
            (book_id, edition_id, through_chapter_ordinal),
        ).fetchall()
    raw_axes: dict[str, dict[str, Any]] = {}
    current_world_stage: str | None = None
    import json

    for row in rows:
        try:
            output = json.loads(str(row["output_json"] or "{}"))
        except (TypeError, ValueError):
            continue
        for change in output.get("state_changes", []):
            if not isinstance(change, Mapping):
                continue
            payload = change.get("payload", {})
            if not isinstance(payload, Mapping):
                continue
            progression = payload.get("progression")
            if isinstance(progression, Mapping) and progression.get("axis_id"):
                axis_id = str(progression["axis_id"])
                value = raw_axes.setdefault(axis_id, {"evidence": []})
                if progression.get("stage_id"):
                    value["current_stage"] = str(progression["stage_id"])
                    value["recent_breakthrough"] = {
                        "chapter_ordinal": int(row["ordinal"]),
                        "stage_id": str(progression["stage_id"]),
                        "state_change_record_id": change.get("record_id"),
                    }
                if progression.get("substage"):
                    value["current_substage"] = str(progression["substage"])
                if progression.get("readiness"):
                    value["readiness"] = str(progression["readiness"])
                value["available_branches"] = list(
                    progression.get("available_branches", value.get("available_branches", []))
                )
                value["locked_branches"] = list(
                    progression.get("locked_branches", value.get("locked_branches", []))
                )
                value["evidence"].extend(
                    str(item) for item in change.get("evidence_quotes", [])
                )
            world_expansion = payload.get("world_expansion")
            if isinstance(world_expansion, Mapping) and world_expansion.get("stage_id"):
                current_world_stage = str(world_expansion["stage_id"])
        trace = output.get("realized_kernel_trace")
        if not isinstance(trace, Mapping):
            continue
        impact = trace.get("progression_impact", {})
        if isinstance(impact, Mapping):
            for axis_id in impact.get("axis_advanced", []):
                value = raw_axes.setdefault(str(axis_id), {"evidence": []})
                value["pending_showcases"] = list(impact.get("ability_showcase", []))
                value["progression_debts"] = list(trace.get("debts_advanced", []))
    return (
        {
            axis_id: AxisObservation.model_validate(value)
            for axis_id, value in raw_axes.items()
        },
        current_world_stage,
    )


def _source_axis_observations(
    world_state: Mapping[str, Any],
) -> tuple[dict[str, AxisObservation], str | None]:
    axes: dict[str, AxisObservation] = {}
    world_stage: str | None = None
    roots: list[object] = [world_state.get("character", {})]
    for collection in ("characters", "facts"):
        values = world_state.get(collection, [])
        if isinstance(values, list):
            roots.extend(values)
    for item in roots:
        for value in _nested_mappings(item):
            progression = value.get("progression")
            if isinstance(progression, Mapping) and progression.get("axis_id"):
                axis_id = str(progression["axis_id"])
                axes[axis_id] = AxisObservation.model_validate(
                    {
                        "current_stage": progression.get("stage_id"),
                        "current_substage": progression.get("substage"),
                        "available_branches": progression.get("available_branches", []),
                        "locked_branches": progression.get("locked_branches", []),
                        "readiness": progression.get("readiness", "UNKNOWN"),
                        "evidence": value.get("source_evidence", []),
                    }
                )
            expansion = value.get("world_expansion")
            if isinstance(expansion, Mapping) and expansion.get("stage_id"):
                world_stage = str(expansion["stage_id"])
    return axes, world_stage


def build_progression_workspace_from_world_state(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    world_state: Mapping[str, Any],
    planning_target_ordinal: int | None = None,
) -> dict[str, Any]:
    """Attach only contract + chapter-state projections; never persist observations."""

    chapter_id, chapter_ordinal = _chapter(world_state)
    effective_ordinal = planning_target_ordinal or chapter_ordinal
    if effective_ordinal < chapter_ordinal:
        raise ValueError("成长投影的生效边界不能早于状态章节")
    records = {
        contract_type: record
        for contract_type, record in effective_contract_records(
            database,
            book_id=book_id,
            edition_id=edition_id,
        ).items()
        if int(record.effective_from_boundary or 0) <= effective_ordinal
    }
    proposals = [
        record
        for record in list_contract_records(
            database,
            book_id=book_id,
            edition_id=edition_id,
        )
        if record.status.value in {"INFERRED_PROPOSAL", "NEEDS_REVIEW"}
    ]
    progression_record = records.get(ProgressionContractType.PROGRESSION)
    world_record = records.get(ProgressionContractType.WORLD_EXPANSION)
    payoff_record = records.get(ProgressionContractType.PAYOFF_CHANNEL)

    progression = None
    source_observations, source_world_stage = _source_axis_observations(world_state)
    approved_observations, approved_world_stage = _approved_kernel_observations(
        database,
        book_id=book_id,
        edition_id=edition_id,
        through_chapter_ordinal=chapter_ordinal,
    )
    axis_observations = {**source_observations, **approved_observations}
    if progression_record is not None:
        contract = ProgressionContract.model_validate(
            progression_record.payload
        ).model_copy(update={"effective_from_boundary": None})
        subject_id = str(world_state.get("selected_character_id") or book_id)
        progression = project_progression_state(
            world_state,
            contract,
            subject_id=subject_id,
            axis_observations=axis_observations,
        )

    world_expansion = None
    if world_record is not None:
        world_expansion = project_world_expansion_state(
            world_state,
            WorldExpansionContract.model_validate(world_record.payload).model_copy(
                update={"effective_from_boundary": None}
            ),
            current_stage_id=approved_world_stage or source_world_stage,
        )

    opportunity_surface = project_opportunity_surface(world_state, ())
    payoff_readiness: list[dict[str, Any]] = []
    if payoff_record is not None:
        payoff = PayoffChannelProfile.model_validate(payoff_record.payload)
        payoff_readiness = [
            {
                "channel": channel.value,
                "promise_strength": strength.value,
                "readiness": "UNKNOWN",
                "evidence": [],
            }
            for channel, strength in payoff.channels.items()
        ]
    anticipation = build_anticipation_surface(
        chapter_id=chapter_id,
        chapter_ordinal=chapter_ordinal,
        opportunities=opportunity_surface,
        active_threads=_thread_inputs(world_state),
        world_expansion=world_expansion,
    )
    available = progression is not None
    proposal_values: list[dict[str, Any]] = []
    for item in proposals:
        value = item.model_dump(mode="json")
        if item.contract_type is ProgressionContractType.NARRATIVE_DRIVE:
            payload = dict(value["payload"])
            payload["primary_drive_display"] = narrative_drive_label(
                str(payload.get("primary_drive") or "")
            )
            payload["secondary_drive_displays"] = [
                narrative_drive_label(str(drive))
                for drive in payload.get("secondary_drives", [])
            ]
            value["payload"] = payload
        elif item.contract_type is ProgressionContractType.MARKET_CATEGORY:
            payload = dict(value["payload"])
            payload["display_labels"] = [
                market_category_label(str(category))
                for category in [
                    payload.get("primary_market_category"),
                    *payload.get("secondary_market_categories", []),
                ]
                if category
            ]
            value["payload"] = payload
        proposal_values.append(value)
    return {
        "available": available,
        "message": (
            "成长状态来自当前章节的 World State；没有证据的阶段与准备度保持 UNKNOWN。"
            if available
            else "这本书尚未建立成长体系。现有世界状态仍可正常使用。"
        ),
        "chapter": {"chapter_id": chapter_id, "ordinal": chapter_ordinal},
        "effective_at_boundary": effective_ordinal,
        "progression_state": (
            None if progression is None else progression.model_dump(mode="json")
        ),
        "progression_contract": (
            None if progression_record is None else progression_record.payload
        ),
        "world_expansion": (
            None if world_expansion is None else world_expansion.model_dump(mode="json")
        ),
        "world_expansion_contract": (
            None if world_record is None else world_record.payload
        ),
        "opportunity_surface": opportunity_surface.model_dump(mode="json"),
        "payoff_readiness": payoff_readiness,
        "anticipation": anticipation.model_dump(mode="json"),
        "contract_records": {
            contract_type.value: {
                "contract_record_id": record.contract_record_id,
                "version_number": record.version_number,
                "effective_from_boundary": record.effective_from_boundary,
            }
            for contract_type, record in records.items()
        },
        "contract_proposals": proposal_values,
        "projection_only": True,
        "canon_mutation_allowed": False,
    }


def attach_progression_workspace(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    world_state: dict[str, Any],
) -> dict[str, Any]:
    if not world_state.get("chapter"):
        world_state.update(
            {
                "progression_state": None,
                "world_expansion": None,
                "opportunity_surface": None,
                "payoff_readiness": [],
                "anticipation": None,
                "progression_workspace": None,
            }
        )
        return world_state
    workspace = build_progression_workspace_from_world_state(
        database,
        book_id=book_id,
        edition_id=edition_id,
        world_state=world_state,
    )
    world_state.update(
        {
            "progression_state": workspace["progression_state"],
            "world_expansion": workspace["world_expansion"],
            "opportunity_surface": workspace["opportunity_surface"],
            "payoff_readiness": workspace["payoff_readiness"],
            "anticipation": workspace["anticipation"],
            "progression_workspace": workspace,
        }
    )
    return world_state


def build_progression_workspace(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    chapter_id: str,
) -> dict[str, Any]:
    from novel_authoring.author_control.projections import build_story_game_state

    world_state = build_story_game_state(
        database,
        book_id,
        edition_id,
        chapter_id=chapter_id,
    )
    chapter = world_state.get("chapter") or {}
    if str(chapter.get("chapter_id") or "") != chapter_id:
        raise ValueError("章节不存在，不能回退到最新章生成成长投影")
    workspace = world_state.get("progression_workspace")
    if not isinstance(workspace, dict):
        raise RuntimeError("成长工作台投影未建立")
    return workspace


__all__ = [
    "attach_progression_workspace",
    "build_progression_workspace",
    "build_progression_workspace_from_world_state",
]
