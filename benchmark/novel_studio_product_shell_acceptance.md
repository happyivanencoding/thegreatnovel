# Novel Studio Product Shell Consolidation 验收报告

验收日期：2026-08-11

分支：`小说续写_codex`

真实书库：`cable-survival-blind-50` / `base`
Web：`http://127.0.0.1:8766`

## 结论

~~通过~~（**已于 2026-08-11 复审修订**）。

> 修订后结论：~~**Shell 自身验收项（A–M）维持通过；但全站页面渲染路径曾被 readiness 崩溃 live blocker 波及（在存在初始化中书的书库中 Shell 页面亦会 400），且初始化交接指令链路存在缺陷。两缺陷修复已合入工作树且自动测试通过；端到端浏览器复验与真实 Codex 初始化证据：进行中（待补）。**~~（**已于 2026-08-11 证据回填后再次更新**）
>
> 最终结论（2026-08-11 证据回填后）：**通过（含 2026-08-11 修复与真实端到端证据）**：Shell 自身验收项（A–M）维持通过；blocker S-1/S-2/S-3 已全部解除（逐条状态与证据出处见文末“Blocker 清单与解除状态”），共享渲染路径与任务中心指令复制链路的真实浏览器端到端复验（PASS）及真实语义执行证据已回填。关键限定：本次真实语义执行的执行主体为开发代理在 Codex 桌面端合同下按 skill 执行，非作者手工操作的 Codex 桌面端会话，不得称为“作者侧 Codex 桌面端执行”。详见文末“2026-08-11 复审修订”章节。

作者现在从单一“小说工作台”完成章节阅读、历史世界状态查询、续写、改写、后续规划、全书画像和任务恢复；原有 Handoff、Jobs、API、审批与 Canon 边界继续保留，但不再作为主导航暴露给作者。

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

- `uv run --no-sync pytest -q`：187 passed，192.76s。（本报告初次验收时的数字；2026-08-11 缺陷修复后全量回归为 **210 passed**，见复审章节）
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

## 2026-08-11 复审修订

### 修订原因

同日 Library Onboarding 验收复审确认了两个真实缺陷（均有真实 HTTP 响应与 traceback 证据），本报告需复查其“通过”结论是否受波及：

1. **缺陷 1（交接指令路径）**：legacy migrate 导入书的 `NOVEL_INITIALIZATION` handoff `prompt_path` 缺 `input/` 段，`copy_instruction` 抛 `FileNotFoundError`，instruction endpoint 返回 HTTP 400 `WORKFLOW_ERROR`，前端显示“无法读取交接指令”（真实复现：`cable-survival-demo`）。Shell 的任务中心与 Handoff 指令复制入口复用同一链路，故受影响。
2. **缺陷 2（readiness 崩溃）**：`library_catalog.py` 对字符串 readiness（`"BLOCKED"`）做 `dict()` 崩溃，导致所有 HTML 页面与 catalog API 400（真实复现：`book-6k-0lnr4da` 初始化写入后全页面 400）。**Shell 全部页面均消费 Catalog（书籍选择器/任务中心），只要书库中存在一本初始化中的书，Shell 界面即整体不可用**，A–M 验收项全部受波及。

两缺陷均已在本会话修复并合入工作树，全量回归通过；但真实浏览器端到端复验与真实 Codex 初始化证据仍在补齐中。

### 对本报告结论的影响重评

- 初次验收当时（书库中无字符串 readiness 书、未触发 legacy 指令链路），A–M 的浏览器观察真实成立，逐项结果维持；
- 但“通过”作为终验收结论**不再成立**：缺陷 2 属于全站渲染级 live blocker，缺陷 1 属于 Shell 任务中心指令复制链路的 live blocker；
- 修订后结论：**Shell 功能验收项维持，但整体结论降级为“修复已落地，自动测试证据充分；端到端/真实 Codex 证据：进行中（待补）”。**

### 证据四分类（截至 2026-08-11，2026-08-11 证据回填后更新）

**a) 自动测试证据（已有）**

- 本报告初次验收时：`uv run --no-sync pytest -q` 187 passed；ruff/mypy/compileall/web doctor 均通过。
- 缺陷修复后：新增回归 `uv run --no-sync pytest -q tests/integration/test_handoff_instruction_reliability.py` **14 passed**（含字符串 readiness 不崩溃、指令回退解析与结构化错误、前端错误透传契约）；全量回归 **210 passed**；ruff、mypy、compileall、node --check、web doctor 均通过。
- 局限：进程内/TestClient 级验证，不覆盖真实浏览器行为。

**b) 真实浏览器证据（初次验收已有；2026-08-11 修复后端到端证据已回填，PASS）**

- 已有：初次验收的 11 张截图（`artifacts/novel_studio_shell/01–11`）与 A–M 真实浏览器操作记录（书 `cable-survival-blind-50`/`base`）。
- 2026-08-11 回填（PASS，截图目录 `artifacts/acceptance-browser/20260811-init-handoff/`，step1–step6 共 7 张，与 Library Onboarding 报告 L-1/L-3 同一证据源）：在真实书库（含初始化中书与字符串 readiness 存量书）中，Library 页、任务中心（NOVEL_INITIALIZATION 条目）与指令复制链路端到端正常：GET instruction 200、content-length=1083，剪贴板 723 字符与服务端 `body.instruction` 逐字相同（CRLF 归一化后），含 `$process-novel-handoff`/`$initialize-existing-novel`，页面反馈“给 Codex 的真实初始化指令已复制。”；静态资源全部 `?v=3.3.0`。Shell 任务中心与指令复制入口复用同一链路，即本报告 S-1/S-2 波及路径的端到端复验。
- 存量修复佐证：`cable-survival-demo` 失效 `prompt_path` 行经 `copy_instruction` 回退读取成功并自动回写 DB（instruction_available=true）。

