# Atomic Authority IR v1｜Architecture

> Experimental architecture. It is not wired into the production chapter pipeline.

## 1. The two products are separate

### A. Atomic Authority Contract

```text
Entity Registry
Frozen Mission IR
Canon IR
World Authority IR
Power Authority IR
Human Authority IR
Reader Release IR
        ↓ trusted source-specific freeze
Runtime deterministic merge
        ↓
Atomic Authority Contract
```

The Hard Contract contains only machine-checkable story facts already decided by the creative authority layers. It may contain actors, actions, objects, result/state/ending transitions, resource and ownership states, power boundaries, deadlines, scheduled Reader Release, relationship states and named unknown boundaries.

It may **not** contain:

- Primary realization;
- Curator interpretation;
- prose quality;
- “a good desire beat”;
- Surprise detection;
- paragraph locations;
- revision preferences.

### B. Primary Preservation Map

```text
Primary Draft
+ fact → paragraph realization bindings
+ optional Curator location/protection hints
+ current blocker fact IDs
        ↓
Primary Preservation Map
```

The map controls editing permission:

- which paragraphs realize the current blocked Hard Facts;
- which small locality is editable;
- which paragraphs are locked;
- which exact fragment inside the editable locality must survive.

The map does not create a Hard Fact, Entity ID or source conflict. A Curator hint cannot expand the edit window or change the Contract hash.

## 2. Creative ownership

```text
Story Program
    ↓ decides long-term promises
Outline
    ↓ allocates promise/reward/turn to chapters
Director
    ↓ freezes the current chapter decision
Runtime
    ↓ merges already-frozen typed Authority
Atomic
    ↓ verifies that final prose did not silently erase or alter the decision
```

Atomic does not decide whether the protagonist upgrades, gets an artifact, kisses someone, surprises the crowd, loses money or changes a relationship. Those are creative decisions. Atomic only checks approved decisions after they exist.

## 3. Entity Registry

Hard facts reference stable IDs:

```yaml
entity_id: PROTAGONIST_001
kind: character
display_name: 顾停舟
aliases: [他, 本体, 少年]
```

Mission facts reference IDs:

```yaml
actor_id: PROTAGONIST_001
action_id: defeat
object_ids: [RIVAL_003]
```

Primary names, pronouns and titles are realization evidence only. They cannot redefine `protagonist_id`. An unknown or conflicting ID fails preflight; the system does not solve identity by saying Mission wording outranks Primary wording.

## 4. Trusted Frozen Authority artifacts

A Hard Contract is built only from source-specific `FrozenAuthorityArtifact` objects created by trusted Runtime constructors:

- `freeze_mission_artifact()`;
- `freeze_canon_artifact()`;
- `freeze_world_artifact()`;
- `freeze_power_artifact()`;
- `freeze_human_artifact()`;
- `freeze_reader_release_artifact()`.

Each artifact has a source-specific ID prefix and a SHA-256 digest over normalized facts. Raw facts and self-labelled fragments are rejected. Curator/Primary cannot spoof `source=canon` and enter the builder. Direct construction is rejected by a private issuer token; Builder recomputes the digest. Empty contracts are ineligible, and Registry / Contract / Fact payloads are immutable snapshots.

Diagnostics may be attached for audit, but they do not enter the Contract hash and cannot become conflict.

## 5. Stable slots and dependencies

Fact IDs are artifact-local. Cross-source dependencies should use stable slots:

```text
ownership:CONTRACT_ESCORT_001
resource:RESOURCE_PREPAYMENT_001
relationship:PROTAGONIST_001:CHAR_PARTNER_001
power:PROTAGONIST_001
```

The builder validates:

- unknown entity IDs;
- unknown fact dependencies;
- unknown stable slots;
- self-dependency and dependency cycles;
- same-slot/same-phase incompatible Authority facts;
- transition `from_state` against explicit pre-chapter state.

It does not guess a missing pre-state.

## 6. Native Director structured decision

The tested free-text appendices are rejected as the target architecture:

- verbose JSON Sidecar: large latency and parse burden;
- compact JSON Sidecar: Story quality regressed and eligibility remained poor;
- micro DSL Sidecar: parse failed completely.

The intended experiment is a native `DirectorStructuredDecision` where the model makes one typed decision. Runtime projects it in two directions:

```text
DirectorStructuredDecision
    ├─ ActionSurfaceRegistry → human-readable eight-field Mission
    └─ deterministic fact IDs/defaults → Frozen Mission artifact
```

There is deliberately no free semantic `human_clause` beside the typed clause. A second free-text clause would create two semantic sources that can disagree. `surface_note` is non-authoritative and ignored by both Mission rendering and Contract hash.

This native structured mode has schema/unit evidence only. It has not yet been run as the real production Director output protocol, so Story quality and latency are unproven.

## 7. Preservation by permission, not semantic classification

Default:

```text
blocked fact evidence = P42–P43
editable = P42–P43
locked = every other paragraph
```

The system does not need a global Desire Detector, Surprise Detector or Relationship Detector to protect P1–P41 and P44–end. They are simply outside the editing permission.

Only when the blocked paragraph itself carries valuable realization may a narrow exact fragment be protected. The fragment must remain inside the replacement payload for that paragraph; moving a duplicate elsewhere does not satisfy the map.

The map stores paragraph hashes and rejects a stale/changed Primary body. Primary evidence bindings are Runtime-issued and bound to the same Primary SHA-256; Curator cannot relabel a hint as evidence. Preservation validation also requires the current Contract hash and rejects paragraph-count shifts or locked-paragraph drift.

## 8. Critical historical claims

Do not require every remembered line of dialogue to exist in Authority. A historical claim becomes Hard only when typed Authority marks state-bearing history involving:

- money/resource commitment;
- relationship promise;
- mystery answer;
- current action basis;
- ownership transfer;
- active threat or obligation.

Ordinary family sayings and harmless memories remain prose freedom unless they collide with another frozen boundary.

## 9. Routing

Atomic is an acceleration layer, not a global hard gate:

```text
Atomic Contract preflight eligible?
        │
    ┌───┴───┐
    NO      YES
    ↓        ↓
Current Full  Normal Delta
Reviser       ↓
ungated      Supported Atomic Gate
              ├─ PASS → Final
              └─ FAIL → Full Reviser
                          ↓
                     Supported Gate
                       ├─ PASS → Final
                       └─ FAIL → residual failure
```

If the compiler does not support a chapter, the chapter follows the current production Full Reviser path. The same unsupported compiler may not reject the Full result.

## 10. Current evidence boundary

What is proven:

- source-pure static contracts can be constructed for two books/four chapters with the same ID/Fact schema;
- 4/4 static contracts are preflight eligible after explicit Canon pre-states are supplied;
- Curator/Primary do not enter hard sources;
- Edit Locality opens an average 3.11% of paragraphs and blocks outside edits 4/4;
- 57 focused negative/positive tests pass;
- four schemas and generated artifacts pass 22 bounded schema/runtime checks, including five expected-invalid probes;
- verbose/compact/micro free-text Sidecars are not acceptable output protocols.

What is not proven:

- a real Director can use native structured output without Story loss or latency increase;
- automatic Entity/Fact registry generation for a long novel;
- full-prose Contract closure from IDs without a new language parser;
- real cross-book Atomic Delta adoption;
- complete fallback-adjusted speed advantage;
- replacement of Full Reviser.

Production remains unchanged.
