# Chinese Serialized Webnovel Kernel

## 1. 定位

Chinese Serialized Webnovel Kernel 是中文长篇连载的轻量通用编排层。它回答“这本书长期靠什么持续产生下一章期待”，再把已确认的驱动力分派给专用故事引擎。

Progression Webnovel Kernel 是它的第一个、最成熟、当前唯一达到完整生产能力的 Specialized Narrative Engine。玄幻、仙侠、高武、科幻玄幻、末世进化与神秘学晋升仍优先使用它；通用层不会降低成长、资源、突破、能力验证、世界扩张与成长债务的深度。

```text
Chinese Serialized Webnovel Kernel
├── Reader Experience Contract
├── Market Category Metadata
├── Narrative Drive Contract / Drive Mix
├── Universal Serial Scheduler
├── existing Payoff / Narrative Debt / Hook infrastructure
└── Specialized Narrative Engines
    ├── Progression Engine                 # V1 深实现
    ├── Mystery & Reveal Engine            # V1.1，复用现有 Truth / Reveal
    ├── Career & Mastery Engine             # V1.2
    ├── Strategy & State-Building Engine    # V1.3
    ├── Competitive Skill / Team Engine     # V1.4
    ├── Survival / Base-Building Engine     # V1.5
    └── Relationship / Life Engine          # V1.6
```

## 2. Market Category 与 Narrative Drive

`MarketCategoryMetadata` 服务书库分类、标签、推荐、检索、统计和产品展示。`XUANHUAN`、`URBAN`、`HISTORY` 等分类不进入章节调度权威，也不能自动推出战争、朝堂、比赛、突破或关系情节。

`NarrativeDriveContract` 是经作者确认的长期推进机制：一个 Primary Drive、二至四个 Secondary Drives、优先级、读者承诺、当前状态、Payoff Channel、Debt Type、疲劳风险和作者覆盖。Universal Scheduler 只读取 Drive Mix、各 Engine 的状态与建议，以及既有 Debt、Payoff、Thread、Reveal、Author Task、Arc Phase 和 Fatigue；它不读取书站分类来决定章节功能。

Reader Experience 回答“读者为什么追”；Narrative Drive 回答“故事靠哪些长期机制兑现”；Specialized Engine 回答“该机制的领域状态、门槛、意图、债务与验证如何计算”。三层不得折叠成一个题材名称。

## 3. Engine Adapter 边界

所有专用引擎通过 `NarrativeEngineAdapter` 暴露统一能力：

- `build_state`：从既有 Source / Canon / Author Control 投影领域状态；
- `recommend_intents`：返回带 Drive、证据、读者承诺、债务和风险的建议；
- `evaluate_candidate` / `validate_candidate`：解释候选对该 Drive 的作用，不创建第二套 Candidate；
- `produce_payoff_channels` / `produce_debts`：扩展既有 Payoff / Narrative Debt，不复制公式或账本；
- `render_author_summary`：提供作者可读摘要，不把 Raw Enum 直接当界面。

Progression Engine 完整实现协议。其他 Engine 在当前阶段只登记能力与 `NOT_IMPLEMENTED_DEEPLY` 深度，不显示假的完整控制台、不阻断旧项目，也不自行创建 Truth、World State、Candidate、Payoff 或 Debt authority。Mystery & Reveal 后续必须复用现有 Author Truth、Reader Knowledge、Character Knowledge、Reveal Plan、Reveal Agenda 与 Secret Board。

## 4. Universal Scheduler

每个已启用 Engine 返回若干 `EngineIntentRecommendation`。Universal Scheduler 在 Author Task、即时余波和硬边界之后，按已确认 Drive Priority、Engine 信号、Debt 成熟度、Payoff 期待与疲劳风险合成一个 Primary Chapter Intent 和最多两个 Secondary Intents，并说明：为什么现在需要、来自哪个 Drive、解决什么债务、兑现什么 Reader Promise、有什么风险。

Scheduler 只建议章节功能，不生成事件、不选择 Candidate、不写 Canon。作者 Override 仍是最高优先的显式规划输入。单章没有服务 Primary Drive 是软诊断；长期失衡或与确认承诺冲突才产生 Drive Drift Warning。

## 5. 为什么 Progression 仍然优先

Progression Engine 已具备阶段、非数字成长、分支与牺牲拓扑、资源门槛、能力来源、验证、成长主体、世界上限、机会、期待、Debt、Payoff、Scheduler、Candidate Alignment 与 Drift/Evolution。通用层只聚合这些输出，不复制字段。

非成长小说可以把 `CAREER_MASTERY`、`STATE_BUILDING`、`COMPETITIVE_SKILL`、`MYSTERY_INVESTIGATION`、`RELATIONSHIP_EMOTIONAL` 等设为 Primary Drive，并不创建虚假的战力阶段、神秘能量或突破门槛。若 Progression 只是 Secondary，Progression Contract 可以为空或只覆盖知识、团队、身份等真实成长轴。

## 6. Structural Reference Corpus Catalog

约 454 本参考语料首先只建立 `WebnovelCorpusEntry` 目录：标题、规范标题、别名、市场分类、来源集合、可用格式、分析状态和人工审阅状态。仅凭标题不得填充 Narrative Drive、Progression Model、Payoff Channel、Arc 结构、文风或关系强度。

结构标签只能来自 `MANUAL_CONFIRMED`、`DISTILL_DERIVED`、`SOURCE_DERIVED` 或 `PROPOSAL`，未确认 Proposal 不得成为训练和评估权威。后续 Corpus Phase 从中选择约 40—60 本覆盖不同 Narrative Engine 的结构锚点做深度蒸馏；具体作品名只可出现在目录、研究报告或用户本地书库，生产代码和测试一律使用原创合成 Seed，禁止 title-specific Adapter 和剧情模板。

## 7. 路线图与当前范围

- V1：Progression Engine 深实现；通用 Drive Contract、Engine Protocol、Universal Scheduler、Drive Alignment / Drift。
- V1.1：Mystery & Reveal Engine，优先复用现有揭露基础设施。
- V1.2：Career & Mastery Engine。
- V1.3：Strategy / State-Building Engine。
- V1.4：Competitive Skill / Team Engine。
- V1.5：Survival / Base-Building Engine。
- V1.6：Relationship / Life Engine。
- V2：多引擎连载调度与 Corpus Calibration。

当前版本不实现八套完整引擎。验收重点是：Progression 专长不退化；职业、历史治理、电竞、灵异等非力量成长 Seed 能被正确识别，且不会被强制玄幻化。
