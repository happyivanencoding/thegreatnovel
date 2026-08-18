from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml
from fastapi.testclient import TestClient

import story_mvp.app as app_module
import story_mvp.gbrain as gbrain_module
from story_mvp.app import app
from story_mvp.gbrain import GBrainQueryError, query_gbrain, resolve_command_prefix
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, HardGateError, generate_prompt
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
    assert set(payload["sections"]) == {"design", "long_plan", "small_plan", "status"}
    assert len(payload["design_sections"]) == 13
    assert "growth_genome" in payload["design_sections"]
    assert "## 0. 本书成长基因图" in payload["book_content"]


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
    duplicate = client.post(
        "/api/books/demo/chapters",
        json={"chapter_number": 7, "content": "replacement body"},
    )
    assert duplicate.status_code == 400
    assert "已经存在" in duplicate.json()["detail"]
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


def test_gbrain_query_uses_bun_cli_when_path_command_is_missing(tmp_path: Path, monkeypatch) -> None:
    cli_file = tmp_path / "src" / "cli.ts"
    cli_file.parent.mkdir()
    cli_file.write_text("// test cli", encoding="utf-8")
    monkeypatch.setattr(gbrain_module, "HERMES_CLI", cli_file)

    def fake_which(name: str):
        return {"gbrain": None, "bun": "bun.exe"}.get(name)

    monkeypatch.setattr(gbrain_module.shutil, "which", fake_which)
    assert resolve_command_prefix() == ["bun.exe", "run", str(cli_file)]


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
        book_content="# 小说总体设计画像\n\n## 0. 本书成长基因图\n\n知识 → 职业 → 世界入口",
        creative_direction="求生建造",
        gbrain_inspiration="Contrast：从个人套利转为组织能力",
        actual_summaries="实际十章内容",
    )
    assert "求生建造" in prompt
    assert "组织能力" in prompt
    assert "知识 → 职业 → 世界入口" in prompt


def test_review_prompt_discusses_growth_loop_variation() -> None:
    prompt = generate_prompt(
        mode="review",
        template=DEFAULT_PROMPT_TEMPLATES["review"],
        book_content="# 小说总体设计画像\n\n## 0. 本书成长基因图\n\n规则理解 × 关系网络",
    )
    assert "本书成长基因图" in prompt
    assert "当前实际运行了什么成长循环" in prompt
    assert "是否重复使用同一路径" in prompt
    assert "成长基因图是否需要更新" in prompt


def test_outline_prompt_has_exact_book_headings_and_concrete_formats() -> None:
    prompt = generate_prompt(
        mode="outline",
        template=DEFAULT_PROMPT_TEMPLATES["outline"],
        book_content="BOOK",
    )
    for heading in (
        "# 小说总体设计画像",
        "# 未来100章大型剧情块",
        "# 未来十章逐章小纲",
        "# 当前状态、未兑现承诺与作者备注",
    ):
        assert heading in prompt
    assert "## 0. 本书成长基因图" in prompt
    assert "核心组合" in prompt
    assert "转换网络" in prompt
    assert "循环族" in prompt
    assert "阶段变异" in prompt
    assert "POWER_BREAKTHROUGH" not in prompt
    assert "资源 → 修炼" not in prompt
    assert "4—8 个自然剧情块" in prompt
    assert all(f"## {number}." in prompt for number in range(1, 13))
    assert "完整输出所有剧情块" in prompt
    assert "覆盖第1章到第100章" in prompt
    assert "具体发生" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt


def test_review_prompt_uses_the_concrete_small_outline_format() -> None:
    prompt = generate_prompt(
        mode="review",
        template=DEFAULT_PROMPT_TEMPLATES["review"],
        book_content="BOOK",
    )
    assert "## 下一批十章总体事件链" in prompt
    assert "3—6 句话" in prompt
    assert "具体剧情：用 2—4 句" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt


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
            "current_long_block": "当前块：废丹秘密与第一次生产循环",
            "current_outline": outline,
            "gbrain_inspiration": "本十章已选灵感",
        },
    )
    assert response.status_code == 200
    assert "本十章已选灵感" in response.json()["prompt"]


