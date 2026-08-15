from __future__ import annotations

import json
from pathlib import Path

import pytest

from novel_authoring.reference_corpus.context import (
    ReferenceContextConflict,
    ReferenceContextIntegrityError,
    ReferenceContextSnapshot,
    freeze_reference_context,
    load_reference_context_snapshot,
    project_reference_context_for_prompt,
)
from novel_authoring.reference_corpus.query import (
    ReferenceCorpusQueryEcho,
    ReferenceCorpusQueryRequest,
    ReferenceCorpusQueryResponse,
)


def _card() -> dict[str, object]:
    books = ["book-01", "book-02", "book-03", "book-04"]
    return {
        "card_id": "mechanism-context-test",
        "card_type": "mechanism-card",
        "knowledge_level": "CROSS_BOOK_CONTRAST",
        "status": "REFERENCE_ONLY",
        "source_book_ids": books,
        "category_ids": ["玄幻", "科幻"],
        "creative_problem_tags": ["breakthrough"],
        "reader_experiences": ["BREAKTHROUGH"],
        "narrative_drives": ["POWER_PROGRESSION"],
        "payoff_channels": ["POWER_BREAKTHROUGH"],
        "evidence_scope": "MULTI_CATEGORY",
        "maturity": "SUPPORTED",
        "source_refs": [
            {
                "source_book_id": book,
                "source_id": f"source-{book}",
                "distill_id": f"distill-{book}",
                "segment_id": "segment-0001",
                "line_start": 1,
                "line_end": 3,
            }
            for book in books
        ],
        "metadata_match_fields": ["creative_problem_tags"],
        "creative_problem": "突破如何打开新的行动空间",
        "applicability_conditions": ["回报改变行动空间"],
        "mechanism": "先展示角色实际完成过去不能完成的动作。",
        "reader_payoff": ["读者看到新的可能性"],
        "action_space_effect": ["行动从单一路径变为组合路径"],
        "variants": ["能力试玩"],
        "when_not_to_use": ["只改变数值时"],
        "contrast_cases": ["没有可观察后果时"],
        "failure_risks": ["只讲机制不写现场"],
        "failure_basis": ["OBSERVED_REPETITION"],
    }


def _response(
    package_hash: str = "package-a",
) -> tuple[ReferenceCorpusQueryRequest, ReferenceCorpusQueryResponse]:
    request = ReferenceCorpusQueryRequest(
        purpose="PLANNING",
        creative_problem="突破如何打开新的行动空间",
        creative_problem_tags=["breakthrough"],
        reader_experiences=["BREAKTHROUGH"],
        narrative_drives=["POWER_PROGRESSION"],
        payoff_channels=["POWER_BREAKTHROUGH"],
        max_cards=3,
    )
    response = ReferenceCorpusQueryResponse(
        schema_version="reference-corpus-query-v1",
        purpose="PLANNING",
        query=ReferenceCorpusQueryEcho(
            **request.model_dump(mode="json", exclude={"purpose"})
        ),
        status="ENABLED",
        package_schema_version="reference-corpus-machine-package-v1",
        package_hash=package_hash,
        cards=[_card()],
    )
    return request, response


def test_snapshot_hash_is_stable_and_reference_only(tmp_path: Path) -> None:
    request, response = _response()
    left = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
    )
    right = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
    )
    assert left.snapshot_id == right.snapshot_id
    assert left.snapshot_hash == right.snapshot_hash
    assert left.usage == "REFERENCE_ONLY"
    assert left.selected_card_count == 1
    assert left.selected_card_ids == ["mechanism-context-test"]
    assert "observation_summary" not in json.dumps(left.model_dump(mode="json"))


def test_snapshot_identity_uses_machine_bundle_not_legacy_package_hash() -> None:
    request, response = _response("package-a")
    response.machine_bundle_hash = "bundle-a"
    left = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
    )
    response.package_hash = "package-generated-at-changed"
    right = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
    )
    assert left.snapshot_id == right.snapshot_id
    assert left.snapshot_hash == right.snapshot_hash


