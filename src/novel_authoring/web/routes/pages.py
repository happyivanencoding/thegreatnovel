from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from novel_authoring.author_control.service import author_control_view
from novel_authoring.author_control.source_state import source_state_coverage_summary
from novel_authoring.edition import (
    author_edition_groups,
    edition_chapters,
    list_editions,
    resolve_edition_id,
)
from novel_authoring.initialization.metrics import metric_bootstrap_status
from novel_authoring.initialization.service import latest_initialization
from novel_authoring.metrics.registry import load_registry
from novel_authoring.metrics.segments import list_segments, rebuild_segments
from novel_authoring.metrics.service import MetricsAssembler, ObservationResolver
from novel_authoring.planning.innovation import load_book_innovation_control
from novel_authoring.web.routes.jobs import list_handoffs
from novel_authoring.workflows.handoffs import resolve_instruction_path


def _instruction_availability(item: dict[str, Any]) -> tuple[bool, str | None]:
    """Mirror the copy_instruction fallback order for activity-center views."""

    task_directory = str(item.get("task_directory") or "")
    if not task_directory:
        return False, "交接任务目录缺失"
    resolved = resolve_instruction_path(Path(task_directory), item.get("prompt_path"))
    if resolved is None:
        return False, "交接任务存在，但交接指令文件缺失。请重新准备初始化任务。"
    return True, None


def _book_row(connection: Any, book_id: str) -> dict[str, Any]:
    row = connection.execute("SELECT * FROM books WHERE book_id=?", (book_id,)).fetchone()
    if row is None:
        raise ValueError("book 不存在")
    return dict(row)


def home_context(database: Any, book_id: str) -> dict[str, Any]:
    database.initialize()
    edition_id = resolve_edition_id(database, book_id)
    with database.connect() as connection:
        book = _book_row(connection, book_id)
        chapters = edition_chapters(connection, book_id, edition_id)
        books = [
            dict(row) for row in connection.execute("SELECT * FROM books ORDER BY title, book_id")
        ]
    edition_models = list_editions(database, book_id)
    editions = [edition.model_dump(mode="json") for edition in edition_models]
    return {
        "book": book,
        "books": books,
        "book_id": book_id,
        "edition_id": edition_id,
        "editions": editions,
        "chapters": chapters,
    }


