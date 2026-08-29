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
TREATMENT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "speculative-next-director-rebase-low"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "blind-speculative-next-director-rebase-low"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (3, 4, 6, 13, 15, 19)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt: Path, output: Path, model: str) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt), str(output), model, "high", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
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


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    key = {}
    for chapter in CHAPTERS:
        source = SOURCE / f"chapter-{chapter:04d}"
        treatment_dir = TREATMENT / f"chapter-{chapter:04d}"
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        control = clean((source / "director_response.md").read_text(encoding="utf-8"))
        speculative = clean((treatment_dir / "final_director.md").read_text(encoding="utf-8"))
        order = ["control", "speculative"]
        random.Random(20260829130 + chapter).shuffle(order)
        texts = {"control": control, "speculative": speculative}
        key[str(chapter)] = {"A": order[0], "B": order[1]}
        frozen = (source / "director_prompt.md").read_text(encoding="utf-8")

        story_prompt = f"""你是匿名的成熟中文男频长篇 Story Contract 审稿人。两版都是同一章的八字段 Director 合同；其中一版在上一章 State Delta 完成后生成，另一版在 State 与 Director 并行时只看到上一章正式正文尾部和旧 Canon。你不知道哪版是哪条路线，不得按来源评分。

比较哪版更适合继续生成顶级男频正文：主角主动性、具体欲望、冲突/力量/关系/奖励的前景、结果与章末推动、反程序化、Writer 可执行性。任何与最终 Canon、当前计划或上一章结果冲突的内容都是硬问题。允许 MIXED，但不要回避明确差异。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
PROTAGONIST_AGENCY: A / B / TIE
COMMERCIAL_SALIENCE: A / B / TIE
RESULT_AND_PAYOFF: A / B / TIE
ANTI_PROCEDURE: A / B / TIE
WRITER_EXECUTABILITY: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 8—14句，必须引用两版具体合同。

# FINAL FROZEN DIRECTOR INPUT AFTER STATE
{frozen}

# OPTION A
{texts[order[0]]}

# OPTION B
{texts[order[1]]}
"""
        authority_prompt = f"""你是匿名的 TGN Director Authority 审稿人。两版共享同一最终 Current Plan、上一章正式正文和完成后的 Canon State。先检查当前章事件预算、行动者/对象/顺序、Direct Result、State Change、Ending、资源/持有关系、力量位置、人物关系、未知边界与章末 Handoff；再比较故事价值。不能因为某版更精彩而原谅 Canon/Plan 硬错。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
FINAL_CANON_FIDELITY: A / B / TIE
PLAN_BUDGET_FIDELITY: A / B / TIE
RESULT_STATE_ENDING: A / B / TIE
HUMAN_POWER_WORLD: A / B / TIE
STORY_VALUE: A / B / TIE
REASON: 8—14句，必须引用两版具体合同。

# FINAL FROZEN DIRECTOR INPUT AFTER STATE
{frozen}

# OPTION A
{texts[order[0]]}

# OPTION B
{texts[order[1]]}
"""
        (directory / "story_prompt.md").write_text(story_prompt, encoding="utf-8")
        (directory / "authority_prompt.md").write_text(authority_prompt, encoding="utf-8")
    (OUT / "blind_key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")


def one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    story_data = call(directory / "story_prompt.md", directory / "story_terra_acp.json", "gpt-5.6-terra")
    story = clean(story_data.get("text", ""))
    (directory / "story_terra.md").write_text(story + "\n", encoding="utf-8")
    authority_data = call(directory / "authority_prompt.md", directory / "authority_luna_acp.json", "gpt-5.6-luna")
    authority = clean(authority_data.get("text", ""))
    (directory / "authority_luna.md").write_text(authority + "\n", encoding="utf-8")
    return {
        "chapter": chapter,
        "story_wall_seconds": story_data.get("wall_seconds"),
        "story": story,
        "authority_wall_seconds": authority_data.get("wall_seconds"),
        "authority": authority,
    }


def main() -> None:
    prepare()
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps({"chapter": row["chapter"], "story": row["story"].splitlines()[:2], "authority": row["authority"].splitlines()[:2]}, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

