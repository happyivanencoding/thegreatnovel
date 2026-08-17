"""Deterministic adapter for the offline Reference Corpus Program-Deep package.

This module deliberately does not infer literary meaning.  It freezes the
existing Google Drive preparation/index inputs, creates locator-complete
pending ledgers, merges bounded semantic-worker artifacts, and exposes
structural validation and machine-package compilation for the new parallel
corpus.  The old Reference Corpus and all authoring/runtime paths remain
outside this module's write scope.
"""

from __future__ import annotations

import json
import shutil
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import yaml

PROGRAM_MANIFEST_SCHEMA = "story-program-manifest-v1"
LEDGER_SCHEMA = "story-program-chapter-ledger-v1"
ARC_SCHEMA = "story-program-arc-v1"
PAYOFF_SCHEMA = "story-program-payoff-v1"
DNA_SCHEMA = "book-program-dna-v1"


class ProgramDeepError(ValueError):
    """Raised when a Program-Deep input or artifact cannot be trusted."""


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class SegmentRecord:
    segment_id: str
    ordinal: int
    heading: str
    start_line: int
    end_line: int
    start_char: int
    end_char: int
    char_count: int


@dataclass(frozen=True)
class SourceRecord:
    source_book_id: str
    source_id: str
    distill_id: str
    title: str
    category: str
    source_path: str
    normalized_path: Path
    chapter_index_path: Path
    line_count: int
    segments: tuple[SegmentRecord, ...]
    input_warnings: tuple[str, ...]

    @property
    def segment_count(self) -> int:
        return len(self.segments)


