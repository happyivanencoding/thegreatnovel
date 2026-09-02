# GBrain Story Craft v3 与 TGN 接入

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义 GBrain Story Craft 的知识、检索、蒸馏与接入边界。

## 目标

GBrain 是 TGN 的可选创作灵感库，不是价值观裁判或硬门禁。生产知识优先保存原作如何制造：读者欲望、世界进入感、长篇玩法变异、长中短线编织、高价值获得、人物回流与关键场景兑现。公共治理、资源分配、维护职责和责任升级只保留为 source-specific 研究证据，不进入 production active inspiration。

蒸馏正文以中文为主。当前 GBrain 在没有 query embedding API Key 时会退化为 English FTS keyword-only，因此英文 alias 不属于创作知识正文。当前 Pilot 将它们集中记录在 `routing/retrieval-aliases-v3.yaml`，并在可搜索页面标题区保留低层 `Retrieval aliases` 行；TGN 只抽取 `##` 下的中文 Creative Problem / Mechanism / Guidance 等区块，因此 alias 不进入模型的 Inspiration Bundle，也不显示成作者默认查询。

## 四个知识支柱

1. **World Fantasy**：为什么读者想进入、获得、成为、知道；世界扩大后新增什么欲望。
2. **Story Program**：同一核心幻想如何跨几十/几百章换 Plot Engine；长中短线怎样沉睡、提醒、碰撞；配角怎样带着自主目标离屏并回流。
3. **Reward / Opportunity**：主角怎样持续得到真正值得想要的力量、宝物、知识、身份、资格、伙伴或世界入口；获得怎样立即证明价值、扩大行动空间并在后文复用或重解释。
4. **Scene Skills**：身份揭露、核心人物离开、牺牲、多年后重聚等关键事件怎样落成读者可感知的场景。

## TGN 阶段消费

- `World Vision`：protagonist-blind，默认 GBrain ON，固定读取 1 条 Reader Coordinates Reference，再选最多 3 条 focused creative inspiration；固定坐标参考不占 creative 名额。它只帮助世界自身的 desire、entry、奇观、正常力量坐标与独立事件成立，不读取未来 Power/Human。
- `Power Seed`：默认 GBrain ON，固定读取 1 条 source-blind `Naming Craft Reference`，再读取小型 Power lane bundle；固定命名参考不占 creative inspiration 名额。它只看 `POWER_BASELINE`，借鉴力量幻想、成长兼容、长期玩法与 reader-facing 命名 craft，不读取 Human Biography 或 named Story Opportunities。命名参考来自 69 个已登记 source-first 小说来源的确定性候选抽取 → 10 批 Terra Fidelity → Sol 跨书 synthesis → Luna audit，只迁移规律，不迁移原著专名。
- `Human Seed`：默认 GBrain ON，最多 3 条 Human craft，Appetite / Behavior / Relationship 各最多 1 条；只看 `LIFE_CONTEXT`，不读取 Power 或 named Story Opportunities。
- `Story Program`（UI mode=`idea`）：默认 GBrain ON，最多 3 条 focused inspiration；优先借鉴 Plot Engine 变异、thread ecology、人物回流、Reward/Opportunity 与历史复用，但不能覆盖已批准 World / Character。GBrain 可以提醒“什么值得想要、旧获得怎样继续生效”，不能重新把这些原则变成每阶段 Acquisition / Compounding 表单。
- `Outline`：默认 GBrain ON，通常 4 条、最多 5 条 focused inspiration；把 Thread Collision、身份揭露、离队归来、牺牲/二次兑现、高价值获得与旧奖励重释落实为具体故事锚点。World 的固定 Coordinate Reference 同样不重复进入 Outline creative 候选，坐标语义由已批准 World Vision 继承。
- `Director`：仅单章 fallback / 专项实验使用；不负责凭空发明长期大奖励或重新设计 Story Program。
- `Scene Skill v2`：GBrain/原著只在离线研究层提供 source-first bounded evidence；跨书收敛成 source-blind Deep Craft。2026-08-28 冻结研究覆盖 64 条定向 lane、26 本经典长篇、857 次 bounded-window Fidelity 审核；这些数字只是研究证据，不构成 Runtime 配额。当前默认 Batch 不调用 Curator / Scene Skill Router；24 个 Primary + 3 个 Shared Reference Lens 继续服务单章 fallback、专项修订与离线 craft 维护。fallback 中 Curator 仍只看 `Reading Question + 一行 Projection Guidance` 并编译 2—4 句 `Scene Prose Projection`（允许 `NONE`），Primary 不直接读取完整 Skill 或原著 evidence。
- `Authority Reviser`：默认 Batch 使用 Sol-high exact Delta，raw GBrain 固定 OFF；Scene Craft Revision Watch 当前只保留在单章 fallback / 专项修订，完整 Revision Lens 不进入。
- `State Extraction`：继续用当前 `current_state` 记录重要能力、物品、规则、持有人与状态变化；不新增 Inventory 数据库。

