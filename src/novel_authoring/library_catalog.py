"""Read-only discovery and author-facing catalog views for Novel Studio."""

from __future__ import annotations

import json
import re
import sqlite3
from base64 import urlsafe_b64encode
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from novel_authoring.config import load_settings
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookKind, BookRecord, BookRegistry
from novel_authoring.workflows.handoffs import resolve_instruction_path

_IGNORED_NAMES = {"library", "benchmark", "audit", "_system"}
_ACTIVE_HANDOFF_STATUSES = {"READY_FOR_CODEX", "CLAIMED", "RUNNING", "WAITING_FOR_USER"}


class CatalogScope(StrEnum):
    AUTHOR = "AUTHOR"
    TECHNICAL = "TECHNICAL"


def _normalized_path(path: Path) -> str:
    return str(path.expanduser().resolve()).replace("/", "\\").casefold()


def _iso_mtime(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=UTC).isoformat()


def _candidate_id(relative_path: str) -> str:
    encoded = urlsafe_b64encode(relative_path.casefold().encode("utf-8")).decode("ascii")
    return "candidate-" + encoded.rstrip("=")


def _legacy_source_key(record: BookRecord) -> tuple[str, int] | None:
    if len(record.source_files) != 1:
        return None
    source = record.source_root / record.source_files[0]
    try:
        size = source.stat().st_size
    except OSError:
        return None
    return Path(record.source_files[0]).name.casefold(), size


def _ignored(path: Path) -> bool:
    name = path.name
    folded = name.casefold()
    return (
        not name
        or name.startswith(".")
        or name.startswith(".~")
        or folded in _IGNORED_NAMES
        or folded == "readme"
        or folded.startswith("readme.")
        or folded.endswith(".tmp")
    )


def _ignored_relative_part(name: str) -> bool:
    folded = name.casefold()
    return (
        not name
        or name.startswith(".")
        or name.startswith(".~")
        or folded in _IGNORED_NAMES
    )


@dataclass(frozen=True, slots=True)
class DiscoveredBookCandidate:
    candidate_id: str
    display_title: str
    source_path: str
    source_kind: str
    source_filename: str
    file_size: int
    modified_at: str
    discovery_status: str = "DISCOVERED"
    linked_book_id: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BookDiscoveryService:
    """Scan one drop-in root without creating files, databases, or tasks."""

    def __init__(self, discovery_root: Path, extensions: Iterable[str] | None = None) -> None:
        self.discovery_root = Path(discovery_root).expanduser().resolve()
        configured = extensions or load_settings().ingest.extensions
        self.extensions = tuple(
            sorted({str(item).casefold() for item in configured if str(item).startswith(".")})
        )

    def scan(self) -> list[DiscoveredBookCandidate]:
        if not self.discovery_root.is_dir():
            return []
        candidates: list[DiscoveredBookCandidate] = []
        try:
            children = sorted(
                self.discovery_root.iterdir(), key=lambda item: item.name.casefold()
            )
        except OSError:
            return []
        for child in children:
            if _ignored(child) or child.is_symlink():
                continue
            if child.is_file() and child.suffix.casefold() in self.extensions:
                candidate = self._candidate(child, [child], "FILE")
            elif child.is_dir():
                source_files = [
                    path
                    for path in child.rglob("*")
                    if path.is_file()
                    and not path.is_symlink()
                    and path.suffix.casefold() in self.extensions
                    and not any(
                        _ignored_relative_part(part)
                        for part in path.relative_to(child).parts[:-1]
                    )
                    and not _ignored(path)
                ]
                candidate = self._candidate(child, source_files, "FOLDER")
            else:
                candidate = None
            if candidate is not None:
                candidates.append(candidate)
        return candidates

    def _candidate(
        self, source: Path, source_files: list[Path], source_kind: str
    ) -> DiscoveredBookCandidate | None:
        if not source_files:
            return None
        try:
            stats = [path.stat() for path in source_files]
            source_stat = source.stat()
        except OSError:
            return None
        relative = source.relative_to(self.discovery_root).as_posix()
        return DiscoveredBookCandidate(
            candidate_id=_candidate_id(relative),
            display_title=source.stem if source_kind == "FILE" else source.name,
            source_path=str(source),
            source_kind=source_kind,
            source_filename=source.name,
            file_size=sum(item.st_size for item in stats),
            modified_at=_iso_mtime(max([source_stat.st_mtime, *(item.st_mtime for item in stats)])),
        )


