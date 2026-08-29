from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "paragraph-delta-reviser-crossbook"
OUT = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-f2-crossbook-static-corrected"
CHAPTERS = (1, 4, 6, 8, 10)

sys.path.insert(0, str(ROOT / "temps"))
from atomic_chapter_obligations import compile_obligations, load_operations, save_pack, validate_candidate


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for chapter in CHAPTERS:
        source = SOURCE / f"chapter-{chapter:04d}"
        prompt = (source / "paragraph_delta_prompt.md").read_text(encoding="utf-8")
        runtime = prompt[prompt.index("# Hybrid Runtime"):prompt.index("# NUMBERED PRIMARY DRAFT")].strip()
        curator_start = runtime.index("## CURATOR｜本章近端注意力与实现要求")
        world_start = runtime.index("## WORLD REALITY AUTHORITY｜远端安全世界事实")
        curator = runtime[curator_start:world_start].split("\n", 1)[1].strip()
        numbered = prompt.split("# NUMBERED PRIMARY DRAFT", 1)[1].strip()
        primary = "\n\n".join(
            re.sub(r"^P\d{3}:\s*", "", line.strip())
            for line in numbered.splitlines()
            if line.strip()
        )
        pack = compile_obligations(chapter=chapter, authority_prompt=runtime, curator_response=curator, primary_body=primary)
        delta = (source / "final_body.md").read_text(encoding="utf-8").strip()
        operations = load_operations(SOURCE / "summary.json", chapter)
        gate = validate_candidate(pack, primary_body=primary, final_body=delta, operations=operations)
        target = OUT / f"chapter-{chapter:04d}"
        save_pack(pack, target / "obligation_pack.json")
        (target / "gate.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rows.append({
            "chapter": chapter,
            "protagonist": pack.protagonist,
            "preflight_eligible": pack.preflight_eligible,
            "obligation_count": len(pack.obligations),
            "unsupported_count": len(pack.unsupported_clauses),
            "source_conflict_count": len(pack.source_conflicts),
            "delta_gate": gate["decision"],
            "blocking_ids": [item["obligation_id"] for item in gate.get("blocking_checks", [])],
            "blocking_reasons": [item["reason"] for item in gate.get("blocking_checks", [])],
        })
    summary = {
        "version": "atomic-obligations-v0.3-boundary-calibrated",
        "samples": len(rows),
        "preflight_eligible": sum(row["preflight_eligible"] for row in rows),
        "preflight_fail_closed": sum(not row["preflight_eligible"] for row in rows),
        "delta_adoptable": sum(row["delta_gate"] == "ADOPT_DELTA" for row in rows),
        "delta_blocked": sum(row["delta_gate"] != "ADOPT_DELTA" for row in rows),
        "rows": rows,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