## 统一的 Supporting Logic 原则

TGN 不为治理化、工程化、蓝领职业化和过度验证分别增加 Reviewer。它们共用一条上游原则：世界中的合理解释、风险、技术机制和组织逻辑可以存在，但 supporting logic 不自动升级为 story engine。

- 对手或势力的理由可以真实成立，但不自动成为作者结论或主角长期职责；主角的职责从核心欲望、具体关系和人物选择中生长。
- 能力可信性优先嵌入有真实目标和利害关系的行动中证明，不单独搭建测试场景来穷举机制。
- 观察、分析、测试、验证、调整、实施只有在其中仍有关键选择、冲突或反转时展开；其余压缩到足以支撑因果。
- 可重复能力优先扩大主角的主动权、敌人策略、人物关系、身份、机缘和世界入口，不因可重复使用就自然职业化。

该原则直接复用现有 World Vision → Power/Human → Character → Story Program → Outline → Director 的职责边界，不新增 Agent、Hard Gate、评分器或 LLM 调用。

## Asymmetry Reveal / Social Repricing Pilot（2026-08-28）

为解决“Power/World 明明定义主角极特殊，但现场人物像理所当然、读者感不到力量尺与社会涟漪”的问题，完成 6 本经典长篇、16 个 bounded canonical windows 的 SOURCE-FIRST 定向蒸馏，覆盖 private / selective / public / accidental / secondhand disclosure，以及普通人、专家、rival、利益方、敌对者、亲近者的差异反应。Terra high 负责原著事实/Fidelity，Luna high 综合 Scene Craft，Sol high 综合 Story/Ripple。

跨书结果只形成两张最小 PILOT 资产，不扩 taxonomy：

- `mech-disclosure-repricing-ripple-v1`：Story Craft。限定谁实际取得什么证据，让不同观察者按自己的正常尺形成不同价格；只有后续独立行动继续受该新估值影响时才升级为 Ripple。它是 Supporting Logic，不是 Story Engine，不新增 Disclosure Ledger。
- `prose-control-observer-specific-repricing-v1`：Scene Craft，`active_inspiration:false`。高价值 reveal 采用**双通道校准**：`Behavioral Repricing` 让一个关键观察者真的换动作；`Ruler Calibration` 由最有资格者短促说明“正常同层/同类能做到什么 → 主角这次超出哪里 → 为什么罕见/异常或值得重新判断”。首次显露、新层级/质变、新复合、新高圈层重新观察、旧社会估值过时等节点应重新校准，不把它当 opening 一次性说明。

顾临川 Ch1/Ch2 Scene-level 与 Story Program production-shaped ON/OFF 为 **DIRECTIONAL PASS**：ON 更稳定地产生角色专属反应、专业尺、报价/挑战规格变化、部分知识与基于已知事实的 Counterplay，同时没有把每次显露都扩成追杀/招揽税。当前结论是**值得继续 production A/B**，但不直接新增独立 `Asymmetry Reveal` Primary Scene Skill；更优候选是接入现有 `showcase_evaluation` / public-proof 类 Scene Craft 的 conditional short Projection，并在 Story Program / Outline 负责长期 Disclosure/Ripple 因果。

两张卡已 scoped import 到 GBrain。当前 keyword retrieval 回归中，`observer knowledge / social repricing / counterplay` 等查询可稳定 Top-1 命中新卡；当前 runtime 为 **3829 Pages / 15858 Chunks / 15858 Embedded**，embedding debt 已清零。研究资产因此完成 import + embedding + retrieval 门禁，但仍只处于 **PILOT / production-A/B ready**，不等于已经进入默认 production bundle。

## Reward 职责

高价值获得不是随机掉宝器，也不是固定章数节拍器。

