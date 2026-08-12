"""Conservative contract proposals for existing novels without a kernel contract."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.db.database import Database
from novel_authoring.edition import edition_chapters
from novel_authoring.progression.interpretation import (
    ReaderExperienceInterpretation,
    compile_kernel_contract_proposals,
)
from novel_authoring.progression.models import (
    ContractStatus,
    DerivedAdapterSpec,
    ExperiencePriority,
    ExplanationStyle,
    GenreAdapterKind,
    GrowthAxisType,
    PayoffChannel,
    PrimaryFamily,
    ProgressionDeltaType,
    ProgressionSubject,
    ProgressionTopology,
    ReaderExperience,
    ReaderExperienceContract,
    RuntimeGenreCapabilities,
    SettingSkin,
)
from novel_authoring.progression.service import (
    ProgressionContractType,
    create_contract_proposal,
    list_contract_records,
)


def _names(world_state: Mapping[str, Any], collections: tuple[str, ...]) -> list[str]:
    names: list[str] = []
    for collection in collections:
        values = world_state.get(collection, [])
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, Mapping):
                continue
            name = value.get("name") or value.get("title") or value.get("statement")
            if name:
                names.append(str(name))
    return list(dict.fromkeys(names))


def infer_existing_contract_proposals(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
) -> dict[str, Any]:
    """Create author-reviewable proposals; never infer current stage or Canon facts."""

    with database.connect() as connection:
        chapters = edition_chapters(connection, book_id, edition_id)
    if not chapters:
        raise ValueError("已有小说至少需要一个真实章节才能生成成长建议")
    latest = chapters[-1]
    chapter_id = str(latest["chapter_id"])
    world_state = build_story_game_state(
        database,
        book_id,
        edition_id,
        chapter_id=chapter_id,
        include_global_scope=True,
    )
    resources = _names(world_state, ("resources", "inventory", "equipment"))
    abilities = _names(world_state, ("abilities",))
    relationships = _names(world_state, ("relationships", "factions"))
    world_entries = _names(world_state, ("locations", "world_rules"))
    threads = _names(world_state, ("threads", "promises", "tasks"))
    priorities = {
        ReaderExperience.PROGRESSION: (
            ExperiencePriority.HIGH if abilities or resources else ExperiencePriority.MEDIUM
        ),
        ReaderExperience.RESOURCE_OPPORTUNITY: (
            ExperiencePriority.HIGH if resources else ExperiencePriority.MEDIUM
        ),
        ReaderExperience.WORLD_EXPANSION: (
            ExperiencePriority.HIGH if world_entries else ExperiencePriority.MEDIUM
        ),
        ReaderExperience.RELATIONSHIP: (
            ExperiencePriority.HIGH if relationships else ExperiencePriority.MEDIUM
        ),
        ReaderExperience.MYSTERY: (
            ExperiencePriority.HIGH if threads else ExperiencePriority.MEDIUM
        ),
    }
    evidence_summary = (
        f"第{int(latest['ordinal'])}章边界：能力 {len(abilities)}、资源 {len(resources)}、"
        f"关系/势力 {len(relationships)}、世界入口 {len(world_entries)}、未决线程 {len(threads)}"
    )
    reader = ReaderExperienceContract(
        contract_id=f"{book_id}-inferred-reader-experience",
        primary_family=PrimaryFamily.CUSTOM,
        setting_skin=SettingSkin.CUSTOM,
        experience_priorities=priorities,
        explanation_style=ExplanationStyle.BALANCED,
        growth_centrality=priorities[ReaderExperience.PROGRESSION],
        world_expansion_centrality=priorities[ReaderExperience.WORLD_EXPANSION],
        mystery_centrality=priorities[ReaderExperience.MYSTERY],
        team_centrality=ExperiencePriority.MEDIUM,
        relationship_centrality=priorities[ReaderExperience.RELATIONSHIP],
        theme_centrality=ExperiencePriority.MEDIUM,
        tone=["沿用现有作品", "先证据后确认"],
        must_deliver=["由作者确认什么变化才算这本书的真实成长"],
        must_not_drift_into=["不得把已有作品强制套入预设题材等级表"],
        author_notes=evidence_summary,
        status=ContractStatus.INFERRED_PROPOSAL,
    )
    capabilities = RuntimeGenreCapabilities(
        has_progression_axis=bool(abilities or resources),
        has_resource_gate=bool(resources),
        has_ability_unlock=bool(abilities),
        has_verification_requirement=True,
        has_world_expansion=bool(world_entries),
        has_mystery_binding=bool(threads),
        has_team_progression=bool(relationships),
    )
    derived = DerivedAdapterSpec(
        spec_id=f"{book_id}-inferred-structure",
        progression_subject=ProgressionSubject.CUSTOM,
        growth_object="现有事实中可观察的能力、资源与行动空间变化",
        progression_topology=[ProgressionTopology.ACCUMULATIVE],
        delta_types=[ProgressionDeltaType.ADVANCE, ProgressionDeltaType.UNLOCK],
        growth_resources=resources,
        growth_gates=["由作者确认哪些既有变化构成有效成长"],
        growth_costs=["不得用无来源的新设定补齐成长链"],
        verification_modes=["逐章 Source State 或 Canon 事件证据"],
        unlock_logic="只有章节事实证明新增可用行动时才视为解锁",
        world_expansion_relation="成长只打开已有因果可达的新空间",
        reader_visible_progress=["能力、资源、关系或进入空间发生可验证变化"],
        long_term_ceiling_logic="保持未知，随已发生事实逐步显露",
        payoff_logic=["回收既有线程并让成长产生可见后果"],
        capabilities=capabilities,
        payoff_channels=[
            PayoffChannel.DISCOVERY,
            PayoffChannel.STRATEGIC_ADVANTAGE,
            PayoffChannel.CUSTOM,
        ],
        status=ContractStatus.INFERRED_PROPOSAL,
    )
    bundle = compile_kernel_contract_proposals(
        ReaderExperienceInterpretation(
            summary="从现有章节状态生成的保守建议，所有语义均待作者确认",
            reader_contract=reader,
            primary_adapter=GenreAdapterKind.CUSTOM,
            growth_object=derived.growth_object,
            progression_subject=derived.progression_subject,
            axis_type=GrowthAxisType.CUSTOM,
            topology=derived.progression_topology,
            derived_adapter_spec=derived,
            interpretation_notes=[evidence_summary],
        )
    )
    existing = list_contract_records(
        database,
        book_id=book_id,
        edition_id=edition_id,
    )
    existing_types = {
        record.contract_type
        for record in existing
        if record.status not in {ContractStatus.REJECTED, ContractStatus.SUPERSEDED}
    }
    created = []
    for contract_type, payload in (
        (ProgressionContractType.READER_EXPERIENCE, bundle.reader_experience),
        (ProgressionContractType.GENRE, bundle.genre),
        (ProgressionContractType.PROGRESSION, bundle.progression),
        (ProgressionContractType.WORLD_EXPANSION, bundle.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, bundle.payoff_channels),
    ):
        if contract_type in existing_types:
            continue
        created.append(
            create_contract_proposal(
                database,
                book_id=book_id,
                edition_id=edition_id,
                contract_type=contract_type,
                payload=payload,
                source="EXISTING_NOVEL_CHAPTER_STATE_INFERENCE",
                status=ContractStatus.INFERRED_PROPOSAL,
                author_notes=evidence_summary,
            )
        )
    return {
        "chapter": {"chapter_id": chapter_id, "ordinal": int(latest["ordinal"])},
        "evidence_summary": evidence_summary,
        "created": [item.model_dump(mode="json") for item in created],
        "deduplicated": not created,
        "canon_changed": False,
    }


__all__ = ["infer_existing_contract_proposals"]
