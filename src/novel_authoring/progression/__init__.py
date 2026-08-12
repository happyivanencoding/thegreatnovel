"""Progression Webnovel Kernel public contracts."""

from novel_authoring.progression.adapters import (
    BUILTIN_GENRE_ADAPTERS,
    compile_genre_adapters,
    effective_genre_contract,
)
from novel_authoring.progression.models import (
    AuthoringPreset,
    ContractStatus,
    EffectiveGenreContract,
    ExperiencePriority,
    ExplanationStyle,
    GenreAdapter,
    GenreAdapterKind,
    GenreContract,
    GenrePromise,
    GenrePromiseStrength,
    PayoffChannel,
    PrimaryFamily,
    ReaderExperience,
    ReaderExperienceContract,
    RuntimeGenreCapabilities,
    SerialForm,
    SettingSkin,
    StoryProfile,
)
from novel_authoring.progression.presets import (
    BUILTIN_STORY_PROFILES,
    compile_story_profile,
)

__all__ = [
    "AuthoringPreset",
    "BUILTIN_STORY_PROFILES",
    "BUILTIN_GENRE_ADAPTERS",
    "ContractStatus",
    "EffectiveGenreContract",
    "ExperiencePriority",
    "ExplanationStyle",
    "GenreAdapter",
    "GenreAdapterKind",
    "GenreContract",
    "GenrePromise",
    "GenrePromiseStrength",
    "PayoffChannel",
    "PrimaryFamily",
    "ReaderExperience",
    "ReaderExperienceContract",
    "RuntimeGenreCapabilities",
    "SerialForm",
    "SettingSkin",
    "StoryProfile",
    "compile_story_profile",
    "compile_genre_adapters",
    "effective_genre_contract",
]
