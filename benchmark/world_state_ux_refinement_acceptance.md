# World State UX Refinement 验收报告

> **2026-08-11 复审修订提示**：本报告自身 UX 验收项与两个当日缺陷无直接因果关系（验收样本未触发缺陷路径），但全站页面渲染路径曾被 readiness 崩溃 live blocker 波及，原隐含“通过”结论已按复审结果加注限定；详见文末“2026-08-11 复审修订”章节。**2026-08-11 证据回填后，波及限定已按证据范围解除（见文末“证据回填”与“最终结论”）。**

## Before UX problems

改造前截图保存在 `benchmark/artifacts/world_state_ux_refinement/before/`。实际页面存在以下作者体验问题：

- 总览先呈现 Coverage、Projection、Delta 等工程概念，作者需要自行翻译“这一章究竟改变了什么”。
- 左树、中心标签和右侧面板重复同一套导航，信息密度高但行动入口不清楚。
- `UPDATE`、`SOURCE_VERIFIED`、`AFTER_CHAPTER`、原始字段名等技术语言进入主界面。
- 背包默认展开大量记录，搜索、类别与排序不能形成真正的可见过滤；规划用 Add Item 表单抢占当前状态空间。
- 认知矩阵默认承担全部人物 × 主题，长书下既拥挤又昂贵。
- 地点、势力和关系只有通用卡片，缺少各自的作者工作语义。
- Inspector 只像通用 JSON 查看器，缺少历史、谁知道、读者边界、揭示计划与原文证据的稳定结构。
- 左栏下方项目点击后曾回到顶部；不同功能页还会继承上一页中心滚动位置。

## Delta-first overview

- 默认问题改为“这一章改变了什么？”，按人物、物品、装备、能力、资源、关系、剧情等作者类别分组。
- 操作统一翻译为“新增 / 获得 / 失去 / 转交 / 状态更新 / 关系变化”等作者语言。
- 明确区分三种情况：有确认变化、`本章没有确认变化`、分析未完成；没有变化不会被误写成数据缺失。
- 本章变化之后提供与上一章的数量比较，以及“当前关键状态”四块落点：人物、世界、剧情、幕后与揭示。
- “完整状态”改为显式按需展开，不再与默认 Delta 视图同时渲染。

## Global vs Character scope

- 状态工作区常驻“选中人物 / 全局”范围开关，URL 保留 `state_scope`、`character_id`、章节和镜头。
- 人物范围只构建所选人物的背包、装备、能力、认知和关系；全局范围才合并全体实体，避免默认付出全局投影成本。
- 真实第 50 章浏览器验收：苏牧背包 68 项，全局背包 75 项；切回人物范围后恢复 68 项且人物选择未丢失。
- 左侧数量和名称跟随范围变化，例如“苏牧背包”与“全局背包”，不再让作者猜当前集合边界。

## Inventory improvements

- 背包、装备、能力使用紧凑卡片，显示作者类别、持有者、状态摘要、证据层和本章变化。
- 支持名称/说明/持有者搜索、类别过滤、最近变化/首次获得/名称排序。
- 浏览器实测输入“木”并选择“资源”后，68 张卡片中仅 1 张可见、67 张真实隐藏。
- 点击对象后，Inspector 展示当前状态、首次/最近确认、持有者、装备状态、变化历史、谁知道、揭示计划与原文证据。
- 未来物品与作者计划不再混入当前背包；规划入口回到剧情规划边界。

## Knowledge views

- 默认按人物查看，左侧选择人物，右侧只列该人物的认知主题，并明确“尚未知”是无证据而非断言不知道。
- 可切换按主题查看“谁知道”，但不与默认人物视图同时显示。
- 完整矩阵只在作者先选择“完整矩阵”、再点击“构建完整矩阵”后生成。
- 真实数据验收为 4 人 × 112 主题，共 448 个按需单元格；构建前 DOM 中没有矩阵表格。

