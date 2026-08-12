# PWK V1.1 生产接线审计

审计日期：2026-08-12  
审计分支：`progression-webnovel-kernel-v1`  
审计时基线：`a9945fb`；`origin/main` 只多一次 README 文档更新。该 README 内容已以独立 feature 提交保留，未合并 main，未重写 feature 历史。

## 1. 审计结论

PWK V1 的数据模型、作者确认生命周期、章节投影、专用 Engine Adapter、通用 Scheduler 和作者界面已经存在，但它们还没有形成完整的生产闭环。核心断点是：

1. Planning Aggregate 冻结了 Metrics、Profile、Author Control、Truth/Reveal、Rhythm 与 Atlas 引用，但没有 typed `KernelPlanningContext`。
2. PLAN_ONLY Candidate Handoff 会另行写出 Chapter World State，但没有把已生效合同、Progression State、Anticipation 和 Scheduler 作为同一份冻结输入传递。
3. Candidate 的 `gate_input`、大部分 `score_inputs`、Progress 六分量、Reader/Drive/Progression/World/Payoff/Drift 影响都是 LLM declared claims。
4. Python 只重算结构差异、用候选自报六分量调用旧 `progress()`、用候选自报 gate 调用旧 Hard Gate，并重算旧 Candidate Score / Innovation Reward；它还没有从冻结 Kernel Context 编译证据。
5. Progression Adapter 的 `validate_candidate()` 固定 `valid=True`。
6. Chapter Contract 保存 Candidate 自报影响，Draft 没有 `RealizedKernelTrace`，现有十项 Validator 没有 Expected/Realized Kernel 对照。
7. Approval 会通过现有 State Delta / Canon Event 更新 World State，但没有显式完成 Planning Aggregate 失效、Progression Debt / Anticipation 重投影的章后闭环。
8. Existing Novel Discovery 只看最新 Chapter World State 的集合是否非空，属于词法/结构 fallback，还没有受控语义 handoff。
9. 通用 PLAN_ONLY Prompt 含 `M500`、`林雨薇` 专属测试实体，是确认的生产污染。

因此 V1.1 应做“编译与接线”，不是再造一套评分、Hard Gate、Debt、Payoff、World State 或 Scheduler。

## 2. 接线状态矩阵

