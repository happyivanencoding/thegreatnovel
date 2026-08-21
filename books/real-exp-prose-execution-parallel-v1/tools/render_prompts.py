"""Render current production prompts into the isolated parallel experiment.

This helper imports the production ``story_mvp.prompts.generate_prompt`` function
without changing production code. It only writes experiment-local prompt files.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt


ROOT = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parents[0].parent


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def subchapter(text: str, number: int) -> str:
    match = re.search(
        rf"(?ms)^##\s+第\s*{number}\s*章[：:].*?\n(.*?)(?=^##\s+第\s*\d+\s*章[：:]|\Z)",
        text,
    )
    if match:
        title = re.search(rf"(?m)^##\s+第\s*{number}\s*章[：:].*$", text)
        return f"{title.group(0)}\n\n{match.group(1).strip()}" if title else match.group(1).strip()
    return ""


def long_block(text: str, number: int) -> str:
    body = section(text, "当前中期规划窗口") or section(text, "未来100章大型剧情块")
    blocks = re.split(r"(?m)(?=^##\s+)", body)
    for block in blocks:
        if re.search(rf"第\s*{number}\s*[—-]", block) or re.search(
            rf"第\s*{number}\s*章", block
        ):
            return block.strip()
    return body.strip()


def recent_summaries(book: str) -> str:
    status = section(book, "当前状态、未兑现承诺与作者备注")
    memory = re.search(r"(?ms)^##\s+RECENT SUMMARIES\s*\n(.*?)(?=^##\s+|\Z)", status)
    if memory:
        return memory.group(1).strip()
    legacy = re.search(r"(?ms)^最近章节摘要：?\s*\n(.*?)(?=^当前状态：|^未兑现承诺：|^作者备注：|\Z)", status)
    return legacy.group(1).strip() if legacy else ""


def previous_prose(candidate: Path, chapter: int) -> str:
    chunks: list[str] = []
    for index in range(1, chapter):
        path = candidate / f"chapter-{index:02d}" / "formal_prose.md"
        body = read(path).strip()
        if body:
            chunks.append(f"# {index}章正文\n\n{body}")
    return "\n\n".join(chunks)


def render_outline() -> tuple[str, Path]:
    candidate = EXP / "candidate-c"
    seed = read(candidate / "source" / "fantasy_seed.md")
    world = read(candidate / "source" / "world_vision_response.md")
    story = read(candidate / "source" / "story_program_response.md")
    creative_state = {
        "fantasy_seed": {"origin": "model_selected", "status": "author_approved"},
        "world_vision": {"origin": "model_selected", "status": "author_approved"},
        "proposal": {"origin": "model_selected", "status": "author_approved"},
    }
    prompt = generate_prompt(
        mode="outline",
        template=DEFAULT_PROMPT_TEMPLATES["outline"],
        book_content="",
        fantasy_seed=seed,
        world_vision=world,
        proposal_context=story,
        creative_state=creative_state,
        selected_references=[],
        gbrain_inspiration="",
    )
    output = candidate / "outline" / "outline_prompt.md"
    output.write_text(prompt, encoding="utf-8")
    return prompt, output


def render_execution(candidate_name: str, chapter: int, mode: str, current_outline: str = "") -> tuple[str, Path]:
    candidate = EXP / candidate_name
    book_path = candidate / "BOOK.md"
    book = read(book_path)
    plan = section(book, "未来十章逐章小纲")
    prompt = generate_prompt(
        mode=mode,
        template=DEFAULT_PROMPT_TEMPLATES.get(mode, ""),
        book_content=book,
        current_long_block=long_block(book, chapter),
        current_chapter_plan=subchapter(plan, chapter),
        previous_chapter_text=previous_prose(candidate, chapter),
        current_outline=current_outline,
        recent_summaries=recent_summaries(book),
        selected_references=[],
        gbrain_inspiration="",
        creative_direction="",
        chapter_number=chapter,
    )
    output = candidate / f"chapter-{chapter:02d}" / f"{mode}_prompt.md"
    output.write_text(prompt, encoding="utf-8")
    return prompt, output


def render_state_delta(candidate_name: str, chapter: int, prose_file: str, summary_file: str) -> tuple[str, Path]:
    candidate = EXP / candidate_name
    book = read(candidate / "BOOK.md")
    prose = read(Path(prose_file))
    summary = read(Path(summary_file))
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=book,
        current_outline="",
        recent_summaries=recent_summaries(book),
        selected_references=[],
        gbrain_inspiration="",
        chapter_number=chapter,
        chapter_prose=prose,
        chapter_fact_summary=summary,
    )
    output = candidate / f"chapter-{chapter:02d}" / "state_delta_prompt.md"
    output.write_text(prompt, encoding="utf-8")
    return prompt, output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", choices=("candidate-a", "candidate-c"))
    parser.add_argument("--chapter", type=int)
    parser.add_argument("--mode", choices=("director", "chapter_prep", "chapter"))
    parser.add_argument("--current-outline", default="")
    parser.add_argument("--current-outline-file")
    parser.add_argument("--state-delta", action="store_true")
    parser.add_argument("--prose-file")
    parser.add_argument("--summary-file")
    parser.add_argument("--outline", action="store_true")
    args = parser.parse_args()
    if args.outline:
        prompt, path = render_outline()
    elif args.state_delta:
        if not args.candidate or not args.chapter or not args.prose_file or not args.summary_file:
            parser.error("state delta rendering requires --candidate, --chapter, --prose-file and --summary-file")
        prompt, path = render_state_delta(args.candidate, args.chapter, args.prose_file, args.summary_file)
    else:
        if not args.candidate or not args.chapter or not args.mode:
            parser.error("execution rendering requires --candidate, --chapter and --mode")
        current_outline = args.current_outline
        if args.current_outline_file:
            current_outline = read(Path(args.current_outline_file))
        prompt, path = render_execution(args.candidate, args.chapter, args.mode, current_outline)
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    print(f"path={path}")
    print(f"chars={len(prompt)}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
