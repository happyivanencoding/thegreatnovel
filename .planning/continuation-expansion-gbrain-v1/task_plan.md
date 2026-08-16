# Task Plan: Continuation Expansion + GBrain Operational Wiring v1

> 本文件前一版记录了错误的 docs-only 复核结论；那一版只作为历史记录保留。

## Goal

在现有 `continuation-expansion-gbrain-v1` 分支上真正实现 Continuation Expansion +
GBrain Operational Wiring v1。目标是让正常逐章续写拥有较轻的创作输入、可诊断的
章节展开与体验重复、以及可审计且带确定性 fallback 的普通续写 GBrain 选择链路；
同时修复当前 clean-checkout 能复现的 CI 根因。

## Historical scope (previous attempt)

- S1：Reference Corpus 为 `ENABLED` 且存在 selected cards 时，Revision strategy
  selection 必须在 draft task 前完成 import；无卡、不可用、zero-result 仍允许 fallback。
- S2：selector 使用真正的 unit-scoped scene context，不混入 campaign-global 聚合值。
- 对真实 CI failure 做根因修复；若当前远端已绿，记录该结论，不制造无关改动。
- 为以上行为补最小回归测试和审计记录。

该范围没有满足当前目标，不能作为本轮完成条件。

## Current implementation scope

- `DraftCreativeOutput -> compile_draft_output -> DraftOutput`，由 Python 编译内部
  evidence / fit / trace 字段。
- `ChapterRealizationBrief`、自适应软篇幅与 `SCENE_REALIZATION_THIN` warning/repair
  trigger；repair 只允许 realization-only 表达修复，不增加固定字数 hard gate。
- `ChapterExperienceSignature` 的最近窗口、软体验目标与同构体验提示。
- 普通 continuation 的 deterministic GBrain fallback tiers、bounded selector、
  `PlanningReferenceStrategy` 及 Candidate -> Contract -> Draft provenance。
- 从 Boundary / Directive / Reveal / Style 派生 Candidate 防守字段；不让 LLM 回填
  系统内部约束，`required_cost` 不再默认必填。
- 同步 `continue-novel`、`novel-prose-realization`、`process-novel-handoff` Skill
  的真实合同。
- 修复 clean-checkout 中可复现的 materialization owner、RealizedKernelTrace contract
  mismatch 和 Original semantic Skill contract 问题。
- 保持 book/、Canon approval、Reference-only isolation、machine seal、既有 Revision
  selector 和 fallback 语义不变。

## Explicit non-goals

- 不修改 `reference-corpus-semantic-v1` 或 `workflow-gate-simplification-v1`。
- 不 force-push，不清理用户已有工作树，不修改 `book/` 或 Canon。
- 不新增 Vector DB、Embedding、Taste Brain、Trajectory Engine、硬字数门禁、迁移框架或兼容层。
- 不把 GBrain 故障变成写作硬阻断。

## Historical phases (previous attempt)

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

- [x] 只提交本轮拥有的文件/行
- [x] 更新 re-audit 计划与证据文件
- [x] commit、push、报告 source/new branch、HEAD、origin 和 working tree

**Historical status:** completed

## Reopened implementation phases

### Phase 5: Current codepath inventory

- [x] 读取当前 continuation candidate/contract/draft、reference query、validators 和
  handoff 的实际调用链。
- [x] 为每一项拟运行的检查写明具体失败与后续动作。
- [x] 记录 dirty worktree 所有权，避免混入用户已有修改。

### Phase 6: Production implementation

- [x] Draft creative schema/compiler/evidence/realization brief。
- [x] Experience Signature 与 candidate/contract soft experience guidance。
- [x] Continuation GBrain fallback tiers、selector、provenance、book-local usage。
- [x] Skill contracts 与 handoff/web integration。
- [x] 五个 clean-checkout failure 的根因修复保持基线既有实现，不重复造改动。

### Phase 7: Verification and delivery

- [x] 先跑各模块 targeted tests，再跑完整 pytest、ruff、mypy、compileall 和相关 Web
  检查。
- [ ] clean committed tree 上运行 GitHub Actions；失败则读取真实日志并修根因。
- [x] 只提交本轮拥有的生产代码、测试、Skill、审计/计划更新；不得提交现有 dirty
  文件或运行产物。
- [ ] 只有所有 required acceptance 通过后，才报告可进入十章实验。

**Current status:** in_progress

## Result

上一轮没有生产代码差异；本轮必须产生对应生产代码和测试差异。不得以文档-only 或
旧 CI 绿色作为完成结论。

## Historical acceptance

1. `ENABLED + selected_card_count > 0 + no imported selection` 明确拒绝 draft task。
2. `DISABLED/UNAVAILABLE/CORRUPT/ZERO_RESULTS/selected_card_count == 0` 允许既有 no-card fallback。
3. 不同 Unit 的 selector 输入不再共享 campaign-level scene function aggregate。
4. 当前真实 CI 失败全部有明确 PASS/BASELINE 结论，不能以 dirty-tree 测试代替 clean checkout 证据。
5. 既有 Reference Corpus machine seal、provenance isolation、bounded selector 和 soft-fail 测试继续通过。

## Current acceptance

6. Draft task 暴露 `DraftCreativeOutput`，模型不再提交内部 evidence/fit/trace 字段；
   Python 能从正文与合同编译这些字段。
7. Draft task 包含 `ChapterRealizationBrief`，短薄诊断只能 warning/repair trigger，
   不形成固定字数 hard gate。
8. 最近章节体验签名进入下一章规划，重复体验只产生 soft guidance。
9. 普通 continuation 通过 bounded GBrain selector 生成 strategy，并把 selection
   provenance 自动贯穿 Candidate -> Contract -> Draft；无卡/不可用保持 fallback。
10. 当前 clean-checkout 的 materialization owner、RealizedKernelTrace、Original Skill
    contract 测试通过。
