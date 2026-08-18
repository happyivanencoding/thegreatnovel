# real-exp-002 Cleanroom Experiment

## 预注册信息

- `SYSTEM_FREEZE_COMMIT`: `8fbb1b42a1e0548426d43f213505ebc414915719`
- `EXPERIMENT_BRANCH`: `exp/cleanroom-real-exp-002`
- `EXPERIMENT_COMMIT`: 待实验结束后填写；若实验失败且按规则停止，则记录实际提交状态
- `CREATED_AT`: `2026-08-18`（Europe/Paris）
- `CREATIVE_DIRECTION`: 现代都市职业成长男频爽文
- `EXPERIMENT_QUESTION`: 当前冻结的 Story MVP，在不修改系统的情况下，能否从一个宽泛的现代都市职业成长方向，独立产生可持续的故事结构，并生成连续、具体、自然的前三章正文？

## 隔离与边界

本实验从冻结 commit 独立创建，不复制、改皮或引用 `real-exp-001` 的人物、世界、术式、道具、剧情结构、GBrain query 或 Reference 选择。输入只提供以下方向与边界：现实世界；不使用超自然能力、修炼体系、战斗升级、学院试炼、遗迹、副本或异世界；主角成长主要来自职业能力、信息、流程、资源、关系、谈判、项目或商业机会；具体主角、职业、核心优势、人物关系和故事玩法由当前系统生成。

实验期间不得修改 `src/**`、`tests/**`、`docs/**`、`.agents/**`、`pyproject`、配置、runtime code、默认 Prompt 或 Skill；不得直接编辑任何正式章节文件；不得人工修正文后继续实验。若出现明显系统失败，保留全部输入和原始输出，记录失败层级并停止受影响的后续步骤。

## 预先注册的验收标准

本节在第一次调用 GBrain 或生成 Idea 之前冻结。实验结束后只提供证据与判断，不用词频、AI detector 或总分替代人工判断，也不事后改变标准。

### A. Idea

- 核心优势具体，而不是泛泛的“努力、聪明、信息差”标签。
- 核心优势真实改变主角的行动方式。
- 核心优势可以重复利用，并具有复利空间。
- 第 3—10 章能看到核心优势的可见兑现。
- 3—5 个候选之间存在实质结构差异，而不只是更换职业名称。

### B. BOOK / 100 章

- Reader Promise 清楚。
- 成长对象具体。
- 主循环可以重复但不会机械复制。
- 100 章规划存在阶段换挡。
- 大型剧情块写成具体事件，而不是抽象功能清单。
- 结构不无理由滑向战斗、升级、学院、遗迹等旧语境。

### C. 未来十章

- 十章是连续故事，而不是十个独立任务拼盘。
- 每章结尾能以因果关系进入下一章。
- 有具体人物、行动、反应和结果。
- 不用“危机升级、关系深化、获得认可”等抽象短语替代剧情。

### D. Chapter continuity

- 第 2 章真实读取第 1 章正文；第 3 章真实读取第 1—2 章正文。
- 地点、时间、人物、物品、已知信息、资源、关系、未完成即时目标前后连续。

### E. Scene realization

- 八字段在场景中真正发生。
- 重要动作被场景化。
- 对手或环境产生真实反应。
- payoff 实际发生。
- 正文不是把小纲扩写成带情节名词的长摘要。

### F. Prose

- 名词具体但不过量；动词写出动作和结果。
- 对话改变现场。
- 句长和段落随场景变化。
- 推理影响下一步行动。
- 说明绑定当前需求。
- 情绪避免重复解释。
- payoff 没有三重说明。
- 没有明显 AI 模板重复。

## 执行协议与 provenance 字段

以下字段先留空，必须在真实流程完成后用实际值追加；不知道就写“未保留”，不得补造。

- 实际新书创建流程与页面/应用状态：待记录
- GBrain query：待记录
- GBrain raw results：待记录
- VALIDATED Reference Programs 实际选择（最多 3 个）：待记录
- Idea Prompt：待记录
- Idea 原始候选：待记录
- 最终选中候选及选择理由：待记录
- Outline Prompt：待记录
- 原始 BOOK：待记录
- Proposal → BOOK 应用流程：待记录
- 前十章事件链概要：待记录
- 第 1 章八字段小纲：待记录
- 第 1 章最终 Prompt：待记录
- 第 2 章八字段小纲：待记录
- 第 2 章最终 Prompt：待记录
- 第 3 章八字段小纲：待记录
- 第 3 章最终 Prompt：待记录
- `SUBAGENT_MODE`：待记录
- Writer A task/agent ID：待记录
- Writer B task/agent ID：待记录
- Writer C task/agent ID：待记录
- Writer A/B/C 字符数：待记录
- 正式正文提取与 chapter save 流程：待记录
- 是否发生系统失败：待记录
- 是否发生任何人工内容修改：待记录
- provenance 完整性：待实验结束后判断

