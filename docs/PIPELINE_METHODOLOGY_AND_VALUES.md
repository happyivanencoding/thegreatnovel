# Story MVP 分层方法论与价值观

> 这是“接手项目先读”文档。目标不是描述每个 API，而是解释为什么系统要分这些层、每层负责什么创造性责任、什么问题应该在哪一层修，以及哪些方向是产品明确不希望退化成的东西。

## 1. 一句话理解整个系统

Story MVP 不是“让一个大模型从设定一路写到正文”的流水线，而是把不同尺度的创作问题拆开，让每一层只解决自己最擅长的问题：

`Fantasy → Agency → Relationship Reconfiguration → Narrative Compounding → Story Anchors → Chapter Execution`

对应实际链路：

`作者粗方向 → Fantasy Seed → World Vision → Story Program → Outline → Director → Curator → Primary Writer → State Extraction`

其中最重要的原则是：**越靠上游，越决定“这本书是什么”；越靠下游，越只负责忠实执行已经确定的故事。**

如果下游正文出现系统性偏差，优先检查最早发生语义坍缩的上游层，不要默认继续给 Writer 增加规则。

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
- 敌人和世界为什么会随着主角成长改变反应。

#### 不负责

- 重新发明核心幻想；
- 提前决定长期剧情；
- 把未知一次解释完；
- 把长期积累整理成构筑、库存、权限树、路线网络。

#### 判断是否健康

World Vision 应让能力“更有世界感”，而不是把能力变成一个更完整的系统产品。

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
- 每个阶段的 Fantasy Proof、一级成长、收益与反哺、下一块推动。

#### 不负责

- 把 100 章全部写成精细施工步骤；
- 把每个锚点拆成“观察、分析、验证、执行”；
- 重新发明 Story Program；
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

#### 不负责

- 生成世界观；
- 重做几十章 Story Program；
- 拯救一个已经工程化的长期大纲；
- 把“主角行动”写成完整施工清单。

Director 的核心问题不是“这一章还能安排什么任务”，而是：

**谁想得到什么？主角凭核心优势完成了别人做不到的什么？这让谁的选择、利益、地位或行动空间发生了什么变化？**

---

### Curator：决定 Writer 真正需要看到什么

#### 负责

- 从大量 Canon / Book Contract / Inspiration / Scene Skill 中筛选当前章真正相关信息；
- 保留人物欲望、关系、力量、风险、承诺与当前冲突；
- 压缩不必要的规则和机制说明；
- 发现跨维度冲突并在 Curator Audit 中报告。

#### 不负责

- 重写长期剧情；
- 重新当 Director；
- 为了“更完整”恢复全部上下文；
- 把 Writer 重新淹没在规划语言里。

当前系统使用 deterministic Index-first prefetch，目标是降低 token 和认知负担，而不是给 Curator 再增加工具调用。

---

### Primary Writer：只写小说

#### 负责

- 把 Director Contract + Curated Context 写成完整、可保存的正式正文；
- Reader-First：先让读者理解人、问题和 stakes，再给最低限度规则；
- 让人物反应、力量结果和现场变化承担信息；
- 保持小说声音，而不是工作报告声音。

#### 不负责

- 重新规划章节；
- 输出 Audit、Fact Summary、状态更新；
- 解释自己为什么这么写；
- 为上游错误剧情方向做结构性救援。

Writer 的目标是“写小说”，不是维护 pipeline bookkeeping。

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

## 5. 最常见的退化模式

### 5.1 Ability → Job

核心能力逐渐变成职业技能：探路、检测、维护、运输、研究、管理。

症状：删掉操作过程以后，章节几乎没有人物冲突和不可逆变化。

### 5.2 Fantasy → Asset System

力量复利被误解为资产越来越多：路线、权限、节点、库存、领地、生产能力逐渐组成系统。

症状：读者记得系统结构，却说不出主角这阶段到底做成了什么令人向往的事情。

### 5.3 Plot Engine Repetition

相邻剧情块只是更换地图、敌人和任务名，底层仍是同一个“问题→分析→步骤→结算”。

### 5.4 Relationship as State Update

配角只负责提供信息、发任务、改变态度，没有自己的欲望和行动。

### 5.5 Planning Language Leakage

正文开始出现“阶段收益、风险、验证、资源闭环、路线控制权”等策划语言，人物不像人在活，而像在维护规划状态。

### 5.6 Over-gating

