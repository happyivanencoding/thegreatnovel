# Story MVP 产品方向

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义当前产品方向、创意权威与 Anti-Goals；架构细节见 `docs/PIPELINE_METHODOLOGY_AND_VALUES.md` 与 `docs/SPLIT_CHARACTER_AUTHORITY.md`，历史实验不自动成为当前规范。

## 一句话产品目标

TGN 要生成的是成熟中文男频成长长篇：读者明确想拥有主角的力量、生命状态、行动自由或其它非对称优势；主角本人长期真正变强；同时这个人仍有自己的欲望、关系与人生，世界也不是为金手指搭出来的测试场。

**Fantasy First 是读者价值优先级，不再是 production 阶段顺序。**

当前真实生产链路是：

`作者方向 →（可选）Premise Forge S1/S2/S3 → Independent Compiler → 作者批准 / 显式跳过 → protagonist-blind World Vision → POWER_BASELINE / LIFE_CONTEXT → 独立 Power Seed + Human Seed → 作者一次批准 Character → deterministic CHARACTER.md → Story Program（第一次完整 Collision）→ 作者批准 → Outline / Future-10 → Full Deterministic 4—6章 Authority Packet（默认5）→ Terra Batch Primary → Sol Batch Authority Delta → 整批采用 → State Extraction逐章落盘`

没有 production Fantasy Seed，也没有 Character Composer LLM。Premise Aperture 只在 Authority 冻结前搜索完整大胆货架前提：候选 Non-Canon，Compiler 不评分/选择/修稿，批准后由代码拆成四条 lane contract，Story Program 后不再下传 raw card。

当前作者批准点保持紧凑：

1. 可选 Premise Contract；
2. World Vision；
3. Character（Power + Human 一次批准）；
4. Story Program。

模型生成、模型选择和作者编辑都只是 draft；作者明确批准才形成创意权威。

## Fantasy-First 读者承诺

- 主角本人越来越能做什么，是一级成长主轴；
- Core Power 不只要新，还要形成相对同层普通人/天才清楚可比、值得羡慕的超标优势；允许有条件越级，边界防万能而不抹平爽感；
- 非对称优势要长期形成**优势栈**：开局核心继续成长，后续加入新的 Power Asymmetry，并让新旧优势产生单项做不到的复合玩法；不要求每阶段新增；
- 永久/累积/复用型私有优势要在**原本就有故事价值**的后续事件里让读者亲眼确认“上次极限现在可以直接用”；不为证明能力新增训练、复测或工作小戏。若现成高价值目标自然要求更高极限且符合 Frozen Human 欲望，可让“成功后这个新极限也会成为自己的”参与当前选择，形成目标奖励 + 新永久极限的双重诱惑；
- 新优势、新层级或意外复合首次被他人看见时，允许 **Collective Shock / 群体震动、懂行者 Ruler Calibration、关键人物 Behavioral Repricing** 三条 Public Proof 并列成立；三者没有高低之分。主力量已有精确主尺时，三条线共用同一坐标：读者要知道主角/对手到底几级、几星、几重、差多少，以及这个超标怎样改变现场与社会价格；**Public Proof ≠ Hidden Mechanism Knowledge**：观察者只能解释自己实际看见的表现、公开主尺、伤势/器物和 World/Canon 已知事实，不能仅因高手在场就知道私有能力的永久性、隐藏触发、内部计数或因果；
- **世界强制保留一把精确、长期可复用的主力量尺**：只能采用连续数字、大境界+数字子级或数字序列等简单 Grammar，使主要修炼者始终有唯一 `Current Power Position`。突破、新强敌、公开验证或世界换挡后重新校准；精确尺是 Reader Ruler，不是战斗公式，越级胜利不自动升级。新圈层只按各自真实知道的旧名声/战绩/已公开能力先判断，再因最低充分的新事实更新待遇、敌意或合作，不默认全知也不靠降智轻视；
- **力量成长还必须有可复述的因果链**：World 冻结 Power Growth Causality（普通人怎样变强、为什么不能无限快、主要瓶颈/伤停/恢复是什么）；Power Seed 冻结 Growth Coupling（主角异常是否改变其中一环）；Story/Outline 用已有事件形成 Living Power Progression 与少量 Distance Closing；正文第一次进入力量体系时直接讲清最少充分因果，之后只补新的 delta。静态能力机制可随使用衰减解释，动态成长因果与 Ruler 不一起衰减；
- **Reader-Facing Scene Ecology**：上游人物/世界很丰富不等于读者拿得到。重要人物已有公开精确力量位置且会改变现场行为时，让力量尺成为整个社会的共同语言，不只服务主角/Rival；Story Program 已明确决定的少量具名高阶演示通过 `Reader-Facing Actor Ruler Anchors` 原样送进 Outline/Future-10，不允许自由摘要丢演员/数字/地点。复杂多方场景先建立少量稳定空间锚点，动作若持续推进则周期性直接重报当前局势；有限 POV 帮读者完成最低充分判断。重要配角只携带当前会起作用的私人压力，不倾倒 Biography；多线大碰撞遵守 `Convergence is payoff, not simultaneous loading`；
- Core Fantasy 必须反复兑现，但它是长期 **Reader Promise**，不是主角唯一的人生目的；
- 长篇需要少量**震撼式长期重释**：旧事实在后续出现意外但可回看的新解释，并立刻改变力量、身份、关系或世界格局；不强制隐藏身世或伏笔配额；
- 财富、装备、身份、关系、势力、领地、入口和资格可以很重要，但不逐渐取代主角自身成长；
- 普通小胜允许明显净收益，阶段大胜通常收益明显大于当前成本；
- 成熟不等于每次胜利立刻补等量代价、责任或审查；
- 世界可以强烈偏向核心幻想，提供强敌、宝物、秘境、战争与奇观；风险不在“世界适合主角”，而在世界所有重要对象都只能解释成下一次能力用法。

