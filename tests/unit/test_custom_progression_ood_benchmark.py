import pytest

from novel_authoring.planning.innovation import (
    GenrePromiseRewardBreakdown,
    InnovationControl,
)
from novel_authoring.planning.rewards import calculate_innovation_reward
from novel_authoring.progression.diagnostics import (
    GenreChangeStatus,
    GenreStructureEvidence,
    diagnose_genre_change,
)
from novel_authoring.progression.interpretation import interpret_reader_experience
from novel_authoring.progression.models import GenreAdapterKind

OOD_CASES = (
    "这个世界的人每做出一个真正不可撤销的选择，都会失去一种未来。",
    "一座城市本身是成长主体，并会因居民协作发生变化。",
    "主角每理解一种已经灭亡的语言，就能接触不同的现实层。",
)


@pytest.mark.parametrize("seed", OOD_CASES)
def test_ood_premise_does_not_synthesize_a_bespoke_grammar(seed: str) -> None:
    interpretation = interpret_reader_experience(seed, contract_prefix="ood")

    assert interpretation.primary_adapter is GenreAdapterKind.CUSTOM
    assert interpretation.derived_adapter_spec is None


def test_nontraditional_payoff_enters_existing_reward_after_gate() -> None:
    reward = calculate_innovation_reward(
        None,
        InnovationControl(),
        base_candidate_score=60,
        eligible=True,
        genre_promise_reward=GenrePromiseRewardBreakdown(
            reader_promise_alignment=2,
            progression_payoff=2,
            world_expansion_utility=1,
            genre_evolution_value=1,
            total_reward=6,
        ),
    )

    assert reward.eligible is True
    assert reward.genre_promise_reward.total_reward == 6
    assert reward.final_selection_score > reward.base_candidate_score
    assert reward.capped_innovation_reward <= reward.reward_cap


def test_custom_progression_evolution_preserves_core_promise() -> None:
    result = diagnose_genre_change(
        GenreStructureEvidence(
            progression_gate_affects_causality=True,
            extraordinary_resource_affects_choice=True,
            power_opens_space=True,
            core_promise_preserved=True,
            delivery_channel_changed=True,
            evidence=["个人选择权柄逐步转为集体规则塑造，但可能性扩张仍是核心"],
        )
    )

    assert result.drift.status is GenreChangeStatus.CLEAR
    assert result.evolution.status is GenreChangeStatus.GENRE_EVOLUTION
    assert result.drift.hard_failure is False
