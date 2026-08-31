# Batch Production Final Report

日期：2026-08-31
状态：FINAL DECISION（Direct Future-10 held-out 结果在本文末节记录）

## 1. 用户侧结论先行

这轮不再讨论“要不要保留 Batch”。Batch 4—6 章连续写作窗口正式视为小说质量资产，默认 5 章。问题从“Batch 会不会有细节漂移”改成：怎样让 Authority recovery 看见整批、只修真正不能错的地方，而不把 Terra 的小说正文重新写成说明稿。

## 2. 第一轮：为什么 `Batch Primary → 逐章 Reviser` 失败

同一冻结上游、镜海界前五章：

| Topology | Equivalent full-chain wall | 结果 |
|---|---:|---|
| 当前旧逐章 full-chain | 2104.231s | Authority 稳，但像五章分别完成 |
| Compact Batch Primary + 5×逐章 Reviser | 2124.256s | FAIL：Primary 快，但后章 stale 使 Reviser 更重 |

Primary 本身由约 261.8s 降到 184.7s（约 -29.5%），但 Reviser 由 735.6s 升到 836.2s（约 +13.7%）。第5章 Primary→Final 相似度只有约 76.8%，说明前章逐章 finalization 会不断使后章预写稿失效。

结论：失败的是 **Authority finalization topology**，不是 Batch narrative window。

## 3. 第二轮：整批全文 Reviser 也不是答案

让 Luna-high 一次看到完整 5 章并重输全文，Reviser wall 降到约 331s，等价 full-chain 约 1621s；增强 final sweep 后约 1596s。Authority 明显改善，但 Story blind 明确指出：解释、总结、Reward 交付流程重新浮到页面，小说味下降。

结论：Reviser 必须看完整 Batch，但不该重新生成完整 Batch。

## 4. 冻结关键：Batch Authority Delta

新方法：

`Batch Primary → Reviser 看完整5章 + Authority → exact OLD→NEW local patches → 代码应用 → untouched prose 物理保留`

同时增加两个边界：

1. 同一事实域出现一个 Authority 冲突后，必须跨章扫描所有依赖位置，例如旧火屑返还 + 新火屑奖励、天海上下空间轴。
2. 若修复需要新增传送、追踪、世界机制、重大胜负、身份或奖励，Reviser 不得“聪明补洞”，必须返回 `upstream_conflicts`，回 Story / Outline 修最早根因。

镜海样本 Luna-high Delta：140.979s，只改 4 处 / 296 chars；等价 full-chain 约 1431.071s，Story blind 排第一。

## 5. Cross-book held-out

在完全不同的 `real-exp-game-instance-rse-5ch-20260829-v2` 上，用同一原则重新生成：

- Terra-high Batch Primary：199.138s；
- Luna-high Batch Delta：185.687s；
- 只改 4 处；
- Story blind：Batch+Delta 胜；
- Authority blind：Batch+Delta **0 hard problems**；旧逐章 full-chain 对照被抓到 4 个 hard problems。

因此 Batch Delta 不是镜海单书过拟合。

## 6. Reviser 模型 / effort 矩阵

同一镜海 Batch Primary：

| Reviser | wall | patches | 观察 |
|---|---:|---:|---|
| Luna-high | 140.979s | 4 | 有漏项，也有不必要前置补写 |
| Terra-high | 28.791s | 3 | 过轻 |
| Sol-high | 147.647s | 6 | Authority 覆盖完整且较克制 |
| Terra-max | 160.531s | 6 | 覆盖强，但包含无授权 access patch |
| Terra-ultra | 444.849s | 6 | 未证明相对 max 的补偿性收益 |
| Luna-max | 558.572s | 10 | overrepair 倾向 |

独立 **Sol-max Patch Adjudicator** 不按模型名评分，先自行重建真实 hard problems，再判 proposals。结论：合法 patch 子集排序 **Sol-high > Terra-ultra > Terra-max > Luna-max > Luna-high > Terra-high**。

特别重要：所有版本为裴照临自行发明“剑意追入镜海”的 patch 都被判越权，因为 Frozen Plan 从未授权跨界机制。正确动作是 upstream conflict，不是 Reviser 造机制。

冻结模型：**Sol-high Batch Authority Delta**。Max / Ultra 保留诊断，不成为默认税。

## 7. Batch Director 实验：Story 赢，但不冻结

为了进一步减少逐章 Director/Curator 重启，测试了：

`Luna Batch Director → Terra Batch Primary → Authority Delta`

held-out 的 Story blind 把这版排第一，证明短中程规划视野确实有小说价值；但 Batch Director 自己重新解释了已批准 Outline，造成：

- 界阶1时序提前；
- 试火炭与明擂奖励炭来源混同；
- 返照环首次记录 / 更远跃越时序被改写。

换 Sol-high Delta 后 Story 仍第一，但 Authority 仍认为这些是 P0，因为根因已经进入 Primary 的主事件时序，不能靠局部 patch 合法恢复。

结论：**不要为了 Batch 再增加一个规划 LLM。** 已批准 Future-10 本来就是这五章的故事 Authority。

## 8. 最简 production 候选

