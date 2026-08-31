# GitHub 小说生成竞品代码深审：46 个仓库 × TGN 架构突破点｜2026-08-31

## 结论

这轮不再以 README、功能名或 GitHub Stars 作为主要依据，而是把前两轮识别出的项目全部拉到本地，沿着真正决定长篇小说系统能力的代码路径阅读：

> **输入怎样冻结 → 谁决定故事 → Writer 实际拿到什么 → 草稿怎样审核 → 什么时刻进入正史 → 失败后怎样恢复 → 长期状态怎样继续影响后文。**

本轮共覆盖 **46 个仓库**，扫描到约 **327.5 万行代码、8.76 万行文档、5.35 万个文件和 6,441 个测试文件**。对大型仓库采用“架构关键路径深读”，没有把前端组件、翻译文件、生成代码和与小说因果无关的基础设施逐行阅读；对小型 Skill 仓库则基本读完了全部可执行代码和主要协议文档。

最重要的结论有六条。

### 1. 公开竞品已经把“AI 写长篇的基础设施”做得相当完整

现在已经不稀缺的能力包括：

- 大纲 → 章节 → 正文的多阶段流水线；
- RAG、向量检索、知识图谱和滚动摘要；
- 角色卡、世界观卡、伏笔表和时间线；
- Writer、Editor、Reviewer、Director 等多 Agent 命名；
- 断点恢复、工作区、任务进度和桌面编辑器；
- “去 AI 味”、章节评分和一致性检查；
- 把用户名字、MBTI 或 Persona 文本写进故事。

因此，TGN 再增加一个 Agent、一个 Reviewer、一个知识图谱，已经不足以构成突破。

### 2. 真正稀缺的是“叙事事务”，而不是“更多记忆”

代码层最强的项目不是 Agent 最多的项目，而是能回答下面这些问题的项目：

- 被审核的正文，是否就是最后写入正史的那一份？
- 未通过的候选稿，能否污染人物状态、RAG 或 Canon？
- 章节中途崩溃后，系统知道应该从哪个确定阶段恢复吗？
- 状态提取与状态采用是否分开？
- 下一阶段读取的是已批准事实，还是某次临时生成结果？

这一方向上，`novel-studio`、`inkos`、`ainovel-cli`、`novel-architect` 和 `AI-Novel-Writing-Assistant` 最值得研究。

### 3. TGN 在“创意来源与正文权限”上仍然领先绝大多数公开项目

没有发现另一个公开系统同时具备：

1. 无主角的世界先独立成立；
2. Power Seed 与 Human Seed 分开生成；
3. Story Program 才进行第一次完整碰撞；
4. Director、Curator、Primary Writer 拥有不同信息权限；
5. 正文必须闭合结果、归属、奖励、Public Proof、关系和社会重新估价；
6. Supporting Logic 不得抢成 Story Engine。

竞品通常是在一个 Architect 或同一上下文中连续完成“世界—人物—能力—主线—正文”。这很容易得到连贯、自洽、合理，却被同一种理性同化的小说。

### 4. TGN 当前真正落后的，是运行内核和产品可观测性

TGN 已有 Frozen Authority、Atomic Chapter Obligations、Authority Reviser、Canon 和 Run Ledger，但代码层仍可继续收敛为更清楚的事务链：

```text
PREPARED
→ DIRECTED
→ CURATED
→ DRAFTED
→ AUTHORITY_ACCEPTED
→ STATE_EXTRACTED
→ CANON_COMMITTED
```

并明确规定：

> **只有 AUTHORITY_ACCEPTED 的精确正文，才有资格产生正式状态；只有正式状态提交成功，才允许下一章读取。**

产品层上，TGN 也明显落后于 `AI-Novel-Writing-Assistant`、`NovelForge` 和 `NovelClaw` 的桌面工作台、运行进度、人工接管、差异预览与恢复界面。

### 5. “把用户本人放进小说”不是创新；“人格造成长期优势分化”仍是明显空白

公开项目已经会：

- 把用户姓名和经历写进主角；
- 用 MBTI 或问卷生成 Persona；
- 让用户每回合自己选 A/B/C；
- 根据 Persona 生成更符合性格的台词或动作。

但本轮没有找到一个系统，把下面这条链正式做成长篇 Canon：

```text
真实人格的稳定选择偏向
→ 同一机会面上的不同选择
→ 不同路线与真实错失
→ 不同人物、地点与际遇
→ 不同的新非对称优势
→ 与旧优势发生不同复合
→ 改变后续几十章的行动空间
```

这正是 TGN 最有希望建立的新品类：

> **人格因果型非对称成长（Personality-Causal Asymmetric Progression）**。

### 6. TGN 不应抄一个竞品，而应吸收三种不同优势

- 从 `novel-studio`、`inkos`、`ainovel-cli` 吸收**事务、阶段和恢复**；
- 从 `AI-Novel-Writing-Assistant`、`NovelForge`、`NovelClaw` 吸收**产品工作台与可观测性**；
- 从交互世界项目吸收**离屏人物、后果账本和平行 Reality**；
- 保留 TGN 自己的**创意来源分离、Authority Wall、商业男频 Story Craft 和人格因果成长**。

---

# 一、研究范围与方法

## 1. 审计对象

本轮仓库来自三轮检索：

- 真正生成长篇小说的引擎；
- 作者工作台、知识图谱、互动叙事和世界 Runtime；
- 论文代码、Claude/Codex Skill、中文网文工作流和榜单中项目。

最终拉取 46 个公开仓库的当前默认分支浅克隆，并记录其 commit。完整修订号见附录。

## 2. 深读标准

对于每个具有真实运行代码的项目，优先寻找以下路径：

```text
Orchestrator / Pipeline / Router
Context Assembler
Writer / Narrator Prompt
State / Memory / Canon
Review / Revision / Acceptance
Persistence / Commit / Recovery
Branch / Reality / Consequence
Tests
```

不把以下内容误当成故事引擎能力：

- README 中没有代码支撑的市场预测或留存评分；
- 仅仅存在一个名为 `Agent` 的类；
- 把全文塞入向量库；
- 用 LLM 对自己的正文打分；
- 只检查字数和文件是否存在；
- UI 中存在“人物”“世界观”“伏笔”几个页面。

## 3. 证据等级

本报告不用虚假的 0—100 分，而采用三种证据等级：

- **深读**：核心运行路径、状态路径和测试均已检查，部分项目实际运行测试；
- **代码核验**：关键实现已读，但因依赖、语言环境或仓库规模没有完整运行；
- **协议/说明核验**：仓库本质是 Skill、手册、模板或项目清单，可执行代码很少或不存在。

## 4. 实际运行的测试

本轮只运行能改变判断的测试，而没有为了数字好看把所有仓库都安装一遍。

