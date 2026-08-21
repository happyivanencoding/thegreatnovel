"""本 Pilot 的薄编排器：只渲染生产 Prompt、提取正式正文和承接 State Delta。

它不调用模型、不重试内容调用，也不修改 src/。每次真实子代理调用前，主线程先用本文件
生成完整 Prompt；子代理把同一调用的原始 response 写回对应 candidate 的实验目录。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
EXP = REPO / "books" / "real-exp-opening-three-chapter-hook-v1"
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import extract_final_chapter_artifact  # noqa: E402
from story_mvp.prompts import (  # noqa: E402
    DEFAULT_PROMPT_TEMPLATES,
    generate_prompt,
    parse_state_delta_v2,
)
from story_mvp.storage import (  # noqa: E402
    apply_state_delta_to_book,
    validate_chapter_body_for_save,
)


CANDIDATES = {
    "candidate-a": "《偷走明天的人》",
    "candidate-b": "《炉藏万象》",
    "candidate-c": "《掌中天工》",
}

CREATIVE_STATE = {
    "fantasy_seed": {"origin": "frozen_prior_experiment", "status": "author_approved"},
    "world_vision": {"origin": "frozen_prior_experiment", "status": "author_approved"},
    "proposal": {"origin": "frozen_prior_experiment", "status": "author_approved"},
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def candidate_dir(candidate: str) -> Path:
    if candidate not in CANDIDATES:
        raise ValueError(f"未知 candidate：{candidate}")
    return EXP / candidate


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def outline_text(candidate: str) -> str:
    root = candidate_dir(candidate)
    return read(root / "outline" / "outline_response.md") or read(
        root / "source" / "frozen_outline.md"
    )


def long_block(outline: str, chapter: int) -> str:
    body = section(outline, "当前中期规划窗口") or section(outline, "未来100章大型剧情块")
    blocks = re.split(r"(?m)(?=^##\s+)", body)
    for block in blocks:
        if re.search(rf"第\s*{chapter}\s*[—-]", block):
            return block.strip()
    return body.strip()


def chapter_plan(outline: str, chapter: int) -> str:
    body = section(outline, "未来十章逐章小纲")
    match = re.search(
        rf"(?ms)^##\s+第\s*{chapter}\s*章[：:].*?\n(.*?)(?=^##\s+第\s*\d+\s*章[：:]|^###\s+本批结束结算|\Z)",
        body,
    )
    if not match:
        return ""
    title = re.search(rf"(?m)^##\s+第\s*{chapter}\s*章[：:].*$", body)
    return f"{title.group(0)}\n\n{match.group(1).strip()}" if title else match.group(1).strip()


def previous_prose(candidate: str, chapter: int) -> str:
    root = candidate_dir(candidate)
    chunks: list[str] = []
    for number in range(1, chapter):
        body = read(root / "chapters" / f"chapter-{number:04d}.md").strip()
        if body:
            chunks.append(f"### 第{number}章已批准正文\n\n{body}")
    return "\n\n".join(chunks)


def recent_summaries(book: str) -> str:
    status = section(book, "当前状态、未兑现承诺与作者备注")
    match = re.search(r"(?ms)^##\s+RECENT SUMMARIES\s*\n(.*?)(?=^##\s+|\Z)", status)
    return match.group(1).strip() if match else ""


def frozen_source(candidate: str, name: str) -> str:
    return read(candidate_dir(candidate) / "source" / name)


def render_outline(candidate: str) -> Path:
    root = candidate_dir(candidate)
    prompt = generate_prompt(
        mode="outline",
        template=DEFAULT_PROMPT_TEMPLATES["outline"],
        book_content=read(root / "BOOK.md"),
        fantasy_seed=frozen_source(candidate, "fantasy_seed.md"),
        world_vision=frozen_source(candidate, "world_vision.md"),
        proposal_context=frozen_source(candidate, "story_program.md"),
        creative_state=CREATIVE_STATE,
        selected_references=[],
        gbrain_inspiration="",
    )
    target = root / "outline" / "outline_prompt.md"
    write(target, prompt)
    write(
        root / "outline" / "input_manifest.json",
        json.dumps(
            {
                "candidate": CANDIDATES[candidate],
                "fantasy_seed": "source/fantasy_seed.md",
                "world_vision": "source/world_vision.md",
                "story_program": "source/story_program.md",
                "generation": "single_call",
                "token_usage": "UNKNOWN",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    return target


def render_execution(candidate: str, chapter: int, mode: str) -> Path:
    if mode not in {"director", "chapter_prep", "chapter"}:
        raise ValueError(f"不支持的执行模式：{mode}")
    root = candidate_dir(candidate)
    book = read(root / "BOOK.md")
    outline = outline_text(candidate)
    prep = read(root / "runs" / f"chapter-{chapter:04d}" / "chapter_prep_response.md")
    prompt = generate_prompt(
        mode=mode,
        template="" if mode == "director" else DEFAULT_PROMPT_TEMPLATES[mode],
        book_content=book,
        current_long_block=long_block(outline, chapter),
        current_chapter_plan=chapter_plan(outline, chapter),
        current_outline=prep if mode == "chapter" else "",
        previous_chapter_text=previous_prose(candidate, chapter),
        recent_summaries=recent_summaries(book),
        creative_direction=f"严格执行当前 Pilot 的第{chapter}章；不要提前结算第{chapter + 1}章及以后。",
        selected_references=[],
        gbrain_inspiration="",
        chapter_number=chapter,
    )
    target = root / "runs" / f"chapter-{chapter:04d}" / f"{mode}_prompt.md"
    write(target, prompt)
    return target


def render_state_delta(candidate: str, chapter: int) -> Path:
    root = candidate_dir(candidate)
    prose = read(root / "chapters" / f"chapter-{chapter:04d}.md")
    summary = read(root / "runs" / f"chapter-{chapter:04d}" / "chapter_fact_summary.md")
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=read(root / "BOOK.md"),
        recent_summaries=recent_summaries(read(root / "BOOK.md")),
        selected_references=[],
        gbrain_inspiration="",
        chapter_number=chapter,
        chapter_prose=prose,
        chapter_fact_summary=summary,
    )
    target = root / "runs" / f"chapter-{chapter:04d}" / "state_delta_prompt.md"
    write(target, prompt)
    return target


def extract_writer(candidate: str, chapter: int) -> None:
    root = candidate_dir(candidate)
    run = root / "runs" / f"chapter-{chapter:04d}"
    response = read(run / "chapter_response.md")
    artifact = extract_final_chapter_artifact(response)
    if artifact is None:
        raise ValueError("Writer response 缺少 # 正式正文 / # 章节事实摘要")
    prose, summary = artifact
    validate_chapter_body_for_save(prose)
    write(root / "chapters" / f"chapter-{chapter:04d}.md", prose.strip() + "\n")
    write(run / "chapter_fact_summary.md", summary.strip() + "\n")
    write(run / "formal_prose.md", prose.strip() + "\n")


def apply_state(candidate: str, chapter: int) -> None:
    root = candidate_dir(candidate)
    run = root / "runs" / f"chapter-{chapter:04d}"
    response = read(run / "state_delta_response.md")
    if not response.strip():
        raise ValueError("State Delta response 为空")
    parse_state_delta_v2(response)
    updated = apply_state_delta_to_book(read(root / "BOOK.md"), chapter, response)
    write(run / "BOOK_after_state_delta.md", updated)
    write(root / "BOOK.md", updated)


def write_manifest(candidate: str, chapter: int, node: str, status: str) -> None:
    root = candidate_dir(candidate)
    path = root / "runs" / f"chapter-{chapter:04d}" / "manifest.json"
    current = json.loads(read(path) or "{}")
    current.update(
        {
            "candidate": CANDIDATES[candidate],
            "chapter": chapter,
            "writer_mode": "single",
            "token_usage": "UNKNOWN",
        }
    )
    nodes = current.setdefault("nodes", {})
    nodes[node] = {
        "status": status,
        "prompt_file": f"{node}_prompt.md" if node != "chapter" else "chapter_prompt.md",
        "response_file": f"{node}_response.md" if node != "chapter" else "chapter_response.md",
        "token_usage": "UNKNOWN",
        "generation": "single_call",
    }
    write(path, json.dumps(current, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("outline", "render", "render-state", "extract", "apply-state", "manifest"))
    parser.add_argument("candidate", choices=tuple(CANDIDATES))
    parser.add_argument("chapter", type=int, nargs="?")
    parser.add_argument("mode", nargs="?")
    parser.add_argument("status", nargs="?")
    args = parser.parse_args()
    if args.command == "outline":
        print(render_outline(args.candidate))
    elif args.command == "render":
        if not args.chapter or not args.mode:
            parser.error("render 需要 chapter 和 mode")
        print(render_execution(args.candidate, args.chapter, args.mode))
    elif args.command == "render-state":
        if not args.chapter:
            parser.error("render-state 需要 chapter")
        print(render_state_delta(args.candidate, args.chapter))
    elif args.command == "extract":
        if not args.chapter:
            parser.error("extract 需要 chapter")
        extract_writer(args.candidate, args.chapter)
    elif args.command == "apply-state":
        if not args.chapter:
            parser.error("apply-state 需要 chapter")
        apply_state(args.candidate, args.chapter)
    else:
        if not args.chapter or not args.mode or not args.status:
            parser.error("manifest 需要 chapter、node 和 status")
        write_manifest(args.candidate, args.chapter, args.mode, args.status)


if __name__ == "__main__":
    main()