## Split Character Authority

### World Vision：世界先成立

World Vision 不知道未来主角是谁，也不知道未来金手指是什么。

它负责：

- 普通人怎样生活与上升；
- 本世界力量正常值、稀缺度与可观察差距；同时冻结一把可写出唯一精确位置的主力量尺（连续数字 / 大境界+数字子级 / 数字序列三选一），只展开当前 World Horizon 需要的可见范围；
- 宗门、王朝、家族、商盟、种族等怎样真实改变选择；
- 世界里什么真正值钱、值得争、值得羡慕；
- 即使没有主角也会推进的人物行动、战争、迁徙、争夺与灾难；这些大事优先从具体人物/生物/小群体的私人目标与下一步行动发动，机构只放大后果，不用“组织在运转”冒充世界有故事；
- 值得进入的地点、奇观、危险和未知；
- 普通人、专业人士、顶层势力各自知道什么。

World Vision 不负责主角 Biography、主角欲望、Power Asymmetry、第一次兑现或终局使命。

世界独立通过“没有主角仍有别的人正在想要、行动、互相撞上”证明，不通过完整政治经济模拟、机构任务清单或额外 Reviewer 证明。

### Power Seed：相对世界正常力量的 Power Asymmetry

Power Seed 只看 deterministic `POWER_BASELINE` 与少量 Power GBrain craft，不看 Human Biography，也不看 named Story Opportunities。

核心顺序：

`World Power Normal → Power Asymmetry → Core Fantasy → Growth Compatibility`

World Power Normal 是比较尺，不是来源限制。Power Asymmetry 可以来自世界内稀有异常、唯一奇物/际遇、外来知识/经验、外挂、极端正常天赋或少量优势叠加；不要求故事一开始就证明“合法”。默认宁强勿弱：至少一个维度让同层人明显觉得不公平，甚至提前拥有通常更高层才有的局部特权；Permanent Boundary 只防万能，不做对称成本抵消。Power Seed 只定义开局 Core Asymmetry 及其成长语法，不预先包办后续新优势；正常修炼仍必须真实增强主角本人。能力优先扩大战斗、探索、生存与行动自由，不默认职业化成维修、诊断、运输、审核或流程优化。

### Human Seed：一个人的权威快照，不是人格证明论文

Human Seed 只看 deterministic `LIFE_CONTEXT` 与 Human GBrain craft，不看 Power，也不看 named Story Opportunities。

