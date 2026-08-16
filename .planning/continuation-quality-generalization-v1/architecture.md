# Architecture Audit: Continuation Quality Generalization v1

## Intended data flow to verify against the live repository

```text
Author intent / Reader Experience
  → Candidate
  → Chapter Contract
  → prose generation
  → reader-visible semantic extraction/review
  → deterministic validation against Projection
  → author approval
  → Event Store
  → Projection
  → next planning window / experience portfolio
```

The live implementation ties the arrows to `planning/candidates.py`,
`planning/contracts.py`, `drafting/compiler.py`, `validation/validators.py`,
`workflows/approval.py`, the existing event store/projection rebuild, and the
page-native approval routes in `web/app.py`. The new layer does not create a
second workflow or persistence authority.

## Authority constraints confirmed

- The repository Constitution is the highest product specification. `AGENTS.md` and `PLAN.md` require immutable `book/`, explicit author approval, replayable Event Store/Projection state, and no duplicate Canon/workflow/database.
- `LLM at the edges; deterministic state, metrics and validation at the center; author above both` is an implementation constraint, not a suggested style.
- Type-specific pressure, growth, payoff and horizon are configuration/contract inputs. The Constitution's defaults are not permission to hard-code one genre or fixed chapter count.
- `DESIGN_VALUES.md` and `MVP_REWRITE_SPEC.md` are absent from the available repository history; the audit must not fabricate their content.

## Audit questions

### 1. Where reader-visible facts are currently lost

The old path persisted declared `StateChange` evidence but had no small,
reviewable boundary for high-value facts visible in prose. `DraftCreativeOutput`
now carries `ReaderVisibleClaim`; `drafting/compiler.py` preserves it in
`DraftOutput`, and `validate_canon` checks evidence, Projection base values,
StateChange binding, subject existence, Contract membership and materialization.

### 2. LLM semantic fields vs Python authoritative state

Creative models carry prose, claims and semantic declarations. Python compiles
deterministic measurements, contract-surface coverage, evidence locators,
usage/progression checks and publication findings; Event Store/Projection stay
authoritative for committed facts. A claim is not Canon merely because it is
present in a draft.

### 3. Character/Style measurements

The old score inputs remain only for explicitly hand-authored
`STRICT_LEGACY` fixtures. Normal `COMPILED_SOFT` output sets them empty and
reports `semantic_review_status=UNKNOWN`, deterministic counts/ratios and
contract coverage. Edge semantic findings must carry a quote; Python only
checks that the quote is in the prose.

### 4. Repetition detection

`ChapterExperienceSignature` contains structural dimensions including
opposition, subject, method, choice, cost, payoff, progression and ending
action. `build_serial_experience_portfolio` compares those dimensions and reads
history/horizons from the active settings or handoff policy; absent policy
produces UNKNOWN rather than a hidden chapter window.

### 5. Progression reuse vs upgrade

`ProgressionDelta` distinguishes REUSE/SHOWCASE from MASTERY/UPGRADE/
BREAKTHROUGH/STAGE_TRANSITION and requires before/after and reader-visible
evidence for actual growth. `validate_economy_power` also rejects an index
change without a delta and REUSE/SHOWCASE advancing the index.

### 6. Periodic usage constraints

`UsageConstraint` is parsed from existing StateChange payloads. DAILY,
COMBAT_SCENE, RESOURCE_GATED and ONE_TIME are values of the same model;
period identity, counters, resource cost and explicit reset flags are checked.
Chapter boundaries never reset a counter.

### 7. Reference Corpus adoption proof

Planning carries the frozen snapshot and selected cards as
`PlanningReferenceProvenance`. Status is separated into UNAVAILABLE,
ZERO_RESULTS, OFFERED, APPLIED, OFFERED_NOT_APPLIED and
REJECTED_DUE_TO_CONFLICT. `APPLIED` additionally requires declared structural
dimensions, a changed dimension, and evidence that points into the frozen
selected cards/solutions; no innovation reward is inferred from offering a
card.

### 8. Blocking approval paths

The blocking calls were in `web/static/original.js` and the edition activation
path. Chapter approval now uses `web/static/approval.js`; Draft Review exposes
the shared page-native button, while Original first-chapter approval calls the
same server-side `approve_draft` boundary through its existing endpoint.
Revision preparation has no separate Canon approval UI in the current web
surface. Library import/delete dialogs remain outside chapter approval scope.

