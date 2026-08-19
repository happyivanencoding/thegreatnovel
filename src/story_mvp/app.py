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
from .prompts import DEFAULT_PROMPT_TEMPLATES, HardGateError, generate_prompt
from .references import REFERENCE_ROOT, load_validated_references
from .storage import (
    create_book,
    list_books,
    read_chapter,
    read_book_payload,
    save_chapter,
    write_book,
    write_prompt_templates,
    write_proposal,
)


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


class PromptTemplatesRequest(BaseModel):
    templates: dict[str, str] = Field(default_factory=dict)


class GBrainContextRequest(BaseModel):
    mode: Literal["idea", "outline", "chapter", "review"] = "idea"
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


class PromptRequest(BaseModel):
    mode: Literal["idea", "outline", "chapter", "review"]
    template: str = ""
    book_content: str = ""
    creative_direction: str = ""
    current_long_block: str = ""
    previous_chapter_text: str = ""
    current_outline: str = ""
    recent_summaries: str = ""
    selected_references: list[dict[str, Any]] = Field(default_factory=list)
    gbrain_inspiration: str = ""
    actual_summaries: str = ""
    current_state: str = ""
    unfulfilled_promises: str = ""
    future_direction: str = ""


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


@app.get("/api/books/{book_id}/chapters/{chapter_number}")
def get_chapter(book_id: str, chapter_number: int) -> dict[str, str | int]:
    try:
        content = read_chapter(book_id, chapter_number, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"chapter_number": chapter_number, "content": content}


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


@app.post("/api/prompt")
def post_prompt(payload: PromptRequest) -> dict[str, str]:
    try:
        prompt = generate_prompt(**payload.model_dump())
    except HardGateError as error:
        raise HTTPException(
            status_code=422,
            detail={"message": str(error), "missing_fields": error.missing_fields},
        ) from error
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
def put_proposal(book_id: str, payload: TextRequest) -> dict[str, str]:
    try:
        write_proposal(book_id, payload.content, workspace_path())
    except FileNotFoundError as error:
        raise not_found(error) from error
    return {"status": "saved", "file": "PROPOSAL.md"}


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
