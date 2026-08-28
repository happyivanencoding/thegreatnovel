# Split Character Authority｜冻结的上游创意权威

状态：**FROZEN / production**

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义当前新书的上游创意权威与信息边界，不新增 Agent、Reviewer、Scorer 或审批门来重复执行这些原则。

## 1. Production 链

```text
作者方向
  → protagonist-blind World Vision
  → POWER_BASELINE / LIFE_CONTEXT
  → 独立 Power Seed + Human Seed
  → 作者一次批准 Character
  → deterministic CHARACTER.md
  → Story Program（第一次完整 Collision）
  → Outline
```

- **没有 production Fantasy Seed。**
- Power Seed 与 Human Seed 是两份独立创意权威，但**不是两个审批门**；作者只批准一次 Character。
- 核心去相关机制是 **fresh context + authority isolation**，不是必须使用不同模型。

## 2. World Vision

World Vision 负责一个即使换掉未来主角也仍值得写的世界，包括：普通生活与上升路径、力量正常值/稀缺度、社会现实与身份后果、具体价值物、独立人物与事件、地点/奇观/危险/未知、知识边界。

它不负责主角欲望、Biography、特殊能力、命运、第一次爽点或终局使命。完整 World Canon 可以同时包含 World Reality 与 Story Opportunities，但下游可见性不同。

Reader-facing 世界规则先写具体作用，再命名：基础力量应能用 1—3 句普通话说明来源、能做什么、怎样变强和怎样失败；已有一到少数互补力量轴如果已经简单、有辨识度，就保护它，后续优先从旧语法长新招式、身体、兵器、异兽、环境、组合与稀有例外，不为“更统一”泛化成总机制；新词只给已经理解、会反复出现的对象贴短标签，不靠多个新词互相定义。“全新”优先改变力量因果与玩法，不要求回避境界、功法、兵器、异兽等清楚题材词。默认直接力量先写身体、攻击、防御、移动、元素、兵器等可感知效果；除非作者明确选择认知/概念系幻想，不把路径、定义、权限等抽象关系本身当作创新证明。

## 3. Power Seed

Power Seed 只读取确定性的 `POWER_BASELINE`，不看完整 Story Opportunities，也不看 Human Biography。

生成语法：

`世界力量正常值 → Power Novelty Spark → Power Asymmetry → 核心幻想 → 长篇成长兼容`

Power Novelty Spark 是非 Canon 的轻量随机扰动：3 个候选各取一个“熟悉能力幻想 × 单一异常”，只负责拉开候选起点；不进入 Human / Story Program / Outline。**Spark 负责不同，不负责强。** Power Asymmetry 才负责把候选推到明显超标：来源可以是世界内稀有天赋/体质、唯一奇物/际遇、外来知识/经验、外挂、极端正常天赋或少量优势叠加，不强制先证明为世界内合法例外。每个候选最多一个主异常，必须先用一句大白话讲清；默认宁可初稿偏强一档，也不要被 LLM 自动平衡成“更方便”。至少一个维度要让同层普通人/天才明显羡慕，Permanent Boundary 防万能但不做对称成本结算，优先只保留真正根边界；长期默认 **Boundary Stable, Privilege Expands**。复杂玩法从简单规则与后续功法/装备/环境等复合成长中长出来。直接型能力的后续掌握继续扩展控制、对象、战斗复合和危险场景下的稳定使用，不反向变成结构分析、材料诊断或路线计算；Legendary / Future Legend 也不能越过 Permanent Boundary。

它负责：相关正常值/稀缺度、Power Asymmetry、核心幻想、正常修炼轴、异常掌握轴、高阶质变、永久边界、传奇力量状态。

`Future Legend Image` 只用于候选审计，不进入 Canon。Power Seed 匿名，不负责姓名与个人身份，也只定义**开局 Core Asymmetry**；全书后续新非对称优势由 Story Program 通过真实获得加入。正常成长必须真实增强主角本人，异常不能只把修炼替换成更聪明的职业技能。

## 4. Human Seed

Human Seed 只读取确定性的 `LIFE_CONTEXT` 与 Human GBrain craft；对 Power 和 named Story Opportunities 保持盲态。

