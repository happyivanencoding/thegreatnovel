# Chapter Runtime and State

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义章节 Runtime、Canon、State 与恢复边界。

## 定位

章节 Runtime 只负责执行已经批准的故事，不重新设计长期主线。当前默认模式是 `curator_primary`：

`Director → Context Curator → Primary Writer → Authority Reviser → State Extraction`

Authority Reviser 是默认 `curator_primary` 的固定正文修订节点；Specialist / Integrator 不在默认链，只有作者明确启动局部 repair 时才临时进入。`single`、`hybrid_selective`、`hybrid_full` 仅保留兼容与专项实验用途。

章节 Runtime 默认不直接读取 raw GBrain。GBrain 对章节层的影响只通过已批准的 Story Program / Outline，以及离线深蒸馏后的 source-blind Scene Deep Craft 间接进入；原著 evidence 不进入章节模型。当前 Scene Skill v2 冻结为 **24 个 Primary + 3 个不进 Router 的 Shared Reference Lens**；Authority Reviser 目前只有 `social_bargain_decision` 与 `relationship` 两张 Skill 开放短 `Revision Watch`，其余 22 张为 `NONE`。

已批准 `WORLD_VISION.md` 仍是一等 World Root，不由 Outline 的 `BOOK §2` 摘要替代。长期进入新 World Horizon 后，Runtime 组合 `World Root + 当前章已生效的 Forward World Expansions`，再确定性裁成安全 `WORLD AUTHORITY`。Expansion 只投影公共现实、力量/身份/价值尺度、公开地点/势力和具体价值物；世界人物未公开欲望、隐藏行动、未知边界与未来 reveal 不因存在于 Expansion 就直接进入 Writer。`scope=instance` 只在自己的 `Effective From/Until` 章节窗口生效，离开副本后 Local World 自动退场；跨副本留下的能力、物品、关系、知识与 Meta consequence 继续由 Canon 承载。

Outline 在 `BOOK §2 / Reader Release Map` 只保存 timing-sensitive、与该章实际事件相交的首次释放；未来仍作为 reveal 的答案不能提前排入 Map。Runtime 按当前章读取该条目，再从 WORLD AUTHORITY 做 bounded prefetch。Director 不读取完整 World，Curator 不重做 release 选择，Primary 也不自行选择世界资料。

Progressive Canonization 的作者隐藏真相使用独立 `MYSTERY_CONTROL.json`，**不属于 Canon、BOOK、AUTHOR NOTES 或普通章节上下文**。`AUTHOR OPEN` 里作者自己也没有答案；`AUTHOR FIXED HIDDEN` 只允许 Story Refresh / World Expansion 对应 planning route 读取。Story Program 保存时，`MYSTERY REVEAL CONTRACT` 被代码从 Proposal 正文确定性剥离并单独保存；Outline 只得到 `第N章 + [MYSTERY-REVEAL:ID]`，看不到 Event Atom、State Residue 或 raw Fixed Point。

`MYSTERY_CONTROL.json / compiler_inputs` 只保存低频作者定真流程的**精确 Compiler 输入快照**：当前 Thread、selected candidate、Decision Surface、author planning need 与当时 BOOK/Canon 原文。它不进入 Story / Outline / chapter Runtime；用途只有一个——采用候选前发现候选、Thread 或 Canon 是否已经变化。变化即 stale，重新编译；不使用 hash/checksum 代替直接文本比较。

章节侧不新增 Mystery 节点。Reveal 前章的 current plan 保持原样；只有 `Reveal Chapter == 当前章` 时，runtime 才把 reader-facing `Event Atom + State Residue + Still Open` 确定性并入当前章计划，再沿原来的 `Director → Curator → Primary → Authority Reviser → State` 执行。**raw Hidden Fixed Point 永远不进入 Writer。** Reveal 必须由正文动作/物证真实发生；State 只能从最终正文提取已经发生的 Residue。随后作者显式 advance 才把该层从 `FIXED_HIDDEN` 转回更深 `OPEN`，并将已揭 Residue 作为后续 Known Anchor；不能因为 planning 已经知道答案就提前改 Canon。

## 延迟基线与安全优化边界（2026-08-29）

