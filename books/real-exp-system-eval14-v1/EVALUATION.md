# System Eval 14 — Fresh Book Regression

## Test goal

Run one completely fresh novel through the current `principal_dev_new_sys` runtime:

`Fantasy Seed → World Vision → Story Program → Outline → Director → Curator → Primary → State`

Only Chapters 1–5 are written. The test does not reuse any old book-specific setting or downstream patch.

Baseline: `b0ee3ef777a946f45a9e8eed17c7d6761528faa7` (`fix: move world readability upstream`).

## Frozen routing

- Fantasy Seed: GPT-5.6 Luna, high, GBrain OFF.
- World Vision: GPT-5.6 Luna, high, GBrain ON, max 3.
- Story Program: GPT-5.6 Sol, high, GBrain ON, max 3.
- Outline: GPT-5.6 Luna, high, GBrain ON, 4 accepted in this run.
- Director: GPT-5.6 Luna, high, GBrain OFF.
- Curator: GPT-5.6 Luna, high, raw GBrain OFF, Scene Skills ON.
- Primary: GPT-5.6 Terra, high, raw GBrain OFF, Scene Skills ON.
- State: GPT-5.6 Luna, low, GBrain OFF.

ACP ran read-only with ChatGPT authentication. A pure-text ACP wrapper was required for the final Outline run because the coding-agent host initially interpreted the Outline prompt as a request to edit `BOOK.md`; that failed run did not change the book and is recorded separately as a harness issue, not a TGN creative result.

## Frozen Seed selection

The Fantasy Seed generated four candidates. Selection was frozen before generation to **always take Candidate 1**, avoiding cherry-picking.

Selected concept: **借命成真**.

Core fantasy: 顾行舟能看见当前因果中真实存在的多种未定未来，并主动夺取其中一个结果，使它提前成为现实。它不是普通预知、时间回溯或万能复制。

## Upstream results

### World Vision — PASS

The new upstream readability responsibilities were actually produced rather than deferred downstream.

World coordinates were defined as four observable tiers:

- 养息
- 成术
- 立域
- 见界

The World Vision also separated normal organizational baseline conditions from scarce rewards, and explicitly defined the core-advantage compatibility boundary: 顾行舟不能从高层目标身上凭空复制修为、法则或生命层次；面对远高于自己的目标，只能夺取当前因果里真实存在的破绽、介入、逃生或其它可承接结果。如果所有可见未来都没有接触点，他必须先改变现实局面，让新的分支出现。

This is the intended system-level fix for the previous “reader does not know who is stronger / what advancement means / whether the cheat breaks high-level scaling” problem.

World GBrain accepted exactly 3 abstractions:

- `mechanisms/story-state-compounding-v3`
- `mechanisms/world-entry-v3`
- `mechanisms/world-desire-ladder-v3`

### Story Program — PASS

Sol produced six natural large stages:

1. 雨夜夺命，古城归来
2. 一城两史，谁算活着
3. 万宗下注，先手成局
4. 无未来之地
5. 天下只许一种结果
6. 诸界留真

The Plot Engine changes across stages instead of repeating the same operational loop. The core advantage evolves from夺取局部动作/物品结果，to主动制造分叉，to维持他人的选择，then to争夺城池、地域和世界未来的存在资格。

Program GBrain accepted 3 abstractions:

- `mechanisms/plot-engine-variation-v3`
- `mechanisms/thread-ecology-v3`
- `mechanisms/earned-high-value-acquisition-v3`

### Outline — MOSTLY PASS, one root failure

The successful Outline produced a natural planning window of Chapters 1–42, not a forced 100-chapter window. Future 10 is concrete and causally continuous.

The first five planned beats are clear and non-procedural:

1. 被押往悬崖灭口，顾行舟挑拨三名追杀者争功。
2. 第一次看见十七种未来。
3. 第一次真正夺取“断腕”结果。
4. 利用敌人的功劳与药瓶欲望主动制造分支。
5. 夺取续命药瓶、服药并恢复到能够奔跑。

No engineering / blue-collar workflow appears in this chain.

Outline GBrain accepted 4 abstractions:

- `mechanisms/thread-collision-v3`
- `mechanisms/sacrifice-convergence-v3`
- `mechanisms/hidden-identity-long-v3`
- `mechanisms/reward-recontextualization-v3`

#### Root failure: initial Canon time boundary collapsed

The Outline's final `# 当前状态、未兑现承诺与作者备注` was supposed to describe the state **before Chapter 1**, but it incorrectly inserted facts from future Chapters 3–8 as already happened, including:

- “已第一次夺取未来中的斩击和灵药结果”
- “韩烬断腕但未死”
- “拥有半份账册、送信人的暂时协作和烬河旧印线索”

This is the earliest semantic collapse in the run.

The consequences were observable immediately:

- Chapter 1 Director received both the Chapter 1 plan (“only挑拨/争功”) and Canon saying later payoffs had already happened.
- It therefore invented an early successful ability use in Chapter 1.
- Chapter 2 then followed the original Future 10 and treated the ability as newly understood, creating a “first use / first understanding” timeline tug-of-war.
- State correctly acted as a lightweight clerk and preserved old Canon rather than guessing that the upstream Canon was wrong. This is not a State bug.
- Curator correctly reported the contradictions instead of silently reconciling them. This is evidence that Curator's boundary is healthy.

