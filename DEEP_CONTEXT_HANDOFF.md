# DEEP CONTEXT HANDOFF

日期：2026-08-27
项目：TheGreatNovel / TGN Story MVP
主要工作目录：`C:\dev\tgn-story-mvp`
开发分支：`principal_dev_new_sys`

---

## 0. Handoff Purpose

这是一份供全新 Agent 直接接手 TGN 项目的**最终融合版深层认知交接**。它不是聊天流水账，也不是当前代码文档的替代品。

本文件融合了此前两份独立 Handoff：`DEEP_CONTEXT_HANDOFF.md` 与 `DEEP_CONTEXT_HANDOFF_2.md`。融合不是简单拼接：重复内容去重；发生冲突时按“用户后续明确修正 → 当前 production/code/tests → 后续受控实验 → 长期稳定共识”的顺序取舍；第二份中新增但尚未冻结的研究方向被保留在 Open Questions / Experimental Hypothesis，而不会伪装成 Core Principle。

它试图迁移三类东西：

1. 这个项目真正想达到的读者体验与产品目标；
2. 经过长期纠偏形成的判断模型：为什么某种方案对，为什么一个表面相似的方案仍然错；
3. 截至 2026-08-27 的已验证结论、当前实现、并行工作状态与下一步实验。

使用方式：

- 开始任何 TGN 工作前，仍应先读根目录 `PROJECT_RULES.md`，再检查 live code、tests、`git status` 与用户本轮最新指令；它们的事实优先级高于本文。
- 本文优先传递**决策模型**。当技术实现变化时，不要机械维护本文所列的旧函数名、模型名或目录；应保留更高层目标和边界。
- 本文将 Stable Principle、Validated Conclusion、Current Implementation、Open Question 分开。不要把当前实现伪装成永恒原则，也不要把一次实验假说写成 production 事实。

### 可访问范围说明

本文基于当前对话可访问的长对话内容、项目级历史摘要、当前仓库文件、实际实验产物与当前工作树。部分更早消息在界面中以“Skipped”形式出现，无法逐字恢复；对这些历史只采用后来明确复述、已进入代码/文档或被实验重新验证的结论。本文不会伪造被截断消息的原文，也不会把无法确认的中间判断当作最终共识。

---

## 1. North Star

TGN 的目标不是“自动生成一个逻辑完整的故事”，而是生成一部具有顶级商业潜力的**成熟中文男频成长长篇**：

> 读者明确想拥有主角的力量、身体状态、行动自由、世界位置或其它主角级非对称优势；主角本人长期真实变强；他持续进入第一章时没有资格进入的力量层、人物圈层、世界层、真相层和选择层；与此同时，这个人仍有自己的欲望、情欲、关系、虚荣、好奇、享受、偏心和人生，世界也不是为了金手指搭出来的测试场。

个性化产品的更高目标是：

> **读者的人格不只改变主角口吻，而要真实改变选择、路线、关系、遭遇、错失、获得及最终长成怎样的强者。**

但这不能牺牲男频读者承诺。无论是哪种人格，主角都应保有强成长底盘：

> **Growth Floor, Route Freedom。**

即：成长下限稳定，成长路线开放。

理想的个性化因果链是：

> `Human → Choice → Route → Encountered Opportunity → New Power Asymmetry → Compound Growth`

不是：

> `人格标签 → 系统直接发放对应外挂`

也不是：

> `所有人格走同一升级树，只是升级速度不同`

TGN 最终应该做到：不同读者进入同一个好世界，都能获得强烈、持续、可比较的成长爽感；但他们因为不同选择，逐渐拥有不同的关系、际遇、优势栈和传奇形态。

---

## 2. Core Mental Model

### 2.1 读者价值、创意权威、长期因果和章节实现必须分开

TGN 的整体框架是：

```text
Reader Promise
    ↓
Independent Creative Authorities
    ↓
Character Collision / Long-Form Causality
    ↓
Story Scheduling
    ↓
Chapter Realization
    ↓
Canon / State Continuity
```

当前 production 对应：

```text
作者方向
→ protagonist-blind World Vision
→ POWER_BASELINE / LIFE_CONTEXT
→ 独立 Power Seed + Human Seed
→ 作者一次批准 Character
→ deterministic CHARACTER.md
→ Story Program（第一次完整 Collision）
→ 作者批准
→ Outline
→ Director
→ Curator
→ Primary Writer
→ State Extraction
```

越靠上游，越决定“这本书是什么”；越靠下游，越只负责忠实执行。下游不能为了救当前样本，临时发明本应由上游决定的世界规则、人物核心、长期能力或主线。

### 2.2 Split Authority 的根本目的不是流程美观，而是阻止后验合理化

旧式单模型 Seed 很容易同时决定：

> 世界是什么 → 主角是什么人 → 为什么他恰好拥有这个能力 → 世界为什么恰好奖励这种人格。

模型会把一切主题化、适配化，最后世界、能力和人格都像同一个抽象命题的不同写法。

因此当前系统把三份权威拆开：

- **World**：没有主角也成立；
- **Power**：相对世界正常力量，主角哪里拥有明显特权；
- **Human**：这个人原本是谁，完全不知道未来能力；
- **Story Program**：第一次允许它们碰撞，负责后果而不负责重写来源。

核心不是“多几个 Agent”，而是：

> **fresh context + information boundary + deterministic composition。**

### 2.3 TGN 真正防的是“合理性自动扩张”

LLM 的高频退化不是完全不懂故事，而是看见一个合理问题后，会继续把它完整解决：

> 需要解释世界 → 写成制度百科；
> 需要证明能力 → 写成测试流程；
> 需要人物能干 → 写成维修/诊断/路线小任务；
> 需要成长 → 每阶段填升级/奖励；
> 需要世界独立 → 写成治理与资源分配模型；
> 需要关系自治 → 写成所有人对称议价；
> 需要伏笔 → 所有秘密并成一个幕后真相。

所以最重要的统一原则是：

> **Supporting Logic Must Not Automatically Become Story Engine。**
> 支撑性逻辑不得自动成为故事发动机。

### 2.4 男频成长不是数值曲线，而是“力量—定价—入口—欲望”的反馈机器

《Bad Born Blood》《斗破苍穹》和多轮 TGN 实验最终指向同一个纵向结构：

> 力量/身体/优势真实变化
> → 更高层人物重新估价
> → 身份、关系、资源、敌策或世界入口改变
> → 主角看到更高层真正想要的东西
> → 获得过去没有资格作出的选择
> → 再进入下一轮成长。

这不是要求每阶段升级，而是要求整本书不断发生**主人公升格**。

### 2.5 人格与幻想不是二选一

错误二分法：

- 强调成长，就让所有人格都选择眼前最优升级；
- 强调人物，就允许主角长期不变强。

正确关系：

> **系统保证男频 Growth Floor；Human 决定路线、取舍、投入顺序、错失和优势树。**

一个力量第一的人可能留下参加试炼；一个具体关系能改路的人可能为某个人放弃同一试炼。二者都可以是好男频主角。区别不在于谁“更正确”，而在于选择是否来自冻结 Human，而不是来自新增结构原则覆盖人物效用函数。

---

## 3. Core Principles

以下原则已经经过长期讨论、纠偏或跨样本验证。除非出现强新证据，不应轻易推翻。

### 3.1 Fantasy First 是读者价值优先级，不是 production 阶段

TGN 应先保护：

- 我想拥有这项力量；
- 我想看他变强；
- 我想看他进入更高世界；
- 我想看世界如何重新对待他；
- 我想知道下一个更馋的东西是什么。

但不再用一个 Fantasy Seed 同时预先决定世界、能力、人物和命运。Fantasy First 决定质量优先级，Split Authority 决定创意因果边界。

### 3.2 Character is a person, not a psychological proof

人物不是一篇“童年如何证明人格”的论文。

正确结构：

> `生活事实 → 多股竞争动机 → 稳定选择偏向 → 具体关系改变选择`

错误结构：

> `先定一个核心执念 → 发明几段童年逐条证明 → 所有选择都回到同一句哲学`

真实人物可以同时想要钱、胜负、身体欲望、审美、享受、亲密、自由、面子、野心、报复、归属；这些动机不必被统一成一个高尚命题。情欲就是情欲，不需要净化成“深层精神连接”。

### 3.3 Stable Choice Bias + Variable Realization

人物辨识度不是固定招式、口头禅或每次反套路。

应让读者逐渐知道：

- 他通常保护什么；
- 拒绝什么；
- 会为何承担代价；
- 哪些人能改变他的风险阈值和路线。

但具体做法必须随现场信息、能力、关系和风险重新生成。核心可预测，手段不可机械预测。

### 3.4 Person-specific Relationship 必须改变选择

关系不是“他重感情”的形容词，也不是配角有几句自主台词。

成立标准：

> 原本按利益、安全、力量最优解会做 A；因为是某个具体的人，他实际做了 B。换成另一个同等有用的人，未必如此。

关系可以让主角留下、离开、暴露底牌、错过名额、改变力量路线或承担不划算风险。它也不要求关系永远压过力量；关键是具体人物有真实效用权重。

### 3.5 World Independence ≠ Governance Simulation

世界独立只要求：

- 没有主角也有人在追求具体东西；
- 有战争、争夺、迁徙、比赛、传承、奇观或未知在推进；
- 世界有真正值钱和值得进入的对象；
- 人物不是为了测试金手指而出生。

