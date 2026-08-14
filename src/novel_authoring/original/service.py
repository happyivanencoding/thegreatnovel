"""Source-free original novel service built on the existing authoring kernel."""

from __future__ import annotations

import json
import sqlite3
import uuid
from collections.abc import Mapping, Sequence
from enum import StrEnum
from pathlib import Path
from typing import Any

from novel_authoring.author_control.book_profile import (
    load_effective_book_profile,
)
from novel_authoring.db.database import Database
from novel_authoring.domain.models import ContinuationMode
from novel_authoring.drafting.service import prepare_draft_task
from novel_authoring.edition import ensure_base_edition
from novel_authoring.original.genesis import (
    GenesisApplyError,
    accepted_foundation,
    apply_genesis_plan,
    build_genesis_apply_plan,
    export_accepted_foundation,
)
from novel_authoring.original.models import (
    AuthorInnovationIntent,
    CoreInnovationProposal,
    FoundationDevelopmentProposal,
    OriginalBookRequest,
    OriginalCreativeSemantics,
    OriginalFoundationConfirmation,
    OriginalReaderKernelAuthorOverrides,
    OriginalReaderKernelGenerationRequest,
    OriginalReaderKernelProposal,
    OriginalState,
    StoryFoundationProposal,
)
from novel_authoring.original.state import original_record
from novel_authoring.planning.boundary import build_boundary_packet
from novel_authoring.planning.contracts import build_chapter_contract
from novel_authoring.planning.innovation import resolve_innovation_control
from novel_authoring.progression.interpretation import (
    READER_EXPERIENCE_PRESETS,
    READER_EXPERIENCE_UI,
    ReaderExperienceAdjustment,
    ReaderExperienceStrength,
    adjust_reader_experience,
    apply_reader_experience_overrides,
)
from novel_authoring.progression.models import (
    ContractStatus,
    ExperiencePriority,
    ExplanationStyle,
    PrimaryFamily,
    ReaderExperience,
    ReaderExperienceContract,
    SerialForm,
    SettingSkin,
)
from novel_authoring.progression.service import (
    ContractRecord,
    ProgressionContractType,
    _confirm_contract_in_connection,
    _create_contract_proposal_in_connection,
    _reject_contract_in_connection,
    create_contract_proposal,
    effective_contract_records,
    list_contract_records,
    reject_contract,
)
from novel_authoring.serial_kernel.classification import (
    ensure_drive_support_metadata,
    market_category_label,
    narrative_drive_label,
)
from novel_authoring.serial_kernel.models import (
    MarketCategory,
    NarrativeDrive,
    NarrativeDriveContract,
)
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.operations import ensure_operation
from novel_authoring.storage.registry import (
    BookKind,
    BookRegistry,
    CreationMode,
)
from novel_authoring.utils import json_dumps, safe_book_id, utc_now
from novel_authoring.validation.service import validate_draft
from novel_authoring.workflows.approval import approval_preview, approve_draft
from novel_authoring.workflows.handoffs import (
    HandoffType,
    create_continuation_handoff,
    create_original_bootstrap_handoff,
    create_original_reader_interpretation_handoff,
    get_handoff,
    load_completed_handoff_result,
    mark_stale,
)


class OriginalWorkflowError(RuntimeError):
    pass


def _enum_options(enum_type: type[StrEnum]) -> list[dict[str, str]]:
    return [
        {"value": item.value, "label": item.value.replace("_", " ").title()}
        for item in enum_type
    ]


def _original_root(database: Database, book_id: str) -> Path:
    record = original_record(database, book_id)
    if record is None:
        raise OriginalWorkflowError("当前项目不是 ORIGINAL 小说")
    return Path(record.root)


def _original_dir(database: Database, book_id: str) -> Path:
    root = _original_root(database, book_id)
    path = BookLayout(root.parent).for_book(book_id).edition("base").analysis / "original"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _reader_kernel_author_overrides(
    database: Database, book_id: str
) -> tuple[OriginalReaderKernelAuthorOverrides, str]:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT reader_kernel_author_overrides_json, "
            "reader_kernel_author_instruction FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if row is None:
        raise OriginalWorkflowError("Original state 不存在")
    raw = row["reader_kernel_author_overrides_json"]
    overrides = (
        OriginalReaderKernelAuthorOverrides()
        if not raw
        else OriginalReaderKernelAuthorOverrides.model_validate_json(str(raw))
    )
    return overrides, str(row["reader_kernel_author_instruction"] or "")


def _assert_reader_kernel_overrides_applied(
    proposal: OriginalReaderKernelProposal,
    overrides: OriginalReaderKernelAuthorOverrides,
) -> None:
    sections = (
        ("reader_experience", proposal.reader_experience, overrides.reader_experience),
        ("market_category", proposal.market_category, overrides.market_category),
        ("narrative_drive", proposal.narrative_drive, overrides.narrative_drive),
        ("creative_semantics", proposal.creative_semantics, overrides.creative_semantics),
    )
    for section_name, actual, expected in sections:
        for field_name in type(expected).model_fields:
            expected_value = getattr(expected, field_name)
            if expected_value is None:
                continue
            if section_name == "reader_experience" and field_name == "experience_priorities":
                if not expected_value:
                    continue
                if not isinstance(actual, ReaderExperienceContract):
                    raise OriginalWorkflowError("Reader Experience Override 目标无效")
                for experience, priority in expected_value.items():
                    if actual.experience_priorities.get(experience) != priority:
                        raise OriginalWorkflowError(
                            "重新生成的 Reader Kernel 未遵守 Author Override："
                            f"reader_experience.experience_priorities.{experience.value}"
                        )
                continue
            if getattr(actual, field_name) != expected_value:
                raise OriginalWorkflowError(
                    "重新生成的 Reader Kernel 未遵守 Author Override："
                    f"{section_name}.{field_name}"
                )


def _normalize_reader_kernel_projections(
    proposal: OriginalReaderKernelProposal,
) -> OriginalReaderKernelProposal:
    """Keep Reader mirrors derived from their single structured authorities."""
    reader = proposal.reader_experience
    priorities = reader.experience_priorities
    drive = proposal.narrative_drive
    normalized_reader = reader.model_copy(
        update={
            "growth_centrality": priorities[ReaderExperience.PROGRESSION],
            "world_expansion_centrality": priorities[
                ReaderExperience.WORLD_EXPANSION
            ],
            "mystery_centrality": priorities[ReaderExperience.MYSTERY],
            "team_centrality": priorities[ReaderExperience.TEAM_GROWTH],
            "relationship_centrality": priorities[ReaderExperience.RELATIONSHIP],
            "theme_centrality": priorities[ReaderExperience.SOCIAL_THEME],
            "primary_narrative_drive": drive.primary_drive.value,
            "secondary_narrative_drives": [
                item.value for item in drive.secondary_drives
            ],
            "drive_priority_order": [item.value for item in drive.drive_mix],
        }
    )
    return proposal.model_copy(update={"reader_experience": normalized_reader})


