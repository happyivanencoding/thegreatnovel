from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.progression.discovery import import_kernel_contract_discovery
from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.web.app import create_app
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    HandoffWorkflowError,
    claim_handoff,
    update_handoff_status,
)


def _existing_book(tmp_path: Path) -> tuple[Database, list[dict[str, object]]]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "novel.md").write_text(
        "\n\n".join(
            [
                "第1章 失去\n\n矿工失去了超凡能力，只能听见废弃矿脉的回声。",
                "第2章 回声\n\n他发现回声能够重塑身体，但每次尝试都会失去一段记忆。",
                "第3章 未来\n\n只有到达第三章才出现的未来组织名称。",
            ]
        ),
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="semantic-discovery-book",
        title="原创矿脉成长测试",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "semantic-discovery-book" / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = [
            dict(item)
            for item in connection.execute(
                "SELECT chapter_id, ordinal, title FROM chapters "
                "WHERE book_id='semantic-discovery-book' ORDER BY ordinal"
            ).fetchall()
        ]
    return database, chapters


def _proposal_bundle() -> dict[str, object]:
    bundle = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "一名失去超凡能力的矿工发现，废弃矿脉中残留的声音能够重塑他的身体。",
            genre_hint="肉身进化",
            contract_prefix="semantic-discovery",
        )
    ).model_dump(mode="json")
    for key in (
        "reader_experience",
        "narrative_drive",
        "genre",
        "progression",
        "world_expansion",
        "payoff_channels",
    ):
        value = bundle.get(key)
        if isinstance(value, dict) and "status" in value:
            value["status"] = "INFERRED_PROPOSAL"
    return bundle


def _complete_discovery(
    database: Database,
    handoff: dict[str, object],
    artifact: dict[str, object],
) -> None:
    handoff_id = str(handoff["handoff_id"])
    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads((task_directory / "task.json").read_text(encoding="utf-8"))
    artifact_path = task_directory / "artifacts" / "kernel_contract_discovery" / "proposal.json"
    artifact_path.parent.mkdir(parents=True)
    artifact_path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    claim = claim_handoff(database, handoff_id, "semantic-discovery-test")
    token = str(claim["claim_token"])
    update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.RUNNING,
        claim_token=token,
    )
    update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.COMPLETED,
        claim_token=token,
        result={
            "handoff_id": handoff_id,
            "handoff_type": "KERNEL_CONTRACT_DISCOVERY",
            "requested_stage": "KERNEL_CONTRACT_DISCOVERY",
            "completed_stage": "CONTRACT_PROPOSAL_READY",
            "book_id": "semantic-discovery-book",
            "edition_id": "base",
            "status": "COMPLETED",
            "task_ids": [],
            "candidate_ids": [],
            "selected_candidate_id": None,
            "contract_id": None,
            "draft_id": None,
            "campaign_id": None,
            "revision_unit_ids": [],
            "artifact_paths": [
                "artifacts/kernel_contract_discovery/proposal.json"
            ],
            "validation_summary": {"schema_valid": True},
            "warnings": [],
            "next_action": "由 Python 收集并由作者逐项确认",
            "canon_committed": False,
            "edition_activated": False,
            "base_event_seq": task["base_event_seq"],
            "base_projection_hash": task["base_projection_hash"],
            "metric_run_ids": [],
            "metric_bundle_hash": task["metric_bundle_hash"],
            "completed_at": "2026-08-12T00:00:00Z",
        },
    )


