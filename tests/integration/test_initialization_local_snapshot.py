from __future__ import annotations

import json
from pathlib import Path

from novel_authoring.atlas.offline import export_snapshot
from novel_authoring.atlas.visuals import render_atlas_visuals
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.initialization.service import (
    calculate_source_coverage,
    create_initialization,
)
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    complete_handoff,
    create_initialization_handoff,
    start_handoff,
)


def _book(tmp_path: Path, count: int = 24) -> tuple[Database, str]:
    source = tmp_path / "source"
    source.mkdir()
    source_file = source / "novel.md"
    source_file.write_text(
        "".join(
            f"# 第{ordinal}章 章节{ordinal}\n主角继续观察与选择。\n\n"
            for ordinal in range(1, count + 1)
        ),
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="init-book",
        title="初始化测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
        confirm_order=True,
    )
    return Database(workspace / "init-book" / "state.sqlite3"), "init-book"


def test_initialization_maps_every_chapter_and_does_not_build_planning_aggregate(
    tmp_path: Path,
) -> None:
    database, book_id = _book(tmp_path)
    source_coverage = calculate_source_coverage(database, book_id, "base")
    assert source_coverage["status"] == "FULL"
    assert source_coverage["chapter_coverage"] == 1.0

    before = int(database.scalar("SELECT COUNT(*) FROM planning_aggregates") or 0)
    result = create_initialization(database, book_id, edition_id="base", char_limit=2_000)
    after = int(database.scalar("SELECT COUNT(*) FROM planning_aggregates") or 0)
    assert before == after == 0
    assert result["chapter_count"] == 24
    assert result["arc_count"] >= 2

    root = Path(result["root"])
    coverage = json.loads((root / "source_coverage.json").read_text(encoding="utf-8"))
    arcs = json.loads((root / "arc_manifest.json").read_text(encoding="utf-8"))["arcs"]
    assignments = [item["assigned_arc_id"] for item in coverage["chapters"]]
    assert len(assignments) == len(set(item["chapter_id"] for item in coverage["chapters"]))
    assert all(1 <= len(item["chapter_ids"]) <= 20 for item in arcs)
    assigned_by_arc = {arc["arc_id"]: set(arc["chapter_ids"]) for arc in arcs}
    assert set().union(*assigned_by_arc.values()) == {
        item["chapter_id"] for item in coverage["chapters"]
    }
    assert all(item["assigned_arc_id"] in assigned_by_arc for item in coverage["chapters"])

    handoff = create_initialization_handoff(
        database,
        book_id,
        edition_id="base",
        requested_stage="NOVEL_INITIALIZATION",
    )
    assert handoff["status"]["status"] == "READY_FOR_CODEX"
    assert int(database.scalar("SELECT COUNT(*) FROM planning_aggregates") or 0) == 0


def test_initialization_synthetic_handoff_uses_scheduled_manifests_only(
    tmp_path: Path,
) -> None:
    database, book_id = _book(tmp_path)
    prepared = create_initialization(database, book_id, edition_id="base")
    handoff = create_initialization_handoff(
        database,
        book_id,
        edition_id="base",
        requested_stage="NOVEL_INITIALIZATION",
    )
    task_directory = Path(str(handoff["task_directory"]))
    input_root = (
        task_directory / "input"
        if (task_directory / "input").is_dir()
        else task_directory
    )
    task = json.loads(
        (input_root / "task.json").read_text(encoding="utf-8")
    )
    assert task["executor_skill"] == "initialize-existing-novel"
    assert task["business_input_files"] == [
        "initialization_manifest.json",
        "arc_manifest.json",
    ]
    assert all(
        (input_root / name).is_file()
        for name in task["business_input_files"]
    )
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(
        json.dumps(
            {
                "handoff_id": str(handoff["handoff_id"]),
                "handoff_type": "NOVEL_INITIALIZATION",
                "requested_stage": "NOVEL_INITIALIZATION",
                "completed_stage": "INITIALIZATION_READY",
                "book_id": book_id,
                "edition_id": "base",
                "status": "COMPLETED",
                "initialization_id": prepared["initialization_id"],
                "readiness": "FULL_READY",
                "canon_committed": False,
                "edition_activated": False,
                "base_event_seq": task["base_event_seq"],
                "base_projection_hash": task["base_projection_hash"],
            }
        ),
        encoding="utf-8",
    )
    completed = complete_handoff(
        database,
        str(handoff["handoff_id"]),
        str(started["claim_token"]),
        result_path,
    )
    assert completed["status"] == HandoffStatus.COMPLETED.value


def test_visuals_and_offline_snapshot_are_self_contained(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path, count=3)
    artifact_root = tmp_path / "artifact"
    (artifact_root / "graphs").mkdir(parents=True)
    visuals = render_atlas_visuals(artifact_root)
    assert len(visuals) == 7
    assert all((artifact_root / path).is_file() for path in visuals)
    visual_status = json.loads(
        (artifact_root / "visuals" / "visual_status.json").read_text(encoding="utf-8")
    )
    assert all(item["status"] == "EMPTY_SOURCE_GRAPH" for item in visual_status.values())

    initialization = create_initialization(database, book_id, edition_id="base")
    snapshot = export_snapshot(
        database,
        book_id,
        edition_id="base",
        output_root=tmp_path / "snapshot",
    )
    index = Path(snapshot["index"])
    assert index.is_file()
    assert (index.parent / "snapshot_manifest.json").is_file()
    assert "fetch(" not in index.read_text(encoding="utf-8")
    assert snapshot["chapter_count"] == 3
    assert snapshot["initialization_id"] == initialization["initialization_id"]
