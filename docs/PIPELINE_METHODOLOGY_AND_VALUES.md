# Story MVP 分层方法论与价值观

> 这是“接手项目先读”文档。目标不是描述每个 API，而是解释为什么系统要分这些层、每层负责什么创造性责任、什么问题应该在哪一层修，以及哪些方向是产品明确不希望退化成的东西。

## 1. 一句话理解整个系统

Story MVP 不是“让一个大模型从设定一路写到正文”的流水线，而是把不同尺度的创作问题拆开，让每一层只解决自己最擅长的问题：

`Fantasy → Agency → Relationship Reconfiguration → Narrative Compounding → Story Anchors → Chapter Execution`

对应实际链路：

`作者粗方向 → Fantasy Seed → World Vision → Story Program → Outline → Director → Curator → Primary Writer → State Extraction`

其中最重要的原则是：**越靠上游，越决定“这本书是什么”；越靠下游，越只负责忠实执行已经确定的故事。**

如果下游正文出现系统性偏差，优先检查最早发生语义坍缩的上游层，不要默认继续给 Writer 增加规则。

### 系统问题必须在“生成事实的最早层”解决

判断一个修复是不是系统修复，先问：**换一本完全不同的新书，这个问题还会不会重新出现？** 如果会，就不能靠某本书的 BOOK 补字段、某一章 Director 临时发明设定、Curator 改词或 Writer 兜底。应找到最早应该产生该事实的层，并在那里建立通用职责。下游可以忠实释放、选择、压缩和表达上游事实，但不能为了救当前样本创造本来应该由上游决定的世界规则。

例如：读者不知道谁强、晋升到底得到什么、核心金手指遇到高层对象会不会直接越级，这不是 Chapter 4 的局部问题，而是 World Vision 没有给下游足够的 Reader-Facing World Model；连续几章用同一能力、同一对手、同一反转，则优先是 Story Program / Outline 的玩法变异问题。修复目标不是“让这本实验书下一章正常”，而是“下一本新书从零生成时自然不会再掉进同一个坑”。

---

## 2. 核心价值观

### 2.1 Fantasy First

先回答“读者最想亲自拥有什么”，再回答世界、资源、势力和规则怎样承载它。

成熟男频成长长篇的一级主轴优先是：主角本人越来越能做什么、拥有怎样的力量、自由、生命状态、世界位置或命运主动权。

财富、装备、身份、关系、势力、领地、入口、资格等可以重要，但它们默认是承载和结算，不应逐步取代核心幻想成为故事本体。

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

关系重构不是万能定律，也不是 Hard Gate。探索、战斗、谜团、生存和世界奇观都可以是主发动机。它的价值在于让核心优势改变后续博弈条件，使新冲突自然生长，而不是不断安排“更大版本的同一个任务”。

### 2.4 Narrative Compounding > Asset Compounding

“复利”首先指故事不会回到原点，而不是资产种类越来越多。

优先看：

- 主角下一轮多能做什么；
- 对手以后必须怎样改变应对；
- 重要关系出现什么新的选择；
- 身份和世界位置发生什么不可回滚变化；
- 下一轮因此出现什么过去根本不会发生的冲突。

能力、装备、资源、关系、身份、领地等可以承载复利，但不要为了证明成长主动堆成路线网、权限树、库存、节点网络或组合系统。

### 2.5 Supporting Logic Must Not Automatically Become Story Engine

这是当前系统非常重要的一条统一准则。它把过去分别表现为“治理化、工程化、蓝领职业化、过度验证”的问题归到同一个根因：**LLM 看见一个合理问题以后，容易把“让因果成立”继续推演成“把这个问题完整解决”，最后 supporting logic 反客为主。**

必须持续区分：

