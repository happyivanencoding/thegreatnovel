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

## Reopened audit — implementation scope correction

- 引用线程最新回复不是旧的 S1/S2 审计，而是对上一轮 docs-only 交付的否定；其核心
  指出普通 continuation 仍缺少 DraftCreativeOutput、realization brief、体验签名、
  continuation GBrain selector/fallback/provenance，以及 clean-checkout 的 5 个失败
  根因修复。
- 这些内容尚未被当前仓库证明存在；不得从 Revision 已有 selector 直接推断普通
  continuation 已经具备同等能力。
- 本轮需要先以 `rg`/测试/模型定义定位真实入口，再决定哪些提议可以用现有结构完成。
  不预先创建第二套 workflow、Vector/Embedding 或固定字数 hard gate。

## Live implementation evidence

- `DraftCreativeOutput` 只暴露正文、StateChange 和创意语义；`compile_draft_output()` 在
  Python 侧生成 normalized evidence、Character/Style soft audit、Experience Signature、
  Realized Kernel Trace 和 Draft 内部 provenance。缺少 StateChange 仍是输入错误；已有
  StateChange 的 evidence 缺失只形成 warning。
- `ChapterRealizationBrief` 使用最近章节长度生成 advisory range；`SCENE_REALIZATION_THIN`
  只记录 warning/repair trigger，不形成字数 hard gate，也不授权 Contract 外的状态变化。
- 普通 continuation 的 Reference Corpus 链路已闭合为 query diagnostics
  (`EXACT/FALLBACK/ZERO_RESULTS`) -> frozen snapshot -> bounded `PlanningReferenceStrategy`
  -> Candidate -> Contract -> Draft provenance。selector 最多选择 3 张卡；近期 10 个已校验
  Draft 的 card/solution provenance 会降低重复项优先级，无卡/禁用/损坏均保留 soft fallback。
- 最近 5 个已校验章节的 `ChapterExperienceSignature` 会进入下一次候选规划；重复体验只
  产生 soft guidance。Candidate 的内部防守字段由 Boundary/Directive/Reveal/Style 冻结输入
  编译，不再由创意 schema 回填。
- 验证证据：targeted 67 passed；全量 `pytest` 532 passed；全量 Ruff passed；mypy
  `Success: no issues found in 200 source files`；compileall passed。直接运行 mypy.exe 的
  GBK `.pth` 失败属于本机入口问题，UTF-8 `python -S -X utf8` 入口已通过同一检查。
- 工作树中的用户既有修改和运行产物仍未纳入本轮所有权；十章实验尚未启动。
