# Progress Log: Continuation Quality Generalization v1

## Session: 2026-08-16

### Phase 1 — Baseline and planning

- **Status:** in progress
- **Specific failure this phase detects:** whether the current tree already contains user-owned modifications, missing authority docs, an existing target branch, or prior planning state that would make a clean implementation unsafe or invalidate the requested evidence.
- **If detected:** preserve dirty files, read authority material from Git/history or audit bundle, isolate this plan, and do not run destructive repository commands.
- Read the referenced pasted text before continuing.
- Created the actual implementation goal after completing the thread's prior file-reading goal.
- Read and selected `planning-with-files`; ran session catch-up with no report.
- Read current branch/working tree and existing continuation-expansion planning files.
- Created `.planning/continuation-quality-generalization-v1/task_plan.md`, `findings.md`, `progress.md`, and this initial log; switched `.planning/.active_plan` to the new plan.
- Read `AGENTS.md`, `Novel_Authoring_System_Constitution_V2.md`, and `PLAN.md` from `HEAD` in full blocks because the working tree copies are deleted; confirmed `DESIGN_VALUES.md` and `MVP_REWRITE_SPEC.md` are absent from HEAD/history/branches.

### Checks run

| Check | Specific failure it detects | Result / next action |
|---|---|---|
| `git status --short --branch` | Dirty user work or wrong baseline could be overwritten or mixed into commits | Dirty tree confirmed; preserve and audit ownership before edits |
| `git branch --all` | Target branch/ancestry assumptions could be wrong | Target branch not listed locally; inspect remotes/merge-base before creating |
| `rg --files` for authority/planning docs | Required governance docs may be missing from working tree | Root docs absent/deleted in current tree; read Git/history and audit bundle |
| existing `.planning` inventory/read | Prior plan may contain unsynced context or overlap | Existing plan belongs to previous continuation-expansion task; do not treat as acceptance evidence |
| `git show HEAD:AGENTS.md`, Constitution, `PLAN.md` | Product hard boundaries could be violated by the new abstractions | Read and recorded single Event Store/Projection, author approval, type-config, book read-only, and LLM/Python boundary |
| Constitution line-block reads | Long authority file could be partially omitted by output truncation | Read by numbered blocks through line 1506; architecture decisions must follow it |
| `rg` production anti-overfitting baseline | Current experiment may be hard-coded in production or fixed-window logic may already exist | No direct story-specific or obvious fixed-window hits; inspect model defaults and dynamic horizon wiring |
| approval UI/route inventory | Chapter approval may be blocked in browser or absent for continuation; shared server gate might be bypassed | Shared `approve_draft` gate exists; Original delegates to it; continuation Web POST/button is missing and Original/workbench JS still has blocking confirms |

### Errors encountered

| Error | Attempt | Resolution |
|---|---:|---|
| `create_goal` rejected because an unfinished read-file goal existed | 1 | Inspected with `get_goal`, marked that completed objective complete, then created this implementation goal |

### Next action

Inspect current live source/test/UI entry points. Before each search or test, add its failure target and consequence here.

### Planned read-only inventory

- **Specific failure to detect:** the proposed abstractions may already exist under different names, or their real authority/approval path may differ from the pasted task's suggested directories.
- **If detected:** extend the existing model/service/route at its actual ownership boundary; do not create duplicate modules or infer behavior from filenames alone.

### Baseline anti-overfitting search

- **Specific failure to detect:** current production `src/`/`config` may already encode the experiment's book id, title, names, prop names, measurement values, or fixed ten-chapter rules.
- **If detected:** remove or relocate only the real production special case into fixture/benchmark scope, then replace it with contract/projection/type-driven logic; if no hit, retain the clean baseline as evidence.

### Approval UI inventory

- **Specific failure to detect:** any first-chapter, continuation, revision, batch or candidate approval path may still invoke browser-blocking confirmation or use divergent approval semantics.
- **If detected:** route every affected click to the existing server approval boundary, remove only the blocking prompt, and add inline failure/success state without bypassing stale-bundle or transaction checks.

### 已完成的边界审计

