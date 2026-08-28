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



def project_world_reality(world_vision: str) -> str:
    """Project approved world facts safe for downstream runtime.

    Keeps ordinary life, power normality, social reality, generic value structures
    and public knowledge boundaries while excluding named active story opportunities
    and named unresolved mysteries. This is fact authority, not prose guidance.
    """

    parts: list[str] = ["# WORLD REALITY AUTHORITY｜Approved Facts Only"]
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
    return "\n".join(parts).strip() + "\n"


def project_character_world_slice(world_vision: str) -> str:
    """Project world reality for character generation without active story hooks."""

    reality = project_world_reality(world_vision).strip().replace(
        "# WORLD REALITY AUTHORITY｜Approved Facts Only",
        "# CHARACTER WORLD SLICE｜World Reality Only",
        1,
    )
    parts: list[str] = [reality]
    parts += [
        "",
        "## Character 生成边界",
        "人物可以深受上述世界现实塑造，并应当相对于世界正常值形成特殊性。",
        "成长环境必须来自世界真实社会层，但不要求所有人物从普通底层起步：可以来自普通家庭、富商、军户、宗门附属、专业家庭、地方权势或其它世界合法位置。关键是这个切片本身不是 named 大事件、named 秘境、named NPC、named 神兵或未来剧情路线，不是为了给剧情插座配钥匙。",
        "特殊能力/际遇优先采用 World Normal → Power Asymmetry：先指出普通人或普通修士通常怎样，再说明人物相对同层到底多了什么明显特权，以及这种优势为什么会被察觉、嫉妒、利用或恐惧。优势来源不必强制是世界内已知的合法例外，也可以是稀有天赋、唯一奇物/际遇、外来知识/经验、外挂、极端正常天赋或少量优势叠加；来源可以晚解释，但眼前结果必须清楚。异常不能只是一项更高效的职业技能、诊断流程、维护技巧或行政缝隙；若它主要体现专业能力，也必须进一步形成读者能直接想拥有的个人力量、身份、关系或行动自由。",
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
        "## Power Asymmetry 生成边界",
        "Core Fantasy / 特殊能力首先相对于本区块的力量 Normal / Rarity / Acquisition Conditions 生成，而不是相对于人物职业生成。",
        "先回答：这个世界绝大多数人怎样获得、承载和使用超凡力量？哪些能力常见、哪些少见、哪些尚未被可靠证实？再创造一个相对正常分布明显超标的 Power Asymmetry。它可以来自世界内稀有异常，也可以来自唯一奇物、外来知识/经验、外挂、极端正常天赋或少量优势叠加；不要为了“合法化”强行给世界补一套机制。",
        "成长背景可以解释人物为什么发现、理解、珍惜、滥用或隐藏这个异常，却不能因为人物是矿工、匠人、账房、向导等职业，就把异常自动写成超级辨矿、维修诊断、路线优化、账契解释等职业强化。",
        "专业技能可以与异常发生化学反应，但不能替代男频 Core Fantasy 本身。",
        "这是男频成长长篇：Power Asymmetry 不能只是一闪即逝的便利。正常境界提升应真实增强主角基础力量，非对称优势的掌握则继续扩大玩法；默认宁可让第一稿偏强一档，也不要把特权削成普通同层水平。至少保留一条高阶也不会自动消失的边界来防万能，但不要用等价代价把核心爽点抵消。",
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
