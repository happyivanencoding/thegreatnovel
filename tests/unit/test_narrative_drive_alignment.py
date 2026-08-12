from __future__ import annotations

from novel_authoring.planning.innovation import (
    NarrativeDebt,
    NarrativeHorizon,
    NarrativePayoff,
)
from novel_authoring.planning.models import NarrativeDriveAlignment
from novel_authoring.serial_kernel import (
    NarrativeDrive,
    NarrativeDriveDriftStatus,
    NarrativeDriveStructureEvidence,
    diagnose_narrative_drive_drift,
)


def test_candidate_drive_alignment_keeps_specialized_impact_separate() -> None:
    alignment = NarrativeDriveAlignment(
        primary_drive="CAREER_MASTERY",
        primary_drive_effect="急救流程首次在团队协同中闭环",
        secondary_drive_effects={"TEAM_GROWTH": "护士长获得明确调度权"},
        drives_advanced=["CAREER_MASTERY", "TEAM_GROWTH"],
        drives_paid_off=["CAREER_MASTERY"],
        drive_balance="PRIMARY_SERVICED",
        evidence=["候选中的流程、结果与团队状态变化"],
    )

    assert alignment.primary_drive == "CAREER_MASTERY"
    assert "POWER_PROGRESSION" not in alignment.drives_advanced


def test_narrative_debt_and_payoff_reference_drive_without_new_ledger() -> None:
    debt = NarrativeDebt(
        debt_id="career-recognition",
        question_or_promise="区域急救中心能否获得转诊资格",
        horizon=NarrativeHorizon.MID,
        opened_chapter=3,
        source_event="chapter-3",
        expected_payoff_window="10-15",
        drive_type="CAREER_MASTERY",
        engine_type="CAREER_MASTERY",
    )
    payoff = NarrativePayoff(
        payoff_id="first-recognition",
        description="首次完成跨院创伤救治",
        horizon=NarrativeHorizon.MID,
        debt_id=debt.debt_id,
        associated_drive="CAREER_MASTERY",
        engine_type="CAREER_MASTERY",
    )

    assert debt.drive_type == payoff.associated_drive
    assert payoff.debt_id == debt.debt_id


def test_drive_drift_warns_when_secondary_replaces_primary() -> None:
    result = diagnose_narrative_drive_drift(
        NarrativeDriveStructureEvidence(
            primary_drive=NarrativeDrive.POWER_PROGRESSION,
            secondary_drive_replaces_primary=True,
            consecutive_primary_misses=5,
            evidence=["连续五章只有制度讨论改变状态"],
        )
    )

    assert result.status is NarrativeDriveDriftStatus.SECONDARY_REPLACEMENT
    assert result.warning is True
    assert result.hard_failure is False


def test_author_confirmed_drive_evolution_is_not_drift() -> None:
    result = diagnose_narrative_drive_drift(
        NarrativeDriveStructureEvidence(
            primary_drive=NarrativeDrive.POWER_PROGRESSION,
            secondary_drive_replaces_primary=True,
            author_changed_contract=True,
            evidence=["作者确认新版 Drive Contract"],
        )
    )

    assert result.status is NarrativeDriveDriftStatus.AUTHOR_EVOLUTION
    assert result.warning is False


def test_single_primary_drive_miss_is_soft_only() -> None:
    result = diagnose_narrative_drive_drift(
        NarrativeDriveStructureEvidence(
            primary_drive=NarrativeDrive.POWER_PROGRESSION,
            consecutive_primary_misses=1,
            evidence=["余波与恢复章节"],
        )
    )

    assert result.status is NarrativeDriveDriftStatus.SOFT_MISS
    assert result.hard_failure is False
