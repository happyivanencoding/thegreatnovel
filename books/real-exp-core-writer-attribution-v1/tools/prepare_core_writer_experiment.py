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


SNAPSHOTS: dict[str, dict[str, Any]] = {
    "snapshot-01": {
        "candidate": "candidate-b",
        "book": "《炉藏万象》",
        "chapter": 1,
        "purpose": "Opening、第一异能高光、世界到主角收缩",
        "book_path": f"{V2_ROOT}/candidate-b/BOOK.md",
    },
    "snapshot-02": {
        "candidate": "candidate-b",
        "book": "《炉藏万象》",
        "chapter": 3,
        "purpose": "资产复利、人物协作、空间和下一阶段入口",
        "book_path": f"{V2_ROOT}/candidate-b/runs/chapter-0002/BOOK_after_state_delta.md",
    },
    "snapshot-03": {
        "candidate": "candidate-c",
        "book": "《掌中天工》",
        "chapter": 2,
        "purpose": "动作、机械空间、对白、能力第二次应用",
        "book_path": f"{V2_ROOT}/candidate-c/runs/chapter-0001/BOOK_after_state_delta.md",
    },
}

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
    match = re.search(
        rf"(?ms)^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def long_block(outline: str, chapter: int) -> str:
    body = section(outline, "当前中期规划窗口") or section(outline, "未来100章大型剧情块")
    blocks = re.split(r"(?m)(?=^##\s+)", body)
    for block in blocks:
        if re.search(rf"第\s*{chapter}\s*[—-]", block):
            return block.strip()
    return body.strip()


def chapter_plan(outline: str, chapter: int) -> str:
    body = section(outline, "未来十章逐章小纲")
    if not body:
        batch = re.search(
            r"(?ms)^未来十章开头批次说明：\s*\n(.*?)(?=^#\s+|\Z)",
            outline,
        )
        body = batch.group(1).strip() if batch else ""
    match = re.search(
        rf"(?ms)^##\s+第\s*{chapter}\s*章[：:].*?\n(.*?)(?=^##\s+第\s*\d+\s*章[：:]|^###\s+本批结束结算|\Z)",
        body,
    )
    if not match:
        return ""
    title = re.search(rf"(?m)^##\s+第\s*{chapter}\s*章[：:].*$", body)
    return f"{title.group(0)}\n\n{match.group(1).strip()}" if title else match.group(1).strip()


def previous_prose(candidate: str, chapter: int) -> str:
    chunks: list[str] = []
    for number in range(1, chapter):
        path = f"{V2_ROOT}/{candidate}/chapters/chapter-{number:04d}.md"
        body = git_text(path).strip()
        if body:
            chunks.append(f"### 第{number}章已批准正文\n\n{body}")
    return "\n\n".join(chunks)


def recent_summaries(book: str) -> str:
    status = section(book, "当前状态、未兑现承诺与作者备注")
    match = re.search(r"(?ms)^## RECENT SUMMARIES\s*\n(.*?)(?=^##\s+|\Z)", status)
    return match.group(1).strip() if match else ""


def snapshot_inputs(snapshot: dict[str, Any]) -> dict[str, Any]:
    candidate = snapshot["candidate"]
    chapter = snapshot["chapter"]
    chapter_name = f"chapter-{chapter:04d}"
    outline_path = f"{V2_ROOT}/{candidate}/outline/outline_response.md"
    prep_path = f"{V2_ROOT}/{candidate}/runs/{chapter_name}/chapter_prep_response.md"
    book = git_text(snapshot["book_path"])
    outline = git_text(outline_path)
    current_outline = git_text(prep_path)
    fantasy_seed = git_text(f"{V2_ROOT}/{candidate}/source/fantasy_seed.md")
    world_vision = git_text(f"{V2_ROOT}/{candidate}/source/world_vision.md")
    story_program = git_text(f"{V2_ROOT}/{candidate}/source/story_program.md")
    return {
        "candidate": candidate,
        "book": snapshot["book"],
        "chapter": chapter,
        "purpose": snapshot["purpose"],
        "source_commit": SOURCE_COMMIT,
        "source_paths": {
            "book": snapshot["book_path"],
            "outline": outline_path,
            "current_outline": prep_path,
            "previous_prose": [
                f"{V2_ROOT}/{candidate}/chapters/chapter-{number:04d}.md"
                for number in range(1, chapter)
            ],
            "fantasy_seed": f"{V2_ROOT}/{candidate}/source/fantasy_seed.md",
            "world_vision": f"{V2_ROOT}/{candidate}/source/world_vision.md",
            "story_program": f"{V2_ROOT}/{candidate}/source/story_program.md",
        },
        "book_content": book,
        "outline": outline,
        "current_long_block": long_block(outline, chapter),
        "current_chapter_plan": chapter_plan(outline, chapter),
        "current_outline": current_outline,
        "previous_chapter_text": previous_prose(candidate, chapter),
        "recent_summaries": recent_summaries(book),
        "fantasy_seed": fantasy_seed,
        "world_vision": world_vision,
        "proposal_context": story_program,
        "gbrain_inspiration": "",
        "optional_inspiration_source": "EMPTY_BY_FROZEN_V2_RUNTIME",
    }


def prompt_common(inputs: dict[str, Any], writer_mode: str) -> dict[str, Any]:
    return {
        "template": "",
        "book_content": inputs["book_content"],
        "creative_direction": f"严格执行当前实验的第{inputs['chapter']}章；不要提前结算第{inputs['chapter'] + 1}章及以后。",
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
        "chapter_number": inputs["chapter"],
        "writer_mode": writer_mode,
        "chapter_prose": "",
        "chapter_fact_summary": "",
        "enabled_specialists": {},
    }


def render(inputs: dict[str, Any], mode: str, writer_mode: str, **overrides: str) -> str:
    kwargs = prompt_common(inputs, writer_mode)
    kwargs["mode"] = mode
    kwargs["template"] = DEFAULT_PROMPT_TEMPLATES[mode]
    kwargs.update(overrides)
    return generate_prompt(**kwargs)


def write_frozen_inputs(root: Path, inputs: dict[str, Any]) -> None:
    frozen = root / "frozen-input"
    write(frozen / "BOOK.md", inputs["book_content"])
    write(frozen / "outline.md", inputs["outline"])
    write(frozen / "current-long-block.md", inputs["current_long_block"])
    write(frozen / "current-chapter-plan.md", inputs["current_chapter_plan"])
    write(frozen / "current-outline.md", inputs["current_outline"])
    write(frozen / "previous-prose.md", inputs["previous_chapter_text"] or "(本 snapshot 没有前文正文)")
    write(frozen / "recent-summaries.md", inputs["recent_summaries"] or "(本 snapshot 没有 recent summaries)")
    write(frozen / "fantasy-seed.md", inputs["fantasy_seed"])
    write(frozen / "world-vision.md", inputs["world_vision"])
    write(frozen / "story-program.md", inputs["proposal_context"])
    write(frozen / "optional-inspiration.md", inputs["gbrain_inspiration"] or inputs["optional_inspiration_source"])
    write(frozen / "input-manifest.json", json.dumps({key: value for key, value in inputs.items() if key not in {"book_content", "outline", "current_long_block", "current_chapter_plan", "current_outline", "previous_chapter_text", "recent_summaries", "fantasy_seed", "world_vision", "proposal_context"}}, ensure_ascii=False, indent=2))


def prepare() -> None:
    manifest: dict[str, Any] = {
        "experiment_generation_base": SOURCE_COMMIT,
        "code_audit_base": "c405b7d1b6d7ad89fc7a41ce1a4da4126aa4dc42",
        "arms": {
            "single": {"content_calls": 1, "mode": "chapter"},
            "primary-fallback": {"content_calls": 1, "mode": "primary_writer", "curator_response": ""},
            "curator": {"content_calls": 1, "mode": "context_curator"},
            "curator-primary": {"content_calls": 1, "mode": "primary_writer", "curator_response": "raw curator response"},
        },
        "snapshots": {},
    }
    for snapshot_name, snapshot in SNAPSHOTS.items():
        root = OUTPUT / snapshot_name
        inputs = snapshot_inputs(snapshot)
        write_frozen_inputs(root, inputs)
        write(root / "single" / "prompt.md", render(inputs, "chapter", "single"))
        write(root / "primary-fallback" / "prompt.md", render(inputs, "primary_writer", "hybrid_selective", curator_response="", curated_context=""))
        write(root / "curator" / "prompt.md", render(inputs, "context_curator", "hybrid_selective"))
        manifest["snapshots"][snapshot_name] = {
            "book": inputs["book"],
            "candidate": inputs["candidate"],
            "chapter": inputs["chapter"],
            "purpose": inputs["purpose"],
            "source_paths": inputs["source_paths"],
            "prompt_files": {
                "single": f"{snapshot_name}/single/prompt.md",
                "primary-fallback": f"{snapshot_name}/primary-fallback/prompt.md",
                "curator": f"{snapshot_name}/curator/prompt.md",
                "curator-primary": f"{snapshot_name}/curator-primary/prompt.md (after curator response)",
            },
        }
    write(OUTPUT / "SOURCE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    write(OUTPUT / "call-plan.json", json.dumps({"snapshots": list(SNAPSHOTS), "maximum_content_calls": 12, "planned_calls": 12}, ensure_ascii=False, indent=2))


def render_curated() -> None:
    for snapshot_name, snapshot in SNAPSHOTS.items():
        root = OUTPUT / snapshot_name
        inputs = snapshot_inputs(snapshot)
        curator_response_path = root / "curator" / "response.md"
        if not curator_response_path.is_file():
            raise FileNotFoundError(curator_response_path)
        curator_response = curator_response_path.read_text(encoding="utf-8")
        write(
            root / "curator-primary" / "prompt.md",
            render(
                inputs,
                "primary_writer",
                "hybrid_selective",
                curator_response=curator_response,
                curated_context=curator_response,
            ),
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "render-curated"))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    else:
        render_curated()


if __name__ == "__main__":
    main()