- `zhougz520/novel-architect`：**77 passed**；验证其 Brief、Beat Competition、Gate、State Guard 和重算逻辑确实有代码合同。
- `leenbj/novel-creator-skill`：**10 个流程测试通过**；覆盖初始化、自动草稿、Gate、回滚、缓存幂等、重工和发布失败。
- `wgwtest/novel-writing`：**13 passed**；其正文检查器是小而真实的确定性工具。
- `JeroTan/novel-writer-english`：**11/11 passed**；其只读 Story Library MCP 能正确处理章节范围、缺章、重号和来源位置。
- `novel-studio`、`ainovel-cli`：本机与 WSL 均没有 Go，因此没有运行测试；这不是仓库失败。
- `NarrativeRuntimeEngine`：新克隆环境在测试收集阶段缺少 `loguru`、`chardet`，仓库又没有可直接找到的依赖清单。这是**可复现性/打包问题**，不是测试断言失败。

---

# 二、竞品真正形成的六类架构

## A. 叙事事务型引擎

代表：`novel-studio`、`inkos`、`ainovel-cli`、`novel-architect`。

共同特点不是“写得更好”，而是：

- 阶段明确；
- 草稿和正式事实分离；
- 失败可以恢复；
- 某些工件在进入下一阶段后冻结；
- 代码而非 LLM 决定下一步允许做什么。

这是 TGN 最值得直接吸收的一类。

## B. 整本生产与产品工作台

代表：`AI-Novel-Writing-Assistant`、`NovelForge`、`NovelClaw`、`Novelgen`。

优势是：

- 书、卷、章、卡片、运行任务与模型配置均有 UI；
- 用户能看见进度、手动接管和修改；
- 数据库存储、桌面端和长任务管理较成熟。

短板是：Story Craft 通常较通用，Authority 边界没有 TGN 严格。

## C. 互动世界与角色模拟 Runtime

代表：`project-lunar`、`openovel`、`rpg-roleplay-platform`、`EdgeTales`、`Corvus-Story-Core`、`InfiPlot`。

优势是：

- NPC 有私人状态、目标、秘密和对玩家的看法；
- 世界可离屏推进；
- 每次行动产生结构化后果；
- 某些系统支持分支存档和平行 Reality。

短板是：用户每回合亲自选行动，所以它们没有回答“系统认为真实的你会怎样选择”。

## D. 层级规划与研究框架

代表：`Dramatron`、`Re3`、`DOC`、`RecurrentGPT`、`MARP`、`LongWriter`、`GOAT-Storytelling-Agent`。

这些项目分别证明了：

- 层级规划比一次生成全文稳定；
- 候选重排和局部重写能改善短中篇；
- 更细的未来纲要能提高控制；
- 自然语言长期记忆可以递归维持；
- 多角色 Agent 能产生涌现事件；
- 将长输出拆成子任务能突破模型长度。

但它们多数不处理数百章 Canon、奖励归属、力量复利和正史事务。

## E. Skill、手册和工作流包

代表：`novelops-skill`、`novel-creator-skill`、`webnovel-handbook`、`novel-writer-skills`、`oh-story-claudecode` 等。

这里的质量差异极大：

- 好项目会把文件状态、章节 Gate、只读查询或确定性检查真正写成代码；
- 弱项目只是在 `SKILL.md` 中罗列几十个高级功能；
- 有的甚至把同一模型的自评称为“留存预测”“爆款模型”。

TGN 应吸收小而确定的工具，不应把大而全的 Skill 当作新的权威层。

## F. 编辑器、清单和展示项目

代表：`91Writing`、`MaliangAINovalWriter`、`awesome-llm-story-generation`。

它们可以帮助发现项目或参考 UI，但不能作为小说因果架构证据。

---

# 三、最重要竞品的代码级判断

## 1. `Xiaoyangy/novel-studio`：当前最完整的“叙事事务”参考

### 实际架构

核心代码不是简单的：

```text
Outline → Writer → Reviewer
```

而是：

```text
当前弧全局模拟
→ POV Projection
→ Capacity Check
→ Seal Arc
→ Chapter Promotion
→ Exact-body Render
→ Exact-body Review
→ Acceptance
→ Live Canon Publish
```

关键文件：

- `cmd/novel-studio/pipeline_arc_cycle.go`
- `cmd/novel-studio/pipeline_chapter_render_transaction.go`
- `internal/agents/render_drafter_prompt.go`
- `README-TECHNICAL.md`

### 真正强的地方

1. **先投影整弧，再逐章生成。** 当前章不是在毫无未来承载力的情况下临时决定。
2. **封存后的计划具有身份。** 恢复时可以判断当前运行对应哪一个 Plan，而非只看文件名。
3. **审核针对精确正文。** 不是先审核 A，最后保存 Writer 又改过的 B。
4. **候选稿与 live canon 分离。** 未接受正文不会自然进入正式世界状态。
5. **Canon、Foundation、RAG 有独立 snapshot root。** 检索材料不等于正史。
6. **有 provider call budget 和 bounded realization。** 能避免失败循环无限调用模型。

### 对 TGN 的直接价值

TGN 不必复制所有 SHA 和 Receipt；只有当摘要能替代重新读大文件、或需要证明“被审核正文就是被提交正文”时，才值得保留正文摘要身份。

真正应该吸收的是：

> **Candidate Workspace → Acceptance → Exact Commit**。

### 它不如 TGN 的地方

它的世界、角色和故事上游仍没有 TGN 那样明确的 World/Power/Human 独立来源；也没有 TGN 的主角欲望、Reward、Surprise、Social Repricing、Public Proof 和非对称优势复合语义。

---

## 2. `narcooo/inkos`：章节工作区与恢复机制最值得近距离借鉴

关键文件：

- `packages/core/src/pipeline/runner.ts`
- `chapter-review-cycle.ts`
- `chapter-state-recovery.ts`
- `chapter-persistence.ts`
- `chapter-truth-validation.ts`
- `state/chapter-workspace.ts`
- `persisted-governed-plan.ts`
- `agents/planner-context.ts`
- `forecast/runner.ts`

### 代码实际做到的事

- 每章拥有独立 Workspace；
- Governing Plan 被持久化；
- 草稿、审核、真值校验、状态结算与工件落盘分开；
- 中断后能重建章节运行状态；
- 对未来有独立 Forecast，而不是让正文 Writer 临时编造所有后续；
- Persistence 与 Truth Validation 是显式步骤。

### 对 TGN 的价值

`inkos` 比很多“多 Agent 小说系统”更接近 TGN，因为它没有把所有正确性寄托给 Reviewer，而是承认：

> **章节生产是一个有中间工件、有采用边界、有失败恢复的事务。**

