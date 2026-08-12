"""Conservative premise classification into proposal-layer drive contracts."""

from __future__ import annotations

from collections.abc import Iterable

from novel_authoring.progression.models import ContractStatus, PayoffChannel
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
    NarrativeDrive.BODY_EVOLUTION: "身体蜕变",
    NarrativeDrive.MYSTERY_INVESTIGATION: "谜团调查",
    NarrativeDrive.MYSTERY_REVELATION: "秘密揭露",
    NarrativeDrive.CAREER_MASTERY: "职业能力与事业建设",
    NarrativeDrive.STATUS_RISE: "身份与认可提升",
    NarrativeDrive.TERRITORY_FACTION: "势力与领地推进",
    NarrativeDrive.POLITICAL_STRATEGY: "政治与战略博弈",
    NarrativeDrive.STATE_BUILDING: "治理与体系建设",
    NarrativeDrive.COMPETITIVE_SKILL: "竞技技能成长",
    NarrativeDrive.COMPETITIVE_RANK: "排名与赛事晋级",
    NarrativeDrive.SURVIVAL_RESOURCE: "生存与资源",
    NarrativeDrive.TEAM_GROWTH: "团队成长",
    NarrativeDrive.RELATIONSHIP_EMOTIONAL: "关系与人生阶段",
    NarrativeDrive.WORLD_EXPLORATION: "世界探索",
    NarrativeDrive.RESOURCE_OPPORTUNITY: "资源与机缘",
    NarrativeDrive.IDENTITY_PRESSURE: "身份保存压力",
    NarrativeDrive.CUSTOM: "作者自定义长期驱动力",
}


def narrative_drive_label(value: NarrativeDrive | str) -> str:
    try:
        drive = value if isinstance(value, NarrativeDrive) else NarrativeDrive(value)
    except ValueError:
        return str(value)
    return _DRIVE_LABELS.get(drive, drive.value)


def _contains(text: str, values: Iterable[str]) -> bool:
    return any(value in text for value in values)


def _market_categories(text: str) -> tuple[MarketCategory, list[MarketCategory]]:
    if _contains(text, ("修仙", "仙侠", "气修")):
        secondary = (
            [MarketCategory.SCIENCE_FICTION]
            if _contains(text, ("近未来", "科技", "赛博"))
            else []
        )
        return MarketCategory.XIANXIA, secondary
    if _contains(text, ("玄幻", "超凡", "矿脉", "异能")):
        return MarketCategory.XUANHUAN, []
    if _contains(text, ("历史", "地方官", "边城", "朝堂")):
        return MarketCategory.HISTORY, []
    if _contains(text, ("电竞", "战队", "联赛", "选手")):
        return MarketCategory.GAME, [MarketCategory.URBAN]
    if _contains(text, ("灵异", "旧公寓", "鬼", "不存在的房间")):
        return MarketCategory.SUPERNATURAL, []
    if _contains(text, ("医生", "医院", "职业", "商业", "文娱")):
        return MarketCategory.URBAN, []
    if _contains(text, ("科幻", "未来", "星际", "宇宙")):
        return MarketCategory.SCIENCE_FICTION, []
    return MarketCategory.CUSTOM, []


