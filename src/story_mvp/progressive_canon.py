from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


AuthorMysteryState = Literal["OPEN", "FIXED_HIDDEN"]
MysteryRoute = Literal["world", "story"]


@dataclass(frozen=True)
class MysteryThread:
    mystery_id: str
    question: str
    state: AuthorMysteryState
    known_anchors: str
    decision_trigger: str
    fixed_point: str = ""
    remains_unknown: str = ""
    reveal_boundary: str = ""
    route: MysteryRoute = "story"


@dataclass(frozen=True)
class MysteryRevealContract:
    mystery_id: str
    reveal_chapter: int
    event_atom: str
    state_residue: str
    reader_anchors: tuple[str, ...]
    still_open_after_reveal: str


DECISION_SURFACE_PROMPT = """你是 TGN 的 Mystery Decision Surface。你不是解谜 Agent，也不负责替作者补世界观。

任务只有一个：判断**接下来这个具体 Story Horizon 是否已经真的需要作者决定某个长期谜团的一小层答案**。

必须区分：
- Reader / Character Unknown：故事里的人或读者不知道；
- Author Open Mystery：作者自己也还没有决定答案；
- Author Fixed Hidden Truth：作者已经决定，但暂时还不让读者/人物知道。

规则：
- 作者尚未决定不是缺陷。只要下一段好故事仍可在不回答该谜团的情况下成立，就必须 `DEFER`。
- 不能因为“长篇最好有大纲”或“以后总要解释”而要求现在决定。
- 只有当前已批准方向真的会因缺少某一个事实而无法定义下一阶段的冲突、入口、人物选择或可执行世界事实时，才写 `DECISION NEEDED`。
- 即使需要决定，也只指出**最小必须定真的一层**；其它终极来源、幕后、结局继续未知。
- 不提出答案，不评分，不自动替作者选择。

严格输出：
# MYSTERY DECISION SURFACE
Status: DEFER / DECISION NEEDED
Smallest Decision: NONE 或一句当前必须决定的最小问题
Why Now: 2—5句
Can Remain Unknown: 1—5条仍可不决定的更深问题
Safe Next Move If Deferred: 若可继续未知，写一条具体可行的下一步；若当前路线确实必须决定，写 `CURRENT ROUTE BLOCKED`。
"""


REFRAME_FORGE_PROMPT = """你是 TGN 的 Non-Canon Mystery Reframe Forge。作者已经写了很长一段故事，现在只需要为一个长期谜团提出**三种局部定真方向**，不是替作者写完整终极答案。

三种候选必须：
- 都兼容已经发生的 Canon / Known Anchors；
- 每张只新增 1—2 个真正会改变后续故事的大方向事实；
- 明确写出“这次仍然不决定什么”；
- 允许以后出现更大的、向后兼容的重释；
- 产生不同的下一阶段故事门，而不是三种同义 lore；
- 不要求现在立刻在正文 Reveal。作者可以先知道，人物和读者以后再知道。
- 不把“解释得完整”当质量；不要补宇宙创造者、最终 Boss、终局历史，除非它就是本次 Smallest Decision 唯一不可避免的内容。

同时给一个 `D0｜继续未知`：不新增任何真相，只说明若作者拒绝现在定真，怎样改变当前路线继续写而不作弊。

严格格式：
# MYSTERY REFRAME CANDIDATES
## R1｜短标签
### New Fixed Point
### What Remains Unknown
### Backward Compatibility
### New Story Doors
### Reveal Boundary
### Authority Route
只能写 `world` 或 `story`。
## R2｜短标签
（同结构）
## R3｜短标签
（同结构）
## D0｜继续未知
### No New Truth
必须写 `NONE`。
### Safe Deferred Route
### What Remains Unknown
"""