def _mapping(value: Any, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ProgramDeepError(f"{label} 必须是 mapping")
    return cast(JsonObject, value)


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ProgramDeepError(f"{label} 必须是 list")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProgramDeepError(f"{label} 必须是非空文本")
    return value


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ProgramDeepError(f"{label} 必须是 >= {minimum} 的整数")
    return cast(int, value)


def _read_json(path: Path) -> JsonObject:
    try:
        return _mapping(json.loads(path.read_text(encoding="utf-8")), str(path))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProgramDeepError(f"无法读取 JSON：{path}：{exc}") from exc


def _read_yaml(path: Path) -> JsonObject:
    try:
        return _mapping(yaml.safe_load(path.read_text(encoding="utf-8")), str(path))
    except (OSError, yaml.YAMLError) as exc:
        raise ProgramDeepError(f"无法读取 YAML：{path}：{exc}") from exc


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> list[JsonObject]:
    if not path.is_file():
        return []
    rows: list[JsonObject] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(_mapping(json.loads(line), f"{path}:{number}"))
        except json.JSONDecodeError as exc:
            raise ProgramDeepError(f"JSONL 无法解析：{path}:{number}：{exc}") from exc
    return rows


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _selection_sources(corpus_root: Path) -> list[JsonObject]:
    path = corpus_root / "selection" / "corpus-sources-v0.confirmed.yaml"
    payload = _read_yaml(path)
    expected = _integer(payload.get("source_count"), "selection.source_count", minimum=1)
    sources = [
        _mapping(item, f"selection.sources[{index}]")
        for index, item in enumerate(_list(payload.get("sources"), "selection.sources"))
    ]
    if expected != len(sources):
        raise ProgramDeepError(f"selection source_count={expected} 但实际 sources={len(sources)}")
    ids = [_text(item.get("source_book_id"), "source_book_id") for item in sources]
    if len(ids) != len(set(ids)):
        raise ProgramDeepError("selection 存在重复 source_book_id")
    return sources


def _index_source(index_path: Path) -> JsonObject:
    payload = _read_json(index_path)
    candidates = _list(payload.get("sources"), f"{index_path}.sources")
    if len(candidates) != 1:
        raise ProgramDeepError(f"{index_path} 必须包含唯一 source entry，实际 {len(candidates)}")
    return _mapping(candidates[0], f"{index_path}.sources[0]")


def _segments(index_path: Path, source: JsonObject) -> tuple[SegmentRecord, ...]:
    values = _list(source.get("segments"), f"{index_path}.segments")
    result: list[SegmentRecord] = []
    previous_ordinal = 0
    seen_ids: set[str] = set()
    for index, value in enumerate(values):
        item = _mapping(value, f"{index_path}.segments[{index}]")
        segment_id = _text(item.get("segment_id"), "segment_id")
        ordinal = _integer(item.get("ordinal"), f"{segment_id}.ordinal", minimum=1)
        if ordinal <= previous_ordinal:
            raise ProgramDeepError(f"{index_path}: segment ordinal 不严格递增：{segment_id}")
        if segment_id in seen_ids:
            raise ProgramDeepError(f"{index_path}: segment_id 重复：{segment_id}")
        start_line = _integer(item.get("start_line"), f"{segment_id}.start_line", minimum=1)
        end_line = _integer(item.get("end_line"), f"{segment_id}.end_line", minimum=1)
        if end_line < start_line:
            raise ProgramDeepError(f"{index_path}: {segment_id} line range 反向")
        result.append(
            SegmentRecord(
                segment_id=segment_id,
                ordinal=ordinal,
                heading=_text(item.get("heading"), f"{segment_id}.heading"),
                start_line=start_line,
                end_line=end_line,
                start_char=_integer(item.get("start_char"), f"{segment_id}.start_char"),
                end_char=_integer(item.get("end_char"), f"{segment_id}.end_char"),
                char_count=_integer(item.get("char_count"), f"{segment_id}.char_count"),
            )
        )
        previous_ordinal = ordinal
        seen_ids.add(segment_id)
    declared = _integer(source.get("segment_count"), f"{index_path}.segment_count", minimum=1)
    if declared != len(result):
        raise ProgramDeepError(f"{index_path}: segment_count={declared} != actual={len(result)}")
    return tuple(result)


def load_source_records(corpus_root: Path | str, operations_root: Path | str) -> list[SourceRecord]:
    """Load the frozen 26-book selection and its read-only preparation indexes."""

    corpus = Path(corpus_root).expanduser().resolve()
    operations = Path(operations_root).expanduser().resolve()
    records: list[SourceRecord] = []
    for selection in _selection_sources(corpus):
        source_book_id = _text(selection.get("source_book_id"), "source_book_id")
        manifest_path = corpus / "machine" / "manifests" / f"{source_book_id}.json"
        machine = _read_json(manifest_path)
        if machine.get("source_book_id") != source_book_id:
            raise ProgramDeepError(f"{manifest_path}: source_book_id 不匹配")
        prep = operations / "preparations" / source_book_id
        index_path = prep / "chapter_index.json"
        if not index_path.is_file():
            raise ProgramDeepError(f"缺少 canonical chapter index：{index_path}")
        index_source = _index_source(index_path)
        normalized_path = Path(
            _text(index_source.get("normalized_path"), f"{source_book_id}.normalized_path")
        )
        if not normalized_path.is_file():
            raise ProgramDeepError(f"缺少 normalized source：{normalized_path}")
        segments = _segments(index_path, index_source)
        warnings: list[str] = []
        parse_warning = selection.get("parse_warning")
        if isinstance(parse_warning, str) and parse_warning.strip():
            warnings.append(parse_warning.strip())
        if selection.get("source_path") == "UNKNOWN":
            warnings.append("selection.source_path=UNKNOWN；采用 chapter_index.input_path")
        records.append(
            SourceRecord(
                source_book_id=source_book_id,
                source_id=_text(machine.get("source_id"), f"{source_book_id}.source_id"),
                distill_id=_text(machine.get("distill_id"), f"{source_book_id}.distill_id"),
                title=_text(machine.get("title"), f"{source_book_id}.title"),
                category=_text(machine.get("category"), f"{source_book_id}.category"),
                source_path=_text(index_source.get("input_path"), f"{source_book_id}.input_path"),
                normalized_path=normalized_path,
                chapter_index_path=index_path,
                line_count=_integer(
                    index_source.get("lines"), f"{source_book_id}.lines", minimum=1
                ),
                segments=segments,
                input_warnings=tuple(warnings),
            )
        )
    return records


def _source_payload(record: SourceRecord) -> JsonObject:
    return {
        "source_book_id": record.source_book_id,
        "source_id": record.source_id,
        "distill_id": record.distill_id,
        "title": record.title,
        "category": record.category,
        "source_path": record.source_path,
        "normalized_path": str(record.normalized_path),
        "chapter_index_path": str(record.chapter_index_path),
        "line_count": record.line_count,
        "canonical_unit_kind": "INDEX_SEGMENT",
        "canonical_unit_count": record.segment_count,
        "input_warnings": list(record.input_warnings),
        "status": "PENDING_SEMANTIC",
    }


def _locator(record: SourceRecord, segment: SegmentRecord) -> JsonObject:
    return {
        "source_book_id": record.source_book_id,
        "source_id": record.source_id,
        "distill_id": record.distill_id,
        "segment_id": segment.segment_id,
        "line_start": segment.start_line,
        "line_end": segment.end_line,
    }


def _skeleton_row(record: SourceRecord, segment: SegmentRecord) -> JsonObject:
    return {
        "schema_version": LEDGER_SCHEMA,
        "source_book_id": record.source_book_id,
        "source_chapter_id": segment.segment_id,
        "canonical_unit_kind": "INDEX_SEGMENT",
        "chapter_ordinal": segment.ordinal,
        "source_locator": _locator(record, segment),
        "heading_observed": segment.heading,
        "coverage_status": "PENDING_SEMANTIC",
        "one_line_story": "UNKNOWN",
        "primary_function": "UNKNOWN",
        "protagonist_goal": "UNKNOWN",
        "pressure_or_opportunity": "UNKNOWN",
        "choice_or_action": "UNKNOWN",
        "immediate_result": "UNKNOWN",
        "reader_payoff_channels": [],
        "immediate_upside": None,
        "state_deltas": {},
        "knowledge_gap": "尚未完成该 canonical unit 的语义蒸馏。",
    }


def _skeleton_evidence(record: SourceRecord, segment: SegmentRecord) -> JsonObject:
    return {
        "evidence_id": f"{record.source_book_id}--{segment.segment_id}",
        **_locator(record, segment),
        "observation_summary": "仅建立 locator；语义观察待 bounded worker 完成。",
        "status": "PENDING_SEMANTIC",
    }


def initialize_program_deep(
    corpus_root: Path | str,
    operations_root: Path | str,
    output_root: Path | str,
    *,
    raw_root: Path | str | None = None,
) -> dict[str, Any]:
    """Create a locator-complete, resumable Program-Deep skeleton.

    Existing output is never overwritten.  This makes reruns safe after a
    worker interruption and keeps the semantic workers' isolated artifacts as
    the only inputs to later merges.
    """

    records = load_source_records(corpus_root, operations_root)
    output = Path(output_root).expanduser().resolve()
    manifest_path = output / "manifest.yaml"
    if manifest_path.exists():
        existing = _read_yaml(manifest_path)
        if existing.get("source_count") != len(records):
            raise ProgramDeepError(
                "已有 Program-Deep manifest 的 source_count 与当前 freeze 不一致"
            )
        return {"status": "EXISTING", "output_root": str(output), "source_count": len(records)}

    output.mkdir(parents=True, exist_ok=True)
    manifest: JsonObject = {
        "schema_version": PROGRAM_MANIFEST_SCHEMA,
        "program_id": "reference-corpus-program-deep-v1",
        "status": "SKELETON_READY",
        "knowledge_boundary": "REFERENCE_ONLY",
        "source_count": len(records),
        "unit_kind": "INDEX_SEGMENT",
        "input": {
            "corpus_root": str(Path(corpus_root).expanduser().resolve()),
            "operations_root": str(Path(operations_root).expanduser().resolve()),
            "raw_root": str(Path(raw_root).expanduser().resolve()) if raw_root else None,
        },
        "source_freeze": "selection/corpus-sources-v0.confirmed.yaml",
        "new_content_hashes": False,
        "canon_committed": False,
        "edition_activated": False,
        "sources": [_source_payload(record) for record in records],
    }
    manifest_path.write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
        newline="\n",
    )
    progress: JsonObject = {
        "schema_version": "story-program-progress-v1",
        "program_id": manifest["program_id"],
        "books": {},
    }
    for record in records:
        book_root = output / "books" / record.source_book_id
        book_root.mkdir(parents=True, exist_ok=True)
        ledger_path = book_root / "chapter-ledger.jsonl"
        evidence_path = book_root / "evidence-index.jsonl"
        if not ledger_path.exists():
            _write_jsonl(
                ledger_path, (_skeleton_row(record, segment) for segment in record.segments)
            )
        if not evidence_path.exists():
            _write_jsonl(
                evidence_path,
                (_skeleton_evidence(record, segment) for segment in record.segments),
            )
        progress["books"][record.source_book_id] = {
            "stage": "SKELETON_READY",
            "completed_ranges": [],
            "remaining_ranges": [[1, record.segment_count]],
            "last_completed_artifact": str(ledger_path),
            "status": "PENDING_SEMANTIC",
            "canonical_unit_count": record.segment_count,
        }
    _write_json(output / "operations" / "progress.json", progress)
    return {
        "status": "CREATED",
        "output_root": str(output),
        "source_count": len(records),
        "canonical_unit_count": sum(record.segment_count for record in records),
    }


