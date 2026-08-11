"""Transactional application of an author-confirmed original-novel foundation."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from novel_authoring.author_control.book_profile import PROFILE_DIMENSIONS
from novel_authoring.author_control.truth import TruthType
from novel_authoring.db.database import Database
from novel_authoring.original.models import (
    GenesisApplyPlan,
    OriginalBookRequest,
    OriginalBootstrapProposal,
    OriginalFoundationConfirmation,
    SettingStrength,
)
from novel_authoring.planning.models import CandidateLens, CandidateProposal
from novel_authoring.utils import json_dumps, utc_now


class GenesisApplyError(RuntimeError):
    pass


def _candidate_plan(
    source: Any,
    *,
    thread_id: str,
    world_rules: list[str],
    request: OriginalBookRequest,
    lens: CandidateLens,
) -> dict[str, Any]:
    score_names = (
        "thread_need_fit",
        "pressure_curve_fit",
        "debt_utility",
        "progress_gain",
        "payoff_or_setup_utility",
        "agency_gain",
        "risk_fit",
        "structural_diversity",
        "style_fit",
        "repetition_fatigue",
        "future_damage",
    )
    plan = CandidateProposal.model_validate(
        {
            "local_id": source.candidate_id,
            "title": source.title,
            "summary": source.chapter_goal,
            "primary_thread_id": thread_id,
            "primary_function": source.primary_function.value,
            "secondary_functions": [],
            "reader_question": source.hook,
            "event_source": source.opening_situation,
            "solution_method": source.protagonist_action,
            "protagonist_strategy": source.central_choice,
            "risk_form": source.conflict,
            "opportunity_cost": source.cost,
            "emotional_outcome": source.ending_turn,
            "social_feedback": source.distinctiveness,
            "scene_topology": source.opening_situation,
            "ending_state": source.ending_turn,
            "state_changes": [source.irreversible_change, source.ending_turn],
            "causal_sources": ["作者确认的故事基础方案与创作起点"],
            "required_irreversible_change": source.irreversible_change,
            "required_cost": source.cost,
            "must_not_resolve": ["不得在首章锁死长期路线或结局"],
            "canon_constraints": world_rules,
            "knowledge_constraints": ["不得让角色无依据知晓幕后设定"],
            "forbidden_repetitions": request.forbidden,
            "style_constraints": {
                "tone_style": request.tone_style or "遵循已确认画像",
                "pov": request.pov or "由章节合同冻结",
            },
            "commit_updates": [
                f"thread_status:{thread_id}",
                "character_state:protagonist",
            ],
            "pressure_before": 0,
            "pressure_target_after": 35,
            "score_inputs": dict.fromkeys(score_names, 0),
            "score_evidence": {name: [] for name in score_names},
            "gate_input": {"character_fit_inputs": {}, "style_fit_inputs": {}},
            "lens": lens.value,
            "wildcard": lens is CandidateLens.FORWARD_EXPANSION,
        }
    )
    return plan.model_dump(mode="json")


def build_genesis_apply_plan(
    *,
    proposal_version_id: str,
    proposal: OriginalBootstrapProposal,
    confirmation: OriginalFoundationConfirmation,
    request: OriginalBookRequest,
) -> GenesisApplyPlan:
    if not confirmation.confirmed:
        raise GenesisApplyError("请在影响摘要中确认后再开始写作")
    if confirmation.selected_title not in proposal.title_candidates:
        raise GenesisApplyError("选择的书名不属于当前方案")
    foundation = next(
        (
            item
            for item in proposal.foundation_candidates
            if item.candidate_id == confirmation.selected_foundation_id
        ),
        None,
    )
    route = next(
        (item for item in proposal.routes if item.route_id == confirmation.selected_route_id),
        None,
    )
    if foundation is None or route is None:
        raise GenesisApplyError("选择的故事基础或路线不属于当前方案")
    selected_title = confirmation.title_override.strip() or confirmation.selected_title
    protagonist = confirmation.protagonist_override.strip() or proposal.protagonist
    protagonist_goal = confirmation.protagonist_goal_override.strip() or proposal.protagonist_goal
    main_conflict = confirmation.main_conflict_override.strip() or foundation.main_conflict
    protagonist_cost = confirmation.protagonist_cost_override.strip() or proposal.protagonist_cost
    protagonist_growth = (
        confirmation.protagonist_growth_override.strip() or proposal.protagonist_growth
    )
    rolling = {
        "short": confirmation.rolling_short_override or proposal.rolling_planning.short,
        "mid": confirmation.rolling_mid_override or proposal.rolling_planning.mid,
        "long": confirmation.rolling_long_override or proposal.rolling_planning.long,
    }
    prefix = f"{proposal_version_id}-{foundation.candidate_id}"
    settings = []
    known_statements = set()
    for setting in proposal.foundation_settings:
        strength = confirmation.setting_strength_overrides.get(setting.setting_id, setting.strength)
        settings.append(
            {
                **setting.model_dump(mode="json"),
                "strength": strength.value,
            }
        )
        known_statements.add(setting.statement)
    for index, rule in enumerate(confirmation.world_rules, start=1):
        if rule not in known_statements:
            settings.append(
                {
                    "setting_id": f"author-world-rule-{index}",
                    "category": "WORLD_RULE",
                    "statement": rule,
                    "strength": SettingStrength.CORE.value,
                }
            )
    truth_specs: list[tuple[TruthType, str, str]] = [
        (TruthType.CHARACTER_IDENTITY, "主角", protagonist),
        (TruthType.CHARACTER_GOAL, "主角目标", protagonist_goal),
        (TruthType.PLOT_TRUTH, "主冲突", main_conflict),
        (TruthType.CUSTOM, "主角代价", protagonist_cost),
        (TruthType.CUSTOM, "主角成长空间", protagonist_growth),
        (
            TruthType.FUTURE_EVENT_PRECONDITION,
            "第一阶段目标",
            confirmation.first_phase_objective,
        ),
    ]
    truth_specs.extend(
        (TruthType.CUSTOM, str(item["category"]), str(item["statement"]))
        for item in settings
        if item["strength"] == SettingStrength.CORE.value
    )
    author_truths = [
        {
            "truth_id": f"truth-{prefix}-{index}",
            "truth_type": truth_type.value,
            "title": title,
            "statement": statement,
            "subject_type": "STORY_FOUNDATION",
        }
        for index, (truth_type, title, statement) in enumerate(truth_specs, start=1)
    ]
    directives = [
        {
            "directive_id": f"directive-{prefix}-must-{index}",
            "directive_type": "requirement",
            "content": content,
        }
        for index, content in enumerate(request.must_include, start=1)
    ]
    directives.extend(
        {
            "directive_id": f"directive-{prefix}-forbid-{index}",
            "directive_type": "forbidden",
            "content": content,
        }
        for index, content in enumerate(request.forbidden, start=1)
    )
    directives.extend(
        {
            "directive_id": f"directive-{prefix}-preference-{index}",
            "directive_type": "preference",
            "content": str(item["statement"]),
        }
        for index, item in enumerate(
            [item for item in settings if item["strength"] == SettingStrength.PREFERENCE.value],
            start=1,
        )
    )
    profile_payload = proposal.book_profile_draft.model_dump(mode="json")
    expected_dimensions = {item[0] for item in PROFILE_DIMENSIONS}
    if set(profile_payload) != expected_dimensions:
        raise GenesisApplyError("故事方案必须完整提供九维全书画像初稿")
    open_questions: list[dict[str, object]] = []
    secret_candidates: list[dict[str, object]] = []
    for index, question in enumerate(proposal.open_questions, start=1):
        question_id = f"question-{prefix}-{index}"
        action = confirmation.open_question_actions.get(question_id, "KEEP_OPEN")
        if action == "KEEP_OPEN":
            open_questions.append(
                {"question_id": question_id, "title": "开放问题", "question": question}
            )
        elif action == "SECRET":
            secret_candidates.append(
                {
                    "candidate_id": f"secret-{prefix}-question-{index}",
                    "title": "由开放问题转来的幕后候选",
                    "statement": question,
                    "confidence": 0.5,
                }
            )
        elif action == "TENTATIVE":
            secret_candidates.append(
                {
                    "candidate_id": f"secret-{prefix}-tentative-{index}",
                    "title": "暂定答案",
                    "statement": question,
                    "confidence": 0.35,
                }
            )
    open_settings = [item for item in settings if item["strength"] == SettingStrength.OPEN.value]
    open_questions.extend(
        {
            "question_id": f"question-{prefix}-setting-{index}",
            "title": str(item["category"]),
            "question": str(item["statement"]),
        }
        for index, item in enumerate(open_settings, start=1)
    )
    for index, candidate in enumerate(proposal.hidden_truth_candidates, start=1):
        hidden_action = confirmation.hidden_truth_actions.get(
            candidate.candidate_id, "KEEP_CANDIDATE"
        )
        if hidden_action == "CONFIRM_TRUTH":
            author_truths.append(
                {
                    "truth_id": f"truth-{prefix}-hidden-{index}",
                    "truth_type": TruthType.CUSTOM.value,
                    "title": candidate.title,
                    "statement": candidate.statement,
                    "subject_type": "STORY_FOUNDATION",
                }
            )
        elif hidden_action == "KEEP_CANDIDATE":
            secret_candidates.append(
                {
                    "candidate_id": f"secret-{prefix}-hidden-{index}",
                    "title": candidate.title,
                    "statement": candidate.statement,
                    "confidence": candidate.confidence,
                }
            )
        elif hidden_action == "KEEP_OPEN":
            open_questions.append(
                {
                    "question_id": f"question-{prefix}-hidden-{index}",
                    "title": candidate.title,
                    "question": candidate.statement,
                }
            )
    thread_id = f"thread-original-{prefix}"
    lenses = (
        CandidateLens.CONTINUITY_ACTIVE_THREAD,
        CandidateLens.EARNED_OPPORTUNITY,
        CandidateLens.FORWARD_EXPANSION,
    )
    first_chapter_candidates = []
    for rank, (source, lens) in enumerate(
        zip(proposal.first_chapter_candidates, lenses, strict=True), start=1
    ):
        first_chapter_candidates.append(
            {
                "candidate_id": f"genesis-candidate-{prefix}-{source.candidate_id}",
                "source_candidate_id": source.candidate_id,
                "rank": rank,
                "title": source.title,
                "chapter_goal": source.chapter_goal,
                "protagonist_action": source.protagonist_action,
                "cost": source.cost,
                "irreversible_change": source.irreversible_change,
                "future_space": source.ending_turn,
                "risk": source.distinctiveness,
                "lens": lens.value,
                "plan": _candidate_plan(
                    source,
                    thread_id=thread_id,
                    world_rules=confirmation.world_rules,
                    request=request,
                    lens=lens,
                ),
                "score_status": "NOT_COMPUTED",
                "gate_status": "NOT_RUN",
            }
        )
    return GenesisApplyPlan(
        proposal_version_id=proposal_version_id,
        selected_title=selected_title,
        selected_foundation=foundation.model_dump(mode="json"),
        selected_route=route.model_dump(mode="json"),
        author_truths=author_truths,
        persistent_directives=directives,
        profile_dimensions=profile_payload,
        open_questions=open_questions,
        secret_candidates=secret_candidates,
        narrative_spine={
            "spine_id": f"spine-{prefix}",
            "route_id": route.route_id,
            "direction": route.direction,
            "central_pressure": route.central_pressure,
            "opportunity": route.opportunity,
            "risk": route.risk,
            "commitments": route.commitments,
            "open_alternatives": route.open_alternatives,
        },
        rolling_planning=rolling,
        main_thread={
            "thread_id": thread_id,
            "goal": protagonist_goal,
            "stakes": main_conflict,
            "foundation_candidate_id": foundation.candidate_id,
            "route_id": route.route_id,
        },
        first_chapter_candidates=first_chapter_candidates,
    )


def _existing_apply(
    connection: sqlite3.Connection,
    proposal_version_id: str,
    selected_foundation_id: str,
) -> sqlite3.Row | None:
    row = connection.execute(
        "SELECT * FROM original_genesis_applies WHERE proposal_version_id=? "
        "AND selected_foundation_id=?",
        (proposal_version_id, selected_foundation_id),
    ).fetchone()
    return row if isinstance(row, sqlite3.Row) else None


def apply_genesis_plan(
    database: Database,
    book_id: str,
    plan: GenesisApplyPlan,
) -> dict[str, Any]:
    payload = plan.model_dump(mode="json")
    selected_foundation_id = str(plan.selected_foundation["candidate_id"])
    apply_id = f"genesis-apply-{plan.proposal_version_id}-{selected_foundation_id}"
    now = utc_now()
    with database.connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        proposal = connection.execute(
            "SELECT status FROM original_proposal_versions WHERE proposal_version_id=? "
            "AND book_id=? AND edition_id='base'",
            (plan.proposal_version_id, book_id),
        ).fetchone()
        if proposal is None or str(proposal["status"]) != "CURRENT":
            raise GenesisApplyError("只能确认当前故事方案")
        existing = _existing_apply(connection, plan.proposal_version_id, selected_foundation_id)
        if existing is not None:
            if json.loads(str(existing["apply_plan_json"])) != payload:
                raise GenesisApplyError("同一故事方案已经按不同内容确认，不能再次覆盖")
            return {
                "apply_id": str(existing["apply_id"]),
                "apply_plan": payload,
                "idempotent": True,
            }
        state = connection.execute(
            "SELECT accepted_apply_id FROM original_states WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        if state is not None and state["accepted_apply_id"]:
            raise GenesisApplyError("这部作品的故事基础已经确认")
        for truth in plan.author_truths:
            connection.execute(
                "INSERT INTO author_truths("
                "truth_id, book_id, edition_id, truth_type, subject_type, title, statement, "
                "status, confidence, introduced_by, effective_from_chapter, retroactive_scope, "
                "compatibility_status, compatibility_summary, must_remain_true, tags_json, "
                "metadata_json, created_at, updated_at, version"
                ") VALUES (?, ?, 'base', ?, ?, ?, ?, 'ACTIVE_TRUTH', 1.0, "
                "'AUTHOR_CONFIRMED', 1, 'FORWARD_ONLY', 'COMPATIBLE_WITH_GAPS', "
                "'原创项目从第一章起生效', 1, '[\"ORIGINAL_GENESIS\"]', ?, ?, ?, 1)",
                (
                    str(truth["truth_id"]),
                    book_id,
                    str(truth["truth_type"]),
                    str(truth["subject_type"]),
                    str(truth["title"]),
                    str(truth["statement"]),
                    json_dumps(
                        {
                            "proposal_version_id": plan.proposal_version_id,
                            "foundation_candidate_id": selected_foundation_id,
                        }
                    ),
                    now,
                    now,
                ),
            )
        for directive in plan.persistent_directives:
            connection.execute(
                "INSERT INTO author_directives("
                "directive_id, book_id, edition_id, directive_type, content, mode, status, "
                "priority, source, created_at, version"
                ") VALUES (?, ?, 'base', ?, ?, 'persistent', 'ACTIVE', 100, "
                "'AUTHOR_CONFIRMED_FOUNDATION', ?, 1)",
                (
                    str(directive["directive_id"]),
                    book_id,
                    str(directive["directive_type"]),
                    str(directive["content"]),
                    now,
                ),
            )
        current_profile = connection.execute(
            "SELECT COALESCE(MAX(version_number), 0) FROM book_profile_versions "
            "WHERE book_id=? AND edition_id='base'",
            (book_id,),
        ).fetchone()
        profile_version = int(current_profile[0]) + 1
        profile_labels = {dimension: label for dimension, label, _ in PROFILE_DIMENSIONS}
        profile_files = {dimension: filename for dimension, _, filename in PROFILE_DIMENSIONS}
        baseline = {
            dimension: {
                "dimension": dimension,
                "label": profile_labels[dimension],
                "filename": profile_files[dimension],
                "content": str(value["summary"]),
                "available": True,
                "source": "ORIGINAL_FOUNDATION_PROPOSAL",
                "draft": value,
            }
            for dimension, value in plan.profile_dimensions.items()
        }
        connection.execute(
            "INSERT INTO book_profile_versions("
            "profile_version_id, book_id, edition_id, version_number, baseline_json, "
            "author_edits_json, reason, created_at, version"
            ") VALUES (?, ?, 'base', ?, ?, '[]', ?, ?, 1)",
            (
                f"book-profile-{plan.proposal_version_id}",
                book_id,
                profile_version,
                json_dumps(baseline),
                "作者确认故事基础方案",
                now,
            ),
        )
        for horizon, items in plan.rolling_planning.items():
            connection.execute(
                "INSERT INTO author_control_intents("
                "intent_id, book_id, edition_id, intent_type, subject_type, subject_id, "
                "title, description, horizon, priority, status, payload_json, created_at, "
                "updated_at, version) VALUES (?, ?, 'base', 'ROLLING_PLANNING', "
                "'STORY_FOUNDATION', ?, ?, ?, ?, 100, 'PLANNED', ?, ?, ?, 1)",
                (
                    f"intent-{plan.proposal_version_id}-{horizon}",
                    book_id,
                    selected_foundation_id,
                    {"short": "近期方向", "mid": "中期方向", "long": "长期可能性"}[horizon],
                    "；".join(items),
                    horizon.upper(),
                    json_dumps(
                        {
                            "items": items,
                            "fixed_chapter_outline": False,
                            "route_id": plan.selected_route["route_id"],
                        }
                    ),
                    now,
                    now,
                ),
            )
        for question in plan.open_questions:
            connection.execute(
                "INSERT INTO open_creative_questions("
                "question_id, book_id, edition_id, title, question, subject_type, horizon, "
                "status, created_at, updated_at, version"
                ") VALUES (?, ?, 'base', ?, ?, 'STORY_FOUNDATION', 'LONG', "
                "'OPEN_QUESTION', ?, ?, 1)",
                (
                    str(question["question_id"]),
                    book_id,
                    str(question["title"]),
                    str(question["question"]),
                    now,
                    now,
                ),
            )
        for secret in plan.secret_candidates:
            connection.execute(
                "INSERT INTO secret_candidates("
                "candidate_id, book_id, edition_id, title, statement, truth_type, "
                "subject_type, evidence_json, confidence, source, status, created_at, "
                "updated_at, version) VALUES (?, ?, 'base', ?, ?, 'CUSTOM', "
                "'STORY_FOUNDATION', '[]', ?, 'ORIGINAL_PROPOSAL', "
                "'INFERRED_SECRET_CANDIDATE', ?, ?, 1)",
                (
                    str(secret["candidate_id"]),
                    book_id,
                    str(secret["title"]),
                    str(secret["statement"]),
                    float(secret["confidence"]),
                    now,
                    now,
                ),
            )
        spine = plan.narrative_spine
        connection.execute(
            "INSERT INTO active_narrative_spines("
            "spine_id, book_id, edition_id, proposal_version_id, route_id, direction, "
            "central_pressure, opportunity, risk, commitments_json, open_alternatives_json, "
            "status, created_at, updated_at, version"
            ") VALUES (?, ?, 'base', ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?, 1)",
            (
                str(spine["spine_id"]),
                book_id,
                plan.proposal_version_id,
                str(spine["route_id"]),
                str(spine["direction"]),
                str(spine["central_pressure"]),
                str(spine["opportunity"]),
                str(spine["risk"]),
                json_dumps(spine["commitments"]),
                json_dumps(spine["open_alternatives"]),
                now,
                now,
            ),
        )
        thread = plan.main_thread
        connection.execute(
            "INSERT INTO threads(thread_id, book_id, goal, stakes, phase, importance, "
            "reader_visibility, progress, dependencies_json, status, payload_json, "
            "created_at, version, edition_id) VALUES (?, ?, ?, ?, 'setup', 1.0, 1.0, "
            "0.0, '[]', 'APPROVED_OUTLINE', ?, ?, 1, 'base')",
            (
                str(thread["thread_id"]),
                book_id,
                str(thread["goal"]),
                str(thread["stakes"]),
                json_dumps(thread),
                now,
            ),
        )
        task_id = f"genesis-plan-{plan.proposal_version_id}-{selected_foundation_id}"
        for candidate in plan.first_chapter_candidates:
            connection.execute(
                "INSERT INTO candidate_plans("
                "candidate_id, book_id, task_id, rank, primary_thread_id, primary_function, "
                "secondary_functions_json, plan_json, score_json, gate_report_json, "
                "selection_status, status, created_at, version, edition_id"
                ") VALUES (?, ?, ?, ?, ?, ?, '[]', ?, ?, ?, 'NOT_SELECTED', "
                "'CANDIDATE', ?, 1, 'base')",
                (
                    str(candidate["candidate_id"]),
                    book_id,
                    task_id,
                    int(candidate["rank"]),
                    str(thread["thread_id"]),
                    str(candidate["plan"]["primary_function"]),
                    json_dumps(candidate["plan"]),
                    json_dumps(
                        {
                            "score_status": "NOT_COMPUTED",
                            "reason": "尚未经过评分引擎",
                        }
                    ),
                    json_dumps(
                        {
                            "gate_status": "NOT_RUN",
                            "reason": "选择后执行章节合同校验",
                        }
                    ),
                    now,
                ),
            )
        connection.execute(
            "INSERT INTO original_genesis_applies("
            "apply_id, book_id, edition_id, proposal_version_id, selected_foundation_id, "
            "selected_route_id, selected_title, apply_plan_json, status, applied_at, version"
            ") VALUES (?, ?, 'base', ?, ?, ?, ?, ?, 'APPLIED', ?, 1)",
            (
                apply_id,
                book_id,
                plan.proposal_version_id,
                selected_foundation_id,
                str(plan.selected_route["route_id"]),
                plan.selected_title,
                json_dumps(payload),
                now,
            ),
        )
        connection.execute(
            "UPDATE original_states SET state='FOUNDATION_READY', accepted_apply_id=?, "
            "current_proposal_version_id=?, updated_at=?, version=version+1 "
            "WHERE book_id=? AND edition_id='base'",
            (apply_id, plan.proposal_version_id, now, book_id),
        )
        connection.execute(
            "UPDATE books SET title=?, updated_at=?, version=version+1 WHERE book_id=?",
            (plan.selected_title, now, book_id),
        )
    return {"apply_id": apply_id, "apply_plan": payload, "idempotent": False}


def accepted_foundation(
    database: Database,
    book_id: str,
) -> dict[str, Any] | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT a.* FROM original_states s JOIN original_genesis_applies a "
            "ON a.apply_id=s.accepted_apply_id WHERE s.book_id=? AND s.edition_id='base'",
            (book_id,),
        ).fetchone()
    if row is None:
        return None
    plan = json.loads(str(row["apply_plan_json"]))
    return {
        "schema_version": "original-foundation-v2",
        "information_status": "AUTHOR_CONFIRMED",
        "confirmed_at": str(row["applied_at"]),
        "apply_id": str(row["apply_id"]),
        "selected_title": str(row["selected_title"]),
        "selected_foundation_id": str(row["selected_foundation_id"]),
        "selected_route_id": str(row["selected_route_id"]),
        "genesis_task_id": (
            f"genesis-plan-{row['proposal_version_id']}-{row['selected_foundation_id']}"
        ),
        "apply_plan": plan,
    }


def export_accepted_foundation(
    database: Database,
    book_id: str,
    path: Path,
) -> Path:
    payload = accepted_foundation(database, book_id)
    if payload is None:
        raise GenesisApplyError("数据库中尚无已确认的故事基础")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


__all__ = [
    "GenesisApplyError",
    "accepted_foundation",
    "apply_genesis_plan",
    "build_genesis_apply_plan",
    "export_accepted_foundation",
]
