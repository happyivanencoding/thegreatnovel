# Novel Studio Library & Drop-In Book Onboarding 验收报告

验收日期：2026-08-11

分支：`小说续写_codex`

结论：~~**通过**~~（**已于 2026-08-11 复审撤销**，见下方“2026-08-11 复审修订”）

> 修订后结论：~~**不通过 → 修复已落地，自动测试证据充分；端到端/真实 Codex 证据：进行中（待补）。**~~（**已于 2026-08-11 证据回填后再次更新**）
>
> 最终结论（2026-08-11 证据回填后）：**通过（含 2026-08-11 修复与真实端到端证据）**。blocker L-1/L-2/L-3 已全部解除（逐条状态与证据出处见复审章节“Blocker 清单与解除状态”）；真实浏览器端到端与真实语义执行证据见“证据回填”小节。关键限定：本次真实语义执行的执行主体为开发代理在 Codex 桌面端合同下按 skill 执行，非作者手工操作的 Codex 桌面端会话，不得称为“作者侧 Codex 桌面端执行”。

## 1. 交付结果

本轮把现有 Book Library、deterministic ingest、NOVEL_INITIALIZATION Local File Handoff 与 Novel Studio 串成一条作者可理解的路径：

`放入正文 → 只读发现 → 作者确认 → deterministic ingest → NOVEL_INITIALIZATION handoff → Codex 初始化 → 严格 READY → 显式进入 Studio`

没有新建第二套 Library、Ingest、Initialization Engine 或任务协议；Web 仍只负责准备本地 handoff、展示真实指令和轮询状态，不调用模型、Codex 子进程或 shell。

## 2. Discovery Root 与格式

- 默认 Discovery Root：`<Library Root 的同级目录>/book`。当前真实配置即 `C:\dev\小说续写系统\book`。
- Browser Acceptance 使用隔离目录：`C:\Users\jingx\AppData\Local\Temp\novel-studio-onboarding-20260811-codex\book`。
- Library Root 与 Discovery Root 明确分离；不会扫描 `library/` 并把内部产物识别为新书。
- 支持格式直接读取当前 ingest 配置：`.md`、`.txt`；不向用户展示解析器尚不支持的格式。
- 顶层 `.md/.txt` 文件各视为一本书；顶层目录视为一个候选，内部文件仍交给现有 ingest 行为处理。
- 忽略隐藏项、`.~*`、`.tmp`、README、符号链接、不支持格式以及 `library/`、`benchmark/`、`audit/`、`_system/` 等内部目录。
- V1 没有引入文件监听守护进程；书库/工作台打开时扫描，前端每 10 秒轻量刷新，也提供“刷新书籍”。

## 3. Catalog 架构

新增的 read model 保持很薄：

| 对象 | 含义 | 权威边界 |
|---|---|---|
| `DiscoveredBookCandidate` | Discovery Root 中只读发现的文件或目录 | 不写 DB、不创建 Book、不创建任务 |
| `LibraryCatalogEntry` | 统一呈现 Registered Book 与 Candidate | 只做作者状态与动作映射 |
| `LibraryCatalogView` | `/library` 与 Workbench Selector 的共同数据源 | 合并 BookRegistry 与扫描结果 |
| `StudioReadinessView` | 判断完整 Studio 是否可开放 | 严格消费现有 Initialization Contract |

Discovery candidate ID 使用规范化相对路径的 URL-safe 编码；没有新增内容哈希体系。同名不同路径保持为不同候选。已注册书通过 `book.yaml` 中精确的 `source_origin.path` 与 candidate 合并，不按标题猜测，也不会重复显示。

统一接口：

- `GET /api/library/catalog`（并保留 `/api/library` 为同一 payload）
- `POST /api/library/discovery/refresh`
- `POST /api/library/candidates/{candidate_id}/initialize`
- `GET /api/books/{book_id}/studio-readiness`

## 4. Discovered、Library 与 Studio Ready

- **Discovered Book**：仅在目录中被发现；`book_id` 为空，Library/DB/Canon 均未改变。
- **Library Book**：作者点击后才通过现有 `ingest_book` 建立；可能仍未初始化。
- **Studio Ready Book**：只有完整初始化合同严格通过后才为 `ready=true`。

