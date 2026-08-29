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
FIRST = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-c0-gate-only-delta"
OUT = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-c4-residual-repair-repeat2"
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

RESIDUAL_TEMPLATE = """你是 TGN 的 Residual Atomic Paragraph Repair，使用 GPT-5.6 Luna high。

前一轮 Paragraph-Delta 已经尽量保持人物、场面和商业读感，但 deterministic Atomic Gate 只发现下方列出的少数 hard blockers。你只能修这些 blocker，不能重新规划、不能顺手润色、不能处理未列出的普通问题。

规则：
- 每个 blocker 必须用最小局部改动闭合；
- actor → action → object 不得换本体/分身、原件/副本或支付/接收者；
- Reader Release 只补一次可复述事实，不开百科；
- 修一处状态若与后文有同对象状态，必须把相关后文一并闭合；
- 不删主角欲望、关系、Reward、Public Proof、Social Repricing、具体场面或章末推动；
- 不新增数字、制度、世界规则、能力机制、人物到场、奖励、旧史或未来事件；
- 如果 candidate 已经真实闭合 blocker，输出 KEEP_ALL；
- 输出只允许 KEEP_ALL 或 Paragraph Delta 操作格式。
"""


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




def load_first_candidate(first_dir: Path, primary: str) -> str:
    """Load the pre-fallback Gate-only candidate, rebuilding it if needed."""

    for name in (
        "delta_candidate.md",
        "delta_body.md",
        "candidate_body.md",
        "patched_body.md",
    ):
        path = first_dir / name
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    response_path = first_dir / "delta_response.md"
    if response_path.exists():
        response = response_path.read_text(encoding="utf-8").strip()
        candidate, _ = base.apply_ops(response, primary)
        return candidate.strip()
    raise FileNotFoundError(f"missing Gate-only pre-fallback candidate in {first_dir}")


