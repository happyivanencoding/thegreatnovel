from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(r"C:\dev\tgn-story-mvp")
sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    ActionSurfaceRegistry,
    AtomicAuthorityContract,
    AtomicAuthorityContractBuilder,
    AtomicRoutingPolicy,
    AuthorityFact,
    AuthoritySource,
    ContractGateResult,
    DirectorStructuredDecision,
    EntityKind,
    EntityRecord,
    EntityRegistry,
    FactEvidenceBinding,
    FactKind,
    FactMode,
    FactPhase,
    FinalRoute,
    FrozenAuthorityArtifact,
    IRValidationError,
    NarrativeFunctionRegistry,
    PatchKind,
    PatchOperation,
    PreflightRoute,
    PrimaryPreservationMap,
    PreservationProvenance,
    ProtectionHint,
    RepairTarget,
    SourcePurityError,
    bind_primary_realization,
    build_primary_preservation_map,
    expand_compact_mission_sidecar,
    expand_micro_mission_sidecar,
    freeze_canon_artifact,
    freeze_human_artifact,
    freeze_mission_artifact,
    freeze_power_artifact,
    freeze_reader_release_artifact,
    freeze_world_artifact,
    validate_primary_preservation,
)


def registry(*, chapter_id: str = "BOOK_A:CH001") -> EntityRegistry:
    entities = {
        "PROTAGONIST_001": EntityRecord(
            entity_id="PROTAGONIST_001",
            kind=EntityKind.CHARACTER,
            display_name="顾停舟",
            aliases=("他", "本体", "少年"),
            authority_refs=("character.entity.PROTAGONIST_001",),
        ),
        "CLONE_001": EntityRecord(
            entity_id="CLONE_001",
            kind=EntityKind.MANIFESTATION,
            display_name="分身",
            aliases=("影身",),
            authority_refs=("power.manifestation.CLONE_001",),
            parent_entity_id="PROTAGONIST_001",
        ),
        "ITEM_001": EntityRecord(
            entity_id="ITEM_001",
            kind=EntityKind.ITEM,
            display_name="回潮楔",
            aliases=("楔子", "古器"),
            authority_refs=("canon.item.ITEM_001",),
        ),
        "RIVAL_001": EntityRecord(
            entity_id="RIVAL_001",
            kind=EntityKind.CHARACTER,
            display_name="阮青蜃",
            aliases=(),
            authority_refs=("canon.character.RIVAL_001",),
        ),
        "ALLY_001": EntityRecord(
            entity_id="ALLY_001",
            kind=EntityKind.CHARACTER,
            display_name="少东家",
            aliases=(),
            authority_refs=("canon.character.ALLY_001",),
        ),
        "RESOURCE_001": EntityRecord(
            entity_id="RESOURCE_001",
            kind=EntityKind.RESOURCE,
            display_name="个人矿利",
            aliases=("矿利份额",),
            authority_refs=("world.resource.RESOURCE_001",),
        ),
        "TIER_001": EntityRecord(
            entity_id="TIER_001",
            kind=EntityKind.POWER_TIER,
            display_name="成炉一重",
            aliases=(),
            authority_refs=("power.tier.TIER_001",),
        ),
        "TIER_002": EntityRecord(
            entity_id="TIER_002",
            kind=EntityKind.POWER_TIER,
            display_name="成炉二重",
            aliases=(),
            authority_refs=("power.tier.TIER_002",),
        ),
        "TIER_003": EntityRecord(
            entity_id="TIER_003",
            kind=EntityKind.POWER_TIER,
            display_name="成炉三重",
            aliases=(),
            authority_refs=("power.tier.TIER_003",),
        ),
        "ROUTE_001": EntityRecord(
            entity_id="ROUTE_001",
            kind=EntityKind.ROUTE,
            display_name="粮路",
            aliases=("粮道",),
            authority_refs=("world.route.ROUTE_001",),
        ),
        "MYSTERY_001": EntityRecord(
            entity_id="MYSTERY_001",
            kind=EntityKind.MYSTERY,
            display_name="地潮提前原因",
            aliases=(),
            authority_refs=("canon.mystery.MYSTERY_001",),
        ),
    }
    return EntityRegistry(
        chapter_id=chapter_id,
        protagonist_id="PROTAGONIST_001",
        entities=entities,
    )


def fact(
    fact_id: str,
    *,
    slot_id: str | None = None,
    source: AuthoritySource = AuthoritySource.FROZEN_MISSION,
    kind: FactKind = FactKind.ACTION,
    mode: FactMode = FactMode.MUST_HOLD,
    phase: FactPhase = FactPhase.DURING_CHAPTER,
    actor_id: str = "PROTAGONIST_001",
    action_id: str = "protect",
    object_ids: tuple[str, ...] = ("ROUTE_001",),
    counterparty_ids: tuple[str, ...] = (),
    from_state: str = "",
    to_state: str = "",
    value=None,
    terminal: bool = False,
    condition_fact_ids: tuple[str, ...] = (),
    depends_on_fact_ids: tuple[str, ...] = (),
    condition_slots: tuple[str, ...] = (),
    depends_on_slots: tuple[str, ...] = (),
    metadata=None,
) -> AuthorityFact:
    return AuthorityFact(
        fact_id=fact_id,
        slot_id=slot_id or f"slot:{fact_id}",
        source=source,
        source_ref=f"{source.value}.{fact_id.lower()}",
        kind=kind,
        mode=mode,
        phase=phase,
        actor_id=actor_id,
        action_id=action_id,
        object_ids=object_ids,
        counterparty_ids=counterparty_ids,
        from_state=from_state,
        to_state=to_state,
        value=value,
        terminal=terminal,
        condition_fact_ids=condition_fact_ids,
        depends_on_fact_ids=depends_on_fact_ids,
        condition_slots=condition_slots,
        depends_on_slots=depends_on_slots,
        metadata=metadata or {},
    )


