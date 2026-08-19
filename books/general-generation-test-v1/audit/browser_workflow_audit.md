# Story MVP 正常产品流程测试审计

- 测试 book：`general-generation-test-v1`
- 项目：`C:\dev\tgn-story-mvp`
- 运行端口：`http://127.0.0.1:8000/`
- 审计模式：只记录和诊断；不自动批准章节，不修改生产代码、Prompt Template、GBrain、Reference Corpus 或正文事实。

## 页面/事件 1 · 初始工作台

- 时间：2026-08-19 09:11 左右 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=UNKNOWN；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：读取初始 DOM、工作区路径、GBrain 状态、Reference Programs 展示和可用按钮。
- 输入：无。
- 页面可见结果：工作区为 `C:\dev\tgn-story-mvp\books`；GBrain 显示“未查询”；查询范围显示“全 Brain”；可新建小说；BOOK 设计、100 章、未来十章、状态、Proposal 编辑区均可见。
- 机器输出：应用页面标题为 `Transparent GBrain Story Studio`；服务为当前 checkout 的 8000 端口；Reference Programs 由页面加载。
- 一致性判断：通过。实际页面是透明协作流程，不是内置自动 LLM 生成流程；后续以该真实边界执行。
- 调试/下一动作：创建不覆盖既有目录的全新测试 book。

## 页面/事件 2 · 新建测试书

- 时间：2026-08-19 09:12:34 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：在“小说 ID”输入 `general-generation-test-v1`，点击“新建小说”。
- 输入：`general-generation-test-v1`。
- 页面可见结果：状态为“已创建并加载 general-generation-test-v1”；已存在小说下拉框选中该 book；默认 BOOK 内容进入编辑区。
- 机器输出：新建接口返回成功；测试目录为 `C:\dev\tgn-story-mvp\books\general-generation-test-v1`。
- 一致性判断：通过。book 创建并加载，尚未写入作者创作方向、Proposal 或自定义 BOOK 内容。
- 调试/下一动作：填写作者唯一的宽泛方向，然后生成实际 GBrain 查询。

## 页面/事件 3 · 作者方向与 Idea 查询

- 时间：2026-08-19 09:13—09:14 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：填写作者唯一宽方向，点击“生成默认查询”。
- 输入：`传统玄幻 / 超凡成长类男频长篇。主角从普通或较弱起点开始，通过自身优势、成长、资源、关系和不断扩大的世界逐渐变强。希望有明确成长感、探索感、阶段性兑现和长期世界扩张。具体世界观、能力体系、成长机制、角色、组织和剧情由当前系统提出。`
- 页面可见结果：Idea 查询自动拼接作者原文与 Reader Promise、Character Desire & Agency、Advantage / Special Capability、Repeatable Reader Loop、Core Progression Grammar、Action-Space Expansion、World Expansion Grammar、Social / Relationship Dynamics、Resource / Economy、Narrative Drive、Phase Transition、Failure / Fatigue Risks、Book DNA、Mechanism、Contrast、Reference Program 等焦点。
- 机器输出：未手工指定书名、机制或 Reference Program；Reference Programs 页面加载为 40 个 VALIDATED，当前选择 `0 / 3`。
- 一致性判断：通过。输入仍保持宽泛，未人为补主角、世界、金手指、等级或剧情。
- 调试/下一动作：提交页面生成的有效查询到 GBrain。

## 页面/事件 4 · Idea GBrain 返回

- 时间：2026-08-19 09:14 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：点击“从 GBrain 取灵感”，等待返回。
- 输入：页面自动生成的 Idea effective query；页面未选择 Reference Program。
- 页面可见结果：GBrain 状态为“可用”；范围为“全 Brain”；stdout 原样进入 GBrain Inspiration Results 文本框。
- 机器输出：raw count=17。raw slugs（按页面返回顺序）：`book-dna/rcv0-02-xianxia-bailian-chengxian`、`syntheses/categories/synth-category-02`、`book-dna/rcv0-03-dushi-xiuzhen-chatianqun`、`arcs/rcv0-23-xianxia-jiantu-zhi-lu-arc-v1-03`、`book-dna/rcv0-20-gaowu-quanqiu-gaowu`、`arcs/arc-personal-wish-to-historical-scale-v1`、`book-dna/rcv0-14-wuxia-langzi-jianghu`、`maps/progression-and-breakthrough`、`book-dna/rcv0-28-xuanhuan-jiangye`、`book-dna/rcv0-13-wuxia-jinyong-shijie-daoshi`、`book-dna/rcv0-04-kehuan-taxing`、`syntheses/categories/synth-category-07`、`arcs/arc-03-craft-to-second-floor`、`arcs/rcv0-22-xuanhuan-wulian-dianfeng-arc-v1-03`、`maps/exploration-and-world-expansion`、`book-dna/rcv0-16-youxi-hupozhijian`、`observations/rcv0-23-xianxia-jiantu-zhi-lu-observation-v1-05`。
- 一致性判断：通过。结果与玄幻/成长/探索方向总体相关，未出现查询错误；当前产品没有 accepted/rejected 字段或自动筛选层，故 accepted count、rejected count、rejection reasons 均为 NOT EXPOSED，而不是推定为 17/0。
- 调试/下一动作：使用原始结果生成 Idea Prompt，不手工筛选材料。

