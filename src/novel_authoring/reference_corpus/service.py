"""Filesystem-only Reference Corpus V0 operations.

The raw novel directory is an immutable input.  This module only reads it for
bounded metadata (stat, decoding, and chapter-heading counts) and writes
derived JSON/YAML/Markdown outside that directory.  It deliberately has no
database, vector, or LLM dependency.
"""

# Markdown templates intentionally keep their prose in one artifact string.
# ruff: noqa: E501

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from novel_authoring.distill.preparation import (
    SUPPORTED_EXTENSIONS,
    extract_source,
)
from novel_authoring.reference_corpus.models import (
    CategoryDefinition,
    CorpusCardFrontmatter,
    InventoryCategory,
    InventoryFile,
    InventoryManifest,
    InventoryParseStatus,
    PilotSelectionProposal,
    SelectionAlternative,
    SelectionCategory,
    SelectionRecommendation,
)
from novel_authoring.utils import json_dumps, utc_now

EXPECTED_CATEGORIES = (
    CategoryDefinition(category_id="01_玄幻", category_name="玄幻"),
    CategoryDefinition(category_id="02_仙侠", category_name="仙侠"),
    CategoryDefinition(category_id="03_都市", category_name="都市"),
    CategoryDefinition(category_id="04_科幻", category_name="科幻"),
    CategoryDefinition(category_id="05_奇幻", category_name="奇幻"),
    CategoryDefinition(category_id="06_历史", category_name="历史"),
    CategoryDefinition(category_id="07_武侠", category_name="武侠"),
    CategoryDefinition(category_id="08_游戏", category_name="游戏"),
    CategoryDefinition(category_id="09_高武", category_name="高武"),
    CategoryDefinition(category_id="10_灵异", category_name="灵异"),
    CategoryDefinition(category_id="11_体育竞技", category_name="体育竞技"),
    CategoryDefinition(category_id="12_军事谍战", category_name="军事谍战"),
    CategoryDefinition(category_id="13_其他", category_name="其他"),
)
PILOT_TARGET_BOOK_COUNT = 26

SCAFFOLD_DIRS = (
    "docs",
    "schema-pack",
    "schema-pack/novel-reference-corpus-v1",
    "selection",
    "books",
    "book-dna",
    "prose-dna",
    "arcs",
    "observations",
    "mechanisms",
    "contrasts",
    "syntheses",
    "syntheses/categories",
    "syntheses/cross-category",
    "taste",
    "maps",
    "machine",
    "machine/manifests",
    "machine/evidence",
    "machine/dependencies",
    "machine/packages",
    "operations",
    "skills",
)

REQUIRED_FILES = (
    "RESOLVER.md",
    "schema.md",
    "corpus.yaml",
    "schema-pack/novel-reference-corpus-v1/pack.yaml",
)

FORBIDDEN_DIR_NAMES = {"raw", "normalized", "normalized-full-text", "full-text"}
RAW_EXTENSIONS = {
    ".txt",
    ".epub",
    ".docx",
    ".rtf",
    ".html",
    ".htm",
    ".rst",
    ".adoc",
}
CARD_DIRS = {
    "books",
    "book-dna",
    "prose-dna",
    "arcs",
    "observations",
    "mechanisms",
    "contrasts",
    "syntheses",
    "taste",
}
SCHEMA_PACK_PRIMITIVES = {"entity", "media", "temporal", "annotation", "concept"}
SCHEMA_PACK_PAGE_TYPES = {
    "reference-book",
    "book-dna",
    "prose-dna",
    "arc-observation",
    "observation",
    "mechanism-card",
    "contrast-card",
    "corpus-synthesis",
    "taste-note",
}
SCHEMA_PACK_LINK_TYPES = {
    "distilled-from",
    "evidenced-by",
    "appears-in",
    "synthesized-from",
    "contrasts-with",
    "variant-of",
    "taste-rates",
}

CHAPTER_LINE_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:chapter\s+(?:\d+|[ivxlcdm]+)|"
    r"第[零〇一二三四五六七八九十百千万两\d]+[章节回卷部篇]|序章|楔子|尾声|终章)"
    r"(?:\b|\s*)[^\n]*$",
    re.IGNORECASE,
)


class ReferenceCorpusError(ValueError):
    """Raised for invalid corpus paths or derived contracts."""


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def _category_name(category_id: str) -> str:
    return category_id.split("_", 1)[1] if "_" in category_id else category_id


def _title_from_path(path: Path) -> str:
    title = path.stem.strip()
    for suffix in ("_正文全集", "正文全集", "_全本", "全本", "_完本", "完本"):
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip(" _-")
    return title or path.name


def normalize_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).casefold()
    normalized = re.sub(r"正文全集|全集|全本|完本", "", normalized)
    return re.sub(r"[^\w\u3400-\u9fff]+", "", normalized)


def _detect_encoding(path: Path) -> str:
    sample = path.read_bytes()[: 64 * 1024]
    if sample.startswith((b"\xff\xfe", b"\xfe\xff")):
        return "utf-16"
    if sample.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    for encoding in ("utf-8", "gb18030", "big5", "utf-16"):
        try:
            sample.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return "utf-8"


def _scan_lines(lines: Iterable[str]) -> tuple[int, int, bool, bool]:
    line_count = 0
    chapter_count = 0
    replacement = False
    has_content = False
    for line in lines:
        line_count += 1
        if line.strip():
            has_content = True
        if "\ufffd" in line:
            replacement = True
        if CHAPTER_LINE_RE.match(line):
            chapter_count += 1
    return line_count, chapter_count, replacement, has_content


