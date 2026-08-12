"""Proposal-layer interpretation of an original premise into kernel contracts."""

from __future__ import annotations

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
    GenrePromiseStrength,
    GrowthAxisType,
    PayoffChannel,
    PayoffChannelProfile,
    PrimaryFamily,
    ProgressionContract,
    ProgressionDeltaType,
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


class ReaderExperienceAdjustment(StrEnum):
    CONFIRM = "CONFIRM"
    CULTIVATION_STRONGER = "CULTIVATION_STRONGER"
    PAYOFF_STRONGER = "PAYOFF_STRONGER"
    MYSTERY_STRONGER = "MYSTERY_STRONGER"
    TEAM_STRONGER = "TEAM_STRONGER"


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
    interpretation_notes: list[str] = Field(default_factory=list)


class KernelContractProposalBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reader_experience: ReaderExperienceContract
    genre: GenreContract
    progression: ProgressionContract
    world_expansion: WorldExpansionContract
    payoff_channels: PayoffChannelProfile
    derived_adapter_spec: DerivedAdapterSpec | None = None


def _base_priorities() -> dict[ReaderExperience, ExperiencePriority]:
    return {
        ReaderExperience.PROGRESSION: ExperiencePriority.VERY_HIGH,
        ReaderExperience.BREAKTHROUGH: ExperiencePriority.HIGH,
        ReaderExperience.POWER_VERIFICATION: ExperiencePriority.HIGH,
        ReaderExperience.EXPLORATION: ExperiencePriority.HIGH,
        ReaderExperience.RESOURCE_OPPORTUNITY: ExperiencePriority.HIGH,
        ReaderExperience.ARTIFACT_OR_ABILITY: ExperiencePriority.HIGH,
        ReaderExperience.WORLD_EXPANSION: ExperiencePriority.HIGH,
        ReaderExperience.FACTION_CONFLICT: ExperiencePriority.MEDIUM,
        ReaderExperience.MYSTERY: ExperiencePriority.MEDIUM,
        ReaderExperience.REVEAL: ExperiencePriority.MEDIUM,
        ReaderExperience.TEAM_GROWTH: ExperiencePriority.LOW,
        ReaderExperience.RELATIONSHIP: ExperiencePriority.MEDIUM,
        ReaderExperience.COMBAT: ExperiencePriority.MEDIUM,
        ReaderExperience.SOCIAL_THEME: ExperiencePriority.LOW,
    }


