from __future__ import annotations

import pytest
from pydantic import ValidationError

from novel_authoring.contracts.draft import (
    DraftCreativeOutput,
    DraftCreativeStateChange,
)
from novel_authoring.domain.models import ContinuationMode, NarrativeFunction
from novel_authoring.drafting.compiler import (
    ChapterRealizationBrief,
    compile_draft_output,
    diagnose_scene_realization,
)
from novel_authoring.planning.models import (
    CandidateCreativeProposal,
    ChapterContract,
)
from novel_authoring.planning.reference_strategy import (
    select_planning_reference_strategy,
)


def _contract() -> ChapterContract:
    return ChapterContract.model_construct(
        contract_id="contract-1",
        chapter=3,
        mode=ContinuationMode.FAITHFUL,
        boundary_packet_id="packet-1",
        continuation_boundary={"base_event_seq": 1, "base_projection_hash": "p"},
        candidate_id="candidate-1",
        primary_thread="thread-1",
        primary_function=NarrativeFunction.PROGRESS,
        secondary_functions=[],
        reader_question="他能否守住机械门",
        pressure={"before": 60, "target_after": 70},
        payoff_plan={},
        narrative_debt={"advance": ["thread-1"], "fully_pay": []},
        progress={},
        required_irreversible_change="机械门完成加固",
        required_cost="最后一枚螺栓耗尽",
        canon_constraints=[],
        knowledge_constraints=[],
        must_not_resolve=[],
        forbidden_repetitions=[],
        style_constraints={},
        ending_state="门外传来新的敲击",
        commit_updates=["thread_status"],
        innovation_control={},
    )


def test_creative_draft_compiles_python_owned_evidence_and_soft_audits() -> None:
    creative = DraftCreativeOutput(
        task_id="draft-task-1",
        contract_id="contract-1",
        chapter_title="机械门",
        prose_markdown="机械门完成加固，最后一枚螺栓耗尽。门外传来新的敲击。",
        state_changes=[
            DraftCreativeStateChange(
                kind="resource",
                record_id="resource-1",
                payload={"name": "最后一枚螺栓", "delta": -1},
            )
        ],
    )

    compiled = compile_draft_output(creative, _contract())

    assert compiled.evidence_policy == "COMPILED_SOFT"
    assert compiled.contract_evidence["required_cost"] == ["最后一枚螺栓耗尽"]
    assert compiled.state_changes[0].evidence_quotes == ["最后一枚螺栓"]
    assert compiled.character_fit_inputs
    assert compiled.style_fit_inputs
    assert compiled.realized_kernel_trace is not None


def test_missing_state_change_is_still_a_hard_input_failure() -> None:
    with pytest.raises(ValidationError):
        DraftCreativeOutput(
            task_id="draft-task-1",
            contract_id="contract-1",
            chapter_title="空场景",
            prose_markdown="只有一句话。",
            state_changes=[],
        )


def test_thin_realization_is_a_warning_only_diagnostic() -> None:
    result = diagnose_scene_realization(
        "他点头。",
        ChapterRealizationBrief(target_word_range=(100, 300), target_scene_count=2),
    )
    assert result["code"] == "SCENE_REALIZATION_THIN"
    assert result["severity"] == "WARNING"


def test_planning_reference_strategy_is_bounded_and_has_no_card_fallback() -> None:
    snapshot = {
        "snapshot_id": "snapshot-1",
        "snapshot_hash": "hash-1",
        "match_tier": "RELAXED_SCENE",
        "compact_cards": [
            {
                "card_id": f"card-{index}",
                "card_type": "mechanism-card",
                "metadata_match_fields": ["scene_functions"],
                "failure_risks": ["重复套路"],
            }
            for index in range(5)
        ],
    }
    selected = select_planning_reference_strategy(snapshot)
    fallback = select_planning_reference_strategy(
        {"snapshot_id": "empty", "snapshot_hash": "empty-hash", "compact_cards": []}
    )

    assert len(selected.selected_card_ids) == 3
    assert selected.match_tier == "RELAXED_SCENE"
    assert selected.usage == "REFERENCE_ONLY"
    assert fallback.selected_card_ids == []
    assert fallback.match_tier == "ZERO_RESULTS"
    assert fallback.reuse_reason == "ZERO_RESULTS_OR_REFERENCE_UNAVAILABLE"


def test_planning_reference_strategy_deprioritizes_recent_solutions() -> None:
    selected = select_planning_reference_strategy(
        {
            "snapshot_id": "snapshot-2",
            "snapshot_hash": "hash-2",
            "compact_cards": [
                {
                    "card_id": "contrast-recent",
                    "card_type": "contrast-card",
                    "solutions": [{"solution_id": "solution-recent"}],
                },
                {"card_id": "mechanism-new", "card_type": "mechanism-card"},
            ],
        },
        recent_solution_ids=["solution-recent"],
    )

    assert selected.selected_card_ids[0] == "mechanism-new"
    assert selected.reuse_reason is not None


def test_candidate_creative_schema_does_not_expose_internal_scoring_fields() -> None:
    properties = CandidateCreativeProposal.model_json_schema()["properties"]
    assert "score_inputs" not in properties
    assert "gate_input" not in properties
    assert "commit_updates" not in properties
    assert "style_constraints" not in properties
