"""Scene Skill Runtime v1 的确定性选择解析与按需加载。

Scene Skill 只影响场景如何落成正文，不调用模型、不修改 Chapter Mission 或 Canon。
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path


SCENE_SKILL_IDS = (
    "social_bargain_decision",
    "relationship",
    "comedy_banter",
    "investigation",
    "deduction_reveal",
    "horror_anomaly",
    "exploration",
    "survival_endurance",
    "stealth_infiltration",
    "chase_escape",
    "combat",
    "hunt_acquisition",
    "training_learning",
    "comprehension_insight",
    "trial_challenge",
    "breakthrough_advancement",
    "showcase_evaluation",
    "resource_economy",
    "crafting_creation",
    "recovery_restoration",
)

_SCENE_SKILL_ROOT = (
    Path(__file__).resolve().parents[2]
    / ".agents"
    / "skills"
    / "novel-scene-skills"
    / "scenes"
)
_NONE_VALUES = {"", "none", "无", "null", "n/a"}


@lru_cache(maxsize=None)
def load_scene_skill(skill_id: str) -> str:
    """读取一个已知 Primary Scene Skill；未知或缺失时返回空串。"""

    if skill_id not in SCENE_SKILL_IDS:
        return ""
    path = _SCENE_SKILL_ROOT / f"{skill_id}.md"
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _primary_reading_question(content: str) -> str:
    match = re.search(
        r"(?m)^\*\*Primary Reading Question:\*\*\s*(.+?)\s*$",
        content,
    )
    return match.group(1).strip() if match else ""


@lru_cache(maxsize=1)
def render_scene_skill_catalog() -> str:
    """给 Curator 的紧凑可选目录，只暴露 ID 与 Primary Reading Question。"""

    lines: list[str] = []
    for skill_id in SCENE_SKILL_IDS:
        content = load_scene_skill(skill_id)
        if not content:
            continue
        question = _primary_reading_question(content)
        lines.append(f"- {skill_id}: {question or '按该 Scene Skill 的主要阅读问题执行'}")
    return "\n".join(lines) or "（当前没有可读取的 Scene Skill。）"


def _extract_selection_section(curated_context: str) -> str:
    lines = curated_context.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "## Scene Skill Selection":
            continue
        selected: list[str] = []
        for next_line in lines[index + 1 :]:
            stripped = next_line.strip()
            if stripped.startswith("## ") or stripped.startswith("# "):
                break
            selected.append(next_line)
        return "\n".join(selected).strip()
    return ""


def parse_scene_skill_selection(curated_context: str) -> tuple[str, str]:
    """解析 Curator 的 Primary / Secondary 选择；Primary 无效时整体视为未选择。"""

    section = _extract_selection_section(curated_context)
    if not section:
        return "", ""

    def value_for(label: str) -> str:
        match = re.search(
            rf"(?mi)^{label}\s*[:：]\s*([a-z0-9_/-]+|无)\s*$",
            section,
        )
        return match.group(1).strip().lower() if match else ""

    primary = value_for("Primary")
    secondary = value_for("Secondary")
    if primary in _NONE_VALUES or not load_scene_skill(primary):
        return "", ""
    if secondary in _NONE_VALUES or secondary == primary or not load_scene_skill(secondary):
        secondary = ""
    return primary, secondary


def render_selected_scene_skills(curated_context: str) -> str:
    """只渲染 Curator 选中的 1 个 Primary 与可选 1 个 Secondary。"""

    primary, secondary = parse_scene_skill_selection(curated_context)
    if not primary:
        return ""

    blocks = [
        "Scene Skill Runtime v1：下列 Skill 只控制 HOW TO REALIZE THE SCENE；不得修改 Chapter Mission、Canon、直接结果、资源状态、人物决定或章末推动，也不要求新增场景。",
        f"## Primary: {primary}\n\n{load_scene_skill(primary)}",
    ]
    if secondary:
        blocks.append(f"## Secondary: {secondary}\n\n{load_scene_skill(secondary)}")
    return "\n\n".join(blocks)


def strip_scene_skill_selection(curated_context: str) -> str:
    """从 Writer 可见 Curated Context 中移除运行期选择控制区块。"""

    lines = curated_context.splitlines()
    kept: list[str] = []
    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## Scene Skill Selection":
            skipping = True
            continue
        if skipping and (stripped.startswith("## ") or stripped.startswith("# ")):
            skipping = False
        if not skipping:
            kept.append(line)
    return "\n".join(kept).strip()