@dataclass(frozen=True, slots=True)
class StudioReadinessView:
    book_id: str
    status: str
    ready: bool
    missing_requirements: tuple[str, ...]
    initialization_id: str | None
    initialization_status: str | None
    author_summary: str
    handoff_id: str | None = None
    handoff_status: str | None = None
    updated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["missing_requirements"] = list(self.missing_requirements)
        return value


@dataclass(frozen=True, slots=True)
class LibraryCatalogEntry:
    catalog_id: str
    title: str
    state: str
    state_label: str
    studio_ready: bool
    primary_action: str
    primary_action_label: str
    source_path: str
    modified_at: str | None
    book_id: str | None = None
    candidate_id: str | None = None
    source_kind: str | None = None
    chapter_count: int = 0
    edition_count: int = 0
    active_edition: str = "base"
    book_kind: str | None = None
    creation_mode: str | None = None
    initialization_status: str | None = None
    initialization_id: str | None = None
    handoff_id: str | None = None
    handoff_status: str | None = None
    instruction_available: bool = False
    instruction_error: str | None = None
    missing_requirements: tuple[str, ...] = ()
    author_summary: str = ""
    technical: dict[str, Any] = field(default_factory=dict)

    @property
    def href(self) -> str:
        if self.book_id:
            return f"/books/{self.book_id}/editions/{self.active_edition}/workbench"
        return f"/library/candidates/{self.candidate_id}"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["missing_requirements"] = list(self.missing_requirements)
        value["href"] = self.href
        return value


@dataclass(frozen=True, slots=True)
class LibraryCatalogView:
    library_root: str
    discovery_root: str
    supported_formats: tuple[str, ...]
    entries: tuple[LibraryCatalogEntry, ...]
    revision: str
    scope: CatalogScope = CatalogScope.AUTHOR

    def to_dict(self) -> dict[str, Any]:
        grouped = {
            "ready": [item.to_dict() for item in self.entries if item.studio_ready],
            "running": [
                item.to_dict()
                for item in self.entries
                if item.state in {"INITIALIZING", "INITIALIZATION_REVIEW"}
            ],
            "pending": [
                item.to_dict()
                for item in self.entries
                if not item.studio_ready
                and item.state not in {"INITIALIZING", "INITIALIZATION_REVIEW"}
            ],
        }
        kind_groups = {
            kind.value: [
                item.to_dict() for item in self.entries if item.book_kind == kind.value
            ]
            for kind in (
                BookKind.BENCHMARK,
                BookKind.TEST,
                BookKind.DEMO,
                BookKind.UNCLASSIFIED,
            )
        }
        return {
            "library_root": self.library_root,
            "discovery_root": self.discovery_root,
            "supported_formats": list(self.supported_formats),
            "entries": [item.to_dict() for item in self.entries],
            "groups": grouped,
            "counts": {name: len(items) for name, items in grouped.items()},
            "kind_groups": kind_groups,
            "kind_counts": {name: len(items) for name, items in kind_groups.items()},
            "scope": self.scope.value,
            "revision": self.revision,
        }


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _latest_initialization(paths: Any, edition_id: str) -> dict[str, Any] | None:
    root = paths.edition(edition_id).initialization
    if not root.is_dir():
        return None
    candidates = [
        path
        for path in root.iterdir()
        if path.is_dir() and (path / "initialization_manifest.json").is_file()
    ]
    if not candidates:
        return None
    selected = max(candidates, key=lambda path: path.stat().st_mtime)
    manifest = _read_json(selected / "initialization_manifest.json")
    status = _read_json(selected / "status.json")
    if manifest is None or status is None:
        return {"root": selected, "manifest": manifest or {}, "status": status or {}}
    return {"root": selected, "manifest": manifest, "status": status}


def _read_book_runtime(database_path: Path, book_id: str, edition_id: str) -> dict[str, Any]:
    value: dict[str, Any] = {
        "chapter_count": 0,
        "edition_count": 0,
        "handoff": None,
    }
    if not database_path.is_file():
        return value
    try:
        uri = f"{database_path.resolve().as_uri()}?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM chapters WHERE book_id=?", (book_id,)
            ).fetchone()
            value["chapter_count"] = 0 if row is None else int(row["count"])
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM editions WHERE book_id=?", (book_id,)
            ).fetchone()
            value["edition_count"] = 0 if row is None else int(row["count"])
            try:
                handoff = connection.execute(
                    "SELECT handoff_id, status, created_at, completed_at, error_message, "
                    "prompt_path, task_directory "
                    "FROM workflow_handoffs WHERE book_id=? AND edition_id=? "
                    "AND handoff_type='NOVEL_INITIALIZATION' "
                    "ORDER BY created_at DESC LIMIT 1",
                    (book_id, edition_id),
                ).fetchone()
            except sqlite3.OperationalError:
                handoff = None
            value["handoff"] = None if handoff is None else dict(handoff)
    except (OSError, sqlite3.Error):
        return value
    return value


