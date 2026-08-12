"""Controlled semantic discovery of author-reviewable kernel contracts.

The discovery task is a Local File Handoff.  Python freezes bounded evidence,
validates every returned chapter/span reference, and stores proposal records.
Nothing in this module confirms a contract or mutates Canon.
"""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.atlas.service import latest_atlas
from novel_authoring.author_control.book_profile import load_effective_book_profile
from novel_authoring.author_control.projections import build_story_game_state
from novel_authoring.author_control.reveal import build_reveal_agenda
from novel_authoring.author_control.service import author_control_view
from novel_authoring.author_control.truth import list_author_truths
from novel_authoring.db.database import Database
from novel_authoring.distill.service import latest_distill_reference
from novel_authoring.edition import edition_chapters
from novel_authoring.initialization.service import latest_initialization
from novel_authoring.progression.interpretation import KernelContractProposalBundle
from novel_authoring.progression.models import ContractStatus
from novel_authoring.progression.service import (
    ProgressionContractType,
    create_contract_proposal,
    list_contract_records,
)
from novel_authoring.serial_kernel.models import PROGRESSION_DRIVES
from novel_authoring.storage.layout import BookLayout

_CONTEXT_CHAPTER_LIMIT = 8
_CHAPTER_EXCERPT_LIMIT = 6_000
_REFERENCE_TEXT_LIMIT = 12_000
_DISCOVERY_ARTIFACT = "artifacts/kernel_contract_discovery/proposal.json"


class KernelDiscoveryEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim: str = Field(min_length=1)
    source_layer: Literal[
        "SOURCE_TEXT",
        "CHAPTER_CONTINUITY_INDEX",
        "SOURCE_STATE",
        "CURRENT_BOUNDARY",
        "GLOBAL_BOOK_PROFILE",
        "AUTHOR_TRUTH",
        "REVEAL_AGENDA",
        "STORY_ATLAS",
        "DISTILLATION_PACKAGE",
    ]
    chapter_id: str | None = None
    chapter_ordinal: int | None = Field(default=None, ge=1)
    source_span_ids: list[str] = Field(default_factory=list)
    evidence_quote: str = ""
    confidence: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def validate_source_evidence(self) -> KernelDiscoveryEvidence:
        if (self.chapter_id is None) != (self.chapter_ordinal is None):
            raise ValueError("chapter_id 与 chapter_ordinal 必须同时提供")
        if self.source_layer == "SOURCE_TEXT" and (
            self.chapter_id is None or not self.source_span_ids or not self.evidence_quote
        ):
            raise ValueError("SOURCE_TEXT evidence 必须包含章节、source span 与原文摘录")
        return self


class KernelContractDiscoveryArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["kernel-contract-discovery-v1"]
    discovery_mode: Literal["SEMANTIC_CONTROLLED"]
    book_id: str
    edition_id: str
    context_chapter_id: str
    context_chapter_ordinal: int = Field(ge=1)
    source_chapter_ids: list[str] = Field(min_length=1, max_length=_CONTEXT_CHAPTER_LIMIT)
    evidence: list[KernelDiscoveryEvidence] = Field(min_length=1)
    unknowns: list[str] = Field(default_factory=list)
    proposal_bundle: KernelContractProposalBundle
    author_confirmation_required: Literal[True] = True
    canon_committed: Literal[False] = False

    @model_validator(mode="after")
    def validate_proposal_lifecycle(self) -> KernelContractDiscoveryArtifact:
        bundle = self.proposal_bundle
        lifecycle = [
            bundle.reader_experience.status,
            bundle.narrative_drive.status,
            bundle.genre.status,
            bundle.world_expansion.status,
            bundle.payoff_channels.status,
        ]
        if bundle.progression is not None:
            lifecycle.append(bundle.progression.status)
        if any(status is not ContractStatus.INFERRED_PROPOSAL for status in lifecycle):
            raise ValueError("语义发现只能返回 INFERRED_PROPOSAL")
        drive_mix = set(bundle.narrative_drive.drive_mix)
        if bundle.progression is not None and not drive_mix.intersection(PROGRESSION_DRIVES):
            raise ValueError("非成长 Narrative Drive 不得强制生成 Progression Contract")
        return self


