---
name: novel-prose-realization
description: >-
  在 Chapter Contract 已决定事件之后，把中文长篇小说场景写成自然、具体、可读的商业网文 prose。
  只控制表达方式，不负责故事规划、Canon、人物事实、Progression 或草稿审批；使用当前书 Prose DNA、
  Reference Corpus 的抽象 prose controls 和有界的人性化审阅。
---

# Mission

本 Skill 是 Draft 阶段的 Novel Prose Realization Layer。它回答“已经决定的事情应该怎样落到中文句子、段落、
对话和场景里”，不回答“下一章发生什么”。目标是自然、具体、可读、有角色感的商业中文网文，不是文学总分，
也不是规避 AI 检测器。

它与 `reference-corpus-distillation` 保持两个独立职责：

- `reference-corpus-distillation`：理解故事设计、推进、回报、机制和结构。
- `novel-prose-realization`：把已冻结的场景决定写成 prose。

禁止把两个 Skill 合成一个全能 Skill。Prose DNA 只保存写法变量和来源定位，不保存来源正文、作者身份、
来源人物口癖、签名比喻或可直接仿写的长句。

# Authority

故事事实和事件顺序的权威顺序是：

`Chapter Contract > Canon > Current Scene Context > Prose Controls`

Prose Realization 不得：

- 修改 Chapter Contract、Canon、Boundary、人物事实或资源状态；
- 发明关键情节、删除必需 payoff、添加新的成本，或改变 Progression；
- 以“这样写更自然”为理由改变事件、线索、选择、不可逆改变或结尾状态；
- 用来源书的角色、设定、专名、事件、作者身份或句法作为模板。

只在表达层做选择：句子和段落节奏、叙述距离、信息显隐、对话轮次、动作顺序的呈现、感官细节、内心落点、
过渡方式、段落收束和章节结尾的落点。

表达控制的优先级是：

`Current Book Prose DNA > Author Explicit Style Intent > Reference Corpus Prose Controls > Humanizer Generic Guidance > Generic LLM Prior`

这条优先级只解决“怎么写”，不能覆盖上面的故事权威。

# Pipeline Position

`Reader Kernel / Core / Foundation -> Planner -> Chapter Contract -> Novel Prose Realization -> Draft -> Prose Humanization Audit -> Validation`

Humanization Audit 不是第二个 Draft，也不是故事改写器。它只把表达问题报告给 Repair Pass。

# Before Writing

在动笔前读取并冻结：

1. 当前 Chapter Contract、Continuation Boundary 和本章允许的 POV；
2. 当前 Canon、角色状态、知识边界、资源和线程证据；
3. 本章场景的动作、选择、回报、代价和结尾状态；
4. 参与角色的当前语气与关系距离；
5. 当前书的 `prose-dna/<source_book_id>.md` 或 ORIGINAL 小说的 `Original Prose Profile`；
6. 只加载本场景真正需要的 `prose-controls/`，并把它们当作软提示；
7. 明确哪些信息角色知道、哪些信息读者知道、哪些信息暂时不能解释。

如果当前书没有 Prose DNA（例如 ORIGINAL），使用 Reader Kernel、Genre/Tone、Narrative Drive 和选定的
Prose Controls 形成目标书的 `Original Prose Profile`，不得随机挑一本来源书模仿。

# Drafting Principles

## 具体先于解释

优先让动作、物件、停顿、反应、环境变化和选择结果承载信息。抽象判断可以出现，但不自动跟在每个事件后面
解释“这意味着什么”。如果读者已经能从场景看出结果，删掉重复的旁白结论。

## 节奏由场景压力决定

不要把每段写成固定的三四句，也不要追求平均句长。危险、追逐和决断允许更直接；观察、关系和余波可以放慢。
短句是动作工具，不是全篇鼓点；长句是容纳感知和犹豫的工具，不是装饰。

## 段落结尾要有功能

段落可以落在动作、反应、物件、信息缺口、未说完的话、选择或安静状态上。不要让每段都用金句、总结或悬念
收尾。

## 叙述距离要随场景变化

近距离场景允许身体感受、偏见、误读和不完整信息；远距离场景可以交代空间、制度或跨人群变化。不要在同一
个关键动作后同时做事件说明、旁白解释、角色思考和总结，形成四层同义复述。

# Dialogue Principles