Story Program 负责：当人物/世界因果自然产生高价值对象时，决定它怎样成为真实故事机会；不要求每个大型阶段都出现新获得。High-Value Acquisition 是 reader-appetite principle，不是阶段税。

Outline 负责：具体机会怎样出现，主角为什么想要，谁阻止，主角怎样真正拿到，第一次怎样证明它值钱，以及哪一个旧奖励将在后文被复用或重新解释。获得一旦发生，后续必须真实改变行动、选择或敌人应对；这就是有效 Compounding，不需要每阶段填写 `Compounding Growth`。

Director/Writer 不应为了“这一章需要爽点”自行添加计划外的长期大奖励。

## Model Routing：规划生成与 GBrain 蒸馏

### 规划生成模型

| 阶段 | 当前默认 | 为什么 |
|---|---|---|
| World Vision | GPT-5.6 Luna high | protagonist-blind 建世界：普通生活、正常力量、价值物、独立事件与奇观 |
| Power Seed | GPT-5.6 Luna high | 以 World Normal 为比较尺生成清楚、可成长、默认偏强的开局 Core Asymmetry；不强制世界内合法例外 |
| Human Seed | GPT-5.6 Luna high | world-conditioned / power-blind 生成人本身；保留 competing motives 与具体关系变量 |
| Story Program | GPT-5.6 Sol high | 负责长期优势栈：开局优势成长、新 Power Asymmetry 获得与复合，同时处理玩法变异、人物自主、敌人策略和关系回流 |
| Outline | GPT-5.6 Luna high | 能高质量执行正确 Program，把长期结构落实成故事锚点而不过度膨胀 |
| Director | GPT-5.6 Luna high | 当前 production；Terra/条件模块路由只作显式 A/B，尚未证明最终故事质量等价 |
| Curator | GPT-5.6 Luna high | Scene Skill v2 compact Catalog → short Projection；允许 `NONE`；medium/Terra/Slim 路由均未证明最终正文质量等价 |
| Primary Writer | GPT-5.6 Terra high | 只消费 Curator short Projection，不直接读 Deep Skill；先完成第一版正文 |
| Authority Reviser | GPT-5.6 Luna high | safe Authority Refresh Pack + optional short Revision Watch；raw GBrain OFF；Preservation First |
| State Extraction | GPT-5.6 Luna low | 当前成本优先默认，只记录最终正式正文已发生事实 |

模型不是线性排名：

- **Terra**：章节实测 wall-clock 通常最快、输出更克制，但单价显著高于 Luna；当前用于一次连续 4—6 章的 Batch Primary。
- **Luna**：当前单价最低，也是 World / Outline 等规划层与 State 的默认主力；不再增加 LLM Batch Director 去重写已批准 Future-10。
- **Sol high**：长期故事结构强，同时单价最高且通常最慢；当前除 Story Program / Story Refresh 外，固定承担整批可见的 **Batch Authority Delta**。
- **Max / Ultra**：只作疑难诊断与质量对照；2026-08-31 同稿矩阵没有证明 Ultra 相对 high/max 的补偿性收益，Luna-max 还出现 overrepair。
- **GPT-5.4 high**：当前没有补偿性优势，不作为默认创作模型。

章节路由要分开看 **质量 / wall-clock / 实际成本**。当前默认是 `Approved Future-10 → Full Deterministic Batch Packet → Terra high Batch Primary → Sol high Batch Authority Delta → Luna low State逐章落盘`，默认5章、支持4—6章；Packet 复用 Chapter Context compiler 前置完整安全 Authority 与 BOOK Prose Profile。2026-08-29 的 Curator medium/Terra/Slim、单章 Reviser medium/Patch-only、Conditional Director 失败结论继续约束 fallback；任何进一步模型/effort缩减仍需正常下游 Reader + Authority 双盲。

### GBrain 蒸馏模型

- **Terra high**：原文事实、Scene Evidence、Reward Event Evidence、Source Fidelity。重点是“原作实际上发生了什么”。
- **Luna high**：Book DNA、World Fantasy、人物/关系解释、Reward/Opportunity synthesis、Scene Skill synthesis。重点是“为什么让人想要、为什么好看”。
- **Sol high**：Longitudinal Threads、Thread Braid、Story Program patterns、跨书高级 synthesis。重点是“几十/几百章以后为什么仍然有效”。

简化理解：**Terra 看清事实 → Luna 理解吸引力 → Sol 理解长篇结构。**

