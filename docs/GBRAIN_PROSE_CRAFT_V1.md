# GBrain Prose Craft v1 与 TGN 正文表达层

## 目标

Prose Craft v1 解决的是：**故事已经知道写什么以后，怎样把同一个正确事件写得清楚、顺畅、有身体、有关系反应、有力量感，同时减少 AI 常见的抽象解释、均匀句式和无效环境纹理。**

它只控制 HOW TO SAY，不重规划 WHAT HAPPENS。

权威顺序不变：

- BOOK Prose Profile 决定当前书长期表达方向；
- Chapter Mission / Canon 决定本章必须发生的事实；
- Prose Controls 只是 OPTIONAL INSPIRATION；
- 来源小说 Prose DNA 是 evidence layer，不直接发送给 Primary Writer。

## 为什么不是“作者风格模仿”

v1 不保存“冷峻、宏大、细腻、华丽”作为主要生产知识，也不要求模仿任何作者。

蒸馏下沉到可观察的微观层：

- Diction / lexical selection：具体名词、动作动词、抽象认知词、修饰词和语体边界；
- Sentence realization：长句、短句、并列、省略分别在什么叙事功能下出现；
- Paragraph rhythm：自然段什么时候承载连续动作，什么时候因为真实状态变化而断开；
- Detail selection：Story-bearing / Embodied / Atmospheric 三类细节怎样取舍；
- Physicality：方向、距离、接触对象和结果怎样让动作落地；
- Dialogue / voice：回答、回避、反问、称呼、动作插入如何改变关系状态；
- Micro reaction：身体、视线、站位、手中动作等怎样承担人物反应；
- Exposition timing：说明什么时候进入、说到什么程度、怎样立即反哺行动；
- Omission / restraint：哪些意义可以不解释，仍让读者从行动与后果读懂；
- Payoff / aftermath：重大结果怎样由现场、关系或下一步行动确认。

不使用固定句长、固定段落、词频配额、禁词表或 hard gate。

## Scene Families

研究和检索使用 8 个宽 Scene Family，不继续拆成大量 Specialist：

1. `ORDINARY`
2. `ENTRY_EXPLORATION`
3. `DIALOGUE_NEGOTIATION`
4. `DISCOVERY_REVEAL`
5. `EXPOSITION_RULE`
6. `ACTION_COMBAT`
7. `PAYOFF_POWER_PROOF`
8. `EMOTION_RELATIONSHIP`

可附 OPENING / AFTERMATH / ENDING、压力等级、人数和 POWER / RELATIONSHIP / MYSTERY / WORLD_WONDER / STATUS / SURVIVAL / COMEDY 等软标签。这些只帮助检索，不是场景分类门禁。

## 第一批 SOURCE-FIRST 样本

| 书 | source_book_id | Prose 专项 |
|---|---|---|
| 《遮天》 | `rcv0-31-xuanhuan-zhetian` | 奇观、尺度、探索、战斗空间 |
| 《仙逆》 | `rcv0-32-xianxia-xianni` | 情绪、执念、普通生活、兑现余波 |
| 《斗破苍穹》 | `rcv0-34-xuanhuan-doupo-cangqiong` | 商业可读性、战斗、公开证明与反应 |
| 《大圣传》 | `rcv0-38-xianxia-dashengzhuan` | 主角气、身体感、日常生命力、力量兑现 |
| 《幽冥仙途》 | `rcv0-39-xianxia-youming-xiantu` | 信息差、危险关系、多方压力、微反应 |
| 《死人经》 | `rcv0-40-wuxia-sirenjing` | 高压对白、潜台词、联盟/背叛、多方博弈 |

最终采样 **85 个 bounded scene windows**：遮天14、仙逆15，其余四本各14。全部 locator 使用 canonical `source_book_id / source_id / distill_id / segment_id / line_start / line_end`，验收为 **85 refs / 0 error**。

## Prose DNA：证据层

六张正式 Prose DNA 已写入 `reference-corpus/prose-dna/`。它们保留单书的 Scene Window 与微观 prose 观察，并全部设置：

`active_inspiration: false`

理由：Primary Writer 不应该随机混入《死人经》的谈判声线、《遮天》的奇观尺度和《大圣传》的身体豪气。source-specific Prose DNA 用于证据、审计和跨书 synthesis，不直接承担生产路由。

## Production Prose Controls

跨书 Luna synthesis → Luna integrator → Terra final fidelity audit 后，最终保留 **7 张 active prose-controls**：

### 1. action-anchored-grounding-v1

适用：`ENTRY_EXPLORATION`、陌生地点和即时空间危险。

先让人物正在做的动作与眼前目标成立，再选一个会改变路线、距离、选择或安全判断的局部异常。进入场景不是环境导览。

### 2. dialogue-state-pressure-v1

适用：高压 `DIALOGUE_NEGOTIATION`。

对白压力来自可见状态变化：资格、关系距离、主动权、证据、承诺或是否继续合作。关键回答、回避、反问、称呼变化或动作只有在真正改变这些状态时才值得前景化；多人场景不要求所有人轮流发言。

### 3. embodied-reaction-private-scale-v1

适用：`EMOTION_RELATIONSHIP`、重大结果后的私人反应。

先让结果明确，再选一两个与人物真实习惯、身体和私人生活相关的细节，使反应与原状态产生差异，并连接新的选择或关系动作。不使用统一“手一顿、眸光一凝”模板。

### 4. evidence-first-limited-reveal-v1

适用：`DISCOVERY_REVEAL / EXPOSITION_RULE`。

先给可观察证据，再给当前人物足够使用的局部判断，只解释到当前选择需要的程度，并保留仍有价值的未知。

### 5. payoff-consequence-conversion-v1