def _scan_file_content(path: Path) -> tuple[str, int, int, list[str]]:
    """Return encoding, line count, chapter estimate, and scan warnings."""

    suffix = path.suffix.casefold()
    warnings: list[str] = []
    if suffix in {".epub", ".docx"}:
        text = extract_source(path)
        line_count, chapter_count, replacement, has_content = _scan_lines(text.splitlines())
        encoding = f"{suffix[1:]}-embedded-text"
    else:
        encoding = _detect_encoding(path)
        with path.open("r", encoding=encoding, errors="replace", newline=None) as handle:
            line_count, chapter_count, replacement, has_content = _scan_lines(handle)
    if not has_content:
        warnings.append("文件为空或没有可见文本")
    if encoding not in {"utf-8", "utf-8-sig"}:
        warnings.append(f"使用非 UTF-8 编码：{encoding}")
    if replacement:
        warnings.append("解码出现替换字符，正文解析需要人工复核")
    if chapter_count == 0 and has_content:
        warnings.append("未识别到章节标题")
    elif chapter_count < 3:
        warnings.append("可识别章节少于三个，章节级证据较弱")
    return encoding, line_count, chapter_count, warnings


def _scan_inventory_file(raw_root: Path, category: Path, path: Path) -> InventoryFile:
    relative_path = path.relative_to(raw_root).as_posix()
    suffix = path.suffix.casefold() or "<none>"
    title = _title_from_path(path)
    warnings: list[str] = []
    try:
        stat = path.stat()
        modified_at = datetime.fromtimestamp(stat.st_mtime, UTC).isoformat()
        size_bytes = int(stat.st_size)
    except OSError as exc:
        return InventoryFile(
            category_id=category.name,
            category_name=_category_name(category.name),
            relative_path=relative_path,
            file_name=path.name,
            extension=suffix,
            size_bytes=0,
            modified_at="",
            parse_status=InventoryParseStatus.ERROR,
            estimated_chapter_count=0,
            title=title,
            normalized_title=normalize_title(title),
            warnings=[f"无法读取文件元数据：{exc}"],
        )
    if suffix not in SUPPORTED_EXTENSIONS:
        return InventoryFile(
            category_id=category.name,
            category_name=_category_name(category.name),
            relative_path=relative_path,
            file_name=path.name,
            extension=suffix,
            size_bytes=size_bytes,
            modified_at=modified_at,
            parse_status=InventoryParseStatus.UNSUPPORTED,
            detected_encoding=None,
            estimated_chapter_count=0,
            title=title,
            normalized_title=normalize_title(title),
            warnings=[f"不支持的来源格式：{suffix}"],
        )
    try:
        encoding, _, chapter_count, scan_warnings = _scan_file_content(path)
        warnings.extend(scan_warnings)
        parse_status = InventoryParseStatus.WARNING if warnings else InventoryParseStatus.OK
        return InventoryFile(
            category_id=category.name,
            category_name=_category_name(category.name),
            relative_path=relative_path,
            file_name=path.name,
            extension=suffix,
            size_bytes=size_bytes,
            modified_at=modified_at,
            parse_status=parse_status,
            detected_encoding=encoding,
            estimated_chapter_count=chapter_count,
            title=title,
            normalized_title=normalize_title(title),
            warnings=warnings,
        )
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        return InventoryFile(
            category_id=category.name,
            category_name=_category_name(category.name),
            relative_path=relative_path,
            file_name=path.name,
            extension=suffix,
            size_bytes=size_bytes,
            modified_at=modified_at,
            parse_status=InventoryParseStatus.ERROR,
            detected_encoding=None,
            estimated_chapter_count=0,
            title=title,
            normalized_title=normalize_title(title),
            warnings=[f"解析失败：{type(exc).__name__}: {exc}"],
        )


def _eligible(item: InventoryFile) -> bool:
    return item.parse_status in {
        InventoryParseStatus.OK,
        InventoryParseStatus.WARNING,
    } and item.estimated_chapter_count >= 3


def build_inventory(raw_root: Path, corpus_root: Path) -> InventoryManifest:
    raw = _resolved(raw_root)
    corpus = _resolved(corpus_root)
    if not raw.is_dir():
        raise ReferenceCorpusError(f"raw-root 不是目录：{raw}")
    categories: list[Path] = []
    warnings: list[str] = []
    for child in sorted(raw.iterdir(), key=lambda item: item.name.casefold()):
        if not child.is_dir() or child.is_symlink():
            continue
        if _resolved(child) == corpus:
            warnings.append("已排除 corpus-root，不能把派生目录当作 raw category")
            continue
        categories.append(child)
    actual = [
        CategoryDefinition(category_id=category.name, category_name=_category_name(category.name))
        for category in categories
    ]
    expected_ids = {item.category_id for item in EXPECTED_CATEGORIES}
    actual_ids = {item.category_id for item in actual}
    missing = [
        item.category_id for item in EXPECTED_CATEGORIES if item.category_id not in actual_ids
    ]
    extra = sorted(actual_ids - expected_ids, key=str.casefold)
    if missing:
        warnings.append(f"预期类别缺失：{', '.join(missing)}")
    if extra:
        warnings.append(f"发现未列入预期的类别：{', '.join(extra)}")

    files: list[InventoryFile] = []
    for category in categories:
        for candidate in sorted(category.rglob("*"), key=lambda item: item.as_posix().casefold()):
            if candidate.is_file() and not candidate.is_symlink():
                files.append(_scan_inventory_file(raw, category, candidate))

    by_title: dict[tuple[str, str], list[InventoryFile]] = defaultdict(list)
    for item in files:
        by_title[(item.category_id, item.normalized_title)].append(item)
    for (_category_id, normalized), duplicates in by_title.items():
        if normalized and len(duplicates) > 1:
            paths = ", ".join(item.relative_path for item in duplicates)
            for item in duplicates:
                item.warnings.append(f"同类别 normalized title 重复：{paths}")
                if item.parse_status is InventoryParseStatus.OK:
                    item.parse_status = InventoryParseStatus.WARNING

    category_summaries: list[InventoryCategory] = []
    for category in categories:
        category_files = [item for item in files if item.category_id == category.name]
        eligible_count = sum(1 for item in category_files if _eligible(item))
        category_warnings: list[str] = []
        if len(category_files) < 2:
            category_warnings.append("BLOCKER：文件少于两本，无法形成 pilot 对照")
        if eligible_count < 2:
            category_warnings.append("BLOCKER：可解析且有章节证据的文件少于两本")
        category_summaries.append(
            InventoryCategory(
                category_id=category.name,
                category_name=_category_name(category.name),
                file_count=len(category_files),
                supported_file_count=sum(
                    1
                    for item in category_files
                    if item.parse_status is not InventoryParseStatus.UNSUPPORTED
                ),
                eligible_file_count=eligible_count,
                warnings=category_warnings,
            )
        )
    return InventoryManifest(
        schema_version="reference-corpus-inventory-v1",
        created_at=utc_now(),
        raw_root=str(raw),
        corpus_root=str(corpus),
        expected_categories=list(EXPECTED_CATEGORIES),
        actual_categories=actual,
        categories=category_summaries,
        files=files,
        warnings=warnings,
    )


