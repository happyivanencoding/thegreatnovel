# Hybrid Multi-Agent Chapter Runtime v1

本项目的 Hybrid Runtime 是透明 Prompt 工作台上的一组确定性上下文投影，不是后台 Agent 调度服务。产品默认是 `hybrid_selective`；作者仍然复制 Prompt、执行独立模型会话、粘贴返回，并显式选择下一步。

## 运行顺序

`chapter_prep` 复用现有八字段事件合同，之后按以下顺序执行：

`Director → Context Curator → Primary Writer → 0—2 个作者选择的 Specialist → Revision Integrator（有有效 Patch 时）→ 正式正文 → State Delta → 作者批准`

Curator 只从 BOOK Contract、规范化 Canon Index、当前计划、Prose Profile、可选 Inspiration 和前文章末局部片段中选择本章相关信息。Primary Writer 先独立写完整章节；专项 Agent 只看 Primary Draft 与职责相关的局部上下文，并返回最多三个可选局部 Patch。Integrator 以 Primary Draft 为唯一正文底稿，可以全部拒绝专项建议。

章节节点只接收本章三行成长短投影：`本章一级成长推进`、`本章二级收益结算`、`本章反哺`。它们不是第九字段，也不是文学质量门禁；完整 Growth Benefit Hierarchy 只进入 Idea、Outline 和 Review Prompt，不注入 Primary Writer、专项 Agent 或 Integrator。

## Prompt modes

新增可编辑并持久化的模板：

- `context_curator`
- `primary_writer`
- `specialist_opening`
- `specialist_dialogue`
- `specialist_action`
- `specialist_emotion`
- `chapter_integrator`

Director 使用固定模板生成八字段合同和非必填专项建议；它不增加第九个 Hard Gate。

旧书加载时，缺失模板在内存中使用代码默认值；不会自动改写旧的 `PROMPTS.md`。点击现有保存按钮后才会写入模板。

## 结构门禁与 fallback

只保留会改变实际动作的结构校验：八字段小纲、非空 Primary Draft、Integrator 非空 `# 正式正文`，以及现有的章节防覆盖和 State Delta v2 提案标题校验。文学质量、Patch 数量、采纳比例和专项 Agent 是否发现问题都不是门禁。

Curator 缺失时，Primary Writer Prompt 明确显示“使用完整上下文 fallback”。专项缺失时，Integrator 显示“无有效 Patch”并继续；所有专项都没有建议时直接 skipped。Integrator 失败时不会自动重跑，作者可以显式采用 Primary Draft。`hybrid_full` 仍保留给架构测试、卷首、关键高潮或作者明确要求的全专项实验。

## 实现边界

`src/story_mvp/hybrid_runtime.py` 只做 dataclass、局部文本投影、尾部衔接截取和一级标题提取。它不调用模型、不写文件、不引入数据库、队列、通用 Workflow Engine、自动重试框架或新的 LLM API。章节和 BOOK 仍然只在既有作者显式保存动作中写盘；State Delta 仍然是人工应用。

每章的中间产物由固定节点 Chapter Run Ledger 记录；Ledger 只提供文件级恢复、节点状态和最终正文来源显示，不自动写 BOOK 或章节。
