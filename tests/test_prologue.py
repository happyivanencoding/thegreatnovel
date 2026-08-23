from pathlib import Path

from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.chapter_context import build_prologue_context
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt
from story_mvp.run_ledger import create_or_load_run
from story_mvp.storage import create_book, read_book_payload, read_prologue, save_chapter, save_prologue
from story_mvp.workflow_state import workflow_impact, workflow_status
from story_mvp.workflow_cli import apply_response


OUTLINE = "\n".join(
    f"{field}：内容"
    for field in (
        "触发事件",
        "推动事件的人",
        "主角行动",
        "对手或世界反应",
        "直接结果",
        "状态变化",
        "叙事功能",
        "结尾推动力",
    )
)

BOOK = """# 小说总体设计画像

## 2. 世界观结构

WORLD_STRUCTURE

## 3. 世界如何持续制造剧情压力

WORLD_PRESSURE

## 7. 叙事结构

PROLOGUE_DIRECTION

## 8. 文风与可操作参数

PROSE_PROFILE

# 当前中期规划窗口

LONG_PLAN

# 未来十章逐章小纲

FUTURE_PLAN

# 当前状态、未兑现承诺与作者备注

STATUS
"""


def test_prologue_prompt_uses_small_event_context() -> None:
    prompt = generate_prompt(
        mode="prologue",
        template="",
        book_content=BOOK,
        current_long_block="CURRENT_FIRST_BLOCK",
        current_chapter_plan="CURRENT_FIRST_CHAPTER_PLAN",
        creative_direction="AUTHOR_PROLOGUE_INTENT",
    )

    assert DEFAULT_PROMPT_TEMPLATES["prologue"]
    assert "具体异常事件承载世界规则" in prompt
    assert "不是固定步骤" in prompt
    assert "一两个有代表性的普通动作" in prompt
    assert "如果这本书不需要 Prologue，可以不创建它" in prompt
    assert "WORLD_STRUCTURE" in prompt
    assert "WORLD_PRESSURE" in prompt
    assert "PROLOGUE_DIRECTION" in prompt
    assert "CURRENT_FIRST_BLOCK" in prompt
    assert "CURRENT_FIRST_CHAPTER_PLAN" in prompt
    assert "AUTHOR_PROLOGUE_INTENT" in prompt
    assert "FUTURE_PLAN" not in prompt


def test_prologue_storage_is_optional_and_not_a_chapter(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)

    assert read_prologue("demo", tmp_path) == ""
    assert not (book_dir / "PROLOGUE.md").exists()

    save_prologue("demo", "序章正文", tmp_path)

    assert (book_dir / "PROLOGUE.md").read_text(encoding="utf-8") == "序章正文"
    assert read_prologue("demo", tmp_path) == "序章正文"
    assert not (book_dir / "chapters" / "chapter-0000.md").exists()
    assert read_book_payload("demo", tmp_path)["prologue"] == "序章正文"


def test_chapter_one_receives_prologue_as_reader_knowledge_not_previous_scene() -> None:
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER_TEMPLATE",
        book_content=BOOK,
        current_outline=OUTLINE,
        previous_chapter_text="PREVIOUS_SCENE_MARKER",
        prologue_text="PROLOGUE_READER_MARKER",
        chapter_number=1,
    )

    assert "CANON PROLOGUE / READER ALREADY KNOWS" in prompt
    assert "PROLOGUE_READER_MARKER" in prompt
    assert "PREVIOUS_SCENE_MARKER" in prompt
    assert "PROLOGUE_READER_MARKER" not in prompt.split("CANON PROLOGUE / READER ALREADY KNOWS", 1)[0]

    later_prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER_TEMPLATE",
        book_content=BOOK,
        current_outline=OUTLINE,
        prologue_text="PROLOGUE_READER_MARKER",
        chapter_number=2,
    )
    assert "CANON PROLOGUE / READER ALREADY KNOWS" not in later_prompt
    assert "PROLOGUE_READER_MARKER" not in later_prompt