它不要求完整税制、公共治理、资源分配、维护责任和利益方平衡。世界可以强烈偏向核心幻想，充满强敌、宝物、秘境和奇观，只要它不被主角能力完全解释。

### 3.6 Authority Separation > Negative Prompt Accumulation

如果问题来自信息泄漏或后验适配，正确修法通常是拆权威、限制可见性或移动决策层，而不是继续往 Prompt 里加“不要”。

这也是为什么当前没有 Character Composer LLM，没有 raw GBrain 直达 Writer，也不让 Outline/章节临时发明长期优势。

### 3.7 Growth is longitudinal, not a stage/block/chapter tax

某个阶段可以没有：

- 境界突破；
- 新技能；
- 新装备；
- 新地图；
- Power Delta。

它仍可由关系、战争、身份、秘密、地点或选择完整成立。

但整本男频长篇不能没有真实成长。主角长期必须更能打、更能去、更能掌握、更能选择，并持续兑现核心幻想。

### 3.8 Plot Pace ≠ Tier Pace

故事可以快速推进：敌人变化、关系决裂、世界事件、获得、发现、换玩法都可以很快；境界不需要跟着狂升。

同一层级可以写多个完整剧情块，只要：

- 对手策略变了；
- 旧能力有新用法；
- 新优势加入；
- 社会位置变化；
- 世界入口扩大；
- 关系和欲望继续变化。

不要用升阶替代故事进展，也不要过早耗尽力量主尺。

### 3.9 Power Asymmetry 必须产生明确 Privilege Delta

金手指不能只是“更方便、更灵活、效率更高”。

合格能力必须能回答：

- 同层普通人通常只能做什么；
- 同层天才能做到什么；
- 主角独占、提前或低代价拥有哪种通常更高层才有的特权；
- 为什么读者明天醒来得到它会立刻想用。

Permanent Boundary 用来防万能，不是为每一点爽感配等价代价。能力必须保留明显纯收益区间。

### 3.10 设定创新 ≠ 术语创新 ≠ 机制复杂化

强能力应：

> 一句话大白话能懂 + 一个主异常 + 明显占便宜 + 后期可复合。

复杂和丰富应在几百章中由功法、装备、身体、环境、传承、新优势和敌人反制慢慢长出来，不应在第一章要求读者学习一套抽象哲学。

### 3.11 Power Asymmetry 要形成优势栈

开局 Core Asymmetry 继续成长，但全书不能只把同一能力从“小”放大到“大”。后续应通过真实故事获得新的非对称优势，并让新旧优势形成单项做不到的复合效果。

这是全书级要求，不是每阶段新增能力税。

### 3.12 World Ruler 是长期坐标，也是压缩器

力量、战绩、价值、天赋/适配、技熟、装备、排名、身份、世界层级都可以是尺。

尺的作用不是报表，而是快速让读者知道：

> 主角在哪档 → 同档普通人/天才怎样 → 主角哪里超标 → 下一档还有多远。

一次强比较应替代多轮验证。尺度必须在突破、新强敌、公开证明、装备变化或世界换挡时重新出现，不能只在 World Vision 介绍一次。

### 3.13 Proof once → Calibrate once → Consequence immediately

一个事实已经通过动作结果和一次足够的世界尺度校准成立后，不要换五种证据继续证明。

社会确认只有在会改变：

- 机会；
- 敌意；
- 关系；
- 身份；
- 资源；
- 行动入口；

时才值得继续占用篇幅。

同理，重大选择的选项与代价已经清楚后，应尽快选择，然后写选择造成的新局面，而不是继续证明“这个人物为什么会这样选”。

### 3.14 Social Proof 的核心是重新定价，不是围观震惊

好的公开证明是：

> 既有尺度 → 超标结果 → 有利害关系的人重新估价 → 待遇、挑战规格、资源、资格、敌策或关系发生改变。

惊讶本身可以提供爽感，但若没有后续行为变化，不要强行让所有人态度转变。

### 3.15 Audience Knowledge Distribution

新圈层不应默认全知主角全部战绩，也不应为打脸而集体降智。

不同人物只按自己真实掌握的：

- 旧名声；
- 公开战绩；
- 身份；
- 已暴露能力；

作初始判断。最低充分的新事实出现后，他们再按各自利益分别更新招揽、敌意、合作或挑战规格。

### 3.16 High-Value Acquisition 是读者欲望原则，不是阶段字段

真正让人馋的剑、功法、体质、奇物、身份、伙伴、地点、资格、飞舟、洞府等仍然是男频燃料。

问题从来不是“获得”本身，而是把它制度化成每阶段必填项。没有自然机会不制造；一旦获得，就必须改变后续故事。

### 3.17 Compounding 是历史继续生效，不是后台词

好的复利是：过去得到的步法、兵器、关系、身份、知识、入口，在一百章后仍影响战斗、选择、敌人反制或新获得。

坏的复利是：每阶段写一句“资产产生复利”，但旧东西不再真实出现。

### 3.18 主人公连续升格

主角成长不只是战力数字。长期应进入第一章时没有资格进入的：

- 力量层；
- 人物圈层；
- 世界层；
- 真相层；
- 选择层。

力量/身体、身份/关系、世界入口、认知与选择权应尽量组成因果螺旋，而不是平行 KPI。

### 3.19 Shock Recontextualization

长期重释不是普通伏笔回收，而是：

> **意外 + 回看成立 + 重大状态变化。**

揭晓瞬间应有“原来如此”的 shock，前文证据回看成立；同时它必须改变力量、身份、关系、敌我或世界格局。

它不等于隐藏身世、转世、神秘父母，也不要求每阶段一个秘密。来源可以是能力真正原理、人物身份、旧关系、旧事件、宝物或世界联系。

### 3.20 Strategic Direct Exposition / Reader Orientation

“少解释”不是目标。目标是：

> 给读者最短但完整的可复用预测模型。

高价值 Orientation 在新势力、地点、身份、资源、力量层或生活边界第一次真正影响选择时，可以用短直接旁白回答：

- 这是什么；
- 为什么此刻重要；
- 当前 POV 通常知道什么。

然后立即回到现场。

低价值解释则是同一结论反复证明、决定后的实施过程、已经成立的能力边界再次说明。

### 3.21 World Entry 应在真正跨门槛的当章兑现

正式上路、进入新组织/内层、第一次实际使用身份入口时，读者就应感到：

> 主角进入了第一章时进不去的世界。

不要等下一章遇险后才补说明，也不要为此增加 Prelude/百科章。

### 3.22 Story-bearing Texture > Decorative Density

正文丰富感来自承载故事的少量具体细节：动作、物件、空间、身体反馈、力量后果和人物差异化反应。

不是五感覆盖、辞藻堆叠、每个动作都拆力路。尤其 Action 场景应压缩受力、工序和技术拆解。

### 3.23 Few Deep Rules > Many Hard Gates

系统发现问题时，优先：

- 删除旧规则；
- 移动 authority；
- 降权；
- 改可见性；
- 合并重叠原则；

最后才新增 Prompt。默认不增加 Agent、Reviewer、Scorer、数据库或 Hard Gate。

### 3.24 Evidence First；对的就说对

不要为了完成审计制造问题。一个层已经正确，就明确冻结，不要因为研究了某部经典作品就硬塞新机制。

任何检查前先问：

> 它会检测出什么具体失败？出现后我会做什么不同？

答不上来就不运行。不要加无用途的哈希、兼容层、防御脚手架或不可达角落处理。

---

## 4. Important Concepts

### 4.1 Protagonist-blind World Vision

**是什么：** 一个不知道未来主角和金手指的世界权威。
**为什么存在：** 防止世界先为主角准备钥匙孔，防止能力、人物与世界主题同构。
**负责：** 普通生活、力量正常值、社会现实、价值物、独立事件、奇观、知识边界。
**不是什么：** 完整治理模拟；也不是“世界必须中性，不得适合男频幻想”。
**正确应用：** 没有主角仍有值得看的故事；世界又能提供大量真正想争的力量、宝物、强者和地点。

### 4.2 POWER_BASELINE / LIFE_CONTEXT

它们是 World 的确定性投影：

- `POWER_BASELINE` 只给 Power Seed 世界力量正常值与生成边界，不给 named Story Opportunities；
- `LIFE_CONTEXT` 只给 Human Seed 普通生活、阶层、教育和现实环境，不给未来能力和 named 大事。

它们解决的是信息隔离，不是新增创作 Agent。

### 4.3 Power Novelty Spark

**是什么：** 给三个 Power 候选各一枚“熟悉能力幻想 × 单一异常”的非 Canon 随机扰动。
**作用：** 打破模型默认能力先验、拉开候选起点。
**不负责：** 强度；不向下游传播；不允许 Luna 原样照抄。
**常见误读：** 有 Spark 就等于金手指够强。错误。Novelty 只负责不同，Privilege Delta 才负责爽。

### 4.4 Power Asymmetry / Privilege Delta

Power Asymmetry 是主角相对世界正常分布的明显特权。Privilege Delta 是它的可比较表达：同层别人必须二选一、等待、服从或到更高层才能做的事，主角现在就能做一部分。

正确例子：

> 对手正在发动一招时，主角可以抢走其中正在生效的一部分，让对方当场缺掉，并把它用于自己的下一动作。