## 页面/事件 5 · Idea → Proposal

- 时间：2026-08-19 09:15—09:16 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：点击“生成男频爽文创意 Prompt”，复制 Prompt；将 Codex 返回文本放入 Proposal 编辑区；点击“保存 Proposal”。
- 输入：Idea Prompt 页面原文（复制长度 4,953 字符）；Codex 返回 3 个候选：`灰炉借火`、`借名登天`、`山海行账`。
- 页面可见结果：Prompt 复制成功；Proposal 编辑区显示完整候选文本；保存状态为“Proposal 编辑区已保存到 PROPOSAL.md”。
- 机器输出：Idea Proposal 已写入 `books/general-generation-test-v1/PROPOSAL.md`；未应用到 BOOK，因为 Idea 输出没有 BOOK 四个一级标题。
- 一致性判断：通过。返回文本未经页面外人工改写；产品没有候选选择控件，也没有自动把候选传给 Outline 的字段。
- 调试/下一动作：保持作者宽方向不变，切换真实 Outline 模式并重新运行 GBrain。

## 页面/事件 6 · Outline GBrain 与规划 Prompt

- 时间：2026-08-19 09:16—09:18 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：选择“新书/总纲规划”，生成默认查询，点击“从 GBrain 取灵感”，再点击“生成当前 Prompt”。
- 输入：同一份作者宽方向；Outline effective query 额外携带空 BOOK 的初始缺口/非对称位置/成长基因占位，未人工填入 Idea 候选。
- 页面可见结果：GBrain 状态为“可用”；Outline Prompt 要求完整输出 BOOK、约 100 章剧情块、连续十章和当前状态。
- 机器输出：raw count=13。raw slugs（按页面返回顺序，重复 slug 保留）：`arcs/rcv0-23-xianxia-jiantu-zhi-lu-arc-v1-03`、`book-dna/rcv0-20-gaowu-quanqiu-gaowu`、`book-dna/rcv0-03-dushi-xiuzhen-chatianqun`、`syntheses/categories/synth-category-02`、`selection/inventory`、`book-dna/rcv0-19-gaowu-wozai-jingshenbingyuan-xue-zhanshen`、`book-dna/rcv0-14-wuxia-langzi-jianghu`、`selection/inventory`、`arcs/arc-personal-wish-to-historical-scale-v1`、`arcs/arc-uncertainty-to-three-realm-duty-v1`、`book-dna/rcv0-28-xuanhuan-jiangye`、`book-dna/rcv0-02-xianxia-bailian-chengxian`、`selection/pilot-selection.proposed`。
- 一致性判断：GBrain 查询成功；前四项、Book DNA 和 arcs 与规划相关，但 `selection/inventory` 含 `WARNING 使用非 UTF-8 编码：gb18030`，`selection/pilot-selection.proposed` 标为 PROPOSED，属于当前全 Brain raw 结果中明显较弱/不应直接当 VALIDATED 证据的材料。产品没有 rejected 字段，未做人工剔除。
- 调试/下一动作：使用页面当前 Outline Prompt 生成一份完整规划返回。

## 页面/事件 7 · Outline → Proposal → BOOK

- 时间：2026-08-19 09:18—09:20 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：将 Outline Codex 返回放入 Proposal；保存 Proposal；点击“将 Proposal 应用到 BOOK 编辑区”；点击“保存 BOOK.md”。
- 输入：完整四个一级标题的 Outline 返回；无人工补充世界、能力、角色或剧情。
- 页面可见结果：应用提示“16 个 BOOK 区域”；100 章全景识别 `5 个剧情块`；保存状态为“BOOK.md 已保存”。
- 机器输出：`PROPOSAL.md` 包含 4 个一级区块；`BOOK.md` 含 13 个设计字段、5 个剧情块、完整十章和状态区；未写入章节正文。
- 一致性判断：通过。Outline 的 16 个正式区域进入 BOOK 编辑区并写盘；Idea Proposal 被当前 Outline Proposal 覆盖是单文件 Proposal contract 的实际行为。
- 调试/下一动作：reload 页面并重新加载同一 book，检查正式内容是否恢复。

## 页面/事件 8 · Reload 回读

- 时间：2026-08-19 09:20 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：刷新页面；从已存在小说下拉框选择 `general-generation-test-v1`；点击“加载”。
- 输入：book id `general-generation-test-v1`。
- 页面可见结果：状态为“已加载 general-generation-test-v1”；成长基因标记、`雨渡灰契` 与 `天门反写`、`雨夜断灯` 与 `入院信的最后一行`、`陆衡十七岁` 均在回读页面可见；全景仍为 `5 个剧情块`。
- 机器输出：API reload 返回的 BOOK、Proposal、Prompt Templates 和章节列表重新填入页面；章节列表为空。
- 一致性判断：通过。正式世界观、成长基因、长期大纲、十章计划和状态没有因 reload 丢失。
- 调试/下一动作：做磁盘文件和模板完整性核对，再测试下一阶段 Prompt。

