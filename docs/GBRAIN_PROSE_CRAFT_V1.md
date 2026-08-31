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

六张 v1 Prose DNA 与六张 **Selection Prose DNA v2** 均已写入 `reference-corpus/prose-dna/`。v2 不重新取证，而是完整继承 85 个 canonical scene refs，把微观观察重组为“作者在什么条件下选择什么进入文本”的 evidence layer。它们全部设置：

`active_inspiration: false`

理由：Primary Writer 不应该随机混入《死人经》的谈判声线、《遮天》的奇观尺度和《大圣传》的身体豪气。source-specific Prose DNA 用于证据、审计和跨书 synthesis，不直接承担生产路由。

## Production Prose Controls

跨书 Luna synthesis → Luna integrator → Terra final fidelity audit 后，当前保留 **6 张 active prose-controls + 1 张 merged/reference-only payoff card**。完整研究卡只为 Curator 提供可选知识，不直接进入 Primary：

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

### 5. payoff-consequence-conversion-v1 — MERGED / REFERENCE_ONLY

不再作为独立常规 production projection。它留下的有效原则已并入共享 result-stop：**结果已经发生但现场仍读不出局面变化时，只选择一个会改变行为、关系或行动空间的必要后果；已经清楚就停止。**

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

2026-08-31 Batch Production 冻结后，**BOOK Prose Profile 仍是默认正文表达权威，但 Scene Projection Compiler 不再处于默认 Batch critical path**。默认 Batch 由 Full Deterministic Authority Packet 直接把 BOOK §§7–10 Prose Profile 交给 Terra；Curator / Scene Projection Compiler 暂时只服务单章 fallback / 专项修订：

`默认 Batch：BOOK Prose Profile + Full Deterministic Authority Packet → Terra Batch Primary`

`单章 fallback：BOOK Prose Profile + Chapter Mission / Canon / 当前人物状态 + current Scene + optional Prose Control evidence → Curator → NONE 或 2—4 句 Scene Prose Projection → Terra Primary`

没有经过独立 Batch-compatible A/B 前，不为了“功能齐全”把 Curator 或 Scene Router重新塞回默认 Batch。

关键边界：

- `NONE` 是正常结果，并优先于弱 Projection；
- Scene Family 有匹配 Control **不是**使用理由；当前 Mission / Canon 已让即时目标、关键位置、主要因果和结果停点自然可读时，应允许 `NONE`；
- Projection 只写本场具体注意点、知识边界、承重细节、节奏转折与停止点，不回显 DNA / Control 名称；
- Primary 确定性剥离 legacy `Relevant Prose Controls`，source Prose DNA 和完整研究卡不直接进入 Writer；
- no-key retrieval fallback 采用高精度、低召回、否定感知的 scene-signal scoring：宁可无候选，也不因零散“站位 / 试探 / 公开”等词误路由；
- Payoff 不再独立路由 Control；共享 result-stop 足够。

当前高置信候选主要为：

| 真实 prose problem | 可选 Control evidence |
|---|---|
| 复杂追逐 / 多人 / 移动地形导致方位与因果易丢失 | `spatially-traceable-causality-v1` |
| 发现 / 规则复验需要保持证据与知识边界 | `evidence-first-limited-reveal-v1` |
| 陌生入口确实缺少即时动作与空间承重 | `action-anchored-grounding-v1` |
| 私人关系变化缺少可读反应 | `embodied-reaction-private-scale-v1` |
| 高压多人谈判且基础对白无法自然读出筹码变化 | `dialogue-state-pressure-v1` |
| 真实尺度跃迁 / 世界边界第一次显形 | `scale-anchored-wonder-v1` |
| payoff 本身 | **NONE；使用共享 result-stop** |

## Model Routing

