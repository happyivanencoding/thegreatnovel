from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from novel_authoring.canon.materialize import missing_materialization_fields
from novel_authoring.canon.projection import CanonProjection
from novel_authoring.config import Settings
from novel_authoring.continuation_quality import (
    ProgressionDelta,
    QualityIssue,
    UsageConstraint,
    progression_delta_issues,
    usage_constraint_issues,
)
from novel_authoring.contracts.draft import (
    DraftOutput,
    DraftStateChange,
    RealizedKernelEvidence,
    RealizedKernelTrace,
)
from novel_authoring.domain.models import ContinuationMode, NarrativeFunction, Severity
from novel_authoring.metrics.formulas import (
    character_fit,
    payoff_cooldown_allowed,
    style_fit,
)
from novel_authoring.planning.models import ChapterContract, ProgressionImpact
from novel_authoring.validation.aliases import resolve_projection_alias
from novel_authoring.validation.models import (
    ValidationFinding,
    ValidationReport,
    ValidatorName,
)
from novel_authoring.validation.publication_boundary import (
    edge_publication_findings,
    internal_workflow_language_hits,
)


@dataclass(frozen=True)
class ValidationContext:
    draft: DraftOutput
    contract: ChapterContract
    projection: CanonProjection
    settings: Settings


def _finding(
    code: str,
    message: str,
    *,
    severity: Severity = Severity.ERROR,
    evidence: list[str] | None = None,
    location: str | None = None,
    suggested_fix: str | None = None,
) -> ValidationFinding:
    return ValidationFinding(
        code=code,
        severity=severity,
        message=message,
        evidence=evidence or [],
        location=location,
        suggested_fix=suggested_fix,
    )


_SEVERITY_RANK = {
    Severity.INFO: 0,
    Severity.WARNING: 1,
    Severity.ERROR: 2,
    Severity.FATAL: 3,
}


EvidenceMatchStatus = Literal["EXACT", "NORMALIZED", "AMBIGUOUS", "NOT_FOUND"]

_EVIDENCE_PUNCTUATION = str.maketrans(
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


def _normalize_evidence(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).translate(
        _EVIDENCE_PUNCTUATION
    )
    return re.sub(r"\s+", " ", normalized).strip()


def _match_evidence(prose: str, quote: str) -> EvidenceMatchStatus:
    if not isinstance(quote, str) or not quote.strip():
        return "NOT_FOUND"
    if quote in prose:
        return "EXACT"
    normalized_quote = _normalize_evidence(quote)
    if not normalized_quote:
        return "NOT_FOUND"
    normalized_prose = _normalize_evidence(prose)
    first = normalized_prose.find(normalized_quote)
    if first < 0:
        return "NOT_FOUND"
    second = normalized_prose.find(normalized_quote, first + 1)
    return "AMBIGUOUS" if second >= 0 else "NORMALIZED"


def _report(
    validator: ValidatorName,
    findings: list[ValidationFinding],
    measurements: dict[str, Any] | None = None,
) -> ValidationReport:
    blocking = any(
        finding.severity in {Severity.ERROR, Severity.FATAL} for finding in findings
    )
    severity = max(
        (finding.severity for finding in findings),
        key=lambda item: _SEVERITY_RANK[item],
        default=Severity.INFO,
    )
    return ValidationReport(
        validator=validator,
        passed=not blocking,
        severity=severity,
        findings=findings,
        measurements=measurements or {},
    )


def _changes(context: ValidationContext, kind: str) -> list[DraftStateChange]:
    return [change for change in context.draft.state_changes if change.kind == kind]


def _clean_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if not key.startswith("_")}


def _projection_value(
    projection: CanonProjection, subject_ref: str, predicate: str
) -> tuple[bool, Any]:
    """Resolve only direct projection fields; do not infer natural-language facts."""

    collections = (
        projection.facts,
        projection.entities,
        projection.character_states,
        projection.knowledge,
        projection.relationships,
        projection.resources,
        projection.capabilities,
        projection.threads,
        projection.promises,
    )
    for collection in collections:
        item = collection.get(subject_ref)
        if isinstance(item, dict) and predicate in item:
            return True, item[predicate]
        for key, candidate in collection.items():
            if not isinstance(candidate, dict):
                continue
            identifiers = {
                str(key),
                str(candidate.get("id") or ""),
                str(candidate.get("record_id") or ""),
                str(candidate.get("resource_id") or ""),
                str(candidate.get("capability_id") or ""),
                str(candidate.get("character_id") or ""),
                str(candidate.get("entity_id") or ""),
                str(candidate.get("relationship_id") or ""),
                str(candidate.get("name") or ""),
            }
            if subject_ref in identifiers and predicate in candidate:
                return True, candidate[predicate]
    return False, None


def _projection_subject_exists(projection: CanonProjection, subject_ref: str) -> bool:
    collections = (
        projection.facts,
        projection.entities,
        projection.character_states,
        projection.knowledge,
        projection.relationships,
        projection.resources,
        projection.capabilities,
        projection.threads,
        projection.promises,
    )
    for collection in collections:
        if subject_ref in collection:
            return True
        for key, candidate in collection.items():
            if not isinstance(candidate, dict):
                continue
            identifiers = {
                str(key),
                str(candidate.get("id") or ""),
                str(candidate.get("record_id") or ""),
                str(candidate.get("resource_id") or ""),
                str(candidate.get("capability_id") or ""),
                str(candidate.get("character_id") or ""),
                str(candidate.get("entity_id") or ""),
                str(candidate.get("relationship_id") or ""),
                str(candidate.get("name") or ""),
            }
            if subject_ref in identifiers:
                return True
    return False


