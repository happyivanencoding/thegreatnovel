# Batch-5 Primary 正式 Full-Chain 实验报告

日期：2026-08-31
实验目录：`books/real-exp-batch5-full-chain-20260831-v1`
结论：**PARTIAL PASS；Batch-5 叙事窗口成立，但当前“只 Batch Primary、其余仍逐章”的拓扑不进入 Production。**

## 1. 要回答的问题

前一轮 Writer-only 实验显示，Terra high 一次连续写 5 章，在修好 Chapter Handoff 后，速度和短中程连续性都优于 5 次逐章 Writer。但那一轮没有 Director / Curator / Authority Reviser / State，不能代表 Production。

本轮固定同一套 World / Character / 五章 Plan，正式比较：

- Control：当前 Production 的逐章链
  `Luna-high Director → Luna-high Curator → Terra-high Primary → Luna-high Authority Reviser → Luna-low State` × 5
- Treatment：复用 Control 已生成的五份 Director + Curator Authority packet，只把 5 次 Terra Primary 合成 1 次 Batch-5 Primary；之后仍按章运行 5 次 Authority Reviser + 5 次 State，并让 Treatment 自己的最终正文滚动成为 Canon。

这样隔离的主要变量是 Primary 的认知窗口。Director / Curator 在 Treatment 中复用 Control 输出，因此 Treatment 的“同 D/C 成本等价时间”是公平估算，不是假装已经实现了新的 live critical path。

## 2. Control：当前逐章 Full Chain

五章节点 wall 总和：

| Stage | 5章 wall |
|---|---:|
| Director | 319.020s |
| Curator | 660.808s |
| Primary | 261.804s |
| Authority Reviser | 735.571s |
| State | 127.028s |
| **合计** | **2104.231s / 35m04.2s** |

Control 说明了一个重要事实：正式链的延迟并不主要来自 Terra Primary。Director + Curator 已占 **979.828s / 46.6%**；复杂章的 Authority Reviser 也非常重，第4、5章分别约 200.3s、214.8s。

Control 最终五章约 12,903 字符。第4→5章 Handoff 修复真实生效：第4章裴照临斩断浮桥堵路，第5章从同一现场继续，宁烬借断桥、倒悬城外墙石檐、镜离的镜光、澜生引来的黑舰完成具体脱身，没有瞬移，也没有新增“城内禁杀”。

Control 仍出现两个局部风险：

- 第3章先写澜生“骨舟在我们手里”，第5章又把“骨舟”作为宁烬赌宴所得；若没有明确是另一艘，这会削弱 Reward 的首次取得，至少形成资产连续性歧义。
- 第1章正文让裴照临公开竞价到“两百万”，第2章却按冻结 Plan 用“十万灵玉 + 洞府”私下收购，正文没有解释为何突然降价。它不是系统 Authority 硬冲突，但读感上不够顺。

## 3. 第一版 Formal Batch：INVALID

第一次 Treatment 把五份完整 Primary Runtime Prompt 机械拼接：Prompt 达约 **151KB**。Terra high 只用 105.556s 就完成五章，但总输出被压到约 5,896 字符，进入“完成五个任务”的摘要化模式。

虽然按相同 D/C 成本折算约 1738.797s，看似比 Control 快约 17%，匿名正文 Judge 明确判 Control 大胜：Batch 稿把本应场景化的动作、奇观、人物和 Reward 压成了剧情摘要。

因此这不是 Batch-5 topology 的有效反证，而是**重复上下文造成的注意力 / 输出带宽坍缩**。该 Treatment 判 `INVALID`，不能用它的速度支持 Production 决策。

## 4. Compact Batch-5：有效 Treatment

第二版只给一次共享 World / Character / 五章 Block，每章重复真正章特异的：

`Approved Chapter Plan + Luna Director + Luna Curator`

Prompt 降到 **57.9KB**。

Terra-high Batch-5 Primary：

- wall：**184.704s**
- 五章 Primary 正文：约 **9,253 字符**（单章 1817 / 1405 / 1666 / 1499 / 2866）
- 输出总 response：约 9,810 字符

它恢复到了正常小说展开区间，也重新出现了上一轮 Batch 的短中程优势。例如：

- 宁烬更有人味：`“这东西要是从自己眼前飞过去，他以后睡觉都得把自己气醒。”`
- 裴照临的压迫不仅靠报等级，而是通过“门没有接纳他，却接纳了宁烬”“城里见”等持续存在。
- 第4→5章直接从断桥继续：宁烬踢碎石栏扰追兵，镜离上石檐挡人，澜生把黑舰拖到城门下，裴照临被迫停半瞬，宁烬抓断桥索荡入城。没有临时新增世界规则。

### 4.1 最终 Full-Chain 时间

Compact Batch 后仍逐章跑 Reviser + State：

| Stage | wall |
|---|---:|
| Batch-5 Primary | 184.704s |
| 5× Authority Reviser | 836.197s |
| 5× State | 123.527s |
| Treatment 实际跑出的 post-D/C | 1144.428s |
| 加回 Control 相同 Director + Curator 成本后的等价总和 | **2124.256s / 35m24.3s** |
| Control | **2104.231s / 35m04.2s** |

即：**当前拓扑反而慢约 20.0s / +0.95%**。

Primary 本身确实省了：

- Control Primary：261.804s
- Batch Primary：184.704s
- 节省：**77.100s / 29.5%**

但 Reviser 被拖重：