### Fast / Default / Deep 模式

- Fast：需要大量试书、上游 A/B 时可临时用 Terra high；
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

因此当前默认保持：**Seed OFF；World 固定 1 Coordinate Reference + 最多 3 creative；Program 最多 3；Outline 通常 4 / 最多 5。** GBrain 的作用不是替模型提供故事答案，而是给已经很强的模型提供少量长期小说 craft reminders。

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

当前 GBrain 的 hybrid query 需要可用 `OPENAI_API_KEY` 才生成 query embedding；没有有效 key 时会退化成 keyword-only。Windows 上 TGN 不再只看启动时继承到的进程环境：统一 resolver 按 `当前进程 → User Environment → Machine Environment` 查找持久 Key，并显式传给 GBrain 子进程，因此 AgentDock / ChatGPT 宿主在 Key 配置前已经启动也不需要靠重启才能恢复 semantic query。Key 本身不写入 repo / `.env`。

TGN 因此：

1. 始终生成并展示中文 BOOK-aware Retrieval Brief；
2. 如果 semantic query 可用，后端直接使用完整 brief；
3. 如果不可用，World Vision / Story Program / Outline 使用 2–3 组互补的内部 retrieval intents，而不是把越来越大的 GBrain 压成一个关键词 query；每组仍只做 bounded recall；
4. 多 intent 结果按 round-robin 合并再去重，防止第一组 query 独占候选窗口；普通 creative 规划阶段最多检查 12 个候选，并保持 World creative 最多 3、Program 最多 3、Outline 最多 5；World 的 Reader Coordinates 由固定 slug 单独读取，不参加 creative 排名；单个可选 intent 查询失败时保留其它结果，只有全部查询失败才向上报告 GBrain 错误；
5. 用户手工编辑查询时，手工 query 永远优先；
6. 返回给 LLM 的 `可用抽象` 仍来自卡片中文 Mechanism/Guidance 等正文，不把英文 aliases 注入 Prompt。

这是一层确定性 fallback，不新增 LLM、reranker、Agent 或 Hard Gate。

原则是 **wide recall, narrow context**：GBrain 变大以后优先提高候选覆盖与意图多样性，不同步扩大最终 Prompt 中的 inspiration 数量。

## Prose Craft v1

Story Craft 负责“长期故事为什么好看”；正文表达层另有 `docs/GBRAIN_PROSE_CRAFT_V1.md`。Scene Craft 的研究链仍是 `原著 bounded evidence → Fidelity Audit → cross-book synthesis → source-blind Deep Craft`；其 `Curator short Projection / Reviser short Watch` 目前只服务单章 fallback / 专项修订，默认 Batch 不调用该 Router。研究层可深，章节 Runtime 必须窄，书名/locator/source-specific DNA 不进入 Writer。Prose Craft v1 使用六本经典的 85 个 bounded scene windows 建立 source-specific Prose DNA，再跨书收敛为 7 张 production-facing Prose Controls；BOOK Prose Profile 由 Full Deterministic Batch Packet 直接带给 Terra。Prose DNA 不直接进入 Primary Writer；Prose Controls 只影响 HOW TO SAY，不覆盖 BOOK Prose Profile、Chapter Mission 或 Canon。当前完成 GBrain import + embedding（15705/15705）。
## Pilot Active / HOLD

当前主 `gbrain-story-craft-v3/staging` 已确定性重建 manifest，共 **71 张 staging pages：68 active / 3 HOLD-or-reference-only**。其中真正的 HOLD mechanisms 仍是：

- `partner-reward-agency-v3`
- `reward-timing-variation-v3`

Batch D 原有 2 张 cross-book synthesis 最初均为 `active_inspiration: false`。2026-08-25 起，`reader-facing-world-coordinates-batch-d-v3` 已显式激活并提升为 production-facing **PILOT**，由 World Vision 固定作为 Coordinate Reference；其完整 cross-book 研究矩阵仍保留 Action Space / Mystery / Expectation / Impact 等坐标，但生产 Guidance 已明确区分“世界前台尺”与“读者体验/故事尺”。`gameplay-counterplay-thread-afterlife-batch-d-v3` 仍保持 REFERENCE_ONLY / `active_inspiration: false`。新 Batch D Book/Arc 与两个新 mechanism 继续保持 PILOT overlay；`reference-corpus/machine` 保持旧 validated snapshot。

## Priority Batch D 扩展（2026-08-24）

