from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs" / "chapter-0016"
ATOMIC = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1"
REPEAT = ATOMIC / "phase-c2-atomic-delta-repeat2" / "chapter-0016"
OUT = ATOMIC / "phase-e-atomic-full-fallback" / "chapter-0016"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

sys.path.insert(0, str(ROOT / "temps"))
from atomic_chapter_obligations import (  # noqa: E402
    body,
    compile_obligations,
    infer_diff_operations,
    save_pack,
    validate_candidate,
)


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
            data = json.loads(output_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    authority_prompt = (SOURCE / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    curator = (SOURCE / "curator_response.md").read_text(encoding="utf-8")
    primary = body((SOURCE / "primary_response.md").read_text(encoding="utf-8"))
    pack = compile_obligations(
        chapter=16,
        authority_prompt=authority_prompt,
        curator_response=curator,
        primary_body=primary,
    )
    save_pack(pack, OUT / "obligation_pack.json")
    failed_gate = json.loads((REPEAT / "atomic_gate.json").read_text(encoding="utf-8"))
    by_id = {item.id: item for item in pack.obligations}
    lines = [
        "# ATOMIC FALLBACK REPAIR｜Gate-confirmed hard failures",
        "",
        "前一次 Paragraph-Delta 未通过 deterministic Gate。下面每一项都是当前 Full Reviser 必须修复的具体失败，不是新剧情，也不是扩写配额。修复后仍要做全章状态闭合；不得只改第一处、不得顺手重写正确段落。",
        "",
    ]
    for block in failed_gate.get("blocking_checks", []):
        obligation = by_id.get(block["obligation_id"])
        lines.append(f"## [{block['obligation_id']}] {obligation.kind.value if obligation else 'unknown'}")
        if obligation:
            lines.append(f"Source: {obligation.source_text}")
            lines.append(
                "Actor / Action / Object: "
                + " → ".join(part for part in (obligation.subject, obligation.action, obligation.object) if part)
            )
            lines.append(f"Boundary: {obligation.boundary}")
        lines.append(f"Gate failure: {block['reason']}")
        lines.append("")
    lines.extend(
        [
            "修复重点：冻结 Mission 要求分身携带并固定回潮楔，本体与分身必须分别改变两个位置；不能让本体替分身拿楔。回潮楔仍处于再次使用前必须散尽残压的 cooldown；不要求本章章末残压已经归零，但不能写成可连续硬压。",
            "",
            "固定输出仍只允许 `# 正式正文` 与完整最终正文。",
        ]
    )
    supplement = "\n".join(lines)
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    if authority_prompt.count(marker) != 1:
        raise RuntimeError("primary marker missing")
    prompt = authority_prompt.replace(marker, supplement + "\n\n" + marker, 1)
    prompt_path = OUT / "atomic_full_fallback_prompt.md"
    output_path = OUT / "atomic_full_fallback_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    final = body(response)
    (OUT / "atomic_full_fallback_response.md").write_text(response + "\n", encoding="utf-8")
    (OUT / "final_body.md").write_text(final + "\n", encoding="utf-8")
    gate = validate_candidate(
        pack,
        primary_body=primary,
        final_body=final,
        operations=infer_diff_operations(primary, final),
    )
    (OUT / "gate.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    repeat_summary = json.loads((ATOMIC / "phase-c2-atomic-delta-repeat2" / "summary.json").read_text(encoding="utf-8"))
    repeat_row = next(row for row in repeat_summary["rows"] if row["chapter"] == 16)
    delta_wall = float(repeat_row["delta_wall_seconds"])
    fallback_wall = float(data.get("wall_seconds") or 0)
    control_wall = float(repeat_row["control_full_reviser_seconds"])
    effective = delta_wall + fallback_wall
    summary = {
        "chapter": 16,
        "delta_wall_seconds": delta_wall,
        "atomic_full_fallback_wall_seconds": fallback_wall,
        "effective_route_seconds": round(effective, 3),
        "control_full_reviser_seconds": control_wall,
        "fallback_adjusted_speedup_percent": round((1 - effective / control_wall) * 100, 2),
        "gate_decision": gate["decision"],
        "blocking_ids": [item["obligation_id"] for item in gate.get("blocking_checks", [])],
        "final_chars": len(final),
        "usage": data.get("result", {}).get("usage", {}),
    }
    (ATOMIC / "phase-e-atomic-full-fallback" / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