def _custom_spec(premise: str, contract_prefix: str) -> DerivedAdapterSpec:
    if "城市" in premise and ("成长主体" in premise or "自然法则" in premise):
        return DerivedAdapterSpec(
            spec_id=f"{contract_prefix}-derived-city",
            progression_subject=ProgressionSubject.SETTLEMENT,
            growth_object="城市共同解决问题后获得的自然法则",
            progression_topology=[
                ProgressionTopology.NETWORK,
                ProgressionTopology.ACCUMULATIVE,
            ],
            delta_types=[ProgressionDeltaType.UNLOCK, ProgressionDeltaType.MERGE],
            growth_resources=["居民共同理解", "被解决的新型问题"],
            growth_gates=["居民共同解决此前无法解决的问题"],
            growth_costs=["共同选择会改变城市未来规则"],
            verification_modes=["城市地图、居民权限或自然规则发生可见变化"],
            unlock_logic="共同解决问题后生成一条新的城市自然法则",
            world_expansion_relation="城市能力与文明影响范围同步扩大",
            reader_visible_progress=["新自然法则", "居民权限", "城市影响范围"],
            long_term_ceiling_logic="城市逐步成为能够改写更大区域规则的集体主体",
            payoff_logic=["城市能力兑现", "文明规则变化", "共同选择后果"],
            capabilities=RuntimeGenreCapabilities(
                has_progression_axis=True,
                has_ability_unlock=True,
                has_verification_requirement=True,
                has_world_expansion=True,
                has_team_progression=True,
            ),
            payoff_channels=[PayoffChannel.TEAM_GROWTH, PayoffChannel.WORLD_EXPANSION],
        )
    if "语言" in premise and ("现实层" in premise or "文明" in premise):
        return DerivedAdapterSpec(
            spec_id=f"{contract_prefix}-derived-language",
            progression_subject=ProgressionSubject.CHARACTER,
            growth_object="理解灭亡语言后可进入的文明现实层",
            progression_topology=[
                ProgressionTopology.NETWORK,
                ProgressionTopology.TRANSFORMATIVE,
            ],
            delta_types=[ProgressionDeltaType.UNLOCK, ProgressionDeltaType.TRANSFORM],
            growth_resources=["语言材料", "文明语境", "真正理解"],
            growth_gates=["真正理解而非仅翻译一种灭亡语言"],
            growth_costs=["新理解改变主角对现实的认知边界"],
            verification_modes=["进入该文明曾理解过的现实层并解决问题"],
            unlock_logic="理解一门语言即获得对应现实层的进入权限",
            world_expansion_relation="知识成长直接打开新的本体与历史空间",
            reader_visible_progress=["可理解文本", "可进入现实层", "文明知识权限"],
            long_term_ceiling_logic="多种文明理解相互连接，显露现实的更高结构",
            payoff_logic=["知识兑现", "谜团揭示", "世界扩张"],
            capabilities=RuntimeGenreCapabilities(
                has_progression_axis=True,
                has_knowledge_gate=True,
                has_ability_unlock=True,
                has_verification_requirement=True,
                has_world_expansion=True,
                has_mystery_binding=True,
            ),
            payoff_channels=[
                PayoffChannel.KNOWLEDGE_GAIN,
                PayoffChannel.MYSTERY_REVEAL,
                PayoffChannel.WORLD_EXPANSION,
            ],
        )
    return DerivedAdapterSpec(
        spec_id=f"{contract_prefix}-derived-possibility",
        progression_subject=ProgressionSubject.CHARACTER,
        growth_object="被不可逆选择关闭的未来与现实可能性权柄",
        progression_topology=[
            ProgressionTopology.BRANCHING,
            ProgressionTopology.TRADEOFF,
        ],
        delta_types=[
            ProgressionDeltaType.BRANCH,
            ProgressionDeltaType.SACRIFICE,
            ProgressionDeltaType.LOCK_OUT,
        ],
        growth_resources=["被放弃的未来", "不可逆选择"],
        growth_gates=["做出真正不可撤销的选择"],
        growth_costs=["永久失去一条人生路线"],
        verification_modes=["现实开始服从新获得的可能性权柄"],
        unlock_logic="失去一种未来后，获得使用该未来残余可能性的权限",
        world_expansion_relation="每次选择都改变可进入的现实分支",
        reader_visible_progress=["可使用的失去未来", "已锁死路线", "现实服从范围"],
        long_term_ceiling_logic="力量增长与人生可能性持续减少形成终极张力",
        payoff_logic=["不可逆选择后果", "权柄验证", "新现实分支"],
        capabilities=RuntimeGenreCapabilities(
            has_progression_axis=True,
            has_stage_transition=True,
            has_resource_gate=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_world_expansion=True,
            has_mystery_binding=True,
        ),
        payoff_channels=[
            PayoffChannel.STRATEGIC_ADVANTAGE,
            PayoffChannel.TRANSFORMATION,
            PayoffChannel.WORLD_EXPANSION,
        ],
    )


