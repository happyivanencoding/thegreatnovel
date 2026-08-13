"""Conservative premise classification into proposal-layer drive contracts."""

from __future__ import annotations

from collections.abc import Iterable

from novel_authoring.progression.models import (
    ContractStatus,
    ExperiencePriority,
    PayoffChannel,
    ReaderExperience,
    ReaderExperienceContract,
)
from novel_authoring.serial_kernel.models import (
    PROGRESSION_DRIVES,
    DrivePayoffChannel,
    MarketCategory,
    MarketCategoryMetadata,
    NarrativeDrive,
    NarrativeDriveContract,
    NarrativeDriveInterpretation,
    NarrativeEngineType,
)

_DRIVE_LABELS: dict[NarrativeDrive, str] = {
    NarrativeDrive.POWER_PROGRESSION: "力量与阶段成长",
    NarrativeDrive.KNOWLEDGE_PROGRESSION: "知识与认知成长",
    NarrativeDrive.ABILITY_PROGRESSION: "能力解锁与组合成长",
    NarrativeDrive.BODY_EVOLUTION: "身体蜕变",
    NarrativeDrive.SEQUENCE_PROGRESSION: "序列与路径晋升",
    NarrativeDrive.STATUS_PROGRESSION: "身份层级成长",
    NarrativeDrive.MYSTERY_INVESTIGATION: "谜团调查",
    NarrativeDrive.MYSTERY_REVELATION: "秘密揭露",
    NarrativeDrive.CAREER_MASTERY: "职业能力与事业建设",
    NarrativeDrive.CRAFT_PROFESSION: "技艺与职业精进",
    NarrativeDrive.STATUS_WEALTH: "财富与社会地位",
    NarrativeDrive.STATUS_RISE: "身份与认可提升",
    NarrativeDrive.TERRITORY_FACTION: "势力与领地推进",
    NarrativeDrive.POLITICAL_STRATEGY: "政治与战略博弈",
    NarrativeDrive.STATE_BUILDING: "治理与体系建设",
    NarrativeDrive.COMPETITIVE_SKILL: "竞技技能成长",
    NarrativeDrive.COMPETITIVE_RANK: "排名与赛事晋级",
    NarrativeDrive.SURVIVAL_RESOURCE: "生存与资源",
    NarrativeDrive.BASE_BUILDING: "基地与生存体系建设",
    NarrativeDrive.TEAM_GROWTH: "团队成长",
    NarrativeDrive.RELATIONSHIP_EMOTIONAL: "关系与人生阶段",
    NarrativeDrive.WORLD_EXPLORATION: "世界探索",
    NarrativeDrive.RESOURCE_OPPORTUNITY: "资源与机缘",
    NarrativeDrive.IDENTITY_PRESSURE: "身份保存压力",
    NarrativeDrive.COMEDY_EXPECTATION: "喜剧期待与回调",
    NarrativeDrive.CUSTOM: "作者自定义长期驱动力",
}

_MARKET_LABELS: dict[MarketCategory, str] = {
    MarketCategory.XUANHUAN: "玄幻",
    MarketCategory.XIANXIA: "仙侠",
    MarketCategory.URBAN: "都市",
    MarketCategory.SCIENCE_FICTION: "科幻",
    MarketCategory.FANTASY: "奇幻",
    MarketCategory.HISTORY: "历史",
    MarketCategory.WUXIA: "武侠",
    MarketCategory.GAME: "游戏 / 电竞",
    MarketCategory.HIGH_MARTIAL: "高武",
    MarketCategory.SUPERNATURAL: "灵异",
    MarketCategory.CUSTOM: "作者自定义",
}

