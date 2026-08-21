# candidate-b Chapter 2 selection mismatch

本章 Director 响应没有 `## 专项建议`，实验辅助记录的 declared selection 是空；但 `dialogue_response.md` 与 `action_response.md` 已在本轮 Ledger 同步前由并行工作写入，随后 Integrator 也已存在。两份 Specialist 建议各自只执行一次，Integrator 正式正文与 Primary Draft 完全一致。

因此本章不删除或伪造这些真实 artifact：execution 记录同时保留 `selected_specialists=[]`、`executed_specialists=[dialogue, action]` 与 `selection_mismatch=true`，实际调用成本按 8 个节点计。该 mismatch 是并行工作证据，不能当作 clean selective 分支的选择行为。
