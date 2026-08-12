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


class GrowthAxisType(StrEnum):
    POWER_STAGE = "POWER_STAGE"
    BODY_EVOLUTION = "BODY_EVOLUTION"
    ABILITY_UNLOCK = "ABILITY_UNLOCK"
    KNOWLEDGE = "KNOWLEDGE"
    CRAFT = "CRAFT"
    EQUIPMENT = "EQUIPMENT"
    BLOODLINE = "BLOODLINE"
    SEQUENCE = "SEQUENCE"
    STATUS = "STATUS"
    TEAM = "TEAM"
    FACTION_AUTHORITY = "FACTION_AUTHORITY"
    CIVILIZATION = "CIVILIZATION"
    TERRITORY = "TERRITORY"
    IDENTITY = "IDENTITY"
    CUSTOM = "CUSTOM"


class BreakthroughGateType(StrEnum):
    ACCUMULATION = "ACCUMULATION"
    RESOURCE_GATE = "RESOURCE_GATE"
    RITUAL_GATE = "RITUAL_GATE"
    INSIGHT_GATE = "INSIGHT_GATE"
    COMBAT_GATE = "COMBAT_GATE"
    BODY_TRANSFORMATION = "BODY_TRANSFORMATION"
    KNOWLEDGE_GATE = "KNOWLEDGE_GATE"
    RELATIONSHIP_GATE = "RELATIONSHIP_GATE"
    STATUS_GATE = "STATUS_GATE"
    SACRIFICE_GATE = "SACRIFICE_GATE"
    CHOICE_GATE = "CHOICE_GATE"
    MIXED = "MIXED"
    CUSTOM = "CUSTOM"


class AbilityUnlockMode(StrEnum):
    STAGE = "STAGE"
    RESOURCE = "RESOURCE"
    COMBAT_INSIGHT = "COMBAT_INSIGHT"
    KNOWLEDGE = "KNOWLEDGE"
    ARTIFACT_OR_EQUIPMENT = "ARTIFACT_OR_EQUIPMENT"
    COMBINATION = "COMBINATION"
    RELATIONSHIP = "RELATIONSHIP"
    STATUS_ACCESS = "STATUS_ACCESS"
    IRREVERSIBLE_CHOICE = "IRREVERSIBLE_CHOICE"
    CUSTOM = "CUSTOM"


class UpperCeilingVisibility(StrEnum):
    VISIBLE = "VISIBLE"
    PARTIAL = "PARTIAL"
    HINTED = "HINTED"
    UNKNOWN = "UNKNOWN"


class StageStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    LOCKED = "LOCKED"
    UNKNOWN = "UNKNOWN"
    RETIRED = "RETIRED"


class ProgressionStageDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    name: str = Field(min_length=1)
    order: int | None = Field(default=None, ge=0)
    reader_visible: bool = True
    entry_requirements: list[str] = Field(default_factory=list)
    typical_capabilities: list[str] = Field(default_factory=list)
    typical_costs: list[str] = Field(default_factory=list)
    validation_expectations: list[str] = Field(default_factory=list)
    next_stage_candidates: list[str] = Field(default_factory=list)
    status: StageStatus = StageStatus.AVAILABLE


class GrowthAxis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    axis_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    name: str = Field(min_length=1)
    axis_type: GrowthAxisType
    current_stage_schema: str = Field(min_length=1)
    stage_order: list[str] = Field(default_factory=list)
    stage_definitions: list[ProgressionStageDefinition] = Field(default_factory=list)
    progress_measure: str = Field(min_length=1)
    unlock_effects: list[str] = Field(default_factory=list)
    costs: list[str] = Field(default_factory=list)
    bottlenecks: list[str] = Field(default_factory=list)
    evidence_requirements: list[str] = Field(default_factory=list)
    visibility: UpperCeilingVisibility = UpperCeilingVisibility.PARTIAL

    @model_validator(mode="after")
    def validate_stage_graph(self) -> GrowthAxis:
        stage_ids = [stage.stage_id for stage in self.stage_definitions]
        if len(stage_ids) != len(set(stage_ids)):
            raise ValueError("Growth Axis 的 stage_id 不得重复")
        if self.stage_order and (
            len(self.stage_order) != len(set(self.stage_order))
            or set(self.stage_order) != set(stage_ids)
        ):
            raise ValueError("stage_order 必须恰好覆盖唯一的 stage definitions")
        missing = sorted(
            {
                target
                for stage in self.stage_definitions
                for target in stage.next_stage_candidates
                if target not in set(stage_ids)
            }
        )
        if missing:
            raise ValueError(f"next_stage_candidates 引用了未知阶段：{missing}")
        return self


class BreakthroughGate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    gate_type: BreakthroughGateType
    requirement: str = Field(min_length=1)
    evidence_requirements: list[str] = Field(min_length=1)
    required_resources: list[str] = Field(default_factory=list)
    irreversible: bool = False


class BreakthroughModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gates: list[BreakthroughGate] = Field(min_length=1)
    all_gates_required: bool = True


class AbilityUnlockRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unlock_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    mode: AbilityUnlockMode
    condition: str = Field(min_length=1)
    effect: str = Field(min_length=1)
    provenance_required: bool = True


class ProgressionContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    progression_contract_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    progression_subject: ProgressionSubject
    primary_axis: GrowthAxis
    secondary_axes: list[GrowthAxis] = Field(default_factory=list)
    topology: list[ProgressionTopology] = Field(min_length=1, max_length=3)
    allowed_delta_types: list[ProgressionDeltaType] = Field(min_length=1)
    stage_model: str = Field(min_length=1)
    breakthrough_model: BreakthroughModel
    ability_unlock_model: list[AbilityUnlockRule] = Field(default_factory=list)
    resource_economy: list[str] = Field(default_factory=list)
    artifact_or_equipment_model: list[str] = Field(default_factory=list)
    growth_costs: list[str] = Field(default_factory=list)
    verification_modes: list[str] = Field(min_length=1)
    status_rise_model: str = ""
    next_ceiling_model: str = Field(min_length=1)
    upper_ceiling_visibility: UpperCeilingVisibility
    progression_promises: list[str] = Field(min_length=1)
    author_constraints: list[str] = Field(default_factory=list)
    effective_from_boundary: int | None = Field(default=None, ge=0)
    status: ContractStatus = ContractStatus.NEEDS_REVIEW

    @model_validator(mode="after")
    def axes_and_topology_are_consistent(self) -> ProgressionContract:
        axes = [self.primary_axis, *self.secondary_axes]
        axis_ids = [axis.axis_id for axis in axes]
        if len(axis_ids) != len(set(axis_ids)):
            raise ValueError("Progression Contract 的 axis_id 不得重复")
        if (
            ProgressionTopology.MULTI_AXIS in self.topology
            and not self.secondary_axes
        ):
            raise ValueError("MULTI_AXIS topology 至少需要一个 secondary axis")
        return self


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
