# real-exp-002 Browser Workflow Audit

## 页面/事件 1 · 预注册与工作区核对

- 时间：2026-08-18T23:35:23+02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=UNKNOWN；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：读取页面 DOM、确认新建入口、默认 Prompt 模板入口、GBrain 查询入口、Reference Programs 区域和章节保存入口
- 输入：实验方向尚未发送；未调用 GBrain；未生成 Idea
- 页面可见结果：小说工作区为 C:\dev\tgn-story-mvp\books；新建小说按钮可用；已有旧书列表可见；GBrain 状态为“未查询”；Reference 区域初始为 0 / 3
- 机器输出：冻结应用首页 HTTP 200；当前页面标题与 URL 已读取
- 一致性判断：通过。此时未产生 real-exp-002 内容输出，符合 cleanroom 起点
- 调试/下一动作：先通过页面创建 real-exp-002，再恢复本实验预注册文件，随后才允许输入方向和调用 GBrain

## 页面/事件 2 · 正常新建小说

- 时间：2026-08-18T23:35:23+02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：在“小说 ID”输入 `real-exp-002`，点击“新建小说”，重新读取页面 DOM
- 输入：`real-exp-002`
- 页面可见结果：状态为“已创建并加载 real-exp-002”；书籍列表选中 real-exp-002；BOOK 编辑区为默认空白画像；GBrain 状态仍为“未查询”；章节列表为空
- 机器输出：`books/real-exp-002/BOOK.md`、`PROMPTS.md`、`PROPOSAL.md` 与 `chapters/` 由应用创建
- 一致性判断：通过。新书由当前应用正常新建流程创建，未复制旧实验
- 调试/下一动作：恢复预注册的 `EXPERIMENT.md`，然后开始输入唯一宽方向

## 页面/事件 3 · 预注册文件恢复

- 时间：2026-08-18T23:35:23+02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：将首次生成前已创建的同一 `EXPERIMENT.md` 放回应用创建的书目录
- 输入：冻结 commit、实验问题、A—F 预注册标准和 provenance 空位；没有新增创作内容
- 页面可见结果：页面仍加载 real-exp-002，GBrain 仍为“未查询”
- 机器输出：`books/real-exp-002/EXPERIMENT.md` 已恢复；其余应用生成文件未改动
- 一致性判断：通过。预注册内容在第一次 GBrain/Idea 之前存在于目标书目录；恢复动作没有改变其文本
- 调试/下一动作：在页面输入完整宽方向，生成并保存当前默认 GBrain query

## 页面/事件 4 · 宽方向与默认 query

- 时间：2026-08-18T23:35:50+02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：填写“创作方向 / 想保留的成长链或元素”，点击“生成默认查询”，读取 query 文本
- 输入：用户给出的现代都市职业成长方向与现实世界/非超自然/职业成长边界；没有增加主角、职业、金手指、关系或剧情设计
- 页面可见结果：GBrain 状态仍为“未查询”；默认 query 已填入；Reference 计数为 0 / 3
- 机器输出：实际 query 已原样写入 `EXPERIMENT.md`
- 一致性判断：通过。query 来自当前页面默认模板；尚未调用 GBrain 或生成 Idea
- 调试/下一动作：保存 query 后，点击当前页面的“从 GBrain 取灵感”，并原样保留返回文本

## 页面/事件 5 · 真实 GBrain 查询

- 时间：2026-08-18T23:36（Europe/Paris；页面返回精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：点击“从 GBrain 取灵感”，等待页面完成 CLI 请求，读取 GBrain Inspiration Results 文本
- 输入：`EXPERIMENT.md` 中记录的实际默认 query
- 页面可见结果：GBrain 状态为“可用”；页面提示“GBrain 灵感已返回，可删改后进入 Prompt”；Reference 仍为 0 / 3
- 机器输出：返回文本字符数 3099；原始 stdout 已写入 `EXPERIMENT.md`
- 一致性判断：通过。GBrain 真实调用成功，结果未被筛选或改写；内容含多种都市/职业及非目标旧语境卡片，作为系统当前检索结果保留
- 调试/下一动作：只从页面可见的 VALIDATED Reference Programs 中选择最多 3 个与现实职业成长方向真正相关的程序

## 审计补充 5a · GBrain raw provenance 转录校正

- 时间：2026-08-18T23:36（Europe/Paris）
- 具体失败：首次手工落盘时把页面原文 `[0.7052]` 误写成 `[0.7051]`
- 处理：以页面当前真实值为准，仅修正实验记录中的这一字符；没有重跑 GBrain、没有改 query、没有改结果内容
- 结果：页面文本与 `EXPERIMENT.md` 中对应原文重新一致；实验继续

