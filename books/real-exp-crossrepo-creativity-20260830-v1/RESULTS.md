# Cross-Repo Creativity Lift｜Final Results

日期：2026-08-30  
状态：**World/Human PASS；Premise Quarry PARTIAL / NOT DEFAULT PRODUCTION**

## 目标

从其它长篇小说系统中只抽取“怎样扩大创意搜索、怎样让世界自己长故事、怎样让人物在候选阶段活起来”的方法，不复制实现、角色、设定、文句，也不因多 Agent / RAG / Knowledge Graph 本身显得先进就引入新架构。

本轮抽象了四个外部方法：

1. 正式 architecture 前允许 source / research / craft 刺激，但刺激本身 Non-Canon；
2. Scan → deconstruct → recombine，只迁移情绪与功能，不迁移来源外壳；
3. 角色/世界主体像独立 Player 一样先有自己的目标与动作；
4. 用具体物件、痕迹、身体状态和地点承载反复变化的故事含义，而不是只靠解释。

最终没有把四点混成一个新 Agent，而是拆成三个可归因实验。

---

## Phase A｜Creative Quarry → Premise Forge

### Treatment

在现有 production Premise Forge 前增加一个独立、可丢弃的 `Creative Quarry`：只产出 Concrete Substrate、Appetite Pressure、Living Actor Engine、Recurring Carrier 和 Collision Invitation，不写完整 premise，不写 Power/Human/终局。Forge 每张卡最多借一个具体 substrate + 一个 actor/carrier，也可以全部不用。

### 三题结果

| Author Direction | Blind creative verdict | Control Compiler | Quarry Compiler | 判断 |
|---|---|---:|---:|---|
| generic_fantasy | **Quarry 赢** | 1 Conditional / 2 Fail | 2 Conditional / 1 Fail | 正向 |
| fast_multiworld | **Control 赢** | 2 Conditional / 1 Fail | 1 Conditional / 2 Fail | 反向 |
| game_instance | **Quarry 赢** | 3 Fail | 3 Fail | 创意正向、可编译性无增益 |

### 真正看到的增益

Generic treatment 出现：

- **《伤口里的刺客》**：主角住在伤口里；开放伤口就是路；敌人打伤同伴等于替主角铺路。它改变治疗、集火、撤退、追杀等基础动作，而不是只换能源名。
- **《披身者》**：主角没有身体，只能进入刚刚脱离主人的外皮；身体像战术装备一样被抢夺和更换。

Game-instance treatment 出现：

- **《死者最后一步》**：由尸体最后动作孵出的行动残骸，偷走死者最后一个动作；“溺死船夫最后一次抛绳”可以被主角拿来把自己拉过断桥。
- **《看见我，给我一条路》**：只有被看见才能落地的影子，目光本身成为移动资源与社会地形。
- **《一张会走路的嘴》**：没有身体的嘴，只能贴在真实边界上，通过吞掉墙、门、牢笼的一段咬出通路。

### 真实退化

Fast-multiworld treatment 三张虽然单独都不差，却收敛成：

- 活影沿阴影移动；
- 活声音沿震动移动；
- 活伤口沿固体裂口移动。

三个候选都变成“非人媒介穿行”的材质变体。Control 反而给出死亡动作继承、会走路的吞城门、公共见证/影子等明显更宽的动作空间。

### Verdict

**PARTIAL / NOT DEFAULT PRODUCTION。**

Quarry 可以扩大某些题目的素材距离，但它也会把一个特别鲜明的 substrate 家族放大到整个候选池。2/3 创意胜出不足以抵消 1/3 明显候选同质化，而且 Compiler 没有稳定改善。

因此：

- 不新增 production `Creative Quarry` stage；
- 不把 GBrain/raw research 直接接到 Premise Forge；
- Quarry 可保留为未来作者显式请求的 **optional inspiration board / research tool**；
- 它产出的 concrete substrate / recurring carrier 更适合 World / Scene / Story material，而不适合作为每本书必经的 book-premise 前置层。

这也是本轮最重要的负结论：**不同外部创意方法应该落到它最擅长的创作层，不能用一个 Inspiration Agent 从 Premise 一路管到正文。**

---

## Phase B｜Living Actor World

### Treatment

不新增字段、不新增 Agent，只改变现有 `## 世界正在发生的大事` 的生成问题：

> 谁现在私人地想要什么 → 下一步已经准备做什么可见动作 → 即使没有主角，这会真实改变谁/哪件东西/哪个地方？

机构、战争、市场和资源格局只负责放大后果；至少一些大事允许被钱、赢、爱、嫉妒、占有、好奇、报复、舍不得、证明自己等私人欲望发动。多线碰撞优先来自争同一个具体人/物/地点、抢先抵达、带走/毁掉某物或互相追杀。