本文件是实验记录，不是系统实现；已有记录只追加，不为了制造 PASS 而改写。

## 已发生的输入与生成记录

### 页面输入的创作方向

```text
现代都市职业成长男频爽文。

边界：
- 现实世界；
- 不使用超自然能力；
- 不使用修炼体系；
- 不使用战斗升级；
- 不使用学院试炼；
- 不使用遗迹、副本或异世界；
- 主角成长必须主要来自职业能力、信息、流程、资源、关系、谈判、项目或商业机会；
- 具体主角、职业、核心优势、人物关系和故事玩法全部由当前系统正常生成。
```

### 实际默认 GBrain query

```text
主角成长型虚构世界小说；作者创作方向：现代都市职业成长男频爽文。边界：- 现实世界；- 不使用超自然能力；- 不使用修炼体系；- 不使用战斗升级；- 不使用学院试炼；- 不使用遗迹、副本或异世界；- 主角成长必须主要来自职业能力、信息、流程、资源、关系、谈判、项目或商业机会；- 具体主角、职业、核心优势、人物关系和故事玩法全部由当前系统正常生成。。
寻找 Reader Promise；Character Desire & Agency；Advantage / Special Capability；Repeatable Reader Loop；Core Progression Grammar；Action-Space Expansion；World Expansion Grammar；Social / Relationship Dynamics；Resource / Economy；Narrative Drive；Phase Transition；Failure / Fatigue Risks；Book DNA；Mechanism；Contrast；Reference Program，生成可以自由采用经典主干、新型组合或混合结构的创意。不要从当前 BOOK 设计猜测作者未表达的方向。
```

- 记录时间：2026-08-18T23:35:50+02:00（Europe/Paris）
- GBrain 状态：尚未调用；结果：未生成
- Reference 选择：尚未进行

### GBrain raw results（实际 stdout）

- 调用时间：2026-08-18T23:36（页面返回时间；精确秒未单独保留）
- 页面状态：`GBrain：可用`
- 返回字符数：`3099`

```text
[0.8547] arcs/rcv0-23-xianxia-jiantu-zhi-lu-arc-v1-03 -- ## Local Creative Problem

如何让一个看似无欲望的成年人拥有足以启动长篇的具体欲望。

## Setup

职业、婚姻和日常生活都趋于平淡，但剑术距离感给出可测量天赋。

#
[0.8357] book-dna/rcv0-03-dushi-xiuzhen-chatianqun -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

普通都市生活被一个可交流、可求助、可行动的修真社群接口打穿；读者持续获
[0.8223] book-dna/rcv0-20-gaowu-quanqiu-gaowu -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者先享受重生带来的资源套利、制度误读和武科竞争，再追逐个人战力、身份
[0.8064] arcs/rcv0-26-qihuan-tianqi-yubao-arc-v1-03 -- ## Local Creative Problem

如何把一个现实中的职业错配转成具有情感历史的超自然入口。

## Setup

主角有技能却只想找兼职，市场按外形和岗位需求而非真正能力判断他。

[0.7933] book-dna/rcv0-02-xianxia-bailian-chengxian -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

资质普通甚至受限的修士，通过勤修、资源、准备和危险路径持续获得可验证的
[0.7832] prose-controls/action/action-before-interpretation -- # Action Before Interpretation

## 支持范围

- 支持书本数：16+
- 支持类别：玄幻、仙侠、科幻、奇幻、武侠、历史、高武、灵异、游戏、其他
- 证据卡：
  `
[0.7732] syntheses/categories/synth-category-03 -- ## Evidence Scope

MULTI_BOOK；3 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.7616] book-dna/rcv0-14-wuxia-langzi-jianghu -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者追逐一个有能力、受欢迎又不愿被随意支配的江湖人物，看他在名望、关系
[0.7517] syntheses/categories/synth-category-02 -- ## Evidence Scope

MULTI_BOOK；3 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.7425] arcs/arc-personal-wish-to-historical-scale-v1 -- ## Local Creative Problem

宏大历史和文明危机扩展后，如何不让具体的日常愿望被叙事抛弃。

