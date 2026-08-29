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
    DEFAULT_COLLISION_MATRIX,
    build_axis_prompt,
    build_collision_prompt,
    build_lane_bundle,
    build_single_pass_prompt,
    extract_sections,
    render_lane_direction,
    validate_collision_locks,
)


@dataclass(frozen=True)
class Case:
    case_id: str
    root: Path
    direction_rel: str
    baseline_rels: tuple[str, ...]


CASES = (
    Case(
        "generic_fantasy",
        ROOT / "books" / "real-exp-personality-advantage-tree-20260827-v1",
        "AUTHOR_DIRECTION.md",
        (
            "WORLD_VISION.md",
            "POWER_SEED.md",
            "human_3/HUMAN_SEED.md",
            "human_3/STORY_PROGRAM.md",
        ),
    ),
    Case(
        "fast_multiworld",
        ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1",
        "AUTHOR_DIRECTION.md",
        ("WORLD_VISION.md", "POWER_SEED.md", "HUMAN_SEED.md", "STORY_PROGRAM.md"),
    ),
    Case(
        "game_instance",
        ROOT / "books" / "real-exp-game-instance-5ch-20260829-v1",
        "AUTHOR_DIRECTION.md",
        ("WORLD_VISION.md", "POWER_SEED.md", "HUMAN_SEED.md", "STORY_PROGRAM.md"),
    ),
)

AXES = ("world", "ontology", "privilege", "interface")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def run_one(
    prompt_path: Path,
    out_json: Path,
    response_path: Path,
    *,
    label: str,
    model: str = "gpt-5.6-luna",
    effort: str = "high",
) -> dict[str, object]:
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, label],
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
    return {
        "label": label,
        "model": model,
        "effort": effort,
        "wall_seconds": data.get("wall_seconds"),
        "chars": len(text),
    }


def prepare_case(case: Case) -> list[tuple[Path, Path, Path, str]]:
    case_dir = EXP / case.case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    direction = read(case.root / case.direction_rel)
    (case_dir / "AUTHOR_DIRECTION.md").write_text(direction + "\n", encoding="utf-8")

    baseline_parts = ["# CURRENT PRODUCTION BASELINE", "", f"Source: `{case.root}`"]
    for rel in case.baseline_rels:
        path = case.root / rel
        if not path.exists():
            raise FileNotFoundError(f"baseline artifact missing: {path}")
        baseline_parts.extend(("", f"## {rel}", "", read(path)))
    (case_dir / "CURRENT_BASELINE_PACKAGE.md").write_text(
        "\n".join(baseline_parts).strip() + "\n", encoding="utf-8"
    )

    jobs: list[tuple[Path, Path, Path, str]] = []
    single_dir = case_dir / "single_pass"
    single_dir.mkdir(exist_ok=True)
    single_prompt = build_single_pass_prompt(author_direction=direction)
    single_prompt_path = single_dir / "prompt.md"
    single_prompt_path.write_text(single_prompt, encoding="utf-8")
    jobs.append(
        (
            single_prompt_path,
            single_dir / "acp.json",
            single_dir / "response.md",
            f"premise-aperture-{case.case_id}-single",
        )
    )

    axes_dir = case_dir / "orthogonal" / "axes"
    axes_dir.mkdir(parents=True, exist_ok=True)
    for axis in AXES:
        axis_dir = axes_dir / axis
        axis_dir.mkdir(exist_ok=True)
        prompt = build_axis_prompt(axis=axis, author_direction=direction)  # type: ignore[arg-type]
        prompt_path = axis_dir / "prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        jobs.append(
            (
                prompt_path,
                axis_dir / "acp.json",
                axis_dir / "response.md",
                f"premise-aperture-{case.case_id}-{axis}",
            )
        )
    return jobs


def build_collision(case: Case) -> tuple[Path, Path, Path, str]:
    case_dir = EXP / case.case_id
    direction = read(case_dir / "AUTHOR_DIRECTION.md")
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

    collision_dir = case_dir / "orthogonal" / "collision"
    collision_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_collision_prompt(
        author_direction=direction,
        world_sparks=pools["world"],
        ontology_sparks=pools["ontology"],
        privilege_sparks=pools["privilege"],
        interface_sparks=pools["interface"],
    )
    prompt_path = collision_dir / "prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    return (
        prompt_path,
        collision_dir / "acp.json",
        collision_dir / "response.md",
        f"premise-aperture-{case.case_id}-collision",
    )


