from __future__ import annotations

import json
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.author_control.book_profile import (
    PROFILE_DIMENSIONS,
    ProfileEditOperation,
    ProfileStrength,
    create_book_profile_refresh_proposal,
    edit_book_profile,
    load_effective_book_profile,
    resolve_book_profile_refresh_proposal,
)
from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.author_control.service import execute_author_intent
from novel_authoring.author_control.source_state import (
    SourceChapterStateDelta,
    SourceStateCategory,
    SourceStateCoverageStatus,
    SourceStateOperation,
    SourceStateVerification,
    record_source_chapter_deltas,
    record_source_state_coverage,
)
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.edition import create_edition
from novel_authoring.ingest.service import ingest_book
from novel_authoring.planning.aggregates import build_planning_aggregate
from novel_authoring.planning.candidates import prepare_handoff_candidate_task
from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.service import (
    ProgressionContractType,
    confirm_contract,
    create_contract_proposal,
)
from novel_authoring.web.app import create_app
from novel_authoring.web.workbench import build_workbench_context
from novel_authoring.workflows.handoffs import claim_handoff


class _VisibleAuthorText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag in {"details", "script", "style"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"details", "script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth and data.strip():
            self.parts.append(data.strip())


def _visible_author_text(markup: str) -> str:
    parser = _VisibleAuthorText()
    parser.feed(markup)
    return " ".join(parser.parts)


def _state_author_text(markup: str) -> str:
    start = markup.index('<section class="wb-mode-panel wb-state-workspace"')
    end = markup.index(
        '<section class="wb-mode-panel wb-truth-workspace"', start
    )
    return _visible_author_text(markup[start:end])


def _v22_book(
    tmp_path: Path, *, chapter_count: int = 23
) -> tuple[Database, list[dict[str, object]]]:
    source = tmp_path / "source"
    source.mkdir()
    source_text = "\n\n".join(
        f"第{ordinal}章 边界{ordinal}\n\n这是第{ordinal}章的原文，只描述本章可见事实。"
        for ordinal in range(1, chapter_count + 1)
    )
    (source / "story.md").write_text(source_text, encoding="utf-8")
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="story-world-v22",
        title="Story World Workbench V2.2 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "story-world-v22" / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = [
            dict(row)
            for row in connection.execute(
                "SELECT chapter_id, ordinal, title FROM chapters "
                "WHERE book_id='story-world-v22' ORDER BY ordinal"
            ).fetchall()
        ]
        spans = {
            str(row["chapter_id"]): str(row["span_id"])
            for row in connection.execute(
                "SELECT chapter_id, MIN(span_id) AS span_id FROM source_spans "
                "WHERE book_id='story-world-v22' AND chapter_id IS NOT NULL "
                "GROUP BY chapter_id"
            ).fetchall()
        }
    character_delta = SourceChapterStateDelta(
        delta_id="v22-character-hero",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[0]["chapter_id"]),
        chapter_ordinal=1,
        category=SourceStateCategory.CHARACTER_STATE,
        operation=SourceStateOperation.ADD,
        subject_id="character:hero",
        statement="主角在第一章登场。",
        source_span_ids=[spans[str(chapters[0]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "主角", "current_location": "边界一"},
    )
    item_delta = SourceChapterStateDelta(
        delta_id="v22-item-key",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ACQUIRE,
        subject_id="character:hero",
        object_id="item:boundary-key",
        statement="主角在第二章取得边界钥匙。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={
            "name": "边界钥匙",
            "owner_id": "character:hero",
            "quantity": 1,
        },
    )
    character_update = SourceChapterStateDelta(
        delta_id="v22-character-hero-update",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.CHARACTER_STATE,
        operation=SourceStateOperation.UPDATE,
        subject_id="character:hero",
        statement="主角击败临时目标后更新经验。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "临时目标", "experience": 1},
    )
    relationship_delta = SourceChapterStateDelta(
        delta_id="v22-relationship-ally",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.RELATIONSHIP,
        operation=SourceStateOperation.RELATIONSHIP_CHANGE,
        subject_id="character:hero",
        object_id="hero-ally-cooperation",
        statement="主角与盟友建立一次有条件合作。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={
            "counterparty_id": "character:ally",
            "relationship_state": "CONDITIONAL_COOPERATION",
        },
    )
    ability_delta = SourceChapterStateDelta(
        delta_id="v22-ability-observe",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[0]["chapter_id"]),
        chapter_ordinal=1,
        category=SourceStateCategory.CAPABILITY,
        operation=SourceStateOperation.LEARN,
        subject_id="character:hero",
        object_id="capability:observe-boundary",
        statement="主角学会观察边界。",
        source_span_ids=[spans[str(chapters[0]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "观察边界", "owner_id": "character:hero"},
    )
    record_source_chapter_deltas(
        database,
        "story-world-v22",
        "base",
        [
            character_delta,
            item_delta,
            ability_delta,
            character_update,
            relationship_delta,
        ],
    )
    for chapter, status, count in (
        (chapters[0], SourceStateCoverageStatus.COMPLETE_WITH_CHANGES, 2),
        (chapters[1], SourceStateCoverageStatus.COMPLETE_WITH_CHANGES, 3),
        (chapters[2], SourceStateCoverageStatus.COMPLETE_NO_CHANGE, 0),
    ):
        record_source_state_coverage(
            database,
            book_id="story-world-v22",
            edition_id="base",
            chapter_id=str(chapter["chapter_id"]),
            chapter_ordinal=int(chapter["ordinal"]),
            status=status,
            verified_delta_count=count,
        )
    return database, chapters


def test_chapter_world_state_separates_coverage_delta_and_future_facts(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path)

    chapter_one = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[0]["chapter_id"]),
        character_id="character:hero",
    )
    chapter_two = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[1]["chapter_id"]),
        character_id="character:hero",
    )
    chapter_three = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[2]["chapter_id"]),
        character_id="character:hero",
    )

    assert chapter_one["view"] == "AFTER_CHAPTER"
    assert chapter_one["selected_character_id"] == "character:hero"
    assert chapter_one["characters"][0]["name"] == "主角"
    assert "边界钥匙" not in json.dumps(chapter_one, ensure_ascii=False)
    assert any(item["name"] == "观察边界" for item in chapter_one["abilities"])
    assert any(item["name"] == "边界钥匙" for item in chapter_two["inventory"])
    assert chapter_two["characters"][0]["name"] == "主角"
    relationship_edge = chapter_two["relationship_graph"]["edges"][0]
    assert relationship_edge["from_id"] == "character:hero"
    assert relationship_edge["to_id"] == "character:ally"
    assert relationship_edge["label"] == "hero-ally-cooperation"
    assert relationship_edge["layer"] == "SOURCE_VERIFIED"
    assert chapter_three["availability"] == "SOURCE_CHAPTER_STATE_PROJECTION"
    assert chapter_three["coverage_status"] == "COMPLETE_NO_CHANGE"
    assert chapter_three["state_changed"] is False
    assert chapter_three["chapter_delta"]["confirmed"] == []
    assert chapter_three["coverage_summary"] == {
        "total": 23,
        "analyzed": 3,
        "with_changes": 2,
        "no_changes": 1,
        "ready": 0,
        "running": 0,
        "partial": 0,
        "failed": 0,
        "not_started": 20,
        "percentage": 13.0,
    }


