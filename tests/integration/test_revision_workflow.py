from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.edition import (
    EditionPurpose,
    OfficialRole,
    activate_edition,
    create_edition,
    get_edition,
)
from novel_authoring.ingest.service import ingest_book
from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.reference_corpus.query import (
    ProseControlCardProjection,
    ReferenceCorpusQueryEcho,
    ReferenceCorpusQueryRequest,
    ReferenceCorpusQueryResponse,
    SourceRefProjection,
)
from novel_authoring.reference_corpus.semantic_models import (
    EvidenceScope,
    SemanticMaturity,
    SemanticStatus,
)
from novel_authoring.revision import (
    RevisionSpec,
    approve_revision_campaign,
    build_revision_impact,
    build_revision_plan,
    complete_revision_impact_audit,
    create_revision_campaign,
    import_revision_draft,
    prepare_revision_draft_task,
    validate_revision_campaign,
)
from novel_authoring.revision.service import RevisionWorkflowError
from novel_authoring.workflows.edition_export import export_edition


def _setup(tmp_path: Path) -> tuple[Database, Path]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "book.md").write_text(
        "## 第一章 缺口\n主角缺少晶体。\n\n## 第二章 夜袭\n夜袭逼近。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="revision-book",
        title="改写测试",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "revision-book" / "state.sqlite3")
    create_edition(database, "revision-book", "edition-r1", "改写候选")
    return database, workspace


def _spec() -> dict[str, object]:
    return {
        "campaign_name": "修正晶体缺口",
        "revision_kind": "correction",
        "intent": "把第一章错误的资源事实改为已获得晶体",
        "target_scope": {"chapter_ranges": [[1, 1]], "semantic_queries": []},
        "canon_changes": [],
        "entity_changes": [],
        "must_preserve": ["夜袭"],
        "must_change": ["晶体"],
        "forbidden_changes": [],
        "propagation_rules": [],
        "style_policy": {},
        "completion_policy": {},
    }


def _prepare_campaign(database: Database) -> tuple[str, str, dict[str, object]]:
    campaign = create_revision_campaign(database, "revision-book", _spec(), edition_id="edition-r1")
    impact = build_revision_impact(database, "revision-book", str(campaign["campaign_id"]))
    complete_revision_impact_audit(
        database,
        "revision-book",
        str(campaign["campaign_id"]),
        [{"impact_id": item["impact_id"], "status": "HANDLED"} for item in impact["items"]],
    )
    plan = build_revision_plan(database, "revision-book", str(campaign["campaign_id"]))
    unit_id = str(plan["units"][0]["unit_id"])
    task = prepare_revision_draft_task(
        database, "revision-book", str(campaign["campaign_id"]), unit_id
    )
    return str(campaign["campaign_id"]), unit_id, task


def _write_output(
    database: Database, tmp_path: Path, campaign_id: str, unit_id: str, task: dict[str, object]
) -> Path:
    with database.connect() as connection:
        unit = connection.execute(
            "SELECT base_chapter_id, base_content_sha256 FROM revision_units WHERE unit_id=?",
            (unit_id,),
        ).fetchone()
    output = {
        "task_type": "REVISION_DRAFT",
        "task_id": task["task_id"],
        "campaign_id": campaign_id,
        "unit_id": unit_id,
        "edition_id": "edition-r1",
        "base_chapter_id": unit["base_chapter_id"],
        "base_content_sha256": unit["base_content_sha256"],
        "replacement_title": "缺口",
        "replacement_markdown": "主角已经拥有晶体。",
        "change_map": [
            {
                "source_span_id": "source-span",
                "old_quote": "缺少晶体",
                "new_quote": "拥有晶体",
                "change_class": "REQUIRED",
                "reason": "修正明确错误",
            }
        ],
        "state_changes": [],
        "facts_superseded": [],
        "facts_added": [],
        "relationships_updated": [],
        "knowledge_updates": [],
        "invariant_evidence": {"夜袭": ["夜袭逼近"]},
        "required_change_evidence": {"晶体": ["拥有晶体"]},
        "stale_reference_checks": [],
        "character_fit_inputs": {},
        "style_fit_inputs": {},
        "notes": ["保留原章节叙事视角"],
    }
    path = tmp_path / "revision-output.json"
    path.write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")
    return path


def test_revision_spec_rejects_unknown_fields() -> None:
    value = _spec()
    value["unknown"] = True
    with pytest.raises(ValueError):
        RevisionSpec.model_validate(value)