| 能力 | 当前状态 | 证据 | V1.1 缺口 |
|---|---|---|---|
| Effective Contract 版本生命周期 | 已经生产接通 | `progression/service.py:97-292` | 按目标章边界选择后冻结到 Aggregate |
| Contract 章节边界 | 投影中已接通 | `progression/projections.py:98-102,208-212` | Aggregate 尚未消费相同边界规则 |
| Planning Aggregate | 已有生产生命周期，Kernel 仅模型未接入 | `planning/aggregates.py:20-74,251-449` | 新增 typed `kernel_context`，不放进 `author_policy` 通用 dict |
| Profile / Author Control / Truth / Reveal 冻结 | 已经生产接通 | `planning/aggregates.py:281-314` | 纳入 `KernelPlanningContext.author_state` 引用 |
| Metrics / Rhythm / Atlas 引用 | 已经生产接通 | `planning/aggregates.py:315-402` | 保留现有 authority，Kernel 只编译输入 |
| Candidate Handoff 的 World State | 已经生产接通 | `planning/candidates.py:735-810` | 目前与 Aggregate 分开读取，需共享冻结 Kernel Context |
| Effective Kernel Contracts 进 Candidate Handoff | 仅通过完整 World State 间接可见，未正式冻结 | task metadata 只有 author/profile/truth/innovation/metric；`world_state_context.json` 间接含 progression workspace | 写入 typed machine-readable context 与 author-readable prompt |
| Universal Scheduler 进正式 Candidate | 仅有模型与单元测试 | `progression/scheduler.py`、`tests/unit/test_progression_scheduler.py` | 在 Aggregate 构建时产生并冻结 recommendation |
| Candidate ProgressPreview | 模型已有，输入仍是自报 | `planning/models.py:131-160,379`、`planning/candidates.py:985-995` | Python 从 verified evidence 生成六分量 |
| Candidate Hard Gate | 旧引擎生产接通，Kernel Gate 未编译 | `metrics/gates.py:8-63`、`planning/candidates.py:967-976` | 编译 Stage/Gate/Resource/Ability/World/Core Promise 违规到现有 violations |
| Candidate Score | 旧公式生产接通，输入多数自报 | `planning/models.py:77-90`、`planning/candidates.py:982-1008` | 用 verified compilation 替换自报输入，不改公式与权重 |
| Innovation Reward | 已经由 Python 重算 | `planning/candidates.py:1010-1018` | Genre/Progression soft reward 只消费 verified evidence |
| Progression Adapter validation | 仅有接口 | `serial_kernel/engines.py:197-204` | 实现真实 Progression Consistency Validator |
| Narrative Debt | 旧公式已复用 | `metrics/formulas.py:65`、`progression/debt.py:45` | 统一从 verified drive/engine/type 编译输入，不新增账本 |
| Payoff | 旧公式已存在 | `metrics/formulas.py:176`、`metrics/service.py:1113` | Payoff Channel Profile 决定证据适配，不更改基础公式 |
| Resource Pressure | 旧公式已存在 | `metrics/formulas.py:218-239`、`metrics/service.py:1133` | 编译 owned/opportunity/unknown/forward 分层证据 |
| Genre / Drive Drift | 模型与 UI 已有，Candidate 值是自报 | `planning/models.py:387-388`、`serial_kernel/diagnostics.py` | import 时使用 effective contract + verified impact 重算 |
| Chapter Contract Kernel 数据 | 保存 declared 影响 | `planning/models.py:461-475`、`planning/contracts.py` | 同时保存 declared/verified/differences/scheduler trace |
| Draft Realized Trace | 尚未接通 | `contracts/draft.py:47-69` 无 Kernel Trace | 新增结构化 trace 并在 import/validate 复核 |
| Draft 十项 Validator | 已经生产接通 | `validation/service.py:30-162`、`validation/validators.py` | 扩展现有 Economy/Power、Contract、Debt、Payoff 等，不增第十一套总 Validator |
| Approval / Canon / World State | 已经生产接通 | `workflows/approval.py:200-670` | approval 后使旧 Aggregate 失效，下章重建 Kernel 派生层 |
| Existing Novel Discovery | 仅有 lexical/structural fallback | `progression/inference.py:63-296` | 增受控语义 handoff，fallback 显式降级 |
| Workbench 成长/候选页 | 已有 UI | `web/templates/workbench_progression_workspace.html`、`workbench.html` | 区分 AI 声明/系统验证/未确认/冲突 |
| GitHub CI | 尚未接通 | 审计时无 `.github/workflows` | 新增轻量 pytest/ruff/mypy/node-check |

## 3. Effective Contract 存储与版本生命周期

`progression_contract_versions` 是 Reader、Market、Drive、Genre、Progression、World Expansion 与 Payoff Channel 的统一版本表。`create_contract_proposal()` 禁止 Proposal 直接 EFFECTIVE；`confirm_contract()` 只在作者确认时写 `effective_from_boundary`，并将旧同类合同标记 SUPERSEDED。

已有优点：

- 统一 contract record ID、type、version、status 和 boundary；
- Proposal 不会自动生效；
- 章节 Progression Projection 已会过滤尚未到边界的 Effective Contract。

缺口：`effective_contract_records()` 只按 status 返回最新有效记录，Planning Aggregate 目前根本没有调用它，也没有为 target chapter 编译合同快照。`confirm_contract()` 也没有使旧 Planning Aggregate / Candidate Handoff 失效，因此合同边界发生变化后，旧任务仍可能保持 ACTIVE。

## 4. Planning Aggregate 当前真正冻结的内容

`PlanningMetricBundle` 当前是引用型快照，包含：

- edition/recent chapter/window/promise/thread metric run IDs；
- author policy；
- metrics registry/config/projection 现有一致性引用；
- rhythm snapshot；
- Atlas / Horizon 引用。

`author_policy` 中又冻结：

- active author tasks/intents；
- effective nine-dimension profile；
- truth/reveal context。

它尚未冻结：

- target chapter ID / ordinal；
- Effective Kernel Contract records 与 payload；
- chapter-pinned Progression State；
- World Expansion / Opportunity / Resource / Capability / Knowledge 派生层；
- Anticipation / Progression Debt；
- Universal Scheduler Recommendation；
- Proposal-only context 与 production context 的类型区分。

