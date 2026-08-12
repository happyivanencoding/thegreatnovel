from __future__ import annotations

import pytest

from novel_authoring.progression.adapters import (
    BUILTIN_GENRE_ADAPTERS,
    compile_genre_adapters,
    effective_genre_contract,
)
from novel_authoring.progression.derived import compile_derived_adapter
from novel_authoring.progression.models import (
    AuthoringPreset,
    ContractStatus,
    DerivedAdapterSpec,
    EffectiveGenreContract,
    ExperiencePriority,
    ExplanationStyle,
    GenreAdapterKind,
    PayoffChannel,
    PrimaryFamily,
    ProgressionDeltaType,
    ProgressionSubject,
    ProgressionTopology,
    ReaderExperience,
    ReaderExperienceContract,
    RuntimeGenreCapabilities,
    SettingSkin,
)
from novel_authoring.progression.presets import (
    BUILTIN_STORY_PROFILES,
    compile_story_profile,
)


def reader_contract(**overrides: object) -> ReaderExperienceContract:
    payload: dict[str, object] = {
        "contract_id": "reader-near-future-body",
        "primary_family": PrimaryFamily.PROGRESSION_FANTASY,
        "secondary_families": [PrimaryFamily.COSMIC_PROGRESSION],
        "setting_skin": SettingSkin.NEAR_FUTURE,
        "experience_priorities": {
            ReaderExperience.PROGRESSION: ExperiencePriority.VERY_HIGH,
            ReaderExperience.POWER_VERIFICATION: ExperiencePriority.VERY_HIGH,
            ReaderExperience.WORLD_EXPANSION: ExperiencePriority.HIGH,
            ReaderExperience.SOCIAL_THEME: ExperiencePriority.LOW,
        },
        "growth_centrality": ExperiencePriority.VERY_HIGH,
        "world_expansion_centrality": ExperiencePriority.HIGH,
        "mystery_centrality": ExperiencePriority.MEDIUM,
        "team_centrality": ExperiencePriority.LOW,
        "relationship_centrality": ExperiencePriority.MEDIUM,
        "theme_centrality": ExperiencePriority.LOW,
        "explanation_style": ExplanationStyle.MIXED_MYSTICAL,
        "must_deliver": ["成长必须持续扩大行动可能性"],
        "status": ContractStatus.NEEDS_REVIEW,
    }
    payload.update(overrides)
    return ReaderExperienceContract.model_validate(payload)


def test_reader_experience_contract_validates_priorities() -> None:
    contract = reader_contract()

    assert contract.experience_priorities[ReaderExperience.PROGRESSION] is (
        ExperiencePriority.VERY_HIGH
    )
    assert contract.status is ContractStatus.NEEDS_REVIEW


def test_reader_experience_cannot_disable_every_priority() -> None:
    with pytest.raises(ValueError, match="不能全部关闭"):
        reader_contract(
            experience_priorities={
                ReaderExperience.PROGRESSION: ExperiencePriority.OFF,
                ReaderExperience.COMBAT: ExperiencePriority.OFF,
            }
        )


def test_setting_skin_cannot_replace_primary_genre() -> None:
    contract = reader_contract(
        primary_family=PrimaryFamily.PROGRESSION_FANTASY,
        setting_skin=SettingSkin.NEAR_FUTURE,
    )

    assert contract.primary_family is PrimaryFamily.PROGRESSION_FANTASY
    assert contract.setting_skin is SettingSkin.NEAR_FUTURE


def test_primary_family_cannot_be_duplicated_as_secondary() -> None:
    with pytest.raises(ValueError, match="primary_family"):
        reader_contract(
            secondary_families=[
                PrimaryFamily.PROGRESSION_FANTASY,
                PrimaryFamily.COSMIC_PROGRESSION,
            ]
        )


