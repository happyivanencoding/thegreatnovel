from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
OUT = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-g2-all20-shadow-corrected"

sys.path.insert(0, str(ROOT / "temps"))
from atomic_chapter_obligations import body, compile_obligations, infer_diff_operations, save_pack, validate_candidate


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for chapter in range(1, 21):
        source = SOURCE / f"chapter-{chapter:04d}"
        primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
        final = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
        pack = compile_obligations(
            chapter=chapter,
            authority_prompt=(source / "authority_reviser_prompt.md").read_text(encoding="utf-8"),
            curator_response=(source / "curator_response.md").read_text(encoding="utf-8"),
            primary_body=primary,
        )
        gate = validate_candidate(pack, primary_body=primary, final_body=final, operations=infer_diff_operations(primary, final))
        target = OUT / f"chapter-{chapter:04d}"
        save_pack(pack, target / "obligation_pack.json")
        (target / "full_gate.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rows.append({
            "chapter": chapter,
            "protagonist": pack.protagonist,
            "preflight_eligible": pack.preflight_eligible,
            "obligation_count": len(pack.obligations),
            "unsupported_count": len(pack.unsupported_clauses),
            "unsupported": pack.unsupported_clauses,
            "source_conflict_count": len(pack.source_conflicts),
            "source_conflicts": pack.source_conflicts,
            "historical_full_gate": gate["decision"],
            "blocking_ids": [item["obligation_id"] for item in gate.get("blocking_checks", [])],
            "blocking_reasons": [item["reason"] for item in gate.get("blocking_checks", [])],
        })
    eligible = [row for row in rows if row["preflight_eligible"]]
    summary = {
        "version": "atomic-obligations-v0.3-boundary-calibrated",
        "chapters": len(rows),
        "preflight_eligible": len(eligible),
        "preflight_fail_closed": len(rows) - len(eligible),
        "eligible_historical_full_pass": sum(row["historical_full_gate"] == "ADOPT_DELTA" for row in eligible),
        "eligible_historical_full_blocked": sum(row["historical_full_gate"] != "ADOPT_DELTA" for row in eligible),
        "all_historical_full_pass": sum(row["historical_full_gate"] == "ADOPT_DELTA" for row in rows),
        "all_historical_full_blocked": sum(row["historical_full_gate"] != "ADOPT_DELTA" for row in rows),
        "rows": rows,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
