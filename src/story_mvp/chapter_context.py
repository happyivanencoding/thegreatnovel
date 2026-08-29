"""章节写作运行期上下文包（Chapter Runtime Lite v1）。

只由页面已提交的可见输入做确定性组装：不调用 LLM、不写文件、不发网络请求。
每个逻辑区块在渲染进最终 Prompt 时都携带明确权威标签：

- CANON PROSE：已批准的正式前文，已经发生事实的最高来源
- BOOK CONTRACT：作者批准的长期设计（BOOK §0—§5），约束未来，不等于已经发生
- CANON INDEX：当前状态与最近摘要，只是正式正文的压缩索引
- PLAN：尚未发生的当前意图（当前大型剧情块、十章计划与八字段小纲）
- PROSE PROFILE：软表达控制（BOOK §7—§10 节奏/文风画像），只控制表达方式
- OPTIONAL INSPIRATION：可选参考（GBrain 结果与 Reference Programs），
  不得覆盖以上任何层级

权威不再使用单条总排名，而是按维度划分（见 MINIMAL_AUTHORITY_RULE）：
已发生事实（CANON PROSE > CANON INDEX）、未来创作意图
（BOOK CONTRACT > PLAN > OPTIONAL INSPIRATION）、表达控制（PROSE PROFILE）。
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from .character_context import project_effective_world_reality
from .prompts import (
    CURRENT_STATE_HEADING,
    canon_memory_has_labels,
    canon_index_has_labels,
    format_references,
    parse_canon_memory,
    parse_canon_index,
    parse_outline_fields,
    render_canon_memory,
    render_canon_index,
)

#: authority 区块只放这一份最小权威规则（按维度划分 + 冲突处理方式），
#: 整份运行合同不再重复注入。
MINIMAL_AUTHORITY_RULE = """权威规则按维度划分（不使用单条总排名）：
1. 已发生事实：CANON PROSE > CANON INDEX。CANON PROSE 是已批准的正式前文；已经发生事实的最高来源。CANON INDEX 是当前状态和最近摘要，是正式正文的压缩索引；与正式正文冲突时以正式正文为准。
2. 世界事实：WORLD AUTHORITY 是已批准 World Vision 的安全事实投影，负责世界规律、普通生活、力量正常值、社会现实、价值结构与公开知识边界；BOOK / PLAN 可以决定这些事实何时进入故事，但不得改写它们。named 大事件与未解谜底不在该投影中，仍服从已批准 Story / Plan 与未知边界。
3. 未来创作意图：BOOK CONTRACT > PLAN > OPTIONAL INSPIRATION。BOOK CONTRACT 决定长期故事方向、读者承诺和人物方向；PLAN 决定当前尚未发生的剧情；OPTIONAL INSPIRATION 不能覆盖以上任何权威。
4. 表达控制：PROSE PROFILE 只控制表达方式，不能修改已发生事实或未来计划，也不能改写 WORLD AUTHORITY。
5. 跨维度冲突：已发生事实不能被 BOOK CONTRACT 或 PLAN 覆盖；如果正文证明旧 BOOK CONTRACT 已经失效，保留已发生事实，不得自动修改 BOOK CONTRACT。世界事实不能被 BOOK / PLAN / Writer 临时改写。Curator 负责在 Curator Audit 中暴露会影响本章执行的明确冲突；Primary 不承担冲突报告或其它 pipeline bookkeeping，只服从已经投影出的有效事实与计划。"""

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

CANON_INDEX_STATUS_HEADING = CURRENT_STATE_HEADING

PROSE_PROFILE_HEADINGS = (
    "## 7. 叙事结构",
    "## 8. 文风与可操作参数",
    "## 9. 对话特点",
    "## 10. 节奏结构",
)

GROWTH_PROJECTION_LABELS = (
    "一级成长变化",
    "二级收益结算",
    "反哺下一轮",
)


@dataclass(frozen=True)
class ChapterContextPacket:
    """章节写作运行期上下文包；所有区块均为确定性文本。"""

    authority: str
    world_authority: str
    book_contract: str
    chapter_mission: str
    canon_context: str
    recent_prose: str
    rolling_plan: str
    chapter_plan_context: str
    current_long_block: str
    current_chapter_plan: str
    prose_profile: str
    optional_inspiration: str
    human_core: str = ""
    power_core: str = ""
    growth_benefit_projection: str = ""
    growth_genome_compact: str = ""
    reader_release: str = ""


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


_CHAPTER_PLAN_FIELDS = (
    "具体剧情",
    "结果 / 状态变化",
    "叙事功能",
    "结尾推动",
)

PLAN_OUTCOME_ADJUSTMENT_MARKER = "[PLAN OUTCOME ADJUSTMENT]"

_LONG_BLOCK_RANGE_HEADING = re.compile(
    r"(?m)^#{1,6}\s*第\s*(\d+)\s*[—–－-]\s*(\d+)\s*章(?:\s*[：:].*)?\s*$"
)
_LONG_BLOCK_SCOPE = re.compile(
    r"规划范围\s*[：:]\s*(?:预计)?\s*第\s*(\d+)\s*[—–－-]\s*(\d+)\s*章"
)


def project_current_long_block_for_chapter(current_long_block: str, chapter_number: int) -> str:
    """只保留明确覆盖当前章的大型剧情块，拒绝把过期块继续注入章节链。

    调用方有时会把整份长纲或上一个窗口的剧情块误传为 ``current_long_block``。
    这类文本一旦带有明确章节范围，就可以确定性裁剪：

    - 有覆盖当前章的范围时，保留最窄的匹配块；
    - 文本明确声明了范围、但没有任何范围覆盖当前章时，返回空；
    - 没有可解析章节范围时保持原文，避免猜测作者意图。

    该函数只删除已经由文本自身证明为 stale 的计划，不生成新计划，也不改变
    ``current_chapter_plan`` 这一本章唯一事件预算。
    """

    text = current_long_block.strip()
    if not text or chapter_number <= 0:
        return text

    scope = _LONG_BLOCK_SCOPE.search(text)
    if scope:
        scope_start, scope_end = sorted((int(scope.group(1)), int(scope.group(2))))
        if not scope_start <= chapter_number <= scope_end:
            return ""

    matches = list(_LONG_BLOCK_RANGE_HEADING.finditer(text))
    if not matches:
        return text

    candidates: list[tuple[int, int, str]] = []
    for index, match in enumerate(matches):
        start, end = sorted((int(match.group(1)), int(match.group(2))))
        if not start <= chapter_number <= end:
            continue
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.start():section_end].strip()
        candidates.append((end - start, index, section))
    if not candidates:
        return ""

    _, _, selected = min(candidates, key=lambda item: (item[0], item[1]))
    preamble = text[:matches[0].start()].strip()
    return "\n\n".join(part for part in (preamble, selected) if part).strip()


def parse_chapter_plan_fields(current_chapter_plan: str) -> dict[str, str]:
    """Parse one production Future-10 chapter entry into its supported fields."""

    text = current_chapter_plan.strip()
    if not text:
        return {}
    field_labels = "|".join(re.escape(field) for field in _CHAPTER_PLAN_FIELDS)
    pattern = re.compile(rf"^\s*(?:[-*]\s*)?({field_labels})\s*[：:](.*)$")
    values: dict[str, str] = {}
    current_label: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        if current_label is None:
            return
        value = "\n".join(current_lines).strip()
        if value:
            values[current_label] = value

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if re.match(r"^#{1,6}(?:\s|$)", stripped):
            flush()
            current_label = None
            current_lines = []
            continue
        match = pattern.match(raw_line)
        if match:
            flush()
            current_label = match.group(1)
            inline = match.group(2).strip()
            current_lines = [inline] if inline else []
            continue
        if current_label is not None and stripped:
            current_lines.append(stripped)
    flush()
    return values


def project_chapter_plan_execution_boundary(current_chapter_plan: str) -> str:
    """Separate this chapter's executable budget from its next-chapter handoff."""

    text = current_chapter_plan.strip()
    values = parse_chapter_plan_fields(text)
    if not values:
        return text
    lines = [
        "本章唯一可执行事件预算（只做这里已经分配给本章的事）：",
        f"具体剧情：{values.get('具体剧情') or '（未填写）'}",
        f"必须兑现的计划结果 / 状态变化：{values.get('结果 / 状态变化') or '（未填写）'}",
    ]
    if values.get("叙事功能"):
        lines.append(f"规划功能：{values['叙事功能']}（只用于理解本章作用，不新增事件。）")
    handoff = values.get("结尾推动")
    if handoff:
        lines.extend(
            [
                "",
                "章末 Handoff Reservation（只能让压力、入口、来人、线索或未完成动作出现；不得在本章完成其下一步事件或结算）：",
                handoff,
            ]
        )
    return "\n".join(lines).strip()


