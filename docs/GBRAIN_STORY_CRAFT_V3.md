# GBrain Story Craft v3 与 TGN 接入

## 目标

GBrain 是 TGN 的可选创作灵感库，不是价值观裁判或硬门禁。生产知识优先保存原作如何制造：读者欲望、世界进入感、长篇玩法变异、长中短线编织、高价值获得、人物回流与关键场景兑现。

蒸馏正文以中文为主。当前 GBrain 在没有 query embedding API Key 时会退化为 English FTS keyword-only，因此英文 alias 不属于创作知识正文。当前 Pilot 将它们集中记录在 `routing/retrieval-aliases-v3.yaml`，并在可搜索页面标题区保留低层 `Retrieval aliases` 行；TGN 只抽取 `##` 下的中文 Creative Problem / Mechanism / Guidance 等区块，因此 alias 不进入模型的 Inspiration Bundle，也不显示成作者默认查询。

## 四个知识支柱

1. **World Fantasy**：为什么读者想进入、获得、成为、知道；世界扩大后新增什么欲望。
2. **Story Program**：同一核心幻想如何跨几十/几百章换 Plot Engine；长中短线怎样沉睡、提醒、碰撞；配角怎样带着自主目标离屏并回流。
3. **Reward / Opportunity**：主角怎样持续得到真正值得想要的力量、宝物、知识、身份、资格、伙伴或世界入口；获得怎样立即证明价值、扩大行动空间并在后文复用或重解释。
4. **Scene Skills**：身份揭露、核心人物离开、牺牲、多年后重聚等关键事件怎样落成读者可感知的场景。

## TGN 阶段消费

- `Fantasy Seed`：继续保持隔离，不自动读取 GBrain，先保证核心幻想来自当前作者方向与模型本身。
- `World Vision`：默认 GBrain ON，最多 3 条 focused inspiration；借鉴 world fantasy / world entry / narrative compounding，不能覆盖已批准 Fantasy Seed。
- `Story Program`（UI mode=`idea`）：默认 GBrain ON，最多 3 条 focused inspiration；优先借鉴 Plot Engine 变异、thread ecology、人物回流与 Reward/Opportunity，不能覆盖已批准 Seed / World Vision。
- `Outline`：默认 GBrain ON，通常 4 条、最多 5 条 focused inspiration；把 Thread Collision、身份揭露、离队归来、牺牲/二次兑现、高价值获得与旧奖励重释落实为具体故事锚点。
- `Director`：不负责凭空发明长期大奖励或重新设计 Story Program。
- `Curator / Primary`：Scene Skills 只控制 HOW TO REALIZE THE SCENE，不改变 Chapter Mission 或 Canon。
- `State Extraction`：继续用当前 `current_state` 记录重要能力、物品、规则、持有人与状态变化；不新增 Inventory 数据库。

## 统一的 Supporting Logic 原则

TGN 不为治理化、工程化、蓝领职业化和过度验证分别增加 Reviewer。它们共用一条上游原则：世界中的合理解释、风险、技术机制和组织逻辑可以存在，但 supporting logic 不自动升级为 story engine。

- 对手或势力的理由可以真实成立，但不自动成为作者结论或主角长期职责；主角的职责从核心欲望、具体关系和人物选择中生长。
- 能力可信性优先嵌入有真实目标和利害关系的行动中证明，不单独搭建测试场景来穷举机制。
- 观察、分析、测试、验证、调整、实施只有在其中仍有关键选择、冲突或反转时展开；其余压缩到足以支撑因果。
- 可重复能力优先扩大主角的主动权、敌人策略、人物关系、身份、机缘和世界入口，不因可重复使用就自然职业化。

该原则直接复用现有 World Vision → Story Program → Outline → Director 的共享 Prompt 规则，不新增 Agent、Hard Gate、评分器或 LLM 调用。

## Reward 职责

高价值获得不是随机掉宝器，也不是固定章数节拍器。

Story Program 负责：在不同阶段选择当前最适合的“获得体验”，例如能力、宝物、知识、身份、师承、资格、伙伴、生命变化或世界入口。它们没有固定先后顺序，可以提前、后置、跳过或再次出现。

Outline 负责：具体机会怎样出现，主角为什么想要，谁阻止，主角怎样真正拿到，第一次怎样证明它值钱，以及哪一个旧奖励将在后文被复用或重新解释。

