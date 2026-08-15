"""Deterministic Semantic Distillation V1 operations.

This module owns only the mechanical boundary around the Reference Corpus:
frontmatter parsing, strict validation, evidence resolution, machine-package
compilation, diagnostics, and metadata-only retrieval.  It never reads an
LLM key, creates embeddings, writes a database, or promotes reference material
to Canon.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter, ValidationError

from novel_authoring.reference_corpus.models import CardKnowledgeLevel
from novel_authoring.reference_corpus.semantic_models import (
    ArcObservationCard,
    AtomicObservationCard,
    BookDnaCard,
    ContrastCard,
    CorpusSynthesisCard,
    EvidenceRef,
    MechanismCard,
    ReferenceBookCard,
    SemanticCard,
    SemanticMaturity,
    SemanticStatus,
    SpanKind,
)
from novel_authoring.reference_corpus.service import normalize_title
from novel_authoring.utils import json_dumps

SEMANTIC_CARD_DIRS = (
    "books",
    "book-dna",
    "arcs",
    "observations",
    "mechanisms",
    "contrasts",
    "syntheses/categories",
    "syntheses/cross-category",
)
MACHINE_PACKAGE_VERSION = "reference-corpus-machine-package-v1"
SOURCE_FREEZE_VERSION = "reference-corpus-source-freeze-v1"
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
_SEGMENT_RE = re.compile(r"^segment-(\d+)$")
_CHINESE_RE = re.compile(r"[\u3400-\u9fff]")
_RAW_SUFFIXES = {".txt", ".epub", ".docx", ".rtf", ".html", ".htm"}
_RAW_DIR_NAMES = {"raw", "normalized", "normalized-full-text", "full-text"}
_LENS_TERMS = {
    "governance": ("治理", "行政", "公共秩序", "制度化"),
    "responsibility": ("责任", "公共职责", "承担"),
    "constraint": ("约束", "边界", "限制"),
    "cost": ("成本", "代价", "损耗", "债务"),
    "scarcity": ("稀缺", "资源压力", "匮乏"),
}
_EXPECTED_CREATIVE_PROBLEMS = (
    "opening",
    "first-payoff",
    "breakthrough",
    "power-verification",
    "resource-release",
    "pure-upside",
    "post-payoff-anticipation",
    "world-expansion",
    "map-transition",
    "exploration",
    "mystery-reveal",
    "status-rise",
    "ability-rule",
    "artifact-ability",
    "relationship",
    "long-form",
    "fatigue",
    "ending-settlement",
)

SEMANTIC_CARD_ADAPTER: TypeAdapter[SemanticCard] = TypeAdapter(SemanticCard)


class SemanticCorpusError(ValueError):
    """Raised when the V1 semantic boundary cannot be safely consumed."""


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def _parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise SemanticCorpusError(f"无法读取卡片：{path}") from exc
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        raise SemanticCorpusError(f"卡片缺少 YAML frontmatter：{path}")
    try:
        value = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise SemanticCorpusError(f"卡片 frontmatter 无法解析：{path}") from exc
    if not isinstance(value, dict):
        raise SemanticCorpusError(f"卡片 frontmatter 必须是 object：{path}")
    return value, text[match.end() :]


def _card_paths(corpus_root: Path) -> list[Path]:
    paths: list[Path] = []
    for relative_dir in SEMANTIC_CARD_DIRS:
        directory = corpus_root / relative_dir
        if directory.is_dir():
            paths.extend(sorted(directory.rglob("*.md"), key=lambda item: item.as_posix()))
    return paths


def _load_cards(corpus_root: Path) -> tuple[list[tuple[SemanticCard, Path, str]], list[str]]:
    cards: list[tuple[SemanticCard, Path, str]] = []
    errors: list[str] = []
    for path in _card_paths(corpus_root):
        try:
            payload, body = _parse_frontmatter(path)
            card = SEMANTIC_CARD_ADAPTER.validate_python(payload)
            cards.append((card, path, body))
        except (SemanticCorpusError, ValidationError, TypeError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
    return cards, errors


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise SemanticCorpusError(f"YAML 无法读取：{path}") from exc
    if not isinstance(value, dict):
        raise SemanticCorpusError(f"YAML 根节点必须是 object：{path}")
    return value


def _source_freeze_path(corpus_root: Path) -> Path:
    return corpus_root / "selection" / "corpus-sources-v0.confirmed.yaml"


def _load_source_freeze(corpus_root: Path) -> dict[str, dict[str, Any]]:
    path = _source_freeze_path(corpus_root)
    if not path.is_file():
        return {}
    payload = _load_yaml(path)
    sources = payload.get("sources")
    if not isinstance(sources, list):
        raise SemanticCorpusError(f"来源冻结文件缺少 sources：{path}")
    result: dict[str, dict[str, Any]] = {}
    for item in sources:
        if isinstance(item, dict) and isinstance(item.get("source_book_id"), str):
            result[item["source_book_id"]] = item
    return result


def _load_preparation_metadata(corpus_root: Path, source_book_id: str) -> dict[str, Any]:
    operations_root = corpus_root.parent / "reference-corpus-operations"
    path = operations_root / "preparations" / source_book_id / "manifest.json"
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    sources = payload.get("sources")
    if isinstance(sources, list) and sources and isinstance(sources[0], dict):
        return sources[0]
    return {}


def _read_legacy_book_metadata(corpus_root: Path) -> list[dict[str, Any]]:
    inventory_path = corpus_root / "selection" / "inventory.json"
    inventory: list[dict[str, Any]] = []
    if inventory_path.is_file():
        payload = json.loads(inventory_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("files"), list):
            inventory = [item for item in payload["files"] if isinstance(item, dict)]
    by_title = {
        normalize_title(str(item.get("title", ""))): item
        for item in inventory
        if item.get("title")
    }

    def inventory_for_title(title: str) -> dict[str, Any]:
        candidates = (
            title,
            re.sub(r"[（(]参考语料库\s*V0[）)]", "", title),
            title.replace("（参考语料库 V0）", "").replace("(参考语料库 V0)", ""),
        )
        for candidate in candidates:
            item = by_title.get(normalize_title(candidate))
            if item is not None:
                return item
        return {}
    records: list[dict[str, Any]] = []
    for path in sorted((corpus_root / "books").glob("*.md")):
        try:
            payload, _body = _parse_frontmatter(path)
        except SemanticCorpusError:
            continue
        source_book_id = payload.get("source_book_id")
        if not isinstance(source_book_id, str):
            continue
        title = str(payload.get("title") or path.stem)
        display_title = re.sub(r"[（(]参考语料库\s*V0[）)]", "", title).strip()
        inventory_item = inventory_for_title(title)
        prepared = _load_preparation_metadata(corpus_root, source_book_id)
        records.append(
            {
                "source_book_id": source_book_id,
                "source_path": inventory_item.get("relative_path", "UNKNOWN"),
                "title": display_title or title,
                "category": inventory_item.get("category_name", "UNKNOWN"),
                "distill_id": payload.get("distill_id", "UNKNOWN"),
                "parse_warning": "；".join(inventory_item.get("warnings", [])),
                "coverage_status": "V0_CONFIRMED_EXISTING_DISTILL",
                "source_id": prepared.get("source_id", "UNKNOWN"),
                "line_count": int(prepared.get("lines", 0) or 0),
                "segment_count": int(prepared.get("segment_count", 0) or 0),
                "chapter_detection_confidence": prepared.get(
                    "chapter_detection_confidence", "UNKNOWN"
                ),
            }
        )
    return records


def confirm_v0_sources(corpus_root: Path) -> dict[str, Any]:
    """Freeze the already-produced 26-book set without re-running selection."""

    root = _resolved(corpus_root)
    records = _read_legacy_book_metadata(root)
    if len(records) != 26:
        raise SemanticCorpusError(
            "当前 books/ 未形成 26 本 V0 基线："
            f"发现 {len(records)} 本；不重新运行 selection algorithm"
        )
    records.sort(key=lambda item: str(item["source_book_id"]))
    payload = {
        "schema_version": SOURCE_FREEZE_VERSION,
        "status": "CONFIRMED",
        "confirmed_by": "CURRENT_CORPUS_BASELINE",
        "created_at": _now(),
        "source_count": len(records),
        "selection_note": "冻结已经实际产生 V0 Corpus 的来源集，不表示作者喜欢每本书的全部机制。",
        "selection_parser_issue": {
            "status": "RECORDED",
            "description": (
                "旧 inventory 的 chapter-title parser 对部分格式不可靠，"
                "可能把完整长篇估为 5 或 7 章。"
            ),
            "handling": (
                "本 V1 使用实际 distill segment/line coverage；"
                "不再用 chapter_count distance 推导 literary contrast。"
            ),
        },
        "sources": records,
    }
    path = _source_freeze_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "path": str(path),
        "source_count": len(records),
        "confirmed_by": payload["confirmed_by"],
    }


def _source_manifests(
    corpus_root: Path, cards: Iterable[SemanticCard]
) -> dict[str, dict[str, Any]]:
    freeze = _load_source_freeze(corpus_root)
    result: dict[str, dict[str, Any]] = {}
    for source_book_id in sorted({item for card in cards for item in card.source_book_ids}):
        item = dict(freeze.get(source_book_id, {}))
        evidence = [
            ref
            for card in cards
            for ref in _all_evidence_refs(card)
            if ref.source_book_id == source_book_id
        ]
        max_line = max((ref.line_end for ref in evidence), default=0)
        max_segment = max(
            (int(ref.segment_id.removeprefix("segment-")) for ref in evidence), default=0
        )
        result[source_book_id] = {
            "schema_version": "reference-corpus-source-manifest-v1",
            "source_book_id": source_book_id,
            "source_id": item.get("source_id", evidence[0].source_id if evidence else "UNKNOWN"),
            "distill_id": item.get(
                "distill_id", evidence[0].distill_id if evidence else "UNKNOWN"
            ),
            "title": item.get("title", source_book_id),
            "category": item.get("category", "UNKNOWN"),
            "source_path": item.get("source_path", "UNKNOWN"),
            "line_count": max(int(item.get("line_count", 0) or 0), max_line),
            "segment_count": max(int(item.get("segment_count", 0) or 0), max_segment),
            "coverage_status": item.get("coverage_status", "UNKNOWN"),
            "raw_text_included": False,
        }
    return result


def _all_evidence_refs(card: SemanticCard) -> list[EvidenceRef]:
    refs = list(card.evidence_refs)
    if isinstance(card, ContrastCard):
        for solution in card.solutions:
            refs.extend(solution.evidence_refs)
    return refs


def _validate_evidence(
    card: SemanticCard, manifests: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    for ref in _all_evidence_refs(card):
        manifest = manifests.get(ref.source_book_id)
        if manifest is None:
            errors.append(f"{card.card_id}: evidence 来源不在 source freeze：{ref.source_book_id}")
            continue
        if manifest.get("source_id") not in {"UNKNOWN", ref.source_id}:
            errors.append(
                f"{card.card_id}: source_id 不匹配 {ref.source_id} != {manifest.get('source_id')}"
            )
        segment_number = int(ref.segment_id.removeprefix("segment-"))
        segment_count = int(manifest.get("segment_count", 0) or 0)
        line_count = int(manifest.get("line_count", 0) or 0)
        if segment_count and segment_number > segment_count:
            errors.append(f"{card.card_id}: segment 超出冻结来源范围 {ref.segment_id}")
        if line_count and ref.line_end > line_count:
            errors.append(
                f"{card.card_id}: line_end 超出冻结来源范围 {ref.line_end}>{line_count}"
            )


def _validate_card_specific(card: SemanticCard, errors: list[str]) -> None:
    declared = set(card.source_book_ids)
    if isinstance(card, (BookDnaCard, ArcObservationCard, AtomicObservationCard)):
        if len(declared) != 1:
            errors.append(f"{card.card_id}: 单书卡必须只有一个 source_book_id")
        if card.knowledge_level is not CardKnowledgeLevel.BOOK_OBSERVATION:
            errors.append(f"{card.card_id}: 单书卡 knowledge_level 错误")
    if isinstance(card, (MechanismCard,)):
        if card.knowledge_level is not CardKnowledgeLevel.CROSS_BOOK_CONTRAST:
            errors.append(f"{card.card_id}: Mechanism knowledge_level 错误")
        if card.source_count != len(declared):
            errors.append(f"{card.card_id}: source_count 与来源集合不一致")
        if card.source_count < 4:
            errors.append(f"{card.card_id}: Mechanism 至少需要 4 本 distinct books")
        if card.category_count != len(set(card.category_ids)):
            errors.append(f"{card.card_id}: category_count 与 category_ids 不一致")
    if (
        isinstance(card, ReferenceBookCard)
        and card.knowledge_level is not CardKnowledgeLevel.BOOK_OBSERVATION
    ):
        errors.append(f"{card.card_id}: Reference Book knowledge_level 错误")
    if isinstance(card, ArcObservationCard) and not card.span_kind:
        errors.append(f"{card.card_id}: Arc 缺少 span_kind")
    if isinstance(card, AtomicObservationCard) and not card.observation_summary:
        errors.append(f"{card.card_id}: Observation 缺少 observation_summary")
    if isinstance(card, CorpusSynthesisCard):
        if card.knowledge_level is not CardKnowledgeLevel.CORPUS_SYNTHESIS:
            errors.append(f"{card.card_id}: Synthesis knowledge_level 错误")
        if card.synthesis_kind == "CATEGORY" and len(declared) < 2:
            errors.append(f"{card.card_id}: Category Synthesis 至少需要 2 本书")
        if card.synthesis_kind == "CROSS_CATEGORY":
            if len(declared) < 4 and card.maturity is not SemanticMaturity.PILOT:
                errors.append(
                    f"{card.card_id}: Cross-category synthesis 至少需要 4 本书或标记 PILOT"
                )
            if len(set(card.category_ids)) < 3 and card.maturity is not SemanticMaturity.PILOT:
                errors.append(
                    f"{card.card_id}: Cross-category synthesis 至少需要 3 个类别或标记 PILOT"
                )


def _body_leakage(path: Path, body: str, errors: list[str]) -> None:
    for line_number, line in enumerate(body.splitlines(), start=1):
        stripped = line.strip()
        if len(stripped) > 360:
            errors.append(f"{path}:{line_number}: Markdown 存在疑似长段来源正文泄漏")
        if stripped.startswith(("```", "http://", "https://")):
            continue


def _raw_leakage(corpus_root: Path, errors: list[str]) -> None:
    for path in corpus_root.rglob("*"):
        if path.is_dir() and path.name in _RAW_DIR_NAMES:
            errors.append(f"存在完整正文目录：{path}")
        elif path.is_file() and path.suffix.casefold() in _RAW_SUFFIXES:
            errors.append(f"存在来源正文文件：{path}")


def validate_semantic_corpus(corpus_root: Path) -> dict[str, Any]:
    """Validate V1 Markdown contracts and evidence without touching GBrain."""

    root = _resolved(corpus_root)
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        raise SemanticCorpusError(f"corpus-root 不是目录：{root}")
    cards, load_errors = _load_cards(root)
    errors.extend(load_errors)
    card_values = [item[0] for item in cards]
    ids = [card.card_id for card in card_values]
    for card_id, count in Counter(ids).items():
        if count > 1:
            errors.append(f"card_id 重复：{card_id}")
    manifests = _source_manifests(root, card_values)
    freeze = _load_source_freeze(root)
    if not freeze:
        warnings.append("尚未生成 selection/corpus-sources-v0.confirmed.yaml")
    elif len(freeze) != 26:
        errors.append(f"来源冻结基线必须为 26 本，当前 {len(freeze)} 本")
    for card, path, body in cards:
        _validate_evidence(card, manifests, errors)
        _validate_card_specific(card, errors)
        _body_leakage(path, body, errors)
        if not _CHINESE_RE.search(body):
            warnings.append(f"卡片缺少中文可读内容：{path}")
        if card.status not in {SemanticStatus.REFERENCE_ONLY, SemanticStatus.STALE}:
            errors.append(f"{card.card_id}: status 不是 reference-only 边界")
    _raw_leakage(root, errors)
    machine_path = root / "machine" / "cards.jsonl"
    if machine_path.is_file():
        try:
            machine_lines = [
                line
                for line in machine_path.read_text(encoding="utf-8").splitlines()
                if line
            ]
            for line in machine_lines:
                SEMANTIC_CARD_ADAPTER.validate_python(json.loads(line))
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            ValidationError,
            TypeError,
            ValueError,
        ) as exc:
            errors.append(f"machine/cards.jsonl 无法按统一 contract 解析：{exc}")
    stats = semantic_stats(card_values, manifests)
    return {
        "valid": not errors,
        "corpus_root": str(root),
        "card_count": len(card_values),
        "errors": errors,
        "warnings": warnings,
        "stats": stats,
    }


def _jsonl_write(path: Path, values: Iterable[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values),
        encoding="utf-8",
        newline="\n",
    )


def compile_semantic_corpus(corpus_root: Path) -> dict[str, Any]:
    """Compile validated Markdown projections into the machine package."""

    root = _resolved(corpus_root)
    freeze_result = confirm_v0_sources(root)
    cards, errors = _load_cards(root)
    if errors:
        raise SemanticCorpusError(
            "无法 compile 未通过 Markdown contract 的 Corpus：\n" + "\n".join(errors)
        )
    card_values = [item[0] for item in cards]
    manifests = _source_manifests(root, card_values)
    validation = validate_semantic_corpus(root)
    if not validation["valid"]:
        raise SemanticCorpusError(
            "无法 compile 未通过 evidence/schema validation 的 Corpus：\n"
            + "\n".join(validation["errors"])
        )
    machine_root = root / "machine"
    manifest_root = machine_root / "manifests"
    manifest_root.mkdir(parents=True, exist_ok=True)
    for source_book_id, manifest in manifests.items():
        (manifest_root / f"{source_book_id}.json").write_text(
            json_dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    cards_path = machine_root / "cards.jsonl"
    evidence_path = machine_root / "evidence.jsonl"
    dependencies_path = machine_root / "dependencies.jsonl"
    machine_root.mkdir(parents=True, exist_ok=True)
    _jsonl_write(cards_path, (card.model_dump(mode="json") for card in card_values))
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for card in card_values:
        for ref in _all_evidence_refs(card):
            evidence_by_id[ref.evidence_id] = {
                "evidence_id": ref.evidence_id,
                "source_book_id": ref.source_book_id,
                "distill_id": ref.distill_id,
                "source_id": ref.source_id,
                "segment_id": ref.segment_id,
                "line_start": ref.line_start,
                "line_end": ref.line_end,
                "observation_summary": ref.observation_summary,
            }
    _jsonl_write(evidence_path, (evidence_by_id[key] for key in sorted(evidence_by_id)))
    known_ids = {card.card_id for card in card_values}
    dependency_rows: list[dict[str, Any]] = []
    for card in card_values:
        for upstream in card.depends_on:
            if upstream not in known_ids:
                raise SemanticCorpusError(f"{card.card_id}: depends_on 不存在：{upstream}")
            dependency_rows.append(
                {
                    "upstream_card_id": upstream,
                    "downstream_card_id": card.card_id,
                    "relation": "supports",
                    "status": "STALE" if _is_stale(upstream, card_values) else "ACTIVE",
                }
            )
    _jsonl_write(
        dependencies_path,
        sorted(
            dependency_rows,
            key=lambda item: (item["upstream_card_id"], item["downstream_card_id"]),
        ),
    )
    stats = semantic_stats(card_values, manifests)
    package = {
        "schema_version": MACHINE_PACKAGE_VERSION,
        "status": "REFERENCE_ONLY",
        "generated_at": _now(),
        "raw_text_included": False,
        "canon_committed": False,
        "edition_activated": False,
        "source_freeze": freeze_result,
        "paths": {
            "cards": "machine/cards.jsonl",
            "evidence": "machine/evidence.jsonl",
            "dependencies": "machine/dependencies.jsonl",
            "manifests": "machine/manifests",
        },
        "counts": {
            "cards": len(card_values),
            "evidence": len(evidence_by_id),
            "dependencies": len(dependency_rows),
        },
        "stats": stats,
    }
    package_path = machine_root / "corpus-package.json"
    package_path.write_text(json_dumps(package, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {
        "valid": True,
        "corpus_root": str(root),
        "package_path": str(package_path),
        "card_count": len(card_values),
        "evidence_count": len(evidence_by_id),
        "dependency_count": len(dependency_rows),
        "paths": package["paths"],
    }


def _is_stale(card_id: str, cards: Sequence[SemanticCard]) -> bool:
    return any(card.card_id == card_id and card.status is SemanticStatus.STALE for card in cards)


def semantic_stats(
    cards: Sequence[SemanticCard], manifests: dict[str, dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Return diagnostic coverage facts, never a literary score."""

    type_counts = Counter(card.card_type for card in cards)
    knowledge_counts = Counter(card.knowledge_level.value for card in cards)
    span_counts = Counter(
        card.span_kind.value for card in cards if isinstance(card, ArcObservationCard)
    )
    source_ids = sorted({source for card in cards for source in card.source_book_ids})
    category_ids = sorted({category for card in cards for category in card.category_ids})
    experience_counts = Counter(
        experience.value for card in cards for experience in card.reader_experiences
    )
    payoff_counts = Counter(channel.value for card in cards for channel in card.payoff_channels)
    source_concentration = Counter(source for card in cards for source in card.source_book_ids)
    return {
        "reference_books": type_counts.get("reference-book", 0),
        "book_dna": type_counts.get("book-dna", 0),
        "arcs": type_counts.get("arc-observation", 0),
        "contiguous_arcs": span_counts.get(SpanKind.CONTIGUOUS_ARC.value, 0),
        "longitudinal_trajectories": span_counts.get(SpanKind.LONGITUDINAL_TRAJECTORY.value, 0),
        "observations": type_counts.get("observation", 0),
        "mechanisms": type_counts.get("mechanism-card", 0),
        "contrasts": type_counts.get("contrast-card", 0),
        "category_syntheses": sum(
            1
            for card in cards
            if isinstance(card, CorpusSynthesisCard) and card.synthesis_kind == "CATEGORY"
        ),
        "cross_category_syntheses": sum(
            1
            for card in cards
            if isinstance(card, CorpusSynthesisCard) and card.synthesis_kind == "CROSS_CATEGORY"
        ),
        "machine_cards": len(cards),
        "source_book_count": len(source_ids),
        "category_count": len(category_ids),
        "knowledge_level_coverage": dict(sorted(knowledge_counts.items())),
        "source_ids": source_ids,
        "category_ids": category_ids,
        "reader_experience_coverage": dict(sorted(experience_counts.items())),
        "payoff_channel_coverage": dict(sorted(payoff_counts.items())),
        "source_concentration": dict(source_concentration.most_common()),
        "evidence_count": sum(len(_all_evidence_refs(card)) for card in cards),
        "dependency_count": sum(len(card.depends_on) for card in cards),
        "manifest_count": len(manifests or {}),
    }