_READER_EXPERIENCE_DRIVES: dict[ReaderExperience, NarrativeDrive] = {
    ReaderExperience.RESOURCE_OPPORTUNITY: NarrativeDrive.RESOURCE_OPPORTUNITY,
    ReaderExperience.MYSTERY: NarrativeDrive.MYSTERY_INVESTIGATION,
    ReaderExperience.REVEAL: NarrativeDrive.MYSTERY_REVELATION,
    ReaderExperience.TEAM_GROWTH: NarrativeDrive.TEAM_GROWTH,
    ReaderExperience.RELATIONSHIP: NarrativeDrive.RELATIONSHIP_EMOTIONAL,
    ReaderExperience.STATUS_RISE: NarrativeDrive.STATUS_RISE,
    ReaderExperience.SURVIVAL: NarrativeDrive.SURVIVAL_RESOURCE,
    ReaderExperience.KNOWLEDGE: NarrativeDrive.KNOWLEDGE_PROGRESSION,
    ReaderExperience.WEALTH: NarrativeDrive.STATUS_WEALTH,
}

_PROGRESSION_ENGINE_EXPERIENCES = {
    ReaderExperience.PROGRESSION,
    ReaderExperience.BREAKTHROUGH,
    ReaderExperience.ARTIFACT_OR_ABILITY,
}

_PROGRESSION_ENGINE_METADATA = ("成长", "升级", "progression")

_READER_PRIORITY_SCORES = {
    ExperiencePriority.OFF: 0,
    ExperiencePriority.LOW: 25,
    ExperiencePriority.MEDIUM: 50,
    ExperiencePriority.HIGH: 75,
    ExperiencePriority.VERY_HIGH: 100,
}


def narrative_drive_label(value: NarrativeDrive | str) -> str:
    try:
        drive = value if isinstance(value, NarrativeDrive) else NarrativeDrive(value)
    except ValueError:
        return str(value)
    return _DRIVE_LABELS.get(drive, drive.value)


def market_category_label(value: MarketCategory | str) -> str:
    try:
        category = value if isinstance(value, MarketCategory) else MarketCategory(value)
    except ValueError:
        return str(value)
    return _MARKET_LABELS.get(category, category.value)


def align_narrative_drive_to_reader_experience(
    value: NarrativeDriveInterpretation,
    reader_contract: ReaderExperienceContract,
) -> NarrativeDriveInterpretation:
    """Make confirmed strong reader priorities visible in the existing Drive proposal."""

    drive_scores: dict[NarrativeDrive, int] = {}
    for experience, priority in reader_contract.experience_priorities.items():
        if priority not in {ExperiencePriority.HIGH, ExperiencePriority.VERY_HIGH}:
            continue
        drive = _READER_EXPERIENCE_DRIVES.get(experience)
        if drive is None:
            continue
        score = _READER_PRIORITY_SCORES[priority]
        drive_scores[drive] = max(score, drive_scores.get(drive, 0))
    progression_enabled = value.progression_engine_enabled or any(
        reader_contract.experience_priorities.get(experience)
        in {ExperiencePriority.HIGH, ExperiencePriority.VERY_HIGH}
        for experience in _PROGRESSION_ENGINE_EXPERIENCES
    )
    ranked = sorted(drive_scores, key=lambda drive: (-drive_scores[drive], drive.value))
    current_primary = value.drive_contract.primary_drive
    primary = current_primary
    if current_primary is NarrativeDrive.CUSTOM and ranked:
        highest = drive_scores[ranked[0]]
        strongest = [drive for drive in ranked if drive_scores[drive] == highest]
        if len(strongest) == 1:
            primary = strongest[0]
    secondary = [drive for drive in ranked if drive is not primary][:4]
    contract = value.drive_contract
    priorities = dict(contract.drive_priorities)
    promises = dict(contract.drive_promises)
    payoff_channels = list(contract.drive_payoff_channels)
    debt_types = dict(contract.drive_debt_types)
    for drive in [primary, *secondary]:
        if drive is NarrativeDrive.CUSTOM:
            continue
        priorities[drive] = max(priorities.get(drive, 0), drive_scores.get(drive, 50))
        promises.setdefault(
            drive,
            [f"持续通过{_DRIVE_LABELS.get(drive, drive.value)}产生可见后果"],
        )
        debt_types.setdefault(drive, [drive.value])
        if not any(item.associated_drive is drive for item in payoff_channels):
            payoff_channels.append(
                DrivePayoffChannel(
                    channel=_payoff_for_drive(drive),
                    associated_drive=drive,
                )
            )
    updated_contract = contract.model_copy(
        update={
            "primary_drive": primary,
            "secondary_drives": secondary,
            "drive_priorities": priorities,
            "drive_promises": promises,
            "drive_payoff_channels": payoff_channels,
            "drive_debt_types": debt_types,
            "progression_engine_enabled": (
                progression_enabled
                or any(drive in PROGRESSION_DRIVES for drive in [primary, *secondary])
            ),
            "author_overrides": (
                contract.author_overrides
                if "READER_EXPERIENCE_STRENGTHS" in contract.author_overrides
                else [*contract.author_overrides, "READER_EXPERIENCE_STRENGTHS"]
            ),
        }
    )
    progression_enabled = updated_contract.progression_engine_enabled
    mix = updated_contract.drive_mix
    enabled_engines = list(dict.fromkeys(_engine_for_drive(drive) for drive in mix))
    if progression_enabled and NarrativeEngineType.PROGRESSION not in enabled_engines:
        enabled_engines.append(NarrativeEngineType.PROGRESSION)
    evidence = (
        value.evidence
        if "AUTHOR_READER_EXPERIENCE_STRENGTHS" in value.evidence
        else [*value.evidence, "AUTHOR_READER_EXPERIENCE_STRENGTHS"]
    )
    return value.model_copy(
        update={
            "summary": (
                f"主要依靠{_DRIVE_LABELS.get(primary, primary.value)}推进；"
                f"已读取作者确认的阅读体验优先级"
            ),
            "drive_contract": updated_contract,
            "enabled_engines": enabled_engines,
            "progression_engine_enabled": progression_enabled,
            "display_primary_drive": _DRIVE_LABELS.get(primary, primary.value),
            "display_secondary_drives": [
                _DRIVE_LABELS.get(drive, drive.value) for drive in secondary
            ],
            "evidence": evidence,
        }
    )


