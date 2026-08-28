# Experiment Protocol

TGN 的实验不是为了“证明我们喜欢的方案正确”，而是为了把系统问题从文学直觉变成可归因证据。

## 1. 先写 Hypothesis

实验前用一句话写清：

> 如果只改变 X，那么 Y 应该怎样变化；如果 Y 不变，说明 X 不是主要原因。

避免一轮同时改变 World、Prompt、GBrain、模型、Schema 和 Selector。

## 2. Freeze Baseline

保存：

- baseline artifact；
- prompt；
- model / reasoning；
- GBrain snapshot（Pages / Chunks / Embedded）；
- retrieval bundle；
- 关键输入 hash（必要时）；
- 当前 git commit。

如果 baseline 本身已经不可复现，先承认实验只能做 directional evidence。

## 3. One Main Variable

优先单变量：

- same World, different Human GBrain；
- same Character, different Story Program field schema；
- same Scene, Prose Control OFF vs ON；
- same Prompt, different model；
- same source evidence, different retrieval allocator。

如果必须有两个变量，说明为何不可分，并把结论限定为组合效果。

## 4. Fresh Context for Causal Isolation

测试 authority independence / rationalization 时：

- 新 session；
- 不带上游隐藏信息；
- 不允许模型通过 prompt history 猜另一个 seed；
- deterministic projection 优先；
- 不让后续 Composer 回头重新合理化。

## 5. Cheapest Adequate Model

模型不是越强越好。

- 用 Luna 做大量上游候选与 A/B；
- Terra 用于正文、fidelity 或高精度 bounded extraction；
- Sol 只用于真正需要长期多线程结构整合的高杠杆节点；
- Judge 不是默认必需。

如果实验问题只靠 deterministic code 能回答，不调用 LLM。

## 6. Direct Reading Before Metrics

先读具体输出，问：

- 到底哪里变了？
- 变好来自哪一句/哪一结构？
- 有没有新的副作用？
- 是否只是更长、更会解释？

自动指标只辅助验证，例如：

- leakage hit；
- abstract-term density；
- tool/professional vocabulary；
- repetition；
- schema completion；
- token/cost。

指标不能替代文学判断。

## 7. Judge Only When Needed

以下情况可用 blind judge：

- 两版都成立，细微 prose quality 难人工稳定判断；
- 多场景比较需要汇总；
- 需要隔离作者知道 treatment 的偏见。

以下情况不需要 Judge：

- 明显 named hook leakage；
- Schema 越权；
- Power 与 Biography 逐项押韵；
- 一版直接缺关键剧情；
- 两边输入完全相同。

## 8. No Cherry-Pick

如果一批生成4个 candidate：

- 不因为最好的一张很好就宣布 generator PASS；
- 也不因为一张普通就宣布架构 FAIL。

分别判断：

- architecture 是否允许健康分布；
- distribution 是否坍缩；
- candidate 本身是否商业上值得选。

“架构 PASS，候选4较弱”是健康结论。

## 9. Character Authority Invariance

当 Treatment 可能改变主角取舍、路线优先级或长期效用函数时，不只测一个人物。

默认冻结至少 2—3 个动机排序明显不同的 Human，例如力量第一、具体关系可改路、认可/新鲜感混合型，并对每个 Human 做同一 A/B。

分别验收两件事：

1. Treatment 是否真的产生目标结构增益；
2. 关键选择是否仍随 Human 改变。

如果不同 Human 被 Treatment 推成同一种“成长最优”“关系最优”“道德最优”路线，即使结构更整齐，也应 FAIL 或降级。反过来，保留人物差异本身也不能证明机制有效；结构增益与 Character Authority Invariance 必须分开判断。

## 10. Matched Decision Point

要验证 `Personality → Choice → Route`，先让不同冻结 Human 面对**同一个具体诱惑 / 冲突 / 机会**，只比较选择是否随 Human 分叉；再放开 Story Program，观察不同选择是否长期长成不同路线。

