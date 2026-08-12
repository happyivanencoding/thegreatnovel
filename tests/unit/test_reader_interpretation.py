from novel_authoring.progression.interpretation import (
    ReaderExperienceAdjustment,
    adjust_reader_experience,
    apply_reader_experience_overrides,
    compile_kernel_contract_proposals,
    interpret_reader_experience,
)
from novel_authoring.progression.models import (
    ExperiencePriority,
    GenreAdapterKind,
    ProgressionSubject,
    ReaderExperience,
)
from novel_authoring.serial_kernel.classification import (
    align_narrative_drive_to_reader_experience,
)


def test_near_future_body_seed_is_growth_first() -> None:
    value = interpret_reader_experience(
        "近未来的气修修仙小说，体修成神的故事。",
        contract_prefix="body-seed",
    )

    assert value.primary_adapter is GenreAdapterKind.MYTHIC_BODY_ANCIENT_WORLD
    assert value.reader_contract.setting_skin.value == "NEAR_FUTURE"
    assert (
        value.reader_contract.experience_priorities[ReaderExperience.PROGRESSION]
        is ExperiencePriority.VERY_HIGH
    )
    assert (
        value.reader_contract.experience_priorities[ReaderExperience.SOCIAL_THEME]
        is ExperiencePriority.LOW
    )
    bundle = compile_kernel_contract_proposals(value)
    assert bundle.progression.primary_axis.name.startswith("体修")
    assert bundle.genre.status.value == "NEEDS_REVIEW"


def test_reader_experience_without_specialized_evidence_uses_normal_defaults() -> None:
    value = interpret_reader_experience("一个人寻找失踪姐姐的故事。")

    assert value.narrative_drive.drive_contract.primary_drive.value == "CUSTOM"
    assert set(value.reader_contract.experience_priorities.values()) == {
        ExperiencePriority.MEDIUM
    }


def test_reader_strength_override_reaches_existing_narrative_drive_proposal() -> None:
    value = interpret_reader_experience("一个人寻找失踪姐姐的故事。")
    adjusted = apply_reader_experience_overrides(
        value.reader_contract,
        {
            "RESOURCE_OPPORTUNITY": ExperiencePriority.VERY_HIGH,
            "MYSTERY": ExperiencePriority.HIGH,
        },
    )
    aligned = align_narrative_drive_to_reader_experience(value.narrative_drive, adjusted)

    assert adjusted.experience_priorities[ReaderExperience.RESOURCE_OPPORTUNITY] is (
        ExperiencePriority.VERY_HIGH
    )
    assert aligned.drive_contract.primary_drive.value == "RESOURCE_OPPORTUNITY"
    assert "MYSTERY_INVESTIGATION" in {
        item.value for item in aligned.drive_contract.secondary_drives
    }


def test_reader_adjustment_is_author_review_before_contracts() -> None:
    value = interpret_reader_experience(
        "近未来的气修修仙小说，体修成神的故事。"
    )
    adjusted = adjust_reader_experience(
        value.reader_contract,
        ReaderExperienceAdjustment.PAYOFF_STRONGER,
    )

    assert (
        adjusted.experience_priorities[ReaderExperience.COMBAT]
        is ExperiencePriority.VERY_HIGH
    )
    assert adjusted.status.value == "NEEDS_REVIEW"


def test_ood_city_seed_compiles_without_character_level_assumption() -> None:
    value = interpret_reader_experience(
        "一座城市本身是成长主体。每当居民共同解决一种此前无法解决的问题，城市就会获得一条新的自然法则。",
        contract_prefix="city-seed",
    )
    bundle = compile_kernel_contract_proposals(value)

    assert value.derived_adapter_spec is not None
    assert value.progression_subject is ProgressionSubject.SETTLEMENT
    assert bundle.progression.progression_subject is ProgressionSubject.SETTLEMENT
    generated_structure = str(
        {
            "axis": bundle.progression.primary_axis.model_dump(mode="json"),
            "resources": bundle.progression.resource_economy,
            "world": [
                stage.model_dump(mode="json")
                for stage in bundle.world_expansion.stages
            ],
        }
    )
    assert all(word not in generated_structure for word in ("宗门", "秘境", "学院", "擂台"))


def test_ood_knowledge_seed_disables_combat_priority() -> None:
    value = interpret_reader_experience(
        "主角没有战斗能力。他每真正理解一种已经灭亡的语言，就能进入那个文明曾经理解过的现实层。",
        contract_prefix="language-seed",
    )
    bundle = compile_kernel_contract_proposals(value)

    assert value.derived_adapter_spec is not None
    assert (
        value.reader_contract.experience_priorities[ReaderExperience.COMBAT]
        is ExperiencePriority.OFF
    )
    assert bundle.genre.capabilities.has_knowledge_gate is True
    assert bundle.genre.capabilities.has_world_expansion is True
