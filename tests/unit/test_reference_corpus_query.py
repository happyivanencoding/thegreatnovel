from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from novel_authoring.reference_corpus.query import (
    ReferenceCorpusQueryEcho,
    ReferenceCorpusQueryRequest,
    ReferenceCorpusQueryResponse,
    query_reference_corpus,
    reference_corpus_runtime_diagnostic,
)
from novel_authoring.reference_corpus.semantic import (
    retrieve_metadata_candidates,
    source_diversity_guard,
)
from novel_authoring.reference_corpus.semantic_models import (
    ProseControlCard,
)


def _evidence(book_id: str, index: int) -> dict[str, object]:
    return {
        "evidence_id": f"ev-{book_id}-{index}",
        "source_book_id": book_id,
        "source_id": f"source-{book_id}",
        "distill_id": f"distill-{book_id}",
        "segment_id": "segment-0001",
        "line_start": 1,
        "line_end": 3,
        "observation_summary": "测试窗口只保留抽象动作和反馈，不保存来源正文。",
    }


def _mechanism(card_id: str = "mechanism-test") -> dict[str, object]:
    books = ["book-01", "book-02", "book-03", "book-04"]
    return {
        "schema_version": "reference-corpus-card-v1",
        "card_id": card_id,
        "card_type": "mechanism-card",
        "knowledge_level": "CROSS_BOOK_CONTRAST",
        "status": "REFERENCE_ONLY",
        "source_book_ids": books,
        "evidence_refs": [_evidence(book, index) for index, book in enumerate(books, 1)],
        "creative_problem_tags": ["pure-upside", "breakthrough"],
        "reader_experiences": ["BREAKTHROUGH"],
        "narrative_drives": ["POWER_PROGRESSION"],
        "payoff_channels": ["POWER_BREAKTHROUGH"],
        "evidence_scope": "MULTI_CATEGORY",
        "maturity": "SUPPORTED",
        "category_ids": ["玄幻", "仙侠", "科幻"],
        "depends_on": [],
        "creative_problem": "突破如何打开新的行动空间",
        "applicability_conditions": ["回报必须改变可用行动"],
        "mechanism": "先让角色使用新能力完成过去不能完成的动作。",
        "reader_payoff": ["看到选择空间扩大"],
        "action_space_effect": ["从单一解法变为可组合解法"],
        "variants": ["能力试玩", "资源释放"],
        "when_not_to_use": ["只改变数值而不改变行动"],
        "contrast_cases": ["需要立即处理余波的场景"],
        "failure_risks": ["重复验证造成疲劳"],
        "failure_basis": ["OBSERVED_REPETITION"],
        "source_count": 4,
        "category_count": 3,
    }


def _prose_control(card_id: str = "prose-control-test") -> dict[str, object]:
    books = ["book-01", "book-02", "book-03", "book-04"]
    return {
        "schema_version": "reference-corpus-card-v1",
        "card_id": card_id,
        "card_type": "prose-control",
        "knowledge_level": "CORPUS_SYNTHESIS",
        "status": "REFERENCE_ONLY",
        "source_book_ids": books,
        "evidence_refs": [_evidence(book, index) for index, book in enumerate(books, 1)],
        "creative_problem_tags": ["prose-realization", "action"],
        "reader_experiences": [],
        "narrative_drives": [],
        "payoff_channels": [],
        "evidence_scope": "MULTI_CATEGORY",
        "maturity": "BROAD",
        "category_ids": ["玄幻", "都市", "科幻"],
        "depends_on": [],
        "control_topic": "动作先于解释",
        "applicable_scene_functions": ["ACTION", "PAYOFF"],
        "guidance": "先让动作和反馈发生，再补当前场景需要的解释。",
        "variants": ["战斗保留距离和反馈", "专业操作保留判断和结果"],
        "when_to_use": ["读者只能复述能力名，不能复述现场过程"],
        "failure_signals": ["把技能名排成清单"],
        "transfer_boundary": "只迁移抽象写法变量，不迁移来源人物、事件或句式。",
    }


