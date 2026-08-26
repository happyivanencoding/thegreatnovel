from __future__ import annotations

import re


_ALLOWED_CHARACTER_SECTIONS = (
    "## 普通人的生活与上升",
    "## 力量体系与正常值",
    "## 社会现实与身份",
    "## 世界里真正值钱、值得想要的东西",
    "## 世界知识边界",
)

_CHARACTER_POWER_SECTIONS = (
    "## 力量体系与正常值",
)

_CHARACTER_LIFE_SECTIONS = (
    "## 普通人的生活与上升",
    "## 社会现实与身份",
    "## 世界里真正值钱、值得想要的东西",
    "## 世界知识边界",
)

_STORY_OPPORTUNITY_SECTIONS = (
    "## 世界正在发生的大事",
    "## 值得进入的地点、奇观与未知",
)


_HEADING_RE = re.compile(r"(?m)^## .+$")


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    after = text[start + len(heading):]
    m = _HEADING_RE.search(after)
    end = start + len(heading) + (m.start() if m else len(after))
    return text[start:end].strip()


def _preamble(text: str) -> str:
    first = _HEADING_RE.search(text)
    raw = text[: first.start()] if first else text
    raw = re.sub(r"(?m)^#\s+PROTAGONIST-BLIND WORLD VISION\s*$", "", raw).strip()
    return raw


def _strip_named_mysteries(knowledge_section: str) -> tuple[str, str]:
    marker = re.search(r"当前没人能完整解释的事实(?:包括)?：", knowledge_section)
    if marker is None:
        return knowledge_section.strip(), ""
    safe = knowledge_section[: marker.start()].rstrip()
    mysteries = knowledge_section[marker.start() :].strip()
    return safe, mysteries


def project_character_world_slice(world_vision: str) -> str:
    """Project world facts that may shape a character without leaking active story hooks.

    The projection intentionally preserves laws, normal/rarity baselines, culture,
    ordinary life and generic value structures. It excludes named active events,
    named adventure locations, unresolved named mysteries and author-facing reader
    coordinates. No LLM call is involved.
    """

    parts: list[str] = ["# CHARACTER WORLD SLICE｜World Reality Only"]
    preamble = _preamble(world_vision)
    if preamble:
        parts += ["", "## 世界基础现实", preamble]

    for heading in _ALLOWED_CHARACTER_SECTIONS:
        block = _section(world_vision, heading)
        if not block:
            continue
        if heading == "## 世界知识边界":
            block, _ = _strip_named_mysteries(block)
        if block:
            parts += ["", block]

    parts += [
        "",
        "## Character 生成边界",
        "人物可以深受上述世界现实塑造，并应当相对于世界正常值形成特殊性。",
        "成长环境必须来自世界真实社会层，但不要求所有人物从普通底层起步：可以来自普通家庭、富商、军户、宗门附属、专业家庭、地方权势或其它世界合法位置。关键是这个切片本身不是 named 大事件、named 秘境、named NPC、named 神兵或未来剧情路线，不是为了给剧情插座配钥匙。",
        "特殊能力/际遇优先采用 World Normal → Legal Exception：先指出普通人或普通修士通常怎样，再说明人物合法偏离了哪一条正常分布，以及这种异常为什么在本世界可被察觉、嫉妒、利用或恐惧。异常不能只是一项更高效的职业技能、诊断流程、维护技巧或行政缝隙；若它主要体现专业能力，也必须进一步形成读者能直接想拥有的个人力量、身份、关系或行动自由。",
        "经历是背景，不是人格证明：先保留世界内真实生活事实，再让欲望、关系与稳定选择偏向在其中自然形成；经历可以塑造人物，但不要求每段经历逐条推出一个人格适应结论，也不从预设人格反向发明童年。",
        "人物受世界塑形，但不为预设剧情服务：人物属于这个世界，却不是为世界已经准备好的故事机会而出生。",
    ]
    return "\n".join(parts).strip() + "\n"


