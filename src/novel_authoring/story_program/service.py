"""File-backed Story Program operations with explicit author write boundaries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from novel_authoring.story_program.board import (
    StoryProgramPaths,
    board_summary,
    ensure_workspace,
    initial_board,
    parse_markdown_sections,
    paths_for_book,
    read_board,
    read_proposal,
)
from novel_authoring.story_program.board import (
    save_board as write_board,
)
from novel_authoring.story_program.proposal import ProposalDraft, parse_proposal
from novel_authoring.story_program.reference_programs import (
    DEFAULT_REFERENCE_ROOT,
    load_reference_programs,
)

_CHAPTER_RE = re.compile(r"^chapter-(\d{4})\.md$")
_PROMPT_TEMPLATE_PATH = Path(__file__).with_name("GBRAIN_PROMPTS.md")


@dataclass(frozen=True, slots=True)
class ChapterFile:
    number: int
    title: str
    path: Path
    content: str
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "path": str(self.path),
            "summary": self.summary,
        }


def prepare_paths(book_root: Path) -> StoryProgramPaths:
    paths = paths_for_book(book_root)
    ensure_workspace(paths, _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8"))
    return paths


def _chapter_title(content: str, number: int) -> str:
    for line in content.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line.strip())
        if match:
            return match.group(1).strip()
    return f"第{number}章"


def _chapter_summary(content: str) -> str:
    marker = "# Chapter Commit"
    if marker in content:
        summary = content.split(marker, 1)[1].strip()
        return summary[:1200]
    body = content.strip()
    return body[:600]


def list_chapters(paths: StoryProgramPaths) -> list[ChapterFile]:
    result: list[ChapterFile] = []
    if not paths.chapters.is_dir():
        return result
    for path in sorted(paths.chapters.glob("chapter-*.md")):
        match = _CHAPTER_RE.match(path.name)
        if match is None:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        number = int(match.group(1))
        result.append(
            ChapterFile(
                number=number,
                title=_chapter_title(content, number),
                path=path,
                content=content,
                summary=_chapter_summary(content),
            )
        )
    return result


def story_program_view(
    book_root: Path,
    *,
    reference_root: Path | None = None,
    include_provisional: bool = False,
    reference_query: str = "",
) -> dict[str, Any]:
    paths = prepare_paths(book_root)
    board = read_board(paths)
    chapters = list_chapters(paths)
    proposal = parse_proposal(read_proposal(paths))
    programs = load_reference_programs(
        reference_root or DEFAULT_REFERENCE_ROOT,
        include_provisional=include_provisional,
        query=reference_query,
    )
    summaries = board_summary(board, len(chapters))
    summaries["recent_chapter_summaries"] = [
        {"number": item.number, "title": item.title, "summary": item.summary}
        for item in chapters[-3:]
    ]
    return {
        "paths": {
            "root": str(paths.root),
            "board": str(paths.board),
            "prompts": str(paths.prompts),
            "proposal": str(paths.proposal),
            "chapters": str(paths.chapters),
        },
        "board_markdown": board,
        "board_sections": [
            {
                "key": item.key,
                "title": item.title,
                "body": item.body,
                "raw": item.raw,
            }
            for item in parse_markdown_sections(board)
        ],
        "board_is_saved": paths.board.is_file(),
        "prompt_templates": paths.prompts.read_text(encoding="utf-8"),
        "proposal": proposal.to_dict(),
        "programs": [item.to_dict() for item in programs],
        "chapters": [item.to_dict() for item in chapters],
        "next_chapter_number": (chapters[-1].number + 1) if chapters else 1,
        "summary": summaries,
        "reference_root": str((reference_root or DEFAULT_REFERENCE_ROOT).expanduser()),
        "include_provisional": include_provisional,
    }


def save_story_board(book_root: Path, markdown: str) -> dict[str, str]:
    paths = prepare_paths(book_root)
    path = write_board(paths, markdown)
    return {"path": str(path), "board_markdown": path.read_text(encoding="utf-8")}


def save_initial_story_board(
    book_root: Path,
    *,
    title: str,
    premise: str,
    genre: str = "",
    reader_experience: str = "",
    forbidden_style: str = "",
) -> dict[str, str]:
    return save_story_board(
        book_root,
        initial_board(
            title=title,
            premise=premise,
            genre=genre,
            reader_experience=reader_experience,
            forbidden_style=forbidden_style,
        ),
    )


def import_proposal(book_root: Path, raw: str) -> ProposalDraft:
    paths = prepare_paths(book_root)
    paths.proposal.write_text(raw, encoding="utf-8", newline="\n")
    return parse_proposal(raw)


def adopt_proposal(
    book_root: Path,
    *,
    selected_keys: list[str],
    base_board: str | None = None,
) -> dict[str, Any]:
    paths = prepare_paths(book_root)
    proposal = parse_proposal(read_proposal(paths))
    if proposal.parse_error and not proposal.adoptable_sections:
        raise ValueError(proposal.parse_error)
    from novel_authoring.story_program.proposal import adopt_sections

    current = base_board if base_board is not None else read_board(paths)
    updated = adopt_sections(current, proposal, selected_keys)
    path = write_board(paths, updated)
    return {
        "path": str(path),
        "board_markdown": path.read_text(encoding="utf-8"),
        "selected_sections": selected_keys,
        "proposal": proposal.to_dict(),
    }


def save_chapter(
    book_root: Path,
    *,
    chapter_number: int,
    title: str,
    chapter_markdown: str,
    chapter_commit: str = "",
) -> dict[str, Any]:
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1—9999 之间")
    paths = prepare_paths(book_root)
    chapters = list_chapters(paths)
    expected = chapters[-1].number + 1 if chapters else 1
    if chapter_number != expected:
        raise ValueError(f"下一章应保存为第 {expected} 章，不能跳号或覆盖既有章节")
    content = chapter_markdown.strip()
    if not content:
        raise ValueError("章节正文不能为空")
    if not re.match(r"^#\s+", content):
        content = f"# 第{chapter_number}章 {title.strip() or '未命名'}\n\n{content}"
    if chapter_commit.strip() and "# Chapter Commit" not in content:
        content = f"{content.rstrip()}\n\n---\n\n# Chapter Commit\n\n{chapter_commit.strip()}"
    path = paths.chapters / f"chapter-{chapter_number:04d}.md"
    if path.exists():
        raise FileExistsError(f"章节文件已存在：{path.name}")
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    return {
        "path": str(path),
        "chapter_number": chapter_number,
        "title": _chapter_title(content, chapter_number),
        "canon_changed": False,
        "chapter": ChapterFile(
            chapter_number,
            _chapter_title(content, chapter_number),
            path,
            content,
            _chapter_summary(content),
        ).to_dict(),
    }


__all__ = [
    "ChapterFile",
    "adopt_proposal",
    "import_proposal",
    "list_chapters",
    "prepare_paths",
    "save_chapter",
    "save_initial_story_board",
    "save_story_board",
    "story_program_view",
]
