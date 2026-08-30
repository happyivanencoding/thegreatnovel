# Story MVP 分层方法论与价值观

> 项目执行规则的唯一长期权威是根目录 `PROJECT_RULES.md`。本文只解释系统为什么这样分层、每层负责什么创造性责任、问题应在哪一层修，以及哪些方向明确不希望退化成。

## 1. 一句话理解整个系统

Story MVP 不是“让一个大模型从设定一路写到正文”的流水线，而是把不同尺度的创作问题拆开，让每一层只解决自己最擅长的问题：

`Independent World → Split Power / Human Authority → Character Collision → Long-Form Causality → Story Anchors → Chapter Execution → Forward Evolution`

对应实际链路：

`作者方向 →（可选）Non-Canon Premise Forge S1/S2/S3 → Independent Premise Authority Compiler → 作者批准 / 显式跳过 → protagonist-blind World Vision → POWER_BASELINE / LIFE_CONTEXT → 独立 Power Seed + Human Seed → deterministic Character → Story Program / Collision → Outline → Director → Curator → Primary Writer → Authority Reviser → State Extraction`

Premise Aperture 已冻结为可跳过的 production 开书阶段，但不是第四 Authority。Forge 一次形成三张完整货架候选；Compiler 只审 trigger、载体、T0 尺位、Interface 因果与远期复合，不评分、不选择、不修稿。作者批准后，代码确定性拆出 World / Power / Human / Story 四条 lane contract；Story Program 第一次读取完整 Promise，Outline 与章节不再读取 raw card。该阶段从未开始或显式跳过时，原 Split Authority 路径保持可用；一旦开始，必须 strict PASS + 作者批准后才能继续。完整合同见 `docs/PREMISE_APERTURE.md`。

长篇不是把这条开书链一次跑完后消费 500 章。当前 World Horizon 被故事真正活透时，进入低频的向前循环：

`Story Program 的 World Horizon Handoff → protagonist-blind World Expansion →（只有长期证据足够时）Human Development → deterministic Current Character → Sol Story Refresh / Re-Collision → 作者批准 Story Program → Outline → 后续章节`

这里的核心是 **Stable Origins, Evolving Authorities**：开书 World / Power / Human Origin 不因后期增长被重写；新世界、新能力、人物发展和长期状态只向未来追加。World Expansion 与 Human Development 使用隔离上下文，只有 Story Refresh 第一次同时看到新 World 与 Current Character，避免单一 Agent 把“下一世界—主角现有 Build—未来奖励”预先自洽成一套钥匙孔。

其中最重要的原则是：**越靠上游，越决定“这本书是什么”；越靠下游，越只负责忠实执行已经确定的故事。**

如果下游正文出现系统性偏差，优先检查最早发生语义坍缩的上游层，不要默认继续给 Writer 增加规则。

### 系统问题必须在“生成事实的最早层”解决

判断一个修复是不是系统修复，先问：**换一本完全不同的新书，这个问题还会不会重新出现？** 如果会，就不能靠某本书的 BOOK 补字段、某一章 Director 临时发明设定、Curator 改词或 Writer 兜底。应找到最早应该产生该事实的层，并在那里建立通用职责。下游可以忠实释放、选择、压缩和表达上游事实，但不能为了救当前样本创造本来应该由上游决定的世界规则。

例如：读者不知道谁强、晋升到底得到什么、核心金手指遇到高层对象会不会直接越级，这不是 Chapter 4 的局部问题，而是 World Vision 没有给下游足够的 Reader-Facing World Model；连续几章用同一能力、同一对手、同一反转，则优先是 Story Program / Outline 的玩法变异问题。修复目标不是“让这本实验书下一章正常”，而是“下一本新书从零生成时自然不会再掉进同一个坑”。

### 显式系统审计

系统审计不是小说 production 节点。用户明确要求“审计”时，使用当前激活的 `tgn-system-steward` 做独立审计，同时由当前 ChatGPT 复核 live code / docs / artifact，再合并结论。审计区分 **Stable Principle / Current Default / Experimental Hypothesis**，优先找最早语义坍缩点；默认不因此新增常驻 Reviewer、Scorer 或 Hard Gate。具体触发与 Skill 更新规则以 `PROJECT_RULES.md` 为准。

---

## 2. 核心价值观

### 2.1 Fantasy First

Fantasy First 是读者价值优先级，不再是 production 阶段。系统仍先保护“读者最想亲自拥有什么、主角本人怎样真正变强”的承诺，但创意 authority 由 protagonist-blind World、Power Seed 与 Human Seed 分拆承担，避免一个 Seed 同时预先决定世界、能力、Biography 与人生意义。

成熟男频成长长篇的一级主轴优先是：主角本人越来越能做什么、拥有怎样的力量、自由、生命状态、世界位置或命运主动权。

财富、装备、身份、关系、势力、领地、入口、资格等可以重要，但它们默认是承载和结算，不应逐步取代核心幻想；同样，核心幻想本身也不能反过来吞掉主角的人生，把所有长期欲望都变成“继续升级这项能力”。

### 2.2 Agency First

金手指的价值不只是“提高完成任务的效率”，而是让主角获得别人没有的行动可能性。

健康方向：

- 别人进不去，他能进去；
- 别人必须服从的规则，他有额外选择；
- 别人无法争夺的目标，他能主动介入；
- 过去只能被安排，现在可以选择战场、目标、合作与拒绝。

危险方向：

- 同一工作做得更快、更稳、更精准；
- 路线更多、节点更多、权限更多；
- 能力逐渐退化成职业技能、Build、工作流或资产管理系统。

### 2.3 Relationship Reconfiguration

优秀设定经常会改变默认博弈关系，而不仅仅改变战斗数值。

核心问题不是“人物关系一定要很多”，而是：**当主角获得新的非对称能力后，原本谁能命令谁、忽略谁、利用谁、封锁谁、定价谁、依赖谁，这些默认关系是否还成立？**

例如“看见别人看不见的路”真正重要的长期价值，不是主角更擅长找路，而是：

- 宗门过去靠唯一入口控制主角，现在单纯守门失效；
- 商人过去可以把主角当探路工具，现在必须争夺主角本人；
- 原本只能依附宗门的人，现在拥有另一种选择；
- 敌人过去只需要堵路，现在必须控制主角、攻击关系或改变战略。

关系重构不是万能定律，也不是 Hard Gate。**Character Autonomy ≠ Symmetric Stakeholder Power，Relationship Reconfiguration ≠ Permanent Renegotiation**：配角自治只要求人物有自己的欲望并据此行动，不要求每个人都保持平等议价、拒绝追随或永远只按条件合作。人物可以因为自己的欲望真心崇拜、爱慕、投靠、拜师、效忠、屈服、背叛、竞争或成为死敌。探索、战斗、谜团、生存和世界奇观都可以是主发动机；关系变化服务故事，不把所有关系写成 stakeholder negotiation。

### 2.4 Narrative Compounding > Asset Compounding

“复利”首先指故事不会回到原点，而不是资产种类越来越多。

优先看：

- 主角下一轮多能做什么；
- 对手以后必须怎样改变应对；
- 重要关系出现什么新的选择；
- 身份和世界位置发生什么不可回滚变化；
- 下一轮因此出现什么过去根本不会发生的冲突。

能力、装备、资源、关系、身份、领地等可以承载复利，但不要为了证明成长主动堆成路线网、权限树、库存、节点网络或组合系统。

### 2.5 Backstage Principles Must Not Become Generated Ontology

TGN 会保留一组区别于模板化小说生成器的后台创作原则与读者体验坐标：World Independence、Concrete Value、High-Value Acquisition、Net New、Irreversible State、Action Space、World Entry、Reward Opportunity、Fantasy Compounding、资源反哺，以及 Expectation Ladder、Mystery Depth、Impact 等。它们非常重要，负责判断长篇是否真的在积累、换挡、制造期待、保留纵深并扩大未来故事可能性；**但它们属于 Author Model / Creative Constitution，不是小说世界里的自然名词、资源、势力理念或终极主题。**

Reader Coordinates 因此分成两类：

- **世界前台尺**：Power / Technique / Threat / Status / Value / World，必要时 Gear / Potential；它们可以被世界内名称、境界、身份、装备和价值体系直接承载。至少一把当前主尺应长期复用，并在突破、新强敌、公开验证或世界换挡时重新校准，而不是开篇介绍一次就消失。
- **读者体验 / 故事尺**：Action Space / Expectation Ladder / Mystery Depth / Impact，必要时 Reach；它们必须真实参与生成，但要投影成具体故事事实，而不是变成世界内部术语。

正确方向是“抽象价值观 → 阶段专属的具体创作问题”，而不是“抽象价值观 → 世界 ontology”：

- World Independence 编译成：**没有主角时，谁正在追什么，哪里正在发生什么值得看的事？** 它证明世界还有别的故事，不要求建立完整利益社会；
- Concrete Value / Reward Opportunity 编译成：**这里什么东西真的值钱、值得人物去争？**
- Net New / Irreversible State / Action Space 编译成 Stage Delta：**这一阶段到底有哪些维度真实改变，哪些东西从此不能回到原状？** Power / Capability、Possession、Relationship、Identity / Access、Knowledge、Enemy State、World State 只写实际变化的部分；不为后台坐标制造剧情。
- Fantasy Compounding 编译成纵向持续性：**过去已经得到的力量、物件、关系、身份、知识或入口，是否继续改变今天的行动、选择、敌人应对与世界局面？** 它不是每阶段必填字段。
- Expectation Ladder 编译成：**下一层有哪些已经看得见、尚未拿到，但读者会想要/想看的具体人、物、地点、能力、身份或奇观？**
- Mystery Depth 编译成：**哪个已经出现的旧物、旧人、旧事实或旧异常还保留可回收的更深解释，并会触发未来行动？**
- **震撼式长期重释**：高价值回收不是“终于解释了”，而是让读者当下意外、回看前文又觉得证据早已存在，并使旧事实立刻获得更大的力量、身份、关系或世界含义。来源可以是能力、人物、关系、旧事件、宝物或世界联系，不默认等于隐藏身世，也不按阶段配额出现。
- Impact 编译成：**这次行动实际改变了多少人物、关系、地点、阵营或世界事实？**
- World Entry 编译成：**人物因什么具体事件去到新的地方/圈层，那里新增什么值得想要或害怕的东西？**

因此可以在规划与评估中继续使用 Action Space、Expectation、Mystery、Impact、Net New 等术语，但生成世界和阶段主线时先产出人物、物品、功法、资源、地点、关系和事件，再由后台判断这些原则是否成立。**Backstage principles should constrain generation, not become generated ontology.**

