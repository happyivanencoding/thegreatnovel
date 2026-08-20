from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from .gbrain import GBrainQueryError, NOVEL_GBRAIN_SCOPE, get_gbrain, query_gbrain


RAW_RESULT_LIMIT = 8
# Hermes query scope selects the novel distilled domain before candidate limits.
QUERY_RECALL_LIMIT = 24
FINAL_RESULT_LIMIT = 5
#: Chapter Runtime Lite v1：chapter 模式灵感负担减半，最多 2 条；其他模式不受影响。
CHAPTER_FINAL_RESULT_LIMIT = 2
GENRE_PRIOR_ACCEPT_LIMIT = 2
EMPTY_RESULT = "（本次没有找到与 BOOK 硬约束和当前章节任务兼容的 GBrain 证据；不要用不相关材料补位。）"
GBRAIN_SCOPE_LABEL = "修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选"

SOURCE_CATEGORIES = frozenset(
    {"mechanisms", "contrasts", "syntheses", "prose-controls", "book-dna", "prose-dna", "maps", "arcs"}
)
MODE_ALLOWED_CATEGORIES = {
    "idea": SOURCE_CATEGORIES,
    "outline": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls", "book-dna", "arcs"}),
    "chapter_prep": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "chapter": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "context_curator": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "primary_writer": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "specialist_opening": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "specialist_dialogue": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "specialist_action": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "specialist_emotion": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "chapter_integrator": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
    "review": frozenset({"mechanisms", "contrasts", "syntheses", "prose-controls"}),
}

GENRE_PRIOR_ALLOWED_MODES = frozenset({"idea", "outline", "review"})

CONSTRAINT_PATTERNS = (
    ("现实世界", ("现实世界", "现代都市", "现实职业", "现代社会")),
    ("无超自然", ("超自然", "魔法", "法术", "异能", "系统奇迹")),
    ("无修炼体系", ("修炼体系", "修炼", "修真", "修仙")),
    ("无战斗升级", ("战斗升级", "战力升级", "武科")),
    ("无学院试炼", ("学院试炼",)),
    ("无遗迹", ("遗迹",)),
    ("无副本", ("副本",)),
    ("无异世界", ("异世界",)),
)

FORBIDDEN_SURFACES = {
    "无超自然": ("超自然", "魔法", "法术", "异能", "系统奇迹"),
    "无修炼体系": ("修真", "修仙", "修炼", "修士", "境界", "功法", "灵气", "宗门"),
    "无战斗升级": ("战力升级", "战斗升级", "武科"),
    "无学院试炼": ("学院试炼",),
    "无遗迹": ("遗迹",),
    "无副本": ("副本",),
    "无异世界": ("异世界",),
}

ABSTRACT_HEADINGS = {
    "creative problem",
    "local creative problem",
    "setup",
    "reader promise",
    "promise",
    "mechanism",
    "reader payoff",
    "when not to use",
    "transfer boundary",
    "action-space change",
    "action space effect",
    "action-space effect",
    "progression",
    "payoff",
    "future opening",
    "aftermath",
    "verification",
    "optional pressure / cost",
    "optional pressure/cost",
    "protagonist action",
    "repeatable reader loop",
    "core progression grammar",
    "advantage / special capability",
    "world expansion grammar",
    "resource / economy",
    "social / relationship dynamics",
    "novelty / recombination",
    "long-form sustainability",
    "optional constraints / costs",
    "payoff grammar",
    "failure modes",
    "failure risks",
    "anti-repetition",
    "anti-repetition notes",
    "future opening",
    "guidance",
    "control",
    "when to use",
    "variants",
    "applicability conditions",
    "shared creative problem",
    "solution a/b/c",
    "reader experience differences",
    "tradeoffs",
    "shared tendencies",
    "major divergences",
    "what this sample cannot tell us",
    "证据范围",
    "共享趋势",
    "主要分歧",
    "机制",
    "读者回报",
    "使用边界",
    "适用时",
    "失败信号",
    "适用范围与权威",
    "核心读者满足",
    "常见一级成长主轴",
    "常见二级收益",
    "主要情节发动机",
    "常见开局方式",
    "常见兑现形式",
    "reader-facing language",
    "长篇变异方向",
    "常见退化风险",
    "不应默认",
}
EXCLUDED_SECTION_WORDS = ("evidence", "证据", "sampling", "支持范围")

