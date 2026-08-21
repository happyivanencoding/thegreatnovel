from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "d4e2dd6f3377f967d8930480016f15a450b74e1b"
V2_ROOT = "books/real-exp-opening-pipeline-comparison-v2"
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt  # noqa: E402


CREATIVE_STATE = {
    "fantasy_seed": {"origin": "frozen_prior_experiment", "status": "author_approved"},
    "world_vision": {"origin": "frozen_prior_experiment", "status": "author_approved"},
    "proposal": {"origin": "frozen_prior_experiment", "status": "author_approved"},
}


def git_text(path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)", text)
    return match.group(1).strip() if match else ""


def chapter_plan(outline: str, chapter: int) -> str:
    body = section(outline, "未来十章逐章小纲")
    if not body:
        batch = re.search(r"(?ms)^未来十章开头批次说明：\s*\n(.*?)(?=^#\s+|\Z)", outline)
        body = batch.group(1).strip() if batch else ""
    match = re.search(
        rf"(?ms)^##\s+第\s*{chapter}\s*章[：:].*?\n(.*?)(?=^##\s+第\s*\d+\s*章[：:]|^###\s+本批结束结算|\Z)",
        body,
    )
    if not match:
        return ""
    title = re.search(rf"(?m)^##\s+第\s*{chapter}\s*章[：:].*$", body)
    return f"{title.group(0)}\n\n{match.group(1).strip()}" if title else match.group(1).strip()


def long_block(outline: str, chapter: int) -> str:
    body = section(outline, "当前中期规划窗口") or section(outline, "未来100章大型剧情块")
    blocks = re.split(r"(?m)(?=^##\s+)", body)
    for block in blocks:
        if re.search(rf"第\s*{chapter}\s*[—-]", block):
            return block.strip()
    return body.strip()


def build_inputs() -> dict[str, Any]:
    candidate = "candidate-b"
    chapter = 2
    base = f"{V2_ROOT}/{candidate}"
    outline = git_text(f"{base}/outline/outline_response.md")
    book_path = f"{base}/runs/chapter-0001/BOOK_after_state_delta.md"
    book = git_text(book_path)
    prep_path = f"{base}/runs/chapter-0002/chapter_prep_response.md"
    current_outline = git_text(prep_path)
    previous = git_text(f"{base}/chapters/chapter-0001.md")
    return {
        "candidate": candidate,
        "book": "《炉藏万象》",
        "chapter": chapter,
        "source_commit": SOURCE_COMMIT,
        "source_paths": {
            "book": book_path,
            "outline": f"{base}/outline/outline_response.md",
            "current_outline": prep_path,
            "previous_prose": f"{base}/chapters/chapter-0001.md",
            "fantasy_seed": f"{base}/source/fantasy_seed.md",
            "world_vision": f"{base}/source/world_vision.md",
            "story_program": f"{base}/source/story_program.md",
        },
        "book_content": book,
        "outline": outline,
        "current_long_block": long_block(outline, chapter),
        "current_chapter_plan": chapter_plan(outline, chapter),
        "current_outline": current_outline,
        "previous_chapter_text": f"### 第1章已批准正文\n\n{previous.strip()}",
        "recent_summaries": section(book, "当前状态、未兑现承诺与作者备注"),
        "fantasy_seed": git_text(f"{base}/source/fantasy_seed.md"),
        "world_vision": git_text(f"{base}/source/world_vision.md"),
        "proposal_context": git_text(f"{base}/source/story_program.md"),
        "gbrain_inspiration": "",
    }


def common(inputs: dict[str, Any], writer_mode: str) -> dict[str, Any]:
    return {
        "book_content": inputs["book_content"],
        "creative_direction": "严格执行当前实验的第2章；不要提前结算第3章及以后。",
        "fantasy_seed": inputs["fantasy_seed"],
        "world_vision": inputs["world_vision"],
        "creative_state": CREATIVE_STATE,
        "proposal_context": inputs["proposal_context"],
        "current_long_block": inputs["current_long_block"],
        "previous_chapter_text": inputs["previous_chapter_text"],
        "current_outline": inputs["current_outline"],
        "current_chapter_plan": inputs["current_chapter_plan"],
        "recent_summaries": inputs["recent_summaries"],
        "selected_references": [],
        "gbrain_inspiration": inputs["gbrain_inspiration"],
        "chapter_number": 2,
        "writer_mode": writer_mode,
        "chapter_prose": "",
        "chapter_fact_summary": "",
        "enabled_specialists": {},
    }


def render(inputs: dict[str, Any], mode: str, writer_mode: str, **overrides: str) -> str:
    kwargs = common(inputs, writer_mode)
    kwargs.update(mode=mode, template=DEFAULT_PROMPT_TEMPLATES[mode], **overrides)
    return generate_prompt(**kwargs)


def prepare() -> None:
    inputs = build_inputs()
    root = OUTPUT / "replacement-snapshot"
    frozen = root / "frozen-input"
    for name, value in {
        "BOOK.md": inputs["book_content"],
        "outline.md": inputs["outline"],
        "current-long-block.md": inputs["current_long_block"],
        "current-chapter-plan.md": inputs["current_chapter_plan"],
        "current-outline.md": inputs["current_outline"],
        "previous-prose.md": inputs["previous_chapter_text"],
        "recent-summaries.md": inputs["recent_summaries"],
        "fantasy-seed.md": inputs["fantasy_seed"],
        "world-vision.md": inputs["world_vision"],
        "story-program.md": inputs["proposal_context"],
        "optional-inspiration.md": "EMPTY_BY_FROZEN_V2_RUNTIME",
    }.items():
        write(frozen / name, value)
    write(frozen / "input-manifest.json", json.dumps({key: value for key, value in inputs.items() if key not in {"book_content", "outline", "current_long_block", "current_chapter_plan", "current_outline", "previous_chapter_text", "recent_summaries", "fantasy_seed", "world_vision", "proposal_context"}}, ensure_ascii=False, indent=2))
    write(root / "single" / "prompt.md", render(inputs, "chapter", "single"))
    write(root / "primary-fallback" / "prompt.md", render(inputs, "primary_writer", "hybrid_selective", curator_response="", curated_context=""))
    write(root / "curator" / "prompt.md", render(inputs, "context_curator", "hybrid_selective"))
    write(OUTPUT / "SOURCE_MANIFEST.json", json.dumps({"experiment_generation_base": SOURCE_COMMIT, "snapshot": "《炉藏万象》 Chapter 2 replacement", "source_paths": inputs["source_paths"], "arms": ["single", "primary-fallback", "curator", "curator-primary"]}, ensure_ascii=False, indent=2))
    write(OUTPUT / "call-plan.json", json.dumps({"replacement_content_calls": 4, "reader_calls": 3, "specialist_calls": 0, "integrator_calls": 0, "state_delta_calls": 0}, ensure_ascii=False, indent=2))


def render_curated() -> None:
    inputs = build_inputs()
    response = (OUTPUT / "replacement-snapshot" / "curator" / "response.md").read_text(encoding="utf-8")
    write(OUTPUT / "replacement-snapshot" / "curator-primary" / "prompt.md", render(inputs, "primary_writer", "hybrid_selective", curator_response=response, curated_context=response))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "render-curated"))
    command = parser.parse_args().command
    if command == "prepare":
        prepare()
    else:
        render_curated()


if __name__ == "__main__":
    main()