FREEZERS = {
    AuthoritySource.FROZEN_MISSION: freeze_mission_artifact,
    AuthoritySource.CANON: freeze_canon_artifact,
    AuthoritySource.WORLD_AUTHORITY: freeze_world_artifact,
    AuthoritySource.POWER_AUTHORITY: freeze_power_artifact,
    AuthoritySource.HUMAN_AUTHORITY: freeze_human_artifact,
    AuthoritySource.READER_RELEASE: freeze_reader_release_artifact,
}


def add_facts(
    builder: AtomicAuthorityContractBuilder,
    source: AuthoritySource,
    artifact_suffix: str,
    *facts: AuthorityFact,
) -> None:
    prefix = {
        AuthoritySource.FROZEN_MISSION: "mission",
        AuthoritySource.CANON: "canon",
        AuthoritySource.WORLD_AUTHORITY: "world",
        AuthoritySource.POWER_AUTHORITY: "power",
        AuthoritySource.HUMAN_AUTHORITY: "human",
        AuthoritySource.READER_RELEASE: "reader_release",
    }[source]
    builder.add_artifact(
        FREEZERS[source](f"{prefix}:test:{artifact_suffix}", facts)
    )


def eligible_contract():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "eligible",
        fact("FACT_PROTECT_ROUTE"),
    )
    return builder.build()


def primary_80() -> str:
    return "\n\n".join(
        f"P{i:02d} ordinary story paragraph" for i in range(1, 81)
    )


def primary_binding(
    fact_id: str,
    paragraph_ids: tuple[int, ...],
    primary_body: str,
    note: str = "",
):
    return bind_primary_realization(
        fact_id=fact_id,
        paragraph_ids=paragraph_ids,
        primary_body=primary_body,
        note=note,
    )


def surface_registry() -> ActionSurfaceRegistry:
    return ActionSurfaceRegistry.from_dict(
        {
            "route_breaks": "{objects}在地潮中断裂。",
            "choose_to_protect": "{actor}决定先保住{objects}。",
            "repair_under_pressure": "{actor}顶住潮压，把{objects}重新接上。",
            "world_reprices_route": "现场势力停止撤货，转而按{objects}撤人。",
            "preserve_route": "{actor}保住{objects}。",
            "relationship_reprice": "{counterparties}开始把{actor}当作{to_state}。",
            "depart_before_low_tide": "下一次低潮前，{actor}必须沿{objects}离开。",
        }
    )


def narrative_registry() -> NarrativeFunctionRegistry:
    return NarrativeFunctionRegistry.from_dict(
        {
            "function.public_judgment": "让主角第一次以自己的判断改变公共行动。",
            "function.private_choice": "让主角把一次私人选择变成下一阶段的行动方向。",
        }
    )


def structured_canon_artifact():
    return freeze_canon_artifact(
        "canon:test:structured-prestate",
        [
            fact(
                "CANON_RIVAL_RELATION_PRESTATE",
                slot_id="relationship:PROTAGONIST_001:RIVAL_001",
                source=AuthoritySource.CANON,
                kind=FactKind.RELATIONSHIP_TRANSITION,
                mode=FactMode.MUST_HOLD,
                phase=FactPhase.PRE_CHAPTER,
                actor_id="PROTAGONIST_001",
                action_id="remain_unknown_competitor",
                counterparty_ids=("RIVAL_001",),
                to_state="unknown_competitor",
            )
        ],
    )


# ---------------------------------------------------------------------------
# Source purity and trusted artifacts
# ---------------------------------------------------------------------------


def test_raw_fact_and_self_labelled_fragment_are_rejected():
    builder = AtomicAuthorityContractBuilder(registry())
    with pytest.raises(SourcePurityError):
        builder.add_fact(fact("FACT_RAW"))
    with pytest.raises(SourcePurityError):
        builder.add_fragment(
            {"source": "canon", "facts": [fact("FACT_SPOOF").to_dict()]}
        )


def test_source_specific_factory_overrides_payload_source_label():
    spoofed = fact("FACT_SOURCE", source=AuthoritySource.CANON)
    artifact = freeze_mission_artifact("mission:test:source", [spoofed])
    assert artifact.source == AuthoritySource.FROZEN_MISSION
    assert artifact.facts[0].source == AuthoritySource.FROZEN_MISSION
    assert artifact.facts[0].source_ref.startswith("mission:test:source#fact:")


def test_artifact_prefix_and_digest_are_validated():
    with pytest.raises(SourcePurityError):
        FrozenAuthorityArtifact(
            source=AuthoritySource.CANON,
            artifact_id="mission:wrong-prefix",
            revision_sha256="0" * 64,
            facts=(),
        )
    with pytest.raises(SourcePurityError):
        FrozenAuthorityArtifact(
            source=AuthoritySource.CANON,
            artifact_id="canon:test:bad-digest",
            revision_sha256="bad",
            facts=(),
        )


def test_curator_diagnostic_cannot_create_hard_conflict_or_change_hash():
    first = AtomicAuthorityContractBuilder(registry())
    add_facts(
        first,
        AuthoritySource.FROZEN_MISSION,
        "diag-a",
        fact("FACT_PROTECT_ROUTE"),
    )
    contract_a = first.build()

    second = AtomicAuthorityContractBuilder(registry())
    add_facts(
        second,
        AuthoritySource.FROZEN_MISSION,
        "diag-a",
        fact("FACT_PROTECT_ROUTE"),
    )
    second.add_diagnostic("Curator says: 无法判断，似乎存在冲突。")
    contract_b = second.build()

    assert contract_a.contract_hash == contract_b.contract_hash
    assert contract_b.preflight_eligible
    assert not contract_b.conflicts
    assert contract_b.diagnostics == (
        "Curator says: 无法判断，似乎存在冲突。",
    )