def blocker_text(pack, gate: dict) -> str:
    by_id = {item.id: item for item in pack.obligations}
    lines = []
    for blocker in gate.get("blocking_checks", []):
        item = by_id.get(blocker["obligation_id"])
        if item is None:
            lines.append(f"- [{blocker['obligation_id']}] {blocker['reason']}")
            continue
        triplet = " → ".join(part for part in (item.subject, item.action, item.object) if part)
        lines.extend(
            [
                f"- [{item.id}] {item.kind.value} / {item.mode.value}",
                f"  Required: {item.source_text}",
                f"  Typed: {triplet or '(no triplet)'}",
                f"  Boundary: {item.boundary}",
                f"  Gate failure: {blocker['reason']}",
            ]
        )
    return "\n".join(lines)


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    first_dir = FIRST / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    authority_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    curator = (source / "curator_response.md").read_text(encoding="utf-8")
    primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    full = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
    first_candidate = load_first_candidate(first_dir, primary)
    first_gate = json.loads((first_dir / "atomic_gate.json").read_text(encoding="utf-8"))
    pack = compile_obligations(
        chapter=chapter,
        authority_prompt=authority_prompt,
        curator_response=curator,
        primary_body=primary,
    )
    save_pack(pack, directory / "obligation_pack.json")

    first_summary = json.loads((FIRST / "summary.json").read_text(encoding="utf-8"))
    first_row = next(row for row in first_summary["rows"] if row["chapter"] == chapter)
    first_wall = float(first_row["delta_wall_seconds"])
    full_wall = float(first_row["control_full_reviser_seconds"])
    residual_wall = 0.0
    residual_operations: list[dict] = []
    residual_response = "NOT_RUN"
    second_candidate = first_candidate
    apply_error = ""

    if first_gate["decision"] != "ADOPT_DELTA":
        runtime_start = authority_prompt.index("# Hybrid Runtime")
        draft_marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
        draft_start = authority_prompt.index(draft_marker, runtime_start)
        authority_context = authority_prompt[runtime_start:draft_start].strip()
        blockers = blocker_text(pack, first_gate)
        (directory / "residual_blockers.md").write_text(blockers + "\n", encoding="utf-8")
        prompt = (
            base.DELTA_TEMPLATE
            + "\n\n"
            + RESIDUAL_TEMPLATE
            + "\n\n# ONLY BLOCKING OBLIGATIONS\n\n"
            + blockers
            + "\n\n"
            + authority_context
            + "\n\n# NUMBERED CURRENT CANDIDATE\n\n"
            + base.numbered(first_candidate)
        )
        prompt_path = directory / "residual_prompt.md"
        output_path = directory / "residual_acp.json"
        prompt_path.write_text(prompt, encoding="utf-8")
        data = call(prompt_path, output_path)
        residual_wall = float(data.get("wall_seconds") or 0)
        residual_response = clean(data.get("text", ""))
        (directory / "residual_response.md").write_text(residual_response + "\n", encoding="utf-8")
        try:
            second_candidate, residual_operations = base.apply_ops(residual_response, first_candidate)
        except Exception as error:
            apply_error = str(error)
            second_candidate = first_candidate
            residual_operations = []

    (directory / "residual_candidate.md").write_text(second_candidate + "\n", encoding="utf-8")
    if apply_error:
        second_gate = {
            "decision": "FALLBACK_FULL_REVISER",
            "blocking_checks": [{"obligation_id": "PATCH_APPLY", "reason": apply_error}],
            "status_counts": {},
        }
    else:
        second_gate = validate_candidate(
            pack,
            primary_body=primary,
            final_body=second_candidate,
            operations=infer_diff_operations(primary, second_candidate),
        )
    (directory / "atomic_gate.json").write_text(
        json.dumps(second_gate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    full_gate = validate_candidate(
        pack,
        primary_body=primary,
        final_body=full,
        operations=infer_diff_operations(primary, full),
    )
    adopted = second_gate["decision"] == "ADOPT_DELTA"
    if adopted:
        route_body = second_candidate
        route_status = "ADOPT_DELTA" if residual_wall == 0 else "ADOPT_AFTER_RESIDUAL_REPAIR"
        effective_wall = first_wall + residual_wall
    else:
        route_body = full
        route_status = "FALLBACK_FULL_REVISER" if full_gate["decision"] == "ADOPT_DELTA" else "FULL_REVISER_RESIDUAL_FAILURE"
        effective_wall = first_wall + residual_wall + full_wall
    (directory / "route_final_body.md").write_text(route_body + "\n", encoding="utf-8")
    return {
        "chapter": chapter,
        "first_gate_decision": first_gate["decision"],
        "first_blocking_ids": [item["obligation_id"] for item in first_gate.get("blocking_checks", [])],
        "residual_ran": residual_wall > 0,
        "residual_wall_seconds": residual_wall,
        "residual_operation_count": len(residual_operations),
        "residual_response_mode": residual_response.splitlines()[0] if residual_response else "",
        "second_gate_decision": second_gate["decision"],
        "second_blocking_ids": [item["obligation_id"] for item in second_gate.get("blocking_checks", [])],
        "route_status": route_status,
        "first_delta_wall_seconds": first_wall,
        "full_reviser_wall_seconds": full_wall,
        "effective_route_seconds": round(effective_wall, 3),
        "fallback_adjusted_speedup_percent": round((1 - effective_wall / full_wall) * 100, 2),
        "apply_error": apply_error,
        "route_final_chars": len(route_body),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    control = sum(row["full_reviser_wall_seconds"] for row in rows)
    effective = sum(row["effective_route_seconds"] for row in rows)
    summary = {
        "version": "atomic-obligations-v0.1-residual-repair",
        "samples": len(rows),
        "adopted_direct": sum(row["route_status"] == "ADOPT_DELTA" for row in rows),
        "adopted_after_residual": sum(row["route_status"] == "ADOPT_AFTER_RESIDUAL_REPAIR" for row in rows),
        "fallback_full": sum(row["route_status"] == "FALLBACK_FULL_REVISER" for row in rows),
        "full_reviser_residual_failure": sum(row["route_status"] == "FULL_REVISER_RESIDUAL_FAILURE" for row in rows),
        "control_total_seconds": round(control, 3),
        "effective_total_seconds": round(effective, 3),
        "fallback_adjusted_speedup_percent": round((1 - effective / control) * 100, 2),
        "rows": rows,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
