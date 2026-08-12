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


class GenrePromiseStrength(StrEnum):
    CORE = "CORE"
    IMPORTANT = "IMPORTANT"
    OPTIONAL = "OPTIONAL"
    DISABLED = "DISABLED"


class GenreAdapterKind(StrEnum):
    CULTIVATION_ESCALATION = "CULTIVATION_ESCALATION"
    ABILITY_UNLOCK_TEAM = "ABILITY_UNLOCK_TEAM"
    MYTHIC_BODY_ANCIENT_WORLD = "MYTHIC_BODY_ANCIENT_WORLD"
    COSMIC_PROGRESSION = "COSMIC_PROGRESSION"
    EVOLUTION_APOCALYPSE = "EVOLUTION_APOCALYPSE"
    OCCULT_SEQUENCE_MYSTERY = "OCCULT_SEQUENCE_MYSTERY"
    SURVIVAL_RESOURCE_PROGRESSION = "SURVIVAL_RESOURCE_PROGRESSION"
    CUSTOM = "CUSTOM"


class PayoffChannel(StrEnum):
    POWER_BREAKTHROUGH = "POWER_BREAKTHROUGH"
    NEW_ABILITY = "NEW_ABILITY"
    NEW_TECHNIQUE = "NEW_TECHNIQUE"
    NEW_ARTIFACT = "NEW_ARTIFACT"
    RESOURCE_GAIN = "RESOURCE_GAIN"
    COMBAT_DOMINANCE = "COMBAT_DOMINANCE"
    UNDERDOG_VICTORY = "UNDERDOG_VICTORY"
    STATUS_RISE = "STATUS_RISE"
    RANKING_RISE = "RANKING_RISE"
    RECOGNITION = "RECOGNITION"
    REVENGE = "REVENGE"
    MYSTERY_REVEAL = "MYSTERY_REVEAL"
    WORLD_EXPANSION = "WORLD_EXPANSION"
    FACTION_ADVANCE = "FACTION_ADVANCE"
    TEAM_GROWTH = "TEAM_GROWTH"
    RELATIONSHIP_ADVANCE = "RELATIONSHIP_ADVANCE"
    WEALTH_GAIN = "WEALTH_GAIN"
    SURVIVAL_ESCAPE = "SURVIVAL_ESCAPE"
    KNOWLEDGE_GAIN = "KNOWLEDGE_GAIN"
    MASTERY = "MASTERY"
    DISCOVERY = "DISCOVERY"
    TRANSFORMATION = "TRANSFORMATION"
    STRATEGIC_ADVANTAGE = "STRATEGIC_ADVANTAGE"
    CUSTOM = "CUSTOM"


class ProgressionSubject(StrEnum):
    CHARACTER = "CHARACTER"
    MULTIPLE_CHARACTERS = "MULTIPLE_CHARACTERS"
    TEAM = "TEAM"
    FACTION = "FACTION"
    SETTLEMENT = "SETTLEMENT"
    ORGANIZATION = "ORGANIZATION"
    CIVILIZATION = "CIVILIZATION"
    COLLECTIVE = "COLLECTIVE"
    WORLD = "WORLD"
    HYBRID = "HYBRID"
    CUSTOM = "CUSTOM"


class ProgressionTopology(StrEnum):
    LINEAR = "LINEAR"
    MULTI_AXIS = "MULTI_AXIS"
    BRANCHING = "BRANCHING"
    NETWORK = "NETWORK"
    TRANSFORMATIVE = "TRANSFORMATIVE"
    CYCLICAL = "CYCLICAL"
    ACCUMULATIVE = "ACCUMULATIVE"
    TRADEOFF = "TRADEOFF"
    CUSTOM = "CUSTOM"


class ProgressionDeltaType(StrEnum):
    ADVANCE = "ADVANCE"
    UNLOCK = "UNLOCK"
    BRANCH = "BRANCH"
    CONVERT = "CONVERT"
    SACRIFICE = "SACRIFICE"
    REGRESS = "REGRESS"
    REBUILD = "REBUILD"
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    LOCK_OUT = "LOCK_OUT"
    TRANSFORM = "TRANSFORM"
    TRANSFER = "TRANSFER"
    CUSTOM = "CUSTOM"


