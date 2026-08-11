from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from novel_authoring.author_control.book_profile import (
    PROFILE_DIMENSIONS,
    create_profile_reanalysis_handoff,
    import_profile_reanalysis_result,
    load_effective_book_profile,
    resolve_book_profile_refresh_proposal,
)
from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.author_control.reveal import (
    KnowledgeState,
    RevealTrace,
    apply_canon_reveal_trace_in_transaction,
    build_planning_truth_context,
    build_reveal_agenda,
    create_reveal_plan,
    project_truth_lens,
    set_character_truth_knowledge,
    set_reader_knowledge,
    truth_knowledge_view,
)
from novel_authoring.author_control.source_state import (
    SourceChapterStateDelta,
    SourceStateCategory,
    SourceStateCoverageStatus,
    SourceStateOperation,
    SourceStateVerification,
    record_source_chapter_deltas,
    record_source_state_coverage,
)
from novel_authoring.author_control.truth import (
    create_author_truth,
    create_secret_candidate,
    list_author_truths,
    list_open_creative_questions,
    list_secret_candidates,
    resolve_secret_candidate,
    update_author_truth,
)
from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.metrics.gates import HardGateInput
from novel_authoring.planning.candidates import _truth_reveal_failures
from novel_authoring.planning.models import CandidateProposal, CandidateScoreInputs
from novel_authoring.web.app import create_app
from novel_authoring.web.workbench import build_workbench_context

BOOK_ID = "story-truth-v23"


def _v23_book(
    tmp_path: Path, *, chapter_count: int = 50
) -> tuple[Database, list[dict[str, object]], dict[int, dict[str, str]]]:
    source = tmp_path / "source"
    source.mkdir()
    chapters_text = []
    for ordinal in range(1, chapter_count + 1):
        detail = (
            "周振国当众说自己从未加入南方商会。"
            if ordinal == 20
            else f"这是第{ordinal}章能够被读者直接看见的事实。"
        )
        chapters_text.append(f"第{ordinal}章 边界{ordinal}\n\n{detail}")
    (source / "story.md").write_text("\n\n".join(chapters_text), encoding="utf-8")
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id=BOOK_ID,
        title="Story Truth V2.3 测试书",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / BOOK_ID / "state.sqlite3")
    database.initialize()
    with database.connect() as connection:
        chapters = [
            dict(row)
            for row in connection.execute(
                "SELECT chapter_id, ordinal, title FROM chapters WHERE book_id=? "
                "ORDER BY ordinal",
                (BOOK_ID,),
            ).fetchall()
        ]
        span_rows = connection.execute(
            "SELECT c.ordinal, s.span_id, s.excerpt FROM source_spans s "
            "JOIN chapters c ON c.chapter_id=s.chapter_id WHERE s.book_id=? "
            "ORDER BY c.ordinal, s.start_line, s.span_id",
            (BOOK_ID,),
        ).fetchall()
    spans: dict[int, dict[str, str]] = {}
    for row in span_rows:
        spans.setdefault(
            int(row["ordinal"]),
            {"span_id": str(row["span_id"]), "excerpt": str(row["excerpt"])},
        )

    first_chapter_id = str(chapters[0]["chapter_id"])
    character_deltas = [
        SourceChapterStateDelta(
            delta_id="v23-character-su-mu",
            book_id=BOOK_ID,
            edition_id="base",
            chapter_id=first_chapter_id,
            chapter_ordinal=1,
            category=SourceStateCategory.CHARACTER_STATE,
            operation=SourceStateOperation.ADD,
            subject_id="character:su-mu",
            statement="苏牧在第一章登场。",
            source_span_ids=[spans[1]["span_id"]],
            confidence=1.0,
            verification_status=SourceStateVerification.SOURCE_VERIFIED,
            payload={"name": "苏牧"},
        ),
        SourceChapterStateDelta(
            delta_id="v23-character-lin-yuwei",
            book_id=BOOK_ID,
            edition_id="base",
            chapter_id=first_chapter_id,
            chapter_ordinal=1,
            category=SourceStateCategory.CHARACTER_STATE,
            operation=SourceStateOperation.ADD,
            subject_id="character:lin-yuwei",
            statement="林雨薇在第一章登场。",
            source_span_ids=[spans[1]["span_id"]],
            confidence=1.0,
            verification_status=SourceStateVerification.SOURCE_VERIFIED,
            payload={"name": "林雨薇"},
        ),
    ]
    record_source_chapter_deltas(database, BOOK_ID, "base", character_deltas)
    for chapter in chapters:
        ordinal = int(chapter["ordinal"])
        record_source_state_coverage(
            database,
            book_id=BOOK_ID,
            edition_id="base",
            chapter_id=str(chapter["chapter_id"]),
            chapter_ordinal=ordinal,
            status=(
                SourceStateCoverageStatus.COMPLETE_WITH_CHANGES
                if ordinal == 1
                else SourceStateCoverageStatus.COMPLETE_NO_CHANGE
            ),
            verified_delta_count=2 if ordinal == 1 else 0,
        )
    return database, chapters, spans


