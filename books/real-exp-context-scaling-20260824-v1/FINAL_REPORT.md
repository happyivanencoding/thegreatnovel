# Context Scaling 30 / 120 / 300 / 600 — Final Report

Date: 2026-08-24

## Question

Can the current TGN deterministic Index-first → Curator → Primary architecture remain usable hundreds of chapters into a novel, or does long history require a new Character Continuity / heavier memory subsystem?

A secondary question emerged during the run: when long-dormant mysteries return, does the main continuity failure occur in retrieval/Curator or in Primary prose generation?

## Model route

The test used the current default chapter models:

- Curator: **GPT-5.6 Luna, high**
- Primary Writer: **GPT-5.6 Terra, high**
- raw GBrain: **OFF**
- Scene Skills: current catalog available to Curator and compiled into Primary as usual

All ACP sessions were fresh and read-only.

## Synthetic long-form snapshots

Four frozen snapshots were constructed:

- Chapter 30: one early dormant promise.
- Chapter 120: character return after ~90 chapters plus an old promise.
- Chapter 300: identity / object line with an old counterfeit clue.
- Chapter 600: three long-running lines collide — Ning Qingwu / third lamp, Shen Xuezhou / bronze mirror, Gu Huaisheng / White Tower oath.

Hundreds of irrelevant resolved records were added as deterministic noise. Relevant old facts and explicit unknowns were placed in the synthetic Canon.

Each chapter compared:

1. **Full** — Curator receives the full synthetic Canon text.
2. **Index** — Curator input is produced by the current production `build_curator_context()` / `_project_indexed_text()` implementation.

Both then generated a real Curator response and a real Terra Primary response.

## Input scaling

| Chapter | Index Curator prompt | Full Curator prompt | Index reduction | Index Primary prompt | Full Primary prompt |
|---:|---:|---:|---:|---:|---:|
| 30 | 8,199 | 8,186 | n/a | 7,424 | 7,458 |
| 120 | 10,659 | 15,474 | 31.1% | 7,320 | 7,444 |
| 300 | 6,054 | 29,684 | 79.6% | 7,693 | 7,609 |
| 600 | 6,316 | 53,619 | **88.2%** | 7,849 | 8,053 |

At Chapter 600 the current deterministic projection reduced the Curator prompt by about **88%**, while the downstream Primary prompt stayed around 8k characters for both variants.

Curator response size also stayed approximately flat instead of growing with history:

- Ch30: ~1.8k chars
- Ch120: ~1.8–1.9k
- Ch300: ~2.0–2.1k
- Ch600: ~2.2–2.4k

The ACP `usage_update.used` counter showed the same engineering direction at the Curator stage (this counter is **not** treated as billing cost):

- Ch600 Index Curator: 34,857
- Ch600 Full Curator: 73,397

Primary usage stayed similar after Curator compression.

## Retrieval / Curator findings

### Chapter 120

Index-first preserved the facts that actually mattered to the current chapter:

- the Chapter 18 Ning Qingwu promise;
- the Xuanlu jade token;
- the third lamp;
- Ning Qingwu's return after a long absence;
- the current payoff window.

The Curator did not drag the synthetic resolved side records downstream.

### Chapter 300

Index-first retrieved the bronze-mirror identity line and the earlier counterfeit clue. However, this snapshot contains an **experiment construction defect**: one synthetic fact said that only Shen Xuezhou knew the true `2-1-3` scratch order, while the frozen chapter mission simultaneously required Jiang Lin to use that scratch information to judge identity. That internal contradiction caused materially different conflict handling between the two Curators.

Therefore **Chapter 300 is excluded from any Index-vs-Full winner claim**. Its artifacts are retained because they are still useful evidence about conflict handling, but it is not a clean architecture comparison.

### Chapter 600

The Index Curator successfully retained all three deliberately long-dormant lines at once:

- Ning Qingwu / third lamp / jade-token line;
- Shen Xuezhou / `2-1-3` signal line;
- Gu Huaisheng / Chapter 411 White Tower oath.

Crucially, it also explicitly preserved the unknown boundary:

- why Gu Huaisheng changed his position was unknown;
- whether the tower signal was really Shen Xuezhou was unknown;
- why Ning Qingwu returned at that moment was unknown.

So the stress test did **not** show a Chapter-600 Curator memory collapse.

## Primary failure discovered

The most important result was downstream.

