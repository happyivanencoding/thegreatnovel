# Original Novel Genesis

原创小说与导入小说共用同一套 Authoring Kernel。差异只发生在创作起点：原创项目没有不可变
来源正文，因此不运行 Source Coverage、Arc Extraction 或已有小说 Story Atlas 初始化，也不制造
假“第 0 章”。

## 状态

`ORIGINAL_SEED → READER_EXPERIENCE_GENERATING → READER_EXPERIENCE_REVIEW →
CORE_INNOVATION_GENERATING → CORE_INNOVATION_REVIEW → FOUNDATION_GENERATING →
FOUNDATION_REVIEW → DEVELOPMENT_GENERATING → DEVELOPMENT_REVIEW → FOUNDATION_READY →
FIRST_CHAPTER_DRAFTING → FIRST_CHAPTER_VALIDATED → WRITING_READY`

- `ORIGINAL_SEED`：只保存一句话创意与可选作者约束。
- `READER_EXPERIENCE_GENERATING`：`ORIGINAL_READER_INTERPRETATION` 只读取冻结的
  `original_request.json`，由 Codex 对 premise 做 Semantic First Read；Python 不按 premise 或
  genre 关键词推断 Reader Experience、Narrative Drive 或 Progression Engine。
- `READER_EXPERIENCE_REVIEW`：Reader、Market、Narrative Drive 均是 `NEEDS_REVIEW`
  Proposal；作者可分别调整 20 个阅读体验、Primary/Secondary Drive 和独立的 Progression
  Engine 开关。阅读体验强度不会静默改写 Primary Drive。
- `CORE_INNOVATION_GENERATING` / `CORE_INNOVATION_REVIEW`：在作者确认的 Reader Kernel
  边界内生成并选择一个开放核心机制。
- `FOUNDATION_GENERATING`：新的故事基础方案正在生成；当前方案仍保留。
- `FOUNDATION_REVIEW`：Codex 桌面端已生成待确认方案，仍没有作者幕后设定、章节或正式正文。
- `FOUNDATION_READY`：作者确认影响摘要后，系统在一个数据库事务中建立作者幕后设定、持久
  指令、九维全书画像、近期/中期/长期方向、Active Narrative Spine、开放问题、幕后候选和
  三个首章候选；仍没有正式章节。
- `FIRST_CHAPTER_DRAFTING` / `FIRST_CHAPTER_VALIDATED`：复用 Chapter Contract、Draft 和十项
  Validator，草稿停在批准门前。
- `WRITING_READY`：作者逐字确认“批准写入正史”后，第 1 章成为正式正文；后续复用标准续写
  工作流。原创项目不会因此显示为已有小说的 `FULL_READY`。

## Proposal 合同

`ORIGINAL_READER_INTERPRETATION` handoff 只输出 Reader Experience、Market Category、
Narrative Drive、Progression Engine 建议和语义依据，不得越级生成外挂、Foundation 或章节。

后续 `ORIGINAL_BOOK_BOOTSTRAP` handoff 必须输出恰好三个书名、三个结构上不同的 Story
Foundation、三条未来路线和三个首章候选，并包含主角、目标、冲突、代价、成长、世界规则、
人物/势力、第一阶段目标、近期/中期/长期方向、开放问题、幕后候选、风险与避免陈词滥调。
Proposal 还必须直接提供九维 Profile 初稿；设定逐项标记 `CORE / PREFERENCE / OPEN`；每条
路线提供 commitments 和 open alternatives。长期方向只描述可能性，不能固定结局或生成逐章
FAR 大纲。没有经过评分引擎的首章候选不显示分数。

Foundation Development 同时保留作者可读 grammar，并以现有 `GenreContract`、可选
`ProgressionContract`、`WorldExpansionContract`、`PayoffChannelProfile` 输出结构化
`NEEDS_REVIEW` Proposal。最终确认复用现有 Contract lifecycle 使其成为 `EFFECTIVE`，供
`KernelPlanningContext` 直接读取；关闭 Progression Engine 时不得生成 Progression Contract。

三条路线始终属于同一本 Book/base Edition。每次重新生成创建独立 Proposal Version，并保留
当前方案；同一时间最多一个 `GENERATING`。新方案完成后只能替换“当前待确认方案”，不能修改
已经确认的 Foundation、作者幕后设定或正式正文。

## 作者批准边界

“确认并开始写作”和“批准写入正史”是两道不同的显式批准：

1. Foundation 确认先构造完整 `GenesisApplyPlan`，再在单一数据库事务中写入；
   `accepted.json` 只是数据库成功后的可再生成导出。相同方案重试幂等，不重复写记录。
2. 选择首章候选后才建立 Chapter Contract 与 Draft handoff。
3. 十项 Validator 全部通过后，草稿停在 `VALIDATED`。
4. 只有作者当前明确提供“批准写入正史”，系统才创建第 1 章与 Canon Commit。

原创项目不检查不存在的导入 Source Manifest；它仍校验当前投影、Edition、合同、Draft 内容、
Validator 和作者批准。已有导入小说的 Source 校验保持不变。