def test_edition_purpose_is_separate_from_lifecycle(tmp_path: Path) -> None:
    database, _ = _setup(tmp_path)
    base = get_edition(database, "revision-book", "base")
    revision = get_edition(database, "revision-book", "edition-r1")
    alternate = create_edition(
        database,
        "revision-book",
        "alternate-r1",
        "第二章备选路线",
        edition_purpose=EditionPurpose.ALTERNATE_ROUTE,
        fork_chapter_ordinal=2,
        created_by_action="ALTERNATE_ROUTE",
    )

    assert base.edition_purpose is EditionPurpose.SOURCE_BASE
    assert base.official_role is OfficialRole.CURRENT
    assert revision.edition_purpose is EditionPurpose.AUTHOR_REVISION
    assert revision.official_role is OfficialRole.CANDIDATE
    assert alternate.edition_purpose is EditionPurpose.ALTERNATE_ROUTE
    assert alternate.official_role is OfficialRole.ALTERNATE
    assert alternate.fork_chapter_ordinal == 2


def test_revision_workflow_approval_then_separate_activation(tmp_path: Path) -> None:
    database, workspace = _setup(tmp_path)
    campaign_id, unit_id, task = _prepare_campaign(database)
    output_path = _write_output(database, tmp_path, campaign_id, unit_id, task)
    import_revision_draft(database, "revision-book", output_path)
    assert validate_revision_campaign(database, "revision-book", campaign_id)["passed"]
    committed = approve_revision_campaign(
        database,
        "revision-book",
        campaign_id,
        confirmation="批准改写版本",
    )
    assert committed["activation_required"] is True
    with database.connect() as connection:
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM chapter_variants WHERE campaign_id=? AND active=1",
                (campaign_id,),
            ).fetchone()[0]
            == 1
        )
        assert (
            connection.execute(
                "SELECT status FROM editions WHERE edition_id='edition-r1'"
            ).fetchone()[0]
            == "VALIDATED"
        )
        assert tuple(
            connection.execute(
                "SELECT source_type, status FROM book_profile_refresh_proposals "
                "WHERE book_id='revision-book' AND edition_id='edition-r1' "
                "ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
        ) == ("REVISION_COMMIT", "PENDING")
    with pytest.raises(RevisionWorkflowError):
        approve_revision_campaign(
            database, "revision-book", campaign_id, confirmation="批准改写版本"
        )
    activated = activate_edition(
        database,
        "revision-book",
        "edition-r1",
        confirmation="启用改写版本",
    )
    assert activated.status.value == "ACTIVE"
    exported = export_edition(database, "revision-book", "edition-r1")
    export_dir = Path(str(exported["path"]))
    assert {item for item in exported["files"].values()} <= {
        path.name for path in export_dir.iterdir()
    }
    assert "主角已经拥有晶体" in (export_dir / "complete_edition.md").read_text(encoding="utf-8")
    assert (workspace / "revision-book" / "editions" / "edition-r1").exists()


def test_revision_approval_requires_exact_phrase(tmp_path: Path) -> None:
    database, _ = _setup(tmp_path)
    campaign_id, unit_id, task = _prepare_campaign(database)
    import_revision_draft(
        database, "revision-book", _write_output(database, tmp_path, campaign_id, unit_id, task)
    )
    validate_revision_campaign(database, "revision-book", campaign_id)
    with pytest.raises(RevisionWorkflowError, match="批准改写版本"):
        approve_revision_campaign(
            database, "revision-book", campaign_id, confirmation="批准写入正史"
        )


def test_revision_event_projection_isolated_from_base(tmp_path: Path) -> None:
    database, _ = _setup(tmp_path)
    from novel_authoring.canon.events import EventStatus, EventStore
    from novel_authoring.canon.projection import rebuild_projection
    from novel_authoring.domain.models import InformationStatus

    EventStore(database).append(
        book_id="revision-book",
        edition_id="edition-r1",
        event_type="FACT_ASSERTED",
        aggregate_type="fact",
        aggregate_id="derived-fact",
        payload={"fact_id": "derived-fact", "predicate": "state", "object": "new"},
        source_kind="TEST",
        status=EventStatus.COMMITTED,
        information_state=InformationStatus.CANON,
    )
    assert (
        "derived-fact"
        not in rebuild_projection(database, "revision-book", edition_id="base", persist=False).facts
    )
    assert (
        "derived-fact"
        in rebuild_projection(
            database, "revision-book", edition_id="edition-r1", persist=False
        ).facts
    )


def test_revision_reference_context_is_ordered_and_compact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database, _ = _setup(tmp_path)
    calls: list[ReferenceCorpusQueryRequest] = []

    def fake_query(
        request: ReferenceCorpusQueryRequest, *, corpus_root: Path | None = None
    ) -> ReferenceCorpusQueryResponse:
        del corpus_root
        calls.append(request)
        payload = request.model_dump(mode="json")
        prose_card = ProseControlCardProjection(
            card_id="prose-control-test",
            card_type="prose-control",
            knowledge_level=CardKnowledgeLevel.CORPUS_SYNTHESIS,
            status=SemanticStatus.REFERENCE_ONLY,
            source_book_ids=["source-book-a", "source-book-b", "source-book-c"],
            category_ids=["玄幻", "科幻"],
            creative_problem_tags=["prose-realization"],
            reader_experiences=[],
            narrative_drives=[],
            payoff_channels=[],
            evidence_scope=EvidenceScope.MULTI_CATEGORY,
            maturity=SemanticMaturity.BROAD,
            source_refs=[
                SourceRefProjection(
                    source_book_id="source-book-a",
                    source_id="source-a",
                    distill_id="distill-a",
                    segment_id="segment-a",
                    line_start=1,
                    line_end=2,
                )
            ],
            metadata_match_fields=["scene_functions"],
            control_topic="动作先于解释",
            applicable_scene_functions=["PAYOFF"],
            guidance="先让动作和反馈发生，再补解释。",
            variants=["动作反馈"],
            when_to_use=["读者只能复述能力名"],
            failure_signals=["技能名清单"],
            transfer_boundary="只迁移抽象表达控制。",
        )
        is_prose = payload["purpose"] == "PROSE"
        return ReferenceCorpusQueryResponse(
            schema_version="reference-corpus-query-v1",
            purpose=payload["purpose"],
            query=ReferenceCorpusQueryEcho.model_validate(
                {key: value for key, value in payload.items() if key != "purpose"}
            ),
            status="ENABLED" if is_prose else "ZERO_RESULTS",
            cards=[prose_card] if is_prose else [],
            knowledge_gaps=[] if is_prose else ["测试无可用卡片"],
            warnings=[] if is_prose else ["soft-fail：测试 Reference Corpus zero results"],
        )

    monkeypatch.setattr(
        "novel_authoring.revision.service.query_reference_corpus", fake_query
    )
    spec = _spec()
    spec["style_policy"] = {
        "creative_problem_tags": ["breakthrough"],
        "reader_experiences": ["BREAKTHROUGH"],
        "narrative_drives": ["POWER_PROGRESSION"],
        "payoff_channels": ["POWER_BREAKTHROUGH"],
        "scene_functions": ["PAYOFF"],
        "max_cards": 3,
    }
    campaign = create_revision_campaign(database, "revision-book", spec, edition_id="edition-r1")
    campaign_id = str(campaign["campaign_id"])
    impact = build_revision_impact(database, "revision-book", campaign_id)
    assert calls == []
    complete_revision_impact_audit(
        database,
        "revision-book",
        campaign_id,
        [
            {"impact_id": item["impact_id"], "status": "HANDLED"}
            for item in cast(list[dict[str, Any]], impact["items"])
        ],
    )
    assert calls == []

    plan = build_revision_plan(database, "revision-book", campaign_id)
    assert len(calls) == 1
    planning_request = calls[0]
    assert planning_request.purpose == "PLANNING"
    assert planning_request.creative_problem.startswith("修订意图：")
    assert planning_request.creative_problem_tags == ["breakthrough"]
    assert planning_request.reader_experiences == ["BREAKTHROUGH"]
    assert planning_request.narrative_drives == ["POWER_PROGRESSION"]
    assert planning_request.payoff_channels == ["POWER_BREAKTHROUGH"]
    assert planning_request.scene_functions == ["PAYOFF"]
    assert planning_request.max_cards == 3
    planning_context = cast(dict[str, Any], plan["reference_planning_context"])
    assert planning_context["status"] == "ZERO_RESULTS"
    assert planning_context["warnings"]
    assert Path(str(planning_context["snapshot_path"])).is_file()

    units = cast(list[dict[str, Any]], plan["units"])
    task = prepare_revision_draft_task(
        database, "revision-book", campaign_id, str(units[0]["unit_id"])
    )
    assert len(calls) == 2
    prose_request = calls[1]
    assert prose_request.purpose == "PROSE"
    assert prose_request.scene_functions == ["PAYOFF"]
    metadata = json.loads(Path(str(task["task_path"])).read_text(encoding="utf-8"))
    assert metadata["reference_planning_context"]["snapshot_id"] == planning_context["snapshot_id"]
    assert metadata["reference_prose_context"]["status"] == "ENABLED"
    assert metadata["reference_prose_context"]["controls"][0]["control_topic"] == "动作先于解释"
    assert "source_refs" not in metadata["reference_prose_context"]["controls"][0]
    assert "source_book_ids" not in metadata["reference_prose_context"]["controls"][0]
    input_text = Path(str(task["input_markdown"])).read_text(encoding="utf-8")
    assert "Reference Corpus Prose Controls" in input_text
    assert "只影响表达" in input_text
    assert "source_refs" not in input_text
    assert "source_book_ids" not in input_text