## Setup

主角从普通人的冒险、家业或陪伴愿望出发。

## Promis
[0.7324] book-dna/rcv0-13-wuxia-jinyong-shijie-daoshi -- ## Evidence Coverage

OPENING；EARLY；MID；LATE；END

## Reader Promise

读者先享受隐居日常与轻易能力，再期待好奇、调查和声望把主角带入
[0.7228] maps/progression-and-breakthrough -- ## 进阶与突破

这是导航层，不是 authority taxonomy，也不是创作 Hard Gate。

## 可检索卡片

- `rcv0-01-xuanhuan-wangu-shendi-dn
[0.7138] book-dna/rcv0-19-gaowu-wozai-jingshenbingyuan-xue-zhanshen -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者先从公共日常对异常人的误读中获得轻微喜剧和悬念，再追逐能力系统、团

[0.7052] syntheses/categories/synth-category-01 -- ## Evidence Scope

MULTI_BOOK；3 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.6951] arcs/rcv0-24-dushi-shoushu-zhibojian-arc-v1-03 -- ## Local Creative Problem

如何让系统赠予的第一次奇迹转成主角自己的职业能力。

## Setup

限时峰值直接完成高难手术，主角身体不完全由自己控制。

## Promi
[0.6868] book-dna/rcv0-16-youxi-hupozhijian -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者追逐一个普通人的训练、探索和战斗本能如何打开更大的奇幻世界；能力提
[0.6787] prose-dna/rcv0-03-dushi-xiuzhen-chatianqun -- # Prose DNA

仅保存中文 prose 执行观察与来源定位；不保存来源正文。

## Sampling

- coverage mode: `SCENE_FUNCTION_WINDOWS`

[0.6698] syntheses/categories/synth-category-07 -- ## Evidence Scope

PILOT_TWO_BOOK；2 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.6628] syntheses/categories/synth-category-10 -- ## Evidence Scope

PILOT_TWO_BOOK；2 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.6551] prose-dna/rcv0-20-gaowu-quanqiu-gaowu -- # Prose DNA

仅保存中文 prose 执行观察与来源定位；不保存来源正文。

## Sampling

- coverage mode: `SCENE_FUNCTION_WINDOWS`
```

### 实际 Reference 选择

- 选择时间：2026-08-18T23:37:46+02:00（Europe/Paris）
- 实际选择数量：1 / 3
- 实际 `program_id`：`rcv0-24-reputation-research-training`
- 选择理由：这是当前页面中最直接对应“职业能力从个人实践转为可复现能力，并通过网络认可、机构谈判、培训和更难测试继续扩张”的程序；相较其它卡片，它最接近职业成长的转换关系。卡片原文仍带有 clinical 语境，因此可能对职业选择产生偏置，作为实验输入风险保留，不宣称它是领域中性的。
- 未选择其余程序的理由：多数程序明确绑定修炼、宗门、战斗、农业家庭、临床救治或具体超自然入口；在宽方向实验中继续选择会提前收窄系统应自行生成的职业和核心玩法。

#### 选中卡片原文摘录

```text
program_id: rcv0-24-reputation-research-training
story_phase: Major Arc Transition / reputation becomes institutional capital
input_state: Repeated clinical successes have created reputation, but the protagonist's methods must be tested, taught, researched, and negotiated across institutions.
central_pressure: The protagonist must convert private practice into reproducible capability without losing time, trust, or control of credit.
reusable_program: Repeated proof -> network recognition -> institutional negotiation -> deliberate training -> harder test.
applicable_conditions: A serial protagonist's competence can become social or academic capital.；Mid-story escalation should change the institution around the protagonist.
failure_modes: Turning every success into automatic status without credit conflict.；Letting training replace real uncertainty rather than prepare for it.
anti_repetition_notes: A reputation payoff must create a new gate or negotiation, not only praise.；Training has value only if a later real-world uncertainty tests it.
output_state: The protagonist has institutional capital and a team whose future depends on how credit and capability are shared.
```

- Reference 数据状态：页面显示为 `VALIDATED`；没有修改 Reference 文件。

### Idea 原始返回（实际候选，未修改）

- 生成方式：使用已记录的实际 Idea Prompt；当前 Agent 直接产生创作返回
- 原始返回文件：`IDEA_RAW.md`
- 候选数量：4
- 原始内容人工修改：否

### Idea 选择结果

