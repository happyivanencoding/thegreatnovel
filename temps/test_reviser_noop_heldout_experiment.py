from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "books" / "real-exp-reviser-noop-upstream-heldout-20260830-v1"
H1 = EXP / "heldout-new-novel"
H2 = EXP / "heldout-new-novel-2"
PROTOCOL2_SHA = "E11BEFFE12F5016CA1DFB362631D3145212437A21C20BCA360B7D540C5E692E4"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def data(path: Path):
    return json.loads(read(path))


def test_candidate2_protocol_remained_frozen() -> None:
    digest = hashlib.sha256((EXP / "PROTOCOL_CANDIDATE_2.md").read_bytes()).hexdigest().upper()
    assert digest == PROTOCOL2_SHA


def test_heldout_novels_are_distinct_from_derivation_and_each_other() -> None:
    world1 = read(H1 / "WORLD_VISION.md")
    power1 = read(H1 / "POWER_SEED.md")
    world2 = read(H2 / "WORLD_VISION.md")
    power2 = read(H2 / "POWER_SEED.md")
    assert "星力阶" in world1 and "远身" in power1
    assert "鸣阶" in world2 and "借境成身" in power2
    assert "回潮楔" not in power1 + power2
    assert "分身" not in power2
    assert "远身" not in power2


def test_both_heldouts_use_first_four_consecutive_chapters() -> None:
    for book in (H1, H2):
        for chapter in range(1, 5):
            directory = book / "runs" / f"chapter-{chapter:04d}"
            assert (directory / "control_primary_body.md").exists()
            assert (directory / "treatment_primary_body.md").exists()
            assert (directory / "control_final_body.md").exists()
            assert (directory / "treatment_final_body.md").exists()


def test_candidate2_does_not_pass_reviser_noop_goal() -> None:
    result = data(H2 / "FINAL_ANALYSIS.json")
    assert result["success"]["all_directional_pass"] is False
    assert result["success"]["engineering_noop_improved"] is False
    assert result["blind"]["pairwise"]["authority"]["treatment_primary_minus_control_primary"]["mean_delta"] < 0
    assert result["blind"]["pairwise"]["authority"]["treatment_reviser_minus_treatment_primary"]["mean_delta"] > result["blind"]["pairwise"]["authority"]["control_reviser_minus_control_primary"]["mean_delta"]
    assert result["generation"]["treatment"]["exact_noop"] == 0


def test_candidate2_story_attention_signal_is_real_but_separate() -> None:
    result = data(H2 / "FINAL_ANALYSIS.json")
    assert result["blind"]["pairwise"]["story"]["treatment_primary_minus_control_primary"]["mean_delta"] > 0
    assert result["blind"]["aggregates"]["story"]["treatment_primary"]["mean_score"] > result["blind"]["aggregates"]["story"]["control_primary"]["mean_score"]


def test_medium_screen_is_faster_but_fails_authority_bar() -> None:
    timing = data(H2 / "medium-reviser-screen" / "summary.json")
    blind = data(H2 / "medium-reviser-screen" / "BLIND_SUMMARY.json")["aggregates"]
    assert timing["mean_medium_reviser_wall"] < timing["mean_high_reviser_wall"]
    assert blind["story"]["medium"]["mean_score"] >= blind["story"]["high"]["mean_score"]
    assert blind["authority"]["medium"]["mean_score"] < blind["authority"]["high"]["mean_score"]
    assert blind["authority"]["medium"]["hard_problems"] > blind["authority"]["high"]["hard_problems"]