在经典样本扩展后，继续 SOURCE-FIRST 蒸馏 10 本互补长篇：《牧神记》《大奉打更人》《全球高武》《不科学御兽》《沧元图》《乱世书》《超神机械师》《明克街13号》《大王饶命》《莽荒纪》。每本由 Luna high 负责 Book DNA / World Fantasy，Sol high 负责 Longitudinal Threads / Story Program；共新增 20 张 source-specific Book/Arc Pilot。

Terra Source Fidelity 的最终权威链是 **direct raw-source audit → Required Edits → targeted recheck**：`outputs/source_fidelity_batch_d.json` 直接回原著行号得到 6 PASS / 4 PASS_WITH_EDITS / 0 FAIL；修正 locator 覆盖与 TGN Transfer 表层专名后，`outputs/source_fidelity_recheck_batch_d.json` 定向 recheck **PASS，无剩余项**。目录中更早的 pack-based `SOURCE_FIDELITY_AUDIT / REAUDIT` FAIL 记录保留作 provenance，它们暴露的是 audit pack RAW window 与宽 locator 不闭环的问题，已被后续 direct-source audit supersede，不作为最终 promotion verdict。

跨书 World synthesis 未扩张 ontology：Reader-Facing World Coordinates、Core Advantage ↔ World Compatibility、Promotion Afterlife、Concrete Value / World Desire 均 MERGE 现有机制。跨书 Program synthesis 只保留两个真正独立的新 PILOT mechanism：

- `opponent-learning-success-condition-rewrite-v3`：敌人根据已暴露事实学习，并改写主角核心优势的成功条件；
- `longitudinal-thread-dormancy-collision-afterlife-v3`：长线沉睡、行动性提醒、异质线程碰撞，以及第一次 payoff 后的 second payoff / afterlife。

其它候选继续 MERGE：首个高光后的选择空间化 → action-space / old-ability-new-use；阶段发动机换问法并续燃旧状态 → map-transition / plot-engine-variation；首五章“证明—选择—条件变化”只作 Outline 可选语法，不成为五步 Hard Gate。

本轮与 Prose Priority Batch 合并向 GBrain scoped import 32 页，runtime 从 `3753 / 15717 / 15717` 增至 **`3785 Pages / 15780 Chunks / 15780 Embedded`**；`embed --stale` 实际刷新 63 chunks，最终 embedding debt 为 0，无 root-level duplicate。

TGN retrieval regression 通过：SP01 仍以 `plot-engine-variation` 为首，SP02 仍由 `thread-collision / sacrifice-convergence` 主导，SP03 仍是 `reunion / departure / character-autonomy`，OL01 `thread-ecology` 第1，WV01 `world-desire-ladder / world-entry` 第1/2；只有明确询问“敌人怎样学习并反制”时，新 `opponent-learning` 升到第1。该次 2026-08-24 regression 中两张 reference-only synthesis 尚未激活；Reader Coordinates 已于 2026-08-25 单独 promotion 为 World 固定参考。

完整本地报告：`reference-corpus/operations/gbrain-story-craft-v3/expansion-batch-d-20260824/FINAL_BATCH_D_REPORT_20260824.md`。

## Planning Recall Widening（2026-08-25）

随着 source-specific Book/Arc、Reward、Thread、Reader Coordinates 等蒸馏材料增加，规划阶段采用 **World 固定 1 Coordinate Reference + 最多 3 creative / Story Program 最多 3 / Outline 最多 5**。当前无 query embedding 的 keyword fallback 为：World Vision 2 组互补 creative intent，Story Program 3 组，Outline 3 组；每组 `QUERY_RECALL_LIMIT=24`，多组结果 round-robin 合并并按 slug 去重，普通 creative 最多检查 12 个候选。

同一 `real-exp-system-eval14-v1` 输入的本地 regression：

- World Vision：候选 `12 → 13`，最终仍 `3/3`，保持 `story-state-compounding / world-entry / world-desire-ladder`；
- Story Program：候选 `5 → 7`，最终仍 `3/3`，从偏 Thread 的组合扩成 `plot-engine-variation / thread-collision / earned-high-value-acquisition`，Reward intent 能稳定进入竞争；
- Outline：候选 `6 → 25`，最终 `4/5 → 5/5`，覆盖 Thread、Reunion/Departure、Action Space、Hidden Identity 等互补方向；
- Reader Coordinates cross-book synthesis 现已显式 `active_inspiration: true`，并增加 `## Guidance` 作为可提取抽象；World Vision 固定按 slug 读取它作为独立 Coordinate Reference，不占 3 个 creative 名额，也不要求 Story Program / Outline 重复固定注入；
- 当前 GBrain runtime 检查为 `3786 Pages / 15783 Chunks / 15783 Embedded`，embedding debt 为 0。

