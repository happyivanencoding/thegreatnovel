from __future__ import annotations

import difflib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = (
    ROOT
    / "books"
    / "real-exp-reviser-noop-upstream-heldout-20260830-v1"
    / "heldout-new-novel-2"
)


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def edit_blocks(primary: str, final: str) -> int:
    matcher = difflib.SequenceMatcher(
        a=paragraphs(primary), b=paragraphs(final), autojunk=False
    )
    return sum(tag != "equal" for tag, *_ in matcher.get_opcodes())


def similarity(primary: str, final: str) -> float:
    return difflib.SequenceMatcher(a=primary, b=final, autojunk=False).ratio()


def generation_rows() -> list[dict]:
    rows: list[dict] = []
    for run in ("repeat1", "repeat2"):
        for chapter in range(1, 5):
            directory = (
                BASE / "runs" / f"chapter-{chapter:04d}"
                if run == "repeat1"
                else BASE / "repeat2" / f"chapter-{chapter:04d}"
            )
            if run == "repeat1":
                timing = json.loads((directory / "timing.json").read_text(encoding="utf-8"))
            else:
                summary = json.loads((BASE / "repeat2" / "summary.json").read_text(encoding="utf-8"))
                timing = {
                    f"{row['arm']}_primary": row["primary_wall"]
                    for row in summary["rows"]
                    if row["chapter"] == chapter
                }
                timing.update(
                    {
                        f"{row['arm']}_reviser": row["reviser_wall"]
                        for row in summary["rows"]
                        if row["chapter"] == chapter
                    }
                )
            for arm in ("control", "treatment"):
                primary = (directory / f"{arm}_primary_body.md").read_text(encoding="utf-8").strip()
                final = (directory / f"{arm}_final_body.md").read_text(encoding="utf-8").strip()
                rows.append(
                    {
                        "run": run,
                        "chapter": chapter,
                        "arm": arm,
                        "primary_chars": len(primary),
                        "final_chars": len(final),
                        "edit_blocks": edit_blocks(primary, final),
                        "similarity": round(similarity(primary, final), 4),
                        "exact_noop": primary == final,
                        "primary_wall": float(timing[f"{arm}_primary"]),
                        "reviser_wall": float(timing[f"{arm}_reviser"]),
                        "primary_plus_reviser_wall": round(
                            float(timing[f"{arm}_primary"])
                            + float(timing[f"{arm}_reviser"]),
                            3,
                        ),
                    }
                )
    return rows


def aggregate_generation(rows: list[dict]) -> dict:
    result: dict[str, dict] = {}
    for arm in ("control", "treatment"):
        group = [row for row in rows if row["arm"] == arm]
        result[arm] = {
            "samples": len(group),
            "primary_chars_mean": round(statistics.mean(row["primary_chars"] for row in group), 3),
            "edit_blocks_mean": round(statistics.mean(row["edit_blocks"] for row in group), 3),
            "similarity_mean": round(statistics.mean(row["similarity"] for row in group), 4),
            "exact_noop": sum(row["exact_noop"] for row in group),
            "primary_wall_mean": round(statistics.mean(row["primary_wall"] for row in group), 3),
            "reviser_wall_mean": round(statistics.mean(row["reviser_wall"] for row in group), 3),
            "primary_plus_reviser_wall_mean": round(
                statistics.mean(row["primary_plus_reviser_wall"] for row in group), 3
            ),
        }
    result["treatment_minus_control"] = {
        "primary_wall_seconds": round(
            result["treatment"]["primary_wall_mean"]
            - result["control"]["primary_wall_mean"],
            3,
        ),
        "reviser_wall_seconds": round(
            result["treatment"]["reviser_wall_mean"]
            - result["control"]["reviser_wall_mean"],
            3,
        ),
        "primary_plus_reviser_seconds": round(
            result["treatment"]["primary_plus_reviser_wall_mean"]
            - result["control"]["primary_plus_reviser_wall_mean"],
            3,
        ),
        "edit_blocks": round(
            result["treatment"]["edit_blocks_mean"]
            - result["control"]["edit_blocks_mean"],
            3,
        ),
        "similarity": round(
            result["treatment"]["similarity_mean"]
            - result["control"]["similarity_mean"],
            4,
        ),
    }
    return result


def aggregate_blind() -> tuple[dict, list[dict]]:
    blind = json.loads((BASE / "BLIND_SUMMARY.json").read_text(encoding="utf-8"))
    rows = blind["rows"]
    pairwise: dict[str, dict] = {}
    pairs = (
        ("treatment_primary", "control_primary", "treatment_primary_minus_control_primary"),
        ("control_reviser", "control_primary", "control_reviser_minus_control_primary"),
        ("treatment_reviser", "treatment_primary", "treatment_reviser_minus_treatment_primary"),
        ("treatment_reviser", "control_reviser", "treatment_reviser_minus_control_reviser"),
        ("treatment_primary", "control_reviser", "treatment_primary_minus_control_reviser"),
    )
    for judge in ("story", "authority"):
        group = [row for row in rows if row["judge"] == judge]
        pairwise[judge] = {}
        for left, right, label in pairs:
            deltas = [row["scores"][left] - row["scores"][right] for row in group]
            pairwise[judge][label] = {
                "mean_delta": round(statistics.mean(deltas), 3),
                "left_wins": sum(value > 0 for value in deltas),
                "right_wins": sum(value < 0 for value in deltas),
                "ties": sum(value == 0 for value in deltas),
            }
        if judge == "authority":
            pairwise[judge]["hard_problem_counts"] = {
                name: sum(len(row["hard_problems"].get(name, [])) for row in group)
                for name in (
                    "control_primary",
                    "treatment_primary",
                    "control_reviser",
                    "treatment_reviser",
                )
            }
    return {"aggregates": blind["aggregates"], "pairwise": pairwise}, rows


