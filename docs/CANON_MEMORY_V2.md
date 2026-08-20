# Canon Memory v2

章节状态区使用五个语义层：`ACTIVE SCENE STATE`、`PERSISTENT CANON`、`RECENT SUMMARIES`、`OPEN PROMISES`、`AUTHOR NOTES`。

`ACTIVE SCENE STATE` 记录下一章马上需要的地点、人物、伤势、物品、追兵、倒计时和直接目标；下一章可以整体替换。`PERSISTENT CANON` 只保留长期能力、限制、关系阶段、持久资源、身份、确认知识、长期伤势和敌我状态。旧书只有旧“当前状态”时，读取投影把它作为旧 Persistent Canon，不建立迁移框架。

State Delta v2 只输出：

- `# State Delta Audit`
- `# Proposed Active Scene State`
- `# Proposed Persistent Canon`
- `# Proposed Chapter Summary`
- `# Proposed Open Promises`

代码逐字保留旧 `AUTHOR NOTES`，模型返回 AUTHOR NOTES 标题、缺少任一标题或内容为空时拒绝应用，但不阻止正式章节保存。应用动作只在作者显式批准后更新 BOOK 状态区，不改 BOOK Contract、计划或正文。
