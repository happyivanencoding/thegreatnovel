from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.db.database import Database
from novel_authoring.initialization import create_initialization, latest_initialization
from novel_authoring.library_catalog import BookDiscoveryService
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookRegistry
from novel_authoring.web.app import create_app


def _write_novel(path: Path, title: str = "新测试小说") -> None:
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


def _mark_initialization_ready(database: Database, book_id: str) -> Path:
    prepared = create_initialization(database, book_id, edition_id="base")
    root = Path(str(prepared["root"]))
    manifest_path = root / "initialization_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "READY"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    (root / "entity_resolution" / "entity_resolution_map.json").write_text("{}", encoding="utf-8")
    (root / "synthesis" / "current_world_model.md").write_text("# 当前世界模型\n", encoding="utf-8")
    (root / "synthesis" / "graphs.json").write_text("{}", encoding="utf-8")
    (root / "metrics" / "metric_bootstrap_manifest.json").write_text("{}", encoding="utf-8")
    (root / "reports" / "readiness_report.md").write_text("# READY\n", encoding="utf-8")
    arc_manifest = json.loads((root / "arc_manifest.json").read_text(encoding="utf-8"))
    for arc in arc_manifest["arcs"]:
        output = (
            BookLayout(database.path.parents[2])
            .for_book(book_id)
            .edition("base")
            .operation(f"{prepared['initialization_id']}-arc-{arc['arc_id']}")
            .output
            / "output.json"
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("{}", encoding="utf-8")
    readiness = {
        "status": "READY",
        "source_mapping_coverage": 1.0,
        "arc_output_coverage": 1.0,
        "chapter_semantic_feature_coverage": 1.0,
        "metric_bootstrap_status": "COMPLETE",
        "core_graphs_complete": True,
        "protagonist_confirmed": True,
        "current_thread_confirmed": True,
        "blocking_reasons": [],
        "gaps": [],
    }
    (root / "status.json").write_text(
        json.dumps(
            {
                "initialization_id": prepared["initialization_id"],
                "state": "READY",
                "readiness": readiness,
                "updated_at": "2026-08-11T12:00:00+00:00",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return root


def test_discovery_is_read_only_and_uses_supported_top_level_sources(tmp_path: Path) -> None:
    discovery = tmp_path / "book"
    _write_novel(discovery / "小说A.md", "同名小说")
    _write_novel(discovery / "A" / "小说.md", "同名小说")
    _write_novel(discovery / "B" / "小说.md", "同名小说")
    _write_novel(discovery / ".hidden" / "secret.md")
    _write_novel(discovery / "benchmark" / "fixture.md")
    (discovery / "README.md").write_text("说明", encoding="utf-8")
    (discovery / "notes.pdf").write_text("unsupported", encoding="utf-8")
    before = {
        path.relative_to(discovery).as_posix(): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in discovery.rglob("*")
        if path.is_file()
    }

    candidates = BookDiscoveryService(discovery).scan()

    after = {
        path.relative_to(discovery).as_posix(): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in discovery.rglob("*")
        if path.is_file()
    }
    assert before == after
    assert {item.display_title for item in candidates} == {"小说A", "A", "B"}
    assert len({item.candidate_id for item in candidates}) == 3
    assert [item.display_title for item in candidates].count("A") == 1


def test_local_upload_never_overwrites_same_named_source(tmp_path: Path) -> None:
    client, _library, discovery = _client(tmp_path)
    headers = {"X-CSRF-Token": client.app.state.csrf_token}
    first = client.post(
        "/api/library/upload",
        headers=headers,
        data={"conflict_policy": "KEEP_BOTH", "renamed_filename": ""},
        files={"files": ("小说.md", "第一份正文", "text/markdown")},
    )
    cancelled = client.post(
        "/api/library/upload",
        headers=headers,
        data={"conflict_policy": "CANCEL", "renamed_filename": ""},
        files={"files": ("小说.md", "第二份正文", "text/markdown")},
    )
    kept = client.post(
        "/api/library/upload",
        headers=headers,
        data={"conflict_policy": "KEEP_BOTH", "renamed_filename": ""},
        files={"files": ("小说.md", "第二份正文", "text/markdown")},
    )

    assert first.status_code == 200
    assert cancelled.status_code == 409
    assert kept.status_code == 200
    assert (discovery / "小说.md").read_text(encoding="utf-8") == "第一份正文"
    assert (discovery / "小说 (2).md").read_text(encoding="utf-8") == "第二份正文"


def test_candidate_ingest_creates_existing_initialization_handoff_and_deduplicates(
    tmp_path: Path,
) -> None:
    client, library, discovery = _client(tmp_path)
    source = discovery / "新测试小说.md"
    _write_novel(source)
    source_before = source.read_bytes()

    initial = client.get("/api/library/catalog").json()
    candidate = next(item for item in initial["entries"] if item["candidate_id"])
    assert not library.exists()
    assert initial["counts"] == {
        "needs_action": 0,
        "preparing": 0,
        "creative": 0,
        "awaiting_import": 1,
    }
    assert client.get(candidate["href"]).status_code == 200
    assert (
        client.post(f"/api/library/candidates/{candidate['candidate_id']}/initialize").status_code
        == 403
    )

    response = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={"depth": "QUICK"},
    )
    assert response.status_code == 200
    result = response.json()
    assert source.read_bytes() == source_before
    record = BookRegistry(BookLayout(library)).record(result["book_id"])
    assert record.source_origin == source.resolve()
    database = Database(BookLayout(library).for_book(result["book_id"]).database)
    initialization = client.get(
        f"/api/books/{result['book_id']}/editions/base/initialization"
    ).json()
    assert initialization["manifest"]["initialization_depth"] == "QUICK"
    with database.connect() as connection:
        handoff = connection.execute(
            "SELECT handoff_type, status FROM workflow_handoffs WHERE handoff_id=?",
            (result["handoff_id"],),
        ).fetchone()
    assert handoff is not None
    assert handoff["handoff_type"] == "NOVEL_INITIALIZATION"
    assert handoff["status"] == "READY_FOR_CODEX"
    instruction = client.get(result["instruction_url"])
    assert instruction.status_code == 200
    assert "$initialize-existing-novel" in instruction.json()["instruction"]

    updated = client.get("/api/library/catalog").json()
    assert [item["book_id"] for item in updated["entries"]] == [result["book_id"]]
    assert all(item["candidate_id"] is None for item in updated["entries"])
    onboarding = client.get(result["workbench_url"])
    assert onboarding.status_code == 200
    assert "data-wb-chapter-tree" in onboarding.text
    access = client.get(f"/api/books/{result['book_id']}/studio-access").json()
    assert access["access_level"] == "LIMITED"
    assert access["capabilities"]["browse_structure"] is True
    assert access["capabilities"]["plan_next"] is True
    assert access["capabilities"]["continue_from_current_boundary"] is False
    assert access["author_label"] != "可以续写 · 历史仍在补齐"
    catalog_entry = next(
        item
        for item in client.get("/api/library/catalog").json()["entries"]
        if item["book_id"] == result["book_id"]
    )
    assert catalog_entry["state"] != "CONTINUE_READY"
    limited_api = client.get(f"/api/books/{result['book_id']}/editions/base/workbench")
    assert limited_api.status_code == 200


def test_completed_handoff_without_core_artifacts_remains_blocked(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    _write_novel(discovery / "不完整.md")
    candidate = client.get("/api/library/catalog").json()["entries"][0]
    created = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={},
    ).json()
    database = Database(BookLayout(library).for_book(created["book_id"]).database)
    with database.connect() as connection:
        connection.execute(
            "UPDATE workflow_handoffs SET status='COMPLETED' WHERE handoff_id=?",
            (created["handoff_id"],),
        )

    readiness = client.get(f"/api/books/{created['book_id']}/studio-readiness").json()
    assert readiness["ready"] is False
    assert readiness["status"] == "NEEDS_REPAIR"
    assert "核心关系图谱缺失" in readiness["missing_requirements"]


def test_valid_ready_contract_opens_full_studio_and_catalog_selector(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    _write_novel(discovery / "可创作.md")
    candidate = client.get("/api/library/catalog").json()["entries"][0]
    created = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={},
    ).json()
    paths = BookLayout(library).for_book(created["book_id"])
    _mark_initialization_ready(Database(paths.database), created["book_id"])

    readiness = client.get(f"/api/books/{created['book_id']}/studio-readiness").json()
    assert readiness["ready"] is True
    assert readiness["status"] == "READY"
    access = client.get(f"/api/books/{created['book_id']}/studio-access").json()
    assert access["access_level"] == "FULL"
    assert access["author_label"] == "完整就绪"
    assert access["authoring_capabilities"]["FULL_READY"] is True
    catalog = client.get("/api/library/catalog").json()
    entry = next(item for item in catalog["entries"] if item["book_id"] == created["book_id"])
    assert entry["state_label"] == "完整就绪"
    assert catalog["groups"]["needs_action"][0]["book_id"] == created["book_id"]
    page = client.get(created["workbench_url"])
    assert page.status_code == 200
    assert "data-wb-chapter-tree" in page.text
    assert "世界状态" in page.text
    assert "剧情规划" in page.text
    assert "全书画像" in page.text
    assert "data-book-selector" in page.text
    assert "切换 session" not in page.text


def test_ready_with_gaps_opens_limited_studio_without_claiming_full_readiness(
    tmp_path: Path,
) -> None:
    client, library, discovery = _client(tmp_path)
    _write_novel(discovery / "有待补齐.md")
    candidate = client.get("/api/library/catalog").json()["entries"][0]
    created = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={},
    ).json()
    paths = BookLayout(library).for_book(created["book_id"])
    root = _mark_initialization_ready(Database(paths.database), created["book_id"])

    manifest_path = root / "initialization_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["state"] = "READY_WITH_GAPS"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    status_path = root / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["state"] = "READY_WITH_GAPS"
    status["readiness"]["status"] = "READY_WITH_GAPS"
    status["readiness"]["gaps"] = ["远期路线仍有待定项"]
    status["readiness"]["continuation_boundary"] = {"ready_for_continuation": True}
    status_path.write_text(json.dumps(status, ensure_ascii=False), encoding="utf-8")

    readiness = client.get(f"/api/books/{created['book_id']}/studio-readiness").json()
    assert readiness["status"] == "READY_WITH_GAPS"
    assert readiness["ready"] is False
    assert readiness["missing_requirements"] == []

    access = client.get(f"/api/books/{created['book_id']}/studio-access").json()
    assert access["access_level"] == "ACTION_READY"
    assert access["accessible"] is True
    assert access["authoring_capabilities"]["CONTINUE_READY"] is True
    assert access["authoring_capabilities"]["FULL_READY"] is False
    assert access["author_label"] == "可以续写 · 历史仍在补齐"
    catalog = client.get("/api/library/catalog").json()
    entry = next(item for item in catalog["entries"] if item["book_id"] == created["book_id"])
    assert entry["state"] == "CONTINUE_READY"
    assert entry["state_label"] == "可以续写 · 历史仍在补齐"
    assert entry in catalog["groups"]["creative"]
    assert entry not in catalog["groups"]["needs_action"]
    assert entry["studio_ready"] is False
    assert entry["studio_accessible"] is True
    assert entry["primary_action"] == "OPEN_STUDIO"
    page = client.get(created["workbench_url"])
    assert page.status_code == 200
    assert "初始化尚未完整" not in page.text
    assert "data-wb-chapter-tree" in page.text


def test_ready_with_gaps_without_structural_index_stays_blocked(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    _write_novel(discovery / "缺结构索引.md")
    candidate = client.get("/api/library/catalog").json()["entries"][0]
    created = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={},
    ).json()
    paths = BookLayout(library).for_book(created["book_id"])
    database = Database(paths.database)
    root = _mark_initialization_ready(database, created["book_id"])
    (root / "structural_index.json").unlink()
    with database.connect() as connection:
        connection.execute(
            "UPDATE workflow_handoffs SET status='COMPLETED' WHERE handoff_id=?",
            (created["handoff_id"],),
        )

    readiness = client.get(f"/api/books/{created['book_id']}/studio-readiness").json()
    assert readiness["status"] == "NEEDS_REPAIR"
    assert "全书结构索引缺失" in readiness["missing_requirements"]
    access = client.get(f"/api/books/{created['book_id']}/studio-access").json()
    assert access["access_level"] == "ONBOARDING"
    assert access["accessible"] is False


def test_continue_ready_is_the_author_status_while_full_analysis_is_blocked(
    tmp_path: Path,
) -> None:
    client, library, discovery = _client(tmp_path)
    _write_novel(discovery / "渐进续写.md")
    candidate = client.get("/api/library/catalog").json()["entries"][0]
    created = client.post(
        f"/api/library/candidates/{candidate['candidate_id']}/initialize",
        headers={"X-CSRF-Token": client.app.state.csrf_token},
        json={"depth": "BALANCED"},
    ).json()
    paths = BookLayout(library).for_book(created["book_id"])
    current = latest_initialization(Database(paths.database), created["book_id"], "base")
    assert current is not None
    root = Path(str(current["root"]))
    status_path = root / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["state"] = "METRIC_BOOTSTRAP_RUNNING"
    status["readiness"] = {
        "status": "BLOCKED",
        "chapter_semantic_feature_coverage": 0.4,
        "blocking_reasons": ["完整 READY 需要 FULL"],
        "gaps": ["非阻塞历史章节仍保持 UNKNOWN / NOT_ANALYZED"],
        "continuation_boundary": {"ready_for_continuation": True},
    }
    status_path.write_text(json.dumps(status, ensure_ascii=False), encoding="utf-8")

    access = client.get(f"/api/books/{created['book_id']}/studio-access").json()
    assert access["authoring_capabilities"]["CONTINUE_READY"] is True
    assert access["authoring_capabilities"]["FULL_READY"] is False
    assert access["author_label"] == "可以续写 · 历史仍在补齐"
    catalog = client.get("/api/library/catalog").json()
    entry = next(item for item in catalog["entries"] if item["book_id"] == created["book_id"])
    assert entry["state"] == "CONTINUE_READY"
    assert entry["state_label"] == "可以续写 · 历史仍在补齐"
    assert entry["author_summary"] == "当前续写边界已经就绪；未覆盖的历史语义仍在渐进补齐。"
    assert entry in catalog["groups"]["creative"]
    assert entry not in catalog["groups"]["needs_action"]
    assert paths.root.is_dir()


def test_library_and_selector_share_catalog_and_poll_without_mutation(tmp_path: Path) -> None:
    client, library, discovery = _client(tmp_path)
    _write_novel(discovery / "候选甲.md")
    catalog = client.get("/api/library/catalog").json()
    library_page = client.get("/library").text
    candidate_page = client.get(catalog["entries"][0]["href"]).text

    assert "候选甲" in library_page
    assert "候选甲" in candidate_page
    assert "先了解这本书" in candidate_page
    assert "尽快续写最新章节" in candidate_page
    assert "做完整全书审查" in candidate_page
    assert catalog["entries"][0]["state_label"] == "待初始化"
    assert "页面局部检查进度" in candidate_page
    assert "data-current-book-state-label" in candidate_page
    assert "data-onboarding-activity-count>0</span>" in candidate_page
    script = client.get("/static/library_catalog.js").text
    assert "setInterval" in script
    assert "10000" in script
    assert "data-current-book-option-state-label" in script
    assert "showReady" in script
    assert "studio_accessible" in script
    assert "location.reload" not in script
    assert "data-onboarding-activity-count" in script
    assert not library.exists()