同时必须区分：**核心幻想是长期读者承诺，不是主角的人生使命。** TGN 的长期故事不再默认由单一幻想发动机驱动，而是允许**人生发动机 / 幻想发动机 / 世界发动机**编织：人物人生欲望与未完成关系、核心幻想与力量获得、世界本来就在发生的大事都可以成为大型阶段的主要发动来源。三者不要求平均配额，也不新增打标签的字段；重要的是能力持续活着，但不自动决定整个人生。

同时遵守 **Narrative Appetite Before Defensive Balance**：先保护最让人眼馋、兴奋、好奇、痛快、恼火或非看不可的东西，再补维持长篇所需的最小边界。World 负责世界事实，Power 负责力量幻想，Human 负责人本身；Story Program 再处理它们碰撞后的长期变异、后果与复利。允许局部明显过量、偏心、不均衡，只要这种“放纵”真正增加本书的独占性阅读欲望，而不是把合理性检查做完以后才看还剩多少爽点。

### 2.6 支撑性逻辑不得自动成为故事发动机

这是当前系统非常重要的一条统一准则。它把过去分别表现为“治理化、工程化、蓝领职业化、过度验证”的问题归到同一个根因：**LLM 看见一个合理问题以后，容易把“让因果成立”继续推演成“把这个问题完整解决”，最后让支撑性逻辑反客为主。**

必须持续区分：

- **世界复杂度 ≠ 叙事焦点**：世界可以复杂，某种风险或制度理由可以真实存在，但不自动成为作品主要讨论对象。
- **世界独立 ≠ 所有真实事物拥有同等叙事权重**：世界独立只要求没有主角仍有别的故事在发生，不要求税、土地、治理、迁徙、制度和每个利益方都获得同等篇幅；核心幻想、主角人生牵引和当前最馋人的故事对象决定前景权重。世界可以强烈偏向核心幻想并大量提供适合其发挥的强敌、宝物、遗迹与奇观；只要世界不被核心能力完全解释、重要人物不只作为下一次能力关卡存在。
- **人物自主 ≠ 每个人都必须拥有对称议价权**：人物有自己的欲望，不等于每个人都必须维持平等议价或拒绝追随；效忠、崇拜、爱慕、投靠、屈服、背叛和死敌都可以是自主选择。
- **对手有理由 ≠ 作品认同 ≠ 主角有义务**：对手可以有真实理由，甚至局部是对的；这首先用于制造冲突，不因为主角力量变大就自动推出“主角有义务管理所有人”。
- **机制真实存在 ≠ 必须展开实施细节**：阵法、地形、规则、制作、技术过程可以存在，但只展开足以支撑当前人物选择和结果的部分。
- **能力 ≠ 职业**：能力可以重复使用，但长期成长优先扩大主动权、敌人策略、关系、身份、机缘和世界入口，不自然职业化成探路、检测、维护、运输、生产或运营工作。
- **可以验证 ≠ 验证过程就是故事**：能力可信性优先嵌入有真实目标和利害关系的行动中证明，不单独搭建测试场景穷举机制与限制。

因此，“具体”优先具体在：谁想得到什么、谁阻止、主角决定什么、核心优势怎样改变局势、谁因此得到或失去什么、什么从此不可回滚。观察、分析、测试、验证、调整、实施如果没有新的关键选择、冲突或反转，就压缩到足以支撑因果的最小程度。

这条准则不是禁词表，也不禁止工程、经营、治理、研究等题材；如果作者明确选择这些题材，它们可以成为主发动机。关键是 **supporting logic 只有在本书真的把它选为主要阅读体验时，才升级为 story engine。**

### 2.7 Few Deep Rules > Many Hard Gates

旧系统的重要失败之一，是规则过多以后 LLM 开始优先维护 Schema 和门禁，而不是写故事。

因此默认策略是：

- 不为每个质量问题增加 Agent；
- 不为每个原则增加 scorer；
- 不把软创作方向改成逐项验收；
- 能用一条更深的原则修上游语义，就不要在下游叠更多补丁。

---

## 3. 每一层到底负责什么

### World Vision：先创造一个没有主角也成立的世界

World Vision 是 protagonist-blind：不知道未来主角是谁，也不知道未来 Power Asymmetry 是什么。它仍是一轮 Luna high，不新增 World Reviewer。

#### 负责

- 普通人的生活、上升与失败路径；
- 当安全、地理或旅行会限制人生时，普通人怎样跨越聚落、谁能独行、哪些现实通道把当前生活连接到更大世界；
- 力量体系的正常值、稀缺度、境界/能力的可观察差距；先用 1—3 句普通话说清力量来源、直接作用、成长与失败，再给会反复使用的对象/层级短名。**精确力量主尺是强制 Root Grammar**：World 必须选择 `连续数字 / 大境界+数字子级 / 数字序列` 之一，并给出主尺名称、含 `{N}` 的精确位置格式、明确数字精度规则、当前可见数字范围和少量大档位；任何主要修炼者都应能被写成一个唯一精确位置。它只负责 Reader Ruler，不变成总战力分或战斗公式。**Small Grammar, Large Variation**：已有一到少数互补力量操作轴如果已经简单、有辨识度，就保护它，不为“更统一”泛化成元能量/总机制；Small Grammar 不等于 Small World，主动让旧规则长出新招式/战斗姿态、身体/物种、兵器/奇物、异兽/伴生物、会改变玩法的环境、组合与稀有例外，让读者旧知识持续复利。World 同时主动寻找 0—1 条真正成熟的 Optional Secondary Fantasy Road；没有足够好的创意就不造，也不预设未来主角一定会走。创新放在力量因果和玩法，不靠多个新词互相解释；默认直接力量先写身体、攻击、防御、移动、元素、兵器等可感知效果。对当前会频繁使用的少数力量/价值/身份档位给 1—2 个可感知、可复用 benchmark，供下游稳定比较，不建战力数据库；
- 明确区分 **Public World Knowledge / Mystery**：普通人从小知道的主流力量、粗略强弱尺、当前/下一档现实含义、日常危险、上升入口与价值物，要能被下游直接用普通话说明；环境纹理和专名不能替代基础答案。来源、隐藏原因、幕后关系与未来 reveal 继续进入知识边界；
- 宗门、王朝、家族、商盟、种族等怎样真实影响人生； named 势力 / 部族若会进入世界大事，同时给一个不剧透的公开类别锚点，让章节期 WORLD AUTHORITY 能回答“它是什么”；
- 世界里真正值钱、值得人物争夺和羡慕的东西；
- 3—6 件即使主角从未出生也会推进的人物行动、战争、迁徙、竞争或灾难；
- 真正值得进入的地点、奇观、危险与未知；
- 普通人 / 专业人士 / 顶层势力各自知道什么。

#### 不负责

- 主角 Biography、欲望、关系原点；
- Core Power / Power Asymmetry；
- 为未来能力预留“钥匙孔”；
- 主角第一次兑现与终局使命；
- 为证明世界独立而补完整政治经济模拟。

健康判断只问：**没有主角，世界是不是仍有具体的人在做事、具体地方想去、具体东西值得争？** 不再为这个问题增加 production 正交删除测试、Reviewer 或 scorer。

---

### World Expansion：世界根语法稳定，故事视野向前生长

开书 `WORLD_VISION.md` 是 **World Root + 当前可见 World Horizon**，不是要求第一天就写完 500 章所有大陆、文明、顶级势力和终局规则。世界真正被当前故事活透后，可以追加 forward-only World Expansion；这和作者回头修改开书世界是两种不同语义：

- **World Rewrite**：改已经成立的根规则或旧事实，会使 Power / Human / Character 及全部未来下游 stale；
- **World Expansion**：旧事实不变，只增加从某一未来章节开始才真实进入故事的新世界层，只刷新未来 Story / Outline / Run，不重做 Origin Character。

触发由故事边界决定，不按“每 100 章必须扩一次”缴税。100 章可以是普通长篇的观察尺度；真正条件是当前世界层已经难以继续制造新的欲望、尺度、入口或不同 Story Engine，且人物通过具体事件真正来到更高边界。

World Expansion 使用 **GPT-5.6 Luna high 的 protagonist-blind fresh context**：只看 World Root、此前已批准 Expansion、明确的 `Canon → World State` 与小型 World craft；不看 Current Character、Power Stack、Human、关系、Story Handoff 的人物化答案或未来计划。它只创造世界现实，不替 Story 设计“最适合主角的下一件宝物”。

力量尺也服从 Forward Expansion：`scope=macro` 只能延展 World Root 已冻结精确主尺的**可见数字范围**，不得把“每境1—9星”改成初/中/后期或另造第二套全局计数；如果本轮只扩地理/社会，精确尺范围可以 `NONE`。多世界副本流使用同一机制但有双层时钟：跨世界稳定规则留在 Global / Meta World；每个真正独立新世界用 `scope=instance` 追加 Local World Authority，并强制建立自己的**本地精确力量尺**。本地尺帮助读者理解该世界内部位置，但不会反向改写主角全局主尺。离开副本后 Local World 与本地尺从章节 `WORLD AUTHORITY` 退场；真正带走的 Power、物品、关系、身份、知识和 Meta consequence 继续留在 Canon。

---

### Power Seed：决定“主角相对世界正常力量，哪里拥有明显非对称优势”

Power Seed 只读 deterministic `POWER_BASELINE`、固定 1 条 source-blind Naming Craft Reference、少量 Power GBrain craft，以及非 Canon `Power Novelty Spark + Optional Lexique Primitive Pool`，不读 Human Biography，也不读 named Story Opportunities。Novelty Spark 为 3 个候选各采样一个“熟悉能力幻想 × 单一异常”；Lexique pool 只提供少量对象×变化 primitive，模型每个 Candidate 最多借 0—1 个、也可以全部忽略。两者都只在 Power 生成时存在，不向下游传播。

核心语法：

`World Power Normal → Familiar Fantasy × One Deviation → Power Asymmetry → Core Fantasy → Growth Compatibility`

