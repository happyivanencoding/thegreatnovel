from __future__ import annotations

import json

from novel_authoring.db.database import Database
from novel_authoring.domain.models import ContinuationMode
from novel_authoring.edition import edition_workspace, resolve_edition_id
from novel_authoring.planning.boundary import PlanningError
from novel_authoring.planning.innovation import (
    InnovationCommitments,
    InnovationControl,
    NarrativePortfolioSnapshot,
)
from novel_authoring.planning.models import CandidateProposal, ChapterContract
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.operations import book_root, find_operation
from novel_authoring.utils import json_dumps, sha256_bytes, stable_id, utc_now


def build_chapter_contract(
    database: Database,
    book_id: str,
    candidate_id: str,
    *,
    edition_id: str | None = None,
) -> dict[str, object]:
    selected_edition = resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM candidate_plans WHERE book_id=? AND candidate_id=? AND edition_id=?",
            (book_id, candidate_id, selected_edition),
        ).fetchone()
        if row is None:
            raise PlanningError(f"候选不存在：{candidate_id}")
        if row["selection_status"] == "REJECTED":
            raise PlanningError("被硬门拒绝的候选不能生成章节合同")
        task_id = str(row["task_id"])
        book_row = connection.execute(
            "SELECT mode FROM books WHERE book_id=?", (book_id,)
        ).fetchone()
    workspace = edition_workspace(database, book_id, selected_edition)
    root = book_root(database, book_id)
    operation = find_operation(database, book_id, selected_edition, task_id)
    task_path = (
        operation.input / "task.json"
        if operation is not None
        else workspace / "agent_tasks" / task_id / "task.json"
    )
    task_metadata = json.loads(task_path.read_text(encoding="utf-8"))
    aggregate_id = str(task_metadata.get("aggregate_id") or "")
    if aggregate_id:
        with database.connect() as connection:
            aggregate = connection.execute(
                "SELECT status, bundle_hash, author_policy_json FROM planning_aggregates "
                "WHERE aggregate_id=? AND book_id=? AND edition_id=?",
                (aggregate_id, book_id, selected_edition),
            ).fetchone()
        if aggregate is None or str(aggregate["status"]) != "ACTIVE":
            raise PlanningError("Planning Aggregate 已失效，不能生成 Chapter Contract")
        expected_hash = str(
            task_metadata.get("aggregate_hash") or task_metadata.get("bundle_hash") or ""
        )
        if expected_hash and str(aggregate["bundle_hash"]) != expected_hash:
            raise PlanningError("Planning Aggregate hash 与候选任务冻结值不一致")
        aggregate_policy = json.loads(str(aggregate["author_policy_json"] or "{}"))
        if task_metadata.get("truth_reveal", {}) != aggregate_policy.get(
            "truth_reveal", {}
        ):
            raise PlanningError("Truth/Reveal 冻结快照已漂移，不能生成合同")
    packet_id = str(task_metadata["boundary_packet_id"])
    boundary_dir = (
        BookLayout(root.parent).for_book(book_id).edition(selected_edition).boundaries
        if (root / "book.yaml").is_file()
        else workspace / "boundaries"
    )
    boundary_json = json.loads(
        (boundary_dir / f"{packet_id}.json").read_text(encoding="utf-8")
    )
    candidate = CandidateProposal.model_validate_json(str(row["plan_json"]))
    score_payload = json.loads(str(row["score_json"] or "{}"))
    kernel_compilation = score_payload.get("kernel_evidence_compilation")
    declared_kernel_trace: dict[str, object] = {}
    verified_kernel_trace: dict[str, object] = {}
    kernel_verification_status = "LEGACY_NO_EFFECTIVE_CONTRACT"
    if isinstance(kernel_compilation, dict):
        declared_raw = kernel_compilation.get("declared", {})
        verified_raw = kernel_compilation.get("verified", {})
        declared_kernel_trace = (
            dict(declared_raw) if isinstance(declared_raw, dict) else {}
        )
        verified_kernel_trace = (
            dict(verified_raw) if isinstance(verified_raw, dict) else {}
        )
        verified_kernel_trace["evidence_compilation"] = kernel_compilation
        kernel_verification_status = str(
            kernel_compilation.get("completeness") or "UNKNOWN"
        )
    innovation_control = InnovationControl.model_validate(
        task_metadata.get("innovation_control", {})
    )
    portfolio_raw = task_metadata.get("narrative_portfolio_snapshot")
    narrative_portfolio = (
        NarrativePortfolioSnapshot.model_validate(portfolio_raw)
        if portfolio_raw is not None
        else None
    )
    next_chapter = int(boundary_json["current_position"]["next_chapter"])
    truth_reveal = dict(task_metadata.get("truth_reveal", {}))
    if not truth_reveal:
        truth_reveal = {
            "target_chapter_ordinal": next_chapter,
            "active_author_truths": list(
                boundary_json.get("active_author_truths", [])
            ),
            "reveal_agenda": dict(boundary_json.get("reveal_agenda", {})),
        }
    rhythm_diagnostics = dict(boundary_json.get("rhythm_diagnostics", {}))
    rhythm_constraints: dict[str, object] = {}
    function_streak = rhythm_diagnostics.get("same_function_streak", {})
    if function_streak.get("severity") == "STRONG_WARNING":
        rhythm_constraints["change_primary_function_or_pressure_shape"] = True
    ending_streak = rhythm_diagnostics.get("ending_mode_streak", {})
    if ending_streak.get("severity") == "STRONG_WARNING":
        rhythm_constraints["avoid_repeated_ending_mode"] = ending_streak.get("mode")
    hooks = boundary_json.get("hook_diagnostics", {})
    rhythm_constraints["advance_due_promises"] = [
        item.get("promise_id") for item in hooks.get("advance_due", [])
    ]
    rhythm_constraints["resolve_due_promises"] = [
        item.get("promise_id") for item in hooks.get("resolve_due", [])
    ]
    contract_seed = {
        "candidate_id": candidate_id,
        "packet_id": packet_id,
        "next_chapter": next_chapter,
        "projection": boundary_json["base_projection_hash"],
        "story_atlas_anchor": boundary_json.get("story_atlas_anchor", {}),
        "batch_anchor": boundary_json.get("batch_anchor", {}),
        "book_profile_version": task_metadata.get("effective_book_profile", {}).get(
            "profile_version_id"
        ),
        "active_truth_ids": [
            item.get("truth_id")
            for item in truth_reveal.get("active_author_truths", [])
        ],
        "reveal_agenda_chapter": truth_reveal.get("target_chapter_ordinal"),
        "truth_reveal_snapshot": truth_reveal,
    }
    contract_id = stable_id("contract", json_dumps(contract_seed))
    innovation_commitments = InnovationCommitments()
    if candidate.innovation_preview is not None:
        preview = candidate.innovation_preview
        innovation_commitments = InnovationCommitments(
            expected_innovation_elements=preview.expected_innovation_elements,
            expected_element_synergies=preview.expected_element_synergies,
            expected_horizon_roles=preview.expected_horizon_roles,
            expected_cross_horizon_synergies=preview.expected_cross_horizon_synergies,
            expected_payoffs=preview.expected_payoffs,
            expected_new_debts=preview.expected_new_debts,
            expected_future_options_opened=preview.future_options_opened,
            minimum_meaningful_delta=preview.expected_narrative_delta,
        )
    contract = ChapterContract(
        contract_id=contract_id,
        chapter=next_chapter,
        mode=ContinuationMode(str(book_row["mode"])),
        boundary_packet_id=packet_id,
        continuation_boundary={
            "last_canon_chapter": boundary_json["current_position"]["last_canon_chapter"],
            "base_event_seq": boundary_json["base_event_seq"],
            "base_projection_hash": boundary_json["base_projection_hash"],
            "story_atlas_anchor": boundary_json.get("story_atlas_anchor", {}),
            "batch_anchor": boundary_json.get("batch_anchor", {}),
        },
        candidate_id=candidate_id,
        primary_thread=candidate.primary_thread_id,
        primary_function=candidate.primary_function,
        secondary_functions=candidate.secondary_functions,
        reader_question=candidate.reader_question,
        pressure={
            "before": candidate.pressure_before,
            "target_after": candidate.pressure_target_after,
        },
        payoff_plan={
            "causal_sources": candidate.causal_sources,
            "state_changes": candidate.state_changes,
            "must_change_behavior": candidate.commit_updates,
        },
        narrative_debt={
            "advance": candidate.promises_to_advance,
            "fully_pay": candidate.promises_to_pay,
            "new_major_hooks_allowed": 1,
        },
        progress={
            "minimum_score": 25,
            "required_irreversible_change": candidate.required_irreversible_change,
        },
        required_irreversible_change=candidate.required_irreversible_change,
        required_cost=candidate.required_cost,
        canon_constraints=candidate.canon_constraints,
        knowledge_constraints=candidate.knowledge_constraints,
        must_not_resolve=candidate.must_not_resolve,
        forbidden_repetitions=candidate.forbidden_repetitions,
        style_constraints=candidate.style_constraints,
        ending_state=candidate.ending_state,
        commit_updates=candidate.commit_updates,
        rhythm_constraints=rhythm_constraints,
        lens=candidate.lens,
        novelty_provenance=candidate.novelty_provenance,
        innovation_control=innovation_control,
        innovation_preview=candidate.innovation_preview,
        innovation_commitments=innovation_commitments,
        narrative_portfolio=narrative_portfolio,
        effective_book_profile=dict(task_metadata.get("effective_book_profile", {})),
        active_author_truths=list(truth_reveal.get("active_author_truths", [])),
        reveal_agenda=dict(truth_reveal.get("reveal_agenda", {})),
        truth_reveal_commitments={
            "truth_alignment": [
                item.model_dump(mode="json") for item in candidate.truth_alignment
            ],
            "reveal_impact": candidate.reveal_impact.model_dump(mode="json"),
            "rule": (
                "Hidden Truth 只作为行为约束；未获 Agenda 授权不得向读者或角色揭示。"
            ),
        },
        reader_promise_alignment=candidate.reader_promise_alignment,
        genre_alignment=candidate.genre_alignment,
        narrative_drive_alignment=candidate.narrative_drive_alignment,
        progress_preview=candidate.progress_preview,
        progression_impact=candidate.progression_impact,
        payoff_channel_impact=candidate.payoff_channel_impact,
        world_expansion_impact=candidate.world_expansion_impact,
        resource_opportunity_impact=candidate.resource_opportunity_impact,
        chapter_intent=candidate.chapter_intent,
        scheduler_alignment=candidate.scheduler_alignment,
        progression_debt_impact=candidate.progression_debt_impact,
        anticipation_impact=candidate.anticipation_impact,
        genre_drift_diagnostic=candidate.genre_drift_diagnostic,
        genre_evolution_diagnostic=candidate.genre_evolution_diagnostic,
        narrative_drive_drift_diagnostic=candidate.narrative_drive_drift_diagnostic,
        declared_kernel_trace=declared_kernel_trace,
        verified_kernel_trace=verified_kernel_trace,
        kernel_verification_status=kernel_verification_status,
    )
    contract_json = json_dumps(contract.model_dump(mode="json"), indent=2)
    contract_hash = sha256_bytes(contract_json.encode())
    contracts_dir = (
        BookLayout(root.parent).for_book(book_id).edition(selected_edition).contracts
        if (root / "book.yaml").is_file()
        else workspace / "contracts"
    )
    contracts_dir.mkdir(parents=True, exist_ok=True)
    path = contracts_dir / f"{contract_id}.json"
    path.write_text(contract_json + "\n", encoding="utf-8")
    with database.connect() as connection:
        candidate_anchor = connection.execute(
            "SELECT metric_run_id, metric_bundle_hash, rhythm_snapshot_id, registry_hash, "
            "config_hash, aggregate_id "
            "FROM candidate_plans WHERE book_id=? AND candidate_id=? AND edition_id=?",
            (book_id, candidate_id, selected_edition),
        ).fetchone()
        connection.execute(
            """
            INSERT OR REPLACE INTO chapter_contracts(
                contract_id, book_id, candidate_id, target_chapter_ordinal,
                mode, contract_json, contract_sha256, status, created_at, version
                , edition_id, metric_run_id, metric_bundle_hash, rhythm_snapshot_id,
                registry_hash, config_hash, aggregate_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'READY', ?, 1, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                contract_id,
                book_id,
                candidate_id,
                next_chapter,
                contract.mode.value,
                contract_json,
                contract_hash,
                utc_now(),
                selected_edition,
                None if candidate_anchor is None else candidate_anchor["metric_run_id"],
                None if candidate_anchor is None else candidate_anchor["metric_bundle_hash"],
                None if candidate_anchor is None else candidate_anchor["rhythm_snapshot_id"],
                None if candidate_anchor is None else candidate_anchor["registry_hash"],
                None if candidate_anchor is None else candidate_anchor["config_hash"],
                None if candidate_anchor is None else candidate_anchor["aggregate_id"],
            ),
        )
    return {
        "contract_id": contract_id,
        "path": str(path),
        "sha256": contract_hash,
        "candidate_id": candidate_id,
        "chapter": next_chapter,
    }
