# RESULTS｜SUBJECTIVE_AUDIT_0001_0010 根修与受控 A/B

## 总结

针对 `real-exp-private-prototype-reader-facing-20260827-v1/SUBJECTIVE_AUDIT_0001_0010.md`，本轮没有按章节逐条打 Writer 补丁，而是把问题归并为四个最早生产层：

1. **Story Program**：核心幻想主要被写成战术用途，Fantasy Possession / Personal Myth 偏弱；
2. **Outline**：Ch2 / Ch6 / Ch10 的前景锚点容易被二次资格证明、找路和统一说明等 process carrier 占据，World Entry 只有危险、缺少欲望与尺度；
3. **Chapter Runtime / Curator**：Frozen Human Core 原本没有进入章节期，最近几章“负责、救人、克制”的行为会反向覆盖原始 competing motives；
4. **Primary**：Curator 已排程的 Reader Release 只是“允许解释”，实际可以被 Writer 丢掉；私人欲望即使存在，也容易被净化成职责协作。

最终 production 根修不新增 Agent / Reviewer / Hard Gate：

- `Story Program` 保留核心幻想最独有的**生活特权**、具体 Fantasy Possession、主角级 recontext；
- `Outline` 使用 **World Entry = Threat + Desire + Ruler** 与 **Stage Settlement = Consequence, not Process Carrier**；
- `CHARACTER.md → Frozen Human Core` 由 deterministic projector **只投影给 Curator**，不重复 Power Core，不替代 BOOK/State；
- Curator 增加 **Specific Relationship Trigger**；
- Primary 将已排程 Reader Release 视为必须兑现的 timing decision，并保留最短价值锚点；
- High-Value Acquisition 增加 **真实错失允许有空窗**，防止为了维持爽点立刻塞等价补偿。

## Deterministic Validation

最终全量：**297 passed**。

测试过程中有两次有价值的失败，没有通过放宽测试掩盖：

1. `CORE_FANTASY_INVARIANT` 真正接入当前 Story Program 后暴露旧 `Fantasy Seed` 概念；production 已无 Fantasy Seed，因此直接改成当前权威 `Character 中已批准的 Power Core`。
2. 第一版 Human projector 遇到真实 `CHARACTER.md` 的 Human Seed 内嵌 `##` 标题时提前停止，只投影了标题。真实 Ch9 A/B 因此判 **INVALID**；projector 后改为只在 `## Composition Boundary` 停止，并增加真实嵌套结构 API/runtime 回归测试。

## A/B 1｜Outline

**结论：PASS。**

冻结：原 Author Direction / World / Character / **原 Story Program** / 原 Outline GBrain；只更换 current production Outline prompt，Luna high。

### Baseline 问题

- Ch1 已完成分影公开高光后，Ch2 又搭一个“同时守两处 + 事故”场面，再证明一次它值得正式护卫资格；
- 折日峡 / 石城主要以路线与危险进入；传承虽然存在，但在放弃前没有充分成为 reader desire；
- Ch10 用统一说明、责任记录和资格发放承载阶段结算。

### Treatment 变化

- Ch2 直接从“能力已证明”进入结果：公开登记能力、谈清报酬与伤势责任，**正式护卫身份 + 第一笔独立收入到账**；不再安排第二次资格证明。
- World Entry 前移欲望与尺度。Treatment Ch7 明确：
  - 顾斜阳追逐的线索可能改变宗门继承资格；
  - 传承从传闻变成眼前高价值机会；
  - 救人和扬名无法同时无代价完成。
- 前10章不再用一个完整“统一说明章”结算；Ch10 停在两条人生真正合回一个人，程序性说明压到后续 consequence。
- 后续进入沉昼城时，核心欲望变成“**真正拥有一件古代影兵**”，而不是继续拿一张资格牌。

### What This Did Not Solve

- 本组冻结的是旧 Story Program，因此 Gu Xieyang 的 ruler 仍更多是身份/继承位置，不一定带明确 tier/战绩数字。最终 Story Program 已提供更清楚的“完整宗门训练 / 更高功法 / 正常同阶比较”上游尺度，但仍需在新书里观察泛化。

