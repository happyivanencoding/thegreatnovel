from __future__ import annotations

import json
from pathlib import Path

import pytest

from novel_authoring.canon.projection import CanonProjection
from novel_authoring.config import load_settings
from novel_authoring.continuation_quality import (
    ProgressionDelta,
    ProgressionDeltaKind,
    ReaderVisibleClaim,
    ReferenceApplication,
    UsageConstraint,
    progression_delta_issues,
    structural_overlap,
    usage_constraint_issues,
)
from novel_authoring.contracts.draft import (
    DraftCreativeOutput,
    DraftStateChange,
    SemanticPublicationReview,
)
from novel_authoring.db.database import Database
from novel_authoring.domain.models import ContinuationMode, NarrativeFunction
from novel_authoring.drafting.compiler import build_chapter_realization_brief
from novel_authoring.drafting.service import _healthy_realization_lengths
from novel_authoring.planning.experience_portfolio import (
    build_serial_experience_portfolio,
)
from novel_authoring.planning.models import (
    ChapterContract,
    ChapterExperienceSignature,
    PlanningReferenceProvenance,
    ReferenceApplicationStatus,
)
from novel_authoring.validation.validators import (
    ValidationContext,
    validate_canon,
    validate_character,
    validate_style,
)


def _contract() -> ChapterContract:
    return ChapterContract.model_construct(
        contract_id="quality-contract",
        chapter=3,
        mode=ContinuationMode.FAITHFUL,
        boundary_packet_id="quality-boundary",
        continuation_boundary={"base_event_seq": 1, "base_projection_hash": "p"},
        candidate_id="quality-candidate",
        primary_thread="thread",
        primary_function=NarrativeFunction.PROGRESS,
        secondary_functions=[],
        reader_question="what changes?",
        pressure={"before": 40, "target_after": 50},
        payoff_plan={},
        narrative_debt={"advance": [], "fully_pay": []},
        progress={},
        required_irreversible_change="state changes",
        required_cost="cost is visible",
        canon_constraints=[],
        knowledge_constraints=[],
        must_not_resolve=[],
        forbidden_repetitions=[],
        style_constraints={},
        ending_state="a consequence remains",
        commit_updates=["thread_status"],
        innovation_control={},
    )


@pytest.mark.parametrize(
    ("family", "subject", "axis", "period"),
    [
        ("survival_resource", "shelter", "supplies", "RESOURCE_GATED"),
        ("combat_cultivation", "technique", "mastery", "COMBAT_SCENE"),
        ("mystery_relationship", "alliance", "trust", "ONE_TIME"),
    ],
)
def test_same_quality_kernel_accepts_cross_family_shapes(
    family: str, subject: str, axis: str, period: str
) -> None:
    claim = ReaderVisibleClaim(
        claim_id=f"{family}-claim",
        subject_ref=subject,
        predicate="status",
        before_value="old",
        after_value="new",
        evidence_quote="the visible change",
        transition_source=f"{family}-change",
    )
    delta = ProgressionDelta(
        delta_id=f"{family}-delta",
        subject_ref=subject,
        axis=axis,
        kind=ProgressionDeltaKind.UPGRADE,
        before_state="old",
        after_state="new",
        reader_visible_delta="the reader sees a new option",
        opened_actions=["new option"],
        evidence_quotes=["the visible change"],
    )
    usage = UsageConstraint(
        constraint_id=f"{family}-usage",
        subject_ref=subject,
        action="use",
        period=period,
        limit=1 if period == "ONE_TIME" else None,
        resource_ref="resource" if period == "RESOURCE_GATED" else "",
        resource_cost=1 if period == "RESOURCE_GATED" else None,
    )

    assert claim.subject_ref == subject
    assert not progression_delta_issues([delta])
    if period == "RESOURCE_GATED":
        assert not usage_constraint_issues(usage, resource_quantity=1)
    else:
        assert not usage_constraint_issues(usage)


