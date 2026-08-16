"""Compile prose-task creative output into the internal DraftOutput contract.

The executor submits only prose and semantic state declarations.  Evidence,
soft audits and trace material are derived here so a model cannot manufacture
the system's own score or provenance inputs.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from statistics import median
from typing import Any

from novel_authoring.contracts.draft import (
    ChapterRealizationBrief,
    DraftCreativeOutput,
    DraftOutput,
    DraftStateChange,
    RealizedKernelEvidence,
    RealizedKernelTrace,
)
from novel_authoring.planning.models import (
    ChapterContract,
    ChapterExperienceSignature,
    PlanningReferenceProvenance,
    ProgressionImpact,
)

_PUNCTUATION = str.maketrans(
    {
        "，": ",",
        "。": ".",
        "！": "!",
        "？": "?",
        "：": ":",
        "；": ";",
        "（": "(",
        "）": ")",
        "【": "[",
        "】": "]",
        "［": "[",
        "］": "]",
        "｛": "{",
        "｝": "}",
        "、": ",",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "「": '"',
        "」": '"',
        "『": '"',
        "』": '"',
    }
)


def normalize_evidence(value: str) -> str:
    """Normalize the supported Chinese punctuation/whitespace variants."""

    normalized = unicodedata.normalize("NFKC", value).translate(_PUNCTUATION)
    return re.sub(r"\s+", " ", normalized).strip()


def _evidence_present(prose: str, candidate: str) -> bool:
    if not candidate or len(candidate.strip()) < 2:
        return False
    if candidate in prose:
        return True
    normalized = normalize_evidence(candidate)
    return bool(normalized and normalized in normalize_evidence(prose))


def _string_leaves(value: object) -> Iterable[str]:
    if isinstance(value, str):
        if len(value.strip()) >= 2:
            yield value.strip()
        return
    if isinstance(value, Mapping):
        for nested in value.values():
            yield from _string_leaves(nested)
        return
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for nested in value:
            yield from _string_leaves(nested)


_NON_EVIDENCE_PAYLOAD_KEYS = frozenset(
    {
        "id",
        "ids",
        "record_id",
        "fact_id",
        "resource_id",
        "character_id",
        "thread_id",
        "source",
        "source_id",
        "source_ids",
        "causal_source",
        "causal_sources",
        "kind",
        "status",
        "type",
    }
)


def _meaningful_payload_strings(value: object, *, key: str = "") -> Iterable[str]:
    """Yield human-observable payload text, excluding machine locators."""

    normalized_key = key.casefold().replace("-", "_")
    if isinstance(value, str):
        candidate = value.strip()
        if (
            len(candidate) >= 2
            and normalized_key not in _NON_EVIDENCE_PAYLOAD_KEYS
            and not normalized_key.endswith("_id")
            and not (
                re.fullmatch(r"[A-Za-z0-9._:-]+", candidate)
                and (
                    candidate.isdigit()
                    or any(marker in candidate for marker in (".", ":", "_", "-"))
                )
            )
        ):
            yield candidate
        return
    if isinstance(value, Mapping):
        for nested_key, nested in value.items():
            yield from _meaningful_payload_strings(
                nested, key=str(nested_key)
            )
        return
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for nested in value:
            yield from _meaningful_payload_strings(nested, key=key)


def _semantic_tokens(value: str) -> set[str]:
    """Build small deterministic concept tokens for paragraph location."""

    tokens: set[str] = set()
    for run in re.findall(r"[\u4e00-\u9fff]+|[A-Za-z0-9_]+", normalize_evidence(value)):
        if re.fullmatch(r"[\u4e00-\u9fff]+", run):
            tokens.update(run[index : index + 2] for index in range(len(run) - 1))
        else:
            tokens.add(run.casefold())
    return {token for token in tokens if len(token) >= 2}


def _paragraphs(prose: str) -> list[str]:
    paragraphs = [
        item.strip()
        for item in re.split(r"\r?\n\s*(?:\r?\n)?", prose)
        if item.strip()
    ]
    return paragraphs or ([prose.strip()] if prose.strip() else [])


def _semantic_paragraph_quote(prose: str, payload: Mapping[str, Any]) -> str | None:
    """Locate one prose paragraph that realizes the declared payload.

    This is deliberately a bounded locator, not a second semantic validator:
    it requires at least two shared concept tokens and returns the actual
    paragraph so the normal evidence matcher remains authoritative.
    """

    values = list(dict.fromkeys(_meaningful_payload_strings(payload)))
    if not values:
        return None
    value_tokens = set().union(*(_semantic_tokens(value) for value in values))
    if len(value_tokens) < 2:
        return None
    best: tuple[int, str] | None = None
    for paragraph in _paragraphs(prose):
        overlap = len(value_tokens & _semantic_tokens(paragraph))
        if overlap < 2:
            continue
        candidate = (overlap, paragraph)
        if best is None or candidate[0] > best[0]:
            best = candidate
    return None if best is None else best[1]


def _state_change_quotes(prose: str, payload: Mapping[str, Any]) -> list[str]:
    exact = _matched_quotes(prose, _meaningful_payload_strings(payload))
    if exact:
        return exact
    semantic = _semantic_paragraph_quote(prose, payload)
    return [] if semantic is None else [semantic]


def _matched_quotes(prose: str, values: Iterable[str], *, limit: int = 4) -> list[str]:
    seen: set[str] = set()
    matches: list[str] = []
    # Longer phrases are more useful evidence than isolated labels.
    for candidate in sorted(values, key=lambda item: (-len(item), item)):
        if candidate in seen or not _evidence_present(prose, candidate):
            continue
        seen.add(candidate)
        matches.append(candidate)
        if len(matches) >= limit:
            break
    return matches


def _contract_evidence(prose: str, contract: ChapterContract | None) -> dict[str, list[str]]:
    if contract is None:
        return {}
    requirements: dict[str, str] = {
        "required_irreversible_change": contract.required_irreversible_change,
        "ending_state": contract.ending_state,
    }
    if contract.required_cost.strip():
        requirements["required_cost"] = contract.required_cost
    requirements.update(
        {f"commit:{item}": item for item in contract.commit_updates if item.strip()}
    )
    return {
        key: _matched_quotes(prose, [value]) if value.strip() else []
        for key, value in requirements.items()
    }


def _soft_character_audit(
    prose: str, contract: ChapterContract | None
) -> dict[str, float]:
    keys = (
        "motivation_alignment",
        "knowledge_alignment",
        "capability_alignment",
        "relationship_alignment",
        "emotional_continuity",
    )
    if contract is None:
        return {}
    anchors = [
        contract.primary_thread,
        contract.reader_question,
        contract.required_irreversible_change,
        contract.ending_state,
    ]
    anchor_hits = sum(bool(item.strip()) and _evidence_present(prose, item) for item in anchors)
    base = min(100.0, 70.0 + 7.5 * anchor_hits)
    return {key: base for key in keys}


def _soft_style_audit(prose: str) -> dict[str, float]:
    if not prose.strip():
        return {}
    sentence_count = max(1, len(re.findall(r"[。！？!?]", prose)))
    paragraph_count = max(1, len([item for item in prose.splitlines() if item.strip()]))
    has_dialogue = any(mark in prose for mark in ('“', '”', '「', '」', '"'))
    return {
        "pov_and_tense": 75.0,
        "diction_register": 75.0,
        "sentence_rhythm": min(100.0, 60.0 + min(sentence_count, 8) * 5.0),
        "dialogue_voice": 80.0 if has_dialogue else 68.0,
        "exposition_density": min(100.0, 70.0 + min(paragraph_count, 6) * 3.0),
        "emotional_distance": 75.0,
    }


def _experience_signature(
    prose: str,
    state_changes: Sequence[DraftStateChange],
    contract: ChapterContract | None,
    promises_advanced: list[str],
    promises_paid: list[str],
) -> ChapterExperienceSignature | None:
    if contract is None:
        return None
    signature_fields = (
        "event_source",
        "solution_method",
        "protagonist_strategy",
        "risk_form",
        "emotional_outcome",
        "social_feedback",
        "scene_topology",
        "ending_mode",
        "outcome_magnitude",
        "action_space_delta",
        "knowledge_delta",
        "relationship_delta",
        "world_scale_delta",
        "core_promise_delivery",
    )
    values = {field: "" for field in signature_fields}
    for change in state_changes:
        for field in signature_fields:
            declared = change.payload.get(field)
            if declared not in (None, "") and not values[field]:
                values[field] = str(declared).strip()
    if not values["event_source"]:
        values["event_source"] = ";".join(
            dict.fromkeys(change.kind for change in state_changes)
        )
    if not values["scene_topology"]:
        values["scene_topology"] = (
            "DIALOGUE"
            if any(mark in prose for mark in ("“", "”", "「", "」", '"'))
            else "ACTION"
        )
    if not values["ending_mode"]:
        last_paragraph = _paragraphs(prose)[-1] if _paragraphs(prose) else ""
        values["ending_mode"] = (
            "DIALOGUE"
            if any(mark in last_paragraph for mark in ("“", "”", "「", "」", '"'))
            else "CONSEQUENCE"
        )
    if not values["core_promise_delivery"]:
        values["core_promise_delivery"] = ";".join(
            promises_paid if promises_paid else promises_advanced
        )
    return ChapterExperienceSignature.model_validate(values)


def _trace(
    prose: str,
    changes: Sequence[DraftStateChange],
    contract: ChapterContract | None,
    promises_advanced: list[str],
    promises_paid: list[str],
) -> RealizedKernelTrace | None:
    if contract is None:
        return None
    evidence = [
        RealizedKernelEvidence(
            claim=f"{change.kind}:{change.record_id}",
            state_change_record_ids=[change.record_id],
            evidence_quotes=list(change.evidence_quotes),
        )
        for change in changes
        if change.evidence_quotes
    ]
    resource_changes = [
        change.record_id for change in changes if change.kind == "resource"
    ]
    world_expansion = [
        change.record_id
        for change in changes
        if isinstance(change.payload.get("world_expansion"), dict)
    ]
    return RealizedKernelTrace(
        expected_contract_id=contract.contract_id,
        primary_intent=contract.chapter_intent,
        reader_promises_served=list(dict.fromkeys([*promises_advanced, *promises_paid])),
        progression_impact=ProgressionImpact(
            axis_advanced=[
                change.record_id
                for change in changes
                if change.kind in {"capability", "knowledge", "relationship"}
            ],
            resource_change=list(resource_changes),
        ),
        resource_changes=list(resource_changes),
        world_expansion_changes=list(world_expansion),
        payoff_channels_realized=list(dict.fromkeys(promises_paid)),
        debts_advanced=list(dict.fromkeys(promises_advanced)),
        debts_paid=list(dict.fromkeys(promises_paid)),
        evidence=evidence,
    )


def build_chapter_realization_brief(
    contract: ChapterContract,
    *,
    recent_lengths: Sequence[int] = (),
) -> ChapterRealizationBrief:
    """Build an adaptive, advisory realization range from available context."""

    clean_lengths = [int(value) for value in recent_lengths if int(value) > 0]
    anchor = int(median(clean_lengths)) if clean_lengths else 0
    # A no-history chapter still needs useful expression guidance.  This is a
    # soft character-range hint only; diagnose_scene_realization never turns it
    # into a hard validation gate.
    target_range = (
        (1800, 3200)
        if anchor <= 0
        else (max(1, int(anchor * 0.65)), int(anchor * 1.45))
    )
    targets = list(contract.dramatization_targets)
    if not targets:
        targets = [
            item
            for item in (contract.required_irreversible_change, contract.ending_state)
            if item.strip()
        ]
    return ChapterRealizationBrief(
        target_word_range=target_range,
        target_scene_count=max(1, min(5, 1 + len(contract.secondary_functions))),
        dramatization_targets=targets,
        realization_scope=contract.realization_scope,
    )


def diagnose_scene_realization(
    prose: str, brief: ChapterRealizationBrief
) -> dict[str, Any]:
    """Return an advisory thin-scene finding without creating a hard gate."""

    lower, upper = brief.target_word_range
    paragraphs = [item for item in prose.splitlines() if item.strip()]
    sentences = len(re.findall(r"[。！？!?]", prose))
    too_thin = bool(lower and len(prose.strip()) < lower)
    too_summary_like = len(paragraphs) < brief.target_scene_count and sentences < 3
    if not (too_thin or too_summary_like):
        return {
            "code": "SCENE_REALIZATION_CLEAR",
            "severity": "INFO",
            "status": "CLEAR",
            "character_count": len(prose.strip()),
            "target_word_range": [lower, upper],
        }
    reasons = []
    if too_thin:
        reasons.append("正文低于自适应软范围")
    if too_summary_like:
        reasons.append("场面动作、反应或后果展开不足")
    return {
        "code": "SCENE_REALIZATION_THIN",
        "severity": "WARNING",
        "status": "REVIEW",
        "character_count": len(prose.strip()),
        "target_word_range": [lower, upper],
        "reasons": reasons,
        "suggested_fix": "只补充动作、感官、人物反应或场面后果；不得新增 Contract 外的状态变化。",
    }


def compile_draft_output(
    creative_output: DraftCreativeOutput,
    contract: ChapterContract | None = None,
    *,
    realization_brief: ChapterRealizationBrief | None = None,
) -> DraftOutput:
    """Compile executor prose into the internal, validator-facing output."""

    prose = creative_output.prose_markdown
    changes = [
        DraftStateChange(
            kind=item.kind,
            record_id=item.record_id,
            payload=dict(item.payload),
            evidence_quotes=_state_change_quotes(prose, item.payload),
        )
        for item in creative_output.state_changes
    ]
    promises_advanced = list(dict.fromkeys(creative_output.promises_advanced))
    promises_paid = list(dict.fromkeys(creative_output.promises_paid))
    if contract is not None:
        contract_advance = contract.narrative_debt.get("advance", [])
        contract_paid = contract.narrative_debt.get("fully_pay", [])
        if isinstance(contract_advance, list):
            promises_advanced = list(
                dict.fromkeys([*promises_advanced, *map(str, contract_advance)])
            )
        if isinstance(contract_paid, list):
            promises_paid = list(
                dict.fromkeys([*promises_paid, *map(str, contract_paid)])
            )
    brief = realization_brief or (
        build_chapter_realization_brief(contract) if contract is not None else None
    )
    diagnostics = (
        diagnose_scene_realization(prose, brief)
        if brief is not None
        else {"code": "SCENE_REALIZATION_UNSCOPED", "severity": "INFO", "status": "UNKNOWN"}
    )
    notes = list(creative_output.notes)
    if diagnostics.get("code") == "SCENE_REALIZATION_THIN":
        notes.append("SCENE_REALIZATION_THIN：仅提示表达层复核，不阻止 VALIDATED_DRAFT。")
    reference = (
        contract.reference_provenance
        if contract is not None
        else PlanningReferenceProvenance()
    )
    return DraftOutput(
        task_id=creative_output.task_id,
        contract_id=creative_output.contract_id,
        chapter_title=creative_output.chapter_title,
        prose_markdown=prose,
        state_changes=changes,
        contract_evidence=_contract_evidence(prose, contract),
        knowledge_claims=list(creative_output.knowledge_claims),
        reveal_trace=creative_output.reveal_trace,
        character_fit_inputs=_soft_character_audit(prose, contract),
        style_fit_inputs=_soft_style_audit(prose),
        promises_advanced=promises_advanced,
        promises_paid=promises_paid,
        new_major_hooks=creative_output.new_major_hooks,
        structure_tags=(
            []
            if contract is None
            else [
                f"function:{contract.primary_function.value}",
                *[f"secondary:{item.value}" for item in contract.secondary_functions],
            ]
        ),
        innovation_control=None if contract is None else contract.innovation_control,
        realized_kernel_trace=_trace(
            prose, changes, contract, promises_advanced, promises_paid
        ),
        chapter_experience_signature=_experience_signature(
            prose, changes, contract, promises_advanced, promises_paid
        ),
        realization_diagnostics=diagnostics,
        reference_provenance=reference,
        evidence_policy="COMPILED_SOFT",
        notes=notes,
    )


__all__ = [
    "build_chapter_realization_brief",
    "compile_draft_output",
    "diagnose_scene_realization",
    "normalize_evidence",
]
