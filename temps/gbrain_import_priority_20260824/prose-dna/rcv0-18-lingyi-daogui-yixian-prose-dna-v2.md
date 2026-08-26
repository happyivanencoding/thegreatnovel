---
schema_version: reference-corpus-card-v1
card_type: prose-dna
knowledge_level: BOOK_OBSERVATION
status: REFERENCE_ONLY
source_book_ids:
- rcv0-18-lingyi-daogui-yixian
evidence_refs:
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-001
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-0001
  line_start: 6
  line_end: 29
  observation_summary: 开场以重复劳动和异常环境建立低温基调，突发冲突用单个物件动作打破静态，随后立刻插入自我压制。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-002
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-0002
  line_start: 76
  line_end: 99
  observation_summary: 现实场景用临床问答对照幻觉叙述，医生的平静与患者的疑问形成双层距离，信息以纠正和回避推进。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-003
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-0100
  line_start: 5864
  line_end: 5887
  observation_summary: 日常劳作写得具体而克制，生活细节后接冷峻判断，短暂平静同时埋下不安全感。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-004
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-0400
  line_start: 24053
  line_end: 24076
  observation_summary: 恐怖动作按群体争论、尖叫、追逐、物件试验和局部规则确认推进，身体变形与声音共同制造节奏。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-005
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-0700
  line_start: 40378
  line_end: 40401
  observation_summary: 极端感知被拆成连续短句和身体后果，外部异响与主观认知互相改写，情绪高点不靠总结。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-006
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-0900
  line_start: 51490
  line_end: 51513
  observation_summary: 死亡余波以克制的对话、尸体触感和命令冲突处理，悲伤被迫压回继续上路的动作选择。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-007
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-1000
  line_start: 56633
  line_end: 56656
  observation_summary: 后段战斗把抽象力量写成可见的破坏和连续挥击，规则说明紧随结果，宏大尺度由动作逐层推高。
- evidence_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-008
  source_book_id: rcv0-18-lingyi-daogui-yixian
  source_id: book-01-ea099238
  distill_id: distill_4f0a2c0d9691803bb89e7f46
  segment_id: segment-1045
  line_start: 59573
  line_end: 59606
  observation_summary: 当前末段以计划出现偏差、交易式对话和新的天灾提示收尾，认知悬念强，未形成完整ENDING。
creative_problem_tags:
- prose-realization
- sentence-rhythm
- paragraph-rhythm
- dialogue-prose
- action-prose
- payoff-prose
- exposition-prose
- emotion-prose
reader_experiences: []
narrative_drives: []
payoff_channels: []
evidence_scope: SINGLE_BOOK
maturity: PILOT
category_ids:
- 灵异
depends_on:
- rcv0-18-lingyi-daogui-yixian-reference
source_book_id: rcv0-18-lingyi-daogui-yixian
title: 道诡异仙
category: 灵异
sampling_strategy: 按开篇现实与异象、早期日常、中段身体与关系压力、后段高位冲突、当前末段，依据 index 起止行选取 8 个功能窗口；末段作为 LATE 而非完整结尾。
coverage_mode: SCENE_FUNCTION_WINDOWS
sample_window_count: 8
scene_functions:
- OPENING
- DIALOGUE
- ORDINARY
- ACTION
- EMOTION
- AFTERMATH
- LATE
card_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v2
active_inspiration: false
prose_dna_schema: selection-prose-dna-v2
derived_from_card_id: rcv0-18-lingyi-daogui-yixian-prose-dna-v1
source_style_leakage_check: PASS
transfer_boundary: 只迁移词汇选择、句法功能、段落节奏、细节选择、叙述距离、对白功能、动作可视化、信息时序和回报落点；不迁移人物、事件、专名、原句、口癖或签名比喻。
---

# 道诡异仙 Selection Prose DNA v2

## Evidence Basis

本卡只重组旧卡已有的 `evidence_refs`、`scene_functions`、窗口摘要与 prose observations；未重新读取原著，未新增 locator。

