# Chapter Run Ledger

Ledger 是每章固定节点的文件记录，不是后台调度器或通用 Workflow Engine。

## 固定节点

`director → curator → primary → opening / dialogue / action / emotion → integrator → state_delta`

每章目录为 `books/<book_id>/runs/chapter-NNNN/`，保存 `manifest.json`、节点 Prompt、节点 Response 和作者显式采用的最终来源记录。未选专项标为 `skipped`，不生成假 Response。

## 状态与恢复

节点状态只有 `pending`、`completed`、`failed`、`skipped`、`stale`、`adopted`。失败节点重试时复用已保存 Prompt、attempts 加一，不重跑上游；旧 Response 文件保留为历史产物。上游内容变化只让真实依赖下游变为 `stale`。

如果所有已运行专项都没有有效 `## Patch N`，Integrator 标记 `skipped`，Primary 可以由作者显式采用；Integrator 没有拒绝 Primary 或自动写章的权力。

Ledger 不写 BOOK、不写正式章节、不调用 Agent、不使用数据库、队列、事件总线、DAG 编辑器、哈希或校验和。
