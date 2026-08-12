from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import novel_authoring.canon.projection as projection_module
import novel_authoring.web.workbench as workbench_module
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.storage.library import LibraryAddOptions, add_book
from novel_authoring.web.app import create_app, web_doctor
from novel_authoring.web.routes.pages import workflow_context


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._hidden_depth = 0
        self._hidden_tags: list[bool] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }:
            return
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        hidden = "hidden" in values or classes.intersection(
            {"wb-technical-details", "workflow-task-details", "workflow-developer-details"}
        )
        self._hidden_tags.append(hidden)
        if hidden:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        hidden = self._hidden_tags.pop() if self._hidden_tags else False
        if hidden:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._hidden_depth:
            self.parts.append(data)


def _visible_text(html: str) -> str:
    parser = _VisibleTextParser()
    parser.feed(html)
    return " ".join(parser.parts)


def _book(tmp_path: Path, book_id: str = "workbench-book") -> Database:
    source = tmp_path / "source"
    source.mkdir()
    (source / "novel.md").write_text(
        "第1章 灯塔\n\n海风把旧门吹开。\n\n"
        "第2章 潮声\n\n潮声里藏着一段坐标。\n\n"
        "第3章 返航\n\n主角把坐标收进怀里。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id=book_id,
        title="Workbench 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / book_id / "state.sqlite3")
    database.initialize()
    profile_root = workspace / book_id / "book_profil"
    profile_root.mkdir()
    (profile_root / "worldbuilding.md").write_text(
        "# 世界观\n\n潮汐会遮蔽灯塔坐标。\n", encoding="utf-8"
    )
    (profile_root / "profile_manifest.json").write_text(
        json.dumps(
            {"scope": "SELF_BOOK", "profile_version": "test-profile-v1"},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return database


def _chapter_ids(database: Database) -> list[str]:
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT chapter_id FROM chapters ORDER BY ordinal"
        ).fetchall()
    return [str(row["chapter_id"]) for row in rows]


def _read_only_snapshot(database: Database) -> dict[str, object]:
    with database.connect() as connection:
        events = connection.execute(
            "SELECT event_id, event_seq, event_type FROM events ORDER BY event_seq"
        ).fetchall()
        commits = connection.execute(
            "SELECT commit_id, draft_id, event_end_seq FROM canon_commits ORDER BY commit_id"
        ).fetchall()
        projection = connection.execute(
            "SELECT book_id, through_event_seq, state_sha256, state_json "
            "FROM projection_metadata ORDER BY book_id"
        ).fetchall()
        editions = connection.execute(
            "SELECT edition_id, status, version FROM editions ORDER BY edition_id"
        ).fetchall()
        books = connection.execute(
            "SELECT book_id, active_edition_id, mode FROM books ORDER BY book_id"
        ).fetchall()
    return {
        "events": [tuple(row) for row in events],
        "commits": [tuple(row) for row in commits],
        "projection": [tuple(row) for row in projection],
        "editions": [tuple(row) for row in editions],
        "books": [tuple(row) for row in books],
    }


def _insert_handoff(
    database: Database,
    root: Path,
    *,
    handoff_id: str,
    handoff_type: str,
    requested_stage: str,
    status: str,
    chapter_id: str,
    created_at: str,
) -> None:
    task_directory = root / handoff_id
    task_directory.mkdir(parents=True)
    task_manifest = task_directory / "task.json"
    task_manifest.write_text(
        json.dumps({"context_chapter_id": chapter_id}, ensure_ascii=False),
        encoding="utf-8",
    )
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO workflow_handoffs(
                handoff_id, book_id, edition_id, handoff_type, requested_stage,
                status, task_directory, prompt_path, task_manifest_path,
                output_schema_path, result_path, event_log_path, base_event_seq,
                base_projection_hash, source_manifest_sha256, registry_hash,
                config_hash, created_at
            ) VALUES (?, 'shell-test-book', 'base', ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      0, 'projection', 'source', 'registry', 'config', ?)
            """,
            (
                handoff_id,
                handoff_type,
                requested_stage,
                status,
                str(task_directory),
                str(task_directory / "prompt.md"),
                str(task_manifest),
                str(task_directory / "schema.json"),
                str(task_directory / "result.json"),
                str(task_directory / "events.jsonl"),
                created_at,
            ),
        )


def test_workbench_renders_real_profile_and_highlights_selected_node(tmp_path: Path) -> None:
    database = _book(tmp_path)
    app = create_app(database, book_id="workbench-book")
    client = TestClient(app)

    response = client.get(
        "/books/workbench-book/editions/base/workbench?node=worldbuilding&mode=analysis"
    )

    assert response.status_code == 200
    assert "小说工作台" in response.text
    assert "潮汐会遮蔽灯塔坐标" in response.text
    assert "全书画像 · 当前有效版本" in _visible_text(response.text)
    assert "SOFT INTERPRETATION" not in _visible_text(response.text)
    assert "SELF_BOOK" not in _visible_text(response.text)
    assert "Distill version" not in _visible_text(response.text)
    assert 'data-workbench-shell' in response.text
    assert 'data-pane-rail="left"' in response.text
    assert 'data-pane-rail="right"' in response.text
    assert "action=continue" in response.text
    assert "action=rewrite" in response.text
    assert "action=plan" in response.text
    assert "续写下一章" in response.text
    assert "改写本章" in response.text
    assert "规划后续" in response.text
    assert "data-activity-trigger" in response.text
    assert "隐藏左栏" in response.text
    assert "隐藏右栏" in response.text
    assert "is-selected" in response.text
    assert "当前 Book 没有" not in response.text


def test_chapter_navigation_is_query_only_and_exposes_source_gap(tmp_path: Path) -> None:
    database = _book(tmp_path, "historical-workbench-book")
    app = create_app(database, book_id="historical-workbench-book")
    client = TestClient(app)
    chapter_ids = _chapter_ids(database)
    before = _read_only_snapshot(database)

    for chapter_id in (chapter_ids[0], chapter_ids[2], chapter_ids[1], chapter_ids[0]):
        response = client.get(
            "/api/books/historical-workbench-book/editions/base/"
            f"chapters/{chapter_id}/context"
        )
        assert response.status_code == 200
        body = response.json()
        assert body["chapter_id"] == chapter_id
        assert body["read_only_navigation"] is True
        assert body["before_state"]["availability"] == "SOURCE_CHAPTER_STATE_PROJECTION_MISSING"
        assert body["after_state"]["availability"] == "SOURCE_CHAPTER_STATE_PROJECTION_MISSING"
        assert body["chapter_delta"]["status"] == "SOURCE_CHAPTER_STATE_PROJECTION_MISSING"

    selected = client.get(
        f"/books/historical-workbench-book/editions/base/workbench?chapter_id={chapter_ids[1]}"
        "&node=chapter&mode=continuity&right_tab=state"
    )
    assert selected.status_code == 200
    assert "第2章" in selected.text
    assert "当前章节 · 第2章" in _visible_text(selected.text)
    assert "正在补齐这一章的故事状态" in _visible_text(selected.text)
    assert "当前没有可回指本章的原文状态证据" in _visible_text(selected.text)
    assert "SOURCE_CHAPTER_STATE_PROJECTION_MISSING" not in _visible_text(selected.text)
    assert "潮声里藏着一段坐标" in selected.text
    assert _read_only_snapshot(database) == before


def test_modes_tabs_and_right_tabs_have_readable_state(tmp_path: Path) -> None:
    database = _book(tmp_path, "mode-workbench-book")
    app = create_app(database, book_id="mode-workbench-book")
    client = TestClient(app)
    chapter_id = _chapter_ids(database)[0]

    page = client.get(
        "/books/mode-workbench-book/editions/base/workbench"
        f"?chapter_id={chapter_id}&node=chapter&mode=continuity&right_tab=state"
    )

    assert page.status_code == 200
    assert 'data-active-mode="continuity"' in page.text
    assert 'data-active-right-tab="state"' in page.text
    visible = _visible_text(page.text)
    assert "连续性审查" in visible
    assert "章末状态" in visible
    assert "当前没有可读取的章节状态" not in visible
    assert "正在补齐这一章的故事状态" in visible
    assert "SOURCE_CHAPTER_STATE_PROJECTION_MISSING" not in visible
    assert "anchor_chapter_ordinal" not in visible


def test_workbench_builds_only_the_state_requested_by_the_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database = _book(tmp_path, "workbench-query-budget")
    chapter_id = _chapter_ids(database)[1]
    calls = 0
    original = workbench_module.build_story_game_state

    def counted(*args: object, **kwargs: object) -> dict[str, object]:
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    def no_full_replay(*args: object, **kwargs: object) -> object:
        raise AssertionError("Workbench 普通读取不得完整审计 Event Chain")

    monkeypatch.setattr(workbench_module, "build_story_game_state", counted)
    monkeypatch.setattr(projection_module, "projection_from_connection", no_full_replay)

    workbench_module.build_workbench_context(
        database, "workbench-query-budget", "base", chapter_id=chapter_id, mode="home"
    )
    assert calls == 0
    workbench_module.build_workbench_context(
        database,
        "workbench-query-budget",
        "base",
        chapter_id=chapter_id,
        mode="state",
        state_tab="overview",
    )
    assert calls == 2
    workbench_module.build_workbench_context(
        database,
        "workbench-query-budget",
        "base",
        chapter_id=chapter_id,
        mode="state",
        state_tab="knowledge",
    )
    assert calls == 3


def test_author_workflow_surface_is_readable_and_embedded_in_workbench(
    tmp_path: Path,
) -> None:
    database = _book(tmp_path, "workflow-surface-book")
    app = create_app(database, book_id="workflow-surface-book")
    client = TestClient(app)

    legacy = client.get("/books/workflow-surface-book/workflow", follow_redirects=False)
    assert legacy.status_code == 302
    assert legacy.headers["location"].startswith(
        "/books/workflow-surface-book/editions/base/workbench?action=continue"
    )

    workflow = client.get(legacy.headers["location"])
    assert workflow.status_code == 200
    visible = _visible_text(workflow.text)
    assert "续写 · 第4章" in visible
    assert "续写设置" in visible
    assert "创新程度" in visible
    assert "创新方向" in visible
    assert "当前还没有作者任务" in visible
    assert "PLAN_ONLY" not in visible
    assert "WAITING_FOR_USER" not in visible
    assert workflow.text.count("data-workflow-form") == 1
    assert 'data-active-action="continue"' in workflow.text
    assert "workflow-shell" not in workflow.text
    assert workflow.text.count('data-toggle-pane="left"') == 2
    assert workflow.text.count('data-toggle-pane="right"') == 2

    workbench = client.get(
        "/books/workflow-surface-book/editions/base/workbench?action=continue"
    )
    assert workbench.status_code == 200
    assert "续写 · 第4章" in _visible_text(workbench.text)
    assert "续写设置" in _visible_text(workbench.text)
    assert workbench.text.count('data-toggle-pane="left"') == 2
    assert workbench.text.count('data-toggle-pane="right"') == 2


def test_product_shell_has_one_primary_nav_and_three_chapter_actions(tmp_path: Path) -> None:
    database = _book(tmp_path, "shell-test-book")
    app = create_app(database, book_id="shell-test-book")
    page = TestClient(app).get("/books/shell-test-book/editions/base/workbench")

    assert page.status_code == 200
    assert 'data-active-mode="home"' in page.text
    assert page.text.count("data-workbench-shell") == 1
    assert "续写下一章" in page.text
    assert "改写本章" in page.text
    assert "规划后续" in page.text
    assert "剧情规划" in page.text
    assert 'href="/books/shell-test-book/workflow"' not in page.text
    assert 'href="/books/shell-test-book/jobs"' not in page.text
    assert "data-activity-trigger" in page.text


def test_each_chapter_action_opens_its_center_and_keeps_chapter_anchor(
    tmp_path: Path,
) -> None:
    database = _book(tmp_path, "shell-test-book")
    app = create_app(database, book_id="shell-test-book")
    client = TestClient(app)
    chapter_id = _chapter_ids(database)[1]

    expected = {
        "continue": ("续写 · 第3章", "/handoffs/continuation"),
        "rewrite": ("改写 · 第2章", "/handoffs/revision"),
        "plan": ("规划 · 第3章以后", "/handoffs/continuation"),
    }
    for action, (title, endpoint) in expected.items():
        page = client.get(
            "/books/shell-test-book/editions/base/workbench"
            f"?action={action}&chapter_id={chapter_id}"
        )
        assert page.status_code == 200
        assert f'data-active-action="{action}"' in page.text
        assert title in _visible_text(page.text)
        assert endpoint in page.text
        assert page.text.count("data-workflow-form") == 1
        assert f"chapter_id={chapter_id}" in page.text


def test_activity_center_groups_system_work_and_keeps_author_tasks_separate(
    tmp_path: Path,
) -> None:
    database = _book(tmp_path, "shell-test-book")
    chapter_id = _chapter_ids(database)[-1]
    _insert_handoff(
        database,
        tmp_path / "activities",
        handoff_id="handoff-shell-plan",
        handoff_type="CONTINUATION",
        requested_stage="PLAN_ONLY",
        status="READY_FOR_CODEX",
        chapter_id=chapter_id,
        created_at="2026-08-10T10:00:00+00:00",
    )
    _insert_handoff(
        database,
        tmp_path / "activities",
        handoff_id="handoff-shell-profile",
        handoff_type="PROFILE_REANALYSIS",
        requested_stage="PROFILE_REANALYSIS",
        status="COMPLETED",
        chapter_id=chapter_id,
        created_at="2026-08-10T09:00:00+00:00",
    )
    with database.connect() as connection:
        connection.executemany(
            """
            INSERT INTO author_control_tasks(
                task_id, book_id, edition_id, title, task_type, description,
                horizon, lifecycle_status, priority, payload_json, created_at, updated_at
            ) VALUES (?, 'shell-test-book', 'base', ?, ?, '', 'MID', 'ACTIVE',
                      100, '{}', 'now', 'now')
            """,
            [
                ("task-story", "获得长枪", "AUTHOR_TASK"),
                ("task-hydration", "补齐第3章的故事状态", "SOURCE_STATE_HYDRATION"),
            ],
        )

    context = workflow_context(database, "shell-test-book", edition_id="base")
    assert [task["title"] for task in context["author_tasks"]] == ["获得长枪"]
    assert context["activity_center"]["badge_count"] == 1
    groups = {
        group["key"]: [item["title"] for item in group["items"]]
        for group in context["activity_center"]["groups"]
    }
    assert groups["running"] == ["第4章规划候选"]
    assert groups["completed"] == ["全书画像重新分析"]

    app = create_app(database, book_id="shell-test-book")
    page = TestClient(app).get(
        f"/books/shell-test-book/editions/base/workbench?chapter_id={chapter_id}"
    )
    assert "等待 AI 处理" in page.text
    assert "第4章规划候选" in page.text
    assert "任务中心" in page.text
    assert "task_directory" in page.text
    assert "READY_FOR_CODEX" not in _visible_text(page.text)

    planning = TestClient(app).get(
        "/books/shell-test-book/editions/base/workbench"
        f"?mode=plan&node=planning&planning_view=tasks&chapter_id={chapter_id}"
    )
    planning_visible = _visible_text(planning.text)
    assert "获得长枪" in planning_visible
    assert "补齐第3章的故事状态" not in planning_visible
    assert "不等于系统任务" in planning_visible


def test_chapter_anchor_is_shared_by_profile_planning_state_and_continuity(
    tmp_path: Path,
) -> None:
    database = _book(tmp_path, "shell-test-book")
    chapter_id = _chapter_ids(database)[0]
    app = create_app(database, book_id="shell-test-book")
    page = TestClient(app).get(
        "/books/shell-test-book/editions/base/workbench"
        f"?mode=analysis&node=worldbuilding&chapter_id={chapter_id}"
    )

    assert page.status_code == 200
    assert f'data-current-chapter-id="{chapter_id}"' in page.text
    assert f"mode=analysis&chapter_id={chapter_id}" in page.text
    state_link = (
        "mode=state&state_tab=overview&state_scope=character&truth_lens=AUTHOR"
        f"&chapter_id={chapter_id}"
    )
    assert state_link in page.text
    assert f"mode=continuity&node=chapter&chapter_id={chapter_id}" in page.text
    planning_link = (
        f"action=plan&node=planning&planning_view=candidates&chapter_id={chapter_id}"
    )
    assert planning_link in page.text


def test_navigation_and_item_scripts_preserve_history_scroll_and_current_state() -> None:
    root = Path(__file__).parents[2]
    script = (root / "src" / "novel_authoring" / "web" / "static" / "workbench.js").read_text(
        encoding="utf-8"
    )

    assert "options && options.fromPop" in script
    assert "bindScrollPersistence" in script
    assert "leftTreeScrollTop" in script
    assert "centerScrollTop" in script
    assert "rightScrollTop" in script
    assert "leftCollapsed" in script and "rightCollapsed" in script
    assert "history.pushState" in script
    assert "DROP_ITEM" not in script
    assert "没有当前证据" in script
    assert "已存在：" in script
    assert "item.record_id" in script
    assert "item.name" in script
    assert "item.label" in script
    assert (
        'form.querySelector("[data-item-submit]").addEventListener("click", submitItem)'
        in script
    )


def test_draft_is_provisional_and_explicit_save_does_not_touch_canon(tmp_path: Path) -> None:
    database = _book(tmp_path, "draft-workbench-book")
    root = tmp_path / "workspace" / "draft-workbench-book"
    draft_path = root / "drafts" / "draft-61.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("旧稿\n", encoding="utf-8")
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO chapter_contracts(
                contract_id, book_id, candidate_id, target_chapter_ordinal,
                mode, contract_json, contract_sha256, status, created_at,
                version, edition_id
            ) VALUES (?, ?, NULL, ?, 'faithful_continuation', ?, 'contract',
                      'READY', 'now', 1, 'base')
            """,
            (
                "contract-61",
                "draft-workbench-book",
                4,
                json.dumps({"lens": "CONTINUITY_ACTIVE_THREAD"}),
            ),
        )
        connection.execute(
            """
            INSERT INTO drafts(
                draft_id, book_id, contract_id, candidate_id, file_path,
                content_sha256, status, revision, created_at, task_id,
                edition_id, chapter_title, output_json, base_event_seq,
                base_projection_hash, validation_run_id
            ) VALUES (?, ?, ?, NULL, ?, 'old-content', 'VALIDATED', 1, 'now',
                      'task-61', 'base', '第4章 接续', ?, 0, 'empty', 'run-1')
            """,
            (
                "draft-61",
                "draft-workbench-book",
                "contract-61",
                str(draft_path),
                json.dumps(
                    {
                        "prose_markdown": "旧稿",
                        "state_changes": [{"kind": "ADDED", "description": "新线索"}],
                    },
                    ensure_ascii=False,
                ),
            ),
        )
        connection.execute(
            """
            INSERT INTO validation_reports(
                report_id, book_id, draft_id, validator, severity, passed,
                report_json, created_at, version
            ) VALUES ('report-61', ?, 'draft-61', 'test', 'INFO', 1, '{}', 'now', 1)
            """,
            ("draft-workbench-book",),
        )

    app = create_app(database, book_id="draft-workbench-book")
    client = TestClient(app)
    page = client.get(
        "/books/draft-workbench-book/editions/base/workbench?draft_id=draft-61"
        "&node=chapter&mode=continuity"
    )
    assert page.status_code == 200
    assert "草稿临时状态" in _visible_text(page.text)
    assert "草稿临时变化" in _visible_text(page.text)
    assert "PROVISIONAL_DRAFT_DELTA" not in _visible_text(page.text)
    assert "旧稿" in page.text

    before = _read_only_snapshot(database)
    saved = client.post(
        "/api/books/draft-workbench-book/editions/base/drafts/draft-61/content",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={"content": "新稿\n"},
    )
    assert saved.status_code == 200
    assert saved.json()["status"] == "DRAFT"
    assert draft_path.read_text(encoding="utf-8") == "新稿\n"
    with database.connect() as connection:
        draft = connection.execute(
            "SELECT status, validation_run_id, output_json FROM drafts WHERE draft_id='draft-61'"
        ).fetchone()
        reports = connection.execute(
            "SELECT COUNT(*) FROM validation_reports WHERE draft_id='draft-61'"
        ).fetchone()[0]
    assert draft is not None
    assert draft["status"] == "DRAFT"
    assert draft["validation_run_id"] is None
    assert json.loads(str(draft["output_json"]))["prose_markdown"] == "新稿"
    assert reports == 0
    assert _read_only_snapshot(database) == before


def test_web_doctor_checks_native_workbench_surface() -> None:
    result = web_doctor()

    assert result["ok"] is True
    assert result["checks"]["frontend"]["mode"] == "native-javascript-css"
    assert result["checks"]["routes"]["missing"] == []
    assert result["checks"]["api_health"]["ok"] is True


def test_library_mode_auto_discovers_canonical_sessions_and_opens_each_workbench(
    tmp_path: Path,
) -> None:
    library_root = tmp_path / "library"
    for book_id in ("session-a", "session-b"):
        source = tmp_path / f"{book_id}.md"
        source.write_text(f"第1章 {book_id}\n\n正文。\n", encoding="utf-8")
        add_book(
            LibraryAddOptions(
                book_id=book_id,
                title=f"标题 {book_id}",
                source=source,
                library_root=library_root,
            )
        )
    (library_root / ".raw-input").mkdir(parents=True)
    (library_root / ".raw-input" / "notes.md").write_text("输入素材", encoding="utf-8")

    app = create_app(Database(tmp_path / "boot.sqlite3"), library_root=library_root)
    client = TestClient(app)

    root = client.get("/", follow_redirects=False)
    assert root.status_code == 307
    assert root.headers["location"] == "/library"

    library = client.get("/api/library")
    assert library.status_code == 200
    assert [item["book_id"] for item in library.json()["books"]] == [
        "session-a",
        "session-b",
    ]
    page = client.get("/library")
    assert page.status_code == 200
    assert "标题 session-a" in page.text
    assert "标题 session-b" in page.text
    assert ".raw-input" not in page.text
    assert page.text.count("准备初始化") == 2

    workbench = client.get("/books/session-b/editions/base/workbench")
    assert workbench.status_code == 200
    assert "标题 session-b" in workbench.text
    assert "标题 session-a" in workbench.text
    assert "还需要初始化" in workbench.text
    assert 'data-wb-chapter-tree' not in workbench.text
