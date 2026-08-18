# Story MVP Novel Prose Realization

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
4. Writer A / B / C 的清晰职责；
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
2. 说明必须绑定当前决策；
3. 具体动作和物件优先于抽象总结；
4. 叙述距离可以变化，但不能无目的漂移；
5. 句段节奏服从场景压力；
6. 对话必须改变信息、关系或行动；
7. 内心活动必须产生下一步；
8. 动作要形成“观察—行动—反应—空间变化—结果”；
9. payoff 不做三重说明；
10. 情绪允许延迟、不完整和嘴硬；
11. 章末必须留下新状态或新理解；
12. Humanizer 审查结构，不建立禁词和禁标点表。

完整证据和单书差异见 `PROSE_DISTILLATION_THREE_CLASSICS.md`。

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

当前最小管线：

`BOOK / Plan / Saved Chapters`

→ `Current Chapter Outline Hard Gate`

→ `Chapter Prompt`

→ `Writer A: Scene Draft`

→ `Writer B: Continuity & Realization`

→ `Writer C: Prose Realization & Bounded Humanization`

→ `Separated Audit`

→ `Author Approval`

→ `chapter-NNNN.md`

Prose Realization 不新增第二个 Draft API，也不在章节保存后盲目重写正文。

---

## 7. Writer Protocol

### Writer A — Scene Draft

目标：让小纲中决定的事情真的发生。

重点：

- 场景；
- 动作；
- 人物反应；
- 对话；
- 空间；
- payoff；
- 因果桥接。

A 不追求最终润色，但不能只把小纲扩写成概述。

### Writer B — Continuity & Realization

B 完整看到 A 后修复：

- 时间或地点跳切；
- 人物、能力或物品突然出现；
- 重要动作被一句话跳过；
- 对手或世界没有反应；
- 关系不连续；
- 桥接不存在；
- 关键场景过薄。

B 不得改变当前章主要事件、直接结果、状态变化和结尾推动。

### Writer C — Prose Realization & Bounded Humanization

C 完整看到 B 后处理：

- 重复能力说明；
- 重复身体状态；
- 重复情绪；
- 泛化措辞；
- 均匀句段；
- 不自然对话；
- 无功能连接；
- payoff 重复解释；
- 多余总结；
- POV 声音漂移。

C 可以重组句子和段落，但不得改动 B 已确定的事实和因果。

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

最终 `chapter-NNNN.md` 只包含 Writer C 的正式小说正文。

以下内容必须与正文分离：

- Writer A/B/C 字符数；
- SUBAGENT_MODE；
- continuity audit；
- prose audit；
- repair notes；
- 事实摘要；
- provenance。

调用方已有正文/审计分区合同时，Skill 必须遵守现有合同，不另建第二套格式。

本层不自动写 BOOK，不自动批准章节，不自动覆盖已有章节。
