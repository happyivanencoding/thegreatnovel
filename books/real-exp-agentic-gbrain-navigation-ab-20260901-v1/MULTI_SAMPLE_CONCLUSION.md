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

### Root-cause correction after the A/B

后续沿着“为什么六本书会拿同一组三张”继续追查，确认最早根因不是 embedding 本身，也不是必须引入 Agent，而是 **Windows `gbrain.cmd` 的多行位置参数边界**：旧 TGN 把多行 BOOK-aware query 直接作为 positional argument 传入 `.cmd`，实际命令会在换行处被截断，导致不同样本只把相同的第一行送进 GBrain，并可能连后面的 `--scope` 一起丢失。这解释了此前出现的“不同书分数完全一致”“合法结果为空”“非小说 scope 污染”和“fallback 三卡同质化”。

修复后：

1. `query_gbrain()` 在进入 Windows CLI 前把 query 的换行与连续空白压成单行，保证完整 query 与 `--scope` 都到达 GBrain。
2. Story Program `idea` 不再用一个超长 semantic brief 做唯一检索，而是确定性拆成三条短、内容优先的 semantic query：当前 World 的 Living Actors / 机会；Frozen Human 私人欲望 / 机会成本；本轮得到/失去如何继续改变后续选择。
3. 三路结果仍按 round-robin 合并、原有 category / active-inspiration / BOOK 约束过滤，最终最多 3 张；没有新增 Navigator、reranker 或 Story Agent。
4. **GBrain ON 阶段强制要求 embedding Key。** resolver 找不到 `OPENAI_API_KEY` 时立即停止生成并明确报错；不再 keyword-only fallback，也不再用固定通用卡补位。
5. Primary / Batch execution 完全不变。

同一六样本真实回归已不再同质：游戏副本偏 `world-entry`；亚特兰蒂斯加入 `departure-vacancy`；顾野、阮青禾、商砚在同一兽脊 World 下分别得到不同的 `departure-vacancy / reward-afterlife / earned-high-value-acquisition` 组合；坠星海也得到不同第三卡。修复后没有再出现投资、日记、book-dna 等非法 scope 污染。

### Current production conclusion

- Integrated JIT Story Agent：仍 FAIL，不升 production。
- Full Navigator before every Story Program / Refresh：仍 NOT PROMOTED；此前 3:3 质量结果与 +27%～39% wall 结论继续成立。
- **当前 production 采用 deterministic semantic decomposition，而不是 Agentic Navigation。**
- embedding 必须可用；没有 Key 就停止生成。

## What This Did Not Prove

- 这次修复证明的是检索输入与 routing 根因，不等于已经证明新的三路 semantic decomposition 在所有 Story Program 上都比其它可能结构更优；后续仍可用 Sol-high real Horizon 做质量复验。
- 没有证明 embedding 应删除；相反，本轮根因修复后 embedding 才真正表现出 World / Human specificity。
- 没有理由修改 Primary / Batch Writer / Authority Delta；本轮问题仍位于 planning retrieval 层。