def test_reuse_is_not_upgrade_and_breakthrough_needs_visible_action_space() -> None:
    reuse = ProgressionDelta(
        delta_id="reuse",
        subject_ref="subject",
        axis="identity",
        kind=ProgressionDeltaKind.REUSE,
        before_state="same",
        after_state="same",
        reader_visible_delta="the same ability is used under pressure",
    )
    invalid_reuse = reuse.model_copy(
        update={
            "after_state": "new",
        }
    )
    invalid_breakthrough = reuse.model_copy(
        update={
            "delta_id": "breakthrough",
            "kind": ProgressionDeltaKind.BREAKTHROUGH,
            "after_state": "new",
        }
    )

    assert not progression_delta_issues([reuse])
    assert any(
        item.code == "PROGRESSION_REUSE_CHANGES_STATE"
        for item in progression_delta_issues([invalid_reuse])
    )
    assert any(
        item.code == "BREAKTHROUGH_ACTION_SPACE_UNCHANGED"
        for item in progression_delta_issues([invalid_breakthrough])
    )


def test_usage_does_not_reset_at_chapter_boundary() -> None:
    daily = UsageConstraint(
        constraint_id="daily",
        subject_ref="subject",
        action="observe",
        period="DAILY",
        limit=1,
        used_before=1,
        uses=1,
        reset_condition="rest_complete",
    )
    assert any(
        item.code == "PERIODIC_USAGE_LIMIT_EXCEEDED"
        for item in usage_constraint_issues(daily, reset_observed=False)
    )
    assert not usage_constraint_issues(daily, reset_observed=True)


@pytest.mark.parametrize(
    ("period", "limit", "used_before", "uses", "resource_quantity", "cost"),
    [
        ("DAILY", 1, 1, 1, None, None),
        ("COMBAT_SCENE", 1, 1, 1, None, None),
        ("ONE_TIME", 1, 1, 1, None, None),
        ("RESOURCE_GATED", None, 0, 1, 0, 1),
    ],
)
def test_usage_constraint_engine_covers_multiple_period_kinds(
    period: str,
    limit: int | None,
    used_before: int,
    uses: int,
    resource_quantity: float | None,
    cost: float | None,
) -> None:
    constraint = UsageConstraint(
        constraint_id=f"{period.lower()}-usage",
        subject_id="generic-subject",
        action_type="act",
        period_kind=period,
        period_id="period-1",
        limit=limit,
        used_before=used_before,
        uses=uses,
        resource_id="resource" if cost is not None else "",
        resource_cost=cost,
        reset_condition="explicit reset event",
    )
    issues = usage_constraint_issues(
        constraint,
        resource_quantity=resource_quantity,
        reset_observed=period == "RESOURCE_GATED" and resource_quantity == 0,
    )
    if period == "RESOURCE_GATED":
        assert any(item.code == "USAGE_RESOURCE_GATE_EXCEEDED" for item in issues)
    else:
        assert any(item.code == "PERIODIC_USAGE_LIMIT_EXCEEDED" for item in issues)


def test_usage_constraint_accepts_explicit_reset_and_used_count_alias() -> None:
    constraint = UsageConstraint(
        constraint_id="rest-reset",
        subject_id="capability",
        action_type="recover",
        period_kind="DAILY",
        period_id="day-2",
        limit=1,
        used_count=1,
        reset_condition="rest completed",
    )
    assert constraint.subject_id == "capability"
    assert not usage_constraint_issues(constraint, reset_observed=True)


def test_structural_overlap_detects_renamed_surface_labels() -> None:
    candidate = {
        "opposition_source": "resource scarcity",
        "primary_subject": "shelter",
        "choice_type": "spend reserve",
        "cost_type": "future shortage",
        "payoff_channel": "escape",
        "progression_delta_type": "REUSE",
        "scene_topology": "ACTION",
        "ending_mode": "CONSEQUENCE",
    }
    recent = {
        **candidate,
        "primary_subject": "a different named location",
        "event_source": "a different label",
    }
    overlap = structural_overlap(candidate, recent)
    assert overlap["repeated"] is True
    assert "choice_type" in overlap["critical_same_dimensions"]


