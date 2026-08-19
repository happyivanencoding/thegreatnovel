from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml
from fastapi.testclient import TestClient

import story_mvp.app as app_module
import story_mvp.gbrain as gbrain_module
from story_mvp.app import app
from story_mvp.gbrain import GBrainQueryError, query_gbrain, resolve_command_prefix
from story_mvp.gbrain_retrieval import (
    EMPTY_RESULT,
    FINAL_RESULT_LIMIT,
    RAW_RESULT_LIMIT,
    _forbidden_terms,
    build_retrieval_brief,
    extract_hard_constraints,
    parse_query_results,
    retrieve_gbrain,
)
from story_mvp.prompts import (
    DEFAULT_PROMPT_TEMPLATES,
    PROSE_REALIZATION_CONTRACT,
    HardGateError,
    generate_prompt,
)
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


def test_chapter_prompt_includes_rhythm_profile_without_full_plan_or_strengths() -> None:
    book = """# 小说总体设计画像

## 7. 叙事结构
视角 marker

## 8. 文风与可操作参数
文风 marker

## 9. 对话特点
对话 marker

## 10. 节奏结构
RHYTHM_MARKER_ALPHA

## 12. 当前设计最强点与最弱点
STRENGTHS_MARKER_BETA

# 未来100章大型剧情块
FULL_PLAN_MARKER_GAMMA
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=book,
        current_outline=outline,
    )
    assert "RHYTHM_MARKER_ALPHA" in prompt
    assert "FULL_PLAN_MARKER_GAMMA" not in prompt
    assert "STRENGTHS_MARKER_BETA" not in prompt


def test_chapter_prompt_uses_formal_body_as_status_authority() -> None:
    book = """# 小说总体设计画像

## 7. 叙事结构
NARRATIVE_MARKER

## 8. 文风与可操作参数
PROSE_MARKER

## 9. 对话特点
DIALOGUE_MARKER

## 10. 节奏结构
RHYTHM_MARKER