## Cheap root-cause A/B

A single Director-only A/B was run with everything frozen except the Outline initial State.

B changed only the initial State into a Chapter-1-start **T0 snapshot**: no断腕、no药瓶到账、no账册、no送信人、no烬河旧印；it explicitly stated that Chapters 2/3/5 contain those future payoffs.

Result: Chapter 1 Director immediately returned to the intended event budget. It explicitly wrote:

> 顾行舟……把处决变成近距离混战。他仍未确认或使用“借命成真”。

It ended with 韩烬把顾行舟逼到悬崖边 and did not consume Chapter 2 or Chapter 3.

**Conclusion: fixing the Outline initial State is sufficient for this observed failure. Do not add another Director hard gate, reviewer, or State correction layer.**

The minimal upstream repair should be semantic, inside Outline responsibility:

> The final initial State is a T0 snapshot immediately before Chapter 1. Only facts already true before the first scene may enter Current State / Canon. Anything introduced by Future 10 or later story anchors is future Plan or Open Promise, never Current State, even if the Outline discussed it earlier in the same response.

## Chapter results

### Chapter 1 — PARTIAL FAIL due upstream Canon pollution

The prose itself is readable and concrete, but the Director prematurely lets 顾行舟 successfully alter a sword result. This steals part of Chapters 2–3's intended discovery curve.

### Chapter 2 — PARTIAL FAIL due inherited timeline conflict

Terra writes the “十七种未来” scene clearly. Curator explicitly refuses the polluted Canon claim that 韩烬 is already断腕 and protects the current plan. However, the chapter now says 顾行舟 sees but does not yet know how to make a future real, while Chapter 1 already showed a successful result alteration.

### Chapter 3 — PASS

The first major payoff lands cleanly: 顾行舟真正夺取断腕结果，韩烬断腕，两名追杀者第一次不敢靠近。Curator marks prior explanation as already established; Terra does not turn the scene into another rules lecture.

### Chapter 4 — PASS

Gameplay changes from direct result theft to social/combat decision pressure. 顾行舟 uses the enemies' greed for功劳与药瓶 to break their coordination. The chapter is about people wanting things and acting against each other, not procedure.

### Chapter 5 — PASS

The first concrete resource payoff lands: black-jade medicine bottle enters 顾行舟's hand, he drinks it, and the gain visibly changes what he can do—he can finally run and escape along the cliff. This is a direct improvement over the previous pattern where advancement/qualification produced no usable reward.

## Prose/runtime assessment

### No return to engineering / procedural cultivation

Across the five saved chapters, no正文 hits were found for planning/procedural leakage terms such as:

- 行动空间
- 结果落定
- 兑现
- 状态变化
- 叙事功能
- 闭环
- 验证
- 流程
- 承重点 / 受力
- 项目 / 治理

The prose remains focused on people, killing pressure, greed, injuries, weapons, medicine, choices and visible consequences.

### Core Gameplay Variation is working

The sequence is not five repetitions of the same cheat use:

- Ch1: human manipulation under execution pressure
- Ch2: perception / discovery
- Ch3: direct combat result theft
- Ch4: manufacture a branch by exploiting enemy desire
- Ch5: resource acquisition and escape

### Curator / Primary division is healthy

Curator repeatedly detects Canon/Plan conflicts, keeps unknown facts unknown, selects scene skills, and warns against repeated explanation. It does not rewrite the story.

Terra Primary is concise and reader-facing. Chapters 3–5 especially show that once the event contract and Canon are coherent, it can stop explaining the mechanism and let physical result / human reaction carry the scene.

### World Model Release is not yet fully validated by Chapters 1–5

World Vision successfully defined `养息 / 成术 / 立域 / 见界`, but the first five prose chapters do not yet expose those tier names. The current cliff sequence remains understandable because the relative danger is concrete (three pursuers, severe injuries, weapons, position, medicine), so this is not yet a reader-confusion failure.

Therefore this run proves **upstream world coordinates exist**, but it does not yet prove that Outline's `World Model Release` reliably releases them at the right reader-facing moment. That should be observed when the story first needs readers to compare broader power/status levels; no new gate is justified from these five chapters alone.

## Resource record

ACP-reported successful-turn totals for this run (Codex host/system context included, so these are useful for experiment comparison, not pure application prompt cost):

- Input tokens: 870,032
- Cached input tokens: 317,696
- Output tokens: 71,983
- Reasoning output tokens: 22,312

Successful model-turn wall-clock recorded from available timestamps is about 26 minutes when the Seed/World transcript durations are included. The failed first Outline ACP attempt is excluded from creative-result timing.

AgentDock/Codex on the current Prolite route did not return a usable per-turn credits charge, so actual credits are recorded as unavailable rather than estimated.

## Final verdict

This fresh-book regression is **materially better than the previous sample** on the exact system-level concerns from Eval 14:

- World Vision now owns readable power/value/compatibility facts: PASS.
- Story Program maintains long-form Plot Engine variation: PASS.
- Outline gives concrete, non-engineering early story anchors and real early rewards: PASS.
- Curator and Terra Primary avoid procedural prose and keep scenes reader-facing: PASS.
- Initial Canon time boundary in Outline: FAIL and is the earliest/root failure.

Recommended next repair is only the Outline T0-state semantic boundary. Do not patch Director, Curator, Primary or State for this observed failure.