def project_frozen_power_core(character_card: str) -> str:
    """只投影 deterministic CHARACTER.md 中冻结的 Power Core。"""

    lines = character_card.splitlines()
    start: int | None = None
    collected: list[str] = []
    for line in lines:
        stripped = line.strip()
        if start is None:
            if stripped.startswith("## POWER CORE"):
                start = 1
            continue
        if stripped.startswith("## HUMAN CORE"):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def project_frozen_human_core(character_card: str) -> str:
    """只投影 deterministic CHARACTER.md 中稳定的 Human Core。"""

    lines = character_card.splitlines()
    start: int | None = None
    collected: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if start is None:
            if stripped.startswith("## HUMAN CORE"):
                start = index + 1
            continue
        if stripped == "## Composition Boundary":
            break
        collected.append(line)
    return "\n".join(collected).strip()


def extract_reader_release_for_chapter(book_content: str, chapter_number: int) -> str:
    """Extract one chapter's optional Reader Release Map entry from BOOK §2.

    This is planning metadata, not Canon and not a per-chapter requirement. It keeps
    Outline's timing decision visible to chapter runtime without another model call.
    """

    if chapter_number <= 0:
        return ""
    world_structure = _markdown_block(book_content, "## 2. 世界观结构")
    if not world_structure:
        return ""
    match = re.search(
        r"(?ms)^### Reader Release Map\s*$\n(.*?)(?=^###\s+|\Z)",
        world_structure,
    )
    if not match:
        return ""
    target = f"第{chapter_number}章"
    return "\n".join(
        line.strip()
        for line in match.group(1).splitlines()
        if line.strip() and target in line
    ).strip()