- **Terra high**：SOURCE-FIRST bounded scene evidence、Source Fidelity；重点是原文实际上怎样用词、断句、断段、选细节。
- **Luna high**：单书 Prose DNA、跨书 Scene synthesis、最终 controls integrator；重点是为什么这些微观写法让阅读更自然有力。
- **Sol**：本轮不使用。它的长篇结构优势继续留给 Story Program。

## Final Audit

Production controls：

- 6 active cards + 1 merged/reference-only payoff card
- 33 representative canonical evidence refs
- 0 evidence error
- 0 source-author / source-book surface leakage in TGN abstract output
- 0 fixed sentence length / fixed paragraph / banned-word / imitation hard-gate risk

六张 source Prose DNA：85 scene refs / 0 error。

TGN runtime validation：当前完整测试基线 **229 tests passed**；no-key Curator fallback 已升级为高精度可空路由，并通过复杂 Action / Reveal / Emotion NONE / Payoff NONE 等回归。

## GBrain / Embedding

Prose Craft 前：

- 3734 pages
- 15686 chunks
- 15686 embedded

Selection DNA v2 / Projection Compiler 本轮完成后：

- **3753 pages**
- **15717 chunks**
- **15717 embedded**

完成标准为 `Embedded == Chunks`，已达成。从本轮起，所有 GBrain 增量统一按 `Distill → Formalize → Import → Embed → Embedded == Chunks → Retrieval Regression → Done` 收尾；没有补完 embedding 不算任务完成。

Windows / Git Bash 必须使用真实 executable：`~/.bun/bin/gbrain.exe`。`~/bin/gbrain` 是 WSL wrapper，不作为 Git Bash 的 GBrain executable。

推荐收尾流程：

`import --no-embed → source ~/.bashrc → ~/.bun/bin/gbrain.exe embed --stale → stats → retrieval regression`

## Retrieval

TGN `context_curator` 的 no-key fallback 不再按 8 个 Scene Family 机械映射一张卡，而采用**高精度、低召回**策略：

- 只分析当前章事实任务，不让 BOOK 长期规划、Growth 术语或叙事功能备注主导 scene routing；
- 对关键词做基本否定感知，`没有追逐 / 并非围堵` 不计为正 signal；
- 复杂 Action 需要追逐、搜捕、围堵、支路/入口持续变化等强空间锚点，单独出现“站位”不会触发；
- Reveal 需要复验、线索、异常、未知边界等集中证据；
- 模糊或混合 Scene 默认返回 `NONE`；
- 手工 query override 仍最高优先；planning 的 World 3 / Story Program 3 / Outline 4 路由不受影响。

真实 production regression 已确认：复杂追逐 → spatial control；受控复验 → evidence-first；关系场景可以 `NONE`；payoff → `NONE`。

Curator 得到候选以后仍需判断当前场景是否真的缺少某种读法，候选卡本身不构成生成 Projection 的理由。

### 当前 GBrain scoped semantic 限制

GBrain 当前存在一个已观测的搜索行为：纯中文 query 在全库 hybrid search 可以返回相关结果，但 `query --scope prose-controls` 对中文 semantic 分支返回空；同 scope 下英文 alias/keyword 查询正常精准命中。doctor 同时确认 embedding coverage 为 100%，因此这不是缺 embedding。

当前单章 fallback / 专项修订路径如调用 Curator，应使用 Scene Family → approved English alias 的确定性 fallback 检索 Prose Controls，不依赖纯中文 scoped semantic search；默认 Batch 不执行这次检索。

## Prose Control Multi-Scene A/B（2026-08-24）

已完成 4 个不同 Scene Family 的低成本 A/B。每组冻结同一 Chapter Mission / Canon / BOOK Prose Profile / GPT-5.6 Terra high Primary Writer，ON 组只额外增加 1 张 Scene Prose Control；最后用 1 次 Luna high 联合 blind judge，标签随机打乱。

