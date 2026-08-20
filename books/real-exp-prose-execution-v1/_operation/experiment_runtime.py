"""本实验的薄编排器：只调用当前 Story MVP 的正式渲染、Ledger、保存和 State Delta 函数。

它不实现第二套 runtime；_operation 目录只保存真实子代理的隔离响应和本实验的
编排输入。正式节点产物仍写入当前项目约定的 runs/、chapters/ 和 BOOK.md。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
BOOK_ID = "real-exp-prose-execution-v1"
BOOK_DIR = REPO / "books" / BOOK_ID
SRC_DIR = REPO / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_final_chapter_artifact,
    extract_primary_draft,
    extract_primary_fact_summary,
)
from story_mvp.prompts import generate_prompt, parse_outline_fields  # noqa: E402
from story_mvp.run_ledger import (  # noqa: E402
    adopt_final_source,
    create_or_load_run,
    load_run,
    save_node_prompt,
    save_node_response,
    set_selected_specialists,
    should_run_integrator,
    skip_integrator_if_no_patches,
)
from story_mvp.storage import (  # noqa: E402
    apply_state_delta_to_book,
    book_directory,
    read_book_payload,
    save_chapter,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _section(text: str, heading_pattern: str, next_pattern: str) -> str:
    match = re.search(heading_pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"找不到冻结输入区块：{heading_pattern}")
    start = match.start()
    tail = text[match.end() :]
    next_match = re.search(next_pattern, tail, flags=re.MULTILINE)
    end = match.end() + (next_match.start() if next_match else len(tail))
    return text[start:end].strip()


def frozen_inputs(chapter: int) -> tuple[str, str]:
    book = _read(BOOK_DIR / "BOOK.md")
    long_block = _section(
        book,
        r"^## 第\d+—\d+章：",
        r"^## 第\d+—\d+章：|^# 未来十章逐章小纲",
    )
    chapter_plan = _section(
        book,
        rf"^## 第{chapter}章：",
        r"^## 第\d+章：|^### 本批结束结算|^# 当前状态、未兑现承诺与作者备注",
    )
    return long_block, chapter_plan


def previous_prose(chapter: int) -> str:
    chunks: list[str] = []
    for number in range(max(1, chapter - 2), chapter):
        path = BOOK_DIR / "chapters" / f"chapter-{number:04d}.md"
        if path.is_file():
            chunks.append(f"### 第{number}章已批准正文\n\n{_read(path)}")
    return "\n\n".join(chunks)


def recent_summary_input() -> str:
    # 当前状态区已包含 Canon Memory；页面摘要留空，避免同一摘要被重复注入。
    return ""


def current_outline(chapter: int, mode: str) -> str:
    operation = BOOK_DIR / "_operation" / f"chapter-{chapter:04d}"
    if mode == "director":
        return ""
    candidates = (
        operation / "chapter_prep_response.md",
        operation / "director_response.md",
    )
    for path in candidates:
        if path.is_file() and _read(path).strip():
            return _read(path)
    return ""


def current_intent(chapter: int) -> str:
    return f"严格执行 Frozen Future 10 第{chapter}章，不提前兑现第{chapter + 1}章及以后内容。"


def _response_value(operation: Path, name: str) -> str:
    return _read(operation / f"{name}_response.md")


def render(chapter: int, mode: str) -> Path:
    payload = read_book_payload(BOOK_ID, REPO / "books")
    long_block, chapter_plan = frozen_inputs(chapter)
    operation = BOOK_DIR / "_operation" / f"chapter-{chapter:04d}"
    operation.mkdir(parents=True, exist_ok=True)
    previous = previous_prose(chapter)
    curator = _response_value(operation, "curator")
    primary = _response_value(operation, "primary")
    outline = current_outline(chapter, mode)
    selected = load_run(BOOK_DIR, chapter).get("selected_specialists", []) if (BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / "manifest.json").is_file() else []
    specialist_responses = {
        name: _response_value(operation, name)
        for name in ("opening", "dialogue", "action", "emotion")
    }
    enabled = {name: name in selected for name in specialist_responses}
    template = payload["prompt_templates"].get(mode, "")
    prompt = generate_prompt(
        mode=mode,
        template=template,
        book_content=payload["book_content"],
        current_long_block=long_block,
        current_chapter_plan=chapter_plan,
        current_outline=outline,
        previous_chapter_text=previous,
        recent_summaries=recent_summary_input(),
        creative_direction=current_intent(chapter),
        creative_state=payload["creative_state"],
        fantasy_seed=payload["fantasy_seed"],
        world_vision=payload["world_vision"],
        proposal_context=payload["proposal"],
        gbrain_inspiration="",
        selected_references=[],
        chapter_number=chapter,
        writer_mode="hybrid_selective",
        curator_response=curator,
        curated_context=curator,
        primary_writer_response=primary,
        primary_draft=extract_primary_draft(primary) if primary else "",
        primary_fact_summary=extract_primary_fact_summary(primary) if primary else "",
        specialist_opening_response=specialist_responses["opening"],
        specialist_dialogue_response=specialist_responses["dialogue"],
        specialist_action_response=specialist_responses["action"],
        specialist_emotion_response=specialist_responses["emotion"],
        enabled_specialists=enabled,
        chapter_prose=_read(BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / "final_formal_prose.md"),
        chapter_fact_summary=_read(operation / "chapter_fact_summary.md"),
    )
    if mode == "chapter_prep":
        target = BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / "chapter_prep_prompt.md"
        target.parent.mkdir(parents=True, exist_ok=True)
    else:
        node = {
            "director": "director",
            "context_curator": "curator",
            "primary_writer": "primary",
            "specialist_opening": "opening",
            "specialist_dialogue": "dialogue",
            "specialist_action": "action",
            "specialist_emotion": "emotion",
            "chapter_integrator": "integrator",
            "state_delta": "state_delta",
        }.get(mode)
        if not node:
            raise ValueError(f"无法为 Prompt mode 定位正式节点：{mode}")
        save_node_prompt(BOOK_DIR, chapter, node, prompt)
        target = BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / f"{node}_prompt.md"
    target.write_text(prompt, encoding="utf-8")
    operation.joinpath(f"{mode}_prompt.md").write_text(prompt, encoding="utf-8")
    print(target)
    print(f"PROMPT_CHARS={len(prompt)}")
    return target


def init_run(chapter: int) -> None:
    create_or_load_run(
        BOOK_DIR,
        chapter,
        writer_mode="hybrid_selective",
        selected_specialists=[],
    )


def record_response(chapter: int, node: str) -> None:
    operation = BOOK_DIR / "_operation" / f"chapter-{chapter:04d}"
    source = operation / f"{node}_response.md"
    response = _read(source)
    if not response.strip():
        raise ValueError(f"隔离响应为空：{source}")
    if node == "chapter_prep":
        target = BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / "chapter_prep_response.md"
        target.write_text(response, encoding="utf-8")
    else:
        save_node_response(BOOK_DIR, chapter, node, response)
    print(f"RECORDED={node};CHARS={len(response)}")


def select_specialists(chapter: int) -> None:
    response = _read(BOOK_DIR / "_operation" / f"chapter-{chapter:04d}" / "director_response.md")
    names = ("opening", "dialogue", "action", "emotion")
    selected = [
        name
        for name in names
        if re.search(rf"^{name.capitalize()}：\s*启用\b", response, flags=re.MULTILINE)
    ][:2]
    set_selected_specialists(BOOK_DIR, chapter, selected)
    (BOOK_DIR / "_operation" / f"chapter-{chapter:04d}" / "selected_specialists.md").write_text(
        "\n".join(selected) + ("\n" if selected else "（无）\n"), encoding="utf-8"
    )
    print("SELECTED=" + ",".join(selected))


def finish_writer(chapter: int) -> None:
    operation = BOOK_DIR / "_operation" / f"chapter-{chapter:04d}"
    specialist_responses = {
        name: _response_value(operation, name)
        for name in ("opening", "dialogue", "action", "emotion")
    }
    if should_run_integrator(specialist_responses):
        return
    skip_integrator_if_no_patches(BOOK_DIR, chapter, specialist_responses)
    adopt_final_source(BOOK_DIR, chapter, "primary")
    print("FINAL_SOURCE=primary")


def adopt_integrator(chapter: int) -> None:
    adopt_final_source(BOOK_DIR, chapter, "integrator")
    print("FINAL_SOURCE=integrator")


def finalize_chapter(chapter: int) -> None:
    manifest = load_run(BOOK_DIR, chapter)
    source = manifest.get("final_source")
    if source not in {"primary", "integrator"}:
        raise ValueError("正式正文来源尚未采用")
    response = _read(BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / f"{source}_response.md")
    if source == "integrator":
        artifact = extract_final_chapter_artifact(response)
        if artifact is None:
            raise ValueError("Integrator Response 缺少 # 正式正文 / # 章节事实摘要")
        prose, fact_summary = artifact
    else:
        prose = extract_primary_draft(response)
        fact_summary = extract_primary_fact_summary(response)
    if not prose.strip():
        raise ValueError("正式正文为空")
    run_dir = BOOK_DIR / "runs" / f"chapter-{chapter:04d}"
    run_dir.joinpath("final_formal_prose.md").write_text(prose.strip() + "\n", encoding="utf-8")
    run_dir.joinpath("chapter_fact_summary.md").write_text(fact_summary.strip() + "\n", encoding="utf-8")
    save_chapter(BOOK_ID, chapter, prose.strip() + "\n", REPO / "books")
    (BOOK_DIR / "_operation" / f"chapter-{chapter:04d}" / "chapter_fact_summary.md").write_text(
        fact_summary.strip() + "\n", encoding="utf-8"
    )
    print(f"CHAPTER_SAVED={chapter};PROSE_CHARS={len(prose.strip())};FACT_CHARS={len(fact_summary.strip())}")


def apply_state(chapter: int) -> None:
    response_path = BOOK_DIR / "_operation" / f"chapter-{chapter:04d}" / "state_delta_response.md"
    response = _read(response_path)
    if not response.strip():
        raise ValueError("State Delta 隔离响应为空")
    book_path = BOOK_DIR / "BOOK.md"
    current_book = _read(book_path)
    updated = apply_state_delta_to_book(current_book, chapter, response)
    book_path.write_text(updated, encoding="utf-8")
    (BOOK_DIR / "runs" / f"chapter-{chapter:04d}" / "state_delta_approval.md").write_text(
        "作者实验规则批准：应用本次 State Delta v2；只更新 BOOK 状态区，不改 BOOK Contract、计划或正式章节。\n",
        encoding="utf-8",
    )
    print(f"STATE_APPLIED={chapter}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p_init = sub.add_parser("init")
    p_init.add_argument("chapter", type=int)
    p_render = sub.add_parser("render")
    p_render.add_argument("chapter", type=int)
    p_render.add_argument("mode")
    p_record = sub.add_parser("record")
    p_record.add_argument("chapter", type=int)
    p_record.add_argument("node")
    p_select = sub.add_parser("select")
    p_select.add_argument("chapter", type=int)
    p_finish = sub.add_parser("finish-writer")
    p_finish.add_argument("chapter", type=int)
    p_adopt = sub.add_parser("adopt-integrator")
    p_adopt.add_argument("chapter", type=int)
    p_finalize = sub.add_parser("finalize")
    p_finalize.add_argument("chapter", type=int)
    p_state = sub.add_parser("apply-state")
    p_state.add_argument("chapter", type=int)
    args = parser.parse_args()
    if args.command == "init":
        init_run(args.chapter)
    elif args.command == "render":
        render(args.chapter, args.mode)
    elif args.command == "record":
        record_response(args.chapter, args.node)
    elif args.command == "select":
        select_specialists(args.chapter)
    elif args.command == "finish-writer":
        finish_writer(args.chapter)
    elif args.command == "adopt-integrator":
        adopt_integrator(args.chapter)
    elif args.command == "finalize":
        finalize_chapter(args.chapter)
    elif args.command == "apply-state":
        apply_state(args.chapter)


if __name__ == "__main__":
    main()
