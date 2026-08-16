# Findings: Continuation Expansion + GBrain Operational Wiring v1

## Initial evidence

- 引用线程最新可见审计提出 S1：Revision strategy selection 可被 draft-task 绕过；
  S2：selector scene context 仍含 campaign-global aggregate；并提到 5 个 CI failure。
- 当前 `workflow-gate-simplification-v1` HEAD 为 `50a2915`，远端同 SHA。
- `workflow-gate-simplification-v1` 的 GitHub Actions `quality-gates` 已成功；引用中的
  5 个 failure 可能来自旧 HEAD，必须重新定位。
- 当前工作树有任务开始前的 modified files 和 untracked artifacts，已保留。

## Live code audit

- S1 已在当前基线实现：`_revision_strategy_selection_required()` 只在
  `ENABLED + selected_card_count > 0 + bounded options 非空` 时返回 true；
  `prepare_revision_draft_task()` 检查 `strategy_selection_result.status=IMPORTED`、
  planning task id、task type 和 unit coverage，并报 `REVISION_STRATEGY_SELECTION_PENDING`。
- S2 已在当前基线实现：`_revision_strategy_selector_input()` 先按
  `unit.base_chapter_id` 过滤 target features，再由 `_unit_selector_scene_context()`
  读取 unit anchored 的 rhythm functions；不会直接复制 campaign-level scene functions。
- 现有 `tests/integration/test_revision_workflow.py` 已覆盖 S1 fallback/required、
  selector import 前拒绝 draft，以及 S2 两个 unit 的 scene/rhythm 隔离。
- 当前 `workflow-gate-simplification-v1` 的 Actions 已对 `50a2915` 通过；引用审计中的
  5 个 CI failure 属于旧快照，需以新分支 clean checkout 重跑为准。

## Verification evidence

- `test_revision_strategy_uses_frozen_cards_effective_metadata_and_real_scene_source`：PASS。
- `test_revision_strategy_selection_is_per_unit_and_bounded`：PASS。
- `test_revision_strategy_selector_input_uses_unit_local_scene_and_rhythm_functions` 与
  `test_revision_strategy_selection_requirement_keeps_soft_fail_fallback`：PASS。
- GitHub Actions `quality-gates` run `31945837568` on commit `50a2915`：PASS；Test/Lint/
  Type check/Compile Python/JavaScript syntax 全部成功。
- 因此本轮结论是“审计建议已在当前基线实现”，不是再写一套 selection gate 或第二套 selector。

## Decisions

- 先检查当前代码和 clean-branch CI，再决定是否修改；不因引用审计中的旧 SHA 直接改代码。
- 主 Agent 持有共享 handoff/revision interfaces；任何 worker 必须获得明确不重叠文件所有权。
- fallback 继续是软路径；只有“已启用且有可用卡片但 selection 未导入”才阻断 draft task。
