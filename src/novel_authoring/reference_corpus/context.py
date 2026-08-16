"""Frozen, compact Reference Corpus context artifacts.

The query module is the only retrieval gateway.  This module freezes its
already-filtered response for one planning or prose operation so later Corpus
changes cannot rewrite an in-flight task.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from novel_authoring.reference_corpus.query import (
    COMPACT_CARD_ADAPTER,
    QueryMatchTier,
    QueryStatus,
    ReferenceCorpusQueryEcho,
    ReferenceCorpusQueryRequest,
    ReferenceCorpusQueryResponse,
)
from novel_authoring.utils import json_dumps, sha256_bytes, stable_id, utc_now


class ReferenceContextConflict(ValueError):
    """An existing immutable snapshot does not match the requested content."""


class ReferenceContextIntegrityError(ReferenceContextConflict):
    """A persisted snapshot fails its strict schema or canonical hash check."""


def _contains_forbidden(value: object) -> str | None:
    forbidden = {
        "observation_summary",
        "source_quote",
        "raw_text",
        "full_text",
        "source_prose",
        "source_content",
        "book_dna",
        "prose_dna",
        "full_dna",
        "full dna",
        "full-dna",
    }
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).casefold()
            if normalized_key in forbidden:
                return str(key)
            found = _contains_forbidden(nested)
            if found:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = _contains_forbidden(nested)
            if found:
                return found
    return None


class ReferenceContextSnapshot(BaseModel):
    """The only context shape passed from the reference gateway to a task."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["reference-context-snapshot-v1"]
    snapshot_id: str = Field(min_length=1)
    purpose: Literal["PLANNING", "PROSE"]
    book_id: str = Field(min_length=1)
    edition_id: str = Field(min_length=1)
    operation_id: str = Field(min_length=1)
    creative_problem: str = ""
    creative_problem_tags: list[str] = Field(default_factory=list)
    reader_experiences: list[str] = Field(default_factory=list)
    narrative_drives: list[str] = Field(default_factory=list)
    payoff_channels: list[str] = Field(default_factory=list)
    scene_functions: list[str] = Field(default_factory=list)
    max_cards: int = Field(ge=3, le=8)
    match_tier: QueryMatchTier | None = None
    original_query: ReferenceCorpusQueryEcho | None = None
    effective_query: ReferenceCorpusQueryEcho | None = None
    relaxed_fields: list[str] = Field(default_factory=list)
    zero_result_reason: str | None = None
    package_schema_version: str | None = None
    package_hash: str | None = None
    machine_bundle_hash: str | None = None
    selected_card_ids: list[str] = Field(default_factory=list)
    selected_card_count: int = Field(ge=0, le=8)
    selected_card_types: list[str] = Field(default_factory=list)
    selected_card_knowledge_levels: list[str] = Field(default_factory=list)
    metadata_match_fields: dict[str, list[str]] = Field(default_factory=dict)
    compact_cards: list[dict[str, Any]] = Field(default_factory=list, max_length=8)
    knowledge_gaps: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    status: QueryStatus
    usage: Literal["REFERENCE_ONLY"] = "REFERENCE_ONLY"
    created_at: str = Field(min_length=1)
    snapshot_hash: str = Field(min_length=1)

    @field_validator("compact_cards")
    @classmethod
    def validate_compact_cards(cls, cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for card in cards:
            forbidden = _contains_forbidden(card)
            if forbidden:
                raise ValueError(f"Reference Context 不得包含来源正文字段：{forbidden}")
            if card.get("status") != "REFERENCE_ONLY":
                raise ValueError("Reference Context compact card 必须保持 REFERENCE_ONLY")
            # Re-validate the projection against the gateway union.  This also
            # rejects Book DNA/Prose DNA and any unbounded raw card shape.
            COMPACT_CARD_ADAPTER.validate_python(card)
        return cards


_PROMPT_SNAPSHOT_FIELDS = (
    "purpose",
    "status",
    "match_tier",
    "original_query",
    "effective_query",
    "relaxed_fields",
    "zero_result_reason",
    "snapshot_id",
    "snapshot_hash",
    "machine_bundle_hash",
    "selected_card_count",
    "selected_card_ids",
    "selected_card_types",
    "selected_card_knowledge_levels",
    "compact_cards",
    "knowledge_gaps",
    "warnings",
    "usage",
)
_PROMPT_FORBIDDEN_FIELDS = frozenset(
    {
        "source",
        "source_ref",
        "source_refs",
        "source_book_id",
        "source_book_ids",
        "source_id",
        "source_title",
        "distill_id",
        "segment_id",
        "line_start",
        "line_end",
        "raw",
        "raw_text",
        "raw_text_included",
        "full_text",
        "source_quote",
        "source_prose",
        "source_content",
        "observation_summary",
        "evidence",
        "evidence_ref",
        "evidence_refs",
        "evidence_id",
        "locator",
        "locators",
        "provenance",
        "book_dna",
        "prose_dna",
        "full_dna",
    }
)


def _prompt_field_name(key: object) -> str:
    normalized = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", str(key))
    normalized = re.sub(r"[\s-]+", "_", normalized)
    return normalized.casefold()


def _is_forbidden_prompt_field(key: object) -> bool:
    normalized = _prompt_field_name(key)
    return normalized in _PROMPT_FORBIDDEN_FIELDS or normalized.startswith(
        ("source_", "provenance_")
    )


def _project_prompt_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            str(key): _project_prompt_value(nested)
            for key, nested in value.items()
            if not _is_forbidden_prompt_field(key)
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_project_prompt_value(item) for item in value]
    return value


