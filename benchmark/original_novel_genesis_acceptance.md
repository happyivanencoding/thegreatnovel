# Novel Project Governance、Progressive Initialization 与 Original Genesis 验收

验收日期：2026-08-11
永久分支：`小说续写_codex`

## 1. 作者书库治理

改造前的真实基线是 59 个可见条目：56 本 Registered Book，加 3 个 production discovery
Candidate。分类计划对 56 本已注册书给出的当前权威计数为：

| book_kind | 数量 |
|---|---:|
| AUTHOR | 2 |
| BENCHMARK | 49 |
| TEST | 3 |
| DEMO | 1 |
| UNCLASSIFIED | 1 |

改造后的 production 作者书库默认只显示 2 张 AUTHOR 卡片：`douluo-dalu` 与
`book-6k-0lnr4da`。已经导入的 source 不再重复显示为 Candidate；BENCHMARK、TEST、DEMO 和
UNCLASSIFIED 不会进入作者 Catalog 或 Book Selector。技术内容没有删除，使用
`novel web serve --developer-mode` 才能进入服务端提供的技术书库。

唯一未分类项目为 `personal-original-root-cause-candidate`。本轮没有足够权威证据决定它是作者
作品、参考书还是技术候选，因此保持 UNCLASSIFIED。当前证据报告没有认定任何自动可合并的重复
书；标题和路径没有被用作自动合并依据。

分类建议与显式应用记录见：

- `benchmark/library_project_classification_plan.md`
- `benchmark/library_project_classification_plan.json`
- `benchmark/library_project_classification_mapping.json`

## 2. 正式创作与实验边界

- 正式续写沿用当前 ACTIVE/OFFICIAL Edition，依次产生 Candidate、Chapter Contract、Draft、
  十项 Validator、作者显式批准和 Canon Commit；不会创建新 Book 或 Edition。
- 局部改写沿用当前 Edition 的 Revision Campaign、Revision Draft 与 Chapter Variant；批准改写和
  启用版本仍是两次独立动作。
- 只有“保留当前版本并另开路线”才创建派生 Edition；实验 Edition 不能直接成为正式 ACTIVE。
- Benchmark 脚本使用隔离运行根并显式写 `book_kind=BENCHMARK`，不会进入作者书库。

自动证明覆盖 `tests/integration/test_revision_workflow.py`、
`tests/integration/test_project_governance.py`、`tests/integration/test_draft_approval.py` 和
`tests/integration/test_original_novel.py`。本次真实浏览器 Genesis 验收也证明第一章批准后进入同一本
Book、同一个 base Edition 的“续写第2章”，没有产生第二本书。

## 3. QUICK / BALANCED / FULL

三个深度都先建立全书 Source Coverage、Arc 唯一归属和低成本结构索引；深度只改变语义覆盖，
不改变 Source 完整性，也不降低 Canon、Approval、Edition 或 FULL READY 门禁。

| 深度 | 深读策略 | 访问能力 | 明确不声称 |
|---|---|---|---|
| QUICK | 开篇、最新边界、Arc 首尾和少量高变化章节 | 浏览结构、部分画像、初步规划、手动补齐 | 全书语义完整、完整历史状态 |
| BALANCED | 每个 Arc 关键锚点、当前 Arc、边界、活跃实体/线程依赖 | Limited/Action Ready；只有边界依赖无阻断时才续写 | 固定间隔抽样、全书历史完整 |
| FULL | 所有有效章节、全部 Arc、实体解析、综合、指标和图谱 | FULL；现有严格 READY | 推断自动升级为 Canon |

30 章隔离结构 fixture 的实测打包结果如下。这是 Python 合同与任务规划耗时，不是 Codex 语义分析
耗时，也不冒充真实长篇质量 Benchmark：

| depth | 全书轻量索引 | 深读任务章节 | 未分析章节 | 打包耗时 |
|---|---:|---:|---:|---:|
| QUICK | 30 | 12 | 18 | 0.1031s |
| BALANCED | 30 | 19 | 11 | 0.1057s |
| FULL | 30 | 30 | 0 | 0.1084s |

升级只创建缺失任务并复用已验证结果；未分析章节保持 UNKNOWN。续写/改写发现目标依赖不足时，
系统创建本地 Evidence Hydration handoff，补齐后恢复原动作。详细合同和证据见
`benchmark/progressive_initialization_acceptance.md`。

