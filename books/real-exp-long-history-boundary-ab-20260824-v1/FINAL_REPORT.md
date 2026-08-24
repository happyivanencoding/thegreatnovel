# Long-History Fact Boundary 120 / 600 A/B — Final Report

Date: 2026-08-24

## Goal

Repair the long-form failure discovered by the 30 / 120 / 300 / 600 context-scaling experiment:

> Curator can correctly preserve an old mystery as unknown, but Primary may still turn a plausible explanation into retrospective canon while realizing the scene.

The repair had two intended responsibilities only:

1. **Director**: when a dormant character / promise / identity mystery / long-term secret returns, use the existing eight fields to state exactly what new fact becomes true in this chapter, and what older truth remains unresolved.
2. **Primary**: preserve unknown / unresolved historical facts as unknown. Present-tense realization is free; unapproved past history, hidden motive, fixed mechanism, prior knowledge or true identity is not.

No new Agent, reviewer, scorer, hard gate, database, Character subsystem or LLM call was allowed.

## Frozen inputs

The test reused the previous validated Index-first stress fixtures and froze:

- Chapter 120 synthetic Canon / packet;
- Chapter 600 synthetic Canon / packet;
- the prior real Luna-high Index Curator responses;
- the same approved current-chapter goals.

This means retrieval was not rerun and could not become a hidden variable.

## Model route

The current default chapter route was preserved:

- Director: **GPT-5.6 Luna, high**
- Curator: frozen output from **GPT-5.6 Luna, high**
- Primary Writer: **GPT-5.6 Terra, high**
- final blind judges: **GPT-5.6 Luna, high**
- raw GBrain: **OFF**

All real generation runs used fresh read-only ACP sessions through AgentDock / codex-acp with ChatGPT authentication.

## Baseline failure

### Chapter 120

The baseline Primary correctly received the authorized result “the real lighter is in Huideng Tower”, but then invented persistent mechanism/history such as:

- the third lamp cannot be lit arbitrarily;
- someone lit it on Jiang Lin's behalf;
- the jade token reacts because the lamp was lit;
- leaving the old city or handing over the token would cause the tower person to find him.

These are exactly the unsupported long-history facts the repair was meant to stop.

### Chapter 600

The baseline was substantially better than the older scaling sample, but still allowed unsupported historical explanation around Gu Huaisheng's changed position and old agreements. The pressure point remained useful because three dormant lines collide at once.

## Repair iterations

### V1 — prompt rule only

Added:

- Director long-history new-fact specificity;
- Primary unknown-history rule inside the prose contract.

Result: **NOT READY TO FREEZE**.

A Luna-high blind judge found that Chapter 120 still invented Huideng Tower / jade-token mechanisms and Chapter 600 could still assign a fixed past meaning to the `2-1-3` signal.

### V2 — move the fact rule to the top of Primary

The unknown rule became a high-salience `最高事实边界` in the Primary template. It also stated that Chapter Mission's authorized new fact is a factual ceiling, not an invitation to explain more.

Result: improved, but Chapter 120 still used dialogue to invent Ning Qingwu's return motive and Huideng Tower mechanics.

### V3 — “dialogue is not an escape hatch for Canon”

Added the explicit rule:

> **对白不是补 Canon 的逃生口。**

Any new statement that would be written by State Extraction into Persistent Canon must come from Canon or Chapter Mission when the topic is unresolved. Dialogue may still ask, refuse, admit uncertainty, express suspicion/stance, make a current request or make a current decision.

Result: Chapter 600 became clean, but Chapter 120 still showed that important unresolved facts were too deeply buried inside the full Curated Context.

### V4 — deterministic unresolved-fact projection

Final production design:

1. Curator remains unchanged as an LLM node.
2. Runtime deterministically extracts a short boundary from Curator output:
   - uncertain Curator Audit lines;
   - `Relevant Open Promises`;
   - explicitly unresolved World / Mechanism lines;
   - explicitly unresolved / not-yet-paid-off Payoff lines.