冻结 20 章真实链的正常采用节点平均为 **6.17 分钟/章**；计入废弃重跑、Ch1 后 Replan、十章 Review 与终检 Repair 后，章节批次实际摊销为 **7.73 分钟/章**。正常链中 Curator 占 31.4%，Authority Reviser 占 37.1%，两者合计 68.5%；Primary Writer 只占 15.0%。因此慢的核心确实在两个高推理辅助节点，但“耗时高”不等于可以直接删除或降档。

当前只冻结不改变 Story Authority 的 Phase 0：

- `current_long_block` 按文本自带章节范围确定性投影：保留覆盖当前章的最窄块；范围明确但已过期时丢弃；无法解析时保留原文，不让 LLM 猜作者意图。该投影同时作用于 rolling plan、chapter plan context 与 growth/payoff projection。
- Hybrid Chapter Runtime 对 raw GBrain / Reference Programs fail closed；章节只消费批准上游、safe Authority 与 source-blind Scene Skill。
- Curator 固定输出合同显式统一为 13 个区块，不再出现“列表只写 9 项、后文又要求 4 项”的矛盾。
- 耗时账分开保存 adopted chain、真实批次 rerun/Review/Repair 与上游摊销；每节点记录 Prompt chars、input/cache/output/thought、wall、fallback/adopted 与 Reviser diff。

Phase 1–3 已完成冻结输入、正常下游与最终正文 Reader + Authority 双盲，但均未达到 production 标准：Luna-medium Curator 虽约快 61%，Authority 由 high control 以 5:2 获胜；Slim Curator 约快 70%，却没有稳定模型赢家并出现时序/动作对象漂移；medium / Patch Reviser 在商业读感或全章状态闭合上失败；Conditional Director 约快 41%，商业读感由 full control 4 胜 1 平，且个别章出现 Agency 降级或 `[PLAN OUTCOME ADJUSTMENT]` 越权。因此默认路由继续保持 `Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`。

本轮按作者范围**没有修改 ACP runner，也没有修改前端**；二者不是未完成交付项。完整速度、盲评与正文对照见 `books/real-exp-chapter-latency-optimization-20260829-v1/RESULTS.md`。

### Latency Innovation Round｜不删质量保险的路线（2026-08-29）

后续又系统测试了：Parallel Pre-Curator、Authority Blueprint、并行 Authority Watch + medium Reviser、Paragraph-Delta Reviser、Commercial Spark、跨章 Speculative Director、Ten-Chapter Attention Kernel、Reviser+State 合并、严格删除式 Reader Polish 与持久 ACP process。所有语义路线均继续接回正式下游，并同时做商业 Reader 与 Authority/Canon blind；Paragraph-Delta 还做了独立重复运行和跨书复验。

最终没有新的章节语义路线达到 production 标准：

- Paragraph-Delta 可把 Reviser wall 缩短约 48%—57%，跨书 Reader 4:1 偏 Treatment，但 Authority 为 control 2 / mixed 3，且同书两次独立运行只有 1/5 最终正文完全一致；
- Speculative Director 的 `State + Director` 子路径约快 45%，接回完整 Curator/Primary/Reviser 后只快约 12%，Reader 3:3、Authority control 4 / treatment 1 / mixed 1；
- no-old-Canon Speculative Director 完整下游约快12.4%，Reader 3:3、Authority control 3 / treatment 2 / mixed 1；它比旧投机稍稳，但仍在第15章丢三方合作、同步危机并新增世界事实；
- Ten-Chapter Attention Kernel 摊销后只快约 4.8%，Reader control 3:2，Authority control 2 / treatment 1 / mixed 2；
- Reviser 与 State 同调用在两章中反而慢约 35%—50%；
- 严格删除式 Polish 可并行隐藏在 State 后，但两次20章触发集合只重合2章，跨书10章全 `NO_CHANGE`，不值得新增常驻 Agent。
- 完整 Curator 改为 Terra high 并接回相同 Primary/Reviser 后，四章总链平均快约26.9%，但 Reader 与 Authority 都是 Terra 2 / Luna 2；第10、14章仍出现行动者、独自稳车、分身硬规则与残压 Ending 漂移，不能改默认模型。
- 去掉当前 Canon 的 Speculative Director 完整下游平均快约12.4%，Reader 3:3、Authority control 3 / treatment 2 / mixed 1；第4章仍会补出第二袋钱，第15章仍漏水路确认和同步危机，说明实时 State 不能从注意力绑定中拿掉。
- State 改 Terra low 在8章中总体慢约3.3%，且0/8四字段 exact；Paragraph Manifest 第一版5/5 fallback，第二版仅2/5采用且平均仍更慢，均停止。