弱例子：

> 主角可以把力量留在接触过的东西上，稍微更灵活。

后者不是绝对不能写，但若读者第一反应是“这也没什么稀奇”，候选质量就不够。

### 4.5 Advantage Stack

开局 Core Asymmetry 是第一层；后续通过世界中的真实获得，加入兵器、身体、知识、奇物、伴生体、技艺等新的非对称优势，并发生复合。

它不等于技能栏越堆越多，也不要求每阶段添加。判断标准是：新旧组合是否产生单项做不到的新结果，旧优势是否继续活着。

### 4.6 Human Seed

Human Seed 是“这个人原本是谁”的权威快照，不是人物全传。当前核心 lanes：

- Appetite：真正持续想要什么；
- Behavior：稳定选择偏向 + 现场实现变化；
- Relationship：哪些具体的人会改变选择。

当前私人欲望只初始化 T0 State，不冻结为永久人格；Audition Hook 只用于候选辨识，不进入 Canon。

### 4.7 Explicit Anonymous Human Prototype

`prism-wanderer-alpha` 是作者显式选择的匿名私人原型实验控制。

边界：

- 只提供 Appetite / Behavior / Relationship 的结构性偏向；
- 不迁移现实身份、履历、地点、机构、关系对象或身体特征；
- 只有 Human Seed 可消费精确 selector；
- World、Power、Story、Outline 默认不能召回；
- 普通新书 selector 为空，不得静默污染默认人物分布。

产品目标是“以作者人格生成幻想人物”，不是把现实 Biography 搬进小说。

### 4.8 Deterministic Character Composition

`CHARACTER.md` 只是冻结 Power Core + Human Core 的确定性合并，没有 Character Composer LLM。

它故意不解释“为什么这种童年注定得到这种能力”。不协调是 Collision 的材料，不是错误。

### 4.9 Story Program / Collision

Story Program 是第一次同时看见完整 World 与 Character 的层，默认 Sol high。

它的权威是：

> 这些既定的人、力量与世界，接下来如何互相改变。

它可以：

- 设计 5—7 个自然大型阶段；
- 决定开局优势如何在故事中实现；
- 通过真实获得加入新的 Power Asymmetry；
- 让新旧优势复合；
- 编织人生、幻想、世界三类发动机；
- 补少量非奠基性过去以支持局部关系/选择。

它不能重写 World、Power、Human，也不能把每阶段变成升级/奖励表单。

### 4.10 Authority ≠ Scheduling

Power Seed 决定开局能力的成长语法；Story Program 决定它在什么长期因果中实现，并决定后续新优势；Outline 只决定已批准变化在当前窗口通过哪些事件发生。

Outline 不应自行决定“给主角什么新外挂”；Director/Writer 更不能在打斗中临时觉醒一项长期能力。

### 4.11 Stage Delta / Block Delta

Delta 的问题是：

> 结束时什么真实东西与开始不同？

可包括 Power/Capability、Possession、Relationship、Identity/Access、Knowledge、Enemy State、World State；有就写，没有就省略。

它不是字段税。上一块已经发生的变化不能重复包装成新 Delta。

### 4.12 Reader Release Map / WORLD AUTHORITY

- `WORLD AUTHORITY`：Approved World Vision 的章节期安全投影，不含 named 大事件目的、隐藏关系、未解谜底和未来 reveal。
- `Reader Release Map`：Outline 只排当前窗口中 timing-sensitive、且与真实事件相交的首次世界事实释放。

正确逻辑：

> World 决定事实 → Outline 决定何时需要 → Runtime bounded prefetch → Curator 筛选 → Writer 最短充分表达。

不要把“World 文件里写过”误认为读者已经知道。

### 4.13 Minimum-Sufficient Public Proof

公开证明只展示到足以迫使别人改变行动。它不追求所有人完全理解能力，也不要求连续专家认证。

好的结果：对手换策略、强者提高招揽规格、身份/资格改变。
坏的结果：五个人轮流说“确实不是运气”，故事状态不变。

### 4.14 Secondary Fantasy Axis

职业、专业或技艺只有在**即使完全不增强主战力，读者仍会想看主角练到顶**时，才是第二幻想轴。

需要：

- 独立强弱差；
- 真正顶层人物；
- 可见胜负或作品；
- 稀有高价值成果；
- 社会价格。

炼药可以成立；“更快制作补给、赚更多钱再买修炼资源”通常只是 Supporting Workflow。

不强制每本书有副职，是否投入由 Human 决定。

### 4.15 Adjudicable Payoff Debt

少量强承诺可以有：

> 具体对象 + 至少一个读者可观察的结算条件。

例如期限、比赛、场域、资格或明确结果。它给读者“离结账还有多远”的感觉。

它不是每个 Open Promise 的 schema，不是机械倒计时，也不保证主角一定赴约、追回或获胜。

### 4.16 Character Authority Invariance

任何可能改变主角取舍的结构 Treatment，都应至少用 2—3 个动机排序不同的冻结 Human 测试。

Treatment 必须同时做到：

- 产生目标结构增益；
- 保留 Human-specific 选择差异。

若力量型、关系型、混合型最后都被推成同一种“成长最优/关系最优/道德最优”，即使故事更整齐，也应 FAIL 或降级。

### 4.17 Matched Decision Point

要证明 `Personality → Choice → Route`，先让不同 Human 面对**同一个具体诱惑、冲突和机会池**，只看选择是否分叉；再放开长期 Story Program。

如果每个人连开局事故都不同，只能证明生成结果不同，不能纯归因于人格。

### 4.18 GBrain

GBrain 是 Optional Inspiration，不是 Canon、价值裁判、剧情素材库或 Hard Gate。

两条路径：

```text
GBrain → World / Power / Human / Story Program / Outline → Approved Story
GBrain 离线蒸馏 → Scene Skills → Curator / Primary
```

raw GBrain 不直接进入 Writer。source-specific DNA 默认 `REFERENCE_ONLY`；只有真正新增跨书判断能力的 craft 才 active。检索可以为空，不为凑数塞弱卡。

蒸馏口诀：

> Terra 看清事实 → Luna 理解吸引力 → Sol 理解长篇结构。

### 4.19 System Steward

`tgn-system-steward` 是独立审计 Skill，不是 production 节点。

用户说“审计”时：

- 自动调用当前激活 Steward 做一次独立审计；
- 当前 Agent 同时复核 live code/docs/artifact；
- 最终合并结论，分歧需显式说明。

它只在审计方法本身稳定变化时更新。当前已加入 Character Authority Invariance 与 Matched Decision Point。

---

## 5. Decision Model

面对一个以前从未讨论过的新问题，不应先问“往哪个 Prompt 加一句”，而应沿以下逻辑判断。

### 5.1 先定义读者真正失败在哪里

不要把表象当问题本身。

例如“第四章很慢”可能分别意味着：

- 故事状态没有推进；
- 同一事实被重复证明；
- 世界入口没有让读者感到地图打开；
- 重要势力首次出现却没有类别说明；
- Supporting Skill 被扩成流程；
- 章节本来缺少真正事件。

不同失败对应不同层，不能统一用“少写一点”解决。

### 5.2 找到事实最早被生成的层

问：

> 如果换一本完全不同的新书，这个问题会不会再次出现？

- World 缺力量正常值或公共类别：修 World authority；
- Power 不馋、不超标：修 Power candidate distribution；
- 人物像人格论文：修 Human schema；
- 长期阶段机械重复：修 Story Program；
- 十章块硬补升级/奖励：修 Outline；
- 本章计划已正确但仍扩成工序：修 Director/Curator/Writer；
- 正文事实串错：修 State/Canon。

不要让下游兜底上游缺失。

### 5.3 区分“缺少”与“释放失败”

读者不知道世界事实时，依次检查：

1. Approved World 是否存在；
2. 是否属于可安全公开事实；
3. Outline 是否在第一次影响事件时排程；
4. Runtime 是否真的传入；
5. Curator 是否保留；
6. Primary 是否最短充分表达。

这避免两种误诊：World 明明没有，却怪 Writer；World 明明有，但从未传到 Writer，却继续补设定。

### 5.4 判断是单本 candidate 问题还是系统分布问题

一个能力弱、一个人物普通、一章对话长，不足以立即改架构。

应区分：

- 架构是否允许健康结果；
- 多候选分布是否坍缩；
- 当前 candidate 本身是否值得选；
- 问题是否跨新书复现。

“架构 PASS，候选3较弱”是正常结论。不要 cherry-pick 最好候选证明系统成功，也不要因一个弱候选推倒架构。

### 5.5 先保护已经工作的东西，再做最小根修

每次修复都问：

- 哪一层已经正确，必须冻结？
- 新规则会不会过度纠偏？
- 能否通过删除、移动、降权、改变可见性解决？
- 是否真的需要新增字段/Agent/测试？

典型过度纠偏：

- 去工程化 → 把高价值 Reader Orientation 也删掉；
- 去阶段税 → 把男频成长也删掉；
- 保持世界独立 → 不允许世界偏向幻想；
- 保护人物 → 主角长期不变强；
- 强化爽感 → 所有人选择成长最优；
- 简化机制 → 能力变弱；
- 防降智打脸 → 所有人自动全知主角。

### 5.6 用因果实验，而不是 Prompt 自我感觉

受控实验优先：

