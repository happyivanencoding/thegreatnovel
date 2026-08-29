from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
OLD = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-b-calibration"
OUT = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-b2-calibration-corrected"

sys.path.insert(0, str(ROOT / "temps"))
from atomic_chapter_obligations import body, compile_obligations, infer_diff_operations, save_pack, validate_candidate


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mutation_rows = []
    shadow_rows = []
    chapter_dirs = sorted(path for path in OLD.glob("chapter-*") if path.is_dir())
    for old_dir in chapter_dirs:
        chapter = int(old_dir.name.split("-")[-1])
        source = SOURCE / old_dir.name
        required = [source / "authority_reviser_prompt.md", source / "curator_response.md", source / "primary_response.md", source / "authority_reviser_response.md"]
        if not all(path.exists() for path in required):
            continue
        primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
        full = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
        pack = compile_obligations(
            chapter=chapter,
            authority_prompt=(source / "authority_reviser_prompt.md").read_text(encoding="utf-8"),
            curator_response=(source / "curator_response.md").read_text(encoding="utf-8"),
            primary_body=primary,
        )
        target = OUT / old_dir.name
        save_pack(pack, target / "obligation_pack.json")

        full_gate = validate_candidate(
            pack,
            primary_body=primary,
            final_body=full,
            operations=infer_diff_operations(primary, full),
        )
        (target / "shadow-full-gate.json").write_text(json.dumps(full_gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        shadow_rows.append({
            "chapter": chapter,
            "label": "SHADOW_CONTROL_NOT_GOLD",
            "decision": full_gate["decision"],
            "blocking_ids": [item["obligation_id"] for item in full_gate.get("blocking_checks", [])],
            "blocking_reasons": [item["reason"] for item in full_gate.get("blocking_checks", [])],
        })

        for mutation in sorted(old_dir.glob("mut-*.md")):
            candidate = mutation.read_text(encoding="utf-8").strip()
            gate = validate_candidate(
                pack,
                primary_body=primary,
                final_body=candidate,
                operations=infer_diff_operations(primary, candidate),
            )
            name = mutation.stem
            (target / f"gate-{name}.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            mutation_rows.append({
                "chapter": chapter,
                "mutation": name,
                "expected": "FALLBACK_FULL_REVISER",
                "decision": gate["decision"],
                "detected": gate["decision"] == "FALLBACK_FULL_REVISER",
                "blocking_ids": [item["obligation_id"] for item in gate.get("blocking_checks", [])],
                "blocking_reasons": [item["reason"] for item in gate.get("blocking_checks", [])],
            })

    summary = {
        "version": "atomic-obligations-v0.3-boundary-calibrated",
        "calibration_policy": {
            "mutation_rows": "KNOWN_BAD recall only",
            "historical_full_rows": "SHADOW_CONTROL_NOT_GOLD; not counted as safe precision",
            "controlled_safe_boundaries": "covered by temps/test_atomic_chapter_obligations.py",
        },
        "mutation_total": len(mutation_rows),
        "mutation_detected": sum(row["detected"] for row in mutation_rows),
        "mutation_missed": sum(not row["detected"] for row in mutation_rows),
        "shadow_control_total": len(shadow_rows),
        "shadow_control_pass": sum(row["decision"] == "ADOPT_DELTA" for row in shadow_rows),
        "shadow_control_blocked": sum(row["decision"] != "ADOPT_DELTA" for row in shadow_rows),
        "mutation_rows": mutation_rows,
        "shadow_rows": shadow_rows,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key not in {"mutation_rows", "shadow_rows"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
