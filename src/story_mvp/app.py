from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from .batch_runtime import (
    DEFAULT_BATCH_SIZE,
    BatchWindow,
    apply_batch_delta,
    build_batch_delta_reviser_prompt,
    build_batch_primary_prompt,
    extract_batch_outline_plans,
    parse_batch_delta_response,
    parse_batch_primary_response,
)
from .character_prompts import generate_split_prompt
from .gbrain import GBrainQueryError
from .gbrain_retrieval import (
    build_retrieval_brief,
    default_effective_query,
    extract_hard_constraints,
    retrieve_gbrain,
)
from .openai_executor import (
    OpenAIExecutorError,
    batch_authority_reviser_model,
    batch_primary_model,
    configure_settings,
    configured as openai_configured,
    authority_reviser_model,
    default_model,
    generate_text,
    settings_status,
    state_extraction_model,
)
from .premise_aperture import (
    build_premise_compiler_prompt,
    build_selected_premise_compiler_prompt,
    build_single_pass_prompt,
)
from .premise_workflow import (
    approve_premise,
    read_premise_payload,
    record_premise_compiler_input,
    save_premise_candidates,
    save_premise_compiler_report,
    save_selected_premise,
    skip_premise,
)
from .progressive_canon import (
    MysteryThread,
    build_canonization_compiler_prompt,
    build_decision_surface_prompt,
    build_reframe_prompt,
)
from .prompts import DEFAULT_PROMPT_TEMPLATES, HardGateError, generate_prompt
from .references import REFERENCE_ROOT, load_validated_references
from .run_ledger import (
    activate_optional_repair,
    adopt_final_source,
    create_or_load_run,
    load_run,
    load_node_prompt,
    load_node_response,
    mark_node_failed,
    mark_node_skipped,
    next_actionable_node,
    retry_node,
    save_node_prompt,
    save_node_response,
    skip_integrator_if_no_patches,
)
from .storage import (
    adopt_mystery_candidate,
    advance_mystery_after_reveal,
    approve_human_development,
    approve_character_artifact,
    approve_creative_artifact,
    approve_world_expansion,
    create_book,
    get_mystery_thread,
    inject_mystery_reveals_into_chapter_plan,
    list_books,
    read_chapter,
    read_book_payload,
    read_creative_payload,
    read_mystery_control,
    refresh_current_character,
    replace_chapter,
    require_book,
    render_mystery_outline_schedule,
    render_mystery_planning_context,
    save_mystery_compiler_input,
    save_mystery_thread,
    save_chapter,
    write_book,
    write_creative_artifact,
    write_prompt_templates,
)
from .workflow_state import workflow_impact, workflow_status


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = PROJECT_ROOT / "src" / "story_mvp" / "templates"
STATIC_DIR = PROJECT_ROOT / "src" / "story_mvp" / "static"

app = FastAPI(title="Transparent GBrain Story Studio")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


class BookCreateRequest(BaseModel):
    book_id: str


class TextRequest(BaseModel):
    content: str = ""


class MysteryThreadRequest(BaseModel):
    question: str
    state: Literal["OPEN", "FIXED_HIDDEN"] = "OPEN"
    known_anchors: str = ""
    decision_trigger: str = ""
    fixed_point: str = ""
    remains_unknown: str = ""
    reveal_boundary: str = ""
    route: Literal["world", "story"] = "story"


class MysteryDecisionRequest(BaseModel):
    mystery_id: str
    planning_need: str


class MysteryReframeRequest(BaseModel):
    mystery_id: str
    decision_surface: str


class MysteryCompilerRequest(BaseModel):
    mystery_id: str
    selected_candidate: str
    decision_surface: str
    planning_need: str


class MysteryAdoptRequest(BaseModel):
    mystery_id: str
    selected_candidate: str
    compiler_report: str


class MysteryAdvanceRequest(BaseModel):
    next_decision_trigger: str = ""


class WorldExpansionApproveRequest(BaseModel):
    content: str
    scope: Literal["macro", "instance"] = "macro"
    effective_from: int = Field(ge=1)
    effective_until: int = Field(default=0, ge=0)


class OpenAIExecutorRequest(BaseModel):
    prompt: str = ""
    model: str = ""
    purpose: Literal[
        "default",
        "state_extraction",
        "authority_reviser",
        "batch_primary",
        "batch_authority_reviser",
    ] = "default"
    reasoning_effort: str = ""


class BatchPromptRequest(BaseModel):
    start_chapter: int = Field(ge=1, le=9999)
    batch_size: int = Field(default=DEFAULT_BATCH_SIZE, ge=4, le=6)
    book_content: str = ""
    world_vision: str = ""
    world_expansions: str = ""
    character_card: str = ""
    story_program: str = ""
    previous_chapter_text: str = ""
    batch_primary_response: str = ""


class BatchDeltaApplyRequest(BaseModel):
    start_chapter: int = Field(ge=1, le=9999)
    batch_size: int = Field(default=DEFAULT_BATCH_SIZE, ge=4, le=6)
    batch_primary_response: str
    batch_delta_response: str