def test_semantic_discovery_handoff_imports_review_only_contracts(tmp_path: Path) -> None:
    database, chapters = _existing_book(tmp_path)
    app = create_app(database, book_id="semantic-discovery-book")
    client = TestClient(app)
    headers = {"X-CSRF-Token": app.state.csrf_token}
    with database.connect() as connection:
        authority_before = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM events), "
                "(SELECT COUNT(*) FROM canon_commits), "
                "(SELECT COUNT(*) FROM author_truths)"
            ).fetchone()
        )
    response = client.post(
        "/api/books/semantic-discovery-book/editions/base/"
        "progression-contracts/discovery",
        headers=headers,
        json={"context_chapter_id": str(chapters[1]["chapter_id"])},
    )
    assert response.status_code == 200
    handoff = response.json()
    task_directory = Path(handoff["task_directory"])
    context = json.loads(
        (task_directory / "kernel_discovery_context.json").read_text(encoding="utf-8")
    )
    assert context["discovery_mode"] == "SEMANTIC_CONTROLLED"
    assert context["efficiency"]["source_chapters_read"] == 2
    assert context["efficiency"]["full_book_reread"] is False
    assert "只有到达第三章" not in json.dumps(context, ensure_ascii=False)
    chapter_id = str(chapters[1]["chapter_id"])
    with database.connect() as connection:
        span = connection.execute(
            "SELECT span_id, excerpt FROM source_spans "
            "WHERE book_id='semantic-discovery-book' AND chapter_id=? "
            "ORDER BY start_line LIMIT 1",
            (chapter_id,),
        ).fetchone()
    assert span is not None
    quote = str(span["excerpt"])[-12:]
    artifact = {
        "schema_version": "kernel-contract-discovery-v1",
        "discovery_mode": "SEMANTIC_CONTROLLED",
        "book_id": "semantic-discovery-book",
        "edition_id": "base",
        "context_chapter_id": chapter_id,
        "context_chapter_ordinal": 2,
        "source_chapter_ids": context["bounded_inputs"]["chapter_ids"],
        "evidence": [
            {
                "claim": "长期推进依赖有代价的身体成长",
                "source_layer": "SOURCE_TEXT",
                "chapter_id": chapter_id,
                "chapter_ordinal": 2,
                "source_span_ids": [str(span["span_id"])],
                "evidence_quote": quote,
                "confidence": 0.91,
            }
        ],
        "unknowns": ["世界天花板尚未显露"],
        "proposal_bundle": _proposal_bundle(),
        "author_confirmation_required": True,
        "canon_committed": False,
    }
    _complete_discovery(database, handoff, artifact)
    collected = client.post(
        "/api/books/semantic-discovery-book/editions/base/"
        f"progression-contracts/discovery/{handoff['handoff_id']}/collect",
        headers=headers,
    )
    assert collected.status_code == 200
    payload = collected.json()
    assert payload["discovery_mode"] == "SEMANTIC_CONTROLLED"
    assert len(payload["created"]) == 7
    assert {item["status"] for item in payload["created"]} == {"INFERRED_PROPOSAL"}
    assert {item["source"] for item in payload["created"]} == {
        "KERNEL_CONTRACT_DISCOVERY"
    }
    with database.connect() as connection:
        authority_after = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM events), "
                "(SELECT COUNT(*) FROM canon_commits), "
                "(SELECT COUNT(*) FROM author_truths)"
            ).fetchone()
        )
    assert authority_after == authority_before


def test_semantic_discovery_rejects_future_chapter_evidence(tmp_path: Path) -> None:
    database, chapters = _existing_book(tmp_path)
    app = create_app(database, book_id="semantic-discovery-book")
    client = TestClient(app)
    headers = {"X-CSRF-Token": app.state.csrf_token}
    handoff = client.post(
        "/api/books/semantic-discovery-book/editions/base/"
        "progression-contracts/discovery",
        headers=headers,
        json={"context_chapter_id": str(chapters[1]["chapter_id"])},
    ).json()
    future_id = str(chapters[2]["chapter_id"])
    with database.connect() as connection:
        future_span = connection.execute(
            "SELECT span_id, excerpt FROM source_spans WHERE chapter_id=? LIMIT 1",
            (future_id,),
        ).fetchone()
    assert future_span is not None
    artifact = {
        "schema_version": "kernel-contract-discovery-v1",
        "discovery_mode": "SEMANTIC_CONTROLLED",
        "book_id": "semantic-discovery-book",
        "edition_id": "base",
        "context_chapter_id": str(chapters[1]["chapter_id"]),
        "context_chapter_ordinal": 2,
        "source_chapter_ids": [future_id],
        "evidence": [
            {
                "claim": "偷看未来章节",
                "source_layer": "SOURCE_TEXT",
                "chapter_id": future_id,
                "chapter_ordinal": 3,
                "source_span_ids": [str(future_span["span_id"])],
                "evidence_quote": str(future_span["excerpt"])[-12:],
                "confidence": 1.0,
            }
        ],
        "unknowns": [],
        "proposal_bundle": _proposal_bundle(),
        "author_confirmation_required": True,
        "canon_committed": False,
    }
    _complete_discovery(database, handoff, artifact)
    with pytest.raises(HandoffWorkflowError, match="未冻结章节"):
        import_kernel_contract_discovery(database, handoff_id=str(handoff["handoff_id"]))
