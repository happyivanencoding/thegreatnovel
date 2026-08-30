from __future__ import annotations

import json
from pathlib import Path

from story_mvp.run_ledger import (
    adopt_final_source,
    create_or_load_run,
    load_node_response,
    load_run,
    mark_node_failed,
    mark_run_stale,
    next_actionable_node,
    retry_node,
    run_directory,
    save_node_prompt,
    save_node_response,
)


def _book(tmp_path: Path, *, writer_mode: str = "single") -> Path:
    book_dir = tmp_path / "demo"
    book_dir.mkdir(parents=True)
    (book_dir / "BOOK.md").write_text("# book\n", encoding="utf-8")
    create_or_load_run(book_dir, 1, writer_mode=writer_mode)
    return book_dir


def test_exact_prompt_receipt_restores_stale_completed_node_without_new_response(tmp_path: Path) -> None:
    book_dir = _book(tmp_path)
    save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR RESPONSE")
    before = load_run(book_dir, 1)["nodes"]["director"].copy()

    mark_run_stale(book_dir, 1)
    restored = save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    node = restored["nodes"]["director"]

    assert node["status"] == "completed"
    assert node["attempts"] == before["attempts"] == 1
    assert node["response_file"] == before["response_file"]
    assert node["response_sha256"] == before["response_sha256"]
    assert node["response_prompt_sha256"] == node["prompt_sha256"]
    assert node["receipt_reuses"] == 1
    assert node["receipt_reused"] is True
    assert load_node_response(book_dir, 1, "director") == "DIRECTOR RESPONSE"


def test_changed_prompt_keeps_stale_node_actionable(tmp_path: Path) -> None:
    book_dir = _book(tmp_path)
    save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR RESPONSE")

    mark_run_stale(book_dir, 1)
    manifest = save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT CHANGED")

    assert manifest["nodes"]["director"]["status"] == "stale"
    assert manifest["nodes"]["director"]["receipt_reuses"] == 0
    assert next_actionable_node(book_dir, 1) == "director"


def test_tampered_response_file_invalidates_exact_prompt_receipt(tmp_path: Path) -> None:
    book_dir = _book(tmp_path)
    save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR RESPONSE")
    response_path = run_directory(book_dir, 1) / "director_response.md"
    response_path.write_text("MANUALLY CHANGED RESPONSE", encoding="utf-8")

    mark_run_stale(book_dir, 1)
    manifest = save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")

    assert manifest["nodes"]["director"]["status"] == "stale"
    assert manifest["nodes"]["director"]["receipt_reuses"] == 0


def test_explicit_retry_bypasses_receipt_even_when_prompt_is_identical(tmp_path: Path) -> None:
    book_dir = _book(tmp_path)
    save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR RESPONSE")
    mark_node_failed(book_dir, 1, "director")
    retried = retry_node(book_dir, 1, "director")
    assert retried["nodes"]["director"]["status"] == "pending"
    assert retried["nodes"]["director"]["attempts"] == 2
    assert retried["nodes"]["director"]["receipt_reused"] is False

    manifest = save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    assert manifest["nodes"]["director"]["status"] == "pending"
    assert manifest["nodes"]["director"]["receipt_reuses"] == 0


def test_legacy_manifest_without_receipt_fails_closed_to_rerun(tmp_path: Path) -> None:
    book_dir = _book(tmp_path)
    save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR RESPONSE")
    manifest_path = run_directory(book_dir, 1) / "manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    node = payload["nodes"]["director"]
    for key in (
        "prompt_sha256",
        "response_prompt_sha256",
        "response_sha256",
        "response_receipt_status",
        "receipt_reuses",
    ):
        node.pop(key, None)
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    mark_run_stale(book_dir, 1)
    manifest = save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")

    assert manifest["nodes"]["director"]["status"] == "stale"
    assert manifest["nodes"]["director"]["receipt_reuses"] == 0


def test_exact_receipt_restores_adopted_final_source(tmp_path: Path) -> None:
    book_dir = _book(tmp_path, writer_mode="curator_primary")
    save_node_prompt(book_dir, 1, "authority_reviser", "AUTHORITY PROMPT")
    save_node_response(book_dir, 1, "authority_reviser", "AUTHORITY RESPONSE")
    adopt_final_source(book_dir, 1, "authority_reviser")
    assert load_run(book_dir, 1)["nodes"]["authority_reviser"]["status"] == "adopted"

    mark_run_stale(book_dir, 1)
    restored = save_node_prompt(book_dir, 1, "authority_reviser", "AUTHORITY PROMPT")

    assert restored["final_source"] == "authority_reviser"
    assert restored["nodes"]["authority_reviser"]["status"] == "adopted"
    assert restored["nodes"]["authority_reviser"]["receipt_reuses"] == 1


def test_manually_failed_saved_response_cannot_be_restored_by_later_stale(tmp_path: Path) -> None:
    book_dir = _book(tmp_path)
    save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR RESPONSE")
    failed = mark_node_failed(book_dir, 1, "director")
    assert failed["nodes"]["director"]["response_receipt_status"] == "failed"

    mark_run_stale(book_dir, 1)
    manifest = save_node_prompt(book_dir, 1, "director", "DIRECTOR PROMPT")

    assert manifest["nodes"]["director"]["status"] == "stale"
    assert manifest["nodes"]["director"]["receipt_reuses"] == 0
    assert manifest["nodes"]["director"]["receipt_reused"] is False
