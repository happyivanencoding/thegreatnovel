from __future__ import annotations

import pytest

from novel_authoring.progression.models import (
    ContractStatus,
    ExperiencePriority,
    ExplanationStyle,
    PrimaryFamily,
    ReaderExperience,
    ReaderExperienceContract,
    SettingSkin,
)


def reader_contract(**overrides: object) -> ReaderExperienceContract:
    payload: dict[str, object] = {
        "contract_id": "reader-near-future-body",
        "primary_family": PrimaryFamily.PROGRESSION_FANTASY,
        "secondary_families": [PrimaryFamily.COSMIC_PROGRESSION],
        "setting_skin": SettingSkin.NEAR_FUTURE,
        "experience_priorities": {
            ReaderExperience.PROGRESSION: ExperiencePriority.VERY_HIGH,
            ReaderExperience.POWER_VERIFICATION: ExperiencePriority.VERY_HIGH,
            ReaderExperience.WORLD_EXPANSION: ExperiencePriority.HIGH,
            ReaderExperience.SOCIAL_THEME: ExperiencePriority.LOW,
        },
        "growth_centrality": ExperiencePriority.VERY_HIGH,
        "world_expansion_centrality": ExperiencePriority.HIGH,
        "mystery_centrality": ExperiencePriority.MEDIUM,
        "team_centrality": ExperiencePriority.LOW,
        "relationship_centrality": ExperiencePriority.MEDIUM,
        "theme_centrality": ExperiencePriority.LOW,
        "explanation_style": ExplanationStyle.MIXED_MYSTICAL,
        "must_deliver": ["成长必须持续扩大行动可能性"],
        "status": ContractStatus.NEEDS_REVIEW,
    }
    payload.update(overrides)
    return ReaderExperienceContract.model_validate(payload)


def test_reader_experience_contract_validates_priorities() -> None:
    contract = reader_contract()

    assert contract.experience_priorities[ReaderExperience.PROGRESSION] is (
        ExperiencePriority.VERY_HIGH
    )
    assert contract.status is ContractStatus.NEEDS_REVIEW


def test_reader_experience_cannot_disable_every_priority() -> None:
    with pytest.raises(ValueError, match="不能全部关闭"):
        reader_contract(
            experience_priorities={
                ReaderExperience.PROGRESSION: ExperiencePriority.OFF,
                ReaderExperience.COMBAT: ExperiencePriority.OFF,
            }
        )


def test_setting_skin_cannot_replace_primary_genre() -> None:
    contract = reader_contract(
        primary_family=PrimaryFamily.PROGRESSION_FANTASY,
        setting_skin=SettingSkin.NEAR_FUTURE,
    )

    assert contract.primary_family is PrimaryFamily.PROGRESSION_FANTASY
    assert contract.setting_skin is SettingSkin.NEAR_FUTURE


def test_primary_family_cannot_be_duplicated_as_secondary() -> None:
    with pytest.raises(ValueError, match="primary_family"):
        reader_contract(
            secondary_families=[
                PrimaryFamily.PROGRESSION_FANTASY,
                PrimaryFamily.COSMIC_PROGRESSION,
            ]
        )
