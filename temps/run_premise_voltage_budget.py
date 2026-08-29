from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-premise-aperture-20260829-v1"
RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.premise_aperture import (  # noqa: E402
    build_voltage_budget_prompt,
    extract_sections,
    validate_voltage_budget_locks,
)


@dataclass(frozen=True)
class Case:
    case_id: str


CASES = (
    Case("generic_fantasy"),
    Case("fast_multiworld"),
    Case("game_instance"),
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def run_one(case: Case) -> dict[str, object]:
    case_dir = EXP / case.case_id
    axes_dir = case_dir / "orthogonal" / "axes"
    pools = {
        "world": extract_sections(read(axes_dir / "world" / "response.md"), prefix="W"),
        "ontology": extract_sections(read(axes_dir / "ontology" / "response.md"), prefix="O"),
        "privilege": extract_sections(read(axes_dir / "privilege" / "response.md"), prefix="P"),
        "interface": extract_sections(read(axes_dir / "interface" / "response.md"), prefix="I"),
    }
    for axis, pool in pools.items():
        if len(pool) != 3:
            raise RuntimeError(f"{case.case_id} {axis}: expected 3 sparks, got {tuple(pool)}")

    out_dir = case_dir / "orthogonal" / "voltage_budget_2"
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_voltage_budget_prompt(
        author_direction=read(case_dir / "AUTHOR_DIRECTION.md"),
        world_sparks=pools["world"],
        ontology_sparks=pools["ontology"],
        privilege_sparks=pools["privilege"],
        interface_sparks=pools["interface"],
    )
    prompt_path = out_dir / "prompt.md"
    out_json = out_dir / "acp.json"
    response_path = out_dir / "response.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    label = f"premise-voltage-budget-{case.case_id}"
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_json), "gpt-5.6-luna", "high", label],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if cp.returncode:
        raise RuntimeError(f"{label}: {cp.stderr[-2500:]}")
    data = json.loads(out_json.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"{label}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    response_path.write_text(text + "\n", encoding="utf-8")
    sections = extract_sections(text, prefix="V")
    if len(sections) != 3:
        raise RuntimeError(f"{label}: expected V1/V2/V3, got {tuple(sections)}")
    missing = validate_voltage_budget_locks(
        text,
        world_sparks=pools["world"],
        ontology_sparks=pools["ontology"],
        privilege_sparks=pools["privilege"],
        interface_sparks=pools["interface"],
    )
    return {
        "case": case.case_id,
        "wall_seconds": data.get("wall_seconds"),
        "chars": len(text),
        "candidate_ids": list(sections),
        "missing_locked_cores": missing,
    }


def main() -> None:
    protocol = """# Asymmetric Voltage Budget Experiment

- Reuses the exact fresh-context axis outputs from the four-axis experiment; no new axis sampling.
- Each candidate locks exactly two high-voltage cores.
- V1 = W1 + P2, standard human, no special Interface.
- V2 = O3 + P1, familiar concrete world, no special Interface.
- V3 = W3 + I3, standard human, special Power deferred.
- Pairing and low-voltage rules are deterministic in code before outputs.
- Same Luna-high model as prior collision.
- Production default remains unchanged.
"""
    (EXP / "VOLTAGE_BUDGET_PROTOCOL.md").write_text(protocol, encoding="utf-8")
    summaries: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_one, case): case.case_id for case in CASES}
        for future in as_completed(futures):
            result = future.result()
            summaries.append(result)
            print("DONE", result, flush=True)
    (EXP / "VOLTAGE_BUDGET_SUMMARY.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