作者界面只显示“可创作、待初始化、等待处理、初始化中、等待确认、初始化失败、需要修复”。`NOVEL_INITIALIZATION`、`READY_FOR_CODEX`、`RUNNING` 等原始枚举仅在折叠的技术详情中出现。

## 5. Studio Readiness Gate

服务端 `/workbench` 与对应 API 都执行门禁，不能靠手工 URL 绕过。完整 Studio 只在以下条件全部满足时开放：

1. 至少存在一个有效章节。
2. Initialization manifest、status 和 readiness 三者均为精确 `READY`；`READY_WITH_GAPS`、`BLOCKED`、`STALE` 均不放行。
3. 当前初始化目录包含 Source Coverage、Arc Manifest、events、实体解析、当前世界模型、核心图谱、语义指标清单和 readiness report。
4. 每个 Arc 都存在对应语义提取输出。
5. Source、Arc、章节语义覆盖率均为 100%。
6. Metric bootstrap 为 `COMPLETE`。
7. 核心图谱、主角当前状态、当前主线程已确认，且没有 blocking reason。

没有另造“九维 Markdown 存在即成功”规则。当前 Initialization Contract 并没有把某个单独 Profile/Atlas/Runtime 文件定义成额外的唯一就绪标记，因此门禁使用合同现有 manifest/status/readiness 与其核心产物；这样避免 UI 自己维护第二套初始化标准。合同以后增加新的必需产物时，应在同一 read model 中同步收紧。

## 6. Library、Selector 与 Onboarding

- `/library` 改为作者书库：单一“书库”标题、轻量卡片、作者状态、对应 CTA、折叠技术详情和空书库引导。
- Library 与左上书籍选择器消费同一个 `LibraryCatalogView`。
- 选择器按“可创作 / 进行中 / 待准备”分组，支持书名搜索，不再使用巨大原生 select。
- 每本书保存独立的最近访问 URL；跨书切换不会携带上一书的 `chapter_id`，没有记录时由工作台落到最新章节。
- 顶栏和左栏去除重复书名；edition 与书名同名时面包屑只显示“书名 / 第 N 章”。
- 未初始化书仍使用同一 Studio Shell，但只显示准备步骤，不渲染假世界状态、空 Profile 或空规划区。
- 左右栏继续保留常驻折叠按钮。
- 初始化 handoff 进入右上任务中心，明确归类为“小说初始化”系统任务；等待/运行时显示任务 1，完整 READY 后原地更新为任务 0 / 已完成。

## 7. Initialization Handoff

作者点击“准备初始化”后：

1. Candidate 通过现有 deterministic ingest 复制到受管 Library 并建立章节。
2. 调用现有 `create_initialization_handoff()` 创建 `NOVEL_INITIALIZATION` Local File Handoff。
3. 页面显示“复制给 Codex 的指令”和进度入口。
4. 指令由现有 `copy_instruction()` 从该 handoff 的真实 `prompt.md`/任务合同返回；前端不拼假 prompt。
   **（2026-08-11 复审更正：该步骤在 legacy migrate 导入书上真实失效，见复审章节缺陷 1。修复后 `copy_instruction()` 按“显式 prompt_path → canonical `input/prompt.md` → legacy flat `prompt.md`”回退解析并在缺失时返回 `HANDOFF_INSTRUCTION_MISSING` 结构化错误，不再抛裸 `FileNotFoundError`。）**
5. 页面每 10 秒重新计算 Catalog 与 StudioReadiness。变成 READY 时不突然跳页，而是显示“初始化完成”和显式“进入小说工作台”。
   **（2026-08-11 复审更正：Catalog/StudioReadiness 计算路径曾被字符串 readiness 崩溃阻断，见复审章节缺陷 2；修复后字符串 readiness 被防御性解析，页面与 API 不再 400。）**

## 8. Browser Acceptance（127.0.0.1:8766）

