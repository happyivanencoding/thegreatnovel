"""Prepare the deterministic prompts for the Codex-subagent experiment.

This file never calls an external model. Curator responses are supplied by the
main Codex thread after independent subagents finish; it then prepares the
three isolated Primary prompts for each chapter.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "books" / "real-exp-scene-skill-prose-v11"
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from run_experiment import (  # noqa: E402
    CHAPTERS,
    EXPECTED_SELECTIONS,
    GROUPS,
    STATIC,
    inject_scene_skill,
    old_skill_block,
    parse_scene_skill_selection,
    primary_prompt,
    read,
    selection_record,
    write,
)


def forced_current_skill_block(primary: str, secondary: str) -> str:
    blocks = [
        "Scene Skill Runtime v1：下列 Skill 只控制 HOW TO REALIZE THE SCENE；不得修改 Chapter Mission、Canon、直接结果、资源状态、人物决定或章末推动，也不要求新增场景。",
        f"## Primary: {primary}\n\n{read(ROOT / '.agents' / 'skills' / 'novel-scene-skills' / 'scenes' / (primary + '.md'))}",
    ]
    if secondary:
        blocks.append(
            f"## Secondary: {secondary}\n\n{read(ROOT / '.agents' / 'skills' / 'novel-scene-skills' / 'scenes' / (secondary + '.md'))}"
        )
    return "\n\n".join(blocks)


def main() -> None:
    for chapter in CHAPTERS:
        chapter_dir = OUT / f"chapter-{chapter:04d}"
        response = read(chapter_dir / "curator_response.md")
        if not response.strip():
            raise SystemExit(f"Chapter {chapter} 缺少 curator_response.md")

        selection = selection_record(chapter, response)
        write(chapter_dir / "selection.json", json.dumps(selection, ensure_ascii=False, indent=2))
        write(
            chapter_dir / "selection.md",
            "\n".join(
                [
                    f"# Chapter {chapter} Scene Skill Selection",
                    f"Actual Primary: {selection['actual_primary']}",
                    f"Actual Secondary: {selection['actual_secondary']}",
                    f"Valid: {selection['selection_valid']}",
                    f"Matches expected review reference: {selection['selection_matches_expected']}",
                    "",
                    "若实际选择无效，A/B/C 的 Skill 注入使用预先声明的 review reference；实际 Curator 失败保留在 curator_response.md 与 selection.json。",
                ]
            ),
        )

        primary, secondary = parse_scene_skill_selection(response)
        forced = not bool(primary)
        if forced:
            primary, secondary = EXPECTED_SELECTIONS[chapter]

        for group, _label in GROUPS:
            prompt = primary_prompt(chapter, response, group)
            if forced and group != "A_no_skill":
                block = (
                    old_skill_block(primary, secondary)
                    if group == "B_scene_skill_v1"
                    else forced_current_skill_block(primary, secondary)
                )
                prompt = inject_scene_skill(prompt, block)
            write(chapter_dir / group / "primary_prompt.md", prompt)

        base = read(OUT / "SOURCE_MANIFEST.json")
        if base.strip():
            manifest = json.loads(base)
            manifest["model"] = "Codex subagent（具体底层模型由当前环境决定）"
            manifest["executor_adapter"] = "codex_subagent"
            manifest["external_api_calls"] = "not part of experiment; see EXTERNAL_API_ATTEMPTS.json"
            write(OUT / "SOURCE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    print("prepared")


if __name__ == "__main__":
    main()
