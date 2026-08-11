"""Source-free original novel service built on the existing authoring kernel."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from novel_authoring.author_control.book_profile import (
    PROFILE_DIMENSIONS,
    ProfileEditOperation,
    ProfileStrength,
    edit_book_profile,
    load_effective_book_profile,
)
from novel_authoring.author_control.models import AuthorControlHorizon
from novel_authoring.author_control.service import execute_author_intent
from novel_authoring.author_control.truth import (
    AuthorTruthInput,
    TruthSource,
    TruthType,
    create_author_truth,
)
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.domain.models import ContinuationMode
from novel_authoring.drafting.service import prepare_draft_task
from novel_authoring.edition import ensure_base_edition
from novel_authoring.original.models import (
    FOUNDATION_CONFIRMATION,
    FirstChapterCandidate,
    OriginalBookRequest,
    OriginalBootstrapProposal,
    OriginalFoundationConfirmation,
    OriginalState,
)
from novel_authoring.original.state import original_record
from novel_authoring.planning.boundary import build_boundary_packet
from novel_authoring.planning.contracts import build_chapter_contract
from novel_authoring.planning.innovation import resolve_innovation_control
from novel_authoring.planning.models import CandidateLens, CandidateProposal
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.operations import ensure_operation
from novel_authoring.storage.registry import (
    BookKind,
    BookRegistry,
    CreationMode,
)
from novel_authoring.utils import json_dumps, safe_book_id, utc_now
from novel_authoring.validation.service import validate_draft
from novel_authoring.workflows.approval import approval_preview, approve_draft
from novel_authoring.workflows.directives import add_directive
from novel_authoring.workflows.handoffs import (
    HandoffType,
    create_continuation_handoff,
    create_original_bootstrap_handoff,
    get_handoff,
    validate_result_file,
)


class OriginalWorkflowError(RuntimeError):
    pass


def _original_root(database: Database, book_id: str) -> Path:
    record = original_record(database, book_id)
    if record is None:
        raise OriginalWorkflowError("当前项目不是 ORIGINAL 小说")
    return Path(record.root)


def _original_dir(database: Database, book_id: str) -> Path:
    root = _original_root(database, book_id)
    path = BookLayout(root.parent).for_book(book_id).edition("base").analysis / "original"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _update_registry(
    database: Database,
    book_id: str,
    *,
    state: OriginalState,
    title: str | None = None,
    latest_chapter: int | None = None,
) -> None:
    root = _original_root(database, book_id)
    layout = BookLayout(root.parent)
    registry = BookRegistry(layout)
    paths = layout.for_book(book_id)
    values = registry.read(book_id)
    values["original_state"] = state.value
    values["readiness_status"] = state.value
    values["updated_at"] = utc_now()
    if title is not None:
        values["title"] = title
    if latest_chapter is not None:
        values["latest_chapter"] = latest_chapter
    registry.write(paths, values)
    registry.write_readme(paths, values)


def create_original_book(
    layout: BookLayout,
    request: OriginalBookRequest | dict[str, Any],
    *,
    book_id: str | None = None,
) -> dict[str, Any]:
    data = (
        request
        if isinstance(request, OriginalBookRequest)
        else OriginalBookRequest.model_validate(request)
    )
    selected_id = safe_book_id(book_id or f"original-{uuid.uuid4().hex[:12]}")
    paths = layout.for_book(selected_id)
    if paths.root.exists():
        raise OriginalWorkflowError(f"原创项目已存在：{selected_id}")
    layout.library_root.mkdir(parents=True, exist_ok=True)
    paths = layout.ensure_book(selected_id)
    for directory in paths.edition("base").all_directories():
        directory.mkdir(parents=True, exist_ok=True)
    database = Database(paths.database)
    database.initialize()
    now = utc_now()
    working_title = "原创项目 · " + data.premise.strip().replace("\n", " ")[:24]
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO books(book_id, title, mode, source_root, workspace_root, "
            "created_at, updated_at, version) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
            (
                selected_id,
                working_title,
                ContinuationMode.CONSTRAINED_INNOVATION.value,
                str(paths.source),
                str(paths.root),
                now,
                now,
            ),
        )
    ensure_base_edition(database, selected_id)
    registry = BookRegistry(layout)
    registry.ensure(
        selected_id,
        title=working_title,
        active_edition_id="base",
        readiness_status=OriginalState.ORIGINAL_SEED.value,
        book_kind=BookKind.AUTHOR,
        creation_mode=CreationMode.ORIGINAL,
    )
    values = registry.read(selected_id)
    values["original_state"] = OriginalState.ORIGINAL_SEED.value
    values["source_storage_mode"] = "NONE_ORIGINAL"
    values["source"] = {"root": "source", "files": []}
    values["source_files"] = []
    registry.write(paths, values)
    registry.write_readme(paths, values)
    request_path = _write_json(
        paths.edition("base").analysis / "original" / "request.json",
        data.model_dump(mode="json"),
    )
    return {
        "book_id": selected_id,
        "title": working_title,
        "database": str(paths.database),
        "request_path": str(request_path),
        "book_kind": BookKind.AUTHOR.value,
        "creation_mode": CreationMode.ORIGINAL.value,
        "original_state": OriginalState.ORIGINAL_SEED.value,
        "chapter_count": 0,
        "source_required": False,
    }


def prepare_original_bootstrap(
    database: Database, book_id: str
) -> dict[str, Any]:
    request_path = _original_dir(database, book_id) / "request.json"
    request = _read_json(request_path)
    if request is None:
        raise OriginalWorkflowError("原创 premise 请求不存在")
    handoff = create_original_bootstrap_handoff(
        database,
        book_id,
        edition_id="base",
        original_bootstrap_request=request,
    )
    _update_registry(database, book_id, state=OriginalState.ORIGINAL_SEED)
    return handoff


def import_original_bootstrap_proposal(
    database: Database, book_id: str, handoff_id: str
) -> dict[str, Any]:
    accepted_path = _original_dir(database, book_id) / "story_foundation" / "accepted.json"
    if accepted_path.is_file():
        raise OriginalWorkflowError("Story Foundation 已确认，不能再导入 Proposal")
    handoff = get_handoff(database, handoff_id)
    if (
        str(handoff["book_id"]) != book_id
        or str(handoff["handoff_type"]) != HandoffType.ORIGINAL_BOOK_BOOTSTRAP.value
    ):
        raise OriginalWorkflowError("handoff 不属于当前原创项目的基础框架任务")
    result = validate_result_file(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"])).resolve()
    artifact_root = (task_directory / "artifacts").resolve()
    proposal_path: Path | None = None
    for raw_path in result.get("artifact_paths", []):
        candidate = Path(str(raw_path))
        if not candidate.is_absolute():
            candidate = task_directory / candidate
        candidate = candidate.resolve()
        try:
            candidate.relative_to(artifact_root)
        except ValueError:
            continue
        if candidate.name == "proposal.json" and candidate.is_file():
            proposal_path = candidate
            break
    if proposal_path is None:
        raise OriginalWorkflowError("handoff 未返回 story_foundation/proposal.json")
    proposal = OriginalBootstrapProposal.model_validate_json(
        proposal_path.read_text(encoding="utf-8")
    )
    foundation_ids = [item.candidate_id for item in proposal.foundation_candidates]
    if list(result.get("candidate_ids", [])) != foundation_ids:
        raise OriginalWorkflowError("handoff candidate_ids 与 Foundation Proposal 不一致")
    canonical_path = _write_json(
        _original_dir(database, book_id) / "story_foundation" / "proposal.json",
        proposal.model_dump(mode="json"),
    )
    _update_registry(database, book_id, state=OriginalState.BOOTSTRAP_READY)
    return {
        "book_id": book_id,
        "handoff_id": handoff_id,
        "original_state": OriginalState.BOOTSTRAP_READY.value,
        "proposal_path": str(canonical_path),
        "proposal": proposal.model_dump(mode="json"),
        "canon_changed": False,
        "chapter_created": False,
    }


def load_original_proposal(
    database: Database, book_id: str
) -> OriginalBootstrapProposal | None:
    path = _original_dir(database, book_id) / "story_foundation" / "proposal.json"
    if not path.is_file():
        return None
    return OriginalBootstrapProposal.model_validate_json(path.read_text(encoding="utf-8"))


def _profile_values(
    request: OriginalBookRequest,
    *,
    protagonist: str,
    protagonist_growth: str,
    main_conflict: str,
    core_reading_promise: str,
    characters: list[str],
    factions: list[str],
    world_rules: list[str],
    phase_objective: str,
) -> dict[str, str]:
    character_text = "；".join(characters)
    faction_text = "；".join(factions)
    return {
        "worldbuilding": "；".join(world_rules),
        "characters": (
            f"主角：{protagonist}；成长：{protagonist_growth}；{character_text}"
        ),
        "plot": f"主冲突：{main_conflict}；第一阶段：{phase_objective}",
        "style": request.tone_style or "以当前 Foundation 的阅读承诺为文风基准",
        "narrative": request.pov or "视角在首章合同中明确并保持一致",
        "dialogue": "对话必须承担人物选择、关系压力或信息差，不作设定讲义",
        "pacing": f"SHORT/MID/LONG 滚动规划；不锁定逐章远期大纲。势力：{faction_text or '开放'}",
        "themes": core_reading_promise,
        "continuity": "所有后续变化必须经过 Chapter Contract、Validator 与作者显式批准",
    }


def _candidate_plan(
    item: FirstChapterCandidate,
    *,
    thread_id: str,
    world_rules: list[str],
    request: OriginalBookRequest,
    lens: CandidateLens,
) -> CandidateProposal:
    settings = load_settings()
    character_inputs = dict.fromkeys(
        settings.metrics["character_fit"]["weights"], 85.0
    )
    style_inputs = dict.fromkeys(settings.metrics["style_fit"]["weights"], 85.0)
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
    return CandidateProposal.model_validate(
        {
            "local_id": item.candidate_id,
            "title": item.title,
            "summary": item.chapter_goal,
            "primary_thread_id": thread_id,
            "primary_function": item.primary_function.value,
            "secondary_functions": [],
            "reader_question": item.hook,
            "event_source": item.opening_situation,
            "solution_method": item.protagonist_action,
            "protagonist_strategy": item.central_choice,
            "risk_form": item.conflict,
            "opportunity_cost": item.cost,
            "emotional_outcome": item.ending_turn,
            "social_feedback": item.distinctiveness,
            "scene_topology": item.opening_situation,
            "ending_state": item.ending_turn,
            "state_changes": [item.irreversible_change, item.ending_turn],
            "causal_sources": ["作者确认的 Story Foundation 与 Genesis State"],
            "required_irreversible_change": item.irreversible_change,
            "required_cost": item.cost,
            "must_not_resolve": ["不得在首章锁死长期路线或结局"],
            "canon_constraints": world_rules,
            "knowledge_constraints": ["不得让角色无依据知晓隐藏真相"],
            "forbidden_repetitions": request.forbidden,
            "style_constraints": {
                "tone_style": request.tone_style or "遵循已确认画像",
                "pov": request.pov or "由 Chapter Contract 冻结",
            },
            "commit_updates": [f"thread_status:{thread_id}", "character_state:protagonist"],
            "pressure_before": 0,
            "pressure_target_after": 35,
            "score_inputs": {name: 75 for name in score_names},
            "score_evidence": {
                name: [f"Genesis 候选差异：{item.distinctiveness}"] for name in score_names
            },
            "gate_input": {
                "character_fit_inputs": character_inputs,
                "style_fit_inputs": style_inputs,
            },
            "lens": lens.value,
            "wildcard": lens is CandidateLens.FORWARD_EXPANSION,
        }
    )


def _seed_genesis_candidates(
    database: Database,
    book_id: str,
    proposal: OriginalBootstrapProposal,
    request: OriginalBookRequest,
    *,
    thread_id: str,
    world_rules: list[str],
) -> dict[str, Any]:
    boundary = build_boundary_packet(database, book_id, edition_id="base")
    boundary_payload = json.loads(
        Path(str(boundary["json_path"])).read_text(encoding="utf-8")
    )
    innovation, _ = resolve_innovation_control(database, book_id)
    profile = load_effective_book_profile(database, book_id, "base")
    task_id = f"genesis-plan-{uuid.uuid4().hex}"
    operation = ensure_operation(
        database,
        book_id,
        "base",
        task_id,
        "GENESIS_PLAN",
        {"boundary_packet_id": boundary["packet_id"], "chapter": 1},
    )
    if operation is None:
        raise OriginalWorkflowError("原创项目必须使用 Book Library Operation Workspace")
    metadata = {
        "task_id": task_id,
        "task_type": "genesis_plan",
        "book_id": book_id,
        "edition_id": "base",
        "boundary_packet_id": boundary["packet_id"],
        "boundary_path": boundary["json_path"],
        "innovation_control": innovation.model_dump(mode="json"),
        "narrative_portfolio_snapshot": boundary_payload.get("narrative_portfolio"),
        "truth_reveal": {
            "target_chapter_ordinal": 1,
            "active_author_truths": boundary_payload.get("active_author_truths", []),
            "reveal_agenda": boundary_payload.get("reveal_agenda", {}),
        },
        "effective_book_profile": profile,
        "aggregate_id": None,
        "created_at": utc_now(),
        "information_status": "CANDIDATE",
    }
    _write_json(operation.input / "task.json", metadata)
    lenses = (
        CandidateLens.CONTINUITY_ACTIVE_THREAD,
        CandidateLens.EARNED_OPPORTUNITY,
        CandidateLens.FORWARD_EXPANSION,
    )
    candidate_rows: list[dict[str, Any]] = []
    with database.connect() as connection:
        for rank, (source, lens) in enumerate(
            zip(proposal.first_chapter_candidates, lenses, strict=True), start=1
        ):
            plan = _candidate_plan(
                source,
                thread_id=thread_id,
                world_rules=world_rules,
                request=request,
                lens=lens,
            )
            candidate_id = f"genesis-candidate-{uuid.uuid4().hex}"
            score = {
                "score": 75,
                "base_candidate_score": 75,
                "final_selection_score": 75,
                "reason": "作者已确认 Foundation；等待显式选择首章候选",
                "genesis": True,
            }
            gate = {
                "passed": True,
                "hard_failures": [],
                "character_fit": 85,
                "style_fit": 85,
                "requires_character_bridge": False,
                "style_review_required": False,
            }
            connection.execute(
                "INSERT INTO candidate_plans(candidate_id, book_id, task_id, rank, "
                "primary_thread_id, primary_function, secondary_functions_json, plan_json, "
                "score_json, gate_report_json, selection_status, status, created_at, version, "
                "edition_id) VALUES (?, ?, ?, ?, ?, ?, '[]', ?, ?, ?, 'NOT_SELECTED', "
                "'CANDIDATE', ?, 1, 'base')",
                (
                    candidate_id,
                    book_id,
                    task_id,
                    rank,
                    thread_id,
                    plan.primary_function.value,
                    json_dumps(plan.model_dump(mode="json")),
                    json_dumps(score),
                    json_dumps(gate),
                    utc_now(),
                ),
            )
            candidate_rows.append(
                {
                    "candidate_id": candidate_id,
                    "rank": rank,
                    "title": source.title,
                    "summary": source.chapter_goal,
                    "hook": source.hook,
                    "cost": source.cost,
                    "ending_turn": source.ending_turn,
                    "lens": lens.value,
                    "selection_status": "NOT_SELECTED",
                }
            )
    return {
        "task_id": task_id,
        "boundary_packet_id": boundary["packet_id"],
        "candidates": candidate_rows,
    }


def confirm_original_foundation(
    database: Database,
    book_id: str,
    confirmation: OriginalFoundationConfirmation | dict[str, Any],
) -> dict[str, Any]:
    data = (
        confirmation
        if isinstance(confirmation, OriginalFoundationConfirmation)
        else OriginalFoundationConfirmation.model_validate(confirmation)
    )
    if data.confirmation != FOUNDATION_CONFIRMATION:
        raise OriginalWorkflowError(
            f"必须逐字提供确认语“{FOUNDATION_CONFIRMATION}”"
        )
    proposal = load_original_proposal(database, book_id)
    if proposal is None:
        raise OriginalWorkflowError("尚无可确认的 Story Foundation Proposal")
    accepted_path = _original_dir(database, book_id) / "story_foundation" / "accepted.json"
    if accepted_path.is_file():
        raise OriginalWorkflowError("Story Foundation 已确认，不能重复确认")
    if data.selected_title not in proposal.title_candidates:
        raise OriginalWorkflowError("selected_title 必须来自三个标题候选")
    foundation = next(
        (
            item
            for item in proposal.foundation_candidates
            if item.candidate_id == data.selected_foundation_id
        ),
        None,
    )
    if foundation is None:
        raise OriginalWorkflowError("selected_foundation_id 不属于当前 Proposal")
    if data.selected_route_id not in {item.route_id for item in proposal.routes}:
        raise OriginalWorkflowError("selected_route_id 不属于当前 Proposal")
    selected_title = data.title_override.strip() or data.selected_title
    protagonist = data.protagonist_override.strip() or proposal.protagonist
    protagonist_goal = data.protagonist_goal_override.strip() or proposal.protagonist_goal
    main_conflict = data.main_conflict_override.strip() or foundation.main_conflict
    protagonist_cost = data.protagonist_cost_override.strip() or proposal.protagonist_cost
    protagonist_growth = (
        data.protagonist_growth_override.strip() or proposal.protagonist_growth
    )
    characters = data.characters_override or proposal.characters
    factions = data.factions_override or proposal.factions
    rolling_short = data.rolling_short_override or proposal.rolling_planning.short
    rolling_mid = data.rolling_mid_override or proposal.rolling_planning.mid
    rolling_long = data.rolling_long_override or proposal.rolling_planning.long
    request_payload = _read_json(_original_dir(database, book_id) / "request.json")
    if request_payload is None:
        raise OriginalWorkflowError("原创 premise 请求不存在")
    request = OriginalBookRequest.model_validate(request_payload)
    with database.connect() as connection:
        chapters_before = int(
            connection.execute(
                "SELECT COUNT(*) FROM chapters WHERE book_id=?", (book_id,)
            ).fetchone()[0]
        )
        commits_before = int(
            connection.execute(
                "SELECT COUNT(*) FROM canon_commits WHERE book_id=?", (book_id,)
            ).fetchone()[0]
        )
    truth_payloads = [
        (TruthType.CHARACTER_IDENTITY, "主角", protagonist),
        (TruthType.CHARACTER_GOAL, "主角目标", protagonist_goal),
        (TruthType.PLOT_TRUTH, "主冲突", main_conflict),
        (TruthType.CUSTOM, "主角代价", protagonist_cost),
        (TruthType.CUSTOM, "主角成长空间", protagonist_growth),
        (TruthType.FUTURE_EVENT_PRECONDITION, "第一阶段目标", data.first_phase_objective),
        *[
            (TruthType.CUSTOM, f"世界规则 {index}", rule)
            for index, rule in enumerate(data.world_rules, start=1)
        ],
    ]
    truth_ids: list[str] = []
    for truth_type, title, statement in truth_payloads:
        truth = create_author_truth(
            database,
            book_id,
            "base",
            AuthorTruthInput(
                truth_type=truth_type,
                subject_type="STORY_FOUNDATION",
                title=title,
                statement=statement,
                introduced_by=TruthSource.AUTHOR_CONFIRMED,
                effective_from_chapter=1,
                tags=["ORIGINAL_GENESIS"],
                metadata={"foundation_candidate_id": foundation.candidate_id},
            ),
        )
        truth_ids.append(str(truth["truth_id"]))
    for content in request.must_include:
        add_directive(
            database,
            book_id,
            directive_type="requirement",
            content=content,
            scope="persistent",
            source="AUTHOR_CONFIRMED_FOUNDATION",
            edition_id="base",
        )
    for content in request.forbidden:
        add_directive(
            database,
            book_id,
            directive_type="forbidden",
            content=content,
            scope="persistent",
            source="AUTHOR_CONFIRMED_FOUNDATION",
            edition_id="base",
        )
    for dimension, _, _ in PROFILE_DIMENSIONS:
        edit_book_profile(
            database,
            book_id,
            "base",
            dimension=dimension,
            operation=ProfileEditOperation.ADD,
            content=_profile_values(
                request,
                protagonist=protagonist,
                protagonist_growth=protagonist_growth,
                main_conflict=main_conflict,
                core_reading_promise=foundation.core_reading_promise,
                characters=characters,
                factions=factions,
                world_rules=data.world_rules,
                phase_objective=data.first_phase_objective,
            )[dimension],
            strength=ProfileStrength.PREFER,
            reason="作者确认原创 Story Foundation",
        )
    for horizon, items in (
        (AuthorControlHorizon.SHORT, rolling_short),
        (AuthorControlHorizon.MID, rolling_mid),
        (AuthorControlHorizon.LONG, rolling_long),
    ):
        execute_author_intent(
            database,
            book_id,
            "base",
            intent_type="ROLLING_PLANNING",
            subject_type="STORY_FOUNDATION",
            title=f"{horizon.value} Rolling Planning",
            description="；".join(items),
            horizon=horizon,
            payload={"items": items, "fixed_chapter_outline": False},
        )
    thread_id = f"thread-original-{uuid.uuid4().hex}"
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO threads(thread_id, book_id, goal, stakes, phase, "
            "introduced_chapter, last_advanced_chapter, importance, reader_visibility, "
            "progress, dependencies_json, status, source_span_id, payload_json, created_at, "
            "version, edition_id) VALUES (?, ?, ?, ?, 'setup', NULL, NULL, 1.0, 1.0, "
            "0.0, '[]', 'APPROVED_OUTLINE', NULL, ?, ?, 1, 'base')",
            (
                thread_id,
                book_id,
                protagonist_goal,
                main_conflict,
                json_dumps(
                    {
                        "foundation_candidate_id": foundation.candidate_id,
                        "route_id": data.selected_route_id,
                        "information_status": "APPROVED_OUTLINE",
                    }
                ),
                utc_now(),
            ),
        )
        connection.execute(
            "UPDATE books SET title=?, updated_at=?, version=version+1 WHERE book_id=?",
            (selected_title, utc_now(), book_id),
        )
    genesis = _seed_genesis_candidates(
        database,
        book_id,
        proposal,
        request,
        thread_id=thread_id,
        world_rules=data.world_rules,
    )
    accepted = {
        "schema_version": "original-foundation-v1",
        "information_status": "AUTHOR_CONFIRMED",
        "confirmed_at": utc_now(),
        "selected_title": selected_title,
        "selected_foundation_id": foundation.candidate_id,
        "selected_route_id": data.selected_route_id,
        "protagonist": protagonist,
        "protagonist_goal": protagonist_goal,
        "main_conflict": main_conflict,
        "protagonist_cost": protagonist_cost,
        "protagonist_growth": protagonist_growth,
        "characters": characters,
        "factions": factions,
        "world_rules": data.world_rules,
        "first_phase_objective": data.first_phase_objective,
        "rolling_planning": {
            "short": rolling_short,
            "mid": rolling_mid,
            "long": rolling_long,
        },
        "truth_ids": truth_ids,
        "main_thread_id": thread_id,
        "genesis_task_id": genesis["task_id"],
        "proposal": proposal.model_dump(mode="json"),
    }
    accepted_path = _write_json(accepted_path, accepted)
    _update_registry(
        database,
        book_id,
        state=OriginalState.FOUNDATION_ACCEPTED,
        title=selected_title,
    )
    with database.connect() as connection:
        chapters_after = int(
            connection.execute(
                "SELECT COUNT(*) FROM chapters WHERE book_id=?", (book_id,)
            ).fetchone()[0]
        )
        commits_after = int(
            connection.execute(
                "SELECT COUNT(*) FROM canon_commits WHERE book_id=?", (book_id,)
            ).fetchone()[0]
        )
    if chapters_after != chapters_before or commits_after != commits_before:
        raise OriginalWorkflowError("确认 Foundation 不得创建章节或 Canon Commit")
    return {
        "book_id": book_id,
        "original_state": OriginalState.FOUNDATION_ACCEPTED.value,
        "accepted_path": str(accepted_path),
        "truth_ids": truth_ids,
        "genesis": genesis,
        "chapter_created": False,
        "canon_changed": False,
    }


def select_first_chapter_candidate(
    database: Database, book_id: str, candidate_id: str
) -> dict[str, Any]:
    accepted = _read_json(
        _original_dir(database, book_id) / "story_foundation" / "accepted.json"
    )
    if accepted is None:
        raise OriginalWorkflowError("必须先确认 Story Foundation")
    task_id = str(accepted.get("genesis_task_id") or "")
    with database.connect() as connection:
        selected_row = connection.execute(
            "SELECT candidate_id FROM candidate_plans WHERE book_id=? AND edition_id='base' "
            "AND task_id=? AND selection_status='SELECTED'",
            (book_id, task_id),
        ).fetchone()
        if selected_row is not None:
            raise OriginalWorkflowError("第一章候选已经选择，不能重复创建合同与 Draft handoff")
        row = connection.execute(
            "SELECT candidate_id FROM candidate_plans WHERE book_id=? AND edition_id='base' "
            "AND task_id=? AND candidate_id=? AND status='CANDIDATE'",
            (book_id, task_id, candidate_id),
        ).fetchone()
        if row is None:
            raise OriginalWorkflowError("首章候选不存在或已失效")
        connection.execute(
            "UPDATE candidate_plans SET selection_status='NOT_SELECTED' "
            "WHERE book_id=? AND edition_id='base' AND task_id=?",
            (book_id, task_id),
        )
        connection.execute(
            "UPDATE candidate_plans SET selection_status='SELECTED' "
            "WHERE book_id=? AND edition_id='base' AND candidate_id=?",
            (book_id, candidate_id),
        )
    contract = build_chapter_contract(
        database, book_id, candidate_id, edition_id="base"
    )
    draft_task = prepare_draft_task(
        database, book_id, str(contract["contract_id"]), edition_id="base"
    )
    handoff = create_continuation_handoff(
        database,
        book_id,
        edition_id="base",
        requested_stage="DRAFT_AND_VALIDATE",
        prepared_draft_task=draft_task,
        author_goal=(
            "这是原创小说 Genesis 首章。只使用已经选择的 candidate_id="
            f"{candidate_id}、contract_id={contract['contract_id']} 与 draft task_id="
            f"{draft_task['task_id']}；完成正文导入和十项校验，停在 VALIDATED。"
        ),
    )
    _update_registry(database, book_id, state=OriginalState.FIRST_CHAPTER_DRAFTING)
    return {
        "book_id": book_id,
        "candidate_id": candidate_id,
        "contract": contract,
        "draft_task": draft_task,
        "handoff": handoff,
        "canon_changed": False,
    }


def validate_original_draft(
    database: Database, book_id: str, draft_id: str
) -> dict[str, Any]:
    preview = approval_preview(database, book_id, draft_id, edition_id="base")
    if int(str(preview["chapter"])) != 1:
        raise OriginalWorkflowError("原创 Genesis 校验只接受第一章合同")
    bundle = validate_draft(database, book_id, draft_id, edition_id="base")
    if bundle.passed:
        _update_registry(database, book_id, state=OriginalState.FIRST_CHAPTER_VALIDATED)
    return bundle.model_dump(mode="json")


def approve_original_first_chapter(
    database: Database, book_id: str, draft_id: str, confirmation: str
) -> dict[str, Any]:
    preview = approval_preview(database, book_id, draft_id, edition_id="base")
    if int(str(preview["chapter"])) != 1:
        raise OriginalWorkflowError("原创 Genesis 批准只接受第一章合同")
    result = approve_draft(
        database,
        book_id,
        draft_id,
        confirmation=confirmation,
        edition_id="base",
    )
    _update_registry(
        database,
        book_id,
        state=OriginalState.WRITING,
        latest_chapter=1,
    )
    return {**result, "original_state": OriginalState.WRITING.value}


def original_overview(database: Database, book_id: str) -> dict[str, Any]:
    record = original_record(database, book_id)
    if record is None:
        raise OriginalWorkflowError("当前项目不是 ORIGINAL 小说")
    proposal = load_original_proposal(database, book_id)
    accepted = _read_json(
        _original_dir(database, book_id) / "story_foundation" / "accepted.json"
    )
    with database.connect() as connection:
        latest_task = "" if accepted is None else str(accepted.get("genesis_task_id") or "")
        candidates = [
            dict(row)
            for row in connection.execute(
                "SELECT candidate_id, rank, selection_status, plan_json FROM candidate_plans "
                "WHERE book_id=? AND edition_id='base' AND task_id=? ORDER BY rank",
                (book_id, latest_task),
            ).fetchall()
        ]
        for item in candidates:
            plan = json.loads(str(item.pop("plan_json")))
            item.update(
                {
                    "title": plan.get("title"),
                    "summary": plan.get("summary"),
                    "reader_question": plan.get("reader_question"),
                    "required_cost": plan.get("required_cost"),
                    "ending_state": plan.get("ending_state"),
                    "lens": plan.get("lens"),
                }
            )
        drafts = [
            dict(row)
            for row in connection.execute(
                "SELECT draft_id, status, chapter_title, file_path, created_at FROM drafts "
                "WHERE book_id=? AND edition_id='base' ORDER BY created_at DESC",
                (book_id,),
            ).fetchall()
        ]
        chapter_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM chapters WHERE book_id=?", (book_id,)
            ).fetchone()[0]
        )
        handoffs = [
            dict(row)
            for row in connection.execute(
                "SELECT handoff_id, handoff_type, requested_stage, status, prompt_path, "
                "created_at FROM workflow_handoffs WHERE book_id=? AND edition_id='base' "
                "ORDER BY created_at DESC LIMIT 5",
                (book_id,),
            ).fetchall()
        ]
    return {
        "book_id": book_id,
        "title": record.title,
        "original_state": record.original_state or OriginalState.ORIGINAL_SEED.value,
        "proposal": None if proposal is None else proposal.model_dump(mode="json"),
        "accepted": accepted,
        "candidates": candidates,
        "drafts": drafts,
        "chapter_count": chapter_count,
        "handoffs": handoffs,
        "foundation_confirmation": FOUNDATION_CONFIRMATION,
        "approval_confirmation": "批准写入正史",
    }


__all__ = [
    "OriginalWorkflowError",
    "approve_original_first_chapter",
    "confirm_original_foundation",
    "create_original_book",
    "import_original_bootstrap_proposal",
    "load_original_proposal",
    "original_overview",
    "prepare_original_bootstrap",
    "select_first_chapter_candidate",
    "validate_original_draft",
]
