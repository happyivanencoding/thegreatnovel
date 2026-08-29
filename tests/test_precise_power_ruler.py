from __future__ import annotations

from pathlib import Path

import pytest

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.long_form_evolution import compile_current_character
from story_mvp.power_ruler import (
    CURRENT_POWER_POSITION_PREFIX,
    MACRO_RULER_HEADING,
    ROOT_RULER_HEADING,
    parse_root_precise_power_ruler,
    validate_human_seed_start,
    validate_world_expansion_ruler,
)
from story_mvp.prompts import generate_prompt
from story_mvp.prompts import (
    ASYMMETRY_REVEAL_PAYOFF_DIRECTION,
    DEFAULT_PROMPT_TEMPLATES,
    PERSISTENT_READER_RULER_DIRECTION,
)
from story_mvp.storage import (
    approve_character_artifact,
    approve_creative_artifact,
    approve_world_expansion,
    create_book,
    write_creative_artifact,
)


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人在山城、武馆和商路生活。

## 力量体系与正常值
武者以真气淬体，公开主尺长期用于招生、挑战、军职与交易。

### 精确力量主尺｜Frozen Grammar
主尺类型：大境界+数字子级
主尺名称：真气阶
精确位置格式：{大境界}{N}重
数字精度规则：每个大境界1—9重
当前可见范围：开脉1重—化域9重
当前大档位：开脉、凝罡、化域

开脉者开始稳定用真气，凝罡者可正面挡强弩，化域者是一城核心。

## 社会现实与身份
宗门、商盟和军府都会直接询问真气阶的精确位置。

## 世界里真正值钱、值得想要的东西
武技、兵器、灵药与跨州入口。

## 世界正在发生的大事
跨州商路恢复。

## 值得进入的地点、奇观与未知
中域仍未展开。

## 世界知识边界
普通人知道精确力量主尺；更高世界的具体上限未知。
"""

POWER = """# POWER SEED｜借一式
## World Power Normal → Power Asymmetry
普通武者学招需要长期练习；持有者完整看过一式后可无损复现一次。
## Core Fantasy
看懂强招，当场变成自己的一次底牌。
## 为什么读者会馋
第一次看见就能真用。
## Growth Compatibility
### 正常修炼轴
真气与身体正常成长。
### 异常掌握轴
可保存招式数量增加。
### High-Tier Mutation
旧招与新武器复合。
### 永久边界
每一式使用后仍会消失。
## Legendary Power State
见过的顶级招式都可能成为一次真实底牌。
"""

HUMAN = """# HUMAN SEED｜顾野
## 世界中的初始位置与生活事实
开局精确力量位置｜主尺：真气阶｜精确位置：开脉3重
山城普通家庭，从小在武馆外围做杂活。
## 持续牵引与互相竞争的动机
想赢、爱钱，也讨厌长期被组织控制。
## Behavior Signature
高收益时愿意冒险。
## 重要关系原点
沈照会改变他部分风险判断。
## Initial State Seed
### 当前私人欲望
赢下一场能离开山城的比赛。
## Audition Metadata（非 Canon）
### 人物钩子
看到好刀会多看一眼。
"""

MACRO = """# WORLD EXPANSION

## 新增公共现实与普通生活
中域有沿大河建立的武城群。

## 新力量 / 威胁 / 身份 / 价值尺度
### 精确力量主尺延展｜Macro
沿用主尺：真气阶
主尺语法改动：NONE
新增可见范围：化域9重—天门9重

中域公开出现更高大档天门，但仍使用同一套每境1—9重的计数语法。

## 新地点、势力与公共识别
天门武院是中域公开宗门。

## 世界人物欲望与正在发生的事
当地强者争夺跨河古塔。

## 真正值得想要或进入的东西
高阶武技和天门武院的藏兵阁。

## 仍未知的边界
中域以外仍未知。
"""

INSTANCE = """# WORLD EXPANSION

## 新增公共现实与普通生活
雾港居民靠潮钟决定出海时间。

## 新力量 / 威胁 / 身份 / 价值尺度
### 本地精确力量主尺｜Instance Grammar
主尺类型：数字序列
主尺名称：潮印序列
精确位置格式：潮印序列{N}
数字精度规则：9—0，数字越小越高
当前可见范围：潮印序列9—潮印序列3
与全局主尺关系：本地独立尺，只用于雾港世界，不改写真气阶

## 新地点、势力与公共识别
雾港议潮塔公开记录本地序列。

## 世界人物欲望与正在发生的事
船主们争夺深雾航线。

## 真正值得想要或进入的东西
深雾航线与潮印遗物。