def _output_sources(output_root: Path) -> dict[str, JsonObject]:
    manifest = _read_yaml(output_root / "manifest.yaml")
    return {
        _text(item.get("source_book_id"), "manifest.sources.source_book_id"): _mapping(
            item, "manifest.sources.item"
        )
        for item in _list(manifest.get("sources"), "manifest.sources")
    }


def _valid_worker_row(row: JsonObject, records: Mapping[str, SourceRecord]) -> tuple[str, str]:
    source_book_id = _text(row.get("source_book_id"), "worker.source_book_id")
    if source_book_id not in records:
        raise ProgramDeepError(f"worker row 使用了未冻结来源：{source_book_id}")
    locator = _mapping(row.get("source_locator"), f"{source_book_id}.source_locator")
    segment_id = _text(locator.get("segment_id"), f"{source_book_id}.segment_id")
    known = {segment.segment_id: segment for segment in records[source_book_id].segments}
    segment = known.get(segment_id)
    if segment is None:
        raise ProgramDeepError(f"worker row locator 不存在：{source_book_id}/{segment_id}")
    if locator.get("source_id") != records[source_book_id].source_id:
        raise ProgramDeepError(f"worker row source_id 不匹配：{source_book_id}/{segment_id}")
    if locator.get("distill_id") != records[source_book_id].distill_id:
        raise ProgramDeepError(f"worker row distill_id 不匹配：{source_book_id}/{segment_id}")
    if (
        locator.get("line_start") != segment.start_line
        or locator.get("line_end") != segment.end_line
    ):
        raise ProgramDeepError(f"worker row line locator 不匹配：{source_book_id}/{segment_id}")
    return source_book_id, segment_id


