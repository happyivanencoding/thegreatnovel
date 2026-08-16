from __future__ import annotations

import json
import os
from contextlib import suppress
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from novel_authoring.config import load_settings
from novel_authoring.context.router import (
    ContextPurpose,
    RuntimeContextRequest,
    route_runtime_context,
)
from novel_authoring.contracts.draft import (
    ChapterRealizationBrief,
    DraftCreativeOutput,
    DraftOutput,
)
from novel_authoring.db.database import Database
from novel_authoring.domain.models import DraftStatus
from novel_authoring.drafting.compiler import (
    build_chapter_realization_brief,
    compile_draft_output,
)
from novel_authoring.edition import edition_workspace, resolve_edition_id
from novel_authoring.planning.boundary import _workspace
from novel_authoring.planning.models import ChapterContract
from novel_authoring.planning.rewards import (
    calculate_realized_innovation_reward,
    detect_semantic_policy_leak,
)
from novel_authoring.reference_corpus.context import (
    ReferenceContextSnapshot,
    freeze_reference_context,
    load_reference_context_snapshot,
)
from novel_authoring.reference_corpus.query import (
    ReferenceCorpusQueryRequest,
    query_reference_corpus,
)
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.operations import book_root, ensure_operation, find_operation
from novel_authoring.utils import json_dumps, sha256_bytes, sha256_file, stable_id, utc_now


class DraftWorkflowError(RuntimeError):
    pass


