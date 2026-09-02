# Author Workspace UI V2

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义 Author Workspace 的 UI 信息架构与交互语义。

## 现有真实入口

- `index.html` 使用沉浸式私人创作舱：浮动项目栏、窄导航 rail、阅读优先的正文工作区，以及桌面常驻/小屏覆盖的 AgentDock 创作中枢。旧编辑器仍只有一份，按 hash view 与高级区呈现。
- `app.js` 的保存真源保持不变：`saveCreativeArtifact`、`saveBook`、`approveChapter`、`saveRunPromptForMode`、`saveRunResponseForMode`、`applyCanonIndexProposal`。
- 后端真源保持不变：`/api/books/{book_id}`、`/api/prompt`、章节与 Run Ledger API、`/api/books/{book_id}/workflow`、Impact、Executors、OpenAI Settings；AgentDock 仅增加独立的内存作业 API，不写任何 Authority artifact。

## 新信息架构

左侧导航仍使用 hash view：

```text
概览 · 创意 · 故事设计 · 章节写作 · 记忆 · 工具
```

默认概览只显示当前书、当前章节、下一步、stale 摘要、继续写作主 CTA 和轻量 Story Flow；不放大 textarea。

- 创意：可选 Premise Aperture + World / Character / Story 三个 Authority 阶段；默认阅读态，编辑/生成/批准按阶段展开；GBrain/References 折叠。
- 故事设计：总体设计 / 中期规划 / 未来十章 Tabs；section cards 默认阅读态，原文编辑显式打开。
- 章节写作：production 默认是 4—6 章 Batch（默认 5）：已批准 Future-10 → deterministic Batch Packet → Terra Batch Primary → Sol Authority Delta → 作者显式整批采用 → State 逐章落盘。正文阅读/编辑区优先；Workflow / Run Ledger 继续显示正式 artifact 状态，AgentDock 作业与 Batch 本地状态独立显示，绝不伪装成已保存节点。旧单章 Director → Curator → Primary → Full Reviser 只保留为 fallback / 高级详情。
- 记忆：Canon Memory / Current State 默认阅读态，复用 BOOK status 保存路径。State Delta 应用到浏览器状态编辑区时，`Current Power Position` 不允许因模型漏写而消失：已有 Canon 位置优先继承；第一章尚无 Canon 时从 `CHARACTER.md` 的 T0 `开局精确力量位置` 确定性转成 Current Position。只有 State 返回了新的明确数字位置时才覆盖；越级胜利本身不触发 UI 推断升级。
- 工具：Prompt Templates、OpenAI Settings、References、Workflow Debug。

Premise 工作区固定提供：Forge Prompt、三卡保存、batch Compiler、作者选择/编辑、selected-card Compiler、Report 保存、批准与显式跳过。UI 不出现自动 selector 或 Repair 按钮。候选和 Compiler Report 只在该工作区可见；批准后显示四条只读 lane contract，Workflow 只登记正式 `premise.contract`。从未开始/已跳过不阻止 World；开始未批准时 World / Power / Human / Story 的生成与保存显示后端 fail-loud 错误；World 批准后 Premise 控件不可再改变事实。

章节主 CTA 由 Workflow snapshot 的 `next_actionable_node` 驱动：继续写作会自动选择当前章节、载入可用的十章计划，并将 Director / 执行小纲 / 正文 / Hybrid 节点映射到作者可读的中文动作；Prompt Mode、完整 Prompt、Response 和 Codex Task 仅在右侧 Drawer 可见。

Future 10 和记忆保留显式编辑入口；保存仍统一走 BOOK 保存路径，stale / Impact 由现有 Workflow State 计算。小于 800px 时左侧导航转为顶部横向导航，右侧 Drawer 覆盖打开且页面不产生横向溢出。

## 高级透明性

右侧 AgentDock 创作中枢在桌面常驻、小屏作为覆盖 Drawer，复用现有 DOM 编辑器和输出区，不创建第二份内容来源；可查看完整 Prompt、Response、Run Ledger、Dependency Impact、revision/source/file path、Primary / Authority Delta / optional repair 节点和 State。节点状态只来自真实 Workflow / Run Ledger；ACP 作业状态（queued/running/completed/failed/cancelled、模型、耗时、结果）独立显示，不伪装成 artifact。

`agentdock_acp` 由后端可信配置解析本机 ACP，优先运维环境变量、再 PATH、最后固定 npm fallback；浏览器不能提交 executable、cwd、mode 或 MCP。后端固定项目 cwd、空 MCP、read-only mode、模型/推理白名单、短控制 RPC deadline + 长生成 job deadline、后台 stdout/stderr drain、有界 pending queue / output / completed history，以及 terminate → wait → kill 清理。`read-only` 表示 Agent 可读取项目上下文但不能写入小说或 Workflow；status 不返回本机路径。

每次启动均冻结 `book_id + chapter_number + workflow_mode + launch_token`。自动回填还必须满足：当前 identity 完全一致、仍是该 response target 的最新启动、页面仍保有本次 launch snapshot、且目标 Response 的单调编辑版本自启动后没有变化；因此作者即使改过后又撤回到原文本，旧 Agent 结果也不会自动覆盖。页面刷新只恢复 queued/running 轮询，不自动回填旧作业；错位、过期、作者已编辑或服务重启丢失的结果只能标记“待查看”。列表只返回 summary/`has_output`，点击后才 GET 全文；身份匹配时仍需作者显式确认载入，随后继续显式 Apply / Save / Approve。咨询遵守同样的最新启动与编辑保护，且不会写入小说或工作流。

右侧 Batch Production 是 production 默认的真实控制面：作者选择任意起始章和 4—6 章窗口（默认 5），前两章连续性上下文由既有章节 API 确定性读取，再依次调用现有 `primary-prompt`、AgentDock Terra high `batch_primary`、`authority-reviser-prompt`、AgentDock Sol high `batch_authority_reviser`、`apply-authority-delta` 预检，最后才可显式调用 `adopt-authority-delta`。Primary / Delta 都有专属 Response，不混入单章或 State Response。窗口、Primary 或 Delta 变化会清空 / 标记其下游 Prompt 与 exact-response 预检 stale；upstream conflict、已有章节、解析失败或 stale 预检都禁止采用。采用后只显示 `state_next`，载入真实章节正文并引导作者逐章 State Extraction，绝不自动写 Canon。

## 不变约束

- UI 不另造生成/保存语义；Workflow dependency、Run Ledger 与 Executor 的真实语义由 production runtime 决定。当前 `curator_primary` 已包含固定 Authority Reviser；其它 writer mode 保持兼容行为。
- 不自动保存、不自动批准、不自动重跑 stale；真实保存仍走现有 API。
- Manual、Codex External、OpenAI API、AgentDock ACP 只改变 Response 产生方式，共享同一 Prompt、Apply、Save 和 Workflow State；AgentDock 不允许执行外部 CLI apply。
- 本轮不生成新章节、不运行小说质量实验。

## 浏览器证据

冻结基线保留为 `before.png`；当前 V2 证据为 `workspace-v2-light.png`、`workspace-v2-dark.png` 与 `workspace-v2-mobile.png`。浏览器 smoke 同时验证 1440×900 亮/暗模式，以及 390×844 下 `document.scrollWidth == clientWidth`、单一 active nav 和 390px 覆盖式 AgentDock drawer。
