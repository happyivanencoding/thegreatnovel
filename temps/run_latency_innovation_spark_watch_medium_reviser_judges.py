from __future__ import annotations

import json
import random
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
TREATMENT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "spark-watch-medium-reviser"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "blind-spark-watch-medium-reviser"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (3, 10, 19)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


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


def authority_context(chapter: int) -> str:
    text = (SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    return text.split("## PRIMARY DRAFT｜唯一待修订正文底稿", 1)[0].strip()


def control_body(chapter: int) -> str:
    adopted = BOOK / "chapters" / f"chapter-{chapter:04d}.md"
    if adopted.exists():
        return adopted.read_text(encoding="utf-8").strip()
    return body((SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_response.md").read_text(encoding="utf-8"))


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    key = {}
    for chapter in CHAPTERS:
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        control = control_body(chapter)
        treatment = (TREATMENT / f"chapter-{chapter:04d}" / "final_body.md").read_text(encoding="utf-8").strip()
        order = ["control", "spark_watch_medium"]
        random.Random(20260829210 + chapter).shuffle(order)
        texts = {"control": control, "spark_watch_medium": treatment}
        key[str(chapter)] = {"A": order[0], "B": order[1]}
        previous_tail = ""
        if chapter > 1:
            previous_tail = (BOOK / "chapters" / f"chapter-{chapter-1:04d}.md").read_text(encoding="utf-8")[-2200:]
        reader_prompt = f"""你是匿名的成熟中文男频长篇读者审稿人。两版来自同一冻结章节，不要猜模型、架构或哪版加入了额外灵感，也不因字数长短自动评分。

比较哪一版更接近顶级男频：主角是否像具体的人并主动争取欲望；核心幻想、力量、奖励、关系与社会反馈是否更有分量；场景是否清楚、紧凑、有惊喜或反差；是否减少工程/报告/流程味；结果和章末是否真正落地；是否为制造“人味”或爽感新增了不合法事实。允许 MIXED，但不要用 MIXED 回避明确差异。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
PROTAGONIST_AGENCY: A / B / TIE
COMMERCIAL_PULL: A / B / TIE
HUMAN_DESIRE: A / B / TIE
FANTASY_PAYOFF: A / B / TIE
RELATIONSHIP_SOCIAL_REPRICING: A / B / TIE
SCENE_CLARITY: A / B / TIE
ANTI_AI_PROCEDURE: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 8—14句，必须引用双方具体正文。

# PREVIOUS TAIL
{previous_tail}

# OPTION A
{texts[order[0]]}

# OPTION B
{texts[order[1]]}
"""
        authority_prompt = f"""你是匿名的 TGN Final Draft Authority 审稿人。两版共享同一 Frozen Mission、Curator、World、Reader Release、Power/Human Core、Canon 与上一章尾部。先核对行动者/对象/顺序、Direct Result、State Change、Ending、资源/持有关系、时间窗口、力量位置、未知边界、Reader Release、Named Entity；任何硬错不能被更强爽感抵消。再比较哪版更好保护主角主动性、Human desire、核心幻想、Payoff、Public Proof、关系和故事价值。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
MISSION_RESULT_ENDING: A / B / TIE
CANON_POWER_WORLD: A / B / TIE
OWNERSHIP_TIME_NAMED_ENTITY: A / B / TIE
HUMAN_DESIRE_RELATIONSHIP: A / B / TIE
PAYOFF_PUBLIC_PROOF: A / B / TIE
PRESERVATION_AND_STORY_VALUE: A / B / TIE
REASON: 8—14句，必须引用双方具体正文。

# FROZEN AUTHORITY
{authority_context(chapter)}

# OPTION A
{texts[order[0]]}

# OPTION B
{texts[order[1]]}
"""
        (directory / "reader_prompt.md").write_text(reader_prompt, encoding="utf-8")
        (directory / "authority_prompt.md").write_text(authority_prompt, encoding="utf-8")
    (OUT / "blind_key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")


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
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps({"chapter": row["chapter"], "reader": row["reader"].splitlines()[:2], "authority": row["authority"].splitlines()[:2]}, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