当前结构是：

`生活事实 → 多重动机 → 冲突中的稳定选择偏向 → 具体人物关系`

核心原则：

- **经历是背景，不是人格证明**：过去先作为真实生活存在，不要求每段经历逐条证明今天的人格；
- **多重动机并存**：人物可以同时被胜负、钱、身体欲望、审美、好奇、享受、面子、亲近、自由、责任、野心、报复、归属等多股私人牵引影响，它们可以互相冲突与重新排序；
- 不再要求一个“核心执念 + 过量代价”解释整个人生；
- **稳定选择偏向 + 具体实现随现场变化**：读者逐渐知道他保护什么、拒绝什么、愿为何付代价，但具体手段由现场重新生成；
- 重要关系必须**真实改变选择**：因为是这个具体的人，路线、风险、时间、暴露或机会牺牲才发生变化；换成同等有用的人未必成立；
- 身体吸引、情欲、虚荣、争胜、自利、反复和矛盾都可以真实存在，不自动净化成理性、负责、反控制的标准优秀人格。

当前私人欲望只初始化 T0 State；Audition Hook 固定写成一次短 Action Audition：让已成立的 competing motives / 具体关系在一个非主线小现场里真正改变选择并留下小代价。它只用于作者判断候选“活起来有没有戏”，不新增过去/未来事实，也不进入 Human Core、T0 State 或永久 Canon。

### Character：deterministic composition

`CHARACTER.md` 只把冻结的 Power Core 与 Human Core 并列组合。

不新增 Character Composer 来解释“为什么这种童年注定得到这种能力”。Mismatch 是后续故事材料，不是需要消除的错误。

## Story Program：第一次完整 Collision

Story Program 是 World 与 Character 第一次同时进入一个模型上下文的阶段，也是默认使用 Sol high 的最高杠杆长期规划节点。

核心原则：

> **成长是全书纵向不变量，不是每个阶段的必填项。**

全书必须有清楚的成长与核心幻想兑现脊柱，核心幻想也必须在多个自然阶段持续兑现；但大型阶段可以主要由三种发动机中的任意一种发动：

- **人生**：私人欲望、具体关系、人生去留或旧后果；
- **幻想**：力量、战斗、获得、探索或核心玩法真正质变；
- **世界**：世界本来就在推进、即使主角不来也会发生的事件。

Collision 可以为了让当前关系、局部性格反应或某次选择更自然，补充少量**非奠基性的过去经历、共同往事或旧事件**。这些过去可以解释局部质感，但不能重写 Human Core，也不能把整个人格收束成一条创伤因果链。不要为了人格合理化自动制造悲惨童年、背叛、虐待或重大失去；普通、愉快、尴尬、失败、欲望、争执、错过同样可以有重量。**过去存在不等于现在就要告诉读者**：这类补充历史不得自动成为小说主线或大型阶段发动机，也不得一次性倾倒；Outline 只在当前故事真正需要时逐步安排读者看见其中一小部分。

三者不平均配额，也不要求每阶段各打一勾。

当前每个大型阶段只编译六个真正的故事问题：

1. 为什么现在发生；
2. 谁想要什么；
3. 主角的关键选择与行动；
4. 这一阶段真正的阅读满足；
5. Stage Delta：哪些维度真实改变；
6. 下一阶段为何自然发生。

Stage Delta 只写真实变化，不逐项填满。可包含 Power / Capability、Possession、Relationship、Identity / Access、Knowledge、Enemy State、World State 等；某项没变就不写。没有新能力、没有掉宝、甚至主角主动放弃直接成长收益，只要 Life / World 因果与永久结果成立，就是完整大型阶段。

这并不削弱男频成长。**Power Seed 决定开局 Core Asymmetry；Story Program 决定长期优势栈怎样通过故事长出来。** 开局能力的正常修炼轴、异常掌握轴、高阶质变、永久边界与传奇力量状态不能被改写；但 Story Program 可以通过真实获得加入新的 Power Asymmetry，并安排新旧优势复合。