| Check | 具体失败 | 失败后的不同动作 | 结果 |
|---|---|---|---|
| Canon materialization seam | 新 claim/usage 若需要独立表或绕过 EventStore，会产生第二事实源 | 改为复用 DraftStateChange payload 与现有 materialize/Projection | 已确认可复用 |
| Legacy pseudo-score audit | COMPILED_SOFT 仍写入固定人物/文风分数，会制造不可解释评分 | 删除 compiler 的 pseudo inputs；输出测量与 UNKNOWN 语义状态 | 已定位 `compiler.py`、`validators.py`、`metrics/gates.py` |
| Reference provenance audit | selected card 被误当作已应用 | 增加 offered/applied/rejected 状态并保留 snapshot provenance | 已确认当前缺失 |
| Fixed-window audit | 章节体验仍固定取 5，Boundary 默认固定最近 3 章 | 引入配置/合同驱动的 history policy，避免 story-specific window | 已确认当前存在 |

## 下一步实现验收

- 先用跨家族 unit fixtures 验证 survival/resource、combat/cultivation、mystery/relationship 三种 payload 只依赖 generic fields；若 fixture 必须写某家族实体名，则退回模型设计。
- 对每个 targeted check 先记录预期失败与处置，再运行；最小验证集合包括模型 round-trip、usage reset semantics、structural overlap、compiled-soft score absence、approval route response。

### 第一组生产改动后的定向检查

- **具体失败：** 新增 continuation-quality models、Draft 字段和 validator/compiler 接线可能有 Python 语法、import cycle 或 Pydantic schema 错误。
- **如果失败：** 只修复这组模型/接线的最小错误，不进入 UI 或 branch 提交；旧字段仍保留默认值。

- **具体失败：** 运行级模型/纯函数 smoke 可能暴露 Pydantic 默认值、枚举序列化、reuse/upgrade 判定或 usage reset 语义错误。
- **如果失败：** 修复对应通用函数并补 unit fixture；若结果通过，再进入 integration/compiler 接线检查。

| Runtime smoke | system Python 未安装当前 `src` package，无法判断模型运行结果 | 用仓库 `src` 加入 `PYTHONPATH`（后续正式测试优先使用项目 venv/uv），不把环境错误当成代码结论 | 首次运行环境失败，待重跑 |
| Runtime smoke assertion | smoke 脚本把合法的 ONE_TIME 第一次使用误写成“应报错” | 修正 fixture 为 `used_before=1` 的第二次使用，保持实现语义：首次使用不报错，超额才报错 | 测试脚本错误，非实现结论 |

### 结构/窗口/基线接线检查

- **具体失败：** structural overlap、reference status、无窗口 experience history 或无历史 realization baseline 可能破坏现有候选/合同序列化或旧 planning tests。
- **如果失败：** 保持模型字段可选，修复实际调用方；不恢复隐含固定窗口、不把无历史强行填成全局字数基线。

| Structure/reference smoke | Pydantic `after` validator 返回 `model_copy`，初始化时不会替换顶层实例，`card_ids_used` 没有变成 OFFERED | 直接在可变模型实例上设置 application_status 并返回 self；不依赖 validator 返回副本 | 已定位，待修复后重跑 |

### 现有 continuation regression

- **具体失败：** 旧 continuation expansion tests 可能仍断言 pseudo Character/Style inputs 或固定 realization range，暴露需要同步更新的产品契约，而非隐藏回退。
- **如果失败：** 更新测试断言到 deterministic measurements/UNKNOWN baseline；若是旧数据反序列化失败，则修复可选字段接线。

### Approval UI 接线检查

- **具体失败：** 页面可能仍含 `window.confirm`，draft review 可能没有 page-native POST，或新增 template/static 引用无法加载。
- **如果失败：** 只修 shared approval.js、模板和 route；保留 `approve_draft` 的显式短语、stale 检查、事务和 Canon 写入边界。

### Cross-family fixtures

- **具体失败：** 新 kernel 可能只对 resource/战斗字段有效，或三类 family 需要不同算法/固定实体名。
- **如果失败：** 抽出仍然通用的 subject/axis/period 字段；不新增 genre-specific production code。