- Control Reviser：735.571s
- Batch Reviser：836.197s
- 增加：**100.626s / 13.7%**

Primary 的节省被后续 Reviser 返工全部吃掉。

## 5. 为什么 Reviser 变重

Reviser 的改动量从前往后显著增加：

| 章 | Primary→Final similarity | edit blocks |
|---|---:|---:|
| 1 | 0.9571 | 10 |
| 2 | 0.9465 | 15 |
| 3 | 0.9482 | 24 |
| 4 | 0.9110 | 27 |
| 5 | **0.7678** | **112** |

第5章是最清楚的例子。Batch Primary 在第1—5章一次性预写时，还没有第1—4章经 Reviser + State 后最终定真的 rolling Canon，因此更容易提前决定细节。真实出现了：

- 把第4章已有白昼火屑拿去前几轮赌局并输掉，再在最终赌局赢回来；Frozen Plan 没批准这个资产变化。Reviser 必须删除这条支线，改成输掉普通随身小物。
- 为赌具、真实航线载体等补了比 Authority 更具体的实现；Reviser 又需要回收或压缩。

这就是当前 Batch-5 与逐章 Authority Finalization 的结构摩擦：

> **Batch Primary 的后几章是在“未来 Canon 尚未定真”时写出的；而 Reviser / State 仍然逐章改变最终事实与实现。**

越往后，预写稿越可能需要 rebase。

## 6. 最终质量

### Story Blind Judge

匿名 Luna-high 把 Compact Batch 标为 A、Control 标为 B，结论是：**A / Compact Batch 小胜**。

它认为 Compact Batch 更强的地方包括：

- 连续阅读欲；
- 宁烬的具体人格与对白；
- 二照妖兽战的动作因果；
- Reward 兑现；
- 裴照临持续压迫；
- 4→5章桥接；
- 更少“规则说明替代戏剧”。

Control 在镜海公共规则第一次解释上稍清楚。

因此，前一轮 Writer-only 看到的 **“5章左右是有价值的短中程小说认知窗口”** 并没有被 Full Chain 推翻；它在最终正文里仍可见。

### Authority Blind Judge

匿名 Terra-high Authority Judge 把 Control 标为 A、Compact Batch 标为 B：

- Control：0 个 Judge 判定的 Hard Problem
- Compact：1 个 Hard Problem

Compact 第3章镜离说：

> “成交。但门骨暂时不能离开你手。”

Frozen Authority 只允许“宁烬当前持有 / 对门有特殊适配”，没有授权“门骨物理上不能离开他手”的规则。这里为了稳定合作状态，Writer 把人物选择偷换成了世界机制。Reviser也没有清掉。

正确实现应是“门先留你手里 / 暂时由你拿着”，而不是新增绑定规则。

所以 Compact Batch 的 Story 增益是真实的，但 Authority 可靠性目前还没有达到可以替换 Production 的水平。

## 7. 结论

### Narrative Hypothesis

**DIRECTIONAL PASS / 强 positive。**

五章连续认知窗口确实能改善：

- 短中程铺垫与回收；
- 跨章动作连续性；
- 人物声音延续；
- Rival 压迫的持续感；
- 世界规则从“说明”变成连续使用。

这不是单纯为了提速的 batch trick，而可能是更接近小说作者短中程工作记忆的写作窗口。

### Current Production Replacement

**FAIL。当前不采用 `5×D/C → 1×Batch Primary → 5×Reviser/State` 替换默认逐章链。**

原因非常具体：

1. Full-chain 等价时间没有下降，反而 +0.95%；
2. Primary 虽快 29.5%，Reviser wall 却增加 13.7%，把收益吃光；
3. 后章 Primary 在 rolling Canon 定真前预写，Reviser edit burden 从 Ch1 到 Ch5明显扩大；
4. Compact Batch 最终仍残留 1 个真实 Authority overreach；
5. 本轮仍只有一本书，不足以升级为稳定 Production 结论。

## 8. 下一步最值得测试的方向

不要删 Reviser，也不要继续把五份完整 Runtime 粗暴塞给 Terra。

真正值得测试的是：

> **把“5章短中程叙事窗口”提升到一个更完整的局部 Production Packet，而不是只 Batch Writer。**

下一个实验应优先回答：是否能让五章的 Director / Curator 共享一次局部故事模型与非重复 Authority，同时让 Authority Finalization 不把后四章变成 stale draft。候选可以研究“5章 compact planning packet + Batch Primary + 能看到整批的 Authority finalization”，但任何 Batch Reviser / Reviser topology 都必须重新证明 Authority hard problems 不增加，不能因这次 Story Judge 喜欢 Batch 就直接采用。

尤其值得注意：Control 的 Director + Curator 本轮占全链约 **46.6%**。如果未来要真正提速，最大理论空间很可能不只在 Primary；但 D/C batching 尚未测试，不能从本轮直接推导为安全方案。

## 9. What This Did Not Solve

- 没有测试 full Batch Director / Curator；
- 没有测试 Batch Authority Reviser；
- 没有测试第二本 held-out 小说；
- ACP runner 本轮 `usage=null`，因此没有可靠 credits / token 成本比较；
- 没有证明 Batch-5 的最佳窗口一定是 5，而不是 3 / 4；
- 没有改变当前 Production 默认。

当前 Production 仍保持：

`Luna Director → Luna Curator → Terra Primary → Luna-high Authority Reviser → Luna-low State`