TGN 最值得借的是它的 Workspace 结构，而不是复制其所有字段。

---

## 3. `ExplosiveCoderflome/AI-Novel-Writing-Assistant`：完整产品链最强

关键文件：

- `server/src/services/novel/production/NovelPipelineExecutor.ts`
- `runtime/ChapterRuntimeCoordinator.ts`
- `runtime/ChapterPipelineRuntimeAdapter.ts`
- `runtime/chapterRuntimePipeline.ts`
- `runtime/GenerationContextAssembler.ts`
- `volume/ChapterExecutionContractService.ts`
- `state/StateCommitService.ts`
- `prompting/prompts/novel/chapterLayeredContext.ts`

### 实际架构

它已经从“一句话生成一章”发展成：

```text
Book Direction
→ World / Characters
→ Volume Strategy
→ Chapter Execution Contract
→ Layered Context
→ Generation / Review / Repair
→ State Commit
→ Pending / Official Facts
```

### 最值得借鉴

- Chapter Execution Contract；
- Context 分层组装；
- 正式事实与待确认事实分开；
- State Commit 的来源记录；
- 长任务 Runtime、Checkpoint 和产品 UI；
- 人工接管与质量债务可视化。

### 与 TGN 的边界

它拥有执行合同，却没有 TGN 那样严格的 Primary Authority Blind 和 Atomic Commercial Obligations。它更像成熟导演式产品，TGN 更像叙事编译器。

---

## 4. `voocel/ainovel-cli`：最干净的确定性路由器

关键文件：

- `docs/engine-rfc.md`
- `internal/flow/state.go`
- `internal/flow/router.go`
- `internal/host/engine.go`

它的核心原则可以概括为：

> **事实层由代码决定，语义层交给模型。**

Engine 从 Store 读取 Phase/Flow，路由到下一步 Worker。模型不负责决定工作流是否完成。

### 对 TGN 的启发

TGN 的角色可以很多，但运行状态机应尽量少：

```text
状态 + 确定性 Route → 唯一下一步
```

不要让 Director 或 Reviser 自己决定“我现在是否应该写 Canon”。

### 不应照搬

它的 Writer 同时负责计划、写作、自检和 Commit，容易重新形成单模型自洽闭环。TGN 的 Agent 权限分离仍更适合高质量商业小说。

---

## 5. `zhougz520/novel-architect`：这轮最意外、也最值得持续跟踪的项目

关键文件：

- `orchestrator/pipeline.py`
- `planning/brief.py`
- `planning/writing_task.py`
- `planning/beat_competition.py`
- `planning/context.py`
- `review/gate.py`
- `review/repair.py`
- `signals/visible_payoff.py`
- `signals/state_guard.py`
- `state/master.py`
- `state/recompute.py`

其 **77 个测试全部通过**。

### 实际能力

- 将章节 Brief 编译成写作任务；
- 多个 Beat 候选竞争，而不是只采纳第一个自洽方案；
- 检查 Visible Payoff；
- 用 State Guard 阻止错误状态推进；
- 通过确定性重算恢复 Master State；
- Gate 与 Repair 分开。

### 与 TGN 的关系

它证明 TGN 的两个方向是对的：

1. 章节任务需要先编译，而不是让 Writer 自己理解全部上游；
2. 候选竞争比同一个 Agent 内部“认真想一想”更可能产生真实 Variation。

但它还没有：

- World/Power/Human 的来源隔离；
- 人格导致路线和优势谱系分叉；
- 正文信息权限墙；
- TGN 式力量尺、Public Proof 和社会重新估价。

---

## 6. `RhythmicWave/NovelForge`：数据模型与工作流工作台强，故事权威弱

关键文件：

- `backend/app/services/workflow/engine/runtime.py`
- `execution_plan.py`
- `state_manager.py`
- `workflow/nodes/ai/context.py`
- `memory_extractors/character_dynamic.py`
- `review/review_prompt_builders.py`

### 优势

- Schema 驱动的卡片；
- 通用 Workflow Engine；
- 图谱化人物、地点、物品与关系；
- 动态人物状态抽取；
- 可编程 Context 节点和 Review；
- Electron/Vue/FastAPI 的成熟作者工作台。

### 判断

NovelForge 非常适合作为 TGN 未来 UI 和结构化编辑器的参考，但它把“什么是正确工作流”交给用户配置。知识图谱能表示事实，却不能替代 Story Program 决定下一件最值得读的事。

---

## 7. `letuhao/lore-weave`：最宏大的世界平台，但不适合直接搬进 TGN MVP

关键文件：

- `services/composition-service/app/services/plan_forge_service.py`
- `contracts/plan-forge/novel_system_spec.schema.json`
- `authoring_run_service.py`
- `engine/cowrite.py`
- `engine/self_heal.py`

### 真正值得注意的两个思想

1. **PlanForge**：把作品计划变成结构化系统规格；
2. **一本源世界可以生成多个持久 Reality**：不同分支不是一次性聊天，而是各自拥有持续世界状态。

### 对 TGN 的价值

平行 Reality 很适合未来的“现实自我 / 理想自我 / 阴影自我”三条人格命运实验。

### 不应复制

LoreWeave 是一个庞大微服务平台。TGN 当前不需要复制它的服务数量、契约层和基础设施；先把人格因果与章节事务做对，价值更高。

---

## 8. `felixchaos/rpg-roleplay-platform`：后果账本与分支提交很成熟

关键文件：

- `rpg/chat_pipeline/gm.py`
- `persist.py`
- `context_engine/core.py`
- `agents/acceptance_verifier.py`
- `state/consequence_ledger.py`
- `kb/canon_repo.py`
- `platform_app/branches/commits.py`
- `platform_app/persona_skills.py`

### 强项

- Event-style 持久化；
- Consequence Ledger；
- Canon Repository；
- Acceptance Verifier；
- 分支 Commit；
- Persona Skill；
- 可以把既有小说世界摄取成可玩的 Runtime。

### 对 TGN 的启发

TGN 的人格实验最好不要只保存三本正文，而应保存：

```text
Human → Choice → Consequence → Acquisition
```

这样才能解释三条命运为何分开。

但此项目仍然由玩家每回合选择，Persona 只是辅助上下文，不是自动替用户持续作决定的 Frozen Human。

---

## 9. `Feed-Scription/openovel`：前台叙述与后台世界维护的分离很有价值

关键文件：

- `src/runtime/storyTransaction.js`
- `src/runtime/sessionProcessor.js`
- `src/workflows/storykeeperWorkflow.js`
- `src/lib/narrator.js`
- `src/agents/README.md`

它把快速响应的 Narrator 与后台 Showrunner、Story Keeper、Card Manager 分开，避免每回合都等待所有世界更新。

### 值得借鉴