def _write_package(root: Path, records: list[dict[str, object]]) -> None:
    machine = root / "machine"
    machine.mkdir(parents=True)
    (machine / "corpus-package.json").write_text(
        json.dumps(
            {
                "schema_version": "reference-corpus-machine-package-v1",
                "status": "REFERENCE_ONLY",
                "query_ready": True,
                "raw_text_included": False,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (machine / "cards.jsonl").write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def test_query_contract_limits_purpose_and_card_families(tmp_path: Path) -> None:
    root = tmp_path / "corpus"
    _write_package(root, [_mechanism(), _prose_control()])

    planning = query_reference_corpus(
        {
            "purpose": "PLANNING",
            "creative_problem": "pure-upside",
            "reader_experiences": ["BREAKTHROUGH"],
            "max_cards": 3,
        },
        corpus_root=root,
    )
    assert planning.usage == "REFERENCE_ONLY"
    assert planning.status == "ENABLED"
    assert planning.package_schema_version == "reference-corpus-machine-package-v1"
    assert planning.package_hash
    assert all(card.card_type == "mechanism-card" for card in planning.cards)
    assert all(card.card_type != "prose-control" for card in planning.cards)
    assert all("observation_summary" not in card.model_dump() for card in planning.cards)

    prose = query_reference_corpus(
        {
            "purpose": "PROSE",
            "creative_problem": "",
            "scene_functions": ["ACTION"],
            "max_cards": 3,
        },
        corpus_root=root,
    )
    assert prose.status == "ENABLED"
    assert [card.card_type for card in prose.cards] == ["prose-control"]
    assert all(card.card_type != "mechanism-card" for card in prose.cards)
    assert "source_refs" in prose.cards[0].model_dump()


def test_query_soft_fails_without_package_or_with_zero_results(tmp_path: Path) -> None:
    missing = query_reference_corpus(
        {"purpose": "PROSE", "scene_functions": ["ACTION"]},
        corpus_root=tmp_path / "missing",
    )
    assert not missing.cards
    assert missing.status == "UNAVAILABLE"
    assert any("soft-fail" in warning for warning in missing.warnings)

    root = tmp_path / "empty"
    _write_package(root, [_mechanism()])
    empty = query_reference_corpus(
        {"purpose": "PROSE", "scene_functions": ["DIALOGUE"]},
        corpus_root=root,
    )
    assert not empty.cards
    assert empty.status == "ZERO_RESULTS"
    assert empty.knowledge_gaps


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("query_ready", False, "query_ready=false"),
        ("raw_text_included", True, "raw_text_included=true"),
    ],
)
def test_query_soft_fails_when_machine_package_is_not_retrieval_ready(
    tmp_path: Path, field: str, value: object, reason: str
) -> None:
    root = tmp_path / field
    _write_package(root, [_mechanism()])
    package_path = root / "machine" / "corpus-package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package[field] = value
    package_path.write_text(json.dumps(package), encoding="utf-8")

    response = query_reference_corpus(
        {"purpose": "PLANNING", "creative_problem": "pure-upside", "max_cards": 3},
        corpus_root=root,
    )

    assert response.status == "UNAVAILABLE"
    assert not response.cards
    assert response.machine_bundle_hash
    assert any(reason in warning for warning in response.warnings)
    assert any(reason in gap for gap in response.knowledge_gaps)


def test_machine_bundle_hash_changes_when_cards_change_without_package_hash_change(
    tmp_path: Path,
) -> None:
    root = tmp_path / "bundle-hash"
    _write_package(root, [_mechanism()])
    request = {"purpose": "PLANNING", "creative_problem": "pure-upside", "max_cards": 3}
    before = query_reference_corpus(request, corpus_root=root)

    package_path = root / "machine" / "corpus-package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package["generated_at"] = "later-but-not-semantic"
    package_path.write_text(json.dumps(package), encoding="utf-8")
    generated_at_only = query_reference_corpus(request, corpus_root=root)
    assert generated_at_only.machine_bundle_hash == before.machine_bundle_hash
    assert generated_at_only.package_hash != before.package_hash

    cards_path = root / "machine" / "cards.jsonl"
    card = json.loads(cards_path.read_text(encoding="utf-8").splitlines()[0])
    card["mechanism"] = "cards 改动后的机制"
    cards_path.write_text(json.dumps(card) + "\n", encoding="utf-8")
    after = query_reference_corpus(request, corpus_root=root)

    assert after.status == "ENABLED"
    assert after.machine_bundle_hash != before.machine_bundle_hash
    assert after.package_hash == generated_at_only.package_hash


def test_runtime_diagnostic_reports_configured_package_identity(tmp_path: Path) -> None:
    root = tmp_path / "diagnostic"
    _write_package(root, [_mechanism(), _prose_control()])

    result = reference_corpus_runtime_diagnostic(corpus_root=root)

    assert result["status"] == "ENABLED"
    assert result["configured_root"] == str(root)
    assert result["query_ready"] is True
    assert result["machine_bundle_hash"]
    assert result["card_count"] == 2


def test_runtime_diagnostic_reports_not_ready_without_cards(tmp_path: Path) -> None:
    root = tmp_path / "diagnostic-not-ready"
    _write_package(root, [_mechanism()])
    package_path = root / "machine" / "corpus-package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package["query_ready"] = False
    package["readiness_reasons"] = ["semantic validation 未通过"]
    package_path.write_text(json.dumps(package), encoding="utf-8")

    result = reference_corpus_runtime_diagnostic(corpus_root=root)

    assert result["status"] == "UNAVAILABLE"
    assert result["query_ready"] is False
    assert result["machine_bundle_hash"]
    assert result["card_count"] == 1
    assert result["knowledge_gaps"] == ["semantic validation 未通过"]


def test_query_status_disabled_when_root_is_not_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "novel_authoring.reference_corpus.query._root_from_config",
        lambda _corpus_root: None,
    )

    response = query_reference_corpus({"purpose": "PLANNING"})

    assert response.status == "DISABLED"
    assert not response.cards