- 选择状态：已选择候选 2
- 选择理由：候选 2《把空车卖成通道》最直接把职业能力、信息、流程、实体资源、关系、谈判和商业机会串成可重复循环；其第一章到第十章有可见的订单、路线、延误、结算和节点变化，100 章可从个人调度换挡到区域网络、平台规则和供应链方案。它也明确留在现实世界，不需要超自然、修炼、战斗、学院或遗迹语境。
- 选择依据：候选 1 的证据链和候选 3 的试点循环具体但存在单一复盘/评审重复风险；候选 4 的现金时间表有复利但早期更容易说明化。候选 2 的空间节点和现场反应最适合检验 E/F。
- 选择动作：只选择 `IDEA_RAW.md` 中完整的“候选2：把空车卖成通道”；没有修改该候选的任何文字。

### 实际 Outline Prompt

- 生成时间：2026-08-18T23:41（Europe/Paris；精确秒未单独保留）
- Prompt mode：`outline`
- 页面实际创作方向输入字符数：1994
- Outline Prompt 字符数：10751
- 完整原文：`OUTLINE_PROMPT.md`
- 人工修改后发送：否
- 页面输入 warning：候选原文通过单行 input 进入页面，换行被压平；候选文字仍存在于 Prompt，没有内容丢失。此 warning 不在本步升级为系统失败，后续继续观察 BOOK 是否受影响。

### BOOK 原始返回与 Proposal → BOOK 保存流程

- 原始 BOOK 返回：`BOOK_RAW.md`；模型返回字符串长度 13122，文件末尾由落盘工具保留一个换行，文件长度 13123
- 页面 Codex 返回区：回读字符数 13123；首行为 `# 小说总体设计画像`；末行为空
- Proposal 流程：点击“将 Codex 返回放入 Proposal 编辑区”，页面回读 Proposal 长度 13123；点击“保存 Proposal”，状态为“Proposal 编辑区已保存到 PROPOSAL.md”
- Proposal 文件：Windows 换行后 13461 字符；规范化为 LF 后与 `BOOK_RAW.md` 完全一致
- BOOK 应用流程：点击“将 Proposal 应用到 BOOK 编辑区”，页面报告已应用 16 个 BOOK 区域；各总体画像、100 章计划、十章小纲和状态区均非空
- BOOK 保存：点击“保存 BOOK.md”，页面状态为“BOOK.md 已保存”
- BOOK 文件：Windows 换行后 13461 字符；规范化为 LF 后与 `BOOK_RAW.md` 完全一致
- 人工内容修改：否；只执行了当前页面的 Proposal→BOOK 正常应用和保存动作
- BOOK 当前状态：已保存，尚未生成章节正文

### 第 1 章八字段小纲与最终 Prompt

- 八字段小纲原文：`CHAPTER-0001-OUTLINE.md`
- 八字段字符数：`509`
- 最终 Prompt 原文：`CHAPTER-0001-PROMPT.md`
- Prompt mode：`chapter`
- Prompt 字符数：`17969`
- 前两章正文输入字符数：`0`（第 1 章按流程为空）
- 当前大型剧情块输入字符数：`697`
- 人工 Prompt 修改：否
- Hard Gate：八个字段均非空，页面生成成功

### Writer A → B → C provenance 与第 1 章保存

- `SUBAGENT_MODE`：`actual`
- Writer A：task/agent ID `01a016de-29b2-73f0-a3ea-e36c19fb5e76`；自报正文 `2697` 字符；中间稿 `CHAPTER-0001-WRITER-A.md`；主线程复制稿在文件终端换行前为 `2699`，文件含终端换行为 `2700`，差异已记录为通知/Markdown 尾空格 warning
- Writer B：task/agent ID `01a016e2-825b-7933-a623-8e81c1250c63`；自报正文 `2989` 字符（不计换行）；B 任务写入 `CHAPTER-0001-WRITER-B.md`，去除所有换行后核对为 `2989`
- Writer C：task/agent ID `01a016e7-00f1-73d2-8364-17019b34f745`；自报正文 `2784` 字符（不计换行）；完整返回 `CHAPTER-0001-WRITER-C-RAW.md`；正式正文区块和最终 chapter 去除换行后为 `2786`，差异为两处 Markdown hard-break 尾空格
- C 返回契约：三个一级标题恰好存在；事实摘要去除换行后 `142` 字符；正式正文不含 Writer Audit 或事实摘要
- 正式正文保存流程：C raw → 页面 Codex 返回区 →“提取正式正文”→页面正文 `2957` 字符/去换行 `2786` →“批准并保存章节”→ `chapters/chapter-0001.md`；磁盘正文与 C raw 正式正文区块规范化换行后完全一致
- 正式正文人工修改：否；没有直接编辑 `chapter-0001.md`；没有把 Audit/摘要写入正文
- 第 1 章结果：完成；Writer A/B/C 均为 actual；chapter save API 成功

