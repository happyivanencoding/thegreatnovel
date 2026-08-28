"""Scene Skill Runtime v2 的确定性选择解析、短投影元数据与按需加载。

Scene Skill 只影响场景如何落成正文，不调用模型、不修改 Chapter Mission 或 Canon。
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path


SCENE_SKILL_IDS = (
    "social_bargain_decision",
    "relationship",
    "identity_reveal",
    "departure_vacancy",
    "sacrifice_convergence",
    "reunion_reentry",
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


def _inline_runtime_field(content: str, label: str) -> str:
    match = re.search(
        rf"(?m)^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$",
        content,
    )
    if not match:
        return ""
    value = match.group(1).strip()
    return "" if value.casefold() in _NONE_VALUES else value


def scene_skill_projection_guidance(skill_id: str) -> str:
    content = load_scene_skill(skill_id)
    return _inline_runtime_field(content, "Projection Guidance") if content else ""


def scene_skill_revision_watch(skill_id: str) -> str:
    content = load_scene_skill(skill_id)
    return _inline_runtime_field(content, "Revision Watch") if content else ""


@lru_cache(maxsize=1)
def render_scene_skill_catalog() -> str:
    """给 Curator 的紧凑可选目录，只暴露 ID、Reading Question 与短 Projection Guidance。"""

    lines: list[str] = []
    for skill_id in SCENE_SKILL_IDS:
        content = load_scene_skill(skill_id)
        if not content:
            continue
        question = _primary_reading_question(content)
        guidance = scene_skill_projection_guidance(skill_id)
        line = f"- {skill_id}: {question or '按该 Scene Skill 的主要阅读问题执行'}"
        if guidance:
            line += f" | Projection Guidance: {guidance}"
        lines.append(line)
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
    """深 Skill 文档的 legacy / research renderer；production Primary v2 不直接消费此输出。"""

    primary, secondary = parse_scene_skill_selection(curated_context)
    if not primary:
        return ""

    blocks = [
        "Scene Skill Deep Craft（legacy / research renderer）：下列 Skill 只控制 HOW TO REALIZE THE SCENE；不得修改 Chapter Mission、Canon、直接结果、资源状态、人物决定或章末推动，也不要求新增场景。执行 Skill 时只在其关键 beat 上提高细节密度：优先少量承载故事的动作、物件、空间、身体反馈、力量可见后果和人物差异化反应，不把整章都提高修饰密度。",
        f"## Primary: {primary}\n\n{load_scene_skill(primary)}",
    ]
    if secondary:
        blocks.append(f"## Secondary: {secondary}\n\n{load_scene_skill(secondary)}")
    return "\n\n".join(blocks)


def render_selected_revision_watches(curated_context: str) -> str:
    """只给 Authority Reviser 渲染已选 Skill 的极短 failure-based watch。"""

    primary, secondary = parse_scene_skill_selection(curated_context)
    if not primary:
        return ""
    blocks: list[str] = []
    for label, skill_id in (("Primary", primary), ("Secondary", secondary)):
        if not skill_id:
            continue
        watch = scene_skill_revision_watch(skill_id)
        if watch:
            blocks.append(f"- {label} / {skill_id}: {watch}")
    if not blocks:
        return ""
    return "\n".join(
        [
            "这些只是 failure-triggered 局部观察点，不是补写清单；Primary Draft 没有对应失败时全部忽略，Preservation First。",
            *blocks,
        ]
    )


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
