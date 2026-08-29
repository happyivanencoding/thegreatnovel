from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
OUT = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-h2-atomic-delta-corrected-repeat2"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 9, 14, 16)

sys.path.insert(0, str(ROOT / "temps"))
from atomic_chapter_obligations import (  # noqa: E402
    body,
    compile_obligations,
    infer_diff_operations,
    save_pack,
    validate_candidate,
)

spec = importlib.util.spec_from_file_location(
    "paragraph_delta_base",
    ROOT / "temps" / "run_latency_innovation_paragraph_delta_reviser.py",
)
base = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base)

ATOMIC_SUPPLEMENT = """# ATOMIC CHAPTER OBLIGATIONS｜Deterministic Adoption Contract

下方 Atomic Pack 由代码从 Frozen Mission / Reader Release / Canon / Power / Human / Curator 与 Primary evidence 编译。它不是新 Authority，也不是正文配额。局部操作应用后，代码会逐条验证；任何 hard obligation 未闭合，整份 Delta 都会被丢弃并回退 Full Luna-high Reviser。

你必须遵守：
- actor → action → object 不可换人、换本体/分身、换原件/副本；
- received / entitlement / pending / lost / disputed 不得互相升级；
- battle scale / pressure / Public Proof 不得升级成未批准稳定境界；
- deadline 不等于已完成，实际 Ending 不能降成准备；
- MUST_REMAIN_UNKNOWN 只禁止补答案，不要求重复“未知”；
- PRESERVE_IF_PRESENT 只在你触及相关 Primary 段落时保护其类别价值，不要求新增欲望、关系、奖励或惊喜；
- CONDITIONAL cue 只在 Pack 已明确触发时处理；
- Pack 与上方 Frozen Authority 冲突时以 Frozen Authority 为准，并宁可 KEEP_ALL；
- 若修一个状态会影响非相邻后文，必须把所有相关段落同时列入操作。

不要把 obligation 文案复制进正文。若 Primary 已闭合所有义务且没有明确低价值失败，输出 KEEP_ALL。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def compact_pack(pack) -> str:
    lines = [
        f"chapter: {pack.chapter}",
        f"protagonist: {pack.protagonist}",
        f"preflight_eligible: {str(pack.preflight_eligible).lower()}",
        "",
        "## HARD / CONDITIONAL OBLIGATIONS",
    ]
    for item in pack.obligations:
        if item.kind.value == "source_conflict":
            continue
        triplet = " → ".join(part for part in (item.subject, item.action, item.object) if part)
        lines.append(
            f"- [{item.id}] {item.kind.value} / {item.mode.value} / {item.severity.value}"
            + (f" | {triplet}" if triplet else "")
        )
        lines.append(f"  Source: {item.source_text}")
        if item.status:
            lines.append(f"  Required state: {item.status}")
        if item.boundary:
            lines.append(f"  Boundary: {item.boundary}")
        if item.primary_evidence_paragraphs:
            lines.append(
                "  Primary evidence: "
                + ", ".join(f"P{index:03d}" for index in item.primary_evidence_paragraphs)
            )
    if pack.diagnostics:
        lines.extend(("", "## NON-BLOCKING SOURCE DIAGNOSTICS"))
        lines.extend(f"- {item}" for item in pack.diagnostics)
    return "\n".join(lines).strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                [
                    "node",
                    str(RUNNER),
                    str(prompt_path),
                    str(output_path),
                    "gpt-5.6-luna",
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
            last = f"timeout after 1200s: {prompt_path}"
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
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    authority_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    curator = (source / "curator_response.md").read_text(encoding="utf-8")
    primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    full = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
    pack = compile_obligations(
        chapter=chapter,
        authority_prompt=authority_prompt,
        curator_response=curator,
        primary_body=primary,
    )
    save_pack(pack, directory / "obligation_pack.json")
    compact = compact_pack(pack)
    (directory / "compact_obligations.md").write_text(compact + "\n", encoding="utf-8")
    if not pack.preflight_eligible:
        raise RuntimeError(f"chapter {chapter} unexpectedly not preflight eligible")

    runtime_start = authority_prompt.index("# Hybrid Runtime")
    draft_marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    draft_start = authority_prompt.index(draft_marker, runtime_start)
    authority_context = authority_prompt[runtime_start:draft_start].strip()
    prompt = (
        base.DELTA_TEMPLATE
        + "\n\n"
        + ATOMIC_SUPPLEMENT
        + "\n\n# ATOMIC PACK\n\n"
        + compact
        + "\n\n"
        + authority_context
        + "\n\n# NUMBERED PRIMARY DRAFT\n\n"
        + base.numbered(primary)
    )
    prompt_path = directory / "atomic_delta_prompt.md"
    output_path = directory / "atomic_delta_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "atomic_delta_response.md").write_text(response + "\n", encoding="utf-8")

    apply_error = ""
    try:
        delta_body, operations = base.apply_ops(response, primary)
    except Exception as error:
        apply_error = str(error)
        delta_body, operations = primary, []
    (directory / "delta_body.md").write_text(delta_body + "\n", encoding="utf-8")

    if apply_error:
        gate = {
            "chapter": chapter,
            "decision": "FALLBACK_FULL_REVISER",
            "blocking_checks": [{"obligation_id": "PATCH_APPLY", "reason": apply_error}],
            "status_counts": {},
            "touched_source_paragraphs": [],
        }
    else:
        gate = validate_candidate(
            pack,
            primary_body=primary,
            final_body=delta_body,
            operations=operations,
        )
    (directory / "atomic_gate.json").write_text(
        json.dumps(gate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    full_gate = validate_candidate(
        pack,
        primary_body=primary,
        final_body=full,
        operations=infer_diff_operations(primary, full),
    )
    (directory / "full_reviser_gate.json").write_text(
        json.dumps(full_gate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    adopted = gate["decision"] == "ADOPT_DELTA"
    route_body = delta_body if adopted else full
    route_status = (
        "ADOPT_DELTA"
        if adopted
        else (
            "FALLBACK_FULL_REVISER"
            if full_gate["decision"] == "ADOPT_DELTA"
            else "FULL_REVISER_RESIDUAL_FAILURE"
        )
    )
    (directory / "route_final_body.md").write_text(route_body + "\n", encoding="utf-8")

    full_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    delta_wall = float(data.get("wall_seconds") or 0)
    full_wall = float(full_data.get("wall_seconds") or 0)
    effective_wall = delta_wall if adopted else delta_wall + full_wall
    return {
        "chapter": chapter,
        "preflight_eligible": pack.preflight_eligible,
        "obligation_count": len(pack.obligations),
        "compact_obligation_chars": len(compact),
        "delta_wall_seconds": delta_wall,
        "control_full_reviser_seconds": full_wall,
        "effective_route_seconds": round(effective_wall, 3),
        "fallback_adjusted_speedup_percent": round((1 - effective_wall / full_wall) * 100, 2),
        "delta_gate_decision": gate["decision"],
        "route_status": route_status,
        "operation_count": len(operations),
        "operations": operations,
        "apply_error": apply_error,
        "blocking_ids": [item["obligation_id"] for item in gate.get("blocking_checks", [])],
        "blocking_reasons": [item["reason"] for item in gate.get("blocking_checks", [])],
        "full_reviser_gate_decision": full_gate["decision"],
        "full_reviser_blocking_ids": [item["obligation_id"] for item in full_gate.get("blocking_checks", [])],
        "delta_prompt_chars": len(prompt),
        "delta_response_chars": len(response),
        "delta_final_chars": len(delta_body),
        "route_final_chars": len(route_body),
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
    summary = {
        "version": "atomic-obligations-v0.2-protagonist-corrected",
        "chapters": list(CHAPTERS),
        "samples": len(rows),
        "adopted": sum(row["route_status"] == "ADOPT_DELTA" for row in rows),
        "fallback_full": sum(row["route_status"] == "FALLBACK_FULL_REVISER" for row in rows),
        "full_reviser_residual_failure": sum(row["route_status"] == "FULL_REVISER_RESIDUAL_FAILURE" for row in rows),
        "control_total_seconds": round(sum(row["control_full_reviser_seconds"] for row in rows), 3),
        "effective_total_seconds": round(sum(row["effective_route_seconds"] for row in rows), 3),
        "rows": rows,
    }
    summary["fallback_adjusted_speedup_percent"] = round(
        (1 - summary["effective_total_seconds"] / summary["control_total_seconds"]) * 100,
        2,
    )
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
