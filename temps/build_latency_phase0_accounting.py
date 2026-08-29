from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from difflib import SequenceMatcher, unified_diff
from pathlib import Path
from statistics import mean, median

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
OUT = (
    ROOT
    / "books"
    / "real-exp-chapter-latency-optimization-20260829-v1"
    / "phase-0-runtime-accounting"
)
STAGES = ("director", "curator", "primary", "authority_reviser", "state")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.hybrid_runtime import extract_primary_draft  # noqa: E402


def clean_model_text(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text
    ).strip()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def usage_from(data: dict) -> dict[str, int]:
    usage = data.get("result", {}).get("usage", {}) or {}
    return {
        "input_tokens": int(usage.get("inputTokens") or 0),
        "cached_read_tokens": int(usage.get("cachedReadTokens") or 0),
        "output_tokens": int(usage.get("outputTokens") or 0),
        "thought_tokens": int(usage.get("thoughtTokens") or 0),
        "total_tokens": int(usage.get("totalTokens") or 0),
    }


def response_body(path: Path) -> str:
    if not path.is_file():
        return ""
    return extract_primary_draft(clean_model_text(path.read_text(encoding="utf-8"))).strip()


def changed_line_count(before: str, after: str) -> int:
    diff = unified_diff(before.splitlines(), after.splitlines(), lineterm="")
    return sum(
        1
        for line in diff
        if (line.startswith("+") or line.startswith("-"))
        and not line.startswith("+++")
        and not line.startswith("---")
    )


def round_or_blank(value: float | int | None, digits: int = 3):
    if value is None:
        return ""
    return round(float(value), digits)


def build_node_and_chapter_metrics() -> tuple[list[dict], list[dict]]:
    node_rows: list[dict] = []
    chapter_rows: list[dict] = []
    for chapter in range(1, 21):
        run_dir = BOOK / "runs" / f"chapter-{chapter:04d}"
        chapter_stage_seconds: dict[str, float] = {}
        for stage in STAGES:
            acp_path = run_dir / f"{stage}_acp.json"
            prompt_path = run_dir / f"{stage}_prompt.md"
            response_path = run_dir / f"{stage}_response.md"
            if not acp_path.is_file():
                continue
            data = read_json(acp_path)
            usage = usage_from(data)
            wall = float(data.get("wall_seconds") or 0.0)
            chapter_stage_seconds[stage] = wall
            node_rows.append(
                {
                    "chapter": chapter,
                    "stage": stage,
                    "model": data.get("model", ""),
                    "effort": data.get("effort", ""),
                    "wall_seconds": round(wall, 3),
                    "prompt_chars": len(prompt_path.read_text(encoding="utf-8"))
                    if prompt_path.is_file()
                    else 0,
                    "response_chars": len(
                        clean_model_text(response_path.read_text(encoding="utf-8"))
                    )
                    if response_path.is_file()
                    else 0,
                    **usage,
                }
            )

        primary = response_body(run_dir / "primary_response.md")
        reviser = response_body(run_dir / "authority_reviser_response.md")
        final_path = BOOK / "chapters" / f"chapter-{chapter:04d}.md"
        final = final_path.read_text(encoding="utf-8").strip() if final_path.is_file() else reviser
        primary_reviser_similarity = SequenceMatcher(None, primary, reviser).ratio()
        reviser_final_similarity = SequenceMatcher(None, reviser, final).ratio()
        primary_final_similarity = SequenceMatcher(None, primary, final).ratio()
        chapter_rows.append(
            {
                "chapter": chapter,
                **{
                    f"{stage}_seconds": round_or_blank(
                        chapter_stage_seconds.get(stage)
                    )
                    for stage in STAGES
                },
                "adopted_stage_sum_seconds": round(
                    sum(chapter_stage_seconds.values()), 3
                ),
                "primary_chars": len(primary),
                "reviser_chars": len(reviser),
                "final_chars": len(final),
                "primary_reviser_exact": primary == reviser,
                "primary_reviser_similarity": round(primary_reviser_similarity, 5),
                "primary_reviser_changed_lines": changed_line_count(primary, reviser),
                "reviser_final_exact": reviser == final,
                "reviser_final_similarity": round(reviser_final_similarity, 5),
                "primary_final_similarity": round(primary_final_similarity, 5),
                "final_file_diff": reviser != final,
                "final_file_substantial_diff": reviser_final_similarity < 0.99,
            }
        )
    return node_rows, chapter_rows


