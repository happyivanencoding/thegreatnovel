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
4. Director / Curator / Primary Writer / Authority Reviser / optional repair 的清晰职责；
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

`BOOK / Plan / Saved Chapters → Director → Context Curator → Primary Writer → Authority Reviser → State Extraction → Author Approval → chapter-NNNN.md`

`curator_primary` 默认固定运行 Authority Reviser，但不运行 Specialist / Integrator。只有作者明确启动局部 repair 时，才在 Authority Revision 之后临时加入少量 Specialist Patch，并在确有有效 Patch 时调用 Integrator；没有有效 Patch 就保留 Authority Revision。旧兼容 Prompt 不构成新的 production 写作层。

---

## 7. Runtime Responsibilities

### Director — Event Contract

只决定本章发生什么：八字段事件合同、直接结果、状态变化和结尾推动。Future 10 当前条目在进入 Director 前先被确定性拆成 `本章唯一可执行事件预算` 与 `章末 Handoff Reservation`；Long Block 只作阶段背景，不能把下一章付款、正式身份、获得、升级或其它结算提前搬进本章。上一章正式正文如果停在即时未解的拦截、追杀、攻击、坠落/被困、关闭中的门或必须当场回答的交易/选择，该场面自动成为下一章 continuity debt：Director 先用最低充分动作接续/转化它，才进入本章 Plan；桥接至少写出一个可直接落正文的具体动作因果，不能只写“趁乱脱身 / 成功进入 / 摆脱追兵”；不能把章节边界当成“冲突已经自动解决”。Outline / Review 同样不得规划出这种无桥接跳转。当前条目的 `结果 / 状态变化` 还会确定性并入后续 Frozen Mission 的 `状态变化`，所以 Director 静默漏写不构成取消；若已发生 Canon 真使原结果不可能，必须在 `状态变化` 中写 `[PLAN OUTCOME ADJUSTMENT]` + 最小原因/替代结果，不能因节奏或方便使用该标记。它可以使用精确的抽象策划语言；八字段合同是事实约束，不是正文句式来源。若单章计划提到试场/选拔/招募/契约，却把同一剧情块已批准的具名机会价值压掉，runtime 会确定性投影一条匹配的 `当前具名机会权威`；Director 保留具体机会名与“成功参与通常打开什么”，不新增回报、不提前写主角成功。

### Context Curator — Context Projection

从 `WORLD AUTHORITY`、deterministic `CHARACTER.md` 中**只截取的 Frozen Human Core**、BOOK、Canon、当前计划、Prose Profile、可选 Inspiration 与前文章末中选择 Writer 真正需要的信息；Power Core 不在章节期重复注入，可变状态仍由 BOOK/State 提供。Scene Skill v2 只向 Curator 暴露 `skill_id + Primary Reading Question + 一行 Projection Guidance`；Curator 选择 1 个 Primary、最多 1 个 Secondary，并只在当前场景确有 realization 缺口时把 Deep Craft 编译成 2—4 句 `Scene Prose Projection`，已经清楚则写 `NONE`。完整 Skill、原著 evidence、书名/locator 不进入 Writer。`WORLD AUTHORITY` 是 Approved World Vision 的安全事实投影；Outline 的 `Reader Release Map` 为当前章排程哪条世界事实，Curator 就保留/压缩哪条，不自行改选说明主题。开篇 `公共常识` Release 必须保留成可以直接陈述的事实句义，不压成单个道具、环境意象或“有这个感觉”的模糊提示。冻结 Human Core 高于最近几章行为归纳；场景自然触发已批准的身体吸引、审美、虚荣、钱、享受、好奇、偏心等私人牵引时，保留一个可直接进入 POV 的具体触发，不因连续负责/克制而把人物收束成新的道德人格。若本章已批准为高价值 Asymmetry Reveal，Curator 的短 Projection 应优先同时保留两个 reader-facing 任务：`Behavioral Repricing`（一个关键观察者真的换动作）与 `Ruler Calibration`（最有资格者短促说明正常值、超标点与稀有/异常意义）；不把它们压成只有“有人震惊”或只有设定旁白。当前新 `observer-specific repricing` 卡仍是 PILOT，不因此新增 Scene Primary 或强制每章调用。它输出 `Reader-Facing Language`，但不重规划、不新增事实、不自行写正文。

