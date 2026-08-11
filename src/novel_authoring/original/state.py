"""Small registry helpers shared by original workflows and hard gates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookRegistry, CreationMode


def original_record(database: Any, book_id: str) -> Any | None:
    root_value = database.scalar("SELECT workspace_root FROM books WHERE book_id=?", (book_id,))
    if root_value is None:
        return None
    root = Path(str(root_value)).expanduser().resolve()
    if not (root / "book.yaml").is_file():
        return None
    record = BookRegistry(BookLayout(root.parent)).record(book_id)
    return record if record.creation_mode is CreationMode.ORIGINAL else None


def is_original_book(database: Any, book_id: str) -> bool:
    return original_record(database, book_id) is not None


__all__ = ["is_original_book", "original_record"]
