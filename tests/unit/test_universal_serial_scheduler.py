from __future__ import annotations

from novel_authoring.progression.anticipation import AnticipationSurfaceView
from novel_authoring.progression.scheduler import (
    ChapterIntent,
    recommend_universal_chapter_intent,
)
from novel_authoring.serial_kernel import (
    EngineIntentRecommendation,
    NarrativeDrive,
    NarrativeDriveContract,
    NarrativeEngineType,
)


def _drive_contract() -> NarrativeDriveContract:
    return NarrativeDriveContract(
        drive_contract_id="mixed",
        primary_drive=NarrativeDrive.POWER_PROGRESSION,
        secondary_drives=[
            NarrativeDrive.MYSTERY_REVELATION,
            NarrativeDrive.RELATIONSHIP_EMOTIONAL,
        ],
        drive_priorities={
            NarrativeDrive.POWER_PROGRESSION: 100,
            NarrativeDrive.MYSTERY_REVELATION: 80,
            NarrativeDrive.RELATIONSHIP_EMOTIONAL: 55,
        },
        drive_promises={
            NarrativeDrive.POWER_PROGRESSION: ["持续变强"],
            NarrativeDrive.MYSTERY_REVELATION: ["逐步看见真相"],
            NarrativeDrive.RELATIONSHIP_EMOTIONAL: ["关系变化有后果"],
        },
    )


def test_universal_scheduler_aggregates_engine_scores_and_drive_priorities() -> None:
    recommendations = [
        EngineIntentRecommendation(
            engine_type=NarrativeEngineType.PROGRESSION,
            drive=NarrativeDrive.POWER_PROGRESSION,
            intent="POWER_VERIFICATION",
            priority=82,
            why_now=["能力仍待场景验证"],
            debt_ids=["power-showcase"],
            reader_promises=["持续变强"],
            evidence=["chapter-12:ability-earned"],
        ),
        EngineIntentRecommendation(
            engine_type=NarrativeEngineType.MYSTERY_REVEAL,
            drive=NarrativeDrive.MYSTERY_REVELATION,
            intent="MYSTERY_ADVANCE",
            priority=64,
            why_now=["Reveal Agenda 进入近期窗口"],
        ),
        EngineIntentRecommendation(
            engine_type=NarrativeEngineType.RELATIONSHIP_LIFE,
            drive=NarrativeDrive.RELATIONSHIP_EMOTIONAL,
            intent="RELATIONSHIP_ADVANCE",
            priority=41,
            why_now=["关系承诺需要承接"],
        ),
    ]

    result = recommend_universal_chapter_intent(
        drive_contract=_drive_contract(),
        engine_recommendations=recommendations,
        debts=[],
        anticipation=AnticipationSurfaceView(
            chapter_id="chapter-12",
            chapter_ordinal=12,
        ),
    )

    assert result.primary_intent is ChapterIntent.POWER_VERIFICATION
    assert result.secondary_intents == [
        ChapterIntent.MYSTERY_ADVANCE,
        ChapterIntent.RELATIONSHIP_ADVANCE,
    ]
    assert result.source_drive == "POWER_PROGRESSION"
    assert result.supporting_debt_ids == ["power-showcase"]
    assert result.reader_promises_served == ["持续变强"]


def test_scheduler_ignores_recommendations_for_unconfirmed_drives() -> None:
    result = recommend_universal_chapter_intent(
        drive_contract=_drive_contract(),
        engine_recommendations=[
            EngineIntentRecommendation(
                engine_type=NarrativeEngineType.CAREER_MASTERY,
                drive=NarrativeDrive.CAREER_MASTERY,
                intent="CAREER_MASTERY",
                priority=100,
                why_now=["不属于已确认 Drive Mix"],
            ),
            EngineIntentRecommendation(
                engine_type=NarrativeEngineType.PROGRESSION,
                drive=NarrativeDrive.POWER_PROGRESSION,
                intent="PROGRESSION_SETUP",
                priority=50,
                why_now=["保持成长因果"],
            ),
        ],
        debts=[],
        anticipation=AnticipationSurfaceView(
            chapter_id="chapter-1",
            chapter_ordinal=1,
        ),
    )

    assert result.primary_intent is ChapterIntent.PROGRESSION_SETUP
    assert len(result.engine_recommendations) == 1