def _drive_mix(text: str) -> tuple[NarrativeDrive, list[NarrativeDrive], list[str]]:
    evidence: list[str] = []
    if _contains(text, ("医生", "医院", "急救", "外科", "职业体系")):
        evidence.append("职业、医疗或组织能力是显式长期目标")
        return (
            NarrativeDrive.CAREER_MASTERY,
            [NarrativeDrive.TEAM_GROWTH, NarrativeDrive.STATUS_RISE],
            evidence,
        )
    if _contains(text, ("地方官", "恢复人口", "粮食", "治理", "国家建设")):
        evidence.append("治理指标与组织建设是显式长期目标")
        return (
            NarrativeDrive.STATE_BUILDING,
            [NarrativeDrive.POLITICAL_STRATEGY, NarrativeDrive.TERRITORY_FACTION],
            evidence,
        )
    if _contains(text, ("电竞", "战队", "联赛", "选手", "竞技排名")):
        evidence.append("技能、赛事排名与团队磨合共同构成长线")
        return (
            NarrativeDrive.COMPETITIVE_SKILL,
            [
                NarrativeDrive.COMPETITIVE_RANK,
                NarrativeDrive.TEAM_GROWTH,
                NarrativeDrive.CAREER_MASTERY,
            ],
            evidence,
        )
    if _contains(text, ("不存在的房间", "失去关于", "灵异", "旧公寓")):
        evidence.append("异常规律的调查与揭露是下一章期待来源")
        return (
            NarrativeDrive.MYSTERY_INVESTIGATION,
            [NarrativeDrive.SURVIVAL_RESOURCE, NarrativeDrive.MYSTERY_REVELATION],
            evidence,
        )
    if _contains(text, ("禁忌晋升", "禁忌", "晋升路线")) and _contains(
        text, ("职业", "身份", "秘密")
    ):
        evidence.append("晋升与秘密、身份代价绑定")
        return (
            NarrativeDrive.KNOWLEDGE_PROGRESSION,
            [NarrativeDrive.MYSTERY_REVELATION, NarrativeDrive.IDENTITY_PRESSURE],
            evidence,
        )
    if _contains(text, ("灭亡的语言", "理解一种", "现实层")):
        evidence.append("知识理解持续解锁此前不可进入的现实层")
        return (
            NarrativeDrive.KNOWLEDGE_PROGRESSION,
            [NarrativeDrive.MYSTERY_REVELATION, NarrativeDrive.WORLD_EXPLORATION],
            evidence,
        )
    if _contains(text, ("城市本身是成长主体", "城市获得", "新的自然法则")):
        evidence.append("集体解决问题会让城市主体获得可验证的新能力")
        return (
            NarrativeDrive.POWER_PROGRESSION,
            [NarrativeDrive.TEAM_GROWTH, NarrativeDrive.WORLD_EXPLORATION],
            evidence,
        )
    if _contains(text, ("恒星", "宇宙能量", "吸收残留能量")):
        evidence.append("能量积累与宇宙尺度共同扩大主体可能性")
        return (
            NarrativeDrive.POWER_PROGRESSION,
            [NarrativeDrive.WORLD_EXPLORATION, NarrativeDrive.KNOWLEDGE_PROGRESSION],
            evidence,
        )
    if _contains(
        text,
        (
            "体修",
            "修仙",
            "修为",
            "炼化",
            "超凡能力",
            "重塑他的身体",
            "进化",
            "突破",
        ),
    ):
        evidence.append("主动变强、资源与验证直接改变行动可能性")
        secondary = [
            NarrativeDrive.WORLD_EXPLORATION,
            NarrativeDrive.RESOURCE_OPPORTUNITY,
        ]
        if _contains(text, ("势力", "宗门", "城市")):
            secondary.append(NarrativeDrive.TERRITORY_FACTION)
        if _contains(text, ("秘密", "古老")):
            secondary.append(NarrativeDrive.MYSTERY_REVELATION)
        return NarrativeDrive.POWER_PROGRESSION, secondary[:4], evidence
    if _contains(text, ("队伍", "团队", "能力槽")):
        evidence.append("团队组合能力是显式推进机制")
        return (
            NarrativeDrive.TEAM_GROWTH,
            [NarrativeDrive.ABILITY_PROGRESSION, NarrativeDrive.WORLD_EXPLORATION],
            evidence,
        )
    if _contains(text, ("不可撤销的选择", "失去一种未来", "可能性")):
        evidence.append("不可逆选择持续改变主体能力与可达世界")
        return (
            NarrativeDrive.POWER_PROGRESSION,
            [NarrativeDrive.WORLD_EXPLORATION, NarrativeDrive.IDENTITY_PRESSURE],
            evidence,
        )
    evidence.append("当前文字不足以可靠推断成熟专用驱动力")
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

    text = f"{premise} {market_hint}".casefold()
    primary_category, secondary_categories = _market_categories(text)
    primary, secondary, evidence = _drive_mix(text)
    mix = [primary, *secondary]
    priorities = {drive: max(45, 100 - index * 15) for index, drive in enumerate(mix)}
    promises = {
        drive: [f"持续通过{_DRIVE_LABELS.get(drive, drive.value)}产生可见后果"]
        for drive in mix
    }
    enabled_engines = list(dict.fromkeys(_engine_for_drive(drive) for drive in mix))
    progression_enabled = any(drive in PROGRESSION_DRIVES for drive in mix)
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
            display_labels=[primary_category.value, *[item.value for item in secondary_categories]],
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
            "author_overrides": [*contract.author_overrides, adjustment],
        }
    )
    mix = updated_contract.drive_mix
    enabled_engines = list(dict.fromkeys(_engine_for_drive(drive) for drive in mix))
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
    "adjust_narrative_drive_interpretation",
    "interpret_narrative_drives",
    "narrative_drive_label",
]