## 页面/事件 6 · Reference 选择

- 时间：2026-08-18T23:37:46+02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：读取页面全部 Reference 卡片后勾选 `rcv0-24-reputation-research-training`
- 输入：选择最多 3 个真正相关的 VALIDATED 程序；本次选择 1 个
- 页面可见结果：Reference 计数为 1 / 3；选中 ID 为 `rcv0-24-reputation-research-training`
- 机器输出：选中卡片字段已记录到 `EXPERIMENT.md`
- 一致性判断：通过但有已知输入偏置。该程序最接近职业能力→机构资本的转换关系，但卡片原文含 clinical 语境；这一偏置由实际 Reference 输入产生，已记录，不将其伪装成中性选择
- 调试/下一动作：生成 Idea Prompt；保留完整 Prompt，不手工增删后发送

## 页面/事件 7 · Idea Prompt 生成

- 时间：2026-08-18T23:38（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：点击“生成男频爽文创意 Prompt”，读取完整 Prompt 文本
- 输入：页面默认 `idea` 模板、宽方向、空 BOOK、GBrain 原样结果、一个实际选中的 Reference
- 页面可见结果：Prompt mode 为 `idea`；页面状态为“Prompt 已生成，可继续编辑后复制”；Prompt 字符数为 `6659`
- 机器输出：完整 Prompt 已原样写入 `EXPERIMENT.md`
- 一致性判断：通过。Prompt 由当前默认模板生成，没有人工改写或额外 Prompt engineering
- 调试/下一动作：把原始 Prompt 交给真实创作模型，保存原始 3—5 个候选；不评分、不排名、不替作者选择

## 页面/事件 9 · Idea 验收与选择

- 时间：2026-08-18T23:40（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：回读原始候选结构，按预注册 A 进行人工判断，选择候选 2
- 输入：`IDEA_RAW.md` 中未修改的 4 个候选
- 页面可见结果：当前页面仍保留 Idea Prompt；选择本身由作者/Agent判断，不由系统评分器代选
- 机器输出：四个候选均含所需 Idea 区块；选择结果与理由已追加到 `EXPERIMENT.md`
- 一致性判断：通过。候选间差异来自证据链、运力节点、规则试点和现金时间表四种不同转换网络，不是只换职业名
- 调试/下一动作：把选中候选原文作为下一步 Outline Prompt 的输入，随后只接受系统生成的 BOOK

## 页面/事件 10 · Outline Prompt

- 时间：2026-08-18T23:41（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：将原始候选 2 连同宽方向填入创作方向字段，切换 Prompt mode 为 `outline`，点击“生成当前 Prompt”，读取完整文本
- 输入：未修改的候选 2 原文、原始宽方向、当前空 BOOK、GBrain 原文、选中 Reference
- 页面可见结果：状态为“Prompt 已生成，可继续编辑后复制”；mode=`outline`；Prompt 字符数为 `10751`
- 机器输出：完整 Prompt 已保存为 `OUTLINE_PROMPT.md`，路径已写入 `EXPERIMENT.md`
- 一致性判断：通过但有 warning。候选文字仍完整进入 Prompt，单行输入导致换行格式丢失；没有人工 Prompt engineering
- 调试/下一动作：用该真实 Outline Prompt 生成完整 BOOK；若 BOOK 出现明显职业/边界/时间线失败，保留原输出并停止，不修 Prompt

## 页面/事件 11 · BOOK Proposal→BOOK 保存

- 时间：2026-08-18T23:44（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：填入 BOOK 原始返回；放入 Proposal 编辑区；保存 Proposal；应用 16 个 BOOK 区域；保存 BOOK
- 输入：未修改的 `BOOK_RAW.md` 原文
- 页面可见结果：Proposal 保存成功；应用报告 16 个区域；BOOK 保存成功；BOOK 编辑区有 5 个剧情块和 10 个逐章小纲
- 机器输出：`PROPOSAL.md`、`BOOK.md` 已落盘；规范化换行后均与 `BOOK_RAW.md` 一致
- 一致性判断：通过。没有人工润色 BOOK，没有正文或 Writer Audit 混入 BOOK
- 调试/下一动作：进入第 1 章，先生成八字段小纲，再生成当前默认 chapter Prompt

## 页面/事件 12 · 第 1 章小纲与 Prompt

- 时间：2026-08-18T23:46（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=1；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：切换 chapter mode，填入第 1—18 章剧情块和八字段小纲，点击“生成当前 Prompt”
- 输入：已保存 BOOK 的第 1—18 章块；第 1 章八字段小纲；前两章正文为空
- 页面可见结果：mode=`chapter`；Prompt 生成成功；小纲字符数 `509`；Prompt 字符数 `17969`；前文输入字符数 `0`
- 机器输出：小纲与完整 Prompt 已分别保存为 `CHAPTER-0001-OUTLINE.md`、`CHAPTER-0001-PROMPT.md`
- 一致性判断：通过。八字段 Hard Gate 通过；第 1 章没有前文，符合初章条件
- 调试/下一动作：严格执行 Writer A→B→C 串行正文流程；不把 audit/摘要写入正文

