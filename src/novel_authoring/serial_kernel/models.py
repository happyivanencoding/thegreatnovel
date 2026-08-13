"""Universal contracts for Chinese serialized webnovels.

Market labels are discovery metadata.  Narrative drives are author-reviewed
planning inputs.  Neither model owns Canon, world state, candidates, payoff,
or narrative debt.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.progression.models import ContractStatus, PayoffChannel


class MarketCategory(StrEnum):
    XUANHUAN = "XUANHUAN"
    XIANXIA = "XIANXIA"
    URBAN = "URBAN"
    SCIENCE_FICTION = "SCIENCE_FICTION"
    FANTASY = "FANTASY"
    HISTORY = "HISTORY"
    WUXIA = "WUXIA"
    GAME = "GAME"
    HIGH_MARTIAL = "HIGH_MARTIAL"
    SUPERNATURAL = "SUPERNATURAL"
    CUSTOM = "CUSTOM"


class NarrativeDrive(StrEnum):
    POWER_PROGRESSION = "POWER_PROGRESSION"
    KNOWLEDGE_PROGRESSION = "KNOWLEDGE_PROGRESSION"
    ABILITY_PROGRESSION = "ABILITY_PROGRESSION"
    BODY_EVOLUTION = "BODY_EVOLUTION"
    SEQUENCE_PROGRESSION = "SEQUENCE_PROGRESSION"
    STATUS_PROGRESSION = "STATUS_PROGRESSION"
    MYSTERY_INVESTIGATION = "MYSTERY_INVESTIGATION"
    MYSTERY_REVELATION = "MYSTERY_REVELATION"
    CAREER_MASTERY = "CAREER_MASTERY"
    CRAFT_PROFESSION = "CRAFT_PROFESSION"
    STATUS_WEALTH = "STATUS_WEALTH"
    STATUS_RISE = "STATUS_RISE"
    TERRITORY_FACTION = "TERRITORY_FACTION"
    POLITICAL_STRATEGY = "POLITICAL_STRATEGY"
    STATE_BUILDING = "STATE_BUILDING"
    COMPETITIVE_SKILL = "COMPETITIVE_SKILL"
    COMPETITIVE_RANK = "COMPETITIVE_RANK"
    SURVIVAL_RESOURCE = "SURVIVAL_RESOURCE"
    BASE_BUILDING = "BASE_BUILDING"
    TEAM_GROWTH = "TEAM_GROWTH"
    RELATIONSHIP_EMOTIONAL = "RELATIONSHIP_EMOTIONAL"
    WORLD_EXPLORATION = "WORLD_EXPLORATION"
    RESOURCE_OPPORTUNITY = "RESOURCE_OPPORTUNITY"
    IDENTITY_PRESSURE = "IDENTITY_PRESSURE"
    COMEDY_EXPECTATION = "COMEDY_EXPECTATION"
    CUSTOM = "CUSTOM"


class NarrativeEngineType(StrEnum):
    PROGRESSION = "PROGRESSION"
    MYSTERY_REVEAL = "MYSTERY_REVEAL"
    CAREER_MASTERY = "CAREER_MASTERY"
    STATUS_WEALTH = "STATUS_WEALTH"
    STRATEGY_STATE_BUILDING = "STRATEGY_STATE_BUILDING"
    COMPETITIVE_SKILL = "COMPETITIVE_SKILL"
    SURVIVAL_RESOURCE = "SURVIVAL_RESOURCE"
    RELATIONSHIP_LIFE = "RELATIONSHIP_LIFE"
    TEAM_FACTION_GROWTH = "TEAM_FACTION_GROWTH"
    CUSTOM = "CUSTOM"


class EngineImplementationDepth(StrEnum):
    DEEP = "DEEP"
    NOT_IMPLEMENTED_DEEPLY = "NOT_IMPLEMENTED_DEEPLY"


class MarketCategoryMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metadata_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    primary_market_category: MarketCategory
    secondary_market_categories: list[MarketCategory] = Field(
        default_factory=list, max_length=4
    )
    display_labels: list[str] = Field(default_factory=list)
    source: str = "AUTHOR_PREMISE_INTERPRETATION"
    status: ContractStatus = ContractStatus.NEEDS_REVIEW

    @model_validator(mode="after")
    def validate_categories(self) -> MarketCategoryMetadata:
        if self.primary_market_category in self.secondary_market_categories:
            raise ValueError("primary market category 不得在 secondary 中重复")
        if len(self.secondary_market_categories) != len(
            set(self.secondary_market_categories)
        ):
            raise ValueError("secondary market categories 不得重复")
        return self


class DriveState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drive: NarrativeDrive
    state: str = "UNKNOWN"
    evidence: list[str] = Field(default_factory=list)


class DrivePayoffChannel(BaseModel):
    """A mapping onto the existing payoff infrastructure."""

    model_config = ConfigDict(extra="forbid")

    channel: PayoffChannel
    associated_drive: NarrativeDrive


class NarrativeDriveContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drive_contract_id: str = Field(pattern=r"^[A-Za-z0-9._-]+$")
    primary_drive: NarrativeDrive
    secondary_drives: list[NarrativeDrive] = Field(
        default_factory=list, min_length=0, max_length=4
    )
    drive_priorities: dict[NarrativeDrive, int]
    drive_promises: dict[NarrativeDrive, list[str]]
    drive_states: list[DriveState] = Field(default_factory=list)
    drive_payoff_channels: list[DrivePayoffChannel] = Field(default_factory=list)
    drive_debt_types: dict[NarrativeDrive, list[str]] = Field(default_factory=dict)
    drive_fatigue_risks: dict[NarrativeDrive, list[str]] = Field(default_factory=dict)
    progression_engine_enabled: bool = False
    author_overrides: list[str] = Field(default_factory=list)
    status: ContractStatus = ContractStatus.NEEDS_REVIEW

    @property
    def drive_mix(self) -> list[NarrativeDrive]:
        return [self.primary_drive, *self.secondary_drives]

    @model_validator(mode="after")
    def validate_drive_mix(self) -> NarrativeDriveContract:
        if self.primary_drive in self.secondary_drives:
            raise ValueError("primary drive 不得在 secondary drives 中重复")
        if len(self.secondary_drives) != len(set(self.secondary_drives)):
            raise ValueError("secondary drives 不得重复")
        missing = [drive for drive in self.drive_mix if drive not in self.drive_priorities]
        if missing:
            raise ValueError(f"drive priorities 缺少：{', '.join(item.value for item in missing)}")
        if any(value < 0 or value > 100 for value in self.drive_priorities.values()):
            raise ValueError("drive priority 必须位于 0..100")
        return self


class NarrativeDriveInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    market_category: MarketCategoryMetadata
    drive_contract: NarrativeDriveContract
    enabled_engines: list[NarrativeEngineType]
    progression_engine_enabled: bool = False
    display_primary_drive: str
    display_secondary_drives: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


PROGRESSION_DRIVES = frozenset(
    {
        NarrativeDrive.POWER_PROGRESSION,
        NarrativeDrive.KNOWLEDGE_PROGRESSION,
        NarrativeDrive.ABILITY_PROGRESSION,
        NarrativeDrive.BODY_EVOLUTION,
        NarrativeDrive.SEQUENCE_PROGRESSION,
        NarrativeDrive.STATUS_PROGRESSION,
    }
)


__all__ = [
    "DrivePayoffChannel",
    "DriveState",
    "EngineImplementationDepth",
    "MarketCategory",
    "MarketCategoryMetadata",
    "NarrativeDrive",
    "NarrativeDriveContract",
    "NarrativeDriveInterpretation",
    "NarrativeEngineType",
    "PROGRESSION_DRIVES",
]