全书成长脊柱不能只写一句“以后会变强”，也不能始终只把同一个外挂放大。长期要同时看到：开局优势深化、新的非对称优势加入、以及旧优势与新优势组合后出现单项做不到的新玩法。每次都写成具体事实：以前打不过谁、进不了哪里、做不到什么；现在具体能怎样战斗、移动、探索，或哪两项优势怎样一起产生新结果。它是全书纵向要求，不是每阶段新增能力税。**这种递归 Advantage Stack 默认是主角的长期叙事特权**；NPC / Rival 可以更高等级、拿走主角错失的东西、拥有自己的 signature asset 和专业第一，但普通重要配角不为“永远追平”而自动获得第二套同级递归 Stack，除非 Story Program 明确把极少数镜像宿敌/最终 Boss 设计成例外。

**High-Value Acquisition 不消失，只从阶段字段降级为 reader-appetite principle。** 世界自然出现真正让人想要的剑、功法、体质变化、奇物、知识、身份、同伴、洞府、飞舟、名额或其它高价值对象时，可以成为强阶段燃料；其中真正形成新 Privilege Delta 的获得可以进入 Power Asymmetry Stack，没有自然机会就不制造。**Compounding 也不消失：旧优势必须继续生效，并与新优势产生真实化学反应，而不是写完即消失。**

## Long-form Evolution：Stable Origins, Evolving Authorities

开书 World / Power / Human 是稳定 Origins，不要求一次写完 500 章所有具体世界与能力。Story Program 只具体规划当前已批准 `World Horizon`；**非终局**接近本轮世界层自然终点时输出普通 `World Horizon Handoff`，只定义可观察触发条件、`macro / instance` scope、需要继续携带的已发生事实和 orchestration，不预写下一世界给主角什么。**作者明确当前就是小说最终 Horizon 时，Handoff 第一行改为 `FINAL NOVEL END`：不再 Expansion，主角进入最终公开力量最高可见圈层，并以长期 Advantage Stack 在最后决定性事件中完成 Final Apex；Rival 可同级/活着/专业更强。未解释世界余白可以保留，但不再是 future story obligation。**

Handoff 真正触发后：

`protagonist-blind World Expansion → optional Human Development → deterministic CURRENT_CHARACTER.md → Sol Story Refresh / Re-Collision → 作者批准刷新后的 Story Program → Outline`

- **World Expansion**：Luna high，向前追加世界层；不看 Current Character / Power Stack / Human / Future Story。`macro` 只能延展 World Root 已冻结精确主尺的可见范围，不能改计数 Grammar；真正独立 `instance` 必须有自己的本地精确尺，可用章节范围承载 Local World，离开后 Local World/本地尺退场，跨世界 consequence 留在 Canon。
- **两层 Power**：Frozen Power Origin Core + `Canon → Power / Capability` 中已经真实获得/证明的 Current Power Portfolio；其中持续维护 `Current Power Position`。后期神兵、传承、新 Asymmetry 不回写 Seed，越级胜利也不能反推精确位置自动升级。
- **三层 Human**：Frozen Human Origin + Current Human State + 极低频、可为 `NONE` 的 Human Development Delta。Human Development 只看已发生历史，不看未来 World / Story。
- **Current Character**：纯确定性编译 Frozen Origins + Current Power/Human/关系/身份/知识/资产，不新增 Character Composer。
- **Story Refresh**：Sol high 首次同时看到独立生成的 Effective World 与 Current Character；惊喜来自 Collision，不允许单 Agent 先把“世界—人物—奖励”调成天生适配。
- **Outline / Review**：不得越过未执行的普通 Handoff 补满十章/百章；到触发章即停止，先完成下一轮 Expansion / Refresh。遇到 `FINAL NOVEL END` 则只编译到真正结局，不再等待下一轮 Expansion，也不制造“更强者仍在远方”的续图钩子。

长期 Mystery 采用 **Progressive Canonization**，而不是强迫作者在开书时先写终极真相。作者可以把一个真实问题保持为 `AUTHOR OPEN`，继续写已经足够具体的故事；只有作者下一步明确想写的事件已经依赖某一层答案时，系统才询问最小 `Smallest Decision`。作者可选 R1/R2/R3、继续 D0、自己改写，或继续换路线；模型不能自动替作者决定。选中的局部真相只进入 runtime-blind Mystery Control 与 Story/World planning；读者只在批准的 Reveal 章通过具体事件逐层知道，State 发生后该层才成为 Canon，更深问题重新开放。

