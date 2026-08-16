from __future__ import annotations

from novel_authoring.config import load_settings
from novel_authoring.metrics.gates import HardGateInput, evaluate_hard_gates

CONFIG = load_settings().metrics


def test_character_fit_below_75_is_a_soft_warning() -> None:
    gate = HardGateInput(
        character_fit_inputs={
            "motivation_alignment": 70,
            "knowledge_alignment": 70,
            "capability_alignment": 70,
            "relationship_alignment": 70,
            "emotional_continuity": 70,
        },
        style_fit_inputs=dict.fromkeys(CONFIG["style_fit"]["weights"], 100),
    )
    report = evaluate_hard_gates(gate, CONFIG)
    assert report.passed
    assert report.requires_character_bridge
    assert report.soft_warnings
    assert report.character_fit == 70


def test_hard_conflict_blocks_even_with_high_fit() -> None:
    report = evaluate_hard_gates(
        HardGateInput(
            canon_conflicts=["钥匙材质与原文冲突"],
            character_fit_inputs=dict.fromkeys(CONFIG["character_fit"]["weights"], 100),
            style_fit_inputs=dict.fromkeys(CONFIG["style_fit"]["weights"], 100),
        ),
        CONFIG,
    )
    assert not report.passed
    assert report.hard_failures == ["钥匙材质与原文冲突"]


def test_exact_character_threshold_passes() -> None:
    report = evaluate_hard_gates(
        HardGateInput(
            character_fit_inputs=dict.fromkeys(CONFIG["character_fit"]["weights"], 75),
            style_fit_inputs=dict.fromkeys(CONFIG["style_fit"]["weights"], 80),
        ),
        CONFIG,
    )
    assert report.passed
    assert not report.requires_character_bridge


def test_payoff_cooldown_is_soft_review() -> None:
    report = evaluate_hard_gates(
        HardGateInput(
            payoff_cooldown_violations=["同组爽点冷却不足"],
            character_fit_inputs=dict.fromkeys(CONFIG["character_fit"]["weights"], 80),
            style_fit_inputs=dict.fromkeys(CONFIG["style_fit"]["weights"], 80),
        ),
        CONFIG,
    )

    assert report.passed
    assert report.soft_warnings == ["payoff cooldown review: 同组爽点冷却不足"]