def project_reference_context_for_prompt(
    snapshot_or_dict: ReferenceContextSnapshot | Mapping[str, Any],
) -> dict[str, Any]:
    """Project a full Reference Context Snapshot into prompt-safe context."""

    if isinstance(snapshot_or_dict, ReferenceContextSnapshot):
        payload: Mapping[str, Any] = snapshot_or_dict.model_dump(mode="json")
    elif isinstance(snapshot_or_dict, Mapping):
        payload = snapshot_or_dict
    else:
        raise TypeError("snapshot_or_dict 必须是 ReferenceContextSnapshot 或 mapping")

    projected: dict[str, Any] = {
        key: _project_prompt_value(payload[key])
        for key in _PROMPT_SNAPSHOT_FIELDS
        if key in payload
    }
    cards = projected.get("compact_cards")
    if isinstance(cards, list):
        projected["compact_cards"] = [
            card for card in cards if isinstance(card, dict)
        ]
    return projected


def _hash_payload(snapshot: ReferenceContextSnapshot) -> str:
    # package_hash is a legacy file hash and may change with generated_at;
    # machine_bundle_hash is the retrieval identity that belongs in the seal.
    payload = snapshot.model_dump(
        mode="json",
        exclude={"snapshot_hash", "created_at", "package_hash"},
    )
    return sha256_bytes(json_dumps(payload).encode("utf-8"))


def _read_existing(path: Path) -> ReferenceContextSnapshot:
    return load_reference_context_snapshot(path)


def load_reference_context_snapshot(path: Path | str) -> ReferenceContextSnapshot:
    """Strictly load and integrity-check one persisted context snapshot."""

    target = Path(path).expanduser().resolve()
    try:
        snapshot = ReferenceContextSnapshot.model_validate_json(
            target.read_text(encoding="utf-8"),
            strict=True,
        )
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        raise ReferenceContextIntegrityError(
            f"已有 Reference Context Snapshot 无法严格验证：{target}"
        ) from exc
    expected_hash = _hash_payload(snapshot)
    if snapshot.snapshot_hash != expected_hash:
        raise ReferenceContextIntegrityError(
            f"Reference Context Snapshot hash 不匹配：{target}"
        )
    return snapshot


def freeze_reference_context(
    request: ReferenceCorpusQueryRequest,
    response: ReferenceCorpusQueryResponse,
    *,
    book_id: str,
    edition_id: str,
    operation_id: str,
    output_path: Path | None = None,
) -> ReferenceContextSnapshot:
    """Freeze a query response without reading any raw Corpus/source file."""

    if response.purpose != request.purpose:
        raise ValueError("Reference Query 与 Snapshot purpose 不一致")
    cards = [card.model_dump(mode="json") for card in response.cards]
    request_payload = request.model_dump(mode="json")
    package_identity = (
        response.machine_bundle_hash or response.package_hash or "NO_PACKAGE"
    )
    query_diagnostics = {
        "match_tier": response.match_tier,
        "original_query": (
            response.original_query.model_dump(mode="json")
            if response.original_query is not None
            else None
        ),
        "effective_query": (
            response.effective_query.model_dump(mode="json")
            if response.effective_query is not None
            else None
        ),
        "relaxed_fields": list(response.relaxed_fields),
        "zero_result_reason": response.zero_result_reason,
    }
    snapshot_id = stable_id(
        "reference-context",
        operation_id,
        request.purpose,
        json_dumps(request_payload),
        package_identity,
        json_dumps(query_diagnostics),
    )
    metadata_matches = {
        str(card["card_id"]): list(card.get("metadata_match_fields", []))
        for card in cards
    }
    snapshot = ReferenceContextSnapshot(
        schema_version="reference-context-snapshot-v1",
        snapshot_id=snapshot_id,
        purpose=request.purpose,
        book_id=book_id,
        edition_id=edition_id,
        operation_id=operation_id,
        creative_problem=request.creative_problem,
        creative_problem_tags=list(request.creative_problem_tags),
        reader_experiences=list(request.reader_experiences),
        narrative_drives=list(request.narrative_drives),
        payoff_channels=list(request.payoff_channels),
        scene_functions=list(request.scene_functions),
        max_cards=request.max_cards,
        match_tier=response.match_tier,
        original_query=response.original_query,
        effective_query=response.effective_query,
        relaxed_fields=list(response.relaxed_fields),
        zero_result_reason=response.zero_result_reason,
        package_schema_version=response.package_schema_version,
        package_hash=response.package_hash,
        machine_bundle_hash=response.machine_bundle_hash,
        selected_card_ids=[str(card["card_id"]) for card in cards],
        selected_card_count=len(cards),
        selected_card_types=[str(card["card_type"]) for card in cards],
        selected_card_knowledge_levels=[str(card["knowledge_level"]) for card in cards],
        metadata_match_fields=metadata_matches,
        compact_cards=cards,
        knowledge_gaps=list(response.knowledge_gaps),
        warnings=list(response.warnings),
        status=response.status,
        created_at=utc_now(),
        snapshot_hash="pending",
    )
    snapshot.snapshot_hash = _hash_payload(snapshot)

    if output_path is not None:
        target = output_path.expanduser().resolve()
        if target.is_file():
            existing = _read_existing(target)
            if existing.snapshot_hash != snapshot.snapshot_hash:
                raise ReferenceContextConflict(
                    f"Reference Context Snapshot 已冻结且内容不同：{target}"
                )
            return existing
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json_dumps(snapshot.model_dump(mode="json"), indent=2) + "\n",
            encoding="utf-8",
        )
    return snapshot


__all__ = [
    "ReferenceContextConflict",
    "ReferenceContextIntegrityError",
    "ReferenceContextSnapshot",
    "freeze_reference_context",
    "load_reference_context_snapshot",
    "project_reference_context_for_prompt",
]