def _reader_visible_claim_findings(context: ValidationContext) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    state_changes = {
        change.record_id: change for change in context.draft.state_changes
    }
    for claim in context.draft.reader_visible_claims:
        location = f"reader_visible_claims:{claim.claim_id}"
        evidence_status = _match_evidence(
            context.draft.prose_markdown, claim.evidence_quote
        )
        if not claim.evidence_quote or evidence_status == "NOT_FOUND":
            findings.append(
                _finding(
                    "READER_VISIBLE_CLAIM_NOT_OBSERVED",
                    f"读者可见声明 {claim.claim_id} 没有正文证据。",
                    location=location,
                    suggested_fix="补充正文中可直接观察到的 evidence_quote，或删除该声明。",
                )
            )
        elif evidence_status == "AMBIGUOUS":
            findings.append(
                _finding(
                    "READER_VISIBLE_CLAIM_EVIDENCE_AMBIGUOUS",
                    f"读者可见声明 {claim.claim_id} 的 evidence_quote 在正文中出现多次。",
                    severity=Severity.WARNING,
                    location=location,
                )
            )
        transition = state_changes.get(claim.transition_source)
        has_transition = transition is not None
        transition_payload = transition.payload if transition is not None else {}
        if (
            not _projection_subject_exists(context.projection, claim.subject_ref)
            and not has_transition
        ):
            findings.append(
                _finding(
                    "READER_VISIBLE_CLAIM_SUBJECT_NOT_FOUND",
                    f"声明 {claim.claim_id} 引用了 Projection 中不存在的实体/主体。",
                    location=location,
                )
            )
        contract_record_ids = set(
            getattr(context.contract, "state_change_record_ids", []) or []
        )
        if (
            has_transition
            and contract_record_ids
            and claim.transition_source not in contract_record_ids
        ):
            findings.append(
                _finding(
                    "READER_VISIBLE_CLAIM_OUTSIDE_CONTRACT",
                    f"声明 {claim.claim_id} 绑定的 StateChange 不在当前 Chapter Contract。",
                    location=location,
                )
            )
        if claim.before_value is not None and claim.after_value is not None:
            if not claim.transition_source or not has_transition:
                unbound_code = {
                    "LOCATION": "LOCATION_CHANGE_WITHOUT_TRANSITION",
                    "OWNERSHIP": "OWNERSHIP_CHANGE_WITHOUT_EVENT",
                    "TEMPORAL": "TEMPORAL_RESET_WITHOUT_TRANSITION",
                    "TEMPORAL_STATE": "TEMPORAL_RESET_WITHOUT_TRANSITION",
                }.get(
                    claim.claim_kind.value,
                    "READER_VISIBLE_CLAIM_TRANSITION_UNBOUND",
                )
                findings.append(
                    _finding(
                        unbound_code,
                        f"声明 {claim.claim_id} 有 before/after，但没有绑定本章 StateChange。",
                        location=location,
                    )
                )
            found, current = _projection_value(
                context.projection, claim.subject_ref, claim.predicate
            )
            if found and current != claim.before_value:
                findings.append(
                    _finding(
                        "STATE_CONTRADICTION",
                        (
                            f"声明 {claim.claim_id} 的 before_value={claim.before_value!r} "
                            f"与 Projection 当前值={current!r} 不一致。"
                        ),
                        location=location,
                    )
                )
            elif (
                claim.claim_kind.value == "QUANTITY"
                and claim.before_value != claim.after_value
                and not any(
                    transition_payload.get(key)
                    for key in ("source", "causal_source", "cause", "event_id", "origin")
                )
            ):
                findings.append(
                    _finding(
                        "QUANTITY_JUMP_WITHOUT_SOURCE",
                        f"数量声明 {claim.claim_id} 有变化，但 StateChange 没有来源。",
                        location=location,
                    )
                )
            elif (
                claim.claim_kind.value
                in {"CAPABILITY", "CAPABILITY_STATE", "CAPABILITY_USE"}
                and str(claim.before_value).casefold()
                in {"depleted", "empty", "unavailable", "false", "0"}
                and str(claim.after_value).casefold()
                in {"available", "ready", "true", "1"}
                and not any(
                    transition_payload.get(key)
                    for key in (
                        "usage_reset",
                        "reset_condition_satisfied",
                        "reset_event",
                        "source",
                        "causal_source",
                        "cause",
                    )
                )
            ):
                findings.append(
                    _finding(
                        "CAPABILITY_AVAILABLE_AFTER_DEPLETION",
                        f"能力声明 {claim.claim_id} 从耗尽/不可用恢复，但没有 reset 或来源事件。",
                        location=location,
                    )
                )
        if claim.value is not None and claim.temporal_scope.upper() == "CURRENT":
            found, current = _projection_value(
                context.projection, claim.subject_ref, claim.predicate
            )
            if found and current != claim.value and not has_transition:
                findings.append(
                    _finding(
                        "READER_VISIBLE_CLAIM_NOT_MATERIALIZED",
                        (
                            f"声明 {claim.claim_id} 报告当前值 {claim.value!r}，"
                            "但 Projection 当前值为 "
                            f"{current!r}，且没有绑定 StateChange。"
                        ),
                        location=location,
                    )
                )
    return findings


def _publication_boundary_findings(context: ValidationContext) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    for term in internal_workflow_language_hits(context.draft.prose_markdown):
        findings.append(
            _finding(
                "INTERNAL_WORKFLOW_LANGUAGE_LEAK",
                f"正文包含内部工作流术语：{term}。",
                evidence=[term],
                location="prose_markdown",
                suggested_fix="改写为读者可理解的故事事实，不暴露系统合同、字段或状态名。",
            )
        )
    for index, item in enumerate(
        edge_publication_findings(context.draft.publication_review_findings)
    ):
        quote = item["evidence_quote"]
        if not quote:
            findings.append(
                _finding(
                    "PUBLICATION_REVIEW_EVIDENCE_MISSING",
                    "语义出版审阅提出了问题，但没有正文 evidence_quote。",
                    location=f"publication_review_findings:{index}",
                )
            )
            continue
        match_status = _match_evidence(context.draft.prose_markdown, quote)
        if match_status == "NOT_FOUND":
            findings.append(
                _finding(
                    "PUBLICATION_REVIEW_EVIDENCE_NOT_FOUND",
                    f"语义出版审阅的 evidence_quote 不在正文中：{quote}",
                    location=f"publication_review_findings:{index}",
                    evidence=[quote],
                )
            )
        elif match_status == "AMBIGUOUS":
            findings.append(
                _finding(
                    "PUBLICATION_REVIEW_EVIDENCE_AMBIGUOUS",
                    f"语义出版审阅的 evidence_quote 在正文中出现多次：{quote}",
                    severity=Severity.WARNING,
                    location=f"publication_review_findings:{index}",
                    evidence=[quote],
                )
            )
        else:
            findings.append(
                _finding(
                    "PUBLICATION_SEMANTIC_REVIEW_FINDING",
                    item["reason"] or "边缘语义审阅报告了出版边界问题。",
                    location=f"publication_review_findings:{index}",
                    evidence=[quote],
                )
            )
    return findings


def _quality_findings(issues: list[QualityIssue]) -> list[ValidationFinding]:
    return [
        _finding(
            item.code,
            item.message,
            severity=Severity.ERROR if item.severity == "ERROR" else Severity.WARNING,
            location=item.location,
        )
        for item in issues
    ]