| Cross-family collection | 测试文件从另一个测试模块导入 fixture，但仓库没有 `tests.unit` package | 将合同 fixture 本地化为通用 `ChapterContract.model_construct`，不改变 production code | 测试组织错误，已修复，待重跑 |
| Cross-family assertion | fixture 将有完整 before/after 的 UPGRADE 错误地当成不完整 | 改为测试 REUSE 改变状态、以及 BREAKTHROUGH 缺少行动空间；完整 UPGRADE 应通过 | 测试断言错误，非实现结论 |

- `test_continuation_quality_generalization.py`: **9 passed**，覆盖三类 family、usage reset、progression distinction、renamed structural overlap、reference offered/applied、compiled-soft 与 no-history baseline。

- **具体失败：** reader-visible claim 可能只在模型层 round-trip，未真正比较 Projection before state。
- **如果失败：** 修复 `validate_canon` 的 direct projection lookup 或 fixture；不把 prose 解析扩展成自然语言事实推断。

- Projection before-state continuity test passed; cross-family file now **10 passed**。

### Serial Experience Portfolio check

- **具体失败：** portfolio 可能仍使用隐藏默认窗口/固定 horizon，或合同无法携带结构历史。
- **如果失败：** 修复 `experience_portfolio.py`、Settings policy 或 contract metadata；不增加第二套 rhythm/debt 数据库。

- Serial portfolio + related continuation tests: **19 passed**。

### Static UI syntax check

- **具体失败：** approval.js/original.js/workbench.js 可能有 JS 语法错误，导致非阻塞按钮根本无法执行。
- **如果失败：** 只修静态脚本语法/未使用变量，不改变 API payload 或 server approval semantics。

- Node `--check` for approval/original/workbench scripts: **passed**。

### Anti-overfitting and fixed-window scan

- **具体失败：** production/config could still contain current-story identifiers, pseudo-score constants, or hidden fixed chapter-window defaults.
- **如果失败：** remove only story-specific code or move it to fixtures; replace hidden windows with explicit config/contract policy. Leave legitimate generic test thresholds and persistence query limits alone.
- Scan found no current-story identifiers or experimental title/prop/measurement matches. It found the remaining global `Settings.recent_full_chapters=3` default, which is now being removed in favor of an unset/all-history default; explicit callers/tests may still provide a configured window.

### Shared approval route smoke

- **具体失败：** new continuation route may not be mounted, may omit CSRF, or may bypass the shared workflow when the draft is missing.
- **如果失败：** fix route wiring and error handling; the missing-draft response must remain a workflow error and no Canon event may be written.

### UI/route regression run

- **具体失败：** 现有 web app import、draft review template 或 workbench/original integration 可能因新 schema/route 导入而失败。
- **如果失败：** 修复 import/template context 或测试 fixture；不让 UI 直接调用 materialize/EventStore。

- `test_continuation_expansion_v1.py`, progression family/consistency, metric gates and `test_authoring_workbench.py`: **39 passed**。
- 这次回归先暴露并修正了旧测试对 pseudo Character/Style inputs 的断言；现已改为验证 `{}`、`semantic_review_status=UNKNOWN` 和 deterministic measurements。

### Shared approval route smoke result

- 第一次冒烟脚本错误地从 `novel_authoring.storage` 导入 `Database`；真实定义在 `novel_authoring.db.database`。这是检查脚本的导入错误，不是路由结论。
- 第二次脚本在未初始化 SQLite schema 时创建 app，暴露的是冒烟 fixture 缺少 `db.initialize()`；补初始化后重跑。
- **结果：通过。** 未携带 CSRF 时 `POST /api/books/demo/editions/base/drafts/draft/approve` 返回 `403 CSRF_INVALID`，说明新路由没有绕过共享 CSRF 边界；由于请求在 workflow 前被拒绝，不会写入 Canon。

### Generic gap-fix targeted check

- **具体失败：** 新增通用字段别名、ending action、Publication Boundary、Reader-visible 冲突码、跨题材 Usage/Progression 测试或 Contract underspecified 分支可能破坏 Pydantic round-trip、旧 Draft 编译或既有 validator。
- **如果失败：** 只修实际失败的模型/validator/fixture 接线；不恢复故事专有字段、不把语义判断改成 Python 关键词推断。