In the Chapter 600 Index variant, the Curator correctly said the three core mysteries were unresolved, but Primary nevertheless invented persistent past-history facts such as:

- prior White Tower memory-loss history for Gu Huaisheng;
- an unprovided old reason behind Shen Xuezhou's `2-1-3` signal;
- an unprovided origin and mechanism for Ning Qingwu's red cord.

The Full variant did the same kind of thing with different invented details, including extra old interactions and hidden knowledge not present in frozen Canon.

Therefore this failure **is not caused by Index-first compression**. More history did not solve it.

The pattern is:

> Curator preserves uncertainty → Primary wants to complete a satisfying scene → Primary converts plausible explanation into retroactive canon.

This gets more dangerous at long scale because there are more dormant mysteries available for prose to “explain”.

## Blind evaluation

Two independent Luna-high judges received randomized X/Y labels. They saw the frozen ground-truth/mission plus both Curator and Primary outputs and were asked to judge long-memory recall, unknown discipline, consistency, story focus, reader quality and contract fidelity.

Both judges independently concluded:

- Reader quality remained generally strong even at Chapter 600.
- Curator quality did **not** show the same scale-driven collapse as Primary.
- Primary increasingly invented convincing old history / mechanisms behind unresolved threads.
- The principal bottleneck is **Primary unknown-discipline / upstream event specificity**, not insufficient raw context.

Winner labels are not treated as the main result because:

1. Ch30 is below the projection threshold and Full/Index input size is effectively the same.
2. Ch300 contains the synthetic contradiction described above.
3. At Ch600 the two blind judges split on which prose version they preferred, while both identified the same Primary continuity failure.

The robust comparison is therefore architectural rather than a simple win count.

## Experiment limitations

Two limitations are explicitly retained rather than hidden:

1. **Chapter 300 synthetic contradiction.** It invalidates the clean Index-vs-Full winner comparison for that chapter.
2. The blind-judge ground-truth summary did not repeat every stable BOOK CONTRACT world rule, so judges occasionally flagged a Curator sentence inherited from Book Contract as “unsupported”. Those flags are not counted as evidence of hallucination when the source prompt actually contained the rule.

Neither limitation changes the core Chapter-600 observation: both Curators marked major historical causes as unknown, while both Primaries nevertheless created retroactive explanations.

## Decisions

### 1. Index-first deterministic retrieval: PASS

Current evidence supports keeping the existing architecture.

At Chapter 600 it cut the Curator input by ~88% while still surfacing the deliberately planted long-term facts needed by the scene. There is no evidence here that Full Context is required for better long-form continuity.

### 2. Character Continuity Projection: NOT JUSTIFIED YET

This experiment does **not** justify adding a new Character subsystem now.

The Curator was able to recover the relevant long-term character/relationship facts at Chapter 600. Adding a larger Character ledger would not address the primary failure observed in the generated prose.

### 3. Next repair target: Primary / Director boundary

The earliest useful repair is smaller than a new memory architecture.

Recommended direction:

- Treat Curator-listed `unknown / unresolved / open promise` facts as **not resolvable by Primary unless the Chapter Mission explicitly resolves them**.
- Primary may invent present-tense realization details (gesture, immediate evidence, dialogue wording, physical action) but should not invent persistent events that supposedly happened dozens or hundreds of chapters earlier.
- Director Contracts for major old-line payoffs should state the **new fact / irreversible result of this chapter** concretely enough that Primary does not have to become a planner and choose the hidden explanation itself.
- Do not add a new reviewer, scorer, continuity agent or hard gate for this problem before testing the narrower prompt/contract repair.

## Overall conclusion

The 600-chapter stress test changes the diagnosis.

The current TGN memory architecture is not presently failing because it cannot retrieve enough history. In this synthetic test, **Index-first retrieval scaled well and retained the relevant old lines**.

The more serious long-form risk is:

> **a fluent Primary Writer turning unresolved long-term history into plausible but unsupported canon while realizing the current scene.**

That should be repaired at the Primary / Director semantic boundary before adding a heavier memory subsystem.

## Artifacts

For every snapshot directory:

- frozen `packet.json`
- Index / Full Curator prompts and responses
- Index / Full Primary prompts and responses
- ACP metadata

Root evaluation artifacts:

- `CURATOR_MANIFEST.json`
- `PRIMARY_MANIFEST.json`
- `blind_context_judge_1_*`
- `blind_context_judge_2_*`
- `tools/generate_inputs.py`
