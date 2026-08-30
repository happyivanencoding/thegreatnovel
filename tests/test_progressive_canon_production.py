from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.progressive_canon import MysteryThread
from story_mvp.storage import (
    advance_mystery_after_reveal,
    create_book,
    get_mystery_thread,
    inject_mystery_reveals_into_chapter_plan,
    read_creative_payload,
    read_mystery_control,
    render_mystery_outline_schedule,
    render_mystery_planning_context,
    save_mystery_thread,
    write_creative_artifact,
)


FIXED = MysteryThread(
    mystery_id="M-01",
    question="井后到底是什么？",
    state="FIXED_HIDDEN",
    known_anchors="第1章只确认井会吐出异常旧物。",
    decision_trigger="作者明确要让主角跨过去时，才决定最小现实类别。",
    fixed_point="后台答案：另一侧是同一现实中的异常实体夹层。",
    remains_unknown="夹层为何存在；钥牌来源；哥哥是否进入。",
    reveal_boundary="本轮只允许确认活人可以进入、返回，并带回持续物理后果。",
    route="story",
)

REVEAL_RESPONSE = """# STORY PROGRAM

## 当前 Re-Collision
继续写钥牌争夺。

# MYSTERY REVEAL CONTRACT
Mystery ID: M-01
Reveal Chapter: 3
Event Atom: 陆昭踏入石道取回短刀，回到雨里以后刀面水痕仍逆向流动。
State Residue: 已确认活人可以进入石道并返回，携入物能带回持续物理异常。
Reader Anchors: 石道；黑柄短刀；逆流水痕
Still Open After Reveal: 石道为何存在；钥牌来源；哥哥是否进入。
"""

PLAN = """## 第3章：进井
具体剧情：陆昭带钥牌回到井边。
结果 / 状态变化：钥牌仍归陆昭。
叙事功能：推进井线。
结尾推动：兵坊闻讯赶来。
"""

CANDIDATE = """## R2｜局部定真
### New Fixed Point
另一侧是一处可进入并返回的异常实体空间。
### What Remains Unknown
空间为何存在；钥牌来源；哥哥是否进入。
### Backward Compatibility
不否定已经发生的吐物与持有事实。
### New Story Doors
作者可以安排一次真实穿越与带回物。
### Reveal Boundary
本轮只允许确认能进入、返回并留下持续后果。
### Authority Route
story
"""


def mark_book_completed(workspace: Path, book_id: str, chapter: int) -> None:
    path = workspace / book_id / "BOOK.md"
    text = path.read_text(encoding="utf-8")
    heading = "# 当前状态、未兑现承诺与作者备注"
    assert heading in text
    text = text.replace(heading, heading + f"\n\n当前已完成第{chapter}章。", 1)
    path.write_text(text, encoding="utf-8")


def test_new_book_initializes_runtime_blind_mystery_control(tmp_path: Path) -> None:
    create_book("mystery", tmp_path)
    control = read_mystery_control("mystery", tmp_path)
    assert control == {"threads": {}, "reveals": {}, "compiler_inputs": {}}
    payload = read_creative_payload("mystery", tmp_path)
    assert payload["mystery_control"] == control


def test_fixed_hidden_story_planning_is_separate_from_outline_and_runtime(tmp_path: Path) -> None:
    create_book("mystery", tmp_path)
    save_mystery_thread("mystery", FIXED, tmp_path)

    planning = render_mystery_planning_context("mystery", tmp_path, route="story")
    assert "AUTHOR FIXED HIDDEN" in planning
    assert FIXED.fixed_point in planning
    assert render_mystery_outline_schedule("mystery", tmp_path) == ""

    unchanged = inject_mystery_reveals_into_chapter_plan("mystery", 2, PLAN, tmp_path)
    assert unchanged == PLAN


def test_story_program_save_extracts_reveal_and_keeps_outline_answer_free(tmp_path: Path) -> None:
    create_book("mystery", tmp_path)
    save_mystery_thread("mystery", FIXED, tmp_path)

    write_creative_artifact("mystery", "proposal", REVEAL_RESPONSE, tmp_path)
    payload = read_creative_payload("mystery", tmp_path)
    assert "# MYSTERY REVEAL CONTRACT" not in payload["proposal"]
    assert FIXED.fixed_point not in payload["proposal"]

    control = read_mystery_control("mystery", tmp_path)
    reveal = control["reveals"]["M-01"]
    assert reveal["reveal_chapter"] == 3
    assert "逆向流动" in reveal["event_atom"]

    schedule = render_mystery_outline_schedule("mystery", tmp_path)
    assert "第3章" in schedule
    assert "[MYSTERY-REVEAL:M-01]" in schedule
    assert "逆向流动" not in schedule
    assert FIXED.fixed_point not in schedule