- 冻结被测层之前全部已批准 authority；
- 冻结模型、reasoning、retrieval bundle 和其它输入；
- 一次改变一个主要变量；
- 预先规定候选选择规则；
- 先直接读真实输出，再使用 Judge；
- 记录 tokens、wall-clock、成本和副作用；
- 明确 PASS / DIRECTIONAL PASS / PARTIAL / FAIL / INVALID；
- 写 `What This Did Not Solve`。

测试人格因果时必须额外用：

- Character Authority Invariance；
- Matched Decision Point。

### 5.7 只有通过后才冻结；通过也只冻结它证明的部分

实验通过不等于解决所有相关问题。

例如：

- Audience Knowledge Distribution PASS，只证明局部认知有益，不证明需要 Reputation Database；
- Secondary Axis B2 PASS，不证明每本书都要炼药；
- Reader Orientation 五章 PASS，不证明 100 章后仍不会膨胀；
- Personality Advantage Tree PARTIAL，只证明人格改变路线和用途，不能宣称已产生四棵独立优势树。

### 5.8 若新机制覆盖 Human，结构再漂亮也失败

当某个 Treatment 让不同人物都做同一“最优”选择，它是在改写人物效用函数。

一个力量欲极强的人留下试炼可能完全正确；一个已冻结为“具体关系可改变路线”的人被同一 Treatment 推去试炼，则是 Story Architecture overriding Character Authority。

判断的是来源，不是选择表面。

### 5.9 最终判断标准

一个健康结果应同时满足：

- 读者想要主角的东西；
- 主角主动制造故事；
- 人物选择仍像这个具体的人；
- 世界有自己的欲望和故事；
- 主角真实变强并升格；
- 旧状态继续改变新故事；
- 尺度清楚，社会会重新定价；
- 系统没有把后台原则写成小说 ontology；
- 下游没有为了合理性增加流程税。

---

## 6. Taste / Quality Bar

### 6.1 好的男频体验

- 金手指一句能懂，第一眼就想拥有；
- 能力相对同层明显不公平，有条件越级；
- 读者频繁知道主角在哪一档、超标在哪里；
- 高价值对象在真正获得前先被写得让人馋；
- 获得后立刻证明价值，之后继续复用；
- 新圈层根据局部信息合理报价，看到事实后更新；
- 主角力量、身体、身份、关系、世界位置和认知持续升格；
- 人物会为了钱、爱、性、面子、好奇、审美、野心、兄弟或报复做不完全理性的选择；
- 关系是选择变量，不是团队配置；
- 世界有强者、宝物、奇观、比赛、秘境、战争和真正想去的地方；
- 章节不断发生新的不可逆状态，而不是提高同一结论置信度；
- 偶尔出现足够震撼的长期重释。

### 6.2 不好的“看似高级”

- 世界抽象、哲学化、制度化，读者不知道具体能干什么；
- 大量“秩序、资格、责任、治理、维护、承载、分配”成为故事主词；
- 能力变成工作技能、路线优化或项目管理；
- 主角像理性风险经理，所有选择都财务最优；
- 每个阶段获得资产、解锁功能、投资下一轮；
- 人物都自主到只会安全谈判，不会崇拜、爱慕、效忠、屈服或疯狂竞争；
- 所有胜利立刻补一笔同等责任或损失；
- 所有谜团都变成验证程序；
- 解释极少但读者根本不知道世界和势力是什么；
- 名词很多却不能帮助预测；
- 对话完整到像会议纪要；
- 内心反复证明已经做出的选择；
- 场景细节多但不承载冲突、人物或幻想。

### 6.3 “具体”的真正含义

Specificity 不是 Sensory Density，也不是技术细节密度。

优先具体在：

- 谁想要什么；
- 谁阻止；
- 主角决定什么；
- 核心优势怎样改变结果；
- 谁因此得到或失去什么；
- 什么从此不能回到原状；
- 世界尺度如何说明这次超标。

专业细节只保留能够改变判断的 discriminative detail。

---

## 7. Tacit Knowledge

以下共识很多是在多轮纠偏中形成，未必总以正式规则出现，但对未来判断非常重要。

### 7.1 TGN 的最大敌人是“模型的理性收敛”，不是缺乏逻辑

模型天然倾向把一切变成：

- 责任；
- 自主；
- 边界；
- 成本；
- 风险控制；
- 公共利益；
- 合理流程。

这会把不同人物写成同一个高认知、克制、反控制的项目经理。TGN 必须允许贪、赢、面子、性欲、爱情、兄弟、报复、享受、自利、审美和野心真实支配选择。

### 7.2 用户要的是“既像我，又是爽文主角”

个性化不能只让主角说话像用户，也不能为了像用户而削弱男频成长。

真正目标是：

> 这个人会因自己的偏好进入不同故事；但无论怎样选择，长期仍拥有主角级成长、优势栈和世界升格。

### 7.3 不要用机械补偿保护 Growth Floor

关系型主角放弃试炼后，不应由系统立刻发一个更好的外挂作为道德奖励。

正确因果是：他进入了另一条真实路线，而那条路线本来就有自己的机会、损失和可能获得。人格改变机会分布，不是宇宙按人格发奖。

### 7.4 社会重新定价比“大家震惊”更重要

读者的优越感来自世界不得不改变行为：更高规格招揽、更强敌策、身份入口、报价、资格、婚姻/关系位置等。单纯倒吸凉气很快会空。

### 7.5 经典主干不是失败

资源→成长→战斗→身份→更大世界，探索→机缘→成长→新区域，比赛、拍卖、秘境、强导师等成熟结构都可以用。

创新应主要落在：

- 本书核心幻想；
- 人物选择；
- 关系；
- 能力复合；
- 阶段换挡；

而不是为了显得原创绕开一切有效结构。

### 7.6 系统原则必须隐身

Action Space、Net New、Impact、Compounding、World Independence 等可以用于后台判断，但不能变成世界里的术语、资源类别、势力口号或每阶段字段。

系统一旦成为故事内容，LLM 就会开始维护系统而不是写小说。

### 7.7 解释的价值取决于未来预测力

一个境界、品级、榜单或势力类别若会反复工作，早点清楚解释可以降低总认知成本。真正要压的是一次性抽象名词和不产生预测力的流程说明。

### 7.8 人物自主不等于对称权力

配角可以真心投靠、崇拜、爱慕、拜师、效忠、害怕、屈服或背叛，只要源于自己的欲望。不要把每段关系写成双方永久对等的 stakeholder negotiation。

### 7.9 主角可以输机会，但不能失去长篇分量

一次选择可以让主角错过秘境、名额、钱或功法；这甚至能增强人物。但长期必须看到他从其它真实因果中继续成长、获得和升格。

### 7.10 “对的就冻结”比不断优化更难也更重要

多轮实验中最健康的行为之一，是撤销自己想加的 patch：World 正交删除测试、Director ruler projection、Cross-Ruler prompt、Power 看公共价值物等。研究经典作品不意味着 production 必须变化。

### 7.11 LLM 最危险的失败经常是“太合理”，因此比明显胡编更难抓

工程、验证、责任、流程、风险控制、资源安排往往局部都说得通。真正的审计问题不是“这段有没有逻辑”，而是：**它为什么获得了这么高的叙事权重？** TGN 要识别的常常不是错误事实，而是合理支撑层悄悄取代了读者真正想看的幻想、人物选择和世界进入。

### 7.12 人格最有力的证明通常是机会成本，不是心理分析

一个选择只有在另一条路也真正诱人时，才会暴露人物。若所有选项中只有一个显然正确，Human 再丰富也难以进入故事。因此测试人格时应让力量、关系、钱、身份、好奇等真实价值发生冲突；人物为某一项付出的**真实错失**本身就是 Character Proof。

### 7.13 反 AI 纠偏本身也会过度

TGN 曾从“AI 爱解释”过度纠偏到“什么都压缩”，导致正文逻辑清楚但世界薄。今后任何反偏置原则都要检查它是否误伤邻近的高价值能力：反解释不能误伤 Orientation；反阶段税不能误伤 Growth Floor；反职业流程不能误伤真正的 Secondary Fantasy Axis。

### 7.14 好系统允许高质量的不均匀

不是每章一样长、每阶段都升级、每段关系都改变、每个候选都一样强、每本书都有副职、每章都解释世界、每个 Promise 都债务化。Checklist 倾向会把小说平均化；系统应保护**有因果理由的不均匀注意力**。

### 7.15 世界自主性与主角传奇感并不冲突

世界不为主角出生，不代表主角不能越来越重要。更好的传奇感是：**世界本来就很大、很多事与我无关；但随着我真正变强和做出选择，原本独立的人与事件越来越不得不考虑我。** 这比“所有秘密早就在等主角”更有分量。

---

## 8. Important Corrections

### 8.1 从单一 Fantasy Seed 到 Split Authority

**早期误解：** 先生成一个统一 Seed，可以自然协调世界、能力、人物。
**实际问题：** 同一模型会后验合理化，世界和人物都变成能力隐喻。
**最终理解：** World protagonist-blind；Power/Human 独立；Character deterministic；Story Program 才第一次碰撞。

### 8.2 从 Biography→Adaptation→Core Obsession 到 Human 快照

**早期误解：** 人物深度来自每段过去解释今天人格。
**问题：** 人物像心理学证明论文，童年被主题化，最终都变成“自主、负责、有边界”。
**最终理解：** 生活事实可以只是生活；多股动机竞争；稳定选择偏向；具体关系改变选择。

