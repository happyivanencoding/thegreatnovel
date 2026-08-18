from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


PROMPT_MODES = {
    "idea": "男频爽文创意生成",
    "outline": "新书/总纲规划",
    "chapter": "当前章节写作",
    "review": "十章复盘与下一批十章",
}

REQUIRED_OUTLINE_FIELDS = (
    "触发事件",
    "推动事件的人",
    "主角行动",
    "对手或世界反应",
    "直接结果",
    "状态变化",
    "叙事功能",
    "结尾推动力",
)

DEFAULT_PRODUCT_DIRECTION = """当前产品默认目标是成熟中文男频成长爽文。优先寻找具有主角主动性、非对称优势、可重复利用、复利增长、早期兑现和持续行动空间扩大的具体故事。创新应优先体现在玩法和成长路径上，而不是单纯通过悲剧代价、伦理折磨或反爽机制制造“高级感”。这是创作方向，不是机械模板；如果作者明确要求其他类型，以作者要求为准。"""

DEFAULT_POWER_FANTASY_DIRECTION = """Power Fantasy First：当前“爽”首先是主角获得过去没有的能力，并产生直接、可感知、逐渐扩大的正向结果。资源经营只能作为发动机之一，必须持续转换为修为、功法、技法、装备、战斗胜利、身份、机缘或新地图。直接爽感（突破、新术、越阶胜利、机缘、实力反转）与间接爽感（财富、渠道、组织、席位）都可以存在，但不能让多个大型剧情块只停留在间接层。可用 payoff channel 包括 POWER_BREAKTHROUGH、NEW_TECHNIQUE、COMBAT_DOMINANCE、UNDERDOG_VICTORY、RESOURCE_GAIN、TREASURE_GAIN、STATUS_RISE、PUBLIC_RECOGNITION、KNOWLEDGE_ADVANTAGE、STRATEGIC_ADVANTAGE、WORLD_EXPANSION、ACTION_SPACE_EXPANSION；按题材选择，不要求全部出现。"""


