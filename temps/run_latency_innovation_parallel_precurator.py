from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-precurator"
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

PRECURATOR_TEMPLATE = """你是 TGN 的 Parallel Pre-Curator，使用 GPT-5.6 Luna high。你与 Director 并行运行，因此看不到 Director 最终八字段合同；你只能根据已批准 Future 10 当前章计划、阶段背景、Canon、World/Human/Book/Prose 与上一章尾部，提前编译本章的静态注意力包。

你不是 Director，不得决定本章具体事件、行动者、动作对象、胜负、资源得失、状态变化或 Ending。`Relevant Plan` 必须只写 `BIND_FROM_DIRECTOR`，运行时会在 Director 完成后确定性换成 Frozen Mission。其它区块可以判断当前章最相关的人物欲望、世界事实、未知边界、表达压力、已成立边界、重复风险与 Payoff 窗口，但不得借“让场景更具体”补造 Director 尚未冻结的动作步骤。

固定输出：
# Curator Audit
只报告上游 Plan / Canon / World / Human 的明确冲突或未知；不要因为没看到 Director 而报缺失。
# Curated Chapter Context
## Relevant Book Contract
## Relevant Characters and Relationships
## Relevant World Rules
## Relevant Open Promises
## Relevant Plan
必须逐字写：BIND_FROM_DIRECTOR
## Scene Prose Projection
已经清楚写 NONE；否则只写2—4句当前章静态表达压力，不新增事件。
## Opening Strategy
## Scene Skill Selection
Primary: <skill_id 或 none>
Secondary: <skill_id 或 none>
## Relevant Inspiration
## Reader-Facing Language
## Already Established — Do Not Re-explain
## Recent Repetition Risks
## Payoff and Promise Window

全部区块保留，无内容写“无”。不要输出正文、评分、完整计划或思考过程。"""


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


def h2_span(text: str, prefix: str) -> tuple[int, int, str]:
    starts = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(starts):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        return match.start(), end, text[match.end():end].strip()
    raise ValueError(f"missing heading prefix: {prefix}")


def replace_h2(text: str, prefix: str, new_heading: str, new_body: str) -> str:
    start, end, _ = h2_span(text, prefix)
    replacement = f"## {new_heading}\n\n{new_body}\n\n"
    return text[:start] + replacement + text[end:].lstrip()


def exact_block(text: str, start_marker: str, end_marker: str | None) -> str:
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start) if end_marker else len(text)
    return text[start:end].strip()


def build_precurator_prompt(chapter: int) -> tuple[str, str]:
    source = SOURCE / f"chapter-{chapter:04d}"
    curator_prompt = (source / "curator_prompt.md").read_text(encoding="utf-8")
    director_prompt = (source / "director_prompt.md").read_text(encoding="utf-8")
    runtime_inputs = curator_prompt[curator_prompt.index("# Hybrid Runtime"):]
    chapter_plan = ""
    try:
        chapter_plan = h2_span(director_prompt, f"第{chapter}章")[2]
    except ValueError:
        pass
    skeleton = "\n\n".join(
        part for part in (
            (f"Future 10 第{chapter}章条目：\n" + chapter_plan) if chapter_plan else "",
            "注意：这不是 Frozen Mission；不得据此决定精确行动者/动作对象/反应/Ending。",
        )
        if part
    )
    runtime_inputs = replace_h2(runtime_inputs, "当前章事件合同", "PRE-DIRECTOR PLAN SKELETON", skeleton)
    return PRECURATOR_TEMPLATE + "\n\n" + runtime_inputs, curator_prompt