def _bounded_file(path: Path, limit: int = _REFERENCE_TEXT_LIMIT) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")[:limit]
    except (OSError, UnicodeError):
        return None


def _bounded_json(path: Path, limit: int = _REFERENCE_TEXT_LIMIT) -> Any:
    text = _bounded_file(path, limit)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"bounded_text": text}


def _chapter_snapshot(chapter: dict[str, Any], spans: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "chapter_id": str(chapter["chapter_id"]),
        "ordinal": int(chapter["ordinal"]),
        "title": str(chapter.get("title") or chapter.get("raw_heading") or ""),
        "document_status": str(chapter.get("document_status") or "SOURCE"),
        "content_excerpt": str(chapter.get("content") or "")[:_CHAPTER_EXCERPT_LIMIT],
        "source_spans": spans,
    }


def _select_world_state(world_state: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "chapter",
        "timepoint",
        "characters",
        "inventory",
        "equipment",
        "resources",
        "abilities",
        "knowledge",
        "relationships",
        "locations",
        "factions",
        "world_rules",
        "tasks",
        "threads",
        "promises",
        "chapter_delta",
        "source_state",
        "progression_workspace",
    )
    selected: dict[str, Any] = {}
    for key in keys:
        value = world_state.get(key)
        selected[key] = value[:100] if isinstance(value, list) else value
    return selected