产品因此支持一种重要作者体验：**先有一个很好看的小主意，边写边发现自己真正需要怎样的大世界；后来的决定可以重新解释旧事实，但不能否定已经明确发生的事实。** 这不是“没有大纲”，而是把确定性推迟到故事真正赚到它的时候。

World Root 被作者回头改写仍是 **Rewrite**，会按原依赖链 stale Power/Human/Character；Forward World Expansion 则不重做 Origins，只刷新受影响的未来 Story / Outline / Run。已完成章节永不因后期扩世界被回写。

## Creative Constitution → Stage-specific Compilation

TGN 仍保留 World Independence、Concrete Value、High-Value Acquisition、Net New、Irreversible State、Action Space、World Entry、Reward Opportunity、Fantasy Compounding、Expectation Ladder、Mystery Depth、Impact 等后台价值观。

它们不消失，但不再要求 Story Program 把每个后台坐标变成一个输出字段。

正确关系是：

`后台创作价值 → 当前阶段真正的故事问题 → 具体人物/行动/结果`

而不是：

`后台创作价值 → 固定表单字段 → 模型为填字段发明剧情`

## 产品级 Anti-Goals

TGN 最怕的不是局部辞藻不够漂亮，而是系统结构把不同故事压成同一种东西：

- **Ability → Job**：能力退化成探路、检测、维护、搬运、生产或运营职业；
- **Fantasy → Asset / Build / System**：库存、权限、节点和组合越来越复杂，主角本人反而不更令人向往；
- **Supporting Logic → Story Engine**：治理、工程、医疗、制度、材料处理等支撑因果抢走叙事前景；
- **Verification → Procedure**：观察、分析、测试、验证替代真实目标和冲突；
- **Character → Psychological Proof**：Biography 被写成单一人格命题的逐条论证；
- **Character → Tool**：配角只发任务、给资源、被救或做能力 Counter；
- **Core Fantasy → Life Purpose**：主角后半生只剩继续找适合能力的对象；
- **Story Program → Upgrade Tax**：每个大型阶段都被强迫交一次能力参与、升级、奖励和净新增；
- **Plot Engine Repetition**：接任务 → 进危险地点 → 打竞争者 → 拿资源 → 升级 → 更大地图；
- **Payoff → Tax**：每次胜利自动补等量代价、责任或审查；
- **System → Story**：Agent、Gate、Context、数据库和参考库越来越复杂，LLM 开始维护系统而不是写小说。

这些是方向性 Anti-Goals，不是逐项 Hard Gate。发现问题时修最早语义坍缩点，不为每一个症状再新增 Reviewer。

## 支撑性逻辑边界

统一准则：

> **支撑性逻辑不得自动成为故事发动机**

- 世界复杂度 ≠ 叙事焦点；
- 对手有理由 ≠ 作品认同 ≠ 主角有义务；
- 机制真实存在 ≠ 必须展开实施细节；
- 能力 ≠ 职业；
- 可以验证 ≠ 验证过程就是故事。

内部因果必须可信，但只展开会改变人物选择、风险、胜负、关系或结果的部分。普通实施过程默认压缩。

## Growth Genome / Outline 的位置

BOOK 中保留 `## 0. 本书成长基因图` 主要为了兼容现有 BOOK / Chapter Runtime，但它现在是**已批准上游的短投影**，不是第二个故事设计器：

- 压缩已批准幻想不变量；
- 复述 Story Program 已经安排的长期 Power / Capability 真实质变，不新增数量要求或升级节点；
- 记录会跨阶段继续生效的重要获得、关系、身份、知识或世界后果；
- 保留少量核心不变量与真实退化风险。

Outline 的职责是把 Story Program 编译成当前窗口的具体 Story Anchors。每个剧情块使用 `Block Delta`，只记录相对本块开始真实改变的 Power/Capability、Possession、Relationship、Identity/Access、Knowledge、Enemy State、World State；没有变化的维度直接省略。**Growth is longitudinal, not a per-block or ten-chapter tax.** Outline 不重新规划 Story Program，也不为了填表补微升级、小奖励、新权限或新地图。

