from __future__ import annotations

import json
import random
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
TREATMENT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "speculative-next-director-downstream"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "blind-speculative-next-director-downstream"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (3, 4, 6, 13, 15, 19)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def h2_block(text: str, prefix: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(headings):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[match.end():end].strip()
    return ""


def call(prompt: Path, output: Path, model: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                ["node", str(RUNNER), str(prompt), str(output), model, "high", str(ROOT)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout after 1200s: {prompt}"
            time.sleep(2 + attempt * 2)
            continue
        if process.returncode == 0 and output.exists():
            try:
                data = json.loads(output.read_text(encoding="utf-8"))
            except Exception as error:
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def prepare() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    key = {}
    for chapter in CHAPTERS:
        source = SOURCE / f"chapter-{chapter:04d}"
        treatment_dir = TREATMENT / f"chapter-{chapter:04d}"
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        control = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
        candidate = (treatment_dir / "final_body.md").read_text(encoding="utf-8").strip()
        order = ["control", "speculative_downstream"]
        random.Random(20260829640 + chapter).shuffle(order)
        texts = {"control": control, "speculative_downstream": candidate}
        key[str(chapter)] = {"A": order[0], "B": order[1]}
        authority_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
        blocks = []
        for label, prefix in (
            ("FROZEN MISSION", "FROZEN CHAPTER MISSION"),
            ("WORLD AUTHORITY", "WORLD REALITY AUTHORITY"),
            ("READER RELEASE", "READER RELEASE"),
            ("POWER CORE", "POWER CORE"),
            ("HUMAN CORE", "HUMAN CORE"),
            ("CANON INDEX", "CANON INDEX"),
            ("CANON TAIL", "CANON TAIL"),
        ):
            value = h2_block(authority_prompt, prefix)
            if value:
                blocks.append(f"## {label}\n{value}")
        authority = "\n\n".join(blocks)
        tail = h2_block(authority_prompt, "CANON TAIL")

        reader_prompt = f"""你是匿名盲读的成熟中文男频长篇审稿人。两版来自同一最终章节计划和相同模型链；你不知道哪版的 Director 与上一章 State 并行生成。只评最终正文。

目标是缩小与顶级男频的差距：主角主动、欲望具体、力量/获得/关系/身份真正落地，冲突与场面有重量，人物有独立声音，同时清楚、快速、少流程、少后台抽象、少重复证明。任何事实硬错也属于严重阅读问题。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
READABILITY_AND_PACE: A / B / TIE
PROTAGONIST_AGENCY: A / B / TIE
CHARACTER_RELATIONSHIP: A / B / TIE
POWER_PAYOFF_REWARD: A / B / TIE
ANTI_PROCEDURE_AI_FLAVOR: A / B / TIE
CONTINUATION_PULL: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 8—14句，使用具体事件证据，不长引原文。

# 上一章必要尾部
{tail[-1800:] if tail else '未提供。'}

# OPTION A
{texts[order[0]]}

# OPTION B
{texts[order[1]]}
"""
        authority_judge_prompt = f"""你是匿名 TGN Authority / Canon 盲审员。两版最终正文共享同一 Frozen Mission、最终 Canon、World / Power / Human Authority、Reader Release 与 Ending。你不知道哪版使用投机 Director。

先检查主要事件顺序、行动者和对象、胜负、资源/物品归属、伤势、身份/力量位置、知识边界、Reader Release、Direct Result、State Change、Ending 与下一章 Handoff；再比较人物欲望、关系、Public Proof、收益和反程序化质量。任何 hard violation 不能被文笔抵消。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
MISSION_FIDELITY: A / B / TIE
CANON_WORLD_POWER_HUMAN: A / B / TIE
RESULT_STATE_ENDING: A / B / TIE
PAYOFF_AND_RELATIONSHIP: A / B / TIE
STORY_VALUE: A / B / TIE
REASON: 8—14句，使用具体事件层证据。

# FROZEN AUTHORITY
{authority}

# OPTION A
{texts[order[0]]}

# OPTION B
{texts[order[1]]}
"""
        (directory / "reader_prompt.md").write_text(reader_prompt, encoding="utf-8")
        (directory / "authority_prompt.md").write_text(authority_judge_prompt, encoding="utf-8")
    (OUT / "blind_key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")
    return key


def one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    reader_data = call(directory / "reader_prompt.md", directory / "reader_terra_acp.json", "gpt-5.6-terra")
    reader = clean(reader_data.get("text", ""))
    (directory / "reader_terra.md").write_text(reader + "\n", encoding="utf-8")
    authority_data = call(directory / "authority_prompt.md", directory / "authority_luna_acp.json", "gpt-5.6-luna")
    authority = clean(authority_data.get("text", ""))
    (directory / "authority_luna.md").write_text(authority + "\n", encoding="utf-8")
    return {
        "chapter": chapter,
        "reader_wall_seconds": reader_data.get("wall_seconds"),
        "reader": reader,
        "authority_wall_seconds": authority_data.get("wall_seconds"),
        "authority": authority,
    }


def main() -> None:
    prepare()
    rows = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps({"chapter": row["chapter"], "reader": row["reader"].splitlines()[:2], "authority": row["authority"].splitlines()[:2]}, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
