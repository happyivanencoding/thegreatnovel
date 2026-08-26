"""Clean ten-chapter experiment runner.

This file is an experiment harness only. It does not call a model, select a
scene skill, or rewrite a response. All model text is supplied by the parent
Codex task after an independent subagent returns.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
EXP = REPO / "books" / "real-exp-clean-e2e-scene-skill-v11-10ch"
WORKSPACE = EXP.parent
BOOK_ID = EXP.name
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_primary_draft,
    extract_primary_fact_summary,
)
from story_mvp.prompts import (  # noqa: E402
    DEFAULT_PROMPT_TEMPLATES,
    parse_outline_fields,
    parse_state_delta_v2,
    generate_prompt,
    validate_current_outline,
)
from story_mvp.run_ledger import (  # noqa: E402
    adopt_final_source,
    create_or_load_run,
    load_run,
    mark_node_failed,
    retry_node,
    save_node_prompt,
    save_node_response,
)
from story_mvp.scene_skills import parse_scene_skill_selection  # noqa: E402
from story_mvp.storage import (  # noqa: E402
    apply_state_delta_to_book,
    approve_creative_artifact,
    compose_book_content,
    default_book_content,
    default_prompt_templates,
    parse_book_sections,
    prompt_templates_to_text,
    save_chapter,
    validate_chapter_body_for_save,
    write_book,
    write_creative_artifact,
)


CREATIVE_FILES = {
    "fantasy_seed": "FANTASY_SEED.md",
    "world_vision": "WORLD_VISION.md",
    "proposal": "PROPOSAL.md",
}
STAGE_FILES = {
    "fantasy_seed": ("fantasy_seed_prompt.md", "fantasy_seed_response.md"),
    "world_vision": ("world_vision_prompt.md", "world_vision_response.md"),
    "story_program": ("story_program_prompt.md", "story_program_response.md"),
    "outline": ("outline_prompt.md", "outline_response.md"),
}
NODE_FILES = {
    "director": ("director_prompt.md", "director_response.md"),
    "curator": ("curator_prompt.md", "curator_response.md"),
    "primary": ("primary_prompt.md", "primary_response.md"),
    "state_delta": ("state_delta_prompt.md", "state_delta_response.md"),
}
NODE_MODES = {
    "director": ("director", "director"),
    "curator": ("context_curator", "curator"),
    "primary": ("primary_writer", "primary"),
    "state_delta": ("state_delta", "state_delta"),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def book_path() -> Path:
    return EXP / "BOOK.md"


def chapter_dir(chapter: int) -> Path:
    return EXP / f"chapter-{chapter:04d}"


def run_dir(chapter: int) -> Path:
    return EXP / "runs" / f"chapter-{chapter:04d}"


def initialize() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    (EXP / "chapters").mkdir(exist_ok=True)
    (EXP / "runs").mkdir(exist_ok=True)
    if not book_path().is_file():
        write(book_path(), default_book_content())
    if not (EXP / "PROMPTS.md").is_file():
        write(EXP / "PROMPTS.md", prompt_templates_to_text(default_prompt_templates()))
    for filename in CREATIVE_FILES.values():
        if not (EXP / filename).is_file():
            write(EXP / filename, "")
    if not (EXP / "CREATIVE_STATE.json").is_file():
        write(
            EXP / "CREATIVE_STATE.json",
            json.dumps(
                {
                    "fantasy_seed": {"origin": "empty", "status": "empty"},
                    "world_vision": {"origin": "empty", "status": "empty"},
                    "proposal": {"origin": "empty", "status": "empty"},
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        )
    if not (EXP / "CALL_LOG.json").is_file():
        write(
            EXP / "CALL_LOG.json",
            json.dumps(
                {
                    "experiment": "real-exp-clean-e2e-scene-skill-v11-10ch",
                    "branch": "principal_dev_new_sys",
                    "writer_mode": "curator_primary",
                    "model": "Codex subagent；具体底层模型未由环境独立暴露",
                    "calls": [],
                    "retries": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        )


def creative_state() -> dict[str, Any]:
    return read_json(EXP / "CREATIVE_STATE.json", {})


def input_text() -> str:
    return read(EXP / "INPUT.md").strip()


def top_section(content: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        content,
    )
    return match.group(1).strip() if match else ""


def long_block(chapter: int) -> str:
    body = parse_book_sections(read(book_path())).get("long_plan", "")
    blocks = re.split(r"(?m)(?=^##\s+)", body)
    for block in blocks:
        heading = block.splitlines()[0] if block.splitlines() else ""
        range_match = re.search(
            r"第\s*(\d+)\s*[—\-~至]\s*(\d+)\s*章", heading
        )
        if range_match and int(range_match.group(1)) <= chapter <= int(range_match.group(2)):
            return block.strip()
        single_match = re.search(r"第\s*(\d+)\s*章", heading)
        if single_match and int(single_match.group(1)) == chapter:
            return block.strip()
    return body.strip()


def chapter_plan(chapter: int) -> str:
    body = parse_book_sections(read(book_path())).get("small_plan", "")
    pattern = re.compile(
        rf"(?ms)^##\s+第\s*{chapter}\s*章[：:].*?\n(.*?)(?=^##\s+第\s*\d+\s*章[：:]|\Z)"
    )
    match = pattern.search(body)
    if not match:
        return ""
    title = re.search(rf"(?m)^##\s+第\s*{chapter}\s*章[：:].*$", body)
    return (
        f"{title.group(0)}\n\n{match.group(1).strip()}"
        if title
        else match.group(1).strip()
    )


def previous_prose(chapter: int) -> str:
    chunks: list[str] = []
    for number in range(1, chapter):
        body = read(EXP / "chapters" / f"chapter-{number:04d}.md").strip()
        if body:
            chunks.append(f"# {number}章正文\n\n{body}")
    return "\n\n".join(chunks)


def recent_summaries() -> str:
    status = parse_book_sections(read(book_path())).get("status", "")
    match = re.search(r"(?ms)^##\s+RECENT SUMMARIES\s*\n(.*?)(?=^##\s+|\Z)", status)
    return match.group(1).strip() if match else ""


def stage_prompt(stage: str) -> Path:
    initialize()
    if stage not in STAGE_FILES:
        raise ValueError(f"未知创意阶段：{stage}")
    mode = "idea" if stage == "story_program" else stage
    prompt = generate_prompt(
        mode=mode,
        template=DEFAULT_PROMPT_TEMPLATES[mode],
        book_content=read(book_path()),
        creative_direction=input_text(),
        fantasy_seed=read(EXP / "FANTASY_SEED.md"),
        world_vision=read(EXP / "WORLD_VISION.md"),
        creative_state=creative_state(),
        proposal_context=read(EXP / "PROPOSAL.md"),
        selected_references=[],
        gbrain_inspiration="",
    )
    target = EXP / STAGE_FILES[stage][0]
    write(target, prompt)
    return target


def apply_creative(stage: str) -> None:
    initialize()
    if stage not in {"world_vision", "story_program"}:
        raise ValueError("该命令只接入 World Vision 或 Story Program Response")
    response = read(EXP / STAGE_FILES[stage][1])
    if not response.strip():
        raise ValueError(f"{stage} Response 为空")
    artifact = "world_vision" if stage == "world_vision" else "proposal"
    write_creative_artifact(
        BOOK_ID,
        artifact,
        response,
        WORKSPACE,
        origin="model_generated",
        workflow_source="clean_e2e_model_response",
    )
    approve_creative_artifact(BOOK_ID, artifact, WORKSPACE)
    write(
        EXP / f"{stage}_approval_fixture.md",
        "实验审批夹具：本次状态仅用于顺序推进，不是真实用户人工批准。\n",
    )


def select_fantasy_seed() -> None:
    initialize()
    selector = read(EXP / "blind_selector_response.md")
    match = re.search(
        r"(?mi)^\s*(?:最终选择|选定候选|选择)\s*[：:]\s*候选\s*(\d+)\s*$",
        selector,
    )
    if not match:
        raise ValueError("Blind Selector Response 缺少可解析的最终候选编号")
    number = int(match.group(1))
    raw = read(EXP / "fantasy_seed_response.md")
    candidate = re.search(
        rf"(?ms)^##\s+候选\s*{number}\s*[：:].*?(?=^##\s+候选\s*\d+\s*[：:]|\Z)",
        raw,
    )
    if not candidate:
        raise ValueError(f"Fantasy Seed 中找不到候选 {number}")
    selected = candidate.group(0).strip() + "\n"
    write(EXP / "fantasy_seed_selected.md", selected)
    write_creative_artifact(
        BOOK_ID,
        "fantasy_seed",
        selected,
        WORKSPACE,
        origin="model_selected",
        workflow_source="clean_e2e_blind_selector",
    )
    approve_creative_artifact(BOOK_ID, "fantasy_seed", WORKSPACE)
    write(
        EXP / "fantasy_seed_approval_fixture.md",
        "实验审批夹具：Blind Selector 选定后用于顺序推进，不是真实用户人工批准。\n",
    )


def selector_prompt() -> Path:
    initialize()
    prompt = (
        "你是本次 Clean 10-Chapter 实验的唯一 Blind Selector。\n"
        "你只能依据下方 INPUT.md 与 Fantasy Seed 候选内容作一次选择；不要重新生成候选，"
        "不要引入任何其它小说、旧实验或 Reviewer 结论，不要制作复杂评分表。\n\n"
        "选择标准：选择最有潜力成为成熟中文男频长期成长爽文、同时最适合当前系统继续展开的一个。\n\n"
        "# INPUT.md\n\n"
        + input_text()
        + "\n\n# Fantasy Seed 候选内容\n\n"
        + read(EXP / "fantasy_seed_response.md")
        + "\n\n"
        "最终返回必须先单独一行写：最终选择：候选N\n"
        "随后用不超过 300 字说明选择理由。"
    )
    target = EXP / "blind_selector_prompt.md"
    write(target, prompt)
    return target


def apply_outline() -> None:
    initialize()
    outline = read(EXP / "outline_response.md")
    if not outline.strip():
        raise ValueError("Outline Response 为空")
    sections = parse_book_sections(outline)
    required = ("design", "long_plan", "small_plan", "status")
    missing = [key for key in required if not sections.get(key, "").strip()]
    if missing:
        raise ValueError("Outline 缺少 BOOK 一级区块：" + "、".join(missing))
    content = compose_book_content(sections)
    write_book(BOOK_ID, content, WORKSPACE, source="clean_e2e_outline_apply")
    write(EXP / "BOOK_after_outline.md", content)


def reviewer_prompt() -> Path:
    initialize()
    prompt = (
        "你是本次 Clean 10-Chapter 实验的独立 Reviewer。十章已经冻结；"
        "只依据下方材料写最终复盘，不重写任何正文，不调用外部服务，不读取历史实验 Reviewer。\n\n"
        "请直接回答：这十章是不是一本小说；主角是否越来越主动；一级成长、二级收益与反哺是否成立；"
        "十章 Scene Skill 选择是否自然；Reader-First 是否稳定；人物与关系是否跨章累积；"
        "是否有 Planning Language leakage；长篇阶段感与男频爽感如何；第十章是否让人想继续读。\n"
        "不要机械打总分。必须给出最严重的 3 个真实问题、已经明确正确且不建议再动的 3 个部分、"
        "以及下一步最值得修的 1—3 个系统问题；没有真实问题时明确写没有，不要为了凑数制造问题。\n\n"
        "# INPUT.md\n\n"
        + input_text()
        + "\n\n# 当前 BOOK.md\n\n"
        + read(book_path())
        + "\n\n# TEN_CHAPTERS_COMBINED.md\n\n"
        + read(EXP / "TEN_CHAPTERS_COMBINED.md")
        + "\n\n# SCENE_SKILL_TRACE.json\n\n"
        + read(EXP / "SCENE_SKILL_TRACE.json")
        + "\n\n# DETERMINISTIC_VERIFICATION.md\n\n"
        + read(EXP / "DETERMINISTIC_VERIFICATION.md")
        + "\n\n"
        "最终输出为一份可直接保存为 FINAL_REPORT.md 的中文报告，包含清楚的判断和证据位置；"
        "不要输出内部推理过程。"
    )
    target = EXP / "reviewer_prompt.md"
    write(target, prompt)
    return target


def chapter_prompt(chapter: int, node: str) -> Path:
    initialize()
    if chapter < 1 or chapter > 10:
        raise ValueError("实验章节必须在 1—10")
    if node not in NODE_MODES:
        raise ValueError(f"未知章节节点：{node}")
    create_or_load_run(EXP, chapter, writer_mode="curator_primary", selected_specialists=[])
    mode, ledger_node = NODE_MODES[node]
    book = read(book_path())
    director = read(chapter_dir(chapter) / "director_response.md")
    curator = read(chapter_dir(chapter) / "curator_response.md")
    primary = read(chapter_dir(chapter) / "primary_response.md")
    body = read(chapter_dir(chapter) / "chapter.md")
    fact = read(chapter_dir(chapter) / "chapter_fact_summary.md")
    current_outline = director if node in {"curator", "primary"} else ""
    prompt = generate_prompt(
        mode=mode,
        template="" if mode in {"director", "state_delta"} else DEFAULT_PROMPT_TEMPLATES[mode],
        book_content=book,
        creative_direction=input_text(),
        fantasy_seed=read(EXP / "FANTASY_SEED.md"),
        world_vision=read(EXP / "WORLD_VISION.md"),
        creative_state=creative_state(),
        proposal_context=read(EXP / "PROPOSAL.md"),
        current_long_block=long_block(chapter),
        previous_chapter_text=previous_prose(chapter),
        current_outline=current_outline,
        current_chapter_plan=chapter_plan(chapter),
        recent_summaries=recent_summaries(),
        prologue_text="",
        selected_references=[],
        gbrain_inspiration="",
        chapter_number=chapter,
        chapter_prose=body if node == "state_delta" else "",
        chapter_fact_summary=fact if node == "state_delta" else "",
        writer_mode="curator_primary",
        curator_response=curator if node == "primary" else "",
        curated_context=curator if node == "primary" else "",
        primary_writer_response=primary if node == "state_delta" else "",
        primary_draft=extract_primary_draft(primary) if node == "state_delta" else "",
        primary_fact_summary=extract_primary_fact_summary(primary) if node == "state_delta" else "",
    )
    save_node_prompt(EXP, chapter, ledger_node, prompt)
    target = chapter_dir(chapter) / NODE_FILES[node][0]
    write(target, prompt)
    return target


def record_chapter_response(chapter: int, node: str, response_name: str | None = None) -> None:
    initialize()
    if node not in NODE_MODES:
        raise ValueError(f"未知章节节点：{node}")
    _, ledger_node = NODE_MODES[node]
    filename = response_name or NODE_FILES[node][1]
    response_path = chapter_dir(chapter) / filename
    response = read(response_path)
    if not response.strip():
        mark_node_failed(EXP, chapter, ledger_node)
        raise ValueError(f"{response_path} 为空")
    save_node_response(EXP, chapter, ledger_node, response)
    try:
        if node == "director":
            validate_current_outline(response)
        elif node == "curator":
            primary, secondary = parse_scene_skill_selection(response)
            write(
                chapter_dir(chapter) / "scene_skill_selection.json",
                json.dumps(
                    {
                        "chapter": chapter,
                        "primary": primary or None,
                        "secondary": secondary or None,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
            )
        elif node == "primary":
            draft = extract_primary_draft(response).strip()
            fact = extract_primary_fact_summary(response).strip()
            if not draft or not fact:
                raise ValueError("Primary Response 缺少 Primary Draft 或 Primary Fact Summary")
            validate_chapter_body_for_save(draft)
            write(chapter_dir(chapter) / "chapter.md", draft + "\n")
            write(chapter_dir(chapter) / "chapter_fact_summary.md", fact + "\n")
            adopt_final_source(EXP, chapter, "primary")
            save_chapter(
                BOOK_ID,
                chapter,
                draft + "\n",
                WORKSPACE,
                source="clean_e2e_primary",
            )
        elif node == "state_delta":
            updated = apply_state_delta_to_book(read(book_path()), chapter, response)
            write(run_dir(chapter) / "BOOK_after_state_delta.md", updated)
            write(chapter_dir(chapter) / "BOOK_after_state_delta.md", updated)
            write_book(BOOK_ID, updated, WORKSPACE, source="clean_e2e_state_delta")
            write(
                chapter_dir(chapter) / "state_delta_approval.md",
                "实验规则批准：应用本次 State Delta；仅更新实验副本状态区。\n",
            )
    except Exception:
        mark_node_failed(EXP, chapter, ledger_node)
        raise


def retry_chapter_node(chapter: int, node: str) -> None:
    initialize()
    if node not in NODE_MODES:
        raise ValueError(f"未知章节节点：{node}")
    retry_node(EXP, chapter, NODE_MODES[node][1])


def log_call(
    *,
    kind: str,
    chapter: int,
    agent_id: str,
    agent_role: str,
    prompt_file: str,
    response_file: str,
    parser_status: str,
    status: str = "completed",
    retry_of: int | None = None,
    failure_reason: str = "",
) -> None:
    initialize()
    log = read_json(EXP / "CALL_LOG.json", {"calls": [], "retries": []})
    calls = log.setdefault("calls", [])
    record: dict[str, Any] = {
        "call_index": len(calls) + 1,
        "kind": kind,
        "chapter": chapter or None,
        "agent_id": agent_id,
        "agent_role": agent_role,
        "model": "Codex subagent；具体底层模型未由环境独立暴露",
        "status": status,
        "prompt_file": prompt_file,
        "response_file": response_file,
        "parser_status": parser_status,
    }
    if retry_of is not None:
        record["retry_of_call_index"] = retry_of
    if failure_reason:
        record["failure_reason"] = failure_reason
    calls.append(record)
    if status != "completed" or retry_of is not None:
        log.setdefault("retries", []).append(record)
    write(EXP / "CALL_LOG.json", json.dumps(log, ensure_ascii=False, indent=2) + "\n")


def status() -> None:
    initialize()
    print(json.dumps(load_run(EXP, int(args.chapter)), ensure_ascii=False, indent=2))


def main() -> None:
    global args
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")
    p_stage = sub.add_parser("stage-prompt")
    p_stage.add_argument("stage", choices=tuple(STAGE_FILES))
    p_apply = sub.add_parser("apply-creative")
    p_apply.add_argument("stage", choices=("world_vision", "story_program"))
    sub.add_parser("select-fantasy")
    sub.add_parser("selector-prompt")
    sub.add_parser("apply-outline")
    sub.add_parser("reviewer-prompt")

    p_cp = sub.add_parser("chapter-prompt")
    p_cp.add_argument("chapter", type=int)
    p_cp.add_argument("node", choices=tuple(NODE_MODES))
    p_cr = sub.add_parser("record-chapter")
    p_cr.add_argument("chapter", type=int)
    p_cr.add_argument("node", choices=tuple(NODE_MODES))
    p_cr.add_argument("--response-file")
    p_retry = sub.add_parser("retry-chapter")
    p_retry.add_argument("chapter", type=int)
    p_retry.add_argument("node", choices=tuple(NODE_MODES))

    p_log = sub.add_parser("log-call")
    p_log.add_argument("--kind", required=True)
    p_log.add_argument("--chapter", type=int, default=0)
    p_log.add_argument("--agent-id", required=True)
    p_log.add_argument("--agent-role", required=True)
    p_log.add_argument("--prompt-file", required=True)
    p_log.add_argument("--response-file", required=True)
    p_log.add_argument("--parser-status", required=True)
    p_log.add_argument("--status", default="completed")
    p_log.add_argument("--retry-of", type=int)
    p_log.add_argument("--failure-reason", default="")

    parsed = parser.parse_args()
    args = parsed
    if parsed.command == "init":
        initialize()
    elif parsed.command == "stage-prompt":
        print(stage_prompt(parsed.stage))
    elif parsed.command == "apply-creative":
        apply_creative(parsed.stage)
    elif parsed.command == "select-fantasy":
        select_fantasy_seed()
    elif parsed.command == "selector-prompt":
        print(selector_prompt())
    elif parsed.command == "apply-outline":
        apply_outline()
    elif parsed.command == "reviewer-prompt":
        print(reviewer_prompt())
    elif parsed.command == "chapter-prompt":
        print(chapter_prompt(parsed.chapter, parsed.node))
    elif parsed.command == "record-chapter":
        record_chapter_response(parsed.chapter, parsed.node, parsed.response_file)
    elif parsed.command == "retry-chapter":
        retry_chapter_node(parsed.chapter, parsed.node)
    elif parsed.command == "log-call":
        log_call(
            kind=parsed.kind,
            chapter=parsed.chapter,
            agent_id=parsed.agent_id,
            agent_role=parsed.agent_role,
            prompt_file=parsed.prompt_file,
            response_file=parsed.response_file,
            parser_status=parsed.parser_status,
            status=parsed.status,
            retry_of=parsed.retry_of,
            failure_reason=parsed.failure_reason,
        )


if __name__ == "__main__":
    main()
