# Reviser No-Op Upstream｜Held-out New Novel Protocol

> Status: hypothesis frozen before held-out novel generation.

## Question

Can a very small, zero-extra-call change to the existing rich free-text chapter chain make Terra Primary closer to a true Final Draft, so that the Luna-high Authority Reviser contributes materially less Story/Authority value?

This experiment does **not** test an Atomic skip gate yet. It first tests whether the Reviser can become closer to no-op.

## Derivation / Hold-out split

Derivation-only books:
- `real-exp-fast-world-20ch-20260828-v1` / 九垂原 related fresh pairs.
- `real-exp-current-pipeline-authority-reviser-0010-20260828-v1` / 分影 related fresh pairs.

These pairs may be used only to identify recurring Reviser contribution families. After this file is frozen, no Treatment wording may be changed from held-out results.

Held-out evaluation:
- Generate one entirely new novel after Treatment freeze.
- It must not reuse 九垂原 / 分影 / 商队契约 / 粮道水源 / 回潮楔 / 分身 as premise machinery.
- Evaluate four consecutive chapters from that one novel; do not cherry-pick chapters.

## Frozen hypothesis

Across the derivation pairs, useful Reviser changes repeatedly fall into five narrow families:

1. **Authority-literal cleanup**: remove invented price/number/past quote/injury/state; keep exact approved object/state wording consistent.
2. **Boundary closure once**: ownership/resource/power/cooldown/unknown boundary that matters to the current result should be made visible once, but not expanded beyond Authority.
3. **Reader-value concreteness**: an already scheduled Reader Release or named opportunity should be stated once in concrete reader-facing value, not diluted into an abstract “opportunity/entry”.
4. **Result Stop**: after action/result/reaction has already proved the point, do not add interpretation paragraphs that restate “what this means”, moralize the choice, or prove the same competence again.
5. **Specific private motive**: when Curated Context explicitly activates money, winning, possession, attraction, pride, jealousy or a named relationship motive, let that concrete motive appear once instead of replacing it with neutral analysis.

## Treatment｜Frozen Primary Final-Draft Readiness Watch

Append the following short block at the **end of the existing Primary prompt**. It adds no new facts and creates no new output section:

```
## FINAL-DRAFT READINESS WATCH｜只在写完正文前内部检查一次

不要重规划剧情，也不要输出审计。只用本 Prompt 已经给你的 Authority / Mission / Curated Context，对最终正文做一次很窄的提交前检查：

1. **精确事实不自己补全**：金额、价格、旧对白、伤势、身份、持有人、能力边界与历史状态，输入没明确就不补；输入已经给了具体对象/状态时，全章用同一个具体对象/状态，不把“资格/份额/承诺”升级成“已到账/已拥有”。
2. **关键边界只落一次**：若本章结果真实依赖一个已明确的持有/付款/力量/冷却/未知边界，在发生点让读者看懂一次即可；不要漏，也不要后面再解释一遍。
3. **已排程价值说具体一次**：Curated Context / Reader Release 已明确某个具名入口、契约、奖励、地点或身份为什么值，就用现成事实让读者知道一次；不要压成“一个机会 / 更大的入口”，也不要新增待遇。
4. **结果成立就停**：动作、对白、物体变化和人物反应已经把意义写出来后，删掉随后同义的作者解释、人物总结、能力复盘或“不是A也不是B”的裁断；让后果进入下一动作。
5. **私人动机别净化**：Curated Context 已明确钱、胜负、占有、虚荣、审美/身体吸引、嫉妒、报复或某个具体人的牵引，而且现场自然触发时，让它通过一次想法/对白/注意力/选择露出来；不要改写成中性职责或正确分析。

除此之外按原 Primary 合同正常写，不为了通过这五项而新增说明段。
```

## A/B

For each held-out chapter, freeze the same:
- Director response;
- Curator response;
- Primary prompt before the appended block;
- all Authority / Canon / Plan inputs;
- Terra high model and effort.

Run in parallel:
- Control Primary = current prompt.
- Treatment Primary = current prompt + frozen Readiness Watch.

Then send each Primary through the **same current Luna-high Authority Reviser** to measure residual Reviser work.

## Evidence

Per chapter:
- Primary wall;
- Reviser wall;
- paragraph/block delta Primary→Reviser;
- character count delta;
- anonymous Primary Control vs Treatment Story Blind;
- anonymous Primary Control vs Treatment Authority Blind;
- within each arm, Primary vs its own Reviser Story/Authority no-op audit;
- final Control-Reviser vs Treatment-Reviser Story/Authority blind;
- independent repeat on the same four frozen chapter inputs.

## Success condition

Do not productionize from one held-out novel. This experiment is a directional pass only if:
- Treatment Primary does not lose Story vs Control Primary;
- Treatment Primary improves or ties Authority;
- Reviser Story/Authority advantage over Treatment Primary shrinks materially versus Control;
- residual Reviser edit volume shrinks without merely shortening prose;
- final Treatment-Reviser does not regress;
- Primary wall does not materially increase.

Even a pass only justifies another held-out novel. It does not yet justify skipping Reviser.
