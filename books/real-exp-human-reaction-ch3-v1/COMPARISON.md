# Chapter 3 可观察对比

本文件只记录旧稿与本轮新稿的可观察差异，不对文学质量打分，也不自动宣布新版更高。

## 样本与字符数

- `OLD_CHAPTER_3.md`：来自 `real-exp-opening-reader-first-fresh-v1/chapters/chapter-0003.md`，约 3775 个文本字符，73 个非空段落。
- `NEW_CHAPTER_3.md`：来自本轮 Primary 正式正文，约 2835 个文本字符，67 个非空段落。
- 新稿没有生成 Chapter 1、Chapter 2 或 Chapter 4；原稿没有被改写。

## Director

- Director response 保持了八个原有字段，没有新增“情绪字段”。
- 在“推动事件的人”“对手或世界反应”“状态变化”等已有位置中，确实规划了周既明的竞争性反应、许照的守约确认、宁秋禾的公开记录和候考弟子的社会判断。
- 但 Director 把冻结的“公开取牌回线”改成了“指定进攻后完成触肩反制”，并把“尚未正式入内门”写成“取得内门弟子身份”。这是事实漂移，不是人物温度改善。

## Curator

- Curator 使用了原有 `Relevant Characters and Relationships` 标题，没有生成 Character Card、心理档案或新的固定字段。
- 角色投影保留了顾长川的变强欲望和克制声音、周既明的竞争目标与防备、许照的守约边界、宁秋禾的流程职责。
- Curator response 没有修正 Director 的规则和身份漂移，反而把“触肩反制/内门弟子身份”继续放进 Relevant World Rules 和 Relevant Plan；因此下游不是完全干净的冻结事实输入。

## Primary / Reader-First

- Primary Prompt 实际包含新增 Reader-First Human Reaction 规则和 Primary “人物不是状态更新器”软提醒。
- 新稿保持普通、直接的动作表达：读者可以直接知道周既明怎样进攻、顾长川何时转身、动作怎样改变现场；没有长篇心理独白或复杂隐喻堆积。
- 顾长川获得“通过”后不是立即只更新状态：他先听见结果，再感到右肩疼痛往里沉；之后低头看名册并带伤走向下一流程。
- 周既明失败后给出具体竞争反应：“下一次，我先封你的脚，再出手”，随后离开，没有统一写成“重新评估”。
- 许照看到交易兑现后只说“守约”，检查顾长川是否泄露步法，再补充以后先说清条件；她保持职业化，但有明确的边界反应。
- 宁秋禾通过在名册上落笔、确认结果完成自己的反应和职责，而不是只说“确认交易条件”。
- 新稿没有出现“大家都震惊”式统一反应，也没有把情绪改写成连续心理解释；反应主要通过肩痛、停留、视线、落笔、短句和离开动作表现。

## 事实边界观察

- 旧稿保留了台心合格牌、取牌回线、周既明越线、顾长川回到自己的白线，以及“尚未正式入内门”。
- 新稿改成了白线内有效触肩反制，没有出现取牌回线；并写成顾长川取得内门弟子身份。State Delta 也把这一漂移写入了本实验副本的 BOOK.md。
- 因此，本轮可以证明新规则在当前输入下确实进入了 Director、Curator 和 Primary，并且正文出现了更具体的短反应；但不能把新旧正文的全部差异归因于 Human Reaction 修复，因为上游 Director/Curator 同时改变了本章事件合同和结果事实。

## Harness 根因与本次修正

- 上一轮 `EXPERIMENT.md` 声称冻结原 Chapter 3 核心事实，但实际 `CHAPTER_PLANS.md` / `FIXED_CORE.md` 没有把“台心合格牌、取牌回线、周既明越线、尚未正式入内门”等具体事实写入 Director 可见的当前章输入。
- `render_experiment.py` 的 `chapter_plan()` 会把完整 Chapter 3 计划段落传入 Director 的 `current_chapter_plan`；本次已把上述事实明确写入该段落，并同步写入 `FIXED_CORE.md`，未来重跑时可以直接核对 Prompt。
- 本次只修正输入定义和说明，没有重跑 Chapter 3，没有覆盖任何 raw Prompt / Response，也没有新增模型调用。
