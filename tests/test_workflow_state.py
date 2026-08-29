from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.run_ledger import create_or_load_run, save_node_prompt
from story_mvp.storage import (
    approve_character_artifact,
    approve_creative_artifact,
    compose_book_content,
    create_book,
    replace_chapter,
    save_chapter,
    write_book,
    write_creative_artifact,
)
from story_mvp.workflow_state import workflow_impact, workflow_status
from story_mvp.workflow_cli import apply_response


def _book_content(
    *,
    design: str = "DESIGN",
    long_plan: str = "LONG_PLAN",
    future_10: str = "## 第18章：十八\n具体剧情：A\n\n## 第19章：十九\n具体剧情：B",
    canon_state: str = "CANON",
) -> str:
    return compose_book_content(
        {
            "design": design,
            "long_plan": long_plan,
            "small_plan": future_10,
            "status": canon_state,
        }
    )


def _run(book_dir: Path, chapter: int) -> None:
    create_or_load_run(book_dir, chapter, writer_mode="single")
    save_node_prompt(book_dir, chapter, "director", "PROMPT")


def _artifacts(workspace: Path, book_id: str) -> dict[str, dict[str, object]]:
    return workflow_status(workspace / book_id)["artifacts"]


def test_world_vision_stales_split_future_chain_but_protects_completed_body(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    write_creative_artifact("demo", "world_vision", "WORLD-1", tmp_path)
    approve_creative_artifact("demo", "world_vision", tmp_path)
    write_creative_artifact("demo", "power_seed", "# POWER SEED｜能力\n\n## Core Fantasy\n能力。", tmp_path)
    write_creative_artifact("demo", "human_seed", "# HUMAN SEED｜人物／欲望\n\n## Core Obsession\n想赢。", tmp_path)
    approve_character_artifact("demo", tmp_path)
    write_creative_artifact("demo", "proposal", "PROGRAM-1", tmp_path)
    write_book("demo", _book_content(), tmp_path)
    _run(book_dir, 1)
    save_chapter("demo", 1, "chapter one", tmp_path)
    _run(book_dir, 18)

    write_creative_artifact("demo", "world_vision", "WORLD-2", tmp_path)
    artifacts = _artifacts(tmp_path, "demo")

    for key in (
        "creative.power_seed",
        "creative.human_seed",
        "creative.character_card",
        "creative.story_program",
        "book.design",
        "book.long_plan",
        "book.future_10",
        "chapter.18.run",
    ):
        assert artifacts[key]["status"] == "STALE"
    assert artifacts["chapter.1.body"]["status"] == "DONE"
    assert artifacts["chapter.1.body"]["freshness"] == "fresh"

def test_power_seed_change_does_not_stale_world_but_reopens_character(tmp_path: Path) -> None:
    create_book("demo", tmp_path)
    write_creative_artifact("demo", "world_vision", "WORLD-1", tmp_path)
    approve_creative_artifact("demo", "world_vision", tmp_path)
    write_creative_artifact("demo", "power_seed", "# POWER SEED｜A\n\n## Core Fantasy\nA", tmp_path)
    write_creative_artifact("demo", "human_seed", "# HUMAN SEED｜人／X\n\n## Core Obsession\nX", tmp_path)
    approve_character_artifact("demo", tmp_path)
    before = _artifacts(tmp_path, "demo")

    write_creative_artifact("demo", "power_seed", "# POWER SEED｜B\n\n## Core Fantasy\nB", tmp_path)
    after = _artifacts(tmp_path, "demo")

    assert after["creative.world_vision"]["revision"] == before["creative.world_vision"]["revision"]
    assert after["creative.world_vision"]["status"] == before["creative.world_vision"]["status"]
    assert after["creative.power_seed"]["revision"] == before["creative.power_seed"]["revision"] + 1
    assert after["creative.character_card"]["status"] == "STALE"

def test_future_10_change_only_stales_existing_runs_in_changed_entries(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    write_book(
        "demo",
        _book_content(
            future_10="## 第18章：十八\n具体剧情：A\n\n## 第19章：十九\n具体剧情：B"
        ),
        tmp_path,
    )
    _run(book_dir, 18)
    _run(book_dir, 19)
    before = _artifacts(tmp_path, "demo")
    changed = _book_content(
        future_10="## 第18章：十八\n具体剧情：CHANGED\n\n## 第19章：十九\n具体剧情：B"
    )
    write_book("demo", changed, tmp_path)
    after = _artifacts(tmp_path, "demo")

    assert after["chapter.18.run"]["status"] == "STALE"
    assert after["chapter.19.run"]["status"] == before["chapter.19.run"]["status"]
    impact = workflow_impact(book_dir, "book.future_10")
    assert impact["existing_nodes_affected"] == ["chapter.18.run"]
    assert impact["protected_completed_chapters"] == []


def test_canon_change_stales_future_runs_without_staling_plans(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    write_book("demo", _book_content(canon_state="CANON-1"), tmp_path)
    _run(book_dir, 18)
    before = _artifacts(tmp_path, "demo")
    write_book("demo", _book_content(canon_state="CANON-2"), tmp_path)
    after = _artifacts(tmp_path, "demo")

    assert after["book.long_plan"]["status"] == before["book.long_plan"]["status"]
    assert after["book.future_10"]["status"] == before["book.future_10"]["status"]
    assert after["chapter.18.run"]["status"] == "STALE"


def test_editing_chapter_body_stales_its_state_delta_and_later_runs_only(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    write_book("demo", _book_content(), tmp_path)
    _run(book_dir, 1)
    save_chapter("demo", 1, "chapter one", tmp_path)
    _run(book_dir, 2)
    _run(book_dir, 3)
    replace_chapter("demo", 1, "chapter one edited", tmp_path)
    artifacts = _artifacts(tmp_path, "demo")

    assert artifacts["chapter.1.state_delta"]["status"] == "STALE"
    assert artifacts["chapter.2.run"]["status"] == "STALE"
    assert artifacts["chapter.3.run"]["status"] == "STALE"
    assert "chapter.1.body" not in artifacts["chapter.1.body"].get("stale_from", [])
    impact = workflow_impact(book_dir, "chapter.1.body")
    assert "chapter.1.state_delta" in impact["existing_nodes_affected"]
    assert "chapter.2.run" in impact["existing_nodes_affected"]


def test_same_content_does_not_increment_revision_or_stale(tmp_path: Path) -> None:
    create_book("demo", tmp_path)
    content = _book_content()
    write_book("demo", content, tmp_path)
    before = _artifacts(tmp_path, "demo")
    write_book("demo", content, tmp_path)
    after = _artifacts(tmp_path, "demo")

    assert after == before


def test_book_section_diff_only_changes_future_10_revision(tmp_path: Path) -> None:
    create_book("demo", tmp_path)
    initial = _book_content()
    write_book("demo", initial, tmp_path)
    before = _artifacts(tmp_path, "demo")
    write_book("demo", _book_content(future_10="## 第18章：十八\n具体剧情：CHANGED"), tmp_path)
    after = _artifacts(tmp_path, "demo")

    assert after["book.future_10"]["revision"] == before["book.future_10"]["revision"] + 1
    for key in ("book.design", "book.long_plan", "book.canon_state"):
        assert after[key]["revision"] == before[key]["revision"]


def test_old_book_lazy_state_does_not_rewrite_existing_files(tmp_path: Path) -> None:
    book_dir = tmp_path / "old-book"
    book_dir.mkdir()
    book_text = "# 小说总体设计画像\n\n旧书内容\n"
    (book_dir / "BOOK.md").write_text(book_text, encoding="utf-8")
    (book_dir / "PROMPTS.md").write_text("", encoding="utf-8")
    (book_dir / "chapters").mkdir()

    snapshot = workflow_status(book_dir)

    assert snapshot["version"] == 1
    assert (book_dir / "BOOK.md").read_text(encoding="utf-8") == book_text
    assert (book_dir / "WORKFLOW_STATE.json").is_file()
    state = json.loads((book_dir / "WORKFLOW_STATE.json").read_text(encoding="utf-8"))
    assert "# 小说总体设计画像" not in json.dumps(state, ensure_ascii=False)


def test_workflow_refresh_prunes_unsupported_static_artifacts(tmp_path: Path) -> None:
    book_dir = create_book("demo", tmp_path)
    _run(book_dir, 1)
    workflow_status(book_dir)
    state_path = book_dir / "WORKFLOW_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["artifacts"]["book.obsolete"] = {
        "revision": 1,
        "status": "DONE",
        "freshness": "fresh",
        "source": "legacy",
    }
    state["artifacts"]["chapter.1.run"]["source_revisions"]["book.obsolete"] = 1
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    refreshed = workflow_status(book_dir)

    assert "book.obsolete" not in refreshed["artifacts"]
    assert "book.obsolete" not in refreshed["artifacts"]["chapter.1.run"]["source_revisions"]


def test_workflow_and_impact_api_use_real_book_state(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "api-demo"}).status_code == 201
    book = _book_content()
    assert client.put("/api/books/api-demo/book", json={"content": book}).status_code == 200
    workflow = client.get("/api/books/api-demo/workflow")
    assert workflow.status_code == 200
    assert workflow.json()["version"] == 1
    impact = client.get(
        "/api/books/api-demo/workflow/impact",
        params={"artifact": "book.future_10"},
    )
    assert impact.status_code == 200
    assert impact.json()["artifact"] == "book.future_10"


def test_existing_chapter_can_be_manually_edited_through_unified_save_path(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "chapter-edit"}).status_code == 201
    assert client.post(
        "/api/books/chapter-edit/chapters",
        json={"chapter_number": 1, "content": "first body"},
    ).status_code == 200
    edited = client.put(
        "/api/books/chapter-edit/chapters/1",
        json={"content": "edited body"},
    )
    assert edited.status_code == 200
    assert client.get("/api/books/chapter-edit/chapters/1").json()["content"] == "edited body"


def test_codex_external_apply_uses_shared_service_and_cleans_workflow_temp(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    create_book("external", tmp_path)
    write_book("external", _book_content(), tmp_path)
    book_dir = tmp_path / "external"
    temp_dir = book_dir / ".workflow_tmp"
    temp_dir.mkdir()
    response = temp_dir / "future-10.md"
    response.write_text("## 第18章：十八\n具体剧情：外部更新", encoding="utf-8")

    result = apply_response(
        book_id="external",
        artifact="book.future_10",
        input_path=response,
        source="codex_external",
    )

    assert result["status"] == "applied"
    assert result["source"] == "codex_external"
    assert not response.exists()
    assert "外部更新" in (book_dir / "BOOK.md").read_text(encoding="utf-8")


def test_codex_external_apply_run_response_uses_run_ledger(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    book_dir = create_book("external-run", tmp_path)
    _run(book_dir, 18)
    response = tmp_path / "response.md"
    response.write_text("DIRECTOR RESPONSE", encoding="utf-8")

    apply_response(
        book_id="external-run",
        artifact="chapter.18.run",
        input_path=response,
        source="codex_external",
        chapter=18,
        node="director",
    )

    manifest = json.loads(
        (book_dir / "runs" / "chapter-0018" / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["nodes"]["director"]["status"] == "completed"
    assert (book_dir / "runs" / "chapter-0018" / "director_response.md").read_text(encoding="utf-8") == "DIRECTOR RESPONSE"


def test_codex_external_authority_reviser_auto_adopts_final_source(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    book_dir = create_book("external-reviser", tmp_path)
    _run(book_dir, 18)
    from story_mvp.run_ledger import save_node_prompt, save_node_response

    for node in ("director", "curator", "primary"):
        save_node_prompt(book_dir, 18, node, f"{node} prompt")
        save_node_response(book_dir, 18, node, f"{node} response")
    save_node_prompt(book_dir, 18, "authority_reviser", "authority prompt")

    response = tmp_path / "authority-response.md"
    response.write_text("# 正式正文\n\nREVISED FINAL", encoding="utf-8")
    apply_response(
        book_id="external-reviser",
        artifact="chapter.18.run",
        input_path=response,
        source="codex_external",
        chapter=18,
        node="authority_reviser",
    )

    manifest = json.loads(
        (book_dir / "runs" / "chapter-0018" / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["nodes"]["authority_reviser"]["status"] == "adopted"
    assert manifest["final_source"] == "authority_reviser"
    assert manifest["nodes"]["state_delta"]["status"] in {"pending", "stale"}


def test_codex_external_authority_reviser_prepares_bounded_outcome_repair(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    book_dir = create_book("external-outcome-repair", tmp_path)
    _run(book_dir, 19)
    from story_mvp.run_ledger import save_node_prompt, save_node_response

    for node in ("director", "curator", "primary"):
        save_node_prompt(book_dir, 19, node, f"{node} prompt")
        save_node_response(book_dir, 19, node, f"{node} response")
    authority_prompt = """FROZEN CHAPTER MISSION
状态变化：顾停舟重伤。
上游计划已批准结果（本章必须同时成立；若与已发生 Canon 冲突则 Canon 优先）：顾停舟本人进入镇海，镇海潮兽被压回远潮。
结尾推动力：战后结算。
"""
    save_node_prompt(book_dir, 19, "authority_reviser", authority_prompt)

    response = tmp_path / "authority-response.md"
    response.write_text(
        "# 正式正文\n\n顾停舟以照域承住镇海潮兽，最终把它压回远潮。",
        encoding="utf-8",
    )
    result = apply_response(
        book_id="external-outcome-repair",
        artifact="chapter.19.run",
        input_path=response,
        source="codex_external",
        chapter=19,
        node="authority_reviser",
    )

    manifest = json.loads(
        (book_dir / "runs" / "chapter-0019" / "manifest.json").read_text(encoding="utf-8")
    )
    reviser = manifest["nodes"]["authority_reviser"]
    assert result["status"] == "repair_required"
    assert result["repair_prompt_file"] == "authority_reviser_prompt.md"
    assert reviser["status"] == "pending"
    assert reviser["attempts"] == 2
    assert manifest["final_source"] is None
    repair_prompt = (book_dir / "runs" / "chapter-0019" / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    assert "条件性 Outcome Repair" in repair_prompt
    assert "顾停舟本人进入镇海" in repair_prompt