| 项目 | 结果 | 证据 |
|---|---|---|
| A. Web 已打开后放入新文件 | 通过 | 10.5 秒内 Selector 与 `/library` 出现“新测试小说 / 待初始化”，无需重启服务 |
| B. 发现不写 DB | 通过 | 点击前 candidate 的 `book_id=null`；Registry 仍只有原 Ready Book；自动测试同时验证 Library 尚不存在 |
| C. 点击开始初始化 | 通过 | 浏览器真实点击后完成现有 ingest，并生成 `NOVEL_INITIALIZATION` handoff |
| D. 真实指令 | **复审降级：有条件通过（隔离目录）／真实书库复现失败 → 修复后待真实浏览器复验** | 隔离目录内 instruction endpoint 返回现有 `$process-novel-handoff` / `$initialize-existing-novel` 流程；但真实书库复现（`cable-survival-demo`，legacy migrate 导入书）返回 HTTP 400 `WORKFLOW_ERROR`（根因：`prompt_path` 缺 `input/` 段，`copy_instruction` 抛 `FileNotFoundError`），前端显示“无法读取交接指令”。修复已合入工作树，真实浏览器端到端复验待补 |
| E. 初始化处理与 READY | **复审降级：仅合同 fixture 级通过；真实 Codex 证据：无（待补）** | 在隔离 Library 中领取并置为 RUNNING；随后写入的是**合同级 fixture**，不是真实 Codex 语义初始化结果。fixture 只能证明 Web/handoff/readiness 边界契约，不得称为真实 Codex 初始化；StudioReadiness 独立计算为 READY 仅在 fixture 前提下成立 |
| F. 显式进入 Studio | 通过 | READY 页保持原地；点击“进入小说工作台”后才出现正文、世界状态、剧情规划、全书画像和连续性 |
| G. 多书切换 | 通过 | 最终 Selector 同时显示 2 本 Ready、1 本 Running、1 个 Pending candidate；Ready 书之间切换并恢复各自章节正常 |

说明：Browser Acceptance 的语义初始化结果使用隔离目录中的合同级 fixture，目的是验证 Web/handoff/readiness 端到端边界，不伪装成真实模型分析，也没有修改用户真实 source、Canon 或真实 Library。**（2026-08-11 复审强调：fixture 验收不构成真实 Codex 初始化证据；且本轮浏览器验收未发现、后续真实复现暴露了缺陷 1 与缺陷 2 两个 live blocker，原 D/E 项“通过”标记已撤销，详见复审章节。）**

浏览器控制台最终为 0 条 error / warning。

## 9. 截图

1. [01-library-redesign.png](artifacts/library_onboarding/01-library-redesign.png)
2. [02-book-selector.png](artifacts/library_onboarding/02-book-selector.png)
3. [03-new-book-discovered.png](artifacts/library_onboarding/03-new-book-discovered.png)
4. [04-initialization-required.png](artifacts/library_onboarding/04-initialization-required.png)
5. [05-handoff-ready.png](artifacts/library_onboarding/05-handoff-ready.png)
6. [06-initializing.png](artifacts/library_onboarding/06-initializing.png)
7. [07-initialization-complete.png](artifacts/library_onboarding/07-initialization-complete.png)
8. [08-studio-ready.png](artifacts/library_onboarding/08-studio-ready.png)
9. [09-selector-multiple-books.png](artifacts/library_onboarding/09-selector-multiple-books.png)

## 10. DB 与真实书库安全

- Discovery 扫描仅执行目录读取与文件元数据读取；Catalog 查询受管数据库时使用 SQLite `mode=ro`。
- 自动测试对扫描前后文件大小与修改时间逐项比对，保持完全一致。
- 只有带 CSRF 且由作者点击的初始化 POST 才调用 ingest/handoff 写路径。
- 原始 source 在 ingest 前后字节保持一致；受管 Library 使用 COPY_READ_ONLY。
- 当前真实 Library 的只读验收：54 本 Registered Book 全部保留，Catalog 合并后共 58 项；`cable-survival-blind-50` 仍存在，另有 4 个 Discovery candidate。没有按 `book_id` 猜测、隐藏或删除测试/演示书。

当前 Registry 没有可靠的 AUTHOR/DEMO/BENCHMARK/TEST 权威元数据。本轮因此遵循“不猜测”的要求继续显示全部已有书，而没有按名称误分类；未来若加入显式 metadata，可直接在 Catalog read model 上增加作者/技术筛选。

