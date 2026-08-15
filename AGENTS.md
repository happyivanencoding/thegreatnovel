## 1. 规范优先级

`Novel_Authoring_System_Constitution_V2.md` 是最高产品规范和长期不变量。

当前用户 / 当前任务可以指定 branch、文件、实现范围、测试范围和当前交付目标；
但不得被解释为静默取消 Constitution 的产品硬边界。若用户明确要求修改
Constitution 本身，则按该任务处理。

本 `AGENTS.md` 提供默认工程纪律；相关 skill、当前代码和历史 benchmark / audit
分别只在其适用范围内提供执行细节或证据。

---

## 2. Git / Agent 工作方式

不要永久绑定某一个开发分支。

- 当前任务指定分支时，只在该分支工作。
- 未指定时，继续当前 checkout 分支。
- 不擅自创建 branch、PR、merge 或 rebase；不得创建额外 worktree。
- Push 前确认当前分支、工作树和目标远端正确。
- 子代理不再限于只读审计或隔离 artifact。只要任务可以冻结输入、明确输出、划分文件/资源所有权并定义验收标准，任何任务类型都可以委派，包括代码实现、测试、文档、schema、Corpus 蒸馏、研究、验证和浏览器/CLI 操作。
- 子代理可以直接修改父任务明确授权的生产文件；主 Agent 负责拆解、依赖排序、冲突整合、最终验收，并负责最终 staging、commit 和 push。子代理不得擅自修改未授权文件、回退他人改动或提交 Git 历史。
- 并行优先按不重叠的写入集合和冻结的输入展开；不同类型的任务也可以并行，不要求它们属于同一种工作。共享文件、共享状态、顺序敏感的迁移、同一个 PGLite/SQLite 写入资源和互相依赖的任务必须指定单一 owner 或由主 Agent 串行处理。
- 委派任务必须自包含，写明上下文、输入、负责文件/资源、禁止触碰的边界、预期产物和验收标准。worker 完成后返回改动清单、验证结果和未解决问题；主 Agent 必须检查结果，不得把 worker 的完成声明直接当作验收结论。
- worker 可以运行任务所需的非破坏性命令和测试；不得输出或持久化 secret，不得删除数据库/lock，不得执行 Canon Commit、branch/merge/rebase、强制 reset 或未经授权的 push。需要这些动作时由主 Agent 根据当前任务显式执行。
- 如果多个 worker 无法安全并行，先检查当前生效的 `config.toml` 中 `[agents]` 的 `max_concurrent_threads_per_session`；若为 `1` 则串行处理，不为了并行擅自修改配置。并发额度允许时，优先把可独立推进的工作拆给多个 worker，以缩短端到端等待时间。
- 不为了并行而修改并发配置或制造多个开发分支。

---

## 3. 项目硬边界

- `book/` 原文永久只读。
- 新运行数据写入 `library/<book_id>/`，路径通过 `BookLayout`。
- `workspace/` 仅用于 legacy 读取和迁移，不作为新运行目录。
- `INFERENCE / CANDIDATE / PROSE_ONLY / SOFT_REFERENCE` 不得静默升级为 Canon。
- Draft 默认停在 `VALIDATED`。
- 未经作者当前明确批准，不得执行 Canon Commit。
- Story Atlas 是版本化软理解层，不是 Canon、Truth 或固定未来大纲。
- Revision 必须使用派生 Edition，不覆盖 base 或 `book/`。

---

## 4. Existing Novel Initialization

初始化原则：

> **Evidence-first, Progressive, capability-specific readiness**

`ingest` 只负责：

- immutable source
- chapters
- source spans

不等于初始化完成。

初始化不要求每次先做完整全文深分析。

应优先保证当前任务需要的能力，例如：

- Continuation Boundary
- 当前人物状态
- 当前资源 / 能力
- 当前知识边界
- 当前主要线程
- 当前世界规则
- 当前成长 / Narrative Drive 状态

证据不足时：

- 保持 `UNKNOWN`
- 或执行有界 Hydration

不要用抽样结果冒充全书事实。

具体初始化状态和 readiness 以当前代码为准，不在 AGENTS.md 固定枚举。

Readiness 按创作动作判断，不用一个全局状态替代所有能力：

- `CONTINUE_READY` 只要求当前安全续写所需的证据与边界完整。
- `CONTINUE_READY` 不要求 `FULL_READY`；历史语义仍可渐进补齐。
- Full Readiness 继续保持严格定义，不因某个动作已可用而放宽。

---

## 5. Deterministic / Semantic 边界

核心原则：

> **Facts are deterministic. Meaning is probabilistic.**

Python 负责：

