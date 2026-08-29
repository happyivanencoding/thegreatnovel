from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import random
import re
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-premise-aperture-20260829-v1"
sys.path.insert(0, str(ROOT / "temps"))

from run_premise_aperture_panel import CASES, ROLE_PROMPTS, read, run_one  # noqa: E402


OLD_IDS = ("B0", "S1", "S2", "S3", "C1", "C2", "C3")
VOLTAGE_IDS = ("V1", "V2", "V3")
ALL_IDS = OLD_IDS + VOLTAGE_IDS
LABELS = tuple("ABCDEFGHIJ")


VOLTAGE_STANDARDIZER = """你是事实压缩员，不是评审或改稿者。把下方 V1/V2/V3 三个两押注候选压成三张与既有前提卡完全同构的卡片。

绝对规则：
- 不评价、不排名、不修补，不替候选增加桥梁。
- 只能使用来源明确事实；缺失写“未明确”。
- 每张卡 430—650 个中文字符，字段完全相同。
- 保持 V1/V2/V3 边界，不混合候选。
- 卡内不要解释“电压预算”“两押注”或来源机制。

严格格式，不要前言：
# STANDARDIZED VOLTAGE CARDS｜题材名
## V1
### 一句话货架简介
### 主角开局存在形态
### 世界眼前高压事实
### 直接不公平特权
### 第一章标志性画面
### 反复改变玩法的新动作
### 首次兑现与他人反应
### 20章换挡与百章长线
### 最小边界与主要风险
## V2
（同字段）
## V3
（同字段）
"""


CASEWISE_JUDGE = """你只会看到一个题材、十张匿名且同格式的中文男频长篇前提卡。来源未知。

评价原则：
- 不奖励篇幅、术语数量、血腥、生理猎奇或“设定很多”。
- Boldness 是一个高风险押注能一句话让人看见，并永久改变主角动作、欲望或社会位置。
- 高分方案应迅速回答：为什么想点开；主角反复做什么；第一次如何不公平兑现；别人为何重新估价他。
- 惩罚四个同等 gimmick 抢主轴、世界与外挂钥匙锁孔式预配、只换名词、长解释、百章后只剩同一招放大。
- 非人主角不自动加分或减分；关键是可读、可欲、可持续。
- 只能评价当前这一组，不得引用或想象其它题材候选。

每个方案给以下 0—10 分：Click、Bold、Clear、Changed Verbs、Immediate Payoff、Social Repricing、Long-form Runway、Coherence Without Overfit、Risk（0最好，10最危险），再给 Overall 0—100。

严格输出，不要前言：
# VOLTAGE BLIND PANEL
## CASE｜题材名
### Score Table
| 方案 | Click | Bold | Clear | Verbs | Payoff | Social | Long | Indep | Risk | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
（A—J 十行全部输出）
### Top 3
1. 方案X：最强理由；最大风险。
2. ...
3. ...
### Decision
- 最愿意直接试写前三章：方案X，因为……
- 最有野心但目前过载：方案Y，因为……
- 最安全却最可能被忘记：方案Z，因为……
"""


def extract_cards(text: str, ids: tuple[str, ...]) -> dict[str, str]:
    alternation = "|".join(re.escape(x) for x in ids)
    pattern = re.compile(rf"(?m)^## ({alternation})\s*$")
    matches = list(pattern.finditer(text))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.end() : end].strip()
    missing = [item for item in ids if item not in result]
    if missing:
        raise RuntimeError(f"missing standardized cards: {missing}")
    return result


def make_blind(case_id: str, cards: dict[str, str]) -> tuple[str, dict[str, str]]:
    source_ids = list(ALL_IDS)
    rng = random.Random(2026082902 + sum(ord(ch) for ch in case_id))
    rng.shuffle(source_ids)
    mapping = dict(zip(LABELS, source_ids, strict=True))
    blocks: list[str] = []
    for label in LABELS:
        blocks.extend((f"## 方案 {label}", cards[mapping[label]], ""))
    return "\n".join(blocks).strip() + "\n", mapping


def validate_report(text: str, *, case_display: str) -> None:
    if case_display not in text:
        raise RuntimeError(f"voltage panel missing case title: {case_display}")
    labels = set(re.findall(r"(?m)^\|\s*(?:方案\s*)?([A-J])\s*\|", text))
    if labels != set(LABELS):
        raise RuntimeError(f"voltage panel labels invalid: {case_display} {sorted(labels)}")


