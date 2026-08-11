"""Strict contracts for source-free original novel genesis."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.domain.models import NarrativeFunction


class OriginalState(StrEnum):
    ORIGINAL_SEED = "ORIGINAL_SEED"
    BOOTSTRAP_READY = "BOOTSTRAP_READY"
    FOUNDATION_ACCEPTED = "FOUNDATION_ACCEPTED"
    FIRST_CHAPTER_DRAFTING = "FIRST_CHAPTER_DRAFTING"
    FIRST_CHAPTER_VALIDATED = "FIRST_CHAPTER_VALIDATED"
    WRITING = "WRITING"


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


class StoryFoundationCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    core_reading_promise: str = Field(min_length=1)
    protagonist: str = Field(min_length=1)
    protagonist_goal: str = Field(min_length=1)
    main_conflict: str = Field(min_length=1)
    world_mechanism: str = Field(min_length=1)
    growth_loop: str = Field(min_length=1)
    long_term_possibility: str = Field(min_length=1)
    risk: str = Field(min_length=1)
    premise_relationship: str = Field(min_length=1)


class StoryRoute(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    title: str = Field(min_length=1)
    direction: str = Field(min_length=1)
    central_pressure: str = Field(min_length=1)
    opportunity: str = Field(min_length=1)
    risk: str = Field(min_length=1)


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


class OriginalBootstrapProposal(BaseModel):
    """A proposal-only semantic package produced by the desktop handoff."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["original-bootstrap-v1"] = "original-bootstrap-v1"
    information_status: Literal["PROPOSAL"] = "PROPOSAL"
    title_candidates: list[str] = Field(min_length=3, max_length=3)
    expanded_premise: str = Field(min_length=1)
    foundation_candidates: list[StoryFoundationCandidate] = Field(
        min_length=3, max_length=3
    )
    protagonist: str = Field(min_length=1)
    protagonist_goal: str = Field(min_length=1)
    protagonist_conflict: str = Field(min_length=1)
    protagonist_cost: str = Field(min_length=1)
    protagonist_growth: str = Field(min_length=1)
    world_rules: list[str] = Field(min_length=1)
    characters: list[str] = Field(min_length=1)
    factions: list[str] = Field(default_factory=list)
    routes: list[StoryRoute] = Field(min_length=3, max_length=3)
    recommended_route_id: str = Field(min_length=1)
    recommendation_reason: str = Field(min_length=1)
    first_phase_objective: str = Field(min_length=1)
    rolling_planning: RollingPlanning
    first_chapter_candidates: list[FirstChapterCandidate] = Field(
        min_length=3, max_length=3
    )
    open_questions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    avoid_cliches: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def choices_are_distinct_and_recommendation_exists(self) -> OriginalBootstrapProposal:
        collections = {
            "标题": self.title_candidates,
            "基础框架": [item.candidate_id for item in self.foundation_candidates],
            "路线": [item.route_id for item in self.routes],
            "首章": [item.candidate_id for item in self.first_chapter_candidates],
        }
        for label, values in collections.items():
            if len(set(values)) != 3:
                raise ValueError(f"{label}必须恰好包含三个不同候选")
        if self.recommended_route_id not in {item.route_id for item in self.routes}:
            raise ValueError("recommended_route_id 必须指向三条路线之一")
        return self


class OriginalFoundationConfirmation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmation: str
    selected_title: str = Field(min_length=1)
    title_override: str = ""
    selected_foundation_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    selected_route_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    protagonist_override: str = ""
    protagonist_goal_override: str = ""
    main_conflict_override: str = ""
    protagonist_cost_override: str = ""
    protagonist_growth_override: str = ""
    characters_override: list[str] = Field(default_factory=list)
    factions_override: list[str] = Field(default_factory=list)
    world_rules: list[str] = Field(min_length=1)
    first_phase_objective: str = Field(min_length=1)
    rolling_short_override: list[str] = Field(default_factory=list)
    rolling_mid_override: list[str] = Field(default_factory=list)
    rolling_long_override: list[str] = Field(default_factory=list)


FOUNDATION_CONFIRMATION = "确认基础框架"


__all__ = [
    "FOUNDATION_CONFIRMATION",
    "FirstChapterCandidate",
    "OriginalBookRequest",
    "OriginalBootstrapProposal",
    "OriginalFoundationConfirmation",
    "OriginalState",
    "RollingPlanning",
    "StoryFoundationCandidate",
    "StoryRoute",
]
