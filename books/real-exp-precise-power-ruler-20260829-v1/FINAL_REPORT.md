# Precise Power Ruler + Public Proof Validation

Date: 2026-08-29

## Goal

Validate the new production rule that long-form TGN worlds must expose an exact reader-facing main power ruler, and that this ruler must drive all three Public Proof lanes without becoming a combat formula.

## Production topology under test

`World Root exact ruler grammar → Human T0 exact position → State Current Power Position → World Expansion range extension → Public Proof (Collective Shock + Ruler Calibration + Behavioral Repricing)`

The exact ruler is a Reader Ruler only. Skills, equipment, environment, experience and Power Asymmetry can still produce cross-level wins. A cross-level win does not itself update Current Power Position.

## Smoke A — 500-chapter World Vision

Model: GPT-5.6 Luna high

Direction: mature Chinese male-frequency fantasy planned for roughly 500 chapters; exact long-term power position should remain easy to read, while only the current World Horizon is concretely expanded.

Result: PASS after a parser fix.

The model produced:

- ruler type: continuous numeric;
- ruler name: `锚力阶`;
- exact format: `锚力{N}阶`;
- numeric grammar: `1—100`, every single rank recordable; rank 0 is the pre-cultivation position;
- current visible range: `1—60`;
- reader-facing major bands: `1—10 / 11—20 / 21—40 / 41—60`;
- `61—100` exists only as distant upper-scale knowledge, not as a full opening encyclopedia.

The generated World also explicitly states that exact rank is not a combat formula; technique, weapon, terrain, tide timing and matchup can create cross-rank outcomes.

Initial automated validation failed only because the parser accepted `当前大档位：value` on one line but not the model's natural multiline list under `当前大档位：`. The World itself satisfied the contract. The parser was fixed to support multiline production fields; the same unchanged output then passed the hard gate. The validator was not relaxed.

World generation wall time: about 170.7s.

## Smoke B — Exact ruler × three Public Proof lanes

Model: GPT-5.6 Luna high Authority Reviser

Frozen facts:

- protagonist: level 43;
- opponent: level 58;
- normal world rule: a five-level gap is already very difficult; this match crosses a ten-level social band;
- protagonist wins through approved asymmetry;
- the win does **not** cause a level-up;
- hundreds of students, teachers and three recruiters are already present.

The weak Primary intentionally contained only a generic pause, `这小子，有点东西`, and recruiters exchanging looks.

Treatment result: PASS.

The Authority Reviser restored all three lanes around the same exact ruler:

1. **Collective Shock** — hundreds of observers go quiet, discussion is cut off, then the stands erupt.
2. **Ruler Calibration** — the expert directly states `58级` vs `43级`, explains that even five levels is normally hard, and identifies that this crosses a whole ten-level band.
3. **Behavioral Repricing** — a recruiter physically replaces the ordinary registration plate and cancels the ordinary recruitment terms in favor of a formal top-school invitation.

The final prose also explicitly preserves: protagonist is still level 43. No false level-up was inferred from the cross-level victory.

Public Proof revision wall time: about 21.1s.

## Frozen production conclusions

- Exact main ruler is mandatory at World approval, not an optional style suggestion.
- Allowed root grammars stay deliberately simple: continuous numeric, major tier + numeric sublevel, or numeric sequence.
- Human Seed carries one exact T0 power position from the World ruler without seeing Power Seed.
- State carries `Current Power Position` as the first line of `Power / Capability`; a later State omission deterministically preserves the previous position.
- Macro World Expansion may extend visible range but may not rewrite ruler grammar.
- A true independent instance must have its own exact local ruler; that local ruler does not rewrite the global ruler.
- Exact ruler is a shared coordinate for Collective Shock, Ruler Calibration and Behavioral Repricing.
- Exact ruler is not a total combat score or deterministic fight calculator.
- Numeric milestone phrases such as `提升到43级 / 达到43级` are covered by existing conditional Outcome Fidelity repair.

## What This Did Not Solve

- This does not build a combat simulator, attribute database or total power score.
- It does not require every chapter to repeat the protagonist's number.
- It does not prove the optimal number of levels for every genre; it freezes exactness, not one universal 1—100 scale.
- It does not yet provide a 500-chapter E2E proof; long-horizon World Expansion and Current Power Position now have the authority structure required for that future pressure test.
