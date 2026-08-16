from __future__ import annotations

from typing import Any, cast

from novel_authoring.config import load_settings
from novel_authoring.contracts.draft import (
    DraftOutput,
    DraftStateChange,
    RealizedKernelTrace,
)
from novel_authoring.planning.models import ChapterContract
from novel_authoring.validation.models import ValidationReport
from novel_authoring.validation.validators import (
    ValidationContext,
    _match_evidence,
    validate_contract,
)


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


def _validate(draft: DraftOutput) -> ValidationReport:
    return validate_contract(
        ValidationContext(
            draft=draft,
            contract=_contract(),
            projection=cast(Any, None),
            settings=load_settings(),
        )
    )


def test_verified_contract_missing_realized_kernel_trace_is_warning() -> None:
    report = _validate(_draft(None))

    assert report.passed
    finding = next(
        finding
        for finding in report.findings
        if finding.code == "REALIZED_KERNEL_TRACE_MISSING"
    )
    assert finding.severity.value == "WARNING"


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

    finding = next(
        finding
        for finding in report.findings
        if finding.code == "REALIZED_KERNEL_EXCEEDS_VERIFIED_CONTRACT"
    )
    assert finding.severity.value == "WARNING"


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


def test_evidence_matching_records_exact_normalized_ambiguous_and_not_found() -> None:
    prose = "他说：“系统，已启动。” 系统，已启动。"

    assert _match_evidence(prose, "系统，已启动。") == "EXACT"
    assert _match_evidence(prose, "系统,已启动.") == "AMBIGUOUS"
    assert _match_evidence("系统，已启动。", "系统,已启动.") == "NORMALIZED"
    assert _match_evidence(prose, "不存在") == "NOT_FOUND"
    assert _match_evidence(prose, "  \n\t ") == "NOT_FOUND"


def test_contract_evidence_not_found_is_warning_but_state_change_is_hard() -> None:
    draft = _draft(None).model_copy(
        update={
            "contract_evidence": {
                "required_irreversible_change": ["不存在的证据"],
                "required_cost": ["代价发生"],
                "ending_state": ["结尾改变"],
            },
            "state_changes": [
                DraftStateChange(
                    kind="fact",
                    record_id="fact-1",
                    payload={},
                    evidence_quotes=["不存在的 StateChange 证据"],
                )
            ],
        }
    )

    report = _validate(draft)

    contract_finding = next(
        finding
        for finding in report.findings
        if finding.code == "EVIDENCE_NOT_IN_PROSE"
        and finding.location == "required_irreversible_change"
    )
    state_change_finding = next(
        finding
        for finding in report.findings
        if finding.code == "EVIDENCE_NOT_IN_PROSE"
        and finding.location == "state_changes:fact-1"
    )
    assert contract_finding.severity.value == "WARNING"
    assert state_change_finding.severity.value == "ERROR"
    matches = report.measurements["evidence_matches"]
    assert {item["status"] for item in matches} >= {"NOT_FOUND", "EXACT"}
