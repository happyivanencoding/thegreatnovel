"""Non-destructive book classification planning and explicit metadata updates."""

from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.registry import BookKind, BookRecord, BookRegistry, CreationMode
from novel_authoring.utils import json_dumps, utc_now

APPLY_CONFIRMATION = "APPLY_BOOK_CLASSIFICATION"
_TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt"}


@dataclass(frozen=True, slots=True)
class ClassificationSuggestion:
    book_id: str
    title: str
    source_origin: str | None
    chapter_count: int
    edition_count: int
    initialization_status: str | None
    current_book_kind: str
    suggested_book_kind: str
    suggested_creation_mode: str
    confidence: str
    reason: str
    evidence: tuple[str, ...]
    suspected_duplicate_of: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["evidence"] = list(self.evidence)
        value["suspected_duplicate_of"] = list(self.suspected_duplicate_of)
        return value


def _runtime_counts(record: BookRecord) -> tuple[int, int]:
    database = record.root / "_system" / "state.sqlite3"
    if not database.is_file():
        return 0, 0
    try:
        uri = f"{database.resolve().as_uri()}?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            chapters = connection.execute(
                "SELECT COUNT(*) FROM chapters WHERE book_id=?", (record.book_id,)
            ).fetchone()
            editions = connection.execute(
                "SELECT COUNT(*) FROM editions WHERE book_id=?", (record.book_id,)
            ).fetchone()
    except sqlite3.Error:
        return 0, 0
    return int(chapters[0]) if chapters else 0, int(editions[0]) if editions else 0


def _evidence_hits(records: list[BookRecord], roots: tuple[Path, ...]) -> dict[str, list[str]]:
    if not records:
        return {}
    pattern = re.compile(
        r"(?<![A-Za-z0-9._-])(" + "|".join(
            re.escape(item.book_id) for item in sorted(records, key=lambda row: -len(row.book_id))
        ) + r")(?![A-Za-z0-9._-])"
    )
    hits: dict[str, list[str]] = defaultdict(list)
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if (
                not path.is_file()
                or path.suffix.casefold() not in _TEXT_SUFFIXES
                or {
                    "artifacts",
                    "phase5_live_library",
                    "phase6_live_library",
                    "phase5_live_hidden",
                    "phase6_live_hidden",
                }
                & {part.casefold() for part in path.parts}
            ):
                continue
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for book_id in set(pattern.findall(text)):
                hits[book_id].append(str(path.resolve()))
    return {key: sorted(set(value))[:12] for key, value in hits.items()}


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _suggest(
    record: BookRecord,
    evidence: list[str],
    *,
    project_root: Path,
) -> tuple[BookKind, str, str, list[str]]:
    if record.book_kind is not BookKind.UNCLASSIFIED:
        return record.book_kind, "HIGH", "book.yaml 已有权威分类", evidence
    evidence_paths = [Path(item) for item in evidence]
    phase_evidence = [
        item
        for item in evidence_paths
        if (_is_within(item, project_root / "scripts") and item.name.startswith("phase"))
        or (
            _is_within(item, project_root / "benchmark")
            and (
                item.name.startswith(("phase4", "phase5", "phase6"))
                or any(
                    part.casefold().startswith(("phase4", "phase5", "phase6"))
                    for part in item.parts
                )
                or "live_phase5" in {part.casefold() for part in item.parts}
            )
        )
    ]
    test_evidence = [item for item in evidence_paths if _is_within(item, project_root / "tests")]
    origin = record.source_origin
    if origin is not None and _is_within(origin, project_root / "book"):
        return BookKind.AUTHOR, "HIGH", "来源位于正式 production discovery root", [str(origin)]
    if origin is not None and any(
        part.casefold().startswith("acceptance") for part in origin.parts
    ):
        return BookKind.TEST, "HIGH", "来源位于显式 acceptance 隔离目录", [str(origin)]
    if test_evidence:
        return (
            BookKind.TEST,
            "HIGH",
            "自动化测试明确引用该 book_id",
            [str(item) for item in test_evidence],
        )
    legacy = " ".join(str(item) for item in record.legacy_locations).casefold()
    if "demo" in legacy and "temp" in legacy:
        return BookKind.DEMO, "HIGH", "legacy 记录明确来自临时 Demo 运行", evidence
    if phase_evidence:
        return (
            BookKind.BENCHMARK,
            "HIGH",
            "Benchmark/Phase 脚本或验收报告明确引用该 book_id",
            [str(item) for item in phase_evidence],
        )
    if re.match(r"^phase[456]-", record.book_id, flags=re.IGNORECASE):
        return (
            BookKind.BENCHMARK,
            "MEDIUM",
            "book_id 的 Phase 命名仅作为辅助建议，仍需显式 mapping 确认",
            evidence,
        )
    if any("benchmark" in item.casefold() for item in record.source_files):
        return BookKind.BENCHMARK, "MEDIUM", "source 文件名提供 Benchmark 辅助证据", evidence
    if "demo" in record.book_id.casefold() and evidence:
        return BookKind.DEMO, "MEDIUM", "Demo 命名与文档引用共同提供辅助证据", evidence
    return BookKind.UNCLASSIFIED, "UNKNOWN", "现有证据不足，等待作者显式分类", evidence


