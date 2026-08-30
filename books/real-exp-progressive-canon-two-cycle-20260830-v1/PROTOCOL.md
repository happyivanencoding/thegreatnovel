# Two-Cycle Progressive Canonization E2E

状态：EXPERIMENTAL / NOT PRODUCTION

## Hypothesis

同一个长期 Mystery 可以经历：

`AUTHOR OPEN → DEFER → 正常故事 → DECISION NEEDED → 局部 Hidden Fixed Point → reader-facing Reveal → Canon → 更深 AUTHOR OPEN → 第二次局部定真 → 第二次 Reveal → 更深问题继续开放`

而不需要开书时知道终极答案。

## New holdout

全新 Mystery：听雨城“回影井”会吐出与现存物件完全同源、却经历不同的第二份实物。第一章只建立可观察异常；作者没有预设来源答案。

## Pre-registration

- Decision 0：DEFER。
- Cycle 1：Chapter 1 后应 DECISION NEEDED；Reframe 固定选 R2；Compiler 非 PASS 则停止；首次 Reveal 固定在 Chapter 3。
- Cycle 2：Chapter 3 后应 DECISION NEEDED；Reframe 固定选 R3；Compiler 非 PASS 则停止；第二次 Reveal 固定在 Chapter 4。
- Chapter 4 后重新打开更深问题；当前下一路线不依赖终极解释，最终 Decision 应 DEFER。
- 不因输出质量换 R1/R2/R3。

## Runtime secrecy contract

- Reveal 前 Director / Curator / Primary / Authority Reviser Prompt 不得收到 raw Hidden Fixed Point、State Residue 或 Reader Anchors。
- Story Refresh 是 planning-only，可见 Hidden Fixed Point；它必须把允许揭晓的一层编译成独立 `Mystery Reveal Contract`。
- Outline 只拿去掉 Reveal Contract 的 Story Program + 一个不含答案的 scheduling marker；不拿 raw Hidden Truth。
- 只有 Reveal 章由代码把 Event Atom / State Residue / Still Open 注入当前章计划。
- Reveal 后 State Extraction 从正式正文产生普通 Canon；旧 Hidden payload 不再进入 runtime。

## Character Authority Invariance

Cycle 1 同一 Fixed Point 额外跑一个冻结 Human B：
- Human A：好胜、贪钱、收藏欲强，优先把异常转成可占有的路线/货物。
- Human B：对妹妹安全高度偏心，宁可错失高价值先手也不让未知风险靠近家人。

Treatment 必须保留两者不同选择，不得把两人都推成“最优解调查员”。

## Full chapter chain

Main Human A 的 Chapters 1—4 使用当前 production prompt source：

`Luna Director → Luna Curator → Terra Primary → Luna Authority Reviser → Luna-low State`

Chapter 2 是 Cycle-1 pre-reveal chapter；Chapter 3 是 Reveal-1；Chapter 4 是 Reveal-2。

## Failure semantics

- Decision Surface 不符预注册：FAIL。
- Compiler 非 PASS：停止该 cycle。
- Reveal 前语义泄漏 Hidden Truth：FAIL。
- Reveal 章越过 Still Open：FAIL。
- State 未保存已揭 State Residue，或把更深未知补成 Canon：FAIL。
- 第二轮定真推翻第一轮已揭事实：FAIL。
- Human A/B 被推成同一种主要选择：降级或 FAIL。
