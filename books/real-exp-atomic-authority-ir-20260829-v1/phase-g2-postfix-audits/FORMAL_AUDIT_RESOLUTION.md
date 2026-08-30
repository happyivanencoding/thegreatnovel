# Atomic Authority IR v1｜Formal Audit Resolution

> Scope: resolution of the formal audit findings after the source-boundary cleanup. The original audit remains preserved as evidence; this file records which findings were fixed and which remain research risks.

## Fixed in code and tests

| Finding | Resolution | Evidence |
|---|---|---|
| `FrozenAuthorityArtifact` could be instantiated or digest-spoofed | Private issuer token; source-specific freezer required; artifact and Builder both recompute digest | `test_direct_or_digest_forged_authority_artifact_is_rejected` |
| Empty builder produced an eligible empty contract | Builder records unsupported when no artifacts or no hard facts | `test_empty_contract_is_not_preflight_eligible` |
| Registry / Contract / nested values / Preservation Map were mutable | Frozen dataclasses, `MappingProxyType`, tuples/frozensets, deep-freeze of nested values/metadata | `test_registry_contract_and_nested_fact_payload_are_immutable_snapshots`, `test_preservation_map_is_immutable_after_construction` |
| Stable slots accepted arbitrary IDs | Canonical slot regex enforced in `AuthorityFact` and Schema | focused suite + schema checks |
| State-bearing terminal transition could omit `from_state` | Builder marks it unsupported; explicit Canon pre-state required | `test_terminal_state_transition_without_from_state_is_unsupported`, structured pre-state tests |
| Dependency self-loop / cycle / missing slot | Builder validates fact and slot dependencies and cycles | existing focused dependency tests |
| Curator could label evidence as Primary and expand the window | Primary evidence now requires Runtime-issued `FactEvidenceBinding` with private issuer and Primary SHA-256; Curator only supplies `ProtectionHint` | `test_curator_evidence_binding_cannot_expand_edit_window`, `test_primary_evidence_binding_is_runtime_issued_and_primary_bound` |
| Preservation Map could be used with another Contract | Validation requires current Contract and checks `chapter_id` + `contract_hash` | `test_preservation_validation_requires_the_same_contract_snapshot` |
| Map was serializable without the paragraph hashes used for drift detection | `paragraph_hashes` persisted, restored and schema-required | round-trip test + negative schema probe |
| Replace/insert/delete could shift paragraphs and invalidate locks | Candidate paragraph count and all locked paragraph hashes are rechecked | parameterized paragraph-structure test |
| Empty exact-fragment hint silently passed | Empty hints rejected at construction | `test_empty_protection_hint_is_rejected` |
| Director still had `human_clause`, free `narrative_function` and suggestions as second semantic sources | Canonical decision has one typed clause set plus `narrative_function_id`; Runtime registries render human Mission; free semantic fields and unknown keys rejected | narrative ID tests + expected-invalid schema probes |
| Contract snapshot format could not reconstruct trusted artifacts | `artifact_provenance` now includes `fact_ids`; `AtomicAuthorityContract.from_dict()` reconstructs source-specific artifacts, rechecks digest, membership, hash, conflicts and unsupported state | contract round-trip/tamper tests + runtime negative probe |
| Entity provenance was only an arbitrary string | Entity refs are restricted to Authority domains; Curator/Primary refs rejected | `test_entity_provenance_rejects_curator_or_primary_refs` |

## Fixed in experimental fixtures

The four static fixtures now include explicit Canon pre-states for every terminal resource / ownership / relationship / location transition. They no longer obtain eligibility by omitting the state against which `from_state` must be checked.

## Remaining formal risks

These are deliberately **not** hidden by the passing static suite:

1. **Manual Entity / Fact fixtures.** Two books/four chapters prove schema reuse, not automatic long-novel registry generation.
2. **Action/Narrative surface registries are trusted configuration.** The typed decision has one semantic source, but a malicious or incorrect Runtime surface template can still mistranslate it for humans. Native structured Director experiments must review Mission surface and Contract together.
3. **Automatic fact-to-paragraph binding is unproven.** Current static maps use manually verified Primary locations. A production locator must not become a hidden LLM Authority classifier.
4. **No real native structured Director run.** Free-text Sidecars failed; schema/unit readiness does not prove Story quality, latency or model compliance.
5. **No prose-level Contract gate for arbitrary books.** The architecture avoids a general Chinese parser, but the final bridge from typed IDs to prose evidence still needs bounded, typed realization evidence.
6. **No complete fast-route E2E.** Full Reviser has not been converted from fixed tax to fallback in production.
7. **Unsupported chapter behavior is intentionally conservative.** It bypasses Atomic and follows current Full Reviser; this protects robustness but provides no speed gain.

## False-safe counterexamples that remain mandatory in future tests

- Mission references an existing but wrong Entity ID.
- A surface template renders the opposite action while typed IR is correct.
- A paragraph locator maps the right Fact ID to the wrong paragraph and opens an unrelated scene.
- A multi-step transfer uses the same resource slot but omits an intermediate holder.
- A condition slot is satisfied in Canon but expires before the chapter action.
- The final prose realizes a typed action through metaphor or implication that the bounded evidence mapper cannot prove.

## False-fallback counterexamples that remain mandatory

- A stylistically different but semantically correct realization of the same typed action.
- A relationship transition realized through dialogue without repeating the state name.
- A terminal result spread across two adjacent paragraphs inside the allowed locality.
- A harmless Primary memory that is not state-bearing history.
- A Curator hint outside the edit window that should remain protected simply because the paragraph is locked.

## Freeze / do not freeze

### Freeze

- `Atomic Authority Contract ≠ Primary Preservation Map`.
- Trusted source-specific Authority artifacts.
- Entity IDs and stable slots.
- Curator/Primary cannot define Hard facts, conflicts or identity.
- Edit Locality as the default preservation mechanism.
- Unsupported chapters bypass Atomic.
- Supported Full fallback is re-gated.

### Do not freeze

- Current hand-authored fixtures.
- Current Runtime surface registries as production truth.
- Any free-text Sidecar.
- Native structured Director performance.
- Automatic paragraph binding.
- Removal of Full Reviser.
- Any production speed claim.

## Final formal classification

**Architecture and source-boundary invariants: PASS for continued experimentation.**  
**Automatic compiler / native Director / fast route: NOT PROVEN, NOT PRODUCTION.**