| Scene | OFF | ON | Δ ON |
|---|---:|---:|---:|
| Dialogue / Negotiation | 8.5 | 8.2 | -0.3 |
| Action / Pursuit | 8.3 | 8.7 | +0.4 |
| Payoff / Public Proof | 8.6 | 8.6 | 0.0 |
| Entry / Opening | 8.8 | 8.5 | -0.3 |
| Mean | 8.55 | 8.50 | -0.05 |

Blind judge 产品判定：**KEEP OPTIONAL**。

结论：Prose Controls 有真实增量价值，但不是统一正收益。`spatially-traceable-causality-v1` 在复杂追逐中最明显改善空间链、动作接触与敌方策略变化；Dialogue 与 Entry 的完整 control 注入则更容易诱发未冻结细节、机制解释和程序化扩写；Payoff 与现有 Reader-First / Human Reaction / Public Proof 规则高度重叠，当前增量接近零。

因此当前不冻结“每章自动 ON Prose Controls”。保留 Curator 的 Scene Family 检索和 1 主卡选择能力，但 control 是否进入当前章仍保持 OPTIONAL。下一轮只做两个很小的验证：Action 再换一个场景复验；Dialogue / Entry 测试 Curator 将 control 压成 2—4 句 scene-specific projection 后，是否能消除 boundary drift 与 over-explanation。

完整实验见 `books/real-exp-prose-control-ab-multiscene-v1/AB_REPORT.md`。
## Micro Projection A/B v2（2026-08-24）

在首轮 4 Scene A/B 的 `KEEP OPTIONAL` 基础上，进一步验证“抽象解释抑制 + 短 projection”：

- 7 张 Prose Controls 均加入共享 stop rule：动作、对白、物体变化或人物反应已经让意义成立时，不追加“意味着 / 说明 / 显然 / 可以看出 / 这不是……而是……”式同义解释；只有当前 POV 必须据此选择时才保留具体判断。这不是禁词表。
- Action 换成公开考核近身对抗复验：OFF 8.6 / ON 7.8；结合上一轮复杂路线追逐 ON +0.4，说明 `spatially-traceable-causality` 只应优先用于追逐、多人、移动地形、多入口等读者可能丢失方位/因果的 Action，不应覆盖简单一对一。
- Dialogue 完整 Control 上轮 ON -0.3；本轮压成三句 scene projection 后仍 ON -0.3。说明问题不只在长度，当前基础 Writer 已能完成多数谈判；`dialogue-state-pressure` 继续 OPTIONAL，并禁止为执行控制新增交易条件/回合。
- Entry 完整 Control 上轮 ON -0.3；本轮三句 projection 变为 OFF 8.1 / ON 8.5（+0.4）。因此 `action-anchored-grounding` 保留完整研究卡，但增加短 `Writer Projection` 作为生产候选；至少再跨一个 Entry 场景复验后才 promotion。
- 抽象解释指标在 Action 1→0、Dialogue 1→0，但 Entry 0→1；因此 stop rule 有方向价值，但不能升级成机械禁词/重写门禁。

当前产品判断仍是 **KEEP OPTIONAL**；短 projection 比“把完整研究卡压给 Primary”更值得继续验证。完整实验见 `books/real-exp-prose-control-projection-ab-v2/AB_REPORT.md`。

GBrain final hygiene: **3747 Pages / 15705 Chunks / 15705 Embedded**; updated prose-control slugs are single scoped pages with no accidental root-level duplicates.

## Selection Prose DNA v2（2026-08-24）

六本新经典的 85 个 scene windows 已重组为六维 Selection DNA：

| DNA | 核心问题 |
|---|---|
| Attention DNA | 作者什么时候愿意花字，什么直接压缩？ |
| Knowledge DNA | 哪些东西现在解释，哪些即使存在也暂时留着？ |
| Causal DNA | 因果写到什么粒度已经足以支持下一步？ |
| Reaction DNA | 人物状态怎样通过动作、对白、物件与社会行为泄露？ |
| Rhythm DNA | 句段怎样跟随真实 scene beat / state change 改变？ |
| Lexical DNA | 哪类具体名词、动作/结果动词和判断词成为功能落点？ |

