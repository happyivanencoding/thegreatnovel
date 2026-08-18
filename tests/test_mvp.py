from __future__ import annotations

from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.prompts import HardGateError, generate_prompt
from story_mvp.references import load_validated_references
from story_mvp.storage import create_book, read_book_payload


client = TestClient(app)


def test_new_book_has_only_the_four_requested_items(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    assert {path.name for path in book_dir.iterdir()} == {
        "BOOK.md",
        "PROMPTS.md",
        "PROPOSAL.md",
        "chapters",
    }
    assert (book_dir / "chapters").is_dir()


def test_new_book_has_no_database_or_old_system_directory(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    names = {path.name.lower() for path in book_dir.rglob("*")}
    assert not any(name.endswith((".db", ".sqlite", ".sqlite3")) for name in names)
    assert not {"edition", "atlas", "novel_authoring"} & names


def test_only_validated_reference_programs_are_loaded(tmp_path: Path) -> None:
    valid = {"program_id": "valid", "status": "VALIDATED", "story_phase": "one"}
    draft = {"program_id": "draft", "status": "DRAFT", "story_phase": "two"}
    (tmp_path / "valid.yaml").write_text(yaml.safe_dump(valid), encoding="utf-8")
    (tmp_path / "draft.yaml").write_text(yaml.safe_dump(draft), encoding="utf-8")
    loaded = load_validated_references(tmp_path)
    assert [item["program_id"] for item in loaded] == ["valid"]


def test_prompt_is_built_from_submitted_visible_inputs() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="VISIBLE TEMPLATE",
        book_content="VISIBLE IDEA",
        selected_references=[{"program_id": "visible-program", "output_state": "visible state"}],
    )
    assert "VISIBLE TEMPLATE" in prompt
    assert "VISIBLE IDEA" in prompt
    assert "visible-program" in prompt
    assert "hidden" not in prompt


def test_clipboard_code_uses_prompt_textarea_value() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "navigator.clipboard.writeText(text)" in js
    assert 'const text = $("prompt-text").value;' in js


def test_prompt_generation_and_response_do_not_write_book_before_save(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client.post("/api/books", json={"book_id": "demo"})
    before = (tmp_path / "demo" / "BOOK.md").read_text(encoding="utf-8")
    response = client.post(
        "/api/prompt",
        json={
            "mode": "outline",
            "template": "template",
            "book_content": "page-visible-book",
            "selected_references": [],
        },
    )
    assert response.status_code == 200
    assert (tmp_path / "demo" / "BOOK.md").read_text(encoding="utf-8") == before


def test_empty_eight_outline_fields_block_chapter_prompt() -> None:
    empty = "\n".join(f"{field}：" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    try:
        generate_prompt(
            mode="chapter",
            template="template",
            book_content="book",
            current_outline=empty,
        )
    except HardGateError as error:
        assert len(error.missing_fields) == 8
    else:
        raise AssertionError("empty outline fields must block chapter prompt")


def test_non_empty_eight_outline_fields_allow_chapter_prompt() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="template",
        book_content="book",
        current_outline=outline,
    )
    assert "template" in prompt
    assert "结尾推动力：内容" in prompt


def test_approved_chapter_gets_correct_numbered_markdown_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    created = client.post("/api/books", json={"book_id": "demo"})
    assert created.status_code == 201
    saved = client.post(
        "/api/books/demo/chapters",
        json={"chapter_number": 7, "content": "chapter body"},
    )
    assert saved.status_code == 200
    assert saved.json()["file"] == "chapter-0007.md"
    assert (tmp_path / "demo" / "chapters" / "chapter-0007.md").read_text(encoding="utf-8") == "chapter body"