def test_reveal_runtime_gets_event_not_hidden_truth_and_advance_reopens(tmp_path: Path) -> None:
    create_book("mystery", tmp_path)
    save_mystery_thread("mystery", FIXED, tmp_path)
    write_creative_artifact("mystery", "proposal", REVEAL_RESPONSE, tmp_path)

    pre = inject_mystery_reveals_into_chapter_plan("mystery", 2, PLAN, tmp_path)
    assert pre == PLAN
    reveal_plan = inject_mystery_reveals_into_chapter_plan("mystery", 3, PLAN, tmp_path)
    assert "陆昭踏入石道取回短刀" in reveal_plan
    assert "已确认活人可以进入石道并返回" in reveal_plan
    assert "[MYSTERY-REVEAL:M-01]" in reveal_plan
    assert FIXED.fixed_point not in reveal_plan

    with pytest.raises(ValueError, match="尚未完成并进入 State"):
        advance_mystery_after_reveal(
            "mystery",
            "M-01",
            next_decision_trigger="下一次故事动作真正依赖两侧关系时再定真。",
            workspace=tmp_path,
        )
    mark_book_completed(tmp_path, "mystery", 3)
    advanced = advance_mystery_after_reveal(
        "mystery",
        "M-01",
        next_decision_trigger="下一次故事动作真正依赖两侧关系时再定真。",
        workspace=tmp_path,
    )
    assert advanced["reveals"] == {}
    thread = get_mystery_thread("mystery", "M-01", tmp_path)
    assert thread.state == "OPEN"
    assert thread.fixed_point == ""
    assert "已确认活人可以进入石道并返回" in thread.known_anchors
    assert "石道为何存在" in thread.question


def test_story_program_reveal_batch_is_all_or_nothing(tmp_path: Path) -> None:
    create_book("mystery-batch", tmp_path)
    save_mystery_thread("mystery-batch", FIXED, tmp_path)
    invalid_second = REVEAL_RESPONSE + """

# MYSTERY REVEAL CONTRACT
Mystery ID: M-NOT-REGISTERED
Reveal Chapter: 4
Event Atom: 第二个事件。
State Residue: 第二个状态。
Reader Anchors: X
Still Open After Reveal: Y
"""
    with pytest.raises(ValueError, match="M-NOT-REGISTERED"):
        write_creative_artifact("mystery-batch", "proposal", invalid_second, tmp_path)
    control = read_mystery_control("mystery-batch", tmp_path)
    assert control["reveals"] == {}
    assert read_creative_payload("mystery-batch", tmp_path)["proposal"] == ""


def test_split_planning_uses_hidden_truth_only_in_planning_lane() -> None:
    story_prompt = generate_split_prompt(
        mode="story_refresh",
        book_content="# 当前状态、未兑现承诺与作者备注\n\n当前状态：x",
        creative_direction="继续当前阶段",
        world_vision="### 精确力量主尺｜Frozen Grammar\n主尺类型：连续数字\n主尺名称：纹阶\n精确位置格式：纹阶{N}\n数字精度规则：1—36\n当前可见范围：1—36\n当前大档位：1—6普通；7—12骨干",
        current_character="Compiled Through Chapter: 1",
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
            "proposal": {"status": "author_approved"},
        },
        mystery_planning_context="Mystery M-01｜AUTHOR FIXED HIDDEN\nFixed Point: secret",
    )
    assert "AUTHOR MYSTERY CONTROL｜Planning Only" in story_prompt
    assert "Fixed Point: secret" in story_prompt
    assert "MYSTERY REVEAL CONTRACT" in story_prompt

    outline_prompt = generate_split_prompt(
        mode="outline",
        book_content="# 小说总体设计画像\n\nX",
        creative_direction="继续",
        world_vision="world",
        character_card="character",
        current_character="Compiled Through Chapter: 1",
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
            "proposal": {"status": "author_approved"},
        },
        proposal_context="# STORY PROGRAM\nclean",
        mystery_outline_schedule="- 第3章｜[MYSTERY-REVEAL:M-01]｜只排时机",
    )
    assert "[MYSTERY-REVEAL:M-01]" in outline_prompt
    assert "Fixed Point: secret" not in outline_prompt
    assert "不产生第二次批准点" in outline_prompt


def test_mystery_api_exposes_author_control_without_writing_answer_into_book(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "mystery-api"}).status_code == 201
    before = (tmp_path / "mystery-api" / "BOOK.md").read_text(encoding="utf-8")

    saved = client.put(
        "/api/books/mystery-api/mysteries/M-OPEN",
        json={
            "question": "玩家到底是什么？",
            "state": "OPEN",
            "known_anchors": "故乡已经被确认为一个副本。",
            "decision_trigger": "只有下一段故事必须依赖玩家本体时再决定。",
            "remains_unknown": "玩家来源；NPC 本体；系统来源。",
            "route": "story",
        },
    )
    assert saved.status_code == 200
    control = client.get("/api/books/mystery-api/mysteries")
    assert control.status_code == 200
    assert control.json()["threads"]["M-OPEN"]["state"] == "OPEN"

    decision = client.post(
        "/api/books/mystery-api/mysteries/decision-prompt",
        json={
            "mystery_id": "M-OPEN",
            "planning_need": "进入第二个副本；当前不需要知道玩家本体。",
        },
    )
    assert decision.status_code == 200
    assert "作者尚未决定不是缺陷" in decision.json()["prompt"]
    assert "DEFER" in decision.json()["prompt"]
    assert (tmp_path / "mystery-api" / "BOOK.md").read_text(encoding="utf-8") == before