def finalize_case(case: Case) -> dict[str, object]:
    case_dir = EXP / case.case_id
    axes_dir = case_dir / "orthogonal" / "axes"
    pools = {
        "world": extract_sections(read(axes_dir / "world" / "response.md"), prefix="W"),
        "ontology": extract_sections(read(axes_dir / "ontology" / "response.md"), prefix="O"),
        "privilege": extract_sections(read(axes_dir / "privilege" / "response.md"), prefix="P"),
        "interface": extract_sections(read(axes_dir / "interface" / "response.md"), prefix="I"),
    }
    single_sections = extract_sections(read(case_dir / "single_pass" / "response.md"), prefix="S")
    if len(single_sections) != 3:
        raise RuntimeError(f"{case.case_id} single: expected 3 candidates, got {tuple(single_sections)}")

    collision_text = read(case_dir / "orthogonal" / "collision" / "response.md")
    collision_sections = extract_sections(collision_text, prefix="C")
    if len(collision_sections) != 3:
        raise RuntimeError(f"{case.case_id} collision: expected 3 candidates, got {tuple(collision_sections)}")
    missing_locks = validate_collision_locks(
        collision_text,
        world_sparks=pools["world"],
        ontology_sparks=pools["ontology"],
        privilege_sparks=pools["privilege"],
        interface_sparks=pools["interface"],
    )

    selected = DEFAULT_COLLISION_MATRIX[1]  # pre-registered: C2, no post-hoc cherry-pick
    bundle = build_lane_bundle(
        selected=selected,
        collision_text=collision_text,
        world_sparks=pools["world"],
        ontology_sparks=pools["ontology"],
        privilege_sparks=pools["privilege"],
        interface_sparks=pools["interface"],
    )
    lane_dir = case_dir / "orthogonal" / "selected_C2_lane_projection"
    lane_dir.mkdir(parents=True, exist_ok=True)
    for lane in ("world", "power", "human", "story"):
        (lane_dir / f"{lane.upper()}_DIRECTION.md").write_text(
            render_lane_direction(bundle, lane=lane) + "\n",  # type: ignore[arg-type]
            encoding="utf-8",
        )
    (lane_dir / "SELECTED_COLLISION.md").write_text(bundle.collision + "\n", encoding="utf-8")
    (case_dir / "single_pass" / "SELECTED_S2.md").write_text(
        single_sections["S2"] + "\n", encoding="utf-8"
    )

    return {
        "case": case.case_id,
        "single_candidate_ids": list(single_sections),
        "collision_candidate_ids": list(collision_sections),
        "missing_locked_cores": missing_locks,
        "pre_registered_downstream_selection": "C2",
        "single_chars": len(read(case_dir / "single_pass" / "response.md")),
        "collision_chars": len(collision_text),
    }


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    protocol = """# Premise Aperture A/B Protocol

- Date: 2026-08-29
- Production default remains unchanged.
- Three frozen existing author directions: generic fantasy, fast multiworld, game instance.
- A0: existing current production artifacts, copied without regeneration.
- A1: one fresh Luna-high single-agent Premise Forge call.
- B: four fresh isolated Luna-high axis calls (World / Ontology / Privilege / Interface), followed by one Luna-high collision call.
- Same model and effort for A1/B; B pairing is deterministic in code, not model-selected.
- Collision must preserve all four Core lines verbatim; code reports any smoothing.
- For any downstream preservation experiment, C2 is pre-registered before outputs are inspected. S2 is the single-agent comparison counterpart.
- No model judge, selector, reviewer, production Authority write, Outline or chapter generation in this script.
"""
    (EXP / "PROTOCOL.md").write_text(protocol, encoding="utf-8")

    phase1_jobs: list[tuple[Path, Path, Path, str]] = []
    for case in CASES:
        phase1_jobs.extend(prepare_case(case))

    results: list[dict[str, object]] = []
    print(f"PHASE 1: {len(phase1_jobs)} independent calls", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(run_one, p, o, r, label=label): label
            for p, o, r, label in phase1_jobs
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print("DONE", result, flush=True)

    collision_jobs = [build_collision(case) for case in CASES]
    print(f"PHASE 2: {len(collision_jobs)} fixed collision calls", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(run_one, p, o, r, label=label): label
            for p, o, r, label in collision_jobs
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print("DONE", result, flush=True)

    case_summaries = [finalize_case(case) for case in CASES]
    (EXP / "RUN_SUMMARY.json").write_text(
        json.dumps(
            {"calls": results, "cases": case_summaries},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps(case_summaries, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
