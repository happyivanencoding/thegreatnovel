---
name: discover-kernel-contracts
description: 在冻结章节窗口内提出 Kernel Contract Proposal；只生成作者审阅的语义提案。
---

# Discover Kernel Contracts

前置条件：`novel workflow start` 已成功返回 `status=RUNNING` 且
`executor_skill=discover-kernel-contracts`。只读取 `task.json` 列出的
`kernel_discovery_context.json` 与 `kernel_contract_proposal_schema.json`，在限定章节和
证据边界内提出 Reader Experience / Narrative Drive / Progression 等合同提案。

不得重新领取 handoff、调用 protocol Skill、重算 hash、读取无关 Atlas/Metric 或把提案
写入 Canon。输出必须保留 UNKNOWN、证据定位和作者确认边界；完成后写 result JSON 到
`result_target`，由 `novel workflow complete` 统一完成通用协议校验。
