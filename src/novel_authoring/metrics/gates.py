from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from novel_authoring.metrics.formulas import character_fit, style_fit


class HardGateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canon_conflicts: list[str] = Field(default_factory=list)
    timeline_conflicts: list[str] = Field(default_factory=list)
    knowledge_violations: list[str] = Field(default_factory=list)
    missing_causal_sources: list[str] = Field(default_factory=list)
    payoff_cooldown_violations: list[str] = Field(default_factory=list)
    capability_violations: list[str] = Field(default_factory=list)
    author_constraint_violations: list[str] = Field(default_factory=list)
    style_boundary_violations: list[str] = Field(default_factory=list)
    character_bottom_line_violation: bool = False
    character_fit_inputs: dict[str, float] = Field(default_factory=dict)
    style_fit_inputs: dict[str, float] = Field(default_factory=dict)


class GateReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    passed: bool
    hard_failures: list[str]
    character_fit: float | None
    style_fit: float | None
    requires_character_bridge: bool
    style_review_required: bool
    soft_warnings: list[str] = Field(default_factory=list)
    kernel_warnings: list[str] = Field(default_factory=list)
    kernel_evidence: dict[str, object] = Field(default_factory=dict)


def evaluate_hard_gates(
    gate_input: HardGateInput, metrics_config: dict[str, object]
) -> GateReport:
    failures = [
        *gate_input.canon_conflicts,
        *gate_input.timeline_conflicts,
        *gate_input.knowledge_violations,
        *gate_input.missing_causal_sources,
        *gate_input.capability_violations,
        *gate_input.author_constraint_violations,
        *gate_input.style_boundary_violations,
    ]
    character_config = metrics_config["character_fit"]
    style_config = metrics_config["style_fit"]
    if not isinstance(character_config, dict) or not isinstance(style_config, dict):
        raise ValueError("Character/Style 配置无效")
    try:
        character_score = character_fit(gate_input.character_fit_inputs, character_config)
    except (KeyError, TypeError, ValueError):
        character_score = None
    try:
        style_score = style_fit(gate_input.style_fit_inputs, style_config)
    except (KeyError, TypeError, ValueError):
        style_score = None
    requires_bridge = (
        character_score is not None
        and character_score < float(character_config["minimum"])
    )
    soft_warnings = []
    if requires_bridge and character_score is not None:
        soft_warnings.append(f"character_fit={character_score:g} below recommendation minimum")
    soft_warnings.extend(
        f"payoff cooldown review: {item}"
        for item in gate_input.payoff_cooldown_violations
    )
    if gate_input.character_bottom_line_violation:
        failures.append("人物底线冲突且无桥梁")
    return GateReport(
        passed=not failures,
        hard_failures=failures,
        character_fit=character_score,
        style_fit=style_score,
        requires_character_bridge=requires_bridge,
        style_review_required=bool(gate_input.style_boundary_violations),
        soft_warnings=soft_warnings,
    )
