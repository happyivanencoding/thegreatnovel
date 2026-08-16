# Findings & Decisions

## Requirements

- 新建并推送安全分支 `workflow-gate-simplification-v1`。
- 先创建可审计 Gate Inventory，再做最小实现。
- 只保留真实 Canon/Timeline/Knowledge/Resource/Capability/秘密泄露/身份/来源/审批/Edition 等硬门。
- 时间戳、路径、内部 ID、metrics、候选数量、KEEP_HIDDEN 回填、标点 evidence、软 Kernel、风格/重复/数量偏好等应归一化、自动推导、warning 或移到更早的业务 artifact 校验。
- 完成后停止，不自动启动十章实验。

## Research Findings

- 当前基线分支为 `reference-corpus-semantic-v1`，HEAD 为 `0bca63b docs: close experiment readiness audit`，远端为 `origin`。
- 已创建并推送 `workflow-gate-simplification-v1`，基于上述 HEAD。
- 工作树在本轮开始前已有 12 个 modified files 和大量 untracked experiment/runtime artifacts；其中 `planning/candidates.py` 当前反而仍有 `len(metric_rows) < 6` hard failure，`workflows/handoffs.py` 已有 Original artifact schema 校验的未提交改动。
- 当前 AGENTS.md 明确：`book/` 永久只读；Draft 默认 `VALIDATED`；未经作者明确批准不得 Canon Commit；Facts deterministic / meaning probabilistic；WARNING 默认不是 Hard Failure；全量验证命令固定为 pytest/ruff/mypy/compileall。
- Constitution V2 明确：Canon/Timeline/Knowledge 是硬事实边界；CandidateScore、metrics、Story Atlas、future route 不得代替作者或写入 Canon；正文必须有可观察后果；十项生成后校验继续存在，但严重问题不得自动写入正史。
- 引用任务的已知重点还包括 Reference Corpus：Revision Strategy 要从“拼接所有卡片”改为 bounded selection；machine bundle 必须校验 stored hash；Original executor 不得看到 provenance identity；Snapshot/readiness/soft-fail 保持；需要 Revision evidence chain 和 FINAL_CLOSURE。

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 先以只读搜索建立 gate-to-owner 映射，再派发不重叠实现任务 | 共享模型和 handoff 状态不能并发猜测，减少冲突 |
| 对现有未提交重叠文件先做 baseline diff 记录，必要时由主 Agent 串行整合 | 这些改动属于用户已有工作，不能由 worker 覆盖或回退 |
| 使用现有 schema/validator/service 作为权威，不新建第二套 Canon 或 migration/compat 层 | 符合 Constitution 和范围约束 |

## Issues Encountered

| Issue | Resolution |
|-------|------------|
| 工作树脏且与本轮范围重叠 | 已记录；后续按文件/行所有权处理，不清理或重置 |
| 引用回复超出线程读取单项 20,000 字符限制 | 已取得最新回复主体（0–24 节）；其可见内容足以冻结当前已知范围，后续以仓库代码与审计补齐，不假定不可见内容为新授权 |

## Resources

- `AGENTS.md`
- `Novel_Authoring_System_Constitution_V2.md`
- `src/novel_authoring/`
- `tests/`
- `audit/reference_corpus_system_integration/`
- `C:/Users/jingx/.codex/memories/MEMORY.md`

## Visual/Browser Findings

- 尚未执行真实 Browser 控制；不能把 TestClient 或 HTTP 200 冒充 Browser PASS。
