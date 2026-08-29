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
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "authority-blueprint-primary"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

FINAL_WRITER_CONTRACT = """# Final-Draft Authority Blueprint Contract

本次 Terra Writer 的输出将直接作为候选最终正文，不再假设后面有 Reviser 替你补结果。下方 `PRE-DRAFT AUTHORITY WATCHLIST` 是独立 Luna-high 在未见 Draft 时根据 Frozen Authority 编译的语义保险，不是正文措辞来源，也不是让章节变短的摘要。

- `MUST LAND` 必须通过完整场景真实完成，尤其是行动者、对象、直接结果、状态变化与 Ending；不得降成准备、依据、资格、以后结算或“即将”。
- `MUST NOT INVENT / GLOBAL CLOSURE` 是事实边界；全文所有相关位置必须一致。
- `REALIZATION PRIORITIES / PRESERVE VALUE` 是本章的商业价值下限：主角主动性、人物欲望、关系、核心幻想、具体占有/收益、Public Proof、社会重新定价与章末动作不能因为守 Authority 而被写薄。它们应该通过动作、对白、具体反应和结果成为场景，而不是逐条解释 Watchlist。
- `COMPRESS ONLY IF PRESENT` 只处理真实出现的流程膨胀，不授权压掉故事、人物或 payoff。
- 维持当前 BOOK prose profile 与 Curator attention；正文长度、场景完整度和人物密度按这本书需要，不因 Watchlist 较短就缩成摘要。

输出仍严格服从原 Primary Writer 合同，只输出 `# 正式正文` 与完整小说正文。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-terra", "high", str(ROOT)],
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
    prompt = (source / "primary_prompt.md").read_text(encoding="utf-8")
    watchlist = (WATCH / f"chapter-{chapter:04d}" / "watchlist.md").read_text(encoding="utf-8").strip()
    marker = "## CANON PROSE——上一章全文与上上章必要章末"
    if marker not in prompt:
        raise RuntimeError(f"ch{chapter}: primary prompt marker missing")
    injection = (
        FINAL_WRITER_CONTRACT
        + "\n\n# PRE-DRAFT AUTHORITY WATCHLIST\n\n"
        + watchlist
        + "\n\n"
        + marker
    )
    prompt = prompt.replace(marker, injection, 1)
    prompt_path = directory / "authority_blueprint_primary_prompt.md"
    output_path = directory / "authority_blueprint_primary_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    final_body = body(response)
    (directory / "authority_blueprint_primary_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    primary_data = json.loads((source / "primary_acp.json").read_text(encoding="utf-8"))
    reviser_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    planner_data = json.loads((WATCH / f"chapter-{chapter:04d}" / "watch_planner_acp.json").read_text(encoding="utf-8"))
    planner_wall = float(planner_data.get("wall_seconds") or 0)
    writer_wall = float(data.get("wall_seconds") or 0)
    control_wall = float(primary_data.get("wall_seconds") or 0) + float(reviser_data.get("wall_seconds") or 0)
    treatment_serial = planner_wall + writer_wall
    return {
        "chapter": chapter,
        "planner_wall_seconds": planner_wall,
        "writer_wall_seconds": writer_wall,
        "control_primary_plus_reviser_seconds": round(control_wall, 3),
        "treatment_planner_plus_writer_seconds": round(treatment_serial, 3),
        "speedup_percent": round((1 - treatment_serial / control_wall) * 100, 2),
        "prompt_chars": len(prompt),
        "watchlist_chars": len(watchlist),
        "final_chars": len(final_body),
        "writer_usage": data.get("result", {}).get("usage", {}),
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
