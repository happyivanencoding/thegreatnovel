from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-commercial-spark"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (3, 10, 19)

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.scene_skills import render_selected_revision_watches  # noqa: E402

SPARK_TEMPLATE = """你是 TGN 的 Parallel Commercial Spark，使用 Luna high，与 Context Curator 并行。你看见 Frozen Mission 与已批准 World / Power / Human / Canon，但看不到 Curator 输出和 Primary Draft。

目标不是重新规划，也不是增加情节，而是在完全不改变本章事件、行动者、对象、结果、状态变化、Ending、资源/持有关系、力量位置和未知边界的前提下，提出少量能让本章更接近顶级中文男频的 realization 机会。

只允许从输入中已经明确存在的欲望、关系、能力、奖励、公开见证、选择与代价中选择。严禁新增：人物/围观者、数字、价格、制度、地点设施、能力机制、旧史、奖励、身体接触、胜负、升级、支付方式、未来事件。

严格输出，全部可以写 NONE，总长不超过 1000 中文字符：
# HUMAN DESIRE CUE
1条：当前场景自然触发时，主角最具体的贪、胜负、虚荣、审美、钱、享受、偏心、舍不得或人生牵引如何通过一个动作/注意/短句露出来。不得改变选择。
# FANTASY / PAYOFF REALIZATION
1条：已有力量、获得或胜负怎样用一个可见结果、占有感或旧标尺对照更有分量。不得新增事实或升级。
# RELATIONSHIP / SOCIAL REPRICING
1条：当前已在场人物怎样用一个动作、改口、报价、退让、敌意或关系反应承认结果。只有 Authority 已支持在场与反应时才写。
# SURPRISE / CONTRAST
0—1条：利用已批准事实产生一个非同义解释的反差、人物口吻或结果后的意外感；不能新增情节。
# COMPRESS TO MAKE ROOM
1条：若正文出现，最应压缩的重复证明、流程、协调或后台说明是什么；不得要求删掉人物、Payoff或必要因果。

不要写正文句子成品，不输出评分、Audit、思考或通用写作口号。"""

PRIMARY_SUPPLEMENT = """# Parallel Commercial Spark｜Optional Realization, Not Authority

以下 Spark 由独立 Luna-high 在看不到 Draft 的情况下，从同一 Frozen Authority 中提出。它不是事实来源、不是额外 Mission，也不是逐条配额。

只在自然且完全兼容 Mission / Canon / Curator 时选用 0—2 项；优先保留人物欲望、核心幻想、关系重新定价和结果后的具体重量。不得为了采用 Spark 新增人物、数字、制度、动作、奖励、能力机制、身体接触或未来事件。若 Curator / Authority 已经让场景足够，全部不用。"""

