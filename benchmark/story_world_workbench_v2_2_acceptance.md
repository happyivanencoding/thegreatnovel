# Story World Workbench V2.2 验收报告

验收日期：2026-08-10

开发分支：`小说续写_codex`

真实 Web：`http://127.0.0.1:8766`

真实书库 session：`cable-survival-blind-50`

真实数据库：`library/cable-survival-blind-50/_system/state.sqlite3`

## 验收结论

V2.2 已在真实 50 章 session 上完成端到端闭环：章节时间旅行、全书 Source State hydration、九维 Global Book Profile、Profile 到三候选的硬门、状态对象 Inspector、知识矩阵、关系网络、作者任务和可折叠三栏均已在实际 Web 中验证。

本轮只完成 `PLAN_ONLY`：3 个候选已生成并导入，未生成 Chapter Contract 或草稿，未写入 Canon，未启用 Edition。

## 1. 章节时间旅行不是 latest-state 复制

选择人物 `苏牧` 后，第 10、30、50 章实际投影如下：

| 章后时间点 | 人物 | 地点 | 背包 | 装备 | 资源 | 能力 | 知识主题 | 关系 | 世界规则 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 第 10 章 | 3 | 1 | 11 | 5 | 3 | 2 | 24 | 0 | 5 |
| 第 30 章 | 3 | 1 | 48 | 16 | 27 | 6 | 80 | 1 | 5 |
| 第 50 章 | 4 | 3 | 68 | 19 | 31 | 6 | 112 | 3 | 6 |

三个时间点的物品、能力、知识与关系均来自截至该章的 Source State replay。切回旧章不会看到后续章节才出现的状态；切回第 50 章会恢复完整的当前截面。

特别更正：M500 不是第 50 章新获得物品。全书 hydration 确认它在第 6 章首次获得、首次确认，第 33 章最近再次确认，因此第 10、30、50 章都应可见。系统现按真实来源展示，没有采用需求文档中的示意时间点。

## 2. 全书 hydration 与 coverage

| 项目 | 实际结果 |
| --- | --- |
| 章节 coverage | 50/50，100% |
| 状态 | 50 章均为 `COMPLETE_WITH_CHANGES` |
| Source State delta | 279 条 |
| `SOURCE_VERIFIED` | 263 条 |
| `SOURCE_PARTIAL` | 16 条 |
| 单独登记的不确定发现 | 69 条 |
| Hydration Author Task | 50 个，全部 `DONE` |
| Hydration handoff | 50 个，全部 `COMPLETED` |
| 被拒绝导入 | 0 |

真实 50 章中没有零变化章节，因此 Web 没有伪造一个 `COMPLETE_NO_CHANGES` 样本。零 delta 的合法完成语义由集成测试单独覆盖：它会标记为已分析、无变化，而不是误判为缺失或失败。

第 50 章源文件标题为《削的木箭》，但正文内章节标题标记为第 49 章；Workbench 继续使用 ingest 后的真实 ordinal 50，并在本报告保留这一来源不一致，不擅自修正文稿。

## 3. Global Book Profile

Profile 固定为九个维度：

1. 世界观与规则
2. 人物
3. 剧情
4. 文风
5. 叙事
6. 对话
7. 节奏
8. 主题
9. 连续性

Profile 属于 Book + Edition，不随章节切换。真实 Web 已完成两次版本化作者 Overlay：

- v1：在“世界观与规则”增加建议“测试规则：某类型复活不得出现”。
- v2：在“主题”增加 MUST 约束“主角不应无理由主动伤害无辜角色”。

页面可查看 Effective Profile、作者 Overlay、版本历史和可读变更；修改 Profile 会让旧规划失效，但不会改变 Source、Canon 或已写正文。

## 4. Profile 到三候选的真实闭环

Lunar Worker 在冻结的 Local File Handoff 中生成了 3 个不同 lens 的候选，主线程通过正式 CLI 合同导入：

