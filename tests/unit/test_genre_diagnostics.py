from novel_authoring.progression.diagnostics import (
    GenreChangeStatus,
    GenreStructureEvidence,
    diagnose_genre_change,
)


def test_remove_the_skin_detects_foundation_without_genre_causality() -> None:
    result = diagnose_genre_change(
        GenreStructureEvidence(
            evidence=["超凡名词存在，但解决方案仍只是普通行政流程"],
        )
    )

    assert result.drift.status is GenreChangeStatus.GENRE_SKIN_ONLY
    assert result.drift.warning is True
    assert result.drift.hard_failure is False


def test_genre_evolution_is_not_automatically_drift() -> None:
    result = diagnose_genre_change(
        GenreStructureEvidence(
            progression_gate_affects_causality=True,
            power_opens_space=True,
            core_promise_preserved=True,
            delivery_channel_changed=True,
            evidence=["个人能力成长转为团队与城市共同扩大可能性"],
        )
    )

    assert result.drift.status is GenreChangeStatus.CLEAR
    assert result.evolution.status is GenreChangeStatus.GENRE_EVOLUTION


def test_one_chapter_missing_core_service_is_not_hard_failure() -> None:
    result = diagnose_genre_change(
        GenreStructureEvidence(
            ability_changes_solution=True,
            consecutive_core_misses=1,
        )
    )

    assert result.drift.status is GenreChangeStatus.CLEAR
    assert result.drift.hard_failure is False


def test_contradicting_core_promise_is_hard_failure() -> None:
    result = diagnose_genre_change(
        GenreStructureEvidence(
            ability_changes_solution=True,
            contradicts_core_promise=True,
            evidence=["候选宣布此前超凡全部不存在"],
        )
    )

    assert result.drift.status is GenreChangeStatus.GENRE_REPLACEMENT
    assert result.drift.hard_failure is True


def test_theme_cannot_replace_core_promise_without_author_change() -> None:
    result = diagnose_genre_change(
        GenreStructureEvidence(
            progression_gate_affects_causality=True,
            theme_replaces_core=True,
        )
    )

    assert result.drift.status is GenreChangeStatus.GENRE_REPLACEMENT
    assert result.drift.warning is True
    assert result.drift.hard_failure is False