## Chapter Runtime

章节默认链：

`Approved Future-10 → Full Deterministic 4—6章 Authority Packet（默认5）→ Terra high Batch Primary → Sol high Batch Authority Delta → 整批采用 → Luna low State逐章落盘`

- Batch Packet：代码原样抽取当前 Future-10 逐章条目，不让第二个规划 LLM 改写已批准 Event / Result / Ending；同时复用现有 Chapter Context compiler 叠加 Frozen Power/Human、safe World、Reader Release、Protected RSE、Book Contract、BOOK Prose Profile、starting Canon；
- Batch Primary：一次连续写完整窗口，保留章间 Handoff、人物声音、物件/地形复用和短中程铺垫回收；
- Batch Authority Delta：一次看完整 Batch 与 safe Effective World / Frozen Power+Human / Reader Release / Story/Outline/Canon，只做 exact local patch；同一事实域跨章扫清，无法不新增机制地修复时返回 `upstream_conflicts`，整批不采用；
- State：等整批正文 final 后按章顺序记录已经发生的事实，并持续维护 `Current Power Position`；没有明确突破时沿用原位置，不能由越级表现推断升级。

旧 `Luna Director → Luna Curator → Terra Primary → Luna Full Reviser → State` 保留为单章 fallback / 专项实验，不再是默认正文拓扑。Scene Skill v2 的 Curator `Scene Prose Projection` 与短 Revision Watch 也暂时只在这条 fallback / 专项修订中使用；默认 Batch 未经单独 A/B 不增加 Batch Curator。

章节 Runtime 不直接读取 raw GBrain，也不重新决定 World / Power / Human / Story Program。

## Author Workspace / AgentDock

网页是阅读优先的本地创作舱：浮动项目栏、hash 工作区、窄导航 rail，以及桌面常驻/小屏覆盖的 AgentDock 面板。Light / Dark 是独立设计层级，正文优先 Serif 阅读，卡片使用 22—28px 圆角、细边框、低饱和玻璃层和极轻阴影。Workflow State 与 Run Ledger 仍是正式 artifact 状态的唯一来源；AgentDock / Batch 执行状态独立显示，不伪装成已保存节点，也不另造内容真源。

`agentdock_acp` 是本机、内存作业型 Response executor：后端从可信安装锚点解析 `codex-acp` 的 JS 入口并由 `node.exe` 直接承载 UTF-8 NDJSON，固定 TGN 项目 cwd、空 MCP 与 `read-only` mode；不再通过 PowerShell wrapper 转发协议流。`fs/read_text_file` 只允许项目根内 UTF-8 文件；只读命令的 `execute` permission 可单次通过，但仍受 read-only sandbox 约束，`edit` / file-write / permission escalation 继续拒绝。短控制 RPC 与长生成 job 使用不同 deadline，stdout/stderr 持续 drain，pending job queue、ACP stdout event queue、activity、output、error 与 completed history 全部有界；高频 update 通过有界 FIFO 反压，不丢 RPC response / callback。它可以读取项目上下文，但不能保存、采用、批准或写 Authority artifact；status 只说明 ACP 入口是否存在，ChatGPT 登录在真实启动时确认。自动回填必须同时匹配 book / chapter / workflow mode / Batch window / latest launch、精确 Prompt / 上游输入快照，并确认作者未改动目标编辑区；刷新恢复、错位、旧 launch 或丢失作业只允许只读查看。

长任务 UI 不显示虚假百分比或 ETA，而持续显示真实阶段、累计耗时、距最近信号时长、通用 plan / tool / activity 摘要、取消入口和低打扰定时提醒。ACP commentary、private reasoning、原始命令、路径与凭据都不进入作者可见 activity；最终 Response 只接收明确 final channel。短暂列表 / 状态查询失败保留 pending lock 并退避重试，不能因此允许重复启动。