创新边界：**设定创新 ≠ 术语创新 ≠ 机制复杂化，Novelty ≠ Power Fantasy 强度**。Power Asymmetry 不强制来自世界内合法例外；它可以是稀有天赋/体质、唯一奇物/际遇、外来知识/经验、外挂、正常维度上的极端天赋或少量优势叠加。每个候选最多一个主异常，必须先用一句大白话讲清“别人做不到什么，我具体多能做什么”。Lexique primitive 只有在它让同一主异常获得更具体的身体/器物/空间载体或真正新玩法时才采用；只是换皮、增加限制、变玄或降低 Privilege Delta 时直接忽略，不得借它改写 Novelty Spark / POWER BASELINE 已有触发、覆盖、代价或 Boundary。命名同样**语义先于气味**：固定 Naming Craft Reference 只帮助读者理解与词根复利；首读准确高于世界气味，只有不牺牲准确时才复用 World 已有具体词，lexique 次之，也可以完全不用。普通短名已经准确、顺口、低学习成本时，不为“更独特”强行改写；名字多承诺了来源、对象、代价、等级或第二系统时，改名字，不扩机制迁就它。默认强度故意偏夸张：宁可初稿偏强一档，也不要让 LLM 把优势平衡成“更方便”；相对同层普通人/天才至少一个维度要明显超标，甚至提前拥有通常更高一大档或数档才有的局部特权。Permanent Boundary 防万能，不做对称成本结算，优先收束成一到少数真正根边界，必须留下明显纯收益；长期默认 **Boundary Stable, Privilege Expands**，不随成长同步追加疲劳、反噬、冷却等平账条款。直接型能力的长期掌握继续扩大控制、对象、战斗复合和危险场景下的稳定使用，不变回结构分析、材料诊断、路线计算或验证流程；Legendary / Future Legend 也不能绕过 Permanent Boundary。为什么“馋”必须落到读者立刻想使用的具体体验；长期还应能与功法、装备、环境、传承等产生新化学反应，而不只增加数量与距离。

#### 负责

- 一句话能理解、能想拥有的 Core Fantasy；
- 正常修炼轴：世界本来的成长怎样真实增强主角本人；
- Power Asymmetry mastery：非对称优势怎样继续扩大具体能力；
- High-Tier Mutation：高阶发生什么真正质变；
- Permanent Boundary：高阶也不会自动消失的边界；
- Legendary Power State：力量体验上限。

#### 不负责

- 谁会得到这个能力；
- 童年、家庭、人格、关系和人生使命；
- Story Opportunities；
- 把能力自然职业化成维修、诊断、运输、审核、构筑或流程管理。

关键原则：**Power Seed 只决定开局 Core Asymmetry 的成长语法。** 它不包办全书所有能力；后续新的 Power Asymmetry 由 Story Program 通过真实故事获得并与旧优势复合。

长篇运行时因此采用**两层 Power**：

- `Power Origin Core`：开书已批准、长期冻结的核心异常与根边界；
- `Current Power Portfolio`：正文已经真实获得/证明的后续能力、身体变化、兵器权限与 Advantage Stack，由 `PERSISTENT CANON → Power / Capability` 持续更新；该小节第一行固定保存 `Current Power Position｜主尺：…｜精确位置：…`。Human Seed 冻结 T0 精确位置；State 只有在最终正文明确突破时才更新，越级胜利/社会重新估价不能反推升级。后续 State 若漏写该行，代码继承上一 Canon 位置，避免几百章里因一次抽取遗漏丢失主坐标。

例如后期拿到神兵、魂骨、传承或第二种非对称优势，是 forward Power Delta，不回头改写 Power Seed。周期性 `CURRENT_CHARACTER.md` 把 Frozen Origin、Current Power Portfolio 与**当前精确力量位置**一起编译给 Story Refresh，而不是拿 Chapter 1 的能力状态重新规划几百章后的主角。

---

### Human Seed：决定“这个人原本是谁”

Human Seed 只读 deterministic `LIFE_CONTEXT` 与 Human GBrain craft，不看 Power，也不看 named Story Opportunities。

当前结构：

`生活事实 → 多重动机 → 冲突中的稳定选择偏向 → 具体人物关系`

#### 负责

- 世界中的初始位置与具体生活事实；
- 2—4 股会长期进入选择、可能互相冲突的私人动机；
- 稳定选择偏向 + 具体实现随现场变化；
- 能真实改变去留、风险、时间、暴露和机会牺牲的具体关系；
- T0 当前私人欲望（只进入可变状态）；
- 候选人物钩子（非正式故事事实）。

#### 不负责

- 逐条用 Biography 证明人格；
- 把一生统一成一个 `Core Obsession + Excess`；
- 把人净化成理性、责任、自主、反控制的标准优等生；
- 猜未来 Power 或为外挂预留主题化童年。

**经历是背景，不是人格证明。** 同样的生活事实本来就可能长出不同的人。人物辨识度来自多股动机冲突时反复暴露的选择偏向，而不是漂亮的人生哲学。

长篇运行时采用**三层 Human**，但三层时钟不同：

- `Human Origin Core`：开书稳定选择偏向与 competing motives，长期冻结为人物起源；
- `Current Human State`：当前欲望、关系、承诺、身份与短中期状态，随 Canon/State 正常变化；
- `Human Development Delta`：只有几十章甚至更长的已发生历史已经稳定证明“继续只用旧 bias 会写错这个人”时，才由独立 Luna high 阶段提出 forward-only Delta；默认允许 `NONE`，不要求每次 World Expansion 或每个副本都运行。

Human Development 只看 Frozen Human + 已发生 Canon，**看不到未来 World、奖励与 Story**。这样既避免“连续救人三章 → 人格被改成圣人”，也避免 Story Refresh 为了适配新世界反向把人物进化成最正确的样子。后续 Delta 按生效顺序保留；人物可以真的改变，但不能失去自己的历史。

---

### Character：确定性组合，不做后验合理化

`CHARACTER.md` 由已冻结 Power Core 与 Human Core deterministic compose，没有 Character Composer LLM。

它只保留两个 authority 并列，不解释“为什么这段童年注定得到这种能力”。World / Power / Human 之间的不协调是后续 Collision 的故事材料，不是需要抹平的错误。

开书 `CHARACTER.md` 仍只保存 Frozen Origins。长篇边界需要重新规划时，代码再确定性生成 `CURRENT_CHARACTER.md`：`Origin Power + Current Power + Origin Human + Human Development + Current State / Relationships / Identity / Knowledge / Assets / Canon`。这不是新的 Character Composer，也不调用 LLM；它只是把已经发生的历史压成给 Story Refresh / refreshed Outline 使用的当前人物权威。

---

### Story Program：Collision + Long-Form Causality Designer

Story Program 是第一次同时看到完整 World 与 Character 的阶段，也是当前默认使用 Sol high 的最高杠杆规划节点。

核心身份不是“小说总体产品经理”，而是：

> **这些已经存在的人、力量与世界，接下来怎样互相改变。**

第一原则：

> **成长是全书纵向不变量，不是每个阶段的必填项。**

#### 权威与调度必须分开

- Power Seed 决定开局 Core Asymmetry 及其成长语法；
- Human Seed 决定人物长期选择偏向与多重动机；
- World Vision 决定世界事实与独立人物行动；
- Story Program 不能重写以上创意权威，但可以通过真实获得加入新的 Power Asymmetry；
- Story Program 决定开局优势怎样成长、新优势怎样加入，以及新旧优势怎样复合成新的具体玩法；后续新 Asymmetry 先用普通话写“以前做不到什么、现在具体多能做什么”，再决定是否需要世界内短名，新名只压缩已经理解的能力。

因此：**Power Seed 决定开局核心；Story Program 决定长期优势栈怎样通过故事长出来。**

#### 当前 World Horizon 的长期责任

- 通常 5—7 个自然大型阶段，但只具体规划当前已批准 World Horizon；若当前世界层 3—4 个阶段就自然走到边界，就停在那里，不为凑数提前发明未知下一世界；
- 清楚的 **全书成长与 Core Fantasy 兑现脊柱**：少数够重的结构质变分布在早期、中期、高阶自然阶段，不固定次数；结构质变少而重，但 Fantasy Surface 可以持续偏丰富，质变之间继续用既有力量语法长出新招/战斗姿态、装备/奇物、身体/物种、异兽/伴生物、环境、越级对象与复合玩法；
- 优势栈不能只让开局能力变大：全书要有新的 Power Asymmetry 加入，并出现新旧优势组合后单项做不到的复合玩法；这不是每阶段新增能力税；
- 每次成长写成具体事实：以前打不过谁、去不了哪里、做不到什么，现在具体能怎样战斗、移动、探索，或哪两项优势怎样一起产生新结果；
- **高价值 Asymmetry Reveal 要反复做 Public Proof，而且三条线共享精确力量主尺**：Core Asymmetry 首次被看见、新层级/质变、新旧优势首次复合、进入更高圈层后第一次被重新观察、或旧社会估值已明显落后时，按现场条件允许三条并列爽点同时成立：真实观众的 Collective Shock、懂行者的 `Ruler Calibration`、关键人物的 `Behavioral Repricing`。若事件与主力量有关，三条线用同一个精确坐标工作：群体震动承受“43级击败58级 / 三星打五星 / 开脉4重越凝罡1重”这种明确差距带来的现场重量；懂行者直接说明双方精确位置、正常差距与这次超标在哪里；关键人物再因为“精确位置 + 超标表现”改变报价、待遇、敌意、战术、招揽或准入。三者没有高低之分，大型公开节点可以一起吃满。**精确尺是 Reader Ruler，不是胜负公式**：低位者可以靠技能、装备、经验、环境与 Power Asymmetry 越级，越级胜利本身不能反推 `Current Power Position` 自动提升。只避免凭空造群众或让所有人轮流说同一套专业解释；短期群体震动本身可以成立，只有重新估价继续改变后续资源、关系、敌意、战术或信息流时才进入长期 Canon。
- Core Fantasy 必须周期性重新证明“为什么这项力量仍值得追”，但不要求每阶段升级；兑现优先保留这项幻想最独有的**生活特权**，不只复用最容易安排的战术用途。长期重释也不能永远只落在世界层：Power / Character / 已批准旧人旧物旧关系自然存在可回收锚点时，保留主角级重释纵深，但不为 Personal Myth 凭空补隐藏身世或未批准旧史。
- **AGGRESSIVE Payoff Bias**：因果已支持的主 payoff 真正落地，不无故降成资格/认可/以后再给；大胜可以自然连带主奖品 + 钱/资源 + 招揽/入口，秘境可以有主目标外惊喜，大型阶段可以同时带来据点、队伍、产业、商路份额或长期收入。奖励数量本身不是失败，只淘汰无因果到账与同窗口近似奖励抹平真实牺牲。
- **Character relevance ≠ Story Engine authorization**：除非作者明确选择职业/制度/经营题材，责任、精确、审计、边界、路线、损失归因等职业性倾向只作为低权重局部偏好；即使它们与 World 的公共资源/路线/治理素材高度匹配，也不能因此连续成为大型阶段的共同解题语法。主角不是多方协调员。大型阶段优先先锁定少数具体 Desire / Major Reward Anchor，再把公共资源实施压到大方向选择与直接后果。
- **Plot Pace ≠ Tier Pace**：事件、关系、发现、敌人策略、获得和玩法可以快速推进；同一力量层级仍有丰富故事空间时可承载多个完整阶段，不用境界提升证明“剧情有进展”，避免过早耗尽主尺。
- **Rapid Growth Needs Protagonist-Specific Causality**：若作者明确要求异常快升级，Core Asymmetry / Advantage Stack 必须有一条读者可观察的效率、资源、实战反馈、风险收益或机会获取优势来解释速度；不能只由情节按章递送升级材料。真正有吸引力的 Mystery 也不急着资源化/结算化；长期 Rival 学到能力边界后，至少一次反制要真实改变主角的选择或局面。
- **主人公连续升格**：力量/身体、身份/关系、世界入口、认知与选择权不是平行 KPI；优先让一次成长造成更高层人物重新估价，继而打开新圈层/地点/真相，再产生新欲望、敌人与过去没有资格作出的选择。新圈层人物只按自己真实知道的旧名声/战绩/已公开底牌先判断，再因最低充分的新事实分别更新待遇、敌意或合作，不默认全知也不靠降智轻视；同一等级可以先真正活出新的社会位置和世界位置，再自然升阶。
- **成熟第二幻想轴**：Story Program 主动检查 Approved World 中已经成立的副轴，不因它不是 Core Power 就忽略；职业/专业只有在它本身就是可欲望的强者道路时才升格——有独立强弱、顶层人物、可见胜负/作品、稀有成果与社会价格。普通实施继续压缩；主角是否投入由 Human 决定，Human 不想走就让它属于世界或配角，不强制每书有副职。
- **可判定兑现债务**：少量自然出现的强挑战/承诺可以保留“具体对象 + 至少一个可观察结算条件”，给长期读者明确距离感；它不是倒计时 KPI，可以错过、失效、延期、输掉或被人物主动放弃。
- **World Horizon Handoff**：当最后 1—2 个自然阶段已经把当前世界层主要压力活透，Program 要给下一轮留一个交接任务：写可观察触发条件、`macro / instance` scope、为什么此时必须扩、哪些已发生事实必须 carry forward；不得提前指定下一世界宝物、能力、势力或针对当前 Build 的答案。若 Approved World / Canon 已有真实外缘信号，可在 Handoff 前让读者看见一次“刚登顶才发现山外有天”的尺度冲击；没有现成 authority 就不硬造。若还没到边界，明确 `NOT YET`，不按固定章数强行扩张。

