"""Frozen production input that connects PWK projections to planning.

The context is not an authority.  It only freezes chapter-pinned read models,
effective contract versions, existing planning state, and author controls for
one Planning Aggregate.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.edition import edition_chapters
from novel_authoring.metrics.formulas import narrative_debt as narrative_debt_metric
from novel_authoring.planning.diagnostics import build_narrative_portfolio_snapshot
from novel_authoring.planning.innovation import NarrativeDebt
from novel_authoring.progression.anticipation import AnticipationSurfaceView
from novel_authoring.progression.scheduler import (
    ChapterIntentRecommendation,
    load_scheduler_override,
    recommend_chapter_intent,
)
from novel_authoring.progression.service import (
    ProgressionContractType,
    list_contract_records,
)
from novel_authoring.progression.workspace import build_progression_workspace_from_world_state
from novel_authoring.serial_kernel.engines import NARRATIVE_ENGINE_REGISTRY
from novel_authoring.serial_kernel.models import (
    NarrativeDriveContract,
    NarrativeEngineType,
)


class KernelContractReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_record_id: str
    contract_type: ProgressionContractType
    version_number: int = Field(ge=1)
    effective_from_boundary: int = Field(ge=0)
    status: str


class EffectiveKernelContracts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reader_experience: dict[str, Any] | None = None
    market_category: dict[str, Any] | None = None
    narrative_drive: dict[str, Any] | None = None
    genre: dict[str, Any] | None = None
    progression: dict[str, Any] | None = None
    world_expansion: dict[str, Any] | None = None
    payoff_channel: dict[str, Any] | None = None


class KernelProposalContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    records: list[dict[str, Any]] = Field(default_factory=list)
    excluded_from_scoring: bool = True


class KernelWorldStateReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chapter_id: str
    chapter_ordinal: int = Field(ge=0)
    availability: str
    coverage_status: str | None = None
    source_layer: str | None = None
    projection_only: bool = True


class KernelChapterState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    world_state_reference: KernelWorldStateReference
    progression_state: dict[str, Any] | None = None
    world_expansion_state: dict[str, Any] | None = None
    opportunity_surface: dict[str, Any] | None = None
    resource_state: list[dict[str, Any]] = Field(default_factory=list)
    capability_state: list[dict[str, Any]] = Field(default_factory=list)
    knowledge_state: list[dict[str, Any]] = Field(default_factory=list)


class KernelPlanningState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    anticipation_surface: dict[str, Any] | None = None
    narrative_debts: list[dict[str, Any]] = Field(default_factory=list)
    active_threads: list[dict[str, Any]] = Field(default_factory=list)
    promises: list[dict[str, Any]] = Field(default_factory=list)
    reveal_agenda: list[dict[str, Any]] = Field(default_factory=list)
    scheduler_recommendation: ChapterIntentRecommendation | None = None


class KernelAuthorState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author_tasks: list[dict[str, Any]] = Field(default_factory=list)
    author_intents: list[dict[str, Any]] = Field(default_factory=list)
    effective_book_profile: dict[str, Any] = Field(default_factory=dict)
    author_truths: list[dict[str, Any]] = Field(default_factory=list)


class KernelCoverage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    known: list[str] = Field(default_factory=list)
    partial: list[str] = Field(default_factory=list)
    unknown: list[str] = Field(default_factory=list)
    blocking_gaps: list[str] = Field(default_factory=list)


class KernelPlanningContext(BaseModel):
    """Immutable input embedded in one Planning Aggregate."""

    model_config = ConfigDict(extra="forbid")

    book_id: str
    edition_id: str
    target_chapter_id: str | None = None
    target_chapter_ordinal: int = Field(ge=0)
    context_chapter_id: str
    context_chapter_ordinal: int = Field(ge=0)
    effective_contracts: EffectiveKernelContracts
    contract_references: list[KernelContractReference] = Field(default_factory=list)
    proposal_context: KernelProposalContext = Field(default_factory=KernelProposalContext)
    chapter_state: KernelChapterState
    planning_state: KernelPlanningState
    author_state: KernelAuthorState
    coverage: KernelCoverage
    warnings: list[str] = Field(default_factory=list)


_CONTRACT_FIELDS: dict[ProgressionContractType, str] = {
    ProgressionContractType.READER_EXPERIENCE: "reader_experience",
    ProgressionContractType.MARKET_CATEGORY: "market_category",
    ProgressionContractType.NARRATIVE_DRIVE: "narrative_drive",
    ProgressionContractType.GENRE: "genre",
    ProgressionContractType.PROGRESSION: "progression",
    ProgressionContractType.WORLD_EXPANSION: "world_expansion",
    ProgressionContractType.PAYOFF_CHANNEL: "payoff_channel",
}


def _mapping_list(value: object) -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        return [dict(item) for item in value.values() if isinstance(item, Mapping)]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [dict(item) for item in value if isinstance(item, Mapping)]
    return []


def _promise_mapping(value: object) -> dict[str, dict[str, object]]:
    items = _mapping_list(value)
    result: dict[str, dict[str, object]] = {}
    for index, item in enumerate(items, start=1):
        key = str(item.get("promise_id") or item.get("id") or f"promise-{index}")
        result[key] = dict(item)
    return result


def _planning_item_id(item: Mapping[str, Any]) -> str:
    return str(
        item.get("thread_id")
        or item.get("promise_id")
        or item.get("id")
        or item.get("record_id")
        or item.get("state_key")
        or ""
    )


def _portfolio_debts(
    *,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int,
    active_threads: list[dict[str, Any]],
    promises: list[dict[str, Any]],
) -> list[NarrativeDebt]:
    if not promises:
        return []
    snapshot = build_narrative_portfolio_snapshot(
        active_threads=active_threads,
        promises=_promise_mapping(promises),
        current_chapter=chapter_ordinal,
        snapshot_id=f"kernel-portfolio-{book_id}-{edition_id}-{chapter_ordinal}",
    )
    settings = load_settings()
    values: list[NarrativeDebt] = []
    source_by_id = _promise_mapping(promises)
    for debt in snapshot.narrative_debts:
        if debt.debt_score is not None:
            values.append(debt)
            continue
        source = source_by_id.get(debt.debt_id, {})
        try:
            metric = narrative_debt_metric(
                importance=float(str(source.get("importance", 0.5))),
                reader_visibility=float(str(source.get("reader_visibility", 0.5))),
                promise_progress=float(str(source.get("progress", 0))),
                age_chapters=max(0, chapter_ordinal - debt.opened_chapter),
                target_max_age=max(
                    1,
                    int(
                        str(
                            source.get("target_max_age")
                            or source.get("target_max_age_chapters")
                            or 8
                        )
                    ),
                ),
                reminder_count=max(
                    0, int(str(source.get("reminder_count") or 0))
                ),
                config=settings.metrics["narrative_debt"],
            )
        except (TypeError, ValueError):
            values.append(debt)
            continue
        values.append(
            debt.model_copy(
                update={
                    "debt_score": metric.score,
                    "metric_components": metric.inputs,
                    "evidence": [
                        *debt.evidence,
                        f"existing_formula:{metric.metric}",
                    ],
                }
            )
        )
    return values


def _engine_recommendations(
    *,
    drive_contract: NarrativeDriveContract | None,
    progression_state: Mapping[str, Any] | None,
    debts: Sequence[NarrativeDebt],
    reader_promises: Sequence[str],
) -> list[Any]:
    if drive_contract is None:
        return []
    adapter = NARRATIVE_ENGINE_REGISTRY.get(NarrativeEngineType.PROGRESSION)
    if adapter is None:
        return []
    recommendations: list[Any] = []
    for drive in drive_contract.drive_mix:
        if drive not in adapter.supported_drives:
            continue
        recommendations.extend(
            adapter.recommend_intents(
                {
                    "drive": drive.value,
                    "progression_state": dict(progression_state or {}),
                    "reader_promises": list(reader_promises),
                    "debt_ids": [item.debt_id for item in debts],
                    "evidence": list(
                        (progression_state or {})
                        .get("primary_axis_state", {})
                        .get("evidence", [])
                    ),
                }
            )
        )
    return recommendations


def build_kernel_planning_context(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    author_policy: Mapping[str, Any],
    context_chapter_id: str | None = None,
    target_chapter_id: str | None = None,
    target_chapter_ordinal: int | None = None,
    world_state: Mapping[str, Any] | None = None,
) -> KernelPlanningContext | None:
    """Freeze the state through one real chapter for planning the next chapter."""

    from novel_authoring.author_control.projections import build_story_game_state

    with database.connect() as connection:
        chapters = edition_chapters(connection, book_id, edition_id)
    if not chapters:
        return None
    selected_chapter_id = context_chapter_id or str(chapters[-1]["chapter_id"])
    world_state = (
        dict(world_state)
        if world_state is not None
        else build_story_game_state(
            database,
            book_id,
            edition_id,
            chapter_id=selected_chapter_id,
        )
    )
    chapter = world_state.get("chapter")
    if (
        not isinstance(chapter, Mapping)
        or str(chapter.get("chapter_id") or "") != selected_chapter_id
    ):
        raise ValueError("Kernel Planning Context 必须绑定一个真实且匹配的上下文章节")
    context_ordinal = int(chapter.get("ordinal") or 0)
    planning_ordinal = target_chapter_ordinal or context_ordinal + 1
    if planning_ordinal < context_ordinal:
        raise ValueError("Kernel Planning Context 的目标章不能早于状态上下文章")

    all_records = list_contract_records(
        database,
        book_id=book_id,
        edition_id=edition_id,
    )
    active_records = {
        record.contract_type: record
        for record in all_records
        if record.status.value == "EFFECTIVE"
        if int(record.effective_from_boundary or 0) <= planning_ordinal
    }
    effective_values: dict[str, dict[str, Any] | None] = {
        field: None for field in _CONTRACT_FIELDS.values()
    }
    references: list[KernelContractReference] = []
    for contract_type, record in active_records.items():
        effective_values[_CONTRACT_FIELDS[contract_type]] = dict(record.payload)
        references.append(
            KernelContractReference(
                contract_record_id=record.contract_record_id,
                contract_type=record.contract_type,
                version_number=record.version_number,
                effective_from_boundary=int(record.effective_from_boundary or 0),
                status=record.status.value,
            )
        )
    proposals = [
        record.model_dump(mode="json")
        for record in all_records
        if record.status.value in {"INFERRED_PROPOSAL", "NEEDS_REVIEW"}
    ]
    workspace = build_progression_workspace_from_world_state(
        database,
        book_id=book_id,
        edition_id=edition_id,
        world_state=world_state,
        planning_target_ordinal=planning_ordinal,
    )
    active_threads = _mapping_list(world_state.get("threads"))
    promises = _mapping_list(world_state.get("promises"))
    debts = _portfolio_debts(
        book_id=book_id,
        edition_id=edition_id,
        chapter_ordinal=context_ordinal,
        active_threads=active_threads,
        promises=promises,
    )
    truth_reveal = author_policy.get("truth_reveal", {})
    truth_reveal = truth_reveal if isinstance(truth_reveal, Mapping) else {}
    reveal_agenda = _mapping_list(truth_reveal.get("reveal_agenda"))
    anticipation = AnticipationSurfaceView.model_validate(workspace["anticipation"])
    drive_payload = effective_values["narrative_drive"]
    drive_contract = (
        None
        if drive_payload is None
        else NarrativeDriveContract.model_validate(drive_payload)
    )
    reader_payload = effective_values["reader_experience"] or {}
    reader_promises = [str(item) for item in reader_payload.get("must_deliver", [])]
    progression_state = workspace.get("progression_state")
    engine_recommendations = _engine_recommendations(
        drive_contract=drive_contract,
        progression_state=(
            progression_state if isinstance(progression_state, Mapping) else None
        ),
        debts=debts,
        reader_promises=reader_promises,
    )
    author_control = author_policy.get("author_control", {})
    author_control = author_control if isinstance(author_control, Mapping) else {}
    author_tasks = _mapping_list(author_control.get("tasks"))
    scheduler = recommend_chapter_intent(
        debts=debts,
        anticipation=anticipation,
        author_tasks=author_tasks,
        active_thread_ids=[
            _planning_item_id(item)
            for item in active_threads
            if _planning_item_id(item)
        ],
        override=load_scheduler_override(
            database,
            book_id=book_id,
            edition_id=edition_id,
            chapter_ordinal=planning_ordinal,
        ),
        drive_contract=drive_contract,
        engine_recommendations=engine_recommendations,
    )

    known = [f"contract:{reference.contract_type.value}" for reference in references]
    unknown = [
        f"contract:{contract_type.value}"
        for contract_type in ProgressionContractType
        if contract_type not in active_records
    ]
    if progression_state is not None:
        known.append("progression_state")
    elif ProgressionContractType.PROGRESSION in active_records:
        unknown.append("progression_state")
    source_state = world_state.get("source_state", {})
    source_state = source_state if isinstance(source_state, Mapping) else {}
    coverage_status = str(
        world_state.get("coverage_status")
        or source_state.get("projection_status")
        or "UNKNOWN"
    )
    partial = [] if coverage_status.startswith("COMPLETE") else ["source_state"]
    warnings = []
    if not references:
        warnings.append("当前目标章没有已生效 Kernel Contract；Legacy 工作流保持可用。")
    if proposals:
        warnings.append("Proposal Context 仅供作者审阅，不参与评分或 Hard Gate。")

    resource_state = [
        *_mapping_list(world_state.get("resources")),
        *_mapping_list(world_state.get("inventory")),
        *_mapping_list(world_state.get("equipment")),
    ]
    return KernelPlanningContext(
        book_id=book_id,
        edition_id=edition_id,
        target_chapter_id=target_chapter_id,
        target_chapter_ordinal=planning_ordinal,
        context_chapter_id=selected_chapter_id,
        context_chapter_ordinal=context_ordinal,
        effective_contracts=EffectiveKernelContracts.model_validate(effective_values),
        contract_references=sorted(
            references, key=lambda item: item.contract_type.value
        ),
        proposal_context=KernelProposalContext(records=proposals),
        chapter_state=KernelChapterState(
            world_state_reference=KernelWorldStateReference(
                chapter_id=selected_chapter_id,
                chapter_ordinal=context_ordinal,
                availability=str(world_state.get("availability") or "UNKNOWN"),
                coverage_status=coverage_status,
                source_layer=(
                    str(source_state.get("layer")) if source_state.get("layer") else None
                ),
            ),
            progression_state=(
                dict(progression_state)
                if isinstance(progression_state, Mapping)
                else None
            ),
            world_expansion_state=(
                dict(workspace["world_expansion"])
                if isinstance(workspace.get("world_expansion"), Mapping)
                else None
            ),
            opportunity_surface=(
                dict(workspace["opportunity_surface"])
                if isinstance(workspace.get("opportunity_surface"), Mapping)
                else None
            ),
            resource_state=resource_state,
            capability_state=_mapping_list(world_state.get("abilities")),
            knowledge_state=_mapping_list(world_state.get("knowledge")),
        ),
        planning_state=KernelPlanningState(
            anticipation_surface=dict(workspace["anticipation"]),
            narrative_debts=[item.model_dump(mode="json") for item in debts],
            active_threads=active_threads,
            promises=promises,
            reveal_agenda=reveal_agenda,
            scheduler_recommendation=scheduler,
        ),
        author_state=KernelAuthorState(
            author_tasks=author_tasks,
            author_intents=_mapping_list(author_control.get("intents")),
            effective_book_profile=dict(
                author_policy.get("effective_book_profile", {})
            ),
            author_truths=_mapping_list(truth_reveal.get("active_author_truths")),
        ),
        coverage=KernelCoverage(
            known=known,
            partial=partial,
            unknown=unknown,
            blocking_gaps=[],
        ),
        warnings=warnings,
    )


__all__ = [
    "EffectiveKernelContracts",
    "KernelAuthorState",
    "KernelChapterState",
    "KernelContractReference",
    "KernelCoverage",
    "KernelPlanningContext",
    "KernelPlanningState",
    "KernelProposalContext",
    "KernelWorldStateReference",
    "build_kernel_planning_context",
]
