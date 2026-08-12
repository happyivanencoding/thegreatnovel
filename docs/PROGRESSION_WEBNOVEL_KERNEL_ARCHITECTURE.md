# Progression Webnovel Kernel V1 架构审计

> 状态：PWK-01 / 实施前审计  
> 基线：`progression-webnovel-kernel-v1`  
> 最高规范：`Novel_Authoring_System_Constitution_V2.md`

## 1. 结论

Progression Webnovel Kernel 应作为现有作者控制、规划和章节状态之上的结构合同层，而不是第二套小说运行时。它需要补齐的是“这本书持续向读者交付什么成长体验、成长怎样改变可能性、世界怎样随成长扩大、当前最值得承担什么章节功能”，而不是重新拥有已发生事实、正史提交、候选生成、债务、爽点、揭露或世界状态。

运行时权力保持如下顺序：

1. Source / Canon / `ChapterWorldStateView` 中已经发生的事实；
2. Author Truth、Author Directive、Author Must / Must Not；
3. 作者确认且在当前边界生效的 Effective Contracts；
4. Planning Aggregate、Narrative Debt、Reveal Agenda、Opportunity 等当前规划状态；
5. `SerialScheduler` 的可解释建议；
6. 现有 Candidate Ranking；
7. 现有 Innovation Reward；
8. Story Profile 和 Genre Adapter 的默认建议。

Preset 和 Adapter 只生成 Proposal。Scheduler、Candidate、Validator、Payoff 与 Debt 只读统一 Effective Contract，不允许按 Profile 或 Adapter 名称安排情节。

## 2. 现有系统职责图

| 现有职责 | 当前实现 | PWK 处理方式 |
|---|---|---|
| 不可变原文与章节 | Source Store、Edition、`BookLayout` | 不修改；所有历史投影继续以 Edition 和章节边界为准 |
| 已发生事实 | Canon Projection、`ChapterWorldStateView` | Progression State 只从它投影，不成为 Authority |
| 作者硬控制 | Author Truth、Author Directive、Author Task / Intent | Effective Contract 排在其后；冲突时作者控制优先 |
| 读者/人物知识 | Truth / Reveal、Knowledge Matrix | Progression Mystery 只引用 Reveal Agenda 与知识边界 |
| 候选 | `CandidateProposal`、三候选导入与硬门 | 扩展现有模型，不建立第二个 Candidate Engine |
| 章节合同 | `ChapterContract` | 冻结选中候选的 Progression / Genre / Intent 影响 |
| 叙事债务 | `NarrativePortfolioSnapshot.narrative_debts` | 增加债务类别和来源，不建立第二个 Debt Engine |
| 爽点与创新 | `NarrativePayoff`、`calculate_innovation_reward` | 增加 Genre Promise breakdown，仍先过硬门 |
| 多视界协同 | `CrossHorizonSynergy` | 直接复用，不建立新 Synergy Engine |
| Planning 冻结输入 | `PlanningAggregate.author_policy` | 加入 Effective Contracts、Progression State、Anticipation 与 Scheduler Recommendation |
| 作者工作台 | `build_workbench_context` + `workbench.html` | 增加“成长”节点和作者可读卡片，不显示空 RPG 面板 |
| 原创新书 | Original request → Local File Handoff → Proposal → 作者确认 → Genesis | 在 Foundation 之前增加 Reader Experience 确认 |
| 已有小说初始化 | Atlas-first Progressive Initialization | 生成 `NEEDS_REVIEW` / `SOFT_REFERENCE` Proposal，不写 Author Truth |

## 3. 当前架构审计问题

### 3.1 `OriginalBookRequest.genre` 为什么不足

`src/novel_authoring/original/models.py` 中 `OriginalBookRequest.genre` 只是一个自由文本字符串。`original_new.html` 也只把它呈现为“类型”输入框；当前 `original.service` 与 `original.genesis` 不消费该字段，因而它既不是合同，也不是运行时输入。它没有：

- 主阅读体验和副体验的层级；
- Setting Skin 与核心 Genre 的分离；
- Explanation Style；
- CORE / IMPORTANT / OPTIONAL / DISABLED 的 Genre Promise；
- 作者确认状态和生效边界；
- 可供 Validator、Scheduler、Candidate 共同读取的统一结构能力。

