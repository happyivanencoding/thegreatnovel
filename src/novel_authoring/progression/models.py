"""Typed contracts for the Progression Webnovel Kernel.

These models describe author-reviewed promises.  They do not own Canon,
runtime world state, candidate selection, or author truth.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractStatus(StrEnum):
    INFERRED_PROPOSAL = "INFERRED_PROPOSAL"
    SOFT_REFERENCE = "SOFT_REFERENCE"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    EFFECTIVE = "EFFECTIVE"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class ExperiencePriority(StrEnum):
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    OFF = "OFF"


class PrimaryFamily(StrEnum):
    PROGRESSION_FANTASY = "PROGRESSION_FANTASY"
    MYSTERY_PROGRESSION = "MYSTERY_PROGRESSION"
    SURVIVAL_PROGRESSION = "SURVIVAL_PROGRESSION"
    TEAM_PROGRESSION = "TEAM_PROGRESSION"
    COSMIC_PROGRESSION = "COSMIC_PROGRESSION"
    EVOLUTION_PROGRESSION = "EVOLUTION_PROGRESSION"
    CIVILIZATION_PROGRESSION = "CIVILIZATION_PROGRESSION"
    CUSTOM = "CUSTOM"


class ReaderExperience(StrEnum):
    PROGRESSION = "PROGRESSION"
    BREAKTHROUGH = "BREAKTHROUGH"
    POWER_VERIFICATION = "POWER_VERIFICATION"
    COMBAT = "COMBAT"
    EXPLORATION = "EXPLORATION"
    RESOURCE_OPPORTUNITY = "RESOURCE_OPPORTUNITY"
    ARTIFACT_OR_ABILITY = "ARTIFACT_OR_ABILITY"
    WORLD_EXPANSION = "WORLD_EXPANSION"
    FACTION_CONFLICT = "FACTION_CONFLICT"
    MYSTERY = "MYSTERY"
    REVEAL = "REVEAL"
    TEAM_GROWTH = "TEAM_GROWTH"
    RELATIONSHIP = "RELATIONSHIP"
    ROMANCE = "ROMANCE"
    STATUS_RISE = "STATUS_RISE"
    REVENGE = "REVENGE"
    SURVIVAL = "SURVIVAL"
    KNOWLEDGE = "KNOWLEDGE"
    WEALTH = "WEALTH"
    SOCIAL_THEME = "SOCIAL_THEME"


class SettingSkin(StrEnum):
    ANCIENT_FANTASY = "ANCIENT_FANTASY"
    OTHERWORLD = "OTHERWORLD"
    MODERN_CITY = "MODERN_CITY"
    NEAR_FUTURE = "NEAR_FUTURE"
    APOCALYPSE = "APOCALYPSE"
    COSMIC = "COSMIC"
    STEAMPUNK = "STEAMPUNK"
    CUSTOM = "CUSTOM"


class SerialForm(StrEnum):
    LONG_SERIAL = "LONG_SERIAL"
    SEASONAL_SERIAL = "SEASONAL_SERIAL"
    OPEN_ENDED_SERIAL = "OPEN_ENDED_SERIAL"
    CUSTOM = "CUSTOM"


class ExplanationStyle(StrEnum):
    MYSTICAL = "MYSTICAL"
    MIXED_MYSTICAL = "MIXED_MYSTICAL"
    BALANCED = "BALANCED"
    MIXED_HARD = "MIXED_HARD"
    HARD_EXPLANATION = "HARD_EXPLANATION"


class AuthoringPreset(StrEnum):
    CHINESE_MALE_COMMERCIAL_PROGRESSION = "CHINESE_MALE_COMMERCIAL_PROGRESSION"
    SURVIVAL_PROGRESSION = "SURVIVAL_PROGRESSION"
    MYSTERY_PROGRESSION = "MYSTERY_PROGRESSION"
    TEAM_PROGRESSION = "TEAM_PROGRESSION"
    CIVILIZATION_PROGRESSION = "CIVILIZATION_PROGRESSION"
    CUSTOM_AUTHOR_PROFILE = "CUSTOM_AUTHOR_PROFILE"


class StoryProfile(BaseModel):
    """Author-facing defaults used to propose, never enforce, a contract."""

    model_config = ConfigDict(extra="forbid")

    profile_id: AuthoringPreset
    label: str = Field(min_length=1)
    experience_defaults: dict[ReaderExperience, ExperiencePriority]
    growth_centrality: ExperiencePriority
    world_expansion_centrality: ExperiencePriority
    mystery_centrality: ExperiencePriority
    team_centrality: ExperiencePriority
    relationship_centrality: ExperiencePriority
    theme_centrality: ExperiencePriority
    mysticism_level: ExperiencePriority = ExperiencePriority.MEDIUM
    explanation_style: ExplanationStyle = ExplanationStyle.BALANCED
    must_deliver_defaults: list[str] = Field(min_length=1)
    drift_guard_defaults: list[str] = Field(default_factory=list)


class ReaderExperienceContract(BaseModel):
    """The reader-facing promise confirmed before story-foundation generation."""

    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    primary_family: PrimaryFamily
    secondary_families: list[PrimaryFamily] = Field(default_factory=list, max_length=3)
    setting_skin: SettingSkin
    serial_form: SerialForm = SerialForm.LONG_SERIAL
    experience_priorities: dict[ReaderExperience, ExperiencePriority]
    mysticism_level: ExperiencePriority = ExperiencePriority.MEDIUM
    explanation_style: ExplanationStyle = ExplanationStyle.BALANCED
    growth_centrality: ExperiencePriority
    world_expansion_centrality: ExperiencePriority
    mystery_centrality: ExperiencePriority
    team_centrality: ExperiencePriority
    relationship_centrality: ExperiencePriority
    theme_centrality: ExperiencePriority
    tone: list[str] = Field(default_factory=list)
    must_deliver: list[str] = Field(min_length=1)
    must_not_drift_into: list[str] = Field(default_factory=list)
    author_notes: str = ""
    status: ContractStatus = ContractStatus.NEEDS_REVIEW

    @model_validator(mode="after")
    def validate_reader_promise(self) -> ReaderExperienceContract:
        if self.primary_family in self.secondary_families:
            raise ValueError("primary_family 不得重复出现在 secondary_families")
        if len(self.secondary_families) != len(set(self.secondary_families)):
            raise ValueError("secondary_families 不得重复")
        if not self.experience_priorities:
            raise ValueError("必须至少定义一个阅读体验优先级")
        if all(value is ExperiencePriority.OFF for value in self.experience_priorities.values()):
            raise ValueError("阅读体验优先级不能全部关闭")
        return self