## A/B 2｜Chapter 6 Primary / Reader Release

**结论：PASS for Reader Release realization；World Appetite 仅 DIRECTIONAL。**

冻结：Chapter 5 后 BOOK、Ch5 正文、原 Ch6 Director、原 Ch6 Curator、原 Scene Skill；只更换 current Primary prompt，Terra high。

Baseline 中 Curator 已明确要求介绍观日宗与石城价值，但 Primary 丢掉。

Treatment 第一次出现观日宗时直接说明它正在折日峡寻找失落传承，弟子争的是更高功法与宗门位置；石城也明确有旧城遗物、珍稀药材和异兽巢穴。说明只有短段，随后立即回到当前冲突。

因此“**已排程 Reader Release 必须兑现**”有效。

但石城的具体吸引力仍偏泛——“遗物 / 药材 / 值钱东西”——这证明 Primary 不能替上游凭空发明更强欲望对象。整体 World Desire 仍应由 Story Program / Outline 先建立。

## A/B 3｜Frozen Human Core → Curator → Primary

### R1｜INVALID

第一版 deterministic projector 错把 Human Core 内部的 `## 持续牵引...` 当成下一大区块，真实 Ch9 prompt 只得到 `# HUMAN SEED｜...` 标题，没有动机正文。

因此该次 Curator 输出不用于评价模型。

### R2｜PARTIAL PASS

修正 projector 后，真实 Ch9 Curator prompt 已明确包含：

- 身体吸引；
- 对陆绾的气味、姿态、靠近感；
- 自由钱；
- 被真正有分量的人看见；
- 不把责任 / 安全永远排第一。

Curator 不再把顾临川总结成“负责型人格”，会保留传承、陆绾、被看见等 competing motives。

但即使本章天然存在“陆绾近身扶住、处理影伤”的关系现场，它仍没有选择身体/感官 attraction cue。剩余坍缩被定位到 **Curator relationship relevance**。

### R3｜PASS

加入 `Specific Relationship Trigger` 后，Curator 明确保留：

> 近身扶住、处理伤口时，保留顾临川对她的靠近、药粉气味和熟悉身体感的具体注意，但不必扩写成表白或稳定关系。

随后 Terra Primary 自然实现为一次很短的 POV 注意：

> 她离得很近，衣袖擦过他腰侧。药粉和草叶混在一起的气味钻进鼻子里，清苦，却让顾临川昏沉的脑子清醒了一点。

之后正文仍然回到影身回返、伤势、传承与责任，没有转成恋爱章，也没有强行解释“他爱她”。

因此可以判：

`Frozen Human Core → deterministic Human-only projection → Curator specific relationship cue → Primary bounded realization`

**PASS。**

这解决的是 authority/projection 丢失，不是给 Writer 手塞“写点情欲”。

## A/B 4｜Story Program

### R1｜DIRECTIONAL PASS / overcorrection

Sol high 第一轮已显著改善：

- 分影第一次被规划成生活特权：一具身体练功，另一具处理生活；
- 远期出现“同时在两座城市生活”的真实双人生幻想；
- 陆绾的身体吸引、气味、动作与不等人的生活方式进入长期关系因果；
- 出现具体古代兵器 / 奇物，而非一路资格牌；
- 旧铜扣第一次获得 protagonist-level recontext，而不是所有 mystery 都只落世界层。

但阶段2出现一个过纠正：放弃传承后很快又给古兵，容易形成“牺牲一个爽点 → 立即补一个等价爽点”。因此没有直接冻结 R1。

### Final｜PASS

加入 **真实错失允许有空窗** 后重新 Sol high。

最终 Story Program 的改善是实质性的：

1. **Dual-life life privilege**
   - 开局一具身体在客舍记账、接待住客，另一具在武馆练习；合并后得到两边完整的一日经历，也一起承担两边疲惫。
   - 读者满足直接写成“一人同时过两份日子的能力第一次变成可触摸的生活特权”。