## 页面/事件 9 · 磁盘持久化核对

- 时间：2026-08-19 09:20—09:21 +02:00（Europe/Paris）
- 页面：本地文件核对；URL：N/A
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：读取测试 book 目录、解析正式区块、比较 Prompt Templates 默认内容和 Proposal/BOOK 区块。
- 输入：只读文件核对；未写入文件。
- 页面可见结果：N/A。
- 机器输出：`BOOK.md` 44,773 bytes；`PROPOSAL.md` 44,745 bytes；`PROMPTS.md` 21,790 bytes；`audit/browser_workflow_audit.md` 2,267 bytes；`chapters/` 中 0 个文件。BOOK 有 4 个一级标题和 13 个设计标题；Proposal 有 4 个一级标题；Prompt Templates 与当前默认模板相等。
- 一致性判断：通过。BOOK 与 Proposal 的设计区块字面差异仅为 12 个空行；去除空行后内容相等，属于页面 compose 的格式归一化，不是内容丢失。
- 调试/下一动作：检查 reload 后的运行上下文是否也持久化，并尝试生成 Outline/当前章节上下文。

## 页面/事件 10 · Reload 后 Outline context

- 时间：2026-08-19 09:21—09:22 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：观察 reload 后运行字段；重新填写完全相同的作者方向；切换 Outline；重新运行默认查询和 GBrain；生成当前 Prompt。
- 输入：原作者宽方向原文；无新增设定。
- 页面可见结果：刚 reload 时创作方向为空、GBrain 为“未查询”；重新输入和查询后 Prompt 生成成功。
- 机器输出：reload 后生成的 Outline Prompt 长度约 21,503 字符，并同时包含 `残契识别`、`雨渡灰契`、`天门反写`、`雨夜断灯`、作者宽方向和新的 GBrain slug。
- 一致性判断：正式 BOOK 可以驱动下一阶段；但创作方向和 GBrain Results 不在当前 book storage 中，不能仅靠 reload 恢复完整运行上下文，需要作者重新输入/查询。
- 调试/下一动作：不人工从十章计划补八字段，直接测试当前章节 Hard Gate。

## 页面/事件 11 · 当前章节 Hard Gate

- 时间：2026-08-19 09:22:08 +02:00（Europe/Paris）
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:8000/`
- 作用域：book_id=`general-generation-test-v1`；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：切换“当前章节写作”，不填写或改写第一章事件，点击“生成当前 Prompt”。
- 输入：当前章具体小纲为空；未来十章计划仍为系统生成的四字段格式。
- 页面可见结果：Prompt 被阻止，状态原文为“当前章节 Prompt 被阻止：触发事件、推动事件的人、主角行动、对手或世界反应、直接结果、状态变化、叙事功能、结尾推动力”。
- 机器输出：`parse_outline_fields` 的八字段 Hard Gate 未通过；未生成正文，未写入章节文件。
- 一致性判断：通过门禁行为；但当前流程没有从已生成的十章计划自动产生八字段当前章小纲的 UI 步骤，因此本轮不能宣称已经“可以开始写第一章”。
- 调试/下一动作：停止测试，不写正文、不人工补小纲；输出 Functional 与 Creative/Product 分离的报告。

## 最终审计摘要

- 事实结果：1 个新 book；1 个 Idea Proposal 过程结果；1 个完整 Outline Proposal；1 个已保存 BOOK；5 个未来 100 章剧情块；完整十章；0 个章节正文。
- 证据结果：`C:\dev\tgn-story-mvp\books\general-generation-test-v1\BOOK.md`、`PROPOSAL.md`、`PROMPTS.md`、`audit/browser_workflow_audit.md`；页面全景 5 块；reload 后正式 BOOK 标记全部恢复；章节目录为空。
- 页面结果：最终 URL 为 `http://127.0.0.1:8000/`；最终状态是当前章节 Prompt 被八字段 Hard Gate 阻止；没有处理中任务或假成功章节提示。
- Cohesion 结果：作者方向 -> GBrain -> Idea -> Proposal -> Outline -> BOOK -> reload -> Outline context 已闭合；Idea 候选没有专用选择/传递链；正式 BOOK 与 Proposal 内容闭合（仅空行归一化）；BOOK -> 当前八字段小纲未闭合。
- 潜在问题：运行方向和 GBrain 结果 reload 丢失；GBrain raw 结果没有 accepted/rejected 过滤层且混入 WARNING/PROPOSED selection 材料；Idea 到 Outline 没有候选选择和上下文传递；未来十章四字段格式与当前章节八字段 Hard Gate 不连通。
- 下一步：若要继续产品测试，应先由产品正常流程生成当前章八字段小纲，再单独测试章节 Prompt；本轮不人工补写、不生成正文。