## 仍未知的边界
序列2以上的来源未知。
"""


def _state(approved: bool = True) -> dict[str, dict[str, str]]:
    value = "author_approved" if approved else "draft"
    return {
        "world_vision": {"status": value},
        "power_seed": {"status": "draft"},
        "human_seed": {"status": "draft"},
        "character_card": {"status": "draft"},
        "proposal": {"status": "draft"},
    }


def test_root_ruler_is_exact_and_coarse_world_is_rejected() -> None:
    ruler = parse_root_precise_power_ruler(WORLD)
    assert ruler.name == "真气阶"
    assert ruler.position_format == "{大境界}{N}重"
    assert ruler.numeric_rule == "每个大境界1—9重"
    assert ruler.visible_range == "开脉1重—化域9重"

    coarse = WORLD.replace(
        f"\n{ROOT_RULER_HEADING}\n主尺类型：大境界+数字子级\n主尺名称：真气阶\n精确位置格式：{{大境界}}{{N}}重\n数字精度规则：每个大境界1—9重\n当前可见范围：开脉1重—化域9重\n当前大档位：开脉、凝罡、化域\n",
        "",
    )
    with pytest.raises(ValueError, match="精确力量主尺"):
        parse_root_precise_power_ruler(coarse)


def test_world_approval_hard_gates_precise_ruler(tmp_path: Path) -> None:
    create_book("ruler", tmp_path)
    coarse = "# PROTAGONIST-BLIND WORLD VISION\n\n## 力量体系与正常值\n开脉、凝罡、化域。"
    write_creative_artifact("ruler", "world_vision", coarse, tmp_path, origin="author_edited")
    with pytest.raises(ValueError, match="精确力量主尺"):
        approve_creative_artifact("ruler", "world_vision", tmp_path)

    write_creative_artifact("ruler", "world_vision", WORLD, tmp_path, origin="author_edited")
    approve_creative_artifact("ruler", "world_vision", tmp_path)


def test_human_start_position_is_exact_and_must_match_world_ruler() -> None:
    validate_human_seed_start(HUMAN, WORLD)
    with pytest.raises(ValueError, match="缺少.*开局精确力量位置"):
        validate_human_seed_start(HUMAN.replace("开局精确力量位置｜主尺：真气阶｜精确位置：开脉3重\n", ""), WORLD)
    with pytest.raises(ValueError, match="不一致"):
        validate_human_seed_start(HUMAN.replace("主尺：真气阶", "主尺：魂力"), WORLD)


def test_character_approval_hard_gates_initial_exact_position(tmp_path: Path) -> None:
    create_book("character-ruler", tmp_path)
    write_creative_artifact("character-ruler", "world_vision", WORLD, tmp_path, origin="author_edited")
    approve_creative_artifact("character-ruler", "world_vision", tmp_path)
    write_creative_artifact("character-ruler", "power_seed", POWER, tmp_path, origin="author_edited")
    bad_human = HUMAN.replace("开局精确力量位置｜主尺：真气阶｜精确位置：开脉3重\n", "")
    write_creative_artifact("character-ruler", "human_seed", bad_human, tmp_path, origin="author_edited")
    with pytest.raises(ValueError, match="开局精确力量位置"):
        approve_character_artifact("character-ruler", tmp_path)

    write_creative_artifact("character-ruler", "human_seed", HUMAN, tmp_path, origin="author_edited")
    approve_character_artifact("character-ruler", tmp_path)


def test_macro_expansion_can_only_extend_range_and_instance_gets_local_exact_ruler() -> None:
    validate_world_expansion_ruler(MACRO, WORLD, scope="macro")
    validate_world_expansion_ruler(INSTANCE, WORLD, scope="instance")

    changed_grammar = MACRO.replace("主尺语法改动：NONE", "主尺语法改动：改成初期/中期/后期")
    with pytest.raises(ValueError, match="必须为 NONE"):
        validate_world_expansion_ruler(changed_grammar, WORLD, scope="macro")


def test_approved_macro_expansion_is_hard_gated(tmp_path: Path) -> None:
    create_book("expand-ruler", tmp_path)
    write_creative_artifact("expand-ruler", "world_vision", WORLD, tmp_path, origin="author_edited")
    approve_creative_artifact("expand-ruler", "world_vision", tmp_path)
    with pytest.raises(ValueError, match="精确力量主尺延展"):
        approve_world_expansion(
            "expand-ruler",
            "# WORLD EXPANSION\n\n## 新增公共现实与普通生活\n中域武城群。",
            tmp_path,
            scope="macro",
            effective_from=1,
        )
    assert approve_world_expansion(
        "expand-ruler", MACRO, tmp_path, scope="macro", effective_from=1
    )["status"] == "approved"


def test_world_and_human_prompts_receive_frozen_precise_ruler() -> None:
    human_prompt = generate_split_prompt(
        mode="human_seed",
        creative_state=_state(),
        world_vision=WORLD,
    )
    assert "FROZEN PRECISE POWER RULER GRAMMAR" in human_prompt
    assert "开局精确力量位置" in human_prompt
    assert "真气阶" in human_prompt

    expansion_prompt = generate_split_prompt(
        mode="world_expansion",
        creative_state=_state(),
        world_vision=WORLD,
        evolution_scope="macro",
        effective_from_chapter=101,
    )
    assert "FROZEN PRECISE POWER RULER GRAMMAR" in expansion_prompt
    assert MACRO_RULER_HEADING in expansion_prompt
    assert "主尺语法改动：NONE" in expansion_prompt


def test_state_prompt_carries_only_precise_ruler_and_current_position_authority() -> None:
    character = f"""# CHARACTER CARD 1｜Split Authority

