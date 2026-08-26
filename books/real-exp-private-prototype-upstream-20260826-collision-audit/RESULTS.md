# System Eval 16 — Split Authority / Human / Collision Root-Cause Results

Date: 2026-08-26
Branch: `principal_dev_new_sys`

This report records architecture experiments only. Model-selected experiment fixtures are not author-approved Canon.

## 1. What this batch was actually testing

The target was not to patch individual bad generations. The target was to identify the earliest system layer that structurally recreates previously observed failures on a completely new book.

Observed historical failures included:

- Character biography becoming a retrospective justification for the protagonist's Power or one elegant personality thesis;
- world / ability semantic isomorphism;
- engineering / governance / procedure becoming story engines;
- Fantasy Engine consuming the protagonist's life and the world's independent events;
- Story Program turning every large stage into capability iteration + acquisition + compounding paperwork.

The architecture under test was:

`protagonist-blind World -> independent Power + Human -> deterministic Character -> Story Program first collision`

## 2. Upstream progress recovered from v1 / v2 / v3

### v1

Validated the isolation idea: the explicit anonymous Human prototype could enter the Human lane without leaking into Power generation. Power and Human remained mutually blind.

### v2

Failed at World. The new world collapsed back into a tide / earth-vein / flow-routing ontology. This was rejected rather than repaired downstream.

### v3

A fresh world fingerprint produced the `百铸身` world. World blind audit returned `PASS_WITH_RISK`: it had independent people, conflicts and spectacle, but still risked material / implant / repair proceduralization and numeric-level table thinking.

Power blind selector, without Human visibility, selected candidate 3 `离印`. Human prototype projection remained power-blind. Human fidelity audit returned `PASS_WITH_RISK` and exposed a new problem: biography / occupation facts were arranged too neatly to prove one life philosophy.

## 3. Traditional cultivation control

A second protagonist-blind world was generated with Luna high using a deliberately traditional cultivation direction: cultivation methods, meridians/dantian/spirit, flying swords, techniques, artifacts, sects, secret realms and concrete combat / exploration progression; no body-material-engineering ontology.

Generation:

- World: Luna high, 130.967s;
- Power: Luna high, 87.173s;
- explicit-prototype Human: Luna high, 98.644s.

Power candidates were `分流真元 / 回流真元 / 术种封存`; independent Power selector chose candidate 1 `分流真元`.

World blind audit again returned `PASS_WITH_RISK`. The risk changed from engineering/material procedure to the classic cultivation treadmill: `sect task -> secret realm -> resource fight -> promotion -> bigger map`.

This control matters because it demonstrates that procedural sameness is not only an engineering-world problem. Any progression world can be swallowed by a bad Story compiler.

## 4. Real implementation bug found during isolation

`project_character_life_context()` stripped named mysteries only when the World wrote exactly:

`当前没人能完整解释的事实：`

A real generated World used:

`当前没人能完整解释的事实包括：`

This leaked named Story Opportunities into Human `LIFE_CONTEXT`, violating the frozen information boundary.

Fix: accept the real supported wording with optional `包括`; regression test added. This is an implementation-boundary bug, not a literary patch.

## 5. Human root cause

### Baseline production Human control

On the same traditional World, current production Human generation (Luna high, 104.671s) produced four candidates. All four showed the same structural tendency:

`childhood / family / occupation fact -> explicit adaptation -> current behavior -> one Core Obsession`

Examples included:

- disappearance / unfinished departures -> “people who leave must have somewhere to return”;
- contract-family euphemism -> “must hear the truth”;
- mining productivity + abandoned carving -> “make useless things perfect”;
- privileged family planning every choice -> “do not live a life arranged by others”.

This reproduced across a fresh traditional world, so it was not an explicit-private-prototype quirk.

### First-principles Human A/B

Same World, same Luna high, same Human GBrain, same number of calls. Only the Human data model changed.

New model:

`Lived Facts -> Competing Motives -> Stable Choice Bias under conflict -> Person-specific Relationships`

Traditional control: Luna high, 83.839s.

Result: biographies became life context rather than proof. Candidates could simultaneously want money, aesthetic objects, status, physical desire, curiosity, family security, winning, freedom, etc., with real conflicts between them.

The same structure was projected through the explicit anonymous prototype in the `百铸身` world (Luna high, 77.513s) and likewise preserved appetite / sexuality / relationship variables without reducing everything to one `freshness / being seen` life thesis.

### Human production conclusion

Replace the Human schema itself. Do not add a “don't over-explain your childhood” patch after generation.

Current production Human authority now uses:

- concrete lived facts;
- competing motives;
- Stable Choice Bias + Variable Realization;
- person-specific relationship variables;
- T0 desire as mutable state;
- audition hook as non-Canon.

No new Agent, scorer, reviewer, state database or LLM call was added.

## 6. Story Program root cause

### Legacy contract symptoms

