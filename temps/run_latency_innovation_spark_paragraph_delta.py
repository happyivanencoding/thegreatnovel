from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
INNOVATION = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1"
SPARK = INNOVATION / "parallel-commercial-spark"
OUT = INNOVATION / "spark-paragraph-delta"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (3, 10, 19)

spec = importlib.util.spec_from_file_location(
    "paragraph_delta_base", ROOT / "temps" / "run_latency_innovation_paragraph_delta_reviser.py"
)
base = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base)

SPARK_SUPPLEMENT = """# COMMERCIAL VALUE WATCH｜Optional, Not Authority

下方 Spark 由独立 Luna-high 在看不到 Primary Draft 时，从同一 Frozen Authority 中编译。它不是新事实、不是额外 Mission、不是逐条配额。

Paragraph-Delta Reviser 仍以 Frozen Mission / Canon / World / Power / Human / Reader Release 为最高边界。只有在 Primary 已经出现对应人物、欲望、力量、奖励、关系与结果，而且 Spark 能用最小局部改动恢复或保护商业价值时，才允许采用 0—2 项：
- 主角具体欲望、占有感、胜负心或人生牵引；
- Core Fantasy / Reward / Public Proof 已经成立后的可见重量；
- 当前在场人物对结果的差异化反应或重新定价；
- 一个不新增事件的反差、人物口吻或结果后惊喜；
- 为上述价值腾空间而压缩重复证明或程序化实施。

严禁为了 Spark 新增人物、围观者、数字、价格、制度、地点、能力机制、身体接触、奖励、胜负、升级、支付方式、旧史或未来事件。Spark 与 Frozen Authority 冲突时完全忽略。不要因为 Spark 存在就扩大修改范围；Primary 已经写好时继续 KEEP。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "high", str(ROOT)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=900,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout after 900s: {prompt_path}"
            time.sleep(2 + attempt * 2)
            continue
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
    spark_dir = SPARK / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)

    full_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    primary = base.body((source / "primary_response.md").read_text(encoding="utf-8"))
    runtime_start = full_prompt.index("# Hybrid Runtime")
    draft_marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    draft_start = full_prompt.index(draft_marker, runtime_start)
    authority_context = full_prompt[runtime_start:draft_start].strip()
    spark = (spark_dir / "spark.md").read_text(encoding="utf-8").strip()
    prompt = (
        base.DELTA_TEMPLATE
        + "\n\n"
        + SPARK_SUPPLEMENT
        + "\n\n# SPARK OPTIONS\n\n"
        + spark
        + "\n\n"
        + authority_context
        + "\n\n# NUMBERED PRIMARY DRAFT\n\n"
        + base.numbered(primary)
    )
    prompt_path = directory / "spark_paragraph_delta_prompt.md"
    output_path = directory / "spark_paragraph_delta_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "spark_paragraph_delta_response.md").write_text(response + "\n", encoding="utf-8")
    final, operations = base.apply_ops(response, primary)
    (directory / "final_body.md").write_text(final + "\n", encoding="utf-8")

    curator_data = json.loads((source / "curator_acp.json").read_text(encoding="utf-8"))
    primary_data = json.loads((source / "primary_acp.json").read_text(encoding="utf-8"))
    reviser_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    spark_data = json.loads((spark_dir / "spark_acp.json").read_text(encoding="utf-8"))
    curator_wall = float(curator_data.get("wall_seconds") or 0)
    primary_wall = float(primary_data.get("wall_seconds") or 0)
    reviser_wall = float(reviser_data.get("wall_seconds") or 0)
    spark_wall = float(spark_data.get("wall_seconds") or 0)
    delta_wall = float(data.get("wall_seconds") or 0)
    control = curator_wall + primary_wall + reviser_wall
    treatment = max(curator_wall, spark_wall) + primary_wall + delta_wall
    return {
        "chapter": chapter,
        "curator_wall_seconds": curator_wall,
        "spark_wall_seconds": spark_wall,
        "primary_wall_seconds": primary_wall,
        "delta_wall_seconds": delta_wall,
        "control_c_p_full_reviser_seconds": round(control, 3),
        "treatment_parallel_c_spark_p_delta_seconds": round(treatment, 3),
        "critical_path_speedup_percent": round((1 - treatment / control) * 100, 2),
        "operation_count": len(operations),
        "operations": operations,
        "response_chars": len(response),
        "final_chars": len(final),
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
