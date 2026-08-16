# Task Plan: Continuation Expansion + GBrain Operational Wiring v1

## Goal

在 `workflow-gate-simplification-v1` 最新提交之上，复核并闭合引用审计指出的
Revision GBrain selector 默认工作流缺口；只修复真实可复现的 CI 问题，不把过期审计
结果当成当前事实。

## Scope

- S1：Reference Corpus 为 `ENABLED` 且存在 selected cards 时，Revision strategy
  selection 必须在 draft task 前完成 import；无卡、不可用、zero-result 仍允许 fallback。
- S2：selector 使用真正的 unit-scoped scene context，不混入 campaign-global 聚合值。
- 对真实 CI failure 做根因修复；若当前远端已绿，记录该结论，不制造无关改动。
- 为以上行为补最小回归测试和审计记录。

## Explicit non-goals

- 不修改 `reference-corpus-semantic-v1` 或 `workflow-gate-simplification-v1`。
- 不 force-push，不清理用户已有工作树，不修改 `book/` 或 Canon。
- 不新增 Vector DB、Embedding、Taste Brain、Trajectory Engine、硬字数门禁、迁移框架或兼容层。
- 不把 GBrain 故障变成写作硬阻断。

## Phases

### Phase 1: Discovery and baseline

- [x] 读取引用对话最后审计回复
- [x] fetch、确认基线 branch/commit/远端 Actions
- [x] 创建并推送安全分支
- [x] 记录 dirty worktree 和上一轮计划
- [x] 复核 S1/S2 真实代码路径
- [x] 复现或排除审计列出的 CI failures

### Phase 2: Minimal implementation

- [x] 确认 S1 必要 selection gate 与 fallback 边界已存在
- [x] 确认 S2 unit-scoped selector context 已存在
- [x] 保留现有 provenance、snapshot、machine seal 和 hard authority

### Phase 3: Verification

- [x] 运行最小 S1/S2 回归测试
- [x] 由 clean checkout GitHub Actions 运行 pytest、ruff、mypy、compileall、JS syntax
- [x] push 后确认 GitHub Actions clean checkout 结果

### Phase 4: Delivery

- [ ] 只提交本轮拥有的文件/行
- [x] 更新 re-audit 计划与证据文件
- [ ] commit、push、报告 source/new branch、HEAD、origin 和 working tree

## Result

本轮没有生产代码差异：S1/S2 已由基线提交实现，当前 clean checkout Actions 已全绿。

## Acceptance

1. `ENABLED + selected_card_count > 0 + no imported selection` 明确拒绝 draft task。
2. `DISABLED/UNAVAILABLE/CORRUPT/ZERO_RESULTS/selected_card_count == 0` 允许既有 no-card fallback。
3. 不同 Unit 的 selector 输入不再共享 campaign-level scene function aggregate。
4. 当前真实 CI 失败全部有明确 PASS/BASELINE 结论，不能以 dirty-tree 测试代替 clean checkout 证据。
5. 既有 Reference Corpus machine seal、provenance isolation、bounded selector 和 soft-fail 测试继续通过。