def test_progression_workspace_reuses_historical_world_state_without_future_leak(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    bundle = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "主角以可验证能力突破边界，并逐步打开更大的世界。",
            genre_hint="成长冒险",
            contract_prefix="story-world-v22",
        )
    )
    for contract_type, payload in (
        (ProgressionContractType.PROGRESSION, bundle.progression),
        (ProgressionContractType.WORLD_EXPANSION, bundle.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, bundle.payoff_channels),
    ):
        proposal = create_contract_proposal(
            database,
            book_id="story-world-v22",
            edition_id="base",
            contract_type=contract_type,
            payload=payload,
            source="TEST_AUTHOR_PROPOSAL",
        )
        confirm_contract(database, proposal.contract_record_id, effective_from_boundary=1)

    with database.connect() as connection:
        canon_before = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM events), (SELECT COUNT(*) FROM canon_commits)"
            ).fetchone()
        )
    chapter_one = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[0]["chapter_id"]),
        character_id="character:hero",
    )
    chapter_two = build_story_game_state(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[1]["chapter_id"]),
        character_id="character:hero",
    )
    with database.connect() as connection:
        canon_after = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM events), (SELECT COUNT(*) FROM canon_commits)"
            ).fetchone()
        )

    assert chapter_one["progression_workspace"]["available"] is True
    assert chapter_one["progression_state"]["primary_axis_state"]["current_stage"] is None
    assert chapter_one["progression_state"]["next_breakthrough_readiness"] == "UNKNOWN"
    assert "边界钥匙" not in json.dumps(chapter_one["progression_workspace"], ensure_ascii=False)
    assert "边界钥匙" in chapter_two["progression_state"]["available_resources"]
    assert chapter_one["safety"]["canon_mutation_allowed"] is False
    assert canon_after == canon_before

    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    chapter_id = str(chapters[0]["chapter_id"])
    progression = client.get(
        f"/api/books/story-world-v22/editions/base/chapters/{chapter_id}/progression"
    )
    assert progression.status_code == 200
    assert progression.json()["chapter"]["chapter_id"] == chapter_id
    assert client.get(
        "/api/books/story-world-v22/editions/base/chapters/missing/progression"
    ).status_code == 404
    page = client.get(
        "/books/story-world-v22/editions/base/workbench",
        params={"mode": "growth", "node": "growth", "chapter_id": chapter_id},
    )
    assert page.status_code == 200
    assert "Progression Workspace" in page.text
    assert "UNKNOWN" in page.text
    assert "观察边界" in page.text