### 实验停止与系统失败记录

- 停止时间：2026-08-19T00:10:29+02:00（Europe/Paris）
- 停止层级：第 2 章 continuity UI / 章节编号 change 监听，不是 GBrain、BOOK、Writer 或 chapter-0001 保存层
- 触发证据：页面章节编号显示 `2`，但 `previous-chapter-text` 长度始终为 `0`；第 1 章保存区仍保留正文 `2957` 字符和事实摘要 `142` 字符
- 已尝试的正常页面动作：编号填入 2 并失焦；点击当前章小纲触发失焦；ArrowDown→ArrowUp；ControlOrMeta+A 后逐字符输入 2 并失焦；每次回读都仍为 previous length `0`
- 区分检查：直接读取当前应用 `/api/books/real-exp-002/chapters/1` 返回 HTTP `200`、chapter_number `1`、content `2957` 字符；因此文件/API存在，失败发生在页面自动读取监听没有把第 1 章放入第 2 章上下文
- 正确动作：保留第 1 章和全部原始输入/输出，停止第 2 章及后续；没有用 API 内容手工填入页面，没有生成第 2 章 Prompt、正文或 save
- 实验状态：`STOPPED_AT_CHAPTER_2_CONTINUITY_FAILURE`
- 系统修改：否；`src/**`、`tests/**`、`docs/**`、`.agents/**`、pyproject、Prompt、Skill 均未修改
- 内容修改：候选、BOOK、C 正式正文均未人工修改；只对 provenance 做了明确记录的转录修正，并另存 `IDEA_PROMPT.md` 精确副本
- Provenance 状态：已执行步骤完整；第 2 章未执行的字段保持未发生，不补造 task、Prompt、正文或字符数

## 最终验收判断（实验停止）

### A. Idea

- 判断：通过（候选结构层）。候选 2 的核心优势是把返程空载、仓库时间窗、温区、路线限制、违约记录和节点信用组合成可执行运力表；它改变主角行动方式——从找最低价车辆改为先判断可兑现时间窗和替代节点；可以反复使用，并从单笔订单复利到固定窗口、区域节点和规则权。第 1—10 章的首次兑现已在 Idea/BOOK 中写具体，但因实验在第 2 章停止，只有第 1 章实际正文得到验证。
- 候选差异证据：4 个候选分别以证据责任链、实体运力节点、规则试点、现金时间表为核心转换网络，不是只更换职业名。

### B. BOOK / 100 章

- 判断：通过（规划层）。Reader Promise、成长对象、主循环和五个阶段换挡均具体；五个剧情块共同覆盖第 1—100 章，事件包含急单、损耗、结算、平台控制、跨城网络和大客户合同，没有把主线滑向战斗、升级、学院或遗迹。BOOK 是系统生成后经正常 Proposal→BOOK 应用保存的原文，没有人工润色。

### C. 未来十章

- 判断：通过（规划层，未完成运行验证）。第 1—10 章从权限被收走、三城急单、夜班节点、异常损耗、提前结算、赔掉利润、合同谈判、公开证明到固定夜班窗口形成连续因果链；每章有具体人物、行动、反应、结果和下一章起点，不是十个任务名词。但没有把这份计划伪装成已写成的十章正文。

### 实际 Idea Prompt

- 生成时间：2026-08-18T23:38（Europe/Paris；精确秒未单独保留）
- Prompt mode：`idea`
- 字符数：`6659`
- 来源：页面默认 `idea` Prompt template + 当前页面创作方向 + 当前空 BOOK + 选中 Reference + GBrain 原样结果
- 人工修改后发送：否
- provenance 转录修正：原始内联记录第一行曾多一个字面 `+`，页面实际 Prompt 未含该字符；完整精确副本为 `IDEA_PROMPT.md`，长度 6659。此次仅修正记录，不重跑 Idea。

