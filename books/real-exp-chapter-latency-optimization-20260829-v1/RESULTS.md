# TGN 章节延迟优化｜Phase 0–3 最终判定包

> 日期：2026-08-29
> 冻结样本：`books/real-exp-fast-world-20ch-20260828-v1`
> 目标：在不显著降低顶级男频长篇质量、Chapter Mission、Canon、Power/Human Authority 与 Reader Release 保真度的前提下缩短单章生成时间。
> 用户明确排除：**不修改 ACP runner；不修改“正文先显示、State 后完成”的前端流程；前端不纳入本轮。**

## 0. 最终结论

本轮要求的 **Phase 0 前五项、Phase 1、Phase 2、Phase 3 均已完成实验**。

最终 production 决策是：

- **Phase 0 已冻结进入 production**：只做由文本本身即可证明正确的确定性裁剪、raw GBrain 章节边界、合同消歧与真实耗时记账。
- **Phase 1 / 2 / 3 均不冻结**：它们确实能把相关节点缩短约 41%—78%，但最终正文盲评出现人物主动性下降、动作对象漂移、结算丢失、局部 Patch 自相矛盾、`[PLAN OUTCOME ADJUSTMENT]` 越权等问题。
- production 章节链继续保持：
  `Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`
- 本轮没有修改 ACP runner，也没有修改前端。

因此，本轮不是“优化失败”，而是得到一个可信边界：

> **确定性脏上下文可以安全删除；一旦改模型、effort、输出合同或语义路由，速度收益很大，但目前尚不能证明质量损失足够小。**

## 1. “一章约 7 分钟”到底是什么

| 口径 | 总耗时 | 平均每章 |
|---|---:|---:|
| 最终采用的五节点链 | 123.43 min | **6.17 min** |
| 加入废弃重跑、Ch1 Replan、十章 Review、终检 Repair/State rebuild | 154.53 min | **7.73 min** |
| 再把开书 World/Power/Human/Story/Outline 摊在仅 20 章上 | 176.72 min | **8.84 min** |

正常采用链的节点占比：

| 节点 | 平均 wall | 占比 | 平均 thought tokens |
|---|---:|---:|---:|
| Director | 33.9s | 9.1% | 865 |
| Curator | 116.2s | 31.4% | 4,122 |
| Primary | 55.4s | 15.0% | 355 |
| Authority Reviser | 137.3s | 37.1% | 3,491 |
| State | 27.4s | 7.4% | 147 |

Curator + Reviser 合计 **68.5% wall-clock**，也是主要 reasoning 消耗来源；真正写正文的 Terra Primary 只占 15%。

## 2. 作者判定总表

> “速度变化”只代表本次冻结样本上的 ACP wall-clock，不是 SLA；“盲评”均比较最终正文或最终可执行合同，而不是只看中间输出是否完整。