因此 `genre="近未来修仙"` 同时混合了世界外壳、成长语法和题材名称。后续语义生成只能自行解释，无法确定“近未来”应服务“修炼成长”，还是反过来让基础设施、制度或社会议题成为主发动机。

### 3.2 Story Foundation 为什么容易题材漂移

`StoryFoundationCandidate` 已有 `core_reading_promise`、`world_mechanism`、`growth_loop` 和 `long_term_possibility`，这是可复用基础；但三个候选只受 Pydantic 的数量与 ID 唯一性约束，没有共同绑定一份作者已确认的 Reader Experience / Genre / Progression Contract，也没有 Remove-the-skin 结构诊断。

当前 Bootstrap handoff 在同一次语义生成中同时解释 premise、决定类型、建立九维画像、生成三个 Foundation 和首章候选。生成器可以在“候选要明显不同”的压力下，把三案分散到不同文学类型；技术或主题细节也可能在尚未确认 Reader Promise 时取代成长发动机。

PWK 必须把流程改为：

```text
Premise
→ Reader Experience Interpretation Proposal
→ Author Confirmation
→ Effective Reader / Genre / Progression Proposal
→ 三个共享核心合同但结构不同的 Foundation
```

### 3.3 九维 Profile 为什么可能压过 Reader Promise

`BookProfileDraft` 和 `Global Book Profile` 要求完整覆盖 worldbuilding、characters、plot、style、narrative、dialogue、pacing、themes、continuity。Genesis 会把九维初稿写入 `book_profile_versions`，Planning Aggregate 和 Candidate 的 `profile_alignment` 也会读取它。

九维当前是覆盖面最完整、最显式的语义约束；相对地，Reader Promise 只有 Foundation 的一段文字。若 themes 或 worldbuilding 写得更具体，它们就可能在生成与对齐时获得更强注意力，使“怎么表现”压过“读者为什么追”。

PWK 不删除九维，而是把它降为 Craft Layer：九维继续约束表现方式；Reader Experience、Genre、Progression、World Expansion 和 Payoff Channel Contracts 先定义持续体验与结构因果。Profile 更新必须读取这些 Effective Contracts，但 Profile 不得反向覆盖核心 Promise。

### 3.4 `progress_gain` 为什么缺少结构化依据

`CandidateScoreInputs.progress_gain` 当前只是 `0..100` 数值；候选导入要求提供一组自由文本 `score_evidence`，评分器按已有权重消费它。Original Genesis 的首章候选甚至明确以 `NOT_COMPUTED` 和全零输入入库。现有确定性 authority 已在 `metrics.formulas.progress` 与 `metrics_registry.yaml` 定义 Permanent Growth、World State、Relationship、Knowledge、Goal、Strategy 六组件，但 Candidate Import 没有把自报标量桥接到这些组件、Metric Run 或 evidence span。

这意味着数值没有统一说明它来自：阶段变化、分支打开、瓶颈变化、资源转化、能力解锁、能力验证、成长代价或更高天花板可见性。不同生成任务可以用不同含义填写同一个数。

PWK 应先形成结构化 `ProgressionImpact`，映射到既有六组件或引用既有 Metric Run / observation，再调用现有 progress 公式计算或解释 `progress_gain`。非突破章节也可以因发现门槛、获得条件、验证能力、打开路线或看见下一层而获得进展；没有结构证据时数值保持缺失或不计算，不能伪造百分比。

### 3.5 Narrative Debt 如何直接扩展

现有 `planning.innovation.NarrativeDebt`、`NarrativePortfolioSnapshot`、`planning.diagnostics.build_narrative_portfolio_snapshot` 已经拥有多视界生命周期、到期状态、PAYOFF_READY / OVERDUE 诊断和 Candidate Planning 输入。`NarrativeDelta`、`ExpectedNarrativeDebt` 与 `NarrativePayoff` 也已连接 Innovation Reward。

PWK 只需给同一条债务增加结构类别与 Progression 引用，例如 PLOT、MYSTERY、RELATIONSHIP、PROGRESSION、POWER_SHOWCASE、RESOURCE、WORLD_EXPANSION、STATUS、TEAM、ANTICIPATION，并让投影器从当前能力、资源、阶段、世界层级与期待表面生成同类型债务。债务分值继续由 `metrics.formulas.narrative_debt` 负责，Age / Dormancy / Readiness / Dependency 的动作继续复用 `rhythm.diagnose_hooks`；Planning Portfolio 只携带这些结果及证据引用。POWER_SHOWCASE 的偿还方式是“能力真实改变解决方法”，可发生于战斗、逃脱、救援、探索、制作、谈判或规则破解。

