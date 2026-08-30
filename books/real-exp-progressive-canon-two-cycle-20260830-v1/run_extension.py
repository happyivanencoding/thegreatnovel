from __future__ import annotations

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(EXP))

import run_experiment as r
from story_mvp.progressive_canon import (
    advance_after_reveal,
    compile_runtime_mystery_projection,
    parse_reveal_contract,
    render_thread,
)
from story_mvp.storage import compose_book_content, parse_book_sections


def adopt_outline(outline_text: str, current_book: str) -> str:
    sections = parse_book_sections(outline_text)
    sections["status"] = parse_book_sections(current_book)["status"]
    return compose_book_content(sections)


def require_pass(text: str, label: str) -> None:
    if not re.search(r"(?mi)^Verdict:\s*PASS\s*$", text):
        raise RuntimeError(f"{label} did not PASS")


def reframe_and_compile_v2(directory: Path, label: str, thread, surface_text: str, planning_need: str, context: str, selected_id: str):
    rp = r.build_reframe_prompt(thread=thread, decision_surface=surface_text, current_context=context)
    rr = r.run_acp(rp, directory, f"{label}_REFRAME", model="gpt-5.6-luna", effort="high")
    candidates = r.extract_reframe_candidates(rr["text"])
    selected = candidates[selected_id]
    (directory / f"{label}_SELECTED_{selected_id}.md").write_text(selected + "\n", encoding="utf-8")
    cp = r.build_canonization_compiler_prompt(
        thread=thread,
        selected_candidate=selected,
        current_context=context,
        decision_surface=surface_text,
        planning_need=planning_need,
    )
    cr = r.run_acp(cp, directory, f"{label}_COMPILER_V2", model="gpt-5.6-terra", effort="high")
    verdict = r.parse_compiler_verdict(cr["text"])
    if verdict != "PASS":
        raise RuntimeError(f"{label} compiler V2={verdict}; preregistered candidate not replaced")
    fixed = r.adopt_hidden_fixed_point(thread=thread, selected_candidate=selected, compiler_report=cr["text"])
    (directory / f"{label}_FIXED_V2.md").write_text(render_thread(fixed), encoding="utf-8")
    return fixed, selected, {"reframe": rr, "compiler": cr}


def assert_no_exact_hidden(prompts: dict[str, str], fixed_point: str, label: str) -> None:
    for node, prompt in prompts.items():
        if node == "state":
            continue
        if fixed_point.strip() and fixed_point.strip() in prompt:
            raise RuntimeError(f"{label}: raw Fixed Point leaked into {node} prompt")