def test_mystery_api_requires_compiled_exact_candidate_for_fixed_hidden(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "mystery-adopt"}).status_code == 201
    assert client.put(
        "/api/books/mystery-adopt/mysteries/M-01",
        json={
            "question": "井后是什么？",
            "state": "OPEN",
            "known_anchors": "井已经吐出异常旧物。",
            "decision_trigger": "只有下一事件必须穿过去时再定。",
            "remains_unknown": "井后类别；来源。",
            "route": "story",
        },
    ).status_code == 200

    direct_fixed = client.put(
        "/api/books/mystery-adopt/mysteries/M-01",
        json={
            "question": "井后是什么？",
            "state": "FIXED_HIDDEN",
            "known_anchors": "井已经吐出异常旧物。",
            "decision_trigger": "T",
            "fixed_point": "secret",
            "reveal_boundary": "reader-safe",
            "remains_unknown": "source",
            "route": "story",
        },
    )
    assert direct_fixed.status_code == 400
    assert "strict-PASS" in direct_fixed.json()["detail"]

    compiled = client.post(
        "/api/books/mystery-adopt/mysteries/compiler-prompt",
        json={
            "mystery_id": "M-01",
            "selected_candidate": CANDIDATE,
            "decision_surface": "Status: DECISION NEEDED\nSmallest Decision: 井后最低属于什么现实类别？",
            "planning_need": "第3章作者明确要让主角穿过去真实行动。",
        },
    )
    assert compiled.status_code == 200
    control = client.get("/api/books/mystery-adopt/mysteries").json()
    assert control["compiler_inputs"]["M-01"]["selected_candidate"] == CANDIDATE

    stale_candidate = client.post(
        "/api/books/mystery-adopt/mysteries/adopt",
        json={
            "mystery_id": "M-01",
            "selected_candidate": CANDIDATE.replace("异常实体空间", "另一种实体空间"),
            "compiler_report": "Verdict: PASS",
        },
    )
    assert stale_candidate.status_code == 400
    assert "Compiler Input 不一致" in stale_candidate.json()["detail"]

    adopted = client.post(
        "/api/books/mystery-adopt/mysteries/adopt",
        json={
            "mystery_id": "M-01",
            "selected_candidate": CANDIDATE,
            "compiler_report": "Verdict: PASS",
        },
    )
    assert adopted.status_code == 200
    assert adopted.json()["threads"]["M-01"]["state"] == "FIXED_HIDDEN"
    assert adopted.json()["compiler_inputs"] == {}

    overwrite_fixed = client.put(
        "/api/books/mystery-adopt/mysteries/M-01",
        json={
            "question": "想直接改回 OPEN",
            "state": "OPEN",
            "known_anchors": "A",
            "decision_trigger": "T",
            "remains_unknown": "U",
            "route": "story",
        },
    )
    assert overwrite_fixed.status_code == 400
    assert "不能由普通 PUT 覆盖" in overwrite_fixed.json()["detail"]


def test_mystery_adopt_rejects_compiler_snapshot_after_book_changes(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "mystery-stale-book"}).status_code == 201
    client.put(
        "/api/books/mystery-stale-book/mysteries/M-01",
        json={
            "question": "井后是什么？",
            "state": "OPEN",
            "known_anchors": "井已经吐出异常旧物。",
            "decision_trigger": "T",
            "remains_unknown": "来源。",
            "route": "story",
        },
    )
    compiled = client.post(
        "/api/books/mystery-stale-book/mysteries/compiler-prompt",
        json={
            "mystery_id": "M-01",
            "selected_candidate": CANDIDATE,
            "decision_surface": "Status: DECISION NEEDED\nSmallest Decision: 类别？",
            "planning_need": "下一章必须进入。",
        },
    )
    assert compiled.status_code == 200
    book_path = tmp_path / "mystery-stale-book" / "BOOK.md"
    book_path.write_text(book_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    stale = client.post(
        "/api/books/mystery-stale-book/mysteries/adopt",
        json={
            "mystery_id": "M-01",
            "selected_candidate": CANDIDATE,
            "compiler_report": "Verdict: PASS",
        },
    )
    assert stale.status_code == 400
    assert "BOOK / Canon 已变化" in stale.json()["detail"]