## 11. 自动验证

- `uv run --no-sync pytest -q`：**192 passed**（201.21s）（本报告初次验收时的数字；2026-08-11 缺陷修复后全量回归为 **210 passed**，见复审章节）
- Library/Workbench 定向回归：**33 passed**
- 新增 onboarding 集成测试：**5 passed**
- `uv run --no-sync ruff check src tests`：通过
- `uv run --no-sync mypy src`：通过，148 个源文件零问题
- `uv run --no-sync python -m compileall -q src`：通过
- `node --check`（`library_catalog.js`、`workbench.js`）：通过
- `uv run --no-sync novel web doctor`：通过，新增路由完整
- `novel --help`、`features`、`rhythm`、`hooks`、`metrics`、`segments`、`workflow` 帮助命令：全部通过

新增测试覆盖：只读发现、支持/忽略格式、同名不同路径、registered source 去重、统一 Catalog、CSRF、现有 ingest、真实 handoff 类型与 prompt、未初始化路由门禁、不完整 COMPLETED 阻断、严格 READY 放行、Library/Selector 共源、10 秒轮询和任务中心状态。

## 2026-08-11 复审修订

### 修订原因：两个真实缺陷的复现证据摘要

本报告初次验收把存在 live blocker 的功能标记为“通过”，与后续真实故障矛盾，本次复审予以纠正。两个缺陷均已在本会话确认、修复并通过全量回归，但端到端证据仍在补齐中。

**缺陷 1：legacy migrate 导入书的初始化交接指令无法读取**

- 真实复现：`cable-survival-demo`（legacy migrate 导入书）的 `NOVEL_INITIALIZATION` handoff 点击“复制给 Codex 的指令”。
- 现象：instruction endpoint 返回 HTTP 400，响应体错误码 `WORKFLOW_ERROR`；服务端 traceback 为 `FileNotFoundError`（`copy_instruction` 按 `prompt_path` 读不到文件）；前端显示“无法读取交接指令”。
- 根因：legacy migrate 路径写入的 `prompt_path` 缺少 `input/` 段（指向 `task_directory/prompt.md`，而 canonical 操作布局的指令实际在 `task_directory/input/prompt.md`）。
- 修复：新增 `resolve_instruction_path()` 按“显式 `prompt_path` → canonical `input/prompt.md` → legacy flat `task_directory/prompt.md`”优先级回退，回退成功后回写修复 DB 中的 `prompt_path`；文件全部缺失时返回结构化 404 `HANDOFF_INSTRUCTION_MISSING`（固定作者可读文案）而非裸异常；前端透传后台真实 `error.message` 并在指令缺失时展示“交接指令不可用/重新准备初始化”状态。

**缺陷 2：字符串 readiness 导致全页面与 catalog API 400**

- 真实复现：`book-6k-0lnr4da` 初始化写入（`status.json` 中 `readiness` 为字符串 `"BLOCKED"`）后，所有 HTML 页面与 `GET /api/library/catalog` 均返回 HTTP 400。
- 现象：服务端 traceback 为对字符串做 `dict()` 转换崩溃（`library_catalog.py` 构建 Catalog/StudioReadiness 时假定 `readiness` 必为 dict）。
- 影响面：Catalog 被所有页面（书库、工作台、任务中心等）消费，单本书的字符串 readiness 即导致**全站页面渲染阻断**，包括本报告第 6–8 节描述的全部界面。
- 修复：`library_catalog.py` 对字符串/dict 两种 readiness 形态做防御性解析，`"BLOCKED"` 等字符串状态被正确识别为未就绪且不崩溃。

### 原结论修订对照