| Phase | Treatment | 样本 | 节点速度变化 | 商业读感盲评 | Authority / Canon 盲评 | 关键问题 | Production |
|---|---|---:|---:|---|---|---|---|
| 0A | 删除明确过期 Long Block | 4 章 | Curator 131.0s → 95.3s，约 **-27.2%**，波动较大 | 不改变创意 Authority | 文本范围可确定性证明 | 后十章每章删掉 2,545 个旧 1—10 章字符 | **冻结** |
| 0B | 章节 raw GBrain fail closed | 20 章账目 | 19/20 零命中；累计只接受 1 条 | 不削 Scene Skill；章节仍吃 source-blind craft | 与当前 Runtime 文档一致 | 每章检索没有稳定价值，偶发低分命中反而增加噪声 | **冻结** |
| 0C | Curator 固定合同统一为 13 区块 | 7 章 | Luna high 117.0s → 106.6s，仅作方向信号 | 7/7 结构完整 | 消除“明文列 9 项、后文又要求 4 项”的矛盾 | 属合同 bug，不是模型能力问题 | **冻结** |
| 0D | 真实批次耗时记账 | 20 章 | 建立 6.17 / 7.73 / 8.84 三种口径 | 无语义变化 | 记录 rerun / Review / Repair / fallback | 防止只报采用版本、低估真实等待 | **冻结** |
| 0E | 逐节点 tokens / wall / diff / fallback 账 | 20 章 | 建立可归因基线 | 无语义变化 | Reviser exact/similarity 不再被误当“无价值” | 以后任何快路都必须计算 fallback 总成本 | **冻结** |
| 1A | Full Reviser：Luna high → medium | 3 章 | 122.8s → 57.9s，约 **-52.8%** | **high 3/3 胜** | medium 1 胜 / high 1 胜 / 1 平 | 读感稳定下降；少数 Authority 恢复不可预测 | **拒绝** |
| 1B | Luna high Patch Reviser | 7 章 | 132.8s → 74.0s，约 **-44.3%** | full high 5 胜 / patch 1 胜 / 1 平 | 3:3:1 | 局部修复会制造全章连续性矛盾、漏 Ending 或误删场面价值 | **拒绝** |
| 1C | “安全章” Patch 路由 | 4 章 | 路由后平均约 **-16.0%** | 唯一未 fallback 章读感偏 Patch | 同章 Authority 偏 full high | **3/4 自动 fallback**，前置 Patch 成为额外税 | **拒绝** |
| 2A | 完整 13 区块 Curator：Luna high → medium | 7 章 | 117.0s → 45.5s，约 **-61.2%** | control 3 胜 / treatment 2 胜 / 2 平 | **control 5:2 胜** | 动作对象、Public Proof、战功/收益落袋会漂移 | **拒绝** |
| 2B | Slim Curator + Luna medium | 3 章 | 86.0s → 26.2s，约 **-69.5%**；Prompt 约 -53% | 1 章胜 | 0 章胜 | 某章时序冲突；另需 high Reviser 补动作链 | **拒绝** |
| 2C | Slim Curator + Terra medium | 3 章 | 86.0s → 26.0s，约 **-69.8%**；Prompt 约 -53% | 1 章胜 | 1 章胜 | 无稳定模型赢家；动作执行路径仍可丢失 | **拒绝** |
| 2D | Slim Curator + Luna high，完整接回 Primary/Reviser | 5 章 | Curator 约 **-50.3%**；完整 C+P+R 313.3s → 277.5s，约 **-11.4%** | control **3:2** | treatment **3:2** | Treatment 仍在 3/5 压力章出现力量/结算/Ending 硬问题；第2、14章整链反而更慢 | **拒绝全局上线** |
| 3 | Conditional Director Core + Modules | 5 章 | 36.7s → 21.6s，约 **-41.1%**；Prompt 约 -35.7% | **full control 4 胜 / 1 平 / treatment 0 胜** | treatment 3 胜 / control 1 胜 / 1 平 | 短版有时更守边界，但稳定削弱人物主动性和故事具体性；Ch20 又越权 | **拒绝** |
| 3B | 修正触发范围后的 Conditional Director 复验 | 5 章 | 36.7s → 23.1s，约 **-36.9%**（只占整章约 9.1% 的 Director 节点） | control **3:2** | treatment **3:2** | 第19章双盲胜出，第3章双盲失败，其余分裂；典型压力章只省 2—3 秒 | **保留研究，不上线** |

## 3. 为什么“快很多”仍不能上线

这些 Treatment 的失败不是“少了几个标题”或“文风略差一点”，而是集中发生在男频长篇最贵的少数位置：

- 主角从主动判断变成“跟随查看”；
- Mission 规定分身携带器物，正文却改成本体执行；
- 本章必须到账的矿利/护粮结算被降成“以后结算的依据”；
- 局部 Patch 修了当前句，却与后文保留句自相矛盾；
- 为了缩短 Director，滥用 `[PLAN OUTCOME ADJUSTMENT]` 把尚未完成的结果提前写成 Canon；
- 结尾从人物下一步变成 pipeline / World Expansion 调度说明。

这些错误可能只占全文数句，因此全文相似度仍然很高；但它们恰好决定：**主角有没有做成、奖励有没有拿到、能力是谁在用、下一章有没有被偷、人物是否仍像一个主动的人。**

## 4. 详细正文 / 合同对照