这次没有新增 LLM、reranker、Agent 或 Hard Gate。单次本地三阶段 retrieval 观察到 wall-clock 从约 11 秒上升到约 14 秒，属于更多本地 query/page read 的成本；World Vision 额外固定注入 1 条压缩后的 Coordinate Reference，普通 creative 上限不变。

## Character / Relationship / World Hook Batch（2026-08-25）

为补当前 TGN 相对较弱的“人物本人值得追更 / 关系与谜团复利 / 世界与身份本身有记忆点”，SOURCE-FIRST 蒸馏三本本地原著全文：

- 《诸神愚戏》：Character Hook / Protagonist-as-IP；
- 《十日终焉》：Relationship + Mystery Engine；
- 《我不是戏神》：Character Identity + World/IP Hook。

三本共形成 **64 个 bounded evidence windows**，全部使用 `小说整理合集` 下 GB18030 canonical TXT；locator 范围检查 64/64 通过。Terra final fidelity 直接回原著复核 23 个代表窗口，结论为 `PASS_WITH_EDITS`；修正内容主要是单窗不能独立证明长期人格、跨章边界、关系判断越窗以及“不可回滚”措辞过强，不改变三本的核心 craft verdict。

跨书 Sol 去重后只新增 **1 张 active PILOT mechanism**：

- `actionable-hypothesis-reconstruction-loop-v3`：当身份、记忆、共享历史或世界解释尚不完整但人物必须行动时，先建立足够支持当前行动的局部假设；行动结果、物证、关系反应或记忆差异暴露边界后，保留已证实部分、削弱旧解释并重构模型；只有新模型真实改变下一次信任、合作、保护对象、世界入口或其它选择时，Mystery 才继续复利。Relationship reaction 只是 evidence channel，不自动成为世界事实。

其它候选均 **MERGE，不新增机制卡**：

- Character Hook / character-as-payoff / relationship chemistry → 当前 Human Seed 的 Appetite / Behavior / Relationship lanes + `character-autonomy-v3`；
- unit-event relationship/information residue → `thread-ecology-v3` + `story-state-compounding-v3`；
- identity-bearing objects / place recontextualization → `narrative-compounding-v3`；
- world desire without immediate growth utility → World Vision `Story-Bearing World` + `world-desire-ladder-v3`。

这批蒸馏当时曾提出“继续给 Fantasy Seed / World Vision 加生产规则”的候选修法。2026-08-26 的 Split Authority / Collision 根因实验已经推翻这部分生产化结论：**真正需要修改的最早节点是 Human schema 与 Story Program compiler，而不是继续给 World 增加正交删除测试。** 因此这批材料保留为研究证据，但不再作为当前 Runtime 的 production 指令。

当前 production 解释是：

1. Behavior craft 进入 Human Seed：Stable Choice Bias + Variable Realization，与 competing motives、person-specific relationships 一起构成人物权威；
2. World Vision 继续 protagonist-blind，只要求没有主角仍有具体人物、价值物、事件与奇观成立，不新增正交删除 Hard Rule；
3. Story Program 使用 native Collision contract：Growth 是全书纵向不变量，不是每阶段 Acquisition / Compounding / Power Growth 税；High-Value Acquisition 与 Compounding 保留为纵向 reader-appetite / continuity 原则；
4. Outline 继续使用既有 Story Anchor / State Change / Open Promise；Story Craft 与 Prose DNA 继续分离。章节期 Authority Reviser 不是 GBrain 消费节点：它不读取 raw GBrain，只用已批准远端 authority 的安全投影修复 Primary realization；Scene Skill 只可提供一行已验证的 failure-triggered Watch。

正式 GBrain 只新增 **3 张 `REFERENCE_ONLY / active_inspiration:false` source book cards + 1 张 active PILOT mechanism**。曾尝试给 4 张旧 mechanism 增加 alias/evidence，但 retrieval regression 显示会扰动既有排序，因此该修改已撤回；最终不通过“顺手增强旧卡”制造检索噪声。

