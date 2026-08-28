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
    for node in ("director", "curator", "primary", "authority_reviser"):
        save_node_prompt(book_dir, chapter, node, f"{node} prompt")
        save_node_response(book_dir, chapter, node, f"{node} response")
    adopt_final_source(book_dir, chapter, "authority_reviser")
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
    assert manifest["nodes"]["authority_reviser"]["status"] == "pending"
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

    assert next_actionable_node(book_dir, 1) == "authority_reviser"
    save_node_prompt(book_dir, 1, "authority_reviser", "authority prompt")
    save_node_response(book_dir, 1, "authority_reviser", "authority response")
    adopt_final_source(book_dir, 1, "authority_reviser")
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


def test_optional_repair_requires_authority_reviser_and_does_not_mutate_early(
    tmp_path: Path,
) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1, writer_mode="curator_primary")
    before = load_run(book_dir, 1)

    try:
        activate_optional_repair(book_dir, 1, ["action"])
    except ValueError as error:
        assert "Authority Reviser" in str(error)
    else:
        raise AssertionError("repair must require a completed Authority Reviser")
    assert load_run(book_dir, 1) == before


def test_optional_repair_no_patch_keeps_authority_revision_and_recompletes_run(tmp_path: Path) -> None:
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
    assert settled["final_source"] == "authority_reviser"
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


def test_curator_primary_cannot_adopt_primary_before_authority_revision(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    create_or_load_run(book_dir, 1)
    for node in ("director", "curator", "primary"):
        save_node_prompt(book_dir, 1, node, f"{node} prompt")
        save_node_response(book_dir, 1, node, f"{node} response")

    try:
        adopt_final_source(book_dir, 1, "primary")
    except ValueError as error:
        assert "Authority Reviser" in str(error)
    else:
        raise AssertionError("curator_primary must not bypass Authority Reviser")


def test_legacy_modes_remain_creatable(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)

    single = create_or_load_run(book_dir, 1, writer_mode="single")
    selective = create_or_load_run(
        book_dir, 2, writer_mode="hybrid_selective", selected_specialists=["opening"]
    )
    full = create_or_load_run(book_dir, 3, writer_mode="hybrid_full")

    assert single["writer_mode"] == "single"
    assert single["nodes"]["authority_reviser"]["status"] == "skipped"
    assert selective["selected_specialists"] == ["opening"]
    assert selective["nodes"]["authority_reviser"]["status"] == "skipped"
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


def test_repair_endpoint_allows_explicit_activation_after_authority_reviser(
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


def _valid_outline() -> str:
    return "\n".join(
        f"{field}：内容"
        for field in (
            "触发事件", "推动事件的人", "主角行动", "对手或世界反应",
            "直接结果", "状态变化", "叙事功能", "结尾推动力",
        )
    )


def test_prompt_api_can_hydrate_authority_reviser_from_saved_primary_run(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "hydrate-reviser"}).status_code == 201
    book_dir = tmp_path / "hydrate-reviser"
    create_or_load_run(book_dir, 1)
    save_node_prompt(book_dir, 1, "director", "director prompt")
    save_node_response(book_dir, 1, "director", "director response")
    save_node_prompt(book_dir, 1, "curator", "curator prompt")
    save_node_response(book_dir, 1, "curator", "CURATOR_FROM_LEDGER")
    save_node_prompt(book_dir, 1, "primary", "primary prompt")
    save_node_response(book_dir, 1, "primary", "# 正式正文\n\nPRIMARY_FROM_LEDGER")

    response = client.post(
        "/api/prompt",
        json={
            "mode": "authority_reviser",
            "book_id": "hydrate-reviser",
            "chapter_number": 1,
            "current_outline": _valid_outline(),
        },
    )
    assert response.status_code == 200
    prompt = response.json()["prompt"]
    assert "PRIMARY_FROM_LEDGER" in prompt
    assert "CURATOR_FROM_LEDGER" in prompt


def test_state_delta_uses_authority_reviser_final_source_not_page_primary(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "state-source"}).status_code == 201
    book_dir = tmp_path / "state-source"
    create_or_load_run(book_dir, 1)
    for node, response in (
        ("director", "director response"),
        ("curator", "curator response"),
        ("primary", "# 正式正文\n\nPRIMARY_MUST_NOT_ENTER_STATE"),
        ("authority_reviser", "# 正式正文\n\nREVISED_BODY_IS_STATE_SOURCE"),
    ):
        save_node_prompt(book_dir, 1, node, f"{node} prompt")
        save_node_response(book_dir, 1, node, response)
    adopt_final_source(book_dir, 1, "authority_reviser")

    response = client.post(
        "/api/prompt/state-delta",
        json={
            "mode": "state_delta",
            "book_id": "state-source",
            "chapter_number": 1,
            "chapter_prose": "PAGE_PRIMARY_BYPASS_ATTEMPT",
        },
    )
    assert response.status_code == 200
    prompt = response.json()["prompt"]
    assert "REVISED_BODY_IS_STATE_SOURCE" in prompt
    assert "PAGE_PRIMARY_BYPASS_ATTEMPT" not in prompt
    assert "PRIMARY_MUST_NOT_ENTER_STATE" not in prompt


def test_state_delta_rejects_curator_primary_before_authority_revision_final_source(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "state-too-early"}).status_code == 201
    book_dir = tmp_path / "state-too-early"
    create_or_load_run(book_dir, 1)
    for node in ("director", "curator", "primary"):
        save_node_prompt(book_dir, 1, node, f"{node} prompt")
        save_node_response(book_dir, 1, node, f"{node} response")

    response = client.post(
        "/api/prompt/state-delta",
        json={
            "mode": "state_delta",
            "book_id": "state-too-early",
            "chapter_number": 1,
            "chapter_prose": "PRIMARY_BYPASS",
        },
    )
    assert response.status_code == 400
    assert "Authority Reviser" in response.json()["detail"]


def test_optional_specialist_prompt_hydrates_authority_revision_as_draft(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "repair-source"}).status_code == 201
    book_dir = tmp_path / "repair-source"
    create_or_load_run(book_dir, 1)
    for node, response in (
        ("director", "director response"),
        ("curator", "CURATOR_REPAIR_CONTEXT"),
        ("primary", "# 正式正文\n\nPRIMARY_OLD_DRAFT"),
        ("authority_reviser", "# 正式正文\n\nAUTHORITY_REVISED_DRAFT"),
    ):
        save_node_prompt(book_dir, 1, node, f"{node} prompt")
        save_node_response(book_dir, 1, node, response)
    adopt_final_source(book_dir, 1, "authority_reviser")
    activate_optional_repair(book_dir, 1, ["action"])

    response = client.post(
        "/api/prompt",
        json={
            "mode": "specialist_action",
            "book_id": "repair-source",
            "chapter_number": 1,
            "current_outline": _valid_outline(),
        },
    )
    assert response.status_code == 200
    prompt = response.json()["prompt"]
    assert "AUTHORITY_REVISED_DRAFT" in prompt
    assert "PRIMARY_OLD_DRAFT" not in prompt
