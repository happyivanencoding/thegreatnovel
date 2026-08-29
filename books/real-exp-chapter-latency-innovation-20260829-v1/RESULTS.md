# TGN Chapter Latency Innovation｜最终实验报告

> 日期：2026-08-29  
> 冻结主样本：`real-exp-fast-world-20ch-20260828-v1`  
> 跨书样本：`real-exp-current-pipeline-authority-reviser-0010-20260828-v1`  
> 目标：**在不削弱主角主动性、人物欲望、Power Asymmetry、Public Proof、Reward/Ownership、Ending 与 Canon 的前提下，让章节更接近顶级男频，同时缩短生成时间。**

## 0. Final Verdict

本轮没有发现一条可以安全替换当前 production 五节点链、同时带来大幅加速的语义路线。

当前默认继续保持：

`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`

这不是因为现有链永远最优，而是因为所有大幅快路都呈现同一种分裂：

- 把 Authority 前移或压缩后，事实更稳，但人物现场、关系与商业爽感变薄；
- 把商业 Spark 补回来后，容易把“更爽”越权写成稳定突破、无损胜利或额外奖励；
- 局部 Delta 能快一半，但独立重复运行只 **1/5** 章产生完全相同最终正文；跨书后 Reader 仍常喜欢它，Authority 却不稳定；
- 只改调度、不删质量节点的路线最安全，但完整下游后通常只省 5%—12%，且部分章节反而更慢。

因此本轮 production 决策是：

1. **不改变语义节点、模型或 effort。**
2. **不新增常驻 Agent / Judge / Classifier。**
3. **保留两个研究方向，不上线：Paragraph-Delta Reviser 与跨章 speculative scheduling。**
4. **唯一零语义风险的正信号是持久 ACP 进程复用，但绝对收益只有约 1.263 秒/调用；此前作者明确不改 ACP runner，因此只记录，不生产化。**

## 1. Innovation Decision Table

| 路线 | 样本 | 关键路径速度 | Reader 双盲 | Authority 双盲 | 结论 |
|---|---:|---:|---|---|---|
| Parallel Pre-Curator | 5 | **+21.72%** | parallel_precurator 3 / control 2 | parallel_precurator 1 / control 4 | 注意力在 Mission 前冻结，硬边界漂移；拒绝 |
| Authority Blueprint → Primary | 5 | **+40.44%** | authority_blueprint_primary 1 / control 3 / MIXED 1 | authority_blueprint_primary 4 / MIXED 1 | Authority 更强、人物/爽感更薄；拒绝 |
| Parallel Watch + medium Reviser | 5 | **+37.95%** | parallel_watch_medium 1 / control 3 / MIXED 1 | parallel_watch_medium 4 / MIXED 1 | 同样出现“事实赢、故事输”；拒绝 |
| Paragraph-Delta Reviser｜run 1 | 5 | **+51.90%** | paragraph_delta 2 / control 2 / MIXED 1 | paragraph_delta 4 / MIXED 1 | 最有潜力，但单次证据不够 |
| Paragraph-Delta Reviser｜repeat | 5 | **+56.58%** | paragraph_delta 2 / control 2 / MIXED 1 | paragraph_delta 2 / control 2 / MIXED 1 | 修改段落不稳定；不生产化 |
| Paragraph-Delta｜跨书 | 5 | **+47.71%** | paragraph_delta 4 / control 1 | control 2 / MIXED 3 | Reader 可提升，Authority 无稳定胜；继续研究 |
| Commercial Spark + Delta | 3 | **+13.33%** | paragraph_delta 1 / control 1 / MIXED 1 | paragraph_delta 1 / control 1 / MIXED 1 | 会把爽感越权成升级/无损；拒绝 |
| Speculative Next Director｜只看 State+Director | 6 | **+45.36%** | — | — | 子路径很快，但不能只看中间合同 |
| Speculative Director｜完整下游 | 6 | **+12.09%** | speculative_downstream 3 / control 3 | speculative_downstream 1 / control 4 / MIXED 1 | Authority control 4胜；拒绝默认 |
| Speculative Director｜不注入旧 Canon，完整下游 | 6 | **+12.41%** | treatment 3 / control 3 | treatment 2 / control 3 / MIXED 1 | 比旧投机稍稳，但第15章仍丢合作/同步冲击并新增世界事实；拒绝默认 |
| Ten-Chapter Attention Kernel | 5 | **+4.75%** | attention_kernel 2 / control 3 | attention_kernel 1 / control 2 / MIXED 2 | 摊销仅小幅快，仍会漏 Ending/加事实；拒绝 |
| Reviser + State 同调用 | 2 | **-40.76%** | 未继续 | Schema 完整但 wall 膨胀 | 明确速度失败 |
| Persistent ACP 进程复用 | 6 次最小调用 | 相对 **+28.35%**；绝对 1.263s/调用 | 同 Prompt，无语义变化 | 同 Prompt，无语义变化 | Directional PASS；不改 runner |
| Strict delete-only Polish 与 State 并行 | 20章×2 + 跨书10章 | 不增加关键路径；每章约10s并行 | repeat Reader 4/4偏 Polish | 3/4偏 Polish | 触发集合低重复、跨书全 NO_CHANGE；不新增 Agent |
| Full Curator：Luna high → Terra high，完整下游 | 4 | **+26.92%** | Terra 2 / Luna 2 | Terra 2 / Luna 2 | 两边各在不同章节出现硬问题；无稳定赢家，拒绝 |
| Canonless Speculative Director｜完整下游 | 6 | **+12.41%** | speculative 3 / control 3 | speculative 2 / control 3 / MIXED 1 | 去掉当前 Canon 未解决注意力漂移；拒绝 |
| State：Luna low → Terra low | 8 | **-3.32%** | 未继续 | 0/8 四字段 exact | 总体更慢，且状态语义不等价；拒绝 |
| Paragraph Manifest Reviser | 5×2 | v1 有效路线 **-105.93%**；v2 平均 **-5.93%** | 单章 race 无稳定胜 | 单章 race MIXED | v1 5/5 fallback；v2 仅2/5采用且仍有 hard violation；拒绝 |