def test_query_status_unavailable_when_machine_file_is_missing(tmp_path: Path) -> None:
    root = tmp_path / "incomplete"
    machine = root / "machine"
    machine.mkdir(parents=True)
    (machine / "corpus-package.json").write_text(
        json.dumps({"schema_version": "reference-corpus-machine-package-v1"}),
        encoding="utf-8",
    )

    response = query_reference_corpus({"purpose": "PLANNING"}, corpus_root=root)

    assert response.status == "UNAVAILABLE"
    assert not response.cards


@pytest.mark.parametrize("package_text", ["{broken", json.dumps({"schema_version": "wrong"})])
def test_query_status_corrupt_when_package_json_or_schema_is_invalid(
    tmp_path: Path, package_text: str
) -> None:
    root = tmp_path / "corrupt-package"
    machine = root / "machine"
    machine.mkdir(parents=True)
    (machine / "corpus-package.json").write_text(package_text, encoding="utf-8")
    (machine / "cards.jsonl").write_text("", encoding="utf-8")

    response = query_reference_corpus({"purpose": "PLANNING"}, corpus_root=root)

    assert response.status == "CORRUPT"
    assert not response.cards


def test_query_status_corrupt_when_cards_jsonl_is_invalid(tmp_path: Path) -> None:
    root = tmp_path / "corrupt-cards"
    _write_package(root, [])
    (root / "machine" / "cards.jsonl").write_text("{broken\n", encoding="utf-8")

    response = query_reference_corpus({"purpose": "PLANNING"}, corpus_root=root)

    assert response.status == "CORRUPT"
    assert response.package_schema_version == "reference-corpus-machine-package-v1"
    assert response.package_hash


