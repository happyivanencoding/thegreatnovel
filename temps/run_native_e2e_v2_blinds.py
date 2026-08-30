from __future__ import annotations

import argparse
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

WORKTREE = Path(r"C:\dev\tgn-story-mvp-native-e2e")
BASE = WORKTREE / "books" / "real-exp-native-structured-e2e-20260830-v1"
sys.path.insert(0, str(WORKTREE / "temps"))

from run_native_structured_e2e import body, call_acp, clean_model_text, parse_mission_fields, source_directory  # noqa: E402

RUNS = ("e2e-run4", "e2e-run5", "control-chain-1", "control-chain-2")
SAMPLES = ("jiuchui_ch14", "jiuchui_ch16", "shadow_ch4", "shadow_ch9")
JUDGES = {"story": ("gpt-5.6-terra", "high"), "authority": ("gpt-5.6-luna", "high")}
LABELS = ("A", "B", "C", "D")
MISSION_LABELS = (
    "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
    "直接结果", "状态变化", "叙事功能", "结尾推动力",
)

STORY_MISSION = """你是成熟中文男频长篇的匿名 Story Director 审稿人。

下面四个候选来自同一章、同一份上游 Story / Outline / Canon，但路线完全匿名。请先读共享上游，再只评“本章故事选择与商业张力”，不要因为结构更整齐、字段更多、解释更完整就自动给高分。

重点：本章最值得看的冲突是否被抓住；主角欲望与主动选择；Reward / Public Proof / Surprise / Relationship；能力玩法；Ending续读；是否任务清单化、程序化、抽象总结化。因果允许时，更爽、更大胆、更有公开反应不是缺点。

严格只输出一个 JSON 对象：
{{"ranking":["A","B","C","D"],"scores":{{"A":0,"B":0,"C":0,"D":0}},"best":"A","worst":"D","reason":"中文6—10句具体比较","hard_problems":{{"A":"","B":"","C":"","D":""}}}}
分数0—10，可有小数。不要输出 Markdown。

# SHARED PRE-DIRECTOR CONTEXT
{AUTHORITY}

{CANDIDATES}
"""

AUTHORITY_MISSION = """你是匿名的 TGN Frozen Authority 审计员。

下面四个 Director Mission 候选来自同一章。根据共享 pre-Director Authority，检查 Plan fidelity、actor/action/object、Direct Result、State Change、Ending、money/ownership/power/relationship、Reader Release、unknown与跨章timing。不要因为结构化或更详细就偏爱它。会污染下一章 Canon 的错误优先。

严格只输出一个 JSON 对象：
{{"ranking":["A","B","C","D"],"scores":{{"A":0,"B":0,"C":0,"D":0}},"best":"A","worst":"D","reason":"中文6—10句具体比较","hard_problems":{{"A":"","B":"","C":"","D":""}}}}
分数0—10，可有小数。不要输出 Markdown。

# SHARED PRE-DIRECTOR AUTHORITY
{AUTHORITY}

{CANDIDATES}
"""

STORY_FINAL = """你是匿名的成熟中文男频商业编辑兼读者。

下面四个候选是同一章、同一上游阶段的最终正文。路线完全匿名，正文已统一清除系统元数据。只评最终读者体验：续读欲、主角欲望和选择、冲突与动作、能力/Reward/Public Proof/Surprise、人物关系、具体后果、节奏、AI总结味、程序/报告味、漂亮二段论。不要因更长或更克制自动偏爱。

严格只输出一个 JSON 对象：
{{"ranking":["A","B","C","D"],"scores":{{"A":0,"B":0,"C":0,"D":0}},"best":"A","worst":"D","reason":"中文6—10句具体比较","hard_problems":{{"A":"","B":"","C":"","D":""}}}}
分数0—10，可有小数。不要输出 Markdown。

{CANDIDATES}
"""

AUTHORITY_FINAL = """你是匿名的 TGN Authority / continuity 审计员。

下面四个候选是同一章的最终正文。根据共享 pre-Director Authority，检查 actor/action/object、Direct Result、State Change、Ending、money/ownership、power boundary、Reader Release、unresolved facts、relationship、Public Proof timing。不要评文笔；会污染下一章 Canon 的事实错误优先。不要因为候选更结构化或更长而偏爱。

严格只输出一个 JSON 对象：
{{"ranking":["A","B","C","D"],"scores":{{"A":0,"B":0,"C":0,"D":0}},"best":"A","worst":"D","reason":"中文6—10句具体比较","hard_problems":{{"A":"","B":"","C":"","D":""}}}}
分数0—10，可有小数。不要输出 Markdown。

# SHARED PRE-DIRECTOR AUTHORITY
{AUTHORITY}

{CANDIDATES}
"""


def mission_core(text: str) -> str:
    text = clean_model_text(text)
    fields = parse_mission_fields(text)
    if len(fields) < 6:
        return text
    return "\n\n".join(f"{label}：{fields[label]}" for label in MISSION_LABELS if label in fields)