### Primary Writer — Reader Experience

以 Primary Draft 为正式正文底稿，按当前 POV 让事件先发生、人物感知和反应跟上，再补当前决定所需的最少解释。Future 10 已批准的 `结果 / 状态变化` 已确定性并入 Frozen Mission；其中力量/身份跨档、持有关系或其它显式里程碑必须明确成为正文事实，不能只用“打出该级战绩 / 接近 / 获得资格”暗示。Primary **不再直接读取完整 selected Scene Skill**；Scene Craft 只通过 Curator 已编译的短 `Scene Prose Projection` 进入，允许 `NONE`。若 Curator 已投影当前 Plan 排程的 World fact，**该 Reader Release 必须在本章兑现**。普通 World Entry 仍可“动作提出问题 → 1—3 个短直接旁白段回答 → 回现场”；开篇 Public Common Knowledge 则允许在自然落点直接说明，不要求先制造问题。公共常识的完成标准是普通读者读完可以直接复述规则，而不是从火盆、服装、站位、专名或氛围自己归纳；本章真实跨过已说明的公开力量/身份档位时，结果处直接命名新档位一次，不让读者自己换算。若同一事实还说明地点/势力/传承为什么值得争，保留一个最短价值锚点。Writer 不从完整 World 自选说明主题，也不要求把世界说明伪装成对白；隐藏原因与未来 reveal 继续未知。Curated Context 已明确带入私人欲望且当前场景自然触发时，让一次注意力、身体反应、靠近/回避、想要或短期选择保留它，不统一净化成职责协作与成熟沟通。决定完成后的普通实施默认一句或短段概括。 非核心 Supporting Skill 即使承担一个关键动作，也写到“做了什么 / 为什么有效 / 结果”就停；Reader Release 已给 named 对象公开类别时，首次识别可直接说清一次。高价值非对称优势显露时，不把“克制”理解成只写一个停顿：若现场本来有真实观众且 Projection / Authority 已提供足够尺，**群体震动、懂行者 Ruler Calibration、关键人物 Behavioral Repricing 三者没有高低之分，可以在大型 Public Proof 同时吃满**。主力量已有精确主尺时，三路使用同一数字坐标：全场鸦雀无声、喧哗骤停或所有人明显震惊承受“43级打赢58级”这种差距的现场重量；懂行者直接说清双方精确位置、正常差距和异常点；关键人物再用报价、称呼、站位、战术或待遇变化证明这个“精确位置 + 超标表现”的社会价格。**Public Proof 不授权隐藏机制知识**：NPC 只说现场可观察表现、公开 ruler 与 World/Canon 已知现象；Writer 看见 Frozen Power 不等于角色知道其永久性、私有触发或内部状态，后者由 POV、后续自然复用或合法 Meta Authority 确认。精确位置不是胜负公式，越级获胜不自动升级。RSE / Meta/UI 也只锁事实与 reader-safe anchors，任务、退出、携带等其余措辞优先翻成“还剩多久 / 出口在哪 / 能带走什么 / 失败怎样”的直接语言。只避免凭空造观众和让所有人轮流说同一套专业解释。Planning 的抽象标签不直接变成旁白总结。

**漂亮二段论不得重复成章法**：Primary 可以在真正关键处自然出现一次短促对照或金句，但不得把“事实 / 动作已经成立 → 另起短句裁断或否定翻转 → 再升华其意义”复现为整章稳定收束语法。`他不怕 A。他怕的是 B。`、`他只会 A。可这一件事已经够了。`、`一个 X 做 A，另一个 X 做 B`、连续 `不是 A / 不是 B / 而是 C` 都只按语义结构判断，不靠换词规避。若本章已经自然出现一处明显的这种收束，后文不再主动制造第二处；让动作、反应、后果、沉默或下一事件自己完成意义。该约束只作用于 Primary 生成，不新增禁词扫描、style score、Reviewer 或自动重写。

