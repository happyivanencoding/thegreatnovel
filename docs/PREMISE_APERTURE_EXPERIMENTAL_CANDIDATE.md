# Premise Aperture｜大胆设定前置搜索候选

状态：`EXPERIMENTAL / AUTHOR-GATED / NOT PRODUCTION DEFAULT`

日期：2026-08-29

证据目录：`books/real-exp-premise-aperture-20260829-v1/`

## 1. 根因

当前 `protagonist-blind World → Split Power / Human → Character → Story Program` 成功阻止了旧 Fantasy Seed 把世界、能力和人物统一成一篇意义论文，但也留下了一个更早的搜索缺口：

> 在任何 Authority 冻结前，没有一个非 Canon 空间先提出“这本书最值得押注的完整高风险前提”。

于是每个 lane 都会分别给出合理、完整、长期可运行的答案，却很容易在完整货架承诺形成前就收敛：标准人形主角、职业性能力、可解释世界、观察／分析／维护／探路／登记等旧动词。

四本扫榜素材的共同优势不是百科更复杂，而是很早把以下内容绑成一个主押注：

- 一句话就能复述的异常前提；
- 第一章不可替代的具体场面；
- 主角会反复执行的新身体／战斗／移动／占有／生存动词；
- 立刻发生的不公平兑现；
- 群体、对手、弹幕、生态或社会对主角行为的第二层反应；
- 熟悉商业类型之上的一处大偏离，而非所有部分都同时陌生。

因此问题不主要在 Writer、GBrain 或术语库，也不是简单要求 World / Power “再创新一点”。缺的是 **premise-level search operator**。

## 2. 当前候选架构

```text
作者方向
  → Single-Agent Premise Forge
       一次生成 S1 / S2 / S3 三张完整非 Canon 候选
  → Independent Premise Authority Compiler
       只审可满足性；不评分、不排名、不改稿、不选择
  → 作者选择 / 要求修复 / 放弃
  → lane-specific frozen contract
       World：World-only + protagonist-blind public interface
       Power：literal Ontology + Initial Scale Position
              + trigger / target coverage / action / carrier / root boundary
       Human：literal Ontology + exact T0 Origin + Initial Scale Position
       Story：Authorities 批准后第一次读取完整 Promise
  → 现有 Split Authority 链
  → Outline / chapter 只读 approved Authorities，不再读 raw Premise Card
```

Premise Aperture 不是第四 Authority：

- 候选未被作者选择前，不产生 Canon；
- Compiler 不能自动挑“最安全”或“最高分”的一张；
- 作者选择后，事实仍分别由现有 World / Power / Human / Story Authority 实现和批准；
- 无法同时实现时必须显式返回 `PREMISE-AUTHORITY CONFLICT`，不能静默削弱、增强或换义；
- 只在开书阶段低频运行，不进入章节 Runtime。

## 3. Forge 输出合同

每张候选必须有一个主押注，并明确输出：

- 一句话货架简介；
- World-only Direction；
- protagonist-blind World Interface；
- literal Protagonist Ontology；
- exact T0 Origin；
- Initial Scale Position：主角在 World 已定义每条适用主／副尺上的精确位置；
- Power trigger、目标类别、可执行动作、载体与永久边界；
- Story Interface / Opening Promise；
- 第一章标志性画面；
- Changed Verbs；
- 第一次不公平兑现；
- 20 章玩法扩张与 100 章 runway；
- `Authority-Compilation Trace`。

Trace 是 Forge 的自检，不是合法性证明。它必须具体写“动作／结果 → 来源字段 → trigger → 目标／载体 → 为什么合法”，但独立 Compiler 仍需重新检查。

## 4. Independent Premise Authority Compiler

Compiler 只回答“这张大胆卡能否被现有 Authority 精确实现”。它不能：

- 评分、排名或替作者选 S1 / S2 / S3；
- 把激进、怪异、主角占便宜大本身判成风险；
- 自动把冲突候选修成保守版本；
- 成为章节期 Reviewer / Gate。

它必须检查：