# 当前状态、未兑现承诺与作者备注
STATUS_MARKER
"""
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER TEMPLATE",
        book_content=book,
        current_outline=outline,
    )
    assert prompt.count("STATUS_MARKER") == 1
    for marker in (
        "已批准的前文正文是已发生事实的最高来源",
        "BOOK 当前状态和最近摘要只是正文事实的压缩索引",
        "以正式正文为准",
        "当前章小纲只决定尚未发生的本章事件",
        "任何冲突必须写入 Writer Audit",
    ):
        assert marker in prompt


def test_legacy_chapter_template_receives_prose_contract_once() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template="LEGACY CHAPTER TEMPLATE",
        book_content="",
        current_outline=outline,
    )
    assert "# Story MVP Prose Realization Contract" in prompt
    assert prompt.count(PROSE_REALIZATION_CONTRACT) == 1


def test_default_chapter_prompt_has_no_source_style_leakage() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=outline,
    )
    for marker in (
        "《第一序列》", "《将夜》", "《诡秘之主》", "模仿《", "仿写《",
        "PROSE_DISTILLATION_THREE_CLASSICS.md", ".agents/skills/novel-prose-realization",
    ):
        assert marker not in prompt


def test_chapter_prompt_includes_diction_and_sentence_controls() -> None:
    outline = "\n".join(f"{field}：内容" for field in (
        "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
        "直接结果", "状态变化", "叙事功能", "结尾推动力",
    ))
    prompt = generate_prompt(
        mode="chapter",
        template=DEFAULT_PROMPT_TEMPLATES["chapter"],
        book_content="",
        current_outline=outline,
    )
    for marker in (
        "具体名词",
        "方向、接触对象与实际结果",
        "真实不确定性",
        "语体服从人物身份、关系与当前压力",
        "sentence realization",
        "锚点→动作→反应→条件改变",
        "观察→暂定解释→新细节→修正→行动",
        "可选关系，不是每段都套用的模板",
    ):
        assert marker in prompt
    for marker in (
        "《第一序列》", "《将夜》", "《诡秘之主》",
        "会说话的肘子", "猫腻", "爱潜水的乌贼", "C:\\dev\\tgn-story-mvp",
    ):
        assert marker not in prompt


def test_chapter_template_exposes_writer_responsibilities() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["chapter"]
    assert "Writer A — Scene Draft" in template
    assert "Writer B — Continuity & Realization" in template
    assert "Writer C — Prose Realization & Bounded Humanization" in template
    assert "不把小纲扩写成更长概述" in template
    assert "不能改变事实、事件顺序" in template


def test_outline_template_requests_executable_prose_profile() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["outline"]
    assert "何时贴近或拉远" in template
    assert "高低压力场景的句段变化" in template
    assert "词汇、句长、礼貌、攻击性、避答和沉默方式" in template
    assert "opening、ordinary、dialogue、action、payoff、aftermath、emotion、ending" in template
    assert "名词具体度" in template
    assert "动词的方向/接触/结果" in template
    assert "修饰词使用倾向" in template
    assert "不确定词使用边界" in template
    assert "口语/庄重/专业语体边界" in template


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
    read_saved = client.get("/api/books/demo/chapters/7")
    read_missing = client.get("/api/books/demo/chapters/6")
    assert read_saved.status_code == 200
    assert read_saved.json()["content"] == "chapter body"
    assert read_missing.status_code == 200
    assert read_missing.json()["content"] == ""
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
    assert "--limit" in calls["command"]
    assert "8" in calls["command"]
    assert "--detail" in calls["command"]
    assert calls["kwargs"]["capture_output"] is True


def test_gbrain_get_calls_public_cli(monkeypatch) -> None:
    calls: dict[str, object] = {}
    monkeypatch.setattr(gbrain_module.shutil, "which", lambda name: "gbrain.CMD")

    def fake_run(command, **kwargs):
        calls["command"] = command
        calls["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="---\ntype: concept\n---\n\n## Mechanism\n\nfull page", stderr="")

    monkeypatch.setattr(gbrain_module.subprocess, "run", fake_run)
    assert "## Mechanism" in gbrain_module.get_gbrain("mechanisms/example")
    assert calls["command"] == ["gbrain.CMD", "get", "mechanisms/example"]


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
    def fail_query(**_kwargs):
        raise GBrainQueryError("真实 CLI 失败")

    monkeypatch.setattr(app_module, "retrieve_gbrain", fail_query)
    response = client.post("/api/gbrain/query", json={"mode": "idea"})
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
        creative_direction="AUTHOR_DIRECTION_ALPHA",
        gbrain_inspiration="Book DNA：阶段回报窗口",
    )
    assert "AUTHOR_DIRECTION_ALPHA" in prompt
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
    assert "经典成长模式是一等公民" in prompt
    assert "一个主循环和零到多个辅助循环" in prompt
    assert "4—8 个自然剧情块" in prompt
    assert all(f"## {number}." in prompt for number in range(1, 13))
    assert "完整输出所有剧情块" in prompt
    assert "覆盖第1章到第100章" in prompt
    assert "具体发生" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt
    assert "第一章开篇策略" in prompt
    assert "第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点" in prompt


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
    assert "第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点" in prompt


def test_chapter_prompt_does_not_start_a_gbrain_query(monkeypatch) -> None:
    def unexpected_query(_query: str) -> str:
        raise AssertionError("chapter prompt must not query GBrain")

    monkeypatch.setattr(app_module, "retrieve_gbrain", unexpected_query)
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
            "current_long_block": "CURRENT_LONG_BLOCK_DELTA",
            "previous_chapter_text": "# 第1章正文\n\n上一章最后一句：门外有人敲门。",
            "current_outline": outline,
            "gbrain_inspiration": "本十章已选灵感",
        },
    )
    assert response.status_code == 200
    assert "本十章已选灵感" in response.json()["prompt"]
    assert "上一章最后一句：门外有人敲门" in response.json()["prompt"]


def test_chapter_prompt_uses_relevant_design_without_full_image_or_plan() -> None:
    book = """# 小说总体设计画像