REVISER_SUPPLEMENT = """# Commercial Spark Preservation Note

下方 Spark 不是 Authority。Primary 已采用且 Frozen Authority 支持的 Human / Fantasy / Relationship / Payoff realization，修事实时按 Value-Preserving Relocation 保留；Primary 未采用时，不要求为了完成清单强补。任何新增事实、数字、人物、机制、奖励或剧情一律拒绝。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def call(prompt_path: Path, output_path: Path, model: str) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), model, "high", str(ROOT)],
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


def h2_block(text: str, prefix: str) -> str:
    starts = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(starts):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        return text[match.end():end].strip()
    return ""


def spark_context(chapter: int) -> str:
    curator_prompt = (SOURCE / f"chapter-{chapter:04d}" / "curator_prompt.md").read_text(encoding="utf-8")
    reviser_prompt = (SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    blocks = []
    for label, prefix in (
        ("FROZEN MISSION", "当前章事件合同"),
        ("READER RELEASE", "READER RELEASE——"),
        ("WORLD FACTS", "WORLD AUTHORITY——"),
        ("HUMAN CORE", "FROZEN HUMAN CORE——"),
        ("BOOK FOCUS", "BOOK CONTRACT——"),
        ("CANON", "CANON INDEX——"),
        ("PLAN", "当前大型剧情块与十章计划"),
        ("PREVIOUS TAIL", "前文章末局部衔接片段"),
    ):
        value = h2_block(curator_prompt, prefix)
        if value:
            blocks.append(f"## {label}\n\n{value}")
    power = h2_block(reviser_prompt, "POWER CORE")
    if power:
        blocks.append(f"## POWER CORE\n\n{power}")
    return "\n\n".join(blocks)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)

    spark_prompt = SPARK_TEMPLATE + "\n\n# FROZEN INPUT\n\n" + spark_context(chapter)
    spark_prompt_path = directory / "spark_prompt.md"
    spark_output_path = directory / "spark_acp.json"
    spark_prompt_path.write_text(spark_prompt, encoding="utf-8")
    spark_data = call(spark_prompt_path, spark_output_path, "gpt-5.6-luna")
    spark = clean(spark_data.get("text", ""))
    (directory / "spark.md").write_text(spark + "\n", encoding="utf-8")

    primary_prompt = (source / "primary_prompt.md").read_text(encoding="utf-8")
    primary_prompt += "\n\n" + PRIMARY_SUPPLEMENT + "\n\n# SPARK OPTIONS\n\n" + spark + "\n"
    primary_prompt_path = directory / "primary_prompt.md"
    primary_output_path = directory / "primary_acp.json"
    primary_prompt_path.write_text(primary_prompt, encoding="utf-8")
    primary_data = call(primary_prompt_path, primary_output_path, "gpt-5.6-terra")
    primary_text = clean(primary_data.get("text", ""))
    primary_body = body(primary_text)
    (directory / "primary_response.md").write_text(primary_text + "\n", encoding="utf-8")
    (directory / "primary_body.md").write_text(primary_body + "\n", encoding="utf-8")

    old_primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    reviser_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    reviser_prompt = replace_once(reviser_prompt, old_primary, primary_body, f"ch{chapter} primary")
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    reviser_prompt = replace_once(
        reviser_prompt,
        marker,
        REVISER_SUPPLEMENT + "\n\n# SPARK OPTIONS\n\n" + spark + "\n\n" + marker,
        f"ch{chapter} reviser marker",
    )
    reviser_prompt_path = directory / "reviser_prompt.md"
    reviser_output_path = directory / "reviser_acp.json"
    reviser_prompt_path.write_text(reviser_prompt, encoding="utf-8")
    reviser_data = call(reviser_prompt_path, reviser_output_path, "gpt-5.6-luna")
    reviser_text = clean(reviser_data.get("text", ""))
    final_body = body(reviser_text)
    (directory / "reviser_response.md").write_text(reviser_text + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    control = {
        stage: json.loads((source / f"{stage}_acp.json").read_text(encoding="utf-8"))
        for stage in ("curator", "primary", "authority_reviser")
    }
    spark_wall = float(spark_data.get("wall_seconds") or 0)
    curator_wall = float(control["curator"].get("wall_seconds") or 0)
    primary_wall = float(primary_data.get("wall_seconds") or 0)
    reviser_wall = float(reviser_data.get("wall_seconds") or 0)
    control_total = sum(float(control[stage].get("wall_seconds") or 0) for stage in control)
    treatment_total = max(curator_wall, spark_wall) + primary_wall + reviser_wall
    return {
        "chapter": chapter,
        "control_curator_seconds": curator_wall,
        "spark_seconds": spark_wall,
        "primary_seconds": primary_wall,
        "reviser_seconds": reviser_wall,
        "control_c_p_r_seconds": round(control_total, 3),
        "treatment_parallel_c_spark_p_r_seconds": round(treatment_total, 3),
        "speedup_percent": round((1 - treatment_total / control_total) * 100, 2),
        "spark_hidden_by_curator": spark_wall <= curator_wall,
        "spark_chars": len(spark),
        "primary_chars": len(primary_body),
        "final_chars": len(final_body),
        "spark_usage": spark_data.get("result", {}).get("usage", {}),
        "primary_usage": primary_data.get("result", {}).get("usage", {}),
        "reviser_usage": reviser_data.get("result", {}).get("usage", {}),
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