```text
+你是透明协作的男频成长爽文创意助手。根据作者的粗方向、页面上完整可见的 GBrain Inspiration Results 和手动选择的 Reference Programs，生成 3—5 个明显不同的商业男频成长爽文核心创意。不评分、不排名、不替作者选择，不调用任何外部服务。

当前产品默认目标是成熟中文男频成长爽文。优先寻找具有主角主动性、非对称优势、可重复利用、复利增长、早期兑现和持续行动空间扩大的具体故事。创新应优先体现在玩法和成长路径上，而不是单纯通过悲剧代价、伦理折磨或反爽机制制造“高级感”。这是创作方向，不是机械模板；如果作者明确要求其他类型，以作者要求为准。

当前产品只提供主角成长型虚构世界男频长篇的启动方向。不要预设所有书都沿同一条力量链成长；优先寻找本书自己的非对称位置、成长对象、转换网络、可重复循环、阶段变异和核心不变量。成长可以来自力量、知识、职业、规则、身份、造物、组织、关系、世界通行能力或它们的组合；作者选定具体创意后，以本书成长基因为准。

经典成长模式是一等公民：可组合只表示不强迫所有作品相同，不表示主动回避成熟主干。资源→成长→战斗→身份→更高级资源→更大世界，以及职业→技能→任务→身份、探索→机缘→成长→新区域、内容副本→战斗→战利品→构筑等，都可以成为本书主干。如果作者输入、GBrain证据或当前创意表明某条经典链最适合本书，应当保留它，创新放在新优势、世界机制、转换方式、关系反馈或阶段变异上。

默认创作偏置：主角要有明显主动性；金手指要形成可重复、可放大的非对称优势；代价服务于策略，不负责抵消爽感；1—3 章出现核心异常或优势，3—10 章完成第一次明确利用，10—30 章形成稳定循环或公开证明；成长要打开新的行动空间，每次扩大都带来新的玩法。

核心优势或成长对象必须有纵向成长路线：早期能做什么，随后如何恢复、放大、反推或重新组合，进一步如何打开本书自己的新问题、新关系、新规则或新世界。每个候选说明本书最重要的读者满足和它如何变化，不要求套用直接/间接 payoff 分类。

每个候选还必须输出：
## 成长组合
说明本候选把哪些变量和循环组合在一起。
## 初始转换网络
用箭头说明主角最初怎样把一种优势转换成新的行动能力，允许分叉、反馈和条件转换。
## 长篇变异潜力
说明 100 章内成长对象、行动方式、主要循环或世界理解怎样发生至少几次本质变化，而不是只让敌人变强。
## 与其它候选的真正差异
说明转换网络或循环关系的不同，不能只换题材名、金手指名字、敌人或地图。候选可以共享同一个经典成长骨架，只要非对称优势、资源生成方式、验证玩法、世界结构、核心关系、长期变异或 reader promise 真正不同；不要为了差异强迫某个候选变成纯谜团、纯规则、纯建设或纯关系小说。

不要为了显得高级，默认使用失忆、寿命、感情、伦理诅咒或越成功越痛苦等抵消型代价。除非作者明确要求，否则优先寻找可以复利、早期兑现并自然扩大到 100 章的玩法。

每个候选必须完整使用以下结构：
## 候选N：书名/概念名
一句话创意：主角是谁 + 得到什么非对称优势 + 最直接要解决什么问题。
主角核心优势：它具体能做什么。
为什么这是优势：别人为什么无法轻易复制。
核心爽点循环：主角做什么 → 得到什么 → 怎样进一步放大优势 → 引来什么更高层机会或敌人。
开局1—3章：具体发生什么。
前10章：第一个完整小闭环是什么。
第一个公开证明：主角什么时候让别人第一次真正意识到他的价值、实力或异常。
100章扩张方向：小能力怎样扩大为资源、身份、组织、地域或世界行动能力。
关键关系：至少一个会随主角成长持续改变的人。
最大的重复风险：这个玩法写久以后最容易重复什么。



# 页面当前输入

## 作者粗方向

现代都市职业成长男频爽文。边界：- 现实世界；- 不使用超自然能力；- 不使用修炼体系；- 不使用战斗升级；- 不使用学院试炼；- 不使用遗迹、副本或异世界；- 主角成长必须主要来自职业能力、信息、流程、资源、关系、谈判、项目或商业机会；- 具体主角、职业、核心优势、人物关系和故事玩法全部由当前系统正常生成。

## 当前 BOOK.md（如果作者已经填写）

# 小说总体设计画像

## 0. 本书成长基因图

（请填写这项总体设计。）

## 1. 核心类型与读者承诺

（请填写这项总体设计。）

## 2. 世界观结构

（请填写这项总体设计。）

## 3. 世界如何持续制造剧情压力

（请填写这项总体设计。）

## 4. 主角模型、人物弧与核心矛盾

（请填写这项总体设计。）

## 5. 配角与关系系统

（请填写这项总体设计。）

## 6. 核心情节发动机

（请填写这项总体设计。）

## 7. 叙事结构

（请填写这项总体设计。）

## 8. 文风与可操作参数

（请填写这项总体设计。）

## 9. 对话特点

（请填写这项总体设计。）

## 10. 节奏结构

（请填写这项总体设计。）

## 11. 主题、价值观与长期问题

（请填写这项总体设计。）

## 12. 当前设计最强点与最弱点

（请填写这项总体设计。）

# 未来100章大型剧情块

（先写具体事件链，再写叙事功能。）

# 未来十章逐章小纲

（每章请使用八个字段写出可执行的小纲。）

# 当前状态、未兑现承诺与作者备注

当前状态：

未兑现承诺：

作者备注：

## 选中的 Reference Programs

Reference Program 1
program_id: rcv0-24-reputation-research-training
story_phase: Major Arc Transition / reputation becomes institutional capital
input_state: Repeated clinical successes have created reputation, but the protagonist's methods must be tested, taught, researched, and negotiated across institutions.
central_pressure: The protagonist must convert private practice into reproducible capability without losing time, trust, or control of credit.
reusable_program: Repeated proof -> network recognition -> institutional negotiation -> deliberate training -> harder test.
applicable_conditions: A serial protagonist's competence can become social or academic capital.；Mid-story escalation should change the institution around the protagonist.
failure_modes: Turning every success into automatic status without credit conflict.；Letting training replace real uncertainty rather than prepare for it.
anti_repetition_notes: A reputation payoff must create a new gate or negotiation, not only praise.；Training has value only if a later real-world uncertainty tests it.
output_state: The protagonist has institutional capital and a team whose future depends on how credit and capability are shared.

## GBrain Inspiration Results（作者可编辑原文）

[0.8547] arcs/rcv0-23-xianxia-jiantu-zhi-lu-arc-v1-03 -- ## Local Creative Problem

如何让一个看似无欲望的成年人拥有足以启动长篇的具体欲望。

## Setup

职业、婚姻和日常生活都趋于平淡，但剑术距离感给出可测量天赋。

#
[0.8357] book-dna/rcv0-03-dushi-xiuzhen-chatianqun -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

普通都市生活被一个可交流、可求助、可行动的修真社群接口打穿；读者持续获
[0.8223] book-dna/rcv0-20-gaowu-quanqiu-gaowu -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者先享受重生带来的资源套利、制度误读和武科竞争，再追逐个人战力、身份
[0.8064] arcs/rcv0-26-qihuan-tianqi-yubao-arc-v1-03 -- ## Local Creative Problem

如何把一个现实中的职业错配转成具有情感历史的超自然入口。

## Setup

主角有技能却只想找兼职，市场按外形和岗位需求而非真正能力判断他。

[0.7933] book-dna/rcv0-02-xianxia-bailian-chengxian -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

资质普通甚至受限的修士，通过勤修、资源、准备和危险路径持续获得可验证的
[0.7832] prose-controls/action/action-before-interpretation -- # Action Before Interpretation

## 支持范围

- 支持书本数：16+
- 支持类别：玄幻、仙侠、科幻、奇幻、武侠、历史、高武、灵异、游戏、其他
- 证据卡：
  `