def _semantic_row(row: Mapping[str, Any]) -> bool:
    status = row.get("coverage_status", row.get("status"))
    story = row.get("one_line_story")
    return (
        status in {"SEMANTIC_COMPLETE", "COMPLETE", "DISTILLED"}
        and isinstance(story, str)
        and story != "UNKNOWN"
    )


def _reject_obvious_template_rows(book_id: str, rows: Sequence[Mapping[str, Any]]) -> None:
    semantic_stories = [str(row["one_line_story"]) for row in rows if _semantic_row(row)]
    if len(semantic_stories) < 20:
        return
    counts = Counter(semantic_stories)
    top_story, top_count = counts.most_common(1)[0]
    if len(counts) <= 8 and top_count / len(semantic_stories) >= 0.8:
        raise ProgramDeepError(
            f"{book_id}: semantic rows 明显模板化；{top_count}/{len(semantic_stories)} "
            f"行复用同一 one_line_story：{top_story}"
        )
    template_markers = (
        "当前局面的局部推进",
        "局部文本显示",
        "读者获得POWER_VERIFICATION",
        "本段把",
        "段尾转为",
    )
    marker_rows = sum(
        any(marker in story for marker in template_markers) for story in semantic_stories
    )
    if marker_rows / len(semantic_stories) >= 0.8:
        raise ProgramDeepError(
            f"{book_id}: semantic rows 共享模板化叙述骨架；"
            f"{marker_rows}/{len(semantic_stories)} 行命中固定结构"
        )


def _ordinal_ranges(ordinals: Iterable[int]) -> list[list[int]]:
    ordered = sorted(set(ordinals))
    if not ordered:
        return []
    ranges: list[list[int]] = []
    start = previous = ordered[0]
    for ordinal in ordered[1:]:
        if ordinal != previous + 1:
            ranges.append([start, previous])
            start = ordinal
        previous = ordinal
    ranges.append([start, previous])
    return ranges


def _merge_jsonl_by_id(path: Path, rows: Iterable[JsonObject], key: str) -> None:
    combined = {str(row[key]): row for row in _read_jsonl(path) if key in row}
    for row in rows:
        if key in row:
            combined[str(row[key])] = row
    _write_jsonl(path, (combined[item] for item in sorted(combined)))


