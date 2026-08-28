我会按只读审计执行：先读取适用的 Scene Skill / TGN 架构研究规范，再定位 Runtime、24 张 Skill、两份 craft 文档、GBrain corpus/prose-dna 与小说合集目录；之后基于实际目录与原著可用性建立甄优矩阵。不会改生产代码、Skill 或研究资料。已确认本任务与历史的关键约束一致：Scene Skill 只负责实现方式，不能触碰 Chapter Mission / Canon；Prose DNA 只能作为受场景条件约束的机制证据，不能直接变成 Writer 风格指令。接下来读取三份本地技能规范，并只用它们要求的证据边界。这一步的检查目的很具体：确认当前分支与未提交状态，避免把旧实验误当生产；同时列出实际 Runtime / Skill / corpus 入口，决定后续只读范围。若发现未提交改动，我会避开它们；若发现 24 张并非当前 production，我会以真实调用路径为准。当前 repo 的 24 张 Skill 已核实，确实是 `scenes/` 下的 24 个文件；但工作树有大量用户/其他 agent 的未提交实验目录，我不会触碰。当前分支是 `principal_dev_new_sys`，且顶层最新提交不是 Scene Skill 升级提交，因此接下来会把未跟踪的同名实验目录当“参考候选”，不当作已冻结 production。现有文档已经给出一个重要基线：8 个宽 Prose Family、7 张 production-facing prose control、`NONE` 可空路由，以及 24 张 Scene Skill 与其独立运行时。但这不等于 24 张都已有原著证据；下一步我在区分“已有证据可复用”和“只有通用写作常识、必须回原著补窗”。这是本次矩阵的核心。已完成两条证据链的盘点：
1) Runtime 实际加载 `SCENE_SKILL_IDS` 中的 24 张文件，Curator 只选 `Primary + 可选 Secondary`，Writer 才收到完整 Skill；没有 variant 字段。
2) Prose DNA 现有证据主要是 8 个宽 family、14-window 单书采样与六维 Selection DNA；它能支撑“注意/知识/因果/反应/节奏/词汇如何选择”，但不能直接证明 Combat 的具体姿态或 Desire/Voice/Training 等新 lane。下一步据此给出“复用 / 补窗 / 暂不生产化”的矩阵。矩阵结论已经收敛：第一轮不做 24→80，也不把每个战斗姿态做成独立 Primary。建议是“保留 Combat Core + 一个受控 posture + 最多一个结果/状态 modifier”，其余 7 个高杠杆 lane 以深化现有 Skill 为主，只把 World Entry 作为新增 Primary 候选，Desire / Voice / Public Proof 先以 modifier 或现有 Skill variant 验证。下面我会按要求给出完整 Markdown。# Verdict

当前 24 张 Skill 的方向正确，但分辨率不均：多数是“通用场景发动机”，Combat、Dialogue/Voice、Desire、World Entry、Training/Comprehension、Public Proof 的具体选择问题仍未被充分编码。

建议：

- 保留当前 24 个核心引擎，不扩张到 80 个独立 Skill。
- Combat 使用 `combat core + 一个 posture + 最多一个 modifier`。
- 深化 7–8 个高杠杆 family。
- 只新增 `world_entry_lived_texture` 作为 Primary 候选；Desire、Voice、Public Proof 先作为 variant/modifier 验证。
- 所有新结论先停留在 evidence / Pilot，不直接进入 Writer。

当前 Runtime 的边界是正确的：Curator 选一个 Primary、最多一个 Secondary，Skill 只控制 HOW TO REALIZE，不改变 Mission / Canon。[Scene Skill Runtime](C:/dev/tgn-story-mvp/src/story_mvp/scene_skills.py:13) [Selection Rule](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/SKILL.md:17)

# Current Skill Gap

## 现有 24 张 Skill 的判断