- **World Complexity ≠ Narrative Focus**：世界可以复杂，某种风险或制度理由可以真实存在，但不自动成为作品主要讨论对象。
- **Opponent Rationale ≠ Authorial Truth ≠ Protagonist Duty**：对手可以有真实理由，甚至局部是对的；这首先用于制造冲突，不因为主角力量变大就自动推出“主角有义务管理所有人”。
- **Mechanism Reality ≠ Implementation Detail**：阵法、地形、规则、制作、技术过程可以存在，但只展开足以支撑当前人物选择和结果的部分。
- **Ability ≠ Occupation**：能力可以重复使用，但长期成长优先扩大主动权、敌人策略、关系、身份、机缘和世界入口，不自然职业化成探路、检测、维护、运输、生产或运营工作。
- **Verification Exists ≠ Verification Is The Story**：能力可信性优先嵌入有真实目标和利害关系的行动中证明，不单独搭建测试场景穷举机制与限制。

因此，“具体”优先具体在：谁想得到什么、谁阻止、主角决定什么、核心优势怎样改变局势、谁因此得到或失去什么、什么从此不可回滚。观察、分析、测试、验证、调整、实施如果没有新的关键选择、冲突或反转，就压缩到足以支撑因果的最小程度。

这条准则不是禁词表，也不禁止工程、经营、治理、研究等题材；如果作者明确选择这些题材，它们可以成为主发动机。关键是 **supporting logic 只有在本书真的把它选为主要阅读体验时，才升级为 story engine。**

### 2.6 Few Deep Rules > Many Hard Gates

旧系统的重要失败之一，是规则过多以后 LLM 开始优先维护 Schema 和门禁，而不是写故事。

因此默认策略是：

- 不为每个质量问题增加 Agent；
- 不为每个原则增加 scorer；
- 不把软创作方向改成逐项验收；
- 能用一条更深的原则修上游语义，就不要在下游叠更多补丁。

---

## 3. 每一层到底负责什么

### Fantasy Seed：决定“这本书最值得幻想什么”

#### 负责

- 核心幻想；
- 主角最强欲望；
- 非对称优势；
- 第一次标志性奇观；
- 长期增长发动机的原型；
- 早期兑现与远期升格方向。

#### 不负责

- 完整世界百科；
- 几十章大纲；
- 复杂成长网络；
- 操作规则手册；
- 为了平衡而机械添加成本。

#### 判断是否健康

一句话问：**读者是否会明确产生“我也想拥有这个”的欲望？**

如果 Seed 已经把能力写成职业流程、研究课题、管理系统，后面很难靠 Director 或 Writer 救回来。

---

### World Vision：让世界承载已批准的 Fantasy

#### 负责

- 世界为什么能让核心幻想持续成立；
- 力量、资源、阶层、地域、种族、宗门、王朝等怎样产生真实冲突；
- 世界奇观与力量上限；
- 地图扩大为什么意味着更高价值的新机会；
- 敌人和世界为什么会随着主角成长改变反应；
- **Reader-Operable World Rules**：会进入故事决策的世界规则，先落成“什么条件 → 什么可观察变化 → 人物因此能/不能做什么 → 结果怎样”的世界事实；抽象概念、象征与深层解释可以存在，但不能替代读者可预测的规则效果；
- **Reader-Facing World Coordinates**：当读者需要比较强弱、身份、危险、价值或进入权时，给出当前故事需要的最小可读尺度；可以是境界/段位/评级，也可以只是可观察的能力阈值、权限差或现实后果，不强迫每本书都有等级表；
- **Core Advantage ↔ World Compatibility**：明确核心优势真正复制/借用/改变/绕过的是什么，以及哪些效果仍受主角自身身体、能量、知识、材料、身份或环境约束；尤其要能回答“用在远高于当前层级的对象上会怎样”；
- 当组织、宗门、学院、职业或阶层晋升重要时，区分该层级的正常基础条件与真正稀缺、值得争夺的额外收益；如果世界故意不给基础条件，这本身必须是明确冲突；
- 当“资源”会推动剧情时，先定义世界里真实流通、花费、获得和争夺的具体对象及大致稀缺感，不要求提前写死每次数量。

#### 不负责