def test_planning_aggregate_freezes_chapter_aware_kernel_context(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    bundle = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "主角以可验证能力突破边界，并逐步打开更大的世界。",
            genre_hint="成长冒险",
            contract_prefix="story-world-v22-freeze",
        )
    )
    payloads = {
        ProgressionContractType.READER_EXPERIENCE: bundle.reader_experience,
        ProgressionContractType.MARKET_CATEGORY: bundle.market_category,
        ProgressionContractType.NARRATIVE_DRIVE: bundle.narrative_drive,
        ProgressionContractType.GENRE: bundle.genre,
        ProgressionContractType.PROGRESSION: bundle.progression,
        ProgressionContractType.WORLD_EXPANSION: bundle.world_expansion,
        ProgressionContractType.PAYOFF_CHANNEL: bundle.payoff_channels,
    }
    for contract_type, payload in payloads.items():
        assert payload is not None
        proposal = create_contract_proposal(
            database,
            book_id="story-world-v22",
            edition_id="base",
            contract_type=contract_type,
            payload=payload,
            source="TEST_AUTHOR_PROPOSAL",
        )
        confirm_contract(database, proposal.contract_record_id, effective_from_boundary=3)

    before_boundary = build_planning_aggregate(
        database,
        "story-world-v22",
        edition_id="base",
        context_chapter_id=str(chapters[0]["chapter_id"]),
        target_chapter_ordinal=2,
    )
    before_context = before_boundary["kernel_context"]
    assert before_context is not None
    assert before_context["contract_references"] == []
    assert before_context["chapter_state"]["progression_state"] is None

    review_only = bundle.reader_experience.model_copy(
        update={"contract_id": "story-world-v22-review-only"}
    )
    create_contract_proposal(
        database,
        book_id="story-world-v22",
        edition_id="base",
        contract_type=ProgressionContractType.READER_EXPERIENCE,
        payload=review_only,
        source="TEST_REVIEW_ONLY",
    )
    aggregate = build_planning_aggregate(
        database,
        "story-world-v22",
        edition_id="base",
        context_chapter_id=str(chapters[1]["chapter_id"]),
        target_chapter_ordinal=3,
    )
    context = aggregate["kernel_context"]
    assert context is not None
    assert context["context_chapter_ordinal"] == 2
    assert context["target_chapter_ordinal"] == 3
    assert {item["contract_type"] for item in context["contract_references"]} == {
        item.value for item in ProgressionContractType
    }
    assert context["effective_contracts"]["reader_experience"]["status"] == "EFFECTIVE"
    assert context["effective_contracts"]["progression"]["status"] == "EFFECTIVE"
    assert context["chapter_state"]["progression_state"] is not None
    assert context["planning_state"]["scheduler_recommendation"]["primary_intent"]
    assert context["proposal_context"]["excluded_from_scoring"] is True
    assert any(
        item["contract_record_id"]
        for item in context["proposal_context"]["records"]
        if item["source"] == "TEST_REVIEW_ONLY"
    )
    with database.connect() as connection:
        stored = json.loads(
            str(
                connection.execute(
                    "SELECT kernel_context_json FROM planning_aggregates "
                    "WHERE aggregate_id=?",
                    (aggregate["aggregate_id"],),
                ).fetchone()[0]
            )
        )
    assert stored == context