def merge_worker_artifacts(
    corpus_root: Path | str,
    operations_root: Path | str,
    output_root: Path | str,
    worker_root: Path | str,
) -> dict[str, Any]:
    """Overlay isolated worker rows onto the locator skeleton."""

    records = {
        record.source_book_id: record
        for record in load_source_records(corpus_root, operations_root)
    }
    output = Path(output_root).expanduser().resolve()
    workers = Path(worker_root).expanduser().resolve()
    if not workers.is_dir():
        raise ProgramDeepError(f"worker artifact root 不存在：{workers}")

    ledger_updates: dict[str, list[JsonObject]] = {}
    for path in sorted(workers.rglob("chapter-ledger.jsonl")):
        for row in _read_jsonl(path):
            book_id, _ = _valid_worker_row(row, records)
            ledger_updates.setdefault(book_id, []).append(row)
    for book_id, updates in ledger_updates.items():
        ledger_path = output / "books" / book_id / "chapter-ledger.jsonl"
        current = {row["source_chapter_id"]: row for row in _read_jsonl(ledger_path)}
        for row in updates:
            current[_text(row.get("source_chapter_id"), "worker.source_chapter_id")] = row
        record = records[book_id]
        ordered = [
            current[segment.segment_id]
            for segment in record.segments
            if segment.segment_id in current
        ]
        _reject_obvious_template_rows(book_id, ordered)
        _write_jsonl(ledger_path, ordered)

    arc_rows: dict[str, list[JsonObject]] = {}
    payoff_rows: dict[str, list[JsonObject]] = {}
    for path in sorted(workers.rglob("arc-map.jsonl")):
        for row in _read_jsonl(path):
            book_id = _text(row.get("source_book_id"), "arc.source_book_id")
            if book_id not in records:
                raise ProgramDeepError(f"worker arc 使用了未冻结来源：{book_id}")
            arc_rows.setdefault(book_id, []).append(row)
    for path in sorted(workers.rglob("payoff-map.jsonl")):
        for row in _read_jsonl(path):
            book_id = _text(row.get("source_book_id"), "payoff.source_book_id")
            if book_id not in records:
                raise ProgramDeepError(f"worker payoff 使用了未冻结来源：{book_id}")
            payoff_rows.setdefault(book_id, []).append(row)
    for book_id, rows in arc_rows.items():
        _merge_jsonl_by_id(output / "books" / book_id / "arc-map.jsonl", rows, "arc_id")
    for book_id, rows in payoff_rows.items():
        _merge_jsonl_by_id(output / "books" / book_id / "payoff-map.jsonl", rows, "payoff_id")

    dna_books: list[str] = []
    for path in sorted(workers.rglob("book-program-dna.yaml")):
        dna = _read_yaml(path)
        book_id_value = dna.get("source_book_id")
        book_id = (
            _text(book_id_value, "book-program-dna.source_book_id")
            if book_id_value is not None
            else path.parent.name
        )
        if book_id not in records:
            raise ProgramDeepError(f"worker Book Program DNA 使用了未冻结来源：{book_id}")
        dna.setdefault("schema_version", DNA_SCHEMA)
        destination = output / "books" / book_id / "book-program-dna.yaml"
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                yaml.safe_dump(dna, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
                newline="\n",
            )
        dna_books.append(book_id)

    progress_path = output / "operations" / "progress.json"
    progress = _read_json(progress_path) if progress_path.is_file() else {"books": {}}
    merged_books: dict[str, Any] = {}
    for book_id, record in records.items():
        rows = _read_jsonl(output / "books" / book_id / "chapter-ledger.jsonl")
        complete = sum(1 for row in rows if _semantic_row(row))
        segment_ordinals = {segment.segment_id: segment.ordinal for segment in record.segments}
        completed_ordinals = [
            segment_ordinals[str(row["source_chapter_id"])]
            for row in rows
            if _semantic_row(row) and str(row.get("source_chapter_id")) in segment_ordinals
        ]
        completed_ranges = _ordinal_ranges(completed_ordinals)
        completed_set = set(completed_ordinals)
        remaining_ranges = _ordinal_ranges(
            ordinal
            for ordinal in range(1, record.segment_count + 1)
            if ordinal not in completed_set
        )
        coverage = {
            "schema_version": "story-program-book-coverage-v1",
            "source_book_id": book_id,
            "canonical_unit_count": record.segment_count,
            "ledger_rows": len(rows),
            "semantic_complete_rows": complete,
            "completed_ranges": completed_ranges,
            "remaining_ranges": remaining_ranges,
            "status": "SEMANTIC_COMPLETE"
            if complete == record.segment_count
            else "PENDING_SEMANTIC",
            "input_warnings": list(record.input_warnings),
        }
        _write_json(output / "books" / book_id / "coverage.json", coverage)
        merged_books[book_id] = {
            "stage": "SEMANTIC_PARTIAL" if complete else "SKELETON_READY",
            "completed_ranges": completed_ranges,
            "remaining_ranges": remaining_ranges,
            "last_completed_artifact": str(output / "books" / book_id / "chapter-ledger.jsonl"),
            "status": (
                "SEMANTIC_COMPLETE" if complete == record.segment_count else "PENDING_SEMANTIC"
            ),
            "canonical_unit_count": record.segment_count,
            "semantic_complete_rows": complete,
        }
    progress["books"] = merged_books
    _write_json(progress_path, progress)
    return {
        "status": "MERGED",
        "worker_root": str(workers),
        "books_with_ledger_updates": sorted(ledger_updates),
        "books_with_arc_updates": sorted(arc_rows),
        "books_with_payoff_updates": sorted(payoff_rows),
        "books_with_program_dna_updates": sorted(set(dna_books)),
    }


