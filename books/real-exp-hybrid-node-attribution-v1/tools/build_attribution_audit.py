from __future__ import annotations

import difflib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "d4e2dd6f3377f967d8930480016f15a450b74e1b"
V2_ROOT = "books/real-exp-opening-pipeline-comparison-v2"
VERIFIED_ATTRIBUTION = {
    1: {"accepted_patch_count": 1, "change_class": "B_LOCAL_REPAIR_WITH_RHYTHM_REGRESSION"},
    2: {"accepted_patch_count": 1, "change_class": "C_DIALOGUE_AND_CHARACTER_REPAIR"},
    3: {"accepted_patch_count": 3, "change_class": "C_ACTION_CONTINUITY_AND_SPATIAL_REPAIR"},
}


def git_text(path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def extract_section(text: str, heading: str, stop_heading: str | None = None) -> str:
    lines = text.splitlines()
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == heading)
    except StopIteration as error:
        raise ValueError(f"missing heading: {heading}") from error
    end = len(lines)
    if stop_heading:
        for index in range(start + 1, len(lines)):
            if lines[index].strip() == stop_heading:
                end = index
                break
    return "\n".join(lines[start + 1 : end]).strip()


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def diff_metrics(primary: str, final: str) -> dict[str, Any]:
    char_matcher = difflib.SequenceMatcher(None, primary, final, autojunk=False)
    changed_chars = 0
    for tag, old_start, old_end, new_start, new_end in char_matcher.get_opcodes():
        if tag != "equal":
            changed_chars += (old_end - old_start) + (new_end - new_start)

    old_paragraphs = paragraphs(primary)
    new_paragraphs = paragraphs(final)
    paragraph_matcher = difflib.SequenceMatcher(None, old_paragraphs, new_paragraphs, autojunk=False)
    changed_paragraphs = 0
    for tag, old_start, old_end, new_start, new_end in paragraph_matcher.get_opcodes():
        if tag != "equal":
            changed_paragraphs += max(old_end - old_start, new_end - new_start)

    return {
        "primary_chars": len(primary),
        "final_chars": len(final),
        "textual_diff_size": changed_chars,
        "changed_paragraph_count": changed_paragraphs,
        "primary_paragraphs": len(old_paragraphs),
        "final_paragraphs": len(new_paragraphs),
        "final_equals_primary": primary == final,
    }


def patch_blocks(text: str) -> list[dict[str, str | int]]:
    lines = text.splitlines()
    starts = [
        (index, int(match.group(1)))
        for index, line in enumerate(lines)
        if (match := re.match(r"^##\s+Patch\s+(\d+)\s*$", line.strip()))
    ]
    blocks: list[dict[str, str | int]] = []
    for position, (start, number) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        blocks.append({"number": number, "text": "\n".join(lines[start:end]).strip()})
    return blocks