## Location / Faction / Relationship

- 地点档案支持全部、本章变化、最近变化与搜索；卡片呈现公开状态、在场人物、资源、限制、近期事件、关联势力和最近确认章节。缺失字段显示“尚未确认”，不会把 `SOURCE_VERIFIED` 当地点状态。
- 势力工作区分开公开目标与作者全知目标，并显示关键人物、控制地点、资源、关系、态度、当前行动及公开/未知边界。
- 关系工作区同时提供关系图和列表，Inspector 展示双方、关系类型、七个关系维度、变化历史和证据；物品专属“首次获得/是否装备”不会泄漏到关系或势力。
- 真实书没有势力事实，因此势力正样本只在一次性临时数据库中验收，未写入真实书库。

## Author / Reader / Character Lens

- 章节工具条常驻作者、读者、人物三个镜头；切换只改变查询投影，不改变 Truth、Reveal 或 Canon。
- 真实第 50 章验收：作者镜头可见 4 个主题；读者镜头只见 1 个截至本章的认知投影；林雨薇人物镜头只见 1 个且答案保持隐藏。
- 读者/人物镜头不会泄漏“尚未公开的组织”等作者独占真相。
- 章节上一章/下一章导航保留当前功能、范围、镜头和人物选择。

## Inspector standardization

统一右侧结构为：

1. 当前状态与适用于该实体的字段；
2. 变化历史；
3. 谁知道 / 读者边界 / 人物认知；
4. 揭示计划，并明确不属于当前事实；
5. 公开与未知边界及相关对象；
6. 原文证据；
7. 默认折叠的技术详情。

不同实体只显示适用字段，避免关系被标记“未装备”、势力被标记“首次获得”等跨实体污染。

## Technical information hiding

- `Coverage`、Source State、原始类别、原始操作、ID、source span 等只放入折叠的“技术详情”。
- Story Atlas 明确标注为软参考且默认折叠，不会提升为当前世界事实。
- 主界面使用“原文确认 / 正史事件 / 作者记录 / 尚未确认”等作者语言。
- CSS 重新确立 `[hidden]` 的强语义，筛选记录、认知子视图和完整状态不会因组件 `display` 规则重新出现。

## Long-book scalability

- 服务端只渲染当前状态功能页，不再把十一套中心工作区一起下发。
- 默认人物范围不构建全局人物集合；只有选择全局时才合并。
- 认知矩阵延迟到二次明确操作后构建，默认仅渲染按人物列表。
- 真实 50 章富状态书已覆盖 68 项人物背包、112 个认知主题和 448 个矩阵单元格。
- 书库中更长的 379 章会话缺少同等丰富的 Source State 数据；验收保持未知/未分析，不伪造正样本。长书结论因此覆盖导航、分页式工作区和延迟矩阵架构，不声称不存在的 379 章富状态性能样本。

## Browser acceptance

- 浏览器视口：1600 × 1000，真实书 `cable-survival-blind-50` 第 50 章为主要样本。
- 该富状态样本在正常书库目录中的状态仍是 `INITIALIZATION_REQUIRED`，产品会按既有门禁进入初始化页。截图阶段因此使用只读直连其现有 SQLite 的可视化 harness，只关闭 library/discovery 路由门禁，不改变目录状态；交付结束后已恢复正常书库服务。
- 人物/全局范围：68 → 75 → 68，URL 与人物选择均保持。
- 章节时间旅行：第 50 章背包 → 第 49 章 → 第 50 章，`state_tab=inventory`、作者镜头、人物范围和苏牧均保持。
- 左树在下方区域点击后仍停留在下方，没有回到 `0`；关闭浏览器滚动锚定，由显式导航状态恢复负责位置。
- 从已滚动页面切换到新功能页时，中心区与 Inspector 回到顶部；浏览器后退仍使用历史状态。
- 搜索/类别过滤实际隐藏 67 张卡片；认知矩阵构建前不存在、构建后出现 448 个单元格。
- 技术详情、Story Atlas 和完整状态在默认 Delta 视图中均保持折叠。