2. **Human / private appetite**
   - 顾临川会因陆绾的身体、气味、利落动作与鲜活感改路；
   - 她会让他推迟离开、花掉原本留给自己的钱；
   - 没有把这种牵引解释成更优成长路线。

3. **Fantasy Possession**
   - 具体影兵短刀、贴影衣等对象有可观察效果与使用场面；
   - Access / Identity 仍存在，但不再是唯一奖励形态。

4. **真实错失 / 非即时补偿**
   - 最终阶段2把顾斜阳的宗门传承明确成他自己的继承目标，顾临川没有被设置成“先放弃自己最想要的传承再马上拿替代品”；
   - 更直接的空窗出现在盐港：顾临川把原本用于外城生活的自由钱投入病棚和证人安置，**短期内没有得到等价补偿**。

5. **Personal Myth / protagonist-level recontext**
   - 早年陌生护卫留下的普通铜扣在黑峡关重新出现；
   - 后来得知它只是旧建筑上的普通扣件，不是命定信物；
   - 在无光海，它成为让错位旧门暂时对齐的实际钥匙，随后彻底断裂。
   - 即：普通旧物被重新理解并改变当前行动，但没有把主角改写成命定继承人。

6. **Rival ruler**
   - 顾斜阳被明确为比顾临川更早接受完整宗门训练、拥有更成熟宗门路径的人；
   - 他不靠降智轻视主角，而是在看见分影后主动研究怎样让两具身体同时进入不利光线。
   - 这是明显提升，但仍主要是相对尺度，不保证每一本新书都会自动出现一条数值化 tier benchmark，因此只判 **DIRECTIONAL PASS** for Rival Ruler 泛化。

## 最终判定

- **Process / qualification / settlement bias：PASS**
- **World Entry 的 Desire + Ruler：PASS in Outline sample；跨书泛化待观察**
- **Scheduled Reader Release → Primary realization：PASS**
- **Frozen Human Authority 在章节期不再丢失：PASS**
- **私人 / 身体性 competing motive 不再自动净化：PASS on matched Ch9 scene**
- **Core Power 从战术工具扩展为独有生活幻想：PASS in Story Program**
- **Access-only reward → Fantasy Possession：PASS in Story Program / Outline**
- **真实错失不被即时等价补偿：PASS in final Story Program**
- **Protagonist-level recontext / Personal Myth：PASS in final Story Program**
- **Rival ruler：DIRECTIONAL PASS**

## What This Did Not Solve

1. 这是同一本书、同一匿名 Human 的冻结 A/B，不能单样本证明新书分布永久稳定；下一次全新书应重点观察 World Entry、Rival ruler 与 private desire 是否自然复现。
2. 本轮没有专门解决“正文通用手势库偏重复”（看了他一眼、沉默片刻等）的 Prose variety；它不是本次最早根因，不能顺手在 Writer 加禁词。
3. Ch6 证明 Primary 会兑现 Orientation，但价值锚点多强仍取决于上游批准事实；Primary 不应自行发明更昂贵的传承或宝物。
4. 100 / 200 / 300 章后的稳定性没有在本轮测试。

## Artifacts

- `STORY_BASELINE.md` / `STORY_DIRECTIONAL_R1.md` / `STORY_TREATMENT.md`
- `OUTLINE_BASELINE.md` / `OUTLINE_TREATMENT.md`
- `CH6_PRIMARY_BASELINE.md` / `CH6_PRIMARY_TREATMENT.md`
- `CH9_CURATOR_INVALID_R1.md` / `CH9_CURATOR_PARTIAL_R2.md` / `CH9_CURATOR_TREATMENT.md`
- `CH9_PRIMARY_BASELINE.md` / `CH9_PRIMARY_TREATMENT.md`
- `USAGE.json`

所有真实 LLM 调用均通过 ACP / ChatGPT 登录；运行时未返回 credits / token usage，因此 `USAGE.json` 将 credits 记录为 `N/A`，并保留 model / effort / wall-clock。