def studio_readiness(layout: BookLayout, record: BookRecord) -> StudioReadinessView:
    paths = layout.for_book(record.book_id)
    runtime = _read_book_runtime(paths.database, record.book_id, record.active_edition_id)
    handoff = runtime.get("handoff") or {}
    initialization = _latest_initialization(paths, record.active_edition_id)
    missing: list[str] = []
    if int(runtime.get("chapter_count") or 0) < 1:
        missing.append("正文尚未建立有效章节")
    initialization_id: str | None = None
    initialization_status: str | None = None
    updated_at: str | None = None
    if initialization is None:
        missing.append("尚未建立小说初始化结果")
    else:
        root = Path(initialization["root"])
        manifest = dict(initialization.get("manifest") or {})
        status_payload = dict(initialization.get("status") or {})
        # ``readiness`` is defined as ``string | null | object`` by the output
        # schema; a string such as "BLOCKED" is a status marker, never a dict.
        readiness_payload = status_payload.get("readiness")
        if isinstance(readiness_payload, dict):
            readiness = readiness_payload
            readiness_status = str(readiness.get("status") or "")
        else:
            readiness = {}
            readiness_status = str(readiness_payload or "")
        initialization_id = str(
            manifest.get("initialization_id")
            or status_payload.get("initialization_id")
            or ""
        ) or None
        initialization_status = str(
            readiness_status
            or status_payload.get("state")
            or manifest.get("state")
            or ""
        ) or None
        updated_at = str(status_payload.get("updated_at") or "") or None
        if str(manifest.get("state") or "") != "READY":
            missing.append("初始化清单尚未达到完整就绪")
        if str(status_payload.get("state") or "") != "READY":
            missing.append("初始化状态尚未达到完整就绪")
        if readiness_status != "READY":
            missing.append("初始化验收尚未达到完整就绪")
        required_files = {
            "Source Coverage": root / "source_coverage.json",
            "Arc Manifest": root / "arc_manifest.json",
            "事件记录": root / "events.jsonl",
            "实体解析": root / "entity_resolution" / "entity_resolution_map.json",
            "当前世界模型": root / "synthesis" / "current_world_model.md",
            "核心关系图谱": root / "synthesis" / "graphs.json",
            "语义指标清单": root / "metrics" / "metric_bootstrap_manifest.json",
            "初始化验收报告": root / "reports" / "readiness_report.md",
        }
        missing.extend(
            label + "缺失"
            for label, path in required_files.items()
            if not path.is_file()
        )
        arc_manifest = _read_json(root / "arc_manifest.json") or {}
        arcs = arc_manifest.get("arcs")
        if not isinstance(arcs, list) or not arcs:
            missing.append("Arc 初始化任务缺失")
        else:
            for arc in arcs:
                arc_id = str(arc.get("arc_id") or "") if isinstance(arc, dict) else ""
                if not arc_id:
                    missing.append("Arc 初始化任务标识缺失")
                    continue
                operation_id = f"{initialization_id or ''}-arc-{arc_id}"
                if not re.fullmatch(r"[A-Za-z0-9._-]+", operation_id):
                    missing.append(f"Arc {arc_id} 的任务标识无效")
                    continue
                output = (
                    paths.edition(record.active_edition_id)
                    .operation(operation_id)
                    .output
                    / "output.json"
                )
                if not output.is_file():
                    missing.append(f"Arc {arc_id} 的语义提取结果缺失")
        for label, key in (
            ("Source Coverage", "source_mapping_coverage"),
            ("Arc Coverage", "arc_output_coverage"),
            ("章节语义覆盖", "chapter_semantic_feature_coverage"),
        ):
            if float(readiness.get(key) or 0.0) < 1.0:
                missing.append(f"{label}尚未达到 100%")
        if str(readiness.get("metric_bootstrap_status") or "") != "COMPLETE":
            missing.append("语义指标初始化尚未完成")
        if not bool(readiness.get("core_graphs_complete")):
            missing.append("核心世界图谱尚未完成")
        if not bool(readiness.get("protagonist_confirmed")):
            missing.append("主角当前状态尚未确认")
        if not bool(readiness.get("current_thread_confirmed")):
            missing.append("当前主线程尚未确认")
        missing.extend(str(item) for item in readiness.get("blocking_reasons") or [])
    missing = list(dict.fromkeys(item for item in missing if item))
    ready = not missing
    handoff_status = str(handoff.get("status") or "") or None
    if ready:
        status = "READY"
        summary = "初始化已完整验收，可以进入小说工作台。"
    elif handoff_status in {"CLAIMED", "RUNNING"}:
        status = "INITIALIZING"
        summary = "Codex 正在处理初始化任务，页面会自动更新进度。"
    elif handoff_status == "WAITING_FOR_USER":
        status = "INITIALIZATION_REVIEW"
        summary = "初始化需要你的确认后才能继续。"
    elif handoff_status == "READY_FOR_CODEX":
        status = "INITIALIZATION_READY_FOR_CODEX"
        summary = "初始化任务已准备好，等待在 Codex 桌面端领取。"
    elif handoff_status in {"FAILED", "STALE", "CANCELLED"}:
        status = "FAILED"
        summary = "上一次初始化没有完成，可以查看原因并重新准备。"
    elif initialization is not None or handoff_status == "COMPLETED":
        status = "NEEDS_REPAIR"
        summary = "初始化尚未完整，补齐关键结果后才能进入工作台。"
    else:
        status = "INITIALIZATION_REQUIRED"
        summary = "正文已读取，还需要完成小说初始化才能开始创作。"
    return StudioReadinessView(
        book_id=record.book_id,
        status=status,
        ready=ready,
        missing_requirements=tuple(missing),
        initialization_id=initialization_id,
        initialization_status=initialization_status,
        author_summary=summary,
        handoff_id=str(handoff.get("handoff_id") or "") or None,
        handoff_status=handoff_status,
        updated_at=updated_at or (str(handoff.get("created_at") or "") or None),
    )


