from __future__ import annotations

import json
import shutil
from collections.abc import Mapping, Sequence
from itertools import combinations
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from novel_authoring.config import Settings
from novel_authoring.context.router import (
    ContextPurpose,
    RuntimeContextRequest,
    route_runtime_context,
)
from novel_authoring.db.database import Database
from novel_authoring.edition import edition_workspace, resolve_edition_id
from novel_authoring.metrics.formulas import (
    candidate_score,
    narrative_debt,
    thread_need,
)
from novel_authoring.metrics.formulas import (
    progress as progress_metric,
)
from novel_authoring.metrics.gates import evaluate_hard_gates
from novel_authoring.planning.aggregates import build_planning_aggregate
from novel_authoring.planning.boundary import (
    PlanningError,
    _workspace,
    atlas_soft_thread_rows,
    build_boundary_packet,
)
from novel_authoring.planning.diagnostics import (
    build_narrative_portfolio_snapshot,
    diagnose_candidate_portfolio,
)
from novel_authoring.planning.innovation import (
    InnovationControl,
    NarrativePortfolioSnapshot,
    resolve_innovation_control,
)
from novel_authoring.planning.models import (
    CandidateCreativeOutput,
    CandidateCreativeProposal,
    CandidateOutput,
    CandidateProposal,
    ChapterExperienceSignature,
    PlanningReferenceProvenance,
    ThreadPriority,
)
from novel_authoring.planning.reference_strategy import (
    select_planning_reference_strategy,
)
from novel_authoring.planning.rewards import calculate_candidate_innovation_reward
from novel_authoring.progression.context import KernelPlanningContext
from novel_authoring.progression.evidence import KernelEvidenceCompiler
from novel_authoring.reference_corpus.context import (
    freeze_reference_context,
    load_reference_context_snapshot,
)
from novel_authoring.reference_corpus.query import (
    ReferenceCorpusQueryRequest,
    query_reference_corpus,
)
from novel_authoring.runtime_baseline import load_earned_surface
from novel_authoring.storage.operations import ensure_operation, find_operation
from novel_authoring.utils import json_dumps, sha256_bytes, stable_id, utc_now

STRUCTURE_FIELDS = (
    "event_source",
    "solution_method",
    "protagonist_strategy",
    "risk_form",
    "opportunity_cost",
    "emotional_outcome",
    "social_feedback",
    "scene_topology",
    "ending_state",
)


def _kernel_author_summary(context: KernelPlanningContext) -> dict[str, Any]:
    contracts = context.effective_contracts.model_dump(mode="json")
    reader = contracts.get("reader_experience") or {}
    genre = contracts.get("genre") or {}
    drive = contracts.get("narrative_drive") or {}
    progression = context.chapter_state.progression_state or {}
    primary_axis = progression.get("primary_axis_state", {})
    opportunity = context.chapter_state.opportunity_surface or {}
    anticipation = context.planning_state.anticipation_surface or {}
    core_genre_promises = [
        item
        for item in genre.get("genre_promises", [])
        if isinstance(item, dict) and item.get("strength") == "CORE"
    ]
    return {
        "why_this_book_is_worth_following": reader.get("must_deliver", []),
        "reader_experience_core_promises": [
            *reader.get("must_deliver", []),
            *core_genre_promises,
        ],
        "narrative_drives": {
            "primary_drive": drive.get("primary_drive"),
            "secondary_drives": drive.get("secondary_drives", []),
            "drive_priorities": drive.get("drive_priorities", {}),
        },
        "current_progression": {
            "axis": primary_axis.get("axis_id"),
            "stage": primary_axis.get("current_stage"),
            "next_stage_visibility": primary_axis.get("next_stage_visibility"),
            "bottlenecks": primary_axis.get("current_bottlenecks", []),
            "missing_resources": progression.get("missing_resources", []),
            "pending_ability_showcases": progression.get(
                "pending_ability_showcases", []
            ),
            "growth_costs": progression.get("growth_costs_active", []),
            "readiness": progression.get("next_breakthrough_readiness", "UNKNOWN"),
        },
        "world_expansion": context.chapter_state.world_expansion_state,
        "resources_and_opportunities": {
            "owned_or_current": context.chapter_state.resource_state,
            "opportunities": opportunity.get("items", []),
        },
        "knowledge_boundary": context.chapter_state.knowledge_state,
        "reader_anticipation": anticipation.get("items", []),
        "narrative_debts": context.planning_state.narrative_debts,
        "scheduler_recommendation": (
            None
            if context.planning_state.scheduler_recommendation is None
            else context.planning_state.scheduler_recommendation.model_dump(mode="json")
        ),
        "author_control": {
            "tasks": context.author_state.author_tasks,
            "intents": context.author_state.author_intents,
            "profile": context.author_state.effective_book_profile,
            "truths": context.author_state.author_truths,
            "reveal_agenda": context.planning_state.reveal_agenda,
        },
        "coverage": context.coverage.model_dump(mode="json"),
        "warnings": context.warnings,
    }


def _reference_values(payload: object, *keys: str) -> list[str]:
    if not isinstance(payload, Mapping):
        return []
    values: list[str] = []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, (dict, list)):
            values.extend(str(item) for item in value)
        elif value not in (None, ""):
            values.append(str(value))
    return list(dict.fromkeys(values))


def _contract_payload(value: object) -> dict[str, Any]:
    """Use effective contract business fields whether metadata is wrapped or not."""

    if not isinstance(value, Mapping):
        return {}
    payload = value.get("payload")
    return dict(payload) if isinstance(payload, Mapping) else dict(value)


_CONTROLLED_CREATIVE_PROBLEM_TAGS = frozenset(
    {
        "opening",
        "first-payoff",
        "breakthrough",
        "power-verification",
        "resource-release",
        "pure-upside",
        "post-payoff-anticipation",
        "world-expansion",
        "map-transition",
        "exploration",
        "mystery-reveal",
        "status-rise",
        "ability-rule",
        "artifact-ability",
        "relationship",
        "long-form",
        "fatigue",
        "ending-settlement",
    }
)

_REFERENCE_PROMPT_FORBIDDEN_FIELDS = frozenset(
    {
        "source_refs",
        "source_book_ids",
        "raw",
        "full_dna",
        "book_dna",
        "prose_dna",
        "source_prose",
        "source_content",
        "full_text",
        "raw_text",
    }
)


def _is_forbidden_reference_prompt_field(key: object) -> bool:
    normalized = str(key).casefold().replace("-", "_").replace(" ", "_")
    return normalized in _REFERENCE_PROMPT_FORBIDDEN_FIELDS


def _compact_reference_prompt_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            str(key): _compact_reference_prompt_value(nested)
            for key, nested in value.items()
            if not _is_forbidden_reference_prompt_field(key)
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_compact_reference_prompt_value(item) for item in value]
    return value


