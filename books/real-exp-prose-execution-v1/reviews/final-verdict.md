# Frozen Upstream + 3-Chapter Execution & World Engine Test v1：最终报告

## 1. 实验结论

- Reader Verdict：`STRONG_OPENING`
- World Engine Verdict：`EARLY_WORLD_ENGINE_HEALTHY`
- Execution Pipeline Verdict：`EXECUTION_PIPELINE_HEALTHY`
- 本轮没有进入第 4 章。
- 本轮没有修改生产源码、生产 Prompt、Frozen 上游、GBrain、Canon Contract、State Delta 逻辑或其它生产逻辑。

盲读者认为前三章已经让读者看见一个具体的主角、一个可复述的核心玩法和一次实际主动收益；Execution Fidelity Reviewer 没有发现上游设计在 Director、Chapter Prep 或 Writer 执行层被丢失或扭曲；World Engine Reviewer 在三章范围内观察到资源、NPC、管理秩序和阵营利益均会在沈砚停下时继续运转。

同时，AI 味 Reviewer 发现了 Writer 层的“过度完成”：动作、感知和局部细节经常在刚出现后立即被命名、解释或总结，对白也偏向完整的格言式判断。这是正文实现层的观察结果，不足以重开本轮冻结的上游设计，也没有改变三个总判定。

## 2. 仓库、分支与冻结基线

- 仓库：`happyivanencoding/thegreatnovel`
- branch：`principal_dev_new_sys`
- experiment start HEAD：`5992f62d11e8014c3cf783bf993589e1cb881585`
- Long-Form Pacing baseline：`2c1e3434b6d68043ba0aac556e63d7912ba23368`
- Frozen baseline：`CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2`
- 实验目录：`books/real-exp-prose-execution-v1/`

本轮使用《掌中天工》candidate-b 的 Dynamic Pacing Treatment：

- `source/fantasy_seed.md`：candidate-b `legacy_seed.md`
- `source/world_vision.md`：candidate-b `treatment_world_vision.md`
- `source/story_program.md`：candidate-b `treatment_story_program.md`
- `source/outline.md`：candidate-b `treatment_outline.md`
- Frozen Future 10：直接使用 `source/outline.md` 的 `# 未来十章逐章小纲`
- Control Outline：未读取、未使用

运行副本 `BOOK.md` 承载 Frozen Outline，`FANTASY_SEED.md`、`WORLD_VISION.md`、`PROPOSAL.md` 和 `CREATIVE_STATE.json` 只用于当前真实工作台的输入与批准边界。三个上游 artifact 在本实验状态中均为 `author_approved`；没有把模型生成、模型选择或普通保存当作批准。

## 3. 真实执行链与产物

本轮使用当前分支正式 Prompt 渲染函数、Run Ledger、章节保存和 State Delta/Canon 应用逻辑。实际链路为：

`Frozen Future 10 → Director → Chapter Prep → Context Curator → Primary Writer → 0—2 个 Director 建议的 Specialist → Revision Integrator（有有效 Patch 时）→ 正式正文 → State Delta / Canon`

所有生成节点均由独立真实子代理执行。每个节点先保存完整 rendered Prompt，再把同一份 Prompt 交给子代理；生成 Agent 没有看到本实验的 Reviewer 标准、Reviewer 输出或实验选择理由。本轮没有 GBrain 查询、Inspiration Results 或 Reference Programs。

### Chapter 1

- Director：`runs/chapter-0001/director_prompt.md` / `director_response.md`
- Chapter Prep：`runs/chapter-0001/chapter_prep_prompt.md` / `chapter_prep_response.md`
- Writer：`runs/chapter-0001/primary_prompt.md` / `primary_response.md`
- 实际 Hybrid：Curator、Opening Specialist、Emotion Specialist、Integrator 均有正式 Prompt/Response；Dialogue、Action 按 Director 建议 skipped。
- 最终来源：`integrator`
- 正式正文：`chapters/chapter-0001.md`，6308 字符
- State Delta：`runs/chapter-0001/state_delta_prompt.md` / `state_delta_response.md`
- Canon：应用后 `BOOK.md` 标记 `当前已完成第1章。`

