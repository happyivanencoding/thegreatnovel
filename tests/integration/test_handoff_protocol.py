from __future__ import annotations

import json
from pathlib import Path

import pytest

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.utils import utc_now
from novel_authoring.workflows.handoffs import (
    HANDOFF_BUSINESS_INPUT_FILES,
    HANDOFF_DEPENDENCIES,
    HANDOFF_EXECUTOR_SKILLS,
    HandoffStatus,
    HandoffType,
    HandoffWorkflowError,
    claim_handoff,
    complete_handoff,
    create_continuation_handoff,
    create_handoff,
    get_handoff,
    load_completed_handoff_result,
    start_handoff,
    update_handoff_status,
)

FIXTURE = Path(__file__).parents[1] / "fixtures" / "合成求生小说.md"


def test_handoff_files_claim_and_result_boundary(tmp_path: Path) -> None:
    source = tmp_path / "book"
    source.mkdir()
    (source / FIXTURE.name).write_bytes(FIXTURE.read_bytes())
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="handoff-book",
        title="合成求生小说",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "handoff-book" / "state.sqlite3")
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO rhythm_diagnostic_snapshots(
                snapshot_id, book_id, edition_id, as_of_chapter, as_of_event_seq,
                projection_hash, config_hash, analyzer_versions_json, snapshot_json, created_at
            ) VALUES (
                'rhythm-test', 'handoff-book', 'base', 3, 0,
                'projection', 'config', '{}', '{}', ?
            )
            """,
            (utc_now(),),
        )
    handoff = create_continuation_handoff(
        database, "handoff-book", requested_stage="PLAN_ONLY"
    )
    task_directory = Path(handoff["task_directory"])
    assert (task_directory / "task.json").is_file()
    task = json.loads((task_directory / "task.json").read_text(encoding="utf-8"))
    assert task["forbidden_actions"]
    claimed = claim_handoff(database, handoff["handoff_id"], "codex-desktop")
    assert claimed["status"] == HandoffStatus.CLAIMED
    with pytest.raises(HandoffWorkflowError):
        claim_handoff(database, handoff["handoff_id"], "second-thread")
    update_handoff_status(
        database,
        handoff["handoff_id"],
        HandoffStatus.RUNNING,
        claim_token=claimed["claim_token"],
    )
    with pytest.raises(HandoffWorkflowError):
        update_handoff_status(
            database,
            handoff["handoff_id"],
            HandoffStatus.COMPLETED,
            claim_token=claimed["claim_token"],
            result={
                "status": "VALIDATED_DRAFT",
                "canon_committed": True,
                "edition_activated": False,
            },
        )


def _continuation_handoff(tmp_path: Path) -> tuple[Database, dict[str, object]]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    source = tmp_path / "book"
    source.mkdir()
    (source / FIXTURE.name).write_bytes(FIXTURE.read_bytes())
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="fast-path-book",
        title="合成求生小说",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "fast-path-book" / "state.sqlite3")
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO rhythm_diagnostic_snapshots(
                snapshot_id, book_id, edition_id, as_of_chapter, as_of_event_seq,
                projection_hash, config_hash, analyzer_versions_json, snapshot_json, created_at
            ) VALUES ('rhythm-fast', 'fast-path-book', 'base', 3, 0,
                      'projection', 'config', '{}', '{}', ?)
            """,
            (utc_now(),),
        )
    return database, create_continuation_handoff(
        database, "fast-path-book", requested_stage="PLAN_ONLY"
    )


def _plan_result(database: Database, handoff_id: str) -> dict[str, object]:
    frozen = get_handoff(database, handoff_id)
    return {
        "handoff_id": handoff_id,
        "handoff_type": "CONTINUATION",
        "requested_stage": "PLAN_ONLY",
        "completed_stage": "PLANNED",
        "book_id": str(frozen["book_id"]),
        "edition_id": str(frozen["edition_id"]),
        "status": "COMPLETED",
        "candidate_ids": ["candidate-fast-1", "candidate-fast-2", "candidate-fast-3"],
        "canon_committed": False,
        "edition_activated": False,
        "base_event_seq": int(frozen["base_event_seq"]),
        "base_projection_hash": str(frozen["base_projection_hash"]),
    }