def test_existing_novel_lexical_fallback_requires_item_by_item_confirmation(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    headers = {"X-CSRF-Token": app.state.csrf_token}
    chapter_id = str(chapters[1]["chapter_id"])
    before = client.get(
        f"/api/books/story-world-v22/editions/base/chapters/{chapter_id}/progression"
    ).json()
    with database.connect() as connection:
        authority_before = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM events), (SELECT COUNT(*) FROM canon_commits), "
                "(SELECT COUNT(*) FROM author_truths)"
            ).fetchone()
        )

    inferred = client.post(
        "/api/books/story-world-v22/editions/base/progression-contracts/lexical-fallback",
        headers=headers,
    )
    assert inferred.status_code == 200
    assert len(inferred.json()["created"]) == 7
    assert "NARRATIVE_DRIVE" in {
        item["contract_type"] for item in inferred.json()["created"]
    }
    assert {item["status"] for item in inferred.json()["created"]} == {
        "INFERRED_PROPOSAL"
    }
    assert inferred.json()["canon_changed"] is False
    assert inferred.json()["discovery_mode"] == "LEXICAL_FALLBACK"
    assert inferred.json()["confidence_boundary"] == "RECALL_HINT_ONLY"
    assert before["available"] is False
    assert client.post(
        "/api/books/story-world-v22/editions/base/progression-contracts/lexical-fallback",
        headers=headers,
    ).json()["deduplicated"] is True

    contracts = client.get(
        "/api/books/story-world-v22/editions/base/progression-contracts"
    ).json()["records"]
    progression = next(
        item for item in contracts if item["contract_type"] == "PROGRESSION"
    )
    confirmed = client.post(
        "/api/books/story-world-v22/editions/base/progression-contracts/"
        f"{progression['contract_record_id']}/confirm",
        headers=headers,
        json={"effective_from_boundary": 2, "author_notes": "仅确认成长轴"},
    )
    assert confirmed.status_code == 200
    assert confirmed.json()["record"]["status"] == "EFFECTIVE"
    after = client.get(
        f"/api/books/story-world-v22/editions/base/chapters/{chapter_id}/progression"
    ).json()
    assert after["available"] is True
    assert len(after["contract_proposals"]) == 6
    with database.connect() as connection:
        authority_after = tuple(
            connection.execute(
                "SELECT (SELECT COUNT(*) FROM events), (SELECT COUNT(*) FROM canon_commits), "
                "(SELECT COUNT(*) FROM author_truths)"
            ).fetchone()
        )
    assert authority_after == authority_before


def test_completed_zero_delta_chapter_is_not_requeued_and_batch_is_chunked(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path)
    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    endpoint = "/api/books/story-world-v22/editions/base/author-commands"
    headers = {"X-CSRF-Token": app.state.csrf_token}

    single = client.post(
        endpoint,
        headers=headers,
        json={
            "command_type": "REQUEST_SOURCE_STATE_HYDRATION",
            "chapter_id": str(chapters[2]["chapter_id"]),
        },
    )
    assert single.status_code == 200
    assert single.json()["code"] == "SOURCE_STATE_HYDRATION_ALREADY_COMPLETE"
    assert single.json()["handoff"] is None

    batch = client.post(
        endpoint,
        headers=headers,
        json={
            "command_type": "REQUEST_SOURCE_STATE_BATCH_HYDRATION",
            "payload": {"start_ordinal": 1, "end_ordinal": 23, "chunk_size": 15},
        },
    )
    assert batch.status_code == 200
    handoff = batch.json()["handoff"]
    assert [len(chunk) for chunk in handoff["chunks"]] == [15, 5]
    assert len(handoff["skipped"]) == 3
    assert all(
        entry["handoff"]["status"] == "READY_FOR_CODEX"
        for chunk in handoff["chunks"]
        for entry in chunk
    )
    first_handoff = handoff["chunks"][0][0]["handoff"]
    task_directory = Path(first_handoff["task_directory"])
    schema_path = task_directory / "input" / "output_schema.json"
    if not schema_path.is_file():
        schema_path = task_directory / "output_schema.json"
    hydration_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "SourceChapterStateDelta" in hydration_schema["$defs"]
    assert hydration_schema["properties"]["deltas"]["items"] == {
        "$ref": "#/$defs/SourceChapterStateDelta"
    }
    with database.connect() as connection:
        ready = connection.execute(
            "SELECT COUNT(*) FROM source_state_chapter_coverage "
            "WHERE book_id='story-world-v22' AND edition_id='base' "
            "AND status='READY_FOR_CODEX'"
        ).fetchone()[0]
    assert ready == 20


