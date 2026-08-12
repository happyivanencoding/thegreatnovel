# PWK V1.1 Quantitative Kernel Integration

日期：2026-08-12
分支：`progression-webnovel-kernel-v1`
生产接线提交：`5a7271f`

## 结论

PWK V1.1 已将 Progression Kernel 接入既有 Planning、Hard Gate、Metrics、Candidate Score、Innovation Reward、Chapter Contract、Draft Validator 与 Approval 投影链。实现没有新建第二套 Candidate、总分、Hard Gate、Debt、Payoff 或 World State。

本报告只说明代码与自动化生产链已接通。Live B 草稿尚未获得作者明确的“批准写入正史”，因此本轮整体状态仍为 `PRODUCTION WIRING INCOMPLETE`。

## Effective Contract → Planning Aggregate

`PlanningAggregate.kernel_context_json` 持久化 typed `KernelPlanningContext`。目标章边界选择发生在 Aggregate 构建时，而不是让 Candidate 临时读取最新状态。

Live B 的 Aggregate：

- aggregate：`planning-aggregate_667057dec2c81abe70d4c518`
- status：`ACTIVE`
- context chapter：50
- target chapter：51
- frozen contract references：7
- P0 六类：Reader Experience、Narrative Drive、Genre、Progression、World Expansion、Payoff Channel
- 同时冻结 Market Category，但它不进入 Scheduler authority
- coverage：8 known、0 partial、0 unknown、0 blocking gap

合同任一确认或 supersede 会使旧 Aggregate、Candidate、Chapter Contract 与 READY Handoff 失效；Legacy Book 的 `kernel_context=None` 继续走旧工作流。

## Candidate Handoff

正式 Continuation / PLAN_ONLY Handoff `handoff_7d20458a61b76806c794921f` 生成：

- task：`plan_ffe0e06d113a1f02f1156d17`
- Boundary：`boundary_0f25cf85ceb7c5870b105c23`
- Frozen Effective Contracts
- chapter-pinned state（chapter 50 → target 51）
- current resources / capabilities / knowledge
- Opportunity Surface（soft reference，不拥有资源）
- Narrative Portfolio / Debt
- Anticipation Surface
- Scheduler Recommendation：`PROGRESSION_SETUP`

正式 handoff task 现在也保存 `boundary_packet_id`、`boundary_path` 与 `narrative_portfolio_snapshot`，Chapter Contract 不再依赖 direct-plan 专属路径。

## Verified quantitative compilation

LLM 的 Reader/Drive/Progression/Resource/World/Genre/Drive Drift 字段保留为 `declared`。`KernelEvidenceCompiler` 根据冻结合同和章节状态产生 `verified`、`differences`、`warnings` 与 completeness，再接入旧数值系统：

- `HardGateInput`：Canon、Timeline、Knowledge、Causal Source、Cooldown、Capability、Author Constraint；
- Progress：仍调用 `metrics.formulas.progress()`；
- Candidate Score：仍调用既有 `candidate_score()`；
- Narrative Debt：仍调用既有 `narrative_debt()`；
- Resource Pressure：仍调用既有公式；
- Payoff：仍调用既有 `payoff_score()`；
- Innovation Reward：只在 Hard Gate 后使用 verified soft inputs。

UNKNOWN 保持 UNKNOWN，不偷换为 0；自报值不再能覆盖 verified 值。

## Live B quantitative result

三候选均经 Python 重算并通过既有 Hard Gate：

| Candidate | Base score | Final score | Gate | Selection |
|---|---:|---:|---|---|
| `pwk-b-fog-bearing-mark` | 68.6765 | 73.0265 | PASS | SELECTED |
| `pwk-b-controlled-arrow-test` | 66.2629 | 70.6129 | PASS | NOT_SELECTED |
| `pwk-b-conditional-medical-deal` | 65.3153 | 69.6653 | PASS | NOT_SELECTED |

结构差异由 Python 重算，三案两两差异均为 9 个结构维度。选中项 `candidate_627c9669f9e1241d0790b0ca` 生成 `contract_40141b35706e489cfe9c8041`。

## 自动化门禁

- Unit：145 passed
- Integration：196 passed
- Total：341 passed
- Ruff：pass
- mypy：184 source files pass
- compileall：pass
- workbench.js `node --check`：pass
- `novel web doctor`：pass
- production fixture scan：clear

关键回归：

- `test_planning_aggregate_freezes_chapter_aware_kernel_context`
- `test_effective_kernel_candidate_claims_are_verified_before_contract`
- `test_verified_kernel_evidence_feeds_existing_metrics_and_score_inputs`
- `test_verified_kernel_trace_closes_through_approval_and_next_state`
- `test_progression_validator_rejects_fake_breakthrough_and_opportunity_ownership`
- `test_progression_workspace_reuses_historical_world_state_without_future_leak`