## 0. 本书成长基因图
GENOME_MARKER_ALPHA；循环在中期换挡。

## 1. 核心类型与读者承诺
主角成长型虚构世界；读者期待能力改变行动空间。

## 2. 世界观结构
WORLD_RULE_ALPHA：两套规则互相咬合。

## 3. 世界如何持续制造剧情压力
WORLD_PRESSURE_BETA：环境压力和敌人试探会推动主角行动。

## 4. 主角模型、人物弧与核心矛盾
PROTAGONIST_STYLE_BETA：发现信息 → 小规模验证 → 隐藏优势。

## 5. 配角与关系系统
RELATION_MARKER_GAMMA：长期关系会改变主角选择。

## 7. 叙事结构
贴近主角第三人称，必要时使用他人反应。

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
        current_long_block="CURRENT_LONG_BLOCK_DELTA",
        current_outline=outline,
    )
    assert "GENOME_MARKER_ALPHA" in prompt
    assert "WORLD_RULE_ALPHA" in prompt
    assert "WORLD_PRESSURE_BETA" in prompt
    assert "PROTAGONIST_STYLE_BETA" in prompt
    assert "RELATION_MARKER_GAMMA" in prompt
    assert "CURRENT_LONG_BLOCK_DELTA" in prompt
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
    assert 'id="gbrain-raw-results"' in page.text
    assert 'id="gbrain-rejections"' in page.text
    assert 'id="gbrain-count"' in page.text
    assert 'id="chapter-body-for-save"' in page.text
    assert 'id="chapter-fact-summary"' in page.text
    assert 'id="extract-chapter-body"' in page.text
    assert 'id="design-growth_genome"' in page.text
    assert 'id="creative-direction" value=""' in page.text
    assert "例如：传统仙侠；资源→战斗→身份" in page.text
    assert "GBrain 范围：全 Brain 检索 → BOOK 兼容性筛选" in page.text
    assert "从 GBrain 取灵感" in page.text
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "function gbrainContextPayload" in js
    assert "query_override" in js
    assert "raw_stdout" in js
    assert "POWER_BREAKTHROUGH" not in js
    assert "秘境" not in js
    assert "历史建设" not in js
    assert "都市职业" not in js
    assert "BOOK-aware Retrieval Brief" in page.text
    assert "/api/gbrain/brief" in js


def test_default_retrieval_query_uses_context_instead_of_generic_prefix() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("function gbrainContextPayload")
    end = js.index("async function setDefaultGbrainQuery", start)
    context_body = js[start:end]
    assert 'book_content: composeBookContent()' in context_body
    assert 'current_long_block' in context_body
    assert 'current_outline' in context_body
    assert 'recent_summaries' in context_body
    assert "主角成长型虚构世界小说" not in js[start:]


REAL_COLD_CHAIN_BOOK = """# 小说总体设计画像

## 0. 本书成长基因图
现代都市职业成长；冷链调度；返程空载；仓库时间窗；司机信用；结算与责任。

## 1. 核心类型与读者承诺
现实世界职业成长。

## 2. 世界观结构
司机、仓库、门店、订单和时间窗。

# 当前状态、未兑现承诺与作者备注
现实世界；没有超自然；没有修炼；没有战斗升级；没有副本或异世界。
"""

REAL_COLD_CHAIN_OUTLINE = """触发事件：主角被收走车队权限并接到急单。
推动事件的人：采购和车队负责人。
主角行动：翻出三个月返程空载记录，寻找第一段现实路线。
对手或世界反应：车辆能到第一城，但没有第二城预约号。
直接结果：第一段路线出现，第二段无法直送。
状态变化：主角失去公司担保但保留个人记录。
叙事功能：把职业优势落到现场行动。
结尾推动力：继续寻找夜班仓库节点。
"""