def test_snapshot_is_immutable_and_replays_after_package_change(tmp_path: Path) -> None:
    request, response = _response()
    path = tmp_path / "reference_context_snapshot.json"
    frozen = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
        output_path=path,
    )
    changed_request, changed_response = _response("package-b")
    replay = freeze_reference_context(
        changed_request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
        output_path=path,
    )
    assert replay.snapshot_hash == frozen.snapshot_hash
    with pytest.raises(ReferenceContextConflict):
        freeze_reference_context(
            changed_request,
            changed_response,
            book_id="book-under-write",
            edition_id="base",
            operation_id="plan-task-1",
            output_path=path,
        )


def test_strict_snapshot_loader_rejects_tampering(tmp_path: Path) -> None:
    request, response = _response()
    path = tmp_path / "reference_context_snapshot.json"
    freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
        output_path=path,
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["compact_cards"][0]["mechanism"] = "篡改后的机制"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ReferenceContextIntegrityError):
        load_reference_context_snapshot(path)


def test_snapshot_rejects_raw_source_fields() -> None:
    request, response = _response()
    payload = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
    ).model_dump(mode="json")
    payload["compact_cards"][0]["source_quote"] = "不得保存"
    with pytest.raises(ValueError, match="来源正文字段"):
        ReferenceContextSnapshot.model_validate(payload)

    payload["compact_cards"][0].pop("source_quote")
    payload["compact_cards"][0]["full DNA"] = "不得保存"
    with pytest.raises(ValueError, match="来源正文字段"):
        ReferenceContextSnapshot.model_validate(payload)


def test_prompt_projection_keeps_compact_creative_fields_without_provenance() -> None:
    request, response = _response()
    snapshot = freeze_reference_context(
        request,
        response,
        book_id="book-under-write",
        edition_id="base",
        operation_id="plan-task-1",
    )
    payload = snapshot.model_dump(mode="json")
    payload["machine_bundle_hash"] = "bundle-a"
    payload["compact_cards"][0].update(
        {
            "source title": "来源书名",
            "source_id": "source-a",
            "distill_id": "distill-a",
            "segment_id": "segment-0001",
            "line_start": 1,
            "line_end": 3,
            "raw_text": "来源正文",
            "observation_summary": "来源观察",
            "full DNA": "完整 DNA",
            "prose DNA": "完整 prose DNA",
            "nested": {
                "source_book_ids": ["book-a"],
                "mechanism": "嵌套创作字段保留",
                "source_content": "来源内容",
            },
        }
    )

    projected = project_reference_context_for_prompt(payload)
    projected_from_model = project_reference_context_for_prompt(snapshot)

    assert projected["status"] == "ENABLED"
    assert projected["snapshot_id"] == snapshot.snapshot_id
    assert projected["snapshot_hash"] == snapshot.snapshot_hash
    assert projected["machine_bundle_hash"] == "bundle-a"
    assert projected["selected_card_ids"] == ["mechanism-context-test"]
    assert projected_from_model["selected_card_ids"] == snapshot.selected_card_ids
    card = projected["compact_cards"][0]
    assert card["card_type"] == "mechanism-card"
    assert card["knowledge_level"] == "CROSS_BOOK_CONTRAST"
    assert card["mechanism"] == "先展示角色实际完成过去不能完成的动作。"
    assert card["nested"]["mechanism"] == "嵌套创作字段保留"
    for forbidden in (
        "source_refs",
        "source_book_ids",
        "source title",
        "source_id",
        "distill_id",
        "segment_id",
        "line_start",
        "line_end",
        "raw_text",
        "observation_summary",
        "full DNA",
        "prose DNA",
        "source_content",
    ):
        assert forbidden not in json.dumps(projected, ensure_ascii=False)
