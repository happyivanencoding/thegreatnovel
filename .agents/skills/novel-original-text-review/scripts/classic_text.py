from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_TGN_GBRAIN_ROOT = Path(r"C:\GoogleDrive\笔记\50_Corpora\TGN")
CLASSIC_LIBRARY_SUBDIRS = ("400+本高质量完本合集", "起点精选小说合集", "小说整理合集")
DEFAULT_ROOTS = tuple(DEFAULT_TGN_GBRAIN_ROOT / name for name in CLASSIC_LIBRARY_SUBDIRS)

ALIASES = {
    "斗破苍穹": "斗破",
    "斗破": "斗破",
    "斗罗": "斗罗大陆",
}

ENCODINGS = ("utf-8-sig", "utf-8", "gb18030")
CHAPTER_RE = re.compile(
    r"^\s*第\s*([0-9零〇一二三四五六七八九十百千万两]+)\s*章(?:\s*[:：、.-]?\s*)(.*)$"
)
TITLE_WRAPPER_RE = re.compile(r"^[《〈]\s*(.+?)\s*[》〉](.*)$")
SUFFIX_RE = re.compile(r"[（(].*?(?:校对|精校|全本|完本|番外|TXT|txt).*?[）)]")


@dataclass(frozen=True)
class Book:
    title: str
    path: Path
    size_bytes: int


@dataclass(frozen=True)
class Chapter:
    number: int | None
    ordinal: int
    heading: str
    title: str
    start_line: int
    end_line: int
    text: str


def roots_from_env() -> tuple[Path, ...]:
    raw = os.environ.get("TGN_CLASSIC_LIBRARY_ROOTS", "").strip()
    if raw:
        return tuple(Path(part) for part in raw.split(";") if part.strip())
    gbrain_root = os.environ.get("TGN_GBRAIN_ROOT", "").strip()
    if gbrain_root:
        root = Path(gbrain_root)
        return tuple(root / name for name in CLASSIC_LIBRARY_SUBDIRS)
    return DEFAULT_ROOTS