class OpenAISettingsRequest(BaseModel):
    name: str = ""
    url: str = ""
    api_key: str = ""


class CreativeArtifactRequest(BaseModel):
    content: str = ""
    origin: Literal["model_generated", "model_selected", "author_edited"] | None = None


class PromptTemplatesRequest(BaseModel):
    templates: dict[str, str] = Field(default_factory=dict)


class GBrainContextRequest(BaseModel):
    mode: Literal[
        "world_vision",
        "world_expansion",
        "power_seed",
        "human_seed",
        "idea",
        "story_refresh",
        "outline",
        "director",
        "chapter_prep",
        "chapter",
        "review",
        "context_curator",
        "primary_writer",
        "specialist_opening",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
        "chapter_integrator",
    ] = "idea"
    book_content: str = ""
    creative_direction: str = ""
    world_vision: str = ""
    character_card: str = ""
    proposal_context: str = ""
    current_long_block: str = ""
    current_outline: str = ""
    recent_summaries: str = ""
    query_override: str = ""
    prototype_id: str = ""


class GBrainQueryRequest(GBrainContextRequest):
    pass


class ChapterRequest(BaseModel):
    chapter_number: int
    content: str


class RunRequest(BaseModel):
    writer_mode: Literal[
        "single", "curator_primary", "hybrid_selective", "hybrid_full"
    ] = "curator_primary"
    selected_specialists: list[str] = Field(default_factory=list)


class RunNodeContentRequest(BaseModel):
    content: str


class RunAdoptRequest(BaseModel):
    source: Literal["primary", "authority_reviser", "integrator"]


class RunIntegratorSkipRequest(BaseModel):
    specialist_responses: dict[str, str] = Field(default_factory=dict)


class RunRepairSpecialistsRequest(BaseModel):
    selected_specialists: list[str] = Field(default_factory=list)


class PromptRequest(BaseModel):
    mode: Literal[
        "premise_forge",
        "premise_compiler",
        "idea",
        "world_vision",
        "world_expansion",
        "power_seed",
        "human_seed",
        "human_development",
        "story_refresh",
        "outline",
        "director",
        "chapter_prep",
        "chapter",
        "review",
        "state_delta",
        "context_curator",
        "primary_writer",
        "authority_reviser",
        "specialist_opening",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
        "chapter_integrator",
    ]
    book_id: str = ""
    template: str = ""
    writer_mode: Literal[
        "single", "curator_primary", "hybrid_selective", "hybrid_full"
    ] = "curator_primary"
    book_content: str = ""
    creative_direction: str = ""
    premise_candidates: str = ""
    selected_premise: str = ""
    premise_compiler_scope: Literal["candidates", "selected"] = "candidates"
    world_vision: str = ""
    world_expansions: str = ""
    power_seed: str = ""
    human_seed: str = ""
    prototype_id: str = ""
    character_card: str = ""
    character_initial_state: str = ""
    human_development: str = ""
    current_character: str = ""
    evolution_scope: Literal["macro", "instance"] = "macro"
    effective_from_chapter: int = Field(default=0, ge=0)
    effective_until_chapter: int = Field(default=0, ge=0)
    creative_state: dict[str, Any] = Field(default_factory=dict)
    proposal_context: str = ""
    current_long_block: str = ""
    previous_chapter_text: str = ""
    current_outline: str = ""
    current_chapter_plan: str = ""
    recent_summaries: str = ""
    selected_references: list[dict[str, Any]] = Field(default_factory=list)
    gbrain_inspiration: str = ""
    actual_summaries: str = ""
    current_state: str = ""
    unfulfilled_promises: str = ""
    future_direction: str = ""
    chapter_number: int = Field(default=0, ge=0)
    chapter_prose: str = ""
    chapter_fact_summary: str = ""
    curator_response: str = ""
    curated_context: str = ""
    primary_writer_response: str = ""
    primary_draft: str = ""
    primary_fact_summary: str = ""
    specialist_opening_response: str = ""
    specialist_dialogue_response: str = ""
    specialist_action_response: str = ""
    specialist_emotion_response: str = ""
    enabled_specialists: dict[str, bool] = Field(default_factory=dict)


def workspace_path() -> Path:
    configured = os.environ.get("STORY_MVP_WORKSPACE", "")
    return Path(configured) if configured else PROJECT_ROOT / "books"


def not_found(error: FileNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(error))


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "reference_root": str(REFERENCE_ROOT),
            "workspace": str(workspace_path()),
        },
    )


@app.get("/api/books")
def get_books() -> dict[str, list[str]]:
    return {"books": list_books(workspace_path())}


@app.get("/api/prompt-templates")
def get_prompt_templates() -> dict[str, dict[str, str]]:
    return {"templates": dict(DEFAULT_PROMPT_TEMPLATES)}


@app.get("/api/executors")
def get_executors() -> dict[str, Any]:
    openai_settings = settings_status()
    return {
        "manual": {"available": True},
        "codex_external": {"available": True},
        "openai_api": {
            "available": True,
            "configured": openai_configured(),
            "model": default_model(),
            "state_model": state_extraction_model(),
            "authority_reviser_model": authority_reviser_model(),
            "authority_reviser_reasoning": "high",
            "batch_primary_model": batch_primary_model(),
            "batch_primary_reasoning": "high",
            "batch_authority_reviser_model": batch_authority_reviser_model(),
            "batch_authority_reviser_reasoning": "high",
            "name": openai_settings["name"],
        },
    }


