---
name: reanalyze-book-profile
description: 基于冻结 profile context 生成书籍画像变更 Proposal；不直接改变 Effective Profile。
---

# Reanalyze Book Profile

前置条件：`novel workflow start` 已成功返回 `status=RUNNING` 且
`executor_skill=reanalyze-book-profile`。只读取 `task.json` 列出的
`profile_context.json`，按冻结的九维画像合同生成 additions、modifications、removals、
reason、evidence 和 confidence。

结果只能是 Proposal；不得重新领取 handoff、调用 protocol Skill、重算冻结 hash、读取
无关 Atlas/Metric 或自行判断 task type，也不得直接写 Effective Profile、Canon 或正文。
完成后写 result JSON 到 `artifact_target`，由 `novel workflow complete` 统一执行通用
结果、artifact、漂移、状态和事件校验。
