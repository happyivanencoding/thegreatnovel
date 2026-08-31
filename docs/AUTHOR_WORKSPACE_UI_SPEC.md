# Author Workspace UI V1

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义 Author Workspace 的 UI 信息架构与交互语义。

## 现有真实入口

- `index.html` 当前是一张长页面：创意、BOOK 设计、规划、GBrain、References、Prompt、Hybrid Run、章节输入、正文、State Delta、Prompt Templates 全部同屏。
- `app.js` 的保存真源保持不变：`saveCreativeArtifact`、`saveBook`、`approveChapter`、`saveRunPromptForMode`、`saveRunResponseForMode`、`applyCanonIndexProposal`。
- 后端真源保持不变：`/api/books/{book_id}`、`/api/prompt`、章节与 Run Ledger API、`/api/books/{book_id}/workflow`、Impact、Executors、OpenAI Settings。

## 新信息架构

左侧导航使用 hash view：

```text
概览 · 创意 · 故事设计 · 章节写作 · 记忆 · 工具
```

默认概览只显示当前书、当前章节、下一步、stale 摘要、继续写作主 CTA 和轻量 Story Flow；不放大 textarea。

- 创意：可选 Premise Aperture + World / Character / Story 三个 Authority 阶段；默认阅读态，编辑/生成/批准按阶段展开；GBrain/References 折叠。
- 故事设计：总体设计 / 中期规划 / 未来十章 Tabs；section cards 默认阅读态，原文编辑显式打开。
- 章节写作：生产正文改为 4—6 章 Batch（默认5）：已批准 Future-10 直接形成 deterministic Batch Packet → Terra Batch Primary → Sol Authority Delta → 整批采用 → State 逐章落盘。当前旧单章 Director → Curator → Primary → Full Reviser 界面保留为 fallback / 高级详情；本轮没有新增 Batch 专用视觉工作区，产品层若后续暴露 Batch 操作，应复用同一章节阅读态与高级详情，不把 Authority patch 变成作者必须逐条管理的主界面。
- 记忆：Canon Memory / Current State 默认阅读态，复用 BOOK status 保存路径。State Delta 应用到浏览器状态编辑区时，`Current Power Position` 不允许因模型漏写而消失：已有 Canon 位置优先继承；第一章尚无 Canon 时从 `CHARACTER.md` 的 T0 `开局精确力量位置` 确定性转成 Current Position。只有 State 返回了新的明确数字位置时才覆盖；越级胜利本身不触发 UI 推断升级。
- 工具：Prompt Templates、OpenAI Settings、References、Workflow Debug。

Premise 工作区固定提供：Forge Prompt、三卡保存、batch Compiler、作者选择/编辑、selected-card Compiler、Report 保存、批准与显式跳过。UI 不出现自动 selector 或 Repair 按钮。候选和 Compiler Report 只在该工作区可见；批准后显示四条只读 lane contract，Workflow 只登记正式 `premise.contract`。从未开始/已跳过不阻止 World；开始未批准时 World / Power / Human / Story 的生成与保存显示后端 fail-loud 错误；World 批准后 Premise 控件不可再改变事实。

章节主 CTA 由 Workflow snapshot 的 `next_actionable_node` 驱动：继续写作会自动选择当前章节、载入可用的十章计划，并将 Director / 执行小纲 / 正文 / Hybrid 节点映射到作者可读的中文动作；Prompt Mode、完整 Prompt、Response 和 Codex Task 仅在右侧 Drawer 可见。

Future 10 和记忆保留显式编辑入口；保存仍统一走 BOOK 保存路径，stale / Impact 由现有 Workflow State 计算。小于 800px 时左侧导航转为顶部横向导航，右侧 Drawer 覆盖打开且页面不产生横向溢出。

## 高级透明性

右侧 Drawer 按需打开，复用现有 DOM 编辑器和输出区，不创建第二份内容来源；可查看完整 Prompt、Codex Response、Run Ledger、Dependency Impact、revision/source/file path、Primary / Authority Reviser / optional repair 节点和 State Delta。Authority Reviser 卡固定标示 `GPT-5.6 Luna · high`；`curator_primary` 下 Primary 只作为第一版草稿，必须采用 Authority Revision 后才能进入 State。若 Run Ledger 检测到当前章已批准的显式力量/身份里程碑仍未在 Authority Revision 中直接落成，该 Reviser 节点显示 failed 并准备一次窄 `Outcome Repair`；用户点击同一节点“重试节点”时 UI 直接加载后端保存的 repair Prompt，OpenAI executor 可立即执行，Codex External 使用同一保存 Prompt。repair 通过前不能采用正文或进入 State。

## 不变约束

- UI 不另造生成/保存语义；Workflow dependency、Run Ledger 与 Executor 的真实语义由 production runtime 决定。当前 `curator_primary` 已包含固定 Authority Reviser；其它 writer mode 保持兼容行为。
- 不自动保存、不自动批准、不自动重跑 stale；真实保存仍走现有 API。
- Manual、Codex External、OpenAI API 只改变 Response 产生方式，共享同一 Prompt、Apply、Save 和 Workflow State。
- 本轮不生成新章节、不运行小说质量实验。

## 浏览器证据

1440×900 的冻结基线与当前 Author Workspace 截图保存在 `docs/ui-audit/`：`before.png`、`after-overview.png`、`after-chapter.png`、`after-design.png`。