Traditional `分流真元` baseline with old Story Program contract:

- Sol high;
- 809.223s;
- 1143 output lines;
- generated the complete Story Program twice;
- each stage structurally had to pay `Power participation / first-tier growth / acquisition / net-new / next-stage` fields.

The same old contract on `百铸身 + blind-selected 离印` ran for more than 15 minutes and timed out without an artifact.

A separate old-contract `百铸身 + 活相` sensitivity run completed, but almost every phase still carried mandatory progression/acquisition fields. World and Human content survived, yet Fantasy Engine retained structural ownership of each stage.

### Native Collision A/B

Holding World, Character, Story GBrain and Sol high fixed, only the Story Program compiler was replaced by a native Collision contract.

Traditional control:

- 778.434s;
- 188 lines;
- one Story Program only;
- `万灯不等人`: protagonist permanently loses the Sword Pool opportunity and gets no new ability;
- `寒关两边`: no new signature ability, no drop, no breakthrough; war / relationship / choice still make a complete stage.

`百铸身 + 离印`:

- 485.207s;
- 171 lines;
- one Story Program only;
- `白盐海`: world conflict remains the primary engine and no new Power form is forced;
- `无面案`: relationship + mystery can drive a complete stage while Power serves the action;
- growth still reaches a concrete 100-level `万铸身` trajectory.

Independent Luna high root audit concluded that the legacy Story Program contract was the earliest reproducible semantic collapse point in this comparison. It explicitly recommended changing Human schema + Story compiler, and not adding new World / Power / Outline rules.

## 7. Final correction: growth is not removed

The native compiler was then refined after architecture review.

Final invariant:

> **Growth is a longitudinal invariant, not a per-stage form requirement.**

And:

> **Acquisition and compounding are optional stage outcomes, but persistent story consequences when they occur.**

This separates authority from scheduling:

- Power Seed = growth grammar;
- Story Program = growth realization through story.

Power Seed still owns normal progression, exception mastery, high-tier mutation, permanent boundary and legendary state. Story Program cannot rewrite them, but it must decide where those approved possibilities become concrete story facts.

Current Story Program therefore contains a global `全书成长与核心幻想兑现脊柱` with 4–6 observable transformations distributed across early / middle / high-tier story, while individual stages use only:

1. why now;
2. who wants what;
3. protagonist choice/action;
4. primary reading satisfaction;
5. Stage Delta;
6. why the next stage follows.

`Stage Delta` writes only dimensions that truly changed: Power/Capability, Possession, Relationship, Identity/Access, Knowledge, Enemy State, World State, etc. A stage may have no Power change and no Possession change.

High-Value Acquisition remains a reader-appetite principle, not a stage field. Compounding remains “past gains continue to change future story”, not a per-stage `Compounding Growth` form.

## 8. Final production revalidation

### 百铸身 + blind-selected 离印

Current production contract, Sol high:

- 239.848s;
- 8482 text chars;
- one valid Story Program;
- all seven stages use Stage Delta rather than mandatory growth/acquisition forms.

Important evidence:

- Stage 5 explicitly gains no old-tomb high-tier spectrum and stabilizes in the 70s using existing body divisions and combat experience; the stage still works through home destruction, parents' choice, relationship change and royal politics.
- Whole-book progression remains concrete: first separated body part -> multi-part operation -> distributed senses -> layered local battle bodies -> molt / field-control -> level-100 `万铸身`.
- Compounding is observable: the naturally shed leader-beast heart armor gained in Stage 3 is still used in Stage 4 to stop a bolt aimed at the protagonist's core body.

This is the intended shape: local no-upgrade is legal; longitudinal no-growth is not.

### Traditional cultivation

Current production contract, same frozen traditional World / `分流真元` Character / Story GBrain, Sol high:

- 441.284s;
- 9020 text chars;
- one valid Story Program;
- seven stages, each using only actual Stage Delta dimensions.

Important evidence:

- Stage 5 (`开山之后，没有他的位置`) has **no Power / Capability delta at all**. It is driven by sect succession, ownership of the Black-Sun route, Lu Huichuan's refusal of a stable True Disciple position, and his changed relationship with Shen Yanqiu. The stage remains complete without a breakthrough.
- Whole-book progression remains distributed and concrete: first ten-second dual flow -> Foundation-stage adjustable ratios while sword-flying -> Golden-Core heterogeneous spells + recombination strike -> Nascent-Soul remote sword + body movement -> Void-stage multi-position coordination -> Tribulation-stage multi-trajectory legendary recombination. The story does not merely declare future growth; early / middle / high-tier changes are observable.
- High-Value Acquisition is optional but real when it occurs: the Fire-Marrow sword embryo in Stage 3 is fought for, contractually delivered and forged into the long-term sword `照水`; it continues to participate in Black-Sun exploration, northern war and the final Heaven-Gate fight rather than disappearing after the acquisition arc.
- The small private desire also compounds narratively: the postponed East-Sea trip from Stage 1 returns in Stage 4 as an actual ten-day life choice, and choosing to complete it costs the protagonist the safest first expedition slot instead of being retrofitted into an upgrade reason.

