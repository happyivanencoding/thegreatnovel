# Chapter Runtime and State

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义章节 Runtime、Canon、State 与恢复边界。

## 定位

章节 Runtime 只负责执行已经批准的故事，不重新设计长期主线。当前默认模式是 `curator_primary`：

`Director → Context Curator → Primary Writer → Authority Reviser → State Extraction`

Authority Reviser 是默认 `curator_primary` 的固定正文修订节点；Specialist / Integrator 不在默认链，只有作者明确启动局部 repair 时才临时进入。`single`、`hybrid_selective`、`hybrid_full` 仅保留兼容与专项实验用途。

章节 Runtime 默认不直接读取 raw GBrain。GBrain 对章节层的影响只通过已批准的 Story Program / Outline，以及离线深蒸馏后的 source-blind Scene Deep Craft 间接进入；原著 evidence 不进入章节模型。当前 Scene Skill v2 冻结为 **24 个 Primary + 3 个不进 Router 的 Shared Reference Lens**；Authority Reviser 目前只有 `social_bargain_decision` 与 `relationship` 两张 Skill 开放短 `Revision Watch`，其余 22 张为 `NONE`。

已批准 `WORLD_VISION.md` 仍是一等世界事实权威，不由 Outline 的 `BOOK §2` 摘要替代。Runtime 会把它确定性裁成不含 named 大事件 / 未解谜底的 `WORLD AUTHORITY`；Outline 在 `BOOK §2 / Reader Release Map` 只保存 timing-sensitive、与该章实际事件相交的首次释放；未来仍作为 reveal 的答案不能提前排入 Map。Runtime 按当前章读取该条目，再从 WORLD AUTHORITY 做 bounded prefetch。Director 不读取完整 World，Curator 不重做 release 选择，Primary 也不自行选择世界资料。

## 节点职责

### Director

只根据当前剧情块、当前章计划、压缩成长信息、Canon Index、最近摘要、章末衔接和作者意图生成八字段事件合同。它决定 WHAT，不提供正文句式，不重做 World / Story Program / Outline。**单章计划只是当前剧情块的压缩投影**：当它已经提到试场/选拔/招募/契约，但把同一剧情块中已批准的具名机会价值压掉时，runtime 确定性恢复一条匹配的 `当前具名机会权威` 给 Director；Director 保留具体机会名与“成功参与通常打开什么”，不能再降成“公开机会 / 资格 / 更大机会”。该投影不生成新回报、不提前宣布结果、也不从未来章偷事实。若本章是 Core Asymmetry 首次被外界看见、新层级/质变、新复合用法、进入更高圈层后的首次重新观察，或旧社会估值明显过时，`对手或世界反应` 优先同时规划 `Behavioral Repricing + Ruler Calibration`；长期后果只有会继续改变行动/关系/资源/敌意/信息流时才进入状态与结尾。

### Context Curator

从确定性 Index-first 预取中筛选 Writer 真正需要的信息，输入包括 `WORLD AUTHORITY`、**从 `CHARACTER.md` 确定性截取的 Frozen Human Core**、BOOK Contract、Canon、计划、Prose Profile、Open Promises，以及 Scene Skill v2 的紧凑 Catalog。Catalog 只暴露 `skill_id + Primary Reading Question + 一行 Projection Guidance`；Curator 选择 1 个 Primary、最多 1 个 Secondary，并只在当前 Mission / Canon 仍有真实 realization 缺口时把 Deep Craft 编译成 2—4 句 `Scene Prose Projection`，已经清楚则写 `NONE`。完整 Scene Skill、原著 evidence 与 source-specific 研究不进入章节 Prompt。Power Core 不在章节期重复注入，可变状态仍由 BOOK/State 提供。World fact 的选择时机由 Outline 决定：Plan 排程了哪条已批准事实，Curator 就保留/压缩哪条；Plan 没排程时不自行从完整世界挑一段补课。若 Reader Release 是开篇 `公共常识`，Curator 必须保留可直接说明的事实句义，不把“主流力量是什么 / 粗略怎么分强弱 / 日常危险为何改变习惯 / 上升入口为什么重要”压成道具、意象或模糊氛围。冻结 Human Core 高于最近几章行为归纳；近期救人、负责或克制只能改变关系预期，不能静默改写主角稳定人格。场景自然触发已批准私人欲望时，Curator 应保留一个可直接进入 POV 的具体触发，而不只剩职责协作；若 Frozen Human 明确某个具体人会改变选择，而本章正发生近身照料、重逢、分别、私密靠近、嫉妒或邀请等关系性现场，默认属于自然触发，保留一个克制 cue 即可。高价值 Asymmetry Reveal 若已由 Plan/Director 批准，Curator 不应把其社会校准压成单一“震惊 cue”：短 Projection 应同时保留观察者行为变化与专业 ruler 解释；新 `observer-specific repricing` Deep Craft 当前仍是 PILOT，尚未因此新增独立 Primary taxonomy。它不补读全库、不重新规划、不把 Planning Language 改写成正文。

