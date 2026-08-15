"""Reference Corpus Semantic V1 integration closure evidence.

All Corpus data in this module is disposable machine-package input under
``tmp_path``.  It is deliberately not a production Corpus or browser proof.
The tests exercise the public query gateway/context seam and the existing
authoring task preparation functions without approving drafts or committing
Canon.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from novel_authoring.canon.events import EventStatus, EventStore
from novel_authoring.canon.projection import rebuild_projection
from novel_authoring.config import Settings, load_settings
from novel_authoring.db.database import Database
from novel_authoring.domain.models import InformationStatus
from novel_authoring.drafting.service import prepare_draft_task
from novel_authoring.edition import create_edition
from novel_authoring.ingest.service import ingest_book
from novel_authoring.metrics.engine import MetricInputBundle, diagnose_bundle, persist_results
from novel_authoring.original import service as original_service
from novel_authoring.original.service import create_original_book
from novel_authoring.planning.candidates import prepare_candidate_task
from novel_authoring.planning.models import ChapterContract
from novel_authoring.reference_corpus.context import (
    freeze_reference_context,
    load_reference_context_snapshot,
)
from novel_authoring.reference_corpus.query import (
    ReferenceCorpusQueryRequest,
    ReferenceCorpusQueryResponse,
    query_reference_corpus,
)
from novel_authoring.reference_corpus.semantic import compute_machine_bundle_hash
from novel_authoring.revision import (
    build_revision_impact,
    build_revision_plan,
    complete_revision_impact_audit,
    create_revision_campaign,
    import_revision_strategy_selection,
    prepare_revision_draft_task,
)
from novel_authoring.revision.service import RevisionWorkflowError
from novel_authoring.storage.layout import BookLayout
from novel_authoring.utils import json_dumps, stable_id, utc_now
from novel_authoring.workflows.handoffs import get_handoff

MACHINE_PACKAGE_VERSION = "reference-corpus-machine-package-v1"
MACHINE_BOOKS = ["reference-book-01", "reference-book-02", "reference-book-03", "reference-book-04"]
MACHINE_CATEGORIES = ["玄幻", "都市", "科幻"]
CORPUS_FIXTURE_TAG = "resource-pressure"


def _evidence(book_id: str, index: int, *, line_start: int = 1) -> dict[str, object]:
    return {
        "evidence_id": f"ev-{book_id}-{index}",
        "source_book_id": book_id,
        "source_id": f"source-{book_id}",
        "distill_id": f"distill-{book_id}",
        "segment_id": "segment-0001",
        "line_start": line_start,
        "line_end": line_start + 2,
        "observation_summary": "只保留抽象动作、反馈和局部证据定位，不保存来源正文。",
    }


def _common_card(card_id: str, card_type: str) -> dict[str, object]:
    return {
        "schema_version": "reference-corpus-card-v1",
        "card_id": card_id,
        "card_type": card_type,
        "knowledge_level": "CROSS_BOOK_CONTRAST",
        "status": "REFERENCE_ONLY",
        "source_book_ids": list(MACHINE_BOOKS),
        "evidence_refs": [
            _evidence(book_id, index) for index, book_id in enumerate(MACHINE_BOOKS, 1)
        ],
        "creative_problem_tags": [
            CORPUS_FIXTURE_TAG,
            "breakthrough",
            "long-form",
            "post-payoff-anticipation",
            "relationship",
            "mystery-reveal",
        ],
        "reader_experiences": ["BREAKTHROUGH"],
        "narrative_drives": ["POWER_PROGRESSION"],
        "payoff_channels": ["POWER_BREAKTHROUGH"],
        "evidence_scope": "MULTI_CATEGORY",
        "maturity": "SUPPORTED",
        "category_ids": list(MACHINE_CATEGORIES),
        "depends_on": [],
    }


def _mechanism_card(card_id: str = "mechanism-closure") -> dict[str, object]:
    return {
        **_common_card(card_id, "mechanism-card"),
        "creative_problem": "资源缺口如何转成可观察的场景动作",
        "applicability_conditions": ["资源缺口必须改变当前选择"],
        "mechanism": "让资源限制迫使角色交换或取舍，并把结果写成行动反馈。",
        "reader_payoff": ["读者直接感到代价和选择压力"],
        "action_space_effect": ["把资源缺口转成可观察的行动约束"],
        "variants": ["先交换再反转", "先暴露短缺再改变选择"],
        "when_not_to_use": ["不要把卡片建议写成本书事实"],
        "contrast_cases": ["不要用旁白直接宣布修订结果"],
        "failure_risks": ["动作变成解释性清单"],
        "failure_basis": ["缺少场景后果"],
        "source_count": len(MACHINE_BOOKS),
        "category_count": len(MACHINE_CATEGORIES),
    }


def _contrast_card(card_id: str = "contrast-closure") -> dict[str, object]:
    solutions = []
    for index, book_id in enumerate(MACHINE_BOOKS[:3], 1):
        solutions.append(
            {
                "solution_id": f"solution-{index}",
                "label": f"方案 {index}",
                "source_book_ids": [book_id],
                "description": "以当前场景动作承载变化，保留可验证的结果反馈。",
                "conditions": ["变化必须可被读者观察"],
                "reader_experience_differences": ["让变化产生即时反馈"],
                "tradeoffs": ["牺牲部分解释篇幅换取现场感"],
                "failure_risks": ["把参考方案误写成事实"],
                "evidence_refs": [_evidence(book_id, index, line_start=index + 3)],
            }
        )
    return {
        **_common_card(card_id, "contrast-card"),
        "shared_creative_problem": "如何让同一类资源修订产生不同读者反馈",
        "solutions": solutions,
        "transfer_boundary": "只迁移结构动作与读者效果，不迁移来源事实或人物事件。",
    }


def _prose_control_card(card_id: str = "prose-control-closure") -> dict[str, object]:
    return {
        **_common_card(card_id, "prose-control"),
        "knowledge_level": "CORPUS_SYNTHESIS",
        "maturity": "BROAD",
        "creative_problem_tags": ["prose-realization", "action"],
        "reader_experiences": [],
        "narrative_drives": [],
        "payoff_channels": [],
        "control_topic": "动作先于解释",
        "applicable_scene_functions": ["ACTION", "DIALOGUE", "PAYOFF", "AFTERMATH"],
        "guidance": "先让动作和反馈发生，再补当前场景需要的解释。",
        "variants": ["战斗保留距离和反馈", "对话保留动作与回应"],
        "when_to_use": ["读者只能复述能力名，不能复述现场过程"],
        "failure_signals": ["把技能名排成清单"],
        "transfer_boundary": "只迁移抽象写法变量，不迁移来源人物、事件或句式。",
    }


def _write_machine_package(
    root: Path,
    *,
    records: list[dict[str, object]] | None = None,
    query_ready: bool = True,
) -> Path:
    """Create the smallest disposable machine package consumed by the gateway."""

    machine = root / "machine"
    machine.mkdir(parents=True, exist_ok=True)
    package = {
        "schema_version": MACHINE_PACKAGE_VERSION,
        "status": "REFERENCE_ONLY",
        "query_ready": query_ready,
        "raw_text_included": False,
        "readiness_status": "READY" if query_ready else "NOT_READY",
        "readiness_reasons": [] if query_ready else ["closure fixture deliberately not ready"],
        "prose_controls_compiled": query_ready,
        "canon_committed": False,
        "edition_activated": False,
    }
    (machine / "corpus-package.json").write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    values = records if records is not None else [
        _mechanism_card(),
        _contrast_card(),
        _prose_control_card(),
    ]
    (machine / "cards.jsonl").write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in values),
        encoding="utf-8",
    )
    (machine / "dependencies.jsonl").write_text("", encoding="utf-8")
    package["machine_bundle_hash"] = compute_machine_bundle_hash(root, package=package)
    (machine / "corpus-package.json").write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return root


def _setup_revision_book(tmp_path: Path) -> Database:
    source = tmp_path / "source"
    source.mkdir(parents=True)
    (source / "book.md").write_text(
        "## 第一章 缺口\n主角缺少晶体。\n\n## 第二章 夜袭\n夜袭逼近。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="closure-revision",
        title="改写 closure 测试",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    database = Database(workspace / "closure-revision" / "state.sqlite3")
    create_edition(database, "closure-revision", "edition-r1", "closure 改写候选")
    return database


def _revision_spec() -> dict[str, object]:
    return {
        "campaign_name": "closure 修正晶体缺口",
        "revision_kind": "correction",
        "intent": "把第一章错误的资源事实改为已获得晶体",
        "target_scope": {"chapter_ranges": [[1, 1]], "semantic_queries": []},
        "canon_changes": [],
        "entity_changes": [],
        "must_preserve": ["夜袭"],
        "must_change": ["晶体"],
        "forbidden_changes": [],
        "propagation_rules": [],
        "style_policy": {
            "creative_problem_tags": [CORPUS_FIXTURE_TAG],
            "max_cards": 6,
        },
        "completion_policy": {},
    }


def _setup_continuation_book(tmp_path: Path) -> tuple[Database, Settings]:
    fixture = Path(__file__).parents[1] / "fixtures" / "合成求生小说.md"
    source_root = tmp_path / "中文小说"
    source_root.mkdir(parents=True)
    (source_root / fixture.name).write_bytes(fixture.read_bytes())
    workspace = tmp_path / "workspace"
    settings = load_settings()
    ingest_book(
        book_id="closure-continuation",
        title="合成求生 closure 测试",
        source_root=source_root,
        workspace_root=workspace,
        settings=settings,
    )
    database = Database(workspace / "closure-continuation" / "state.sqlite3")
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
                ) VALUES (?, 'closure-continuation', ?, ?, 'escalation', '1', ?, ?, 0.9, ?, '[]',
                          'CANON', ?, ?)
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
        "closure-continuation",
        diagnose_bundle(bundle, settings.metrics),
        settings.metrics,
    )
    return database, settings


def _setup_draft_book(tmp_path: Path) -> tuple[Database, ChapterContract]:
    source_dir = tmp_path / "中文来源"
    source_dir.mkdir(parents=True)
    source_path = source_dir / "合成小说.md"
    source_path.write_text(
        "## 第一章 缺口\n主角缺少低级晶体。\n\n## 第二章 夜袭\n夜袭逼近。\n",
        encoding="utf-8",
    )
    workspace_root = tmp_path / "中文工作区"
    ingest_book(
        book_id="closure-draft",
        title="Draft closure 测试",
        source_root=source_dir,
        workspace_root=workspace_root,
        settings=load_settings(),
    )
    database = Database(workspace_root / "closure-draft" / "state.sqlite3")
    EventStore(database).append(
        book_id="closure-draft",
        event_type="TIMELINE_ENTRY_SET",
        aggregate_type="timeline",
        aggregate_id="timeline-existing",
        payload={"timeline_id": "timeline-existing", "label": "夜袭开始", "order_key": 1},
        source_kind="TEST",
        status=EventStatus.COMMITTED,
        information_state=InformationStatus.CANON,
        canon_commit_id="closure-seed",
    )
    projection = rebuild_projection(database, "closure-draft")
    packet_id = "packet-closure-draft"
    boundary_dir = workspace_root / "closure-draft" / "boundaries"
    boundary_dir.mkdir(parents=True, exist_ok=True)
    (boundary_dir / f"{packet_id}.md").write_text("# 合成边界\n", encoding="utf-8")
    contract = ChapterContract(
        contract_id="contract-closure-draft",
        chapter=3,
        mode="faithful_continuation",
        boundary_packet_id=packet_id,
        continuation_boundary={
            "last_canon_chapter": 2,
            "base_event_seq": projection.through_event_seq,
            "base_projection_hash": projection.sha256(),
        },
        candidate_id="candidate-closure-draft",
        primary_thread="thread-resource",
        primary_function="major_payoff",
        secondary_functions=["aftershock"],
        reader_question="低级晶体能否形成正循环？",
        pressure={"before": 82.0, "target_after": 38.0},
        payoff_plan={"causal_sources": ["夜袭"], "state_changes": ["资源自由"]},
        narrative_debt={"advance": [], "fully_pay": [], "new_major_hooks_allowed": 1},
        progress={"minimum_score": 25, "required_irreversible_change": "资源自由"},
        required_irreversible_change="普通诡晶不再是核心焦虑",
        required_cost="备用箭矢耗尽",
        canon_constraints=["不得凭空增加资源"],
        knowledge_constraints=["主角只能知道已观察事实"],
        must_not_resolve=["高级诡晶短缺"],
        forbidden_repetitions=["普通宝箱暴富"],
        style_constraints={"pov": "第三人称限知"},
        ending_state="高级诡晶仍是下一层瓶颈",
        commit_updates=["resource_stock", "payoff_history", "aftershock_obligations"],
    )
    contract_json = json_dumps(contract.model_dump(mode="json"))
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO candidate_plans(
                candidate_id, book_id, task_id, rank, primary_thread_id,
                primary_function, plan_json, score_json, gate_report_json,
                selection_status, status, created_at
            ) VALUES (?, ?, 'task', 1, ?, 'major_payoff', '{}', '{}', '{}',
                      'SELECTED', 'CANDIDATE', ?)
            """,
            ("candidate-closure-draft", "closure-draft", "thread-resource", utc_now()),
        )
        connection.execute(
            """
            INSERT INTO chapter_contracts(
                contract_id, book_id, candidate_id, target_chapter_ordinal,
                mode, contract_json, contract_sha256, status, created_at
            ) VALUES (?, ?, ?, 3, ?, ?, ?, 'READY', ?)
            """,
            (
                contract.contract_id,
                "closure-draft",
                contract.candidate_id,
                contract.mode.value,
                contract_json,
                stable_id("hash", contract_json),
                utc_now(),
            ),
        )
    return database, contract


