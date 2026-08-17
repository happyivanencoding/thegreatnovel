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
from typing import Any, Literal

from novel_authoring.continuation_quality import (
    ProgressionDelta,
    ReaderClaimStatus,
    ReaderVisibleClaim,
)
from novel_authoring.contracts.draft import (
    ChapterRealizationBrief,
    DraftCreativeOutput,
    DraftOutput,
    DraftStateChange,
    RealizedKernelEvidence,
    RealizedKernelTrace,
    SemanticPublicationReview,
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


def _commit_matches_change(change: DraftStateChange, commit_update: str) -> bool:
    prefix, separator, target = commit_update.partition(":")
    if not separator or not target.strip():
        return False
    descriptive_kind = {
        "thread status advances": "thread",
        "character state changes": "character_state",
        "social status changes": None,
        "world/social state changes": None,
    }.get(prefix.strip().casefold())
    if prefix.strip().casefold() in {
        "thread status advances",
        "character state changes",
        "social status changes",
        "world/social state changes",
    }:
        if descriptive_kind is not None and change.kind != descriptive_kind:
            return False
        return any(target.strip() in quote for quote in change.evidence_quotes)
    expected_kind = {
        "thread_status": "thread",
        "character_state": "character_state",
        "resource": "resource",
        "capability": "capability",
        "knowledge": "knowledge",
        "relationship": "relationship",
    }.get(prefix.strip().casefold(), prefix.strip().casefold())
    if change.kind != expected_kind:
        return False
    identifiers = {
        str(change.record_id),
        str(change.payload.get("id") or ""),
        str(change.payload.get("record_id") or ""),
        str(change.payload.get("thread_id") or ""),
        str(change.payload.get("character_id") or ""),
        str(change.payload.get("resource_id") or ""),
        str(change.payload.get("capability_id") or ""),
        str(change.payload.get("relationship_id") or ""),
        str(change.payload.get("knowledge_id") or ""),
    }
    return target.strip() in identifiers


def _contract_evidence(
    prose: str,
    contract: ChapterContract | None,
    changes: Sequence[DraftStateChange] = (),
) -> dict[str, list[str]]:
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
    evidence: dict[str, list[str]] = {}
    for key, value in requirements.items():
        matches = _matched_quotes(prose, [value]) if value.strip() else []
        if key.startswith("commit:") and not matches:
            for change in changes:
                if not _commit_matches_change(change, key.removeprefix("commit:")):
                    continue
                matches.extend(change.evidence_quotes)
            matches = list(dict.fromkeys(matches))
        evidence[key] = matches
    return evidence


def _deterministic_measurements(prose: str) -> dict[str, Any]:
    """Return observable form measurements, never a literary quality score."""

    paragraphs = _paragraphs(prose)
    sentences = len(re.findall(r"[。！？!?]", prose))
    dialogue_chars = sum(prose.count(mark) for mark in ('“', '”', '「', '」', '"'))
    return {
        "character_count": len(prose.strip()),
        "paragraph_count": len(paragraphs),
        "sentence_count": sentences,
        "dialogue_marker_count": dialogue_chars,
        "dialogue_marker_ratio": round(dialogue_chars / max(1, len(prose.strip())), 4),
        "average_sentence_character_count": round(
            len(prose.strip()) / max(1, sentences), 2
        ),
    }


def _contract_surface_coverage(
    contract: ChapterContract | None, evidence: Mapping[str, list[str]]
) -> dict[str, Any]:
    if contract is None:
        return {"required": [], "observed": [], "missing": [], "status": "UNSCOPED"}
    required = [
        key
        for key, value in {
            "required_irreversible_change": contract.required_irreversible_change,
            "ending_state": contract.ending_state,
            "required_cost": contract.required_cost,
            **{f"commit:{item}": item for item in contract.commit_updates},
        }.items()
        if str(value or "").strip()
    ]
    observed = [key for key in required if evidence.get(key)]
    missing = [key for key in required if key not in observed]
    return {
        "required": required,
        "observed": observed,
        "missing": missing,
        "observed_count": len(observed),
        "required_count": len(required),
        "status": "COMPLETE" if not missing else "PARTIAL",
    }


def _compile_reader_visible_claims(
    prose: str, claims: Sequence[ReaderVisibleClaim]
) -> list[ReaderVisibleClaim]:
    compiled: list[ReaderVisibleClaim] = []
    for claim in claims:
        quote = claim.evidence_quote.strip()
        if not quote:
            candidates = [claim.predicate]
            for value in (claim.value, claim.after_value):
                if value not in (None, ""):
                    candidates.append(str(value))
            quote = next(
                (item for item in candidates if _evidence_present(prose, item)),
                "",
            )
        status = (
            ReaderClaimStatus.OBSERVED
            if quote and _evidence_present(prose, quote)
            else ReaderClaimStatus.UNOBSERVED
        )
        compiled.append(
            claim.model_copy(update={"evidence_quote": quote, "status": status})
        )
    return compiled


def _claim_identity(claim: ReaderVisibleClaim) -> tuple[str, str, str]:
    return (
        claim.subject_ref.strip().casefold(),
        claim.predicate.strip().casefold(),
        claim.temporal_scope.strip().casefold(),
    )


def _claim_value_signature(claim: ReaderVisibleClaim) -> tuple[str, str, str]:
    return (
        repr(claim.value),
        repr(claim.before_value),
        repr(claim.after_value),
    )


def _merge_reader_visible_claims(
    creative_claims: Sequence[ReaderVisibleClaim],
    review_claims: Sequence[ReaderVisibleClaim],
) -> list[ReaderVisibleClaim]:
    """Merge an independent review while retaining disagreements for validation."""

    merged = list(creative_claims)
    by_identity: dict[tuple[str, str, str], int] = {
        _claim_identity(claim): index for index, claim in enumerate(merged)
    }
    for review_claim in review_claims:
        identity = _claim_identity(review_claim)
        existing_index = by_identity.get(identity)
        if existing_index is None:
            by_identity[identity] = len(merged)
            merged.append(review_claim)
            continue
        existing = merged[existing_index]
        if _claim_value_signature(existing) != _claim_value_signature(review_claim):
            merged.append(review_claim.model_copy(update={"status": ReaderClaimStatus.CONFLICT}))
            continue
        updates: dict[str, Any] = {}
        if not existing.evidence_quote and review_claim.evidence_quote:
            updates["evidence_quote"] = review_claim.evidence_quote
        if not existing.transition_source and review_claim.transition_source:
            updates["transition_source"] = review_claim.transition_source
        if (
            existing.status is not ReaderClaimStatus.OBSERVED
            and review_claim.status is ReaderClaimStatus.OBSERVED
        ):
            updates["status"] = ReaderClaimStatus.OBSERVED
        if updates:
            merged[existing_index] = existing.model_copy(update=updates)
    return merged


def _progression_deltas(
    creative_deltas: Sequence[ProgressionDelta], changes: Sequence[DraftStateChange]
) -> list[ProgressionDelta]:
    values: list[ProgressionDelta] = list(creative_deltas)
    for change in changes:
        progression = change.payload.get("progression")
        if not isinstance(progression, Mapping):
            continue
        raw = progression.get("deltas", [])
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
            continue
        for item in raw:
            try:
                values.append(ProgressionDelta.model_validate(item))
            except (TypeError, ValueError):
                continue
    seen: set[str] = set()
    result: list[ProgressionDelta] = []
    for item in values:
        if item.delta_id in seen:
            continue
        seen.add(item.delta_id)
        result.append(item)
    return result


def _experience_signature(
    prose: str,
    state_changes: Sequence[DraftStateChange],
    contract: ChapterContract | None,
    promises_advanced: list[str],
    promises_paid: list[str],
    progression_deltas: Sequence[ProgressionDelta] = (),
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
        "opposition_source",
        "primary_subject",
        "choice_type",
        "cost_type",
        "payoff_channel",
        "reader_visible_delta",
        "progression_delta_type",
        "ending_action",
    )
    values: dict[str, Any] = {field: "" for field in signature_fields}
    values["chapter_ordinal"] = contract.chapter
    target_values = contract.experience_target.model_dump(mode="json")
    for change in state_changes:
        for field in signature_fields:
            declared = change.payload.get(field)
            if declared not in (None, ""):
                values[field] = str(declared).strip()
        progression = change.payload.get("progression")
        if isinstance(progression, Mapping):
            for field in signature_fields:
                declared = progression.get(field)
                if declared not in (None, ""):
                    values[field] = str(declared).strip()
    for field in signature_fields:
        if not values[field]:
            declared = target_values.get(field)
            if declared not in (None, ""):
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
    if not values["progression_delta_type"] and progression_deltas:
        values["progression_delta_type"] = ";".join(
            dict.fromkeys(item.kind.value for item in progression_deltas)
        )
    if not values["reader_visible_delta"] and progression_deltas:
        values["reader_visible_delta"] = ";".join(
            dict.fromkeys(
                item.reader_visible_delta
                for item in progression_deltas
                if item.reader_visible_delta
            )
        )
    return ChapterExperienceSignature.model_validate(values)


def _trace(
    prose: str,
    changes: Sequence[DraftStateChange],
    contract: ChapterContract | None,
    promises_advanced: list[str],
    promises_paid: list[str],
    progression_deltas: Sequence[ProgressionDelta] = (),
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
            deltas=list(progression_deltas),
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
    # Without a healthy history there is no defensible global word-count
    # baseline; the brief remains scoped to the Contract's observable targets.
    target_range = (
        (0, 0)
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
    contract_status: Literal["SUFFICIENT", "UNDERSPECIFIED"] = (
        "SUFFICIENT"
        if contract.required_irreversible_change.strip()
        and contract.ending_state.strip()
        and contract.commit_updates
        else "UNDERSPECIFIED"
    )
    return ChapterRealizationBrief(
        target_word_range=target_range,
        target_scene_count=max(1, 1 + len(contract.secondary_functions)),
        dramatization_targets=targets,
        realization_scope=contract.realization_scope,
        contract_realization_status=contract_status,
        adaptive=anchor > 0,
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
    if brief.contract_realization_status == "UNDERSPECIFIED":
        return {
            "code": "CONTRACT_REALIZATION_UNDERSPECIFIED",
            "severity": "ERROR",
            "status": "RETURN_TO_PLANNING",
            "character_count": len(prose.strip()),
            "target_word_range": [lower, upper],
            "baseline_status": "HEALTHY_HISTORY" if lower else "UNKNOWN",
            "suggested_fix": (
                "返回 Planning/Contract，补齐独立章节的变化、结果、反应或代价；"
                "不要只堆描写。"
            ),
        }
    if not (too_thin or too_summary_like):
        return {
            "code": "SCENE_REALIZATION_CLEAR",
            "severity": "INFO",
            "status": "CLEAR",
            "character_count": len(prose.strip()),
            "target_word_range": [lower, upper],
            "baseline_status": "HEALTHY_HISTORY" if lower else "UNKNOWN",
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
        "baseline_status": "HEALTHY_HISTORY" if lower else "UNKNOWN",
        "reasons": reasons,
        "suggested_fix": "只补充动作、感官、人物反应或场面后果；不得新增 Contract 外的状态变化。",
    }


def compile_draft_output(
    creative_output: DraftCreativeOutput,
    contract: ChapterContract | None = None,
    *,
    realization_brief: ChapterRealizationBrief | None = None,
    publication_review: SemanticPublicationReview | None = None,
    semantic_review_required: bool = False,
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
    reader_visible_claims = _compile_reader_visible_claims(
        prose, creative_output.reader_visible_claims
    )
    publication_review_claims = (
        _compile_reader_visible_claims(prose, publication_review.reader_visible_claims)
        if publication_review is not None
        else []
    )
    merged_reader_visible_claims = _merge_reader_visible_claims(
        reader_visible_claims,
        publication_review_claims,
    )
    progression_deltas = _progression_deltas(
        creative_output.progression_deltas, changes
    )
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
    measurements = _deterministic_measurements(prose)
    contract_evidence = _contract_evidence(prose, contract, changes)
    coverage = _contract_surface_coverage(contract, contract_evidence)
    notes = list(creative_output.notes)
    if diagnostics.get("code") == "SCENE_REALIZATION_THIN":
        notes.append("SCENE_REALIZATION_THIN：仅提示表达层复核，不阻止 VALIDATED_DRAFT。")
    elif diagnostics.get("code") == "CONTRACT_REALIZATION_UNDERSPECIFIED":
        notes.append(
            "CONTRACT_REALIZATION_UNDERSPECIFIED：应返回 Planning/Contract，"
            "不以补字数代替章节设计。"
        )
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
        contract_evidence=contract_evidence,
        knowledge_claims=list(creative_output.knowledge_claims),
        reveal_trace=creative_output.reveal_trace,
        character_fit_inputs={},
        style_fit_inputs={},
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
            prose,
            changes,
            contract,
            promises_advanced,
            promises_paid,
            progression_deltas,
        ),
        chapter_experience_signature=_experience_signature(
            prose,
            changes,
            contract,
            promises_advanced,
            promises_paid,
            progression_deltas,
        ),
        realization_diagnostics=diagnostics,
        reference_provenance=reference,
        evidence_policy="COMPILED_SOFT",
        semantic_review_required=semantic_review_required,
        reader_visible_claims=merged_reader_visible_claims,
        publication_review_claims=publication_review_claims,
        progression_deltas=progression_deltas,
        semantic_review_status=(
            "UNKNOWN" if publication_review is None else publication_review.status
        ),
        deterministic_measurements=measurements,
        contract_surface_coverage=coverage,
        publication_review_findings=(
            [
                item.model_dump(mode="json")
                for item in publication_review.publication_review_findings
            ]
            if publication_review is not None
            else []
        ),
        notes=notes,
    )


__all__ = [
    "build_chapter_realization_brief",
    "compile_draft_output",
    "diagnose_scene_realization",
    "normalize_evidence",
]
