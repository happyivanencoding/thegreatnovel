# Three Random Books — Seed → World Vision → Story Program

## Experiment integrity

- Baseline: `21ba884`, branch `principal_dev_new_sys`.
- One GPT-5.6 Luna high Fantasy Seed call produced four candidates; candidates 1 / 2 / 3 were frozen as the three books before downstream generation.
- World Vision: GPT-5.6 Luna high, each with fixed 1 Coordinate Reference + 3 creative GBrain inspirations.
- Story Program: GPT-5.6 Sol high, each with 3 GBrain inspirations: `plot-engine-variation-v3`, `thread-collision-v3`, `earned-high-value-acquisition-v3`.
- No Outline or chapter generation.

## Book 1 — 《拆禁成刃》

Core fantasy: the protagonist can see a real, currently enforced “cannot” boundary and peel one restriction away after personally entering its effect. The power restores or creates action possibility; it does not automatically win the fight.

World: 九垣界. Cultivation progresses broadly through 引炁 → 成印 → 立界 → 天关. Stable techniques can become 法印; when anchored to flags, bloodlines, terrain, contracts or formations they become observable prohibitions: who may enter, whose power can operate, which weapon can hurt whom, which identity can access a road or inheritance. Valuable things include 灵髓, 界材, 行印/域籍 and 原印/禁令来源.

Long story stages:
1. 从跪城到裂域 — regain bodily freedom, enter a bloodline-locked ruin, expose a regional original seal.
2. 裂口不属于旧主人 — contest whether opened opportunities simply become a new hunting ground for old owners.
3. 名字成为猎场 — fight identity-based collective pursuit rather than another stronger gate.
4. 世上本无此路 — cross a region that rejects low-level life itself and face bait restrictions.
5. 普通铁刀入天关 — let low-level people/objects temporarily touch a tier that supposedly excludes them absolutely.
6. 两界之间，谁定义不可能 — decide which world-boundary restrictions still deserve to exist when another sealed world is revealed.

## Book 2 — 《把必然改成选择》

Core fantasy: just before a result truly locks, the protagonist can split one inevitable result into two reality-supported outcomes and choose one. He cannot invent a perfect third answer or reverse completed history.

World: 九衡界. The core reader ruler is action space: how close a situation is to having every alternative closed. Cultivation broadly progresses through 炼息 → 成脉 → 立相 → 镇域. Results become “fixed” when action, counterplay, people’s choices and environmental/contractual conditions all close; a visible 定痕 appears. The protagonist sees two possible landing points only before closure.

Long story stages:
1. 从刑台死人到未定之人 — survive a public execution and turn a sealed family tragedy into an investigable fact.
2. 旧案必须有人开口 — preserve a witness’s second real option before identity/family/cultivation rights force one testimony.
3. 一座城不再只有一种归属 — reopen a border city’s choice between official protection and independent passage.
4. 必胜之战重新下注 — prevent a war machine from making all local victories merely serve one predetermined winner.
5. 十万人的第二种结局 — enter a city-scale final node where every route, surrender and self-destruction option has been precomputed.
6. 终门不再决定唯一时代 — contest whether one faction may turn its victory into the only valid future of the age.

## Book 3 — 《以舍弃换登临》

Core fantasy: the protagonist can voluntarily discard something he truly owns and compress its real importance to his life into one beyond-current-tier “登临” action. The discarded thing is genuinely lost; the lasting gain is a changed body, combat path, identity or world access, not a sacrifice counter.

World: cultivation uses 灵息, body, techniques, artifacts and identity/access. The early ruler is 凡身 → 成式 → 成势 → 立域. A one-tier gap can still be contested with conditions; two tiers strongly suppress action; three tiers make direct fighting essentially suicidal. The protagonist can break one key relationship once, not permanently possess the higher tier.

Long story stages:
1. 碎印出旧界 — abandon bloodline techniques, safety identity and finally the family seal; leave the old cultivation path entirely.
2. 万相之地 — enter a higher world that recognizes different life forms and fight for a body that is not another permanent ownership cage.
3. 被制造的拥有 — enemies stop attacking directly and instead give him genuinely valuable power/status so they can later force the “right” sacrifice.
4. 白色荒原 — discover a world made from traces of discarded identities, techniques and life forms; enemies can reconstruct old selves from those traces.
5. 诸界定相 — gain cross-world action without accepting that every anomaly must finally be named, classified and confined.
6. 永恒之前 — confront the offer of a genuinely powerful, free, near-eternal form whose price is becoming one permanently fixed self.

## Regression found during generation

Book 3 initially caused `extract_hard_constraints` to read “从此无法回到原本的修炼体系” as an author constraint meaning “无修炼体系”. Root cause: the generic negation regex treated the `无` in `无法` as a genre-ban prefix. The parser now accepts explicit `无修炼体系` (or real negative instructions such as `不要/不得/没有…修炼`) but does not infer a genre ban from story-internal `无法…修炼` wording. A regression test was added before World generation was rerun. Fix commit: `3175762`.
