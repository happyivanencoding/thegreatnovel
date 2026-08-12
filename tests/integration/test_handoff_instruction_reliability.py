from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from novel_authoring.db.database import Database
from novel_authoring.initialization import create_initialization
from novel_authoring.storage.layout import BookLayout
from novel_authoring.web import app as web_app_module
from novel_authoring.web.app import STATIC_ASSET_VERSION, create_app
from novel_authoring.web.routes.pages import _activity_view
from novel_authoring.workflows.handoffs import (
    HandoffWorkflowError,
    copy_instruction,
    resolve_instruction_path,
)

MISSING_INSTRUCTION_MESSAGE = "交接任务存在，但交接指令文件缺失。请重新准备初始化任务。"


def _write_novel(path: Path, title: str = "指令小说") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"第1章 {title}\n\n潮声掩住了远处的警报。\n", encoding="utf-8")


def _client(tmp_path: Path) -> tuple[TestClient, Path, Path]:
    library = tmp_path / "library"
    discovery = tmp_path / "book"
    discovery.mkdir()
    app = create_app(
        Database(tmp_path / "boot.sqlite3"),
        library_root=library,
        discovery_root=discovery,
    )
    return TestClient(app), library, discovery


def _create_initialized_book(
    client: TestClient, discovery: Path, title: str = "指令小说"
) -> dict[str, Any]:
    _write_novel(discovery / f"{title}.md", title)
    catalog = client.get("/api/library/catalog").json()
    candidate = next(item for item in catalog["entries"] if item["candidate_id"])
    response = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={},
    )
    assert response.status_code == 200
    return response.json()


def _database_for(library: Path, book_id: str) -> Database:
    return Database(BookLayout(library).for_book(book_id).database)


def _handoff_row(database: Database, handoff_id: str) -> dict[str, Any]:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM workflow_handoffs WHERE handoff_id=?", (handoff_id,)
        ).fetchone()
    assert row is not None
    return dict(row)


def _set_prompt_path(database: Database, handoff_id: str, prompt_path: str | None) -> None:
    with database.connect() as connection:
        connection.execute(
            "UPDATE workflow_handoffs SET prompt_path=? WHERE handoff_id=?",
            (prompt_path, handoff_id),
        )


def _instruction_url(created: dict[str, Any]) -> str:
    return created["instruction_url"]


def _flatten_to_legacy_layout(task_directory: Path) -> Path:
    """Convert a canonical operation layout into the legacy flat layout."""

    flat_prompt = task_directory / "prompt.md"
    (task_directory / "input" / "prompt.md").rename(flat_prompt)
    shutil.rmtree(task_directory / "input")
    shutil.rmtree(task_directory / "output")
    return flat_prompt


