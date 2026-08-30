from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(r"C:\dev\tgn-story-mvp-native-e2e")
BASE = ROOT / "books" / "real-exp-native-structured-e2e-20260830-v1"
TREATMENTS = ("e2e-run4", "e2e-run5")
CONTROLS = ("fresh-control-3", "fresh-control-4")
SAMPLES = ("jiuchui_ch14", "jiuchui_ch16", "shadow_ch4", "shadow_ch9")
NODES = ("director", "curator", "primary", "reviser")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_fact_set(contract: dict[str, Any]) -> set[str]:
    rows = []
    for fact in contract["facts"]:
        clean = {
            key: value
            for key, value in fact.items()
            if key not in {"fact_id", "source_ref"}
        }
        rows.append(json.dumps(clean, ensure_ascii=False, sort_keys=True))
    return set(rows)


def mean(values):
    return statistics.mean(values)


def treatment_summary(run: str) -> dict[str, Any]:
    return load(BASE / run / "summary.json")


def control_summary(run: str) -> dict[str, Any]:
    return load(BASE / run / "summary.json")


def treatment_row(run: str, sample: str) -> dict[str, Any]:
    return next(row for row in treatment_summary(run)["rows"] if row["sample"] == sample)


def control_row(run: str, sample: str) -> dict[str, Any]:
    return next(row for row in control_summary(run)["rows"] if row["sample"] == sample)


def control_node(row: dict[str, Any], node: str) -> float:
    return float(next(item for item in row["nodes"] if item["node"] == node)["wall_seconds"])


