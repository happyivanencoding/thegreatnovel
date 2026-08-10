# Story Game State V2.1 验收报告

验收日期：2026-08-10

开发分支：`小说续写_codex`

本轮真实 Web：`http://127.0.0.1:8766`

真实书库 session：`cable-survival-blind-50`
数据库：`library/cable-survival-blind-50/_system/state.sqlite3`

## 1. 真实 50 章验收

真实章节数为 50。实际打开并检查了第 10、30、50 章的 Workbench 状态页；三个时间点不是同一个 latest baseline 的复制品：

| 时间点 | 角色记录 | 当前背包 / 资源 | 能力 | 知识 / 矩阵 | 结论 |
| --- | ---: | --- | --- | --- | --- |
| 第 10 章《降溫》 | 2 | `棉被` | 0 | 2 个矩阵单元：苏牧 `SUSPECTED`，林雨薇 `UNKNOWN` | hydration 完成后显示本章 Source State |
| 第 30 章《這是人能做到的？》 | 2 | `棉被` | 0 | 2 个矩阵单元 | 没有倒灌第 50 章的武器/能力 |
| 第 50 章《削的木箭》 | 2 | `M500转轮手枪`、`槍豪职业技能书`、`9mm子弹制作图纸` | `额外攻击`、`分解规则的隐藏用法` | 2 个矩阵单元，另有 2 条已确认知识记录 | 边界状态显示真实可追溯资料 |

重点历史检查：第 10、30 章没有 `M500转轮手枪` 或第 50 章的能力；第 50 章才显示它们为原文已确认。第 10 章的 `棉被` 来自当前章节 source span，不是由第 50 章 baseline 回填。

## 2. 真实 SOURCE_STATE_HYDRATION 闭环

从第 10 章页面点击“准备本章状态任务”，实际生成并领取 handoff，读取 `hydration_context.json`，将结构化结果写入 `result.json`，再从 Web 点击“收集结果”。没有直接人工调用 `record_source_chapter_deltas()` 写入真实验收结果。

| 项目 | 结果 |
| --- | --- |
| handoff | `handoff_269c440f1303b0b4cad67293` |
| 类型 / 状态 | `SOURCE_STATE_HYDRATION` / `COMPLETED` |
| 关联 Author Task | `task-6a12a4cf08dd40cf9782af8fbb544d59` |
| 关联任务最终状态 | `DONE` |
| 章节 | 第 10 章，`chapter_a5d622fc3e59f58c7b6aca2b` |
| 导入 Delta | 2 |
| `SOURCE_VERIFIED` Delta | 2 |
| 本章不确定发现 | 1 |
| 实际 state keys | `item:cotton-blanket`、`knowledge:character:su-mu:lin-yu-wei-suspicion` |
| 拒绝数 | 0；另有集成测试覆盖跨章节 evidence 的拒绝路径 |

真实页面刷新后的可见结果为“原文状态（部分） / 原文已确认”，背包中显示“棉被”，并保留“当前事实”和“计划物品”的边界。

## 3. Source State / Canon 安全边界

- `events`：hydration 前 0，hydration 后 0。
- `canon_commits`：hydration 前 0，hydration 后 0。
- `book/` 与 source text：未修改。
- hydration 只写 Source State Ledger、snapshot cache、handoff/task 状态；不写 Canon Event Store、Canon Commit、Edition activation 或正文。
- Author Intent 与 Author Task 只进入作者控制层；当前背包、当前关系和当前能力没有被规划项覆盖。
- `source_state_snapshots` 是可删除重建的 projection cache，Ledger 才是事实来源。

## 4. 作者控制层真实浏览器操作

所有操作均从第 50 章 Workbench 的“状态”模式完成，并刷新页面复核：

| 类型 | ID | 最终结果 |
| --- | --- | --- |
| Future Item | `intent-085e60fc875642b3a587f4895483f490` | `测试长枪` / `MID` / `PLANNED`，只出现在“计划物品”，不进入当前背包 |
| Relationship Goal | `intent-31c4f42c4b094f808a8146587f4733dc` | 真实人物 `character:su-mu` ↔ `character:lin-yu-wei`，`MID`，当前关系仍为空 |
| Author Task | `task-039d11dd410c4dbabeb3c1e565bbc6a5` | `测试剧情任务`：`MID → SHORT`，刷新后仍为 `SHORT`；`BACKLOG → ACTIVE`，刷新后仍为 `ACTIVE` |

任务卡保留 HTML drag/drop 的 `MOVE_TASK_HORIZON` 路径，并增加同一 Author Command 的可访问跨度控件，确保键盘/浏览器自动化也能完成相同的规划层操作。任务移动和生命周期更新均未产生 Canon event。

## 5. 实现范围

- `source_state.py`：业务 `state_key`、`subject_id/object_id` 校验、ADD/ACQUIRE、LOSE/REMOVE、TRANSFER、EQUIP/UNEQUIP、UPDATE、LEARN、snapshot replay。
- `migration_11.py`：Source State Ledger 的 `state_key`、`source_state_snapshots` 表及索引。
- `workflows/handoffs.py`、`process-novel-handoff`、Web collect route：正式 `SOURCE_STATE_HYDRATION` Local File Handoff 闭环与确定性导入门。
- `projections.py`：历史 baseline mutable-state 隔离、Item/Knowledge/Relationship/Faction 结构化投影及 Character × Knowledge Topic 矩阵。
- Workbench：Item Inspector、Who Knows 矩阵、Relationship/Faction inspector、当前事实/作者计划分栏、任务板。
- Planning：`AuthorControlTrace` 与 Candidate Proposal 的 task/intent hit、advanced、unused reason 结构化合同。

## 6. 自动化与 Web 验证

| 检查 | 结果 |
| --- | --- |
| `uv run --no-sync pytest -q` | **170 passed** |
| `uv run --no-sync ruff check src tests` | **All checks passed** |
| `uv run --no-sync mypy src` | **Success: no issues found in 142 source files** |
| `python -m compileall -q src` | **passed** |
| CLI help：`novel`、`features`、`rhythm`、`hooks`、`metrics`、`segments`、`workflow` | **passed** |
| `uv run --no-sync novel web doctor` | **ok=true；routes/static/templates 全部通过** |
| localhost HTTP smoke | `/library`、真实 Workbench、`/jobs` 均 HTTP 200 |

## 7. 浏览器截图

截图保存在本地 `benchmark/artifacts/story_game_state_v2_1/`，未要求提交为 Git binary：

- `C:\dev\小说续写系统\benchmark\artifacts\story_game_state_v2_1\01-state-chapter50.png`
- `C:\dev\小说续写系统\benchmark\artifacts\story_game_state_v2_1\02-inventory-inspector-chapter50.png`
- `C:\dev\小说续写系统\benchmark\artifacts\story_game_state_v2_1\03-knowledge-matrix-chapter50.png`
- `C:\dev\小说续写系统\benchmark\artifacts\story_game_state_v2_1\04-relationship-goal-chapter50.png`
- `C:\dev\小说续写系统\benchmark\artifacts\story_game_state_v2_1\05-task-board-chapter50.png`
- `C:\dev\小说续写系统\benchmark\artifacts\story_game_state_v2_1\06-hydrated-chapter10.png`
