# Reviser No-Op Upstream｜Held-out Novel 2 Protocol

> Candidate 2 is frozen before Held-out Novel 2 is generated. Held-out Novel 1 is now derivation evidence and may not be used to retune this candidate after generation starts.

## Hypothesis

The previous generic Primary self-check failed because it asked Terra to infer final correctness from a lower-salience / incomplete Authority view. Test a source-pure, zero-call alternative: **Runtime Final Facts Projection**.

Do not tell Primary how to revise itself. Do not add a Reviewer. Do not expose the full Atomic Contract. Runtime only repeats a few already-frozen facts at the end of the existing Primary prompt, close to generation:

```text
## FINAL FACTS PROJECTION｜Runtime deterministic; no new story facts
Direct Result: <exact Director frozen field>
State Change: <exact Director frozen field>
Ending: <exact Director frozen field>
Scheduled Reader Release: <exact chapter-matched Reader Release lines, or NONE>
Core Power: <POWER SEED / 一句话大白话>
Permanent Power Boundary: <POWER SEED / 永久边界>
```

No new instruction checklist follows this block. The normal Primary contract still governs prose.

## Source rules

- Direct Result / State Change / Ending are parsed by exact Director field labels, not semantic NLP.
- Reader Release is read by exact chapter number from the approved BOOK `Reader Release Map`; if no line matches, output `NONE`.
- Core Power / Permanent Boundary are exact bounded sections from approved `POWER_SEED.md`.
- No Curator or Primary text may create a projection fact.
- No Chinese synonym parser, classifier, or LLM call.
- The projection is not Authority creation; it is attention placement of already-frozen Authority.

## Derivation split

Candidate 2 was motivated by:
- 九垂原 / 分影 Primary→Reviser pairs;
- Held-out Novel 1 failure of generic self-check and source-diff showing Reviser-only Power Core / high-salience terminal facts.

## Held-out Novel 2

Generate a second entirely new novel after this protocol hash is frozen. It must not use:
- 九垂原 / 潮路 / 回潮楔 / 分身;
- 烬星洲 / 星力阶 / 远身 / remote-controlled weapon;
- contract/logistics as the core premise.

Take the first four consecutive chapters. No chapter selection after reading outputs.

## A/B

Same Director, same Curator, same Primary base prompt.
- Control Primary: current prompt.
- Treatment Primary: current prompt + deterministic Final Facts Projection.
- Both then go through the same Luna-high Authority Reviser.
- Control Reviser Final alone advances Canon for the next chapter.
- Independent repeat uses frozen chapter inputs.

## Success

Directional pass requires all:
1. Treatment Primary Story does not regress materially.
2. Treatment Primary Authority improves or ties.
3. Treatment reduces `Reviser - Primary` Story/Authority gap or increases exact/no-op/similarity evidence.
4. Treatment does not increase Primary wall materially.
5. Treatment Reviser Final does not regress.
6. Result repeats across the four chapters rather than depending on one chapter.

Even a pass only justifies a third-book replication before production changes.