def test_global_book_profile_versions_are_edition_aware_and_author_controlled(
    tmp_path: Path,
) -> None:
    database, _chapters = _v22_book(tmp_path, chapter_count=3)
    base = edit_book_profile(
        database,
        "story-world-v22",
        "base",
        dimension="worldbuilding",
        operation=ProfileEditOperation.ADD,
        content="世界规则必须通过角色可见代价呈现。",
        strength=ProfileStrength.MUST,
        reason="作者确认世界观约束",
    )
    assert len(base["dimensions"]) == len(PROFILE_DIMENSIONS) == 9
    assert base["version_number"] == 1
    assert base["hard_constraints"]["must"][0]["content"].startswith("世界规则")

    create_edition(database, "story-world-v22", "revision-a", "改写 A")
    inherited = load_effective_book_profile(database, "story-world-v22", "revision-a")
    assert inherited["inherited_from_edition_id"] == "base"
    assert "世界规则必须" in next(
        item["content"]
        for item in inherited["dimensions"]
        if item["dimension"] == "worldbuilding"
    )
    edit_book_profile(
        database,
        "story-world-v22",
        "revision-a",
        dimension="style",
        operation=ProfileEditOperation.ADD,
        content="改写版采用更紧凑的短句。",
        strength=ProfileStrength.PREFER,
    )
    unchanged_base = load_effective_book_profile(database, "story-world-v22", "base")
    assert "改写版采用" not in next(
        item["content"]
        for item in unchanged_base["dimensions"]
        if item["dimension"] == "style"
    )

    proposed_baseline = deepcopy(unchanged_base["baseline"])
    proposed_baseline["themes"]["content"] = "生存选择必须留下伦理余波。"
    proposal = create_book_profile_refresh_proposal(
        database,
        "story-world-v22",
        "base",
        source_type="MAJOR_ARC_COMPLETE",
        proposed_baseline=proposed_baseline,
        summary="大弧结束后的画像刷新建议",
    )
    pending = load_effective_book_profile(database, "story-world-v22", "base")
    assert pending["version_number"] == 1
    assert pending["proposals"][0]["status"] == "PENDING"
    accepted = resolve_book_profile_refresh_proposal(
        database,
        "story-world-v22",
        "base",
        proposal["proposal_id"],
        action="ACCEPT",
    )
    assert accepted["version_number"] == 2
    assert accepted["author_edits"] == unchanged_base["author_edits"]
    assert accepted["history"][0]["reason"].startswith("接受 Profile proposal")


