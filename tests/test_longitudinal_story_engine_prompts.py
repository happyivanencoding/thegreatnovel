from __future__ import annotations

from story_mvp.character_prompts import STORY_REFRESH_PROMPT
from story_mvp.prompts import (
    OUTLINE_TEMPLATE,
    READER_FIRST_PROSE_CONTRACT,
    STORY_PROGRAM_TEMPLATE,
)


def test_story_program_carries_longitudinal_engine_rules() -> None:
    assert "Canon 被保存不等于故事在推进" in STORY_PROGRAM_TEMPLATE
    assert "回归不能长期退化为" in STORY_PROGRAM_TEMPLATE
    assert "Opportunity Collision ≠ Task Board" in STORY_PROGRAM_TEMPLATE
    assert "Persistent Global Progress Ruler" in STORY_PROGRAM_TEMPLATE
    assert "不能把跨 Horizon 长线全部降成文末备忘" in STORY_PROGRAM_TEMPLATE
    assert "Book-Level Longitudinal Spine" in STORY_PROGRAM_TEMPLATE
    assert "60—120 章" in STORY_PROGRAM_TEMPLATE


def test_story_refresh_requires_real_cross_horizon_progress() -> None:
    assert "Canon 被保存不等于故事在推进" in STORY_REFRESH_PROMPT
    assert "旧线不能只被保存" in STORY_REFRESH_PROMPT
    assert "回归不能长期退化为" in STORY_REFRESH_PROMPT
    assert "Opportunity Collision ≠ Task Board" in STORY_REFRESH_PROMPT
    assert "Persistent Global Progress Ruler" in STORY_REFRESH_PROMPT


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
