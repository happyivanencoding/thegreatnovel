"""One-off, lossless projection for the current production outline hard gate.

The production Prep prompt displays each field label on its own line, while the
production parser currently accepts only ``label：value`` on one line. This
script preserves the raw response and creates an auditable derived input by
joining each label with its immediately following non-empty value. It does not
generate, rewrite, or review story content.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from story_mvp.prompts import REQUIRED_OUTLINE_FIELDS, parse_outline_fields, validate_current_outline


def project(raw: str) -> str:
    labels = set(REQUIRED_OUTLINE_FIELDS)
    lines = raw.splitlines()
    output: list[str] = []
    pending: str | None = None
    for line in lines:
        stripped = line.strip()
        if stripped in labels or stripped in {f"{label}：" for label in labels}:
            pending = stripped.rstrip("：:").strip()
            continue
        if pending is not None and stripped:
            output.append(f"{pending}：{stripped}")
            pending = None
            continue
        if not stripped:
            continue
        output.append(line.rstrip())
    if pending is not None:
        output.append(f"{pending}：")
    projected = "\n".join(output).strip() + "\n"
    validate_current_outline(projected)
    return projected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    raw = args.source.read_text(encoding="utf-8")
    projected = project(raw)
    args.destination.write_text(projected, encoding="utf-8")
    print(f"path={args.destination}")
    print(f"raw_chars={len(raw)}")
    print(f"projected_chars={len(projected)}")
    print(f"fields={','.join(parse_outline_fields(projected))}")


if __name__ == "__main__":
    main()
