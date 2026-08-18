from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .prompts import DEFAULT_PROMPT_TEMPLATES


SECTION_TITLES = {
    "design": "# 小说总体设计画像",
    "long_plan": "# 未来100章大型剧情块",
    "small_plan": "# 未来十章逐章小纲",
    "status": "# 当前状态、未兑现承诺与作者备注",
}

DESIGN_SECTION_TITLES = {
    "growth_genome": "## 0. 本书成长基因图",
    "type_promise": "## 1. 核心类型与读者承诺",
    "world_structure": "## 2. 世界观结构",
    "world_pressure": "## 3. 世界如何持续制造剧情压力",
    "protagonist_model": "## 4. 主角模型、人物弧与核心矛盾",
    "relationships": "## 5. 配角与关系系统",
    "plot_engine": "## 6. 核心情节发动机",
    "narrative_structure": "## 7. 叙事结构",
    "prose": "## 8. 文风与可操作参数",
    "dialogue": "## 9. 对话特点",
    "rhythm": "## 10. 节奏结构",
    "theme": "## 11. 主题、价值观与长期问题",
    "strengths_risks": "## 12. 当前设计最强点与最弱点",
}

PROMPT_TEMPLATE_LABELS = {
    "idea": "男频爽文创意生成",
    "outline": "新书/总纲规划",
    "chapter": "当前章节写作",
    "review": "十章复盘与下一批十章",
}

BOOK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def default_book_content() -> str:
    design_bodies = {
        key: "（请填写这项总体设计。）" for key in DESIGN_SECTION_TITLES
    }
    bodies = {
        "design": compose_design_content(design_bodies),
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


def compose_design_content(design_sections: dict[str, str]) -> str:
    chunks: list[str] = []
    for key, title in DESIGN_SECTION_TITLES.items():
        chunks.append(f"{title}\n\n{design_sections.get(key, '').strip()}")
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


def parse_design_sections(content: str) -> dict[str, str]:
    headings = {title: key for key, title in DESIGN_SECTION_TITLES.items()}
    sections = {key: "" for key in DESIGN_SECTION_TITLES}
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
    sections = parse_book_sections(book_content)
    return {
        "book_id": book_id,
        "book_content": book_content,
        "sections": sections,
        "design_sections": parse_design_sections(sections["design"]),
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
    if target.exists():
        raise ValueError(f"第{chapter_number}章已经存在，请先明确处理已有章节")
    target.write_text(content, encoding="utf-8")
    return target


def read_chapter(book_id: str, chapter_number: int, workspace: Path) -> str:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    if not target.is_file():
        return ""
    return target.read_text(encoding="utf-8")