CANONIZATION_COMPILER_PROMPT = """你是 TGN 的 Mystery Canonization Compiler。作者已经选中一张 Non-Canon Reframe 候选。你只检查这一个局部 Fixed Point 能否安全升级为**Author Fixed Hidden Truth**；不评价它酷不酷，也不替作者改稿或换候选。

检查：
1. 是否与已发生 Canon / Known Anchors 明确冲突；
2. 是否把过去明确为真的事实改成假的；允许重新解释旧事实，但不能重写旧事实；
3. `AUTHOR OPEN` 阶段旧的 Still Open 是**决策前的未决定池**，不是永远禁止回答的冻结列表。若 Decision Surface 已明确一个 `Smallest Decision`，作者选中的 `New Fixed Point` 可以且只可以回答这一小层；采用后真正必须继续开放的是候选自己的 `What Remains Unknown`。
4. Author-Approved Future Direction 可以授权**未来将发生**的入口、对质、穿越或其它事件；这不等于它已经发生。候选可以使未来事件可执行，但不能把未来方向倒写成过去 Canon。
5. 是否把“作者知道”误写成“人物/读者已经知道”；
6. 是否真的只增加 1—2 个局部 Fixed Point，而不是一口气生成终极世界观；
7. Authority Route 是否只有 `world` 或 `story`，并且后续只应进入规划层，不直接注入章节 Writer。

严格输出：
# MYSTERY CANONIZATION COMPILER
Verdict: PASS / FAIL
Exact Conflicts: 无，或逐条写冲突
Backward-Compatible Reinterpretation: YES / NO
Hidden-Truth Boundary Preserved: YES / NO
Still-Open Boundary Preserved: YES / NO
Planning Route: world / story / NONE
"""


def render_thread(thread: MysteryThread) -> str:
    lines = [
        f"# MYSTERY {thread.mystery_id}",
        f"Question: {thread.question.strip()}",
        f"Author State: {thread.state}",
        f"Authority Route: {thread.route}",
        "## Known Anchors",
        thread.known_anchors.strip() or "NONE",
        "## Decision Trigger",
        thread.decision_trigger.strip() or "NONE",
    ]
    if thread.state == "FIXED_HIDDEN":
        if not thread.fixed_point.strip():
            raise ValueError("FIXED_HIDDEN Mystery 必须有 fixed_point")
        if not thread.reveal_boundary.strip():
            raise ValueError("FIXED_HIDDEN Mystery 必须有 reveal_boundary")
        lines += [
            "## Author Fixed Hidden Truth",
            thread.fixed_point.strip(),
            "## Reveal Boundary",
            thread.reveal_boundary.strip() or "NONE",
            "## Still Open",
            thread.remains_unknown.strip() or "NONE",
        ]
    else:
        if thread.fixed_point.strip():
            raise ValueError("OPEN Mystery 不得预填 fixed_point")
        if thread.reveal_boundary.strip():
            raise ValueError("OPEN Mystery 不得预填 reveal_boundary")
        lines += ["## Still Open", thread.remains_unknown.strip() or thread.question.strip()]
    return "\n\n".join(lines).strip() + "\n"


def build_decision_surface_prompt(*, thread: MysteryThread, planning_need: str, current_context: str) -> str:
    return "\n\n".join(
        (
            DECISION_SURFACE_PROMPT.strip(),
            "# AUTHOR MYSTERY STATE\n" + render_thread(thread).strip(),
            "# CURRENT PLANNING NEED\n" + planning_need.strip(),
            "# CURRENT APPROVED / ALREADY-HAPPENED CONTEXT\n" + current_context.strip(),
        )
    ) + "\n"


def parse_decision_surface(text: str) -> Literal["DEFER", "DECISION NEEDED"]:
    match = re.search(r"(?mi)^Status:\s*(DEFER|DECISION NEEDED)\s*$", text)
    if not match:
        raise ValueError("Mystery Decision Surface 缺少合法 Status")
    return match.group(1).upper()  # type: ignore[return-value]


def _extract_field(text: str, heading: str) -> str:
    pattern = rf"(?ms)^### {re.escape(heading)}\s*\n(.*?)(?=^### |^## |\Z)"
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f"缺少三级标题：{heading}")
    return match.group(1).strip()


