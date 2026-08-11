from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.initialization import (
    InitializationDepth,
    create_initialization,
    prepare_action_deepening,
    refresh_initialization,
    upgrade_initialization,
)
from novel_authoring.initialization.models import ArcExtractionOutput


def _book(tmp_path: Path, count: int = 30) -> tuple[Database, str]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "长篇.md").write_text(
        "\n\n".join(
            f"第{ordinal}章 阶段{(ordinal - 1) // 10 + 1}\n"
            f"角色在第{ordinal}章作出决定。"
            f"{'危险升级并揭示线索。' if ordinal in {7, 14, 21, 28} else '局势继续。'}"
            for ordinal in range(1, count + 1)
        ),
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="depth-book",
        title="深度测试",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
        confirm_order=True,
    )
    return Database(workspace / "depth-book" / "state.sqlite3"), "depth-book"


def _payload(result: dict[str, object], name: str) -> dict[str, object]:
    return json.loads((Path(str(result["root"])) / name).read_text(encoding="utf-8"))


def _complete_semantic_tasks(result: dict[str, object]) -> None:
    root = Path(str(result["root"]))
    arc_manifest = json.loads((root / "arc_manifest.json").read_text(encoding="utf-8"))
    for arc in arc_manifest["arcs"]:
        chapter_ids = list(arc["semantic_chapter_ids"])
        if not chapter_ids:
            continue
        output = ArcExtractionOutput(
            initialization_id=str(result["initialization_id"]),
            arc_id=str(arc["arc_id"]),
            chapter_semantic_features=[
                {"chapter_id": chapter_id, "analysis_status": "COMPLETE"}
                for chapter_id in chapter_ids
            ],
        )
        output_path = root / "arc_outputs" / str(arc["arc_id"]) / "output.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(output.model_dump(mode="json"), ensure_ascii=False),
            encoding="utf-8",
        )


def test_all_depths_keep_full_structure_but_different_semantic_scope(
    tmp_path: Path,
) -> None:
    database, book_id = _book(tmp_path)
    results = {
        depth: create_initialization(database, book_id, depth=depth)
        for depth in InitializationDepth
    }

    deep_counts: dict[InitializationDepth, int] = {}
    for depth, result in results.items():
        manifest = _payload(result, "initialization_manifest.json")
        coverage = _payload(result, "source_coverage.json")
        structural = _payload(result, "structural_index.json")
        assert manifest["initialization_depth"] == depth.value
        assert coverage["chapter_coverage"] == 1.0
        assert len(coverage["chapters"]) == 30
        assert len(structural["chapters"]) == 30
        assert structural["semantic_authority"] == "RECALL_HINT_ONLY"
        assert all(
            hint["information_status"] is None
            for chapter in structural["chapters"]
            for hint in chapter["recall_hints"]
        )
        deep_counts[depth] = len(manifest["deep_chapter_ids"])
        selected = set(manifest["deep_chapter_ids"])
        for chapter in coverage["chapters"]:
            expected = "PENDING" if chapter["chapter_id"] in selected else "UNKNOWN"
            assert chapter["analysis_status"] == expected
    assert deep_counts[InitializationDepth.QUICK] < deep_counts[InitializationDepth.FULL]
    assert deep_counts[InitializationDepth.BALANCED] < deep_counts[InitializationDepth.FULL]
    assert deep_counts[InitializationDepth.QUICK] <= deep_counts[InitializationDepth.BALANCED]
    assert deep_counts[InitializationDepth.FULL] == 30