def test_story_profile_compiles_into_contract_proposal() -> None:
    profile = BUILTIN_STORY_PROFILES[
        AuthoringPreset.CHINESE_MALE_COMMERCIAL_PROGRESSION
    ]

    proposal = compile_story_profile(
        profile,
        contract_id="reader-from-profile",
        primary_family=PrimaryFamily.PROGRESSION_FANTASY,
        setting_skin=SettingSkin.NEAR_FUTURE,
        priority_overrides={ReaderExperience.SOCIAL_THEME: ExperiencePriority.OFF},
    )

    assert proposal.status is ContractStatus.NEEDS_REVIEW
    assert proposal.experience_priorities[ReaderExperience.PROGRESSION] is (
        ExperiencePriority.VERY_HIGH
    )
    assert proposal.experience_priorities[ReaderExperience.SOCIAL_THEME] is (
        ExperiencePriority.OFF
    )
    assert "profile" not in type(proposal).model_fields


def test_profile_name_is_not_part_of_compiled_runtime_shape() -> None:
    profile = BUILTIN_STORY_PROFILES[
        AuthoringPreset.CHINESE_MALE_COMMERCIAL_PROGRESSION
    ]
    proposal = compile_story_profile(
        profile,
        contract_id="reader-runtime-shape",
        primary_family=PrimaryFamily.TEAM_PROGRESSION,
        setting_skin=SettingSkin.OTHERWORLD,
    )

    payload = proposal.model_dump(mode="json")
    assert "profile_id" not in payload
    assert "CHINESE_MALE_COMMERCIAL_PROGRESSION" not in str(payload)


def test_genre_adapters_can_compose_without_runtime_identity() -> None:
    contract = compile_genre_adapters(
        reader_contract(),
        genre_contract_id="genre-composed",
        primary_adapter=BUILTIN_GENRE_ADAPTERS[
            GenreAdapterKind.ABILITY_UNLOCK_TEAM
        ],
        secondary_adapters=[
            BUILTIN_GENRE_ADAPTERS[GenreAdapterKind.COSMIC_PROGRESSION]
        ],
    )

    assert contract.capabilities.has_team_progression is True
    assert contract.capabilities.has_world_expansion is True
    assert contract.capabilities.has_knowledge_gate is True
    assert "adapter" not in type(contract).model_fields


def test_adapter_compiles_into_effective_contract() -> None:
    proposal = compile_genre_adapters(
        reader_contract(),
        genre_contract_id="genre-occult",
        primary_adapter=BUILTIN_GENRE_ADAPTERS[
            GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY
        ],
    )
    effective = effective_genre_contract(
        proposal.model_copy(update={"status": ContractStatus.EFFECTIVE})
    )

    assert effective.capabilities.has_mystery_binding is True
    assert effective.capabilities.has_knowledge_gate is True
    assert "adapter_id" not in effective.model_dump(mode="json")


def test_runtime_contract_does_not_require_adapter_identity() -> None:
    effective = EffectiveGenreContract(
        genre_contract_id="genre-custom-runtime",
        reader_experience_contract_id="reader-near-future-body",
        promises=[],
        payoff_channels=[],
        capabilities=RuntimeGenreCapabilities(has_progression_axis=True),
    )

    assert effective.capabilities.has_progression_axis is True


def test_derived_adapter_supports_unknown_progression_grammar() -> None:
    spec = DerivedAdapterSpec(
        spec_id="derived-lost-futures",
        progression_subject=ProgressionSubject.CHARACTER,
        growth_object="被放弃的未来与现实可能性权柄",
        progression_topology=[
            ProgressionTopology.BRANCHING,
            ProgressionTopology.TRADEOFF,
        ],
        delta_types=[
            ProgressionDeltaType.BRANCH,
            ProgressionDeltaType.SACRIFICE,
            ProgressionDeltaType.LOCK_OUT,
        ],
        growth_resources=["已经放弃的未来"],
        growth_gates=["作出真正不可撤销的选择"],
        growth_costs=["永久失去一条人生路线"],
        verification_modes=["现实开始服从新的可能性权柄"],
        unlock_logic="每次不可逆选择将一条失去的未来转化为可使用权柄",
        world_expansion_relation="选择越多，现实可被重写的层次越深",
        reader_visible_progress=["失去的未来", "可使用权柄", "永久锁死的路线"],
        long_term_ceiling_logic="上限由仍可牺牲的真实未来和承担后果的能力共同决定",
        payoff_logic=["选择产生不可逆后果", "失去的未来改变现实"],
        capabilities=RuntimeGenreCapabilities(
            has_progression_axis=True,
            has_verification_requirement=True,
            has_world_expansion=True,
        ),
        payoff_channels=[
            PayoffChannel.TRANSFORMATION,
            PayoffChannel.STRATEGIC_ADVANTAGE,
        ],
    )
    custom_adapter = compile_derived_adapter(spec)
    contract = compile_genre_adapters(
        reader_contract(primary_family=PrimaryFamily.CUSTOM),
        genre_contract_id="genre-lost-futures",
        primary_adapter=custom_adapter,
    )

    assert spec.progression_topology == [
        ProgressionTopology.BRANCHING,
        ProgressionTopology.TRADEOFF,
    ]
    assert ProgressionDeltaType.LOCK_OUT in spec.delta_types
    assert contract.capabilities.has_progression_axis is True
    assert "CULTIVATION" not in str(contract.model_dump(mode="json"))