**Story-bearing Texture > Decorative Density**：正文不以“多写”或“多修饰”制造丰富感。每个主要 beat 选择少量真正改变画面的具体动作、物件/空间、身体反馈、力量后果和人物差异化反应；感官细节选择最有辨识度的少数锚点，不机械覆盖五感。细节如果不承载人物、冲突、因果或幻想体验，就继续压缩。

该原则已通过 2026-08-24 五场景冻结 A/B：两个独立盲评合计 **Texture 9 胜 / Baseline 1 胜**，正式冻结为 `Story-bearing Texture v1`。冻结含义是：保持“故事承载细节而非装饰密度”的核心实现，不再以一般性“多描写”替代它。战斗 / Action 场景仍需特别压缩力路、受力、步骤和机制拆解；未来如优化，只做窄范围 Action/Combat refinement，不回退本原则。

**长期历史未知边界**：Curated Context、Canon 或 Open Promise 已明确为未知、未解释、真假未定、原因未明的过去事实，不因进入正文就自动成为可补写的背景。除非 Director Contract 明确规定本章哪一个新事实成为确定事实，Primary 只能创造当前场景的动作、对白措辞、即时证据、感官和人物暂时判断；不得为了让场景显得完整，把几十 / 几百章前的秘密经历、旧对话、隐藏动机、既有知识或世界机制补成 retrospective canon。

该边界已经通过 Chapter 120 / 600 压力 A/B 验证并冻结为 `Long-History Fact Boundary v1`。最终版本除 Prompt 顶层事实规则外，还把 Curator 已识别的 Open Promises / 未解机制 / 未兑现事项确定性投影为约 300 多字的 `UNRESOLVED FACT BOUNDARY`，放在 Chapter Mission 之后、正文连续性之前；不增加模型调用。冻结样本中两章的核心 unknown discipline 均达到盲评 5/5。已知残余是极少数后台章节编号可能被 Writer 自我纠正式带入正文，这属于 prose hygiene，不改变 Canon，也不应通过新增 continuity agent 解决。

### Authority Reviser — Preservation-First Authority Recovery

Primary Writer 先用窄上下文完成一版完整正文；Authority Reviser 再以该稿为唯一底稿，用更接近上游原始权威但仍安全的投影做**局部恢复与笔墨校正**。默认模型是 GPT-5.6 Luna high，raw GBrain OFF。

Reviser 输入包括冻结 Chapter Mission、Curator、safe World Authority、逐条 Reader Release、Frozen Power + Human Core、Canon 与 Primary Draft。若当章选中的 Scene Skill 有经过 A/B 验证、可局部安全执行的一行 `Revision Watch`，只额外注入这条 failure-triggered 提醒；完整 Generation/Revision Lens 不进入 Reviser。它首先保护已正确的正文，但 **Preservation First 不保护 process carrier**：没有明确问题的句段默认逐字保留；多段“谁守哪 / 谁撤哪 / 谁赔什么 / 谁承担 / 谁见证 / 路线与资源怎样分”的协调、责任和程序化实现若没有新的选择/失败/关系变化/不可逆结果，Reviser 应激进压到最短因果，把注意力还给已经批准的 Choice、Power、Rival、Relationship、Reward、Public Proof 和 Consequence。大型主力量 Public Proof 若 Current/World Authority 已有精确位置，Reviser 用同一坐标恢复三条线：群体震动、精确 Ruler Calibration、关键人物 Repricing；不让“很强/很震惊”代替数字差，也不把越级胜利修成主角升级。**Public Proof 不授权专家知道私有机制；Frozen Power Core 是 Reviser 的校正 Authority，不是 NPC 的知识包。** 若 Primary 已把永久性、私有触发或内部状态塞进 NPC 台词，保留真实 Power Delta，把确认来源移回 POV / 自然复用 / Meta。相反，如果 Primary 已在同一批准事件里用一次自然再次使用，让读者亲眼看见私有永久/累积能力真的留下，并且这次使用直接造成已批准结果，默认保留，不按重复证明删除。RSE / Meta/UI 同样保事实语义、不还原后台抽象原句。生活细节仍必须来自 safe World Authority，不为“更生动”临时创造风俗、建筑或制度。