| 处理 | Skill | 判断 |
|---|---|---|
| 保留核心，不拆 | `investigation`、`deduction_reveal`、`horror_anomaly`、`exploration`、`survival_endurance`、`stealth_infiltration`、`chase_escape` | 核心阅读问题与停止点已经清楚，先补证据，不增加子类 |
| 保留核心，不拆 | `hunt_acquisition`、`resource_economy`、`crafting_creation`、`recovery_restoration` | 对“取得—配置—使用—恢复”的边界已有可执行骨架，主要风险是写成流程说明 |
| 保留核心，不拆 | `trial_challenge`、`breakthrough_advancement` | “外部判定线”与“状态跨门槛”区分正确，不应再按题材拆分 |
| 保留核心，不拆 | `identity_reveal`、`departure_vacancy`、`reunion_reentry`、`sacrifice_convergence` | 已是事件型 Scene Engine，继续拆会迅速变成剧情标签库 |
| 深化 | `social_bargain_decision` | 能处理筹码变化，但不足以覆盖非交易型对白、声音差异、熟人互损和拒答 |
| 深化 | `relationship` | 核心正确，但仍偏“关系边界变化”抽象，缺少欲望、亏欠、身体距离和选择代价的证据 |
| 深化 | `comedy_banter` | 已有错位机制，但没有充分区分角色声音、信息传递与严肃场景中的喜剧停点 |
| 深化 | `training_learning`、`comprehension_insight` | 概念区分良好，但目前主要是合理的通用规则，缺原著支持的反馈密度与压缩方式 |
| 深化 | `showcase_evaluation` | 能处理尺度与反应，但把“证明自己有多强”和“改变公共判断”混在一起 |
| 拆 variant | `combat` | 当前 Core 已足够，但一套规则覆盖了势均力敌、越级、碾压、伏击、群战、保护、追击、重伤求生等完全不同的注意力与压缩逻辑 |
| 新增候选 | `world_entry_lived_texture` | 当前只有 `scene_entry` Utility，不能作为主要阅读问题被 Curator 选择；但必须先经过原著证据与 A/B |
| 暂不新增 | Desire / Temptation、Dialogue Voice、Public Proof | 先作为 `relationship`、`social_bargain_decision`、`showcase_evaluation` 的 modifier / variant，除非证据证明它们有独立的下一拍与停止点 |

有一个实际的 taxonomy 不一致：`.agents/skills/novel-scene-skills/SKILL.md` 只列出 20 个 Primary，但 Runtime 的 `SCENE_SKILL_IDS` 和目录渲染实际加载 24 个文件，包括四个事件型 Skill。[SKILL.md](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/SKILL.md:23) [scene_skills.py](C:/dev/tgn-story-mvp/src/story_mvp/scene_skills.py:13)

这不是立即要新增抽象层的问题，但升级前必须统一语义，否则后续 variant 会被误当成新的 Primary。

# Combat Research Map

Combat 不应先固定为 11 个 Skill。建议先研究四个轴：

```text
Combat Core
├── 交锋关系：parity / underdog / dominance
├── 战术姿态：counterplay / protect-hold / ambush / pursuit
├── 空间规模：duel / multi-actor / battlefield-local-POV
├── 状态条件：public-proof / wounded-survival
```

这些是待证伪的 research hypotheses，不是 production taxonomy。

| 假说 | Anchor Books | Cross-check Books | 需要验证的独立性 |
|---|---|---|---|
| parity duel | 《武道宗师》 | 《一世之尊》 | 是否需要持续追踪架势、节奏、预判，而不是普通“双方互换动作” |
| underdog upward | 《斗破苍穹》 | 《仙逆》 | 越级是否靠信息、底牌、环境和时机改变胜负，而非单纯突然增力 |
| dominance payoff | 《大圣传》 | 《吞噬星空》、 《极道天魔》 | 碾压戏是否应压缩交换，把笔墨转给 ruler、身体结果和社会重估 |
| adaptation / counterplay | 《一世之尊》 | 《全球高武》 | 对手是否会学习已暴露能力，并改写主角成功条件 |
| protect / hold | 《全球高武》 | 《永夜君王》、 《斗罗大陆》 | 保护对象、阵地或撤离窗口如何改变攻击优先级与风险 |
| ambush / assassination | 《死人经》 | 《永夜君王》 | 低信息、先手、杀意与单一接触点是否需要独立压缩规则 |
| multi-actor melee | 《全球高武》 | 《遮天》、 《吞噬星空》 | 多人混战是否应按局部目标、分工和视野组织，而非逐人描写 |
| mobile pursuit | 《仙逆》 | 《永夜君王》、 《一世之尊》 | 战斗与 chase 的边界是否由相对位置和目标控制权决定 |
| public proof | 《斗破苍穹》 | 《武道宗师》、 《斗罗大陆》 | 战斗何时已不只是取胜，而是在改变旁观者、资格和下一次定价 |
| large-scale local POV | 《遮天》 | 《吞噬星空》、 《永夜君王》 | 巨大战场如何压回一个局部人物的可知信息与身体后果 |
| wounded survival | 《永夜君王》 | 《仙逆》、 《全球高武》 | 伤势、弹药、体力和撤离窗口何时真正改变下一拍 |