def _source_evidence(
    chapters: list[dict[str, object]],
    spans: dict[int, dict[str, str]],
    ordinal: int,
    verdict: str = "NO_CONTRADICTION",
) -> dict[str, object]:
    return {
        "verdict": verdict,
        "chapter_id": str(chapters[ordinal - 1]["chapter_id"]),
        "chapter_ordinal": ordinal,
        "source_span_id": spans[ordinal]["span_id"],
        "evidence_quote": spans[ordinal]["excerpt"],
        "explanation": "引用真实 Source span 作为兼容性审计证据。",
    }


def _candidate(
    *, agenda_bucket: str, hint: dict[str, object] | None = None, kept: bool = False
) -> CandidateProposal:
    score = CandidateScoreInputs(
        **{name: 60 for name in CandidateScoreInputs.model_fields}
    )
    return CandidateProposal.model_validate(
        {
            "local_id": "candidate-v23",
            "title": "异常交易记录",
            "summary": "周振国更重视情报收集，但本案不由旁白公开幕后答案。",
            "primary_thread_id": "thread-trade",
            "primary_function": "setup",
            "reader_question": "他为何反复核对物资编号？",
            "event_source": "冻结的 Author Truth 行为约束",
            "solution_method": "用可观察交易动作推进",
            "protagonist_strategy": "核验异常记录",
            "risk_form": "错误暴露交易意图",
            "opportunity_cost": "消耗交易窗口",
            "emotional_outcome": "不安增加",
            "social_feedback": "同伴注意到异常",
            "scene_topology": "交易站核验",
            "ending_state": "留下可追踪编号",
            "state_changes": ["交易记录出现异常"],
            "causal_sources": ["truth-v23"],
            "required_irreversible_change": "异常编号被记录",
            "required_cost": "牺牲一次交易效率",
            "commit_updates": ["推进交易情报线"],
            "pressure_before": 40,
            "pressure_target_after": 55,
            "score_inputs": score.model_dump(),
            "score_evidence": {
                name: ["结构化验收证据"] for name in CandidateScoreInputs.model_fields
            },
            "gate_input": HardGateInput(
                character_fit_inputs={"agency": 80, "consistency": 80},
                style_fit_inputs={"sentence": 80, "diction": 80},
            ).model_dump(),
            "truth_alignment": [
                {
                    "truth_id": "truth-v23",
                    "title": "隐藏情报任务",
                    "behavioral_effect": "让周振国优先收集可复用的交易信息。",
                    "respected": True,
                    "agenda_bucket": agenda_bucket,
                    "evidence": ["行为符合，但没有直接解释身份。"],
                }
            ],
            "reveal_impact": {
                "secrets_used": ["truth-v23"],
                "hints": [] if hint is None else [hint],
                "kept_hidden": ["truth-v23"] if kept else [],
            },
        }
    )


def test_candidate_can_obey_hidden_truth_but_hint_requires_a_readable_clue() -> None:
    truth = {
        "truth_id": "truth-v23",
        "title": "隐藏情报任务",
        "statement": "周振国替未公开组织收集交易情报。",
    }
    keep_frozen = {
        "active_author_truths": [truth],
        "reveal_agenda": {
            "must_reveal": [],
            "should_hint": [],
            "keep_hidden": [
                {
                    "truth_id": "truth-v23",
                    "agenda_bucket": "KEEP_HIDDEN",
                    "reveal_depth": None,
                    "plan": None,
                }
            ],
            "optional": [],
        },
    }
    assert _truth_reveal_failures(
        _candidate(agenda_bucket="KEEP_HIDDEN", kept=True), keep_frozen
    ) == []
    leaked = _candidate(
        agenda_bucket="KEEP_HIDDEN",
        hint={
            "truth_id": "truth-v23",
            "depth": "HINT",
            "clue": "旁白直接解释了幕后身份。",
            "target": "READER",
        },
    )
    assert any(
        "KEEP_HIDDEN" in failure
        for failure in _truth_reveal_failures(leaked, keep_frozen)
    )

    hint_frozen = {
        "active_author_truths": [truth],
        "reveal_agenda": {
            "must_reveal": [],
            "should_hint": [
                {
                    "truth_id": "truth-v23",
                    "agenda_bucket": "SHOULD_HINT",
                    "reveal_depth": "HINT",
                    "plan": {"target": "READER", "target_entity_id": None},
                }
            ],
            "keep_hidden": [],
            "optional": [],
        },
    }
    readable_hint = {
        "truth_id": "truth-v23",
        "depth": "HINT",
        "clue": "交易时，他异常记录了某种物资的编号。",
        "target": "READER",
        "reader_knowledge_delta": "UNKNOWN -> HINTED",
    }
    assert _truth_reveal_failures(
        _candidate(agenda_bucket="SHOULD_HINT", hint=readable_hint), hint_frozen
    ) == []
    missing_clue = {**readable_hint, "clue": ""}
    assert any(
        "缺少可读线索" in failure
        for failure in _truth_reveal_failures(
            _candidate(agenda_bucket="SHOULD_HINT", hint=missing_clue), hint_frozen
        )
    )


