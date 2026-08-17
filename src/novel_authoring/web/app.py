from __future__ import annotations

import json
import re
import sqlite3
import subprocess
from pathlib import Path
from typing import Annotated, Any, cast
from urllib.parse import urlencode

try:  # Optional dependency: CLI/core remains usable without the web extra.
    from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
    from fastapi.responses import (
        FileResponse,
        HTMLResponse,
        JSONResponse,
        RedirectResponse,
        Response,
    )
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
except ImportError:  # pragma: no cover - exercised only without web extras
    FastAPI = None  # type: ignore[misc, assignment]
    HTTPException = Exception  # type: ignore[misc, assignment]
    Request = Any  # type: ignore[misc, assignment]
    File = Form = lambda *args, **kwargs: None
    UploadFile = Any  # type: ignore[misc, assignment]
    FileResponse = HTMLResponse = JSONResponse = RedirectResponse = Response = Any  # type: ignore[misc, assignment]
    StaticFiles = None  # type: ignore[misc, assignment]
    Jinja2Templates = None  # type: ignore[misc, assignment]

from novel_authoring import __version__
from novel_authoring.atlas.models import AtlasAction
from novel_authoring.atlas.service import (
    AtlasError,
    atlas_root,
    get_atlas_overview,
    record_atlas_action,
)
from novel_authoring.author_control.book_profile import (
    create_book_profile_refresh_proposal,
    create_profile_reanalysis_handoff,
    edit_book_profile,
    load_effective_book_profile,
    resolve_book_profile_refresh_proposal,
)
from novel_authoring.author_control.models import AuthorStateCommand
from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.author_control.reveal import (
    RevealPlanInput,
    build_reveal_agenda,
    build_secret_board,
    create_reveal_plan,
    override_reveal_agenda,
    project_truth_lens,
    set_character_truth_knowledge,
    set_reader_knowledge,
    truth_knowledge_view,
)
from novel_authoring.author_control.service import (
    author_control_view,
    execute_author_command,
    execute_author_intent,
    execute_author_task,
)
from novel_authoring.author_control.truth import (
    AuthorTruthInput,
    create_author_truth,
    create_open_creative_question,
    create_secret_candidate,
    evaluate_truth_compatibility,
    list_author_truths,
    list_open_creative_questions,
    list_secret_candidates,
    resolve_secret_candidate,
    update_author_truth,
)
from novel_authoring.db.database import Database
from novel_authoring.drafting import repair_draft_metadata, save_draft_content
from novel_authoring.edition import (
    ACTIVATE_PHRASE,
    activate_edition,
    edition_chapters,
    list_editions,
)
from novel_authoring.initialization import (
    InitializationDepth,
    InitializationError,
    create_initialization,
    latest_initialization,
    prepare_action_deepening,
    refresh_initialization,
    upgrade_initialization,
)
from novel_authoring.initialization.metrics import prepare_metric_bootstrap
from novel_authoring.library_catalog import (
    CatalogScope,
    LibraryCatalogEntry,
    LibraryCatalogView,
    build_library_catalog,
    find_candidate,
    studio_access,
    studio_readiness,
    suggest_book_id,
)
from novel_authoring.metrics.registry import load_registry
from novel_authoring.metrics.segments import list_segments
from novel_authoring.metrics.service import (
    MetricConflictError,
    MetricsAssembler,
    MetricValidationError,
    ObservationResolver,
)
from novel_authoring.original.models import (
    OriginalBookRequest,
    OriginalFoundationConfirmation,
)
from novel_authoring.original.service import (
    approve_original_first_chapter,
    compare_original_proposals,
    confirm_original_foundation,
    confirm_original_reader_experience,
    create_original_book,
    import_original_bootstrap_proposal,
    import_original_core_innovation_proposal,
    import_original_foundation_development,
    import_original_reader_kernel_proposal,
    original_overview,
    prepare_original_bootstrap,
    prepare_original_core_innovation,
    prepare_original_foundation_development,
    prepare_original_reader_experience,
    regenerate_original_reader_kernel,
    resolve_original_proposal_version,
    save_original_reader_kernel_overrides,
    select_first_chapter_candidate,
    select_original_core_innovation,
    select_original_foundation,
    validate_original_draft,
)
from novel_authoring.pending_actions import (
    attach_deepening_operation,
    author_activity_view,
    ensure_pending_author_action,
    list_pending_author_actions,
    set_pending_author_action_status,
)
from novel_authoring.progression.discovery import (
    import_kernel_contract_discovery,
    prepare_kernel_contract_discovery,
)
from novel_authoring.progression.inference import (
    infer_existing_contract_proposals_lexical_fallback,
)
from novel_authoring.progression.service import (
    confirm_contract,
    get_contract_record,
    list_contract_records,
)
from novel_authoring.progression.workspace import build_progression_workspace
from novel_authoring.readiness import evaluate_revision_range
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.library import (
    LibraryAddOptions,
    LibraryProjectDeleteError,
    add_book,
    delete_library_project,
)
from novel_authoring.storage.registry import BookKind, BookRegistry
from novel_authoring.utils import stable_id, utc_now
from novel_authoring.web.dependencies import create_csrf_token, verify_csrf
from novel_authoring.web.routes.atlas import (
    GRAPH_TYPES,
    atlas_context,
    atlas_entry_detail,
    atlas_graph_view,
    public_atlas_overview,
)
from novel_authoring.web.routes.jobs import list_handoffs
from novel_authoring.web.routes.metrics import save_author_input
from novel_authoring.web.routes.pages import (
    chapter_context,
    dashboard_context,
    metric_history,
    observation_history,
    workflow_context,
)
from novel_authoring.web.routes.workflow import (
    prepare_continuation,
    prepare_revision,
    prepare_selected_candidate_draft,
)
from novel_authoring.web.schemas import (
    AtlasActionRequest,
    AuthorInputRequest,
    AuthorIntentRequest,
    AuthorTaskRequest,
    AuthorTruthUpdateRequest,
    BookProfileEditRequest,
    BookProfileProposalRequest,
    BookProfileProposalResolutionRequest,
    CandidateSelectionRequest,
    DraftApprovalRequest,
    DraftContentRequest,
    DraftMetadataRepairRequest,
    EditionActivationRequest,
    HandoffRequest,
    HiddenItemRequest,
    KernelContractDiscoveryRequest,
    KnowledgeUpdateRequest,
    OpenCreativeQuestionRequest,
    OriginalCandidateSelectionRequest,
    OriginalCoreInnovationSelectionRequest,
    OriginalDraftActionRequest,
    OriginalFoundationSelectionRequest,
    OriginalProposalImportRequest,
    OriginalProposalVersionResolutionRequest,
    OriginalReaderExperienceConfirmationRequest,
    OriginalReaderKernelRegenerationRequest,
    ProfileReanalysisRequest,
    ProgressionContractConfirmationRequest,
    RecomputeRequest,
    RetractRequest,
    RevealAgendaOverrideRequest,
    SecretCandidateRequest,
    SecretCandidateResolutionRequest,
    TruthCompatibilityRequest,
    UserResponseRequest,
)
from novel_authoring.web.workbench import build_workbench_context
from novel_authoring.workflows.approval import approve_draft
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    HandoffType,
    HandoffWorkflowError,
    cancel_handoff,
    complete_handoff,
    copy_instruction,
    create_initialization_handoff,
    get_handoff,
    mark_stale,
    record_user_response,
    validate_result_file,
)

_ID = re.compile(r"^[A-Za-z0-9._-]+$")
_QUERY_ID = re.compile(r"^[A-Za-z0-9._:-]+$")
_ACTION_MODES = {"continue": "continue", "rewrite": "rewrite", "plan": "plan"}

# Single source of truth for the cache-busting ``?v=`` suffix used by every
# template; also reported by /health so stale static assets are diagnosable.
STATIC_ASSET_VERSION = "3.5.1"


# Sentinel distinguishing "never probed" from a probed result of ``None``.
_COMMIT_NOT_PROBED = object()
_commit_cache: object = _COMMIT_NOT_PROBED


def _current_commit() -> str | None:
    """Best-effort git commit hash; never raises, returns None when unknown.

    The probe runs at most once per process and the result is cached, so
    ``/health`` never spawns ``git`` per request and a hanging ``git`` cannot
    block the event loop more than once.
    """

    global _commit_cache
    if _commit_cache is not _COMMIT_NOT_PROBED:
        return cast("str | None", _commit_cache)
    value: str | None
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=str(Path(__file__).resolve().parents[2]),
        )
    except (OSError, subprocess.SubprocessError):
        value = None
    else:
        value = completed.stdout.strip() or None if completed.returncode == 0 else None
    _commit_cache = value
    return value


def _check_id(value: str) -> str:
    if not _ID.fullmatch(value):
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_ID", "message": "标识符格式无效", "details": {}},
        )
    return value


def _query_id(request: Request, name: str) -> str | None:
    value = request.query_params.get(name)
    if value and not _QUERY_ID.fullmatch(value):
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_ID", "message": "查询标识符格式无效", "details": {}},
        )
    return value or None


def _query_flag(request: Request, name: str) -> bool:
    return str(request.query_params.get(name) or "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _query_action(request: Request) -> str | None:
    action = str(request.query_params.get("action") or "").strip().lower()
    return action if action in _ACTION_MODES else None


def _workbench_mode(request: Request) -> str:
    action = _query_action(request)
    return _ACTION_MODES[action] if action else request.query_params.get("mode", "home")


def _error(exc: Exception) -> JSONResponse:
    error_code = getattr(exc, "error_code", None)
    if error_code:
        status = getattr(exc, "status_code", 400)
        return JSONResponse(
            status_code=status if isinstance(status, int) and status < 500 else 400,
            content={"error": {"code": error_code, "message": str(exc), "details": {}}},
        )
    code = "CONFLICT" if getattr(exc, "status_code", 500) == 409 else "WORKFLOW_ERROR"
    status = 409 if code == "CONFLICT" else 400
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": str(exc), "details": {}}},
    )


def _handoff_not_found_response() -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "HANDOFF_NOT_FOUND",
                "message": "handoff 不存在",
                "details": {},
            }
        },
    )


def _template(templates: Any, name: str, request: Request, context: dict[str, Any]) -> Any:
    context = {"request": request, "asset_version": STATIC_ASSET_VERSION, **context}
    return templates.TemplateResponse(request=request, name=name, context=context)


def _library_root_for_database(database: Database, explicit: Path | None) -> Path | None:
    if explicit is not None:
        return Path(explicit).expanduser().resolve()
    try:
        value = database.scalar("SELECT workspace_root FROM books LIMIT 1")
    except (OSError, RuntimeError):
        return None
    if value is None:
        return None
    book_root = Path(str(value)).expanduser().resolve()
    return book_root.parent if (book_root / "book.yaml").is_file() else None


def _require_book_scope(app: Any, book_id: str) -> str:
    checked = _check_id(book_id)
    root = app.state.library_root
    if root is None:
        return checked
    try:
        record = BookRegistry(BookLayout(root)).record(checked)
    except FileNotFoundError:
        return checked
    if record.book_kind is not BookKind.AUTHOR and not app.state.developer_mode:
        raise HTTPException(
            status_code=404,
            detail={"code": "BOOK_NOT_IN_AUTHOR_SCOPE", "message": "作品不在作者书库"},
        )
    return checked


def _database_for_book(app: Any, book_id: str) -> Database:
    """Resolve a canonical book database instead of reusing the boot DB."""

    checked = _require_book_scope(app, book_id)
    root = app.state.library_root
    if root is not None:
        paths = BookLayout(root).for_book(checked)
        if paths.database.is_file():
            return Database(paths.database)
        raise HTTPException(
            status_code=404,
            detail={"code": "BOOK_RUNTIME_NOT_FOUND", "message": "书籍运行库不存在"},
        )
    if app.state.book_id is None or str(app.state.book_id) == checked:
        return cast(Database, app.state.database)
    raise HTTPException(status_code=404, detail="书籍不在当前 Web 运行库")


def _library_catalog_for_app(
    app: Any, scope: CatalogScope = CatalogScope.AUTHOR
) -> LibraryCatalogView | None:
    root = app.state.library_root
    discovery_root = app.state.discovery_root
    if root is None or discovery_root is None:
        return None
    return build_library_catalog(BookLayout(root), discovery_root, scope=scope)


def _catalog_entry_for_app(
    app: Any, catalog: LibraryCatalogView, book_id: str
) -> LibraryCatalogEntry | None:
    entry = _catalog_entry(catalog, book_id=book_id)
    if entry is not None or not app.state.developer_mode:
        return entry
    technical = _library_catalog_for_app(app, CatalogScope.TECHNICAL)
    return None if technical is None else _catalog_entry(technical, book_id=book_id)


def _catalog_entry(
    catalog: LibraryCatalogView, *, book_id: str | None = None, candidate_id: str | None = None
) -> LibraryCatalogEntry | None:
    return next(
        (
            item
            for item in catalog.entries
            if (book_id is not None and item.book_id == book_id)
            or (candidate_id is not None and item.candidate_id == candidate_id)
        ),
        None,
    )