## 页面/事件 8 · Idea 原始返回

- 时间：2026-08-18T23:39（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：根据页面生成的实际 Idea Prompt 产生 4 个候选，并先保存原始返回
- 输入：未修改的 Idea Prompt；GBrain 和 Reference 原文作为 Prompt 输入
- 页面可见结果：Prompt 文本仍在页面；候选尚未写入 Proposal 或 BOOK
- 机器输出：4 个候选完整文本已写入 `IDEA_RAW.md`；`EXPERIMENT.md` 已记录文件路径
- 一致性判断：待人工验收。候选之间需按预注册 A 标准判断，选择前不修改任何候选
- 调试/下一动作：逐项检查核心优势具体性、行动改变、复利、早期兑现和候选间结构差异，然后选择一个

## 页面/事件 13 · Writer A→B→C 串行执行

- 时间：2026-08-18T23:47—2026-08-19T00:07（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=1；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：真实串行派发 Writer A、等待完成；将 A 交给 Writer B、等待完成；将 B 交给 Writer C、等待完成
- 输入：BOOK、CHAPTER-0001-OUTLINE.md、CHAPTER-0001-PROMPT.md，以及上一阶段完整中间稿
- 机器输出：A agent `01a016de-29b2-73f0-a3ea-e36c19fb5e76` 自报 2697；B agent `01a016e2-825b-7933-a623-8e81c1250c63` 自报 2989；C agent `01a016e7-00f1-73d2-8364-17019b34f745` 自报 2784；三者均返回 `SUBAGENT_MODE: actual`
- 一致性判断：通过。A/B/C 串行，不并行；中间稿分别保存；C 返回严格分离 Audit、正式正文和事实摘要
- 调试/下一动作：把 C raw 返回交给页面“提取正式正文”，再调用正常 chapter save API

## 页面/事件 14 · 第 1 章正文提取与保存

- 时间：2026-08-19T00:08（Europe/Paris；精确秒未单独保留）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=1；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：填入 C 完整返回，点击“提取正式正文”，回读正文/摘要边界，点击“批准并保存章节”
- 页面可见结果：正文首行为“晚上十点四十，调度室最上方的车队排班栏灰了下去。”；正文末行为“今晚还剩下的，不是一辆车，而是一扇必须有人打开、并且愿意留下交接记录的门。”；摘要 142 字符；状态为 `chapter-0001.md 已保存`
- 机器输出：正文页面长度 2957；去换行 2786；`chapters/chapter-0001.md` 已写入
- 一致性判断：通过。磁盘正文与 C raw 正式正文区块规范化换行后一致；没有 Audit/摘要混入
- 调试/下一动作：切换到第 2 章，要求页面真实读取第 1 章

## 页面/事件 15 · 第 2 章 continuity 失败并停止

- 时间：2026-08-19T00:09—00:10（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：http://127.0.0.1:8000/
- 作用域：book_id=real-exp-002；edition_id=UNKNOWN；chapter_id=2；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：章节编号改为 2；依次尝试失焦、点击小纲输入框、ArrowDown→ArrowUp、ControlOrMeta+A 后逐字符输入 2 并失焦；每次重新读取页面状态
- 页面可见结果：数字框为 `2`；`previous-chapter-text` 长度始终为 `0`；第 1 章正文保存区仍为 2957 字符；未生成第 2 章 Prompt
- 机器输出：直接 GET `/api/books/real-exp-002/chapters/1` 为 HTTP 200，返回正文 2957 字符；文件/API存在，页面 continuity 自动读取未发生
- 一致性判断：失败。第 2 章无法在当前正常页面流程中真实读取第 1 章；继续手工填充会违反实验规则
- 调试/下一动作：保留所有已完成 artifact 和原始输出，停止第 2 章及后续；不修改系统、不手工修正文、不生成后续 Prompt

## 审计补充 · 实际执行顺序索引

- 预注册/建书/query/GBrain/Reference/Idea：页面事件 1—9（其中事件 8 的文件位置由追加式 patch 锚点造成显示顺序偏移，内容与真实动作不变）
- Outline/BOOK/第 1 章小纲与 Prompt：页面事件 10—12
- Writer 串行、chapter save、continuity stop：页面事件 13—15
- 该索引不重排既有追加记录，只明确实际动作顺序和事件编号
