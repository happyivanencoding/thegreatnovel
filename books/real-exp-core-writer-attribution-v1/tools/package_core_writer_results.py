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


SNAPSHOTS = ("snapshot-01", "snapshot-02", "snapshot-03")
ARMS = ("single", "primary-fallback", "curator-primary")
EXPECTED_CHAPTER = {"snapshot-01": 1, "snapshot-02": 3, "snapshot-03": 2}
SEED = 20260821


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def extract_body(snapshot: str, arm: str) -> tuple[str, str, list[str]]:
    response_path = OUTPUT / snapshot / arm / "response.md"
    response = read(response_path)
    if arm == "single":
        artifact = extract_final_chapter_artifact(response)
        if artifact is None:
            raise ValueError(f"{response_path}: missing # 正式正文")
        body, fact = artifact
    else:
        body = extract_primary_draft(response)
        fact = extract_primary_fact_summary(response)
        if not body.strip():
            raise ValueError(f"{response_path}: missing # Primary Draft")
    headings = [line.strip() for line in body.splitlines() if re.match(r"^#{1,3}\s+", line.strip())]
    return body.strip(), fact.strip(), headings


def prompt_context_labels(prompt: str) -> list[str]:
    labels = [
        "AUTHORITY",
        "BOOK CONTRACT",
        "CHAPTER MISSION",
        "CANON PROSE",
        "CANON INDEX",
        "PLAN",
        "PROSE PROFILE",
        "OPTIONAL INSPIRATION",
        "Curated Chapter Context",
        "Opening Three Chapter Contract",
        "前文章末局部衔接片段",
    ]
    return [label for label in labels if label in prompt]


def main() -> None:
    result_manifest: dict[str, Any] = {
        "blind_seed": SEED,
        "content_call_count": 12,
        "snapshots": {},
        "tokens": "UNKNOWN",
    }
    blind_key: list[str] = [
        "# Blind key (do not provide to Reader)",
        "",
        "Options contain extracted formal body only; labels and prompts are withheld.",
    ]
    for index, snapshot in enumerate(SNAPSHOTS):
        snapshot_results: dict[str, Any] = {}
        curator_prompt = OUTPUT / snapshot / "curator" / "prompt.md"
        curator_response = OUTPUT / snapshot / "curator" / "response.md"
        snapshot_results["curator"] = {
            "prompt_chars": len(read(curator_prompt)),
            "response_chars": len(read(curator_response)),
            "actual_input_tokens": "UNKNOWN",
            "actual_output_tokens": "UNKNOWN",
            "call_count": 1,
            "prompt_context_labels": prompt_context_labels(read(curator_prompt)),
        }
        option_items: list[tuple[str, str]] = []
        for arm in ARMS:
            response_path = OUTPUT / snapshot / arm / "response.md"
            prompt_path = OUTPUT / snapshot / arm / "prompt.md"
            body, fact, headings = extract_body(snapshot, arm)
            write(OUTPUT / snapshot / arm / "body.md", body)
            write(OUTPUT / snapshot / arm / "fact-summary.md", fact or "(empty)")
            option_items.append((arm, body))
            snapshot_results[arm] = {
                "prompt_chars": len(read(prompt_path)),
                "response_chars": len(read(response_path)),
                "body_chars": len(body),
                "fact_summary_chars": len(fact),
                "actual_input_tokens": "UNKNOWN",
                "actual_output_tokens": "UNKNOWN",
                "call_count": 1,
                "body_headings": headings,
                "prompt_context_labels": prompt_context_labels(read(prompt_path)),
                "format_notes": [],
            }
            if snapshot == "snapshot-01" and arm == "primary-fallback" and any("第四章" in heading for heading in headings):
                snapshot_results[arm]["format_notes"].append("BODY_TITLE_CHAPTER_MISMATCH_EXPECTED_CHAPTER_1")
            if not headings:
                snapshot_results[arm]["format_notes"].append("BODY_HAS_NO_MARKDOWN_CHAPTER_HEADING")

        random.Random(SEED + index).shuffle(option_items)
        blind_dir = OUTPUT / "blind" / snapshot
        for option_index, (arm, body) in enumerate(option_items):
            label = chr(ord("A") + option_index)
            write(blind_dir / f"option-{label.lower()}.md", body)
            blind_key.append(f"- {snapshot} option-{label}: {arm}")
        snapshot_results["blind_order"] = [arm for arm, _ in option_items]
        result_manifest["snapshots"][snapshot] = snapshot_results

    write(OUTPUT / "blind" / "blind-key.md", "\n".join(blind_key))
    write(OUTPUT / "results.json", json.dumps(result_manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