def interpret_reader_experience(
    premise: str,
    *,
    genre_hint: str = "",
    contract_prefix: str = "original",
) -> ReaderExperienceInterpretation:
    """Create an author-reviewable interpretation; never an Effective Contract."""

    text = f"{premise} {genre_hint}".casefold()
    priorities = _base_priorities()
    primary_family = PrimaryFamily.PROGRESSION_FANTASY
    secondary: list[PrimaryFamily] = []
    setting = SettingSkin.CUSTOM
    explanation = ExplanationStyle.MIXED_MYSTICAL
    adapter = GenreAdapterKind.CUSTOM
    secondary_adapters: list[GenreAdapterKind] = []
    growth_object = "持续扩大可能性的原创成长"
    subject = ProgressionSubject.CHARACTER
    axis_type = GrowthAxisType.CUSTOM
    topology = [ProgressionTopology.ACCUMULATIVE]
    derived: DerivedAdapterSpec | None = None
    summary = "自定义成长型长篇：先确认成长语法，再生成故事方向"

    if "能力槽" in text or ("队伍" in text and "能力" in text):
        primary_family = PrimaryFamily.TEAM_PROGRESSION
        adapter = GenreAdapterKind.ABILITY_UNLOCK_TEAM
        growth_object = "成员能力槽与团队组合可能性"
        subject = ProgressionSubject.MULTIPLE_CHARACTERS
        axis_type = GrowthAxisType.TEAM
        topology = [ProgressionTopology.MULTI_AXIS, ProgressionTopology.NETWORK]
        priorities[ReaderExperience.TEAM_GROWTH] = ExperiencePriority.VERY_HIGH
        summary = "团队能力成长：成员解锁与组合共同扩大解决空间"
    elif "恒星" in text or "宇宙" in text:
        primary_family = PrimaryFamily.COSMIC_PROGRESSION
        setting = SettingSkin.COSMIC
        adapter = GenreAdapterKind.COSMIC_PROGRESSION
        growth_object = "宇宙能量、生命层级与感知范围"
        axis_type = GrowthAxisType.BODY_EVOLUTION
        topology = [ProgressionTopology.TRANSFORMATIVE, ProgressionTopology.ACCUMULATIVE]
        summary = "宇宙生命成长：天体资源、认知与世界尺度同步扩大"
    elif "禁忌" in text and ("职业" in text or "晋升" in text):
        primary_family = PrimaryFamily.MYSTERY_PROGRESSION
        adapter = GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY
        growth_object = "禁忌知识、身份保存与职业权限"
        axis_type = GrowthAxisType.SEQUENCE
        topology = [ProgressionTopology.BRANCHING, ProgressionTopology.TRADEOFF]
        priorities[ReaderExperience.MYSTERY] = ExperiencePriority.VERY_HIGH
        priorities[ReaderExperience.REVEAL] = ExperiencePriority.HIGH
        summary = "神秘学晋升：知识门槛、身份代价与揭露权限相互绑定"
    elif ("近未来" in text or "科技" in text) and ("体修" in text or "肉身" in text):
        setting = SettingSkin.NEAR_FUTURE
        secondary = [PrimaryFamily.MYSTERY_PROGRESSION]
        adapter = GenreAdapterKind.MYTHIC_BODY_ANCIENT_WORLD
        secondary_adapters = [GenreAdapterKind.CULTIVATION_ESCALATION]
        growth_object = "体修、肉身蜕变与生命层级提升"
        axis_type = GrowthAxisType.BODY_EVOLUTION
        topology = [ProgressionTopology.TRANSFORMATIVE, ProgressionTopology.ACCUMULATIVE]
        priorities[ReaderExperience.COMBAT] = ExperiencePriority.VERY_HIGH
        summary = "成长型科幻玄幻：近未来是外壳，体修蜕变与战斗验证是发动机"
    elif "修为" in text or "炼化" in text or "修仙" in text:
        setting = SettingSkin.ANCIENT_FANTASY
        adapter = GenreAdapterKind.CULTIVATION_ESCALATION
        growth_object = "积累、资源转化与阶段突破"
        axis_type = GrowthAxisType.POWER_STAGE
        topology = [ProgressionTopology.LINEAR, ProgressionTopology.ACCUMULATIVE]
        summary = "阶段成长玄幻：资源转化、突破门槛与能力验证持续推进"
    else:
        derived = _custom_spec(premise, contract_prefix)
        subject = derived.progression_subject
        growth_object = derived.growth_object
        topology = derived.progression_topology
        if subject is ProgressionSubject.SETTLEMENT:
            primary_family = PrimaryFamily.CIVILIZATION_PROGRESSION
            priorities[ReaderExperience.TEAM_GROWTH] = ExperiencePriority.VERY_HIGH
        elif derived.capabilities.has_knowledge_gate:
            primary_family = PrimaryFamily.MYSTERY_PROGRESSION
            priorities[ReaderExperience.KNOWLEDGE] = ExperiencePriority.VERY_HIGH
            priorities[ReaderExperience.COMBAT] = ExperiencePriority.OFF
        summary = f"原创成长语法：{growth_object}"

    reader = ReaderExperienceContract(
        contract_id=f"{contract_prefix}-reader-experience",
        primary_family=primary_family,
        secondary_families=secondary,
        setting_skin=setting,
        experience_priorities=priorities,
        mysticism_level=ExperiencePriority.HIGH,
        explanation_style=explanation,
        growth_centrality=ExperiencePriority.VERY_HIGH,
        world_expansion_centrality=ExperiencePriority.HIGH,
        mystery_centrality=priorities[ReaderExperience.MYSTERY],
        team_centrality=priorities[ReaderExperience.TEAM_GROWTH],
        relationship_centrality=priorities[ReaderExperience.RELATIONSHIP],
        theme_centrality=priorities[ReaderExperience.SOCIAL_THEME],
        tone=["长篇连载", "成长驱动", "保留未知"],
        must_deliver=[
            "成长持续扩大主体能够做什么、进入哪里或理解什么",
            "关键成长拥有事件验证与后果",
            "始终保留可感知的下一层期待",
        ],
        must_not_drift_into=[
            "不得让世界外壳或社会议题取代核心成长因果",
            "不得把原创成长语法强制替换为宗门、秘境、学院或擂台套路",
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
        interpretation_notes=[
            "这是 Proposal，不会写入 Author Truth 或 Canon",
            "作者确认后才会生成 Genre 与 Progression Contract Proposal",
        ],
    )


def adjust_reader_experience(
    contract: ReaderExperienceContract,
    adjustment: ReaderExperienceAdjustment,
) -> ReaderExperienceContract:
    priorities = dict(contract.experience_priorities)
    if adjustment is ReaderExperienceAdjustment.CULTIVATION_STRONGER:
        priorities[ReaderExperience.PROGRESSION] = ExperiencePriority.VERY_HIGH
        priorities[ReaderExperience.BREAKTHROUGH] = ExperiencePriority.VERY_HIGH
        priorities[ReaderExperience.RESOURCE_OPPORTUNITY] = ExperiencePriority.VERY_HIGH
    elif adjustment is ReaderExperienceAdjustment.PAYOFF_STRONGER:
        priorities[ReaderExperience.POWER_VERIFICATION] = ExperiencePriority.VERY_HIGH
        priorities[ReaderExperience.COMBAT] = ExperiencePriority.VERY_HIGH
    elif adjustment is ReaderExperienceAdjustment.MYSTERY_STRONGER:
        priorities[ReaderExperience.MYSTERY] = ExperiencePriority.VERY_HIGH
        priorities[ReaderExperience.REVEAL] = ExperiencePriority.HIGH
    elif adjustment is ReaderExperienceAdjustment.TEAM_STRONGER:
        priorities[ReaderExperience.TEAM_GROWTH] = ExperiencePriority.VERY_HIGH
    return contract.model_copy(
        update={
            "experience_priorities": priorities,
            "mystery_centrality": priorities.get(
                ReaderExperience.MYSTERY, contract.mystery_centrality
            ),
            "team_centrality": priorities.get(
                ReaderExperience.TEAM_GROWTH, contract.team_centrality
            ),
        }
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
    genre = compile_genre_adapters(
        reader,
        genre_contract_id=reader.contract_id.replace("reader-experience", "genre"),
        primary_adapter=primary_adapter,
        secondary_adapters=[
            BUILTIN_GENRE_ADAPTERS[item] for item in interpretation.secondary_adapters
        ],
    )
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
    "adjust_reader_experience",
    "compile_kernel_contract_proposals",
    "interpret_reader_experience",
]