_HIT_PATTERN = re.compile(
    r"^\s*\[(?P<score>-?(?:\d+(?:\.\d+)?|\.\d+))\]\s+(?P<slug>\S+)\s+--\s*(?P<snippet>.*?)\s*$"
)


def _compact(value: str, limit: int) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def _markdown_block(content: str, heading: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1:]:
            stripped = next_line.strip()
            if stripped.startswith("# ") or stripped.startswith("## "):
                break
            collected.append(next_line)
        return "\n".join(collected).strip()
    return ""


def extract_hard_constraints(*texts: str) -> list[str]:
    combined = "\n".join(text for text in texts if text).strip()
    constraints = []
    for label, phrases in CONSTRAINT_PATTERNS:
        if label == "现实世界":
            matched = any(phrase in combined for phrase in phrases)
        else:
            matched = any(
                re.search(
                    rf"(?:无|没有|不使用|不含|禁止|不得|不要)[^。；;\n]{{0,20}}{re.escape(phrase)}",
                    combined,
                )
                for phrase in phrases
            )
        if matched:
            constraints.append(label)
    return constraints


def _book_signal(book_content: str) -> str:
    headings = (
        "## 0. 本书成长基因图",
        "## 1. 核心类型与读者承诺",
        "## 2. 世界观结构",
        "## 3. 世界如何持续制造剧情压力",
        "## 4. 主角模型、人物弧与核心矛盾",
        "## 5. 配角与关系系统",
        "## 6. 核心情节发动机",
    )
    blocks = [f"{heading}\n{_compact(_markdown_block(book_content, heading), 550)}" for heading in headings]
    blocks = [block for block in blocks if block.split("\n", 1)[1]]
    if blocks:
        return "\n\n".join(blocks)
    return _compact(book_content, 1800)


def build_retrieval_brief(
    *,
    mode: str,
    book_content: str = "",
    creative_direction: str = "",
    current_long_block: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
) -> str:
    constraints = extract_hard_constraints(
        creative_direction,
        book_content,
        current_long_block,
        current_outline,
        recent_summaries,
    )
    lines = [f"检索模式：{mode}"]
    if creative_direction.strip():
        lines.append(f"作者当前方向：{_compact(creative_direction, 500)}")
    if book_content.strip():
        lines.append(f"BOOK 关键事实与成长上下文：\n{_compact(_book_signal(book_content), 2200)}")
    if current_long_block.strip():
        lines.append(f"当前大型剧情块：\n{_compact(current_long_block, 900)}")
    if current_outline.strip():
        lines.append(f"当前章任务：\n{_compact(current_outline, 1000)}")
    if recent_summaries.strip():
        lines.append(f"最近章节摘要：\n{_compact(recent_summaries, 500)}")
    lines.append(f"明确硬约束：{'、'.join(constraints) if constraints else '未检测到明确题材硬约束'}")
    if mode in {
        "chapter_prep",
        "chapter",
        "context_curator",
        "primary_writer",
        "specialist_opening",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
        "chapter_integrator",
        "review",
    }:
        lines.append("章节精度优先：寻找可迁移的 mechanisms、contrasts、syntheses、prose-controls；不引入来源作品表层故事。")
    elif mode == "outline":
        lines.append("规划用途：允许较广的 Book DNA、Arc、Mechanism、Contrast、Synthesis，但必须服从上述明确硬约束。")
    else:
        lines.append("创意用途：允许寻找不同成长玩法，但仍不得违反上述明确硬约束。")
    return "\n".join(lines).strip()


