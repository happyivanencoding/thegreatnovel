"""Source-free original novel service built on the existing authoring kernel."""

from __future__ import annotations

import json
import sqlite3
import uuid
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
    OriginalBookRequest,
    OriginalBootstrapProposal,
    OriginalFoundationConfirmation,
    OriginalState,
)
from novel_authoring.original.state import original_record
from novel_authoring.planning.boundary import build_boundary_packet
from novel_authoring.planning.contracts import build_chapter_contract
from novel_authoring.planning.innovation import resolve_innovation_control
from novel_authoring.progression.interpretation import (
    ReaderExperienceAdjustment,
    ReaderExperienceInterpretation,
    adjust_reader_experience,
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.models import ContractStatus, ReaderExperienceContract
from novel_authoring.progression.service import (
    ContractRecord,
    ProgressionContractType,
    confirm_contract,
    create_contract_proposal,
    effective_contract_records,
    list_contract_records,
    reject_contract,
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
    get_handoff,
    validate_result_file,
)


class OriginalWorkflowError(RuntimeError):
    pass


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


def prepare_original_reader_experience(database: Database, book_id: str) -> dict[str, Any]:
    records = list_contract_records(database, book_id=book_id, edition_id="base")
    existing = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.READER_EXPERIENCE
            and record.status
            in {ContractStatus.NEEDS_REVIEW, ContractStatus.EFFECTIVE}
        ),
        None,
    )
    interpretation_path = _original_dir(database, book_id) / "reader_experience.json"
    existing_interpretation = _read_json(interpretation_path)
    if existing is not None and existing_interpretation is not None:
        return {
            "contract": existing.model_dump(mode="json"),
            "interpretation": existing_interpretation,
            "deduplicated": True,
            "canon_changed": False,
        }
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创的一句话创意不存在")
    request = OriginalBookRequest.model_validate(request_payload)
    interpretation = interpret_reader_experience(
        request.premise,
        genre_hint=request.genre,
        contract_prefix=book_id,
    )
    proposal = create_contract_proposal(
        database,
        book_id=book_id,
        edition_id="base",
        contract_type=ProgressionContractType.READER_EXPERIENCE,
        payload=interpretation.reader_contract,
        source="ORIGINAL_READER_EXPERIENCE_INTERPRETATION",
    )
    _write_json(interpretation_path, interpretation.model_dump(mode="json"))
    _set_original_state(database, book_id, OriginalState.READER_EXPERIENCE_REVIEW)
    return {
        "contract": proposal.model_dump(mode="json"),
        "interpretation": interpretation.model_dump(mode="json"),
        "deduplicated": False,
        "canon_changed": False,
    }


def _create_kernel_contract_proposals(
    database: Database,
    book_id: str,
    interpretation: ReaderExperienceInterpretation,
) -> list[ContractRecord]:
    existing = list_contract_records(database, book_id=book_id, edition_id="base")
    existing_types = {
        record.contract_type
        for record in existing
        if record.status in {ContractStatus.NEEDS_REVIEW, ContractStatus.EFFECTIVE}
    }
    bundle = compile_kernel_contract_proposals(interpretation)
    created: list[ContractRecord] = []
    for contract_type, payload in (
        (ProgressionContractType.GENRE, bundle.genre),
        (ProgressionContractType.PROGRESSION, bundle.progression),
        (ProgressionContractType.WORLD_EXPANSION, bundle.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, bundle.payoff_channels),
    ):
        if contract_type in existing_types:
            continue
        created.append(
            create_contract_proposal(
                database,
                book_id=book_id,
                edition_id="base",
                contract_type=contract_type,
                payload=payload,
                source="CONFIRMED_READER_EXPERIENCE",
            )
        )
    return created


