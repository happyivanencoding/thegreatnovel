"""FastAPI routes for the transparent GBrain Story Studio."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from novel_authoring.db.database import Database
from novel_authoring.original.models import OriginalBookRequest
from novel_authoring.original.service import create_original_book
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookKind, BookRecord, BookRegistry
from novel_authoring.story_program.board import read_board
from novel_authoring.story_program.prompt_builder import build_prompt
from novel_authoring.story_program.reference_programs import (
    DEFAULT_REFERENCE_ROOT,
    load_reference_programs,
    select_reference_programs,
)
from novel_authoring.story_program.service import (
    adopt_proposal,
    import_proposal,
    prepare_paths,
    save_chapter,
    save_initial_story_board,
    save_story_board,
    story_program_view,
)
from novel_authoring.utils import safe_book_id, utc_now
from novel_authoring.web.dependencies import verify_csrf

_ID = re.compile(r"^[A-Za-z0-9._-]+$")


def _split_lines(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [line.strip() for line in str(value or "").splitlines() if line.strip()]


def _checked_id(value: object, label: str = "book_id") -> str:
    item = str(value or "").strip()
    if not _ID.fullmatch(item):
        raise HTTPException(status_code=400, detail=f"{label} 格式无效")
    return item


def _record_payload(record: BookRecord) -> dict[str, Any]:
    return {
        "book_id": record.book_id,
        "title": record.title,
        "book_kind": record.book_kind.value,
        "creation_mode": record.creation_mode.value,
        "active_edition_id": record.active_edition_id,
        "root": str(record.root),
    }


def register_story_program_routes(
    app: Any,
    templates: Any,
    *,
    render_template: Callable[[Any, str, Any, dict[str, Any]], Any],
    asset_version: str,
) -> None:
    """Register routes without adding a second application or frontend."""

    def library_root() -> Path:
        root = app.state.library_root
        if root is None:
            raise HTTPException(status_code=404, detail="library 未配置")
        return Path(root)

    def reference_root() -> Path:
        value = getattr(app.state, "story_program_reference_root", None)
        return Path(value) if value is not None else DEFAULT_REFERENCE_ROOT

    def book_context(book_id: str) -> tuple[Path, BookRecord]:
        checked = _checked_id(book_id)
        layout = BookLayout(library_root())
        try:
            record = BookRegistry(layout).record(checked)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="书籍不存在") from exc
        if record.book_kind is not BookKind.AUTHOR and not app.state.developer_mode:
            raise HTTPException(status_code=404, detail="书籍不在作者书库")
        return record.root, record

    def author_books() -> list[dict[str, Any]]:
        try:
            records = BookRegistry(BookLayout(library_root())).list()
        except (FileNotFoundError, OSError, ValueError):
            return []
        return [
            _record_payload(record)
            for record in records
            if record.book_kind is BookKind.AUTHOR or app.state.developer_mode
        ]

    def page_context(
        request: Request,
        view: dict[str, Any] | None,
        record: BookRecord | None,
    ) -> Any:
        return render_template(
            templates,
            "story_program.html",
            request,
            {
                "story_program": view,
                "selected_book": None if record is None else _record_payload(record),
                "books": author_books(),
                "csrf_token": app.state.csrf_token,
                "story_program_reference_root": str(reference_root()),
                "asset_version": asset_version,
            },
        )

    @app.get("/story-program", response_class=HTMLResponse)
    async def story_program_index(request: Request) -> Any:
        selected = str(request.query_params.get("book_id") or "").strip()
        if selected:
            return RedirectResponse(
                url=f"/books/{_checked_id(selected)}/story-program", status_code=302
            )
        return page_context(request, None, None)

    @app.get("/books/{path_book_id}/story-program", response_class=HTMLResponse)
    async def story_program_page(request: Request, path_book_id: str) -> Any:
        root, record = book_context(path_book_id)
        view = story_program_view(
            root,
            reference_root=reference_root(),
            include_provisional=str(request.query_params.get("include_provisional") or "")
            in {"1", "true", "yes"},
            reference_query=str(request.query_params.get("reference_query") or ""),
        )
        return page_context(request, view, record)

    @app.get("/api/books/{path_book_id}/story-program")
    async def story_program_api(request: Request, path_book_id: str) -> dict[str, Any]:
        root, record = book_context(path_book_id)
        view = story_program_view(
            root,
            reference_root=reference_root(),
            include_provisional=str(request.query_params.get("include_provisional") or "")
            in {"1", "true", "yes"},
            reference_query=str(request.query_params.get("reference_query") or ""),
        )
        view["book"] = _record_payload(record)
        return view

    @app.post("/api/story-program/books")
    async def create_story_program_book(request: Request) -> dict[str, Any]:
        verify_csrf(request, None)
        payload = await request.json()
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="新书输入必须是对象")
        title = str(payload.get("title") or "").strip()
        premise = str(payload.get("premise") or "").strip()
        if not title or not premise:
            raise HTTPException(status_code=400, detail="暂定书名和一句话创意不能为空")
        requested_id = str(payload.get("book_id") or "").strip()
        book_id = _checked_id(requested_id) if requested_id else None
        request_model = OriginalBookRequest(
            premise=premise,
            genre=str(payload.get("genre") or ""),
            tone_style=str(payload.get("tone_style") or ""),
            pov=str(payload.get("pov") or ""),
            expected_length=str(payload.get("expected_length") or ""),
            must_include=_split_lines(payload.get("must_include")),
            forbidden=_split_lines(payload.get("forbidden_style")),
            reference_traits=_split_lines(payload.get("reference_traits")),
        )
        created = create_original_book(BookLayout(library_root()), request_model, book_id=book_id)
        created_id = safe_book_id(str(created["book_id"]))
        layout = BookLayout(library_root())
        registry = BookRegistry(layout)
        values = registry.read(created_id)
        values["title"] = title
        values["updated_at"] = utc_now()
        registry.write(layout.for_book(created_id), values)
        registry.write_readme(layout.for_book(created_id), values)
        with Database(layout.for_book(created_id).database).connect() as connection:
            connection.execute(
                "UPDATE books SET title=?, updated_at=? WHERE book_id=?",
                (title, utc_now(), created_id),
            )
        save_initial_story_board(
            layout.for_book(created_id).root,
            title=title,
            premise=premise,
            genre=str(payload.get("genre") or ""),
            reader_experience=str(payload.get("reader_experience") or ""),
            forbidden_style=str(payload.get("forbidden_style") or ""),
        )
        return {
            "book_id": created_id,
            "title": title,
            "redirect_url": f"/books/{created_id}/story-program",
            "canon_changed": False,
        }

    @app.post("/api/books/{path_book_id}/story-program/prompt")
    async def story_program_prompt(request: Request, path_book_id: str) -> dict[str, Any]:
        verify_csrf(request, None)
        root, _record = book_context(path_book_id)
        payload = await request.json()
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Prompt 输入必须是对象")
        paths = prepare_paths(root)
        mode = str(payload.get("mode") or "new_book")
        board = payload.get("board_markdown")
        board_markdown = str(board) if isinstance(board, str) else read_board(paths)
        allow_provisional = bool(payload.get("allow_provisional"))
        programs = load_reference_programs(
            reference_root(), include_provisional=allow_provisional
        )
        selected = select_reference_programs(
            programs,
            [str(item) for item in payload.get("program_ids", [])]
            if isinstance(payload.get("program_ids"), list)
            else [],
            allow_provisional=allow_provisional,
        )
        result = build_prompt(
            template_file=paths.prompts,
            mode=mode,
            payload=payload,
            board_markdown=board_markdown,
            references=selected,
        )
        return result.to_dict()

    @app.post("/api/books/{path_book_id}/story-program/proposal")
    async def story_program_proposal(request: Request, path_book_id: str) -> dict[str, Any]:
        verify_csrf(request, None)
        root, _record = book_context(path_book_id)
        payload = await request.json()
        raw = str(payload.get("raw") or "") if isinstance(payload, dict) else ""
        proposal = import_proposal(root, raw)
        return {"proposal": proposal.to_dict(), "board_unchanged": True}

    @app.post("/api/books/{path_book_id}/story-program/board")
    async def story_program_board(request: Request, path_book_id: str) -> dict[str, Any]:
        verify_csrf(request, None)
        root, _record = book_context(path_book_id)
        payload = await request.json()
        markdown = str(payload.get("markdown") or "") if isinstance(payload, dict) else ""
        saved = save_story_board(root, markdown)
        return {**saved, "author_approved": True, "canon_changed": False}

    @app.post("/api/books/{path_book_id}/story-program/proposal/adopt")
    async def story_program_adopt(request: Request, path_book_id: str) -> dict[str, Any]:
        verify_csrf(request, None)
        root, _record = book_context(path_book_id)
        payload = await request.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("sections"), list):
            raise HTTPException(status_code=400, detail="请选择要采用的 Proposal 区块")
        base = payload.get("board_markdown")
        result = adopt_proposal(
            root,
            selected_keys=[str(item) for item in payload["sections"]],
            base_board=str(base) if isinstance(base, str) else None,
        )
        return {**result, "author_approved": True, "canon_changed": False}

    @app.post("/api/books/{path_book_id}/story-program/chapter")
    async def story_program_chapter(request: Request, path_book_id: str) -> dict[str, Any]:
        verify_csrf(request, None)
        root, _record = book_context(path_book_id)
        payload = await request.json()
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="章节输入必须是对象")
        raw_number = payload.get("chapter_number")
        if not isinstance(raw_number, (str, int)):
            raise HTTPException(status_code=400, detail="章节编号无效")
        try:
            number = int(raw_number)
        except (TypeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail="章节编号无效") from exc
        result = save_chapter(
            root,
            chapter_number=number,
            title=str(payload.get("title") or ""),
            chapter_markdown=str(payload.get("chapter_markdown") or ""),
            chapter_commit=str(payload.get("chapter_commit") or ""),
        )
        return {**result, "author_approved": True}
