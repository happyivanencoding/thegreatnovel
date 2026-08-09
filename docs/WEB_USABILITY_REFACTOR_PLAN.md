# Web Authoring Workbench Usability Refactor

更新时间：2026-08-09
范围：`/books/{book_id}/editions/{edition_id}/workbench` 及其只读章节上下文接口。

## 目标与边界

Workbench 是作者的本地 Web 工作台，不是另一个写作引擎。它只读取现有 Book Library、Edition、chapter、draft、validation 和 projection 数据；本轮不修改 `book/` 原文、不写入 Canon、不批准 Draft、不激活 Edition，也不启动 Codex/API。

作者首先需要看到：当前书、Edition、章节锚点、正文、章末状态是否可用、下一步能否继续。数据库字段、投影事件序号、来源枚举和完整 JSON 只作为技术排查材料，默认放在可展开的“技术详情”中。

## U0 审计结论

| 区域 | 当前问题 | 本轮处理 |
| --- | --- | --- |
| 顶部主模式 | `续写/改写/规划/分析/连续性审查` 只有 active class，没有内容状态或真实路由变化 | 统一 `mode` 状态；每个模式渲染独立内容面板，已有数据直接展示，未接入能力明确说明并提供真实工作流入口 |
| 右侧标签 | `正文` 可用；`章末状态` 展示原始 JSON；`下一章接续包` 是空占位 | `prose/state/next` 统一状态；章末状态先显示作者可读摘要和状态卡，接续包显示真实可用性与下一步 |
| 左右栏 | 折叠后网格列和 Pane 都被隐藏，重新打开依赖顶部按钮 | 折叠后保留窄 Rail，Rail 内保留带 tooltip 的展开按钮；宽度、折叠状态和最后模式/标签写入 localStorage |
| 章节状态 | `SOURCE_CHAPTER_STATE_PROJECTION_MISSING`、`anchor_chapter_ordinal`、`through_event_seq` 等内部字段进入主视图 | Python 查询层提供作者可读的状态标签、解释、变化摘要；原始值只放技术详情 |
| Book Profile | `SOFT INTERPRETATION`、`SELF_BOOK`、`Distill version`、`Scope` 直接暴露 | 主层改成“本书画像/柔性理解/来源”；版本和范围移入技术详情 |
| 交互 | 未接入按钮看起来像可执行操作；AI 输入是 disabled 但原因不清 | 能力未接入时使用明确空态，说明原因和下一步；可以进入现有 Workflow 的动作保留真实链接 |

## 状态流

页面状态分为两层：

1. 服务端只读状态：`book_id`、`edition_id`、`chapter_id`、`draft_id`、左侧选中节点、`active_main_mode`、`active_right_tab`。章节/节点导航通过 Workbench HTML 片段重新读取，保持 query-only。
2. 浏览器布局状态：左/右栏宽度、左/右折叠状态、最后主模式和右标签。键为 `novel-authoring-workbench-layout`，只影响当前浏览器，不写入书库。

模式和右标签切换必须改变可见内容；章节切换必须改变中心正文上下文和右侧正文/状态/接续包内容。任何不具备后端服务的动作不得伪造成功状态。

## U1–U4 实施顺序

- **U1 Rails**：Pane 内容和窄 Rail 分离；折叠后保留 Rail；Rail/顶部/Pane header 共用一个 toggle 状态；保存宽度和折叠状态。
- **U2 真实标签**：主模式用独立面板表达续写、改写、规划、分析、连续性审查；右侧标签用真实面板表达正文、章末状态、下一章接续包；缺少服务时给出解释性空态。
- **U3 翻译层**：在查询层集中做枚举、状态和变化摘要的作者化翻译；模板默认只读翻译字段；原始结构进入 `技术详情`。
- **U4 历史状态空态**：章节状态缺失时说明“尚未建立逐章历史状态记录”，解释系统不会用最新状态冒充历史，并给出可执行的下一步；接续包缺失时说明需要先形成可审计的 Boundary/Contract。

## 验收标准

- 点击五个主模式时中心可见内容发生变化，且 URL/localStorage 能恢复最后模式。
- 点击三个右标签时右侧可见内容发生变化，且 URL/localStorage 能恢复最后标签。
- 左右栏折叠后仍各有窄 Rail 和带 tooltip 的展开按钮；刷新后状态保留。
- 默认作者视图不出现原始状态枚举、字段名或完整 JSON；技术详情展开后仍能追溯原始值。
- Source-only 历史状态和缺失接续包均有作者可读解释，不把缺失伪装成“当前状态”。
- 章节切换能更新中心与右侧内容，且不改变 Canon、Edition、Approval 或原文。