对于 TGN 产品化，可以让：

- 用户先看到章节正文；
- 后台再完成昂贵但非阻塞的索引与展示工件；
- 但正式下一章仍必须等待 Canon Commit。

### 关键限制

它面向互动叙事，事务主要保护一轮会话状态，没有 `novel-studio` 那种“精确被接受正文 = 精确正史正文”的强合同。

---

## 10. `horizonfps/project-lunar`：NPC 私人心智和离屏演化最值得学习

关键文件：

- `backend/app/services/game_session.py`
- `backend/app/engines/auditor_engine.py`
- `backend/app/engines/npc_mind_engine.py`

NPC 不只有一张公开人物卡，还拥有：

- 私人感受；
- 对玩家的看法；
- 当前目标；
- 秘密计划；
- 离屏活动。

### 对 TGN 的价值

这能帮助 TGN 避免配角只在主角视野内存在。尤其在 World Expansion 后，已有强者、组织和敌人应根据自己的知识和利益作出反应，而不是等主角登场才启动。

### 限制

它仍是互动 RPG；主角人格由玩家即时行动表达，而非系统内部 Frozen Human。

---

## 11. `kirinonakar/Novelgen`：滚动 Memory 做得丰富，但采用边界较弱

关键文件：

- `src-tauri/src/generator/types.rs`
- `memory.rs`
- `streams.rs`

它会维护：

- Facts；
- Open Threads；
- 角色状态；
- 关系状态；
- 滑动窗口上下文；
- 分段流式生成。

这是一套不错的长文 Continuation Memory，但“被抽取到 Memory”与“经过 Authority 批准成为正史”没有 TGN 那样严格分开。

---

## 12. `iLearn-Lab/NovelClaw`：运行可观测性优于故事权威

关键文件：

- `apps/novelclaw/workflow/executor.py`
- `apps/novelclaw/workflow/claw_manager.py`

它最值得参考的是：

- Session、Task、Progress、Log 和 Artifact；
- Storyboard 与 Manuscript 分开；
- 用户可返回运行现场；
- Memory Bank、World、Character、Style 分面板。

TGN 当前需要类似的“这一章到底卡在哪里、用了多少时间、哪个工件已经冻结”的产品层。

---

## 13. `YILING0013/AI_NovelGenerator`：经典流水线的代表，也暴露了传统方案的上限

关键文件：

- `novel_generator/architecture.py`
- `blueprint.py`
- `chapter.py`
- `knowledge.py`
- `vectorstore_utils.py`
- `finalization.py`

### 实际流程

```text
一个大 Prompt 生成设定/人物/情节/章节纲要
→ 生成章节
→ 更新全局摘要
→ 更新人物状态
→ 更新情节弧
→ 写入向量库
```

### 代码级问题

这些更新按顺序直接执行，没有一个统一采用事务。中途失败时，章节、摘要、人物状态、Plot Arc 和向量库可能处在不同步状态。

它的一致性检查主要生成报告，不是“未通过就禁止状态进入下一章”的 Gate。

这正是 TGN 不应退回的传统结构。

---

## 14. `qiyan233/novelops-skill`：小而清楚的 Draft / Revise / Extract / Update

关键文件：

- `scripts/novelops_cli.py`
- `draft_chapter.py`
- `auto_revise.py`
- `extract_state.py`

其真实价值是把以下动作拆开：

```text
Draft
→ Revise
→ Extract State
→ Update Truth Files
```

同时提供快照、diff 和 CLI。

它没有 TGN 的 Authority 语义，但适合参考文件布局与最小 CLI，而不是引入大型 Agent 框架。

---

## 15. `leenbj/novel-creator-skill`：单体流程虽重，但并非纯宣传项目

关键文件：

- `scripts/novel_flow_executor.py`
- `scripts/chapter_gate_check.py`
- `scripts/test_novel_flow_executor.py`

本轮实际运行的 10 个流程测试全部通过，覆盖：

- 初始化；
- 自动草稿与 Gate；
- 回滚；
- 幂等缓存；
- 质量失败；
- 节奏跳过；
- 发布失败；
- 记忆更新控制。

它的问题是大量职责集中在一个 Flow Executor 中，长期维护会变困难；但不能简单归类为“只有 Prompt”。

---

## 16. `Re3` 与 `DOC`：最值得保留的是候选控制，不是论文时代的模型实现

### Re3

关键文件：

- `scripts/main.py`
- `story_generation/plan_module/plan.py`
- `draft_module/beam_candidate.py`

它使用 Plan、候选续写、相关性/连贯性重排和局部重写，说明：

> 第一个可接受生成不一定应该直接成为正文。

### DOC

关键文件：

- `story_generation/plan_module/outline.py`
- `draft_module/beam_candidate.py`

它使用更细的多层 Outline 和未来上下文控制，说明细纲对长距离控制有效。

### 对 TGN 的判断

TGN 可以在**高杠杆 Beat 或 Opportunity**上采用有限候选竞争，但不应让每个段落都 Beam Search。后者会极慢，而且容易把惊喜重排成平均正确。

---

## 17. `RecurrentGPT`、`MARP`、`LongWriter`：解决的是三个不同问题

- `RecurrentGPT`：用自然语言模拟短期记忆、长期记忆和下一段计划；
- `MARP`：让环境、设计者、Writer 和角色 Agent 共同形成故事；
- `LongWriter`：把超长输出拆成多个子任务，突破单次长度。

它们分别解决“记住”“涌现”“写长”，都没有自动解决：

- 什么有资格成为正史；
- 奖励是否真正归主角；
- 同一 Human 是否持续作出同类但不重复的选择；
- 世界位置是否发生商业可感的重新估价。

---

# 四、图片中十个 Skill 项目的代码真相

## 1. `JeroTan/novel-writer-english`

最真实的代码资产是 `src/mcp/story-library.js`：它提供项目目录绑定的只读查询，能返回人物、地点、术语、章节范围、缺章、重号和来源行号。11 个测试全部通过。

结论：**优秀的包装和查询层，不是小说引擎。**

## 2. `GonsonInter/novel-writer-workflow`

主要是场景 SOP、道具/时间/术语/数字表和 P0/P1/P2 审核协议。

结论：可吸收“机械问题交给代码、叙事问题交给模型”，但默认每场多轮审稿会拖慢 TGN 并平均文风。

## 3. `wgwtest/novel-writing`

其 `check_manuscript_text.py` 会确定性检测标点、对话标签、可疑标题、短段密度、镜像句和重复句首。13 个测试通过。

结论：**小而诚实的 Lint**，适合 TGN 审计技能，不需要升级成 Agent。

## 4. `qiyan233/novelops-skill`

代码真实实现 Draft、Revise、Extract、Truth Update、快照和 diff。