唯一零语义风险的正信号是：保留 fresh session、只复用 ACP adapter process / initialize，6次最小调用相对快约28%，但绝对只省约1.26秒/调用；前端不使用这条 runner，本轮也不修改 ACP runner。默认章节链与模型路由继续不变。完整证据见 `books/real-exp-chapter-latency-innovation-20260829-v1/RESULTS.md`。

下一代高潜方向不是再加一个 classifier，而是把 Frozen Mission / Reader Release / Power / Human / Ending 编译成代码可验证的 `Atomic Chapter Obligations`，再让 Paragraph-Delta 只有在 actor-action-object、result/state/ending、ownership/time/money、power ruler、unknown boundary 与 protected commercial value 全部闭合时才可采用，否则直接保留 full Reviser。


### Atomic Authority IR v1 实验边界（2026-08-29）

旧 Atomic v0.3 只保留为 Boundary Discovery Experiment。正式架构是两个互不越权的产物：

```text
Atomic Authority Contract
  = Entity Registry + Frozen Mission / Canon / World / Power / Human / Reader Release IR

Primary Preservation Map
  = Runtime签发的 Primary fact evidence + blocker edit window + optional Curator fragment hint
```

Hard Contract 只接收 source-specific trusted artifacts：私有 issuer、normalized-fact SHA-256、稳定 Entity ID / slot、显式 from-state、dependency cycle 与 source conflict 校验。Curator / Primary / Reviser / Judge 不能创建 Hard Fact、Conflict 或 Identity；空 Contract 不 eligible；Registry / Fact / Contract / Preservation 均为不可变快照，序列化重载会重建 artifacts 并复核 digest、fact membership 与 Contract hash。

Preservation 默认依靠 Edit Locality，而不是 Desire / Surprise / Relationship detector。Evidence binding 由 Runtime 签发并绑定 Primary SHA-256；Curator只能给 editable window 内的窄 protection hint，不能伪装成 evidence、扩窗或改变 Contract。Gate 还会拒绝 paragraph-count shift 与 locked-paragraph drift。

两本书四章静态实验：4/4 source-pure、4/4 preflight eligible、4/4窗口外修改被阻止，平均只开放3.11%段落。57项 focused tests、22/22 Schema/runtime checks通过。自由文本 Director Sidecar 三版全部失败：verbose JSON wall +205.83%，compact JSON +147.41%，micro DSL +146.45%；compact blind 中Story 3:1偏原Director，Authority 3:1偏Sidecar。

2026-08-30 已完成 native `DirectorStructuredDecision → Runtime双投影 → Curator → Primary → Authority Reviser → Final Draft` 的真实两书四章E2E。冻结v2协议后2次Treatment均8/8 Native accepted、手工fixture结构覆盖100%，但这不是Contract completeness：Mission Story为6.99 vs Control 8.60，Mission Authority 6.55 vs 8.41，Final Authority 6.79 vs 8.04；只有Final Story方向性更好（8.41 vs 7.88）。正确串联Control平均325.954s/章，Native平均351.566s/章，实际慢25.612s/章（7.86%）；Primary Oracle仅2/8可直出Final，即使假设完美零成本Gate也只理论快1.68%。因此当前Native human-Mission replacement与Full-Reviser免税均不进入Production；Hard IR下一候选应前移到Story/Outline/Runtime已决定的结构化事实，保留Director的高故事密度Mission。Unsupported chapter仍绕过Atomic走现有Full。完整报告：`books/real-exp-native-structured-e2e-20260830-v1/RESULTS.md`。

