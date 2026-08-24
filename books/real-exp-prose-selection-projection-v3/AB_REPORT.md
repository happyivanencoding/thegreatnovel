# Selection Prose DNA v2 → Scene Projection A/B

Date: 2026-08-24

## Question

验证新的正文链是否比“完整 Prose Control → Writer”更有效：

`Selection Prose DNA v2 / BOOK Prose Profile / Chapter Mission / Canon / current Scene → Curator → NONE 或 2–4句 Scene Prose Projection → Terra Primary`

本实验不测试 AI detector，也不测试后置 Humanizer。唯一目标是判断局部选择压力是否能改善同一事件合同下的正文实现。

## Isolation

四组都复用已经存在的完整冻结章节输入，不重跑 Director / Outline。每对 OFF / ON 使用同一个 GPT-5.6 Terra high Primary Writer；机械 hash 验证除 `Scene Prose Projection` 外基线完全一致。

- OFF：`Scene Prose Projection = NONE`
- ON：使用一次 GPT-5.6 Luna high Curator 编译出的 2–4 句局部 Projection
- Judge：一次 GPT-5.6 Luna high 联合 blind judge；X/Y 随机打乱，judge 不知道实验条件

来源作品 Prose DNA、Control 名称和完整 GBrain 卡都不直接进入 Primary。

## Samples

| Scene | Frozen sample | GBrain control candidate |
|---|---|---|
| Entry / survival opening | clean E2E Ch1 | NONE（高精度 fallback 不强行补卡） |
| Complex Action / pursuit | clean E2E Ch6 | `spatially-traceable-causality-v1` |
| Discovery / Reveal | xianxia-blind Ch2 | `evidence-first-limited-reveal-v1` |
| Emotion / Relationship | opening-reader-first Ch2 | NONE（Curator 只靠 BOOK / Scene /人物状态编译） |

这也验证了一个重要架构点：**Scene Projection 不要求先有 GBrain control；control 是可选研究知识，不是生成 Projection 的前置条件。**

## Blind Result

| Scene | OFF | ON | Δ ON |
|---|---:|---:|---:|
| Entry | 7.8 | 6.9 | -0.9 |
| Complex Action | 6.9 | 7.8 | +0.9 |
| Discovery / Reveal | 8.2 | 8.7 | +0.5 |
| Emotion / Relationship | 7.7 | 8.4 | +0.7 |
| **Mean** | **7.65** | **7.95** | **+0.30** |

ON **3胜1负**，平均分从 **7.65 → 7.95（+0.30）**。

## What Changed

### Complex Action — ON +0.9

ON 更完整地落实“故意现身 → 诱入错误支路 → 重新判断承重点 → 逆潮路返回”的战术链，并把知识边界限制在陆砚当前真正看见/确认的东西。OFF 更容易为追逐补踏风钉、固定白痕、灯线分队等未冻结设施或程序，使动作开始像路线设计。

结论：`spatially-traceable-causality` 的正确使用对象仍是**读者可能丢失位置与因果的复杂 Action**，不是所有战斗。

### Discovery / Reveal — ON +0.5

ON 将抽象异常压回灰粉、滴水、轻敲、指定受压位置和复现结果；“受力记忆”只作为暂用判断，不自动补全来源、机制或能力结论。OFF 也忠实，但更容易扩展压钳、记录、冷却等步骤，出现轻微方法执行感。

结论：Knowledge / Causal DNA 在 Reveal 场景有明显增量价值，重点是**证据 → 当前足够判断 → 下一选择**，不是人为制造神秘。

### Emotion / Relationship — ON +0.7

这组没有 GBrain prose-control 候选，Curator 仍能根据 BOOK / Canon / Scene 编译有效 Projection。ON 更准确地把关系变化放在拒绝、站位、试探、见证权和一次性交换上，并保持“明天能用一次，不等于永久学会”的边界。OFF 更容易自行补人物过去动机或过去经历。

结论：Projection Compiler 的价值不等于“Control Translator”。**Reaction / Knowledge / Attention 可以直接从本书当前状态产生局部选择压力。**

### Entry — ON -0.9

这是必须保留的反证。OFF 已经自然形成“白汗承重 → 矿鸣 → 旧道错位 → 逆流落脚 → 水槽 → 路印 → 求救”的清楚事件链。ON 再加 Projection 后，局部承重点和一步一步移动被写得更模板化；两版也都有少量未冻结事实扩写。

结论：即使 Projection 本身合理，**当 Chapter Mission / Canon 已经把即时目标、关键位置、主要因果和结果停点写得很清楚时，额外 Projection 仍可能降低 prose。** 这不是继续优化 Entry Control 的理由，而是让 Curator 更愿意输出 `NONE` 的理由。

## Deterministic Metrics

| Scene | OFF chars | ON chars | OFF abstract markers | ON abstract markers |
|---|---:|---:|---:|---:|
| Entry | 2486 | 2234 | 1 | 1 |
| Action | 4694 | 3613 | 1 | 2 |
| Reveal | 3692 | 2591 | 0 | 2 |
| Emotion | 3014 | 3364 | 1 | 0 |

这些指标只做诊断，不决定胜负。尤其 Reveal ON 虽然 abstract marker 0→2，盲评仍更高，说明“抽象词出现次数”不能替代语义判断；真正的问题是**结果已经成立后是否重复解释**。

## Product Decision

**PROMOTE PROJECTION COMPILER / KEEP PROJECTION OPTIONAL.**

冻结下面的产品行为：

1. Curator 拥有 `Scene Prose Projection` 编译能力，但输出允许 `NONE`。
2. `NONE` 是正常结果，并优先于弱 Projection。
3. Scene Family 有匹配 Control **不是**使用理由；只有当前正文实现存在真实局部读法缺口才投影。
4. Projection 最多 2–4 句，只使用当前人物、物件、位置、关系、知识边界和结果停点；不回显六维 DNA，不输出 Control 名称。
5. GBrain Prose Controls 继续 OPTIONAL；无高置信候选时不补位。
6. Primary 不直接读取 source Prose DNA，也不读取 legacy 完整 `Relevant Prose Controls`。
7. Payoff 不再拥有独立常规 Control；结果已成立但现场仍读不出变化时，只补一个必要后果，已经清楚就停止。
8. 不新增 Humanizer Agent、AI detector gate 或自动 rewrite。

## Interpretation

Selection Prose DNA v2 的有效增量不是“提供更多写作规则”，而是帮助 Curator回答：**这一场究竟缺哪一种读法？**

当前最合理的正文链因此冻结为：

`BOOK Prose Profile + Canon / POV + current Scene + optional Selection DNA / Prose Control evidence → Curator → NONE or 2–4 sentence local projection → Terra Primary`

成功标准不是每章都生成 Projection，而是模型在需要时获得局部选择压力，在已经足够清楚时不干预。
