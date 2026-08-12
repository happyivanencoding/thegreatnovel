from pathlib import Path

from novel_authoring.db.database import Database
from novel_authoring.planning.innovation import (
    NarrativeDebt,
    NarrativeDebtType,
    NarrativeHorizon,
)
from novel_authoring.progression.anticipation import AnticipationSurfaceView
from novel_authoring.progression.scheduler import (
    ChapterIntent,
    load_scheduler_override,
    recommend_chapter_intent,
    save_scheduler_override,
)


def database_with_book(path: Path) -> Database:
    database = Database(path)
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO books(
                book_id, title, mode, source_root, workspace_root,
                created_at, updated_at
            ) VALUES ('scheduler-book', '调度测试', 'CONSTRAINED_INNOVATION', '', '', 'now', 'now')
            """
        )
    return database


def test_scheduler_recommends_explainable_intent() -> None:
    debt = NarrativeDebt(
        debt_id="resource-debt",
        debt_type=NarrativeDebtType.RESOURCE,
        question_or_promise="已获得资源何时转化？",
        horizon=NarrativeHorizon.SHORT,
        opened_chapter=2,
        source_event="chapter-2",
        expected_payoff_window="5 chapters",
        debt_score=72,
    )
    recommendation = recommend_chapter_intent(
        debts=[debt],
        anticipation=AnticipationSurfaceView(
            chapter_id="chapter-8",
            chapter_ordinal=8,
        ),
    )

    assert recommendation.primary_intent is ChapterIntent.RESOURCE_CONVERSION
    assert recommendation.supporting_debt_ids == ["resource-debt"]
    assert recommendation.why_now


def test_scheduler_override_persists(tmp_path: Path) -> None:
    database = database_with_book(tmp_path / "scheduler.sqlite3")
    saved = save_scheduler_override(
        database,
        book_id="scheduler-book",
        edition_id="base",
        chapter_ordinal=9,
        primary_intent=ChapterIntent.RECOVERY,
        secondary_intents=[ChapterIntent.RELATIONSHIP_ADVANCE],
        reason="作者要给角色喘息空间",
    )
    loaded = load_scheduler_override(
        database,
        book_id="scheduler-book",
        edition_id="base",
        chapter_ordinal=9,
    )

    assert loaded == saved
    assert loaded is not None
    assert loaded.primary_intent is ChapterIntent.RECOVERY