def _manual_hidden_truth(
    database: Database,
    chapters: list[dict[str, object]],
    spans: dict[int, dict[str, str]],
) -> dict[str, object]:
    return create_author_truth(
        database,
        BOOK_ID,
        "base",
        {
            "truth_type": "CHARACTER_SECRET",
            "subject_type": "CHARACTER",
            "subject_id": "character:zhou-zhenguo",
            "title": "周振国的隐藏情报任务",
            "statement": "测试：周振国正在替一个尚未公开的组织收集交易情报。",
            "status": "ACTIVE_TRUTH",
            "introduced_by": "AUTHOR_MANUAL",
            "effective_from_chapter": 30,
            "compatibility_evidence": [_source_evidence(chapters, spans, 30)],
        },
    )


def test_retroactive_truth_plans_and_knowledge_are_five_separate_layers(
    tmp_path: Path,
) -> None:
    database, chapters, spans = _v23_book(tmp_path)
    with database.connect() as connection:
        source_span_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM source_spans WHERE book_id=?", (BOOK_ID,)
            ).fetchone()[0]
        )
        canon_event_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM events WHERE book_id=?", (BOOK_ID,)
            ).fetchone()[0]
        )

    truth = _manual_hidden_truth(database, chapters, spans)
    truth_id = str(truth["truth_id"])
    assert truth["status"] == "ACTIVE_TRUTH"
    assert truth["compatibility_status"] == "COMPATIBLE"
    assert truth["retroactive_scope"] == "RETROACTIVE_HIDDEN_COMPATIBLE"

    hint_plan = create_reveal_plan(
        database,
        BOOK_ID,
        "base",
        {
            "truth_id": truth_id,
            "target": "READER",
            "strategy": "交易时异常记录某种物资，但不确认组织身份。",
            "target_chapter_min": 51,
            "target_chapter_max": 55,
            "horizon": "SHORT",
            "status": "ACTIVE",
            "reveal_depth": "HINT",
        },
    )
    full_plan = create_reveal_plan(
        database,
        BOOK_ID,
        "base",
        {
            "truth_id": truth_id,
            "target": "READER",
            "strategy": "在长期窗口完整公开组织身份。",
            "target_chapter_min": 70,
            "horizon": "LONG",
            "status": "ACTIVE",
            "reveal_depth": "FULL_REVEAL",
        },
    )
    assert hint_plan["reveal_plan_id"] != full_plan["reveal_plan_id"]
    assert build_reveal_agenda(database, BOOK_ID, "base", 50)["keep_hidden"][0][
        "truth_id"
    ] == truth_id
    assert build_reveal_agenda(database, BOOK_ID, "base", 51)["should_hint"][0][
        "truth_id"
    ] == truth_id
    assert build_reveal_agenda(database, BOOK_ID, "base", 60)["keep_hidden"][0][
        "truth_id"
    ] == truth_id
    assert build_reveal_agenda(database, BOOK_ID, "base", 70)["must_reveal"][0][
        "truth_id"
    ] == truth_id

    knowledge_before = truth_knowledge_view(
        database, BOOK_ID, "base", chapter_ordinal=50, truth_id=truth_id
    )["topics"][0]
    assert knowledge_before["author_state"] == "KNOWN"
    assert knowledge_before["reader"]["state"] == "UNKNOWN"
    assert knowledge_before["characters"] == []
    planning = build_planning_truth_context(
        database, BOOK_ID, "base", chapter_ordinal=51
    )
    assert truth_id in {
        item["truth_id"] for item in planning["active_author_truths"]
    }
    assert planning["reveal_agenda"]["should_hint"][0]["can_reveal"] is True

    provisional = set_reader_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        state=KnowledgeState.HINTED,
        chapter_ordinal=50,
        mode="AUTHOR_PLANNING",
    )
    assert provisional["provisional"] is True
    assert project_truth_lens(
        database,
        BOOK_ID,
        "base",
        chapter_ordinal=50,
        lens="READER",
    )["topics"] == []

    visible_evidence = [
        {
            "source_span_id": spans[50]["span_id"],
            "quote": spans[50]["excerpt"],
        }
    ]
    set_reader_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        state="HINTED",
        chapter_ordinal=50,
        evidence=visible_evidence,
        mode="SOURCE_EVIDENCE",
    )
    set_character_truth_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        "character:lin-yuwei",
        state="SUSPECTED",
        chapter_ordinal=50,
        evidence=visible_evidence,
        mode="SOURCE_EVIDENCE",
    )
    separated = truth_knowledge_view(
        database, BOOK_ID, "base", chapter_ordinal=50, truth_id=truth_id
    )["topics"][0]
    assert separated["reader"]["state"] == "HINTED"
    assert separated["characters"][0]["character_id"] == "character:lin-yuwei"
    assert separated["characters"][0]["state"] == "SUSPECTED"

    reader_projection = project_truth_lens(
        database, BOOK_ID, "base", chapter_ordinal=50, lens="READER"
    )
    assert reader_projection["topics"][0]["truth"]["redacted"] is True
    assert truth["statement"] not in json.dumps(
        reader_projection, ensure_ascii=False
    )
    character_projection = project_truth_lens(
        database,
        BOOK_ID,
        "base",
        chapter_ordinal=50,
        lens="CHARACTER",
        character_id="character:lin-yuwei",
    )
    assert character_projection["topics"][0]["projection_state"] == "SUSPECTED"
    assert character_projection["topics"][0]["characters"] == [
        separated["characters"][0]
    ]
    assert project_truth_lens(
        database,
        BOOK_ID,
        "base",
        chapter_ordinal=50,
        lens="CHARACTER",
        character_id="character:su-mu",
    )["topics"] == []

    conflict = create_author_truth(
        database,
        BOOK_ID,
        "base",
        {
            "truth_type": "FACTION_RELATIONSHIP",
            "subject_type": "CHARACTER",
            "subject_id": "character:zhou-zhenguo",
            "title": "与第20章明确冲突的加入记录",
            "statement": "周振国在第20章之前已经公开加入南方商会。",
            "status": "ACTIVE_TRUTH",
            "effective_from_chapter": 20,
            "compatibility_evidence": [
                _source_evidence(chapters, spans, 20, "CONTRADICTION")
            ],
        },
    )
    assert conflict["status"] == "CONFLICTING"
    assert conflict["compatibility_status"] == "CONFLICTING"
    assert conflict["requires_revision"] is True
    assert conflict["truth_id"] not in {
        item["truth_id"]
        for item in build_planning_truth_context(
            database, BOOK_ID, "base", chapter_ordinal=51
        )["active_author_truths"]
    }

    compatible = create_author_truth(
        database,
        BOOK_ID,
        "base",
        {
            "truth_type": "MOTIVE",
            "subject_type": "CHARACTER",
            "subject_id": "character:lin-yuwei",
            "title": "后期加入但不改旧章的动机",
            "statement": "林雨薇从第20章起暗中保护某条补给路线。",
            "status": "ACTIVE_TRUTH",
            "effective_from_chapter": 20,
            "compatibility_evidence": [_source_evidence(chapters, spans, 20)],
        },
    )
    assert compatible["status"] == "ACTIVE_TRUTH"
    assert compatible["retroactive_scope"] == "RETROACTIVE_HIDDEN_COMPATIBLE"

    with database.connect() as connection:
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM source_spans WHERE book_id=?", (BOOK_ID,)
            ).fetchone()[0]
            == source_span_count
        )
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM events WHERE book_id=?", (BOOK_ID,)
            ).fetchone()[0]
            == canon_event_count
        )


