# DEEP CONTEXT HANDOFF

日期：2026-08-30
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
3. 截至 2026-08-30 的已验证结论、当前实现、并行工作状态与下一步实验。

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
→ Authority Reviser
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

### 3.14 High-Value Asymmetry Reveal = Crowd Shock + Ruler Calibration + Behavioral Repricing

公开/选择性显露不能因为反群体吹捧而过度克制成一个停顿。高价值非对称优势显露按现场条件可以同时承载三条**并列、没有高低之分**的 reader-facing 通道：

> **Collective Shock / Field Reaction**：现场本来有足够见证者时，全场鸦雀无声、喧哗骤停、所有人明显震惊、集体退开/围拢本身就是有效爽点，负责让读者感到“整个场子真的被撼动”。
>
> **Ruler Calibration**：最有资格者在自己的知识边界内，用短而明确的判断告诉读者“正常同层/同类通常能做到什么 → 主角这次具体超出哪里 → 为什么罕见、异常或值得重新判断”。
>
> **Behavioral Repricing**：至少一个有资格、有利益或有关系位置的观察者，因为新证据真的换了动作——停手、改口、加价、退距、换战术、招揽、敌视、保护或重新安排准入。

大型 Public Proof 可以三路一起吃满；不要以“克制/避免吹捧”为由自动删群众震动。只避免凭空造观众、让所有人轮流说同一套专业解释。以下节点应重新校准：Core Asymmetry 首次被外界看见、新层级/质变、新旧 Asymmetry 第一次复合、进入更高圈层后的首次重新观察、旧社会估值明显落后时。短期群体震动可以当场成立；只有 Repricing 继续改变后续资源、关系、敌意、战术、准入或信息流时，才升级长期 Ripple。

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

### 3.25 Long-History Fact Boundary：未知旧事实不是 Writer 的自由补全区

如果 Canon / Curated Context / Open Promise 已明确某段过去是未知、未解释、真假未定或原因未明，Writer 不得为了让场景完整而补出几十/几百章前的秘密经历、旧对话、隐藏动机、既有知识或世界机制。只有 Director Contract 明确让某个新事实在本章成为确定事实，才能改变 unknown boundary。

这与 Reader Orientation 不冲突：**已批准的公共事实可以直接说清；未批准的历史答案不能被 prose completion 偷偷发明。**

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

### 4.13 Public Proof / Social Calibration 的双层职责

公开证明不追求所有人完全理解能力，也不要求连续专家认证；但过去“只要有人换动作就够”的版本过于克制。当前更准确的编译目标是：

> **场景层：Collective Shock + Ruler Calibration + Behavioral Repricing。** 有真实观众时群体震动本身成立；最有资格者用短专业判断校准正常值/超标点/稀有意义；关键人物再用行动证明社会价格改变。
>
> **长线层：Disclosure → Repricing → Ripple。** 只有当这个新估值在后续场景继续改变资源、战术、关系、敌意、准入或信息流时，才进入长期 Story/Canon。

好的短期结果可以只是：对手停手并改变试探，教头/长老说明“常规一阶/三阶本来只能怎样，而这次已经越出常规范畴”，然后马上继续比赛。它已经是完整爽点，不必硬接招揽/追杀。

坏的结果有两种：五个人轮流说“确实不是运气”；或者为了反群体吹捧，只写一个“教头站起来/众人沉默”，却不告诉读者为什么这个结果在当前力量尺上真正异常。

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
GBrain 离线深蒸馏 → source-blind Scene Deep Craft → Curator short Projection / Reviser short Watch
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

### 6.4 章节长短服从信息价值，不服从统一压缩目标

节奏好坏不能用字数判断。曾经 Ch2 从四千字压到约一千五百字是进步，因为删掉的是重复 Verification；后来 Ch1/Ch3 因 Opening Orientation / World Entry 变长同样是进步，因为新增的是高价值读者坐标。正确目标是：**低价值实施和重复更短，高价值世界进入、冲突、幻想兑现和人物选择可以占更多篇幅。**

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

### 9.10 Matched Decision Point + Long-History Fact Boundary：Steward v0.1.13

v0.1.11 已建立 Matched Decision Point；v0.1.12 进一步要求决策点对每个被测 Human 至少有两个真实有价值、不能同时完整取得的方向，并保留未选路线的主要机会成本，不能用隐藏奖励立即抵消。同时把 Long-History Fact Boundary 纳入正式审计：公共事实可以说明，未知旧史不能由 Writer 补造。

Skill lint、package validate、安装、激活及双案例 smoke 均通过：旧史被 Writer 补成确定事实被判 FAIL / authority breach；选择虽分叉但机会成本被更强隐藏奖励完全抹平，被判 INVALID / CONFOUNDED。

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

### 9.18 Long-History Fact Boundary：已冻结并经长篇压力验证

Chapter 120 / 600 压力 A/B 已验证：当旧历史被标记为 unknown / unresolved 时，Primary 必须保持未知纪律，只能写当前动作、即时证据、对白和暂时判断；不能为“完整感”补造 retrospective canon。当前 Runtime 还会把未解事项投影成 bounded `UNRESOLVED FACT BOUNDARY`，不增加新的模型调用。

