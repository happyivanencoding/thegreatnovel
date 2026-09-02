from __future__ import annotations

from story_mvp.character_context import (
    project_character_life_context,
    project_story_opportunity_layer,
    project_world_reality,
)
from story_mvp.character_prompts import (
    PROTAGONIST_BLIND_WORLD_TEMPLATE,
    STORY_REFRESH_PROMPT,
    WORLD_EXPANSION_PROMPT,
)
from story_mvp.batch_runtime import build_batch_delta_reviser_prompt, BatchWindow
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


def test_world_can_begin_with_existing_relationship_history() -> None:
    assert "Living Actors 可以在主角出现以前就彼此活过一段人生" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "过去发生了什么关键选择 → 今天留下什么关系/身份/债/空位/误解" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "## 已经活过的人与关系史" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "第三个人或下一代" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "表层解释" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "新区域的人不是在主角抵达那天才出生" in WORLD_EXPANSION_PROMPT
    assert "## 新人物的既有关系与旧选择" in WORLD_EXPANSION_PROMPT


def test_story_program_allows_past_gap_backfill_but_not_fake_future() -> None:
    assert "Relationship-History Backfill" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "过去可以被补出来，未来不能被假装已经发生" in LONGITUDINAL_THREAD_ADVANCE_DIRECTION
    assert "这里明确允许 Relationship-History Backfill" in STORY_PROGRAM_TEMPLATE
    assert "过去可以被补，已经写过的事件不能被改" in STORY_PROGRAM_TEMPLATE
    assert "多个既有人物、甚至跨代影响今天" in STORY_PROGRAM_TEMPLATE
    assert "允许补此前从未被 Authority / Canon 定义过的配角关系史与旧选择" in STORY_REFRESH_PROMPT
    assert "过去空白可以补，离屏未来不能事后伪造" in STORY_REFRESH_PROMPT
    assert "不得事后凭空补一段关键人生" not in STORY_PROGRAM_TEMPLATE


def test_outline_keeps_hidden_relationship_history_backstage_until_reveal() -> None:
    assert "隐藏人物旧史是 backstage Authority，不是自动 Reader Release" in OUTLINE_TEMPLATE
    assert "本次需要让读者知道的最小一层" in OUTLINE_TEMPLATE
    assert "这一节会进入章节 Runtime" in OUTLINE_TEMPLATE
    assert "不要复制 Story Program 中尚未排程揭露" in OUTLINE_TEMPLATE


def test_batch_reviser_does_not_auto_reveal_backfilled_history() -> None:
    plans = {n: f"第{n}章：表层关系继续成立，不揭露旧史。" for n in range(1, 5)}
    chapters = {n: f"# 第{n}章\n两人仍按当前表层关系行动。" for n in range(1, 5)}
    prompt = build_batch_delta_reviser_prompt(
        window=BatchWindow(1, 4),
        batch_plans=plans,
        primary_chapters=chapters,
        book_content="# 当前状态、未兑现承诺与作者备注\n",
        world_vision="",
        world_expansions="",
        character_card="",
        story_program="两人其实是旧爱，但本阶段尚未揭露。",
    )
    assert "Hidden Relationship-History Boundary" in prompt
    assert "一致性 Authority，不是自动公开 Authority" in prompt
    assert "不要顺手写出隐藏答案" in prompt


def test_world_relationship_history_is_story_opportunity_not_runtime_world_reality() -> None:
    world = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人坐船。

## 力量体系与正常值
潮阶1—20。

## 社会现实与身份
港城与家族。

## 世界里真正值钱、值得想要的东西
潮兵。

## 世界正在发生的大事
维娅正在抢古砖。

## 已经活过的人与关系史
维娅与岑绯的母亲曾共同沉船，旧债今天仍改变两人的路线。

## 值得进入的地点、奇观与未知
第七环。

## 世界知识边界
普通人知道潮阶。
"""
    opportunity = project_story_opportunity_layer(world)
    runtime = project_world_reality(world)
    human_life = project_character_life_context(world)
    assert "维娅与岑绯的母亲曾共同沉船" in opportunity
    assert "维娅与岑绯的母亲曾共同沉船" not in runtime
    assert "维娅与岑绯的母亲曾共同沉船" not in human_life