- Source / Canon / State
- Boundary
- Schema
- Evidence
- Knowledge / Resource / Capability constraints
- Hard Gates
- deterministic metrics
- Approval
- Projection / Snapshot

LLM / Codex 负责：

- 文学理解
- Narrative interpretation
- Candidate creativity
- Draft prose
- semantic proposal
- uncertainty explanation

不要让 LLM 成为 Canon authority。

也不要让 Python 用大量机械规则替代文学判断。

---

## 6. Progression / Narrative Kernel

Narrative Drive / Progression Kernel 是语义与规划层。

它不得创建第二套：

- Canon
- World State
- Candidate Score
- Hard Gate
- Narrative Debt
- Payoff
- Approval

应把 Kernel Evidence 编译进现有：

- Hard Gates
- Progress
- Narrative Debt
- Resource Pressure
- Payoff
- Candidate Score
- Innovation Reward
- Scheduler

原则：

> **Kernel 负责告诉旧系统“该算什么”，旧系统继续负责“怎么算”。**

---

## 7. 验证与性能原则

本项目需要验证，但禁止重复验证和过度防御。

同一事实只在正确的权威边界验证一次；下游复用已冻结、已验证的结果。

任何检查前先回答：

1. 它检测什么具体失败？
2. 出现失败后系统会做什么不同动作？

答不上来就不要加。

保留真正改变行为的检查，例如：

- Schema validation
- Canon / Timeline / Knowledge
- Resource / Capability
- Author hard constraints
- Draft evidence
- Boundary freshness
- Author Approval
- Source immutable verification

避免：

- 同一事实反复验证
- 普通页面反复完整 Event Replay
- 已 VALIDATED Draft 在 Approval 时再次完整 Validation
- 已冻结 Planning Context 再次生成
- 无消费者的 hash / checksum
- 为不存在的情况增加 wrapper / compatibility layer / feature flag

性能是产品要求。

优先：

- materialized state
- snapshot
- incremental delta
- request 内复用
- lazy loading
- 避免 N+1 查询

---

## 8. Continuation / Batch / Revision

正式续写遵循：

`.agents/skills/continue-novel/SKILL.md`

必须经过：

`Boundary -> Candidate -> Chapter Contract -> Draft -> Validation -> Author Approval`

Batch 的具体 chunk / checkpoint 以当前 Skill 和任务配置为准，不在这里永久固定数字。

Batch provisional state 不得变成 Canon。

改写遵循：

`.agents/skills/revise-novel/SKILL.md`

---

## 9. Metrics / Rhythm

节奏和指标用于诊断，不是自动批准依据。

遵循：

- `.agents/skills/analyze-novel-rhythm/SKILL.md`
- `.agents/skills/review-novel-metrics/SKILL.md`

缺失证据保持：

`UNKNOWN / null / incomplete`

不要为了填满指标而伪造值。

WARNING 默认不是 Hard Failure。

---

## 10. Local File Handoff

遵循：

`.agents/skills/process-novel-handoff/SKILL.md`

当任务是一个已明确给出绝对 `library_root`、`book_id` 和 `handoff_id` 的标准单
handoff 时，默认委派给 `.codex/agents/novel-handoff-runner.toml`。只有子代理不可用、
父任务明确要求在当前会话执行或存在真实不可委派约束时，才由主会话直接执行；一次
Agent invocation 只处理一个 handoff。

Web 只负责：

- 创建 handoff
- 展示 handoff
- 读取结果
- 导入结果

Web 不得自行调用：

- Codex subprocess
- `codex exec`
- OpenAI API
- 自动 shell 执行 Codex

---

## 11. 测试与交付

开发中先运行相关测试。

完整改动完成后，再运行一次全量验证：

```powershell
uv run --no-sync pytest -q
uv run --no-sync ruff check src tests
uv run --no-sync mypy src
uv run --no-sync python -m compileall -q src tests
```

只有修改对应 CLI / Web 时才运行相关：

uv run --no-sync novel --help
uv run --no-sync novel web doctor
node --check <changed-js>

不要为了展示验收完整而反复运行与本次修改无关的检查。

Windows 中文路径需要重新安装时：

uv sync --python "C:\Users\jingx\anaconda3\python.exe" --extra dev --no-editable --reinstall-package novel-authoring-system

不需要每次小改动都重新安装。

## 12. 最终判断原则
对的就说对，不要为了审计硬找问题。
不为理论上的 corner case 增加工程复杂度。
不新增没有真实消费者的 Hash、Cache、Migration、Wrapper。
已经验证完成的东西，不要无理由重新验证。
能用现有系统解决，就不要创建第二套系统。

最终目标：

用尽可能少而清晰的机制，可靠地维护长篇小说的事实、状态、作者意图和连续性。