def build_classification_plan(
    layout: BookLayout,
    *,
    project_root: Path,
) -> dict[str, Any]:
    project_root = Path(project_root).expanduser().resolve()
    records = BookRegistry(layout).list()
    hits = _evidence_hits(
        records,
        tuple(project_root / name for name in ("scripts", "tests", "benchmark", "docs")),
    )
    origins: dict[str, list[str]] = defaultdict(list)
    for record in records:
        if record.source_origin is not None:
            origins[str(record.source_origin).casefold()].append(record.book_id)
    suggestions: list[ClassificationSuggestion] = []
    for record in records:
        chapter_count, edition_count = _runtime_counts(record)
        suggested, confidence, reason, evidence = _suggest(
            record,
            hits.get(record.book_id, []),
            project_root=project_root,
        )
        duplicate_ids = (
            origins.get(str(record.source_origin).casefold(), [])
            if record.source_origin is not None
            else []
        )
        suggestions.append(
            ClassificationSuggestion(
                book_id=record.book_id,
                title=record.title,
                source_origin=None if record.source_origin is None else str(record.source_origin),
                chapter_count=chapter_count,
                edition_count=edition_count,
                initialization_status=record.readiness_status,
                current_book_kind=record.book_kind.value,
                suggested_book_kind=suggested.value,
                suggested_creation_mode=record.creation_mode.value,
                confidence=confidence,
                reason=reason,
                evidence=tuple(evidence),
                suspected_duplicate_of=tuple(
                    sorted(item for item in duplicate_ids if item != record.book_id)
                ),
            )
        )
    counts = {
        kind.value: sum(1 for item in suggestions if item.suggested_book_kind == kind.value)
        for kind in BookKind
    }
    return {
        "schema_version": "library-classification-plan-v1",
        "generated_at": utc_now(),
        "library_root": str(layout.library_root),
        "registered_book_count": len(suggestions),
        "suggested_counts": counts,
        "automatic_apply": False,
        "suggestions": [item.to_dict() for item in suggestions],
    }


def write_classification_plan(
    plan: dict[str, Any], *, json_path: Path, markdown_path: Path
) -> tuple[Path, Path]:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json_dumps(plan, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# Library Classification Plan",
        "",
        f"- Registered books: {plan['registered_book_count']}",
        "- Automatic apply: disabled",
        "- Evidence-first only; no deletion, move, merge or rename is performed.",
        "",
        "| book_id | title | suggested | confidence | chapters | editions | reason | duplicates |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for item in plan["suggestions"]:
        lines.append(
            "| {book_id} | {title} | {suggested_book_kind} | {confidence} | "
            "{chapter_count} | {edition_count} | {reason} | {duplicates} |".format(
                **item,
                duplicates=", ".join(item["suspected_duplicate_of"]) or "—",
            )
        )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return json_path, markdown_path


def set_book_classification(
    layout: BookLayout,
    book_id: str,
    *,
    book_kind: BookKind,
    creation_mode: CreationMode | None = None,
) -> BookRecord:
    registry = BookRegistry(layout)
    paths = layout.for_book(book_id)
    values = registry.read(book_id)
    values["book_kind"] = book_kind.value
    if creation_mode is not None:
        values["creation_mode"] = creation_mode.value
    values["updated_at"] = utc_now()
    registry.write(paths, values)
    registry.write_readme(paths, values)
    return registry.record(book_id)


def apply_classification_mapping(
    layout: BookLayout,
    mapping_path: Path,
    *,
    confirm: str,
) -> list[BookRecord]:
    if confirm != APPLY_CONFIRMATION:
        raise ValueError(f"需要精确确认词 {APPLY_CONFIRMATION}")
    payload = json.loads(Path(mapping_path).read_text(encoding="utf-8"))
    mappings = payload.get("mappings") if isinstance(payload, dict) else None
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("分类 mapping 必须包含非空 mappings 列表")
    requested: list[tuple[str, BookKind, CreationMode | None]] = []
    seen: set[str] = set()
    registry = BookRegistry(layout)
    known = {item.book_id for item in registry.list()}
    for item in mappings:
        if not isinstance(item, dict):
            raise ValueError("每条分类 mapping 必须是 object")
        book_id = str(item.get("book_id") or "")
        if not book_id or book_id in seen or book_id not in known:
            raise ValueError(f"分类 mapping 的 book_id 无效或重复: {book_id}")
        seen.add(book_id)
        kind = BookKind(str(item.get("book_kind") or ""))
        mode_value = item.get("creation_mode")
        mode = None if mode_value is None else CreationMode(str(mode_value))
        requested.append((book_id, kind, mode))
    return [
        set_book_classification(layout, book_id, book_kind=kind, creation_mode=mode)
        for book_id, kind, mode in requested
    ]


__all__ = [
    "APPLY_CONFIRMATION",
    "ClassificationSuggestion",
    "apply_classification_mapping",
    "build_classification_plan",
    "set_book_classification",
    "write_classification_plan",
]