生成语法：

`生活事实 → 多重动机 → 冲突中的稳定选择偏向 → 具体人物关系`

核心原则：**经历是背景，不是人格证明。** Human Seed 是一个人的权威快照，不要求单一核心执念或统一人生哲学，也不把每段童年反向写成某个漂亮人格命题的证据。

它负责：初始社会位置、具体生活事实、会竞争/重排的长期私人动机、行为签名、重要关系原点与相对稳定的身份事实。

行为签名 = **稳定选择偏向 + 具体实现随现场变化**。具体关系只有在“因为是这个人”而真实改变选择时才成立；同等有用的人不能自动替代。章节期从 deterministic `CHARACTER.md` 先只截取 Frozen Human Core 投影给 Curator；Power Core 不在 Curator 重复注入。Primary 完成第一版后，固定 Authority Reviser 会重新读取 **Frozen Human Core + Frozen Power Core** 的安全确定性投影，用于恢复被近端压缩丢掉的人格/力量 realization；它们仍是只读 authority，不允许重组 Character、改写剧情或把近期行为反推成新人格。冻结 Human Core 高于后续几章的局部行为归纳：连续负责、救人、诚实或克制可以成为已发生事实和关系预期，但不能由 Curator / Writer / Reviser 反推成新的稳定道德人格。当前场景自然触发已批准的虚荣、钱、审美、身体吸引、享受、好奇、偏心等 competing motive 时，应允许它真实进入注意力与选择，不统一净化成成熟合作。

### 可变状态与非 Canon 边界

- `current private desire` 只初始化 `CHARACTER_INITIAL_STATE.md`，不冻结进 Human Core。
- `Character Hook` 只进入 `CHARACTER_AUDITION.md`，用于候选辨识，不绑定前三章，也不进入 Canon。
- `CHARACTER_INITIAL_STATE.md` 只表示 T0；章节开始后，BOOK Canon + State Delta 链仍是唯一长期运行状态权威。

## 5. Character：确定性组合

`CHARACTER.md` 只是 Power Core + Human Core 的确定性合并，**没有 Character Composer LLM**。

不得为了让两份权威显得“天生匹配”而补 Biography 或主题解释，例如“两个家所以得到双位置能力”“从事修理所以得到修理型超能力”。不协调是故事材料，不是错误。

编辑任一已选 Seed 会使 Character 及下游 Story/Outline stale，但不会重写 World。

## 6. Story Program / Collision

Story Program 是第一次同时看到完整 World、完整 Character、T0 State 与 Story GBrain / References 的阶段。

核心合同：**不要把碰撞消解成命中注定的适配。** World 与 Character 都是既定事实；Story Program 负责它们碰撞后的事件、关系、反制、后果、阶段发动机与长期因果，不能为主题整齐重写上游。

权威与调度分开：Power Seed 决定开局 Core Asymmetry 的成长语法；Story Program 决定它怎样实现，并可通过真实获得加入新的 Power Asymmetry、让新旧优势发生复合。后续新 Asymmetry 继承同一 Reader-facing 边界：先写“以前做不到什么、现在具体多能做什么”，再决定是否需要短名；新名只压缩已经理解的能力。**成长是全书纵向不变量，不是每阶段升级税。**

Collision 可以补少量**非奠基性的过去经历、共同往事或旧事件**，让当前关系、局部性格反应或选择更自然，但：

- 不得重写 Human Core；
- 不得用过去证明整个人；
- 不得为了人格合理化自动制造悲惨童年、背叛、虐待或重大失去；
- 不得自动成为小说主线或大型阶段发动机；
- **过去存在，不等于现在就告诉读者**；Outline 只在故事需要时逐步揭示。

大型阶段保持轻量：为什么现在发生、谁想要什么、主角关键选择/行动、主要阅读满足、`Stage Delta`、下一阶段为何自然发生。`Stage Delta` 只写实际变化的维度；Power、获得、关系、身份、知识、敌人或世界变化都不是必填项。

