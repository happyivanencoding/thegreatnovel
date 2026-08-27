# Story MVP Novel Prose Realization

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只定义章节正文的表达与实现边界。

## 定位

Novel Prose Realization 是 Story MVP 的章节表达合同。

它回答：

> 已经决定的本章事件，怎样写成自然、具体、连续、可读的中文商业长篇小说正文？

它不回答“下一章发生什么”，不负责创意、总纲、十章规划、成长循环选择或故事事实审批。

本层吸收 Humanizer-zh 中可迁移的表达原则，并以《第一序列》《将夜》《诡秘之主》的全书级 prose distillation 进行修订。它不复制三书原文，不模仿作者声音，不把某一本书的风格设为产品默认。

---

## 1. 当前 MVP 的最小边界

当前 cleanroom MVP 不建立：

- Canon 数据库；
- Chapter Contract 数据模型；
- RevisionUnit；
- ChapterRealizationBrief；
- Prose DNA 数据库；
- 风格向量；
- Humanizer Agent；
- 独立 `/api/humanize`；
- 自动评分器；
- AI 检测器。

当前真实输入已经足够：

- 已保存的前文正文；
- BOOK 当前状态；
- 当前大型剧情块；
- 当前十章计划；
- 当前章具体小纲；
- BOOK 的叙事、文风、对话和节奏区块；
- 作者手动输入的表达意图（未来可选）。

因此本层首先是：

1. 一份可维护的设计文档；
2. 一个 Agent Skill；
3. 注入章节 Prompt 的短执行投影；
4. Director / Curator / Primary Writer / optional repair 的清晰职责；
5. 与正文分离的审阅结果。

---

## 2. Authority

### 2.1 已发生事实

以下内容不得被 prose 修改：

`Saved Previous Chapters + BOOK Current Status`

包括：

- 人物所在地点；
- 时间；
- 已知与未知信息；
- 伤势；
- 资源；
- 已拥有物品；
- 能力历史；
- 关系状态；
- 已经发生的选择；
- 已经兑现或失败的承诺。

### 2.2 本章必须完成

本章事件由以下内容决定：

`Current Chapter Outline`

并受：

`Current Long Block + Current Ten-Chapter Plan + BOOK Design`

约束。

当前章小纲决定本章的主要事件、直接结果、状态变化、叙事功能和结尾推动，但不能覆盖前文已经发生的事实。如果冲突存在，应报告冲突，不得靠 prose 偷改前文。

### 2.3 表达方式

表达优先级是：

`Current Book Prose Profile`

→ `Author Explicit Prose Intent`

→ `Scene-Appropriate Abstract Prose Controls`

→ `Generic Prose Realization Guidance`

→ `Generic LLM Prior`

表达控制永远不能覆盖故事事实。

---

## 3. Current Book Prose Profile

当前 MVP 不另建 `prose-dna/`。

BOOK 中以下四个区块共同组成当前书的 prose profile：

- `## 7. 叙事结构`
- `## 8. 文风与可操作参数`
- `## 9. 对话特点`
- `## 10. 节奏结构`

它们应回答：

### §7 叙事结构

- 主要 POV；
- 叙述距离；
- 何时允许拉远；
- 何时切换他人视角；
- 切换为了展示什么；
- 世界信息如何进入。

### §8 文风与可操作参数

- 日常、高压、说明、情绪和 aftermath 的句段差异；
- 描写密度；
- 内心活动方式；
- 感官细节选择；
- 动作和规则说明如何结合；
- 本书最容易出现的机械表达。

### §9 对话特点

- 核心角色的词汇、句长、礼貌程度、攻击性、沉默方式；
- 对话承担的交易、试探、关系和行动功能；
- 不能退化成什么。

### §10 节奏结构

- 单场景如何起、转、落；
- 普通章节和高压章节如何换气；
- payoff 后是否需要 aftermath；
- 哪些过程展开，哪些过程压缩；
- 章节结尾通常承担什么状态变化。

这些是软表达控制，不是逐句 Hard Gate。

---

## 4. Cross-Book Prose Controls

三部样本共同支持以下规则：