#### 大型阶段发动机

阶段可以主要由任意一种发动：

- **人生**：私人欲望、关系、人生去留、旧后果；
- **幻想**：力量、战斗、获得、探索、新玩法；
- **世界**：世界本来就在发生的人物行动与大事。

三者不平均配额。一个阶段可以没有境界突破、没有新装备、没有新技能；只要故事因果与 Stage Delta 成立，就可以完整。

#### Collision 补充过去的边界

Story Program 可以为了让当前关系、局部性格反应或某次选择更自然，补充少量**非奠基性的过去经历、共同往事或旧事件**。这些历史可以解释人物的一部分质感，但不能重写 Human Core，也不能把整个人格收束成一条整齐的创伤因果链。

- 不为了人格合理化自动制造悲惨童年、父母惨死、被抛弃、背叛、虐待或重大失去；普通、愉快、尴尬、失败、欲望、争执、错过同样可以有叙事重量；
- 这类为人物/关系新补的过去**不得自动成为小说主线或大型阶段发动机**；
- **历史事实与历史揭示分开**：Story Program 可以知道某件过去存在，但 Outline 只在当前故事真正需要时安排读者逐步看到其中一小部分，不一次性倾倒完整往事。

#### 当前轻量阶段合同

每个阶段只回答：

1. **为什么现在发生**；
2. **谁想要什么**；
3. **主角的关键选择与行动**；Power 若介入，直接写它怎样改变行动和结果，不单列能力税；
4. **这一阶段真正的阅读满足**；
5. **Stage Delta**：只写真实改变的维度，可包括 Power / Capability、Possession、Relationship、Identity / Access、Knowledge、Enemy State、World State；某维度没变就不写；
6. **下一阶段为何自然发生**。

#### High-Value Acquisition 与 Compounding

二者保留，但从固定 stage schema 降级为纵向 reader-appetite / continuity 原则：

- **High-Value Acquisition**：世界自然出现真正让人想要的剑、功法、身份、同伴、洞府、飞舟、名额或其它高价值对象时，让人物真实争取、占有、使用和可能失去；Access / Identity 可以是爽点，但不能长期替代具体 Fantasy Possession。某件功法、兵器、身体变化、奇物或传承已经成为主要欲望时，先让读者知道它为什么值、谁愿意为它冒险、拿到后具体能做什么，再让到手、错失或放弃发生；**真实错失允许有空窗**，刚因关键选择放弃一个已建立欲望的高价值对象时，不为补爽点在同一结算窗口立刻塞分量/功能近似的替代奖励；没有自然机会就不制造；
- **Compounding**：过去得到的力量、物件、关系、身份、知识与入口一旦成立，就必须继续改变后续行动、选择、敌人应对或世界局面；不要每阶段填 `Compounding Growth`，也不要让旧获得写完即消失。

#### 不负责

- 重新定义 Power / Human / World；
- 每阶段强制 `核心优势参与 / 一级成长 / 关键获得 / High-Value Acquisition / Compounding Growth / 净新增`；
- 把 Life / World 事件重新解释成“更好的升级路线”；
- 把同一 Plot Engine 换地图重复六遍；
- 为维持长篇发明未批准的新力量层。

健康的 Program 让读者同时看到：**这个人仍然是这个人；世界仍然大于外挂；主角确实越来越强；过去发生的事情继续改变现在。**

---

### Story Refresh：Periodic Re-Collision，不把旧 Program 无限延长

World Expansion 被作者批准后，先确定性刷新 `CURRENT_CHARACTER.md`；只有这个阶段，Sol high 才第一次同时看到 **Effective World × Current Character**，重新规划当前新的 World Horizon。

Story Refresh 不是把旧 Program 续写几十行，而是 fresh collision：新世界不能为了主角重新改；Current Character 也不能为了适配新世界被重写。旧 Story Program 只保留仍未兑现且仍成立的因果。允许主角错过机会、NPC 拒绝、旧能力在新世界出现意外用途、Human 因私人偏好走非最优路线；新的 Power Asymmetry 只能从新世界已经独立成立的真实机会中获得。

真实模型 A/B（普通玄幻 Ch120 + 多世界 Ch80）比较了“单 Sol 全包”与分权路线：单 Agent 两个 Case 都没有获胜，最典型失败是把世界材料、岗位、奖励和人物课程做成当前主角的钥匙孔。最终 production 采用：**独立 World Expansion + 可选独立 Human Development + deterministic Current Character + Sol Re-Collision**。这类 Agent 只在长篇边界运行，不进入每章链。

Story Refresh 自己也只规划当前新 World Horizon，并继续输出下一次 `World Horizon Handoff`；它不会因为进入第二轮规划就重新一次性预写全书剩余世界。

---

### Progressive Canonization：允许作者自己暂时不知道答案

长篇 Mystery 不要求开书时存在完整终极答案。TGN 正式区分：

- `AUTHOR OPEN`：问题已经成立，但作者自己当前也没有决定答案；这是合法状态，不是待补设定；
- `AUTHOR FIXED HIDDEN`：作者已经决定一小层事实，但人物与读者尚未知道。

低频工作流是：`AUTHOR OPEN → Decision Surface → DEFER / DECISION NEEDED → Reframe R1/R2/R3/D0 → 作者选择 → Independent Compiler → AUTHOR FIXED HIDDEN → Planning → reader-facing Reveal Event → State/Canon → 更深 AUTHOR OPEN`。

**触发由下一段故事真正需要什么决定，不由章节数决定。** 如果作者下一步仍可以写出具体的争夺、关系、探索、获得和后果，Decision Surface 必须允许 `DEFER`；只有作者已经批准的下一事件无法在缺少某一最小事实时成立，才指出 `Smallest Decision`。因此作者可以先有一个好小点子一路写，等某个真正想看的新场面把世界逼到墙角时，再只补足那一层大框架。

Reframe 只给局部方向，不替作者选。Compiler V2 只检查：该 Fixed Point 是否回答且只回答 `Smallest Decision`、是否兼容已发生 Canon、是否把 Future Direction 错当过去事实、候选自己的 `What Remains Unknown` 是否继续开放。旧 `AUTHOR OPEN` 的 Unknown 列表是**决策前未知池**，不是永远不可回答的禁区；采用后新的 `What Remains Unknown` 才是保护边界。

Compiler 也遵守和 Premise Compiler 相同的 stale discipline，但不增加 hash：生成 Compiler Prompt 时，代码把当前 Mystery Thread、selected candidate、Decision Surface、author planning need 与当前 BOOK/Canon **原文 snapshot** 保存在 `MYSTERY_CONTROL.json`。采用 Hidden Fixed Point 时直接比较这些文本；候选、Thread 或 BOOK/Canon 任一变化都要求重新编译。作者可以自己改候选，但不能把旧 PASS 误绑到新候选；`FIXED_HIDDEN` 不能通过普通 PUT 绕过 Compiler + adopt。

Hidden Truth 存在独立的 runtime-blind `MYSTERY_CONTROL.json`，不放进 BOOK / AUTHOR NOTES。`story` route 只给 Story Refresh，`world` route 只给 World Expansion；Outline 只得到 Reveal 章号与 `[MYSTERY-REVEAL:ID]`，看不到答案。Story Refresh 若决定当前 Horizon 应揭这一层，只输出 reader-facing `MYSTERY REVEAL CONTRACT`；保存 Story Program 时代码把 Contract 剥离并单独保存。Reveal 章 Runtime 只得到具体 Event Atom、State Residue 与 Still Open，不得到 raw Fixed Point。

**Reveal 是事件，不是百科答案。** 后台可以知道“两个现实共享同一实体”，正文却应该让读者看到“另一侧敲了一刀，主角手里同一把刀当场崩出缺口”。只有正文实际发生以后，State 才把 reader-facing Residue 写成 Canon；随后更深问题重新成为 AUTHOR OPEN。Backward-compatible reinterpretation 可以让旧事实获得新意义，但不能把过去明确为真的事实改成假的。

这套机制不进入每章链，不新增 Mystery Reviewer / 每章 Gate / 自动 Repair，也不要求所有 Open Promise 使用 Progressive Canonization。普通悬念仍走现有 Story / State；只有真正需要作者分层决定长期真相的 Mystery 使用它。

---

### Growth Genome：整理，不创造

