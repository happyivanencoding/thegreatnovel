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
TREATMENT = BASE / "phase-1-patch-reviser"
OUT = BASE / "blind-judges-phase1-patch"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 13, 16)


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text
    ).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def exact_top_block(prompt: str, start: str, end: str | None) -> str:
    start_index = prompt.index(start) + len(start)
    end_index = prompt.index(end, start_index) if end else len(prompt)
    return prompt[start_index:end_index].strip()


def authority_pack(prompt: str) -> str:
    specs = (
        (
            "FROZEN MISSION",
            "## FROZEN CHAPTER MISSION｜不得改剧情",
            "## CURATOR｜本章近端注意力与实现要求",
        ),
        (
            "WORLD AUTHORITY",
            "## WORLD REALITY AUTHORITY｜远端安全世界事实",
            "## READER RELEASE｜本章已批准首次释放事实；逐条核对",
        ),
        (
            "READER RELEASE",
            "## READER RELEASE｜本章已批准首次释放事实；逐条核对",
            "## POWER CORE｜Frozen Authority",
        ),
        (
            "POWER CORE",
            "## POWER CORE｜Frozen Authority",
            "## HUMAN CORE｜Frozen Authority",
        ),
        (
            "HUMAN CORE",
            "## HUMAN CORE｜Frozen Authority",
            "## CANON INDEX｜已发生事实压缩索引",
        ),
        (
            "CANON INDEX",
            "## CANON INDEX｜已发生事实压缩索引",
            "## CANON TAIL｜上一章必要衔接",
        ),
    )
    return "\n\n".join(
        f"## {label}\n{exact_top_block(prompt, start, end)}"
        for label, start, end in specs
    )


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
        treatment_dir = TREATMENT / f"chapter-{chapter:04d}"
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        control = body(
            (source / "authority_reviser_response.md").read_text(encoding="utf-8")
        )
        patch = (treatment_dir / "final_patch_body.md").read_text(encoding="utf-8").strip()
        options = {"control_high": control, "patch_medium": patch}
        order = ["control_high", "patch_medium"]
        random.Random(2026082930 + chapter).shuffle(order)
        key[str(chapter)] = {"A": order[0], "B": order[1]}
        high_prompt = (source / "authority_reviser_prompt.md").read_text(
            encoding="utf-8"
        )
        tail_start = "## CANON TAIL｜上一章必要衔接"
        tail_end = (
            "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
            if "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
            in high_prompt
            else "## PRIMARY DRAFT｜唯一待修订正文底稿"
        )
        tail = exact_top_block(high_prompt, tail_start, tail_end)
        reader = f"""你是匿名盲读的成熟中文男频长篇审稿人。两版共享同一 Primary Draft 和冻结剧情，只是后处理方式不同。不要猜来源，不按篇幅评分。比较清晰、具体、人物欲望与关系、力量/收益/损失落地、去重复与去流程、章末牵引；事实错误必须指出。允许 MIXED，但不要机械中立。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
READABILITY: A / B / TIE
CHARACTER_AND_RELATIONSHIP: A / B / TIE
PAYOFF_AND_POWER: A / B / TIE
ANTI_PROCEDURAL_PROSE: A / B / TIE
CONTINUATION_PULL: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 6—12句。

# 上一章必要尾部
{tail[-1800:]}

# OPTION A
{options[order[0]]}

# OPTION B
{options[order[1]]}
"""
        (directory / "reader_prompt.md").write_text(reader, encoding="utf-8")
        authority = f"""你是匿名 TGN Authority / Canon 盲审员。两版共享同一冻结 Mission、Canon 与 Primary Draft。先查主要事件、人物决定、资源得失、力量/身份、Reader Release、未知边界、Direct Result、State Change、Ending，再比较人物、payoff、去重复/去流程。硬冲突不能凭文笔获胜，不把“改得少”本身当优点。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
MISSION_FIDELITY: A / B / TIE
CANON_AND_AUTHORITY: A / B / TIE
HUMAN_AND_RELATIONSHIP: A / B / TIE
PAYOFF_RULER_RESULT: A / B / TIE
ANTI_REPETITION_PROCESS: A / B / TIE
REASON: 6—12句。

# FROZEN AUTHORITY
{authority_pack(high_prompt)}

# OPTION A
{options[order[0]]}

# OPTION B
{options[order[1]]}
"""
        (directory / "authority_prompt.md").write_text(authority, encoding="utf-8")
    (OUT / "blind_key.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return key


def judge_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    reader_data, reader_text = run(
        directory / "reader_prompt.md",
        directory / "reader_terra_acp.json",
        "gpt-5.6-terra",
    )
    (directory / "reader_terra.md").write_text(reader_text + "\n", encoding="utf-8")
    authority_data, authority_text = run(
        directory / "authority_prompt.md",
        directory / "authority_luna_acp.json",
        "gpt-5.6-luna",
    )
    (directory / "authority_luna.md").write_text(
        authority_text + "\n", encoding="utf-8"
    )
    return {
        "chapter": chapter,
        "reader_seconds": reader_data.get("wall_seconds"),
        "reader": reader_text,
        "authority_seconds": authority_data.get("wall_seconds"),
        "authority": authority_text,
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
