from __future__ import annotations

import json
import random
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
BASE = ROOT / "books" / "real-exp-chapter-latency-optimization-20260829-v1"
TREATMENT = BASE / "phase-3-conditional-director"
OUT = BASE / "blind-judges-phase3-director"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 13, 16, 19, 20)


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text
    ).strip()


def exact_top_block(prompt: str, start: str, end: str | None) -> str:
    start_index = prompt.index(start) + len(start)
    end_index = prompt.index(end, start_index) if end else len(prompt)
    return prompt[start_index:end_index].strip()


def context_pack(chapter: int, prompt: str) -> str:
    blocks = []
    specs = (
        (
            "CURRENT CHAPTER PLAN",
            "## 当前章十章计划条目",
            "## compact Growth Genome",
        ),
        (
            "CANON INDEX",
            "## 当前 Canon Index",
            "## 最近 1—3 章摘要",
        ),
        (
            "RECENT SUMMARIES",
            "## 最近 1—3 章摘要",
            "## 前文章末必要衔接",
        ),
        (
            "PREVIOUS TAIL",
            "## 前文章末必要衔接",
            "## 作者当前章意图",
        ),
        ("AUTHOR INTENT", "## 作者当前章意图", None),
    )
    for label, start, end in specs:
        if start not in prompt:
            continue
        content = exact_top_block(prompt, start, end)
        if label == "CURRENT CHAPTER PLAN":
            match = re.search(
                rf"(?ms)^##\s*第{chapter}章(?:[：:].*)?$.*?(?=^##\s*第\d+章(?:[：:].*)?$|\Z)",
                content,
            )
            if match:
                content = match.group(0).strip()
        if label == "PREVIOUS TAIL":
            content = content[-1800:]
        blocks.append(f"## {label}\n{content}")
    return "\n\n".join(blocks)


def run(prompt: Path, output: Path, model: str) -> tuple[dict, str]:
    process = subprocess.run(
        [
            "node",
            str(RUNNER),
            str(prompt),
            str(output),
            model,
            "high",
            str(ROOT),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.returncode:
        raise RuntimeError(process.stderr[-3000:])
    data = json.loads(output.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(str(data.get("error")))
    return data, clean(data.get("text", ""))


def prepare() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    key = {}
    for chapter in CHAPTERS:
        source = SOURCE / f"chapter-{chapter:04d}"
        treatment = TREATMENT / f"chapter-{chapter:04d}"
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        variants = {
            "control_full_director": clean(
                (source / "director_response.md").read_text(encoding="utf-8")
            ),
            "conditional_director": clean(
                (treatment / "conditional_director_response.md").read_text(
                    encoding="utf-8"
                )
            ),
        }
        order = list(variants)
        random.Random(2026082950 + chapter).shuffle(order)
        labels = {"A": order[0], "B": order[1]}
        key[str(chapter)] = labels
        source_prompt = (source / "director_prompt.md").read_text(encoding="utf-8")
        options = "\n\n".join(
            f"# OPTION {letter}\n{variants[name]}" for letter, name in labels.items()
        )
        authority_prompt = f"""你是匿名 TGN Director Contract 权威审计员。两版都试图把同一逐章计划与 Canon 编译成八字段合同。不要猜来源。先检查本章唯一事件预算、必须兑现结果、Canon、未兑现收益、未知边界、章末 Reservation 与 `[PLAN OUTCOME ADJUSTMENT]` 是否只有真实 Canon 冲突才使用。不能让更简洁或更有力的措辞掩盖提前结算、漏结果或偷下一章。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条
HARD_VIOLATIONS_B: 无 或逐条
EVENT_BUDGET_FIDELITY: A / B / TIE
REQUIRED_RESULT_FIDELITY: A / B / TIE
CANON_AND_UNPAID_BOUNDARY: A / B / TIE
ENDING_RESERVATION: A / B / TIE
DOWNSTREAM_SAFETY: A / B / TIE
REASON: 8—15句，逐项引用具体字段。

# FROZEN INPUT
{context_pack(chapter, source_prompt)}

{options}
"""
        (directory / "authority_prompt.md").write_text(
            authority_prompt, encoding="utf-8"
        )
        story_prompt = f"""你是匿名成熟中文男频长篇策划审稿人。比较两份当前章八字段合同，不猜来源，不把更长当更好。先守住逐章计划与 Canon，再看谁更具体地抓住人物欲望、关键选择、核心幻想、真正结果、对手反应与下一章牵引；避免工程流程、后台术语和主角协调员化。任何提前奖励、漏掉代价/未知或 pipeline 语言进入故事合同都要指出。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
STORY_SALIENCE: A / B / TIE
CHARACTER_AGENCY: A / B / TIE
PAYOFF_WITHOUT_OVERPAY: A / B / TIE
ANTI_PROCEDURAL: A / B / TIE
CONTINUATION_CAUSALITY: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 8—15句，必须引用两版具体差异。

# FROZEN INPUT
{context_pack(chapter, source_prompt)}

{options}
"""
        (directory / "story_prompt.md").write_text(story_prompt, encoding="utf-8")
    (OUT / "blind_key.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return key


def judge_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    authority_data, authority = run(
        directory / "authority_prompt.md",
        directory / "authority_luna_acp.json",
        "gpt-5.6-luna",
    )
    (directory / "authority_luna.md").write_text(
        authority + "\n", encoding="utf-8"
    )
    story_data, story = run(
        directory / "story_prompt.md",
        directory / "story_terra_acp.json",
        "gpt-5.6-terra",
    )
    (directory / "story_terra.md").write_text(story + "\n", encoding="utf-8")
    return {
        "chapter": chapter,
        "authority_seconds": authority_data.get("wall_seconds"),
        "authority": authority,
        "story_seconds": story_data.get("wall_seconds"),
        "story": story,
    }


def main() -> None:
    prepare()
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(judge_one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