- 重新发明核心幻想；
- 为了显得完整而堆十几层境界、数值表、制度百科；
- 把每次奖励的精确数量和价格全部提前锁死；
- 提前决定长期剧情；
- 把未知一次解释完；
- 把长期积累整理成构筑、库存、权限树、路线网络。

#### 判断是否健康

World Vision 应让能力“更有世界感”，而不是把能力变成系统产品或抽象哲学。健康的 World Vision 既要给下游足够的**比较尺**，也要让核心规则能够被普通读者预测：概念名拿掉以后，仍然说得清“发生什么、为什么当前人物必须这样选、这件事做成/失败会怎样”。神秘感优先留在原因、来源和更深层世界，不要留在眼前规则效果本身。

---

### Story Program：决定“这本书为什么能写几百章”

这是长期规划链里最重要的高杠杆节点。

#### 负责

- 5—7 个自然大型阶段；
- 核心玩法怎样真正变异，而不是换地图重复；
- 敌人策略怎样升级；
- 重要人物怎样拥有自主目标并持续回流；
- 上一阶段结果怎样改变下一阶段的博弈条件；
- 关系重构；
- 世界和力量怎样自然扩大；
- 核心优势的**选择空间与反制**：如果乐趣来自选谁、选什么、何时使用、保留或舍弃，就让关键选择具有真实竞争性（Contestable Choice），避免题面预先把一个选项写成明显正确答案；不同选项可以因真实价值、信息不完整、时机或对手干预而难以简单排序，对手也可以隐藏、诱导、封锁、改变条件或逼主角提前消耗优势；不强制统一槽位/冷却模板，也不要求每次选择都附带惨痛代价；
- 核心幻想怎样保持不变量，同时产生不同的兑现形式。

#### 不负责

- 逐章列事件；
- 把长期成长整理成技能树、权限树、资产网络；
- 为了凑阶段强行升级世界尺度；
- 把同一 Plot Engine 重复六遍。

#### 最关键的问题

每个主要阶段后应优先问：

1. 主角现在多能做什么？
2. 谁因此不能再按原来的方式对待他？
3. 敌人必须怎样换策略？
4. 哪段关系出现过去不会有的新选择？
5. 下一阶段为什么会自然出现一种新的故事，而不是一个更大的同类任务？

Story Program 如果已经把“核心优势”降维成工作流、Build 或系统经营，Outline 只能把错误方向写得更好看，无法真正救回来。

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
- 每个阶段的 Fantasy Proof、一级成长、收益与反哺、下一块推动；
- **World Model Release**：作者知道 World Vision 不等于读者知道。开书前三章在相关冲突或爽点需要之前，通过事件让读者获得当前需要的强弱、身份、价值与能力边界；新造概念第一次影响选择时，先让读者看到触发、可见结果和行动含义，再允许名称或深层解释进入，不把正文写成设定说明；
- **Core Gameplay Variation**：第一次高光以后，尽快把“它能不能做到”推进成“为什么选这个对象/时机/用法、别人怎样反制、同一优势还能产生什么不同结果”；尤其不要让上一轮已经证明有效的解法自动解决下一轮主要问题，下一轮冲突优先攻击它尚未解决的对象、关系、资源、目标或条件，或迫使主角换一种用法。这样实现换挡，不要求机械让主角失败或每轮加新代价。

#### 不负责

- 把 100 章全部写成精细施工步骤；
- 把每个锚点拆成“观察、分析、验证、执行”；
- 重新发明 Story Program；
- 临时重写 World Vision 的力量尺度、身份基础逻辑或核心能力兼容边界；
- 把远期升格强塞进固定百章窗口。

#### 为什么需要故事锚点

如果 Outline 只写“这一阶段利用隐藏道路扩大优势”，Director 就必须自己发明中间事件，LLM 最容易选择可操作、可重复、逻辑稳定的任务：搬运、探路、验证、修复、调查。

Story Anchor 的作用是提前确定“真正的故事发生了什么”，降低 Director 自己发明低价值任务的空间。