def test_partial_depth_tasks_only_include_selected_chapters(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    result = create_initialization(database, book_id, depth=InitializationDepth.QUICK)
    manifest = _payload(result, "initialization_manifest.json")
    arc_manifest = _payload(result, "arc_manifest.json")
    selected = set(manifest["deep_chapter_ids"])

    packaged: set[str] = set()
    for arc in arc_manifest["arcs"]:
        semantic_ids = set(arc["semantic_chapter_ids"])
        assert semantic_ids <= selected
        if not semantic_ids:
            continue
        operation = Path(str(arc["operation_input_path"]))
        task_manifest = json.loads(
            (operation / "source_manifest.json").read_text(encoding="utf-8")
        )
        assert set(task_manifest["chapter_ids"]) == semantic_ids
        packaged.update(task_manifest["chapter_ids"])
    assert packaged == selected


def test_arc_semantic_records_require_explicit_information_status() -> None:
    with pytest.raises(ValidationError, match="information_status"):
        ArcExtractionOutput(
            initialization_id="init",
            arc_id="arc",
            characters=[{"name": "甲", "source_span_ids": ["span-1"]}],
        )

    with pytest.raises(ValidationError, match="unknown_boundary"):
        ArcExtractionOutput(
            initialization_id="init",
            arc_id="arc",
            characters=[
                {
                    "name": "甲",
                    "information_status": "INFERENCE",
                    "source_span_ids": ["span-1"],
                    "reasoning_summary": "根据称谓推断",
                    "confidence": 0.6,
                    "counter_evidence": [],
                }
            ],
        )


def test_upgrade_resumes_pending_then_reuses_completed_semantic_chapters(
    tmp_path: Path,
) -> None:
    database, book_id = _book(tmp_path)
    quick = create_initialization(
        database, book_id, depth=InitializationDepth.QUICK
    )

    pending = upgrade_initialization(
        database, book_id, depth=InitializationDepth.BALANCED
    )
    assert pending["upgrade_status"] == "RESUME_REQUIRED"
    assert pending["manifest"]["initialization_id"] == quick["initialization_id"]

    _complete_semantic_tasks(quick)
    upgraded = upgrade_initialization(
        database, book_id, depth=InitializationDepth.BALANCED
    )
    assert upgraded["upgrade_status"] == "UPGRADE_CREATED"
    assert upgraded["upgrade_from_initialization_id"] == quick["initialization_id"]
    arc_manifest = _payload(upgraded, "arc_manifest.json")
    reused_count = sum(
        len(arc["reused_semantic_chapter_ids"])
        for arc in arc_manifest["arcs"]
    )
    assert reused_count == quick["deep_chapter_count"]
    for arc in arc_manifest["arcs"]:
        scheduled = set(arc["scheduled_semantic_chapter_ids"])
        reused = set(arc["reused_semantic_chapter_ids"])
        assert not scheduled & reused


def test_rewrite_deepening_targets_unknown_chapter_and_dependencies(
    tmp_path: Path,
) -> None:
    database, book_id = _book(tmp_path)
    quick = create_initialization(
        database, book_id, depth=InitializationDepth.QUICK
    )
    _complete_semantic_tasks(quick)
    manifest = _payload(quick, "initialization_manifest.json")
    target = str(manifest["uncovered_semantic_chapter_ids"][0])

    result = prepare_action_deepening(
        database,
        book_id,
        action="REWRITE",
        target_chapter_id=target,
    )

    assert result["status"] == "ACTION_DEEPENING_CREATED"
    assert target in result["required_chapter_ids"]
    assert result["requested_action"] == "REWRITE"
    deepened = _payload(result, "initialization_manifest.json")
    assert target in deepened["deep_chapter_ids"]


def test_refresh_rejects_source_span_from_outside_arc(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    created = create_initialization(
        database, book_id, depth=InitializationDepth.QUICK
    )
    root = Path(str(created["root"]))
    arcs = _payload(created, "arc_manifest.json")["arcs"]
    first, second = arcs[0], arcs[1]
    with database.connect() as connection:
        invalid_span = connection.execute(
            "SELECT span_id FROM source_spans WHERE chapter_id=?",
            (second["chapter_ids"][0],),
        ).fetchone()["span_id"]
    output = ArcExtractionOutput(
        initialization_id=str(created["initialization_id"]),
        arc_id=str(first["arc_id"]),
        characters=[
            {
                "name": "越界人物",
                "information_status": "CANON",
                "source_span_ids": [str(invalid_span)],
            }
        ],
    )
    output_path = root / "arc_outputs" / str(first["arc_id"]) / "output.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output.model_dump(mode="json"), ensure_ascii=False),
        encoding="utf-8",
    )

    refreshed = refresh_initialization(database, book_id)

    assert first["arc_id"] in refreshed["status"]["failed_arc_ids"]
    error = json.loads(
        (output_path.parent / "validation_error.json").read_text(encoding="utf-8")
    )
    assert "不属于该 Book/Arc" in error["error"]