> 表内“速度”是冻结样本的 ACP wall-clock 关键路径，不是 Direct API SLA，也不能跨执行后端外推。

## 2. 最关键的新发现

### 2.1 真正昂贵的是 Sparse High-Value Semantics，不是平均文字

Curator / Reviser 的高成本并不是因为每个句子都难，而是因为少数稀疏语义必须同时闭合：

- 谁执行动作、作用于哪个对象；
- 钱、器物、身份、力量位置是否真的到账；
- Reader Release 是否完成；
- 未知事实是否仍未知；
- Human 私人欲望是否被净化；
- Public Proof 是否既有冲击又不越权；
- Ending 是已经发生，还是被降成“准备/以后”。

Paragraph-Delta 可以把 Reviser wall 缩短约一半，说明**全文重输不是唯一形态**；但独立重复运行只 1/5 完全一致，又说明这些稀疏语义还没有被确定性编译成足够可靠的 typed obligations。

### 2.2 Authority 与 Commercial Reader 的冲突是真问题，不是 Judge 噪音

几条路线反复出现：

- Authority Blueprint / Parallel Watch：Authority 4/5 偏 Treatment，Reader 只 1/5；
- Paragraph Delta 跨书：Reader 4/5 偏 Treatment，Authority 0胜、2次 control、3次 mixed；
- Spark + Delta：更强的突破/社会震动会提高即时爽感，但也会把一次战局承压越权写成稳定境界。

这证明 TGN 下一步不能继续单独优化“准确”或“好看”。要缩小与顶级男频差距，必须让同一输出同时成立：

`Authority-safe → 人物具体 → Fantasy/Payoff 有重量 → 结果闭合 → Trust Reader`

### 2.3 并行不等于免费：下游会为上游注意力偏差付费

Speculative Director 的 State+Director 子路径快 45.36%，但接回完整 Curator/Primary/Reviser 后只快 12.09%，且第6、13章反而更慢。原因不是下游“救得不够”，而是旧 Canon 让 Director 一开始选择了不同的故事重点；后面高模型只能围绕这个偏差继续工作。

进一步把旧 Canon 完全拿掉、只保留上一章正式正文尾部后，完整关键路径快 12.41%，Reader 3:3，Authority 为 control 3 / treatment 2 / mixed 1。它修复了部分旧 Canon 偏差：第6章 Reader 与 Authority 都选择 Treatment；但第15章仍没有让砺骨部承担水路、没有落实三座新井与粮队同步受冲击，还新增“潮兽随地潮迁徙”的未授权世界事实。**没有旧 Canon ≠ 没有信息损失；上一章尾部也不能替代完成后的动态状态。**