## Screenshot index

| # | 文件 | 数据来源 | 验收点 |
|---|---|---|---|
| 01 | `01-overview-delta-first.png` | 真实第 50 章 | Delta-first 总览 |
| 02 | `02-overview-no-change.png` | 临时测试样本第 3 章 | 完整分析但无变化 |
| 03 | `03-character-workspace.png` | 真实第 50 章 | 人物工作区 |
| 04 | `04-inventory-search-filter.png` | 真实第 50 章 | 搜索 + 资源过滤 |
| 05 | `05-item-inspector-who-knows.png` | 真实第 50 章 | 物品历史、谁知道、证据 |
| 06 | `06-knowledge-by-character.png` | 真实第 50 章 | 默认按人物认知 |
| 07 | `07-knowledge-full-matrix.png` | 真实第 50 章 | 按需完整矩阵 |
| 08 | `08-location-sheet.png` | 真实第 50 章 | 地点档案 |
| 09 | `09-faction-inspector.png` | 临时测试样本第 2 章 | 势力正样本与 Inspector |
| 10 | `10-relationship-inspector.png` | 真实第 50 章 | 关系图、维度、历史 |
| 11 | `11-author-lens.png` | 真实第 50 章 | 作者镜头 |
| 12 | `12-reader-lens.png` | 真实第 50 章 | 读者镜头 |
| 13 | `13-character-lens.png` | 真实第 50 章，林雨薇 | 人物镜头 |
| 14 | `14-technical-details-hidden.png` | 真实第 50 章 | 技术区默认折叠 |

## Tests

- `uv sync --python "C:\Users\jingx\anaconda3\python.exe" --extra dev --no-editable --reinstall-package novel-authoring-system`：通过。
- `uv run --no-sync pytest -q`：196 passed。（本报告初次验收时的数字；2026-08-11 缺陷修复后全量回归为 **210 passed**，见复审章节）
- 世界状态与 Truth/Reveal 聚焦测试：15 passed。
- `uv run --no-sync ruff check src tests`：通过。
- `uv run --no-sync mypy src`：148 个源文件无错误。
- `uv run --no-sync python -m compileall -q src`：通过。
- `node --check src/novel_authoring/web/static/workbench.js`：通过。
- `novel --help`、`features/rhythm/hooks/metrics/segments/workflow --help`：全部通过。
- `uv run --no-sync novel web doctor`：`ok: true`，路由、模板、静态资源和原生前端均正常。
- `git diff --check`：通过，仅有工作区既有换行提示。

## Safety

- 未修改 `book/`、Canon、Source 原文、Truth/Reveal 权威记录或 edition 正文。
- Web 状态投影使用只读查询路径；页面构建不物化 snapshot。
- 集成测试对 Author/Reader/Character 三个镜头查询前后的 SQLite dump 做完全相等比较，确认只读。
- 截图 02 与 09 的临时样本创建于系统临时目录；服务停止后不属于真实 `library/`，也不进入提交。
- 未创建新分支、worktree 或 PR；交付只在永久分支 `小说续写_codex` 完成。
- 仓库中与本任务无关的既有 benchmark 产物和 `workspace/.auto-workbench.sqlite3` 均未改动、未纳入交付。

## Git

- 分支：`小说续写_codex`。
- 交付范围：世界状态投影、Workbench 模板/样式/交互、相关集成测试、本报告与本目录 14 张截图。
- 提交与远端同步结果以最终交付消息和仓库历史为准。

## 2026-08-11 复审修订

### 复查结论：与当日两个缺陷的关系

同日复审确认了两个真实缺陷（均有真实 HTTP 响应与 traceback 证据）：

