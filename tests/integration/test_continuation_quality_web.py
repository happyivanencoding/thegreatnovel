from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.db.database import Database
from novel_authoring.web.app import create_app


def test_shared_draft_approval_route_keeps_csrf_and_workflow_boundaries(tmp_path: Path) -> None:
    database = Database(tmp_path / "boot.sqlite3")
    database.initialize()
    app = create_app(database, book_id="demo")
    client = TestClient(app)

    before = int(database.scalar("SELECT COUNT(*) FROM events") or 0)
    missing_csrf = client.post(
        "/api/books/demo/editions/base/drafts/missing/approve",
        json={"confirmation": "批准写入正史"},
    )
    assert missing_csrf.status_code == 403
    assert missing_csrf.json()["error"]["code"] == "CSRF_INVALID"

    missing_draft = client.post(
        "/api/books/demo/editions/base/drafts/missing/approve",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={"confirmation": "批准写入正史"},
    )
    assert missing_draft.status_code == 400
    assert missing_draft.json()["error"]["code"] == "WORKFLOW_ERROR"
    assert int(database.scalar("SELECT COUNT(*) FROM events") or 0) == before


def test_chapter_approval_pages_use_one_non_blocking_shared_component() -> None:
    root = Path(__file__).parents[2] / "src" / "novel_authoring" / "web"
    static_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (root / "static").glob("*.js")
    )
    template_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (root / "templates").glob("*.html")
    )
    assert "window.confirm" not in static_text
    assert "approval.js" in template_text
    assert "data-approval-action" in template_text
    draft_review = (root / "templates" / "draft_review.html").read_text(encoding="utf-8")
    original_studio = (root / "templates" / "original_studio.html").read_text(encoding="utf-8")
    original_script = (root / "static" / "original.js").read_text(encoding="utf-8")
    assert "<dialog" not in draft_review
    assert "<dialog" not in original_studio
    assert 'data-original-action="approve"' in original_studio
    assert "CodexApproval.submit" in original_script