Growth Genome 是投影和记忆工具，不是创意权威。

#### Classic Patterns Are First-Class Citizens

可组合不等于主动回避成熟男频主干。资源 → 成长 → 战斗 → 身份 → 更大资源/世界、探索 → 机缘 → 成长 → 新区域等结构都可以直接使用；创新优先放在本书自己的核心幻想、能力玩法、人物关系和阶段换挡，而不是为了显得新而绕开有效结构。

一级成长始终优先回答“主角本人越来越能做什么”；财富、装备、身份、关系、势力、领地和世界入口属于二级收益，优先反哺下一轮一级成长。

#### 负责

- 整理一级成长；
- 二级收益；
- 主循环与反哺；
- 阶段升格；
- 重复风险。

#### 不负责

- 重新选择 Fantasy；
- 替 Story Program 发明剧情；
- 强迫每本书拥有复杂变量网络；
- 把故事转换成数据库思维。

原则：**Growth Genome 服务故事，不让故事服务 Growth Genome。**

---

### Outline：决定“这几十章具体有哪些故事”

Outline 是 Story Program 与 Director 之间的中层分辨率。

#### 负责

- 当前中期规划窗口；
- 若干大型剧情块；
- 每个剧情块真正的故事主问题；
- 通常 3—5 个连续故事锚点；
- Future 10 的逐章具体事件；
- 故事开写前的 **T0 Initial State**：只记录 Chapter 1 第一场事件发生前已经成立的事实；Future 10 / 剧情块中规划出的能力使用、奖励、物品、关系变化、伤亡和其它未来结果只能留在 Plan / Open Promises，不能提前进入 Current State / Canon；
- **Story Program execution, not rescheduling**：Power Seed 决定开局 Core Asymmetry grammar；Story Program 决定开局优势成长、后续新 Asymmetry 获得与复合；Outline 只把已批准变化落进当前窗口。某个剧情块可以完全没有 Power / Acquisition / 新地图；已经安排在当前窗口的真实成长又不能被省略；
- **Forward Authority after refresh**：开书 Outline 读取 `CHARACTER.md + T0 + WORLD_VISION.md`；周期性 Story Refresh 后，Outline 改读 deterministic `CURRENT_CHARACTER.md + Effective World（Root + 已批准 Expansion）`，不能拿 Chapter 1 的人物状态继续规划 Chapter 200；
- **World Horizon Handoff 是前向边界**：如果批准 Story Program 的 Handoff 会在当前中期窗口 / Future 10 内触发，Outline 只排到触发章就停止。剩余章数不补占位，不自行发明下一大陆、下一副本或新规则；先完成 World Expansion / Current Character / Story Refresh，再生成新的 Outline；
- **Block Delta**：每块只记录相对本块开始真实改变的 Power/Capability、Possession、Relationship、Identity/Access、Knowledge、Enemy State、World State，没变化的维度省略，上一块已经发生的变化不能重复包装成新 Delta；
- **World Model Release / Reader Release Scheduler**：Approved World Vision 决定世界事实；Outline 在 `## 2. 世界观结构` 内用一个很短的 `Reader Release Map` 保存当前窗口里值得显式调度的首次释放，格式 `第N章｜触发：具体 World fact`，不是每章 KPI。未来仍作为 discovery / reveal 的答案不得提前排入 Map；只能先释放不回答谜底的公共背景。明显陌生/架空世界的第1章若 World 与前3章确实提供多类相关公共事实，默认把力量/当前与下一档 ruler、生活危险/共同常识、其它确属 World 的社会位置/价值物拆成 2—3 条 Public Common-Knowledge Release；下一档若有现实 benchmark，同时写能力效果与社会含义。**具名机会价值不混进 World Release**：若 Story Program / 当前剧情块已批准机会名与公开价值，但 Future 10 单章条目只剩泛化“试场前训练 / 争取机会”，Director runtime 只在当章已指向同一机会时，从当前剧情块确定性恢复一条“具体机会名 + 当前已知价值”；不新增回报、不提前宣布结果。**World Entry 在人物真正跨过门槛的当章释放**；重要 named 势力、地点、Rival、传承或高价值机会第一次进入时保留最短欲望与尺度锚点。Chapter Runtime 按章读取，再从 WORLD AUTHORITY 取对应事实；开篇同时建立最低生活世界位置与必要 ruler。不新增 Prelude / Setup 章，也不能推迟第一章核心优势真实结果；
- **Ruler = Compression**：当前事件碰到哪把尺（力量、战绩、价值、天赋/适配、技熟、装备、排名、身份或世界层级），就用一次 World 已批准的 benchmark / 懂行比较完成校准；它优先替代多轮重复验证，不是新的百科段落。若本章真实跨过已经介绍过的公开档位，结果处直接命名新档位一次，不让读者从本地术语或现象自己换算；
- **State Advance After Proof / Choice → Consequence**：一个问题经动作结果与一次足够校准成立后，不再把换证据证明同一结论规划成独立 beat；社会确认只有改变机会、敌意、关系、身份、资源或行动入口时才继续。重大选择的选项与主要代价清楚后尽快做出，让后续篇幅进入选择造成的新局面。**Stage Settlement = Consequence, not Process Carrier**：事实已清楚时，报告、登记、责任说明、复盘、资格发放等只作一句/背景，前景放在重新估价、实际得失、Rival 换位与下一件值得想要的机会；十章批次不是拉长当前剧情块的配额，块完成就进入相邻块；不做每章状态变化配额；
- **Core Gameplay Variation**：第一次高光以后，尽快把“它能不能做到”推进成“为什么选这个对象/时机/用法、别人怎样反制、同一优势还能产生什么不同结果”；尤其不要让上一轮已经证明有效的解法自动解决下一轮主要问题，下一轮冲突优先攻击它尚未解决的对象、关系、资源、目标或条件，或迫使主角换一种用法。这样实现换挡，不要求机械让主角失败或每轮加新代价；
- **Reader Experience Projection**：Action Space / Expectation Ladder / Mystery Depth / Impact 仍作为后台阅读体验坐标，但通过具体故事锚点和实际 Delta 自然显现，不再要求每块或每十章分别填写“一级成长 / 净收益 / 新行动空间 / 世界扩张”；
- **Theme Is Derived**：`## 11. 主题、价值观与长期问题` 只后验总结已经由人物、欲望、世界与事件自然形成的主题；没有稳定主题时允许“暂不预设”，不得反向决定世界 ontology、资源、敌人、能力升格或终局。

#### 不负责

- 把 100 章全部写成精细施工步骤；
- 把每个锚点拆成“观察、分析、验证、执行”；
- 重新发明 Story Program；
- 临时重写 World Vision 的力量尺度、身份基础逻辑或核心能力兼容边界；
- 越过尚未执行的 World Horizon Handoff 替未知下一世界写具体设定、奖励或长期 Power；
- 把远期升格强塞进固定百章窗口。

#### 为什么需要故事锚点

如果 Outline 只写“这一阶段利用隐藏道路扩大优势”，Director 就必须自己发明中间事件，LLM 最容易选择可操作、可重复、逻辑稳定的任务：搬运、探路、验证、修复、调查。

Story Anchor 的作用是提前确定“真正的故事发生了什么”，降低 Director 自己发明低价值任务的空间。

---

### Director：决定“这一章到底发生什么”

#### 负责

- 根据已批准长期方向、当前剧情块、Future 10 和 Canon，生成当前章事件合同；Future 10 当前条目在进入 Director 前先被确定性拆成 `本章唯一可执行事件预算` 与 `章末 Handoff Reservation`，Long Block 只作阶段背景；带明确章节范围的 Long Block 只有覆盖当前章才进入，显式过期或无合法匹配时 fail closed，不回退整份旧长纲；后者只能制造下一章为什么必须发生，不能提前付款、正式身份、获得、升级或其它下一章结算；
- 当前条目已批准的 `结果 / 状态变化` 不依赖 Director 重新复述：runtime 确定性并入 Frozen Mission 的 `状态变化`；Director 静默省略不构成取消，只有已发生 Canon 真冲突时才允许结果失效；
- 抓本章最值得读、最值得复述的人物冲突、关键选择、力量使用、反转和结果；
- **Discriminative Detail Only**：调查、手艺、医学、制作、检测、推理等 Supporting Skill 只保留足以改变判断的少量关键细节；一旦能推出发现或决定，立即进入发现的选择、冲突与后果，不继续展开实施过程；
- 决定已经做完后的停车、搬运、排布、绑缚、登记、普通赶路等实施默认压缩；只有重新出现选择、冲突、不确定性或失败风险才恢复成场景； `主角行动` 对此只保留关键决定 + 至多一个决定性动作 + 结果，不把并列实施步骤继续传下游； 若该决定性动作仍只是非核心 Supporting Skill，就只保留“做什么 / 为什么有效 / 结果”，不把技能实施本身变成第二个场景发动机； 前文已成立的 Supporting Skill 默认只写其结果，不再把“利用某判断/技巧”方法重新放进事件合同；只有新边界、失败或质变例外；
- 不用 **Competence Filler** 填低动作章节：若真正故事是 World Entry、势力登场、立场、误判或关系变化，主角只做观察、站队、拒绝、跟随或守住位置也成立；不得为了“显得有用”临时制造排车、维修、诊断、路线、清点等专业问题；
- Outline 已经把入口、邀请、名额、工作机会、身份待遇或奖励作为可选择/可获得条件时，不为“证明配得上”自行补试工、观察、检查、考核、登记或资格流程；Plan 没安排，就直接进入接受/拒绝及其后果；
- 决定章节边界与停止位置；
- 保证已发生事实和当前计划连续。
- 旧人物、旧承诺、身份谜团或长期秘密回流时，在现有八字段中明确本章结束后**哪一个新事实真正成为确定事实**；若上游未授权揭晓过去原因，就明确原因仍未知，并把不可逆变化落在当下选择、证据、立场、职责、关系或行动入口。

#### 不负责

- 生成世界观；
- 临时发明境界名、等级数值、货币、基础待遇、稀缺奖励、能力限制或高层力量兼容规则；这些属于上游已批准世界/玩法事实；
- 重做几十章 Story Program；
- 拯救一个已经工程化的长期大纲；
- 把“主角行动”写成完整施工清单。
- 用“真相进一步揭露 / 至少一条旧线发生变化”把隐藏答案留给 Writer 自行决定；
- 为了填满本章结果，补造几十 / 几百章前未被 Canon 或上游计划确定的秘密历史。

Director 的核心问题不是“这一章还能安排什么任务”，而是：

**谁想得到什么？主角凭核心优势完成了别人做不到的什么？这让谁的选择、利益、地位或行动空间发生了什么变化？**