def test_disposable_machine_package_gateway_and_snapshot_closure(tmp_path: Path) -> None:
    root = _write_machine_package(tmp_path / "disposable-corpus")
    package = json.loads(
        (root / "machine" / "corpus-package.json").read_text(encoding="utf-8")
    )
    assert package["status"] == "REFERENCE_ONLY"
    assert package["query_ready"] is True
    assert package["raw_text_included"] is False
    planning_request = {
        "purpose": "PLANNING",
        "creative_problem": "资源缺口如何转成当前修订的可观察动作",
        "creative_problem_tags": [CORPUS_FIXTURE_TAG],
        "max_cards": 6,
    }
    planning = query_reference_corpus(planning_request, corpus_root=root)

    assert planning.status == "ENABLED"
    assert planning.usage == "REFERENCE_ONLY"
    assert planning.package_schema_version == MACHINE_PACKAGE_VERSION
    assert planning.machine_bundle_hash
    assert {card.card_id for card in planning.cards} == {
        "mechanism-closure",
        "contrast-closure",
    }
    assert all(card.card_type in {"mechanism-card", "contrast-card"} for card in planning.cards)
    assert all("observation_summary" not in card.model_dump() for card in planning.cards)

    snapshot_path = tmp_path / "snapshot" / "reference_context_snapshot.json"
    request_model = ReferenceCorpusQueryRequest.model_validate(planning_request)
    frozen = freeze_reference_context(
        request_model,
        planning,
        book_id="closure-book",
        edition_id="base",
        operation_id="closure-query-snapshot",
        output_path=snapshot_path,
    )
    assert frozen.status == "ENABLED"
    assert frozen.machine_bundle_hash == planning.machine_bundle_hash
    assert frozen.selected_card_count == 2
    assert set(frozen.selected_card_ids) == {"mechanism-closure", "contrast-closure"}
    assert frozen.snapshot_id
    loaded = load_reference_context_snapshot(snapshot_path)
    assert loaded.snapshot_id == frozen.snapshot_id
    assert loaded.snapshot_hash == frozen.snapshot_hash

    prose = query_reference_corpus(
        {
            "purpose": "PROSE",
            "scene_functions": ["ACTION"],
            "max_cards": 4,
        },
        corpus_root=root,
    )
    assert prose.status == "ENABLED"
    assert [card.card_id for card in prose.cards] == ["prose-control-closure"]