## 4. 一句话原创新书：真实浏览器与 Codex 语义执行

本次使用独立验收根
`C:\Users\jingx\AppData\Local\Temp\novel-original-browser-acceptance-20260811`，没有写入 production
`library/`，也没有预先创建 TXT/Markdown。

实际链路：

1. 浏览器输入 premise“城市每天删除一种情感，失忆档案员决定找回它们”。
2. 创建 `original-3856173273c7`：AUTHOR + ORIGINAL、base Edition、0 个章节、无 Source Document。
3. 创建并由 Codex 桌面端处理 `handoff_6de757432b870813e4b451b3`；输出恰好 3 个书名、3 个
   Foundation、3 条未来路线和 3 个首章候选，全部保持 PROPOSAL。
4. Proposal 导入后仍是 0 章、0 Canon。浏览器编辑书名与核心冲突，并提交精确确认语
   `确认基础框架`。
5. 确认后建立 Author Truth、persistent directives、九维 Book Profile、SHORT/MID/LONG Planning
   和 Genesis State；仍不创建第0章或正式章节。
6. 页面显示恰好 3 个首章候选。选择“《不存在的悲伤档案》”后冻结现有 Candidate、
   `contract_f1f31d28858f654eca1d9915` 和 Draft Task，不重新生成候选。
7. Codex 桌面端按冻结合同生成首章正文，导入为 `draft_51bacf681382b0a05afe33fe`。Canon、
   Timeline、Knowledge、Character、Economy/Power、Contract、Debt、Payoff、Repetition、Style
   共 10 项 Validator 全部通过，状态停在 VALIDATED，Canon 仍未变化。
8. 隔离验收页面提交精确批准语 `批准写入正史` 后，才产生第 1 章 Canon，项目状态变为 WRITING。
9. 点击“继续下一章”进入现有 Workbench，页面显示“续写下一章 · 第2章”，证明后续回归标准
   continue-novel 内核。

这里的 Foundation Proposal 和首章正文是本次 Codex 根据冻结输入实际生成的语义产物，不是测试
fixture。`tests/integration/test_original_novel.py` 另外使用固定本地 DraftOutput 验证合同和审批事务；
两种证据没有混称。

浏览器证据：

- `benchmark/artifacts/original_novel_genesis/01-production-author-library.png`
- `benchmark/artifacts/original_novel_genesis/02-original-first-chapter-approved.png`
- `benchmark/artifacts/original_novel_genesis/03-standard-continuation-workbench.png`

三个页面的浏览器控制台均无 error。

## 5. 自动验收

- `uv sync --python C:\Users\jingx\anaconda3\python.exe --extra dev --no-editable --reinstall-package novel-authoring-system`：通过。
- `uv run --no-sync pytest -q`：231 passed。
- `uv run --no-sync ruff check src tests`：通过。
- `uv run --no-sync mypy src`：153 个 source files 无问题。
- `uv run --no-sync python -m compileall -q src tests`：通过。
- Web static 下 4 个 JavaScript 文件全部通过 `node --check`。
- `novel --help`、features/rhythm/hooks/metrics/segments/workflow help：通过。
- `uv run --no-sync novel web doctor`：全部检查通过。

## 6. Safety 与已知限制

- 没有删除、移动或重写任何现有 `library/` Book，也没有修改 `book/` 原始正文。
- 没有按标题自动合并，不新增第二套 Library、Planning、Drafting 或 Approval Engine。
- Web 只生成和读取本地 handoff；语义执行由 Codex 桌面端领取，Web 没有调用模型进程或远程 API。
- QUICK/BALANCED 的 Soft Reference、Recall Hint 和未分析内容不会升级为 SOURCE_VERIFIED、CURRENT_STATE
  或 Canon。
- 本轮没有完成真实长篇在 QUICK/BALANCED/FULL 下的语义质量、事实错误率和总耗时对照；当前可报告的
  三深度数字仅是确定性任务打包证据。该质量 Benchmark 仍需要分别领取真实 Arc handoff 后运行。
- Genesis 候选的数值门禁用于把作者确认的 Proposal 接入现有 Chapter Contract；它不是独立的文学质量
  Benchmark 分数。真正正文仍必须经过十项 Validator 和作者批准。