[0.7732] syntheses/categories/synth-category-03 -- ## Evidence Scope

MULTI_BOOK；3 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.7616] book-dna/rcv0-14-wuxia-langzi-jianghu -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者追逐一个有能力、受欢迎又不愿被随意支配的江湖人物，看他在名望、关系
[0.7517] syntheses/categories/synth-category-02 -- ## Evidence Scope

MULTI_BOOK；3 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.7425] arcs/arc-personal-wish-to-historical-scale-v1 -- ## Local Creative Problem

宏大历史和文明危机扩展后，如何不让具体的日常愿望被叙事抛弃。

## Setup

主角从普通人的冒险、家业或陪伴愿望出发。

## Promis
[0.7324] book-dna/rcv0-13-wuxia-jinyong-shijie-daoshi -- ## Evidence Coverage

OPENING；EARLY；MID；LATE；END

## Reader Promise

读者先享受隐居日常与轻易能力，再期待好奇、调查和声望把主角带入
[0.7228] maps/progression-and-breakthrough -- # 进阶与突破

这是导航层，不是 authority taxonomy，也不是创作 Hard Gate。

## 可检索卡片

- `rcv0-01-xuanhuan-wangu-shendi-dn
[0.7138] book-dna/rcv0-19-gaowu-wozai-jingshenbingyuan-xue-zhanshen -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者先从公共日常对异常人的误读中获得轻微喜剧和悬念，再追逐能力系统、团
[0.7052] syntheses/categories/synth-category-01 -- ## Evidence Scope

MULTI_BOOK；3 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪连接。

[0.6951] arcs/rcv0-24-dushi-shoushu-zhibojian-arc-v1-03 -- ## Local Creative Problem

如何让系统赠予的第一次奇迹转成主角自己的职业能力。

## Setup

限时峰值直接完成高难手术，主角身体不完全由自己控制。

## Promi
[0.6868] book-dna/rcv0-16-youxi-hupozhijian -- ## Evidence Coverage

OPENING；EARLY；MID；LATE

## Reader Promise

读者追逐一个普通人的训练、探索和战斗本能如何打开更大的奇幻世界；能力提
[0.6787] prose-dna/rcv0-03-dushi-xiuzhen-chatianqun -- # Prose DNA

仅保存中文 prose 执行观察与来源定位；不保存来源正文。

## Sampling

- coverage mode: `SCENE_FUNCTION_WINDOWS`

[0.6698] syntheses/categories/synth-category-07 -- ## Evidence Scope

PILOT_TWO_BOOK；2 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪
[0.6628] syntheses/categories/synth-category-10 -- ## Evidence Scope

PILOT_TWO_BOOK；2 本来源。

## Shared Tendencies

样本都保留可识别的阶段推进和回报窗口。；世界扩大与角色目标之间存在可追踪
[0.6551] prose-dna/rcv0-20-gaowu-quanqiu-gaowu -- # Prose DNA

仅保存中文 prose 执行观察与来源定位；不保存来源正文。

## Sampling

- coverage mode: `SCENE_FUNCTION_WINDOWS`

```
- 第 1—10 章从权限被收走、三城急单、夜班节点、异常损耗、提前结算、赔掉利润、合同谈判、公开证明到固定夜班窗口形成连续因果链；每章有具体人物、行动、反应、结果和下一章起点，不是十个任务名词。但没有把这份计划伪装成已写成的十章正文。