Author Workspace 桌面布局为窄 nav rail → 真实 Story Structure tree → 中央 manuscript surface → 固定 AgentDock。Structure tree 的 World/Character/Story/Long Plan/Future-10/当前章/Canon/Run 均从 Workflow artifacts 和已解析 Future-10 生成，点击定位真实工作区。顶部 Manuscript、Structure、Memory 切换真实 view；Audit 与 Versions 打开右侧真实区域。Batch Production 复用既有 Batch API，并确定性补齐任意起始章的连续性上下文，完成 Packet → Terra high Primary → Sol high Delta → exact-window/exact-response 预检 → 作者显式 Adopt → 作者逐章 State；窗口或 Response 变化会使下游 Prompt / 预检失效，不复制 Authority 算法。

GBrain 在 Workspace 中使用 Curator 交互：semantic retrieval / full-page extraction 后分别展示 fixed references 与 BOOK-compatible candidates；每轮默认不选，作者可按 Human 三 lane 浏览、显式勾选、并排比较、组装可编辑 Bundle，或明确本轮不注入。请求返回、Bundle 与 Prompt 都绑定发起时上下文；上下文变化后旧材料只读保留并标 stale，selection stale / 未绑定手工文本 / GBrain-OFF 阶段由前后端共同 fail-closed。GBrain 仍只提供 Optional Inspiration，不写 Canon，也不成为 Hard Gate。

## GBrain 与模型默认路由

当前默认：

- World Vision：GPT-5.6 Luna high，GBrain ON，固定 1 条 Reader Coordinates Reference + 最多 3 条 focused creative inspiration；固定坐标参考不占 creative 名额；
- World Expansion：GPT-5.6 Luna high，World-only GBrain + Coordinate Reference；低频、protagonist-blind；
- Power Seed：GPT-5.6 Luna high，Power lane GBrain，小 bundle；
- Human Seed：GPT-5.6 Luna high，Human lane GBrain，Appetite / Behavior / Relationship 各最多 1 条，总计最多 3 条；
- Human Development：GPT-5.6 Luna high，GBrain OFF，可选慢时钟；
- Current Character：deterministic，GBrain OFF；
- Mystery Decision / Reframe：GPT-5.6 Luna high，GBrain OFF，低频且 author-gated；
- Mystery Compiler：GPT-5.6 Terra high，GBrain OFF，只审局部兼容与 Still-Open；
- Story Program：GPT-5.6 Sol high，GBrain ON，最多 3 条 focused inspiration；
- Story Refresh：GPT-5.6 Sol high，GBrain ON，最多 3 条 focused inspiration；必要时 planning-only 编译 reader-facing Mystery Reveal Contract；
- Outline：GPT-5.6 Luna high，GBrain ON，通常 4 条、最多 5 条；
- Batch Packet：deterministic，直接抽取 Approved Future-10，默认5章、支持4—6章，并复用现有 Chapter Context compiler 前置完整安全 Authority；
- Batch Primary Writer：Terra high；
- Batch Authority Delta：Sol high；
- State Extraction：Luna low；
- 单章 Director / Curator / Full Reviser：Luna high，仅 fallback / 专项实验。

模型选择看三个坐标：**生成质量 ≠ wall-clock ≠ 实际成本**。Sol 仍只放高杠杆节点：Story Program / Refresh 与跨章 Authority Delta；Max / Ultra 只有真实 closure 优于 high 时才采用，不按档位名称自动升级。

GBrain 详细边界见 `docs/GBRAIN_STORY_CRAFT_V3.md`。

## Review 与章节边界

十章 Review 只调整未来，不修改已经完成的正文。它可以发现核心幻想退化、Plot Engine 重复、人物工具化或世界程序化，但不自动创建新的上游事实。

ChapterContextPacket、Canon Memory、State Delta、Run Ledger 与章节保存边界保持当前 Runtime 事实。

## Experiment Boundary

`books/real-exp-*` 下的世界、人物、能力、审计、模型选择与实验输出只用于验证系统假设；模型选择不等于作者批准，实验角色也不自动进入产品默认。

只有当问题跨新书稳定复现、且能定位到最早语义节点时，才改 production。一次样本的局部怪异不值得长出新的 Prompt 规则、Agent 或 Gate。
