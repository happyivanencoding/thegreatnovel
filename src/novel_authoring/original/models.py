"""Strict contracts for source-free original novel genesis."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.domain.models import NarrativeFunction


class OriginalState(StrEnum):
    ORIGINAL_SEED = "ORIGINAL_SEED"
    READER_EXPERIENCE_REVIEW = "READER_EXPERIENCE_REVIEW"
    CORE_INNOVATION_GENERATING = "CORE_INNOVATION_GENERATING"
    CORE_INNOVATION_REVIEW = "CORE_INNOVATION_REVIEW"
    FOUNDATION_GENERATING = "FOUNDATION_GENERATING"
    FOUNDATION_REVIEW = "FOUNDATION_REVIEW"
    DEVELOPMENT_GENERATING = "DEVELOPMENT_GENERATING"
    DEVELOPMENT_REVIEW = "DEVELOPMENT_REVIEW"
    FOUNDATION_READY = "FOUNDATION_READY"
    FIRST_CHAPTER_DRAFTING = "FIRST_CHAPTER_DRAFTING"
    FIRST_CHAPTER_VALIDATED = "FIRST_CHAPTER_VALIDATED"
    WRITING_READY = "WRITING_READY"


class SettingStrength(StrEnum):
    CORE = "CORE"
    PREFERENCE = "PREFERENCE"
    OPEN = "OPEN"


class FoundationSetting(BaseModel):
    model_config = ConfigDict(extra="forbid")

    setting_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    category: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    strength: SettingStrength


class BookProfileDimensionDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str = Field(min_length=1)
    core_commitments: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class BookProfileDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    worldbuilding: BookProfileDimensionDraft
    characters: BookProfileDimensionDraft
    plot: BookProfileDimensionDraft
    style: BookProfileDimensionDraft
    narrative: BookProfileDimensionDraft
    dialogue: BookProfileDimensionDraft
    pacing: BookProfileDimensionDraft
    themes: BookProfileDimensionDraft
    continuity: BookProfileDimensionDraft


class HiddenTruthCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    confidence: float = Field(default=0.5, ge=0, le=1)


class OriginalBookRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    premise: str = Field(min_length=1)
    genre: str = ""
    tone_style: str = ""
    pov: str = ""
    expected_length: str = ""
    must_include: list[str] = Field(default_factory=list)
    forbidden: list[str] = Field(default_factory=list)
    reference_traits: list[str] = Field(default_factory=list)


class CoreInnovationCandidate(BaseModel):
    """An open semantic mechanism proposal, not a classified innovation type."""

    model_config = ConfigDict(extra="forbid")

    innovation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    one_sentence_hook: str = Field(min_length=1)
    core_mechanism: str = Field(min_length=1)
    protagonist_special_rule: str = Field(min_length=1)
    choice_generation: str = Field(min_length=1)
    progression_generation: str = Field(min_length=1)
    payoff_generation: str = Field(min_length=1)
    limitation: str = Field(min_length=1)
    expansion_grammar: str = Field(min_length=1)
    long_form_capacity: str = Field(min_length=1)
    novelty_source: str = Field(min_length=1)
    repetition_risk: str = Field(min_length=1)
    fit_with_reader_promise: str = Field(min_length=1)


class CoreInnovationProposal(BaseModel):
    """Exactly three open-ended mechanisms sharing the frozen reader kernel."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["core-innovation-v1"] = "core-innovation-v1"
    information_status: Literal["PROPOSAL"] = "PROPOSAL"
    innovation_candidates: list[CoreInnovationCandidate] = Field(min_length=3, max_length=3)
    kernel_contracts: dict[str, Any]

    @model_validator(mode="after")
    def candidates_are_distinct(self) -> CoreInnovationProposal:
        innovation_ids = [item.innovation_id for item in self.innovation_candidates]
        if len(set(innovation_ids)) != 3:
            raise ValueError("Core Innovation 必须恰好包含三个不同候选")
        return self


class AuthorInnovationIntent(BaseModel):
    """The author's selected mechanism boundary carried into later Genesis stages."""

    model_config = ConfigDict(extra="forbid")

    selected_primary_innovation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    optional_mix_notes: str = ""


class FirstPhaseProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selected_foundation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    opening_pressure: str = Field(min_length=1)
    first_concrete_goal: str = Field(min_length=1)
    first_resource_bottleneck: str = Field(min_length=1)
    first_progression_opportunity: str = Field(min_length=1)
    first_payoff: str = Field(min_length=1)
    first_meaningful_escalation: str = Field(min_length=1)
    stage_climax: str = Field(min_length=1)
    after_climax_change: str = Field(min_length=1)


class StoryFoundationCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    core_reading_promise: str = Field(min_length=1)
    protagonist: str = Field(min_length=1)
    protagonist_competence: str = Field(min_length=1)
    protagonist_weakness: str = Field(min_length=1)
    protagonist_goal: str = Field(min_length=1)
    main_conflict: str = Field(min_length=1)
    world_carrier: str = Field(min_length=1)
    first_stage_objective: str = Field(min_length=1)
    risk_structure: str = Field(min_length=1)
    social_configuration: str = Field(min_length=1)
    resource_structure: str = Field(min_length=1)
    premise_relationship: str = Field(min_length=1)
    author_facing_pitch: str = Field(min_length=1)
    opening_situation: str = Field(min_length=1)
    typical_choice: str = Field(min_length=1)
    innovation_fit: str = Field(min_length=1)