- **结果：通过。** `tests/unit/test_continuation_quality_generalization.py` 与 `tests/unit/test_continuation_expansion_v1.py` 共 **29 passed**；覆盖四种周期约束、跨家族 alias、结构非重复、Reference unavailable/zero-results、Publication Boundary、数量来源、复用不推进 index、Contract underspecified。

### Post-gap wiring regression

- **具体失败：** Reference status 保留、Serial Portfolio 的 underserved 字段、healthy realization baseline 查询和新增 publication metadata 可能造成导入错误、schema 校验错误或旧 continuation 行为变化。
- **如果失败：** 回退到最小字段/调用方修复；保留现有 Canon/Approval 边界，不添加第二个状态存储。

- **结果：通过。** 两个定向 continuation 文件共 **29 passed**。

### Shared approval integration check

- **具体失败：** 页面统一组件可能只通过静态扫描，却在实际 FastAPI 路由上绕过 CSRF、把缺失草稿当成功，或产生 Canon event；同一检查也确认 Original/continuation 页面都加载共享 approval.js 且没有阻塞确认调用。
- **如果失败：** 修复实际路由或模板接线；缺失草稿必须返回 workflow error，事件计数保持不变，绝不在测试中跳过作者批准。

- **结果：通过。** `tests/integration/test_continuation_quality_web.py`: **2 passed**；有效 CSRF 的缺失草稿返回 `WORKFLOW_ERROR`，Canon event 数量不变，页面脚本共享 `approval.js` 且无 `window.confirm`。

### Realization baseline check

- **具体失败：** 健康基线查询若把 `SCENE_REALIZATION_THIN` 或未接受的短章混入，会继续压低后续章节的自适应范围；Contract 过小若只返回 thin，也会错误进入补字数路径。
- **如果失败：** 只调整健康样本筛选或 underspecified 分支；不增加统一最低字数，不让章节数阈值替代当前书的健康历史。

- **结果：通过。** 通用质量 unit suite: **22 passed**；thin/未接受短章不会进入 baseline，显式接受的短章可作为健康样本。

### Configured-horizon cross-family experiment

- **具体失败：** Portfolio 若隐含使用固定章节数、只对生存/资源字段有效，或跨过当前配置的 NEAR/SHORT horizon 后仍不能比较结构，就不能证明通用性。
- **如果失败：** 修复 portfolio 的配置读取、结构签名或参数化 fixture；不把某一实验书的章数写回生产代码。

### Current Seed artifact rehydration check

- **具体失败：** 既有十章 Seed 的只读 SQLite/草稿 artifact 若不能按新增 Draft/Contract schema 重新读取，说明本轮字段不是可选接线；同时核对 Canon commit、validated draft 与历史 thin/continuity evidence 的数量基线。
- **如果失败：** 只补旧 artifact 的可选字段读取或记录明确迁移边界；不修改 Seed 的 `book/`/Canon，也不把其专有实体写入生产代码。

- **结果：通过。** 只读读取既有 Seed `_system/state.sqlite3`：`CANON_COMMITTED=10`、保留 `DRAFT=2`、Canon commits **10**、validation reports **120**；10 个 DraftOutput 与 10 个 ChapterContract 均可按新 schema rehydrate，`schema_failures=[]`。该检查没有写回 artifact。

- **纵切结果：通过。** 从 `config/default.yaml` 读取 SHORT=12，并对 survival/resource、combat/cultivation、mystery/relationship 各生成 13 个 generic signatures、`current_chapter=14`；三组均为 `SHORT=12, MID=1, UNKNOWN=0`，结构比较均识别 78 对同构样本。该结果证明 horizon 来自配置和同一 portfolio 函数，不证明任何新正文的文学质量。
- **盲读边界：** 本轮没有重新生成匿名盲读正文；新 artifact 明确引用既有 Seed 盲读报告，不伪造新的盲读结论。

### In-app browser smoke

