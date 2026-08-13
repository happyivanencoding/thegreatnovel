import inspect

import pytest

from novel_authoring.progression.interpretation import (
    READER_EXPERIENCE_UI,
    ReaderExperienceAdjustment,
    adjust_reader_experience,
    apply_reader_experience_overrides,
    interpret_reader_experience,
)
from novel_authoring.progression.models import (
    ExperiencePriority,
    GenreAdapterKind,
    ReaderExperience,
)
from novel_authoring.serial_kernel import classification
from novel_authoring.serial_kernel.classification import (
    align_narrative_drive_to_reader_experience,
)
from novel_authoring.serial_kernel.models import NarrativeDrive, NarrativeEngineType


def test_explicit_genre_metadata_can_select_a_builtin_adapter() -> None:
    value = interpret_reader_experience(
        "一个生产代码从未见过的开放前提。",
        genre_hint="近未来 / 肉身进化",
        contract_prefix="body-seed",
    )

    assert value.primary_adapter is GenreAdapterKind.MYTHIC_BODY_ANCIENT_WORLD
    assert value.derived_adapter_spec is None


def test_unknown_premise_keeps_open_semantics() -> None:
    value = interpret_reader_experience("一个人寻找失踪姐姐的故事。")

    assert value.narrative_drive.drive_contract.primary_drive is NarrativeDrive.CUSTOM
    assert value.primary_adapter is GenreAdapterKind.CUSTOM
    assert value.derived_adapter_spec is None
    assert set(value.reader_contract.experience_priorities.values()) == {
        ExperiencePriority.MEDIUM
    }


def test_direct_reader_hint_can_fill_an_unresolved_primary() -> None:
    value = interpret_reader_experience("一个生产代码从未见过的开放前提。")
    adjusted = apply_reader_experience_overrides(
        value.reader_contract,
        {
            "RESOURCE_OPPORTUNITY": ExperiencePriority.VERY_HIGH,
            "MYSTERY": ExperiencePriority.HIGH,
        },
    )
    aligned = align_narrative_drive_to_reader_experience(value.narrative_drive, adjusted)

    assert aligned.drive_contract.primary_drive is NarrativeDrive.RESOURCE_OPPORTUNITY
    assert NarrativeDrive.MYSTERY_INVESTIGATION in aligned.drive_contract.secondary_drives


@pytest.mark.parametrize("experience", ["PROGRESSION", "BREAKTHROUGH", "COMBAT"])
def test_broad_experience_does_not_force_power_progression(experience: str) -> None:
    value = interpret_reader_experience("一个生产代码从未见过的开放前提。")
    adjusted = apply_reader_experience_overrides(
        value.reader_contract, {experience: ExperiencePriority.VERY_HIGH}
    )

    aligned = align_narrative_drive_to_reader_experience(value.narrative_drive, adjusted)

    assert aligned.drive_contract.primary_drive is not NarrativeDrive.POWER_PROGRESSION


def test_survival_primary_and_progression_engine_can_coexist() -> None:
    value = interpret_reader_experience(
        "一名普通人被困在持续变化的环境中，每天只能做一次不可逆选择。",
        genre_hint="生存升级 / 都市异常 / 资源管理 / 轻悬疑",
    )
    adjusted = apply_reader_experience_overrides(
        value.reader_contract,
        {
            "SURVIVAL": "CORE",
            "RESOURCE_OPPORTUNITY": "CORE",
            "PROGRESSION": "CORE",
            "BREAKTHROUGH": "STRONG",
            "ARTIFACT_OR_ABILITY": "CORE",
            "MYSTERY": "STRONG",
            "REVEAL": "SECONDARY",
            "COMBAT": "SECONDARY",
        },
    )

    aligned = align_narrative_drive_to_reader_experience(value.narrative_drive, adjusted)

    assert aligned.drive_contract.primary_drive is NarrativeDrive.SURVIVAL_RESOURCE
    assert aligned.progression_engine_enabled is True
    assert aligned.drive_contract.progression_engine_enabled is True
    assert NarrativeEngineType.PROGRESSION in aligned.enabled_engines
    assert NarrativeDrive.RESOURCE_OPPORTUNITY in aligned.drive_contract.secondary_drives
    assert NarrativeDrive.MYSTERY_INVESTIGATION in aligned.drive_contract.secondary_drives


def test_all_reader_experiences_have_one_author_visible_ui_declaration() -> None:
    keys = [item["key"] for item in READER_EXPERIENCE_UI]

    assert len(keys) == len(set(keys)) == len(ReaderExperience)
    assert set(keys) == {item.value for item in ReaderExperience}


def test_reader_adjustment_is_author_review_before_contracts() -> None:
    value = interpret_reader_experience("一个开放前提。")
    adjusted = adjust_reader_experience(
        value.reader_contract,
        ReaderExperienceAdjustment.PAYOFF_STRONGER,
    )

    assert adjusted.experience_priorities[ReaderExperience.COMBAT] is (
        ExperiencePriority.VERY_HIGH
    )
    assert adjusted.status.value == "NEEDS_REVIEW"


def test_old_bespoke_literals_are_absent_from_production_classifiers() -> None:
    source = inspect.getsource(classification._drive_mix) + inspect.getsource(
        classification._market_categories
    )

    for literal in (
        "城市本身是成长主体",
        "灭亡的语言",
        "失去一种未来",
        "不存在的房间",
        "地方官",
        "医生",
        "恒星",
    ):
        assert literal not in source