### 8.3 删除阶段成长税，但不能删掉男频成长

**过度删减风险：** Story Program 只保留因果、选择、永久变化，逐渐成为人物剧。
**最终理解：** 成长是全书纵向不变量，不是每阶段表单。阶段可无升级；整本书不能长期不变强。

### 8.4 High-Value Acquisition / Compounding 从字段降级，不是消失

**错误理解：** 旧表单有害，所以奖励与复利思想都应删。
**最终理解：** 获得是可选阶段结果；一旦发生必须进入后续故事。复利是历史持续生效，不是后台词。

### 8.5 Outline 不是第二个 Story Program

**问题：** Story Program 允许无 Power Delta，Outline 又要求每块“一级成长/收益反哺/世界扩张”，阶段税下沉。
**最终理解：** Outline 只编译已批准变化；Block Delta 只写实际变化，不补小技能、小奖励、新权限、新地图。

### 8.6 Power 简单不等于 Power 弱

**错误方向：** 为避免复杂术语，把能力压成“稍微灵活”。
**最终理解：** 一句话能懂、一个异常、明显超标；复杂性从长期复合长出来。

### 8.7 Shock 不等于隐藏身世

**错误方向：** 每本书设置一条主角秘密/血统链。
**最终理解：** 长期重释可以来自能力原理、旧物、人物、关系或世界事件；必须 shock、回看成立并改变状态，不强制身世。

### 8.8 去工程化不等于禁止一切专业成长

**错误方向：** 因为修渠、维护、诊断曾抢故事，所以炼药、炼器等都只能压成背景。
**最终理解：** 若一条专业本身拥有可欲望的强者尺度、顶层人物、作品胜负和社会价格，它可以是 Secondary Fantasy Axis；普通实施仍压缩。

### 8.9 反验证不等于反比赛/测试

**错误方向：** 所有测试、排名、考核都程序化。
**最终理解：** 有共同尺度、真实竞争、见证人和状态后果的竞技证明场非常高效；问题是只提高同一结论置信度的重复验证。

### 8.10 强化成长不能覆盖人格

**典型失败：** Cross-Ruler Conversion Treatment 把闻野舟从“为顾晚禾放弃复测”改成“留下参加力量试炼”。
**为什么失败：** Human 未变，事件未变，只因结构原则强调成长，人物效用函数被覆盖。
**最终理解：** 力量第一型留下完全正确；关系可改路型放弃也正确。结构提供机会，Human 决定取舍。

### 8.11 Reader Orientation 不是设定倾倒

**早期问题：** 为反 AI 解释和百科，开局世界信息被压得过少；读者不知道商队为何重要、势力是什么。
**最终理解：** 动作第一次引发问题时，用 Approved World 的最短充分事实回答；World Entry 当章兑现；不新增 Prelude，不推迟核心爽点。

### 8.12 人格差异实验需要 Matched Decision Point

**旧实验局限：** 四个 Human 的 Story Program 连开局事故都不同，路线差异混有采样创意。
**最终理解：** 先给同一冲突和机会池，看选择是否分叉；再观察长期路线。否则不能纯归因人格。

### 8.13 “不同人格 → 不同优势树”目前只做到一半

人格已经改变：为何去、跟谁走、错过什么、能力用给谁。
但同 World/同 Core 的四线实验中，所有人仍拿到某种剥纹，最终只是两类机械分支、四种用途。
因此不能宣称个性化优势树已经完成。

### 8.14 《斗破》研究不意味着所有漂亮机制都进 production

后来 A/B 否定或降级了：

- Director 额外 Ruler Projection：增益小，当前系统已能工作；
- Cross-Ruler Conversion Prompt：覆盖 Human；
- Power Seed 读取 World Public Value：不稳定，容易世界先造宝物、Power 再配钥匙。

研究报告中较早的 P0 建议若与后续 A/B 冲突，以后续实验为准。

---

## 9. Validated Conclusions

### 9.1 Split Character Authority：已冻结 production

证据：多轮 World/Power/Human/Collision 实验与代码回归。它显著减少世界—能力—人格同构，并允许关系/人生阶段不依赖 Power Delta 成立。

适用范围：新书上游创意链。它不是所有写作任务的普遍真理，但对 TGN 当前生成目标是稳定默认。

### 9.2 Human Seed 新 schema：已验证优于旧模型

旧 `Biography → Adaptation → Behavior → Core Obsession` 已被：

> `Lived Facts → Competing Motives → Stable Choice Bias → Person-specific Relationships`

替换。A/B 显示人物更像人，不再要求所有过去解释人格。

### 9.3 Story Program 阶段税根修：已验证

传统修仙与百铸身等实验中，完整大型阶段可以没有 Power/Capability Delta，仍靠关系、战争、身份和世界变化成立；全书力量线同时持续质变。

结论：

> `Growth is a longitudinal invariant, not a per-stage form requirement.`

### 9.4 Outline 的 Block Delta / execution boundary：当前已实现

当前 docs/code 明确：Outline 是执行编译层，不重新调度 Story Program，不得自行添加 Power Asymmetry、微升级、小奖励、新权限或新地图。

### 9.5 Power Novelty Spark + Power Asymmetry：已验证并 production 化

A/B 表明 Spark 能拉开候选，但必须额外要求：

- 明确 Privilege Delta；
- 保留 Spark 单一异常；
- 默认宁强勿弱；
- 一句话能懂；
- 长期可复合。

弱能力“落景”促成了这次根修；后续“夺势/截景”类候选明显更有男频欲望。

### 9.6 Persistent Reader Ruler：已冻结

《斗破》全文 1646 章研究显示，境界、星级、功法/斗技品阶、炼药品级、异火、榜单、资格等尺度几乎贯穿每个百章区间。尺度是长期阅读语言，不是开篇设定表。

TGN 当前已将 Ruler 定义为压缩工具，而非战力数据库。

### 9.7 Protagonist Ascension：已冻结

抽象结构：

> 力量/身体升格 → 被更高层重新估价 → 身份/关系/入口改变 → 世界/认知扩大 → 新选择与新欲望。

这与用户希望的《Bad Born Blood》式纵向成长骨架一致。

### 9.8 《斗破》三项机制 A/B：已最小 production 化

用三种冻结 Human 做多组 Sol high A/B：

1. **Audience Knowledge Distribution：PASS / DIRECTIONAL PASS**
   最小合并进 Protagonist Ascension；没有 Reputation Database。
2. **Strong Secondary Fantasy Axis：B2 PASS**
   普通练习/考试/流程压缩；作品、胜负、稀有创造、强者认可与社会价格前置；不强制副职。
3. **Adjudicable Payoff Debt：PASS**
   少量 Promise 可有可观察结算条件；继续复用 Open Promises，无新 schema。

### 9.9 Character Authority Invariance：已成为实验协议

同一结构机制必须在不同 Human 上保持不同选择。它成功识别了“结构更整齐但人物被改写”的失败。

### 9.10 Matched Decision Point：已加入 Steward v0.1.11

Skill lint、package validate、安装、激活及 smoke 均通过。Smoke 正确把“不同 Human + 不同事件 → 声称人格因果成立”判为 INVALID/CONFOUNDED。

### 9.11 私人匿名原型 selector：已 production 验证

`prism-wanderer-alpha` 只在显式选择时进入 Human Seed；不会污染 World/Power 或普通新书。早期 Selector E2E 证明人格可以改变 Story Program 选择，而不是只改变口吻。

### 9.12 前五章私人原型实验的连续结论

- `分流真元/谢临川`：人物成立，但第2—4章被修船、欠账、通行等 supporting logic 拉慢；
- `落景/裴听岚`：世界更鲜明，但金手指不够稀奇，力量尺仍弱；
- `夺势/闻野舟`：第一章的 Power Asymmetry 和尺度明显增强，但第2—5章出现重复证明、Choice Loitering 和专业细节膨胀；
- 后续 pace/ruler/orientation 修复将问题定位到 Outline、Reader Release、World Authority 与 Supporting Skill compression，而不是继续给 Writer 加“别水”。

### 9.13 Reader Orientation / World Entry 最终回归：PASS WITH RESIDUAL RISK

五章实验验证：

- Ch1 可以在不增加 Prelude、不推迟 Core Power 的情况下建立最低生活/安全坐标；
- Ch3 在真正跨南门时说明商队为何是无阶普通人的现实世界入口；
- Ch4 首次出现白角部时只说明“荒原部族/南迁被边军视为入侵”，不泄露动机和幼兽真相；
- Ch4 从约 3604 字压到约 1575 字，低价值排车/绑缚实施显著减少；
- Ch5 保留核心能力再次兑现与幼叫 reveal。

结论不是“多写世界观”，而是：

> Approved World → Release timing → Curator projection → Primary direct orientation。

### 9.14 Story-bearing Texture：已冻结

2026-08-24 五场景 A/B，两个独立盲评合计 Texture 9 胜 / Baseline 1 胜。正文应丰富但不腻，细节承载故事，不做装饰密度。

### 9.15 GBrain ON 的主要增益位于 Story Program / Outline

同 Seed OFF/ON A/B 显示：ON 更稳定产生 Plot Engine 变异、Thread Ecology、高价值获得后续复用和长线回流；World 和章节 Writer 不应因此得到更大 raw context。

