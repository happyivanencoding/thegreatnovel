from __future__ import annotations

import pytest

from story_mvp.progressive_canon import (
    MysteryRevealContract,
    MysteryThread,
    advance_after_reveal,
    adopt_hidden_fixed_point,
    build_canonization_compiler_prompt,
    build_decision_surface_prompt,
    build_reframe_prompt,
    compile_runtime_mystery_projection,
    extract_reframe_candidates,
    parse_compiler_verdict,
    parse_decision_surface,
    parse_reveal_contract,
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


def fixed_thread_for_runtime() -> MysteryThread:
    return MysteryThread(
        mystery_id="M-RUNTIME-01",
        question="井中遗物到底来自哪里？",
        state="FIXED_HIDDEN",
        known_anchors="井里确实出现过活人的旧物。",
        decision_trigger="进入源头前必须决定最小来源类别。",
        fixed_point="秘密答案原句：遗物来自第二座实体城市。",
        remains_unknown="第二座城市为什么存在；两座城谁是原本。",
        reveal_boundary="本阶段只允许确认存在第二座实体城市。",
        route="story",
    )


def reveal_contract_for_runtime() -> MysteryRevealContract:
    return MysteryRevealContract(
        mystery_id="M-RUNTIME-01",
        reveal_chapter=3,
        event_atom="井壁打开一道短暂视野，众人亲眼看见一座与本城街形一致、却有不同毁损的真实城市。",
        state_residue="已确认井中遗物来自另一座真实存在的城市层；不是幻象或纯预言。",
        reader_anchors=("井壁", "另一座城"),
        still_open_after_reveal="另一座城为何存在；两座城是什么关系；是否还有更多城市层。",
    )


def test_parse_reveal_contract_is_strict() -> None:
    parsed = parse_reveal_contract(
        """# MYSTERY REVEAL CONTRACT
Mystery ID: M-RUNTIME-01
Reveal Chapter: 3
Event Atom: 井壁短暂打开，能看到另一座城。
State Residue: 已确认另一座真实城市层存在。
Reader Anchors: 井壁；另一座城
Still Open After Reveal: 两座城为什么存在。
"""
    )
    assert parsed.reveal_chapter == 3
    assert parsed.reader_anchors == ("井壁", "另一座城")
    with pytest.raises(ValueError, match="缺少字段"):
        parse_reveal_contract("Mystery ID: M-RUNTIME-01\nReveal Chapter: 3")


def test_pre_reveal_runtime_projection_cannot_see_hidden_fixed_point() -> None:
    thread = fixed_thread_for_runtime()
    projection = compile_runtime_mystery_projection(
        thread, reveal_contract_for_runtime(), chapter_number=2
    )
    assert "秘密答案原句" not in projection
    assert thread.fixed_point not in projection
    assert "MYSTERY UNRESOLVED FACT BOUNDARY" in projection
    assert "不得补答案" in projection


def test_reveal_chapter_gets_event_not_raw_hidden_truth() -> None:
    thread = fixed_thread_for_runtime()
    reveal = reveal_contract_for_runtime()
    projection = compile_runtime_mystery_projection(thread, reveal, chapter_number=3)
    assert "MYSTERY REVEAL EVENT" in projection
    assert reveal.event_atom in projection
    assert thread.fixed_point not in projection
    assert "秘密答案原句" not in projection
    assert reveal.still_open_after_reveal in projection


def test_post_reveal_runtime_projection_is_empty() -> None:
    projection = compile_runtime_mystery_projection(
        fixed_thread_for_runtime(), reveal_contract_for_runtime(), chapter_number=4
    )
    assert projection == ""


def test_advance_after_reveal_reopens_deeper_question_without_hidden_payload() -> None:
    reveal = reveal_contract_for_runtime()
    next_thread = advance_after_reveal(
        fixed_thread_for_runtime(),
        reveal,
        next_decision_trigger="要决定两座城关系才能安全跨城行动。",
    )
    assert next_thread.state == "OPEN"
    assert next_thread.fixed_point == ""
    assert next_thread.reveal_boundary == ""
    assert reveal.state_residue in next_thread.known_anchors
    assert next_thread.question == reveal.still_open_after_reveal
    assert "秘密答案原句" not in render_thread(next_thread)


def test_compiler_v2_distinguishes_old_open_pool_from_new_protected_unknowns() -> None:
    prompt = build_canonization_compiler_prompt(
        thread=open_thread(),
        selected_candidate=candidate(),
        current_context="第一章只确认异常物存在。",
        decision_surface="Status: DECISION NEEDED\nSmallest Decision: 另一侧最低属于什么现实类别？",
        planning_need="第3章作者明确要让主角穿过未来才打开的通道。",
    )
    assert "决策前的未决定池" in prompt
    assert "AUTHOR-APPROVED FUTURE DIRECTION" in prompt
    assert "第3章作者明确要让主角穿过未来才打开的通道" in prompt
    assert "Smallest Decision" in prompt
