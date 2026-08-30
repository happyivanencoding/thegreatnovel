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

## 5. Director / human projection boundary

A single-source `DirectorStructuredDecision` may generate a deterministic Frozen Mission artifact, but the human Mission projection is a separate realization surface that must be audited independently. Do not keep a second free semantic `human_clause`, free narrative paragraph or machine Sidecar.

Free-text verbose/compact/micro Sidecars are negative evidence and must not be revived. The current Action/Narrative-registry human projection is also negative production evidence: in the 2026-08-30 two-book/four-chapter E2E it covered 58/58 registered facts yet lost both Mission Story and Mission Authority, then produced higher Final Story but materially lower Final Authority. A correct typed core does not prove a sufficiently rich human Mission.

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

### 6.1 Primary-bypass boundary

The routing above does **not** imply that an Authority-clean Primary may automatically bypass a value-bearing Full Reviser. `Atomic Authority closure` and `Reviser necessity` are different questions. A Contract Gate can only prove the Hard Authority facts it actually binds; it cannot prove that the Reviser would add no Reader/Story value, nor can an LLM Oracle be trusted as that proof.

The 2026-08-30 rich-free-text bypass experiment froze two fresh repeats and got 0/8 deterministic bypasses. More importantly, among 7 Primary/Reviser pairs that a strict Oracle initially considered direct-final candidates, two independent anonymous pair-blind rounds produced Story **Primary 4 vs Reviser 10** and Authority **Primary 1 vs Reviser 8, with 5 ties**; 0/7 pairs were stably both Story-nondegrading and Authority-clean. Several Oracle PASSes still contained concrete Canon errors. Therefore bypassing Full Reviser requires repeated pair evidence that the stage is actually becoming a no-op for both Story and Authority; Contract PASS alone is insufficient. Do not add an LLM "Reviser necessity" classifier to bridge this gap.

## 7. Evidence standard

Report separately:

- source-purity and controlled negative tests;
- registered known-fact recall;
- complete semantic Contract repeat, including extra facts;
- human Mission Story blind and Authority blind;
- Final Draft Story blind and Authority blind;
- real native structured Director wall;
- cross-book registry coverage, explicitly manual versus automatic;
- complete fallback-adjusted route wall, including discarded structured calls;
- when skipping Full Reviser, repeated frozen Primary-vs-Reviser Story + Authority pair evidence, not only Contract/Oracle PASS.

Never collapse these into one “coverage” number. Static fixtures/schema validity do not prove model quality; known-fact recall does not prove human projection fidelity; Final Story winning while Final Authority loses is a production failure. Runtime projection wall alone is irrelevant if the model takes longer to create the typed decision.

## 8. Freeze / do not freeze

Freeze architecture, trust boundary, Entity/slot model, Edit Locality, unsupported bypass and the requirement to audit typed core, human projection and final prose separately.

Do not freeze hand-authored fixtures, Runtime surface registries, automatic paragraph locator, current Native human Mission replacement, Primary-direct-final routing, Full Reviser removal or any speed claim. The 2026-08-30 properly chained repeat found the current Native route slower both at Director and across the complete Final-Draft critical path; its Final Story gain came with substantial Final Authority loss. Treat the dated numbers as experiment evidence, not a permanent threshold.