V1.1 应在 Aggregate 上加 typed `KernelPlanningContext | None`。Legacy Book 使用 `None`；Proposal 只进 `proposal_context`，不进正式评分和 Hard Gate。

## 5. Candidate Handoff 当前实际发送的内容

### CLI `plan-next`

`planning/candidates.py:489-625` 把 Boundary、Planning Aggregate、三条线程、legacy `metric_results`、Runtime Context、Innovation Control 和 Narrative Portfolio 写入任务。Prompt 另行展示 Author Control、Profile、Truth/Reveal、Rhythm 与 Hook diagnostics。

### Workbench PLAN_ONLY

`planning/candidates.py:690-810` 会检查 Aggregate 生命周期，从 handoff 取 chapter ID，重新调用 `build_story_game_state()` 并写 `world_state_context.json`。

Effective Contract、Progression State、Opportunity 与 Anticipation 会通过完整 World State 的 progression workspace 间接出现，但没有作为正式、窄化、typed 的任务输入冻结；Scheduler Recommendation 完全没有进入生产任务。世界状态又是任务准备时另行查询，没有从 Aggregate 的同一份冻结 Context 读取。

## 6. Candidate 自报与 Python 重算边界

### LLM declared claims

- `gate_input` 的 Canon/Timeline/Knowledge/Causality/Capability/Author/Style 违规；
- 十一项 `score_inputs`；
- `ProgressPreview` 六分量的 value 与 evidence；
- `reader_promise_alignment`、`narrative_drive_alignment`、`progression_impact`；
- payoff/world/resource/anticipation impact；
- genre drift/evolution diagnostics。

### Python 已重算

- 三候选之间的结构差异；
- Profile MUST/MUST_NOT 和 Truth/Reveal 冻结引用合法性；
- 用 declared ProgressPreview values 调用旧 `progress()`；
- 用 declared gate + Python 追加的 Profile/Truth 违规调用旧 `evaluate_hard_gates()`；
- 结构差异分量；
- 旧 Candidate Score；
- Innovation Reward（仅 Hard Gate 通过时）。

`ProgressPreview.metric_run_id` 虽在模型中存在，import 尚未验证它是否属于 Aggregate 冻结的真实 metric run；无 Aggregate 的 Original Genesis / legacy candidate 路径仍可生产运行，V1.1 必须保留该路径而不能伪造 Kernel Context。

### Python 尚未重算

- Reader Promise ID 是否属于 Effective Reader Contract；
- Drive 是否属于 Effective Drive Mix；
- Stage 跳转、Breakthrough Gate、Resource ownership/opportunity/forward introduction；
- Ability unlock provenance 与 Knowledge Boundary；
- World Expansion transition；
- Genre / Drive Drift；
- Debt/Payoff/Resource Pressure/Candidate Score 各分项的 Kernel evidence completeness。

## 7. Hard Gate 与旧数值系统

`metrics/gates.py` 是唯一 Candidate Hard Gate。它汇总已结构化的 violations，调用旧 Character Fit 和 Style Fit，并生成唯一 GateReport。V1.1 不应改变这个事实，而应将 Kernel violations 编译到它的现有分组，或在同一 GateReport 中增加可追溯 compilation。

唯一公式 authority 保持不变：

- Progress：`metrics/formulas.py:135`；
- Narrative Debt：`metrics/formulas.py:65`；
- Payoff：`metrics/formulas.py:176`；
- Resource Pressure / Liberation：`metrics/formulas.py:218-239`；
- Candidate Score：`metrics/formulas.py:454`。

V1.1 只新增 `KernelEvidenceCompiler`，产生这些旧公式可消费的 verified components、evidence、completeness 和 source。UNKNOWN 不得偷换成 0。

## 8. Draft / Validation / Approval 闭环

`DraftOutput` 当前包含 prose、state changes、contract evidence、knowledge claims、reveal trace、fit inputs、promise changes、structure tags 与 innovation trace，但没有 Expected/Realized Kernel Trace。

