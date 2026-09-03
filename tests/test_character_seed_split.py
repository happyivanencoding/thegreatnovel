from __future__ import annotations

from story_mvp.character_seeds import (
    HUMAN_SEED_SCHEMA,
    POWER_SEED_SCHEMA,
    compose_character_card,
    extract_frozen_power_seed,
    split_character_candidates,
    split_human_seed_authorities,
)
from story_mvp.character_prompts import HUMAN_PROMPT, PROTAGONIST_BLIND_WORLD_TEMPLATE


SAMPLE = """# CHARACTER CANDIDATE 1｜甲／能力A
## World Power Normal → Exception
正常A → 异常A。
## Core Fantasy / 特殊际遇
能力A。
## Growth Compatibility｜怎样真正越来越强
正常修炼A；异常掌握A；永久边界A。
## 为什么读者会馋
想要A。
## 成长环境切片
不应进入 Power Seed。

# CHARACTER CANDIDATE 2｜乙／能力B
## World Power Normal → Exception
正常B → 异常B。
## Core Fantasy / 特殊际遇
能力B。
## Growth Compatibility｜怎样真正越来越强
正常修炼B；异常掌握B；永久边界B。
## 为什么读者会馋
想要B。
## 成长环境切片
不应进入 Power Seed。
"""


def test_split_character_candidates_preserves_order() -> None:
    cards = split_character_candidates(SAMPLE)
    assert [card["index"] for card in cards] == [1, 2]
    assert [card["title"] for card in cards] == ["甲／能力A", "乙／能力B"]


def test_extract_frozen_power_seed_excludes_biography_and_does_not_backfill_ambition() -> None:
    card = split_character_candidates(SAMPLE)[0]["text"]
    power = extract_frozen_power_seed(str(card))
    assert "正常A → 异常A" in power
    assert "能力A" in power
    assert "正常修炼A" in power
    assert "想要A" in power
    assert "成长环境切片" not in power
    assert "不应进入 Power Seed" not in power
    assert "暂不回填" in power
    assert "High-Tier Mutation" in power
    assert power.splitlines()[0] == "# FROZEN POWER SEED 1｜能力A"
    assert "甲" not in power


def test_new_seed_schemas_restore_ambition_without_story_hooks() -> None:
    assert "一句话大白话" in POWER_SEED_SCHEMA
    assert "World Power Normal → Power Asymmetry" in POWER_SEED_SCHEMA
    assert "来源不必强制是世界内的合法例外" in POWER_SEED_SCHEMA
    assert "默认宁强勿弱" in POWER_SEED_SCHEMA
    assert "主尺负责哪些基础盘、Asymmetry 改变哪一部分" in POWER_SEED_SCHEMA
    assert "不能自动把明显更高档对手的其余主尺基础优势全部清零" in POWER_SEED_SCHEMA
    assert "为什么读者会馋" in POWER_SEED_SCHEMA
    assert "High-Tier Mutation" in POWER_SEED_SCHEMA
    assert "Legendary Power State" in POWER_SEED_SCHEMA
    assert "Legendary Trajectory" not in POWER_SEED_SCHEMA
    assert "Future Legend Image" in POWER_SEED_SCHEMA
    assert "持续牵引与互相竞争的动机" in HUMAN_SEED_SCHEMA
    assert "经历是生活上下文，不是人格证明" in HUMAN_SEED_SCHEMA
    assert "生活根：" in HUMAN_SEED_SCHEMA
    assert "不得为了证明 Behavior Signature 反向新造童年" in HUMAN_SEED_SCHEMA
    assert "默认只作为低权重局部习惯" in HUMAN_SEED_SCHEMA
    assert "主角永远不是协调员" in HUMAN_SEED_SCHEMA
    assert "Audition Metadata（非 Canon）" in HUMAN_SEED_SCHEMA
    assert "Action Audition" in HUMAN_SEED_SCHEMA
    assert "机会成本" in HUMAN_SEED_SCHEMA
    assert "Initial State Seed" in HUMAN_SEED_SCHEMA
    assert "named NPC" not in HUMAN_SEED_SCHEMA


def test_world_and_human_prompts_generate_living_story_material_without_new_authority() -> None:
    assert "World Independence 要通过 Living Actors 成立" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "谁现在私人地想要什么" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "不要为此新增角色表、倒计时表或事件 schema" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "Action Audition" in HUMAN_PROMPT
    assert "不新增童年、能力、命运、使命、未来剧情" in HUMAN_PROMPT
    assert "AUDIT_ONLY / Non-Canon" in HUMAN_PROMPT


def test_split_human_seed_moves_current_desire_and_hook_out_of_core() -> None:
    human = """# HUMAN SEED CANDIDATE 1｜甲／标签
## 世界中的初始位置与生活事实
家庭A。
## 当前私人欲望
现在想买船。
## 持续牵引与互相竞争的动机
想去更远，也想留下陪人。
## 人物钩子
他当众烧掉船票。
"""
    parts = split_human_seed_authorities(human)
    assert "现在想买船" not in parts["human_core"]
    assert "当众烧掉船票" not in parts["human_core"]
    assert "现在想买船" in parts["initial_state"]
    assert "当众烧掉船票" in parts["audition_metadata"]


def test_compose_character_card_does_not_reconcile_authorities_or_persist_audition() -> None:
    human = """# HUMAN SEED CANDIDATE 1｜甲／标签
## 当前私人欲望
想出名。
## 持续牵引与互相竞争的动机
想赢，也想保住朋友。
## 人物钩子
公开挑战冠军。
"""
    card = compose_character_card(power_seed="# POWER\n能力：留住半招", human_seed=human, index=1)
    assert "能力：留住半招" in card
    assert "想赢，也想保住朋友" in card
    assert "想出名" not in card
    assert "INITIAL CHARACTER STATE" not in card
    assert "公开挑战冠军" not in card
    assert "Mutable Character State" in card
    assert "不解释为什么某段童年象征某种能力" in card
    assert "留给后续 Collision Authority" in card
