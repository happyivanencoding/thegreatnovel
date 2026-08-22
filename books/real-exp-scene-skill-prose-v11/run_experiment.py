"""Run the frozen Scene Skill v1.1 prose attribution experiment.

This harness only writes the new experiment directory. It does not modify
production code, BOOK state, formal chapters, or the frozen source experiments.
Each model call is made exactly once and every prompt/response is preserved.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "books" / "real-exp-scene-skill-prose-v11"
STATIC = REPO / "books" / "real-exp-scene-skill-runtime-v1"
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_primary_draft,
    extract_primary_fact_summary,
)
from story_mvp.scene_skills import (  # noqa: E402
    parse_scene_skill_selection,
    render_selected_scene_skills,
)


CHAPTERS = (2, 3)
GROUPS = (
    ("A_no_skill", "No Scene Skill"),
    ("B_scene_skill_v1", "Scene Skill v1"),
    ("C_scene_skill_v11", "Scene Skill v1.1"),
)
EXPECTED_SELECTIONS = {
    2: ("social_bargain_decision", ""),
    3: ("trial_challenge", "combat"),
}
CALL_LOG: list[dict[str, object]] = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def git_text(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def historical_skill(skill_id: str) -> str:
    return subprocess.check_output(
        [
            "git",
            "show",
            f"c5be62c:.agents/skills/novel-scene-skills/scenes/{skill_id}.md",
        ],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).strip()


def current_skill_block(curator_response: str) -> str:
    return render_selected_scene_skills(curator_response)


def old_skill_block(primary: str, secondary: str) -> str:
    if not primary:
        return ""
    blocks = [
        "Scene Skill Runtime v1：下列 Skill 只控制 HOW TO REALIZE THE SCENE；不得修改 Chapter Mission、Canon、直接结果、资源状态、人物决定或章末推动，也不要求新增场景。",
        f"## Primary: {primary}\n\n# {primary}\n\n{historical_skill(primary)}",
    ]
    if secondary:
        blocks.append(f"## Secondary: {secondary}\n\n# {secondary}\n\n{historical_skill(secondary)}")
    return "\n\n".join(blocks)


def replace_level_one_block(prompt: str, heading: str, body: str) -> str:
    pattern = rf"(?ms)^#\s+{re.escape(heading)}\s*$\n.*?(?=^#\s+|\Z)"
    replacement = f"# {heading}\n\n{body.strip()}\n"
    updated, count = re.subn(pattern, replacement, prompt, count=1)
    if count != 1:
        raise RuntimeError(f"Primary Prompt 缺少可替换区块：{heading}")
    return updated.rstrip() + "\n"


def inject_scene_skill(prompt: str, block: str) -> str:
    if not block.strip():
        return prompt
    marker = "# Curator Audit\n"
    if marker not in prompt:
        raise RuntimeError("Primary Prompt 缺少 Curator Audit 插入点")
    return prompt.replace(
        marker,
        f"## ACTIVE SCENE SKILLS——只控制场景如何落成正文\n\n{block.strip()}\n\n{marker}",
        1,
    )


def primary_prompt(chapter: int, curator_response: str, group: str) -> str:
    base_path = STATIC / f"chapter-{chapter:04d}" / "primary_prompt_without_scene_skill.md"
    prompt = read(base_path)
    curator_audit = section(curator_response, "Curator Audit") or "无。"
    curated_context = section(curator_response, "Curated Chapter Context")
    if not curated_context:
        raise RuntimeError(f"Chapter {chapter} Curator response 缺少 Curated Chapter Context")
    prompt = replace_level_one_block(prompt, "Curator Audit", curator_audit)
    prompt = replace_level_one_block(prompt, "Curated Chapter Context", curated_context)

    primary, secondary = parse_scene_skill_selection(curator_response)
    if group == "A_no_skill":
        return prompt
    if group == "B_scene_skill_v1":
        return inject_scene_skill(prompt, old_skill_block(primary, secondary))
    if group == "C_scene_skill_v11":
        return inject_scene_skill(prompt, current_skill_block(curator_response))
    raise ValueError(f"未知实验组：{group}")


def call_model(kind: str, chapter: int, group: str, prompt: str) -> str:
    raise RuntimeError(
        "本实验禁止外部模型 API；请使用 Codex 独立子代理并由主线程保存 Response。"
    )


def selection_record(chapter: int, response: str) -> dict[str, object]:
    actual = parse_scene_skill_selection(response)
    expected = EXPECTED_SELECTIONS[chapter]
    valid = bool(actual[0])
    effective = actual if valid else expected
    return {
        "actual_primary": actual[0] or "none",
        "actual_secondary": actual[1] or "none",
        "selection_valid": valid,
        "selection_matches_expected": actual == expected,
        "expected_for_review_only": {
            "primary": expected[0] or "none",
            "secondary": expected[1] or "none",
        },
        "effective_for_ab_comparison": {
            "primary": effective[0] or "none",
            "secondary": effective[1] or "none",
        },
    }


def main() -> None:
    if OUT.exists():
        existing = {
            path.name
            for path in OUT.iterdir()
            if path.name != "__pycache__"
        }
        allowed = {
            "run_experiment.py",
            "README.md",
            "SOURCE_MANIFEST.json",
            "CALL_LOG.json",
            "RUN_STATUS.md",
            "chapter-0002",
            "chapter-0003",
        }
        if existing - allowed:
            raise SystemExit(f"实验目录已存在，为避免覆盖既有证据而停止：{OUT}")
    if git_text("branch", "--show-current") != "principal_dev_new_sys":
        raise SystemExit("当前分支不是 principal_dev_new_sys，停止实验")
    if git_text("rev-parse", "HEAD") != git_text("rev-parse", "f15190b"):
        raise SystemExit("当前 HEAD 不是 f15190b，停止实验")

    OUT.mkdir(parents=True, exist_ok=True)
    previous_log = read(OUT / "CALL_LOG.json")
    if previous_log.strip():
        loaded_log = json.loads(previous_log)
        if not isinstance(loaded_log, list):
            raise SystemExit("已有 CALL_LOG.json 不是列表，停止以避免覆盖未知证据")
        CALL_LOG.extend(loaded_log)
    write(
        OUT / "README.md",
        """# Scene Skill v1.1 真实章节 A/B/C 实验