class StoryRoute(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    direction: str = Field(min_length=1)
    central_pressure: str = Field(min_length=1)
    opportunity: str = Field(min_length=1)
    risk: str = Field(min_length=1)
    commitments: list[str] = Field(min_length=1)
    open_alternatives: list[str] = Field(default_factory=list)


class FirstChapterCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    opening_situation: str = Field(min_length=1)
    hook: str = Field(min_length=1)
    chapter_goal: str = Field(min_length=1)
    central_choice: str = Field(min_length=1)
    conflict: str = Field(min_length=1)
    protagonist_action: str = Field(min_length=1)
    cost: str = Field(min_length=1)
    irreversible_change: str = Field(min_length=1)
    ending_turn: str = Field(min_length=1)
    distinctiveness: str = Field(min_length=1)
    primary_function: NarrativeFunction = NarrativeFunction.SETUP


class RollingPlanning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    short: list[str] = Field(min_length=1)
    mid: list[str] = Field(min_length=1)
    long: list[str] = Field(min_length=1)


class StoryFoundationProposal(BaseModel):
    """Exactly three story carriers for one selected Core Innovation."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["story-foundation-v1"] = "story-foundation-v1"
    information_status: Literal["PROPOSAL"] = "PROPOSAL"
    core_innovation_intent: AuthorInnovationIntent
    foundation_candidates: list[StoryFoundationCandidate] = Field(min_length=3, max_length=3)
    kernel_contracts: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def candidates_are_distinct(self) -> StoryFoundationProposal:
        ids = [item.candidate_id for item in self.foundation_candidates]
        if len(set(ids)) != 3:
            raise ValueError("Story Foundation 必须恰好包含三个不同候选")
        return self


class FoundationDevelopmentProposal(BaseModel):
    """Long-form development for the author-selected Story Foundation."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["foundation-development-v1"] = "foundation-development-v1"
    information_status: Literal["PROPOSAL"] = "PROPOSAL"
    core_innovation_intent: AuthorInnovationIntent
    selected_foundation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    selected_foundation: StoryFoundationCandidate
    title_candidates: list[str] = Field(min_length=3, max_length=3)
    expanded_premise: str = Field(min_length=1)
    protagonist: str = Field(min_length=1)
    protagonist_goal: str = Field(min_length=1)
    protagonist_conflict: str = Field(min_length=1)
    protagonist_cost: str = Field(min_length=1)
    protagonist_growth: str = Field(min_length=1)
    world_rules: list[str] = Field(min_length=1)
    foundation_settings: list[FoundationSetting] = Field(min_length=1)
    characters: list[str] = Field(min_length=1)
    factions: list[str] = Field(default_factory=list)
    routes: list[StoryRoute] = Field(min_length=3, max_length=3)
    recommended_route_id: str = Field(min_length=1)
    recommendation_reason: str = Field(min_length=1)
    progression_grammar: list[str] = Field(min_length=1)
    expansion_grammar: list[str] = Field(min_length=1)
    payoff_grammar: list[str] = Field(min_length=1)
    first_phase: FirstPhaseProposal
    first_phase_objective: str = Field(min_length=1)
    rolling_planning: RollingPlanning
    book_profile_draft: BookProfileDraft
    first_chapter_candidates: list[FirstChapterCandidate] = Field(min_length=3, max_length=3)
    open_questions: list[str] = Field(default_factory=list)
    hidden_truth_candidates: list[HiddenTruthCandidate] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    avoid_cliches: list[str] = Field(default_factory=list)
    kernel_contracts: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def choices_are_distinct_and_recommendation_exists(
        self,
    ) -> FoundationDevelopmentProposal:
        collections = {
            "标题": self.title_candidates,
            "路线": [item.route_id for item in self.routes],
            "首章": [item.candidate_id for item in self.first_chapter_candidates],
        }
        for label, values in collections.items():
            if len(set(values)) != 3:
                raise ValueError(f"{label}必须恰好包含三个不同候选")
        if self.recommended_route_id not in {item.route_id for item in self.routes}:
            raise ValueError("recommended_route_id 必须指向三条路线之一")
        if self.selected_foundation.candidate_id != self.selected_foundation_id:
            raise ValueError("Development Proposal 的 Foundation 快照与选择不一致")
        if self.first_phase.selected_foundation_id != self.selected_foundation_id:
            raise ValueError("First Phase 必须绑定作者选择的 Story Foundation")
        return self


class OriginalFoundationConfirmation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmed: bool = True
    selected_title: str = Field(min_length=1)
    title_override: str = ""
    selected_foundation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    selected_route_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    protagonist_override: str = ""
    protagonist_goal_override: str = ""
    main_conflict_override: str = ""
    protagonist_cost_override: str = ""
    protagonist_growth_override: str = ""
    first_phase_overrides: dict[str, str] = Field(default_factory=dict)
    characters_override: list[str] = Field(default_factory=list)
    factions_override: list[str] = Field(default_factory=list)
    world_rules: list[str] = Field(min_length=1)
    first_phase_objective: str = Field(min_length=1)
    rolling_short_override: list[str] = Field(default_factory=list)
    rolling_mid_override: list[str] = Field(default_factory=list)
    rolling_long_override: list[str] = Field(default_factory=list)
    setting_strength_overrides: dict[str, SettingStrength] = Field(default_factory=dict)
    open_question_actions: dict[str, Literal["KEEP_OPEN", "TENTATIVE", "SECRET", "DELETE"]] = Field(
        default_factory=dict
    )
    hidden_truth_actions: dict[
        str, Literal["CONFIRM_TRUTH", "KEEP_CANDIDATE", "KEEP_OPEN", "REJECT"]
    ] = Field(default_factory=dict)
    confirm_kernel_contracts: bool = True


class GenesisApplyPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proposal_version_id: str
    selected_title: str
    selected_foundation: dict[str, Any]
    selected_route: dict[str, Any]
    core_innovation_intent: dict[str, Any]
    growth_grammar: dict[str, list[str]]
    first_phase: dict[str, str]
    author_truths: list[dict[str, Any]]
    persistent_directives: list[dict[str, Any]]
    profile_dimensions: dict[str, dict[str, Any]]
    open_questions: list[dict[str, Any]]
    secret_candidates: list[dict[str, Any]]
    narrative_spine: dict[str, Any]
    rolling_planning: dict[str, list[str]]
    main_thread: dict[str, Any]
    first_chapter_candidates: list[dict[str, Any]]


__all__ = [
    "AuthorInnovationIntent",
    "BookProfileDimensionDraft",
    "BookProfileDraft",
    "CoreInnovationCandidate",
    "CoreInnovationProposal",
    "FirstPhaseProposal",
    "FoundationDevelopmentProposal",
    "FoundationSetting",
    "GenesisApplyPlan",
    "HiddenTruthCandidate",
    "FirstChapterCandidate",
    "OriginalBookRequest",
    "OriginalFoundationConfirmation",
    "OriginalState",
    "RollingPlanning",
    "StoryFoundationCandidate",
    "StoryFoundationProposal",
    "StoryRoute",
    "SettingStrength",
]
