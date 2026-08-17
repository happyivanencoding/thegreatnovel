from __future__ import annotations

from novel_authoring.initialization import service as initialization_service


def test_original_continue_does_not_require_source_initialization(
    monkeypatch,
) -> None:
    monkeypatch.setattr(initialization_service, "resolve_edition_id", lambda *args: "base")
    monkeypatch.setattr(initialization_service, "latest_initialization", lambda *args: None)
    monkeypatch.setattr(initialization_service, "is_original_book", lambda *args: True)

    result = initialization_service.prepare_action_deepening(
        object(),
        "original-book",
        edition_id="base",
        action="CONTINUE",
    )

    assert result["status"] == "ACTION_CONTEXT_READY"
    assert result["source_mode"] == "ORIGINAL_NO_SOURCE"
