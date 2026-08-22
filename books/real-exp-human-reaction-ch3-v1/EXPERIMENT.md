# 《借我一招》Chapter 3 Human Reaction 最小验证

基线：`origin/principal_dev_new_sys` / `26df07a72ecbb126ec66f2b3609621ce16f8f15e`

本实验只重新生成 Chapter 3，验证最新 Reader-First / Human Reaction 软规则是否让人物在既定胜负、资格和关系结果中出现自然、可见、短暂的个人反应。不得修改生产 Prompt、生产代码、原实验或冻结故事事实。

## 冻结输入

- 起始 `BOOK.md` 来自原实验 Chapter 2 的 `runs/chapter-0002/BOOK_after_state_delta.md`；
- `chapters/chapter-0001.md`、`chapters/chapter-0002.md` 来自原实验并保持不变；
- `OLD_CHAPTER_3.md` 是原实验 Chapter 3，仅用于人工对比；
- `CHAPTER_PLANS.md` Chapter 3 段落和 `FIXED_CORE.md` 的 `Chapter 3 Frozen Event Facts` 是未来重跑的明确冻结输入；它们不是“原实验事实共同约束”的说明文字。
- 冻结事实包括台心合格牌、取牌回线、周既明越线、顾长川本轮公开升院合格、尚未正式入内门、一次回身卸力步、许照守约和周既明成为公开竞争者。复制的 `render_experiment.py` 会把完整 Chapter 3 计划段落传入 Director 的 `current_chapter_plan`。

## 执行边界

严格执行：`Director → Curator → Primary → State Delta`。

每个节点只调用一次；Specialists、Emotion Specialist、Integrator、Reviewer、自动重写和重试均为 0。Raw Prompt / Response 与 `CALL_LOG.json` 分开保存。State Delta 只应用到本实验副本的 `BOOK.md`。

本实验不生成 Chapter 1、Chapter 2 或 Chapter 4，不对正文打数字分数，不自动宣布新版文学质量更高。

## 本轮已知结论

上一轮新稿不是严格控制变量样本：Director 把“取牌回线”漂移成“触肩反制”，并把“尚未正式入内门”漂移成“取得内门弟子身份”；Curator 没有纠正，Primary 和 State Delta 继承了该漂移。该差异不能归因于 Human Reaction。修正冻结输入后，本轮不重跑正文。
