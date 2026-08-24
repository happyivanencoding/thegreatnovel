# Chapter Runtime and State

## 定位

章节 Runtime 只负责执行已经批准的故事，不重新设计长期主线。当前默认模式是 `curator_primary`：

`Director → Context Curator → Primary Writer → State Extraction`

Specialist / Integrator 不在默认链；只有作者明确启动局部 repair 时才临时进入。`single`、`hybrid_selective`、`hybrid_full` 仅保留兼容与专项实验用途。

章节 Runtime 默认不直接读取 raw GBrain。GBrain 对章节层的影响只通过已批准的 Story Program / Outline，以及离线蒸馏后的 Scene Skills 间接进入。

## 节点职责

### Director

只根据当前剧情块、当前章计划、压缩成长信息、Canon Index、最近摘要、章末衔接和作者意图生成八字段事件合同。它决定 WHAT，不提供正文句式，不重做 World / Story Program / Outline。长期旧线回流时仍保持八字段，不新增 schema；但 `直接结果 / 状态变化 / 结尾推动力` 必须具体写清本章新成立的事实，或明确过去原因仍未解决，不能把“真相揭露到哪一步”留给 Primary 自行决定。

### Context Curator

从确定性 Index-first 预取中筛选 Writer 真正需要的信息，压缩 BOOK Contract、Canon、计划、Prose Profile、Open Promises 与 Scene Skills。它不补读全库、不重新规划、不把 Planning Language 改写成正文。

Curator 返回后，runtime 还会做一次**不调用模型的 unresolved fact projection**：从 `Curator Audit`、`Relevant Open Promises`、明确未解的 World Rules 与 `Payoff and Promise Window` 中抽取约束，形成紧贴 Chapter Mission 的 `UNRESOLVED FACT BOUNDARY`。这不是新节点、Reviewer、RAG 或 Hard Gate；它只把 Curator 已经识别出的“仍未知 / 未兑现”提高到 Primary 的高显著事实边界，避免长篇时被埋在较长 Curated Context 中。

### Primary Writer

只写正式正文。输入以 Director Contract + `UNRESOLVED FACT BOUNDARY` + Curated Context + 必要连续性为主；不直接读取 raw GBrain，不承担状态记账或长期结构修复。Canon / Curator 已标记为未知、未解释、真假未定或原因未明的过去事实继续保持未知；除非 Director Contract 明确规定本章新成立的事实，Primary 只能创造当前场景实现细节，不得把 plausible explanation 写成 retrospective canon。对白同样不能成为补 Canon 的旁路。

### Optional Repair

`opening / dialogue / action / emotion` Specialist 与 Integrator 只在作者显式开启 repair 时使用。Specialist 最多给局部 Patch；Integrator 以 Primary Draft 为唯一底稿，可以全部拒绝。若没有有效 Patch，Primary 直接保留。

### State Extraction

只从正式正文提取已经发生的事实，不读取 GBrain，不把计划、推测或参考机制写进 Canon。

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

State Delta 不改 BOOK Contract、计划或正文；只有作者显式批准后才应用状态更新。

## Run Ledger

每章目录：`books/<book_id>/runs/chapter-NNNN/`。

Ledger 记录固定节点的 Prompt、Response、状态与最终采用来源，不是后台调度器或通用 Workflow Engine。节点状态只使用：

`pending / completed / failed / skipped / stale / adopted`

底层节点仍可记录：

`director → curator → primary → opening / dialogue / action / emotion → integrator → state_delta`

在默认 `curator_primary` 中，Specialist 与 Integrator 默认 `skipped`；需要 repair 时再显式激活。失败节点重试复用已保存 Prompt，不重跑无关上游；上游变化只让真实依赖的下游变为 `stale`。

## 实现边界

- `chapter_context.py`：确定性上下文投影与压缩。
- `hybrid_runtime.py`：Curator / Primary / Specialist 的局部文本投影，不调用模型。
- `run_ledger.py`：节点文件状态与恢复，不写小说事实。
- `storage.py`：显式保存与 State Delta 应用边界。

不要为章节 Runtime 引入数据库、队列、事件总线、通用 DAG、自动重试框架或新的全量上下文系统。运行时目标是：**少节点、窄上下文、事实与计划分离、失败可恢复。**