def test_all_hard_sources_are_typed_and_never_primary_or_curator():
    builder = AtomicAuthorityContractBuilder(registry())
    for index, source in enumerate(AuthoritySource, 1):
        add_facts(
            builder,
            source,
            f"all-sources-{index}",
            fact(f"FACT_SOURCE_{index:02d}", slot_id=f"slot:{index}", source=source),
        )
    contract = builder.build()
    assert set(contract.to_dict()["hard_sources"]) == {
        source.value for source in AuthoritySource
    }
    serialized = str(contract.to_dict()).lower()
    assert "primary_draft" not in serialized
    assert "curator_audit" not in serialized


# ---------------------------------------------------------------------------
# Entity identity
# ---------------------------------------------------------------------------


def test_primary_text_cannot_define_protagonist_identity():
    contract = eligible_contract()
    assert contract.registry.protagonist_id == "PROTAGONIST_001"
    assert contract.registry.entities["PROTAGONIST_001"].display_name == "顾停舟"
    assert contract.registry.resolve_surface("顾临川拔刀。") == set()


def test_unique_surface_resolver_fails_on_zero_or_ambiguous_match():
    current = registry()
    with pytest.raises(IRValidationError):
        current.resolve_unique_surface("无人被具名。")
    with pytest.raises(IRValidationError):
        current.resolve_unique_surface("顾停舟命令分身按住回潮楔。")
    assert current.resolve_unique_surface("顾停舟拔刀。") == "PROTAGONIST_001"


def test_unknown_entity_id_fails_preflight_instead_of_name_priority():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "unknown-actor",
        fact("FACT_WRONG_ACTOR", actor_id="PROTAGONIST_999"),
    )
    contract = builder.build()
    assert not contract.preflight_eligible
    assert any("PROTAGONIST_999" in item for item in contract.unsupported)


# ---------------------------------------------------------------------------
# Conflict, transitions and dependency closure
# ---------------------------------------------------------------------------


def pre_power_fact(fact_id: str, state: str, source: AuthoritySource):
    return fact(
        fact_id,
        slot_id="power:PROTAGONIST_001",
        source=source,
        kind=FactKind.STATE_TRANSITION,
        phase=FactPhase.PRE_CHAPTER,
        action_id="remain_at_tier",
        object_ids=(state,),
        to_state=state,
    )


def power_transition(fact_id: str, from_state: str, to_state: str):
    return fact(
        fact_id,
        slot_id="power:PROTAGONIST_001",
        kind=FactKind.POWER_TRANSITION,
        mode=FactMode.TERMINAL,
        phase=FactPhase.CHAPTER_END,
        action_id="advance_power",
        object_ids=(to_state,),
        from_state=from_state,
        to_state=to_state,
        terminal=True,
    )


def test_same_slot_same_phase_incompatible_authority_is_conflict():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.CANON,
        "power-a",
        pre_power_fact("FACT_POWER_A", "TIER_002", AuthoritySource.CANON),
    )
    add_facts(
        builder,
        AuthoritySource.POWER_AUTHORITY,
        "power-b",
        pre_power_fact(
            "FACT_POWER_B", "TIER_003", AuthoritySource.POWER_AUTHORITY
        ),
    )
    contract = builder.build()
    assert not contract.preflight_eligible
    assert any("incompatible Authority facts" in item for item in contract.conflicts)


def test_transition_from_state_must_match_existing_canon():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.CANON,
        "power-current",
        pre_power_fact(
            "FACT_POWER_CURRENT", "TIER_002", AuthoritySource.CANON
        ),
    )
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "power-up",
        power_transition("FACT_POWER_UP", "TIER_001", "TIER_003"),
    )
    contract = builder.build()
    assert not contract.preflight_eligible
    assert any("expects from_state" in item for item in contract.conflicts)


def test_transition_with_declared_from_state_but_no_prestate_is_unsupported():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "missing-prestate",
        power_transition("FACT_POWER_UP", "TIER_002", "TIER_003"),
    )
    contract = builder.build()
    assert not contract.preflight_eligible
    assert any("no pre-chapter state exists" in item for item in contract.unsupported)


def test_matching_power_transition_is_eligible():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.CANON,
        "power-current",
        pre_power_fact(
            "FACT_POWER_CURRENT", "TIER_002", AuthoritySource.CANON
        ),
    )
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "power-up",
        power_transition("FACT_POWER_UP", "TIER_002", "TIER_003"),
    )
    assert builder.build().preflight_eligible


def test_unknown_fact_and_slot_dependencies_fail_preflight():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "unknown-deps",
        fact(
            "FACT_PROOF",
            kind=FactKind.PUBLIC_PROOF,
            depends_on_fact_ids=("FACT_MISSING",),
            depends_on_slots=("slot:missing",),
        ),
    )
    contract = builder.build()
    assert not contract.preflight_eligible
    assert any("FACT_MISSING" in item for item in contract.unsupported)
    assert any("slot:missing" in item for item in contract.unsupported)


def test_cross_source_dependency_uses_stable_slot():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.CANON,
        "resource-prestate",
        fact(
            "CANON_RESOURCE_NOT_RECEIVED",
            slot_id="resource:RESOURCE_001",
            source=AuthoritySource.CANON,
            kind=FactKind.RESOURCE_TRANSITION,
            mode=FactMode.MUST_HOLD,
            phase=FactPhase.PRE_CHAPTER,
            action_id="remain_not_received",
            object_ids=("RESOURCE_001",),
            to_state="not_received",
        ),
    )
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "resource",
        fact(
            "MISSION_RUNTIME_ASSIGNED_99",
            slot_id="resource:RESOURCE_001",
            kind=FactKind.RESOURCE_TRANSITION,
            mode=FactMode.TERMINAL,
            phase=FactPhase.CHAPTER_END,
            action_id="receive_resource",
            object_ids=("RESOURCE_001",),
            from_state="not_received",
            to_state="received",
            terminal=True,
        ),
    )
    add_facts(
        builder,
        AuthoritySource.READER_RELEASE,
        "resource-value",
        fact(
            "READER_RELEASE_RESOURCE_VALUE",
            slot_id="reader_release:resource_value",
            source=AuthoritySource.READER_RELEASE,
            kind=FactKind.READER_RELEASE,
            phase=FactPhase.READER_KNOWLEDGE,
            actor_id="",
            action_id="reader_learns_resource_value",
            object_ids=("RESOURCE_001",),
            depends_on_slots=("resource:RESOURCE_001",),
        ),
    )
    assert builder.build().preflight_eligible