def _format_inventory_markdown(manifest: InventoryManifest) -> str:
    lines = [
        "# Reference Corpus V0 Inventory",
        "",
        f"- raw root: `{manifest.raw_root}`",
        f"- corpus root: `{manifest.corpus_root}`",
        f"- actual categories: {len(manifest.actual_categories)}",
        f"- files: {len(manifest.files)}",
        "- 本表只记录元数据、编码与章节标题估计；未复制或输出原文。",
        "",
        "## Category Summary",
        "",
        "| category | files | supported | eligible | warnings |",
        "|---|---:|---:|---:|---|",
    ]
    for category in manifest.categories:
        lines.append(
            f"| {category.category_id} {category.category_name} | {category.file_count} | "
            f"{category.supported_file_count} | {category.eligible_file_count} | "
            f"{'；'.join(category.warnings) or '—'} |"
        )
    lines.extend(["", "## Files", "", "| category | relative path | title | bytes | chapters | status | warnings |", "|---|---|---|---:|---:|---|---|"])
    for item in manifest.files:
        warning = "；".join(item.warnings).replace("|", "\\|") or "—"
        title = item.title.replace("|", "\\|")
        lines.append(
            f"| {item.category_id} | `{item.relative_path}` | {title} | "
            f"{item.size_bytes} | {item.estimated_chapter_count} | {item.parse_status.value} | {warning} |"
        )
    if manifest.warnings:
        lines.extend(["", "## Inventory Warnings", ""])
        lines.extend(f"- {warning}" for warning in manifest.warnings)
    return "\n".join(lines) + "\n"


def write_inventory(manifest: InventoryManifest, corpus_root: Path) -> dict[str, str]:
    selection_root = _resolved(corpus_root) / "selection"
    selection_root.mkdir(parents=True, exist_ok=True)
    json_path = selection_root / "inventory.json"
    markdown_path = selection_root / "inventory.md"
    json_path.write_text(json_dumps(manifest.model_dump(mode="json"), indent=2) + "\n", encoding="utf-8", newline="\n")
    markdown_path.write_text(_format_inventory_markdown(manifest), encoding="utf-8", newline="\n")
    return {"json": str(json_path), "markdown": str(markdown_path)}


def load_inventory(path: Path) -> InventoryManifest:
    try:
        value = (
            yaml.safe_load(path.read_text(encoding="utf-8"))
            if path.suffix in {".yaml", ".yml"}
            else json.loads(path.read_text(encoding="utf-8"))
        )
        return InventoryManifest.model_validate(value)
    except (OSError, UnicodeError, ValueError, ValidationError, yaml.YAMLError) as exc:
        raise ReferenceCorpusError(f"inventory 无法校验：{path}") from exc


def _coverage_key(item: InventoryFile) -> tuple[int, int, int, int, str]:
    return (
        int(item.estimated_chapter_count >= 20),
        item.estimated_chapter_count,
        int(math.log1p(item.size_bytes) * 1000),
        -len(item.warnings),
        item.relative_path.casefold(),
    )


def _contrast_distance(first: InventoryFile, second: InventoryFile) -> float:
    first_chapters = max(1, first.estimated_chapter_count)
    second_chapters = max(1, second.estimated_chapter_count)
    first_density = first.size_bytes / first_chapters
    second_density = second.size_bytes / second_chapters
    return (
        abs(math.log1p(first_chapters) - math.log1p(second_chapters))
        + 0.35 * abs(math.log1p(first.size_bytes) - math.log1p(second.size_bytes))
        + 0.25 * abs(math.log1p(first_density) - math.log1p(second_density))
    )


def _warning_text(item: InventoryFile) -> str:
    return "；".join(item.warnings) if item.warnings else "无"


def _recommendation(
    item: InventoryFile,
    category: InventoryCategory,
    role: str,
    alternatives: list[InventoryFile],
) -> SelectionRecommendation:
    if role == "coverage-anchor":
        reason = (
            f"可解析；估计 {item.estimated_chapter_count} 个章节、{item.size_bytes} bytes，"
            "以章节覆盖和可追溯章节证据作为类别锚点；未将文件大小单独当作质量判断。"
        )
    elif role == "structural-contrast":
        reason = (
            f"可解析；估计 {item.estimated_chapter_count} 个章节、{item.size_bytes} bytes，"
            "与同类别锚点在章节规模/每章字节密度上形成结构对照，便于后续 2-book pilot。"
        )
    elif _eligible(item):
        reason = (
            f"补位代表书；估计 {item.estimated_chapter_count} 个章节、{item.size_bytes} bytes，"
            "保留真实来源类别，用于扩大代表性覆盖，不改变主推荐的两本对照。"
        )
    else:
        reason = (
            f"补位代表书；inventory 仅记录 {item.size_bytes} bytes，章节证据不足，"
            "保留真实来源类别，仅用于代表性覆盖；蒸馏前必须人工复核。"
        )
    return SelectionRecommendation(
        source_path=item.relative_path,
        title=item.title,
        category=category.category_id,
        category_name=category.category_name,
        selection_reason=reason,
        contrast_role=role,
        known_warning=_warning_text(item),
        alternatives=[
            SelectionAlternative(
                source_path=alternative.relative_path,
                title=alternative.title,
                known_warning=_warning_text(alternative),
            )
            for alternative in alternatives
        ],
    )


