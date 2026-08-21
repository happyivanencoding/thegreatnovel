from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.run_ledger import (
    activate_optional_repair,
    adopt_final_source,
    create_or_load_run,
    load_run,
    mark_node_failed,
    next_actionable_node,
    save_node_prompt,
    save_node_response,
    skip_integrator_if_no_patches,
)
from story_mvp.storage import create_book


def _complete_core(book_dir: Path, chapter: int = 1) -> None:
    for node in ("director", "curator", "primary"):
        save_node_prompt(book_dir, chapter, node, f"{node} prompt")
        save_node_response(book_dir, chapter, node, f"{node} response")
    adopt_final_source(book_dir, chapter, "primary")
    save_node_prompt(book_dir, chapter, "state_delta", "state delta prompt")
    save_node_response(book_dir, chapter, "state_delta", "state delta response")


def test_curator_primary_initial_nodes_and_core_next_sequence(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    manifest = create_or_load_run(book_dir, 1)

    assert manifest["writer_mode"] == "curator_primary"
    assert manifest["selected_specialists"] == []
    assert manifest["final_source"] is None
    assert manifest["nodes"]["director"]["status"] == "pending"
    assert manifest["nodes"]["curator"]["status"] == "pending"
    assert manifest["nodes"]["primary"]["status"] == "pending"
    assert manifest["nodes"]["state_delta"]["status"] == "pending"
    for node in ("opening", "dialogue", "action", "emotion", "integrator"):
        assert manifest["nodes"][node]["status"] == "skipped"

    assert next_actionable_node(book_dir, 1) == "director"
    for node in ("director", "curator", "primary"):
        save_node_prompt(book_dir, 1, node, f"{node} prompt")
        save_node_response(book_dir, 1, node, f"{node} response")
        if node == "director":
            assert next_actionable_node(book_dir, 1) == "curator"
        elif node == "curator":
            assert next_actionable_node(book_dir, 1) == "primary"

    assert next_actionable_node(book_dir, 1) == "state_delta"
    adopt_final_source(book_dir, 1, "primary")
    assert next_actionable_node(book_dir, 1) == "state_delta"


def test_curator_primary_rejects_specialists_at_run_creation(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)

    try:
        create_or_load_run(
            book_dir,
            1,
            writer_mode="curator_primary",
            selected_specialists=["action"],
        )
    except ValueError as error:
        assert "Primary" in str(error)
    else:
        raise AssertionError("curator_primary must reject creation-time specialists")
    assert not (book_dir / "runs" / "chapter-0001" / "manifest.json").exists()


def test_existing_legacy_manifest_is_not_overwritten_by_new_default(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1, writer_mode="hybrid_selective")

    loaded = create_or_load_run(book_dir, 1)

    assert loaded["writer_mode"] == "hybrid_selective"


def test_optional_repair_requires_primary_and_does_not_mutate_before_primary(
    tmp_path: Path,
) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1, writer_mode="curator_primary")
    before = load_run(book_dir, 1)

    try:
        activate_optional_repair(book_dir, 1, ["action"])
    except ValueError as error:
        assert "Primary" in str(error)
    else:
        raise AssertionError("repair must require a completed Primary")
    assert load_run(book_dir, 1) == before


def test_optional_repair_no_patch_keeps_primary_and_recompletes_run(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1, writer_mode="curator_primary")
    _complete_core(book_dir)
    assert load_run(book_dir, 1)["run_status"] == "completed"

    activated = activate_optional_repair(book_dir, 1, ["action"])
    assert activated["run_status"] == "in_progress"
    assert activated["nodes"]["action"]["status"] == "pending"
    assert activated["nodes"]["integrator"]["status"] == "pending"
    assert activated["nodes"]["state_delta"]["status"] == "completed"

    save_node_prompt(book_dir, 1, "action", "action prompt")
    response = "# Action Specialist\n没有需要修改的 Patch。"
    save_node_response(book_dir, 1, "action", response)
    settled = skip_integrator_if_no_patches(book_dir, 1, {"action": response})

    assert settled["nodes"]["integrator"]["status"] == "skipped"
    assert settled["final_source"] == "primary"
    assert settled["run_status"] == "completed"


def test_optional_repair_supports_multiple_explicit_specialists(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1)
    _complete_core(book_dir)

    activated = activate_optional_repair(book_dir, 1, ["dialogue", "action"])

    assert activated["nodes"]["dialogue"]["status"] == "pending"
    assert activated["nodes"]["action"]["status"] == "pending"
    assert activated["nodes"]["opening"]["status"] == "skipped"
    assert activated["nodes"]["emotion"]["status"] == "skipped"
    assert activated["nodes"]["integrator"]["status"] == "pending"


