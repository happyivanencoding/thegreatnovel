from novel_authoring.planning.innovation import (
    DebtResolutionMode,
    NarrativeDebtStatus,
    NarrativeDebtType,
    NarrativeHorizon,
)
from novel_authoring.progression.debt import (
    ProgressionDebtInput,
    can_resolve_power_showcase,
    score_progression_debt,
)


def debt_input(**overrides: object) -> ProgressionDebtInput:
    payload: dict[str, object] = {
        "debt_id": "showcase-1",
        "debt_type": NarrativeDebtType.POWER_SHOWCASE,
        "question_or_promise": "新能力如何改变事件？",
        "horizon": NarrativeHorizon.SHORT,
        "opened_chapter": 2,
        "current_chapter": 8,
        "target_max_age": 5,
        "importance": 0.9,
        "reader_visibility": 0.9,
        "promise_progress": 0.0,
        "reminder_count": 2,
        "source_event": "chapter-2 unlock",
        "evidence": ["chapter-2 ability delta"],
        "allowed_resolution_modes": [
            DebtResolutionMode.COMBAT,
            DebtResolutionMode.NEGOTIATION,
            DebtResolutionMode.EXPLORATION,
        ],
    }
    payload.update(overrides)
    return ProgressionDebtInput.model_validate(payload)


def test_progression_debt_reuses_existing_formula() -> None:
    debt = score_progression_debt(
        debt_input(),
        formula_config={
            "age_ratio_cap": 1.5,
            "reminder_step": 0.15,
            "reminder_cap": 3,
            "progress_exponent": 1.2,
            "debt_cap": 150,
        },
    )

    assert debt.debt_score is not None and debt.debt_score > 100
    assert debt.status in {
        NarrativeDebtStatus.PAYOFF_READY,
        NarrativeDebtStatus.OVERDUE,
    }
    assert debt.metric_components["age_chapters"] == 6


def test_power_showcase_can_be_paid_without_combat() -> None:
    assert can_resolve_power_showcase(DebtResolutionMode.NEGOTIATION)
    assert can_resolve_power_showcase(DebtResolutionMode.EXPLORATION)
