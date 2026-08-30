from __future__ import annotations

import pytest

from story_mvp.progressive_canon import (
    MysteryThread,
    adopt_hidden_fixed_point,
    build_canonization_compiler_prompt,
    build_decision_surface_prompt,
    build_reframe_prompt,
    extract_reframe_candidates,
    parse_compiler_verdict,
    parse_decision_surface,
    render_planning_projection,
    render_thread,
)


def open_thread() -> MysteryThread:
    return MysteryThread(
        mystery_id="M-01",
        question="谁把故乡变成了副本？",
        state="OPEN",
        known_anchors="故乡被界签标记为第一副本；主角确实在这里长大。",
        decision_trigger="只有下一阶段必须定义副本来源时才决定。",
        remains_unknown="玩家来自哪里；副本是谁建立；主角为何能离开。",
    )


def candidate(route: str = "world") -> str:
    return f"""## R2｜局部定真
### New Fixed Point
副本居民拥有连续真实人生；“NPC”至少不是“没有真实经历的人”的同义词。
### What Remains Unknown
谁建立副本；玩家本体是什么；主角为何能离开。
### Backward Compatibility
不否定主角童年、家人和已发生损失。
### New Story Doors
主角可遇见把居民当脚本的跨界者，并发现其判断并不可靠。
### Reveal Boundary
作者现在知道，但人物与读者暂时只获得间接证据。
### Authority Route
{route}
"""


def reframe_text() -> str:
    base = candidate("world")
    r1 = base.replace("## R2｜局部定真", "## R1｜局部定真一")
    r2 = base
    r3 = base.replace("## R2｜局部定真", "## R3｜局部定真三").replace("world\n", "story\n")
    d0 = """## D0｜继续未知
### No New Truth
NONE
### Safe Deferred Route
先进入一个完全独立的新副本，只确认跨副本行为者存在，不解释其本体。
### What Remains Unknown
全部 Meta 来源问题继续开放。
"""
    return "# MYSTERY REFRAME CANDIDATES\n" + r1 + r2 + r3 + d0


def test_open_thread_has_no_hidden_truth() -> None:
    rendered = render_thread(open_thread())
    assert "Author State: OPEN" in rendered
    assert "Author Fixed Hidden Truth" not in rendered


def test_open_thread_rejects_prefilled_answer() -> None:
    thread = MysteryThread(
        mystery_id="M-01",
        question="Q",
        state="OPEN",
        known_anchors="A",
        decision_trigger="T",
        fixed_point="secret",
    )
    with pytest.raises(ValueError, match="OPEN Mystery"):
        render_thread(thread)


def test_fixed_hidden_requires_fixed_point() -> None:
    thread = MysteryThread(
        mystery_id="M-01",
        question="Q",
        state="FIXED_HIDDEN",
        known_anchors="A",
        decision_trigger="T",
    )
    with pytest.raises(ValueError, match="fixed_point"):
        render_thread(thread)


def test_decision_surface_parser() -> None:
    assert parse_decision_surface("Status: DEFER") == "DEFER"
    assert parse_decision_surface("Status: DECISION NEEDED") == "DECISION NEEDED"
    with pytest.raises(ValueError):
        parse_decision_surface("Status: MAYBE")


def test_reframe_can_only_start_after_decision_needed() -> None:
    with pytest.raises(ValueError, match="DECISION NEEDED"):
        build_reframe_prompt(
            thread=open_thread(),
            decision_surface="Status: DEFER",
            current_context="ctx",
        )


def test_reframe_exact_candidates_and_defer() -> None:
    result = extract_reframe_candidates(reframe_text())
    assert tuple(result) == ("R1", "R2", "R3", "D0")


def test_reframe_rejects_invalid_route() -> None:
    bad = reframe_text().replace("### Authority Route\nworld", "### Authority Route\nhuman", 1)
    with pytest.raises(ValueError, match="Authority Route"):
        extract_reframe_candidates(bad)


def test_defer_must_add_no_truth() -> None:
    bad = reframe_text().replace("### No New Truth\nNONE", "### No New Truth\n新增真相")
    with pytest.raises(ValueError, match="No New Truth"):
        extract_reframe_candidates(bad)


def test_compiler_prompt_is_non_scoring_and_hidden() -> None:
    prompt = build_canonization_compiler_prompt(
        thread=open_thread(), selected_candidate=candidate(), current_context="existing canon"
    )
    assert "不评价它酷不酷" in prompt
    assert "Author Fixed Hidden Truth" in prompt
    assert "不直接注入章节 Writer" in prompt


def test_compiler_verdict_is_strict() -> None:
    assert parse_compiler_verdict("Verdict: PASS") == "PASS"
    assert parse_compiler_verdict("Verdict: FAIL") == "FAIL"
    with pytest.raises(ValueError):
        parse_compiler_verdict("Verdict: CONDITIONAL PASS")


def test_adopt_hidden_fixed_point_only_after_pass() -> None:
    adopted = adopt_hidden_fixed_point(
        thread=open_thread(),
        selected_candidate=candidate(),
        compiler_report="Verdict: PASS",
    )
    assert adopted.state == "FIXED_HIDDEN"
    assert adopted.route == "world"
    assert "NPC" in adopted.fixed_point
    assert "作者现在知道" in adopted.reveal_boundary
    with pytest.raises(ValueError, match="未 PASS"):
        adopt_hidden_fixed_point(
            thread=open_thread(),
            selected_candidate=candidate(),
            compiler_report="Verdict: FAIL",
        )


def test_open_projection_explicitly_forbids_answering() -> None:
    projection = render_planning_projection(open_thread())
    assert "AUTHOR OPEN" in projection
    assert "不得把任何答案升级成事实" in projection


def test_fixed_projection_is_planning_only() -> None:
    fixed = adopt_hidden_fixed_point(
        thread=open_thread(),
        selected_candidate=candidate("story"),
        compiler_report="Verdict: PASS",
    )
    projection = render_planning_projection(fixed)
    assert "AUTHOR FIXED HIDDEN" in projection
    assert "只供 World/Story 规划层" in projection
    assert "章节 Writer" in projection


def test_decision_prompt_never_requests_answer() -> None:
    prompt = build_decision_surface_prompt(
        thread=open_thread(),
        planning_need="进入第二副本",
        current_context="第一副本已完成",
    )
    assert "不提出答案" in prompt
    assert "DEFER" in prompt


def test_fixed_hidden_requires_reveal_boundary() -> None:
    thread = MysteryThread(
        mystery_id="M-02",
        question="Q",
        state="FIXED_HIDDEN",
        known_anchors="A",
        decision_trigger="T",
        fixed_point="hidden truth",
    )
    with pytest.raises(ValueError, match="reveal_boundary"):
        render_thread(thread)


def test_open_thread_rejects_reveal_boundary() -> None:
    thread = MysteryThread(
        mystery_id="M-03",
        question="Q",
        state="OPEN",
        known_anchors="A",
        decision_trigger="T",
        reveal_boundary="should not exist yet",
    )
    with pytest.raises(ValueError, match="OPEN Mystery"):
        render_thread(thread)
