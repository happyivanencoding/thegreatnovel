from __future__ import annotations

import json
import tomllib
from datetime import UTC, datetime, timedelta
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
    heartbeat_handoff,
    load_completed_handoff_result,
    recover_stale_runners,
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


def _plan_result() -> dict[str, object]:
    return {
        "completed_stage": "PLANNED",
        "candidate_ids": ["candidate-fast-1", "candidate-fast-2", "candidate-fast-3"],
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
    assert "--library-root" in process_skill
    assert "不得通过当前工作目录" in process_skill


def test_novel_handoff_runner_is_one_handoff_protocol_boundary() -> None:
    config_path = (
        Path(__file__).parents[2]
        / ".codex"
        / "agents"
        / "novel-handoff-runner.toml"
    )
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))

    required_keys = {"name", "description", "developer_instructions"}
    assert required_keys <= set(config)
    assert config["name"] == "novel_handoff_runner"
    instructions = config["developer_instructions"]
    for required_fact in {
        "$process-novel-handoff",
        "library_root",
        "book_id",
        "handoff_id",
        "executor_skill",
        "business_input_files",
        "result_target",
        "claim_token",
        "workflow complete",
        "一次 Agent invocation 只处理一个 handoff",
    }:
        assert required_fact in instructions
    assert "不得从 cwd" in instructions
    assert "不得通过 workflow list/jobs" in instructions
    assert "不领取下一个 handoff" in instructions
    assert "HandoffType" not in instructions
    assert not any(
        executor in instructions for executor in HANDOFF_EXECUTOR_SKILLS.values()
    )


def test_reader_kernel_skill_uses_frozen_proposal_schema_authority() -> None:
    skill_path = (
        Path(__file__).parents[2]
        / ".agents"
        / "skills"
        / "interpret-original-reader-kernel"
        / "SKILL.md"
    )
    skill = skill_path.read_text(encoding="utf-8")

    assert "task.json.original_reader_interpretation.proposal_schema" in skill
    assert "不得自行选择、升级、降级或兼容 schema version" in skill
    assert "original-reader-kernel-v2" not in skill


def test_workflow_start_is_one_claim_and_running_transition(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]), "fast-path-a")

    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads((task_directory / "task.json").read_text(encoding="utf-8"))
    prompt = (task_directory / "prompt.md").read_text(encoding="utf-8")

    assert started["status"] == HandoffStatus.RUNNING.value
    assert started["executor_skill"] == task["executor_skill"] == "continue-novel"
    assert f'${started["executor_skill"]}' in prompt
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
    output_schema = json.loads(
        Path(str(frozen["output_schema_path"])).read_text(encoding="utf-8")
    )
    assert set(output_schema["required"]) == {"completed_stage"}
    assert output_schema["x-stage-rules"]["PLAN_ONLY"]["system_derived"] == [
        "candidate_ids",
        "task_ids",
    ]
    with pytest.raises(HandoffWorkflowError):
        start_handoff(database, str(handoff["handoff_id"]), "fast-path-b")


def test_runner_heartbeat_prevents_stale_reclaim(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]), "heartbeat-runner")
    heartbeat = heartbeat_handoff(
        database,
        str(handoff["handoff_id"]),
        str(started["claim_token"]),
        current_phase="GENERATING",
        last_progress="已完成场景骨架",
    )

    heartbeat_at = datetime.fromisoformat(str(heartbeat["heartbeat_at"]))
    future = heartbeat_at.astimezone(UTC) + timedelta(seconds=299)
    assert recover_stale_runners(
        database,
        timeout_seconds=300,
        now=future.isoformat(),
    ) == []
    frozen = get_handoff(database, str(handoff["handoff_id"]))
    assert frozen["status"] == HandoffStatus.RUNNING.value
    assert frozen["events"][-1]["event_type"] == "HEARTBEAT"


def test_runner_without_heartbeat_is_reclaimed(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]), "stale-runner")
    now = datetime.now(UTC) + timedelta(seconds=301)

    reclaimed = recover_stale_runners(
        database,
        timeout_seconds=300,
        now=now.isoformat(),
    )
    assert reclaimed == [
        {
            "handoff_id": str(handoff["handoff_id"]),
            "status": HandoffStatus.STALE.value,
            "reason": "STALE_RUNNER_TIMEOUT",
            "last_activity": reclaimed[0]["last_activity"],
            "age_seconds": reclaimed[0]["age_seconds"],
        }
    ]
    assert get_handoff(database, str(handoff["handoff_id"]))["status"] == HandoffStatus.STALE.value
    assert started["status"] == HandoffStatus.RUNNING.value


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