def test_self_dependency_and_dependency_cycle_are_conflicts():
    self_builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        self_builder,
        AuthoritySource.FROZEN_MISSION,
        "self",
        fact(
            "FACT_SELF",
            depends_on_fact_ids=("FACT_SELF",),
        ),
    )
    assert any(
        "depend on itself" in item for item in self_builder.build().conflicts
    )

    cycle_builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        cycle_builder,
        AuthoritySource.FROZEN_MISSION,
        "cycle",
        fact("FACT_A", depends_on_fact_ids=("FACT_B",)),
        fact("FACT_B", depends_on_fact_ids=("FACT_A",)),
    )
    assert any(
        "dependency cycle" in item.lower()
        for item in cycle_builder.build().conflicts
    )


# ---------------------------------------------------------------------------
# Semantic consistency of typed facts
# ---------------------------------------------------------------------------


def test_unknown_boundary_requires_must_remain_unknown():
    with pytest.raises(IRValidationError):
        fact(
            "FACT_UNKNOWN_BAD",
            kind=FactKind.UNKNOWN_BOUNDARY,
            mode=FactMode.MUST_HOLD,
            actor_id="",
            action_id="keep_unknown",
            object_ids=("MYSTERY_001",),
        )
    good = fact(
        "FACT_UNKNOWN_GOOD",
        kind=FactKind.UNKNOWN_BOUNDARY,
        mode=FactMode.MUST_REMAIN_UNKNOWN,
        actor_id="",
        action_id="keep_unknown",
        object_ids=("MYSTERY_001",),
    )
    assert good.mode == FactMode.MUST_REMAIN_UNKNOWN


def test_terminal_flag_and_mode_must_agree():
    with pytest.raises(IRValidationError):
        fact("FACT_BAD_TERMINAL", mode=FactMode.MUST_HOLD, terminal=True)


def test_deadline_and_ending_have_distinct_phase_semantics():
    deadline = fact(
        "FACT_DEADLINE",
        kind=FactKind.DEADLINE,
        phase=FactPhase.POST_CHAPTER,
        action_id="depart_before_low_tide",
        object_ids=("ROUTE_001",),
    )
    ending = fact(
        "FACT_ENDING",
        kind=FactKind.ENDING,
        mode=FactMode.TERMINAL,
        phase=FactPhase.CHAPTER_END,
        action_id="depart_now",
        object_ids=("ROUTE_001",),
        terminal=True,
    )
    assert not deadline.terminal
    assert ending.terminal


def test_metadata_and_value_keys_are_kind_specific():
    with pytest.raises(IRValidationError):
        fact("FACT_META", metadata={"random": True})
    with pytest.raises(IRValidationError):
        fact(
            "FACT_VALUE",
            kind=FactKind.ABILITY_BOUNDARY,
            value={"unlimited_power": True},
        )


def test_critical_history_requires_state_bearing_allowed_domain():
    with pytest.raises(IRValidationError):
        fact(
            "FACT_HISTORY_BAD",
            kind=FactKind.HISTORICAL_CLAIM_BOUNDARY,
            mode=FactMode.MUST_NOT_HOLD,
            actor_id="",
            action_id="no_invented_history",
            object_ids=("RESOURCE_001",),
            metadata={"domain": "daily_memory", "criticality": "state_bearing"},
        )
    good = fact(
        "FACT_HISTORY_GOOD",
        kind=FactKind.HISTORICAL_CLAIM_BOUNDARY,
        mode=FactMode.MUST_NOT_HOLD,
        actor_id="",
        action_id="no_invented_history",
        object_ids=("RESOURCE_001",),
        metadata={
            "domain": "money",
            "criticality": "state_bearing",
            "allowed_claim_ids": [],
        },
    )
    assert good.metadata["domain"] == "money"


# ---------------------------------------------------------------------------
# Compact/micro sidecar bounded behavior
# ---------------------------------------------------------------------------


def test_compact_sidecar_expands_deterministic_fact_ids():
    payload = {
        "v": "AAIR1",
        "chapter": "BOOK_A:CH001",
        "protagonist": "PROTAGONIST_001",
        "actions": [
            {
                "slot": "action:BOOK_A_CH001:1",
                "actor": "PROTAGONIST_001",
                "verb": "protect",
                "objects": ["ROUTE_001"],
            }
        ],
        "results": [
            {
                "slot": "result:BOOK_A_CH001:1",
                "kind": "direct_result",
                "actor": "PROTAGONIST_001",
                "verb": "preserve_route",
                "objects": ["ROUTE_001"],
                "to": "preserved",
            }
        ],
        "states": [],
        "ending": [
            {
                "slot": "ending:BOOK_A_CH001:1",
                "kind": "ending",
                "actor": "PROTAGONIST_001",
                "verb": "depart",
                "objects": ["ROUTE_001"],
            }
        ],
        "boundaries": [],
    }
    first = expand_compact_mission_sidecar(payload, registry())
    second = expand_compact_mission_sidecar(payload, registry())
    assert [item.fact_id for item in first] == [item.fact_id for item in second]