def extract_reframe_candidates(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^## (R[123]|D0)｜.*$", text))
    result: dict[str, str] = {}
    for i, match in enumerate(matches):
        key = match.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[key] = text[match.start():end].strip()
    if tuple(result) != ("R1", "R2", "R3", "D0"):
        raise ValueError(f"Mystery Reframe 必须恰好包含 R1/R2/R3/D0，实际为 {tuple(result)}")
    for key in ("R1", "R2", "R3"):
        candidate = result[key]
        for heading in (
            "New Fixed Point",
            "What Remains Unknown",
            "Backward Compatibility",
            "New Story Doors",
            "Reveal Boundary",
            "Authority Route",
        ):
            _extract_field(candidate, heading)
        route = _extract_field(candidate, "Authority Route").strip().casefold()
        if route not in {"world", "story"}:
            raise ValueError(f"{key} Authority Route 必须为 world/story")
    if _extract_field(result["D0"], "No New Truth").strip().upper() != "NONE":
        raise ValueError("D0 必须明确 No New Truth = NONE")
    return result


def build_reframe_prompt(*, thread: MysteryThread, decision_surface: str, current_context: str) -> str:
    if parse_decision_surface(decision_surface) != "DECISION NEEDED":
        raise ValueError("只有 DECISION NEEDED 才允许启动 Reframe Forge")
    return "\n\n".join(
        (
            REFRAME_FORGE_PROMPT.strip(),
            "# AUTHOR MYSTERY STATE\n" + render_thread(thread).strip(),
            "# DECISION SURFACE\n" + decision_surface.strip(),
            "# CURRENT APPROVED / ALREADY-HAPPENED CONTEXT\n" + current_context.strip(),
        )
    ) + "\n"


def build_canonization_compiler_prompt(
    *,
    thread: MysteryThread,
    selected_candidate: str,
    current_context: str,
    decision_surface: str = "",
    planning_need: str = "",
) -> str:
    # Parsing the selected candidate first prevents malformed outputs from reaching the compiler.
    for heading in (
        "New Fixed Point",
        "What Remains Unknown",
        "Backward Compatibility",
        "New Story Doors",
        "Reveal Boundary",
        "Authority Route",
    ):
        _extract_field(selected_candidate, heading)
    return "\n\n".join(
        (
            CANONIZATION_COMPILER_PROMPT.strip(),
            "# CURRENT AUTHOR MYSTERY STATE\n" + render_thread(thread).strip(),
            "# DECISION SURFACE｜What is authorized to become fixed now\n"
            + (decision_surface.strip() or "（未提供；不得自行扩大可回答范围。）"),
            "# AUTHOR-APPROVED FUTURE DIRECTION｜Future only, not past Canon\n"
            + (planning_need.strip() or "（未提供额外未来方向。）"),
            "# AUTHOR-SELECTED CANDIDATE\n" + selected_candidate.strip(),
            "# EXISTING CANON / KNOWN ANCHORS\n" + current_context.strip(),
        )
    ) + "\n"


def parse_compiler_verdict(text: str) -> Literal["PASS", "FAIL"]:
    match = re.search(r"(?mi)^Verdict:\s*(PASS|FAIL)\s*$", text)
    if not match:
        raise ValueError("Mystery Canonization Compiler 缺少 PASS/FAIL")
    return match.group(1).upper()  # type: ignore[return-value]


def adopt_hidden_fixed_point(*, thread: MysteryThread, selected_candidate: str, compiler_report: str) -> MysteryThread:
    if thread.state != "OPEN":
        raise ValueError("只能从 OPEN Mystery 采用新的 Hidden Fixed Point")
    if parse_compiler_verdict(compiler_report) != "PASS":
        raise ValueError("Compiler 未 PASS，不得采用 Hidden Fixed Point")
    fixed = _extract_field(selected_candidate, "New Fixed Point")
    remains = _extract_field(selected_candidate, "What Remains Unknown")
    reveal_boundary = _extract_field(selected_candidate, "Reveal Boundary")
    route = _extract_field(selected_candidate, "Authority Route").strip().casefold()
    if route not in {"world", "story"}:
        raise ValueError("Authority Route 必须为 world/story")
    return MysteryThread(
        mystery_id=thread.mystery_id,
        question=thread.question,
        state="FIXED_HIDDEN",
        known_anchors=thread.known_anchors,
        decision_trigger=thread.decision_trigger,
        fixed_point=fixed,
        remains_unknown=remains,
        reveal_boundary=reveal_boundary,
        route=route,  # type: ignore[arg-type]
    )


def render_planning_projection(thread: MysteryThread) -> str:
    if thread.state != "FIXED_HIDDEN":
        return (
            f"Mystery {thread.mystery_id}｜AUTHOR OPEN\n"
            f"Question: {thread.question.strip()}\n"
            "作者尚未决定答案。规划可以制造新证据、误判、后果或更具体的问题，但不得把任何答案升级成事实。\n"
            f"Still Open: {thread.remains_unknown.strip() or thread.question.strip()}"
        )
    return (
        f"Mystery {thread.mystery_id}｜AUTHOR FIXED HIDDEN｜Route: {thread.route}\n"
        f"Fixed Point: {thread.fixed_point.strip()}\n"
        f"Reveal Boundary: {thread.reveal_boundary.strip() or 'NONE'}\n"
        f"Still Open: {thread.remains_unknown.strip() or 'NONE'}\n"
        "这是作者层隐藏事实，只供 World/Story 规划层约束未来兼容性。规划必须真实使用 Fixed Point：当前阶段的门、证据、人物行动与后果不得依赖其它答案；如果 Reveal Boundary 允许本阶段确认一层，就必须安排足以让这一层在未来正文成为确定事实的可观察事件。不得把 Fixed Point 本身当旁白泄露，也不得越过 Reveal Boundary；人物、读者与章节 Writer 在实际 Reveal Event 发生前不能直接得到答案。"
    )


_REVEAL_FIELD_RE = re.compile(
    r"^(Mystery ID|Reveal Chapter|Event Atom|State Residue|Reader Anchors|Still Open After Reveal)\s*:\s*(.*?)\s*$"
)


def parse_reveal_contract(text: str) -> MysteryRevealContract:
    """Parse one research-only reader-facing reveal transport contract.

    The contract is deliberately tiny. It contains only what the reveal chapter may
    receive; raw Author Hidden Truth is never a runtime field.
    """

    values: dict[str, str] = {}
    for raw in text.splitlines():
        match = _REVEAL_FIELD_RE.match(raw.strip())
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if key in values:
            raise ValueError(f"Mystery Reveal Contract 重复字段：{key}")
        values[key] = value
    required = (
        "Mystery ID",
        "Reveal Chapter",
        "Event Atom",
        "State Residue",
        "Reader Anchors",
        "Still Open After Reveal",
    )
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise ValueError("Mystery Reveal Contract 缺少字段：" + "、".join(missing))
    try:
        reveal_chapter = int(values["Reveal Chapter"])
    except ValueError as error:
        raise ValueError("Reveal Chapter 必须是正整数") from error
    if reveal_chapter < 1:
        raise ValueError("Reveal Chapter 必须是正整数")
    anchors = tuple(
        part.strip()
        for part in re.split(r"[；;]", values["Reader Anchors"])
        if part.strip()
    )
    if not anchors:
        raise ValueError("Mystery Reveal Contract 至少需要一个 Reader Anchor")
    if len(anchors) > 6:
        raise ValueError("Mystery Reveal Contract Reader Anchors 最多 6 个")
    return MysteryRevealContract(
        mystery_id=values["Mystery ID"],
        reveal_chapter=reveal_chapter,
        event_atom=values["Event Atom"],
        state_residue=values["State Residue"],
        reader_anchors=anchors,
        still_open_after_reveal=values["Still Open After Reveal"],
    )


def extract_reveal_contracts(text: str) -> tuple[MysteryRevealContract, ...]:
    """Extract zero or more reveal contracts from a Story Program response."""

    matches = list(re.finditer(r"(?m)^# MYSTERY REVEAL CONTRACT\s*$", text))
    contracts: list[MysteryRevealContract] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end].strip()
        contracts.append(parse_reveal_contract(block))
    ids = [contract.mystery_id for contract in contracts]
    if len(ids) != len(set(ids)):
        raise ValueError("同一 Story Program 不得为同一个 Mystery 输出多个 Reveal Contract")
    return tuple(contracts)


