from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .prompts import DEFAULT_PROMPT_TEMPLATES


SECTION_TITLES = {
    "core": "# 小说核心与读者承诺",
    "values_world": "# 价值观与世界观",
    "protagonist": "# 主角、能力与关键关系",
    "long_plan": "# 未来100章大型剧情块",
    "small_plan": "# 未来十章逐章小纲",
    "status": "# 当前状态、未兑现承诺与作者备注",
}

PROMPT_TEMPLATE_LABELS = {
    "outline": "新书/总纲规划",
    "chapter": "当前章节写作",
    "review": "十章复盘与下一批十章",
}

BOOK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def default_book_content() -> str:
    bodies = {
        "core": "一句话创意：\n\n读者承诺：",
        "values_world": "价值观：\n\n会主动制造压力的世界规则：",
        "protagonist": "稳定决策模式：\n\n能力玩法及代价：\n\n关键长期关系：",
        "long_plan": "（先写具体事件链，再写叙事功能。）",
        "small_plan": "（每章请使用八个字段写出可执行的小纲。）",
        "status": "当前状态：\n\n未兑现承诺：\n\n作者备注：",
    }
    return compose_book_content(bodies)


def compose_book_content(sections: dict[str, str]) -> str:
    chunks: list[str] = []
    for key, title in SECTION_TITLES.items():
        chunks.append(f"{title}\n\n{sections.get(key, '').strip()}")
    return "\n\n".join(chunks).rstrip() + "\n"


def parse_book_sections(content: str) -> dict[str, str]:
    headings = {title: key for key, title in SECTION_TITLES.items()}
    sections = {key: "" for key in SECTION_TITLES}
    current_key: str | None = None
    lines: list[str] = []
    for line in content.splitlines():
        title = line.strip()
        if title in headings:
            if current_key is not None:
                sections[current_key] = "\n".join(lines).strip()
            current_key = headings[title]
            lines = []
            continue
        if current_key is not None:
            lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(lines).strip()
    return sections


def prompt_templates_to_text(templates: dict[str, str]) -> str:
    chunks: list[str] = []
    for key, label in PROMPT_TEMPLATE_LABELS.items():
        chunks.append(f"# {label}\n\n{templates.get(key, '').strip()}")
    return "\n\n".join(chunks).rstrip() + "\n"


def text_to_prompt_templates(content: str) -> dict[str, str]:
    headings = {f"# {label}": key for key, label in PROMPT_TEMPLATE_LABELS.items()}
    templates = {key: "" for key in PROMPT_TEMPLATE_LABELS}
    current_key: str | None = None
    lines: list[str] = []
    for line in content.splitlines():
        title = line.strip()
        if title in headings:
            if current_key is not None:
                templates[current_key] = "\n".join(lines).strip()
            current_key = headings[title]
            lines = []
            continue
        if current_key is not None:
            lines.append(line)
    if current_key is not None:
        templates[current_key] = "\n".join(lines).strip()
    return templates


def default_prompt_templates() -> dict[str, str]:
    return dict(DEFAULT_PROMPT_TEMPLATES)


def validate_book_id(book_id: str) -> str:
    value = book_id.strip()
    if not BOOK_ID_PATTERN.fullmatch(value):
        raise ValueError("book_id 只能包含字母、数字、下划线和短横线，且必须以字母或数字开头")
    return value


def book_directory(book_id: str, workspace: Path) -> Path:
    return workspace / validate_book_id(book_id)


def create_book(book_id: str, workspace: Path) -> Path:
    workspace.mkdir(parents=True, exist_ok=True)
    directory = book_directory(book_id, workspace)
    if directory.exists():
        raise FileExistsError(f"小说已存在：{book_id}")
    directory.mkdir()
    (directory / "chapters").mkdir()
    (directory / "BOOK.md").write_text(default_book_content(), encoding="utf-8")
    (directory / "PROMPTS.md").write_text(
        prompt_templates_to_text(default_prompt_templates()), encoding="utf-8"
    )
    (directory / "PROPOSAL.md").write_text("", encoding="utf-8")
    return directory


def list_books(workspace: Path) -> list[str]:
    if not workspace.exists():
        return []
    return sorted(
        directory.name
        for directory in workspace.iterdir()
        if directory.is_dir() and (directory / "BOOK.md").is_file()
    )


def require_book(book_id: str, workspace: Path) -> Path:
    directory = book_directory(book_id, workspace)
    if not (directory / "BOOK.md").is_file():
        raise FileNotFoundError(f"找不到小说：{book_id}")
    return directory


def read_book_payload(book_id: str, workspace: Path) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    book_content = (directory / "BOOK.md").read_text(encoding="utf-8")
    prompt_content = (directory / "PROMPTS.md").read_text(encoding="utf-8")
    return {
        "book_id": book_id,
        "book_content": book_content,
        "sections": parse_book_sections(book_content),
        "prompt_templates": text_to_prompt_templates(prompt_content),
        "proposal": (directory / "PROPOSAL.md").read_text(encoding="utf-8"),
        "chapters": sorted(path.name for path in (directory / "chapters").glob("chapter-*.md")),
    }


def write_book(book_id: str, content: str, workspace: Path) -> None:
    directory = require_book(book_id, workspace)
    (directory / "BOOK.md").write_text(content, encoding="utf-8")


def write_prompt_templates(book_id: str, templates: dict[str, str], workspace: Path) -> None:
    directory = require_book(book_id, workspace)
    normalized = {
        key: str(templates.get(key, "")) for key in PROMPT_TEMPLATE_LABELS
    }
    (directory / "PROMPTS.md").write_text(
        prompt_templates_to_text(normalized), encoding="utf-8"
    )


def write_proposal(book_id: str, content: str, workspace: Path) -> None:
    directory = require_book(book_id, workspace)
    (directory / "PROPOSAL.md").write_text(content, encoding="utf-8")


def save_chapter(book_id: str, chapter_number: int, content: str, workspace: Path) -> Path:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    if not content.strip():
        raise ValueError("章节正文不能为空")
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    target.write_text(content, encoding="utf-8")
    return target