def _contains(text: str, values: Iterable[str]) -> bool:
    return any(value in text for value in values)


def _market_categories(metadata: str) -> tuple[MarketCategory, list[MarketCategory]]:
    if _contains(metadata, ("修仙", "仙侠", "xianxia")):
        secondary = (
            [MarketCategory.SCIENCE_FICTION]
            if _contains(metadata, ("科幻", "science fiction", "sci-fi"))
            else []
        )
        return MarketCategory.XIANXIA, secondary
    if _contains(metadata, ("玄幻", "xuanhuan")):
        return MarketCategory.XUANHUAN, []
    if _contains(metadata, ("历史", "historical")):
        return MarketCategory.HISTORY, []
    if _contains(metadata, ("电竞", "游戏", "esports", "game")):
        return MarketCategory.GAME, [MarketCategory.URBAN]
    if _contains(metadata, ("灵异", "supernatural", "horror")):
        return MarketCategory.SUPERNATURAL, []
    if _contains(metadata, ("都市", "urban", "职场", "career")):
        return MarketCategory.URBAN, []
    if _contains(metadata, ("科幻", "science fiction", "sci-fi")):
        return MarketCategory.SCIENCE_FICTION, []
    if _contains(metadata, ("奇幻", "fantasy")):
        return MarketCategory.FANTASY, []
    if _contains(metadata, ("武侠", "wuxia")):
        return MarketCategory.WUXIA, []
    return MarketCategory.CUSTOM, []


