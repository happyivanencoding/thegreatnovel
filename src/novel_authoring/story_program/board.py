"""Readable Markdown state for the transparent Story Program workspace."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

BOARD_FILENAME = "BOOK_BOARD.md"
GBRAIN_PROMPTS_FILENAME = "GBRAIN_PROMPTS.md"
PROPOSAL_FILENAME = "PROPOSAL_DRAFT.md"
CHAPTERS_DIRNAME = "chapters"

_PLACEHOLDER_RE = re.compile(r"^(?:待|尚未|暂无|未建立|未填写|无|→)")
_TOP_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
_NESTED_HEADING_RE = re.compile(r"^###\s+(.+?)\s*$")


DEFAULT_BOARD_TEMPLATE = """# Book Board

> 这是作者权威工作板。Proposal、Codex 返回和软警告都不能自动覆盖它。

## 0. 基本信息

- 暂定书名：待作者填写
- 一句话创意：待作者填写
- 类型：待作者填写
- 期待的读者体验：待作者填写
- 不希望出现的写法：待作者填写

## 1. 新书整体画像

### 核心类型与读者承诺
待 Proposal 或作者填写。必须具体说明前期、中期和第100章结束时读者为什么继续追读。

### 类型升级路径
待 Proposal 或作者填写。说明类型升级发生在什么具体剧情变化上。

### 核心情节发动机
待 Proposal 或作者填写。先写具体循环，再写它如何升级。

### 主要爽点
待 Proposal 或作者填写。

### 长篇扩张方式
待 Proposal 或作者填写。说明每十章、每个大型块和第100章改变了什么。

### 主要重复风险
待 Proposal 或作者填写。

## 2. 小说价值观

### 故事赞赏什么
待 Proposal 或作者填写。

### 故事惩罚什么
待 Proposal 或作者填写。

### 核心价值冲突
待 Proposal 或作者填写。

### Worldview Claim
待 Proposal 或作者填写。

### Worldview Counterclaim
待 Proposal 或作者填写。

### 胜利意味着什么
待 Proposal 或作者填写。

### 哪些胜利方式会毁掉本书
待 Proposal 或作者填写。

## 3. 世界观

### 世界如何运转
待 Proposal 或作者填写。

### 核心资源
待 Proposal 或作者填写。

### 权力与社会秩序
待 Proposal 或作者填写。

### 普通人的上升渠道
待 Proposal 或作者填写。

### 成长门槛
待 Proposal 或作者填写。

### 世界如何持续制造剧情压力
待 Proposal 或作者填写。

### 主角优势如何改变玩法
待 Proposal 或作者填写。

### 主角优势的代价
待 Proposal 或作者填写。

### 不可随意修改的世界规则
待 Proposal 或作者填写。

### 当前未知秘密
待 Proposal 或作者填写。

## 4. 主角

### 主角起点
待 Proposal 或作者填写。

### 核心欲望
待 Proposal 或作者填写。

### 性格优势
待 Proposal 或作者填写。

### 性格缺口
待 Proposal 或作者填写。

### 稳定决策模式
待 Proposal 或作者填写。用箭头写出可重复的判断逻辑。

### 核心能力
待 Proposal 或作者填写。

### 能力边界
待 Proposal 或作者填写。

### 近期成长目标
待 Proposal 或作者填写。

### 中期成长目标
待 Proposal 或作者填写。

### 第100章目标状态
待 Proposal 或作者填写。

### 主角可能面对的价值反转
待 Proposal 或作者填写。

## 5. 关键人物与关系债务

待 Proposal 或作者填写。至少包含长期情感锚点、利益伙伴、立场变化者和价值矛盾揭示者。

## 6. 未来100章大型剧情块

待 Proposal 或作者填写。每块必须先写触发事件→主角行动→对手或世界反应→转折→高潮→具体结果
→新问题，再写叙事功能。

## 7. 十个十章中纲

待 Proposal 或作者填写。每段都要是一段具体故事，不是抽象功能标签。

## 8. 未来十章逐章小纲

待 Proposal 或作者填写。每章必须有具体事件、直接结果、状态变化、叙事功能和结尾推动力。

## 9. 当前故事状态

- 已完成章节：0
- 当前大型剧情块：尚未建立
- 当前十章模块：尚未建立
- 当前地点：待作者填写
- 当前人物、资源、能力和关系：待作者填写

## 10. 当前未兑现承诺

待 Proposal 或作者填写。每项写清建立位置、当前进度、下一次具体推进和允许延后的理由。

## 11. 最近章节摘要

尚未有正式章节。

## 12. GBrain参考依据

尚未选择 Reference Program。整体蒸馏画像和每轮采用原因由作者明确填写。

## 13. 作者备注

待作者填写。
"""


@dataclass(frozen=True, slots=True)
class StoryProgramPaths:
    """Author-facing files for one Book Library project."""

    root: Path

    @property
    def board(self) -> Path:
        return self.root / BOARD_FILENAME

    @property
    def prompts(self) -> Path:
        return self.root / GBRAIN_PROMPTS_FILENAME

    @property
    def proposal(self) -> Path:
        return self.root / PROPOSAL_FILENAME

    @property
    def chapters(self) -> Path:
        return self.root / CHAPTERS_DIRNAME


@dataclass(frozen=True, slots=True)
class MarkdownSection:
    """One top-level ``##`` Markdown block."""

    key: str
    title: str
    body: str
    raw: str


def paths_for_book(book_root: Path) -> StoryProgramPaths:
    return StoryProgramPaths(Path(book_root).expanduser().resolve() / "story_program")