- **具体失败：** 实际服务页面可能仍加载旧 bundle、共享审批按钮缺失、Original/continuation 页面触发 JS dialog，或 draft review 不能从真实 artifact 渲染审批状态。
- **如果失败：** 只修页面/template/static bundle 或服务启动 fixture；不在浏览器中点击批准、不改变测试数据库 Canon，保留服务端 approval/CSRF/stale 边界。
- 首次启动浏览器 smoke server 时 `.venv` 的 site-package 读取因 Windows 默认 GBK 解码工作区路径失败（`UnicodeDecodeError`）；这是运行环境错误，不是 Web 路由结论。下一步只切换 `PYTHONUTF8=1` 重启，不修改代码或依赖。
- 之后用系统 Python 从临时英文路径启动时，8765 端口被 Windows 返回 `WinError 10013` 拒绝绑定；这仍是 smoke 环境端口冲突/权限问题，改用新的本地端口，不调整 Web 实现。
- **结果：通过。** 系统 Python 在临时副本上以 `127.0.0.1:8877` 启动实际 FastAPI 页面；原始 seed 页确认加载共享 `approval.js`、无 `window.confirm`。因原始副本的草稿均已 `CANON_COMMITTED`，先用临时副本把一条草稿标成 `VALIDATED`，刷新后实际页面出现“批准写入正史”按钮（1 个 `[data-approval-action]`），仍无浏览器 JS dialog；未点击按钮，未改变仓库或实验 seed。

### 修改文件 Ruff

- **具体失败：** 本轮新增/修改的 Python 文件可能存在 import 顺序、未使用变量或新通用模块自身的 lint 错误。
- **如果失败：** 只修本轮新增或接线造成的 lint 问题；不顺手清理无关既有 lint 债务。
- 新增 `continuation_quality.py`、`planning/experience_portfolio.py`、`validation/publication_boundary.py`：Ruff **通过**。接线文件的输出包含若干既有 `ISC004/TRY/BLE` 债务；已修复本轮新增的 `ReaderVisibleClaim` 未使用 import 和 `state_change_ids` 未使用变量，未对无关债务做大范围格式化。

### 定向 mypy

- **具体失败：** 新增模型字段的 Literal 推断或可选 StateChange 绑定可能让严格类型检查失效。
- **如果失败：** 为本轮字段补准确的 Literal/None narrowing；不放宽全局类型策略。
- 第一次严格定向检查发现 3 个真实类型错误：`contract_realization_status` 被推断为 `str`，以及两个可选 `transition.payload` 访问；已分别补 Literal 注解和显式空值收窄，等待重跑。
- **结果：通过。** 使用同一 `.venv` 的 Python 3.11 `-S` 模式、严格选项和 `ignore-missing-imports` 对 10 个本轮涉及的生产模块检查，`Success: no issues found in 10 source files`。

### compileall

- **具体失败：** 本轮修改的 Python 文件可能存在语法错误或导入阶段无法编译的代码，导致服务/测试在运行前失败。
- **如果失败：** 只修语法或直接导入错误，然后重跑受影响模块。
- **结果：通过。** Python 3.11 `compileall -q` 对完整 `src/novel_authoring` 无输出、退出码 0。

### Final targeted regression

- **具体失败：** Literal/None narrowing、ending-action 结构字段、Reader-visible validator 和非阻塞审批接线的最后修改可能回归跨家族质量测试或旧 continuation contract。
- **如果失败：** 只修实际回归；不降低断言或跳过对应 family。
- **结果：通过。** 通用质量、旧 continuation expansion、共享审批 integration、progression family/consistency、metric gates 和 authoring workbench 定向集合共 **63 passed**。

### Full pytest

