from __future__ import annotations

import json
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
TREATMENT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "combined-reviser-state"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "blind-combined-reviser-state"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.prompts import parse_state_delta_v2  # noqa: E402


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def h2_block(text: str, prefix: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(headings):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[match.end():end].strip()
    return ""


def call(prompt: Path, output: Path, model: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                ["node", str(RUNNER), str(prompt), str(output), model, "high", str(ROOT)],
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
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def prepare() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    key = {}
    parser_rows = []
    for chapter in CHAPTERS:
        source = SOURCE / f"chapter-{chapter:04d}"
        treatment_dir = TREATMENT / f"chapter-{chapter:04d}"
        directory = OUT / f"chapter-{chapter:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        control_body = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
        treatment_body = (treatment_dir / "final_body.md").read_text(encoding="utf-8").strip()
        control_state = (source / "state_response.md").read_text(encoding="utf-8").strip()
        treatment_state = (treatment_dir / "state_delta.md").read_text(encoding="utf-8").strip()
        # Deterministic schema validation before any subjective judging.
        parsed_control = parse_state_delta_v2(control_state)
        parsed_treatment = parse_state_delta_v2(treatment_state)
        parser_rows.append({
            "chapter": chapter,
            "control_fields": {key: len(value) for key, value in parsed_control.items()},
            "treatment_fields": {key: len(value) for key, value in parsed_treatment.items()},
        })
        order = ["control", "combined"]
        random.Random(20260829720 + chapter).shuffle(order)
        bodies = {"control": control_body, "combined": treatment_body}
        states = {"control": control_state, "combined": treatment_state}
        key[str(chapter)] = {"A": order[0], "B": order[1]}
        authority_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
        blocks = []
        for label, prefix in (
            ("FROZEN MISSION", "FROZEN CHAPTER MISSION"),
            ("WORLD AUTHORITY", "WORLD REALITY AUTHORITY"),
            ("READER RELEASE", "READER RELEASE"),
            ("POWER CORE", "POWER CORE"),
            ("HUMAN CORE", "HUMAN CORE"),
            ("CANON INDEX", "CANON INDEX"),
            ("CANON TAIL", "CANON TAIL"),
        ):
            value = h2_block(authority_prompt, prefix)
            if value:
                blocks.append(f"## {label}\n{value}")
        authority = "\n\n".join(blocks)
        state_prompt = (source / "state_prompt.md").read_text(encoding="utf-8")
        current_canon = state_prompt.split("## 本次新正式章节正文", 1)[0]

        reader_prompt = f"""你是匿名盲读的成熟中文男频长篇审稿人。两版来自同一冻结章节链；一版的 Reviser 只写正文，另一版在同一次调用末尾额外做 State Extraction。你不知道来源，只比较正式正文。

目标：清楚、推进快、主角主动且欲望具体、人物关系有张力、力量/奖励/身份/损失落地、高潮有重量，同时少流程、少后台抽象、少重复证明、少 AI 味。事实硬错也属于严重阅读问题。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
READABILITY_AND_PACE: A / B / TIE
PROTAGONIST_AGENCY: A / B / TIE
CHARACTER_RELATIONSHIP: A / B / TIE
POWER_PAYOFF_REWARD: A / B / TIE
ANTI_PROCEDURE_AI_FLAVOR: A / B / TIE
CONTINUATION_PULL: A / B / TIE
HARD_PROBLEM_A: 无 或一句
HARD_PROBLEM_B: 无 或一句
REASON: 8—14句，引用具体事件证据，不长引原文。

# OPTION A
{bodies[order[0]]}

# OPTION B
{bodies[order[1]]}
"""
        authority_judge = f"""你是匿名 TGN Authority / Canon 盲审员。两版正文共享同一 Frozen Mission、Canon、World / Power / Human Authority、Reader Release 与 Ending。你不知道哪版同时承担了 State Extraction。

检查行动者/对象、事件顺序、胜负、资源与持有关系、伤势、身份/力量位置、知识边界、Reader Release、Direct Result、State Change、Ending，以及主角欲望、关系、Public Proof、收益和反程序化质量。Hard violation 不能凭文笔抵消。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
MISSION_FIDELITY: A / B / TIE
CANON_WORLD_POWER_HUMAN: A / B / TIE
RESULT_STATE_ENDING: A / B / TIE
PAYOFF_AND_RELATIONSHIP: A / B / TIE
STORY_VALUE: A / B / TIE
REASON: 8—14句，引用具体事件层证据。

# FROZEN AUTHORITY
{authority}

# OPTION A
{bodies[order[0]]}

# OPTION B
{bodies[order[1]]}
"""
        state_judge = f"""你是匿名的 TGN State Delta 事实审计员。Option A 与 B 各自包含一份最终正文和由它提取的 State Delta。两套都从同一旧 Canon 开始。不要比较正文文风；只比较各自 State 是否忠实、完整、不过度推断地记录自己的正文。

检查：Active Scene State 是否足够下一章连续；Persistent Canon 是否保留仍有效事实且只新增正文已发生内容；力量位置不从战绩反推；人物关系、身份、知识、World State、Tracked Assets 的状态/持有人/转移正确；Summary 只写已发生事实；Open Promises 删除已兑现项、不制造未来事实，且有界。任何未授权数字、机制、支付方式、旧史、人物到场或未来结果都是 hard violation。

严格输出：
VERDICT: A / B / MIXED
CONFIDENCE: high / medium / low
HARD_VIOLATIONS_A: 无 或逐条短写
HARD_VIOLATIONS_B: 无 或逐条短写
ACTIVE_SCENE_CONTINUITY: A / B / TIE
PERSISTENT_CANON_FIDELITY: A / B / TIE
ASSET_POWER_RELATION_STATE: A / B / TIE
SUMMARY_ACCURACY: A / B / TIE
PROMISE_WINDOW: A / B / TIE
REASON: 8—14句，必须对照各自正文。

# OLD CANON / STATE INPUT
{current_canon}

# OPTION A FINAL BODY
{bodies[order[0]]}

# OPTION A STATE DELTA
{states[order[0]]}

# OPTION B FINAL BODY
{bodies[order[1]]}

# OPTION B STATE DELTA
{states[order[1]]}
"""
        (directory / "reader_prompt.md").write_text(reader_prompt, encoding="utf-8")
        (directory / "authority_prompt.md").write_text(authority_judge, encoding="utf-8")
        (directory / "state_prompt.md").write_text(state_judge, encoding="utf-8")
    (OUT / "blind_key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "parser_validation.json").write_text(json.dumps(parser_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return key


def one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    reader_data = call(directory / "reader_prompt.md", directory / "reader_terra_acp.json", "gpt-5.6-terra")
    reader = clean(reader_data.get("text", ""))
    (directory / "reader_terra.md").write_text(reader + "\n", encoding="utf-8")
    authority_data = call(directory / "authority_prompt.md", directory / "authority_luna_acp.json", "gpt-5.6-luna")
    authority = clean(authority_data.get("text", ""))
    (directory / "authority_luna.md").write_text(authority + "\n", encoding="utf-8")
    state_data = call(directory / "state_prompt.md", directory / "state_luna_acp.json", "gpt-5.6-luna")
    state = clean(state_data.get("text", ""))
    (directory / "state_luna.md").write_text(state + "\n", encoding="utf-8")
    return {
        "chapter": chapter,
        "reader": reader,
        "authority": authority,
        "state": state,
    }


def main() -> None:
    prepare()
    rows = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps({"chapter": row["chapter"], "reader": row["reader"].splitlines()[:2], "authority": row["authority"].splitlines()[:2], "state": row["state"].splitlines()[:2]}, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