def parse_run_log() -> tuple[list[dict], dict]:
    lines = (BOOK / "RUN_LOG.txt").read_text(encoding="utf-8").splitlines()
    start_pattern = re.compile(
        r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ACP START "
        r"(?P<label>\S+) (?P<model>\S+?)/(?P<effort>\S+)$"
    )
    done_pattern = re.compile(
        r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ACP DONE "
        r"(?P<label>\S+) wall=(?P<wall>[0-9.]+) chars=(?P<chars>\d+)$"
    )
    timestamp_pattern = re.compile(
        r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<message>.*)$"
    )
    active: dict[str, list[dict]] = defaultdict(list)
    calls: list[dict] = []
    timeline: list[tuple[datetime, str]] = []
    for line in lines:
        timestamp_match = timestamp_pattern.match(line)
        if timestamp_match:
            timeline.append(
                (
                    datetime.strptime(timestamp_match.group("ts"), TIME_FORMAT),
                    timestamp_match.group("message"),
                )
            )
        start_match = start_pattern.match(line)
        if start_match:
            active[start_match.group("label")].append(
                {
                    "started_at": start_match.group("ts"),
                    "model": start_match.group("model"),
                    "effort": start_match.group("effort"),
                }
            )
            continue
        done_match = done_pattern.match(line)
        if done_match:
            label = done_match.group("label")
            start = active[label].pop(0) if active[label] else {}
            calls.append(
                {
                    "label": label,
                    "started_at": start.get("started_at", ""),
                    "completed_at": done_match.group("ts"),
                    "model": start.get("model", ""),
                    "effort": start.get("effort", ""),
                    "wall_seconds": float(done_match.group("wall")),
                    "response_chars": int(done_match.group("chars")),
                }
            )

    chapter_pattern = re.compile(
        r"^fast20-ch(?P<chapter>\d{2})-(?P<stage>director|curator|primary|authority_reviser|state)$"
    )
    latest_index: dict[tuple[int, str], int] = {}
    for index, call in enumerate(calls):
        match = chapter_pattern.match(call["label"])
        if match:
            latest_index[(int(match.group("chapter")), match.group("stage"))] = index

    for index, call in enumerate(calls):
        match = chapter_pattern.match(call["label"])
        if match:
            chapter = int(match.group("chapter"))
            stage = match.group("stage")
            call.update(
                {
                    "category": "adopted_chapter_stage"
                    if latest_index[(chapter, stage)] == index
                    else "discarded_chapter_stage",
                    "chapter": chapter,
                    "stage": stage,
                }
            )
        elif call["label"] == "fast20-review10":
            call["category"] = "periodic_review"
        else:
            call["category"] = "upstream_setup"

    # A replan occurred inside the interrupted Ch3 interval but was not written to RUN_LOG.
    replan_path = BOOK / "REPLAN_AFTER_CH1_ACP.json"
    if replan_path.is_file():
        data = read_json(replan_path)
        calls.append(
            {
                "label": "fast20-replan-after-ch1",
                "started_at": "",
                "completed_at": "",
                "model": data.get("model", ""),
                "effort": data.get("effort", ""),
                "wall_seconds": float(data.get("wall_seconds") or 0),
                "response_chars": len(clean_model_text(data.get("text", ""))),
                "category": "replan",
                "chapter": 1,
                "stage": "review_replan",
            }
        )

    repair_specs = (
        ("CH19_TIER_REPAIR_ACP.json", "post_run_outcome_repair", 19),
        ("CH19_STATE_REPAIR_ACP.json", "post_run_state_rebuild", 19),
        ("CH20_STATE_REPAIR_ACP.json", "post_run_state_rebuild", 20),
    )
    for filename, category, chapter in repair_specs:
        path = BOOK / filename
        if not path.is_file():
            continue
        data = read_json(path)
        calls.append(
            {
                "label": filename.removesuffix("_ACP.json").lower(),
                "started_at": "",
                "completed_at": "",
                "model": data.get("model", ""),
                "effort": data.get("effort", ""),
                "wall_seconds": float(data.get("wall_seconds") or 0),
                "response_chars": len(clean_model_text(data.get("text", ""))),
                "category": category,
                "chapter": chapter,
                "stage": "repair",
            }
        )

    first_ts = timeline[0][0]
    upstream_done = next(ts for ts, message in timeline if message.startswith("UPSTREAM COMPLETE"))
    first_chapter = next(
        ts for ts, message in timeline if message.startswith("ACP START fast20-ch01-director")
    )
    all_complete = next(ts for ts, message in reversed(timeline) if message.startswith("ALL COMPLETE"))
    interrupted_start = next(
        ts for ts, message in timeline if message.startswith("ACP START fast20-ch03-primary")
    )
    resume = next(ts for ts, message in timeline if message == "RESUME AFTER CH1 REPLAN")
    elapsed = {
        "upstream_actual_seconds": (upstream_done - first_ts).total_seconds(),
        "chapter_batch_actual_seconds": (all_complete - first_chapter).total_seconds(),
        "whole_run_actual_seconds": (all_complete - first_ts).total_seconds(),
        "interrupted_ch3_interval_seconds": (resume - interrupted_start).total_seconds(),
    }
    return calls, elapsed


