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
        "## Scene Prose Projection",
        "## Relevant Prose Controls",  # legacy Curator output compatibility
        "## Relevant Plan",
        "## Reader-Facing Language",
    ),
    "dialogue": (
        "## Relevant Characters and Relationships",
        "## Scene Prose Projection",
        "## Relevant Prose Controls",  # legacy Curator output compatibility
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
        "## Scene Prose Projection",
        "## Relevant Prose Controls",  # legacy Curator output compatibility
        "## Reader-Facing Language",
    ),
}


@dataclass(frozen=True)
class CuratorContextPacket:
    authority: str
    chapter_mission: str
    context_index: str
    world_authority: str
    human_core: str
    book_contract: str
    growth_genome_compact: str
    canon_index: str
    rolling_plan: str
    prose_profile: str
    optional_inspiration: str
    growth_benefit_projection: str
    transition_context: str
    reader_release: str = ""


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


def strip_legacy_prose_controls(curated_response: str) -> str:
    """Primary 不再接收旧版完整 Prose Control 区块。

    新 Curator 应输出 `## Scene Prose Projection`。对历史 response 保持其它区块兼容，
    但确定性删除 `## Relevant Prose Controls`，避免完整方法论重新进入 Writer。
    """

    lines = curated_response.splitlines()
    kept: list[str] = []
    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## Relevant Prose Controls":
            skipping = True
            continue
        if skipping and (stripped.startswith("## ") or stripped.startswith("# ")):
            skipping = False
        if not skipping:
            kept.append(line)
    return "\n".join(kept).strip()


_UNRESOLVED_MARKERS = (
    "未知",
    "未确认",
    "未解释",
    "未兑现",
    "未解决",
    "未明确",
    "不明",
    "尚未",
    "真假",
    "不要补造",
    "无法确认",
    "无法判断",
    "不提供",
)


def extract_unresolved_fact_boundary(curated_response: str) -> str:
    """把 Curator 已识别的未解事实提升到 Primary 的高显著事实边界。

    这是确定性投影，不做语义推断、不调用模型。Open Promises 全量保留；
    Audit / World Rules / Payoff Window 只保留明确带未知标记的行，避免把
    整份 Curated Context 再复制一遍。
    """

    sections: list[str] = []
    audit = _extract_level_one_section(curated_response, "# Curator Audit")
    if audit and "无需要报告" not in audit:
        audit_lines = [
            line.strip()
            for line in audit.splitlines()
            if line.strip() and any(marker in line for marker in _UNRESOLVED_MARKERS)
        ]
        if audit_lines:
            sections.append("## Curator Uncertainty\n" + "\n".join(audit_lines))

    promises = _extract_subsection(curated_response, "## Relevant Open Promises")
    if promises and promises.strip() != "无":
        sections.append("## Open Promises\n" + promises)

    for heading, label in (
        ("## Relevant World Rules", "## Unresolved World / Mechanism Facts"),
        ("## Payoff and Promise Window", "## Still Unresolved / Not Yet Paid Off"),
    ):
        body = _extract_subsection(curated_response, heading)
        lines = [
            line.strip()
            for line in body.splitlines()
            if line.strip() and any(marker in line for marker in _UNRESOLVED_MARKERS)
        ]
        if lines:
            sections.append(label + "\n" + "\n".join(lines))

    return "\n\n".join(sections).strip()


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
    """读取新版 Primary 正文，同时兼容旧三段式 Primary 返回。"""

    body = _extract_level_one_section(response, "# 正式正文")
    if body:
        return body
    # ACP/外部执行器偶尔会把一句模型前言和标题粘在同一行。
    # 标题本身仍是明确正文边界时，确定性丢弃标题前模型自述。
    marker = "# 正式正文"
    if marker in response:
        normalized = marker + "\n" + response.split(marker, 1)[1].lstrip()
        body = _extract_level_one_section(normalized, marker)
        if body:
            return body
    body = _extract_level_one_section(response, "# Primary Draft")
    if body:
        return body
    legacy_marker = "# Primary Draft"
    if legacy_marker in response:
        normalized = legacy_marker + "\n" + response.split(legacy_marker, 1)[1].lstrip()
        body = _extract_level_one_section(normalized, legacy_marker)
        if body:
            return body
    clean = response.strip()
    if not clean or re.search(
        r"(?m)^#\s+(?:Primary Writer Audit|Primary Fact Summary|Writer Audit|章节事实摘要)\s*$",
        clean,
    ):
        return ""
    # 手工/外部执行器可以只返回纯正文；没有 pipeline 标题时整段视为正文。
    return clean


