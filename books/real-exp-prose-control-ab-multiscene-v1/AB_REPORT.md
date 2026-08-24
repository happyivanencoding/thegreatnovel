# Prose Control Multi-Scene A/B — 2026-08-24

## Question

在保持同一 Chapter Mission / Canon / BOOK Prose Profile / GPT-5.6 Terra high Primary Writer 的前提下，仅增加 1 张 Scene Prose Control，是否稳定改善正文？

## Design

4 个不同 Scene Family：

1. Dialogue / Negotiation：回灯集 Chapter 4，入集资格与路线价值谈判；control=`dialogue-state-pressure-v1`。
2. Action / Pursuit：Chapter 6，陆砚诱敌进入错误支路并脱身；control=`spatially-traceable-causality-v1`。
3. Payoff / Public Proof：青崖宗公开升院考核 Chapter 3；control=`payoff-consequence-conversion-v1`。
4. Entry / Opening / Exploration：Chapter 1，矿井坍塌绝境与第一次开路；control=`action-anchored-grounding-v1`。

每组 OFF / ON 使用相同冻结 Primary Prompt；机械 SHA 检查确认 control test block 之前全文完全一致。ON 只多出 1 张由 TGN `extract_abstract_content()` 生成的中文 Prose Control 摘要。8 路均使用 GPT-5.6 Terra high。最后使用 1 次 GPT-5.6 Luna high 联合 blind judge，组内 X/Y 随机打乱，judge 不知道 ON/OFF。

## Blind Result

| Scene | OFF | ON | Δ ON | Blind winner |
|---|---:|---:|---:|---|
| Dialogue | 8.5 | 8.2 | -0.3 | OFF |
| Action | 8.3 | 8.7 | +0.4 | ON |
| Payoff | 8.6 | 8.6 | 0.0 | TIE |
| Entry | 8.8 | 8.5 | -0.3 | OFF |
| **Mean** | **8.55** | **8.50** | **-0.05** | — |

所有单项置信度均为 medium。产品判定：**KEEP OPTIONAL**。

## What improved

### Action — clear positive

ON 的动作空间链更容易复原：灯阵外门 → 墙下旧路 → 错误支路 → 裂缝 → 逆潮路 → 水槽 → 黑市内圈。敌方对“旧关卡与灯线锁不住陆砚”的新判断也更明确地转成“必须活捉”的策略变化。

确定性指标同样支持：

- Primary body chars：3219 → 3596
- abstract-term hits：9 → 6
- action-verb hits：19 → 35
- single-sentence paragraph ratio：0.716 → 0.673

这说明 `spatially-traceable-causality` 确实能让复杂追逐的接触、方向、位置和后果更清楚，而不是只让文字更长。

仍有风险：ON 操作细节也更密，局部会让胜利像“机关技巧/路线机制说明”，紧迫感受到影响。因此当前只能标记 **PROMISING / NEEDS ONE MORE ACTION SAMPLE**，不能单样本冻结。

## What did not improve

### Dialogue — control introduced boundary drift

OFF 更完整地完成“拒绝入集 → 展示旧渠价值 → 扣押而非交人 → 谈药与保护 → 追加交易”的价格变化，底线对白也更直接改变筹码。

ON 虽更生活化，但：

- 守门人没有真正确认旧渠可通就进入后续；
- 把后续交换具体化为冻结 Mission 没有明确写出的“带货”；
- 对话控制的“筹码/报价/关系重定价”容易诱使 Writer 补造新的谈判事实。

因此 `dialogue-state-pressure` 目前不适合默认注入；它需要更短、更强调“只从已有 Canon/Plan 找筹码，不新增筹码”的 projection。

### Payoff — redundant with existing prose rules

两版都完成公开结果，blind judge 判 TIE。

ON body 更短（2786 → 2326 chars），但 abstract-term hits 从 2 → 9。说明 control 并没有稳定减少解释，反而可能与现有 Reader-First / Human Reaction / Public Proof 规则重复，引出更多“这代表什么”的显式说明。

当前 `payoff-consequence-conversion` 的增量价值不足，不应自动 ON。

### Entry — over-execution and mechanism load

OFF 第一段更快落到坍塌、受伤、定责和处死，规则都在即时危险中出现；blind judge 给 OFF +0.3。

ON：

- body chars：2822 → 3317
- abstract-term hits：5 → 9
- action verbs：35 → 39

也就是动作更多，但解释和新增机制负担也更多。`action-anchored-grounding` 与当前 Primary 已有的“动作先于术语 / Reader-First / Story-bearing Texture”高度重叠，因此全卡注入容易过度执行。

## Cross-scene conclusion

这次 A/B 不支持“Prose Control 默认 ON”。

真正得到的结论是：

1. **Prose DNA / Prose Controls 有价值，但应保持 OPTIONAL。**
2. **不同 Scene Family 的边际收益不同。** Action 当前最强；Payoff 近乎冗余；Dialogue/Entry 可能因为过强控制而发生事实补造或机制扩写。
3. **问题不一定是 mechanism 错，而是 projection 太厚。** 本实验把 `extract_abstract_content()` 的整段 Control 摘要投给 Primary；真实 Curator 更适合把 control 压成 2—4 句当前场景专用的 soft reminder。
4. 生产边界继续保持：默认 1 张；但“能检索到”不等于“每章自动注入”。
5. 下一轮最便宜、最有价值的实验不是再测全部 7 张，而是：
   - Action：再找 1 个不同动作场景复验 `spatially-traceable-causality`；
   - Dialogue / Entry：测试 **compressed projection**（2—4句）是否消除 boundary drift / over-explanation。

## Product Decision

**KEEP OPTIONAL**

- 不 FREEZE 全局 ON。
- 不 REJECT Prose Craft。
- 保留 Curator Scene Family 检索与选择能力。
- 当前不把“每章自动查询并注入 Prose Control”冻结为默认生产行为。
- `spatially-traceable-causality-v1` 标记为最值得单独复验的候选。

## Artifacts

每组目录包含：

- `prompt_OFF.md`
- `prompt_ON.md`
- `OFF.json` / `ON.json`
- `OFF_response.md` / `ON_response.md`
- `OFF_body.md` / `ON_body.md`
- `control_abstract.md`

根目录另含：

- `blind_judge_prompt.md`
- `blind_judge.json`
- `blind_key.json`
- `metrics.json`
