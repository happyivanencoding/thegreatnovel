"""Hybrid chapter runtime 的确定性上下文和产物辅助函数。

这个模块只负责把已经存在的 ChapterContextPacket 投影成各节点需要的
局部文本，以及从作者可见的模型返回中提取正式区块。它不调用模型、写文件
或调度节点。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Mapping

from .chapter_context import ChapterContextPacket, project_event_contract_for_prose


SPECIALIST_NAMES = ("opening", "dialogue", "action", "emotion")

_SPECIALIST_HEADINGS = {
    "opening": (
        "## Opening Strategy",
        "## Relevant Prose Controls",
        "## Relevant Plan",
        "## Reader-Facing Language",
    ),
    "dialogue": (
        "## Relevant Characters and Relationships",
        "## Relevant Prose Controls",
        "## Relevant Plan",
        "## Reader-Facing Language",
    ),
    "action": (
        "## Relevant World Rules",
        "## Relevant Plan",
        "## Relevant Characters and Relationships",
        "## Reader-Facing Language",
    ),
    "emotion": (
        "## Relevant Characters and Relationships",
        "## Relevant Open Promises",
        "## Relevant Prose Controls",
        "## Reader-Facing Language",
    ),
}


@dataclass(frozen=True)
class CuratorContextPacket:
    authority: str
    chapter_mission: str
    book_contract: str
    growth_genome_compact: str
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


def compact_book_contract_for_chapter(
    book_contract: str, growth_genome_compact: str
) -> str:
    """用固定 §0 压缩投影替换完整成长基因图。"""

    remainder = drop_growth_hierarchy(book_contract)
    compact = growth_genome_compact.strip()
    if not compact:
        return remainder
    return "\n\n".join(part for part in (compact, remainder) if part).strip()


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


def _extract_front_context(text: str, max_chars: int) -> str:
    clean = text.strip()
    if len(clean) <= max_chars:
        return clean
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", clean) if part.strip()]
    selected: list[str] = []
    size = 0
    for paragraph in paragraphs:
        added = len(paragraph) + (2 if selected else 0)
        if selected and size + added > max_chars:
            break
        if not selected and len(paragraph) > max_chars:
            return paragraph[:max_chars]
        selected.append(paragraph)
        size += added
    return "\n\n".join(selected) or clean[:max_chars]


def _extract_dialogue_context(text: str, max_chars: int = 3600) -> str:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    if not paragraphs:
        return ""
    dialogue_pattern = re.compile(r"[“”「」『』]|(?:^|\n)\s*[^\n]{0,30}[：:]\s*[^\n]+")
    selected_indexes: set[int] = set()
    for index, paragraph in enumerate(paragraphs):
        if dialogue_pattern.search(paragraph):
            selected_indexes.update({index - 1, index, index + 1})
    selected = [paragraphs[index] for index in sorted(selected_indexes) if 0 <= index < len(paragraphs)]
    if not selected:
        return _extract_front_context(text, max_chars)
    return _extract_front_context("\n\n".join(selected), max_chars)


def extract_primary_prose_context(text: str, previous_tail_chars: int = 1800) -> str:
    """Primary Writer 保留上一章全文；上上章仅保留必要章末片段。"""

    clean = text.strip()
    markers = list(re.finditer(r"(?m)^#\s*\d+章正文\s*$", clean))
    if len(markers) < 2:
        return clean
    previous_start = markers[-2].start()
    current_start = markers[-1].start()
    previous = clean[previous_start:current_start].strip()
    current = clean[current_start:].strip()
    return "\n\n".join(
        part for part in (extract_last_transition_context(previous, previous_tail_chars), current) if part
    )


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


def extract_specialist_patches(response: str) -> str:
    """只提取有效 Patch，排除 Specialist Audit 和其它整段建议。"""

    if count_specialist_patches(response) == 0:
        # 正式 Specialist 合同总会带有「# Proposed Patches」；没有该合同的
        # 手工粘贴只作为可见原文保留，真正的 Ledger 运行会把无 Patch 合同视为无效。
        return response.strip() if "# Proposed Patches" not in response else ""
    lines = response.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.strip() == "# Proposed Patches"),
        None,
    )
    if start is None:
        return ""
    collected = [lines[start]]
    for line in lines[start + 1 :]:
        if line.startswith("# "):
            break
        if line.strip().startswith("## Patch ") or collected[-1].strip().startswith("## Patch "):
            collected.append(line)
        elif any(item.strip().startswith("## Patch ") for item in collected):
            collected.append(line)
    return "\n".join(collected).strip()


def has_valid_specialist_patches(responses: Mapping[str, str]) -> bool:
    return any(extract_specialist_patches(response) for response in responses.values())


def build_curator_context(packet: ChapterContextPacket) -> CuratorContextPacket:
    compact = packet.growth_genome_compact
    if not any(
        heading in compact
        for heading in ("### 作者明确保留", "### 核心不变量", "### 退化风险")
    ):
        compact = "（旧 BOOK 未提供 Growth Genome 的三个章节压缩小节。）"
    return CuratorContextPacket(
        authority=packet.authority,
        chapter_mission=packet.chapter_mission,
        book_contract=drop_growth_hierarchy(packet.book_contract),
        growth_genome_compact=compact,
        canon_index=packet.canon_context,
        rolling_plan=packet.chapter_plan_context or packet.rolling_plan,
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
    if specialist == "opening":
        projected_draft = _extract_front_context(primary_draft, 1800)
    elif specialist == "dialogue":
        projected_draft = _extract_dialogue_context(primary_draft)
    elif specialist == "emotion":
        projected_draft = extract_last_transition_context(primary_draft, 2500)
    else:
        projected_draft = primary_draft
    return SpecialistContextPacket(
        specialist=specialist,
        chapter_mission=project_event_contract_for_prose(packet.chapter_mission),
        primary_draft=projected_draft,
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
        name: extract_specialist_patches(specialist_responses.get(name, "")) or "无有效 Patch（未提供）"
        for name in SPECIALIST_NAMES
    }
    return IntegratorContextPacket(
        authority=packet.authority,
        chapter_mission=project_event_contract_for_prose(packet.chapter_mission),
        canon_prose=extract_last_transition_context(packet.recent_prose),
        canon_index=packet.canon_context,
        curated_context=curated_response.strip() or "（Curator 未提供，使用完整上下文。）",
        primary_draft=primary_draft,
        growth_benefit_projection=packet.growth_benefit_projection,
        specialist_responses=responses,
    )