class RuntimeGenreCapabilities(BaseModel):
    """Adapter-neutral structural capabilities consumed by runtime services."""

    model_config = ConfigDict(extra="forbid")

    has_progression_axis: bool = False
    has_stage_transition: bool = False
    has_resource_gate: bool = False
    has_knowledge_gate: bool = False
    has_ability_unlock: bool = False
    has_verification_requirement: bool = False
    has_status_progression: bool = False
    has_world_expansion: bool = False
    has_mystery_binding: bool = False
    has_team_progression: bool = False


class GenrePromise(BaseModel):
    model_config = ConfigDict(extra="forbid")

    promise_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    statement: str = Field(min_length=1)
    strength: GenrePromiseStrength


class GenreAdapter(BaseModel):
    """A proposal generator.  Its identity must not enter effective runtime."""

    model_config = ConfigDict(extra="forbid")

    adapter_id: GenreAdapterKind
    label: str = Field(min_length=1)
    capabilities: RuntimeGenreCapabilities
    expected_payoff_channels: list[PayoffChannel] = Field(default_factory=list)
    genre_native_scene_types: list[str] = Field(default_factory=list)
    genre_native_resource_types: list[str] = Field(default_factory=list)
    genre_native_conflicts: list[str] = Field(default_factory=list)
    drift_risks: list[str] = Field(default_factory=list)


class DerivedAdapterSpec(BaseModel):
    """Author-reviewable structural interpretation for an unknown grammar."""

    model_config = ConfigDict(extra="forbid")

    spec_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    progression_subject: ProgressionSubject
    growth_object: str = Field(min_length=1)
    progression_topology: list[ProgressionTopology] = Field(min_length=1, max_length=3)
    delta_types: list[ProgressionDeltaType] = Field(min_length=1)
    growth_resources: list[str] = Field(default_factory=list)
    growth_gates: list[str] = Field(default_factory=list)
    growth_costs: list[str] = Field(default_factory=list)
    verification_modes: list[str] = Field(min_length=1)
    unlock_logic: str = Field(min_length=1)
    world_expansion_relation: str = Field(min_length=1)
    reader_visible_progress: list[str] = Field(min_length=1)
    long_term_ceiling_logic: str = Field(min_length=1)
    payoff_logic: list[str] = Field(min_length=1)
    capabilities: RuntimeGenreCapabilities
    payoff_channels: list[PayoffChannel] = Field(min_length=1)
    status: ContractStatus = ContractStatus.NEEDS_REVIEW


class GenreContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    genre_contract_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    primary_genre: PrimaryFamily
    subgenres: list[PrimaryFamily] = Field(default_factory=list)
    reader_experience_contract_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    genre_promises: list[GenrePromise] = Field(min_length=1)
    genre_native_engines: list[str] = Field(default_factory=list)
    expected_payoff_channels: list[PayoffChannel] = Field(default_factory=list)
    expected_progression_shape: list[str] = Field(default_factory=list)
    world_expansion_expectation: str = ""
    genre_native_scene_types: list[str] = Field(default_factory=list)
    genre_native_resource_types: list[str] = Field(default_factory=list)
    genre_native_conflicts: list[str] = Field(default_factory=list)
    genre_drift_risks: list[str] = Field(default_factory=list)
    forbidden_drift_patterns: list[str] = Field(default_factory=list)
    author_overrides: list[str] = Field(default_factory=list)
    capabilities: RuntimeGenreCapabilities
    status: ContractStatus = ContractStatus.NEEDS_REVIEW


class EffectiveGenreContract(BaseModel):
    """Adapter-free contract shape consumed by runtime services."""

    model_config = ConfigDict(extra="forbid")

    genre_contract_id: str
    reader_experience_contract_id: str
    promises: list[GenrePromise]
    payoff_channels: list[PayoffChannel]
    capabilities: RuntimeGenreCapabilities
    world_expansion_expectation: str = ""
    forbidden_drift_patterns: list[str] = Field(default_factory=list)


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
