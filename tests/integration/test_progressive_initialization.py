from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

import novel_authoring.initialization.service as initialization_service
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
        continuity_ids = list(arc["continuity_chapter_ids"])
        if not chapter_ids and not continuity_ids:
            continue
        output = ArcExtractionOutput(
            initialization_id=str(result["initialization_id"]),
            arc_id=str(arc["arc_id"]),
            chapter_semantic_features=[
                {"chapter_id": chapter_id, "analysis_status": "COMPLETE"}
                for chapter_id in chapter_ids
            ],
            chapter_continuity_deltas=[
                {"chapter_id": chapter_id, "status": "COMPLETE_NO_CHANGE"}
                for chapter_id in continuity_ids
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
        continuity = set(manifest["analysis_plan"]["continuity_index_chapter_ids"])
        for chapter in coverage["chapters"]:
            expected = (
                "PENDING"
                if chapter["chapter_id"] in selected | continuity
                else "UNKNOWN"
            )
            assert chapter["analysis_status"] == expected
    assert deep_counts[InitializationDepth.QUICK] < deep_counts[InitializationDepth.FULL]
    assert deep_counts[InitializationDepth.BALANCED] < deep_counts[InitializationDepth.FULL]
    assert deep_counts[InitializationDepth.FULL] == 30
    quick_manifest = _payload(results[InitializationDepth.QUICK], "initialization_manifest.json")
    balanced_manifest = _payload(
        results[InitializationDepth.BALANCED], "initialization_manifest.json"
    )
    full_manifest = _payload(results[InitializationDepth.FULL], "initialization_manifest.json")
    quick_continuity = set(quick_manifest["analysis_plan"]["continuity_index_chapter_ids"])
    balanced_continuity = set(
        balanced_manifest["analysis_plan"]["continuity_index_chapter_ids"]
    )
    full_continuity = set(full_manifest["analysis_plan"]["continuity_index_chapter_ids"])
    assert len(quick_continuity) < 30
    assert len(balanced_continuity) < 30
    assert len(full_continuity) == 30
    assert set(balanced_manifest["current_boundary_window"]) <= balanced_continuity


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
        continuity_ids = set(arc["continuity_chapter_ids"])
        if not semantic_ids and not continuity_ids:
            continue
        operation = Path(str(arc["operation_input_path"]))
        task_manifest = json.loads(
            (operation / "source_manifest.json").read_text(encoding="utf-8")
        )
        assert set(task_manifest["chapter_ids"]) == semantic_ids | continuity_ids
        packaged.update(task_manifest["chapter_ids"])
    continuity = set(manifest["analysis_plan"]["continuity_index_chapter_ids"])
    assert packaged == selected | continuity


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
    quick_manifest = _payload(quick, "initialization_manifest.json")
    upgraded_manifest = _payload(upgraded, "initialization_manifest.json")
    reused_count = sum(
        len(arc["reused_semantic_chapter_ids"])
        for arc in arc_manifest["arcs"]
    )
    assert reused_count == len(
        set(quick_manifest["deep_chapter_ids"])
        & set(upgraded_manifest["deep_chapter_ids"])
    )
    for arc in arc_manifest["arcs"]:
        scheduled = set(arc["scheduled_semantic_chapter_ids"])
        reused = set(arc["reused_semantic_chapter_ids"])
        assert not scheduled & reused


def _ready_boundary(*args: object, **kwargs: object) -> object:
    del args
    return initialization_service.ContinuationBoundaryReadiness.model_validate(
        {
            "book_id": kwargs["book_id"],
            "edition_id": kwargs["edition_id"],
            "target_chapter_ordinal": kwargs["target_chapter_ordinal"],
            "current_protagonist": {
                "entity_id": "character:hero",
                "confirmed": True,
                "current_state_available": True,
            },
            "active_main_threads": [
                {
                    "thread_id": "thread:current",
                    "confirmed": True,
                    "status": "ACTIVE",
                }
            ],
            "current_world_boundaries": {"confirmed_rules": [{"id": "rule:current"}]},
            "current_character_state": {
                "inventory_ready": True,
                "abilities_ready": True,
                "relationships_ready": True,
                "knowledge_ready": True,
            },
            "current_narrative_state": {"reveal_agenda_ready": True},
            "ready_for_continuation": True,
        }
    )


def test_balanced_prioritizes_boundary_current_arc_and_dependencies(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    result = create_initialization(database, book_id, depth=InitializationDepth.BALANCED)
    manifest = _payload(result, "initialization_manifest.json")
    arcs = _payload(result, "arc_manifest.json")["arcs"]
    continuity = set(manifest["analysis_plan"]["continuity_index_chapter_ids"])
    reasons = manifest["analysis_plan"]["selection_reasons"]

    assert len(continuity) < manifest["chapter_count"]
    assert set(manifest["current_boundary_window"]) <= continuity
    assert set(arcs[-1]["chapter_ids"]) <= continuity
    dependency_ids = {
        chapter_id
        for chapter_id, chapter_reasons in reasons.items()
        if "ACTIVE_DEPENDENCY_RECALL" in chapter_reasons
    }
    assert dependency_ids
    assert dependency_ids <= continuity
    priorities = []
    for arc in arcs:
        if not arc["operation_input_path"]:
            continue
        source_manifest = json.loads(
            (Path(arc["operation_input_path"]) / "source_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        priorities.append((source_manifest["execution_priority"], set(arc["chapter_ids"])))
    boundary_ids = set(manifest["current_boundary_window"])
    assert min(
        priority for priority, chapters in priorities if chapters & boundary_ids
    ) == 1


def test_continuation_capability_is_independent_but_requires_boundary_continuity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(initialization_service, "evaluate_continuation_boundary", _ready_boundary)
    database, book_id = _book(tmp_path)
    created = create_initialization(database, book_id, depth=InitializationDepth.BALANCED)

    blocked = refresh_initialization(database, book_id)
    assert blocked["readiness"]["continuation_boundary"]["ready_for_continuation"] is False
    assert any(
        "Continuation Boundary" in gap
        for gap in blocked["readiness"]["continuation_boundary"]["blocking_gaps"]
    )

    _complete_semantic_tasks(created)
    ready = refresh_initialization(database, book_id)
    assert ready["readiness"]["chapter_semantic_feature_coverage"] < 1.0
    assert ready["readiness"]["continuity_index_coverage"] < 1.0
    assert ready["readiness"]["continuation_boundary"]["ready_for_continuation"] is True
    assert ready["status"]["capabilities"]["continue_from_current_boundary"] is True
    persisted = _payload(created, "initialization_manifest.json")
    assert persisted["capabilities"]["continue_from_current_boundary"] is True


def test_completed_analysis_is_reused_only_for_the_same_source_revision(tmp_path: Path) -> None:
    database, book_id = _book(tmp_path)
    created = create_initialization(database, book_id, depth=InitializationDepth.QUICK)
    _complete_semantic_tasks(created)
    refresh_initialization(database, book_id)
    manifest = _payload(created, "initialization_manifest.json")
    chapter_id = str(manifest["deep_chapter_ids"][0])

    completed = initialization_service._completed_chapter_layers(database, book_id, "base")
    assert chapter_id in completed["LITERARY"]
    assert chapter_id in completed["CONTINUITY"]

    with database.connect() as connection:
        connection.execute(
            "UPDATE chapters SET version=version+1 WHERE chapter_id=?",
            (chapter_id,),
        )
    stale = initialization_service._completed_chapter_layers(database, book_id, "base")
    assert chapter_id not in stale["LITERARY"]
    assert chapter_id not in stale["CONTINUITY"]

    manifest_path = Path(str(created["root"])) / "initialization_manifest.json"
    stale_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    stale_manifest["capabilities"]["continue_from_current_boundary"] = True
    manifest_path.write_text(
        json.dumps(stale_manifest, ensure_ascii=False), encoding="utf-8"
    )
    with database.connect() as connection:
        connection.execute(
            "UPDATE chapters SET content_sha256='changed' WHERE chapter_id=?",
            (chapter_id,),
        )
    refreshed = refresh_initialization(database, book_id)
    assert refreshed["status"]["state"] == "STALE"
    assert refreshed["status"]["capabilities"]["continue_from_current_boundary"] is False
    persisted = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert persisted["capabilities"]["continue_from_current_boundary"] is False


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
