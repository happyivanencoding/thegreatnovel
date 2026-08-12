from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.models import (
    GenreAdapterKind,
    ProgressionSubject,
    ProgressionTopology,
)

KNOWN_SEEDS = (
    (
        "一名被废除修为的少年，通过炼化万物残留的火种重新成长。",
        GenreAdapterKind.CULTIVATION_ESCALATION,
        ProgressionSubject.CHARACTER,
    ),
    (
        "每个人出生时只有一个能力槽，七名失败者组成队伍寻找第二能力。",
        GenreAdapterKind.ABILITY_UNLOCK_TEAM,
        ProgressionSubject.MULTIPLE_CHARACTERS,
    ),
    (
        "人类只能在恒星死亡后吸收残留能量，主角却能听见尚未死亡恒星的呼吸。",
        GenreAdapterKind.COSMIC_PROGRESSION,
        ProgressionSubject.CHARACTER,
    ),
    (
        "城市中的每个职业都有一条禁忌晋升路线，越接近顶层越难保留自己的身份。",
        GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY,
        ProgressionSubject.CHARACTER,
    ),
)


def test_four_built_in_families_compile_through_one_runtime_contract() -> None:
    results = []
    for index, (seed, adapter, subject) in enumerate(KNOWN_SEEDS, start=1):
        interpretation = interpret_reader_experience(
            seed,
            contract_prefix=f"known-{index}",
        )
        bundle = compile_kernel_contract_proposals(interpretation)
        assert interpretation.primary_adapter is adapter
        assert interpretation.derived_adapter_spec is None
        assert bundle.progression.progression_subject is subject
        assert bundle.progression.model_fields_set
        results.append(bundle)

    assert {type(item.progression) for item in results} == {
        type(results[0].progression)
    }
    assert len({item.progression.primary_axis.axis_type for item in results}) == 4
    assert len({tuple(item.progression.topology) for item in results}) == 4
    assert ProgressionTopology.MULTI_AXIS in results[1].progression.topology


def test_known_families_do_not_collapse_into_one_trope_package() -> None:
    structures = []
    for index, (seed, _adapter, _subject) in enumerate(KNOWN_SEEDS, start=1):
        bundle = compile_kernel_contract_proposals(
            interpret_reader_experience(seed, contract_prefix=f"trope-{index}")
        )
        structures.append(
            str(
                {
                    "axis": bundle.progression.primary_axis.model_dump(mode="json"),
                    "resources": bundle.progression.resource_economy,
                    "world": bundle.world_expansion.model_dump(mode="json"),
                }
            )
        )

    forbidden_uniform_package = ("宗门", "擂台", "秘境", "学院", "传统境界")
    assert not any(
        all(word in value for value in structures) for word in forbidden_uniform_package
    )
    assert len({value for value in structures}) == 4
