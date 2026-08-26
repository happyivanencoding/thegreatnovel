from __future__ import annotations

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.power_novelty import build_power_novelty_bundle


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 力量体系与正常值
普通修士只能稳定维持一种主承载；御剑时很难同时施展另一套完整术式。
"""

STATE = {"world_vision": {"status": "author_approved"}}


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
    assert "POWER CRAFT" in prompt


def test_power_novelty_can_be_disabled_for_control_experiments() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=STATE,
        power_novelty="",
    )

    assert "Power Novelty Spark（随机扰动；非 Canon）" not in prompt
    assert "## 一句话大白话" in prompt