## POWER CORE｜Frozen Authority
{POWER}

## HUMAN CORE｜Frozen Authority
{HUMAN}

## Composition Boundary
X
"""
    book = """# 当前状态、未兑现承诺与作者备注
## ACTIVE SCENE STATE
当前地点：山城。

## PERSISTENT CANON
### Power / Capability
Current Power Position｜主尺：真气阶｜精确位置：开脉4重
顾野仍保有借一式。

## RECENT SUMMARIES
第1章：顾野赢下一战。

## OPEN PROMISES
无。

## AUTHOR NOTES
无。
"""
    prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=book,
        world_vision=WORLD,
        character_card=character,
        chapter_number=2,
        chapter_prose="顾野打赢凝罡1重对手，但修为仍是开脉4重。",
    )
    assert "PRECISE POWER RULER AUTHORITY" in prompt
    assert "当前可见范围：开脉1重—化域9重" in prompt
    assert "CURRENT / INITIAL POWER POSITION AUTHORITY" in prompt
    assert "Current Power Position｜主尺：真气阶｜精确位置：开脉4重" in prompt
    assert "打赢更高等级对手" in prompt


def test_current_character_promotes_exact_current_position_over_initial_position() -> None:
    character = f"""# CHARACTER CARD 1｜Split Authority

## POWER CORE｜Frozen Authority
{POWER}

## HUMAN CORE｜Frozen Authority
{HUMAN}

## Composition Boundary
X
"""
    status = """## ACTIVE SCENE STATE
当前地点：州府。

## PERSISTENT CANON
### Power / Capability
Current Power Position｜主尺：真气阶｜精确位置：凝罡2重
顾野已能保存三式。
"""
    compiled = compile_current_character(
        character_card=character,
        status_text=status,
        human_development="",
        chapter_number=20,
    )
    assert "## Current Power Position｜Exact Public Ruler" in compiled
    assert "Current Power Position｜主尺：真气阶｜精确位置：凝罡2重" in compiled
    assert "开局精确力量位置｜主尺：真气阶｜精确位置：开脉3重" in compiled


def test_current_character_falls_back_to_frozen_t0_position_before_first_canon_update() -> None:
    character = f"""# CHARACTER CARD 1｜Split Authority

## POWER CORE｜Frozen Authority
{POWER}

## HUMAN CORE｜Frozen Authority
{HUMAN}

## Composition Boundary
X
"""
    compiled = compile_current_character(
        character_card=character,
        status_text="## PERSISTENT CANON\n暂无。",
        human_development="",
        chapter_number=1,
    )
    assert f"{CURRENT_POWER_POSITION_PREFIX}主尺：真气阶｜精确位置：开脉3重" in compiled


def test_precise_ruler_is_wired_into_all_three_public_proof_lanes() -> None:
    assert "三条线的共同坐标" in ASYMMETRY_REVEAL_PAYOFF_DIRECTION
    assert "群体震动" in ASYMMETRY_REVEAL_PAYOFF_DIRECTION
    assert "当前精确位置" in ASYMMETRY_REVEAL_PAYOFF_DIRECTION
    assert "Ruler Calibration" in ASYMMETRY_REVEAL_PAYOFF_DIRECTION
    assert "Behavioral Repricing" in ASYMMETRY_REVEAL_PAYOFF_DIRECTION
    assert "不能把“赢了高等级”反推成主角等级自动提升" in ASYMMETRY_REVEAL_PAYOFF_DIRECTION

    ruler = PERSISTENT_READER_RULER_DIRECTION
    assert "唯一 `Current Power Position`" in ruler
    assert "43级对58级" in ruler
    assert "精确位置是公开坐标，不是胜负公式" in ruler

    reviser = DEFAULT_PROMPT_TEMPLATES["authority_reviser"]
    assert "Public Proof 三路并列，并共享精确力量尺" in reviser
    assert "43级对58级" in reviser
    assert "State 仍是43级" in reviser