def test_only_canon_reveal_trace_advances_durable_knowledge_and_keeps_history(
    tmp_path: Path,
) -> None:
    database, chapters, _spans = _v23_book(tmp_path, chapter_count=3)
    truth = create_author_truth(
        database,
        BOOK_ID,
        "base",
        {
            "truth_type": "WORLD_RULE_SECRET",
            "subject_type": "WORLD_RULE",
            "title": "隐藏规则",
            "statement": "边界会记录每一次未公开的交易。",
            "status": "ACTIVE_TRUTH",
            "effective_from_chapter": 3,
        },
    )
    truth_id = str(truth["truth_id"])
    chapter_id = str(chapters[-1]["chapter_id"])
    with database.connect() as connection:
        canon_before = int(
            connection.execute(
                "SELECT COUNT(*) FROM events WHERE book_id=?", (BOOK_ID,)
            ).fetchone()[0]
        )
        apply_canon_reveal_trace_in_transaction(
            connection,
            book_id=BOOK_ID,
            edition_id="base",
            chapter_id=chapter_id,
            chapter_ordinal=3,
            draft_id="draft-v23-hint",
            commit_id="commit-v23-hint",
            reveal_trace=RevealTrace.model_validate(
                {
                    "planned": [
                        {"truth_id": truth_id, "agenda_bucket": "SHOULD_HINT", "depth": "HINT"}
                    ],
                    "realized": [
                        {
                            "truth_id": truth_id,
                            "target": "READER",
                            "depth": "HINT",
                            "evidence_quote": "边界表面浮出一笔无法解释的交易编号。",
                            "expected_knowledge_change": "HINTED",
                        }
                    ],
                    "knowledge_transitions": [
                        {
                            "truth_id": truth_id,
                            "target": "READER",
                            "before": "UNKNOWN",
                            "after": "HINTED",
                        }
                    ],
                }
            ),
            approved_character_knowledge=set(),
        )
    assert truth_knowledge_view(
        database, BOOK_ID, "base", chapter_ordinal=3, truth_id=truth_id
    )["topics"][0]["reader"]["state"] == "HINTED"

    with database.connect() as connection:
        apply_canon_reveal_trace_in_transaction(
            connection,
            book_id=BOOK_ID,
            edition_id="base",
            chapter_id=chapter_id,
            chapter_ordinal=3,
            draft_id="draft-v23-strong-hint",
            commit_id="commit-v23-strong-hint",
            reveal_trace=RevealTrace.model_validate(
                {
                    "planned": [
                        {
                            "truth_id": truth_id,
                            "agenda_bucket": "SHOULD_HINT",
                            "depth": "STRONG_HINT",
                        }
                    ],
                    "realized": [
                        {
                            "truth_id": truth_id,
                            "target": "READER",
                            "depth": "STRONG_HINT",
                            "evidence_quote": "编号与此前三次秘密交易完全相同。",
                            "expected_knowledge_change": "SUSPECTED",
                        }
                    ],
                    "knowledge_transitions": [
                        {
                            "truth_id": truth_id,
                            "target": "READER",
                            "before": "HINTED",
                            "after": "SUSPECTED",
                        }
                    ],
                }
            ),
            approved_character_knowledge=set(),
        )
        edges = connection.execute(
            "SELECT edge_id, state, supersedes_edge_id FROM reader_knowledge_edges "
            "WHERE truth_id=? ORDER BY created_at, edge_id",
            (truth_id,),
        ).fetchall()
        assert len(edges) == 2
        assert {str(row["state"]) for row in edges} == {"HINTED", "SUSPECTED"}
        suspected = next(row for row in edges if row["state"] == "SUSPECTED")
        hinted = next(row for row in edges if row["state"] == "HINTED")
        assert suspected["supersedes_edge_id"] == hinted["edge_id"]
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM reveal_events WHERE truth_id=?", (truth_id,)
            ).fetchone()[0]
            == 2
        )
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM events WHERE book_id=?", (BOOK_ID,)
            ).fetchone()[0]
            == canon_before
        )
    assert truth_knowledge_view(
        database, BOOK_ID, "base", chapter_ordinal=3, truth_id=truth_id
    )["topics"][0]["reader"]["state"] == "SUSPECTED"


