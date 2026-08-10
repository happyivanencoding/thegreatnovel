# Story Truth + Knowledge + Reveal Engine V2.3 验收报告

- 验收日期：2026-08-10
- 真实书：`cable-survival-blind-50`
- Edition：`base`
- 验收结论：**PASS**

## 1. 验收总表

| 项目 | 结果 | 真实验收证据 |
|---|---|---|
| A. Manual Hidden Truth | PASS | Chapter 50 新增 `truth-8368d4acea024abeb39cdb971481cd82`，正文为“测试：周振国正在替一个尚未公开的组织收集交易情报。”，`effective_from=30`，状态 `ACTIVE_TRUTH`，兼容性 `COMPATIBLE`，Reader 与苏牧均保持 `UNKNOWN`。Chapter 51–55 为 `HINT`，Chapter 70+ 为 `FULL_REVEAL`。 |
| B. Behavior Without Reveal | PASS | Planning Context 可读取该幕后真相并约束周振国重视交易情报；三份候选均保持身份答案隐藏，没有出现“其实周振国是间谍”式直接揭底。 |
| C. Hint | PASS | Chapter 51 Reveal Agenda 将该真相放入 `HINT`；每份候选都给出“异常记录物资编号”类可读线索，同时不确认组织身份。 |
| D. Character / Reader Separation | PASS | `truth-3e9d23d080204d08a49123c6574203dc` 在同一 Inspector 中显示 Author=`KNOWN`、Reader=`HINTED`、苏牧=`UNKNOWN`、林雨薇=`SUSPECTED`，四层互不推导。 |
| E. Retroactive Conflict | PASS | `truth-3673016bd54146ad858b480f823f67d7` 从 Chapter 20 生效，但与真实 Source 明确冲突；结果为 `CONFLICTING`，兼容性为 `CONFLICTING`，要求 Revision，不能进入 `ACTIVE_TRUTH`。 |
| F. Late Compatible Truth | PASS | `truth-40b804860ae9411ba0d918f8aa56a8f5` 从 Chapter 20 生效，Chapter 20–50 未发现明确冲突；结果为 `ACTIVE_TRUTH + RETROACTIVE_HIDDEN_COMPATIBLE`，不改旧正文，并从 Chapter 51 起进入 Planner。 |
| G. Profile Re-analysis | PASS | 两次真实 `PROFILE_REANALYSIS` Local File Handoff 均完成。第一次 proposal `profile-proposal-7ff064bbb0dd4a05b133a5d04c77beb5` 被拒绝，Effective Profile 保持 v3；第二次 proposal `profile-proposal-a94ab400a65c4045992758ecc639c1a3` 被接受，生成 v4，并新增 Continuity 开放项“药品赊换与静音符交付”。 |
| H. Unified Chapter World State | PASS | Chapter 30 中间状态、右侧章末状态和连续性审查均读取同一个 `ChapterWorldStateView`：人物 3、背包 48、装备 16、能力 6、知识主题 80、关系 1、地点 1、规则 5、Delta 4。连续性链为 Chapter 29 → Delta@30 → Chapter 30。 |
| I. Navigation | PASS | 从 Chapter 10 依次进入世界状态 → 分析主题 → 世界观 → 规划 → 世界状态背包，URL 与页面锚点始终保留 Chapter 10，只有主动点击其他章节才改变锚点。 |
| J. Candidate UI | PASS | 页面显示三张作者可读 Candidate Card，按“目标 / 隐藏真相 / Reveal / Profile / Hard Gate”组织，不默认展示 `author_control_trace` 或 `profile_alignment` 原始 JSON。 |

## 2. Truth、Knowledge 与 Reveal

### Manual Hidden Truth

- Truth：`truth-8368d4acea024abeb39cdb971481cd82`
- 当前状态：`ACTIVE_TRUTH`
- 生效边界：Chapter 30
- 回溯范围：`RETROACTIVE_HIDDEN_COMPATIBLE`
- 兼容性：`COMPATIBLE`
- Reader Knowledge：`UNKNOWN`
- 苏牧 Knowledge：`UNKNOWN`
- Reveal Plan 1：`reveal-plan-239cbd79b34d45a89ee23c25cb4c62af`，Chapter 51–55，`HINT`
- Reveal Plan 2：`reveal-plan-c555fe81f9a44c2da382349303def961`，Chapter 70+，`FULL_REVEAL`

`Author Truth` 只进入作者全知投影、Planning Boundary 和候选约束，不进入 Canon Event Store。Reader/Character 的 `UNKNOWN` 不会因 Truth 创建而自动变化；Reveal Plan 也不等于 Reveal Event。

### Reader / Character Separation

四层知识状态按独立边存储和投影：

- Author：知道完整幕后真相。
- Reader：只获得已发生 Reveal Event 支持的读者知识；本例为 `HINTED`。
- 苏牧：没有对应知识边，因此保持 `UNKNOWN`。
- 林雨薇：有 Source Evidence 支持的 `SUSPECTED` 知识边。

Reader Lens 已实测不会下发 `UNKNOWN` 真相原文、答案或未来 Reveal Plan；只显示允许公开的提示性主题。

### Reveal Agenda 与 Secret Board

- Chapter 50：0 个 Hint，3 个 Keep Hidden。
- Chapter 51：1 个 Hint，2 个 Keep Hidden。
- Chapter 55：1 个 Hint，2 个 Keep Hidden。
- Chapter 60：0 个 Hint，3 个 Keep Hidden。
- Chapter 70：1 个 Must Reveal，2 个 Keep Hidden。
- Secret Board 支持 `SHORT / MID / LONG` 筛选、状态筛选、优先级排序和拖放更新；`SHORT` 实测只显示 Chapter 51–55 的 HINT 项。
- 历史生效 Truth 默认不污染早期 ChapterWorldState；作者显式开启“显示未来真相”后才作为边界外提示出现。

