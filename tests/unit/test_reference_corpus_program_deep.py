from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from novel_authoring.reference_corpus.program_deep import (
    ProgramDeepError,
    _reject_obvious_template_rows,
    compile_machine_package,
    initialize_program_deep,
    merge_worker_artifacts,
    validate_program_deep,
)


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    corpus = tmp_path / "corpus"
    operations = tmp_path / "operations"
    output = tmp_path / "output"
    raw = tmp_path / "raw"
    source_book_id = "rcv0-test-book"
    source_id = "book-01-test"
    distill_id = "distill-test"

    (corpus / "selection").mkdir(parents=True)
    (corpus / "machine" / "manifests").mkdir(parents=True)
    (operations / "preparations" / source_book_id / "index").mkdir(parents=True)
    (operations / "preparations" / source_book_id / "normalized").mkdir(parents=True)
    raw.mkdir()
    normalized = operations / "preparations" / source_book_id / "normalized" / f"{source_id}.txt"
    normalized.write_text("第一章\n甲\n第二章\n乙\n", encoding="utf-8")
    raw_file = raw / "test.txt"
    raw_file.write_text("raw", encoding="utf-8")
    segments = [
        {
            "segment_id": "segment-0001",
            "ordinal": 1,
            "heading": "第一章",
            "start_line": 1,
            "end_line": 2,
            "start_char": 0,
            "end_char": 4,
            "char_count": 4,
        },
        {
            "segment_id": "segment-0002",
            "ordinal": 2,
            "heading": "第二章",
            "start_line": 3,
            "end_line": 4,
            "start_char": 4,
            "end_char": 8,
            "char_count": 4,
        },
    ]
    index_source = {
        "input_path": str(raw_file),
        "normalized_path": str(normalized),
        "lines": 4,
        "segment_count": 2,
        "segments": segments,
    }
    (operations / "preparations" / source_book_id / "chapter_index.json").write_text(
        json.dumps(
            {"schema_version": "distill-chapter-index-v1", "sources": [index_source]},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (corpus / "machine" / "manifests" / f"{source_book_id}.json").write_text(
        json.dumps(
            {
                "source_book_id": source_book_id,
                "source_id": source_id,
                "distill_id": distill_id,
                "title": "测试书",
                "category": "测试",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (corpus / "selection" / "corpus-sources-v0.confirmed.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "reference-corpus-source-freeze-v1",
                "source_count": 1,
                "sources": [
                    {
                        "source_book_id": source_book_id,
                        "source_path": "test.txt",
                        "parse_warning": "",
                    }
                ],
            },
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    return corpus, operations, output, raw


def test_initialize_validate_and_compile_pending_package(tmp_path: Path) -> None:
    corpus, operations, output, raw = _fixture(tmp_path)

    created = initialize_program_deep(corpus, operations, output, raw_root=raw)
    assert created["source_count"] == 1
    validation = validate_program_deep(corpus, operations, output)
    assert validation["valid"] is True
    assert validation["canonical_unit_count"] == 2
    assert validation["pending_semantic_rows"] == 2

    package = compile_machine_package(corpus, operations, output)
    assert package["status"] == "IN_PROGRESS"
    assert package["raw_text_included"] is False
    assert package["canon_committed"] is False


def test_merge_worker_row_requires_exact_locator(tmp_path: Path) -> None:
    corpus, operations, output, _ = _fixture(tmp_path)
    initialize_program_deep(corpus, operations, output)
    workers = tmp_path / "workers" / "worker-01"
    workers.mkdir(parents=True)
    valid = {
        "schema_version": "story-program-chapter-ledger-v1",
        "source_book_id": "rcv0-test-book",
        "source_chapter_id": "segment-0001",
        "chapter_ordinal": 1,
        "source_locator": {
            "source_book_id": "rcv0-test-book",
            "source_id": "book-01-test",
            "distill_id": "distill-test",
            "segment_id": "segment-0001",
            "line_start": 1,
            "line_end": 2,
        },
        "coverage_status": "SEMANTIC_COMPLETE",
        "one_line_story": "主角完成第一次选择并打开下一步行动。",
        "primary_function": "首次能力验证",
        "protagonist_goal": "确认能力边界",
        "pressure_or_opportunity": "出现新的机会",
        "choice_or_action": "主动选择并执行",
        "immediate_result": "行动空间扩大",
        "reader_payoff_channels": ["POWER_VERIFICATION"],
        "immediate_upside": {"gained": "一次可见验证", "freedom_opened": "新的行动"},
        "state_deltas": {"action_space": "从不可行变为可行"},
    }
    (workers / "chapter-ledger.jsonl").write_text(
        json.dumps(valid, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    merged = merge_worker_artifacts(corpus, operations, output, tmp_path / "workers")
    assert merged["books_with_ledger_updates"] == ["rcv0-test-book"]
    validation = validate_program_deep(corpus, operations, output)
    assert validation["semantic_complete_rows"] == 1
    assert validation["pending_semantic_rows"] == 1

    invalid = dict(valid)
    invalid["source_locator"] = dict(valid["source_locator"])
    invalid["source_locator"]["line_end"] = 99
    bad_worker = tmp_path / "workers" / "worker-bad"
    bad_worker.mkdir()
    (bad_worker / "chapter-ledger.jsonl").write_text(json.dumps(invalid) + "\n", encoding="utf-8")
    with pytest.raises(ProgramDeepError, match="line locator"):
        merge_worker_artifacts(corpus, operations, output, tmp_path / "workers")


def test_template_quality_gate_rejects_repeated_story_skeleton() -> None:
    rows = [
        {
            "coverage_status": "SEMANTIC_COMPLETE",
            "one_line_story": "本段把局部文本显示并置在当前局面的局部推进中。",
        }
        for _ in range(20)
    ]
    with pytest.raises(ProgramDeepError, match="模板化"):
        _reject_obvious_template_rows("rcv0-test-book", rows)
