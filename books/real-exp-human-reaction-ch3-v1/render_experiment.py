"""《借我一招》Chapter 3 人物温度隔离实验编排器。

只读取当前 Story MVP 的 Prompt、Context、Run Ledger 和 State Delta 函数，
只写本实验目录。模型响应由外部一次性节点调用写入；本脚本不调用模型、不修改
src、不启用 Specialists/Integrator，也不创建 Chapter 1、2、4。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
EXP = REPO / "books" / "real-exp-human-reaction-ch3-v1"
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_primary_draft,
    extract_primary_fact_summary,
)
from story_mvp.prompts import (  # noqa: E402
    DEFAULT_PROMPT_TEMPLATES,
    generate_prompt,
    parse_state_delta_v2,
)
from story_mvp.run_ledger import (  # noqa: E402
    create_or_load_run,
    save_node_prompt,
    save_node_response,
)
from story_mvp.storage import (  # noqa: E402
    apply_state_delta_to_book,
    validate_chapter_body_for_save,
)


NODE_FOR_MODE = {
    "director": "director",
    "context_curator": "curator",
    "primary_writer": "primary",
    "state_delta": "state_delta",
}
MODES = tuple(NODE_FOR_MODE)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def run_dir(chapter: int) -> Path:
    return EXP / "runs" / f"chapter-{chapter:04d}"


def chapter_path(chapter: int) -> Path:
    return EXP / "chapters" / f"chapter-{chapter:04d}.md"


def section(text: str, heading: str, level: int = 1) -> str:
    marker = "#" * level
    pattern = rf"(?ms)^{re.escape(marker)}\s+{re.escape(heading)}\s*$\n(.*?)(?=^{marker}\s+|\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def chapter_plan(chapter: int) -> str:
    text = read(EXP / "CHAPTER_PLANS.md")
    match = re.search(
        rf"(?ms)^##\s+第{chapter}章：.*?\n(.*?)(?=^##\s+第\d+章：|\Z)",
        text,
    )
    title = re.search(rf"(?m)^##\s+第{chapter}章：.*$", text)
    if not match:
        raise ValueError(f"CHAPTER_PLANS.md 缺少第{chapter}章合同")
    return f"{title.group(0)}\n\n{match.group(1).strip()}" if title else match.group(1).strip()


def long_block() -> str:
    book = read(EXP / "BOOK.md")
    return section(book, "当前中期规划窗口")


def previous_prose(chapter: int) -> str:
    blocks: list[str] = []
    for number in range(1, chapter):
        body = read(chapter_path(number)).strip()
        if body:
            blocks.append(f"### 第{number}章已冻结正式正文\n\n{body}")
    return "\n\n".join(blocks)


def recent_summaries() -> str:
    status = section(read(EXP / "BOOK.md"), "当前状态、未兑现承诺与作者备注")
    return section(status, "RECENT SUMMARIES", level=2)


def author_intent(chapter: int) -> str:
    reader_priority = read(EXP / "READER_IMMEDIATE_UNDERSTANDING.md")
    return f"""这是《借我一招》隔离 Opening Three Chapter 实验的第{chapter}章。

只使用实验目录 BOOK.md、FIXED_CORE.md 和 CHAPTER_PLANS.md 中的冻结输入；不要读取其它小说、GBrain、Reference Programs 或外部来源。只运行到 Chapter 3，禁止提前写 Chapter 4 以后。

本轮通用表达目标：清楚 > 顺畅 > 有画面 > 文学感。普通读者应先知道顾长川眼前要什么、失败后果是什么、他看见了什么、做了什么、结果怎样，再接触名称和更远机制。第一次能力必须用普通语言成立：看见别人近距离完整打出一招，顾长川能让身体完整打出这一次；不是永久复制，不是整门武学，不是面板。

前三章必须形成不同阶段：第一章发现并真实逆转；第二章主角主动选择借谁的招并进行关系 / 资源博弈；第三章公开升院竞争并改变社会身份。每章重要成功后保留短暂社会反馈，不要连续叠加新危机。

## 本轮正文最高优先级补充

