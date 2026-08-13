from novel_authoring.progression.interpretation import interpret_reader_experience
from novel_authoring.progression.models import (
    GenreAdapterKind,
    ProgressionSubject,
)

KNOWN_SEEDS = (
    (
        "修仙",
        GenreAdapterKind.CULTIVATION_ESCALATION,
        ProgressionSubject.CHARACTER,
    ),
    (
        "团队成长",
        GenreAdapterKind.ABILITY_UNLOCK_TEAM,
        ProgressionSubject.MULTIPLE_CHARACTERS,
    ),
    (
        "宇宙成长",
        GenreAdapterKind.COSMIC_PROGRESSION,
        ProgressionSubject.CHARACTER,
    ),
    (
        "神秘学晋升",
        GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY,
        ProgressionSubject.CHARACTER,
    ),
)


def test_four_built_in_families_compile_through_one_runtime_contract() -> None:
    results = []
    for index, (metadata, adapter, subject) in enumerate(KNOWN_SEEDS, start=1):
        interpretation = interpret_reader_experience(
            "一个开放 premise。",
            genre_hint=metadata,
            contract_prefix=f"known-{index}",
        )
        assert interpretation.primary_adapter is adapter
        assert interpretation.derived_adapter_spec is None
        assert interpretation.progression_subject is subject
        results.append(interpretation)

    assert len({item.primary_adapter for item in results}) == 4


def test_known_families_do_not_collapse_into_one_trope_package() -> None:
    structures = []
    for index, (metadata, _adapter, _subject) in enumerate(KNOWN_SEEDS, start=1):
        interpretation = interpret_reader_experience(
            "一个开放 premise。",
            genre_hint=metadata,
            contract_prefix=f"trope-{index}",
        )
        structures.append(
            str(
                {
                    "adapter": interpretation.primary_adapter,
                    "subject": interpretation.progression_subject,
                    "topology": interpretation.topology,
                }
            )
        )

    forbidden_uniform_package = ("宗门", "擂台", "秘境", "学院", "传统境界")
    assert not any(
        all(word in value for value in structures) for word in forbidden_uniform_package
    )
    assert len({value for value in structures}) == 4