同日继续完成 `rich free-text Director → Curator → Primary → deterministic Atomic bypass Gate` 的冻结E2E：两次fresh、8章中Gate仅声明4次shape supported，但0/8实际PASS，最终Control 2457.403s、Treatment 2457.424s，等价零加速；Gate本身仅约2.5ms/章，瓶颈不是代码wall，而是free prose→typed evidence无法低成本可靠证明。更重要的是，7组strict Oracle看似可直出的Primary/Reviser pair经两轮匿名复核后，Story 14票为Reviser 10胜/Primary 4胜，Authority为Reviser 8胜/Primary 1胜/5平，0/7稳定质量等价。由此冻结：**Contract Gate只能证明其已覆盖的Authority，不证明Full Reviser无Reader/Story价值；Authority PASS不是skip-Reviser充分条件。** 当前Full Reviser平均131.3s/章、占Control wall约42.74%，但仍是value-bearing stage。不要扩大中文surface parser或新增LLM classifier；未来只有先使Primary稳定达到Reviser后的Story+Authority、让Reviser趋近no-op，才重新测试skip。完整报告：`books/real-exp-free-text-atomic-gate-skip-reviser-20260830-v1/RESULTS.md`。

为避免旧case过拟合，又把“先让Primary接近Final”在两部**生成于Treatment冻结之后的新小说**上复验。Candidate 1 的5行self-check在新书1中把Primary Authority略提高，却让Reviser Authority增益从+8.125扩大到+12.375，0/8 exact no-op；Candidate 2 只确定性重投影Direct Result / State Change / Ending / Reader Release / Core Power / Permanent Boundary，在新书2中使Primary Story +2.812，却让Authority -2.125、Hard问题32→41，Reviser gap仍扩大，且Primary+Reviser反而慢4.47s/章。Luna-medium屏幕是唯一强速度信号：Reviser 133.3s→59.6s（约-55%），Story不降，但Authority 57.5 vs high 61.875、Hard问题9 vs3，按冻结规则停止。**因此当前不再用通用Primary自查或简单事实重复追求no-op；任何降档/skip候选先在derivation证明Primary→Reviser Story+Authority gap收敛，再冻结Treatment并用全新held-out小说验证。**完整报告：`books/real-exp-reviser-noop-upstream-heldout-20260830-v1/RESULTS.md`。

## 节点职责

### Director

只根据当前剧情块、当前章计划、压缩成长信息、Canon Index、最近摘要、章末衔接和作者意图生成八字段事件合同。runtime 先把 Future 10 当前条目确定性拆成 `本章唯一可执行事件预算` 与 `章末 Handoff Reservation`：前者是本章 WHAT HAPPENS 的唯一预算；后者只能制造下一章压力/入口/来人/线索，不能提前结算。当前剧情块只作阶段背景，不授权把未来付款、身份、获得或升级搬进本章；带明确章节范围的 Long Block 只有覆盖当前章才进入，显式过期或找不到合法匹配时直接丢弃，不回退整份旧长纲。它决定 WHAT，不提供正文句式，不重做 World / Story Program / Outline。**单章计划只是当前剧情块的压缩投影**：当它已经提到试场/选拔/招募/契约，但把同一剧情块中已批准的具名机会价值压掉时，runtime 确定性恢复一条匹配的 `当前具名机会权威` 给 Director；Director 保留具体机会名与“成功参与通常打开什么”，不能再降成“公开机会 / 资格 / 更大机会”。该投影不生成新回报、不提前宣布结果、也不从未来章偷事实。若本章是 Core Asymmetry 首次被外界看见、新层级/质变、新复合用法、进入更高圈层后的首次重新观察，或旧社会估值明显过时，`对手或世界反应` 按现场条件允许同时规划三条并列 Public Proof：真实观众的群体震动、懂行者 `Ruler Calibration`、关键人物 `Behavioral Repricing`；三者没有高低之分。主力量 Public Proof 优先让三条线共享 `Current Power Position` 与对手精确位置：群体承受明确数字差带来的现场重量，懂行者说清几级/几星/几重差多少，关键人物据此改变待遇、报价、战术或敌意。越级胜负不授权修改主角精确位置。长期后果只有会继续改变行动/关系/资源/敌意/信息流时才进入状态与结尾。

