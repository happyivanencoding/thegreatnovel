from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


PROMPT_MODES = {
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
    "outline": """你是透明协作的 GBrain 故事规划助手。只根据下方作者输入与参考程序，生成一份完整、具体、可编辑的故事规划提案，不调用任何外部服务。

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
    "chapter": """你是透明协作的 GBrain 章节写作助手。只根据作者当前页面提供的 BOOK、当前章小纲、最近章节摘要和选中的 Reference Programs 写作，不调用任何外部服务。

先遵守当前章小纲，再在必要时做有明确原因的细节调整。输出：
1. 章节正文；
2. 简短的本章结果摘要；
3. 状态变化；
4. 下一章压力；
5. 与原小纲的偏差。

不要替作者写入文件，不要把未发生的结果说成既定事实。""",
    "review": """你是透明协作的 GBrain 故事复盘助手。只根据作者当前页面提供的原计划、实际十章摘要、当前状态、未兑现承诺和尚未发生的远期方向，生成一份可编辑 Proposal，不调用任何外部服务。

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
    current_outline: str = "",
    recent_summaries: str = "",
    selected_references: list[Mapping[str, Any]] | None = None,
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
    parts.append(_input_block("当前 BOOK.md", book_content))
    parts.append(_input_block("选中的 Reference Programs", format_references(selected_references or [])))

    if mode == "outline":
        parts.append(
            _input_block(
                "作者当前创意与结构（请在上面的 BOOK 输入中保留一句话创意）",
                book_content,
            )
        )
    elif mode == "chapter":
        parts.append(_input_block("当前章具体小纲", current_outline))
        parts.append(_input_block("最近 1—3 章摘要", recent_summaries))
    else:
        parts.append(_input_block("原计划", book_content))
        parts.append(_input_block("实际十章摘要", actual_summaries))
        parts.append(_input_block("当前状态", current_state))
        parts.append(_input_block("未兑现承诺", unfulfilled_promises))
        parts.append(_input_block("尚未发生的 100 章方向", future_direction))

    return "\n\n".join(parts).strip() + "\n"
