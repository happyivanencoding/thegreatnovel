# Web Workflow UX Audit

## 真实页面审计

审计对象：`/books/cable-survival-blind-50/workflow`，在 `127.0.0.1:8766` 的当前 Web 服务上实测。

当前页面使用 `workflow.html`、`innovation_controls.html` 和全局 `style.css`：

- 页面只使用 `shell narrow`，主要内容被限制在约 1100px，并将续写、改写两个完整长表单放进同一个双栏 `stat-grid`；在 1920px 窗口下形成明显的大面积空白和两张窄卡。
- `requested_stage`、`Edition ID`、`PLAN_ONLY`、`WAITING_FOR_USER`、`Handoff` 直接从模板和任务页暴露给作者。
- 创新级别和创新方向复用旧的纵向 `label`，没有足够的横向点击区域，也没有把 AUTO 互斥规则呈现为简单的 chips 交互。
- Workflow 路由只向模板提供 `book_id`、默认 edition、handoff 列表和创新默认值，不提供当前章节上下文、作者控制任务、Narrative Portfolio 或可读的任务阶段。
- 创建表单仍然提交既有 `/api/books/{book_id}/handoffs/continuation` 与 `/revision`；这些后端服务继续是权威，页面改造不新增 Workflow 状态机。
- Workbench 已经有 `wb-topbar`、`wb-shell`、左右 rail、可持久化折叠按钮和 `data-workbench-shell` 初始化逻辑；Workflow 应复用这套 shell 和 pane 行为。

## 可复用能力

- `home_context` / `edition_chapters`：提供书名、版本、章节和当前版本，不读取或修改 `book/`。
- `list_handoffs` / `get_handoff`：提供现有任务、状态和事件；任务状态的作者文案在 presentation layer 映射，原始值仅放进技术详情。
- `author_control_view`：提供作者任务、作者意图和按短/中/长期分组的组合摘要。作者目标写入现有 Author Control Intent 层，不追加 Canon 事件、不批准草稿、不启用 Edition。
- `create_continuation_handoff` / `create_revision_handoff`：继续承接现有 Local File Handoff Protocol；作者目标和勾选的作者任务作为冻结的操作输入附带到既有 handoff，不改变状态机或 Codex 领取方式。
- `app.js` 的 `initLayout`：复用左右栏折叠、窄 rail、宽度持久化和响应式行为；Workflow 只新增模式 tab、表单反馈和 AUTO/focus 交互。

## 本轮验收口径

1. `/books/cable-survival-blind-50/workflow` 使用 Workbench shell，主体不再是双窄卡，配置区和上下文区合理占满桌面宽度。
2. 续写、改写、规划一次只显示一个作者配置面板；创新程度为横向 segmented control，创新方向为 chips，AUTO 与显式 focus 自动互斥。
3. 页面显示当前章节、版本的人类可读文案、作者目标、可选作者任务和 Narrative Portfolio 摘要；默认不显示原始工程枚举。
4. 任务列表按作者可读状态展示，并可以展开阶段时间线、复制 Codex 指令和查看技术详情。
5. 创建按钮有准备中、成功或失败反馈；仍调用既有 handoff API，所有正式 Canon / Edition / Approval 边界保持不变。
6. Workbench 的“续写”中心模式使用同一套 Workflow presentation layer；左右 pane 继续以可见 rail 方式折叠。
