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
TREATMENT = BASE / "phase-2-slim-curator"
OUT = BASE / "blind-judges-phase2-slim"
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
        treatment = TREATMENT / f"chapter-{chapter:04d}"
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        variants = {
            "control_full_high": body(
                (source / "authority_reviser_response.md").read_text(encoding="utf-8")
            ),
            "slim_luna_medium": (
                treatment / "luna_medium_final_body.md"
            ).read_text(encoding="utf-8").strip(),
            "slim_terra_medium": (
                treatment / "terra_medium_final_body.md"
            ).read_text(encoding="utf-8").strip(),
        }
        order = list(variants)
        random.Random(2026082940 + chapter).shuffle(order)
        labels = {letter: order[index] for index, letter in enumerate(("A", "B", "C"))}
        key[str(chapter)] = labels
        high_prompt = (source / "authority_reviser_prompt.md").read_text(
            encoding="utf-8"
        )
        tail_end = (
            "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
            if "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
            in high_prompt
            else "## PRIMARY DRAFT｜唯一待修订正文底稿"
        )
        tail = exact_top_block(
            high_prompt, "## CANON TAIL｜上一章必要衔接", tail_end
        )
        option_text = "\n\n".join(
            f"# OPTION {letter}\n{variants[name]}" for letter, name in labels.items()
        )
        reader_prompt = f"""你是匿名盲读的成熟中文男频长篇审稿人。三版共享同一冻结剧情，差别来自 Context Curator 路径。不要猜来源，不按篇幅长短评分，也不要因措辞不同自动偏向旧版。比较读者能否快速理解、人物欲望/关系、核心力量与得失、场景画面、去流程但不写空、章末牵引。事实错误或事件遗漏必须指出。

严格输出：
VERDICT: A / B / C / MIXED
CONFIDENCE: high / medium / low
READABILITY: A / B / C / TIE
CHARACTER_AND_RELATIONSHIP: A / B / C / TIE
PAYOFF_AND_POWER: A / B / C / TIE
SCENE_AND_TEXTURE: A / B / C / TIE
ANTI_PROCEDURAL_WITHOUT_DRYNESS: A / B / C / TIE
CONTINUATION_PULL: A / B / C / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
HARD_PROBLEM_C: 无 或一句
REASON: 8—15句，必须引用各版至少一个具体实现差异。

# 上一章必要尾部
{tail[-1800:]}

{option_text}
"""
        (directory / "reader_prompt.md").write_text(reader_prompt, encoding="utf-8")
        authority_prompt = f"""你是匿名 TGN Authority / Canon 盲审员。三版共享同一 Frozen Mission、World、Power、Human、Canon。先检查事件、决定、胜负、资源/物品持有、身份/力量、Reader Release、未知边界、Direct Result、State Change 与 Ending；再比较人物与正文质量。下游 Reviser 不能替 Curator 路径遗漏的 Mission 漂移洗白。硬冲突不能凭文笔获胜。

严格输出：
VERDICT: A / B / C / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
HARD_VIOLATIONS_C: 无 或逐条短写
MISSION_FIDELITY: A / B / C / TIE
CANON_AND_AUTHORITY: A / B / C / TIE
HUMAN_AND_RELATIONSHIP: A / B / C / TIE
PAYOFF_RULER_RESULT: A / B / C / TIE
ANTI_REPETITION_PROCESS: A / B / C / TIE
REASON: 8—15句，必须指出各版最重要的具体事实/实现差异。

# FROZEN AUTHORITY
{authority_pack(high_prompt)}

{option_text}
"""
        (directory / "authority_prompt.md").write_text(
            authority_prompt, encoding="utf-8"
        )
    (OUT / "blind_key.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return key


def judge_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    reader_data, reader = run(
        directory / "reader_prompt.md",
        directory / "reader_terra_acp.json",
        "gpt-5.6-terra",
    )
    (directory / "reader_terra.md").write_text(reader + "\n", encoding="utf-8")
    authority_data, authority = run(
        directory / "authority_prompt.md",
        directory / "authority_luna_acp.json",
        "gpt-5.6-luna",
    )
    (directory / "authority_luna.md").write_text(
        authority + "\n", encoding="utf-8"
    )
    return {
        "chapter": chapter,
        "reader_seconds": reader_data.get("wall_seconds"),
        "reader": reader,
        "authority_seconds": authority_data.get("wall_seconds"),
        "authority": authority,
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