def propose_selection(manifest: InventoryManifest) -> PilotSelectionProposal:
    by_category: dict[str, list[InventoryFile]] = defaultdict(list)
    for item in manifest.files:
        by_category[item.category_id].append(item)
    inventory_categories = {item.category_id: item for item in manifest.categories}
    expected_order = [item.category_id for item in manifest.expected_categories]
    actual_order = [item.category_id for item in manifest.actual_categories]
    ordered_ids = expected_order + [item for item in actual_order if item not in expected_order]
    proposal_categories: list[SelectionCategory] = []
    blocking_issues: list[str] = []
    for category_id in ordered_ids:
        category = inventory_categories.get(category_id)
        if category is None:
            definition = next(
                (item for item in manifest.expected_categories if item.category_id == category_id),
                CategoryDefinition(category_id=category_id, category_name=_category_name(category_id)),
            )
            blocker = f"BLOCKER：raw root 缺少直接子目录 {category_id}"
            blocking_issues.append(blocker)
            proposal_categories.append(
                SelectionCategory(
                    category_id=definition.category_id,
                    category_name=definition.category_name,
                    status="BLOCKED",
                    recommendations=[],
                    blocker=blocker,
                )
            )
            continue
        eligible = [item for item in by_category[category_id] if _eligible(item)]
        eligible.sort(key=_coverage_key, reverse=True)
        if len(eligible) < 2:
            blocker = f"BLOCKER：{category_id} 只有 {len(eligible)} 本可解析且有章节证据的候选，少于两本"
            blocking_issues.append(blocker)
            proposal_categories.append(
                SelectionCategory(
                    category_id=category.category_id,
                    category_name=category.category_name,
                    status="BLOCKED",
                    recommendations=[],
                    blocker=blocker,
                )
            )
            continue
        first = eligible[0]
        remaining = eligible[1:]
        second = max(
            remaining,
            key=lambda item: (_contrast_distance(first, item), _coverage_key(item)),
        )
        selected = {first.relative_path, second.relative_path}
        alternatives = [item for item in eligible if item.relative_path not in selected][:3]
        proposal_categories.append(
            SelectionCategory(
                category_id=category.category_id,
                category_name=category.category_name,
                status="PROPOSED",
                recommendations=[
                    _recommendation(first, category, "coverage-anchor", alternatives),
                    _recommendation(second, category, "structural-contrast", alternatives),
                ],
            )
        )
    selected_count = sum(len(item.recommendations) for item in proposal_categories)
    supplemental_recommendations: list[SelectionRecommendation] = []
    selected_paths = {
        recommendation.source_path
        for category in proposal_categories
        for recommendation in category.recommendations
    }
    supplemental_target = max(0, PILOT_TARGET_BOOK_COUNT - selected_count)
    category_by_id = {category.category_id: category for category in proposal_categories}

    def candidates_for_supplement(category_id: str) -> list[InventoryFile]:
        candidates = [
            item
            for item in by_category[category_id]
            if item.parse_status in {InventoryParseStatus.OK, InventoryParseStatus.WARNING}
            and item.relative_path not in selected_paths
        ]
        candidates.sort(key=_coverage_key, reverse=True)
        return candidates

    blocked_actual_ids = [
        category_id
        for category_id in actual_order
        if category_by_id[category_id].status == "BLOCKED"
    ]
    for category_id in blocked_actual_ids:
        needed = max(0, 2 - len(category_by_id[category_id].recommendations))
        for _ in range(needed):
            if len(supplemental_recommendations) >= supplemental_target:
                break
            candidates = candidates_for_supplement(category_id)
            if not candidates:
                break
            item = candidates[0]
            selected_paths.add(item.relative_path)
            alternatives = candidates[1:4]
            supplemental_recommendations.append(
                _recommendation(
                    item,
                    inventory_categories[category_id],
                    "supplemental-representative",
                    alternatives,
                )
            )

    while len(supplemental_recommendations) < supplemental_target:
        added_in_round = False
        for category_id in actual_order:
            if len(supplemental_recommendations) >= supplemental_target:
                break
            category = inventory_categories[category_id]
            candidates = candidates_for_supplement(category_id)
            if not candidates:
                continue
            item = candidates[0]
            selected_paths.add(item.relative_path)
            alternatives = candidates[1:4]
            supplemental_recommendations.append(
                _recommendation(item, category, "supplemental-representative", alternatives)
            )
            added_in_round = True
        if not added_in_round:
            break
    selected_count += len(supplemental_recommendations)
    if selected_count < PILOT_TARGET_BOOK_COUNT:
        blocking_issues.append(
            f"BLOCKER：可解析且有章节证据的来源不足，无法补齐 {PILOT_TARGET_BOOK_COUNT} 本；当前 {selected_count} 本"
        )
    return PilotSelectionProposal(
        schema_version="reference-corpus-selection-v1",
        status="PROPOSED",
        created_at=utc_now(),
        raw_root=manifest.raw_root,
        corpus_root=manifest.corpus_root,
        expected_categories=manifest.expected_categories,
        actual_categories=manifest.actual_categories,
        selection_basis=[
            "主推荐先过滤不可解析、格式不支持或章节证据不足的文件；补位可保留代表性来源但显式标记弱章节证据。",
            "coverage-anchor 以章节数量、长篇标志、字节规模和 warning 数共同排序。",
            "第二本最大化章节规模、文件规模与每章密度的结构距离，形成可解释对照。",
            "normalized title 重复只产生 warning，不用额外 hash 判断重复。",
            f"若类别槽位不足，优先用实际 blocker 类别的代表来源，再用其他实际类别补齐 {PILOT_TARGET_BOOK_COUNT} 本；不改写来源类别标签。",
            "该提案只记录 metadata，status 固定为 PROPOSED，不开始语义蒸馏。",
        ],
        categories=proposal_categories,
        supplemental_recommendations=supplemental_recommendations,
        target_book_count=PILOT_TARGET_BOOK_COUNT,
        selected_book_count=selected_count,
        blocking_issues=blocking_issues,
    )