---

### Curator：决定 Writer 真正需要看到什么

#### 负责

- 从大量 Canon / Book Contract / Inspiration 与 Scene Skill v2 紧凑 Catalog 中筛选当前章真正相关信息；Catalog 只含 `skill_id + Reading Question + 一行 Projection Guidance`，Curator 只在当前场景有真实 realization 缺口时编译 2—4 句 `Scene Prose Projection`，已经清楚则写 `NONE`；
- 保留人物欲望、关系、力量、风险、承诺与当前冲突；**Frozen Human Core 高于最近几章行为归纳**，不因连续救人、负责、诚实或克制就把现场选择升级成新的稳定道德人格。若本章自然触发已批准的虚荣、钱、审美、身体吸引、享受、好奇、偏心等私人牵引，保留一个可直接进入场景的注意/想要/靠近/回避/选择触发，不只剩职责协作与成熟沟通；若 Frozen Human 已明确某个具体人会因吸引/依恋/偏心改变主角选择，而本章出现近身照料、重逢、分别、私密靠近、嫉妒或邀请等关系性现场，默认属于自然触发，保留一个克制 cue，不要求它改写主事件；
- 压缩不必要的规则和机制说明；
- `WORLD AUTHORITY` 是已批准 World Vision 的安全事实源；`Reader Release Map` 为当前章排程了哪条 World fact，Curator 就从 deterministic prefetch 中保留/压缩哪条，不自行选择另一套世界介绍； `Relevant Plan` 同样压缩决定后的普通实施，只把决定、真正影响成败的动作和结果交给 Writer；
- 把规划层抽象词投影成 BOOK / Canon / Plan **已经存在**的世界内具体名词和动作，让正文写人物真正拿到、失去、进入或看见什么；
- 让细节预算跟随本书核心幻想真正值得注意的对象，而不是把“具体性”自动变成地形、受力或流程细节；
- 发现跨维度冲突并在 Curator Audit 中报告。

#### 不负责

- 重写长期剧情；
- 重新当 Director；
- 为了“更完整”恢复全部上下文；
- 把 Writer 重新淹没在规划语言里；
- 为了把“资源/机会/资格”写具体而自行发明上游从未定义的物品、价格、制度、待遇或能力规则。

当前系统使用 deterministic Index-first prefetch，目标是降低 token 和认知负担，而不是给 Curator 再增加工具调用。

**Scene Craft 的研究深度与章节带宽分离。** 原著 bounded evidence、书名、locator 与完整 Deep Craft 可以越来越深，但 production Writer 不直接消费它们。新增 Scene Primary 只有在 Reading Question、持续状态、beat engine、Stop/Handoff 都真正不同，且“现有 Skill + compact conditional”的 A/B 仍不足时才允许 promotion；高频、重要或研究预算高本身都不是扩 taxonomy 的理由。当前 production 冻结为 24 个 Primary；`character_voice_pressure / world_entry_lived_texture / desire_temptation` 只作为 Shared Reference Lens，不进入 Router；只有 `social_bargain_decision / relationship` 的 Revision Watch 已通过直接 Reviser A/B。

在长历史场景中，Curator 已识别的未解事实还会被 runtime 确定性投影成一个很短的 `UNRESOLVED FACT BOUNDARY`，紧贴 Chapter Mission 交给 Primary。它不新增 LLM Call，也不扩大 Canon schema；只是把“仍未知 / 未兑现”的事实边界提高显著性。

---

### Primary Writer：只写小说

#### 负责

- 把 Director Contract + Curated Context 写成完整、可保存的正式正文；Primary 不直接读取完整 Scene Skill / 原著 evidence，只消费 Curator 已编译的短 `Scene Prose Projection`；
- Future 10 当前章明确批准的 `结果 / 状态变化` 已确定性并入 Frozen Mission；力量/身份跨档、持有关系和其它不可逆里程碑必须成为正文事实，不能只用“打出该级战绩 / 接近 / 获得资格 / 被重新估价”等暗示替代；若 Canon 真使结果不可能，只接受 Director 的 `[PLAN OUTCOME ADJUSTMENT]` 显式调整；
- Reader-First：先让读者理解人、问题和 stakes，再给最低限度规则；
- 当动作自然提出“这是什么 / 为什么重要”的问题，而 Curator 已投影当前 Plan 排程的 World fact 时，用 1—3 个短直接旁白段或等价场景表达回答到足够后立刻回场景；**已排程 Reader Release 是本章需要兑现的 timing decision**，不是可选装饰。若该事实同时说明地点/势力/传承为什么值得争，保留一个最短价值锚点；Writer 不自行从完整 World 选择说明主题；
- 决定已经成立后的普通实施优先一句或短段概括，不靠实施流水账填充低动作章节；
- 让人物反应、力量结果和现场变化承担信息；Curated Context 已明确带入身体吸引、审美、虚荣、钱、享受、偏心、好奇等私人欲望且场景自然触发时，至少让一次注意力、身体反应、靠近/回避、想要或短期选择把它留在 POV 中，不自动净化成职责合作或“正确但克制”；
- 用少量 story-bearing detail 增加画面与人物存在感，而不是用修饰词堆积制造“丰富”；
- 把 Canon / Curator 明确标记为 unknown / unresolved 的旧事实继续保持为未知；只有 Director Contract 明确规定本章新成立的事实才可在正文中落成 Canon；
- 保持小说声音，而不是工作报告声音。

#### 不负责

- 重新规划章节；
- 输出 Audit、Fact Summary、状态更新；
- 解释自己为什么这么写；
- 为上游错误剧情方向做结构性救援。
- 为让场景“完整”而补写长期谜团的过去经历、旧对话、隐藏动机、人物既有知识或持久世界机制。

Writer 的目标是“写小说”，不是维护 pipeline bookkeeping。 正文目标不是越短越好，而是**克制但不干、丰富但不腻**：细节密度跟随故事价值，修饰密度不替代具体性。`Story-bearing Texture v1` 已通过 2026-08-24 五场景冻结 A/B（两个独立盲评合计 9:1）并作为当前正文基线冻结；战斗细节仍以决定性 beat、身体后果和对手反应为主，不借“丰富”恢复机制拆解。

`Long-History Fact Boundary v1` 也已通过 Chapter 120 / 600 冻结 A/B：Director 用现有八字段明确“本章新成立事实 / 仍未知事实”，runtime 再把 Curator 的未解事实确定性提升到 Primary 前部；最终压力样本中，两个章节都不再把核心 unresolved 谜团补成 retrospective canon。该方案优先于新增 Character Agent、Continuity Reviewer、Knowledge Matrix 或全量历史上下文。

---

### Authority Reviser：恢复远端权威，但只做局部手术

Primary 为了保持注意力集中，只吃 Director Contract、Curated Context 与必要连续性；这会降低写作负担，也会让一些**远端但更准确**的 World / Power / Human 信息在第一次 realization 中被压缩掉。Authority Reviser 专门解决这类“压缩损失”，不重新决定剧情。

#### 负责

- 以 Primary Draft 为唯一底稿，**Preservation First**：没有明确问题的句段默认逐字保留；
- 同时读取冻结 Mission、Curator、safe World Authority、逐条 Reader Release、Frozen Power + Human Core、Canon；若当前 Scene Skill 有经过 A/B 证明安全的一行 `Revision Watch`，只追加该 failure-triggered 提醒，不把完整 Generation/Revision Lens 塞回 Reviser；
- 删除/压缩反复确认、重复证明、工程化/程序化 Supporting Implementation 和 Competence Filler；
- 补回 Authority 已批准但第一版遗漏的最短充分 World Orientation、Core Power 独有体验、Human 私人 cue 或一个真正承载故事的生活细节；Frozen Mission 中的上游计划结果若明确批准“进入 / 踏入 / 晋升 / 突破 / 成为”某个里程碑，不能以战绩或氛围暗示代替一次直接落点；
- 把笔墨从普通实施还给本章真正的 World Entry / Rival / Relationship / Core Fantasy / Choice / Payoff / Consequence。
- 同一维度若 Curator / Primary 与 Frozen Mission / Canon / safe World / Frozen Power / Frozen Human 冲突，Frozen Authority 胜出；按语义扫描整章并清掉全部同义冲突，不只修第一处。
- 修冲突段落时逐句 salvage：本身合法、只错在时点/因果上的 Core Fantasy / Relationship / Desire / Payoff / Surprise / Social Repricing 迁到最近合法位置；salvage 不保护周围 process carrier，后者继续按 Attention Reallocation 压缩。

#### 不负责

- 重排 Chapter Mission、改变人物选择、胜负、资源得失、伤势、身份结果、Direct Result、State Change、Ending；
- 把远端欲望/计划/可能性升级成客观事实；
- raw GBrain 检索；
- 把全章重新润色一遍。

删除程序载体时，先判断是否同时承载新的 `State Change / Social Repricing / Reward / Relationship Change / New Desire / Next Opportunity`；若会，就只能压缩实施，不能删除 Consequence。

**显式里程碑 Outcome Fidelity 是低频条件机制，不是新常驻 Agent。** Run Ledger 只在计划以“进入 / 踏入 / 晋升 / 突破 / 成为”明确批准当前章里程碑、第一次 Authority Revision 却仍未直接落成时，才把同一个 Reviser 收窄为一次 Preservation-First `Outcome Repair` retry。普通章节零额外调用；repair 只补最小合法因果与一次直称，不改事件、胜负、资源、伤势、关系、Ending 或未知边界；最多一次，第二次仍漏则节点保持 failed，`final_source` 不成立，State 不运行。网页 UI 与 Codex External apply 都服从同一 Run Ledger 状态。

**增量恢复优先复用 exact-input receipt，而不是重新调用同一个模型。** Workflow 仍按 Authority 依赖把 future run 标 stale；随后各节点重新构建自己的 bounded Prompt。若 exact Prompt digest 与该节点已保存 Response 的输入 receipt 完全一致，且 Response body digest 未变，则该 Response 仍是当前节点的有效产物，Run Ledger 直接恢复节点，不再调用 LLM；任一字符变化或显式 retry 都正常重跑。这优化 author edit / stale recovery 的 critical path，不改变第一次生成链，也不把“近似相同”当成“相同”。

当前默认使用 GPT-5.6 Luna high。五档同输入对照中，medium Preservation 更高但存在 Reader Release coverage 漏项；high 首次在四类压力样本上全部通过关键 authority 检查；xhigh/max 没有补偿性收益。模型选择是 Current Default，不是 Stable Principle。

---

### State Extraction：只记录已经发生的事实

#### 负责