3. This becomes:

   `UNRESOLVED FACT BOUNDARY——仍未知/未兑现，不得由 Writer 补成旧史`

4. It is injected immediately after Chapter Mission and before Canon Prose.
5. No semantic model, embedding, RAG, tool call or additional LLM call is used.

Observed boundary size in the frozen fixtures:

- Chapter 120: **339 chars**
- Chapter 600: **325 chars**

So the repair increases salience rather than restoring full history.

## V4 outputs

### Chapter 120

The final Primary:

- keeps point-lighter identity unknown;
- keeps point-lighter motive unknown;
- does not explain the third-lamp mechanism;
- does not explain the jade-token mechanism;
- does not explain Ning Qingwu's disappearance or return motive;
- establishes only the authorized new fact: the real lighter is in Huideng Tower;
- turns the remaining scene pressure into current choices rather than more lore explanation.

Residual prose issue: one self-correcting phrase briefly emitted a backend chapter number (`第十八章……不，当年`). This is meta/prose hygiene, not new Canon.

### Chapter 600

The final Primary:

- does not explain why Gu Huaisheng changed position;
- does not assert that the tower signal is truly Shen Xuezhou;
- does not explain Ning Qingwu's return purpose;
- does not explain the red-cord origin or White Tower hidden mechanism;
- completes the authorized present fact: Jiang Lin enters the seventh floor while Gu's current position conflicts with the old oath.

## Blind evaluation

Two independent Luna-high judging passes were used.

The first final judge used cross-randomized labels per chapter. Its **per-chapter** scores were valid, but its Overall label aggregation was invalid because the same X/Y label did not represent the same system across chapters. After decoding:

- V4 won Chapter 120;
- V4 won Chapter 600;
- V4 received **Primary Unknown Discipline 5/5** on both stress points;
- no unsupported retrospective canon was found in either V4 sample.

A second final judge was therefore run with one anonymous label consistently representing the same system across both chapters.

Decoded result:

| Chapter | V4 Unknown Discipline | Baseline Unknown Discipline | Winner |
|---:|---:|---:|---|
| 120 | **5/5** | 2/5 | V4 |
| 600 | **5/5** | 3/5 | V4 |

The coherent blind judge explicitly concluded:

> **V4 is the Overall Winner and is FREEZE READY.**

Reader Quality remained 4/5 at Chapter 120 and 5/5 at Chapter 600, so the fact discipline did not collapse the prose into a rigid report.

## Decision

**PASS — freeze as `Long-History Fact Boundary v1`.**

The validated production behavior is:

- Director still has exactly eight fields;
- Director makes the chapter's newly true fact concrete and explicitly preserves unauthorized old truths as unresolved;
- Curator remains the same planning/context node;
- runtime adds a tiny deterministic unresolved-fact projection;
- Primary treats Chapter Mission as a factual ceiling for unresolved long-history material;
- dialogue cannot create persistent historical Canon that the Mission / Canon did not authorize.

This result does **not** justify adding Character Continuity Projection, a Continuity Reviewer, a Knowledge Matrix, a new specialist or full-history context.

## Residual risk

A small prose-hygiene issue remains: backend chapter-number phrases can very rarely leak into a self-correcting sentence when the Curated Context itself contains chapter labels. This did not create false Canon and did not block the blind judge's freeze decision. It should be handled later as ordinary Planning-Language / diction hygiene, not by expanding continuity architecture.

## Artifact map

Each `chapter-0120/` and `chapter-0600/` directory retains:

- frozen packet and Curator response;
- `A_before_*` baseline Director / Primary prompts and responses;
- `B_after_*` Director repair artifacts;
- intermediate V2 / V3 Primary artifacts;
- `E_after_v4_unresolved_projection.md`;
- final V4 Primary prompt / response;
- ACP metadata for real runs.

Root includes:

- baseline / intermediate / final Primary template snapshots;
- first failed blind evaluation;
- final blind judge prompts, mappings and responses.