def _profile_result(
    handoff_id: str, *, changed_dimension: str | None, suffix: str
) -> dict[str, object]:
    return {
        "handoff_id": handoff_id,
        "handoff_type": "PROFILE_REANALYSIS",
        "status": "COMPLETED",
        "book_id": BOOK_ID,
        "edition_id": "base",
        "dimensions": [
            {
                "dimension": dimension,
                "additions": (
                    [f"{label}新增可审计约束：{suffix}"]
                    if dimension == changed_dimension
                    else []
                ),
                "modifications": [],
                "removals": [],
                "reason": f"复核九维中的{label}",
                "evidence": [f"冻结 Profile context · {filename}"],
                "confidence": 0.8,
            }
            for dimension, label, filename in PROFILE_DIMENSIONS
        ],
        "summary": "九维 Profile 已基于冻结上下文重新分析。",
        "canon_committed": False,
        "edition_activated": False,
    }


def test_profile_reanalysis_is_a_real_handoff_and_requires_a_changed_proposal(
    tmp_path: Path,
) -> None:
    database, chapters, _spans = _v23_book(tmp_path, chapter_count=3)
    before = load_effective_book_profile(database, BOOK_ID, "base")
    first = create_profile_reanalysis_handoff(
        database,
        BOOK_ID,
        "base",
        context_chapter_id=str(chapters[-1]["chapter_id"]),
    )
    assert first["status"] == "READY_FOR_CODEX"
    assert first["analysis_status"] == "HANDOFF_READY"
    task_directory = Path(str(first["task_directory"]))
    profile_context = task_directory / "input" / "profile_context.json"
    if not profile_context.is_file():
        profile_context = task_directory / "profile_context.json"
    assert profile_context.is_file()
    frozen = json.loads(profile_context.read_text(encoding="utf-8"))
    assert frozen["effective_profile"]["version_number"] == before["version_number"]
    assert "profile_history" in frozen

    with pytest.raises(ValueError, match="完全相同"):
        import_profile_reanalysis_result(
            database,
            str(first["handoff_id"]),
            _profile_result(
                str(first["handoff_id"]), changed_dimension=None, suffix="无变化"
            ),
        )
    first_proposal = import_profile_reanalysis_result(
        database,
        str(first["handoff_id"]),
        _profile_result(
            str(first["handoff_id"]), changed_dimension="themes", suffix="第一次"
        ),
    )
    rejected = resolve_book_profile_refresh_proposal(
        database,
        BOOK_ID,
        "base",
        str(first_proposal["proposal_id"]),
        action="REJECT",
    )
    assert rejected["version_number"] == before["version_number"]
    assert rejected["baseline"] == before["baseline"]

    second = create_profile_reanalysis_handoff(
        database,
        BOOK_ID,
        "base",
        context_chapter_id=str(chapters[-1]["chapter_id"]),
    )
    second_proposal = import_profile_reanalysis_result(
        database,
        str(second["handoff_id"]),
        _profile_result(
            str(second["handoff_id"]), changed_dimension="style", suffix="第二次"
        ),
    )
    accepted = resolve_book_profile_refresh_proposal(
        database,
        BOOK_ID,
        "base",
        str(second_proposal["proposal_id"]),
        action="ACCEPT",
    )
    assert accepted["version_number"] == before["version_number"] + 1
    assert "第二次" in accepted["baseline"]["style"]["content"]


