# Novel Studio Product Shell Consolidation 验收报告

验收日期：2026-08-11

分支：`小说续写_codex`

真实书库：`cable-survival-blind-50` / `base`
Web：`http://127.0.0.1:8766`

## 结论

通过。作者现在从单一“小说工作台”完成章节阅读、历史世界状态查询、续写、改写、后续规划、全书画像和任务恢复；原有 Handoff、Jobs、API、审批与 Canon 边界继续保留，但不再作为主导航暴露给作者。

## A–M 浏览器验收

| 项目 | 结果 | 真实浏览器证据 |
|---|---|---|
| A. 单一作者工作台 | 通过 | 顶栏显示第50章、续写下一章、改写本章、规划后续和任务入口；没有工作流/任务交接主导航。见 `01-studio-home.png`。 |
| B. 章节上下文贯穿视图 | 通过 | 从第30章背包切到主题画像，再切到关系，URL 与页面上下文始终锚定第30章。见 `02-world-state-chapter30.png`、`03-profile-chapter-anchor-preserved.png`。 |
| C. 续写动作空间 | 通过 | 第30章点击续写后在同一壳中显示“续写 · 第31章”和作者步骤条。见 `04-continuation-action-workspace.png`。 |
| D. 创建续写任务 | 通过 | 创建第31章续写 Handoff 后，任务中心显示“第31章续写 · 等待 AI 处理”。见 `05-activity-center-running.png`。 |
| E. 从任务恢复 | 通过 | 点击运行中活动返回 `action=continue`、第30章锚点和“续写 · 第31章”工作区，没有跳到 Jobs。 |
| F. Hydration 活动 | 通过 | 四个历史 Hydration Handoff 聚合为一个“世界状态补齐 · 50/50章 · 100%”完成活动。见 `06-activity-center-completed.png`。 |
| G. 剧情任务与系统活动分层 | 通过 | `AUTHOR_TASK`“获得长枪”显示在作者规划卡；世界状态补齐、续写 Handoff 等只显示在任务中心。见 `07-narrative-task-vs-system-activity.png`。 |
| H. 统一章节状态视图 | 通过 | 中心、右栏均使用第30章 `ChapterWorldStateView`，没有暴露 `SOURCE_STATE_MISSING` 等原始状态码。见 `08-unified-right-chapter-state.png`。 |
| I. 左栏滚动保持 | 通过 | 左栏下滚后连续点击背包、装备、能力、知识、地点、势力、关系、规则、任务和三项画像，共12次；每次滚动位置均大于0且章节仍为第30章。见 `10-sidebar-scroll-preserved.png`。 |
| J. 浏览器历史恢复 | 通过 | 后退/前进恢复第30/31章、关系/主题画像、正文/章末状态子视图、左栏滚动位置及右栏折叠/展开状态。 |
| K. 技术详情分层 | 通过 | 任务中心默认不显示 `READY_FOR_CODEX`、`task_directory`、`CLAIMED`；展开“技术详情”后可见底层字段。 |
| L. Add Item CURRENT | 通过 | `A17Pro芯片`返回“已存在”并打开证据检查器；不存在物品返回“没有当前证据”，仅提供“未来获得 / 创建改写 / 取消”，没有发送 `DROP_ITEM`。 |
| M. 候选可读性 | 通过 | 第50章只读取绑定到第51章的三候选，并以目标、状态变化、隐藏真相、揭示安排、画像对齐和硬约束展示，无原始 JSON。见 `11-candidate-human-readable.png`。 |

## 截图清单

截图位于 `benchmark/artifacts/novel_studio_shell/`：

1. `01-studio-home.png`
2. `02-world-state-chapter30.png`
3. `03-profile-chapter-anchor-preserved.png`
4. `04-continuation-action-workspace.png`
5. `05-activity-center-running.png`
6. `06-activity-center-completed.png`
7. `07-narrative-task-vs-system-activity.png`
8. `08-unified-right-chapter-state.png`
9. `09-continuity-unified-world-state.png`
10. `10-sidebar-scroll-preserved.png`
11. `11-candidate-human-readable.png`

## 自动化门禁

- `uv run --no-sync pytest -q`：187 passed，192.76s。
- `uv run --no-sync ruff check src tests`：通过。
- `uv run --no-sync mypy src`：147 个源文件通过。
- `uv run --no-sync python -m compileall -q src`：通过。
- `uv run --no-sync novel web doctor`：健康检查、必需路由、模板和静态资源均通过。
- Legacy `/books/cable-survival-blind-50/workflow`：302 到 canonical workbench，并保留 edition、chapter 和 action。

## 数据与权限边界

- 未修改 `book/` 原文或 Canon。
- 浏览器验收只新增规划层数据：一个第31章续写 Handoff，以及一个 `AUTHOR_TASK`“获得长枪”。
- CURRENT 物品查询只读取第30章背包与装备；缺失物品不会直接写入当前世界状态。
- Activity Center 复用现有 Handoff 与系统任务记录，没有新增任务数据库。