对每个被测 Human，决策点都应至少包含两个具有真实私人价值、且不能同时完整取得的方向；价值来源与强弱可以不同。选择之后，未选路线的主要机会成本必须真实保留；不能马上用隐藏奖励、事后证明“其实这条路更赚”或等价补偿把代价抹掉。否则测试到的只是伪选择，不足以证明 Character Authority。

如果人物、触发事件和机会池同时变化，只能证明“生成结果不同”，不能把差异纯归因于人格。Matched Decision Point 只用于因果识别，不要求 production 把所有人物放进同一剧情。


## 11. Information Release / Realization Causal Trace

当实验目标是“世界信息进入正文”或“压缩实施细节”，不要直接做一轮大而混的全文 rewrite。优先逐层冻结：

1. 同 World / Story / Canon，先比较 release scheduling 是否正确；
2. 冻结 Outline / chapter result，检查 runtime 是否真的传入当章 safe world fact；
3. 冻结 Director，比较 Curator 是否保留 public fact、是否把已成立 Supporting Skill 降到结果级；
4. 最后才在同 Curator 输入下比较 Primary realization。

某一层失败就保留该产物为 evidence，不继续让下游“救”。如果 Writer 仍扩写，再把残余明确归因到 realization，而不是回头重写 World。

对 reveal 单独做泄漏检查：**World 已知但 Future Plan 仍安排后续发现的答案，在揭晓前不得因为 Reader Orientation 被提前投放。**

## 12. Verdict Vocabulary

### PASS
主要假设被真实输出支持，副作用可接受，可冻结/上线。

### DIRECTIONAL PASS
方向正确，但证据量、live treatment 或覆盖不足；可以保留机制，不应宣称问题完全解决。

### PARTIAL PASS
解决一个子问题，同时暴露独立残余问题。不要把残余重新归咎于已通过架构。

### FAIL
核心 treatment 没产生预期变化，或副作用抵消收益。

### INVALID / CONFOUNDED
实验变量不干净、输入不同、selector 偷选、GBrain 中途变化、baseline 不一致。不得用来冻结系统结论。

## 13. Always Record What It Did Not Solve

每个通过实验都写：

> What This Did Not Solve

例如：

- Split Seed 解决 Power↔Biography 合理化，不自动解决 Human appetite distribution；
- Private Appetite Continuity 减少职业化，不自动产生好胜/虚荣/战斗欲；
- lane cap 解决检索配额，不凭空创造 Behavior/Relationship ACTIVE craft；
- prose texture 改善场景质感，不修 Story Program 的剧情同质化。

这样下一轮不会回头破坏已经验证的层。

## 14. Code Experiment Safety

修改 production code 前：

- `git status`；
- 记录 protected uncommitted files；
- 不覆盖其他 agent 工作；
- 新实验优先放独立目录；
- 实现后 focused tests；
- full suite；
- `git diff --check`；
- stage 白名单或自己的 hunks；
- 再 commit/push。

不要因为旧测试失败就恢复已经明确废弃的架构。先判断测试是否属于 legacy expectation。

## 15. GBrain Experiment Safety

涉及 GBrain 时记录：

- before / after Pages；
- Chunks；
- Embedded；
- `Embedded == Chunks`；
- accepted / rejected cards；
- active vs reference-only；
- retrieval regression；
- unrelated negative queries。

如果蒸馏仍在跑，不把 staging / materialized 文件当 live GBrain treatment。

## 16. Stop Conditions

以下情况应停止继续加实验变量：

- treatment 没有改变实际输入；
- 已经找到清晰 root cause；
- 下一步只是重复验证同一结论；
- 剩余问题已经属于另一个层；
- 用户目标已达到。

不要为了“实验完整”继续烧 quota。
## Creative Intensity Decision

当多个 treatment 都满足 hard authority / causality，仅在爽感强度、奖励丰富度或主角局部优势上存在 trade-off 时，不由 Steward/Judge 自动向保守版收敛。保留代表性真实输出，并把 AGGRESSIVE / MODERATE / CONSERVATIVE 的关键差异交给作者选择；当前 TGN 默认审美先验偏 AGGRESSIVE。只有事实矛盾、authority 越界、或即时近似补偿抹平真实牺牲可以直接淘汰。