def test_query_separates_human_problem_from_machine_tags_and_keeps_legacy_tag(
    tmp_path: Path,
) -> None:
    root = tmp_path / "tags"
    _write_package(root, [_mechanism()])

    tagged = query_reference_corpus(
        {
            "purpose": "PLANNING",
            "creative_problem": "突破如何打开新的行动空间",
            "creative_problem_tags": ["pure-upside"],
            "max_cards": 3,
        },
        corpus_root=root,
    )
    assert [card.card_id for card in tagged.cards] == ["mechanism-test"]
    assert tagged.query.creative_problem == "突破如何打开新的行动空间"
    assert tagged.query.creative_problem_tags == ["pure-upside"]

    legacy = query_reference_corpus(
        {"purpose": "PLANNING", "creative_problem": "pure-upside", "max_cards": 3},
        corpus_root=root,
    )
    assert [card.card_id for card in legacy.cards] == ["mechanism-test"]

    human_sentence = query_reference_corpus(
        {
            "purpose": "PLANNING",
            "creative_problem": "突破 如何打开新的行动空间",
            "scene_functions": ["DIALOGUE"],
            "max_cards": 3,
        },
        corpus_root=root,
    )
    assert human_sentence.status == "ZERO_RESULTS"
    assert not human_sentence.cards


def test_retrieval_legacy_problem_only_accepts_safe_single_tags(tmp_path: Path) -> None:
    root = tmp_path / "semantic-tags"
    _write_package(root, [_mechanism()])

    assert retrieve_metadata_candidates(
        root,
        creative_problem="pure-upside",
        card_families=("mechanism-card",),
        max_cards=3,
    )
    human_sentence_results = retrieve_metadata_candidates(
        root,
        creative_problem="突破 如何打开新的行动空间",
        card_families=("mechanism-card",),
        max_cards=3,
    )
    assert len(human_sentence_results) == 1
    assert "creative_problem_tags" not in human_sentence_results[0][
        "metadata_match_fields"
    ]


def test_response_status_defaults_for_existing_construction() -> None:
    response = ReferenceCorpusQueryResponse(
        schema_version="reference-corpus-query-v1",
        purpose="PLANNING",
        query=ReferenceCorpusQueryEcho(max_cards=3),
    )

    assert response.status == "ENABLED"
    assert response.package_schema_version is None
    assert response.package_hash is None


def test_query_excludes_stale_cards_and_cards_depending_on_stale(tmp_path: Path) -> None:
    root = tmp_path / "stale"
    stale = _mechanism("stale-mechanism")
    stale["status"] = "STALE"
    dependent = _mechanism("dependent-mechanism")
    dependent["depends_on"] = ["stale-mechanism"]
    _write_package(root, [_mechanism(), stale, dependent])

    response = query_reference_corpus(
        {"purpose": "PLANNING", "creative_problem": "pure-upside", "max_cards": 3},
        corpus_root=root,
    )

    assert [card.card_id for card in response.cards] == ["mechanism-test"]


def test_query_request_is_strict_and_source_diversity_is_bounded() -> None:
    with pytest.raises(ValidationError):
        ReferenceCorpusQueryRequest.model_validate(
            {"purpose": "PLANNING", "max_cards": 2}
        )
    with pytest.raises(ValidationError):
        ReferenceCorpusQueryRequest.model_validate(
            {"purpose": "PLANNING", "max_cards": 9, "unexpected": True}
        )
    with pytest.raises(ValidationError):
        ReferenceCorpusQueryRequest.model_validate(
            {"purpose": "PLANNING", "max_cards": 3, "unexpected": True}
        )
    records = [{"source_book_ids": ["book-01"]} for _ in range(3)]
    assert source_diversity_guard(records) is False


def test_prose_control_contract_uses_abstract_lists_and_reference_only() -> None:
    card = ProseControlCard.model_validate(_prose_control())
    assert card.status.value == "REFERENCE_ONLY"
    assert isinstance(card.when_to_use, list)
    assert isinstance(card.failure_signals, list)
    with pytest.raises(ValidationError):
        ProseControlCard.model_validate({**_prose_control(), "source_quote": "原文"})