### Context Curator

从确定性 Index-first 预取中筛选 Writer 真正需要的信息，输入包括 `WORLD AUTHORITY`、**从 `CHARACTER.md` 确定性截取的 Frozen Human Core**、BOOK Contract、Canon、计划、Prose Profile、Open Promises，以及 Scene Skill v2 的紧凑 Catalog。Catalog 只暴露 `skill_id + Primary Reading Question + 一行 Projection Guidance`；Curator 选择 1 个 Primary、最多 1 个 Secondary，并只在当前 Mission / Canon 仍有真实 realization 缺口时把 Deep Craft 编译成 2—4 句 `Scene Prose Projection`，已经清楚则写 `NONE`。完整 Scene Skill、原著 evidence 与 source-specific 研究不进入章节 Prompt。Power Core 不在章节期重复注入，可变状态仍由 BOOK/State 提供。World fact 的选择时机由 Outline 决定：Plan 排程了哪条已批准事实，Curator 就保留/压缩哪条；Plan 没排程时不自行从完整世界挑一段补课。若 Reader Release 是开篇 `公共常识`，Curator 必须保留可直接说明的事实句义，不把“主流力量是什么 / 粗略怎么分强弱 / 日常危险为何改变习惯 / 上升入口为什么重要”压成道具、意象或模糊氛围。冻结 Human Core 高于最近几章行为归纳；近期救人、负责或克制只能改变关系预期，不能静默改写主角稳定人格。场景自然触发已批准私人欲望时，Curator 应保留一个可直接进入 POV 的具体触发，而不只剩职责协作；若 Frozen Human 明确某个具体人会改变选择，而本章正发生近身照料、重逢、分别、私密靠近、嫉妒或邀请等关系性现场，默认属于自然触发，保留一个克制 cue 即可。高价值 Asymmetry Reveal 若已由 Plan/Director 批准，Curator 不应把它压成单一“震惊 cue”或只剩专家说明：有真实群众时保留群体震动的场面价值，同时保留最有资格者的 ruler 解释与关键人物的行为重新定价；三路可以一起成立。主力量 Public Proof 若 Canon / World 已给精确位置，Curator 的短 Projection 应保留这把坐标，让专家校准可以直接落成“43 vs 58 / 三星 vs 五星”之类最短比较，而不是重新压成“明显越级”。新 `observer-specific repricing` Deep Craft 当前仍是 PILOT，尚未因此新增独立 Primary taxonomy。它不补读全库、不重新规划、不把 Planning Language 改写成正文。

Curator 返回后，runtime 还会做一次**不调用模型的 unresolved fact projection**：从 `Curator Audit`、`Relevant Open Promises`、明确未解的 World Rules 与 `Payoff and Promise Window` 中抽取约束，形成紧贴 Chapter Mission 的 `UNRESOLVED FACT BOUNDARY`。这不是新节点、Reviewer、RAG 或 Hard Gate；它只把 Curator 已经识别出的“仍未知 / 未兑现”提高到 Primary 的高显著事实边界，避免长篇时被埋在较长 Curated Context 中。

### Primary Writer