| 排名 | 候选 | Lens | 最终选择分 | 硬门 | 选择状态 |
| ---: | --- | --- | ---: | --- | --- |
| 1 | 把一匣子弹变成一份有条件的账 | `EARNED_OPPORTUNITY` | 99.33 | 通过 | `SELECTED` |
| 2 | 把每一发子弹算清 | `CONTINUITY_ACTIVE_THREAD` | 97.92 | 通过 | `NOT_SELECTED` |
| 3 | 不扣扳机的侦察窗口 | `FORWARD_EXPANSION` | 94.96 | 通过 | `NOT_SELECTED` |

三个候选均满足：

- 九维 Profile 对齐 9/9；
- MUST 主题约束通过，零违反；
- 本次作者目标命中 3/3；
- 明确将 M500 视为第 6 章既有装备，不回溯篡改获得时间；
- 将资源代价、林雨薇的独立选择与后续开放空间写入结构化证据；
- 不把 INCOMPLETE metric run 中缺失的八项分数冒充观测值。

正式 continuation handoff 已为 `COMPLETED / PLAN_ONLY`。当前仍为候选层，`Candidate ≠ Canon`。

## 5. 状态工作区与 Inspector

- M500 Inspector 显示 `SOURCE_VERIFIED`、首次获得第 6 章、首次确认第 6 章、最近确认第 33 章、持有者、槽位、本章证据与 Who Knows。
- 知识页使用 Character × Knowledge Topic 矩阵区分 `KNOWN / SUSPECTED / UNKNOWN`，未建立的知识保持未知。
- 第 50 章关系图为 4 个节点、3 条可追溯关系：苏牧—林雨薇合作、苏牧—林雨薇默契、苏牧—周振国信息交易。
- 当前没有可确认势力事实，势力页诚实显示“尚无势力事实”，没有把 Atlas 或规划项伪装成 Source fact。
- Source 状态中的任务为 0；作者未来任务、意图和剧情线在独立规划层显示，不覆盖当前世界状态。

## 6. 三栏、滚动与返回行为

- 左栏、右栏都具有常驻 rail 按钮，折叠后仍可随时展开。
- 实际浏览器连续选择 10 个左栏下方项目，左侧 explorer 的滚动位置保持，不再跳回顶部。
- 项目选择只更新中心工作区或 Inspector，不调用 `scrollIntoView()` 抢占左栏。
- 浏览器前进/后退后仍恢复 mode、node、chapter、character、state tab、两侧栏折叠状态和各自滚动位置。
- 当前章节状态摘要保持 sticky，但不会拦截 tab 或列表项点击。

## 7. 安全边界

| 对象 | 验收结果 |
| --- | ---: |
| Canon Commit | 0 |
| Chapter Contract | 0 |
| Draft | 0 |
| Edition activation | 0 |
| `book/` 修改 | 0 |

Hydration 只写 Source State Ledger、可重建 snapshot cache、handoff/task 状态；Profile 和候选只写各自软理解/规划层。`book/`、不可变 source、base 正文和 Canon Event Store 均未被改写。

## 8. 自动化与 Web 验证

| 检查 | 结果 |
| --- | --- |
| `uv run --no-sync pytest -q` | **176 passed in 92.20s** |
| `uv run --no-sync ruff check src tests` | **All checks passed** |
| `uv run --no-sync mypy src` | **Success: no issues found in 144 source files** |
| `python -m compileall -q src tests` | **passed** |
| CLI help：`novel`、`features`、`rhythm`、`hooks`、`metrics`、`segments`、`workflow` | **passed** |
| `uv run --no-sync novel web doctor` | **ok=true；routes/static/templates/API health 全部通过** |
| localhost HTTP smoke | `/library` HTTP 200；真实 Workbench 已在浏览器交互验收 |

## 9. 浏览器证据

截图目录：`benchmark/artifacts/story_world_workbench_v2_2/`

- `01-state-chapter10.png`
- `02-state-chapter30.png`
- `03-state-chapter50.png`
- `04-equipment-m500-inspector.png`
- `05-knowledge-matrix.png`
- `06-relationship-graph.png`
- `06b-factions-empty.png`
- `06c-tasks-author-plan.png`
- `07-analysis-worldbuilding-edit.png`
- `08-analysis-theme-version-history.png`
- `09-sidebar-scroll-before.png`
- `10-sidebar-scroll-after.png`
- `11-candidate-cards.png`