**c) 真实语义执行证据（2026-08-11 已回填；非 fixture；执行主体限定如实标注）**

- 2026-08-11 回填（与 Library Onboarding 报告 L-2 同一证据源）：`handoff_c3582f9ea417a15da6c7d45b` 被真实领取处理，按 `.agents/skills/process-novel-handoff` 与 `initialize-existing-novel` 完整执行 Atlas-first 流水线至严格 READY：`result.json` status=COMPLETED、readiness=READY、canon_committed=false、edition_activated=false；`novel workflow validate-result` 通过；catalog API 最终 `book-qombhi5tza` state=READY、studio_ready=true、primary_action=OPEN_STUDIO。
- 执行主体限定（如实标注）：本次语义执行由开发代理在 Codex 桌面端合同下按 skill 执行——非合同 fixture，但执行主体不是作者手工操作的 Codex 桌面端会话，**不得称为“作者侧 Codex 桌面端执行”**。
- 本报告 D 项创建的第 31 章续写 Handoff 仍仅到“等待 AI 处理”，未发生真实 Codex 处理。

**d) 合同 fixture 证据（间接，明确局限）**

- 本报告自身未依赖 fixture；但同日 Library Onboarding 报告的 READY 验收使用合同 fixture，其结论不传导为本报告的真实初始化证据。
- 局限：fixture 只验证边界契约，不得称为真实 Codex 初始化。

**声明：不得把 fixture 称为真实 Codex 初始化。本次回填的真实语义执行虽非 fixture，但执行主体为开发代理（Codex 桌面端合同下按 skill 执行），不等同于作者侧 Codex 桌面端执行，二者如实区分。**

### Blocker 清单与解除状态（2026-08-11 证据回填后更新）

| ID | Blocker | 解除状态 | 证据出处 |
|---|---|---|---|
| S-1 | readiness 崩溃波及 Shell 全页面渲染的端到端复验 | **已解除（2026-08-11）** | 证据 b)：`artifacts/acceptance-browser/20260811-init-handoff/` step1–step6；真实书库（含初始化中书与字符串 readiness 存量书）中 Library 页、任务中心、指令复制链路端到端正常、无 400；Shell 共享同一 Catalog/渲染路径 |
| S-2 | 任务中心交接指令复制链路（legacy migrate 书）端到端复验 | **已解除（2026-08-11）** | 证据 b)：step5 复制指令端到端成功（GET 200、content-length=1083，剪贴板 723 字符与服务端 instruction 逐字相同，含 `$process-novel-handoff`/`$initialize-existing-novel`）；存量修复佐证：`cable-survival-demo` 失效 `prompt_path` 行经回退读取成功并自动回写 DB（instruction_available=true） |
| S-3 | 无真实 Codex 处理 handoff 至 READY 的证据 | **已解除（2026-08-11，含执行主体限定）** | 证据 c)：与 Library Onboarding 报告 L-2 同一证据源（`handoff_c3582f9ea417a15da6c7d45b` 真实语义执行至严格 READY）；执行主体为开发代理（非作者手工 Codex 桌面端会话），如实标注 |

**S-1、S-2、S-3 已全部解除。**

### 证据回填（2026-08-11）

本节在保留上方复审修订全部历史记录的前提下，回填新证据（详见“证据四分类”b/c 两节与上方解除状态表）：

1. **真实浏览器端到端证据（PASS）**：截图目录 `artifacts/acceptance-browser/20260811-init-handoff/`（step1 至 step6 共 7 张），覆盖 S-1（共享渲染路径）与 S-2（指令复制链路）的解除条件。
2. **真实语义执行证据（非 fixture）**：`handoff_c3582f9ea417a15da6c7d45b` 完整执行 Atlas-first 初始化流水线至严格 READY，解除 S-3（与 L-2 同一证据源）；执行主体为开发代理在 Codex 桌面端合同下按 skill 执行，不得称为“作者侧 Codex 桌面端执行”。
3. **存量修复佐证**：`cable-survival-demo` 失效 `prompt_path` 行经 `copy_instruction` 回退读取成功并自动回写 DB（instruction_available=true）。

### 最终结论（2026-08-11 证据回填后）

**通过（含 2026-08-11 修复与真实端到端证据）。** Shell 自身验收项（A–M）维持通过；S-1/S-2/S-3 blocker 全部解除，共享渲染路径与任务中心指令复制链路的真实浏览器端到端复验（PASS）及真实语义执行证据齐备。限定性说明：本次真实语义执行由开发代理在 Codex 桌面端合同下按 skill 执行，非作者手工操作的 Codex 桌面端会话，本报告不声称“作者侧 Codex 桌面端执行”已完成；合同 fixture 仍不构成真实 Codex 初始化证据。