def test_structural_overlap_allows_same_subject_when_method_and_payoff_change() -> None:
    candidate = {
        "primary_subject": "mystery",
        "solution_method": "witness interview",
        "payoff_channel": "knowledge confirmation",
        "ending_action": "confront ally",
        "opposition_source": "institution",
        "progression_delta_type": "KNOWLEDGE_UPDATE",
    }
    recent = {
        **candidate,
        "solution_method": "document comparison",
        "payoff_channel": "relationship rupture",
        "ending_action": "protect witness",
        "progression_delta_type": "RELATIONSHIP_SHIFT",
    }
    assert structural_overlap(candidate, recent)["repeated"] is False


def test_serial_experience_portfolio_uses_configured_horizons() -> None:
    signatures = [
        ChapterExperienceSignature(
            chapter_ordinal=10,
            opposition_source="scarcity",
            primary_subject="shelter",
            choice_type="spend",
            payoff_channel="escape",
        ),
        ChapterExperienceSignature(
            chapter_ordinal=1,
            opposition_source="scarcity",
            primary_subject="another place",
            choice_type="spend",
            payoff_channel="escape",
        ),
    ]
    portfolio = build_serial_experience_portfolio(
        signatures,
        current_chapter=10,
        horizon_policy={"SHORT": 0, "MID": 20, "LONG": 100},
    )
    assert portfolio.horizon_counts == {"SHORT": 1, "MID": 1}
    assert portfolio.unknown_horizon_count == 0
    assert portfolio.repeated_structure_pairs


def test_reference_provenance_separates_offered_and_applied() -> None:
    offered = PlanningReferenceProvenance(card_ids_used=["card-1"])
    applied = PlanningReferenceProvenance(
        card_ids_used=["card-1"],
        application_status=ReferenceApplicationStatus.APPLIED,
        applied_dimensions=["choice_type"],
        application_evidence=["作者声明采用 choice_type"],
    )
    assert offered.application_status is ReferenceApplicationStatus.OFFERED
    assert applied.application_status is ReferenceApplicationStatus.APPLIED
    assert ReferenceApplication(
        summary="采用结构机制",
        applied_dimensions=["choice_type"],
        evidence=["作者声明采用 choice_type"],
    ).summary


def test_reference_provenance_supports_unavailable_and_zero_results() -> None:
    from novel_authoring.planning.models import ReferenceApplicationStatus

    assert (
        PlanningReferenceProvenance(application_status=ReferenceApplicationStatus.UNAVAILABLE)
        .application_status
        is ReferenceApplicationStatus.UNAVAILABLE
    )
    assert (
        PlanningReferenceProvenance(application_status=ReferenceApplicationStatus.ZERO_RESULTS)
        .application_status
        is ReferenceApplicationStatus.ZERO_RESULTS
    )


def test_reference_application_evidence_must_point_to_frozen_cards() -> None:
    from novel_authoring.planning.candidates import _reference_evidence_matches_frozen

    context = {
        "compact_cards": [
            {
                "card_id": "card-1",
                "solutions": [{"solution_id": "solution-1", "label": "bounded choice"}],
            }
        ]
    }
    strategy = {"selected_cards": context["compact_cards"]}
    assert _reference_evidence_matches_frozen(["card-1"], context, strategy)
    assert _reference_evidence_matches_frozen(["bounded choice"], context, strategy)
    assert not _reference_evidence_matches_frozen(["invented mechanism"], context, strategy)


