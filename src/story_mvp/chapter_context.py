"""章节写作运行期上下文包（Chapter Runtime Lite v1）。

只由页面已提交的可见输入做确定性组装：不调用 LLM、不写文件、不发网络请求。
每个逻辑区块在渲染进最终 Prompt 时都携带明确权威标签：

- CANON：已经发生，不得修改（前文正文、已确认设定/状态/摘要）
- PLAN：尚未发生的当前意图（当前大型剧情块、十章计划与八字段小纲）
- PROSE PROFILE：软表达控制（BOOK §7—§10 节奏/文风画像）
- OPTIONAL INSPIRATION：可选参考（GBrain 结果与 Reference Programs），
  不得覆盖 CANON 或 PLAN
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from .prompts import format_references, parse_outline_fields

#: authority 区块只放这一份最小权威规则（权威层级 + 冲突处理方式），
#: 整份运行合同不再重复注入。
MINIMAL_AUTHORITY_RULE = """权威层级（从高到低）：
1. CANON——已批准的前文正文是已发生事实的最高来源；BOOK 当前状态和最近摘要只是正文事实的压缩索引；若摘要、当前状态或旧计划与正式正文冲突，以正式正文为准。已确认的 BOOK 设定与状态/摘要属于已经发生、不得修改的事实。
2. PLAN——当前章小纲只决定尚未发生的本章事件，不能覆盖正式正文。
3. PROSE PROFILE——BOOK §7—§10 软表达控制，只调整表达方式，不改变事实与事件。
4. INSPIRATION——可选参考，不得覆盖 CANON 或 PLAN。
冲突处理方式：若前文事实与小纲冲突，保留已发生事实并显式暴露冲突；任何冲突必须写入 Writer Audit，不得偷偷改写过去。"""

#: 事件合同重点呈现的六项；「推动事件的人」作为场景上下文，「叙事功能」降级为规划备注。
EVENT_CONTRACT_FIELDS = (
    "触发事件",
    "主角行动",
    "对手或世界反应",
    "直接结果",
    "状态变化",
    "结尾推动力",
)

CONTEXT_HEADINGS = (
    "## 0. 本书成长基因图",
    "## 1. 核心类型与读者承诺",
    "## 2. 世界观结构",
    "## 3. 世界如何持续制造剧情压力",
    "## 4. 主角模型、人物弧与核心矛盾",
    "## 5. 配角与关系系统",
)

PROSE_PROFILE_HEADINGS = (
    "## 7. 叙事结构",
    "## 8. 文风与可操作参数",
    "## 9. 对话特点",
    "## 10. 节奏结构",
)


@dataclass(frozen=True)
class ChapterContextPacket:
    """章节写作运行期上下文包；所有区块均为确定性文本。"""

    authority: str
    chapter_mission: str
    canon_context: str
    recent_prose: str
    rolling_plan: str
    prose_profile: str
    optional_inspiration: str


def _markdown_block(content: str, heading: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1:]:
            stripped = next_line.strip()
            if stripped.startswith("# ") or (heading.startswith("## ") and stripped.startswith("## ")):
                break
            collected.append(next_line)
        return "\n".join(collected).strip()
    return ""


def render_event_contract(current_outline: str) -> str:
    """把八字段小纲渲染为单 Writer 执行合同。

    六项合同字段按原文保留“字段：内容”形式；「推动事件的人」呈现为场景上下文；
    「叙事功能」明确标为规划备注，不要求正文显式表达。
    """
    values = parse_outline_fields(current_outline)
    lines = [
        "单 Writer 职责：根据下方已批准的事件合同直接写出可提交的正式正文，不把小纲扩写成更长概述。",
        "",
        f"场景上下文——推动事件的人：{values.get('推动事件的人') or '（未填写）'}",
        "",
        "事件合同（六项必须落实）：",
    ]
    lines.extend(
        f"{field}：{values.get(field) or '（未填写）'}" for field in EVENT_CONTRACT_FIELDS
    )
    lines.extend(
        [
            "",
            "规划备注（planning note）：",
            (
                f"叙事功能：{values.get('叙事功能') or '（未填写）'}"
                "——这是规划备注，只用于理解本章在局部故事中的作用；"
                "不要求正文显式表达它，也不把它当成正文硬约束。"
            ),
        ]
    )
    return "\n".join(lines)


def build_chapter_context(
    *,
    book_content: str = "",
    current_long_block: str = "",
    previous_chapter_text: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
    gbrain_inspiration: str = "",
    selected_references: Iterable[Mapping[str, Any]] | None = None,
) -> ChapterContextPacket:
    """由现有页面输入确定性地构建章节运行期上下文包。"""
    prose_profile = "\n\n".join(
        f"{heading}\n\n{_markdown_block(book_content, heading)}"
        for heading in PROSE_PROFILE_HEADINGS
        if _markdown_block(book_content, heading)
    )

    canon_parts = [
        f"{heading}\n\n{_markdown_block(book_content, heading)}"
        for heading in CONTEXT_HEADINGS
        if _markdown_block(book_content, heading)
    ]
    status = _markdown_block(book_content, "# 当前状态、未兑现承诺与作者备注")
    if status:
        canon_parts.append(f"当前状态与未兑现承诺\n\n{status}")
    if recent_summaries.strip():
        canon_parts.append(f"最近 1—3 章摘要\n\n{recent_summaries.strip()}")
    canon_context = "\n\n".join(canon_parts)

    plan_parts: list[str] = []
    if current_long_block.strip():
        plan_parts.append(f"当前大型剧情块\n\n{current_long_block.strip()}")
    small_plan = _markdown_block(book_content, "# 未来十章逐章小纲")
    if small_plan:
        plan_parts.append(f"当前十章计划\n\n{small_plan}")
    rolling_plan = "\n\n".join(plan_parts)

    inspiration = gbrain_inspiration.strip() or "（本次没有提供灵感；允许空结果，不补位。）"
    references = format_references(selected_references or [])
    optional_inspiration = (
        "可选参考声明：以下灵感与 Reference Programs 只是可选参考，"
        "不得覆盖 BOOK、当前小纲或 CANON；无兼容结果时允许空结果，不补位。\n\n"
        f"GBrain Inspiration Results（作者可编辑原文）\n\n{inspiration}\n\n"
        f"选中的 Reference Programs（可选参考，不与事件合同并列为硬要求）\n\n{references}"
    )

    return ChapterContextPacket(
        authority=MINIMAL_AUTHORITY_RULE,
        chapter_mission=render_event_contract(current_outline),
        canon_context=canon_context,
        recent_prose=previous_chapter_text.strip(),
        rolling_plan=rolling_plan,
        prose_profile=prose_profile,
        optional_inspiration=optional_inspiration,
    )