DEFAULT_PROMPT_TEMPLATES = {
    "idea": f"""你是透明协作的男频成长爽文创意助手。根据作者的粗方向、页面上完整可见的 GBrain Inspiration Results 和手动选择的 Reference Programs，生成 3—5 个明显不同的商业男频成长爽文核心创意。不评分、不排名、不替作者选择，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_POWER_FANTASY_DIRECTION}

默认创作偏置：主角要有明显主动性；金手指要形成可重复、可放大的非对称优势；代价服务于策略，不负责抵消爽感；1—3 章出现核心异常或优势，3—10 章完成第一次明确利用，10—30 章形成稳定循环或公开证明；成长要打开新的行动空间，每次扩大都带来新的玩法。

核心能力必须有纵向成长路线：早期能做什么，随后如何恢复/放大/反推规则，进一步如何服务修炼、技法、战斗准备、传承或新地图。每个候选都要写至少一个直接爽感 payoff 和一个间接爽感 payoff。

不要为了显得高级，默认使用失忆、寿命、感情、伦理诅咒或越成功越痛苦等抵消型代价。除非作者明确要求，否则优先寻找可以复利、早期兑现并自然扩大到 100 章的玩法。

每个候选必须完整使用以下结构：
## 候选N：书名/概念名
一句话创意：主角是谁 + 得到什么非对称优势 + 最直接要解决什么问题。
主角核心优势：它具体能做什么。
为什么这是优势：别人为什么无法轻易复制。
核心爽点循环：主角做什么 → 得到什么 → 怎样进一步放大优势 → 引来什么更高层机会或敌人。
开局1—3章：具体发生什么。
前10章：第一个完整小闭环是什么。
第一个公开证明：主角什么时候让别人第一次真正意识到他的价值、实力或异常。
100章扩张方向：小能力怎样扩大为资源、身份、组织、地域或世界行动能力。
关键关系：至少一个会随主角成长持续改变的人。
最大的重复风险：这个玩法写久以后最容易重复什么。""",
    "outline": f"""你是透明协作的 GBrain 故事规划助手。只根据下方作者输入、作者编辑过的 GBrain Inspiration Results 与参考程序，生成一份完整、具体、可编辑的故事规划提案，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_POWER_FANTASY_DIRECTION}

先建立整本书的总体设计画像，再据此规划 100 章和第一批十章。最终返回内容必须按以下四个一级 Markdown 标题逐字输出，不能增加其它一级标题：

# 小说总体设计画像
# 未来100章大型剧情块
# 未来十章逐章小纲
# 当前状态、未兑现承诺与作者备注

在“小说总体设计画像”下完整输出以下 12 个二级标题，不生成 JSON/YAML，不评分，不把任何一项变成 Hard Gate：

## 1. 核心类型与读者承诺
说明本质类型、前中远期读者为什么继续追，以及类型升级由什么具体故事变化产生。
## 2. 世界观结构
只写真正决定剧情的 2—4 条核心坐标轴，并说明它们怎样咬合、每次成长打开什么行动空间。
## 3. 世界如何持续制造剧情压力
从境界压制、功法与传承、资源竞争、强敌、同辈竞争、宗门阶层、秘境、遗迹、妖兽、地域危险、身份暴露、大势力、市场/渠道和上层世界规则中选择合适来源；不要让市场、认证或制度天然占据主要位置。
## 4. 主角模型、人物弧与核心矛盾
优先写主角最强欲望、最喜欢采取的行动、如何利用优势、如何越来越主动、从弱者走向什么位置，以及哪类胜利最能让读者满足。只有自然存在时才写核心人物矛盾，不要为了显得深刻强制生成伦理困境。
## 5. 配角与关系系统
写长期角色、各自利益、关系变化与反转、情绪价值，以及关系系统最容易失败的地方。关系可以承担崇拜、友情、师徒、竞争、嫉妒、恐惧、爱慕、忠诚、背叛和旧日轻视后的重新评价；不要把所有角色都写成制度利益方，也不要让所有人只做同一种反应。
## 6. 核心情节发动机
至少写两个并行循环：A. 优势复利循环（发现/加工/放大资源并获得更高级资源）；B. 力量兑现循环（资源进入修炼/新术/实战，突破或领先后获得新身份、秘境资格和更高级资源）。说明两者如何互相驱动，以及第2/3/4次运行如何改变资源、风险、身份、规模或收益形式。
## 7. 叙事结构
写主要视角、切换条件、切换目的，以及前后期场景叙事和总结叙事的变化；说明如何用他人反应展示主角地位变化。
## 8. 文风与可操作参数
写目标单章长度、段落、信息/描写/对话/内心/战斗密度、系统信息频率、每章推进台阶和禁止形成的机械文风；这些是创作目标，不是代码限制。
## 9. 对话特点
写核心角色的节奏、信息量、身份、隐藏目的、直接或试探方式，以及对话承担的博弈功能。
## 10. 节奏结构
分别说明单章、约10章、大型剧情块和100章推进什么，如何交替小爽点、中型兑现、阶段大兑现、afterward与新压力，并指出节奏重复风险。
## 11. 主题、价值观与长期问题
写故事赞赏什么、警惕什么、主角相信什么、世界迫使他面对什么反例，以及主题如何从实际机制中浮现。主题是长期运行后自然出现的东西，不得要求主角承受伦理惩罚；可以是普通人靠选择和积累逆袭、知识打破资源壁垒、实力带来选择权或弱小时别人定规则、强大后主角获得定义规则的资格。
## 12. 当前设计最强点与最弱点
写设计统一性、当前最弱处和写作时真正需要防止的 2—5 个问题，不生成风险清单。

画像必须是作者可修改的创作模型，而不是百科全书或机械模板。

未来 100 章写 4—8 个自然剧情块，不要套固定 5 × 20。每个剧情块必须使用以下顺序：

所有大型剧情块必须共同覆盖第1章到第100章：第一块从第1章开始，最后一块结束于第100章，相邻章节范围必须清楚衔接。必须完整输出所有剧情块，不能只展示第一个块，不能用“后续类似”“后面略”省略。越靠后的块可以稍粗，但仍必须明确核心人物、主要事件、主角行动、核心转折、高潮、得到什么、失去或承担什么，以及如何进入下一块。

## 第X—Y章：具体块名
具体发生：先写具体人物、具体地点、具体事件、主角行动、对手或世界反应、转折、高潮和新问题；不要只写“建立资源循环”或“敌人升级”。
阶段结果：说明主角获得或失去什么资源、能力、身份、关系或行动空间，以及下一块为什么必然发生。
叙事功能：说明这组具体事件完成了什么兑现、换挡或压力升级。
推向下一块：写出下一块从哪个具体问题开始。

每个大型剧情块还必须明确：这一块结束后，读者具体看到了主角更强、更富、更自由、更有地位或更有选择权中的哪一种变化，并尽量改变 payoff channel。对仙侠、玄幻或高武，100 章内应自然出现明确境界/能力成长、新功法或技巧、战斗/高压验证、同辈或强敌比较、资源/宝物争夺、秘境/遗迹/新地图、公开实力证明或更高层人物重新评价；具体多少由故事决定，不是 Python 检查。

资源经营必须服务于力量成长：资源 → 修炼/新术/装备 → 实战胜利或能力证明 → 新身份/机缘/地图 → 更高级资源。不要让卖丹、开店、扩渠道本身取代主角变强。

未来十章必须是一个连续的小故事，而不是十个独立主题。每章使用：

## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

每章都必须有具体人物、具体事件、主角具体行动、直接结果、状态变化、叙事功能和结尾推动。禁止用“主角继续调查”“危机升级”“爆发点”“关系深化”“敌人变强”代替剧情。

必须连续逐章列出完整的十章，不能合并章节，不能省略后几章。

最后在当前状态一级标题下写出故事开始前的初始状态、已经建立的远期承诺、当前未解决问题和作者备注。

不要把抽象主题当作事件链，不要自动替作者批准或保存任何内容。""",
    "chapter": """你是透明协作的 GBrain 章节写作助手。只根据作者当前页面提供的 BOOK 执行相关画像、当前大型剧情块、当前章小纲、最近章节摘要、当前十章已经选定的 GBrain Inspiration Results 和选中的 Reference Programs 写作，不调用任何外部服务。

先遵守当前章小纲，再在必要时做有明确原因的细节调整。输出：
1. 章节正文；
2. 简短的本章结果摘要；
3. 状态变化；
4. 下一章压力；
5. 与原小纲的偏差。

不要替作者写入文件，不要把未发生的结果说成既定事实。""",
    "review": f"""你是透明协作的 GBrain 故事复盘助手。只根据作者当前页面提供的原计划、实际十章摘要、当前状态、未兑现承诺、尚未发生的远期方向和作者编辑过的 GBrain Inspiration Results，生成一份可编辑 Proposal，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

请输出：
1. 实际完成内容；
2. 重复或未兑现的问题；
3. 对远期计划的有限建议；
4. 下一批十章逐章小纲。

如果实际写作已经证明总体画像需要变化，先输出：

## 总体画像需要调整的地方

只写被已发生事实支持的有限建议，不自动修改 BOOK；如果没有必要调整，明确写“暂不调整”。

在逐章小纲之前，先写：

## 下一批十章总体事件链

用 3—6 句话说明这一批十章从什么具体状态开始、出现什么问题、主角准备怎么解决、中途发生什么转折、第十章左右具体兑现什么，以及留下什么新问题。

下一批十章必须使用与 outline 完全相同的格式：

## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

十章必须组成一个连续的局部故事。禁止只写“主角继续调查”“危机升级”“爆发点”“关系深化”或“敌人变强”，再让 Writer 自己补造剧情。

建议必须尊重已经发生的事实，不能自动采用、保存或重写 BOOK。""",
}