这条与 Orientation 的共同边界是：**该知道的公共事实可以直接说；尚未批准的历史答案不能由 Writer 自行补。**

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
- 本次最终融合校准时的 source baseline HEAD：`bad80ae docs: finalize deep context handoff`；接手时仍应 live-check HEAD，不把该 commit 当永久事实。
- 前一关键提交：
  - `1760c9a docs: add deep context handoff`
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
→（可选）Non-Canon Premise Forge S1/S2/S3
→ Independent Premise Authority Compiler
→ 作者批准 Premise Contract / 显式跳过
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
→ Authority Reviser
→ State Extraction
```

没有 production Fantasy Seed，没有 Character Composer LLM。Premise Aperture 是可跳过、可丢弃的开书搜索/编译阶段，不是第四 Authority；保存候选后必须 strict PASS + exact Compiler Input + 作者批准，或显式跳过。

### 11.3 当前批准点

1. 可选 Premise Contract；
2. World Vision；
3. Character（Power + Human 一次批准）；
4. Story Program。

### 11.4 当前重要模块/文档

- `PROJECT_RULES.md`：唯一长期项目执行权威；
- `docs/MVP_PRODUCT_DIRECTION.md`：产品目标、创意权威、Anti-Goals；
- `docs/PIPELINE_METHODOLOGY_AND_VALUES.md`：分层方法论；
- `docs/PREMISE_APERTURE.md`：可选开书 Premise Forge / Compiler / Author Gate / lane contract 真源；
- `docs/SPLIT_CHARACTER_AUTHORITY.md`：World/Power/Human/Collision 边界；
- `docs/GBRAIN_STORY_CRAFT_V3.md`：GBrain 接入与蒸馏；
- `docs/CHAPTER_RUNTIME_AND_STATE.md`：章节、Canon、State；
- `docs/NOVEL_PROSE_REALIZATION.md`：正文表达；
- `docs/AUTHOR_WORKSPACE_UI_SPEC.md`：UI；
- `tgn-system-steward`：AgentDock 审计 Skill；当前激活 **v0.3.20**。已包含 Premise Search / Compiler / production state audit、Atomic Obligation、Post-Writer Authority Revision、Scene Craft Evidence & Runtime Bandwidth，以及 Asymmetry Reveal / Social Calibration Trace；Steward 仍以 live discovery 读取 production，不把完整系统快照写死在 Skill；
- `.agents/skills/novel-prose-realization/`：正文实现 Skill；Reader Orientation / Supporting Skill compression 更新已随 `15a389d` 提交。

### 11.5 当前关键实验

- `books/real-exp-second-pass-authority-revision-20260827-v1`：冻结 Primary Draft 的 Second-Pass Authority Revision A/B；确立 Preservation First、safe Authority Refresh、Reader Release 逐条核对与 Consequence 保护，并比较 Luna low / medium / high / xhigh / max；production 选择 Luna high。
- `books/real-exp-doupo-system-mechanisms-20260827-v1`：三项《斗破》机制 A/B；
- `books/real-exp-personality-advantage-tree-20260827-v1`：四 Human 优势树实验，结论 PARTIAL；
- `books/real-exp-private-prototype-orientation-world-entry-final-20260827-v1`：Reader Orientation/World Entry 最终五章回归；
- `books/real-exp-private-prototype-asymmetry-novel-20260826-v2`：闻野舟/夺势五章与主观审计；
- `docs/research/DOUPO_FULLTEXT_TGN_ARCHITECTURE_STUDY_20260827.md`：全文研究；其中较早的架构建议须用后续 A/B 校准。

### 11.6 测试状态

Scene Skill v2 production 冻结后的最新完整回归为 **310 passed**；同时通过 Scene Runtime focused tests、`git diff --check`、Skill lint/package validate/install/activate 与 production coherence audit。当前 Scene Skill v2 冻结提交为 `540743c feat(story): upgrade scene skills v2`。由于工作树仍有并行未提交内容，任何后续开发仍应先 `git status` 并按任务重跑相关专项测试。

### 11.7 GBrain 当前真实状态

当前实测：

- Pages：3827
- Chunks：15856
- Embedded：15850

即 **还有 6 个 chunk 未 embedding**。这与某些旧 docs 中历史上的 `Embedded == Chunks` 状态不同；以当前 stats 为准。最近《斗破》全文 Story Craft / Longitudinal / Mentor Knowledge 等材料已存在，但 GBrain 更新交付仍不能标记完全结束，直到执行 `embed --stale` 并验证 `Embedded == Chunks`。

### 11.8 Authority Reviser 已进入当前 production

章节实验暴露了一个与“上游事实是否正确”不同的问题：Primary 为了集中注意力只吃近端压缩上下文，虽然能更好地完成场景，但会丢失远端、已批准且更准确的 World / Power / Human realization。把完整远端资料重新塞回 Primary 会重新放大上下文与注意力负担，因此当前采用**两遍职责分离**：

`Director → Curator → Terra Primary Draft → Luna high Authority Reviser → State`

Authority Reviser 不是第二 Writer。它只读取冻结 Chapter Mission、Curator、safe `WORLD AUTHORITY`、逐条 `Reader Release`、`CHARACTER.md` 的 Frozen Power + Human Core、Canon 与 Primary Draft；raw GBrain OFF。默认 **Preservation First**：没明确问题的段落逐字保留，只删/压重复确认、重复证明、工程化/程序化 Supporting Implementation、Competence Filler，只补 Authority 已批准但第一版漏掉的最短世界/人物/力量 realization；不得改剧情结果、人物选择、状态变化、章末推动或 unknown boundary。

选择 Luna high 的证据不是“更贵所以更强”。同一最终 Revision Contract、同一冻结 Ch5/6/9/10 Primary Draft 上：low 5/7 关键检查；medium 6/7 且 Preservation 最好；high 7/7；xhigh/max 同为 7/7 但更慢、改动更多。当前 default 因 coverage stability 选 high；这仍是 Current Default，不是 Stable Principle。

**State closure 是硬接线**：`curator_primary` 不允许 Primary 直接成为 `final_source`；State 后端从 Run Ledger 重新读取 `authority_reviser` 或显式 repair 后的 `integrator`，页面粘贴的 Primary 不能旁路进入长期 Canon。Optional Specialist/Integrator 也必须以 Authority Revision 为底稿。

2026-08-29 又冻结了两个由真实 20 章快节奏 E2E 暴露的章节 Authority 问题。第一，Future 10 条目现在在进入 Director 前确定性拆成 `本章唯一可执行事件预算` 与 `章末 Handoff Reservation`；Long Block 只是阶段背景，不能授权 Director 提前执行下一章付款、正式身份、获得、升级或其它结算。第二，当前章 `结果 / 状态变化` 不再依赖 Director 重述：runtime 将其确定性并入 Frozen Mission 的 `状态变化`，；不再额外重复投影给 Primary/Reviser。真实 Ch19 证明仅靠 Prompt/可见性仍不足：Luna Director、Terra Primary、Luna Reviser 都曾把批准的“顾停舟本人进入镇海”合理化成“镇海级战绩”。因此 Run Ledger 新增**同一 Authority Reviser 的一次性条件 Outcome Repair retry**：只检测计划中以“进入 / 踏入 / 晋升 / 突破 / 成为”明确批准、而最终稿仍未直接落成的显式里程碑；普通章节零额外调用。第一次漏掉就不能 adopt / 不能进 State，自动准备窄 Preservation-First Repair Prompt；最多一次，第二次仍漏则保持 failed。真实旧 Ch19 自动 Repair 用 Luna high 85.4s 通过，明确恢复“本人进入镇海”，与原 Revision 正文相似度约 96.75%，没有重写战斗。网页 UI 与 Codex External apply 都服从同一 Run Ledger gate。

---

### 11.9 当前最重要的问题

不是“人格能不能改变剧情”——这一点已经 PASS。

当前核心未决是：

> **人格能否通过真实选择与路线，稳定改变第二、第三项非对称优势的种类，而不只是改变同一优势的用途。**

现有四线实验中，所有人都拿到剥纹，说明 Story Program 会从整个 World 选择与 Core 最容易复合的全局最佳机制，route-specific opportunity 对新优势的约束还不够强。

---

### 11.9 Scene Skill v2：Deep Research / Narrow Runtime

2026-08-28 的深度 Scene Craft 研究把经典长篇重新按场景问题定向细读：source-specific bounded windows 先由 Terra 做 locator / anchor / observation Fidelity Audit，再由 Luna 做跨书 synthesis，最后由受控 A/B 决定哪些判断可以进入 production。最终冻结研究覆盖 **64 条 source-first lanes、26 本经典长篇、857 次 bounded-window Fidelity 审核**，其中 21 个不可靠窗口被剔除；这些数字是研究证据，不是 Runtime 配额。研究层允许很深，但 source 书名、原文、locator、完整 Generation/Revision Lens 不进入章节 Writer。

当前 production 保留 **24 个 Scene Primary**，没有因为 Combat 很重要就拆出十几个新 Primary。战斗的势均、弱打强、碾压、适应、保护、团队、大战、规则/远程等都作为 `combat` 内部 posture / conditional：只有新的 Reading Question、持续 scene state、beat engine、Stop/Handoff 都不同，并且 `existing Skill + compact conditional` 的 A/B 仍不足，才允许新增 Primary。

运行时分三层带宽：

1. `scenes/*.md` 保存 source-blind **Deep Craft**，供研究/维护；
2. Curator Catalog 只暴露 `skill_id + Primary Reading Question + 一行 Projection Guidance`，有真实 realization 缺口时编译 2—4 句 `Scene Prose Projection`，已经清楚则 `NONE`；
3. Terra Primary 不再读取完整 Scene Skill；Luna Authority Reviser 也不读完整 Revision Lens，只在该 Skill 有直接 A/B 支持时追加一行 failure-triggered `Revision Watch`，否则不加。当前只有 `social_bargain_decision` 与 `relationship` 两张 Watch 开放，其余 **22/24 = NONE**。

双盲 Primary A/B（Luna + Sol）支持“Deep Research → Curator short Projection → Terra”作为默认方向：删掉完整 Skill 注入没有系统性丢失关键 craft，反而减少了深规则变成流程、教程和 prompt bloat 的风险。Reviser A/B 同样说明完整 Revision Lens 不应常驻；Preservation First 优先。

另保留三个**非 Primary 的 Shared Reference Lens**：`character_voice_pressure`、`world_entry_lived_texture`、`desire_temptation`。它们用于升级/校准 Scene Craft 与 Curator 投影，不进入 Primary Router，也不构成每章配额。

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
| Curator | GPT-5.6 Luna | high | raw GBrain OFF；Scene Skill v2 compact Catalog → short Projection |
| Primary Writer | GPT-5.6 Terra | high | raw GBrain OFF；只吃 Curator short Scene Projection；第一版草稿 |
| Authority Reviser | GPT-5.6 Luna | high | raw GBrain OFF；safe Authority Refresh Pack + optional short Revision Watch；Preservation First |
| State | GPT-5.6 Luna | low | OFF；只读最终正式来源 |

默认章节链：

> `Luna Director → Luna Curator → Terra Primary Draft → Luna high Authority Reviser → Luna State`

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

### 13.9 Asymmetry Reveal / Social Repricing 已从假设升级为稳定方法，但 production wiring 仍在继续

2026-08-28 已完成专项 Evidence-first Deep Distillation：6 本经典小说、16 个 bounded canonical windows，覆盖 private / selective / public / accidental / secondhand disclosure，以及普通人、专家、rival、利益方、敌对者、亲近者和 NONE / next-scene / multi-chapter ripple。Terra high 负责 canonical fidelity，Luna high 综合 Scene Craft，Sol high 综合 Story/Ripple。

稳定结论已经不再是“要不要多写震惊”，而是两层：

> **Scene：Collective Shock + Ruler Calibration + Behavioral Repricing。** 三条是并列 reader-facing payoff：真实群众可以完整震动，最有资格者说清正常值/超标点/意义，关键人物用行动完成重新定价；大型 Public Proof 可以一起吃满，并在新层级、新复合、新圈层和旧估值过时时重新校准。
>
> **Story：Disclosure → Repricing → Ripple。** 只保存“谁实际知道/相信什么”；只有后续独立行动继续被新估值改变时才升级成长期 Ripple / Canon。

两张最小 PILOT 资产已经形成：`mech-disclosure-repricing-ripple-v1` 与 `prose-control-observer-specific-repricing-v1`。顾临川 Ch1/Ch2 Scene-level 与 Story Program production-shaped ON/OFF 为 **DIRECTIONAL PASS**：能更稳定产生报价、挑战规格、Counterplay、知识不完整与专业尺，而没有自动制造“每次显露都追杀/招揽”的新税。

仍未冻结的是具体 production wiring：当前更优候选是 Story Program / Outline 负责长期 Disclosure/Ripple，现有 `showcase_evaluation` / public-proof 类 Scene Craft 通过 conditional short Projection 承担现场双通道校准；**不要新增 Disclosure Ledger、旁人震惊 Agent 或独立 Asymmetry Reveal Primary taxonomy。**

GBrain 两张卡已完成 import + embedding + keyword retrieval regression；当前 runtime 为 **3829 Pages / 15858 Chunks / 15858 Embedded**，embedding debt = 0。研究资产门禁已完整通过，但仍只属于 PILOT / production-A/B ready，不等于默认 production wiring 已冻结。

### 13.10 Doupo Feel Engine / 正文气质

工作树中存在 `real-exp-doupo-feel-engine-20260827-v1` 与相关 prompts，但尚未形成可确认的最终 RESULTS。不要把它当已验证结论。其仍值得继续研究的是 Visible Desire Horizon / Reward Lifecycle；原先的 Immediate Social Repricing 线索已被 2026-08-28 的跨书 Asymmetry Reveal / Social Calibration 蒸馏部分 supersede，不再当作未研究假设。

### 13.11 Human Prompt 的人格菜单风险

当前 Human Prompt 仍列出钱、审美、身体欲望、好奇等例子。它比单一 Core Obsession 好，但 Luna 可能机械从菜单抽 2—4 个组合。尚未有跨样本失败证据；继续观察，不因理论洁癖立即加 negative rule。

### 13.12 “4—6 次质变”是否会变成新 Hard Pattern

目前实验自然产生 5—6 次，未见明显机械凑数。但第一性原则是 early/mid/high-tier 有真实质变，数量应由具体 Power grammar 决定。低优先级观察项。

### 13.13 当前并行未提交工作

截至 2026-08-28，Authority Reviser、Public World Knowledge Clarity、Social Calibration 与 AGGRESSIVE payoff 均已进入当前 production。最新又完成 **Variation / Secondary Fantasy / Naming Craft** 根修：World 的 Small Grammar 不再被误读为 Small World，而会主动把变化预算花在招式/战斗姿态、身体/物种、兵器/奇物、异兽/伴生物、环境与复合；World 主动寻找 0—1 条成熟 Optional Secondary Fantasy Road，Story Program 主动检查，但 Human 决定主角是否投入。Power Seed 新增可完全忽略的 Optional Lexique Primitive Pool，只在同一主异常上提供 concrete carrier / gameplay 灵感；另固定读取一条由 69 个 source-first 小说来源蒸馏出的 source-blind Naming Craft Reference。当前专项测试 `34/34`、全量 `324/324` PASS。

当前激活审计技能为 **`tgn-system-steward 0.3.8`**：在既有 `Public/Known World = Clarity`、Social Calibration、Plan Compression、Authority 等审计上，新增三条稳定判断：**Small Grammar ≠ Small World**；成熟 Secondary Fantasy Axis 不得因反工程化被被动删掉，World 可主动找候选但 Human 决定是否成为主角道路；Naming 语义先于气味，lexique 只能提供可丢弃 semantic primitive / naming fragrance，名字不能反向授权机制。

**Public main 已冻结。** `main` 当前 release commit / freeze tag：`10520df97c3729ef2c970035a9e031ccf15754ce` / `tgn-freeze-2026-08-28-v1`。main 是 public production freeze，不能 fast-forward / merge dev 私有历史；发布必须以现有 main 为父节点构造 clean release commit，只带 production code、必要 runtime skills、构建配置与可公开测试。`docs/`、Handoff、`PROJECT_RULES.md`、Steward、temps、内部实验 provenance 不得进入 main；本次 main 当前树敏感路径检查为 NONE，release 测试 316/316 PASS。注意：旧 main 历史在本次规则建立前已经存在 docs；本次只清理当前树并防止未来再次加入，没有做 destructive history rewrite。

当前工作树仍有并行 owner 的 `docs/MVP_PRODUCT_DIRECTION.md`、`src/story_mvp/hybrid_runtime.py`、`tests/test_mvp.py` 等修改与大量 Scene Skill / Doupo / Orientation provenance；`DEEP_CONTEXT_HANDOFF_2.md` 仍为旧 provenance。接手者必须先看 `git status`，只 stage 自己的文件/hunk。

---

## 14. Immediate Continuation

### 14.1 Variation / Secondary Fantasy 已冻结为 current default

当前最重要的新判断不是继续减少力量规则，而是：**Small Grammar ≠ Small World；克制 Grammar，放纵 Fantasy Surface。** World 已经能用少量普通话讲清主力量、且一到少数互补轴有辨识度时，应保护它；不要为统一而改成元能量。丰富度应优先来自新招式/战斗姿态、身体与物种差异、兵器/奇物、异兽/伴生物、会改变用法的环境、组合、越级对象与稀有例外。

World 会主动寻找 **0—1 条 Optional Secondary Fantasy Road**：只有一条职业/专业/技艺即使完全不反哺主战力，仍有独立强弱、顶层人物、作品/胜负、稀有成果与社会价格，才算成熟副轴。Story Program 主动检查 Approved World 中这样的道路，但是否让主角投入由 Frozen Human 的具体欲望决定；Human 不想走时，副轴继续属于世界或配角。不要因为过去反工程化，就把炼药/炼器/作品竞争等真正可欲望的第二幻想轴一律压回背景。

本轮 World A/B：影子世界与伤痕世界 Treatment 胜出；兽印世界 TIE，说明不能为了“更 Small Grammar”压掉原本有辨识度的兽印副轴，只吸收高价值 Variation / 兵器师道路。Story Program 用三个不同 Frozen Human 复验均 PASS / DIRECTIONAL PASS，未把人物统一推成成长最优路线。

### 14.2 Lexique 现在有两种合法用途

`docs/MALE_WEBNOVEL_STRANGE_SETTING_LEXICON.md` 不再只被理解成“取名词库”，但仍不是 Canon 或完成设定库：

1. **Semantic Primitive Spark**：Power Seed 在原 `World Normal + Power Novelty Spark` 已成立后，拿一个很小的 `对象 × 变化` pool 做可丢弃偏航；每个 Candidate 最多借 0—1 个，也可以全部忽略。只有它为同一个主异常带来新的 concrete carrier / gameplay 才采用；不得改写 trigger、coverage、cost、Permanent Boundary，也不得长成第二系统。
2. **Naming Fragrance**：能力/对象大白话已经成立后，才用具体词根增加气味。首读准确高于世界气味；World 已建立、读者已学会的词根只有在不牺牲准确时才优先，lexique 次之，也可以不用。普通短名已经准确时不为“更独特”强改；名字比 authority 多承诺机制时改名字，不扩机制迁就名字。

强制“一 Candidate 一 primitive”的 A/B 大多失败；Optional Pool 方向更好。代表性成功例是 `影子 × 替代`：把抽象“死亡延迟”启发成“影子暂时顶替被打坏的心脏/脊柱继续行动，最终伤势仍结算”，明显增加身体画面与生存玩法；没有真实新玩法的 primitive 应直接忽略。

### 14.3 Naming Craft v1 已完成全库 source-first 蒸馏并进入 GBrain

命名研究不只覆盖 Scene Skill 的 26 本，而是当前已登记的 **69 个 source-first 小说来源（rcv0-01—rcv0-69）**。流程：确定性候选抽取（约 4,760）→ 10 批 Terra high Fidelity → Sol high 跨书 source-blind synthesis → Luna high Fidelity / Overgeneralization Audit。Audit 对原 synthesis 判 `REVISE`，主要防止“一个名字只能一个差异”和“世界词根 + 固定后缀”被误读成新模板；最终固定 Runtime Guidance 已按审计版冻结。

最终 Naming 模型：**语义先于命名；首读准确高于世界气味。** 类别可以由名称、句法、持有动作或人物关系承担，不规定四字结构或统一后缀；抽象/陌生名可以存在，但首见附近必须有类别、关系、风险、数量或兑现锚点；只给反复出现、影响决策、可争夺或社会流通的节点命名。词族只在真实来源/制造/持有/继承/制度/升级关系存在时建立，每个派生项还要有独立功能。普通短名已经准确、顺口、低学习成本时，不为了“更独特 / 更世界化”强行改写。

最终 9-candidate 冻结语义命名 A/B 在加入这条 accuracy guard 后为：**Treatment 2 胜 / Baseline 1 胜 / 6 平，Naming Gain LOW，Semantic Safety PASS，Directional PASS**。正例是 `影刻 / 影身` 比更泛的名字增加画面和世界贴合；反例是 `双行` 不如 `双成` 准确。因此 fixed Naming Craft 是低带宽定向/筛选参考，不是自动重命名器：语义平局时保留普通名，出现误读立即回退。

GBrain 固定卡：`syntheses/reader-facing-naming-craft-v1`，`REFERENCE_ONLY + active_inspiration=true`，只迁移 source-blind craft，不迁移原著专名。Power Seed 直接按 slug 固定读取，不占普通 Power creative inspiration 名额；其它阶段不重复消费。

最终 GBrain：**3830 Pages / 15859 Chunks / 15859 Embedded**，`Embedded == Chunks` PASS；`gbrain get`、keyword search、TGN 实际 `retrieve_gbrain(mode=power_seed)` fixed-reference smoke 均 PASS。完整 provenance：`reference-corpus/operations/gbrain-naming-craft-v1-20260828/FINAL_REPORT.md`。

### 14.4 当前验证与下一自然研究方向

production 已完成 World Fantasy Surface、Secondary Axis 主动发现/检查、Power Optional Lexique Primitive Pool 与 fixed Naming Craft Reference 接线；没有新增常驻 Agent、Reviewer、Scorer 或 Hard Gate。专项 contracts **34/34 PASS**，完整测试 **324/324 PASS**；`tgn-system-steward 0.3.7` 已 lint 0/0、validate、install/activate，并通过 bounded smoke：它不会因 Treatment 内容更多就自动判为过度，而会分别审底层 Grammar 与 Fantasy Surface。

这轮完成后，不要再继续为了“Variation”增加字段或副轴数量。下一自然研究方向仍可以回到：

1. `Choice → Route-specific Opportunity → Different Advantage Tree`；
2. 《斗破》式 Visible Desire Horizon / Dominant Commercial Engine；
3. Reward Lifecycle / Fantasy Heartbeat。

都继续遵守冻结上游、近单变量、真实输出先读、Human Invariance、AGGRESSIVE/保守版本若都 authority-safe 就交作者选择的实验纪律。

### 14.5 Progressive Long-form Authority 已进入 production（2026-08-28）

这轮解决的是一个比“副本流支持”更通用的长篇缺口：开书 `WORLD_VISION.md` 不应该被要求一次性写完 500 章所有具体大陆、文明、力量层和未来异世界；后期主角也不能一直拿 Chapter 1 的 Power/Human 状态继续做 Story Program。

冻结的新总模型：

> **Stable Origins, Evolving Authorities, Periodic Fresh Re-Collision.**

开书链仍是：

`World Root → Power Seed + Human Seed → deterministic CHARACTER.md → first Story Program → Outline → chapters / Canon`

当当前 World Horizon 真正被故事活透后，进入低频循环：

`Story Program World Horizon Handoff → protagonist-blind World Expansion → optional Human Development → deterministic CURRENT_CHARACTER.md → Sol Story Refresh / Re-Collision → author-approved refreshed Story Program → Outline → chapters`

#### World Rewrite 与 World Expansion 已正式分语义

- **World Root Rewrite**：回头改变已经成立的根规则/旧事实；仍按旧 stale graph 使 Power/Human/Character/Story/Outline 失效。
- **World Expansion**：旧事实不变，只向未来增加世界层；不 stale Origin Power/Human/Character，只刷新 Story/Outline 与 `effective_from` 之后的未来 Run。
- Expansion 触发是 Story Boundary，不是固定 100 章税；100 章最多是普通长篇的观察 horizon。
- `scope=macro`：新大陆/文明/力量圈层/社会世界层。
- `scope=instance`：真正独立 Local World，可有 `effective_until`；离开后 Local World 从章节 `WORLD AUTHORITY` 退场，跨世界 consequence 留在 Canon。

World Expansion 固定 **Luna high**、fresh context，且 protagonist-blind 一直贯彻到 GBrain retrieval：不读 Current Character、Power Stack、Human、关系、Story Program/Outline 或 BOOK 当前人物状态。它只创造世界现实。Story Program 的 Handoff 只负责 orchestration，**不注入 World Agent**，防止“当前主角需要什么”间接成为下一世界设计要求。

#### 两层 Power 已接通

1. `Power Origin Core`：`CHARACTER.md` Frozen Power；保存开局 Core Asymmetry 与根边界。
2. `Current Power Portfolio`：State Extraction 在 `PERSISTENT CANON → Power / Capability` 维护后续已经真实获得/证明的 Power、身体变化、兵器权限和 Advantage Stack。

后期神兵、传承、新能力/新 Asymmetry 等是 forward Power Delta，不回写 Power Seed。`CURRENT_CHARACTER.md` 会把 Origin + Current Power 一起交给后期规划。

#### 三层 Human 已接通

1. `Human Origin Core`：Frozen stable origin。
2. `Current Human State`：当前欲望、关系、承诺、身份等，继续由 Canon/State 变化。
3. `Human Development Delta`：只有长期已发生历史真的证明 Stable Choice Bias 变化时才允许新增；Luna high、GBrain OFF、看不到未来 World / Story / Reward，可直接返回 `NONE`。

Human Development 是比 World Expansion 更慢的可选时钟：多世界副本可以连续换几个 Local World 而一次都不跑。后续 Delta 按生效章节顺序保留；后期 Delta 可细化/改变早期偏向，但不能删除人物历史。

#### CURRENT_CHARACTER.md 是确定性 current authority，不是 Composer

代码从 Frozen Origins + Persistent Canon + Human Development 确定性编译：Power Origin + Current Power、Human Origin + Human Development + Current State，以及 relationships / identity / knowledge / assets / already-happened Canon。它不调用 LLM，不看未来 World，不创造新事实。Canon 更新会让已有 Current Character stale；普通章节 Writer 不整份读取它，仍使用 Frozen Cores + bounded Canon。

#### Story Refresh 是 Periodic Re-Collision

Sol high 第一次同时看到：

`Effective World（Root + active Expansions） × CURRENT_CHARACTER.md`

它不是把旧 Program 延长，而是 fresh collision。World 不为主角重写；人物也不为新世界优化。新 Power 必须从独立世界已经成立的真实机会中获得；旧 Power/物品/关系继续复利。每次 Refresh 仍只规划当前新 World Horizon，并继续留下下一次 `World Horizon Handoff`。

#### Story Program Handoff 已成为前向 Authority 边界

开书 Story Program 不再具体预写所有未来世界。当前 Horizon 后段若自然接近边界，输出 `## World Horizon Handoff`：可观察 trigger、`macro / instance` scope、为什么当前层已经需要扩、必须 carry forward 的已批准/已发生事实，以及固定 orchestration：`protagonist-blind World Expansion → deterministic Current Character → Story Refresh`。

若尚未到边界，写 `NOT YET`；不为格式强制扩世界。Outline / Review 不能越过未执行 Handoff 补满 Future 10 / 100 章；如果 Handoff 在当前十章内触发，只排到触发章即停止。批准/曾批准和 fresh/stale 分开：Outline 只有在 Story Program 已批准且 Workflow fresh 时才可继续；已有 Current Character 若 stale 也必须先刷新。

#### Chapter WORLD AUTHORITY 只吃 Expansion safe facts

`chapter_context` 按章节组合 Root + active Expansion，但只把 expansion 中已经批准的公共现实、力量/身份/价值尺度、公开地点/势力和具体价值物投给 Writer。世界人物未公开欲望、正在发生的隐藏行动、未知边界不会因为存在于 Expansion 就直接泄漏给 Writer；它们由 Story / Reader Release 决定何时进入。

#### State 为长期演化提供原料，但没有新数据库

`PERSISTENT CANON` 按需要维护轻量小节：`Power / Capability`、`Active Relationships`、`Identity / Access`、`Knowledge / Enemy State`、`World State`、`Tracked Assets`。只留以后仍会改变选择的信息。`World State` 是 protagonist-blind Expansion 唯一读取的 current Canon slice；不得混入主角私人欲望或未来设计请求。State Extraction 明确**不判断 Human Development**。

#### 单 Agent 自洽风险已做真实 A/B

实验：`books/real-exp-progressive-authority-20260828-v1/`

两个 Case：普通玄幻 Ch120 扩世界 + 多世界 Ch80 新 instance。比较：

- X：单 Sol high 同时做 World Expansion + Human Development + Current Character + Future Story；
- Y：独立 World → current facts → Sol Re-Collision；
- Z：独立 World + 独立 Human Development → deterministic Current Character → Sol Re-Collision。

两组 blind judge 都没有选 X。X 的典型问题恰恰是**太自洽**：世界材料、身份、冲突、奖励会自动对准当前主角能力/人格缺口，形成“教学世界 / 钥匙孔世界”，Surprise 被提前消化。Split World 更容易保留 NPC refusal、误价、绕路、错失和旧能力在陌生世界的意外用途。

跨 Case synthesis 选择 production topology Z；但两个 Human Development 输出均为 `NONE`，因此**独立 Human Agent 对真实稳定人格变化的净质量增益尚未单独证明**。它保留为低频 correctness mechanism，不宣传为已验证质量增益。

专项 `tests/test_long_form_evolution.py` 当前 **12/12 PASS**；全量 **336/336 PASS**。完整实验报告：`books/real-exp-progressive-authority-20260828-v1/FINAL_REPORT.md`。明确未解决：没有做真实 500 章 E2E；没有证明最佳 World Expansion 频率；没有证明连续 10—20 个副本 Macro Variation 已稳定；没有证明 Human Development 在“人物真的改变”Case 的独立增益。

### 14.6 Chapter Plan Execution Boundary + Explicit Milestone Outcome Fidelity（2026-08-29）

20 章 / 世界的第一世界压力实验暴露两个不同根因。**Cross-chapter spill**：第1章 Director 在已经完成“救人 + 保车”后，又提前做完原第2章的付款、核账和校路判断，导致下一章重复；修复不是再加一句“别提前”，而是 deterministic visibility separation：Future 10 的 `具体剧情 + 结果/状态变化` 是唯一当前章事件预算，`结尾推动` 变成只可制造压力/入口的 Handoff Reservation，Long Block context-only。用原第1章 fresh-context Luna high 回归后，Treatment 正确停在事故结果，把付款/正式结算留到下一章。

**Explicit milestone loss**：第19章计划明确批准“顾停舟本人进入镇海”，但最终 Director/Primary/Reviser/State 只兑现“顶住镇海战局”。连续受控验证表明：仅把 outcome 加进 Director Prompt、并入 Frozen Mission、或单独前置给 Primary/Reviser，模型仍可能用战绩暗示替代状态事实，因此 prompt-only 修法判 FAIL。最终冻结为：Plan Outcome 确定性并入 Frozen Mission + Run Ledger 条件检测；若已发生 Canon 真使原结果不可能，只接受 Director 在 `状态变化` 中显式写 `[PLAN OUTCOME ADJUSTMENT]`，不把静默省略当取消。只有显式 transition milestone 漏落时，同一 Reviser 允许一次窄 Outcome Repair retry。自动 Repair 在真实失败稿上 PASS，正文相似度约 96.75%；第二次仍漏则 fail closed，不形成循环，不让错误 State 进入长期 Canon。该机制不试图语义审计所有任意计划结果，只保护这类已经证明可达、读者必须明确知道的里程碑状态。

### 14.7 Supporting Logic Bypass / Aggressive Payoff / Public Proof 根修（2026-08-29）

20 章九垂原实验的两份审计共同暴露：旧规则“Supporting Logic 不得升格 Story Engine”没有消失，但出现了更深旁路——`Human 的责任/边界/路线型职业倾向 × World 的粮道/水源/矿权/迁徙素材 → Sol Collision 认为高度匹配 → 正式批准为长期 Story Grammar`。因此这次根修不再只打 Writer negative prompt。

当前 production 已冻结：

- **Human Occupational Trait Ceiling**：除非作者明确选择职业/制度/经营题材，责任、精确、审计、边界、路线、损失归因、职业伦理只作低权重局部习惯；钱、胜负、审美、身体欲望、享受、面子、自由、野心、报复、偏心与具体关系优先前景。**Character relevance ≠ Story Engine authorization**；主角不是多方协调员。
- **Major Reward Anchor / Big Direction First**：公共资源型 World 先锁阶段真正值得馋的少数对象/结果与价值，再让 Supporting Logic 只承担大方向选择 + 直接后果；奖励方向提前锁，兑现强度不预先克制。
- **Plot Pace ≠ Tier Pace**；若作者明确要求异常高速升级，则 **Rapid Growth Needs Protagonist-Specific Causality**，由 Core Asymmetry / Advantage Stack 解释学习、资源、实战反馈、风险收益或机会获取优势，不靠逐章送材料。
- **Mystery Before Settlement + Effective Opponent Adaptation**：奇观/古器来源/未知生物不因出现价格与归属就立刻资源化；长期 Rival 学到能力边界后至少一次反制要真的改变主角选择/局面。
- **Authority Reviser**：可以激进压缩谁守/谁撤/谁赔/谁承担/谁见证等 process carrier，但不能越权把已经冻结成公共协调题的 Chapter Mission 改成另一种故事。真实 Ch15 A/B 中 MAX 从约 4160 字压到 3165 字（约 -24%）且保持 Mission，但仍无法消除上游已冻结的井/粮道/迁徙分工，证明根修必须在 Human/Story/Outline。
- **Backstage Abstraction Translation**：真实追源确认“对普通人来说，这是离开聚落的身份入口”是旧 Authority Reviser 自己加入，Primary 原句反而更自然。新 Reviser 用同一 Ch4 Primary/Authority 复验后改为具体待遇/行动语言，不再输出“身份入口”后台标签。
- **Public Proof 三路并列**：`Collective Shock / 全场鸦雀无声或所有人震惊`、懂行者 `Ruler Calibration`、关键人物 `Behavioral Repricing` 没有高低之分。真实 Ch14 MAX 在同一 Authority 下同时形成全场止声 → 专家说明正常成炉者与四十丈改潮差距 → 阮青蜃立刻改报价，方向 PASS。系统不得因“克制/避免吹捧”自动删群众震动。
- **World Horizon Reader-Facing Edge**：若 Approved World/Canon 已有真实外缘信号，在 Handoff 前最后 1—2 章让读者看见一次“刚登顶才发现山外有天”；只复用已批准旧事实/旧未知，不提前替 protagonist-blind World Expansion 发明答案。
- continuity 三项已直接修正：阮青蜃性别、唐绾年龄/资历称谓、`镇潮军府` 正式名。

真实 A/B 保留在 `books/real-exp-fast-world-20ch-20260828-v1/system-fix-validation-v2/`。同一九垂原/Character 下，current production Story Program 已从责任协调改成 `潮路生两身 → 百炉夺槊 → 深矿猎王 → 生活/关系兑现 → 裂潮关断矿 → 两身镇海`；MAX 进一步提高夺取、越阶、复合奖励和公开震动。Human A/B 也保留 production 强降权与更激进 MAX 两档；**MAX 不自动 productionize，强度继续由作者读真实输出决定。** 当前结构专项与全量回归 **358/358 PASS**。

审计方法同步升级为 **`tgn-system-steward 0.3.8`**：保留 0.3.7 的 Small Grammar / Secondary Axis / Naming 审计，并把 Public Proof 改为三条并列通道；不再把真实群体震动默认判为低级。0.3.8 已通过 AgentDock package validate、install/activate 与 bounded Luna-high smoke；smoke 对“全场止声 + 专家尺度 + 立即改价”判 PASS，没有要求压低群体反应。

### 14.8 Precise Power Ruler 强制 Authority + Public Proof 三线共尺（2026-08-29）

用户明确要求几百章长篇不能只有“入潮→成炉→照域→镇海”这种粗档位，而应像成熟长篇一样始终知道主角**精确在几级 / 几星 / 几重 / 哪个数字序列**。这次把精确尺从软建议升级为 production Authority，不新增战力数据库或总战力分。

冻结结构：

- **World Root 必须有 `### 精确力量主尺｜Frozen Grammar`**，只允许三种简单形态：`连续数字`、`大境界+数字子级`、`数字序列`。固定写主尺名称、含 `{N}` 的精确位置格式、明确数字精度规则、当前可见数字范围与少量大档位；World 缺该结构不能批准。
- **Human T0 精确位置**：Human Seed 仍然对 Power Seed 盲，但会额外看到只读的 Frozen Precise Ruler；在生活事实第一行冻结 `开局精确力量位置｜主尺：…｜精确位置：…`。Character Approval 会校验主尺名与数字位置，不允许只写“普通人 / 未入门 / 大概低阶”。
- **Current Power Position**：`PERSISTENT CANON → Power / Capability` 第一行持续保存 `Current Power Position｜主尺：…｜精确位置：…`。只有最终正文明确突破才更新；越级胜利、承受高阶攻击、装备增强或社会重新估价都不能反推升级。后续 State 若漏写该行，runtime 确定性保留上一 Canon 位置；`CURRENT_CHARACTER.md` 单独投影当前精确位置，若尚未有 Canon 更新则回退 Human T0。
- **World Expansion 延展 Range，不重写 Grammar**：`scope=macro` 必须明确 `沿用主尺`、`主尺语法改动：NONE`、`新增可见范围`，可以把 1—60 扩到 61—100，但不能把“每境1—9星”改成初/中/后期。真正独立 `scope=instance` 必须有自己的 `### 本地精确力量主尺｜Instance Grammar`，但明确不改写全局主尺；离开 instance 后本地尺随 Local World 退出章节 Authority。
- **精确尺是 Reader Ruler，不是 Combat Formula**：技能、装备、经验、环境、克制与 Power Asymmetry 仍可造成越级；不建攻击力/防御力/总战力数据库，也不要求每章报数字。
- **与 Public Proof 三条线强连接**：主力量相关大型 Public Proof 中，Collective Shock、懂行者 `Ruler Calibration`、关键人物 `Behavioral Repricing` 共同使用同一精确坐标。群体震动承受“43级击败58级”这种差距的现场重量；懂行者直接说双方精确位置、正常差距和超标点；关键人物再因为“精确位置 + 超标表现”改变报价、待遇、敌意、战术、招揽或准入。三条线没有高低之分。越级胜利后若没有另行批准的突破，State 仍保持原精确位置。
- **Outcome Fidelity 支持数字里程碑**：现有条件 Repair 现在也识别“提升到 / 升到 / 达到 43级”等明确数字里程碑；“42级打赢58级”不能替代批准的“提升到43级”。

真实 Luna-high smoke：`books/real-exp-precise-power-ruler-20260829-v1/`。World 样本生成 `锚力阶`：连续数字 1—100、每1阶可记录，当前 Horizon 只展开1—60并给四个读者大档，61—100只作为远方上限；同一输出明确说明等级不是胜负公式。首次自动验收只因 parser 不接受 `当前大档位：` 后的自然多行列表而失败，修 parser 后**同一原输出直接 PASS**，没有放松 validator。Public Proof 样本冻结主角43级、对手58级、胜利不升级；弱 Primary 只有“有点东西 / 互相看一眼”，Treatment Reviser 最终同时恢复：数百人先止声后炸开 → 导师直称58 vs 43、正常差5级已难赢且跨一个十级大档 → 招生负责人当场废除普通招揽规格、换牌并升级正式邀请，同时明确主角仍是43级。三线联动 PASS。

专项 + 全项目回归当前 **370/370 PASS**。完整实验说明见 `books/real-exp-precise-power-ruler-20260829-v1/FINAL_REPORT.md`。这次同时把长期审计方法升级为 **`tgn-system-steward 0.3.9`**：新增 Precise Ruler authority-chain 与 Public Proof 三线共尺审计；已通过 `skill-authoring` lint（0 error / 0 warning）、package validate、install/activate，并用“43级击败58级但正文只有群体震动”的已知样本做 Luna-high bounded smoke，正确判 `PARTIAL PASS`、缺 Ruler Calibration + Behavioral Repricing，并明确 State 仍保持43级。尚未解决：还没有真实500章 E2E，因此只冻结精确尺 Authority / State / Expansion / Public Proof 接线，不声称已证明最优等级数量或最佳长期升级频率。


### 14.9 Chapter Runtime Latency Phase 0–3 Final（2026-08-29）

20章九垂原冻结运行确认：正常采用的五节点章节链平均 **6.17分钟/章**；把废弃重跑、Ch1 后 Replan、十章 Review 与终检 Repair 纳入真实批次后为 **7.73分钟/章**，开书上游一并摊销约 **8.84分钟/章**。正常链中 Curator 31.4%、Authority Reviser 37.1%，合计 **68.5%**；Primary Writer 只占 15.0%。慢的核心不是 Terra 正文，而是两个高推理辅助节点与重跑/Review/Repair 批次税。

本轮按作者要求只把 Phase 0 的确定性低风险项冻结：

1. `current_long_block` 只保留覆盖当前章的最窄显式范围；明确过期时 fail closed，不再回退整份旧长纲。后十章真实样本每章删掉 2,545 个 stale 字符。
2. 章节 raw GBrain / Reference Program fail closed；历史 20 章检索中 19 章零命中、累计只接受 1 条，章节继续通过批准上游与 source-blind Scene Skill 获得 craft。
3. Curator 固定输出合同由矛盾的“明列 9 项、后文再要求 4 项”统一为显式 13 区块并加回归测试。
4. 真实耗时账区分 adopted chain、actual batch、upstream amortization；rerun / Review / Repair / fallback 单列。
5. 每节点保存 Prompt chars、input/cache/output/thought、wall、fallback/adopted 与 Reviser diff / exact 信息。

Phase 1–3 全部完成真实模型实验，但没有冻结：

- Full Reviser Luna medium 约快 52.8%，商业读感仍由 Luna high **3/3** 获胜。
- Luna-high Patch Reviser 约快 44.3%，商业读感为 full high **5胜 / Patch 1胜 / 1平**；局部 Patch 会制造后文状态矛盾、漏 Ending 或误删有价值 realization。“安全章”路由 4 章中 3 章 fallback，前置 Patch 反成额外税。
- 完整合同 Luna-medium Curator 约快 61.2%，Authority 由 high control **5:2** 获胜；Slim Luna/Terra medium Curator 可把节点缩短约 70%，但无稳定模型赢家，并出现低潮时序、反潮记录持有与分身/回潮楔执行路径问题。将相同 Slim Envelope 恢复为 **Luna high** 后，Curator 131.0s → 65.2s（约 -50.3%），但完整 `Curator → Primary → Reviser` 只快 **11.4%**；Reader 选 control 3:2，Authority 为 control 2 / treatment 2 / mixed 1。Treatment 仍会漏结算或 Ending，且第2/14章整链反而更慢，不能视为质量等价。
- Conditional Director 首轮约快 41.1%，商业故事盲评由 full control **4胜 / 1平 / treatment 0胜**，并在 Ch20 越权。把短 Director 接回完整下游后，Director 43.3s → 26.8s（约 -38.2%），完整 `Director → Curator → Primary → Reviser` 仅从 331.3s 降到 313.9s（约 -5.3%）；Reader 为 control 3:2，Authority 为 **control 4:1**。只有 Ch19 双盲胜出，第2/13/16章双盲失败，第20章仅 Reader 偏 Treatment，仍不值得增加 production 路由复杂度。

这些实验也发现 current full route 并非永远正确：Ch19 Conditional 最终稿同时消除了“尚待结算 / 终于到手”的内部矛盾并赢得双盲；Slim 在部分章也能收回未授权设定。真正未解决的是**没有可靠自动路由知道哪一章、哪一句可以缩**，所以不能因局部胜例全局上线。

默认章节路由继续冻结：`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`。本轮作者明确排除 ACP runner 与前端，因此二者没有修改，也不是未完成项。唯一最终判定包：`books/real-exp-chapter-latency-optimization-20260829-v1/RESULTS.md`；机器可读表：同目录 `QUALITY_DECISION_TABLE.csv`；Phase 0 production commit：`7c1fc05`。

上述延迟审计方法已进入 **`tgn-system-steward 0.3.10`**：必须分开 adopted node wall、真实批次 elapsed、上游摊销与 execution/queue；高字符相似度不证明节点冗余；模型、effort、Slim/Patch/conditional contract 等语义路线变化必须接回正常下游并审最终正文。AgentDock package validate 通过并已 install/activate；Luna-high bounded read-only smoke 正确判定“全局 Curator medium”与“按相似度跳过 Reviser”均为 `FAIL`，只允许冻结 stale Long Block / raw GBrain fail-closed 等确定性根修。当前全项目回归 **373/373 PASS**。


### 14.10 Chapter Runtime Latency Innovation Round（2026-08-29）

在 Phase 0–3 之后，进一步测试了不直接全局降档的创新路线：Parallel Pre-Curator、Authority Blueprint、并行 Authority Watch + medium Reviser、Paragraph-Delta Reviser、Commercial Spark、Speculative Next Director、Ten-Chapter Attention Kernel、Reviser+State 合并、严格删除式 Reader Polish 与持久 ACP process。所有有语义影响的 Treatment 都接回正式 downstream，并同时做 Reader + Authority blind；Paragraph-Delta 另做独立 repeat 与跨书复验。

最终 production 路由仍不变。关键结论：

- `Parallel Pre-Curator` 关键路径约快21.7%，Reader Treatment 3:2，但 Authority control 4:1；Mission 前冻结注意力会产生无法完全 rebind 的偏差。
- `Authority Blueprint → Primary` 约快40.4%，Authority Treatment 4/5，Reader 仅1/5；“事实更稳、人物/爽感更薄”不是可接受交换。
- `Parallel Watch + Luna-medium Reviser` 约快38.0%，同样 Authority 4/5、Reader 1/5，不能上线。
- `Paragraph-Delta Reviser` 在同书约快51.9%，首次 Authority 4/5偏 Delta；但 repeat 只1/5最终正文完全一致，repeat blind 回到 Reader 2:2:1、Authority 2:2:1。跨书仍约快47.7%，Reader 4:1偏 Delta，Authority却是 control 2 / mixed 3。它是唯一高潜语义研究方向，但当前不 productionize。
- `Spark + Delta` 只约快13.3%，并会把商业强度越权写成稳定境界、无损胜利或额外事实。
- `Speculative Next Director` 的 State+Director 子路径约快45.4%，完整 `State→Director→Curator→Primary→Reviser` 只快12.1%，Reader 3:3、Authority control 4 / treatment 1 / mixed 1；不能默认投机。
- 去掉旧 Canon、只依赖上一章正文尾部的复验，完整关键路径快12.41%，Reader 3:3、Authority control 3 / treatment 2 / mixed 1；第6章双赢但第15章双输，第19章 Reader赢而Authority输，仍不能默认投机。
- `Ten-Chapter Attention Kernel` 摊销只快4.75%，Reader control 3:2，Authority control 2 / treatment 1 / mixed 2；稳定 Book/Human/Prose 可以预编译，但实时 attention 仍必须绑定当前 Mission/Canon。
- `Reviser+State` 同调用两章反而慢34.9%与49.6%，停止实验。
- 严格删除式 Reader Polish 可以隐藏在 State 并行窗口，第二次被改4章的 Reader 4/4、Authority 3/4偏 Polish；但两次20章触发集合只重合第16/18章，跨书10章全部 `NO_CHANGE`，不值得新增常驻 Agent。
- 持久 ACP process 在6个最小 fresh-session 调用上相对快28.35%，绝对只省1.263秒/调用；它不改语义，但前端不用该 runner，本轮未修改 ACP。
- 完整 Curator 改为 Terra high 并接回相同 Primary/Reviser 后，四章总链平均快26.92%，但 Reader 与 Authority都正好 Terra 2 / Luna 2。Terra在第2/14章更具体，却在第10/14章出现行动者漂移、共同推车替代独自稳车、未授权分身规则与残压 Ending 错误；没有稳定模型赢家，不改变默认。
- 去掉当前 Canon 的 Speculative Director 完整下游仍只快12.41%，Reader 3:3、Authority control 3 / treatment 2 / mixed 1；第4章补出第二袋钱，第15章漏水路确认和同步危机，证明实时 State 不能从当前注意力绑定中删除。
- State 改 Terra low 在8章中总体慢3.32%，0/8四字段 exact；Paragraph Manifest v1 5/5 fallback、有效路径平均慢105.93%，v2仅2/5采用且平均仍慢5.93%，停止。

新的稳定方法论：延迟语义路线必须同时报告完整 critical path、Reader + Authority、repeat、cross-book、fallback/丢弃成本；不能用单次 wall、单个 Judge 或中间节点输出生产化。下一代最有希望的是代码级 `Atomic Chapter Obligations`：actor-action-object、Direct Result / State / Ending、ownership / transfer / money / time、precise ruler、Reader Release、unresolved facts、Human-specific cue 与 protected commercial value。Paragraph-Delta 只有在这些 obligations 全部闭合且全文状态一致时才可采用，否则继续走 full Luna-high Reviser。完整报告：`books/real-exp-chapter-latency-innovation-20260829-v1/RESULTS.md`。

本轮最终验证：全项目 `388 passed`；`tgn-system-steward 0.3.11` package validate / install / activate 完成，bounded smoke 将 Paragraph-Delta 判为 `PARTIAL`，只允许冻结速度信号与研究方向，不允许冻结 production route。


### 14.11 Atomic Authority IR v1（2026-08-29）

用户对旧Atomic v0.3的关键修正被实验确认：`Atomic Authority Contract` 与 `Primary Preservation Map` 必须彻底拆开。Hard Contract只来自Entity Registry与Frozen Mission / Canon / World / Power / Human / Reader Release的可信typed artifacts；Curator/Primary只能提供realization位置与Edit Locality，不能定义Fact、Conflict或Identity。

稳定decision model：

1. Entity ID替代“Mission名字优先还是Primary名字优先”；正文名字/代词只作evidence mapping。
2. Runtime拥有fact ID、stable slot、source/mode/phase和cross-source dependency；terminal state-bearing transition必须有可验证from-state。
3. Artifact使用source-specific freezer、私有issuer与fact digest；空合同不eligible；Registry/Contract/Map不可变，Contract snapshot重载会复核provenance、membership、digest与hash。
4. Primary evidence由Runtime签发并绑定Primary SHA-256；Curator hint不能扩窗。Preservation校验同一Contract hash、paragraph topology和locked paragraph hashes。
5. Edit Locality是默认商业价值保护：blocker在P42–P43，只开放P42–P43；窗口外欲望、关系、Reward、Surprise不需要语义分类器。
6. 只有money/relationship promise/mystery/current action basis/ownership/active threat等被Authority明确标记的state-bearing history才是Hard，不登记所有旧对白。
7. Unsupported chapter直接走当前Full且不post-gate；supported Delta失败才Full fallback并supported re-gate。
8. Primary不看Atomic Pack；Normal Delta只在失败后看到具体blocker与窄locality。
9. verbose/compact/micro自由文本Sidecar全部失败；目标改为单一canonical `DirectorStructuredDecision`，Runtime双投影human Mission与Frozen Mission artifact，不保留第二份自由human clause。

证据：57项focused tests；两书四章4/4 source-pure/preflight eligible，平均editable 3.11%，窗口外4/4阻止；22/22 Schema/runtime checks；Sidecar wall分别+205.83%/+147.41%/+146.45%，compact blind Story 3:1偏Control、Authority 3:1偏Treatment。Native structured Director仅schema/unit-ready，真实模型Story/latency/最终正文未测；Full Reviser固定税尚未减少。最终分类：Architecture/static implementation PASS；free-text Sidecar FAIL；native model route与Atomic fast route NOT PRODUCTION。完整报告：`books/real-exp-atomic-authority-ir-20260829-v1/RESULTS.md`。

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

自动调用当前激活 `tgn-system-steward` 独立审计，同时自己复核，最后给统一结论。当前激活版本为 **0.3.8**；除 Social Calibration、`Public/Known World = Clarity`、Plan Compression 与 Authority 边界外，还长期审计 **Small Grammar ≠ Small World**、Secondary Fantasy Axis 是否被反工程化误删、Naming 是否出现“词先于机制 / 名字反向授权机制”、以及 lexique 是否只有真实 semantic/gameplay gain 才被采用。Steward 不进入 production，也不替 Story/Director 创造招揽、嫉妒、暗杀或长期 Ripple。

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
30. 覆盖当前 dirty worktree 或混提交无关文件；
31. 为了正文“完整”替尚未揭晓的旧历史、旧对话、隐藏动机或世界机制补造 retrospective canon。
32. 因反“群众震惊”而过度克制，把高价值 reveal 压成一个停顿/站起，却不给读者正常值、超标点和稀有意义的专业 ruler 校准。
33. 把力量尺校准当成 opening 一次性说明；新层级、新复合、新圈层或旧估值过时时不再重新提醒读者主角现在到底特殊到哪里。
34. 因“反百科”让公共常识只藏在火盆、服装、建筑、术语或氛围里，逼读者自己推理世界怎么运行。
35. 把 Long Block 已经明确的具名机会价值在 Future 10 / Director 中压成“公开机会 / 一个资格”，让读者不知道眼前机会为什么值得争。
36. Frozen Power 只批准“重新接触 / 合并”时，为了场景方便自行发明远程召回、跨距离影子回收或无需重新碰面的合并。
37. 把 Small Grammar 误读成 Small World，为了少规则把原本鲜明的兽印、装备、身体、异兽、环境与副轴一起压平。
38. 因过去反工程化就把炼药/炼器/作品竞争等真正具备强者尺度、作品胜负和社会价格的 Secondary Fantasy Axis 一律压成背景；或反过来强迫每个主角都走副轴。
39. 把 lexique 当完成设定/命名答案，强迫每个 Candidate 使用 primitive；或为了一个“好听名字”反向补机制、边界与第二系统。
40. 把 Naming Craft 变成固定四字格式、统一后缀、词族配额；名字的第一职责仍是避免读者误解已批准语义。
41. 要求开书 World Vision 预先具体设计足够支撑 500 章的所有大陆、文明、终局力量和未来异世界；长篇世界允许 forward expansion。
42. 让一个 Agent 同时看到 Current Character 并创造下一 World，再让它顺手安排下一奖励/人物发展；这会把 Surprise 自洽成主角钥匙孔。
43. 把 World Expansion 当 World Rewrite，重新生成/重抽 Power Seed、Human Seed 或 Character Origin；Forward Expansion 不回写过去。
44. 每次扩世界、每个副本都强制跑出 Human Development；稳定人格没有真实长期变化时必须允许 `NONE`。
45. 把 Story Program 的 `World Horizon Handoff` 当成下一世界设计说明书喂给 World Agent；Handoff 只管什么时候扩与 carry-forward，不能告诉独立 World 应怎样适配主角。
46. Outline / Review 为了凑足十章/百章越过未执行 Handoff，自行发明下一大陆、下一副本、公共规则或未来 Power。
47. 新 World Expansion 全文直接进入 Writer；章节 `WORLD AUTHORITY` 只允许 safe public facts，隐藏人物行动与未知边界仍需 Reader Release。
48. Canon 已更新却继续用 stale `CURRENT_CHARACTER.md` / stale Story Program 做 refreshed Outline；“曾批准”不等于“仍 fresh”。

---

49. 因 Split Authority 已经正确，就误以为设定搜索空间也自动足够；分权能防泄漏，但不替代 Authority 冻结前的大胆 Premise 搜索。
50. 看到多个 fresh-context Agent 各自产出新奇组件，就把“独立性”当作整体创意质量；四个高电压好点子可能只会争夺第一章注意力。
51. 把非 Canon Premise Card 直接升级成第四 Authority、自动 selector 或所有 lane 的共同输入；候选应先经独立 Premise Compiler 只审可满足性，再由作者选择，并按现有 Authority 确定性拆为 `World + protagonist-blind Interface`、`Ontology + Initial Scale Position + exact Power trigger/target/action/carrier/boundary`、`Ontology + T0 Origin + Initial Scale Position` 与后置 Story Promise。这些字段是 binding contract，不是柔性 direction。
52. 用换名词、换能源、换职业证明创新，却没有改变主角反复会做的基本动词；大胆度优先看身体、战斗、移动、生存、占有、变形和社会关系动作是否真实不同。
53. Primary 把“事实 / 动作已经成立 → 另起漂亮短句裁断或否定翻转 → 再升华意义”反复写成整章稳定节拍。单独一次可以是好句；问题是 LLM 把它复现成章法。当前 Primary Prompt 已加窄硬禁令：本章自然出现一处明显的这种收束后，后文不再主动制造第二处同构；按语义结构判断，不做禁词扫描，也不新增 Reviewer / style score。
54. 把 Forge 自己写的 `Authority-Compilation Trace` 当作客观证明；单个 Agent 会把“棚屋开始缩小”误写成“棚屋已完整穿门”，也会为不存在的出口、共同载体或等级跃迁补出合理感。必须由独立 Compiler 重查具体 trigger、目标、载体与尺度。
55. 把 Premise Compiler 做成评分器、自动修稿器或保守 selector；它只判断约束能否同时成立，不能因为设定激进、主角占便宜大或风险高就否决，也不能替作者选择 S1 / S2 / S3。
56. Compiler FAIL 后自动进入 LLM repair loop；一次预注册 V5 定点修复即使 Prompt 明令保护，仍漏掉整个 `主角反复会做的新动作` 字段并扩大成机制重构。正式边界应先把精确冲突交给作者；任何 repair 研究都必须代码锁定标题、货架句、Ontology、Changed Verbs 与不可磨平项，并在独立 Compiler 前 fail closed。

---

## 16A. Premise Aperture 已冻结为可选 Production 开书阶段（2026-08-30）

用户用四本 2026-08-29 新书扫榜素材指出：它们的共同优势不是设定百科更复杂，而是很早押注一个会立刻改变主角形态、玩法或社会位置的高风险核心幻想。受控实验确认最早坍缩发生在任何 Authority 生成之前：Split Authority 能防泄漏，却不会自动搜索完整货架前提。

有效 casewise evidence：Single-Agent 完整 Premise pool **85.1**，current baseline **75.8**，四轴正交 collision pool **71.7**；预注册 S2 比 C2 三案平均高 **16.3**。关键判断是：**fresh-context isolation 是 authority leakage control，不是 creative composition optimizer。** 完整 premise 一次形成负责主承诺，后续 lane isolation 负责防止后验合理化。

F1—F5 已由作者明确冻结，当前 production 链为：

```text
作者方向
  →（可选）Single-Agent Premise Forge：S1 / S2 / S3
  → Independent Premise Authority Compiler
  → 作者选择并批准 / 手动处理冲突 / 显式跳过
  → deterministic lane-specific frozen contracts
       World：World-only + protagonist-blind public Interface
       Power：literal Ontology + Initial Scale Position
              + trigger / target coverage / action / carrier / root boundary
       Human：literal Ontology + exact T0 Origin + Initial Scale Position
       Story：Authorities 批准后第一次读取完整 Promise / Interface
  → 现有 Split Authority 链
  → Outline / chapter 不读取 raw Premise Card
```

运行语义：

- Premise 从未开始或作者显式跳过时，原 Split Authority 路径保持可用；
- 一旦保存 S1/S2/S3，World / Power / Human / Story 的生成、保存与批准必须等待 strict `PASS` + 作者批准，不能静默绕过；
- Compiler 只审 trigger、载体、出口、见证者、T0 尺位、Interface 因果与远期复合，不评分、不排名、不选择、不修稿；
- batch / selected Compiler Prompt 生成当下就落盘 exact Input snapshot，报告保存不改写它；作者在模型返回前继续编辑卡片时，即使旧报告 PASS，也必须因 snapshot 不一致做 selected-card recompile；
- 批准后代码生成 `PREMISE_CONTRACT.md` 与四份 lane contract；Workflow 只登记 `premise.contract`，候选/选择/Compiler Report 不成为 Authority 节点；
- Story Program 第一次、也是最后一次读取完整 Story contract；之后只携带已经由 Authority 实现的事实；
- World Vision 一旦作者批准，Premise 决定冻结；
- `CONDITIONAL PASS / FAIL` 返回作者，不自动选择、不自动 Repair。

作者工作区已提供 Forge、三卡保存、batch Compiler、S1/S2/S3 作者选择、编辑、selected-card Compiler、Report 保存、批准与显式跳过；没有自动 selector 或 Repair 按钮。当前模型路由：Forge Luna high / GBrain OFF；Compiler Terra high / GBrain OFF。

真实失败边界仍保留：direction-only projection 会静默改写 Ontology、Power coverage 与 Interface；Forge 自带 Trace 会相信自己的假桥梁；一次预注册 Selected Premise Repair 又漏掉整个受保护 Changed Verbs 字段。因此 frozen contract + independent Compiler 成为正式边界，自动 repair loop 仍 `FAIL / RESEARCH_ONLY`。

明确拒绝：四轴完整高电压碰撞、Two-Bet 进入 production、Judge/模型自动 selector、旧统一 Fantasy Seed、章节期 Premise Reviewer/Scorer/Repair Agent。

当前真源：`docs/PREMISE_APERTURE.md`、`src/story_mvp/premise_aperture.py`、`src/story_mvp/premise_workflow.py`、`tests/test_premise_production.py`。研究证据保留在 `books/real-exp-premise-aperture-20260829-v1/`。

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
12. 高价值 Asymmetry Reveal 的群体震动、`Ruler Calibration`、`Behavioral Repricing` 是三条并列爽点；大型 Public Proof 可以一起吃满，只有持续改变后续行动的重新估价才升级 Ripple。
13. High-Value Acquisition 可选；一旦发生必须有后续生命。
14. Supporting Logic 只支撑因果，不自动成为故事发动机。
15. 高价值 Orientation 可以直接说；低价值重复解释和实施必须压缩。
16. Shock = 意外 + 回看成立 + 重大状态变化，不等于隐藏身世。
17. Outline 只编译，Director/Writer 不临时发明长期权威。
18. GBrain 是小型可选 craft inspiration，不是 Canon。
19. 先找最早语义坍缩点；少深规则胜过多 Gate。
20. 实验冻结上游、单变量、无 cherry-pick；人格因果使用 Character Authority Invariance + Matched Decision Point。
21. 未揭晓的长期历史保持 unknown boundary；Writer 不为完整感补 retrospective canon。
22. 节奏服从信息价值，不服从统一章长：低价值更短，高价值可以更长。
23. 对的就冻结；证据不足就保留 OPEN，不为完成感硬改 production。
24. Small Grammar 不等于 Small World：底层规则少而稳，上层招式、身体、兵器、异兽、环境、奇物、副轴与复合可以持续丰富。
25. World 可以主动寻找少量成熟 Secondary Fantasy Axis；Story 主动检查，Human 决定主角是否投入，不强塞副职也不被动删掉好副轴。
26. Lexique 可以提供可丢弃 semantic primitive 和后置 naming fragrance；语义先于命名，World 已有词根优先，名字不能反向授权机制。
27. Stable Origins, Evolving Authorities：World Root / Power Origin / Human Origin 稳定；World、Power、Human 的后续变化只向前追加，不回写历史。
28. Story Program 只具体规划当前 World Horizon；靠近边界时留下 Handoff，独立 World Expansion 后才用 Current Character 做 fresh Re-Collision。
29. Power 是 Frozen Origin + Current Portfolio；Human 是 Frozen Origin + Current State + 可选 Human Development；Current Character 纯确定性编译。
30. 新世界必须 protagonist-blind 到 retrieval 层；惊喜留到 `Effective World × Current Character` 的 Story Refresh 才发生。
31. 多世界 `instance` Local World 可以高频进入/退场，Human Development 是更慢时钟；不要把不同长期时钟机械绑定。
32. 当前下一自然研究方向：`Choice → Route-specific Opportunity → Different Advantage Tree`、Visible Desire Horizon / Dominant Commercial Engine、Reward Lifecycle / Fantasy Heartbeat，以及“真实人物长期改变”Case 的 Human Development A/B；继续冻结上游、近单变量、Human Invariance 与 AGGRESSIVE/保守作者选择协议。
33. Authority Separation 保护真实独立性，Premise Aperture 扩大冻结前搜索，Premise Compiler 只验证大胆候选能否被这些 Authority 精确实现；三者职责不同。大胆度看一个完整货架承诺与 Changed Verbs，不看 Agent 数量、术语数量或机制表长度；可编译性也不能替作者决定商业强度。
34. Premise Aperture 可跳过但不能半启动：未开始/显式跳过走原链；保存候选后必须 strict PASS + exact input snapshot + 作者批准，或清空并跳过。没有自动 selector、Repair Loop 或章节期 Premise Agent。

---

## Cognitive Integrity Check

阅读本文后，一个新 Agent 不应只知道“项目采用了哪些 Prompt”，还应能够面对新案例作出以下判断：

- 一个关系型主角放弃力量试炼并不违背男频，只要长期 Growth Floor 仍成立；
- 一个力量型主角选择留下也不表示人物薄弱，关键在选择是否来自 Human；
- 一个炼药系统可以是强幻想轴，也可以只是工作流，区别在于它本身是否值得追到顶；
- 一段直接世界说明可以是高价值 Orientation，而五次专家确认仍然是水；
- 一个教头站起来并不自动等于爽点已经完成：如果没人告诉读者“普通一阶/三阶本来能做到什么、主角这次到底越出了哪里”，就是 `Reaction present / Ruler missing`；反过来只有“百年难遇”的解释而没人改变动作，也是失败；
- 第一章已经解释过金手指很稀有，不代表几十章后的新层级、新复合或更高圈层可以永远不再重新校准；
- 一个世界很适合主角发挥并不自动失去独立性；
- 一个能力简单不应被自动削弱；
- 一项结构机制即使让故事更整齐，只要覆盖人物选择就应失败；
- 四个 Story Program 看起来不同，如果触发事件也不同，就不能纯证明人格因果；
- 人格改变路线已经成立，不等于人格化优势树已经完成；
- 新实验若只解决一个子问题，应明确 PARTIAL，而不是宣布上游完全收敛。

只要下一位 Agent能稳定作出这些区分，本文迁移的就不只是 conclusions，而是当前对话长期形成的 decision model。