结论：图中十项里最接近运行系统的项目之一。

## 5. `miserylee/webnovel-handbook`

高质量中文网文知识库，强调渐进式加载、每章承诺/进度/回报、人物不是作者喇叭、避免纪要式证据链。

结论：适合 Curator 选择性读取，不应整体注入 Primary。

## 6. `HZ-KMNO/web-novel-writing-guidance-skill`

所谓 A/B/C 不是三个并行候选，而是：初稿 → 内容修正 → 内容锁定后的语言处理。

结论：与 TGN Preservation First 高度兼容，但不需要再增加三个常驻 Agent。

## 7. `wordflowlab/novel-writer-skills`

CLI 的主要价值是安装、模板、项目初始化。`check-consistency.sh` 主要依赖 Markdown 表格计数和 grep；其中用 `-f` 检查 `tracking` 目录，是一处真实可达的条件判断错误。

结论：借产品包装，不借“小说 = Spec-Kit 实施”的认知模型。

## 8. `wgwtest/novel-project-strategy`

强调 planned、drafted、accepted、synced 不是一回事，以及新会话恢复时的文件加载纪律。

结论：对 TGN Run Ledger 很有帮助。

## 9. `jwynia/agent-skills` 中的 `story-sense`

它只是大型 Skill 库中的诊断路由器：Assess → Diagnose → Route。

结论：TGN 可做 Failure Router，但应根据 Atomic 缺失、状态错误和具体证据路由，不能只凭另一个 LLM 的整体印象。

## 10. `novel-writer-skill` 同名仓库

### `czq8411/novel-writer-skill`

可执行代码主要是文件管理、备份和字数检查；README 所称市场趋势、留存预测、爆款模型、风格指纹等，没有相应校准模型或训练代码。

结论：**功能名称明显大于代码能力。**

### `2306192492-coder/novel-writer-skill`

所谓 Vector Search 实际是中文 bigram TF-IDF + cosine；它是无依赖词法检索，不是 Embedding 语义记忆。

结论：可作廉价 Baseline，不应宣传成长期语义记忆。

---

# 五、其他项目中的具体代码发现

## `PenglongHuang/chinese-novelist-skill`

这是纯协议型工作流。其“并行章节无冲突”声明与实际文件合同不一致：多个 Agent 都会更新同一个 `01-大纲.md` 和 `02-写作计划.json`，在文档支持的并行模式下存在真实写冲突。连续三次生成失败后，流程仍可能把项目标成 `completed`。

另外，每章硬性要求固定比例对话、多个张力峰和惊喜，容易把长篇节奏写成同一模板。

## `ALBEDO-TABAI/deep-novel-system`

代码主要是幂等复制模板；同一个 Acting Model 完成写作、自评、记忆更新和状态更新。

结论：结构文件很多，但没有独立 Authority。

## `mave99a/novel-skill`

支持 RPG 选项、章节生成和 EPUB。Self-insert 由用户自己持续选路，不是人格模型替用户作选择。

## `91Writing`

`src/services/api.js` 是多供应商前端 API 适配，`src/stores/novel.js` 主要维护 localStorage 中的项目、章节、人物和世界观。

结论：是不错的本地编辑器，不是长篇 Canon Runtime。

## `Deng-m1/MaliangAINovalWriter`

当前仓库克隆内容基本只有说明材料，没有足够代码供架构核验。产品功能可以列入市场观察，但不能与已经审过核心运行代码的项目放在同一证据层。

## `Picrew/awesome-llm-story-generation`

这是项目清单，不是生成系统。

---

# 六、TGN 当前真正应该吸收的五项能力

## 1. Thin Narrative Transaction Kernel

不要新增一个庞大的“事务平台”，只需让当前章节链拥有一个清楚的 Workspace：

```text
chapter_workspace/
  frozen_input/
  director/
  curator/
  candidates/
  accepted_body/
  extracted_state/
  commit_record/
```

运行状态固定为：

```text
PREPARED
DIRECTED
CURATED
DRAFTED
AUTHORITY_ACCEPTED
STATE_EXTRACTED
CANON_COMMITTED
```

必须满足：

- Rejected Draft 不得更新 live Canon；
- State Extraction 只读取 accepted body；
- 下一章只读取 CANON_COMMITTED；
- 恢复逻辑只根据显式状态决定下一步；
- 若正文摘要身份真的用于跳过重读或证明采用一致性，可以使用 digest；否则不增加无用途哈希。

## 2. Deterministic Failure Router

不是再安排一个“万能审稿人”，而是把具体失败路由到最小修复：

```text
Atomic Obligation 未闭合
→ Authority Repair

Human 选择无因果证据
→ Human Causality Repair

程序化说明抢正文
→ Procedural Leakage Repair

奖励没有真正归属
→ Acquisition Repair

Public Proof 只有震惊、没有现实变化
→ Social Repricing Repair

World Expansion 忽略主角当前状态
→ Expansion Collision Repair
```

## 3. Candidate Competition 只放在高杠杆位置

从 `novel-architect`、Re3 和 DOC 学到的不是“每段生成三稿”，而是：

- 第一场碰撞；
- 重大选择；
- 新优势来源；
- 世界扩张入口；
- 卷末结算；

这些位置可以产生 2—4 个结构候选，再由代码检查硬条件、由独立判断选择。普通段落不需要候选搜索。

## 4. Product Observability

未来工作台应让作者直接看到：

- 当前章处于哪个状态；
- Frozen Authority 与 Writer 实际上下文；
- 哪条义务未闭合；
- Reviser 改了哪些段落；
- 哪些状态已提取、哪些已提交；
- 模型、时间、成本和失败原因；
- 接受、拒绝、局部重跑的影响范围。

## 5. Parallel Reality 只服务于人格实验

暂时不构建 LoreWeave 级平台。最小版本只需允许：

```text
同一 World Seed + 同一 Core Power
→ Human A Reality
→ Human B Reality
→ Human C Reality
```

每个 Reality 分别拥有 Canon、Route Ledger 和 Advantage Stack。

---

# 七、TGN 最有机会形成的新品类：人格因果型非对称成长

## 1. 不是 MBTI 外挂

错误做法：

```text
谨慎 → 护盾
善良 → 治疗
外向 → 魅惑
野心 → 火焰
```

这只是人格测试结果页。

正确结构是：

```text
同一个不为主角设计的世界
+ 同一个初始 Core Power
+ 同一个机会面
+ 不同 Frozen Human
→ 不同选择
→ 不同路线
→ 不同错失
→ 不同获得
```

## 2. Frozen Human 应保存什么

不是标签，而是稳定选择变量：