def main() -> None:
    out = EXP / "voltage_panel_casewise"
    out.mkdir(exist_ok=True)
    run_meta: list[dict[str, object]] = []

    # One fact-only standardizer per case; prior B/S/C standardized cards are reused unchanged.
    standardize_jobs = []
    for case in CASES:
        d = out / case.case_id
        d.mkdir(exist_ok=True)
        source = read(EXP / case.case_id / "orthogonal" / "voltage_budget_2" / "response.md")
        prompt = "\n\n".join(
            (
                VOLTAGE_STANDARDIZER.replace("题材名", case.display).strip(),
                f"# SOURCE｜{case.display}\n{source}",
            )
        ) + "\n"
        p = d / "STANDARDIZE_PROMPT.md"
        p.write_text(prompt, encoding="utf-8")
        standardize_jobs.append(
            (
                p,
                d / "STANDARDIZE_ACP.json",
                d / "STANDARDIZED_VOLTAGE_CARDS.md",
                f"voltage-standardize-{case.case_id}",
            )
        )

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(run_one, p, o, r, label=label, model="gpt-5.6-terra"): label
            for p, o, r, label in standardize_jobs
        }
        for future in as_completed(futures):
            result = future.result()
            run_meta.append(result)
            print("DONE", result, flush=True)

    mappings: dict[str, dict[str, str]] = {}
    blind_packages: dict[str, str] = {}
    for case in CASES:
        old = extract_cards(
            read(EXP / "blind_panel" / case.case_id / "STANDARDIZED_CARDS.md"),
            OLD_IDS,
        )
        voltage = extract_cards(
            read(out / case.case_id / "STANDARDIZED_VOLTAGE_CARDS.md"),
            VOLTAGE_IDS,
        )
        blind, mapping = make_blind(case.case_id, {**old, **voltage})
        full = f"# CASE｜{case.display}\n\n{blind}"
        (out / case.case_id / "BLIND_CARDS.md").write_text(full, encoding="utf-8")
        mappings[case.case_id] = mapping
        blind_packages[case.case_id] = full
    (out / "ANON_MAPPING.json").write_text(
        json.dumps(mappings, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    models = {
        "commercial": "gpt-5.6-luna",
        "cold_reader": "gpt-5.6-terra",
        "longform": "gpt-5.6-sol",
    }
    judge_jobs = []
    for case in CASES:
        for role, model in models.items():
            d = out / case.case_id / role
            d.mkdir(parents=True, exist_ok=True)
            prompt = "\n\n".join(
                (ROLE_PROMPTS[role].strip(), CASEWISE_JUDGE.strip(), blind_packages[case.case_id])
            ) + "\n"
            p = d / "PROMPT.md"
            p.write_text(prompt, encoding="utf-8")
            judge_jobs.append(
                (
                    p,
                    d / "ACP.json",
                    d / "REPORT.md",
                    f"voltage-panel-{case.case_id}-{role}",
                    model,
                    case.display,
                )
            )

    with ThreadPoolExecutor(max_workers=9) as pool:
        futures = {
            pool.submit(run_one, p, o, r, label=label, model=model): (r, display)
            for p, o, r, label, model, display in judge_jobs
        }
        for future in as_completed(futures):
            report_path, display = futures[future]
            result = future.result()
            validate_report(read(report_path), case_display=display)
            run_meta.append(result)
            print("DONE", result, flush=True)

    report_blocks: list[str] = []
    for case in CASES:
        for role in models:
            report_blocks.extend(
                (
                    f"# REPORT｜{case.case_id}｜{role}",
                    read(out / case.case_id / role / "REPORT.md"),
                )
            )
    synthesis_prompt = f"""你是实验统计与架构审计员。下方是九份逐题材独立盲评和匿名映射。候选来源：
- B0 = current production
- S1-S3 = Single-Agent Premise Forge
- C1-C3 = four-axis all-hot fixed collision
- V1-V3 = four fresh axes reused under an asymmetric two-bet voltage budget

只能使用表内数字算术汇总。逐候选列出三位 Overall 和平均分（1位小数），再分别给四类来源的 ceiling / floor / pool mean。重点回答：V 是否修复 C 的清晰度/过载损失；是否追上 S；哪一类风险仍存在。不要替作者宣称 production 已冻结。

严格格式：
# VOLTAGE PANEL SYNTHESIS
## Data Integrity
## Per-Case De-blinded Scores
### 通用玄幻成长
### 20章一世界快节奏长篇
### 游戏副本／无限流
## Generator-Level Ceiling / Floor / Mean
## Did Two-Bet Budget Repair Full Collision?
## Single-Pass vs Two-Bet Trade-off
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
        label="voltage-panel-synthesis",
        model="gpt-5.6-luna",
    )
    run_meta.append(result)
    (out / "RUN_SUMMARY.json").write_text(
        json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
