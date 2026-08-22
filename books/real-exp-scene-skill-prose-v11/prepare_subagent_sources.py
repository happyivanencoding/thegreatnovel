"""Copy only the frozen source prompts needed by the subagent experiment."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "books" / "real-exp-scene-skill-prose-v11"
STATIC = ROOT / "books" / "real-exp-scene-skill-runtime-v1"


def copy_if_missing(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_file():
        shutil.copyfile(source, target)


def main() -> None:
    copy_if_missing(
        STATIC / "chapter-0002" / "curator_prompt_with_catalog.md",
        OUT / "chapter-0002" / "curator_prompt.md",
    )
    copy_if_missing(
        STATIC / "chapter-0003" / "curator_prompt_with_catalog.md",
        OUT / "chapter-0003" / "curator_prompt.md",
    )
    copy_if_missing(
        ROOT / "books" / "real-exp-opening-reader-first-fresh-v1" / "runs" / "chapter-0002" / "director_response.md",
        OUT / "chapter-0002" / "director_frozen.md",
    )
    copy_if_missing(
        ROOT / "books" / "real-exp-human-reaction-ch3-v1" / "after-v2" / "director_response.md",
        OUT / "chapter-0003" / "director_frozen.md",
    )
    print("sources-prepared")


if __name__ == "__main__":
    main()