def test_compiled_soft_output_has_no_pseudo_character_or_style_scores() -> None:
    creative = DraftCreativeOutput(
        task_id="quality-task",
        contract_id="contract-1",
        chapter_title="质量测试",
        prose_markdown="门被推开。新的道路出现在读者面前。",
        state_changes=[
            {
                "kind": "fact",
                "record_id": "fact-1",
                "payload": {
                    "predicate": "status",
                    "object": "open",
                    "statement": "门被推开",
                },
            }
        ],
    )
    from novel_authoring.drafting.compiler import compile_draft_output

    compiled = compile_draft_output(creative, _contract())
    assert compiled.evidence_policy == "COMPILED_SOFT"
    assert compiled.character_fit_inputs == {}
    assert compiled.style_fit_inputs == {}
    assert compiled.semantic_review_status == "UNKNOWN"
    assert compiled.deterministic_measurements["sentence_count"] > 0


def test_compiler_binds_descriptive_commit_updates_to_state_change_evidence() -> None:
    from novel_authoring.drafting.compiler import _contract_evidence

    contract = _contract().model_copy(
        update={
            "commit_updates": [
                "thread status advances: 资格记录进入下一场复核",
                "character state changes: 主角主动争取正式挑战资格",
                "social status changes: 记录者开始将主角视为待验证竞争者",
            ]
        }
    )
    changes = [
        DraftStateChange(
            kind="thread",
            record_id="thread",
            payload={},
            evidence_quotes=["资格记录进入下一场复核"],
        ),
        DraftStateChange(
            kind="character_state",
            record_id="character",
            payload={},
            evidence_quotes=["主角主动争取正式挑战资格"],
        ),
        DraftStateChange(
            kind="fact",
            record_id="social",
            payload={},
            evidence_quotes=["记录者开始将主角视为待验证竞争者"],
        ),
    ]
    evidence = _contract_evidence(
        "资格记录进入下一场复核。主角主动争取正式挑战资格。"
        "记录者开始将主角视为待验证竞争者。",
        contract,
        changes,
    )
    assert all(evidence["commit:" + key] for key in contract.commit_updates)


def test_independent_publication_review_catches_creative_omission_and_contradiction() -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    creative = DraftCreativeOutput(
        task_id="publication-review-task",
        contract_id="quality-contract",
        chapter_title="独立审阅",
        prose_markdown="X 已经打开。",
        state_changes=[
            {"kind": "fact", "record_id": "scene", "payload": {"statement": "X 已经打开"}}
        ],
        reader_visible_claims=[],
    )
    review = SemanticPublicationReview(
        task_id=creative.task_id,
        contract_id=creative.contract_id,
        status="REVIEWED",
        reader_visible_claims=[
            ReaderVisibleClaim(
                claim_id="review-x-open",
                subject_ref="X",
                predicate="state",
                value="OPEN",
                evidence_quote="X 已经打开",
            )
        ],
    )
    compiled = compile_draft_output(
        creative,
        _contract(),
        publication_review=review,
        semantic_review_required=True,
    )
    context = ValidationContext(
        draft=compiled,
        contract=_contract(),
        projection=CanonProjection(
            book_id="quality-book",
            entities={"X": {"state": "CLOSED"}},
        ),
        settings=load_settings(),
    )
    codes = {item.code for item in validate_canon(context).findings}
    assert compiled.semantic_review_status == "REVIEWED"
    assert compiled.publication_review_claims
    assert "STATE_CONTRADICTION" in codes
    assert validate_character(context).measurements["semantic_review_status"] == "REVIEWED"
    assert validate_style(context).measurements["semantic_review_status"] == "REVIEWED"


