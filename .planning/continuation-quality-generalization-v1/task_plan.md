# Task Plan: Continuation Quality Generalization v1

## Goal

在不覆盖工作树既有用户改动的前提下，把现有 TheGreatNovel 续写/原创/修订链路收敛为一套可跨题材复用的连续创作质量内核，并把所有章节批准动作改为作者显式点击、服务端复核、页面内反馈的非阻塞交互。

完成条件不是让当前十章样本“看起来更好”，而是让同一套生产函数能够在生存/资源、战力/修炼、谜团或关系等不同 Reader Experience 中发现读者可见矛盾、伪成长、同构疲劳、长期未兑现的体验承诺和实现缩水，同时不把某类男频规则硬加给其他小说。

## Scope and ownership

- 当前工作树已有大量未提交/未跟踪内容；本轮只修改本轮明确归属的源代码、测试、计划/审计工件和新分支提交内容，不清理、不重置、不覆盖既有内容。
- 先核对当前 branch、HEAD、merge-base、远端和目标分支 ancestry；目标分支为 `continuation-quality-generalization-v1`，若创建前发现同名分支则先审计其差异。
- 不创建第二套 Canon、Event Store、Scheduler、Workflow、Vector DB、Embedding 或当前 fixture 专用 parser。
- 不把自然语言文学判断伪装成 Python 分数；边缘模型负责语义提取/审阅，Python 负责合同、证据存在性、Projection 对比、约束结算和发布边界。

## Phases

### Phase 1 — Baseline and architecture audit

- [completed] 读取并记录当前工作树、分支 ancestry、权威文档来源和现有计划。
- [completed] 逐项审计 `DESIGN_VALUES.md`、`MVP_REWRITE_SPEC.md`、`Novel_Authoring_System_Constitution_V2.md`、`AGENTS.md`、`PLAN.md`；当前树缺失时从 Git 历史/其他分支读取并明确记录。
- [completed] 追踪 Candidate → Chapter Contract → prose → review/handoff → validation → approval → Event Store/Projection → next planning 的真实数据流。
- [completed] 回答 `architecture.md` 的十个问题，列出可扩展的现有模型/路径与最小插入点。
- [completed] 搜索当前故事专有实体、固定章节窗口、伪 Character/Style 分数、blocking approval 路径，建立改造基线。

### Phase 2 — Reader-visible continuity and shared authority

- [completed] 在现有 Draft/StateChange/Projection 结构中扩展最小 `ReaderVisibleClaim`（或遵循现有命名的等价模型），不建立平行事实库。
- [completed] 让 prose review/revision/handoff 或现有边缘步骤输出高价值 claims 与正文证据；Python 验证实体、前值、transition、数量来源、Contract 范围、证据存在性和 materialization。
- [completed] 覆盖状态矛盾、数量跳变、无事件所有权/位置变化、耗尽能力重现、周期超限、无 delta 的 progression、时间重置、未物化 claim 和内部 workflow 泄漏等通用 finding。
- [completed] 用至少三类 fixture 参数化测试连续性引擎，并确认硬 Canon/Timeline/Knowledge 冲突仍阻断、软体验诊断不越权。

### Phase 3 — Usage constraints and progression delta

- [completed] 扩展现有 progression/state/contract 模型，加入通用周期 Usage Constraint：DAILY、COMBAT_SCENE、RESOURCE_GATED、ONE_TIME 及合法 reset event。
- [completed] 明确 period 不等于章节，进入下一章不自动 reset，约束可附着能力/物品/资源/规则/角色/世界机制。
- [completed] 建立通用 Progression Delta，区分 REUSE、SHOWCASE、MASTERY、UNLOCK、UPGRADE、BREAKTHROUGH、STAGE_TRANSITION、LOSS、TRADEOFF；只有合同宣称成长时强制核对 before/after、可见 delta、来源与新行动可能。
- [completed] 增加跨家族参数化测试，证明同一引擎可处理资源、修炼和关系/知识变化。

### Phase 4 — Serial experience, realization, metrics, reference, publication

