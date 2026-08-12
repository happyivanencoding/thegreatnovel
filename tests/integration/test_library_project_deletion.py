from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from novel_authoring.db.database import Database
from novel_authoring.original.service import create_original_book
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.library import (
    LibraryAddOptions,
    add_book,
)
from novel_authoring.utils import utc_now
from novel_authoring.web.app import create_app


def _add_imported(layout: BookLayout, source_root: Path, book_id: str) -> Path:
    source_root.mkdir(parents=True, exist_ok=True)
    source = source_root / f"{book_id}.md"
    source.write_text(f"第1章 {book_id}\n\n这是 {book_id} 的原始正文。\n", encoding="utf-8")
    add_book(
        LibraryAddOptions(
            book_id=book_id,
            title=f"项目 {book_id}",
            source=source,
            source_origin=source,
            library_root=layout.library_root,
        )
    )
    return source


def _client(layout: BookLayout, book_id: str, source_root: Path) -> tuple[TestClient, object]:
    app = create_app(
        Database(layout.for_book(book_id).database),
        book_id=book_id,
        library_root=layout.library_root,
        discovery_root=source_root,
    )
    return TestClient(app), app


def _insert_handoff(database: Path, book_id: str, status: str) -> None:
    task_root = database.parent.parent / "operations" / f"handoff-{status.lower()}"
    task_root.mkdir(parents=True, exist_ok=True)
    with Database(database).connect() as connection:
        connection.execute(
            """
            INSERT INTO workflow_handoffs(
                handoff_id, book_id, edition_id, handoff_type, requested_stage,
                status, task_directory, prompt_path, task_manifest_path,
                output_schema_path, result_path, event_log_path, base_event_seq,
                base_projection_hash, source_manifest_sha256, registry_hash,
                config_hash, created_at
            ) VALUES (?, ?, 'base', 'CONTINUATION', 'PLAN_ONLY', ?, ?, ?, ?, ?, ?, ?,
                      0, 'projection', 'source', 'registry', 'config', ?)
            """,
            (
                f"handoff-{status.lower()}",
                book_id,
                status,
                str(task_root),
                str(task_root / "prompt.md"),
                str(task_root / "task.json"),
                str(task_root / "schema.json"),
                str(task_root / "result.json"),
                str(task_root / "events.jsonl"),
                utc_now(),
            ),
        )


def test_library_page_shows_delete_entry_and_imported_delete_preserves_source(
    tmp_path: Path,
) -> None:
    layout = BookLayout(tmp_path / "library")
    sources = tmp_path / "book"
    source_a = _add_imported(layout, sources, "book-a")
    source_b = _add_imported(layout, sources, "book-b")
    before_sources = {path.name: path.read_bytes() for path in sources.iterdir()}
    book_b_marker = layout.for_book("book-b").root / "keep-me.txt"
    book_b_marker.write_text("Book B 必须保留", encoding="utf-8")
    client, app = _client(layout, "book-b", sources)

    page = client.get("/library")
    assert page.status_code == 200
    assert 'data-book-id="book-a"' in page.text
    assert 'data-delete-book data-book-id="book-a"' in page.text
    assert "删除项目" in page.text
    assert "永久删除" in page.text

    response = client.delete(
        "/api/library/books/book-a",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )

    assert response.status_code == 200
    assert response.json()["creation_mode"] == "IMPORTED"
    assert response.json()["source_origin_preserved"] is True
    assert not layout.for_book("book-a").root.exists()
    assert layout.for_book("book-b").root.is_dir()
    assert book_b_marker.read_text(encoding="utf-8") == "Book B 必须保留"
    assert source_a.is_file() and source_b.is_file()
    assert {path.name: path.read_bytes() for path in sources.iterdir()} == before_sources
    books = client.get("/api/library").json()["books"]
    assert "book-a" not in {item["book_id"] for item in books}
    assert "book-b" in {item["book_id"] for item in books}


def test_original_project_is_deleted_completely(tmp_path: Path) -> None:
    layout = BookLayout(tmp_path / "library")
    source = _add_imported(layout, tmp_path / "book", "boot-book")
    create_original_book(
        layout,
        {
            "premise": "一座城市每天遗忘一种颜色",
            "tone_style": "克制",
            "pov": "第三人称限知",
            "must_include": ["代价"],
            "forbidden": ["万能外挂"],
        },
        book_id="original-book",
    )
    original_root = layout.for_book("original-book").root
    (original_root / "original-marker.txt").write_text("原创正文与运行数据", encoding="utf-8")
    client, app = _client(layout, "boot-book", source.parent)

    response = client.delete(
        "/api/library/books/original-book",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )

    assert response.status_code == 200
    assert response.json()["creation_mode"] == "ORIGINAL"
    assert response.json()["source_origin_preserved"] is False
    assert not original_root.exists()
    assert source.is_file()


def test_delete_missing_project_returns_explicit_error(tmp_path: Path) -> None:
    layout = BookLayout(tmp_path / "library")
    source = _add_imported(layout, tmp_path / "book", "book-a")
    client, app = _client(layout, "book-a", source.parent)

    response = client.delete(
        "/api/library/books/not-here",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "LIBRARY_PROJECT_NOT_FOUND"


@pytest.mark.parametrize("status", ["CLAIMED", "RUNNING"])
def test_running_or_claimed_handoff_blocks_delete(tmp_path: Path, status: str) -> None:
    layout = BookLayout(tmp_path / "library")
    source = _add_imported(layout, tmp_path / "book", "book-a")
    paths = layout.for_book("book-a")
    _insert_handoff(paths.database, "book-a", status)
    before_yaml = paths.book_yaml.read_bytes()
    client, app = _client(layout, "book-a", source.parent)

    response = client.delete(
        "/api/library/books/book-a",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "LIBRARY_PROJECT_BUSY"
    assert paths.root.is_dir()
    assert paths.book_yaml.read_bytes() == before_yaml
    assert source.is_file()


def test_ready_for_codex_handoff_does_not_block_delete(tmp_path: Path) -> None:
    layout = BookLayout(tmp_path / "library")
    source = _add_imported(layout, tmp_path / "book", "book-a")
    paths = layout.for_book("book-a")
    _insert_handoff(paths.database, "book-a", "READY_FOR_CODEX")
    client, app = _client(layout, "book-a", source.parent)

    response = client.delete(
        "/api/library/books/book-a",
        headers={"X-CSRF-Token": app.state.csrf_token},
    )

    assert response.status_code == 200
    assert not paths.root.exists()
    assert source.is_file()