def project_character_power_baseline(world_vision: str) -> str:
    """Project the world's supernatural normal distribution for Character design."""

    parts: list[str] = ["# CHARACTER POWER BASELINE｜Core Fantasy Authority"]
    preamble = _preamble(world_vision)
    if preamble:
        parts += ["", "## 世界基础自然现实", preamble]
    for heading in _CHARACTER_POWER_SECTIONS:
        block = _section(world_vision, heading)
        if block:
            parts += ["", block]
    parts += [
        "",
        "## Power Exception 生成边界",
        "Core Fantasy / 特殊能力首先相对于本区块的力量 Normal / Rarity / Acquisition Conditions 生成，而不是相对于人物职业生成。",
        "先回答：这个世界绝大多数人怎样获得、承载和使用超凡力量？哪些能力常见、哪些少见、哪些尚未被可靠证实？再寻找一个仍服从底层规则但真实偏离正常分布的 Legal Exception。",
        "成长背景可以解释人物为什么发现、理解、珍惜、滥用或隐藏这个异常，却不能因为人物是矿工、匠人、账房、向导等职业，就把异常自动写成超级辨矿、维修诊断、路线优化、账契解释等职业强化。",
        "专业技能可以与异常发生化学反应，但不能替代男频 Core Fantasy 本身。",
        "这是男频成长长篇：Legal Exception 不能只是一次性奇遇或固定技巧。它必须与世界正常修炼体系兼容——正常境界提升应真实增强主角基础力量，异常掌握则扩大其容量、精度、组合、适用对象或行动自由；同时至少保留一条高阶也不能自动抹掉的硬边界。",
    ]
    return "\n".join(parts).strip() + "\n"


def project_character_life_context(world_vision: str) -> str:
    """Project social reality used to grow personality, desire and relationships."""

    parts: list[str] = ["# CHARACTER LIFE CONTEXT｜Upbringing Authority"]
    for heading in _CHARACTER_LIFE_SECTIONS:
        block = _section(world_vision, heading)
        if not block:
            continue
        if heading == "## 世界知识边界":
            block, _ = _strip_named_mysteries(block)
        if block:
            parts += ["", block]
    parts += [
        "",
        "## Upbringing 生成边界",
        "本区块只负责塑造出身、阶层、家庭生态、教育、欲望、偏见、恐惧、关系与行为适应，不负责决定 Core Fantasy 的异常类型。",
        "人物可以来自世界任何合法社会位置：贫寒、普通、富裕、宗门家庭、军户、商人、专业家庭、地方权势、既得利益或天赋优越者都可以；不默认底层受压迫者。",
        "经历是背景，不是人格证明：具体经历先作为生活事实成立；人物的多重动机、关系与稳定选择偏向可以受这些经历影响，但不要求逐条解释因果，也不从性格标签、职业或道德使命反推经历。",
        "不得引用未提供的 named 大事件、named NPC、named 秘境、named 神兵或未来剧情路线。",
    ]
    return "\n".join(parts).strip() + "\n"


def project_story_opportunity_layer(world_vision: str) -> str:
    """Project named active hooks kept away from character generation."""

    parts: list[str] = ["# STORY OPPORTUNITY LAYER｜Hidden From Character Generation"]
    for heading in _STORY_OPPORTUNITY_SECTIONS:
        block = _section(world_vision, heading)
        if block:
            parts += ["", block]

    knowledge = _section(world_vision, "## 世界知识边界")
    if knowledge:
        _, mysteries = _strip_named_mysteries(knowledge)
        if mysteries:
            parts += ["", "## Named Unresolved Mysteries", mysteries]
    return "\n".join(parts).strip() + "\n"

_WRITER_TEXTURE_SECTIONS = (
    "## 普通人的生活与上升",
    "## 社会现实与身份",
    "## 世界里真正值钱、值得想要的东西",
)


def project_writer_texture_context(world_vision: str, *, max_chars: int = 1400) -> str:
    """Project a tiny, non-authoritative world texture reference for Curator/Writer.

    This is deliberately not Human Seed input. It may only help prose occasionally
    ground an already planned scene in ordinary world life. It cannot create Canon,
    a new character motive, or a new story hook.
    """

    blocks = [
        block
        for heading in _WRITER_TEXTURE_SECTIONS
        if (block := _section(world_vision, heading))
    ]
    if not blocks:
        return ""
    text = "\n\n".join(blocks).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit("\n", 1)[0].rstrip() + "…"
    return (
        "# Optional World-Life Texture Reference｜Writer-side only\n"
        "只在当前场景自然需要时，从以下已批准世界事实里偶尔投影 0—1 个生活性细节。"
        "它只是点缀：不得建立新规则、新人物欲望、新剧情义务或长期 Canon，也不要求每章使用。\n\n"
        + text
        + "\n"
    )