### D. Chapter continuity

- 第 1 章：初章无前文，适用性通过；页面 Prompt 的前文输入为 0，符合起点。
- 第 2 章：失败。页面章节编号显示 2，但自动读取框长度始终为 0；直接 API 对第 1 章返回 HTTP 200 和 2957 字符，说明保存源存在而页面连续性监听没有读取它。已停止，未用 API 内容手工填入。
- 第 3 章：未执行。

### E. Scene realization

- 第 1 章：通过。八字段均在场景中发生：22:40 调度室权限撤回；马立群、苏岚、韩放各自推动现场；贺准拒签空白赔付单、查个人返程记录并打电话；系统账号锁定、车辆表返回、第一城可进/第二城无预约的环境反应实际出现；直接结果是第一段有入口但必须寻找夜班节点，payoff 已落地，章末未完成目标保留。
- 第 2—3 章：未执行，不补判。

### F. Prose

- 第 1 章：通过（单章证据）。正文名词具体到排班栏、赔付单、交接栏、冷库风机、车辆表和仓库记录；动词写出拖、推、停、翻、拨、筛和画线；对话改变责任、信息和下一步；句段在高压对话与低压查表之间有变化；推理直接导致从车辆表转向夜班节点；说明绑定当前行动；payoff 没有三重解释。单章没有足够证据证明长期无模板重复，因此长期项保持未充分验证。
- 第 2—3 章：未执行。

### 实验结论

- 结论：FAIL / STOPPED_AT_CHAPTER_2_CONTINUITY_FAILURE。当前系统能在完全不同于上一轮的现实职业题材上生成具体 Idea、完整 100 章 BOOK、连续十章计划，并真实完成第 1 章的 A→B→C 场景化正文；但在保存第 1 章后，正常页面流程无法把它自动读入第 2 章，因此不能声称“前三章连续、具体、自然”已经成立。
- 失败是否包装为成功：否。
- 是否修改系统：否。
- 是否人工修改正式正文：否。
- 是否中途停止：是，停止在第 2 章 continuity 层。
- 可提交实验内容：只包含本目录下的输入、Prompt、原始输出、中间稿、已保存第 1 章、审计和失败证据；没有后续伪造内容。