适用：Chapter Mission / Canon 本身包含真实 payoff、胜利、获得或身份变化。

先用可见结果完成 payoff，再根据场景选择最有价值的一种后果：外界重新定价，或私人 aftermath；不要求两者同时出现，也不征收固定“代价”。

### 6. scale-anchored-wonder-v1

适用：真实的尺度跃迁、巨大奇观或世界边界首次显形。

用少数可比较的具体空间锚点建立尺度；尺度必须影响人物的空间判断、行动路线或风险认识，建立后及时回到局部身体/行动 POV。

### 7. spatially-traceable-causality-v1

适用：复杂 `ACTION_COMBAT`、追逐、多人混战。

只追踪决定胜负的关键变化：位置/方向 → 接触 → 结果。空间清楚优先于动作步骤完整，不把战斗写成逐招流水账。

原第8候选 `state-change-cadence-v1` 被 Terra audit MERGE，不作为独立检索卡。它只保留为共享提示：**句段压缩可以跟随真实状态变化，但不是固定句式规则。**

## Detail Priority

v1 的共享默认优先级：

1. **Story-bearing detail**：改变力量、关系、身份、风险、地位或下一步行动的理解；
2. **Embodied detail**：让人物与情绪获得身体/私人生活现实；
3. **Atmospheric detail**：在需要时支持空间、压力和奇观。

这是优先级，不是配额。一个场景不需要三种细节全部出现。

## Runtime Soft Routing

默认原则：Curator 只选择 **1 张明确相关的 Prose Control**；第二张很少出现，且必须解决不同的 prose problem。

| Scene Family | Primary | Optional second |
|---|---|---|
| ORDINARY | embodied-reaction-private-scale | 新地点/状态时可 action-anchored-grounding |
| ENTRY_EXPLORATION | action-anchored-grounding | 真正尺度奇观时 scale-anchored-wonder |
| DIALOGUE_NEGOTIATION | dialogue-state-pressure | 关系兑现时 embodied-reaction-private-scale |
| DISCOVERY_REVEAL | evidence-first-limited-reveal | 通过移动发现时 action-anchored-grounding |
| EXPOSITION_RULE | evidence-first-limited-reveal | 规则由即时行动学到时 action-anchored-grounding |
| ACTION_COMBAT | spatially-traceable-causality | 默认无第二张 |
| PAYOFF_POWER_PROOF | payoff-consequence-conversion | payoff 本身是复杂动作高潮时 spatial control |
| EMOTION_RELATIONSHIP | embodied-reaction-private-scale | 仍有谈判压力时 dialogue-state-pressure |

当前这是 **Pilot routing recommendation**，尚未硬接入每章自动链。下一步先做便宜 A/B，再决定是否冻结为默认 Curator 行为。

## Model Routing

- **Terra high**：SOURCE-FIRST bounded scene evidence、Source Fidelity；重点是原文实际上怎样用词、断句、断段、选细节。
- **Luna high**：单书 Prose DNA、跨书 Scene synthesis、最终 controls integrator；重点是为什么这些微观写法让阅读更自然有力。
- **Sol**：本轮不使用。它的长篇结构优势继续留给 Story Program。

## Final Audit

Production controls：

- 7 active cards
- 33 representative canonical evidence refs
- 0 evidence error
- 0 source-author / source-book surface leakage in TGN abstract output
- 0 fixed sentence length / fixed paragraph / banned-word / imitation hard-gate risk

六张 source Prose DNA：85 scene refs / 0 error。

## GBrain / Embedding

Prose Craft 前：

- 3734 pages
- 15686 chunks
- 15686 embedded

Prose Craft 后：

- **3747 pages**
- **15705 chunks**
- **15705 embedded**

完成标准为 `Embedded == Chunks`，已达成。

Windows / Git Bash 必须使用真实 executable：`~/.bun/bin/gbrain.exe`。`~/bin/gbrain` 是 WSL wrapper，不作为 Git Bash 的 GBrain executable。

推荐收尾流程：

`import --no-embed → source ~/.bashrc → ~/.bun/bin/gbrain.exe embed --stale → stats → retrieval regression`

## Retrieval

TGN `primary_writer` 手工查询已验证七种 prose problem 都单一精准命中对应 control，并且 `extract_abstract_content()` 不返回来源书名或硬门禁语言。

原 Story Craft 规划检索回归仍完全保持：World 3 / Story Program 3 / Outline 4。

### 当前 GBrain scoped semantic 限制

GBrain 当前存在一个已观测的搜索行为：纯中文 query 在全库 hybrid search 可以返回相关结果，但 `query --scope prose-controls` 对中文 semantic 分支返回空；同 scope 下英文 alias/keyword 查询正常精准命中。doctor 同时确认 embedding coverage 为 100%，因此这不是缺 embedding。

当前生产路径应使用 Scene Family → approved English alias 的确定性 fallback 检索 Prose Controls，不依赖纯中文 scoped semantic search。

## 下一步：Prose Control A/B

在自动接入前，做同 Chapter Mission / Canon / BOOK Prose Profile / Terra Primary Writer 的便宜 A/B：

- OFF：当前正文链；
- ON：Curator 按 Scene 选择 1 张 control，极少第二张。

重点比较：

- 一遍读懂程度；
- 句段是否更有功能变化；
- Story-bearing / Embodied detail 是否增加；
- “环境很细但人物没生命”的问题是否下降；
- 人物微反应和关系变化是否更自然；
- 战斗空间是否更清楚；
- payoff 后是否更有现实余波；
- AI 式抽象总结、同义解释和 procedural expansion 是否下降；
- 是否产生来源作者风格泄漏。

只有跨不同 Scene Family 的 A/B 稳定胜出，才把 soft routing 冻结成默认生产行为。
