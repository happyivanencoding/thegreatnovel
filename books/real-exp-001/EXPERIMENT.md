# real-exp-001 真实重跑记录

## 基本信息

- 实验书：real-exp-001
- 目标分支：agent/cleanroom-gbrain-story-mvp
- 本次目的：修复远程工作区、BOOK时间线、章节保存合同，并重新生成第1—3章
- 本次 SUBAGENT_MODE：actual
- 本次没有开始第4章

## 上一轮记录状态

- 上一轮本地实际存在 PROMPTS.md 和 PROPOSAL.md，但没有进入远程 Git；本次将它们作为实际文件加入审计历史。
- 上一轮实际使用的 GBrain query：上一轮未保留。
- 上一轮实际 GBrain 返回：上一轮未保留。
- 上一轮实际选择的 Reference Program IDs：上一轮未保留。
- 上一轮逐章完整 Prompt：上一轮未保留。
- 上一轮远程第1—3章是旧的 canonical Experiment A；本次以新的 A→B→C 正文替换，未把上一轮修订稿冒充为已保存文件。

## 本次真实 GBrain

### Query

主角成长型虚构世界男频长篇；失效、残缺或被删改的术式作为非对称优势。寻找 Reader Promise、Advantage / Special Capability、Repeatable Reader Loop、Core Progression Grammar、Action-Space Expansion、World Expansion Grammar、Narrative Drive、Phase Transition、Failure / Fatigue Risks、Book DNA、Mechanism、Contrast 与 Reference Program。重点关注第一次能力质变、把能力转化为现实收益、战斗或高压验证、身份入口和避免重复；不要预设学院、宗门、战斗或固定成长链。

### GBrain 实际返回

    [0.9061] book-dna/rcv0-02-xianxia-bailian-chengxian -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE
    ## Reader Promise
    资质普通甚至受限的修士，通过勤修、资源、准备和危险路径持续获得可验证的

    [0.8927] book-dna/rcv0-03-dushi-xiuzhen-chatianqun -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE
    ## Reader Promise
    普通都市生活被一个可交流、可求助、可行动的修真社群接口打穿；读者持续获

    [0.8804] book-dna/rcv0-16-youxi-hupozhijian -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE
    ## Reader Promise
    读者追逐一个普通人的训练、探索和战斗本能如何打开更大的奇幻世界；能力提

    [0.8669] book-dna/rcv0-14-wuxia-langzi-jianghu -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE
    ## Reader Promise
    读者追逐一个有能力、受欢迎又不愿被随意支配的江湖人物，看他在名望、关系

    [0.8556] book-dna/rcv0-08-kehuan-kongsuxinghen -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE；END
    ## Reader Promise
    读者先获得阶层差异下的个人能力快感，再看到能力被测量、争夺、组

    [0.8445] book-dna/rcv0-20-gaowu-quanqiu-gaowu -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE
    ## Reader Promise
    读者先享受重生带来的资源套利、制度误读和武科竞争，再追逐个人战力、身份

    [0.8336] arcs/rcv0-23-xianxia-jiantu-zhi-lu-arc-v1-03 -- ## Local Creative Problem
    如何让一个看似无欲望的成年人拥有足以启动长篇的具体欲望。
    ## Setup
    职业、婚姻和日常生活都趋于平淡，但剑术距离感给出可测量天赋。

    [0.8229] book-dna/rcv0-04-kehuan-taxing -- ## Evidence Coverage
    OPENING；EARLY；MID；LATE
    ## Reader Promise
    从灾难中的资源匮乏和低位生存出发，主角通过能力验证、制度准入、联盟和探

以上文本是本次 CLI stdout 原样保留的实际返回片段，没有后台过滤或补写。

## 本次实际 Reference Programs

本次实际选择并送入章节 Prompt 的 IDs：

- rcv0-02-foundation-bottleneck
- rcv0-02-opening-bottleneck
- rcv0-24-public-proof-rescue-loop

它们均来自当前本地 reference-corpus-program-deep-v1/reference-programs 中 status 为 VALIDATED 的文件。

## 本次实际 Chapter Prompt

章节模板使用当前 PROMPTS.md 中的“# 当前章节写作”模板；该模板来自当前生产 DEFAULT_PROMPT_TEMPLATES["chapter"]，并包含：

- 前两章完整正文；
- 最近摘要；
- 当前大型剧情块；
- 当前十章计划；
- 当前章八字段小纲；
- 当前 BOOK 执行画像；
- 本次 GBrain Results；
- 上述三个 Reference Program。

最终返回合同实际使用以下标题：

    # Writer Audit
    # 正式正文
    # 章节事实摘要

第1—3章分别使用了当前 BOOK 第1—15章大型块和对应八字段小纲；第2章注入第1章 C 正文，第3章注入第1—2章 C 正文。

第一轮本次重跑的 A→B→C 消息没有把本次 GBrain/Reference 文本显式注入子代理，因此没有把第一轮正文作为最终审计正文。随后执行了 provenance correction pass；修正 pass 的每个 A/B/C 消息都明确要求读取并使用本文件中的真实 GBrain 返回和三个 Reference IDs。

## 本次实际串行 Subagent

### 第1章

- Writer A：01a01630-2197-7411-a56b-45bec8e2c03e
- Writer B：01a0163b-1a40-7a33-85c2-5cf2542c8871
- Writer C：01a0163d-58e7-7701-b9e4-aa595d14a4a3

### 第2—3章（第一轮）

第2—3章由同一个实际 subagent task 串行执行多个 A→B→C pass：

- 01a01642-42da-7741-b798-37fb312650b7

没有并行调用，没有伪造 task ID。

### Provenance correction pass

本次最终写入正文的是以下 correction pass：

- 第1章 A→B→C：实际 task 01a01653-fb51-7840-888e-f97ffdabbc5e，通过连续 send_input 执行三个串行 pass。
- 第2—3章 A→B→C：实际 task 01a01642-42da-7741-b798-37fb312650b7，通过连续 send_input 执行六个串行 pass。
- 每个 correction pass 都明确读取本文件中的 GBrain Results 和 Reference IDs。
- SUBAGENT_MODE：actual。

## 正式正文字符数

计数口径：最终 chapter-NNNN.md 文件的 Unicode 字符数，包含章节标题和段落换行，不包含审计信息与事实摘要。

| 文件 | 字符数 |
|---|---:|
| chapter-0001.md | 2483 |
| chapter-0002.md | 2205 |
| chapter-0003.md | 2626 |

## 从 Codex 返回到章节文件

最终 correction pass 的 C 返回包含 Writer Audit、正式正文和事实摘要。父代理只提取“# 正式正文”区块，将其作为正式章节内容；Writer Audit 和事实摘要没有写入 chapter-NNNN.md。

由于原有第1—3章文件已经存在，当前 save_chapter() 的防覆盖行为不会被绕过。本次是作者明确要求的实验修订，使用显式人工文件替换更新三份 canonical 正文；没有增加 overwrite、版本或 revision 机制。

页面合同修复同时已加入：Codex 返回文本保留在页面；作者点击“提取正式正文”后，只有单独的正式正文 textarea 会进入现有章节保存 API；事实摘要单独显示且不会写盘。
