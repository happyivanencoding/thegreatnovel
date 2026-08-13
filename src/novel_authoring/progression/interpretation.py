"""Proposal-layer interpretation of an original premise into kernel contracts."""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.progression.adapters import (
    BUILTIN_GENRE_ADAPTERS,
    compile_genre_adapters,
)
from novel_authoring.progression.contracts import (
    progression_contract_from_derived,
    progression_contract_from_genre,
)
from novel_authoring.progression.derived import compile_derived_adapter
from novel_authoring.progression.models import (
    ContractStatus,
    DerivedAdapterSpec,
    ExpansionStage,
    ExperiencePriority,
    ExplanationStyle,
    GenreAdapterKind,
    GenreContract,
    GenrePromise,
    GenrePromiseStrength,
    GrowthAxisType,
    PayoffChannelProfile,
    PrimaryFamily,
    ProgressionContract,
    ProgressionSubject,
    ProgressionTopology,
    ReaderExperience,
    ReaderExperienceContract,
    RuntimeGenreCapabilities,
    SettingSkin,
    StageStatus,
    WorldExpansionContract,
    WorldExpansionType,
)
from novel_authoring.serial_kernel.classification import interpret_narrative_drives
from novel_authoring.serial_kernel.models import (
    MarketCategoryMetadata,
    NarrativeDrive,
    NarrativeDriveContract,
    NarrativeDriveInterpretation,
)


class ReaderExperienceAdjustment(StrEnum):
    CONFIRM = "CONFIRM"
    PAYOFF_STRONGER = "PAYOFF_STRONGER"
    MYSTERY_STRONGER = "MYSTERY_STRONGER"
    TEAM_STRONGER = "TEAM_STRONGER"
    RELATIONSHIP_STRONGER = "RELATIONSHIP_STRONGER"
    CAREER_STRONGER = "CAREER_STRONGER"


class ReaderExperienceStrength(StrEnum):
    """Five author-facing levels mapped onto the existing priority contract."""

    WEAK = "WEAK"
    SECONDARY = "SECONDARY"
    NORMAL = "NORMAL"
    STRONG = "STRONG"
    CORE = "CORE"


_STRENGTH_TO_PRIORITY = {
    ReaderExperienceStrength.WEAK: ExperiencePriority.OFF,
    ReaderExperienceStrength.SECONDARY: ExperiencePriority.LOW,
    ReaderExperienceStrength.NORMAL: ExperiencePriority.MEDIUM,
    ReaderExperienceStrength.STRONG: ExperiencePriority.HIGH,
    ReaderExperienceStrength.CORE: ExperiencePriority.VERY_HIGH,
}


READER_EXPERIENCE_UI: tuple[dict[str, str], ...] = (
    {"key": "PROGRESSION", "label": "持续成长", "group": "PRIMARY"},
    {"key": "BREAKTHROUGH", "label": "突破兑现", "group": "PRIMARY"},
    {"key": "POWER_VERIFICATION", "label": "能力验证", "group": "PRIMARY"},
    {"key": "COMBAT", "label": "战斗兑现", "group": "PRIMARY"},
    {"key": "EXPLORATION", "label": "探索机缘", "group": "PRIMARY"},
    {"key": "RESOURCE_OPPORTUNITY", "label": "资源机会", "group": "PRIMARY"},
    {"key": "ARTIFACT_OR_ABILITY", "label": "新物品 / 新能力", "group": "PRIMARY"},
    {"key": "WORLD_EXPANSION", "label": "世界扩张", "group": "PRIMARY"},
    {"key": "FACTION_CONFLICT", "label": "势力竞争", "group": "PRIMARY"},
    {"key": "MYSTERY", "label": "世界谜团", "group": "PRIMARY"},
    {"key": "REVEAL", "label": "揭秘兑现", "group": "MORE"},
    {"key": "TEAM_GROWTH", "label": "团队成长", "group": "MORE"},
    {"key": "RELATIONSHIP", "label": "人物关系", "group": "MORE"},
    {"key": "ROMANCE", "label": "恋爱关系", "group": "MORE"},
    {"key": "STATUS_RISE", "label": "身份提升", "group": "MORE"},
    {"key": "REVENGE", "label": "复仇兑现", "group": "MORE"},
    {"key": "SURVIVAL", "label": "生存压力", "group": "MORE"},
    {"key": "KNOWLEDGE", "label": "知识成长", "group": "MORE"},
    {"key": "WEALTH", "label": "财富增长", "group": "MORE"},
    {"key": "SOCIAL_THEME", "label": "社会议题", "group": "MORE"},
)