@app.get("/api/settings/openai")
def get_openai_settings() -> dict[str, str | bool]:
    return settings_status()


@app.put("/api/settings/openai")
def put_openai_settings(payload: OpenAISettingsRequest) -> dict[str, str | bool]:
    try:
        return configure_settings(payload.name, payload.url, payload.api_key)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/executors/openai")
def post_openai_executor(payload: OpenAIExecutorRequest) -> dict[str, str]:
    try:
        return generate_text(
            payload.prompt, model=payload.model, purpose=payload.purpose, reasoning_effort=payload.reasoning_effort
        )
    except OpenAIExecutorError as error:
        status_code = 503 if not error.configured else 502
        raise HTTPException(status_code=status_code, detail=str(error)) from error


@app.post("/api/batch/primary-prompt")
def post_batch_primary_prompt(payload: BatchPromptRequest) -> dict[str, str | int]:
    try:
        window = BatchWindow(payload.start_chapter, payload.batch_size)
        plans = extract_batch_outline_plans(payload.book_content, window)
        prompt = build_batch_primary_prompt(
            window=window,
            batch_plans=plans,
            book_content=payload.book_content,
            world_vision=payload.world_vision,
            world_expansions=payload.world_expansions,
            character_card=payload.character_card,
            previous_chapter_text=payload.previous_chapter_text,
        )
        return {
            "content": prompt,
            "start_chapter": window.start_chapter,
            "end_chapter": window.end_chapter,
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/batch/authority-reviser-prompt")
def post_batch_authority_reviser_prompt(payload: BatchPromptRequest) -> dict[str, str | int]:
    try:
        window = BatchWindow(payload.start_chapter, payload.batch_size)
        plans = extract_batch_outline_plans(payload.book_content, window)
        chapters = parse_batch_primary_response(payload.batch_primary_response, window)
        prompt = build_batch_delta_reviser_prompt(
            window=window,
            batch_plans=plans,
            primary_chapters=chapters,
            book_content=payload.book_content,
            world_vision=payload.world_vision,
            world_expansions=payload.world_expansions,
            character_card=payload.character_card,
            story_program=payload.story_program,
        )
        return {
            "content": prompt,
            "start_chapter": window.start_chapter,
            "end_chapter": window.end_chapter,
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/batch/apply-authority-delta")
def post_batch_apply_authority_delta(payload: BatchDeltaApplyRequest) -> dict[str, Any]:
    try:
        window = BatchWindow(payload.start_chapter, payload.batch_size)
        chapters = parse_batch_primary_response(payload.batch_primary_response, window)
        delta = parse_batch_delta_response(payload.batch_delta_response, window)
        revised = apply_batch_delta(chapters, delta, window)
        return {
            "start_chapter": window.start_chapter,
            "end_chapter": window.end_chapter,
            "chapters": {str(number): revised[number] for number in window.chapter_numbers},
            "patch_count": len(delta.patches),
            "upstream_conflicts": list(delta.upstream_conflicts),
            "adoptable": not delta.upstream_conflicts,
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/batch/adopt-authority-delta")
def post_batch_adopt_authority_delta(
    book_id: str, payload: BatchDeltaApplyRequest
) -> dict[str, Any]:
    """Preflight the whole batch, then save every finalized chapter before State runs."""

    try:
        window = BatchWindow(payload.start_chapter, payload.batch_size)
        directory = _book_directory(book_id)
        chapters = parse_batch_primary_response(payload.batch_primary_response, window)
        delta = parse_batch_delta_response(payload.batch_delta_response, window)
        if delta.upstream_conflicts:
            raise ValueError(
                "Batch Authority Delta 仍有上游冲突，必须先修 Story / Outline，不能采用正文"
            )
        revised = apply_batch_delta(chapters, delta, window)
        existing = [
            number
            for number in window.chapter_numbers
            if (directory / "chapters" / f"chapter-{number:04d}.md").is_file()
        ]
        if existing:
            rendered = "、".join(str(number) for number in existing)
            raise ValueError(f"Batch 中已有章节存在：{rendered}；请先明确处理已有正文")

        saved: list[str] = []
        for number in window.chapter_numbers:
            target = save_chapter(
                book_id,
                number,
                revised[number],
                workspace_path(),
                source="batch_authority_delta",
            )
            saved.append(str(target))
        return {
            "status": "saved",
            "start_chapter": window.start_chapter,
            "end_chapter": window.end_chapter,
            "patch_count": len(delta.patches),
            "saved": saved,
            "state_next": window.start_chapter,
        }
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books", status_code=201)
def post_book(payload: BookCreateRequest) -> dict[str, Any]:
    try:
        create_book(payload.book_id, workspace_path())
        return read_book_payload(payload.book_id, workspace_path())
    except FileExistsError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}")
def get_book(book_id: str) -> dict[str, Any]:
    try:
        return read_book_payload(book_id, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/mysteries")
def get_mysteries(book_id: str) -> dict[str, Any]:
    try:
        return read_mystery_control(book_id, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/mysteries/{mystery_id}")
def put_mystery(book_id: str, mystery_id: str, payload: MysteryThreadRequest) -> dict[str, Any]:
    try:
        if payload.state != "OPEN" or payload.fixed_point.strip() or payload.reveal_boundary.strip():
            raise ValueError("FIXED_HIDDEN 只能通过 strict-PASS Mystery Compiler + adopt 进入；PUT 只维护 AUTHOR OPEN")
        try:
            existing = get_mystery_thread(book_id, mystery_id, workspace_path())
        except ValueError as error:
            if not str(error).startswith("找不到 Mystery："):
                raise
            existing = None
        if existing is not None and existing.state == "FIXED_HIDDEN":
            raise ValueError("FIXED_HIDDEN Mystery 不能由普通 PUT 覆盖；Reveal 经 State 完成后使用 advance 重新进入 AUTHOR OPEN")
        return save_mystery_thread(
            book_id,
            MysteryThread(
                mystery_id=mystery_id,
                question=payload.question,
                state=payload.state,
                known_anchors=payload.known_anchors,
                decision_trigger=payload.decision_trigger,
                fixed_point=payload.fixed_point,
                remains_unknown=payload.remains_unknown,
                reveal_boundary=payload.reveal_boundary,
                route=payload.route,
            ),
            workspace_path(),
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/mysteries/decision-prompt")
def post_mystery_decision_prompt(book_id: str, payload: MysteryDecisionRequest) -> dict[str, str]:
    try:
        thread = get_mystery_thread(book_id, payload.mystery_id, workspace_path())
        context = read_book_payload(book_id, workspace_path())["book_content"]
        return {
            "prompt": build_decision_surface_prompt(
                thread=thread,
                planning_need=payload.planning_need,
                current_context=context,
            )
        }
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/mysteries/reframe-prompt")
def post_mystery_reframe_prompt(book_id: str, payload: MysteryReframeRequest) -> dict[str, str]:
    try:
        thread = get_mystery_thread(book_id, payload.mystery_id, workspace_path())
        context = read_book_payload(book_id, workspace_path())["book_content"]
        return {
            "prompt": build_reframe_prompt(
                thread=thread,
                decision_surface=payload.decision_surface,
                current_context=context,
            )
        }
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/mysteries/compiler-prompt")
def post_mystery_compiler_prompt(book_id: str, payload: MysteryCompilerRequest) -> dict[str, str]:
    try:
        thread = get_mystery_thread(book_id, payload.mystery_id, workspace_path())
        context = read_book_payload(book_id, workspace_path())["book_content"]
        prompt = build_canonization_compiler_prompt(
            thread=thread,
            selected_candidate=payload.selected_candidate,
            current_context=context,
            decision_surface=payload.decision_surface,
            planning_need=payload.planning_need,
        )
        save_mystery_compiler_input(
            book_id,
            payload.mystery_id,
            selected_candidate=payload.selected_candidate,
            decision_surface=payload.decision_surface,
            planning_need=payload.planning_need,
            current_context=context,
            workspace=workspace_path(),
        )
        return {"prompt": prompt}
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/mysteries/adopt")
def post_mystery_adopt(book_id: str, payload: MysteryAdoptRequest) -> dict[str, Any]:
    try:
        context = read_book_payload(book_id, workspace_path())["book_content"]
        return adopt_mystery_candidate(
            book_id,
            payload.mystery_id,
            selected_candidate=payload.selected_candidate,
            compiler_report=payload.compiler_report,
            current_context=context,
            workspace=workspace_path(),
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/mysteries/{mystery_id}/advance")
def post_mystery_advance(
    book_id: str, mystery_id: str, payload: MysteryAdvanceRequest
) -> dict[str, Any]:
    try:
        return advance_mystery_after_reveal(
            book_id,
            mystery_id,
            next_decision_trigger=payload.next_decision_trigger,
            workspace=workspace_path(),
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/workflow")
def get_workflow(book_id: str) -> dict[str, Any]:
    try:
        return workflow_status(_book_directory(book_id))
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/workflow/impact")
def get_workflow_impact(book_id: str, artifact: str) -> dict[str, Any]:
    try:
        return workflow_impact(_book_directory(book_id), artifact)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/chapters/{chapter_number}")
def get_chapter(book_id: str, chapter_number: int) -> dict[str, str | int]:
    try:
        content = read_chapter(book_id, chapter_number, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"chapter_number": chapter_number, "content": content}


def _book_directory(book_id: str) -> Path:
    return require_book(book_id, workspace_path())


@app.get("/api/books/{book_id}/premise")
def get_premise(book_id: str) -> dict[str, Any]:
    try:
        return read_premise_payload(_book_directory(book_id))
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/premise/candidates")
def put_premise_candidates(book_id: str, payload: TextRequest) -> dict[str, Any]:
    try:
        return save_premise_candidates(_book_directory(book_id), payload.content)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/premise/selected")
def put_selected_premise(book_id: str, payload: TextRequest) -> dict[str, Any]:
    try:
        return save_selected_premise(_book_directory(book_id), payload.content)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/premise/compiler")
def put_premise_compiler(book_id: str, payload: TextRequest) -> dict[str, Any]:
    try:
        return save_premise_compiler_report(_book_directory(book_id), payload.content)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/premise/approve")
def post_premise_approve(book_id: str) -> dict[str, Any]:
    try:
        return approve_premise(_book_directory(book_id))
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/premise/skip")
def post_premise_skip(book_id: str) -> dict[str, Any]:
    try:
        return skip_premise(_book_directory(book_id))
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/runs/{chapter_number}")
def post_run(book_id: str, chapter_number: int, payload: RunRequest) -> dict[str, Any]:
    try:
        manifest = create_or_load_run(
            _book_directory(book_id),
            chapter_number,
            writer_mode=payload.writer_mode,
            selected_specialists=payload.selected_specialists,
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return manifest


@app.put("/api/books/{book_id}/runs/{chapter_number}/repair-specialists")
def put_run_repair_specialists(
    book_id: str, chapter_number: int, payload: RunRepairSpecialistsRequest
) -> dict[str, Any]:
    try:
        return activate_optional_repair(
            _book_directory(book_id), chapter_number, payload.selected_specialists
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/runs/{chapter_number}")
def get_run(book_id: str, chapter_number: int) -> dict[str, Any]:
    try:
        return load_run(_book_directory(book_id), chapter_number)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/runs/{chapter_number}/next")
def get_next_run_node(book_id: str, chapter_number: int) -> dict[str, str | None]:
    try:
        return {"node": next_actionable_node(_book_directory(book_id), chapter_number)}
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/prompt")
def get_run_node_prompt(book_id: str, chapter_number: int, node: str) -> dict[str, str]:
    try:
        return {"content": load_node_prompt(_book_directory(book_id), chapter_number, node)}
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/response")
def get_run_node_response(book_id: str, chapter_number: int, node: str) -> dict[str, str]:
    try:
        return {"content": load_node_response(_book_directory(book_id), chapter_number, node)}
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/prompt")
def put_run_node_prompt(
    book_id: str, chapter_number: int, node: str, payload: RunNodeContentRequest
) -> dict[str, Any]:
    try:
        return save_node_prompt(_book_directory(book_id), chapter_number, node, payload.content)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/response")
def put_run_node_response(
    book_id: str, chapter_number: int, node: str, payload: RunNodeContentRequest
) -> dict[str, Any]:
    try:
        return save_node_response(_book_directory(book_id), chapter_number, node, payload.content)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/failed")
def post_run_node_failed(book_id: str, chapter_number: int, node: str) -> dict[str, Any]:
    try:
        return mark_node_failed(_book_directory(book_id), chapter_number, node)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/skipped")
def post_run_node_skipped(book_id: str, chapter_number: int, node: str) -> dict[str, Any]:
    try:
        return mark_node_skipped(_book_directory(book_id), chapter_number, node)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/runs/{chapter_number}/nodes/{node}/retry")
def post_run_node_retry(book_id: str, chapter_number: int, node: str) -> dict[str, Any]:
    try:
        return retry_node(_book_directory(book_id), chapter_number, node)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/runs/{chapter_number}/adopt")
def post_run_adopt(
    book_id: str, chapter_number: int, payload: RunAdoptRequest
) -> dict[str, Any]:
    try:
        return adopt_final_source(_book_directory(book_id), chapter_number, payload.source)
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/runs/{chapter_number}/integrator/skip-if-no-patches")
def post_integrator_skip_if_no_patches(
    book_id: str, chapter_number: int, payload: RunIntegratorSkipRequest
) -> dict[str, Any]:
    try:
        return skip_integrator_if_no_patches(
            _book_directory(book_id), chapter_number, payload.specialist_responses
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/references")
def get_references() -> dict[str, Any]:
    return {
        "root": str(REFERENCE_ROOT),
        "references": load_validated_references(),
    }


@app.post("/api/gbrain/brief")
def post_gbrain_brief(payload: GBrainContextRequest) -> dict[str, Any]:
    brief = build_retrieval_brief(**payload.model_dump(exclude={"query_override", "prototype_id"}))
    try:
        # All production GBrain planning requires semantic retrieval. Even an explicit
        # Human Prototype must stop here when the embedding credential is missing.
        default_effective_query(payload.mode, brief)
        if payload.mode == "human_seed" and payload.prototype_id.strip():
            effective_query, query_strategy = "", "explicit_human_prototype"
            brief = brief.rstrip() + f"\n显式匿名 Human Prototype：{payload.prototype_id.strip()}"
        else:
            effective_query, query_strategy = default_effective_query(payload.mode, brief)
    except GBrainQueryError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    return {
        "mode": payload.mode,
        "effective_query": effective_query,
        "query_strategy": query_strategy,
        "retrieval_brief": brief,
        "hard_constraints": extract_hard_constraints(
            payload.creative_direction,
            payload.world_vision,
            payload.character_card,
            payload.proposal_context,
            payload.book_content,
            payload.current_long_block,
            payload.current_outline,
            payload.recent_summaries,
        ),
    }


@app.post("/api/gbrain/query")
def post_gbrain_query(payload: GBrainQueryRequest) -> dict[str, Any]:
    try:
        return retrieve_gbrain(**payload.model_dump())
    except GBrainQueryError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


def _prompt_kwargs(payload: PromptRequest) -> dict[str, Any]:
    values = payload.model_dump(exclude={"book_id", "creative_state"})
    if payload.book_id.strip():
        creative = read_creative_payload(payload.book_id, workspace_path())
        if not values.get("book_content"):
            values["book_content"] = read_book_payload(payload.book_id, workspace_path())["book_content"]
        values["creative_state"] = creative["creative_state"]
        if not values.get("world_vision"):
            values["world_vision"] = creative["world_vision"]
        if not values.get("world_expansions"):
            values["world_expansions"] = creative.get("world_expansions", "")
        if not values.get("power_seed"):
            values["power_seed"] = creative["power_seed"]
        if not values.get("human_seed"):
            values["human_seed"] = creative["human_seed"]
        if not values.get("character_card"):
            values["character_card"] = creative["character_card"]
        if not values.get("character_initial_state"):
            values["character_initial_state"] = creative["character_initial_state"]
        if not values.get("human_development"):
            values["human_development"] = creative.get("human_development", "")
        if not values.get("current_character"):
            values["current_character"] = creative.get("current_character", "")
        if not values.get("proposal_context"):
            values["proposal_context"] = creative["proposal"]
        premise = creative.get("premise", {})
        if not values.get("premise_candidates"):
            values["premise_candidates"] = premise.get("candidates", "")
        if (
            payload.premise_compiler_scope == "selected"
            and not values.get("selected_premise")
        ):
            values["selected_premise"] = premise.get("selected", "")
        contracts = premise.get("contracts", {}) if premise.get("approved") else {}
        values["premise_world_contract"] = contracts.get("world", "")
        values["premise_power_contract"] = contracts.get("power", "")
        values["premise_human_contract"] = contracts.get("human", "")
        values["premise_story_contract"] = contracts.get("story", "")

        if payload.mode == "story_refresh":
            values["mystery_planning_context"] = render_mystery_planning_context(
                payload.book_id, workspace_path(), route="story"
            )
        elif payload.mode == "world_expansion":
            values["mystery_planning_context"] = render_mystery_planning_context(
                payload.book_id, workspace_path(), route="world"
            )
        elif payload.mode == "outline":
            values["mystery_outline_schedule"] = render_mystery_outline_schedule(
                payload.book_id, workspace_path()
            )

        if payload.chapter_number > 0:
            if values.get("current_chapter_plan"):
                values["current_chapter_plan"] = inject_mystery_reveals_into_chapter_plan(
                    payload.book_id,
                    payload.chapter_number,
                    str(values["current_chapter_plan"]),
                    workspace_path(),
                )
            directory = require_book(payload.book_id, workspace_path())
            try:
                manifest = load_run(directory, payload.chapter_number)
            except FileNotFoundError:
                manifest = None
            if manifest is not None:
                if payload.mode == "authority_reviser":
                    if not values.get("curator_response"):
                        values["curator_response"] = load_node_response(directory, payload.chapter_number, "curator")
                        values["curated_context"] = values["curator_response"]
                    if not values.get("primary_draft") and not values.get("primary_writer_response"):
                        values["primary_writer_response"] = load_node_response(directory, payload.chapter_number, "primary")
                elif payload.mode in {
                    "specialist_opening", "specialist_dialogue", "specialist_action",
                    "specialist_emotion", "chapter_integrator",
                }:
                    if not values.get("curator_response"):
                        values["curator_response"] = load_node_response(directory, payload.chapter_number, "curator")
                        values["curated_context"] = values["curator_response"]
                    if not values.get("primary_draft"):
                        revised = load_node_response(directory, payload.chapter_number, "authority_reviser")
                        values["primary_writer_response"] = revised or load_node_response(directory, payload.chapter_number, "primary")
                elif payload.mode == "state_delta" and manifest.get("writer_mode") == "curator_primary":
                    source = manifest.get("final_source")
                    if source not in {"authority_reviser", "integrator"}:
                        raise ValueError("curator_primary 的 State Extraction 必须等待 Authority Reviser 成为 final_source")
                    response = load_node_response(directory, payload.chapter_number, source)
                    from .hybrid_runtime import extract_primary_draft

                    body = extract_primary_draft(response)
                    if not body:
                        raise ValueError(f"final_source={source} 没有可提取的正式正文")
                    values["chapter_prose"] = body
    else:
        values["creative_state"] = payload.creative_state
    return values


def _validate_state_delta_input(payload: PromptRequest) -> None:
    """State Delta Prompt 生成动作的输入校验。

    只拦截「生成 State Delta Prompt」本身，不是章节门禁：
    不影响章节提取、批准或保存路径。
    """
    if payload.chapter_number <= 0:
        raise HTTPException(
            status_code=400, detail="生成 State Delta Prompt 需要正整数的当前章节编号"
        )
    if not payload.chapter_prose.strip():
        has_final_run_source = False
        if payload.book_id.strip():
            try:
                manifest = load_run(require_book(payload.book_id, workspace_path()), payload.chapter_number)
                has_final_run_source = (
                    manifest.get("writer_mode") == "curator_primary"
                    and manifest.get("final_source") in {"authority_reviser", "integrator"}
                )
            except (FileNotFoundError, ValueError):
                has_final_run_source = False
        if not has_final_run_source:
            raise HTTPException(
                status_code=400, detail="生成 State Delta Prompt 需要非空的正式正文，或已采用的 Authority Revision / Integrator final_source"
            )


def _planning_only_fields_removed(values: dict[str, Any]) -> dict[str, Any]:
    filtered = dict(values)
    for key in (
        "power_seed",
        "human_seed",
        "prototype_id",
        "character_initial_state",
        "human_development",
        "current_character",
        "evolution_scope",
        "effective_from_chapter",
        "effective_until_chapter",
        "premise_candidates",
        "selected_premise",
        "premise_compiler_scope",
        "premise_world_contract",
        "premise_power_contract",
        "premise_human_contract",
        "premise_story_contract",
        "mystery_planning_context",
        "mystery_outline_schedule",
    ):
        filtered.pop(key, None)
    return filtered


@app.post("/api/prompt")
def post_prompt(payload: PromptRequest) -> dict[str, str]:
    if payload.mode == "state_delta":
        _validate_state_delta_input(payload)
    try:
        values = _prompt_kwargs(payload)
        if payload.mode in {"premise_forge", "premise_compiler"} and payload.book_id.strip():
            world_state = values.get("creative_state", {}).get("world_vision", {})
            if isinstance(world_state, dict) and world_state.get("status") == "author_approved":
                raise ValueError(
                    "World Vision 已批准；Premise 决定已冻结，不能再生成新的 Forge / Compiler Prompt"
                )
        if payload.mode in {"world_vision", "power_seed", "human_seed", "idea"} and payload.book_id.strip():
            premise = read_premise_payload(require_book(payload.book_id, workspace_path()))
            if premise["started_unapproved"]:
                raise ValueError(
                    "Premise Aperture 已开始但尚未批准：请完成 strict PASS + 作者批准，或显式跳过"
                )
        if payload.mode == "premise_forge":
            prompt = build_single_pass_prompt(
                author_direction=str(values.get("creative_direction", ""))
            )
            return {"prompt": prompt}
        if payload.mode == "premise_compiler":
            directory = require_book(payload.book_id, workspace_path())
            compiler_input = record_premise_compiler_input(
                directory,
                scope=payload.premise_compiler_scope,
            )
            if payload.premise_compiler_scope == "selected":
                prompt = build_selected_premise_compiler_prompt(
                    candidate=compiler_input
                )
            else:
                prompt = build_premise_compiler_prompt(
                    candidates=compiler_input
                )
            return {"prompt": prompt}
        if payload.mode == "human_seed" and payload.prototype_id.strip():
            prototype_bundle = retrieve_gbrain(
                mode="human_seed",
                creative_direction=str(values.get("creative_direction", "")),
                world_vision=str(values.get("world_vision", "")),
                prototype_id=payload.prototype_id.strip(),
            )
            values["gbrain_inspiration"] = prototype_bundle["result"]
        if payload.mode == "story_refresh" and payload.book_id.strip():
            snapshot = workflow_status(require_book(payload.book_id, workspace_path()))
            current_entry = snapshot.get("artifacts", {}).get("evolution.current_character", {})
            if current_entry.get("status") != "DONE" or current_entry.get("freshness") != "fresh":
                raise ValueError("Story Refresh 前必须刷新 fresh CURRENT_CHARACTER.md")
        proposal_state = values.get("creative_state", {}).get("proposal", {})
        if (
            payload.mode == "outline"
            and payload.book_id.strip()
            and isinstance(proposal_state, dict)
            and proposal_state.get("status") == "author_approved"
        ):
            snapshot = workflow_status(require_book(payload.book_id, workspace_path()))
            story_entry = snapshot.get("artifacts", {}).get("creative.story_program", {})
            if story_entry.get("status") != "DONE" or story_entry.get("freshness") != "fresh":
                raise ValueError("Outline 前必须先批准 fresh Story Program；当前 Story Program 已 stale 或未完成")
            current_entry = snapshot.get("artifacts", {}).get("evolution.current_character", {})
            if int(current_entry.get("revision", 0)) > 0 and (
                current_entry.get("status") != "DONE" or current_entry.get("freshness") != "fresh"
            ):
                raise ValueError("Refreshed Outline 前必须先刷新 fresh CURRENT_CHARACTER.md")
        split_mode = payload.mode in {
            "world_vision",
            "power_seed",
            "human_seed",
            "idea",
            "outline",
            "world_expansion",
            "human_development",
            "story_refresh",
        }
        prompt = generate_split_prompt(**values) if split_mode else generate_prompt(**_planning_only_fields_removed(values))

    except FileNotFoundError as error:
        raise not_found(error) from error
    except HardGateError as error:
        detail: dict[str, Any] = {
            "message": str(error),
            "missing_fields": error.missing_fields,
        }
        if hasattr(error, "missing_artifacts"):
            detail["missing_artifacts"] = error.missing_artifacts
        raise HTTPException(
            status_code=422,
            detail=detail,
        ) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"prompt": prompt}


@app.post("/api/prompt/state-delta")
def post_state_delta_prompt(payload: PromptRequest) -> dict[str, str]:
    """State Delta Prompt 专用入口：只生成页面可见、可复制的 Prompt，不写任何文件。"""
    _validate_state_delta_input(payload)
    try:
        prompt = generate_prompt(**{**_planning_only_fields_removed(_prompt_kwargs(payload)), "mode": "state_delta"})
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"prompt": prompt}


@app.put("/api/books/{book_id}/book")
def put_book(book_id: str, payload: TextRequest) -> dict[str, str]:
    try:
        write_book(book_id, payload.content, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    return {"status": "saved", "file": "BOOK.md"}


@app.put("/api/books/{book_id}/prompts")
def put_prompt_templates(
    book_id: str, payload: PromptTemplatesRequest
) -> dict[str, str]:
    try:
        write_prompt_templates(book_id, payload.templates, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    return {"status": "saved", "file": "PROMPTS.md"}


@app.put("/api/books/{book_id}/proposal")
def put_proposal(book_id: str, payload: CreativeArtifactRequest) -> dict[str, Any]:
    try:
        creative = write_creative_artifact(
            book_id,
            "proposal",
            payload.content,
            workspace_path(),
            origin=payload.origin,
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": "PROPOSAL.md", **creative}


@app.get("/api/books/{book_id}/creative")
def get_creative(book_id: str) -> dict[str, Any]:
    try:
        return read_creative_payload(book_id, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/books/{book_id}/world-vision")
def put_world_vision(book_id: str, payload: CreativeArtifactRequest) -> dict[str, Any]:
    try:
        creative = write_creative_artifact(
            book_id,
            "world_vision",
            payload.content,
            workspace_path(),
            origin=payload.origin,
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": "WORLD_VISION.md", **creative}


@app.put("/api/books/{book_id}/power-seed")
def put_power_seed(book_id: str, payload: CreativeArtifactRequest) -> dict[str, Any]:
    try:
        creative = write_creative_artifact(
            book_id, "power_seed", payload.content, workspace_path(), origin=payload.origin
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": "POWER_SEED.md", **creative}


@app.put("/api/books/{book_id}/human-seed")
def put_human_seed(book_id: str, payload: CreativeArtifactRequest) -> dict[str, Any]:
    try:
        creative = write_creative_artifact(
            book_id, "human_seed", payload.content, workspace_path(), origin=payload.origin
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": "HUMAN_SEED.md", **creative}


@app.post("/api/books/{book_id}/world-vision/approve")
def approve_world_vision(book_id: str) -> dict[str, Any]:
    try:
        return approve_creative_artifact(book_id, "world_vision", workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/character/approve")
def approve_character(book_id: str) -> dict[str, Any]:
    try:
        return approve_character_artifact(book_id, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/proposal/approve")
def approve_proposal(book_id: str) -> dict[str, Any]:
    try:
        return approve_creative_artifact(book_id, "proposal", workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/api/books/{book_id}/evolution")
def get_long_form_evolution(book_id: str) -> dict[str, Any]:
    try:
        creative = read_creative_payload(book_id, workspace_path())
        return {
            "world_expansions": creative.get("world_expansions", ""),
            "human_development": creative.get("human_development", ""),
            "current_character": creative.get("current_character", ""),
            "world_horizon_handoff": creative.get("world_horizon_handoff", ""),
            "workflow": workflow_status(require_book(book_id, workspace_path())),
        }
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/world-expansions/approve")
def post_world_expansion_approve(
    book_id: str, payload: WorldExpansionApproveRequest
) -> dict[str, Any]:
    try:
        return approve_world_expansion(
            book_id,
            payload.content,
            workspace_path(),
            scope=payload.scope,
            effective_from=payload.effective_from,
            effective_until=payload.effective_until,
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/human-development/approve")
def post_human_development_approve(book_id: str, payload: TextRequest) -> dict[str, Any]:
    try:
        return approve_human_development(
            book_id, payload.content, workspace_path()
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/current-character/refresh")
def post_current_character_refresh(book_id: str) -> dict[str, Any]:
    try:
        return refresh_current_character(book_id, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/chapters")
def post_chapter(book_id: str, payload: ChapterRequest) -> dict[str, str]:
    try:
        target = save_chapter(
            book_id,
            payload.chapter_number,
            payload.content,
            workspace_path(),
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": target.name}


@app.put("/api/books/{book_id}/chapters/{chapter_number}")
def put_chapter(
    book_id: str, chapter_number: int, payload: TextRequest
) -> dict[str, str]:
    try:
        target = replace_chapter(
            book_id,
            chapter_number,
            payload.content,
            workspace_path(),
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": target.name}
