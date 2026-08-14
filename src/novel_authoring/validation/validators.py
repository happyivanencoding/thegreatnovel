from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from novel_authoring.canon.projection import CanonProjection
from novel_authoring.config import Settings
from novel_authoring.contracts.draft import DraftOutput, DraftStateChange
from novel_authoring.domain.models import ContinuationMode, NarrativeFunction, Severity
from novel_authoring.metrics.formulas import (
    character_fit,
    payoff_cooldown_allowed,
    style_fit,
)
from novel_authoring.planning.models import ChapterContract
from novel_authoring.validation.models import (
    ValidationFinding,
    ValidationReport,
    ValidatorName,
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


def validate_canon(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
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
        pair = (claim.character_id, claim.fact_id)
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
    try:
        config = context.settings.metrics["character_fit"]
        score = character_fit(context.draft.character_fit_inputs, config)
        minimum = float(config["minimum"])
        if score < minimum:
            findings.append(
                _finding(
                    "CHARACTER_FIT_BELOW_MINIMUM",
                    f"人物契合度 {score:.2f} 低于硬门 {minimum:.2f}。",
                    location="character_fit_inputs",
                )
            )
    except (KeyError, TypeError, ValueError) as exc:
        findings.append(
            _finding(
                "CHARACTER_FIT_INPUT_INVALID",
                f"人物契合度输入无效：{exc}",
                location="character_fit_inputs",
            )
        )
    for violation in context.draft.character_bottom_line_violations:
        findings.append(
            _finding(
                "CHARACTER_BOTTOM_LINE",
                violation,
                severity=Severity.FATAL,
                location="character_bottom_line_violations",
            )
        )
    return _report("Character Validator", findings, {"character_fit": score})


def validate_economy_power(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    for change in _changes(context, "resource"):
        payload = change.payload
        before = _number(payload.get("before_quantity"))
        delta = _number(payload.get("delta"))
        after = _number(payload.get("after_quantity", payload.get("quantity")))
        existing = context.projection.resources.get(change.record_id)
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
    return _report("Economy / Power Validator", findings)


def _quotes_in_prose(
    prose: str,
    quotes: list[str],
    key: str,
    findings: list[ValidationFinding],
) -> None:
    if not quotes:
        findings.append(
            _finding(
                "CONTRACT_EVIDENCE_EMPTY",
                f"合同证据 {key} 为空。",
                location=f"contract_evidence:{key}",
            )
        )
    for quote in quotes:
        if quote not in prose:
            findings.append(
                _finding(
                    "EVIDENCE_NOT_IN_PROSE",
                    f"证据短句不在正文中：{quote}",
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


def _validate_realized_kernel_trace(
    context: ValidationContext,
) -> tuple[list[ValidationFinding], dict[str, Any]]:
    findings: list[ValidationFinding] = []
    status = context.contract.kernel_verification_status
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
        return findings, {"status": status, "expected": {}, "realized": {}}
    if trace is None:
        findings.append(
            _finding(
                "REALIZED_KERNEL_TRACE_MISSING",
                "本章合同含 Verified Kernel Trace，草稿必须声明 RealizedKernelTrace。",
                location="realized_kernel_trace",
            )
        )
        return findings, {"status": status, "expected": context.contract.verified_kernel_trace}
    if trace.expected_contract_id != context.contract.contract_id:
        findings.append(
            _finding(
                "REALIZED_KERNEL_CONTRACT_MISMATCH",
                "RealizedKernelTrace 引用的 Chapter Contract 不匹配。",
                location="realized_kernel_trace.expected_contract_id",
            )
        )

    state_changes = {item.record_id: item for item in context.draft.state_changes}
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
    }


def validate_contract(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    required = {
        "required_irreversible_change",
        "ending_state",
        *(f"commit:{item}" for item in context.contract.commit_updates),
    }
    if context.contract.required_cost.strip():
        required.add("required_cost")
    for key in sorted(required):
        quotes = context.draft.contract_evidence.get(key)
        if quotes is None:
            findings.append(
                _finding(
                    "CONTRACT_REQUIREMENT_MISSING",
                    f"正文输出未为合同要求 {key} 提供证据。",
                    location="contract_evidence",
                )
            )
            continue
        _quotes_in_prose(context.draft.prose_markdown, quotes, key, findings)
    for change in context.draft.state_changes:
        _quotes_in_prose(
            context.draft.prose_markdown,
            change.evidence_quotes,
            f"state_changes:{change.record_id}",
            findings,
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
            if event.evidence_quote not in context.draft.prose_markdown:
                findings.append(
                    _finding(
                        "REVEAL_EVIDENCE_NOT_IN_PROSE",
                        f"Reveal {event.truth_id} 的证据短句不在正文中。",
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
                    location="reveal_trace.planned",
                )
            )
        required_planned = must_reveal | should_hint | keep_hidden
        if set(planned) != required_planned:
            findings.append(
                _finding(
                    "REVEAL_PLANNED_NOT_FROZEN_AGENDA",
                    "RevealTrace.planned 必须精确声明本章 MUST/SHOULD/KEEP Agenda。",
                    evidence=[
                        f"missing={sorted(required_planned - set(planned))}",
                        f"unknown={sorted(set(planned) - required_planned)}",
                    ],
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
                            location=f"state_changes:{change.record_id}",
                        )
                    )
                else:
                    if not allowed:
                        findings.append(
                            _finding(
                                "PAYOFF_COOLDOWN_ACTIVE",
                                "同子类型爽点仍在冷却期或已是一生一次事件。",
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
                location="structure_tags",
            )
        )
    return _report("Repetition Validator", findings)


def validate_style(context: ValidationContext) -> ValidationReport:
    findings: list[ValidationFinding] = []
    score: float | None = None
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
                location="style_fit_inputs",
            )
        )
    for violation in context.draft.style_boundary_violations:
        findings.append(
            _finding(
                "STYLE_BOUNDARY_VIOLATION",
                violation,
                location="style_boundary_violations",
            )
        )
    return _report("Style Validator", findings, {"style_fit": score})


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