- 对话承担欲望、遮掩、试探、关系和行动，不只是把背景资料轮流说出来；
- 角色不必回答对方已经知道的问题，允许误解、避答、抢话、停顿和未完成的句子；
- 让角色的词汇、句长、礼貌程度、攻击性和沉默方式有差异，但不写固定口癖表；
- 对话后保留动作或反应，让一句话改变现场，而不是用旁白解释它“体现了人物的复杂内心”；
- 不把 Humanizer 的通用口语化建议硬套进古风、历史、专业或紧张场景。

# Action Principles

动作先于解释。写清楚谁看见了什么、做了什么、对方如何反应、空间怎样改变、下一步因此受限或打开。动作
可用感官细节和判断穿插，但不要把战斗写成技能名列表，也不要在每个招式之后补一个同义的胜负总结。

# Payoff Principles

回报在场景中完成：读者看到能力被验证、资源被获得、地位被改变、关系被推进或谜团被揭开。避免“预告回报 ->
场景展示 -> 立即总结回报”的三重说明。回报之后可以留下余波或新问题，但不能用 prose audit 删除 Contract
要求的 payoff。

# Exposition Principles

世界和规则说明要绑定当前人物的需要、选择或风险。优先给出本场景能观察到的规则结果；必要的背景分批进入。
不要写成百科、新闻稿、讲义或“首先/其次/最后”的提纲。专业词可以保留，解释应服从角色知识边界。

# Emotional Principles

情绪通过动作、身体反应、选择、沉默、关系距离和信息不完整落地。抽象情绪词不是禁用词，但同一情绪不要由
动作、旁白、内心和总结连续重复。安静余波可以保留未解决的感受，不强行升华。

# Rhythm, Description and Chapter Ending

- 感官细节挑能改变判断或关系的少数细节，不堆满镜头；
- 过渡以时间、空间、动作、注意力或因果自然发生，少用机械连接词；
- 章节结尾允许动作落地、关系停在一句话上、信息被重新理解、余波安静展开，或留下合理问题；
- 不是每章都必须 cliffhanger，也不是每章都必须总结主题；
- 词汇、标点和幽默服从当前书与场景，不为制造“人味”故意加错字、俚语、噪声或逻辑缺口。

# Anti-AI Prose Audit

对每个 Draft 只做结构性、人类可解释的审阅，不计算 AI 分数。检查：

- 场景是否真的发生，还是只在概述结果；
- 具体动作和后果是否先于抽象结论；
- 是否重复解释显而易见的结果或同一个情绪；
- payoff 是否被提前宣布并在场景后立刻再次总结；
- 对话是否在复述已知信息，角色声音是否可区分；
- 句子、段落和高低张力是否有随场景变化的节奏；
- 是否出现机械三段式、频繁否定排比、连接词串联、抽象名词堆叠或新闻稿语气；
- 感官细节是否选择性服务于 POV 和行动；
- 是否保留信息不完整、沉默、潜台词和合理的反应差异；
- 是否保留 Chapter Contract 的事件顺序、选择、线索、payoff、不可逆改变和结尾状态。

这些是 review triggers，不是逐词禁用清单。Humanizer-zh 的文章/营销规则不能直接当成小说硬规则。

# Repair Pass

先在生成时减少模板表达，再做有界修复。修复只处理：填充、冗余解释、重复解读、均匀节奏、不自然对话、泛化
措辞、过度 signposting、无必要总结和明显 AI 连接词。

修复绝对不能改变：事件顺序、Canon、payoff、线索、setup、选择、角色意图、句子实际含义、不可逆改变或章节
结尾状态。若表达问题与故事决定冲突，保留故事决定并报告冲突，不自行改故事。

# Source-Style Leakage Boundary

Reference Corpus 只提供抽象控制。禁止：

- 大量复制来源句子或连续长摘录；
- 把一本来源书当成唯一 exemplar；
- 指令化地“模仿作者 X”；
- 迁移来源角色口癖、签名隐喻、专名或长句法；
- 用来源书 Prose DNA 覆盖当前书的显式风格意图。

# Output Boundary

本 Skill 输出的是 Draft prose、Prose Humanization Audit 和有限 Repair Pass。它不会写入 Canon，不会修改
Chapter Contract，不会把 `REFERENCE_ONLY`、`INFERENCE` 或 `PROSE_ONLY` 提升为事实，也不会把 Prose DNA
当成作者永久文风。

Influenced by: `op7418/Humanizer-zh`。本项目重写并收窄其原则到中文商业小说 prose，不复制其技能文本或文章示例；
Humanizer-zh 的来源与许可证记录见 `docs/NOVEL_PROSE_REALIZATION.md`。