def test_compact_and_micro_sidecars_reject_unknown_fields_handles_and_overflow():
    base = {
        "v": "AAIR1",
        "chapter": "BOOK_A:CH001",
        "protagonist": "PROTAGONIST_001",
        "actions": [],
        "results": [],
        "states": [],
        "ending": [],
        "boundaries": [],
    }
    with pytest.raises(IRValidationError):
        expand_compact_mission_sidecar(base | {"primary_hints": []}, registry())
    overflow = dict(base)
    overflow["actions"] = [
        {
            "slot": f"action:BOOK_A_CH001:{index}",
            "actor": "PROTAGONIST_001",
            "verb": "protect",
            "objects": ["ROUTE_001"],
        }
        for index in range(1, 5)
    ]
    with pytest.raises(IRValidationError):
        expand_compact_mission_sidecar(overflow, registry())
    with pytest.raises(IRValidationError):
        expand_micro_mission_sidecar(
            "A|P|protect|UNKNOWN|-",
            registry(),
            {"P": "PROTAGONIST_001"},
        )
    with pytest.raises(IRValidationError):
        expand_micro_mission_sidecar(
            "A|P|protect|G|-",
            registry(),
            {"P": "RIVAL_001", "G": "ROUTE_001"},
        )


# ---------------------------------------------------------------------------
# Primary Preservation Map and locality
# ---------------------------------------------------------------------------


def test_primary_preservation_map_is_separate_from_contract():
    contract = eligible_contract()
    primary = "顾停舟想拿到自己的矿利。\n\n他守住了粮道。"
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
        protection_hints=(
            ProtectionHint(
                paragraph_id=1,
                exact_fragment="想拿到自己的矿利",
                provenance=PreservationProvenance.CURATOR_LOCATION_HINT,
                note="already-successful private desire",
            ),
        ),
    )
    assert contract.contract_hash == preservation.contract_hash
    assert "protection_hints" not in contract.to_dict()
    assert preservation.editable_paragraph_ids == {2}
    assert preservation.locked_paragraph_ids == {1}


def test_primary_preservation_map_round_trip_retains_paragraph_hashes():
    contract = eligible_contract()
    primary = "顾停舟想拿到自己的矿利。\n\n他守住了粮道。"
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
    )
    restored = PrimaryPreservationMap.from_dict(preservation.to_dict())
    assert restored.paragraph_hashes == preservation.paragraph_hashes
    assert restored.editable_paragraph_ids == {2}
    assert restored.locked_paragraph_ids == {1}


def test_curator_evidence_binding_cannot_expand_edit_window():
    contract = eligible_contract()
    primary = "P1 desire。\n\nP2 fact。\n\nP3 relation。"
    with pytest.raises(IRValidationError):
        FactEvidenceBinding(
            fact_id="FACT_PROTECT_ROUTE",
            paragraph_ids=(3,),
            provenance=PreservationProvenance.CURATOR_LOCATION_HINT,
            primary_sha256="0" * 64,
        )
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
        protection_hints=(
            ProtectionHint(
                paragraph_id=3,
                exact_fragment="relation",
                provenance=PreservationProvenance.CURATOR_LOCATION_HINT,
            ),
        ),
    )
    assert preservation.editable_paragraph_ids == {2}
    assert 3 in preservation.locked_paragraph_ids


def test_repair_target_requires_fact_ids_and_bounded_radius():
    with pytest.raises(IRValidationError):
        RepairTarget(fact_ids=())
    with pytest.raises(IRValidationError):
        RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",), locality_radius=2)


def test_edit_locality_locks_everything_outside_target_window():
    contract = eligible_contract()
    primary = primary_80()
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (42, 43), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
    )
    assert preservation.editable_paragraph_ids == {42, 43}
    inside = validate_primary_preservation(
        contract=contract,
        preservation=preservation,
        primary_body=primary,
        operations=(
            PatchOperation(
                kind=PatchKind.REPLACE,
                start=42,
                end=43,
                payload="P42 repaired payment.\n\nP43 repaired receipt.",
            ),
        ),
    )
    outside = validate_primary_preservation(
        contract=contract,
        preservation=preservation,
        primary_body=primary,
        operations=(
            PatchOperation(
                kind=PatchKind.REPLACE,
                start=39,
                end=39,
                payload="P39 erased relation.",
            ),
        ),
    )
    assert inside["pass"]
    assert not outside["pass"]


def test_primary_hash_mismatch_invalidates_preservation_map():
    contract = eligible_contract()
    primary = "P1。\n\nP2。"
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
    )
    result = validate_primary_preservation(
        contract=contract,
        preservation=preservation,
        primary_body="P1 changed。\n\nP2。",
        operations=(),
    )
    assert not result["pass"]
    assert any("hash mismatch" in item for item in result["violations"])


def test_exact_fragment_must_remain_in_same_replacement_payload():
    contract = eligible_contract()
    primary = "P1。\n\nP2 钱到账，他终于能自己决定怎么花。\n\nP3。"
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
        protection_hints=(
            ProtectionHint(
                paragraph_id=2,
                exact_fragment="终于能自己决定怎么花",
                provenance=PreservationProvenance.CURATOR_LOCATION_HINT,
            ),
        ),
    )
    erased = validate_primary_preservation(
        contract=contract,
        preservation=preservation,
        primary_body=primary,
        operations=(
            PatchOperation(
                kind=PatchKind.REPLACE,
                start=2,
                end=2,
                payload="P2 钱到账。",
            ),
            PatchOperation(
                kind=PatchKind.INSERT_AFTER,
                start=2,
                end=2,
                payload="他终于能自己决定怎么花。",
            ),
        ),
    )
    preserved = validate_primary_preservation(
        contract=contract,
        preservation=preservation,
        primary_body=primary,
        operations=(
            PatchOperation(
                kind=PatchKind.REPLACE,
                start=2,
                end=2,
                payload="P2 钱到账，他终于能自己决定怎么花。",
            ),
        ),
    )
    assert not erased["pass"]
    assert preserved["pass"]


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


def unsupported_contract():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "unsupported",
        fact("FACT_UNKNOWN", actor_id="PROTAGONIST_999"),
    )
    return builder.build()


def test_unsupported_contract_bypasses_atomic_and_current_full_is_ungated():
    contract = unsupported_contract()
    assert (
        AtomicRoutingPolicy.preflight(contract)
        == PreflightRoute.CURRENT_FULL_REVISER_UNGATED
    )
    assert AtomicRoutingPolicy.after_full(
        contract,
        ContractGateResult(supported=False, pass_=False),
    ) == FinalRoute.CURRENT_FULL_REVISER_FINAL_UNGATED


