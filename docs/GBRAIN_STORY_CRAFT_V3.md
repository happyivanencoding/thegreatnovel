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
| Director | GPT-5.6 Luna high | 需要 Narrative Salience 与对 Outline 的稳定理解 |
| Curator | GPT-5.6 Terra high | 任务偏筛选、压缩和去 planning leakage；快速与克制比继续发散更重要 |
| Primary Writer | GPT-5.6 Luna high（暂定） | 正文尚未完成严格 Terra/Luna/Sol 同输入盲测，规划测试不能替代 prose 测试 |
| State Extraction | 更快、更便宜；GPT-5.6 系列时优先 Terra | 只记录已发生事实，不需要高级创作推理 |

模型不是线性排名：

- **Terra high**：快、直接、克制，适合 evidence、fidelity、Curator、快速 A/B；
- **Luna high**：当前最佳综合主力，适合 Fantasy/World/Outline 与复杂约束执行；
- **Sol high**：长篇“多想一层”最强，但明显更慢，默认只集中在 Story Program 或 Deep Planning 修复；
- **Luna max**：仅用于疑难创意救援、最高质量基线和关键重构，不日常使用；
- **GPT-5.4 high**：当前实测中比 Luna high 慢且没有补偿性优势，更易系统/Build 化，不作为默认创作模型。

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

这只是一个高风险 Seed 的实测，不把 29 张 v3 Pilot 直接提升成正式 machine VALIDATED；继续通过真实新书验证后再 promotion。
## 检索退化兼容

当前 GBrain 的 hybrid query 只有在进程可用 `OPENAI_API_KEY` 时才生成 query embedding；没有 key 时会退化成 keyword-only。TGN 因此：

1. 始终生成并展示中文 BOOK-aware Retrieval Brief；
2. 如果 semantic query 可用，后端直接使用完整 brief；
3. 如果不可用，规划节点后端内部使用少量英文 OR aliases；
4. 用户手工编辑查询时，手工 query 永远优先；
5. 返回给 LLM 的 `可用抽象` 仍来自卡片中文 Mechanism/Guidance 等正文，不把英文 aliases 注入 Prompt。

这是一层确定性 fallback，不新增 LLM、reranker、Agent 或 Hard Gate。

## Pilot Active / HOLD

当前 v3 共有 29 张 Pilot：27 张可作为 active inspiration；`partner-reward-agency-v3` 与 `reward-timing-variation-v3` 保持 HOLD。TGN 对显式 `active_inspiration: false` 的页面自动跳过。v3 尚未写入正式 `reference-corpus/machine`，避免在 Pilot 阶段污染旧 validated snapshot。