第一轮建议最终只验证 5 个可能成为 production posture 的候选：

1. `duel_contest`：包含 parity / underdog / dominance 的关系姿态。
2. `adaptive_counterplay`：敌我根据暴露事实持续改写成功条件。
3. `objective_hold`：保护、守点、撤离和救援优先于击杀。
4. `ambush_pursuit`：先手、低信息、移动关系共同决定因果。
5. `battlefield_local_pov`：多人或大规模战斗只保留局部可行动态势。

`public-proof` 与 `wounded-survival` 更适合作为 modifier，不宜立即成为 Combat Primary。

# Other High-Leverage Families

| Family | 当前问题 | 建议 |
|---|---|---|
| Dialogue / Character Voice | `social_bargain_decision` 偏谈判；不能充分处理拒答、熟人互损、身份差和声音差异 | 深化现有 Skill；候选 `voice_under_pressure` 先不独立成 Primary |
| Relationship | 关系变化写得对，但缺少“这个具体的人如何改变风险阈值、去留、底牌和身体距离” | 深化；与 Desire、Identity、Sacrifice 作为局部 modifier 组合 |
| World Entry / Lived Texture | `scene_entry` 只是 Utility，不能承载第一次进入城市、组织、职业、宗教或生活圈层 | 新增候选 Primary，但必须证明其有独立阅读问题和停点 |
| Desire / Temptation | 当前没有“人物想要什么、为什么此刻失控、欲望如何改写注意和选择” | 第一轮作为 `relationship` / `resource_economy` / `showcase` modifier |
| Horror / Anomaly | `horror_anomaly` 骨架已经较好，缺少正常模型、异常升级、可依赖边界的证据分辨率 | 深化，不拆题材子类 |
| Exploration / Discovery | `exploration` 已有行动地图，但未区分奇观、路线、线索、异常和调查转换点 | 深化；与 `investigation` 保持明确切换边界 |
| Training / Comprehension | 当前区分“练熟”和“想明白”，但容易写成教程、重复失败或无反馈修炼 | 深化；不拆成导师型、独修型、顿悟型三个 Skill |
| Showcase / Public Proof | `showcase_evaluation` 解决“有多强”，不完全解决“外界为何必须改变判断” | 深化，并加入 `minimum_sufficient_public_proof` modifier |

现有 Prose Craft 文档已经支持这一方向：它把证据压缩为 Attention、Knowledge、Causal、Reaction、Rhythm、Lexical 六维，并明确“Detail Selection 不是增加 sensory density”。[GBRAIN_PROSE_CRAFT_V1.md](C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md:250)

# Book Selection Matrix

`R` = 当前 `reference-corpus/prose-dna` 有直接 scene-function / Selection DNA，可复用。
`P` = 有其它 GBrain Story / Character evidence，但没有针对本 lane 的 Prose DNA。
`N` = 只有小说整理合集原著，必须新建 canonical evidence windows。

