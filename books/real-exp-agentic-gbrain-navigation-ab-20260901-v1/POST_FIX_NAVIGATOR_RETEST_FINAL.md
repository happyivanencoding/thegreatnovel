# Post-Fix Navigator Retest — Final Conclusion

Date: 2026-09-02
Branch: `principal_dev_new_sys`

## Question

After fixing personalized deterministic semantic retrieval, does `Full Retrieval Navigator -> fresh Story Program` still produce a reliable production-quality gain over the repaired deterministic retrieval?

## Experiment boundary

- A = repaired personalized deterministic semantic retrieval.
- B = Full Navigator with real multi-hop GBrain search, followed by a fresh Story Program.
- Same Frozen World / Power / Human per pair.
- Same Terra-high Story model for the 10 quality-attributable cases.
- Corrected blind Judge explicitly treats X/Y Story Program / RSE / reward / backfill as independent candidate output; only Frozen World / Character are Authority.
- The earlier integrated JIT shape remains excluded from production consideration because of runtime/context expansion problems.

## Effective quality-attributable cases

| Case | Winner | Gain over A | Notes |
|---|---|---|---|
| game_instance | B | MATERIAL | Both candidates still contain Authority/closure defects; not a clean Navigator win. |
| atlantis | A | NONE | A preserves Shen Lin's material/private desire ordering and lower complexity. |
| beast_h1 / Gu Ye | A | NONE | A better preserves rare-object vs departure tradeoff and avoids early Horizon exhaustion. |
| beast_h2 / Ruan Qinghe | B | MATERIAL | B creates stronger route-changing opportunity cost, but still needs tighter concrete payoff/level causality. |
| beast_h3 / Shang Yan | A | NONE | A keeps the main ruler much slower and preserves comfort/gambling/family-specific choice. |
| fallen_star_h1 / Lin Bozhou | B | MATERIAL | B's owned boat + relationship-based mobility produces stronger action-space and Book State Mutation. |
| heldout sky_chain | A | NONE | B has a Power/World pressure-use seam; A is safer and more Human-specific. |
| heldout world_tree | A | SMALL (B local strengths only) | A preserves the one-slot sacrifice and does not consume the current World Horizon too early. |
| heldout time_tide | B | MATERIAL | Cleanest B win: `opponent learning -> success-condition rewrite` closes a special Plot Engine gap A leaves open. |
| heldout star_ice | A | NONE | A correctly keeps current World NOT YET exhausted; B moves to macro expansion too early. |

Corrected blind-Judge tally:

- A wins: **6 / 10**
- B wins: **4 / 10**

The distribution matters more than the raw score. B's useful cases concentrate around situations where a special Plot Engine has a missing success condition or where a relationship/mobility asset can cause a genuine Book-level route rewrite. It is not a general Story Program upgrade.

## Held-out validation

Four entirely new protagonist-blind Worlds and separately frozen Humans were generated before A/B:

- `sky_chain`: suspended-island / pressure-flight world
- `world_tree`: giant-tree internal biological world
- `time_tide`: recurring ancient-war trace world
- `star_ice`: frozen drifting-sea / starfall world

Held-out result: **A 3 : B 1**. The only held-out B win was `time_tide`, where Navigator retrieved `opponent-learning-success-condition-rewrite` and the Story Program used it to make the opponent's observed counterplay force a new success condition before a legitimate Handoff.

This materially reduces the chance that the earlier result was caused by reuse of Atlantis / beast / instance structures.

## Sol-high real-Horizon retest

`ning_21_30` was attempted as the high-weight Sol-high Story Refresh retest.

However, after the retrieval fix:

- repaired fixed retrieval: `accepted_count = 0`
- Full Navigator: four searches, all `accepted_count = 0`, selected 0 cards

Both Sol candidates were therefore effectively generated without differentiating GBrain inspiration. The pair is **INVALID FOR RETRIEVAL ATTRIBUTION** and is not counted in the A/B tally. This is not evidence that Navigator lost; it is evidence that this Story Refresh retrieval query surface still has a coverage gap that must be studied separately.

## What changed versus the pre-fix experiment

The old quality tally is obsolete because the old Control was damaged by the Windows `.cmd` multiline-query boundary and by overly broad/empty semantic retrieval. After fixing that problem, A became substantially stronger and Human-specific on its own.

The repaired deterministic path now already provides much of what initially motivated Navigator:

- World-specific cards;
- Human-specific divergence inside the same World;
- longitudinal / reward / map / entry craft variation;
- deterministic category / Authority / active-inspiration boundaries;
- lower context and runtime cost than a separate search agent.

Thus Navigator no longer owns the main advantage of "different Humans receive different knowledge routes".

## Production decision

**DO NOT PROMOTE Full Retrieval Navigator as the default production path.**

Keep repaired personalized deterministic semantic retrieval as the production default.

Why:

1. It wins the majority of attributable cases (6/10).
2. It wins 3/4 entirely fresh held-out Worlds.
3. Navigator still increases planning cost and context.
4. Navigator repeatedly increases the tendency to over-consume current World depth, over-pack growth/rewards, or turn craft inspiration into an Authority seam.
5. The strongest Navigator gains are conditional rather than universal.

## Remaining useful hypothesis

The evidence supports a narrower future experiment, not a default agent:

**Conditional Plot-Engine Gap Querying**

If deterministic Story planning can explicitly identify one missing structural question (for example: "the opponent has learned the old solution; what changes the success condition?"), one short targeted semantic query may be useful. This should remain deterministic-boundary, low-frequency, and should not become an open-ended Navigator loop.

This is an experimental hypothesis only. No production wiring is authorized by this retest.

## Judge methodology correction

A prior judge prompt incorrectly risked treating candidate X's newly invented RSE as if it were frozen Authority when judging Y. That judgment shape is invalid. Final judges use this rule:

> X/Y independently propose Story Program / RSE / reward / legal backfill on the same Frozen World / Power / Human. Candidate-local inventions cannot be used as Authority against the other candidate.

This is an experiment-method correction, not a production Story rule change.
