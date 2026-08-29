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
WATCH = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-authority-watch"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-watch-medium-reviser"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

SUPPLEMENT = """# Parallel Authority Watch Supplement

下方 PRE-DRAFT AUTHORITY WATCHLIST 由一个独立 Luna-high Agent 在完全看不到 Primary Draft 时，从本次同一 Frozen Mission / World / Reader Release / Power / Human / Canon Authority 中编译。它只是一份 coverage checklist，不是新 Authority，也不能覆盖本 Prompt 已有的完整 Authority Reviser 合同。

本轮仍执行完整 Preservation-First Authority Revision：
- Watchlist 中 MUST LAND / GLOBAL CLOSURE / PRESERVE VALUE 逐条检查，避免 medium effort 漏掉稀疏但昂贵的结果、Ending、Reader Release、人物 cue、Public Proof 或持有/时间闭合；
- Watchlist 若与下方 Frozen Authority 冲突，以 Frozen Authority 为准；
- Primary 已经正确的段落继续逐字保留，不因为有 Watchlist 就扩写、重写或把章节改成清单；
- 最终输出仍只允许 `# 正式正文` 与完整最终正文。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


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


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    watchlist = (WATCH / f"chapter-{chapter:04d}" / "watchlist.md").read_text(encoding="utf-8").strip()
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    if prompt.count(marker) != 1:
        raise RuntimeError(f"ch{chapter}: primary marker count={prompt.count(marker)}")
    prompt = prompt.replace(
        marker,
        SUPPLEMENT + "\n\n# PRE-DRAFT AUTHORITY WATCHLIST\n\n" + watchlist + "\n\n" + marker,
        1,
    )
    prompt_path = directory / "watch_medium_reviser_prompt.md"
    output_path = directory / "watch_medium_reviser_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    final_body = body(response)
    (directory / "watch_medium_reviser_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    primary_data = json.loads((source / "primary_acp.json").read_text(encoding="utf-8"))
    high_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    planner_data = json.loads((WATCH / f"chapter-{chapter:04d}" / "watch_planner_acp.json").read_text(encoding="utf-8"))
    primary_wall = float(primary_data.get("wall_seconds") or 0)
    high_wall = float(high_data.get("wall_seconds") or 0)
    planner_wall = float(planner_data.get("wall_seconds") or 0)
    medium_wall = float(data.get("wall_seconds") or 0)
    control = primary_wall + high_wall
    treatment = max(primary_wall, planner_wall) + medium_wall
    return {
        "chapter": chapter,
        "primary_wall_seconds": primary_wall,
        "planner_wall_seconds": planner_wall,
        "control_high_reviser_wall_seconds": high_wall,
        "watch_medium_reviser_wall_seconds": medium_wall,
        "control_primary_plus_reviser_seconds": round(control, 3),
        "treatment_parallel_critical_seconds": round(treatment, 3),
        "critical_path_speedup_percent": round((1 - treatment / control) * 100, 2),
        "prompt_chars": len(prompt),
        "watchlist_chars": len(watchlist),
        "final_chars": len(final_body),
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
