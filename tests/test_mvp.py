from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml
from fastapi.testclient import TestClient

import story_mvp.app as app_module
import story_mvp.gbrain as gbrain_module
from story_mvp.app import app
from story_mvp.gbrain import GBrainQueryError, query_gbrain
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
    payload = read_book_payload("demo", tmp_path)
    assert set(payload["prompt_templates"]) == {"idea", "outline", "chapter", "review"}


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


def test_gbrain_query_calls_public_cli_and_preserves_stdout(monkeypatch) -> None:
    calls: dict[str, object] = {}

    monkeypatch.setattr(gbrain_module.shutil, "which", lambda name: "gbrain.CMD")

    def fake_run(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="[0.9] slug -- raw result", stderr="")

    monkeypatch.setattr(gbrain_module.subprocess, "run", fake_run)
    assert query_gbrain("方向查询") == "[0.9] slug -- raw result"
    assert calls["command"][:2] == ["gbrain.CMD", "query"]
    assert "方向查询" in calls["command"]
    assert calls["kwargs"]["capture_output"] is True


def test_failed_gbrain_query_is_returned_as_error_without_fake_result(monkeypatch) -> None:
    def fail_query(_query: str) -> str:
        raise GBrainQueryError("真实 CLI 失败")

    monkeypatch.setattr(app_module, "query_gbrain", fail_query)
    response = client.post("/api/gbrain/query", json={"query": "test"})
    assert response.status_code == 502
    assert response.json()["detail"] == "真实 CLI 失败"
    assert "result" not in response.json()


def test_gbrain_result_enters_idea_prompt() -> None:
    prompt = generate_prompt(
        mode="idea",
        template="IDEA TEMPLATE",
        book_content="",
        creative_direction="都市异能，信息差优势",
        gbrain_inspiration="[0.9] mechanism -- 可重复资源循环",
        selected_references=[{"program_id": "manual-reference"}],
    )
    assert "都市异能，信息差优势" in prompt
    assert "可重复资源循环" in prompt
    assert "manual-reference" in prompt


def test_gbrain_result_enters_outline_prompt() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="OUTLINE TEMPLATE",
        book_content="BOOK CONTENT",
        creative_direction="修仙资源经营",
        gbrain_inspiration="Book DNA：阶段回报窗口",
    )
    assert "修仙资源经营" in prompt
    assert "阶段回报窗口" in prompt


def test_gbrain_result_enters_review_prompt() -> None:
    prompt = generate_prompt(
        mode="review",
        template="REVIEW TEMPLATE",
        book_content="BOOK CONTENT",
        creative_direction="求生建造",
        gbrain_inspiration="Contrast：从个人套利转为组织能力",
        actual_summaries="实际十章内容",
    )
    assert "求生建造" in prompt
    assert "组织能力" in prompt


def test_chapter_prompt_does_not_start_a_gbrain_query(monkeypatch) -> None:
    def unexpected_query(_query: str) -> str:
        raise AssertionError("chapter prompt must not query GBrain")

    monkeypatch.setattr(app_module, "query_gbrain", unexpected_query)
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    response = client.post(
        "/api/prompt",
        json={
            "mode": "chapter",
            "template": "CHAPTER TEMPLATE",
            "book_content": "BOOK",
            "current_outline": outline,
            "gbrain_inspiration": "本十章已选灵感",
        },
    )
    assert response.status_code == 200
    assert "本十章已选灵感" in response.json()["prompt"]


def test_page_shows_editable_gbrain_query_and_results() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="creative-direction"' in page.text
    assert 'id="gbrain-query"' in page.text
    assert 'id="gbrain-results"' in page.text
    assert "从 GBrain 取灵感" in page.text


def test_default_prompt_templates_include_idea_mode() -> None:
    response = client.get("/api/prompt-templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert set(templates) == {"idea", "outline", "chapter", "review"}
    assert Path("docs/MVP_PRODUCT_DIRECTION.md").is_file()
    assert all("中文男频成长爽文" in templates[mode] for mode in ("idea", "outline", "review"))
    assert "中文男频成长爽文" not in templates["chapter"]


def test_outline_prompt_injects_book_content_once() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="OUTLINE TEMPLATE",
        book_content="UNIQUE BOOK CONTENT",
    )
    assert prompt.count("UNIQUE BOOK CONTENT") == 1