def reset_book_to_skeleton(
    corpus_root: Path | str,
    operations_root: Path | str,
    output_root: Path | str,
    source_book_id: str,
    *,
    backup_label: str,
) -> dict[str, Any]:
    """Move a rejected book overlay aside and restore its pending skeleton."""

    records = {
        record.source_book_id: record
        for record in load_source_records(corpus_root, operations_root)
    }
    if source_book_id not in records:
        raise ProgramDeepError(f"未冻结来源：{source_book_id}")
    output = Path(output_root).expanduser().resolve()
    book_root = output / "books" / source_book_id
    backup_root = output / "operations" / "rejected" / backup_label / source_book_id
    if backup_root.exists():
        raise ProgramDeepError(f"rejected backup 已存在，不覆盖：{backup_root}")
    backup_root.mkdir(parents=True, exist_ok=False)
    moved: list[str] = []
    for name in (
        "chapter-ledger.jsonl",
        "arc-map.jsonl",
        "payoff-map.jsonl",
        "book-program-dna.yaml",
        "coverage.json",
    ):
        path = book_root / name
        if path.is_file():
            shutil.move(str(path), str(backup_root / name))
            moved.append(name)
    record = records[source_book_id]
    _write_jsonl(
        book_root / "chapter-ledger.jsonl",
        (_skeleton_row(record, segment) for segment in record.segments),
    )
    _write_jsonl(
        book_root / "evidence-index.jsonl",
        (_skeleton_evidence(record, segment) for segment in record.segments),
    )
    _write_json(
        book_root / "coverage.json",
        {
            "schema_version": "story-program-book-coverage-v1",
            "source_book_id": source_book_id,
            "canonical_unit_count": record.segment_count,
            "ledger_rows": record.segment_count,
            "semantic_complete_rows": 0,
            "completed_ranges": [],
            "remaining_ranges": [[1, record.segment_count]],
            "status": "PENDING_SEMANTIC",
            "input_warnings": list(record.input_warnings),
        },
    )
    progress_path = output / "operations" / "progress.json"
    progress = _read_json(progress_path)
    progress["books"][source_book_id] = {
        "stage": "SKELETON_READY",
        "completed_ranges": [],
        "remaining_ranges": [[1, record.segment_count]],
        "last_completed_artifact": str(book_root / "chapter-ledger.jsonl"),
        "status": "PENDING_SEMANTIC",
        "canonical_unit_count": record.segment_count,
        "semantic_complete_rows": 0,
    }
    _write_json(progress_path, progress)
    return {
        "status": "RESET_TO_SKELETON",
        "source_book_id": source_book_id,
        "moved_to": str(backup_root),
        "moved_artifacts": moved,
    }


def validate_program_deep(
    corpus_root: Path | str,
    operations_root: Path | str,
    output_root: Path | str,
) -> dict[str, Any]:
    """Validate structural coverage and provenance without literary scoring."""

    records = {
        record.source_book_id: record
        for record in load_source_records(corpus_root, operations_root)
    }
    output = Path(output_root).expanduser().resolve()
    manifest_sources = _output_sources(output)
    errors: list[str] = []
    warnings: list[str] = []
    books: list[JsonObject] = []
    total_complete = 0
    total_rows = 0
    for book_id, record in sorted(records.items()):
        if book_id not in manifest_sources:
            errors.append(f"manifest 缺少来源：{book_id}")
            continue
        ledger_path = output / "books" / book_id / "chapter-ledger.jsonl"
        rows = _read_jsonl(ledger_path)
        ids = [row.get("source_chapter_id") for row in rows]
        duplicates = [key for key, count in Counter(ids).items() if key is not None and count > 1]
        if duplicates:
            errors.append(f"{book_id}: ledger source_chapter_id 重复：{duplicates[:3]}")
        expected = {segment.segment_id for segment in record.segments}
        actual = {str(item) for item in ids if item is not None}
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append(f"{book_id}: ledger 缺少 {len(missing)} 个 canonical unit")
        if extra:
            errors.append(f"{book_id}: ledger 存在 {len(extra)} 个冻结范围外 unit")
        complete = 0
        for row in rows:
            try:
                _valid_worker_row(row, records)
            except ProgramDeepError as exc:
                errors.append(str(exc))
            if _semantic_row(row):
                complete += 1
        total_rows += len(rows)
        total_complete += complete
        if record.input_warnings:
            warnings.extend(f"{book_id}: {warning}" for warning in record.input_warnings)
        dna_path = output / "books" / book_id / "book-program-dna.yaml"
        books.append(
            {
                "source_book_id": book_id,
                "title": record.title,
                "canonical_units": record.segment_count,
                "ledger_rows": len(rows),
                "semantic_complete_rows": complete,
                "pending_rows": record.segment_count - complete,
                "arc_rows": len(_read_jsonl(output / "books" / book_id / "arc-map.jsonl")),
                "payoff_rows": len(_read_jsonl(output / "books" / book_id / "payoff-map.jsonl")),
                "book_program_dna": dna_path.is_file(),
                "input_warnings": list(record.input_warnings),
            }
        )
    expected_ids = set(records)
    if set(manifest_sources) != expected_ids:
        errors.append("输出 manifest 的 source_book_id 集合与当前 freeze 不一致")
    optional_fields = (
        "cost_or_tradeoff",
        "responsibility_change",
        "governance_change",
        "institutional_context",
        "maintenance_pressure",
    )
    optional_mentions: Counter[str] = Counter()
    ledger_paths = (
        (output / "books").rglob("chapter-ledger.jsonl") if (output / "books").is_dir() else []
    )
    for path in ledger_paths:
        for row in _read_jsonl(path):
            optional_mentions.update(
                field
                for field in optional_fields
                if row.get(field) not in (None, "", "UNKNOWN", "NOT_MATERIAL")
            )
    expected_total = sum(record.segment_count for record in records.values())
    complete_all = not errors and total_complete == total_rows == expected_total
    all_dna = all(item["book_program_dna"] for item in books) and len(books) == len(records)
    result = {
        "schema_version": "program-deep-validation-v1",
        "valid": not errors,
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "source_count": len(records),
        "canonical_unit_count": sum(record.segment_count for record in records.values()),
        "ledger_rows": total_rows,
        "semantic_complete_rows": total_complete,
        "pending_semantic_rows": expected_total - total_complete,
        "all_book_program_dna": all_dna,
        "cross_book_ready": complete_all and all_dna,
        "optional_pressure_mentions": dict(optional_mentions),
        "books": books,
    }
    _write_json(output / "operations" / "validation.json", result)
    return result


