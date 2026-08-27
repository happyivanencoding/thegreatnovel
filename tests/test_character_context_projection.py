from __future__ import annotations

from story_mvp.character_context import (
    project_character_life_context,
    project_character_power_baseline,
    project_character_world_slice,
    project_story_opportunity_layer,
    project_writer_texture_context,
)


WORLD = """# PROTAGONIST-BLIND WORLD VISION

这是澜生界。归潮每四十八年经过一次，是所有人都知道的世界气候。

## 普通人的生活与上升
普通人住在河谷、海港、盐场、矿镇或宗族村落。可以学炼药、制符、驯兽、铸兵、辨矿、修船。

## 力量体系与正常值
普通人不会正式修行。纳息者能用小术。通脉修士属于地方精锐。照域修士极其罕见。通常不能逆转时间或真正复活。

## 社会现实与身份
世界有王朝、宗门、世家、商盟、军府。身份会受师承、城籍、军籍、商籍影响。

## 世界里真正值钱、值得想要的东西
稳定灵田、可靠地图、合适兵器、正式身份、医术和传承都很值钱。

## 世界正在发生的大事
盐商宋照雪正在买空青灯盐。退隐剑修魏停山正在讨回一把断剑。驯兽师乌芙正在寻找白角夔。

## 值得进入的地点、奇观与未知
悬瓮城城底有向上流的地下河。沉铃泽水下有古钟。古代王朝地下驿网仍在运行。

## 世界知识边界
普通人知道归潮会带来财富与灾难。
专业人士知道不同地区灵气性质不同。
顶层势力知道古代王朝拥有跨域交通技术。
当前没人能完整解释的事实：
1. 沉铃泽的古钟是谁铸造的。
2. 为什么地下驿网仍会识别旧王朝身份。

## 读者可用的世界坐标
作者知道下一层要期待悬瓮城和地下驿网。
"""


def test_character_world_slice_keeps_reality_and_normal_baseline() -> None:
    result = project_character_world_slice(WORLD)
    assert "普通人的生活与上升" in result
    assert "力量体系与正常值" in result
    assert "纳息者" in result
    assert "通脉修士" in result
    assert "照域修士极其罕见" in result
    assert "王朝、宗门、世家、商盟、军府" in result
    assert "稳定灵田" in result
    assert "普通人知道归潮" in result
    assert "World Normal → Power Asymmetry" in result
    assert "经历是背景，不是人格证明" in result
    assert "不要求所有人物从普通底层起步" in result
    assert "异常不能只是一项更高效的职业技能" in result


def test_character_world_slice_excludes_named_story_opportunities() -> None:
    result = project_character_world_slice(WORLD)
    for leaked in (
        "宋照雪",
        "魏停山",
        "乌芙",
        "白角夔",
        "悬瓮城",
        "沉铃泽",
        "地下驿网",
        "当前没人能完整解释的事实",
        "读者可用的世界坐标",
    ):
        assert leaked not in result


def test_story_opportunity_layer_collects_hidden_hooks() -> None:
    result = project_story_opportunity_layer(WORLD)
    for expected in (
        "宋照雪",
        "魏停山",
        "白角夔",
        "悬瓮城",
        "沉铃泽",
        "地下驿网",
        "当前没人能完整解释的事实",
    ):
        assert expected in result
    assert "力量体系与正常值" not in result


def test_power_baseline_is_power_authority_not_life_or_hooks() -> None:
    result = project_character_power_baseline(WORLD)
    assert "力量体系与正常值" in result
    assert "纳息者" in result
    assert "通脉修士" in result
    assert "照域修士极其罕见" in result
    assert "Core Fantasy / 特殊能力首先相对于本区块的力量" in result
    assert "不能因为人物是矿工、匠人、账房、向导等职业" in result
    assert "这是男频成长长篇" in result
    assert "不要为了“合法化”强行给世界补一套机制" in result
    assert "正常境界提升应真实增强主角基础力量" in result
    assert "默认宁可让第一稿偏强一档" in result
    assert "不要用等价代价把核心爽点抵消" in result
    assert "高阶也不会自动消失的边界" in result
    assert "普通人的生活与上升" not in result
    assert "社会现实与身份" not in result
    assert "宋照雪" not in result
    assert "地下驿网" not in result


def test_life_context_shapes_upbringing_but_not_power_exception() -> None:
    result = project_character_life_context(WORLD)
    assert "普通人的生活与上升" in result
    assert "社会现实与身份" in result
    assert "世界里真正值钱、值得想要的东西" in result
    assert "贫寒、普通、富裕、宗门家庭、军户、商人" in result
    assert "不负责决定 Core Fantasy 的异常类型" in result
    assert "力量体系与正常值" not in result
    assert "宋照雪" not in result
    assert "沉铃泽" not in result
    assert "地下驿网" not in result


def test_life_context_excludes_named_mysteries_when_world_says_facts_include() -> None:
    world = WORLD.replace("当前没人能完整解释的事实：", "当前没人能完整解释的事实包括：")
    result = project_character_life_context(world)
    assert "当前没人能完整解释的事实包括" not in result
    assert "沉铃泽" not in result
    assert "地下驿网" not in result



def test_life_context_does_not_accept_writer_texture() -> None:
    result = project_character_life_context(WORLD)
    assert "Life Texture / Human Appetite" not in result
    assert "力量体系与正常值" not in result
    assert "地下驿网" not in result


def test_writer_orientation_reference_is_bounded_relevant_and_story_hook_free() -> None:
    result = project_writer_texture_context(
        WORLD,
        relevance_text="商盟身份影响当前选择，普通人如何生活",
    )
    assert "Writer-side only" in result
    assert "Optional Reader Orientation Reference" in result
    assert "普通人的生活与上升" in result
    assert "社会现实与身份" in result
    assert "1—3 条帮助读者定向" in result
    assert "力量体系与正常值" not in result
    assert "宋照雪" not in result
    assert "沉铃泽" not in result
    assert "地下驿网" not in result

def test_writer_orientation_prioritizes_current_faction_category() -> None:
    world = WORLD.replace(
        "世界有王朝、宗门、世家、商盟、军府。身份会受师承、城籍、军籍、商籍影响。",
        "世界有王朝、宗门、世家、商盟、军府。荒原部族有独立训练法，也会与城镇交易或冲突。",
    )
    result = project_writer_texture_context(
        world,
        relevance_text="白角部迁徙后挡住南行商队，当前第一次真正碰到这个族群。",
    )
    assert "荒原部族有独立训练法" in result
    assert "宋照雪" not in result
    assert "地下驿网" not in result
