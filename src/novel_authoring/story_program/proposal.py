"""Simple Markdown Proposal parsing and explicit section adoption."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from novel_authoring.story_program.board import (
    MarkdownSection,
    normalize_section_key,
    parse_markdown_sections,
    replace_sections,
)

KNOWN_BOARD_SECTION_KEYS = frozenset(
    normalize_section_key(item)
    for item in (
        "0. 基本信息",
        "1. 新书整体画像",
        "2. 小说价值观",
        "3. 世界观",
        "4. 主角",
        "5. 关键人物与关系债务",
        "6. 未来100章大型剧情块",
        "7. 十个十章中纲",
        "8. 未来十章逐章小纲",
        "9. 当前故事状态",
        "10. 当前未兑现承诺",
        "11. 最近章节摘要",
        "12. GBrain参考依据",
        "13. 作者备注",
    )
)


@dataclass(frozen=True, slots=True)
class ProposalDraft:
    raw: str
    sections: tuple[MarkdownSection, ...]
    adoptable_sections: tuple[MarkdownSection, ...]
    parse_error: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw": self.raw,
            "parse_error": self.parse_error,
            "sections": [
                {
                    "key": section.key,
                    "title": section.title,
                    "body": section.body,
                    "raw": section.raw,
                    "adoptable": section in self.adoptable_sections,
                }
                for section in self.sections
            ],
        }


def parse_proposal(raw: str) -> ProposalDraft:
    content = raw.strip()
    sections = tuple(parse_markdown_sections(content))
    adoptable = tuple(section for section in sections if section.key in KNOWN_BOARD_SECTION_KEYS)
    if not content:
        error = "尚未粘贴 Codex 返回内容。"
    elif not sections:
        error = "未找到 ## 顶层区块；保留完整原文，需作者手动复制或补充标题。"
    elif not adoptable:
        error = "找到了 Markdown 标题，但没有匹配 Book Board 区块；不会自动修改正式内容。"
    else:
        error = None
    return ProposalDraft(
        raw=raw,
        sections=sections,
        adoptable_sections=adoptable,
        parse_error=error,
    )


def adopt_sections(
    current_board: str,
    proposal: ProposalDraft,
    selected_keys: list[str],
) -> str:
    requested = {str(item).strip().casefold() for item in selected_keys if str(item).strip()}
    replacements = {
        section.key: section.raw
        for section in proposal.adoptable_sections
        if section.key in requested
    }
    if not replacements:
        raise ValueError("没有选择可采用的 Proposal 区块")
    return replace_sections(current_board, replacements)


__all__ = [
    "KNOWN_BOARD_SECTION_KEYS",
    "ProposalDraft",
    "adopt_sections",
    "parse_proposal",
]
