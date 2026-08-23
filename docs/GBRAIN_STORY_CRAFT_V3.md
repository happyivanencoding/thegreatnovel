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
- `World Vision`：可读取作者选择/编辑过的 GBrain；只借鉴 world fantasy / world entry / narrative compounding，不能覆盖已批准 Fantasy Seed。
- `Story Program`（UI mode=`idea`）：可读取 GBrain；优先借鉴 Plot Engine 变异、thread ecology/collision、配角自治、story-state compounding 与 Reward/Opportunity 体验变异，不能覆盖已批准 Seed / World Vision。
- `Outline`：继续读取 GBrain；把长线、身份揭露、离队归来、牺牲/二次兑现、高价值获得等落实为具体故事锚点。
- `Director`：不负责凭空发明长期大奖励或重新设计 Story Program。
- `Curator / Primary`：Scene Skills 只控制 HOW TO REALIZE THE SCENE，不改变 Chapter Mission 或 Canon。
- `State Extraction`：继续用当前 `current_state` 记录重要能力、物品、规则、持有人与状态变化；不新增 Inventory 数据库。

## Reward 职责

高价值获得不是随机掉宝器，也不是固定章数节拍器。

Story Program 负责：在不同阶段选择当前最适合的“获得体验”，例如能力、宝物、知识、身份、师承、资格、伙伴、生命变化或世界入口。它们没有固定先后顺序，可以提前、后置、跳过或再次出现。

Outline 负责：具体机会怎样出现，主角为什么想要，谁阻止，主角怎样真正拿到，第一次怎样证明它值钱，以及哪一个旧奖励将在后文被复用或重新解释。

Director/Writer 不应为了“这一章需要爽点”自行添加计划外的长期大奖励。

## Model Routing（GBrain 蒸馏）

- Terra high：原文事实、Scene Evidence、Reward Event Evidence、source fidelity。
- Luna high：Book DNA、World Fantasy、Reward/Opportunity synthesis、Scene Skill synthesis。
- Sol high：Longitudinal Threads、Thread Braid、Story Program 跨书高级综合。

简化理解：Terra 看清发生了什么；Luna 理解为什么让人想要/想继续看；Sol 理解这些东西为什么跨几十/几百章仍然有效。

## 检索退化兼容

当前 GBrain 的 hybrid query 只有在进程可用 `OPENAI_API_KEY` 时才生成 query embedding；没有 key 时会退化成 keyword-only。TGN 因此：

1. 始终生成并展示中文 BOOK-aware Retrieval Brief；
2. 如果 semantic query 可用，后端直接使用完整 brief；
3. 如果不可用，规划节点后端内部使用少量英文 OR aliases；
4. 用户手工编辑查询时，手工 query 永远优先；
5. 返回给 LLM 的 `可用抽象` 仍来自卡片中文 Mechanism/Guidance 等正文，不把英文 aliases 注入 Prompt。

这是一层确定性 fallback，不新增 LLM、reranker、Agent 或 Hard Gate。

## Pilot Active / HOLD

当前 v3 共有 29 张 Pilot：27 张可作为 active inspiration；partner-reward-agency-v3 与 eward-timing-variation-v3 保持 HOLD。TGN 对显式 ctive_inspiration: false 的页面自动跳过。v3 尚未写入正式 eference-corpus/machine，避免在 Pilot 阶段污染旧 validated snapshot。