Attention Kernel 同样：四章快约12%–17%，但第3章慢36.7%，五章摊销后只快 4.75%。稳定 Authority 可以预编译，**当前章该注意什么**仍依赖实时 Mission/Canon，不能过早冻结。

### 2.4 换成更快的强模型也不是稳定替代

最后又把完整 Curator 合同从 Luna high 改为 Terra high，并完整接回同一 Terra-high Primary 与 Luna-high Reviser。四章总链平均从 **315.201s 降到 230.356s**，约快 **26.92%**，是本轮最强的“少改架构”信号之一。

但最终正文双盲正好分裂：Reader 是 Terra 2 / Luna 2，Authority 也是 Terra 2 / Luna 2。Terra 在第2、14章更具体或更有商业动作；第10章却把矿队首领换成无名管事、让矿工共同推车，削弱“主角独自稳车”的合同动作，还补出未经授权的分身硬规则；第14章又把“残压已经散尽”写回“仍在散”。Luna 在第19章更稳，但自身也曾把计划要求的矿利与护粮结算推成待发凭单。

因此不能得出“Terra Curator 更差”或“Luna Curator 永远最好”，只能得出：**当前没有可从章类型稳定预测哪一个模型会赢的路由器；2:2 分裂不足以修改 production 默认。**

### 2.5 去掉当前 Canon 的 speculative 版本没有解决根因

为了验证投机失败是否只是“旧 Canon 污染”，又测试了完全不读取当前 State/Canon 的 Next Director，并完整接回 Curator / Primary / Reviser。六章全链平均快 **12.41%**，Reader 3:3，Authority 为 control 3 / speculative 2 / mixed 1。

它既有真实胜例，也有同样明确的失败：第4章新增第二袋个人潮钱；第15章漏掉砺骨部水路确认、三座新井与粮队同步受冲击，并补造“潮兽随地潮迁徙”；第19章又出现势力名漂移与战后结算时点问题。这说明投机 Director 的根因并不只是 Canon 过旧，而是**当前章注意力本身需要最终 State 才能可靠绑定**。

### 2.6 State 换 Terra low 与 Paragraph Manifest 都没有形成快路

State 的 Terra-low A/B 覆盖8章：平均 **27.017s**，原 Luna low 平均 **26.149s**，总体反而慢 **3.32%**；只有2/8章更快，而且四个 State 字段没有一章 exact。它不值得承担新的 Canon 漂移风险。

Paragraph Manifest 试图把 Reviser 变成“逐段动作表 + 本地应用”。第一版 5/5 因 unsafe delete fallback，连同 fallback 后有效速度平均慢 **105.93%**；第二版允许局部 salvage 后只2/5采用，平均仍慢 **5.93%**。唯一明显快的第10章也在盲审中出现人物性别漂移或未授权力量后果，不能上线。

## 3. 详细正文证据

### 例一｜Paragraph Delta：商业读感可以提升，但 Authority 未必更稳

跨书第4章，Reader 更喜欢 Delta，因为契券价值被写得具体：

> “能住进外城驿站，能进商路上的集市，也能让护卫凭契券领到报酬。”

它让“拿到契券”不再只是一个名词，而是住宿、交易、收入和出城路径。与此同时 Authority 更偏向 control，因为 Delta 仍可能多做一次解释或改动正确段落。

这条路线的价值不是可以直接上线，而是证明：**Reviser 应该有能力只改少数段落，且必须保护社会价值与人物反应；但 adoption 需要 deterministic obligation closure，而不是相信单次模型选择。**

### 例二｜Spark 让高光更猛，也最容易越过 Power Authority

第19章 Spark + Delta 写：

> “他的潮炉跨过了原本的关口。”
>
> “顾停舟本人，已经跨进镇海。”

这确实比只写承压更爽，但 Frozen Authority 没有批准稳定突破；同段又把“居民保住”扩大成“居民无伤”。Reader 会感到更强，Authority 必须拒绝。

正确方向不是压掉爽感，而是：

> **把群体震动、懂行者校准、重新定价和复合结算吃满，但不能用未批准升级冒充强度。**

