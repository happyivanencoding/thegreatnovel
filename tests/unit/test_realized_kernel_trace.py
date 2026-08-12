from __future__ import annotations

from typing import Any, cast

from novel_authoring.config import load_settings
from novel_authoring.contracts.draft import DraftOutput, RealizedKernelTrace
from novel_authoring.planning.models import ChapterContract
from novel_authoring.validation.validators import ValidationContext, validate_contract


def _contract() -> ChapterContract:
    return ChapterContract.model_construct(
        contract_id="contract-kernel",
        commit_updates=[],
        chapter_intent="BREAKTHROUGH",
        kernel_verification_status="COMPLETE",
        verified_kernel_trace={
            "reader_promise_alignment": [],
            "narrative_drive_alignment": {
                "drives_advanced": ["POWER_PROGRESSION"]
            },
            "progression_impact": {
                "axis_advanced": [],
                "progression_delta_type": [],
                "stage_change": None,
                "resource_changes": [],
                "ability_unlocks": [],
            },
            "resource_impact": [],
            "world_expansion_impact": [],
            "payoff_channels": [],
            "scheduler_alignment": {"candidate_primary_intent": "BREAKTHROUGH"},
        },
    )


def _draft(trace: RealizedKernelTrace | None) -> DraftOutput:
    prose = "变化发生。代价发生。结尾改变。"
    return DraftOutput.model_construct(
        prose_markdown=prose,
        state_changes=[],
        contract_evidence={
            "required_irreversible_change": ["变化发生"],
            "required_cost": ["代价发生"],
            "ending_state": ["结尾改变"],
        },
        realized_kernel_trace=trace,
    )


def _validate(draft: DraftOutput):
    return validate_contract(
        ValidationContext(
            draft=draft,
            contract=_contract(),
            projection=cast(Any, None),
            settings=load_settings(),
        )
    )


def test_verified_contract_requires_realized_kernel_trace() -> None:
    report = _validate(_draft(None))

    assert not report.passed
    assert "REALIZED_KERNEL_TRACE_MISSING" in {
        finding.code for finding in report.findings
    }


def test_realized_trace_cannot_claim_unverified_drive() -> None:
    report = _validate(
        _draft(
            RealizedKernelTrace(
                expected_contract_id="contract-kernel",
                primary_intent="BREAKTHROUGH",
                narrative_drives_advanced=["MYSTERY_REVELATION"],
            )
        )
    )

    assert not report.passed
    assert "REALIZED_KERNEL_EXCEEDS_VERIFIED_CONTRACT" in {
        finding.code for finding in report.findings
    }


def test_missing_expected_kernel_delivery_is_warning_not_hard_failure() -> None:
    report = _validate(
        _draft(
            RealizedKernelTrace(
                expected_contract_id="contract-kernel",
                primary_intent="BREAKTHROUGH",
            )
        )
    )

    underdelivery = [
        finding
        for finding in report.findings
        if finding.code == "REALIZED_KERNEL_UNDERDELIVERY"
    ]
    assert underdelivery
    assert all(finding.severity.value == "WARNING" for finding in underdelivery)
