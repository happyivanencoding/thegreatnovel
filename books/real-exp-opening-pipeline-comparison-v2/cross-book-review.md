# Cross-book Review

范围：v2 两本各 Chapter 1—3；上游 Fantasy Seed、World Vision、Story Program、Outline、Future 10 和 Chapter 1 后的连续 Canon 已冻结。Single Control 只读取 `real-exp-opening-three-chapter-hook-v1` 的已完成三章；Hybrid 只读取 v2 自己 lane 的连续产物。

## Blind Reader 结果

- 《炉藏万象》：盲位 option-a = Hybrid、option-b = Single；Reviewer 最终判断 `HYBRID_BETTER`。
- 《掌中天工》：盲位 option-a = Single、option-b = Hybrid；Reviewer 最终判断 `HYBRID_BETTER`。

两个书级最终偏好方向一致，但逐问题结果不是全面横扫：Hybrid 的即时翻页、动作/空间或对白、能力落地更常获优势；Single 的人物行为指纹、NPC 独立性、少解释、少工整和资产复利清晰度多次获优势。两份盲读报告都明确写出这种混合，而不是数字评分。

## 只在 Hybrid 改善

- 《炉藏万象》Hybrid 的第一章门槛动作和现场对白更强，开路结果后的翻页推动更直接。
- 《掌中天工》Hybrid 把护腕从第一次救急推进到修承重骨、接断轨和扩大出口，能力输入、限制和现实结果更清楚；Dialogue/Action 局部建议被 Integrator 有选择地处理。
- 两本都没有观察到 Integrator 把 result-stop 改成额外总结；新增内容主要是必要余波、敌方反应、伙伴关系或下一步入口。

## 只在 Single 改善

- 两本 Single 更常保留主角的行为指纹和 NPC 的独立判断，少出现“所有人都在替主角验证能力”的感觉。
- 两本 Single 都被盲读认为解释更少、判断不那么工整；Hybrid 的 Curator/Primary 上下文更丰富，但有时把机制、长期意义或下一步更快说清楚。
- 两本 Single 的能力边界/资产链条更容易一次性复述；Hybrid 的连续调用让核心能力更爽，但也提高了读者记忆负担。

## 两者共同失败或共同风险

- 两条 lane 都把同一核心机制跨三章递进调用，存在“连续三章都围绕同一能力”的重复风险；目前不是同一结果的机械复播。
- 匿名矿工、伤者或炉工在局部仍承担 payoff 证明和运输/受害群体功能，长期人物主体性不能由前三章确认。
- 两条 lane 都有局部“动作后很快给出意义”的倾向，只是 Single 更少、Hybrid 更明显；这不是本轮自动修复对象。
- 实际模型 token usage 没有返回；Single 旧实验也没有可核验 token/call manifest，不能给出伪精确成本倍数。

## 目前证据不足

- Chapter 4 以后 Hybrid 的人物关系、资产复利和能力升级是否继续保持优势：本轮严格停止在 Chapter 3。
- Single 的真实 model call count 与 token usage：旧 Pilot 没有对应真实 usage evidence，只能写 `UNKNOWN`。
- 模型隐藏推理、真实延迟、费用和长周期留存：本轮不推断。
- candidate-b 没有执行 Specialist/Integrator，因此不能用它回答“多节点修订是否会重复解释”；candidate-c 的三章后验没有发现该问题，但样本仍只有一本真实执行了该链路。

## 差异归因

- 不是 Creative upstream 差异：两本的上游幻想、故事方案、Outline/Future 10 和 Chapter 1 后连续状态均冻结。
- 主要差异来自 Writer realization：Single 是单 Writer 控制，Hybrid 是 Director/Prep/Curator/Primary 加实际选择的 Specialist/Integrator。
- 其次来自多 Agent revision：candidate-c 的局部 Patch 有时被采纳、有时被拒绝；candidate-b 没有 Specialist/Integrator，因而其 Hybrid 增益不能归因于多 Agent revision。
- State Delta 只更新各自 lane 的 Canon 状态，不参与正文质量比较。

## Architecture verdict

两个盲读的书级选择都偏向 Hybrid，但逐项质量收益与退化同时出现，且 Hybrid 的结构调用明显更复杂；现有证据不足以满足 `HYBRID_CLEAR_WIN` 的“两个都明显更好、重要维度稳定增益”定义。相反，质量总体接近/混合，而 Hybrid 的调用和上下文成本更高，因此本轮架构结论为：

`QUALITY_TIE_SINGLE_MORE_EFFICIENT`
