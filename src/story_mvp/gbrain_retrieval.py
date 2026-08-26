from __future__ import annotations

import os
import re
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from .character_context import project_character_life_context, project_character_power_baseline
from .gbrain import GBrainQueryError, NOVEL_GBRAIN_SCOPE, get_gbrain, query_gbrain


RAW_RESULT_LIMIT = 8
PLANNING_CANDIDATE_INSPECTION_LIMIT = 12
# Hermes query scope selects the novel distilled domain before candidate limits.
QUERY_RECALL_LIMIT = 24
FINAL_RESULT_LIMIT = 5
#: Chapter Runtime Lite v1：chapter 模式灵感负担减半，最多 2 条；其他模式不受影响。
CHAPTER_FINAL_RESULT_LIMIT = 2
CREATIVE_PLANNING_FINAL_RESULT_LIMIT = 3
GENRE_PRIOR_ACCEPT_LIMIT = 2
HUMAN_LANE_ORDER = ("appetite", "behavior", "relationship")
HUMAN_LANE_CANDIDATE_INSPECTION_LIMIT = 12
HUMAN_LANE_QUERIES = {
    "appetite": '"human appetite" OR "private appetite" OR "private desire" OR "non instrumental desire"',
    "behavior": '"behavior signature" OR "stable choice bias" OR "character hook" OR "protagonist as IP"',
    "relationship": '"relationship gravity" OR "relationship chemistry" OR "character autonomy" OR "reunion relationship"',
}
WORLD_COORDINATE_REFERENCE_SLUG = "syntheses/reader-facing-world-coordinates-batch-d-v3"
EMPTY_RESULT = "（本次没有找到与 BOOK 硬约束和当前章节任务兼容的 GBrain 证据；不要用不相关材料补位。）"
GBRAIN_SCOPE_LABEL = "修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选"