def _card_text(card: SemanticCard) -> str:
    return json.dumps(card.model_dump(mode="json"), ensure_ascii=False)


def _lens_counts(cards: Sequence[SemanticCard]) -> dict[str, int]:
    dna = [card for card in cards if isinstance(card, BookDnaCard)]
    return {
        lens: sum(
            any(term in _card_text(card) for term in terms)
            for card in dna
        )
        for lens, terms in _LENS_TERMS.items()
    }


def _missing_creative_problems(cards: Sequence[SemanticCard]) -> list[str]:
    tags = {tag for card in cards for tag in card.creative_problem_tags}
    return [problem for problem in _EXPECTED_CREATIVE_PROBLEMS if problem not in tags]


def _write_audit_reports(root: Path, result: dict[str, Any]) -> dict[str, str]:
    stats = result["stats"]
    lens = _lens_counts([card for card, _path, _body in _load_cards(root)[0]])
    missing = _missing_creative_problems([card for card, _path, _body in _load_cards(root)[0]])
    operations = root / "operations"
    operations.mkdir(parents=True, exist_ok=True)
    audit_lines = [
        "# Reference Corpus Semantic Audit V1",
        "",
        "本报告只记录确定性覆盖、证据与边界诊断，不是文学评分。",
        "",
        "## 资产数量",
        "",
    ]
    labels = (
        ("Reference Books", "reference_books"),
        ("Book DNA", "book_dna"),
        ("Arc Observations", "arcs"),
        ("CONTIGUOUS_ARC", "contiguous_arcs"),
        ("LONGITUDINAL_TRAJECTORY", "longitudinal_trajectories"),
        ("Atomic Observations", "observations"),
        ("Mechanism Cards", "mechanisms"),
        ("Contrast Cards", "contrasts"),
        ("Category Syntheses", "category_syntheses"),
        ("Cross-category Syntheses", "cross_category_syntheses"),
        ("Machine Cards", "machine_cards"),
        ("Evidence rows", "evidence_count"),
        ("Dependency rows", "dependency_count"),
    )
    audit_lines.extend(f"- {label}: {stats[key]}" for label, key in labels)
    audit_lines.extend(
        [
            "",
            "## 覆盖与检索元数据",
            "",
            f"- source books: {stats['source_book_count']}",
            f"- categories: {stats['category_count']}",
            "- ReaderExperience coverage: `"
            + json.dumps(
                stats["reader_experience_coverage"], ensure_ascii=False, sort_keys=True
            )
            + "`",
            "- PayoffChannel coverage: `"
            + json.dumps(stats["payoff_channel_coverage"], ensure_ascii=False, sort_keys=True)
            + "`",
            "- source concentration: `"
            + json.dumps(stats["source_concentration"], ensure_ascii=False, sort_keys=True)
            + "`",
            f"- missing creative problems: {', '.join(missing) if missing else '无'}",
            "",
            "## Lens coverage（诊断，不是总分）",
            "",
        ]
    )
    audit_lines.extend(
        f"- {name}: {count} / {stats['book_dna']} Book DNA" for name, count in lens.items()
    )
    audit_lines.extend(
        [
            "",
            "## 状态",
            "",
            f"- semantic validation: {'PASS' if result['valid'] else 'FAIL'}",
            f"- errors: {len(result['errors'])}",
            f"- warnings: {len(result['warnings'])}",
            "- Reference-only boundary: PASS（未写入 Canon、原文或数据库）",
            "",
            "## Knowledge Gaps",
            "",
            "证据不足的创作问题保留为缺口，不为了数量制造 Mechanism。",
        ]
    )
    audit_lines.extend(f"- {item}" for item in missing)
    audit_path = operations / "CORPUS_SEMANTIC_AUDIT_V1.md"
    audit_path.write_text("\n".join(audit_lines) + "\n", encoding="utf-8", newline="\n")

    rewrites = [
        card
        for card, _path, _body in _load_cards(root)[0]
        if isinstance(card, BookDnaCard) and card.rewrite_required
    ]
    bias_lines = [
        "# Distillation Lens Audit V1",
        "",
        "本审计专门检查治理 / 责任 / 约束 / 成本 / 稀缺是否吞没了正向体验。没有总分。",
        "",
        "## 1–5. 当前镜头分布",
        "",
        f"1. governance-heavy Book DNA: {lens['governance']}",
        f"2. responsibility-heavy Book DNA: {lens['responsibility']}",
        f"3. constraint-heavy Book DNA: {lens['constraint']}",
        f"4. cost-heavy Book DNA: {lens['cost']}",
        f"5. scarcity-heavy Book DNA: {lens['scarcity']}",
        "",
        "## 正向体验覆盖",
        "",
        "- 具体覆盖见 CORPUS_SEMANTIC_AUDIT_V1.md 的 ReaderExperience / PayoffChannel 统计。",
        "- Pure-upside、能力愉悦、力量验证、行动空间、探索和身份/关系收益，"
        "均允许没有 cost、scarcity 或 responsibility。",
        "",
        "## 是否存在默认偏置",
        "",
        "- 成长是否自动总结为责任：由每个 Book DNA 的 anti_bias_checks "
        "与 rewrite_reason 逐项记录。",
        "- 能力是否自动找成本：由 `Cost Necessity Test` 逐项记录；"
        "无选择影响时允许 `NOT_MATERIAL`。",
        "- 奖励是否自动制造新稀缺：由 `Pure Upside Check` 与 payoff_grammar 逐项记录。",
        "",
        "## 需要 rewrite 的 Book DNA",
        "",
    ]
    if rewrites:
        bias_lines.extend(f"- `{card.card_id}`：{card.rewrite_reason}" for card in rewrites)
    else:
        bias_lines.append("- 无；当前候选都通过 targeted semantic audit。")
    bias_lines.extend(
        [
            "",
            "## 现有约束镜头 Mechanism 的重新定位",
            "",
            "它们只能作为 possible variant，必须同时列出 pure-upside、abundance、"
            "探索、身份跃迁等不适用或互补路线。",
            "",
            "## Remaining Knowledge Gaps",
            "",
        ]
    )
    bias_lines.extend(f"- `{item}`：当前跨书证据尚不足，保留为缺口。" for item in missing)
    bias_path = operations / "DISTILLATION_LENS_AUDIT_V1.md"
    bias_path.write_text("\n".join(bias_lines) + "\n", encoding="utf-8", newline="\n")
    return {"audit_report": str(audit_path), "lens_report": str(bias_path)}


