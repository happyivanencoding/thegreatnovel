# RESULTS｜Power Spark × Privilege Delta

## Verdict

**PASS for the targeted system change.**

Power Novelty Spark 能拉开候选起点，但本身不保证金手指够强。加入 `Privilege Delta + persistent reader ruler + conditional cross-tier + compoundability` 后，Luna 明显更主动把异常写成“同层别人做不到什么、主角提前拥有哪种高层特权”，而不是只写新奇操作方式。

最终 B3 同时满足：

- Spark 单一异常仍真实成立；
- 三个候选都有明确同层/越级比较；
- 比较使用 World 已有境界/战绩等 ruler，不另造总战力分；
- 没有新增“超标坐标/评分表”等 schema 字段；
- 长期成长开始考虑功法、兵器、环境等复合，而不只数量/距离膨胀。

## Why this change exists

指定小说 `real-exp-private-prototype-fresh-novel-20260826-v1` 的主观审计与作者反馈一致暴露两件事：

1. 「落景」虽然有辨识度，但早期只是“留下一点风继续推东西”，`Novelty` 没有转化成足够大的力量欲望。
2. World 虽然定义了力量层级，正文却没有持续使用 ruler 告诉读者“主角现在在哪档、哪里超标、下一档多远”。

而「落景」实验早于 `62acc48 feat(power): add novelty spark sampler`，因此不能用旧小说直接判定新 Spark 机制失败。

## GBrain evidence read before the fix

- 《斗罗大陆》Story Craft：主角优势不是单一技能，而是知识、双生武魂/先天异常、魂环魂骨、血脉重释、关系力量、神级传承的层叠；不同阶段用魂环、比赛、血脉、身份、神考等不同 ruler 重新证明“这次为什么超标”。
- 《不科学御兽》Story Craft：同时使用成长等级、种族潜力、技能熟练度、能量值、职业等级、实战证明、公共身份等交叉 ruler。读者持续能问：几级、潜力多高、技能练到哪、能不能越级、打过谁。
- 《极道天魔》Story Craft：强金手指的价值首先是 Action Possibility Jump——原本只能逃，现在能杀；原本碰不到，现在能打伤；原本只能服从规则，现在能破掉规则。旁观者与敌人会据此重新估价主角。
- Reader Coordinates 跨书 synthesis：**没有 ruler，升级只是名词；只有绝对 ruler，又会退化成机械换算。** 稳定做法是主尺 + 必要校准尺 + 真实结果交叉证明。

Production Power retrieval 本轮实际接受：

- `syntheses/reader-facing-world-coordinates-batch-d-v3`
- `book-dna/rcv0-06-xianxia-xiaoxingji`

## Controlled setup

冻结：World、Power GBrain bundle、Novelty Spark、Luna high、fresh session。

固定 Spark (`seed=20260826`)：

1. 驭使造物 × 每个目标需要独立注意力
2. 借用别人最擅长的一件事 × 只能拿走对方此刻正在使用的部分
3. 临时适配当前处境 × 变化结束后保留一点永久痕迹

### A｜Spark only

候选：`离身操控 / 截用现招 / 留痕适形`。

优点：都比旧「落景」更容易一句话理解，也有基本欲望。

不足：比较优势多为隐含。尤其没有稳定回答“同层普通人/天才怎样、主角具体超标多少”；越级价值和社会可见尺度不够主动。

### B｜First Privilege treatment（rejected refinement）

尺度和越级意识明显增强，但 Candidate 1 把 Spark 的“每件目标都需要独立注意力”反写成“不会抢走我的注意力”。

结论：**强度不能靠删除 Spark 条件获得。**

### B2｜Privilege + Spark fidelity

修复上面问题，Candidate 1 恢复独立注意力成本；三个候选都主动给出同层比较与越级意义。

新问题：模型自行增加 `### 可见超标坐标` 字段，说明比较原则可能诱发 schema 膨胀。

### B3｜Final treatment

增加“不新增比较字段，只在既有段落中自然说明 ruler”的边界后，输出结构恢复干净。

三个候选：

1. **分身兵**：多件兵器像多双手同时战斗，但每件真实占用一份注意力。同境从“一人一正面”变成“一个人同时占多个战斗位置”；越级时可打断、牵制、逼位。
2. **截景**：对手正在施展某段力量时，主角能暂时截走其中正在运行的关键部分。最强的幻想点是：**更高境界的敌人出招，反而可能把一个高层效果送到低境界主角手里，制造真实越级反杀窗口。** 但不能偷境界、潜力或未施展能力。
3. **留痕化身**：身体会对真实接触的极端环境临时适配，并永久留下少量改变。同境修士必须绕开的高阶景域，主角可能短暂闯入；后期旧痕与功法/身体结构产生复合。

## What changed in production

- Power Seed：`Novelty ≠ Power Fantasy 强度`；要求明确 `Privilege Delta`。
- Power Seed：允许有条件越级；Permanent Boundary 防万能，不负责把优势削平。
- Power Seed：Spark 的单一异常不能被 treatment 偷删或反写。
- Power Seed：长期要能与功法、兵器/法宝、身体/血脉、环境、传承等产生新化学反应。
- World Vision：至少建立一把会被社会真实使用、可长期复用的力量主尺。
- Story Program / Outline / Director / Review：突破、新能力/装备、公开验证、新强敌、越级结果、世界换挡后，自然刷新 reader ruler。
- Primary Writer 不接这条系统规则，不允许临时发明等级/数字。
- GBrain Power retrieval aliases 增加 `core reader fantasy / power dominance / power verification / public proof / ability delight`，不增加 retrieval 条数。

## What this did not solve

- Spark 家族本身仍有天然强弱差。B3 的「截景」明显比「留痕化身」更有即时支配感；系统不应为了让三个候选平均而削平差异。
- 这次只证明 Power candidate distribution 的目标改善，**没有重新生成 World / Character / Story Program / 正文**。
- Persistent ruler 是关键换挡后的重新校准，不是每章播报数字，也不是单一“战力值”。