---

### Director：决定“这一章到底发生什么”

#### 负责

- 根据已批准长期方向、当前剧情块、Future 10 和 Canon，生成当前章事件合同；
- 抓本章最值得读、最值得复述的人物冲突、关键选择、力量使用、反转和结果；
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

- 从大量 Canon / Book Contract / Inspiration / Scene Skill 中筛选当前章真正相关信息；
- 保留人物欲望、关系、力量、风险、承诺与当前冲突；
- 压缩不必要的规则和机制说明；
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

在长历史场景中，Curator 已识别的未解事实还会被 runtime 确定性投影成一个很短的 `UNRESOLVED FACT BOUNDARY`，紧贴 Chapter Mission 交给 Primary。它不新增 LLM Call，也不扩大 Canon schema；只是把“仍未知 / 未兑现”的事实边界提高显著性。

---

### Primary Writer：只写小说

#### 负责

- 把 Director Contract + Curated Context 写成完整、可保存的正式正文；
- Reader-First：先让读者理解人、问题和 stakes，再给最低限度规则；
- 让人物反应、力量结果和现场变化承担信息；
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

### State Extraction：只记录已经发生的事实

#### 负责

- 从正式正文提取 Active Scene State；
- Persistent Canon；
- Recent Summary；
- Open Promises；
- 必要的关系、资产和主动目标变化。

#### 不负责

- 判断正文写得好不好；
- 重新解释人物动机；
- 修改规划；
- 补写正文中没有发生的事实。

State Extraction 越轻越好，优先使用更快、更便宜的模型，只要事实抽取正确。

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

---

## 4. 权威与批准边界

创意链的权威顺序是：

`作者明确要求 > 已批准 Fantasy Seed > 已批准 World Vision > 已批准 Story Program > Outline > Director > Writer`

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

参考库从“少量创作提醒”升级成创意权威，导致不同书越来越像同一套蒸馏模板，或 raw reference 继续泄漏到 Writer。Fantasy Seed 默认保持 GBrain OFF；World / Story Program / Outline 只读少量 focused inspiration；章节 Runtime 不直接读取 raw GBrain。

---

## 6. 出现质量问题时怎样定位

不要首先问“Writer 为什么写差了”，而是沿链条找第一次语义坍缩的位置：

`Fantasy Seed → World Vision → Story Program → Outline → Director → Curator → Writer`

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

`Director → Curator → Primary → lightweight State Extraction`

即 3 个主要生成调用 + 1 个轻量状态抽取，不默认运行 Specialist / Integrator。

确定性工作优先本地完成：

- Index-first context prefetch；
- Open Promise 压缩；
- Recent Summary 压缩；
- 状态结构写回。

不要为了省一点本地代码，把简单筛选重新交给 LLM；也不要为了“保险”给每个阶段都上最慢模型。

---

## 8. 当前模型与 GBrain 路由（基于实测，不是方法论硬依赖）

模型选择按**阶段职责**，不是按“谁最强就全链使用谁”。当前证据最充分的规划配置是：