- 欲望排序：钱、胜负、面子、自由、爱情、力量、归属；
- 风险阈值；
- 被轻视后的反应；
- 对未知、占有、竞争和控制的偏好；
- 哪些具体关系会改变最优选择；
- 哪些代价会让他退出；
- 哪些东西会让他自我欺骗；
- 会保护什么、绝不接受什么；
- 核心稳定，但现场手段必须重新生成。

## 3. 必要的最小因果工件

不建议增加十张人物表，只需四种可追踪结果：

### Decision Surface

由世界和当前状态独立生成，列出真正互斥的机会、时间窗口和代价。它不能先读取 Human 后为其定制“专属正确答案”。

### Choice Record

记录：

```text
Human 中哪条证据
→ 使角色在当前现场选择了什么
→ 为什么没有选择另一条更普遍的最优路线
```

### Route / Opportunity Ledger

记录走进了什么路线，以及永远或阶段性错失了什么。错失不能在下一章用等价奖励偷偷补回来。

### Acquisition Provenance

每个新优势必须能追溯：

```text
Human Evidence
→ Choice
→ Route
→ Opportunity
→ Sacrifice / Missed Alternative
→ Acquisition
→ Compound Effect
```

## 4. Shared Growth Floor + Exclusive Opportunity Lineage

真实人格不应成为惩罚机制。

每条路线都必须满足商业小说的共同成长底线：

- 主角获得真实新能力或资源；
- 行动空间扩大；
- 至少一次可感的 Public Proof 或关系变化；
- 世界重新给主角报价；
- 新欲望自然产生。

但不同人格不能总拿到同一奖励。新优势的来源、机制和未来可行动空间必须不同。

## 5. 与 World Expansion 的连接

正确的世界扩张应分两层：

```text
New World Baseline
```

仍然独立、主角盲，不因为主角很强就把整个新世界设计成他的镜子。

```text
Expansion Collision Layer
```

必须读取主角当前：

- 力量与能力组合；
- 已公开声望；
- 关系与同行者；
- 可携带资产；
- 世界留下的伤痕与敌人；
- 过去选择形成的行为倾向。

这样，新世界自身仍然广阔，却会对一个已经足够强大的主角产生真实反应。

---

# 八、最有判别力的受控实验

## 冻结条件

完全相同：

- World Vision；
- Core Power；
- 初始身份；
- 第一场危机；
- Opportunity Graph；
- GBrain 输入；
- 章节长度和商业成长底线。

只替换三个 Frozen Human：

1. 用户批准的现实自我；
2. 与其动机排序明显相反的人格；
3. 用户批准的理想自我或阴影自我。

## 长度

每版 10 章，至少经历 3 个 Matched Decision Points。运行中不让用户点击 A/B/C。

## 通过条件

1. 去掉姓名、外貌和口头禅后，用户仍能仅凭选择认出哪一版最像自己。
2. 每个新优势都能写出完整 Acquisition Provenance。
3. 三版优势在机制、来源和行动空间上不同，而不是同一“剥纹术”的三种用法。
4. 三版都保持强成长和商业阅读价值。
5. 只替换 Human 会改变 Choice/Route/Acquisition；只替换文风不会改变这些因果结果。
6. 至少一次 World Expansion 读取各版已经不同的主角状态，产生不同 Collision，而不是把三版重新合流。

---

# 九、不建议 TGN 复制的东西

1. **不复制超级 Skill。** 一个 Skill 同时做世界、人物、正文、评分、市场预测和修复，只会制造新的自我证明。
2. **不把知识图谱升级为 Story Engine。** 图谱擅长保存事实，不擅长判断下一件最值得读的事。
3. **不让 Writer 自己计划、写作、审核、提交。** 这会破坏现有 Authority Wall。
4. **不默认每场三轮审稿。** 速度、意外性和文风都会被平均。
5. **不把未校准的数值称为留存预测。** 没有真实读者数据，就只能叫启发式信号。
6. **不让不同路线最后拿齐所有奖励。** 那会消灭人格造成的长期差异。
7. **不把人格直接翻译成能力标签。** 人格应该通过选择改变际遇。
8. **不在 MVP 阶段复制大型微服务与迁移框架。** 当前真正缺的是因果和事务，不是平台规模。
9. **不增加无人读取的哈希和 Receipt。** 只有结果会改变恢复、跳过重读或采用判断时才值得存在。

---

# 十、最终优先级判断

## 现在应该做

### 第一优先：人格因果实验

这是 TGN 最可能产生新品类价值的地方，也是当前竞品没有完整占据的空白。

### 第二优先：薄 Narrative Transaction Kernel

它会让现有 Frozen Authority、Atomic Obligations 和 Canon 真正形成不可混淆的运行链。

### 第三优先：高杠杆候选竞争与 Failure Router

解决惊喜、优势谱系趋同和修复成本问题。

## 之后再做

- 作者工作台；
- 平行 Reality UI；
- 更完整的离屏人物模拟；
- 桌面端和富文本编辑；
- 多书管理与团队协作。

## 最终定位

公开竞品大多在争夺：

> “谁能更方便地用 AI 写一本长篇小说。”

TGN 更有价值的定位应是：

> **把一个真实的人放进一个并不为他量身定制的世界，让他的欲望、偏爱、软肋与冒险方式真正改变他会遇见什么、失去什么、得到什么，并最终长成只属于他的非对称强者形态。**

技术上，这需要把 TGN 已有的创意来源分离与 Authority Runtime，同一个更薄、更可靠的章节事务内核结合起来。

---

# 附录 A：46 个仓库逐项覆盖表


> 行数是本轮扫描口径，用于理解仓库规模，不等于有效叙事代码量；大型 monorepo 包含大量 UI、基础设施与生成文件。测试文件数也不等于测试质量。