### 例 1｜Phase 1 Patch Reviser：局部修对一行，却制造全章矛盾

冻结全文原句：

> 唐绾把反潮记录收进自己袖中，又数了数钱袋里的潮铢，推到一旁。

Patch 为了恢复“原件仍由顾停舟携带”，只替换这一句：

> 唐绾把反潮记录重新推回顾停舟面前，又数了数钱袋里的潮铢，推到一旁。

但后文未修改，仍保留：

> “反潮记录我收下了。等我的作品出来，你可以看……”

结果是同一章同时成立“已经推回给顾停舟”和“唐绾已经收下原件”。这证明 Patch-only 并不天然更 Preservation-First：**局部锚点正确，不等于全章状态闭合。**

### 例 2｜Phase 2 Slim Curator：压缩后 Action Object 漂移

冻结 Mission 明确要求：

> 分身只携带“定住”进入第二个潮压节点，将回潮楔固定在那里。

Slim Curator 下的 Primary 一度写成：

> 它踩进泥水，双手按住裂开的地面，整个人像钉进了潮土里。
>
> 顾停舟跨过半截倒墙，把回潮楔狠狠钉进一块翻起的黑石里。

Mission 要求是**分身携楔并固定**，正文却变成**本体固定**。后续 Luna-high Reviser不得不重新补：

> 分身身上只有“定住”这一种本事，回潮楔却稳稳握在它手中。

这类补偿会吃掉 Slim Curator 的一部分速度收益；更严重的是，Reviser 并不保证每次都能重建正确交接路径。

### 例 3｜Phase 3 Conditional Director：事实更短，但主角主动性被削弱

Conditional 版本：

> 主角行动：顾停舟跟随查看新裂槽，保留原路线册，并作为现场记录的实际见证人。

完整 Director：

> 主角行动：顾停舟用原路线记录与现场裂槽、石桩和新鲜矿层对照，确认这不是旧路的局部偏移，而是已经改向的新通道；他保留原册，接受作为本次现场事实的实际见证人。

短版在 Authority 上没有大错，却把“主角通过自己已有记录作出关键判断”压成“跟随查看”。商业读感盲评因此选择完整版本。对顶级男频而言，这不是无关紧要的字数差，而是 **Agency 差**。

### 例 4｜Phase 3 Conditional Director 也有真实优点，但无法稳定路由

第 13 章完整 Director 写：

> 让前章获得的古器从战场战利品变成可带入下一阶段的真实能力。

但回潮楔仍有契约归属争议，“战场战利品”并不准确。Conditional 版本改为：

> 顾停舟以个人资金取得可实际使用的古器，而非修复资格。

同时把结尾具体保留为：

> 阮青蜃带着契约主张进入现场，准备将古器争议推向买断或封锁。

这一章 Conditional 更准确、更干净，Authority 盲评胜出。问题在于，同一套 Conditional 机制到了第 2 章削弱 Agency，到了第 20 章又越权。因此它可以继续作为研究材料，却不能成为全局 production route。

### 例 5｜Phase 3 第 20 章：为了压缩，滥用 Plan Adjustment

Conditional 版本写：

> `[PLAN OUTCOME ADJUSTMENT]` 旧关外层毁弃、居民撤离、粮道与三座新井保全及战后结算已由第19章Canon落地……

但 Canon 并没有明确完成本章仍需公开确认的：

- 砺骨部迁徙窗口；
- 首批矿脉归属；
- 相应公开结算后果。

短版随后又把结尾写成：

> `World Horizon Handoff条件成立；本章不创造第二世界事件，后续仅进入 protagonist-blind World Expansion → deterministic Current Character → Story Refresh → Outline。`

这不仅提前取消了本章结果，还让人物故事合同泄漏成 pipeline 调度语。完整版本虽然更长，却真正写清顾停舟买船、带母亲抵达远方潮市，以及各方关系怎样落定。

### 例 6｜Phase 3 第 19 章：完整版本本身也不是永远正确

完整 Director 一处写：

> 顾停舟取得镇海战局的公开战绩，并获得后续个人矿利与护粮结算的现实依据。

又写：