This independently confirms the final shape on a second, conventional cultivation world: a local stage may carry no Power delta, while longitudinal progression and recurring Core Fantasy payoff remain mandatory.

## 9. Production changes supported by evidence

1. **Human authority model replaced at the root**
   - removed `Formative Fact -> Adaptation -> Observable Behavior` as the mandatory output structure;
   - removed `Core Obsession + Excess` as required singular personality architecture;
   - added lived facts + competing motives + Stable Choice Bias + person-specific relationships.

2. **Story Program compiler replaced at the root**
   - removed the legacy per-stage growth/acquisition/compounding form;
   - added global observable growth + periodic Core Fantasy spine;
   - added lightweight causal stages + Stage Delta;
   - retained High-Value Acquisition and Compounding as longitudinal craft principles.

3. **Information-boundary implementation bug fixed**
   - `LIFE_CONTEXT` now strips the real generated named-mystery heading variant.

4. **No extra system layer added**
   - no new Agent;
   - no production Reviewer;
   - no scorer;
   - no new Hard Gate;
   - no extra LLM call;
   - no extra long-term state database.

## 10. What was deliberately not productionized

- the proposed World “orthogonal deletion test” patch;
- the proposed old Fantasy-Seed Behavior wording patch;
- a per-stage High-Value Acquisition field;
- a per-stage Compounding Growth field;
- a mandatory Power Delta per stage;
- a Character Composer LLM.

Those would reintroduce either symptom-level rules or the same form pressure the experiments identified.

## 11. Outline block-tax follow-up

After Human and Story Program were frozen, the next audit targeted the current production Outline contract rather than adding another upstream rule.

### Current-contract evidence

The legacy Outline block shape still required every block to answer `核心幻想推进 / 一级成长变化 / 收益与反哺 / 世界扩张`, even after Story Program had made Power and Acquisition optional per stage.

On the frozen traditional cultivation Story Program:

- a full current-contract Luna high Outline produced eight blocks for chapters 1–36; all 8/8 filled `一级成长变化` and all 8/8 filled `世界扩张`;
- a focused Stage 5 single-block probe did not invent a new Power upgrade, showing Luna could resist the pressure when the upstream no-Power stage was explicit;
- a harder Stage 5 three-block probe exposed the actual failure: all 3/3 blocks still filled `一级成长变化`, but with non-Power material such as clearer identity boundaries, more explicit negotiation, or willingness to own a failed trade-off. Character maturation was being relabeled as first-tier growth solely because the form demanded an answer;
- `世界扩张` similarly drifted into institutional position / political access even when no new geography, power tier or world layer had opened.

This is semantic form pressure even when it does not fabricate a literal new skill.

### Block Delta A/B

Holding the same Stage 5 facts fixed, the block contract was changed to:

- concrete Story Anchors;
- one `主要阅读兑现`;
- `Block Delta` containing only dimensions that actually changed relative to the start of that block;
- optional cost/aftermath;
- causal handoff to the next block.

Allowed Delta dimensions mirror the Story Program vocabulary: `Power / Capability`, `Possession`, `Relationship`, `Identity / Access`, `Knowledge`, `Enemy State`, `World State`.

Result on the same three Stage 5 blocks:

- block 1: Relationship + Knowledge only;
- block 2: Enemy State + Knowledge only;
- block 3: Possession + Relationship + Identity / Access + World State;
- no Power Delta was invented in any block;
- the real high-value acquisition (the no-expiry cultivation continuation) still arrived where the approved story actually caused it.

A fidelity control on Stage 2, where the approved Program truly contains Foundation breakthrough, preserved the real growth: the breakthrough block correctly emitted `Power / Capability`, formal cultivation method possession, relationship change and enemy-state change. The preceding block, which had no breakthrough, did not invent one.

### Production revalidation

After moving production Outline to the actual-only Delta contract, a fresh Luna high run on the frozen traditional inputs completed in 227.821s and produced one valid Outline (8657 text chars).

The model naturally chose only two blocks for the current executable window, chapters 1–20, rather than mechanically filling a target block count:

- block 1 records the real `引灵 + 双股真元` Power change;
- block 2 records the real `筑基 + 御剑时并行施法` Power change;
- no micro-upgrade fields or per-block world-expansion fields exist anymore.

Together with the Stage 5 focused A/B, this validates both sides of the contract: **real approved growth is preserved when it happens; no-growth blocks are allowed to remain no-growth.**

Final Outline invariant:

> **Outline is Story Program execution, not rescheduling. Growth is longitudinal, not a per-block or ten-chapter tax.**

No new Agent, scorer, reviewer, Hard Gate or LLM call was added.