def test_publication_review_and_creative_claims_are_deduplicated_when_consistent() -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    claim = ReaderVisibleClaim(
        claim_id="same-fact",
        subject_ref="door",
        predicate="state",
        value="OPEN",
        evidence_quote="门开了",
    )
    creative = DraftCreativeOutput(
        task_id="publication-dedupe-task",
        contract_id="quality-contract",
        chapter_title="去重",
        prose_markdown="门开了。",
        state_changes=[
            {"kind": "fact", "record_id": "door-change", "payload": {"statement": "门开了"}}
        ],
        reader_visible_claims=[claim],
    )
    review = SemanticPublicationReview(
        task_id=creative.task_id,
        contract_id=creative.contract_id,
        status="REVIEWED",
        reader_visible_claims=[claim.model_copy(update={"claim_id": "review-same-fact"})],
    )
    compiled = compile_draft_output(
        creative,
        _contract(),
        publication_review=review,
        semantic_review_required=True,
    )
    assert len(compiled.reader_visible_claims) == 1
    assert len(compiled.publication_review_claims) == 1
    assert not any(
        item.code == "PUBLICATION_REVIEW_CLAIM_CONFLICT"
        for item in validate_canon(
            ValidationContext(
                draft=compiled,
                contract=_contract(),
                projection=CanonProjection(book_id="quality-book"),
                settings=load_settings(),
            )
        ).findings
    )


def test_publication_review_evidence_must_be_in_finished_prose() -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    creative = DraftCreativeOutput(
        task_id="publication-evidence-task",
        contract_id="quality-contract",
        chapter_title="证据",
        prose_markdown="他转身离开。",
        state_changes=[
            {"kind": "fact", "record_id": "scene", "payload": {"statement": "他转身离开"}}
        ],
    )
    review = SemanticPublicationReview(
        task_id=creative.task_id,
        contract_id=creative.contract_id,
        status="REVIEWED",
        reader_visible_claims=[
            ReaderVisibleClaim(
                claim_id="missing-quote",
                subject_ref="door",
                predicate="state",
                value="OPEN",
                evidence_quote="正文不存在的证据",
            )
        ],
    )
    compiled = compile_draft_output(
        creative,
        _contract(),
        publication_review=review,
        semantic_review_required=True,
    )
    codes = {
        item.code
        for item in validate_canon(
            ValidationContext(
                draft=compiled,
                contract=_contract(),
                projection=CanonProjection(book_id="quality-book"),
                settings=load_settings(),
            )
        ).findings
    }
    assert "PUBLICATION_REVIEW_EVIDENCE_NOT_FOUND" in codes


def test_reviewed_publication_pass_can_legitimately_find_no_high_value_claims() -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    creative = DraftCreativeOutput(
        task_id="publication-empty-task",
        contract_id="quality-contract",
        chapter_title="纯动作",
        prose_markdown="他抬手，挡住迎面而来的雨。",
        state_changes=[
            {"kind": "fact", "record_id": "scene", "payload": {"statement": "他挡住雨"}}
        ],
    )
    review = SemanticPublicationReview(
        task_id=creative.task_id,
        contract_id=creative.contract_id,
        status="REVIEWED",
        reader_visible_claims=[],
        publication_review_findings=[],
    )
    compiled = compile_draft_output(
        creative,
        _contract(),
        publication_review=review,
        semantic_review_required=True,
    )
    codes = {
        item.code
        for item in validate_canon(
            ValidationContext(
                draft=compiled,
                contract=_contract(),
                projection=CanonProjection(book_id="quality-book"),
                settings=load_settings(),
            )
        ).findings
    }
    assert compiled.semantic_review_status == "REVIEWED"
    assert compiled.reader_visible_claims == []
    assert "SEMANTIC_PUBLICATION_REVIEW_REQUIRED" not in codes


