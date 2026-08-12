"""Composable genre adapters compiled into identity-free contracts."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from novel_authoring.progression.models import (
    ContractStatus,
    EffectiveGenreContract,
    GenreAdapter,
    GenreAdapterKind,
    GenreContract,
    GenrePromise,
    GenrePromiseStrength,
    PayoffChannel,
    ReaderExperienceContract,
    RuntimeGenreCapabilities,
)

_T = TypeVar("_T")


def _capabilities(**enabled: bool) -> RuntimeGenreCapabilities:
    return RuntimeGenreCapabilities.model_validate(enabled)


BUILTIN_GENRE_ADAPTERS: dict[GenreAdapterKind, GenreAdapter] = {
    GenreAdapterKind.CULTIVATION_ESCALATION: GenreAdapter(
        adapter_id=GenreAdapterKind.CULTIVATION_ESCALATION,
        label="阶段积累与突破",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_stage_transition=True,
            has_resource_gate=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_status_progression=True,
            has_world_expansion=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.POWER_BREAKTHROUGH,
            PayoffChannel.NEW_TECHNIQUE,
            PayoffChannel.RESOURCE_GAIN,
            PayoffChannel.WORLD_EXPANSION,
        ],
        genre_native_scene_types=["积累", "门槛尝试", "能力验证", "进入更高力量环境"],
        genre_native_resource_types=["成长能量", "方法知识", "突破条件"],
        genre_native_conflicts=["资源竞争", "能力边界", "更高层力量压力"],
        drift_risks=["只增加阶段名称而不改变行动可能性"],
    ),
    GenreAdapterKind.ABILITY_UNLOCK_TEAM: GenreAdapter(
        adapter_id=GenreAdapterKind.ABILITY_UNLOCK_TEAM,
        label="能力解锁与团队组合",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_team_progression=True,
            has_world_expansion=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.NEW_ABILITY,
            PayoffChannel.TEAM_GROWTH,
            PayoffChannel.STRATEGIC_ADVANTAGE,
        ],
        genre_native_scene_types=["能力组合", "团队验证", "成员选择"],
        genre_native_resource_types=["能力槽位", "组合条件", "信任与协作"],
        genre_native_conflicts=["团队互补", "成员代价", "组合路线选择"],
    ),
    GenreAdapterKind.MYTHIC_BODY_ANCIENT_WORLD: GenreAdapter(
        adapter_id=GenreAdapterKind.MYTHIC_BODY_ANCIENT_WORLD,
        label="身体蜕变与古老世界",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_stage_transition=True,
            has_resource_gate=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_world_expansion=True,
            has_mystery_binding=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.TRANSFORMATION,
            PayoffChannel.POWER_BREAKTHROUGH,
            PayoffChannel.DISCOVERY,
        ],
        genre_native_scene_types=["身体转化", "古老规则验证", "遗留痕迹探索"],
        genre_native_resource_types=["身体材料", "古老知识", "转化条件"],
        genre_native_conflicts=["身体代价", "生命边界", "古今规则冲突"],
    ),
    GenreAdapterKind.COSMIC_PROGRESSION: GenreAdapter(
        adapter_id=GenreAdapterKind.COSMIC_PROGRESSION,
        label="宇宙尺度成长",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_stage_transition=True,
            has_resource_gate=True,
            has_knowledge_gate=True,
            has_verification_requirement=True,
            has_world_expansion=True,
            has_mystery_binding=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.WORLD_EXPANSION,
            PayoffChannel.KNOWLEDGE_GAIN,
            PayoffChannel.TRANSFORMATION,
        ],
        genre_native_scene_types=["尺度扩张", "宇宙规则发现", "生命层级验证"],
        genre_native_resource_types=["天体能量", "航行机会", "宇宙知识"],
        genre_native_conflicts=["生存尺度", "认知天花板", "高层存在压力"],
    ),
    GenreAdapterKind.EVOLUTION_APOCALYPSE: GenreAdapter(
        adapter_id=GenreAdapterKind.EVOLUTION_APOCALYPSE,
        label="灾变进化",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_stage_transition=True,
            has_resource_gate=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_world_expansion=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.SURVIVAL_ESCAPE,
            PayoffChannel.TRANSFORMATION,
            PayoffChannel.RESOURCE_GAIN,
        ],
        genre_native_scene_types=["环境适应", "进化选择", "生存验证"],
        genre_native_resource_types=["生存物资", "进化来源", "安全窗口"],
        genre_native_conflicts=["短缺", "进化代价", "环境升级"],
    ),
    GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY: GenreAdapter(
        adapter_id=GenreAdapterKind.OCCULT_SEQUENCE_MYSTERY,
        label="神秘知识与晋升",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_stage_transition=True,
            has_resource_gate=True,
            has_knowledge_gate=True,
            has_ability_unlock=True,
            has_verification_requirement=True,
            has_world_expansion=True,
            has_mystery_binding=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.MYSTERY_REVEAL,
            PayoffChannel.NEW_ABILITY,
            PayoffChannel.KNOWLEDGE_GAIN,
        ],
        genre_native_scene_types=["知识门槛", "仪式条件", "身份压力", "局部揭示"],
        genre_native_resource_types=["秘密知识", "仪式条件", "身份权限"],
        genre_native_conflicts=["认知风险", "身份保存", "更高层秘密"],
    ),
    GenreAdapterKind.SURVIVAL_RESOURCE_PROGRESSION: GenreAdapter(
        adapter_id=GenreAdapterKind.SURVIVAL_RESOURCE_PROGRESSION,
        label="生存资源成长",
        capabilities=_capabilities(
            has_progression_axis=True,
            has_resource_gate=True,
            has_verification_requirement=True,
            has_status_progression=True,
            has_world_expansion=True,
        ),
        expected_payoff_channels=[
            PayoffChannel.RESOURCE_GAIN,
            PayoffChannel.SURVIVAL_ESCAPE,
            PayoffChannel.STRATEGIC_ADVANTAGE,
        ],
        genre_native_scene_types=["资源发现", "生产转化", "生存能力验证"],
        genre_native_resource_types=["物资", "生产能力", "安全空间"],
        genre_native_conflicts=["短缺", "机会窗口", "资源分配"],
    ),
    GenreAdapterKind.CUSTOM: GenreAdapter(
        adapter_id=GenreAdapterKind.CUSTOM,
        label="作者自定义成长语法",
        capabilities=_capabilities(),
    ),
}


_PROMISES: tuple[tuple[str, str, str], ...] = (
    ("has_progression_axis", "continuous-growth", "持续存在可感知的成长可能"),
    ("has_stage_transition", "stage-change", "阶段变化会改变行动可能性"),
    ("has_resource_gate", "resource-matters", "资源能够改变成长空间"),
    ("has_knowledge_gate", "knowledge-matters", "知识能够打开此前不可进入的空间"),
    ("has_ability_unlock", "ability-unlock", "新能力会改变解决问题的方式"),
    ("has_verification_requirement", "growth-verification", "关键成长拥有验证空间"),
    ("has_status_progression", "status-growth", "身份或权限成长具有后续影响"),
    ("has_world_expansion", "larger-world", "成长会持续打开更大的世界或认知空间"),
    ("has_mystery_binding", "mystery-binding", "成长与秘密或更高层未知相互推动"),
    ("has_team_progression", "team-growth", "团队组合成长会改变集体可能性"),
)


def _unique(values: Iterable[_T]) -> list[_T]:
    return list(dict.fromkeys(values))


def compile_genre_adapters(
    reader_contract: ReaderExperienceContract,
    *,
    genre_contract_id: str,
    primary_adapter: GenreAdapter,
    secondary_adapters: list[GenreAdapter] | None = None,
) -> GenreContract:
    """Compile one primary and up to two secondary adapters to a proposal."""

    secondary = secondary_adapters or []
    if len(secondary) > 2:
        raise ValueError("最多允许两个 secondary Genre Adapter")
    adapters = [primary_adapter, *secondary]
    capability_values = {
        field: any(getattr(adapter.capabilities, field) for adapter in adapters)
        for field in RuntimeGenreCapabilities.model_fields
    }
    capabilities = RuntimeGenreCapabilities.model_validate(capability_values)
    promises = [
        GenrePromise(
            promise_id=promise_id,
            statement=statement,
            strength=GenrePromiseStrength.CORE,
        )
        for field, promise_id, statement in _PROMISES
        if getattr(capabilities, field)
    ]
    if not promises:
        promises = [
            GenrePromise(
                promise_id="author-defined-growth",
                statement="成长语法由作者确认的结构合同定义",
                strength=GenrePromiseStrength.IMPORTANT,
            )
        ]
    return GenreContract(
        genre_contract_id=genre_contract_id,
        primary_genre=reader_contract.primary_family,
        subgenres=reader_contract.secondary_families,
        reader_experience_contract_id=reader_contract.contract_id,
        genre_promises=promises,
        genre_native_engines=[field for field, enabled in capability_values.items() if enabled],
        expected_payoff_channels=_unique(
            channel for adapter in adapters for channel in adapter.expected_payoff_channels
        ),
        expected_progression_shape=[
            field.removeprefix("has_").replace("_", " ")
            for field, enabled in capability_values.items()
            if enabled
        ],
        world_expansion_expectation=(
            "成长持续打开更大地理、社会、力量、知识或本体空间"
            if capabilities.has_world_expansion
            else "由作者决定是否扩大世界空间"
        ),
        genre_native_scene_types=_unique(
            value for adapter in adapters for value in adapter.genre_native_scene_types
        ),
        genre_native_resource_types=_unique(
            value for adapter in adapters for value in adapter.genre_native_resource_types
        ),
        genre_native_conflicts=_unique(
            value for adapter in adapters for value in adapter.genre_native_conflicts
        ),
        genre_drift_risks=_unique(
            value for adapter in adapters for value in adapter.drift_risks
        ),
        forbidden_drift_patterns=reader_contract.must_not_drift_into,
        capabilities=capabilities,
        status=ContractStatus.NEEDS_REVIEW,
    )


def effective_genre_contract(contract: GenreContract) -> EffectiveGenreContract:
    if contract.status is not ContractStatus.EFFECTIVE:
        raise ValueError("只有作者确认的 EFFECTIVE Genre Contract 可供 Runtime 使用")
    return EffectiveGenreContract(
        genre_contract_id=contract.genre_contract_id,
        reader_experience_contract_id=contract.reader_experience_contract_id,
        promises=contract.genre_promises,
        payoff_channels=contract.expected_payoff_channels,
        capabilities=contract.capabilities,
        world_expansion_expectation=contract.world_expansion_expectation,
        forbidden_drift_patterns=contract.forbidden_drift_patterns,
    )


__all__ = [
    "BUILTIN_GENRE_ADAPTERS",
    "compile_genre_adapters",
    "effective_genre_contract",
]