def bind_mission(precurator: str, source_curator_prompt: str) -> str:
    _, _, mission = h2_span(source_curator_prompt, "当前章事件合同")
    start, end, _ = h2_span(precurator, "Relevant Plan")
    replacement = f"## Relevant Plan\n\n{mission}\n\n"
    return (precurator[:start] + replacement + precurator[end:].lstrip()).strip()


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
        if primary_heading not in prompt:
            raise RuntimeError("primary heading missing")
        return prompt.replace(primary_heading, f"{heading}\n\n{new_watch}\n\n{primary_heading}", 1)
    return prompt


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt, source_curator_prompt = build_precurator_prompt(chapter)
    prompt_path = directory / "precurator_prompt.md"
    output_path = directory / "precurator_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    curator_data = call(prompt_path, output_path, "gpt-5.6-luna", "high")
    precurator = clean(curator_data.get("text", ""))
    bound_curator = bind_mission(precurator, source_curator_prompt)
    (directory / "precurator_response.md").write_text(precurator + "\n", encoding="utf-8")
    (directory / "bound_curator_response.md").write_text(bound_curator + "\n", encoding="utf-8")

    old_curator = clean((source / "curator_response.md").read_text(encoding="utf-8"))
    old_visible = strip_legacy_prose_controls(strip_scene_skill_selection(old_curator))
    new_visible = strip_legacy_prose_controls(strip_scene_skill_selection(bound_curator))
    old_unresolved = extract_unresolved_fact_boundary(old_curator)
    new_unresolved = extract_unresolved_fact_boundary(bound_curator)

    primary_prompt = (source / "primary_prompt.md").read_text(encoding="utf-8")
    primary_prompt = replace_once(primary_prompt, old_visible, new_visible, f"ch{chapter} curator visible")
    if old_unresolved != new_unresolved:
        primary_prompt = replace_once(
            primary_prompt,
            old_unresolved or "（Curator 未投影出额外未解事实；仍服从最高事实边界。）",
            new_unresolved or "（Curator 未投影出额外未解事实；仍服从最高事实边界。）",
            f"ch{chapter} unresolved boundary",
        )
    primary_prompt_path = directory / "primary_prompt.md"
    primary_output_path = directory / "primary_acp.json"
    primary_prompt_path.write_text(primary_prompt, encoding="utf-8")
    primary_data = call(primary_prompt_path, primary_output_path, "gpt-5.6-terra", "high")
    primary_text = clean(primary_data.get("text", ""))
    primary_body = body(primary_text)
    (directory / "primary_response.md").write_text(primary_text + "\n", encoding="utf-8")
    (directory / "primary_body.md").write_text(primary_body + "\n", encoding="utf-8")

    old_primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    reviser_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    reviser_prompt = replace_once(reviser_prompt, old_curator, bound_curator, f"ch{chapter} reviser curator")
    reviser_prompt = replace_once(reviser_prompt, old_primary, primary_body, f"ch{chapter} reviser primary")
    reviser_prompt = replace_revision_watch(reviser_prompt, old_curator, bound_curator)
    reviser_prompt_path = directory / "reviser_prompt.md"
    reviser_output_path = directory / "reviser_acp.json"
    reviser_prompt_path.write_text(reviser_prompt, encoding="utf-8")
    reviser_data = call(reviser_prompt_path, reviser_output_path, "gpt-5.6-luna", "high")
    reviser_text = clean(reviser_data.get("text", ""))
    final_body = body(reviser_text)
    (directory / "reviser_response.md").write_text(reviser_text + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    control = {
        stage: json.loads((source / f"{stage}_acp.json").read_text(encoding="utf-8"))
        for stage in ("director", "curator", "primary", "authority_reviser")
    }
    director_wall = float(control["director"].get("wall_seconds") or 0)
    precurator_wall = float(curator_data.get("wall_seconds") or 0)
    primary_wall = float(primary_data.get("wall_seconds") or 0)
    reviser_wall = float(reviser_data.get("wall_seconds") or 0)
    control_total = sum(float(control[stage].get("wall_seconds") or 0) for stage in control)
    treatment_critical = max(director_wall, precurator_wall) + primary_wall + reviser_wall
    return {
        "chapter": chapter,
        "director_recorded_wall_seconds": director_wall,
        "precurator_wall_seconds": precurator_wall,
        "primary_wall_seconds": primary_wall,
        "reviser_wall_seconds": reviser_wall,
        "control_d_c_p_r_seconds": round(control_total, 3),
        "treatment_parallel_critical_seconds": round(treatment_critical, 3),
        "critical_path_speedup_percent": round((1 - treatment_critical / control_total) * 100, 2),
        "precurator_prompt_chars": len(prompt),
        "bound_curator_chars": len(bound_curator),
        "final_chars": len(final_body),
        "precurator_usage": curator_data.get("result", {}).get("usage", {}),
        "primary_usage": primary_data.get("result", {}).get("usage", {}),
        "reviser_usage": reviser_data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