### Control

同一 Author Direction / 同一 World GBrain 的 Control 世界，大事主要是：

- 军府重新封锁和开发矿井；
- 商盟办铸器大赛并争矿；
- 部族南迁并与王朝谈冬牧地；
- 修院探遗址确认高阶记录；
- 擂台强者以连胜换独立守权。

世界完整、可持续，但故事发动机明显容易滑向机构任务与资源协调。

### Treatment

同一世界职责下，大事变为：

- 少东家**罗挽舟**想在继承前证明自己，带三十辆热车去黑熔谷抢唯一完整日骨，想先拿到一条只属于自己的货路；
- 女校尉**齐闻雪**的弟弟被扣，她违令带六名旧部追商队，宁愿毁掉自己军中位置也要先把人抢回来；
- 猎首**阿娑**只想救回被抓走的三个孩子，带二十名夜行猎手准备在裂原下手；
- 铸师**庄伏火**要公开击败把自己逐出门墙的师父，正在炼一把可能先烧伤自己的短刃；
- 火鳞兽群自己追着地下热流南迁，踩坏暖井、逼走村镇，不服务任何人。

力量尺、普通生活、价值物、知识边界没有被削弱，但世界从“组织在运转”变成“人和生物已经要动手”。

### Blind review

- Terra high：**A / Treatment**，Method Gain = YES。
- Luna high：**A / Treatment**，Method Gain = YES。

两者都指出：Control 的世界事实没错，退化点在“开发—竞矿—探遗址—谈判”成为默认发动机；Treatment 用私人行动让多线在同一地点/资源/时间窗自然咬合。

### Verdict

**PASS → production prompt-only。**

最小冻结原则：

> **World Independence = Living Actors, not institutional activity.**

不是要求所有冲突都是私人恩怨，也不要求所有角色聚到同一舞台。制度、生态、战争仍然重要；只是“它们存在”不能替代“有人现在正在因为自己的欲望做事”。

Production 成本：**0 个新增 LLM 调用；0 个新增 schema；0 个新增 gate。**

---

## Phase C｜Human Action Audition

### Treatment

仍使用现有 `Audition Metadata（非 Canon） / 人物钩子`，但把一句人格宣传语改成 100—180 字左右的小型 Action Audition：

- 不属于未来主线；
- 不知道未来 Power；
- 只使用候选已经成立的生活事实、competing motives 与关系；
- 至少两项私人价值不能同时完整满足；
- 人物必须做一个可见选择；
- 留下一个真实的小机会成本、得罪、暴露欲望或即时后果；
- 不解释“这说明他是怎样的人”；
- audition 全部 Non-Canon，作者选择后仍由现有 parser 从 Human Core / Initial State 剥离。

### Control 与 Treatment 的差别

Control Hook 常是：

> “他可能为了赢一场无关紧要的比赛多押一把，也可能为了弟弟复诊让掉一份远途活。”

它复述了人设，却没有新增行为证据。

Treatment 出现：

- **陆炽**刚赢赌局，钱本来够买自己惦记的烤肉；看见母亲搬腌菜，他改买了母亲念叨半年的酸酒，自己饿着，却回家路上偷喝两口。
- **顾野**本来最看重快钱和坐骑；猎队给加价时，童年朋友正等他取回一个丢失的箱子。他把马借给猎队，自己跑去找箱，丢了工钱也磨破鞋，见面第一句却先问箱子有没有坏。
- **许闻**有一块漂亮门骨：全卖能付弟弟学费，全留能做自己的第一件作品。他把材料劈成两半，卖掉规整的一半，把带裂纹的一半做成歪挂饰送弟弟，还故意没把裂纹磨掉。

这些场面不是 Canon；价值在于作者终于能判断“这些动机和关系放进现场后，这个人到底会不会做出有戏的选择”。

### Blind review

- Terra high：**A / Treatment**，Method Gain = PARTIAL（明确认为新增了行为诊断能力；风险是一次 audition 被误当人格算法）。
- Luna high：**A / Treatment**，Method Gain = YES。

两者都确认没有偷塞未来 Power / 命运 / 主线 Canon。

### Verdict

**PASS → production prompt/schema wording only。**

冻结原则：

> **A Human candidate should be auditioned through a costly choice, not summarized through another personality sentence.**

Production 成本：**0 个新增 LLM 调用；0 个新增 Authority；现有 parser 保持 Audition Non-Canon。**

---

## Cross-sample Freeze Validation

