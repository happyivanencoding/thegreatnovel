# World State UX Refinement 验收报告

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
- `uv run --no-sync pytest -q`：196 passed。
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
