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
)


@pytest.mark.parametrize(
    ("premise", "primary", "secondary", "progression_enabled"),
    [
        (
            "一名失去超凡能力的矿工发现，废弃矿脉中残留的声音能够重塑他的身体。",
            NarrativeDrive.POWER_PROGRESSION,
            {NarrativeDrive.RESOURCE_OPPORTUNITY, NarrativeDrive.WORLD_EXPLORATION},
            True,
        ),
        (
            "一名县城外科医生接手一家即将关闭的急救中心，并试图建立完整的区域创伤救治体系。",
            NarrativeDrive.CAREER_MASTERY,
            {NarrativeDrive.TEAM_GROWTH, NarrativeDrive.STATUS_RISE},
            False,
        ),
        (
            "一名年轻地方官接管战乱后的边城，要在三年内恢复人口、粮食与防御。",
            NarrativeDrive.STATE_BUILDING,
            {NarrativeDrive.POLITICAL_STRATEGY, NarrativeDrive.TERRITORY_FACTION},
            False,
        ),
        (
            "五名被不同战队放弃的选手组成新队，目标是在两年内进入最高级联赛。",
            NarrativeDrive.COMPETITIVE_SKILL,
            {
                NarrativeDrive.COMPETITIVE_RANK,
                NarrativeDrive.TEAM_GROWTH,
                NarrativeDrive.CAREER_MASTERY,
            },
            False,
        ),
        (
            "每到午夜，一栋旧公寓都会多出一个不存在的房间，进入过的人会失去关于某个人的记忆。",
            NarrativeDrive.MYSTERY_INVESTIGATION,
            {NarrativeDrive.SURVIVAL_RESOURCE, NarrativeDrive.MYSTERY_REVELATION},
            False,
        ),
        (
            "城市中的每种职业都存在一条禁忌晋升路线，越接近顶层越难保留自己的身份。",
            NarrativeDrive.KNOWLEDGE_PROGRESSION,
            {NarrativeDrive.MYSTERY_REVELATION, NarrativeDrive.IDENTITY_PRESSURE},
            True,
        ),
    ],
)
def test_synthetic_seeds_classify_drive_mix_without_forcing_progression(
    premise: str,
    primary: NarrativeDrive,
    secondary: set[NarrativeDrive],
    progression_enabled: bool,
) -> None:
    result = interpret_narrative_drives(premise, contract_prefix="seed")

    assert result.drive_contract.primary_drive is primary
    assert set(result.drive_contract.secondary_drives) == secondary
    assert result.progression_engine_enabled is progression_enabled


def test_market_category_is_metadata_not_drive_authority() -> None:
    historical = interpret_narrative_drives(
        "一名年轻地方官接管战乱后的边城，要在三年内恢复人口、粮食与防御。"
    )

    assert historical.market_category.primary_market_category is MarketCategory.HISTORY
    assert historical.drive_contract.primary_drive is NarrativeDrive.STATE_BUILDING
    assert historical.enabled_engines == [
        NarrativeEngineType.STRATEGY_STATE_BUILDING,
        NarrativeEngineType.TEAM_FACTION_GROWTH,
    ]


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
        "一名县城外科医生接手一家即将关闭的急救中心，并试图建立完整的区域创伤救治体系。",
        contract_prefix="doctor",
    )
    bundle = compile_kernel_contract_proposals(interpretation)

    assert interpretation.reader_contract.primary_narrative_drive == "CAREER_MASTERY"
    assert bundle.progression is None
    assert bundle.genre.capabilities.has_progression_axis is False
    assert all("境界" not in item.statement for item in bundle.genre.genre_promises)


def test_near_future_body_progression_specialization_is_preserved() -> None:
    interpretation = interpret_reader_experience(
        "近未来的气修修仙小说，体修成神的故事。",
        contract_prefix="body",
    )
    bundle = compile_kernel_contract_proposals(interpretation)

    assert interpretation.narrative_drive.drive_contract.primary_drive is (
        NarrativeDrive.POWER_PROGRESSION
    )
    assert interpretation.narrative_drive.progression_engine_enabled is True
    assert bundle.progression is not None
    assert bundle.genre.capabilities.has_progression_axis is True
    assert bundle.genre.capabilities.has_verification_requirement is True


def test_author_can_raise_secondary_drive_without_replacing_primary() -> None:
    original = interpret_narrative_drives(
        "一名县城外科医生接手一家即将关闭的急救中心。"
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