本实验比较同一冻结 Chapter 2 / Chapter 3 上的三组 Primary Writer：

- A：不注入 Scene Skill；
- B：注入 `c5be62c` 的旧 Scene Skill v1；
- C：注入当前 HEAD 的 Scene Skill v1.1。

每章先调用一次当前生产 Context Curator，再用同一份 Curator Response 生成 A/B/C。除 Scene Skill 注入内容外，三组共用冻结 Primary Prompt 骨架、同一模型和同一章节上下文。不运行 Director、Specialist、Integrator 或 State Delta，不写入 BOOK / 正式 Canon，不人工润色，不自动重试。
""",
    )

    manifest = {
        "experiment": "real-exp-scene-skill-prose-v11",
        "branch": git_text("branch", "--show-current"),
        "head": git_text("rev-parse", "HEAD"),
        "baseline_commit": "f15190b",
        "old_scene_skill_commit": "c5be62c",
        "model": "Codex subagent（具体底层模型由当前环境决定）",
        "executor_adapter": "codex_subagent",
        "executor": {"kind": "codex_subagent"},
        "frozen_prompt_root": str(STATIC.relative_to(REPO)),
        "chapters": {
            "2": {
                "curator_prompt": "books/real-exp-scene-skill-runtime-v1/chapter-0002/curator_prompt_with_catalog.md",
                "primary_base_prompt": "books/real-exp-scene-skill-runtime-v1/chapter-0002/primary_prompt_without_scene_skill.md",
                "frozen_director": "books/real-exp-opening-reader-first-fresh-v1/runs/chapter-0002/director_response.md",
                "expected_scene_review": {"primary": "social_bargain_decision", "secondary": "none"},
            },
            "3": {
                "curator_prompt": "books/real-exp-scene-skill-runtime-v1/chapter-0003/curator_prompt_with_catalog.md",
                "primary_base_prompt": "books/real-exp-scene-skill-runtime-v1/chapter-0003/primary_prompt_without_scene_skill.md",
                "frozen_director": "books/real-exp-human-reaction-ch3-v1/after-v2/director_response.md",
                "expected_scene_review": {"primary": "trial_challenge", "secondary": "combat"},
            },
        },
        "groups": [name for name, _ in GROUPS],
        "call_policy": "one call per listed node; no automatic retry",
    }
    write(OUT / "SOURCE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    for chapter in CHAPTERS:
        chapter_dir = OUT / f"chapter-{chapter:04d}"
        source_dir = STATIC / f"chapter-{chapter:04d}"
        write(chapter_dir / "curator_prompt.md", read(source_dir / "curator_prompt_with_catalog.md"))
        frozen_director = (
            REPO / "books" / "real-exp-opening-reader-first-fresh-v1" / "runs" / "chapter-0002" / "director_response.md"
            if chapter == 2
            else REPO / "books" / "real-exp-human-reaction-ch3-v1" / "after-v2" / "director_response.md"
        )
        write(chapter_dir / "director_frozen.md", read(frozen_director))

        curator_prompt = read(chapter_dir / "curator_prompt.md")
        existing_curator_response = read(chapter_dir / "curator_response.md")
        if existing_curator_response.strip():
            curator_response = existing_curator_response
        else:
            curator_response = call_model("context_curator", chapter, "", curator_prompt)
            write(chapter_dir / "curator_response.md", curator_response)
        selection = selection_record(chapter, curator_response)
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
                    "若实际选择无效，A/B/C 对照的有效 Skill 注入将使用预先声明的 review reference；实际 Curator 失败保留在 curator_response.md 与 selection.json。",
                ]
            ),
        )

        primary, secondary = parse_scene_skill_selection(curator_response)
        if not primary:
            primary, secondary = EXPECTED_SELECTIONS[chapter]
            forced = True
        else:
            forced = False

        for group, _label in GROUPS:
            group_dir = chapter_dir / group
            prompt = primary_prompt(chapter, curator_response, group)
            if forced and group != "A_no_skill":
                if group == "B_scene_skill_v1":
                    block = old_skill_block(primary, secondary)
                else:
                    # The forced path is only used when Curator output is invalid.
                    # Keep the actual failure visible and use the declared reference.
                    blocks = [
                        "Scene Skill Runtime v1：下列 Skill 只控制 HOW TO REALIZE THE SCENE；不得修改 Chapter Mission、Canon、直接结果、资源状态、人物决定或章末推动，也不要求新增场景。",
                        f"## Primary: {primary}\n\n# {primary}\n\n{read(REPO / '.agents' / 'skills' / 'novel-scene-skills' / 'scenes' / (primary + '.md'))}",
                    ]
                    if secondary:
                        blocks.append(f"## Secondary: {secondary}\n\n# {secondary}\n\n{read(REPO / '.agents' / 'skills' / 'novel-scene-skills' / 'scenes' / (secondary + '.md'))}")
                    block = "\n\n".join(blocks)
                prompt = inject_scene_skill(prompt, block)
            write(group_dir / "primary_prompt.md", prompt)
            existing_response = read(group_dir / "primary_response.md")
            if existing_response.strip():
                response = existing_response
            else:
                response = call_model("primary_writer", chapter, group, prompt)
                write(group_dir / "primary_response.md", response)
            draft = extract_primary_draft(response)
            facts = extract_primary_fact_summary(response)
            write(group_dir / "chapter.md", draft or "[Primary Draft 提取失败；保留原始 response 作为证据]")
            write(group_dir / "primary_fact_summary.md", facts or "[Primary Fact Summary 提取失败]")

    write(OUT / "CALL_LOG.json", json.dumps(CALL_LOG, ensure_ascii=False, indent=2))
    write(
        OUT / "RUN_STATUS.md",
        "# Run Status\n\n" +
        f"完成时间（UTC）：{datetime.now(timezone.utc).isoformat()}\n\n" +
        f"实际完成调用：{len([x for x in CALL_LOG if x.get('status') == 'completed'])} / 8\n",
    )
    print(json.dumps({"out": str(OUT), "calls": len(CALL_LOG)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