def _drive_mix(metadata: str) -> tuple[NarrativeDrive, list[NarrativeDrive], list[str]]:
    """Derive conservative hints only from explicit author metadata."""

    evidence = ["只使用作者显式题材元数据生成弱驱动力建议"]
    if _contains(metadata, ("修仙", "cultivation")):
        return (
            NarrativeDrive.POWER_PROGRESSION,
            [NarrativeDrive.RESOURCE_OPPORTUNITY],
            evidence,
        )
    if _contains(metadata, ("肉身进化", "body progression")):
        return NarrativeDrive.BODY_EVOLUTION, [], evidence
    if _contains(metadata, ("宇宙成长", "cosmic progression")):
        return (
            NarrativeDrive.POWER_PROGRESSION,
            [NarrativeDrive.WORLD_EXPLORATION],
            evidence,
        )
    if _contains(metadata, ("神秘学晋升", "occult progression")):
        return (
            NarrativeDrive.SEQUENCE_PROGRESSION,
            [NarrativeDrive.MYSTERY_REVELATION],
            evidence,
        )
    if _contains(metadata, ("生存", "资源管理", "survival", "resource management")):
        return (
            NarrativeDrive.SURVIVAL_RESOURCE,
            [NarrativeDrive.RESOURCE_OPPORTUNITY],
            evidence,
        )
    if _contains(metadata, ("悬疑", "谜团", "mystery", "suspense")):
        return (
            NarrativeDrive.MYSTERY_INVESTIGATION,
            [NarrativeDrive.MYSTERY_REVELATION],
            evidence,
        )
    if _contains(metadata, ("团队", "群像", "team", "ensemble")):
        return (
            NarrativeDrive.TEAM_GROWTH,
            [NarrativeDrive.RELATIONSHIP_EMOTIONAL],
            evidence,
        )
    if _contains(metadata, ("关系", "恋爱", "romance", "relationship")):
        return (
            NarrativeDrive.RELATIONSHIP_EMOTIONAL,
            [],
            evidence,
        )
    if _contains(metadata, ("职场", "职业", "career", "profession")):
        return (
            NarrativeDrive.CAREER_MASTERY,
            [NarrativeDrive.STATUS_RISE],
            evidence,
        )
    if _contains(metadata, ("竞技", "电竞", "competition", "esports")):
        return (
            NarrativeDrive.COMPETITIVE_SKILL,
            [NarrativeDrive.COMPETITIVE_RANK, NarrativeDrive.TEAM_GROWTH],
            evidence,
        )
    if _contains(metadata, ("治理", "建设", "strategy", "state building")):
        return (
            NarrativeDrive.STATE_BUILDING,
            [NarrativeDrive.POLITICAL_STRATEGY],
            evidence,
        )
    evidence = ["显式题材元数据不足以可靠确定主要驱动力"]
    return NarrativeDrive.CUSTOM, [], evidence


def _engine_for_drive(drive: NarrativeDrive) -> NarrativeEngineType:
    if drive in PROGRESSION_DRIVES:
        return NarrativeEngineType.PROGRESSION
    if drive in {NarrativeDrive.MYSTERY_INVESTIGATION, NarrativeDrive.MYSTERY_REVELATION}:
        return NarrativeEngineType.MYSTERY_REVEAL
    if drive in {NarrativeDrive.CAREER_MASTERY, NarrativeDrive.CRAFT_PROFESSION}:
        return NarrativeEngineType.CAREER_MASTERY
    if drive in {NarrativeDrive.POLITICAL_STRATEGY, NarrativeDrive.STATE_BUILDING}:
        return NarrativeEngineType.STRATEGY_STATE_BUILDING
    if drive in {NarrativeDrive.COMPETITIVE_SKILL, NarrativeDrive.COMPETITIVE_RANK}:
        return NarrativeEngineType.COMPETITIVE_SKILL
    if drive in {NarrativeDrive.SURVIVAL_RESOURCE, NarrativeDrive.BASE_BUILDING}:
        return NarrativeEngineType.SURVIVAL_RESOURCE
    if drive is NarrativeDrive.RELATIONSHIP_EMOTIONAL:
        return NarrativeEngineType.RELATIONSHIP_LIFE
    if drive in {NarrativeDrive.TEAM_GROWTH, NarrativeDrive.TERRITORY_FACTION}:
        return NarrativeEngineType.TEAM_FACTION_GROWTH
    if drive in {NarrativeDrive.STATUS_RISE, NarrativeDrive.STATUS_WEALTH}:
        return NarrativeEngineType.STATUS_WEALTH
    return NarrativeEngineType.CUSTOM


