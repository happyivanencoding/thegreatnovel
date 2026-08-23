# Story-bearing Texture Frozen A/B — Final Report

Date: 2026-08-24

## Question

Does the new Primary Writer direction `Story-bearing Texture > Decorative Density` improve TGN prose without mechanically increasing length, adding AI-style ornament, or turning mechanisms into procedural explanation?

## Frozen design

Five materially different scenes were reused from previous real TGN runs:

1. `S1_negotiation` — negotiation / entry-status gate.
2. `S2_combat_payoff` — public combat / status payoff.
3. `S3_reward_status` — high-value acquisition / identity change.
4. `S4_relationship_choice` — relationship choice under pressure / aftermath.
5. `S5_large_payoff` — large stage payoff.

For every scene:

- same original Primary prompt;
- same Director Contract, Curated Context and Scene Skills already embedded in that prompt;
- same model: **GPT-5.6 Terra, reasoning high**;
- separate fresh read-only ACP sessions;
- A = original prompt;
- B = original prompt + only the Story-bearing Texture direction;
- no replanning and no production file changes.

Two independent **GPT-5.6 Luna high** blind judges received randomized X/Y labels and were not told which output was baseline or texture. Judges were told not to reward length or ornament.

## Output length

| Scene | Baseline chars | Texture chars | Change |
|---|---:|---:|---:|
| S1 negotiation | 2,694 | 2,231 | -17.2% |
| S2 combat payoff | 2,351 | 3,232 | +37.5% |
| S3 reward/status | 4,461 | 3,713 | -16.8% |
| S4 relationship choice | 3,490 | 3,344 | -4.2% |
| S5 large payoff | 4,483 | 3,826 | -14.7% |

The rule did **not** behave like a generic “write more detail” instruction. Four of five Texture outputs were shorter. The combat scene was the exception.

## Blind results

After decoding the randomized labels:

- Judge 1: Texture won **4/5**; baseline won only `S2_combat_payoff`.
- Judge 2: Texture won **5/5**.
- Aggregate: **Texture 9 wins / Baseline 1 win**.

Unanimous Texture wins:

- negotiation;
- reward / identity payoff;
- relationship choice;
- large stage payoff.

Split result:

- combat / action.

## What improved

Across the two judges, the Texture version was repeatedly preferred when the extra detail was attached to story-bearing objects, spatial relationships, bodily pressure, visible payoff and differentiated reactions. It often made a scene more concrete **while shortening explanation**.

The strongest gains were not literary ornament. They were things such as:

- a status change becoming a physical object or public action;
- a reward actually arriving in hand;
- a relationship decision changing what people do next;
- a large payoff changing the usable space and other characters' options.

This matches the intended TGN principle: `克制但不干，丰富但不腻`.

## Main risk found

The combat case exposed the exact failure mode that still needs guarding.

When “more concrete detail” attaches to:

- force paths;
- step-by-step mechanics;
- technique decomposition;
- repeated explanation of why an action works;

Story-bearing Texture can regress into procedural expansion. Judge 1 preferred the baseline combat output for this reason; Judge 2 still preferred Texture but independently identified the same risk.

Therefore the useful refinement is **not** “more combat detail”. It is:

> Increase texture on decisive beats, bodily consequence, opponent reaction and visible result; keep mechanism explanation compressed.

## Decision

**PASS. Keep Story-bearing Texture as a production principle.**

Evidence is strong enough that the principle itself should not be reverted. The only follow-up candidate is a narrow Action/Combat wording refinement; this experiment does not justify adding a new agent, reviewer, scorer or hard gate.

## Artifacts

Each scene directory contains:

- `A_baseline_prompt.md`
- `A_baseline_response.md`
- `B_texture_prompt.md`
- `B_texture_response.md`
- ACP metadata for every run

Blind evaluation artifacts:

- `blind_judge_1_prompt.md`
- `blind_judge_1_mapping.txt`
- `blind_judge_1_response.md`
- `blind_judge_2_prompt.md`
- `blind_judge_2_mapping.txt`
- `blind_judge_2_response.md`