| 项 | 原结论 | 修订后 |
|---|---|---|
| 总结论 | 通过 | **不通过 → 修复已落地，自动测试证据充分；端到端/真实 Codex 证据：进行中（待补）** |
| 第 7 节 步骤 4（真实指令） | 通过 | 隔离目录通过；真实书库（legacy migrate 书）曾 live blocker，修复后待真实浏览器复验 |
| 第 7 节 步骤 5（Catalog/Readiness 轮询） | 通过 | 曾被缺陷 2 阻断，修复后待真实浏览器复验 |
| 第 8 节 D（真实指令） | 通过 | 降级：有条件通过（隔离目录），真实复验待补（blocker L-1） |
| 第 8 节 E（初始化处理与 READY） | 通过 | 降级：仅合同 fixture 级；真实 Codex 处理证据无（blocker L-2） |
| 其余 A、B、C、F、G | 通过 | 维持，但整体结论受 L-1/L-2 约束，不作为终验收依据 |

### 证据四分类（截至 2026-08-11，2026-08-11 证据回填后更新）

**a) 自动测试证据（已有）**

- 缺陷修复新增回归：`uv run --no-sync pytest -q tests/integration/test_handoff_instruction_reliability.py`：**14 passed**，覆盖 canonical/legacy flat/stale 绝对路径/空 prompt_path 回退与 DB 回写、指令全缺失 → `HANDOFF_INSTRUCTION_MISSING`、scope mismatch、缺失书库、前端错误透传契约、onboarding 页复制按钮与不可用态、Activity Center 指令可用性、字符串 readiness 不崩溃、`HANDOFF_NOT_FOUND`、回退优先级、`/health` 版本信息。
- 修复后全量回归：`uv run --no-sync pytest -q`：**210 passed**。
- 质量门禁：`ruff check src tests`、`mypy src`、`python -m compileall -q src`、`node --check`（`library_catalog.js` 等）、`novel web doctor` 均通过。
- 局限：均为进程内/TestClient 级验证，不等于真实浏览器与真实 Codex 行为。

**b) 真实浏览器证据（初次验收已有；2026-08-11 修复后端到端证据已回填，PASS）**

- 已有：初次验收的 9 张截图（`artifacts/library_onboarding/01–09`）与 A–G 浏览器操作记录（隔离目录）；缺陷 1 的真实故障现场（`cable-survival-demo`，HTTP 400 响应体与 traceback）。
- 2026-08-11 回填（PASS，截图目录 `artifacts/acceptance-browser/20260811-init-handoff/`，step1–step6 共 7 张）：Library 页发现候选（state=DISCOVERED）→ 点击“准备初始化”原子完成 ingest+initialize（`book_id=book-qombhi5tza`，`handoff_id=handoff_c3582f9ea417a15da6c7d45b`，state=INITIALIZATION_READY_FOR_CODEX）→ 任务中心显示 NOVEL_INITIALIZATION 条目（交接指令可用）→ 点击“复制给 Codex 的指令”：GET instruction 路由 200、content-length=1083，`navigator.clipboard.readText()` 读出 723 字符内容与服务端 `body.instruction` 逐字相同（CRLF 归一化后），包含 `$process-novel-handoff` 与 `$initialize-existing-novel`；页面反馈“给 Codex 的真实初始化指令已复制。”；静态资源全部 `?v=3.3.0`。
- 存量修复佐证：`cable-survival-demo` 失效 `prompt_path` 行经 `copy_instruction` 回退读取成功并自动回写 DB（instruction_available=true）。

**c) 真实语义执行证据（2026-08-11 已回填；非 fixture；执行主体限定如实标注）**

- 2026-08-11 回填：`handoff_c3582f9ea417a15da6c7d45b` 被真实领取处理，按 `.agents/skills/process-novel-handoff` 与 `initialize-existing-novel` 完整执行 Atlas-first 流水线：Source Coverage 10/10、1 arc、6 实体（1 个 UNRESOLVED_IDENTITY 为设计内保留）、2 MINOR 冲突 0 BLOCKING、Narrative DNA/World Model 基于真实剧情、400 条指标观测、Story Atlas 30 artifacts + 7 SVG、FAR 覆盖至第 24 章（≥要求的 20）；`result.json` status=COMPLETED、readiness=READY、canon_committed=false、edition_activated=false；`novel workflow validate-result` 通过；catalog API 最终 `book-qombhi5tza` state=READY、studio_ready=true、primary_action=OPEN_STUDIO。
- 执行主体限定（如实标注）：本次语义执行由开发代理在 Codex 桌面端合同下按 skill 执行——非合同 fixture，但执行主体不是作者手工操作的 Codex 桌面端会话，**不得称为“作者侧 Codex 桌面端执行”**。
- 本报告第 8 节 E 项使用的验收 fixture **仍不是**真实 Codex 初始化证据。