| Research Lane | Anchor Books：为什么值得读 | Cross-check Books：为什么不能只读 Anchor | 现有证据与动作 |
|---|---|---|---|
| Combat | 《斗破苍穹》：越级、底牌递进、公开重估；《大圣传》：身体性与压制 payoff；《武道宗师》：技术型势均力敌 | 《仙逆》检验致命简化；《全球高武》检验群战、伤势和保护；《死人经》检验伏击；《遮天》检验大尺度 | 斗破、大圣、仙逆、死人经、遮天为 `R`；武道宗师、一世之尊、永夜君王、吞噬星空多为 `N`，必须回原著 |
| Dialogue / Voice | 《死人经》：高压拒答、联盟、背叛和潜台词；《将夜》：关系、身份和礼数共存；《修真聊天群》：群体声音、误解和喜剧节奏 | 《第一序列》检验普通生活中的声音；《大奉打更人》检验调查与多人对白是否变成会议 | 三书及第一序列、将夜有 `R`；但现有窗口不是 voice-matched study，仍需新窗 |
| Relationship | 《仙逆》：长期执念如何改变行动；《大圣传》：欲望、身体与关系不被净化；《幽冥仙途》：危险关系与临时合作 | 《十日终焉》检验关系记忆与谜团互相作证；《我不是戏神》检验身份和关系位置变化 | 六本核心 Prose DNA 有 Emotion 窗；十日终焉有 `P` Character/Relationship evidence；须补“关系改变选择”的现场窗 |
| World Entry / Lived Texture | 《将夜》：城市、书院、荒原和阶层入口；《诡秘之主》：职业、宗教、城市生活与超凡圈层如何同时存在 | 《道诡异仙》检验日常模型失效前的生活锚点；《第一序列》检验灾后普通生活与价值物 | 将夜、诡秘、道诡、第一序列有 `R`；但首次进入与“立刻想做什么”尚需新窗 |
| Desire / Temptation | 《大圣传》：不驯化的力量欲望；《斗破苍穹》：资源、面子、机会与占有欲；《掠天记》适合检验抢夺与自利 | 《诸神愚戏》检验荒诞表演背后的贪婪、承诺和偏心；《我不是戏神》检验身份欲望是否改变行动 | 大圣、斗破有 `R` 但非 Desire 专项；诸神愚戏有 `P` Character evidence；掠天记、我不是戏神需新窗 |
| Horror / Anomaly | 《道诡异仙》：正常模型、身体、因果和解释边界逐步失效；《我有一座冒险屋》：空间进入、恐惧和行动目标共存 | 《神秘复苏》检验规则型异常；《深海余烬》检验尺度、未知和船上日常 | 道诡、诡秘有 `R`；冒险屋、神秘复苏、深海余烬需新窗 |
| Exploration / Discovery | 《遮天》：奇观、路线和历史回流；《诡秘之主》：城市探索与知识边界；《天启预报》适合检验世界奇观如何落到局部行动 | 《道诡异仙》检验探索是否转成生存/调查；《仙逆》检验探索后的旧信息重释 | 遮天、诡秘、道诡、仙逆有 `R`；天启预报需按新问题补窗 |
| Training / Comprehension | 《武道宗师》：反馈、对手、节奏和可重复动作；《凡人修仙传》：稳态成长与重复压缩；《灭运图录》：理解升级后故事问题变化 | 《修真四万年》检验制作、理解与世界问题的联动；《吞噬星空》检验突破后第一次应用 | 当前没有这组 lane 的直接 Selection DNA，主要是 `N`；必须新建证据 |
| Showcase / Public Proof | 《斗破苍穹》：最低充分证明、公开重估与行动空间；《斗罗大陆》：公开竞技与团队身份；《全球高武》：战绩、阵营和公共代价 | 《第一序列》检验非修炼型能力如何被社会承认；《武道宗师》检验裁判、观众与实际成绩的最小用量 | 斗破、全球高武、第一序列有 `R`；斗罗、武道宗师需新窗 |

现有六本 Prose DNA 的直接价值集中在：斗破的行动/公开证明、遮天的尺度/探索、仙逆的情绪与战斗、大圣传的身体和力量兑现、幽冥仙途的信息差、死人经的高压对白。[Prose DNA 目录](C:/GoogleDrive/笔记/卡片盒子/20_Knowledge/修仙小说素材库/reference-corpus/prose-dna)

但 Selection Prose DNA v2 多数只是重组既有窗口，并没有为 Combat posture、Desire、Training 或 Voice 建立新证据。因此“已有 v2”不能等同于“该问题已经研究过”。[Prose Craft v1](C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md:250)

# Evidence Questions

## Combat

