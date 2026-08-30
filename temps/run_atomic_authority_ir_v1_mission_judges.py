from __future__ import annotations

import json
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-atomic-authority-ir-20260829-v1"
TREATMENT = BASE / "phase-c-compact-director-sidecar"
OUT = BASE / "phase-e-blind-compact-mission"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

sys.path.insert(0, str(ROOT / "temps"))
from run_atomic_authority_ir_v1_static import sample_specs  # noqa: E402


STORY_TEMPLATE = """你是匿名盲审的成熟中文男频长篇 Story Director 审稿人。A/B 使用同一上游 Story / Outline / Canon；一版是原 Director，一版在同次决策中额外承担机器 IR Sidecar。你不知道来源。

只评八字段事件合同本身。目标：让后续 Curator / Primary 写出更接近顶级男频的当前章——主角主动、欲望与得失具体、行动和对象清楚、结果/状态/Ending真正落地、关系和Public Proof有故事价值，同时不工程化、不把下一章提前结算。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
PROTAGONIST_AGENCY: A / B / TIE
CONFLICT_AND_CHOICE: A / B / TIE
PAYOFF_REWARD_RELATIONSHIP: A / B / TIE
ACTION_OBJECT_CLARITY: A / B / TIE
ANTI_PROCEDURE_AI_FLAVOR: A / B / TIE
CONTINUATION_PULL: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 8—14句，引用具体事件层差异，不按长度评分。

# FROZEN SOURCE CONTEXT
{context}

# OPTION A
{option_a}

# OPTION B
{option_b}
"""


AUTHORITY_TEMPLATE = """你是匿名 TGN Director Contract / Authority 审核员。A/B共享同一上游剧情块、当前章计划、Canon与前文章末；你不知道来源。

检查八字段是否忠实冻结：触发、推动者、主角行动、对手/世界反应、Direct Result、State Change、Narrative Function、Ending。重点检查人物/对象、付款状态、所有权、力量位置、时间终态、Reader Release价值、未来结果偷跑与未批准新事实。一个 hard violation 不能被表达流畅抵消。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
PLAN_FIDELITY: A / B / TIE
CANON_WORLD_POWER: A / B / TIE
ACTOR_ACTION_OBJECT: A / B / TIE
RESULT_STATE_ENDING: A / B / TIE
STORY_VALUE_PRESERVATION: A / B / TIE
REASON: 8—14句，使用具体事实，不评价机器Sidecar格式。

# FROZEN SOURCE CONTEXT
{context}

# OPTION A
{option_a}

# OPTION B
{option_b}
"""


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text
    ).strip()


def call(prompt: Path, output: Path, model: str) -> dict[str, Any]:
    last = ""
    for attempt in range(3):
        try:
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
            last = (process.stderr + "\n" + process.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def prepare() -> dict[str, dict[str, str]]:
    OUT.mkdir(parents=True, exist_ok=True)
    key: dict[str, dict[str, str]] = {}
    for index, spec in enumerate(sample_specs(), 1):
        name = str(spec["name"])
        directory = OUT / name
        directory.mkdir(parents=True, exist_ok=True)
        control = (spec["source_dir"] / "director_response.md").read_text(
            encoding="utf-8"
        ).strip()
        treatment = (
            TREATMENT / name / "director_mission_only.md"
        ).read_text(encoding="utf-8").strip()
        source_prompt = (spec["source_dir"] / "director_prompt.md").read_text(
            encoding="utf-8"
        )
        context = source_prompt.split("# Director Context", 1)[-1].strip()
        candidates = {"control": control, "compact_sidecar": treatment}
        order = ["control", "compact_sidecar"]
        random.Random(202608301100 + index).shuffle(order)
        key[name] = {"A": order[0], "B": order[1]}
        params = {
            "context": context,
            "option_a": candidates[order[0]],
            "option_b": candidates[order[1]],
        }
        (directory / "story_prompt.md").write_text(
            STORY_TEMPLATE.format(**params), encoding="utf-8"
        )
        (directory / "authority_prompt.md").write_text(
            AUTHORITY_TEMPLATE.format(**params), encoding="utf-8"
        )
    (OUT / "blind_key.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return key


def one(spec: Mapping[str, Any]) -> dict[str, Any]:
    name = str(spec["name"])
    directory = OUT / name
    story_data = call(
        directory / "story_prompt.md",
        directory / "story_terra_acp.json",
        "gpt-5.6-terra",
    )
    story = clean(str(story_data.get("text", "")))
    (directory / "story_terra.md").write_text(story + "\n", encoding="utf-8")
    authority_data = call(
        directory / "authority_prompt.md",
        directory / "authority_luna_acp.json",
        "gpt-5.6-luna",
    )
    authority = clean(str(authority_data.get("text", "")))
    (directory / "authority_luna.md").write_text(
        authority + "\n", encoding="utf-8"
    )
    return {
        "sample": name,
        "story": story,
        "story_wall_seconds": story_data.get("wall_seconds"),
        "authority": authority,
        "authority_wall_seconds": authority_data.get("wall_seconds"),
    }


def main() -> None:
    prepare()
    specs = sample_specs()
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=len(specs)) as executor:
        futures = [executor.submit(one, spec) for spec in specs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(
                json.dumps(
                    {
                        "sample": row["sample"],
                        "story": row["story"].splitlines()[:2],
                        "authority": row["authority"].splitlines()[:2],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    rows.sort(key=lambda item: item["sample"])
    (OUT / "summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