> 顾停舟仍保有个人矿利，但具体兑现尚待战后结算。

结尾却改口：

> 战局结束后，矿利、护粮结算和公开战绩终于落到顾停舟手里。

Conditional 版本反而直接兑现了计划要求，避免了“尚待结算 / 已经到手”自相矛盾。这个反例很重要：**实验不是证明当前 full route 永远正确，而是证明目前还没有一个可以稳定判断何时缩、缩到哪里、哪些句子不能缩的自动路由。**

### 例 7｜Slim + Luna high：同一 Treatment 可以 Authority 更准、读感却更弱

第 3 章现有 Control 写入了上游从未明确批准的契约保护：

> “若你判断风险超过契约范围，可以中止实测，交回当时记录，不算违约。”

还把兼容潮髓的世界功能直接写死：

> “它是入潮人养潮用的材料，潮性相冲较少……”

Slim + Luna high Treatment 把它收回到已批准强度：

> 契约上的字不多，约束的也很清楚：在下一次低潮前，核查新裂槽是否可短暂通行，给出实测结果；若未能按约完成，按契赔付。
>
> “矿路实测预付款在内。兼容潮髓另附登记凭条。”

Authority 盲审因此选 Slim；但商业 Reader 盲审仍选 Control，认为 Control 的少东家旧情、利益冲突与谈判节奏更自然。这里没有一个“把 Prompt 缩短就同时赢下所有维度”的简单答案：**Slim 可以消掉未授权细节，也可能同时削弱人物和现场。**

### 例 8｜Slim + Luna high：高 effort 仍会漏掉章末已经批准的动作

第 14 章 Mission 要求合作成立后**随队出发**。现有 Control 真正让动作发生：

> 顾停舟出了开炉场。
>
> ……
>
> 他踩上车辕，坐进第一辆粮车。
>
> 车轮滚过石路，朝城门方向驶去。

Slim + Luna high Treatment 却停在：

> 城南的货队还在等。
>
> 下一次十二日地潮之前，第一批粮必须送到旧关。

这不是文风偏好，而是把“已经出发”降成“准备出发”。Reader 与 Authority 两位盲审都选 Control；而这一章完整 C+P+R 还从 364.5 秒上升到 391.9 秒，说明 stronger Reviser 为补偿 Slim 输入付出了更多推理，却仍没完全恢复 Ending。

### 例 9｜Slim + Luna high：Reader 喜欢更有人的版本，Authority 仍可判结算不足

第 19 章 Slim Treatment 的人物收尾很有吸引力：

> “先回去。”
>
> “回去做什么？”
>
> “问问我娘，想不想坐潮舟。”

Reader 盲审选择了 Treatment，认为它把战绩与钱重新接回了顾停舟带母亲远行的私人欲望。但 Authority 盲审选择 Control，因为 Treatment 只写：

> “战后首笔矿利，由潮场先行折付。”
>
> “这是首笔折付。”

冻结合同要求的个人矿利/护粮结算被降成“首笔”，同时新增了潮场先行折付与损失担责规则。**一段更好看、更像人的正文仍可能在长篇状态上少结一笔关键账。** 这正是不能只用 Reader Judge 或全文相似度决定节点是否可缩的原因。

## 5. 最终冻结范围

### 已进入 production

1. 有明确章节范围的 Long Block 只在覆盖当前章时进入；过期时 fail closed，不再回退整份旧长纲。
2. Hybrid Chapter Runtime 对 raw GBrain / Reference Programs fail closed；章节只消费批准上游、safe Authority 与 source-blind Scene Skill。
3. Curator 固定输出合同显式统一为 13 区块。
4. 真实耗时账区分 adopted chain、actual batch、upstream amortization。
5. 每节点保存 Prompt chars、input/cache/output/thought、wall、fallback/adopted 与 Reviser diff 信息。

Phase 0 production commit：`7c1fc05 perf(story): bound chapter runtime context`。

### 明确没有进入 production

- Luna medium / Terra medium Curator；
- Slim Curator；
- Luna medium Reviser；
- Patch-only Reviser；
- “先 Patch、风险时 fallback high”的自动路由；
- Conditional Director；
- 删除 Curator 或跳过 Reviser；
- 新增 cheap classifier / Reviewer；
- ACP runner、执行后端与前端改动。