1. 作者何时把笔墨从招式名称转向方向、距离、接触、失衡和身体结果？
2. 哪些交换被压缩后，读者仍能还原胜负模型；哪些省略会造成因果断裂？
3. 当前胜负 ruler 是同阶技术、越级缺口、环境、保护对象，还是公共判定？
4. 对手在看见主角能力后，何时改变目标、节奏、站位或成功条件？
5. 保护/守点/撤离如何改变“最优攻击”？
6. 伏击与追击中，有限视野和相对位置如何承担恐惧与因果？
7. 大规模战场如何选择一个局部 POV，并让局部结果反映整体态势？
8. 伤势、资源和体力何时真正改变下一拍；战斗在哪个结果已经成立的节点停止？

## Dialogue / Character Voice

1. 同一压力下，不同人物首先注意的是面子、利益、危险、关系还是信息？
2. 哪些回答、拒答、沉默、反问或称呼变化真正改变筹码、关系或行动？
3. 专业信息如何进入对白而不变成会议记录？
4. 熟人互损或喜剧是否在传递事实、暴露关系，还是只承担换气？
5. 如何用动作、距离和不回答承载潜台词？
6. 一段对白在“关系状态已经改变”后何时停止？

## Relationship

1. 关系戏中哪一个具体私人欲望使人物改变去留、风险阈值或选择？
2. 关系历史何时通过一个物件、称呼、身体动作或拒绝进入当前现场？
3. 双方的反应是否改变了下一拍，而不是只证明情绪存在？
4. 关系 payoff 后，文本保留了什么新的尴尬、边界、亏欠或行动位置？
5. 哪些内心解释被省略后，读者仍能从行为准确读出关系变化？
6. 新边界成立后，为什么继续互动已经不再提供新关系信息？

## World Entry / Lived Texture

1. 第一次进入陌生地方时，作者优先选择哪些生活细节，而不是地理百科？
2. 哪个物件、价格、礼仪、服饰或空间位置同时说明“这里是什么”和“人物为何在意”？
3. 普通知识与仍然未知的谜底如何分界？
4. 世界 Orientation 何时结束并回到人物的目标、选择或冲突？
5. 哪些环境细节删掉后会损失行动可能性、阶层判断或欲望，而哪些只是氛围？

## Desire / Temptation

1. 欲望如何通过注意对象、靠近、舍不得、冒险或回避进入 POV？
2. 人物的欲望何时与安全、职责、关系或长期利益发生真实竞争？
3. 诱惑的价值 ruler 是金钱、占有、面子、身体、好奇、报复还是身份？
4. 欲望造成的身体和空间变化是否改变了行动，而不是只增加心理说明？
5. 欲望已经迫使人物做出选择后，文本在哪个可观察后果处停止解释？

## Horror / Anomaly

1. 异常发生前，哪一个正常模型被建立到足以让读者知道它为何失效？
2. 第一个异常改变的是安全、时间、空间、身份、身体还是因果可信度？
3. 人物先采取什么现实解释或测试；异常如何回应并削弱该解释？
4. 恐怖信息怎样保持“发生了什么”清楚，同时保留“为什么”未知？
5. 反复异常何时仍有新意义，何时只是堆诡异名词？
6. 异常在哪个具体行动被迫改变时停止，并转入逃离、调查或战斗？

## Exploration / Discovery

1. 探索目的或最低生存需求何时被明确？
2. 哪个环境发现改变了路线、风险、资源或目标？
3. 作者如何在奇观与行动地图之间分配注意力？
4. 发现、调查、异常和追踪的切换点由什么现场变化触发？
5. 读者何时已经知道足够内容可以期待下一步，而不需要继续导览？

## Training / Comprehension

1. 训练目标是否被写成速度、精度、稳定性、消耗或适用条件，而非抽象“变强”？
2. 每次练习的反馈改变了什么：动作、理解、身体、方法还是下一目标？
3. 哪些重复失败被压缩，哪些失败必须保留才能解释人物改变练法？
4. 导师或人物自己的解释是否只回答当前失败，而不是完整讲义？
5. 新理解何时通过一次预测、试验或应用获得现实反馈？
6. 练熟、想明白、突破和第一次展示的停点如何分别判断？

## Showcase / Public Proof

1. 公共证明前，旧判断和可证伪标准是否已经清楚？
2. 证明结果需要展示多少，才能让旁观者无法继续按旧判断行动？
3. 哪个 ruler 最有效：身体结果、速度、精度、价格、资格、裁判判定还是敌人改策？
4. 不同立场的反应是否改变待遇、敌意、资源、身份或下一次挑战？
5. 结果成立后是否立即落到现实行动空间，而不是继续追加“他很强”的反应？
6. “最低充分证明”已经完成时，为什么继续测试只是重复？

