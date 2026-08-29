from __future__ import annotations

import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
POLISH = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "post-authority-reader-polish-all20"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "reader-polish-value-gate"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

GATE_TEMPLATE = """你是 TGN 的 Value-Preservation Gate，使用独立 GPT-5.6 Luna medium。上游 Terra medium 只提出了一个纯表达 Patch；你不润色、不改写，只判断它是否可以安全应用。

判定标准非常保守：
- `ACCEPT` 仅当 OLD 的全部事实、人物欲望、情绪对照、关系阶段、立场、世界/力量体验、Payoff、节拍停顿与因果，都已由紧邻上下文更具体地完整承担；删除/压缩后只有明确的重复总结、报告腔或同义确认消失。
- 稳定 Human 牵引不因“读者大概能懂”而删除。尤其保留：不怕真实损失但厌恶伪造天灾、贪钱/算账、审美/占有、旧情与恼火并存、不求人/不示弱、救命恩与明码标价的关系变化，以及重大结果后的欲望确认。
- 一句很短也可能承担人物或关系的一拍；“动作已经证明”不是自动删除理由。
- NEW 不得改变行动者、对象、时态、否定/肯定、数字、持有关系、能力边界、未知强度、资源、奖励或 Ending。
- 只要存在任何独特价值、事实强度变化或不确定，`REJECT`。宁可保留原文。

严格输出：
DECISION: ACCEPT / REJECT
FACT_EQUIVALENT: YES / NO / UNCERTAIN
UNIQUE_HUMAN_RELATIONSHIP_VALUE: NONE / PRESENT / UNCERTAIN
UNIQUE_FANTASY_PAYOFF_VALUE: NONE / PRESENT / UNCERTAIN
PURE_REDUNDANCY: YES / NO / UNCERTAIN
REASON: 4—8句，必须引用 OLD 与邻近上下文。
"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "medium", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if process.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
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


def authority_block(chapter: int) -> str:
    prompt = (SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    start = prompt.index("## FROZEN CHAPTER MISSION")
    end = prompt.index("## CANON INDEX", start)
    return prompt[start:end].strip()


def local_context(original: str, old: str) -> str:
    parts = paragraphs(original)
    joined = "\n\n".join(parts)
    if joined.count(old) != 1:
        # Preserve exact original formatting as fallback context.
        index = original.index(old)
        return original[max(0, index - 800): min(len(original), index + len(old) + 800)]
    for index, paragraph in enumerate(parts):
        if old in paragraph or paragraph in old:
            lo = max(0, index - 2)
            hi = min(len(parts), index + 3)
            return "\n\n".join(parts[lo:hi])
    index = original.index(old)
    return original[max(0, index - 800): min(len(original), index + len(old) + 800)]


def one(chapter: int, patch_index: int, patch: dict, polish_wall: float, state_wall: float) -> dict:
    directory = OUT / f"chapter-{chapter:04d}" / f"patch-{patch_index:02d}"
    directory.mkdir(parents=True, exist_ok=True)
    original = (BOOK / "chapters" / f"chapter-{chapter:04d}.md").read_text(encoding="utf-8").strip()
    old = patch["old"]
    new = patch["new"]
    prompt = (
        GATE_TEMPLATE
        + "\n\n# FROZEN MISSION / HUMAN / POWER AUTHORITY\n\n"
        + authority_block(chapter)
        + "\n\n# LOCAL ORIGINAL CONTEXT\n\n"
        + local_context(original, old)
        + "\n\n# PROPOSED PATCH\n\n## OLD\n"
        + old
        + "\n\n## NEW\n"
        + (new or "（删除）")
    )
    prompt_path = directory / "gate_prompt.md"
    output_path = directory / "gate_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "gate_response.md").write_text(response + "\n", encoding="utf-8")
    match = re.search(r"(?m)^DECISION:\s*(ACCEPT|REJECT)\s*$", response)
    decision = match.group(1) if match else "INVALID"
    gate_wall = float(data.get("wall_seconds") or 0)
    sequential_polish_gate = polish_wall + gate_wall
    return {
        "chapter": chapter,
        "patch_index": patch_index,
        "decision": decision,
        "polish_wall_seconds": polish_wall,
        "gate_wall_seconds": gate_wall,
        "state_wall_seconds": state_wall,
        "polish_gate_seconds": round(sequential_polish_gate, 3),
        "added_wall_over_state_seconds": round(max(0.0, sequential_polish_gate - state_wall), 3),
        "old": old,
        "new": new,
        "response": response,
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = json.loads((POLISH / "summary.json").read_text(encoding="utf-8"))
    jobs = []
    for row in rows:
        for index, patch in enumerate(row.get("patches", []), 1):
            jobs.append((row["chapter"], index, patch, float(row["polish_wall_seconds"]), float(row["state_wall_seconds"])))
    results = []
    with ThreadPoolExecutor(max_workers=min(10, len(jobs))) as executor:
        futures = [executor.submit(one, *job) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            results.append(row)
            print(json.dumps({"chapter": row["chapter"], "decision": row["decision"], "gate_wall_seconds": row["gate_wall_seconds"]}, ensure_ascii=False), flush=True)
    results.sort(key=lambda item: (item["chapter"], item["patch_index"]))
    (OUT / "summary.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