- 从正式正文提取 Active Scene State；
- Persistent Canon；
- Recent Summary；
- Open Promises；
- 必要的关系、资产和主动目标变化。

`PERSISTENT CANON` 在真实需要时维护少量语义小节：`Power / Capability`、`Active Relationships`、`Identity / Access`、`Knowledge / Enemy State`、`World State`、`Tracked Assets`。这不是新数据库：只有以后仍会改变选择的事实才留下。`Power / Capability` 承载后续 Power Delta；`World State` 只承载已经发生、未来 protagonist-blind World Expansion 需要知道的世界级变化。

#### 不负责

- 判断正文写得好不好；
- 重新解释人物动机；
- 从最近几章行为推断 Human Development；
- 修改规划；
- 补写正文中没有发生的事实。

State Extraction 越轻越好，优先使用更快、更便宜的模型，只要事实抽取正确。默认 `curator_primary` 后端从 Run Ledger 的 `final_source` 重读正式正文，Primary 草稿不能旁路进入长期 Canon。

---

### Review：只调整未来，不修改过去

十章 Review 用于检查：

- Core Fantasy 是否仍然明显；
- 一级成长是否仍然是主轴；
- Plot Engine 是否开始机械重复；
- 关系与敌人是否仍在产生新选择；
- 世界是否开始程序化；
- 下一阶段是否需要换挡。

Review 只调整未来计划，不自动重写已完成正文，也不推翻作者已经批准的核心 Fantasy。

若当前 Story Program 的 `World Horizon Handoff` 已经触发、或会在下一批中触发，Review 只规划到触发章即停止；下一动作是 `World Expansion → Current Character → Story Refresh → Outline`。Review 不从侧门替未知下一世界补满十章。

---

## 4. 权威与批准边界

创意链的权威顺序是：

开书时：

`作者明确要求 > 已批准 World Vision > 已批准 Power / Human（Character）> 已批准 Story Program > Outline > Director > Writer`

进入长期向前演化后：

`作者明确要求 > World Root + 已批准 Forward World Expansions > Current Character（Frozen Origins + 已发生 Delta）> 已批准 Refresh Story Program > Outline > Director > Writer`

`CURRENT_CHARACTER.md` 是确定性投影，不高于其来源 Canon / Frozen Origins；World Expansion 只对 `effective_from` 之后生效。已完成章节事实永远不会因为新 World / 新 Program 被回写。

模型生成、模型选择和作者编辑本身都不等于批准。作者明确批准才进入下一层权威链。

下游可以具体化上游，但不能静默替换上游承诺。

例如：

- Story Program 可以改变地图和敌人，但不能把“突破世界边界的自由”改成“路线经营”；
- Outline 可以发明具体人物和事件，但不能把 Program 的“势力争夺主角本人”改成“连续五章运输任务”；
- Director 可以压缩实现过程，但不能改变 Outline 已规定的结果；
- Writer 可以选择最自然的叙述方式，但不能重新规划结局。

---

## 5. 项目最怕的退化模式（Anti-Goals）

TGN 最怕的不是某一章偶尔写差，而是系统逐层把“令人向往的故事”转换成流程、资产、责任、数据库和模板。下面这些是方向红线，不是新的 Hard Gate；发现问题时优先修最早发生语义坍缩的上游层。

### 5.1 Ability → Job / 蓝领职业化

核心能力逐渐变成探路、检测、维护、运输、生产、研究或管理等职业技能。主角越来越专业，却没有越来越自由、强大或拥有更高世界位置。

### 5.2 Fantasy → Asset / Build / System

力量复利被误解为路线、权限、节点、库存、组合、领地或生产能力越来越多，最后读者记得系统结构，却说不出主角这阶段到底做成了什么令人向往的事。

### 5.3 Supporting Logic → Governance / Duty

世界风险、对手理由或组织逻辑本来只用于让冲突可信，却被模型继续推演成“主角力量越大，就越应该负责管理、审核、分配和维持秩序”。复杂世界可以保留，但 Opponent Rationale 不自动成为 Authorial Truth，更不自动成为 Protagonist Duty。

### 5.4 Verification → Procedure

为了证明能力可信，把真实故事拆成观察、分析、测试、验证、调整、再测试。能力优先在有明确欲望、风险和结果的真实行动中证明；没有新选择、冲突或反转的验证过程应压缩。

### 5.5 Plot Engine Repetition

相邻剧情块只是更换地图、敌人和任务名，底层仍是同一个“问题→分析→步骤→结算”，或“更大的封锁→更大的越界→更大的封锁”。长期成长应迫使目标、敌人策略、关系和世界问题发生变化。

### 5.6 Character → Tool / State Update

配角只负责提供信息、发任务、被救、改变态度或给主角结算收益，没有自己的欲望、拒绝、离开、选择和回流。角色应该能在主角视野外继续生活，并带着新状态重新进入主线。

### 5.7 Payoff → Tax

每次胜利、突破或获得刚兑现，就立刻补一个同量级代价、责任、审查或长期负担，导致爽点被系统性抵消。代价可以存在，但不能成为每次 Payoff 的固定税；先让胜利真实成立，再决定是否需要余波。

### 5.8 Planning / Database Language → Prose

正文开始出现“阶段收益、验证、闭环、资源网络、路线控制权”等策划或数据库语言，人物不像人在活，而像在维护规划状态。Planning 决定 WHAT；正文必须通过动作、对白、感知和结果承担这些意义。

### 5.9 Prose Collapse：Too Dry ↔ AI Ornamentation

一端是过度克制，正文只剩事件骨架、人物反应和现场质感不足；另一端是为了“丰富”堆形容词、副词、泛化比喻、五感清单、整齐排比、泛化金句、反复“不是 X 而是 Y”和同义情绪解释，AI 味明显。目标是 **Story-bearing Texture > Decorative Density**：克制但不干，丰富但不腻。

### 5.10 System Serves Story → Story Serves System

为了修质量不断增加 Agent、Reviewer、Hard Gate、评分器、完整人物数据库、事件图、连续性账本和全量上下文，最后 LLM 主要在维护系统而不是创造小说。Index-first、薄状态投影和少量深规则优先；不要重回 Hard Gate hell。

### 5.11 GBrain / Reference Overreach

参考库从“少量创作提醒”升级成创意权威，导致不同书越来越像同一套蒸馏模板，或 raw reference 继续泄漏到 Writer。World / Power / Human / Story Program / Outline 只读各自职责内的少量 focused inspiration；章节 Runtime 不直接读取 raw GBrain。

---

## 6. 出现质量问题时怎样定位

不要首先问“Writer 为什么写差了”，而是沿链条找第一次语义坍缩的位置：

`World Root / Expansion → Power / Human / Current Character → Story Program / Refresh → Outline → Director → Curator → Writer`

例如“看见别人看不见的路”最后变成承重、塌方、搬运：

- 如果 Story Program 已经写成“建立路线网络”，根因在 Program；
- 如果 Program 是“打破宗门封锁”，Outline 却连续设计取货任务，根因在 Outline；
- 如果 Outline 是人物权力争夺，Director 却把主角行动写成施工步骤，根因在 Director；
- 如果 Director 很清楚，Writer 仍花大量篇幅解释物理过程，才是 Writer/Reader-First 问题。

原则：**修最早发生的语义坍缩，不在最后一层无限加补丁。**

---

## 7. 效率原则

系统目标不是“调用最多的模型得到最高质量”，而是让高推理成本集中在高杠杆决策上。

当前章节默认链：

`Director → Curator → Primary Draft → Authority Reviser → lightweight State Extraction`

即 4 个主要生成调用 + 1 个轻量状态抽取，不默认运行 Specialist / Integrator。Reviser 的存在是为了把“Primary 窄上下文”和“远端高权威准确性”解耦，不是为了再写一次全文。

Long-form Evolution 不进入每章成本。World Expansion 只在真实 World Horizon / 新独立副本入口运行；Human Development 更低频且允许 `NONE`；Current Character 纯确定性；Story Refresh 只在扩世界后使用 Sol high 做一次高杠杆 Re-Collision。这里允许增加少量周期 Agent，因为 A/B 显示 fresh-context 分权明显优于单 Agent 全包，但不把它们升级成每章 Reviewer/Coordinator。

确定性工作优先本地完成：

- Index-first context prefetch；
- Open Promise 压缩；
- Recent Summary 压缩；
- 状态结构写回。

不要为了省一点本地代码，把简单筛选重新交给 LLM；也不要为了“保险”给每个阶段都上最慢模型。

延迟优化也遵守 root-cause layering：先区分正常采用链与废弃重跑/周期 Review/Repair 的真实摊销，再区分 deterministic context、模型推理与排队波动。不能用“最终稿和 Primary 很像”证明 Reviser 冗余，也不能用“中间包标题完整”证明降 effort 后最终正文等价。冻结上游、单变量运行，并把 treatment 接回正常下游；只有最终正文同时通过商业读感与 Authority/Canon 盲评，才允许改变 production 路由。涉及随机稀疏修订、条件路由、提前编译或跨章投机时，还必须报告**完整下游 critical path**、独立重复运行、跨书泛化、fallback/丢弃成本与 Reader↔Authority 分裂；子节点快不等于整章快，一次胜出不等于稳定 route。替换成另一强模型也服从同一标准：Full Curator 攡为 Terra high 虽在四章完整下游中快26.9%，但 Reader 与 Authority均2:2，不能按平均速度改默认。2026-08-29 的两轮实验已否决 full/patch medium Reviser、Slim/medium Curator、Conditional/Speculative Director、Parallel Pre-Curator、Authority Blueprint、Attention Kernel、Reviser+State 合并、State Terra low、Paragraph Manifest 与常驻 Reader Polish 作为质量等价默认。Paragraph-Delta 是唯一保留的高潜研究：它证明全文重输可被局部操作替代，但两次独立运行只有1/5完全一致，跨书 Reader 与 Authority仍分裂；下一步需要 deterministic Atomic Chapter Obligations，不再增加一个 LLM classifier。确定性删除 stale context 可以冻结；模型、effort、输出协议、并行语义或新 Agent 继续属于实验假设。

Atomic 的稳定方法论进一步收敛为“**Authority Contract 与 Primary Preservation Map 分离**”。Hard Contract 只能由可信结构化 Frozen Authority artifacts 与 Entity Registry 合并产生；Curator / Primary 只做 Runtime签发的 realization location 与 edit locality，不能创建Fact、Conflict或Identity。商业价值默认通过锁住blocker窗口外正文保护，只有editable window本身承载已成功价值时才使用窄fragment hint。Unsupported chapter必须绕过Atomic走当前Full；supported Full才可post-gate。自由文本verbose/compact/micro Sidecar已经否决；下一步只能测试单一语义源的native structured Director。静态fixture、schema valid与Authority更强都不能替代真实模型Story blind、跨书coverage、repeat和完整fallback-adjusted E2E。