def _payoff_for_drive(drive: NarrativeDrive) -> PayoffChannel:
    mapping = {
        NarrativeDrive.POWER_PROGRESSION: PayoffChannel.POWER_BREAKTHROUGH,
        NarrativeDrive.KNOWLEDGE_PROGRESSION: PayoffChannel.KNOWLEDGE_GAIN,
        NarrativeDrive.MYSTERY_INVESTIGATION: PayoffChannel.DISCOVERY,
        NarrativeDrive.MYSTERY_REVELATION: PayoffChannel.MYSTERY_REVEAL,
        NarrativeDrive.CAREER_MASTERY: PayoffChannel.MASTERY,
        NarrativeDrive.STATUS_RISE: PayoffChannel.RECOGNITION,
        NarrativeDrive.TERRITORY_FACTION: PayoffChannel.FACTION_ADVANCE,
        NarrativeDrive.POLITICAL_STRATEGY: PayoffChannel.STRATEGIC_ADVANTAGE,
        NarrativeDrive.STATE_BUILDING: PayoffChannel.STRATEGIC_ADVANTAGE,
        NarrativeDrive.COMPETITIVE_SKILL: PayoffChannel.MASTERY,
        NarrativeDrive.COMPETITIVE_RANK: PayoffChannel.RANKING_RISE,
        NarrativeDrive.SURVIVAL_RESOURCE: PayoffChannel.SURVIVAL_ESCAPE,
        NarrativeDrive.TEAM_GROWTH: PayoffChannel.TEAM_GROWTH,
        NarrativeDrive.RELATIONSHIP_EMOTIONAL: PayoffChannel.RELATIONSHIP_ADVANCE,
        NarrativeDrive.WORLD_EXPLORATION: PayoffChannel.WORLD_EXPANSION,
        NarrativeDrive.RESOURCE_OPPORTUNITY: PayoffChannel.RESOURCE_GAIN,
    }
    return mapping.get(drive, PayoffChannel.CUSTOM)


def interpret_narrative_drives(
    premise: str,
    *,
    market_hint: str = "",
    contract_prefix: str = "original",
) -> NarrativeDriveInterpretation:
    """Produce a reviewable proposal without changing runtime or Canon."""

    del premise
    metadata = market_hint.casefold()
    primary_category, secondary_categories = _market_categories(metadata)
    primary, secondary, evidence = _drive_mix(metadata)
    mix = [primary, *secondary]
    priorities = {drive: max(45, 100 - index * 15) for index, drive in enumerate(mix)}
    promises = {
        drive: [f"持续通过{_DRIVE_LABELS.get(drive, drive.value)}产生可见后果"]
        for drive in mix
    }
    enabled_engines = list(dict.fromkeys(_engine_for_drive(drive) for drive in mix))
    progression_enabled = any(drive in PROGRESSION_DRIVES for drive in mix) or _contains(
        metadata, _PROGRESSION_ENGINE_METADATA
    )
    if progression_enabled and NarrativeEngineType.PROGRESSION not in enabled_engines:
        enabled_engines.append(NarrativeEngineType.PROGRESSION)
    secondary_summary = "、".join(
        _DRIVE_LABELS.get(item, item.value) for item in secondary
    ) or "待作者补充"
    return NarrativeDriveInterpretation(
        summary=(
            f"主要依靠{_DRIVE_LABELS.get(primary, primary.value)}推进；"
            f"辅助：{secondary_summary}"
        ),
        market_category=MarketCategoryMetadata(
            metadata_id=f"{contract_prefix}-market-category",
            primary_market_category=primary_category,
            secondary_market_categories=secondary_categories,
            display_labels=[
                market_category_label(primary_category),
                *[market_category_label(item) for item in secondary_categories],
            ],
        ),
        drive_contract=NarrativeDriveContract(
            drive_contract_id=f"{contract_prefix}-narrative-drive",
            primary_drive=primary,
            secondary_drives=secondary,
            drive_priorities=priorities,
            drive_promises=promises,
            drive_payoff_channels=[
                DrivePayoffChannel(channel=_payoff_for_drive(drive), associated_drive=drive)
                for drive in mix
            ],
            drive_debt_types={drive: [drive.value] for drive in mix},
            drive_fatigue_risks={
                primary: ["连续多章只推进次要 Drive 会稀释主要承诺"]
            },
            progression_engine_enabled=progression_enabled,
            status=ContractStatus.NEEDS_REVIEW,
        ),
        enabled_engines=enabled_engines,
        progression_engine_enabled=progression_enabled,
        display_primary_drive=_DRIVE_LABELS.get(primary, primary.value),
        display_secondary_drives=[
            _DRIVE_LABELS.get(item, item.value) for item in secondary
        ],
        evidence=evidence,
    )