READER_EXPERIENCE_PRESETS: tuple[dict[str, object], ...] = (
    {
        "key": "PAYOFF_STRONGER",
        "label": "战斗和爽点更强",
        "values": {"POWER_VERIFICATION": "CORE", "COMBAT": "CORE", "BREAKTHROUGH": "STRONG"},
    },
    {
        "key": "MYSTERY_STRONGER",
        "label": "谜团更强",
        "values": {"MYSTERY": "CORE", "REVEAL": "CORE", "WORLD_EXPANSION": "STRONG"},
    },
    {
        "key": "TEAM_STRONGER",
        "label": "团队更强",
        "values": {"TEAM_GROWTH": "CORE", "RELATIONSHIP": "STRONG", "FACTION_CONFLICT": "STRONG"},
    },
    {
        "key": "RELATIONSHIP_STRONGER",
        "label": "关系更强",
        "values": {"RELATIONSHIP": "CORE", "ROMANCE": "CORE", "TEAM_GROWTH": "STRONG"},
    },
    {
        "key": "CAREER_STRONGER",
        "label": "职业更强",
        "values": {
            "STATUS_RISE": "CORE",
            "PROGRESSION": "STRONG",
            "RESOURCE_OPPORTUNITY": "STRONG",
        },
    },
)


def apply_reader_experience_overrides(
    contract: ReaderExperienceContract,
    overrides: Mapping[
        str, ReaderExperienceStrength | ExperiencePriority | str
    ],
) -> ReaderExperienceContract:
    """Apply explicit author levels without replacing unrelated inference."""

    priorities = dict(contract.experience_priorities)
    for raw_key, raw_value in overrides.items():
        try:
            key = raw_key if isinstance(raw_key, ReaderExperience) else ReaderExperience(raw_key)
        except ValueError as exc:
            raise ValueError(f"未知的阅读体验维度：{raw_key}") from exc
        if isinstance(raw_value, ExperiencePriority):
            priority = raw_value
        else:
            try:
                strength = (
                    raw_value
                    if isinstance(raw_value, ReaderExperienceStrength)
                    else ReaderExperienceStrength(raw_value)
                )
            except ValueError as exc:
                raise ValueError(f"未知的阅读体验强度：{raw_value}") from exc
            priority = _STRENGTH_TO_PRIORITY[strength]
        priorities[key] = priority
    return contract.model_copy(
        update={
            "experience_priorities": priorities,
            "growth_centrality": priorities.get(
                ReaderExperience.PROGRESSION, contract.growth_centrality
            ),
            "world_expansion_centrality": priorities.get(
                ReaderExperience.WORLD_EXPANSION, contract.world_expansion_centrality
            ),
            "mystery_centrality": priorities.get(
                ReaderExperience.MYSTERY, contract.mystery_centrality
            ),
            "team_centrality": priorities.get(
                ReaderExperience.TEAM_GROWTH, contract.team_centrality
            ),
            "relationship_centrality": priorities.get(
                ReaderExperience.RELATIONSHIP, contract.relationship_centrality
            ),
            "theme_centrality": priorities.get(
                ReaderExperience.SOCIAL_THEME, contract.theme_centrality
            ),
        }
    )


class ReaderExperienceInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    reader_contract: ReaderExperienceContract
    primary_adapter: GenreAdapterKind
    secondary_adapters: list[GenreAdapterKind] = Field(default_factory=list, max_length=2)
    growth_object: str
    progression_subject: ProgressionSubject
    axis_type: GrowthAxisType
    topology: list[ProgressionTopology]
    derived_adapter_spec: DerivedAdapterSpec | None = None
    narrative_drive: NarrativeDriveInterpretation
    interpretation_notes: list[str] = Field(default_factory=list)


class KernelContractProposalBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reader_experience: ReaderExperienceContract
    market_category: MarketCategoryMetadata
    narrative_drive: NarrativeDriveContract
    genre: GenreContract
    progression: ProgressionContract | None = None
    world_expansion: WorldExpansionContract
    payoff_channels: PayoffChannelProfile
    derived_adapter_spec: DerivedAdapterSpec | None = None


def _base_priorities() -> dict[ReaderExperience, ExperiencePriority]:
    return {item: ExperiencePriority.MEDIUM for item in ReaderExperience}


def interpret_reader_experience(
    premise: str,
    *,
    genre_hint: str = "",
    contract_prefix: str = "original",
) -> ReaderExperienceInterpretation:
    """Create an author-reviewable interpretation; never an Effective Contract."""

    metadata = genre_hint.casefold()
    drive_interpretation = interpret_narrative_drives(
        premise,
        market_hint=genre_hint,
        contract_prefix=contract_prefix,
    )
    priorities = _base_priorities()
    primary_family = PrimaryFamily.CUSTOM
    secondary: list[PrimaryFamily] = []
    setting = SettingSkin.CUSTOM
    explanation = ExplanationStyle.MIXED_MYSTICAL
    adapter = GenreAdapterKind.CUSTOM
    secondary_adapters: list[GenreAdapterKind] = []
    growth_object = "待 Core Innovation 与 Story Foundation 确认后定义"
    subject = ProgressionSubject.CUSTOM
    axis_type = GrowthAxisType.CUSTOM
    topology = [ProgressionTopology.CUSTOM]
    derived: DerivedAdapterSpec | None = None
    summary = "开放语义原创：详细成长语法将在创意与故事基础确认后生成"

    if "团队成长" in metadata or "team progression" in metadata:
        primary_family = PrimaryFamily.TEAM_PROGRESSION
        adapter = GenreAdapterKind.ABILITY_UNLOCK_TEAM
        growth_object = "成员能力槽与团队组合可能性"
        subject = ProgressionSubject.MULTIPLE_CHARACTERS
        axis_type = GrowthAxisType.TEAM
        topology = [ProgressionTopology.MULTI_AXIS, ProgressionTopology.NETWORK]
        priorities[ReaderExperience.TEAM_GROWTH] = ExperiencePriority.VERY_HIGH
        summary = "团队能力成长：成员解锁与组合共同扩大解决空间"
    elif "宇宙成长" in metadata or "cosmic progression" in metadata:
        primary_family = PrimaryFamily.COSMIC_PROGRESSION
        setting = SettingSkin.COSMIC
        adapter = GenreAdapterKind.COSMIC_PROGRESSION
        growth_object = "宇宙能量、生命层级与感知范围"
        subject = ProgressionSubject.CHARACTER
        axis_type = GrowthAxisType.BODY_EVOLUTION
        topology = [ProgressionTopology.TRANSFORMATIVE, ProgressionTopology.ACCUMULATIVE]
        summary = "宇宙生命成长：天体资源、认知与世界尺度同步扩大"
    elif "神秘学晋升" in metadata or "occult progression" in metadata:
        primary_family = PrimaryFamily.MYSTERY_PROGRESSION
        adapter = GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY
        growth_object = "禁忌知识、身份保存与职业权限"
        subject = ProgressionSubject.CHARACTER
        axis_type = GrowthAxisType.SEQUENCE
        topology = [ProgressionTopology.BRANCHING, ProgressionTopology.TRADEOFF]
        priorities[ReaderExperience.MYSTERY] = ExperiencePriority.VERY_HIGH
        priorities[ReaderExperience.REVEAL] = ExperiencePriority.HIGH
        summary = "神秘学晋升：知识门槛、身份代价与揭露权限相互绑定"
    elif "肉身进化" in metadata or "body progression" in metadata:
        setting = SettingSkin.NEAR_FUTURE
        secondary = [PrimaryFamily.MYSTERY_PROGRESSION]
        adapter = GenreAdapterKind.MYTHIC_BODY_ANCIENT_WORLD
        secondary_adapters = [GenreAdapterKind.CULTIVATION_ESCALATION]
        growth_object = "体修、肉身蜕变与生命层级提升"
        subject = ProgressionSubject.CHARACTER
        axis_type = GrowthAxisType.BODY_EVOLUTION
        topology = [ProgressionTopology.TRANSFORMATIVE, ProgressionTopology.ACCUMULATIVE]
        priorities[ReaderExperience.COMBAT] = ExperiencePriority.VERY_HIGH
        summary = "成长型科幻玄幻：近未来是外壳，体修蜕变与战斗验证是发动机"
    elif "修仙" in metadata or "cultivation" in metadata:
        setting = SettingSkin.ANCIENT_FANTASY
        adapter = GenreAdapterKind.CULTIVATION_ESCALATION
        growth_object = "积累、资源转化与阶段突破"
        subject = ProgressionSubject.CHARACTER
        axis_type = GrowthAxisType.POWER_STAGE
        topology = [ProgressionTopology.LINEAR, ProgressionTopology.ACCUMULATIVE]
        summary = "阶段成长玄幻：资源转化、突破门槛与能力验证持续推进"
    elif drive_interpretation.progression_engine_enabled:
        priorities[ReaderExperience.PROGRESSION] = ExperiencePriority.VERY_HIGH
        summary = "原创成长引擎已启用；具体语法等待 Core Innovation 与 Story Foundation"

    if (
        not drive_interpretation.progression_engine_enabled
        and adapter is GenreAdapterKind.CUSTOM
    ):
        # No specialized evidence is still a valid proposal state; keep every
        # unproven dimension at NORMAL instead of presenting it as WEAK.
        priorities = {item: ExperiencePriority.MEDIUM for item in ReaderExperience}
        drive_to_experience = {
            NarrativeDrive.CAREER_MASTERY: ReaderExperience.STATUS_RISE,
            NarrativeDrive.STATE_BUILDING: ReaderExperience.FACTION_CONFLICT,
            NarrativeDrive.POLITICAL_STRATEGY: ReaderExperience.FACTION_CONFLICT,
            NarrativeDrive.COMPETITIVE_SKILL: ReaderExperience.TEAM_GROWTH,
            NarrativeDrive.COMPETITIVE_RANK: ReaderExperience.STATUS_RISE,
            NarrativeDrive.MYSTERY_INVESTIGATION: ReaderExperience.MYSTERY,
            NarrativeDrive.MYSTERY_REVELATION: ReaderExperience.REVEAL,
            NarrativeDrive.SURVIVAL_RESOURCE: ReaderExperience.SURVIVAL,
            NarrativeDrive.TEAM_GROWTH: ReaderExperience.TEAM_GROWTH,
            NarrativeDrive.RELATIONSHIP_EMOTIONAL: ReaderExperience.RELATIONSHIP,
        }
        for index, drive in enumerate(drive_interpretation.drive_contract.drive_mix):
            experience = drive_to_experience.get(drive)
            if experience is not None:
                priorities[experience] = (
                    ExperiencePriority.VERY_HIGH if index == 0 else ExperiencePriority.HIGH
                )
        primary_family = PrimaryFamily.CUSTOM
        adapter = GenreAdapterKind.CUSTOM
        growth_object = "不强制建立力量成长体系"
        subject = ProgressionSubject.CUSTOM
        axis_type = GrowthAxisType.CUSTOM
        topology = [ProgressionTopology.CUSTOM]
        summary = drive_interpretation.summary

    reader = ReaderExperienceContract(
        contract_id=f"{contract_prefix}-reader-experience",
        primary_family=primary_family,
        secondary_families=secondary,
        setting_skin=setting,
        experience_priorities=priorities,
        mysticism_level=ExperiencePriority.HIGH,
        explanation_style=explanation,
        growth_centrality=(
            ExperiencePriority.VERY_HIGH
            if drive_interpretation.progression_engine_enabled
            else ExperiencePriority.LOW
        ),
        world_expansion_centrality=priorities.get(
            ReaderExperience.WORLD_EXPANSION, ExperiencePriority.MEDIUM
        ),
        mystery_centrality=priorities[ReaderExperience.MYSTERY],
        team_centrality=priorities[ReaderExperience.TEAM_GROWTH],
        relationship_centrality=priorities[ReaderExperience.RELATIONSHIP],
        theme_centrality=priorities[ReaderExperience.SOCIAL_THEME],
        tone=["长篇连载", "保留未知"],
        must_deliver=(
            [
                "成长持续扩大主体能够做什么、进入哪里或理解什么",
                "关键成长拥有事件验证与后果",
                "始终保留可感知的下一层期待",
            ]
            if drive_interpretation.progression_engine_enabled
            else [
                f"持续通过{drive_interpretation.display_primary_drive}产生下一章期待",
                "主要驱动力必须改变事件与后续可能性",
            ]
        ),
        must_not_drift_into=(
            [
                "不得让世界外壳或社会议题取代核心成长因果",
                "不得把原创成长语法强制替换为宗门、秘境、学院或擂台套路",
            ]
            if drive_interpretation.progression_engine_enabled
            else ["不得把非成长主驱动强制解释为力量境界、突破或战斗验证"]
        ),
        primary_narrative_drive=drive_interpretation.drive_contract.primary_drive.value,
        secondary_narrative_drives=[
            item.value for item in drive_interpretation.drive_contract.secondary_drives
        ],
        drive_priority_order=[
            item.value for item in drive_interpretation.drive_contract.drive_mix
        ],
        expected_drive_interactions=[
            f"{drive_interpretation.display_primary_drive}为主，辅助驱动力不得长期取代它"
        ],
        author_notes=premise,
        status=ContractStatus.NEEDS_REVIEW,
    )
    return ReaderExperienceInterpretation(
        summary=summary,
        reader_contract=reader,
        primary_adapter=adapter,
        secondary_adapters=secondary_adapters,
        growth_object=growth_object,
        progression_subject=subject,
        axis_type=axis_type,
        topology=topology,
        derived_adapter_spec=derived,
        narrative_drive=drive_interpretation,
        interpretation_notes=[
            "这是 Proposal，不会写入 Author Truth 或 Canon",
            "详细成长、世界与兑现语法等待 Core Innovation 和 Foundation 确认",
        ],
    )