def test_progression_subject_supports_non_character_subjects() -> None:
    spec = DerivedAdapterSpec(
        spec_id="derived-growing-city",
        progression_subject=ProgressionSubject.SETTLEMENT,
        growth_object="城市共同解决问题后获得的新自然法则",
        progression_topology=[ProgressionTopology.NETWORK],
        delta_types=[ProgressionDeltaType.UNLOCK, ProgressionDeltaType.TRANSFORM],
        growth_resources=["居民共同解决问题的经验"],
        growth_gates=["共同解决一种此前无法解决的问题"],
        growth_costs=["新法则改变所有居民的生活条件"],
        verification_modes=["城市地图、居民权限或自然规则真实改变"],
        unlock_logic="集体解决能力转化为城市法则",
        world_expansion_relation="每条新法则扩大城市与外界互动范围",
        reader_visible_progress=["城市能力", "居民权限", "地图变化"],
        long_term_ceiling_logic="由城市能够共同理解和解决的问题复杂度决定",
        payoff_logic=["新自然法则改变集体行动方式"],
        capabilities=RuntimeGenreCapabilities(
            has_progression_axis=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_world_expansion=True,
            has_team_progression=True,
        ),
        payoff_channels=[
            PayoffChannel.TEAM_GROWTH,
            PayoffChannel.WORLD_EXPANSION,
        ],
    )

    assert spec.progression_subject is ProgressionSubject.SETTLEMENT
    assert compile_derived_adapter(spec).capabilities.has_team_progression is True


def test_knowledge_progression_does_not_require_combat() -> None:
    spec = DerivedAdapterSpec(
        spec_id="derived-dead-languages",
        progression_subject=ProgressionSubject.CHARACTER,
        growth_object="理解已灭亡语言后进入对应文明的现实层",
        progression_topology=[ProgressionTopology.NETWORK],
        delta_types=[ProgressionDeltaType.UNLOCK, ProgressionDeltaType.BRANCH],
        growth_resources=["语言材料", "文明语境"],
        growth_gates=["真正理解一种已灭亡语言"],
        growth_costs=["承担该文明认知方式带来的视野改变"],
        verification_modes=["进入该文明曾经理解过的现实层"],
        unlock_logic="知识理解直接打开现实访问权限",
        world_expansion_relation="每种语言打开一个结构不同的现实层",
        reader_visible_progress=["可理解语言", "可进入现实层"],
        long_term_ceiling_logic="由文明认知差异和可建立的跨层连接决定",
        payoff_logic=["知识解谜", "现实层发现", "新访问权限"],
        capabilities=RuntimeGenreCapabilities(
            has_progression_axis=True,
            has_knowledge_gate=True,
            has_verification_requirement=True,
            has_world_expansion=True,
            has_mystery_binding=True,
        ),
        payoff_channels=[
            PayoffChannel.KNOWLEDGE_GAIN,
            PayoffChannel.DISCOVERY,
            PayoffChannel.WORLD_EXPANSION,
        ],
    )

    assert PayoffChannel.COMBAT_DOMINANCE not in spec.payoff_channels
    assert compile_derived_adapter(spec).capabilities.has_knowledge_gate is True