Curator 返回后，runtime 还会做一次**不调用模型的 unresolved fact projection**：从 `Curator Audit`、`Relevant Open Promises`、明确未解的 World Rules 与 `Payoff and Promise Window` 中抽取约束，形成紧贴 Chapter Mission 的 `UNRESOLVED FACT BOUNDARY`。这不是新节点、Reviewer、RAG 或 Hard Gate；它只把 Curator 已经识别出的“仍未知 / 未兑现”提高到 Primary 的高显著事实边界，避免长篇时被埋在较长 Curated Context 中。

### Primary Writer

只写正式正文。输入以 Director Contract + `UNRESOLVED FACT BOUNDARY` + Curated Context + 必要连续性为主；**不直接读取完整 Scene Skill**，只使用 Curator 已编译的短 `Scene Prose Projection`（可为 `NONE`）；不直接读取 raw GBrain，不承担状态记账或长期结构修复。已排程 Reader Release 是本章要兑现的 timing decision：Curator 已投影时，用最短充分的直接旁白或场景表达说明。**开篇公共常识以“普通读者不用推理就能复述规则”为兑现标准**：可以用 1—3 个短说明段直接讲清，不要求先制造问题，也不能用火盆、服装、站位、专名或氛围暗示替代基础答案。若同一事实包含地点/势力/传承的价值，也保留一个最短欲望锚点；隐藏原因与未来 reveal 继续未知。Curated Context 已明确带入私人欲望且当前场景自然触发时，不把它自动净化成职责协作或成熟沟通。高价值 Asymmetry Reveal 若 Curated Context 已带入社会校准要求，Primary 要同时实现 `Behavioral Repricing + Ruler Calibration`：既让关键观察者真的换一个动作，也让最懂行者用 1—3 句说明正常值、超标点和稀有/异常意义；不要因为追求“克制”而把专业尺度删成只剩一个停顿，也不要轮流安排多人解释。Canon / Curator 已标记为未知、未解释、真假未定或原因未明的过去事实继续保持未知；除非 Director Contract 明确规定本章新成立的事实，Primary 只能创造当前场景实现细节，不得把 plausible explanation 写成 retrospective canon。对白同样不能成为补 Canon 的旁路。

### Authority Reviser

固定使用 **GPT-5.6 Luna high**。Primary Draft 是唯一待修订正文底稿；Reviser 不是第二个 Director / Writer，而是 **Preservation-First Authority Recovery**：先假设已写好的正文正确，只有能指出具体失败的局部才允许修改。

它重新获得 Primary 为减负而没有直接持有的远端权威：冻结 Chapter Mission、Curator、safe `WORLD AUTHORITY`、逐条 `Reader Release`、`CHARACTER.md` 的 Frozen Power Core + Frozen Human Core、Canon Index / 上一章必要章末，以及 Primary Draft。若 Curator 选中的 Scene Skill 有经过 A/B 验证的极短 `Revision Watch`，Reviser 只额外看到这 1—2 行 failure-triggered 提醒；完整 Generation/Revision Lens 不进入。raw GBrain 固定 OFF，完整 World / Character 原文也不直接进入；所有远端输入都是确定性安全投影。

允许的修订只有三类：

- 删除/压缩反复确认、重复证明、结构分析、材料诊断、路线计算、验证/报告/登记式展开和无新选择的 Competence Filler；
- 补回 Authority / Reader Release / Curator 已批准但 Primary 漏掉的最短充分世界信息、Core Power 独有体验、Frozen Human 私人 cue 或一个有故事功能的生活细节；
- 在不改变事实的前提下，把过多 Supporting Implementation 的笔墨还给 World Entry、Rival、Relationship、Core Fantasy、Choice、Payoff 或 Consequence。

