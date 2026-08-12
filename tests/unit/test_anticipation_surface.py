from novel_authoring.planning.innovation import (
    DebtResolutionMode,
    NarrativeDebt,
    NarrativeDebtStatus,
    NarrativeDebtType,
    NarrativeHorizon,
)
from novel_authoring.progression.anticipation import build_anticipation_surface


def test_anticipation_surface_is_projection_only() -> None:
    debt = NarrativeDebt(
        debt_id="ability-showcase",
        debt_type=NarrativeDebtType.POWER_SHOWCASE,
        question_or_promise="新能力第一次改变局势",
        horizon=NarrativeHorizon.SHORT,
        opened_chapter=2,
        source_event="chapter-2",
        expected_payoff_window="within 5 chapters",
        status=NarrativeDebtStatus.PAYOFF_READY,
        debt_score=92,
        allowed_resolution_modes=[DebtResolutionMode.NEGOTIATION],
    )
    before = debt.model_dump(mode="json")

    surface = build_anticipation_surface(
        chapter_id="chapter-8",
        chapter_ordinal=8,
        debts=[debt],
    )

    assert surface.projection_only is True
    assert surface.canon_mutation_allowed is False
    assert surface.items[0].urgency == 4
    assert debt.model_dump(mode="json") == before


def test_missing_evidence_does_not_become_fake_maturity() -> None:
    debt = NarrativeDebt(
        debt_id="mystery-unknown",
        debt_type=NarrativeDebtType.MYSTERY,
        question_or_promise="门后是什么？",
        horizon=NarrativeHorizon.LONG,
        opened_chapter=1,
        source_event="chapter-1",
        expected_payoff_window="unknown",
    )

    surface = build_anticipation_surface(
        chapter_id="chapter-3",
        chapter_ordinal=3,
        debts=[debt],
    )

    assert surface.items[0].maturity is None