def extract_primary_fact_summary(response: str) -> str:
    """仅兼容旧 Run；新版 Primary 不再生成事实摘要。"""

    return _extract_level_one_section(response, "# Primary Fact Summary")


def _context_directory(label: str, text: str) -> str:
    """只暴露结构标题，不复制正文；供 Curator 先定位再读取确定性预取。"""

    headings = [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^#{2,3}\s+", line.strip())
    ]
    if not headings:
        return f"{label}: （无结构标题）"
    return "\n".join([f"{label}:", *(f"- {heading}" for heading in headings)])


def _relevance_terms(text: str) -> set[str]:
    """用中文三字片段和英文词做轻量确定性相关性，不调用模型或检索服务。"""

    terms: set[str] = set()
    for token in re.findall(r"[A-Za-z0-9_]{3,}|[\u4e00-\u9fff]{3,}", text.casefold()):
        if re.fullmatch(r"[\u4e00-\u9fff]+", token):
            if len(token) <= 6:
                terms.add(token)
            terms.update(token[index : index + 3] for index in range(len(token) - 2))
        else:
            terms.add(token)
    return terms


def _project_indexed_text(text: str, query: str, *, max_chars: int) -> str:
    """Index-first 的确定性正文预取：每个结构块保留入口，再补相关段落。"""

    clean = text.strip()
    if not clean or len(clean) <= max_chars:
        return clean
    query_terms = _relevance_terms(query)
    raw_sections = re.split(r"(?m)(?=^##\s+)", clean)
    sections = [section.strip() for section in raw_sections if section.strip()]
    if not sections:
        return clean[:max_chars].rstrip()

    parsed: list[tuple[str, list[str]]] = []
    candidates: list[tuple[int, int, int, str]] = []
    for section_index, section in enumerate(sections):
        lines = section.splitlines()
        heading = lines[0].strip() if lines and lines[0].lstrip().startswith("## ") else ""
        body = "\n".join(lines[1:] if heading else lines).strip()
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        parsed.append((heading, paragraphs))
        for paragraph_index, paragraph in enumerate(paragraphs[1:], start=1):
            score = len(query_terms & _relevance_terms(paragraph))
            if score:
                candidates.append((score, section_index, paragraph_index, paragraph))

    selected: dict[int, set[int]] = {}
    used = 0
    for section_index, (heading, paragraphs) in enumerate(parsed):
        base_cost = len(heading) + 2
        selected.setdefault(section_index, set())
        if paragraphs:
            first = paragraphs[0]
            if len(first) > 700:
                first = first[:700].rstrip() + "…"
                paragraphs[0] = first
            base_cost += len(first) + 2
            selected[section_index].add(0)
        if used + base_cost <= max_chars or section_index == 0:
            used += base_cost
        else:
            selected.pop(section_index, None)

    for _, section_index, paragraph_index, paragraph in sorted(
        candidates, key=lambda item: (-item[0], item[1], item[2])
    ):
        if section_index not in selected or paragraph_index in selected[section_index]:
            continue
        extra = min(len(paragraph), 1200) + 2
        if used + extra > max_chars:
            continue
        selected[section_index].add(paragraph_index)
        used += extra

    rendered: list[str] = []
    for section_index, (heading, paragraphs) in enumerate(parsed):
        indexes = selected.get(section_index)
        if indexes is None:
            continue
        section_parts = [heading] if heading else []
        for paragraph_index in sorted(indexes):
            paragraph = paragraphs[paragraph_index]
            if len(paragraph) > 1200:
                paragraph = paragraph[:1200].rstrip() + "…"
            section_parts.append(paragraph)
        if len(indexes) < len(paragraphs):
            section_parts.append("（其余段落未进入本章确定性预取。）")
        rendered.append("\n\n".join(part for part in section_parts if part))
    return "\n\n".join(rendered).strip()