def parse_query_results(stdout: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        match = _HIT_PATTERN.match(line)
        if not match:
            continue
        results.append(
            {
                "score": float(match.group("score")),
                "slug": match.group("slug"),
                "snippet": match.group("snippet"),
            }
        )
    return results


def source_category(slug: str) -> str:
    return slug.split("/", 1)[0].strip().lower()


def _forbidden_terms(constraints: Iterable[str]) -> tuple[str, ...]:
    terms: list[str] = []
    for constraint in set(constraints):
        terms.extend(FORBIDDEN_SURFACES.get(constraint, ()))
    return tuple(dict.fromkeys(terms))


def _has_surface_conflict(text: str, constraints: Iterable[str]) -> bool:
    return any(term in text for term in _forbidden_terms(constraints))


def _parse_markdown_sections(content: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_lines: list[str] = []

    def save() -> None:
        if current_heading:
            sections.append((current_heading, "\n".join(current_lines).strip()))

    for line in content.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            save()
            current_heading = match.group(1).strip()
            current_lines = []
        elif current_heading:
            current_lines.append(line)
    save()
    return sections


def extract_abstract_content(page: str) -> tuple[str, str]:
    selected: list[tuple[str, str]] = []
    boundary = ""
    for heading, body in _parse_markdown_sections(page):
        normalized = heading.casefold().replace("：", ":").strip()
        if any(word in normalized for word in EXCLUDED_SECTION_WORDS):
            continue
        if normalized not in ABSTRACT_HEADINGS or not body:
            continue
        cleaned_lines = []
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("source_", "source-book", "evidence_", "Evidence ", "证据")):
                continue
            cleaned_lines.append(stripped)
        cleaned = "\n".join(cleaned_lines).strip()
        if not cleaned:
            continue
        if normalized in {"transfer boundary", "使用边界"}:
            boundary = _compact(cleaned, 500)
        else:
            selected.append((heading, _compact(cleaned, 800)))
    if not selected:
        return "", boundary
    abstract = "\n".join(f"{heading}：{body}" for heading, body in selected)
    return _compact(abstract, 800), boundary


def is_genre_prior_page(page: str) -> bool:
    """只依据现有卡片 frontmatter 的 creative_problem_tags 识别题材先验。"""

    lines = page.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        return False
    return any("genre-prior" in line.casefold() for line in lines[1:end])


def _genre_prior_title(page: str, slug: str) -> str:
    lines = page.splitlines()
    for line in lines:
        if line.casefold().startswith("title:"):
            return line.split(":", 1)[1].strip()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return slug.rsplit("/", 1)[-1]


def genre_prior_matches_query(page: str, query: str, slug: str) -> bool:
    """题材先验只在 query 明确提到其标题/别名时占用先验名额。"""

    title = _genre_prior_title(page, slug)
    candidates = [part.strip() for part in re.split(r"[｜|/、，,\s]+", title) if len(part.strip()) >= 2]
    if not candidates:
        return False
    normalized_query = query.casefold()
    return any(candidate.casefold() in normalized_query for candidate in candidates)


def _type_for_category(category: str) -> str:
    return {
        "mechanisms": "mechanism",
        "contrasts": "contrast",
        "syntheses": "synthesis",
        "prose-controls": "prose-control",
    }.get(category, category)


def _format_bundle(items: list[Mapping[str, Any]]) -> str:
    if not items:
        return EMPTY_RESULT
    blocks = []
    for index, item in enumerate(items, start=1):
        boundary = item.get("transfer_boundary") or "只迁移当前卡片的抽象机制，不迁移来源人物、事件、专名、世界设定或句式。"
        blocks.append(
            "\n".join(
                [
                    f"### Inspiration {index}",
                    f"source: {item['slug']}",
                    f"type: {item['type']}",
                    f"score: {item['score']:g}",
                    "",
                    f"可用抽象：{item['abstract']}",
                    "",
                    f"使用边界：{boundary}",
                ]
            )
        )
    return "\n\n".join(blocks)


def retrieve_gbrain(
    *,
    mode: str,
    book_content: str = "",
    creative_direction: str = "",
    current_long_block: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
    query_override: str = "",
    query_func: Callable[..., str] | None = None,
    page_func: Callable[[str], str] | None = None,
) -> dict[str, Any]:
    if mode not in MODE_ALLOWED_CATEGORIES:
        raise ValueError(f"未知 GBrain 检索模式：{mode}")
    retrieval_brief = build_retrieval_brief(
        mode=mode,
        book_content=book_content,
        creative_direction=creative_direction,
        current_long_block=current_long_block,
        current_outline=current_outline,
        recent_summaries=recent_summaries,
    )
    effective_query = query_override.strip() or retrieval_brief
    query_runner = query_func or query_gbrain
    page_reader = page_func or get_gbrain
    stdout = query_runner(effective_query, limit=QUERY_RECALL_LIMIT, detail="medium")
    parsed = parse_query_results(stdout)
    constraints = extract_hard_constraints(
        creative_direction,
        book_content,
        current_long_block,
        current_outline,
        recent_summaries,
    )
    allowed_categories = MODE_ALLOWED_CATEGORIES[mode]
    final_limit = CHAPTER_FINAL_RESULT_LIMIT if mode == "chapter" else FINAL_RESULT_LIMIT
    novel_candidates: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for hit in parsed:
        category = source_category(hit["slug"])
        if category not in allowed_categories:
            rejected.append({"slug": hit["slug"], "reason": f"{mode} 模式不自动使用 {category or '未知来源类别'}"})
            continue
        novel_candidates.append(hit)

    visible = novel_candidates[:RAW_RESULT_LIMIT]
    rejected.extend(
        {"slug": hit["slug"], "reason": "超过小说候选数量上限"}
        for hit in novel_candidates[RAW_RESULT_LIMIT:]
    )
    accepted: list[dict[str, Any]] = []
    genre_prior_count = 0
    for hit in visible:
        category = source_category(hit["slug"])
        if _has_surface_conflict(hit["snippet"], constraints):
            rejected.append({"slug": hit["slug"], "reason": "与 BOOK 的明确硬约束冲突"})
            continue
        if len(accepted) >= final_limit:
            rejected.append({"slug": hit["slug"], "reason": "超过最终数量上限"})
            continue
        try:
            page = page_reader(hit["slug"])
        except (GBrainQueryError, OSError, ValueError):
            rejected.append({"slug": hit["slug"], "reason": "完整页面读取失败"})
            continue
        genre_prior = is_genre_prior_page(page)
        if genre_prior and mode not in GENRE_PRIOR_ALLOWED_MODES:
            rejected.append({"slug": hit["slug"], "reason": "章节节点不自动使用 Genre Prior"})
            continue
        if genre_prior and not genre_prior_matches_query(page, effective_query, hit["slug"]):
            rejected.append({"slug": hit["slug"], "reason": "Genre Prior 与当前题材 query 不相关"})
            continue
        if genre_prior and genre_prior_count >= GENRE_PRIOR_ACCEPT_LIMIT:
            rejected.append({"slug": hit["slug"], "reason": "超过 Genre Prior 接受上限"})
            continue
        abstract, transfer_boundary = extract_abstract_content(page)
        if not abstract:
            rejected.append({"slug": hit["slug"], "reason": "没有可提取的抽象区块"})
            continue
        if _has_surface_conflict(abstract, constraints):
            rejected.append({"slug": hit["slug"], "reason": "与 BOOK 的现实模式冲突"})
            continue
        accepted.append(
            {
                **hit,
                "type": _type_for_category(category),
                "is_genre_prior": genre_prior,
                "abstract": abstract,
                "transfer_boundary": transfer_boundary,
            }
        )
        if genre_prior:
            genre_prior_count += 1
    return {
        "status": "available",
        "scope": GBRAIN_SCOPE_LABEL,
        "mode": mode,
        "effective_query": effective_query,
        "retrieval_brief": retrieval_brief,
        "query_scope": NOVEL_GBRAIN_SCOPE,
        "hard_constraints": constraints,
        "raw_count": len(parsed),
        "novel_candidate_count": len(novel_candidates),
        "accepted_count": len(accepted),
        "genre_prior_count": genre_prior_count,
        "rejected_count": len(rejected),
        "query_limit": QUERY_RECALL_LIMIT,
        "requested_limit": RAW_RESULT_LIMIT,
        "final_limit": final_limit,
        "raw_stdout": stdout,
        "novel_candidates": novel_candidates,
        "raw_results": visible,
        "accepted": accepted,
        "rejected": rejected,
        "result": _format_bundle(accepted),
    }