### 3.6 World State 如何投影 Progression State

`author_control.projections.ChapterWorldStateView` 已是按章节读取的 `AFTER_CHAPTER` 视图，包含 characters、inventory、equipment、resources、abilities、knowledge、relationships、factions、world_rules、tasks、threads、promises 与 `chapter_delta`。`build_story_game_state` 已区分 Canon Event Projection、Source Chapter State Projection 和需要补齐的未知状态，并明确禁止把最新状态倒灌到早期章节。

`ProgressionStateView` 应作为其派生字段：

- 以选中章节的 chapter ordinal 为时间锚；
- 只使用该章可见的能力、资源、物品、知识、关系、势力、规则、线程和已生效 Contract；
- 对缺失数据返回 UNKNOWN / 缺少证据，不补造“73%”；
- available / locked branch 由已确认 Progression Contract 与截至该章证据共同决定；
- Opportunity、Anticipation、Payoff Readiness 保持 Planning Projection，不混入已拥有事实；
- 历史点击继续走同一个 `build_story_game_state(chapter_id=...)` 数据流。

当前 Workbench 还同时存在 `_chapter_context` 的 Canon-event-only 变化视图与
`build_story_game_state` 的 Source + Canon + Baseline 合成视图。PWK 不应再造第三套答案：
Progression Workspace 以 chapter-pinned `ChapterWorldStateView` 为唯一展示源，Canon-only
context 只保留边界元数据。跨层同一记录应按稳定 `state_key` / category 去重，同时保留
layer 与 evidence；不能仅按各层自己的 `record_id` 去重。

### 3.7 Author Truth / Reveal 如何连接 Progression Mystery

Author Truth 已管理真相类型、证据、兼容性、生效章与前向范围；Reveal 已管理 Reader / Character Knowledge、Reveal Plan、Agenda Bucket、Secret Board 和章节边界。PWK 不新增 Mystery Authority。

Progression Contract 可以引用 mystery binding；Anticipation 和 Scheduler 读取现有 Reveal Agenda；Candidate 的 `truth_alignment` / `reveal_impact` 继续负责“使用秘密但不越权揭示”。未被确认的 DerivedAdapter、Hidden Truth Candidate 或 Existing Novel Proposal 只能是 PROPOSAL / SOFT_REFERENCE，不能成为 Author Truth。

### 3.8 Payoff / Innovation 可以复用什么

可直接复用：

- `NarrativePayoff` 的 horizon、extent、value；
- `CandidateInnovationPreview` 的 expected payoffs / debts；
- `calculate_candidate_innovation_reward` 的硬门后奖励入口；
- `CrossHorizonSynergy` 的 SHORT / MID / LONG 协同；
- `QuestionBalance`、Pattern Repetition、Integration Cost 与 reward cap；
- Candidate 的 base score、final selection score 和同一可选区间。

新增 `GenrePromiseRewardBreakdown` 只能调节已经合法的 Candidate，且不得把 Innovation 本身当成核心体验。Genre drift penalty、progression utility、world expansion utility 等都在硬门通过后生效。

当前还存在 legacy `metric_results` 与现代 provenance-aware `metric_runs` 两条指标引用路径。
PWK 必须桥接并统一到现有指标 authority，不能再建立第三个 Progression Metrics Engine。

### 3.9 可能重复现有职责的新增模型

以下命名如果实现成可写引擎会产生重复，必须限制为合同或视图：

| 新概念 | 允许职责 | 禁止职责 |
|---|---|---|
| `ProgressionStateView` | Chapter World State 派生视图 | 写 Canon / 自建状态账本 |
| `OpportunitySurface` | 资源、关系、地点和选择的规划输入 | 把“可能存在”写成“已拥有” |
| `AnticipationSurfaceView` | 聚合 Debt、Reveal、Thread、Payoff 等只读期待 | 创造 Promise、Canon 或强制兑现 |
| `SerialScheduler` | 推荐 Chapter Intent 并解释理由 | 自动生成剧情或越过作者 |
| `PayoffChannelProfile` | 对现有 Payoff 分类和排序 | 第二套 Payoff Score / Ledger |
| `GenreDriftDiagnostic` | 软诊断与明确冲突检查 | 自动改题材或因单章未服务核心而硬拒绝 |
| `ContractProposal` | 待作者审查的语义方案 | 自动写 Author Truth |