def test_original_task_freezes_enabled_planning_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_root = _write_machine_package(tmp_path / "corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(corpus_root))
    created = create_original_book(
        BookLayout(tmp_path / "library"),
        {"premise": "城市每天删除一种情感，但每次选择都留下可追踪代价。"},
        book_id="closure-original",
    )
    database = Database(Path(str(created["database"])))
    handoff = get_handoff(database, str(created["reader_handoff"]["handoff_id"]))
    task_directory = Path(str(handoff["task_directory"]))
    request = json.loads(
        (task_directory / "input" / "original_request.json").read_text(encoding="utf-8")
    )
    # The first Original Reader handoff freezes only the reader-kernel request
    # as its business input.  The real Original planning adapter is called at
    # the next authoring stage, so inspect that adapter directly and separately
    # assert that the reader handoff was created.
    context = original_service._original_reference_planning_context(
        {"premise": request["premise"], "progression_kernel": {}},
        stage="CORE_INNOVATION_PROPOSAL",
        book_id="closure-original",
    )

    assert handoff["handoff_id"]
    assert context["status"] == "ENABLED"
    assert context["usage"] == "REFERENCE_ONLY"
    assert context["selected_card_count"] == 2
    assert set(context["selected_card_ids"]) == {"mechanism-closure", "contrast-closure"}
    assert context["machine_bundle_hash"]
    assert context["snapshot_id"]
    assert context["compact_cards"]
    assert "observation_summary" not in json.dumps(context, ensure_ascii=False)


def test_continuation_candidate_task_freezes_enabled_planning_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_root = _write_machine_package(tmp_path / "corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(corpus_root))
    database, settings = _setup_continuation_book(tmp_path)
    task = prepare_candidate_task(database, "closure-continuation", settings)
    task_payload = json.loads(
        (Path(str(task["input"])).parent / "task.json").read_text(encoding="utf-8")
    )
    context = task_payload["reference_planning_context"]

    assert context["status"] == "ENABLED"
    assert context["usage"] == "REFERENCE_ONLY"
    assert context["selected_card_count"] == 2
    assert set(context["selected_card_ids"]) == {"mechanism-closure", "contrast-closure"}
    assert context["machine_bundle_hash"]
    assert context["snapshot_id"]
    assert Path(str(task_payload["reference_context_snapshot"])).is_file()


def test_revision_strategy_chain_uses_selected_cards_and_draft_task(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_root = _write_machine_package(tmp_path / "corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(corpus_root))
    database = _setup_revision_book(tmp_path)

    # Planning cards and prose controls have different query dimensions.  The
    # production planner must therefore keep target scene functions for the
    # later PROSE query, but not use them to filter PLANNING cards.
    from novel_authoring.revision import service as revision_service

    real_query = query_reference_corpus
    captured_requests: list[ReferenceCorpusQueryRequest] = []

    def query_for_closure(
        request: ReferenceCorpusQueryRequest, *, corpus_root: Path | None = None
    ) -> ReferenceCorpusQueryResponse:
        captured_requests.append(request)
        return real_query(request, corpus_root=corpus_root)

    monkeypatch.setattr(revision_service, "query_reference_corpus", query_for_closure)
    campaign = create_revision_campaign(
        database,
        "closure-revision",
        _revision_spec(),
        edition_id="edition-r1",
    )
    campaign_id = str(campaign["campaign_id"])
    impact = build_revision_impact(database, "closure-revision", campaign_id)
    complete_revision_impact_audit(
        database,
        "closure-revision",
        campaign_id,
        [
            {"impact_id": item["impact_id"], "status": "HANDLED"}
            for item in impact["items"]
        ],
    )
    plan = build_revision_plan(database, "closure-revision", campaign_id)
    planning_context = plan["reference_planning_context"]
    assert planning_context["status"] == "ENABLED"
    assert set(planning_context["selected_card_ids"]) == {
        "mechanism-closure",
        "contrast-closure",
    }
    assert planning_context["snapshot_id"]
    planning_snapshot = load_reference_context_snapshot(
        Path(str(planning_context["snapshot_path"]))
    )
    assert planning_snapshot.machine_bundle_hash

    unit = plan["units"][0]
    strategy = plan["strategies"][str(unit["unit_id"])]
    # The deterministic plan may carry a no-card fallback, but enabled cards
    # require the explicit selector-import boundary before draft preparation.
    assert strategy["reference_card_ids_used"] == []
    assert strategy["selected_contrast_solutions"] == []
    assert strategy["planning_snapshot_id"] == planning_context["snapshot_id"]
    assert strategy["planning_snapshot_hash"] == planning_context["snapshot_hash"]
    assert strategy["usage"] == "REFERENCE_ONLY"
    assert "semantic selector" in strategy["strategy_summary"]
    assert strategy["structural_moves"]

    with pytest.raises(
        RevisionWorkflowError, match="REVISION_STRATEGY_SELECTION_PENDING"
    ):
        prepare_revision_draft_task(
            database,
            "closure-revision",
            campaign_id,
            str(unit["unit_id"]),
        )

    selector_output_path = Path(str(plan["strategy_selection"]["expected_output"]))
    selector_output_path.write_text(
        json.dumps(
            {
                "task_type": "REVISION_STRATEGY_SELECTION",
                "task_id": plan["planning_provenance"]["task_id"],
                "campaign_id": campaign_id,
                "edition_id": plan["planning_provenance"]["edition_id"],
                "planning_snapshot_id": planning_snapshot.snapshot_id,
                "planning_snapshot_hash": planning_snapshot.snapshot_hash,
                "strategies": {str(unit["unit_id"]): strategy},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    imported = import_revision_strategy_selection(
        database,
        "closure-revision",
        campaign_id,
        selector_output_path,
    )
    assert imported["status"] == "IMPORTED"

    task = prepare_revision_draft_task(
        database,
        "closure-revision",
        campaign_id,
        str(unit["unit_id"]),
    )
    task_payload = json.loads(Path(str(task["task_path"])).read_text(encoding="utf-8"))
    assert task_payload["revision_strategy"]["reference_card_ids_used"] == strategy[
        "reference_card_ids_used"
    ]
    assert task_payload["planning_provenance"]["planning_snapshot_id"] == planning_context[
        "snapshot_id"
    ]
    assert task_payload["reference_prose_context"]["status"] == "ENABLED"
    assert task_payload["reference_prose_context"]["controls"][0]["control_topic"] == "动作先于解释"
    input_text = Path(str(task["input_markdown"])).read_text(encoding="utf-8")
    assert "Revision Strategy（REFERENCE_ONLY；只描述 HOW）" in input_text
    assert "Reference Corpus Prose Controls" in input_text
    assert captured_requests
    assert any(getattr(request, "purpose", None) == "PLANNING" for request in captured_requests)
    assert any(getattr(request, "purpose", None) == "PROSE" for request in captured_requests)
    planning_requests = [
        request for request in captured_requests if request.purpose == "PLANNING"
    ]
    assert planning_requests and planning_requests[0].scene_functions == []


def test_normal_draft_task_consumes_enabled_prose_controls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_root = _write_machine_package(tmp_path / "corpus")
    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(corpus_root))
    database, contract = _setup_draft_book(tmp_path)
    task = prepare_draft_task(database, "closure-draft", contract.contract_id)
    task_payload = json.loads(
        (Path(str(task["input"])).parent / "task.json").read_text(encoding="utf-8")
    )
    context = task_payload["reference_prose_context"]

    assert context["status"] == "ENABLED"
    assert context["selected_card_ids"] == ["prose-control-closure"]
    assert context["selected_card_count"] == 1
    assert context["machine_bundle_hash"]
    assert context["snapshot_id"]
    input_text = Path(str(task["input"])).read_text(encoding="utf-8")
    assert "Reference Corpus Prose Controls（REFERENCE_ONLY soft context）" in input_text
    assert "动作先于解释" in input_text


@pytest.mark.parametrize(
    ("case", "expected_status"),
    [
        ("not-ready", "UNAVAILABLE"),
        ("zero", "ZERO_RESULTS"),
        ("unavailable", "UNAVAILABLE"),
        ("corrupt", "CORRUPT"),
    ],
)
def test_original_authoring_soft_fails_without_reference_corpus(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
    expected_status: str,
) -> None:
    if case == "not-ready":
        root = _write_machine_package(tmp_path / "corpus", query_ready=False)
    elif case == "zero":
        root = _write_machine_package(tmp_path / "corpus", records=[_prose_control_card()])
    elif case == "corrupt":
        root = _write_machine_package(tmp_path / "corpus")
        (root / "machine" / "cards.jsonl").write_text("{broken\n", encoding="utf-8")
    else:
        root = tmp_path / "missing-corpus"

    monkeypatch.setenv("NOVEL_REFERENCE_CORPUS_ROOT", str(root))
    created = create_original_book(
        BookLayout(tmp_path / "library"),
        {"premise": f"Reference Corpus {case} 不可用时仍应创建作者任务。"},
        book_id=f"closure-soft-fail-{case}",
    )
    database = Database(Path(str(created["database"])))
    handoff = get_handoff(database, str(created["reader_handoff"]["handoff_id"]))
    task_directory = Path(str(handoff["task_directory"]))
    request = json.loads(
        (task_directory / "input" / "original_request.json").read_text(encoding="utf-8")
    )

    assert handoff["handoff_id"]
    context = original_service._original_reference_planning_context(
        {"premise": request["premise"], "progression_kernel": {}},
        stage="CORE_INNOVATION_PROPOSAL",
        book_id=f"closure-soft-fail-{case}",
    )
    assert context["status"] == expected_status
    assert context["selected_card_count"] == 0
    assert context["usage"] == "REFERENCE_ONLY"
