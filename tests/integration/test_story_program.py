from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from novel_authoring.db.database import Database
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookKind, BookRegistry, CreationMode
from novel_authoring.story_program.board import (
    initial_board,
    read_board,
)
from novel_authoring.story_program.prompt_builder import build_prompt, concrete_plan_gate
from novel_authoring.story_program.reference_programs import load_reference_programs
from novel_authoring.story_program.service import (
    prepare_paths,
    save_chapter,
    save_story_board,
)
from novel_authoring.web.app import create_app

BOOK_ID = "story-program-test"


def _write_program(root: Path, program_id: str, status: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{program_id}.yaml").write_text(
        "\n".join(
            [
                f"program_id: {program_id}",
                "source_book_id: reference-book",
                f"status: {status}",
                "story_phase: opening",
                "input_state: 主角拥有有限资源",
                "reader_promise: 先解决局部瓶颈，再打开新的行动空间",
                "central_pressure: 资源渠道被主动竞争者干扰",
                "reusable_program: 瓶颈 -> 替代方法 -> 局部证明 -> 新压力",
                "applicable_conditions:",
                "  - 故事需要建立可重复资源循环",
                "failure_modes:",
                "  - 只增加敌人强度，不改变行动方式",
                "anti_repetition_notes:",
                "  - 下一次应改变渠道或风险所有权",
                "output_state: 主角获得新渠道但承担身份风险",
            ]
        ),
        encoding="utf-8",
    )


@pytest.fixture()
def project(tmp_path: Path) -> tuple[BookLayout, Path, Path]:
    layout = BookLayout(tmp_path / "library")
    paths = layout.ensure_book(BOOK_ID)
    for directory in paths.edition("base").all_directories():
        directory.mkdir(parents=True, exist_ok=True)
    BookRegistry(layout).ensure(
        BOOK_ID,
        title="透明工作台测试书",
        book_kind=BookKind.AUTHOR,
        creation_mode=CreationMode.ORIGINAL,
    )
    reference_root = tmp_path / "reference-programs"
    _write_program(reference_root, "validated-opening", "VALIDATED")
    _write_program(reference_root, "provisional-opening", "PROVISIONAL")
    _write_program(reference_root, "ignored-opening", "DRAFT")
    return layout, paths.root, reference_root


def _app(project: tuple[BookLayout, Path, Path]):
    layout, _book_root, reference_root = project
    return create_app(
        Database(layout.library_root.parent / "boot.sqlite3"),
        library_root=layout.library_root,
        story_program_reference_root=reference_root,
    )


def _headers(client: TestClient) -> dict[str, str]:
    return {"X-CSRF-Token": client.app.state.csrf_token}


def test_reference_programs_default_to_validated_and_expose_core_fields(
    project: tuple[BookLayout, Path, Path],
) -> None:
    _layout, _book_root, reference_root = project
    programs = load_reference_programs(reference_root)
    assert [item.program_id for item in programs] == ["validated-opening"]
    assert programs[0].central_pressure == "资源渠道被主动竞争者干扰"
    assert programs[0].anti_repetition_notes == ("下一次应改变渠道或风险所有权",)

    with_provisional = load_reference_programs(reference_root, include_provisional=True)
    assert {item.program_id for item in with_provisional} == {
        "validated-opening",
        "provisional-opening",
    }