def test_active_failed_node_precedes_completed_state(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1)
    _complete_core(book_dir)
    activate_optional_repair(book_dir, 1, ["action"])

    failed = mark_node_failed(book_dir, 1, "action")

    assert failed["run_status"] == "failed"


def test_optional_repair_valid_patch_requires_integrator_and_new_state_delta(
    tmp_path: Path,
) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1, writer_mode="curator_primary")
    _complete_core(book_dir)
    activate_optional_repair(book_dir, 1, ["action"])

    save_node_prompt(book_dir, 1, "action", "action prompt")
    response = "# Action Specialist\n\n## Patch 1\n补充动作因果。"
    after_specialist = save_node_response(book_dir, 1, "action", response)
    assert after_specialist["nodes"]["integrator"]["status"] == "pending"
    assert after_specialist["run_status"] == "in_progress"
    assert skip_integrator_if_no_patches(book_dir, 1, {"action": response})[
        "nodes"
    ]["integrator"]["status"] == "pending"

    save_node_prompt(book_dir, 1, "integrator", "integrator prompt")
    save_node_response(book_dir, 1, "integrator", "integrator response")
    adopted = adopt_final_source(book_dir, 1, "integrator")
    assert adopted["final_source"] == "integrator"
    assert adopted["nodes"]["state_delta"]["status"] == "stale"
    assert adopted["run_status"] == "in_progress"

    save_node_prompt(book_dir, 1, "state_delta", "state delta rerun prompt")
    completed = save_node_response(book_dir, 1, "state_delta", "state delta rerun")
    assert completed["run_status"] == "completed"


def test_legacy_modes_remain_creatable(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)

    single = create_or_load_run(book_dir, 1, writer_mode="single")
    selective = create_or_load_run(
        book_dir, 2, writer_mode="hybrid_selective", selected_specialists=["opening"]
    )
    full = create_or_load_run(book_dir, 3, writer_mode="hybrid_full")

    assert single["writer_mode"] == "single"
    assert selective["selected_specialists"] == ["opening"]
    assert selective["nodes"]["opening"]["status"] == "pending"
    assert selective["nodes"]["dialogue"]["status"] == "skipped"
    assert full["writer_mode"] == "hybrid_full"
    assert set(full["selected_specialists"]) == {"opening", "dialogue", "action", "emotion"}


def test_run_and_prompt_api_defaults_and_explicit_legacy_mode(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "api-demo"}).status_code == 201

    default_run = client.post("/api/books/api-demo/runs/1", json={})
    assert default_run.status_code == 200
    assert default_run.json()["writer_mode"] == "curator_primary"

    legacy_run = client.post(
        "/api/books/api-demo/runs/2",
        json={"writer_mode": "hybrid_selective", "selected_specialists": ["action"]},
    )
    assert legacy_run.status_code == 200
    assert legacy_run.json()["writer_mode"] == "hybrid_selective"

    outline = "\n".join(
        f"{field}：内容"
        for field in (
            "触发事件",
            "推动事件的人",
            "主角行动",
            "对手或世界反应",
            "直接结果",
            "状态变化",
            "叙事功能",
            "结尾推动力",
        )
    )
    prompt = client.post(
        "/api/prompt",
        json={
            "mode": "context_curator",
            "writer_mode": "curator_primary",
            "current_outline": outline,
        },
    )
    assert prompt.status_code == 200
    assert "writer_mode: curator_primary" in prompt.json()["prompt"]


def test_repair_endpoint_is_explicit_and_enforces_order(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "repair-api"}).status_code == 201
    created = client.post("/api/books/repair-api/runs/1", json={})
    assert created.status_code == 200

    before = client.get("/api/books/repair-api/runs/1").json()
    early = client.put(
        "/api/books/repair-api/runs/1/repair-specialists",
        json={"selected_specialists": ["action"]},
    )
    assert early.status_code == 400
    assert client.get("/api/books/repair-api/runs/1").json() == before

    invalid = client.put(
        "/api/books/repair-api/runs/1/repair-specialists",
        json={"selected_specialists": ["not-a-specialist"]},
    )
    assert invalid.status_code == 400


def test_repair_endpoint_allows_explicit_activation_after_primary(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "repair-api"}).status_code == 201
    assert client.post("/api/books/repair-api/runs/1", json={}).status_code == 200
    _complete_core(tmp_path / "repair-api")

    activated = client.put(
        "/api/books/repair-api/runs/1/repair-specialists",
        json={"selected_specialists": ["dialogue", "action"]},
    )

    assert activated.status_code == 200
    assert activated.json()["run_status"] == "in_progress"
    assert activated.json()["nodes"]["dialogue"]["status"] == "pending"
    assert activated.json()["nodes"]["action"]["status"] == "pending"