`Detail Selection` 横跨六维：不是增加 sensory density，而是选择删掉后会损失人物、因果、关系、身份、身体、尺度或 payoff 读法的 context-specific detail。

Terra final fidelity audit：**PASS_WITH_EDITS**。六本共 **85 canonical refs**，source IDs / locators 全部可回溯；没有新增原著证据。审计要求删除《斗破》重复半稿、去掉 Production Implications 中的配额感、收窄 Dialogue / Spatial applicability、取消 Payoff 独立 projection，以及禁止为了满足 Reveal 卡而人为制造未知，均已落实。

## Selection Projection Multi-Scene A/B v3（2026-08-24）

本轮第一次直接测试新结构：`Selection DNA / BOOK / Canon / current Scene → Curator → 2–4句 Projection → Terra`。四组冻结同一 Primary 基线，OFF 为 `NONE`，ON 只增加 Scene Projection；一次 Luna high 联合盲评。

| Scene | OFF | ON | Δ ON |
|---|---:|---:|---:|
| Entry | 7.8 | 6.9 | -0.9 |
| Complex Action | 6.9 | 7.8 | +0.9 |
| Discovery / Reveal | 8.2 | 8.7 | +0.5 |
| Emotion / Relationship | 7.7 | 8.4 | +0.7 |
| **Mean** | **7.65** | **7.95** | **+0.30** |

ON **3胜1负**。Complex Action、Reveal、Emotion 均得到正增益；Entry 的反证表明：当基础事件链已经天然清楚时，再加局部写作压力会让动作模板化。因此产品决策不是“默认 ON”，而是：

> **PROMOTE PROJECTION COMPILER / KEEP PROJECTION OPTIONAL.**

Scene Projection 能力进入常规 Curator，但内容默认可空；`NONE` 是正常结果。成功标准不是每章都产生 Projection，而是需要时给 Writer 少量局部选择压力，已经足够清楚时不干预。

完整实验：`books/real-exp-prose-selection-projection-v3/AB_REPORT.md`。

## Priority Selection DNA v2 扩展（2026-08-24）

新增把《全球高武》《修真聊天群》《第一序列》《将夜》《道诡异仙》《诡秘之主》的旧 Prose DNA 升级为 Selection Prose DNA v2。此批不重新读取原著，直接复用已有 bounded scene evidence，共 **70 canonical evidence refs**；六卡均 `active_inspiration: false`，仍只作为 Curator 研究/evidence 层。

Terra fidelity audit 重点检查 evidence 越权、量化 hard rule、source-style leakage 与 Production Implication 强制化。两轮定向清理后 final recheck v2：**PASS**。

跨书增量最重要的是“人物声音不是口癖，而是压力处理方式”：人物注意/误判/拒答/保护/交易的对象不同，才形成不同声音。另继续强化：具体动作/数字/待遇承担强弱与身份，Knowledge/Causal 在足够支持当前选择时停止解释，Reaction 不设人味配额，Rhythm / Attention 跟随 scene beat。

唯一真正的新 Control 候选为 `character-voice-pressure-routing-v1`，当前 **HOLD / active_inspiration: false**，不加入 production routing；需要独立 A/B 后再考虑。`social-repricing-status-proof` MERGE 现有 result-stop / dialogue / scale / public-proof，不新增卡。

与 Story Batch D 合并导入后 GBrain 最终为 **3785 Pages / 15780 Chunks / 15780 Embedded**，embedding debt = 0。Semantic query 可以命中新 v2 / HOLD candidate，但 TGN 会过滤所有显式 `active_inspiration: false` 页面。

完整本地报告：`reference-corpus/operations/gbrain-prose-craft-v2-priority-20260824/FINAL_PRIORITY_PROSE_REPORT_20260824.md`。