### 9.16 《斗破》全文研究的核心结论

真正可迁移的不是退婚、异火、拍卖或打脸模板，而是：

> 共同尺度 → 超标结果 → 世界重新估价 → 新资源/资格/对手/圈层 → 下一欲望与成长。

TGN 应保留这套反馈机器，同时比《斗破》更好地保护人物选择、关系、世界独立和非程序化正文。

### 9.17 Personality Advantage Tree 实验：Overall PARTIAL

固定同一 World、同一盲选 Core Power「穿隙」、同一 Human GBrain、同一 Story GBrain，只换四个 Human，生成四套 Sol Story Program。

结果：

- Personality → Choice：PASS；
- Choice → Route → Opportunity：PASS；
- 四线 Growth Floor：PASS；
- Opportunity → Different Advantage Tree：PARTIAL。

四人路线和用途明显不同，但全部获得某种剥纹，最终更像两种机械分支 × 四种人格化使用方式，而非四棵独立优势树。

---

## 10. Rejected / Superseded Directions

以下方向未来很容易被重新提出，应明确避免重复踩坑。

### 10.1 恢复每阶段升级/获得/复利字段

会把故事重新写成：获得资产→解锁功能→投资下一轮→扩大行动空间。已被 Stage Delta 和纵向 Growth invariant 替代。

### 10.2 Story Program 只保留人物因果，不显式关心 Fantasy progression

会过度纠偏成优秀人物剧但忘记男频变强。Growth Floor 必须保留。

### 10.3 Character Composer LLM

会重新制造“童年注定得到能力”的后验适配。当前 deterministic composition 是有意设计。

### 10.4 人格类型菜单、MBTI、评分器或动机配额

会把多样性变成分配题。Human GBrain 应提供判断 craft，而不是人格菜单。

### 10.5 每本书必须隐藏身世/转世/秘密血统

Shock Recontextualization 不等于身世模板。

### 10.6 每本书必须有副职

Secondary Fantasy Axis 仅在这条路本身值得追到顶时成立。

### 10.7 每个 Promise 都有期限、地点和公开对决

Payoff Debt 只用于少量自然强承诺。

### 10.8 Reputation Database / 战力数据库 / Reader State 机器

当前问题主要是 authority、释放和投影，不是缺少大数据库。

### 10.9 raw GBrain 直接进入 Writer

会造成 source leakage、上下文噪声和权威越界。Writer 只消费 approved story 与 Scene Skills。

### 10.10 Cross-Ruler Conversion Prompt

虽然“力量→身份→资源→力量”是好分析语言，但强调后曾把不同 Human 推向成长最优，覆盖人物。现有 Ascension、Acquisition、Compounding 已足够自然产生转换。

### 10.11 Power Seed 直接读取 World Public Value

A/B 不稳定，容易变成 World 先写宝物、Power 为宝物配钥匙，破坏 Split Authority。允许 Collision 后自然发现“同一公共价值物对主角有额外边际价值”。

### 10.12 Director 额外固定 Ruler Projection

后续 A/B 增益不足，baseline 已能用现有 Plan/World release 完成比较。不要因早期研究报告建议而直接上线。

### 10.13 World Independence 的正交删除 Reviewer / Hard Test

实验已确认真正 collapse 多发生在 Collision compiler，不需要各层都加守卫。

### 10.14 禁止一切专业细节

错误。只压缩不改变判断的实施；能改变结论的关键细节、完整第二幻想轴和真正竞技证明应保留。

### 10.15 任何低动作章都给主角安排一个小问题解决

这是 Competence Filler。主角观察、选择、拒绝、站队、进入世界或承受关系后果也可以构成完整章节行动。

### 10.16 所有胜利都必须立刻付同等代价

会把爽点变成税。普通小胜允许明显净收益，阶段大胜通常收益显著高于当前成本。

### 10.17 所有人都必须保持平等、条件化合作

人物自主不等于永远对称议价。

---

## 11. Current System / Project State

### 11.1 Repo 状态

截至本 Handoff 写作前核对：

- Repo：`C:\dev\tgn-story-mvp`
- Branch：`principal_dev_new_sys`
- 本次双 Handoff 融合开始时的 HEAD：`1760c9a docs: add deep context handoff`；接手时仍应 live-check HEAD，不把该 commit 当永久事实。
- 前一关键提交：
  - `15a389d feat(story): finalize reader orientation release`
  - `f81894a chore(steward): add matched decision validation`
  - `e010b8b test(story): compare personality advantage trees`
  - `2d61dae test(story): validate doupo-inspired mechanisms`
  - `a9dcafa fix(outline): separate opening life orientation`
  - `4e9fb5e refactor(story): add reader release map`
- Git identity：`happyivanencoding <jingxuan.ivan@gmail.com>`

`15a389d` 已把 Reader Orientation、World Entry、WORLD AUTHORITY 释放链、Supporting Skill effect-level compression、Qualification Process Tax / Competence Filler 边界、`novel-prose-realization` Skill 与最终五章回归正式提交。

工作树仍有**并行未提交内容**，但范围已缩小，主要包括：

- `docs/MVP_PRODUCT_DIRECTION.md` 对 Audience Knowledge、Secondary Fantasy Axis、Payoff Debt 的 current-doc 对齐；
- 若干早期/中间版 `real-exp-private-prototype-orientation-*` 实验目录；
- 尚未形成最终结论的 `real-exp-doupo-feel-engine-*`；
- 多个研究与重跑用 `temps/*`；
- `DEEP_CONTEXT_HANDOFF_2.md` 已在本最终版中完成内容级融合；原文件仍保留为 provenance，不因生成 FINAL 就自动删除。

接手者必须先 `git status`，不得覆盖、重置、清理或顺手提交这些并行内容。当前 Handoff 应单独处理。

### 11.2 当前 production 创意链

```text
作者方向
→ protagonist-blind World Vision
→ POWER_BASELINE / LIFE_CONTEXT
→ 独立 Power Seed + Human Seed
→ 作者一次批准 Character
→ deterministic CHARACTER.md
→ Story Program / Collision
→ 作者批准
→ Outline
→ Director
→ Curator
→ Primary Writer
→ State Extraction
```

没有 production Fantasy Seed，没有 Character Composer LLM。

### 11.3 当前批准点

1. World Vision；
2. Character（Power + Human 一次批准）；
3. Story Program。

### 11.4 当前重要模块/文档

- `PROJECT_RULES.md`：唯一长期项目执行权威；
- `docs/MVP_PRODUCT_DIRECTION.md`：产品目标、创意权威、Anti-Goals；
- `docs/PIPELINE_METHODOLOGY_AND_VALUES.md`：分层方法论；
- `docs/SPLIT_CHARACTER_AUTHORITY.md`：World/Power/Human/Collision 边界；
- `docs/GBRAIN_STORY_CRAFT_V3.md`：GBrain 接入与蒸馏；
- `docs/CHAPTER_RUNTIME_AND_STATE.md`：章节、Canon、State；
- `docs/NOVEL_PROSE_REALIZATION.md`：正文表达；
- `docs/AUTHOR_WORKSPACE_UI_SPEC.md`：UI；
- `.agents/skills/tgn-system-steward/`：审计 Skill；
- `.agents/skills/novel-prose-realization/`：正文实现 Skill；Reader Orientation / Supporting Skill compression 更新已随 `15a389d` 提交。

### 11.5 当前关键实验

- `books/real-exp-doupo-system-mechanisms-20260827-v1`：三项《斗破》机制 A/B；
- `books/real-exp-personality-advantage-tree-20260827-v1`：四 Human 优势树实验，结论 PARTIAL；
- `books/real-exp-private-prototype-orientation-world-entry-final-20260827-v1`：Reader Orientation/World Entry 最终五章回归；
- `books/real-exp-private-prototype-asymmetry-novel-20260826-v2`：闻野舟/夺势五章与主观审计；
- `docs/research/DOUPO_FULLTEXT_TGN_ARCHITECTURE_STUDY_20260827.md`：全文研究；其中较早的架构建议须用后续 A/B 校准。

### 11.6 测试状态

最近多轮完整回归均为 **294 passed**。本 Handoff 创建前读取的最新实验也记录 294 passed。由于工作树仍有并行改动，任何继续开发前仍应重新运行与任务相关的专项测试和全量回归。

### 11.7 GBrain 当前真实状态

当前实测：

- Pages：3827
- Chunks：15856
- Embedded：15850

即 **还有 6 个 chunk 未 embedding**。这与某些旧 docs 中历史上的 `Embedded == Chunks` 状态不同；以当前 stats 为准。最近《斗破》全文 Story Craft / Longitudinal / Mentor Knowledge 等材料已存在，但 GBrain 更新交付仍不能标记完全结束，直到执行 `embed --stale` 并验证 `Embedded == Chunks`。

### 11.8 当前最重要的问题

不是“人格能不能改变剧情”——这一点已经 PASS。

当前核心未决是：

> **人格能否通过真实选择与路线，稳定改变第二、第三项非对称优势的种类，而不只是改变同一优势的用途。**

现有四线实验中，所有人都拿到剥纹，说明 Story Program 会从整个 World 选择与 Core 最容易复合的全局最佳机制，route-specific opportunity 对新优势的约束还不够强。

---

## 12. Current Implementation Choices

