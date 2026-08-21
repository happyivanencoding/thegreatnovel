"""Curator -> Primary longform stability test 的实验编排器。

它只调用 Story MVP 当前正式的 Prompt、Ledger、正文解析和 State Delta 函数。
模型响应由隔离的真实子代理写入 _operation，再由本文件原样接入实验副本；本文件
不调用模型、不自动重试、不编辑 src/，也不提供第二套 Hybrid Runtime。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
EXP = REPO / "books" / "real-exp-curator-primary-longform-v1"
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_final_chapter_artifact,
    extract_primary_draft,
    extract_primary_fact_summary,
)
from story_mvp.prompts import (  # noqa: E402
    DEFAULT_PROMPT_TEMPLATES,
    generate_prompt,
    parse_state_delta_v2,
)
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
    compose_book_content,
    parse_book_sections,
    save_chapter,
    validate_chapter_body_for_save,
)


CANDIDATES = {
    "candidate-b": "《炉藏万象》",
}
MAX_CHAPTER = 10
SPECIALISTS = ("opening", "dialogue", "action", "emotion")
CREATIVE_STATE = {
    "fantasy_seed": {"origin": "frozen_prior_experiment", "status": "author_approved"},
    "world_vision": {"origin": "frozen_prior_experiment", "status": "author_approved"},
    "proposal": {"origin": "frozen_prior_experiment", "status": "author_approved"},
}
NODE_FOR_MODE = {
    "director": "director",
    "context_curator": "curator",
    "primary_writer": "primary",
    "specialist_opening": "opening",
    "specialist_dialogue": "dialogue",
    "specialist_action": "action",
    "specialist_emotion": "emotion",
    "chapter_integrator": "integrator",
    "state_delta": "state_delta",
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


def run_dir(candidate: str, chapter: int) -> Path:
    return candidate_dir(candidate) / "runs" / f"chapter-{chapter:04d}"


def operation_dir(candidate: str, chapter: int) -> Path:
    return candidate_dir(candidate) / "_operation" / f"chapter-{chapter:04d}"


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def outline_text(candidate: str) -> str:
    return read(candidate_dir(candidate) / "outline" / "outline_response.md")


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
    chunks: list[str] = []
    for number in range(1, chapter):
        body = read(candidate_dir(candidate) / "chapters" / f"chapter-{number:04d}.md").strip()
        if body:
            chunks.append(f"### 第{number}章已批准正文\n\n{body}")
    return "\n\n".join(chunks)


def recent_summaries(book: str) -> str:
    status = section(book, "当前状态、未兑现承诺与作者备注")
    match = re.search(r"(?ms)^## RECENT SUMMARIES\s*\n(.*?)(?=^##\s+|\Z)", status)
    return match.group(1).strip() if match else ""


def reset_book_to_clean_state(candidate: str) -> None:
    """从冻结 source 保留设计，只复原旧 Single Pilot 的 clean Canon 状态。"""

    root = candidate_dir(candidate)
    source = read(root / "source" / "BOOK_after_old_experiment.md")
    sections = parse_book_sections(source)
    sections["status"] = "\n\n".join(
        (
            "## ACTIVE SCENE STATE：\n故事尚未开始；当前实验从冻结的 Fantasy Seed、World Vision、Story Program 和既有长篇设计重新生成开书 Outline。",
            "## PERSISTENT CANON：\n冻结上游设计只约束未来创作，不把旧实验前三章正文写入本次 Canon。",
            "## RECENT SUMMARIES：\n当前尚无已完成正文或已批准章节摘要。",
            "## OPEN PROMISES：\n本实验尚未生成任何章节；只允许运行至 Chapter 3。",
            "## AUTHOR NOTES（作者元控制；不属于 Canon 事实；State Delta 不得自动修改或删除）：\n本 BOOK.md 是 opening-pipeline-comparison-v2 的实验副本；不会写入正式书籍 Canon。",
        )
    )
    write(root / "BOOK.md", compose_book_content(sections))


def _response(candidate: str, chapter: int, node: str) -> str:
    return read(operation_dir(candidate, chapter) / f"{node}_response.md")


def _manifest_selected(candidate: str, chapter: int) -> list[str]:
    return list(load_run(candidate_dir(candidate), chapter).get("selected_specialists", []))


def render(candidate: str, chapter: int, mode: str, *, fallback: bool = False) -> Path:
    if mode not in {"director", "chapter_prep", *NODE_FOR_MODE.keys()}:
        raise ValueError(f"不支持的执行模式：{mode}")
    root = candidate_dir(candidate)
    run = run_dir(candidate, chapter)
    run.mkdir(parents=True, exist_ok=True)
    book = read(root / "BOOK.md")
    outline = outline_text(candidate)
    prep = read(run / "chapter_prep_response.md")
    curator = "" if fallback else read(run / "curator_response.md")
    primary = read(run / "primary_response.md")
    selected = _manifest_selected(candidate, chapter) if (run / "manifest.json").is_file() else []
    specialists = {name: read(run / f"{name}_response.md") for name in SPECIALISTS}
    current_outline = prep if mode not in {"director", "chapter_prep", "state_delta"} else ""
    template = "" if mode in {"director", "state_delta"} else DEFAULT_PROMPT_TEMPLATES[mode]
    prompt = generate_prompt(
        mode=mode,
        template=template,
        book_content=book,
        current_long_block=long_block(outline, chapter),
        current_chapter_plan=chapter_plan(outline, chapter),
        current_outline=current_outline,
        previous_chapter_text=previous_prose(candidate, chapter),
        recent_summaries=recent_summaries(book),
        creative_direction=f"严格执行当前实验的第{chapter}章；不要提前结算第{chapter + 1}章及以后。",
        creative_state=CREATIVE_STATE,
        fantasy_seed=read(root / "source" / "fantasy_seed.md"),
        world_vision=read(root / "source" / "world_vision.md"),
        proposal_context=read(root / "source" / "story_program.md"),
        selected_references=[],
        gbrain_inspiration="",
        chapter_number=chapter,
        writer_mode="hybrid_selective",
        curator_response=curator,
        curated_context=curator,
        primary_writer_response=primary,
        primary_draft=extract_primary_draft(primary) if primary else "",
        primary_fact_summary=extract_primary_fact_summary(primary) if primary else "",
        specialist_opening_response=specialists["opening"],
        specialist_dialogue_response=specialists["dialogue"],
        specialist_action_response=specialists["action"],
        specialist_emotion_response=specialists["emotion"],
        enabled_specialists={name: name in selected for name in SPECIALISTS},
        chapter_prose=read(root / "chapters" / f"chapter-{chapter:04d}.md"),
        chapter_fact_summary=read(run / "chapter_fact_summary.md"),
    )
    if fallback:
        target = run / "primary_fallback_prompt.md"
        write(target, prompt)
        return target
    target = run / f"{('chapter_prep' if mode == 'chapter_prep' else NODE_FOR_MODE[mode])}_prompt.md"
    if mode == "chapter_prep":
        write(target, prompt)
    else:
        save_node_prompt(root, chapter, NODE_FOR_MODE[mode], prompt)
        write(target, prompt)
    write(operation_dir(candidate, chapter) / f"{mode}_prompt.md", prompt)
    return target


def init_run(candidate: str, chapter: int) -> None:
    create_or_load_run(
        candidate_dir(candidate),
        chapter,
        writer_mode="hybrid_selective",
        selected_specialists=[],
    )


def record_response(candidate: str, chapter: int, node: str) -> None:
    response = _response(candidate, chapter, node)
    if not response.strip():
        raise ValueError(f"隔离响应为空：{operation_dir(candidate, chapter) / (node + '_response.md')}")
    root = candidate_dir(candidate)
    if node == "chapter_prep":
        write(run_dir(candidate, chapter) / "chapter_prep_response.md", response)
    else:
        save_node_response(root, chapter, node, response)


def select_specialists(candidate: str, chapter: int) -> list[str]:
    response = read(run_dir(candidate, chapter) / "director_response.md")
    selected = [
        name
        for name in SPECIALISTS
        if re.search(rf"^{name.capitalize()}：\s*启用\b", response, flags=re.MULTILINE)
    ][:2]
    set_selected_specialists(candidate_dir(candidate), chapter, selected)
    write(
        operation_dir(candidate, chapter) / "selected_specialists.md",
        "\n".join(selected) + ("\n" if selected else "（无）\n"),
    )
    return selected


def finish_writer(candidate: str, chapter: int) -> str | None:
    root = candidate_dir(candidate)
    run = run_dir(candidate, chapter)
    selected = _manifest_selected(candidate, chapter)
    responses = {name: read(run / f"{name}_response.md") for name in selected}
    if should_run_integrator(responses):
        return None
    skip_integrator_if_no_patches(root, chapter, responses)
    adopt_final_source(root, chapter, "primary")
    return "primary"


def adopt_integrator(candidate: str, chapter: int) -> str:
    adopt_final_source(candidate_dir(candidate), chapter, "integrator")
    return "integrator"


def finalize_chapter(candidate: str, chapter: int) -> None:
    root = candidate_dir(candidate)
    run = run_dir(candidate, chapter)
    manifest = load_run(root, chapter)
    source = manifest.get("final_source")
    if source not in {"primary", "integrator"}:
        raise ValueError("正式正文来源尚未采用")
    response = read(run / f"{source}_response.md")
    if source == "integrator":
        artifact = extract_final_chapter_artifact(response)
        if artifact is None:
            raise ValueError("Integrator Response 缺少 # 正式正文 / # 章节事实摘要")
        prose, fact_summary = artifact
    else:
        prose = extract_primary_draft(response)
        fact_summary = extract_primary_fact_summary(response)
    validate_chapter_body_for_save(prose)
    write(run / "final_formal_prose.md", prose.strip() + "\n")
    write(run / "chapter_fact_summary.md", fact_summary.strip() + "\n")
    save_chapter(candidate, chapter, prose.strip() + "\n", EXP, source="experiment_hybrid_selective")
    write(operation_dir(candidate, chapter) / "chapter_fact_summary.md", fact_summary.strip() + "\n")


def apply_state(candidate: str, chapter: int) -> None:
    root = candidate_dir(candidate)
    run = run_dir(candidate, chapter)
    response = read(run / "state_delta_response.md")
    if not response.strip():
        raise ValueError("State Delta response 为空")
    parse_state_delta_v2(response)
    updated = apply_state_delta_to_book(read(root / "BOOK.md"), chapter, response)
    write(run / "BOOK_after_state_delta.md", updated)
    write(root / "BOOK.md", updated)
    write(
        run / "state_delta_approval.md",
        "作者实验规则批准：应用本次 State Delta v2；只更新实验副本 BOOK 状态区，不改 BOOK Contract、计划或正式章节。\n",
    )


def _file_chars(path: Path) -> int:
    return len(read(path))


def write_execution_record(candidate: str, chapter: int) -> Path:
    run = run_dir(candidate, chapter)
    manifest = load_run(candidate_dir(candidate), chapter)
    selected = list(manifest.get("selected_specialists", []))
    ordered = ["director", "chapter_prep", "curator", "primary", *selected, "integrator", "state_delta"]
    node_records: dict[str, dict[str, object]] = {}
    calls = 0
    for node in ordered:
        if node == "chapter_prep":
            prompt_path = run / "chapter_prep_prompt.md"
            response_path = run / "chapter_prep_response.md"
            status = "completed" if response_path.is_file() else "missing"
        else:
            info = manifest["nodes"].get(node, {})
            prompt_path = run / (info.get("prompt_file") or f"{node}_prompt.md")
            response_path = run / (info.get("response_file") or f"{node}_response.md")
            status = info.get("status", "missing")
        if status not in {"skipped", "missing"}:
            calls += 1
        node_records[node] = {
            "status": status,
            "model_call": "single_call" if status not in {"skipped", "missing"} else "none",
            "input_tokens": "UNKNOWN",
            "output_tokens": "UNKNOWN",
            "prompt_chars": _file_chars(prompt_path) if prompt_path.is_file() else "UNKNOWN",
            "response_chars": _file_chars(response_path) if response_path.is_file() else "UNKNOWN",
        }
    record = {
        "candidate": CANDIDATES[candidate],
        "chapter": chapter,
        "writer_mode": "hybrid_selective",
        "selected_specialists": selected,
        "integrator_executed": manifest["nodes"]["integrator"].get("status") not in {"skipped", "missing"},
        "final_source": manifest.get("final_source"),
        "model": "gpt-5.6-luna via real subagent",
        "model_calls": calls,
        "input_tokens": "UNKNOWN",
        "output_tokens": "UNKNOWN",
        "total_tokens": "UNKNOWN",
        "nodes": node_records,
    }
    target = run / "execution.json"
    write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("init", "render", "render-fallback", "record", "select", "finish", "adopt-integrator", "finalize", "apply-state", "execution"))
    parser.add_argument("candidate", choices=tuple(CANDIDATES))
    parser.add_argument("chapter", type=int, nargs="?")
    parser.add_argument("value", nargs="?")
    args = parser.parse_args()
    if args.chapter is None or args.chapter < 1 or args.chapter > MAX_CHAPTER:
        raise SystemExit(f"本实验只允许 Chapter 1—{MAX_CHAPTER}")
    if args.command == "init":
        init_run(args.candidate, args.chapter)
    elif args.command == "render":
        if not args.value:
            raise SystemExit("render 需要 mode")
        print(render(args.candidate, args.chapter, args.value))
    elif args.command == "render-fallback":
        print(render(args.candidate, args.chapter, "primary_writer", fallback=True))
    elif args.command == "record":
        if not args.value:
            raise SystemExit("record 需要 node")
        record_response(args.candidate, args.chapter, args.value)
    elif args.command == "select":
        print(",".join(select_specialists(args.candidate, args.chapter)))
    elif args.command == "finish":
        print(finish_writer(args.candidate, args.chapter) or "integrator_required")
    elif args.command == "adopt-integrator":
        print(adopt_integrator(args.candidate, args.chapter))
    elif args.command == "finalize":
        finalize_chapter(args.candidate, args.chapter)
    elif args.command == "apply-state":
        apply_state(args.candidate, args.chapter)
    else:
        print(write_execution_record(args.candidate, args.chapter))


if __name__ == "__main__":
    main()
