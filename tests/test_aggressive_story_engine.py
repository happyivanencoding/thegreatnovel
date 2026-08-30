from story_mvp.character_prompts import (
    HUMAN_PROMPT,
    PROTAGONIST_BLIND_WORLD_TEMPLATE,
    STORY_REFRESH_PROMPT,
)
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


def test_public_proof_does_not_leak_private_power_mechanism_into_npc_knowledge() -> None:
    reviser = HYBRID_PROMPT_TEMPLATES["authority_reviser"]
    primary = HYBRID_PROMPT_TEMPLATES["primary_writer"]
    for text in (STORY_PROGRAM_TEMPLATE, OUTLINE_TEMPLATE, REVIEW_TEMPLATE):
        assert "Public Proof ≠ Hidden Mechanism Knowledge" in text
        assert "隐藏因果" in text
        assert "永久性" in text
    assert "观察反推成隐藏机制知识" in reviser
    assert "不能因为 Power Core 在 Reviser 上下文里可见" in reviser
    assert "不能因为 Chapter Mission / Power Core 向 Writer 公开" in primary
    assert "之后自然再次用出来" in primary


def test_private_persistent_power_gets_reader_proof_without_test_chapter() -> None:
    assert "上次是极限，这次已经能用" in OUTLINE_TEMPLATE
    assert "Proof 必须寄生于 Story，不反过来制造 Story" in OUTLINE_TEMPLATE
    assert "不为 Reader Proof 发明训练、复测、搬炭/护火、工作任务" in OUTLINE_TEMPLATE
    assert "这个新极限本身也会成为我的东西" in OUTLINE_TEMPLATE
    assert "目标奖励 + 可永久留下的新极限形成双重诱惑" in OUTLINE_TEMPLATE
    assert "如果这次跳成，以后这段距离就是自己的" in OUTLINE_TEMPLATE
    assert "四项有一项不成立就跳过" in OUTLINE_TEMPLATE
    assert "只写在 `## 4. 主角模型`、主题说明、主要阅读兑现或 Block Delta 里不算落实" in OUTLINE_TEMPLATE
    assert "不能压成中性的“他选择跃过去 / 继续冒险”" in OUTLINE_TEMPLATE
    reviser = HYBRID_PROMPT_TEMPLATES["authority_reviser"]
    assert "这不是应被压缩的重复证明" in reviser
    assert "没有偷偷制造更高一级新极限" in reviser
    assert "不要为了补这一原则新造第二次使用" in reviser


def test_meta_ui_reader_facing_labels_prefer_plain_concrete_facts() -> None:
    assert "还剩多久、出口/目标在哪里、能带走什么、失败会怎样" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "不要让后台设计语言或抽象状态词替读者完成理解" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "还剩多久 / 去哪里 / 能带走什么 / 失败会怎样" in STORY_REFRESH_PROMPT


def test_world_horizon_handoff_preserves_reader_facing_edge_without_prebuilding_next_world() -> None:
    assert "Reader-Facing Edge" in STORY_PROGRAM_TEMPLATE
    assert "不得为钩子提前发明下一世界答案" in STORY_PROGRAM_TEMPLATE
    assert "外缘信号" in STORY_REFRESH_PROMPT
    assert "不得为钩子预写下一世界" in STORY_REFRESH_PROMPT
