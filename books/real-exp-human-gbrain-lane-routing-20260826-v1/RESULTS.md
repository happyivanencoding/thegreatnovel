# Human GBrain One-Lane-One-Card Routing Experiment

## Verdict

**PASS — route change is correct; no Luna generation A/B is justified yet.**

Live GBrain snapshot: **3802 Pages / 15810 Chunks / 15810 Embedded**. Human Craft v2 second+third batch is complete, but all eight new book DNA cards are `REFERENCE_ONLY / active_inspiration:false`; v1 `private-appetite-continuity-v1` remains the only ACTIVE Human-specific cross-book mechanism.

## Live before / after

### Before: unified candidate pool, Top 3 total

- accepted: 1
- `private-appetite-continuity-v1`
- no explicit lane ownership

### After: three independent lane queries

- Appetite: 1 — `private-appetite-continuity-v1`
- Behavior: 0
- Relationship: 0
- total: 1 / max 3

The new router therefore does **not** change the actual Human craft content currently sent to Luna, except for explicit `human_lane: appetite` metadata. Running Human Seed generation now would measure sampling noise, not lane routing.

## Controlled regression

`tests/test_character_production.py` now verifies:

- two Appetite cards can never consume two slots;
- a cross-hit Appetite card cannot occupy Behavior or Relationship;
- Behavior and Relationship each accept at most one card;
- the same slug cannot occupy two lanes;
- REFERENCE_ONLY / inactive cards do not fill a lane;
- wrong-lane cards do not fill a lane;
- empty lanes remain empty instead of weak-card backfill;
- final Human limit remains 3.

## Production rule

`Human Seed = Appetite <= 1 + Behavior <= 1 + Relationship <= 1`, with total `<= 3`.

These are retrieval budgets, not personality requirements or Hard Gates.
