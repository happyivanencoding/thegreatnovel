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

## 9. Verdict Vocabulary

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

## 10. Always Record What It Did Not Solve

每个通过实验都写：

> What This Did Not Solve

例如：

- Split Seed 解决 Power↔Biography 合理化，不自动解决 Human appetite distribution；
- Private Appetite Continuity 减少职业化，不自动产生好胜/虚荣/战斗欲；
- lane cap 解决检索配额，不凭空创造 Behavior/Relationship ACTIVE craft；
- prose texture 改善场景质感，不修 Story Program 的剧情同质化。

这样下一轮不会回头破坏已经验证的层。

## 11. Code Experiment Safety

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

## 12. GBrain Experiment Safety

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

## 13. Stop Conditions

以下情况应停止继续加实验变量：

- treatment 没有改变实际输入；
- 已经找到清晰 root cause；
- 下一步只是重复验证同一结论；
- 剩余问题已经属于另一个层；
- 用户目标已达到。

不要为了“实验完整”继续烧 quota。