def chapter_record(number: int) -> dict[str, Any]:
    chapter = f"chapter-{number:04d}"
    base = f"{V2_ROOT}/candidate-c"
    primary_path = f"{base}/runs/{chapter}/primary_response.md"
    final_path = f"{base}/runs/{chapter}/final_formal_prose.md"
    integrator_path = f"{base}/runs/{chapter}/integrator_response.md"
    manifest_path = f"{base}/runs/{chapter}/manifest.json"
    execution_path = f"{base}/runs/{chapter}/execution.json"
    selected_path = f"{base}/_operation/{chapter}/selected_specialists.md"

    primary_response = git_text(primary_path)
    primary = extract_section(primary_response, "# Primary Draft", "# Primary Fact Summary")
    final = git_text(final_path).strip()
    manifest = json.loads(git_text(manifest_path))
    execution = json.loads(git_text(execution_path))
    selected = git_text(selected_path).strip().splitlines()
    selected = [line.strip() for line in selected if line.strip()]

    specialist_paths: dict[str, str] = {}
    specialist_payloads: dict[str, str] = {}
    for node in ("opening", "dialogue", "action", "emotion"):
        path = f"{base}/runs/{chapter}/{node}_response.md"
        try:
            content = git_text(path)
        except subprocess.CalledProcessError:
            continue
        specialist_paths[node] = path
        specialist_payloads[node] = content

    metrics = diff_metrics(primary, final)
    completed_specialists = [
        node
        for node in ("opening", "dialogue", "action", "emotion")
        if manifest.get("nodes", {}).get(node, {}).get("status") in {"completed", "adopted"}
    ]
    proposed_patches = [
        {"specialist": node, **patch}
        for node, content in specialist_payloads.items()
        for patch in patch_blocks(content)
    ]

    position = "primary" if number % 2 else "final"
    option_a = primary if position == "primary" else final
    option_b = final if position == "primary" else primary
    chapter_dir = OUTPUT / "blind" / f"chapter-{number:02d}"
    write_text(chapter_dir / "option-a.md", option_a)
    write_text(chapter_dir / "option-b.md", option_b)
    diff_lines = difflib.unified_diff(
        primary.splitlines(),
        final.splitlines(),
        fromfile="Primary Draft",
        tofile="Integrator Final",
        lineterm="",
    )
    write_text(OUTPUT / "diffs" / f"chapter-{number:02d}-primary-to-final.diff", "\n".join(diff_lines) or "(no textual diff)")

    attribution_dir = OUTPUT / "attribution-inputs" / f"chapter-{number:02d}"
    write_text(attribution_dir / "primary-response.md", primary_response)
    write_text(attribution_dir / "integrator-response.md", git_text(integrator_path))
    for node, content in specialist_payloads.items():
        write_text(attribution_dir / f"{node}-response.md", content)

    return {
        "candidate": "candidate-c",
        "book": "《掌中天工》",
        "chapter": number,
        "source_commit": SOURCE_COMMIT,
        "source_paths": {
            "primary_response": primary_path,
            "final_formal_prose": final_path,
            "integrator_response": integrator_path,
            "manifest": manifest_path,
            "execution": execution_path,
            "selected_specialists": selected_path,
            "specialists": specialist_paths,
        },
        "selected_specialists_file": selected,
        "completed_specialists": completed_specialists,
        "specialist_call_count": len(completed_specialists),
        "integrator_call_count": int(bool(execution.get("integrator_executed"))),
        "integrator_final_source": execution.get("final_source"),
        "model_calls": execution.get("model_calls"),
        "proposed_patches": proposed_patches,
        **VERIFIED_ATTRIBUTION[number],
        "blind_position": {"option_a": position, "option_b": "final" if position == "primary" else "primary"},
        **metrics,
    }


def build_candidate_b_control() -> list[dict[str, Any]]:
    records = []
    for number in (1, 2, 3):
        chapter = f"chapter-{number:04d}"
        path = f"{V2_ROOT}/candidate-b/runs/{chapter}/execution.json"
        execution = json.loads(git_text(path))
        records.append(
            {
                "candidate": "candidate-b",
                "book": "《炉藏万象》",
                "chapter": number,
                "source_commit": SOURCE_COMMIT,
                "source_path": path,
                "selected_specialists": execution.get("selected_specialists", []),
                "integrator_executed": execution.get("integrator_executed"),
                "final_source": execution.get("final_source"),
                "model_calls": execution.get("model_calls"),
            }
        )
    return records


def main() -> None:
    records = [chapter_record(number) for number in (1, 2, 3)]
    write_text(
        OUTPUT / "blind" / "blind-key.md",
        "\n".join(
            [
                "# Blind key (do not provide to Reader)",
                "",
                f"source commit: `{SOURCE_COMMIT}`",
                "",
                *[
                    f"- Chapter {record['chapter']:02d}: option-a={record['blind_position']['option_a']}; option-b={record['blind_position']['option_b']}"
                    for record in records
                ],
            ]
        ),
    )
    write_text(
        OUTPUT / "source-manifest.json",
        json.dumps(
            {
                "experiment_generation_base": SOURCE_COMMIT,
                "experiment_generation_tree": "books/real-exp-opening-pipeline-comparison-v2",
                "code_audit_base": "53394ea356393c904e82d988e7b5ae634d2487f7",
                "v1_source_tree": "books/real-exp-opening-pipeline-comparison-v1",
                "v1_source_commit": SOURCE_COMMIT,
                "candidate_c_chapters": [record["source_paths"] for record in records],
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    write_text(OUTPUT / "metrics.json", json.dumps(records, ensure_ascii=False, indent=2))
    write_text(OUTPUT / "candidate-b-control.json", json.dumps(build_candidate_b_control(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