### 3.10 Preset / Adapter / Contract / Runtime 的边界

```text
StoryProfile / AuthoringPreset
        ↓ 默认体验优先级
GenreAdapter / DerivedAdapterSpec
        ↓ 结构能力建议
Contract Proposal
        ↓ 作者确认 / 编辑 / 拒绝
Effective Contracts（带 effective_from_boundary）
        ↓
Runtime Projection / Validator / Scheduler / Candidate / Debt / Payoff
```

- Preset：只提供作者友好的默认值，不进入剧情分支。
- Adapter：把已知或自定义成长语法编译为统一能力，如 stage transition、resource gate、knowledge gate、ability unlock、verification、world expansion、mystery binding、team progression。
- Contract：作者确认后的结构规则和持续承诺；可以只影响后续，不能改写历史。
- Runtime：只读统一 Contract 字段和当前事实，不读取 `profile == ...` 或 `adapter == ...` 决定故事内容。

### 3.11 题材名称驱动业务逻辑的风险

当前没有发现成熟 Runtime 按 cultivation / occult / cosmic 名称安排宗门、秘境、学院或擂台；主要风险在自由文本语义入口：

1. `OriginalBookRequest.genre` 同时承担 setting 和 genre；
2. Bootstrap handoff 在 Reader Promise 未确认前解释题材；
3. Foundation 的三个候选只验证形式差异，不验证共享核心 Promise；
4. 九维 Profile 可能用具体主题覆盖抽象阅读承诺；
5. `progress_gain` 允许生成器直接填写数值；
6. 前端当前只展示“类型”自由文本和原始 Foundation 内容，没有作者先确认的 Step 0。

实施后必须有静态测试，禁止 `if profile == ...`、`if adapter == ...` 或等价题材名分支出现在 Scheduler、Candidate、Validator、Payoff 与 Debt Runtime。

审计还发现一个与新 Kernel 接入直接相关的现存断点：`OriginalFoundationConfirmation`
虽然接收 `characters_override` 与 `factions_override`，`build_genesis_apply_plan` 当前没有消费
这两个字段。PWK 在扩大 Wizard 合同之前必须让作者确认的角色与势力覆盖进入可审计的
Genesis Apply Plan，不能用 Adapter 或语义 Prompt 掩盖表单值丢失。
同一处还要明确顶层 proposal protagonist / goal 与选中 Foundation 对应字段的优先级，避免
作者选择了某个 Foundation，却仍使用另一层的默认主角设定。

## 4. 目标模块边界

最小模块布局：

```text
src/novel_authoring/progression/
├── models.py          # Reader/Genre/Adapter/Progression/World/State/View 合同
├── presets.py         # StoryProfile 和内置 Adapter Proposal 编译
├── contracts.py       # Proposal -> Effective Contract、版本与作者确认
├── projections.py     # chapter-aware Progression/Expansion/Opportunity/Anticipation
├── scheduler.py       # 可解释 ChapterIntentRecommendation
├── diagnostics.py     # Promise、Drift/Evolution、Remove-the-skin
└── service.py         # edition-aware 存取与 Workbench read model
```

`planning.models` 只扩展现有 Candidate 与 Chapter Contract 字段；`planning.rewards` 只增加 Genre Promise breakdown；`author_control.projections` 只挂载投影视图；`web.workbench` 和模板只负责作者侧展示。

## 5. 数据与状态生命周期

### 5.1 Proposal 不是事实

Contract 采用至少以下状态：

- `INFERRED_PROPOSAL`：来自已有小说的证据化推断；
- `SOFT_REFERENCE`：可用于提示但不约束 Runtime；
- `NEEDS_REVIEW`：旧项目或原创新书待作者确认；
- `EFFECTIVE`：作者确认并从指定边界生效；
- `REJECTED`：明确拒绝；
- `SUPERSEDED`：被新版本取代。

创建 Proposal 不产生 Author Truth、Canon Event、Chapter State 或作者批准记录。Effective Contract 修改默认 `FORWARD_ONLY`；若作者要求改变已发生历史，必须进入现有 Edition Revision 工作流。

### 5.2 Legacy 行为

