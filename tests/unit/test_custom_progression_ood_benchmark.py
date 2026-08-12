import pytest

from novel_authoring.planning.innovation import (
    GenrePromiseRewardBreakdown,
    InnovationControl,
)
from novel_authoring.planning.rewards import calculate_innovation_reward
from novel_authoring.progression.anticipation import (
    AnticipationItem,
    AnticipationSource,
    AnticipationSurfaceView,
)
from novel_authoring.progression.diagnostics import (
    GenreChangeStatus,
    GenreStructureEvidence,
    diagnose_genre_change,
)
from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.models import (
    PayoffChannel,
    ProgressionDeltaType,
    ProgressionSubject,
    ProgressionTopology,
)
from novel_authoring.progression.scheduler import (
    ChapterIntent,
    recommend_chapter_intent,
)

OOD_CASES = (
    (
        "这个世界的人每做出一个真正不可撤销的选择，都会失去一种未来。"
        "主角却能使用自己失去的未来作为力量。",
        ProgressionSubject.CHARACTER,
        {ProgressionTopology.BRANCHING, ProgressionTopology.TRADEOFF},
        {ProgressionDeltaType.SACRIFICE, ProgressionDeltaType.LOCK_OUT},
        PayoffChannel.STRATEGIC_ADVANTAGE,
        ChapterIntent.CONTINUITY_ADVANCE,
    ),
    (
        "一座城市本身是成长主体。每当居民共同解决一种此前无法解决的问题，"
        "城市就会获得一条新的自然法则。",
        ProgressionSubject.SETTLEMENT,
        {ProgressionTopology.NETWORK, ProgressionTopology.ACCUMULATIVE},
        {ProgressionDeltaType.UNLOCK, ProgressionDeltaType.MERGE},
        PayoffChannel.TEAM_GROWTH,
        ChapterIntent.TEAM_GROWTH,
    ),
    (
        "主角没有战斗能力。他每真正理解一种已经灭亡的语言，"
        "就能进入那个文明曾经理解过的现实层。",
        ProgressionSubject.CHARACTER,
        {ProgressionTopology.NETWORK, ProgressionTopology.TRANSFORMATIVE},
        {ProgressionDeltaType.UNLOCK, ProgressionDeltaType.TRANSFORM},
        PayoffChannel.KNOWLEDGE_GAIN,
        ChapterIntent.MYSTERY_ADVANCE,
    ),
)


@pytest.mark.parametrize(
    (
        "seed",
        "subject",
        "topologies",
        "delta_types",
        "payoff_channel",
        "expected_intent",
    ),
    OOD_CASES,
)
def test_ood_grammar_compiles_and_runs_without_builtin_adapter_identity(
    seed: str,
    subject: ProgressionSubject,
    topologies: set[ProgressionTopology],
    delta_types: set[ProgressionDeltaType],
    payoff_channel: PayoffChannel,
    expected_intent: ChapterIntent,
) -> None:
    interpretation = interpret_reader_experience(seed, contract_prefix="ood")
    bundle = compile_kernel_contract_proposals(interpretation)
    spec = interpretation.derived_adapter_spec

    assert spec is not None
    assert bundle.derived_adapter_spec == spec
    assert bundle.progression.progression_subject is subject
    assert topologies.issubset(set(bundle.progression.topology))
    assert delta_types.issubset(set(bundle.progression.allowed_delta_types))
    assert payoff_channel in bundle.payoff_channels.channels
    assert bundle.genre.capabilities == spec.capabilities

    anticipation = AnticipationSurfaceView(
        chapter_id="chapter-8",
        chapter_ordinal=8,
        items=[
            AnticipationItem(
                anticipation_id="ood-payoff",
                subject=spec.payoff_logic[0],
                source=AnticipationSource.PAYOFF_READINESS,
                source_reference_id=spec.spec_id,
                urgency=4,
                expected_payoff_channel=payoff_channel,
                expected_horizon="MID",
                risk_if_delayed="原创成长因果长期未兑现",
            )
        ],
    )
    recommendation = recommend_chapter_intent(debts=[], anticipation=anticipation)
    assert recommendation.primary_intent is expected_intent
    assert recommendation.supporting_anticipation_ids == ["ood-payoff"]

    runtime_surface = str(
        {
            "axis": bundle.progression.primary_axis.model_dump(mode="json"),
            "resources": bundle.progression.resource_economy,
            "payoffs": spec.payoff_logic,
            "world": bundle.world_expansion.model_dump(mode="json"),
        }
    )
    assert all(word not in runtime_surface for word in ("宗门", "秘境", "学院", "擂台"))


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