---

## 8. 当前模型与 GBrain 路由（基于实测，不是方法论硬依赖）

模型选择按**阶段职责**，不是按“谁最强就全链使用谁”。当前证据最充分的规划配置是：

| 阶段 | 默认模型 | GBrain | 说明 |
|---|---|---|---|
| World Vision | GPT-5.6 Luna high | **ON，固定 1 条 Coordinate Reference + 最多 3 条 creative inspiration** | protagonist-blind World；固定坐标参考不占 creative 名额，不读取未来 Power/Human |
| World Expansion | GPT-5.6 Luna high | **ON，World-only craft + Coordinate Reference** | 低频、protagonist-blind；只向前扩当前 World Horizon；不读 Current Character / Power Stack / Human / Future Story |
| Power Seed | GPT-5.6 Luna high | **ON，固定 1 条 Naming Craft Reference + Power lane 小 bundle** | 只看 POWER_BASELINE；决定 growth grammar，不看 Human/Story Opportunities；固定命名参考不占 creative 名额 |
| Human Seed | GPT-5.6 Luna high | **ON，Human lanes，最多 3 条** | Appetite / Behavior / Relationship 各最多 1 条；不看 Power/named Story Opportunities |
| Human Development | GPT-5.6 Luna high | **OFF** | 可选慢时钟；只看 Frozen Human + 已发生 Canon；允许 `NONE`，不看未来 World / Story |
| Current Character | deterministic | OFF | 合并 Frozen Origins + 已发生 Power/Human/关系/身份/资产/知识，不调用 LLM |
| Mystery Decision Surface | GPT-5.6 Luna high | **OFF** | 低频；只判断 DEFER / Smallest Decision，不给答案 |
| Mystery Reframe Forge | GPT-5.6 Luna high | **OFF** | 低频；R1/R2/R3/D0，Non-Canon，作者选择 |
| Mystery Canonization Compiler | GPT-5.6 Terra high | **OFF** | 低频；只审 Canon 兼容、Smallest Decision 与新 Still-Open，不评分/修稿 |
| Story Program | GPT-5.6 Sol high | **ON，最多 3 条 focused inspiration** | Collision + long-form causality；最高杠杆长期结构节点 |
| Story Refresh | GPT-5.6 Sol high | **ON，最多 3 条 focused inspiration** | Effective World × Current Character 的周期性 fresh Re-Collision；如有 Fixed Hidden Mystery，可 planning-only 编译 reader-facing Reveal Contract |
| Outline | GPT-5.6 Luna high | **ON，通常 4 条，最多 5 条** | 把批准 Program 编译成中期故事锚点与 Future 10 |
| Director | GPT-5.6 Luna high | 章节相关精选上下文 | 当前 production 默认；模型/effort 切换只做显式下游 A/B |
| Curator | GPT-5.6 Luna high | raw GBrain OFF；Index-first + Scene Skill v2 compact Catalog | 编译短 `Scene Prose Projection`，允许 `NONE`；medium/Terra 路由尚未证明质量等价 |
| Primary Writer | GPT-5.6 Terra high | raw GBrain OFF；只吃短 Scene Projection | 先完成完整第一版正文；不直接读完整 Skill；不是默认 final source |
| Authority Reviser | GPT-5.6 Luna high | **OFF**；safe Authority + optional short Revision Watch | Preservation First；只在明确失败时局部修；默认 final source |
| State Extraction | GPT-5.6 Luna low | OFF | 只抽取最终正式正文已发生事实 |

### 为什么这样分

- **Terra**：这轮章节 A/B 中 wall-clock 通常最快、输出更克制；Primary 的优势尤其明显。但 Terra 单价显著高于 Luna，因此“更快”不等于“更便宜”。
- **Luna**：当前单价最低，也是规划链的默认综合主力；Director/Curator 质量足够且成本优势很大，但正文与 Curator 更容易输出偏长。
- **Sol high**：最强优势集中在几十/几百章的长期变异；单价最高且通常最慢，因此默认只放 Story Program / Deep Planning，不进入常规章节链。
- **Luna max**：不作为日常默认；只用于疑难创意救援、关键架构诊断和最高质量基线。
- **GPT-5.4 high**：当前没有相对 Luna 的补偿性优势，只用于回归或模型对照。

章节模型选择必须分开看 **生成质量 / wall-clock / 实际成本**。当前默认路由是 `Luna Director → Luna Curator → Terra Primary Draft → Luna high Authority Reviser → Luna State`。Terra Primary 是第一版正文行为选择；Luna high Reviser 是 authority-sensitive 局部修订选择。2026-08-29 最终正文双盲已否决 Curator medium/Slim、Reviser medium/Patch-only/Safe-Patch route 与 Conditional Director 作为质量等价低延迟默认；模型或合同切换必须重新通过正常下游与 Reader + Authority 双盲。Sol 不进入常规章节链。

### 已验证的 Theme Emergent A/B 结论（2026-08-25）

三本冻结作者方向、A=旧 production、B=只重划 Seed/World/Program 职责的真实模型 A/B，在统一剥离 ACP 辅助 metadata 后重新跑 6 个 Sol Story Program 与 3 个 Luna high blind judge，B **3/3 全胜**：A 平均 **4.57/10**，B 平均 **8.63/10**。

> 历史说明：这是 Split Character Authority 上线前的中间实验。它证明“语义提纯 / 世界能力同构”确实存在，但下面的 Seed/World/Program 生产化方案已被 2026-08-26 的 `World → Power/Human → Character → Collision` 架构取代；不要把本节当作当前 Runtime 链路。

实验支持的历史结论是：旧链路存在 `Fantasy Seed semantic escalation → World 能力/世界同构 → Story Program same-meaning-bigger-scale` 的“抽象意义提纯器”。当时的候选修法是：

- Seed 收敛到 Fantasy + Desire + Gameplay，不提前寻找能力的终极意义；
- World 先建立独立世界与 Desire Economy，再建立坐标，最后让核心优势切入；
- Program 让阶段由具体目标、人物、价值物、地点与冲突发动，并显式记录关键获得/占有/首次使用；
- Theme 只后验观察；
- Action Space / Expectation / Mystery / Impact 等高价值后台坐标继续保留并真实使用，但必须编译成具体故事事实。

完整实验见 `books/real-exp-theme-emergent-ab-20260825-v1/RESULTS.md`。实验也暴露 B 的新风险：三个偏武斗方向均容易收敛到战痕/技法采集家族，所以“去哲学化”不能代替 Seed 的玩法类型多样性；后续应继续用现有候选差异原则而不是重新引入主题驱动。

### 已验证的 GBrain A/B 结论

同一个“看见别人看不见的路”Fantasy Seed，完整跑 `World Vision(Luna high) → Story Program(Sol high) → Outline(Luna high)`：

- GBrain OFF 已经能产出合格规划；
- GBrain v3 ON 的主要增益集中在 **Story Program 与 Outline**：更早换 Plot Engine、人物更有自主目标、长中短线更完整、高价值获得更自然，并能把一个完整中期故事单位规划到约 60—70 章；
- ON 没有观察到明显的输出膨胀或可见延迟负担；
- 当前规划注入保持 **World 固定 1 Coordinate Reference + 最多 3 creative / Program 最多 3 / Outline 通常 4、最多 5**；不应因为 GBrain 变大就继续同步扩大最终上下文。规划检索采用 **wide recall, narrow context**：普通 creative 候选用互补 retrieval intents 扩覆盖，round-robin 去重后最多检查 12 个候选；World 的固定 Coordinate Reference 直接按 slug 读取，不参与 creative 排名或占位。

因此当前默认不是“让 GBrain 替模型想故事”，而是：**先让强模型拥有自己的创作，再用少量高质量 GBrain 提醒它不要忘记长篇还需要玩法换挡、线程生态、奖励复利和人物回流。**

### GBrain 蒸馏模型路由

GBrain 本身也不使用统一模型：

- Terra high：章节事实、Scene Evidence、Reward Event Evidence、Source Fidelity；
- Luna high：Book DNA、World Fantasy、人物/关系解释、Reward/Opportunity synthesis、Scene Skill synthesis；
- Sol high：Longitudinal Threads、Thread Braid、Story Program patterns、跨书高阶 synthesis。

简化理解：**Terra 看清事实 → Luna 理解吸引力 → Sol 理解长篇结构。**

快速试书或大量 A/B 可把规划链临时切到 Terra high；当 Story Program 明显机械、同一能力连续重复、人物自主性不足或作者明确要求 Deep Planning 时，优先只把 **Story Program** 升到 Sol，而不是整条链升级。

---

## 9. 接手项目时建议先看这些文件

1. `PROJECT_RULES.md` —— 项目执行规则唯一长期权威；
2. `docs/PIPELINE_METHODOLOGY_AND_VALUES.md` —— 分层方法论、Anti-Goals、Supporting Logic、模型职责；
3. `docs/MVP_PRODUCT_DIRECTION.md` —— 产品目标与创意权威；
4. `docs/SPLIT_CHARACTER_AUTHORITY.md` —— 当前 World / Power / Human / Character / Collision 权威边界；
5. `docs/GBRAIN_STORY_CRAFT_V3.md` —— GBrain 知识、ON/OFF 边界、规划/蒸馏模型路由；
6. `docs/CHAPTER_RUNTIME_AND_STATE.md` —— 当前章节链、Canon Memory、Run Ledger 与恢复边界；
7. `docs/NOVEL_PROSE_REALIZATION.md` —— Reader-First、Story-bearing Texture、Scene realization 与正文控制；
8. `docs/AUTHOR_WORKSPACE_UI_SPEC.md` —— 当前作者工作台的信息架构；
9. `src/story_mvp/prompts.py` —— 实际运行 Prompt 真源；
10. `src/story_mvp/chapter_context.py` / `hybrid_runtime.py` —— 当前确定性上下文投影。

如果要修改系统，先判断问题属于“创意语义、长期结构、中层事件、单章执行、正文实现、状态记忆”中的哪一层，再动对应文件。

---

## 10. 最后一个判断标准

一个健康的 TGN 规划，应该越来越容易用人物和结果复述：

> 谁想得到什么？谁不让？主角凭自己的核心优势做成了别人做不到的什么？这迫使谁重新选择？世界从此哪里不一样？

如果系统越来越容易用下面的语言复述，就说明正在退化：

> 新增了几个节点、权限、路线、模块、流程、资产、规则接口，然后下一阶段把它们组合起来。

前者是故事复利；后者只是系统复利。