REAL_WORLD_SUPERPOWER_BOOK = """# 小说总体设计画像

## 0. 本书成长基因图
现代都市；现实世界；现实社会结构；存在少量异能；主角拥有异常感知能力。

## 1. 核心类型与读者承诺
职业调查、信息差、人际关系、资源、身份与组织博弈。

## 2. 世界观结构
真实公司、警察、医院、学校、互联网、金融、交通、劳动合同和法律制度；异能不改变社会基础设施。

# 当前状态、未兑现承诺与作者备注
不使用修炼体系；没有境界升级；没有灵气；没有宗门；没有武道等级；没有学院试炼；没有副本；没有遗迹探索；没有异世界穿越。
"""

REAL_WORLD_BOOK = """# 小说总体设计画像
现代都市；现实世界；现实社会结构；没有超自然；没有异能；没有修炼体系。
"""

XIANXIA_BOOK = """# 小说总体设计画像
仙侠世界；修炼体系；境界突破；宗门资源。
"""

SUPERPOWER_PAGE = """---
type: concept
---

## Mechanism

主角通过一种别人无法获得的信息渠道发现隐藏事实，异常能力只提供信息，不直接解决现实中的执行、关系和责任问题。

## Failure Modes

如果异能直接代替调查、谈判和行动，故事会退化成自动答案机。

## Transfer Boundary

保留信息差与使用限制；具体能力实现服从当前 BOOK。
"""

CULTIVATION_PAGE = """---
type: concept
---

## Mechanism

主角通过吸收灵气修炼功法，不断突破新的境界，并依靠宗门资源成长。

## Transfer Boundary

保留修炼突破，不迁移具体来源故事。
"""

REAL_WORLD_MECHANISM_PAGE = """---
type: concept
---

## Mechanism

主角通过公司记录、医院流程和访谈把异常线索转成可验证的调查行动。

## Transfer Boundary

只迁移调查与责任链，不迁移来源故事。
"""


def _page(heading: str, content: str) -> str:
    return f"---\ntype: concept\n---\n\n## {heading}\n\n{content}\n\n## Transfer Boundary\n\n只迁移抽象结构，不迁移来源故事。"


def test_retrieval_brief_is_book_and_chapter_aware() -> None:
    brief = build_retrieval_brief(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        creative_direction="现代都市职业成长",
        current_long_block="冷链调度中把返程空载接到仓库时间窗。",
        current_outline=REAL_COLD_CHAIN_OUTLINE,
    )
    for marker in (
        "现代都市职业成长",
        "冷链调度",
        "返程空载",
        "仓库时间窗",
        "司机信用",
        "结算与责任",
        "主角被收走车队权限",
        "无超自然",
        "无修炼体系",
        "无战斗升级",
        "无副本",
        "无异世界",
    ):
        assert marker in brief
    assert "主角成长型虚构世界小说" not in brief


def test_real_world_does_not_imply_no_supernatural() -> None:
    constraints = extract_hard_constraints(REAL_WORLD_SUPERPOWER_BOOK)
    forbidden = _forbidden_terms(constraints)
    assert "现实世界" in constraints
    assert "无超自然" not in constraints
    assert "无修炼体系" in constraints
    assert "异能" not in forbidden
    assert "超自然" not in forbidden


def test_superpower_book_brief_preserves_setting_and_does_not_invent_no_supernatural() -> None:
    brief = build_retrieval_brief(
        mode="chapter",
        book_content=REAL_WORLD_SUPERPOWER_BOOK,
        creative_direction="现代都市男频成长小说",
        current_outline="主角用异常感知能力追查物品最近一次主动使用者。",
    )
    for marker in ("现代都市", "现实社会结构", "存在少量异能", "异常感知能力", "职业调查", "组织博弈"):
        assert marker in brief
    assert "明确硬约束：" in brief
    assert "无超自然" not in brief
    assert "无修炼体系" in brief


