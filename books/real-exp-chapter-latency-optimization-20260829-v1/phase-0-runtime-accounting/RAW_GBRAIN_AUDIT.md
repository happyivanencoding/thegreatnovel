# Phase 0｜章节 raw GBrain 审计

> 冻结来源：`real-exp-fast-world-20ch-20260828-v1/runs/chapter-*`。这里只审计历史 runner 的章节级 Curator retrieval，不评价 World / Power / Human / Story Program / Outline 的上游 GBrain。

## 结果

- 留有 retrieval 文件的章节：**20**。
- 零命中章节：**19**。
- 全 20 章累计 accepted：**1** 条。

|章|accepted|slug|
|---:|---:|---|
|1|0|—|
|2|0|—|
|3|0|—|
|4|0|—|
|5|0|—|
|6|1|prose-controls/evidence-first-limited-reveal-v1|
|7|0|—|
|8|0|—|
|9|0|—|
|10|0|—|
|11|0|—|
|12|0|—|
|13|0|—|
|14|0|—|
|15|0|—|
|16|0|—|
|17|0|—|
|18|0|—|
|19|0|—|
|20|0|—|

## 判断

章节 raw GBrain 在该样本里几乎没有提供有效内容，却扩大了运行分支并允许 source-specific inspiration 重新接近章节链。当前安全边界应当是：章节 Runtime 只消费已批准 Story / Outline、safe Authority 与 source-blind Scene Skill；即使调用方误传 GBrain 或 Reference Program，Prompt 真源也 fail closed。

该结论只关闭章节 raw retrieval，不影响上游规划阶段经过约束的 GBrain ON。
