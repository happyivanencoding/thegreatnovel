# Task Plan: Workflow Gate Simplification v1

## Goal

在安全分支上系统性减少无意义的写作工作流硬门禁，同时保留 Canon、事实、身份、审批和来源完整性安全，并以测试与审计证据交付。

## Current Phase

Phase 5 — Delivery

## Phases

### Phase 1: Requirements & Discovery

- [x] 读取引用对话最后一条回复并提取范围
- [x] 读取 AGENTS.md 与 Constitution V2
- [x] 记录当前分支、远端和未提交改动
- [x] 建立完整 Gate Inventory
- **Status:** completed

### Phase 2: Architecture & Ownership

- [x] 逐项判定 KEEP_HARD / AUTO_DERIVE / NORMALIZE / DOWNGRADE_WARNING / REMOVE_REDUNDANT / MOVE_EARLIER
- [x] 冻结跨模块接口与不重叠写入所有权
- [x] 确认现有用户改动与本轮改动的边界
- **Status:** completed

### Phase 3: Implementation

- [x] 完成门禁、候选、Reveal、Handoff、Evidence、Kernel、Browser 和 runner 的最小修复
- [x] 保持 book/只读、Canon/Approval、Edition/Revision 和 Reference Corpus 边界
- **Status:** completed

### Phase 4: Testing & Verification

- [x] 运行针对性回归与集成测试
- [x] 运行 CLI/Web/Browser 可用的真实检查
- [x] 运行全量 pytest、ruff、mypy、compileall
- [x] 生成最终审计与闭环证据
- **Status:** completed

### Phase 5: Delivery

- [ ] 复核仅提交本轮拥有的文件
- [ ] commit 并 push 新分支
- [ ] 给出 source branch/commit、new branch、final commit 和 origin 状态
- [x] 明确 Reference Corpus 是否达到关闭条件；不自动启动十章实验
- **Status:** in_progress

## Key Questions

1. 每个现有阻断点究竟改变了什么安全动作，哪些只是内部字段对账或质量偏好？
2. 如何在不覆盖当前未提交用户改动的前提下完成跨模块集成？
3. 哪些状态/路径/ID 已由 handoff、数据库或 operation root 权威持有，可以自动推导？
4. 哪些软指标缺失应记录 UNKNOWN/PARTIAL/MISSING，而不是伪造或阻断？

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 在 `workflow-gate-simplification-v1` 上工作并立即推送基线 | 用户明确要求安全分支；原分支和基线保持可回退 |
| 保留当前未提交改动，不执行 reset/clean/覆盖 | 工作树含有用户已有代码、测试和实验产物，不能假定属于本轮 |
| 先盘点再改代码 | 任务明确要求完整 Gate Inventory，且跨模块共享接口需要先冻结 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| 引用线程读取结果按单项截断 | 1 | 改用 `turnLimit=1`、结构化读取并确认最新 agentMessage 的可见范围；以已读取的任务主体作为执行输入 |

## Notes

- 本轮不得修改 `book/` 原文、被冻结的 V2 十章数据或执行 Canon Commit。
- 任何新检查都必须说明检测的具体失败和失败后的不同动作。
- 子代理不得提交 Git 历史或触碰未授权文件；主 Agent 负责最终整合、staging、commit、push。