| 阶段 | 默认模型 | GBrain | 说明 |
|---|---|---|---|
| Fantasy Seed | GPT-5.6 Luna high | **OFF** | 保持核心幻想先由作者方向与模型自身产生，避免参考库过早锚定创意 |
| World Vision | GPT-5.6 Luna high | **ON，固定 1 条 Coordinate Reference + 最多 3 条 creative inspiration** | Coordinate Reference 固定提供力量/技法/威胁/身份/价值/行动空间等读者尺，不占 creative 名额；Luna 再用最多 3 条创作启发承载世界入口、复利与力量体验 |
| Story Program | GPT-5.6 Sol high | **ON，最多 3 条 focused inspiration** | 当前最值得使用 Sol 的位置：玩法换挡、长线生态、人物自治、敌人策略、高价值获得 |
| Outline | GPT-5.6 Luna high | **ON，通常 4 条，最多 5 条** | 把正确的长期 Program 展开成连续故事锚点、Thread Collision、身份揭露、Reward Recontextualization |
| Director | GPT-5.6 Luna high | 章节相关精选上下文 | 当前 Balanced 默认；与 Terra high 质量接近但成本显著更低，若优先最低延迟可切 Terra high |
| Curator | GPT-5.6 Luna high | Index-first 后的少量相关材料 | Balanced 默认；应继续压短输出合同。若优先最短延迟与更克制输出，可切 Terra medium |
| Primary Writer | GPT-5.6 Terra high | 只读 Curator 输出/Scene Skills | 正文 A/B 中更克制、较少 procedural expansion、更愿意在章节合同位置停下；这是质量/行为选择，不是成本选择 |
| State Extraction | GPT-5.6 Luna low | 不需要创作型 GBrain | 当前成本优先默认；只抽取已发生事实，不需要高级创作推理 |

### 为什么这样分

- **Terra**：这轮章节 A/B 中 wall-clock 通常最快、输出更克制；Primary 的优势尤其明显。但 Terra 单价显著高于 Luna，因此“更快”不等于“更便宜”。
- **Luna**：当前单价最低，也是规划链的默认综合主力；Director/Curator 质量足够且成本优势很大，但正文与 Curator 更容易输出偏长。
- **Sol high**：最强优势集中在几十/几百章的长期变异；单价最高且通常最慢，因此默认只放 Story Program / Deep Planning，不进入常规章节链。
- **Luna max**：不作为日常默认；只用于疑难创意救援、关键架构诊断和最高质量基线。
- **GPT-5.4 high**：当前没有相对 Luna 的补偿性优势，只用于回归或模型对照。

章节模型选择必须分开看 **生成质量 / wall-clock / 实际成本**。2026-08-23 的配对正文实验里，当前最推荐的 Balanced 路由是 `Luna Director → Luna Curator → Terra Primary → Luna State`；Terra Primary 是正文行为选择，不是成本选择。若优先更短延迟，可把 Director/Curator 切到 Terra high/medium；若质量优先且希望 Curator更精简，可只把 Curator切到 Terra medium。Sol 不进入常规章节链。

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

1. `docs/PIPELINE_METHODOLOGY_AND_VALUES.md` —— 第一权威入口：分层方法论、Anti-Goals、Supporting Logic、模型职责；
2. `docs/MVP_PRODUCT_DIRECTION.md` —— 产品目标、Fantasy-first 与作者权威边界；
3. `docs/GBRAIN_STORY_CRAFT_V3.md` —— GBrain 知识、ON/OFF 边界、规划/蒸馏模型路由；
4. `docs/CHAPTER_RUNTIME_AND_STATE.md` —— 当前 `curator_primary` 章节链、Canon Memory、Run Ledger 与恢复边界；
5. `docs/NOVEL_PROSE_REALIZATION.md` —— Reader-First、Story-bearing Texture、Scene realization 与正文控制；
6. `docs/AUTHOR_WORKSPACE_UI_SPEC.md` —— 当前作者工作台的信息架构；
7. `src/story_mvp/prompts.py` —— 实际运行 Prompt 真源；
8. `src/story_mvp/chapter_context.py` / `hybrid_runtime.py` —— 当前确定性上下文投影。

如果要修改系统，先判断问题属于“创意语义、长期结构、中层事件、单章执行、正文实现、状态记忆”中的哪一层，再动对应文件。

---

## 10. 最后一个判断标准

一个健康的 TGN 规划，应该越来越容易用人物和结果复述：

> 谁想得到什么？谁不让？主角凭自己的核心优势做成了别人做不到的什么？这迫使谁重新选择？世界从此哪里不一样？

如果系统越来越容易用下面的语言复述，就说明正在退化：

> 新增了几个节点、权限、路线、模块、流程、资产、规则接口，然后下一阶段把它们组合起来。

前者是故事复利；后者只是系统复利。