def _compact_reference_prompt_cards(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    cards: list[dict[str, Any]] = []
    for card in value:
        compact = _compact_reference_prompt_value(card)
        if isinstance(compact, dict):
            cards.append(compact)
    return cards


def _mapping_rows(value: object) -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        values = list(value.values())
        if values and all(isinstance(item, Mapping) for item in values):
            return [dict(item) for item in values if isinstance(item, Mapping)]
        return [dict(value)]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [dict(item) for item in value if isinstance(item, Mapping)]
    return []


def _number(value: object) -> float | None:
    if isinstance(value, bool) or value in (None, ""):
        return None
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _record_value(value: object, key: str, *, depth: int = 0) -> object:
    if depth > 3 or not isinstance(value, Mapping):
        return None
    nested_value = value.get(key)
    if nested_value not in (None, ""):
        return nested_value
    for nested_key in ("payload", "raw", "attributes"):
        nested = value.get(nested_key)
        found = _record_value(nested, key, depth=depth + 1)
        if found not in (None, ""):
            return found
    encoded = value.get("payload_json")
    if isinstance(encoded, str) and encoded.strip():
        try:
            decoded = json.loads(encoded)
        except (TypeError, ValueError, json.JSONDecodeError):
            decoded = None
        found = _record_value(decoded, key, depth=depth + 1)
        if found not in (None, ""):
            return found
    return None


def _state_rows(
    *,
    boundary_payload: Mapping[str, Any],
    kernel_context: KernelPlanningContext | None,
    story_state: Mapping[str, Any] | None,
) -> dict[str, Any]:
    state = story_state if story_state is not None else boundary_payload
    if kernel_context is None:
        active_threads = _mapping_rows(
            state.get("active_threads", state.get("threads", []))
        )
        promises = _mapping_rows(state.get("promises", []))
        debts = _mapping_rows(
            (boundary_payload.get("narrative_portfolio") or {}).get(
                "narrative_debts", []
            )
            if isinstance(boundary_payload.get("narrative_portfolio"), Mapping)
            else []
        )
        progression = (
            dict(state["progression_state"])
            if isinstance(state.get("progression_state"), Mapping)
            else {}
        )
        resources = _mapping_rows(state.get("resources", []))
        knowledge = _mapping_rows(
            state.get("knowledge")
            or state.get("knowledge_state")
            or state.get("knowledge_boundaries", [])
        )
        raw_world_expansion = state.get("world_expansion_state")
        if not isinstance(raw_world_expansion, Mapping):
            raw_world_expansion = state.get("world_expansion")
        world_expansion = (
            dict(raw_world_expansion) if isinstance(raw_world_expansion, Mapping) else {}
        )
    else:
        active_threads = [
            dict(item)
            for item in kernel_context.planning_state.active_threads
            if isinstance(item, Mapping)
        ]
        promises = [
            dict(item)
            for item in kernel_context.planning_state.promises
            if isinstance(item, Mapping)
        ]
        debts = [
            dict(item)
            for item in kernel_context.planning_state.narrative_debts
            if isinstance(item, Mapping)
        ]
        progression = dict(kernel_context.chapter_state.progression_state or {})
        resources = [dict(item) for item in kernel_context.chapter_state.resource_state]
        knowledge = [dict(item) for item in kernel_context.chapter_state.knowledge_state]
        world_expansion = dict(kernel_context.chapter_state.world_expansion_state or {})

    if not active_threads:
        active_threads = _mapping_rows(state.get("active_threads") or state.get("threads", []))
    if not promises:
        promises = _mapping_rows(state.get("promises", []))
    if not resources:
        resources = _mapping_rows(state.get("resources", []))
    if not knowledge:
        knowledge = _mapping_rows(
            state.get("knowledge")
            or state.get("knowledge_state")
            or state.get("knowledge_boundaries", [])
        )
    if not world_expansion:
        raw_world_expansion = state.get("world_expansion_state")
        if not isinstance(raw_world_expansion, Mapping):
            raw_world_expansion = state.get("world_expansion")
        if isinstance(raw_world_expansion, Mapping):
            world_expansion = dict(raw_world_expansion)

    portfolio = boundary_payload.get("narrative_portfolio")
    portfolio = portfolio if isinstance(portfolio, Mapping) else {}
    if not debts:
        debts = _mapping_rows(portfolio.get("narrative_debts", []))
    if not debts:
        debts = promises
    payoff_ready_ids = [
        str(item)
        for item in portfolio.get("payoff_ready_thread_ids", [])
        if str(item).strip()
    ]
    overdue_ids = [
        str(item)
        for item in portfolio.get("overdue_debt_ids", [])
        if str(item).strip()
    ]
    for item in debts:
        status = str(_record_value(item, "status") or "").upper()
        debt_id = str(
            _record_value(item, "debt_id")
            or _record_value(item, "promise_id")
            or ""
        ).strip()
        thread_id = str(_record_value(item, "thread_id") or "").strip()
        if status == "PAYOFF_READY" and thread_id:
            payoff_ready_ids.append(thread_id)
        if status == "OVERDUE" and debt_id:
            overdue_ids.append(debt_id)

    payoff_readiness = _mapping_rows(state.get("payoff_readiness", []))
    for item in payoff_readiness:
        readiness = str(
            _record_value(item, "readiness") or _record_value(item, "status") or ""
        ).upper()
        if readiness in {"READY", "PAYOFF_READY"}:
            payoff_id = str(
                _record_value(item, "thread_id")
                or _record_value(item, "promise_id")
                or _record_value(item, "channel")
                or ""
            ).strip()
            if payoff_id:
                payoff_ready_ids.append(payoff_id)

    recent_payoffs = _mapping_rows(state.get("recent_payoffs", []))
    relationships = _mapping_rows(state.get("relationships", []))
    innovation = boundary_payload.get("innovation_diagnostics")
    innovation = innovation if isinstance(innovation, Mapping) else {}
    recent_structures = _mapping_rows(boundary_payload.get("recent_structures", []))
    pressure_values: list[float] = []
    for item in active_threads:
        for key in ("pressure", "pressure_score", "deadline_urgency", "goal_blockage"):
            number = _number(_record_value(item, key))
            if number is not None:
                pressure_values.append(number)
    for item in debts:
        number = _number(_record_value(item, "debt_score"))
        if number is not None:
            pressure_values.append(number)
    for key in ("pressure", "pressure_score"):
        number = _number(progression.get(key))
        if number is not None:
            pressure_values.append(number)
    explicit_pressure = progression.get("resource_pressure")
    if isinstance(explicit_pressure, Mapping):
        explicit_pressure = explicit_pressure.get("score")
    number = _number(explicit_pressure)
    if number is not None:
        pressure_values.append(number)
    current_position = boundary_payload.get("current_position")
    current_chapter = (
        int(current_position.get("last_canon_chapter") or 0)
        if isinstance(current_position, Mapping)
        else 0
    )
    chapter = state.get("chapter")
    if isinstance(chapter, Mapping) and chapter.get("ordinal") is not None:
        current_chapter = int(chapter.get("ordinal") or 0)
    primary_axis = progression.get("primary_axis_state")
    primary_axis = primary_axis if isinstance(primary_axis, Mapping) else {}
    bottlenecks = [
        str(item)
        for item in primary_axis.get("current_bottlenecks", [])
        if str(item).strip()
    ]
    missing_resources = [
        str(item)
        for item in progression.get("missing_resources", [])
        if str(item).strip()
    ]
    pending_showcases = [
        str(item)
        for item in progression.get("pending_ability_showcases", [])
        if str(item).strip()
    ]
    def resource_is_constrained(item: Mapping[str, Any]) -> bool:
        status = str(_record_value(item, "status") or "").upper()
        quantity = _number(_record_value(item, "quantity"))
        return status in {"BLOCKED", "SHORTFALL", "EXHAUSTED"} or (
            quantity is not None and quantity <= 0
        )

    resource_pressure = bool(missing_resources) or any(
        resource_is_constrained(item) for item in resources
    )
    if number is not None and number >= 60:
        resource_pressure = True
    payoff_ready_ids = sorted(set(payoff_ready_ids))
    overdue_ids = sorted(set(overdue_ids))
    debt_types = {
        str(_record_value(item, "debt_type") or "").upper()
        for item in debts
        if _record_value(item, "debt_type")
    }
    mystery = bool(
        "MYSTERY" in debt_types
        or any(
            str(
                _record_value(item, "state")
                or _record_value(item, "knowledge_state")
                or _record_value(item, "visibility_status")
                or ""
            ).upper()
            == "UNKNOWN"
            for item in knowledge
        )
        or bool(kernel_context and kernel_context.planning_state.reveal_agenda)
    )
    relationship = bool("RELATIONSHIP" in debt_types or relationships)
    repeated_patterns = _mapping_rows(innovation.get("repeated_patterns", []))
    repeated = bool(
        innovation.get("repeated_patterns")
        or str(innovation.get("recent_pattern_distance", "")).lower() == "low"
        or repeated_patterns
        or any(str(_record_value(item, "pattern") or "").strip() for item in recent_structures)
    )
    world_expansion_ready = bool(
        world_expansion.get("stage_id")
        or world_expansion.get("current_stage")
        or world_expansion.get("next_stage")
        or world_expansion.get("available_branches")
    )
    map_transition = any(
        bool(world_expansion.get(key))
        for key in ("map_transition", "region_transition", "location_transition", "next_region")
    )
    tags: list[str] = []

    def add_tag(tag: str) -> None:
        if tag in _CONTROLLED_CREATIVE_PROBLEM_TAGS and tag not in tags:
            tags.append(tag)

    if active_threads or overdue_ids:
        add_tag("long-form")
    if bottlenecks or str(progression.get("next_breakthrough_readiness", "")).upper() in {
        "READY_TO_ATTEMPT",
        "GATE_SATISFIED",
    }:
        add_tag("breakthrough")
    if pending_showcases:
        add_tag("power-verification")
    if resource_pressure:
        add_tag("resource-release")
    if payoff_ready_ids or recent_payoffs:
        add_tag("post-payoff-anticipation")
    if world_expansion_ready:
        add_tag("world-expansion")
    if map_transition:
        add_tag("map-transition")
    if relationship:
        add_tag("relationship")
    if mystery:
        add_tag("mystery-reveal")
    if repeated:
        add_tag("fatigue")

    unknown: list[str] = []
    if not pressure_values:
        unknown.append("pressure")
    if not payoff_ready_ids and not recent_payoffs:
        unknown.append("payoff_readiness")
    if not progression:
        unknown.append("progression_bottleneck")
    if not resource_pressure and not resources:
        unknown.append("resource_pressure")
    if not world_expansion_ready:
        unknown.append("world_expansion")
    if not relationship:
        unknown.append("relationship")
    if not mystery:
        unknown.append("mystery")
    if not repeated:
        unknown.append("repetition")
    return {
        "active_threads": active_threads,
        "pressure": max(pressure_values) if pressure_values else None,
        "payoff_ready_ids": payoff_ready_ids,
        "overdue_ids": overdue_ids,
        "bottlenecks": bottlenecks,
        "missing_resources": missing_resources,
        "resource_pressure": resource_pressure,
        "world_expansion_ready": world_expansion_ready,
        "relationship": relationship,
        "mystery": mystery,
        "repeated": repeated,
        "current_chapter": current_chapter,
        "tags": tags,
        "unknown": unknown,
    }


def _continuation_reference_planning_context(
    *,
    book_id: str,
    edition_id: str,
    task_id: str,
    boundary_payload: Mapping[str, Any],
    thread_id: str,
    kernel_context: KernelPlanningContext | None,
    story_state: Mapping[str, Any] | None = None,
    recent_card_ids: Sequence[str] = (),
    recent_solution_ids: Sequence[str] = (),
    recent_signatures: Sequence[Mapping[str, Any]] = (),
    output_path: Path,
) -> dict[str, Any]:
    contracts = (
        {}
        if kernel_context is None
        else kernel_context.effective_contracts.model_dump(mode="json")
    )
    reader = _contract_payload(contracts.get("reader_experience"))
    drive = _contract_payload(contracts.get("narrative_drive"))
    payoff = _contract_payload(contracts.get("payoff_channel"))
    state = _state_rows(
        boundary_payload=boundary_payload,
        kernel_context=kernel_context,
        story_state=story_state,
    )
    pressure = (
        "UNKNOWN"
        if state["pressure"] is None
        else f"{float(state['pressure']):.1f}"
    )
    unknown = ",".join(state["unknown"]) if state["unknown"] else "none"
    query = ReferenceCorpusQueryRequest(
        purpose="PLANNING",
        creative_problem=(
            f"下一章候选需要处理主线程 {thread_id} 的冻结状态与行动空间；"
            f"active_threads={len(state['active_threads'])}；pressure={pressure}；"
            f"payoff_ready={state['payoff_ready_ids'] or 'UNKNOWN'}；"
            f"overdue_debt={state['overdue_ids'] or 'UNKNOWN'}；"
            f"progression_bottleneck={state['bottlenecks'] or 'UNKNOWN'}；"
            f"resource_pressure={'TRUE' if state['resource_pressure'] else 'UNKNOWN'}；"
            f"world_expansion={'TRUE' if state['world_expansion_ready'] else 'UNKNOWN'}；"
            f"relationship={'TRUE' if state['relationship'] else 'UNKNOWN'}；"
            f"mystery={'TRUE' if state['mystery'] else 'UNKNOWN'}；"
            f"repetition={'TRUE' if state['repeated'] else 'UNKNOWN'}；"
            f"unknown={unknown}；"
            "Reference Corpus 只提供可迁移机制，不决定候选。"
        ),
        creative_problem_tags=state["tags"],
        reader_experiences=_reference_values(
            reader,
            "experience_priorities",
            "reader_experiences",
            "primary_experience",
        ),
        narrative_drives=_reference_values(
            drive,
            "primary_drive",
            "secondary_drives",
            "narrative_drives",
        ),
        payoff_channels=_reference_values(
            payoff,
            "channels",
            "payoff_channels",
            "primary_channel",
        ),
        max_cards=6,
    )
    response = query_reference_corpus(query)
    snapshot = freeze_reference_context(
        query,
        response,
        book_id=book_id,
        edition_id=edition_id,
        operation_id=task_id,
        output_path=output_path,
    )
    context = snapshot.model_dump(mode="json")
    strategy = select_planning_reference_strategy(
        context,
        recent_card_ids=recent_card_ids,
        recent_solution_ids=recent_solution_ids,
        creative_problem=query.creative_problem,
        reader_experiences=query.reader_experiences,
        narrative_drives=query.narrative_drives,
        payoff_channels=query.payoff_channels,
        scene_functions=query.scene_functions,
        recent_signatures=recent_signatures,
    )
    strategy_payload = strategy.model_dump(mode="json")
    strategy_path = output_path.with_name("reference_strategy.json")
    strategy_path.write_text(
        json_dumps(strategy_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    context["reference_strategy"] = strategy_payload
    context["reference_strategy_path"] = str(strategy_path)
    return context


def _load_frozen_reference_inputs(metadata: dict[str, Any]) -> None:
    """Use the persisted snapshot/strategy instead of a mutable task copy."""

    planning_context = metadata.get("reference_planning_context")
    if not isinstance(planning_context, Mapping):
        return
    snapshot_path = Path(str(metadata.get("reference_context_snapshot") or ""))
    if snapshot_path.is_file():
        snapshot = load_reference_context_snapshot(snapshot_path)
        expected_snapshot_hash = str(planning_context.get("snapshot_hash") or "")
        if expected_snapshot_hash and snapshot.snapshot_hash != expected_snapshot_hash:
            raise PlanningError("冻结 Reference Context Snapshot 与 task.json 不一致")
    strategy_path = Path(
        str(
            planning_context.get("reference_strategy_path")
            or metadata.get("reference_strategy_path")
            or ""
        )
    )
    if not strategy_path.is_file():
        return
    try:
        frozen_strategy = json.loads(strategy_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PlanningError("冻结 reference_strategy.json 无法读取") from exc
    if not isinstance(frozen_strategy, dict):
        raise PlanningError("冻结 reference_strategy.json 必须是 object")
    embedded = metadata.get("reference_strategy")
    if isinstance(embedded, Mapping) and dict(embedded) != frozen_strategy:
        raise PlanningError("冻结 reference_strategy.json 与 task.json 不一致")
    metadata["reference_strategy"] = frozen_strategy


def _validate_author_control_trace(
    candidate: CandidateProposal, author_control: dict[str, Any]
) -> None:
    """Ensure a candidate can only claim against the frozen planning inputs."""

    tasks = {
        str(item.get("task_id")): item
        for item in author_control.get("tasks", [])
        if isinstance(item, dict) and item.get("task_id")
    }
    intents = {
        str(item.get("intent_id")): item
        for item in author_control.get("intents", [])
        if isinstance(item, dict) and item.get("intent_id")
    }
    trace = candidate.author_control_trace
    task_hit_ids = {item.task_id for item in trace.author_task_hits}
    intent_hit_ids = {item.intent_id for item in trace.author_intent_hits}
    unknown_tasks = (task_hit_ids | set(trace.author_tasks_advanced)) - set(tasks)
    unknown_intents = (intent_hit_ids | set(trace.author_intents_advanced)) - set(intents)
    unknown_goals = set(trace.author_goals_not_used) - (set(tasks) | set(intents))
    if unknown_tasks or unknown_intents or unknown_goals:
        raise PlanningError(
            "AuthorControlTrace 引用了未冻结的任务/意图："
            f"tasks={sorted(unknown_tasks)}, intents={sorted(unknown_intents)}, "
            f"goals={sorted(unknown_goals)}"
        )
    if not set(trace.author_tasks_advanced).issubset(task_hit_ids):
        raise PlanningError("author_tasks_advanced 必须是 author_task_hits 的子集")
    if not set(trace.author_intents_advanced).issubset(intent_hit_ids):
        raise PlanningError("author_intents_advanced 必须是 author_intent_hits 的子集")
    missing_reasons = set(trace.author_goals_not_used) - set(trace.unused_reasons)
    if missing_reasons:
        raise PlanningError(f"未使用作者目标缺少原因：{sorted(missing_reasons)}")


def _profile_constraint_failures(
    candidate: CandidateProposal, frozen_profile: dict[str, Any]
) -> list[str]:
    if not frozen_profile:
        return []
    if (
        not candidate.profile_alignment.dimensions
        and not candidate.profile_alignment.constraint_checks
    ):
        # Creative submissions do not repeat system-owned alignment metadata.
        # Unknown soft alignment is retained in the persisted score context;
        # explicit hard violations still arrive through gate_input.
        return []
    expected_dimensions = {
        str(item.get("dimension"))
        for item in frozen_profile.get("dimensions", [])
        if isinstance(item, dict) and item.get("dimension")
    }
    actual_dimensions = {
        item.dimension for item in candidate.profile_alignment.dimensions
    }
    if actual_dimensions != expected_dimensions:
        raise PlanningError(
            f"候选 {candidate.local_id} 必须逐维检查 Effective Profile："
            f"missing={sorted(expected_dimensions - actual_dimensions)}, "
            f"unknown={sorted(actual_dimensions - expected_dimensions)}"
        )
    hard_constraints = frozen_profile.get("hard_constraints", {})
    expected_checks = {
        str(item.get("edit_id"))
        for strength in ("must", "must_not")
        for item in hard_constraints.get(strength, [])
        if isinstance(item, dict) and item.get("edit_id")
    }
    checks = {
        item.edit_id: item for item in candidate.profile_alignment.constraint_checks
    }
    if set(checks) != expected_checks:
        raise PlanningError(
            f"候选 {candidate.local_id} 的 Profile 硬约束检查不完整："
            f"missing={sorted(expected_checks - set(checks))}, "
            f"unknown={sorted(set(checks) - expected_checks)}"
        )
    return [
        f"Profile 硬约束未通过 {check.edit_id}：{check.evidence}"
        for check in checks.values()
        if not check.passed
    ]


def _truth_reveal_failures(
    candidate: CandidateProposal, frozen: dict[str, Any]
) -> list[str]:
    previews = [
        *candidate.reveal_impact.hints,
        *candidate.reveal_impact.partial_reveals,
        *candidate.reveal_impact.full_reveals,
    ]
    if not frozen:
        if candidate.truth_alignment or previews or candidate.reveal_impact.secrets_used:
            raise PlanningError(
                f"候选 {candidate.local_id} 在未冻结 Truth/Agenda 时声明了揭示"
            )
        return []
    active = {
        str(item.get("truth_id")): item
        for item in frozen.get("active_author_truths", [])
        if isinstance(item, dict) and item.get("truth_id")
    }
    agenda = frozen.get("reveal_agenda", {})

    def truth_ids(key: str) -> set[str]:
        return {
            str(item.get("truth_id"))
            for item in agenda.get(key, [])
            if isinstance(item, dict) and item.get("truth_id")
        }

    must_reveal = truth_ids("must_reveal")
    should_hint = truth_ids("should_hint")
    keep_hidden = truth_ids("keep_hidden")
    alignments = {item.truth_id: item for item in candidate.truth_alignment}
    if len(alignments) != len(candidate.truth_alignment):
        raise PlanningError(f"候选 {candidate.local_id} 的 truth_alignment 存在重复 truth_id")
    unknown = set(alignments) - set(active)
    if unknown:
        raise PlanningError(
            f"候选 {candidate.local_id} 引用了未冻结的 Author Truth：{sorted(unknown)}"
        )
    failures = [
        f"未遵守 Author Truth {item.truth_id}：{item.behavioral_effect}"
        for item in candidate.truth_alignment
        if not item.respected
    ]
    bucket_by_truth = {
        truth_id: bucket
        for bucket, key in (
            ("MUST_REVEAL", "must_reveal"),
            ("SHOULD_HINT", "should_hint"),
            ("KEEP_HIDDEN", "keep_hidden"),
            ("OPTIONAL", "optional"),
        )
        for truth_id in truth_ids(key)
    }
    for truth_id, alignment in alignments.items():
        expected_bucket = bucket_by_truth.get(truth_id, "KEEP_HIDDEN")
        if alignment.agenda_bucket != expected_bucket:
            failures.append(
                f"Truth {truth_id} 的 agenda_bucket 应为 {expected_bucket}，"
                f"候选却声明 {alignment.agenda_bucket}"
            )
    hints = {item.truth_id: item for item in candidate.reveal_impact.hints}
    partial = {item.truth_id: item for item in candidate.reveal_impact.partial_reveals}
    full = {item.truth_id: item for item in candidate.reveal_impact.full_reveals}
    for preview in candidate.reveal_impact.partial_reveals:
        if preview.depth != "PARTIAL_REVEAL":
            failures.append(
                f"Truth {preview.truth_id} 的 partial_reveals 必须使用 PARTIAL_REVEAL"
            )
    for preview in candidate.reveal_impact.full_reveals:
        if preview.depth not in {"CONFIRMATION", "FULL_REVEAL"}:
            failures.append(
                f"Truth {preview.truth_id} 的 full_reveals 深度无效：{preview.depth}"
            )
    revealed = set(hints) | set(partial) | set(full)
    referenced = (
        revealed
        | set(candidate.reveal_impact.secrets_used)
        | set(candidate.reveal_impact.kept_hidden)
    )
    unknown_reveal_ids = referenced - set(active)
    if unknown_reveal_ids:
        raise PlanningError(
            f"候选 {candidate.local_id} 的 reveal_impact 引用了未冻结 Truth："
            f"{sorted(unknown_reveal_ids)}"
        )
    agenda_items = {
        str(item["truth_id"]): item
        for key in ("must_reveal", "should_hint", "keep_hidden", "optional")
        for item in agenda.get(key, [])
        if isinstance(item, dict) and item.get("truth_id")
    }
    for preview in previews:
        planned = agenda_items.get(preview.truth_id)
        if planned is None:
            failures.append(f"Truth {preview.truth_id} 没有本章 Reveal Agenda 授权")
            continue
        plan = planned.get("plan") or {}
        expected_target = str(plan.get("target") or "READER")
        expected_entity = plan.get("target_entity_id")
        if preview.target != expected_target or preview.target_entity_id != expected_entity:
            failures.append(
                f"Truth {preview.truth_id} 的 Reveal target 与冻结 RevealPlan 不一致"
            )
    for truth_id in keep_hidden:
        if truth_id in revealed:
            failures.append(f"KEEP_HIDDEN Truth {truth_id} 被候选写成可见揭示")
    for truth_id in should_hint:
        hint_preview = hints.get(truth_id)
        if hint_preview is None or not hint_preview.clue.strip():
            failures.append(f"SHOULD_HINT Truth {truth_id} 缺少可读线索")
        elif hint_preview.depth not in {"HINT", "STRONG_HINT", "FALSE_LEAD"}:
            failures.append(
                f"SHOULD_HINT Truth {truth_id} 使用了越界深度 {hint_preview.depth}"
            )
        if truth_id in partial or truth_id in full:
            failures.append(f"HINT Truth {truth_id} 越界成 PARTIAL/FULL REVEAL")
    for truth_id in must_reveal:
        if truth_id not in partial and truth_id not in full:
            failures.append(f"MUST_REVEAL Truth {truth_id} 未在候选中兑现")
        reveal_preview = partial.get(truth_id) or full.get(truth_id)
        expected_depth = str(agenda_items.get(truth_id, {}).get("reveal_depth") or "")
        if (
            reveal_preview is not None
            and expected_depth
            and reveal_preview.depth != expected_depth
        ):
            failures.append(
                f"MUST_REVEAL Truth {truth_id} 应使用 {expected_depth}，"
                f"候选却使用 {reveal_preview.depth}"
            )
    return failures


def _creative_candidate_text(candidate: Any) -> str:
    values = candidate.model_dump(mode="json")
    parts: list[str] = []
    for key, value in values.items():
        if key in {"novelty_provenance", "innovation_preview", "reveal_impact"}:
            continue
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif isinstance(value, dict):
            parts.extend(str(item) for item in value.values())
        elif value is not None:
            parts.append(str(value))
    return " ".join(parts)


_NON_BUSINESS_FREEZE_FIELDS = frozenset(
    {
        "created_at",
        "updated_at",
        "generated_at",
        "frozen_at",
        "created_timestamp",
        "updated_timestamp",
        "generated_timestamp",
        "equivalent_timestamp",
    }
)


def _normalize_frozen_semantics(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _normalize_frozen_semantics(item)
            for key, item in value.items()
            if str(key) not in _NON_BUSINESS_FREEZE_FIELDS
        }
    if isinstance(value, list):
        return [_normalize_frozen_semantics(item) for item in value]
    return value


def _effective_kept_hidden(candidate: CandidateProposal, frozen: dict[str, Any]) -> list[str]:
    agenda = frozen.get("reveal_agenda", {}) if isinstance(frozen, dict) else {}
    hidden = {
        str(item.get("truth_id"))
        for item in agenda.get("keep_hidden", [])
        if isinstance(item, dict) and item.get("truth_id")
    }
    revealed = {
        item.truth_id
        for item in (
            *candidate.reveal_impact.hints,
            *candidate.reveal_impact.partial_reveals,
            *candidate.reveal_impact.full_reveals,
        )
    }
    return sorted(hidden - revealed)


def _derive_candidate_defensive_fields(
    metadata: Mapping[str, Any],
    frozen_truth_reveal: Mapping[str, Any],
) -> dict[str, Any]:
    """Compile only explicit Boundary/Directive/Reveal/Style constraints."""

    boundary: dict[str, Any] = {}
    boundary_path = metadata.get("boundary_path")
    if boundary_path and Path(str(boundary_path)).is_file():
        try:
            loaded = json.loads(Path(str(boundary_path)).read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                boundary = loaded
        except (OSError, UnicodeError, TypeError, ValueError, json.JSONDecodeError):
            boundary = {}
    directives = [
        item
        for item in boundary.get("author_directives", [])
        if isinstance(item, Mapping) and str(item.get("content") or "").strip()
    ]
    must_not_resolve = [
        str(item["content"])
        for item in directives
        if str(item.get("directive_type") or item.get("type") or "").casefold()
        in {"forbidden", "must_not"}
    ]
    canon_constraints = [
        str(item["content"])
        for item in directives
        if str(item.get("directive_type") or item.get("type") or "").casefold()
        in {"requirement", "canon_constraint"}
    ]
    agenda = frozen_truth_reveal.get("reveal_agenda", {})
    if isinstance(agenda, Mapping):
        must_not_resolve.extend(
            f"KEEP_HIDDEN:{item.get('truth_id')}"
            for item in agenda.get("keep_hidden", [])
            if isinstance(item, Mapping) and item.get("truth_id")
        )
    knowledge_constraints = []
    for character_id, value in (boundary.get("knowledge_boundaries") or {}).items():
        if not isinstance(value, Mapping):
            continue
        if str(value.get("knowledge_state") or value.get("state") or "").upper() in {
            "UNKNOWN",
            "DENIED",
            "UNAVAILABLE",
        }:
            knowledge_constraints.append(f"{character_id}: {json_dumps(dict(value))}")
    forbidden_repetitions: list[str] = []
    recent_avoid_repetitions: list[str] = []
    for item in boundary.get("recent_structures", []):
        if not isinstance(item, Mapping):
            continue
        signature = item.get("signature") or item.get("pattern") or item.get("tag")
        if signature:
            recent_avoid_repetitions.append(str(signature))
    forbidden_repetitions.extend(
        str(item["content"])
        for item in directives
        if str(item.get("directive_type") or item.get("type") or "").casefold()
        in {"forbidden_repetition", "repetition_forbidden", "must_not_repeat"}
    )
    style_constraints: dict[str, str] = {}
    profiles = boundary.get("style_profiles", [])
    if isinstance(profiles, list) and profiles and isinstance(profiles[-1], Mapping):
        for key in ("pov", "tense", "register", "dialogue", "sentence_rhythm"):
            if profiles[-1].get(key) not in (None, ""):
                style_constraints[key] = str(profiles[-1][key])
    return {
        "must_not_resolve": list(dict.fromkeys(must_not_resolve)),
        "canon_constraints": list(dict.fromkeys(canon_constraints)),
        "knowledge_constraints": list(dict.fromkeys(knowledge_constraints)),
        "forbidden_repetitions": list(dict.fromkeys(forbidden_repetitions)),
        "recent_avoid_repetitions": list(dict.fromkeys(recent_avoid_repetitions)),
        "style_constraints": style_constraints,
    }


def _compile_creative_candidate(
    candidate: Any,
    *,
    metadata: dict[str, Any],
    frozen_truth_reveal: dict[str, Any],
) -> CandidateProposal:
    """Compile executor creative choices into the internal planning model."""

    payload = candidate.model_dump(mode="json")
    priorities = metadata.get("thread_priorities", [])
    priority = None
    for item in priorities:
        if (
            isinstance(item, dict)
            and str(item.get("thread_id") or "") == candidate.primary_thread_id
        ):
            raw_score = item.get("score")
            if raw_score is not None:
                priority = float(raw_score)
                break
    pressure_before = candidate.pressure_before
    pressure_after = candidate.pressure_target_after
    if pressure_before is None:
        pressure_before = priority
    if pressure_after is None:
        pressure_after = priority
    if pressure_before is None:
        pressure_before = 0.0
    if pressure_after is None:
        pressure_after = pressure_before
    payload["pressure_before"] = pressure_before
    payload["pressure_target_after"] = pressure_after
    # These are internal constraints compiled from the frozen planning
    # context.  The executor no longer submits them as if they were scores or
    # governance decisions.
    payload.update(_derive_candidate_defensive_fields(metadata, frozen_truth_reveal))
    payload["commit_updates"] = list(
        dict.fromkeys(
            [
                *candidate.state_changes,
                *(
                    [candidate.required_irreversible_change]
                    if candidate.required_irreversible_change.strip()
                    else []
                ),
            ]
        )
    )
    reference_context = metadata.get("reference_planning_context")
    reference_strategy = metadata.get("reference_strategy")
    if not isinstance(reference_strategy, dict):
        reference_strategy = {}
    if not isinstance(reference_context, dict):
        reference_context = {}
    payload["reference_provenance"] = PlanningReferenceProvenance(
        reference_strategy_id=(
            str(reference_strategy.get("strategy_id"))
            if reference_strategy.get("strategy_id")
            else None
        ),
        snapshot_id=(
            str(
                reference_strategy.get("snapshot_id")
                or reference_context.get("snapshot_id")
            )
            if reference_strategy.get("snapshot_id")
            or reference_context.get("snapshot_id")
            else None
        ),
        snapshot_hash=(
            str(
                reference_strategy.get("snapshot_hash")
                or reference_context.get("snapshot_hash")
            )
            if reference_strategy.get("snapshot_hash")
            or reference_context.get("snapshot_hash")
            else None
        ),
        card_ids_used=[
            str(item)
            for item in (
                reference_strategy.get("selected_card_ids")
                or reference_context.get("selected_card_ids")
                or []
            )
        ],
        selected_solutions=[
            str(item)
            for item in (
                reference_strategy.get("selected_contrast_solutions")
                or reference_strategy.get("selected_solutions")
                or []
            )
        ],
        application_summary=str(reference_strategy.get("application_summary") or ""),
        match_tier=str(
            reference_strategy.get("match_tier")
            or reference_context.get("match_tier")
            or "EXACT"
        ),
    ).model_dump(mode="json")
    reveal_payload = dict(payload.get("reveal_impact") or {})
    reveal_payload["kept_hidden"] = []
    payload["reveal_impact"] = reveal_payload
    payload["score_inputs"] = {}
    payload["score_evidence"] = {}
    if priority is not None:
        payload["score_inputs"] = {"thread_need_fit": priority}
        payload["score_evidence"] = {
            "thread_need_fit": [
                f"冻结线程优先级：{candidate.primary_thread_id}={priority:g}"
            ]
        }
    payload["gate_input"] = {
        "character_fit_inputs": {},
        "style_fit_inputs": {},
    }
    compiled = CandidateProposal.model_validate(payload)
    compiled = compiled.model_copy(
        update={
            "reveal_impact": compiled.reveal_impact.model_copy(
                update={"kept_hidden": _effective_kept_hidden(compiled, frozen_truth_reveal)}
            )
        }
    )
    return compiled


def _parse_creative_output(raw_output: str) -> CandidateCreativeOutput:
    """Keep valid creative candidates when an optional third item is malformed."""

    try:
        return CandidateCreativeOutput.model_validate_json(raw_output)
    except ValidationError as original_error:
        try:
            payload = json.loads(raw_output)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise original_error from exc
        if not isinstance(payload, dict) or set(payload) - {
            "task_id",
            "candidates",
            "notes",
        }:
            raise original_error
        raw_candidates = payload.get("candidates")
        if not isinstance(raw_candidates, list) or not 2 <= len(raw_candidates) <= 3:
            raise original_error
        valid: list[CandidateCreativeProposal] = []
        rejected = 0
        for raw_candidate in raw_candidates:
            try:
                valid.append(CandidateCreativeProposal.model_validate(raw_candidate))
            except ValidationError:
                rejected += 1
        if len(valid) < 2:
            raise original_error
        notes = [str(item) for item in payload.get("notes", [])]
        notes.append(
            f"{rejected} 个候选因创意提交 schema 无效被忽略；"
            f"保留 {len(valid)} 个有效候选。"
        )
        return CandidateCreativeOutput(
            task_id=str(payload.get("task_id") or ""),
            candidates=valid,
            notes=notes,
        )


def _current_ordinal(connection: Any, book_id: str, edition_id: str = "base") -> int:
    from novel_authoring.edition import edition_chapters

    chapters = edition_chapters(connection, book_id, edition_id)
    return max((int(row["ordinal"]) for row in chapters), default=0)


def _recent_experience_signatures(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Read only validated/approved soft signatures for the next plan prompt."""

    with database.connect() as connection:
        rows = connection.execute(
            "SELECT contract_id, output_json FROM drafts "
            "WHERE book_id=? AND edition_id=? "
            "AND status IN ('VALIDATED','AUTHOR_APPROVED','CANON_COMMITTED') "
            "ORDER BY created_at DESC LIMIT ?",
            (book_id, edition_id, max(1, min(limit * 3, 30))),
        ).fetchall()
    signatures: list[dict[str, Any]] = []
    seen_contracts: set[str] = set()
    for row in rows:
        contract_id = str(row["contract_id"] or "")
        if contract_id and contract_id in seen_contracts:
            continue
        try:
            payload = json.loads(str(row["output_json"] or "{}"))
            signature = payload.get("chapter_experience_signature")
            parsed = ChapterExperienceSignature.model_validate(signature)
        except (TypeError, ValueError, json.JSONDecodeError, ValidationError):
            continue
        if contract_id:
            seen_contracts.add(contract_id)
        signatures.append(parsed.model_dump(mode="json"))
        if len(signatures) >= max(1, min(limit, 10)):
            break
    return signatures


_EXPERIENCE_SIGNATURE_FIELDS = (
    "event_source",
    "solution_method",
    "protagonist_strategy",
    "risk_form",
    "emotional_outcome",
    "social_feedback",
    "scene_topology",
    "ending_mode",
    "outcome_magnitude",
    "action_space_delta",
    "knowledge_delta",
    "relationship_delta",
    "world_scale_delta",
)


def _candidate_experience_overlap(
    candidate: CandidateProposal,
    recent_signatures: Sequence[Mapping[str, Any]],
) -> int:
    """Return a small soft repetition penalty in score points."""

    best = 0
    candidate_values = candidate.model_dump(mode="json")
    for recent in recent_signatures:
        overlap = sum(
            bool(candidate_values.get(field))
            and str(candidate_values.get(field)).strip()
            == str(recent.get(field) or "").strip()
            for field in _EXPERIENCE_SIGNATURE_FIELDS
        )
        best = max(best, overlap)
    return min(8, max(0, best - 1) * 2)


def _recent_reference_memory(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    limit: int = 10,
) -> tuple[list[str], list[str]]:
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT output_json FROM drafts WHERE book_id=? AND edition_id=? "
            "AND status IN ('VALIDATED','AUTHOR_APPROVED','CANON_COMMITTED') "
            "ORDER BY created_at DESC LIMIT ?",
            (book_id, edition_id, max(1, min(limit, 10))),
        ).fetchall()
    ids: list[str] = []
    solution_ids: list[str] = []
    for row in rows:
        try:
            payload = json.loads(str(row["output_json"] or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        provenance = payload.get("reference_provenance")
        if not isinstance(provenance, Mapping):
            continue
        values = provenance.get("card_ids_used", [])
        if isinstance(values, Sequence) and not isinstance(values, str):
            ids.extend(str(item) for item in values if str(item).strip())
        solutions = provenance.get("selected_solutions", [])
        if isinstance(solutions, Sequence) and not isinstance(solutions, str):
            solution_ids.extend(str(item) for item in solutions if str(item).strip())
    return list(dict.fromkeys(ids)), list(dict.fromkeys(solution_ids))


def rank_threads(
    database: Database,
    book_id: str,
    settings: Settings,
    *,
    edition_id: str = "base",
) -> list[ThreadPriority]:
    projection = None
    if edition_id != "base":
        from novel_authoring.canon.projection import rebuild_projection

        projection = rebuild_projection(database, book_id, edition_id=edition_id, persist=False)
    atlas_rows = atlas_soft_thread_rows(database, book_id, edition_id)
    with database.connect() as connection:
        current_ordinal = _current_ordinal(connection, book_id, edition_id)
        if projection is None:
            rows = connection.execute(
                """
                SELECT * FROM threads
                WHERE book_id=? AND edition_id=?
                  AND status IN ('CANON','AUTHOR_INTENT','APPROVED_OUTLINE')
                  AND phase NOT IN ('resolved','closed')
                ORDER BY importance DESC, thread_id
                """,
                (book_id, edition_id),
            ).fetchall()
            if not rows:
                rows = atlas_rows
        else:
            rows = []
            for thread_id, value in projection.threads.items():
                item = dict(value)
                item.setdefault("thread_id", thread_id)
                item.setdefault("status", "CANON")
                item.setdefault("phase", "active")
                item.setdefault("importance", 0.5)
                item.setdefault("progress", 0.0)
                item.setdefault("goal", "")
                item.setdefault("introduced_chapter", 0)
                item.setdefault("last_advanced_chapter", 0)
                item.setdefault("payload_json", json_dumps(item))
                if str(item["phase"]) not in {"resolved", "closed"}:
                    rows.append(item)
            rows.sort(key=lambda row: (-float(row["importance"]), str(row["thread_id"])))
            if not rows:
                rows = atlas_rows
        priorities: list[ThreadPriority] = []
        for row in rows:
            payload = json.loads(str(row["payload_json"]))
            if projection is None:
                promise_rows = connection.execute(
                    """
                    SELECT * FROM promises
                    WHERE book_id=? AND edition_id=? AND thread_id=? AND status='CANON'
                    """,
                    (book_id, edition_id, row["thread_id"]),
                ).fetchall()
            else:
                promise_rows = []
                for promise_id, value in projection.promises.items():
                    item = dict(value)
                    item.setdefault("promise_id", promise_id)
                    item.setdefault("status", "CANON")
                    item.setdefault("importance", 0.5)
                    item.setdefault("reader_visibility", 0.5)
                    item.setdefault("progress", 0.0)
                    item.setdefault("introduced_ordinal", 0)
                    item.setdefault("target_max_age", 8)
                    item.setdefault("reminder_count", 0)
                    if str(item.get("thread_id")) == str(row["thread_id"]):
                        promise_rows.append(item)
            debts = []
            for promise in promise_rows:
                debt = narrative_debt(
                    importance=float(promise["importance"]),
                    reader_visibility=float(promise["reader_visibility"]),
                    promise_progress=float(promise["progress"]),
                    age_chapters=max(0, current_ordinal - int(promise["introduced_ordinal"])),
                    target_max_age=int(promise["target_max_age"]),
                    reminder_count=int(promise["reminder_count"]),
                    config=settings.metrics["narrative_debt"],
                ).score
                debts.append(debt)
            last_advanced = int(row["last_advanced_chapter"] or row["introduced_chapter"] or 0)
            gap = max(0, current_ordinal - last_advanced)
            values = {
                "narrative_debt": max(debts, default=0),
                "deadline_urgency": float(payload.get("deadline_urgency", 0)),
                "payoff_readiness": float(
                    payload.get("payoff_readiness", float(row["progress"]) * 100)
                ),
                "recency_neglect": float(payload.get("recency_neglect", min(100, gap / 12 * 100))),
                "goal_blockage": float(
                    payload.get("goal_blockage", (1 - float(row["progress"])) * 100)
                ),
                "protagonist_relevance": float(
                    payload.get("protagonist_relevance", float(row["importance"]) * 100)
                ),
                "diversity_bonus": float(payload.get("diversity_bonus", 50)),
            }
            score = thread_need(values, settings.metrics["thread_need"])
            priorities.append(
                ThreadPriority(
                    thread_id=str(row["thread_id"]),
                    goal=str(row["goal"]),
                    score=score,
                    inputs=values,
                    evidence=[
                        f"active promises={len(promise_rows)}",
                        f"chapters since advance={gap}",
                        f"importance={row['importance']}",
                    ],
                )
            )
    return sorted(priorities, key=lambda item: (-item.score, item.thread_id))[:3]


def prepare_candidate_task(
    database: Database,
    book_id: str,
    settings: Settings,
    *,
    edition_id: str | None = None,
    include_runtime_state: bool = True,
    innovation_control: InnovationControl | None = None,
    innovation_source: str | None = None,
) -> dict[str, object]:
    selected_innovation = innovation_control
    selected_source = innovation_source or "book_default"
    if selected_innovation is None:
        selected_innovation, selected_source = resolve_innovation_control(
            database, book_id
        )
    selected_edition = resolve_edition_id(database, book_id, edition_id)
    boundary = build_boundary_packet(
        database,
        book_id,
        recent_full_chapters=settings.recent_full_chapters,
        edition_id=selected_edition,
        innovation_control=selected_innovation,
    )
    boundary_payload = json.loads(Path(str(boundary["json_path"])).read_text(encoding="utf-8"))
    frozen_portfolio = boundary_payload.get("narrative_portfolio")
    narrative_portfolio = (
        NarrativePortfolioSnapshot.model_validate(frozen_portfolio)
        if frozen_portfolio is not None
        else build_narrative_portfolio_snapshot(
            active_threads=boundary_payload.get("active_threads", []),
            promises=boundary_payload.get("promises", {}),
            current_chapter=int(
                boundary_payload.get("current_position", {}).get("last_canon_chapter", 0)
            ),
            snapshot_id=f"portfolio-{book_id}-{selected_edition}-{boundary['packet_id']}",
            consecutive_deferrals=int(
                boundary_payload.get("hook_diagnostics", {}).get(
                    "consecutive_deferrals", 0
                )
            ),
        )
    )
    runtime_context = route_runtime_context(
        database,
        book_id,
        edition_id=selected_edition,
        purpose=ContextPurpose.CANDIDATE_PLANNING,
        request=RuntimeContextRequest(
            purpose=ContextPurpose.CANDIDATE_PLANNING,
            include_runtime_state=include_runtime_state,
        ),
        boundary=boundary_payload,
    )
    threads = rank_threads(database, book_id, settings, edition_id=selected_edition)
    if not threads:
        raise PlanningError("没有可规划的活跃线程；请先完成抽取与 reconcile")
    boundary_truth_reveal = boundary.get("truth_reveal", {})
    if not isinstance(boundary_truth_reveal, dict):
        raise PlanningError("Boundary Packet 的 Truth/Reveal 冻结快照无效")
    aggregate = build_planning_aggregate(
        database,
        book_id,
        edition_id=selected_edition,
        author_policy={"source": "plan-next", "policy_version": "v1"},
        truth_reveal_snapshot=boundary_truth_reveal,
        context_chapter_id=(
            str(boundary_payload.get("recent_full_chapters", [])[-1]["chapter_id"])
            if boundary_payload.get("recent_full_chapters")
            else None
        ),
        target_chapter_ordinal=int(
            boundary_payload.get("current_position", {}).get("next_chapter", 0)
        )
        or None,
    )
    kernel_context = (
        None
        if aggregate.get("kernel_context") is None
        else KernelPlanningContext.model_validate(aggregate["kernel_context"])
    )
    with database.connect() as connection:
        metric_rows = connection.execute(
            """
            SELECT * FROM metric_results WHERE book_id=?
            AND edition_id=?
            AND as_of_event_seq=(
                SELECT MAX(as_of_event_seq) FROM metric_results
                WHERE book_id=? AND edition_id=?
            )
            ORDER BY metric_name
            """,
            (book_id, selected_edition, book_id, selected_edition),
        ).fetchall()
        if len(metric_rows) < 6:
            v2_run = connection.execute(
                """
                SELECT * FROM metric_runs
                WHERE book_id=? AND edition_id=? AND invalidated_at IS NULL
                ORDER BY as_of_event_seq DESC, created_at DESC
                LIMIT 1
                """,
                (book_id, selected_edition),
            ).fetchone()
            if v2_run is not None:
                v2_results = connection.execute(
                    """
                    SELECT * FROM metric_run_results
                    WHERE run_id=?
                    ORDER BY metric_id
                    """,
                    (str(v2_run["run_id"]),),
                ).fetchall()
                metric_rows = [
                    {
                        **dict(row),
                        "as_of_event_seq": v2_run["as_of_event_seq"],
                        "metric_name": row["metric_id"],
                        "inputs_json": row["components_json"],
                        "evidence_json": row["evidence_summary_json"],
                    }
                    for row in v2_results
                ]
    metric_status = (
        "COMPLETE"
        if len(metric_rows) >= 6
        else "PARTIAL"
        if metric_rows
        else "MISSING"
    )
    def metric_row_value(row: Any, key: str, default: Any = None) -> Any:
        if isinstance(row, Mapping):
            return row.get(key, default)
        try:
            return row[key]
        except (IndexError, KeyError, TypeError):
            return default

    available_components = sorted(
        {
            str(
                metric_row_value(row, "metric_name")
                or metric_row_value(row, "metric_id")
                or ""
            )
            for row in metric_rows
            if metric_row_value(row, "metric_name")
            or metric_row_value(row, "metric_id")
        }
    )
    missing_components: set[str] = set()
    for row in metric_rows:
        raw_missing = metric_row_value(row, "missing_components_json", "[]")
        try:
            parsed_missing = json.loads(str(raw_missing))
        except (TypeError, ValueError, json.JSONDecodeError):
            parsed_missing = []
        if isinstance(parsed_missing, list):
            missing_components.update(str(item) for item in parsed_missing)
    metric_context_summary = {
        "metric_status": metric_status,
        "status": metric_status,
        "available_components": available_components,
        "available_count": len(metric_rows),
        "missing_components": sorted(missing_components),
        "warnings": (
            ["部分指标缺失；相关评分分量保持 UNKNOWN，规划继续。"]
            if metric_status != "COMPLETE"
            else []
        ),
    }
    schema = CandidateCreativeOutput.model_json_schema()
    schema_json = json_dumps(schema, indent=2)
    seed = json_dumps(
        {
            "book_id": book_id,
            "boundary": boundary["packet_id"],
            "planning_aggregate": aggregate,
            "threads": [item.model_dump(mode="json") for item in threads],
            "metrics": [dict(row) for row in metric_rows],
            "metric_context": metric_context_summary,
            "runtime_context": runtime_context.model_dump(mode="json"),
            "innovation_control": selected_innovation.model_dump(mode="json"),
            "narrative_portfolio": narrative_portfolio.model_dump(mode="json"),
        }
    )
    task_id = stable_id("plan", seed, sha256_bytes(schema_json.encode()))
    workspace = edition_workspace(database, book_id, selected_edition)
    operation = ensure_operation(
        database,
        book_id,
        selected_edition,
        task_id,
        "PLAN_NEXT",
        {"boundary_packet_id": boundary["packet_id"]},
    )
    task_dir = (
        operation.input
        if operation is not None
        else workspace / "agent_tasks" / task_id
    )
    output_dir = (
        operation.output
        if operation is not None
        else workspace / "agent_outputs" / task_id
    )
    task_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    recent_reference_card_ids, recent_reference_solution_ids = _recent_reference_memory(
        database, book_id, selected_edition
    )
    recent_experience_signatures = _recent_experience_signatures(
        database, book_id, selected_edition
    )
    reference_planning_context = _continuation_reference_planning_context(
        book_id=book_id,
        edition_id=selected_edition,
        task_id=task_id,
        boundary_payload=boundary_payload,
        thread_id=threads[0].thread_id,
        kernel_context=kernel_context,
        story_state=boundary_payload,
        recent_card_ids=recent_reference_card_ids,
        recent_solution_ids=recent_reference_solution_ids,
        recent_signatures=recent_experience_signatures,
        output_path=task_dir / "reference_context_snapshot.json",
    )
    reference_prompt = {
        key: reference_planning_context[key]
        for key in (
            "status",
            "snapshot_id",
            "snapshot_hash",
            "selected_card_count",
            "selected_card_ids",
            "selected_card_types",
            "selected_card_knowledge_levels",
            "knowledge_gaps",
            "warnings",
        )
    }
    strategy_payload = reference_planning_context.get("reference_strategy", {})
    reference_prompt["reference_strategy"] = _compact_reference_prompt_value(
        strategy_payload
    )
    reference_prompt["compact_cards"] = _compact_reference_prompt_cards(
        strategy_payload.get("selected_cards", [])
        if isinstance(strategy_payload, Mapping)
        else []
    )
    input_text = "\n".join(
        [
            f"# 下一章候选任务 `{task_id}`",
            "",
            f"Boundary Packet: `{boundary['markdown_path']}`",
            "",
            "目标提交三个候选；至少提交两个有效候选。不得只换怪物、资源、地点或社会反馈名词。",
            "候选应分别考虑 CONTINUITY_ACTIVE_THREAD、EARNED_OPPORTUNITY、FORWARD_EXPANSION；"
            "这是三种推理 lens，不是固定配额。",
            "当前 InnovationControl 的 creative-distance guidance："
            f"{selected_innovation.creative_distance_guidance}",
            "当前 soft lens tendency："
            f"{selected_innovation.lens_tendency_guidance}；这不是配额，也不是 Score Bonus。",
            "所有 FORWARD_NOVELTY 必须填写 introduction_event、causal_source、"
            "new_state_if_committed、conflicts_checked；不得把未来状态倒写成既有事实。",
            "只填写创意决定；评分、硬门、证据、画像和 Truth 对齐由 Python 根据冻结输入编译。",
            "候选只处于 CANDIDATE，不得写正文或升级为 CANON。",
            "每个候选必须填写 innovation_preview：creative_distance、主要方向、"
            "打开的 future branches、meaningful/cosmetic 判断与 integration_cost。"
            "Preview 是作者可读计划，不是 Candidate Score，也不放松任何 hard gate。",
            "在 Preview 中优先填写结构化 expected_innovation_elements：每项说明 focus、"
            "meaningful/cosmetic、magnitude、causal_source、state before/after、"
            "horizon roles 与 forward introduction；只有存在共同因果链时才填写 synergy。",
            "同时说明 SHORT/MID/LONG 的 payoff、expected_new_debts 与 expected_narrative_delta。"
            "Python 会独立重算 InnovationRewardBreakdown，不接受 agent 自报的 reward 作为事实。",
            "先检查 Narrative Portfolio 中 PAYOFF_READY 与 overdue debt；"
            "不要为了打开新问题而免费延宕已成熟问题。",
            "## Frozen Reference Corpus Planning Context",
            "",
            "下列内容是本次 task 冻结的 compact context；只提供可迁移机制和对照，"
            "不得复制来源人物、事件、设定、句式，也不得改变 Canon、资源、知识边界或候选选择。",
            "```json",
            json_dumps(reference_prompt, indent=2),
            "```",
            "",
            "## Recent Chapter Experience Signatures（soft guidance）",
            "",
            "下面是最近 3—5 个已校验章节的体验签名。重复解决方式、风险形态或结尾模式只"
            "产生软提醒，不构成硬失败；必须说明本案为何复用或如何变化。",
            "```json",
            json_dumps(recent_experience_signatures, indent=2),
            "```",
            "",
            "## 作者控制输入（必须显式检查）",
            "",
            json_dumps(
                aggregate.get("author_policy", {}).get("author_control", {}),
                indent=2,
            ),
            "",
            "Python 会从创意文本与冻结作者控制输入编译可解释的命中/未命中观察；"
            "这只是规划输入，不会自动改变正史。",
            "AUTO 方向只提供推荐；若候选实际走向不同方向，必须在 Preview 中如实标注。",
            "",
            "## Effective Global Book Profile（九维，必须逐维对齐）",
            "",
            json_dumps(
                aggregate.get("author_policy", {}).get(
                    "effective_book_profile", {}
                ),
                indent=2,
            ),
            "",
            "画像契合与 MUST/MUST_NOT 约束由 Python 结合冻结 Profile 编译；"
            "明确 hard constraint 失败仍不可被 Innovation Reward 抵消。",
            "",
            "## Author Truth + Chapter Reveal Agenda（行为约束不等于揭示许可）",
            "",
            json_dumps(
                aggregate.get("author_policy", {}).get("truth_reveal", {}),
                indent=2,
            ),
            "",
            "候选只填写实际计划的 hints、partial/full/false-lead reveal；"
            "KEEP_HIDDEN 从冻结 Agenda 自动保留，不回写。Active Author Truth 可以改变人物行为；"
            "KEEP_HIDDEN 不得出现在旁白、对话或答案式解释中。",
            "",
            "## Frozen Kernel Planning Context（机器冻结输入）",
            "",
            (
                "当前为 Legacy 规划：没有可冻结的 Kernel Context，沿用原有流程。"
                if kernel_context is None
                else json_dumps(_kernel_author_summary(kernel_context), indent=2)
            ),
            "",
            "不要填写 scheduler_alignment、评分、硬门或内部 provenance；Scheduler 是冻结输入，"
            "Python 会根据候选创意与 kernel_context.json 计算对齐和偏离诊断。",
            "",
            "## 三条优先线程",
            "",
            "```json",
            json_dumps([item.model_dump(mode="json") for item in threads], indent=2),
            "```",
            "",
            "## 最新指标",
            "",
            "状态："
            + metric_status
            + "；缺失指标保持 UNKNOWN，不得自行填入估计值。",
            "```json",
            json_dumps(metric_context_summary, indent=2),
            "```",
            "",
            "```json",
            json_dumps([dict(row) for row in metric_rows], indent=2),
            "```",
            "",
            "## 长跨度节奏证据（只改变候选建议，不改变 Candidate Score 权重）",
            "",
            "```json",
            json_dumps(
                {
                    "planning_aggregate": aggregate,
                    "rhythm_diagnostics": json.loads(
                        Path(str(boundary["json_path"])).read_text(encoding="utf-8")
                    ).get("rhythm_diagnostics", {}),
                    "hook_diagnostics": json.loads(
                        Path(str(boundary["json_path"])).read_text(encoding="utf-8")
                    ).get("hook_diagnostics", {}),
                    "runtime_context": runtime_context.model_dump(mode="json"),
                    "innovation_control": selected_innovation.model_dump(mode="json"),
                    "innovation_source": selected_source,
                    "innovation_recommendation": boundary_payload.get(
                        "innovation_diagnostics", {}
                    ),
                    "narrative_portfolio": narrative_portfolio.model_dump(mode="json"),
                },
                indent=2,
            ),
            "```",
        ]
    )
    metadata = {
        "task_id": task_id,
        "task_type": "plan-next",
        "book_id": book_id,
        "edition_id": selected_edition,
        "boundary_packet_id": boundary["packet_id"],
        "boundary_path": boundary["json_path"],
        "aggregate_id": aggregate["aggregate_id"],
        "author_control": aggregate.get("author_policy", {}).get("author_control", {}),
        "author_control_trace_contract": aggregate.get("author_policy", {}).get(
            "trace_contract", {}
        ),
        "effective_book_profile": aggregate.get("author_policy", {}).get(
            "effective_book_profile", {}
        ),
        "truth_reveal": aggregate.get("author_policy", {}).get("truth_reveal", {}),
        "metric_run_ids": aggregate["metric_run_ids"],
        "metric_context": metric_context_summary,
        "bundle_hash": aggregate["bundle_hash"],
        "rhythm_snapshot_id": aggregate.get("rhythm_snapshot_id"),
        "registry_hash": aggregate["registry_hash"],
        "config_hash": aggregate["config_hash"],
        "thread_priorities": [item.model_dump(mode="json") for item in threads],
        "schema_sha256": sha256_bytes(schema_json.encode()),
        "created_at": utc_now(),
        "runtime_context": runtime_context.model_dump(mode="json"),
        "reference_planning_context": reference_planning_context,
        "reference_strategy": strategy_payload,
        "recent_experience_signatures": recent_experience_signatures,
        "recent_reference_card_ids": recent_reference_card_ids,
        "recent_reference_solution_ids": recent_reference_solution_ids,
        "include_runtime_state": include_runtime_state,
        "innovation_control": selected_innovation.model_dump(mode="json"),
        "innovation_source": selected_source,
        "innovation_recommendation": boundary_payload.get("innovation_diagnostics", {}),
        "narrative_portfolio_snapshot": narrative_portfolio.model_dump(mode="json"),
        "kernel_context": str(task_dir / "kernel_context.json"),
        "reference_context_snapshot": str(task_dir / "reference_context_snapshot.json"),
        "scheduler_recommendation": (
            None
            if kernel_context is None
            or kernel_context.planning_state.scheduler_recommendation is None
            else kernel_context.planning_state.scheduler_recommendation.model_dump(mode="json")
        ),
    }
    (task_dir / "input.md").write_text(input_text, encoding="utf-8")
    (task_dir / "schema.json").write_text(schema_json + "\n", encoding="utf-8")
    (task_dir / "task.json").write_text(json_dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (task_dir / "kernel_context.json").write_text(
        json_dumps(
            None
            if kernel_context is None
            else kernel_context.model_dump(mode="json"),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "task_id": task_id,
        "boundary_packet_id": boundary["packet_id"],
        "input": str(task_dir / "input.md"),
        "schema": str(task_dir / "schema.json"),
        "expected_output": str(output_dir / "output.json"),
        "top_threads": [item.model_dump(mode="json") for item in threads],
        "aggregate_id": aggregate["aggregate_id"],
        "bundle_hash": aggregate["bundle_hash"],
        "effective_book_profile": metadata["effective_book_profile"],
        "truth_reveal": metadata["truth_reveal"],
        "kernel_context": metadata["kernel_context"],
        "reference_planning_context": reference_planning_context,
    }


def prepare_handoff_candidate_task(
    database: Database,
    book_id: str,
    handoff_id: str,
) -> dict[str, object]:
    """Prepare the three-candidate contract from a frozen local handoff."""

    database.initialize()
    with database.connect() as connection:
        handoff = connection.execute(
            "SELECT * FROM workflow_handoffs WHERE handoff_id=? AND book_id=?",
            (handoff_id, book_id),
        ).fetchone()
    if handoff is None:
        raise PlanningError("handoff 不存在")
    if str(handoff["handoff_type"]) != "CONTINUATION":
        raise PlanningError("只有 CONTINUATION handoff 可以准备候选")
    if str(handoff["requested_stage"]) != "PLAN_ONLY":
        raise PlanningError("handoff 不是 PLAN_ONLY")
    if str(handoff["status"]) not in {"READY_FOR_CODEX", "CLAIMED", "RUNNING"}:
        raise PlanningError("handoff 当前状态不能准备候选")

    edition_id = str(handoff["edition_id"])
    aggregate_id = str(handoff["planning_aggregate_id"] or "")
    if not aggregate_id:
        raise PlanningError("handoff 缺少 Planning Aggregate")
    with database.connect() as connection:
        aggregate_row = connection.execute(
            "SELECT * FROM planning_aggregates WHERE aggregate_id=? AND book_id=? "
            "AND edition_id=?",
            (aggregate_id, book_id, edition_id),
        ).fetchone()
    if aggregate_row is None or str(aggregate_row["status"]) != "ACTIVE":
        raise PlanningError("handoff 的 Planning Aggregate 不可用")
    if str(aggregate_row["bundle_hash"]) != str(handoff["planning_aggregate_hash"]):
        raise PlanningError("handoff 的 Planning Aggregate hash 不一致")
    raw_kernel_context = str(aggregate_row["kernel_context_json"] or "null")
    try:
        kernel_context = KernelPlanningContext.model_validate_json(raw_kernel_context)
    except ValidationError as exc:
        raise PlanningError(f"Planning Aggregate 的 Kernel Context 无效：{exc}") from exc

    handoff_root = Path(str(handoff["task_directory"]))
    handoff_input = handoff_root / "input" if (handoff_root / "input").is_dir() else handoff_root
    handoff_task_path = handoff_input / "task.json"
    if not handoff_task_path.is_file():
        raise PlanningError("handoff 缺少冻结 task.json")
    try:
        handoff_task = json.loads(handoff_task_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PlanningError("handoff 的冻结 task.json 无法解析") from exc
    author_policy = json.loads(str(aggregate_row["author_policy_json"] or "{}"))
    task_id = stable_id("plan", handoff_id, aggregate_id)
    operation = ensure_operation(
        database,
        book_id,
        edition_id,
        task_id,
        "PLAN_NEXT",
        {"handoff_id": handoff_id, "planning_aggregate_id": aggregate_id},
    )
    workspace = edition_workspace(database, book_id, edition_id)
    input_dir = operation.input if operation is not None else workspace / "agent_tasks" / task_id
    output_dir = (
        operation.output
        if operation is not None
        else workspace / "agent_outputs" / task_id
    )
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    frozen_chapter_id = kernel_context.context_chapter_id
    handoff_chapter_id = str(handoff_task.get("context_chapter_id") or "") or None
    if handoff_chapter_id is not None and handoff_chapter_id != frozen_chapter_id:
        raise PlanningError("handoff 章节与 Frozen Kernel Context 不一致")
    chapter_id = frozen_chapter_id
    world_state_path = handoff_input / str(
        handoff_task.get("world_state_context_path") or ""
    )
    kernel_context_path = handoff_input / str(
        handoff_task.get("kernel_context_path") or ""
    )
    boundary_packet_id = str(handoff_task.get("boundary_packet_id") or "")
    boundary_json_path = Path(str(handoff_task.get("boundary_packet_json_path") or ""))
    boundary_markdown_path = Path(
        str(handoff_task.get("boundary_packet_markdown_path") or "")
    )
    if not world_state_path.is_file() or not kernel_context_path.is_file():
        raise PlanningError("handoff 缺少冻结 World State 或 Kernel Context")
    if (
        not boundary_packet_id
        or not boundary_json_path.is_file()
        or not boundary_markdown_path.is_file()
    ):
        raise PlanningError("handoff 缺少冻结 Continuation Boundary artifact")
    try:
        world_state = json.loads(world_state_path.read_text(encoding="utf-8"))
        frozen_kernel_payload = json.loads(kernel_context_path.read_text(encoding="utf-8"))
        boundary_payload = json.loads(boundary_json_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PlanningError("handoff 冻结 artifact 无法解析") from exc
    if not isinstance(world_state, dict) or not isinstance(boundary_payload, dict):
        raise PlanningError("handoff 冻结 World State 或 Boundary 结构无效")
    if _normalize_frozen_semantics(frozen_kernel_payload) != _normalize_frozen_semantics(
        kernel_context.model_dump(mode="json")
    ):
        raise PlanningError("handoff Kernel Context 与 Planning Aggregate 不一致")
    world_chapter = world_state.get("chapter")
    if (
        not isinstance(world_chapter, dict)
        or str(world_chapter.get("chapter_id") or "") != chapter_id
    ):
        raise PlanningError("handoff World State 与 Frozen Kernel Context 章节不一致")
    with database.connect() as connection:
        boundary_row = connection.execute(
            "SELECT packet_sha256, status FROM boundary_packets "
            "WHERE packet_id=? AND book_id=? AND edition_id=?",
            (boundary_packet_id, book_id, edition_id),
        ).fetchone()
    if boundary_row is None or str(boundary_row["status"]) != "READY":
        raise PlanningError("handoff 的冻结 Continuation Boundary 不可用")
    if str(boundary_row["packet_sha256"]) != str(
        handoff_task.get("boundary_packet_sha256") or ""
    ):
        raise PlanningError("handoff 的冻结 Continuation Boundary 不一致")
    boundary_position = boundary_payload.get("current_position", {})
    if int(boundary_position.get("last_canon_chapter") or 0) != (
        kernel_context.context_chapter_ordinal
    ):
        raise PlanningError("Continuation Boundary 与 Frozen Kernel Context 章节不一致")
    active_threads = kernel_context.planning_state.active_threads
    thread_id = (
        str(
            active_threads[0].get("thread_id")
            or active_threads[0].get("id")
            or "handoff-thread"
        )
        if active_threads
        else "handoff-thread"
    )
    recent_reference_card_ids, recent_reference_solution_ids = _recent_reference_memory(
        database, book_id, edition_id
    )
    recent_experience_signatures = _recent_experience_signatures(
        database, book_id, edition_id
    )
    reference_planning_context = _continuation_reference_planning_context(
        book_id=book_id,
        edition_id=edition_id,
        task_id=task_id,
        boundary_payload=boundary_payload,
        thread_id=thread_id,
        kernel_context=kernel_context,
        story_state=world_state,
        recent_card_ids=recent_reference_card_ids,
        recent_solution_ids=recent_reference_solution_ids,
        recent_signatures=recent_experience_signatures,
        output_path=input_dir / "reference_context_snapshot.json",
    )
    reference_prompt = {
        key: reference_planning_context[key]
        for key in (
            "status",
            "snapshot_id",
            "snapshot_hash",
            "selected_card_count",
            "selected_card_ids",
            "selected_card_types",
            "selected_card_knowledge_levels",
            "knowledge_gaps",
            "warnings",
        )
    }
    strategy_payload = reference_planning_context.get("reference_strategy", {})
    reference_prompt["reference_strategy"] = _compact_reference_prompt_value(
        strategy_payload
    )
    reference_prompt["compact_cards"] = _compact_reference_prompt_cards(
        strategy_payload.get("selected_cards", [])
        if isinstance(strategy_payload, Mapping)
        else []
    )
    schema = CandidateCreativeOutput.model_json_schema()
    metadata = {
        "task_id": task_id,
        "task_type": "plan-next",
        "book_id": book_id,
        "edition_id": edition_id,
        "handoff_id": handoff_id,
        "aggregate_id": aggregate_id,
        "aggregate_hash": str(aggregate_row["bundle_hash"]),
        "boundary_packet_id": boundary_packet_id,
        "boundary_path": str(boundary_json_path),
        "author_goal": handoff_task.get("author_goal"),
        "author_control": author_policy.get("author_control", {}),
        "author_control_trace_contract": author_policy.get("trace_contract", {}),
        "effective_book_profile": author_policy.get("effective_book_profile", {}),
        "truth_reveal": author_policy.get("truth_reveal", {}),
        "innovation_control": handoff_task.get("innovation_control"),
        "innovation_source": handoff_task.get("innovation_source"),
        "rhythm_snapshot_id": handoff_task.get("rhythm_snapshot_id"),
        "metric_run_id": handoff_task.get("metric_run_id"),
        "metric_bundle_hash": handoff_task.get("metric_bundle_hash"),
        "handoff_input": str(handoff_input),
        "source_state_context": str(input_dir / "world_state_context.json"),
        "kernel_context": str(input_dir / "kernel_context.json"),
        "reference_planning_context": reference_planning_context,
        "reference_strategy": strategy_payload,
        "recent_experience_signatures": recent_experience_signatures,
        "recent_reference_card_ids": recent_reference_card_ids,
        "recent_reference_solution_ids": recent_reference_solution_ids,
        "reference_context_snapshot": str(input_dir / "reference_context_snapshot.json"),
        "effective_contract_references": [
            item.model_dump(mode="json") for item in kernel_context.contract_references
        ],
        "scheduler_recommendation": (
            None
            if kernel_context.planning_state.scheduler_recommendation is None
            else kernel_context.planning_state.scheduler_recommendation.model_dump(mode="json")
        ),
        "narrative_portfolio_snapshot": boundary_payload.get(
            "narrative_portfolio"
        ),
        "created_at": utc_now(),
    }
    input_text = "\n".join(
        [
            f"# PLAN_ONLY 三候选任务 `{task_id}`",
            "",
            f"正式 handoff：`{handoff_id}`。先读取 handoff input 下全部冻结文件。",
            "目标生成三个 Candidate，至少生成两个有效 Candidate；"
            "不生成正文、Chapter Contract 或 Canon Event。",
            "候选 lens 可覆盖 CONTINUITY_ACTIVE_THREAD、EARNED_OPPORTUNITY、"
            "FORWARD_EXPANSION；结构多样性是诊断与排序信号，不是整批硬失败。",
            "只填写创意决定。author control、画像、评分、证据和门禁由 Python 根据冻结输入编译。",
            "所有事实必须来自 world_state_context.json 或 handoff 冻结证据；未来新增只能"
            "作为 CANDIDATE，并填写 novelty provenance。",
            "不得引用任何未出现在 Author Goal、World State、Resource、Relationship、"
            "Knowledge Boundary、Active Threads 或 Kernel Context 中的人物、物品、能力或专名。",
            "当前 provenance-aware 指标若为 INCOMPLETE，必须保留缺失，不得伪造分数或证据。",
            "",
            "## 本次作者目标",
            "",
            str(handoff_task.get("author_goal") or "（未提供）"),
            "",
            "## 冻结 Author Control",
            "",
            json_dumps(author_policy.get("author_control", {}), indent=2),
            "",
            "## Effective Global Book Profile",
            "",
            json_dumps(author_policy.get("effective_book_profile", {}), indent=2),
            "",
            "## Active Author Truth + 本章揭露计划",
            "",
            json_dumps(author_policy.get("truth_reveal", {}), indent=2),
            "",
            "Hidden Truth 是行为约束，不是揭示许可。只填写实际 reveal_impact；"
            "KEEP_HIDDEN 由 Python 从冻结 Agenda 保留，不得泄露；"
            "HINT 必须有可读线索且不得直接确认。",
            "",
            "## Frozen Kernel Planning Context",
            "",
            json_dumps(_kernel_author_summary(kernel_context), indent=2),
            "",
            "不要填写 scheduler_alignment、评分、硬门或内部 provenance；Lens 与 Chapter Intent"
            "是创意决定，Python 会根据冻结输入计算 Debt / Anticipation 对齐。",
            "Reader/Drive/Progression/Resource/World/Drift 字段只是 declared claims；"
            "Python 将依据 kernel_context.json 重新核验。",
            "",
            "## Frozen Reference Corpus Planning Context",
            "",
            "下列内容只提供 REFERENCE_ONLY 的可迁移机制和对照；不得复制来源人物、事件、"
            "设定或句式，也不得改变 Boundary、Canon、资源、知识边界或 Candidate 选择。",
            "```json",
            json_dumps(reference_prompt, indent=2),
            "```",
            "",
            "## Recent Chapter Experience Signatures（soft guidance）",
            "",
            "重复体验模式只产生软提醒，不构成整批候选硬失败；请在创意摘要中保留变化或复用理由。",
            "```json",
            json_dumps(recent_experience_signatures, indent=2),
            "```",
        ]
    )
    (input_dir / "input.md").write_text(input_text + "\n", encoding="utf-8")
    (input_dir / "schema.json").write_text(
        json_dumps(schema, indent=2) + "\n", encoding="utf-8"
    )
    (input_dir / "task.json").write_text(
        json_dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copyfile(world_state_path, input_dir / "world_state_context.json")
    shutil.copyfile(kernel_context_path, input_dir / "kernel_context.json")
    return {
        "task_id": task_id,
        "handoff_id": handoff_id,
        "input": str(input_dir / "input.md"),
        "schema": str(input_dir / "schema.json"),
        "task": str(input_dir / "task.json"),
        "source_state_context": str(input_dir / "world_state_context.json"),
        "kernel_context": str(input_dir / "kernel_context.json"),
        "expected_output": str(output_dir / "output.json"),
        "aggregate_id": aggregate_id,
        "boundary_packet_id": boundary_packet_id,
        "reference_planning_context": reference_planning_context,
        "effective_book_profile": metadata["effective_book_profile"],
        "truth_reveal": metadata["truth_reveal"],
    }


def _difference_count(left: CandidateProposal, right: CandidateProposal) -> int:
    return sum(
        str(getattr(left, field)).strip().casefold()
        != str(getattr(right, field)).strip().casefold()
        for field in STRUCTURE_FIELDS
    )


def import_candidate_output(
    database: Database,
    book_id: str,
    task_id: str,
    settings: Settings,
    output_path: Path | None = None,
    *,
    edition_id: str | None = None,
    include_runtime_state: bool = True,
) -> dict[str, object]:
    database.initialize()
    workspace = _workspace(database, book_id)
    operation = find_operation(database, book_id, edition_id or "base", task_id)
    task_path = (
        operation.input / "task.json"
        if operation is not None
        else workspace / "agent_tasks" / task_id / "task.json"
    )
    if not task_path.exists() and edition_id is None:
        candidates = list((workspace / "editions").glob(f"*/agent_tasks/{task_id}/task.json"))
        if candidates:
            task_path = candidates[0]
            workspace = task_path.parents[2]
    if not task_path.exists():
        raise PlanningError(f"候选任务不存在：{task_id}")
    metadata = json.loads(task_path.read_text(encoding="utf-8"))
    _load_frozen_reference_inputs(metadata)
    selected_edition = str(edition_id or metadata.get("edition_id", "base"))
    workspace = edition_workspace(database, book_id, selected_edition)
    operation = find_operation(database, book_id, selected_edition, task_id)
    task_path = (
        operation.input / "task.json"
        if operation is not None
        else workspace / "agent_tasks" / task_id / "task.json"
    )
    metadata = json.loads(task_path.read_text(encoding="utf-8"))
    path = output_path or (
        operation.output / "output.json"
        if operation is not None
        else workspace / "agent_outputs" / task_id / "output.json"
    )
    try:
        raw_output = path.read_text(encoding="utf-8")
        try:
            creative_output = _parse_creative_output(raw_output)
        except ValidationError:
            # CandidateProposal remains the internal persisted planning model;
            # this branch accepts already-materialized local artifacts, while
            # newly prepared tasks expose only CandidateCreativeOutput.
            output = CandidateOutput.model_validate_json(raw_output)
            creative_output = None
    except (OSError, ValidationError) as exc:
        raise PlanningError(f"候选 output.json 不符合合同：{exc}") from exc
    if (creative_output.task_id if creative_output is not None else output.task_id) != task_id:
        raise PlanningError("候选 output task_id 不匹配")
    expected_innovation = InnovationControl.model_validate(
        metadata.get("innovation_control", {})
    )
    if (
        creative_output is None
        and output.innovation_control is not None
        and output.innovation_control != expected_innovation
    ):
        raise PlanningError("候选 output 的 innovation_control 与任务冻结值不一致")
    earned_surface = (
        load_earned_surface(database, book_id, edition_id=selected_edition)
        if include_runtime_state
        else None
    )
    portfolio_raw = metadata.get(
        "narrative_portfolio_snapshot", metadata.get("narrative_portfolio")
    )
    if portfolio_raw:
        try:
            narrative_portfolio = NarrativePortfolioSnapshot.model_validate(portfolio_raw)
        except ValidationError as exc:
            raise PlanningError(f"候选任务的 Narrative Portfolio Snapshot 无效：{exc}") from exc
    else:
        narrative_portfolio = build_narrative_portfolio_snapshot(
            active_threads=[],
            promises={},
            current_chapter=0,
            snapshot_id=f"legacy-portfolio-{task_id}",
        )
    boundary_path = metadata.get("boundary_path")
    boundary_payload = (
        json.loads(Path(str(boundary_path)).read_text(encoding="utf-8"))
        if boundary_path and Path(str(boundary_path)).is_file()
        else {}
    )
    recent_experience_signatures = _recent_experience_signatures(
        database, book_id, selected_edition
    )
    aggregate_id = str(metadata.get("aggregate_id") or "")
    frozen_author_control: dict[str, Any] = {}
    frozen_profile: dict[str, Any] = {}
    frozen_truth_reveal: dict[str, Any] = {}
    frozen_kernel_context: KernelPlanningContext | None = None
    if aggregate_id:
        with database.connect() as connection:
            aggregate_row = connection.execute(
                "SELECT status, bundle_hash, author_policy_json, kernel_context_json "
                "FROM planning_aggregates "
                "WHERE aggregate_id=? AND book_id=? AND edition_id=?",
                (aggregate_id, book_id, selected_edition),
            ).fetchone()
        if aggregate_row is None:
            raise PlanningError("Planning Aggregate 不存在")
        if str(aggregate_row["status"]) != "ACTIVE":
            raise PlanningError("Planning Aggregate 已失效，必须重建候选任务")
        expected_aggregate_hash = str(
            metadata.get("aggregate_hash") or metadata.get("bundle_hash") or ""
        )
        if expected_aggregate_hash and str(aggregate_row["bundle_hash"]) != expected_aggregate_hash:
            raise PlanningError("Planning Aggregate hash 与候选任务冻结值不一致")
        if aggregate_row is not None:
            try:
                aggregate_policy = json.loads(str(aggregate_row["author_policy_json"] or "{}"))
            except (TypeError, ValueError) as exc:
                raise PlanningError("Planning Aggregate 的作者控制冻结值无效") from exc
            if isinstance(aggregate_policy, dict):
                frozen_author_control = aggregate_policy.get("author_control", {})
                frozen_profile = aggregate_policy.get("effective_book_profile", {})
                frozen_truth_reveal = aggregate_policy.get("truth_reveal", {})
            raw_kernel_context = str(aggregate_row["kernel_context_json"] or "null")
            if raw_kernel_context != "null":
                try:
                    frozen_kernel_context = KernelPlanningContext.model_validate_json(
                        raw_kernel_context
                    )
                except ValidationError as exc:
                    raise PlanningError(
                        f"Planning Aggregate 的 Kernel Context 无效：{exc}"
                    ) from exc
                kernel_path = metadata.get("kernel_context")
                if kernel_path and Path(str(kernel_path)).is_file():
                    task_kernel = KernelPlanningContext.model_validate_json(
                        Path(str(kernel_path)).read_text(encoding="utf-8")
                    )
                    if _normalize_frozen_semantics(
                        task_kernel.model_dump(mode="json")
                    ) != _normalize_frozen_semantics(
                        frozen_kernel_context.model_dump(mode="json")
                    ):
                        raise PlanningError(
                            "候选任务的 Kernel Context 与 Planning Aggregate 不一致"
                        )
        task_truth_reveal = metadata.get("truth_reveal", {})
        if _normalize_frozen_semantics(task_truth_reveal) != _normalize_frozen_semantics(
            frozen_truth_reveal
        ):
            raise PlanningError("候选任务的 Truth/Reveal 冻结快照与 Aggregate 不一致")
    if not frozen_author_control:
        frozen_author_control = dict(metadata.get("author_control") or {})
    if not frozen_profile:
        frozen_profile = dict(metadata.get("effective_book_profile") or {})
    if not frozen_truth_reveal:
        frozen_truth_reveal = dict(metadata.get("truth_reveal") or {})
    if creative_output is not None:
        output = CandidateOutput(
            task_id=creative_output.task_id,
            candidates=[
                _compile_creative_candidate(
                    item,
                    metadata=metadata,
                    frozen_truth_reveal=frozen_truth_reveal,
                )
                for item in creative_output.candidates
            ],
            notes=creative_output.notes,
        )
    portfolio = diagnose_candidate_portfolio(
        output.candidates,
        earned_surface=earned_surface,
    )
    portfolio_path = path.parent / "portfolio_diagnostics.json"
    portfolio_path.write_text(
        json_dumps(portfolio.model_dump(mode="json"), indent=2) + "\n",
        encoding="utf-8",
    )
    differences: dict[str, list[int]] = {candidate.local_id: [] for candidate in output.candidates}
    diversity_warnings: list[str] = []
    for left, right in combinations(output.candidates, 2):
        count = _difference_count(left, right)
        differences[left.local_id].append(count)
        differences[right.local_id].append(count)
        if count < 3:
            diversity_warnings.append(
                f"候选 {left.local_id}/{right.local_id} 只有 {count} 个结构维度不同"
            )
    evaluated: list[dict[str, Any]] = []
    for candidate in output.candidates:
        _validate_author_control_trace(candidate, frozen_author_control)
        profile_failures = _profile_constraint_failures(candidate, frozen_profile)
        truth_reveal_failures = _truth_reveal_failures(
            candidate, frozen_truth_reveal
        )
        kernel_compilation = (
            KernelEvidenceCompiler().compile(
                frozen_kernel_context,
                candidate,
                settings.metrics,
            )
            if frozen_kernel_context is not None
            and frozen_kernel_context.contract_references
            else None
        )
        kernel_gate = (
            None
            if kernel_compilation is None
            else kernel_compilation.hard_gate_compilation
        )
        gate_input = candidate.gate_input.model_copy(
            update={
                "canon_conflicts": [
                    *candidate.gate_input.canon_conflicts,
                    *([] if kernel_gate is None else kernel_gate.canon_conflicts),
                ],
                "timeline_conflicts": [
                    *candidate.gate_input.timeline_conflicts,
                    *([] if kernel_gate is None else kernel_gate.timeline_conflicts),
                ],
                "knowledge_violations": [
                    *candidate.gate_input.knowledge_violations,
                    *([] if kernel_gate is None else kernel_gate.knowledge_violations),
                ],
                "missing_causal_sources": [
                    *candidate.gate_input.missing_causal_sources,
                    *([] if kernel_gate is None else kernel_gate.missing_causal_sources),
                ],
                "payoff_cooldown_violations": [
                    *candidate.gate_input.payoff_cooldown_violations,
                    *(
                        []
                        if kernel_gate is None
                        else kernel_gate.payoff_cooldown_violations
                    ),
                ],
                "capability_violations": [
                    *candidate.gate_input.capability_violations,
                    *([] if kernel_gate is None else kernel_gate.capability_violations),
                ],
                "author_constraint_violations": [
                    *candidate.gate_input.author_constraint_violations,
                    *profile_failures,
                    *truth_reveal_failures,
                    *(
                        []
                        if kernel_gate is None
                        else kernel_gate.author_constraint_violations
                    ),
                ]
            }
        )
        gate = evaluate_hard_gates(gate_input, settings.metrics)
        if kernel_compilation is not None:
            gate = gate.model_copy(
                update={
                    "kernel_warnings": kernel_compilation.warnings,
                    "kernel_evidence": kernel_compilation.model_dump(mode="json"),
                }
            )
        diversity = (
            sum(differences[candidate.local_id])
            / (len(differences[candidate.local_id]) * len(STRUCTURE_FIELDS))
            * 100
        )
        inputs = candidate.score_inputs.model_dump(exclude_none=True)
        inputs["structural_diversity"] = diversity
        score_evidence = dict(candidate.score_evidence)
        if kernel_compilation is not None:
            override_bundle = kernel_compilation.soft_metric_compilation.get(
                "candidate_score_overrides", {}
            )
            overrides = override_bundle.get("values", {})
            sources = override_bundle.get("components", {})
            if isinstance(overrides, dict):
                inputs.update(
                    {
                        str(name): float(value)
                        for name, value in overrides.items()
                        if name in inputs
                    }
                )
            if isinstance(sources, dict):
                for name, source in sources.items():
                    if name not in inputs or not isinstance(source, dict):
                        continue
                    evidence_values = source.get("evidence", [])
                    score_evidence[str(name)] = [
                        str(item) for item in evidence_values
                    ] or [str(source.get("source") or "KERNEL_VERIFIED_EVIDENCE")]
        elif candidate.progress_preview is not None:
            progress_result = progress_metric(
                candidate.progress_preview.values,
                settings.metrics["progress"],
            )
            inputs["progress_gain"] = progress_result.score
            score_evidence["progress_gain"] = [
                evidence
                for component in candidate.progress_preview.components
                for evidence in component.evidence
            ]
        required_evidence = set(inputs) - {"structural_diversity"}
        missing_evidence = sorted(
            key for key in required_evidence if not score_evidence.get(key)
        )
        score_warnings = (
            [f"缺少评分证据，相关分量保留为 UNKNOWN：{missing_evidence}"]
            if missing_evidence
            else []
        )
        score_evidence["structural_diversity"] = [
            f"与另外两案的结构差异维度数：{differences[candidate.local_id]}"
        ]
        base_score = (
            candidate_score(inputs, settings.metrics["candidate_score"])
            if gate.passed
            else 0
        )
        verified_candidate = candidate
        if kernel_compilation is not None:
            verified_payload = kernel_compilation.verified
            verified_reader_ids = {
                str(item.get("promise_id"))
                for item in kernel_compilation.verified_reader_promise_alignment
                if item.get("verification_status") == "VERIFIED"
            }
            verified_impact = kernel_compilation.verified_progression_impact
            verified_candidate = candidate.model_copy(
                update={
                    "reader_promise_alignment": [
                        item
                        for item in candidate.reader_promise_alignment
                        if item.promise_id in verified_reader_ids
                    ],
                    "genre_alignment": (
                        ["VERIFIED_STRUCTURAL_CAUSALITY"]
                        if verified_payload.get("genre_drift", {}).get("status")
                        == "CLEAR"
                        else []
                    ),
                    "narrative_drive_alignment": candidate.narrative_drive_alignment.model_validate(
                        kernel_compilation.verified_drive_alignment
                    ),
                    "progression_impact": candidate.progression_impact.model_copy(
                        update={
                            "axis_advanced": verified_impact.get("axis_advanced", []),
                            "progression_delta_type": verified_impact.get(
                                "progression_delta_type", []
                            ),
                            "stage_change": (
                                candidate.progression_impact.stage_change
                                if verified_impact.get("stage_change")
                                else None
                            ),
                            "resource_change": [
                                str(item.get("claim"))
                                for item in verified_impact.get("resource_changes", [])
                            ],
                            "ability_unlock": [
                                str(item.get("claim"))
                                for item in verified_impact.get("ability_unlocks", [])
                            ],
                            "growth_cost": verified_impact.get("growth_costs", []),
                        }
                    ),
                    "payoff_channel_impact": kernel_compilation.soft_metric_compilation.get(
                        "payoff", {}
                    ).get("evidence", []),
                    "world_expansion_impact": kernel_compilation.verified_world_expansion_impact,
                    "resource_opportunity_impact": [
                        str(item.get("claim"))
                        for item in kernel_compilation.verified_resource_impact
                        if str(item.get("status", "")).startswith("VERIFIED")
                    ],
                    "anticipation_impact": kernel_compilation.verified_anticipation_impact,
                    "genre_drift_diagnostic": verified_payload.get("genre_drift", {}),
                    "genre_evolution_diagnostic": verified_payload.get(
                        "genre_evolution", {}
                    ),
                    "narrative_drive_drift_diagnostic": verified_payload.get(
                        "drive_drift", {}
                    ),
                }
            )
        reward = calculate_candidate_innovation_reward(
            verified_candidate,
            expected_innovation,
            base_candidate_score=base_score,
            portfolio=narrative_portfolio,
            recent_structures=boundary_payload.get("recent_structures", []),
            eligible=gate.passed,
            ineligibility_reasons=gate.hard_failures,
        )
        experience_repetition_penalty = (
            _candidate_experience_overlap(candidate, recent_experience_signatures)
            if gate.passed
            else 0
        )
        if experience_repetition_penalty:
            score_warnings.append(
                "近期已实现体验签名相似；仅施加软避让扣分，不构成硬门。"
            )
        final_selection_score = (
            reward.final_selection_score - experience_repetition_penalty
        )
        evaluated.append(
            {
                "candidate": candidate,
                "candidate_id": stable_id("candidate", task_id, candidate.local_id),
                "gate": gate,
                "score": base_score,
                "base_score": base_score,
                "final_selection_score": final_selection_score,
                "experience_repetition_penalty": experience_repetition_penalty,
                "reward": reward,
                "inputs": inputs,
                "score_evidence": score_evidence,
                "score_warnings": score_warnings,
                "diversity": diversity,
                "kernel_compilation": kernel_compilation,
            }
        )
    passed = sorted(
        (item for item in evaluated if item["gate"].passed),
        key=lambda item: (-float(item["final_selection_score"]), str(item["candidate_id"])),
    )
    if len(passed) < 2:
        raise PlanningError(
            f"有效候选少于两个：{len(passed)}；请重试候选生成"
        )
    selected_id = str(passed[0]["candidate_id"])
    best_score = float(passed[0]["final_selection_score"])
    tie_delta = float(settings.metrics["candidate_score"]["tie_delta"])
    same_choice_band = [
        str(item["candidate_id"])
        for item in passed
        if best_score - float(item["final_selection_score"]) < tie_delta
    ]
    ranking = {str(item["candidate_id"]): index for index, item in enumerate(passed, 1)}
    with database.connect() as connection:
        aggregate = None
        if aggregate_id:
            aggregate = connection.execute(
                "SELECT * FROM planning_aggregates WHERE aggregate_id=? "
                "AND book_id=? AND edition_id=?",
                (aggregate_id, book_id, selected_edition),
            ).fetchone()
        run_ids = [] if aggregate is None else json.loads(str(aggregate["metric_run_ids_json"]))
        v2_run = None
        if run_ids:
            placeholders = ",".join("?" for _ in run_ids)
            v2_run = connection.execute(
                f"SELECT * FROM metric_runs WHERE run_id IN ({placeholders}) "
                "ORDER BY created_at DESC LIMIT 1",
                tuple(run_ids),
            ).fetchone()
        rhythm_snapshot = connection.execute(
            "SELECT snapshot_id FROM rhythm_diagnostic_snapshots WHERE book_id=? AND edition_id=? "
            "ORDER BY as_of_chapter DESC, created_at DESC LIMIT 1",
            (book_id, selected_edition),
        ).fetchone()
    with database.connect() as connection:
        for item in evaluated:
            candidate = item["candidate"]
            assert isinstance(candidate, CandidateProposal)
            candidate_id = str(item["candidate_id"])
            gate = item["gate"]
            selection = (
                "REJECTED"
                if not gate.passed
                else "SELECTED"
                if candidate_id == selected_id
                else "NOT_SELECTED"
            )
            reason = (
                "; ".join(gate.hard_failures)
                if not gate.passed
                else (
                    "综合评分最高且通过硬门；同一可选区间仍由作者审美决定"
                    if len(same_choice_band) > 1
                    else "综合评分最高且通过硬门"
                )
                if candidate_id == selected_id
                else (
                    f"与最高分差小于 {tie_delta:g}，属于同一可选区间；默认未选但保留给作者"
                    if candidate_id in same_choice_band
                    else f"通过硬门但排名 {ranking[candidate_id]}，保留为备选"
                )
            )
            score_json = {
                "score": item["score"],
                "base_candidate_score": item["base_score"],
                "final_selection_score": item["final_selection_score"],
                "experience_repetition_penalty": item[
                    "experience_repetition_penalty"
                ],
                "innovation_reward_breakdown": item["reward"].model_dump(mode="json"),
                "inputs": item["inputs"],
                "evidence": item["score_evidence"],
                "warnings": item["score_warnings"],
                "structural_difference_counts": differences[candidate.local_id],
                "diversity_warnings": diversity_warnings,
                "score_warnings": item["score_warnings"],
                "reason": reason,
                "portfolio_diagnostics": portfolio.model_dump(mode="json"),
                "narrative_portfolio_snapshot": narrative_portfolio.model_dump(mode="json"),
                "author_control_trace": candidate.author_control_trace.model_dump(mode="json"),
                "kernel_evidence_compilation": (
                    None
                    if item["kernel_compilation"] is None
                    else item["kernel_compilation"].model_dump(mode="json")
                ),
            }
            connection.execute(
                """
                INSERT OR REPLACE INTO candidate_plans(
                candidate_id, book_id, task_id, rank, primary_thread_id,
                    primary_function, secondary_functions_json, plan_json,
                    score_json, gate_report_json, selection_status, status,
                    created_at, version, edition_id, metric_run_id, metric_bundle_hash,
                    rhythm_snapshot_id, registry_hash, config_hash, aggregate_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CANDIDATE', ?, 1, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate_id,
                    book_id,
                    task_id,
                    ranking.get(candidate_id),
                    candidate.primary_thread_id,
                    candidate.primary_function.value,
                    json_dumps([item.value for item in candidate.secondary_functions]),
                    json_dumps(candidate.model_dump(mode="json")),
                    json_dumps(score_json),
                    json_dumps(gate.model_dump(mode="json")),
                    selection,
                    utc_now(),
                    selected_edition,
                    None if v2_run is None else str(v2_run["run_id"]),
                    None if v2_run is None else str(v2_run["input_bundle_hash"]),
                    None if rhythm_snapshot is None else str(rhythm_snapshot["snapshot_id"]),
                    None if v2_run is None else str(v2_run["registry_hash"]),
                    None if v2_run is None else str(v2_run["config_hash"]),
                    aggregate_id or None,
                ),
            )
    return {
        "task_id": task_id,
        "selected_candidate_id": selected_id,
        "same_choice_band": same_choice_band,
        "candidates": [
            {
                "candidate_id": item["candidate_id"],
                "local_id": item["candidate"].local_id,
                "title": item["candidate"].title,
                "score": item["score"],
                "base_score": item["base_score"],
                "final_selection_score": item["final_selection_score"],
                "experience_repetition_penalty": item[
                    "experience_repetition_penalty"
                ],
                "innovation_reward_breakdown": item["reward"].model_dump(mode="json"),
                "passed": item["gate"].passed,
                "selection_status": "SELECTED"
                if item["candidate_id"] == selected_id
                else "REJECTED"
                if not item["gate"].passed
                else "NOT_SELECTED",
                "hard_failures": item["gate"].hard_failures,
                "structural_difference_counts": differences[item["candidate"].local_id],
                "author_control_trace": item["candidate"].author_control_trace.model_dump(
                    mode="json"
                ),
                "author_control_hit": bool(
                    item["candidate"].author_control_trace.author_task_hits
                    or item["candidate"].author_control_trace.author_intent_hits
                ),
                "profile_alignment": item[
                    "candidate"
                ].profile_alignment.model_dump(mode="json"),
            }
            for item in evaluated
        ],
        "boundary_packet_id": metadata.get("boundary_packet_id"),
        "aggregate_id": aggregate_id or None,
        "portfolio_diagnostics": portfolio.model_dump(mode="json"),
        "portfolio_diagnostics_path": str(portfolio_path),
        "narrative_portfolio_snapshot": narrative_portfolio.model_dump(mode="json"),
        "diversity_warnings": diversity_warnings,
    }