现有 Validator 已有 Canon、Timeline、Knowledge、Character、Economy/Power、Contract、Debt、Payoff、Repetition、Style 十项固定集合。V1.1 应把 Progression/Resource/Ability/Breakthrough/World/Reader/Drive/Expected-vs-Realized 检查接入其中相应的旧项，不改为并行的第二套“十项”。

Approval 已经是唯一正式状态入口：它重跑 Validation，校验 Boundary，将 Draft State Changes 转为 Canon Events，更新 Projection/Snapshot，并且只在作者精确批准语后执行。

缺口：

- Chapter Contract 没有 verified trace；
- Draft 没有 realized trace；
- Approval 后没有显式将旧 Planning Aggregate 标记 STALE；
- 下一章虽会重读 Canon Projection，但没有验收证明 Debt、Anticipation、Showcase 与 Scheduler 都来自批准后新边界。

## 9. Existing Novel Discovery

`progression/inference.py:63-296` 只读最新章 Chapter World State，然后根据 abilities/resources/threads/relationships/world entries 是否非空选择 Drive，再生成 `INFERRED_PROPOSAL`。该路径安全（不写 Canon、不自动确认），但只能定位为 `LEXICAL_FALLBACK`。

可复用的语义输入已经存在：Distillation Package、Initialization / Chapter Continuity Index、Source State、Current Boundary、Story Atlas、Author Truth、World State 与 Recent Chapters。正式语义 Discovery 应通过 Local File Handoff 产生 schema-validated Proposal Bundle，不重新全文深读，不修改 Canon。

## 10. 生产 Prompt / Skill 污染审计

确认的生产污染：

- `src/novel_authoring/planning/candidates.py:774`：通用 PLAN_ONLY prompt 硬编码 `M500 弹药`、`林雨薇合作`。

合法保留：

- `library_governance.py` 中 phase4/5/6 名称是 benchmark/demo 隔离规则，不是生成 prompt；
- `docs/audits/`、`docs/architecture/BOOK_LIBRARY.md` 中的 cable-survival 和 phase 名称是历史审计/测试记录，不作为通用生成输入；
- tests/benchmark/fixture/demo 中的具体实体合法。

修复应将通用 prompt 改为：只能使用冻结 Author Goal、World State、Resource、Relationship、Knowledge Boundary、Active Threads 和 Kernel Context 中出现的专名，并加自动扫描测试。

## 11. 复用决策

必须复用：

- `progression_contract_versions` 和现有 Contract lifecycle；
- `build_story_game_state()` 作为章节状态唯一入口；
- `build_progression_workspace_from_world_state()` 中的投影构件，提取成无 UI 依赖的纯 Context builder；
- 现有 `PlanningAggregate` 生命周期；
- 现有 CandidateProposal / ChapterContract / DraftOutput / Approval；
- `evaluate_hard_gates()` 和现有 GateReport；
- Metrics Registry / formulas / provenance service；
- Narrative Portfolio / Debt / Payoff / Innovation Reward；
- Author Truth / Knowledge / Reveal；
- Runtime Context / Story Atlas / Distillation / Initialization artifacts；
- 现有十项 Validator。

明确禁止新建：第二 Candidate Score、Hard Gate、Debt Ledger、Payoff Engine、Innovation Reward、World State、Scheduler、Canon 或 Approval。

## 12. 最小实施顺序

1. typed `KernelPlanningContext` + target chapter boundary + Aggregate persistence；
2. Candidate Handoff 只消费该冻结 Context，并冻结 Scheduler Recommendation；
3. 清理 fixture entity prompt 污染；
4. `KernelEvidenceCompiler` 编译 declared/verified/differences；
5. 把 compilation 接入现有 Hard Gate 和旧公式输入；
6. Chapter Contract 冻结 declared + verified trace；
7. Draft Realized Trace 和现有 Validator 扩展；
8. Approval 后 Aggregate 失效与下章重投影；
9. Existing Novel semantic discovery handoff，lexical 路径降级为 fallback；
10. Workbench、失败案例、Legacy、CI、Live A/B 和最终报告。

## 13. 审计验收边界

本报告是代码修改前的生产接线快照。审计期间未修改 `book/`、Canon、Contract 状态、Draft 状态或 Edition；未执行语义生成；未将任何 Proposal 升级为事实。