只写正式正文。输入以 Director Contract + `UNRESOLVED FACT BOUNDARY` + Curated Context + 必要连续性为主；当前章已批准的 `结果 / 状态变化` 会确定性并入 Frozen Mission 的 `状态变化`，避免 Director 静默压掉力量/身份跨档、持有关系或其它不可逆结果；若已发生 Canon 真使原结果不可能，Director 必须用 `[PLAN OUTCOME ADJUSTMENT]` 显式记录最小调整。**不直接读取完整 Scene Skill**，只使用 Curator 已编译的短 `Scene Prose Projection`（可为 `NONE`）；不直接读取 raw GBrain，不承担状态记账或长期结构修复。已排程 Reader Release 是本章要兑现的 timing decision：Curator 已投影时，用最短充分的直接旁白或场景表达说明。**开篇公共常识以“普通读者不用推理就能复述规则”为兑现标准**：可以用 1—3 个短说明段直接讲清，不要求先制造问题，也不能用火盆、服装、站位、专名或氛围暗示替代基础答案。若同一事实包含地点/势力/传承的价值，也保留一个最短欲望锚点；隐藏原因与未来 reveal 继续未知。Curated Context 已明确带入私人欲望且当前场景自然触发时，不把它自动净化成职责协作或成熟沟通。高价值 Asymmetry Reveal 若 Curated Context 已带入 Public Proof 要求，Primary 按现场条件允许三路同时实现：有真实观众时让群体震动完整成立；最懂行者用 1—3 句说明正常值、超标点和稀有/异常意义；关键人物用改口、加价、退距、换战术、招揽/敌意或待遇变化完成 Behavioral Repricing。三者没有高低之分，不因“克制”自动删群众反应，也不要让所有人轮流说同一套专业解释。主力量已有精确主尺时，懂行者优先用一次精确位置比较完成压缩，例如“43级对58级”；群体反应和重新定价围绕同一事实展开，不另造第二把强弱尺。Canon / Curator 已标记为未知、未解释、真假未定或原因未明的过去事实继续保持未知；除非 Director Contract 明确规定本章新成立的事实，Primary 只能创造当前场景实现细节，不得把 plausible explanation 写成 retrospective canon。对白同样不能成为补 Canon 的旁路。

### Authority Reviser

固定使用 **GPT-5.6 Luna high**。Primary Draft 是唯一待修订正文底稿；Reviser 不是第二个 Director / Writer，而是 **Preservation-First Authority Recovery**：先假设已写好的正文正确，只有能指出具体失败的局部才允许修改。

它重新获得 Primary 为减负而没有直接持有的远端权威：冻结 Chapter Mission、Curator、safe `WORLD AUTHORITY`、逐条 `Reader Release`、`CHARACTER.md` 的 Frozen Power Core + Frozen Human Core、Canon Index / 上一章必要章末，以及 Primary Draft。若 Curator 选中的 Scene Skill 有经过 A/B 验证的极短 `Revision Watch`，Reviser 只额外看到这 1—2 行 failure-triggered 提醒；完整 Generation/Revision Lens 不进入。raw GBrain 固定 OFF，完整 World / Character 原文也不直接进入；所有远端输入都是确定性安全投影。

允许的修订只有三类：

- 删除/压缩反复确认、重复证明、结构分析、材料诊断、路线计算、验证/报告/登记式展开和无新选择的 Competence Filler；若 Primary 把一个已冻结的大方向选择实现成多段“谁守/谁撤/谁赔/谁承担/谁见证”的协调流程，Reviser 可以激进压到最短因果，但不能越权改 Frozen Mission 本身；
- 补回 Authority / Reader Release / Curator 已批准但 Primary 漏掉的最短充分世界信息、Core Power 独有体验、Frozen Human 私人 cue 或一个有故事功能的生活细节；Planning/Authority 的“身份入口、行动空间、社会重新定价、责任边界”等后台分析词若直接漏进对白/贴身叙述，翻译成人物会说的话、具体待遇或动作，而不是继续扩写后台标签；
- 在不改变事实的前提下，把过多 Supporting Implementation 的笔墨还给 World Entry、Rival、Relationship、Core Fantasy、Choice、Payoff 或 Consequence；大型 Public Proof 若群体震动、专家校准与关键人物重新定价都被当前 Authority 支持，不以“克制”理由主动削成只剩一种。

同一维度如果 Curator / Primary 与 Frozen Mission / Canon / safe World / Frozen Power / Frozen Human 冲突，以 Frozen Authority 为准，并对最终稿做语义级全章清零。修冲突段落时先逐句 salvage：本身合法、只因错误时点/因果而失效的高价值 Core Fantasy / Relationship / Desire / Payoff / Surprise / Social Repricing 句移到最近合法位置；salvage 不保护周围报告、登记、路线或普通实施。