def _library_paths_payload(
    layout: BookLayout, book_id: str, edition_id: str = "base"
) -> dict[str, Any]:
    paths = layout.for_book(book_id)
    edition = paths.edition(edition_id)
    return {
        "layout_version": layout.layout_version,
        "book_id": paths.book_id,
        "root": str(paths.root),
        "book_yaml": str(paths.book_yaml),
        "readme": str(paths.readme),
        "source": str(paths.source),
        "system": str(paths.system),
        "database": str(paths.database),
        "source_manifest": str(paths.source_manifest),
        "system_snapshots": str(paths.snapshots),
        "system_logs": str(paths.logs),
        "system_cache": str(paths.cache),
        "system_temp": str(paths.temp),
        "edition": {
            "edition_id": edition.edition_id,
            "root": str(edition.root),
            "analysis": str(edition.analysis),
            "initialization": str(edition.initialization),
            "atlas": str(edition.atlas),
            "metrics": str(edition.metrics),
            "rhythm": str(edition.rhythm),
            "writing": str(edition.writing),
            "drafts": str(edition.drafts),
            "continuation": str(edition.continuation),
            "revisions": str(edition.revisions),
            "validation": str(edition.validation),
            "boundaries": str(edition.boundaries),
            "candidates": str(edition.candidates),
            "contracts": str(edition.contracts),
            "operations": str(edition.operations),
            "batches": str(edition.batches),
            "canon": str(edition.canon),
            "exports": str(edition.exports),
            "latest_export": str(edition.latest_export),
            "archive_exports": str(edition.archive_exports),
        },
    }


def _target_action_ordinal(
    database: Database,
    book_id: str,
    edition_id: str,
    action_type: str,
    chapter_id: str | None,
) -> int | None:
    with database.connect() as connection:
        chapters = edition_chapters(connection, book_id, edition_id)
    if action_type == "CONTINUE":
        return max((int(item["ordinal"]) for item in chapters), default=0) + 1
    return next(
        (int(item["ordinal"]) for item in chapters if str(item["chapter_id"]) == str(chapter_id)),
        None,
    )


def _resume_pending_actions(database: Database, book_id: str) -> list[dict[str, Any]]:
    """Advance completed deepening tasks and recreate the author's original action."""

    for item in list_pending_author_actions(database, book_id):
        deepening_id = str(item.get("deepening_operation_id") or "")
        if not deepening_id:
            continue
        try:
            deepening_handoff = get_handoff(database, deepening_id)
        except HandoffWorkflowError:
            continue
        if str(deepening_handoff.get("status")) != HandoffStatus.COMPLETED.value:
            continue
        try:
            refresh_initialization(
                database,
                book_id,
                edition_id=str(item["edition_id"]),
            )
            deepening = prepare_action_deepening(
                database,
                book_id,
                edition_id=str(item["edition_id"]),
                action=str(item["action_type"]),
                target_chapter_id=item.get("chapter_id"),
            )
            if deepening["status"] != "ACTION_CONTEXT_READY":
                next_handoff = create_initialization_handoff(
                    database,
                    book_id,
                    edition_id=str(item["edition_id"]),
                    requested_stage="NOVEL_INITIALIZATION",
                )
                attach_deepening_operation(
                    database,
                    str(item["pending_action_id"]),
                    str(next_handoff["handoff_id"]),
                    deepening,
                )
                continue
            set_pending_author_action_status(
                database,
                str(item["pending_action_id"]),
                "CONTEXT_READY",
            )
            set_pending_author_action_status(
                database,
                str(item["pending_action_id"]),
                "RESUMING",
            )
            request_payload = HandoffRequest.model_validate(item["request"])
            if str(item["action_type"]) == "CONTINUE":
                resumed = prepare_continuation(database, book_id, request_payload)
            else:
                resumed = prepare_revision(database, book_id, request_payload)
            set_pending_author_action_status(
                database,
                str(item["pending_action_id"]),
                "COMPLETED",
                resumed_handoff_id=str(resumed["handoff_id"]),
            )
        except (InitializationError, HandoffWorkflowError, ValueError):
            set_pending_author_action_status(
                database,
                str(item["pending_action_id"]),
                "FAILED",
            )
            continue
    return [
        author_activity_view(item)
        for item in list_pending_author_actions(
            database,
            book_id,
            include_finished=True,
        )
    ]


def _queue_pending_author_action(
    database: Database,
    book_id: str,
    payload: HandoffRequest,
    *,
    action_type: str,
) -> dict[str, Any]:
    edition_id = str(payload.edition_id or "base")
    target_ordinal = _target_action_ordinal(
        database,
        book_id,
        edition_id,
        action_type,
        payload.context_chapter_id,
    )
    pending, reused = ensure_pending_author_action(
        database,
        action_type=action_type,
        book_id=book_id,
        edition_id=edition_id,
        chapter_id=payload.context_chapter_id,
        target_chapter_ordinal=target_ordinal,
        author_goal=str(payload.author_goal or ""),
        innovation={
            "level": None if payload.innovation_level is None else payload.innovation_level.value,
            "focus": [item.value for item in (payload.innovation_focus or [])],
            "save_as_book_default": payload.save_as_book_default,
        },
        selected_author_tasks=list(payload.author_task_ids),
        requested_stage=payload.requested_stage,
        request_payload=payload.model_dump(mode="json"),
        required_context={},
    )
    if reused:
        activities = _resume_pending_actions(database, book_id)
        current = next(
            (
                item
                for item in activities
                if item["pending_action_id"] == pending["pending_action_id"]
            ),
            author_activity_view(pending),
        )
        return {
            "workflow_status": "PENDING_ACTION_REUSED",
            "resume_action": action_type,
            "pending_action": current,
            "deduplicated": True,
        }
    try:
        deepening = prepare_action_deepening(
            database,
            book_id,
            edition_id=edition_id,
            action=action_type,
            target_chapter_id=payload.context_chapter_id,
        )
        if deepening["status"] == "ACTION_CONTEXT_READY":
            set_pending_author_action_status(
                database,
                str(pending["pending_action_id"]),
                "RESUMING",
            )
            resumed = (
                prepare_continuation(database, book_id, payload)
                if action_type == "CONTINUE"
                else prepare_revision(database, book_id, payload)
            )
            completed = set_pending_author_action_status(
                database,
                str(pending["pending_action_id"]),
                "COMPLETED",
                resumed_handoff_id=str(resumed["handoff_id"]),
            )
            return {
                "workflow_status": "ACTION_RESUMED",
                "resume_action": action_type,
                "pending_action": author_activity_view(completed),
                "handoff": resumed,
                "deduplicated": False,
            }
        handoff = create_initialization_handoff(
            database,
            book_id,
            edition_id=edition_id,
            requested_stage="NOVEL_INITIALIZATION",
        )
        attached = attach_deepening_operation(
            database,
            str(pending["pending_action_id"]),
            str(handoff["handoff_id"]),
            deepening,
        )
        return {
            "workflow_status": "CONTEXT_HYDRATION_REQUIRED",
            "resume_action": action_type,
            "pending_action": author_activity_view(attached),
            "deepening": deepening,
            "handoff": handoff,
            "deduplicated": False,
        }
    except Exception:
        set_pending_author_action_status(
            database,
            str(pending["pending_action_id"]),
            "FAILED",
        )
        raise