def ensure_workspace(paths: StoryProgramPaths, prompt_template: str) -> None:
    """Create only the transparent workspace scaffolding, never the Board."""

    paths.root.mkdir(parents=True, exist_ok=True)
    paths.chapters.mkdir(parents=True, exist_ok=True)
    if not paths.prompts.exists():
        paths.prompts.write_text(prompt_template, encoding="utf-8", newline="\n")


def read_board(paths: StoryProgramPaths) -> str:
    if not paths.board.is_file():
        return DEFAULT_BOARD_TEMPLATE
    return paths.board.read_text(encoding="utf-8")


def save_board(paths: StoryProgramPaths, markdown: str) -> Path:
    content = markdown.strip()
    if not content:
        raise ValueError("BOOK_BOARD.md 不能保存为空")
    if not content.startswith("# Book Board"):
        content = "# Book Board\n\n" + content
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.board.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    return paths.board


def read_proposal(paths: StoryProgramPaths) -> str:
    if not paths.proposal.is_file():
        return ""
    return paths.proposal.read_text(encoding="utf-8")


def parse_markdown_sections(markdown: str) -> list[MarkdownSection]:
    """Parse simple top-level sections without attempting a semantic merge."""

    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = _TOP_HEADING_RE.match(line)
        if match:
            title = match.group(1).strip()
            starts.append((index, title, normalize_section_key(title)))
    sections: list[MarkdownSection] = []
    for position, (start, title, key) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw = "\n".join(lines[start:end]).strip()
        body = "\n".join(lines[start + 1 : end]).strip()
        sections.append(MarkdownSection(key=key, title=title, body=body, raw=raw))
    return sections


def normalize_section_key(title: str) -> str:
    normalized = re.sub(r"^\s*\d+(?:[.、)]\s*|\s+)", "", title.strip())
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.casefold()


def section_map(markdown: str) -> dict[str, MarkdownSection]:
    return {section.key: section for section in parse_markdown_sections(markdown)}


def first_meaningful_line(text: str, fallback: str = "尚未建立") -> str:
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("-*> ")
        if not line or line.startswith("#"):
            continue
        if _PLACEHOLDER_RE.match(line):
            continue
        return line
    return fallback


def nested_heading(text: str, fallback: str = "尚未建立") -> str:
    match = _NESTED_HEADING_RE.search(text)
    return match.group(1).strip() if match else fallback


def board_summary(markdown: str, completed_chapters: int) -> dict[str, object]:
    sections = section_map(markdown)

    def body(name: str) -> str:
        section = sections.get(normalize_section_key(name))
        return "" if section is None else section.body

    current_status = body("9. 当前故事状态")
    future_blocks = body("6. 未来100章大型剧情块")
    ten_chapters = body("7. 十个十章中纲")
    next_chapters = body("8. 未来十章逐章小纲")
    debts = body("10. 当前未兑现承诺")
    future_preview = first_meaningful_line(future_blocks, "")
    next_chapter_preview = first_meaningful_line(next_chapters, "")
    return {
        "completed_chapters": completed_chapters,
        "current_block": nested_heading(future_blocks),
        "current_module": nested_heading(ten_chapters),
        "next_chapter": next_chapter_preview or "尚未准备未来十章",
        "important_debt": first_meaningful_line(debts, "当前没有已填写的未兑现承诺"),
        "future_direction_ready": bool(future_preview),
        "next_ten_ready": bool(next_chapter_preview),
        "state_preview": first_meaningful_line(current_status),
    }


def initial_board(
    *,
    title: str,
    premise: str,
    genre: str = "",
    reader_experience: str = "",
    forbidden_style: str = "",
) -> str:
    board = DEFAULT_BOARD_TEMPLATE
    basic = (
        "## 0. 基本信息\n\n"
        f"- 暂定书名：{title.strip() or '待作者填写'}\n"
        f"- 一句话创意：{premise.strip() or '待作者填写'}\n"
        f"- 类型：{genre.strip() or '待作者填写'}\n"
        f"- 期待的读者体验：{reader_experience.strip() or '待作者填写'}\n"
        f"- 不希望出现的写法：{forbidden_style.strip() or '待作者填写'}"
    )
    return replace_sections(board, {normalize_section_key("0. 基本信息"): basic})


def replace_sections(markdown: str, replacements: dict[str, str]) -> str:
    """Replace only selected top-level sections, preserving all other Markdown."""

    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = _TOP_HEADING_RE.match(line)
        if match:
            starts.append((index, normalize_section_key(match.group(1))))
    if not starts:
        return markdown.rstrip() + "\n"

    output: list[str] = []
    cursor = 0
    found: set[str] = set()
    for position, (start, key) in enumerate(starts):
        output.extend(lines[cursor:start])
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        replacement = replacements.get(key)
        if replacement is None:
            output.extend(lines[start:end])
        else:
            output.extend(replacement.strip().splitlines())
            found.add(key)
        cursor = end
    output.extend(lines[cursor:])
    for key, replacement in replacements.items():
        if key not in found and key not in {item[1] for item in starts}:
            output.extend(["", replacement.strip()])
    return "\n".join(output).rstrip() + "\n"


__all__ = [
    "BOARD_FILENAME",
    "CHAPTERS_DIRNAME",
    "DEFAULT_BOARD_TEMPLATE",
    "GBRAIN_PROMPTS_FILENAME",
    "MarkdownSection",
    "PROPOSAL_FILENAME",
    "StoryProgramPaths",
    "board_summary",
    "ensure_workspace",
    "first_meaningful_line",
    "initial_board",
    "normalize_section_key",
    "parse_markdown_sections",
    "paths_for_book",
    "read_board",
    "read_proposal",
    "replace_sections",
    "save_board",
    "section_map",
]