def per_chapter_repeat_consistency(blind_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for chapter in range(1, 5):
        for judge in ("story", "authority"):
            group = [
                row
                for row in blind_rows
                if row["chapter"] == chapter and row["judge"] == judge
            ]
            tp_minus_cp = [
                row["scores"]["treatment_primary"] - row["scores"]["control_primary"]
                for row in group
            ]
            tr_gap = [
                row["scores"]["treatment_reviser"] - row["scores"]["treatment_primary"]
                for row in group
            ]
            cr_gap = [
                row["scores"]["control_reviser"] - row["scores"]["control_primary"]
                for row in group
            ]
            rows.append(
                {
                    "chapter": chapter,
                    "judge": judge,
                    "judgments": len(group),
                    "treatment_primary_minus_control_primary_mean": round(
                        statistics.mean(tp_minus_cp), 3
                    ),
                    "control_reviser_gap_mean": round(statistics.mean(cr_gap), 3),
                    "treatment_reviser_gap_mean": round(statistics.mean(tr_gap), 3),
                    "gap_reduction": round(
                        statistics.mean(cr_gap) - statistics.mean(tr_gap), 3
                    ),
                }
            )
    return rows


def main() -> None:
    rows = generation_rows()
    generation = aggregate_generation(rows)
    blind, blind_rows = aggregate_blind()
    consistency = per_chapter_repeat_consistency(blind_rows)
    projection_chars = [
        len(
            (
                BASE / "runs" / f"chapter-{chapter:04d}" / "final_facts_projection.md"
            ).read_text(encoding="utf-8")
        )
        for chapter in range(1, 5)
    ]
    control_story_gap = blind["pairwise"]["story"]["control_reviser_minus_control_primary"]["mean_delta"]
    treatment_story_gap = blind["pairwise"]["story"]["treatment_reviser_minus_treatment_primary"]["mean_delta"]
    control_authority_gap = blind["pairwise"]["authority"]["control_reviser_minus_control_primary"]["mean_delta"]
    treatment_authority_gap = blind["pairwise"]["authority"]["treatment_reviser_minus_treatment_primary"]["mean_delta"]
    story_gap_closeness_to_zero = abs(control_story_gap) - abs(treatment_story_gap)
    authority_gap_closeness_to_zero = abs(control_authority_gap) - abs(treatment_authority_gap)
    success = {
        "story_primary_non_regression": blind["pairwise"]["story"]["treatment_primary_minus_control_primary"]["mean_delta"] >= -0.5,
        "authority_primary_improves_or_ties": blind["pairwise"]["authority"]["treatment_primary_minus_control_primary"]["mean_delta"] >= 0,
        "story_reviser_gap_closer_to_zero": story_gap_closeness_to_zero > 0,
        "authority_reviser_gap_closer_to_zero": authority_gap_closeness_to_zero > 0,
        "engineering_noop_improved": (
            generation["treatment"]["edit_blocks_mean"] <= generation["control"]["edit_blocks_mean"]
            and generation["treatment"]["similarity_mean"] >= generation["control"]["similarity_mean"]
            and generation["treatment"]["exact_noop"] >= generation["control"]["exact_noop"]
            and (
                generation["treatment"]["edit_blocks_mean"] < generation["control"]["edit_blocks_mean"]
                or generation["treatment"]["similarity_mean"] > generation["control"]["similarity_mean"]
                or generation["treatment"]["exact_noop"] > generation["control"]["exact_noop"]
            )
        ),
        "primary_wall_not_materially_slower": generation["treatment_minus_control"]["primary_wall_seconds"] <= 5,
        "treatment_final_story_non_regression": blind["pairwise"]["story"]["treatment_reviser_minus_control_reviser"]["mean_delta"] >= -0.5,
        "treatment_final_authority_non_regression": blind["pairwise"]["authority"]["treatment_reviser_minus_control_reviser"]["mean_delta"] >= -0.5,
    }
    success["all_directional_pass"] = all(success.values())
    result = {
        "schema_version": "heldout2-final-facts-analysis-v1",
        "candidate_protocol_sha256": "E11BEFFE12F5016CA1DFB362631D3145212437A21C20BCA360B7D540C5E692E4",
        "generation": generation,
        "projection_chars_mean": round(statistics.mean(projection_chars), 3),
        "blind": blind,
        "reviser_gap": {
            "story_control_signed": round(control_story_gap, 3),
            "story_treatment_signed": round(treatment_story_gap, 3),
            "story_closeness_to_zero_improvement": round(story_gap_closeness_to_zero, 3),
            "authority_control_signed": round(control_authority_gap, 3),
            "authority_treatment_signed": round(treatment_authority_gap, 3),
            "authority_closeness_to_zero_improvement": round(authority_gap_closeness_to_zero, 3),
        },
        "success": success,
        "per_chapter_repeat_consistency": consistency,
        "generation_rows": rows,
    }
    (BASE / "FINAL_ANALYSIS.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
