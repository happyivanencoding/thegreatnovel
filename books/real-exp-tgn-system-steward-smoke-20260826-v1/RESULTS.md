# TGN System Steward — Self-Distillation Smoke Test

## Verdict

**PASS**

The `tgn-system-steward` skill reproduces the intended audit process on a recent TGN system problem without reopening already-validated upstream authority or proposing new review machinery.

## Package

- Skill: `tgn-system-steward`
- Repository version: `0.1.1`
- AgentDock package validation: PASS
- AgentDock install/activation: PASS

## Smoke Case

Recent anonymous-prototype upstream experiment:

- current Outline;
- Stage 5 block-tax probe;
- current-production Story Program;
- first-principles Story Program;
- current product / Split Character docs.

Question: identify the smallest next system fix and decide whether upstream authority should be reopened.

## Attempt 1 — Useful Failure

The first prompt asked the Agent to dynamically inspect the live repository without a strict read budget.

Result: command timeout before final response.

Diagnosis: dynamic discovery had been specified too broadly. On a repository with many untracked experiment artifacts, the Agent could spend too long doing archaeology before answering the actual task.

This was treated as an Agent-design failure, not hidden.

Fix in `0.1.1`:

> **bounded live discovery** = git status/log + 2–4 task-relevant current docs + user-specified artifacts; expand only when evidence conflicts or is insufficient.

The Agent explicitly forbids recursive scanning of all `books/real-exp-*` by default.

## Attempt 2 — PASS

Model: GPT-5.6 Luna high

Wall time: ~188.6s

The Agent independently concluded:

> "最早剩余的语义坍缩主要发生在 Outline 编译，不在 World / Power / Human / Character / Story Program。不要重开已经验证的上游 authority。"

It identified the smallest fix as:

> Outline = concrete Story Anchors + optional `Block Delta`; unchanged dimensions are omitted instead of forcing every block to pay fantasy/progression/reward/world-expansion tax.

Concrete evidence it found:

- current methodology already says growth is longitudinal, not per-block tax;
- current Story Program permits a complete stage with no Power/Capability delta;
- Stage 5 probe explicitly says no new Power/Capability delta while still carrying meaningful choice, loss, relationship and world consequences;
- current Outline still repeats fixed fields such as core fantasy progression, primary growth, rewards, world expansion and costs for every block.

It correctly preserved as frozen:

- World Vision;
- Power Seed;
- Human Seed;
- deterministic Character composition;
- approved Story Program and growth grammar;
- private Human prototype as explicit-only, never global default.

It did **not** propose:

- new Agent;
- Reviewer;
- Scorer;
- Hard Gate;
- reopening validated upstream authority.

## Causal Experiment Proposed by the Agent

A: current Outline compiler.

B: only change the Outline contract so `Block Delta` records real changes and omitted dimensions remain absent.

Freeze:

- same World;
- same Character;
- same T0;
- same Story Program;
- same model / reasoning.

Test on:

1. Stage 5 block with no Power delta;
2. one block that genuinely contains Power growth.

Pass condition:

- B stops manufacturing filler progression/reward/world-expansion in the no-Power block;
- B still preserves genuine Power change when Story Program actually scheduled one.

## What the Agent Correctly Said This Would NOT Solve

- World independence quality;
- Human prototype quality;
- whether the author prefers the current-production or first-principles Story Program variant.

This is important: it did not use a downstream imperfection to invalidate already-passed upstream architecture.

## Acceptance Criteria

| Criterion | Result |
|---|---|
| Reads live current system rather than fixed snapshot | PASS |
| Protects concurrent worktree | PASS / read-only smoke |
| Finds earliest real semantic collapse | PASS |
| Distinguishes upstream architecture vs downstream compilation | PASS |
| Preserves already-validated authority | PASS |
| Prefers smallest fix | PASS |
| Avoids Agent / Reviewer / Hard Gate growth | PASS |
| Proposes causal A/B | PASS |
| States residual / unsolved problem | PASS |
| Keeps private prototype explicit-only | PASS |
| Revises its own bad discovery strategy after failure | PASS |

## Final Decision

`TGN System Steward` is ready for explicit use as the project's system-audit / evolution Agent.

It should **not** be inserted automatically into the novel production pipeline. That would add unnecessary calls and turn a stewardship tool into another production gate.

Use it explicitly for:

- system audits;
- architecture changes;
- experiment design / interpretation;
- GBrain governance;
- model-routing experiments;
- cross-layer bug diagnosis;
- implementation reviews;
- handoff preparation.