def candidate_text(run: str, sample: str, kind: str) -> str:
    if kind == "mission":
        if run.startswith("e2e-"):
            p = BASE / run / sample / "effective_director_mission.md"
        else:
            p = BASE / run / sample / "director_response.md"
        return mission_core(p.read_text(encoding="utf-8"))
    if run.startswith("e2e-"):
        p = BASE / run / sample / "final_body.md"
    else:
        p = BASE / run / sample / "reviser_response.md"
    return body(clean_model_text(p.read_text(encoding="utf-8"))).strip()


def parse_json(text: str) -> dict[str, Any]:
    clean = clean_model_text(text)
    if clean.startswith("```"):
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", clean, re.S)
        if m:
            clean = m.group(1)
    start, end = clean.find("{"), clean.rfind("}")
    if start >= 0 and end > start:
        clean = clean[start:end+1]
    value = json.loads(clean)
    if sorted(value.get("ranking", [])) != list(LABELS):
        raise ValueError(f"invalid ranking={value.get('ranking')}")
    if value.get("best") not in LABELS or value.get("worst") not in LABELS:
        raise ValueError("invalid best/worst")
    return value


def one(sample: str, kind: str, judge: str) -> dict[str, Any]:
    out = BASE / "blinds-v2-pure-body" / sample
    out.mkdir(parents=True, exist_ok=True)
    order = list(RUNS)
    random.Random(f"native-final-clean:{sample}:{kind}:{judge}").shuffle(order)
    key = {label: run for label, run in zip(LABELS, order)}
    texts = {label: candidate_text(run, sample, kind) for label, run in key.items()}
    contamination = {label: "oai-mem-citation" in text for label, text in texts.items()}
    if any(contamination.values()):
        raise ValueError(f"candidate contamination remained: {contamination}")
    candidates = "\n\n".join(f"# CANDIDATE {label}\n\n{texts[label]}" for label in LABELS)
    authority = (source_directory(sample) / "director_prompt.md").read_text(encoding="utf-8")
    template = {
        ("mission", "story"): STORY_MISSION,
        ("mission", "authority"): AUTHORITY_MISSION,
        ("final", "story"): STORY_FINAL,
        ("final", "authority"): AUTHORITY_FINAL,
    }[(kind, judge)]
    prompt = template.format(AUTHORITY=authority, CANDIDATES=candidates)
    stem = f"{kind}_{judge}"
    prompt_path = out / f"{stem}_prompt.md"
    acp_path = out / f"{stem}_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    model, effort = JUDGES[judge]
    data = call_acp(prompt_path, acp_path, model=model, effort=effort)
    raw = str(data.get("text", ""))
    (out / f"{stem}_response.md").write_text(raw.strip() + "\n", encoding="utf-8")
    parsed = parse_json(raw)
    decoded_ranking = [key[label] for label in parsed["ranking"]]
    decoded_scores = {key[label]: float(score) for label, score in parsed["scores"].items()}
    decoded_hard = {key[label]: text for label, text in parsed.get("hard_problems", {}).items()}
    return {
        "sample": sample,
        "kind": kind,
        "judge": judge,
        "blind_key": key,
        "raw": parsed,
        "decoded_ranking": decoded_ranking,
        "decoded_scores": decoded_scores,
        "decoded_best": key[parsed["best"]],
        "decoded_worst": key[parsed["worst"]],
        "decoded_hard_problems": decoded_hard,
        "wall_seconds": float(data.get("wall_seconds") or 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    jobs = [(sample, kind, judge) for sample in SAMPLES for kind in ("mission", "final") for judge in ("story", "authority")]
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(one, *job) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps({k: v for k, v in row.items() if k != "raw"}, ensure_ascii=False), flush=True)
    rows.sort(key=lambda row: (row["sample"], row["kind"], row["judge"]))
    aggregates: dict[str, Any] = {}
    for kind in ("mission", "final"):
        for judge in ("story", "authority"):
            group = [row for row in rows if row["kind"] == kind and row["judge"] == judge]
            score_sums = {run: round(sum(row["decoded_scores"][run] for row in group), 3) for run in RUNS}
            best_counts = {run: sum(row["decoded_best"] == run for row in group) for run in RUNS}
            rank_sums = {run: sum(row["decoded_ranking"].index(run) + 1 for row in group) for run in RUNS}
            aggregates[f"{kind}:{judge}"] = {
                "score_sums": score_sums,
                "score_means": {run: round(score_sums[run] / len(group), 3) for run in RUNS},
                "best_counts": best_counts,
                "mean_rank": {run: round(rank_sums[run] / len(group), 3) for run in RUNS},
            }
    summary = {
        "schema_version": "native-structured-v2-pure-body-blind-v1",
        "runs": list(RUNS),
        "samples": len(SAMPLES),
        "judge_calls": len(rows),
        "candidate_metadata_clean": True,
        "aggregates": aggregates,
        "rows": rows,
    }
    out = BASE / "blinds-v2-pure-body"
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