没有 Effective Contract 的旧项目继续：读取 Source、Canon、World State、编辑和使用原有续写流程。Progression Workspace 显示“尚未建立成长体系”，提供生成建议或手动建立；不得显示虚假的 RPG 空面板，也不得阻断旧功能。

### 5.3 Planning 冻结

计划下一章时，Planning Aggregate 冻结：

- Effective Reader Experience / Genre / Progression / World Expansion / Payoff Contracts；
- chapter-aware Progression State；
-现有 Narrative Portfolio、Reveal Agenda、Author Tasks / Intents；
- Anticipation Surface；
- Scheduler Recommendation 及作者 Override。

Candidate Import 检查冻结输入的一致性，再执行现有硬门、评分和 Innovation Reward。Scheduler Recommendation 不是 Candidate Lens；一个 Lens 可以服务不同 Intent。

Scheduler 的组成应直接复用 `rhythm.diagnose_hooks` 的 action queues、作者 Task / Intent、
即时 aftershock / deadline、现有 ThreadNeed 与 pressure，产出带 evidence 的建议。`CandidateLens`
仍只是候选的观察角度；现有 lens coverage diagnostic 不是配额、硬门或分数奖励。

## 6. Hard Gate 与 Soft Diagnostic

Hard：Canon / Source / Author Must / Must Not 冲突；未满足已确认 gate 却突破；未获得资源却消费；新能力无 provenance；未来知识泄漏；明确 `CONTRADICTS_CORE_PROMISE`。

Soft：单章不服务核心 Promise；连续多章成长无变化；能力长期未验证；资源长期不转化；世界长期无新空间；期待衰减；Payoff 渠道重复；突破过密；成长没有代价；Genre Replacement 风险。

`DOES_NOT_SERVE_CORE_PROMISE` 不是硬错误。Recovery、Relationship、Aftermath、Transition 章节完全合法。Genre Evolution 在核心“可能性持续扩大”仍成立时不应被判作 Drift。

## 7. 实施切片与验收

1. Reader Experience、Story Profile、Genre Contract / Adapter / DerivedAdapter 的纯模型与编译测试。
2. Progression Contract、Topology、Delta、Stage、Breakthrough、World Expansion、Resource / Opportunity 模型。
3. Migration 与 edition-aware Proposal / Effective Contract Service；验证 Proposal 不改 Canon。
4. chapter-aware Progression / World Expansion / Anticipation 投影；验证无未来泄漏和 UNKNOWN 语义。
5. 扩展现有 Narrative Debt、Payoff 与 Candidate；验证非战斗 Power Showcase、非数字成长与非人物主体。
6. Serial Scheduler 与持久化 Override；验证可解释、仅建议、Intent 与 Lens 分离。
7. Genre Drift / Evolution / Remove-the-skin；验证单章缺席是软诊断、核心冲突才是硬错误。
8. Original Wizard Step 0、成长与长线确认、三 Foundation 共享 Contract。
9. Workbench“成长”页面、Candidate Card、历史状态与 Imported Proposal。
10. 四个内置 Seed、三个 OOD Seed、近未来体修 A/B、浏览器截图和全量工程验证。

每个切片独立提交并推送到 `origin/progression-webnovel-kernel-v1`。生产代码不得修改 `book/` 原文、自动接受 Contract、自动写 Author Truth，或建立新的 Canon / Debt / Payoff / Candidate / World State authority。

## 8. 关键验收路径

### 原创新书

```text
一句话 Premise
→ 阅读体验解释
→ 作者调整并确认
→ Effective Reader / Genre / Progression Proposal
→ 三个共享核心 Promise、结构不同的 Foundation
→ 作者确认 Foundation 与 Contracts
→ 现有首章 Candidate / Contract / Draft / Approval 流程
```

### 已有小说

```text
Atlas-first Initialization
→ Contract Proposals（INFERRED_PROPOSAL / SOFT_REFERENCE）
→ 作者确认或保持建议
→ chapter-aware Progression Workspace
→ 现有 Continuation Boundary / Candidate / Chapter Contract
```

### OOD 自定义成长

```text
Premise
→ Structural Interpretation
→ DerivedAdapterSpec Proposal
→ Author Confirmation
→ Unified Effective Contracts
→ 同一个 Projection / Scheduler / Candidate / Payoff / Validation Runtime
```

系统最终不得要求原创成长语法“选择最接近的已有模板”，也不得退回宗门、秘境、学院、擂台或 `level + 1`。