def confirm_original_reader_experience(
    database: Database,
    book_id: str,
    adjustment: ReaderExperienceAdjustment | str = ReaderExperienceAdjustment.CONFIRM,
) -> dict[str, Any]:
    selected_adjustment = (
        adjustment
        if isinstance(adjustment, ReaderExperienceAdjustment)
        else ReaderExperienceAdjustment(adjustment)
    )
    interpretation_path = _original_dir(database, book_id) / "reader_experience.json"
    payload = _read_json(interpretation_path)
    if payload is None:
        prepare_original_reader_experience(database, book_id)
        payload = _read_json(interpretation_path)
    if payload is None:
        raise OriginalWorkflowError("Reader Experience Proposal 不存在")
    interpretation = ReaderExperienceInterpretation.model_validate(payload)
    records = list_contract_records(database, book_id=book_id, edition_id="base")
    effective = next(
        (
            record
            for record in records
            if record.contract_type is ProgressionContractType.READER_EXPERIENCE
            and record.status is ContractStatus.EFFECTIVE
        ),
        None,
    )
    if effective is None:
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
        if adjusted != ReaderExperienceContract.model_validate(current.payload):
            replacement = create_contract_proposal(
                database,
                book_id=book_id,
                edition_id="base",
                contract_type=ProgressionContractType.READER_EXPERIENCE,
                payload=adjusted,
                source="AUTHOR_ADJUSTED_READER_EXPERIENCE",
            )
            reject_contract(database, current.contract_record_id)
            current = replacement
        effective = confirm_contract(
            database,
            current.contract_record_id,
            effective_from_boundary=1,
            author_notes=f"作者选择：{selected_adjustment.value}",
        )
    confirmed_reader = ReaderExperienceContract.model_validate(effective.payload)
    interpretation = interpretation.model_copy(update={"reader_contract": confirmed_reader})
    _write_json(interpretation_path, interpretation.model_dump(mode="json"))
    proposals = _create_kernel_contract_proposals(database, book_id, interpretation)
    handoff = prepare_original_bootstrap(database, book_id)
    return {
        "reader_experience": effective.model_dump(mode="json"),
        "created_contract_proposals": [item.model_dump(mode="json") for item in proposals],
        "handoff": handoff,
        "canon_changed": False,
    }


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
    reader_experience = prepare_original_reader_experience(database, selected_id)
    return {
        "book_id": selected_id,
        "title": working_title,
        "database": str(paths.database),
        "request_path": str(request_path),
        "book_kind": BookKind.AUTHOR.value,
        "creation_mode": CreationMode.ORIGINAL.value,
        "original_state": OriginalState.READER_EXPERIENCE_REVIEW.value,
        "chapter_count": 0,
        "source_required": False,
        "reader_experience": reader_experience,
    }


def prepare_original_bootstrap(database: Database, book_id: str) -> dict[str, Any]:
    request_path = _original_dir(database, book_id) / "request.json"
    request = _read_json(request_path)
    if request is None:
        raise OriginalWorkflowError("原创 premise 请求不存在")
    effective = effective_contract_records(database, book_id=book_id, edition_id="base")
    reader = effective.get(ProgressionContractType.READER_EXPERIENCE)
    if reader is None:
        raise OriginalWorkflowError("必须先确认 Reader Experience，才能生成 Story Foundation")
    contract_records = list_contract_records(database, book_id=book_id, edition_id="base")
    latest_by_type: dict[str, dict[str, Any]] = {}
    for record in contract_records:
        latest_by_type.setdefault(
            record.contract_type.value,
            record.model_dump(mode="json"),
        )
    request = {
        **request,
        "progression_kernel": {
            "reader_experience": reader.model_dump(mode="json"),
            "contract_proposals": latest_by_type,
            "foundation_rules": [
                "三个 Foundation 必须共享同一 Reader Experience 与 Genre Promise",
                "三个 Foundation 必须在成长来源、资源经济、世界入口、冲突与人物动力上不同",
                "不得让 setting skin 或社会议题取代核心成长因果",
            ],
        },
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
    ):
        raise OriginalWorkflowError("handoff 不属于当前原创项目的基础框架任务")
    result = validate_result_file(database, handoff_id)
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
    proposal = OriginalBootstrapProposal.model_validate_json(
        proposal_path.read_text(encoding="utf-8")
    )
    handoff_request = _read_json(task_directory / "input" / "original_request.json") or {}
    expected_kernel = handoff_request.get("progression_kernel")
    if expected_kernel and proposal.kernel_contracts != expected_kernel:
        raise OriginalWorkflowError(
            "Foundation Proposal 必须原样携带已冻结的 Progression Kernel Contracts"
        )
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
                stored_proposal = OriginalBootstrapProposal.model_validate_json(stored_payload)
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


