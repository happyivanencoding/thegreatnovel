# Novel Studio Library & Drop-In Book Onboarding 验收报告

验收日期：2026-08-11

分支：`小说续写_codex`

结论：**通过**

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
5. 页面每 10 秒重新计算 Catalog 与 StudioReadiness。变成 READY 时不突然跳页，而是显示“初始化完成”和显式“进入小说工作台”。

## 8. Browser Acceptance（127.0.0.1:8766）

| 项目 | 结果 | 证据 |
|---|---|---|
| A. Web 已打开后放入新文件 | 通过 | 10.5 秒内 Selector 与 `/library` 出现“新测试小说 / 待初始化”，无需重启服务 |
| B. 发现不写 DB | 通过 | 点击前 candidate 的 `book_id=null`；Registry 仍只有原 Ready Book；自动测试同时验证 Library 尚不存在 |
| C. 点击开始初始化 | 通过 | 浏览器真实点击后完成现有 ingest，并生成 `NOVEL_INITIALIZATION` handoff |
| D. 真实指令 | 通过 | 页面和任务中心均调用 book/edition scoped instruction endpoint；返回内容包含现有 `$process-novel-handoff` / `$initialize-existing-novel` 流程 |
| E. 初始化处理与 READY | 通过 | 在隔离 Library 中领取并置为 RUNNING；随后写入符合现有合同的验收 fixture，StudioReadiness 独立计算为 READY |
| F. 显式进入 Studio | 通过 | READY 页保持原地；点击“进入小说工作台”后才出现正文、世界状态、剧情规划、全书画像和连续性 |
| G. 多书切换 | 通过 | 最终 Selector 同时显示 2 本 Ready、1 本 Running、1 个 Pending candidate；Ready 书之间切换并恢复各自章节正常 |

说明：Browser Acceptance 的语义初始化结果使用隔离目录中的合同级 fixture，目的是验证 Web/handoff/readiness 端到端边界，不伪装成真实模型分析，也没有修改用户真实 source、Canon 或真实 Library。

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

- `uv run --no-sync pytest -q`：**192 passed**（201.21s）
- Library/Workbench 定向回归：**33 passed**
- 新增 onboarding 集成测试：**5 passed**
- `uv run --no-sync ruff check src tests`：通过
- `uv run --no-sync mypy src`：通过，148 个源文件零问题
- `uv run --no-sync python -m compileall -q src`：通过
- `node --check`（`library_catalog.js`、`workbench.js`）：通过
- `uv run --no-sync novel web doctor`：通过，新增路由完整
- `novel --help`、`features`、`rhythm`、`hooks`、`metrics`、`segments`、`workflow` 帮助命令：全部通过

新增测试覆盖：只读发现、支持/忽略格式、同名不同路径、registered source 去重、统一 Catalog、CSRF、现有 ingest、真实 handoff 类型与 prompt、未初始化路由门禁、不完整 COMPLETED 阻断、严格 READY 放行、Library/Selector 共源、10 秒轮询和任务中心状态。