第一轮 World / Human 各自只有一个生成样本，按项目规则不足以直接升级为 production。Treatment 冻结后又换了第二组输入做 cross-sample 复验；没有修改 Treatment 再看结果。

### World 复验

第二个 World 的 Control 仍能生成完整世界，但大事主要是盐路战争、宗门进遗迹、商盟捕猎、学院测河道、王朝武会与兽群南迁。Treatment 则生成：

- 外门弟子阮秋棠要夺回被取消的传承资格，已经准备独闯落耳墟；
- 商队首领裴万川要救逐渐失聪的女儿并摆脱债务，已经雇队抢先去无声井取白噤水；
- 风背族族母鸦岚要把幼崽送回祖崖完成第一次滑翔，准备强穿军府封锁山口；
- 校尉苏烈为弟弟复仇，已经调猎队准备烧毁兽巢；
- 受伤黑喉母兽只想带幼兽避过鸣暴，已经撞破采石镇并进入地下道。

这些行动随后因落耳墟、无声井、地下空腔和兽群迁徙自然咬合，并继续改变药价、商路、边境政策、聚落安全与生态。

Blind：

- Terra high：Treatment，`Method Gain = YES`，`Overcorrection = NO`；
- Luna high：Treatment，`Method Gain = YES`；提醒私人动机密度略高，但同时确认宏观制度/生态后果仍完整，没有缩成私人恩怨。

两轮合计：**World Treatment 4/4 blind votes**。

### Human 复验

第二个 Human 样本仍然不是把人物统一写成关系牺牲者：

- 贺临川为了当众赢与被看见，押掉原本给妹妹买鞋的钱，赢了却错过鞋铺；
- 裴照为了眼前的亲密与味觉停留而错车，还因为擅自藏布惹关系对象真正生气；
- 鲁闻因为父亲一句“卖了就卖了”突然不卖旧皮甲，反而把路费押到一枚旧护栏扣上；
- 唐越明知关系对象在等，仍然留下听完新奇声音，结果被当众拆穿、关系对象离开、两张影戏票也失效。

Blind：

- Terra high：Treatment，`Method Gain = YES`，`Overcorrection = NO`；
- Luna high：Treatment，`Method Gain = PARTIAL`；提醒四个 audition 都较容易出现“眼前刺激压过原承诺”的形状，但确认它们没有未来 Power / 主线 / Biography 泄漏，也没有道德化收敛。

两轮合计：**Human Treatment 4/4 blind votes**。

这个复验没有授权新增“必须冲动 / 必须为关系付代价”的规则。相反，production Prompt 已明确：Action Audition 只检验一次选择，不得固化成固定人格算法；World 也只要求至少若干 Living Actor，大尺度制度、生态与自然过程仍可独立发动。

因此最终冻结状态为：

- Living Actor World：**PASS / FROZEN production prompt principle**；
- Human Action Audition：**PASS / FROZEN production non-Canon audition principle**；
- Creative Quarry：继续 **PARTIAL / research-only / optional author inspiration**。

Steward 随后升级为 `tgn-system-steward 0.3.30`，保留并行任务已经冻结的 Exact-Input Receipt 审计方法，同时加入 `Institutional Activity ≠ Living World` 与 `Human candidate needs Action Evidence`。`skill-authoring` lint 为 0 error / 0 warning，package validate、install、activate 均 PASS。安装后又用一个已知 World 反例做 bounded read-only ACP smoke：Steward 正确把最早问题定位到 World 生成层，要求具体主体欲望 + 下一步动作 + 无主角后果，并明确拒绝新增 Agent / Reviewer / Gate / Actor table，smoke PASS。证据见 `steward_smoke/`。

## 最终决策

进入 production：

1. `World Vision / 世界正在发生的大事`：Living Actor generation principle。
2. `Human Seed / Audition Metadata`：Action Audition。

不进入默认 production：

1. Creative Quarry 作为 Premise 前置常驻阶段。
2. raw GBrain / benchmark research 直接进入 Premise Forge。
3. MARP 式角色 Agent 讨论会。
4. novel-studio 式额外 Brainstorm Agent 作为必须阶段。
5. oh-story 式 trope 模板直接决定世界/人物/剧情。

### 为什么

其它项目真正有价值的不是“多 Agent / LangGraph / RAG / Knowledge Graph”，而是它们背后的几个创作动作：**先拆素材、让角色自主行动、让具体事物承载变化、让候选经现场检验。** TGN 只有在这些动作可以嵌入现有 Authority 架构、并且不增加新的自洽闭环时才吸收。

本轮最终采用的两刀都满足：**生成质量提高，但创意 authority、模型路由、批准点和每章成本不变。**