def adjust_narrative_drive_interpretation(
    value: NarrativeDriveInterpretation,
    adjustment: str,
) -> NarrativeDriveInterpretation:
    """Apply a small author-facing emphasis without guessing a new story model."""

    target = {
        "MYSTERY_STRONGER": NarrativeDrive.MYSTERY_REVELATION,
        "TEAM_STRONGER": NarrativeDrive.TEAM_GROWTH,
        "RELATIONSHIP_STRONGER": NarrativeDrive.RELATIONSHIP_EMOTIONAL,
        "CAREER_STRONGER": NarrativeDrive.CAREER_MASTERY,
    }.get(adjustment)
    if target is None:
        return value
    contract = value.drive_contract
    secondary = list(contract.secondary_drives)
    if target is not contract.primary_drive and target not in secondary:
        secondary.append(target)
    secondary = secondary[:4]
    priorities = dict(contract.drive_priorities)
    priorities[target] = max(90, priorities.get(target, 0))
    promises = dict(contract.drive_promises)
    promises.setdefault(
        target,
        [f"持续通过{_DRIVE_LABELS.get(target, target.value)}产生可见后果"],
    )
    payoff_channels = list(contract.drive_payoff_channels)
    if not any(item.associated_drive is target for item in payoff_channels):
        payoff_channels.append(
            DrivePayoffChannel(
                channel=_payoff_for_drive(target),
                associated_drive=target,
            )
        )
    debts = dict(contract.drive_debt_types)
    debts.setdefault(target, [target.value])
    updated_contract = contract.model_copy(
        update={
            "secondary_drives": secondary,
            "drive_priorities": priorities,
            "drive_promises": promises,
            "drive_payoff_channels": payoff_channels,
            "drive_debt_types": debts,
            "progression_engine_enabled": value.progression_engine_enabled,
            "author_overrides": [*contract.author_overrides, adjustment],
        }
    )
    mix = updated_contract.drive_mix
    enabled_engines = list(dict.fromkeys(_engine_for_drive(drive) for drive in mix))
    if (
        updated_contract.progression_engine_enabled
        and NarrativeEngineType.PROGRESSION not in enabled_engines
    ):
        enabled_engines.append(NarrativeEngineType.PROGRESSION)
    return value.model_copy(
        update={
            "summary": (
                f"主要依靠{value.display_primary_drive}推进；"
                f"作者提高了{_DRIVE_LABELS.get(target, target.value)}的优先级"
            ),
            "drive_contract": updated_contract,
            "enabled_engines": enabled_engines,
            "display_secondary_drives": [
                _DRIVE_LABELS.get(item, item.value) for item in secondary
            ],
            "evidence": [*value.evidence, f"AUTHOR_ADJUSTMENT:{adjustment}"],
        }
    )


__all__ = [
    "align_narrative_drive_to_reader_experience",
    "adjust_narrative_drive_interpretation",
    "interpret_narrative_drives",
    "market_category_label",
    "narrative_drive_label",
]