| 仓库 | 类型 | 证据 | 扫描代码行 | 检测测试文件 | 本轮 revision | 代码判断 |
|---|---|---:|---:|---:|---|---|
| `2306192492-coder/novel-writer-skill` | 轻量 Skill | 深读 | 213 | 0 | `cd8b2ada5d` / 2026-04-21 | 中文 bigram TF-IDF 检索，不是语义向量记忆。 |
| `aiwaves-cn/RecurrentGPT` | 递归记忆研究 | 代码核验 | 658 | 0 | `ea520e99f4` / 2024-05-15 | 自然语言短期/长期记忆与下一段计划；记忆不等于 Authority。 |
| `ALBEDO-TABAI/deep-novel-system` | 模板型 Skill | 深读 | 89 | 0 | `a975371f13` / 2026-04-24 | 代码只负责模板初始化；同一模型写作、自评和更新状态。 |
| `czq8411/novel-writer-skill` | 一站式 Skill | 深读 | 1,505 | 2 | `ae95aedbab` / 2026-05-22 | 实际代码主要是文件管理/字数；市场与留存能力明显过度宣称。 |
| `Deng-m1/MaliangAINovalWriter` | 产品说明 | 说明核验 | 0 | 0 | `08894a21e1` / 2026-07-19 | 仓库当前几乎没有可审核心代码，不能把功能表当架构证据。 |
| `edgetales/edgetales` | Solo RPG | 深读 | 15,486 | 0 | `327105b539` / 2026-04-13 | Director/Narrator/Metadata/Risk/Clock 体系丰富；不是自动长篇。 |
| `ExplosiveCoderflome/AI-Novel-Writing-Assistant` | 整本生产产品 | 深读 | 443,465 | 296 | `2b9c429830` / 2026-08-27 | Chapter Contract、分层上下文、State Commit 与桌面工作台成熟。 |
| `Feed-Scription/openovel` | 互动叙事运行时 | 深读 | 86,088 | 118 | `1b4404e85d` / 2026-06-17 | 前台 Narrator 与后台 Story Keeper 分离，适合异步产品体验。 |
| `felixchaos/rpg-roleplay-platform` | 角色扮演平台 | 深读 | 270,140 | 408 | `f8a15039f7` / 2026-08-29 | Consequence Ledger、Canon、Branch Commit、Acceptance Verifier 很有价值。 |
| `GOAT-AI-lab/GOAT-Storytelling-Agent` | 层级故事生成 | 代码核验 | 740 | 0 | `75637b176d` / 2025-11-12 | Book Spec→Chapter Plot→Scene Plan→Prose，结构清楚但状态薄。 |
| `GonsonInter/novel-writer-workflow` | 场景 SOP | 协议核验 | 0 | 0 | `3400a07896` / 2026-04-23 | 场景级审稿与 P0/P1/P2；默认多轮审核可能过重。 |
| `google-deepmind/dramatron` | 研究框架 | 代码核验 | 238 | 0 | `2e7c36afad` / 2024-07-17 | Logline→Character→Plot→Location→Dialogue 的层级剧本生成。 |
| `horizonfps/project-lunar` | 互动世界模拟 | 深读 | 22,898 | 31 | `7bf9ab801c` / 2026-08-11 | NPC 私人心智、离屏目标和 Auditor 强；主角选择仍由玩家输入。 |
| `HZ-KMNO/web-novel-writing-guidance-skill` | 修订工作流 | 协议核验 | 0 | 0 | `24dd6d4009` / 2026-07-09 | 初稿→内容修正→语言处理，符合 Preservation First。 |
| `iLearn-Lab/NovelClaw` | 可观测工作区 | 代码核验 | 56,234 | 1 | `226d50d3ec` / 2026-06-01 | Session/Task/Artifact/Memory 面板优秀；正式采用合同较弱。 |
| `JeroTan/novel-writer-english` | 工作流+只读 MCP | 深读+测试 | 2,199 | 1 | `6d836f2328` / 2026-08-09 | Story Library MCP 查询可靠，11/11 tests passed；不是生成内核。 |
| `JustLateNightAI/Corvus-Story-Core` | 互动故事核心 | 代码核验 | 27,113 | 0 | `8e5e7345eb` / 2026-06-18 | Narrator + 隐藏 GM 抽取状态，事务和测试较弱。 |
| `jwynia/agent-skills` | 通用 Skill 库 | 协议核验 | 58,335 | 3 | `e02ec7e226` / 2026-02-24 | story-sense 是诊断路由器；适合启发 Failure Router。 |
| `kirinonakar/Novelgen` | 桌面长文生成 | 代码核验 | 19,659 | 0 | `f31055dcc5` / 2026-08-29 | 滚动 Facts/Open Threads/角色关系状态丰富；接受边界较弱。 |
| `leenbj/novel-creator-skill` | 单体小说流程 | 深读+测试 | 16,982 | 8 | `a327428ea2` / 2026-03-11 | Flow Executor 与 Gate 有真实代码，10 个流程测试通过。 |
| `letuhao/lore-weave` | 大型世界平台 | 深读 | 1,396,618 | 4,150 | `df18e90496` / 2026-08-09 | PlanForge、自愈约束、持久 Reality 强；规模远超 TGN 当前需要。 |
| `mave99a/novel-skill` | RPG 小说 Skill | 代码核验 | 362 | 0 | `0eadccbeb1` / 2026-01-07 | 用户选路后生成章节/EPUB；不属于自主人格模拟。 |
| `minki-j/InteractiveStoryGame` | 人格互动故事 | 深读 | 2,091 | 0 | `5809f5f22a` / 2024-11-18 | LangGraph + Persona 文本；人格只进入 Prompt，用户每回合选路。 |
| `miserylee/webnovel-handbook` | 中文网文知识库 | 协议核验 | 0 | 0 | `700b2a718c` / 2026-06-15 | 高质量渐进式知识库；应由 Curator 最小读取。 |
| `modoojunko/awesome-novel-agent` | Skill/工具集合 | 深读 | 6,810 | 5 | `98a733dece` / 2026-08-28 | 架构文档和 prose linter 有用；无正式叙事 Runtime。 |
| `multi-agent-story-generation/MARP` | 角色 Agent 研究 | 代码核验 | 2,579 | 0 | `64d899ef6b` / 2024-04-07 | 环境、设计者、Writer 与 Player Agents；易形成共享上下文自洽。 |
| `myjumpers/NarrativeRuntimeEngine` | 小说世界编译器 | 深读 | 37,613 | 50 | `c0d976dcdd` / 2026-06-29 | 文本→世界图谱/时间线/Runtime；新克隆缺依赖清单导致测试不可复现。 |
| `narcooo/inkos` | 长篇运行时 | 深读 | 174,799 | 307 | `091048383f` / 2026-08-26 | 章节 Workspace、Governed Plan、Truth Validation 与恢复链很强。 |
| `PenglongHuang/chinese-novelist-skill` | 中文小说 Skill | 深读 | 179 | 0 | `3db1e3be88` / 2026-08-23 | 并行模式共享写文件有冲突风险，固定节奏指标易模板化。 |
| `Picrew/awesome-llm-story-generation` | 项目清单 | 说明核验 | 0 | 0 | `570893c026` / 2026-06-29 | 用于发现项目，本身不生成小说。 |
| `ponysb/91Writing` | 本地编辑器 | 代码核验 | 52,473 | 0 | `df3de0362e` / 2025-08-12 | 前端多模型 API、localStorage 项目管理；不是 Canon Runtime。 |
| `qiyan233/novelops-skill` | 状态工作流 Skill | 深读 | 5,690 | 2 | `320a42fe76` / 2026-07-26 | Draft/Revise/Extract/Truth Update、快照和 diff 清楚。 |
| `RhythmicWave/NovelForge` | 作者工作台 | 深读 | 75,153 | 1 | `7c2d84ef80` / 2026-08-28 | Schema 卡片、通用 Workflow、图谱和编辑器强；Story Authority 依赖用户配置。 |
| `THUDM/LongWriter` | 长输出研究 | 代码核验 | 4,276 | 0 | `447539b356` / 2025-06-24 | AgentWrite 先规划再分段生成；解决长度而非数百章因果。 |
| `voocel/ainovel-cli` | 确定性状态机 | 深读 | 71,049 | 115 | `c0900290be` / 2026-08-25 | Store/Route/Worker 清楚；Writer 权限比 TGN 更集中。 |
| `wgwtest/novel-project-strategy` | 项目状态治理 | 协议核验 | 0 | 0 | `1ebfc154e1` / 2026-04-19 | planned/drafted/accepted/synced 分层，对恢复纪律有价值。 |
| `wgwtest/novel-writing` | 小说诊断 Skill | 深读+测试 | 766 | 3 | `b6382cf7ff` / 2026-08-24 | 小而真实的正文 Lint，13 tests passed。 |
| `wordflowlab/novel-writer-skills` | Spec-Kit 式 Skill | 代码核验 | 6,380 | 0 | `5bc9b373ff` / 2025-10-20 | 安装和模板强；一致性脚本较粗且存在目录判断错误。 |
| `xiaoxiaoxiaotao/novel-ai-agent-Chinese` | 通用小说 Agent | 代码核验 | 1,863 | 0 | `7aa790ed8b` / 2026-02-16 | 标准 Agent Loop/Context，Canon 与采用边界较薄。 |
| `Xiaoyangy/novel-studio` | 叙事事务引擎 | 深读 | 298,210 | 291 | `9da2ff1555` / 2026-07-25 | 弧级投影、封存、精确正文审核与 Canon 发布最完整；TGN 首要工程参考。 |
| `yangkevin2/doc-story-generation` | 研究框架 | 深读 | 4,416 | 0 | `9d727cdbae` / 2023-10-26 | 多层详细纲要与未来上下文控制；不处理长篇 Canon。 |
| `yangkevin2/emnlp22-re3-story-generation` | 研究框架 | 深读 | 3,018 | 0 | `3a97ebde04` / 2022-12-21 | Plan/Draft/Rewrite/Edit 与候选重排；适合局部候选思想。 |
| `YILING0013/AI_NovelGenerator` | 经典生成流水线 | 深读 | 9,374 | 4 | `f9aefef90b` / 2026-06-25 | 设定—目录—章节—摘要—向量库；顺序状态写入可产生部分提交。 |
| `zenstory-ai/oh-story-claudecode` | 商业写作 Skill 集 | 深读 | 51,295 | 4 | `5de060f9a4` / 2026-08-30 | 章节生命周期、Tracking Commit、Author Memory 和确定性脚本较完整。 |
| `zhougz520/novel-architect` | 章节编译与 Gate | 深读+测试 | 24,623 | 63 | `8be8035225` / 2026-07-27 | Brief Compiler、Beat Competition、Visible Payoff、State Guard 均有真实实现，77 tests passed。 |
| `zonghaoyuan/infiplot` | 互动分支叙事 | 代码核验 | 23,409 | 0 | `a60e18bc66` / 2026-07-02 | Director/Writer/Context 与下一分支预测；用户仍亲自选择。 |

