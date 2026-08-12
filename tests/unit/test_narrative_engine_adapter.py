from __future__ import annotations

from novel_authoring.serial_kernel import (
    NARRATIVE_ENGINE_REGISTRY,
    EngineImplementationDepth,
    NarrativeDrive,
    NarrativeEngineAdapter,
    NarrativeEngineType,
    ProgressionNarrativeEngineAdapter,
)


def test_progression_engine_is_first_deep_protocol_implementation() -> None:
    adapter = NARRATIVE_ENGINE_REGISTRY.get(NarrativeEngineType.PROGRESSION)

    assert isinstance(adapter, NarrativeEngineAdapter)
    assert adapter is not None
    assert adapter.implementation_depth is EngineImplementationDepth.DEEP
    assert NarrativeDrive.POWER_PROGRESSION in adapter.supported_drives
    assert NARRATIVE_ENGINE_REGISTRY.implementation_depth(
        NarrativeEngineType.CAREER_MASTERY
    ) is EngineImplementationDepth.NOT_IMPLEMENTED_DEEPLY


def test_progression_adapter_reuses_chapter_projection_and_explains_intent() -> None:
    adapter = ProgressionNarrativeEngineAdapter()
    context = {
        "drive": "POWER_PROGRESSION",
        "progression_state": {
            "next_breakthrough_readiness": "MISSING_RESOURCE",
            "missing_resources": ["回声矿晶"],
            "pending_ability_showcases": [],
        },
        "reader_promises": ["身体成长改变行动空间"],
        "debt_ids": ["debt-resource"],
        "evidence": ["chapter-8:source-span-3"],
    }

    state = adapter.build_state(context)
    recommendations = adapter.recommend_intents(context)

    assert state is context["progression_state"]
    assert recommendations[0].intent == "RESOURCE_OPPORTUNITY"
    assert recommendations[0].drive is NarrativeDrive.POWER_PROGRESSION
    assert recommendations[0].debt_ids == ["debt-resource"]
    assert recommendations[0].evidence == ["chapter-8:source-span-3"]


def test_adapter_does_not_create_fake_state_for_unimplemented_context() -> None:
    adapter = ProgressionNarrativeEngineAdapter()

    state = adapter.build_state({})

    assert state["availability"] == "UNKNOWN"
    assert "current_stage" not in state