这些是当前默认，不是永恒原则。

### 12.1 模型路由

| 阶段 | 默认模型 | Reasoning | GBrain |
|---|---|---:|---|
| World Vision | GPT-5.6 Luna | high | 固定 1 条 Reader Coordinates + 最多 3 creative |
| Power Seed | GPT-5.6 Luna | high | Power lane，小 bundle |
| Human Seed | GPT-5.6 Luna | high | Appetite/Behavior/Relationship 各最多 1，总计最多 3 |
| Story Program | GPT-5.6 Sol | high | 最多 3 focused inspiration |
| Outline | GPT-5.6 Luna | high | 通常 4，最多 5 |
| Director | GPT-5.6 Luna | high | raw GBrain OFF |
| Curator | GPT-5.6 Luna | high | raw GBrain OFF；Scene Skills ON |
| Primary Writer | GPT-5.6 Terra | high | raw GBrain OFF；Scene Skills ON |
| State | GPT-5.6 Luna | low | OFF |

默认章节链：

> `Luna Director → Luna Curator → Terra Primary → Luna State`

模型判断必须分开：生成质量、wall-clock、实际成本。Terra Primary 是正文行为选择，不是便宜；Sol 只集中在长期高杠杆节点。

### 12.2 Power 生成

- 3 个 Novelty Spark 对应 3 个候选；
- Luna 基于 World Power Normal 重新发明；
- Blind Selector 不看 Human；
- 选择优先级：读者欲望、Privilege Delta、简单度、长期复合、Spark fidelity。

### 12.3 Human Prototype

默认 selector 为空。只有显式选择 `prism-wanderer-alpha` 时，Human Seed 生成一个匿名幻想人物；其它层忽略 selector。

### 12.4 GBrain 工具