同一维度出现冲突时，Frozen Mission / Canon / safe World / Frozen Power / Frozen Human 高于 Curator / Primary，Reviser 必须按语义扫描最终全文，不能只修第一处。若冲突段落里有一句本身合法、只是挂在错误时点/因果上的 Core Fantasy / Relationship / Desire / Payoff / Surprise / Social Repricing，先逐句 salvage 到最近合法位置，再继续压缩周围 process carrier；保护一句高价值文本不等于保护整段实施。

开篇公共常识还要做 clarity recovery：如果 Primary 只留下了生活细节/意象，却没有让普通读者直接知道已排程的力量、强弱、危险或社会入口规则，Reviser 补最小直接说明。Texture 可以保留，但不能替代 Orientation。Planning / Authority 的 `身份入口 / 行动空间 / 社会重新定价 / 持有状态 / 责任边界` 等后台意义若直接漏进人物对白或贴身叙述，则翻译成这个人会说的话、具体待遇或具体动作，不做禁词替换。Frozen Mission 中的上游计划结果同样是 realization authority：若计划明确批准“进入 / 踏入 / 晋升 / 突破 / 提升到 / 达到 / 成为”某个里程碑，而第一次 Authority Revision 仍只给战绩/氛围暗示，Run Ledger 不直接采用该稿，而是把同一个 Reviser 收窄成一次 `Outcome Repair` retry。数字主尺同样适用：42级越级击败58级不能替代批准的“提升到43级”。这个 retry 只补最小合法因果与一次直接命名，最多一次；仍漏则保持 failed，不能进入 State。

它不是第二次剧情创作：不能改变事件顺序、人物决定、胜负、资源得失、伤势、身份结果、Direct Result、State Change、Ending 或 unknown boundary。删除程序载体时必须保留它之后真正发生的 Consequence；如果一段承载新的 State Change、Social Repricing、Reward、Relationship Change、New Desire 或 Next Opportunity，就不能因为含“报告 / 登记 / 说明”而整段删除。

这个职责来自受控 A/B：同一冻结 Primary Draft 比较 Luna `low / medium / high / xhigh / max`，high 是第一个在 Ch5/6/9/10 四类压力下全部完成关键 authority 检查的档位；xhigh/max 没增加可见净收益且 Preservation 更差。该模型结论是 Current Default，不是 prose 永恒原则。

### Specialist / Integrator — Bounded Repair

Specialist 只看职责相关的 Authority Revision 局部和 Curated Context，最多给局部 Patch；Integrator 只以 Authority Revision 为底稿，并且只在真实存在下列问题时有限修复：

- Planning summary 替代了场景结果；
- 重大事件没有人物反应；
- 结果前堆积了机制说明；
- payoff 被重复解释；
- 对话、动作或 POV 声音被抽象总结覆盖。

如果 Authority Revision 已经自然，Integrator 保持原文；任何修复都不得改变主要事件、直接结果、人物决定、资源/能力状态或章节结尾推动。

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

最终 `chapter-NNNN.md` 只保存正式小说正文：默认来自 Authority Reviser；显式 repair 时若 Integrator 产生有效最终稿，则保存 Integrator 最终正文。Primary 在 `curator_primary` 中只是第一版草稿，不能直接成为最终来源；State 也只从 Run Ledger 的最终正式来源读取。

以下内容必须与正文分离：Audit、事实摘要、repair notes、字符/token 统计、运行 metadata 与 provenance。

调用方已有正文/审计分区合同时，继续遵守现有合同，不另建第二套格式。本层不自动写 BOOK，不自动批准章节，也不自动覆盖已有章节。