## 3. Planning 与 Candidate

真实 Local File Handoff：

- Handoff：`handoff_7058ff4b0c2272226949b615`
- Task：`plan_427b86c46c98763ef36fee8b`
- 状态：`COMPLETED`
- 结构：严格 3 份候选，全部通过 Pydantic 输出校验与 Hard Gate，三对候选在九项结构差异检查中均通过。

| 排名 | Candidate | 选择状态 | Hard Gate |
|---|---|---|---|
| 1 | 编号只到交易为止 | `SELECTED` | PASS |
| 2 | 先把药品账对上 | `NOT_SELECTED` | PASS |
| 3 | 以五小时换来的补给谈判 | `NOT_SELECTED` | PASS |

每张卡都明确展示：

- 当前章节目标与状态变化；
- 被使用的 Hidden Truth 与 `KEEP_HIDDEN` 项；
- HINT / Reveal 线索及 Reader、Character Knowledge Delta；
- 九维 Profile 对齐；
- Hard Gate PASS/FAIL 与可读失败原因。

## 4. Profile Re-analysis

“重新分析”按钮真实创建 `PROFILE_REANALYSIS` Handoff，而不是复制当前 baseline。Codex 输出经过独立 Schema 校验后只形成 Proposal：

1. `handoff_22b45946bf00217426fc510b` 完成后，作者拒绝 proposal；Profile 仍为 v3。
2. `handoff_6dca866787853614a717fdb1` 完成后，作者接受不同 proposal；Profile 新建 v4。

拒绝与接受均有独立状态，Proposal 不会自行覆盖 Effective Profile，也不会修改 Canon。

## 5. Unified State 与导航

- Workbench 中间世界状态、右侧章末状态和连续性审查共用同一份 `ChapterWorldStateView`。
- 连续性审查同时展示 `WorldState@N-1 → Delta@N → WorldState@N`，不再把当前投影与旧的“历史缺失”模型混用。
- Source-only、未完成 Hydration 的章节仍保留作者可读的历史状态缺口提示；草稿状态明确标为 provisional。
- 所有世界状态、全书画像、规划和 Inspector 深链路都会携带当前 `chapter_id`，解决跨模式跳转后章节锚点丢失的问题。
- 左右栏隐藏后均保留常驻 Rail 按钮，可以随时恢复；左栏章节滚动位置由章节锚点和用户滚动状态共同维护。

## 6. Data Safety

真实库最终只读计数：

| 数据层 | 数量 |
|---|---:|
| Source chapters | 50 |
| Source spans | 51 |
| Canon commits | 0 |
| Canon events | 0 |
| Author truths | 4 |
| Candidate plans | 6 |

验收过程中没有修改 `book/`、Source 章节、Source Span、Canon Commit 或 Canon Event。Author Truth、Reveal Plan、Reader/Character Knowledge、Profile Proposal、Candidate 和 Draft 分层存储；只有未来显式批准的 Canon 写入才允许正式推进公开知识。

## 7. Web 实测证据

- [三候选作者可读卡片](artifacts/story_truth_reveal_v2_3/01-candidate-cards.png)
- [Chapter 50 Author Truth](artifacts/story_truth_reveal_v2_3/02-author-truth.png)
- [Truth Inspector 四层知识与兼容性证据](artifacts/story_truth_reveal_v2_3/03-truth-inspector.png)
- [Chapter 30 统一连续性视图](artifacts/story_truth_reveal_v2_3/04-chapter-30-continuity.png)
- [Chapter 10 跨模式导航保持](artifacts/story_truth_reveal_v2_3/05-chapter-10-navigation.png)
- [Secret Board SHORT 筛选](artifacts/story_truth_reveal_v2_3/06-secret-board-short.png)

实测还覆盖：Author/Reader Lens 隔离、Truth Board 六类分组、未来 Truth 默认隐藏、全局公开状态与作者真相检索、人物/势力 Inspector、RevealPlan 读取，以及隐藏元素的实际 CSS 可见性。

## 8. 自动化验证

| 命令 | 结果 |
|---|---|
| `uv run --no-sync pytest -q` | PASS，182 passed |
| `uv run --no-sync ruff check src tests` | PASS |
| `uv run --no-sync mypy src` | PASS，147 个源文件无问题 |
| `uv run --no-sync python -m compileall -q src` | PASS |
| `node --check src/novel_authoring/web/static/workbench.js` | PASS |
| `uv run --no-sync novel web doctor` | PASS，API、模板、静态资源与必需路由全部正常 |
| `uv run --no-sync novel --help` | PASS |
| `uv run --no-sync novel features --help` | PASS |
| `uv run --no-sync novel rhythm --help` | PASS |
| `uv run --no-sync novel hooks --help` | PASS |
| `uv run --no-sync novel metrics --help` | PASS |
| `uv run --no-sync novel segments --help` | PASS |
| `uv run --no-sync novel workflow --help` | PASS |
| `git diff --check` | PASS |

## 9. 结论

V2.3 已将系统从单一 World State 扩展为可审计的 **Story Truth + Knowledge + Reveal Engine**：作者可以后期加入与旧正文兼容的幕后真相，不改写过去，不提前污染读者或角色知识，同时从下一章开始让行为受真相约束，并按 HINT、PARTIAL_REVEAL、FULL_REVEAL 或 KEEP_HIDDEN 安排公开节奏。人物、关系、势力、地点、物品、能力、世界规则和剧情真相复用同一套机制。
