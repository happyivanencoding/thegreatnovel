# RESULTS｜Reader-facing Ontology / Power Concreteness

## Verdict

**PASS（针对本轮目标）**。

本轮真正修掉的是同一个上游回归的三条入口：World 先造术语依赖链、Novelty Spark 把直接能力诱导成“理解/分析后才能发动”、Story Program 后续新 Asymmetry 没有继承 Power Seed 的白话边界。最终没有新增 Reviewer / Scorer / Hard Gate，只修改实际生成这些事实的 Prompt / Spark。

## 1. Baseline 失败确实可达

原实验 `WORLD_VISION.md` 直接出现：

> 真质 → 刻纹 → 纹阶 → 引纹 / 定纹 / 展纹 / 镇纹 / 改质 → 质片 / 母碑 / 剥纹 / 错质身

这些词局部都能解释，但读者必须先学词之间的关系，才能知道人物到底能做什么。

同一旧 Power Prompt 的 fresh rerun 也复现了更直接的能力回归：

> “真正弄懂眼前障碍的结构与性质”才能穿过去；掌握轴继续要求“还原障碍层次、连接、真质流向和刻纹变化”。

所以问题不是 Writer 措辞，也不是单次偶然：最早坍缩点真实存在于 World / Power 上游分布。

## 2. 第一版 Treatment：PARTIAL，不提前算成功

只加入“创新不在词汇表 / 先白话后命名”后，World 的三个 Luna 样本中：

- `WORLD_TREATMENT_1`：先解释物质特性怎样进入身体/兵器，再用“物性/刻层”等短名，明显改善；
- `WORLD_TREATMENT_2`：焚骨砂入骨、储热/放热，效果直接，明显改善；
- `WORLD_TREATMENT_3`：又把“天地记住走过的路 → 路痕 → 折路”抬成力量本体。

因此第一版只能判 **PARTIAL**：术语依赖下降，但“抽象关系本身充当力量 ontology”的旁路仍在。

Power 第一版同样只算 PARTIAL：Spark 从“理解障碍”改成“亲手触碰障碍”后，开局已经变成“摸墙就穿”；但 `POWER_TREATMENT_R2` 的异常掌握轴仍出现“判断材料连续性和可穿路线”，说明直接能力可以在成长阶段重新分析化。

## 3. 最终根修

### World

加入统一 Reader-facing 边界：

> 创新落在事实、力量因果与玩法，不落在词汇表。基础力量先用普通话说明来源、直接作用、成长与失败；新词只给已经理解且会反复出现的对象/层级贴短标签。默认直接型男频力量先给身体、攻击、防御、移动、穿越、元素、兵器、异兽等可感知作用；除非作者明确选择认知/概念系幻想，不把路径、定义、权限等抽象关系本身当作创新证明。

“全新世界”因此不再等于“必须回避境界、功法、兵器、异兽等熟悉词”。

### Power Seed / Novelty Spark

- 删除实际会诱发分析化的 Spark：`只能穿过自己能理解的障碍` → `只能穿过自己正在亲手触碰的障碍`；
- 同类 `学习/复制` 的“真正理解”条件改成可观察的“亲手成功复现”；
- 直接型能力的 mastery 不得重新变成结构分析、材料诊断、路线计算或逐步验证；
- Legendary Power State / Future Legend Image 不得绕过 Permanent Boundary。

### Story Program 后续 Asymmetry

新获得仍由真实故事产生，但先写：

> 以前做不到什么 → 现在具体多能做什么

之后才决定是否需要世界内短名；短名只压缩已经理解的能力。

## 4. 第二版 World 复验：3/3 PASS

同 Author Direction、同已保存 World GBrain、Luna high：

- `WORLD_TREATMENT_V2_R1`：天上曜砂 → 炼入骨肉 → 储存/释放热力；主尺 `火序`。先懂“热力强化身体/兵器”，再记名字。
- `WORLD_TREATMENT_V2_R2`：东西真正折断/毁坏会漏出白色力量 → 炼入骨血强化身体/兵器；主尺 `灯数`。机制新，但可观察。
- `WORLD_TREATMENT_V2_R3`：天上蜕片 → 炼入身体 → 长出可硬化/变形的壳；主尺直接就是 `壳层`。