Runtime 从 `3786 Pages / 15783 Chunks / 15783 Embedded` 更新为 **`3790 Pages / 15790 Chunks / 15790 Embedded`**，embedding debt = 0。明确 Mystery query 中 `actionable-hypothesis-reconstruction-loop-v3` 为 rank 1；单元关系残留 query 仍由既有 `story-state-compounding` 等机制主导；三张原著 book cards 在 production retrieval 中因 `active_inspiration:false` 被正确拒绝；Reward 等无关查询未被新 Mystery mechanism 抢占。

## Long-form Spine / Protagonist Tension 六书 refinement（2026-09-01）

新专项 `reference-corpus/operations/gbrain-longform-spine-tension-v1-20260901` source-first 复核《一世之尊》《诡秘之主》《大奉打更人》《全球高武》《修真聊天群》《无限恐怖》。最终 Terra raw-source fidelity 对 21 个 canonical TXT windows 判 **PASS_WITH_EDITS**；跨书 Sol 结论为 **NEW = 0**：主角张力、Book-Level Spine、Character Asset Afterlife 与 Payoff Pressure 都能由现有机制小修覆盖，不新增“主角张力卡”、Book Engine 大卡或 Payoff Scorer。

source-blind A/B 没有支持整包 Treatment 直接上线，而是得到 **SELECTIVE DIRECTIONAL PASS**：

- 《我身藏诸界》21—30 的当前 production Control 胜，原因是它已经有更强的 Main-World Return Consequence——旧 Rival 真换战术、高位势力真换报价；Treatment 虽让局部“不能全拿”更尖，却削弱了这层 Book Mutation；
- 普通单世界闻野舟样本则 Treatment 胜，主要增益来自 `Choice → Route`、未选路线继续由 NPC 推进、旧资产/关系在新语境重新进入因果；
- 因此 production 只吸收 **Decision Vector / Signature ≠ Tension、Local Closure + Book State Mutation、Historical Recontextualization、Character Afterlife without recall tax**，并保护现有更强的 Return Consequence。

GBrain 仍保持 10 张旧 active mechanism 分离，只做原位 refinement：`thread-ecology`、`longitudinal-thread-dormancy-collision-afterlife`、`thread-collision`、`character-autonomy`、`narrative-compounding`、`story-state-compounding`、`plot-engine-variation`、`reward-action-space`、`reward-afterlife`、`minimum-sufficient-public-proof`。每张都补了本专项 provenance；`PILOT_MANIFEST.json` 记录 `last_refinement_operation`，没有新增 active card 或 retrieval slot。

后续人物群 integration **仍是 NEW = 0**：没有新增/修改 GBrain 卡，而是把现有 `character-autonomy` 的“自己的欲望 + 离屏因果 + 回流 delta”、`thread-collision` 的“共享因果铰链而非角色集合”、以及 longitudinal afterlife 的休眠/余生，直接编译进 Story Program / Story Refresh / State。production 因此只让少量 Longitudinal Cast 保存自己的未完人生、已启动行动与必要的人物—人物关系，并明确 `Convergence ≠ Recall`；不新增人物图谱、全员 Human Seed 或回访配额。一次 fresh quality A/B 因同机其它 ACP 实验把全局并发抬到已知不稳定区而判 `INVALID`，不作为 promotion 证据；当前上线依据是既有 source-first cross-book evidence + deterministic prompt/state integration regression。

Embedding 最终状态为 **3834 Pages / 15863 Chunks / 15863 Embedded**，debt = 0。最初 4 个 stale chunk 来自既有 `my-dear-diary/*` 页面，不是本轮小说卡；使用当前机器合法环境配置后补齐 4/4。TGN scoped retrieval regression 通过：`thread-ecology`、`story-state-compounding / narrative-compounding`、`plot-engine-variation` 仍可直接命中；真实 `story_refresh` 默认 bundle 仍稳定返回 `thread-collision / plot-engine-variation / longitudinal-thread-dormancy-collision-afterlife` 三条，研究 operation raw 页面没有越过 active-card 边界进入 production。

完整 promotion 边界与 A/B 记录见该专项 `FINAL_REPORT.md`；若早期 per-book Evidence / Synthesis 与 `FINAL_RAW_SOURCE_FIDELITY_AUDIT.md` 冲突，以 Final Audit 的 locator 与事实/角色判断边界为准。
