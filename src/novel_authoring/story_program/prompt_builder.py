"""Visible prompt templates and the two small hard/soft planning checks."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from novel_authoring.story_program.board import normalize_section_key, parse_markdown_sections
from novel_authoring.story_program.reference_programs import ReferenceProgram

PROMPT_MODE_LABELS = {
    "new_book": "模式一：新书总控 Prompt",
    "next_batch": "模式二：下一批十章 Prompt",
    "current_chapter": "模式三：当前章节 Prompt",
    "review": "模式四：十章复盘与远期调整 Prompt",
}


@dataclass(frozen=True, slots=True)
class ConcretePlanGate:
    passed: bool
    missing: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "missing": list(self.missing)}


@dataclass(frozen=True, slots=True)
class PromptBuildResult:
    mode: str
    prompt: str | None
    template: str
    gate: ConcretePlanGate | None
    soft_warnings: tuple[str, ...]
    references: tuple[ReferenceProgram, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "prompt": self.prompt,
            "template": self.template,
            "gate": None if self.gate is None else self.gate.to_dict(),
            "soft_warnings": list(self.soft_warnings),
            "references": [item.to_dict() for item in self.references],
        }


def template_for_mode(markdown: str, mode: str) -> str:
    label = PROMPT_MODE_LABELS.get(mode)
    if label is None:
        raise ValueError(f"未知 Prompt 模式：{mode}")
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start: int | None = None
    end = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip() == label:
            start = index
            continue
        if start is not None and index > start and line.startswith("## "):
            end = index
            break
    if start is None:
        raise ValueError(f"GBRAIN_PROMPTS.md 缺少模板：{label}")
    return "\n".join(lines[start:end]).strip()


def concrete_plan_gate(plan: str) -> ConcretePlanGate:
    """Check only the concrete fields needed to direct a Writer."""

    text = plan.strip()
    required = (
        ("具体触发事件", ("触发事件", "触发：")),
        ("推动事件的人", ("推动事件的人", "事件推动者", "谁推动")),
        ("主角行动", ("主角行动", "主角采取什么行动", "主角做什么")),
        ("对手或世界反应", ("对手或世界反应", "对手反应", "世界反应")),
        ("直接结果", ("直接结果", "本章结果", "结果：")),
        (
            "状态变化",
            (
                "状态变化",
                "能力变化",
                "资源变化",
                "知识变化",
                "身份变化",
                "关系变化",
                "地点变化",
                "风险变化",
                "承诺变化",
            ),
        ),
        ("叙事功能", ("叙事功能", "本章功能", "叙事作用")),
        ("结尾推动力", ("结尾推动力", "结尾：", "下一章直接压力", "结尾推动")),
    )
    missing = tuple(
        label for label, aliases in required if not any(alias in text for alias in aliases)
    )
    return ConcretePlanGate(passed=not missing, missing=missing)


def _visible_value(payload: Mapping[str, Any], key: str, default: str = "未填写") -> str:
    value = payload.get(key)
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value if str(item).strip()) or default
    text = str(value).strip() if value is not None else ""
    return text or default


def _author_input(mode: str, payload: Mapping[str, Any]) -> str:
    keys_by_mode = {
        "new_book": (
            ("暂定书名", "title"),
            ("一句话创意", "premise"),
            ("类型", "genre"),
            ("期待的读者体验", "reader_experience"),
            ("不希望出现的写法", "forbidden_style"),
            ("参考小说整体画像（仅在作者勾选进入 Prompt 时提供）", "reference_profile"),
        ),
        "next_batch": (
            ("已完成章节摘要", "completed_summaries"),
            ("当前大型剧情块", "current_block"),
            ("当前十章模块", "current_module"),
            ("当前故事状态", "current_state"),
            ("当前未兑现承诺", "debts"),
        ),
        "current_chapter": (
            ("核心类型与读者承诺", "core_promise"),
            ("必要世界规则", "world_rules"),
            ("主角稳定决策模式", "decision_mode"),
            ("当前章具体小纲", "chapter_plan"),
            ("最近1—3章摘要", "recent_summaries"),
            ("当前人物、资源、能力和关系", "current_state"),
            ("当前未兑现承诺", "debts"),
            ("本章不能违反的事实", "hard_facts"),
        ),
        "review": (
            ("原十章中纲", "original_ten_plan"),
            ("十章逐章小纲", "ten_chapter_plan"),
            ("实际十章摘要", "actual_summaries"),
            ("当前状态", "current_state"),
            ("当前未兑现承诺", "debts"),
        ),
    }
    rows = [f"- {label}：\n{_visible_value(payload, key)}" for label, key in keys_by_mode[mode]]
    return "\n".join(rows)


def _board_for_mode(mode: str, board: str) -> str:
    if mode == "new_book":
        return board.strip()
    names = {
        "next_batch": {
            "1. 新书整体画像",
            "6. 未来100章大型剧情块",
            "7. 十个十章中纲",
            "8. 未来十章逐章小纲",
            "9. 当前故事状态",
            "10. 当前未兑现承诺",
            "11. 最近章节摘要",
            "12. GBrain参考依据",
        },
        "current_chapter": {
            "1. 新书整体画像",
            "2. 小说价值观",
            "3. 世界观",
            "4. 主角",
            "6. 未来100章大型剧情块",
            "7. 十个十章中纲",
            "8. 未来十章逐章小纲",
            "9. 当前故事状态",
            "10. 当前未兑现承诺",
            "11. 最近章节摘要",
            "12. GBrain参考依据",
        },
        "review": {
            "6. 未来100章大型剧情块",
            "7. 十个十章中纲",
            "8. 未来十章逐章小纲",
            "9. 当前故事状态",
            "10. 当前未兑现承诺",
            "11. 最近章节摘要",
            "12. GBrain参考依据",
        },
    }[mode]
    chunks = [
        section.raw
        for section in parse_markdown_sections(board)
        if section.title in names or normalize_section_key(section.title) in {
            normalize_section_key(item) for item in names
        }
    ]
    return "\n\n".join(chunks).strip() or "当前没有可用的 Book Board 区块。"


def _reference_block(
    programs: tuple[ReferenceProgram, ...], payload: Mapping[str, Any]
) -> str:
    if not programs:
        return "本轮没有选择 Reference Program。"
    reason = str(payload.get("reference_reason") or "作者未填写采用原因").strip()
    lines = [f"本轮采用原因：{reason}"]
    for program in programs:
        lines.extend(["", "---", program.prompt_payload()])
    return "\n".join(lines)


def _replace(template: str, values: Mapping[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", value)
    return result.strip() + "\n"


def build_prompt(
    *,
    template_file: Path,
    mode: str,
    payload: Mapping[str, Any],
    board_markdown: str,
    references: list[ReferenceProgram],
) -> PromptBuildResult:
    if mode not in PROMPT_MODE_LABELS:
        raise ValueError(f"未知 Prompt 模式：{mode}")
    source = template_file.read_text(encoding="utf-8")
    template = template_for_mode(source, mode)
    gate = (
        concrete_plan_gate(str(payload.get("chapter_plan") or ""))
        if mode == "current_chapter"
        else None
    )
    warnings: list[str] = []
    if mode == "current_chapter" and not str(payload.get("recent_summaries") or "").strip():
        warnings.append("最近章节摘要尚未填写；Writer 仍可继续，但连续性依据较少。")
    if not references:
        warnings.append("本轮没有采用 Reference Program；这不是硬门失败。")
    include_profile = bool(payload.get("include_reference_profile", True))
    visible_payload = dict(payload)
    if not include_profile:
        visible_payload["reference_profile"] = "作者未勾选进入 Prompt"
    context = _author_input(mode, visible_payload)
    board = _board_for_mode(mode, board_markdown)
    reference_block = _reference_block(tuple(references), payload)
    filled = _replace(
        template,
        {
            "AUTHOR_INPUT": context,
            "BOOK_BOARD": board,
            "REFERENCE_PROGRAMS": reference_block,
        },
    )
    if gate is not None and not gate.passed:
        return PromptBuildResult(
            mode=mode,
            prompt=None,
            template=template,
            gate=gate,
            soft_warnings=tuple(warnings),
            references=tuple(references),
        )
    return PromptBuildResult(
        mode=mode,
        prompt=filled,
        template=template,
        gate=gate,
        soft_warnings=tuple(warnings),
        references=tuple(references),
    )


def prompt_payload_json(result: PromptBuildResult) -> str:
    """Useful for tests and the Developer Mode view without extra state."""

    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


__all__ = [
    "ConcretePlanGate",
    "PROMPT_MODE_LABELS",
    "PromptBuildResult",
    "build_prompt",
    "concrete_plan_gate",
    "prompt_payload_json",
    "template_for_mode",
]
