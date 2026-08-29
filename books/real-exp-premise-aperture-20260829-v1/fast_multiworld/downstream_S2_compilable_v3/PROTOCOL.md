# Compilable Single-Pass S2 V3 Downstream Protocol

- The Forge prompt now requires an `Authority-Compilation Trace` inside the same non-Canon generation call.
- `S2` was pre-registered before the Forge response existed; no best-looking candidate was selected post hoc.
- All S1/S2/S3 cards must parse with World Interface, exact T0 Origin, Power trigger/coverage/boundary and Authority-Compilation Trace.
- The trace can expose causality but cannot authorize a missing rule.
- After author selection, code deterministically projects lane-specific frozen contracts.
- World sees World + protagonist-blind interface only.
- Power sees literal Ontology + exact Power only; no Origin/Biography/Story.
- Human sees literal Ontology + exact T0 Origin only; no special Power/Story.
- Story sees the complete selected card only after approved World/Power/Human.
- Every Authority stage must fail loudly with `PREMISE-AUTHORITY CONFLICT`; no later stage may start after a conflict.
- Power candidate 2 and Human candidate 2 are pre-registered.
- Outline consumes approved World/Character/Story and never receives the raw Premise Card.
- Production default is unchanged.