- 根目录：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库`
- Windows/Git Bash 使用：`C:\Users\jingx\.bun\bin\gbrain.exe`
- 更新后：`embed --stale`
- 交付：`Embedded == Chunks`

### 12.5 ACP 边界

普通代码、Prompt、文件、Git 由当前 Agent 直接完成；只有真实 LLM 生成、模型 A/B、正文实验、原著蒸馏、跨书 synthesis 才用 ACP。

ACP：`C:\Users\jingx\AppData\Roaming\npm\codex-acp.ps1`，ChatGPT 登录，不切 API Key。

### 12.6 Docs 维护

Docs 只描述当前有效状态。更新时优先替换、删除、合并，不要不断追加。实验过程放 `books/real-exp-*` 或 `docs/research/`。

---

## 13. Open Questions

### 13.1 Route-specific Opportunity Authority

当前最重要假说：

> 新 Asymmetry 应先从 Human 实际选择后进入的 route-specific opportunity 中产生，而不是 Story Program 扫描整个 World，选择与 Core 最优复合的全局答案。

尚未 production 化，需要 A/B。

### 13.2 新优势应在何时被具体决定

当前 Story Program 可以一次规划几百章后的第二、第三优势。可能过早钉死，削弱真实剧情分叉。

开放问题：

- Story Program 应确定具体长期优势；
- 还是只确定优势方向/候选机会空间，等阶段刷新时具体化？

尚无专项证据，不应直接改架构。

### 13.3 Matched Decision Point 下的人格因果

四 Human 优势树实验开局事件不同，因果不纯。需要让不同 Human 面对同一具体冲突和机会池，先证明选择分叉，再看路线。

### 13.4 100/200/300 章稳定性

当前多数实验停在 Story Program 或前五章。尚未充分验证：

- 优势树到 200/300 章是否仍分叉；
- Reader Ruler 是否持续；
- Orientation 是否不膨胀；
- 人格是否被长期结构重新压成同一成长最优人格。

### 13.5 Reader Orientation 泛化

五章猎墙/商队型世界已 PASS，但未验证：

- 非旅行型题材；
- 20/50/100 章；
- 多次新势力/新地图进入；
- 直接 exposition 是否会逐渐过量。

### 13.6 GBrain embedding debt

当前 6 个 chunk 未 embedding。需补齐并做 retrieval regression，才能称最近更新完整交付。

### 13.7 Dominant Commercial Engine / Visible Desire Horizon

第二份 Handoff 补充了一个尚未冻结但很有价值的观察：有些章节各自清楚、每章都有事件，但读者仍难回答“未来 20—40 章主角最想拿到什么、离它还有多远”。候选假说是：一个阶段需要**Human 批准的可见主欲望/块级商业发动机**，让 Life / Fantasy / World 不只是平均轮换，而围绕一个读者能持续追踪的具体目标形成重力。

它目前仍是 Experimental Hypothesis，风险很高：若系统替 Human 发明一个“最商业”的目标，就会再次覆盖人物；也不能变成每个块必须填写 Dominant Engine 的新字段。下一步只能通过冻结 Human 的因果实验判断。

### 13.8 Fantasy Heartbeat / Reward Lifecycle

另一个未冻结观察：一些好东西在“拿到/展示”后容易离场，导致核心幻想在没有升阶的窗口里变弱。候选研究方向不是增加奖励频率，而是检查高价值资产是否经历完整生命周期：

> 想要 → 争取/承受 → 到手 → 首次证明 → 社会兑换 → 后续复用/重释。

现有 High-Value Acquisition + Compounding 已覆盖一部分原则，因此是否需要任何新 production 规则尚未证明。优先先测“旧资产在 6—10 章无升级窗口里是否仍改变选择和新问题”，避免恢复奖励税。

### 13.9 Immediate Social Repricing 的强度边界

已冻结原则是：Public Proof 的价值在于有利害关系者重新估价并改变行为，而不是群众震惊。尚未确定的是：**一次重要公开证明是否应更稳定地立刻改变某项现实分配**，例如报价、资格、挑战规格、敌策或合作条件。

不能直接升级成“每次显露都必须发奖励”。它需要验证即时 repricing 是否增强爽感而不制造机械奖励、关系免罪或状态税。

### 13.10 Doupo Feel Engine / 正文气质

工作树中存在 `real-exp-doupo-feel-engine-20260827-v1` 与相关 prompts，但尚未形成可确认的最终 RESULTS。不要把它当已验证结论。其当前最有价值的未冻结线索正是上面的 Visible Desire Horizon / Reward Lifecycle / Immediate Social Repricing。

### 13.11 Human Prompt 的人格菜单风险

当前 Human Prompt 仍列出钱、审美、身体欲望、好奇等例子。它比单一 Core Obsession 好，但 Luna 可能机械从菜单抽 2—4 个组合。尚未有跨样本失败证据；继续观察，不因理论洁癖立即加 negative rule。

### 13.12 “4—6 次质变”是否会变成新 Hard Pattern

目前实验自然产生 5—6 次，未见明显机械凑数。但第一性原则是 early/mid/high-tier 有真实质变，数量应由具体 Power grammar 决定。低优先级观察项。

### 13.13 当前并行未提交工作

Reader Orientation、World Entry、Competence Filler 与正文 Skill 的 production 修复已随 `15a389d` 提交；第一份 Handoff 已随 `1760c9a` 提交。当前仍未提交的是一处 `MVP_PRODUCT_DIRECTION` 文档对齐、若干早期/中间实验与研究脚本、尚未完成的 Doupo Feel Engine，以及作为 provenance 保留的 `DEEP_CONTEXT_HANDOFF_2.md`。接手者应先识别 owner/意图、审阅 diff、运行测试，再决定如何分批处理；不能把它们与下一实验混成一个 commit。

---

## 14. Immediate Continuation

下一位 Agent 最自然的工作不是继续给 Story Program 加一句“不同人格要不同能力”，而是完成一个可归因的 **Matched Decision Point + Route-specific Opportunity A/B**。

### 14.1 目标

验证：

> 同 World + 同 Core Power + 同一具体冲突/机会池，仅 Human 不同，是否先产生不同选择；这些选择是否真实限制后续机会；在不削弱 Growth Floor 的前提下，是否形成机械上明显不同的新 Asymmetry Tree。

### 14.2 推荐实验设计

#### Phase A：Matched Decision Point

冻结：

- 同一 World；
- 同一 Core Power；
- 同一地点、时间、人物和三个并列机会；
- 同一信息与代价；
- 3 个动机排序明显不同的 Human。

让每个 Human 只回答：

- 选什么；
- 为什么是这个具体的人会这样选；
- 立即错过什么；
- 实际进入哪条路线。

不要让 Sol 自行改写触发事件。

#### Phase B：Route-specific Opportunity Treatment

对每个 Human 做 A/B：

- **A baseline：** 当前 Story Program，可从完整 World 规划新优势；
- **B treatment：** 新 Power Asymmetry 只能来自该人物已选择路线中实际进入的人、物、地点和事件；不能从未进入的 World 机会池挑最适合 Core 的全局答案。

B 不是“人格类型→能力映射”。人格只通过选择限制路线，路线再限制机会。

#### Phase C：长期投影

让 Story Program覆盖自然的约 200—300 章，比较：

- 第二、第三 Asymmetry 是否在机械上真正不同；
- 是否只是同一机制换载体/用途；
- 新旧复合是否具体；
- 所有 Human 是否仍有强 Growth Floor；
- 是否出现“牺牲成长后宇宙补偿更好外挂”；
- 是否仍存在反控制、第三方案、救具体人等共同道德最优收敛；
- Audience knowledge、ruler、ascension 是否自然工作。

### 14.3 成功条件

- Matched Decision Point 中选择随 Human 分叉；
- route/opportunity 因果可追溯；
- 至少多数 Human 的第二/第三优势不是同一底层机制换皮；
- 所有人持续成长，不因关系/享乐/审美路线失去男频分量；
- Treatment 不直接按人格发外挂；
- 不新增 Agent、数据库或硬配额；
- 跨至少两个 World 复验后，才考虑 production 化。

### 14.4 若实验通过，最小 production 修法候选

只在 Story Program 长期成长合同中增加极短的 authority 边界，例如：

> 后续新 Asymmetry 应从主角真实选择后进入的路线与实际机会中获得；不得绕过已发生的路线选择，从完整 World 中直接挑选与 Core 最优复合的全局奖励。

是否采用、如何措辞，应由实验决定。当前不要提前冻结。

### 14.5 工程收尾顺序

1. 先保护当前 dirty worktree；
2. 明确实验目录与 frozen inputs；
3. 用 ACP 跑真实 Sol/Luna；
4. 写 RESULTS，区分 PASS/PARTIAL/FAIL；
5. 若不通过，只提交实验证据，不改 production；
6. 若通过，做最小 Prompt/docs/test 修改；
7. full regression；
8. 只 stage 自己的文件/hunk；
9. 使用固定 Git identity 提交推送。

### 14.6 第二优先研究队列

如果 Personalized Advantage Tree 已完成或用户明确转回《斗破》式商业可追读性，第二优先不是再加一批 Prompt，而是分别做三个窄 A/B：

1. **Visible Desire Horizon / Dominant Commercial Engine**：冻结 Human，比较“阶段有一个真正可追踪的具体欲望”是否提升 20—40 章牵引，同时不覆盖人物；
2. **Reward Lifecycle / Fantasy Heartbeat**：选无境界升级窗口，验证旧能力/物件/身份是否通过使用、社会兑换和复用继续产生幻想心跳，而不是增加奖励频率；
3. **Immediate Social Repricing**：比较重要公开证明后是否改变一项现实分配；拒绝机械“显露=发奖”。

三项目前都属于 Experimental Hypothesis。只有单变量、跨 Human、跨样本结果稳定后才可 production 化。

---

## 15. How to Work With the User

### 15.1 默认中文

所有交流使用中文。小说、Prompt、审计和文档优先中文；技术名词可保留必要英文。

### 15.2 用户要的是判断，不是清单替代判断

应直接说：

- 哪个问题真的成立；
- 哪一层是根因；
- 哪些部分已经正确；
- 最小修法是什么；
- 为什么一个看似合理的替代方案仍然错。

不要用评分表、无穷 checklist 或“进一步优化即可”回避判断。

### 15.3 第一性原则优先于补丁

用户会反复拒绝：

> 为当前一本书加一个局部 Prompt patch。

每次都应问：下一本全新书是否仍会复现？若会，修最早层；若只在当前 scene，才修正文。

### 15.4 证据要来自实际输出和代码

不要只说 Prompt 看起来合理。用户重视：

- 实际 novel output；
- A/B；
- 当前 code/runtime；
- tests；
- GBrain stats/retrieval；
- 明确反例。

### 15.5 不要过度防御或制造发现

按用户工程范围：

- 不加无用途哈希/校验和；
- 不为不可达角落加兼容层和防御脚手架；
- 不因“可能”就加守卫；
- 不反复审自己的补丁而不完成工作；
- 对的就说对，不制造问题交差。

### 15.6 长任务要更新进度，但不要报告低层操作

用户会问“到哪儿了”。应每隔一段时间简短说明：当前已完成什么、发现什么、剩什么。不要承诺后台工作或让用户等待。

### 15.7 用户说“审计”时有固定协议

自动调用当前激活 `tgn-system-steward` 独立审计，同时自己复核，最后给统一结论。Steward 不进入 production。

### 15.8 Docs 要言简意赅

稳定变化同任务更新 current docs；优先删旧、替换、合并，不不断新建文档。历史证据放实验目录。

### 15.9 Git 与并行工作

- 不覆盖其它 Agent 的本地改动；
- 只 stage 自己的文件/hunk；
- commit identity 固定；
- 有效修改后测试、提交、推送；
- 不把无关 untracked experiments 顺手提交。

### 15.10 不要过度声称完成

如果只是架构支持、但未专项验证，要明确说“架构允许，尚未证明稳定”。用户非常重视这个区别。

---

## 16. Do Not Regress

未来模型最容易退回以下错误理解：

1. 把 Fantasy First 恢复成一个统一 Fantasy Seed；
2. 让 World、Power、Human 在同一模型里互相合理化；
3. 把人物写成童年证明的人格论文；
4. 把所有人物净化成理性、负责、反控制的优等生；
5. 把关系自治写成永久平等谈判；
6. 把 Growth 恢复成每阶段升级/奖励税；
7. 或反过来以人物为由让主角长期不变强；
8. 把 Power 简化成弱小便利工具；
9. 用复杂术语冒充能力创新；
10. 让同一 Core 只做距离、数量、持续时间放大；
11. 让新优势从全局 World 最优解自动掉落，而不尊重实际路线；
12. 把人格直接映射成能力类型；
13. 为关系型选择立即安排宇宙补偿奖励；
14. 把公开证明写成多轮专家验证；
15. 把“大家震惊”当作社会重新定价；
16. 把世界独立写成治理/资源分配模拟；
17. 把能力写成探路、维护、诊断、运输、生产职业；
18. 为低动作章发明 Competence Filler；
19. 为已批准入口/奖励补试工、考核、登记等资格税；
20. 因反百科而不给读者必要世界坐标；
21. 因重视解释而增加 Prelude、每章 World KPI；
22. 把 shock 等同隐藏血统；
23. 把 Secondary Axis 变成每书副职配额；
24. 把 Payoff Debt 变成所有 Promise 的倒计时；
25. 把 GBrain 当 Canon 或让 raw source 进入 Writer；
26. 看到经典作品机制就不经 A/B 直接上线；
27. 为每个新问题增加 Reviewer、Agent、Scorer、数据库或 Hard Gate；
28. 把 current implementation 当永恒原则；
29. 把单本/单候选实验宣称为系统完成；
30. 覆盖当前 dirty worktree 或混提交无关文件。

---

## 17. Compact Operating Constitution

1. TGN 写的是成熟中文男频成长长篇：力量要馋，成长要真，人要活，世界要大。
2. Fantasy First 是读者价值优先级，不是统一 Seed。
3. World、Power、Human 独立；Character 确定性组合；Story Program 才第一次 Collision。
4. 世界没有主角也有故事，但世界独立不等于治理模拟。
5. 人物是多股欲望与具体关系中的人，不是童年证明论文。
6. Core Power 一句话能懂、明显超标、边界防万能但不抹平爽感。
7. Spark 负责不同，Privilege Delta 负责强。
8. Growth 是全书纵向不变量，不是阶段/块/章节税。
9. 系统保证 Growth Floor，Human 决定 Route Freedom。
10. 后续新优势必须通过真实故事获得，与旧优势形成复合；不每阶段强塞。
11. 尺度要长期出现，完成比较后立即推进 State。
12. Public Proof 的终点是世界重新定价，不是重复震惊。
13. High-Value Acquisition 可选；一旦发生必须有后续生命。
14. Supporting Logic 只支撑因果，不自动成为故事发动机。
15. 高价值 Orientation 可以直接说；低价值重复解释和实施必须压缩。
16. Shock = 意外 + 回看成立 + 重大状态变化，不等于隐藏身世。
17. Outline 只编译，Director/Writer 不临时发明长期权威。
18. GBrain 是小型可选 craft inspiration，不是 Canon。
19. 先找最早语义坍缩点；少深规则胜过多 Gate。
20. 实验冻结上游、单变量、无 cherry-pick；人格因果使用 Character Authority Invariance + Matched Decision Point。
21. 对的就冻结；证据不足就保留 OPEN，不为完成感硬改 production。
22. 当前最自然下一步：验证 `Choice → Route-specific Opportunity → Different Advantage Tree`，同时保护所有人格的男频 Growth Floor。

---

## Cognitive Integrity Check

阅读本文后，一个新 Agent 不应只知道“项目采用了哪些 Prompt”，还应能够面对新案例作出以下判断：

- 一个关系型主角放弃力量试炼并不违背男频，只要长期 Growth Floor 仍成立；
- 一个力量型主角选择留下也不表示人物薄弱，关键在选择是否来自 Human；
- 一个炼药系统可以是强幻想轴，也可以只是工作流，区别在于它本身是否值得追到顶；
- 一段直接世界说明可以是高价值 Orientation，而五次专家确认仍然是水；
- 一个世界很适合主角发挥并不自动失去独立性；
- 一个能力简单不应被自动削弱；
- 一项结构机制即使让故事更整齐，只要覆盖人物选择就应失败；
- 四个 Story Program 看起来不同，如果触发事件也不同，就不能纯证明人格因果；
- 人格改变路线已经成立，不等于人格化优势树已经完成；
- 新实验若只解决一个子问题，应明确 PARTIAL，而不是宣布上游完全收敛。

只要下一位 Agent能稳定作出这些区分，本文迁移的就不只是 conclusions，而是当前对话长期形成的 decision model。