# Priority & Agent Plan

## Priority S

第一轮真正建议启动 9 个深读 agent，不按每本书单独开几十个 agent，而是每个 agent 负责一个可比较的问题。

1. `combat_duel_asymmetry`：武道宗师、斗破苍穹、仙逆
2. `combat_dominance_body_scale`：大圣传、吞噬星空、极道天魔
3. `combat_adaptation_hold`：一世之尊、全球高武、斗罗大陆
4. `combat_ambush_pursuit_wound`：死人经、永夜君王、仙逆
5. `combat_multi_actor_local_pov`：遮天、全球高武、吞噬星空
6. `dialogue_voice_pressure`：死人经、将夜、修真聊天群、第一序列
7. `relationship_choice_gravity`：仙逆、大圣传、幽冥仙途、十日终焉
8. `world_entry_lived_texture`：将夜、诡秘之主、道诡异仙
9. `horror_normal_model_failure`：道诡异仙、我有一座冒险屋、神秘复苏

每个 agent 应输出 6–12 个 bounded windows，字段固定为：

- 原著定位：章节、segment、行号；
- 现场目标与人物当前知识；
- 选择了哪些细节；
- 压缩了哪些细节；
- ruler / reaction / body-space consequence；
- 下一拍由什么产生；
- stop point；
- counterexample / limitation。

## Priority A

1. `desire_temptation_choice`：大圣传、斗破苍穹、诸神愚戏、掠天记
2. `exploration_discovery_route`：遮天、诡秘之主、天启预报、道诡异仙
3. `training_comprehension_feedback`：武道宗师、凡人修仙传、灭运图录、修真四万年
4. `showcase_minimum_public_proof`：斗破苍穹、全球高武、斗罗大陆、第一序列

## Priority B

- Comedy/Banter 单独拆分；
- Identity / Reunion / Departure / Sacrifice 再拆子类；
- Recovery、Craft、Resource、Routine 等已经有清楚核心的问题；
- 任何只会增加“细节密度”而不能改变选择、因果、反应或停止点的研究。

深读完成后，先做跨书 synthesis，再做 Terra source-fidelity audit，最后用同一 Chapter Mission / Canon 做 blind A/B。只有某个 variant 能稳定减少具体失败，并且不改变故事事实，才进入 Pilot。

# Risks

1. **已有 Prose DNA 被误当作新证据**：v2 多数只是重组已有窗口；Combat posture、Desire、Training 仍有 evidence debt。
2. **taxonomy 膨胀**：若把 parity、underdog、dominance、ambush 等都做成独立 Primary，Curator 会变成标签填表，Prompt 也会膨胀。
3. **Combat variant 互相正交叠加**：public proof、wounded、multi-actor 常常是 modifier，不应与主体姿态并列为多个 Primary。
4. **source-specific style leakage**：Prose DNA 继续保持 `active_inspiration: false`；只迁移选择机制，不迁移口吻、句法、专名或签名表达。[Prose DNA boundary](C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md:63)
5. **raw GBrain 越过章节边界**：Runtime 已明确 Primary 不直接读取 raw GBrain，Authority Reviser 也固定关闭 raw GBrain。[Story Craft runtime boundary](C:/dev/tgn-story-mvp/docs/GBRAIN_STORY_CRAFT_V3.md:18)
6. **把 supporting logic 写成场景主线**：训练、验证、战术、调查都可能退化成教程或流程；必须持续问“这一步是否改变选择、关系、空间、身体或社会判断”。
7. **只看胜负，不看读者模型**：Combat 研究不能只记录谁赢，要记录读者何时知道 ruler、何时理解反制、何时感到结果已经完成。
8. **首轮 agent 过多且不可比较**：每个 agent 必须使用相同 evidence schema、相同 locator 规范和相同 counterexample 要求；否则得到的是书评，不是可迁移矩阵。
9. **工作树污染**：当前 repo 有大量未提交实验和一个未提交的 Scene Skill deep-upgrade 目录；本次未修改任何文件，也未把这些候选 prompt 当成已验证证据。
