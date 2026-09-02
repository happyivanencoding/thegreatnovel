# GBrain Retrieval Ownership Multi-Sample A/B｜2026-09-02

## Question

在保持 Frozen World / Power / Human、Story 模型与最终窄 inspiration bundle 不变的前提下，比较：

- A｜当前 fixed semantic retrieval → fresh Story Program / Refresh
- B｜Sol Retrieval Navigator 多跳 search/read → 最多 3 张 source-blind inspiration → fresh Story
- C｜代表样本额外加入 deterministic keyword-batch fallback → fresh Story

Integrated JIT（Story Agent 边搜边写）单独测试后出现 >15 分钟无 final，作为运行失败证据，不进入下述质量计票。

## Sample Set

有效质量样本共 7 组：

1. 宁烬《我身藏诸界》21–30｜真实 Horizon Story Refresh｜Sol-high A/B
2. 游戏副本首 Horizon｜Terra-high A/B
3. 亚特兰蒂斯海洋探索｜Terra-high A/B
4. 兽脊世界 Human 1 顾野｜Terra-high A/B
5. 兽脊世界 Human 2 阮青禾｜Terra-high A/B
6. 兽脊世界 Human 3 商砚｜Terra-high A/B
7. 坠星海 Human 1 林泊舟｜Terra-high A/B

另有闻野舟开书样本因 Story 生成 >15 分钟无 final，质量对比 INVALID；其 retrieval 层证据保留。

## Retrieval-Layer Findings

### 1. 当前 semantic one-shot 是真实缺陷

在 6 个新增 `idea` 样本上，启用有效 OpenAI embedding 后，完整 BOOK-aware 长 semantic brief：

- 6/6 `accepted = 0`

不是 embedding 不工作，而是长 query 把近邻拉到不相关区域，经过 category / active-inspiration / BOOK 边界过滤后没有合法 inspiration。

### 2. 旧 keyword fallback 能救空结果，但严重同质化

强制 keyword-only 后：

- 6/6 都获得 3 张卡
- 6/6 都是同一组：
  - `thread-ecology-v3`
  - `earned-high-value-acquisition-v3`
  - `plot-engine-variation-v3`

因此 deterministic fallback 有稳健性价值，但没有足够 World / Human specificity。

### 3. Navigator 确实产生真实 multi-hop 与人格化检索

Navigator 不是同义改写。它会根据上一跳新概念继续搜索，并在同一 Frozen World 的三个 Human 上选出不同 bundle：

- 顾野：`departure-vacancy + thread-collision + earned acquisition`
- 阮青禾：`departure-vacancy + relationship-history-inheritance + story-state-compounding`
- 商砚：`private-appetite-continuity + longitudinal-thread-afterlife + earned acquisition`

这证明“模型拥有 next-query ownership”能扩大 GBrain 的实际可探索空间，并且 retrieval 层没有把不同 Human 压成同一路线。

## Story-Level Results

### 宁烬 Sol-high

Fixed retrieval 胜。Navigator 找到的卡不同且有价值，但 fresh Story 的真实选择代价变软，并出现更冒进的外部反应安排；总 wall 也显著增加。

### 六个新增 Terra-high corrected blind judge

| Case | Winner | 关键结论 |
|---|---|---|
| 游戏副本 | B | B 的人物/奖励生态更强，但 A/B 都有 Authority/continuity 硬缝；B 还存在 12 日内 0→3 过度升阶与腕灯储焰铰链缺失风险 |
| 亚特兰蒂斯 | A | B 为落实 craft 提前具体化 `重潮裂湾` 作为藏海来源，越过当前已批准海相；A 的探索与当前 World 更稳 |
| 兽脊 h1 顾野 | A | B 的“通行契票被自己的选择毁掉”很强，但出现白脊幼兽连续性冲突；A 整体闭合更稳 |
| 兽脊 h2 阮青禾 | B | B 用合法 backfill 与母亲线制造真实稀有血材机会成本，Human-specificity 强；但血阶10正面承小型迁兽超出 Frozen 尺度 |
| 兽脊 h3 商砚 | B | B 明显保住稀罕物占有欲并避免 A 的 1→30 过度成长；但仍有幼兽连续性和苏湄试锋未结算 |
| 坠星海 | A | A 的审美/作品/船/家人选择更分化；B 扩界过早、反制边界含混、关键资产部分幕后化 |

最终：新增 Terra corrected blind vote = **A 3 : B 3**。