def test_reader_visible_claim_is_checked_against_projection_before_state() -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    creative = DraftCreativeOutput(
        task_id="claim-task",
        contract_id="quality-contract",
        chapter_title="声明测试",
        prose_markdown="资源从两份变成一份。",
        state_changes=[
            {
                "kind": "resource",
                "record_id": "resource-change",
                "payload": {
                    "owner_id": "subject",
                    "name": "resource",
                    "quantity": 1,
                    "statement": "资源从两份变成一份",
                },
            }
        ],
        reader_visible_claims=[
            ReaderVisibleClaim(
                claim_id="quantity-change",
                subject_ref="resource",
                predicate="quantity",
                before_value=2,
                after_value=1,
                evidence_quote="资源从两份变成一份",
                transition_source="resource-change",
            )
        ],
    )
    compiled = compile_draft_output(creative, _contract())
    context = ValidationContext(
        draft=compiled,
        contract=_contract(),
        projection=CanonProjection(
            book_id="quality-book",
            resources={"resource": {"resource_id": "resource", "quantity": 2}},
        ),
        settings=load_settings(),
    )
    assert not any(
        item.code == "STATE_CONTRADICTION"
        for item in validate_canon(context).findings
    )
    bad = compiled.model_copy(
        update={
            "reader_visible_claims": [
                compiled.reader_visible_claims[0].model_copy(update={"before_value": 3})
            ]
        }
    )
    bad_context = context.__class__(
        draft=bad,
        contract=context.contract,
        projection=context.projection,
        settings=context.settings,
    )
    assert any(
        item.code == "STATE_CONTRADICTION"
        for item in validate_canon(bad_context).findings
    )
    outside_context = context.__class__(
        draft=compiled,
        contract=context.contract.model_copy(update={"state_change_record_ids": ["other"]}),
        projection=context.projection,
        settings=context.settings,
    )
    assert any(
        item.code == "READER_VISIBLE_CLAIM_OUTSIDE_CONTRACT"
        for item in validate_canon(outside_context).findings
    )


def test_reader_visible_claim_reports_quantity_source_and_internal_language_leaks() -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    creative = DraftCreativeOutput(
        task_id="claim-source-task",
        contract_id="quality-contract",
        chapter_title="声明来源测试",
        prose_markdown="state_changes: quantity changed. ChapterContract was exposed.",
        state_changes=[
            {
                "kind": "resource",
                "record_id": "quantity-change",
                "payload": {"quantity": 3},
            }
        ],
        reader_visible_claims=[
            ReaderVisibleClaim(
                claim_id="quantity-jump",
                subject_ref="resource",
                predicate="quantity",
                claim_kind="QUANTITY",
                before_value=1,
                after_value=3,
                evidence_quote="quantity changed",
                transition_source="quantity-change",
            )
        ],
    )
    compiled = compile_draft_output(creative, _contract())
    context = ValidationContext(
        draft=compiled,
        contract=_contract(),
        projection=CanonProjection(
            book_id="quality-book",
            resources={"resource": {"resource_id": "resource", "quantity": 1}},
        ),
        settings=load_settings(),
    )
    codes = {item.code for item in validate_canon(context).findings}
    assert "QUANTITY_JUMP_WITHOUT_SOURCE" in codes
    assert "INTERNAL_WORKFLOW_LANGUAGE_LEAK" in codes


@pytest.mark.parametrize(
    ("claim_kind", "code"),
    [
        ("LOCATION", "LOCATION_CHANGE_WITHOUT_TRANSITION"),
        ("OWNERSHIP", "OWNERSHIP_CHANGE_WITHOUT_EVENT"),
        ("TEMPORAL_STATE", "TEMPORAL_RESET_WITHOUT_TRANSITION"),
    ],
)
def test_reader_visible_unbound_state_changes_use_generic_conflict_codes(
    claim_kind: str, code: str
) -> None:
    from novel_authoring.drafting.compiler import compile_draft_output

    creative = DraftCreativeOutput(
        task_id=f"{claim_kind.lower()}-claim-task",
        contract_id="quality-contract",
        chapter_title="通用声明冲突",
        prose_markdown="状态从旧值变为新值。",
        state_changes=[
            {
                "kind": "fact",
                "record_id": f"{claim_kind.lower()}-change",
                "payload": {"statement": "状态从旧值变为新值"},
            }
        ],
        reader_visible_claims=[
            ReaderVisibleClaim(
                claim_id=f"{claim_kind.lower()}-claim",
                subject_ref="subject",
                predicate="state",
                claim_kind=claim_kind,
                before_value="old",
                after_value="new",
                evidence_quote="状态从旧值变为新值",
            )
        ],
    )
    context = ValidationContext(
        draft=compile_draft_output(creative, _contract()),
        contract=_contract(),
        projection=CanonProjection(book_id="quality-book"),
        settings=load_settings(),
    )
    assert code in {item.code for item in validate_canon(context).findings}


