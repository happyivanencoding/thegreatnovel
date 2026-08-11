# Novel Studio V3 Product Gap Audit

审计日期：2026-08-11

基线：`小说续写_codex`，HEAD `d7f6335`。本报告在修改生产代码前完成。

## 1. 审计方法与样本

本次不是模板推断。已启动并操作当前 FastAPI/Jinja/native JS Web：

- production：`http://127.0.0.1:8766/library`
- 隔离审计服务：`http://127.0.0.1:8768/library`
- 同一 HEAD 的原创端到端验收书库：`http://127.0.0.1:8769/library`

实际样本：

| 场景 | 样本 | 实际操作 |
|---|---|---|
| production 作者书库 | `book-6k-0lnr4da`、`douluo-dalu` | 浏览分组、状态、导入按钮、进入工作台 |
| 100 章测试书 | 隔离导入 `测试小说.md`，生成 `book_id=100` | 发现、确认、BALANCED、进入 Limited Studio、发起续写、触发补齐 |
| 300 章以上真实长书 | production `douluo-dalu`，379 章 | Workbench、当前边界、版本选择器、续写/改写入口 |
| 新建原创项目 | 隔离 `original-8d961a9fd727` | 一句话创建、生成 bootstrap handoff、连续重新生成 |
| 已有 Revision Edition | production `douluo-dalu`，13 个 Edition | Edition Selector、改写入口、当前/派生版本语义 |
| Foundation 到首章批准 | 同一 HEAD 隔离验收项目 `original-3856173273c7` | 复核已确认 Foundation、首章批准和第二章入口；结合当次真实验收产物核对前序页面 |

浏览器控制台：上述页面未观察到 `error` 或 `warning`。当前主要问题是产品状态与流程语义，而不是浏览器运行错误。

## 2. 真实流程结果

### 2.1 导入与初始化

| 当前实际行为 | 预期行为 | Gap |
|---|---|---|
| 主按钮写“导入现有小说”，点击后只显示“书籍目录已复制” | 打开本地 TXT/Markdown 导入；若没有上传能力则明确叫“复制导入目录” | 文案与行为不一致 |
| 用户必须先把文件放入监听目录，再刷新或等待发现，再进入候选页 | 页面内选择/拖入文件并安全复制到 discovery root | 导入仍依赖系统外手工步骤 |
| 初始化页先要求理解“快速了解/均衡准备/完整初始化” | 先问“接下来想做什么”，系统推荐深度 | 抽象档位先于作者目标 |
| BALANCED 确认后，结构索引完成即直接进入 Limited Studio | 允许早进 Studio，但必须明确哪些创作能力可用 | 进入速度快，但能力标签不足 |
| Workbench 同时显示“均衡准备”“初始化任务等待 Codex”“续写下一章” | CTA 应根据 CONTINUE_READY 决定；不足时保存原动作并补齐 | 可点击不等于可完成 |

100 章真实操作结果：选择 BALANCED 并点击“准备初始化”后约 2 秒完成确定性导入和 100 章结构建立，立即进入 Limited Studio；初始化 handoff 仍为 `READY_FOR_CODEX`。

### 2.2 续写、定向补齐与恢复

真实操作：在 100 章书的 Limited Studio 打开“续写第 101 章”，填写作者目标并点击“开始续写”。

结果：

- 没有保存可见的 Pending Author Action；
- 没有进入一个“续写第 101 章”的统一 Activity；
- 又创建了一个标题同为“小说初始化”的 handoff；
- Activity Center 同时出现两个“小说初始化”；
- 页面仍停留在原续写表单，刚填写的作者目标没有形成可恢复状态；
- 补齐完成后当前没有自动恢复原 Continuation Handoff 的合同。

因此“完成补齐 → 自动恢复续写”在当前产品中不能自然走完；用户必须再次进入动作、重新填写并再次提交。

### 2.3 改写与另开路线

当前“改写本章”直接进入“准备一个派生版本”，只显示创新程度、创新方向和改写目标。

缺失：

- 没有先问“修订当前故事路线”或“保留当前版本，另开故事路线”；
- 没有 `edition_purpose`；
- 没有 `official_role`；
- 没有 `fork_chapter_ordinal`；
- 没有作者可理解的 alternate route 创建入口；
- 已有 Edition Selector 直接混排“使用中 / 已校验草稿 / 草稿”，并显示 `base`、DRAFT/ACTIVE 等生命周期语义。

