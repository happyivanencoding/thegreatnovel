from __future__ import annotations

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.power_novelty import build_power_novelty_bundle
from story_mvp.gbrain_retrieval import PLANNING_KEYWORD_QUERIES, PLANNING_KEYWORD_QUERY_BATCHES


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 力量体系与正常值
普通修士只能稳定维持一种主承载；御剑时很难同时施展另一套完整术式。
"""

STATE = {"world_vision": {"status": "author_approved"}}


def test_world_prompt_requires_reusable_social_power_rulers() -> None:
    prompt = generate_split_prompt(mode="world_vision", creative_direction="男频修仙")
    assert "力量尺必须能长期反复拿来比较" in prompt
    assert "至少建立一把世界内真实使用的当前主尺" in prompt
    assert "不要合成单一总战力分" in prompt
    assert "普通人怎样在聚落之间移动" in prompt
    assert "谁有能力跨越危险区域" in prompt


def test_power_novelty_bundle_is_reproducible_and_diverse() -> None:
    first = build_power_novelty_bundle(seed=20260826)
    second = build_power_novelty_bundle(seed=20260826)

    assert first == second
    assert first.count("## Candidate ") == 3
    labels = [line for line in first.splitlines() if line.startswith("内部标签：")]
    assert len(labels) == 3
    assert len(set(labels)) == 3
    assert "seed: 20260826" in first
    assert "每个候选最多一个主异常" in first
    assert "单一异常只负责制造独特玩法，不是削弱预算" in first
    assert "Power Asymmetry 仍应明显超标" in first


def test_power_prompt_auto_injects_noncanon_novelty_sparks() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=STATE,
        gbrain_inspiration="POWER CRAFT",
    )

    assert "Power Novelty Spark（随机扰动；非 Canon）" in prompt
    assert "熟悉幻想：" in prompt
    assert "单一异常：" in prompt
    assert "设定创新 ≠ 术语创新 ≠ 机制复杂化" in prompt
    assert "## 一句话大白话" in prompt
    assert "如果读者明天醒来得到它" in prompt
    assert "World Power Normal → Power Asymmetry" in prompt
    assert "不必先被证明为世界内合法例外" in prompt
    assert "默认强度故意偏夸张" in prompt
    assert "宁可偏强一档" in prompt
    assert "不要做对称平衡" in prompt
    assert "Core Power 必须保留一块明显的纯收益区间" in prompt
    assert "Privilege Delta" in prompt
    assert "同层普通人通常只能做到什么" in prompt
    assert "不能靠删除 Novelty Spark 的“单一异常”换来" in prompt
    assert "允许并鼓励有条件的越级威胁" in prompt
    assert "不要新增“超标坐标/比较表/评分”等输出字段" in prompt
    assert "不要让长期成长只剩数量、距离、持续时间越来越大" in prompt
    assert "Power Seed 只定义**开局 Core Asymmetry**" in prompt
    assert "后续 Story Program 可以通过真实故事获得新的 Power Asymmetry" in prompt
    assert "POWER CRAFT" in prompt


def test_power_retrieval_aliases_include_power_dominance_and_verification() -> None:
    assert "power dominance" in PLANNING_KEYWORD_QUERIES["power_seed"]
    assert "power verification" in PLANNING_KEYWORD_QUERIES["power_seed"]
    assert "public proof" in PLANNING_KEYWORD_QUERY_BATCHES["power_seed"][1]


def test_power_novelty_can_be_disabled_for_control_experiments() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=STATE,
        power_novelty="",
    )

    assert "Power Novelty Spark（随机扰动；非 Canon）" not in prompt
    assert "## 一句话大白话" in prompt
