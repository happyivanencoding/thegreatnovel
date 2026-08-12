"""Resource and opportunity projections for progression planning."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.progression.models import (
    BreakthroughGate,
    OpportunityInformationStatus,
    OpportunityStatus,
    OpportunitySurface,
    OpportunitySurfaceItem,
    ProgressionEvidence,
)


class ResourceGateAssessment(BaseModel):
    """Evidence-backed assessment; it never consumes or creates a resource."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str
    satisfied: bool = False
    available_resources: list[str] = Field(default_factory=list)
    missing_resources: list[str] = Field(default_factory=list)
    evidence: list[ProgressionEvidence] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


def _chapter(world_state: Mapping[str, Any]) -> tuple[str, int]:
    chapter = world_state.get("chapter")
    if not isinstance(chapter, Mapping) or not chapter.get("chapter_id"):
        raise ValueError("Resource projection 必须显式绑定 chapter_id")
    return str(chapter["chapter_id"]), int(chapter.get("ordinal") or 0)


def _available_resource_names(world_state: Mapping[str, Any]) -> list[str]:
    names: list[str] = []
    for collection in ("resources", "inventory", "equipment"):
        values = world_state.get(collection, [])
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, Mapping):
                continue
            name = value.get("name") or value.get("title") or value.get("statement")
            if name:
                names.append(str(name))
    return list(dict.fromkeys(names))


def evaluate_resource_gate(
    gate: BreakthroughGate,
    world_state: Mapping[str, Any],
    *,
    evidence: Sequence[ProgressionEvidence] = (),
) -> ResourceGateAssessment:
    """Require both chapter-state availability and chapter-pinned evidence."""

    _, chapter_ordinal = _chapter(world_state)
    available = _available_resource_names(world_state)
    available_keys = {value.casefold() for value in available}
    relevant_evidence = [
        item
        for item in evidence
        if item.chapter_ordinal is None or item.chapter_ordinal <= chapter_ordinal
    ]
    statements = " ".join(item.statement.casefold() for item in relevant_evidence)
    missing = [
        resource
        for resource in gate.required_resources
        if resource.casefold() not in available_keys
    ]
    unproven = [
        resource
        for resource in gate.required_resources
        if resource.casefold() not in statements
    ]
    errors = [f"缺少门槛资源：{value}" for value in missing]
    errors.extend(f"资源缺少章节证据：{value}" for value in unproven if value not in missing)
    return ResourceGateAssessment(
        gate_id=gate.gate_id,
        satisfied=not errors,
        available_resources=available,
        missing_resources=missing,
        evidence=relevant_evidence,
        errors=errors,
    )


def project_opportunity_surface(
    world_state: Mapping[str, Any],
    items: Sequence[OpportunitySurfaceItem],
) -> OpportunitySurface:
    """Project only opportunities whose evidence is visible at the selected chapter."""

    chapter_id, chapter_ordinal = _chapter(world_state)
    visible: list[OpportunitySurfaceItem] = []
    for item in items:
        if item.evidence and not any(
            proof.chapter_ordinal is None or proof.chapter_ordinal <= chapter_ordinal
            for proof in item.evidence
        ):
            continue
        visible.append(
            item.model_copy(
                update={
                    "evidence": [
                        proof
                        for proof in item.evidence
                        if proof.chapter_ordinal is None
                        or proof.chapter_ordinal <= chapter_ordinal
                    ]
                }
            )
        )
    return OpportunitySurface(
        chapter_id=chapter_id,
        chapter_ordinal=chapter_ordinal,
        items=visible,
    )


def opportunity_items_from_world_state(
    world_state: Mapping[str, Any],
) -> list[OpportunitySurfaceItem]:
    """Compile explicitly annotated current threads into non-owned opportunities."""

    _, chapter_ordinal = _chapter(world_state)
    items: list[OpportunitySurfaceItem] = []
    for collection in ("tasks", "threads", "promises"):
        values = world_state.get(collection, [])
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values, start=1):
            if not isinstance(value, Mapping):
                continue
            raw = value.get("raw")
            raw = raw if isinstance(raw, Mapping) else {}
            payload = raw.get("payload")
            payload = payload if isinstance(payload, Mapping) else {}
            progression_use = payload.get("progression_use") or value.get(
                "progression_use"
            )
            if not progression_use:
                continue
            evidence_ordinal = int(
                value.get("evidence_chapter_ordinal")
                or value.get("chapter_ordinal")
                or chapter_ordinal
            )
            span_ids = [
                str(item)
                for item in value.get("source_span_ids", [])
                if str(item)
            ]
            evidence = [
                ProgressionEvidence(
                    statement=str(value.get("statement") or progression_use),
                    source_span_id=span_id,
                    chapter_ordinal=evidence_ordinal,
                    information_status="SOURCE_VERIFIED",
                )
                for span_id in span_ids
            ]
            raw_id = str(
                value.get("object_id")
                or value.get("record_id")
                or value.get("state_key")
                or f"{collection}-{index}"
            )
            opportunity_id = re.sub(r"[^A-Za-z0-9._-]+", "-", raw_id).strip("-")
            items.append(
                OpportunitySurfaceItem(
                    opportunity_id=f"opportunity-{opportunity_id}",
                    subject=str(
                        payload.get("title")
                        or value.get("title")
                        or value.get("statement")
                        or raw_id
                    ),
                    progression_use=str(progression_use),
                    source=str(value.get("layer") or value.get("source") or collection),
                    related_entities=[
                        str(item)
                        for item in (
                            payload.get("related_person_id"),
                            payload.get("related_task_id"),
                            payload.get("related_plot_thread_id"),
                        )
                        if item
                    ],
                    risk=[
                        str(payload.get("constraints") or value.get("constraints"))
                    ]
                    if payload.get("constraints") or value.get("constraints")
                    else [],
                    information_status=OpportunityInformationStatus.SOFT_REFERENCE,
                    status=OpportunityStatus.TRACKABLE,
                    evidence=evidence,
                )
            )
    return items


__all__ = [
    "ResourceGateAssessment",
    "evaluate_resource_gate",
    "opportunity_items_from_world_state",
    "project_opportunity_surface",
]