1. 第一章每个超常动作是否由明文字段推出；
2. trigger 在动作发生前是否已满足；
3. 目标、门、出口、身体、空间、见证者与载体是否真实存在并完成规则要求；
4. Interface 是否只观看、记录、传播或改变社会后果，而未偷偷复制／放大 Power；
5. T0 精确位置是否被 protagonist-blind World 的公共尺度容纳；
6. 第一次兑现、20 章终局与百章图景是否只复合已定义规则，而未假设共同载体、无限复制、凭空出口、未定义等级跃迁或新能力。

Compiler 的价值不是让设定更谨慎，而是让大胆前提在进入昂贵 downstream 前先暴露假的因果桥梁。

## 5. 上游受控实验

三种冻结作者方向：普通玄幻、20 章快速多世界、副本流。主实验统一使用 Luna high；baseline 使用既有 production artifact，不重抽。有效评审为 3 case × 3 独立 casewise blind review。

| Source Pool | 跨 Case 平均总分 |
|---|---:|
| Single-Agent 完整 Premise Forge（S1–S3） | **85.1** |
| Current production baseline（B0） | **75.8** |
| 四 fresh-context 轴完整碰撞（C1–C3） | **71.7** |

预注册同位比较：

| Case | S2 − C2 |
|---|---:|
| 普通玄幻 | +17.3 |
| 快节奏多世界 | +16.3 |
| 副本流 | +15.3 |
| 合并 | **+16.3** |

关键判断：

> fresh-context isolation 是 authority leakage control，不是 creative composition optimizer。

四个独立 Agent 各自产出大胆组件，常常制造四个互相竞争的主承诺；一个 Agent 一次形成完整 premise，反而更容易保住单一货架吸引力、清楚第一章与长期玩法。

真实 Changed Verbs 包括：

- 被杀后夺取致死结果；
- 把死亡变成移动与换身；
- 主角本身是一句活命令；
- 主角是一间会吞进真实建筑与人的活房子；
- 主角从被命名者身边的镜面伸手出来；
- 把建筑、巨兽或房间并入自己的身体。

它们不是标准人形修士把分析、维护或路线优化做得更专业。

## 6. Downstream 证据与失败链

### 6.1 Direction-only compiler：FAIL

同一预注册 S2 在真实 `World → Power / Human → Story → Outline` 中发生三项静默改写：

- Human 把“公开处刑后从死者喉中诞生”搬到旧训练场破旗，并补出出生前履历；
- Power 把“门／兵器／野兽／人”四类目标缩窄成只作用于活人；
- 稳定公开重映被降成阶段末一次演出。

结论：**lane-safe 不等于 premise-safe。** 柔性 Direction 不可冻结。

### 6.2 Lane-specific frozen contract：边界 PASS，旧候选整合 FAIL

对同一 S2 使用硬约束后，World、Human、Power 均精确保留原字段；Story 没有继续圆，而是返回 `PREMISE-AUTHORITY CONFLICT`：

- 开篇效果早于 Power trigger；
- 全城开门依赖未批准的复制／共同载体；
- T0 声位 0 不在 World 的 1—100 公共尺中；
- 终局假设未定义的全城共同载体与语义扩张。

这证明 frozen contract 与 fail-loud 有效，但不证明原候选可上线。

### 6.3 Forge 自带 Trace：不足

加入 `Authority-Compilation Trace` 后，候选仍大胆，但 Forge 会相信自己的假桥梁。独立审计发现：

- 开篇多走了一步动作；
- 远期从能力组合直接跳到最高等级；
- 未定义的共同载体或出口被当作已经存在；
- “完整过门”只是文字声明，实际动作并未发生。

因此 Trace 应保留，但不能替代独立 Compiler。

### 6.4 V4 独立 Compiler 实例

三张候选仍保持强货架电压：

| 候选 | Compiler 结论 | 核心结果 |
|---|---|---|
| S1《死式》 | CONDITIONAL PASS | 开篇合法；18—20 章到命火尺 9 与关闭死潮缺少成长映射 |
| S2《一城吞门》 | FAIL | 棚屋未真实完整过门；后墙门凭空出现；见证人数与 9 阶跃迁未闭合 |
| S3《镜外有人》 | CONDITIONAL PASS | 开篇一次出镜只允许一次动作，却连续夺钥匙、割门绳；其余尺位与九锚点 runway 基本闭合 |