def test_secret_candidate_stays_soft_and_truth_edits_recheck_old_evidence(
    tmp_path: Path,
) -> None:
    database, chapters, spans = _v23_book(tmp_path, chapter_count=3)
    candidate = create_secret_candidate(
        database,
        BOOK_ID,
        "base",
        title="可能存在的幕后组织",
        statement="周振国可能在替某个组织工作。",
        truth_type="CHARACTER_SECRET",
        subject_type="CHARACTER",
        subject_id="character:zhou-zhenguo",
        evidence=[{"source_span_id": spans[3]["span_id"]}],
        confidence=0.6,
    )
    assert candidate["planning_role"] == "SOFT_POSSIBILITY_ONLY"
    assert list_author_truths(database, BOOK_ID, "base") == []
    assert list_secret_candidates(database, BOOK_ID, "base")[0]["status"] == (
        "INFERRED_SECRET_CANDIDATE"
    )
    kept_open = resolve_secret_candidate(
        database,
        BOOK_ID,
        "base",
        str(candidate["candidate_id"]),
        action="KEEP_OPEN",
    )
    assert kept_open["truth"] is None
    assert kept_open["open_question"]["status"] == "OPEN_QUESTION"
    assert list_author_truths(database, BOOK_ID, "base") == []
    assert list_open_creative_questions(database, BOOK_ID, "base")[0]["status"] == (
        "OPEN_QUESTION"
    )

    second = create_secret_candidate(
        database,
        BOOK_ID,
        "base",
        title="作者待确认动机",
        statement="林雨薇暗中保护补给路线。",
        truth_type="MOTIVE",
        subject_type="CHARACTER",
        subject_id="character:lin-yuwei",
        confidence=0.8,
    )
    confirmed = resolve_secret_candidate(
        database,
        BOOK_ID,
        "base",
        str(second["candidate_id"]),
        action="CONFIRM_TRUTH",
        effective_from_chapter=3,
    )
    assert confirmed["truth"]["status"] == "ACTIVE_TRUTH"
    assert confirmed["truth"]["introduced_by"] == "AUTHOR_CONFIRMED"

    retroactive = create_author_truth(
        database,
        BOOK_ID,
        "base",
        {
            "truth_type": "PLOT_TRUTH",
            "subject_type": "PLOT",
            "title": "有证据的旧陈述",
            "statement": "第一章起存在一条未公开补给线。",
            "status": "ACTIVE_TRUTH",
            "effective_from_chapter": 1,
            "compatibility_evidence": [_source_evidence(chapters, spans, 1)],
        },
    )
    edited = update_author_truth(
        database,
        BOOK_ID,
        "base",
        str(retroactive["truth_id"]),
        {"statement": "第一章起存在两条未公开补给线。"},
    )
    assert edited["status"] == "PROVISIONAL_TRUTH"
    assert edited["compatibility_status"] == "UNKNOWN"
    assert edited["compatibility_evidence"][0]["active"] is False
    retired = update_author_truth(
        database,
        BOOK_ID,
        "base",
        str(retroactive["truth_id"]),
        {"status": "RETIRED"},
    )
    assert retired["status"] == "RETIRED"