最终候选改为：

`Approved Outline / Future-10`
`→ deterministic 抽取当前 4—6 章（默认5）`
`→ 复用 Chapter Context compiler 叠加 Frozen Power/Human + safe World + Reader Release + Protected RSE + Book Contract + BOOK Prose Profile + starting Canon + active Long Block`
`→ Terra-high Batch Primary`
`→ Sol-high Batch Authority Delta`
`→ upstream_conflicts == 0 才整批采用`
`→ Luna-low State 按最终正文逐章落盘`

这条 topology 删除了会重新解释 Authority 的 Batch Director，同时保留 Batch 写作窗口与整批 Authority 修复窗口。

## 9. 从用户成品评价吸收的系统修正

已进入 Prompt / runtime 原则：

- **Access Provenance**：前文关门/断桥/拒绝入境后，后两三章也不能无因果出现在另一侧；Reviser 不得自行发明剑意追踪、备用门、秘密接引。
- **Premise Identity Payoff**：如果真正卖点是“带走并复合世界可能性”等独特操作，第一自然 Horizon 结束前至少完整兑现一次；普通掉宝、资格、地图不能长期替代。
- **World Rule → Lived Consequence**：强世界规则至少要制造一个只有该规则存在才成立的人物欲望、关系、身份或命运，不只作为战斗/赌局玩法。
- **Trait Saturation**：爱钱/好胜等已经成立后，不持续用同义口癖证明；让其它 Frozen Human 牵引和具体关系进入选择。
- 原有“漂亮二段论不得重复成章法”继续生效。

## 10. Final Decision

- **Batch Narrative Window：STRONG PASS / FREEZE。** 默认 5 章，支持 4—6 章；没有证据要求为了安全退到 4 章。
- `Batch Primary → per-ch Full Reviser`：**FAIL**。
- Whole-Batch Full-Text Reviser：**PARTIAL**，Authority 有效但会磨掉小说味。
- **Whole-Batch Exact Authority Delta：PASS / FREEZE。**
- Batch Director 重新规划 Approved Future-10：**FAIL as default**；可保留研究入口。
- Reviser default：**Sol-high**。Terra/Luna Max/Ultra 不因“更强”自动采用。
- 单章 `Director → Curator → Primary → Full Reviser → State`：保留 fallback / 专项实验，不再作为默认长篇正文拓扑。

## 11. Full Deterministic Packet held-out｜最终确认

最后不采用“薄 Future-10 直接丢给 Writer”，而是复用现有 deterministic Chapter Context Compiler，在**不增加新 LLM Planner**的前提下，把 Approved Future-10 与已经存在的 Authority 一起编进当前 5 章：

- Frozen Power / Human；
- safe Effective World；
- Reader Release；
- Protected RSE；
- Book Contract；
- BOOK Prose Profile；
- starting Canon；
- active Long Block；
- Future-10 原始逐章 Event / Result / Ending。

随后运行：

`Full Deterministic Packet → Terra-high Batch Primary → Sol-high Batch Authority Delta → Luna-low State ×5`

真实结果：

| 节点 | wall |
|---|---:|
| Terra Batch Primary | **202.753s** |
| Sol-high Batch Authority Delta | **1103.588s** |
| Luna-low State ×5 | **136.114s** |
| **完整 production wall** | **1442.455s = 24分02秒** |
| 旧逐章 full-chain | **2104.231s = 35分04秒** |
| **wall reduction** | **31.45%** |

Primary 8632 chars，最终 8685 chars；Reviser 使用 18 个 exact local patches，`upstream_conflicts = 0`。18 个 patch 主要集中在复杂的 Ch1 RSE/点灯时序、Ch2 精确 Public Proof 与 Ch3–4 少量位置/未知边界；Ch5 没有出现此前 `Batch Primary → per-ch Reviser` 那种随章节距离增长的大规模 stale 返工。

四路独立 Authority blind：

> **A（Full Deterministic Packet） > B（复用逐章 D/C 的 Batch+Delta） > C（旧逐章 full-chain） > D（薄 Future-10 Batch）**

A：**0 P0 / 0 P1**。RSE、灯阶/界阶、试火炭与奖励炭、灯阶7校准、返照环材质与首次异位重放、断桥后远跃、人物命名和资产链全部对齐。

四路 Story blind：

> **A > D > B > C**

Judge 明确认为 A 最像已进入正式连载状态的正文：Authority 先进入现场并推动动作，而不是事后说明；动作因果、Reward、章间承接与追更欲也最好。

### Final Freeze

正式默认拓扑冻结为：

`Approved Outline / Future-10`
`→ deterministic 4—6章 Authority Packet（默认5）`
`→ Terra-high Batch Primary`
`→ Sol-high Batch Authority Delta`
`→ upstream_conflicts == 0 才整批采用`
`→ Luna-low State 按最终正文逐章落盘`

不冻结 LLM Batch Director；不把薄 Future-10 当完整 Packet；不回到逐章 Primary；不因为 small drift 把默认 Batch 从5章保守降为4章。4章与6章作为同一 runtime 的允许窗口，具体窗口可在未来真实长篇中按自然故事边界调整。
