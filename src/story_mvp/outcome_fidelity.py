"""Low-frequency explicit milestone outcome fidelity for chapter finalization.

This module does not judge prose quality. It only recognizes a narrow shape that the
production pipeline has proven it can silently lose: an approved current-chapter
transition such as “进入镇海 / 晋升内门 / 成为…”, while the final draft merely implies
it through battle results or atmosphere.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ExplicitMilestoneOutcome:
    outcome: str
    target: str


_OUTCOME_PATTERNS = (
    # Current production: Future-10 result is composed directly into Frozen Mission.
    re.compile(
        r"上游计划已批准结果（[^\n]*?）[：:](.*?)"
        r"(?=\n(?:结尾推动力|叙事功能|规划备注)|\n\n#|\Z)",
        re.S,
    ),
    # Backward-compatible shape for already-created Run prompts from the validation period.
    re.compile(
        r"已批准当前章结果\s*/\s*状态变化[：:]\s*\n(.*?)"
        r"(?=\n\n这是当前章的 Outcome Authority|\n\n这不是第二份剧情计划|\n\n#|\Z)",
        re.S,
    ),
)
_TRANSITION = re.compile(
    r"(?:本人)?(?:真正)?(?:正式)?"
    r"(?:进入|踏入|晋入|突破(?:到|至)?|晋升(?:到|至|为)?|提升(?:到|至)?|升(?:到|至)|达到|成为)"
    r"(?P<target>[\u4e00-\u9fffA-Za-z0-9·_-]{1,12})"
)


def detect_explicit_milestone_outcome(authority_prompt: str) -> ExplicitMilestoneOutcome | None:
    """Return one explicit approved milestone transition, or None for ordinary chapters."""

    outcome = ""
    for pattern in _OUTCOME_PATTERNS:
        match = pattern.search(authority_prompt)
        if match:
            outcome = match.group(1).strip()
            break
    if not outcome:
        return None
    transition = _TRANSITION.search(outcome)
    if not transition:
        return None
    target = transition.group("target").strip()
    if not target:
        return None
    return ExplicitMilestoneOutcome(outcome=outcome, target=target)


def explicit_milestone_realized(final_response: str, requirement: ExplicitMilestoneOutcome) -> bool:
    """Require a direct transition statement; target appearing in a battle name is not enough."""

    target = re.escape(requirement.target)
    patterns = (
        rf"(?:进入|踏入|晋入|突破(?:到|至)?|晋升(?:到|至|为)?|提升(?:到|至)?|升(?:到|至)|达到|成为)\s*{target}(?:者|境|阶|级)?",
        rf"(?:已是|已经是|正式是|当前是|修为是)\s*{target}(?:者|境|阶|级)?",
        rf"{target}(?:者|境|阶|级)\s*(?:已经|正式)?(?:成立|达成|突破|晋升)",
    )
    return any(re.search(pattern, final_response) for pattern in patterns)


def _relevant_authority_lines(authority_prompt: str, target: str, *, limit: int = 8) -> str:
    lines = authority_prompt.splitlines()
    selected: list[str] = []
    for index, line in enumerate(lines):
        if target not in line:
            continue
        start = max(0, index - 1)
        end = min(len(lines), index + 2)
        block = "\n".join(lines[start:end]).strip()
        if block and block not in selected:
            selected.append(block)
        if len(selected) >= limit:
            break
    return "\n\n".join(selected)


def _frozen_mission_excerpt(authority_prompt: str, *, max_chars: int = 4200) -> str:
    marker = "FROZEN CHAPTER MISSION"
    start = authority_prompt.find(marker)
    if start < 0:
        marker = "Chapter Mission"
        start = authority_prompt.find(marker)
    if start < 0:
        return "（原 Prompt 未找到独立 Mission 区块；仍只允许恢复批准 outcome。）"
    tail = authority_prompt[start : start + max_chars]
    next_markers = (
        "CURRENT PLAN OUTCOME AUTHORITY",
        "CURATOR｜",
        "WORLD REALITY AUTHORITY",
    )
    cut = len(tail)
    for next_marker in next_markers:
        pos = tail.find(next_marker, len(marker))
        if pos >= 0:
            cut = min(cut, pos)
    return tail[:cut].strip()


def build_explicit_milestone_repair_prompt(
    authority_prompt: str,
    final_response: str,
    requirement: ExplicitMilestoneOutcome,
) -> str:
    """Build one narrow Preservation-First retry; no new story planning is authorized."""

    relevant = _relevant_authority_lines(authority_prompt, requirement.target)
    mission = _frozen_mission_excerpt(authority_prompt)
    return f"""你是 TGN 的条件性 Outcome Repair。只有因为一个**已批准的当前章显式里程碑结果**在 Authority Revision 中仍未明确成为事实，你才会被调用。你不是第二个 Director，也不是新的审稿 Agent。

唯一必须恢复的已批准结果：
{requirement.outcome}

显式里程碑目标：{requirement.target}

失败定义：仅仅写“打赢了 {requirement.target} 级战局 / 承受了 {requirement.target} 压力 / 被重新估价 / 接近这一层”都不算；如果 Frozen Mission 中已经发生了足以支撑批准结果的事件，最终正文必须有一次普通读者可以直接复述的等义陈述，明确让该里程碑状态成立。

修复边界：
1. Preservation First：当前 Authority Revision 是唯一底稿；没有必要的句子逐字保留，不整章重写。
2. 只在批准事件已经提供因果的位置补最小 realization：必要时补 1 个很短的跨档因果句，再在最近结果处直接命名一次 `{requirement.target}`。
3. 不新增战斗、考核、资源、功法、仪式、伤势、代价、人物决定、胜负、奖励、关系变化或下一世界事实。
4. 不改变任何已经成立的事件顺序、胜负、资源得失、伤势、持有关系、Ending 或未知边界。
5. 若相关能力有 Frozen Boundary，继续保留；主角跨档不授权分身、宠物、装备或其它对象同步获得完整新档能力。
6. 不用第二次证明里程碑；一次最短直接落点足够。
7. 固定只输出：`# 正式正文` + 完整修订正文。不要输出 Audit、解释或修改说明。

# 与目标相关的已有 Authority / Ruler 片段
{relevant or '（没有额外 ruler 片段；只按已批准 outcome 与 Frozen Mission 做最小恢复。）'}

# Frozen Mission 摘要
{mission}

# CURRENT AUTHORITY REVISION｜唯一待修底稿
{final_response.strip()}
"""