为了解决质量问题不断加入评分器、Hard Gate 和 Agent，最终 LLM 的认知资源都用于满足合同，而不是创造故事。

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
| World Vision | GPT-5.6 Luna high | **ON，最多 3 条 focused inspiration** | Luna 擅长把核心幻想抽象成世界欲望、世界入口与力量体验 |
| Story Program | GPT-5.6 Sol high | **ON，最多 3 条 focused inspiration** | 当前最值得使用 Sol 的位置：玩法换挡、长线生态、人物自治、敌人策略、高价值获得 |
| Outline | GPT-5.6 Luna high | **ON，通常 4 条，最多 5 条** | 把正确的长期 Program 展开成连续故事锚点、Thread Collision、身份揭露、Reward Recontextualization |
| Director | GPT-5.6 Luna high | 章节相关精选上下文 | 负责当前章事件合同与 Narrative Salience，不重新设计长期故事 |
| Curator | GPT-5.6 Terra high | Index-first 后的少量相关材料 | 任务偏筛选、压缩、去 planning leakage，不需要最慢模型 |
| Primary Writer | GPT-5.6 Luna high（暂定） | 只读 Curator 输出/Scene Skills | 正文模型尚未完成严格 Terra/Luna/Sol 同输入盲测，不能把规划结论直接外推到 prose |
| State Extraction | 更快、更便宜的模型；GPT-5.6 系列时优先 Terra | 不需要创作型 GBrain | 只抽取已发生事实，reasoning 使用满足正确性的最低合理档位 |

### 为什么这样分

- **Terra high**：快、直接、克制，适合事实抽取、Scene/Reward Evidence、Source Fidelity、Curator，以及大量快速 A/B。它擅长“看清发生了什么”。
- **Luna high**：当前最佳综合主力。擅长核心幻想抽象、复杂约束下的稳定规划和把正确 Program 展开成具体故事。它擅长“理解为什么好看，并可靠执行”。
- **Sol high**：最强优势集中在几十/几百章的长期变异：人物自主性、关系回流、对手策略、同一能力换 Plot Engine，以及把资产重新转回人物/世界后果。它擅长“理解为什么很久以后仍然好看”。由于明显更慢，不默认贯穿全链。
- **Luna max**：不作为日常默认；只用于疑难创意救援、关键架构诊断、最高质量基线或明确要求最大推理深度的重构。
- **GPT-5.4 high**：当前实测中比 Luna high 更慢，幻想抽象和输出稳定性没有补偿性优势，也更容易出现系统/Build 语言；当前不设默认 niche，只用于回归或模型对照。

### 已验证的 GBrain A/B 结论

同一个“看见别人看不见的路”Fantasy Seed，完整跑 `World Vision(Luna high) → Story Program(Sol high) → Outline(Luna high)`：

- GBrain OFF 已经能产出合格规划；
- GBrain v3 ON 的主要增益集中在 **Story Program 与 Outline**：更早换 Plot Engine、人物更有自主目标、长中短线更完整、高价值获得更自然，并能把一个完整中期故事单位规划到约 60—70 章；
- ON 没有观察到明显的输出膨胀或可见延迟负担；
- 当前 **3 / 3 / 4（最多5）条** 的 focused inspiration 已经有效，不应因为有效就扩成每层十几张卡。

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

1. `docs/PIPELINE_METHODOLOGY_AND_VALUES.md` —— 先理解系统为什么这样分层、Supporting Logic 原则和模型职责；
2. `docs/MVP_PRODUCT_DIRECTION.md` —— 产品目标与 Fantasy-first 边界；
3. `docs/GBRAIN_STORY_CRAFT_V3.md` —— GBrain 四类知识、ON/OFF 边界、规划/蒸馏模型路由和当前 A/B 证据；
4. `src/story_mvp/prompts.py` —— 当前实际创作原则与各阶段 Prompt；
5. `src/story_mvp/chapter_context.py` —— Director / chapter context 的确定性投影；
6. `src/story_mvp/hybrid_runtime.py` —— Curator / Primary 的上下文边界与 Index-first；
7. `docs/READER_FIRST_PROSE_RUNTIME.md` —— 正文层如何避免设定说明先于读者理解；
8. `docs/CANON_MEMORY_V2.md` —— 记忆层只保存什么；
9. `docs/CHAPTER_RUN_LEDGER.md` —— 章节运行节点和保存边界。

如果要修改系统，先判断问题属于“创意语义、长期结构、中层事件、单章执行、正文实现、状态记忆”中的哪一层，再动对应文件。

---

## 10. 最后一个判断标准

一个健康的 TGN 规划，应该越来越容易用人物和结果复述：

> 谁想得到什么？谁不让？主角凭自己的核心优势做成了别人做不到的什么？这迫使谁重新选择？世界从此哪里不一样？

如果系统越来越容易用下面的语言复述，就说明正在退化：

> 新增了几个节点、权限、路线、模块、流程、资产、规则接口，然后下一阶段把它们组合起来。

前者是故事复利；后者只是系统复利。
