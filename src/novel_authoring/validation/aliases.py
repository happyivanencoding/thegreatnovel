from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

AliasResolutionStatus = Literal[
    "EXACT",
    "UNIQUE_ALIAS",
    "NOT_FOUND",
    "AMBIGUOUS",
    "CONFLICT",
]


class AliasResolution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requested: str
    status: AliasResolutionStatus
    canonical_id: str | None = None
    matches: list[str] = Field(default_factory=list)


def _normalize(value: object) -> str:
    return re.sub(
        r"\s+",
        " ",
        unicodedata.normalize("NFKC", str(value or "")).strip(),
    ).casefold()


def _aliases(record: Mapping[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("name", "title", "display_name"):
        if record.get(key):
            values.append(str(record[key]))
    raw = record.get("aliases", record.get("aliases_json", []))
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
        except (TypeError, ValueError):
            parsed = [raw]
        raw = parsed
    if isinstance(raw, list):
        values.extend(str(item) for item in raw if str(item).strip())
    return list(dict.fromkeys(values))


def resolve_projection_alias(
    collection: Mapping[str, Mapping[str, Any]], requested: str
) -> AliasResolution:
    """Resolve a Canon/Projection ID or display alias without fuzzy matching."""

    raw_requested = str(requested or "").strip()
    normalized = _normalize(raw_requested)
    if not normalized:
        return AliasResolution(requested=raw_requested, status="NOT_FOUND")

    exact_ids: set[str] = set()
    alias_ids: set[str] = set()
    for key, raw_record in collection.items():
        record = raw_record if isinstance(raw_record, Mapping) else {}
        canonical_id = str(record.get("id") or record.get("resource_id") or key)
        if _normalize(key) == normalized or _normalize(canonical_id) == normalized:
            exact_ids.add(canonical_id)
        if any(_normalize(alias) == normalized for alias in _aliases(record)):
            alias_ids.add(canonical_id)

    competing_aliases = alias_ids - exact_ids
    if exact_ids and competing_aliases:
        return AliasResolution(
            requested=raw_requested,
            status="CONFLICT",
            matches=sorted(exact_ids | alias_ids),
        )
    if len(exact_ids) == 1:
        canonical_id = next(iter(exact_ids))
        return AliasResolution(
            requested=raw_requested,
            status="EXACT",
            canonical_id=canonical_id,
            matches=[canonical_id],
        )
    if len(alias_ids) == 1:
        canonical_id = next(iter(alias_ids))
        return AliasResolution(
            requested=raw_requested,
            status="UNIQUE_ALIAS",
            canonical_id=canonical_id,
            matches=[canonical_id],
        )
    if alias_ids:
        return AliasResolution(
            requested=raw_requested,
            status="AMBIGUOUS",
            matches=sorted(alias_ids),
        )
    return AliasResolution(requested=raw_requested, status="NOT_FOUND")


__all__ = ["AliasResolution", "AliasResolutionStatus", "resolve_projection_alias"]