加上宁烬 Sol-high：**fixed A 再胜 1 组**。

因此不存在“Full Navigator 普遍提高 Story Program”的证据。

## Character Authority Invariance

通过 retrieval 层，且部分通过 story 层：

- 顾野最强 B 想法是“先取得离开路线，再因自己的收藏/活物选择让路线失效”。
- 阮青禾最强 B 想法是“最想赢、最想拿漂亮材料时，因为母亲的具体生活后果放弃当场稀有血材”。
- 商砚最强 B 想法是“多次明确选稀罕物而非关系最优；只有当父亲与旧货车真正替自己吃风险时才放掉利润”。

三人没有被统一成成长最优、关系最优或道德最优路线。这说明 query ownership 对 Human-specific discovery 有真实价值。

但 Navigator bundle 进入 Story 后仍会诱发另一种稳定风险：Planner 想把 `compounding / acquisition / afterlife` 全部在当前 Horizon 落地，导致等级、资产、关系和世界对象过度展开，甚至越过 Frozen World。

## Third Control｜Deterministic Keyword Fallback

代表样本 C 使用相同固定三件套，无 Agent Navigator：

- 游戏副本：303.2s；直接阅读很强，核心成长比 B 克制，可覆盖 B 的不少优点。
- 亚特兰蒂斯：347.2s；能生成完整长线，但潮阶 1→7，明显过度消耗力量尺。
- 兽脊 h1：300.6s；直接阅读很强，血阶 4→6、通行名额、母亲摊位、骨器和商路线形成较好的平衡。

说明 generic fallback 不是低质量方案，但也不是稳定最优：它对某些题材足够，对另一些题材会把通用 Story Craft 过度前景化。

## Wall-Clock

六个 Terra A/B：

- A Story 平均：307.3s
- B Story 本体平均：287.5s
- Navigator 平均：139.5s
- B 总链平均：427.0s

因此 full Navigator 默认链相对 A 平均约 **+39% wall**。

三个 C 代表样本：

- keyword C 平均：317.0s
- 对应 Navigator B 总链平均：403.7s

Navigator 相对 deterministic keyword C 约 **+27% wall**。

## Verdict

### Reject as production default

- Integrated JIT Story Agent：FAIL（运行形状过重，出现 >15 分钟无 final）。
- Full Navigator before every Story Program / Refresh：PARTIAL PASS / NOT PROMOTED。检索能力真实提升，但 Story 净质量 3:3、Authority closure 不稳定、wall 更高。

### Real production problem found

当前“有 semantic key 时只使用一个超长 BOOK-aware semantic query”的 `idea` 检索形状有真实 cross-sample 缺陷：本轮 6/6 新样本合法结果为空。

### Best next candidate

不是删除 embedding，也不是让 Story Agent 自由逛库，而是：

`deterministic authority boundary + lightweight query decomposition / recovery + narrow final bundle + fresh Story`

建议下一轮只测试一个更小变量：

1. 仍由代码拥有 category / active / BOOK / protagonist-blind / source-blind 边界。
2. 不用完整 Navigator，不让 Agent 写 Story。
3. 把一个超长 semantic brief 拆成 2–3 个短 query：
   - 当前 Plot/World 缺口
   - Human-specific 私人牵引/机会成本
   - Book-level consequence / reward action-space（仅需要时）
4. query 可以由一次很短的 planner 生成，也可先尝试确定性抽取；每条仍走现有 semantic retrieval。
5. round-robin merge → deterministic filter → 最终最多 3 张。
6. 如果 semantic 分解仍为空，才 fallback 到现有 keyword batches。
7. fresh Story 只看到最终窄 bundle；Primary / Batch execution 完全不变。

这能保留 Navigator 已证明的“会提出新问题 / Human-specific”价值，同时避免 full multi-hop 的 +27%～39% wall 和更大的 Authority 联想空间。

## What This Did Not Prove

- 没有证明轻量 query decomposition 一定优于当前 keyword fallback；它还需要独立 A/B。
- Terra-high 大样本只用于 screening，不替代 Sol-high production route；若轻量结构在 Terra screening 稳定胜，仍需 Sol-high Story Program + real Horizon Refresh 复验。
- 没有证明 embedding 应删除；相反，Navigator 的自然语言多跳命中恰好依赖 semantic retrieval。
- 没有理由修改 Primary / Batch Writer / Authority Delta；本轮问题完全位于 planning retrieval ownership。