def test_workbench_uses_one_chapter_anchor_redacts_lenses_and_hidden_item_is_not_owned(
    tmp_path: Path,
) -> None:
    database, chapters, spans = _v23_book(tmp_path, chapter_count=30)
    truth = _manual_hidden_truth(database, chapters, spans)
    truth_id = str(truth["truth_id"])
    evidence = [{"source_span_id": spans[30]["span_id"], "quote": spans[30]["excerpt"]}]
    set_reader_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        state="HINTED",
        chapter_ordinal=30,
        evidence=evidence,
        mode="SOURCE_EVIDENCE",
    )
    set_character_truth_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        "character:lin-yuwei",
        state="SUSPECTED",
        chapter_ordinal=30,
        evidence=evidence,
        mode="SOURCE_EVIDENCE",
    )
    future_truth = create_author_truth(
        database,
        BOOK_ID,
        "base",
        {
            "truth_type": "PLOT_TRUTH",
            "subject_type": "PLOT",
            "title": "第31章才生效的未来设定",
            "statement": "这条设定在第30章视图中默认不可见。",
            "status": "ACTIVE_TRUTH",
            "effective_from_chapter": 31,
        },
    )
    chapter_30_id = str(chapters[29]["chapter_id"])
    context = build_workbench_context(
        database,
        BOOK_ID,
        "base",
        chapter_id=chapter_30_id,
        mode="truth",
        node="truth",
        truth_lens="AUTHOR",
    )
    assert context["chapter_world_state"] is context["story_game_state"]
    assert context["chapter_world_state"]["chapter"]["ordinal"] == 30
    assert context["previous_chapter_world_state"]["chapter"]["ordinal"] == 29
    topic = next(
        item
        for item in context["truth_projection"]["topics"]
        if item["truth"]["truth_id"] == truth_id
    )
    assert topic["compatibility_evidence"][0]["source_span_id"] == spans[30]["span_id"]
    matrix = {item["character_id"]: item["state"] for item in topic["character_matrix"]}
    assert matrix == {
        "character:lin-yuwei": "SUSPECTED",
        "character:su-mu": "UNKNOWN",
    }

    app = create_app(database, book_id=BOOK_ID)
    client = TestClient(app)
    author_page = client.get(
        f"/books/{BOOK_ID}/editions/base/workbench?mode=truth&node=truth"
        f"&truth_lens=AUTHOR&chapter_id={chapter_30_id}"
    )
    assert author_page.status_code == 200
    assert str(truth["statement"]) in author_page.text
    assert "Author Truth" in author_page.text
    assert "Reader" in author_page.text
    assert "林雨薇" in author_page.text and "SUSPECTED" in author_page.text
    assert "苏牧" in author_page.text and "UNKNOWN" in author_page.text
    assert str(future_truth["statement"]) not in author_page.text
    assert "显示未来设定" in author_page.text
    assert "公开世界状态索引 · 与隐藏真相一起搜索" in author_page.text
    assert 'name="compatibility_verdict"' in author_page.text
    assert 'name="compatibility_source_span_id"' in author_page.text
    assert 'data-secret-horizon-filter="SHORT"' in author_page.text
    assert 'data-secret-board' in author_page.text
    assert 'draggable="true"' in author_page.text

    future_page = client.get(
        f"/books/{BOOK_ID}/editions/base/workbench?mode=truth&node=truth"
        f"&truth_lens=AUTHOR&include_future_truths=1&chapter_id={chapter_30_id}"
    )
    assert future_page.status_code == 200
    assert str(future_truth["statement"]) in future_page.text
    assert "不属于当前 ChapterWorldState" in future_page.text

    truth_board_page = client.get(
        f"/books/{BOOK_ID}/editions/base/workbench?mode=truth&node=truth-board"
        f"&truth_lens=AUTHOR&chapter_id={chapter_30_id}"
    )
    assert truth_board_page.status_code == 200
    assert "Truth Board · 按对象" in truth_board_page.text
    for label in ("人物", "关系", "势力", "地点", "世界规则", "剧情"):
        assert f"<h3>{label}</h3>" in truth_board_page.text

    reader_page = client.get(
        f"/books/{BOOK_ID}/editions/base/workbench?mode=truth&node=truth"
        f"&truth_lens=READER&chapter_id={chapter_30_id}"
    )
    assert reader_page.status_code == 200
    assert str(truth["statement"]) not in reader_page.text
    assert "读者已接触的未确认主题" in reader_page.text
    assert "未揭露答案、其他角色知识和作者 RevealPlan 不会发送" in reader_page.text

    chapter_10_id = str(chapters[9]["chapter_id"])
    navigation_page = client.get(
        f"/books/{BOOK_ID}/editions/base/workbench?mode=state&node=state"
        f"&state_tab=inventory&chapter_id={chapter_10_id}"
    )
    assert navigation_page.status_code == 200
    assert f'data-current-chapter-id="{chapter_10_id}"' in navigation_page.text
    assert "state_tab=inventory&state_scope=character&truth_lens=AUTHOR" in navigation_page.text
    assert f"chapter_id={chapter_10_id}" in navigation_page.text
    assert f"mode=analysis&chapter_id={chapter_10_id}" in navigation_page.text
    assert f"mode=continuity&node=chapter&chapter_id={chapter_10_id}" in navigation_page.text
    assert "author_control_trace" not in navigation_page.text
    assert "profile_alignment JSON" not in navigation_page.text
    assert "第10章结束时" in navigation_page.text
    assert "苏牧" in navigation_page.text
    assert "的背包状态" in navigation_page.text
    assert "选择一个世界状态对象" in navigation_page.text

    continuity_page = client.get(
        f"/books/{BOOK_ID}/editions/base/workbench?mode=continuity&node=chapter"
        f"&right_tab=state&chapter_id={chapter_30_id}"
    )
    assert continuity_page.status_code == 200
    assert "WorldState@N-1" in continuity_page.text
    assert "Delta@N" in continuity_page.text
    assert "WorldState@N" in continuity_page.text
    assert "打开完整世界状态" in continuity_page.text
    for label in ("人物", "背包", "装备", "能力", "知识", "关系", "势力", "地点", "规则", "Delta"):
        assert label in continuity_page.text

    inventory_before = build_story_game_state(
        database, BOOK_ID, "base", chapter_id=chapter_30_id
    )["inventory"]
    response = client.post(
        f"/api/books/{BOOK_ID}/editions/base/hidden-items",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={
            "name": "地下钥匙",
            "description": "位于地下，但无人持有、无人知晓。",
            "effective_from_chapter": 30,
            "location_id": "location:underground",
            "owner_id": "character:su-mu",
            "target_chapter_min": 31,
            "target_chapter_max": 35,
            "reveal_depth": "HINT",
        },
    )
    assert response.status_code == 200
    assert response.json()["world_state_changed"] is False
    assert response.json()["knowledge_changed"] is False
    hidden_truth = response.json()["truth"]
    assert hidden_truth["truth_type"] == "ITEM_SECRET"
    assert hidden_truth["metadata"]["ownership_layer"] == "SEPARATE_FROM_EXISTENCE"
    inventory_after = build_story_game_state(
        database, BOOK_ID, "base", chapter_id=chapter_30_id
    )["inventory"]
    assert inventory_after == inventory_before

    with database.connect() as connection:
        truth_count_before = int(
            connection.execute(
                "SELECT COUNT(*) FROM author_truths WHERE book_id=? AND edition_id=?",
                (BOOK_ID, "base"),
            ).fetchone()[0]
        )
    invalid_window = client.post(
        f"/api/books/{BOOK_ID}/editions/base/hidden-items",
        headers={"X-CSRF-Token": app.state.csrf_token},
        json={
            "name": "非法揭示窗口物品",
            "effective_from_chapter": 30,
            "target_chapter_min": 40,
            "target_chapter_max": 35,
        },
    )
    assert invalid_window.status_code == 422
    with database.connect() as connection:
        truth_count_after = int(
            connection.execute(
                "SELECT COUNT(*) FROM author_truths WHERE book_id=? AND edition_id=?",
                (BOOK_ID, "base"),
            ).fetchone()[0]
        )
    assert truth_count_after == truth_count_before