class HardGateError(ValueError):
    def __init__(self, missing_fields: list[str]) -> None:
        self.missing_fields = missing_fields
        super().__init__("当前章小纲缺少非空字段：" + "、".join(missing_fields))


def parse_outline_fields(outline: str) -> dict[str, str]:
    """Parse the eight supported outline fields from individual lines."""
    values: dict[str, str] = {}
    for line in outline.splitlines():
        match = re.match(r"^\s*(?:[-*]\s*)?([^：:]+?)\s*[：:]\s*(.*?)\s*$", line)
        if not match:
            continue
        label = match.group(1).strip()
        value = match.group(2).strip()
        if label in REQUIRED_OUTLINE_FIELDS and value:
            values[label] = value
    return values


def validate_current_outline(outline: str) -> None:
    values = parse_outline_fields(outline)
    missing = [field for field in REQUIRED_OUTLINE_FIELDS if not values.get(field)]
    if missing:
        raise HardGateError(missing)


def _display_value(value: Any) -> str:
    if value is None:
        return "（未填写）"
    if isinstance(value, (list, tuple)):
        return "；".join(_display_value(item) for item in value)
    if isinstance(value, Mapping):
        return "；".join(f"{key}：{_display_value(item)}" for key, item in value.items())
    return str(value).strip() or "（未填写）"