def _healthy_realization_lengths(
    database: Database, book_id: str, edition_id: str
) -> list[int]:
    """Read only healthy, already-reviewed drafts for the next soft baseline."""

    lengths: list[int] = []
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT output_json, status FROM drafts "
            "WHERE book_id=? AND edition_id=? "
            "AND status IN ('VALIDATED', 'AUTHOR_APPROVED', 'CANON_COMMITTED') "
            "ORDER BY created_at DESC",
            (book_id, edition_id),
        ).fetchall()
    for row in rows:
        try:
            output = json.loads(str(row["output_json"] or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        if not isinstance(output, dict):
            continue
        diagnostics = output.get("realization_diagnostics")
        if not isinstance(diagnostics, dict):
            continue
        code = str(diagnostics.get("code") or "")
        accepted_short = bool(output.get("intentional_short_chapter")) or (
            str(diagnostics.get("status") or "").upper() == "ACCEPTED"
        )
        if (
            code not in {"SCENE_REALIZATION_CLEAR", "SCENE_REALIZATION_ACCEPTED"}
            and not accepted_short
        ):
            continue
        prose = str(output.get("prose_markdown") or "").strip()
        if prose:
            lengths.append(len(prose))
    return lengths


_PROSE_CONTROL_FIELDS = (
    "card_id",
    "card_type",
    "control_topic",
    "applicable_scene_functions",
    "guidance",
    "variants",
    "when_to_use",
    "failure_signals",
    "transfer_boundary",
)

_PROSE_REALIZATION_PROTOCOL = {
    "shared_with": "Revision Draft Novel Prose Realization",
    "authority": "Chapter Contract > Canon > Current Scene Context > Prose Controls",
    "controls_may_change": [
        "句法、段落节奏、信息呈现、对话自然度、描写与场景收束"
    ],
    "controls_must_not_change": [
        "Chapter Contract、Boundary、Canon、事件顺序、人物选择、资源、知识边界、"
        "事实、payoff、不可逆改变或结尾状态"
    ],
    "thin_scene_repair": {
        "maximum_attempts": 1,
        "scope": "REALIZATION_ONLY",
        "must_not_change": [
            "state_changes、abilities、resources、Chapter Contract 或 ending_state"
        ],
    },
}


def _soft_reference_prose_context(
    snapshot_path: Path,
    *,
    status: str,
    warning: str,
    knowledge_gap: str,
) -> dict[str, object]:
    return {
        "purpose": "PROSE",
        "status": status,
        "controls": [],
        "warnings": [warning],
        "knowledge_gaps": [knowledge_gap],
        "snapshot_id": None,
        "snapshot_hash": None,
        "snapshot_path": str(snapshot_path),
        "selected_card_count": 0,
        "machine_bundle_hash": None,
        "selected_card_ids": [],
        "selected_card_types": [],
        "usage": "REFERENCE_ONLY",
    }


def _prose_scene_functions(contract: ChapterContract) -> list[str]:
    """Map frozen contract functions to the small PROSE query vocabulary."""

    aliases = {
        "setup": ["OPENING"],
        "pressure_build": ["ACTION"],
        "choice": ["ACTION", "DIALOGUE"],
        "discovery": ["DISCOVERY", "EXPLORATION"],
        "progress": ["ACTION"],
        "partial_payoff": ["PAYOFF"],
        "major_payoff": ["PAYOFF"],
        "reversal": ["ACTION"],
        "aftershock": ["AFTERMATH"],
        "recovery": ["AFTERMATH"],
        "relationship_shift": ["DIALOGUE", "RELATIONSHIP_SHIFT"],
        "world_expansion": ["EXPOSITION", "EXPLORATION"],
    }
    functions: list[str] = []
    for value in [contract.primary_function, *contract.secondary_functions]:
        functions.extend(aliases.get(value.value, [value.value]))
    return list(dict.fromkeys(functions))


def _reference_prose_context(
    contract: ChapterContract,
    *,
    book_id: str,
    edition_id: str,
    operation_id: str,
    snapshot_path: Path,
) -> dict[str, object]:
    """Return compact optional prose guidance without touching the Draft schema."""

    def from_snapshot(snapshot: ReferenceContextSnapshot) -> dict[str, object]:
        controls = [
            {key: card[key] for key in _PROSE_CONTROL_FIELDS if key in card}
            for card in snapshot.compact_cards
            if card.get("card_type") == "prose-control"
        ]
        warnings = list(snapshot.warnings)
        legacy_unavailable = snapshot.status == "ENABLED" and any(
            "corrupt package" in warning.casefold() for warning in warnings
        )
        status = "UNAVAILABLE" if legacy_unavailable else snapshot.status
        return {
            "purpose": snapshot.purpose,
            "status": status,
            "controls": controls,
            "warnings": warnings,
            "knowledge_gaps": list(snapshot.knowledge_gaps),
            "snapshot_id": snapshot.snapshot_id,
            "snapshot_hash": snapshot.snapshot_hash,
            "snapshot_path": str(snapshot_path),
            "selected_card_count": snapshot.selected_card_count,
            "package_schema_version": snapshot.package_schema_version,
            "machine_bundle_hash": snapshot.machine_bundle_hash,
            "selected_card_ids": snapshot.selected_card_ids,
            "selected_card_types": snapshot.selected_card_types,
            "usage": snapshot.usage,
        }

    if snapshot_path.is_file():
        try:
            # The Core loader is the only authority allowed to read an existing
            # frozen snapshot.  It verifies the stored hash before returning it.
            return from_snapshot(load_reference_context_snapshot(snapshot_path))
        except (OSError, UnicodeError, TypeError, ValueError) as exc:
            return _soft_reference_prose_context(
                snapshot_path,
                status="CORRUPT",
                warning=(
                    "soft-fail：Reference Context Snapshot 未通过 Core loader 校验："
                    f"{type(exc).__name__}: {exc}"
                ),
                knowledge_gap="冻结的 Reference Context Snapshot 不可可靠读取",
            )

    configured_root: Path | None = None
    with suppress(OSError, TypeError, ValueError):
        configured_root = load_settings().reference_corpus_root
    configured = configured_root is not None or bool(
        os.environ.get("NOVEL_REFERENCE_CORPUS_ROOT", "").strip()
    )
    request = ReferenceCorpusQueryRequest(
        purpose="PROSE",
        creative_problem="",
        scene_functions=_prose_scene_functions(contract),
        max_cards=4,
    )
    try:
        response = query_reference_corpus(request, corpus_root=configured_root)
        if not configured and response.status == "ENABLED":
            response = response.model_copy(
                update={
                    "status": "DISABLED",
                    "package_schema_version": None,
                    "package_hash": None,
                    "machine_bundle_hash": None,
                    "cards": [],
                    "knowledge_gaps": [
                        "当前没有可用的 Reference Corpus machine package/path"
                    ],
                    "warnings": ["soft-fail：Reference Corpus 未启用或未配置"],
                }
            )
        snapshot = freeze_reference_context(
            request,
            response,
            book_id=book_id,
            edition_id=edition_id,
            operation_id=operation_id,
            output_path=snapshot_path,
        )
    except (OSError, UnicodeError, TypeError, ValueError) as exc:
        return _soft_reference_prose_context(
            snapshot_path,
            status="UNAVAILABLE",
            warning=(
                "soft-fail：Reference Corpus Query/Freeze 未完成："
                f"{type(exc).__name__}: {exc}"
            ),
            knowledge_gap="Reference Corpus prose context 未能冻结",
        )
    return from_snapshot(snapshot)


def prepare_draft_task(
    database: Database,
    book_id: str,
    contract_id: str,
    *,
    edition_id: str | None = None,
    include_runtime_state: bool = True,
) -> dict[str, object]:
    database.initialize()
    selected_edition = resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM chapter_contracts WHERE book_id=? AND contract_id=? AND edition_id=?",
            (book_id, contract_id, selected_edition),
        ).fetchone()
        if row is None:
            raise DraftWorkflowError(f"章节合同不存在：{contract_id}")
        if row["status"] != "READY":
            raise DraftWorkflowError(f"章节合同状态不可写作：{row['status']}")
        revision = (
            int(
                connection.execute(
                    """
                    SELECT COUNT(*) FROM drafts
                    WHERE book_id=? AND contract_id=? AND edition_id=?
                    """,
                    (book_id, contract_id, selected_edition),
                ).fetchone()[0]
            )
            + 1
        )
    if revision > 3:
        raise DraftWorkflowError("同一章节合同最多允许初稿加两轮修订")
    contract = ChapterContract.model_validate_json(str(row["contract_json"]))
    workspace = edition_workspace(database, book_id, selected_edition)
    root = book_root(database, book_id)
    boundary_dir = (
        BookLayout(root.parent).for_book(book_id).edition(selected_edition).boundaries
        if (root / "book.yaml").is_file()
        else workspace / "boundaries"
    )
    boundary_path = boundary_dir / f"{contract.boundary_packet_id}.md"
    if not boundary_path.exists():
        raise DraftWorkflowError("Boundary Packet 不存在，禁止准备正文任务")
    boundary_json_path = boundary_path.with_suffix(".json")
    boundary_payload = (
        json.loads(boundary_json_path.read_text(encoding="utf-8"))
        if boundary_json_path.is_file()
        else {}
    )
    runtime_context = route_runtime_context(
        database,
        book_id,
        edition_id=selected_edition,
        purpose=ContextPurpose.DRAFT,
        request=RuntimeContextRequest(
            purpose=ContextPurpose.DRAFT,
            include_runtime_state=include_runtime_state,
        ),
        boundary=boundary_payload,
    )
    schema_json = json_dumps(DraftCreativeOutput.model_json_schema(), indent=2)
    task_id = stable_id("draft-task", contract_id, str(revision), str(row["contract_sha256"]))
    operation = ensure_operation(
        database,
        book_id,
        selected_edition,
        task_id,
        "DRAFT",
        {"contract_id": contract_id, "revision": revision},
    )
    task_dir = (
        operation.input
        if operation is not None
        else workspace / "agent_tasks" / task_id
    )
    output_dir = (
        operation.output
        if operation is not None
        else workspace / "agent_outputs" / task_id
    )
    task_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    reference_prose_context = _reference_prose_context(
        contract,
        book_id=book_id,
        edition_id=selected_edition,
        operation_id=task_id,
        snapshot_path=task_dir / "reference_context_snapshot.json",
    )
    reference_prose_section = (
        [
            "## Reference Corpus Prose Controls（REFERENCE_ONLY soft context）",
            "",
            "以下内容只影响表达方式，不得改变 Chapter Contract、Canon、Boundary、状态、选择、"
            "事件顺序、线索、payoff、不可逆改变或结尾状态；发生冲突时丢弃 Prose Guidance。",
            "当前书 Prose DNA 与作者明确风格意图优先于外部 Reference Corpus Prose Controls。",
            "",
            "```json",
            json_dumps(reference_prose_context, indent=2),
            "```",
            "",
        ]
        if reference_prose_context["status"] != "DISABLED" else []
    )
    recent_lengths = _healthy_realization_lengths(
        database, book_id, selected_edition
    )
    realization_brief = build_chapter_realization_brief(
        contract,
        recent_lengths=recent_lengths,
    )
    input_text = "\n".join(
        [
            f"# 章节正文任务 `{task_id}`",
            "",
            f"revision: {revision}",
            "",
            "严格依据下面的 Boundary Packet 与 Chapter Contract 写正文。",
            "正文不得声明新事实已自动进入正史；state_changes 只声明正文实际发生的状态变化。",
            "可选 reader_visible_claims 只填写正文中读者能直接观察到的高价值声明；"
            "每条声明带 subject_ref、predicate、value 或 before/after，并提供 evidence_quote；"
            "不要把自然语言推断写成声明。",
            "可选 progression_deltas 必须区分 REUSE/SHOWCASE 与 UPGRADE/BREAKTHROUGH；"
            "成长变化要写 before_state、after_state、reader_visible_delta，突破要说明新增行动空间、"
            "范围或可靠性。资源/能力的 usage_constraints 必须写在对应 StateChange payload 中，"
            "新章节不会自动复位 DAILY、COMBAT_SCENE、RESOURCE_GATED 或 ONE_TIME。",
            "不要填写 contract_evidence、evidence_quotes、character_fit_inputs、"
            "style_fit_inputs、structure_tags、RealizedKernelTrace 或系统评分；"
            "这些由 Python 编译。",
            "按 Chapter Contract 中冻结的 InnovationControl 执行；它只改变创作距离，"
            "不改变 Canon、Timeline、Knowledge、Capability、Resource、Approval 或 "
            "Edition hard gates。",
            f"Creative-distance guidance：{contract.innovation_control.creative_distance_guidance}",
            "Lens tendency："
            f"{contract.innovation_control.lens_tendency_guidance}；不得把它写成 Score Bonus。",
            "Canon、Timeline、Knowledge、Capability、Resource 与 Approval 的硬约束由系统内核、"
            "Chapter Contract 和 Validator 负责；正文只写人物如何感知、选择、行动及其后果，"
            "不解释这些治理规则。",
            "本章至少让一个重要状态发生可读的改变；未知可以保留，但若核心谜团继续悬置，"
            "必须推进或兑现另一条 SHORT/MID 线程。",
            "Reveal Agenda 由系统保留；reveal_trace.planned 可省略或只记录本次实际采用的计划，"
            "realized 只记录正文真正发生的线索或揭示，且 evidence_quote 必须出现在正文中。"
            "KEEP_HIDDEN 的 Truth 只能约束行为，不能被旁白、对话或解释直接说破；"
            "HINT 必须留下读者可感知线索，但不能确认完整答案。",
            "系统会从正文、实际 StateChange、Chapter Contract、Reveal 与 promises"
            "自动编译实际 trace；不要把 Expected Kernel Trace 或系统审计字段写进正文输出。",
            "避免连续使用‘谨慎试探—暂不下结论—保留退路—撤回’的审计型叙事，"
            "除非当前 Narrative Portfolio 明确需要这种节奏。",
            "只写 output.json，不要修改 book；系统会把合法正文导入 drafts。",
            "",
            "## Chapter Realization Brief（soft guidance）",
            "",
            "以下范围只用于调节场景展开，不是最低字数硬门；可以用更短或更长的自然场景，"
            "但不得用摘要跳过关键动作、反应与后果。允许 realization-only micro-event，"
            "不得改变 Contract、Canon、Knowledge、Resource 或 Capability。",
            "```json",
            json_dumps(realization_brief.model_dump(mode="json"), indent=2),
            "```",
            "",
            "## Novel Prose Realization Protocol（Normal Draft / Revision Draft shared）",
            "",
            "Novel Prose Realization 只控制表达层；Chapter Contract、Canon、Boundary、"
            "人物事实、资源、知识边界、事件顺序、payoff 与结尾状态保持不变。",
            "```json",
            json_dumps(_PROSE_REALIZATION_PROTOCOL, indent=2),
            "```",
            "",
            "## Continuation Boundary Packet",
            "",
            boundary_path.read_text(encoding="utf-8"),
            "",
            "## Chapter Contract",
            "",
            "```json",
            str(row["contract_json"]),
            "```",
            "",
            *reference_prose_section,
            "## Runtime Context Router（hard boundary + earned surface + soft controls）",
            "",
            "```json",
            json_dumps(runtime_context.model_dump(mode="json"), indent=2),
            "```",
            "",
            (
                "本次是 Planning-only Runtime 消融：Draft 阶段不得读取 raw Runtime Baseline、"
                "Earned Surface 或 Effective Runtime 表；只使用 Contract、最近正文和 "
                "style/dialogue/narrative controls。"
                if not include_runtime_state
                else "本次是 Full Runtime Draft：Runtime 只能影响角色行动和规划兑现，"
                "不得把工程字段写进小说正文。"
            ),
        ]
    )
    metadata = {
        "task_id": task_id,
        "task_type": "draft",
        "book_id": book_id,
        "edition_id": selected_edition,
        "contract_id": contract_id,
        "revision": revision,
        "boundary_packet_id": contract.boundary_packet_id,
        "base_event_seq": contract.continuation_boundary["base_event_seq"],
        "base_projection_hash": contract.continuation_boundary["base_projection_hash"],
        "schema_sha256": sha256_bytes(schema_json.encode()),
        "created_at": utc_now(),
        "runtime_context": runtime_context.model_dump(mode="json"),
        "include_runtime_state": include_runtime_state,
        "runtime_ablation": "FULL_RUNTIME" if include_runtime_state else "PLANNING_ONLY",
        "raw_runtime_tables_loaded": include_runtime_state,
        "innovation_control": contract.innovation_control.model_dump(mode="json"),
        "reference_prose_context": reference_prose_context,
        "reference_context_snapshot": str(task_dir / "reference_context_snapshot.json"),
        "prose_realization_protocol": _PROSE_REALIZATION_PROTOCOL,
        "chapter_realization_brief": realization_brief.model_dump(mode="json"),
        "output_contract": "DraftCreativeOutput",
    }
    (task_dir / "input.md").write_text(input_text, encoding="utf-8")
    (task_dir / "schema.json").write_text(schema_json + "\n", encoding="utf-8")
    (task_dir / "task.json").write_text(json_dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return {
        "task_id": task_id,
        "contract_id": contract_id,
        "revision": revision,
        "input": str(task_dir / "input.md"),
        "schema": str(task_dir / "schema.json"),
        "expected_output": str(output_dir / "output.json"),
    }


def import_draft_output(
    database: Database,
    book_id: str,
    task_id: str,
    output_path: Path | None = None,
    *,
    edition_id: str | None = None,
) -> dict[str, object]:
    database.initialize()
    workspace = _workspace(database, book_id)
    if edition_id is not None:
        workspace = edition_workspace(database, book_id, edition_id)
    operation = find_operation(database, book_id, edition_id or "base", task_id)
    task_path = (
        operation.input / "task.json"
        if operation is not None
        else workspace / "agent_tasks" / task_id / "task.json"
    )
    if not task_path.exists() and edition_id is None:
        candidates = list((workspace / "editions").glob(f"*/agent_tasks/{task_id}/task.json"))
        if candidates:
            task_path = candidates[0]
            workspace = task_path.parents[2]
    if not task_path.exists():
        raise DraftWorkflowError(f"正文任务不存在：{task_id}")
    metadata = json.loads(task_path.read_text(encoding="utf-8"))
    selected_edition = str(metadata.get("edition_id", "base"))
    workspace = edition_workspace(database, book_id, selected_edition)
    operation = find_operation(database, book_id, selected_edition, task_id)
    task_path = (
        operation.input / "task.json"
        if operation is not None
        else workspace / "agent_tasks" / task_id / "task.json"
    )
    metadata = json.loads(task_path.read_text(encoding="utf-8"))
    path = output_path or (
        operation.output / "output.json"
        if operation is not None
        else workspace / "agent_outputs" / task_id / "output.json"
    )
    creative_output: DraftCreativeOutput | None = None
    output: DraftOutput | None = None
    try:
        raw_payload = json.loads(path.read_text(encoding="utf-8"))
        try:
            creative_output = DraftCreativeOutput.model_validate(raw_payload)
            output = None
        except ValidationError as creative_error:
            # Existing persisted/local fixtures are internal DraftOutput
            # artifacts, not the schema exposed to a new executor.  Keep this
            # narrow read path so already-created work remains importable while
            # prepare_draft_task only publishes DraftCreativeOutput.
            legacy_keys = {
                "contract_evidence",
                "character_fit_inputs",
                "style_fit_inputs",
                "structure_tags",
                "realized_kernel_trace",
                "innovation_trace",
                "direction_alignment",
            }
            if not isinstance(raw_payload, dict) or not legacy_keys.intersection(raw_payload):
                raise creative_error
            output = DraftOutput.model_validate(raw_payload)
    except (OSError, TypeError, ValueError, ValidationError) as exc:
        raise DraftWorkflowError(f"Draft output 不符合合同：{exc}") from exc
    if creative_output is None:
        assert output is not None
        submitted_task_id = output.task_id
        submitted_contract_id = output.contract_id
    else:
        submitted_task_id = creative_output.task_id
        submitted_contract_id = creative_output.contract_id
    if submitted_task_id != task_id or submitted_contract_id != metadata["contract_id"]:
        raise DraftWorkflowError("Draft output 的 task_id/contract_id 不匹配")
    contract_row = None
    candidate_plan_row = None
    with database.connect() as connection:
        contract_row = connection.execute(
            "SELECT contract_json FROM chapter_contracts WHERE contract_id=? AND book_id=?",
            (submitted_contract_id, book_id),
        ).fetchone()
        if contract_row is not None:
            contract_payload = json.loads(str(contract_row["contract_json"]))
            candidate_plan_row = connection.execute(
                "SELECT plan_json, score_json FROM candidate_plans "
                "WHERE book_id=? AND candidate_id=? AND edition_id=?",
                (
                    book_id,
                    str(contract_payload.get("candidate_id", "")),
                    selected_edition,
                ),
            ).fetchone()
    if creative_output is not None:
        contract = (
            ChapterContract.model_validate_json(str(contract_row["contract_json"]))
            if contract_row is not None
            else None
        )
        brief = None
        raw_brief = metadata.get("chapter_realization_brief")
        if isinstance(raw_brief, dict):
            try:
                brief = ChapterRealizationBrief.model_validate(raw_brief)
            except ValidationError:
                brief = None
        output = compile_draft_output(
            creative_output,
            contract,
            realization_brief=brief,
        )
    assert output is not None
    realized_reward_payload: dict[str, object] | None = None
    if contract_row is not None:
        contract = ChapterContract.model_validate_json(str(contract_row["contract_json"]))
        expected = contract.innovation_control
        if output.innovation_control is not None and output.innovation_control != expected:
            raise DraftWorkflowError(
                "Draft output 的 innovation_control 与 Chapter Contract 不一致"
            )
        if output.innovation_trace is not None:
            base_score = 0.0
            expected_reward = 0.0
            if candidate_plan_row is not None:
                score_payload = json.loads(str(candidate_plan_row["score_json"] or "{}"))
                base_score = float(score_payload.get("base_candidate_score", 0))
                expected_reward = float(
                    score_payload.get("innovation_reward_breakdown", {})
                    .get("capped_innovation_reward", 0)
                )
            realized = calculate_realized_innovation_reward(
                output.innovation_trace,
                expected,
                base_candidate_score=base_score,
                portfolio=contract.narrative_portfolio,
            )
            realized_reward_payload = {
                "expected_capped_reward": expected_reward,
                "realized": realized.model_dump(mode="json"),
                "innovation_underdelivery": {
                    "status": (
                        "INNOVATION_UNDERDELIVERY"
                        if realized.capped_innovation_reward + 0.5 < expected_reward
                        else "CLEAR"
                    ),
                    "warning_only": True,
                },
            }
    content = output.prose_markdown.strip() + "\n"
    content_hash = sha256_bytes(content.encode())
    draft_id = stable_id("draft", output.contract_id, str(metadata["revision"]), content_hash)
    drafts_dir = workspace / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    draft_path = drafts_dir / f"{draft_id}.md"
    draft_path.write_bytes(content.encode("utf-8"))
    with database.connect() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO drafts(
                draft_id, book_id, contract_id, candidate_id, file_path,
                content_sha256, status, revision, created_at, task_id, edition_id,
                chapter_title, output_json, base_event_seq, base_projection_hash
            )
            SELECT ?, ?, ?, candidate_id, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            FROM chapter_contracts WHERE contract_id=? AND book_id=? AND edition_id=?
            """,
            (
                draft_id,
                book_id,
                output.contract_id,
                str(draft_path),
                content_hash,
                DraftStatus.DRAFT.value,
                int(metadata["revision"]),
                utc_now(),
                task_id,
                selected_edition,
                output.chapter_title,
                json_dumps(output.model_dump(mode="json")),
                int(metadata["base_event_seq"]),
                str(metadata["base_projection_hash"]),
                output.contract_id,
                book_id,
                selected_edition,
            ),
        )
        exists = connection.execute("SELECT 1 FROM drafts WHERE draft_id=?", (draft_id,)).fetchone()
    if exists is None:
        raise DraftWorkflowError("无法关联章节合同，草稿未导入")
    return {
        "draft_id": draft_id,
        "path": str(draft_path),
        "status": DraftStatus.DRAFT.value,
        "revision": int(metadata["revision"]),
        "content_sha256": content_hash,
        "semantic_policy_leak": detect_semantic_policy_leak(
            output.prose_markdown
        ).model_dump(mode="json"),
        "realized_innovation_reward": realized_reward_payload,
    }


def show_draft(
    database: Database,
    book_id: str,
    draft_id: str,
    *,
    edition_id: str | None = None,
) -> dict[str, object]:
    selected_edition = resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM drafts WHERE book_id=? AND draft_id=? AND edition_id=?",
            (book_id, draft_id, selected_edition),
        ).fetchone()
        reports = connection.execute(
            """
            SELECT validator, severity, passed, report_json
            FROM validation_reports
            WHERE book_id=? AND edition_id=? AND draft_id=?
              AND run_id=(
                  SELECT validation_run_id FROM drafts
                  WHERE book_id=? AND edition_id=? AND draft_id=?
              )
            ORDER BY validator
            """,
            (
                book_id,
                selected_edition,
                draft_id,
                book_id,
                selected_edition,
                draft_id,
            ),
        ).fetchall()
    if row is None:
        raise DraftWorkflowError(f"草稿不存在：{draft_id}")
    return {
        "draft_id": draft_id,
        "status": row["status"],
        "revision": row["revision"],
        "path": row["file_path"],
        "content_sha256": row["content_sha256"],
        "content": Path(str(row["file_path"])).read_text(encoding="utf-8"),
        "validation": [
            {
                "validator": report["validator"],
                "severity": report["severity"],
                "passed": bool(report["passed"]),
                "report": json.loads(str(report["report_json"])),
            }
            for report in reports
        ],
    }


def save_draft_content(
    database: Database,
    book_id: str,
    draft_id: str,
    content: str,
    *,
    edition_id: str | None = None,
    expected_content_sha256: str | None = None,
) -> dict[str, object]:
    """Persist an author edit while keeping the draft outside Canon.

    Saving invalidates validation reports and returns the draft to ``DRAFT``.
    It never changes chapters, events, projections, editions, or approval state.
    """

    selected_edition = edition_id or resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM drafts WHERE book_id=? AND draft_id=? AND edition_id=?",
            (book_id, draft_id, selected_edition),
        ).fetchone()
        if row is None:
            raise DraftWorkflowError(f"草稿不存在：{draft_id}")
        if row["status"] in {
            DraftStatus.AUTHOR_APPROVED.value,
            DraftStatus.CANON_COMMITTED.value,
        }:
            raise DraftWorkflowError("已批准或已提交草稿不可直接编辑")
        if (
            expected_content_sha256 is not None
            and str(row["content_sha256"]) != expected_content_sha256
        ):
            raise DraftWorkflowError("草稿已被其他操作修改，请重新加载后再保存")

        draft_path = Path(str(row["file_path"])).expanduser().resolve()
        edition_root = edition_workspace(database, book_id, selected_edition).resolve()
        drafts_root = (edition_root / "drafts").resolve()
        if drafts_root not in draft_path.parents:
            raise DraftWorkflowError("草稿路径不在当前 edition 的 drafts 目录")
        if not content.strip():
            raise DraftWorkflowError("Draft 正文不能为空")

        try:
            output = json.loads(str(row["output_json"] or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise DraftWorkflowError("草稿 output_json 无法读取") from exc
        if not isinstance(output, dict):
            raise DraftWorkflowError("草稿 output_json 必须是 object")
        repair_count = int(output.get("realization_repair_count") or 0)
        if repair_count >= 1:
            raise DraftWorkflowError(
                "SCENE_REALIZATION_THIN 只允许一次 realization-only repair"
            )

        normalized = content if content.endswith("\n") else content + "\n"
        draft_path.write_text(normalized, encoding="utf-8")
        content_hash = sha256_file(draft_path)
        output["prose_markdown"] = normalized.rstrip("\n")
        output["realization_repair_count"] = repair_count + 1
        previous_trace = output.get("reveal_trace")
        if isinstance(previous_trace, dict):
            output["reveal_trace"] = {
                "planned": list(previous_trace.get("planned", [])),
                "realized": [],
                "knowledge_transitions": [],
            }
            notes = output.get("notes")
            if not isinstance(notes, list):
                notes = []
            notes.append("正文已手动编辑；旧 Reveal realized trace 已失效，必须重新声明。")
            notes.append(
                "正文只允许一次 realization-only repair；不得新增 StateChange、资源或能力。"
            )
            output["notes"] = notes
        connection.execute(
            """
            UPDATE drafts
            SET content_sha256=?, status=?, output_json=?, validation_run_id=NULL,
                version=version+1
            WHERE book_id=? AND draft_id=? AND edition_id=?
            """,
            (
                content_hash,
                DraftStatus.DRAFT.value,
                json_dumps(output),
                book_id,
                draft_id,
                selected_edition,
            ),
        )
        connection.execute(
            "DELETE FROM validation_reports WHERE book_id=? AND draft_id=?",
            (book_id, draft_id),
        )
    return {
        "draft_id": draft_id,
        "edition_id": selected_edition,
        "status": DraftStatus.DRAFT.value,
        "content_sha256": content_hash,
        "validation_invalidated": True,
    }


def repair_draft_metadata(
    database: Database,
    book_id: str,
    draft_id: str,
    metadata: dict[str, Any],
    *,
    edition_id: str | None = None,
    expected_content_sha256: str | None = None,
) -> dict[str, object]:
    """Repair DraftOutput metadata without changing the persisted prose bytes."""

    selected_edition = resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM drafts WHERE book_id=? AND draft_id=? AND edition_id=?",
            (book_id, draft_id, selected_edition),
        ).fetchone()
        if row is None:
            raise DraftWorkflowError(f"草稿不存在：{draft_id}")
        if row["status"] in {
            DraftStatus.AUTHOR_APPROVED.value,
            DraftStatus.CANON_COMMITTED.value,
            DraftStatus.REJECTED.value,
        }:
            raise DraftWorkflowError("已批准、已提交或已拒绝草稿不可修复元数据")
        draft_path = Path(str(row["file_path"])).expanduser().resolve()
        edition_root = edition_workspace(database, book_id, selected_edition).resolve()
        drafts_root = (edition_root / "drafts").resolve()
        if drafts_root not in draft_path.parents:
            raise DraftWorkflowError("草稿路径不在当前 edition 的 drafts 目录")
        if not draft_path.is_file():
            raise DraftWorkflowError(f"草稿文件不存在：{draft_path}")
        actual_hash = sha256_file(draft_path)
        stored_hash = str(row["content_sha256"] or "")
        if actual_hash != stored_hash:
            raise DraftWorkflowError("草稿正文哈希已变化，不能执行元数据修复")
        if expected_content_sha256 is not None and actual_hash != expected_content_sha256:
            raise DraftWorkflowError("草稿正文哈希与 expected_content_sha256 不一致")
        try:
            current_output = json.loads(str(row["output_json"] or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise DraftWorkflowError("草稿 output_json 无法读取") from exc
        if not isinstance(current_output, dict):
            raise DraftWorkflowError("草稿 output_json 必须是 object")
        if not isinstance(metadata, dict):
            raise DraftWorkflowError("metadata 必须是 object")
        forbidden = {"prose_markdown", "task_id", "contract_id"}
        attempted_forbidden = sorted(forbidden & set(metadata))
        if attempted_forbidden:
            raise DraftWorkflowError(
                "元数据修复不得修改正文或身份字段：" + ", ".join(attempted_forbidden)
            )
        unknown = sorted(set(metadata) - set(DraftOutput.model_fields))
        if unknown:
            raise DraftWorkflowError("未知 DraftOutput 元数据字段：" + ", ".join(unknown))
        merged = {**current_output, **metadata}
        merged["prose_markdown"] = str(current_output.get("prose_markdown") or "")
        try:
            output = DraftOutput.model_validate(merged)
        except ValidationError as exc:
            raise DraftWorkflowError(f"修复后的 DraftOutput 无效：{exc}") from exc
        if str(output.task_id) != str(row["task_id"] or ""):
            raise DraftWorkflowError("修复后的 DraftOutput task_id 与 Draft 不一致")
        if str(output.contract_id) != str(row["contract_id"] or ""):
            raise DraftWorkflowError("修复后的 DraftOutput contract_id 与 Draft 不一致")
        output_json = json_dumps(output.model_dump(mode="json"))
        previous_version = int(row["version"] or 1)
        created_at = utc_now()
        event_id = stable_id(
            "draft-metadata-repair",
            draft_id,
            str(previous_version + 1),
            actual_hash,
            created_at,
        )
        connection.execute(
            "UPDATE drafts SET status=?, output_json=?, validation_run_id=NULL, "
            "version=version+1 WHERE book_id=? AND draft_id=? AND edition_id=?",
            (
                DraftStatus.DRAFT.value,
                output_json,
                book_id,
                draft_id,
                selected_edition,
            ),
        )
        connection.execute(
            "DELETE FROM validation_reports WHERE book_id=? AND draft_id=? AND edition_id=?",
            (book_id, draft_id, selected_edition),
        )

    root = book_root(database, book_id)
    validation_dir = (
        BookLayout(root.parent).for_book(book_id).edition(selected_edition).validation
        if (root / "book.yaml").is_file()
        else edition_workspace(database, book_id, selected_edition) / "validation"
    )
    validation_dir.mkdir(parents=True, exist_ok=True)
    old_report = validation_dir / f"{draft_id}.json"
    if old_report.is_file():
        old_report.unlink()
    audit_event = {
        "event_id": event_id,
        "event_type": "DRAFT_METADATA_REPAIRED",
        "draft_id": draft_id,
        "book_id": book_id,
        "edition_id": selected_edition,
        "expected_content_sha256": expected_content_sha256 or actual_hash,
        "content_sha256": actual_hash,
        "previous_version": previous_version,
        "new_version": previous_version + 1,
        "changed_fields": sorted(metadata),
        "created_at": created_at,
    }
    operation = find_operation(
        database,
        book_id,
        selected_edition,
        str(row["task_id"] or ""),
    )
    audit_path = (
        operation.events
        if operation is not None
        else validation_dir / "draft_metadata_repairs.jsonl"
    )
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json_dumps(audit_event) + "\n")

    result: dict[str, object] = {
        "draft_id": draft_id,
        "edition_id": selected_edition,
        "status": DraftStatus.DRAFT.value,
        "content_sha256": actual_hash,
        "expected_content_sha256": expected_content_sha256 or actual_hash,
        "changed_fields": sorted(metadata),
        "validation_invalidated": True,
        "audit_event": audit_event,
        "audit_path": str(audit_path),
    }
    from novel_authoring.validation.service import ValidationWorkflowError, validate_draft

    try:
        validation = validate_draft(
            database,
            book_id,
            draft_id,
            edition_id=selected_edition,
        )
    except ValidationWorkflowError as exc:
        result["validation_error"] = str(exc)
    else:
        result["status"] = (
            DraftStatus.VALIDATED.value if validation.passed else DraftStatus.DRAFT.value
        )
        result["validation"] = validation.model_dump(mode="json")
    return result


def discard_draft(
    database: Database,
    book_id: str,
    draft_id: str,
    *,
    edition_id: str | None = None,
) -> dict[str, object]:
    selected_edition = resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT status FROM drafts WHERE book_id=? AND draft_id=? AND edition_id=?",
            (book_id, draft_id, selected_edition),
        ).fetchone()
        if row is None:
            raise DraftWorkflowError(f"草稿不存在：{draft_id}")
        if row["status"] in {
            DraftStatus.AUTHOR_APPROVED.value,
            DraftStatus.CANON_COMMITTED.value,
        }:
            raise DraftWorkflowError("已批准或已提交草稿不可丢弃")
        connection.execute(
            "UPDATE drafts SET status=? WHERE draft_id=?",
            (DraftStatus.REJECTED.value, draft_id),
        )
    return {"draft_id": draft_id, "status": DraftStatus.REJECTED.value}