def _confirmed_reader_kernel_projection(
    database: Database,
    book_id: str,
    proposal: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Overlay confirmed SQLite intent onto optional semantic-read metadata."""
    effective = effective_contract_records(database, book_id=book_id, edition_id="base")
    reader = effective.get(ProgressionContractType.READER_EXPERIENCE)
    market = effective.get(ProgressionContractType.MARKET_CATEGORY)
    drive = effective.get(ProgressionContractType.NARRATIVE_DRIVE)
    if reader is None or market is None or drive is None:
        return proposal
    with database.connect() as connection:
        state = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if state is None or not state["confirmed_creative_semantics_json"]:
        return proposal
    creative_semantics = OriginalCreativeSemantics.model_validate_json(
        str(state["confirmed_creative_semantics_json"])
    )
    return {
        **(proposal or {}),
        "reader_experience": reader.payload,
        "market_category": market.payload,
        "narrative_drive": drive.payload,
        "creative_semantics": creative_semantics.model_dump(mode="json"),
    }


def _update_registry(
    database: Database,
    book_id: str,
    *,
    state: OriginalState,
    title: str | None = None,
    latest_chapter: int | None = None,
) -> None:
    root = _original_root(database, book_id)
    layout = BookLayout(root.parent)
    registry = BookRegistry(layout)
    paths = layout.for_book(book_id)
    values = registry.read(book_id)
    values["original_state"] = state.value
    values["readiness_status"] = state.value
    values["updated_at"] = utc_now()
    if title is not None:
        values["title"] = title
    if latest_chapter is not None:
        values["latest_chapter"] = latest_chapter
    registry.write(paths, values)
    registry.write_readme(paths, values)


def _set_original_state(
    database: Database,
    book_id: str,
    state: OriginalState,
    *,
    current_proposal_version_id: str | None = None,
    accepted_apply_id: str | None = None,
) -> None:
    now = utc_now()
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO original_states(book_id, edition_id, state, "
            "current_proposal_version_id, accepted_apply_id, updated_at, version) "
            "VALUES (?, 'base', ?, ?, ?, ?, 1) "
            "ON CONFLICT(book_id, edition_id) DO UPDATE SET state=excluded.state, "
            "current_proposal_version_id=COALESCE(excluded.current_proposal_version_id, "
            "original_states.current_proposal_version_id), "
            "accepted_apply_id=COALESCE(excluded.accepted_apply_id, "
            "original_states.accepted_apply_id), updated_at=excluded.updated_at, "
            "version=original_states.version+1",
            (book_id, state.value, current_proposal_version_id, accepted_apply_id, now),
        )
    _update_registry(database, book_id, state=state)


def _current_proposal_row(database: Database, book_id: str) -> dict[str, Any] | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM original_proposal_versions WHERE book_id=? AND edition_id='base' "
            "AND status='CURRENT' ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    return None if row is None else dict(row)


def _current_innovation_row(database: Database, book_id: str) -> dict[str, Any] | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM original_innovation_versions WHERE book_id=? AND edition_id='base' "
            "AND status='CURRENT' ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    return None if row is None else dict(row)


def _current_development_row(database: Database, book_id: str) -> dict[str, Any] | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM original_development_versions WHERE book_id=? "
            "AND edition_id='base' AND status='CURRENT' "
            "ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    return None if row is None else dict(row)


def _reject_pending_development_kernel_contracts(
    database: Database, book_id: str
) -> None:
    for record in list_contract_records(database, book_id=book_id, edition_id="base"):
        if (
            record.status is ContractStatus.NEEDS_REVIEW
            and record.source.startswith("ORIGINAL_FOUNDATION_DEVELOPMENT:")
        ):
            reject_contract(database, record.contract_record_id)


def _selected_foundation(database: Database, book_id: str) -> dict[str, Any] | None:
    with database.connect() as connection:
        state = connection.execute(
            "SELECT selected_foundation_proposal_version_id, selected_foundation_id "
            "FROM original_states WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        if state is None or not state["selected_foundation_id"]:
            return None
        row = connection.execute(
            "SELECT proposal_json FROM original_proposal_versions "
            "WHERE proposal_version_id=? AND book_id=?",
            (state["selected_foundation_proposal_version_id"], book_id),
        ).fetchone()
    if row is None:
        raise OriginalWorkflowError("作者选择的 Story Foundation Proposal 不存在")
    proposal = StoryFoundationProposal.model_validate_json(str(row["proposal_json"]))
    selected_id = str(state["selected_foundation_id"])
    selected = next(
        (item for item in proposal.foundation_candidates if item.candidate_id == selected_id),
        None,
    )
    if selected is None:
        raise OriginalWorkflowError("作者选择的 Story Foundation 不属于冻结 Proposal")
    return {
        "proposal_version_id": str(state["selected_foundation_proposal_version_id"]),
        "selected_foundation_id": selected_id,
        "selected_candidate": selected.model_dump(mode="json"),
    }


def _confirmed_progression_kernel(
    database: Database,
    book_id: str,
    *,
    core_innovation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    effective = effective_contract_records(database, book_id=book_id, edition_id="base")
    reader = effective.get(ProgressionContractType.READER_EXPERIENCE)
    market = effective.get(ProgressionContractType.MARKET_CATEGORY)
    drive = effective.get(ProgressionContractType.NARRATIVE_DRIVE)
    if reader is None or market is None or drive is None:
        raise OriginalWorkflowError("必须先确认完整 Reader Kernel")
    with database.connect() as connection:
        state = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if state is None or not state["confirmed_creative_semantics_json"]:
        raise OriginalWorkflowError("必须先确认 Creative Semantics")
    creative_semantics = OriginalCreativeSemantics.model_validate_json(
        str(state["confirmed_creative_semantics_json"])
    )
    latest_by_type = {
        contract_type.value: record.model_dump(mode="json")
        for contract_type, record in effective.items()
    }
    kernel: dict[str, Any] = {
        "reader_experience": reader.model_dump(mode="json"),
        "creative_semantics": creative_semantics.model_dump(mode="json"),
        "contract_proposals": latest_by_type,
        "foundation_rules": [
            "Foundation 必须保留已确认的 Reader Experience、Primary Narrative Drive "
            "与 Creative Semantics",
            "三个 Foundation 候选必须共享并实质依赖作者选择的同一个 Core Innovation；"
            "selected Core 内部仍开放的问题可以被具体化，但不得重新打开已由 Core selection "
            "关闭的同等级机制分叉",
            "不得为追求候选差异新增未经 Seed、Creative Semantics 或 Core Intent "
            "需要的竞争性第二核心机制",
        ],
    }
    if core_innovation is not None:
        kernel["core_innovation"] = core_innovation
    return kernel


def prepare_original_core_innovation(database: Database, book_id: str) -> dict[str, Any]:
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创 premise 请求不存在")
    request = {
        **request_payload,
        "requested_stage": "CORE_INNOVATION_PROPOSAL",
        "progression_kernel": _confirmed_progression_kernel(database, book_id),
    }
    completed = _reconcile_completed_core_innovation(database, book_id)
    if completed is not None:
        return {**completed, "deduplicated": True, "proposal_imported": True}
    with database.connect() as connection:
        generating = connection.execute(
            "SELECT innovation_proposal_version_id, handoff_id "
            "FROM original_innovation_versions WHERE book_id=? AND edition_id='base' "
            "AND status='GENERATING' ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
        current = connection.execute(
            "SELECT * FROM original_innovation_versions WHERE book_id=? "
            "AND edition_id='base' AND status='CURRENT' "
            "ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    if generating is not None and generating["handoff_id"]:
        handoff = get_handoff(database, str(generating["handoff_id"]))
        if str(handoff.get("status")) in {
            "READY_FOR_CODEX",
            "CLAIMED",
            "RUNNING",
            "WAITING_FOR_USER",
        }:
            return {
                **handoff,
                "innovation_proposal_version_id": str(generating["innovation_proposal_version_id"]),
                "deduplicated": True,
            }
        now = utc_now()
        with database.connect() as connection:
            connection.execute(
                "UPDATE original_innovation_versions SET status='REJECTED', "
                "updated_at=?, archived_at=?, version=version+1 "
                "WHERE innovation_proposal_version_id=? AND status='GENERATING'",
                (now, now, str(generating["innovation_proposal_version_id"])),
            )
    if current is not None and current["handoff_id"]:
        current_handoff = get_handoff(database, str(current["handoff_id"]))
        return {
            **current_handoff,
            "innovation_proposal_version_id": str(current["innovation_proposal_version_id"]),
            "proposal_status": "CURRENT",
            "deduplicated": True,
            "proposal_imported": True,
        }
    handoff = create_original_bootstrap_handoff(
        database,
        book_id,
        requested_stage="CORE_INNOVATION_PROPOSAL",
        original_bootstrap_request=request,
    )
    now = utc_now()
    with database.connect() as connection:
        version_number = int(
            connection.execute(
                "SELECT COALESCE(MAX(version_number), 0) + 1 "
                "FROM original_innovation_versions WHERE book_id=? AND edition_id='base'",
                (book_id,),
            ).fetchone()[0]
        )
        proposal_version_id = f"innovation-proposal-{uuid.uuid4().hex}"
        connection.execute(
            "INSERT INTO original_innovation_versions("
            "innovation_proposal_version_id, book_id, edition_id, version_number, status, premise, "
            "handoff_id, proposal_json, created_at, updated_at, version"
            ") VALUES (?, ?, 'base', ?, 'GENERATING', ?, ?, '{}', ?, ?, 1)",
            (
                proposal_version_id,
                book_id,
                version_number,
                str(request.get("premise") or ""),
                str(handoff["handoff_id"]),
                now,
                now,
            ),
        )
        connection.execute(
            "UPDATE original_states SET state=?, updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (OriginalState.CORE_INNOVATION_GENERATING.value, now, book_id),
        )
    _update_registry(database, book_id, state=OriginalState.CORE_INNOVATION_GENERATING)
    return {
        **handoff,
        "innovation_proposal_version_id": proposal_version_id,
        "deduplicated": False,
    }


def prepare_original_reader_experience(database: Database, book_id: str) -> dict[str, Any]:
    completed = _reconcile_completed_original_reader_kernel(database, book_id)
    if completed is not None:
        return {**completed, "deduplicated": True, "proposal_imported": True}
    records = list_contract_records(database, book_id=book_id, edition_id="base")
    existing = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.READER_EXPERIENCE
            and record.status in {ContractStatus.NEEDS_REVIEW, ContractStatus.EFFECTIVE}
        ),
        None,
    )
    proposal_path = _original_dir(database, book_id) / "reader_experience.json"
    existing_proposal = _read_json(proposal_path)
    available_projection = _confirmed_reader_kernel_projection(
        database, book_id, existing_proposal
    )
    if existing is not None and available_projection is not None:
        return {
            "contract": existing.model_dump(mode="json"),
            "proposal": available_projection,
            "deduplicated": True,
            "canon_changed": False,
        }
    with database.connect() as connection:
        active = connection.execute(
            "SELECT handoff_id FROM workflow_handoffs WHERE book_id=? AND edition_id='base' "
            "AND handoff_type=? AND status IN ('READY_FOR_CODEX', 'CLAIMED', 'RUNNING', "
            "'WAITING_FOR_USER') ORDER BY created_at DESC LIMIT 1",
            (book_id, HandoffType.ORIGINAL_READER_INTERPRETATION.value),
        ).fetchone()
    if active is not None:
        return {**get_handoff(database, str(active["handoff_id"])), "deduplicated": True}
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创的一句话创意不存在")
    request = OriginalBookRequest.model_validate(request_payload)
    generation_request = OriginalReaderKernelGenerationRequest(
        **request.model_dump(mode="json")
    )
    handoff = create_original_reader_interpretation_handoff(
        database,
        book_id,
        original_reader_request=generation_request.model_dump(mode="json", exclude_none=True),
    )
    _set_original_state(database, book_id, OriginalState.READER_EXPERIENCE_GENERATING)
    return {
        **handoff,
        "deduplicated": False,
        "canon_changed": False,
    }


def regenerate_original_reader_kernel(
    database: Database,
    book_id: str,
    *,
    author_overrides: OriginalReaderKernelAuthorOverrides | Mapping[str, Any],
    author_instruction: str = "",
) -> dict[str, Any]:
    overrides = OriginalReaderKernelAuthorOverrides.model_validate(author_overrides)
    proposal_path = _original_dir(database, book_id) / "reader_experience.json"
    proposal_payload = _read_json(proposal_path)
    if proposal_payload is None:
        raise OriginalWorkflowError("Reader Kernel Proposal 不存在")
    proposal = OriginalReaderKernelProposal.model_validate(proposal_payload)
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创的一句话创意不存在")
    seed = OriginalBookRequest.model_validate(request_payload)
    with database.connect() as connection:
        state = connection.execute(
            "SELECT state, confirmed_creative_semantics_json, "
            "reader_kernel_overrides_need_regeneration FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        active = connection.execute(
            "SELECT handoff_id FROM workflow_handoffs WHERE book_id=? AND edition_id='base' "
            "AND handoff_type=? AND status IN ('READY_FOR_CODEX', 'CLAIMED', 'RUNNING', "
            "'WAITING_FOR_USER') ORDER BY created_at DESC LIMIT 1",
            (book_id, HandoffType.ORIGINAL_READER_INTERPRETATION.value),
        ).fetchone()
    if state is None or str(state["state"]) not in {
        OriginalState.READER_EXPERIENCE_REVIEW.value,
        OriginalState.READER_EXPERIENCE_GENERATING.value,
    }:
        raise OriginalWorkflowError("只有待审阅的 Reader Kernel Proposal 可以重新生成")
    if state["confirmed_creative_semantics_json"]:
        raise OriginalWorkflowError("Reader Kernel 已确认，不能重新生成 Proposal")
    if active is not None:
        raise OriginalWorkflowError("Reader Kernel Proposal 正在重新生成")
    generation_request = OriginalReaderKernelGenerationRequest(
        **seed.model_dump(mode="json"),
        generation_mode="REGENERATION",
        current_ai_proposal=proposal,
        author_overrides=overrides,
        author_instruction=author_instruction.strip(),
    )
    handoff = create_original_reader_interpretation_handoff(
        database,
        book_id,
        original_reader_request=generation_request.model_dump(mode="json", exclude_none=True),
    )
    now = utc_now()
    with database.connect() as connection:
        connection.execute(
            "UPDATE original_states SET state=?, reader_kernel_author_overrides_json=?, "
            "reader_kernel_author_instruction=?, reader_kernel_overrides_need_regeneration=1, "
            "updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (
                OriginalState.READER_EXPERIENCE_GENERATING.value,
                json_dumps(
                    overrides.model_dump(
                        mode="json", exclude_unset=True, exclude_none=True
                    )
                ),
                author_instruction.strip(),
                now,
                book_id,
            ),
        )
    _update_registry(
        database, book_id, state=OriginalState.READER_EXPERIENCE_GENERATING
    )
    return {
        **handoff,
        "author_overrides": overrides.model_dump(
            mode="json", exclude_unset=True, exclude_none=True
        ),
        "author_instruction": author_instruction.strip(),
        "deduplicated": False,
        "canon_changed": False,
    }


def save_original_reader_kernel_overrides(
    database: Database,
    book_id: str,
    *,
    author_overrides: OriginalReaderKernelAuthorOverrides | Mapping[str, Any],
    author_instruction: str = "",
) -> dict[str, Any]:
    overrides = OriginalReaderKernelAuthorOverrides.model_validate(author_overrides)
    with database.connect() as connection:
        state = connection.execute(
            "SELECT state, confirmed_creative_semantics_json, "
            "reader_kernel_overrides_need_regeneration FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        if state is None:
            raise OriginalWorkflowError("Original state 不存在")
        if (
            str(state["state"]) != OriginalState.READER_EXPERIENCE_REVIEW.value
            or state["confirmed_creative_semantics_json"]
        ):
            raise OriginalWorkflowError("只有待审阅的 Reader Kernel 可以保存 Author Overrides")
        connection.execute(
            "UPDATE original_states SET reader_kernel_author_overrides_json=?, "
            "reader_kernel_author_instruction=?, reader_kernel_overrides_need_regeneration=1, "
            "updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (
                json_dumps(
                    overrides.model_dump(
                        mode="json", exclude_unset=True, exclude_none=True
                    )
                ),
                author_instruction.strip(),
                utc_now(),
                book_id,
            ),
        )
    return {
        "author_overrides": overrides.model_dump(
            mode="json", exclude_unset=True, exclude_none=True
        ),
        "author_instruction": author_instruction.strip(),
        "saved": True,
        "canon_changed": False,
    }


def _reconcile_completed_original_reader_kernel(
    database: Database, book_id: str
) -> dict[str, Any] | None:
    with database.connect() as connection:
        confirmed = connection.execute(
            "SELECT confirmed_creative_semantics_json FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if confirmed is not None and confirmed["confirmed_creative_semantics_json"]:
        return None
    with database.connect() as connection:
        row = connection.execute(
            "SELECT handoff_id, status FROM workflow_handoffs "
            "WHERE book_id=? AND edition_id='base' AND handoff_type=? "
            "ORDER BY created_at DESC, rowid DESC LIMIT 1",
            (book_id, HandoffType.ORIGINAL_READER_INTERPRETATION.value),
        ).fetchone()
    if row is None:
        return None
    handoff = get_handoff(database, str(row["handoff_id"]))
    generation_payload = _read_json(
        Path(str(handoff["task_directory"])) / "input" / "original_request.json"
    ) or {}
    generation_mode = str(generation_payload.get("generation_mode") or "INITIAL")
    handoff_status = str(row["status"])
    if handoff_status == "FAILED" and generation_mode == "REGENERATION":
        _set_original_state(database, book_id, OriginalState.READER_EXPERIENCE_REVIEW)
        return None
    if handoff_status != "COMPLETED":
        return None
    proposal_path = _original_dir(database, book_id) / "reader_experience.json"
    if proposal_path.is_file() and generation_mode != "REGENERATION":
        return None
    try:
        return import_original_reader_kernel_proposal(
            database, book_id, str(row["handoff_id"])
        )
    except (OriginalWorkflowError, ValueError) as exc:
        if generation_mode != "REGENERATION":
            raise
        now = utc_now()
        reason = f"READER_KERNEL_IMPORT_FAILED: {exc}"
        with database.connect() as connection:
            connection.execute(
                "UPDATE workflow_handoffs SET status='FAILED', error_message=?, "
                "result_validation_json=? "
                "WHERE handoff_id=? AND status='COMPLETED'",
                (
                    reason,
                    json_dumps({"valid": False, "error": reason}),
                    str(row["handoff_id"]),
                ),
            )
            connection.execute(
                "UPDATE original_states SET state=?, updated_at=?, version=version+1 "
                "WHERE book_id=? AND edition_id='base'",
                (
                    OriginalState.READER_EXPERIENCE_REVIEW.value,
                    now,
                    book_id,
                ),
            )
        task_directory = Path(str(handoff["task_directory"]))
        _write_json(
            task_directory / "status.json",
            {
                "handoff_id": str(row["handoff_id"]),
                "status": "FAILED",
                "updated_at": now,
                "reason": reason,
            },
        )
        _write_json(task_directory / "error.json", {"error": reason, "created_at": now})
        _update_registry(database, book_id, state=OriginalState.READER_EXPERIENCE_REVIEW)
        return None


def import_original_reader_kernel_proposal(
    database: Database, book_id: str, handoff_id: str
) -> dict[str, Any]:
    handoff = get_handoff(database, handoff_id)
    if (
        str(handoff["book_id"]) != book_id
        or str(handoff["handoff_type"])
        != HandoffType.ORIGINAL_READER_INTERPRETATION.value
        or str(handoff["requested_stage"]).upper() != "READER_KERNEL_PROPOSAL"
    ):
        raise OriginalWorkflowError("handoff 不属于当前原创 Reader Kernel 任务")
    result = load_completed_handoff_result(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"])).resolve()
    expected = (task_directory / "artifacts" / "reader_kernel" / "proposal.json").resolve()
    returned = {
        (task_directory / Path(str(raw))).resolve()
        if not Path(str(raw)).is_absolute()
        else Path(str(raw)).resolve()
        for raw in result.get("artifact_paths", [])
    }
    if expected not in returned or not expected.is_file():
        raise OriginalWorkflowError("handoff 未返回 reader_kernel/proposal.json")
    proposal = OriginalReaderKernelProposal.model_validate_json(
        expected.read_text(encoding="utf-8")
    )
    proposal = _normalize_reader_kernel_projections(proposal)
    task = _read_json(task_directory / "input" / "task.json") or {}
    generation_payload = _read_json(
        task_directory / "input" / "original_request.json"
    ) or {}
    generation_request = OriginalReaderKernelGenerationRequest.model_validate(
        generation_payload
    )
    regenerating = generation_request.generation_mode == "REGENERATION"
    if regenerating:
        _assert_reader_kernel_overrides_applied(
            proposal, generation_request.author_overrides
        )
    frozen_ids = dict(
        (task.get("original_reader_interpretation") or {}).get("contract_ids") or {}
    )
    actual_ids = {
        "reader_experience_contract_id": proposal.reader_experience.contract_id,
        "market_category_metadata_id": proposal.market_category.metadata_id,
        "narrative_drive_contract_id": proposal.narrative_drive.drive_contract_id,
    }
    if actual_ids != frozen_ids:
        raise OriginalWorkflowError("Reader Kernel Proposal 必须使用 Python 冻结的 Contract IDs")
    existing = list_contract_records(database, book_id=book_id, edition_id="base")
    active_types = {
        record.contract_type
        for record in existing
        if record.status in {ContractStatus.NEEDS_REVIEW, ContractStatus.EFFECTIVE}
    }
    required_types = {
        ProgressionContractType.READER_EXPERIENCE,
        ProgressionContractType.MARKET_CATEGORY,
        ProgressionContractType.NARRATIVE_DRIVE,
    }
    if active_types & required_types:
        stored = _read_json(_original_dir(database, book_id) / "reader_experience.json")
        if stored == proposal.model_dump(mode="json"):
            return {
                "book_id": book_id,
                "handoff_id": handoff_id,
                "proposal": stored,
                "deduplicated": True,
                "canon_changed": False,
            }
        active_by_type = {
            record.contract_type: record
            for record in existing
            if record.status is ContractStatus.NEEDS_REVIEW
        }
        proposal_by_type = {
            ProgressionContractType.READER_EXPERIENCE: proposal.reader_experience,
            ProgressionContractType.MARKET_CATEGORY: proposal.market_category,
            ProgressionContractType.NARRATIVE_DRIVE: proposal.narrative_drive,
        }
        if regenerating and all(
            contract_type in active_by_type
            and active_by_type[contract_type].payload
            == payload.model_dump(mode="json")
            for contract_type, payload in proposal_by_type.items()
        ):
            stored = proposal.model_dump(mode="json")
            _write_json(_original_dir(database, book_id) / "reader_experience.json", stored)
            with database.connect() as connection:
                connection.execute(
                    "UPDATE original_states SET state=?, "
                    "reader_kernel_overrides_need_regeneration=0, updated_at=?, "
                    "version=version+1 WHERE book_id=? AND edition_id='base'",
                    (OriginalState.READER_EXPERIENCE_REVIEW.value, utc_now(), book_id),
                )
            _update_registry(database, book_id, state=OriginalState.READER_EXPERIENCE_REVIEW)
            return {
                "book_id": book_id,
                "handoff_id": handoff_id,
                "proposal": stored,
                "deduplicated": True,
                "canon_changed": False,
            }
        if not regenerating or any(
            record.status is ContractStatus.EFFECTIVE
            for record in existing
            if record.contract_type in required_types
        ):
            raise OriginalWorkflowError("当前原创项目已存在 Reader Kernel Proposal")
    created: list[ContractRecord] = []
    with database.connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        if regenerating:
            for record in existing:
                if (
                    record.contract_type in required_types
                    and record.status is ContractStatus.NEEDS_REVIEW
                ):
                    _reject_contract_in_connection(
                        connection, record.contract_record_id
                    )
        for contract_type, payload in (
            (ProgressionContractType.READER_EXPERIENCE, proposal.reader_experience),
            (ProgressionContractType.MARKET_CATEGORY, proposal.market_category),
            (ProgressionContractType.NARRATIVE_DRIVE, proposal.narrative_drive),
        ):
            created.append(
                _create_contract_proposal_in_connection(
                    connection,
                    book_id=book_id,
                    edition_id="base",
                    contract_type=contract_type,
                    payload=payload,
                    source=(
                        "ORIGINAL_READER_AUTHOR_REGENERATION"
                        if regenerating
                        else "ORIGINAL_READER_SEMANTIC_FIRST_READ"
                    ),
                )
            )
    stored = proposal.model_dump(mode="json")
    _write_json(_original_dir(database, book_id) / "reader_experience.json", stored)
    with database.connect() as connection:
        connection.execute(
            "UPDATE original_states SET state=?, "
            "reader_kernel_overrides_need_regeneration=0, updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (OriginalState.READER_EXPERIENCE_REVIEW.value, utc_now(), book_id),
        )
    _update_registry(database, book_id, state=OriginalState.READER_EXPERIENCE_REVIEW)
    return {
        "book_id": book_id,
        "handoff_id": handoff_id,
        "proposal": stored,
        "created_contract_proposals": [item.model_dump(mode="json") for item in created],
        "deduplicated": False,
        "canon_changed": False,
        "chapter_created": False,
    }


def confirm_original_reader_experience(
    database: Database,
    book_id: str,
    adjustment: ReaderExperienceAdjustment | str = ReaderExperienceAdjustment.CONFIRM,
    priority_overrides: Mapping[
        str, ReaderExperienceStrength | ExperiencePriority | str
    ]
    | None = None,
    primary_drive: NarrativeDrive | str | None = None,
    secondary_drives: Sequence[NarrativeDrive | str] | None = None,
    progression_engine_enabled: bool | None = None,
    creative_semantics: OriginalCreativeSemantics | Mapping[str, Any] | None = None,
    *,
    author_overrides: OriginalReaderKernelAuthorOverrides | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    selected_adjustment = (
        adjustment
        if isinstance(adjustment, ReaderExperienceAdjustment)
        else ReaderExperienceAdjustment(adjustment)
    )
    priority_overrides = priority_overrides or {}
    records = list_contract_records(database, book_id=book_id, edition_id="base")
    with database.connect() as connection:
        state = connection.execute(
            "SELECT state, confirmed_creative_semantics_json, "
            "reader_kernel_overrides_need_regeneration FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if state is None:
        raise OriginalWorkflowError("Original state 不存在")
    effective = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.READER_EXPERIENCE
            and record.status is ContractStatus.EFFECTIVE
        ),
        None,
    )
    drive_status = (
        ContractStatus.EFFECTIVE
        if effective is not None
        else ContractStatus.NEEDS_REVIEW
    )
    drive_record = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.NARRATIVE_DRIVE
            and record.status is drive_status
        ),
        None,
    )
    if drive_record is None:
        raise OriginalWorkflowError("Narrative Drive Proposal 不存在")
    market_record = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.MARKET_CATEGORY
            and record.status is drive_status
        ),
        None,
    )
    if market_record is None:
        raise OriginalWorkflowError("Market Category Proposal 不存在")
    current_drive = NarrativeDriveContract.model_validate(drive_record.payload)
    proposal_path = _original_dir(database, book_id) / "reader_experience.json"
    payload = _read_json(proposal_path)
    requested_creative_semantics = None
    if creative_semantics is not None:
        requested_creative_semantics = OriginalCreativeSemantics.model_validate(
            creative_semantics
        )
    elif (
        effective is None
        and payload is not None
        and payload.get("creative_semantics") is not None
    ):
        requested_creative_semantics = OriginalCreativeSemantics.model_validate(
            payload["creative_semantics"]
        )
    selected_primary = (
        current_drive.primary_drive
        if primary_drive is None
        else primary_drive
        if isinstance(primary_drive, NarrativeDrive)
        else NarrativeDrive(primary_drive)
    )
    selected_secondary = (
        list(current_drive.secondary_drives)
        if secondary_drives is None
        else [
            item if isinstance(item, NarrativeDrive) else NarrativeDrive(item)
            for item in secondary_drives
        ]
    )
    if selected_primary in selected_secondary:
        raise OriginalWorkflowError("Primary Drive 不得同时出现在 Secondary Drive")
    if len(selected_secondary) != len(set(selected_secondary)) or len(selected_secondary) > 4:
        raise OriginalWorkflowError("Secondary Drive 必须唯一且最多四个")
    selected_progression = (
        current_drive.progression_engine_enabled
        if progression_engine_enabled is None
        else progression_engine_enabled
    )
    if effective is not None:
        stored_creative_json = state["confirmed_creative_semantics_json"]
        if not stored_creative_json:
            raise OriginalWorkflowError("已确认的 Creative Semantics 不存在")
        confirmed_creative_semantics = OriginalCreativeSemantics.model_validate_json(
            str(stored_creative_json)
        )
        if requested_creative_semantics is None:
            requested_creative_semantics = confirmed_creative_semantics
        effective_reader = ReaderExperienceContract.model_validate(effective.payload)
        requested_reader = adjust_reader_experience(
            effective_reader,
            selected_adjustment,
        )
        requested_reader = apply_reader_experience_overrides(
            requested_reader,
            priority_overrides,
        )
        same_author_intent = (
            requested_reader.experience_priorities
            == effective_reader.experience_priorities
            and selected_primary == current_drive.primary_drive
            and selected_secondary == current_drive.secondary_drives
            and selected_progression == current_drive.progression_engine_enabled
            and requested_creative_semantics == confirmed_creative_semantics
        )
        if not same_author_intent:
            raise OriginalWorkflowError(
                "Reader Kernel 已确认；如需修改，请从新的创世/改写流程重新开始"
            )
        handoff = prepare_original_core_innovation(database, book_id)
        return {
            "reader_experience": effective.model_dump(mode="json"),
            "market_category": market_record.model_dump(mode="json"),
            "narrative_drive": drive_record.model_dump(mode="json"),
            "creative_semantics": confirmed_creative_semantics.model_dump(mode="json"),
            "handoff": handoff,
            "idempotent": True,
            "canon_changed": False,
        }
    if payload is None:
        raise OriginalWorkflowError("Reader Experience Proposal 不存在")
    if bool(state["reader_kernel_overrides_need_regeneration"]):
        raise OriginalWorkflowError("Author Overrides 已修改，请先重新生成 Reader Kernel Proposal")
    proposal = OriginalReaderKernelProposal.model_validate(payload)
    requested_overrides = (
        OriginalReaderKernelAuthorOverrides.model_validate(author_overrides)
        if author_overrides is not None
        else _reader_kernel_author_overrides(database, book_id)[0]
    )
    if requested_overrides.model_dump(exclude_none=True, exclude_defaults=True):
        _assert_reader_kernel_overrides_applied(proposal, requested_overrides)
    if requested_creative_semantics is None:
        raise OriginalWorkflowError("Creative Semantics Proposal 不存在")
    priorities = dict(current_drive.drive_priorities)
    promises = dict(current_drive.drive_promises)
    debts = dict(current_drive.drive_debt_types)
    for index, drive in enumerate([selected_primary, *selected_secondary]):
        priorities[drive] = max(priorities.get(drive, 0), 100 - index * 15)
        promises.setdefault(drive, [f"持续通过{narrative_drive_label(drive)}推动故事状态变化"])
        debts.setdefault(drive, [drive.value])
    confirmed_drive = ensure_drive_support_metadata(
        current_drive.model_copy(
            update={
                "primary_drive": selected_primary,
                "secondary_drives": selected_secondary,
                "drive_priorities": priorities,
                "drive_promises": promises,
                "drive_debt_types": debts,
                "progression_engine_enabled": selected_progression,
                "author_overrides": list(
                    dict.fromkeys(
                        [*current_drive.author_overrides, "AUTHOR_CONFIRMED_DRIVE"]
                    )
                ),
            }
        )
    )
    current = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.READER_EXPERIENCE
            and record.status is ContractStatus.NEEDS_REVIEW
        ),
        None,
    )
    if current is None:
        raise OriginalWorkflowError("没有待确认的 Reader Experience Proposal")
    adjusted = adjust_reader_experience(
        ReaderExperienceContract.model_validate(current.payload),
        selected_adjustment,
    )
    adjusted = apply_reader_experience_overrides(adjusted, priority_overrides)
    adjusted = adjusted.model_copy(
        update={
            "primary_narrative_drive": confirmed_drive.primary_drive.value,
            "secondary_narrative_drives": [
                item.value for item in confirmed_drive.secondary_drives
            ],
            "drive_priority_order": [item.value for item in confirmed_drive.drive_mix],
            "expected_drive_interactions": [
                f"{narrative_drive_label(confirmed_drive.primary_drive)}为主要驱动力"
            ],
        }
    )
    current_reader = ReaderExperienceContract.model_validate(current.payload)
    reader_to_confirm = current
    market_to_confirm = market_record
    drive_to_confirm = drive_record
    with database.connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        for record, label in (
            (current, "Reader Experience"),
            (market_record, "Market Category"),
            (drive_record, "Narrative Drive"),
        ):
            row = connection.execute(
                "SELECT status, payload_json FROM progression_contract_versions "
                "WHERE contract_record_id=?",
                (record.contract_record_id,),
            ).fetchone()
            if (
                row is None
                or str(row["status"]) != ContractStatus.NEEDS_REVIEW.value
                or json.loads(str(row["payload_json"])) != record.payload
            ):
                raise OriginalWorkflowError(
                    f"当前 {label} Proposal 已变化，请刷新后重试"
                )
        if adjusted != current_reader:
            reader_to_confirm = _create_contract_proposal_in_connection(
                connection,
                book_id=book_id,
                edition_id="base",
                contract_type=ProgressionContractType.READER_EXPERIENCE,
                payload=adjusted,
                source="AUTHOR_ADJUSTED_READER_EXPERIENCE",
            )
            _reject_contract_in_connection(connection, current.contract_record_id)
        if confirmed_drive != current_drive:
            drive_to_confirm = _create_contract_proposal_in_connection(
                connection,
                book_id=book_id,
                edition_id="base",
                contract_type=ProgressionContractType.NARRATIVE_DRIVE,
                payload=confirmed_drive,
                source="AUTHOR_CONFIRMED_NARRATIVE_DRIVE",
            )
            _reject_contract_in_connection(connection, drive_record.contract_record_id)
        confirmed_reader = _confirm_contract_in_connection(
            connection,
            reader_to_confirm.contract_record_id,
            effective_from_boundary=1,
            author_notes=f"作者选择：{selected_adjustment.value}",
        )
        confirmed_market_record = _confirm_contract_in_connection(
            connection,
            market_to_confirm.contract_record_id,
            effective_from_boundary=1,
            author_notes="作者在 Step 0 一并确认 Market Category",
        )
        confirmed_drive_record = _confirm_contract_in_connection(
            connection,
            drive_to_confirm.contract_record_id,
            effective_from_boundary=1,
            author_notes="作者在 Step 0 一并确认 Narrative Drive",
        )
        connection.execute(
            "UPDATE original_states SET confirmed_creative_semantics_json=?, "
            "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base'",
            (
                json_dumps(requested_creative_semantics.model_dump(mode="json")),
                utc_now(),
                book_id,
            ),
        )
    from novel_authoring.planning.aggregates import invalidate_planning_aggregates

    invalidate_planning_aggregates(database, book_id, "base")
    proposal = proposal.model_copy(
        update={
            "reader_experience": ReaderExperienceContract.model_validate(
                confirmed_reader.payload
            ),
            "market_category": type(proposal.market_category).model_validate(
                confirmed_market_record.payload
            ),
            "narrative_drive": confirmed_drive,
            "creative_semantics": requested_creative_semantics,
        }
    )
    projection_warning = None
    try:
        _write_json(proposal_path, proposal.model_dump(mode="json"))
    except OSError as exc:
        projection_warning = f"Reader Kernel projection 写入失败：{exc}"
    handoff = prepare_original_core_innovation(database, book_id)
    result = {
        "reader_experience": confirmed_reader.model_dump(mode="json"),
        "market_category": confirmed_market_record.model_dump(mode="json"),
        "narrative_drive": confirmed_drive_record.model_dump(mode="json"),
        "creative_semantics": requested_creative_semantics.model_dump(mode="json"),
        "handoff": handoff,
        "canon_changed": False,
    }
    if projection_warning is not None:
        result["warning"] = projection_warning
    return result


def create_original_book(
    layout: BookLayout,
    request: OriginalBookRequest | dict[str, Any],
    *,
    book_id: str | None = None,
) -> dict[str, Any]:
    data = (
        request
        if isinstance(request, OriginalBookRequest)
        else OriginalBookRequest.model_validate(request)
    )
    selected_id = safe_book_id(book_id or f"original-{uuid.uuid4().hex[:12]}")
    paths = layout.for_book(selected_id)
    if paths.root.exists():
        raise OriginalWorkflowError(f"原创项目已存在：{selected_id}")
    layout.library_root.mkdir(parents=True, exist_ok=True)
    paths = layout.ensure_book(selected_id)
    for directory in paths.edition("base").all_directories():
        directory.mkdir(parents=True, exist_ok=True)
    database = Database(paths.database)
    database.initialize()
    now = utc_now()
    working_title = "原创项目 · " + data.premise.strip().replace("\n", " ")[:24]
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO books(book_id, title, mode, source_root, workspace_root, "
            "created_at, updated_at, version) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
            (
                selected_id,
                working_title,
                ContinuationMode.CONSTRAINED_INNOVATION.value,
                str(paths.source),
                str(paths.root),
                now,
                now,
            ),
        )
    ensure_base_edition(database, selected_id)
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO original_states(book_id, edition_id, state, updated_at, version) "
            "VALUES (?, 'base', ?, ?, 1)",
            (selected_id, OriginalState.ORIGINAL_SEED.value, now),
        )
    registry = BookRegistry(layout)
    registry.ensure(
        selected_id,
        title=working_title,
        active_edition_id="base",
        readiness_status=OriginalState.ORIGINAL_SEED.value,
        book_kind=BookKind.AUTHOR,
        creation_mode=CreationMode.ORIGINAL,
    )
    values = registry.read(selected_id)
    values["original_state"] = OriginalState.ORIGINAL_SEED.value
    values["source_storage_mode"] = "NONE_ORIGINAL"
    values["source"] = {"root": "source", "files": []}
    values["source_files"] = []
    registry.write(paths, values)
    registry.write_readme(paths, values)
    request_path = _write_json(
        paths.edition("base").analysis / "original" / "request.json",
        data.model_dump(mode="json"),
    )
    reader_handoff = prepare_original_reader_experience(database, selected_id)
    return {
        "book_id": selected_id,
        "title": working_title,
        "database": str(paths.database),
        "request_path": str(request_path),
        "book_kind": BookKind.AUTHOR.value,
        "creation_mode": CreationMode.ORIGINAL.value,
        "original_state": OriginalState.READER_EXPERIENCE_GENERATING.value,
        "chapter_count": 0,
        "source_required": False,
        "reader_handoff": reader_handoff,
    }


def prepare_original_bootstrap(database: Database, book_id: str) -> dict[str, Any]:
    request_path = _original_dir(database, book_id) / "request.json"
    request_payload = _read_json(request_path)
    if request_payload is None:
        raise OriginalWorkflowError("原创 premise 请求不存在")
    core_innovation = _selected_innovation_intent(database, book_id)
    if core_innovation is None:
        raise OriginalWorkflowError("必须先确认 Core Innovation，才能生成 Story Foundation")
    progression_kernel = _confirmed_progression_kernel(
        database,
        book_id,
        core_innovation=core_innovation,
    )
    request = {
        **request_payload,
        "requested_stage": "STORY_FOUNDATION_PROPOSAL",
        "progression_kernel": progression_kernel,
    }
    completed = _reconcile_completed_original_bootstrap(database, book_id)
    if completed is not None:
        # A completed Codex handoff is already the user's requested result. Do
        # not classify it as a stale generator and create a replacement task.
        return {**completed, "deduplicated": True, "proposal_imported": True}
    with database.connect() as connection:
        generating = connection.execute(
            "SELECT proposal_version_id, handoff_id FROM original_proposal_versions "
            "WHERE book_id=? AND edition_id='base' AND status='GENERATING' "
            "ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
        state_row = connection.execute(
            "SELECT accepted_apply_id FROM original_states WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    has_accepted_foundation = bool(state_row and state_row["accepted_apply_id"])
    if generating is not None and generating["handoff_id"]:
        handoff = get_handoff(database, str(generating["handoff_id"]))
        if str(handoff.get("status")) in {
            "READY_FOR_CODEX",
            "CLAIMED",
            "RUNNING",
            "WAITING_FOR_USER",
        }:
            return {
                **handoff,
                "proposal_version_id": str(generating["proposal_version_id"]),
                "deduplicated": True,
            }
        with database.connect() as connection:
            connection.execute(
                "UPDATE original_proposal_versions SET status='REJECTED', "
                "updated_at=?, archived_at=?, version=version+1 "
                "WHERE proposal_version_id=? AND status='GENERATING'",
                (utc_now(), utc_now(), str(generating["proposal_version_id"])),
            )
    handoff = create_original_bootstrap_handoff(
        database,
        book_id,
        requested_stage="STORY_FOUNDATION_PROPOSAL",
        edition_id="base",
        original_bootstrap_request=request,
    )
    now = utc_now()
    with database.connect() as connection:
        version_number = int(
            connection.execute(
                "SELECT COALESCE(MAX(version_number), 0) + 1 "
                "FROM original_proposal_versions WHERE book_id=? AND edition_id='base'",
                (book_id,),
            ).fetchone()[0]
        )
        proposal_version_id = f"proposal-{uuid.uuid4().hex}"
        connection.execute(
            "INSERT INTO original_proposal_versions("
            "proposal_version_id, book_id, edition_id, version_number, status, premise, "
            "handoff_id, proposal_json, created_at, updated_at, version"
            ") VALUES (?, ?, 'base', ?, 'GENERATING', ?, ?, '{}', ?, ?, 1)",
            (
                proposal_version_id,
                book_id,
                version_number,
                str(request.get("premise") or ""),
                str(handoff["handoff_id"]),
                now,
                now,
            ),
        )
        if not has_accepted_foundation:
            connection.execute(
                "UPDATE original_states SET state=?, updated_at=?, version=version+1 "
                "WHERE book_id=? AND edition_id='base' AND accepted_apply_id IS NULL",
                (OriginalState.FOUNDATION_GENERATING.value, now, book_id),
            )
    if not has_accepted_foundation:
        _update_registry(database, book_id, state=OriginalState.FOUNDATION_GENERATING)
    return {**handoff, "proposal_version_id": proposal_version_id, "deduplicated": False}


def _reconcile_completed_core_innovation(
    database: Database, book_id: str
) -> dict[str, Any] | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT handoff_id FROM original_innovation_versions "
            "WHERE book_id=? AND edition_id='base' AND status='GENERATING' "
            "AND handoff_id IS NOT NULL ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    if row is None:
        return None
    handoff_id = str(row["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    if str(handoff.get("status")) != "COMPLETED":
        return None
    return import_original_core_innovation_proposal(database, book_id, handoff_id)


def import_original_core_innovation_proposal(
    database: Database, book_id: str, handoff_id: str
) -> dict[str, Any]:
    handoff = get_handoff(database, handoff_id)
    if (
        str(handoff["book_id"]) != book_id
        or str(handoff["handoff_type"]) != HandoffType.ORIGINAL_BOOK_BOOTSTRAP.value
        or str(handoff["requested_stage"]).upper() != "CORE_INNOVATION_PROPOSAL"
    ):
        raise OriginalWorkflowError("handoff 不属于当前原创项目的核心创意任务")
    result = load_completed_handoff_result(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"])).resolve()
    artifact_root = (task_directory / "artifacts").resolve()
    proposal_path: Path | None = None
    for raw_path in result.get("artifact_paths", []):
        candidate = Path(str(raw_path))
        if not candidate.is_absolute():
            candidate = task_directory / candidate
        candidate = candidate.resolve()
        try:
            candidate.relative_to(artifact_root)
        except ValueError:
            continue
        if (
            candidate.name == "proposal.json"
            and candidate.parent.name == "core_innovation"
            and candidate.is_file()
        ):
            proposal_path = candidate
            break
    if proposal_path is None:
        raise OriginalWorkflowError("handoff 未返回 core_innovation/proposal.json")
    proposal = CoreInnovationProposal.model_validate_json(
        proposal_path.read_text(encoding="utf-8")
    )
    handoff_request = _read_json(task_directory / "input" / "original_request.json") or {}
    expected_kernel = handoff_request.get("progression_kernel")
    if expected_kernel and proposal.kernel_contracts != expected_kernel:
        raise OriginalWorkflowError(
            "Core Innovation Proposal 不得修改已确认的 Reader Experience / Kernel"
        )
    innovation_ids = [item.innovation_id for item in proposal.innovation_candidates]
    if list(result.get("innovation_ids", [])) != innovation_ids:
        raise OriginalWorkflowError("handoff innovation_ids 与 Core Innovation Proposal 不一致")
    now = utc_now()
    proposal_payload = proposal.model_dump(mode="json")
    with database.connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        version_row = connection.execute(
            "SELECT * FROM original_innovation_versions WHERE book_id=? "
            "AND edition_id='base' AND handoff_id=?",
            (book_id, handoff_id),
        ).fetchone()
        if version_row is None:
            raise OriginalWorkflowError("找不到本次核心创意任务对应的方案版本")
        stored_status = str(version_row["status"])
        stored_payload = str(version_row["proposal_json"] or "")
        if stored_status in {"CURRENT", "READY"} and stored_payload not in {"", "{}"}:
            stored = CoreInnovationProposal.model_validate_json(stored_payload)
            state_row = connection.execute(
                "SELECT selected_primary_innovation_id FROM original_states "
                "WHERE book_id=? AND edition_id='base'",
                (book_id,),
            ).fetchone()
            resulting_state = (
                OriginalState.CORE_INNOVATION_REVIEW.value
                if state_row is None or not state_row["selected_primary_innovation_id"]
                else OriginalState.FOUNDATION_GENERATING.value
            )
            canonical_path = (
                _original_dir(database, book_id) / "core_innovation" / "proposal.json"
                if stored_status == "CURRENT"
                else _original_dir(database, book_id)
                / "core_innovation"
                / "versions"
                / f"{version_row['innovation_proposal_version_id']}.json"
            )
            return {
                "book_id": book_id,
                "handoff_id": handoff_id,
                "innovation_proposal_version_id": str(
                    version_row["innovation_proposal_version_id"]
                ),
                "proposal_status": stored_status,
                "original_state": resulting_state,
                "proposal_path": str(canonical_path),
                "proposal": stored.model_dump(mode="json"),
                "canon_changed": False,
                "chapter_created": False,
            }
        current = connection.execute(
            "SELECT innovation_proposal_version_id FROM original_innovation_versions "
            "WHERE book_id=? AND edition_id='base' AND status='CURRENT' LIMIT 1",
            (book_id,),
        ).fetchone()
        next_status = "CURRENT" if current is None else "READY"
        connection.execute(
            "UPDATE original_innovation_versions SET status=?, proposal_json=?, "
            "updated_at=?, ready_at=?, version=version+1 "
            "WHERE innovation_proposal_version_id=?",
            (
                next_status,
                json_dumps(proposal_payload),
                now,
                now,
                str(version_row["innovation_proposal_version_id"]),
            ),
        )
        state_row = connection.execute(
            "SELECT selected_primary_innovation_id FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        if current is None or state_row is None or not state_row["selected_primary_innovation_id"]:
            connection.execute(
                "UPDATE original_states SET state=?, current_innovation_proposal_version_id=?, "
                "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base'",
                (
                    OriginalState.CORE_INNOVATION_REVIEW.value,
                    str(version_row["innovation_proposal_version_id"]),
                    now,
                    book_id,
                ),
            )
        resulting_state = (
            OriginalState.CORE_INNOVATION_REVIEW.value
            if state_row is None or not state_row["selected_primary_innovation_id"]
            else OriginalState.FOUNDATION_GENERATING.value
        )
    version_id = str(version_row["innovation_proposal_version_id"])
    version_path = _write_json(
        _original_dir(database, book_id) / "core_innovation" / "versions" / f"{version_id}.json",
        proposal_payload,
    )
    canonical_path = version_path
    if next_status == "CURRENT":
        canonical_path = _write_json(
            _original_dir(database, book_id) / "core_innovation" / "proposal.json",
            proposal_payload,
        )
        _update_registry(database, book_id, state=OriginalState.CORE_INNOVATION_REVIEW)
    elif resulting_state == OriginalState.CORE_INNOVATION_REVIEW.value:
        _update_registry(database, book_id, state=OriginalState.CORE_INNOVATION_REVIEW)
    return {
        "book_id": book_id,
        "handoff_id": handoff_id,
        "innovation_proposal_version_id": version_id,
        "proposal_status": next_status,
        "original_state": resulting_state,
        "proposal_path": str(canonical_path),
        "proposal": proposal.model_dump(mode="json"),
        "canon_changed": False,
        "chapter_created": False,
    }


def load_original_innovation_proposal(
    database: Database, book_id: str
) -> CoreInnovationProposal | None:
    row = _current_innovation_row(database, book_id)
    if row is None:
        return None
    return CoreInnovationProposal.model_validate_json(str(row["proposal_json"]))


def select_original_core_innovation(
    database: Database,
    book_id: str,
    selection: AuthorInnovationIntent | dict[str, Any],
) -> dict[str, Any]:
    data = (
        selection
        if isinstance(selection, AuthorInnovationIntent)
        else AuthorInnovationIntent.model_validate(selection)
    )
    row = _current_innovation_row(database, book_id)
    if row is None:
        raise OriginalWorkflowError("尚无可选择的 Core Innovation Proposal")
    proposal = CoreInnovationProposal.model_validate_json(str(row["proposal_json"]))
    selected = next(
        (
            item
            for item in proposal.innovation_candidates
            if item.innovation_id == data.selected_primary_innovation_id
        ),
        None,
    )
    if selected is None:
        raise OriginalWorkflowError("选择的 Core Innovation 不属于当前提案")
    with database.connect() as connection:
        state = connection.execute(
            "SELECT current_innovation_proposal_version_id, selected_primary_innovation_id, "
            "optional_mix_notes, accepted_apply_id "
            "FROM original_states WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    existing_id = None if state is None else state["selected_primary_innovation_id"]
    existing_mix = "" if state is None else str(state["optional_mix_notes"] or "")
    if existing_id and state is not None and state["accepted_apply_id"]:
        raise OriginalWorkflowError("Genesis 已最终确认，不能从普通流程改选核心创意")
    same_selection = bool(
        state is not None
        and str(state["current_innovation_proposal_version_id"] or "")
        == str(row["innovation_proposal_version_id"])
        and str(existing_id or "") == data.selected_primary_innovation_id
        and existing_mix == data.optional_mix_notes
    )
    if same_selection:
        current_foundation = _current_proposal_row(database, book_id)
        if current_foundation is not None:
            return {
                "book_id": book_id,
                "innovation_intent": data.model_dump(mode="json"),
                "selected_candidate": selected.model_dump(mode="json"),
                "foundation_proposal": StoryFoundationProposal.model_validate_json(
                    str(current_foundation["proposal_json"])
                ).model_dump(mode="json"),
                "idempotent": True,
                "canon_changed": False,
            }
        return {
            "book_id": book_id,
            "innovation_intent": data.model_dump(mode="json"),
            "selected_candidate": selected.model_dump(mode="json"),
            "handoff": prepare_original_bootstrap(database, book_id),
            "idempotent": True,
            "canon_changed": False,
        }
    changed = bool(
        existing_id
        and (
            str(existing_id) != data.selected_primary_innovation_id
            or existing_mix != data.optional_mix_notes
        )
    )
    stale_handoff_ids: list[str] = []
    if changed:
        with database.connect() as connection:
            stale_handoff_ids = [
                str(item["handoff_id"])
                for item in connection.execute(
                    "SELECT handoff_id FROM workflow_handoffs WHERE book_id=? "
                    "AND requested_stage IN ('STORY_FOUNDATION_PROPOSAL', "
                    "'FOUNDATION_DEVELOPMENT_PROPOSAL') "
                    "AND status IN ('READY_FOR_CODEX', 'CLAIMED', 'RUNNING', "
                    "'WAITING_FOR_USER')",
                    (book_id,),
                ).fetchall()
            ]
    now = utc_now()
    with database.connect() as connection:
        if changed:
            connection.execute(
                "UPDATE original_proposal_versions SET status='ARCHIVED', archived_at=?, "
                "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base' "
                "AND status IN ('CURRENT', 'READY', 'GENERATING')",
                (now, now, book_id),
            )
            connection.execute(
                "UPDATE original_development_versions SET status='ARCHIVED', "
                "archived_at=?, updated_at=?, version=version+1 WHERE book_id=? "
                "AND edition_id='base' AND status IN ('CURRENT', 'READY', 'GENERATING')",
                (now, now, book_id),
            )
        connection.execute(
            "UPDATE original_states SET current_innovation_proposal_version_id=?, "
            "selected_primary_innovation_id=?, optional_mix_notes=?, "
            "current_proposal_version_id=CASE WHEN ? THEN NULL "
            "ELSE current_proposal_version_id END, "
            "selected_foundation_proposal_version_id=CASE WHEN ? THEN NULL "
            "ELSE selected_foundation_proposal_version_id END, "
            "selected_foundation_id=CASE WHEN ? THEN NULL ELSE selected_foundation_id END, "
            "current_development_proposal_version_id=CASE WHEN ? THEN NULL "
            "ELSE current_development_proposal_version_id END, "
            "state=?, updated_at=?, "
            "version=version+1 WHERE book_id=? AND edition_id='base'",
            (
                str(row["innovation_proposal_version_id"]),
                data.selected_primary_innovation_id,
                data.optional_mix_notes,
                changed,
                changed,
                changed,
                changed,
                OriginalState.FOUNDATION_GENERATING.value,
                now,
                book_id,
            ),
        )
    for handoff_id in stale_handoff_ids:
        mark_stale(database, handoff_id, "author explicitly reselected Core Innovation")
    if changed:
        _reject_pending_development_kernel_contracts(database, book_id)
    _update_registry(database, book_id, state=OriginalState.FOUNDATION_GENERATING)
    handoff = prepare_original_bootstrap(database, book_id)
    return {
        "book_id": book_id,
        "innovation_intent": data.model_dump(mode="json"),
        "selected_candidate": selected.model_dump(mode="json"),
        "handoff": handoff,
        "idempotent": False,
        "canon_changed": False,
    }


def _selected_innovation_intent(
    database: Database, book_id: str
) -> dict[str, Any] | None:
    row = _current_innovation_row(database, book_id)
    if row is None:
        return None
    proposal = CoreInnovationProposal.model_validate_json(str(row["proposal_json"]))
    with database.connect() as connection:
        state = connection.execute(
            "SELECT selected_primary_innovation_id, optional_mix_notes, "
            "current_innovation_proposal_version_id FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if state is None or not state["selected_primary_innovation_id"]:
        return None
    selected = next(
        (
            item
            for item in proposal.innovation_candidates
            if item.innovation_id == state["selected_primary_innovation_id"]
        ),
        None,
    )
    if selected is None:
        raise OriginalWorkflowError("作者选择的 Core Innovation 已不在当前 Proposal 中")
    if str(state["current_innovation_proposal_version_id"] or "") != str(
        row["innovation_proposal_version_id"]
    ):
        raise OriginalWorkflowError("作者选择的 Core Innovation 版本不是当前版本")
    return {
        "proposal_version_id": str(row["innovation_proposal_version_id"]),
        "selected_primary_innovation_id": str(state["selected_primary_innovation_id"]),
        "optional_mix_notes": str(state["optional_mix_notes"] or ""),
        "selected_candidate": selected.model_dump(mode="json"),
    }


def _reconcile_completed_original_bootstrap(
    database: Database, book_id: str
) -> dict[str, Any] | None:
    """Import a completed bootstrap handoff exactly once when it is observed.

    The Codex desktop client writes the handoff result files and status, while
    the Web app owns the proposal-version projection.  Reconciliation at the
    Web read/create boundaries closes that gap without creating a second
    handoff.  The importer itself is idempotent, so a page refresh and a
    concurrent status check are safe.
    """

    with database.connect() as connection:
        row = connection.execute(
            "SELECT handoff_id FROM original_proposal_versions "
            "WHERE book_id=? AND edition_id='base' AND status='GENERATING' "
            "AND handoff_id IS NOT NULL ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    if row is None:
        return None
    handoff_id = str(row["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    if str(handoff.get("status")) != "COMPLETED":
        return None
    return import_original_bootstrap_proposal(database, book_id, handoff_id)


def import_original_bootstrap_proposal(
    database: Database, book_id: str, handoff_id: str
) -> dict[str, Any]:
    handoff = get_handoff(database, handoff_id)
    if (
        str(handoff["book_id"]) != book_id
        or str(handoff["handoff_type"]) != HandoffType.ORIGINAL_BOOK_BOOTSTRAP.value
        or str(handoff["requested_stage"]).upper() != "STORY_FOUNDATION_PROPOSAL"
    ):
        raise OriginalWorkflowError("handoff 不属于当前原创项目的基础框架任务")
    result = load_completed_handoff_result(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"])).resolve()
    artifact_root = (task_directory / "artifacts").resolve()
    proposal_path: Path | None = None
    for raw_path in result.get("artifact_paths", []):
        candidate = Path(str(raw_path))
        if not candidate.is_absolute():
            candidate = task_directory / candidate
        candidate = candidate.resolve()
        try:
            candidate.relative_to(artifact_root)
        except ValueError:
            continue
        if candidate.name == "proposal.json" and candidate.is_file():
            proposal_path = candidate
            break
    if proposal_path is None:
        raise OriginalWorkflowError("handoff 未返回 story_foundation/proposal.json")
    proposal = StoryFoundationProposal.model_validate_json(
        proposal_path.read_text(encoding="utf-8")
    )
    handoff_request = _read_json(task_directory / "input" / "original_request.json") or {}
    expected_kernel = handoff_request.get("progression_kernel")
    if expected_kernel and proposal.kernel_contracts != expected_kernel:
        raise OriginalWorkflowError(
            "Foundation Proposal 必须原样携带已冻结的 Progression Kernel Contracts"
        )
    expected_innovation = (expected_kernel or {}).get("core_innovation")
    if expected_innovation is None:
        raise OriginalWorkflowError("Foundation Proposal 缺少已确认的 Core Innovation Boundary")
    if proposal.core_innovation_intent.model_dump(mode="json") != {
        "selected_primary_innovation_id": expected_innovation[
            "selected_primary_innovation_id"
        ],
        "optional_mix_notes": expected_innovation.get("optional_mix_notes", ""),
    }:
        raise OriginalWorkflowError("Foundation Proposal 不得替换作者已确认的 Core Innovation")
    foundation_ids = [item.candidate_id for item in proposal.foundation_candidates]
    if list(result.get("candidate_ids", [])) != foundation_ids:
        raise OriginalWorkflowError("handoff candidate_ids 与 Foundation Proposal 不一致")
    now = utc_now()
    proposal_payload = proposal.model_dump(mode="json")
    with database.connect() as connection:
        # Serialize imports for the same proposal version.  Without this
        # lock, two browser requests could both observe GENERATING and the
        # second one would downgrade a CURRENT version to READY.
        connection.execute("BEGIN IMMEDIATE")
        version_row = connection.execute(
            "SELECT * FROM original_proposal_versions WHERE book_id=? "
            "AND edition_id='base' AND handoff_id=?",
            (book_id, handoff_id),
        ).fetchone()
        if version_row is None:
            raise OriginalWorkflowError("找不到本次 AI 任务对应的方案版本")
        stored_status = str(version_row["status"])
        stored_payload = str(version_row["proposal_json"] or "")
        if stored_status == "CURRENT" and stored_payload in {"", "{}"}:
            raise OriginalWorkflowError("当前故事方案版本缺少内容，不能重复导入")
        if stored_status in {"CURRENT", "READY"} and stored_payload not in {"", "{}"}:
            try:
                stored_proposal = StoryFoundationProposal.model_validate_json(stored_payload)
            except ValueError as exc:
                if stored_status == "CURRENT":
                    raise OriginalWorkflowError("当前故事方案版本已损坏，不能重复导入") from exc
            else:
                state_row = connection.execute(
                    "SELECT state, accepted_apply_id FROM original_states "
                    "WHERE book_id=? AND edition_id='base'",
                    (book_id,),
                ).fetchone()
                resulting_state = (
                    str(state_row["state"])
                    if state_row is not None and state_row["accepted_apply_id"]
                    else OriginalState.FOUNDATION_REVIEW.value
                )
                version_id = str(version_row["proposal_version_id"])
                canonical_path = (
                    _original_dir(database, book_id) / "story_foundation" / "proposal.json"
                    if stored_status == "CURRENT"
                    else _original_dir(database, book_id)
                    / "story_foundation"
                    / "versions"
                    / f"{version_id}.json"
                )
                return {
                    "book_id": book_id,
                    "handoff_id": handoff_id,
                    "proposal_version_id": version_id,
                    "proposal_status": stored_status,
                    "original_state": resulting_state,
                    "proposal_path": str(canonical_path),
                    "proposal": stored_proposal.model_dump(mode="json"),
                    "canon_changed": False,
                    "chapter_created": False,
                }
        current = connection.execute(
            "SELECT proposal_version_id FROM original_proposal_versions "
            "WHERE book_id=? AND edition_id='base' AND status='CURRENT' LIMIT 1",
            (book_id,),
        ).fetchone()
        next_status = "CURRENT" if current is None else "READY"
        connection.execute(
            "UPDATE original_proposal_versions SET status=?, proposal_json=?, "
            "updated_at=?, ready_at=?, version=version+1 WHERE proposal_version_id=?",
            (
                next_status,
                json_dumps(proposal_payload),
                now,
                now,
                str(version_row["proposal_version_id"]),
            ),
        )
        state_row = connection.execute(
            "SELECT state, accepted_apply_id FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        if current is None or not (state_row and state_row["accepted_apply_id"]):
            connection.execute(
                "UPDATE original_states SET state=?, current_proposal_version_id=?, "
                "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base'",
                (
                    OriginalState.FOUNDATION_REVIEW.value,
                    str(version_row["proposal_version_id"]),
                    now,
                    book_id,
                ),
            )
        resulting_state = (
            str(state_row["state"])
            if state_row is not None and state_row["accepted_apply_id"]
            else OriginalState.FOUNDATION_REVIEW.value
        )
    version_id = str(version_row["proposal_version_id"])
    version_path = _write_json(
        _original_dir(database, book_id) / "story_foundation" / "versions" / f"{version_id}.json",
        proposal_payload,
    )
    canonical_path = version_path
    if next_status == "CURRENT":
        canonical_path = _write_json(
            _original_dir(database, book_id) / "story_foundation" / "proposal.json",
            proposal_payload,
        )
        _update_registry(database, book_id, state=OriginalState.FOUNDATION_REVIEW)
    elif resulting_state == OriginalState.FOUNDATION_REVIEW.value:
        _update_registry(database, book_id, state=OriginalState.FOUNDATION_REVIEW)
    return {
        "book_id": book_id,
        "handoff_id": handoff_id,
        "proposal_version_id": version_id,
        "proposal_status": next_status,
        "original_state": resulting_state,
        "proposal_path": str(canonical_path),
        "proposal": proposal.model_dump(mode="json"),
        "canon_changed": False,
        "chapter_created": False,
    }


def load_original_proposal(database: Database, book_id: str) -> StoryFoundationProposal | None:
    row = _current_proposal_row(database, book_id)
    if row is None:
        return None
    return StoryFoundationProposal.model_validate_json(str(row["proposal_json"]))


def compare_original_proposals(
    database: Database,
    book_id: str,
    proposal_version_id: str,
) -> dict[str, Any]:
    current = _current_proposal_row(database, book_id)
    with database.connect() as connection:
        target = connection.execute(
            "SELECT * FROM original_proposal_versions WHERE book_id=? "
            "AND edition_id='base' AND proposal_version_id=?",
            (book_id, proposal_version_id),
        ).fetchone()
    if current is None or target is None:
        raise OriginalWorkflowError("找不到可比较的故事方案版本")
    if str(target["status"]) not in {"READY", "CURRENT", "ARCHIVED"}:
        raise OriginalWorkflowError("这个故事方案尚未生成完成")
    return {
        "current_version_id": str(current["proposal_version_id"]),
        "target_version_id": str(target["proposal_version_id"]),
        "current": StoryFoundationProposal.model_validate_json(
            str(current["proposal_json"])
        ).model_dump(mode="json"),
        "target": StoryFoundationProposal.model_validate_json(
            str(target["proposal_json"])
        ).model_dump(mode="json"),
    }


def resolve_original_proposal_version(
    database: Database,
    book_id: str,
    proposal_version_id: str,
    *,
    action: str,
) -> dict[str, Any]:
    normalized = action.strip().upper()
    if normalized not in {"REPLACE_CURRENT", "KEEP_CURRENT", "REJECT"}:
        raise OriginalWorkflowError("方案操作无效")
    now = utc_now()
    with database.connect() as connection:
        target = connection.execute(
            "SELECT * FROM original_proposal_versions WHERE book_id=? "
            "AND edition_id='base' AND proposal_version_id=?",
            (book_id, proposal_version_id),
        ).fetchone()
        if target is None or str(target["status"]) not in {"READY", "CURRENT"}:
            raise OriginalWorkflowError("这个故事方案不能执行当前操作")
        if normalized == "REPLACE_CURRENT":
            state = connection.execute(
                "SELECT state, accepted_apply_id, current_proposal_version_id FROM original_states "
                "WHERE book_id=? AND edition_id='base'",
                (book_id,),
            ).fetchone()
            if (
                state is not None
                and str(state["current_proposal_version_id"] or "")
                == proposal_version_id
                and str(target["status"]) == "CURRENT"
            ):
                return {
                    "proposal_version_id": proposal_version_id,
                    "status": "CURRENT",
                    "current_changed": False,
                    "downstream_invalidated": False,
                    "accepted_foundation_changed": False,
                    "canon_changed": False,
                }
            if state is not None and state["accepted_apply_id"]:
                raise OriginalWorkflowError(
                    "Genesis 已最终确认，不能从普通流程替换 Story Foundation Proposal"
                )
            stale_handoff_ids = [
                str(item["handoff_id"])
                for item in connection.execute(
                    "SELECT handoff_id FROM workflow_handoffs WHERE book_id=? "
                    "AND requested_stage='FOUNDATION_DEVELOPMENT_PROPOSAL' "
                    "AND status IN ('READY_FOR_CODEX', 'CLAIMED', 'RUNNING', "
                    "'WAITING_FOR_USER')",
                    (book_id,),
                ).fetchall()
            ]
            connection.execute(
                "UPDATE original_proposal_versions SET status='ARCHIVED', archived_at=?, "
                "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base' "
                "AND status='CURRENT' AND proposal_version_id<>?",
                (now, now, book_id, proposal_version_id),
            )
            connection.execute(
                "UPDATE original_proposal_versions SET status='CURRENT', updated_at=?, "
                "archived_at=NULL, version=version+1 WHERE proposal_version_id=?",
                (now, proposal_version_id),
            )
            connection.execute(
                "UPDATE original_development_versions SET status='ARCHIVED', archived_at=?, "
                "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base' "
                "AND status IN ('CURRENT', 'READY', 'GENERATING')",
                (now, now, book_id),
            )
            connection.execute(
                "UPDATE original_states SET current_proposal_version_id=?, "
                "selected_foundation_proposal_version_id=NULL, selected_foundation_id=NULL, "
                "current_development_proposal_version_id=NULL, state=?, updated_at=?, "
                "version=version+1 WHERE book_id=? AND edition_id='base'",
                (
                    proposal_version_id,
                    OriginalState.FOUNDATION_REVIEW.value,
                    now,
                    book_id,
                ),
            )
            resulting_status = "CURRENT"
            accepted_apply_id = None if state is None else state["accepted_apply_id"]
        else:
            resulting_status = "ARCHIVED" if normalized == "KEEP_CURRENT" else "REJECTED"
            connection.execute(
                "UPDATE original_proposal_versions SET status=?, archived_at=?, "
                "updated_at=?, version=version+1 WHERE proposal_version_id=?",
                (resulting_status, now, now, proposal_version_id),
            )
            accepted_apply_id = None
    if normalized == "REPLACE_CURRENT":
        proposal = StoryFoundationProposal.model_validate_json(str(target["proposal_json"]))
        _write_json(
            _original_dir(database, book_id) / "story_foundation" / "proposal.json",
            proposal.model_dump(mode="json"),
        )
        if not accepted_apply_id:
            _update_registry(database, book_id, state=OriginalState.FOUNDATION_REVIEW)
        for handoff_id in stale_handoff_ids:
            mark_stale(database, handoff_id, "current Story Foundation Proposal replaced")
        _reject_pending_development_kernel_contracts(database, book_id)
    return {
        "proposal_version_id": proposal_version_id,
        "status": resulting_status,
        "current_changed": normalized == "REPLACE_CURRENT",
        "downstream_invalidated": normalized == "REPLACE_CURRENT",
        "accepted_foundation_changed": False,
        "canon_changed": False,
    }


def select_original_foundation(
    database: Database,
    book_id: str,
    selected_foundation_id: str,
) -> dict[str, Any]:
    proposal_row = _current_proposal_row(database, book_id)
    if proposal_row is None:
        raise OriginalWorkflowError("尚无可选择的 Story Foundation Proposal")
    proposal = StoryFoundationProposal.model_validate_json(
        str(proposal_row["proposal_json"])
    )
    selected = next(
        (
            item
            for item in proposal.foundation_candidates
            if item.candidate_id == selected_foundation_id
        ),
        None,
    )
    if selected is None:
        raise OriginalWorkflowError("选择的 Story Foundation 不属于当前 Proposal")
    with database.connect() as connection:
        state = connection.execute(
            "SELECT accepted_apply_id, selected_foundation_proposal_version_id, "
            "selected_foundation_id, current_development_proposal_version_id "
            "FROM original_states "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
    if state is not None and state["accepted_apply_id"]:
        raise OriginalWorkflowError("Genesis 已最终确认，不能从普通流程改选故事基础")
    same_selection = bool(
        state is not None
        and str(state["selected_foundation_proposal_version_id"] or "")
        == str(proposal_row["proposal_version_id"])
        and str(state["selected_foundation_id"] or "") == selected_foundation_id
    )
    if same_selection:
        existing_development = _current_development_row(database, book_id)
        if existing_development is not None:
            return {
                "book_id": book_id,
                "selected_foundation_id": selected_foundation_id,
                "selected_foundation": selected.model_dump(mode="json"),
                "development_proposal": FoundationDevelopmentProposal.model_validate_json(
                    str(existing_development["proposal_json"])
                ).model_dump(mode="json"),
                "idempotent": True,
                "canon_changed": False,
            }
        handoff = prepare_original_foundation_development(database, book_id)
        return {
            "book_id": book_id,
            "selected_foundation_id": selected_foundation_id,
            "selected_foundation": selected.model_dump(mode="json"),
            "handoff": handoff,
            "idempotent": True,
            "canon_changed": False,
        }
    with database.connect() as connection:
        stale_handoff_ids = [
            str(item["handoff_id"])
            for item in connection.execute(
                "SELECT handoff_id FROM workflow_handoffs WHERE book_id=? "
                "AND requested_stage='FOUNDATION_DEVELOPMENT_PROPOSAL' "
                "AND status IN ('READY_FOR_CODEX', 'CLAIMED', 'RUNNING', "
                "'WAITING_FOR_USER')",
                (book_id,),
            ).fetchall()
        ]
    now = utc_now()
    with database.connect() as connection:
        connection.execute(
            "UPDATE original_development_versions SET status='ARCHIVED', archived_at=?, "
            "updated_at=?, version=version+1 WHERE book_id=? AND edition_id='base' "
            "AND status IN ('CURRENT', 'READY', 'GENERATING')",
            (now, now, book_id),
        )
        connection.execute(
            "UPDATE original_states SET selected_foundation_proposal_version_id=?, "
            "selected_foundation_id=?, current_development_proposal_version_id=NULL, "
            "state=?, updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (
                str(proposal_row["proposal_version_id"]),
                selected_foundation_id,
                OriginalState.DEVELOPMENT_GENERATING.value,
                now,
                book_id,
            ),
        )
    for handoff_id in stale_handoff_ids:
        mark_stale(database, handoff_id, "author explicitly reselected Story Foundation")
    _reject_pending_development_kernel_contracts(database, book_id)
    _update_registry(database, book_id, state=OriginalState.DEVELOPMENT_GENERATING)
    handoff = prepare_original_foundation_development(database, book_id)
    return {
        "book_id": book_id,
        "selected_foundation_id": selected_foundation_id,
        "selected_foundation": selected.model_dump(mode="json"),
        "handoff": handoff,
        "idempotent": False,
        "canon_changed": False,
    }


def prepare_original_foundation_development(
    database: Database, book_id: str
) -> dict[str, Any]:
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    selected_core = _selected_innovation_intent(database, book_id)
    selected_foundation = _selected_foundation(database, book_id)
    if request_payload is None or selected_core is None or selected_foundation is None:
        raise OriginalWorkflowError("必须先确认 Reader Experience、Core 与 Story Foundation")
    completed = _reconcile_completed_foundation_development(database, book_id)
    if completed is not None:
        return {**completed, "deduplicated": True, "proposal_imported": True}
    with database.connect() as connection:
        generating = connection.execute(
            "SELECT development_proposal_version_id, handoff_id "
            "FROM original_development_versions WHERE book_id=? AND edition_id='base' "
            "AND status='GENERATING' ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    if generating is not None and generating["handoff_id"]:
        handoff = get_handoff(database, str(generating["handoff_id"]))
        if str(handoff["status"]) in {
            "READY_FOR_CODEX",
            "CLAIMED",
            "RUNNING",
            "WAITING_FOR_USER",
        }:
            return {
                **handoff,
                "development_proposal_version_id": str(
                    generating["development_proposal_version_id"]
                ),
                "deduplicated": True,
            }
    kernel = _confirmed_progression_kernel(
        database, book_id, core_innovation=selected_core
    )
    kernel_contract_ids = {
        "genre_contract_id": f"{book_id}-genre",
        "progression_contract_id": f"{book_id}-progression",
        "world_expansion_ladder_id": f"{book_id}-world-expansion",
    }
    request = {
        **request_payload,
        "requested_stage": "FOUNDATION_DEVELOPMENT_PROPOSAL",
        "progression_kernel": kernel,
        "selected_story_foundation": selected_foundation,
        "kernel_contract_ids": kernel_contract_ids,
    }
    handoff = create_original_bootstrap_handoff(
        database,
        book_id,
        requested_stage="FOUNDATION_DEVELOPMENT_PROPOSAL",
        edition_id="base",
        original_bootstrap_request=request,
    )
    now = utc_now()
    with database.connect() as connection:
        version_number = int(
            connection.execute(
                "SELECT COALESCE(MAX(version_number), 0) + 1 "
                "FROM original_development_versions WHERE book_id=? AND edition_id='base'",
                (book_id,),
            ).fetchone()[0]
        )
        version_id = f"development-{uuid.uuid4().hex}"
        connection.execute(
            "INSERT INTO original_development_versions("
            "development_proposal_version_id, book_id, edition_id, version_number, "
            "status, handoff_id, proposal_json, created_at, updated_at, version) "
            "VALUES (?, ?, 'base', ?, 'GENERATING', ?, '{}', ?, ?, 1)",
            (version_id, book_id, version_number, str(handoff["handoff_id"]), now, now),
        )
    return {
        **handoff,
        "development_proposal_version_id": version_id,
        "deduplicated": False,
    }


def _reconcile_completed_foundation_development(
    database: Database, book_id: str
) -> dict[str, Any] | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT handoff_id FROM original_development_versions "
            "WHERE book_id=? AND edition_id='base' AND status='GENERATING' "
            "AND handoff_id IS NOT NULL ORDER BY version_number DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    if row is None:
        return None
    handoff = get_handoff(database, str(row["handoff_id"]))
    if str(handoff["status"]) != "COMPLETED":
        return None
    return import_original_foundation_development(
        database, book_id, str(row["handoff_id"])
    )


def import_original_foundation_development(
    database: Database, book_id: str, handoff_id: str
) -> dict[str, Any]:
    handoff = get_handoff(database, handoff_id)
    if (
        str(handoff["book_id"]) != book_id
        or str(handoff["handoff_type"]) != HandoffType.ORIGINAL_BOOK_BOOTSTRAP.value
        or str(handoff["requested_stage"]).upper()
        != "FOUNDATION_DEVELOPMENT_PROPOSAL"
    ):
        raise OriginalWorkflowError("handoff 不属于当前 Foundation Development 任务")
    result = load_completed_handoff_result(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"])).resolve()
    expected = (
        task_directory / "artifacts" / "foundation_development" / "proposal.json"
    ).resolve()
    paths = []
    for raw_path in result.get("artifact_paths", []):
        path = Path(str(raw_path))
        paths.append(
            (task_directory / path).resolve()
            if not path.is_absolute()
            else path.resolve()
        )
    if expected not in paths or not expected.is_file():
        raise OriginalWorkflowError("handoff 未返回 foundation_development/proposal.json")
    proposal = FoundationDevelopmentProposal.model_validate_json(
        expected.read_text(encoding="utf-8")
    )
    selected_core = _selected_innovation_intent(database, book_id)
    selected_foundation = _selected_foundation(database, book_id)
    if selected_core is None or selected_foundation is None:
        raise OriginalWorkflowError("Foundation Development 的作者选择已不存在")
    expected_core = {
        "selected_primary_innovation_id": selected_core["selected_primary_innovation_id"],
        "optional_mix_notes": selected_core.get("optional_mix_notes", ""),
    }
    if proposal.core_innovation_intent.model_dump(mode="json") != expected_core:
        raise OriginalWorkflowError("Development Proposal 不得替换 Core Innovation")
    if proposal.selected_foundation_id != selected_foundation["selected_foundation_id"]:
        raise OriginalWorkflowError("Development Proposal 未绑定作者选择的 Foundation")
    if proposal.selected_foundation.model_dump(mode="json") != selected_foundation[
        "selected_candidate"
    ]:
        raise OriginalWorkflowError("Development Proposal 不得替换已选 Foundation 内容")
    handoff_request = _read_json(task_directory / "input" / "original_request.json") or {}
    expected_kernel = handoff_request.get("progression_kernel")
    if expected_kernel and proposal.kernel_contracts != expected_kernel:
        raise OriginalWorkflowError("Development Proposal 不得替换已确认的 Reader/Drive")
    frozen_ids = dict(handoff_request.get("kernel_contract_ids") or {})
    structured = proposal.kernel_contract_proposals
    actual_ids = {
        "genre_contract_id": structured.genre.genre_contract_id,
        "progression_contract_id": (
            None
            if structured.progression is None
            else structured.progression.progression_contract_id
        ),
        "world_expansion_ladder_id": structured.world_expansion.ladder_id,
    }
    expected_ids = {
        "genre_contract_id": frozen_ids.get("genre_contract_id"),
        "progression_contract_id": frozen_ids.get("progression_contract_id"),
        "world_expansion_ladder_id": frozen_ids.get("world_expansion_ladder_id"),
    }
    narrative_payload = dict(
        ((expected_kernel or {}).get("contract_proposals", {}).get("NARRATIVE_DRIVE") or {}).get(
            "payload", {}
        )
    )
    progression_enabled = bool(narrative_payload.get("progression_engine_enabled", False))
    if not progression_enabled:
        expected_ids["progression_contract_id"] = None
    if actual_ids != expected_ids:
        raise OriginalWorkflowError("Development Kernel Contract IDs 必须匹配 Python 冻结值")
    if progression_enabled != (structured.progression is not None):
        raise OriginalWorkflowError("Progression Contract 必须与确认的 Progression Engine 一致")
    reader_payload = dict((expected_kernel or {}).get("reader_experience", {}).get("payload", {}))
    if structured.genre.reader_experience_contract_id != reader_payload.get("contract_id"):
        raise OriginalWorkflowError("Genre Contract 必须绑定已确认的 Reader Experience")
    source = f"ORIGINAL_FOUNDATION_DEVELOPMENT:{handoff_id}"
    existing_sources = {
        record.contract_type
        for record in list_contract_records(database, book_id=book_id, edition_id="base")
        if record.source == source
    }
    for contract_type, contract in (
        (ProgressionContractType.GENRE, structured.genre),
        (ProgressionContractType.PROGRESSION, structured.progression),
        (ProgressionContractType.WORLD_EXPANSION, structured.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, structured.payoff_channel),
    ):
        if contract is None or contract_type in existing_sources:
            continue
        create_contract_proposal(
            database,
            book_id=book_id,
            edition_id="base",
            contract_type=contract_type,
            payload=contract,
            source=source,
        )
    now = utc_now()
    payload = proposal.model_dump(mode="json")
    with database.connect() as connection:
        row = connection.execute(
            "SELECT development_proposal_version_id FROM original_development_versions "
            "WHERE book_id=? AND handoff_id=?",
            (book_id, handoff_id),
        ).fetchone()
        if row is None:
            raise OriginalWorkflowError("找不到 Development Proposal 版本")
        version_id = str(row["development_proposal_version_id"])
        connection.execute(
            "UPDATE original_development_versions SET status='CURRENT', proposal_json=?, "
            "ready_at=?, updated_at=?, version=version+1 "
            "WHERE development_proposal_version_id=?",
            (json_dumps(payload), now, now, version_id),
        )
        connection.execute(
            "UPDATE original_states SET current_development_proposal_version_id=?, "
            "state=?, updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (version_id, OriginalState.DEVELOPMENT_REVIEW.value, now, book_id),
        )
    path = _write_json(
        _original_dir(database, book_id) / "foundation_development" / "proposal.json",
        payload,
    )
    _update_registry(database, book_id, state=OriginalState.DEVELOPMENT_REVIEW)
    return {
        "book_id": book_id,
        "handoff_id": handoff_id,
        "development_proposal_version_id": version_id,
        "proposal": payload,
        "proposal_path": str(path),
        "canon_changed": False,
        "chapter_created": False,
    }


def _current_genesis_contract_rows(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    development_handoff_id: str,
) -> dict[ProgressionContractType, sqlite3.Row]:
    rows: list[sqlite3.Row] = list(
        connection.execute(
            "SELECT * FROM progression_contract_versions WHERE book_id=? "
            "AND edition_id='base' AND status IN ('NEEDS_REVIEW', 'EFFECTIVE') "
            "ORDER BY version_number DESC",
            (book_id,),
        ).fetchall()
    )

    def select_one(
        contract_type: ProgressionContractType,
        *,
        sources: set[str] | None = None,
        required_status: ContractStatus | None = None,
    ) -> sqlite3.Row:
        matches = [
            row
            for row in rows
            if str(row["contract_type"]) == contract_type.value
            and (sources is None or str(row["source"]) in sources)
            and (required_status is None or str(row["status"]) == required_status.value)
        ]
        if len(matches) != 1:
            raise OriginalWorkflowError(
                f"当前 Genesis 缺少唯一的 {contract_type.value} Contract"
            )
        return matches[0]

    selected = {
        ProgressionContractType.READER_EXPERIENCE: select_one(
            ProgressionContractType.READER_EXPERIENCE,
            required_status=ContractStatus.EFFECTIVE,
        ),
        ProgressionContractType.MARKET_CATEGORY: select_one(
            ProgressionContractType.MARKET_CATEGORY,
            required_status=ContractStatus.EFFECTIVE,
        ),
        ProgressionContractType.NARRATIVE_DRIVE: select_one(
            ProgressionContractType.NARRATIVE_DRIVE,
            required_status=ContractStatus.EFFECTIVE,
        ),
    }
    drive = NarrativeDriveContract.model_validate_json(
        str(selected[ProgressionContractType.NARRATIVE_DRIVE]["payload_json"])
    )
    development_source = f"ORIGINAL_FOUNDATION_DEVELOPMENT:{development_handoff_id}"
    expected_development = {
        ProgressionContractType.GENRE,
        ProgressionContractType.WORLD_EXPANSION,
        ProgressionContractType.PAYOFF_CHANNEL,
    }
    if drive.progression_engine_enabled:
        expected_development.add(ProgressionContractType.PROGRESSION)
    for contract_type in expected_development:
        selected[contract_type] = select_one(
            contract_type,
            sources={development_source},
        )
    return selected


def _validate_current_genesis_selection(
    connection: sqlite3.Connection,
    *,
    book_id: str,
    development_proposal_version_id: str,
    development_handoff_id: str,
    development_proposal: FoundationDevelopmentProposal,
    selected_innovation: dict[str, Any],
    selected_foundation: dict[str, Any],
) -> None:
    state = connection.execute(
        "SELECT current_innovation_proposal_version_id, selected_primary_innovation_id, "
        "optional_mix_notes, current_proposal_version_id, "
        "selected_foundation_proposal_version_id, selected_foundation_id, "
        "current_development_proposal_version_id FROM original_states "
        "WHERE book_id=? AND edition_id='base'",
        (book_id,),
    ).fetchone()
    if state is None or (
        str(state["current_innovation_proposal_version_id"] or "")
        != selected_innovation["proposal_version_id"]
        or str(state["selected_primary_innovation_id"] or "")
        != selected_innovation["selected_primary_innovation_id"]
        or str(state["optional_mix_notes"] or "")
        != selected_innovation.get("optional_mix_notes", "")
        or str(state["current_proposal_version_id"] or "")
        != selected_foundation["proposal_version_id"]
        or str(state["selected_foundation_proposal_version_id"] or "")
        != selected_foundation["proposal_version_id"]
        or str(state["selected_foundation_id"] or "")
        != selected_foundation["selected_foundation_id"]
        or str(state["current_development_proposal_version_id"] or "")
        != development_proposal_version_id
    ):
        raise OriginalWorkflowError("Final Genesis Confirm 的作者选择已变化")
    innovation = connection.execute(
        "SELECT status, proposal_json FROM original_innovation_versions "
        "WHERE innovation_proposal_version_id=? AND book_id=? AND edition_id='base'",
        (selected_innovation["proposal_version_id"], book_id),
    ).fetchone()
    if innovation is None or str(innovation["status"]) != "CURRENT":
        raise OriginalWorkflowError("Final Genesis Confirm 的 Core Innovation 已变化")
    innovation_proposal = CoreInnovationProposal.model_validate_json(
        str(innovation["proposal_json"])
    )
    innovation_candidate = next(
        (
            candidate
            for candidate in innovation_proposal.innovation_candidates
            if candidate.innovation_id
            == selected_innovation["selected_primary_innovation_id"]
        ),
        None,
    )
    if innovation_candidate is None or innovation_candidate.model_dump(mode="json") != (
        selected_innovation["selected_candidate"]
    ):
        raise OriginalWorkflowError("Final Genesis Confirm 的 Core Innovation 已变化")
    foundation = connection.execute(
        "SELECT status, proposal_json FROM original_proposal_versions "
        "WHERE proposal_version_id=? AND book_id=? AND edition_id='base'",
        (selected_foundation["proposal_version_id"], book_id),
    ).fetchone()
    if foundation is None or str(foundation["status"]) != "CURRENT":
        raise OriginalWorkflowError("Final Genesis Confirm 的 Story Foundation 已变化")
    foundation_proposal = StoryFoundationProposal.model_validate_json(
        str(foundation["proposal_json"])
    )
    foundation_candidate = next(
        (
            candidate
            for candidate in foundation_proposal.foundation_candidates
            if candidate.candidate_id == selected_foundation["selected_foundation_id"]
        ),
        None,
    )
    if foundation_candidate is None or foundation_candidate.model_dump(mode="json") != (
        selected_foundation["selected_candidate"]
    ):
        raise OriginalWorkflowError("Final Genesis Confirm 的 Story Foundation 已变化")
    development = connection.execute(
        "SELECT status, handoff_id, proposal_json FROM original_development_versions "
        "WHERE development_proposal_version_id=? AND book_id=? AND edition_id='base'",
        (development_proposal_version_id, book_id),
    ).fetchone()
    if (
        development is None
        or str(development["status"]) != "CURRENT"
        or str(development["handoff_id"] or "") != development_handoff_id
        or FoundationDevelopmentProposal.model_validate_json(
            str(development["proposal_json"])
        )
        != development_proposal
    ):
        raise OriginalWorkflowError("Final Genesis Confirm 的 Development Proposal 已变化")


def confirm_original_foundation(
    database: Database,
    book_id: str,
    confirmation: OriginalFoundationConfirmation | dict[str, Any],
) -> dict[str, Any]:
    data = (
        confirmation
        if isinstance(confirmation, OriginalFoundationConfirmation)
        else OriginalFoundationConfirmation.model_validate(confirmation)
    )
    proposal_row = _current_development_row(database, book_id)
    if proposal_row is None:
        raise OriginalWorkflowError("Foundation Development Proposal 尚未完成")
    proposal = FoundationDevelopmentProposal.model_validate_json(
        str(proposal_row["proposal_json"])
    )
    selected_innovation = _selected_innovation_intent(database, book_id)
    if selected_innovation is None:
        raise OriginalWorkflowError("必须先确认 Core Innovation，才能确认故事基础")
    if proposal.core_innovation_intent.model_dump(mode="json") != {
        "selected_primary_innovation_id": selected_innovation[
            "selected_primary_innovation_id"
        ],
        "optional_mix_notes": selected_innovation.get("optional_mix_notes", ""),
    }:
        raise OriginalWorkflowError("当前故事基础方案没有沿用作者确认的 Core Innovation")
    selected_foundation = _selected_foundation(database, book_id)
    if (
        selected_foundation is None
        or proposal.selected_foundation_id
        != selected_foundation["selected_foundation_id"]
        or data.selected_foundation_id != proposal.selected_foundation_id
    ):
        raise OriginalWorkflowError("最终确认必须使用当前作者选择的 Story Foundation")
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创的一句话创意不存在")
    request = OriginalBookRequest.model_validate(request_payload)
    try:
        plan = build_genesis_apply_plan(
            proposal_version_id=str(selected_foundation["proposal_version_id"]),
            proposal=proposal,
            confirmation=data,
            request=request,
        )
        development_version_id = str(
            proposal_row["development_proposal_version_id"]
        )
        development_handoff_id = str(proposal_row["handoff_id"] or "")
        if not development_handoff_id:
            raise OriginalWorkflowError("当前 Development Proposal 缺少来源 handoff")
        selected_contract_ids: set[str] = set()
        with database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            _validate_current_genesis_selection(
                connection,
                book_id=book_id,
                development_proposal_version_id=development_version_id,
                development_handoff_id=development_handoff_id,
                development_proposal=proposal,
                selected_innovation=selected_innovation,
                selected_foundation=selected_foundation,
            )
            contract_rows = _current_genesis_contract_rows(
                connection,
                book_id=book_id,
                development_handoff_id=development_handoff_id,
            )
            selected_contract_ids = {
                str(row["contract_record_id"]) for row in contract_rows.values()
            }
            applied = apply_genesis_plan(
                database,
                book_id,
                plan,
                connection=connection,
            )
            if applied["idempotent"] and any(
                str(row["status"]) != ContractStatus.EFFECTIVE.value
                for row in contract_rows.values()
            ):
                raise OriginalWorkflowError(
                    "已确认的 Genesis 缺少对应 EFFECTIVE Runtime Kernel Contract"
                )
            for row in contract_rows.values():
                if str(row["status"]) == ContractStatus.NEEDS_REVIEW.value:
                    _confirm_contract_in_connection(
                        connection,
                        str(row["contract_record_id"]),
                        effective_from_boundary=1,
                        author_notes="作者在 Foundation 最终预览中一并确认",
                    )
            if not applied["idempotent"]:
                connection.execute(
                    "UPDATE planning_aggregates SET status='STALE', stale_reason=?, "
                    "invalidated_at=? WHERE book_id=? AND edition_id='base' "
                    "AND status='ACTIVE'",
                    (
                        "author confirmed Original Genesis runtime kernel",
                        utc_now(),
                        book_id,
                    ),
                )
    except (GenesisApplyError, OriginalWorkflowError, sqlite3.IntegrityError, ValueError) as exc:
        raise OriginalWorkflowError(str(exc)) from exc
    confirmed_contracts = [
        record.model_dump(mode="json")
        for record in list_contract_records(database, book_id=book_id, edition_id="base")
        if record.contract_record_id in selected_contract_ids
    ]
    accepted_path = _original_dir(database, book_id) / "story_foundation" / "accepted.json"
    export_warning: str | None = None
    try:
        export_accepted_foundation(database, book_id, accepted_path)
        _update_registry(
            database,
            book_id,
            state=OriginalState.FOUNDATION_READY,
            title=plan.selected_title,
        )
    except OSError as exc:
        export_warning = f"数据库已确认；作者可读导出稍后可重新生成：{exc}"
    accepted = accepted_foundation(database, book_id)
    if accepted is None:
        raise OriginalWorkflowError("故事基础事务已完成，但无法读取确认结果")
    return {
        "book_id": book_id,
        "original_state": OriginalState.FOUNDATION_READY.value,
        "accepted_path": str(accepted_path),
        "apply_id": applied["apply_id"],
        "idempotent": applied["idempotent"],
        "export_warning": export_warning,
        "genesis": {
            "task_id": accepted["genesis_task_id"],
            "candidates": plan.first_chapter_candidates,
        },
        "chapter_created": False,
        "canon_changed": False,
        "confirmed_kernel_contracts": confirmed_contracts,
    }


def select_first_chapter_candidate(
    database: Database, book_id: str, candidate_id: str
) -> dict[str, Any]:
    accepted = accepted_foundation(database, book_id)
    if accepted is None:
        raise OriginalWorkflowError("必须先确认故事基础方案")
    records = list_contract_records(database, book_id=book_id, edition_id="base")
    if records:
        effective_types = {
            record.contract_type
            for record in records
            if record.status is ContractStatus.EFFECTIVE
        }
        required = {
            ProgressionContractType.READER_EXPERIENCE,
            ProgressionContractType.NARRATIVE_DRIVE,
        }
        if not required.issubset(effective_types):
            raise OriginalWorkflowError("必须先确认 Reader 与 Narrative Drive Contract")
    task_id = str(accepted.get("genesis_task_id") or "")
    boundary = build_boundary_packet(database, book_id, edition_id="base")
    boundary_payload = json.loads(Path(str(boundary["json_path"])).read_text(encoding="utf-8"))
    innovation, _ = resolve_innovation_control(database, book_id)
    profile = load_effective_book_profile(database, book_id, "base")
    operation = ensure_operation(
        database,
        book_id,
        "base",
        task_id,
        "GENESIS_PLAN",
        {"boundary_packet_id": boundary["packet_id"], "chapter": 1},
    )
    if operation is None:
        raise OriginalWorkflowError("原创项目必须使用作品目录内的创作任务空间")
    _write_json(
        operation.input / "task.json",
        {
            "task_id": task_id,
            "task_type": "genesis_plan",
            "book_id": book_id,
            "edition_id": "base",
            "boundary_packet_id": boundary["packet_id"],
            "boundary_path": boundary["json_path"],
            "innovation_control": innovation.model_dump(mode="json"),
            "narrative_portfolio_snapshot": boundary_payload.get("narrative_portfolio"),
            "truth_reveal": {
                "target_chapter_ordinal": 1,
                "active_author_truths": boundary_payload.get("active_author_truths", []),
                "reveal_agenda": boundary_payload.get("reveal_agenda", {}),
            },
            "effective_book_profile": profile,
            "aggregate_id": None,
            "created_at": utc_now(),
            "information_status": "CANDIDATE",
        },
    )
    with database.connect() as connection:
        selected_row = connection.execute(
            "SELECT candidate_id FROM candidate_plans WHERE book_id=? AND edition_id='base' "
            "AND task_id=? AND selection_status='SELECTED'",
            (book_id, task_id),
        ).fetchone()
        if selected_row is not None:
            raise OriginalWorkflowError("第一章候选已经选择，不能重复创建合同与 Draft handoff")
        row = connection.execute(
            "SELECT candidate_id FROM candidate_plans WHERE book_id=? AND edition_id='base' "
            "AND task_id=? AND candidate_id=? AND status='CANDIDATE'",
            (book_id, task_id, candidate_id),
        ).fetchone()
        if row is None:
            raise OriginalWorkflowError("首章候选不存在或已失效")
        connection.execute(
            "UPDATE candidate_plans SET selection_status='NOT_SELECTED' "
            "WHERE book_id=? AND edition_id='base' AND task_id=?",
            (book_id, task_id),
        )
        connection.execute(
            "UPDATE candidate_plans SET selection_status='SELECTED' "
            "WHERE book_id=? AND edition_id='base' AND candidate_id=?",
            (book_id, candidate_id),
        )
    contract = build_chapter_contract(database, book_id, candidate_id, edition_id="base")
    draft_task = prepare_draft_task(
        database, book_id, str(contract["contract_id"]), edition_id="base"
    )
    handoff = create_continuation_handoff(
        database,
        book_id,
        edition_id="base",
        requested_stage="DRAFT_AND_VALIDATE",
        prepared_draft_task=draft_task,
        author_goal=(
            "这是原创小说 Genesis 首章。只使用已经选择的 candidate_id="
            f"{candidate_id}、contract_id={contract['contract_id']} 与 draft task_id="
            f"{draft_task['task_id']}；完成正文导入和十项校验，停在 VALIDATED。"
        ),
    )
    _set_original_state(database, book_id, OriginalState.FIRST_CHAPTER_DRAFTING)
    return {
        "book_id": book_id,
        "candidate_id": candidate_id,
        "contract": contract,
        "draft_task": draft_task,
        "handoff": handoff,
        "canon_changed": False,
    }


def validate_original_draft(database: Database, book_id: str, draft_id: str) -> dict[str, Any]:
    preview = approval_preview(database, book_id, draft_id, edition_id="base")
    if int(str(preview["chapter"])) != 1:
        raise OriginalWorkflowError("原创 Genesis 校验只接受第一章合同")
    bundle = validate_draft(database, book_id, draft_id, edition_id="base")
    if bundle.passed:
        _set_original_state(database, book_id, OriginalState.FIRST_CHAPTER_VALIDATED)
    return bundle.model_dump(mode="json")


def approve_original_first_chapter(
    database: Database, book_id: str, draft_id: str, confirmation: str
) -> dict[str, Any]:
    preview = approval_preview(database, book_id, draft_id, edition_id="base")
    if int(str(preview["chapter"])) != 1:
        raise OriginalWorkflowError("原创 Genesis 批准只接受第一章合同")
    result = approve_draft(
        database,
        book_id,
        draft_id,
        confirmation=confirmation,
        edition_id="base",
    )
    _set_original_state(
        database,
        book_id,
        OriginalState.WRITING_READY,
    )
    _update_registry(
        database,
        book_id,
        state=OriginalState.WRITING_READY,
        latest_chapter=1,
    )
    return {**result, "original_state": OriginalState.WRITING_READY.value}


def original_overview(database: Database, book_id: str) -> dict[str, Any]:
    record = original_record(database, book_id)
    if record is None:
        raise OriginalWorkflowError("当前项目不是 ORIGINAL 小说")
    _reconcile_completed_original_reader_kernel(database, book_id)
    _reconcile_completed_core_innovation(database, book_id)
    _reconcile_completed_original_bootstrap(database, book_id)
    _reconcile_completed_foundation_development(database, book_id)
    innovation_proposal = load_original_innovation_proposal(database, book_id)
    proposal = load_original_proposal(database, book_id)
    development_row = _current_development_row(database, book_id)
    development_proposal = (
        None
        if development_row is None
        else FoundationDevelopmentProposal.model_validate_json(
            str(development_row["proposal_json"])
        )
    )
    accepted = accepted_foundation(database, book_id)
    kernel_records = list_contract_records(database, book_id=book_id, edition_id="base")
    reader_proposal = _read_json(
        _original_dir(database, book_id) / "reader_experience.json"
    )
    reader_proposal = _confirmed_reader_kernel_projection(
        database, book_id, reader_proposal
    )
    with database.connect() as connection:
        state_row = connection.execute(
            "SELECT state, current_innovation_proposal_version_id, "
            "selected_primary_innovation_id, optional_mix_notes, "
            "selected_foundation_proposal_version_id, selected_foundation_id, "
            "current_development_proposal_version_id, "
            "reader_kernel_overrides_need_regeneration "
            "FROM original_states WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        proposal_versions = [
            dict(row)
            for row in connection.execute(
                "SELECT proposal_version_id, version_number, status, handoff_id, "
                "created_at, updated_at, ready_at FROM original_proposal_versions "
                "WHERE book_id=? AND edition_id='base' ORDER BY version_number DESC",
                (book_id,),
            ).fetchall()
        ]
        innovation_proposal_versions = [
            dict(row)
            for row in connection.execute(
                "SELECT innovation_proposal_version_id, version_number, status, handoff_id, "
                "created_at, updated_at, ready_at FROM original_innovation_versions "
                "WHERE book_id=? AND edition_id='base' ORDER BY version_number DESC",
                (book_id,),
            ).fetchall()
        ]
        development_proposal_versions = [
            dict(row)
            for row in connection.execute(
                "SELECT development_proposal_version_id, version_number, status, handoff_id, "
                "created_at, updated_at, ready_at FROM original_development_versions "
                "WHERE book_id=? AND edition_id='base' ORDER BY version_number DESC",
                (book_id,),
            ).fetchall()
        ]
        latest_task = "" if accepted is None else str(accepted.get("genesis_task_id") or "")
        candidates = [
            dict(row)
            for row in connection.execute(
                "SELECT candidate_id, rank, selection_status, plan_json FROM candidate_plans "
                "WHERE book_id=? AND edition_id='base' AND task_id=? ORDER BY rank",
                (book_id, latest_task),
            ).fetchall()
        ]
        for item in candidates:
            plan = json.loads(str(item.pop("plan_json")))
            item.update(
                {
                    "title": plan.get("title"),
                    "summary": plan.get("summary"),
                    "reader_question": plan.get("reader_question"),
                    "protagonist_action": plan.get("protagonist_strategy"),
                    "required_cost": plan.get("required_cost"),
                    "irreversible_change": plan.get("required_irreversible_change"),
                    "ending_state": plan.get("ending_state"),
                    "future_space": plan.get("ending_state"),
                    "author_goals": plan.get("causal_sources") or [],
                    "main_risk": plan.get("risk_form"),
                    "lens": plan.get("lens"),
                }
            )
        drafts = [
            dict(row)
            for row in connection.execute(
                "SELECT draft_id, status, chapter_title, file_path, created_at FROM drafts "
                "WHERE book_id=? AND edition_id='base' ORDER BY created_at DESC",
                (book_id,),
            ).fetchall()
        ]
        chapter_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM chapters WHERE book_id=?", (book_id,)
            ).fetchone()[0]
        )
        handoffs = [
            dict(row)
            for row in connection.execute(
                "SELECT handoff_id, handoff_type, requested_stage, status, prompt_path, "
                "created_at FROM workflow_handoffs WHERE book_id=? AND edition_id='base' "
                "ORDER BY created_at DESC LIMIT 5",
                (book_id,),
            ).fetchall()
        ]
    state_value = (
        str(state_row["state"])
        if state_row is not None
        else record.original_state or OriginalState.ORIGINAL_SEED.value
    )
    innovation_selection = None
    if state_row is not None and state_row["selected_primary_innovation_id"]:
        innovation_selection = {
            "selected_primary_innovation_id": str(
                state_row["selected_primary_innovation_id"]
            ),
            "optional_mix_notes": str(state_row["optional_mix_notes"] or ""),
            "proposal_version_id": str(
                state_row["current_innovation_proposal_version_id"] or ""
            ),
        }
    foundation_selection = None
    if state_row is not None and state_row["selected_foundation_id"]:
        foundation_selection = {
            "proposal_version_id": str(
                state_row["selected_foundation_proposal_version_id"] or ""
            ),
            "selected_foundation_id": str(state_row["selected_foundation_id"]),
        }
    reader_payload = (
        dict(reader_proposal.get("reader_experience", {}))
        if reader_proposal is not None
        else {}
    )
    narrative_display = (
        dict(reader_proposal.get("narrative_drive", {}))
        if reader_proposal is not None
        else {}
    )
    drive_contract_display = narrative_display
    market_display = (
        dict(reader_proposal.get("market_category", {}))
        if reader_proposal is not None
        else {}
    )
    priority_value_labels = {
        "WEAK": "弱化",
        "SECONDARY": "次要",
        "NORMAL": "标准",
        "STRONG": "强化",
        "CORE": "核心",
    }
    priority_to_strength = {
        "OFF": ReaderExperienceStrength.WEAK.value,
        "LOW": ReaderExperienceStrength.SECONDARY.value,
        "MEDIUM": ReaderExperienceStrength.NORMAL.value,
        "HIGH": ReaderExperienceStrength.STRONG.value,
        "VERY_HIGH": ReaderExperienceStrength.CORE.value,
    }
    priority_options = [
        {"value": value.value, "label": priority_value_labels[value.value]}
        for value in ReaderExperienceStrength
    ]
    author_overrides, author_instruction = _reader_kernel_author_overrides(
        database, book_id
    )
    author_overrides_payload = author_overrides.model_dump(
        mode="json", exclude_unset=True, exclude_none=True
    )
    reader_override_payload = dict(author_overrides_payload.get("reader_experience", {}))
    market_override_payload = dict(author_overrides_payload.get("market_category", {}))
    drive_override_payload = dict(author_overrides_payload.get("narrative_drive", {}))
    creative_override_payload = dict(author_overrides_payload.get("creative_semantics", {}))

    def current_value(section: dict[str, Any], field: str, recommended: Any) -> Any:
        return section.get(field, recommended)

    recommended_priorities = dict(reader_payload.get("experience_priorities", {}))
    priority_from_contract = {
        **recommended_priorities,
        **dict(reader_override_payload.get("experience_priorities", {})),
    }
    experience_priority_labels = {
        "OFF": "关闭",
        "LOW": "弱化",
        "MEDIUM": "标准",
        "HIGH": "强化",
        "VERY_HIGH": "核心",
    }
    reader_display = (
        {
            "summary": str(reader_proposal.get("summary") or ""),
            "semantic_evidence": list(reader_proposal.get("semantic_evidence", [])),
            "uncertainties": list(reader_proposal.get("uncertainties", [])),
            "author_attention_points": list(
                reader_proposal.get("author_attention_points", [])
            ),
            "primary_family": {
                "PROGRESSION_FANTASY": "成长型玄幻",
                "MYSTERY_PROGRESSION": "神秘学成长",
                "SURVIVAL_PROGRESSION": "生存成长",
                "TEAM_PROGRESSION": "团队成长",
                "COSMIC_PROGRESSION": "宇宙成长",
                "EVOLUTION_PROGRESSION": "进化成长",
                "CIVILIZATION_PROGRESSION": "文明成长",
                "CUSTOM": "自定义成长",
            }.get(str(reader_payload.get("primary_family") or ""), "自定义成长"),
            "recommended_primary_family_value": str(
                reader_payload.get("primary_family") or "CUSTOM"
            ),
            "primary_family_value": str(
                current_value(
                    reader_override_payload,
                    "primary_family",
                    reader_payload.get("primary_family") or "CUSTOM",
                )
            ),
            "secondary_family_values": list(
                current_value(
                    reader_override_payload,
                    "secondary_families",
                    reader_payload.get("secondary_families", []),
                )
            ),
            "recommended_secondary_family_values": list(
                reader_payload.get("secondary_families", [])
            ),
            "primary_family_options": _enum_options(PrimaryFamily),
            "setting_skin": {
                "ANCIENT_FANTASY": "古典幻想",
                "OTHERWORLD": "异世界",
                "MODERN_CITY": "现代城市",
                "NEAR_FUTURE": "近未来",
                "APOCALYPSE": "末世",
                "COSMIC": "宇宙",
                "STEAMPUNK": "蒸汽幻想",
                "CUSTOM": "作者自定义",
            }.get(str(reader_payload.get("setting_skin") or ""), "作者自定义"),
            "recommended_setting_skin_value": str(
                reader_payload.get("setting_skin") or "CUSTOM"
            ),
            "setting_skin_value": str(
                current_value(
                    reader_override_payload,
                    "setting_skin",
                    reader_payload.get("setting_skin") or "CUSTOM",
                )
            ),
            "setting_skin_options": _enum_options(SettingSkin),
            "serial_form_value": str(
                current_value(
                    reader_override_payload,
                    "serial_form",
                    reader_payload.get("serial_form") or "LONG_SERIAL",
                )
            ),
            "recommended_serial_form_value": str(
                reader_payload.get("serial_form") or "LONG_SERIAL"
            ),
            "serial_form_options": _enum_options(SerialForm),
            "mysticism_level_value": str(
                current_value(
                    reader_override_payload,
                    "mysticism_level",
                    reader_payload.get("mysticism_level") or "MEDIUM",
                )
            ),
            "recommended_mysticism_level_value": str(
                reader_payload.get("mysticism_level") or "MEDIUM"
            ),
            "explanation_style": {
                "MYSTICAL": "玄秘",
                "MIXED_MYSTICAL": "混合偏玄秘",
                "BALANCED": "平衡",
                "MIXED_HARD": "混合偏硬",
                "HARD_EXPLANATION": "硬解释",
            }.get(str(reader_payload.get("explanation_style") or ""), "平衡"),
            "recommended_explanation_style_value": str(
                reader_payload.get("explanation_style") or "BALANCED"
            ),
            "explanation_style_value": str(
                current_value(
                    reader_override_payload,
                    "explanation_style",
                    reader_payload.get("explanation_style") or "BALANCED",
                )
            ),
            "explanation_style_options": _enum_options(ExplanationStyle),
            "experience_priority_options": [
                {"value": item.value, "label": experience_priority_labels[item.value]}
                for item in ExperiencePriority
            ],
            "tone": list(
                current_value(
                    reader_override_payload, "tone", reader_payload.get("tone", [])
                )
            ),
            "recommended_tone": list(reader_payload.get("tone", [])),
            "priorities": [
                {
                    "key": str(item["key"]),
                    "label": str(item["label"]),
                    "group": str(item["group"]),
                    "value": str(
                        priority_from_contract.get(str(item["key"]), "MEDIUM")
                    ),
                    "strength": priority_to_strength.get(
                        str(priority_from_contract.get(str(item["key"]), "MEDIUM")),
                        "NORMAL",
                    ),
                    "value_label": priority_value_labels.get(
                        priority_to_strength.get(
                            str(
                                priority_from_contract.get(
                                    str(item["key"]), "MEDIUM"
                                )
                            ),
                            "NORMAL",
                        ),
                        "标准",
                    ),
                    "recommended_value_label": experience_priority_labels.get(
                        str(recommended_priorities.get(str(item["key"]), "MEDIUM")),
                        "标准",
                    ),
                    "options": priority_options,
                }
                for item in READER_EXPERIENCE_UI
            ],
            "presets": list(READER_EXPERIENCE_PRESETS),
            "must_deliver": list(
                current_value(
                    reader_override_payload,
                    "must_deliver",
                    reader_payload.get("must_deliver", []),
                )
            ),
            "recommended_must_deliver": list(reader_payload.get("must_deliver", [])),
            "must_not_drift_into": list(
                current_value(
                    reader_override_payload,
                    "must_not_drift_into",
                    reader_payload.get("must_not_drift_into", []),
                )
            ),
            "recommended_must_not_drift_into": list(
                reader_payload.get("must_not_drift_into", [])
            ),
            "market_categories": [
                market_category_label(str(value))
                for value in [
                    market_display.get("primary_market_category"),
                    *market_display.get("secondary_market_categories", []),
                ]
                if value
            ],
            "primary_market_category_value": str(
                current_value(
                    market_override_payload,
                    "primary_market_category",
                    market_display.get("primary_market_category") or "CUSTOM",
                )
            ),
            "recommended_primary_market_category_value": str(
                market_display.get("primary_market_category") or "CUSTOM"
            ),
            "secondary_market_category_values": list(
                current_value(
                    market_override_payload,
                    "secondary_market_categories",
                    market_display.get("secondary_market_categories", []),
                )
            ),
            "recommended_secondary_market_category_values": list(
                market_display.get("secondary_market_categories", [])
            ),
            "current_market_categories": [
                market_category_label(str(value))
                for value in [
                    current_value(
                        market_override_payload,
                        "primary_market_category",
                        market_display.get("primary_market_category") or "CUSTOM",
                    ),
                    *current_value(
                        market_override_payload,
                        "secondary_market_categories",
                        market_display.get("secondary_market_categories", []),
                    ),
                ]
            ],
            "market_category_options": [
                {"value": item.value, "label": market_category_label(item)}
                for item in MarketCategory
            ],
            "primary_drive": str(
                narrative_drive_label(
                    str(drive_contract_display.get("primary_drive") or "CUSTOM")
                )
            ),
            "primary_drive_value": str(
                current_value(
                    drive_override_payload,
                    "primary_drive",
                    drive_contract_display.get("primary_drive") or "CUSTOM",
                )
            ),
            "recommended_primary_drive_value": str(
                drive_contract_display.get("primary_drive") or "CUSTOM"
            ),
            "current_primary_drive": narrative_drive_label(
                str(
                    current_value(
                        drive_override_payload,
                        "primary_drive",
                        drive_contract_display.get("primary_drive") or "CUSTOM",
                    )
                )
            ),
            "secondary_drives": list(
                [
                    narrative_drive_label(str(value))
                    for value in drive_contract_display.get("secondary_drives", [])
                ]
            ),
            "secondary_drive_values": list(
                current_value(
                    drive_override_payload,
                    "secondary_drives",
                    drive_contract_display.get("secondary_drives", []),
                )
            ),
            "recommended_secondary_drive_values": list(
                drive_contract_display.get("secondary_drives", [])
            ),
            "current_secondary_drives": [
                narrative_drive_label(str(value))
                for value in current_value(
                    drive_override_payload,
                    "secondary_drives",
                    drive_contract_display.get("secondary_drives", []),
                )
            ],
            "progression_engine_enabled": bool(
                current_value(
                    drive_override_payload,
                    "progression_engine_enabled",
                    drive_contract_display.get("progression_engine_enabled", False),
                )
            ),
            "recommended_progression_engine_enabled": bool(
                drive_contract_display.get("progression_engine_enabled", False)
            ),
            "drive_priorities": dict(
                drive_contract_display.get("drive_priorities", {})
            ),
            "drive_options": [
                {"value": drive.value, "label": narrative_drive_label(drive)}
                for drive in NarrativeDrive
            ],
            "author_overrides": author_overrides_payload,
            "author_instruction": author_instruction,
            "current_creative_semantics": {
                key: current_value(creative_override_payload, key, value)
                for key, value in dict(
                    reader_proposal.get("creative_semantics", {})
                ).items()
            },
            "overrides_need_regeneration": bool(
                state_row is not None
                and state_row["reader_kernel_overrides_need_regeneration"]
            ),
        }
        if reader_proposal is not None
        else None
    )
    return {
        "book_id": book_id,
        "title": record.title,
        "original_state": state_value,
        "original_state_label": {
            "ORIGINAL_SEED": "一句话创意已保存",
            "READER_EXPERIENCE_GENERATING": "AI 正在理解阅读体验与叙事驱动力",
            "READER_EXPERIENCE_REVIEW": "等待确认阅读体验",
            "CORE_INNOVATION_GENERATING": "正在生成核心玩法方案",
            "CORE_INNOVATION_REVIEW": "等待选择核心玩法",
            "FOUNDATION_GENERATING": "正在生成故事方案",
            "FOUNDATION_REVIEW": "等待你确认故事方案",
            "DEVELOPMENT_GENERATING": "正在展开选定的故事基础",
            "DEVELOPMENT_REVIEW": "等待最终预览与确认",
            "FOUNDATION_READY": "故事基础已确认",
            "FIRST_CHAPTER_DRAFTING": "正在准备第一章",
            "FIRST_CHAPTER_VALIDATED": "第一章已校验",
            "WRITING_READY": "可以继续创作",
        }.get(state_value, "原创项目"),
        "generating_reader_handoff": next(
            (
                item
                for item in handoffs
                if item["handoff_type"]
                == HandoffType.ORIGINAL_READER_INTERPRETATION.value
                and item["status"]
                in {"READY_FOR_CODEX", "CLAIMED", "RUNNING", "WAITING_FOR_USER"}
            ),
            None,
        ),
        "proposal": None if proposal is None else proposal.model_dump(mode="json"),
        "development_proposal": (
            None
            if development_proposal is None
            else development_proposal.model_dump(mode="json")
        ),
        "development_proposal_versions": development_proposal_versions,
        "current_development_proposal_version_id": (
            None
            if development_row is None
            else str(development_row["development_proposal_version_id"])
        ),
        "generating_development_proposal": next(
            (
                item
                for item in development_proposal_versions
                if item["status"] == "GENERATING"
            ),
            None,
        ),
        "innovation_proposal": (
            None if innovation_proposal is None else innovation_proposal.model_dump(mode="json")
        ),
        "innovation_proposal_versions": innovation_proposal_versions,
        "current_innovation_proposal_version": next(
            (item for item in innovation_proposal_versions if item["status"] == "CURRENT"),
            None,
        ),
        "generating_innovation_proposal": next(
            (
                item
                for item in innovation_proposal_versions
                if item["status"] == "GENERATING"
            ),
            None,
        ),
        "innovation_selection": innovation_selection,
        "foundation_selection": foundation_selection,
        "proposal_versions": proposal_versions,
        "current_proposal_version": next(
            (item for item in proposal_versions if item["status"] == "CURRENT"), None
        ),
        "generating_proposal": next(
            (item for item in proposal_versions if item["status"] == "GENERATING"), None
        ),
        "ready_proposal_versions": [
            item for item in proposal_versions if item["status"] == "READY"
        ],
        "historical_proposal_versions": [
            item for item in proposal_versions if item["status"] in {"ARCHIVED", "REJECTED"}
        ],
        "accepted": accepted,
        "candidates": candidates,
        "drafts": drafts,
        "chapter_count": chapter_count,
        "handoffs": handoffs,
        "approval_confirmation": "批准写入正史",
        "reader_experience": reader_proposal,
        "reader_experience_display": reader_display,
        "reader_kernel_author_overrides": author_overrides_payload,
        "reader_kernel_author_instruction": author_instruction,
        "kernel_contracts": [item.model_dump(mode="json") for item in kernel_records],
        "reader_experience_contract": next(
            (
                item.model_dump(mode="json")
                for item in kernel_records
                if item.contract_type is ProgressionContractType.READER_EXPERIENCE
                and item.status
                in {ContractStatus.EFFECTIVE, ContractStatus.NEEDS_REVIEW}
            ),
            None,
        ),
        "pending_kernel_contracts": [
            item.model_dump(mode="json")
            for item in kernel_records
            if item.contract_type is not ProgressionContractType.READER_EXPERIENCE
            and item.status is ContractStatus.NEEDS_REVIEW
        ],
        "effective_kernel_contracts": [
            item.model_dump(mode="json")
            for item in kernel_records
            if item.status is ContractStatus.EFFECTIVE
        ],
    }


__all__ = [
    "OriginalWorkflowError",
    "approve_original_first_chapter",
    "confirm_original_foundation",
    "confirm_original_reader_experience",
    "compare_original_proposals",
    "create_original_book",
    "import_original_core_innovation_proposal",
    "import_original_bootstrap_proposal",
    "import_original_foundation_development",
    "import_original_reader_kernel_proposal",
    "load_original_proposal",
    "load_original_innovation_proposal",
    "original_overview",
    "prepare_original_core_innovation",
    "prepare_original_bootstrap",
    "prepare_original_foundation_development",
    "prepare_original_reader_experience",
    "regenerate_original_reader_kernel",
    "save_original_reader_kernel_overrides",
    "resolve_original_proposal_version",
    "select_original_core_innovation",
    "select_first_chapter_candidate",
    "validate_original_draft",
]