def render_event_contract(current_outline: str, *, approved_plan_outcome: str = "") -> str:
    """把八字段小纲渲染为规划/筛选节点共用的完整事件合同。

    六项合同字段按原文保留“字段：内容”形式；「推动事件的人」呈现为场景上下文；
    「叙事功能」明确标为规划备注，不要求正文显式表达。若 Future-10 已批准当前章
    outcome，则确定性并入 Frozen Mission 的状态变化，而不是依赖 Director 复述。
    """
    values = parse_outline_fields(current_outline)
    if approved_plan_outcome.strip():
        director_state = values.get("状态变化", "").strip()
        required = (
            "上游计划已批准结果（本章必须同时成立；若与已发生 Canon 冲突则 Canon 优先）："
            + approved_plan_outcome.strip()
        )
        values["状态变化"] = "\n".join(part for part in (director_state, required) if part)
    lines = [
        "当前章事件合同：下方八字段决定 WHAT HAPPENS，不决定 HOW TO SAY；下游节点按各自职责使用这些事实约束，不把小纲扩写成更长概述。",
        "",
        f"场景上下文——推动事件的人：{values.get('推动事件的人') or '（未填写）'}",
        "",
        "事件合同（六项必须落实；这是事实约束，不是正文措辞来源）：",
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


def render_event_contract_with_plan_outcome(
    current_outline: str, current_chapter_plan: str
) -> str:
    """Freeze Future-10 outcome inside Mission unless Canon forced an explicit adjustment."""

    director_state = parse_outline_fields(current_outline).get("状态变化", "")
    if PLAN_OUTCOME_ADJUSTMENT_MARKER in director_state:
        return render_event_contract(current_outline)
    outcome = parse_chapter_plan_fields(current_chapter_plan).get("结果 / 状态变化", "").strip()
    return render_event_contract(current_outline, approved_plan_outcome=outcome)


def project_event_contract_for_prose(chapter_mission: str) -> str:
    """给正文节点的最小事件合同：保留必须发生的现场语义，移除纯规划备注。"""

    mission = chapter_mission.strip()
    if not mission:
        return mission
    mission = mission.split("\n规划备注（planning note）：", 1)[0].rstrip()
    mission = mission.replace(
        "当前章事件合同：下方八字段决定 WHAT HAPPENS，不决定 HOW TO SAY；下游节点按各自职责使用这些事实约束，不把小纲扩写成更长概述。",
        "正文执行合同：只保留本章必须发生的行动、反应、结果与状态变化；这些是事实目标，不是正文措辞。",
        1,
    )
    return mission


def _extract_growth_projection_value(texts: Iterable[str], label: str) -> str:
    labels = set(GROWTH_PROJECTION_LABELS)
    for text in texts:
        lines = text.splitlines()
        for index, line in enumerate(lines):
            normalized_line = line.replace("**", "").strip()
            match = re.match(rf"^{re.escape(label)}\s*[：:]\s*(.*)$", normalized_line)
            if not match:
                continue
            values = [match.group(1).strip()] if match.group(1).strip() else []
            for next_line in lines[index + 1 :]:
                normalized_next_line = next_line.replace("**", "").strip()
                stripped = normalized_next_line
                if any(
                    re.match(rf"^{re.escape(next_label)}\s*[：:]", normalized_next_line)
                    for next_label in labels
                ) or stripped.startswith("#"):
                    break
                if stripped:
                    values.append(stripped)
            return "\n".join(values).strip()
    return ""


def _markdown_subsection(content: str, heading: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1 :]:
            if next_line.strip().startswith("#"):
                break
            collected.append(next_line)
        return "\n".join(collected).strip()
    return ""


def compact_growth_genome_for_chapter(book_content: str) -> str:
    """保留章节 Agent 需要的固定三段 §0 压缩投影。"""

    genome = _markdown_block(book_content, "## 0. 本书成长基因图")
    if not genome:
        return "（BOOK 未提供成长基因图。）"
    blocks: list[str] = []
    fantasy_heading = "### 已批准幻想不变量"
    fantasy = _markdown_subsection(genome, fantasy_heading)
    if not fantasy:
        fantasy_heading = "### 作者明确保留"
        fantasy = _markdown_subsection(genome, fantasy_heading)
    if fantasy:
        blocks.append(f"{fantasy_heading}\n\n{fantasy}")
    for heading in ("### 核心不变量", "### 退化风险"):
        body = _markdown_subsection(genome, heading)
        if body:
            blocks.append(f"{heading}\n\n{body}")
    if not blocks:
        # 旧书没有新固定小节时保留原有短/旧 §0，保证旧书可继续运行。
        return f"## 0. 本书成长基因图\n\n{genome}"
    return "## 0. 本书成长基因图（章节压缩）\n\n" + "\n\n".join(blocks)


def _growth_projection_values(text: str) -> dict[str, str]:
    return {
        label: _extract_growth_projection_value((text,), label)
        for label in GROWTH_PROJECTION_LABELS
    }


def render_growth_benefit_projection(
    *,
    current_long_block: str = "",
    current_chapter_plan: str = "",
    current_outline: str = "",
) -> str:
    """从当前计划的可见标签生成三行非门禁成长投影。"""

    outline_values = _growth_projection_values(current_outline)
    chapter_plan_values = _growth_projection_values(current_chapter_plan)
    long_block_values = _growth_projection_values(current_long_block)

    def render_value(
        prefix: str,
        label: str,
        empty_default: str,
        reference_default: str,
        reference_label: str,
    ) -> str:
        explicit = outline_values[label] or chapter_plan_values[label]
        if explicit:
            return f"{prefix}{explicit}"
        reference = long_block_values[label]
        if reference:
            return (
                f"{prefix}\n未在本章计划中明确；{reference_default}\n"
                f"当前剧情块{reference_label}仅供参照：{reference}"
            )
        return f"{prefix}{empty_default}"

    return "\n".join(
        (
            render_value(
                "本章一级成长推进：",
                "一级成长变化",
                "本章计划未明确；不强制本章推进。",
                "不强制本章推进。",
                "一级成长目标",
            ),
            render_value(
                "本章二级收益结算：",
                "二级收益结算",
                "本章计划未明确；不强制本章结算。",
                "不强制本章结算。",
                "二级收益目标",
            ),
            render_value(
                "本章反哺：",
                "反哺下一轮",
                "本章计划未明确；不强制本章反哺。",
                "不强制本章反哺。",
                "反哺目标",
            ),
        )
    )


def _without_genre_prior(text: str) -> str:
    """章节节点不携带原始 Genre Prior；保留同一 Bundle 中的具体机制材料。"""

    clean = text.strip()
    if not clean:
        return ""
    blocks = re.split(r"(?=^###\s+Inspiration\s+\d+\s*$)", clean, flags=re.MULTILINE)
    if len(blocks) == 1:
        return "" if any(marker in clean.casefold() for marker in ("genre-prior", "题材先验")) else clean
    kept = [
        block.strip()
        for block in blocks
        if block.strip() and not any(marker in block.casefold() for marker in ("genre-prior", "题材先验"))
    ]
    return "\n\n".join(kept).strip()


def build_chapter_context(
    *,
    book_content: str = "",
    character_card: str = "",
    world_vision: str = "",
    world_expansions: str = "",
    current_long_block: str = "",
    previous_chapter_text: str = "",
    current_outline: str = "",
    current_chapter_plan: str = "",
    recent_summaries: str = "",
    gbrain_inspiration: str = "",
    selected_references: Iterable[Mapping[str, Any]] | None = None,
    chapter_number: int = 0,
) -> ChapterContextPacket:
    """由现有页面输入确定性地构建章节运行期上下文包。"""
    effective_long_block = project_current_long_block_for_chapter(
        current_long_block, chapter_number
    )
    prose_profile = "\n\n".join(
        f"{heading}\n\n{_markdown_block(book_content, heading)}"
        for heading in PROSE_PROFILE_HEADINGS
        if _markdown_block(book_content, heading)
    )

    book_contract = "\n\n".join(
        f"{heading}\n\n{_markdown_block(book_content, heading)}"
        for heading in CONTEXT_HEADINGS
        if _markdown_block(book_content, heading)
    )

    canon_parts: list[str] = []
    status = _markdown_block(book_content, CANON_INDEX_STATUS_HEADING)
    page_summaries = recent_summaries.strip()
    summaries_rendered = False
    if status:
        if canon_memory_has_labels(status):
            canon_parts.append(
                "当前状态、未兑现承诺与作者备注（Canon Memory v2）\n\n"
                + render_canon_memory(
                    parse_canon_memory(status), page_recent_summaries=page_summaries
                )
            )
            summaries_rendered = True
        elif canon_index_has_labels(status):
            # 规范化 CANON INDEX：四段语义分开渲染；最近摘要只注入一份
            # （页面显式传入优先，否则用 BOOK 状态区内解析出的摘要）。
            canon_parts.append(
                "当前状态、未兑现承诺与作者备注（规范化 CANON INDEX）\n\n"
                + render_canon_index(
                    parse_canon_index(status), page_recent_summaries=page_summaries
                )
            )
            summaries_rendered = True
        else:
            canon_parts.append(f"当前状态、未兑现承诺与作者备注\n\n{status}")
    if page_summaries and not summaries_rendered:
        canon_parts.append(f"最近 1—3 章摘要\n\n{page_summaries}")
    canon_context = "\n\n".join(canon_parts)

    plan_parts: list[str] = []
    if effective_long_block:
        plan_parts.append(f"当前大型剧情块\n\n{effective_long_block}")
    small_plan = _markdown_block(book_content, "# 未来十章逐章小纲")
    if small_plan:
        plan_parts.append(f"当前十章计划\n\n{small_plan}")
    rolling_plan = "\n\n".join(plan_parts)
    chapter_plan_parts: list[str] = []
    if effective_long_block:
        chapter_plan_parts.append(f"当前大型剧情块\n\n{effective_long_block}")
    if current_chapter_plan.strip():
        chapter_plan_parts.append(f"当前章十章计划条目\n\n{current_chapter_plan.strip()}")
    chapter_plan_context = "\n\n".join(chapter_plan_parts)

    inspiration = _without_genre_prior(gbrain_inspiration) or "（本次没有提供灵感；允许空结果，不补位。）"
    references = format_references(selected_references or [])
    optional_inspiration = (
        "可选参考声明：以下灵感与 Reference Programs 只是可选参考，"
        "不得覆盖以上任何层级（含 BOOK CONTRACT、CANON PROSE、CANON INDEX、PLAN）；"
        "无兼容结果时允许空结果，不补位。\n\n"
        f"GBrain Inspiration Results（作者可编辑原文）\n\n{inspiration}\n\n"
        f"选中的 Reference Programs（可选参考，不与事件合同并列为硬要求）\n\n{references}"
    )
    growth_benefit_projection = render_growth_benefit_projection(
        current_long_block=effective_long_block,
        current_chapter_plan=current_chapter_plan,
        current_outline=current_outline,
    )
    growth_genome_compact = compact_growth_genome_for_chapter(book_content)
    return ChapterContextPacket(
        authority=MINIMAL_AUTHORITY_RULE,
        world_authority=(
            project_effective_world_reality(
                world_vision, world_expansions, chapter_number
            )
            if world_vision.strip()
            else ""
        ),
        reader_release=extract_reader_release_for_chapter(book_content, chapter_number),
        book_contract=book_contract,
        chapter_mission=render_event_contract_with_plan_outcome(current_outline, current_chapter_plan),
        canon_context=canon_context,
        recent_prose=previous_chapter_text.strip(),
        rolling_plan=rolling_plan,
        chapter_plan_context=chapter_plan_context,
        current_long_block=effective_long_block,
        current_chapter_plan=current_chapter_plan.strip(),
        prose_profile=prose_profile,
        optional_inspiration=optional_inspiration,
        human_core=project_frozen_human_core(character_card),
        power_core=project_frozen_power_core(character_card),
        growth_benefit_projection=growth_benefit_projection,
        growth_genome_compact=growth_genome_compact,
    )


@dataclass(frozen=True)
class DirectorContextPacket:
    current_long_block: str
    current_chapter_plan: str
    opportunity_authority: str
    growth_genome_compact: str
    canon_index: str
    recent_summaries: str
    transition_context: str
    author_intent: str


_OPPORTUNITY_PATTERN = re.compile(
    r"公开试场|试场|选拔|招募|报名|大比|竞赛|拍卖|契约|名额|邀请|传承机会|资格"
)
_OPPORTUNITY_VALUE_PATTERN = re.compile(
    r"随队|护送契约|契约|预付款|报酬|收入|离乡|离开本镇|跨城|身份|名额|进入|入口|奖励|传承|功法|兵器|资源"
)


def project_current_opportunity_authority(
    current_long_block: str,
    current_chapter_plan: str,
    *,
    max_chars: int = 360,
) -> str:
    """Recover one approved named-opportunity value line lost by chapter-plan compression.

    This is deterministic projection only. It never synthesizes a reward or promotes a
    future result; it returns an existing sentence from the current long block only when
    the current chapter plan already refers to the same opportunity family.
    """

    long_block = current_long_block.strip()
    chapter_plan = current_chapter_plan.strip()
    if not long_block or not chapter_plan:
        return ""
    plan_terms = set(_OPPORTUNITY_PATTERN.findall(chapter_plan))
    if not plan_terms:
        return ""

    candidates: list[tuple[int, str]] = []
    for raw_line in long_block.splitlines():
        line = raw_line.strip().lstrip("-* ").strip()
        if not line or not _OPPORTUNITY_PATTERN.search(line) or not _OPPORTUNITY_VALUE_PATTERN.search(line):
            continue
        overlap = sum(1 for term in plan_terms if term in line)
        if overlap <= 0:
            continue
        value_hits = len(set(_OPPORTUNITY_VALUE_PATTERN.findall(line)))
        candidates.append((overlap * 10 + value_hits, line))
    if not candidates:
        return ""

    line = max(candidates, key=lambda item: item[0])[1]
    sentences = [part.strip() for part in re.split(r"(?<=[。！？])", line) if part.strip()]
    selected: list[str] = []
    for sentence in sentences:
        if not selected or _OPPORTUNITY_VALUE_PATTERN.search(sentence):
            selected.append(sentence)
        if _OPPORTUNITY_VALUE_PATTERN.search("".join(selected)):
            break
    result = "".join(selected).strip() or line
    return result[:max_chars].strip()


def _tail_for_director(text: str, max_chars: int = 1800) -> str:
    clean = text.strip()
    if len(clean) <= max_chars:
        return clean
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", clean) if part.strip()]
    selected: list[str] = []
    size = 0
    for paragraph in reversed(paragraphs):
        added = len(paragraph) + (2 if selected else 0)
        if selected and size + added > max_chars:
            break
        selected.insert(0, paragraph)
        size += added
    return "\n\n".join(selected) or clean[-max_chars:]


def _recent_summaries_for_director(text: str, max_chars: int = 1800) -> str:
    """给 Director 保留最近 1—3 个摘要，避免只突出最后一章。"""

    clean = text.strip()
    if not clean:
        return ""
    chapter_starts = list(re.finditer(r"(?m)^(?:[-*]\s*)?第\s*\d+\s*章\s*[：:].*$", clean))
    if chapter_starts:
        selected_starts = chapter_starts[-3:]
        blocks = [
            clean[start.start() : (chapter_starts[index + 1].start() if index + 1 < len(chapter_starts) else len(clean))].strip()
            for index, start in enumerate(
                selected_starts,
                start=len(chapter_starts) - len(selected_starts),
            )
        ]
        return _tail_for_director("\n\n".join(blocks), max_chars)
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", clean) if part.strip()]
    return _tail_for_director("\n\n".join(paragraphs[-3:]), max_chars)


def _without_recent_summaries_for_director(text: str) -> str:
    """Director 单独注入最近摘要；Canon Index 保留其它状态，避免重复。"""

    lines = text.splitlines()
    collected: list[str] = []
    skipping = False
    recent_heading = re.compile(
        r"^(?:##\s+)?(?:RECENT SUMMARIES|最近 1—3 章摘要|最近章节摘要)(?:（|\(|：|:|$)"
    )
    next_heading = re.compile(
        r"^(?:##\s+)?(?:OPEN PROMISES|AUTHOR NOTES|CURRENT STATE)(?:（|\(|：|:|$)"
    )
    for line in lines:
        stripped = line.strip()
        if recent_heading.match(stripped):
            skipping = True
            continue
        if skipping and next_heading.match(stripped):
            skipping = False
        if not skipping:
            collected.append(line)
    return "\n".join(collected).strip()


def build_director_context(
    packet: ChapterContextPacket,
    *,
    recent_summaries: str = "",
    author_intent: str = "",
) -> DirectorContextPacket:
    """Director 的固定轻量投影，不读取完整 BOOK 或完整十章计划。"""

    return DirectorContextPacket(
        current_long_block=packet.current_long_block or "（未提供当前大型剧情块。）",
        current_chapter_plan=(
            project_chapter_plan_execution_boundary(packet.current_chapter_plan)
            or "（未提供当前章十章计划条目。）"
        ),
        opportunity_authority=project_current_opportunity_authority(
            packet.current_long_block,
            packet.current_chapter_plan,
        ),
        growth_genome_compact=packet.growth_genome_compact,
        canon_index=(
            _without_recent_summaries_for_director(packet.canon_context)
            or "（当前 Canon Index 为空。）"
        ),
        recent_summaries=_recent_summaries_for_director(recent_summaries) or "（未提供最近 1—3 章摘要。）",
        transition_context=_tail_for_director(packet.recent_prose) or "（无前文章末衔接片段。）",
        author_intent=author_intent.strip() or "（未提供额外作者章意图。）",
    )
