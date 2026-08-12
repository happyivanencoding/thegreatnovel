from __future__ import annotations

from novel_authoring.config import load_settings
from novel_authoring.domain.models import NarrativeFunction
from novel_authoring.metrics.formulas import progress
from novel_authoring.planning.models import (
    CandidateProposal,
    CandidateScoreInputs,
    NarrativeDriveAlignment,
    ProgressionImpact,
    ReaderPromiseAlignment,
    ReaderPromiseService,
    SchedulerAlignment,
)
from novel_authoring.progression.context import (
    EffectiveKernelContracts,
    KernelAuthorState,
    KernelChapterState,
    KernelCoverage,
    KernelPlanningContext,
    KernelPlanningState,
    KernelWorldStateReference,
)
from novel_authoring.progression.evidence import (
    EvidenceCompleteness,
    KernelEvidenceCompiler,
)


def _context() -> KernelPlanningContext:
    return KernelPlanningContext(
        book_id="kernel-book",
        edition_id="base",
        target_chapter_ordinal=3,
        context_chapter_id="chapter-2",
        context_chapter_ordinal=2,
        effective_contracts=EffectiveKernelContracts(
            reader_experience={
                "must_deliver": ["成长改变行动空间"],
                "experience_priorities": {"RESOURCE_OPPORTUNITY": "HIGH"},
            },
            narrative_drive={
                "primary_drive": "POWER_PROGRESSION",
                "secondary_drives": ["WORLD_EXPLORATION"],
            },
            genre={
                "genre_promises": [
                    {
                        "promise_id": "promise-growth",
                        "statement": "成长改变行动空间",
                        "strength": "CORE",
                    }
                ]
            },
            progression={
                "allowed_delta_types": ["ADVANCE"],
                "primary_axis": {
                    "axis_id": "body-axis",
                    "stage_order": ["stage-one", "stage-two"],
                    "stage_definitions": [
                        {
                            "stage_id": "stage-one",
                            "name": "初段",
                            "status": "AVAILABLE",
                            "next_stage_candidates": ["stage-two"],
                        },
                        {
                            "stage_id": "stage-two",
                            "name": "二段",
                            "status": "AVAILABLE",
                            "next_stage_candidates": [],
                        },
                    ],
                },
                "secondary_axes": [],
                "ability_unlock_model": [],
            },
            payoff_channel={"channels": {"POWER_BREAKTHROUGH": "CORE"}},
        ),
        chapter_state=KernelChapterState(
            world_state_reference=KernelWorldStateReference(
                chapter_id="chapter-2",
                chapter_ordinal=2,
                availability="SOURCE_CHAPTER_STATE_PROJECTION",
            ),
            progression_state={
                "primary_axis_state": {
                    "current_stage": "stage-one",
                    "current_bottlenecks": [],
                },
                "next_breakthrough_readiness": "READY_TO_ATTEMPT",
                "missing_resources": [],
            },
            resource_state=[{"resource_id": "ore-heart", "name": "矿心"}],
            opportunity_surface={
                "items": [{"opportunity_id": "rumor", "subject": "远方遗迹"}]
            },
        ),
        planning_state=KernelPlanningState(
            narrative_debts=[{"debt_id": "debt-growth", "debt_score": 82}],
            active_threads=[{"thread_id": "thread-growth"}],
        ),
        author_state=KernelAuthorState(),
        coverage=KernelCoverage(known=["progression_state"]),
    )


