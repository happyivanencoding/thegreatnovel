"""Generic publication-boundary checks for draft prose.

This module deliberately contains only high-confidence internal workflow terms.
Natural-language meta narration remains an edge semantic-review concern and is
accepted here only when an edge finding supplies a quote that Python can verify.
"""

from __future__ import annotations

from collections.abc import Iterable

INTERNAL_WORKFLOW_LANGUAGE: tuple[str, ...] = (
    "ChapterContract",
    "Boundary Packet",
    "CANON_COMMITTED",
    "VALIDATED_DRAFT",
    "primary_thread_id",
    "state_changes",
    "reference_provenance",
)


def internal_workflow_language_hits(prose: str) -> list[str]:
    """Return exact high-confidence system-language hits in prose."""

    return [term for term in INTERNAL_WORKFLOW_LANGUAGE if term in prose]


def edge_publication_findings(value: object) -> Iterable[dict[str, str]]:
    """Yield edge review findings without making the edge authoritative.

    The edge can report a reason and quote; Python later verifies that quote is
    actually present before turning the report into a blocking finding.
    """

    if not isinstance(value, list):
        return []
    result: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        quote = str(item.get("evidence_quote") or item.get("quote") or "").strip()
        reason = str(item.get("reason") or item.get("message") or "").strip()
        if quote or reason:
            result.append({"evidence_quote": quote, "reason": reason})
    return result


__all__ = [
    "INTERNAL_WORKFLOW_LANGUAGE",
    "edge_publication_findings",
    "internal_workflow_language_hits",
]