def _all_ledger_rows(output: Path, records: Mapping[str, SourceRecord]) -> list[JsonObject]:
    rows: list[JsonObject] = []
    for book_id in sorted(records):
        rows.extend(_read_jsonl(output / "books" / book_id / "chapter-ledger.jsonl"))
    return rows


def compile_machine_package(
    corpus_root: Path | str,
    operations_root: Path | str,
    output_root: Path | str,
) -> dict[str, Any]:
    """Compile structured Program-Deep artifacts without adding source text."""

    validation = validate_program_deep(corpus_root, operations_root, output_root)
    if validation["errors"]:
        raise ProgramDeepError(
            "Program-Deep 结构验证失败，不能 compile：\n" + "\n".join(validation["errors"])
        )
    records = {
        record.source_book_id: record
        for record in load_source_records(corpus_root, operations_root)
    }
    output = Path(output_root).expanduser().resolve()
    machine = output / "machine"
    machine.mkdir(parents=True, exist_ok=True)
    ledger_rows = _all_ledger_rows(output, records)
    _write_jsonl(machine / "chapter-ledger.jsonl", ledger_rows)
    arc_rows: list[JsonObject] = []
    payoff_rows: list[JsonObject] = []
    dna_rows: list[JsonObject] = []
    for book_id in sorted(records):
        arc_rows.extend(_read_jsonl(output / "books" / book_id / "arc-map.jsonl"))
        payoff_rows.extend(_read_jsonl(output / "books" / book_id / "payoff-map.jsonl"))
        dna_path = output / "books" / book_id / "book-program-dna.yaml"
        if dna_path.is_file():
            dna = _read_yaml(dna_path)
            dna.setdefault("schema_version", DNA_SCHEMA)
            dna_rows.append(dna)
    _write_jsonl(machine / "arcs.jsonl", arc_rows)
    _write_jsonl(machine / "payoff-map.jsonl", payoff_rows)
    _write_jsonl(machine / "book-program-dna.jsonl", dna_rows)
    evidence_rows = [
        {
            "evidence_id": f"{row['source_book_id']}--{row['source_chapter_id']}",
            "source_book_id": row["source_book_id"],
            "source_locator": row["source_locator"],
            "status": "SEMANTIC_COMPLETE" if _semantic_row(row) else "PENDING_SEMANTIC",
        }
        for row in ledger_rows
    ]
    _write_jsonl(machine / "evidence.jsonl", evidence_rows)
    dependencies = [
        {
            "upstream": f"books/{book_id}/chapter-ledger.jsonl",
            "downstream": f"books/{book_id}/book-program-dna.yaml",
            "status": "ACTIVE" if item["book_program_dna"] else "PENDING",
        }
        for book_id, item in ((item["source_book_id"], item) for item in validation["books"])
    ]
    _write_jsonl(machine / "dependencies.jsonl", dependencies)
    cross_book_names = (
        "sequence-patterns",
        "arc-grammars",
        "payoff-chains",
        "transition-grammars",
        "anti-fatigue-patterns",
        "mechanisms",
        "contrasts",
    )
    for name in cross_book_names:
        path = machine / f"{name}.jsonl"
        if not path.exists():
            _write_jsonl(path, [])
    package = {
        "schema_version": "reference-corpus-program-deep-machine-v1",
        "program_id": "reference-corpus-program-deep-v1",
        "status": (
            "READY_FOR_RETRIEVAL_INTEGRATION" if validation["cross_book_ready"] else "IN_PROGRESS"
        ),
        "knowledge_boundary": "REFERENCE_ONLY",
        "source_count": validation["source_count"],
        "canonical_unit_count": validation["canonical_unit_count"],
        "ledger_rows": validation["ledger_rows"],
        "semantic_complete_rows": validation["semantic_complete_rows"],
        "raw_text_included": False,
        "canon_committed": False,
        "edition_activated": False,
        "paths": {
            "chapter_ledger": "machine/chapter-ledger.jsonl",
            "arcs": "machine/arcs.jsonl",
            "payoffs": "machine/payoff-map.jsonl",
            "book_program_dna": "machine/book-program-dna.jsonl",
            "evidence": "machine/evidence.jsonl",
            "dependencies": "machine/dependencies.jsonl",
        },
        "knowledge_gaps": ["跨书综合仅在 26 本 Book Program DNA 和全章语义覆盖完成后生成。"]
        if not validation["cross_book_ready"]
        else [],
    }
    _write_json(machine / "corpus-package.json", package)
    return package


