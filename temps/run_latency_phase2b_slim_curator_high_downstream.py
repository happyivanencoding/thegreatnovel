from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
EXP = (
    ROOT
    / "books"
    / "real-exp-chapter-latency-optimization-20260829-v1"
    / "phase-2b-slim-curator-high"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_unresolved_fact_boundary,
    strip_legacy_prose_controls,
)
from story_mvp.scene_skills import (  # noqa: E402
    render_selected_revision_watches,
    strip_scene_skill_selection,
)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def call(prompt_path: Path, output_path: Path, model: str, effort: str) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), model, effort, str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if process.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
            except Exception as error:
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def replace_revision_watch(prompt: str, old_curator: str, new_curator: str) -> str:
    old_watch = render_selected_revision_watches(old_curator)
    new_watch = render_selected_revision_watches(new_curator)
    heading = "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
    primary_heading = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    if old_watch:
        block = f"{heading}\n\n{old_watch}"
        if block not in prompt:
            raise RuntimeError("old revision watch block missing")
        if new_watch:
            return prompt.replace(block, f"{heading}\n\n{new_watch}", 1)
        return prompt.replace(block + "\n\n", "", 1)
    if new_watch:
        marker = primary_heading
        if marker not in prompt:
            raise RuntimeError("primary heading missing for new revision watch")
        return prompt.replace(marker, f"{heading}\n\n{new_watch}\n\n{marker}", 1)
    return prompt


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = EXP / f"chapter-{chapter:04d}"
    old_curator = clean((source / "curator_response.md").read_text(encoding="utf-8"))
    new_curator = clean((directory / "slim_curator_response.md").read_text(encoding="utf-8"))
    old_visible = strip_legacy_prose_controls(strip_scene_skill_selection(old_curator))
    new_visible = strip_legacy_prose_controls(strip_scene_skill_selection(new_curator))
    old_unresolved = extract_unresolved_fact_boundary(old_curator)
    new_unresolved = extract_unresolved_fact_boundary(new_curator)

    primary_prompt = (source / "primary_prompt.md").read_text(encoding="utf-8")
    primary_prompt = replace_once(primary_prompt, old_visible, new_visible, f"ch{chapter} curator visible")
    if old_unresolved != new_unresolved:
        primary_prompt = replace_once(
            primary_prompt,
            old_unresolved or "（Curator 未投影出额外未解事实；仍服从最高事实边界。）",
            new_unresolved or "（Curator 未投影出额外未解事实；仍服从最高事实边界。）",
            f"ch{chapter} unresolved boundary",
        )
    primary_prompt_path = directory / "primary_slim_prompt.md"
    primary_prompt_path.write_text(primary_prompt, encoding="utf-8")
    primary_data = call(
        primary_prompt_path,
        directory / "primary_slim_acp.json",
        "gpt-5.6-terra",
        "high",
    )
    primary_text = clean(primary_data.get("text", ""))
    primary_body = body(primary_text)
    (directory / "primary_slim_response.md").write_text(primary_text + "\n", encoding="utf-8")
    (directory / "primary_slim_body.md").write_text(primary_body + "\n", encoding="utf-8")

    old_primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    reviser_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    reviser_prompt = replace_once(reviser_prompt, old_curator, new_curator, f"ch{chapter} reviser curator")
    reviser_prompt = replace_once(reviser_prompt, old_primary, primary_body, f"ch{chapter} reviser primary")
    reviser_prompt = replace_revision_watch(reviser_prompt, old_curator, new_curator)
    reviser_prompt_path = directory / "reviser_slim_prompt.md"
    reviser_prompt_path.write_text(reviser_prompt, encoding="utf-8")
    reviser_data = call(
        reviser_prompt_path,
        directory / "reviser_slim_acp.json",
        "gpt-5.6-luna",
        "high",
    )
    reviser_text = clean(reviser_data.get("text", ""))
    final_body = body(reviser_text)
    (directory / "reviser_slim_response.md").write_text(reviser_text + "\n", encoding="utf-8")
    (directory / "final_slim_body.md").write_text(final_body + "\n", encoding="utf-8")

    curator_data = json.loads((directory / "slim_curator_high_acp.json").read_text(encoding="utf-8"))
    control = {}
    for stage in ("curator", "primary", "authority_reviser"):
        control[stage] = json.loads((source / f"{stage}_acp.json").read_text(encoding="utf-8"))
    treatment_total = sum(
        float(item.get("wall_seconds") or 0)
        for item in (curator_data, primary_data, reviser_data)
    )
    control_total = sum(float(control[stage].get("wall_seconds") or 0) for stage in control)
    return {
        "chapter": chapter,
        "curator_seconds": curator_data.get("wall_seconds"),
        "primary_seconds": primary_data.get("wall_seconds"),
        "reviser_seconds": reviser_data.get("wall_seconds"),
        "treatment_total_seconds": round(treatment_total, 3),
        "control_total_seconds": round(control_total, 3),
        "total_speedup_percent": round((1 - treatment_total / control_total) * 100, 2),
        "primary_chars": len(primary_body),
        "final_chars": len(final_body),
        "primary_usage": primary_data.get("result", {}).get("usage", {}),
        "reviser_usage": reviser_data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (EXP / "downstream_summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
