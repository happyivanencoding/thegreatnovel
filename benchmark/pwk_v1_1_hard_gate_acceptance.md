# PWK V1.1 Hard Gate Acceptance

日期：2026-08-12

## Authority boundary

唯一 Candidate Hard Gate 仍为 `metrics.gates.evaluate_hard_gates()`。Progression Engine 不生成第二份 GateReport；它只把 deterministic violations 编译进现有 `HardGateInput`。

`ProgressionNarrativeEngineAdapter.validate_candidate()` 已不再固定返回 `valid=true`。它调用章节锚定的 `ProgressionConsistencyValidator`，并把错误送入既有 gate compilation。

## P0 检查项

| 检查 | 生产行为 | 自动化证据 |
|---|---|---|
| Stage Transition | 只允许 topology 中合法相邻/声明转换 | illegal stage jump 被拒绝 |
| Breakthrough Gate | 资源、条件与证据必须满足 | unsatisfied gate 被拒绝 |
| Resource Gate | owned/current resource 才能支付；不存在资源被拒绝 | nonexistent resource 被拒绝 |
| Ability Provenance | 解锁/展示必须对应当前能力或可审计 introduction | future showcase、missing provenance 被拒绝 |
| Growth Cost | claimed progression 必须存在成本或合同允许的恢复章 | 无成本伪突破被拒绝；recovery chapter 合法 |
| Knowledge Boundary | 只能使用章节边界前可见知识 | future knowledge 编译进现有 knowledge violations |
| Future Leakage | 合同边界与 evidence chapter ordinal 双重过滤 | historical projection / semantic discovery anti-leak 通过 |
| Opportunity vs Owned | Opportunity 固定 `SOFT_REFERENCE`，不能支付 Resource Gate | opportunity ownership 被拒绝 |
| World Expansion | 必须匹配世界层级转换或 bridge | expansion without bridge 被拒绝 |

对应单测集中在 `tests/unit/test_progression_consistency_validator.py` 与 `tests/unit/test_progression_projections.py`。

## Verified evidence → existing systems

Hard Gate 通过后才允许：

1. verified Progress components 进入旧 Progress formula；
2. verified score overrides 进入旧 Candidate Score；
3. verified Debt/Resource/Payoff 输入进入旧 formulas；
4. verified Genre/Progression evidence进入既有 Innovation Reward。

因此不存在“Kernel 另算一份分数，再与旧分数并列”的路径。

## Live negative boundaries

Live B 选中案声明一个“高阶路线方位”世界扩张影响。Python 将其降级为铺垫并输出 warning；Verified World Expansion 为空。Chapter Contract 的 `kernel_verification_status=PARTIAL`，没有把该声明提升成阶段变化。

Live Draft 仍显示箭匣 `21/100`，但没有发生资源变化。Expected/Realized 对账保留 `REALIZED_KERNEL_UNDERDELIVERY` warning，而不是伪造一个 resource delta 来消除 warning。

## Production prompt hygiene

对 `src/` 与 `.agents/skills/` 扫描以下词项：

- `M500`
- `林雨薇`
- `cable-survival`
- `phase4` / `phase5` / `phase6` 及分隔变体

结果：`PRODUCTION_FIXTURE_SCAN_CLEAR`。测试、benchmark 与本地书库 artifact 不属于通用生产 Prompt/Skill。
