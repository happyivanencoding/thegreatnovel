from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import mean

ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-chapter-latency-optimization-20260829-v1"
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
PHASE1 = BASE / "phase-1-patch-reviser"
OUT = BASE / "phase-1b-patch-risk-router"

# Preflight risks whose semantics must stay with the existing full Authority Reviser.
# The router reads only frozen Mission/Curator authority, never the model's patch output.
HIGH_RISK_PATTERNS = {
    "asset_holder_or_ownership": re.compile(
        r"持有权|所有权|使用决定权|归属|"
        r"(?:交给|交付|接管|收下|买断|转移).{0,20}(?:回潮楔|反潮记录|原件|古器|物品)|"
        r"(?:回潮楔|反潮记录|原件|古器|物品).{0,20}(?:交给|交付|接管|收下|买断|转移)"
    ),
    "explicit_milestone": re.compile(
        r"(?:进入|晋升|突破|达到|成为).{0,8}"
        r"(?:成炉|照域|镇海|\d+级|\d+星|\d+重|正式行潮|正式弟子|长老)"
    ),
    "reader_release": re.compile(r"第\d+章｜触发："),
    "long_history_reveal": re.compile(r"旧史|过去原因|身份谜|秘密揭晓|真相揭晓"),
    "world_horizon": re.compile(r"World Horizon Handoff|世界交接|下一世界"),
}


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text
    ).strip()


def exact_block(prompt: str, start: str, end: str) -> str:
    start_index = prompt.index(start) + len(start)
    end_index = prompt.index(end, start_index)
    return prompt[start_index:end_index].strip()


def route(chapter: int) -> tuple[str, list[str], str]:
    prompt = (
        SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_prompt.md"
    ).read_text(encoding="utf-8")
    mission = exact_block(
        prompt,
        "## FROZEN CHAPTER MISSION｜不得改剧情",
        "## CURATOR｜本章近端注意力与实现要求",
    )
    mission = mission.split("\n规划备注（planning note）：", 1)[0].rstrip()
    curator = exact_block(
        prompt,
        "## CURATOR｜本章近端注意力与实现要求",
        "## WORLD REALITY AUTHORITY｜远端安全世界事实",
    )
    audit_match = re.search(
        r"(?ms)^# Curator Audit\s*$\n(.*?)(?=^# Curated Chapter Context\s*$|\Z)",
        curator,
    )
    curator_audit = audit_match.group(1).strip() if audit_match else ""
    reader_release = exact_block(
        prompt,
        "## READER RELEASE｜本章已批准首次释放事实；逐条核对",
        "## POWER CORE｜Frozen Authority",
    )
    active_release = (
        reader_release
        if "没有排程 Reader Release" not in reader_release
        and "没有 Reader Release" not in reader_release
        else ""
    )
    preflight = "\n\n".join((mission, curator_audit, active_release))
    risks = [
        name
        for name, pattern in HIGH_RISK_PATTERNS.items()
        if pattern.search(preflight)
    ]
    return ("full_high" if risks else "patch_medium"), risks, preflight


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    phase1_rows = json.loads((PHASE1 / "summary.json").read_text(encoding="utf-8"))
    rows = []
    for item in phase1_rows:
        chapter = int(item["chapter"])
        selected_route, risks, _ = route(chapter)
        if selected_route == "full_high":
            effective_seconds = float(item["control_high_wall_seconds"])
            final_source = "control_high"
            quality_note = "preflight 直接走 full high；不运行 Patch"
        else:
            effective_seconds = float(item["wall_seconds"])
            final_source = "patch_medium"
            quality_note = "采用 Patch/NO_CHANGE；仍需作者依据盲评判断质量损失"
        rows.append(
            {
                "chapter": chapter,
                "route": selected_route,
                "risk_reasons": risks,
                "effective_seconds": round(effective_seconds, 3),
                "control_high_seconds": item["control_high_wall_seconds"],
                "speedup_percent": round(
                    (1 - effective_seconds / float(item["control_high_wall_seconds"])) * 100,
                    2,
                ),
                "final_source": final_source,
                "quality_note": quality_note,
            }
        )

    control_average = mean(float(row["control_high_seconds"]) for row in rows)
    routed_average = mean(float(row["effective_seconds"]) for row in rows)
    summary = {
        "rows": rows,
        "control_average_seconds": control_average,
        "routed_average_seconds": routed_average,
        "average_speedup_percent": (1 - routed_average / control_average) * 100,
        "decision": (
            "Risk router catches the Ch13 ownership failure before Patch execution; "
            "accepted routine outputs remain judge-mixed, so keep experimental."
        ),
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Phase 1b｜Patch Reviser 预路由护栏",
        "",
        "> 这不是 production 冻结。它验证能否在调用前把所有权/持有人、显式突破、Reader Release、长期揭晓与 World Handoff 直接路由给现有 Luna-high Full Reviser。",
        "",
        "|章|预路由|触发风险|有效耗时|原 high|节省|质量证据|",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    judge_notes = {
        2: "Reader 选 high；Authority 判 MIXED；Patch 无硬错但少了 high 的去流程修订。",
        13: "所有权/原件风险预路由 high；避开 v1 的‘收进袖中→推回主人公’硬错。",
        16: "Reader 选 Patch；Authority 选 high；无一致硬错结论，仍属 MIXED。",
    }
    for row in rows:
        lines.append(
            f"|{row['chapter']}|{row['route']}|{', '.join(row['risk_reasons']) or '无'}|"
            f"{row['effective_seconds']:.1f}s|{float(row['control_high_seconds']):.1f}s|"
            f"{row['speedup_percent']:.1f}%|{judge_notes[row['chapter']]}|"
        )
    lines.extend(
        [
            "",
            f"- 三章 control high 平均：**{control_average:.1f}s**；预路由后平均：**{routed_average:.1f}s**；理论节省 **{(1-routed_average/control_average)*100:.1f}%**。",
            "- 但两个被允许进入 Patch 的样本，Reader 与 Authority 都没有形成一致胜负，因此不能以‘无硬错’直接等同‘质量不降’。",
            "- 当前结论：**Patch Reviser 架构有速度潜力；v1 失败，v1+预路由仍不足以冻结 production。**",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