def test_workflow_goal_is_frozen_before_handoff_candidate_task(tmp_path: Path) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    bundle = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "主角持续变强、突破阶段，并以能力、资源和世界扩张推进故事。",
            genre_hint="成长冒险",
            contract_prefix="story-world-v22-handoff",
        )
    )
    for contract_type, payload in (
        (ProgressionContractType.READER_EXPERIENCE, bundle.reader_experience),
        (ProgressionContractType.MARKET_CATEGORY, bundle.market_category),
        (ProgressionContractType.NARRATIVE_DRIVE, bundle.narrative_drive),
        (ProgressionContractType.GENRE, bundle.genre),
        (ProgressionContractType.PROGRESSION, bundle.progression),
        (ProgressionContractType.WORLD_EXPANSION, bundle.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, bundle.payoff_channels),
    ):
        assert payload is not None
        proposal = create_contract_proposal(
            database,
            book_id="story-world-v22",
            edition_id="base",
            contract_type=contract_type,
            payload=payload,
            source="TEST_AUTHOR_PROPOSAL",
        )
        confirm_contract(database, proposal.contract_record_id, effective_from_boundary=1)
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO rhythm_diagnostic_snapshots(
                snapshot_id, book_id, edition_id, as_of_chapter, as_of_event_seq,
                projection_hash, config_hash, analyzer_versions_json, snapshot_json, created_at
            ) VALUES ('v22-rhythm', 'story-world-v22', 'base', 3, 0,
                      'projection', 'config', '{}', '{}', 'now')
            """
        )
    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    response = client.post(
        "/api/books/story-world-v22/handoffs/continuation",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={
            "edition_id": "base",
            "context_chapter_id": str(chapters[-1]["chapter_id"]),
            "requested_stage": "PLAN_ONLY",
            "author_goal": "推进钥匙线，并让资源代价可见。",
        },
    )
    assert response.status_code == 200
    handoff = response.json()
    intent_id = handoff["author_intent"]["intent_id"]
    with database.connect() as connection:
        row = connection.execute(
            "SELECT planning_aggregate_id, task_directory FROM workflow_handoffs "
            "WHERE handoff_id=?",
            (handoff["handoff_id"],),
        ).fetchone()
        assert row is not None
        aggregate = connection.execute(
            "SELECT author_policy_json FROM planning_aggregates WHERE aggregate_id=?",
            (row["planning_aggregate_id"],),
        ).fetchone()
    assert aggregate is not None
    handoff_root = Path(str(row["task_directory"]))
    handoff_kernel_path = (
        handoff_root / "input" / "kernel_context.json"
        if (handoff_root / "input").is_dir()
        else handoff_root / "kernel_context.json"
    )
    assert handoff_kernel_path.is_file()
    policy = json.loads(str(aggregate["author_policy_json"]))
    assert intent_id in {
        item["intent_id"] for item in policy["author_control"]["intents"]
    }

    claim_handoff(database, handoff["handoff_id"], "v22-test")
    prepared = prepare_handoff_candidate_task(
        database, "story-world-v22", handoff["handoff_id"]
    )
    task = json.loads(Path(str(prepared["task"])).read_text(encoding="utf-8"))
    assert task["author_goal"] == "推进钥匙线，并让资源代价可见。"
    assert intent_id in {
        item["intent_id"] for item in task["author_control"]["intents"]
    }
    assert len(task["effective_book_profile"]["dimensions"]) == 9
    assert Path(str(prepared["source_state_context"])).is_file()
    kernel_path = Path(str(prepared["kernel_context"]))
    assert kernel_path.is_file()
    kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
    assert len(kernel["contract_references"]) == 7
    assert kernel["chapter_state"]["progression_state"] is not None
    assert "resource_state" in kernel["chapter_state"]
    assert "opportunity_surface" in kernel["chapter_state"]
    assert "narrative_debts" in kernel["planning_state"]
    assert "anticipation_surface" in kernel["planning_state"]
    assert kernel["planning_state"]["scheduler_recommendation"]["primary_intent"]
    assert task["scheduler_recommendation"] == kernel["planning_state"][
        "scheduler_recommendation"
    ]


def test_v22_workbench_renders_matrix_inspector_modal_and_stable_explorer(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    app = create_app(database, book_id="story-world-v22")
    page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=knowledge&chapter_id={chapters[1]['chapter_id']}"
        "&character_id=character:hero"
    )
    assert page.status_code == 200
    assert 'data-explorer-section="world-state"' in page.text
    assert 'data-knowledge-panel="character"' in page.text
    assert 'data-knowledge-panel="topic"' in page.text
    assert 'data-knowledge-panel="matrix"' in page.text
    assert "data-build-knowledge-matrix" in page.text
    assert 'class="wb-knowledge-table"' not in page.text
    assert "谁知道什么？" in page.text
    assert "data-wb-inspector" in page.text
    assert "谁知道" in page.text
    assert "Add Item" not in page.text
    assert "按全书批量准备状态任务" not in page.text

    zero_delta_page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=overview&chapter_id={chapters[2]['chapter_id']}"
        "&character_id=character:hero"
    )
    assert zero_delta_page.status_code == 200
    assert "本章没有确认变化" in zero_delta_page.text
    assert "状态已分析" in zero_delta_page.text
    assert "章末世界状态继承上一章" in zero_delta_page.text
    assert "准备本章状态任务" not in zero_delta_page.text

    profile = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench?mode=analysis&node=worldbuilding"
    )
    assert profile.status_code == 200
    assert "全书画像 · 当前有效版本" in profile.text
    assert profile.text.count("data-profile-edit-form") == 1
    workbench_js_path = (
        Path(__file__).parents[2]
        / "src"
        / "novel_authoring"
        / "web"
        / "static"
        / "workbench.js"
    )
    workbench_js = workbench_js_path.read_text(encoding="utf-8")
    workbench_css = workbench_js_path.with_name("style.css").read_text(encoding="utf-8")
    legacy_js = workbench_js_path.with_name("app.js").read_text(encoding="utf-8")
    assert "scrollIntoView" not in workbench_js
    assert "scrollIntoView" not in legacy_js
    assert 'nextLocation.searchParams.get("state_tab")' in workbench_js
    assert "desired.centerScrollTop = 0" in workbench_js
    assert "[hidden] { display: none !important; }" in workbench_css
    assert "overflow-anchor: none" in workbench_css


def test_world_state_author_view_is_delta_first_and_raw_metadata_is_collapsed(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    app = create_app(database, book_id="story-world-v22")
    client = TestClient(app)
    page = client.get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=overview&chapter_id={chapters[1]['chapter_id']}"
        "&character_id=character:hero&truth_lens=AUTHOR&state_scope=character"
    )
    assert page.status_code == 200
    visible = _state_author_text(page.text)
    assert visible.index("这一章改变了什么？") < visible.index("人物落点")
    assert "本章变化" in visible
    assert "当前关键状态" in visible
    assert "当前世界" in visible
    assert "COMPLETE_WITH_CHANGES" not in visible
    assert "SOURCE_VERIFIED" not in visible
    assert "AFTER_CHAPTER" not in visible
    assert "Coverage + State" not in visible
    assert "chunk_size" not in visible
    assert "Projection" not in visible
    assert "COMPLETE_WITH_CHANGES" in page.text
    assert "AFTER_CHAPTER" in page.text
    assert "Story Atlas 软参考（不属于当前世界事实）" in page.text
    assert "Story Atlas" not in visible


def test_world_state_scope_and_navigation_keep_character_subview_and_lens(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    with database.connect() as connection:
        span_rows = connection.execute(
            "SELECT chapter_id, MIN(span_id) AS span_id FROM source_spans "
            "WHERE book_id='story-world-v22' GROUP BY chapter_id"
        ).fetchall()
    spans = {str(row["chapter_id"]): str(row["span_id"]) for row in span_rows}
    ally = SourceChapterStateDelta(
        delta_id="v22-character-ally",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[0]["chapter_id"]),
        chapter_ordinal=1,
        category=SourceStateCategory.CHARACTER_STATE,
        operation=SourceStateOperation.ADD,
        subject_id="character:ally",
        statement="盟友在第一章登场。",
        source_span_ids=[spans[str(chapters[0]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "盟友"},
    )
    ally_item = SourceChapterStateDelta(
        delta_id="v22-item-ally-map",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.ITEM,
        operation=SourceStateOperation.ACQUIRE,
        subject_id="character:ally",
        object_id="item:ally-map",
        statement="盟友在第二章取得路线图。",
        source_span_ids=[spans[str(chapters[1]["chapter_id"])]],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={"name": "路线图", "owner_id": "character:ally", "quantity": 1},
    )
    record_source_chapter_deltas(
        database, "story-world-v22", "base", [ally, ally_item]
    )

    common = {
        "chapter_id": str(chapters[1]["chapter_id"]),
        "character_id": "character:hero",
        "mode": "state",
        "node": "state",
        "state_tab": "inventory",
        "truth_lens": "READER",
    }
    character = build_workbench_context(
        database, "story-world-v22", "base", state_scope="character", **common
    )["story_game_state"]
    global_state = build_workbench_context(
        database, "story-world-v22", "base", state_scope="global", **common
    )["story_game_state"]
    assert character["scope_label"] == "选中人物"
    assert global_state["scope_label"] == "全局"
    assert character["visible_scope_counts"]["characters"] == 1
    assert global_state["visible_scope_counts"]["characters"] == 2
    assert character["visible_scope_counts"]["inventory"] == 1
    assert global_state["visible_scope_counts"]["inventory"] == 2

    app = create_app(database, book_id="story-world-v22")
    page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=inventory&chapter_id={chapters[1]['chapter_id']}"
        "&character_id=character:hero&truth_lens=READER&state_scope=character"
    )
    assert page.status_code == 200
    assert "主角的背包状态" in page.text
    assert "物品与装备" in page.text
    assert (
        f"state_tab=inventory&state_scope=character&truth_lens=READER&chapter_id="
        f"{chapters[0]['chapter_id']}&character_id=character:hero"
    ) in page.text
    assert (
        f"state_tab=inventory&state_scope=character&truth_lens=READER&chapter_id="
        f"{chapters[2]['chapter_id']}&character_id=character:hero"
    ) in page.text

    missing = build_workbench_context(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[0]["chapter_id"]),
        character_id="character:not-yet-present",
        mode="state",
        node="state",
        state_tab="characters",
        state_scope="character",
        truth_lens="AUTHOR",
    )["story_game_state"]
    assert missing["selected_character_id"] == "character:not-yet-present"
    assert missing["selected_character_workspace"]["state"]["available"] is False
    assert "本章暂无证据" in missing["selected_character_workspace"]["author_name"]


def test_item_faction_and_author_plan_keep_authority_boundaries(
    tmp_path: Path,
) -> None:
    database, chapters = _v22_book(tmp_path, chapter_count=3)
    with database.connect() as connection:
        span_id = str(
            connection.execute(
                "SELECT MIN(span_id) AS span_id FROM source_spans "
                "WHERE book_id='story-world-v22' AND chapter_id=?",
                (str(chapters[1]["chapter_id"]),),
            ).fetchone()["span_id"]
        )
    faction = SourceChapterStateDelta(
        delta_id="v22-faction-north-traders",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.FACTION,
        operation=SourceStateOperation.ADD,
        subject_id="faction:north-traders",
        object_id="faction:north-traders",
        statement="北境商会公开收购通行证，并在边界城组织互助交易。",
        source_span_ids=[span_id],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={
            "name": "北境商会",
            "state": "ACTIVE",
            "public_goal": "互助交易",
            "goal": "垄断运输线",
            "key_people": ["主角"],
            "controlled_locations": ["边界城"],
            "resources": ["车队", "药品"],
            "relationships": ["与守卫队合作"],
            "attitude": "谨慎合作",
            "action": "收购通行证",
            "known": ["公开收购"],
            "unknown": ["幕后资助者"],
        },
    )
    location = SourceChapterStateDelta(
        delta_id="v22-location-border-city",
        book_id="story-world-v22",
        edition_id="base",
        chapter_id=str(chapters[1]["chapter_id"]),
        chapter_ordinal=2,
        category=SourceStateCategory.LOCATION,
        operation=SourceStateOperation.ADD,
        subject_id="location:border-city",
        object_id="location:border-city",
        statement="边界城开放南门集市，主角与商会代表都在场。",
        source_span_ids=[span_id],
        confidence=1.0,
        verification_status=SourceStateVerification.SOURCE_VERIFIED,
        payload={
            "name": "边界城",
            "public_status": "南门集市开放",
            "present_characters": ["主角", "商会代表"],
            "resources": ["通行证"],
            "constraints": ["日落前关闭"],
            "related_factions": ["北境商会"],
            "recent_events": ["互助交易启动"],
            "known": ["南门开放"],
            "unknown": ["幕后资助者"],
        },
    )
    record_source_chapter_deltas(
        database, "story-world-v22", "base", [faction, location]
    )
    execute_author_intent(
        database,
        "story-world-v22",
        "base",
        intent_type="PLOT_DIRECTION",
        subject_type="FACTION",
        title="未来让北境商会封锁南门",
        target_chapter_id=str(chapters[1]["chapter_id"]),
    )
    state = build_workbench_context(
        database,
        "story-world-v22",
        "base",
        chapter_id=str(chapters[1]["chapter_id"]),
        character_id="character:hero",
        mode="state",
        node="state",
        state_tab="factions",
        state_scope="global",
        truth_lens="AUTHOR",
    )["story_game_state"]
    item = next(
        record
        for record in state["visible_inventory"]
        if record["author_name"] == "边界钥匙"
    )
    assert item["history"]
    assert item["who_knows"]
    assert item["source_span_ids"]
    faction_view = state["factions"][0]
    for key in (
        "state",
        "goal",
        "public_goal",
        "key_people",
        "controlled_locations",
        "resources",
        "relationships",
        "attitude",
        "action",
        "known",
        "unknown",
    ):
        assert faction_view[key]
    location_view = state["locations"][0]
    for key in (
        "public_status",
        "present_characters",
        "resources",
        "constraints",
        "related_factions",
        "recent_events",
        "known",
        "unknown",
    ):
        assert location_view[key]
    assert "未来让北境商会封锁南门" not in json.dumps(
        state["current_plot_status"], ensure_ascii=False
    )
    assert "未来让北境商会封锁南门" in json.dumps(
        state["author_intents"], ensure_ascii=False
    )

    app = create_app(database, book_id="story-world-v22")
    page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=factions&chapter_id={chapters[1]['chapter_id']}"
        "&character_id=character:hero&truth_lens=AUTHOR&state_scope=global"
    )
    assert page.status_code == 200
    visible = _state_author_text(page.text)
    for text in (
        "北境商会",
        "正在活动",
        "互助交易",
        "垄断运输线",
        "谨慎合作",
        "收购通行证",
        "关系 1",
    ):
        assert text in visible

    location_page = TestClient(app).get(
        "/books/story-world-v22/editions/base/workbench"
        f"?mode=state&node=state&state_tab=locations&chapter_id={chapters[1]['chapter_id']}"
        "&character_id=character:hero&truth_lens=AUTHOR&state_scope=global"
    )
    assert location_page.status_code == 200
    location_visible = _state_author_text(location_page.text)
    assert "SOURCE_VERIFIED" not in location_visible
    for text in (
        "边界城",
        "南门集市开放",
        "主角、商会代表",
        "通行证",
        "日落前关闭",
        "互助交易启动",
        "关联势力 1",
    ):
        assert text in location_visible