def write_selection_proposal(proposal: PilotSelectionProposal) -> dict[str, str]:
    root = _resolved(Path(proposal.corpus_root)) / "selection"
    root.mkdir(parents=True, exist_ok=True)
    yaml_path = root / "pilot-selection.proposed.yaml"
    markdown_path = root / "pilot-selection.proposed.md"
    yaml_path.write_text(
        yaml.safe_dump(proposal.model_dump(mode="json"), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
        newline="\n",
    )
    lines = [
        "# Reference Corpus V0 Pilot Selection Proposal",
        "",
        "- status: `PROPOSED`",
        f"- target books: {proposal.target_book_count}",
        f"- selected books: {proposal.selected_book_count}",
        "- 本文件等待作者确认；不等于 confirmed selection，也不启动蒸馏。",
        "",
        "## Selection Basis",
        "",
    ]
    lines.extend(f"- {basis}" for basis in proposal.selection_basis)
    lines.extend(["", "## Recommendations", ""])
    for category in proposal.categories:
        lines.append(f"### {category.category_id} {category.category_name} — {category.status}")
        lines.append("")
        if category.blocker:
            lines.append(f"- {category.blocker}")
            lines.append("")
        for index, recommendation in enumerate(category.recommendations, start=1):
            lines.extend(
                [
                    f"{index}. **{recommendation.title}** (`{recommendation.source_path}`)",
                    f"   - role: `{recommendation.contrast_role}`",
                    f"   - reason: {recommendation.selection_reason}",
                    f"   - warning: {recommendation.known_warning}",
                ]
            )
            if recommendation.alternatives:
                lines.append(
                    "   - alternatives: "
                    + ", ".join(
                        f"{item.title} (`{item.source_path}`)" for item in recommendation.alternatives
                    )
                )
        lines.append("")
    if proposal.supplemental_recommendations:
        lines.extend(["## Supplemental Representatives", ""])
        lines.append("这些书用于补齐目标数量；保留 inventory 中的真实来源类别，不冒充缺失类别。")
        lines.append("")
        for index, recommendation in enumerate(proposal.supplemental_recommendations, start=1):
            lines.extend(
                [
                    f"{index}. **{recommendation.title}** (`{recommendation.source_path}`)",
                    f"   - source category: `{recommendation.category}` {recommendation.category_name}",
                    f"   - role: `{recommendation.contrast_role}`",
                    f"   - reason: {recommendation.selection_reason}",
                    f"   - warning: {recommendation.known_warning}",
                ]
            )
            if recommendation.alternatives:
                lines.append(
                    "   - alternatives: "
                    + ", ".join(
                        f"{item.title} (`{item.source_path}`)" for item in recommendation.alternatives
                    )
                )
        lines.append("")
    if proposal.blocking_issues:
        lines.extend(["## Blocking Issues", ""])
        lines.extend(f"- {issue}" for issue in proposal.blocking_issues)
        lines.append("")
    markdown_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return {"yaml": str(yaml_path), "markdown": str(markdown_path)}


def load_selection(path: Path) -> PilotSelectionProposal:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        return PilotSelectionProposal.model_validate(value)
    except (OSError, UnicodeError, yaml.YAMLError, ValidationError, ValueError) as exc:
        raise ReferenceCorpusError(f"selection 无法校验：{path}") from exc


def validate_selection(
    inventory: InventoryManifest,
    proposal: PilotSelectionProposal,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    by_path = {item.relative_path: item for item in inventory.files}
    categories = {item.category_id: item for item in inventory.categories}
    seen: set[str] = set()
    proposal_by_category = {item.category_id: item for item in proposal.categories}
    for expected in inventory.expected_categories:
        if expected.category_id not in proposal_by_category:
            errors.append(f"BLOCKER：selection 缺少类别 {expected.category_id}")
    for blocker in proposal.blocking_issues:
        if blocker not in errors:
            errors.append(blocker)
    for category in proposal.categories:
        actual_category = categories.get(category.category_id)
        if actual_category is None:
            if category.recommendations:
                errors.append(f"selection 为不存在的类别提供了推荐：{category.category_id}")
            continue
        if category.status == "PROPOSED" and len(category.recommendations) != 2:
            errors.append(
                f"BLOCKER：{category.category_id} 推荐数量为 {len(category.recommendations)}，不是恰好两本"
            )
        if category.status == "BLOCKED":
            warnings.append(f"{category.category_id} 标记 BLOCKED：{category.blocker}")
        for recommendation in category.recommendations:
            if recommendation.source_path in seen:
                errors.append(f"selection 重复推荐：{recommendation.source_path}")
            seen.add(recommendation.source_path)
            source = by_path.get(recommendation.source_path)
            if source is None:
                errors.append(f"selection source_path 不在 inventory：{recommendation.source_path}")
                continue
            if Path(recommendation.source_path).is_absolute() or ".." in Path(recommendation.source_path).parts:
                errors.append(f"selection source_path 必须是 raw root 相对路径：{recommendation.source_path}")
            if source.category_id != category.category_id:
                errors.append(f"selection category 与 inventory 不一致：{recommendation.source_path}")
            if recommendation.title != source.title:
                errors.append(f"selection title 与 inventory 不一致：{recommendation.source_path}")
            if not _eligible(source):
                errors.append(f"selection 选择了没有足够章节证据的文件：{recommendation.source_path}")
    for recommendation in proposal.supplemental_recommendations:
        if recommendation.source_path in seen:
            errors.append(f"supplemental selection 重复推荐：{recommendation.source_path}")
        seen.add(recommendation.source_path)
        source = by_path.get(recommendation.source_path)
        if source is None:
            errors.append(
                f"supplemental selection source_path 不在 inventory：{recommendation.source_path}"
            )
            continue
        if Path(recommendation.source_path).is_absolute() or ".." in Path(recommendation.source_path).parts:
            errors.append(
                f"supplemental selection source_path 必须是 raw root 相对路径：{recommendation.source_path}"
            )
        if source.category_id != recommendation.category:
            errors.append(
                f"supplemental selection category 与 inventory 不一致：{recommendation.source_path}"
            )
        if recommendation.title != source.title:
            errors.append(
                f"supplemental selection title 与 inventory 不一致：{recommendation.source_path}"
            )
        if not _eligible(source):
            warnings.append(
                f"supplemental selection 章节证据不足，蒸馏前需人工复核：{recommendation.source_path}"
            )
    for inventory_category in inventory.categories:
        selected = [
            item
            for item in proposal.categories
            if item.category_id == inventory_category.category_id
        ]
        count = sum(len(item.recommendations) for item in selected)
        if inventory_category.eligible_file_count >= 2 and count != 2:
            errors.append(
                f"BLOCKER：{inventory_category.category_id} 应有两本推荐，实际 {count} 本"
            )
        if inventory_category.eligible_file_count < 2:
            category_prefix = f"BLOCKER：{inventory_category.category_id}"
            if not any(error.startswith(category_prefix) for error in errors):
                errors.append(f"BLOCKER：{inventory_category.category_id} 可选文件少于两本")
    errors = list(dict.fromkeys(errors))
    if proposal.selected_book_count != proposal.target_book_count:
        errors.append(
            f"selection 未达到目标数量：当前 {proposal.selected_book_count}，目标 {proposal.target_book_count}"
        )
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "selected_book_count": len(seen),
    }


def validate_card_frontmatter(text: str, *, path: Path | None = None) -> CorpusCardFrontmatter:
    if not text.startswith("---"):
        label = f"：{path}" if path else ""
        raise ReferenceCorpusError(f"卡片缺少 YAML frontmatter{label}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ReferenceCorpusError("卡片 frontmatter 未闭合")
    try:
        value = yaml.safe_load(parts[1])
        return CorpusCardFrontmatter.model_validate(value)
    except (yaml.YAMLError, ValidationError, TypeError, ValueError) as exc:
        label = f"：{path}" if path else ""
        raise ReferenceCorpusError(f"卡片 frontmatter 无效{label}") from exc


def validate_schema_pack(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ReferenceCorpusError(f"schema pack 无法读取：{path}") from exc
    if not isinstance(value, dict):
        raise ReferenceCorpusError("schema pack 顶层必须是 mapping")
    if value.get("api_version") != "gbrain-schema-pack-v1":
        raise ReferenceCorpusError("schema pack api_version 必须是 gbrain-schema-pack-v1")
    if value.get("name") != "novel-reference-corpus-v1":
        raise ReferenceCorpusError("schema pack name 不符合 Reference Corpus V0")
    page_types = value.get("page_types")
    if not isinstance(page_types, list) or {item.get("name") for item in page_types if isinstance(item, dict)} != SCHEMA_PACK_PAGE_TYPES:
        raise ReferenceCorpusError("schema pack page_types 必须恰好包含 Reference Corpus V1 九种类型")
    for item in page_types:
        if not isinstance(item, dict):
            raise ReferenceCorpusError("schema pack page_type 必须是 mapping")
        if item.get("primitive") not in SCHEMA_PACK_PRIMITIVES:
            raise ReferenceCorpusError(f"schema pack primitive 不受 GBrain 支持：{item.get('primitive')}")
        if item.get("expert_routing") is not True:
            raise ReferenceCorpusError(f"schema pack 类型未开启 expert_routing：{item.get('name')}")
        prefixes = item.get("path_prefixes")
        if not isinstance(prefixes, list) or len(prefixes) != 1 or not str(prefixes[0]).endswith("/"):
            raise ReferenceCorpusError(f"schema pack path_prefixes 无效：{item.get('name')}")
    link_types = value.get("link_types")
    if not isinstance(link_types, list) or {item.get("name") for item in link_types if isinstance(item, dict)} != SCHEMA_PACK_LINK_TYPES:
        raise ReferenceCorpusError("schema pack link_types 与 V0 contract 不一致")
    return {
        "valid": True,
        "name": value["name"],
        "version": value.get("version"),
        "page_type_count": len(page_types),
        "link_type_count": len(link_types),
        "primitive_mapping": {
            "analysis-semantic-role": "media (GBrain primitive enum 不提供 analysis)",
        },
    }


def _yaml_config(corpus_root: Path, raw_root: Path) -> dict[str, Any]:
    return {
        "schema_version": "reference-corpus-v0",
        "corpus_id": "novel-reference-corpus",
        "status": "SCAFFOLD_ONLY",
        "raw_root": str(_resolved(raw_root)),
        "derived_root": str(_resolved(corpus_root)),
        "raw_policy": {
            "read_only": True,
            "copy_into_derived_root": False,
            "searchable_in_gbrain": False,
        },
        "knowledge_authority": "markdown-json",
        "gbrain": {
            "topology_status": "PENDING_ENVIRONMENT_AUDIT",
            "candidate_source_id": "novel-reference-corpus",
            "federated": False,
            "indexed_content": "derived-markdown-cards-only",
            "db_operations": "NOT_RUN",
        },
    }


def _schema_pack() -> dict[str, Any]:
    page_types = [
        ("reference-book", "media", "books/"),
        ("book-dna", "media", "book-dna/"),
        ("prose-dna", "media", "prose-dna/"),
        ("arc-observation", "annotation", "arcs/"),
        ("observation", "annotation", "observations/"),
        ("mechanism-card", "concept", "mechanisms/"),
        ("contrast-card", "media", "contrasts/"),
        ("corpus-synthesis", "media", "syntheses/"),
        ("taste-note", "annotation", "taste/"),
    ]
    return {
        "api_version": "gbrain-schema-pack-v1",
        "name": "novel-reference-corpus-v1",
        "version": "0.1.0",
        "description": "Reference Corpus V0 derived creative-decision cards; never source novel text.",
        "gbrain_min_version": "0.42.0",
        "extends": "gbrain-base-v2",
        "borrow_from": [],
        "page_types": [
            {
                "name": name,
                "primitive": primitive,
                "path_prefixes": [prefix],
                "aliases": [],
                "extractable": False,
                "expert_routing": True,
            }
            for name, primitive, prefix in page_types
        ],
        "link_types": [
            {"name": "distilled-from", "inverse": "distills"},
            {"name": "evidenced-by", "inverse": "evidence-for"},
            {"name": "appears-in", "inverse": "contains"},
            {"name": "synthesized-from", "inverse": "supports-synthesis"},
            {"name": "contrasts-with", "inverse": "contrasted-by"},
            {"name": "variant-of", "inverse": "has-variant"},
            {"name": "taste-rates", "inverse": "rated-by"},
        ],
        "takes_kinds": ["fact", "take", "bet", "hunch"],
        "frontmatter_links": [],
        "enrichable_types": [],
        "filing_rules": [],
    }


def create_scaffold(corpus_root: Path, raw_root: Path) -> dict[str, Any]:
    corpus = _resolved(corpus_root)
    raw = _resolved(raw_root)
    if _is_within(corpus, raw):
        raise ReferenceCorpusError("corpus-root 必须位于 raw-root 外部，避免派生目录被当作类别")
    corpus.mkdir(parents=True, exist_ok=True)
    for relative in SCAFFOLD_DIRS:
        (corpus / relative).mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {
        "RESOLVER.md": """# Reference Corpus Resolver\n\n- `reference-book`: 来源书元数据页。\n- `book-dna`: 单书整体结构观察。\n- `prose-dna`: 单书中文 prose 执行观察；不负责故事规划。\n- `arc-observation`: 单书篇章结构观察。\n- `mechanism-card`: 跨书综合后的条件化可迁移机制。\n- `contrast-card`: 相近创作问题的不同解法对照。\n- `corpus-synthesis`: 类别或跨类别综合。\n- `taste-note`: 作者显式写入的喜欢/中性/不喜欢及理由。\n\nBOOK_OBSERVATION 不自动升级为 Mechanism；Prose DNA 不自动升级为作者文风或 Canon；模型判断不自动升级为 AUTHOR_TASTE。\n""",
        "schema.md": """# Reference Corpus V0 Schema\n\n长期本体是 Markdown + JSON；GBrain 只提供可重建索引。\n\n每张来源性卡片必须带 `source_book_id` 与 `locator`，并可回指 chapter/segment/line range。\n知识等级只有：`BOOK_OBSERVATION`、`CROSS_BOOK_CONTRAST`、`CORPUS_SYNTHESIS`、`AUTHOR_TASTE`。\n\nGBrain 当前 schema pack 的 primitive 是封闭枚举；语义上的 analysis role 映射为 `media`，不伪造不存在的 `analysis` primitive。\n""",
        "corpus.yaml": yaml.safe_dump(_yaml_config(corpus, raw), allow_unicode=True, sort_keys=False),
        "docs/REFERENCE_CORPUS_V0_PLAN.md": """# Reference Corpus V0 后续计划\n\n本轮停在确定性 inventory、schema、架构与作者待确认的 `PROPOSED` selection。\n\n1. Phase 3：4-book smoke，至少跨两个类别，生成 Book DNA/Arc Observation/单书 Finding，不生成通用 Mechanism。\n2. Phase 4：26-book per-book distillation；每本独立、可恢复、有界并发，类别完成后才 sync/embed。\n3. Phase 5：每类别两本只形成 `PILOT TWO-BOOK CONTRAST`。\n4. Phase 6：跨类别综合，保留变体、反例与 failure mode。\n5. Phase 7：metadata filter、lexical/BM25、embedding、graph、可选 rerank；查询返回 3–8 张卡片。\n6. Phase 8：只读 `novel corpus query` adapter，不自动注入生产流程。\n7. Phase 9：至少 5 个 Seed 做 A/B，验证来源泄漏、套路收敛和作者口味。\n\n权威顺序：Hard Canon/Source facts > Explicit Author Intent > Current-book Self Understanding > Reference Corpus > Generic Model Prior。\n""",
        "docs/GBRAIN_TOPOLOGY_DECISION.md": """# GBrain Topology Decision\n\n状态：`PENDING_ENVIRONMENT_AUDIT`。必须先读取本机 CLI 的 source/topology 状态；当前 lock 或命令不支持时不注册。\n\n候选：\n- A：卡片盒子已经是 source 且 nested source 会重复索引；不新增 source，只在兼容的 active pack 上扩展 path prefix。\n- B：reference-corpus 不在父 source，或能干净注册；使用 `novel-reference-corpus`，`federated=false`，查询显式指定 source。\n- C：只有 source 无法隔离且 schema/lock 真实阻塞时才提案独立 brain；本轮不自动创建。\n\n未来执行前必须确认：`gbrain sources list --json`、`gbrain mounts list --json`、active schema、父 source path overlap。\n回滚：未注册 source 时删除 proposal；已注册时使用本机对应的 `sources remove`，不删除数据库目录、不改 lock。\n""",
        "operations/README.md": "# Operations\n\n只存可恢复的 inventory/selection/distillation 操作记录；本轮不启动语义蒸馏。\n",
        "skills/README.md": "# Skills\n\n后续由 Codex skill 执行阅读、解释与综合；确定性 CLI 不承担文学判断。\n",
        "schema-pack/novel-reference-corpus-v1/pack.yaml": yaml.safe_dump(
            _schema_pack(), allow_unicode=True, sort_keys=False
        ),
    }
    written: list[str] = []
    for relative, content in files.items():
        path = corpus / relative
        if not path.exists():
            path.write_text(content, encoding="utf-8", newline="\n")
            written.append(str(path))
    return {"corpus_root": str(corpus), "raw_root": str(raw), "created": written}


def _load_corpus_config(corpus_root: Path) -> dict[str, Any]:
    path = _resolved(corpus_root) / "corpus.yaml"
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ReferenceCorpusError(f"corpus.yaml 无法读取：{path}") from exc
    if not isinstance(value, dict):
        raise ReferenceCorpusError("corpus.yaml 顶层必须是 mapping")
    return value


def validate_corpus(corpus_root: Path) -> dict[str, Any]:
    root = _resolved(corpus_root)
    errors: list[str] = []
    warnings: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"缺少 required file：{relative}")
    for relative in SCAFFOLD_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"缺少 required directory：{relative}")
    for forbidden in FORBIDDEN_DIR_NAMES:
        if (root / forbidden).exists():
            errors.append(f"派生 root 禁止出现完整正文目录：{forbidden}/")
    leaked = [
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.suffix.casefold() in RAW_EXTENSIONS
    ]
    if leaked:
        errors.append("派生 root 出现疑似来源正文文件：" + ", ".join(sorted(leaked)))
    config: dict[str, Any] = {}
    if (root / "corpus.yaml").is_file():
        try:
            config = _load_corpus_config(root)
        except ReferenceCorpusError as exc:
            errors.append(str(exc))
    pack_result: dict[str, Any] = {}
    pack_path = root / "schema-pack/novel-reference-corpus-v1/pack.yaml"
    if pack_path.is_file():
        try:
            pack_result = validate_schema_pack(pack_path)
        except ReferenceCorpusError as exc:
            errors.append(str(exc))
    inventory_path = root / "selection/inventory.json"
    inventory: InventoryManifest | None = None
    if inventory_path.is_file():
        try:
            inventory = load_inventory(inventory_path)
        except ReferenceCorpusError as exc:
            errors.append(str(exc))
    else:
        warnings.append("尚未生成 selection/inventory.json")
    selection_path = root / "selection/pilot-selection.proposed.yaml"
    selection_result: dict[str, Any] = {}
    if selection_path.is_file() and inventory is not None:
        try:
            selection_result = validate_selection(inventory, load_selection(selection_path))
            errors.extend(selection_result["errors"])
            warnings.extend(selection_result["warnings"])
        except ReferenceCorpusError as exc:
            errors.append(str(exc))
    else:
        warnings.append("尚未生成 selection/pilot-selection.proposed.yaml")
    card_count = 0
    for directory in CARD_DIRS:
        card_root = root / directory
        if not card_root.is_dir():
            continue
        for path in card_root.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---"):
                warnings.append(f"卡片尚未写入 frontmatter，暂不阻塞：{path.relative_to(root).as_posix()}")
                continue
            card_count += 1
            try:
                validate_card_frontmatter(text, path=path)
            except ReferenceCorpusError as exc:
                errors.append(str(exc))
    return {
        "valid": not errors,
        "corpus_root": str(root),
        "errors": errors,
        "warnings": warnings,
        "config": config,
        "schema_pack": pack_result,
        "inventory": {
            "actual_category_count": len(inventory.actual_categories) if inventory else 0,
            "file_count": len(inventory.files) if inventory else 0,
        },
        "selection": selection_result,
        "card_count": card_count,
    }


def corpus_status(corpus_root: Path) -> dict[str, Any]:
    root = _resolved(corpus_root)
    config: dict[str, Any] = {}
    if (root / "corpus.yaml").is_file():
        config = _load_corpus_config(root)
    inventory_path = root / "selection/inventory.json"
    inventory: InventoryManifest | None = None
    if inventory_path.is_file():
        inventory = load_inventory(inventory_path)
    proposal_path = root / "selection/pilot-selection.proposed.yaml"
    confirmed_path = root / "selection/confirmed.yaml"
    return {
        "corpus_root": str(root),
        "scaffold_exists": root.is_dir() and all((root / relative).exists() for relative in REQUIRED_FILES),
        "inventory_exists": inventory_path.is_file(),
        "proposal_exists": proposal_path.is_file(),
        "confirmed_selection_exists": confirmed_path.is_file(),
        "selection_status": "CONFIRMED" if confirmed_path.is_file() else "PROPOSED" if proposal_path.is_file() else "NONE",
        "actual_category_count": len(inventory.actual_categories) if inventory else 0,
        "file_count": len(inventory.files) if inventory else 0,
        "gbrain": config.get("gbrain", {"topology_status": "UNKNOWN"}),
    }


__all__ = [
    "EXPECTED_CATEGORIES",
    "PILOT_TARGET_BOOK_COUNT",
    "ReferenceCorpusError",
    "build_inventory",
    "corpus_status",
    "create_scaffold",
    "load_inventory",
    "load_selection",
    "propose_selection",
    "validate_card_frontmatter",
    "validate_corpus",
    "validate_schema_pack",
    "validate_selection",
    "write_inventory",
    "write_selection_proposal",
]