def test_real_world_superpower_keeps_superpower_mechanism() -> None:
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_SUPERPOWER_BOOK,
        query_func=lambda _query, **_kwargs: "[0.95] mechanisms/information-superpower -- 异能带来的信息差",
        page_func=lambda _slug: SUPERPOWER_PAGE,
    )
    assert result["accepted_count"] == 1
    assert "异能" in result["result"]
    assert "信息渠道" in result["result"]
    assert "自动答案机" in result["result"]


def test_real_world_superpower_still_rejects_cultivation() -> None:
    pages = {
        "mechanisms/information-superpower": SUPERPOWER_PAGE,
        "mechanisms/cultivation-breakthrough": CULTIVATION_PAGE,
    }
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_SUPERPOWER_BOOK,
        query_func=lambda _query, **_kwargs: "\n".join(
            [
                "[0.95] mechanisms/information-superpower -- 异能信息差",
                "[0.94] mechanisms/cultivation-breakthrough -- 修炼境界",
            ]
        ),
        page_func=pages.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == ["mechanisms/information-superpower"]
    assert any(
        item["slug"] == "mechanisms/cultivation-breakthrough"
        and item["reason"] == "与 BOOK 的明确硬约束冲突"
        for item in result["rejected"]
    )


def test_explicit_no_supernatural_rejects_superpower_in_pure_real_book() -> None:
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_BOOK,
        query_func=lambda _query, **_kwargs: "[0.95] mechanisms/information-superpower -- 异能信息差",
        page_func=lambda _slug: SUPERPOWER_PAGE,
    )
    assert result["accepted_count"] == 0
    assert result["result"] == EMPTY_RESULT
    assert result["rejected"][0]["reason"] == "与 BOOK 的明确硬约束冲突"


def test_pure_real_book_keeps_reality_mechanism_and_rejects_forbidden_surfaces() -> None:
    pages = {
        "mechanisms/urban-investigation": REAL_WORLD_MECHANISM_PAGE,
        "mechanisms/information-superpower": SUPERPOWER_PAGE,
        "mechanisms/cultivation-breakthrough": CULTIVATION_PAGE,
    }
    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_WORLD_BOOK,
        query_func=lambda _query, **_kwargs: "\n".join(
            [
                "[0.97] mechanisms/urban-investigation -- 现实职业调查",
                "[0.96] mechanisms/information-superpower -- 异能信息差",
                "[0.95] mechanisms/cultivation-breakthrough -- 修炼境界",
            ]
        ),
        page_func=pages.__getitem__,
    )
    assert [item["slug"] for item in result["accepted"]] == ["mechanisms/urban-investigation"]
    assert "公司记录" in result["result"]
    assert {item["slug"] for item in result["rejected"]} == {
        "mechanisms/information-superpower",
        "mechanisms/cultivation-breakthrough",
    }


def test_xianxia_without_negative_constraints_keeps_cultivation() -> None:
    constraints = extract_hard_constraints(XIANXIA_BOOK)
    assert "现实世界" not in constraints
    assert "无修炼体系" not in constraints
    result = retrieve_gbrain(
        mode="chapter",
        book_content=XIANXIA_BOOK,
        query_func=lambda _query, **_kwargs: "[0.95] mechanisms/cultivation-breakthrough -- 修炼境界",
        page_func=lambda _slug: CULTIVATION_PAGE,
    )
    assert result["accepted_count"] == 1
    assert "修炼" in result["result"]


def test_three_fixture_spaces_keep_their_distinct_constraint_semantics() -> None:
    pure_real = extract_hard_constraints(REAL_WORLD_BOOK)
    superpower = extract_hard_constraints(REAL_WORLD_SUPERPOWER_BOOK)
    xianxia = extract_hard_constraints(XIANXIA_BOOK)
    assert "无超自然" in pure_real and "无超自然" not in superpower
    assert "无修炼体系" in pure_real and "无修炼体系" in superpower
    assert "无修炼体系" not in xianxia
    assert "现实世界" in pure_real and "现实世界" in superpower
    assert "现实世界" not in xianxia