def audit_program_deep(
    corpus_root: Path | str,
    operations_root: Path | str,
    output_root: Path | str,
) -> dict[str, Any]:
    validation = validate_program_deep(corpus_root, operations_root, output_root)
    output = Path(output_root).expanduser().resolve()
    lines = [
        "# Reference Corpus Program-Deep V1 Audit",
        "",
        f"- 审计时间：{_now()}",
        "- 边界：`REFERENCE_ONLY`；不修改旧 Corpus、原文、Canon 或当前逐章系统。",
        f"- 来源数：{validation['source_count']}",
        f"- canonical unit 数：{validation['canonical_unit_count']}",
        f"- Ledger 行数：{validation['ledger_rows']}",
        f"- 已完成语义行：{validation['semantic_complete_rows']}",
        f"- 待完成语义行：{validation['pending_semantic_rows']}",
        f"- 结构校验：{'PASS' if validation['valid'] else 'FAIL'}",
        f"- Cross-book readiness：{'READY' if validation['cross_book_ready'] else 'KNOWLEDGE_GAP'}",
        "",
        "## 26 本覆盖",
        "",
        "| source_book_id | canonical units | ledger | semantic complete | "
        "pending | arcs | payoffs | DNA |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in validation["books"]:
        lines.append(
            f"| {item['source_book_id']} | {item['canonical_units']} | {item['ledger_rows']} | "
            f"{item['semantic_complete_rows']} | {item['pending_rows']} | {item['arc_rows']} | "
            f"{item['payoff_rows']} | {'YES' if item['book_program_dna'] else 'NO'} |"
        )
    lines.extend(
        [
            "",
            "## 反偏置结果",
            "",
            "- cost/responsibility/governance 未作为 Ledger required 字段。",
            "- immediate upside 与 delayed pressure 分开；证据不足保留 `UNKNOWN`/`Knowledge Gap`。",
            "- 可选压力字段实际出现：`"
            f"{json.dumps(validation['optional_pressure_mentions'], ensure_ascii=False)}`",
            "",
            "## 未完成项",
            "",
        ]
    )
    if validation["pending_semantic_rows"]:
        lines.append(
            f"- 仍有 {validation['pending_semantic_rows']} 个 canonical unit 尚未完成 "
            "semantic worker overlay。"
        )
    if not validation["all_book_program_dna"]:
        lines.append(
            "- 26 本 Book Program DNA 尚未全部出现；跨书 Sequence/Grammar/Mechanism/Contrast "
            "暂不生成。"
        )
    if not validation["errors"] and not validation["pending_semantic_rows"]:
        lines.append("- 无结构性未完成项。")
    if validation["errors"]:
        lines.extend(["", "## Errors", "", *[f"- {error}" for error in validation["errors"]]])
    if validation["warnings"]:
        lines.extend(
            ["", "## 输入警告", "", *[f"- {warning}" for warning in validation["warnings"]]]
        )
    report = output / "operations" / "PROGRAM_DEEP_AUDIT.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return {"report": str(report), **validation}


def stats_program_deep(output_root: Path | str) -> dict[str, Any]:
    output = Path(output_root).expanduser().resolve()
    validation_path = output / "operations" / "validation.json"
    if not validation_path.is_file():
        raise ProgramDeepError("请先运行 validate")
    validation = _read_json(validation_path)
    return {
        "source_count": validation.get("source_count", 0),
        "canonical_unit_count": validation.get("canonical_unit_count", 0),
        "ledger_rows": validation.get("ledger_rows", 0),
        "semantic_complete_rows": validation.get("semantic_complete_rows", 0),
        "pending_semantic_rows": validation.get("pending_semantic_rows", 0),
        "all_book_program_dna": validation.get("all_book_program_dna", False),
        "cross_book_ready": validation.get("cross_book_ready", False),
        "valid": validation.get("valid", False),
    }


__all__ = [
    "ProgramDeepError",
    "audit_program_deep",
    "compile_machine_package",
    "initialize_program_deep",
    "load_source_records",
    "merge_worker_artifacts",
    "reset_book_to_skeleton",
    "stats_program_deep",
    "validate_program_deep",
]
