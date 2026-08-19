"""Hybrid chapter runtime 的确定性上下文和产物辅助函数。

这个模块只负责把已经存在的 ChapterContextPacket 投影成各节点需要的
局部文本，以及从作者可见的模型返回中提取正式区块。它不调用模型、写文件
或调度节点。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Mapping

from .chapter_context import ChapterContextPacket


SPECIALIST_NAMES = ("opening", "dialogue", "action", "emotion")

_SPECIALIST_HEADINGS = {
    "opening": (
        "## Opening Strategy",
        "## Relevant Prose Controls",
        "## Relevant Plan",
    ),
    "dialogue": (
        "## Relevant Characters and Relationships",
        "## Relevant Prose Controls",
        "## Relevant Plan",
    ),
    "action": (
        "## Relevant World Rules",
        "## Relevant Plan",
        "## Relevant Characters and Relationships",
    ),
    "emotion": (
        "## Relevant Characters and Relationships",
        "## Relevant Open Promises",
        "## Relevant Prose Controls",
    ),
}


@dataclass(frozen=True)
class CuratorContextPacket:
    authority: str
    chapter_mission: str
    book_contract: str
    canon_index: str
    rolling_plan: str
    prose_profile: str
    optional_inspiration: str
    growth_benefit_projection: str
    transition_context: str


@dataclass(frozen=True)
class SpecialistContextPacket:
    specialist: str
    chapter_mission: str
    primary_draft: str
    relevant_curated_context: str
    growth_benefit_projection: str
    transition_context: str


@dataclass(frozen=True)
class IntegratorContextPacket:
    authority: str
    chapter_mission: str
    canon_prose: str
    canon_index: str
    curated_context: str
    primary_draft: str
    growth_benefit_projection: str
    specialist_responses: Mapping[str, str]


@dataclass
class HybridChapterArtifacts:
    curator_response: str = ""
    primary_response: str = ""
    specialist_responses: dict[str, str] = field(default_factory=dict)
    integrator_response: str = ""
    selected_body: str = ""
    fact_summary: str = ""


def _extract_level_one_section(content: str, heading: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1 :]:
            stripped = next_line.strip()
            if stripped.startswith("# "):
                break
            collected.append(next_line)
        return "\n".join(collected).strip()
    return ""


def _extract_subsection(content: str, heading: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1 :]:
            stripped = next_line.strip()
            if stripped.startswith("## ") or stripped.startswith("# "):
                break
            collected.append(next_line)
        return "\n".join(collected).strip()
    return ""


def drop_growth_hierarchy(book_contract: str) -> str:
    """从章节上下文中移除完整成长基因图，只保留其它 BOOK Contract 区块。"""

    lines = book_contract.splitlines()
    kept: list[str] = []
    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## 0. 本书成长基因图":
            skipping = True
            continue
        if skipping and stripped.startswith("## "):
            skipping = False
        if not skipping:
            kept.append(line)
    return "\n".join(kept).strip()


def extract_last_transition_context(text: str, max_chars: int = 1800) -> str:
    """保留前文最后几个完整段落，作为章首的必要衔接片段。"""

    clean = text.strip()
    if not clean:
        return "（无前文章末衔接片段。）"
    if len(clean) <= max_chars:
        return clean
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", clean) if part.strip()]
    selected: list[str] = []
    size = 0
    for paragraph in reversed(paragraphs):
        added = len(paragraph) + (2 if selected else 0)
        if selected and size + added > max_chars:
            break
        if not selected and len(paragraph) > max_chars:
            return paragraph[-max_chars:]
        selected.insert(0, paragraph)
        size += added
    return "\n\n".join(selected) or clean[-max_chars:]


def extract_opening_strategy(book_content: str) -> str:
    """从 BOOK §7 提取作者明确选择的第一章开篇策略。"""

    lines = book_content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "### 第一章开篇策略":
            continue
        collected: list[str] = []
        for next_line in lines[index + 1 :]:
            stripped = next_line.strip()
            if stripped.startswith("### ") or stripped.startswith("## ") or stripped.startswith("# "):
                break
            collected.append(next_line)
        return "\n".join(collected).strip() or "（BOOK 未填写第一章开篇策略。）"
    return "（BOOK 未填写第一章开篇策略。）"


def extract_primary_draft(response: str) -> str:
    return _extract_level_one_section(response, "# Primary Draft")


def extract_primary_fact_summary(response: str) -> str:
    return _extract_level_one_section(response, "# Primary Fact Summary")


def extract_final_chapter_artifact(response: str) -> tuple[str, str] | None:
    body = _extract_level_one_section(response, "# 正式正文")
    if not body:
        return None
    return body, _extract_level_one_section(response, "# 章节事实摘要")


def count_specialist_patches(response: str) -> int:
    return len(re.findall(r"^##\s+Patch\s+\d+\s*$", response, flags=re.MULTILINE))


def build_curator_context(packet: ChapterContextPacket) -> CuratorContextPacket:
    return CuratorContextPacket(
        authority=packet.authority,
        chapter_mission=packet.chapter_mission,
        book_contract=drop_growth_hierarchy(packet.book_contract),
        canon_index=packet.canon_context,
        rolling_plan=packet.rolling_plan,
        prose_profile=packet.prose_profile,
        optional_inspiration=packet.optional_inspiration,
        growth_benefit_projection=packet.growth_benefit_projection,
        transition_context=extract_last_transition_context(packet.recent_prose),
    )


def _relevant_curated_context(curated_response: str, specialist: str) -> str:
    headings = _SPECIALIST_HEADINGS.get(specialist)
    if not headings:
        raise ValueError(f"未知专项 Agent：{specialist}")
    blocks = []
    for heading in headings:
        body = _extract_subsection(curated_response, heading)
        if body:
            blocks.append(f"{heading}\n\n{body}")
    if blocks:
        return "\n\n".join(blocks)
    return "（Curator 未提供与本专项对应的局部上下文。）"


def build_specialist_context(
    packet: ChapterContextPacket,
    curated_response: str,
    primary_draft: str,
    specialist: str,
) -> SpecialistContextPacket:
    if specialist not in SPECIALIST_NAMES:
        raise ValueError(f"未知专项 Agent：{specialist}")
    return SpecialistContextPacket(
        specialist=specialist,
        chapter_mission=packet.chapter_mission,
        primary_draft=primary_draft,
        relevant_curated_context=_relevant_curated_context(curated_response, specialist),
        growth_benefit_projection=packet.growth_benefit_projection,
        transition_context=extract_last_transition_context(packet.recent_prose),
    )


def build_integrator_context(
    packet: ChapterContextPacket,
    curated_response: str,
    primary_draft: str,
    specialist_responses: Mapping[str, str],
) -> IntegratorContextPacket:
    responses = {
        name: specialist_responses.get(name, "").strip() or "未提供"
        for name in SPECIALIST_NAMES
    }
    return IntegratorContextPacket(
        authority=packet.authority,
        chapter_mission=packet.chapter_mission,
        canon_prose=packet.recent_prose,
        canon_index=packet.canon_context,
        curated_context=curated_response.strip() or "（Curator 未提供，使用完整上下文。）",
        primary_draft=primary_draft,
        growth_benefit_projection=packet.growth_benefit_projection,
        specialist_responses=responses,
    )