同一维度如果 Curator / Primary 与 Frozen Mission / Canon / safe World / Frozen Power / Frozen Human 冲突，以 Frozen Authority 为准，并对最终稿做语义级全章清零。修冲突段落时先逐句 salvage：本身合法、只因错误时点/因果而失效的高价值 Core Fantasy / Relationship / Desire / Payoff / Surprise / Social Repricing 句移到最近合法位置；salvage 不保护周围报告、登记、路线或普通实施。

Reader Release 的“存在”与“清楚兑现”分开判断：开篇公共常识若只通过道具/环境暗示存在，普通读者仍需自己推理出规则，Reviser 应在不改变剧情的前提下补最小直接说明；生活细节可以保留，但不能冒充 Orientation 已完成。本章若 Direct Result / State Change 已明确跨过前文介绍过的公开力量/身份档位，而 Primary 只留下“凝影了 / 通过了 / 被记名”等现象或本地术语，Reviser 在结果处补一次最短的新档位直称。

不得改变主要事件顺序、人物决定、胜负、资源得失、伤势、身份结果、Direct Result、State Change、Ending 或未知事实边界；没有明确问题的句段默认逐字保留。删除一段前必须先确认不会同时删掉新的 `State Change / Social Repricing / Reward / Relationship Change / New Desire / Next Opportunity`。

在 `curator_primary` 中 Primary 不能直接成为 `final_source`。Authority Reviser 完成后才可采用为正式正文；如果后续显式 repair 运行 Integrator，则 Integrator 可替代它。State Extraction 后端会重新读取 Run Ledger 的最终来源，页面里的 Primary 文本不能旁路进入 State。

### Optional Repair

`opening / dialogue / action / emotion` Specialist 与 Integrator 只在作者显式开启 repair 时使用，而且必须发生在 Authority Reviser 之后。Specialist 读取 Authority Revision 的相关局部；Integrator 也以 Authority Revision 为底稿，可以全部拒绝。若没有有效 Patch，`final_source` 继续保持 Authority Reviser。

### State Extraction

只从最终正式正文提取已经发生的事实，不读取 GBrain，不把计划、推测或参考机制写进 Canon。社会反应本身不自动进入长期状态：只有某个观察者/圈层因直接目击、专业推断或二手来源形成了会继续改变后续选择的稳定知识/误解，并已经导致关系、资源、敌意、战术、准入或信息流变化时，才把“谁知道/相信什么、仍不知道什么、因此持续怎么做”写入普通 Canon；一次性惊讶或短期 Ruler Calibration 不建额外 Disclosure Ledger。默认 `curator_primary` 下必须从 Run Ledger 的 `authority_reviser` / `integrator` `final_source` 重新读取正文；Primary Draft 不得直接进入 State。

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

## Run Ledger

每章目录：`books/<book_id>/runs/chapter-NNNN/`。

Ledger 记录固定节点的 Prompt、Response、状态与最终采用来源，不是后台调度器或通用 Workflow Engine。节点状态只使用：

`pending / completed / failed / skipped / stale / adopted`

底层节点仍可记录：

`director → curator → primary → authority_reviser → opening / dialogue / action / emotion → integrator → state_delta`

在默认 `curator_primary` 中，`authority_reviser` 必跑，Specialist 与 Integrator 默认 `skipped`；需要 repair 时只能在 Reviser 完成后显式激活。历史已完成 Run 不被新节点追溯改写；新/未完成 production Run 必须经过 Reviser。失败节点重试复用已保存 Prompt，不重跑无关上游；上游变化只让真实依赖的下游变为 `stale`。

## 实现边界

- `chapter_context.py`：确定性上下文投影与压缩。
- `hybrid_runtime.py`：Curator / Primary / Authority Reviser / Specialist 的局部文本投影，不调用模型。
- `run_ledger.py`：节点文件状态与恢复，不写小说事实。
- `storage.py`：显式保存与 State Delta 应用边界。

不要为章节 Runtime 引入数据库、队列、事件总线、通用 DAG、自动重试框架或新的全量上下文系统。运行时目标是：**少节点、窄上下文、事实与计划分离、失败可恢复。**
