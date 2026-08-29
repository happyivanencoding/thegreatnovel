from __future__ import annotations

from pathlib import Path
import json
import re
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
SOURCE = BASE / "downstream_S2_compilable_v4"
EXP = BASE / "compilable_single_v5_repair"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "temps"))

from run_premise_aperture_downstream import clean, dump, read, run_acp  # noqa: E402
from story_mvp.premise_aperture import (  # noqa: E402
    build_premise_repair_prompt,
    build_selected_premise_compiler_prompt,
    extract_sections,
    normalize_single_candidate_response,
    validate_premise_repair,
)


def materialize_acp(json_path: Path, response_path: Path) -> str:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"{json_path.name}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    if not text:
        raise RuntimeError(f"{json_path.name}: empty text")
    response_path.write_text(text + "\n", encoding="utf-8")
    return text


def load_or_run(
    *,
    prompt_path: Path,
    json_path: Path,
    response_path: Path,
    model: str,
    label: str,
) -> str:
    if response_path.exists():
        return read(response_path)
    if json_path.exists():
        return materialize_acp(json_path, response_path)
    return str(
        run_acp(
            prompt_path,
            json_path,
            response_path,
            model=model,
            label=label,
        )["text"]
    )


def compiler_verdict(report: str) -> str:
    match = re.search(
        r"(?mi)^\s*-\s*Verdict:\s*(PASS|CONDITIONAL PASS|FAIL)\s*$",
        report,
    )
    if not match:
        raise RuntimeError("selected compiler report missing strict Verdict")
    return match.group(1).upper()


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    original = read(SOURCE / "SELECTED_PREMISE.md")
    compiler_report = read(BASE / "compilable_single_v4" / "AUDIT.md")
    sections = extract_sections(original, prefix="S")
    if tuple(sections) != ("S2",):
        raise RuntimeError(f"expected only preregistered S2, got {tuple(sections)}")
    compiler_sections = extract_sections(compiler_report, prefix="S")
    if "S2" not in compiler_sections:
        raise RuntimeError("source compiler report missing S2 section")
    selected_report = compiler_sections["S2"]

    protocol = """# Selected Premise Repair V5 Protocol

- Source is the preregistered V4 S2 `一城吞门`; no post-hoc candidate selection.
- The V4 independent compiler found four exact causal conflicts before any Authority call.
- One Luna-high repair call is allowed.
- Code locks the candidate title plus exact Shelf Promise, Ontology, Changed Verbs and three `不可磨平` items.
- Repair may change only causal fields needed to close the reported conflicts; it may not humanize, weaken the first payoff, or add a second premise-level bet.
- One independent Terra-high compiler recheck follows.
- Only a strict PASS may enter downstream Authority generation. CONDITIONAL PASS / FAIL stops.
- This is opening-time research only; production default is unchanged.
"""
    (EXP / "PROTOCOL.md").write_text(protocol, encoding="utf-8")
    (EXP / "ORIGINAL_SELECTED_S2.md").write_text(original + "\n", encoding="utf-8")
    (EXP / "SOURCE_COMPILER_REPORT.md").write_text(compiler_report + "\n", encoding="utf-8")
    (EXP / "SELECTED_S2_COMPILER_REPORT.md").write_text(
        selected_report + "\n", encoding="utf-8"
    )

    repair_prompt = build_premise_repair_prompt(
        candidate=original,
        compiler_report=selected_report,
    )
    (EXP / "REPAIR_PROMPT.md").write_text(repair_prompt, encoding="utf-8")
    repaired = load_or_run(
        prompt_path=EXP / "REPAIR_PROMPT.md",
        json_path=EXP / "REPAIR_ACP.json",
        response_path=EXP / "REPAIRED_S2.md",
        model="gpt-5.6-luna",
        label="premise-selected-S2-repair-v5",
    )
    repaired = normalize_single_candidate_response(text=repaired, expected_id="S2")
    (EXP / "REPAIRED_S2.md").write_text(repaired, encoding="utf-8")
    try:
        core_checks = validate_premise_repair(original=original, repaired=repaired)
    except ValueError as error:
        failure = {
            "case": "fast_multiworld/preregistered-S2-repair-v5",
            "source_verdict": "FAIL",
            "repair_calls": 1,
            "compiler_calls": 0,
            "protected_core_passed": False,
            "protected_core_error": str(error),
            "compiler_verdict": "SKIPPED",
            "downstream_authorized": False,
            "production_default_changed": False,
        }
        dump(
            EXP / "PROTECTED_CORE_VALIDATION.json",
            {"passed": False, "error": str(error)},
        )
        dump(EXP / "RUN_SUMMARY.json", failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2), flush=True)
        return
    dump(EXP / "PROTECTED_CORE_VALIDATION.json", {"passed": True, "checks": core_checks})

    compile_prompt = build_selected_premise_compiler_prompt(candidate=repaired)
    (EXP / "COMPILER_PROMPT.md").write_text(compile_prompt, encoding="utf-8")
    report = load_or_run(
        prompt_path=EXP / "COMPILER_PROMPT.md",
        json_path=EXP / "COMPILER_ACP.json",
        response_path=EXP / "COMPILER_REPORT.md",
        model="gpt-5.6-terra",
        label="premise-selected-S2-compiler-v5",
    )
    verdict = compiler_verdict(report)

    # Build a synthetic three-card response only for reuse of the existing
    # downstream harness. No S1/S3 is selected or modified.
    full_v4 = read(BASE / "compilable_single_v4" / "RESPONSE.md")
    pools = extract_sections(full_v4, prefix="S")
    if tuple(pools) != ("S1", "S2", "S3"):
        raise RuntimeError(f"source Forge expected S1/S2/S3, got {tuple(pools)}")
    synthetic = "# SINGLE-PASS PREMISE CANDIDATES\n\n" + "\n\n".join(
        (pools["S1"], repaired.strip(), pools["S3"])
    )
    (EXP / "REPAIRED_FORGE_RESPONSE.md").write_text(synthetic + "\n", encoding="utf-8")

    summary = {
        "case": "fast_multiworld/preregistered-S2-repair-v5",
        "source_verdict": "FAIL",
        "repair_calls": 1,
        "compiler_calls": 1,
        "protected_core_passed": True,
        "compiler_verdict": verdict,
        "downstream_authorized": verdict == "PASS",
        "production_default_changed": False,
    }
    dump(EXP / "RUN_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    if verdict != "PASS":
        raise RuntimeError(f"repair did not reach strict PASS: {verdict}")


if __name__ == "__main__":
    main()