def validate_canon(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = [
        *_reader_visible_claim_findings(context),
        *_publication_boundary_findings(context),
    ]
    for change in context.draft.state_changes:
        missing = missing_materialization_fields(change)
        if missing:
            findings.append(
                _finding(
                    "MATERIALIZATION_REQUIRED_FIELD_MISSING",
                    f"{change.kind} 状态变化缺少物化必填字段: {', '.join(missing)}。",
                    location=f"state_changes:{change.record_id}",
                    suggested_fix="补齐物化契约字段后重新导入并运行十项校验。",
                )
            )
    mode = context.contract.mode
    for change in _changes(context, "fact"):
        payload = _clean_payload(change.payload)
        existing = context.projection.facts.get(change.record_id)
        revision_marker = bool(
            payload.get("supersedes_fact_id") or payload.get("revision_reason")
        )
        if (
            existing is not None
            and _clean_payload(existing) != payload
            and (mode is not ContinuationMode.EXPLICIT_REVISION or not revision_marker)
        ):
            findings.append(
                _finding(
                    "CANON_FACT_OVERWRITE",
                    f"事实 {change.record_id} 与当前正史值不一致。",
                    evidence=[json.dumps(_clean_payload(existing), ensure_ascii=False)],
                    location=f"state_changes:{change.record_id}",
                    suggested_fix="沿用正史值，或切换 explicit_revision 并提供修订来源。",
                )
            )
        subject = payload.get("subject_id")
        predicate = payload.get("predicate")
        if predicate is not None:
            for fact_id, fact in context.projection.facts.items():
                if fact_id == change.record_id:
                    continue
                if fact.get("subject_id") == subject and fact.get("predicate") == predicate:
                    old_object = fact.get("object", fact.get("object_json"))
                    new_object = payload.get("object", payload.get("object_json"))
                    if old_object != new_object and (
                        mode is not ContinuationMode.EXPLICIT_REVISION
                        or not revision_marker
                    ):
                        findings.append(
                            _finding(
                                "CANON_PREDICATE_CONFLICT",
                                f"{subject!s}.{predicate!s} 已有不同正史值（{fact_id}）。",
                                evidence=[json.dumps(old_object, ensure_ascii=False)],
                                location=f"state_changes:{change.record_id}",
                            )
                        )
        if bool(payload.get("retcon")) and mode is not ContinuationMode.EXPLICIT_REVISION:
            findings.append(
                _finding(
                    "SILENT_RETCON",
                    "faithful/constrained 模式禁止把 retcon 静默写入正史。",
                    location=f"state_changes:{change.record_id}",
                )
            )
    return _report("Canon Validator", findings)


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def validate_timeline(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    existing_orders = [
        number
        for item in context.projection.timeline.values()
        if (number := _number(item.get("order_key"))) is not None
    ]
    latest_order = max(existing_orders, default=None)
    for change in _changes(context, "timeline"):
        payload = change.payload
        start = _number(payload.get("story_time_start"))
        end = _number(payload.get("story_time_end"))
        order = _number(payload.get("order_key"))
        if start is not None and end is not None and end < start:
            findings.append(
                _finding(
                    "TIMELINE_REVERSED_RANGE",
                    "story_time_end 早于 story_time_start。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        is_non_linear = bool(payload.get("parallel") or payload.get("flashback"))
        if (
            latest_order is not None
            and order is not None
            and order < latest_order
            and not is_non_linear
        ):
            findings.append(
                _finding(
                    "TIMELINE_ORDER_ROLLBACK",
                    f"order_key={order:g} 早于当前正史 {latest_order:g}，且未声明并行或回忆。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        after_id = payload.get("sequence_after")
        if after_id and str(after_id) not in context.projection.timeline:
            findings.append(
                _finding(
                    "TIMELINE_UNKNOWN_PREDECESSOR",
                    f"sequence_after 指向未知时间线记录 {after_id}。",
                    location=f"state_changes:{change.record_id}",
                )
            )
    return _report(
        "Timeline Validator", findings, {"latest_order_key": latest_order}
    )


def validate_knowledge(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    known: set[tuple[str, str]] = set()
    for edge in context.projection.knowledge.values():
        state = str(edge.get("knowledge_state", "KNOWN")).upper()
        if state not in {"UNKNOWN", "FALSE", "DENIED"}:
            known.add((str(edge.get("character_id")), str(edge.get("fact_id"))))
    learned = {
        (str(change.payload.get("character_id")), str(change.payload.get("fact_id")))
        for change in _changes(context, "knowledge")
    }
    for claim in context.draft.knowledge_claims:
        character_resolution = resolve_projection_alias(
            context.projection.entities, claim.character_id
        )
        if character_resolution.status in {"AMBIGUOUS", "CONFLICT"}:
            findings.append(
                _finding(
                    "KNOWLEDGE_ENTITY_ALIAS_AMBIGUOUS",
                    f"角色/实体别名 {claim.character_id} 无法唯一解析："
                    f"{character_resolution.matches}",
                    location="knowledge_claims",
                )
            )
        character_id = character_resolution.canonical_id or claim.character_id
        pair = (character_id, claim.fact_id)
        if claim.basis == "already_known" and pair not in known:
            findings.append(
                _finding(
                    "KNOWLEDGE_NOT_ESTABLISHED",
                    f"{claim.character_id} 的知识 {claim.fact_id} 未在正史建立。",
                    location="knowledge_claims",
                    suggested_fix="改为在本章可观察地获知，并提交 knowledge state change。",
                )
            )
        if claim.basis == "learned_in_draft" and pair not in learned:
            findings.append(
                _finding(
                    "KNOWLEDGE_LEARNING_NOT_RECORDED",
                    f"{claim.character_id} 在本章获知 {claim.fact_id}，但没有知识边状态变化。",
                    location="knowledge_claims",
                )
            )
    return _report("Knowledge Validator", findings)


def validate_character(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    score: float | None = None
    if context.draft.evidence_policy == "COMPILED_SOFT":
        semantic_status = "UNKNOWN"
    else:
        try:
            config = context.settings.metrics["character_fit"]
            score = character_fit(context.draft.character_fit_inputs, config)
            minimum = float(config["minimum"])
            if score < minimum:
                findings.append(
                    _finding(
                        "CHARACTER_FIT_BELOW_MINIMUM",
                        f"人物契合度 {score:.2f} 低于参考线 {minimum:.2f}，建议人工复核。",
                        severity=Severity.WARNING,
                        location="character_fit_inputs",
                    )
                )
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(
                _finding(
                    "CHARACTER_FIT_INPUT_INVALID",
                    f"人物契合度输入无效：{exc}",
                    severity=Severity.WARNING,
                    location="character_fit_inputs",
                )
            )
        semantic_status = "EXPLICIT_INPUT"
    for violation in context.draft.character_bottom_line_violations:
        findings.append(
            _finding(
                "CHARACTER_BOTTOM_LINE",
                violation,
                severity=Severity.FATAL,
                location="character_bottom_line_violations",
            )
        )
    return _report(
        "Character Validator",
        findings,
        {
            "character_fit": score,
            "semantic_review_status": semantic_status,
            "measurements": context.draft.deterministic_measurements,
        },
    )


def validate_economy_power(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    for change in _changes(context, "resource"):
        payload = change.payload
        resolution = resolve_projection_alias(
            context.projection.resources, change.record_id
        )
        resource_name = str(
            payload.get("resource_name")
            or payload.get("name")
            or payload.get("title")
            or ""
        ).strip()
        if resolution.status == "NOT_FOUND" and resource_name:
            resolution = resolve_projection_alias(
                context.projection.resources, resource_name
            )
        if resolution.status in {"AMBIGUOUS", "CONFLICT"}:
            findings.append(
                _finding(
                    "RESOURCE_ALIAS_AMBIGUOUS",
                    f"资源引用 {change.record_id} 无法唯一解析：{resolution.matches}",
                    location=f"state_changes:{change.record_id}",
                )
            )
        elif (
            resolution.status == "NOT_FOUND"
            and context.projection.resources
            and payload.get("before_quantity") is not None
        ):
            findings.append(
                _finding(
                    "RESOURCE_ALIAS_NOT_FOUND",
                    f"资源引用 {change.record_id} 在当前 Canon Projection 中不存在。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        before = _number(payload.get("before_quantity"))
        delta = _number(payload.get("delta"))
        after = _number(payload.get("after_quantity", payload.get("quantity")))
        existing = (
            None
            if resolution.canonical_id is None
            else context.projection.resources.get(resolution.canonical_id)
        )
        existing_quantity = (
            None if existing is None else _number(existing.get("quantity"))
        )
        if (
            before is not None
            and existing_quantity is not None
            and abs(before - existing_quantity) > 1e-9
        ):
            findings.append(
                _finding(
                    "RESOURCE_BASE_MISMATCH",
                    f"资源起点 {before:g} 与正史 {existing_quantity:g} 不一致。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        if (
            before is not None
            and delta is not None
            and after is not None
            and abs(before + delta - after) > 1e-9
        ):
            findings.append(
                _finding(
                    "RESOURCE_NOT_CONSERVED",
                    "before_quantity + delta 不等于 after_quantity。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        if after is not None and after < 0:
            findings.append(
                _finding(
                    "RESOURCE_NEGATIVE",
                    "资源结余不得为负。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        increased = after is not None and after > (before if before is not None else 0)
        if increased and not (payload.get("source") or payload.get("causal_source")):
            findings.append(
                _finding(
                    "RESOURCE_SOURCE_MISSING",
                    "资源增加缺少 source/causal_source。",
                    location=f"state_changes:{change.record_id}",
                )
            )
    for change in _changes(context, "capability"):
        payload = change.payload
        absolute = _number(payload.get("absolute_capacity"))
        effective = _number(payload.get("effective_capacity"))
        if absolute is not None and absolute < 0 or effective is not None and effective < 0:
            findings.append(
                _finding(
                    "CAPABILITY_NEGATIVE",
                    "能力值不得为负。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        if absolute is not None and effective is not None and effective > absolute:
            findings.append(
                _finding(
                    "CAPABILITY_EXCEEDS_ABSOLUTE",
                    "effective_capacity 不得高于 absolute_capacity。",
                    location=f"state_changes:{change.record_id}",
                )
            )
        if bool(payload.get("increased")) and not (
            payload.get("source") or payload.get("causal_source")
        ):
            findings.append(
                _finding(
                    "CAPABILITY_SOURCE_MISSING",
                    "战力提升缺少可追溯来源。",
                    location=f"state_changes:{change.record_id}",
                )
            )
    delta_values = list(context.draft.progression_deltas)
    for change in context.draft.state_changes:
        progression = change.payload.get("progression")
        raw_deltas = progression.get("deltas", []) if isinstance(progression, dict) else []
        change_deltas: list[ProgressionDelta] = []
        if isinstance(progression, dict) and not raw_deltas:
            before_index = progression.get(
                "before_index", progression.get("before_progression_index")
            )
            after_index = progression.get("after_index", progression.get("progression_index"))
            if before_index is not None and after_index is not None and before_index != after_index:
                findings.append(
                    _finding(
                        "PROGRESSION_INDEX_WITHOUT_DELTA",
                        "progression index 发生变化，但没有对应的 ProgressionDelta。",
                        location=f"state_changes:{change.record_id}:progression",
                    )
                )
        if isinstance(raw_deltas, list):
            for item in raw_deltas:
                try:
                    parsed_delta = ProgressionDelta.model_validate(item)
                    delta_values.append(parsed_delta)
                    change_deltas.append(parsed_delta)
                except (TypeError, ValueError) as exc:
                    findings.append(
                        _finding(
                            "PROGRESSION_DELTA_INVALID",
                            f"progression delta 无效：{exc}",
                            location=f"state_changes:{change.record_id}:progression.deltas",
                        )
                    )
            for item in change_deltas:
                if item.kind.value in {"REUSE", "SHOWCASE"} and isinstance(progression, dict):
                    before_index = progression.get(
                        "before_index", progression.get("before_progression_index")
                    )
                    after_index = progression.get(
                        "after_index", progression.get("progression_index")
                    )
                    if (
                        before_index is not None
                        and after_index is not None
                        and before_index != after_index
                    ):
                        findings.append(
                            _finding(
                                "PROGRESSION_REUSE_ADVANCES_INDEX",
                                f"{item.delta_id} 声明为 {item.kind.value}，"
                                "但 progression index 发生变化。",
                                location=f"state_changes:{change.record_id}:progression",
                            )
                        )
    findings.extend(_quality_findings(progression_delta_issues(delta_values)))

    for change in context.draft.state_changes:
        payload = change.payload
        raw_constraints = payload.get("usage_constraints", payload.get("usage_constraint", []))
        if isinstance(raw_constraints, dict):
            raw_constraints = [raw_constraints]
        if not isinstance(raw_constraints, list):
            findings.append(
                _finding(
                    "USAGE_CONSTRAINT_INVALID",
                    "usage_constraint(s) 必须是 object 或 object 列表。",
                    location=f"state_changes:{change.record_id}:usage_constraints",
                )
            )
            continue
        for index, raw in enumerate(raw_constraints):
            try:
                constraint = UsageConstraint.model_validate(raw)
            except (TypeError, ValueError) as exc:
                findings.append(
                    _finding(
                        "USAGE_CONSTRAINT_INVALID",
                        f"usage constraint 无效：{exc}",
                        location=f"state_changes:{change.record_id}:usage_constraints:{index}",
                    )
                )
                continue
            quantity: float | None = None
            if constraint.resource_ref:
                resolution = resolve_projection_alias(
                    context.projection.resources, constraint.resource_ref
                )
                if resolution.canonical_id:
                    resource = context.projection.resources.get(resolution.canonical_id)
                    if resource is not None:
                        quantity = _number(resource.get("quantity"))
            reset_observed = bool(
                payload.get("usage_reset")
                or payload.get("reset_condition_satisfied")
                or payload.get("reset_event")
            )
            findings.extend(
                _quality_findings(
                    usage_constraint_issues(
                        constraint,
                        resource_quantity=quantity,
                        reset_observed=reset_observed,
                        location=f"state_changes:{change.record_id}:usage_constraints",
                    )
                )
            )
    return _report("Economy / Power Validator", findings)


def _quotes_in_prose(
    prose: str,
    quotes: list[str],
    key: str,
    findings: list[ValidationFinding],
    *,
    contract_requirement: bool = False,
    soft_missing: bool = False,
    actual_state_change: bool = False,
    match_records: list[dict[str, Any]] | None = None,
) -> None:
    if not quotes:
        if match_records is not None:
            match_records.append({"key": key, "quote": "", "status": "NOT_FOUND"})
        findings.append(
            _finding(
                (
                    "STATE_CHANGE_NOT_OBSERVED_IN_PROSE"
                    if actual_state_change
                    else "CONTRACT_EVIDENCE_EMPTY"
                ),
                (
                    f"StateChange {key} 没有可由正文观察到的证据。"
                    if actual_state_change
                    else f"合同证据 {key} 为空。"
                ),
                severity=(
                    Severity.ERROR
                    if actual_state_change
                    else (
                        Severity.WARNING
                        if contract_requirement or soft_missing
                        else Severity.ERROR
                    )
                ),
                location=(key if actual_state_change else f"contract_evidence:{key}"),
            )
        )
        return
    for quote in quotes:
        status = _match_evidence(prose, quote)
        if match_records is not None:
            match_records.append({"key": key, "quote": quote, "status": status})
        if status == "EXACT":
            continue
        if status == "NORMALIZED" and not contract_requirement:
            continue
        severity = (
            Severity.ERROR
            if actual_state_change and status == "NOT_FOUND"
            else (
                Severity.WARNING
                if contract_requirement or soft_missing or status != "NOT_FOUND"
                else Severity.ERROR
            )
        )
        code = (
            "STATE_CHANGE_NOT_OBSERVED_IN_PROSE"
            if actual_state_change and status == "NOT_FOUND"
            else {
            "NORMALIZED": "EVIDENCE_NORMALIZED",
            "AMBIGUOUS": "EVIDENCE_AMBIGUOUS",
            "NOT_FOUND": "EVIDENCE_NOT_IN_PROSE",
            }[status]
        )
        message = (
            f"证据短句匹配状态为 {status}：{quote}"
            if status != "NOT_FOUND"
            else f"证据短句不在正文中（{status}）：{quote}"
        )
        findings.append(
            _finding(
                code,
                message,
                severity=severity,
                evidence=[quote],
                location=key,
            )
        )


def _kernel_claims(value: object, *, key: str | None = None) -> set[str]:
    if not isinstance(value, list):
        return set()
    claims: set[str] = set()
    for item in value:
        if isinstance(item, dict) and key:
            claim = str(item.get(key) or "").strip()
        else:
            claim = str(item).strip()
        if claim:
            claims.add(claim)
    return claims


def _stage_target(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("to") or "").strip()
    parts = [
        item.strip()
        for item in re.split(r"(?:->|→|=>|至|到)", str(value or ""))
        if item.strip()
    ]
    return parts[-1] if parts else ""


def _compiled_realized_kernel_trace(
    context: ValidationContext,
) -> RealizedKernelTrace:
    """Compile the observable trace from authoritative draft fields."""

    axis_advanced: list[str] = []
    progression_delta_type: list[str] = []
    stage_change: str | None = None
    resource_change: list[str] = []
    ability_unlock: list[str] = []
    growth_cost: list[str] = []
    resource_changes: list[str] = []
    world_expansion_changes: list[str] = []
    evidence: list[RealizedKernelEvidence] = []
    progression_deltas: list[ProgressionDelta] = list(context.draft.progression_deltas)
    knowledge_by_truth: dict[str, str] = {}
    for change in context.draft.state_changes:
        payload = change.payload
        if change.kind == "knowledge":
            truth_id = str(payload.get("truth_id") or "").strip()
            if truth_id:
                knowledge_by_truth[truth_id] = change.record_id
        progression = payload.get("progression")
        if isinstance(progression, dict):
            for key, target in (
                ("axis_advanced", axis_advanced),
                ("progression_delta_type", progression_delta_type),
                ("growth_cost", growth_cost),
            ):
                raw = progression.get(key, [])
                if isinstance(raw, list):
                    target.extend(str(item) for item in raw if str(item).strip())
            raw_stage = progression.get("stage_change")
            if raw_stage:
                stage_change = str(raw_stage)
            raw_deltas = progression.get("deltas", [])
            if isinstance(raw_deltas, list):
                for item in raw_deltas:
                    try:
                        progression_deltas.append(ProgressionDelta.model_validate(item))
                    except (TypeError, ValueError):
                        continue
        if change.kind == "resource":
            resource_id = str(
                payload.get("resource_id") or payload.get("name") or change.record_id
            )
            resource_change.append(resource_id)
            resource_changes.append(resource_id)
        if change.kind == "capability":
            ability_unlock.append(
                str(payload.get("capability_id") or payload.get("name") or change.record_id)
            )
        if isinstance(payload.get("world_expansion"), dict):
            world_expansion_changes.append(change.record_id)
        if change.evidence_quotes:
            evidence.append(
                RealizedKernelEvidence(
                    claim=f"{change.kind}:{change.record_id}",
                    state_change_record_ids=[change.record_id],
                    evidence_quotes=list(change.evidence_quotes),
                )
            )
    for event in context.draft.reveal_trace.realized:
        record_id = knowledge_by_truth.get(event.truth_id)
        if record_id:
            evidence.append(
                RealizedKernelEvidence(
                    claim=f"reveal:{event.truth_id}",
                    state_change_record_ids=[record_id],
                    evidence_quotes=[event.evidence_quote],
                )
            )
    return RealizedKernelTrace(
        expected_contract_id=context.contract.contract_id,
        reader_promises_served=list(
            dict.fromkeys(
                [*context.draft.promises_advanced, *context.draft.promises_paid]
            )
        ),
        progression_impact=ProgressionImpact(
            axis_advanced=list(dict.fromkeys(axis_advanced)),
            progression_delta_type=list(dict.fromkeys(progression_delta_type)),
            stage_change=stage_change,
            resource_change=list(dict.fromkeys(resource_change)),
            ability_unlock=list(dict.fromkeys(ability_unlock)),
            growth_cost=list(dict.fromkeys(growth_cost)),
            deltas=list({item.delta_id: item for item in progression_deltas}.values()),
        ),
        resource_changes=list(dict.fromkeys(resource_changes)),
        world_expansion_changes=list(dict.fromkeys(world_expansion_changes)),
        payoff_channels_realized=list(dict.fromkeys(context.draft.promises_paid)),
        debts_advanced=list(dict.fromkeys(context.draft.promises_advanced)),
        debts_paid=list(dict.fromkeys(context.draft.promises_paid)),
        evidence=evidence,
    )


def _validate_realized_kernel_trace(
    context: ValidationContext,
) -> tuple[list[ValidationFinding], dict[str, Any]]:
    findings: list[ValidationFinding] = []
    status = context.contract.kernel_verification_status
    compiled_trace = _compiled_realized_kernel_trace(context)
    trace = context.draft.realized_kernel_trace
    if status == "LEGACY_NO_EFFECTIVE_CONTRACT":
        if trace is not None:
            findings.append(
                _finding(
                    "KERNEL_TRACE_WITHOUT_EFFECTIVE_CONTRACT",
                    "Legacy 合同没有 Verified Kernel Trace；草稿声明只作为未核验备注。",
                    severity=Severity.WARNING,
                    location="realized_kernel_trace",
                )
            )
        return findings, {
            "status": status,
            "expected": {},
            "realized": {},
            "compiled": compiled_trace.model_dump(mode="json"),
        }
    if trace is None:
        findings.append(
            _finding(
                "REALIZED_KERNEL_TRACE_MISSING",
                "草稿未提供 RealizedKernelTrace 提示；已由 Python 根据正文、StateChange、"
                "Reveal 与 promises 编译实际 trace。",
                severity=Severity.WARNING,
                location="realized_kernel_trace",
            )
        )
        return findings, {
            "status": status,
            "expected": context.contract.verified_kernel_trace,
            "evidence_matches": [],
            "realized": compiled_trace.model_dump(mode="json"),
            "compiled": compiled_trace.model_dump(mode="json"),
        }
    if trace.expected_contract_id != context.contract.contract_id:
        findings.append(
            _finding(
                "REALIZED_KERNEL_CONTRACT_MISMATCH",
                "RealizedKernelTrace 引用的 Chapter Contract 不匹配。",
                location="realized_kernel_trace.expected_contract_id",
            )
        )

    state_changes = {item.record_id: item for item in context.draft.state_changes}
    evidence_matches: list[dict[str, Any]] = []
    for item in trace.evidence:
        unknown = set(item.state_change_record_ids) - set(state_changes)
        if unknown:
            findings.append(
                _finding(
                    "KERNEL_EVIDENCE_STATE_CHANGE_UNKNOWN",
                    f"Kernel Evidence 引用了不存在的 StateChange：{sorted(unknown)}",
                    location="realized_kernel_trace.evidence",
                )
            )
        _quotes_in_prose(
            context.draft.prose_markdown,
            item.evidence_quotes,
            f"realized_kernel_trace:{item.claim}",
            findings,
            soft_missing=context.draft.evidence_policy == "COMPILED_SOFT",
            match_records=evidence_matches,
        )

    impact = trace.progression_impact
    realized_has_claims = any(
        (
            trace.reader_promises_served,
            trace.narrative_drives_advanced,
            impact.axis_advanced,
            impact.progression_delta_type,
            impact.stage_change,
            impact.resource_change,
            impact.ability_unlock,
            impact.growth_cost,
            trace.resource_changes,
            trace.world_expansion_changes,
            trace.payoff_channels_realized,
            trace.debts_advanced,
            trace.debts_paid,
        )
    )
    if realized_has_claims and not trace.evidence:
        findings.append(
            _finding(
                "REALIZED_KERNEL_EVIDENCE_MISSING",
                "Realized Kernel 声明必须绑定正文证据与 StateChange。",
                location="realized_kernel_trace.evidence",
            )
        )

    expected = context.contract.verified_kernel_trace
    expected_reader = {
        str(item.get("promise_id"))
        for item in expected.get("reader_promise_alignment", [])
        if isinstance(item, dict)
        and item.get("verification_status") == "VERIFIED"
        and item.get("promise_id")
    }
    expected_drive = expected.get("narrative_drive_alignment", {})
    expected_drives = _kernel_claims(
        expected_drive.get("drives_advanced", [])
        if isinstance(expected_drive, dict)
        else []
    )
    expected_progression = expected.get("progression_impact", {})
    if not isinstance(expected_progression, dict):
        expected_progression = {}
    expected_axes = _kernel_claims(expected_progression.get("axis_advanced", []))
    expected_deltas = _kernel_claims(
        expected_progression.get("progression_delta_type", [])
    )
    expected_resources = _kernel_claims(
        expected_progression.get("resource_changes", []), key="claim"
    ) | _kernel_claims(expected.get("resource_impact", []), key="claim")
    expected_abilities = _kernel_claims(
        expected_progression.get("ability_unlocks", []), key="claim"
    )
    expected_world = _kernel_claims(expected.get("world_expansion_impact", []))
    expected_payoffs = _kernel_claims(expected.get("payoff_channels", []))
    expected_scheduler = expected.get("scheduler_alignment", {})
    if not isinstance(expected_scheduler, dict):
        expected_scheduler = {}
    expected_debts = _kernel_claims(expected_scheduler.get("debts_served", []))
    expected_intent = str(
        expected_scheduler.get("candidate_primary_intent")
        or context.contract.chapter_intent
        or ""
    )
    expected_stage = _stage_target(expected_progression.get("stage_change"))

    checks = (
        ("reader promise", set(trace.reader_promises_served), expected_reader),
        ("narrative drive", set(trace.narrative_drives_advanced), expected_drives),
        ("growth axis", set(impact.axis_advanced), expected_axes),
        ("progression delta", set(impact.progression_delta_type), expected_deltas),
        (
            "resource",
            set(impact.resource_change) | set(trace.resource_changes),
            expected_resources,
        ),
        ("ability", set(impact.ability_unlock), expected_abilities),
        ("world expansion", set(trace.world_expansion_changes), expected_world),
        ("payoff channel", set(trace.payoff_channels_realized), expected_payoffs),
        (
            "narrative debt",
            set(trace.debts_advanced) | set(trace.debts_paid),
            expected_debts,
        ),
    )
    underdelivered: dict[str, list[str]] = {}
    unexpected: dict[str, list[str]] = {}
    for label, realized_values, expected_values in checks:
        extras = realized_values - expected_values
        missing = expected_values - realized_values
        if extras:
            unexpected[label] = sorted(extras)
            findings.append(
                _finding(
                    "REALIZED_KERNEL_EXCEEDS_VERIFIED_CONTRACT",
                    f"Realized {label} 超出 Verified Kernel Trace：{sorted(extras)}",
                    severity=Severity.WARNING,
                    location="realized_kernel_trace",
                )
            )
        if missing:
            underdelivered[label] = sorted(missing)
            findings.append(
                _finding(
                    "REALIZED_KERNEL_UNDERDELIVERY",
                    f"Expected {label} 未在正文中兑现：{sorted(missing)}",
                    severity=Severity.WARNING,
                    location="realized_kernel_trace",
                )
            )

    realized_stage = _stage_target(impact.stage_change)
    if trace.primary_intent and trace.primary_intent != expected_intent:
        findings.append(
            _finding(
                "REALIZED_PRIMARY_INTENT_MISMATCH",
                "实际 Primary Intent "
                f"{trace.primary_intent} 与合同 {expected_intent or 'NONE'} 不一致。",
                severity=Severity.WARNING,
                location="realized_kernel_trace.primary_intent",
            )
        )
    elif expected_intent and not trace.primary_intent:
        underdelivered["primary intent"] = [expected_intent]
        findings.append(
            _finding(
                "REALIZED_KERNEL_UNDERDELIVERY",
                f"Expected Primary Intent 未明确兑现：{expected_intent}",
                severity=Severity.WARNING,
                location="realized_kernel_trace.primary_intent",
            )
        )
    if realized_stage and realized_stage != expected_stage:
        unexpected["stage transition"] = [realized_stage]
        findings.append(
            _finding(
                "REALIZED_STAGE_TRANSITION_MISMATCH",
                f"实际阶段目标 {realized_stage} 与核验合同 {expected_stage or 'NONE'} 不一致。",
                severity=Severity.WARNING,
                location="realized_kernel_trace.progression_impact.stage_change",
            )
        )
    elif expected_stage and not realized_stage:
        underdelivered["stage transition"] = [expected_stage]
        findings.append(
            _finding(
                "REALIZED_KERNEL_UNDERDELIVERY",
                f"Expected stage transition 未兑现：{expected_stage}",
                severity=Severity.WARNING,
                location="realized_kernel_trace.progression_impact.stage_change",
            )
        )

    if realized_stage:
        stage_changes = [
            item
            for item in context.draft.state_changes
            if item.kind in {"character_state", "fact"}
            and isinstance(item.payload.get("progression"), dict)
            and str(item.payload["progression"].get("stage_id") or "")
            == realized_stage
        ]
        if not stage_changes:
            findings.append(
                _finding(
                    "REALIZED_STAGE_STATE_CHANGE_MISSING",
                    "阶段变化必须落到 character_state 或 fact 的 progression payload。",
                    location="state_changes",
                )
            )
    if impact.ability_unlock and not any(
        item.kind == "capability" for item in context.draft.state_changes
    ):
        findings.append(
            _finding(
                "REALIZED_ABILITY_STATE_CHANGE_MISSING",
                "能力解锁必须有 capability StateChange。",
                location="state_changes",
            )
        )
    if (impact.resource_change or trace.resource_changes) and not any(
        item.kind == "resource" for item in context.draft.state_changes
    ):
        findings.append(
            _finding(
                "REALIZED_RESOURCE_STATE_CHANGE_MISSING",
                "资源变化必须有 resource StateChange。",
                location="state_changes",
            )
        )
    if trace.world_expansion_changes and not any(
        item.kind == "fact" and isinstance(item.payload.get("world_expansion"), dict)
        for item in context.draft.state_changes
    ):
        findings.append(
            _finding(
                "REALIZED_WORLD_EXPANSION_STATE_CHANGE_MISSING",
                "世界层级变化必须有 fact StateChange 的 world_expansion payload。",
                location="state_changes",
            )
        )

    return findings, {
        "status": status,
        "expected": expected,
        "realized": trace.model_dump(mode="json"),
        "underdelivered": underdelivered,
        "unexpected": unexpected,
        "evidence_matches": evidence_matches,
        "compiled": compiled_trace.model_dump(mode="json"),
    }


def validate_contract(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    evidence_matches: list[dict[str, Any]] = []
    if (
        context.draft.realization_diagnostics.get("code")
        == "CONTRACT_REALIZATION_UNDERSPECIFIED"
    ):
        findings.append(
            _finding(
                "CONTRACT_REALIZATION_UNDERSPECIFIED",
                "当前 Chapter Contract 不足以承载独立章节，应返回 Planning/Contract。",
                location="realization_diagnostics",
            )
        )
    required = {
        "required_irreversible_change",
        "ending_state",
        *(f"commit:{item}" for item in context.contract.commit_updates),
    }
    if str(getattr(context.contract, "required_cost", "") or "").strip():
        required.add("required_cost")
    for key in sorted(required):
        quotes = context.draft.contract_evidence.get(key)
        if quotes is None:
            evidence_matches.append({"key": key, "quote": "", "status": "NOT_FOUND"})
            findings.append(
                _finding(
                    "CONTRACT_REQUIREMENT_MISSING",
                    f"正文输出未为合同要求 {key} 提供证据。",
                    location="contract_evidence",
                )
            )
            continue
        _quotes_in_prose(
            context.draft.prose_markdown,
            quotes,
            key,
            findings,
            contract_requirement=True,
            match_records=evidence_matches,
        )
    for change in context.draft.state_changes:
        _quotes_in_prose(
            context.draft.prose_markdown,
            change.evidence_quotes,
            f"state_changes:{change.record_id}",
            findings,
            actual_state_change=True,
            match_records=evidence_matches,
        )
    kernel_findings, kernel_comparison = _validate_realized_kernel_trace(context)
    findings.extend(kernel_findings)
    agenda = context.contract.reveal_agenda
    if agenda:
        agenda_items = {
            str(item["truth_id"]): item
            for key in ("must_reveal", "should_hint", "keep_hidden", "optional")
            for item in agenda.get(key, [])
            if isinstance(item, dict) and item.get("truth_id")
        }
        must_reveal = {
            str(item.get("truth_id"))
            for item in agenda.get("must_reveal", [])
            if isinstance(item, dict) and item.get("truth_id")
        }
        should_hint = {
            str(item.get("truth_id"))
            for item in agenda.get("should_hint", [])
            if isinstance(item, dict) and item.get("truth_id")
        }
        keep_hidden = {
            str(item.get("truth_id"))
            for item in agenda.get("keep_hidden", [])
            if isinstance(item, dict) and item.get("truth_id")
        }
        realized: dict[str, list[Any]] = {}
        for event in context.draft.reveal_trace.realized:
            realized.setdefault(event.truth_id, []).append(event)
            planned_item = agenda_items.get(event.truth_id)
            if planned_item is None:
                findings.append(
                    _finding(
                        "REVEAL_NOT_IN_AGENDA",
                        f"Reveal {event.truth_id} 没有本章 Agenda 授权。",
                        location="reveal_trace.realized",
                    )
                )
            else:
                plan = planned_item.get("plan") or {}
                expected_target = str(plan.get("target") or "READER")
                expected_entity = plan.get("target_entity_id")
                if (
                    event.target.value != expected_target
                    or event.target_entity_id != expected_entity
                ):
                    findings.append(
                        _finding(
                            "REVEAL_TARGET_MISMATCH",
                            f"Reveal {event.truth_id} 的 target 与冻结 RevealPlan 不一致。",
                            location="reveal_trace.realized",
                        )
                    )
                expected_depth = str(planned_item.get("reveal_depth") or "")
                if (
                    planned_item.get("agenda_bucket") == "MUST_REVEAL"
                    and expected_depth
                    and event.depth.value != expected_depth
                ):
                    findings.append(
                        _finding(
                            "REVEAL_DEPTH_MISMATCH",
                            f"Reveal {event.truth_id} 应使用 {expected_depth}，"
                            f"实际为 {event.depth.value}。",
                            location="reveal_trace.realized",
                        )
                    )
            depth_state = {
                "HINT": "HINTED",
                "STRONG_HINT": "SUSPECTED",
                "PARTIAL_REVEAL": "PARTIALLY_REVEALED",
                "FALSE_LEAD": "MISLEADING_BELIEF",
                "CONFIRMATION": "CONFIRMED",
                "FULL_REVEAL": "CONFIRMED",
            }[event.depth.value]
            if event.expected_knowledge_change.value != depth_state:
                findings.append(
                    _finding(
                        "REVEAL_KNOWLEDGE_DEPTH_MISMATCH",
                        f"Reveal {event.truth_id} 的知识变化必须与 {event.depth.value} 对应。",
                        location="reveal_trace.realized",
                    )
                )
            evidence_status = _match_evidence(
                context.draft.prose_markdown, event.evidence_quote
            )
            evidence_matches.append(
                {
                    "key": f"reveal_trace:{event.truth_id}",
                    "quote": event.evidence_quote,
                    "status": evidence_status,
                }
            )
            if evidence_status == "AMBIGUOUS":
                findings.append(
                    _finding(
                        "REVEAL_EVIDENCE_AMBIGUOUS",
                        f"Reveal {event.truth_id} 的证据短句匹配状态为 AMBIGUOUS。",
                        severity=Severity.WARNING,
                        evidence=[event.evidence_quote],
                        location="reveal_trace.realized",
                    )
                )
            elif evidence_status == "NOT_FOUND":
                findings.append(
                    _finding(
                        "REVEAL_EVIDENCE_NOT_IN_PROSE",
                        f"Reveal {event.truth_id} 的证据短句不在正文中（NOT_FOUND）。",
                        evidence=[event.evidence_quote],
                        location="reveal_trace.realized",
                    )
                )
            transitions = [
                item
                for item in context.draft.reveal_trace.knowledge_transitions
                if item.truth_id == event.truth_id
                and item.target == event.target
                and item.target_entity_id == event.target_entity_id
            ]
            if len(transitions) != 1 or transitions[0].after.value != depth_state:
                findings.append(
                    _finding(
                        "KNOWLEDGE_TRANSITION_MISSING_OR_INVALID",
                        f"Reveal {event.truth_id} 必须有且只有一条匹配的 KnowledgeTransition。",
                        location="reveal_trace.knowledge_transitions",
                    )
                )
            if event.target.value == "CHARACTER":
                state_changes = [
                    change
                    for change in context.draft.state_changes
                    if change.kind == "knowledge"
                    and str(
                        change.payload.get("truth_id")
                        or change.payload.get("fact_id")
                        or ""
                    )
                    == event.truth_id
                    and str(change.payload.get("character_id") or "")
                    == str(event.target_entity_id or "")
                ]
                if not state_changes:
                    findings.append(
                        _finding(
                            "CHARACTER_REVEAL_STATE_CHANGE_MISSING",
                            f"角色 Reveal {event.truth_id} 缺少 knowledge StateChange。",
                            location="state_changes",
                        )
                    )
        planned = {
            item.truth_id: item for item in context.draft.reveal_trace.planned
        }
        if len(planned) != len(context.draft.reveal_trace.planned):
            findings.append(
                _finding(
                    "REVEAL_PLANNED_DUPLICATE",
                    "RevealTrace.planned 存在重复 truth_id。",
                    severity=Severity.WARNING,
                    location="reveal_trace.planned",
                )
            )
        unknown_planned = set(planned) - set(agenda_items)
        if unknown_planned:
            findings.append(
                _finding(
                    "REVEAL_PLANNED_NOT_IN_AGENDA",
                    "RevealTrace.planned 包含未在合同 Agenda 中的 Truth。",
                    evidence=[
                        f"unknown={sorted(unknown_planned)}",
                    ],
                    severity=Severity.WARNING,
                    location="reveal_trace.planned",
                )
            )
        for truth_id, item in planned.items():
            expected_bucket = str(
                agenda_items.get(truth_id, {}).get("agenda_bucket") or ""
            )
            if item.agenda_bucket.value != expected_bucket:
                findings.append(
                    _finding(
                        "REVEAL_PLANNED_BUCKET_MISMATCH",
                        f"Truth {truth_id} 的 planned bucket 与合同 Agenda 不一致。",
                        location="reveal_trace.planned",
                    )
                )
        for truth_id in sorted(must_reveal):
            events = realized.get(truth_id, [])
            if not events or not any(
                event.depth.value
                in {"PARTIAL_REVEAL", "CONFIRMATION", "FULL_REVEAL"}
                for event in events
            ):
                findings.append(
                    _finding(
                        "MUST_REVEAL_MISSING",
                        f"本章必须揭示的 Truth {truth_id} 未实际发生。",
                        location="reveal_trace",
                    )
                )
        for truth_id in sorted(keep_hidden):
            if realized.get(truth_id):
                findings.append(
                    _finding(
                        "KEEP_HIDDEN_BREACHED",
                        f"Truth {truth_id} 本章必须继续隐藏，却出现在 realized reveal 中。",
                        severity=Severity.FATAL,
                        location="reveal_trace",
                    )
                )
        for truth_id in sorted(should_hint):
            events = realized.get(truth_id, [])
            if not any(
                event.depth.value in {"HINT", "STRONG_HINT", "FALSE_LEAD"}
                and event.evidence_quote.strip()
                for event in events
            ):
                findings.append(
                    _finding(
                        "PLANNED_HINT_MISSING",
                        f"Truth {truth_id} 缺少本章计划的可读线索。",
                        location="reveal_trace",
                    )
                )
            if any(
                event.depth.value
                in {"PARTIAL_REVEAL", "CONFIRMATION", "FULL_REVEAL"}
                for event in events
            ):
                findings.append(
                    _finding(
                        "HINT_ESCALATED_TO_REVEAL",
                        f"Truth {truth_id} 只允许 HINT，却被直接部分或完整揭示。",
                        location="reveal_trace",
                    )
                )
        active_ids = {
            str(item.get("truth_id"))
            for item in context.contract.active_author_truths
            if isinstance(item, dict) and item.get("truth_id")
        }
        unknown = set(realized) - active_ids
        if unknown:
            findings.append(
                _finding(
                    "REVEAL_TRUTH_NOT_FROZEN",
                    f"Reveal Trace 引用了合同未冻结的 Truth：{sorted(unknown)}",
                    location="reveal_trace",
                )
            )
    elif (
        context.draft.reveal_trace.planned
        or context.draft.reveal_trace.realized
        or context.draft.reveal_trace.knowledge_transitions
    ):
        findings.append(
            _finding(
                "REVEAL_TRACE_WITHOUT_AGENDA",
                "合同没有 Reveal Agenda，草稿不得自行声明 RevealTrace。",
                location="reveal_trace",
            )
        )
    return _report(
        "Contract Validator",
        findings,
        {
            "requirements_checked": len(required),
            "kernel_trace_comparison": kernel_comparison,
            "evidence_matches": evidence_matches,
            "reveal_requirements_checked": sum(
                len(agenda.get(key, []))
                for key in ("must_reveal", "should_hint", "keep_hidden")
            )
            if agenda
            else 0,
        },
    )


def validate_debt(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    debt = context.contract.narrative_debt
    advance_value = debt.get("advance", [])
    pay_value = debt.get("fully_pay", [])
    allowed_value = debt.get("new_major_hooks_allowed", 0)
    required_advance = (
        {str(item) for item in advance_value}
        if isinstance(advance_value, list)
        else set()
    )
    required_pay = (
        {str(item) for item in pay_value} if isinstance(pay_value, list) else set()
    )
    missing_advance = required_advance - set(context.draft.promises_advanced)
    missing_pay = required_pay - set(context.draft.promises_paid)
    if missing_advance:
        findings.append(
            _finding(
                "DEBT_ADVANCE_MISSING",
                f"未推进合同承诺：{sorted(missing_advance)}",
                location="promises_advanced",
            )
        )
    if missing_pay:
        findings.append(
            _finding(
                "DEBT_PAYOFF_MISSING",
                f"未兑现合同承诺：{sorted(missing_pay)}",
                location="promises_paid",
            )
        )
    allowed = int(allowed_value) if isinstance(allowed_value, int) else 0
    if context.draft.new_major_hooks > allowed:
        findings.append(
            _finding(
                "DEBT_HOOK_OVERLOAD",
                f"新增重大悬念 {context.draft.new_major_hooks}，合同只允许 {allowed}。",
                severity=Severity.WARNING,
                location="new_major_hooks",
            )
        )
    return _report("Debt Validator", findings)


def validate_payoff(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    payoff_changes = _changes(context, "payoff")
    needs_payoff = context.contract.primary_function in {
        NarrativeFunction.PARTIAL_PAYOFF,
        NarrativeFunction.MAJOR_PAYOFF,
    }
    if needs_payoff and not payoff_changes:
        findings.append(
            _finding(
                "PAYOFF_STATE_CHANGE_MISSING",
                "兑现章节没有 payoff 状态变化。",
                location="state_changes",
            )
        )
    for change in payoff_changes:
        payload = change.payload
        for key in ("causal_source", "cost", "behavior_change"):
            if not payload.get(key):
                findings.append(
                    _finding(
                        "PAYOFF_CAUSAL_FIELD_MISSING",
                        f"兑现记录缺少 {key}。",
                        location=f"state_changes:{change.record_id}",
                    )
                )
        if context.contract.primary_function is NarrativeFunction.MAJOR_PAYOFF:
            aftershocks = payload.get("aftershock_obligations")
            if not isinstance(aftershocks, list) or len(aftershocks) < 4:
                findings.append(
                    _finding(
                        "PAYOFF_AFTERSHOCK_PLAN_MISSING",
                        "重大兑现必须列出至少四类余波义务。",
                        severity=Severity.WARNING,
                        location=f"state_changes:{change.record_id}",
                    )
                )
            cooldown_group = payload.get("cooldown_group")
            chapters_since = payload.get("chapters_since_same_subtype")
            occurrence_count = payload.get("same_subtype_occurrence_count")
            if not isinstance(cooldown_group, str) or not isinstance(
                occurrence_count, int
            ):
                findings.append(
                    _finding(
                        "PAYOFF_COOLDOWN_EVIDENCE_MISSING",
                        "重大兑现必须声明 cooldown_group 与同子类型历史次数。",
                        severity=Severity.WARNING,
                        location=f"state_changes:{change.record_id}",
                    )
                )
            else:
                try:
                    allowed = payoff_cooldown_allowed(
                        group=cooldown_group,
                        chapters_since_last=(
                            chapters_since if isinstance(chapters_since, int) else None
                        ),
                        occurrence_count=occurrence_count,
                        config=context.settings.metrics["payoff_cooldown"],
                    )
                except (KeyError, TypeError, ValueError) as exc:
                    findings.append(
                        _finding(
                            "PAYOFF_COOLDOWN_INPUT_INVALID",
                            f"爽点冷却证据无效：{exc}",
                            severity=Severity.WARNING,
                            location=f"state_changes:{change.record_id}",
                        )
                    )
                else:
                    if not allowed:
                        findings.append(
                            _finding(
                                "PAYOFF_COOLDOWN_ACTIVE",
                                "同子类型爽点仍在冷却期或已是一生一次事件。",
                                severity=Severity.WARNING,
                                location=f"state_changes:{change.record_id}",
                            )
                        )
    return _report("Payoff Validator", findings)


def validate_repetition(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    normalized_tags = {item.strip().casefold() for item in context.draft.structure_tags}
    for forbidden in context.contract.forbidden_repetitions:
        normalized = forbidden.strip().casefold()
        if normalized in normalized_tags or any(
            normalized and normalized in tag for tag in normalized_tags
        ):
            findings.append(
                _finding(
                    "FORBIDDEN_REPETITION",
                    f"命中合同禁止的近期结构：{forbidden}",
                    location="structure_tags",
                )
            )
    for recent in context.contract.recent_avoid_repetitions:
        normalized = recent.strip().casefold()
        if normalized in normalized_tags or any(
            normalized and normalized in tag for tag in normalized_tags
        ):
            findings.append(
                _finding(
                    "RECENT_STRUCTURE_AVOIDANCE",
                    f"命中近期结构软避让提示：{recent}",
                    severity=Severity.WARNING,
                    location="structure_tags",
                )
            )
    recent_signatures = {
        str(value.get("signature", "")).casefold()
        for value in context.projection.repetition.values()
        if value.get("signature")
    }
    repeated = sorted(normalized_tags & recent_signatures)
    if repeated:
        findings.append(
            _finding(
                "RECENT_STRUCTURE_REUSED",
                f"结构标签与近期记录完全重复：{repeated}",
                severity=Severity.WARNING,
                location="structure_tags",
            )
        )
    return _report("Repetition Validator", findings)


def validate_style(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    score: float | None = None
    if context.draft.evidence_policy == "COMPILED_SOFT":
        semantic_status = "UNKNOWN"
    else:
        try:
            score = style_fit(
                context.draft.style_fit_inputs,
                context.settings.metrics["style_fit"],
            )
            if score < 75:
                findings.append(
                    _finding(
                        "STYLE_FIT_LOW",
                        f"文风契合度仅 {score:.2f}，建议人工复核。",
                        severity=Severity.WARNING,
                        location="style_fit_inputs",
                    )
                )
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(
                _finding(
                    "STYLE_FIT_INPUT_INVALID",
                    f"文风契合度输入无效：{exc}",
                    severity=Severity.WARNING,
                    location="style_fit_inputs",
                )
            )
        semantic_status = "EXPLICIT_INPUT"
    for violation in context.draft.style_boundary_violations:
        findings.append(
            _finding(
                "STYLE_BOUNDARY_VIOLATION",
                violation,
                location="style_boundary_violations",
            )
        )
    realization = context.draft.realization_diagnostics
    if realization.get("code") == "SCENE_REALIZATION_THIN":
        findings.append(
            _finding(
                "SCENE_REALIZATION_THIN",
                "场景展开偏薄；只需补充表达层动作、反应或后果，不改变合同状态。",
                severity=Severity.WARNING,
                location="realization_diagnostics",
                suggested_fix=str(realization.get("suggested_fix") or ""),
            )
        )
    return _report(
        "Style Validator",
        findings,
        {
            "style_fit": score,
            "realization": realization,
            "semantic_review_status": semantic_status,
            "measurements": context.draft.deterministic_measurements,
        },
    )


VALIDATORS: tuple[Callable[[ValidationContext], ValidationReport], ...] = (
    validate_canon,
    validate_timeline,
    validate_knowledge,
    validate_character,
    validate_economy_power,
    validate_contract,
    validate_debt,
    validate_payoff,
    validate_repetition,
    validate_style,
)