现有内核已经把 Revision 批准与 Edition 激活分开，并保留显式激活确认，这是正确边界；问题是作者入口和 Edition 业务用途尚未表达。

### 2.4 原创新书、Proposal 与 Foundation

新建页实际暴露：`Original Novel`、`premise`、`Proposal`、`Canon`、`handoff`。创建后页面继续暴露 `Story Foundation / Genesis State`、`ORIGINAL_SEED`、handoff ID、`READY_FOR_CODEX`、`ORIGINAL_BOOK_BOOTSTRAP`。

连续点击“重新生成”时：

- 第一次 handoff 仍未完成；
- 系统立即创建第二个 handoff；
- 页面只显示最新 handoff；
- 没有 CURRENT/GENERATING/READY/ARCHIVED Proposal Version；
- 没有“当前方案 / 正在生成 / 历史方案”；
- 没有相同 GENERATING 任务去重。

同一 HEAD 的已完成原创项目进一步显示：

- Foundation 确认依赖手打固定句“确认基础框架”；
- 确认逻辑依次调用 Truth、Directive、Profile、Intent、Thread、Candidate 和文件写入，不是单数据库事务；
- `accepted.json` 目前同时承担“是否已确认”的权威判断；
- 九维 Profile 主要由通用 `_profile_values` 拼接；
- Route 主要保存 `route_id`，没有独立 `ActiveNarrativeSpine`；
- Open Questions 与 Hidden Truth Candidates 没有进入对应现有模块；
- Genesis Candidate 写入固定 75 分，即使没有真实评分输入；
- 已确认内容详情直接显示转义后的 raw JSON；
- 第一章批准后内部状态为 `WRITING`，书库分组标题仍写“初始化已完整验收”。

### 2.5 Readiness 与错误就绪

代码与页面共同确认：

- `initialization/service.py` 把 `graphs.json` 序列化成字符串，通过是否包含“主角/protagonist”和“thread/线程”设置两项 confirmed；
- 只要 key 或文本出现，就可能产生错误确认；没有验证非空实体、证据、当前章节适用性和当前状态；
- production 379 章书卡位于“可以继续创作 / 初始化已完整验收”，卡片正文却写“初始化尚未完整”；
- 同一工作台显示“标准就绪”，但九维 Profile 全部“未建立”，当前章节状态也正在补齐；
- 原创项目第一章批准后位于“初始化已完整验收”分组，混淆了 `WRITING_READY` 与已有小说 `FULL READY`。

当前没有独立的 `ContinuationBoundaryReadiness`、`RevisionRangeReadiness` 或作者能力矩阵。

### 2.6 渐进初始化、复用、优先级和 ETA

当前结构索引和深读选择已经能让 100 章书快速进入 Limited Studio，这是可保留基础；但：

- 语义工作仍以 Arc output 为主要复用单位；
- 没有持久化的章节级 `ChapterAnalysisRecord(CONTINUITY/LITERARY/BOUNDARY)`；
- BALANCED 不保证每章都有独立 `ChapterContinuityDelta`；
- 当前边界虽被选入深读章节，但整体任务合同仍围绕 Arc 输出，未形成“边界第一”的独立调度队列；
- 定向补齐没有相关性评分与批次预算；
- ETA 使用“初始化创建后的总墙钟时间 / 新完成 Arc 数”，会把作者等待 Codex 的时间算入处理速度；
- `library_catalog.js` 每 10 秒轮询，状态变化时调用 `location.reload()`，会打断滚动、阅读和表单输入。

## 3. 作者需要手工执行的步骤

### 3.1 当前首次可安全续写

按当前产品，导入一本新长书到得到可复制的 Continuation Handoff，正常路径约 15—17 个作者动作：

1. 在系统外找到监听目录；
2. 复制 TXT/Markdown 到目录；
3. 返回书库并刷新/等待发现；
4. 打开待初始化书卡；
5. 理解并选择 QUICK/BALANCED/FULL；
6. 点击准备初始化；
7. 点击复制初始化 Codex 指令；
8. 切换到 Codex 并处理初始化 handoff；
9. 回到 Web 等待/刷新；
10. 进入 Limited Studio；
11. 点击续写下一章；
12. 填写交付阶段、创新程度、方向和作者目标；
13. 点击开始续写；
14. 如果上下文不足，再复制补齐指令并切到 Codex；
15. 回到 Web 等待补齐；
16. 重新打开并重新填写续写表单；
17. 再次提交并复制 Continuation 指令。

