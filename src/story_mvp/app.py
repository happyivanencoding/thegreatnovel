from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from .gbrain import GBrainQueryError
from .gbrain_retrieval import build_retrieval_brief, extract_hard_constraints, retrieve_gbrain
from .openai_executor import (
    OpenAIExecutorError,
    configure_settings,
    configured as openai_configured,
    default_model,
    generate_text,
    settings_status,
    state_extraction_model,
)
from .prompts import DEFAULT_PROMPT_TEMPLATES, HardGateError, generate_prompt
from .references import REFERENCE_ROOT, load_validated_references
from .run_ledger import (
    activate_optional_repair,
    adopt_final_source,
    create_or_load_run,
    load_run,
    mark_node_failed,
    mark_node_skipped,
    next_actionable_node,
    retry_node,
    save_node_prompt,
    save_node_response,
    skip_integrator_if_no_patches,
)
from .storage import (
    approve_creative_artifact,
    create_book,
    list_books,
    read_chapter,
    read_book_payload,
    read_creative_payload,
    read_prologue,
    replace_chapter,
    require_book,
    save_chapter,
    save_prologue,
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


class OpenAIExecutorRequest(BaseModel):
    prompt: str = ""
    model: str = ""
    purpose: Literal["default", "state_extraction"] = "default"


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
        "idea",
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
    current_long_block: str = ""
    current_outline: str = ""
    recent_summaries: str = ""
    query_override: str = ""


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
    source: Literal["primary", "integrator"]


class RunIntegratorSkipRequest(BaseModel):
    specialist_responses: dict[str, str] = Field(default_factory=dict)


class RunRepairSpecialistsRequest(BaseModel):
    selected_specialists: list[str] = Field(default_factory=list)


class PromptRequest(BaseModel):
    mode: Literal[
        "idea",
        "fantasy_seed",
        "world_vision",
        "outline",
        "prologue",
        "director",
        "chapter_prep",
        "chapter",
        "review",
        "state_delta",
        "context_curator",
        "primary_writer",
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
    fantasy_seed: str = ""
    world_vision: str = ""
    creative_state: dict[str, Any] = Field(default_factory=dict)
    proposal_context: str = ""
    current_long_block: str = ""
    previous_chapter_text: str = ""
    current_outline: str = ""
    current_chapter_plan: str = ""
    recent_summaries: str = ""
    prologue_text: str = ""
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
            payload.prompt, model=payload.model, purpose=payload.purpose
        )
    except OpenAIExecutorError as error:
        status_code = 503 if not error.configured else 502
        raise HTTPException(status_code=status_code, detail=str(error)) from error


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


@app.get("/api/books/{book_id}/prologue")
def get_prologue(book_id: str) -> dict[str, str]:
    try:
        return {"file": "PROLOGUE.md", "content": read_prologue(book_id, workspace_path())}
    except FileNotFoundError as error:
        raise not_found(error) from error


@app.put("/api/books/{book_id}/prologue")
def put_prologue(book_id: str, payload: TextRequest) -> dict[str, str]:
    try:
        target = save_prologue(book_id, payload.content, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": target.name}


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
    brief = build_retrieval_brief(**payload.model_dump(exclude={"query_override"}))
    return {
        "mode": payload.mode,
        "effective_query": brief,
        "retrieval_brief": brief,
        "hard_constraints": extract_hard_constraints(
            payload.creative_direction,
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
        values["creative_state"] = creative["creative_state"]
        if not values.get("fantasy_seed"):
            values["fantasy_seed"] = creative["fantasy_seed"]
        if not values.get("world_vision"):
            values["world_vision"] = creative["world_vision"]
        if not values.get("proposal_context"):
            values["proposal_context"] = creative["proposal"]
        if not values.get("prologue_text"):
            values["prologue_text"] = read_prologue(payload.book_id, workspace_path())
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
        raise HTTPException(
            status_code=400, detail="生成 State Delta Prompt 需要非空的本次正式章节正文"
        )


@app.post("/api/prompt")
def post_prompt(payload: PromptRequest) -> dict[str, str]:
    if payload.mode == "state_delta":
        _validate_state_delta_input(payload)
    try:
        prompt = generate_prompt(**_prompt_kwargs(payload))
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
        prompt = generate_prompt(**{**_prompt_kwargs(payload), "mode": "state_delta"})
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


@app.put("/api/books/{book_id}/fantasy-seed")
def put_fantasy_seed(book_id: str, payload: CreativeArtifactRequest) -> dict[str, Any]:
    try:
        creative = write_creative_artifact(
            book_id,
            "fantasy_seed",
            payload.content,
            workspace_path(),
            origin=payload.origin,
        )
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"status": "saved", "file": "FANTASY_SEED.md", **creative}


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


@app.post("/api/books/{book_id}/fantasy-seed/approve")
def approve_fantasy_seed(book_id: str) -> dict[str, Any]:
    try:
        return approve_creative_artifact(book_id, "fantasy_seed", workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/books/{book_id}/world-vision/approve")
def approve_world_vision(book_id: str) -> dict[str, Any]:
    try:
        return approve_creative_artifact(book_id, "world_vision", workspace_path())
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