Reader Release 的“存在”与“清楚兑现”分开判断：开篇公共常识若只通过道具/环境暗示存在，普通读者仍需自己推理出规则，Reviser 应在不改变剧情的前提下补最小直接说明；生活细节可以保留，但不能冒充 Orientation 已完成。本章若 Frozen Mission 已明确跨过公开力量/身份档位，而 Primary 只留下“打出该级战绩 / 凝影了 / 通过了 / 被记名”等暗示，Reviser 在结果处补一次最短的新档位直称；数字主尺同样如此，“42级打赢58级”不能替代批准的“提升到43级”。若第一次 Authority Revision 仍漏掉计划中以“进入 / 踏入 / 晋升 / 突破 / 提升到 / 达到 / 成为”等形式明确批准的里程碑状态，Run Ledger 不允许直接采用：它自动把同一 Reviser 的 Prompt 收窄为一次 Preservation-First `Outcome Repair` retry；只补最小因果与一次直称，不重做剧情。该 retry 最多一次，仍失败则节点保持 failed，State 不运行。

不得改变主要事件顺序、人物决定、胜负、资源得失、伤势、身份结果、Direct Result、State Change、Ending 或未知事实边界；没有明确问题的句段默认逐字保留。删除一段前必须先确认不会同时删掉新的 `State Change / Social Repricing / Reward / Relationship Change / New Desire / Next Opportunity`。

在 `curator_primary` 中 Primary 不能直接成为 `final_source`。Authority Reviser 只有在显式里程碑 Outcome 检查通过后才可采用；若触发一次性 Outcome Repair，则 retry 通过后仍由同一个 Authority Reviser 节点成为 final source。后续作者显式 repair 若运行 Integrator，则 Integrator 可替代它。State Extraction 后端会重新读取 Run Ledger 的最终来源，页面里的 Primary 文本不能旁路进入 State。

### Optional Repair

`opening / dialogue / action / emotion` Specialist 与 Integrator 只在作者显式开启 repair 时使用，而且必须发生在 Authority Reviser 之后。Specialist 读取 Authority Revision 的相关局部；Integrator 也以 Authority Revision 为底稿，可以全部拒绝。若没有有效 Patch，`final_source` 继续保持 Authority Reviser。

### State Extraction

只从最终正式正文提取已经发生的事实，不读取 GBrain，不把计划、推测或参考机制写进 Canon。社会反应本身不自动进入长期状态：只有某个观察者/圈层因直接目击、专业推断或二手来源形成了会继续改变后续选择的稳定知识/误解，并已经导致关系、资源、敌意、战术、准入或信息流变化时，才把“谁知道/相信什么、仍不知道什么、因此持续怎么做”写入普通 Canon；一次性惊讶或短期 Ruler Calibration 不建额外 Disclosure Ledger。默认 `curator_primary` 下必须从 Run Ledger 的 `authority_reviser` / `integrator` `final_source` 重新读取正文；Primary Draft 不得直接进入 State。

State Extraction 还为长篇 Forward Evolution 提供**已经发生的原料**，但不新增一个大数据库。`PERSISTENT CANON` 仅在真实需要时维护：

- `Power / Capability`：第一行固定保存 `Current Power Position｜主尺：…｜精确位置：…`，随后维护后续已获得/证明的 Power Delta、身体变化、兵器权限与关键边界；Frozen Power Core 不在这里重写。等级没变时沿用上一精确位置；只有最终正文明确突破才更新。State 模型偶尔漏写该行时，runtime 确定性保留上一 Canon 位置；越级胜利、承受高阶攻击或社会重新估价都不能推断升级；
- `Active Relationships`：仍会改变选择的关系状态；
- `Identity / Access`：仍会改变待遇/入口的长期身份；
- `Knowledge / Enemy State`：确认知识、重要误解与持续敌我状态；
- `World State`：已经发生、且未来 protagonist-blind World Expansion 需要知道的世界级变化；不得写主角私人欲望或“下一世界应该给什么”；
- `Tracked Assets`：仍有长期选择价值的持有/位置/状态。

**State Extraction 不判断 Human Development。** 当前欲望、关系变近、连续几章救人/负责都先留在 State；只有周期性的 Human Development 阶段基于更长历史才能判断 Stable Choice Bias 是否真的向前变化。

## Canon Memory