高价值获得与纵向复利是全书原则，不是阶段字段税。默认采用 **AGGRESSIVE payoff** 偏置：因果已支持的主奖励真正落地；大胜可以自然连带奖金/招揽/入口，秘境可以有主目标外惊喜，大阶段可以同时带来据点、队伍、产业或长期收入。奖励数量本身不构成失败，只禁止无因果到账与同窗口近似奖励抹平真实牺牲。Power Asymmetry 要长期形成优势栈：旧优势保留，新优势通过故事加入，并出现单项做不到的复合玩法；不要求每阶段新增。显露新优势、新层级或意外复合时，现场已有懂行者/对手/同伴的惊讶与比较本身可以完成爽感；只有重新估价会改变后续行动或关系时才进一步写态度转变。反制只能从碰撞后的学习产生，敌人不能只为机械克制主角而出生。

## 7. Outline：执行编译，不重新调度

Outline 把已批准 Story Program 编译成当前窗口的具体 Story Anchors，不是第二个 Story Program。

每块只在 `Block Delta` 中记录**相对本块开始真正变化的维度**；没有变化就省略。关系/世界驱动的块可以完全没有 Power、Possession 或新地图；反过来，Story Program 已安排在当前窗口的真实成长又不能被省略。

不得为了填表制造微升级、填充奖励、新权限或新地图。

## 8. GBrain 可见性

GBrain retrieval 与 generation prompt 使用同一 authority 边界：

- World lane：World craft；
- Power lane：只读 `POWER_BASELINE`；
- Human lane：只读 `LIFE_CONTEXT`，Appetite / Behavior / Relationship 各最多 1 条，总计最多 3 条，可为空；
- Story lane：第一次允许 Full World + Character。

Human 三个 lane 是**检索预算，不是人格必填维度**；只接受对应 lane 的 ACTIVE craft，REFERENCE_ONLY / HOLD 不为凑数补位，同一卡不占两个 lane。Power/Human 都只接收小型 inspiration bundle。Human GBrain 用来扩展欲望、行为与具体关系的判断能力，不做人格分类或人物类型菜单。

## 9. 生活纹理只在下游出现

`Life Texture / Human Appetite` 不是上游 Human Seed 字段。

当前场景自然需要时，Curator / Writer 可以从已批准 World 事实中偶尔投影 **0–1 个生活性细节**；若 Primary 漏掉而场景因此显得像无背景空间，Authority Reviser 也可以从 safe World Authority 补回一个已批准细节。它不得建立新世界规则、新人物动机、新剧情义务，也不因为出现一次就自动成为长期 Canon，更不要求每章使用。

## 10. 审批与 stale graph

批准点只有：

1. World Vision；
2. Character（Power + Human 一次批准）；
3. Story Program。

依赖方向：

`World → Power/Human → Character → Story Program → BOOK/Outline → chapters`

下游修改永不反写上游权威。World 修改会 stale Power/Human 及以下；Power 或 Human 修改会 stale Character 及以下，但不 stale World。

## 11. 显式匿名 Human Prototype

私人/作者特定 Human prototype 是**显式实验控制**，不是默认 Human craft，也不是 Character Canon。

- 默认 selector 为空，普通新书不能静默召回 prototype；
- 只有 `human_seed` 可以消费 selector，World / Power / Story / Outline 忽略它；
- selector 只允许精确解析已允许的 opaque prototype ID，不做宽泛语义回退；
- prototype 页面必须声明 `experimental_activation: EXPLICIT_PROTOTYPE_TEST`，generic Human retrieval 即使语义命中也拒绝它；
- prototype 必须提供 Appetite / Behavior / Relationship 各一张有效页面，缺失或错 lane 时 fail closed；
- 它只生成一个幻想世界中的 Human Seed，不重建现实 Biography；
- Power 在 Human 生成时仍不可见，Character 仍是确定性合并；
- prototype ID 只是生成 metadata，不进入 Character、T0、Story Program、Outline 或 prose Canon。

不要因为一个私人 prototype 好用，就把它推广成全局 Human prior。

## 12. 明确不新增

默认不新增 Character Composer、人格评分器、MBTI/trait checklist、强制怪异、强制创伤、Life Texture Agent、每人物每章独立状态 LLM、Human diversity Hard Gate。

这套架构通过**信息边界**解决后验合理化，而不是继续堆 negative-prompt 墙。