1. 场景要尽快明确人物、空间、问题和下一步；
2. 说明必须绑定当前决策；**高价值世界定向不是水文**：首次重要势力 / 地点 / 身份 / 资源真正影响选择时，可用短直接旁白回答到足够后回到动作；
3. 具体动作和物件优先于抽象总结；
4. 叙述距离可以变化，但不能无目的漂移；
5. 句段节奏服从场景压力；
6. 对话必须改变信息、关系或行动；
7. 内心活动必须产生下一步；
8. 动作要形成“观察—行动—反应—空间变化—结果”；
9. payoff 不做三重说明；决定已经完成后的普通实施也默认压缩，除非实施中重新出现选择、冲突或失败风险；
10. 情绪允许延迟、不完整和嘴硬；
11. 章末必须留下新状态或新理解；
12. Humanizer 审查结构，不建立禁词和禁标点表。

这些规则已经被吸收为当前 prose contract；具体作品参考不再作为 Runtime 文档依赖，参考作品知识统一由 GBrain 独立维护。

---

## 5. Abstract Prose Profiles

运行时不能要求模仿具体作者，只能选择抽象 profile。

### 5.1 Practical-Comic

适合生存、资源、市场、快节奏行动和关系互损。

重点：

- 现实需求过滤世界；
- 对话直接；
- 结果尽快可见；
- 幽默来自人物与环境落差。

### 5.2 Lyrical-Subtext

适合关系余波、历史感、大场景蓄势和重要收束。

重点：

- 少数意象锚点；
- 允许叙述距离拉远；
- 沉默和未说完的话；
- 关键落点简洁。

### 5.3 Analytic-Mystery

适合调查、规则、仪式、专业现场和战术。

重点：

- POV 控制观察顺序；
- 保留备选假设；
- 推理后必须验证或行动；
- 精确细节服务可验证世界。

这些 profile 可以组合。选择由当前 BOOK 和场景决定，不作为固定 genre 映射。

---

## 6. Pipeline Position

当前默认章节链：

`BOOK / Plan / Saved Chapters → Director → Context Curator → Primary Writer → State Extraction → Author Approval → chapter-NNNN.md`

`curator_primary` 默认不运行 Specialist / Integrator。只有作者明确启动局部 repair 时，才在 Primary Draft 之后临时加入少量 Specialist Patch，并在确有有效 Patch 时调用 Integrator；没有有效 Patch 就保留 Primary 原文。旧兼容 Prompt 不构成新的 production 写作层。

---

## 7. Runtime Responsibilities

### Director — Event Contract

只决定本章发生什么：八字段事件合同、直接结果、状态变化和结尾推动。它可以使用精确的抽象策划语言；八字段合同是事实约束，不是正文句式来源。

### Context Curator — Context Projection

从 `WORLD AUTHORITY`、deterministic `CHARACTER.md` 中**只截取的 Frozen Human Core**、BOOK、Canon、当前计划、Prose Profile、可选 Inspiration 与前文章末中选择 Writer 真正需要的信息；Power Core 不在章节期重复注入，可变状态仍由 BOOK/State 提供。`WORLD AUTHORITY` 是 Approved World Vision 的安全事实投影；Outline 的 `Reader Release Map` 为当前章排程哪条世界事实，Curator 就保留/压缩哪条，不自行改选说明主题。冻结 Human Core 高于最近几章行为归纳；场景自然触发已批准的身体吸引、审美、虚荣、钱、享受、好奇、偏心等私人牵引时，保留一个可直接进入 POV 的具体触发，不因连续负责/克制而把人物收束成新的道德人格。它输出 `Reader-Facing Language`，但不重规划、不新增事实、不自行写正文。

### Primary Writer — Reader Experience

以 Primary Draft 为正式正文底稿，按当前 POV 让事件先发生、人物感知和反应跟上，再补当前决定所需的最少解释。若 Curator 已投影当前 Plan 排程的 World fact，**该 Reader Release 必须在本章兑现**：用 1—3 个短直接旁白段或等价场景表达回答后立刻回现场；若同一事实还说明地点/势力/传承为什么值得争，保留一个最短价值锚点。Writer 不从完整 World 自选说明主题，也不要求把世界说明伪装成对白。Curated Context 已明确带入私人欲望且当前场景自然触发时，让一次注意力、身体反应、靠近/回避、想要或短期选择保留它，不统一净化成职责协作与成熟沟通。决定完成后的普通实施默认一句或短段概括。 非核心 Supporting Skill 即使承担一个关键动作，也写到“做了什么 / 为什么有效 / 结果”就停；Reader Release 已给 named 对象公开类别时，首次识别可直接说清一次。关键事件的人物反应应改变动作、注意力、语气或选择，但不按模板补情绪；Planning 的抽象标签不直接变成旁白总结。

