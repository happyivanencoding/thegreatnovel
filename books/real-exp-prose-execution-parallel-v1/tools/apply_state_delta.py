"""Apply the production State Delta parser to an experiment-local BOOK copy."""

from __future__ import annotations

import argparse
from pathlib import Path

from story_mvp.prompts import parse_state_delta_v2
from story_mvp.storage import apply_state_delta_to_book


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("book", type=Path)
    parser.add_argument("response", type=Path)
    parser.add_argument("chapter", type=int)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    book = args.book.read_text(encoding="utf-8")
    response = args.response.read_text(encoding="utf-8")
    parsed = parse_state_delta_v2(response)
    updated = apply_state_delta_to_book(book, args.chapter, response)
    args.snapshot.write_text(updated, encoding="utf-8")
    args.book.write_text(updated, encoding="utf-8")
    print(f"book={args.book}")
    print(f"snapshot={args.snapshot}")
    print("sections=" + ",".join(parsed))
    print(f"book_chars={len(updated)}")


if __name__ == "__main__":
    main()