### 9. Single-state/workflow repair boundary

The repair uses existing Draft/StateChange/Projection/Event Store and the
existing approval transaction. The only new persisted content is optional
contract data in existing draft/task JSON; there is no second Canon, scheduler,
workflow or database.

### 10. Cross-family coverage

The parameterized tests and configured-horizon experiment use survival/resource,
combat/cultivation and mystery/relationship data through the same claim,
usage, progression and portfolio functions.

## Candidate minimal abstractions

These are hypotheses, not implementation commitments:

- `ReaderVisibleClaim` / equivalent existing model for high-value reader-visible assertions with subject, predicate, value, temporal scope, claim kind, evidence quote, transition source and status.
- Generic usage constraint attached to an existing capability/resource/entity state rather than a daily-evolution table.
- `ProgressionDelta` / equivalent existing impact model with before/after, visible evidence, source, action/scope/reliability/cost changes and delta type.
- Extended `ChapterExperienceSignature` / portfolio using configured horizons and structural dimensions, with diagnostics that do not automatically hard-block every writing mode.
- Centralized publication-boundary vocabulary plus edge semantic audit findings.

## Non-goals

- No second Canon or database.
- No natural-language knowledge graph or regex-based complex semantic inference.
- No current-story parser or genre-specific production field.
- No fixed chapter-count rule or fixed word-count hard gate.

## 审计后的答案

1. `ReaderVisibleClaim` 放在 `DraftCreativeOutput`/`DraftOutput`，每条 claim 明确 subject/predicate/value 或 before/after/evidence_quote；`compile_draft_output` 是创意边缘到内部 Draft 的唯一编译点，`validate_canon` 再以 Projection/Contract/StateChange 核对；它不自动成为 Canon。
2. UsageConstraint 放在 resource/capability StateChange payload；验证器读取当前 Projection 与同章变化，确认 period、limit、remaining、reset_condition。复位必须有显式 reset action/condition，不按 chapter ordinal 自动清零。
3. ProgressionDelta 放在 `ProgressionImpact.deltas`，包含 before/after、kind、reader-visible delta、opened action/cost/reliability/scope；旧 `progression_delta_type` 仍作为已有 contracts 的序列化字段，不再独自承担升级判断。
4. compiled-soft 的人物/文风结果改为 `UNKNOWN` 语义审阅状态 + deterministic measurements/contract coverage；硬边界只保留明确 violation 与 Canon/Timeline/Knowledge/Resource 等可验证冲突。
5. Serial Experience Portfolio 从已验证 draft signatures 聚合结构维度，并使用 Settings 的 history/horizon policy；候选重复是结构相似诊断，比较 opposition/subject/choice/cost/payoff/reader-visible/progression，不靠字符串改名逃逸。
6. Reference status 由 frozen snapshot 产生 `OFFERED`，只有候选显式引用、合法结构维度、结构变化、非空 summary、证据且 evidence 指向冻结卡片/solution 才是 `APPLIED`；无命中/冲突如实记录，不把“有卡”当作“已用”。
7. `approve_draft` 继续是唯一发布 boundary。`approval.js` 只负责一次作者点击、CSRF header、inline feedback；服务端重新执行 stale、validation bundle、transaction 和 Canon 边界。Original first-chapter endpoint 只做其特有 registry/state 更新，再委托同一 boundary。
8. realization baseline 只提供表达建议，`_healthy_realization_lengths` 只读取已验证/已批准/已提交且 CLEAR 或明确接受的章节；thin、summary-like、underspecified 不会拉低历史基线。无 baseline 时状态为 `UNKNOWN`，Contract 缺少不可逆变化/结尾状态/commit update 时返回 `CONTRACT_REALIZATION_UNDERSPECIFIED`，不得用固定全局字数硬门。
9. 没有为每种 genre 建分支算法；三类 fixture 只换 generic subject/resource/relationship payload，验证同一 validator/overlap/usage engine。
10. 若实现需要新表、自动语义评分或从正文猜复杂事实，均视为越过当前范围，退回声明 + 证据 + 现有事件边界。