**Story-bearing Texture > Decorative Density**：正文不以“多写”或“多修饰”制造丰富感。每个主要 beat 选择少量真正改变画面的具体动作、物件/空间、身体反馈、力量后果和人物差异化反应；感官细节选择最有辨识度的少数锚点，不机械覆盖五感。细节如果不承载人物、冲突、因果或幻想体验，就继续压缩。

该原则已通过 2026-08-24 五场景冻结 A/B：两个独立盲评合计 **Texture 9 胜 / Baseline 1 胜**，正式冻结为 `Story-bearing Texture v1`。冻结含义是：保持“故事承载细节而非装饰密度”的核心实现，不再以一般性“多描写”替代它。战斗 / Action 场景仍需特别压缩力路、受力、步骤和机制拆解；未来如优化，只做窄范围 Action/Combat refinement，不回退本原则。

**长期历史未知边界**：Curated Context、Canon 或 Open Promise 已明确为未知、未解释、真假未定、原因未明的过去事实，不因进入正文就自动成为可补写的背景。除非 Director Contract 明确规定本章哪一个新事实成为确定事实，Primary 只能创造当前场景的动作、对白措辞、即时证据、感官和人物暂时判断；不得为了让场景显得完整，把几十 / 几百章前的秘密经历、旧对话、隐藏动机、既有知识或世界机制补成 retrospective canon。

该边界已经通过 Chapter 120 / 600 压力 A/B 验证并冻结为 `Long-History Fact Boundary v1`。最终版本除 Prompt 顶层事实规则外，还把 Curator 已识别的 Open Promises / 未解机制 / 未兑现事项确定性投影为约 300 多字的 `UNRESOLVED FACT BOUNDARY`，放在 Chapter Mission 之后、正文连续性之前；不增加模型调用。冻结样本中两章的核心 unknown discipline 均达到盲评 5/5。已知残余是极少数后台章节编号可能被 Writer 自我纠正式带入正文，这属于 prose hygiene，不改变 Canon，也不应通过新增 continuity agent 解决。

### Specialist / Integrator — Bounded Repair

Specialist 只看职责相关的 Primary Draft 局部和 Curated Context，最多给局部 Patch；Integrator 只以 Primary Draft 为底稿，并且只在真实存在下列问题时有限修复：

- Planning summary 替代了场景结果；
- 重大事件没有人物反应；
- 结果前堆积了机制说明；
- payoff 被重复解释；
- 对话、动作或 POV 声音被抽象总结覆盖。

如果 Primary Draft 已经自然，Integrator 保持原文；任何修复都不得改变主要事件、直接结果、人物决定、资源/能力状态或章节结尾推动。

---

## Diction Controls

Diction Controls 属于 prose soft controls，用来帮助 Writer 在当前 POV 和场景中选择更准确的词。它们不形成 schema、validator、Hard Gate 或 style score，也不建立 prose runtime subsystem。最终仍服从当前 BOOK §7—§10、人物身份、关系和场景压力。

### 名词

优先使用当前 POV 人物能够看见、触摸、使用、搬动、失去、交换或绕开的具体名词。抽象概念可以使用，但如果能通过物件、身体状态、空间、制度后果或人物选择落地，就优先落地；不要为了“具体”机械增加无功能细节。

### 动词

优先写清方向、接触对象和实际结果：从哪里，朝哪里，接触什么，什么发生改变，下一步怎样受限或打开。进行、产生、形成、实现等词不是禁词，只有在它们替代了本可写清的实际动作时才修复。

### 修饰词与不确定词

修饰词优先保留真正改变当前 POV 判断的性质，不堆多个近义词。似乎、仿佛、可能、大概、应该、显然、突然、竟然都不是禁词；它们只在 POV 确实无法确认、判断暂定、后续信息可能修正或变化超出预期时使用。

### 语体与重复

语体服从人物身份、关系、当前压力和当前场景，不全局口语化、书面化或古雅化。专业词第一次进入故事时，应改变选择、风险、行动、理解、机会或关系中的一项。

Humanizer 区分有功能的压力累积、仪式、关系回声、情绪回响和 payoff 回扣，与无功能的相同修辞模板、相同句首、相同“不是 X 而是 Y”、相同情绪解释和相同能力说明；只主动修第二种。

## Sentence Architecture

Sentence Architecture 是 Primary Writer 根据场景选择的句法关系，不是固定模板，也不要求每段套用。