新书第一次进入 Chapter Runtime 时，Outline 提供的 Initial State 必须是严格的 **T0 snapshot**：只包含 Chapter 1 第一场事件发生前已经成立的事实。Outline 中刚刚规划出的 Future 10 / 中期剧情块结果仍是 Plan / Open Promises，不能因为“已被规划”而提前成为 Canon。

章节状态区使用五个语义层：

- `ACTIVE SCENE STATE`：下一章马上需要的地点、人物、伤势、重要物品、追兵、倒计时和直接目标；可整体替换。
- `PERSISTENT CANON`：长期能力、限制、关系阶段、持久资源、身份、确认知识、长期伤势和敌我状态。
- `RECENT SUMMARIES`：只保留最近少量章节摘要，默认不无限累积。
- `OPEN PROMISES`：仍需兑现的近期/长期承诺，确定性去重并保持有界。
- `AUTHOR NOTES`：作者备注，不属于 Canon；代码逐字保留。

State Delta 只提出：

- `# State Delta Audit`
- `# Proposed Active Scene State`
- `# Proposed Persistent Canon`
- `# Proposed Chapter Summary`
- `# Proposed Open Promises`

State Delta 不改 BOOK Contract、计划或正文；应用状态更新时只替换 `# 当前状态、未兑现承诺与作者备注` 区块，前面的总体设计、中期规划和 Future 10 必须逐字保留，不能通过 parse → recompose 顺带重写。只有作者显式批准后才应用状态更新。

`CURRENT_CHARACTER.md` 不是章节期的新全量上下文，也不取代 Canon。它只在长篇规划边界按需从 Frozen Origins + 当前 Canon + 已批准 Human Development 确定性编译；Canon 一更新，已有 Current Character 会 stale。普通章节继续使用 Frozen Core + bounded Canon，不因此增加每章 Prompt 负担。

## Run Ledger

每章目录：`books/<book_id>/runs/chapter-NNNN/`。

Ledger 记录固定节点的 Prompt、Response、状态与最终采用来源，不是后台调度器或通用 Workflow Engine。节点状态只使用：

`pending / completed / failed / skipped / stale / adopted`

底层节点仍可记录：

`director → curator → primary → authority_reviser → opening / dialogue / action / emotion → integrator → state_delta`

在默认 `curator_primary` 中，`authority_reviser` 必跑，Specialist 与 Integrator 默认 `skipped`；需要 repair 时只能在 Reviser 完成后显式激活。历史已完成 Run 不被新节点追溯改写；新/未完成 production Run 必须经过 Reviser。失败节点重试复用已保存 Prompt，不重跑无关上游；上游变化只让真实依赖的下游变为 `stale`。

`stale` 不是“必须重新调用模型”的同义词。Run Ledger 为新节点 Response 保存 exact-input receipt：当前 Prompt SHA-256、生成该 Response 时的 Prompt SHA-256、Response SHA-256 与 receipt status。上游变更后仍先保守 stale；当同一节点的新 Prompt **逐字相同**且旧 Response 文件未变时，保存 Prompt 会直接把节点恢复为 `completed / adopted`，UI 同时回填旧 Response 并跳过 OpenAI/Codex 调用。显式 retry 永远绕过 receipt；旧 manifest 没 receipt 时 fail closed 正常重跑。Digest 只用于决定是否跳过昂贵 LLM 调用，不用于语义等价判断。

Forward Evolution 继续遵守这条原则：World Root Rewrite 会按原依赖链使未来全面 stale；World Expansion 只影响 `effective_from` 之后已经存在的未来 Run，不杀死 Expansion 之前已经准备好的 Run；Human Development / Current Character / Refresh Story 只影响未来。已完成章节正文与历史 State 永远受保护。

## 实现边界

- `chapter_context.py`：确定性上下文投影与压缩。
- `hybrid_runtime.py`：Curator / Primary / Authority Reviser / Specialist 的局部文本投影，不调用模型。
- `run_ledger.py`：节点文件状态与恢复，不写小说事实。
- `storage.py`：显式保存与 State Delta 应用边界。

不要为章节 Runtime 引入数据库、队列、事件总线、通用 DAG、自动重试框架或新的全量上下文系统。运行时目标是：**少节点、窄上下文、事实与计划分离、失败可恢复。**