def _candidate() -> CandidateProposal:
    score_inputs = CandidateScoreInputs(
        thread_need_fit=1,
        pressure_curve_fit=50,
        debt_utility=1,
        progress_gain=100,
        payoff_or_setup_utility=1,
        agency_gain=1,
        risk_fit=1,
        structural_diversity=50,
        style_fit=50,
        repetition_fatigue=0,
        future_damage=99,
    )
    return CandidateProposal.model_construct(
        local_id="candidate-one",
        primary_thread_id="thread-growth",
        primary_function=NarrativeFunction.PROGRESS,
        reader_promise_alignment=[
            ReaderPromiseAlignment(
                promise_id="promise-growth",
                priority="CORE",
                service=ReaderPromiseService.SERVED,
                evidence=["合法阶段推进"],
            )
        ],
        narrative_drive_alignment=NarrativeDriveAlignment(
            primary_drive="POWER_PROGRESSION",
            primary_drive_effect="阶段变化",
            drives_advanced=["POWER_PROGRESSION"],
            evidence=["stage-one -> stage-two"],
        ),
        progression_impact=ProgressionImpact(
            axis_advanced=["body-axis"],
            progression_delta_type=["ADVANCE"],
            stage_change="stage-one -> stage-two",
            resource_change=["消耗矿心"],
            growth_cost=["筋骨损伤"],
        ),
        resource_opportunity_impact=["消耗矿心"],
        world_expansion_impact=[],
        payoff_channel_impact=["POWER_BREAKTHROUGH"],
        anticipation_impact=[],
        scheduler_alignment=SchedulerAlignment(
            candidate_primary_intent="BREAKTHROUGH",
            debts_served=["debt-growth"],
        ),
        chapter_intent="BREAKTHROUGH",
        state_changes=["主角进入二段"],
        promises_to_advance=["debt-growth"],
        promises_to_pay=[],
        required_irreversible_change="进入二段",
        protagonist_strategy="主动消耗矿心完成转化",
        causal_sources=["已持有矿心"],
        required_cost="筋骨损伤",
        score_inputs=score_inputs,
        innovation_preview=None,
    )


def test_verified_kernel_evidence_feeds_existing_metrics_and_score_inputs() -> None:
    settings = load_settings()
    compilation = KernelEvidenceCompiler().compile(
        _context(),
        _candidate(),
        settings.metrics,
    )
    progress_values = compilation.verified_progress_components["components"]
    expected = progress(progress_values, settings.metrics["progress"])
    overrides = compilation.soft_metric_compilation["candidate_score_overrides"]

    assert compilation.completeness is EvidenceCompleteness.COMPLETE
    assert compilation.hard_gate_compilation.hard_failures == []
    assert compilation.verified_progression_impact["stage_change"] == {
        "from": "stage-one",
        "to": "stage-two",
    }
    assert compilation.verified_progress_components["score"] == expected.score
    assert overrides["values"]["progress_gain"] == expected.score
    assert overrides["values"]["progress_gain"] != 100
    assert overrides["values"]["thread_need_fit"] == 100
    assert overrides["values"]["debt_utility"] == 82
    assert compilation.soft_metric_compilation["resource_pressure"]["formula"] == (
        "existing:resource_pressure"
    )
    assert compilation.soft_metric_compilation["payoff"]["formula"] == (
        "existing:payoff_score"
    )


def test_unknown_reader_promise_and_drive_cannot_pass_as_verified() -> None:
    candidate = _candidate().model_copy(
        update={
            "reader_promise_alignment": [
                ReaderPromiseAlignment(
                    promise_id="invented-promise",
                    priority="CORE",
                    service=ReaderPromiseService.SERVED,
                    evidence=["模型自报"],
                )
            ],
            "narrative_drive_alignment": NarrativeDriveAlignment(
                primary_drive="INVENTED_DRIVE",
                drives_advanced=["INVENTED_DRIVE"],
                evidence=["模型自报"],
            ),
        }
    )
    compilation = KernelEvidenceCompiler().compile(
        _context(), candidate, load_settings().metrics
    )

    assert compilation.completeness is EvidenceCompleteness.CONFLICT
    failures = "\n".join(compilation.hard_gate_compilation.hard_failures)
    assert "Reader Promise ID 不属于" in failures
    assert "Narrative Drive 不属于" in failures
    assert compilation.verified_reader_promise_alignment == []