def test_supported_but_gate_unsupported_routes_to_full_ungated():
    assert AtomicRoutingPolicy.after_delta(
        eligible_contract(),
        ContractGateResult(supported=False, pass_=False),
    ) == FinalRoute.FULL_REVISER_UNGATED


def test_supported_delta_failure_routes_to_full_then_supported_gate():
    assert AtomicRoutingPolicy.after_delta(
        eligible_contract(),
        ContractGateResult(
            supported=True,
            pass_=False,
            blocker_fact_ids=("FACT_PROTECT_ROUTE",),
        ),
    ) == FinalRoute.FULL_REVISER_THEN_SUPPORTED_GATE


def test_supported_full_failure_is_residual_failure():
    assert AtomicRoutingPolicy.after_full(
        eligible_contract(),
        ContractGateResult(
            supported=True,
            pass_=False,
            blocker_fact_ids=("FACT_PROTECT_ROUTE",),
        ),
    ) == FinalRoute.FULL_REVISER_RESIDUAL_FAILURE


# ---------------------------------------------------------------------------
# Director native structured decision: one typed source, dual projection
# ---------------------------------------------------------------------------


def structured_decision_payload() -> dict:
    return {
        "schema_version": "director-structured-decision-v1",
        "chapter_id": "BOOK_A:CH001",
        "protagonist_id": "PROTAGONIST_001",
        "clauses": [
            {
                "field": "trigger_event",
                "kind": "event",
                "action_id": "route_breaks",
                "object_ids": ["ROUTE_001"],
                "surface_note": "non-authoritative note",
            },
            {
                "field": "event_driver",
                "kind": "action",
                "actor_id": "PROTAGONIST_001",
                "action_id": "choose_to_protect",
                "object_ids": ["ROUTE_001"],
            },
            {
                "field": "protagonist_action",
                "kind": "action",
                "actor_id": "PROTAGONIST_001",
                "action_id": "repair_under_pressure",
                "object_ids": ["ROUTE_001"],
            },
            {
                "field": "world_reaction",
                "kind": "event",
                "action_id": "world_reprices_route",
                "object_ids": ["ROUTE_001"],
            },
            {
                "field": "direct_result",
                "kind": "direct_result",
                "actor_id": "PROTAGONIST_001",
                "action_id": "preserve_route",
                "object_ids": ["ROUTE_001"],
                "to_state": "preserved",
                "terminal": True,
            },
            {
                "field": "state_change",
                "kind": "relationship_transition",
                "actor_id": "PROTAGONIST_001",
                "action_id": "relationship_reprice",
                "counterparty_ids": ["RIVAL_001"],
                "from_state": "unknown_competitor",
                "to_state": "independent_judgment_holder",
                "terminal": True,
            },
            {
                "field": "ending_drive",
                "kind": "deadline",
                "actor_id": "PROTAGONIST_001",
                "action_id": "depart_before_low_tide",
                "object_ids": ["ROUTE_001"],
                "terminal": False,
            },
        ],
        "narrative_function_id": "function.public_judgment",
    }


def test_structured_decision_dual_projects_human_mission_and_contract():
    decision = DirectorStructuredDecision.from_dict(structured_decision_payload())
    mission = decision.render_human_mission(
        registry=registry(), surfaces=surface_registry(), narrative_functions=narrative_registry()
    )
    contract = decision.build_contract(registry=registry(), authority_artifacts=(structured_canon_artifact(),))
    for label in (
        "触发事件：",
        "推动事件的人：",
        "主角行动：",
        "对手或世界反应：",
        "直接结果：",
        "状态变化：",
        "叙事功能：",
        "结尾推动力：",
    ):
        assert label in mission
    assert contract.preflight_eligible
    assert {
        fact.source for fact in contract.facts.values()
    } == {AuthoritySource.CANON, AuthoritySource.FROZEN_MISSION}


def test_surface_note_changes_neither_rendered_mission_nor_contract_hash():
    first_payload = structured_decision_payload()
    second_payload = structured_decision_payload()
    second_payload["clauses"][0]["surface_note"] = "a completely different note"
    first = DirectorStructuredDecision.from_dict(first_payload)
    second = DirectorStructuredDecision.from_dict(second_payload)
    first_mission = first.render_human_mission(
        registry=registry(), surfaces=surface_registry(), narrative_functions=narrative_registry()
    )
    second_mission = second.render_human_mission(
        registry=registry(), surfaces=surface_registry(), narrative_functions=narrative_registry()
    )
    assert first_mission == second_mission
    assert (
        first.build_contract(registry=registry(), authority_artifacts=(structured_canon_artifact(),)).contract_hash
        == second.build_contract(registry=registry(), authority_artifacts=(structured_canon_artifact(),)).contract_hash
    )


def test_typed_change_changes_both_rendered_mission_and_contract():
    first_payload = structured_decision_payload()
    second_payload = structured_decision_payload()
    second_payload["clauses"][4]["action_id"] = "repair_under_pressure"
    first = DirectorStructuredDecision.from_dict(first_payload)
    second = DirectorStructuredDecision.from_dict(second_payload)
    assert first.render_human_mission(
        registry=registry(), surfaces=surface_registry(), narrative_functions=narrative_registry()
    ) != second.render_human_mission(
        registry=registry(), surfaces=surface_registry(), narrative_functions=narrative_registry()
    )
    assert (
        first.build_contract(registry=registry(), authority_artifacts=(structured_canon_artifact(),)).contract_hash
        != second.build_contract(registry=registry(), authority_artifacts=(structured_canon_artifact(),)).contract_hash
    )


def test_human_clause_is_rejected_as_second_semantic_write():
    payload = structured_decision_payload()
    payload["clauses"][0]["human_clause"] = "自由写一句可能与typed事实冲突的话。"
    with pytest.raises(IRValidationError):
        DirectorStructuredDecision.from_dict(payload)


