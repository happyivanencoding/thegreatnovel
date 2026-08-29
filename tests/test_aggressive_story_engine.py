from story_mvp.character_prompts import HUMAN_PROMPT, STORY_REFRESH_PROMPT
from story_mvp.character_seeds import HUMAN_SEED_SCHEMA
from story_mvp.prompts import (
    HYBRID_PROMPT_TEMPLATES,
    OUTLINE_TEMPLATE,
    REVIEW_TEMPLATE,
    STORY_PROGRAM_TEMPLATE,
)


def test_human_authority_downweights_professional_responsibility_bias() -> None:
    for text in (HUMAN_PROMPT, HUMAN_SEED_SCHEMA):
        assert "主角永远不是协调员" in text
        assert "责任" in text
        assert "低权重" in text or "大幅降权" in text


def test_planning_chain_keeps_big_direction_reward_and_variation_rules_wired() -> None:
    required = (
        "主角永远不是协调员",
        "Major Reward Anchor",
        "Plot Pace ≠ Tier Pace",
        "Rapid Growth Needs Protagonist-Specific Causality",
        "Mystery Before Settlement",
        "Effective Opponent Adaptation",
    )
    for text in (STORY_PROGRAM_TEMPLATE, OUTLINE_TEMPLATE, REVIEW_TEMPLATE):
        for marker in required:
            assert marker in text


def test_story_program_blocks_human_relevance_from_becoming_story_engine() -> None:
    assert "Character relevance 不等于 Story Engine authorization" in STORY_PROGRAM_TEMPLATE
    assert "责任、精确、审计、边界、路线、损失归因" in STORY_PROGRAM_TEMPLATE


def test_authority_reviser_aggressively_compresses_coordination_and_translates_backstage_language() -> None:
    text = HYBRID_PROMPT_TEMPLATES["authority_reviser"]
    assert "Reviser 应激进压缩成最短因果" in text
    assert "主角永远不是协调员" in text
    assert "Backstage Abstraction Translation" in text
    assert "Named Entity Continuity Sweep" in text


def test_public_proof_keeps_crowd_expert_and_repricing_as_coequal_payoffs() -> None:
    text = HYBRID_PROMPT_TEMPLATES["authority_reviser"]
    assert "Public Proof 三路并列" in text
    assert "全场鸦雀无声" in text
    assert "Ruler Calibration" in text
    assert "Behavioral Repricing" in text
    assert "没有高低之分" in text
    assert "受控实验必须保留至少一个明显更激进的真实输出" in text


def test_world_horizon_handoff_preserves_reader_facing_edge_without_prebuilding_next_world() -> None:
    assert "Reader-Facing Edge" in STORY_PROGRAM_TEMPLATE
    assert "不得为钩子提前发明下一世界答案" in STORY_PROGRAM_TEMPLATE
    assert "外缘信号" in STORY_REFRESH_PROMPT
    assert "不得为钩子预写下一世界" in STORY_REFRESH_PROMPT