预注册 S2 在进入 World 前停止，避免花费完整 downstream 调用去重新发现已知冲突。Compiler 没有把它判差是因为它太怪，而是因为它违反了自己写下的门槛规则。

### 6.5 Selected Premise Repair V5：FAIL

对预注册 S2 允许一次 Luna-high 定点修复，代码锁死标题、`一句话货架简介`、非人 Ontology、Changed Verbs 与三条不可磨平项。修复确实补上了完整过门、同一真实门、五名见证者和逐级壳层结构，但它漏掉了整个 `主角反复会做的新动作` 受保护字段，并把窄修复扩写成大范围重构。

确定性 validator 在独立 Compiler 复检前停止；没有把旧字段事后复制回来，也没有进入 downstream。结论：自动修复循环当前仍不可靠，只能 `RESEARCH_ONLY`。Compiler 失败时，正式路径应把精确冲突交给作者，而不是静默自动改稿。

## 7. 当前冻结建议

在作者明确批准前，production default 不变。

| 编号 | 候选 | 当前建议 |
|---|---|---|
| F1 | `Premise search before Authority freeze` 原则 | **建议冻结** |
| F2 | Single-Agent 一次生成 S1 / S2 / S3 完整候选 | **建议冻结为可选开书阶段** |
| F3 | Independent Premise Authority Compiler，作者选择前只审可满足性 | **建议冻结为开书期窄检查** |
| F4 | 作者选择；不自动 selector | **建议冻结** |
| F5 | lane-specific frozen contract + fail-loud + raw card 不下传章节 | **建议冻结** |
| F6 | 具体 Prompt 字数、字段措辞与模型配置 | **暂不冻结；继续跨题材校准** |
| F7 | Selected Premise 自动定点修复 | **已测试 FAIL；RESEARCH_ONLY** |
| F8 | 四轴完整正交碰撞 | **拒绝冻结** |
| F9 | Two-Bet Voltage Budget | **research-only** |
| F10 | 模型／Judge 自动选择最保守或最高分候选 | **拒绝冻结** |
| F11 | 恢复旧统一 Fantasy Seed | **拒绝冻结** |

建议冻结的是架构边界，不是立刻把它接成所有新书的不可跳过 production 默认。最稳妥的上线方式是：先作为可选开书入口，对至少两个额外题材完成“Compiler PASS → 真实 downstream PASS”后，再决定是否默认启用。

## 8. 未解决问题

- 尚未证明哪一档 S 候选适合所有题材；
- 尚未完成两个额外题材的 Compiler PASS → 全链 PASS；
- Compiler 失败后的默认边界应是把精确冲突交给作者；自动定点修复已在一次预注册测试中漏掉受保护字段，后续只能 research-only 复验；
- 尚未证明同一 Changed Verb 到百章后不会变成一招放大；玩法换挡仍属于 Story Program / Outline；
- 没有改变正文 prose、章节 Runtime 或生成速度；
- 独立 Compiler 增加一次开书期调用，但能提前阻止无效 downstream；其净成本需在后续 PASS 样本中记录。

## 9. 实现状态

已实现但未接 production default：

- `src/story_mvp/premise_aperture.py`
  - Single-Agent Forge；
  - Initial Scale Position；
  - `Authority-Compilation Trace`；
  - Independent Premise Compiler prompt builder；
  - Selected Premise repair prompt + protected-core validator（research-only，真实测试 FAIL）；
  - single-card preamble normalization + fail-closed parser；
  - lane-specific frozen projection；
  - explicit conflict detection；
  - 四轴与 Two-Bet research paths。
- `tests/test_premise_aperture.py`
  - non-Canon contract；
  - exact S1 / S2 / S3 compiler input；
  - parser fail-closed；
  - lane isolation；
  - frozen field projection；
  - conflict detector；
  - compiler 不评分／不选择／不自动修复。

Production default remains unchanged pending author decision.