---

# 附录 B：本轮重点阅读文件索引

## 叙事事务与运行状态

- `novel-studio/cmd/novel-studio/pipeline_arc_cycle.go`
- `novel-studio/cmd/novel-studio/pipeline_chapter_render_transaction.go`
- `inkos/packages/core/src/pipeline/runner.ts`
- `inkos/packages/core/src/pipeline/chapter-state-recovery.ts`
- `inkos/packages/core/src/pipeline/chapter-truth-validation.ts`
- `ainovel-cli/internal/flow/router.go`
- `ainovel-cli/internal/flow/state.go`
- `novel-architect/.../orchestrator/pipeline.py`
- `novel-architect/.../review/gate.py`
- `novel-architect/.../state/recompute.py`

## 上下文、执行合同与状态采用

- `AI-Novel-Writing-Assistant/.../ChapterExecutionContractService.ts`
- `AI-Novel-Writing-Assistant/.../GenerationContextAssembler.ts`
- `AI-Novel-Writing-Assistant/.../StateCommitService.ts`
- `NovelForge/backend/app/services/workflow/engine/runtime.py`
- `NovelForge/backend/app/services/workflow/nodes/ai/context.py`
- `Novelgen/src-tauri/src/generator/memory.rs`
- `novelops-skill/scripts/extract_state.py`

## 世界模拟、Persona 与后果

- `project-lunar/backend/app/engines/npc_mind_engine.py`
- `project-lunar/backend/app/engines/auditor_engine.py`
- `rpg-roleplay-platform/rpg/state/consequence_ledger.py`
- `rpg-roleplay-platform/rpg/platform_app/branches/commits.py`
- `InteractiveStoryGame/app/utils/verbalize_profile.py`
- `InteractiveStoryGame/app/agents/subgraphs/decision_game/graph.py`
- `openovel/src/workflows/storykeeperWorkflow.js`

## 候选、规划与研究方法

- `emnlp22-re3-story-generation/story_generation/draft_module/beam_candidate.py`
- `doc-story-generation/story_generation/plan_module/outline.py`
- `doc-story-generation/story_generation/draft_module/beam_candidate.py`
- `LongWriter/agentwrite/plan.py`
- `LongWriter/agentwrite/write.py`
- `RecurrentGPT/recurrentgpt.py`
- `MARP/marp/environments/story_environment.py`

## Skill 与确定性工具

- `novel-writer-english/src/mcp/story-library.js`
- `novel-writing/novel-writing/scripts/check_manuscript_text.py`
- `novel-creator-skill/scripts/chapter_gate_check.py`
- `awesome-novel-agent/tools/check-prose.py`
- `wordflowlab/novel-writer-skills/templates/scripts/bash/check-consistency.sh`
- `2306192492-coder/novel-writer-skill/vector-search.js`

---

# 附录 C：研究边界

本报告可以支持以下判断：

- 这些公开仓库目前实际实现了什么；
- 哪些 README 功能有代码支撑；
- 哪些机制能直接启发 TGN；
- 在本轮公开样本中，哪些组合尚未出现。

本报告不能单独证明：

- TGN 的概念具备专利意义上的全球首创性；
- 某项目生成的小说主观质量一定优于另一个项目；
- 没有公开代码的商业闭源产品不存在相同机制；
- 扫描代码行越多，系统越先进。

最可靠的下一步仍然是受控实验，而不是继续扩大功能名清单。