**d) 合同 fixture 证据（已有，明确局限）**

- 隔离 Library 中写入的符合现有初始化合同的验收 fixture（第 8 节 E 项）及相关集成测试。
- 局限：只能验证 Web/handoff/readiness 边界契约与门禁逻辑，不验证任何语义理解、Arc 分割、实体解析或世界模型质量；不得升级为真实初始化通过的证据。

**声明：不得把 fixture 称为真实 Codex 初始化。本次回填的真实语义执行虽非 fixture，但执行主体为开发代理（Codex 桌面端合同下按 skill 执行），不等同于作者侧 Codex 桌面端执行，二者如实区分。**

### Blocker 清单与解除状态（2026-08-11 证据回填后更新）

| ID | Blocker | 解除状态 | 证据出处 |
|---|---|---|---|
| L-1 | 真实书库（legacy migrate 书）复制交接指令端到端未复验 | **已解除（2026-08-11）** | 证据 b)：`artifacts/acceptance-browser/20260811-init-handoff/` step1–step6（真实书库端到端走通“发现候选 → 准备初始化 → 任务中心 → 复制指令”，剪贴板内容与服务端 instruction 逐字相同，含 `$process-novel-handoff`/`$initialize-existing-novel`）；存量修复佐证：`cable-survival-demo` 失效 `prompt_path` 行经 `copy_instruction` 回退读取成功并自动回写 DB（instruction_available=true） |
| L-2 | 无真实 Codex 处理 `NOVEL_INITIALIZATION` 至严格 `READY` 的证据 | **已解除（2026-08-11，含执行主体限定）** | 证据 c)：`handoff_c3582f9ea417a15da6c7d45b` 真实语义执行至 status=COMPLETED、readiness=READY，`novel workflow validate-result` 通过，catalog API book-qombhi5tza state=READY、studio_ready=true、primary_action=OPEN_STUDIO；执行主体为开发代理（非作者手工 Codex 桌面端会话），如实标注 |
| L-3 | 字符串 readiness 下全页面渲染的端到端复验 | **已解除（2026-08-11）** | 证据 b)：step1/step6 中 Library 页、任务中心与指令复制路径在真实书库（含初始化中书与字符串 readiness 存量书）正常渲染、无 400 |

**L-1、L-2、L-3 已全部解除。**

### 证据回填（2026-08-11）

本节在保留上方复审修订全部历史记录的前提下，回填三类新证据（详见“证据四分类”b/c 两节的更新内容与上方解除状态表）：

1. **真实浏览器端到端证据（PASS）**：截图目录 `artifacts/acceptance-browser/20260811-init-handoff/`（step1 至 step6 共 7 张），完整覆盖 L-1 与 L-3 的解除条件。
2. **真实语义执行证据（非 fixture）**：`handoff_c3582f9ea417a15da6c7d45b` 完整执行 Atlas-first 初始化流水线至严格 READY，解除 L-2；执行主体为开发代理在 Codex 桌面端合同下按 skill 执行，不得称为“作者侧 Codex 桌面端执行”。
3. **存量修复佐证**：`cable-survival-demo` 失效 `prompt_path` 行经 `copy_instruction` 回退读取成功并自动回写 DB（instruction_available=true）。

### 最终结论（2026-08-11 证据回填后）

**通过（含 2026-08-11 修复与真实端到端证据）。** L-1/L-2/L-3 blocker 全部解除；真实浏览器端到端（PASS）与真实语义执行（至严格 READY、canon_committed=false、edition_activated=false）证据齐备。限定性说明：本次真实语义执行由开发代理在 Codex 桌面端合同下按 skill 执行，非作者手工操作的 Codex 桌面端会话，本报告不声称“作者侧 Codex 桌面端执行”已完成；合同 fixture 仍不构成真实 Codex 初始化证据。