def build_kernel_discovery_context(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    context_chapter_id: str | None = None,
) -> dict[str, Any]:
    """Freeze bounded semantic inputs without rereading the whole novel."""

    started = perf_counter()
    database.initialize()
    with database.connect() as connection:
        chapters = edition_chapters(connection, book_id, edition_id)
        if not chapters:
            raise ValueError("已有小说至少需要一个真实章节才能进行语义合同发现")
        target: dict[str, Any] | None = None
        if context_chapter_id is None:
            target = chapters[-1]
        else:
            target = next(
                (item for item in chapters if str(item["chapter_id"]) == context_chapter_id),
                None,
            )
            if target is None:
                raise ValueError("语义合同发现的上下文章节不存在")
        assert target is not None
        target_ordinal = int(target["ordinal"])
        recent = [item for item in chapters if int(item["ordinal"]) <= target_ordinal][
            -_CONTEXT_CHAPTER_LIMIT:
        ]
        recent_ids = [str(item["chapter_id"]) for item in recent]
        placeholders = ",".join("?" for _ in recent_ids)
        span_rows = connection.execute(
            "SELECT span_id, chapter_id, kind, start_line, end_line, excerpt "
            f"FROM source_spans WHERE book_id=? AND chapter_id IN ({placeholders}) "
            "ORDER BY chapter_id, start_line, span_id",
            (book_id, *recent_ids),
        ).fetchall()
        spans_by_chapter: dict[str, list[dict[str, Any]]] = {item: [] for item in recent_ids}
        for row in span_rows:
            bucket = spans_by_chapter.setdefault(str(row["chapter_id"]), [])
            if len(bucket) < 12:
                bucket.append(dict(row))
        continuity_rows = connection.execute(
            "SELECT chapter_id, status, result_json FROM chapter_analysis_records "
            f"WHERE book_id=? AND edition_id=? AND analysis_layer='CONTINUITY' "
            f"AND chapter_id IN ({placeholders}) ORDER BY chapter_id",
            (book_id, edition_id, *recent_ids),
        ).fetchall()
    recent_snapshots = [
        _chapter_snapshot(item, spans_by_chapter.get(str(item["chapter_id"]), []))
        for item in recent
    ]
    continuity = []
    for row in continuity_rows:
        try:
            payload = json.loads(str(row["result_json"]))
        except json.JSONDecodeError:
            payload = {"status": "INVALID_STORED_ANALYSIS"}
        continuity.append(
            {
                "chapter_id": str(row["chapter_id"]),
                "status": str(row["status"]),
                "payload": payload,
            }
        )

    world_state = build_story_game_state(
        database,
        book_id,
        edition_id,
        chapter_id=str(target["chapter_id"]),
        include_global_scope=True,
    )
    profile = load_effective_book_profile(database, book_id, edition_id)
    truths = list_author_truths(
        database,
        book_id,
        edition_id,
        chapter_ordinal=target_ordinal,
        include_future=False,
    )
    reveal = build_reveal_agenda(database, book_id, edition_id, target_ordinal)
    author_control = author_control_view(database, book_id, edition_id)

    workspace_root = Path(
        str(database.scalar("SELECT workspace_root FROM books WHERE book_id=?", (book_id,)))
    )
    canonical = (workspace_root / "book.yaml").is_file()
    edition_paths = (
        BookLayout(workspace_root.parent).for_book(book_id).edition(edition_id)
        if canonical
        else None
    )
    initialization = latest_initialization(database, book_id, edition_id)
    initialization_context: dict[str, Any] | None = None
    if initialization is not None:
        root = Path(str(initialization["root"]))
        initialization_context = {
            "manifest": initialization.get("manifest"),
            "status": initialization.get("status"),
            "structural_index": _bounded_json(root / "structural_index.json"),
            "world_model": _bounded_file(root / "synthesis" / "current_world_model.md"),
            "narrative_dna": _bounded_file(root / "synthesis" / "narrative_dna.md"),
        }
    distill = latest_distill_reference(edition_paths, scope="SELF_BOOK") if edition_paths else None
    distill_context = None
    if distill is not None:
        distill_context = {
            **distill,
            "machine_package": (
                _bounded_json(Path(str(distill["machine_manifest"])))
                if distill.get("machine_manifest")
                else None
            ),
        }
    atlas = latest_atlas(database, book_id, edition_id)
    atlas_context = None
    if atlas is not None:
        atlas_root = Path(str(atlas["artifact_root"]))
        atlas_context = {
            "atlas_id": str(atlas["atlas_id"]),
            "atlas_version": int(atlas["atlas_version"]),
            "readiness_status": str(atlas["readiness_status"]),
            "narrative_dna": _bounded_file(atlas_root / "narrative_dna.md"),
            "current_world_model": _bounded_file(atlas_root / "current_world_model.md"),
            "world_rules": _bounded_file(atlas_root / "world_rules.yaml"),
            "expansion_grammar": _bounded_file(atlas_root / "expansion_grammar.yaml"),
            "unresolved_assumptions": _bounded_file(
                atlas_root / "unresolved_assumptions.yaml"
            ),
        }

    context: dict[str, Any] = {
        "schema_version": "kernel-contract-discovery-context-v1",
        "discovery_mode": "SEMANTIC_CONTROLLED",
        "book_id": book_id,
        "edition_id": edition_id,
        "context_chapter": {
            "chapter_id": str(target["chapter_id"]),
            "ordinal": target_ordinal,
            "title": str(target.get("title") or target.get("raw_heading") or ""),
        },
        "bounded_inputs": {
            "chapter_limit": _CONTEXT_CHAPTER_LIMIT,
            "chapter_ids": recent_ids,
            "recent_chapters": recent_snapshots,
            "chapter_continuity_index": continuity,
            "current_boundary_and_source_state": _select_world_state(world_state),
            "global_book_profile": profile,
            "author_truths": truths[:100],
            "reveal_agenda": reveal,
            "author_control": author_control,
            "initialization": initialization_context,
            "distillation_package": distill_context,
            "story_atlas": atlas_context,
        },
        "authority_rules": [
            "只输出作者可审核的 INFERRED_PROPOSAL，不得确认合同或修改 Canon",
            "未知必须保持 unknown，不得用题材名称或未来章节补齐",
            "Market Category 不能直接决定 Narrative Drive 或章节调度",
            "只有 Drive Mix 包含成长驱动力时才允许输出 Progression Contract",
            "SOURCE_TEXT 结论必须引用冻结章节中的真实 source span 与原文摘录",
        ],
        "expected_artifact": _DISCOVERY_ARTIFACT,
    }
    encoded = json.dumps(context, ensure_ascii=False)
    context["efficiency"] = {
        "context_build_ms": round((perf_counter() - started) * 1000, 3),
        "source_chapters_read": len(recent_snapshots),
        "full_book_reread": False,
        "context_characters": len(encoded),
    }
    return context