### Chapter 2

- Director：`runs/chapter-0002/director_prompt.md` / `director_response.md`
- Chapter Prep：`runs/chapter-0002/chapter_prep_prompt.md` / `chapter_prep_response.md`
- Writer：`runs/chapter-0002/primary_prompt.md` / `primary_response.md`
- Director 未启用 Specialist；四个 Specialist 均按正式 Ledger 标记 skipped，没有生成假 Response；Integrator 按正式 fallback 跳过。
- 最终来源：`primary`
- 正式正文：`chapters/chapter-0002.md`，7614 字符
- State Delta：`runs/chapter-0002/state_delta_prompt.md` / `state_delta_response.md`
- Canon：应用后同时保留第 1、2 章摘要，并标记 `当前已完成第2章。`

### Chapter 3

- Director：`runs/chapter-0003/director_prompt.md` / `director_response.md`
- Chapter Prep：`runs/chapter-0003/chapter_prep_prompt.md` / `chapter_prep_response.md`
- Writer：`runs/chapter-0003/primary_prompt.md` / `primary_response.md`
- Director 未启用 Specialist；四个 Specialist 均按正式 Ledger 标记 skipped；Integrator 按正式 fallback 跳过。
- 最终来源：`primary`
- 正式正文：`chapters/chapter-0003.md`，10976 字符
- State Delta：`runs/chapter-0003/state_delta_prompt.md` / `state_delta_response.md`
- Canon：应用后同时保留第 1—3 章摘要，并标记 `当前已完成第3章。`

三章 manifest 均为 `run_status=completed`，State Delta 均为 `completed`；没有结构重试，没有内容质量重试，没有换模型，没有挑选多次结果。

## 4. State / Canon 连续性

1. Chapter 1 只让沈砚从坏矿车和碎阵盘中确认仍有回响的残件，并看见“散灵无法回体”的具体问题；没有提前得到护腕、炉台或逃生身份。
2. Chapter 2 真实使用 Chapter 1 的三件残件，经过晶核承压失败、右臂受伤、调整间隙和修车验证，得到可重复调用但受限的灵回护腕；霍沉因修车灵痕与回收记录不一致而改变回收命令。
3. Chapter 3 真实承接护腕、右臂伤势和霍沉的提前回收，把监管升级为强制集中；沈砚将新增薄铜、晶核碎屑和阵盘残路分散藏进回收车，并确认废器沿下行轨道进入中央镇灵阵；护腕晶核接近极限，北侧旧巷被证明只能误导搜查，不能成为带人出口。
4. State Delta 应用后 `BOOK.md` 的 Canon Memory 累积三章摘要、主动场景、持久 Canon、未兑现承诺和作者备注；正文没有泄漏 State 清单。

证据文件：`runs/chapter-0001/state_delta_response.md`、`runs/chapter-0002/state_delta_response.md`、`runs/chapter-0003/state_delta_response.md`、`state_delta_approval.md`，以及 `reviews/cross-chapter-review.md`。

## 5. Reader Review

完整报告：`reviews/blind-reader-review.md`

主要结论：

- 第一章的阅读问题来自有期限、有监视、有身体成本的回收工作和“散掉的灵如何回来”，不是人工悬念句。
- 沈砚通过筛选残件、避验印、分散藏件、失败后重排结构和利用车路争取时间成为具体的人。
- 护腕的表层收益可以直接复述为：把废铜和裂晶核拼成能把漏掉灵力兜回来的护腕，再用多出来的一口力修动车轮。
- 第一次主动收益在第二章已经发生，因此没有 `PAYOFF_TOO_DEFERRED`。
- 三章结束读者已经知道本书怎么玩：从废器中找出仍有回响的部分，按受力和方向重新组合成工具，再用维修、流转和现场压力争取下一次成长。

Reader Verdict：`STRONG_OPENING`。

## 6. Execution Fidelity Review

完整报告：`reviews/execution-fidelity-review.md`

检查结果：