def test_query_result_parser_ignores_noise_and_preserves_order() -> None:
    parsed = parse_query_results(
        "杂项\n[0.9] mechanisms/example -- first snippet\ncontinuation noise\n"
        "[0.7] prose-controls/example -- second snippet\n"
    )
    assert [item["slug"] for item in parsed] == ["mechanisms/example", "prose-controls/example"]
    assert parsed[0]["score"] == 0.9
    assert parsed[1]["snippet"] == "second snippet"


def test_chapter_filters_sources_and_builds_bundle_from_full_pages() -> None:
    raw = "\n".join(
        [
            "[0.99] arcs/old -- 修真 arc",
            "[0.98] book-dna/old -- 修炼 book",
            "[0.97] prose-dna/old -- 境界 prose",
            "[0.96] maps/progression -- map",
            "[0.95] prose-controls/action-neutral -- action snippet",
            "[0.94] syntheses/example-neutral -- synthesis snippet",
            "[0.93] mechanisms/example-neutral -- mechanism snippet",
        ]
    )
    calls: list[str] = []
    pages = {
        "prose-controls/action-neutral": _page("Control", "先让位置和操作发生，再补当前需要的规则和反馈。"),
        "syntheses/example-neutral": _page("Shared Tendencies", "阶段推进必须通过具体结果打开新的行动空间。"),
        "mechanisms/example-neutral": _page("Mechanism", "旧资源经过可验证转换，变成新的可用路径。"),
    }

    def fake_query(_query: str, **kwargs) -> str:
        assert kwargs == {"limit": RAW_RESULT_LIMIT, "detail": "medium"}
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return pages[slug]

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        current_outline=REAL_COLD_CHAIN_OUTLINE,
        query_func=fake_query,
        page_func=fake_get,
    )
    assert calls == list(pages)
    assert result["accepted_count"] == 3
    assert "旧资源经过可验证转换" in result["result"]
    assert "Evidence" not in result["result"]
    assert "source_book_id" not in result["result"]
    assert "修真" not in result["result"]
    assert any(item["reason"].startswith("chapter 模式不自动使用 arcs") for item in result["rejected"])
    assert any(item["reason"].startswith("chapter 模式不自动使用 book-dna") for item in result["rejected"])
    assert any(item["reason"].startswith("chapter 模式不自动使用 prose-dna") for item in result["rejected"])
    assert any(item["reason"].startswith("chapter 模式不自动使用 maps") for item in result["rejected"])


def test_get_failure_does_not_fallback_to_query_snippet() -> None:
    def fake_query(_query: str, **_kwargs) -> str:
        return "[0.9] mechanisms/failing -- snippet must not enter bundle"

    def fake_get(_slug: str) -> str:
        raise GBrainQueryError("get failed")

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        query_func=fake_query,
        page_func=fake_get,
    )
    assert result["accepted_count"] == 0
    assert result["result"] == EMPTY_RESULT
    assert "snippet must not enter bundle" not in result["result"]
    assert result["rejected"] == [{"slug": "mechanisms/failing", "reason": "完整页面读取失败"}]


def test_query_override_is_effective_but_book_constraints_still_apply() -> None:
    seen: list[str] = []

    def fake_query(query: str, **_kwargs) -> str:
        seen.append(query)
        return "[0.9] book-dna/incompatible -- 修真"

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        query_override="作者当前可见的手工查询",
        query_func=fake_query,
        page_func=lambda _slug: _page("Mechanism", "不应读取"),
    )
    assert seen == ["作者当前可见的手工查询"]
    assert result["effective_query"] == "作者当前可见的手工查询"
    assert result["accepted_count"] == 0
    assert result["rejected"][0]["reason"].startswith("chapter 模式不自动使用 book-dna")