Director/Writer 不应为了“这一章需要爽点”自行添加计划外的长期大奖励。

## Model Routing：规划生成与 GBrain 蒸馏

### 规划生成模型

| 阶段 | 当前默认 | 为什么 |
|---|---|---|
| Fantasy Seed | GPT-5.6 Luna high | 幻想抽象强、速度合理；此阶段 GBrain OFF，避免参考库过早锚定核心创意 |
| World Vision | GPT-5.6 Luna high | 擅长把核心幻想转成世界欲望、力量体验与进入更大世界的理由 |
| Story Program | GPT-5.6 Sol high | 当前 Sol 最值得发挥的位置：长期玩法变异、人物自主性、敌人策略、关系回流、Thread Ecology、Reward 变化 |
| Outline | GPT-5.6 Luna high | 能高质量执行正确 Program，把长期结构落实成故事锚点而不过度膨胀 |
| Director | GPT-5.6 Luna high | Balanced 默认；质量与 Terra high 接近但成本更低，最低延迟模式可切 Terra high |
| Curator | GPT-5.6 Luna high | Balanced 默认；继续压短输出合同。若优先最短延迟与更克制输出，可切 Terra medium |
| Primary Writer | GPT-5.6 Terra high | 正文 A/B 中更克制、较少 procedural expansion、更愿意按 Chapter Contract 停下；这是质量/行为选择，不是成本选择 |
| State Extraction | GPT-5.6 Luna low | 当前成本优先默认，只记录已发生事实 |

模型不是线性排名：

- **Terra**：章节实测 wall-clock 通常最快、输出更克制，但单价显著高于 Luna；Primary 的优势是正文行为，不是便宜。
- **Luna**：当前单价最低，也是规划与章节理解层的默认主力；Director/Curator 性价比高，但输出更容易偏长。
- **Sol high**：长期故事结构最强，同时单价最高且通常最慢；默认只集中在 Story Program / Deep Planning。
- **Luna max**：仅用于疑难创意救援、最高质量基线和关键重构，不日常使用；
- **GPT-5.4 high**：当前没有相对 Luna 的补偿性优势，不作为默认创作模型。

章节路由要分开看 **质量 / wall-clock / 实际成本**。当前 Balanced 推荐为 `Luna Director → Luna Curator → Terra Primary → Luna State`；若优先最低延迟，可把 Director/Curator 切到 Terra high/medium；若优先 Curator 的极简输出，可只把 Curator 切到 Terra medium。Sol 不进入常规章节链。

### GBrain 蒸馏模型

- **Terra high**：原文事实、Scene Evidence、Reward Event Evidence、Source Fidelity。重点是“原作实际上发生了什么”。
- **Luna high**：Book DNA、World Fantasy、人物/关系解释、Reward/Opportunity synthesis、Scene Skill synthesis。重点是“为什么让人想要、为什么好看”。
- **Sol high**：Longitudinal Threads、Thread Braid、Story Program patterns、跨书高级 synthesis。重点是“几十/几百章以后为什么仍然有效”。

简化理解：**Terra 看清事实 → Luna 理解吸引力 → Sol 理解长篇结构。**

### Fast / Default / Deep 模式

- Fast：需要大量试书、Seed A/B 时可用 Terra high；
- Default：Luna high 为主要规划模型，Story Program 单独使用 Sol high；
- Deep / Repair：当长期主线机械重复、同一能力不停换皮、配角缺少自主性或作者明确要求“想深一层”时，优先只升级/重跑 Story Program，而不是整链切到 Sol；
- Max：Luna max 只用于少量高风险重构或最高质量基线。

## GBrain OFF / ON 规划 A/B 结论

2026-08-23 使用同一个已批准 Fantasy Seed“看见别人看不见的路”，冻结模型和 Prompt，完整比较：

`World Vision(Luna high) → Story Program(Sol high) → Outline(Luna high)`

两组唯一主要变量是 GBrain OFF / v3 ON。结果：

- OFF 已能产出合格且明显避免工程蓝领化的规划；
- ON 的主要提升发生在 **Story Program 与 Outline**：同一个“隐路”更早从空间封锁换挡到目标、人物、身份/资格和世界归属问题；
- ON 更稳定地产生 Thread Ecology、人物自主目标、高价值获得→立即证明→后续反哺，以及旧奖励在新语境重释；
- ON 能把完整中期故事单位连续规划到约 60—70 章，而 OFF 更容易在约 30 章后留下下一轮再规划；
- 两组输出长度接近，并行测试中没有观察到 GBrain ON 带来明显 wall-clock 负担。

