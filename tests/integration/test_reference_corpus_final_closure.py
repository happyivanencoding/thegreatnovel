"""FINAL REFERENCE CORPUS CLOSURE integration evidence.

The Corpus in this module is deliberately disposable.  It is written below
``tmp_path`` and is never imported as production Corpus, Canon, or author
intent.  The tests exercise the public query/context and authoring workflow
seams so the final closure can distinguish a real integration proof from a
private-helper unit test.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.edition import create_edition
from novel_authoring.ingest.service import ingest_book
from novel_authoring.metrics.engine import MetricInputBundle, diagnose_bundle, persist_results
from novel_authoring.original.models import (
    OriginalCreativeSemantics,
    OriginalReaderKernelProposal,
)
from novel_authoring.original.service import (
    confirm_original_reader_experience,
    create_original_book,
    import_original_reader_kernel_proposal,
    prepare_original_core_innovation,
)
from novel_authoring.planning.candidates import prepare_candidate_task
from novel_authoring.progression.interpretation import (
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.reference_corpus.context import (
    ReferenceContextIntegrityError,
    freeze_reference_context,
    load_reference_context_snapshot,
)
from novel_authoring.reference_corpus.query import (
    ReferenceCorpusQueryRequest,
    query_reference_corpus,
    reference_corpus_runtime_diagnostic,
)
from novel_authoring.reference_corpus.semantic import (
    MACHINE_PACKAGE_VERSION,
    compute_machine_bundle_hash,
)
from novel_authoring.revision import (
    build_revision_impact,
    build_revision_plan,
    complete_revision_impact_audit,
    create_revision_campaign,
    import_revision_strategy_selection,
    prepare_revision_draft_task,
)
from novel_authoring.storage.layout import BookLayout
from novel_authoring.utils import json_dumps, utc_now
from novel_authoring.workflows.handoffs import (
    HandoffStatus,
    claim_handoff,
    get_handoff,
    update_handoff_status,
)

MACHINE_BOOKS = ["book-a", "book-b", "book-c", "book-d"]
MACHINE_CATEGORIES = ["玄幻", "都市", "科幻"]
PLANNING_TAGS = [
    "resource-pressure",
    "breakthrough",
    "power-verification",
    "resource-release",
    "world-expansion",
    "exploration",
    "mystery-reveal",
    "relationship",
    "long-form",
    "post-payoff-anticipation",
    "fatigue",
]
FORBIDDEN_EXECUTOR_FIELDS = {
    "source_refs",
    "source_book_ids",
    "raw",
    "full_dna",
    "book_dna",
    "prose_dna",
    "source_prose",
    "source_content",
    "full_text",
    "raw_text",
}


def _evidence(book_id: str, index: int) -> dict[str, object]:
    return {
        "evidence_id": f"evidence-{book_id}-{index}",
        "source_book_id": book_id,
        "source_id": f"source-{book_id}",
        "distill_id": f"distill-{book_id}",
        "segment_id": "segment-0001",
        "line_start": index,
        "line_end": index + 2,
        "observation_summary": "仅记录抽象动作与可追溯定位，不保存来源正文。",
    }


def _common_card(
    card_id: str,
    card_type: str,
    primary_book: str,
    *,
    tags: list[str] | None = None,
) -> dict[str, object]:
    source_books = [primary_book, *[book for book in MACHINE_BOOKS if book != primary_book]]
    return {
        "schema_version": "reference-corpus-card-v1",
        "card_id": card_id,
        "card_type": card_type,
        "knowledge_level": (
            "CORPUS_SYNTHESIS" if card_type == "corpus-synthesis" else "CROSS_BOOK_CONTRAST"
        ),
        "status": "REFERENCE_ONLY",
        "source_book_ids": source_books,
        "evidence_refs": [_evidence(book, index) for index, book in enumerate(source_books, 1)],
        "creative_problem_tags": list(tags or PLANNING_TAGS),
        "reader_experiences": ["BREAKTHROUGH", "RESOURCE_OPPORTUNITY"],
        "narrative_drives": ["POWER_PROGRESSION", "SURVIVAL_RESOURCE"],
        "payoff_channels": ["POWER_BREAKTHROUGH", "RESOURCE_GAIN"],
        "evidence_scope": "MULTI_CATEGORY",
        "maturity": "BROAD" if card_type == "corpus-synthesis" else "SUPPORTED",
        "category_ids": list(MACHINE_CATEGORIES),
        "depends_on": [],
    }


def _mechanism_a() -> dict[str, object]:
    return {
        **_common_card("A", "mechanism-card", "book-a"),
        "creative_problem": "A：资源缺口转成可观察的行动反馈",
        "applicability_conditions": ["当前短缺必须改变人物选择"],
        "mechanism": "A：让资源限制迫使角色交换或取舍。",
        "reader_payoff": ["A：读者直接感到代价和选择压力。"],
        "action_space_effect": ["A：把短缺转成行动约束。"],
        "variants": ["A：先交换再反转。"],
        "when_not_to_use": ["A：不要把卡片建议写成本书事实。"],
        "contrast_cases": ["A：不要用旁白宣布修订结果。"],
        "failure_risks": ["A：动作退化成解释清单。"],
        "failure_basis": ["A：缺少场景后果。"],
        "source_count": 4,
        "category_count": 3,
    }


def _contrast_b() -> dict[str, object]:
    solutions = []
    for index, book_id in enumerate(MACHINE_BOOKS[:3], 1):
        solution_id = f"B.solution_{index}"
        solutions.append(
            {
                "solution_id": solution_id,
                "label": f"B{index}",
                "source_book_ids": [book_id],
                "description": f"{solution_id}：把当前变化放进具体动作与即时反馈。",
                "conditions": [f"{solution_id}：变化必须能被读者观察。"],
                "reader_experience_differences": [
                    f"{solution_id}：让变化产生不同的现场反馈。"
                ],
                "tradeoffs": [f"{solution_id}：用部分解释篇幅换取现场感。"],
                "failure_risks": [f"{solution_id}：不得迁移来源人物或事件。"],
                "evidence_refs": [_evidence(book_id, index + 4)],
            }
        )
    return {
        **_common_card("B", "contrast-card", "book-b"),
        "shared_creative_problem": "B：同一类资源修订如何产生不同读者反馈",
        "solutions": solutions,
        "transfer_boundary": "B：只迁移结构动作与读者效果，不迁移来源事实。",
    }


def _synthesis_c() -> dict[str, object]:
    return {
        **_common_card("C", "corpus-synthesis", "book-c"),
        "synthesis_kind": "CROSS_CATEGORY",
        "title": "C：跨类别的修订合成",
        "shared_creative_problem": "C：第二单元需要收束并打开新的行动空间",
        "shared_tendencies": ["C：结果必须改变后续选择。"],
        "major_divergences": ["C：不同场景承担不同的反馈节奏。"],
        "distinctive_mechanisms": ["C：把已发生变化编排成下一步可用条件。"],
        "payoff_differences": ["C：读者看到结果如何改变后续可能性。"],
        "progression_differences": ["C：进展来自可验证的状态变化。"],
        "world_expansion_differences": ["C：新边界只作为候选，不写成本书事实。"],
        "failure_fatigue_risks": ["C：避免重复同一种资源展示。"],
        "what_sample_cannot_tell_us": ["C：样本不能决定本书 Canon。"],
        "transfer_boundary": "C：只迁移抽象结构变量与读者效果。",
    }


def _prose_control() -> dict[str, object]:
    return {
        **_common_card(
            "prose-control",
            "prose-control",
            "book-d",
            tags=["prose-realization", "action", "dialogue", "payoff"],
        ),
        "knowledge_level": "CORPUS_SYNTHESIS",
        "control_topic": "动作先于解释",
        "applicable_scene_functions": ["ACTION", "DIALOGUE", "PAYOFF", "AFTERMATH"],
        "guidance": "先让动作和反馈发生，再补当前场景需要的解释。",
        "variants": ["战斗保留距离和反馈", "对话保留动作与回应"],
        "when_to_use": ["读者只能复述能力名，不能复述现场过程"],
        "failure_signals": ["把技能名排成清单"],
        "transfer_boundary": "只迁移抽象写法变量，不迁移来源人物、事件或句式。",
    }


def _write_disposable_package(
    root: Path,
    *,
    include_seal: bool = True,
    records: list[dict[str, object]] | None = None,
) -> Path:
    machine = root / "machine"
    machine.mkdir(parents=True, exist_ok=True)
    card_values = records or [_mechanism_a(), _contrast_b(), _synthesis_c(), _prose_control()]
    (machine / "cards.jsonl").write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            for record in card_values
        ),
        encoding="utf-8",
    )
    (machine / "dependencies.jsonl").write_text(
        json.dumps(
            {
                "upstream_card_id": "A",
                "downstream_card_id": "C",
                "relation": "supports",
                "status": "ACTIVE",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    package: dict[str, object] = {
        "schema_version": MACHINE_PACKAGE_VERSION,
        "status": "REFERENCE_ONLY",
        "generated_at": "2026-08-15T00:00:00Z",
        "raw_text_included": False,
        "canon_committed": False,
        "edition_activated": False,
        "query_ready": True,
        "readiness_status": "READY",
        "readiness_reasons": [],
        "prose_controls_compiled": True,
        "paths": {
            "cards": "machine/cards.jsonl",
            "dependencies": "machine/dependencies.jsonl",
        },
    }
    if include_seal:
        package["machine_bundle_hash"] = compute_machine_bundle_hash(root, package=package)
    (machine / "corpus-package.json").write_text(
        json_dumps(package, indent=2), encoding="utf-8"
    )
    return root


def _revision_database(tmp_path: Path) -> Database:
    source_root = tmp_path / "revision-source"
    source_root.mkdir(parents=True)
    (source_root / "book.md").write_text(
        "## 第一章 缺口\n主角缺少晶体，必须在夜袭前作出选择。\n\n"
        "## 第二章 夜袭\n夜袭逼近，晶体仍然不足，选择会改变后续路线。\n",
        encoding="utf-8",
    )
    workspace_root = tmp_path / "revision-workspace"
    ingest_book(
        book_id="final-closure-revision",
        title="FINAL closure revision",
        source_root=source_root,
        workspace_root=workspace_root,
        settings=load_settings(),
    )
    database = Database(workspace_root / "final-closure-revision" / "state.sqlite3")
    create_edition(database, "final-closure-revision", "edition-r1", "FINAL closure revision")
    return database


def _revision_spec() -> dict[str, object]:
    return {
        "campaign_name": "FINAL closure bounded selector",
        "revision_kind": "correction",
        "intent": "把两章的晶体短缺改为可观察、可区分的行动反馈",
        "target_scope": {"chapter_ranges": [[1, 2]], "semantic_queries": []},
        "canon_changes": [],
        "entity_changes": [],
        "must_preserve": ["夜袭"],
        "must_change": ["晶体"],
        "forbidden_changes": [],
        "propagation_rules": [],
        "style_policy": {
            "creative_problem_tags": ["resource-pressure"],
            "max_cards": 6,
        },
        "completion_policy": {},
    }


def _continuation_database(tmp_path: Path) -> tuple[Database, Any]:
    fixture = Path(__file__).parents[1] / "fixtures" / "合成求生小说.md"
    source_root = tmp_path / "continuation-source"
    source_root.mkdir(parents=True)
    (source_root / fixture.name).write_bytes(fixture.read_bytes())
    workspace_root = tmp_path / "continuation-workspace"
    settings = load_settings()
    ingest_book(
        book_id="final-closure-continuation",
        title="FINAL closure continuation",
        source_root=source_root,
        workspace_root=workspace_root,
        settings=settings,
    )
    database = Database(workspace_root / "final-closure-continuation" / "state.sqlite3")
    with database.connect() as connection:
        for index, (thread_id, goal, progress) in enumerate(
            [
                ("station-defense", "守住气象站", 0.7),
                ("radio-caller", "确认无线电呼叫者身份", 0.4),
                ("wind-rule", "理解午夜风向规则", 0.5),
            ],
            1,
        ):
            connection.execute(
                """
                INSERT INTO threads(
                    thread_id, book_id, goal, stakes, phase,
                    introduced_chapter, last_advanced_chapter,
                    importance, reader_visibility, progress,
                    dependencies_json, status, payload_json, created_at
                ) VALUES (
                    ?, 'final-closure-continuation', ?, ?, 'escalation', '1',
                    ?, ?, 0.9, ?, '[]', 'CANON', ?, ?
                )
                """,
                (
                    thread_id,
                    goal,
                    f"线程 {index} 失败会改变后续选择",
                    str(index),
                    1 - index * 0.1,
                    progress,
                    json_dumps(
                        {
                            "deadline_urgency": 80 - index * 10,
                            "payoff_readiness": progress * 100,
                            "goal_blockage": (1 - progress) * 100,
                            "diversity_bonus": 40 + index * 10,
                        }
                    ),
                    utc_now(),
                ),
            )
    bundle = MetricInputBundle.model_validate(
        {
            "pressure": {
                "threat": 70,
                "scarcity": 60,
                "deadline": 80,
                "uncertainty": 50,
                "social_conflict": 20,
                "failure_accumulation": 30,
            },
            "narrative_debt": {
                "importance": 0.8,
                "reader_visibility": 0.9,
                "promise_progress": 0.4,
                "age_chapters": 3,
                "target_max_age": 5,
                "reminder_count": 1,
            },
            "progress": {
                "permanent_growth": 40,
                "world_state_change": 50,
                "relationship_change": 20,
                "knowledge_change": 70,
                "goal_advance": 60,
                "strategy_expansion": 30,
            },
            "payoff": {
                "maturity": 70,
                "impact": 60,
                "causality": 90,
                "after_value": 70,
                "repetition_fatigue": 10,
                "structural_fit": 80,
                "future_damage": 10,
            },
            "repetition_history": [{"distance": 5, "similarity": 0.2}],
            "risk_credibility": {
                "realized_cost_rate": 60,
                "consequence_clarity": 80,
                "opposition_effectiveness": 60,
                "protection_limit_visibility": 70,
                "information_limits": 80,
            },
        }
    )
    persist_results(
        database,
        "final-closure-continuation",
        diagnose_bundle(bundle, settings.metrics),
        settings.metrics,
    )
    return database, settings


def _complete_original_reader_handoff(database: Database, book_id: str) -> None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT handoff_id FROM workflow_handoffs WHERE book_id=? "
            "AND handoff_type='ORIGINAL_READER_INTERPRETATION' "
            "ORDER BY created_at DESC LIMIT 1",
            (book_id,),
        ).fetchone()
    assert row is not None
    handoff_id = str(row["handoff_id"])
    handoff = get_handoff(database, handoff_id)
    task_directory = Path(str(handoff["task_directory"]))
    task = json.loads((task_directory / "input" / "task.json").read_text(encoding="utf-8"))
    contract_ids = task["original_reader_interpretation"]["contract_ids"]
    interpreted = compile_kernel_contract_proposals(
        interpret_reader_experience(
            "用于 FINAL closure 的生存升级 premise。", genre_hint="生存升级"
        )
    )
    assert interpreted.progression is not None
    reader = interpreted.reader_experience.model_copy(
        update={"contract_id": contract_ids["reader_experience_contract_id"]}
    )
    market = interpreted.market_category.model_copy(
        update={"metadata_id": contract_ids["market_category_metadata_id"]}
    )
    drive = interpreted.narrative_drive.model_copy(
        update={"drive_contract_id": contract_ids["narrative_drive_contract_id"]}
    )
    creative_semantics = OriginalCreativeSemantics.model_validate(
        {
            "signature_fantasy": "有限资源在压力中打开新的行动空间",
            "existing_signature_mechanism": "每次选择都留下可追踪代价",
            "open_design_space": ["如何让每次选择保持新鲜"],
            "payoff_texture": ["选择产生即时反馈"],
            "novelty_focus": ["同一资源在不同压力下产生不同用途"],
            "realism_anchors": ["人物始终受资源与信息限制"],
            "complexity_boundaries": ["不新增第二套核心机制"],
            "repeatable_reader_loop": ["压力出现", "作出选择", "承担反馈"],
            "anti_drift": ["不把参考卡片写成本书事实"],
        }
    )
    proposal = OriginalReaderKernelProposal(
        summary="有限资源选择持续制造生存压力与行动机会。",
        reader_experience=reader,
        market_category=market,
        narrative_drive=drive,
        creative_semantics=creative_semantics,
        semantic_evidence=["压力来自不可逆资源选择"],
        uncertainties=["长期机制仍待作者审阅"],
        author_attention_points=["确认资源压力的强度"],
    )
    artifact = task_directory / "artifacts" / "reader_kernel" / "proposal.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json_dumps(proposal.model_dump(mode="json"), indent=2), encoding="utf-8")
    claim = claim_handoff(database, handoff_id, "final-closure-test")
    token = str(claim["claim_token"])
    update_handoff_status(database, handoff_id, HandoffStatus.RUNNING, claim_token=token)
    frozen = get_handoff(database, handoff_id)
    update_handoff_status(
        database,
        handoff_id,
        HandoffStatus.COMPLETED,
        claim_token=token,
        result={
            "handoff_id": handoff_id,
            "handoff_type": "ORIGINAL_READER_INTERPRETATION",
            "requested_stage": "READER_KERNEL_PROPOSAL",
            "completed_stage": "READER_KERNEL_PROPOSED",
            "book_id": book_id,
            "edition_id": "base",
            "status": "COMPLETED",
            "artifact_paths": ["artifacts/reader_kernel/proposal.json"],
            "canon_committed": False,
            "edition_activated": False,
            "base_event_seq": int(frozen["base_event_seq"]),
            "base_projection_hash": str(frozen["base_projection_hash"]),
        },
    )
    imported = import_original_reader_kernel_proposal(database, book_id, handoff_id)
    assert imported["handoff_id"] == handoff_id
    confirmed = confirm_original_reader_experience(
        database, book_id, creative_semantics=creative_semantics.model_dump(mode="json")
    )
    assert confirmed["reader_experience"]["status"] == "EFFECTIVE"


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return {str(key) for key in value} | {
            nested_key for nested in value.values() for nested_key in _all_keys(nested)
        }
    if isinstance(value, list):
        return {nested_key for nested in value for nested_key in _all_keys(nested)}
    return set()


def test_revision_closure_uses_bounded_frozen_cards_and_draft_chain(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _write_disposable_package(tmp_path / "corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(root))
    database = _revision_database(tmp_path)

    from novel_authoring.revision import service as revision_service

    calls: list[ReferenceCorpusQueryRequest] = []
    real_query = revision_service.query_reference_corpus

    def capture_query(
        request: ReferenceCorpusQueryRequest, *, corpus_root: Path | None = None
    ) -> Any:
        calls.append(request)
        return real_query(request, corpus_root=corpus_root)

    monkeypatch.setattr(revision_service, "query_reference_corpus", capture_query)
    campaign = create_revision_campaign(
        database,
        "final-closure-revision",
        _revision_spec(),
        edition_id="edition-r1",
    )
    campaign_id = str(campaign["campaign_id"])
    impact = build_revision_impact(database, "final-closure-revision", campaign_id)
    assert calls == [], "Impact 阶段不得查询 Reference Corpus"
    complete_revision_impact_audit(
        database,
        "final-closure-revision",
        campaign_id,
        [
            {"impact_id": item["impact_id"], "status": "HANDLED"}
            for item in impact["items"]
        ],
    )
    assert calls == [], "Impact Audit 阶段不得查询 Reference Corpus"

    plan = build_revision_plan(database, "final-closure-revision", campaign_id)
    planning_calls = [request for request in calls if request.purpose == "PLANNING"]
    assert len(planning_calls) == 1
    planning_context = plan["reference_planning_context"]
    assert planning_context["status"] == "ENABLED"
    assert set(planning_context["selected_card_ids"]) == {"A", "B", "C"}
    snapshot = load_reference_context_snapshot(Path(str(planning_context["snapshot_path"])))
    snapshot_cards = {str(card["card_id"]): card for card in snapshot.compact_cards}
    assert set(snapshot_cards) == {"A", "B", "C"}
    solution_ids = {
        str(solution["solution_id"]) for solution in snapshot_cards["B"]["solutions"]
    }
    assert solution_ids == {"B.solution_1", "B.solution_2", "B.solution_3"}

    units = plan["units"]
    assert len(units) >= 2, "disposable fixture 必须产生两个 RevisionUnit"
    unit1 = units[0]
    unit2 = units[1]

    # This is the Local File Handoff boundary: the bounded semantic selector
    # chooses HOW per unit, while Python only imports and validates the typed
    # result against the frozen snapshot and RevisionUnit authority.
    fallback1 = dict(plan["strategies"][str(unit1["unit_id"])])
    fallback1.update(
        {
            "strategy_summary": "Unit1 采用 A 的资源约束，并选择 B.solution_2 的现场反馈路线。",
            "structural_moves": [
                "让资源短缺迫使目标场景中的角色作出可观察取舍。",
                "用 B.solution_2 的即时反馈收束本单元，不迁移来源事实。",
            ],
            "reader_effect_targets": ["让读者感到选择代价并看见反馈。"],
            "failure_modes_to_avoid": ["把参考机制写成本书事实。"],
            "reference_card_ids_used": ["A", "B"],
            "selected_contrast_solutions": [
                {"card_id": "B", "solution_id": "B.solution_2"}
            ],
        }
    )
    fallback2 = dict(plan["strategies"][str(unit2["unit_id"])])
    fallback2.update(
        {
            "strategy_summary": "Unit2 采用 C 的后续行动空间收束方式。",
            "structural_moves": ["让已发生的变化改变下一步可用选择。"],
            "reader_effect_targets": ["让读者看见结果如何打开新的行动空间。"],
            "failure_modes_to_avoid": ["重复 Unit1 的同一资源展示。"],
            "reference_card_ids_used": ["C"],
            "selected_contrast_solutions": [],
        }
    )
    selector_output = {
        "task_type": "REVISION_STRATEGY_SELECTION",
        "task_id": plan["planning_provenance"]["task_id"],
        "campaign_id": plan["campaign_id"],
        "edition_id": plan["planning_provenance"]["edition_id"],
        "planning_snapshot_id": snapshot.snapshot_id,
        "planning_snapshot_hash": snapshot.snapshot_hash,
        "strategies": {
            str(unit1["unit_id"]): fallback1,
            str(unit2["unit_id"]): fallback2,
        },
    }
    selector_output_path = Path(str(plan["strategy_selection"]["expected_output"]))
    selector_output_path.write_text(
        json.dumps(selector_output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    imported = import_revision_strategy_selection(
        database,
        "final-closure-revision",
        campaign_id,
        selector_output_path,
    )
    assert imported["status"] == "IMPORTED"
    plan = json.loads(Path(str(plan["plan_path"])).read_text(encoding="utf-8"))
    strategy1 = plan["strategies"][str(unit1["unit_id"])]
    strategy2 = plan["strategies"][str(unit2["unit_id"])]
    used1 = set(strategy1["reference_card_ids_used"])
    used2 = set(strategy2["reference_card_ids_used"])
    strategy1_text = json.dumps(strategy1, ensure_ascii=False)
    strategy2_text = json.dumps(strategy2, ensure_ascii=False)
    frozen_solutions = {
        (card_id, str(solution["solution_id"]))
        for card_id, card in snapshot_cards.items()
        for solution in card.get("solutions", [])
    }

    assert used1 == {"A", "B"}
    assert used1 != set(planning_context["selected_card_ids"])
    assert strategy1["selected_contrast_solutions"] == [
        {"card_id": "B", "solution_id": "B.solution_2"}
    ]
    assert ("B", "B.solution_2") in frozen_solutions
    assert all(
        (str(selection["card_id"]), str(selection["solution_id"])) in frozen_solutions
        for selection in strategy1["selected_contrast_solutions"]
    )
    assert "B.solution_2" in strategy1_text
    assert "B.solution_1" not in strategy1_text
    assert "B.solution_3" not in strategy1_text
    assert used1 <= set(snapshot_cards)
    assert used2 in ({"C"}, set())
    assert used1 != used2
    if used2:
        assert "C" in strategy2_text
        assert "B.solution_1" not in strategy2_text
        assert "B.solution_2" not in strategy2_text
        assert "B.solution_3" not in strategy2_text

    for unit in (unit1, unit2):
        strategy = plan["strategies"][str(unit["unit_id"])]
        task = prepare_revision_draft_task(
            database,
            "final-closure-revision",
            campaign_id,
            str(unit["unit_id"]),
        )
        task_payload = json.loads(Path(str(task["task_path"])).read_text(encoding="utf-8"))
        assert task_payload["revision_strategy"] == strategy
        assert task_payload["planning_provenance"]["planning_snapshot_id"] == snapshot.snapshot_id
        assert task_payload["planning_snapshot_hash"] == snapshot.snapshot_hash
        assert task_payload["reference_prose_context"]["status"] == "ENABLED"
        assert task_payload["reference_prose_context"]["selected_card_ids"] == [
            "prose-control"
        ]
        assert task_payload["scene_functions"] == ["ACTION", "PAYOFF"]
        assert task_payload["scene_function_source"] == "revision_kind_fallback"

    prose_calls = [request for request in calls if request.purpose == "PROSE"]
    # Identical unit scene-function requests reuse the same frozen PROSE
    # snapshot; one gateway call is sufficient for both draft tasks.
    assert len(prose_calls) >= 1
    assert all(request.scene_functions for request in prose_calls)
    assert all(
        set(request.scene_functions).isdisjoint(
            {"mechanism-card", "contrast-card", "corpus-synthesis"}
        )
        for request in prose_calls
    )


@pytest.mark.parametrize("mutation", ["cards", "dependencies"])
def test_valid_seal_rejects_missing_or_mutated_machine_bundle(
    tmp_path: Path, mutation: str
) -> None:
    root = _write_disposable_package(tmp_path / "sealed")
    package_path = root / "machine" / "corpus-package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    assert package["machine_bundle_hash"] == compute_machine_bundle_hash(root, package=package)
    assert (
        query_reference_corpus({"purpose": "PLANNING", "max_cards": 6}, corpus_root=root).status
        == "ENABLED"
    )
    assert reference_corpus_runtime_diagnostic(corpus_root=root)["status"] == "ENABLED"

    missing_seal = dict(package)
    missing_seal.pop("machine_bundle_hash")
    package_path.write_text(json_dumps(missing_seal, indent=2), encoding="utf-8")
    missing_response = query_reference_corpus(
        {"purpose": "PLANNING", "max_cards": 6}, corpus_root=root
    )
    assert missing_response.status == "UNAVAILABLE"
    assert any("RECOMPILE_REQUIRED" in warning for warning in missing_response.warnings)
    assert reference_corpus_runtime_diagnostic(corpus_root=root)["status"] == "UNAVAILABLE"

    package_path.write_text(json_dumps(package, indent=2), encoding="utf-8")
    target = root / "machine" / f"{mutation}.jsonl"
    if mutation == "cards":
        target = root / "machine" / "cards.jsonl"
        rows = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines()]
        rows[0]["mechanism"] = "A：发生了未重新 compile 的 machine mutation。"
        target.write_text(
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
    else:
        target = root / "machine" / "dependencies.jsonl"
        target.write_text(
            json.dumps(
                {
                    "upstream_card_id": "A",
                    "downstream_card_id": "C",
                    "relation": "invalidated",
                    "status": "STALE",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
    mutated_response = query_reference_corpus(
        {"purpose": "PLANNING", "max_cards": 6}, corpus_root=root
    )
    assert mutated_response.status == "CORRUPT"
    assert any(
        "MACHINE_BUNDLE_HASH_MISMATCH" in warning for warning in mutated_response.warnings
    )
    diagnostic = reference_corpus_runtime_diagnostic(corpus_root=root)
    assert diagnostic["status"] == "CORRUPT"
    assert any("MACHINE_BUNDLE_HASH_MISMATCH" in warning for warning in diagnostic["warnings"])


def test_generated_at_only_keeps_valid_machine_seal_stable(tmp_path: Path) -> None:
    root = _write_disposable_package(tmp_path / "generated-at")
    package_path = root / "machine" / "corpus-package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    before = query_reference_corpus(
        {"purpose": "PLANNING", "max_cards": 6}, corpus_root=root
    )
    package["generated_at"] = "2099-01-01T00:00:00Z"
    package_path.write_text(json_dumps(package, indent=2), encoding="utf-8")
    after = query_reference_corpus(
        {"purpose": "PLANNING", "max_cards": 6}, corpus_root=root
    )
    assert before.status == after.status == "ENABLED"
    assert before.machine_bundle_hash == after.machine_bundle_hash
    assert package["machine_bundle_hash"] == after.machine_bundle_hash


def test_original_supported_handoff_keeps_full_snapshot_provenance_out_of_executor_projection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _write_disposable_package(tmp_path / "original-corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(root))
    created = create_original_book(
        BookLayout(tmp_path / "library"),
        {"premise": "城市每天删除一种情感，但每次选择都留下可追踪代价。"},
        book_id="final-closure-original",
    )
    database = Database(Path(str(created["database"])))
    _complete_original_reader_handoff(database, "final-closure-original")
    handoff = prepare_original_core_innovation(database, "final-closure-original")
    task_directory = Path(str(handoff["task_directory"]))
    original_request = json.loads(
        (task_directory / "input" / "original_request.json").read_text(encoding="utf-8")
    )
    executor_task = json.loads(
        (task_directory / "input" / "task.json").read_text(encoding="utf-8")
    )
    context = original_request["reference_planning_context"]
    progression_kernel = original_request["progression_kernel"]
    reader_payload = progression_kernel["reader_experience"]["payload"]

    assert handoff["status"] == "READY_FOR_CODEX"
    assert original_request["requested_stage"] == "CORE_INNOVATION_PROPOSAL"
    assert progression_kernel["creative_semantics"]
    assert reader_payload["contract_id"]
    assert context["status"] == "ENABLED"
    assert set(context["selected_card_ids"]) == {"A", "B", "C"}
    assert context["snapshot_id"]
    assert context["machine_bundle_hash"]
    assert context["compact_cards"]
    assert any(
        card.get("mechanism") or card.get("shared_creative_problem")
        for card in context["compact_cards"]
    )

    assert _all_keys(original_request).isdisjoint(FORBIDDEN_EXECUTOR_FIELDS)
    executor_keys = _all_keys(executor_task)
    assert executor_keys.isdisjoint(FORBIDDEN_EXECUTOR_FIELDS)
    assert "executor_skill" in executor_task
    assert executor_task["book_id"] == "final-closure-original"
    assert executor_task["original_bootstrap"]["request_path"] == "original_request.json"
    assert executor_task["original_bootstrap"]["canon_boundary"] == "NO_CHAPTER_NO_CANON"


def test_continuation_tags_impact_zero_query_family_isolation_and_snapshot_soft_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _write_disposable_package(tmp_path / "regression-corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(root))

    planning = query_reference_corpus(
        {"purpose": "PLANNING", "max_cards": 6}, corpus_root=root
    )
    prose = query_reference_corpus(
        {"purpose": "PROSE", "scene_functions": ["ACTION"], "max_cards": 4},
        corpus_root=root,
    )
    assert planning.status == "ENABLED"
    assert {card.card_type for card in planning.cards} == {
        "mechanism-card",
        "contrast-card",
        "corpus-synthesis",
    }
    assert [card.card_type for card in prose.cards] == ["prose-control"]

    from novel_authoring.planning import candidates as candidate_service

    calls: list[ReferenceCorpusQueryRequest] = []
    real_query = candidate_service.query_reference_corpus

    def capture_candidate_query(
        request: ReferenceCorpusQueryRequest, *, corpus_root: Path | None = None
    ) -> Any:
        calls.append(request)
        return real_query(request, corpus_root=corpus_root)

    monkeypatch.setattr(candidate_service, "query_reference_corpus", capture_candidate_query)
    database, settings = _continuation_database(tmp_path)
    task = prepare_candidate_task(database, "final-closure-continuation", settings)
    candidate_calls = [request for request in calls if request.purpose == "PLANNING"]
    assert len(candidate_calls) == 1
    assert candidate_calls[0].creative_problem_tags, "state-derived tags must reach the query"
    task_payload = json.loads(
        (Path(str(task["input"])).parent / "task.json").read_text(encoding="utf-8")
    )
    assert task_payload["reference_planning_context"]["status"] == "ENABLED"
    assert task_payload["reference_planning_context"]["selected_card_ids"]

    snapshot_path = tmp_path / "integrity" / "snapshot.json"
    frozen = freeze_reference_context(
        ReferenceCorpusQueryRequest(purpose="PLANNING", max_cards=6),
        planning,
        book_id="snapshot-book",
        edition_id="base",
        operation_id="final-closure-snapshot",
        output_path=snapshot_path,
    )
    loaded = load_reference_context_snapshot(snapshot_path)
    assert loaded.snapshot_hash == frozen.snapshot_hash
    tampered = json.loads(snapshot_path.read_text(encoding="utf-8"))
    tampered["compact_cards"][0]["card_id"] = "tampered-card"
    snapshot_path.write_text(json_dumps(tampered, indent=2), encoding="utf-8")
    with pytest.raises(ReferenceContextIntegrityError):
        load_reference_context_snapshot(snapshot_path)

    missing = query_reference_corpus(
        {"purpose": "PLANNING", "max_cards": 6}, corpus_root=tmp_path / "missing"
    )
    assert missing.status == "UNAVAILABLE"
    assert not missing.cards