def strip_reveal_contracts(text: str) -> str:
    """Remove reader-facing reveal transport before Story Program reaches Outline."""

    match = re.search(r"(?m)^# MYSTERY REVEAL CONTRACT\s*$", text)
    return text[: match.start()].rstrip() if match else text.strip()


def compile_runtime_mystery_projection(
    thread: MysteryThread,
    reveal: MysteryRevealContract,
    *,
    chapter_number: int,
) -> str:
    """Project a fixed hidden mystery to chapter runtime without leaking the answer.

    Before the scheduled reveal, chapter agents only see the unresolved boundary.
    On the reveal chapter they receive only the reader-facing event contract. After
    that chapter, the State/Canon path is expected to carry the revealed residue.
    """

    if thread.state != "FIXED_HIDDEN":
        raise ValueError("Runtime reveal projection 需要 FIXED_HIDDEN Mystery")
    if reveal.mystery_id != thread.mystery_id:
        raise ValueError("Reveal Contract 与 Mystery ID 不一致")
    if chapter_number < 1:
        raise ValueError("chapter_number 必须是正整数")
    if chapter_number < reveal.reveal_chapter:
        return (
            f"# MYSTERY UNRESOLVED FACT BOUNDARY｜{thread.mystery_id}\n"
            f"Question: {thread.question.strip()}\n"
            f"Still Unknown: {thread.remains_unknown.strip() or thread.question.strip()}\n"
            "作者层可能已有隐藏决定，但本章没有 Reveal Authority。不得补答案、暗示唯一答案或让角色凭空知道。"
        )
    if chapter_number == reveal.reveal_chapter:
        return (
            f"# MYSTERY REVEAL EVENT｜{thread.mystery_id}\n"
            f"Event Atom: {reveal.event_atom}\n"
            f"State Residue: {reveal.state_residue}\n"
            f"Still Open After Reveal: {reveal.still_open_after_reveal}\n"
            f"Reader Anchors: {'；'.join(reveal.reader_anchors)}\n"
            "只让读者经历这一层 Reveal；State Residue 不能替代现场事件，更深未知不得顺手解释。"
        )
    return ""


def advance_after_reveal(
    thread: MysteryThread,
    reveal: MysteryRevealContract,
    *,
    next_decision_trigger: str,
) -> MysteryThread:
    """Turn one revealed hidden layer into a new Author-Open deeper question."""

    if thread.state != "FIXED_HIDDEN":
        raise ValueError("只有 FIXED_HIDDEN Mystery 完成 Reveal 后才能进入下一轮")
    if reveal.mystery_id != thread.mystery_id:
        raise ValueError("Reveal Contract 与 Mystery ID 不一致")
    anchors = thread.known_anchors.strip()
    revealed = f"- 已揭晓并进入 Canon：{reveal.state_residue.strip()}"
    known = "\n".join(part for part in (anchors, revealed) if part).strip()
    return MysteryThread(
        mystery_id=thread.mystery_id,
        question=reveal.still_open_after_reveal.strip(),
        state="OPEN",
        known_anchors=known,
        decision_trigger=next_decision_trigger.strip(),
        remains_unknown=reveal.still_open_after_reveal.strip(),
        route=thread.route,
    )