def _project_relevant_world_authority(text: str, query: str, *, max_chars: int = 4200) -> str:
    """Select only world paragraphs explicitly relevant to the current planned chapter.

    Unlike generic BOOK prefetch, this does not keep section lead paragraphs by
    default. Outline is the release scheduler: if the current chapter plan does not
    name or paraphrase a world fact, that fact should not become prose material merely
    because it exists somewhere in World Vision.
    """

    clean = text.strip()
    query_terms = _relevance_terms(query)
    if not clean or not query_terms:
        return ""

    sections = [
        section.strip()
        for section in re.split(r"(?m)(?=^##\s+)", clean)
        if section.strip()
    ]
    candidates: list[tuple[int, int, int, str, str]] = []
    for section_index, section in enumerate(sections):
        lines = section.splitlines()
        heading = lines[0].strip() if lines and lines[0].lstrip().startswith("## ") else ""
        body = "\n".join(lines[1:] if heading else lines).strip()
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        heading_score = len(query_terms & _relevance_terms(heading))
        for paragraph_index, paragraph in enumerate(paragraphs):
            score = heading_score + len(query_terms & _relevance_terms(paragraph))
            if score:
                candidates.append((score, section_index, paragraph_index, heading, paragraph))

    if not candidates:
        return ""

    selected: list[tuple[int, int, str, str]] = []
    used = 0
    for _, section_index, paragraph_index, heading, paragraph in sorted(
        candidates, key=lambda item: (-item[0], item[1], item[2])
    ):
        extra = len(heading) + len(paragraph) + 4
        if selected and used + extra > max_chars:
            continue
        selected.append((section_index, paragraph_index, heading, paragraph))
        used += extra
        if len(selected) >= 5:
            break

    rendered: list[str] = []
    last_heading = ""
    for _, _, heading, paragraph in sorted(selected, key=lambda item: (item[0], item[1])):
        if heading and heading != last_heading:
            rendered.append(heading)
            last_heading = heading
        rendered.append(paragraph)
    return "\n\n".join(rendered).strip()


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
        for heading in ("### 已批准幻想不变量", "### 作者明确保留", "### 核心不变量", "### 退化风险")
    ):
        compact = "（旧 BOOK 未提供 Growth Genome 的三个章节压缩小节。）"
    full_book_contract = drop_growth_hierarchy(packet.book_contract)
    relevance_query = "\n\n".join(
        part
        for part in (
            packet.chapter_mission,
            packet.chapter_plan_context,
            packet.reader_release,
            packet.growth_benefit_projection,
            extract_last_transition_context(packet.recent_prose, 1200),
        )
        if part.strip()
    )
    context_index = "\n\n".join(
        (
            _context_directory("WORLD AUTHORITY", packet.world_authority),
            _context_directory("FROZEN HUMAN CORE", packet.human_core),
            _context_directory("BOOK CONTRACT", full_book_contract),
            _context_directory("CANON INDEX", packet.canon_context),
            _context_directory("PROSE PROFILE", packet.prose_profile),
        )
    )
    return CuratorContextPacket(
        authority=packet.authority,
        chapter_mission=packet.chapter_mission,
        context_index=context_index,
        world_authority=_project_relevant_world_authority(
            packet.world_authority,
            "\n\n".join(
                part
                for part in (
                    packet.reader_release,
                    packet.chapter_mission if packet.reader_release else packet.current_chapter_plan,
                )
                if part.strip()
            ),
        ),
        reader_release=packet.reader_release,
        human_core=packet.human_core,
        book_contract=_project_indexed_text(
            full_book_contract, relevance_query, max_chars=6200
        ),
        growth_genome_compact=compact,
        canon_index=_project_indexed_text(
            packet.canon_context, relevance_query, max_chars=5200
        ),
        rolling_plan=packet.chapter_plan_context or packet.rolling_plan,
        prose_profile=packet.prose_profile,
        optional_inspiration=_project_indexed_text(
            packet.optional_inspiration, relevance_query, max_chars=3200
        ),
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
