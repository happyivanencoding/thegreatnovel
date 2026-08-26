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

- 创意：三阶段 Stepper；默认阅读态，编辑/生成/批准按阶段展开；GBrain/References 折叠。
- 故事设计：总体设计 / 中期规划 / 未来十章 Tabs；section cards 默认阅读态，原文编辑显式打开。
- 章节写作：章节选择、当前小纲/正文主体、一个主生成或保存动作；所有开书叙事形式都从 Chapter 1 进入正常 Director → Curator → Writer → State 链，原始上下文和执行节点进入高级详情。
- 记忆：Canon Memory / Current State 默认阅读态，复用 BOOK status 保存路径。
- 工具：Prompt Templates、OpenAI Settings、References、Workflow Debug。

章节主 CTA 由 Workflow snapshot 的 `next_actionable_node` 驱动：继续写作会自动选择当前章节、载入可用的十章计划，并将 Director / 执行小纲 / 正文 / Hybrid 节点映射到作者可读的中文动作；Prompt Mode、完整 Prompt、Response 和 Codex Task 仅在右侧 Drawer 可见。

Future 10 和记忆保留显式编辑入口；保存仍统一走 BOOK 保存路径，stale / Impact 由现有 Workflow State 计算。小于 800px 时左侧导航转为顶部横向导航，右侧 Drawer 覆盖打开且页面不产生横向溢出。

## 高级透明性

右侧 Drawer 按需打开，复用现有 DOM 编辑器和输出区，不创建第二份内容来源；可查看完整 Prompt、Codex Response、Run Ledger、Dependency Impact、revision/source/file path、Hybrid 节点和 State Delta。

## 不变约束

- 不修改任何生成 Prompt、Workflow dependency/stale 语义、Run Ledger、Writer Mode、Executor 后端语义或小说文件格式。
- 不自动保存、不自动批准、不自动重跑 stale；真实保存仍走现有 API。
- Manual、Codex External、OpenAI API 只改变 Response 产生方式，共享同一 Prompt、Apply、Save 和 Workflow State。
- 本轮不生成新章节、不运行小说质量实验。

## 浏览器证据

1440×900 的冻结基线与当前 Author Workspace 截图保存在 `docs/ui-audit/`：`before.png`、`after-overview.png`、`after-chapter.png`、`after-design.png`。