因此当前默认保持：**Seed OFF；World 3 条 ON；Program 3 条 ON；Outline 4/5 条 ON。** GBrain 的作用不是替模型提供故事答案，而是给已经很强的模型提供少量长期小说 craft reminders。

这只是一个高风险 Seed 的实测；后续经典样本扩展也继续保持 PILOT overlay，不因样本数量增加就自动提升为正式 machine VALIDATED。继续通过真实新书验证后再 promotion。
## 经典样本扩展（2026-08-24）

在首轮《斗罗大陆》《诡秘之主》《将夜》《修真聊天群》之后，v3 又完成 10 本互补经典的 SOURCE-FIRST 专项蒸馏：

- 《遮天》：World Desire、世界奇观、古史回流；
- 《仙逆》：情绪长线、旧因回流、Payoff Afterlife；
- 《极道天魔》：Power Dominance、Obstacle Reframing、Plot Engine 换挡；
- 《斗破苍穹》：Reward、Private Acquisition / Public Proof；
- 《盘龙》：Stage Transition、World Scale、家庭/关系 carryover；
- 《凡人修仙传》：稳态成长、机缘、Map Transition，同时保留资源循环重复风险；
- 《灭运图录》：境界升格如何改变故事问题；
- 《大圣传》：强烈主角欲望、不驯化力量幻想、Power ≠ Duty；
- 《幽冥仙途》：多方人物博弈、信息差、临时合作；
- 《死人经》：联盟、背叛、人物自主与主角计划被他人改写。

来源使用稳定 `source_book_id` 区间 `rcv0-30`—`rcv0-40`；新增三本原文已规范到 `02_仙侠/大圣传.txt`、`02_仙侠/幽冥仙途.txt`、`07_武侠/死人经.txt`。增量来源登记见 `reference-corpus/selection/corpus-sources-v3.classics.yaml`。

跨书综合最初提出 4 张新机制候选。Terra Final Source Fidelity Audit 后，只保留一张真正独立的新 active mechanism：

- `minimum-sufficient-public-proof-v3`：**最低充分公开证明**。Private Acquisition 解决“主角是否真的获得”，Public Proof 解决“外界是否还能继续按旧判断行动”；公开证明只展示到足以改变敌人策略、关系位置、身份或新机会。

另外三项没有继续扩张 ontology，而是 MERGE：

- Old Anchor Progressive Recontextualization → `narrative-compounding-v3`；
- Payoff Afterlife → `reward-afterlife-v3` / story-state 语义；
- Realm Change → Story Problem Change → `plot-engine-variation-v3`。

同时用经典样本增强 `world-desire-ladder`、`world-entry`、`character-autonomy`、`map-transition`、`thread-ecology` 等已有机制。原则是：**新书优先增加证据，不按“每本书一个新方法论”增加卡片。**

扩展后 staging 为 **47 张 Pilot：45 active / 2 HOLD**。相比扩展前 29 张，净新增 18 张主要是 source-specific Book/Arc/Observation evidence；默认规划链的 focused mechanism 数量没有同步膨胀。`observations` 只作来源证据，当前 TGN `SOURCE_CATEGORIES` 不消费它们。

GBrain runtime 从 `3716 pages / 15649 chunks` 增至 `3734 pages / 15686 chunks`。导入后同 Seed 回归确认默认检索完全不变：

- World Vision：`story-state-compounding / world-entry / world-desire-ladder`；
- Story Program：`plot-engine-variation / thread-ecology / earned-high-value-acquisition`；
- Outline：`thread-collision / sacrifice-convergence / hidden-identity-long / reward-recontextualization`。

所有 active staging card 的 canonical evidence refs 已统一到稳定 `source_id / distill_id / segment_id`；最终检查为 **33 refs / 0 evidence error / 0 temporary ref / 0 Prompt-risk hit**。完整报告见 GBrain 工作区 `FINAL_CLASSIC_EXPANSION_REPORT_20260824.md`。

## 检索退化兼容

当前 GBrain 的 hybrid query 只有在进程可用 `OPENAI_API_KEY` 时才生成 query embedding；没有 key 时会退化成 keyword-only。TGN 因此：