def test_structured_decision_enforces_field_limits_and_protagonist_actor():
    missing = structured_decision_payload()
    missing["clauses"] = [
        clause
        for clause in missing["clauses"]
        if clause["field"] != "ending_drive"
    ]
    with pytest.raises(IRValidationError):
        DirectorStructuredDecision.from_dict(missing)

    wrong = structured_decision_payload()
    wrong["clauses"][2]["actor_id"] = "RIVAL_001"
    decision = DirectorStructuredDecision.from_dict(wrong)
    with pytest.raises(IRValidationError):
        decision.build_contract(registry=registry(), authority_artifacts=(structured_canon_artifact(),))


def test_structured_decision_rejects_second_frozen_mission_artifact():
    decision = DirectorStructuredDecision.from_dict(structured_decision_payload())
    second_mission = freeze_mission_artifact(
        "mission:test:second",
        [fact("FACT_SECOND_MISSION")],
    )
    with pytest.raises(IRValidationError):
        decision.build_contract(
            registry=registry(), authority_artifacts=(structured_canon_artifact(), second_mission)
        )


def test_same_structured_schema_supports_different_display_names():
    first_registry = registry(chapter_id="BOOK_A:CH001")
    second_entities = {
        key: EntityRecord(
            entity_id=value.entity_id,
            kind=value.kind,
            display_name=(
                "顾临川" if key == "PROTAGONIST_001" else value.display_name
            ),
            aliases=value.aliases,
            authority_refs=("book_b." + value.authority_refs[0],),
            parent_entity_id=value.parent_entity_id,
        )
        for key, value in first_registry.entities.items()
    }
    second_registry = EntityRegistry(
        chapter_id="BOOK_A:CH001",
        protagonist_id="PROTAGONIST_001",
        entities=second_entities,
    )
    decision = DirectorStructuredDecision.from_dict(structured_decision_payload())
    assert decision.build_contract(registry=first_registry, authority_artifacts=(structured_canon_artifact(),)).preflight_eligible
    assert decision.build_contract(registry=second_registry, authority_artifacts=(structured_canon_artifact(),)).preflight_eligible
    assert "顾停舟" in decision.render_human_mission(
        registry=first_registry, surfaces=surface_registry(), narrative_functions=narrative_registry()
    )
    assert "顾临川" in decision.render_human_mission(
        registry=second_registry, surfaces=surface_registry(), narrative_functions=narrative_registry()
    )


# ---------------------------------------------------------------------------
# Post-audit invariants: provenance, immutability, structure and one semantics
# ---------------------------------------------------------------------------


def test_direct_or_digest_forged_authority_artifact_is_rejected():
    good = freeze_canon_artifact(
        "canon:test:trusted",
        [fact("FACT_TRUSTED_CANON", source=AuthoritySource.CANON)],
    )
    with pytest.raises(SourcePurityError):
        FrozenAuthorityArtifact(
            source=good.source,
            artifact_id=good.artifact_id,
            revision_sha256=good.revision_sha256,
            facts=good.facts,
        )
    with pytest.raises(SourcePurityError):
        replace(good, revision_sha256="0" * 64)


def test_empty_contract_is_not_preflight_eligible():
    contract = AtomicAuthorityContractBuilder(registry()).build()
    assert not contract.preflight_eligible
    assert "Atomic Authority Contract has no frozen artifacts" in contract.unsupported
    assert "Atomic Authority Contract has no hard facts" in contract.unsupported


def test_registry_contract_and_nested_fact_payload_are_immutable_snapshots():
    current_registry = registry()
    contract = eligible_contract()
    with pytest.raises(TypeError):
        current_registry.entities["RIVAL_999"] = current_registry.entities["RIVAL_001"]
    with pytest.raises(TypeError):
        contract.facts["FACT_OTHER"] = fact("FACT_OTHER")

    nested = fact(
        "FACT_IMMUTABLE_PAYLOAD",
        kind=FactKind.ABILITY_BOUNDARY,
        value={"allowed": ["stabilize"], "full_body_power": False},
    )
    with pytest.raises(TypeError):
        nested.value["full_body_power"] = True
    assert nested.value["allowed"] == ("stabilize",)
    with pytest.raises(TypeError):
        nested.metadata["source"] = "primary"


def test_terminal_state_transition_without_from_state_is_unsupported():
    builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        builder,
        AuthoritySource.FROZEN_MISSION,
        "missing-terminal-prestate",
        fact(
            "FACT_RESOURCE_RECEIVED_WITHOUT_FROM",
            slot_id="resource:RESOURCE_001",
            kind=FactKind.RESOURCE_TRANSITION,
            mode=FactMode.TERMINAL,
            phase=FactPhase.CHAPTER_END,
            action_id="receive_resource",
            object_ids=("RESOURCE_001",),
            to_state="received",
            terminal=True,
        ),
    )
    contract = builder.build()
    assert not contract.preflight_eligible
    assert any("lacks explicit from_state" in item for item in contract.unsupported)


def test_preservation_map_is_immutable_after_construction():
    contract = eligible_contract()
    primary = "P1 locked。\n\nP2 repair。\n\nP3 locked。"
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
    )
    with pytest.raises(AttributeError):
        preservation.editable_paragraph_ids.add(1)
    with pytest.raises(TypeError):
        preservation.paragraph_hashes[1] = "0" * 64
    with pytest.raises(TypeError):
        preservation.fact_evidence["FACT_PROTECT_ROUTE"] = (1, 2)