1. 缺陷 1（交接指令路径）：legacy migrate 导入书的 `NOVEL_INITIALIZATION` handoff `prompt_path` 缺 `input/` 段，`copy_instruction` 抛 `FileNotFoundError` → HTTP 400 `WORKFLOW_ERROR`（真实复现：`cable-survival-demo`）。**本报告验收不涉及初始化交接指令链路，无直接波及。**
2. 缺陷 2（readiness 崩溃）：`library_catalog.py` 对字符串 readiness（`"BLOCKED"`）做 `dict()` 崩溃，导致所有 HTML 页面与 catalog API 400（真实复现：`book-6k-0lnr4da` 初始化写入后全页面 400）。

**对本报告的波及评估**：

- 初次验收当时，样本书 `cable-survival-blind-50` 为就绪书，书库中不存在字符串 readiness 书，缺陷 2 未被触发；14 张截图与 Browser acceptance 各项观察在当时真实成立，**逐项结果维持**。
- 但世界状态页面与其他页面共享同一 Catalog/页面渲染路径：只要书库中存在一本初始化中（字符串 readiness）书，本报告验收的全部页面同样会 400。因此本报告隐含的“通过”结论需加注限定，不能视为无条件终验收。
- 两缺陷均已在本会话修复并合入工作树，全量回归通过；真实浏览器端到端复验仍在补齐中。

### 修订后结论

~~**UX 验收项维持；整体结论加注限定：“修复已落地，自动测试证据充分；存在初始化中书的书库中的端到端渲染复验：进行中（待补）。”**~~（**已于 2026-08-11 证据回填后再次更新，见文末“最终结论”**）

### 证据四分类（截至 2026-08-11，2026-08-11 证据回填后更新）

**a) 自动测试证据（已有）**

- 本报告初次验收时：`uv run --no-sync pytest -q` 196 passed；世界状态与 Truth/Reveal 聚焦测试 15 passed；ruff/mypy/compileall/node --check/web doctor 均通过。
- 缺陷修复后：新增回归 `uv run --no-sync pytest -q tests/integration/test_handoff_instruction_reliability.py` **14 passed**（含字符串 readiness 不崩溃且页面 200）；全量回归 **210 passed**；各质量门禁均通过。
- 局限：进程内/TestClient 级验证，不覆盖真实浏览器行为。

**b) 真实浏览器证据（初次验收已有；2026-08-11 缺陷波及面的共享渲染路径复验已回填，PASS）**

- 已有：`artifacts/world_state_ux_refinement/` 下 before/after 截图共 14 张（见 Screenshot index）与真实书第 50 章浏览器操作记录；截图使用只读直连 SQLite 的可视化 harness，不改变目录状态，已在报告中如实标注。
- 2026-08-11 回填（PASS，截图目录 `artifacts/acceptance-browser/20260811-init-handoff/`，step1–step6 共 7 张，与 Library Onboarding 报告 L-3 同一证据源）：在真实书库（含初始化中书与字符串 readiness 存量书）中，Library 页、任务中心与指令复制链路端到端正常渲染、无 400（GET instruction 200、content-length=1083，剪贴板 723 字符与服务端 `body.instruction` 逐字相同，含 `$process-novel-handoff`/`$initialize-existing-novel`；静态资源全部 `?v=3.3.0`）。
- 如实限定：上述回填截图覆盖的是与本报告共享的 Catalog/页面渲染路径（Library 页、任务中心）；本报告世界状态功能页自身在存在初始化中书时的直接截图未在本轮单独采集，其渲染正确性由共享路径端到端证据与自动测试（字符串 readiness 下页面 200 回归用例）联合支撑。

**c) 真实语义执行证据（本报告不依赖；同日初始化链路证据已回填，执行主体限定如实标注）**

