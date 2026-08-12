---
name: hydrate-source-state
description: 从冻结章节输入提取 Source State delta；只写结构化状态，不修改正文或 Canon。
---

# Hydrate Source State

前置条件：`novel workflow start` 已成功返回 `status=RUNNING` 且
`executor_skill=hydrate-source-state`。只读取 `task.json` 列出的
`hydration_context.json`，按其冻结章节、source spans 和输出合同完成语义提取。

写出 `SourceStateHydrationResult` 所需的 result JSON；不重新领取 handoff、不调用
protocol Skill、不计算 hash、不判断 task type，也不读取无关 Atlas、Metric 或全文。
`SOURCE_VERIFIED` 必须带冻结章节内的 source span；不确定内容保留
`uncertain_findings`。不得修改 `book/`、Canon、Author Intent 或 SQLite。

完成后将 result 写到 `workflow start` 返回的 `result_target`，由
`novel workflow complete` 统一完成 Python schema、artifact、漂移、状态和事件边界。