def adjust_reader_experience(
    contract: ReaderExperienceContract,
    adjustment: ReaderExperienceAdjustment,
) -> ReaderExperienceContract:
    preset = next(
        (
            item
            for item in READER_EXPERIENCE_PRESETS
            if item["key"] == adjustment.value
        ),
        None,
    )
    if preset is None:
        return contract
    values = preset["values"]
    if not isinstance(values, dict):
        return contract
    return apply_reader_experience_overrides(
        contract, {str(key): str(value) for key, value in values.items()}
    )


def compile_kernel_contract_proposals(
    interpretation: ReaderExperienceInterpretation,
) -> KernelContractProposalBundle:
    reader = interpretation.reader_contract
    primary_adapter = (
        compile_derived_adapter(interpretation.derived_adapter_spec)
        if interpretation.derived_adapter_spec is not None
        else BUILTIN_GENRE_ADAPTERS[interpretation.primary_adapter]
    )
    if interpretation.narrative_drive.progression_engine_enabled:
        genre = compile_genre_adapters(
            reader,
            genre_contract_id=reader.contract_id.replace("reader-experience", "genre"),
            primary_adapter=primary_adapter,
            secondary_adapters=[
                BUILTIN_GENRE_ADAPTERS[item] for item in interpretation.secondary_adapters
            ],
        )
    else:
        genre = GenreContract(
            genre_contract_id=reader.contract_id.replace("reader-experience", "genre"),
            primary_genre=reader.primary_family,
            subgenres=reader.secondary_families,
            reader_experience_contract_id=reader.contract_id,
            genre_promises=[
                GenrePromise(
                    promise_id="primary-narrative-drive",
                    statement=reader.must_deliver[0],
                    strength=GenrePromiseStrength.CORE,
                )
            ],
            genre_native_engines=[
                item.value for item in interpretation.narrative_drive.enabled_engines
            ],
            expected_payoff_channels=[
                item.channel
                for item in interpretation.narrative_drive.drive_contract.drive_payoff_channels
            ],
            forbidden_drift_patterns=reader.must_not_drift_into,
            capabilities=RuntimeGenreCapabilities(),
            status=ContractStatus.NEEDS_REVIEW,
        )
    progression: ProgressionContract | None = None
    if interpretation.narrative_drive.progression_engine_enabled:
        progression = (
            progression_contract_from_derived(
                interpretation.derived_adapter_spec,
                progression_contract_id=reader.contract_id.replace(
                    "reader-experience", "progression"
                ),
            )
            if interpretation.derived_adapter_spec is not None
            else progression_contract_from_genre(
                genre,
                progression_contract_id=reader.contract_id.replace(
                    "reader-experience", "progression"
                ),
                progression_subject=interpretation.progression_subject,
                growth_object=interpretation.growth_object,
                axis_type=interpretation.axis_type,
                topology=interpretation.topology,
            )
        )
    if genre.capabilities.has_mystery_binding:
        expansion_types = [WorldExpansionType.MYSTERY, WorldExpansionType.KNOWLEDGE]
    elif reader.setting_skin is SettingSkin.COSMIC:
        expansion_types = [WorldExpansionType.COSMIC, WorldExpansionType.ONTOLOGICAL]
    elif genre.capabilities.has_team_progression:
        expansion_types = [WorldExpansionType.SOCIAL, WorldExpansionType.POWER]
    else:
        expansion_types = [WorldExpansionType.POWER, WorldExpansionType.KNOWLEDGE]
    world = WorldExpansionContract(
        ladder_id=reader.contract_id.replace("reader-experience", "world"),
        stages=[
            ExpansionStage(
                stage_id="current-known-space",
                name="当前已知空间",
                order=1,
                expansion_types=expansion_types,
                world_scope="故事开篇可验证的地理、社会、力量与知识边界",
                reader_question="当前世界的规则边界在哪里？",
            ),
            ExpansionStage(
                stage_id="next-earned-space",
                name="下一层可争取空间",
                order=2,
                expansion_types=expansion_types,
                world_scope="通过成长、资源、知识或关系可以进入的新空间",
                reader_question="下一次成长会打开什么新的可能性？",
                transition_conditions=["满足已确认成长门槛并建立进入证据"],
            ),
            ExpansionStage(
                stage_id="higher-unknown-space",
                name="更高未知空间",
                order=3,
                expansion_types=expansion_types,
                world_scope="只保留方向与问题，不预建固定结局",
                reader_question="更高力量、文明或世界真相意味着什么？",
                status=StageStatus.UNKNOWN,
            ),
        ],
        current_stage_id="current-known-space",
        transition_rules=["只能由已发生事实与作者确认向前推进"],
        expansion_promises=[genre.world_expansion_expectation],
        stagnation_policy="长期无新可能性只产生软诊断，不规定换地图频率",
        status=ContractStatus.NEEDS_REVIEW,
    )
    payoff = PayoffChannelProfile(
        channels={
            channel: (
                GenrePromiseStrength.CORE
                if index < 2
                else GenrePromiseStrength.IMPORTANT
            )
            for index, channel in enumerate(genre.expected_payoff_channels)
        },
        status=ContractStatus.NEEDS_REVIEW,
    )
    return KernelContractProposalBundle(
        reader_experience=reader,
        market_category=interpretation.narrative_drive.market_category,
        narrative_drive=interpretation.narrative_drive.drive_contract,
        genre=genre,
        progression=progression,
        world_expansion=world,
        payoff_channels=payoff,
        derived_adapter_spec=interpretation.derived_adapter_spec,
    )


__all__ = [
    "KernelContractProposalBundle",
    "ReaderExperienceAdjustment",
    "ReaderExperienceInterpretation",
    "ReaderExperienceStrength",
    "READER_EXPERIENCE_PRESETS",
    "READER_EXPERIENCE_UI",
    "apply_reader_experience_overrides",
    "adjust_reader_experience",
    "compile_kernel_contract_proposals",
    "interpret_reader_experience",
]