_STATE_LABELS = {
    "READY": "可创作",
    "DISCOVERED": "待初始化",
    "INITIALIZATION_REQUIRED": "待初始化",
    "INITIALIZATION_READY_FOR_CODEX": "等待处理",
    "INITIALIZING": "初始化中",
    "INITIALIZATION_REVIEW": "等待确认",
    "FAILED": "初始化失败",
    "NEEDS_REPAIR": "需要修复",
}


def _instruction_availability(handoff: dict[str, Any]) -> tuple[bool, str | None]:
    """Check the instruction file with the same fallback order as copy_instruction."""

    if not handoff:
        return False, "交接任务尚未创建"
    task_directory = str(handoff.get("task_directory") or "")
    if not task_directory:
        return False, "交接任务目录缺失"
    resolved = resolve_instruction_path(Path(task_directory), handoff.get("prompt_path"))
    if resolved is None:
        return False, "交接任务存在，但交接指令文件缺失。请重新准备初始化任务。"
    return True, None


def _registered_entry(layout: BookLayout, record: BookRecord) -> LibraryCatalogEntry:
    paths = layout.for_book(record.book_id)
    runtime = _read_book_runtime(paths.database, record.book_id, record.active_edition_id)
    readiness = studio_readiness(layout, record)
    instruction_available, instruction_error = _instruction_availability(
        runtime.get("handoff") or {}
    )
    if readiness.ready:
        action, action_label = "OPEN_STUDIO", "进入小说工作台"
    elif readiness.handoff_status in _ACTIVE_HANDOFF_STATUSES:
        action, action_label = "VIEW_INITIALIZATION", "查看初始化进度"
    else:
        action, action_label = "PREPARE_INITIALIZATION", "准备初始化"
    return LibraryCatalogEntry(
        catalog_id=f"book:{record.book_id}",
        book_id=record.book_id,
        title=record.title,
        source_path=str(record.source_origin or record.source_root),
        source_kind=record.source_origin_kind or "LIBRARY_COPY",
        state=readiness.status,
        state_label=_STATE_LABELS[readiness.status],
        studio_ready=readiness.ready,
        primary_action=action,
        primary_action_label=action_label,
        modified_at=readiness.updated_at,
        chapter_count=int(runtime["chapter_count"]),
        edition_count=int(runtime["edition_count"]),
        active_edition=record.active_edition_id,
        book_kind=record.book_kind.value,
        creation_mode=record.creation_mode.value,
        initialization_status=readiness.initialization_status,
        initialization_id=readiness.initialization_id,
        handoff_id=readiness.handoff_id,
        handoff_status=readiness.handoff_status,
        instruction_available=instruction_available,
        instruction_error=instruction_error,
        missing_requirements=readiness.missing_requirements,
        author_summary=readiness.author_summary,
        technical={
            "book_id": record.book_id,
            "initialization_status": readiness.initialization_status,
            "handoff_status": readiness.handoff_status,
            "instruction_available": instruction_available,
            "instruction_error": instruction_error,
        },
    )