三者都有原创设定，但没有再要求读者先学习术语链或抽象关系，且力量正常值、高价值物、世界奇观与长期尺仍保留。

## 5. Power 复验：从“分析墙”稳定变成“摸墙就穿”

旧 Prompt fresh baseline：

> 弄懂障碍结构与性质 → 还原层次/连接/流向 → 才能穿。

最终 Prompt：

> “别人必须破门、凿墙、挖地才能过去；他只要亲手碰到障碍，就能带着自己的身体和随身之物直接穿到障碍另一侧。”

`POWER_TREATMENT_V2_R1 / R2` 的掌握轴都保持在穿更厚实体、携带装备、战斗中控制出入口和攻防复合，没有重新依赖结构分析。

其中 `POWER_TREATMENT_V2_R2` 的非 Canon Future Legend 曾错误写“带同伴”，与 Permanent Boundary 冲突；因此又补了极小的边界一致性规则。最终 `POWER_FINAL_R1` 重新生成后，Legendary / Future Legend 均保持“只能自己 + 随身物、不能带未接触他人”的边界。

强度没有被削弱：最终版本仍然是低阶直接绕过墙、牢门、山体与城防实体封锁，并能长期复合进战斗。

## 6. Story Program 后续能力

这里的结论要克制：旧 baseline 已经经常会在 `剥纹术 / 返纹尺` 后补一句具体效果，所以本轮没有证据证明 Story Program 是最近问题的主要根因。

Treatment 证明新增边界能正常工作且不伤长期结构。例如 `STORY_H4_TREATMENT` 先写：

> 触摸非活物接触面后，一息内不再传递推力、拉力或摩擦；门闩还在却暂时锁不住门，刀刃相碰却无法借碰撞传力。

随后才给短名 **“断接”**。这正是目标顺序：**先懂效果，再记名字。**

两名冻结 Human 的 Story Program 都仍保留新的 Asymmetry、正常成长和新旧复合，没有因为语言变直白而削弱 Advantage Stack。

## 7. 第二题材泛化

为了避免只对原作者方向过拟合，又用一份不含“少术语 / 白话能力”提示的普通男频作者方向做 final generalization：

- `CROSS_WORLD_R1`：地潮压力 → 身体储存潮力 → 强化、冲击、护罩、移动；境界再命名。
- `CROSS_WORLD_R2`：地火 → 体内炉火 → 炉料让身体/兵器获得硬化、速度、冲击、兽性或火焰效果；境界再命名。
- `CROSS_POWER_R1`：在新的地潮世界里再次抽中问题型“穿障”幻想，仍稳定得到“亲手碰实体 → 直接穿过”；异常掌握明确写出“核心不是把障碍分析得更清楚”。Permanent Boundary 与 Future Legend 一致。

因此最终修法不是对 `真质 / 刻纹` 这一本书的定向屏蔽，而是改变了生成分布。

## What This Did Not Solve

本实验只证明 **reader-facing ontology / power concreteness** 的根修。`CROSS_WORLD_R1` 仍能出现 `定潮院 / 百桩试 / 修桩` 等较程序化的世界事件；这属于另一个已经存在的 **Supporting Logic / narrative-weight** 问题，不应伪装成本实验也一并解决。它没有重新把核心力量写抽象，但后续若要继续处理，应单独冻结 World 输入做 narrative-weight A/B，而不是把更多 negative rule 塞进本轮修法。

## Runtime / Cost Record

所有真实生成使用 ACP + ChatGPT 登录；World / Power 为 GPT-5.6 Luna high，Story Program 为 GPT-5.6 Sol high。`USAGE.json` 保存每次调用的 tokens 与 wall-clock。当前 ACP payload 不返回 credits 或实际账单成本，因此该字段明确记为 N/A，而不是伪造估算值。

## Final Conclusion

本轮 target 可冻结为 current production 原则：

> **Reader-facing novelty = 熟悉语言 + 新作用。**
>
> 新词可以有，但只能给读者已经看懂的东西贴标签；不能靠词与词互相解释制造原创。直接型能力从开局到长期掌握都保持直接作用，不能在成长阶段偷偷变回分析/诊断/路线/验证能力。

修复层位于 World / Power / Story Program 的真实 authority producer；Writer 无需新增补丁，系统也没有新增 Agent、Reviewer、Scorer 或 Hard Gate。