def test_all_incompatible_sources_return_successful_empty_result() -> None:
    called = False

    def fake_query(_query: str, **_kwargs) -> str:
        return "[0.9] book-dna/old -- old\n[0.8] arcs/old -- old"

    def fake_get(_slug: str) -> str:
        nonlocal called
        called = True
        return _page("Mechanism", "should not be read")

    result = retrieve_gbrain(
        mode="chapter",
        book_content=REAL_COLD_CHAIN_BOOK,
        query_func=fake_query,
        page_func=fake_get,
    )
    assert result["status"] == "available"
    assert result["accepted_count"] == 0
    assert result["result"] == EMPTY_RESULT
    assert called is False


def test_application_and_final_limits_bound_overlong_cli_output() -> None:
    raw = "\n".join(f"[{1 - index / 100:.2f}] mechanisms/item-{index} -- snippet" for index in range(20))
    calls: list[str] = []

    def fake_query(_query: str, **kwargs) -> str:
        assert kwargs["limit"] == RAW_RESULT_LIMIT
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return _page("Mechanism", f"抽象材料 {slug}")

    result = retrieve_gbrain(mode="chapter", book_content="现实世界；无超自然", query_func=fake_query, page_func=fake_get)
    assert result["raw_count"] == 20
    assert result["requested_limit"] == RAW_RESULT_LIMIT
    assert result["final_limit"] == FINAL_RESULT_LIMIT
    assert result["accepted_count"] == FINAL_RESULT_LIMIT
    assert len(calls) == FINAL_RESULT_LIMIT
    assert sum(item["reason"] == "超过原始数量上限" for item in result["rejected"]) == 12


def test_idea_and_outline_keep_broader_sources_without_real_constraint() -> None:
    raw = "[0.9] book-dna/example -- broad\n[0.8] arcs/example -- broad"
    calls: list[str] = []

    def fake_query(_query: str, **_kwargs) -> str:
        return raw

    def fake_get(slug: str) -> str:
        calls.append(slug)
        return _page("Mechanism", "经典成长材料的抽象转换。")

    for mode in ("idea", "outline"):
        result = retrieve_gbrain(mode=mode, book_content="都市成长故事", query_func=fake_query, page_func=fake_get)
        assert result["accepted_count"] == 2
    assert calls == ["book-dna/example", "arcs/example", "book-dna/example", "arcs/example"]


def test_brief_and_query_api_expose_filter_counts(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "retrieve_gbrain",
        lambda **_kwargs: {
            "status": "available",
            "scope": "全 Brain 检索 → BOOK 兼容性筛选",
            "effective_query": "visible brief",
            "raw_count": 8,
            "accepted_count": 1,
            "rejected_count": 7,
            "requested_limit": 8,
            "final_limit": 5,
            "result": "FILTERED_BUNDLE",
            "raw_stdout": "RAW_STDOUT_MUST_STAY_OUTSIDE_PROMPT",
            "raw_results": [],
            "rejected": [],
        },
    )
    brief = client.post(
        "/api/gbrain/brief",
        json={"mode": "chapter", "book_content": REAL_COLD_CHAIN_BOOK, "current_outline": REAL_COLD_CHAIN_OUTLINE},
    )
    assert brief.status_code == 200
    assert "返程空载" in brief.json()["effective_query"]
    queried = client.post("/api/gbrain/query", json={"mode": "chapter"})
    assert queried.status_code == 200
    assert queried.json()["effective_query"] == "visible brief"
    assert queried.json()["raw_count"] == 8
    prompt = generate_prompt(mode="chapter", template="T", book_content="BOOK", current_outline=REAL_COLD_CHAIN_OUTLINE, gbrain_inspiration=queried.json()["result"])
    assert "FILTERED_BUNDLE" in prompt
    assert "RAW_STDOUT_MUST_STAY_OUTSIDE_PROMPT" not in prompt


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
    assert "Classic Patterns Are First-Class Citizens" in Path("docs/COMPOSABLE_GROWTH_GENOME.md").read_text(encoding="utf-8")
    assert "累积成长与可组合成长" in direction_text
    assert "Experiment Boundary" in direction_text
    assert all("成长" in templates[mode] for mode in ("idea", "outline"))
    assert "成长组合" in templates["idea"]
    assert "初始转换网络" in templates["idea"]
    assert "经典成长模式是一等公民" in templates["idea"]
    assert "经典成长模式是一等公民" in templates["outline"]
    assert "作者输入、GBrain证据或当前创意表明" in templates["idea"]
    assert "作者明确保留" in templates["outline"]
    assert "串行写作协议" in templates["chapter"]
    assert "选择性展开" in templates["chapter"]
    assert "SUBAGENT_MODE: actual" in templates["chapter"]
    assert "SUBAGENT_MODE: simulated" in templates["chapter"]
    assert "如果本书需要且对当前故事重要" in templates["outline"]
    assert "第一章开篇策略完全由作者和本书 BOOK 决定" in templates["outline"]
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


