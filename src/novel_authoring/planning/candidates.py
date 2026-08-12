from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from novel_authoring.author_control.projections import build_story_game_state
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
from novel_authoring.planning.models import CandidateOutput, CandidateProposal, ThreadPriority
from novel_authoring.planning.rewards import calculate_candidate_innovation_reward
from novel_authoring.progression.context import KernelPlanningContext
from novel_authoring.progression.evidence import KernelEvidenceCompiler
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
    missing = set(active) - set(alignments)
    if missing:
        raise PlanningError(
            f"候选 {candidate.local_id} 未检查全部 Active Author Truth：{sorted(missing)}"
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
    undeclared = keep_hidden - set(candidate.reveal_impact.kept_hidden)
    if undeclared:
        failures.append(f"候选未显式确认继续隐藏：{sorted(undeclared)}")
    return failures


def _current_ordinal(connection: Any, book_id: str, edition_id: str = "base") -> int:
    from novel_authoring.edition import edition_chapters

    chapters = edition_chapters(connection, book_id, edition_id)
    return max((int(row["ordinal"]) for row in chapters), default=0)


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
        raise PlanningError("缺少六项最新指标；请先运行 novel diagnose")
    schema = CandidateOutput.model_json_schema()
    schema_json = json_dumps(schema, indent=2)
    seed = json_dumps(
        {
            "book_id": book_id,
            "boundary": boundary["packet_id"],
            "planning_aggregate": aggregate,
            "threads": [item.model_dump(mode="json") for item in threads],
            "metrics": [dict(row) for row in metric_rows],
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
    input_text = "\n".join(
        [
            f"# 下一章候选任务 `{task_id}`",
            "",
            f"Boundary Packet: `{boundary['markdown_path']}`",
            "",
            "必须提交恰好三个结构真正不同的候选；不得只换怪物、资源、地点或社会反馈名词。",
            "候选应分别考虑 CONTINUITY_ACTIVE_THREAD、EARNED_OPPORTUNITY、FORWARD_EXPANSION；"
            "这是三种推理 lens，不是固定配额。",
            "当前 InnovationControl 的 creative-distance guidance："
            f"{selected_innovation.creative_distance_guidance}",
            "当前 soft lens tendency："
            f"{selected_innovation.lens_tendency_guidance}；这不是配额，也不是 Score Bonus。",
            "所有 FORWARD_NOVELTY 必须填写 introduction_event、causal_source、"
            "new_state_if_committed、conflicts_checked；不得把未来状态倒写成既有事实。",
            "每个候选先填写硬门证据，再填写评分输入与来源；Python 将重新计算门禁、结构差异和总分。",
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
            "## 作者控制输入（必须显式检查）",
            "",
            json_dumps(
                aggregate.get("author_policy", {}).get("author_control", {}),
                indent=2,
            ),
            "",
            "候选输出中请说明命中了哪些作者任务/意图（task_id/intent_id），"
            "没有命中时也要说明原因；这只是规划输入，不会自动改变正史。",
            "每个候选必须填写 author_control_trace：author_task_hits、author_intent_hits、"
            "author_tasks_advanced、author_intents_advanced、author_goals_not_used 和"
            "unused_reasons。只能引用上方冻结的 ID；硬门永远优先于作者目标命中。",
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
            "每个候选必须填写 profile_alignment：九个 dimension 各一条，并逐项填写"
            " MUST/MUST_NOT constraint_checks。任何 passed=false 都是硬门失败，"
            "Innovation Reward 不得抵消。",
            "",
            "## Author Truth + Chapter Reveal Agenda（行为约束不等于揭示许可）",
            "",
            json_dumps(
                aggregate.get("author_policy", {}).get("truth_reveal", {}),
                indent=2,
            ),
            "",
            "每个候选必须填写 truth_alignment 与 reveal_impact。Active Author Truth 可以"
            "改变人物行为；KEEP_HIDDEN 不得出现在旁白、对话或答案式解释中。"
            "SHOULD_HINT 必须给出可读 clue，但不得确认身份；MUST_REVEAL 才允许按计划深度兑现。",
            "",
            "## Frozen Kernel Planning Context（机器冻结输入）",
            "",
            (
                "当前为 Legacy 规划：没有可冻结的 Kernel Context，沿用原有流程。"
                if kernel_context is None
                else json_dumps(_kernel_author_summary(kernel_context), indent=2)
            ),
            "",
            "每案必须填写 scheduler_alignment。Scheduler 是建议；若选择其他 Primary Intent，"
            "必须给出 deviation_reason。Reader/Drive/Progression/Resource/World 声明将由 Python"
            "依据 kernel_context.json 重新核验，不能靠自报获得评分。",
            "",
            "## 三条优先线程",
            "",
            "```json",
            json_dumps([item.model_dump(mode="json") for item in threads], indent=2),
            "```",
            "",
            "## 最新指标",
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
        "bundle_hash": aggregate["bundle_hash"],
        "rhythm_snapshot_id": aggregate.get("rhythm_snapshot_id"),
        "registry_hash": aggregate["registry_hash"],
        "config_hash": aggregate["config_hash"],
        "thread_priorities": [item.model_dump(mode="json") for item in threads],
        "schema_sha256": sha256_bytes(schema_json.encode()),
        "created_at": utc_now(),
        "runtime_context": runtime_context.model_dump(mode="json"),
        "include_runtime_state": include_runtime_state,
        "innovation_control": selected_innovation.model_dump(mode="json"),
        "innovation_source": selected_source,
        "innovation_recommendation": boundary_payload.get("innovation_diagnostics", {}),
        "narrative_portfolio_snapshot": narrative_portfolio.model_dump(mode="json"),
        "kernel_context": str(task_dir / "kernel_context.json"),
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
    handoff_task = json.loads((handoff_input / "task.json").read_text(encoding="utf-8"))
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
    world_state = build_story_game_state(
        database,
        book_id,
        edition_id,
        chapter_id=chapter_id,
    )
    schema = CandidateOutput.model_json_schema()
    metadata = {
        "task_id": task_id,
        "task_type": "plan-next",
        "book_id": book_id,
        "edition_id": edition_id,
        "handoff_id": handoff_id,
        "aggregate_id": aggregate_id,
        "aggregate_hash": str(aggregate_row["bundle_hash"]),
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
        "effective_contract_references": [
            item.model_dump(mode="json") for item in kernel_context.contract_references
        ],
        "scheduler_recommendation": (
            None
            if kernel_context.planning_state.scheduler_recommendation is None
            else kernel_context.planning_state.scheduler_recommendation.model_dump(mode="json")
        ),
        "created_at": utc_now(),
    }
    input_text = "\n".join(
        [
            f"# PLAN_ONLY 三候选任务 `{task_id}`",
            "",
            f"正式 handoff：`{handoff_id}`。先读取 handoff input 下全部冻结文件。",
            "只生成恰好三个 Candidate，不生成正文、Chapter Contract 或 Canon Event。",
            "三个 lens 必须分别为 CONTINUITY_ACTIVE_THREAD、EARNED_OPPORTUNITY、"
            "FORWARD_EXPANSION，且任意两案至少三个结构维度不同。",
            "每案必须填写 author_control_trace；命中本次 WORKFLOW_GOAL intent，并说明"
            "冻结资源、关系、知识边界与真实代价如何进入因果链。",
            "每案必须逐一填写九维 profile_alignment，并对全部 MUST/MUST_NOT edit_id"
            " 给出 passed 与证据。硬约束失败不得靠创新分抵消。",
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
            "Hidden Truth 是行为约束，不是揭示许可。每案填写 truth_alignment 与"
            " reveal_impact；KEEP_HIDDEN 不得泄露，HINT 必须有可读线索且不得直接确认。",
            "",
            "## Frozen Kernel Planning Context",
            "",
            json_dumps(_kernel_author_summary(kernel_context), indent=2),
            "",
            "每案必须填写 scheduler_alignment：说明是否采纳推荐 Primary Intent、服务哪些"
            " Debt / Anticipation，以及偏离理由。Lens 与 Chapter Intent 是两个独立维度。",
            "Reader/Drive/Progression/Resource/World/Drift 字段只是 declared claims；"
            "Python 将依据 kernel_context.json 重新核验。",
        ]
    )
    (input_dir / "input.md").write_text(input_text + "\n", encoding="utf-8")
    (input_dir / "schema.json").write_text(
        json_dumps(schema, indent=2) + "\n", encoding="utf-8"
    )
    (input_dir / "task.json").write_text(
        json_dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    (input_dir / "world_state_context.json").write_text(
        json_dumps(world_state, indent=2) + "\n", encoding="utf-8"
    )
    (input_dir / "kernel_context.json").write_text(
        json_dumps(kernel_context.model_dump(mode="json"), indent=2) + "\n",
        encoding="utf-8",
    )
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
        output = CandidateOutput.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError) as exc:
        raise PlanningError(f"候选 output.json 不符合合同：{exc}") from exc
    if output.task_id != task_id:
        raise PlanningError("候选 output task_id 不匹配")
    expected_innovation = InnovationControl.model_validate(
        metadata.get("innovation_control", {})
    )
    if output.innovation_control is not None and output.innovation_control != expected_innovation:
        raise PlanningError("候选 output 的 innovation_control 与任务冻结值不一致")
    earned_surface = (
        load_earned_surface(database, book_id, edition_id=selected_edition)
        if include_runtime_state
        else None
    )
    portfolio = diagnose_candidate_portfolio(
        output.candidates,
        earned_surface=earned_surface,
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
                    if task_kernel != frozen_kernel_context:
                        raise PlanningError(
                            "候选任务的 Kernel Context 与 Planning Aggregate 不一致"
                        )
        task_truth_reveal = metadata.get("truth_reveal", {})
        if task_truth_reveal != frozen_truth_reveal:
            raise PlanningError("候选任务的 Truth/Reveal 冻结快照与 Aggregate 不一致")
    portfolio_path = path.parent / "portfolio_diagnostics.json"
    portfolio_path.write_text(
        json_dumps(portfolio.model_dump(mode="json"), indent=2) + "\n",
        encoding="utf-8",
    )
    differences: dict[str, list[int]] = {candidate.local_id: [] for candidate in output.candidates}
    for left, right in combinations(output.candidates, 2):
        count = _difference_count(left, right)
        differences[left.local_id].append(count)
        differences[right.local_id].append(count)
        if count < 3:
            raise PlanningError(
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
            KernelEvidenceCompiler().compile(frozen_kernel_context, candidate)
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
        inputs = candidate.score_inputs.model_dump()
        inputs["structural_diversity"] = diversity
        score_evidence = dict(candidate.score_evidence)
        if candidate.progress_preview is not None:
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
        if missing_evidence:
            raise PlanningError(f"候选 {candidate.local_id} 缺少评分证据：{missing_evidence}")
        score_evidence["structural_diversity"] = [
            f"与另外两案的结构差异维度数：{differences[candidate.local_id]}"
        ]
        base_score = (
            candidate_score(inputs, settings.metrics["candidate_score"])
            if gate.passed
            else 0
        )
        reward = calculate_candidate_innovation_reward(
            candidate,
            expected_innovation,
            base_candidate_score=base_score,
            portfolio=narrative_portfolio,
            recent_structures=boundary_payload.get("recent_structures", []),
            eligible=gate.passed,
            ineligibility_reasons=gate.hard_failures,
        )
        evaluated.append(
            {
                "candidate": candidate,
                "candidate_id": stable_id("candidate", task_id, candidate.local_id),
                "gate": gate,
                "score": base_score,
                "base_score": base_score,
                "final_selection_score": reward.final_selection_score,
                "reward": reward,
                "inputs": inputs,
                "score_evidence": score_evidence,
                "diversity": diversity,
                "kernel_compilation": kernel_compilation,
            }
        )
    passed = sorted(
        (item for item in evaluated if item["gate"].passed),
        key=lambda item: (-float(item["final_selection_score"]), str(item["candidate_id"])),
    )
    if not passed:
        raise PlanningError("三个候选全部未通过硬门")
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
                "final_selection_score": item["reward"].final_selection_score,
                "innovation_reward_breakdown": item["reward"].model_dump(mode="json"),
                "inputs": item["inputs"],
                "evidence": item["score_evidence"],
                "structural_difference_counts": differences[candidate.local_id],
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
                "final_selection_score": item["reward"].final_selection_score,
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
    }