- 基础行动：`锚点 → 动作 → 反应 → 条件改变`；
- POV 推断：`观察 → 暂定解释 → 新细节 → 修正判断 → 行动`；
- 物象反思：`具体物象 → 关系 / 记忆 → 判断 → 简短落点`；
- 对话：`一句话 → 微动作 / 停顿 → 对方行动 / 拒绝 / 改变`；
- 说明：`当前需要 → 最少必要事实 → 选择 / 风险变化 → 回到动作`；
- 情绪：`动作 / 物件 → 未完全说出的感受 → 选择 / 沉默`；
- payoff：`执行 → 可见结果 → 外界反应 → 一次确认 → 新行动空间 / 新压力`。

推理必须影响行动，对话结果必须进入现场，payoff 不做“提前宣布—实际发生—再总结”的三重说明。长句适合空间、关系、因果、观察和犹豫；中句承担推进；短句用于决断、转折、危险、笑点和余波。高压场景可以收紧句段，普通、关系、exposition 和 aftermath 可以拉长；多写短句不是目标，也不要让整章保持同一种句段长度。

这些控制不形成句长阈值、禁词扫描或独立运行时系统。

---

## 8. Scene Realization

优先展开：

- 第一次出现的重要规则；
- 会改变决定或关系的动作；
- payoff；
- 冲突真正变化的节点；
- 后续会复用的信息；
- 空间参与冲突的行为；
- 不展开就会造成连续性断裂的桥接。

可以压缩：

- 没有新信息的普通路程；
- 已明确的相同疼痛；
- 相同担忧的重复；
- 没有新博弈的讨价还价；
- 已经理解的规则复述；
- 不改变任何状态的过场。

桥接可以短，但不能不存在。

---

## 9. Humanizer-zh 的采用边界

### 采用

- 删除填充；
- 删除同义复述；
- 避免机械三段式；
- 避免全章均匀节奏；
- 用具体动作和物件替代空泛判断；
- 让角色声音和关系距离不同；
- 信任读者；
- 保留不规则、停顿和未完成信息。

### 不采用

- AI 检测目标；
- AI 分数；
- 禁词表；
- 禁标点表；
- 全局短句化；
- 全局口语化；
- 全局禁止说明；
- 全局禁止作者旁白；
- 为“人味”故意制造错字、俚语或逻辑缺口；
- 把 Wikipedia、文章或营销文本规则直接套进小说。

---

## 10. Prose Audit

审阅只回答表达问题，不重新规划故事。

检查：

- 本章是否真的发生，还是只概述；
- 重要动作、反应和后果是否展开；
- 信息是否在人物需要之前过早解释；
- POV 是否看到不该知道的东西；
- 对话是否只复述已知信息；
- 角色声音是否可区分；
- 全章是否只有一种句段节奏；
- 是否连续解释同一结果或情绪；
- payoff 是否被提前宣布并事后再总结；
- aftermath 是否产生新意义；
- 结尾是否留下真实状态；
- 是否完整保留小纲和前文事实；
- 是否出现来源风格泄漏。

审阅不输出总分，不因某个词、标点或句式一次出现就判失败。

---

## 11. Bounded Repair

Repair 只修表达层：

- scene realization 太薄；
- 连续性桥接的 prose 缺口；
- 冗余解释；
- 泛化；
- 节奏单一；
- 对话僵硬；
- 无功能总结；
- payoff 重复说明。

Repair 不得：

- 发明关键事件；
- 改变事件顺序；
- 改人物意图；
- 增删关键成本；
- 改资源和能力；
- 改线索；
- 改不可逆结果；
- 改章节结尾状态。

如果需要改故事才能解决问题，停止 repair，报告规划冲突。

---

## 12. Reference Boundary

三部经典作品只提供：

- 观察维度；
- 抽象 profile；
- soft controls；
- 失败模式。

不得进入章节 Prompt 的内容包括：

- 原文；
- 长摘录；
- 来源人物；
- 来源专名；
- 作者姓名模仿指令；
- 签名比喻；
- 固定口癖；
- 单书完整 DNA；
- “照着某书写”的 exemplar。

GBrain Story Reference Programs 继续负责故事设计，不自动变成 prose reference。

未来若增加独立 Prose Controls，也只能传入少量、抽象、当前场景相关的控制。

---

## 13. Output Boundary

最终 `chapter-NNNN.md` 只保存正式小说正文：默认来自 Primary Writer；显式 repair 时若 Integrator 产生有效最终稿，则保存该最终正文。

以下内容必须与正文分离：Audit、事实摘要、repair notes、字符/token 统计、运行 metadata 与 provenance。

调用方已有正文/审计分区合同时，继续遵守现有合同，不另建第二套格式。本层不自动写 BOOK，不自动批准章节，也不自动覆盖已有章节。