def test_progression_reuse_cannot_advance_progression_index() -> None:
    from novel_authoring.contracts.draft import DraftOutput
    from novel_authoring.validation.validators import validate_economy_power

    draft = DraftOutput(
        task_id="progression-index-task",
        contract_id="quality-contract",
        chapter_title="复用测试",
        prose_markdown="同一能力再次使用。",
        state_changes=[
            {
                "kind": "capability",
                "record_id": "capability-change",
                "payload": {
                    "progression": {
                        "before_index": 1,
                        "after_index": 2,
                        "deltas": [
                            {
                                "delta_id": "reuse-index",
                                "subject_id": "capability",
                                "axis_id": "mastery",
                                "delta_type": "REUSE",
                                "before_state": "same",
                                "after_state": "same",
                                "reader_visible_delta": "same capability under pressure",
                            }
                        ],
                    }
                },
            }
        ],
    )
    report = validate_economy_power(
        ValidationContext(
            draft=draft,
            contract=_contract(),
            projection=CanonProjection(book_id="quality-book"),
            settings=load_settings(),
        )
    )
    assert any(item.code == "PROGRESSION_REUSE_ADVANCES_INDEX" for item in report.findings)


def test_contract_realization_underspecified_returns_to_planning() -> None:
    from novel_authoring.contracts.draft import ChapterRealizationBrief
    from novel_authoring.drafting.compiler import diagnose_scene_realization

    result = diagnose_scene_realization(
        "他抬手。",
        ChapterRealizationBrief(contract_realization_status="UNDERSPECIFIED"),
    )
    assert result["code"] == "CONTRACT_REALIZATION_UNDERSPECIFIED"


def test_thin_realization_does_not_lower_the_healthy_baseline(tmp_path: Path) -> None:
    database = Database(tmp_path / "baseline.sqlite3")
    database.initialize()
    clear_prose = "健康章节。" * 20
    accepted_prose = "作者接受的短章。"
    thin_prose = "薄章。"
    rows = [
        ("clear", clear_prose, {"code": "SCENE_REALIZATION_CLEAR"}, "VALIDATED"),
        (
            "accepted",
            accepted_prose,
            {"code": "SCENE_REALIZATION_THIN", "status": "ACCEPTED"},
            "CANON_COMMITTED",
        ),
        ("thin", thin_prose, {"code": "SCENE_REALIZATION_THIN"}, "CANON_COMMITTED"),
    ]
    with database.connect() as connection:
        for draft_id, prose, diagnostics, status in rows:
            connection.execute(
                """
                INSERT INTO drafts(
                    draft_id, book_id, contract_id, file_path, content_sha256,
                    status, revision, created_at, edition_id, output_json
                ) VALUES (?, 'baseline-book', 'contract', ?, 'hash', ?, 1, ?, 'base', ?)
                """,
                (
                    draft_id,
                    str(tmp_path / f"{draft_id}.md"),
                    status,
                    draft_id,
                    json.dumps(
                        {
                            "prose_markdown": prose,
                            "realization_diagnostics": diagnostics,
                            "intentional_short_chapter": draft_id == "accepted",
                        }
                    ),
                ),
            )
    lengths = _healthy_realization_lengths(database, "baseline-book", "base")
    assert len(clear_prose) in lengths
    assert len(accepted_prose) in lengths
    assert len(thin_prose) not in lengths
    brief = build_chapter_realization_brief(_contract(), recent_lengths=lengths)
    assert brief.target_word_range[0] > len(thin_prose)


def test_no_history_realization_brief_has_unknown_baseline() -> None:
    brief = build_chapter_realization_brief(_contract(), recent_lengths=[])
    assert brief.target_word_range == (0, 0)
    assert brief.adaptive is False