def test_state_delta_never_receives_prologue() -> None:
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=BOOK,
        chapter_number=1,
        chapter_prose="CHAPTER_PROSE",
        chapter_fact_summary="CHAPTER_FACTS",
        prologue_text="PROLOGUE_MUST_NOT_ENTER_STATE_DELTA",
    )

    assert "CHAPTER_PROSE" in prompt
    assert "CHAPTER_FACTS" not in prompt
    assert "PROLOGUE_MUST_NOT_ENTER_STATE_DELTA" not in prompt


def test_prologue_api_and_prompt_mode(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)

    assert client.post("/api/books", json={"book_id": "demo"}).status_code == 201
    assert client.get("/api/books/demo/prologue").json() == {
        "file": "PROLOGUE.md",
        "content": "",
    }

    saved = client.put("/api/books/demo/prologue", json={"content": "API_PROLOGUE"})
    assert saved.status_code == 200
    assert saved.json() == {"status": "saved", "file": "PROLOGUE.md"}
    assert client.get("/api/books/demo").json()["prologue"] == "API_PROLOGUE"

    rendered = client.post(
        "/api/prompt",
        json={
            "mode": "prologue",
            "book_id": "demo",
            "book_content": BOOK,
            "current_long_block": "CURRENT_BLOCK",
            "current_chapter_plan": "CURRENT_PLAN",
            "creative_direction": "AUTHOR_INTENT",
        },
    )
    assert rendered.status_code == 200
    assert "具体异常事件承载世界规则" in rendered.json()["prompt"]


def test_prologue_ui_wiring_is_visible_and_explicit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    page = TestClient(app).get("/")
    assert page.status_code == 200
    for marker in (
        'id="prologue-body"',
        'id="generate-prologue-prompt"',
        'id="apply-prologue-response"',
        'id="save-prologue"',
        'id="template-prologue"',
        'value="prologue"',
        "十五个 Prompt 模板",
    ):
        assert marker in page.text
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "async function savePrologue" in js
    assert 'prologue: $("template-prologue").value' in js
    assert 'prologue_text: $("prologue-body").value' in js
    assert 'if (["fantasy_seed", "prologue"].includes' in js


def test_prologue_revision_stales_unfixed_chapter_one_run(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    save_prologue("demo", "PROLOGUE_V1", tmp_path)
    create_or_load_run(book_dir, 1)

    before = workflow_status(book_dir)["artifacts"]
    assert before["book.prologue"]["revision"] == 1
    save_prologue("demo", "PROLOGUE_V2", tmp_path)
    after = workflow_status(book_dir)["artifacts"]

    assert after["book.prologue"]["revision"] == 2
    assert after["chapter.1.run"]["status"] == "STALE"
    impact = workflow_impact(book_dir, "book.prologue")
    assert "chapter.1.run" in impact["existing_nodes_affected"]


def test_prologue_revision_does_not_stale_saved_chapter_one_body(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    save_prologue("demo", "PROLOGUE_V1", tmp_path)
    create_or_load_run(book_dir, 1)
    save_chapter("demo", 1, "FORMAL_CHAPTER_ONE", tmp_path)

    save_prologue("demo", "PROLOGUE_V2", tmp_path)
    artifacts = workflow_status(book_dir)["artifacts"]
    impact = workflow_impact(book_dir, "book.prologue")

    assert artifacts["chapter.1.body"]["status"] == "DONE"
    assert artifacts["chapter.1.run"]["status"] != "STALE"
    assert "chapter.1.run" in impact["existing_nodes_affected"]
    assert "chapter.1.body" in impact["protected_completed_chapters"]
    assert (book_dir / "chapters" / "chapter-0001.md").read_text(encoding="utf-8") == "FORMAL_CHAPTER_ONE"


def test_external_apply_supports_book_prologue(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    book_dir = create_book("demo", tmp_path)
    response = tmp_path / "prologue-response.md"
    response.write_text("EXTERNAL_PROLOGUE", encoding="utf-8")

    result = apply_response(
        book_id="demo",
        artifact="book.prologue",
        input_path=response,
        source="codex_external",
    )

    assert result["artifact"] == "book.prologue"
    assert (book_dir / "PROLOGUE.md").read_text(encoding="utf-8") == "EXTERNAL_PROLOGUE"