当前首次可创作时间的主要浪费不是确定性 ingest，而是重复 handoff、重复表单和没有 Pending Action 自动恢复。

### 3.2 当前原创第一章

当前至少需要：创建项目、复制 bootstrap 指令、切到 Codex、返回、选择 Foundation、编辑长表单、手打确认语、选择首章候选、复制 Draft 指令、切到 Codex、返回、校验、手打正式批准语。Foundation 页面本身不是四步作者 Wizard。

## 4. 页面暴露的工程术语

默认作者界面仍可直接看到：

- Premise、Proposal、Story Foundation、Genesis State；
- Local Handoff、handoff ID、READY_FOR_CODEX、ORIGINAL_BOOK_BOOTSTRAP；
- Canon、Author Truth、Truth Board、Reveal Agenda、Secret Board；
- base、DRAFT、ACTIVE、已校验草稿；
- SHORT/MID/LONG Planning；
- Initialization Contract、Arc ID、Arc Coverage、Semantic Metric Bootstrap；
- raw JSON、转义 Unicode、内部 candidate/draft ID。

这些应保留在“技术详情”，默认界面改成作者语言。

## 5. 重复读取、重复初始化与状态中断点

| 问题 | 真实证据 | 影响 |
|---|---|---|
| 重复初始化任务 | 同一 100 章书先有初始化 handoff，点击续写后又出现第二个“小说初始化” | 作者无法判断哪个任务服务于哪次动作 |
| Proposal 重复生成 | 同一原创项目 GENERATING/READY_FOR_CODEX 时可连续生成新 handoff | 旧任务隐藏，结果可能互相覆盖认知 |
| Arc 级复用 | manifest 记录 `reused_arc_ids`，没有章节层分析记录 | Arc 重划后容易重做整章语义工作 |
| 表单丢失 | 补齐没有 Pending Author Action | 用户必须重新填写续写/改写目标 |
| 墙钟 ETA | `created_at → now / completed Arc` | 把用户等待时间当成模型处理时间 |
| 整页刷新 | catalog 状态变化后 `location.reload()` | 滚动、阅读和输入可能被打断 |

## 6. 优先级结论

### P0：先修语义和可靠性

1. Edition 用途/官方角色迁移，Revision 与 Alternate Route 分流；批准与激活继续分离。
2. 删除字符串搜索 readiness，建立显式 Continuation/Revision Readiness 和能力矩阵。
3. Genesis Foundation 单事务 + 幂等；`accepted.json` 降为可再生成导出。
4. Proposal Version + GENERATING 去重。
5. Pending Author Action + deepening 完成后自动恢复原动作。

### P1：真正缩短首次可创作时间

1. 四层初始化与 CURRENT_BOUNDARY_DEEP 优先队列。
2. BALANCED 全书逐章 CONTINUITY_INDEX，文学深读只做代表章。
3. 章节层分析复用；升级只补缺层。
4. 定向补齐按相关性和预算分批。
5. 基于 active processing 的区间 ETA。

### P1：作者体验收口

1. 真文件导入或诚实改名；书库互斥分组和未分类提示。
2. 初始化目标优先；显示实际计划。
3. 原创四步 Wizard，去固定确认语，隐藏工程术语。
4. Workbench 首屏单主 CTA，默认折叠高级工具。
5. 一个作者动作对应一个 Activity Timeline；技术 ID 全部折叠。
6. 状态 API/局部轮询，禁止自动整页 reload。

## 7. 验收基线

后续实现必须证明：

- Active Edition 与 Canon 未被迁移改变；
- 原创 Foundation 任一步失败时数据库无半状态；
- 相同 Proposal/待恢复动作重试不产生重复记录；
- BALANCED 每章 Continuity 状态只能是有证据的变化、`UNKNOWN` 或 `COMPLETE_NO_CHANGE`；
- 补齐完成后自动产生原 Continuation/Revision handoff，作者输入仍在；
- 每本书在书库只属于一个主分组；
- 原创第一章批准后显示 `WRITING_READY`，不显示 FULL；
- 轮询过程中滚动、展开状态和正在编辑的表单不丢失；
- 真实浏览器控制台无错误，并用 100 章、379 章、原创、Revision Edition 再走一遍主流程。

## 8. V3 实施后复验