### 例三｜Speculative Director 有真实胜例，却不能全局路由

第4章 Treatment 用“两只钱袋”把钱分成家用和个人路资，让母亲、少东家和顾停舟的欲望都落到具体选择；Reader 与 Authority都选 Treatment。

第6章却出现“侧室”空间未先建立、矿权标记和猎队时序漂移，Reader 与 Authority都选 control。

所以相同调度规则会在相邻章节一胜一负，不能用“普通章/高风险章”这种粗标签自动判断。

去掉旧 Canon 的复验也没有消除这种分裂：第6章两位 Judge 都选 Treatment；第15章两位 Judge 都选 control；第19章 Reader 选 Treatment，但 Authority 选 control，因为 Treatment 漏掉力量档位的公开校准、战功入册与结算落地。它是比旧投机方案更好的研究变体，却仍不是稳定 route。

### 例四｜Attention Kernel 可以省重读，却会擦掉精确 Ending

第2章 Kernel 版本在空间和风险上更清楚，Reader偏好 Treatment；但 Authority发现它漏掉冻结 Ending：

> 阮青蜃接收记录并开始寻找个人实测者。

把稳定 Book/Human/Prose 压成十章 Kernel 没问题；问题是 Kernel 进入当前章后仍需要一个精确、逐条的 Mission/Ending binder。现有版本没有证明这个 binder 足够可靠。

### 例五｜Strict Polish 的价值真实，但不稳定到足以新增常驻层

两次20章复验都只在约10秒内并行完成，且不增加 State 之后的关键路径；第二次4个被改章节里，Reader 4/4选择 Polish、Authority 3/4选择 Polish。

但两次触发集合只有第16、18章重合，跨书10章又全部 `NO_CHANGE`。这说明它能偶尔删掉流程/解释，但并没有稳定识别一个可复述的失败类。把它生产化会增加一个“可能什么也不做”的常驻 Agent，不符合少调用原则。

### 例六｜Terra-high Curator：同一模型在不同章同时出现“更商业”和“越权”

第14章 Terra 路线把阮青蜃的报价写成明确的“八百潮铢”，又让顾停舟逐条追问货损、拦路与回潮楔归属，Reader 认为人物谈判和商业诱惑更强。

但同一版结尾仍写回潮楔“残压还在散”，而 Frozen Mission 要求本章结束前残压已经散尽；Authority 因而选择 Luna。第10章 Terra 版又把应由矿队首领执行的索楔行为换成无名管事，并让矿工共同推车，改变了行动者和“顾停舟独自稳住撤离车”的核心证明。

这说明“Terra 更敢写具体”可以缩小与顶级男频的局部差距，但不能直接变成全局 Curator 默认；它需要的不是模型投票，而是 actor / object / result / power-boundary 的 deterministic binder。

### 例七｜Canonless speculative：少读一份状态，仍会凭空补第二袋钱

第4章 speculative 成稿在人物关系上更好：母亲只拿家用，少东家承认不再挂回商号，砺骨部守路人也有更具体的独立声音。Reader 选择 Treatment。

但它凭空写出“前一笔自己留下的潮钱”，使上一章已经交付的一袋预付款变成第二袋资产。Authority 必须选择 control。删除当前 Canon 没有消除 hallucination，反而拿掉了判定“这笔钱到底是不是新的”所需的最近状态。

## 4. Production Decision

### 保留现状

- 五节点模型与 effort 不变；
- Phase 0 的 stale Long Block / raw GBrain fail-closed / 真实耗时账继续有效；
- 不加入 Blueprint、Pre-Curator、Watch Planner、Spark、Polish、Delta Gate、Speculative Director 或 Combined State；
- 不因高相似度跳过 Reviser；
- 不把一次 Reader 胜出或一次 Authority 胜出当作 production pass。

### 允许继续研究，但尚未冻结

**Paragraph-Delta Reviser** 是唯一值得保留的语义研究方向。下一版不能继续只改 Prompt，应先建立 deterministic `Atomic Chapter Obligations`：

- `actor → action → object`；
- Direct Result / State Change / Ending；
- ownership / transfer / money / time；
- precise power position / Public Proof ruler；
- Reader Release checklist；
- unresolved facts；
- Human-specific cue；
- protected commercial value（欲望、关系、Reward、Surprise）。