def test_world_state_lenses_are_chapter_aware_and_read_only(tmp_path: Path) -> None:
    database, chapters, spans = _v23_book(tmp_path, chapter_count=30)
    truth = _manual_hidden_truth(database, chapters, spans)
    truth_id = str(truth["truth_id"])
    evidence = [{"source_span_id": spans[30]["span_id"], "quote": spans[30]["excerpt"]}]
    set_reader_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        state="HINTED",
        chapter_ordinal=30,
        evidence=evidence,
        mode="SOURCE_EVIDENCE",
    )
    set_character_truth_knowledge(
        database,
        BOOK_ID,
        "base",
        truth_id,
        "character:lin-yuwei",
        state="SUSPECTED",
        chapter_ordinal=30,
        evidence=evidence,
        mode="SOURCE_EVIDENCE",
    )
    chapter_id = str(chapters[29]["chapter_id"])
    with database.connect() as connection:
        before = "\n".join(connection.iterdump())

    projections: dict[str, dict[str, object]] = {}
    for lens in ("AUTHOR", "READER", "CHARACTER"):
        projections[lens] = build_workbench_context(
            database,
            BOOK_ID,
            "base",
            chapter_id=chapter_id,
            character_id="character:lin-yuwei",
            mode="state",
            node="state",
            state_tab="overview",
            state_scope="character",
            truth_lens=lens,
        )["story_game_state"]
    with database.connect() as connection:
        after = "\n".join(connection.iterdump())

    assert before == after
    assert projections["AUTHOR"]["lens"]["value"] == "AUTHOR"
    assert projections["READER"]["lens"]["value"] == "READER"
    assert projections["CHARACTER"]["lens"]["value"] == "CHARACTER"
    author_topic = next(
        item
        for item in projections["AUTHOR"]["lens"]["topics"]
        if item["truth"]["truth_id"] == truth_id
    )
    reader_topic = next(
        item
        for item in projections["READER"]["lens"]["topics"]
        if item["truth"]["truth_id"] == truth_id
    )
    character_topic = next(
        item
        for item in projections["CHARACTER"]["lens"]["topics"]
        if item["truth"]["truth_id"] == truth_id
    )
    assert author_topic["truth"]["statement"] == truth["statement"]
    assert reader_topic["truth"].get("statement") != truth["statement"]
    assert character_topic["truth"].get("statement") != truth["statement"]
    assert reader_topic["reader"]["state_label"] == "读者已有暗示"

    app = create_app(database, book_id=BOOK_ID)
    client = TestClient(app)
    pages = {
        lens: client.get(
            f"/books/{BOOK_ID}/editions/base/workbench?mode=state&node=state"
            f"&state_tab=overview&state_scope=character&truth_lens={lens}"
            f"&chapter_id={chapter_id}&character_id=character:lin-yuwei"
        )
        for lens in ("AUTHOR", "READER", "CHARACTER")
    }
    assert all(page.status_code == 200 for page in pages.values())
    assert str(truth["statement"]) in pages["AUTHOR"].text
    assert str(truth["statement"]) not in pages["READER"].text
    assert str(truth["statement"]) not in pages["CHARACTER"].text
