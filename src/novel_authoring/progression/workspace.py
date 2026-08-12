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


def build_progression_workspace_from_world_state(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    world_state: Mapping[str, Any],
) -> dict[str, Any]:
    """Attach only contract + chapter-state projections; never persist observations."""

    chapter_id, chapter_ordinal = _chapter(world_state)
    records = effective_contract_records(
        database,
        book_id=book_id,
        edition_id=edition_id,
    )
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
    if progression_record is not None:
        contract = ProgressionContract.model_validate(progression_record.payload)
        subject_id = str(world_state.get("selected_character_id") or book_id)
        progression = project_progression_state(
            world_state,
            contract,
            subject_id=subject_id,
        )

    world_expansion = None
    if world_record is not None:
        world_expansion = project_world_expansion_state(
            world_state,
            WorldExpansionContract.model_validate(world_record.payload),
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
