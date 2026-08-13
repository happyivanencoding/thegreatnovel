from __future__ import annotations

import pytest

from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.serial_kernel import (
    MarketCategory,
    NarrativeDrive,
    NarrativeDriveContract,
    NarrativeEngineType,
    adjust_narrative_drive_interpretation,
    interpret_narrative_drives,
    market_category_label,
    narrative_drive_label,
)


@pytest.mark.parametrize(
    ("metadata", "primary", "secondary", "progression_enabled"),
    [
        (
            "生存 / 资源管理",
            NarrativeDrive.SURVIVAL_RESOURCE,
            {NarrativeDrive.RESOURCE_OPPORTUNITY},
            False,
        ),
        (
            "修仙",
            NarrativeDrive.POWER_PROGRESSION,
            {NarrativeDrive.RESOURCE_OPPORTUNITY},
            True,
        ),
        (
            "职业 / 都市",
            NarrativeDrive.CAREER_MASTERY,
            {NarrativeDrive.STATUS_RISE},
            False,
        ),
        (
            "治理 / 建设 / 历史",
            NarrativeDrive.STATE_BUILDING,
            {NarrativeDrive.POLITICAL_STRATEGY},
            False,
        ),
        (
            "竞技 / 电竞",
            NarrativeDrive.COMPETITIVE_SKILL,
            {
                NarrativeDrive.COMPETITIVE_RANK,
                NarrativeDrive.TEAM_GROWTH,
            },
            False,
        ),
        (
            "悬疑",
            NarrativeDrive.MYSTERY_INVESTIGATION,
            {NarrativeDrive.MYSTERY_REVELATION},
            False,
        ),
    ],
)
def test_synthetic_seeds_classify_drive_mix_without_forcing_progression(
    metadata: str,
    primary: NarrativeDrive,
    secondary: set[NarrativeDrive],
    progression_enabled: bool,
) -> None:
    result = interpret_narrative_drives(
        "一个生产代码从未见过的开放 premise。",
        market_hint=metadata,
        contract_prefix="seed",
    )

    assert result.drive_contract.primary_drive is primary
    assert set(result.drive_contract.secondary_drives) == secondary
    assert result.progression_engine_enabled is progression_enabled
    assert result.drive_contract.progression_engine_enabled is progression_enabled


def test_market_category_is_metadata_not_drive_authority() -> None:
    historical = interpret_narrative_drives(
        "一个开放 premise。", market_hint="历史 / 治理 / 建设"
    )

    assert historical.market_category.primary_market_category is MarketCategory.HISTORY
    assert historical.drive_contract.primary_drive is NarrativeDrive.STATE_BUILDING
    assert historical.enabled_engines == [
        NarrativeEngineType.STRATEGY_STATE_BUILDING,
    ]


def test_explicit_growth_metadata_enables_engine_without_inventing_power_drive() -> None:
    result = interpret_narrative_drives(
        "一个生产代码从未见过的开放 premise。",
        market_hint="成长冒险",
    )

    assert result.progression_engine_enabled is True
    assert result.drive_contract.progression_engine_enabled is True
    assert result.drive_contract.primary_drive is NarrativeDrive.CUSTOM
    assert NarrativeEngineType.PROGRESSION in result.enabled_engines


def test_drive_contract_rejects_duplicate_and_missing_priorities() -> None:
    with pytest.raises(ValueError, match="primary drive"):
        NarrativeDriveContract(
            drive_contract_id="invalid",
            primary_drive=NarrativeDrive.CAREER_MASTERY,
            secondary_drives=[NarrativeDrive.CAREER_MASTERY],
            drive_priorities={NarrativeDrive.CAREER_MASTERY: 100},
            drive_promises={NarrativeDrive.CAREER_MASTERY: ["职业成长"]},
        )


def test_non_progression_reader_contract_does_not_compile_power_system() -> None:
    interpretation = interpret_reader_experience(
        "一个开放 premise。",
        genre_hint="职业 / 都市",
        contract_prefix="doctor",
    )
    bundle = compile_kernel_contract_proposals(interpretation)

    assert interpretation.reader_contract.primary_narrative_drive == "CAREER_MASTERY"
    assert bundle.progression is None
    assert bundle.genre.capabilities.has_progression_axis is False
    assert all("境界" not in item.statement for item in bundle.genre.genre_promises)


def test_near_future_body_progression_specialization_is_preserved() -> None:
    interpretation = interpret_reader_experience(
        "一个开放 premise。",
        genre_hint="近未来 / 肉身进化",
        contract_prefix="body",
    )
    bundle = compile_kernel_contract_proposals(interpretation)

    assert (
        interpretation.narrative_drive.drive_contract.primary_drive
        is NarrativeDrive.BODY_EVOLUTION
    )
    assert interpretation.narrative_drive.progression_engine_enabled is True
    assert (
        interpretation.narrative_drive.drive_contract.progression_engine_enabled is True
    )
    assert bundle.progression is not None
    assert bundle.genre.capabilities.has_progression_axis is True
    assert bundle.genre.capabilities.has_verification_requirement is True


def test_author_can_raise_secondary_drive_without_replacing_primary() -> None:
    original = interpret_narrative_drives(
        "一个开放 premise。", market_hint="职业 / 都市"
    )

    adjusted = adjust_narrative_drive_interpretation(
        original,
        "RELATIONSHIP_STRONGER",
    )

    assert adjusted.drive_contract.primary_drive is NarrativeDrive.CAREER_MASTERY
    assert NarrativeDrive.RELATIONSHIP_EMOTIONAL in (
        adjusted.drive_contract.secondary_drives
    )
    assert adjusted.drive_contract.author_overrides == ["RELATIONSHIP_STRONGER"]


def test_author_ui_has_readable_labels_for_every_drive_and_market_category() -> None:
    assert all(narrative_drive_label(value) != value.value for value in NarrativeDrive)
    assert all(market_category_label(value) != value.value for value in MarketCategory)