| Evidence ID | Window / Scene Function | Locator | 已有 Evidence Summary |
|---|---|---|---|
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-001` | `rcv0-18-w01` / `OPENING` | `segment-0001:6-29` | 重复劳动与异常环境建立低温基调；单个物件动作打破静态，随后插入自我压制。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-002` | `rcv0-18-w02` / `DIALOGUE` | `segment-0002:76-99` | 临床问答对照幻觉叙述；医生平静、患者疑问形成双层距离；信息通过纠正与回避推进。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-003` | `rcv0-18-w03` / `ORDINARY` | `segment-0100:5864-5887` | 日常劳作具体而克制；生活细节后接冷峻判断；平静中埋下不安全感。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-004` | `rcv0-18-w04` / `ACTION` | `segment-0400:24053-24076` | 群体争论、尖叫、追逐、物件试验与局部规则确认推进恐怖动作；身体变形与声音共同制造节奏。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-005` | `rcv0-18-w05` / `EMOTION` | `segment-0700:40378-40401` | 极端感知拆成连续短句与身体后果；外部异响与主观认知互相改写；情绪高点不靠总结。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-006` | `rcv0-18-w06` / `AFTERMATH` | `segment-0900:51490-51513` | 死亡余波由克制对白、尸体触感与命令冲突处理；悲伤被压回继续上路的动作选择。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-007` | `rcv0-18-w07` / `LATE` | `segment-1000:56633-56656` | 抽象力量转为可见破坏与连续挥击；规则说明紧随结果；宏大尺度由动作逐层推高。 |
| `rcv0-18-lingyi-daogui-yixian-prose-dna-v1-ev-008` | `rcv0-18-w08` / `LATE` | `segment-1045:59573-59606` | 计划偏差、交易式对话与新的天灾提示收尾；认知悬念增强，未形成完整结尾。 |

## Cross-Scene Invariants

1. 文本带宽主要投向会改变感知、身体、行动选择、关系压力或尺度的状态变化；重复劳作与短暂平静承担基线和反差功能。  
   支持：`W01`、`W03`、`W04`、`W05`、`W06`、`W07`、`W08`。

2. 抽象认知通常先由身体、材质、声音、空间、物件或可见结果承载，再进入局部判断或概念说明。  
   支持：`W01`、`W04`、`W05`、`W07`。

3. 因果解释倾向停在“当前结果如何改变理解或下一步行动”的粒度；完整规则、终极真相和全部收束可以保留空缺。  
   支持：`W02`、`W04`、`W07`、`W08`。

4. 人物状态和关系压力更多通过动作、身体后果、对白、命令、物件处置与继续执行任务泄露；高点之后常回到可执行动作。  
   支持：`W01`、`W02`、`W04`、`W05`、`W06`、`W08`。

## Attention DNA

### Core Selection Strategy

选择性放大“状态发生变化”的瞬间，而不是平均铺开所有场面。值得获得带宽的细节通常满足至少一种功能：改变人物下一步选择、让感知失稳可见、让抽象力量产生可见后果、改变人物关系压力，或把场面尺度逐层推高。

静态劳动、日常和平临床问答可以保持具体但克制；突发侵犯、身体异变、死亡余波、计划偏差和新灾难提示则获得更高的感知与行动带宽。

### Scene-Conditioned Behavior

- `OPENING / ORDINARY`：压缩重复劳动，保留异常环境、单个物件动作和随后出现的冷峻判断，让平静成为后续破裂的参照。
- `ACTION / EMOTION`：把带宽给身体、声音、追逐、试验、连续动作和感知互相改写的过程。
- `AFTERMATH`：重点不是泛化悲伤，而是尸体触感、克制对白、命令冲突以及人物如何被迫继续执行任务。
- `LATE`：通过连续破坏、挥击、交易和计划偏差逐步提升尺度；结尾优先保留新的不稳定状态，而不是补齐解释。

### Compression / Omission Boundary

可以压缩重复劳动、稳定环境、已知行动背景和不改变下一步选择的生活细节。

不应为了制造“完整感”而补写情绪总结、宇宙全景解释、完整规则系统或已经未确认的结局。局部状态变化已经清楚时，继续解释可能削弱悬念和行动压力。

### Evidence / Anti-Evidence

证据：`ev-001`、`ev-003`、`ev-004`、`ev-005`、`ev-006`、`ev-007`、`ev-008`。

反证与不足：旧卡没有证明所有异常都应获得同等带宽，也没有证明全书存在稳定的场面强度比例；八个窗口不足以推导固定的注意力分配公式。

## Knowledge DNA

### Core Selection Strategy

让读者共享当前局部感知，同时保留一个可能进行校正的外部观察层。信息可以推进到当前行动所需的结果、局部判断或暂时可用规则，但不自动升级为完整世界答案。

### Scene-Conditioned Behavior

- `DIALOGUE`：通过临床式问答、平静纠正、患者疑问和回避，让不同认知位置同时存在。
- `ACTION`：通过物件试验、身体后果和局部规则确认提供可用知识；先让结果出现，再让判断跟进。
- `EMOTION`：允许外部异响与主观认知互相改写，不急于替读者裁决哪一层是真实。
- `LATE`：计划偏差、交易和天灾提示可以提高认知悬念，但只揭示当前新状态，不强行完成谜团。

### Compression / Omission Boundary

解释到“人物现在需要知道什么、因此能做什么”即可停止。可以省略完整机制、终极动机、全部规则来源和最终真相。

当场景行动必须依赖某条规则时，旧卡没有支持继续制造规则空白；此时应保留行动所需的局部清晰度。

### Evidence / Anti-Evidence

证据：`ev-002`、`ev-004`、`ev-005`、`ev-007`、`ev-008`；对应 `W02`、`W04`、`W05`、`W07`、`W08`。

反证与不足：旧卡只能支持局部知识与解释边界，不能判断全书固定的叙述者知识范围、解释频率或所有超自然规则的揭示顺序。

## Causal DNA

### Core Selection Strategy

因果链优先落在可观察的“对象或身体发生了什么—结果改变了什么—人物因此如何判断或行动”。抽象规则可以跟随结果出现，但应停在当前场景真正改变的部分。

### Scene-Conditioned Behavior

- `OPENING / ORDINARY`：用物件动作打破劳动基线，再接自我压制或冷峻判断，形成局部因果铰链。
- `ACTION`：让争论、尖叫、追逐、物件试验和规则确认互相推动；不可理解不等于不可读，至少要保留感官后果与下一动作。
- `LATE`：先写可见破坏和连续挥击，再让规则说明解释结果；宏大尺度由连续因果动作逐层累积。
- `AFTERMATH`：尸体触感、命令冲突和继续上路共同说明悲伤为何没有停留在内心总结。
- `LATE / 收尾`：把计划偏差与交易作为当前因果转折，把天灾提示作为新的未决压力。

### Compression / Omission Boundary

解释到当前结果如何改变行动、判断或局部关系即可停止。可以省略完整宇宙机制、全部因果来源和最终意义，但不能省略支撑下一动作的感官结果或局部规则。

### Evidence / Anti-Evidence

证据：`ev-001`、`ev-004`、`ev-006`、`ev-007`、`ev-008`。

反证与不足：旧卡支持“结果后接局部说明”，但没有提供足够证据判断所有类型场景都采用相同的因果顺序，也没有提供固定解释长度。

## Reaction DNA

### Core Selection Strategy

人物状态通过动作、身体后果、对白、停顿、物件处置、命令冲突和继续执行任务泄露。情绪高点不依赖作者替人物总结；压抑、怀疑、否认和重估应在感知或选择改变时显现。

### Scene-Conditioned Behavior

- `OPENING`：突发物件动作之后出现自我压制，状态变化表现为立即控制，而非情绪说明。
- `DIALOGUE`：医生的平静、患者的追问、纠正与回避共同暴露认知距离。
- `ACTION`：争论、尖叫、追逐和试验把恐惧、协作与判断压力外化。
- `EMOTION`：用连续身体后果和感知变化承载极端状态，不在峰值处追加概括性情绪结论。
- `AFTERMATH`：用尸体触感、克制对白、命令冲突和继续上路表现悲伤被压回行动。
- `LATE`：交易式对白和计划偏差泄露人物对局势的新估计。

### Compression / Omission Boundary

可删去不增加行动、关系或感知信息的情绪标签和事后总结。不要把所有心理转折都改写成动作；旧卡只支持在关键状态变化处让内心转折落到感知或行动。

### Evidence / Anti-Evidence

证据：`ev-001`、`ev-002`、`ev-004`、`ev-005`、`ev-006`、`ev-008`。

反证与不足：旧卡支持多种反应通道，但不足以推导固定人物声线、固定口头习惯或所有角色的一致反应模式。

## Rhythm DNA

### Core Selection Strategy

句段节奏随 scene beat 改变：静态与临床问答偏短、冷静；异变、追逐和极端感知阶段由连续动词、断裂短句、声音和身体后果加压；解释段可以暂时恢复连贯；高潮后迅速回到任务、命令或下一选择。

### Scene-Conditioned Behavior

- `ORDINARY / DIALOGUE`：维持短促、冷静、可辨认的交换，避免无状态变化的持续加压。
- `ACTION / EMOTION`：随着侵犯、追逐、身体变化和认知失稳缩短或断裂句段，使读者感到 beat 的推进。
- `解释 / 规则确认`：允许句段拉长，但解释块可以被新结果或动作打断。
- `AFTERMATH`：高点之后迅速回到命令、旅途或继续执行的动作。
- `LATE`：战斗通过连续挥击逐步推高；收尾则在计划偏差、交易或灾难提示处悬停，不强行恢复完整闭合。

### Compression / Omission Boundary

不要把所有段落都写成短句、高声量或断裂状态。节奏变化必须服务于状态变化；没有新 beat 时，应压缩或恢复连贯。

### Evidence / Anti-Evidence

证据：`ev-001`、`ev-002`、`ev-004`、`ev-005`、`ev-006`、`ev-007`、`ev-008`。

反证与不足：旧卡没有提供句长阈值、段落长度比例或标点频率；标点只能作为呼吸、疼痛或认知卡顿的局部选择，不能转化为硬模板。

## Lexical DNA

### Core Selection Strategy

词语选择服从场景功能，而不是形成固定词表。具体身体、材质、声音、空间、劳动和物件名词承载抽象问题；测试、追逐、破坏、挥击、继续等动作动词承载因果推进；判断句则负责给当前结果定性。

对白中，日常粗粝语域、临床或制度语域、仪式感语域与抽象语域的并置，会制造认知距离和不安。

### Scene-Conditioned Behavior

- `OPENING / ORDINARY`：优先选择劳动、环境和物件相关的具体名词，再接克制或冷峻判断。
- `ACTION / EMOTION`：优先让身体、材质、声音、空间与连续动作承担恐怖和认知变化。
- `DIALOGUE / AFTERMATH`：根据关系压力选择纠正、质问、命令、平静陈述或交易式表达。
- `LATE`：让可见破坏和连续动作先承载尺度，抽象词只在结果需要判断时进入。

### Compression / Omission Boundary

选择少量具有身份、因果、身体感或尺度功能的感官锚点，避免连续堆叠同类描述。概念词不应替代已经可以承担因果的物质或动作细节。

不迁移来源专名、人物口癖、签名比喻或原句；本维度不构造禁词表。

### Evidence / Anti-Evidence

证据：`ev-001`、`ev-002`、`ev-004`、`ev-005`、`ev-006`、`ev-007`、`ev-008`。

反证与不足：旧卡没有词频、词类比例或跨全书词汇统计，因此不能推出固定高频词、固定句式或固定语域切换次数。

## Detail Selection Across Dimensions

| 候选细节 | 为什么值得进入文本 | 删除后的损失 | 证据 |
|---|---|---|---|
| 重复劳动、日常物件、异常环境 | 建立平静基线，并让后续侵犯具有反差 | 身份感、状态反差与不安全感 | `W01`、`W03` |
| 身体后果、材质、声音、空间 | 把抽象认知或力量转为可感知结果 | 身体感、因果可读性与局部尺度 | `W04`、`W05`、`W07` |
| 物件试验与局部结果 | 让人物通过行动获得有限但可用的判断 | 行动因果、规则确认与下一步选择 | `W04`、`W07` |
| 纠正、质问、命令、交易对白 | 显示认知位置、关系压力和立场变化 | 关系信息、现实校正与选择压力 | `W02`、`W06`、`W08` |
| 尸体触感与继续执行任务 | 让死亡余波同时保留身体事实和行动约束 | 身体感、情绪压抑与 payoff 后的推进 | `W06` |
| 计划偏差、灾难提示、未决选择 | 使收尾产生新的不稳定状态 | 认知悬念、后续行动压力与未完成 payoff | `W08`；尺度递进另见 `W07` |

删除判断应围绕细节是否承担身份、因果、关系、身体感、尺度或局部 payoff；仅重复已有信息、未改变感知或行动的细节可压缩。该判断仍需服从当前 scene beat 与作者显式意图。

## Production Implications

- Curator 可先标注当前场景的主要 state change，再从静态基线、物质异常、身体后果、关系对白或尺度动作中选择一个主要带宽目标。
- Curator 可对需要保持可读的诡异场面优先编译“具体结果＋下一动作＋局部判断”；只有当前行动需要时才增加规则解释。
- Curator 可对人物状态优先选择与当前关系或任务直接相连的动作、对白、停顿、物件处置或命令冲突作为泄露通道。
- Curator 可根据 beat 选择节奏模式：静态/校正时保持冷静连贯，侵犯/异变时加压，解释时暂时恢复，高潮后回到可执行动作。
- Curator 可对高位或抽象内容先选择可见破坏、声音、身体或空间作为尺度支点，再决定是否加入概念判断。
- Curator 可对收尾场景优先编译新的计划偏差、未决交易、灾难提示或认知变化；若当前证据不足，不替场景补写完整结局。

## Limits / Insufficient Evidence

- 本卡只有单一来源书、8 个 scene-function windows，不能代表全书所有阶段或所有场景类型。
- `W07` 与 `W08` 属于 `LATE`；`W08` 只是当前文本末段，不是可确认的大结局，`ENDING` 仍为 `UNKNOWN`。
- 旧卡不足以确定超自然规则在全书中的稳定解释频率、解释长度或揭示顺序。
- 旧卡不足以推出固定句长、段落长度、标点比例、词频、词类比例或对白占比。
- 旧卡不足以把任何人物反应、语域、事件结构或专名转化为通用规则。
- 局部 payoff 支持“旧理解被改写”或“行动角度变化”，但不足以外推全书的最终收束方式。
- 本卡不包含原文句式、原文 locator 之外的新证据，也不构成 Writer hard gate。