1. 始终生成并展示中文 BOOK-aware Retrieval Brief；
2. 如果 semantic query 可用，后端直接使用完整 brief；
3. 如果不可用，规划节点后端内部使用少量英文 OR aliases；
4. 用户手工编辑查询时，手工 query 永远优先；
5. 返回给 LLM 的 `可用抽象` 仍来自卡片中文 Mechanism/Guidance 等正文，不把英文 aliases 注入 Prompt。

这是一层确定性 fallback，不新增 LLM、reranker、Agent 或 Hard Gate。

## Prose Craft v1

Story Craft 负责“长期故事为什么好看”；正文表达层另有 `docs/GBRAIN_PROSE_CRAFT_V1.md`。Prose Craft v1 使用六本经典的 85 个 bounded scene windows 建立 source-specific Prose DNA，再跨书收敛为 7 张 production-facing Prose Controls。Prose DNA 不直接进入 Primary Writer；Prose Controls 只影响 HOW TO SAY，不覆盖 BOOK Prose Profile、Chapter Mission 或 Canon。当前完成 GBrain import + embedding（15705/15705），自动 Curator 路由仍待正文 A/B 后冻结。
## Pilot Active / HOLD

当前主 `gbrain-story-craft-v3/staging` 已确定性重建 manifest，共 **71 张 staging pages：67 active / 4 HOLD-or-reference-only**。其中真正的 HOLD mechanisms 仍是：

- `partner-reward-agency-v3`
- `reward-timing-variation-v3`

另外 2 张 Batch D cross-book synthesis 显式 `active_inspiration: false`，只保留为 provenance / research reference。新 Batch D Book/Arc 与两个新 mechanism 保持 PILOT overlay；`reference-corpus/machine` 继续保持旧 validated snapshot。TGN 对显式 `active_inspiration: false` 的页面自动跳过。

## Priority Batch D 扩展（2026-08-24）

在经典样本扩展后，继续 SOURCE-FIRST 蒸馏 10 本互补长篇：《牧神记》《大奉打更人》《全球高武》《不科学御兽》《沧元图》《乱世书》《超神机械师》《明克街13号》《大王饶命》《莽荒纪》。每本由 Luna high 负责 Book DNA / World Fantasy，Sol high 负责 Longitudinal Threads / Story Program；共新增 20 张 source-specific Book/Arc Pilot。

Terra Source Fidelity Audit 初审为 6 PASS / 4 PASS_WITH_EDITS / 0 FAIL；修正 locator 覆盖与 TGN Transfer 表层专名后定向 recheck **PASS**。

跨书 World synthesis 未扩张 ontology：Reader-Facing World Coordinates、Core Advantage ↔ World Compatibility、Promotion Afterlife、Concrete Value / World Desire 均 MERGE 现有机制。跨书 Program synthesis 只保留两个真正独立的新 PILOT mechanism：

- `opponent-learning-success-condition-rewrite-v3`：敌人根据已暴露事实学习，并改写主角核心优势的成功条件；
- `longitudinal-thread-dormancy-collision-afterlife-v3`：长线沉睡、行动性提醒、异质线程碰撞，以及第一次 payoff 后的 second payoff / afterlife。

其它候选继续 MERGE：首个高光后的选择空间化 → action-space / old-ability-new-use；阶段发动机换问法并续燃旧状态 → map-transition / plot-engine-variation；首五章“证明—选择—条件变化”只作 Outline 可选语法，不成为五步 Hard Gate。

本轮与 Prose Priority Batch 合并向 GBrain scoped import 32 页，runtime 从 `3753 / 15717 / 15717` 增至 **`3785 Pages / 15780 Chunks / 15780 Embedded`**；`embed --stale` 实际刷新 63 chunks，最终 embedding debt 为 0，无 root-level duplicate。

TGN retrieval regression 通过：SP01 仍以 `plot-engine-variation` 为首，SP02 仍由 `thread-collision / sacrifice-convergence` 主导，SP03 仍是 `reunion / departure / character-autonomy`，OL01 `thread-ecology` 第1，WV01 `world-desire-ladder / world-entry` 第1/2；只有明确询问“敌人怎样学习并反制”时，新 `opponent-learning` 升到第1。reference-only syntheses 被 `active_inspiration: false` 正确过滤。

完整本地报告：`reference-corpus/operations/gbrain-story-craft-v3/expansion-batch-d-20260824/FINAL_BATCH_D_REPORT_20260824.md`。