- [completed] 扩展/整理 `ChapterExperienceSignature` 与现有 portfolio/planning，使结构比较覆盖 subject、method、opposition、payoff、ending、delta、社会/关系/知识/世界变化；horizon 从书籍合同/配置读取，不在业务代码固定 3/10/50。
- [completed] 输出结构疲劳与 reader-promise underserved 诊断；按运行模式作为 soft guidance，不把软诊断变成统一硬门。
- [completed] 移除伪 Character Fit/Style Fit；保留确定性 measurements、合同表面覆盖和有正文证据的语义审阅 `UNKNOWN`。
- [completed] 修复 realization baseline：薄章节和非健康状态不能拉低基线；区分表达薄与 Contract 太小导致的 `CONTRACT_REALIZATION_UNDERSPECIFIED`，阈值由 serial policy/config 提供。
- [completed] 让 Reference provenance 区分 UNAVAILABLE、ZERO_RESULTS、OFFERED、APPLIED、OFFERED_NOT_APPLIED、REJECTED_DUE_TO_CONFLICT；核对冻结 snapshot 结构证据，不自动奖励 offered。
- [completed] 集中维护 Publication Boundary：系统内部词由词表检测，元叙事交给有证据的 prose audit，continuity 与 Projection 统一核验。

### Phase 5 — Non-blocking approval UI

- [completed] 盘点原创第一章、普通下一章、修订稿、批量章节和候选入正文所有批准入口及共享组件。
- [completed] 删除 `window.confirm`/章节审批阻塞式 dialog/overlay 等二次确认，保留作者一次显式批准、现有 endpoint、stale bundle 复核、transaction 和 Canon 写入边界。
- [completed] 让成功、stale bundle 拒绝、服务端校验失败都在页面内更新状态和显示 inline feedback，不自动批准、不在前端伪造成功。
- [completed] 以 continuation Draft Review 实际页面做 in-app browser smoke；Original 入口由实际模板/脚本扫描和共享 endpoint integration 覆盖，当前 UI 没有独立 revision Canon approval 页面。

### Phase 6 — Cross-family regression and experiments

- [completed] 优先复用现有 benchmark/fixture，补足生存/资源、战力/修炼、谜团或关系三类最小场景；同一生产函数、usage engine、progression engine、experience portfolio 均参数化复用。
- [completed] 当前 Seed 只做只读回归/rehydration：验证 continuity/既有盲读边界、结构诊断、realization 和 UI，不手写固定十章剧情制造通过。
- [completed] 用 `config/default.yaml` 的 SHORT=12 做跨家族配置 horizon 纵切，生成 13 个 generic signatures（当前章节 14）并记录来源/结果。
- [completed] 沿用并明确引用既有匿名盲读报告；本轮没有伪造新的盲读结论。

### Phase 7 — Verification and delivery

- [completed] 在 `progress.md` 记录每项检查的具体失败目标与失败后的下一步，并运行新增定向测试、完整 pytest、mypy、compileall、修改文件 Ruff 和 browser smoke。
- [completed] 完成防过拟合搜索：故事专有词、固定章节窗口、当前 book id；剩余命中均有明确范围解释。
- [completed] 分离代码与实验工件提交；逐提交验证只含本轮归属；创建/切换目标分支前确认不会覆盖 dirty 内容。
- [completed] 核对 remote、branch、commits、merge-base、working tree、测试证据，形成最终报告；未满足完成条件不得宣称完成。

## Acceptance gates

1. 生产代码/config/template 不含当前实验故事特例，章节 horizon 不由固定章数硬编码。
2. Reader-visible continuity、usage constraints、progression delta 和 experience portfolio 均跨至少三类 fixture 工作。
3. Python 不伪造人物/文风语义评分；thin 不污染健康基线；Reference 区分 offered/applied。
4. Original 第一章与后续章节批准共享非阻塞语义，stale bundle 仍被服务端拒绝。
5. 当前 Seed 改善来自通用 Candidate/Contract/Validator，而不是手写固定剧情；跨家族纵切通过。
6. 所有必需验证有真实命令输出；既有失败准确归因；代码与实验工件分离提交。

## Errors encountered

| Error | Attempt | Resolution |
|---|---:|---|
| `create_goal` 首次调用发现线程已有“读取 pasted text”未完成目标 | 1 | 读取目标状态；目标已完成后创建本轮实际目标 |
| 当前工作树存在大量预先 dirty/untracked 内容且根文档在工作树中被删除 | 1 | 暂不覆盖或清理；从现状和 Git 历史/分支审计，计划单独落在本轮目录 |

## Current status

Phase 7 delivery complete. 代码与测试提交、审计/规划工件提交、目标分支 push 和最终 dirty-worktree/ancestry 报告均已完成；工作树中未暂存内容均为本轮前已存在或独立实验产物。