复验仍使用 production 8766、100 章隔离书库 8768、原创隔离书库 8769；没有把测试状态写入 production `library` 或只读 `book`。

### 8.1 已收口行为

| 验收点 | 复验结果 |
|---|---|
| 版本语义 | Edition 生命周期与 `edition_purpose`、`official_role` 分离；修订和另开路线必须先选用途，批准后不会自动激活。 |
| 就绪语义 | 字符串搜索已移除；续写和改写分别使用带非空内容、证据和章节适用范围的显式 Readiness。 |
| 作者能力 | 书卡按 BROWSE / PROFILE / PLAN / CONTINUE / REWRITE / WORLD_HISTORY / FULL 能力表达；原创第一章批准后为 WRITING_READY，不冒充 FULL。 |
| Genesis 可靠性 | Foundation 先构造并验证 `GenesisApplyPlan`，再在单一数据库事务中写入；`accepted.json` 只在提交后导出；相同 proposal/foundation 重试幂等。 |
| Proposal 版本 | CURRENT / GENERATING / READY / ARCHIVED / REJECTED 已持久化；已有 GENERATING 时重复点击返回原任务。 |
| 渐进初始化 | SOURCE_STRUCTURE、CONTINUITY_INDEX、LITERARY_PROFILE、CURRENT_BOUNDARY_DEEP 分层；BALANCED/FULL 逐章写 Continuity Delta，边界优先。 |
| 分析复用 | `ChapterAnalysisRecord` 按章节、Edition、分析层和 source revision 复用，不再依赖 Arc 不变。 |
| 定向补齐 | 依当前人物、物品/能力、线程、变化、最近出现和因果距离排序，单批预算 12 章；仍阻断时才扩下一批。 |
| 自动恢复 | Pending Author Action 保存原表单与请求阶段；补齐后自动创建原 Continuation/Revision handoff；相同动作去重。 |
| 书库 | 主分组互斥；提供真实 TXT/Markdown 多文件导入和同名冲突策略；未分类项目只在页脚提示并进入独立整理页。 |
| 作者 UX | 初始化先问目标；原创为四步 Wizard；Workbench 首屏只有一个主 CTA；左栏顺序为正文、人物与关系、世界与物品、剧情规划、创作任务、高级工具。 |
| 局部更新 | 书库和 Workbench 均不再因轮询执行整页 reload；浏览器中填写改写目标并等待一轮轮询后，输入仍保持。 |

### 8.2 浏览器实测证据

- production 书库实际显示“导入小说”弹窗，可选 TXT/Markdown、多文件和三种同名冲突行为；未分类项目显示独立整理入口。
- 379 章 production 项目按真实缺口显示“需要修复”，没有再用完整就绪文案掩盖缺失结果。
- 100 章 Workbench 第一屏实际显示当前创作位置、本章状态、下一章必须推进内容、当前任务和唯一主 CTA“继续写下一章”。
- 100 章改写页实际显示“修订当前故事路线”和“保留当前版本，另开故事路线”两个选择，默认只选择前者。
- 左右栏隐藏后均保留常驻展开按钮；默认导航顺序严格为：正文 → 人物与关系 → 世界与物品 → 剧情规划 → 创作任务 → 高级工具。
- 在隔离书库建立 V3 Proposal 后，原创页面实际呈现四步 Wizard、CORE/PREFERENCE/OPEN 的作者文案、九维 Profile 初稿、Active Route、Open Questions 与幕后候选；没有 75 分占位分数，也不要求手打固定确认语。
- 书库、长篇 Workbench、原创 Wizard 三个浏览器标签的 `dev.logs()` 均为空。

### 8.3 自动化验收

- `pytest -q`：238 passed。
- `ruff check src tests`：通过。
- `mypy src`：通过。
- `novel --help`、features/rhythm/hooks/metrics/segments/workflow help 与 `novel web doctor`：8 个入口全部通过。
- migration 14 在 fresh database 和现有测试数据库均通过；Active Edition 和 Canon 相关回归测试通过。

### 8.4 首次可安全续写步骤变化

作者仍需遵守 Local File Handoff，手动把一次 AI 指令交给 Codex；Web 不会启动模型、shell 或 Codex 子进程。在这个硬边界下，正常路径由基线约 15—17 步降为约 8—10 步。上下文不足时不再要求重新填写表单：同一 Activity 自动完成“检查上下文 → 分批补齐 → 恢复原动作 → 准备续写任务”。
