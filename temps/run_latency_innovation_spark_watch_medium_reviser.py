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
SPARK = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-commercial-spark"
WATCH = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-authority-watch"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "spark-watch-medium-reviser"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (3, 10, 19)

SUPPLEMENT = """# Parallel Authority Watch + Commercial Spark Finalization

PRE-DRAFT AUTHORITY WATCHLIST 来自独立 Luna-high、看不到 Draft，只负责覆盖稀疏但昂贵的 Mission / Canon / Reader Release / Power / Human / Ending / ownership / time 风险；COMMERCIAL SPARK 只负责可选人物欲望、幻想、关系和 Payoff realization，不是 Authority。

本轮仍是完整 Preservation-First Authority Revision：
- Frozen Authority > Watchlist > Spark；Watchlist/Spark 冲突或新增事实时拒绝；
- MUST LAND / GLOBAL CLOSURE 逐条核对，尤其不能把结果降成资格、依据、准备、以后到账或即将出发；
- Spark 已被 Primary 自然采用、且 Frozen Authority 支持的 Human/Fantasy/Relationship/Payoff 价值，修事实时按 Value-Preserving Relocation 保留；未采用时不强补；
- Primary 已正确的场景、动作、人物声音和具体收益尽量逐字保留；不要为了 medium effort 压缩成摘要、报告或泛化数字；
- 最终仍只输出 `# 正式正文` 与完整最终正文。"""


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


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    original_primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    spark_primary = (SPARK / f"chapter-{chapter:04d}" / "primary_body.md").read_text(encoding="utf-8").strip()
    spark = (SPARK / f"chapter-{chapter:04d}" / "spark.md").read_text(encoding="utf-8").strip()
    watchlist = (WATCH / f"chapter-{chapter:04d}" / "watchlist.md").read_text(encoding="utf-8").strip()

    prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    prompt = replace_once(prompt, original_primary, spark_primary, f"ch{chapter} primary")
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    addition = (
        SUPPLEMENT
        + "\n\n# PRE-DRAFT AUTHORITY WATCHLIST\n\n"
        + watchlist
        + "\n\n# COMMERCIAL SPARK OPTIONS\n\n"
        + spark
        + "\n\n"
        + marker
    )
    prompt = replace_once(prompt, marker, addition, f"ch{chapter} marker")
    prompt_path = directory / "reviser_prompt.md"
    output_path = directory / "reviser_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    final_body = body(response)
    (directory / "reviser_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    control = {
        stage: json.loads((source / f"{stage}_acp.json").read_text(encoding="utf-8"))
        for stage in ("curator", "primary", "authority_reviser")
    }
    spark_data = json.loads((SPARK / f"chapter-{chapter:04d}" / "spark_acp.json").read_text(encoding="utf-8"))
    spark_primary_data = json.loads((SPARK / f"chapter-{chapter:04d}" / "primary_acp.json").read_text(encoding="utf-8"))
    watch_data = json.loads((WATCH / f"chapter-{chapter:04d}" / "watch_planner_acp.json").read_text(encoding="utf-8"))
    curator_wall = float(control["curator"].get("wall_seconds") or 0)
    spark_wall = float(spark_data.get("wall_seconds") or 0)
    primary_wall = float(spark_primary_data.get("wall_seconds") or 0)
    watch_wall = float(watch_data.get("wall_seconds") or 0)
    medium_wall = float(data.get("wall_seconds") or 0)
    control_total = sum(float(control[stage].get("wall_seconds") or 0) for stage in control)
    treatment_total = max(curator_wall, spark_wall) + max(primary_wall, watch_wall) + medium_wall
    return {
        "chapter": chapter,
        "control_c_p_r_seconds": round(control_total, 3),
        "curator_or_spark_seconds": round(max(curator_wall, spark_wall), 3),
        "primary_or_watch_seconds": round(max(primary_wall, watch_wall), 3),
        "medium_reviser_seconds": medium_wall,
        "treatment_critical_seconds": round(treatment_total, 3),
        "speedup_percent": round((1 - treatment_total / control_total) * 100, 2),
        "spark_hidden_by_curator": spark_wall <= curator_wall,
        "watch_hidden_by_primary": watch_wall <= primary_wall,
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