SOURCE_CATEGORIES = frozenset(
    {"mechanisms", "contrasts", "syntheses", "prose-controls", "book-dna", "prose-dna", "maps", "arcs"}
)
MODE_ALLOWED_CATEGORIES = {
    "world_vision": frozenset({"mechanisms", "syntheses", "book-dna"}),
    "power_seed": frozenset({"mechanisms", "syntheses", "book-dna"}),
    "human_seed": frozenset({"mechanisms", "contrasts", "syntheses", "book-dna"}),
    "idea": frozenset({"mechanisms", "contrasts", "syntheses"}),
    "outline": frozenset({"mechanisms", "contrasts", "syntheses", "book-dna", "arcs"}),
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


# GBrain 当前在没有 OPENAI_API_KEY 时会退化为 English FTS keyword-only。
# 规划节点使用少量、可检索的 v3 craft aliases；完整 BOOK-aware brief 仍单独保留给作者查看。
PLANNING_KEYWORD_QUERIES = {
    "world_vision": '"world fantasy" OR "world entry" OR "narrative compounding"',
    "power_seed": '"core fantasy" OR "asymmetric advantage" OR "power progression" OR "world compatibility"',
    "human_seed": '"character hook" OR "protagonist desire" OR "behavior signature" OR "human appetite" OR "relationship gravity"',
    "idea": '"plot engine variation" OR "thread ecology" OR "reward opportunity"',
    "outline": '"thread collision" OR "hidden identity reveal" OR "departure vacancy" OR "reunion reentry" OR "sacrifice convergence" OR "reward recontextualization"',
}

PLANNING_KEYWORD_QUERY_BATCHES = {
    "world_vision": (
        '"world fantasy" OR "world entry" OR "narrative compounding"',
        '"reader coordinates" OR "progression scale" OR "action space scale" OR "expectation ladder" OR "core advantage" OR "world compatibility" OR "power scale" OR "threat scale"',
    ),
    "power_seed": (
        '"core fantasy" OR "asymmetric advantage" OR "power progression"',
        '"world compatibility" OR "power scale" OR "growth mutation"',
    ),
    "human_seed": tuple(HUMAN_LANE_QUERIES[lane] for lane in HUMAN_LANE_ORDER),
    "idea": (
        '"plot engine variation" OR "gameplay counterplay"',
        '"thread ecology" OR "longitudinal thread" OR "thread collision"',
        '"reward opportunity"',
    ),
    "outline": (
        '"thread collision" OR "hidden identity reveal"',
        '"departure vacancy" OR "reunion reentry" OR "sacrifice convergence"',
        '"reward recontextualization" OR "action space" OR "public proof"',
    ),
}

CURATOR_PROSE_CONTROL_FALLBACK_MODES = frozenset({"context_curator"})

# When query embeddings are unavailable, keep Curator prose retrieval useful without
# adding another model call. Rules are intentionally small and scene-family based.
PROSE_CONTROL_ALIAS_RULES = (
    (("谈判", "交涉", "审问", "报价", "议价", "拒答", "多人对峙", "交易条件", "筹码"),
     '"dialogue negotiation" OR "relationship pressure"'),
    (("追逐", "追捕", "搜捕", "追杀", "突围", "围堵", "错误支路", "站位", "诱敌", "夹击", "多入口", "路线变化"),
     '"action combat" OR "spatial clarity"'),
    (("公开能力证明", "公开证明", "兑现", "大胜", "身份翻转", "获得资格", "结果已经成立", "公开认可", "余波"),
     None),
    (("奇观", "尺度", "天穹", "悬城", "世界边界", "远超既有", "巨大尺度"),
     '"scale anchored wonder" OR "world wonder"'),
    (("第一次进入", "进入陌生", "初到", "踏入", "新地点", "新空间", "陌生空间", "入口和边界", "进入新区域"),
     '"action anchored grounding" OR "scene entry exploration"'),
    (("重逢", "离别", "告别", "牺牲", "想念", "信任", "照护", "心结", "关系距离", "私人反应", "关系边界", "依赖", "疏远"),
     '"emotion relationship" OR "embodied detail"'),
    (("验证", "复现", "推断", "异常", "线索", "规律", "试压", "裂纹", "可重复", "再次出现", "仍未知", "未验证"),
     '"evidence first limited reveal" OR "discovery reveal"'),
    (("日常", "吃饭", "休息", "低压", "生活动作", "恢复期", "闲谈"),
     '"ordinary life prose" OR "embodied detail"'),
)
PROSE_CONTROL_MIN_SIGNAL_SCORE = 2
PROSE_CONTROL_COMPLEX_ACTION_QUERY = '"action combat" OR "spatial clarity"'
PROSE_CONTROL_COMPLEX_ACTION_HARD_ANCHORS = (
    "追逐", "追捕", "搜捕", "追杀", "突围", "围堵", "错误支路", "诱敌", "夹击", "多入口", "路线变化",
)

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
            matched = label in combined or any(
                re.search(
                    rf"(?:没有|不使用|不含|禁止|不得|不要)[^。；;，,：:\n]{{0,20}}{re.escape(phrase)}",
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
    world_vision: str = "",
    character_card: str = "",
    proposal_context: str = "",
    current_long_block: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
) -> str:
    effective_world = world_vision
    if mode == "power_seed" and world_vision.strip():
        effective_world = project_character_power_baseline(world_vision)
    elif mode == "human_seed" and world_vision.strip():
        effective_world = project_character_life_context(world_vision)
    constraints = extract_hard_constraints(
        creative_direction,
        effective_world,
        character_card,
        proposal_context,
        book_content,
        current_long_block,
        current_outline,
        recent_summaries,
    )
    lines = [f"检索模式：{mode}"]
    if creative_direction.strip():
        lines.append(f"作者当前方向：{_compact(creative_direction, 500)}")
    if effective_world.strip():
        label = "已批准 World Vision"
        if mode == "power_seed":
            label = "Power 可见 World Baseline"
        elif mode == "human_seed":
            label = "Human 可见 Life Context"
        lines.append(f"{label}：\n{_compact(effective_world, 1600)}")
    if character_card.strip() and mode in {"idea", "outline"}:
        lines.append(f"已批准 Character Authority：\n{_compact(character_card, 1600)}")
    if proposal_context.strip():
        lines.append(f"已批准 Story Program：\n{_compact(proposal_context, 1600)}")
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
    elif mode == "world_vision":
        lines.append("World Vision 用途：优先寻找 reader fantasy、world entry、world expansion 与 narrative compounding；只作为可选灵感，不替未来 Character 决定主角。")
    elif mode == "idea":
        lines.append("Story Program 用途：优先寻找 Plot Engine 变异、thread ecology/collision、配角自治、story-state compounding 与高价值获得体验；只作为可选灵感，不改写已批准 Character Authority / World Vision。")
    elif mode == "outline":
        lines.append("Outline 用途：优先寻找长中短线编织、身份揭露、离队归来、牺牲/二次兑现、多线合流与高价值获得/旧奖励重释；必须服从已批准 Character Authority / World Vision / Story Program。")
    else:
        lines.append("创意用途：允许寻找不同成长玩法，但仍不得违反上述明确硬约束。")
    return "\n".join(lines).strip()


def _semantic_query_available() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


def _chapter_task_from_retrieval_brief(retrieval_brief: str) -> str:
    marker = "当前章任务："
    start = retrieval_brief.find(marker)
    if start < 0:
        return retrieval_brief
    task = retrieval_brief[start + len(marker):]
    boundaries = [
        position
        for position in (
            task.find("最近章节摘要："),
            task.find("明确硬约束："),
            task.find("章节精度优先："),
        )
        if position >= 0
    ]
    if boundaries:
        task = task[: min(boundaries)]
    return task.strip()


def _positive_scene_signal_count(text: str, term: str, *, cap: int = 2) -> int:
    """Count scene terms only when they are not negated in the same short clause."""

    count = 0
    clause_breaks = "，。；;：:\n"
    negations = ("没有", "并无", "无", "未", "不是", "并非", "不含", "不存在")
    for match in re.finditer(re.escape(term), text):
        clause_start = max(text.rfind(mark, 0, match.start()) for mark in clause_breaks) + 1
        prefix = text[clause_start: match.start()]
        if any(negation in prefix for negation in negations):
            continue
        count += 1
        if count >= cap:
            break
    return count


def _chapter_prose_control_alias_query(retrieval_brief: str) -> str | None:
    """High-precision no-key fallback for Curator prose candidates.

    Only the compact current-chapter task is scored. BOOK/Growth/planning commentary
    is intentionally excluded because incidental terms there caused false routing.
    Ambiguous or weak scenes return NONE; a false negative is safer than forwarding
    the wrong prose method to the Curator.
    """

    task = _chapter_task_from_retrieval_brief(retrieval_brief)
    scored: list[tuple[int, int, str | None]] = []
    for index, (terms, query) in enumerate(PROSE_CONTROL_ALIAS_RULES):
        score = sum(_positive_scene_signal_count(task, term) for term in terms)
        if score:
            scored.append((score, index, query))
    if not scored:
        return None
    scored.sort(key=lambda item: (-item[0], item[1]))
    best_score, _best_index, best_query = scored[0]
    if best_score < PROSE_CONTROL_MIN_SIGNAL_SCORE:
        return None
    if len(scored) > 1 and scored[1][0] == best_score:
        return None
    if best_query == PROSE_CONTROL_COMPLEX_ACTION_QUERY and not any(
        _positive_scene_signal_count(task, anchor, cap=1)
        for anchor in PROSE_CONTROL_COMPLEX_ACTION_HARD_ANCHORS
    ):
        return None
    return best_query


def default_effective_query(mode: str, retrieval_brief: str) -> tuple[str, str]:
    """选择实际查询文本；不增加 LLM/reranker 调用。"""

    if not _semantic_query_available():
        if mode in PLANNING_KEYWORD_QUERIES:
            return PLANNING_KEYWORD_QUERIES[mode], "planning_keyword_aliases"
        if mode in CURATOR_PROSE_CONTROL_FALLBACK_MODES:
            alias_query = _chapter_prose_control_alias_query(retrieval_brief)
            if alias_query is None:
                return "", "prose_control_none"
            return alias_query, "prose_control_keyword_aliases"
    return retrieval_brief, "semantic_brief"


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


def dedupe_query_hits_by_slug(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """同一页面可能由多个 chunk 命中；只保留排序最靠前的一条。"""

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for hit in hits:
        slug = str(hit.get("slug", "")).strip()
        if not slug or slug in seen:
            continue
        seen.add(slug)
        unique.append(hit)
    return unique


def merge_query_hit_batches_round_robin(
    batches: list[list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """多检索意图按轮转合并，避免第一个 query 独占候选池。"""

    positions = [0 for _ in batches]
    seen: set[str] = set()
    merged: list[dict[str, Any]] = []
    while True:
        added_or_advanced = False
        for batch_index, batch in enumerate(batches):
            while positions[batch_index] < len(batch):
                hit = batch[positions[batch_index]]
                positions[batch_index] += 1
                added_or_advanced = True
                slug = str(hit.get("slug", "")).strip()
                if not slug or slug in seen:
                    continue
                seen.add(slug)
                merged.append(hit)
                break
        if not added_or_advanced:
            break
    return merged


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


def active_inspiration_allowed(page: str) -> bool:
    """显式 HOLD/Pilot exclusion；未声明的既有卡保持原行为。"""

    lines = page.splitlines()
    if not lines or lines[0].strip() != "---":
        return True
    try:
        end = lines.index("---", 1)
    except ValueError:
        return True
    for line in lines[1:end]:
        key, sep, value = line.partition(":")
        if sep and key.strip().casefold() == "active_inspiration":
            return value.strip().casefold() not in {"false", "no", "0"}
    return True


def _frontmatter_block(page: str) -> str:
    lines = page.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    try:
        end = lines.index("---", 1)
    except ValueError:
        return ""
    return "\n".join(lines[1:end])


def _explicit_human_lane(page: str) -> str:
    for line in _frontmatter_block(page).splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip().casefold() == "human_lane":
            lane = value.strip().casefold().replace("-", "_")
            aliases = {
                "appetite": "appetite",
                "human_appetite": "appetite",
                "behavior": "behavior",
                "behaviour": "behavior",
                "behavior_signature": "behavior",
                "relationship": "relationship",
                "relationship_gravity": "relationship",
            }
            return aliases.get(lane, "")
    return ""


def human_lane_for_page(page: str, slug: str = "") -> str:
    """Classify Human Craft by its own metadata, not by whichever query happened to hit it.

    New Human Craft should declare ``human_lane`` explicitly. Existing cards are
    supported through narrow frontmatter / identity markers so source text mentioning
    several human concerns cannot steal another lane.
    """

    explicit = _explicit_human_lane(page)
    if explicit:
        return explicit

    frontmatter = _frontmatter_block(page).casefold()
    identity_lines: list[str] = [slug.casefold()]
    for line in page.splitlines():
        stripped = line.strip()
        lowered = stripped.casefold()
        if lowered.startswith(("retrieval aliases:", "# ")):
            identity_lines.append(lowered)
        if len(identity_lines) >= 4:
            break
    identity = "\n".join(identity_lines)
    signal = frontmatter + "\n" + identity

    markers = {
        "appetite": (
            "human-appetite", "private-desire", "non-instrumental-desire",
            "private appetite", "appetite continuity", "human appetite",
        ),
        "behavior": (
            "behavior-signature", "behaviour-signature", "character-hook",
            "protagonist-as-ip", "stable-choice-bias", "behavior signature",
            "stable choice bias", "character hook",
        ),
        "relationship": (
            "relationship-gravity", "relationship-chemistry", "character-autonomy",
            "relationship gravity", "relationship chemistry", "character autonomy",
            "irreplacable relationship", "irreplaceable relationship",
        ),
    }
    matched = [lane for lane, terms in markers.items() if any(term in signal for term in terms)]
    return matched[0] if len(matched) == 1 else ""


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
                    *([f"human_lane: {item['human_lane']}"] if item.get("human_lane") else []),
                    f"score: {item['score']:g}",
                    "",
                    f"可用抽象：{item['abstract']}",
                    "",
                    f"使用边界：{boundary}",
                ]
            )
        )
    return "\n\n".join(blocks)


def _format_fixed_coordinate_reference(item: Mapping[str, Any] | None) -> str:
    if not item:
        return ""
    boundary = item.get("transfer_boundary") or "只使用这张跨书 synthesis 的读者坐标原则，不迁移来源作品表层设定、人物、事件或数值。"
    return "\n".join(
        [
            "### Fixed Coordinate Reference",
            f"source: {item['slug']}",
            "role: World Vision 固定读者坐标参考；不占 creative inspiration 名额",
            "",
            f"可用抽象：{item['abstract']}",
            "",
            f"使用边界：{boundary}",
        ]
    )


def _load_world_coordinate_reference(
    page_reader: Callable[[str], str], constraints: Iterable[str]
) -> tuple[dict[str, Any] | None, str]:
    try:
        page = page_reader(WORLD_COORDINATE_REFERENCE_SLUG)
    except (GBrainQueryError, OSError, ValueError, KeyError) as error:
        return None, f"固定 Coordinate Reference 读取失败：{error}"
    if not active_inspiration_allowed(page):
        return None, "固定 Coordinate Reference 当前未启用为 active inspiration"
    abstract, transfer_boundary = extract_abstract_content(page)
    if not abstract:
        return None, "固定 Coordinate Reference 没有可提取的抽象区块"
    if _has_surface_conflict(abstract, constraints):
        return None, "固定 Coordinate Reference 与 BOOK 明确硬约束冲突"
    return {
        "slug": WORLD_COORDINATE_REFERENCE_SLUG,
        "type": "synthesis",
        "score": 1.0,
        "abstract": abstract,
        "transfer_boundary": transfer_boundary,
    }, ""


def retrieve_gbrain(
    *,
    mode: str,
    book_content: str = "",
    creative_direction: str = "",
    world_vision: str = "",
    character_card: str = "",
    proposal_context: str = "",
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
        world_vision=world_vision,
        character_card=character_card,
        proposal_context=proposal_context,
        current_long_block=current_long_block,
        current_outline=current_outline,
        recent_summaries=recent_summaries,
    )
    if query_override.strip():
        effective_query = query_override.strip()
        query_strategy = "manual_override"
    else:
        effective_query, query_strategy = default_effective_query(mode, retrieval_brief)
    query_runner = query_func or query_gbrain
    page_reader = page_func or get_gbrain
    allowed_categories = MODE_ALLOWED_CATEGORIES[mode]
    query_scope = ",".join(sorted(allowed_categories))
    if query_strategy == "prose_control_none":
        query_texts = ()
    elif mode == "human_seed" and not query_override.strip():
        # Human retrieval is lane-first even when semantic retrieval is available.
        # This prevents one dense Human topic from crowding the other two lanes.
        query_texts = tuple(HUMAN_LANE_QUERIES[lane] for lane in HUMAN_LANE_ORDER)
        query_strategy = "human_lane_queries"
    elif query_strategy == "planning_keyword_aliases":
        query_texts = PLANNING_KEYWORD_QUERY_BATCHES.get(mode, (effective_query,))
    else:
        query_texts = (effective_query,)
    stdout_parts: list[str] = []
    query_failures: list[dict[str, str]] = []
    first_query_error: GBrainQueryError | None = None
    for query_text in query_texts:
        try:
            stdout_parts.append(
                query_runner(
                    query_text,
                    limit=QUERY_RECALL_LIMIT,
                    detail="medium",
                    scope=query_scope,
                )
            )
        except GBrainQueryError as error:
            if first_query_error is None:
                first_query_error = error
            stdout_parts.append("")
            query_failures.append({"query": query_text, "error": str(error)})
    if query_texts and len(query_failures) == len(query_texts) and first_query_error is not None:
        raise first_query_error
    stdout = "\n".join(part for part in stdout_parts if part)
    parsed_batches = [parse_query_results(part) for part in stdout_parts]
    parsed = [hit for batch in parsed_batches for hit in batch]
    unique_hits = merge_query_hit_batches_round_robin(parsed_batches)
    constraint_world = world_vision
    if mode == "power_seed" and world_vision.strip():
        constraint_world = project_character_power_baseline(world_vision)
    elif mode == "human_seed" and world_vision.strip():
        constraint_world = project_character_life_context(world_vision)
    constraints = extract_hard_constraints(
        creative_direction,
        constraint_world,
        character_card,
        proposal_context,
        book_content,
        current_long_block,
        current_outline,
        recent_summaries,
    )
    coordinate_reference: dict[str, Any] | None = None
    coordinate_reference_error = ""
    if mode == "world_vision":
        coordinate_reference, coordinate_reference_error = _load_world_coordinate_reference(
            page_reader, constraints
        )
    if mode == "context_curator" and query_strategy == "prose_control_keyword_aliases":
        final_limit = 1
    elif mode in {"chapter", "context_curator"}:
        final_limit = CHAPTER_FINAL_RESULT_LIMIT
    elif mode in {"world_vision", "power_seed", "human_seed", "idea"}:
        final_limit = CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    else:
        final_limit = FINAL_RESULT_LIMIT
    novel_candidates: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for hit in unique_hits:
        if hit["slug"] == WORLD_COORDINATE_REFERENCE_SLUG and mode in {"world_vision", "idea", "outline"}:
            if mode != "world_vision":
                rejected.append(
                    {
                        "slug": hit["slug"],
                        "reason": "固定 World Coordinate Reference 已由已批准 World Vision 继承，不重复占 downstream creative 名额",
                    }
                )
            continue
        category = source_category(hit["slug"])
        if category not in allowed_categories:
            rejected.append({"slug": hit["slug"], "reason": f"{mode} 模式不自动使用 {category or '未知来源类别'}"})
            continue
        novel_candidates.append(hit)

    candidate_limit = (
        HUMAN_LANE_CANDIDATE_INSPECTION_LIMIT * len(HUMAN_LANE_ORDER)
        if mode == "human_seed"
        else PLANNING_CANDIDATE_INSPECTION_LIMIT
        if mode in {"world_vision", "power_seed", "idea", "outline"}
        else RAW_RESULT_LIMIT
    )
    visible = novel_candidates[:candidate_limit]
    rejected.extend(
        {"slug": hit["slug"], "reason": "超过小说候选数量上限"}
        for hit in novel_candidates[candidate_limit:]
    )
    accepted: list[dict[str, Any]] = []
    genre_prior_count = 0
    human_lane_counts = {lane: 0 for lane in HUMAN_LANE_ORDER}
    page_cache: dict[str, str] = {}

    def read_candidate_page(slug: str) -> str:
        if slug not in page_cache:
            page_cache[slug] = page_reader(slug)
        return page_cache[slug]

    def evaluate_hit(hit: dict[str, Any], *, required_human_lane: str = "") -> dict[str, Any] | None:
        nonlocal genre_prior_count
        category = source_category(hit["slug"])
        if _has_surface_conflict(hit["snippet"], constraints):
            rejected.append({"slug": hit["slug"], "reason": "与 BOOK 的明确硬约束冲突"})
            return None
        try:
            page = read_candidate_page(hit["slug"])
        except (GBrainQueryError, OSError, ValueError, KeyError):
            rejected.append({"slug": hit["slug"], "reason": "完整页面读取失败"})
            return None
        if not active_inspiration_allowed(page):
            rejected.append({"slug": hit["slug"], "reason": "卡片当前未启用为 active inspiration"})
            return None
        if mode == "human_seed":
            page_lane = human_lane_for_page(page, hit["slug"])
            if not page_lane:
                rejected.append({"slug": hit["slug"], "reason": "Human Craft 未声明或无法判定 appetite / behavior / relationship lane"})
                return None
            if required_human_lane and page_lane != required_human_lane:
                rejected.append({"slug": hit["slug"], "reason": f"Human Craft 属于 {page_lane} lane，不占 {required_human_lane} lane"})
                return None
        else:
            page_lane = ""
        genre_prior = is_genre_prior_page(page)
        if genre_prior and mode not in GENRE_PRIOR_ALLOWED_MODES:
            rejected.append({"slug": hit["slug"], "reason": "章节节点不自动使用 Genre Prior"})
            return None
        if genre_prior and not genre_prior_matches_query(page, effective_query, hit["slug"]):
            rejected.append({"slug": hit["slug"], "reason": "Genre Prior 与当前题材 query 不相关"})
            return None
        if genre_prior and genre_prior_count >= GENRE_PRIOR_ACCEPT_LIMIT:
            rejected.append({"slug": hit["slug"], "reason": "超过 Genre Prior 接受上限"})
            return None
        abstract, transfer_boundary = extract_abstract_content(page)
        if not abstract:
            rejected.append({"slug": hit["slug"], "reason": "没有可提取的抽象区块"})
            return None
        if _has_surface_conflict(abstract, constraints):
            rejected.append({"slug": hit["slug"], "reason": "与 BOOK 的现实模式冲突"})
            return None
        candidate = {
            **hit,
            "type": _type_for_category(category),
            "is_genre_prior": genre_prior,
            "abstract": abstract,
            "transfer_boundary": transfer_boundary,
        }
        if page_lane:
            candidate["human_lane"] = page_lane
        if genre_prior:
            genre_prior_count += 1
        return candidate

    if mode == "human_seed":
        accepted_slugs: set[str] = set()
        if query_override.strip():
            # Manual override is one candidate pool, but lane caps still apply.
            lane_pools = {lane: visible for lane in HUMAN_LANE_ORDER}
        else:
            lane_pools = {
                lane: [
                    hit for hit in dedupe_query_hits_by_slug(parsed_batches[index])
                    if source_category(hit["slug"]) in allowed_categories
                ][:HUMAN_LANE_CANDIDATE_INSPECTION_LIMIT]
                for index, lane in enumerate(HUMAN_LANE_ORDER)
            }
        for lane in HUMAN_LANE_ORDER:
            for hit in lane_pools[lane]:
                if hit["slug"] in accepted_slugs:
                    continue
                candidate = evaluate_hit(hit, required_human_lane=lane)
                if candidate is None:
                    continue
                accepted.append(candidate)
                accepted_slugs.add(hit["slug"])
                human_lane_counts[lane] = 1
                break
    else:
        for hit in visible:
            if len(accepted) >= final_limit:
                rejected.append({"slug": hit["slug"], "reason": "超过最终数量上限"})
                continue
            candidate = evaluate_hit(hit)
            if candidate is not None:
                accepted.append(candidate)

    coordinate_bundle = _format_fixed_coordinate_reference(coordinate_reference)
    creative_bundle = _format_bundle(accepted) if accepted else ("" if coordinate_reference else EMPTY_RESULT)
    result_bundle = "\n\n".join(part for part in (coordinate_bundle, creative_bundle) if part)
    return {
        "status": "available",
        "scope": GBRAIN_SCOPE_LABEL,
        "mode": mode,
        "effective_query": effective_query,
        "query_strategy": query_strategy,
        "query_texts": list(query_texts),
        "query_failures": query_failures,
        "retrieval_brief": retrieval_brief,
        "query_scope": query_scope,
        "hard_constraints": constraints,
        "raw_count": len(parsed),
        "unique_raw_count": len(unique_hits),
        "novel_candidate_count": len(novel_candidates),
        "accepted_count": len(accepted),
        "coordinate_reference_count": 1 if coordinate_reference else 0,
        "coordinate_reference": coordinate_reference,
        "coordinate_reference_error": coordinate_reference_error,
        "genre_prior_count": genre_prior_count,
        "human_lane_counts": human_lane_counts if mode == "human_seed" else {},
        "human_lane_order": list(HUMAN_LANE_ORDER) if mode == "human_seed" else [],
        "human_lane_candidate_limit": HUMAN_LANE_CANDIDATE_INSPECTION_LIMIT if mode == "human_seed" else 0,
        "rejected_count": len(rejected),
        "query_limit": QUERY_RECALL_LIMIT,
        "requested_limit": candidate_limit,
        "final_limit": final_limit,
        "raw_stdout": stdout,
        "novel_candidates": novel_candidates,
        "raw_results": visible,
        "accepted": accepted,
        "rejected": rejected,
        "result": result_bundle,
    }