def test_chapter_prompt_uses_relevant_design_without_full_image_or_plan() -> None:
    book = """# 小说总体设计画像

## 0. 本书成长基因图
知识 → 职业 → 世界入口；循环在中期换挡。

## 1. 核心类型与读者承诺
男频成长爽文；主角从废丹套利进入药行。

## 2. 世界观结构
修炼等级和资源市场互相咬合。

## 4. 主角模型、人物弧与核心矛盾
发现信息 → 小规模验证 → 隐藏优势 → 建立渠道。

## 5. 配角与关系系统
周安是长期利益伙伴。

## 8. 文风与可操作参数
短段落、高信息密度、对话用于博弈。

## 9. 对话特点
角色说话都带有交易目的。

## 12. 当前设计最强点与最弱点
强点是资源到身份的因果链。

# 未来100章大型剧情块
FULL_PLAN_SHOULD_NOT_ENTER

# 当前状态、未兑现承诺与作者备注
当前在第一章前。
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=book,
        current_long_block="当前块：废丹秘密与第一次生产循环",
        current_outline=outline,
    )
    assert "男频成长爽文" in prompt
    assert "知识 → 职业 → 世界入口" in prompt
    assert "废丹套利" in prompt
    assert "当前块：废丹秘密与第一次生产循环" in prompt
    assert "FULL_PLAN_SHOULD_NOT_ENTER" not in prompt
    assert "## 12. 当前设计最强点与最弱点" not in prompt
    assert "MVP_PRODUCT_DIRECTION" not in prompt
    assert "诡秘之主" not in prompt


def test_page_shows_editable_gbrain_query_and_results() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="creative-direction"' in page.text
    assert 'id="gbrain-query"' in page.text
    assert 'id="gbrain-results"' in page.text
    assert 'id="design-growth_genome"' in page.text
    assert "GBrain 范围：全 Brain" in page.text
    assert "从 GBrain 取灵感" in page.text
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "Reader Promise" in js
    assert "Core Progression Grammar" in js
    assert "POWER_BREAKTHROUGH" not in js
    assert "秘境" not in js
    assert "历史建设" not in js
    assert "都市职业" not in js


def test_page_shows_twelve_design_sections_and_panorama_controls() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert 'id="expand-design"' in page.text
    assert 'id="collapse-design"' in page.text
    assert 'id="long-plan-panorama"' in page.text
    assert page.text.count('class="design-card"') == 13


def test_panorama_and_apply_contracts_refresh_without_book_write() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "function parseLongPlanBlocks" in js
    assert "function renderLongPlanPanorama" in js
    assert '$("section-long_plan").addEventListener("input", renderLongPlanPanorama)' in js
    apply_start = js.index("function applyOutlineToBook()")
    apply_end = js.index("async function saveBook()", apply_start)
    apply_body = js[apply_start:apply_end]
    assert "renderLongPlanPanorama()" in apply_body
    assert "designTitles" in apply_body
    assert "section-${key}" in apply_body
    assert "requestJson" not in apply_body


def test_default_prompt_templates_include_idea_mode() -> None:
    response = client.get("/api/prompt-templates")
    assert response.status_code == 200
    templates = response.json()["templates"]
    assert set(templates) == {"idea", "outline", "chapter", "review"}
    direction_doc = Path("docs/MVP_PRODUCT_DIRECTION.md")
    assert direction_doc.is_file()
    direction_text = direction_doc.read_text(encoding="utf-8")
    assert "Composable Growth Genome" in Path("docs/COMPOSABLE_GROWTH_GENOME.md").read_text(encoding="utf-8")
    assert "累积成长与可组合成长" in direction_text
    assert all("成长" in templates[mode] for mode in ("idea", "outline"))
    assert "成长组合" in templates["idea"]
    assert "初始转换网络" in templates["idea"]
    assert "## 0. 本书成长基因图" in templates["outline"]
    assert "POWER_BREAKTHROUGH" not in Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")


def test_outline_prompt_injects_book_content_once() -> None:
    prompt = generate_prompt(
        mode="outline",
        template="OUTLINE TEMPLATE",
        book_content="UNIQUE BOOK CONTENT",
    )
    assert prompt.count("UNIQUE BOOK CONTENT") == 1


def test_apply_outline_to_book_is_browser_only() -> None:
    html = Path("src/story_mvp/templates/index.html").read_text(encoding="utf-8")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert 'id="apply-outline-to-book"' in html
    start = js.index("function applyOutlineToBook()")
    end = js.index("async function saveBook()", start)
    function_body = js[start:end]
    assert "requestJson" not in function_body
    assert "fetch(" not in function_body
    assert "/book" not in function_body