- Director 不是只扩写小纲；三章均决定了进入点、冲突顺序、信息暂缓、反作用和自然结尾。
- Chapter Prep 没有把后续逆灵炉、完整世界历史或超出场景的工程说明塞进前三章。
- Writer 的结构词均被铜片、晶核、车轮、血、炉印、封口筐、下行轨道和地底脉动承载。
- 三章均是动作先发生，必要解释在动作中或之后补足；没有发现 `EXPOSITION_BEFORE_ACTION`。
- 没有发现需要归因到 Director、Chapter Prep、Writer 或 State/context 的执行失败。

Execution Pipeline Verdict：`EXECUTION_PIPELINE_HEALTHY`。

## 7. World Engine Observation

完整报告：`reviews/world-engine-review.md`

三章只给 Early Signal，但证据已经超过单一主角外挂：

- 资源有共享社会关系：废器需要清点、拆卸、过秤、入筐；晶核既是矿场废料，也是炉宗材料和沈砚的临时节点；未验废器会被集中送入阵眼。
- NPC 有独立运动：霍沉持续核名册、重排炉籍、验印、改回收制度；唐鹭执行自己的搬运和分区任务，并明确帮助边界。
- 规则长出社会行为：停工会被记编号，换班制造有限窗口，水槽放水、车辙、重量、验印和下行轨道改变每个人的行动。
- 阵营有独立利益：矿场和太衡炉宗的资源控制、封矿、炉籍和中央镇灵阵目标不以沈砚出现为前提。
- 当地生存常识通过动作可见：搬运队、守阵修士、矿奴和唐鹭都知道如何在既有流程中避开、服从、协作或利用窗口。

World Engine Verdict：`EARLY_WORLD_ENGINE_HEALTHY`。

## 8. AI 味 Review

完整报告：`reviews/ai-style-review.md`

实际发现，且归因最近于 Writer：

- 句子和段落过度工整，常把测试拆成输入—反应—结论的完整三格，产生实验记录感。
- 反复使用“不是 A，而是 B”的否定转正句式，迅速替读者完成分类。
- 动作和感官结果出现后立即被旁白解释为规则、策略或命题，未留下足够延迟。
- 主题句和章末判断出现得过于规律，局部结果反复被提升为“路/回收/回来/时间”的完整总结。
- 对白有轻度格言化，不是大段讲设定；不同人物都偏向短促、对称、可引用的判断句。
- 小动作和环境细节真实存在，但大多立刻承担信号、测量、遮挡或记忆功能，缺少无效或暂时无意义的杂质。

同时，报告明确未发现“完全缺少自然小动作”“完全没有错误判断”或“大段对白倾倒世界观”。因此这是 Writer 层的执行观察，不足以归因上游设计，更不构成自动改写或重跑理由。

## 9. Cross-Chapter Review

完整报告：`reviews/cross-chapter-review.md`

- Chapter 1 残件与“让散掉的灵回来”在 Chapter 2 直接变成灵回护腕、伤势与修车收益。
- Chapter 2 的护腕、伤势、记录异常和泥痕路线在 Chapter 3 直接变成强制集中、反查、分散藏件和中央阵眼线索。
- 沈砚持续以自己的维修经验和判断行动；唐鹭受搬运、分区和检查约束；霍沉持续推进自己的监管目标。
- 章节间以同一辆车、同一枚铆钉、同一条回收命令和真实状态变化桥接，没有瞬移或状态倒退。
- 未发现 `STATE_RECAP_LEAK`。

## 10. 预注册标记汇总