def build_library_catalog(
    layout: BookLayout,
    discovery_root: Path,
    *,
    scope: CatalogScope = CatalogScope.AUTHOR,
) -> LibraryCatalogView:
    discovery = BookDiscoveryService(discovery_root)
    records = BookRegistry(layout).list()
    linked_origins = {
        _normalized_path(record.source_origin): record.book_id
        for record in records
        if record.source_origin is not None
    }
    legacy_keys: dict[tuple[str, int], list[str]] = {}
    for record in records:
        key = _legacy_source_key(record)
        if key is not None:
            legacy_keys.setdefault(key, []).append(record.book_id)
    visible_records = [
        record
        for record in records
        if (scope is CatalogScope.AUTHOR and record.book_kind is BookKind.AUTHOR)
        or (scope is CatalogScope.TECHNICAL and record.book_kind is not BookKind.AUTHOR)
    ]
    entries = [_registered_entry(layout, record) for record in visible_records]
    for candidate in discovery.scan() if scope is CatalogScope.AUTHOR else []:
        linked_book_id = linked_origins.get(_normalized_path(Path(candidate.source_path)))
        if linked_book_id is None:
            key = (candidate.source_filename.casefold(), candidate.file_size)
            legacy_matches = legacy_keys.get(key, [])
            linked_book_id = legacy_matches[0] if len(legacy_matches) == 1 else None
        if linked_book_id:
            continue
        entries.append(
            LibraryCatalogEntry(
                catalog_id=f"candidate:{candidate.candidate_id}",
                candidate_id=candidate.candidate_id,
                title=candidate.display_title,
                source_path=candidate.source_path,
                source_kind=candidate.source_kind,
                state="DISCOVERED",
                state_label=_STATE_LABELS["DISCOVERED"],
                studio_ready=False,
                primary_action="INGEST_AND_PREPARE",
                primary_action_label="开始初始化",
                modified_at=candidate.modified_at,
                author_summary="已在书籍目录中发现正文，确认后才会读取并建立初始化任务。",
                technical={
                    "candidate_id": candidate.candidate_id,
                    "source_kind": candidate.source_kind,
                    "file_size": candidate.file_size,
                },
            )
        )
    entries.sort(
        key=lambda item: (
            0
            if item.studio_ready
            else 1
            if item.state in {"INITIALIZING", "INITIALIZATION_REVIEW"}
            else 2,
            item.title.casefold(),
            item.catalog_id,
        )
    )
    revision_parts = [
        f"{item.catalog_id}:{item.state}:{item.modified_at or ''}:{item.handoff_status or ''}"
        for item in entries
    ]
    return LibraryCatalogView(
        library_root=str(layout.library_root),
        discovery_root=str(discovery.discovery_root),
        supported_formats=discovery.extensions,
        entries=tuple(entries),
        revision="|".join(revision_parts),
        scope=scope,
    )


def find_candidate(catalog: LibraryCatalogView, candidate_id: str) -> LibraryCatalogEntry | None:
    return next((item for item in catalog.entries if item.candidate_id == candidate_id), None)


def suggest_book_id(candidate: LibraryCatalogEntry, layout: BookLayout) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", candidate.title).strip("-._").lower()
    suffix = str(candidate.candidate_id or "candidate")[-10:].lower()
    if not base:
        base = f"book-{suffix}"
    if not (layout.library_root / base).exists():
        return base
    return f"{base}-{suffix}"


__all__ = [
    "BookDiscoveryService",
    "CatalogScope",
    "DiscoveredBookCandidate",
    "LibraryCatalogEntry",
    "LibraryCatalogView",
    "StudioReadinessView",
    "build_library_catalog",
    "find_candidate",
    "studio_readiness",
    "suggest_book_id",
]