def main() -> None:
    missing = [str(BASE / run / "summary.json") for run in (*TREATMENTS, *CONTROLS) if not (BASE / run / "summary.json").exists()]
    if missing:
        raise SystemExit("missing final summaries: " + ", ".join(missing))

    treatment_totals = [float(treatment_summary(run)["treatment_full_e2e_total_seconds"]) for run in TREATMENTS]
    control_totals = [float(control_summary(run)["total_seconds"]) for run in CONTROLS]
    tmean, cmean = mean(treatment_totals), mean(control_totals)

    node_analysis = {}
    treatment_field = {
        "director": "effective_director_seconds",
        "curator": "curator_seconds",
        "primary": "primary_seconds",
        "reviser": "reviser_seconds",
    }
    for node in NODES:
        t_runs = [sum(float(row[treatment_field[node]]) for row in treatment_summary(run)["rows"]) for run in TREATMENTS]
        c_runs = [float(control_summary(run)["by_node_seconds"][node]) for run in CONTROLS]
        tm, cm = mean(t_runs), mean(c_runs)
        node_analysis[node] = {
            "treatment_run_seconds": t_runs,
            "control_run_seconds": c_runs,
            "treatment_mean_seconds": round(tm, 3),
            "control_mean_seconds": round(cm, 3),
            "seconds_saved_mean": round(cm - tm, 3),
            "percent_saved_mean": round((1 - tm / cm) * 100, 2),
            "per_chapter_seconds_saved_mean": round((cm - tm) / len(SAMPLES), 3),
        }

    paired = []
    for treatment, control in zip(TREATMENTS, CONTROLS):
        tt = float(treatment_summary(treatment)["treatment_full_e2e_total_seconds"])
        ct = float(control_summary(control)["total_seconds"])
        paired.append({
            "treatment": treatment,
            "control": control,
            "treatment_seconds": tt,
            "control_seconds": ct,
            "seconds_saved": round(ct - tt, 3),
            "percent_saved": round((1 - tt / ct) * 100, 2),
        })

    per_sample = []
    for sample in SAMPLES:
        tvals = [float(treatment_row(run, sample)["treatment_full_total_seconds"]) for run in TREATMENTS]
        cvals = [float(control_row(run, sample)["total_seconds"]) for run in CONTROLS]
        tm, cm = mean(tvals), mean(cvals)
        per_sample.append({
            "sample": sample,
            "treatment_seconds": tvals,
            "control_seconds": cvals,
            "treatment_mean_seconds": round(tm, 3),
            "control_mean_seconds": round(cm, 3),
            "seconds_saved_mean": round(cm - tm, 3),
            "percent_saved_mean": round((1 - tm / cm) * 100, 2),
        })

    repeat_rows = []
    for sample in SAMPLES:
        a = BASE / TREATMENTS[0] / sample
        b = BASE / TREATMENTS[1] / sample
        contract_a = load(a / "native_atomic_contract.json")
        contract_b = load(b / "native_atomic_contract.json")
        repeat_rows.append({
            "sample": sample,
            "raw_decision_exact": sha(a / "native_director_raw_decision.json") == sha(b / "native_director_raw_decision.json"),
            "normalized_decision_exact": sha(a / "native_director_decision.json") == sha(b / "native_director_decision.json"),
            "hard_contract_exact": contract_a["contract_hash"] == contract_b["contract_hash"],
            "semantic_hard_fact_set_exact": semantic_fact_set(contract_a) == semantic_fact_set(contract_b),
            "rendered_mission_exact": sha(a / "effective_director_mission.md") == sha(b / "effective_director_mission.md"),
            "curator_exact": sha(a / "curator_response.md") == sha(b / "curator_response.md"),
            "primary_exact": sha(a / "primary_body.md") == sha(b / "primary_body.md"),
            "final_exact": sha(a / "final_body.md") == sha(b / "final_body.md"),
            "run4_route": treatment_row(TREATMENTS[0], sample)["director_source"],
            "run5_route": treatment_row(TREATMENTS[1], sample)["director_source"],
            "run4_coverage": treatment_row(TREATMENTS[0], sample)["native_structural_coverage"]["coverage"],
            "run5_coverage": treatment_row(TREATMENTS[1], sample)["native_structural_coverage"]["coverage"],
        })

    entity_kind_counts = Counter()
    fact_kind_counts = Counter()
    source_counts = Counter()
    action_ids = set()
    total_entities = 0
    total_facts = 0
    for sample in SAMPLES:
        contract = load(BASE / TREATMENTS[0] / sample / "native_atomic_contract.json")
        decision = load(BASE / TREATMENTS[0] / sample / "native_director_decision.json")
        for entity in contract["registry"]["entities"]:
            entity_kind_counts[entity["kind"]] += 1
            total_entities += 1
        for fact in contract["facts"]:
            fact_kind_counts[fact["kind"]] += 1
            source_counts[fact["source"]] += 1
            total_facts += 1
        action_ids.update(clause["action_id"] for clause in decision["clauses"])

    accepted_attempts = sum(
        treatment_row(run, sample)["director_source"] == "native_structured"
        for run in TREATMENTS for sample in SAMPLES
    )
    fallback_attempts = len(TREATMENTS) * len(SAMPLES) - accepted_attempts
    expected_facts = sum(
        int(treatment_row(run, sample)["native_structural_coverage"]["expected"])
        for run in TREATMENTS for sample in SAMPLES
    )
    matched_facts = sum(
        int(treatment_row(run, sample)["native_structural_coverage"]["matched"])
        for run in TREATMENTS for sample in SAMPLES
    )
    normalization_count = sum(
        int(treatment_row(run, sample).get("runtime_normalization_count", 0))
        for run in TREATMENTS for sample in SAMPLES
    )

    blind_path = BASE / "blinds-final-clean-v2b" / "summary.json"
    blind = load(blind_path) if blind_path.exists() else None

    analysis = {
        "schema_version": "native-structured-e2e-v2-final-analysis",
        "protocol_freeze": load(BASE / "PROTOCOL_FREEZE_V2.json"),
        "timing": {
            "treatment_run_totals_seconds": treatment_totals,
            "control_run_totals_seconds": control_totals,
            "treatment_mean_seconds": round(tmean, 3),
            "control_mean_seconds": round(cmean, 3),
            "mean_seconds_saved": round(cmean - tmean, 3),
            "mean_percent_saved": round((1 - tmean / cmean) * 100, 2),
            "mean_seconds_per_chapter_saved": round((cmean - tmean) / len(SAMPLES), 3),
            "treatment_range_seconds": [min(treatment_totals), max(treatment_totals)],
            "control_range_seconds": [min(control_totals), max(control_totals)],
            "paired_adjacent_runs": paired,
            "nodes": node_analysis,
            "per_sample": per_sample,
            "deterministic_projection_median_ms_previous_benchmark": 1.7005,
        },
        "fallback_adjusted": {
            "final_attempts": len(TREATMENTS) * len(SAMPLES),
            "native_accepted": accepted_attempts,
            "fallbacks": fallback_attempts,
            "final_timing_includes_discarded_native_plus_fallback_when_present": True,
            "v1_empirical_fallback_reference": {
                "run": "e2e-run3",
                "fallbacks": int(treatment_summary("e2e-run3")["director_fallbacks"]) if (BASE / "e2e-run3" / "summary.json").exists() else None,
                "note": "v1 is failure evidence only; excluded from v2 quality/time means",
            },
        },
        "repeatability": {
            "samples": len(SAMPLES),
            "raw_decision_exact": sum(row["raw_decision_exact"] for row in repeat_rows),
            "normalized_decision_exact": sum(row["normalized_decision_exact"] for row in repeat_rows),
            "hard_contract_exact": sum(row["hard_contract_exact"] for row in repeat_rows),
            "semantic_hard_fact_set_exact": sum(row["semantic_hard_fact_set_exact"] for row in repeat_rows),
            "rendered_mission_exact": sum(row["rendered_mission_exact"] for row in repeat_rows),
            "curator_exact": sum(row["curator_exact"] for row in repeat_rows),
            "primary_exact": sum(row["primary_exact"] for row in repeat_rows),
            "final_exact": sum(row["final_exact"] for row in repeat_rows),
            "rows": repeat_rows,
        },
        "cross_book_registry_coverage": {
            "books": 2,
            "chapters": 4,
            "attempts": 8,
            "native_accepted": accepted_attempts,
            "expected_hard_facts": expected_facts,
            "matched_hard_facts": matched_facts,
            "structural_coverage": round(matched_facts / max(1, expected_facts), 4),
            "runtime_normalization_count": normalization_count,
            "registry_entity_instances": total_entities,
            "entity_kind_counts": dict(sorted(entity_kind_counts.items())),
            "contract_fact_instances": total_facts,
            "fact_kind_counts": dict(sorted(fact_kind_counts.items())),
            "authority_source_counts": dict(sorted(source_counts.items())),
            "unique_action_ids": len(action_ids),
            "manual_registry_and_catalog": True,
            "automatic_long_novel_registry_proven": False,
        },
        "blind": blind,
    }
    (BASE / "FINAL_ANALYSIS_V2.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with (BASE / "TIMING_TABLE_V2.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["route", "run", "sample", "director_s", "curator_s", "primary_s", "reviser_s", "total_s", "fallback"])
        for run in TREATMENTS:
            for sample in SAMPLES:
                row = treatment_row(run, sample)
                writer.writerow(["native", run, sample, row["effective_director_seconds"], row["curator_seconds"], row["primary_seconds"], row["reviser_seconds"], row["treatment_full_total_seconds"], row["director_source"] != "native_structured"])
        for run in CONTROLS:
            for sample in SAMPLES:
                row = control_row(run, sample)
                writer.writerow(["control", run, sample, control_node(row, "director"), control_node(row, "curator"), control_node(row, "primary"), control_node(row, "reviser"), row["total_seconds"], False])

    (BASE / "REPEATABILITY_V2.json").write_text(json.dumps(analysis["repeatability"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "REGISTRY_COVERAGE_V2.json").write_text(json.dumps(analysis["cross_book_registry_coverage"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "timing": analysis["timing"],
        "fallback_adjusted": analysis["fallback_adjusted"],
        "repeatability": {k: v for k, v in analysis["repeatability"].items() if k != "rows"},
        "coverage": analysis["cross_book_registry_coverage"],
        "blind_ready": blind is not None,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
