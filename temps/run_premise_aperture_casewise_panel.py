from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import re
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-premise-aperture-20260829-v1"
sys.path.insert(0, str(ROOT / "temps"))

from run_premise_aperture_panel import (  # noqa: E402
    CASES,
    ROLE_PROMPTS,
    read,
    run_one,
)


CASEWISE_JUDGE = """你只会看到一个题材、七张匿名且同格式的中文男频长篇前提卡。来源未知。

评价原则：
- 不奖励篇幅、术语数量、血腥、生理猎奇或“设定很多”。
- Boldness 是一个高风险押注能一句话让人看见，并永久改变主角动作、欲望或社会位置。
- 高分方案应迅速回答：为什么想点开；主角反复做什么；第一次如何不公平兑现；别人为何重新估价他。
- 惩罚四个同等 gimmick 抢主轴、世界与外挂钥匙锁孔式预配、只换名词、长解释、百章后只剩同一招放大。
- 非人主角不自动加分或减分；关键是可读、可欲、可持续。
- 只能评价当前这一组，不得引用或想象其它题材候选。

每个方案给以下 0—10 分：Click、Bold、Clear、Changed Verbs、Immediate Payoff、Social Repricing、Long-form Runway、Coherence Without Overfit、Risk（0最好，10最危险），再给 Overall 0—100。

严格输出，不要前言：
# CASEWISE BLIND PANEL
## CASE｜题材名
### Score Table
| 方案 | Click | Bold | Clear | Verbs | Payoff | Social | Long | Indep | Risk | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
（A—G 七行全部输出）
### Top 3
1. 方案X：最强理由；最大风险。
2. ...
3. ...
### Decision
- 最愿意直接试写前三章：方案X，因为……
- 最有野心但目前过载：方案Y，因为……
- 最安全却最可能被忘记：方案Z，因为……
"""


def validate_report(text: str, *, case_display: str) -> None:
    if case_display not in text:
        raise RuntimeError(f"casewise judge missing case title: {case_display}")
    table_labels = set(re.findall(r"(?m)^\|\s*(?:方案\s*)?([A-G])\s*\|", text))
    if table_labels != set("ABCDEFG"):
        raise RuntimeError(f"casewise judge missing table labels: {case_display} {sorted(table_labels)}")


def main() -> None:
    source = EXP / "blind_panel"
    out = EXP / "blind_panel_casewise"
    out.mkdir(exist_ok=True)
    invalid_note = """# Supersession Note

The earlier batched panel is retained for audit history but is not used as final evidence: the commercial judge's `fast_multiworld` explanation copied concepts from the following `game_instance` case. Cold-reader and long-form reports appeared case-consistent, but all roles are rerun case-by-case so the final comparison has one case per context.
"""
    (out / "BATCH_PANEL_SUPERSESSION.md").write_text(invalid_note, encoding="utf-8")

    models = {
        "commercial": "gpt-5.6-luna",
        "cold_reader": "gpt-5.6-terra",
        "longform": "gpt-5.6-sol",
    }
    jobs: list[tuple[Path, Path, Path, str, str, str]] = []
    for case in CASES:
        blind = read(source / case.case_id / "BLIND_CARDS.md")
        for role, model in models.items():
            d = out / case.case_id / role
            d.mkdir(parents=True, exist_ok=True)
            prompt = "\n\n".join(
                (ROLE_PROMPTS[role].strip(), CASEWISE_JUDGE.strip(), blind)
            ) + "\n"
            prompt_path = d / "PROMPT.md"
            prompt_path.write_text(prompt, encoding="utf-8")
            jobs.append(
                (
                    prompt_path,
                    d / "ACP.json",
                    d / "REPORT.md",
                    f"premise-casewise-{case.case_id}-{role}",
                    model,
                    case.display,
                )
            )

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=9) as pool:
        futures = {
            pool.submit(run_one, p, o, r, label=label, model=model): (r, display)
            for p, o, r, label, model, display in jobs
        }
        for future in as_completed(futures):
            response_path, display = futures[future]
            result = future.result()
            validate_report(read(response_path), case_display=display)
            results.append(result)
            print("DONE", result, flush=True)

    mappings = json.loads(read(source / "ANON_MAPPING.json"))
    report_blocks: list[str] = []
    for case in CASES:
        for role in models:
            report_blocks.extend(
                (
                    f"# REPORT｜{case.case_id}｜{role}",
                    read(out / case.case_id / role / "REPORT.md"),
                )
            )
    synthesis_prompt = f"""你是实验统计与架构审计员。下方是九份真正 case-wise 的独立盲评与匿名映射。此前 batched panel 因一份商业解释串组而作废，不得引用其分数。

来源：B0=current production；S1-S3=Single-Agent Premise Forge；C1-C3=four-axis fixed collision。

逐题材、逐来源解盲。必须区分：
- B0 单一现有方案；
- S pool ceiling/floor/均值；
- C pool ceiling/floor/均值；
- 预注册 S2 vs C2；
- 三位评审的共识与真实分歧。

只能根据九份表内分数做算术汇总。请明确列出每个来源候选的三位 Overall 分数和平均值（保留一位小数），再下判断。不要因候选池有三个就只报最好一个。

严格格式：
# CASEWISE PANEL SYNTHESIS
## Data Integrity
## Per-Case Score Tables
### 通用玄幻成长
### 20章一世界快节奏长篇
### 游戏副本／无限流
## Generator Ceiling / Floor / Stability
## Pre-registered S2 vs C2
## Cross-Reviewer Consensus and Disagreement
## Evidence-Bounded Freeze Implications

# ANON MAPPING
{json.dumps(mappings, ensure_ascii=False, indent=2)}

{chr(10).join(report_blocks)}
"""
    synth = out / "synthesis"
    synth.mkdir(exist_ok=True)
    (synth / "PROMPT.md").write_text(synthesis_prompt, encoding="utf-8")
    result = run_one(
        synth / "PROMPT.md",
        synth / "ACP.json",
        synth / "REPORT.md",
        label="premise-casewise-synthesis",
        model="gpt-5.6-luna",
    )
    results.append(result)
    (out / "RUN_SUMMARY.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
