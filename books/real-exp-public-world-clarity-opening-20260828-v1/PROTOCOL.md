# PROTOCOL｜Public World Knowledge Clarity Opening A/B

## Question

Can TGN make an unfamiliar fantasy world's PUBLIC COMMON KNOWLEDGE clear enough that a first-time reader can restate the rules without inference, while keeping hidden causes/reveals unknown and without turning Chapter 1 into an encyclopedia?

## Source Book

`books/real-exp-current-pipeline-authority-reviser-0010-20260828-v1`

Frozen approved inputs:
- Author Direction
- World Vision
- Character Authority / Initial State
- Story Program
- Outline GBrain retrieval bundle
- Chapter 1 Director Mission
- model/reasoning defaults

## Main Change

`Public World Knowledge = Clarity; Unknown World = Mystery`

No new Agent, Reviewer, schema, Reader State DB, Prelude, or exposition quota.

Treatment changes only:
1. World Vision explicitly distinguishes speakable public/common knowledge from hidden mystery;
2. Outline may schedule a 2–3 line Chapter 1 Public Common-Knowledge Reader Release bundle;
3. Curator must preserve those facts as directly speakable semantics rather than props/atmosphere;
4. Primary may state them in 1–3 short declarative exposition paragraphs without waiting for a fake action question;
5. Authority Reviser treats `texture present / rule missing` as an incomplete Reader Release and may restore minimum direct clarification.

## Isolation

Two detached worktrees from the same current HEAD are used:
- A Baseline: current HEAD unchanged.
- B Treatment: same HEAD with only `src/story_mvp/prompts.py` and `src/story_mvp/character_prompts.py` replaced by this task's treatment versions.

Parallel Scene Skill / other dirty worktree changes are excluded.

## Test 1｜Outline Scheduler

Generate one fresh Outline with B Treatment using Luna high and the exact frozen source inputs/retrieval bundle.

PASS target: Chapter 1 naturally receives 2–3 concrete Reader Release lines that tell the reader public/common facts such as main power/ruler/current-next tier meaning/daily danger/upward route, without revealing hidden causes or future discoveries.

## Test 2｜Matched Chapter Runtime A/B

Use the Treatment Outline's Reader Release Map to build one shared test BOOK. Both A and B receive this exact same BOOK and the exact same frozen Chapter 1 Director Mission.

Run in parallel:
- Luna high Curator
- Terra high Primary
- Luna high Authority Reviser

Thus the chapter A/B tests delivery/realization, not different story planning.

## Reader Restatement Criteria

Read final Chapter 1 and ask only facts actually relevant to this opening:
1. What is the world's main supernatural power/rule?
2. Where is the protagonist roughly on the power scale, and what does the next meaningful tier mean?
3. What daily danger/common rule changes how ordinary people live?
4. What concrete social/upward route or valuable opportunity is visible from the opening?

For B, a fact counts only if an ordinary reader can answer it directly from the prose; inference from firepits, clothing, architecture, positions, terms, or atmosphere alone does not count.

## Anti-overcorrection

B must also preserve:
- Chapter 1's original event order and Core Fantasy payoff;
- no hidden World reveal leakage;
- no full five-tier encyclopedia dump unless naturally necessary (it is not expected here);
- no extra setup chapter;
- no replacement of story action with exposition.

Verdict: PASS / DIRECTIONAL PASS / PARTIAL / FAIL, with explicit `What This Did Not Solve`.