def raw_gbrain_audit() -> dict:
    rows = []
    for chapter in range(1, 21):
        path = BOOK / "runs" / f"chapter-{chapter:04d}" / "curator_retrieval.json"
        if not path.is_file():
            continue
        data = read_json(path)
        accepted = data.get("accepted") or []
        rows.append(
            {
                "chapter": chapter,
                "accepted_count": int(data.get("accepted_count") or len(accepted)),
                "accepted": [item.get("slug", "") for item in accepted],
            }
        )
    return {
        "chapters_with_files": len(rows),
        "zero_hit_chapters": sum(row["accepted_count"] == 0 for row in rows),
        "total_accepted": sum(row["accepted_count"] for row in rows),
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def seconds_to_minutes(value: float) -> str:
    return f"{value / 60:.2f}"


def build_report(
    node_rows: list[dict],
    chapter_rows: list[dict],
    calls: list[dict],
    elapsed: dict,
    gbrain: dict,
) -> tuple[dict, str]:
    stage_groups: dict[str, list[dict]] = defaultdict(list)
    for row in node_rows:
        stage_groups[row["stage"]].append(row)
    stage_summary = []
    adopted_total = sum(row["adopted_stage_sum_seconds"] for row in chapter_rows)
    for stage in STAGES:
        rows = stage_groups[stage]
        wall = sum(float(row["wall_seconds"]) for row in rows)
        stage_summary.append(
            {
                "stage": stage,
                "average_wall_seconds": mean(float(row["wall_seconds"]) for row in rows),
                "median_wall_seconds": median(float(row["wall_seconds"]) for row in rows),
                "share_percent": wall / adopted_total * 100,
                "average_prompt_chars": mean(int(row["prompt_chars"]) for row in rows),
                "average_input_tokens": mean(int(row["input_tokens"]) for row in rows),
                "average_cached_read_tokens": mean(
                    int(row["cached_read_tokens"]) for row in rows
                ),
                "average_output_tokens": mean(int(row["output_tokens"]) for row in rows),
                "average_thought_tokens": mean(int(row["thought_tokens"]) for row in rows),
            }
        )

    category_seconds = Counter()
    for call in calls:
        category_seconds[call["category"]] += float(call["wall_seconds"])
    repair_seconds = (
        category_seconds["post_run_outcome_repair"]
        + category_seconds["post_run_state_rebuild"]
    )
    batch_realized_seconds = elapsed["chapter_batch_actual_seconds"] + repair_seconds
    whole_realized_seconds = elapsed["whole_run_actual_seconds"] + repair_seconds
    exact_count = sum(row["primary_reviser_exact"] for row in chapter_rows)
    final_file_diff_count = sum(row["final_file_diff"] for row in chapter_rows)
    substantial_final_diff_count = sum(
        row["final_file_substantial_diff"] for row in chapter_rows
    )
    accounting = {
        "stage_summary": stage_summary,
        "adopted_chapter_stage_seconds": adopted_total,
        "adopted_average_seconds": adopted_total / 20,
        "adopted_average_minutes": adopted_total / 20 / 60,
        "category_seconds": dict(category_seconds),
        "elapsed": elapsed,
        "post_run_repair_seconds": repair_seconds,
        "realized_chapter_batch_seconds": batch_realized_seconds,
        "realized_chapter_average_minutes": batch_realized_seconds / 20 / 60,
        "whole_run_with_repairs_seconds": whole_realized_seconds,
        "whole_run_amortized_minutes_per_chapter": whole_realized_seconds / 20 / 60,
        "primary_reviser_exact_count": exact_count,
        "primary_reviser_average_similarity": mean(
            float(row["primary_reviser_similarity"]) for row in chapter_rows
        ),
        "final_file_diff_count": final_file_diff_count,
        "substantial_final_file_diff_count": substantial_final_diff_count,
        "recorded_post_run_prose_repair_count": int(
            category_seconds["post_run_outcome_repair"] > 0
        ),
        "raw_gbrain": gbrain,
    }

    lines = [
        "# Phase 0｜章节 Runtime 真实耗时与累赘审计",
        "",
        "> 冻结来源：`real-exp-fast-world-20ch-20260828-v1`。本报告区分正常采用节点、废弃重跑、周期 Review、终检 Repair 与开书上游；不把未完成调用伪装成可精确计量的模型 wall time。",
        "",
        "## 1. 正常采用章节链",
        "",
        "|节点|平均 wall|中位 wall|占正常章节链|平均 Prompt 字符|平均 input|平均 cache|平均 output|平均 thought|",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    labels = {
        "director": "Director",
        "curator": "Curator",
        "primary": "Primary",
        "authority_reviser": "Authority Reviser",
        "state": "State",
    }
    for row in stage_summary:
        lines.append(
            "|{label}|{avg:.1f}s|{med:.1f}s|{share:.1f}%|{prompt:.0f}|{inp:.0f}|{cache:.0f}|{out:.0f}|{thought:.0f}|".format(
                label=labels[row["stage"]],
                avg=row["average_wall_seconds"],
                med=row["median_wall_seconds"],
                share=row["share_percent"],
                prompt=row["average_prompt_chars"],
                inp=row["average_input_tokens"],
                cache=row["average_cached_read_tokens"],
                out=row["average_output_tokens"],
                thought=row["average_thought_tokens"],
            )
        )
    lines.extend(
        [
            "",
            f"- 20 章正常采用节点合计：**{seconds_to_minutes(adopted_total)} 分钟**；平均 **{adopted_total / 20 / 60:.2f} 分钟/章**。",
            f"- Curator + Reviser：**{next(r['share_percent'] for r in stage_summary if r['stage']=='curator') + next(r['share_percent'] for r in stage_summary if r['stage']=='authority_reviser'):.1f}%**；Primary 只占 **{next(r['share_percent'] for r in stage_summary if r['stage']=='primary'):.1f}%**。",
            "",
            "## 2. 正常平均没有计入的真实成本",
            "",
            "|成本|模型 wall / 实际 elapsed|说明|",
            "|---|---:|---|",
            f"|废弃但已完成的章节节点|{seconds_to_minutes(category_seconds['discarded_chapter_stage'])} 分钟|第一次 Ch2 全链 + 第一次 Ch3 Director/Curator；后来因 Ch1 后重规划废弃|",
            f"|Ch1 后 Replan|{seconds_to_minutes(category_seconds['replan'])} 分钟|单独 ACP 文件，原 RUN_LOG 未记录|",
            f"|十章 Review|{seconds_to_minutes(category_seconds['periodic_review'])} 分钟|第10章后一次|",
            f"|终检 Outcome Repair|{seconds_to_minutes(category_seconds['post_run_outcome_repair'])} 分钟|Ch19 明确恢复“本人进入镇海”|",
            f"|终检 State rebuild|{seconds_to_minutes(category_seconds['post_run_state_rebuild'])} 分钟|Ch19、Ch20|",
            f"|中断区间|{seconds_to_minutes(elapsed['interrupted_ch3_interval_seconds'])} 分钟 elapsed|Ch3 Primary 启动后被重规划中断；其中包含 Replan，剩余时间不能可靠归因给模型，故不计入模型 wall|",
            "",
            f"- 从 Ch1 Director 启动到 Ch20 完成，实际 elapsed：**{seconds_to_minutes(elapsed['chapter_batch_actual_seconds'])} 分钟**。",
            f"- 加上运行后终检修复后，真实章节批次：**{seconds_to_minutes(batch_realized_seconds)} 分钟**，摊到 20 章为 **{batch_realized_seconds / 20 / 60:.2f} 分钟/章**。",
            f"- 再摊入开书上游，整本实验从启动到修复完成约 **{seconds_to_minutes(whole_realized_seconds)} 分钟**，即 **{whole_realized_seconds / 20 / 60:.2f} 分钟/章**。",
            "",
            "## 3. Reviser 实际改动量",
            "",
            f"- Primary → Reviser 平均字符相似度：**{accounting['primary_reviser_average_similarity']:.3f}**。",
            f"- 20 章中 Primary 被 Reviser 完全原样返回：**{exact_count} 章**。保存后的最终文件有 **{final_file_diff_count} 章**与 Reviser response 非字节级相同，但只有 **{substantial_final_diff_count} 章**字符相似度低于 0.99；已记录的额外正文 Repair 为 Ch19 一次。",
            "- `CHAPTER_METRICS.csv` 逐章记录 exact、changed lines、Primary/Reviser/最终稿三方相似度，后续 Patch Reviser A/B 以此为基线。",
            "",
            "## 4. 章节 raw GBrain",
            "",
            f"- 历史 runner 共留下 **{gbrain['chapters_with_files']}** 份 Curator retrieval；其中 **{gbrain['zero_hit_chapters']}** 章零命中，总计只接受 **{gbrain['total_accepted']}** 条。",
            "- production prompt 层现已 fail closed：所有 Hybrid Chapter Runtime 即使调用方误传 `gbrain_inspiration` / Reference Program，也不再让它进入 Curator、Primary、Reviser 或 Specialist。Scene Skill 继续作为 source-blind 的窄 craft 带宽。",
            "",
            "## 5. Phase 0 结论",
            "",
            "1. 正常链的主要耗时不是写作，而是 Curator + Reviser 的重复保险。",
            "2. 后十章 stale Long Block 属于确定性脏上下文，必须在 Runtime 边界删除，不能留给模型判断。",
            "3. 章节 raw GBrain 在该实验中几乎无收益，并违背当前章节 Authority 边界，已从 prompt 真源与活跃批量 runner 双重关闭。",
            "4. 后续 Phase 1/2/3 的质量比较必须同时展示“正常采用耗时”和“真实批次摊销耗时”，不能让下游 high Reviser 掩盖上游漂移。",
            "",
            "## What This Did Not Solve",
            "",
            "- 没有把 Curator、Reviser 或 Director 自动降档；这些仍需受控 A/B。",
            "- 没有修改 ACP runner，也没有修改前端。",
            "- 没有把本次 20 章的模型 wall 外推为 direct API latency。",
        ]
    )
    return accounting, "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    node_rows, chapter_rows = build_node_and_chapter_metrics()
    calls, elapsed = parse_run_log()
    gbrain = raw_gbrain_audit()
    accounting, report = build_report(node_rows, chapter_rows, calls, elapsed, gbrain)

    write_csv(OUT / "NODE_METRICS.csv", node_rows)
    write_csv(OUT / "CHAPTER_METRICS.csv", chapter_rows)
    write_csv(OUT / "PIPELINE_EVENTS.csv", calls)
    (OUT / "RAW_GBRAIN_AUDIT.json").write_text(
        json.dumps(gbrain, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "PHASE0_ACCOUNTING.json").write_text(
        json.dumps(accounting, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "PHASE0_ACCOUNTING_REPORT.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
