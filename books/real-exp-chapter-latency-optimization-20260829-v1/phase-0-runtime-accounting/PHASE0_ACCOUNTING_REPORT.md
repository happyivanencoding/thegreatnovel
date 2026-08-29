# Phase 0｜章节 Runtime 真实耗时与累赘审计

> 冻结来源：`real-exp-fast-world-20ch-20260828-v1`。本报告区分正常采用节点、废弃重跑、周期 Review、终检 Repair 与开书上游；不把未完成调用伪装成可精确计量的模型 wall time。

## 1. 正常采用章节链

|节点|平均 wall|中位 wall|占正常章节链|平均 Prompt 字符|平均 input|平均 cache|平均 output|平均 thought|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|Director|33.9s|25.9s|9.1%|11957|18242|17766|1515|865|
|Curator|116.2s|100.0s|31.4%|21884|24600|20787|5756|4122|
|Primary|55.4s|53.2s|15.0%|12569|21122|17408|2766|355|
|Authority Reviser|137.3s|137.5s|37.1%|20267|8865|42906|5855|3491|
|State|27.4s|27.3s|7.4%|6170|18624|12851|1280|147|

- 20 章正常采用节点合计：**123.43 分钟**；平均 **6.17 分钟/章**。
- Curator + Reviser：**68.5%**；Primary 只占 **15.0%**。

## 2. 正常平均没有计入的真实成本

|成本|模型 wall / 实际 elapsed|说明|
|---|---:|---|
|废弃但已完成的章节节点|8.72 分钟|第一次 Ch2 全链 + 第一次 Ch3 Director/Curator；后来因 Ch1 后重规划废弃|
|Ch1 后 Replan|3.92 分钟|单独 ACP 文件，原 RUN_LOG 未记录|
|十章 Review|6.19 分钟|第10章后一次|
|终检 Outcome Repair|1.41 分钟|Ch19 明确恢复“本人进入镇海”|
|终检 State rebuild|0.93 分钟|Ch19、Ch20|
|中断区间|13.50 分钟 elapsed|Ch3 Primary 启动后被重规划中断；其中包含 Replan，剩余时间不能可靠归因给模型，故不计入模型 wall|

- 从 Ch1 Director 启动到 Ch20 完成，实际 elapsed：**152.20 分钟**。
- 加上运行后终检修复后，真实章节批次：**154.53 分钟**，摊到 20 章为 **7.73 分钟/章**。
- 再摊入开书上游，整本实验从启动到修复完成约 **176.72 分钟**，即 **8.84 分钟/章**。

## 3. Reviser 实际改动量

- Primary → Reviser 平均字符相似度：**0.954**。
- 20 章中 Primary 被 Reviser 完全原样返回：**1 章**。保存后的最终文件有 **8 章**与 Reviser response 非字节级相同，但只有 **1 章**字符相似度低于 0.99；已记录的额外正文 Repair 为 Ch19 一次。
- `CHAPTER_METRICS.csv` 逐章记录 exact、changed lines、Primary/Reviser/最终稿三方相似度，后续 Patch Reviser A/B 以此为基线。

## 4. 章节 raw GBrain

- 历史 runner 共留下 **20** 份 Curator retrieval；其中 **19** 章零命中，总计只接受 **1** 条。
- production prompt 层现已 fail closed：所有 Hybrid Chapter Runtime 即使调用方误传 `gbrain_inspiration` / Reference Program，也不再让它进入 Curator、Primary、Reviser 或 Specialist。Scene Skill 继续作为 source-blind 的窄 craft 带宽。

## 5. Phase 0 结论

1. 正常链的主要耗时不是写作，而是 Curator + Reviser 的重复保险。
2. 后十章 stale Long Block 属于确定性脏上下文，必须在 Runtime 边界删除，不能留给模型判断。
3. 章节 raw GBrain 在该实验中几乎无收益，并违背当前章节 Authority 边界，已从 prompt 真源与活跃批量 runner 双重关闭。
4. 后续 Phase 1/2/3 的质量比较必须同时展示“正常采用耗时”和“真实批次摊销耗时”，不能让下游 high Reviser 掩盖上游漂移。

## What This Did Not Solve

- 没有把 Curator、Reviser 或 Director 自动降档；这些仍需受控 A/B。
- 没有修改 ACP runner，也没有修改前端。
- 没有把本次 20 章的模型 wall 外推为 direct API latency。