Delta 应只在这些 obligations 全部闭合、且修改后全文状态一致时采用；否则直接使用 full Reviser。这个方向需要代码级 typed compiler，不应再增加一个 LLM classifier。

### 零语义风险的基础设施候选

Persistent ACP process reuse 在6个最小调用上从 26.737s 降到 19.157s。它保留 fresh session，只复用 adapter process / initialize；绝对收益约 1.263s/调用。

它值得在未来批量 ACP 工具中采用，但：

- 当前前端不使用这条 runner；
- 本轮作者此前明确排除 ACP runner 修改；
- 还没有在真实长 Prompt 五节点链上测稳定缓存、失败隔离和 transcript extraction。

因此只记为 `DIRECTIONAL PASS / INFRASTRUCTURE ONLY`。

## 5. What This Did Not Solve

- 没有把正常章节从6.17分钟稳定降到4分钟；
- 没有证明任何语义节点可以默认删除或降档；
- 没有修改 ACP runner、前端或 Direct API executor；
- 没有重新生成一整本20章新书验证新平均；
- 自动 Judge仍可能有局部偏差，因此本报告同时保留了正文、重复运行和跨书证据，而不是只看票数；
- current full route 本身也不是无错，只是目前仍是综合风险最低的默认。

## 6. Final Classification

- **Persistent ACP process reuse：DIRECTIONAL PASS / infrastructure only**
- **Paragraph-Delta Reviser：PARTIAL / high-potential research, not production**
- **Strict delete-only Polish：PARTIAL / sparse and unstable, not production**
- **Parallel Pre-Curator：FAIL as production route**
- **Authority Blueprint Primary：FAIL as production route**
- **Parallel Watch + medium Reviser：FAIL as production route**
- **Spark + Delta：FAIL as production route**
- **Speculative Next Director（含 no-old-Canon 复验）：FAIL as default route**
- **Ten-Chapter Attention Kernel：FAIL as current implementation**
- **Combined Reviser + State：FAIL on speed**
- **Full Terra-high Curator：PARTIAL speed signal / FAIL as production default**
- **State Terra low：FAIL on speed and semantic equivalence**
- **Paragraph Manifest Reviser：FAIL on fallback-adjusted speed and closure**

## 7. Evidence Paths

- 机器汇总：`EVIDENCE_INDEX.json`
- 决策表：`DECISION_TABLE.csv`
- Paragraph Delta：`paragraph-delta-reviser*` + `blind-paragraph-delta-reviser*`
- 跨书：`paragraph-delta-reviser-crossbook` + `blind-paragraph-delta-reviser-crossbook`
- Speculative Director：`speculative-next-director-downstream` + `blind-speculative-next-director-downstream`
- Speculative Director no-old-Canon：`speculative-next-director-canonless-downstream` + `blind-speculative-next-director-canonless-downstream`
- Attention Kernel：`ten-chapter-attention-kernel` + `blind-ten-chapter-attention-kernel`
- Transport：`persistent-acp-probe`
- Strict Polish：`strict-reader-polish-*` + `blind-strict-reader-polish-fast20-repeat2`
- Full Terra-high Curator：`full-curator-terra-high-downstream` + `blind-full-curator-terra-high-downstream`
- Canonless Speculative Director：`speculative-next-director-canonless-downstream` + `blind-speculative-next-director-canonless-downstream`
- State Terra low：`state-terra-low`
- Paragraph Manifest：`paragraph-manifest-reviser*` + `blind-paragraph-manifest-race`
- 尾部证据汇总：`TAIL_EVIDENCE_VALIDATION.json`

## 8. Validation

- 全项目回归：`388 passed`。
- `git diff --check`：通过。
- `tgn-system-steward` 已升级到 **0.3.11**，package validate 通过，digest：`sha256:e4306ea15aefec69da466130328bd9e7cf583bda702b81bf90faeb7c43c119eb`，已 install + activate。
- 安装后 bounded read-only smoke 对“Terra-high Curator 快26.92%、双盲2:2、但存在行动者/力量/Ending硬错”的样本判为 `PARTIAL / Experimental Hypothesis`，明确禁止冻结 production 默认。
- 本轮没有修改 production 章节模型路由、ACP runner、前端或 Direct API executor。