- **具体失败：** 全部现有单元/integration/contract 测试中可能有本轮数据模型、审批边界、UI route 或 production import 的跨模块回归；这也会区分 dirty worktree 中已删除根文档造成的既有失败。
- **如果失败：** 先按 traceback 判断是否触及本轮代码；修复本轮回归，既有基础设施/脏工作树问题只记录准确证据，不伪称全绿。
- 第一次全量运行（从临时英文工作目录启动以绕过 venv site 的 GBK 问题）为 **558 passed, 1 skipped, 4 failed**：其中 1 个是旧测试仍要求已移除的 pseudo `character_fit_inputs`，已改为断言空 score、`UNKNOWN` 与确定性 measurements；2 个原始小说测试只是相对路径因临时工作目录失败；1 个读取当前已删除 `AGENTS.md` 的测试对应既有 dirty worktree 删除。下一步从仓库工作目录用 `-S` 模式重跑，区分这三类原因。
- 仓库工作目录复核的 4 个失败中，已修正的 pseudo-score 测试和两个 Original 测试均通过；剩余唯一失败仍是工作树中预先删除的 `AGENTS.md`，不是本轮代码。当前证据为 **3 passed, 1 pre-existing missing-file failure**。
- **全量复跑具体失败目标：** 需要确认修正后的 pseudo-score 断言和 Original 页面文案不再导致其它测试回归，同时准确记录唯一的根文档缺失失败。
- **如果失败：** 只修本轮代码/测试回归；若仍只有 `AGENTS.md` 缺失，则保留工作树改动并报告该基础设施阻塞。
- **结果：** 从仓库工作目录用 Python 3.11 `-S` 模式完整运行 **562 passed, 1 skipped, 1 failed**。唯一失败是 `tests/integration/test_library_hardening.py::test_agents_rejects_worktree_creation_instruction` 读取当前 dirty worktree 预先删除的 `AGENTS.md`；本轮相关测试和其它全套测试均通过，未恢复该用户删除文件以保持工作树边界。

### Full-source mypy

- **具体失败：** 仅检查 10 个模块可能遗漏其它生产模块被新模型/配置导入后的类型回归。
- **如果失败：** 按错误是否由本轮 import/schema 变化引起修复；既有无关类型债务单独记录，不修改无关模块。
- **结果：通过。** 同一 Python 3.11 `-S` 环境以严格选项检查 `src/novel_authoring` 共 **203 source files**，无类型错误。

### Project-select Ruff on modified files

- **具体失败：** 本轮修改文件可能违反项目原有 `E,F,I,UP,B,SIM` 规则，尤其是新增 import 接线和语法结构。
- **如果失败：** 只修本轮修改文件中的实际 lint 问题；不启用当前环境额外的全局规则集，也不清理未涉及文件。
- 运行项目原有规则集（`E,F,I,UP,B,SIM`，line length 100）后第一次只剩本轮长行和 import 排序问题；已修复后复跑，结果 **All checks passed**。期间没有按当前工作环境额外启用的 `ISC/TRY/PLW/RUF` 规则去清理既有债务。

### Post-static targeted rerun

- **具体失败：** 最终格式化和 UI 文案改动可能破坏通用 quality tests、旧 continuation regression 或审批 route integration。
- **如果失败：** 只修最终改动造成的断言/导入回归；不重新引入阻塞确认或 pseudo score。
- **结果：通过。** 最终静态修订后同一组定向测试仍为 **63 passed**。

### Generic boundary gap tests

- **具体失败：** `WORLD_STATE`、位置/所有权/时间状态的无 transition 冲突，或 Reference evidence 不来自冻结 card 时，通用层可能静默放行；这会直接削弱跨题材 continuity 和 Reference applied 语义。
- **如果失败：** 只扩展共享 claim/status 校验与冻结 card evidence 核对；不添加故事专有关键词或第二套状态存储。
- **结果：通过。** 通用质量与旧 continuation 单元回归共 **34 passed**；新增覆盖 `WORLD_STATE`、位置/所有权/时间 reset 冲突和冻结 card evidence 正/反例。

### Post-boundary mypy and compileall

- **具体失败：** 新增 Reference evidence helper、扩展 claim enum 和 generic conflict mapping 可能引入类型或语法错误。
- **如果失败：** 只修这次边界扩展的类型/语法接线。
- **结果：通过。** 全源严格 mypy 仍为 `Success: no issues found in 203 source files`；完整生产源码 `compileall -q` 退出码 0。
- 边界扩展后的核心修改文件按项目规则集 Ruff 复跑：**All checks passed**。
- 增加 Projection subject/Contract 边界后，专门的 quality unit suite 为 **26 passed**；随后核心修改文件 Ruff 仍为 **All checks passed**。

### Final cross-module targeted rerun after boundary expansion

