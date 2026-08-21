# Author Workspace UI V1

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
- 章节写作：章节选择、当前小纲/正文主体、一个主生成或保存动作；原始上下文和执行节点进入高级详情。
- 记忆：Canon Memory / Current State 默认阅读态，复用 BOOK status 保存路径。
- 工具：Prompt Templates、OpenAI Settings、References、Workflow Debug。

## 高级透明性

右侧 Drawer 按需打开，复用现有 DOM 编辑器和输出区，不创建第二份内容来源；可查看完整 Prompt、Codex Response、Run Ledger、Dependency Impact、revision/source/file path、Hybrid 节点和 State Delta。

## 不变约束

- 不修改任何生成 Prompt、Workflow dependency/stale 语义、Run Ledger、Writer Mode、Executor 后端语义或小说文件格式。
- 不自动保存、不自动批准、不自动重跑 stale；真实保存仍走现有 API。
- Manual、Codex External、OpenAI API 只改变 Response 产生方式，共享同一 Prompt、Apply、Save 和 Workflow State。
- 本轮不生成新章节、不运行小说质量实验。