def normalize_title(value: str) -> str:
    text = value.strip()
    match = TITLE_WRAPPER_RE.match(text)
    if match:
        text = match.group(1)
    text = SUFFIX_RE.sub("", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[·•:：—_\-]+", "", text)
    return text.casefold()


def title_from_filename(path: Path) -> str:
    stem = path.stem.strip()
    match = TITLE_WRAPPER_RE.match(stem)
    if match:
        return match.group(1).strip()
    return SUFFIX_RE.sub("", stem).strip()


def discover_books(roots: Iterable[Path]) -> list[Book]:
    books: list[Book] = []
    seen: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.txt"):
            try:
                resolved = str(path.resolve()).casefold()
                if resolved in seen:
                    continue
                seen.add(resolved)
                books.append(Book(title_from_filename(path), path, path.stat().st_size))
            except OSError:
                continue
    books.sort(key=lambda item: (normalize_title(item.title), str(item.path)))
    return books


def resolve_book(title: str, roots: Iterable[Path]) -> tuple[Book, list[Book]]:
    books = discover_books(roots)
    requested = normalize_title(ALIASES.get(title, title))
    if not requested:
        raise ValueError("title 不能为空")

    def rank(book: Book) -> tuple[int, int, int, str]:
        candidate = normalize_title(book.title)
        if candidate == requested:
            level = 0
        elif candidate.startswith(requested) or requested.startswith(candidate):
            level = 1
        elif requested in candidate or candidate in requested:
            level = 2
        else:
            level = 9
        sequel_penalty = 1 if re.search(r"(?:II|III|IV|Ⅱ|Ⅲ|Ⅳ|2|3|4|二|三|四)", book.title) else 0
        return (level, sequel_penalty, abs(len(candidate) - len(requested)), str(book.path))

    ranked = sorted((book for book in books if rank(book)[0] < 9), key=rank)
    if not ranked:
        raise FileNotFoundError(f"本地完整原著库中未找到：{title}")
    return ranked[0], ranked[1:6]


def read_book(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    for encoding in ENCODINGS:
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeError(f"无法用 {', '.join(ENCODINGS)} 解码：{path}")


def chinese_number(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    token = token.replace("两", "二").replace("〇", "零")
    digits = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    units = {"十": 10, "百": 100, "千": 1000, "万": 10000}
    if not token or any(ch not in digits and ch not in units for ch in token):
        return None
    total = 0
    section = 0
    number = 0
    for ch in token:
        if ch in digits:
            number = digits[ch]
            continue
        unit = units[ch]
        if unit == 10000:
            section = (section + number) * unit
            total += section
            section = 0
            number = 0
        else:
            if number == 0:
                number = 1
            section += number * unit
            number = 0
    return total + section + number


def parse_chapters(text: str) -> list[Chapter]:
    lines = text.splitlines()
    markers: list[tuple[int, int | None, str, str]] = []
    for index, raw in enumerate(lines, start=1):
        match = CHAPTER_RE.match(raw.strip())
        if not match:
            continue
        number = chinese_number(match.group(1))
        heading = raw.strip()
        title = match.group(2).strip()
        markers.append((index, number, heading, title))
    chapters: list[Chapter] = []
    for ordinal, marker in enumerate(markers, start=1):
        start_line, number, heading, title = marker
        end_line = markers[ordinal][0] - 1 if ordinal < len(markers) else len(lines)
        body = "\n".join(lines[start_line - 1 : end_line]).strip()
        chapters.append(Chapter(number, ordinal, heading, title, start_line, end_line, body))
    return chapters


def choose_chapter(
    chapters: list[Chapter], *, number: int | None = None, ordinal: int | None = None
) -> Chapter:
    if ordinal is not None:
        if 1 <= ordinal <= len(chapters):
            return chapters[ordinal - 1]
        raise LookupError(f"未找到 ordinal {ordinal}；已解析 {len(chapters)} 章")
    if number is None:
        raise ValueError("必须提供 chapter 或 ordinal")
    by_number = [chapter for chapter in chapters if chapter.number == number]
    if len(by_number) == 1:
        return by_number[0]
    if len(by_number) > 1:
        candidates = ", ".join(
            f"ordinal={chapter.ordinal} {chapter.heading}" for chapter in by_number[:8]
        )
        raise LookupError(
            f"章号 {number} 在该书中重复出现；请使用 search 返回的唯一 --ordinal。候选：{candidates}"
        )
    raise LookupError(f"未找到第 {number} 章；已解析 {len(chapters)} 章")


def terms_from_query(query: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"[\s|,，]+", query) if part.strip()]
    return list(dict.fromkeys(parts))


def search_chapters(chapters: list[Chapter], query: str, limit: int) -> list[dict[str, object]]:
    terms = terms_from_query(query)
    if not terms:
        raise ValueError("query 不能为空")
    rows: list[tuple[int, Chapter, list[str]]] = []
    for chapter in chapters:
        score = 0
        matched: list[str] = []
        for term in terms:
            count = chapter.text.count(term)
            if count:
                matched.append(term)
                score += min(count, 12)
            if term in chapter.heading:
                score += 8
        if score:
            rows.append((score, chapter, matched))
    rows.sort(key=lambda item: (-item[0], item[1].ordinal))
    return [
        {
            "chapter": chapter.number,
            "ordinal": chapter.ordinal,
            "heading": chapter.heading,
            "source_lines": [chapter.start_line, chapter.end_line],
            "score": score,
            "matched_terms": matched,
        }
        for score, chapter, matched in rows[:limit]
    ]


def catalog_payload(query: str, limit: int, roots: tuple[Path, ...]) -> dict[str, object]:
    books = discover_books(roots)
    if query.strip():
        needle = normalize_title(query)
        books = [book for book in books if needle in normalize_title(book.title)]
    return {
        "roots": [str(root) for root in roots if root.exists()],
        "count": len(books),
        "books": [
            {"title": book.title, "path": str(book.path), "size_bytes": book.size_bytes}
            for book in books[:limit]
        ],
    }


def window_text(book: Book, encoding: str, selected: list[Chapter]) -> str:
    first = selected[0]
    last = selected[-1]
    title = book.title
    meta = [
        "# ORIGINAL TEXT READING WINDOW",
        f"book: {title}",
        f"source_path: {book.path}",
        f"encoding: {encoding}",
        f"chapters: {first.heading} -> {last.heading}",
        f"source_lines: {first.start_line}-{last.end_line}",
        "continuous_window: YES",
        "gbrain_used_as_original_evidence: NO",
        "",
        "--- ORIGINAL TEXT START ---",
        "",
    ]
    body = "\n\n".join(chapter.text for chapter in selected)
    return "\n".join(meta) + body + "\n\n--- ORIGINAL TEXT END ---\n"


def cmd_resolve(args: argparse.Namespace, roots: tuple[Path, ...]) -> dict[str, object]:
    book, alternatives = resolve_book(args.title, roots)
    return {
        "title": book.title,
        "path": str(book.path),
        "size_bytes": book.size_bytes,
        "alternatives": [{"title": item.title, "path": str(item.path)} for item in alternatives],
    }


def cmd_search(args: argparse.Namespace, roots: tuple[Path, ...]) -> dict[str, object]:
    book, _ = resolve_book(args.title, roots)
    text, encoding = read_book(book.path)
    chapters = parse_chapters(text)
    if not chapters:
        raise RuntimeError(f"未能从完整原著解析章节：{book.path}")
    return {
        "book": book.title,
        "source_path": str(book.path),
        "encoding": encoding,
        "parsed_chapters": len(chapters),
        "query": args.query,
        "results": search_chapters(chapters, args.query, args.limit),
    }


def cmd_window(args: argparse.Namespace, roots: tuple[Path, ...]) -> dict[str, object]:
    book, _ = resolve_book(args.title, roots)
    text, encoding = read_book(book.path)
    chapters = parse_chapters(text)
    if not chapters:
        raise RuntimeError(f"未能从完整原著解析章节：{book.path}")
    center = choose_chapter(chapters, number=args.chapter, ordinal=args.ordinal)
    start_index = max(0, center.ordinal - 1 - args.before)
    end_index = min(len(chapters), center.ordinal + args.after)
    selected = chapters[start_index:end_index]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(window_text(book, encoding, selected), encoding="utf-8")
    return {
        "book": book.title,
        "source_path": str(book.path),
        "encoding": encoding,
        "out": str(out),
        "window": [
            {
                "chapter": chapter.number,
                "ordinal": chapter.ordinal,
                "heading": chapter.heading,
                "source_lines": [chapter.start_line, chapter.end_line],
            }
            for chapter in selected
        ],
        "continuous_window": True,
        "gbrain_used_as_original_evidence": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TGN local classic original-text locator")
    sub = parser.add_subparsers(dest="command", required=True)

    catalog = sub.add_parser("catalog")
    catalog.add_argument("--query", default="")
    catalog.add_argument("--limit", type=int, default=100)

    resolve = sub.add_parser("resolve")
    resolve.add_argument("--title", required=True)

    search = sub.add_parser("search")
    search.add_argument("--title", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=8)

    window = sub.add_parser("window")
    window.add_argument("--title", required=True)
    locator = window.add_mutually_exclusive_group(required=True)
    locator.add_argument("--chapter", type=int)
    locator.add_argument("--ordinal", type=int)
    window.add_argument("--before", type=int, default=0)
    window.add_argument("--after", type=int, default=0)
    window.add_argument("--out", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    roots = roots_from_env()
    try:
        if args.command == "catalog":
            payload = catalog_payload(args.query, args.limit, roots)
        elif args.command == "resolve":
            payload = cmd_resolve(args, roots)
        elif args.command == "search":
            payload = cmd_search(args, roots)
        else:
            payload = cmd_window(args, roots)
    except Exception as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **payload}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
