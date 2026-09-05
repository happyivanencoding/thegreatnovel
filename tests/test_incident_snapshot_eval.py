from __future__ import annotations

from story_mvp.incident_snapshot_eval import (
    DEFAULT_CORPUS_ROOT,
    calibrate_case,
    evaluate_text,
    load_corpus,
    validate_corpus,
)


def test_real_incident_snapshot_corpus_calibrates_all_initial_cases() -> None:
    cases = validate_corpus()
    assert [case.case_id for case in cases] == [f"RIS-{index:03d}" for index in range(1, 9)]


def test_each_snapshot_known_bad_fails_and_known_good_passes() -> None:
    for case in load_corpus(DEFAULT_CORPUS_ROOT):
        bad, good = calibrate_case(case)
        assert bad.passed is False, case.case_id
        assert bad.failures, case.case_id
        assert good.passed is True, case.case_id
        assert good.failures == (), case.case_id


def test_snapshot_assertions_are_case_specific_not_a_global_semantic_gate() -> None:
    case = load_corpus(DEFAULT_CORPUS_ROOT)[3]  # RIS-004: unauthorized binding rule
    unrelated_text = "天气很好，人物继续赶路。"
    result = evaluate_text(case, unrelated_text)
    assert result.passed is False
    assert any("当前人物安排" in failure for failure in result.failures)
