# 《我身藏诸界》Primary Batch Size A/B｜2026-08-31

## 结论

这轮实验只比较 **Terra high Primary Writer 的 batch size / 跨章视野**，不是完整 production pipeline。

当前最强候选是：**一次生成连续 5 章 + 明确 Chapter Handoff Continuity**。

它在本书前五章上同时做到：

- 比 Sequential-1 五次逐章快约 32.1%（189.516s vs 278.987s；换个口径，逐章慢约47.2%）；
- 只比原始 Batch-5 多约9.2% wall（189.516s vs 173.491s）；
- 修掉原 Batch-5 的第4→5章即时冲突消失；
- 匿名 Luna-high 总体选择修复 Batch-5 胜过 Sequential-1。

**但它还不是 production default。** 本轮没有运行 Director / Curator / Authority Reviser / State，不能把约3分钟/5章误报成完整 production 速度，也没有证明 batched Primary 与逐章 Canon/State 更新、Authority Reviser、失败恢复兼容。

## 三个版本

### B0｜原始 Batch-5

- Terra high，一次写第1—5章。
- wall：173.491s。
- runner output：9084 chars。
- 优点：用户实际阅读主观感觉好；人物欲望、世界奇观、商业节奏已经成立；速度最高。
- 明确失败：第4章裴照临拔剑堵路、浮桥断裂，第5章直接从倒悬城入口重新起场，缺少“为何没夺门骨 / 如何脱身 / 如何入城”的因果。

### S1｜Sequential-1

- Terra high，连续5次调用；每次只写一章，下一次显式读取上一章真实全文。
- wall：52.447 / 37.774 / 67.697 / 46.574 / 74.495s；总278.987s，平均55.797s/章。
- runner output：11083 chars。
- 明显优势：章与章直接咬合；第4→5章不会把裴照临堵路静默删除。
- 新暴露问题：为了把坏上游 Plan 接回“已经进入倒悬城”的目标，第5章临时创造“城内禁杀 / 坏宴者押命 / 裴照临宴后再取骨”等保护规则。它证明逐章上下文能发现 continuity debt，但 Writer 自己补桥可能产生新的 world-authority drift。

第一次匿名 Judge（S1 vs B0）选 S1，总体理由主要就是连续性；B0 仍在宁烬具体性、规则清晰度等方面有可移植优点。

### B1｜Batch-5 + Chapter Handoff Continuity

- Terra high，一次写第1—5章；唯一主要新增变量是明确要求每个即时未解 Handoff 必须在下一章先接续/转化，且不得为桥接新增方便规则。
- wall：189.516s。
- runner output：10449 chars；清理模型元话语后的文件约10415 chars。
- 第4章已经把“倒悬城外门 / 断桥 / 城门”放进空间；裴照临斩桥堵路。
- 第5章直接从同一断桥继续：宁烬主动坠下，借倒悬石檐横移钻入城门缝隙；镜离/澜生用上下两处攻击挡剑；随后才进入赌命宴。
- 没有新增“城内禁杀”来保护主角，也没有改变裴照临当前真实强于宁烬的事实。

第二次匿名 Judge（B1 vs S1）总冠军选 B1：整体连读、章间因果、动作、爽点、临时规则控制均胜；S1 在“单身者”铜镜验证、岸身/海身死亡边界等规则场景化上更清楚，值得作为 craft 移植。

## 对 Production 的真实含义

本轮最重要的新证据不是“可以删 Reviser”。当前完整 production 仍是：

`Luna Director → Luna Curator → Terra Primary → Luna high Authority Reviser → Luna State`

此前真实实验已证明 Authority Reviser 目前仍是 value-bearing stage，平均约131s/章量级；本轮所有约40—75s/章或约3分钟/5章的数字都来自 **只跑 Terra Writer** 的隔离实验。

真正值得继续研究的是：**Primary 是否应该拥有一个3—5章的局部连续写作窗口。** 一次看到完整小故事，模型能提前安排空间、人物和下一章桥，而不是每章重新从局部 Plan 找解法；同时能减少五次独立调用的启动/重复上下文成本。

但下一轮必须是新的 full-chain A/B，而不是直接 productionize：冻结同一上游 Authority，至少用一部新 held-out 小说比较当前逐章 full chain 与明确 batched-Primary topology，并同时测完整 critical path、Authority hard problems、Primary→Reviser gap、跨章 Canon/State 更新、失败恢复与中途作者修改。只有这些都成立，Batch-5 才能从 Experimental Hypothesis 升成 Current Default。

## Chapter Handoff Bug 的 production 修复

这部分与 batching 实验分开，已经可以冻结：

- Outline / Review：第N章若把即时未解局面放进结尾推动，第N+1章第一个动作必须继续/解决它；若要换时空/地点，必须明确桥接。
- Director：上一章正式正文的堵路/拔刀、未脱身追杀、已落下攻击、坠落/被困、关闭中的门、必须当场回答的交易/选择，自动形成 continuity debt；先最低充分接续/转化，再进入当前章 Plan。bridge 至少包含一个可直接落正文的具体动作因果，不能只写“趁乱脱身 / 成功进入 / 摆脱追兵”。
- continuity debt 只授权 bridge，不授权 Writer/Director 新增重大胜负、奖励、关系翻转、资源或隐藏事实；真冲突继续走 `[PLAN OUTCOME ADJUSTMENT]`。
- 不新增 Agent / Reviewer / classifier / regex gate。

Focused regression：`tests/test_chapter_plan_authority.py` 11/11 PASS。真实 Luna-high Director 行为回归首轮已识别 debt 但只写“完成脱身”，因此继续收紧；第二轮明确输出“宁烬借追兵逼近迫使裴照临回剑应对，从唯一城门进入倒悬城”，使用既有追兵/地点完成具体 bridge，没有新增禁杀规则，行为 PASS。
