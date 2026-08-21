from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import extract_final_chapter_artifact, extract_primary_draft, extract_primary_fact_summary  # noqa: E402


SEED = 20260821
ARMS = ("single", "primary-fallback", "curator-primary")
NEW_ROOT = ROOT / "books" / "real-exp-core-writer-attribution-v2" / "replacement-snapshot"
OLD_ROOT = ROOT / "books" / "real-exp-core-writer-attribution-v1"
OLD_V2_RESULTS = json.loads((OLD_ROOT / "results.json").read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def extract_raw_body(snapshot_root: Path, arm: str) -> tuple[str, str]:
    response = read(snapshot_root / arm / "response.md")
    if arm == "single":
        artifact = extract_final_chapter_artifact(response)
        if artifact is None:
            raise ValueError(f"missing formal body: {snapshot_root / arm / 'response.md'}")
        return artifact
    body = extract_primary_draft(response)
    fact = extract_primary_fact_summary(response)
    if not body.strip():
        raise ValueError(f"missing Primary Draft: {snapshot_root / arm / 'response.md'}")
    return body, fact


def strip_outer_chapter_title(body: str) -> tuple[str, str | None]:
    lines = body.strip().splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if re.match(r"^#{1,2}\s*第\s*[0-9一二三四五六七八九十百]+\s*章(?:\s|：|:)", line.strip()):
            removed = line.strip()
            del lines[index]
            while lines and not lines[0].strip():
                del lines[0]
            return "\n".join(lines).strip(), removed
        break
    return body.strip(), None


def package_snapshot(snapshot_name: str, source_root: Path, blind_name: str, chapter: int, prompt_source: str | None = None) -> dict[str, Any]:
    records: dict[str, Any] = {}
    options: list[tuple[str, str]] = []
    for arm in ARMS:
        body, fact = extract_raw_body(source_root, arm)
        blind_body, removed_title = strip_outer_chapter_title(body)
        write(OUTPUT / "source-bodies" / blind_name / f"raw-{arm}.md", body)
        write(OUTPUT / "source-bodies" / blind_name / f"option-source-{arm}.md", blind_body)
        records[arm] = {
            "prompt_chars": len(read(source_root / arm / "prompt.md")),
            "response_chars": len(read(source_root / arm / "response.md")),
            "actual_input_tokens": "UNKNOWN",
            "actual_output_tokens": "UNKNOWN",
            "call_count": 1,
            "body_chars": len(body),
            "blind_body_chars": len(blind_body),
            "fact_summary_chars": len(fact),
            "outer_title_removed": removed_title,
            "presentation_format_only": True,
            "content_scope": "CLEAN",
        }
        options.append((arm, blind_body))
    random.Random(SEED + chapter).shuffle(options)
    key_lines = [f"- {blind_name} option mapping:"]
    for index, (arm, body) in enumerate(options):
        label = chr(ord("A") + index)
        write(OUTPUT / "blind" / blind_name / f"option-{label.lower()}.md", body)
        key_lines.append(f"  - option-{label}: {arm}")
    write(OUTPUT / "blind" / blind_name / "_key-fragment.md", "\n".join(key_lines))
    return {"chapter": chapter, "source": str(source_root), "blind": blind_name, "arms": records, "blind_order": [arm for arm, _ in options], "prompt_source": prompt_source}


def main() -> None:
    replacement = package_snapshot(
        "replacement-snapshot",
        NEW_ROOT,
        "snapshot-b2",
        chapter=2,
        prompt_source="books/real-exp-core-writer-attribution-v2/replacement-snapshot",
    )
    b3 = package_snapshot(
        "old-snapshot-02",
        OLD_ROOT / "snapshot-02",
        "snapshot-b3",
        chapter=3,
        prompt_source="books/real-exp-core-writer-attribution-v1/snapshot-02",
    )
    c2 = package_snapshot(
        "old-snapshot-03",
        OLD_ROOT / "snapshot-03",
        "snapshot-c2",
        chapter=2,
        prompt_source="books/real-exp-core-writer-attribution-v1/snapshot-03",
    )
    key = [
        "# Blind key (do not provide to Reader)",
        "",
        *read(OUTPUT / "blind" / "snapshot-b2" / "_key-fragment.md").splitlines(),
        *read(OUTPUT / "blind" / "snapshot-b3" / "_key-fragment.md").splitlines(),
        *read(OUTPUT / "blind" / "snapshot-c2" / "_key-fragment.md").splitlines(),
    ]
    write(OUTPUT / "blind" / "blind-key.md", "\n".join(key))
    for path in OUTPUT.glob("blind/snapshot-*/_key-fragment.md"):
        path.unlink()

    write(OUTPUT / "validity-data.json", json.dumps({
        "old_snapshot_01": {
            "status": "INVALID_CONTEXT_CONTAMINATION",
            "target": "Chapter 1",
            "reason": "frozen-input/BOOK.md already contained Chapter 1-3 summaries, Rift Cutter, fire-scale embryo, rescued furnace workers, and post-Chapter-3 branch state",
        },
        "old_snapshot_02": {"status": "CLEAN", "target": "《炉藏万象》 Chapter 3", "source": "old-snapshot-02"},
        "old_snapshot_03": {"status": "CLEAN", "target": "《掌中天工》 Chapter 2", "source": "old-snapshot-03"},
        "replacement_snapshot_b2": {"status": "CLEAN", "target": "《炉藏万象》 Chapter 2", "source": "replacement-snapshot"},
    }, ensure_ascii=False, indent=2))
    write(OUTPUT / "results.json", json.dumps({"replacement": replacement, "snapshot_b3": b3, "snapshot_c2": c2, "reader_calls": 3, "new_content_calls": 4}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