- 本报告验收基于既有 Source State 只读投影，自身不涉及 Codex 执行。
- 2026-08-11 同日初始化链路回填（与 Library Onboarding 报告 L-2 同一证据源）：`handoff_c3582f9ea417a15da6c7d45b` 被真实领取处理，按 skill 完整执行 Atlas-first 初始化流水线至严格 READY（status=COMPLETED、readiness=READY、canon_committed=false、edition_activated=false；catalog API 最终 book-qombhi5tza state=READY、studio_ready=true）。执行主体为开发代理在 Codex 桌面端合同下按 skill 执行，非作者手工操作的 Codex 桌面端会话，**不得称为“作者侧 Codex 桌面端执行”**。

**d) 合同 fixture 证据（间接，明确局限）**

- 本报告仅使用一次性临时数据库样本（截图 02、09）验证势力正样本，不属于初始化合同 fixture；同日 Library Onboarding 报告的 READY 验收所用合同 fixture 不传导为本报告证据。
- 局限：fixture/临时样本只验证展示与契约，不得称为真实 Codex 初始化。

**声明：不得把 fixture 称为真实 Codex 初始化。本次回填的真实语义执行虽非 fixture，但执行主体为开发代理（Codex 桌面端合同下按 skill 执行），不等同于作者侧 Codex 桌面端执行，二者如实区分。**

### Blocker 清单与解除状态（2026-08-11 证据回填后更新）

| ID | Blocker | 解除状态 | 证据出处 |
|---|---|---|---|
| W-1 | 存在初始化中（字符串 readiness）书时世界状态页面渲染的端到端复验 | **已按波及范围解除（2026-08-11）** | 证据 b)：`artifacts/acceptance-browser/20260811-init-handoff/` step1–step6，真实书库（含初始化中书与字符串 readiness 存量书）中共享 Catalog/页面渲染路径（Library 页、任务中心、指令复制链路）端到端 200、无崩溃；叠加自动测试中字符串 readiness 下页面 200 的回归用例。如实限定：世界状态功能页自身的直接截图未在本轮单独采集 |

关联报告证据同步：L-2/S-3 对应的真实语义执行证据已于 2026-08-11 补齐（执行主体为开发代理，非作者手工 Codex 桌面端会话，如实标注）。

### 证据回填（2026-08-11）

本节在保留上方复审修订全部历史记录的前提下，回填新证据（详见“证据四分类”b/c 两节与上方解除状态表）：

1. **真实浏览器端到端证据（PASS）**：截图目录 `artifacts/acceptance-browser/20260811-init-handoff/`（step1 至 step6 共 7 张），覆盖 W-1 波及面：真实书库（含初始化中书与字符串 readiness 存量书）中共享渲染路径端到端正常。
2. **真实语义执行证据（非 fixture）**：`handoff_c3582f9ea417a15da6c7d45b` 完整执行 Atlas-first 初始化流水线至严格 READY（与 L-2/S-3 同一证据源）；本报告自身不依赖该项，仅同步记录。执行主体为开发代理在 Codex 桌面端合同下按 skill 执行，不得称为“作者侧 Codex 桌面端执行”。
3. **存量修复佐证**：`cable-survival-demo` 失效 `prompt_path` 行经 `copy_instruction` 回退读取成功并自动回写 DB（instruction_available=true）。

### 最终结论（2026-08-11 证据回填后，按波及评估）

**UX 验收项维持通过；缺陷 2 波及的共享 Catalog/页面渲染路径限定已解除**：真实书库（含初始化中书与字符串 readiness 存量书）端到端复验（PASS，`artifacts/acceptance-browser/20260811-init-handoff/`）确认 Library 页、任务中心与指令复制链路正常渲染，叠加字符串 readiness 页面 200 的自动回归用例，W-1 按波及范围解除。如实保留两点限定：（1）本报告世界状态功能页自身在存在初始化中书时的直接截图未在本轮单独采集；（2）本报告不声称“作者侧 Codex 桌面端执行”已完成（同日真实语义执行的执行主体为开发代理，非作者手工 Codex 桌面端会话），合同 fixture 仍不构成真实 Codex 初始化证据。