def test_every_handoff_type_has_one_executor_and_protocol_has_no_business_router() -> None:
    assert set(HANDOFF_EXECUTOR_SKILLS) == set(HandoffType)
    assert set(HANDOFF_BUSINESS_INPUT_FILES) == set(HandoffType)
    assert (
        HANDOFF_EXECUTOR_SKILLS[HandoffType.SOURCE_STATE_HYDRATION]
        == "hydrate-source-state"
    )
    assert (
        HANDOFF_EXECUTOR_SKILLS[HandoffType.PROFILE_REANALYSIS]
        == "reanalyze-book-profile"
    )
    assert (
        HANDOFF_EXECUTOR_SKILLS[HandoffType.KERNEL_CONTRACT_DISCOVERY]
        == "discover-kernel-contracts"
    )
    assert not (
        HANDOFF_DEPENDENCIES[HandoffType.ORIGINAL_BOOK_BOOTSTRAP]
        & {"metrics", "rhythm", "atlas"}
    )
    skill_root = Path(__file__).parents[2] / ".agents" / "skills"
    for skill_name in {
        "hydrate-source-state",
        "reanalyze-book-profile",
        "discover-kernel-contracts",
    }:
        text = (skill_root / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "workflow start" in text
        assert "process-novel-handoff" not in text
    process_skill = (
        skill_root / "process-novel-handoff" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "HandoffType" not in process_skill
    assert "executor_skill=process-novel-handoff" not in process_skill


def test_workflow_start_is_one_claim_and_running_transition(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]), "fast-path-a")

    assert started["status"] == HandoffStatus.RUNNING.value
    assert started["executor_skill"] == "continue-novel"
    assert started["result_target"]
    assert set(started) == {
        "handoff_id",
        "status",
        "claim_token",
        "executor_skill",
        "task_directory",
        "business_input_files",
        "result_target",
    }
    frozen = get_handoff(database, str(handoff["handoff_id"]))
    assert frozen["status"] == HandoffStatus.RUNNING.value
    assert [event["event_type"] for event in frozen["events"]][-2:] == ["CLAIMED", "RUNNING"]
    with pytest.raises(HandoffWorkflowError):
        start_handoff(database, str(handoff["handoff_id"]), "fast-path-b")


def test_workflow_start_marks_frozen_input_drift_stale(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    task_path = Path(str(handoff["task_directory"])) / "task.json"
    task_path.write_text(task_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(HandoffWorkflowError, match="漂移"):
        start_handoff(database, str(handoff["handoff_id"]))
    assert get_handoff(database, str(handoff["handoff_id"]))["status"] == HandoffStatus.STALE.value


def test_profile_reanalysis_stales_when_effective_edition_content_changes(
    tmp_path: Path,
) -> None:
    database, _ = _continuation_handoff(tmp_path)
    handoff = create_handoff(
        database,
        "fast-path-book",
        handoff_type=HandoffType.PROFILE_REANALYSIS,
        requested_stage="PROFILE_REANALYSIS",
    )
    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads((task_directory / "task.json").read_text(encoding="utf-8"))
    assert task["business_input_files"] == ["profile_context.json"]
    assert all(
        (task_directory / name).is_file() for name in task["business_input_files"]
    )

    with database.connect() as connection:
        connection.execute(
            "UPDATE chapters SET content_sha256='changed-after-freeze' "
            "WHERE book_id=? AND ordinal=(SELECT MAX(ordinal) FROM chapters WHERE book_id=?)",
            ("fast-path-book", "fast-path-book"),
        )

    with pytest.raises(HandoffWorkflowError, match="effective chapter hash changed"):
        start_handoff(database, str(handoff["handoff_id"]))
    assert get_handoff(database, str(handoff["handoff_id"]))["status"] == "STALE"


def test_workflow_complete_rejects_invalid_and_detects_runtime_drift(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(json.dumps({"invalid": True}), encoding="utf-8")
    with pytest.raises(HandoffWorkflowError):
        complete_handoff(
            database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
        )
    assert (
        get_handoff(database, str(handoff["handoff_id"]))["status"]
        == HandoffStatus.FAILED.value
    )

    database, handoff = _continuation_handoff(tmp_path / "runtime-drift")
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(
        json.dumps(_plan_result(database, str(handoff["handoff_id"]))), encoding="utf-8"
    )
    with database.connect() as connection:
        connection.execute(
            "UPDATE editions SET status='ARCHIVED' WHERE book_id=? AND edition_id='base'",
            ("fast-path-book",),
        )
    with pytest.raises(HandoffWorkflowError, match="漂移"):
        complete_handoff(
            database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
        )
    assert (
        get_handoff(database, str(handoff["handoff_id"]))["status"]
        == HandoffStatus.STALE.value
    )


def test_workflow_complete_valid_result_is_authority(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(
        json.dumps(_plan_result(database, str(handoff["handoff_id"]))), encoding="utf-8"
    )

    completed = complete_handoff(
        database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
    )
    assert completed["status"] == HandoffStatus.COMPLETED.value
    assert (
        get_handoff(database, str(handoff["handoff_id"]))["status"]
        == HandoffStatus.COMPLETED.value
    )


def test_completed_result_loader_uses_persisted_validated_envelope(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(
        json.dumps(_plan_result(database, str(handoff["handoff_id"]))), encoding="utf-8"
    )
    complete_handoff(
        database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
    )
    result_path.write_text(json.dumps({"not": "the persisted envelope"}), encoding="utf-8")

    loaded = load_completed_handoff_result(database, str(handoff["handoff_id"]))
    assert loaded["handoff_id"] == handoff["handoff_id"]
    assert loaded["candidate_ids"] == [
        "candidate-fast-1",
        "candidate-fast-2",
        "candidate-fast-3",
    ]