def main() -> None:
    summary: dict[str, object] = {
        "extension_preregistered": True,
        "decision_after_correct_ch1": "DEFER",
        "critical1_expected": "DECISION NEEDED",
        "cycle1_selected": "R2",
        "reveal1_chapter": 3,
        "critical2_expected": "DECISION NEEDED",
        "cycle2_selected": "R3",
        "reveal2_chapter": 4,
        "final_expected": "DEFER",
    }

    open_story = (EXP / "open_phase" / "STORY_REFRESH_OPEN.md").read_text(encoding="utf-8")
    open_outline = (EXP / "open_phase" / "OUTLINE_OPEN.md").read_text(encoding="utf-8")
    initial_book = r.make_base_book()
    book = adopt_outline(open_outline, initial_book)

    # Corrected Chapter 1 only: grab/hold the second key, no source answer.
    ch1 = r.chapter_chain(
        chapter=1,
        runtime_book=book,
        outline_book=open_outline,
        char=r.CHAR_A,
        previous_prose="",
        directory=EXP / "chapter1_v2",
    )
    audit1 = r.run_acp(
        r.boundary_audit_prompt(
            mode="open",
            thread=r.INITIAL_THREAD,
            reveal=None,
            prompts=ch1["prompts"],
            prose=ch1["prose"],
            state_text=(EXP / "chapter1_v2" / "STATE_DELTA.md").read_text(encoding="utf-8"),
        ),
        EXP / "chapter1_v2",
        "OPEN_BOUNDARY_AUDIT",
        model="gpt-5.6-terra",
        effort="high",
    )
    require_pass(audit1["text"], "corrected chapter1 open boundary")
    book = ch1["book"]

    # The corrected early checkpoint should still defer.
    d_after_ch1 = r.decision(
        EXP / "extension" / "decision_after_ch1",
        "DECISION_AFTER_CH1",
        r.INITIAL_THREAD,
        "第一章只确认陆昭已经抢到并持有回影井吐出的第二枚同编号钥牌；下一步仍可以先做价格、公开比对、夺物与持有冲突，不需要知道来源。",
        r.state_context(book),
        "DEFER",
    )
    summary["decision_after_correct_ch1_actual"] = d_after_ch1["status"]

    # Author-selected critical direction: physical traversal in Ch3 requires minimum destination category.
    critical1_need = """作者现在明确决定下一小段的阅读目标：第3章陆昭必须亲自穿过“两枚钥牌共同打开的异常通道”，并在另一侧真实行动至少一个完整场景；另一侧必须有具体环境、人物/物件和能留下长期后果的现实，不允许用模糊黑暗、幻觉、梦境或只看一眼来规避。要让第3章的环境、可触碰对象、能否带回东西和当地人的反应成为可执行事实，当前至少必须决定“另一侧属于什么最低现实类别”；不要求解释为什么存在、谁造成、哥哥终局或全宇宙结构。"""
    d1 = r.decision(
        EXP / "extension" / "cycle1",
        "CRITICAL_DECISION1",
        r.INITIAL_THREAD,
        critical1_need,
        r.state_context(book),
        "DECISION NEEDED",
    )
    fixed1, selected1, _ = reframe_and_compile_v2(
        EXP / "extension" / "cycle1",
        "CYCLE1",
        r.INITIAL_THREAD,
        d1["text"],
        critical1_need,
        r.state_context(book),
        "R2",
    )
    summary["critical1_actual"] = d1["status"]
    (EXP / "extension" / "cycle1" / "FIXED1.md").write_text(render_thread(fixed1), encoding="utf-8")

    # Same Fixed Point under two Humans.
    pair = r.story_pair_for_humans(
        book=book,
        fixed=fixed1,
        previous_story=open_story,
        reveal_chapter=3,
        chapter=1,
        directory=EXP / "extension" / "cycle1" / "human_pair",
    )
    story_a = pair["A"]["run"]["text"]
    story_b = pair["B"]["run"]["text"]
    h_audit = r.run_acp(
        r.human_invariance_prompt(fixed=fixed1, story_a=story_a, story_b=story_b),
        EXP / "extension" / "cycle1",
        "HUMAN_INVARIANCE_AUDIT",
        model="gpt-5.6-terra",
        effort="high",
    )
    require_pass(h_audit["text"], "human invariance")
    summary["human_invariance"] = "PASS"

    reveal1 = parse_reveal_contract(story_a)
    if reveal1.reveal_chapter != 3 or reveal1.mystery_id != fixed1.mystery_id:
        raise RuntimeError("Reveal1 violates preregistration")
    safe_story_a = r.strip_reveal_contract(story_a)
    if fixed1.fixed_point.strip() in safe_story_a:
        raise RuntimeError("Story Refresh leaked raw Fixed Point outside reveal contract")
    (EXP / "extension" / "cycle1" / "REVEAL1.json").write_text(
        json.dumps(reveal1.__dict__, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Outline only gets stripped story + answer-free scheduling marker.
    current1 = r.current_character(book, r.CHAR_A, 1)
    o1 = r.run_acp(
        r.outline_prompt(
            book=book,
            char=r.CHAR_A,
            current=current1,
            story=story_a,
            reveal_id=reveal1.mystery_id,
            reveal_chapter=3,
        ),
        EXP / "extension" / "cycle1",
        "OUTLINE1_V2",
        model="gpt-5.6-luna",
        effort="high",
    )
    book = adopt_outline(o1["text"], book)
    ch2_plan = r.extract_chapter_plan(o1["text"], 2)
    marker1 = f"[MYSTERY-REVEAL:{reveal1.mystery_id}]"
    if marker1 in ch2_plan or reveal1.state_residue in ch2_plan:
        raise RuntimeError("Outline leaked Reveal1 into pre-reveal Chapter2")

    # Chapter 2: full production chain; no hidden truth.
    ch2 = r.chapter_chain(
        chapter=2,
        runtime_book=book,
        outline_book=o1["text"],
        char=r.CHAR_A,
        previous_prose=ch1["prose"],
        directory=EXP / "extension" / "chapter2",
    )
    assert_no_exact_hidden(ch2["prompts"], fixed1.fixed_point, "chapter2")
    pre_projection = compile_runtime_mystery_projection(fixed1, reveal1, chapter_number=2)
    (EXP / "extension" / "chapter2" / "MYSTERY_RUNTIME_PROJECTION.md").write_text(pre_projection + "\n", encoding="utf-8")
    pre_audit = r.run_acp(
        r.boundary_audit_prompt(
            mode="pre",
            thread=fixed1,
            reveal=reveal1,
            prompts=ch2["prompts"],
            prose=ch2["prose"],
            state_text=(EXP / "extension" / "chapter2" / "STATE_DELTA.md").read_text(encoding="utf-8"),
        ),
        EXP / "extension" / "chapter2",
        "PRE_REVEAL1_AUDIT",
        model="gpt-5.6-terra",
        effort="high",
    )
    require_pass(pre_audit["text"], "pre reveal1")
    summary["pre_reveal1"] = "PASS"
    book = ch2["book"]

    # Chapter 3: only now inject reader-facing reveal event.
    book = adopt_outline(o1["text"], book)
    ch3 = r.chapter_chain(
        chapter=3,
        runtime_book=book,
        outline_book=o1["text"],
        char=r.CHAR_A,
        previous_prose=ch2["prose"],
        reveal=reveal1,
        directory=EXP / "extension" / "chapter3",
    )
    if fixed1.fixed_point.strip() in ch3["prompts"]["primary"]:
        raise RuntimeError("Reveal chapter got raw Hidden Fixed Point instead of event transport")
    reveal_projection = compile_runtime_mystery_projection(fixed1, reveal1, chapter_number=3)
    (EXP / "extension" / "chapter3" / "MYSTERY_RUNTIME_PROJECTION.md").write_text(reveal_projection + "\n", encoding="utf-8")
    reveal_audit1 = r.run_acp(
        r.boundary_audit_prompt(
            mode="reveal",
            thread=fixed1,
            reveal=reveal1,
            prompts=ch3["prompts"],
            prose=ch3["prose"],
            state_text=(EXP / "extension" / "chapter3" / "STATE_DELTA.md").read_text(encoding="utf-8"),
        ),
        EXP / "extension" / "chapter3",
        "REVEAL1_AUDIT",
        model="gpt-5.6-terra",
        effort="high",
    )
    require_pass(reveal_audit1["text"], "reveal1")
    summary["reveal1"] = "PASS"
    book = ch3["book"]

    # First layer is now Canon; reopen deeper mystery.
    open2 = advance_after_reveal(
        fixed1,
        reveal1,
        next_decision_trigger="只有下一段双向跨越/取物的结果必须依赖两处现实之间的关系时，才决定这一层；其它来源仍未知。",
    )
    (EXP / "extension" / "cycle2" / "OPEN2.md").parent.mkdir(parents=True, exist_ok=True)
    (EXP / "extension" / "cycle2" / "OPEN2.md").write_text(render_thread(open2), encoding="utf-8")

    critical2_need = """第3章已经把第一层 Reveal 写进 Canon。作者现在明确决定第4章要让陆昭利用两处现实之间的联系完成一次双向行动：从另一侧取回一个会在听雨城继续造成现实争夺的东西，并能够返回；该行动的可行性、同一物件能否两边同时存在、哪边的变化会不会影响另一边，都取决于“两处现实最低是什么关系”。现在只决定这一层关系；不解释为什么会产生、谁制造、哥哥最终在哪、是否还有第三处或更高层。"""
    d2 = r.decision(
        EXP / "extension" / "cycle2",
        "CRITICAL_DECISION2",
        open2,
        critical2_need,
        r.state_context(book),
        "DECISION NEEDED",
    )
    fixed2, selected2, _ = reframe_and_compile_v2(
        EXP / "extension" / "cycle2",
        "CYCLE2",
        open2,
        d2["text"],
        critical2_need,
        r.state_context(book),
        "R3",
    )
    summary["critical2_actual"] = d2["status"]

    current3 = r.current_character(book, r.CHAR_A, 3)
    sr2 = r.run_acp(
        r.story_refresh_prompt(
            book=book,
            char=r.CHAR_A,
            current=current3,
            previous_story=safe_story_a,
            thread=fixed2,
            reveal_chapter=4,
        ),
        EXP / "extension" / "cycle2",
        "STORY_REFRESH2",
        model="gpt-5.6-sol",
        effort="high",
    )
    reveal2 = parse_reveal_contract(sr2["text"])
    if reveal2.reveal_chapter != 4 or reveal2.mystery_id != fixed2.mystery_id:
        raise RuntimeError("Reveal2 violates preregistration")
    safe_story2 = r.strip_reveal_contract(sr2["text"])
    if fixed2.fixed_point.strip() in safe_story2:
        raise RuntimeError("Story Refresh2 leaked raw Fixed Point outside reveal contract")
    (EXP / "extension" / "cycle2" / "REVEAL2.json").write_text(
        json.dumps(reveal2.__dict__, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    o2 = r.run_acp(
        r.outline_prompt(
            book=book,
            char=r.CHAR_A,
            current=current3,
            story=sr2["text"],
            reveal_id=reveal2.mystery_id,
            reveal_chapter=4,
        ),
        EXP / "extension" / "cycle2",
        "OUTLINE2_V2",
        model="gpt-5.6-luna",
        effort="high",
    )
    book = adopt_outline(o2["text"], book)

    # Chapter 4: second bounded reveal.
    ch4 = r.chapter_chain(
        chapter=4,
        runtime_book=book,
        outline_book=o2["text"],
        char=r.CHAR_A,
        previous_prose=ch3["prose"],
        reveal=reveal2,
        directory=EXP / "extension" / "chapter4",
    )
    if fixed2.fixed_point.strip() in ch4["prompts"]["primary"]:
        raise RuntimeError("Reveal2 chapter got raw Hidden Fixed Point")
    reveal_audit2 = r.run_acp(
        r.boundary_audit_prompt(
            mode="reveal",
            thread=fixed2,
            reveal=reveal2,
            prompts=ch4["prompts"],
            prose=ch4["prose"],
            state_text=(EXP / "extension" / "chapter4" / "STATE_DELTA.md").read_text(encoding="utf-8"),
        ),
        EXP / "extension" / "chapter4",
        "REVEAL2_AUDIT",
        model="gpt-5.6-terra",
        effort="high",
    )
    require_pass(reveal_audit2["text"], "reveal2")
    summary["reveal2"] = "PASS"
    book = ch4["book"]

    # After two partial truths, the story should again be free to postpone ultimate explanation.
    open3 = advance_after_reveal(
        fixed2,
        reveal2,
        next_decision_trigger="只有新阶段真的依赖更深来源时才继续定真。",
    )
    (EXP / "extension" / "OPEN3.md").write_text(render_thread(open3), encoding="utf-8")
    d3 = r.decision(
        EXP / "extension" / "final",
        "FINAL_DECISION",
        open3,
        "下一阶段先处理第4章带回之物造成的抢夺、兵坊/城主府重新定价、陆昭的收益选择与家人风险；这些后果都可以在不解释终极来源、幕后创造者或哥哥终局的情况下成立。",
        r.state_context(book),
        "DEFER",
    )
    summary["final_actual"] = d3["status"]
    summary["final_defer"] = "PASS"
    summary["production_modified"] = False
    summary["current_user_novel_modified"] = False

    (EXP / "extension" / "FINAL_BOOK.md").write_text(book, encoding="utf-8")
    r.dump(EXP / "EXTENSION_RUN_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