{reader_priority}
"""


def init_run(chapter: int) -> None:
    create_or_load_run(
        EXP,
        chapter,
        writer_mode="curator_primary",
        selected_specialists=[],
    )


def render(chapter: int, mode: str) -> Path:
    if chapter not in {1, 2, 3}:
        raise ValueError("本实验只允许 Chapter 1—3")
    if mode not in MODES:
        raise ValueError(f"不支持的 mode：{mode}")

    init_run(chapter)
    root = EXP
    run = run_dir(chapter)
    book = read(root / "BOOK.md")
    director = read(run / "director_response.md")
    curator = read(run / "curator_response.md")
    primary = read(run / "primary_response.md")
    current_outline = director if mode in {"context_curator", "primary_writer"} else ""
    template = "" if mode in {"director", "state_delta"} else DEFAULT_PROMPT_TEMPLATES[mode]
    current_plan = (
        chapter_plan(chapter)
        + "\n\n## 本轮正文最高优先级：读者立即理解\n\n"
        + read(root / "READER_IMMEDIATE_UNDERSTANDING.md")
    )

    prompt = generate_prompt(
        mode=mode,
        template=template,
        book_content=book,
        current_long_block=long_block(),
        current_chapter_plan=current_plan,
        current_outline=current_outline,
        previous_chapter_text=previous_prose(chapter),
        recent_summaries=recent_summaries(),
        creative_direction=author_intent(chapter),
        creative_state={
            "fantasy_seed": {"origin": "author_edited", "status": "author_approved"},
            "world_vision": {"origin": "author_edited", "status": "author_approved"},
            "proposal": {"origin": "author_edited", "status": "author_approved"},
        },
        fantasy_seed=read(root / "FIXED_CORE.md"),
        world_vision=read(root / "FIXED_CORE.md"),
        proposal_context=read(root / "CHAPTER_PLANS.md"),
        selected_references=[],
        gbrain_inspiration="",
        chapter_number=chapter,
        writer_mode="curator_primary",
        curator_response=curator,
        curated_context=curator,
        primary_writer_response=primary,
        primary_draft=extract_primary_draft(primary) if primary else "",
        primary_fact_summary=extract_primary_fact_summary(primary) if primary else "",
        specialist_opening_response="未提供（本实验未启用 Specialists）",
        specialist_dialogue_response="未提供（本实验未启用 Specialists）",
        specialist_action_response="未提供（本实验未启用 Specialists）",
        specialist_emotion_response="未提供（本实验未启用 Specialists）",
        enabled_specialists={"opening": False, "dialogue": False, "action": False, "emotion": False},
        chapter_prose=read(chapter_path(chapter)),
        chapter_fact_summary=read(run / "chapter_fact_summary.md"),
    )
    node = NODE_FOR_MODE[mode]
    save_node_prompt(root, chapter, node, prompt)
    target = run / f"{node}_prompt.md"
    write(target, prompt)
    return target


def record(chapter: int, node: str) -> None:
    if node not in {"director", "curator", "primary", "state_delta"}:
        raise ValueError(f"不支持的 node：{node}")
    response = read(run_dir(chapter) / f"{node}_response.md")
    if not response.strip():
        raise ValueError(f"response 为空：{run_dir(chapter) / (node + '_response.md')}")
    save_node_response(EXP, chapter, node, response)


def finalize_primary(chapter: int) -> None:
    response = read(run_dir(chapter) / "primary_response.md")
    prose = extract_primary_draft(response).strip()
    facts = extract_primary_fact_summary(response).strip()
    validate_chapter_body_for_save(prose)
    if not facts:
        raise ValueError("Primary response 缺少事实摘要")
    write(chapter_path(chapter), prose)
    write(run_dir(chapter) / "final_formal_prose.md", prose)
    write(run_dir(chapter) / "chapter_fact_summary.md", facts)


def apply_state(chapter: int) -> None:
    response = read(run_dir(chapter) / "state_delta_response.md")
    parse_state_delta_v2(response)
    current = read(EXP / "BOOK.md")
    updated = apply_state_delta_to_book(current, chapter, response)
    write(run_dir(chapter) / "BOOK_after_state_delta.md", updated)
    write(EXP / "BOOK.md", updated)


def execution_record(chapter: int) -> Path:
    run = run_dir(chapter)
    manifest = json.loads(read(run / "manifest.json"))
    nodes = {}
    calls = 0
    for node in ("director", "curator", "primary", "state_delta"):
        info = manifest["nodes"].get(node, {})
        status = info.get("status", "missing")
        if status not in {"skipped", "missing"}:
            calls += 1
        nodes[node] = {
            "status": status,
            "model_call": "single_call" if status not in {"skipped", "missing"} else "none",
            "prompt_chars": len(read(run / f"{node}_prompt.md")),
            "response_chars": len(read(run / f"{node}_response.md")),
        }
    record = {
        "book": "《借我一招》",
        "chapter": chapter,
        "writer_mode": "curator_primary",
        "model": "gpt-5.6-luna via real luna_worker",
        "model_calls": calls,
        "selected_specialists": [],
        "integrator_executed": False,
        "nodes": nodes,
    }
    target = run / "execution.json"
    write(target, json.dumps(record, ensure_ascii=False, indent=2))
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("init", "render", "record", "finalize-primary", "apply-state", "execution"),
    )
    parser.add_argument("chapter", type=int)
    parser.add_argument("value", nargs="?")
    args = parser.parse_args()
    if args.chapter not in {1, 2, 3}:
        raise SystemExit("本实验只允许 Chapter 1—3")
    if args.command == "init":
        init_run(args.chapter)
    elif args.command == "render":
        if not args.value:
            raise SystemExit("render 需要 mode")
        print(render(args.chapter, args.value))
    elif args.command == "record":
        if not args.value:
            raise SystemExit("record 需要 node")
        record(args.chapter, args.value)
    elif args.command == "finalize-primary":
        finalize_primary(args.chapter)
    elif args.command == "apply-state":
        apply_state(args.chapter)
    else:
        print(execution_record(args.chapter))


if __name__ == "__main__":
    main()