def format_references(references: Iterable[Mapping[str, Any]]) -> str:
    lines: list[str] = []
    fields = (
        "program_id",
        "story_phase",
        "input_state",
        "central_pressure",
        "reusable_program",
        "applicable_conditions",
        "failure_modes",
        "anti_repetition_notes",
        "output_state",
    )
    for index, reference in enumerate(references, start=1):
        lines.append(f"Reference Program {index}")
        for field in fields:
            lines.append(f"{field}: {_display_value(reference.get(field))}")
        lines.append("")
    return "\n".join(lines).strip() or "（本次未选择 Reference Program）"


def _input_block(title: str, value: str) -> str:
    return f"## {title}\n\n{value.strip() or '（未填写）'}"


def _extract_markdown_block(content: str, heading: str) -> str:
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


def _chapter_book_context(book_content: str) -> str:
    headings = (
        "## 1. 核心类型与读者承诺",
        "## 2. 世界观结构",
        "## 4. 主角模型、人物弧与核心矛盾",
        "## 5. 配角与关系系统",
        "## 8. 文风与可操作参数",
        "## 9. 对话特点",
    )
    blocks = [
        f"{heading}\n\n{_extract_markdown_block(book_content, heading)}"
        for heading in headings
        if _extract_markdown_block(book_content, heading)
    ]
    status = _extract_markdown_block(book_content, "# 当前状态、未兑现承诺与作者备注")
    if status:
        blocks.append(f"# 当前状态、未兑现承诺与作者备注\n\n{status}")
    return "\n\n".join(blocks)


def generate_prompt(
    *,
    mode: str,
    template: str,
    book_content: str,
    creative_direction: str = "",
    current_long_block: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
    selected_references: list[Mapping[str, Any]] | None = None,
    gbrain_inspiration: str = "",
    actual_summaries: str = "",
    current_state: str = "",
    unfulfilled_promises: str = "",
    future_direction: str = "",
) -> str:
    if mode not in PROMPT_MODES:
        raise ValueError(f"未知 Prompt 模式：{mode}")
    if len(selected_references or []) > 3:
        raise ValueError("最多只能选择 3 个 Reference Program")
    if mode == "chapter":
        validate_current_outline(current_outline)

    prompt_template = template.strip()
    parts = [prompt_template, "", "# 页面当前输入"]
    if mode == "idea":
        parts.append(_input_block("作者粗方向", creative_direction))
        parts.append(_input_block("当前 BOOK.md（如果作者已经填写）", book_content))
    elif mode == "review":
        parts.append(_input_block("原计划", book_content))
        parts.append(_input_block("创作方向", creative_direction))
    elif mode == "chapter":
        parts.append(_input_block("当前 BOOK 的执行相关画像与状态", _chapter_book_context(book_content)))
        parts.append(_input_block("当前大型剧情块", current_long_block))
    else:
        parts.append(_input_block("当前 BOOK.md", book_content))
        parts.append(_input_block("创作方向", creative_direction))
    parts.append(_input_block("选中的 Reference Programs", format_references(selected_references or [])))
    parts.append(_input_block("GBrain Inspiration Results（作者可编辑原文）", gbrain_inspiration))

    if mode == "chapter":
        parts.append(_input_block("当前章具体小纲", current_outline))
        parts.append(_input_block("最近 1—3 章摘要", recent_summaries))
    elif mode == "review":
        parts.append(_input_block("实际十章摘要", actual_summaries))
        parts.append(_input_block("当前状态", current_state))
        parts.append(_input_block("未兑现承诺", unfulfilled_promises))
        parts.append(_input_block("尚未发生的 100 章方向", future_direction))

    return "\n\n".join(parts).strip() + "\n"
