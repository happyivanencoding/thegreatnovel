# Transactional High Diff T1｜Frozen Derivation Protocol

> Derivation source: held-out novel 2 from prior Reviser-noop experiment. Frozen before T1 outputs.

## Hypothesis

Full Luna-high reasoning may still be necessary, but full-body regeneration may not be. Let high read the same full Authority + full Primary and emit only globally complete paragraph replacement transactions.

```text
full Frozen Authority + full Primary
        ↓ Luna high
transactional paragraph diff
        ├─ NO_CHANGE → Primary final
        ├─ PATCH → code applies all transaction patches atomically
        └─ ESCALATE_FULL → discard diff and use existing Full-high Reviser path
```

## Material difference from rejected 2026-08-29 Patch-only

Old Patch-only allowed independent local patches and produced a demonstrated contradiction: an object was pushed back in one paragraph while a later paragraph still said it had been accepted. T1 makes global dependency closure part of the output contract:

- every patch belongs to a named `domain` transaction;
- if changing a fact/status requires multiple mentions, all dependent paragraphs must be included in the same transaction;
- the model sees the full Primary, not a locality excerpt;
- if it cannot prove all dependent mentions are covered within the patch budget, it must `ESCALATE_FULL`;
- code applies all transactions atomically or none.

## Output contract

JSON only:

```json
{"disposition":"PATCH","transactions":[{"domain":"ownership:item_x","reason":"...","patches":[{"paragraph_id":12,"old_text":"exact full original paragraph","new_text":"one replacement paragraph"}]}]}
```

or `{"disposition":"NO_CHANGE","transactions":[]}`
or `{"disposition":"ESCALATE_FULL","transactions":[],"reason":"..."}`.

Rules:

- paragraph replacements only; no insert/delete/reorder/split/merge;
- `old_text` must equal the entire numbered Primary paragraph exactly;
- every changed Authority domain must sweep all dependent mentions before PATCH is allowed;
- max 8 changed paragraphs and <=20% of chapter paragraphs;
- preserve correct paragraphs verbatim; no synonym polishing;
- allowed reasons are the existing Reviser responsibilities: Frozen Authority conflict, required Reader Release/result/state/ending omission, named continuity, necessary World/Power/Human realization, or clear repetitive/procedural prose whose removal does not change story facts;
- never invent injuries, numbers, ownership/source, old history, hidden cognition or new power;
- if a necessary repair cannot be completed under these bounds, ESCALATE_FULL.

## Route timing

- NO_CHANGE/PATCH route wall = T1 call wall.
- ESCALATE_FULL route wall = T1 call wall + stored matched Full-high wall.
- Judges compare route final vs Primary vs Full-high.

## Acceptance gate before any new held-out novel

Across 2 repeats × 4 chapters:

1. route-final Story mean within 2 points of Full-high and no catastrophic output;
2. route-final Authority hard problems <= Full-high +2 and Authority mean within 3 points of Full-high;
3. parse/apply 8/8; unpatched paragraphs exact; paragraph count unchanged;
4. fallback-adjusted route wall saves >=40s/chapter vs Full-high mean;
5. no transaction leaves a same-domain contradiction identified by Authority Blind.

Fail any condition => stop; no third held-out novel.