def prepare_kernel_contract_discovery(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    context_chapter_id: str | None = None,
) -> dict[str, Any]:
    context = build_kernel_discovery_context(
        database,
        book_id=book_id,
        edition_id=edition_id,
        context_chapter_id=context_chapter_id,
    )
    from novel_authoring.workflows.handoffs import HandoffType, create_handoff

    return create_handoff(
        database,
        book_id,
        handoff_type=HandoffType.KERNEL_CONTRACT_DISCOVERY,
        requested_stage="KERNEL_CONTRACT_DISCOVERY",
        edition_id=edition_id,
        context_chapter_id=str(context["context_chapter"]["chapter_id"]),
        kernel_discovery_request=context,
    )


def _artifact_path(task_directory: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path.resolve() if path.is_absolute() else (task_directory / path).resolve()


def import_kernel_contract_discovery(
    database: Database,
    *,
    handoff_id: str,
) -> dict[str, Any]:
    """Validate a completed semantic artifact and persist review-only proposals."""

    from novel_authoring.workflows.handoffs import (
        HandoffType,
        HandoffWorkflowError,
        load_completed_handoff_result,
    )

    result = load_completed_handoff_result(database, handoff_id)
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM workflow_handoffs WHERE handoff_id=?", (handoff_id,)
        ).fetchone()
    if row is None or str(row["handoff_type"]) != HandoffType.KERNEL_CONTRACT_DISCOVERY.value:
        raise HandoffWorkflowError("handoff 不是 Kernel Contract Discovery")
    task_directory = Path(str(row["task_directory"])).resolve()
    task_path = (
        task_directory / "input" / "task.json"
        if (task_directory / "input").is_dir()
        else task_directory / "task.json"
    )
    context_path = (
        task_directory / "input" / "kernel_discovery_context.json"
        if (task_directory / "input").is_dir()
        else task_directory / "kernel_discovery_context.json"
    )
    task = json.loads(task_path.read_text(encoding="utf-8"))
    frozen = json.loads(context_path.read_text(encoding="utf-8"))
    artifact_candidates = [
        _artifact_path(task_directory, str(item))
        for item in result.get("artifact_paths", [])
        if str(item).replace("\\", "/").endswith("kernel_contract_discovery/proposal.json")
    ]
    if len(artifact_candidates) != 1 or not artifact_candidates[0].is_file():
        raise HandoffWorkflowError("语义发现结果必须包含唯一 proposal.json artifact")
    artifact = KernelContractDiscoveryArtifact.model_validate_json(
        artifact_candidates[0].read_text(encoding="utf-8")
    )
    if artifact.book_id != str(row["book_id"]) or artifact.edition_id != str(row["edition_id"]):
        raise HandoffWorkflowError("语义发现 artifact 越过冻结 book/edition scope")
    frozen_chapter = dict(frozen["context_chapter"])
    if (
        artifact.context_chapter_id != str(frozen_chapter["chapter_id"])
        or artifact.context_chapter_ordinal != int(frozen_chapter["ordinal"])
    ):
        raise HandoffWorkflowError("语义发现 artifact 的章节边界与冻结输入不一致")
    frozen_ids = set(frozen["bounded_inputs"]["chapter_ids"])
    if not set(artifact.source_chapter_ids).issubset(frozen_ids):
        raise HandoffWorkflowError("语义发现 artifact 引用了未冻结章节")
    chapter_ordinals = {
        str(item["chapter_id"]): int(item["ordinal"])
        for item in frozen["bounded_inputs"]["recent_chapters"]
    }
    for evidence in artifact.evidence:
        if evidence.chapter_id is None:
            continue
        if evidence.chapter_id not in frozen_ids:
            raise HandoffWorkflowError("语义证据引用了未冻结章节")
        if chapter_ordinals[evidence.chapter_id] != evidence.chapter_ordinal:
            raise HandoffWorkflowError("语义证据章节序号与冻结输入不一致")
        if int(evidence.chapter_ordinal or 0) > artifact.context_chapter_ordinal:
            raise HandoffWorkflowError("语义证据泄漏了边界后的未来章节")
        if evidence.source_span_ids:
            placeholders = ",".join("?" for _ in evidence.source_span_ids)
            with database.connect() as connection:
                rows = connection.execute(
                    "SELECT span_id, chapter_id, excerpt FROM source_spans "
                    f"WHERE book_id=? AND span_id IN ({placeholders})",
                    (artifact.book_id, *evidence.source_span_ids),
                ).fetchall()
            found = {str(item["span_id"]): str(item["chapter_id"]) for item in rows}
            if set(evidence.source_span_ids) != set(found):
                raise HandoffWorkflowError("语义证据引用了不存在的 source span")
            if any(chapter_id != evidence.chapter_id for chapter_id in found.values()):
                raise HandoffWorkflowError("source span 不属于 evidence 声明的章节")
            if evidence.evidence_quote and not any(
                evidence.evidence_quote in str(item["excerpt"]) for item in rows
            ):
                raise HandoffWorkflowError("语义证据摘录不存在于声明的 source span")

    bundle = artifact.proposal_bundle
    existing_types = {
        record.contract_type
        for record in list_contract_records(
            database, book_id=artifact.book_id, edition_id=artifact.edition_id
        )
        if record.status not in {ContractStatus.REJECTED, ContractStatus.SUPERSEDED}
    }
    created = []
    for contract_type, payload in (
        (ProgressionContractType.READER_EXPERIENCE, bundle.reader_experience),
        (ProgressionContractType.MARKET_CATEGORY, bundle.market_category),
        (ProgressionContractType.NARRATIVE_DRIVE, bundle.narrative_drive),
        (ProgressionContractType.GENRE, bundle.genre),
        (ProgressionContractType.PROGRESSION, bundle.progression),
        (ProgressionContractType.WORLD_EXPANSION, bundle.world_expansion),
        (ProgressionContractType.PAYOFF_CHANNEL, bundle.payoff_channels),
    ):
        if payload is None or contract_type in existing_types:
            continue
        created.append(
            create_contract_proposal(
                database,
                book_id=artifact.book_id,
                edition_id=artifact.edition_id,
                contract_type=contract_type,
                payload=payload,
                source="KERNEL_CONTRACT_DISCOVERY",
                status=ContractStatus.INFERRED_PROPOSAL,
                author_notes="；".join(item.claim for item in artifact.evidence[:8]),
            )
        )
    return {
        "handoff_id": handoff_id,
        "discovery_mode": artifact.discovery_mode,
        "chapter": frozen_chapter,
        "created": [item.model_dump(mode="json") for item in created],
        "deduplicated": not created,
        "unknowns": artifact.unknowns,
        "author_confirmation_required": True,
        "canon_changed": False,
        "task": task.get("kernel_contract_discovery"),
    }


__all__ = [
    "KernelContractDiscoveryArtifact",
    "KernelDiscoveryEvidence",
    "build_kernel_discovery_context",
    "import_kernel_contract_discovery",
    "prepare_kernel_contract_discovery",
]
