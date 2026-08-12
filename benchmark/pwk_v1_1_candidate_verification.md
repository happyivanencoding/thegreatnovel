# PWK V1.1 Candidate Verification

日期：2026-08-12

## Declared 与 Verified

Candidate JSON 中以下字段是模型声明，不是事实：

- `reader_promise_alignment`
- `narrative_drive_alignment`
- `progression_impact`
- `resource_opportunity_impact`
- `world_expansion_impact`
- `genre_drift_diagnostic`
- `narrative_drive_drift_diagnostic`

Candidate import 会保存 declared trace，同时用 Aggregate 冻结的 `KernelPlanningContext` 编译 verified trace。未知 Promise/Drive、没有结构效果的核心兑现、伪 `CLEAR` drift、未来能力、机会冒充库存均不能以声明通过验证。

## Live B trace

选中候选：`candidate_627c9669f9e1241d0790b0ca` / `pwk-b-fog-bearing-mark`。

Python 确认：

- Primary Drive：`POWER_PROGRESSION`
- Scheduler intent：`PROGRESSION_SETUP`
- axis：`survival-cable-growth`
- delta：`ADVANCE`
- current owned resource：小型箭匣 21/100
- Opportunity：药品/静音符/Lv2 威胁线索，`SOFT_REFERENCE`
- world transition：无
- stage transition：无
- ability unlock：无
- hard gate：PASS

Python 降级：

- Candidate 声明的“高阶路线方位”只保留为 future setup；Verified World Expansion 为空。

## Chapter Contract

`contract_40141b35706e489cfe9c8041` 同时保存：

- `declared_kernel_trace`
- `verified_kernel_trace`
- `kernel_verification_status=PARTIAL`
- `scheduler_alignment`
- `chapter_intent=PROGRESSION_SETUP`

`PARTIAL` 是诚实状态：候选可以进入写作，但不能把未验证的世界扩张当成事实。

## Draft Expected vs Realized

Live Draft revision 1 因未推进合同要求的两条 Narrative Debt 而未通过 Debt Validator。系统没有自动放行。

Revision 2：`draft_8a313c3153f4b1558fe3a938`

- `RealizedKernelTrace.expected_contract_id` 精确匹配合同；
- 证据短句逐字存在于正文；
- evidence 绑定 `knowledge` / `thread` StateChange record IDs；
- Primary Intent、Reader Promises、Primary Drive、Axis、Progression Delta 与 Payoff Channel 对账；
- 未声明阶段变化、能力解锁、资源获得或世界层级变化；
- 十项 Validator 全部通过；Contract Validator 仅保留“资源保持不是资源变化”的 warning；
- semantic policy leak：CLEAR。

## 可复核 artifact

目录：`benchmark/artifacts/pwk_v1_1_live_ab/existing/variant-b/`

- `kernel-context.json`
- `candidate-task.json`
- `candidate-claims.json`
- `chapter-contract.json`
- `draft-output.json`
- `chapter-051.md`
- `validation.json`
- `handoff-result.json`
