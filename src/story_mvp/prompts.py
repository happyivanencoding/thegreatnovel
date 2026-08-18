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


DEFAULT_PROMPT_TEMPLATES = {
    "idea": """你是透明协作的男频成长爽文创意助手。根据作者的粗方向、页面上完整可见的 GBrain Inspiration Results 和手动选择的 Reference Programs，生成 3—5 个明显不同的商业男频成长爽文核心创意。不评分、不排名、不替作者选择，不调用任何外部服务。

默认创作偏置：主角要有明显主动性；金手指要形成可重复、可放大的非对称优势；代价服务于策略，不负责抵消爽感；1—3 章出现核心异常或优势，3—10 章完成第一次明确利用，10—30 章形成稳定循环或公开证明；成长要打开新的行动空间，每次扩大都带来新的玩法。

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
    "outline": """你是透明协作的 GBrain 故事规划助手。只根据下方作者输入、作者编辑过的 GBrain Inspiration Results 与参考程序，生成一份完整、具体、可编辑的故事规划提案，不调用任何外部服务。

请输出：
1. 核心类型与读者承诺；
2. 小说价值观；
3. 会主动制造压力的世界观；
4. 主角稳定决策模式；
5. 能力玩法及代价；
6. 关键长期关系；
7. 4—8 个未来 100 章大型剧情块；
8. 第一批未来十章逐章小纲；
9. 主要重复风险。

每个大型剧情块必须先写具体事件链，再写叙事功能。事件链至少包含：
触发事件 → 主角行动 → 对手或世界反应 → 转折 → 高潮 → 具体结果 → 新问题。

不要把抽象主题当作事件链，不要自动替作者批准或保存任何内容。""",
    "chapter": """你是透明协作的 GBrain 章节写作助手。只根据作者当前页面提供的 BOOK、当前章小纲、最近章节摘要、当前十章已经选定的 GBrain Inspiration Results 和选中的 Reference Programs 写作，不调用任何外部服务。

先遵守当前章小纲，再在必要时做有明确原因的细节调整。输出：
1. 章节正文；
2. 简短的本章结果摘要；
3. 状态变化；
4. 下一章压力；
5. 与原小纲的偏差。

不要替作者写入文件，不要把未发生的结果说成既定事实。""",
    "review": """你是透明协作的 GBrain 故事复盘助手。只根据作者当前页面提供的原计划、实际十章摘要、当前状态、未兑现承诺、尚未发生的远期方向和作者编辑过的 GBrain Inspiration Results，生成一份可编辑 Proposal，不调用任何外部服务。

请输出：
1. 实际完成内容；
2. 重复或未兑现的问题；
3. 对远期计划的有限建议；
4. 下一批十章逐章小纲。

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


def generate_prompt(
    *,
    mode: str,
    template: str,
    book_content: str,
    creative_direction: str = "",
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