def create_app(
    database: Database,
    *,
    book_id: str | None = None,
    library_root: Path | None = None,
    discovery_root: Path | None = None,
    developer_mode: bool = False,
    story_program_reference_root: Path | None = None,
) -> Any:
    if FastAPI is None or Jinja2Templates is None:
        raise RuntimeError("Web 功能需要安装可选依赖：pip install '.[web]'")
    app = FastAPI(title="Author Workbench", docs_url="/api/docs")
    app.state.database = database
    app.state.book_id = book_id
    app.state.library_root = _library_root_for_database(database, library_root)
    app.state.discovery_root = (
        Path(discovery_root).expanduser().resolve()
        if discovery_root is not None
        else (
            None if app.state.library_root is None else Path(app.state.library_root).parent / "book"
        )
    )
    app.state.developer_mode = developer_mode
    app.state.story_program_reference_root = (
        None
        if story_program_reference_root is None
        else Path(story_program_reference_root).expanduser().resolve()
    )
    app.state.csrf_token = create_csrf_token()
    template_dir = Path(__file__).parent / "templates"
    templates = Jinja2Templates(directory=str(template_dir))
    templates.env.autoescape = True

    def render_onboarding(
        request: Request,
        catalog: LibraryCatalogView,
        entry: LibraryCatalogEntry,
    ) -> Any:
        return _template(
            templates,
            "workbench_onboarding.html",
            request,
            {
                "book": {"title": entry.title},
                "book_id": entry.book_id or "",
                "edition_id": entry.active_edition,
                "catalog": catalog.to_dict(),
                "library_catalog": catalog.to_dict(),
                "catalog_entry": entry.to_dict(),
                "current_catalog_id": entry.catalog_id,
                "csrf_token": app.state.csrf_token,
            },
        )

    @app.exception_handler(HTTPException)
    async def handle_http_error(_request: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
        if "code" not in detail:
            detail = {"code": "HTTP_ERROR", **detail}
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {**detail, "details": detail.get("details", {})}},
        )

    @app.exception_handler(Exception)
    async def handle_error(_request: Request, exc: Exception) -> JSONResponse:
        return _error(exc)

    if StaticFiles is not None:
        app.mount(
            "/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static"
        )

    from novel_authoring.web.routes.story_program import register_story_program_routes

    register_story_program_routes(
        app,
        templates,
        render_template=_template,
        asset_version=STATIC_ASSET_VERSION,
    )

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "executor": "Windows Codex desktop client via local file handoff",
            "version": __version__,
            "commit": _current_commit(),
            "static_asset_version": STATIC_ASSET_VERSION,
        }

    def catalog_payload(scope: CatalogScope = CatalogScope.AUTHOR) -> dict[str, Any]:
        catalog = _library_catalog_for_app(app, scope)
        if catalog is None:
            return {
                "library_root": None,
                "discovery_root": None,
                "supported_formats": [],
                "entries": [],
                "groups": {"ready": [], "running": [], "pending": []},
                "counts": {"ready": 0, "running": 0, "pending": 0},
                "revision": "",
                "books": [],
            }
        payload = catalog.to_dict()
        payload["books"] = [item for item in payload["entries"] if item["book_id"]]
        return payload

    @app.get("/api/library")
    @app.get("/api/library/catalog")
    async def library_api(request: Request) -> dict[str, Any]:
        requested_scope = str(request.query_params.get("scope") or "AUTHOR").upper()
        try:
            scope = CatalogScope(requested_scope)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="书库 scope 无效") from exc
        if scope is CatalogScope.TECHNICAL and not app.state.developer_mode:
            raise HTTPException(status_code=404, detail="技术书库未启用")
        return catalog_payload(scope)

    @app.delete("/api/library/books/{path_book_id}")
    async def delete_library_book_api(request: Request, path_book_id: str) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        try:
            return delete_library_project(BookLayout(root), _require_book_scope(app, path_book_id))
        except LibraryProjectDeleteError as exc:
            return _error(exc)

    @app.post("/api/library/discovery/refresh")
    async def library_discovery_refresh_api(request: Request) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        requested_scope = str(request.query_params.get("scope") or "AUTHOR").upper()
        try:
            scope = CatalogScope(requested_scope)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="书库 scope 无效") from exc
        if scope is CatalogScope.TECHNICAL and not app.state.developer_mode:
            raise HTTPException(status_code=404, detail="技术书库未启用")
        return catalog_payload(scope)

    @app.post("/api/library/candidates/{candidate_id}/initialize")
    async def candidate_initialize_api(request: Request, candidate_id: str) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_candidate = _check_id(candidate_id)
        catalog = _library_catalog_for_app(app)
        if catalog is None:
            raise HTTPException(status_code=404, detail="书库未配置")
        candidate = find_candidate(catalog, checked_candidate)
        if candidate is None:
            raise HTTPException(status_code=404, detail="待初始化书籍不存在或已被处理")
        layout = BookLayout(app.state.library_root)
        book_id_value = suggest_book_id(candidate, layout)
        try:
            raw = await request.body()
            payload = json.loads(raw) if raw else {}
            if not isinstance(payload, dict):
                raise ValueError("初始化请求必须是 object")
            depth = InitializationDepth(
                str(payload.get("depth") or InitializationDepth.BALANCED).upper()
            )
            author_goal = str(payload.get("author_goal") or "CONTINUE").upper()
            if author_goal not in {"CONTINUE", "UNDERSTAND", "REWRITE", "AUDIT"}:
                raise ValueError("创作目标无效")
            added = add_book(
                LibraryAddOptions(
                    book_id=book_id_value,
                    title=candidate.title,
                    source=Path(candidate.source_path),
                    source_origin=Path(candidate.source_path),
                    library_root=layout.library_root,
                    confirm_order=True,
                    initialize_mode="prepare",
                )
            )
            selected_database = Database(added.database)
            create_initialization(
                selected_database,
                added.book_id,
                edition_id="base",
                depth=depth,
                requested_action=f"GOAL_{author_goal}",
            )
            handoff = create_initialization_handoff(
                selected_database,
                added.book_id,
                edition_id="base",
                requested_stage="NOVEL_INITIALIZATION",
            )
        except (OSError, ValueError, RuntimeError) as exc:
            return _error(exc)
        handoff_id = str(handoff["handoff_id"])
        return {
            "book_id": added.book_id,
            "title": added.title,
            "handoff_id": handoff_id,
            "status_label": "等待处理",
            "instruction_url": (
                f"/api/books/{added.book_id}/editions/base/handoffs/{handoff_id}/instruction"
            ),
            "workbench_url": f"/books/{added.book_id}/editions/base/workbench",
        }

    @app.get("/api/library/{path_book_id}/paths")
    async def library_paths_api(path_book_id: str) -> dict[str, Any]:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        return _library_paths_payload(BookLayout(root), _require_book_scope(app, path_book_id))

    @app.post("/api/library/import")
    async def library_import_api(request: Request) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=400, detail="library 未配置")
        try:
            payload = await request.json()
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="请求必须是 JSON") from exc
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="请求 JSON 必须是 object")
        book_id = _check_id(str(payload.get("book_id") or ""))
        source_value = payload.get("source_path")
        if not isinstance(source_value, str) or not source_value.strip():
            raise HTTPException(status_code=400, detail="需要 source_path")
        source = Path(source_value).expanduser().resolve()
        try:
            result = add_book(
                LibraryAddOptions(
                    book_id=book_id,
                    title=str(payload.get("title") or book_id),
                    source=source,
                    library_root=root,
                    confirm_order=bool(payload.get("confirm_order", False)),
                    initialize_mode=str(payload.get("initialize_mode") or "deferred"),
                )
            )
            value = result.to_dict()
            value["source_read_only"] = True
            return value
        except (OSError, ValueError) as exc:
            return _error(exc)

    @app.get("/library", response_class=HTMLResponse)
    async def library_page(request: Request) -> Any:
        catalog = _library_catalog_for_app(app)
        payload = catalog_payload() if catalog is None else catalog.to_dict()
        return _template(
            templates,
            "library.html",
            request,
            {
                "catalog": payload,
                "library": payload["entries"],
                "library_root": payload.get("library_root") or "",
                "csrf_token": app.state.csrf_token,
                "developer_mode": app.state.developer_mode,
                "technical_library": False,
            },
        )

    @app.get("/library/original/new", response_class=HTMLResponse)
    async def original_new_page(request: Request) -> Any:
        if app.state.library_root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        return _template(
            templates,
            "original_new.html",
            request,
            {"csrf_token": app.state.csrf_token},
        )

    @app.get("/library/unclassified", response_class=HTMLResponse)
    async def unclassified_library_page(request: Request) -> Any:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        registry = BookRegistry(BookLayout(root))
        projects = [
            record for record in registry.list() if record.book_kind is BookKind.UNCLASSIFIED
        ]
        return _template(
            templates,
            "library_unclassified.html",
            request,
            {
                "projects": projects,
                "csrf_token": app.state.csrf_token,
            },
        )

    @app.post("/api/library/{path_book_id}/classify")
    async def classify_library_book(request: Request, path_book_id: str) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        payload = await request.json()
        try:
            book_kind = BookKind(str(payload.get("book_kind") or ""))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="项目分类无效") from exc
        checked_book = _check_id(path_book_id)
        registry = BookRegistry(BookLayout(root))
        values = registry.read(checked_book)
        values["book_kind"] = book_kind.value
        values["updated_at"] = utc_now()
        registry.write(BookLayout(root).for_book(checked_book), values)
        registry.write_readme(BookLayout(root).for_book(checked_book), values)
        return {"book_id": checked_book, "book_kind": book_kind.value}

    @app.post("/api/library/original")
    async def original_create_api(request: Request, payload: OriginalBookRequest) -> Any:
        verify_csrf(request, None)
        if app.state.library_root is None:
            raise HTTPException(status_code=400, detail="library 未配置")
        try:
            created = create_original_book(BookLayout(app.state.library_root), payload)
            return {
                **created,
                "original_url": f"/books/{created['book_id']}/original",
            }
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/library/upload")
    async def library_upload_api(
        request: Request,
        files: Annotated[list[UploadFile], File()],
        conflict_policy: Annotated[str, Form()] = "KEEP_BOTH",
        renamed_filename: Annotated[str, Form()] = "",
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        discovery_root = app.state.discovery_root
        if discovery_root is None:
            raise HTTPException(status_code=400, detail="导入目录未配置")
        policy = conflict_policy.upper()
        if policy not in {"KEEP_BOTH", "RENAME", "CANCEL"}:
            raise HTTPException(status_code=400, detail="同名文件处理方式无效")
        if not files:
            raise HTTPException(status_code=400, detail="请选择正文文件")
        allowed = {".txt", ".md", ".markdown"}
        names = [Path(str(item.filename or "")).name for item in files]
        if any(not name or Path(name).suffix.casefold() not in allowed for name in names):
            raise HTTPException(status_code=400, detail="只支持 TXT、MD 或 Markdown 正文")
        target_root = Path(discovery_root).expanduser().resolve()
        target_root.mkdir(parents=True, exist_ok=True)
        if len(files) > 1:
            folder_name = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "-", Path(names[0]).stem)
            destination = target_root / f"{folder_name or '章节合集'}-章节"
            folder_suffix = 2
            while destination.exists():
                destination = target_root / f"{folder_name or '章节合集'}-章节-{folder_suffix}"
                folder_suffix += 1
            destination.mkdir()
        else:
            destination = target_root
        if policy == "RENAME":
            if len(files) != 1:
                raise HTTPException(status_code=400, detail="更改文件名只适用于单文件导入")
            renamed = Path(renamed_filename).name
            if not renamed or Path(renamed).suffix.casefold() not in allowed:
                raise HTTPException(status_code=400, detail="请输入带 TXT/Markdown 后缀的新文件名")
            names = [renamed]
        targets = [destination / name for name in names]
        if policy == "CANCEL" and any(path.exists() for path in targets):
            raise HTTPException(status_code=409, detail="存在同名文件，本次导入已取消")
        written: list[str] = []
        for upload, target in zip(files, targets, strict=True):
            if target.exists():
                stem, file_suffix = target.stem, target.suffix
                index = 2
                while target.exists():
                    target = target.with_name(f"{stem} ({index}){file_suffix}")
                    index += 1
            target.write_bytes(await upload.read())
            written.append(str(target))
        return {
            "status": "IMPORTED_TO_DISCOVERY",
            "file_count": len(written),
            "paths": written,
            "message": f"已导入 {len(written)} 个正文文件，书库会立即识别。",
        }

    @app.get("/books/{path_book_id}/original", response_class=HTMLResponse)
    async def original_studio_page(request: Request, path_book_id: str) -> Any:
        checked = _require_book_scope(app, path_book_id)
        try:
            overview = original_overview(_database_for_book(app, checked), checked)
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)
        return _template(
            templates,
            "original_studio.html",
            request,
            {"original": overview, "csrf_token": app.state.csrf_token},
        )

    @app.post("/api/books/{path_book_id}/original/bootstrap")
    async def original_bootstrap_api(request: Request, path_book_id: str) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return prepare_original_bootstrap(_database_for_book(app, checked), checked)
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/reader-experience/prepare")
    async def original_reader_experience_prepare_api(
        request: Request,
        path_book_id: str,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return prepare_original_reader_experience(
                _database_for_book(app, checked), checked
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/reader-experience/confirm")
    async def original_reader_experience_confirm_api(
        request: Request,
        path_book_id: str,
        payload: OriginalReaderExperienceConfirmationRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return confirm_original_reader_experience(
                _database_for_book(app, checked),
                checked,
                payload.adjustment,
                payload.priority_overrides,
                payload.primary_drive,
                payload.secondary_drives,
                payload.progression_engine_enabled,
                payload.creative_semantics,
                author_overrides=payload.author_overrides,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/reader-kernel/regenerate")
    async def original_reader_kernel_regenerate_api(
        request: Request,
        path_book_id: str,
        payload: OriginalReaderKernelRegenerationRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return regenerate_original_reader_kernel(
                _database_for_book(app, checked),
                checked,
                author_overrides=payload.author_overrides,
                author_instruction=payload.author_instruction,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/reader-kernel/overrides")
    async def original_reader_kernel_overrides_api(
        request: Request,
        path_book_id: str,
        payload: OriginalReaderKernelRegenerationRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return save_original_reader_kernel_overrides(
                _database_for_book(app, checked),
                checked,
                author_overrides=payload.author_overrides,
                author_instruction=payload.author_instruction,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/reader-kernel/import")
    async def original_reader_kernel_import_api(
        request: Request,
        path_book_id: str,
        payload: OriginalProposalImportRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return import_original_reader_kernel_proposal(
                _database_for_book(app, checked), checked, payload.handoff_id
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/proposal/import")
    async def original_proposal_import_api(
        request: Request,
        path_book_id: str,
        payload: OriginalProposalImportRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return import_original_bootstrap_proposal(
                _database_for_book(app, checked), checked, payload.handoff_id
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/core-innovation/import")
    async def original_core_innovation_import_api(
        request: Request,
        path_book_id: str,
        payload: OriginalProposalImportRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return import_original_core_innovation_proposal(
                _database_for_book(app, checked), checked, payload.handoff_id
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/core-innovation/prepare")
    async def original_core_innovation_prepare_api(
        request: Request,
        path_book_id: str,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return prepare_original_core_innovation(_database_for_book(app, checked), checked)
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/core-innovation/select")
    async def original_core_innovation_select_api(
        request: Request,
        path_book_id: str,
        payload: OriginalCoreInnovationSelectionRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return select_original_core_innovation(
                _database_for_book(app, checked), checked, payload.model_dump(mode="json")
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.get("/api/books/{path_book_id}/original/proposals/{proposal_version_id}/compare")
    async def original_proposal_compare_api(
        path_book_id: str,
        proposal_version_id: str,
    ) -> Any:
        checked = _require_book_scope(app, path_book_id)
        try:
            return compare_original_proposals(
                _database_for_book(app, checked),
                checked,
                _check_id(proposal_version_id),
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/proposals/{proposal_version_id}/resolve")
    async def original_proposal_resolution_api(
        request: Request,
        path_book_id: str,
        proposal_version_id: str,
        payload: OriginalProposalVersionResolutionRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return resolve_original_proposal_version(
                _database_for_book(app, checked),
                checked,
                _check_id(proposal_version_id),
                action=payload.action,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/foundation/confirm")
    async def original_foundation_confirm_api(
        request: Request,
        path_book_id: str,
        payload: OriginalFoundationConfirmation,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return confirm_original_foundation(_database_for_book(app, checked), checked, payload)
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/foundation/select")
    async def original_foundation_select_api(
        request: Request,
        path_book_id: str,
        payload: OriginalFoundationSelectionRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return select_original_foundation(
                _database_for_book(app, checked),
                checked,
                payload.selected_foundation_id,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/foundation-development/prepare")
    async def original_foundation_development_prepare_api(
        request: Request, path_book_id: str
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return prepare_original_foundation_development(
                _database_for_book(app, checked), checked
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/foundation-development/import")
    async def original_foundation_development_import_api(
        request: Request,
        path_book_id: str,
        payload: OriginalProposalImportRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return import_original_foundation_development(
                _database_for_book(app, checked), checked, payload.handoff_id
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/first-chapter/select")
    async def original_first_chapter_select_api(
        request: Request,
        path_book_id: str,
        payload: OriginalCandidateSelectionRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return select_first_chapter_candidate(
                _database_for_book(app, checked), checked, payload.candidate_id
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/first-chapter/validate")
    async def original_first_chapter_validate_api(
        request: Request,
        path_book_id: str,
        payload: OriginalDraftActionRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return validate_original_draft(
                _database_for_book(app, checked), checked, payload.draft_id
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/original/first-chapter/approve")
    async def original_first_chapter_approve_api(
        request: Request,
        path_book_id: str,
        payload: OriginalDraftActionRequest,
    ) -> Any:
        verify_csrf(request, None)
        checked = _require_book_scope(app, path_book_id)
        try:
            return approve_original_first_chapter(
                _database_for_book(app, checked),
                checked,
                payload.draft_id,
                payload.confirmation,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/drafts/{draft_id}/approve"
    )
    async def draft_approve_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        draft_id: str,
        payload: DraftApprovalRequest,
    ) -> Any:
        """Page-native author approval; the shared workflow remains authoritative."""

        verify_csrf(request, None)
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        checked_draft = _check_id(draft_id)
        try:
            result = approve_draft(
                _database_for_book(app, checked_book),
                checked_book,
                checked_draft,
                confirmation=payload.confirmation,
                edition_id=checked_edition,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)
        return {**result, "canon_changed": True}

    @app.get("/library/technical", response_class=HTMLResponse)
    async def technical_library_page(request: Request) -> Any:
        if not app.state.developer_mode:
            raise HTTPException(status_code=404, detail="技术书库未启用")
        catalog = _library_catalog_for_app(app, CatalogScope.TECHNICAL)
        payload = catalog_payload(CatalogScope.TECHNICAL) if catalog is None else catalog.to_dict()
        return _template(
            templates,
            "library.html",
            request,
            {
                "catalog": payload,
                "library": payload["entries"],
                "library_root": payload.get("library_root") or "",
                "csrf_token": app.state.csrf_token,
                "developer_mode": True,
                "technical_library": True,
            },
        )

    @app.get("/library/candidates/{candidate_id}", response_class=HTMLResponse)
    async def candidate_onboarding_page(request: Request, candidate_id: str) -> Any:
        catalog = _library_catalog_for_app(app)
        if catalog is None:
            raise HTTPException(status_code=404, detail="书库未配置")
        candidate = find_candidate(catalog, _check_id(candidate_id))
        if candidate is None:
            raise HTTPException(status_code=404, detail="待初始化书籍不存在或已被处理")
        return render_onboarding(request, catalog, candidate)

    @app.get("/library/{path_book_id}/paths", response_class=HTMLResponse)
    async def library_paths_page(request: Request, path_book_id: str) -> Any:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        layout = BookLayout(root)
        checked = _require_book_scope(app, path_book_id)
        return _template(
            templates,
            "library_paths.html",
            request,
            {
                "paths": _library_paths_payload(layout, checked),
                "csrf_token": app.state.csrf_token,
            },
        )

    @app.get("/library/{path_book_id}/export/latest")
    async def latest_export_redirect(path_book_id: str) -> Any:
        _require_book_scope(app, path_book_id)
        return RedirectResponse(url=f"/library/{path_book_id}/export/latest/")

    @app.get("/library/{path_book_id}/export/latest/", include_in_schema=False)
    async def latest_export_index(path_book_id: str) -> Any:
        return await latest_export_asset(path_book_id, "index.html")

    @app.get("/library/{path_book_id}/export/latest/{asset_path:path}")
    async def latest_export_asset(path_book_id: str, asset_path: str) -> Any:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        layout = BookLayout(root)
        latest = (
            layout.for_book(_require_book_scope(app, path_book_id)).edition("base").latest_export
        )
        path = (latest / asset_path).resolve()
        if latest.resolve() not in path.parents or not path.is_file():
            raise HTTPException(status_code=404, detail="latest export 不存在")
        return FileResponse(path)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request) -> Any:
        if app.state.book_id is None:
            return RedirectResponse(url="/library", status_code=307)
        checked_book = _check_id(str(app.state.book_id))
        catalog = _library_catalog_for_app(app)
        current_entry = (
            None if catalog is None else _catalog_entry_for_app(app, catalog, checked_book)
        )
        if catalog is not None:
            if current_entry is None:
                raise HTTPException(status_code=404, detail="书籍不在当前书库")
            if current_entry.creation_mode == "ORIGINAL" and current_entry.chapter_count == 0:
                return RedirectResponse(url=f"/books/{checked_book}/original", status_code=302)
            if not current_entry.studio_accessible:
                return render_onboarding(request, catalog, current_entry)
        selected_database = _database_for_book(app, checked_book)
        context = build_workbench_context(
            selected_database,
            checked_book,
            None,
            chapter_id=_query_id(request, "chapter_id"),
            draft_id=_query_id(request, "draft_id"),
            node=request.query_params.get("node", "overview"),
            mode=_workbench_mode(request),
            right_tab=request.query_params.get("right_tab", "prose"),
            state_tab=request.query_params.get("state_tab", "overview"),
            state_scope=request.query_params.get("state_scope", "character"),
            character_id=_query_id(request, "character_id"),
            truth_lens=request.query_params.get("truth_lens", "AUTHOR"),
            truth_id=_query_id(request, "truth_id"),
            include_future_truths=_query_flag(request, "include_future_truths"),
        )
        context["active_action"] = _query_action(request)
        context["planning_view"] = request.query_params.get("planning_view", "tasks")
        context["csrf_token"] = app.state.csrf_token
        context["library_catalog"] = None if catalog is None else catalog.to_dict()
        context["library_books"] = (
            [] if catalog is None else [item.to_dict() for item in catalog.entries]
        )
        context["current_catalog_id"] = f"book:{checked_book}"
        context["catalog_entry"] = None if current_entry is None else current_entry.to_dict()
        if current_entry is not None and current_entry.studio_accessible:
            context["book_status_label"] = current_entry.readiness_label
        context["workflow"] = workflow_context(
            selected_database,
            checked_book,
            edition_id=str(context["edition_id"]),
            chapter_id=(
                None
                if context.get("selected_chapter") is None
                else str(context["selected_chapter"]["chapter_id"])
            ),
            activity_id=_query_id(request, "activity_id"),
        )
        context["pending_activities"] = _resume_pending_actions(
            _database_for_book(app, checked_book), checked_book
        )
        context["activity_badge_count"] = int(
            context["workflow"]["activity_center"]["badge_count"]
        ) + sum(
            1
            for item in context["pending_activities"]
            if item["status"] in {"WAITING_FOR_CONTEXT", "CONTEXT_READY", "RESUMING"}
        )
        context["innovation_default"] = context["workflow"]["innovation_default"]
        return _template(templates, "workbench.html", request, context)

    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/workbench",
        response_class=HTMLResponse,
    )
    async def workbench_page(request: Request, path_book_id: str, edition_id: str) -> Any:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        catalog = _library_catalog_for_app(app)
        current_entry = (
            None if catalog is None else _catalog_entry_for_app(app, catalog, checked_book)
        )
        if catalog is not None:
            if current_entry is None:
                raise HTTPException(status_code=404, detail="书籍不在当前书库")
            if current_entry.creation_mode == "ORIGINAL" and current_entry.chapter_count == 0:
                return RedirectResponse(url=f"/books/{checked_book}/original", status_code=302)
            if not current_entry.studio_accessible:
                return render_onboarding(request, catalog, current_entry)
        try:
            context = build_workbench_context(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                chapter_id=_query_id(request, "chapter_id"),
                draft_id=_query_id(request, "draft_id"),
                node=request.query_params.get("node", "overview"),
                mode=_workbench_mode(request),
                right_tab=request.query_params.get("right_tab", "prose"),
                state_tab=request.query_params.get("state_tab", "overview"),
                state_scope=request.query_params.get("state_scope", "character"),
                character_id=_query_id(request, "character_id"),
                truth_lens=request.query_params.get("truth_lens", "AUTHOR"),
                truth_id=_query_id(request, "truth_id"),
                include_future_truths=_query_flag(request, "include_future_truths"),
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": str(exc), "details": {}},
            ) from exc
        context["active_action"] = _query_action(request)
        context["planning_view"] = request.query_params.get("planning_view", "tasks")
        context["csrf_token"] = app.state.csrf_token
        context["library_catalog"] = None if catalog is None else catalog.to_dict()
        context["library_books"] = (
            [] if catalog is None else [item.to_dict() for item in catalog.entries]
        )
        context["current_catalog_id"] = f"book:{checked_book}"
        context["catalog_entry"] = None if current_entry is None else current_entry.to_dict()
        if current_entry is not None and current_entry.studio_accessible:
            context["book_status_label"] = current_entry.readiness_label
        context["workflow"] = workflow_context(
            _database_for_book(app, checked_book),
            checked_book,
            edition_id=str(context["edition_id"]),
            chapter_id=(
                None
                if context.get("selected_chapter") is None
                else str(context["selected_chapter"]["chapter_id"])
            ),
            activity_id=_query_id(request, "activity_id"),
        )
        context["innovation_default"] = context["workflow"]["innovation_default"]
        return _template(templates, "workbench.html", request, context)

    @app.get(
        "/books/{path_book_id}/dashboard",
        response_class=HTMLResponse,
        include_in_schema=False,
    )
    async def legacy_dashboard_page(request: Request, path_book_id: str) -> Any:
        checked_book = _check_id(path_book_id)
        context = dashboard_context(_database_for_book(app, checked_book), checked_book)
        context["csrf_token"] = app.state.csrf_token
        return _template(templates, "index.html", request, context)

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/workbench")
    async def workbench_api(request: Request, path_book_id: str, edition_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        catalog = _library_catalog_for_app(app)
        if catalog is not None:
            entry = _catalog_entry_for_app(app, catalog, checked_book)
            if entry is None:
                raise HTTPException(status_code=404, detail="书籍不在当前书库")
            if not entry.studio_accessible:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "code": "STUDIO_NOT_READY",
                        "message": entry.author_summary,
                        "details": {"missing_requirements": list(entry.missing_requirements)},
                    },
                )
        return build_workbench_context(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_id=_query_id(request, "chapter_id"),
            draft_id=_query_id(request, "draft_id"),
            node=request.query_params.get("node", "overview"),
            mode=request.query_params.get("mode", "continue"),
            right_tab=request.query_params.get("right_tab", "prose"),
            state_tab=request.query_params.get("state_tab", "overview"),
            state_scope=request.query_params.get("state_scope", "character"),
            character_id=_query_id(request, "character_id"),
            truth_lens=request.query_params.get("truth_lens", "AUTHOR"),
            truth_id=_query_id(request, "truth_id"),
            include_future_truths=_query_flag(request, "include_future_truths"),
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/context")
    async def chapter_context_projection_api(
        path_book_id: str, edition_id: str, chapter_id: str
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        context = build_workbench_context(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_id=_check_id(chapter_id),
            node="chapter",
            mode="continue",
            right_tab="prose",
        )["chapter_context"]
        if not isinstance(context, dict):
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": "章节不存在", "details": {}},
            )
        return cast(dict[str, Any], context)

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/game-state")
    async def chapter_game_state_api(
        request: Request, path_book_id: str, edition_id: str, chapter_id: str
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return build_story_game_state(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_id=_check_id(chapter_id),
            character_id=_query_id(request, "character_id"),
            include_history=_query_flag(request, "include_history"),
        )

    @app.get(
        "/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/progression"
    )
    async def chapter_progression_api(
        path_book_id: str, edition_id: str, chapter_id: str
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        try:
            return build_progression_workspace(
                _database_for_book(app, checked_book),
                book_id=checked_book,
                edition_id=checked_edition,
                chapter_id=_check_id(chapter_id),
            )
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/progression-contracts")
    async def progression_contracts_api(
        path_book_id: str, edition_id: str
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        records = list_contract_records(
            _database_for_book(app, checked_book),
            book_id=checked_book,
            edition_id=checked_edition,
        )
        return {
            "records": [record.model_dump(mode="json") for record in records],
            "canon_changed": False,
        }

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/progression-contracts/discovery"
    )
    async def prepare_kernel_contract_discovery_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: KernelContractDiscoveryRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return prepare_kernel_contract_discovery(
            _database_for_book(app, checked_book),
            book_id=checked_book,
            edition_id=checked_edition,
            context_chapter_id=payload.context_chapter_id,
        )

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/progression-contracts/"
        "discovery/{handoff_id}/collect"
    )
    async def collect_kernel_contract_discovery_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        handoff_id: str,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        checked_handoff = _check_id(handoff_id)
        selected_database = _database_for_book(app, checked_book)
        item = get_handoff(selected_database, checked_handoff)
        if (
            str(item.get("book_id")) != checked_book
            or str(item.get("edition_id")) != checked_edition
            or str(item.get("handoff_type"))
            != HandoffType.KERNEL_CONTRACT_DISCOVERY.value
        ):
            raise HTTPException(status_code=404, detail="Kernel discovery handoff scope 不匹配")
        try:
            return import_kernel_contract_discovery(
                selected_database,
                handoff_id=checked_handoff,
            )
        except HandoffWorkflowError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/progression-contracts/"
        "lexical-fallback"
    )
    async def lexical_fallback_progression_contracts_api(
        request: Request, path_book_id: str, edition_id: str
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return infer_existing_contract_proposals_lexical_fallback(
            _database_for_book(app, checked_book),
            book_id=checked_book,
            edition_id=checked_edition,
        )

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/progression-contracts/"
        "{contract_record_id}/confirm"
    )
    async def confirm_progression_contract_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        contract_record_id: str,
        payload: ProgressionContractConfirmationRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        selected_database = _database_for_book(app, checked_book)
        checked_record_id = _check_id(contract_record_id)
        current = get_contract_record(selected_database, checked_record_id)
        if (
            current is None
            or current.book_id != checked_book
            or current.edition_id != checked_edition
        ):
            raise HTTPException(status_code=404, detail="Contract Proposal 不属于当前作品版本")
        record = confirm_contract(
            selected_database,
            checked_record_id,
            effective_from_boundary=payload.effective_from_boundary,
            author_notes=payload.author_notes,
        )
        return {"record": record.model_dump(mode="json"), "canon_changed": False}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/author-control")
    async def author_control_api(path_book_id: str, edition_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return author_control_view(
            _database_for_book(app, checked_book), checked_book, checked_edition
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/author-truths")
    async def author_truths_api(
        path_book_id: str,
        edition_id: str,
        chapter_ordinal: int | None = None,
        include_future: bool = False,
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        truths = list_author_truths(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_ordinal=chapter_ordinal,
            include_future=include_future,
        )
        return {"truths": truths, "canon_changed": False}

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/author-truths")
    async def create_author_truth_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: AuthorTruthInput,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        truth = create_author_truth(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            payload,
        )
        return {"truth": truth, "canon_changed": False, "knowledge_changed": False}

    @app.patch("/api/books/{path_book_id}/editions/{edition_id}/author-truths/{truth_id}")
    async def update_author_truth_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        truth_id: str,
        payload: AuthorTruthUpdateRequest,
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        try:
            truth = update_author_truth(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                _check_id(truth_id),
                payload.changes,
            )
        except ValueError as exc:
            return _error(exc)
        return {"truth": truth, "canon_changed": False, "knowledge_changed": False}

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/author-truths/{truth_id}/compatibility"
    )
    async def truth_compatibility_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        truth_id: str,
        payload: TruthCompatibilityRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        truth = evaluate_truth_compatibility(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            _check_id(truth_id),
            evidence=list(payload.evidence),
        )
        return {"truth": truth, "canon_changed": False, "knowledge_changed": False}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/open-questions")
    async def open_questions_api(
        path_book_id: str,
        edition_id: str,
        include_resolved: bool = False,
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return {
            "questions": list_open_creative_questions(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                include_resolved=include_resolved,
            ),
            "canon_changed": False,
        }

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/open-questions")
    async def create_open_question_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: OpenCreativeQuestionRequest,
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        try:
            question = create_open_creative_question(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                title=payload.title,
                question=payload.question,
                subject_type=payload.subject_type,
                subject_id=payload.subject_id,
                horizon=payload.horizon,
            )
        except ValueError as exc:
            return _error(exc)
        return {"question": question, "canon_changed": False}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/secret-candidates")
    async def secret_candidates_api(
        path_book_id: str,
        edition_id: str,
        include_resolved: bool = False,
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return {
            "candidates": list_secret_candidates(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                include_resolved=include_resolved,
            ),
            "canon_changed": False,
        }

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/secret-candidates")
    async def create_secret_candidate_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: SecretCandidateRequest,
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        try:
            candidate = create_secret_candidate(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                title=payload.title,
                statement=payload.statement,
                truth_type=payload.truth_type,
                subject_type=payload.subject_type,
                subject_id=payload.subject_id,
                evidence=payload.evidence,
                confidence=payload.confidence,
                source=payload.source,
            )
        except ValueError as exc:
            return _error(exc)
        return {"candidate": candidate, "canon_changed": False}

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/secret-candidates/{candidate_id}/resolve"
    )
    async def resolve_secret_candidate_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        candidate_id: str,
        payload: SecretCandidateResolutionRequest,
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        try:
            result = resolve_secret_candidate(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                _check_id(candidate_id),
                action=payload.action,
                effective_from_chapter=payload.effective_from_chapter,
                compatibility_evidence=payload.compatibility_evidence,
            )
        except ValueError as exc:
            return _error(exc)
        return {**result, "canon_changed": False}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/truth-knowledge")
    async def truth_knowledge_api(
        path_book_id: str,
        edition_id: str,
        chapter_ordinal: int,
        truth_id: str | None = None,
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return truth_knowledge_view(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_ordinal=chapter_ordinal,
            truth_id=None if truth_id is None else _check_id(truth_id),
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/truth-lens")
    async def truth_lens_api(
        path_book_id: str,
        edition_id: str,
        chapter_ordinal: int,
        lens: str = "AUTHOR",
        character_id: str | None = None,
        include_future: bool = False,
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return project_truth_lens(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_ordinal=chapter_ordinal,
            lens=lens,
            character_id=character_id,
            include_future=include_future,
        )

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/author-truths/{truth_id}/reader-knowledge"
    )
    async def reader_knowledge_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        truth_id: str,
        payload: KnowledgeUpdateRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        result = set_reader_knowledge(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            _check_id(truth_id),
            state=payload.state,
            chapter_ordinal=payload.chapter_ordinal,
            evidence=payload.evidence,
            mode=payload.mode,
        )
        return {**result, "canon_changed": False}

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/author-truths/"
        "{truth_id}/character-knowledge"
    )
    async def character_knowledge_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        truth_id: str,
        payload: KnowledgeUpdateRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        if not payload.character_id:
            raise HTTPException(status_code=422, detail="character_id 必填")
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        result = set_character_truth_knowledge(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            _check_id(truth_id),
            payload.character_id,
            state=payload.state,
            chapter_ordinal=payload.chapter_ordinal,
            evidence=payload.evidence,
            mode=payload.mode,
        )
        return {**result, "canon_changed": False}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/reveal-agenda")
    async def reveal_agenda_api(
        path_book_id: str, edition_id: str, chapter_ordinal: int
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return build_reveal_agenda(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_ordinal,
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/reveal-plans")
    async def create_reveal_plan_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: RevealPlanInput,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        plan = create_reveal_plan(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            payload,
        )
        return {"plan": plan, "canon_changed": False, "knowledge_changed": False}

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/reveal-agenda/override")
    async def reveal_agenda_override_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: RevealAgendaOverrideRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        result = override_reveal_agenda(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            truth_id=payload.truth_id,
            chapter_ordinal=payload.chapter_ordinal,
            agenda_bucket=payload.agenda_bucket,
            reveal_depth=payload.reveal_depth,
            reason=payload.reason,
        )
        return {**result, "canon_changed": False}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/secret-board")
    async def secret_board_api(
        path_book_id: str,
        edition_id: str,
        chapter_ordinal: int,
        horizon: str | None = None,
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return build_secret_board(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            chapter_ordinal=chapter_ordinal,
            horizon=horizon,
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/hidden-items")
    async def hidden_item_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: HiddenItemRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        selected_database = _database_for_book(app, checked_book)
        item_id = stable_id(
            "author-hidden-item",
            checked_book,
            checked_edition,
            payload.name.strip(),
            payload.location_id or "unplaced",
            str(payload.effective_from_chapter),
        )
        truth = create_author_truth(
            selected_database,
            checked_book,
            checked_edition,
            {
                "truth_type": "ITEM_SECRET",
                "subject_type": "ITEM",
                "subject_id": item_id,
                "title": f"隐藏物品：{payload.name}",
                "statement": f"{payload.name} 确实存在，但当前不等于任何角色已经持有。",
                "description": payload.description,
                "status": "ACTIVE_TRUTH",
                "effective_from_chapter": payload.effective_from_chapter,
                "metadata": {
                    "item_id": item_id,
                    "category": payload.category.strip().upper(),
                    "exists": True,
                    "location_id": payload.location_id,
                    "intended_owner_id": payload.owner_id,
                    "owner_id": None,
                    "holder_id": None,
                    "known_by": [],
                    "reader_visibility": "UNKNOWN",
                    "horizon": payload.horizon.strip().upper(),
                    "priority": payload.priority,
                    "ownership_layer": "SEPARATE_FROM_EXISTENCE",
                },
            },
        )
        plan = None
        if payload.target_chapter_min is not None:
            plan = create_reveal_plan(
                selected_database,
                checked_book,
                checked_edition,
                {
                    "truth_id": truth["truth_id"],
                    "target": "READER",
                    "target_chapter_min": payload.target_chapter_min,
                    "target_chapter_max": payload.target_chapter_max,
                    "horizon": payload.horizon,
                    "priority": payload.priority,
                    "reveal_depth": payload.reveal_depth,
                    "strategy": "作者通过 Hidden Item 表单创建的揭示计划",
                },
            )
        return {
            "truth": truth,
            "plan": plan,
            "world_state_changed": False,
            "knowledge_changed": False,
            "canon_changed": False,
        }

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/book-profile")
    async def book_profile_api(path_book_id: str, edition_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return load_effective_book_profile(
            _database_for_book(app, checked_book), checked_book, checked_edition
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/book-profile/edits")
    async def book_profile_edit_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: BookProfileEditRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return edit_book_profile(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            dimension=payload.dimension,
            operation=payload.operation,
            content=payload.content,
            strength=payload.strength,
            reason=payload.reason,
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/book-profile/proposals")
    async def book_profile_proposal_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: BookProfileProposalRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return create_book_profile_refresh_proposal(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            source_type=payload.source_type,
            proposed_baseline=payload.proposed_baseline,
            summary=payload.summary,
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/book-profile/reanalysis")
    async def book_profile_reanalysis_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: ProfileReanalysisRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        result = create_profile_reanalysis_handoff(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            context_chapter_id=payload.context_chapter_id,
        )
        return {**result, "canon_changed": False, "effective_profile_changed": False}

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/book-profile/proposals/"
        "{proposal_id}/resolve"
    )
    async def book_profile_proposal_resolution_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        proposal_id: str,
        payload: BookProfileProposalResolutionRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        return resolve_book_profile_refresh_proposal(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            _check_id(proposal_id),
            action=payload.action,
            edited_baseline=payload.edited_baseline,
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/author-commands")
    async def author_command_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: AuthorStateCommand,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        resolution = execute_author_command(
            _database_for_book(app, checked_book), checked_book, checked_edition, payload
        )
        return resolution.model_dump(mode="json")

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/source-state-hydration/{handoff_id}/collect"
    )
    async def collect_source_state_hydration_api(
        request: Request, path_book_id: str, edition_id: str, handoff_id: str
    ) -> Any:
        """Collect a Codex-written result file; Web never executes the model."""

        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        checked_handoff = _check_id(handoff_id)
        selected_database = _database_for_book(app, checked_book)
        try:
            item = get_handoff(selected_database, checked_handoff)
            if (
                str(item.get("book_id")) != checked_book
                or str(item.get("edition_id")) != checked_edition
                or str(item.get("handoff_type")) != HandoffType.SOURCE_STATE_HYDRATION.value
            ):
                raise HandoffWorkflowError("hydration handoff scope 不匹配")
            status = str(item.get("status"))
            if status == HandoffStatus.COMPLETED.value:
                return {"handoff_id": checked_handoff, "status": status, "already_completed": True}
            result_path = Path(str(item.get("result_path") or ""))
            if not result_path.is_file():
                raise HandoffWorkflowError("尚未找到 Codex 写入的 result.json")
            claim_token = str(item.get("claim_token") or "")
            if not claim_token:
                raise HandoffWorkflowError("handoff 尚未由 Codex 桌面端领取")
            if status != HandoffStatus.RUNNING.value:
                raise HandoffWorkflowError(
                    "hydration handoff 必须先通过 novel workflow start 进入 RUNNING"
                )
            completed = complete_handoff(
                selected_database,
                checked_handoff,
                claim_token,
                result_path,
            )
            return completed
        except (HandoffWorkflowError, OSError, ValueError, json.JSONDecodeError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/author-intents")
    async def author_intent_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: AuthorIntentRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        resolution = execute_author_intent(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            intent_type=payload.intent_type,
            subject_type=payload.subject_type,
            subject_id=payload.subject_id,
            title=payload.title,
            description=payload.description,
            horizon=payload.horizon,
            priority=payload.priority,
            target_chapter_id=payload.target_chapter_id,
            payload=payload.payload,
        )
        return resolution.model_dump(mode="json")

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/author-tasks")
    async def author_task_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: AuthorTaskRequest,
    ) -> dict[str, Any]:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        resolution = execute_author_task(
            _database_for_book(app, checked_book),
            checked_book,
            checked_edition,
            title=payload.title,
            task_type=payload.task_type,
            description=payload.description,
            horizon=payload.horizon,
            lifecycle_status=payload.lifecycle_status,
            priority=payload.priority,
            subject_type=payload.subject_type,
            subject_id=payload.subject_id,
            context_chapter_id=payload.context_chapter_id,
            context_chapter_ordinal=payload.context_chapter_ordinal,
            due_chapter_ordinal=payload.due_chapter_ordinal,
            payload=payload.payload,
        )
        return resolution.model_dump(mode="json")

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/drafts/{draft_id}/content")
    async def save_draft_content_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        draft_id: str,
        payload: DraftContentRequest,
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        try:
            return save_draft_content(
                _database_for_book(app, _check_id(path_book_id)),
                _check_id(path_book_id),
                _check_id(draft_id),
                payload.content,
                edition_id=_check_id(edition_id),
                expected_content_sha256=payload.expected_content_sha256,
            )
        except (OSError, ValueError, RuntimeError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/drafts/{draft_id}/metadata")
    async def repair_draft_metadata_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        draft_id: str,
        payload: DraftMetadataRepairRequest,
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        try:
            return repair_draft_metadata(
                _database_for_book(app, _check_id(path_book_id)),
                _check_id(path_book_id),
                _check_id(draft_id),
                payload.metadata,
                edition_id=_check_id(edition_id),
                expected_content_sha256=payload.expected_content_sha256,
            )
        except (OSError, ValueError, RuntimeError) as exc:
            return _error(exc)

    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/atlas",
        response_class=HTMLResponse,
    )
    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/story-atlas",
        response_class=HTMLResponse,
    )
    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/atlas/{atlas_view}",
        response_class=HTMLResponse,
    )
    async def atlas_page(
        request: Request,
        path_book_id: str,
        edition_id: str,
        atlas_view: str = "overview",
    ) -> Any:
        try:
            checked_book = _check_id(path_book_id)
            checked_edition = _check_id(edition_id)
            context = atlas_context(
                _database_for_book(app, checked_book),
                checked_book,
                checked_edition,
                view=_check_id(atlas_view),
                status=request.query_params.get("status"),
                horizon=request.query_params.get("horizon"),
                query=request.query_params.get("q"),
            )
        except AtlasError as exc:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": str(exc), "details": {}},
            ) from exc
        context["csrf_token"] = app.state.csrf_token
        return _template(templates, "atlas.html", request, context)

    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/initialization",
        response_class=HTMLResponse,
    )
    async def initialization_page(request: Request, path_book_id: str, edition_id: str) -> Any:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        context = {
            "book_id": checked_book,
            "edition_id": checked_edition,
            "initialization": latest_initialization(
                _database_for_book(app, checked_book), checked_book, checked_edition
            ),
            "csrf_token": app.state.csrf_token,
        }
        return _template(templates, "initialization.html", request, context)

    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}",
        response_class=HTMLResponse,
    )
    async def chapter_page(
        request: Request, path_book_id: str, edition_id: str, chapter_id: str
    ) -> Any:
        try:
            checked_book = _check_id(path_book_id)
            context = chapter_context(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                _check_id(chapter_id),
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": str(exc), "details": {}},
            ) from exc
        context["csrf_token"] = app.state.csrf_token
        return _template(templates, "chapter.html", request, context)

    @app.get("/books/{path_book_id}/editions/{edition_id}/missing", response_class=HTMLResponse)
    async def missing_page(request: Request, path_book_id: str, edition_id: str) -> Any:
        book = _check_id(path_book_id)
        edition = _check_id(edition_id)
        selected_database = _database_for_book(app, book)
        selected_database.initialize()
        with selected_database.connect() as connection:
            edition_rows = edition_chapters(connection, book, edition)
        chapter = edition_rows[-1] if edition_rows else None
        if chapter is None:
            return _template(
                templates,
                "missing.html",
                request,
                {"run": {"run_id": "", "results": []}, "csrf_token": app.state.csrf_token},
            )
        run = MetricsAssembler(selected_database).rebuild(
            book, edition_id=edition, scope_type="CHAPTER", scope_id=str(chapter["chapter_id"])
        )
        segments = list_segments(
            selected_database,
            book,
            edition_id=edition,
            chapter_id=str(chapter["chapter_id"]),
        )
        registry = load_registry()
        component_definitions: dict[str, dict[str, Any]] = {}
        for metric in run["results"]:
            definition = registry.metric(str(metric["metric_id"]))
            component_definitions[str(metric["metric_id"])] = {
                component_id: {
                    "display_name": component.display_name,
                    "description": component.description,
                    "minimum": component.minimum,
                    "maximum": component.maximum,
                    "value_type": component.value_type,
                    "evidence_required": component.evidence_required,
                    "allowed_source_kinds": [item.value for item in component.allowed_source_kinds],
                }
                for component_id, component in definition.components.items()
            }
        return _template(
            templates,
            "missing.html",
            request,
            {
                "run": run,
                "book_id": book,
                "edition_id": edition,
                "scope_id": str(chapter["chapter_id"]),
                "chapter": chapter,
                "segments": segments,
                "component_definitions": component_definitions,
                "csrf_token": app.state.csrf_token,
            },
        )

    @app.get("/books/{path_book_id}/workflow", include_in_schema=False)
    async def workflow_page(request: Request, path_book_id: str) -> Any:
        checked_book = _check_id(path_book_id)
        selected_database = _database_for_book(app, checked_book)
        context = workflow_context(
            selected_database,
            checked_book,
            edition_id=request.query_params.get("edition_id"),
            chapter_id=_query_id(request, "chapter_id"),
        )
        action = _query_action(request) or "continue"
        query = {"action": action}
        if context.get("current_chapter"):
            query["chapter_id"] = str(context["current_chapter"]["chapter_id"])
        target = (
            f"/books/{checked_book}/editions/{context['edition_id']}/workbench?{urlencode(query)}"
        )
        return RedirectResponse(url=target, status_code=302)

    @app.get("/books/{path_book_id}/jobs", response_class=HTMLResponse)
    async def jobs_page(request: Request, path_book_id: str) -> Any:
        checked = _check_id(path_book_id)
        context = {
            "book_id": checked,
            "handoffs": list_handoffs(_database_for_book(app, checked), checked),
        }
        context["csrf_token"] = app.state.csrf_token
        return _template(templates, "jobs.html", request, context)

    @app.get(
        "/books/{path_book_id}/editions/{edition_id}/draft-review", response_class=HTMLResponse
    )
    async def draft_review_page(request: Request, path_book_id: str, edition_id: str) -> Any:
        selected_database = _database_for_book(app, _check_id(path_book_id))
        selected_database.initialize()
        with selected_database.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM drafts WHERE book_id=? AND edition_id=? ORDER BY created_at DESC",
                (_check_id(path_book_id), _check_id(edition_id)),
            ).fetchall()
            drafts: list[dict[str, Any]] = []
            for row in rows:
                draft = dict(row)
                draft["display_status"] = (
                    "VALIDATED_DRAFT"
                    if str(draft["status"]) == "VALIDATED"
                    else str(draft["status"])
                )
                draft_path = Path(str(draft.get("file_path") or ""))
                try:
                    draft["content"] = (
                        draft_path.read_text(encoding="utf-8")[:200_000]
                        if draft_path.is_file()
                        else ""
                    )
                except OSError:
                    draft["content"] = ""
                try:
                    draft["output"] = json.loads(str(draft.get("output_json") or "{}"))
                except ValueError:
                    draft["output"] = {"raw": draft.get("output_json", "")}
                reports = connection.execute(
                    "SELECT validator, severity, passed, report_json, run_id "
                    "FROM validation_reports WHERE draft_id=? AND edition_id=? "
                    "AND run_id=? ORDER BY validator, created_at",
                    (
                        str(row["draft_id"]),
                        str(row["edition_id"]),
                        draft.get("validation_run_id"),
                    ),
                ).fetchall()
                draft["validation_reports"] = []
                for report in reports:
                    item = dict(report)
                    try:
                        item["report"] = json.loads(str(item.get("report_json") or "{}"))
                    except ValueError:
                        item["report"] = {"raw": item.get("report_json", "")}
                    draft["validation_reports"].append(item)
                draft["candidates"] = []
                for candidate_row in connection.execute(
                    "SELECT candidate_id, rank, primary_thread_id, primary_function, "
                    "selection_status, status, score_json FROM candidate_plans "
                    "WHERE book_id=? AND edition_id=? ORDER BY rank, created_at",
                    (_check_id(path_book_id), _check_id(edition_id)),
                ).fetchall():
                    candidate = dict(candidate_row)
                    try:
                        score_payload = json.loads(str(candidate.get("score_json") or "{}"))
                    except ValueError:
                        score_payload = {}
                    candidate["score_payload"] = score_payload
                    draft["candidates"].append(candidate)
                contract = connection.execute(
                    "SELECT * FROM chapter_contracts WHERE contract_id=?",
                    (str(row["contract_id"]),),
                ).fetchone()
                draft["contract"] = None if contract is None else dict(contract)
                try:
                    draft["contract_payload"] = (
                        {}
                        if contract is None
                        else json.loads(str(contract["contract_json"] or "{}"))
                    )
                except ValueError:
                    draft["contract_payload"] = {"raw": contract["contract_json"]}
                rhythm = connection.execute(
                    "SELECT snapshot_json FROM rhythm_diagnostic_snapshots "
                    "WHERE book_id=? AND edition_id=? ORDER BY as_of_chapter DESC, "
                    "created_at DESC LIMIT 1",
                    (_check_id(path_book_id), _check_id(edition_id)),
                ).fetchone()
                try:
                    draft["rhythm"] = (
                        {} if rhythm is None else json.loads(str(rhythm["snapshot_json"] or "{}"))
                    )
                except ValueError:
                    draft["rhythm"] = {"raw": rhythm["snapshot_json"]}
                draft["promises"] = [
                    dict(promise)
                    for promise in connection.execute(
                        "SELECT promise_id, statement, status, progress, target_max_age "
                        "FROM promises WHERE book_id=? AND edition_id=? ORDER BY importance DESC",
                        (_check_id(path_book_id), _check_id(edition_id)),
                    ).fetchall()
                ]
                draft["metric_changes"] = draft["output"].get("metric_changes", [])
                draft["state_changes"] = draft["output"].get("state_changes", [])
                draft["approval_preview"] = {
                    "draft_id": draft["draft_id"],
                    "current_status": draft["status"],
                    "canon_commit": False,
                    "author_confirmation_required": True,
                    "continuation_approval_command": (
                        f"novel approve --book-id {_check_id(path_book_id)} "
                        f"--draft-id {draft['draft_id']} --confirm '批准写入正史'"
                    ),
                    "revision_approval_command": "novel revision approve --confirm '批准改写版本'",
                    "note": "此预览不会写入 Canon；批准必须由作者在 CLI 明确执行。",
                }
                drafts.append(draft)
        return _template(
            templates,
            "draft_review.html",
            request,
            {
                "drafts": drafts,
                "book_id": _check_id(path_book_id),
                "edition_id": _check_id(edition_id),
                "csrf_token": app.state.csrf_token,
            },
        )

    @app.get("/api/books")
    async def books_api() -> list[dict[str, Any]]:
        if app.state.library_root is not None:
            books: list[dict[str, Any]] = []
            for record in BookRegistry(BookLayout(app.state.library_root)).list():
                book_database = Database(record.root / "_system" / "state.sqlite3")
                if not book_database.path.is_file():
                    continue
                book_database.initialize()
                with book_database.connect() as connection:
                    row = connection.execute(
                        "SELECT * FROM books WHERE book_id=?", (record.book_id,)
                    ).fetchone()
                    if row is not None:
                        books.append(dict(row))
            return sorted(
                books,
                key=lambda item: (
                    str(item.get("title", "")),
                    str(item.get("book_id", "")),
                ),
            )
        database.initialize()
        with database.connect() as connection:
            rows = connection.execute("SELECT * FROM books ORDER BY title, book_id").fetchall()
            return [dict(row) for row in rows]

    @app.get("/api/books/{path_book_id}/editions")
    async def editions_api(path_book_id: str) -> list[dict[str, Any]]:
        checked_book = _check_id(path_book_id)
        return [
            item.model_dump(mode="json")
            for item in list_editions(_database_for_book(app, checked_book), checked_book)
        ]

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/chapters")
    async def chapters_api(path_book_id: str, edition_id: str) -> list[dict[str, Any]]:
        checked_book = _check_id(path_book_id)
        selected_database = _database_for_book(app, checked_book)
        selected_database.initialize()
        with selected_database.connect() as connection:
            return edition_chapters(connection, checked_book, _check_id(edition_id))

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/atlas")
    @app.get("/api/books/{path_book_id}/editions/{edition_id}/story-atlas")
    async def atlas_overview_api(path_book_id: str, edition_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        return public_atlas_overview(
            _database_for_book(app, checked_book), checked_book, _check_id(edition_id)
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/initialization")
    async def initialization_api(path_book_id: str, edition_id: str) -> dict[str, Any] | None:
        checked_book = _check_id(path_book_id)
        return latest_initialization(
            _database_for_book(app, checked_book), checked_book, _check_id(edition_id)
        )

    @app.get("/api/books/{path_book_id}/studio-readiness")
    async def studio_readiness_api(path_book_id: str) -> dict[str, Any]:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="书库未配置")
        layout = BookLayout(root)
        checked_book = _require_book_scope(app, path_book_id)
        try:
            record = BookRegistry(layout).record(checked_book)
        except (OSError, ValueError) as exc:
            raise HTTPException(status_code=404, detail="书籍不存在") from exc
        return studio_readiness(layout, record).to_dict()

    @app.get("/api/books/{path_book_id}/studio-access")
    async def studio_access_api(path_book_id: str) -> dict[str, Any]:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="书库未配置")
        layout = BookLayout(root)
        checked_book = _require_book_scope(app, path_book_id)
        try:
            record = BookRegistry(layout).record(checked_book)
        except (OSError, ValueError) as exc:
            raise HTTPException(status_code=404, detail="书籍不存在") from exc
        return studio_access(layout, record).to_dict()

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/initialization")
    async def initialization_handoff_api(
        request: Request, path_book_id: str, edition_id: str
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        try:
            checked_book = _check_id(path_book_id)
            raw = await request.body()
            payload = json.loads(raw) if raw else {}
            if not isinstance(payload, dict):
                raise ValueError("初始化请求必须是 object")
            depth = InitializationDepth(
                str(payload.get("depth") or InitializationDepth.BALANCED).upper()
            )
            author_goal = str(payload.get("author_goal") or "CONTINUE").upper()
            if author_goal not in {"CONTINUE", "UNDERSTAND", "REWRITE", "AUDIT"}:
                raise ValueError("创作目标无效")
            selected_database = _database_for_book(app, checked_book)
            current = latest_initialization(selected_database, checked_book, _check_id(edition_id))
            if current is None:
                create_initialization(
                    selected_database,
                    checked_book,
                    edition_id=_check_id(edition_id),
                    depth=depth,
                    requested_action=f"GOAL_{author_goal}",
                )
            else:
                upgrade_initialization(
                    selected_database,
                    checked_book,
                    edition_id=_check_id(edition_id),
                    depth=depth,
                    requested_action=f"GOAL_{author_goal}",
                )
            return create_initialization_handoff(
                selected_database,
                checked_book,
                edition_id=_check_id(edition_id),
                requested_stage="NOVEL_INITIALIZATION",
            )
        except Exception as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/initialization/deepen")
    async def initialization_deepen_api(
        request: Request, path_book_id: str, edition_id: str
    ) -> Any:
        verify_csrf(request, request.headers.get("X-CSRF-Token"))
        try:
            payload = await request.json()
            if not isinstance(payload, dict):
                raise ValueError("补齐请求必须是 object")
            checked_book = _require_book_scope(app, path_book_id)
            selected_database = _database_for_book(app, checked_book)
            result = prepare_action_deepening(
                selected_database,
                checked_book,
                edition_id=_check_id(edition_id),
                action=str(payload.get("action") or ""),
                target_chapter_id=(
                    str(payload["target_chapter_id"]) if payload.get("target_chapter_id") else None
                ),
            )
            if result["status"] != "ACTION_CONTEXT_READY":
                result["handoff"] = create_initialization_handoff(
                    selected_database,
                    checked_book,
                    edition_id=_check_id(edition_id),
                    requested_stage="NOVEL_INITIALIZATION",
                )
            return result
        except Exception as exc:
            return _error(exc)

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/atlas/visuals/{visual_name}")
    async def atlas_visual_api(path_book_id: str, edition_id: str, visual_name: str) -> Response:
        if not re.fullmatch(r"[A-Za-z0-9._-]+\.svg", visual_name):
            raise HTTPException(status_code=400, detail="visual name 无效")
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        selected_database = _database_for_book(app, checked_book)
        overview = get_atlas_overview(selected_database, checked_book, checked_edition)
        index = overview.get("index") or {}
        raw_root = str(index.get("artifact_root") or "")
        if not raw_root:
            raise HTTPException(status_code=404, detail="visual 不存在")
        try:
            base = atlas_root(selected_database, checked_book, checked_edition).resolve()
            root = Path(raw_root).resolve()
        except (AtlasError, OSError, ValueError) as exc:
            raise HTTPException(status_code=404, detail="visual 不存在") from exc
        if root != base and base not in root.parents:
            raise HTTPException(status_code=404, detail="visual 不存在")
        path = (root / "visuals" / visual_name).resolve()
        if root not in path.parents or not path.is_file():
            raise HTTPException(status_code=404, detail="visual 不存在")
        return Response(content=path.read_text(encoding="utf-8"), media_type="image/svg+xml")

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/atlas/reports")
    async def atlas_reports_api(path_book_id: str, edition_id: str) -> dict[str, str]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        selected_database = _database_for_book(app, checked_book)
        overview = get_atlas_overview(selected_database, checked_book, checked_edition)
        index = overview.get("index") or {}
        raw_root = str(index.get("artifact_root") or "")
        if not raw_root:
            return {}
        try:
            base = atlas_root(selected_database, checked_book, checked_edition).resolve()
            root = Path(raw_root).resolve()
        except (AtlasError, OSError, ValueError) as exc:
            raise HTTPException(status_code=404, detail="Atlas reports 不存在") from exc
        if root != base and base not in root.parents:
            raise HTTPException(status_code=404, detail="Atlas reports 不存在")
        reports: dict[str, str] = {}
        if root.is_dir():
            for path in sorted((root / "reports").glob("*.md")):
                try:
                    reports[path.name] = path.read_text(encoding="utf-8")[:250_000]
                except OSError:
                    continue
        return reports

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/atlas/graphs/{graph_type}")
    async def atlas_graph_api(
        path_book_id: str,
        edition_id: str,
        graph_type: str,
        status: str | None = None,
        horizon: str | None = None,
        node_type: str | None = None,
        q: str | None = None,
        limit: int = 250,
    ) -> dict[str, Any]:
        try:
            if graph_type not in GRAPH_TYPES:
                raise AtlasError(f"不支持的 Atlas graph_type：{graph_type}")
            checked_book = _check_id(path_book_id)
            return atlas_graph_view(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                graph_type,
                status=status,
                horizon=horizon,
                node_type=node_type,
                query=q,
                limit=limit,
            )
        except AtlasError as exc:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": str(exc), "details": {}},
            ) from exc

    @app.get(
        "/api/books/{path_book_id}/editions/{edition_id}/atlas/graphs/{graph_type}/nodes/{entry_id}"
    )
    async def atlas_node_api(
        path_book_id: str, edition_id: str, graph_type: str, entry_id: str
    ) -> dict[str, Any]:
        try:
            checked_book = _check_id(path_book_id)
            return atlas_entry_detail(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                graph_type,
                _check_id(entry_id),
            )
        except AtlasError as exc:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": str(exc), "details": {}},
            ) from exc

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/atlas/history")
    async def atlas_history_api(path_book_id: str, edition_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        overview = public_atlas_overview(
            _database_for_book(app, checked_book), checked_book, _check_id(edition_id)
        )
        return {"history": overview.get("history", [])}

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/atlas/actions")
    async def atlas_action_api(
        path_book_id: str,
        edition_id: str,
        request: Request,
        payload: AtlasActionRequest,
    ) -> Any:
        verify_csrf(request, None)
        try:
            checked_book = _check_id(path_book_id)
            action = AtlasAction.model_validate(
                {
                    "action_type": payload.action_type,
                    "target_id": payload.target_id,
                    "payload": payload.payload,
                    "actor": "AUTHOR",
                }
            )
            return record_atlas_action(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                action,
                atlas_id=payload.expected_atlas_id,
                expected_atlas_version=payload.expected_atlas_version,
                expected_manifest_hash=payload.expected_manifest_hash,
            )
        except (AtlasError, ValueError) as exc:
            return _error(exc)

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}")
    async def chapter_detail_api(
        path_book_id: str, edition_id: str, chapter_id: str
    ) -> dict[str, Any]:
        try:
            checked_book = _check_id(path_book_id)
            return chapter_context(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                _check_id(chapter_id),
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": str(exc), "details": {}},
            ) from exc

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/segments")
    async def segments_api(
        path_book_id: str, edition_id: str, chapter_id: str
    ) -> list[dict[str, Any]]:
        checked_book = _check_id(path_book_id)
        return cast(
            list[dict[str, Any]],
            chapter_context(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                _check_id(chapter_id),
            )["segments"],
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/metrics")
    async def metrics_api(path_book_id: str, edition_id: str, chapter_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        return chapter_context(
            _database_for_book(app, checked_book),
            checked_book,
            _check_id(edition_id),
            _check_id(chapter_id),
        )

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/metrics/bootstrap/prepare")
    async def metric_bootstrap_prepare_api(
        path_book_id: str, edition_id: str, request: Request
    ) -> Any:
        verify_csrf(request, None)
        try:
            checked_book = _check_id(path_book_id)
            checked_edition = _check_id(edition_id)
            selected_database = _database_for_book(app, checked_book)
            initialization = latest_initialization(selected_database, checked_book, checked_edition)
            if not initialization:
                raise ValueError("尚未创建初始化包，无法准备语义指标任务")
            manifest = initialization.get("manifest") or {}
            initialization_id = str(manifest.get("initialization_id") or "")
            if not initialization_id:
                raise ValueError("初始化 manifest 缺少 initialization_id")
            return prepare_metric_bootstrap(
                selected_database,
                checked_book,
                edition_id=checked_edition,
                initialization_id=initialization_id,
                recent_detailed_window=50,
            )
        except (InitializationError, OSError, ValueError) as exc:
            return _error(exc)

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/metric-history")
    async def metric_history_api(
        path_book_id: str, edition_id: str, scope_type: str = "CHAPTER", scope_id: str = ""
    ) -> list[dict[str, Any]]:
        if not scope_id:
            raise HTTPException(
                status_code=400,
                detail={"code": "MISSING_SCOPE_ID", "message": "需要 scope_id"},
            )
        checked_book = _check_id(path_book_id)
        return metric_history(
            _database_for_book(app, checked_book),
            checked_book,
            _check_id(edition_id),
            scope_type,
            _check_id(scope_id),
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/metrics/observations/history")
    async def observation_history_api(
        path_book_id: str,
        edition_id: str,
        scope_type: str = "CHAPTER",
        scope_id: str = "",
    ) -> list[dict[str, Any]]:
        if not scope_id:
            raise HTTPException(
                status_code=400,
                detail={"code": "MISSING_SCOPE_ID", "message": "需要 scope_id"},
            )
        checked_book = _check_id(path_book_id)
        return observation_history(
            _database_for_book(app, checked_book),
            checked_book,
            _check_id(edition_id),
            scope_type,
            _check_id(scope_id),
        )

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/metrics/missing")
    @app.get("/api/books/{path_book_id}/editions/{edition_id}/missing-inputs")
    async def missing_api(path_book_id: str, edition_id: str, scope_id: str) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        run = MetricsAssembler(_database_for_book(app, checked_book)).rebuild(
            checked_book,
            edition_id=_check_id(edition_id),
            scope_type="CHAPTER",
            scope_id=_check_id(scope_id),
        )
        return {
            "run_id": run["run_id"],
            "missing": {
                item["metric_id"]: item["missing_components"]
                for item in run["results"]
                if item["missing_components"]
            },
        }

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/disputes")
    async def disputes_api(
        path_book_id: str, edition_id: str, scope_id: str
    ) -> list[dict[str, Any]]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        checked_scope = _check_id(scope_id)
        selected_database = _database_for_book(app, checked_book)
        selected_database.initialize()
        with selected_database.connect() as connection:
            rows = connection.execute(
                "SELECT DISTINCT scope_type, metric_id, component_id "
                "FROM metric_observations WHERE book_id=? AND edition_id=? AND scope_id=? "
                "ORDER BY metric_id, component_id",
                (checked_book, checked_edition, checked_scope),
            ).fetchall()
        resolver = ObservationResolver(selected_database)
        disputes: list[dict[str, Any]] = []
        for row in rows:
            resolution = resolver.resolve(
                checked_book,
                checked_edition,
                str(row["scope_type"]),
                checked_scope,
                str(row["metric_id"]),
                str(row["component_id"]),
            )
            if resolution.status.value == "DISPUTED":
                disputes.append(
                    {
                        "scope_type": str(row["scope_type"]),
                        "metric_id": str(row["metric_id"]),
                        "component_id": str(row["component_id"]),
                        "resolution": resolution.model_dump(mode="json"),
                    }
                )
        return disputes

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/metrics/observations")
    async def author_input_api(
        path_book_id: str, edition_id: str, request: Request, payload: AuthorInputRequest
    ) -> Any:
        verify_csrf(request, None)
        try:
            checked_book = _check_id(path_book_id)
            return save_author_input(
                _database_for_book(app, checked_book), checked_book, _check_id(edition_id), payload
            )
        except (MetricConflictError, MetricValidationError, ValueError) as exc:
            return _error(exc)

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/metrics/observations/"
        "{observation_id}/retract"
    )
    async def retract_observation_api(
        path_book_id: str,
        edition_id: str,
        observation_id: str,
        request: Request,
        payload: RetractRequest,
    ) -> Any:
        verify_csrf(request, None)
        try:
            from novel_authoring.metrics.service import AuthorMetricInputService

            checked_book = _check_id(path_book_id)
            return AuthorMetricInputService(_database_for_book(app, checked_book)).retract(
                _check_id(observation_id),
                book_id=checked_book,
                edition_id=_check_id(edition_id),
                scope_type=payload.scope_type,
                scope_id=_check_id(payload.scope_id),
                reason=payload.reason,
                expected_active_observation_id=payload.expected_active_observation_id,
            )
        except (MetricConflictError, MetricValidationError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/metrics/recompute")
    async def recompute_api(
        path_book_id: str, edition_id: str, request: Request, payload: RecomputeRequest
    ) -> Any:
        verify_csrf(request, None)
        try:
            checked_book = _check_id(path_book_id)
            selected_database = _database_for_book(app, checked_book)
            assembler = MetricsAssembler(selected_database)
            bundle = assembler.assemble(
                checked_book,
                edition_id=_check_id(edition_id),
                scope_type=payload.scope_type,
                scope_id=_check_id(payload.scope_id),
                requested_metric_ids=payload.requested_metric_ids,
            )
            for field, expected in (
                ("effective_content_sha256", bundle.effective_content_sha256),
                ("projection_hash", bundle.projection_hash),
                ("registry_hash", bundle.registry_hash),
                ("config_hash", bundle.config_hash),
            ):
                supplied = getattr(payload, field)
                if supplied is not None and supplied != expected:
                    raise MetricConflictError(f"{field} 已变化，请刷新后重试")
            resolver = ObservationResolver(selected_database)
            for key, expected_id in payload.expected_effective_observation_ids.items():
                parts = key.split(".", 1)
                if len(parts) != 2 or not parts[0] or not parts[1]:
                    raise MetricValidationError(
                        "expected_effective_observation_ids 的 key 必须是 metric_id.component_id"
                    )
                current = resolver.resolve(
                    checked_book,
                    _check_id(edition_id),
                    payload.scope_type,
                    _check_id(payload.scope_id),
                    parts[0],
                    parts[1],
                ).effective_observation_id
                if current != expected_id:
                    raise MetricConflictError(f"{key} 的 active observation 已变化，请刷新后重试")
            return assembler.run(bundle)
        except (MetricConflictError, MetricValidationError, ValueError) as exc:
            return _error(exc)

    @app.get("/api/handoffs")
    async def all_handoffs_api(book: str | None = None) -> list[dict[str, Any]]:
        database.initialize()
        with database.connect() as connection:
            if book is None:
                rows = connection.execute(
                    "SELECT * FROM workflow_handoffs ORDER BY created_at DESC"
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM workflow_handoffs WHERE book_id=? ORDER BY created_at DESC",
                    (_check_id(book),),
                ).fetchall()
        return [dict(row) for row in rows]

    @app.get("/api/handoffs/{handoff_id}")
    async def handoff_api(handoff_id: str) -> dict[str, Any]:
        return get_handoff(database, _check_id(handoff_id))

    @app.get("/api/handoffs/{handoff_id}/events")
    async def handoff_events_api(handoff_id: str) -> list[dict[str, Any]]:
        return cast(list[dict[str, Any]], get_handoff(database, _check_id(handoff_id))["events"])

    @app.get("/api/handoffs/{handoff_id}/result")
    async def handoff_result_api(handoff_id: str) -> dict[str, Any]:
        item = get_handoff(database, _check_id(handoff_id))
        if item.get("status") == "COMPLETED":
            item["validated_result"] = validate_result_file(database, handoff_id)
        return {
            key: item[key]
            for key in ("handoff_id", "status", "result", "validated_result")
            if key in item
        }

    @app.get("/api/handoffs/{handoff_id}/instruction")
    async def handoff_instruction_api(handoff_id: str) -> Any:
        checked = _check_id(handoff_id)
        try:
            get_handoff(database, checked)
        except (HandoffWorkflowError, sqlite3.OperationalError):
            # A missing workflow_handoffs table also means the handoff does not
            # exist; align with the book-scoped route's error mapping.
            return _handoff_not_found_response()
        try:
            instruction = copy_instruction(
                database, checked, library_root=app.state.library_root
            )
        except HandoffWorkflowError as exc:
            return _error(exc)
        return {"handoff_id": checked, "instruction": instruction}

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/handoffs/{handoff_id}/instruction")
    async def book_handoff_instruction_api(
        path_book_id: str, edition_id: str, handoff_id: str
    ) -> Any:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        checked_handoff = _check_id(handoff_id)
        selected_database = _database_for_book(app, checked_book)
        try:
            item = get_handoff(selected_database, checked_handoff)
        except HandoffWorkflowError:
            return _handoff_not_found_response()
        if (
            str(item.get("book_id")) != checked_book
            or str(item.get("edition_id")) != checked_edition
        ):
            return JSONResponse(
                status_code=404,
                content={
                    "error": {
                        "code": "HANDOFF_SCOPE_MISMATCH",
                        "message": "handoff 不属于当前 book/edition",
                        "details": {},
                    }
                },
            )
        try:
            instruction = copy_instruction(
                selected_database,
                checked_handoff,
                library_root=app.state.library_root,
            )
        except HandoffWorkflowError as exc:
            return _error(exc)
        return {
            "handoff_id": checked_handoff,
            "instruction": instruction,
        }

    @app.get("/api/books/{path_book_id}/editions/{edition_id}/handoffs/{handoff_id}/result")
    async def book_handoff_result_api(
        path_book_id: str, edition_id: str, handoff_id: str
    ) -> dict[str, Any]:
        checked_book = _check_id(path_book_id)
        checked_edition = _check_id(edition_id)
        checked_handoff = _check_id(handoff_id)
        selected_database = _database_for_book(app, checked_book)
        item = get_handoff(selected_database, checked_handoff)
        if (
            str(item.get("book_id")) != checked_book
            or str(item.get("edition_id")) != checked_edition
        ):
            raise HTTPException(status_code=404, detail="handoff 不属于当前 book/edition")
        if item.get("status") == HandoffStatus.COMPLETED.value:
            item["validated_result"] = validate_result_file(selected_database, checked_handoff)
        return {
            key: item[key]
            for key in ("handoff_id", "status", "result", "validated_result")
            if key in item
        }

    @app.get("/api/books/{path_book_id}/handoffs")
    async def handoffs_api(
        path_book_id: str, edition_id: str | None = None
    ) -> list[dict[str, Any]]:
        checked_book = _check_id(path_book_id)
        return list_handoffs(_database_for_book(app, checked_book), checked_book, edition_id)

    @app.get("/api/books/{path_book_id}/pending-actions")
    async def pending_author_actions_api(
        path_book_id: str,
        edition_id: str | None = None,
    ) -> list[dict[str, Any]]:
        checked_book = _check_id(path_book_id)
        activities = _resume_pending_actions(_database_for_book(app, checked_book), checked_book)
        return [
            item
            for item in activities
            if edition_id is None or item["edition_id"] == _check_id(edition_id)
        ]

    @app.post("/api/books/{path_book_id}/editions/{edition_id}/activate")
    async def activate_edition_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        payload: EditionActivationRequest,
    ) -> Any:
        verify_csrf(request, None)
        if not payload.confirmed:
            return _error(ValueError("请确认切换正式版本的影响"))
        checked_book = _require_book_scope(app, path_book_id)
        try:
            activated = activate_edition(
                _database_for_book(app, checked_book),
                checked_book,
                _check_id(edition_id),
                confirmation=ACTIVATE_PHRASE,
            )
            return {
                "edition": activated.model_dump(mode="json"),
                "redirect_url": (
                    f"/books/{checked_book}/editions/{activated.edition_id}/workbench"
                ),
                "canon_changed": False,
            }
        except (OSError, RuntimeError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/handoffs/continue")
    @app.post("/api/books/{path_book_id}/handoffs/continuation")
    async def continuation_api(
        request: Request, payload: HandoffRequest, path_book_id: str | None = None
    ) -> Any:
        verify_csrf(request, None)
        try:
            target_book = path_book_id or app.state.book_id
            if target_book is None:
                raise HandoffWorkflowError("需要 book_id")
            checked_book = _check_id(str(target_book))
            selected_database = (
                _database_for_book(app, checked_book) if path_book_id is not None else database
            )
            if app.state.library_root is not None:
                record = BookRegistry(BookLayout(app.state.library_root)).record(checked_book)
                access = studio_access(BookLayout(app.state.library_root), record)
                if access.accessible and not access.capabilities["continue_from_current_boundary"]:
                    return _queue_pending_author_action(
                        selected_database,
                        checked_book,
                        payload,
                        action_type="CONTINUE",
                    )
            return prepare_continuation(selected_database, checked_book, payload)
        except (HandoffWorkflowError, ValueError) as exc:
            return _error(exc)

    @app.post(
        "/api/books/{path_book_id}/editions/{edition_id}/planning/candidates/"
        "{candidate_id}/draft"
    )
    async def selected_candidate_draft_api(
        request: Request,
        path_book_id: str,
        edition_id: str,
        candidate_id: str,
        payload: CandidateSelectionRequest,
    ) -> Any:
        verify_csrf(request, None)
        try:
            checked_book = _check_id(path_book_id)
            checked_edition = _check_id(edition_id)
            checked_candidate = _check_id(candidate_id)
            if payload.candidate_id != checked_candidate:
                raise HandoffWorkflowError("候选路径 ID 与请求体 ID 不一致")
            payload = payload.model_copy(update={"edition_id": checked_edition})
            return prepare_selected_candidate_draft(
                _database_for_book(app, checked_book), checked_book, payload
            )
        except (HandoffWorkflowError, OSError, ValueError, RuntimeError) as exc:
            return _error(exc)

    @app.post("/api/handoffs/revise")
    @app.post("/api/books/{path_book_id}/handoffs/revision")
    async def revision_api(
        request: Request, payload: HandoffRequest, path_book_id: str | None = None
    ) -> Any:
        verify_csrf(request, None)
        try:
            target_book = path_book_id or app.state.book_id
            if target_book is None:
                raise HandoffWorkflowError("需要 book_id")
            checked_book = _check_id(str(target_book))
            selected_database = (
                _database_for_book(app, checked_book) if path_book_id is not None else database
            )
            revision_readiness = None
            if payload.context_chapter_id:
                with selected_database.connect() as connection:
                    revision_readiness = evaluate_revision_range(
                        connection,
                        book_id=checked_book,
                        edition_id=str(payload.edition_id or "base"),
                        target_chapter_ids=[payload.context_chapter_id],
                    )
            if app.state.library_root is not None:
                record = BookRegistry(BookLayout(app.state.library_root)).record(checked_book)
                access = studio_access(BookLayout(app.state.library_root), record)
                if access.accessible and (
                    not access.capabilities["rewrite_selected_chapter"]
                    or revision_readiness is None
                    or not revision_readiness.ready
                ):
                    return _queue_pending_author_action(
                        selected_database,
                        checked_book,
                        payload,
                        action_type="REWRITE",
                    )
            return prepare_revision(selected_database, checked_book, payload)
        except (HandoffWorkflowError, ValueError) as exc:
            return _error(exc)

    @app.post("/api/handoffs/{handoff_id}/cancel")
    async def cancel_api(handoff_id: str, request: Request) -> Any:
        verify_csrf(request, None)
        try:
            return cancel_handoff(database, _check_id(handoff_id))
        except HandoffWorkflowError as exc:
            return _error(exc)

    @app.post("/api/handoffs/{handoff_id}/stale")
    @app.post("/api/handoffs/{handoff_id}/mark-stale")
    async def stale_api(handoff_id: str, request: Request) -> Any:
        verify_csrf(request, None)
        try:
            return mark_stale(database, _check_id(handoff_id))
        except HandoffWorkflowError as exc:
            return _error(exc)

    @app.post("/api/handoffs/{handoff_id}/user-response")
    async def user_response_api(
        handoff_id: str, request: Request, payload: UserResponseRequest
    ) -> Any:
        verify_csrf(request, None)
        try:
            return record_user_response(database, _check_id(handoff_id), payload.response)
        except HandoffWorkflowError as exc:
            return _error(exc)

    return app


def web_doctor() -> dict[str, Any]:
    """Validate the local Web Workbench surface without opening a server."""

    template_dir = Path(__file__).parent / "templates"
    static_dir = Path(__file__).parent / "static"
    checks: dict[str, dict[str, Any]] = {
        "templates": {
            "ok": (template_dir / "workbench.html").is_file(),
            "path": str(template_dir / "workbench.html"),
        },
        "static_assets": {
            "ok": all((static_dir / name).is_file() for name in ("app.js", "style.css")),
            "paths": [str(static_dir / name) for name in ("app.js", "style.css")],
        },
        "story_program": {
            "ok": (template_dir / "story_program.html").is_file()
            and (static_dir / "story_program.js").is_file(),
            "paths": [
                str(template_dir / "story_program.html"),
                str(static_dir / "story_program.js"),
            ],
        },
        "frontend": {
            "ok": True,
            "mode": "native-javascript-css",
            "detail": "不需要 Node 或额外 frontend build。",
        },
        "version": {
            "ok": True,
            "package": __version__,
            "commit": _current_commit(),
            "static_asset_version": STATIC_ASSET_VERSION,
        },
    }
    try:
        probe = create_app(
            Database(Path(".novel-authoring-workbench-doctor.sqlite3")),
            library_root=Path("library"),
        )
        route_paths = {str(route.path) for route in probe.routes if hasattr(route, "path")}
        required = {
            "/health",
            "/",
            "/library",
            "/story-program",
            "/books/{path_book_id}/story-program",
            "/api/books/{path_book_id}/story-program",
            "/api/books/{path_book_id}/story-program/prompt",
            "/api/library",
            "/api/library/catalog",
            "/api/library/books/{path_book_id}",
            "/api/library/discovery/refresh",
            "/api/library/candidates/{candidate_id}/initialize",
            "/books/{path_book_id}/editions/{edition_id}/workbench",
            "/api/books/{path_book_id}/editions/{edition_id}/workbench",
            "/api/books/{path_book_id}/studio-readiness",
            "/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/context",
            "/api/books/{path_book_id}/editions/{edition_id}/chapters/{chapter_id}/game-state",
            "/api/books/{path_book_id}/editions/{edition_id}/author-control",
            "/api/books/{path_book_id}/editions/{edition_id}/author-commands",
        }
        checks["routes"] = {
            "ok": required.issubset(route_paths),
            "required": sorted(required),
            "missing": sorted(required - route_paths),
        }
        from fastapi.testclient import TestClient

        health_response = TestClient(probe).get("/health")
        checks["api_health"] = {
            "ok": health_response.status_code == 200
            and health_response.json().get("status") == "ok",
            "status_code": health_response.status_code,
        }
    except (ImportError, RuntimeError, OSError) as exc:
        checks["routes"] = {"ok": False, "error": str(exc)}
        checks["api_health"] = {"ok": False, "error": str(exc)}
    return {
        "ok": all(bool(item.get("ok")) for item in checks.values()),
        "executor": "Windows Codex desktop client",
        "bind_default": "127.0.0.1",
        "checks": checks,
    }


def serve(
    database: Database,
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    allow_remote: bool = False,
    book_id: str | None = None,
    library_root: Path | None = None,
    discovery_root: Path | None = None,
    developer_mode: bool = False,
    story_program_reference_root: Path | None = None,
) -> None:
    if host not in ("127.0.0.1", "localhost", "::1") and not allow_remote:
        raise ValueError("默认只允许本机绑定；需要远程访问时显式传入 allow_remote")
    # Apply structural migrations before the server starts.  This prepares the
    # author-control tables but does not create Canon events or approve drafts.
    database.initialize()
    if library_root is not None:
        layout = BookLayout(library_root)
        for record in BookRegistry(layout).list():
            Database(layout.for_book(record.book_id).database).initialize()
    import uvicorn

    uvicorn.run(
        create_app(
            database,
            book_id=book_id,
            library_root=library_root,
            discovery_root=discovery_root,
            developer_mode=developer_mode,
            story_program_reference_root=story_program_reference_root,
        ),
        host=host,
        port=port,
    )