def audit_semantic_corpus(corpus_root: Path) -> dict[str, Any]:
    root = _resolved(corpus_root)
    result = validate_semantic_corpus(root)
    paths = _write_audit_reports(root, result)
    return {**result, "report_paths": paths}


def stats_semantic_corpus(corpus_root: Path) -> dict[str, Any]:
    root = _resolved(corpus_root)
    cards, errors = _load_cards(root)
    if errors:
        raise SemanticCorpusError("无法统计未能解析的 V1 cards：\n" + "\n".join(errors))
    manifests = _source_manifests(root, [card for card, _path, _body in cards])
    return {
        "corpus_root": str(root),
        **semantic_stats([card for card, _path, _body in cards], manifests),
    }


def _query_values(value: str | Sequence[str] | None) -> set[str]:
    if value is None:
        return set()
    values = [value] if isinstance(value, str) else list(value)
    return {str(item).strip().casefold() for item in values if str(item).strip()}


def retrieve_metadata_candidates(
    corpus_root: Path,
    *,
    creative_problem: str | Sequence[str] | None = None,
    reader_experiences: Sequence[str] | None = None,
    narrative_drives: Sequence[str] | None = None,
    payoff_channels: Sequence[str] | None = None,
    max_cards: int = 6,
) -> list[dict[str, Any]]:
    """Return metadata-prefiltered candidates without embedding or literary scoring."""

    if not 3 <= max_cards <= 8:
        raise ValueError("max_cards 必须位于 3..8")
    path = _resolved(corpus_root) / "machine" / "cards.jsonl"
    if not path.is_file():
        raise SemanticCorpusError("machine package 不存在，请先运行 novel corpus compile")
    problems = _query_values(creative_problem)
    experiences = _query_values(reader_experiences)
    drives = _query_values(narrative_drives)
    payoffs = _query_values(payoff_channels)
    records: list[tuple[int, dict[str, Any]]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        try:
            record = SEMANTIC_CARD_ADAPTER.validate_python(json.loads(line)).model_dump(
                mode="json"
            )
        except (json.JSONDecodeError, TypeError, ValidationError, ValueError) as exc:
            raise SemanticCorpusError("machine package 存在无法解析的 card") from exc
        fields = {
            "creative_problem_tags": {
                str(item).casefold() for item in record.get("creative_problem_tags", [])
            },
            "reader_experiences": {
                str(item).casefold() for item in record.get("reader_experiences", [])
            },
            "narrative_drives": {
                str(item).casefold() for item in record.get("narrative_drives", [])
            },
            "payoff_channels": {
                str(item).casefold() for item in record.get("payoff_channels", [])
            },
        }
        matches = sum(
            bool(query & fields[name])
            for query, name in (
                (problems, "creative_problem_tags"),
                (experiences, "reader_experiences"),
                (drives, "narrative_drives"),
                (payoffs, "payoff_channels"),
            )
        )
        if any((problems, experiences, drives, payoffs)) and matches == 0:
            continue
        record["metadata_match_fields"] = [
            name
            for query, name in (
                (problems, "creative_problem_tags"),
                (experiences, "reader_experiences"),
                (drives, "narrative_drives"),
                (payoffs, "payoff_channels"),
            )
            if query & fields[name]
        ]
        records.append((matches, record))
    records.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("card_type")),
            str(item[1].get("card_id")),
        )
    )
    result: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    for _matches, record in records:
        sources = [str(item) for item in record.get("source_book_ids", [])]
        primary = sources[0] if sources else "UNKNOWN"
        if source_counts[primary] >= 2:
            continue
        source_counts[primary] += 1
        result.append(record)
        if len(result) >= max_cards:
            break
    return result


def source_diversity_guard(records: Sequence[dict[str, Any]], max_per_source: int = 2) -> bool:
    counts: Counter[str] = Counter(
        str(source)
        for record in records
        for source in record.get("source_book_ids", [])[:1]
    )
    return all(count <= max_per_source for count in counts.values())


__all__ = [
    "SemanticCorpusError",
    "audit_semantic_corpus",
    "compile_semantic_corpus",
    "confirm_v0_sources",
    "retrieve_metadata_candidates",
    "semantic_stats",
    "source_diversity_guard",
    "stats_semantic_corpus",
    "validate_semantic_corpus",
]
