"""Story profiles that compile to author-reviewable contract proposals."""

from __future__ import annotations

from collections.abc import Mapping

from novel_authoring.progression.models import (
    AuthoringPreset,
    ContractStatus,
    ExperiencePriority,
    PrimaryFamily,
    ReaderExperience,
    ReaderExperienceContract,
    SettingSkin,
    StoryProfile,
)

CHINESE_MALE_COMMERCIAL_PROGRESSION = StoryProfile(
    profile_id=AuthoringPreset.CHINESE_MALE_COMMERCIAL_PROGRESSION,
    label="中文商业成长长篇",
    experience_defaults={
        ReaderExperience.PROGRESSION: ExperiencePriority.VERY_HIGH,
        ReaderExperience.BREAKTHROUGH: ExperiencePriority.HIGH,
        ReaderExperience.POWER_VERIFICATION: ExperiencePriority.HIGH,
        ReaderExperience.RESOURCE_OPPORTUNITY: ExperiencePriority.HIGH,
        ReaderExperience.WORLD_EXPANSION: ExperiencePriority.HIGH,
        ReaderExperience.EXPLORATION: ExperiencePriority.HIGH,
        ReaderExperience.FACTION_CONFLICT: ExperiencePriority.MEDIUM,
        ReaderExperience.MYSTERY: ExperiencePriority.MEDIUM,
        ReaderExperience.RELATIONSHIP: ExperiencePriority.MEDIUM,
        ReaderExperience.SOCIAL_THEME: ExperiencePriority.LOW,
    },
    growth_centrality=ExperiencePriority.VERY_HIGH,
    world_expansion_centrality=ExperiencePriority.HIGH,
    mystery_centrality=ExperiencePriority.MEDIUM,
    team_centrality=ExperiencePriority.MEDIUM,
    relationship_centrality=ExperiencePriority.MEDIUM,
    theme_centrality=ExperiencePriority.LOW,
    must_deliver_defaults=[
        "成长持续扩大叙事主体能够采取的行动",
        "关键成长拥有可观察的验证空间",
        "已获得成果在更大世界中继续有效",
    ],
    drift_guard_defaults=["不得让世界外壳取代成长型核心阅读体验"],
)


BUILTIN_STORY_PROFILES: dict[AuthoringPreset, StoryProfile] = {
    CHINESE_MALE_COMMERCIAL_PROGRESSION.profile_id: CHINESE_MALE_COMMERCIAL_PROGRESSION,
}


def compile_story_profile(
    profile: StoryProfile,
    *,
    contract_id: str,
    primary_family: PrimaryFamily,
    setting_skin: SettingSkin,
    priority_overrides: Mapping[ReaderExperience, ExperiencePriority] | None = None,
    must_deliver: list[str] | None = None,
    must_not_drift_into: list[str] | None = None,
) -> ReaderExperienceContract:
    """Compile defaults to a proposal without carrying preset identity into runtime."""

    priorities = dict(profile.experience_defaults)
    priorities.update(priority_overrides or {})
    return ReaderExperienceContract(
        contract_id=contract_id,
        primary_family=primary_family,
        setting_skin=setting_skin,
        experience_priorities=priorities,
        mysticism_level=profile.mysticism_level,
        explanation_style=profile.explanation_style,
        growth_centrality=profile.growth_centrality,
        world_expansion_centrality=profile.world_expansion_centrality,
        mystery_centrality=profile.mystery_centrality,
        team_centrality=profile.team_centrality,
        relationship_centrality=profile.relationship_centrality,
        theme_centrality=profile.theme_centrality,
        must_deliver=must_deliver or profile.must_deliver_defaults,
        must_not_drift_into=must_not_drift_into or profile.drift_guard_defaults,
        status=ContractStatus.NEEDS_REVIEW,
    )


__all__ = [
    "BUILTIN_STORY_PROFILES",
    "CHINESE_MALE_COMMERCIAL_PROGRESSION",
    "compile_story_profile",
]