def test_workflow_complete_invalid_business_result_is_retryable(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    invalid_result = {
        "candidate_ids": ["candidate-fast-1", "candidate-fast-2", "candidate-fast-3"]
    }
    result_path.write_text(json.dumps(invalid_result), encoding="utf-8")

    with pytest.raises(HandoffWorkflowError) as excinfo:
        complete_handoff(
            database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
        )
    assert str(excinfo.value).startswith("RESULT_INVALID:")
    assert "completed_stage" in str(excinfo.value)

    frozen = get_handoff(database, str(handoff["handoff_id"]))
    assert frozen["status"] == HandoffStatus.RUNNING.value
    assert frozen["claim_token"] == started["claim_token"]
    assert "FAILED" not in [event["event_type"] for event in frozen["events"]]
    assert json.loads(result_path.read_text(encoding="utf-8")) == invalid_result
    status = json.loads(
        (Path(str(handoff["task_directory"])) / "status.json").read_text(encoding="utf-8")
    )
    assert status["status"] == HandoffStatus.RUNNING.value
    assert "completed_stage" in status["result_validation_error"]

    result_path.write_text(json.dumps(_plan_result()), encoding="utf-8")
    completed = complete_handoff(
        database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
    )
    assert completed["status"] == HandoffStatus.COMPLETED.value


@pytest.mark.parametrize(
    ("field", "wrong_value"),
    [("book_id", "wrong-book"), ("base_projection_hash", "wrong-projection")],
)
def test_workflow_complete_deterministic_conflict_is_retryable(
    tmp_path: Path, field: str, wrong_value: str
) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result = _plan_result()
    result[field] = wrong_value
    result_path.write_text(json.dumps(result), encoding="utf-8")

    with pytest.raises(HandoffWorkflowError, match=field):
        complete_handoff(
            database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
        )
    assert get_handoff(database, str(handoff["handoff_id"]))["status"] == "RUNNING"

    result.pop(field)
    result_path.write_text(json.dumps(result), encoding="utf-8")
    completed = complete_handoff(
        database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
    )
    assert completed["status"] == HandoffStatus.COMPLETED.value


def test_workflow_complete_runtime_drift_still_becomes_stale(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path / "runtime-drift")
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(json.dumps(_plan_result()), encoding="utf-8")
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
    result_path.write_text(json.dumps(_plan_result()), encoding="utf-8")

    completed = complete_handoff(
        database, str(handoff["handoff_id"]), str(started["claim_token"]), result_path
    )
    assert completed["status"] == HandoffStatus.COMPLETED.value
    assert (
        get_handoff(database, str(handoff["handoff_id"]))["status"]
        == HandoffStatus.COMPLETED.value
    )
    frozen = get_handoff(database, str(handoff["handoff_id"]))
    persisted = load_completed_handoff_result(database, str(handoff["handoff_id"]))
    assert persisted["handoff_id"] == handoff["handoff_id"]
    assert persisted["handoff_type"] == HandoffType.CONTINUATION.value
    assert persisted["book_id"] == frozen["book_id"]
    assert persisted["edition_id"] == frozen["edition_id"]
    assert persisted["requested_stage"] == frozen["requested_stage"]
    assert persisted["status"] == HandoffStatus.COMPLETED.value
    assert persisted["base_event_seq"] == frozen["base_event_seq"]
    assert persisted["base_projection_hash"] == frozen["base_projection_hash"]
    assert persisted["canon_committed"] is False
    assert persisted["edition_activated"] is False


def test_completed_result_loader_uses_persisted_validated_envelope(tmp_path: Path) -> None:
    database, handoff = _continuation_handoff(tmp_path)
    started = start_handoff(database, str(handoff["handoff_id"]))
    result_path = Path(str(started["result_target"]))
    result_path.write_text(json.dumps(_plan_result()), encoding="utf-8")
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