- **具体失败：** subject existence/Contract-scope checks、Reference evidence verification 或新增 UI assertions 可能回归原有 progression/metric/workbench 行为。
- **如果失败：** 修复真实跨模块回归；不删除通用冲突断言或放宽审批边界。
- **结果：通过。** 最终跨模块定向集合共 **67 passed**，包括新增 26 项 quality tests、旧 continuation、共享审批 integration、progression/metric/workbench 回归。

### Final full pytest after generic boundary expansion

- **具体失败：** 最终 `WORLD_STATE`/subject/Contract/Reference changes 可能影响全仓所有 validators、draft approval、Original 和 workbench fixtures。
- **如果失败：** 根据 traceback 修复本轮回归；仍将当前工作树预先删除的根文档失败单独列出，不恢复用户文件。
- **结果：** 最终全量运行 **566 passed, 1 skipped, 1 failed**。唯一失败仍为 `test_agents_rejects_worktree_creation_instruction` 读取当前 dirty worktree 预先删除的 `AGENTS.md`；generic boundary expansion 没有引入其它全仓回归。

### Global approval UI scan

- **具体失败：** 第一章、续写 Draft Review、修订或 Canon 写入路径仍可能调用浏览器 `confirm()`，或将审批入口藏在阻塞式对话框/遮罩中。
- **如果失败：** 将对应章节审批入口接到共享 `approval.js`，保留页面内反馈和服务端 CSRF/stale/transaction 校验；不改动与章节审批无关的资料库导入/删除对话框。
- `src/novel_authoring/web/static` 与 `web/templates` 扫描结果：`window.confirm`、裸 `confirm(`、审批相关阻塞弹窗词均 **无命中**。剩余 `<dialog>`/`data-confirm-delete` 仅属于资料库导入/删除；`data-confirm-progression-contract` 是直接接受成长合同建议的按钮，不是 Canon/章节审批确认。

### Pre-commit staged-scope check

- **具体失败：** 暂存区可能混入用户既有混合 hunk、根目录删除或实验/缓存产物，导致本次代码提交越界。
- **如果失败：** 仅用逐 hunk staging 移除越界内容；不恢复或覆盖用户工作树。
- **结果：** 暂存区只包含本轮通用质量内核、规划/校验接线、共享审批 UI、相关测试与路由；`app.py`、`original.js`、`original_studio.html` 中的既有混合 hunk 留在未暂存区。根文档删除、运行库、benchmark、缓存和其他用户改动均未暂存。

### Pre-commit whitespace check

- **具体失败：** 本次 staged patch 可能包含尾随空白或空白错误，导致代码提交不可复现或触发 CI 检查。
- **如果失败：** 只修复 staged 本轮文件中的空白问题，然后重新检查；不触碰未暂存用户改动。

### Artifact staged-scope and whitespace check

- **具体失败：** 工件暂存区可能遗漏本轮审计证据，或混入其他实验目录；工件文本也可能有尾随空白。
- **如果失败：** 只调整 `.planning/continuation-quality-generalization-v1`、active plan 和本轮实验报告的暂存范围/空白，不修改其他工作树内容。

### Pre-push Git delivery check

- **具体失败：** 当前分支、远端、merge-base 或两次提交的归属可能与目标不一致，导致推送到错误分支、覆盖已有远端分支，或无法证明代码/工件分离。
- **如果失败：** 停止 push，修正分支/暂存/提交关系后再检查；不执行 force push，不改写远端历史。
- **结果：** 当前分支为 `continuation-quality-generalization-v1`；`origin` 为项目远端；同名远端分支此前不存在；代码提交为 `804ddff`、工件提交为当前 HEAD 的前一提交；`merge-base(origin/main)` 为 `a9945fb`；普通工作树仍有 359 个本轮前已存在或独立实验状态项，未进入本轮提交。

### Post-push remote verification

- **具体失败：** push 可能没有把本地目标分支完整发布，或误留下 staged 内容/混入错误文件边界。
- **如果失败：** 只重新核对目标分支与提交边界；若远端缺失则重试普通 push，若边界异常则停止交付并保留证据。
- **结果：** `origin/continuation-quality-generalization-v1` 与本地 HEAD 同为 `36e159b`；staged entries 为 0；代码提交和工件提交文件集合分别独立；工作树 359 项未被本轮交付触碰。
