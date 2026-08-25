from __future__ import annotations

from story_mvp.character_seeds import (
    HUMAN_SEED_SCHEMA,
    POWER_SEED_SCHEMA,
    compose_character_card,
    extract_frozen_power_seed,
    split_character_candidates,
)


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


def test_new_seed_schemas_restore_ambition_without_story_hooks() -> None:
    assert "High-Tier Mutation" in POWER_SEED_SCHEMA
    assert "Legendary Trajectory" in POWER_SEED_SCHEMA
    assert "Future Legend Image" in POWER_SEED_SCHEMA
    assert "Core Obsession" in HUMAN_SEED_SCHEMA
    assert "Excess" in HUMAN_SEED_SCHEMA
    assert "人物钩子" in HUMAN_SEED_SCHEMA
    assert "named NPC" not in HUMAN_SEED_SCHEMA


def test_compose_character_card_does_not_reconcile_authorities() -> None:
    card = compose_character_card(power_seed="# POWER\n能力：留住半招", human_seed="# HUMAN\n欲望：想出名", index=1)
    assert "能力：留住半招" in card
    assert "欲望：想出名" in card
    assert "不解释为什么某段童年象征某种能力" in card
    assert "留给后续 Collision Authority" in card