| 标记 | 结果 | 最近证据/归因 |
|---|---|---|
| `ABILITY_EXPLANATION_OVERHEAD` | 未出现 | 能力收益由漏灵回体、修动车轮的动作直接成立 |
| `COMPLEX_BACKEND_SIMPLE_PAYOFF` | 出现 | 复杂残路/承压底层对应清楚的护腕与修车收益 |
| `PAYOFF_TOO_DEFERRED` | 未出现 | 第2章完成护腕并用于修车，首次主动收益已到账 |
| `ENGINE_NOT_VISIBLE` | 未出现 | 三章已形成“废器观察→组合工具→维修/流转争取窗口”玩法 |
| `ENGINE_VISIBLE_STORY_THIN` | 未出现 | 玩法推进同时伴随霍沉、唐鹭、矿场秩序和阵眼压力 |
| `DIRECTOR_AS_EXPANDER_ONLY` | 未出现 | Director 具体决定动作顺序、反作用和信息暂缓 |
| `PREP_OVERLOAD` | 未出现 | Chapter Prep 只准备当章拆解、试制、藏件和流程压力 |
| `DESIGN_LANGUAGE_LEAK` | 未出现 | 结构词均由物体、火/灵、血、声音和动作承载 |
| `EXPOSITION_BEFORE_ACTION` | 未出现 | 主要章节均先进入劳动/试制/回收动作，再补必要解释 |
| `PROTAGONIST_ONLY_RESOURCE` | 未出现 | 废器、晶核和回收流程有管理、用途与争夺关系 |
| `NPC_ORBITS_PROTAGONIST` | 未出现 | 霍沉与唐鹭均有主角之外的工作、利益和边界 |
| `NPC_HAS_INDEPENDENT_MOTION` | 出现 | 霍沉改制度、唐鹭执行搬运和分区任务 |
| `RULE_WITHOUT_SOCIAL_CONSEQUENCE` | 未出现 | 炉籍、验印、回收令和车流自然产生队列、服从、搜查和藏件行为 |
| `FACTION_ONLY_PLOT_OBSTACLE` | 未出现 | 太衡炉宗/矿场有持续的封矿、资源集中和中央阵眼利益 |
| `FACTION_HAS_INDEPENDENT_INTEREST` | 出现 | 管理方在沈砚不参与时也会清空、分区、验印、送入阵眼 |
| `WORLD_COMMON_SENSE_VISIBLE` | 出现 | 当地人按水槽、换班、过秤、车流、炉籍和搜查常识行动 |
| `STATE_RECAP_LEAK` | 未出现 | 状态归纳均紧贴触摸、验印、推车、藏件等动作 |

## 11. Reader / World / Pipeline 三项最终判定

### Reader Verdict

`STRONG_OPENING`

满足：主角有辨识度；核心能力已经产生明确表层快感；前三章有真实推进；读者知道本书怎么玩；人物和世界不只是工具；没有严重能力解释负担。

### World Engine Verdict

`EARLY_WORLD_ENGINE_HEALTHY`

这是三章范围内的 Early Signal，不宣称整个长篇最终已经验证完成。

### Execution Pipeline Verdict

`EXECUTION_PIPELINE_HEALTHY`

上游 Dynamic Outline 的主要动作链、收益节奏、人物压力和信息暂缓成功进入正文。AI 味问题主要在 Writer 表达实现，不是 Director、Chapter Prep 或 Frozen Outline 失败。

## 12. 最近失败层与是否重开 Frozen Prompt

- 最近的实际问题层：`Writer`
- 问题性质：表达层“过度完成”，包括即时解释、否定转正、主题总结、对白格言化和功能化细节。
- 是否有足够证据重开 Fantasy Seed：否。
- 是否有足够证据重开 World Vision：否。
- 是否有足够证据重开 Story Program：否。
- 是否有足够证据重开 Frozen Outline：否。
- 是否自动修改 Director、Chapter Prep、Writer、World Engine 或正文：否。

当前证据支持把 Writer 层问题保留为下一轮独立假设，而不是把本轮健康的上游冻结重新打开。

## 13. Git 状态

最终复核时，目标实验目录为本轮新增产物；生产源码和测试未出现 diff。工作树同时存在两个不属于本实验、未由本报告处理的未跟踪目录，已保留原样：

```text
?? books/real-exp-clean-e2e-novel-v1/
?? books/real-exp-prose-execution-parallel-v1/
?? books/real-exp-prose-execution-v1/
```

本轮不删除、不合并、不提交这些并行/未跟踪目录；如需 Git 提交，应只选择 `books/real-exp-prose-execution-v1/`。

## 14. 停止边界

本报告写入后停止。没有生成第 4 章，没有根据 Reviewer 结果修改系统，没有重写前三章，没有重新打开 Frozen 上游。