# 验收清单 1：fresh canonical operation prompt。
def test_fresh_canonical_operation_prompt_served(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    task_directory = Path(str(row["task_directory"]))
    canonical_prompt = task_directory / "input" / "prompt.md"
    assert canonical_prompt.is_file()
    assert Path(str(row["prompt_path"])) == canonical_prompt

    response = client.get(_instruction_url(created))

    assert response.status_code == 200
    payload = response.json()
    assert payload["handoff_id"] == created["handoff_id"]
    assert payload["instruction"] == canonical_prompt.read_text(encoding="utf-8")
    assert "$initialize-existing-novel" in payload["instruction"]


# 验收清单 2：legacy root prompt（flat 布局 task_directory/prompt.md）。
def test_legacy_flat_prompt_layout_fallback(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    task_directory = Path(str(row["task_directory"]))
    flat_prompt = _flatten_to_legacy_layout(task_directory)

    response = client.get(_instruction_url(created))

    assert response.status_code == 200
    assert response.json()["instruction"] == flat_prompt.read_text(encoding="utf-8")


# 验收清单 3：stale absolute prompt_path，回退成功且 DB prompt_path 被回写修复。
def test_stale_absolute_prompt_path_is_repaired_in_database(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    task_directory = Path(str(row["task_directory"]))
    canonical_prompt = task_directory / "input" / "prompt.md"
    stale_path = tmp_path / "moved-away" / "prompt.md"
    _set_prompt_path(database, created["handoff_id"], str(stale_path))

    response = client.get(_instruction_url(created))

    assert response.status_code == 200
    assert response.json()["instruction"] == canonical_prompt.read_text(encoding="utf-8")
    repaired = _handoff_row(database, created["handoff_id"])
    assert Path(str(repaired["prompt_path"])) == canonical_prompt


# 验收清单 4：prompt_path 失效（legacy 空值）但 input/prompt.md 存在时回退到 canonical input。
def test_fallback_to_input_prompt_when_prompt_path_missing(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    task_directory = Path(str(row["task_directory"]))
    canonical_prompt = task_directory / "input" / "prompt.md"
    # prompt_path 为 NOT NULL 列；legacy 行的空字符串表示从未登记过指令路径。
    _set_prompt_path(database, created["handoff_id"], "")

    response = client.get(_instruction_url(created))

    assert response.status_code == 200
    assert response.json()["instruction"] == canonical_prompt.read_text(encoding="utf-8")
    repaired = _handoff_row(database, created["handoff_id"])
    assert Path(str(repaired["prompt_path"])) == canonical_prompt


# 验收清单 5：全部缺失 → HANDOFF_INSTRUCTION_MISSING + 固定 message。
def test_missing_prompt_returns_handoff_instruction_missing(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    task_directory = Path(str(row["task_directory"]))
    (task_directory / "input" / "prompt.md").unlink()
    _set_prompt_path(database, created["handoff_id"], str(tmp_path / "gone" / "prompt.md"))

    response = client.get(_instruction_url(created))

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HANDOFF_INSTRUCTION_MISSING"
    assert error["message"] == MISSING_INSTRUCTION_MESSAGE
    assert error["details"] == {}
    with pytest.raises(HandoffWorkflowError) as excinfo:
        copy_instruction(database, created["handoff_id"])
    assert excinfo.value.error_code == "HANDOFF_INSTRUCTION_MISSING"
    assert excinfo.value.status_code == 404
    assert str(excinfo.value) == MISSING_INSTRUCTION_MESSAGE

    catalog = client.get("/api/library/catalog").json()
    entry = next(item for item in catalog["entries"] if item["book_id"] == created["book_id"])
    assert entry["instruction_available"] is False
    assert entry["instruction_error"] == MISSING_INSTRUCTION_MESSAGE
    assert entry["technical"]["instruction_available"] is False


# 验收清单 6：scope mismatch。
def test_instruction_scope_mismatch_returns_dedicated_error(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)

    response = client.get(
        f"/api/books/{created['book_id']}/editions/other-edition/"
        f"handoffs/{created['handoff_id']}/instruction"
    )

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HANDOFF_SCOPE_MISMATCH"
    assert error["details"] == {}
    assert "book/edition" in error["message"]


# 验收清单 7：missing book database。
def test_instruction_missing_book_database_returns_book_runtime_not_found(
    tmp_path: Path,
) -> None:
    client, _library, _discovery = _client(tmp_path)

    response = client.get(
        "/api/books/no-such-book/editions/base/handoffs/any-handoff/instruction"
    )

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "BOOK_RUNTIME_NOT_FOUND"
    assert error["message"] == "书籍运行库不存在"


# 验收清单 8：前端展示后台真实错误——后端 error.message 透传且 JS 契约保持。
def test_frontend_contract_surfaces_real_backend_error(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    (Path(str(row["task_directory"])) / "input" / "prompt.md").unlink()

    response = client.get(_instruction_url(created))

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["message"] == MISSING_INSTRUCTION_MESSAGE
    assert error["message"] != "WORKFLOW_ERROR"
    assert error["code"] != "WORKFLOW_ERROR"
    # 无 JS 运行时，沿用现有做法：断言前端脚本解析 body.error.message 并附 HTTP 状态码。
    script = client.get("/static/library_catalog.js").text
    assert "instructionErrorMessage" in script
    assert "body.error.message" in script
    assert "（HTTP " in script
    assert "data-copy-handoff" in script


# 验收清单 9：Onboarding browser copy 的两种形态。
def test_onboarding_page_copy_button_and_unavailable_states(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)

    available_page = client.get(created["workbench_url"])
    assert available_page.status_code == 200
    assert "复制给 Codex 的指令" in available_page.text
    assert (
        f'data-instruction-url="/api/books/{created["book_id"]}/editions/base/'
        f'handoffs/{created["handoff_id"]}/instruction"'
    ) in available_page.text

    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])
    (Path(str(row["task_directory"])) / "input" / "prompt.md").unlink()

    unavailable_page = client.get(created["workbench_url"])
    assert unavailable_page.status_code == 200
    assert "交接指令不可用" in unavailable_page.text
    assert "重新准备初始化" in unavailable_page.text
    assert "技术详情" in unavailable_page.text
    assert MISSING_INSTRUCTION_MESSAGE in unavailable_page.text
    assert "复制给 Codex 的指令" not in unavailable_page.text
    assert "data-copy-handoff" not in unavailable_page.text


# 验收清单 10：Activity Center 视图的 instruction_available/instruction_error。
def test_activity_view_instruction_availability_matches_files(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    row = _handoff_row(database, created["handoff_id"])

    available_view = _activity_view(
        row,
        book_id=created["book_id"],
        edition_id="base",
        chapters_by_id={},
        current_chapter=None,
    )
    assert available_view["instruction_available"] is True
    assert available_view["instruction_error"] is None
    assert available_view["technical"]["instruction_available"] is True
    assert available_view["technical"]["instruction_error"] is None

    (Path(str(row["task_directory"])) / "input" / "prompt.md").unlink()

    missing_view = _activity_view(
        row,
        book_id=created["book_id"],
        edition_id="base",
        chapters_by_id={},
        current_chapter=None,
    )
    assert missing_view["instruction_available"] is False
    assert missing_view["instruction_error"] == MISSING_INSTRUCTION_MESSAGE
    assert missing_view["technical"]["instruction_available"] is False
    assert missing_view["technical"]["instruction_error"] == MISSING_INSTRUCTION_MESSAGE


# 补充：字符串 readiness（"BLOCKED"）下 catalog 构建不崩溃且页面 200。
def test_string_readiness_status_does_not_crash_catalog_or_pages(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)
    database = _database_for(library, created["book_id"])
    prepared = create_initialization(database, created["book_id"], edition_id="base")
    root = Path(str(prepared["root"]))
    (root / "status.json").write_text(
        json.dumps(
            {
                "initialization_id": prepared["initialization_id"],
                "state": "BLOCKED",
                "readiness": "BLOCKED",
                "updated_at": "2026-08-11T12:00:00+00:00",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    catalog_response = client.get("/api/library/catalog")
    assert catalog_response.status_code == 200
    entry = next(
        item for item in catalog_response.json()["entries"] if item["book_id"] == created["book_id"]
    )
    assert entry["studio_ready"] is False
    assert entry["instruction_available"] is True
    assert entry["initialization_status"] == "BLOCKED"

    readiness = client.get(f"/api/books/{created['book_id']}/studio-readiness")
    assert readiness.status_code == 200
    assert readiness.json()["ready"] is False
    assert "初始化验收尚未达到完整就绪" in readiness.json()["missing_requirements"]

    page = client.get(created["workbench_url"])
    assert page.status_code == 200


# 补充：handoff 不存在 → HANDOFF_NOT_FOUND。
def test_unknown_handoff_returns_handoff_not_found(tmp_path: Path) -> None:
    client, _library, discovery = _client(tmp_path)
    created = _create_initialized_book(client, discovery)

    response = client.get(
        f"/api/books/{created['book_id']}/editions/base/handoffs/missing-handoff/instruction"
    )

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HANDOFF_NOT_FOUND"
    assert error["message"] == "handoff 不存在"


# 补充：resolve_instruction_path 的回退优先级。
def test_resolve_instruction_path_priority_order(tmp_path: Path) -> None:
    task_directory = tmp_path / "operation"
    (task_directory / "input").mkdir(parents=True)
    (task_directory / "output").mkdir()
    canonical = task_directory / "input" / "prompt.md"
    canonical.write_text("canonical", encoding="utf-8")
    flat = task_directory / "prompt.md"
    flat.write_text("flat", encoding="utf-8")
    explicit = tmp_path / "elsewhere" / "prompt.md"
    explicit.parent.mkdir()
    explicit.write_text("explicit", encoding="utf-8")

    assert resolve_instruction_path(task_directory, str(explicit)) == explicit
    assert resolve_instruction_path(task_directory, None) == canonical
    assert resolve_instruction_path(task_directory, str(tmp_path / "gone.md")) == canonical
    canonical.unlink()
    assert resolve_instruction_path(task_directory, None) == flat
    flat.unlink()
    assert resolve_instruction_path(task_directory, None) is None


# W1：相对 prompt_path 必须锚定到 task_directory，而不是进程 CWD。
def test_resolve_instruction_path_anchors_relative_prompt_to_task_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    task_directory = tmp_path / "operation"
    task_directory.mkdir()
    anchored = task_directory / "prompt.md"
    anchored.write_text("anchored", encoding="utf-8")
    cwd_decoy = tmp_path / "cwd" / "prompt.md"
    cwd_decoy.parent.mkdir()
    cwd_decoy.write_text("cwd-decoy", encoding="utf-8")
    monkeypatch.chdir(cwd_decoy.parent)

    assert resolve_instruction_path(task_directory, "prompt.md") == anchored


# W1：task_directory 为空时只信任绝对 prompt_path，跳过所有目录型回退。
def test_resolve_instruction_path_empty_task_directory_trusts_absolute_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    absolute = tmp_path / "somewhere" / "prompt.md"
    absolute.parent.mkdir()
    absolute.write_text("absolute", encoding="utf-8")
    cwd_decoy = tmp_path / "cwd" / "input" / "prompt.md"
    cwd_decoy.parent.mkdir(parents=True)
    cwd_decoy.write_text("cwd-decoy", encoding="utf-8")
    monkeypatch.chdir(tmp_path / "cwd")

    assert resolve_instruction_path(Path(""), str(absolute)) == absolute
    assert resolve_instruction_path(Path(""), "input/prompt.md") is None
    assert resolve_instruction_path(Path(""), None) is None


# W2：commit 探测进程内只 spawn 一次 git，结果缓存。
def test_current_commit_probed_only_once(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(web_app_module, "_commit_cache", web_app_module._COMMIT_NOT_PROBED)
    calls = {"count": 0}

    def fake_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls["count"] += 1
        return subprocess.CompletedProcess(args, 0, stdout="abc1234\n", stderr="")

    monkeypatch.setattr(web_app_module.subprocess, "run", fake_run)

    assert web_app_module._current_commit() == "abc1234"
    assert web_app_module._current_commit() == "abc1234"
    assert calls["count"] == 1


# S3：旧单库路由与 book-scoped 路由的 handoff 不存在错误码对齐。
def test_legacy_instruction_route_returns_handoff_not_found(tmp_path: Path) -> None:
    client, _library, _discovery = _client(tmp_path)

    response = client.get("/api/handoffs/missing-handoff/instruction")

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HANDOFF_NOT_FOUND"
    assert error["message"] == "handoff 不存在"
    assert error["details"] == {}


# 补充：/health 暴露版本信息，静态资源版本与模板注入常量一致。
def test_health_reports_versions(tmp_path: Path) -> None:
    client, _library, _discovery = _client(tmp_path)

    health = client.get("/health").json()

    assert health["status"] == "ok"
    assert health["static_asset_version"] == STATIC_ASSET_VERSION
    assert health["static_asset_version"] == "3.5.0"
    assert "version" in health
    assert "commit" in health
