# Atomic Authority IR Audit Protocol

> Stable architecture and experiment protocol. It does not authorize production wiring.

## 1. Separate the products

### Atomic Authority Contract

Hard facts may come only from trusted Entity Registry + Frozen Mission / Canon / World / Power / Human / Reader Release artifacts.

### Primary Preservation Map

May contain only Runtime-issued fact→paragraph evidence, blocker edit locality, locked paragraphs and narrow exact-fragment hints. It cannot create Hard Facts, identity or conflicts.

## 2. Trust boundary

- Use source-specific freezer constructors, private issuer and normalized-fact SHA-256.
- Reject direct/self-labelled artifacts, digest tampering, empty contracts and facts lacking artifact membership.
- Registry, Fact payload, Contract and Preservation Map are immutable snapshots.
- Snapshot reload reconstructs source artifacts and verifies fact membership, digest, conflicts/unsupported state and Contract hash.
- Curator diagnostics never enter Contract hash or become conflict.

## 3. Entity and state boundary

- Use stable Entity IDs; Primary names/pronouns never define canonical identity.
- Runtime owns fact IDs and canonical stable slots.
- Validate unknown entities/slots, self-dependency, cycles and same-slot conflicts.
- Terminal state-bearing transitions require explicit `from_state` and a compatible Canon pre-state.

## 4. Preservation boundary

- Primary evidence bindings are Runtime-issued and bound to Primary SHA-256.
- Curator may add ProtectionHint only; it cannot masquerade as Primary evidence or expand the edit window.
- Validation requires the same chapter and Contract hash.
- Reject paragraph-count shifts and any locked-paragraph hash drift.
- Protect desire/relationship/reward/surprise mainly by permission, not semantic detectors.

## 5. Director boundary

Target a native single-source `DirectorStructuredDecision`. Runtime uses Action/Narrative registries to render the human eight-field Mission and deterministic Frozen Mission artifact. Do not keep a second free semantic `human_clause`, free narrative paragraph or machine Sidecar.

Free-text verbose/compact/micro Sidecars are negative evidence and must not be revived.

## 6. Routing

```text
preflight unsupported → current Full Reviser, ungated by unsupported Atomic
preflight supported → Delta → Gate
    PASS → Final
    FAIL → Full Reviser → supported Gate
        PASS → Final
        FAIL → residual failure
```

Atomic is an acceleration layer, not a global hard gate.

## 7. Evidence standard

Report separately:

- source-purity and controlled negative tests;
- static fixture coverage;
- real native structured Director model behavior;
- Story + Authority blind;
- independent repeat;
- cross-book registry coverage;
- fallback-adjusted complete-route wall.

Static fixtures and schema validity do not prove model quality or production speed. A gate that refuses unsupported chapters is safe but not generalized.

## 8. Freeze / do not freeze

Freeze architecture, trust boundary, Entity/slot model, Edit Locality and unsupported bypass. Do not freeze hand-authored fixtures, Runtime surface registries, automatic paragraph locator, native Director quality, Full Reviser removal or any speed claim until real E2E evidence exists.