def _metric_card_metadata(
    database: Any,
    book_id: str,
    edition_id: str,
    chapter: dict[str, Any],
    metrics: list[dict[str, Any]],
    observation_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    content_hash = str(chapter.get("content_sha256") or "")
    current_rows = [
        row
        for row in observation_rows
        if row.get("current")
        and not row.get("stale")
        and row.get("retracted_at") is None
        and str(row.get("effective_content_sha256") or "") == content_hash
    ]
    by_metric: dict[str, list[dict[str, Any]]] = {}
    for row in current_rows:
        by_metric.setdefault(str(row["metric_id"]), []).append(row)
    unknown_statuses = {
        "UNKNOWN",
        "UNKNOWN_AFTER_ANALYSIS",
        "MISSING",
        "NOT_ANALYZED",
        "MISSING_OPTIONAL_AUTHOR_INPUT",
    }
    for metric in metrics:
        metric_id = str(metric["metric_id"])
        rows = by_metric.get(metric_id, [])
        statuses = {str(row.get("status")) for row in rows}
        if not rows:
            analysis_state = "NOT_ANALYZED"
        elif str(metric.get("status")) == "NOT_APPLICABLE" or statuses == {"NOT_APPLICABLE"}:
            analysis_state = "NOT_APPLICABLE"
        elif statuses & unknown_statuses:
            analysis_state = "UNKNOWN"
        else:
            analysis_state = "ANALYZED"
        metric["analysis_state"] = analysis_state
        metric["observation_count"] = len(rows)
        metric["semantic_estimate_count"] = sum(
            1 for row in rows if str(row.get("source_kind")) == "SEMANTIC_ESTIMATE"
        )
        metric["last_analyzer_version"] = next(
            (str(row["analyzer_version"]) for row in rows if row.get("analyzer_version")),
            "—",
        )
        metric["import_tasks"] = sorted(
            {str(row["source_task_id"]) for row in rows if row.get("source_task_id")}
        )
        metric["evidence_count"] = sum(len(row.get("evidence_links", [])) for row in rows)
        metric["unknown_reasons"] = sorted(
            {
                str(row.get("reason"))
                for row in rows
                if str(row.get("status")) in unknown_statuses and row.get("reason")
            }
        )
        metric["observation_history"] = rows
    bootstrap: dict[str, Any] = {
        "status": "NOT_READY",
        "coverage": {
            "source_mapping_coverage": 0.0,
            "arc_output_coverage": 0.0,
            "chapter_semantic_feature_coverage": 0.0,
            "metric_observation_coverage": 0.0,
            "recent_detailed_metric_coverage": 0.0,
            "current_chapter_metric_coverage": 0.0,
        },
        "initialization_id": None,
    }
    initialization = latest_initialization(database, book_id, edition_id)
    if initialization:
        initialization_manifest = initialization.get("manifest") or {}
        initialization_id = initialization_manifest.get("initialization_id")
        if initialization_id:
            try:
                bootstrap = metric_bootstrap_status(
                    database,
                    book_id,
                    edition_id=edition_id,
                    initialization_id=str(initialization_id),
                )
            except (OSError, ValueError):
                bootstrap["initialization_id"] = initialization_id
    metadata = {
        "observation_count": len(current_rows),
        "semantic_estimate_count": sum(
            1 for row in current_rows if str(row.get("source_kind")) == "SEMANTIC_ESTIMATE"
        ),
        "evidence_count": sum(len(row.get("evidence_links", [])) for row in current_rows),
        "analyzer_versions": sorted(
            {str(row["analyzer_version"]) for row in current_rows if row.get("analyzer_version")}
        ),
        "import_tasks": sorted(
            {str(row["source_task_id"]) for row in current_rows if row.get("source_task_id")}
        ),
        "current_content_hash": content_hash,
        "bootstrap": bootstrap,
    }
    return metrics, metadata


def chapter_context(
    database: Any, book_id: str, edition_id: str, chapter_id: str
) -> dict[str, Any]:
    database.initialize()
    with database.connect() as connection:
        chapters = edition_chapters(connection, book_id, edition_id)
        chapter_index = next(
            (index for index, item in enumerate(chapters) if str(item["chapter_id"]) == chapter_id),
            None,
        )
        if chapter_index is None:
            raise ValueError("章节不存在")
        chapter = chapters[chapter_index]
        book = _book_row(connection, book_id)
    segments = list_segments(database, book_id, edition_id=edition_id, chapter_id=chapter_id)
    if not segments:
        rebuild_segments(database, book_id, edition_id=edition_id)
        segments = list_segments(database, book_id, edition_id=edition_id, chapter_id=chapter_id)
    assembler = MetricsAssembler(database)
    run = assembler.rebuild(
        book_id, edition_id=edition_id, scope_type="CHAPTER", scope_id=chapter_id
    )
    latest = assembler.latest(book_id, edition_id, "CHAPTER", chapter_id)
    metrics = run["results"]
    missing_count = sum(len(item.get("missing_components", [])) for item in metrics)
    history = metric_history(database, book_id, edition_id, "CHAPTER", chapter_id)
    observation_rows = observation_history(database, book_id, edition_id, "CHAPTER", chapter_id)
    metrics, metric_metadata = _metric_card_metadata(
        database,
        book_id,
        edition_id,
        dict(chapter),
        metrics,
        observation_rows,
    )
    return {
        "book": book,
        "book_id": book_id,
        "edition_id": edition_id,
        "chapter": chapter,
        "chapters": chapters,
        "segments": segments,
        "bundle": run["bundle"],
        "run": run,
        "latest": latest,
        "metrics": metrics,
        "history": history,
        "observation_history": observation_rows,
        "metric_metadata": metric_metadata,
        "metric_bootstrap": metric_metadata["bootstrap"],
        "missing_count": missing_count,
        "previous_chapter": None if chapter_index == 0 else chapters[chapter_index - 1],
        "next_chapter": None if chapter_index == len(chapters) - 1 else chapters[chapter_index + 1],
        "source_info": {
            "relative_path": chapter.get("relative_path", ""),
            "source_span_id": chapter.get("source_span_id"),
            "content_sha256": chapter.get("content_sha256", ""),
            "document_status": chapter.get("document_status", ""),
        },
    }


def metric_history(
    database: Any, book_id: str, edition_id: str, scope_type: str, scope_id: str
) -> list[dict[str, Any]]:
    database.initialize()
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT * FROM metric_runs WHERE book_id=? AND edition_id=? "
            "AND scope_type=? AND scope_id=? ORDER BY created_at DESC",
            (book_id, edition_id, scope_type, scope_id),
        ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["requested_metric_ids"] = json.loads(
                str(item.get("requested_metric_ids_json") or "[]")
            )
            item["disputed_components"] = json.loads(
                str(item.get("disputed_components_json") or "[]")
            )
            item["stale_components"] = json.loads(str(item.get("stale_components_json") or "[]"))
            result.append(item)
        return result


def observation_history(
    database: Any, book_id: str, edition_id: str, scope_type: str, scope_id: str
) -> list[dict[str, Any]]:
    """Return the append-only observation ledger, including retracted rows."""
    database.initialize()
    resolver = ObservationResolver(database, load_registry())
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT * FROM metric_observations WHERE book_id=? AND edition_id=? "
            "AND scope_type=? AND scope_id=? ORDER BY created_at DESC, observation_id DESC",
            (book_id, edition_id, scope_type, scope_id),
        ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            try:
                item["value"] = json.loads(str(item.get("value_json") or "null"))
            except json.JSONDecodeError:
                item["value"] = item.get("value_json")
            links = connection.execute(
                "SELECT * FROM metric_evidence_links WHERE observation_id=? "
                "ORDER BY created_at, link_id",
                (str(row["observation_id"]),),
            ).fetchall()
            item["evidence_links"] = [dict(link) for link in links]
            resolved = resolver.resolve(
                book_id,
                edition_id,
                scope_type,
                scope_id,
                str(row["metric_id"]),
                str(row["component_id"]),
            )
            item["current"] = resolved.effective_observation_id == str(row["observation_id"])
            item["resolution_status"] = resolved.status.value
            item["effective_observation_id"] = resolved.effective_observation_id
            item["stale"] = bool(
                str(row["freshness_status"] or "FRESH") != "FRESH"
                or row["stale_reason"]
                or resolved.stale_reason
            )
            item["stale_reason"] = row["stale_reason"] or resolved.stale_reason
            result.append(item)
        return result


def dashboard_context(database: Any, book_id: str) -> dict[str, Any]:
    context = home_context(database, book_id)
    edition_id = context["edition_id"]
    chapters = context["chapters"]
    latest_chapter = chapters[-1] if chapters else None
    latest_run = None
    missing = disputed = stale = complete = incomplete = 0
    if latest_chapter is not None:
        run = MetricsAssembler(database).rebuild(
            book_id,
            edition_id=edition_id,
            scope_type="CHAPTER",
            scope_id=str(latest_chapter["chapter_id"]),
        )
        latest_run = run
        for item in run["results"]:
            if item["status"] == "COMPLETE":
                complete += 1
            else:
                incomplete += 1
            missing += len(item.get("missing_components", []))
            disputed += len(item.get("disputed_components", []))
            stale += len(item.get("stale_components", []))
    with database.connect() as connection:
        handoff_rows = connection.execute(
            "SELECT status, COUNT(*) AS count FROM workflow_handoffs WHERE book_id=? "
            "GROUP BY status",
            (book_id,),
        ).fetchall()
        handoffs = {str(row["status"]): int(row["count"]) for row in handoff_rows}
        latest_draft = connection.execute(
            "SELECT * FROM drafts WHERE book_id=? AND edition_id=? "
            "AND status IN ('VALIDATED', 'VALIDATED_DRAFT') ORDER BY created_at DESC LIMIT 1",
            (book_id, edition_id),
        ).fetchone()
        latest_campaign = connection.execute(
            "SELECT * FROM revision_campaigns WHERE book_id=? AND edition_id=? "
            "ORDER BY created_at DESC LIMIT 1",
            (book_id, edition_id),
        ).fetchone()
        latest_aggregate = connection.execute(
            "SELECT * FROM planning_aggregates WHERE book_id=? AND edition_id=? "
            "ORDER BY created_at DESC LIMIT 1",
            (book_id, edition_id),
        ).fetchone()
        rhythm_row = connection.execute(
            "SELECT snapshot_json FROM rhythm_diagnostic_snapshots WHERE book_id=? "
            "AND edition_id=? ORDER BY as_of_chapter DESC, created_at DESC LIMIT 1",
            (book_id, edition_id),
        ).fetchone()
        latest_ordinal = max((int(item["ordinal"]) for item in chapters), default=0)
        overdue_promises = connection.execute(
            "SELECT promise_id, statement, target_max_age, last_advanced_ordinal, status "
            "FROM promises WHERE book_id=? AND edition_id=? "
            "AND status NOT IN ('RESOLVED', 'CLOSED', 'PAID')",
            (book_id, edition_id),
        ).fetchall()
        overdue = [
            dict(row)
            for row in overdue_promises
            if row["target_max_age"] is not None
            and latest_ordinal - int(row["last_advanced_ordinal"] or 0) > int(row["target_max_age"])
        ]
    rhythm: dict[str, Any] = {}
    if rhythm_row is not None:
        try:
            rhythm = json.loads(str(rhythm_row["snapshot_json"] or "{}"))
        except json.JSONDecodeError:
            rhythm = {"raw": str(rhythm_row["snapshot_json"])}
    return {
        **context,
        "latest_chapter": latest_chapter,
        "latest_run": latest_run,
        "counts": {
            "complete": complete,
            "incomplete": incomplete,
            "missing": missing,
            "disputed": disputed,
            "stale": stale,
        },
        "handoffs": handoffs,
        "latest_draft": (
            None
            if latest_draft is None
            else {
                **dict(latest_draft),
                "display_status": (
                    "VALIDATED_DRAFT"
                    if str(latest_draft["status"]) == "VALIDATED"
                    else str(latest_draft["status"])
                ),
            }
        ),
        "latest_campaign": None if latest_campaign is None else dict(latest_campaign),
        "latest_aggregate": None if latest_aggregate is None else dict(latest_aggregate),
        "rhythm": rhythm,
        "overdue_promises": overdue,
    }


_WORKFLOW_STATUS_LABELS = {
    "READY_FOR_CODEX": "等待 AI 处理",
    "CLAIMED": "已接收，正在准备",
    "RUNNING": "正在分析",
    "WAITING_FOR_USER": "等待你的操作",
    "COMPLETED": "已生成结果",
    "FAILED": "处理失败",
    "STALE": "需要刷新上下文",
    "CANCELLED": "已取消",
    "DRAFT": "准备中",
}
_WORKFLOW_HANDOFF_LABELS = {"CONTINUATION": "续写", "REVISION": "改写"}
_ACTIVITY_TYPE_LABELS = {
    "CONTINUATION": "续写",
    "REVISION": "改写",
    "METRIC_SEMANTIC_ANALYSIS": "语义指标分析",
    "CHAPTER_FEATURE_ANALYSIS": "章节特征分析",
    "STORY_ATLAS_BOOTSTRAP": "故事地图初始化",
    "STORY_ATLAS_REFRESH": "故事地图刷新",
    "WORLD_MODEL_REVIEW": "世界模型复核",
    "STORY_ATLAS_RENDER": "故事地图渲染",
    "BATCH_CONTINUATION": "批量续写",
    "NOVEL_INITIALIZATION": "小说初始化",
    "NOVEL_DISTILLATION": "写作知识提炼",
    "SOURCE_STATE_HYDRATION": "世界状态补齐",
    "PROFILE_REANALYSIS": "全书画像重新分析",
}
_WORKFLOW_STAGE_LABELS = {
    "PLAN_ONLY": "只生成方案",
    "DRAFT_AND_VALIDATE": "方案、正文与校验",
    "IMPACT_AND_PLAN": "影响审计与改写计划",
}
_WORKFLOW_LEVEL_LABELS = {
    "minimal": "最小",
    "low": "低",
    "medium": "中",
    "high": "高",
    "bold": "大胆",
}
_WORKFLOW_FOCUS_LABELS = {
    "auto": "自动",
    "plot": "剧情",
    "character": "人物",
    "relationship": "关系",
    "world": "世界",
    "mechanism": "机制",
    "narrative_structure": "叙事结构",
    "style": "文风",
}
_WORKFLOW_TIMELINE_STAGES = (
    ("context", "准备上下文"),
    ("handoff", "交给 AI"),
    ("candidates", "生成候选"),
    ("draft", "生成正文"),
    ("validation", "连续性校验"),
    ("approval", "等待你的确认"),
)


def _workflow_date(value: Any) -> str:
    text = str(value or "")
    return text.replace("T", " ")[:16] if text else "—"


def _workflow_task_file(item: dict[str, Any]) -> dict[str, Any]:
    raw_path = item.get("task_manifest_path")
    if not raw_path:
        return {}
    path = Path(str(raw_path))
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _workflow_timeline(status: str, requested_stage: str) -> list[dict[str, str]]:
    stage_index = {
        "READY_FOR_CODEX": 1,
        "CLAIMED": 1,
        "RUNNING": 2,
        "WAITING_FOR_USER": 5,
        "COMPLETED": len(_WORKFLOW_TIMELINE_STAGES) + 1,
        "FAILED": 2,
        "STALE": 1,
        "CANCELLED": 1,
    }.get(status, 1)
    if requested_stage == "PLAN_ONLY":
        stage_index = {
            "READY_FOR_CODEX": 1,
            "CLAIMED": 1,
            "RUNNING": 2,
            "WAITING_FOR_USER": 5,
            "COMPLETED": 4,
            "FAILED": 2,
            "STALE": 1,
            "CANCELLED": 1,
        }.get(status, stage_index)
    result: list[dict[str, str]] = []
    for index, (key, label) in enumerate(_WORKFLOW_TIMELINE_STAGES, start=1):
        state = "done" if index < stage_index else "current" if index == stage_index else "upcoming"
        if status in {"FAILED", "STALE", "CANCELLED"} and index == stage_index:
            state = "failed"
        result.append({"key": key, "label": label, "state": state})
    return result


def _workflow_task_view(
    item: dict[str, Any],
    editions_by_id: dict[str, dict[str, Any]],
    current_chapter: dict[str, Any] | None,
) -> dict[str, Any]:
    task_file = _workflow_task_file(item)
    status = str(item.get("status") or "DRAFT").upper()
    handoff_type = str(item.get("handoff_type") or "").upper()
    requested_stage = str(item.get("requested_stage") or "").upper()
    innovation = task_file.get("innovation_control")
    innovation = innovation if isinstance(innovation, dict) else {}
    focus = innovation.get("focus")
    focus_values = focus if isinstance(focus, list) else []
    target_ordinal = task_file.get("context_chapter_ordinal")
    if target_ordinal is None:
        target_ordinal = task_file.get("target_chapter_ordinal")
    if target_ordinal is None and current_chapter is not None:
        target_ordinal = int(current_chapter["ordinal"]) + (0 if handoff_type == "REVISION" else 1)
    selected_edition = editions_by_id.get(str(item.get("edition_id")))
    return {
        **item,
        "author_type_label": _WORKFLOW_HANDOFF_LABELS.get(handoff_type, "工作任务"),
        "author_status_label": _WORKFLOW_STATUS_LABELS.get(status, "处理中"),
        "author_stage_label": _WORKFLOW_STAGE_LABELS.get(requested_stage, "生成任务"),
        "edition_display_name": (
            selected_edition.get("display_name")
            if selected_edition
            else str(item.get("edition_id") or "当前版本")
        ),
        "target_chapter_label": f"第{target_ordinal}章" if target_ordinal else "当前章节",
        "created_at_label": _workflow_date(item.get("created_at")),
        "innovation_level_label": _WORKFLOW_LEVEL_LABELS.get(
            str(innovation.get("level") or ""), "默认"
        ),
        "innovation_focus_label": "、".join(
            _WORKFLOW_FOCUS_LABELS.get(str(value), str(value)) for value in focus_values
        )
        or "自动",
        "timeline": _workflow_timeline(status, requested_stage),
        "next_action_label": {
            "READY_FOR_CODEX": "复制指令给 Codex",
            "CLAIMED": "查看准备进度",
            "RUNNING": "查看处理进度",
            "WAITING_FOR_USER": "处理作者请求",
            "COMPLETED": "查看生成结果",
            "FAILED": "查看失败原因",
            "STALE": "重新检查上下文",
            "CANCELLED": "查看任务记录",
        }.get(status, "查看任务"),
        "technical": {
            "handoff_id": item.get("handoff_id"),
            "requested_stage": requested_stage,
            "edition_id": item.get("edition_id"),
            "task_directory": item.get("task_directory"),
            "status": status,
        },
    }


def _activity_status_group(status: str) -> str:
    if status in {"WAITING_FOR_USER", "FAILED", "STALE"}:
        return "attention"
    if status in {"COMPLETED", "CANCELLED"}:
        return "completed"
    return "running"


def _activity_progress(handoff_type: str, status: str) -> int | None:
    if handoff_type not in {"CONTINUATION", "REVISION", "BATCH_CONTINUATION"}:
        return 100 if status in {"COMPLETED", "CANCELLED"} else None
    return {
        "DRAFT": 0,
        "READY_FOR_CODEX": 20,
        "CLAIMED": 30,
        "RUNNING": 55,
        "WAITING_FOR_USER": 85,
        "COMPLETED": 100,
        "FAILED": 55,
        "STALE": 20,
        "CANCELLED": 100,
    }.get(status)


def _activity_target(
    item: dict[str, Any],
    task_file: dict[str, Any],
    chapters_by_id: dict[str, dict[str, Any]],
    current_chapter: dict[str, Any] | None,
) -> tuple[str | None, int | None]:
    handoff_type = str(item.get("handoff_type") or "").upper()
    hydration = task_file.get("hydration")
    hydration = hydration if isinstance(hydration, dict) else {}
    chapter_id = (
        str(
            task_file.get("context_chapter_id")
            or hydration.get("chapter_id")
            or item.get("context_chapter_id")
            or ""
        )
        or None
    )
    chapter = chapters_by_id.get(chapter_id or "")
    context_ordinal = None if chapter is None else int(chapter["ordinal"])
    if context_ordinal is None and hydration.get("chapter_ordinal") is not None:
        context_ordinal = int(hydration["chapter_ordinal"])
    if context_ordinal is None and current_chapter is not None:
        context_ordinal = int(current_chapter["ordinal"])
        chapter_id = str(current_chapter["chapter_id"])
    target_ordinal = context_ordinal
    if handoff_type in {"CONTINUATION", "BATCH_CONTINUATION"} and context_ordinal:
        target_ordinal = context_ordinal + 1
    return chapter_id, target_ordinal


def _workbench_target(
    book_id: str,
    edition_id: str,
    *,
    chapter_id: str | None,
    action: str | None = None,
    mode: str | None = None,
    node: str | None = None,
    activity_id: str | None = None,
    state_tab: str | None = None,
) -> str:
    query: dict[str, str] = {}
    if chapter_id:
        query["chapter_id"] = chapter_id
    if action:
        query["action"] = action
    if mode:
        query["mode"] = mode
    if node:
        query["node"] = node
    if activity_id:
        query["activity_id"] = activity_id
    if state_tab:
        query["state_tab"] = state_tab
    suffix = f"?{urlencode(query)}" if query else ""
    return f"/books/{book_id}/editions/{edition_id}/workbench{suffix}"


def _activity_view(
    item: dict[str, Any],
    *,
    book_id: str,
    edition_id: str,
    chapters_by_id: dict[str, dict[str, Any]],
    current_chapter: dict[str, Any] | None,
) -> dict[str, Any]:
    task_file = _workflow_task_file(item)
    handoff_type = str(item.get("handoff_type") or "").upper()
    requested_stage = str(item.get("requested_stage") or "").upper()
    status = str(item.get("status") or "DRAFT").upper()
    chapter_id, target_ordinal = _activity_target(item, task_file, chapters_by_id, current_chapter)
    action: str | None = None
    mode: str | None = "home"
    node = "overview"
    if handoff_type == "CONTINUATION":
        action = "plan" if requested_stage == "PLAN_ONLY" else "continue"
        mode = None
        node = "planning" if action == "plan" else "chapter"
    elif handoff_type == "REVISION":
        action = "rewrite"
        mode = None
        node = "chapter"
    elif handoff_type == "PROFILE_REANALYSIS":
        mode = "analysis"
        node = "worldbuilding"
    elif handoff_type == "SOURCE_STATE_HYDRATION":
        mode = "state"
        node = "state"
    type_label = _ACTIVITY_TYPE_LABELS.get(handoff_type, "系统任务")
    if handoff_type == "CONTINUATION":
        title = (
            f"第{target_ordinal}章规划候选"
            if requested_stage == "PLAN_ONLY" and target_ordinal
            else f"第{target_ordinal}章续写"
            if target_ordinal
            else "下一章续写"
        )
    elif handoff_type == "REVISION":
        title = f"第{target_ordinal}章改写" if target_ordinal else "本章改写"
    elif handoff_type == "PROFILE_REANALYSIS":
        title = "全书画像重新分析"
    elif handoff_type == "SOURCE_STATE_HYDRATION":
        title = f"第{target_ordinal}章世界状态补齐" if target_ordinal else "世界状态补齐"
    else:
        title = type_label
    summary = {
        "CONTINUATION": "从所选章节继续，生成可比较的方向或草稿。",
        "REVISION": "先完成影响审计，再进入派生版本改写。",
        "PROFILE_REANALYSIS": "重新分析九维全书画像；当前画像保持可用。",
        "SOURCE_STATE_HYDRATION": "从原文证据补齐这一章的历史世界状态。",
    }.get(handoff_type, "后台能力正在为小说工作台准备结果。")
    handoff_id = str(item.get("handoff_id") or "")
    progress = _activity_progress(handoff_type, status)
    instruction_available, instruction_error = _instruction_availability(item)
    open_target = _workbench_target(
        book_id,
        edition_id,
        chapter_id=chapter_id,
        action=action,
        mode=mode,
        node=node,
        activity_id=handoff_id,
        state_tab="overview" if node == "state" else None,
    )
    return {
        "activity_id": handoff_id,
        "activity_kind": "SYSTEM_ACTIVITY",
        "handoff_type": handoff_type,
        "type_label": type_label,
        "title": title,
        "summary": summary,
        "status": status,
        "status_label": _WORKFLOW_STATUS_LABELS.get(status, "处理中"),
        "status_group": _activity_status_group(status),
        "progress": progress,
        "progress_label": f"{progress}%" if progress is not None else "按阶段显示",
        "instruction_available": instruction_available,
        "instruction_error": instruction_error,
        "created_at_label": _workflow_date(item.get("created_at")),
        "open_target": open_target,
        "next_action_label": {
            "READY_FOR_CODEX": "等待 AI 处理",
            "CLAIMED": "查看准备进度",
            "RUNNING": "查看处理进度",
            "WAITING_FOR_USER": "继续处理",
            "COMPLETED": "查看结果",
            "FAILED": "查看问题",
            "STALE": "刷新后重试",
            "CANCELLED": "查看记录",
        }.get(status, "查看任务"),
        "technical": {
            "handoff_id": handoff_id,
            "handoff_type": handoff_type,
            "requested_stage": requested_stage,
            "status": status,
            "edition_id": item.get("edition_id"),
            "task_directory": item.get("task_directory"),
            "instruction_available": instruction_available,
            "instruction_error": instruction_error,
        },
    }


def _hydration_activity(
    activities: list[dict[str, Any]],
    *,
    book_id: str,
    edition_id: str,
    current_chapter: dict[str, Any] | None,
    coverage: dict[str, int | float],
) -> dict[str, Any] | None:
    hydration = [item for item in activities if item["handoff_type"] == "SOURCE_STATE_HYDRATION"]
    if not hydration:
        return None
    latest = hydration[0]
    total = int(coverage["total"])
    analyzed = int(coverage["analyzed"])
    if analyzed >= total and total:
        status = "COMPLETED"
    elif int(coverage["failed"]):
        status = "FAILED"
    elif int(coverage["running"]):
        status = "RUNNING"
    elif int(coverage["ready"]):
        status = "READY_FOR_CODEX"
    else:
        status = str(latest["status"])
    progress = round(analyzed * 100 / total) if total else 0
    chapter_id = None if current_chapter is None else str(current_chapter["chapter_id"])
    return {
        **latest,
        "activity_id": f"source-state-hydration:{edition_id}",
        "title": f"世界状态补齐 · {analyzed}/{total}章",
        "summary": "从原文证据建立各章的历史世界状态；无变化也会明确记为已分析。",
        "status": status,
        "status_label": _WORKFLOW_STATUS_LABELS.get(status, "处理中"),
        "status_group": _activity_status_group(status),
        "progress": progress,
        "progress_label": f"{analyzed}/{total}章 · {progress}%",
        "open_target": _workbench_target(
            book_id,
            edition_id,
            chapter_id=chapter_id,
            mode="state",
            node="state",
            activity_id=f"source-state-hydration:{edition_id}",
            state_tab="overview",
        ),
        "technical": {
            "handoff_count": len(hydration),
            "handoff_ids": [item["technical"]["handoff_id"] for item in hydration],
            "raw_statuses": sorted({str(item["status"]) for item in hydration}),
            "task_directories": [item["technical"]["task_directory"] for item in hydration],
        },
    }


def activity_center_view(
    database: Any,
    *,
    book_id: str,
    edition_id: str,
    handoffs: list[dict[str, Any]],
    chapters: list[dict[str, Any]],
    current_chapter: dict[str, Any] | None,
    selected_activity_id: str | None,
) -> dict[str, Any]:
    chapters_by_id = {str(item["chapter_id"]): item for item in chapters}
    activities = [
        _activity_view(
            item,
            book_id=book_id,
            edition_id=edition_id,
            chapters_by_id=chapters_by_id,
            current_chapter=current_chapter,
        )
        for item in handoffs
    ]
    with database.connect() as connection:
        coverage = source_state_coverage_summary(connection, book_id, edition_id)
    hydration = _hydration_activity(
        activities,
        book_id=book_id,
        edition_id=edition_id,
        current_chapter=current_chapter,
        coverage=coverage,
    )
    activities = [item for item in activities if item["handoff_type"] != "SOURCE_STATE_HYDRATION"]
    if hydration is not None:
        activities.append(hydration)
    activities.sort(key=lambda item: str(item["created_at_label"]), reverse=True)
    group_labels = {
        "attention": "需要你",
        "running": "进行中",
        "completed": "已完成",
    }
    groups = [
        {
            "key": key,
            "label": group_labels[key],
            "items": [item for item in activities if item["status_group"] == key],
        }
        for key in ("attention", "running", "completed")
    ]
    active = [item for item in activities if item["status_group"] != "completed"]
    selected = next(
        (item for item in activities if item["activity_id"] == selected_activity_id),
        None,
    )
    return {
        "activities": activities,
        "groups": groups,
        "badge_count": len(active),
        "selected_activity": selected,
        "coverage": coverage,
    }


def _workflow_portfolio(author_control: dict[str, Any]) -> list[dict[str, Any]]:
    portfolio = author_control.get("portfolio")
    portfolio = portfolio if isinstance(portfolio, dict) else {}
    result: list[dict[str, Any]] = []
    horizon_labels = {"SHORT": "短线", "MID": "中线", "LONG": "长线"}
    for horizon in ("SHORT", "MID", "LONG"):
        rows = portfolio.get(horizon) or []
        open_count = sum(
            1 for row in rows if str(row.get("lifecycle_status")) not in {"DONE", "CANCELLED"}
        )
        active_count = sum(1 for row in rows if str(row.get("lifecycle_status")) == "ACTIVE")
        result.append(
            {
                "horizon": horizon,
                "label": horizon_labels[horizon],
                "total": len(rows),
                "open": open_count,
                "active": active_count,
                "summary": (
                    f"{active_count} 条活跃 · {open_count} 条待推进"
                    if open_count
                    else "还没有作者任务"
                ),
            }
        )
    return result


def workflow_context(
    database: Any,
    book_id: str,
    *,
    edition_id: str | None = None,
    chapter_id: str | None = None,
    activity_id: str | None = None,
) -> dict[str, Any]:
    database.initialize()
    selected_edition_id = resolve_edition_id(database, book_id, edition_id)
    with database.connect() as connection:
        book = _book_row(connection, book_id)
        chapters = edition_chapters(connection, book_id, selected_edition_id)
        library_books = [
            dict(row) for row in connection.execute("SELECT * FROM books ORDER BY title, book_id")
        ]
    edition_models = list_editions(database, book_id)
    editions = [edition.model_dump(mode="json") for edition in edition_models]
    editions_by_id = {str(item["edition_id"]): item for item in editions}
    selected_chapter = next(
        (item for item in chapters if chapter_id and str(item["chapter_id"]) == chapter_id),
        chapters[-1] if chapters else None,
    )
    current_chapter = None
    if selected_chapter is not None:
        status = str(selected_chapter.get("document_status") or "SOURCE").upper()
        current_chapter = {
            **selected_chapter,
            "status_label": {"CANON": "原文", "SOURCE": "原文", "PROVISIONAL": "草稿"}.get(
                status, "只读内容"
            ),
        }
    author_control = author_control_view(database, book_id, selected_edition_id)
    handoffs = list_handoffs(database, book_id, selected_edition_id)
    workflow_tasks = [
        _workflow_task_view(item, editions_by_id, current_chapter)
        for item in handoffs
        if str(item.get("handoff_type") or "").upper() in {"CONTINUATION", "REVISION"}
    ]
    narrative_tasks = [
        task
        for task in author_control.get("tasks", [])
        if str(task.get("task_type") or "").upper() == "AUTHOR_TASK"
    ]
    narrative_portfolio = {
        horizon: [task for task in narrative_tasks if str(task.get("horizon") or "") == horizon]
        for horizon in ("SHORT", "MID", "LONG")
    }
    activity_center = activity_center_view(
        database,
        book_id=book_id,
        edition_id=selected_edition_id,
        handoffs=handoffs,
        chapters=chapters,
        current_chapter=current_chapter,
        selected_activity_id=activity_id,
    )
    selected_edition = editions_by_id.get(selected_edition_id, {})
    return {
        "book_id": book_id,
        "book": book,
        "library_books": library_books,
        "chapters": chapters,
        "current_chapter": current_chapter,
        "edition_id": selected_edition_id,
        "edition": selected_edition,
        "editions": editions,
        "edition_groups": author_edition_groups(edition_models),
        "handoffs": handoffs,
        "workflow_tasks": workflow_tasks,
        "activity_center": activity_center,
        "author_control": author_control,
        "author_tasks": narrative_tasks,
        "author_intents": author_control.get("intents", []),
        "portfolio": _workflow_portfolio({"portfolio": narrative_portfolio}),
        "innovation_default": load_book_innovation_control(database, book_id).model_dump(
            mode="json"
        ),
    }