@pytest.mark.parametrize(
    "operation",
    (
        PatchOperation(
            kind=PatchKind.REPLACE,
            start=2,
            end=2,
            payload="replacement A。\n\nreplacement B。",
        ),
        PatchOperation(
            kind=PatchKind.INSERT_AFTER,
            start=2,
            end=2,
            payload="inserted paragraph。",
        ),
        PatchOperation(kind=PatchKind.DELETE, start=2, end=2),
    ),
)
def test_edit_locality_rejects_paragraph_structure_shift(operation):
    contract = eligible_contract()
    primary = "P1 locked。\n\nP2 repair。\n\nP3 locked。"
    preservation = build_primary_preservation_map(
        contract=contract,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
    )
    result = validate_primary_preservation(
        contract=contract,
        preservation=preservation,
        primary_body=primary,
        operations=(operation,),
    )
    assert not result["pass"]
    assert any("paragraph structure" in item for item in result["violations"])


def test_empty_protection_hint_is_rejected():
    with pytest.raises(IRValidationError):
        ProtectionHint(
            paragraph_id=2,
            exact_fragment="   ",
            provenance=PreservationProvenance.CURATOR_LOCATION_HINT,
        )


def test_old_free_narrative_fields_are_rejected():
    payload = structured_decision_payload()
    payload["narrative_function"] = "第二份自由语义。"
    with pytest.raises(IRValidationError):
        DirectorStructuredDecision.from_dict(payload)
    payload = structured_decision_payload()
    payload["specialty_suggestions"] = ["Action：启用。"]
    with pytest.raises(IRValidationError):
        DirectorStructuredDecision.from_dict(payload)


def test_narrative_function_id_changes_surface_but_not_hard_contract():
    first_payload = structured_decision_payload()
    second_payload = structured_decision_payload()
    second_payload["narrative_function_id"] = "function.private_choice"
    first = DirectorStructuredDecision.from_dict(first_payload)
    second = DirectorStructuredDecision.from_dict(second_payload)
    first_mission = first.render_human_mission(
        registry=registry(),
        surfaces=surface_registry(),
        narrative_functions=narrative_registry(),
    )
    second_mission = second.render_human_mission(
        registry=registry(),
        surfaces=surface_registry(),
        narrative_functions=narrative_registry(),
    )
    assert first_mission != second_mission
    assert first.build_contract(
        registry=registry(),
        authority_artifacts=(structured_canon_artifact(),),
    ).contract_hash == second.build_contract(
        registry=registry(),
        authority_artifacts=(structured_canon_artifact(),),
    ).contract_hash


def test_unknown_narrative_function_surface_fails_render():
    decision = DirectorStructuredDecision.from_dict(structured_decision_payload())
    with pytest.raises(IRValidationError):
        decision.render_human_mission(
            registry=registry(),
            surfaces=surface_registry(),
            narrative_functions=NarrativeFunctionRegistry.from_dict(
                {"function.other": "另一个叙事功能。"}
            ),
        )


def test_structured_terminal_transition_without_canon_prestate_is_ineligible():
    decision = DirectorStructuredDecision.from_dict(structured_decision_payload())
    contract = decision.build_contract(registry=registry())
    assert not contract.preflight_eligible
    assert any("no pre-chapter state exists" in item for item in contract.unsupported)


def test_entity_provenance_rejects_curator_or_primary_refs():
    for reference in ("curator.entity.fake", "primary.entity.fake"):
        with pytest.raises(SourcePurityError):
            EntityRecord(
                entity_id="CHARACTER_FAKE_001",
                kind=EntityKind.CHARACTER,
                display_name="假人物",
                authority_refs=(reference,),
            )


def test_primary_evidence_binding_is_runtime_issued_and_primary_bound():
    primary = "P1。\n\nP2。"
    with pytest.raises(IRValidationError):
        FactEvidenceBinding(
            fact_id="FACT_PROTECT_ROUTE",
            paragraph_ids=(2,),
            provenance=PreservationProvenance.PRIMARY_REALIZATION,
            primary_sha256="0" * 64,
        )
    binding = primary_binding("FACT_PROTECT_ROUTE", (2,), primary)
    with pytest.raises(IRValidationError):
        build_primary_preservation_map(
            contract=eligible_contract(),
            primary_body="P1 changed。\n\nP2。",
            evidence_bindings=(binding,),
            repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
        )


def test_preservation_validation_requires_the_same_contract_snapshot():
    first = eligible_contract()
    primary = "P1。\n\nP2 repair。"
    preservation = build_primary_preservation_map(
        contract=first,
        primary_body=primary,
        evidence_bindings=(
            primary_binding("FACT_PROTECT_ROUTE", (2,), primary),
        ),
        repair_target=RepairTarget(fact_ids=("FACT_PROTECT_ROUTE",)),
    )

    second_builder = AtomicAuthorityContractBuilder(registry())
    add_facts(
        second_builder,
        AuthoritySource.FROZEN_MISSION,
        "other-contract",
        fact(
            "FACT_OTHER_ROUTE",
            slot_id="event:FACT_OTHER_ROUTE",
            action_id="protect_other",
        ),
    )
    second = second_builder.build()
    result = validate_primary_preservation(
        contract=second,
        preservation=preservation,
        primary_body=primary,
        operations=(),
    )
    assert not result["pass"]
    assert any("contract_hash" in item for item in result["violations"])


def test_contract_snapshot_round_trip_rechecks_artifact_membership_and_hash():
    contract = eligible_contract()
    payload = contract.to_dict()
    restored = AtomicAuthorityContract.from_dict(payload)
    assert restored.contract_hash == contract.contract_hash
    assert restored.to_dict() == payload

    tampered_digest = replace_dict(payload)
    tampered_digest["artifact_provenance"][0]["revision_sha256"] = "0" * 64
    with pytest.raises(SourcePurityError):
        AtomicAuthorityContract.from_dict(tampered_digest)

    missing_membership = replace_dict(payload)
    missing_membership["artifact_provenance"][0]["fact_ids"] = []
    with pytest.raises(IRValidationError):
        AtomicAuthorityContract.from_dict(missing_membership)

    tampered_hash = replace_dict(payload)
    tampered_hash["contract_hash"] = "0" * 64
    with pytest.raises(SourcePurityError):
        AtomicAuthorityContract.from_dict(tampered_hash)


def replace_dict(payload):
    import copy

    return copy.deepcopy(payload)