def test_new_book_form_creates_markdown_story_program_workspace(
    project: tuple[BookLayout, Path, Path],
) -> None:
    layout, _book_root, _reference_root = project
    client = TestClient(_app(project))
    response = client.post(
        "/api/story-program/books",
        headers=_headers(client),
        json={
            "book_id": "new-story-program",
            "title": "废药与夜班药铺",
            "premise": "主角把废药修复成新资源，却被黑市药商盯上。",
            "genre": "都市超凡",
            "reader_experience": "看见一个小能力逐步改变行动空间。",
            "forbidden_style": "抽象升级\n工具人配角",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["redirect_url"] == "/books/new-story-program/story-program"
    new_paths = layout.for_book("new-story-program")
    board_path = new_paths.root / "story_program" / "BOOK_BOARD.md"
    assert board_path.is_file()
    assert "废药与夜班药铺" in board_path.read_text(encoding="utf-8")
    assert (new_paths.root / "story_program" / "GBRAIN_PROMPTS.md").is_file()
    with Database(new_paths.database).connect() as connection:
        handoffs = connection.execute("SELECT COUNT(*) FROM workflow_handoffs").fetchone()[0]
    assert handoffs == 0


def test_prompt_contains_only_visible_template_board_and_selected_reference(
    project: tuple[BookLayout, Path, Path],
) -> None:
    _layout, book_root, reference_root = project
    paths = prepare_paths(book_root)
    board = initial_board(title="废药与夜班药铺", premise="主角修复废药并被渠道竞争者盯上")
    programs = load_reference_programs(reference_root)
    result = build_prompt(
        template_file=paths.prompts,
        mode="new_book",
        payload={
            "title": "废药与夜班药铺",
            "premise": "主角修复废药并被渠道竞争者盯上",
            "genre": "都市超凡",
            "reader_experience": "看见小能力变成具体行动空间",
            "forbidden_style": "抽象升级",
            "reference_profile": "参考整体画像文本",
            "include_reference_profile": True,
            "reference_reason": "需要先建立具体资源循环",
        },
        board_markdown=board,
        references=programs,
    )
    assert result.prompt is not None
    assert "validated-opening" in result.prompt
    assert "资源渠道被主动竞争者干扰" in result.prompt
    assert "禁止复制：来源小说的人物" in result.prompt
    assert "## 页面可见作者输入" in result.prompt
    assert "未选择的 PROVISIONAL" not in result.prompt


def test_story_program_page_shows_reference_fields_and_full_prompt_template(
    project: tuple[BookLayout, Path, Path],
) -> None:
    client = TestClient(_app(project))
    response = client.get(f"/books/{BOOK_ID}/story-program")
    assert response.status_code == 200
    assert "GBrain Story Studio" in response.text
    assert "validated-opening" in response.text
    assert "资源渠道被主动竞争者干扰" in response.text
    assert "GBRAIN_PROMPTS.md 模板原文" in response.text
    assert "provisional-opening" not in response.text
    assert "未来100章方向：尚未建立" in response.text

    provisional = client.get(f"/books/{BOOK_ID}/story-program?include_provisional=1")
    assert provisional.status_code == 200
    assert "provisional-opening" in provisional.text
    assert "该 Program 的连续证据尚不完整" in provisional.text


def test_proposal_import_does_not_change_board_and_partial_adoption_is_explicit(
    project: tuple[BookLayout, Path, Path],
) -> None:
    _layout, book_root, _reference_root = project
    save_story_board(
        book_root,
        initial_board(title="旧标题", premise="旧创意"),
    )
    before = read_board(prepare_paths(book_root))
    client = TestClient(_app(project))
    proposal = """# Book Board

## 2. 小说价值观

故事赞赏具体承担代价的选择。

## 3. 世界观

世界通过资源垄断主动制造压力。
"""
    imported = client.post(
        f"/api/books/{BOOK_ID}/story-program/proposal",
        headers=_headers(client),
        json={"raw": proposal},
    )
    assert imported.status_code == 200, imported.text
    assert imported.json()["board_unchanged"] is True
    assert read_board(prepare_paths(book_root)) == before

    adopted = client.post(
        f"/api/books/{BOOK_ID}/story-program/proposal/adopt",
        headers=_headers(client),
        json={"sections": ["小说价值观"], "board_markdown": before},
    )
    assert adopted.status_code == 200, adopted.text
    board = read_board(prepare_paths(book_root))
    assert "故事赞赏具体承担代价的选择" in board
    assert "世界通过资源垄断主动制造压力" not in board


def test_prompt_generation_does_not_save_unsaved_board_and_concrete_gate_blocks_writer(
    project: tuple[BookLayout, Path, Path],
) -> None:
    _layout, book_root, reference_root = project
    save_story_board(book_root, initial_board(title="标题", premise="创意"))
    before = read_board(prepare_paths(book_root))
    client = TestClient(_app(project))
    incomplete = client.post(
        f"/api/books/{BOOK_ID}/story-program/prompt",
        headers=_headers(client),
        json={
            "mode": "current_chapter",
            "board_markdown": before + "\n作者临时修改但尚未保存。",
            "chapter_plan": "第1章：主角遇到危机。\n叙事功能：建立压力。",
            "program_ids": [],
        },
    )
    assert incomplete.status_code == 200, incomplete.text
    assert incomplete.json()["prompt"] is None
    assert "具体触发事件" in incomplete.json()["gate"]["missing"]
    assert read_board(prepare_paths(book_root)) == before

    complete_plan = """触发事件：主角收到哥哥寄来的超凡警告信。
推动事件的人：哥哥和被阴影控制的同学。
主角行动：主角使用尚未验证的仪式自救。
对手或世界反应：警察和陌生教会人员同时到场。
直接结果：主角确认超凡世界真实存在。
状态变化：知识增加，留下会被调查的仪式痕迹。
叙事功能：打破普通生活并制造调查压力。
结尾推动力：警察开始调查宿舍。
"""
    complete = client.post(
        f"/api/books/{BOOK_ID}/story-program/prompt",
        headers=_headers(client),
        json={
            "mode": "current_chapter",
            "board_markdown": before,
            "chapter_plan": complete_plan,
            "recent_summaries": "没有最近章节",
            "program_ids": ["validated-opening"],
            "reference_reason": "建立第一次瓶颈循环",
        },
    )
    assert complete.status_code == 200, complete.text
    assert complete.json()["gate"]["passed"] is True
    assert complete.json()["prompt"] is not None
    assert "validated-opening" in complete.json()["prompt"]


def test_soft_warning_does_not_block_board_save_or_chapter_approval(
    project: tuple[BookLayout, Path, Path],
) -> None:
    _layout, book_root, _reference_root = project
    saved = save_story_board(book_root, "# Book Board\n\n## 0. 基本信息\n\n只有一句话。")
    assert saved["path"].endswith("BOOK_BOARD.md")
    result = save_chapter(
        book_root,
        chapter_number=1,
        title="灯亮了",
        chapter_markdown="# 第1章 灯亮了\n\n主角听见门外有人。",
    )
    assert result["canon_changed"] is False
    assert Path(result["path"]).name == "chapter-0001.md"
    with pytest.raises(ValueError, match="下一章应保存为第 2 章"):
        save_chapter(
            book_root,
            chapter_number=1,
            title="重复",
            chapter_markdown="重复正文",
        )


def test_review_prompt_is_proposal_only_and_clipboard_uses_visible_textarea(
    project: tuple[BookLayout, Path, Path],
) -> None:
    _layout, book_root, _reference_root = project
    save_story_board(book_root, initial_board(title="标题", premise="创意"))
    before = read_board(prepare_paths(book_root))
    client = TestClient(_app(project))
    response = client.post(
        f"/api/books/{BOOK_ID}/story-program/prompt",
        headers=_headers(client),
        json={
            "mode": "review",
            "board_markdown": before,
            "actual_summaries": "第1—10章完成了局部资源循环。",
            "program_ids": [],
        },
    )
    assert response.status_code == 200
    assert response.json()["prompt"] is not None
    assert read_board(prepare_paths(book_root)) == before
    script = Path("src/novel_authoring/web/static/story_program.js").read_text(
        encoding="utf-8"
    )
    assert "navigator.clipboard.writeText(output.value)" in script


def test_concrete_plan_gate_reports_only_required_fields() -> None:
    result = concrete_plan_gate("主角遇到危机。\n叙事功能：建立压力。")
    assert result.passed is False
    assert result.missing == (
        "具体触发事件",
        "推动事件的人",
        "主角行动",
        "对手或世界反应",
        "直接结果",
        "状态变化",
        "结尾推动力",
    )