def load_original_proposal(database: Database, book_id: str) -> OriginalBootstrapProposal | None:
    row = _current_proposal_row(database, book_id)
    if row is None:
        return None
    return OriginalBootstrapProposal.model_validate_json(str(row["proposal_json"]))


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
        "current": OriginalBootstrapProposal.model_validate_json(
            str(current["proposal_json"])
        ).model_dump(mode="json"),
        "target": OriginalBootstrapProposal.model_validate_json(
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
                "SELECT state, accepted_apply_id FROM original_states "
                "WHERE book_id=? AND edition_id='base'",
                (book_id,),
            ).fetchone()
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
                "UPDATE original_states SET current_proposal_version_id=?, updated_at=?, "
                "version=version+1 WHERE book_id=? AND edition_id='base'",
                (proposal_version_id, now, book_id),
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
        proposal = OriginalBootstrapProposal.model_validate_json(str(target["proposal_json"]))
        _write_json(
            _original_dir(database, book_id) / "story_foundation" / "proposal.json",
            proposal.model_dump(mode="json"),
        )
        if not accepted_apply_id:
            _update_registry(database, book_id, state=OriginalState.FOUNDATION_REVIEW)
    return {
        "proposal_version_id": proposal_version_id,
        "status": resulting_status,
        "current_changed": normalized == "REPLACE_CURRENT",
        "accepted_foundation_changed": False,
        "canon_changed": False,
    }


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
    proposal_row = _current_proposal_row(database, book_id)
    if proposal_row is None:
        raise OriginalWorkflowError("尚无可确认的当前故事基础方案")
    proposal = OriginalBootstrapProposal.model_validate_json(str(proposal_row["proposal_json"]))
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创的一句话创意不存在")
    request = OriginalBookRequest.model_validate(request_payload)
    try:
        plan = build_genesis_apply_plan(
            proposal_version_id=str(proposal_row["proposal_version_id"]),
            proposal=proposal,
            confirmation=data,
            request=request,
        )
        applied = apply_genesis_plan(database, book_id, plan)
    except (GenesisApplyError, sqlite3.IntegrityError) as exc:
        raise OriginalWorkflowError(str(exc)) from exc
    confirmed_contracts: list[dict[str, Any]] = []
    if data.confirm_kernel_contracts:
        seen: set[ProgressionContractType] = set()
        for record in list_contract_records(database, book_id=book_id, edition_id="base"):
            if (
                record.contract_type is ProgressionContractType.READER_EXPERIENCE
                or record.contract_type in seen
            ):
                continue
            seen.add(record.contract_type)
            if record.status is ContractStatus.NEEDS_REVIEW:
                confirmed = confirm_contract(
                    database,
                    record.contract_record_id,
                    effective_from_boundary=1,
                    author_notes="作者在 Foundation 最终预览中一并确认",
                )
                confirmed_contracts.append(confirmed.model_dump(mode="json"))
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
            ProgressionContractType.GENRE,
            ProgressionContractType.PROGRESSION,
        }
        if not required.issubset(effective_types):
            raise OriginalWorkflowError("必须先确认 Reader、Genre 与 Progression Contract")
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
    _reconcile_completed_original_bootstrap(database, book_id)
    proposal = load_original_proposal(database, book_id)
    accepted = accepted_foundation(database, book_id)
    kernel_records = list_contract_records(database, book_id=book_id, edition_id="base")
    reader_interpretation = _read_json(
        _original_dir(database, book_id) / "reader_experience.json"
    )
    with database.connect() as connection:
        state_row = connection.execute(
            "SELECT state FROM original_states WHERE book_id=? AND edition_id='base'",
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
    reader_payload = (
        dict(reader_interpretation.get("reader_contract", {}))
        if reader_interpretation is not None
        else {}
    )
    priority_labels = {
        "PROGRESSION": "成长突破",
        "POWER_VERIFICATION": "能力兑现",
        "COMBAT": "战斗兑现",
        "EXPLORATION": "机缘探索",
        "RESOURCE_OPPORTUNITY": "资源机会",
        "WORLD_EXPANSION": "世界扩张",
        "FACTION_CONFLICT": "势力竞争",
        "MYSTERY": "世界谜团",
        "TEAM_GROWTH": "团队成长",
        "RELATIONSHIP": "人物关系",
        "KNOWLEDGE": "知识成长",
        "SOCIAL_THEME": "社会议题",
    }
    reader_display = (
        {
            "summary": str(reader_interpretation.get("summary") or ""),
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
            "explanation_style": {
                "MYSTICAL": "玄秘",
                "MIXED_MYSTICAL": "混合偏玄秘",
                "BALANCED": "平衡",
                "MIXED_HARD": "混合偏硬",
                "HARD_EXPLANATION": "硬解释",
            }.get(str(reader_payload.get("explanation_style") or ""), "平衡"),
            "priorities": [
                {
                    "key": key,
                    "label": priority_labels[key],
                    "value": str(value),
                    "value_label": {
                        "VERY_HIGH": "核心",
                        "HIGH": "重要",
                        "MEDIUM": "辅助",
                        "LOW": "弱化",
                        "OFF": "不需要",
                    }.get(str(value), str(value)),
                }
                for key, value in dict(
                    reader_payload.get("experience_priorities", {})
                ).items()
                if key in priority_labels
            ],
            "must_deliver": list(reader_payload.get("must_deliver", [])),
            "must_not_drift_into": list(
                reader_payload.get("must_not_drift_into", [])
            ),
            "derived_adapter": reader_interpretation.get("derived_adapter_spec"),
        }
        if reader_interpretation is not None
        else None
    )
    return {
        "book_id": book_id,
        "title": record.title,
        "original_state": state_value,
        "original_state_label": {
            "ORIGINAL_SEED": "一句话创意已保存",
            "READER_EXPERIENCE_REVIEW": "等待确认阅读体验",
            "FOUNDATION_GENERATING": "正在生成故事方案",
            "FOUNDATION_REVIEW": "等待你确认故事方案",
            "FOUNDATION_READY": "故事基础已确认",
            "FIRST_CHAPTER_DRAFTING": "正在准备第一章",
            "FIRST_CHAPTER_VALIDATED": "第一章已校验",
            "WRITING_READY": "可以继续创作",
        }.get(state_value, "原创项目"),
        "proposal": None if proposal is None else proposal.model_dump(mode="json"),
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
        "reader_experience": reader_interpretation,
        "reader_experience_display": reader_display,
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
    "import_original_bootstrap_proposal",
    "load_original_proposal",
    "original_overview",
    "prepare_original_bootstrap",
    "prepare_original_reader_experience",
    "resolve_original_proposal_version",
    "select_first_chapter_candidate",
    "validate_original_draft",
]
