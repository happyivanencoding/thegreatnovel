from __future__ import annotations

from story_mvp.character_prompts import STORY_REFRESH_PROMPT
from story_mvp.prompts import (
    DEFAULT_STATE_DELTA_TEMPLATE,
    FANTASY_COMPOUNDING_DIRECTION,
    LONGITUDINAL_THREAD_ADVANCE_DIRECTION,
    OUTLINE_TEMPLATE,
    PROTAGONIST_BEHAVIOR_SIGNATURE_DIRECTION,
    READER_FIRST_PROSE_CONTRACT,
    STORY_PROGRAM_TEMPLATE,
)


def test_story_program_carries_longitudinal_engine_rules() -> None:
    assert "Canon 被保存不等于故事在推进" in STORY_PROGRAM_TEMPLATE
    assert "回归不能长期退化为" in STORY_PROGRAM_TEMPLATE
    assert "Opportunity Collision ≠ Task Board" in STORY_PROGRAM_TEMPLATE
    assert "Persistent Global Progress Ruler" in STORY_PROGRAM_TEMPLATE
    assert "自然 Horizon 末尾做“双结算”，不是旧线回访配额" in STORY_PROGRAM_TEMPLATE
    assert "Book-Level Longitudinal Spine" in STORY_PROGRAM_TEMPLATE
    assert "60—120 章" in STORY_PROGRAM_TEMPLATE
    assert "Local Closure + Book State Mutation" in STORY_PROGRAM_TEMPLATE
    assert "谁从此不能再按旧身份/关系/价格/策略/知识位置行动" in STORY_PROGRAM_TEMPLATE


def test_story_refresh_requires_real_cross_horizon_progress() -> None:
    assert "Canon 被保存不等于故事在推进" in STORY_REFRESH_PROMPT
    assert "旧线不能只被保存" in STORY_REFRESH_PROMPT
    assert "回归不能长期退化为" in STORY_REFRESH_PROMPT
    assert "Opportunity Collision ≠ Task Board" in STORY_REFRESH_PROMPT
    assert "Persistent Global Progress Ruler" in STORY_REFRESH_PROMPT
    assert "没有每 Horizon 回访税" in STORY_REFRESH_PROMPT
    assert "Local Closure + Book State Mutation" in STORY_REFRESH_PROMPT


def test_outline_receives_longitudinal_and_anti_task_board_rules() -> None:
    assert "Canon 被保存不等于故事在推进" in OUTLINE_TEMPLATE
    assert "回归不能长期退化为" in OUTLINE_TEMPLATE
    assert "Opportunity Collision ≠ Task Board" in OUTLINE_TEMPLATE
    assert "Persistent Global Progress Ruler" in OUTLINE_TEMPLATE


def test_primary_prose_contract_decays_mechanism_explanation() -> None:
    assert "规则说明随使用次数衰减" in READER_FIRST_PROSE_CONTRACT
    assert "第三次以后" in READER_FIRST_PROSE_CONTRACT
    assert "不要在高潮前先把" in READER_FIRST_PROSE_CONTRACT
    assert "章名优先抓人物、争夺物、地点变化、胜负或有画面的结果" in READER_FIRST_PROSE_CONTRACT


def test_book_engine_uses_decision_vector_without_old_thread_quota() -> None:
    assert "Signature ≠ Tension" in PROTAGONIST_BEHAVIOR_SIGNATURE_DIRECTION
    assert "第三条路不能无损全拿" in PROTAGONIST_BEHAVIOR_SIGNATURE_DIRECTION
    assert "Local Closure + Book State Mutation" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "长期线可以完整休眠一个甚至多个 Horizon" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "至少应让 1—3 条" not in LONGITUDINAL_THREAD_ADVANCE_DIRECTION


def test_history_is_recontextualized_before_compounding() -> None:
    assert "Carry → Recontextualize → Combine → Consequence / Reprice" in FANTASY_COMPOUNDING_DIRECTION
    assert "若只是换地图后原样再用一次，不算新的 compounding" in FANTASY_COMPOUNDING_DIRECTION


def test_longitudinal_cast_is_not_protagonist_star_topology() -> None:
    assert "Longitudinal Cast ≠ Important NPC List" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "如果主角此刻消失" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "Convergence ≠ Recall" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "主角只是关系网中的一条边" in STORY_PROGRAM_TEMPLATE
    assert "自己的未完人生与已启动行动" in STORY_PROGRAM_TEMPLATE
    assert "Convergence，不是召回旧 NPC 站队" in STORY_REFRESH_PROMPT


def test_state_keeps_cast_motion_without_building_relationship_graph() -> None:
    assert "自己的当前目标/已启动动作" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "其它会改变行动的关键人物关系" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "与主角关系只是其中一项" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "不画全员关系网" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "补造离屏恋爱、联盟、背叛、升级" in DEFAULT_STATE_DELTA_TEMPLATE