## 6. 当前用户可据此作出的判断

| 选择 | 实际含义 | 本轮证据 | 我的判断 |
|---|---|---|---|
| A｜质量优先 | 只保留 Phase 0，production 路由不降档 | 无稳定语义退化；速度收益主要来自去脏上下文和减少未来误跑 | **已采用，推荐** |
| B｜实验性快路 | 手动对特定章节试 Patch/Slim/Conditional，结果仍须逐章对照 | 单节点可快 40%—78%，但没有可靠自动路由 | 保留实验，不做默认 |
| C｜全局低延迟 | Curator/Reviser/Director 全面降档或瘦身 | 会稳定牺牲部分 Agency、Payoff、Action Object 或 Authority | 不应上线 |

## 7. 尚未声称的事情

- 没有重新跑一整本 20 章的 Phase 0 后 E2E，因此不能宣称 production 已从 6.17 分钟稳定降到某个新数字。
- 四章 stale-context A/B 的平均下降是方向证据，不是 SLA；ACP 排队波动明显。
- Phase 1–3 中确有个别 Treatment 胜出，不能概括成“短 Prompt 一定差”；只能说**当前自动路由无法稳定识别那些安全样本**。
- 本轮按用户要求没有改 ACP runner，也没有动前端；它们不是“尚未完成的交付项”。

## 8. 证据位置

- Phase 0 真实账：`phase-0-runtime-accounting/PHASE0_ACCOUNTING_REPORT.md`
- 风险来源：`RISK_SOURCE_TABLE.md`
- Curator medium 完整合同：`phase-h-curator-medium-contract-fixed/` + `blind-judges-curator-medium-contract-fixed/`
- Reviser medium：`phase-d-routine-reviser-medium/` + `blind-judges-reviser-medium/`
- Patch high：`phase-j-patch-reviser-high/` + `blind-judges-phasej-patch-high/`
- Safe Patch route：`phase-1b-safe-patch-reviser/` + `blind-judges-phase1b-safe-patch/`
- Slim Curator：`phase-2-slim-curator/` + `blind-judges-phase2-slim/`
- Slim Curator medium 完整下游复验：`phase-2-slim-curator-medium/` + `blind-judges-phase2-slim-curator-medium/`
- Slim Curator Luna high 完整下游复验：`phase-2b-slim-curator-high/` + `blind-judges-phase2b-slim-curator-high/`
- Conditional Director：`phase-3-conditional-director/` + `blind-judges-phase3-director/`
- 修正触发范围后的 Conditional Director：`phase-3-conditional-director/` + `blind-judges-phase3-conditional-director/`

## 9. Final Verdict

**Phase 0：PASS / FROZEN。**
**Phase 1：FAIL AS PRODUCTION ROUTE。**
**Phase 2：FAIL AS PRODUCTION ROUTE。**
**Phase 3：PARTIAL INSIGHT / FAIL AS PRODUCTION ROUTE。**

本轮最可靠的系统结论不是“多 Agent 都不能优化”，而是：

> **TGN 的延迟主要来自 Curator 与 Reviser，但它们保护的恰好是少数高价值语义。下一次优化必须继续把稳定规则确定性编译掉，而不能仅靠更短 Prompt、更低 effort、局部 Patch 或条件模块去猜哪些语义可以丢。**

## 10. Validation

- Phase 0 focused regression：`210 passed`。
- 全项目回归：`373 passed`。
- `tgn-system-steward` 已升级为 **0.3.10**，新增 latency / cost causal audit；AgentDock package validate 通过，digest：`sha256:ccf1a1cd045bbcddbbedcd9a5d8bc78a8e895fb7aae8070310237d7c14e3dcdf`，已 install + activate。
- 0.3.10 bounded read-only smoke 正确判定“全局 Curator medium”与“按相似度跳过 Reviser”均为 `FAIL`，只允许冻结 stale Long Block / raw GBrain fail-closed 等确定性根修，符合已知结论。
- `git diff --check` 通过。