def test_proposal_source_is_explicit_and_editor_only() -> None:
    html = Path("src/story_mvp/templates/index.html").read_text(encoding="utf-8")
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    assert "proposalDraftActive" not in js
    assert "将 Codex 返回放入 Proposal 编辑区" in html
    assert "将 Proposal 应用到 BOOK 编辑区" in html
    assert "唯一 Proposal 来源" in html

    apply_start = js.index("function applyOutlineToBook()")
    apply_end = js.index("function extractChapterArtifact", apply_start)
    apply_body = js[apply_start:apply_end]
    assert 'const source = $("proposal-editor").value;' in apply_body
    assert '$("codex-response").value' not in apply_body
    assert "Proposal 编辑区中的" in apply_body

    save_start = js.index("async function saveProposal()")
    save_end = js.index("async function approveChapter", save_start)
    save_body = js[save_start:save_end]
    assert 'const draft = $("proposal-editor").value;' in save_body
    assert '$("codex-response").value' not in save_body
    assert "Proposal 编辑区已保存到 PROPOSAL.md" in save_body

    assert '$("apply-response").addEventListener("click"' in js
    assert 'applyResponseToEditor($("codex-response"), $("proposal-editor"));' in js
    assert '$("proposal-editor").value = $("codex-response").value' not in js
    assert '$("codex-response").addEventListener("input"' not in js
    assert '$("proposal-editor").addEventListener("input"' not in js


def test_generate_prompt_does_not_clear_proposal_editor() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("async function generatePrompt()")
    end = js.index("async function generateIdeaPrompt", start)
    function_body = js[start:end]
    assert 'const payload = await requestJson("/api/prompt"' in function_body
    assert '$("prompt-text").value = payload.prompt;' in function_body
    assert "proposal-editor" not in function_body
    assert "codex-response" not in function_body
    assert "composeBookContent" not in function_body
    assert "saveBook" not in function_body


def test_previous_chapter_fetch_failure_is_visible_and_does_not_clear_context() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("async function refreshPreviousChapterText()")
    end = js.index("async function loadBook", start)
    function_body = js[start:end]
    assert "const chapters = [];" in function_body
    assert "target.value = chapters.join" in function_body
    assert "读取第${number}章连续性上下文失败：${error.message}" in function_body
    assert "catch {" not in function_body
    assert 'target.value = "";' not in function_body.split("const first", 1)[1]


def test_chapter_response_contract_saves_only_extracted_body() -> None:
    js = Path("src/story_mvp/static/app.js").read_text(encoding="utf-8")
    start = js.index("function extractChapterArtifact")
    end = js.index("async function saveBook", start)
    parser = js[start:end]
    assert 'const bodyHeading = "# 正式正文";' in parser
    assert 'const summaryHeading = "# 章节事实摘要";' in parser
    approve_start = js.index("async function approveChapter")
    approve_end = js.index("async function createBook", approve_start)
    approve = js[approve_start:approve_end]
    assert 'const chapterBody = $("chapter-body-for-save").value.trim();' in approve
    assert 'content: chapterBody' in approve
    assert 'content: $("codex-response").value' not in approve
