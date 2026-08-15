# Reference Corpus / GBrain Integration Closure Review

日期：2026-08-15
分支：`reference-corpus-semantic-v1`

本轮只修复“已接线但未真正消费”的结构问题。Reference Corpus 仍是
`REFERENCE_ONLY` 软知识，不参与 Canon、事实、Impact scope、Author Intent、Hard Gate、
Approval 或 Canon Commit。

## 证据边界

当前运行环境的 `NOVEL_REFERENCE_CORPUS_ROOT` 未配置。因此以下闭环证据使用 pytest
`tmp_path` 创建的 disposable machine package；它证明接口和调用链，不冒充生产 Corpus
证据。当前会话没有可用的 browser control 工具，`REAL_BROWSER=BLOCKED`；没有伪造浏览器、
生产 book 或 task 证据。

最终修复后的实际验证结果：targeted closure matrix `107 passed`，full pytest `498 passed`，
Ruff `All checks passed`，mypy `Success: no issues found in 197 source files`，compileall
成功，source-tree web doctor 成功（API health `200`、missing routes 为空）。当前没有
browser control，`REAL_BROWSER=BLOCKED`；生产 Corpus root 未配置，因此生产 package
live proof 保持 `PARTIAL`，没有把 disposable evidence 冒充生产证据。

## Issue A — Revision Planning 先决定 HOW，再生成 Strategy

**Previous behavior**：RevisionUnit 已写入后才查询 PLANNING，Reference Context 更像计划
完成后的附加 metadata；即使 selected cards 存在，也没有明确的可消费 Strategy。

**Root cause**：Revision planner 没有把 deterministic Impact/Audit 和 Reference PLANNING
之间的边界固化为 `RevisionStrategy` 合同。

**Fix**：`build_revision_plan()` 先完成 deterministic Impact → Audit → RevisionUnit，随后
查询冻结的 PLANNING context，再从 selected mechanism/contrast/synthesis cards 编译
`RevisionStrategy`。Strategy 只描述结构动作、读者效果、保留方式和失败模式；其
`reference_card_ids_used` 强制是 frozen `selected_card_ids` 的子集。

**Files changed**：

- `src/novel_authoring/revision/models.py`
- `src/novel_authoring/revision/service.py`
- `tests/integration/test_revision_workflow.py`
- `tests/integration/test_reference_corpus_closure.py`

**Regression test**：Revision Impact 阶段 spy 的 Query 次数为 0；完成 Impact Audit 后，
PLANNING selected cards 进入 Strategy，再进入 Draft task。

**Final status**：`PASS（disposable machine package；production root 未配置）`。

## Issue B — Revision Query metadata 自动来自当前书

**Previous behavior**：reader experience、narrative drive、payoff channel 和 creative
problem tags 主要依赖 `RevisionSpec.style_policy` / `completion_policy`，普通作者不填
这些字段时查询维度会丢失。

**Root cause**：Revision 没有统一读取 Effective Contract payload，也没有把 target chapter、
rhythm、narrative debt、payoff 和 Impact 状态适配到 Corpus 已存在的 controlled tags。

**Fix**：从 `effective_contract_records()` 的真实 `ContractRecord.payload` 读取三类有效
合同；显式 RevisionSpec metadata 只作 augment。新增有界 deterministic adapter，使用当前
Corpus 已出现的 `breakthrough`、`power-verification`、`resource-release`、
`world-expansion`、`exploration`、`mystery-reveal`、`relationship`、`long-form`、
`post-payoff-anticipation`、`fatigue` 等标签；没有可信状态映射时不伪造标签。

**Files changed**：`src/novel_authoring/revision/service.py`；对应 Revision integration
tests。

**Regression test**：真实 Effective Reader/Narrative/Payoff contracts 在 Revision Query
中产生非空 metadata；planning inputs 同时保留实际章节 scene functions，且不依赖作者
手写 tags 才能得到 derived controlled tag。

**Final status**：`PASS`。

## Issue C — Original Reader Experience 使用 payload

**Previous behavior**：Effective contract wrapper 的 `model_dump()` 被当作业务 payload，
导致 Original PLANNING 查询可能读不到 `experience_priorities`、primary experience 等
真实字段。

**Root cause**：`ContractRecord.payload` 与外层 record 混用。

**Fix**：统一 contract extraction：优先读取 `ContractRecord.payload`，再规范化为
Original、Continuation、Revision 各自的 Reference Query fields；不把 wrapper metadata
误当作 Reader Experience 内容。

**Files changed**：`src/novel_authoring/original/service.py`、
`src/novel_authoring/planning/candidates.py` 及 Original integration tests。

**Regression test**：真实 Effective Reader Experience contract payload 进入 Original
PLANNING Query，`reader_experiences` 非空且与 payload 一致。

**Final status**：`PASS（payload extraction code path）；完整 browser Genesis 仍受环境限制`。

## Issue D — Continuation 使用真实 state-derived creative problem tags

**Previous behavior**：Continuation 有自然语言 `creative_problem`，但没有稳定真实上游的
`creative_problem_tags`，检索无法使用当前故事状态。

**Root cause**：Query metadata 没有从冻结 Boundary/Story State、Narrative Portfolio、
payoff readiness、resource pressure、world expansion、relationship、mystery 和 repetition
诊断编译。

**Fix**：在 `planning/candidates.py` 中从当前冻结 state 读取并只输出 Corpus 已存在的
controlled tags；自然语言问题继续只作人类说明。Reader Experience、Narrative Drive、
Payoff Channel 仍作为独立维度。

**Files changed**：`src/novel_authoring/planning/candidates.py` 及 Continuation tests。

**Regression test**：disposable Continuation task 有 active thread、压力/回报/资源等
state 时，Query 至少包含一个 state-derived tag，并且 compact planning cards 到达
Candidate prompt。

**Final status**：`PASS（disposable continuation task）`。

## Issue E — Query Gateway 强制 machine readiness

**Previous behavior**：Gateway 主要检查路径、文件和 schema，可能在 semantic package
尚未 `query_ready` 或带有 raw text 时继续返回 cards。

**Root cause**：semantic compile 的 readiness 没有成为 retrieval 前的 hard input check。

**Fix**：查询前验证 `schema_version`、`status=REFERENCE_ONLY`、`query_ready=true`、
`raw_text_included=false`；不满足时返回现有 `UNAVAILABLE` soft status、明确 readiness
warning/knowledge gap 和空 cards，不新增全局状态枚举。PLANNING 不返回 prose-control，
PROSE 不返回 mechanism/contrast/synthesis。

**Files changed**：`src/novel_authoring/reference_corpus/query.py`、相关 unit/closure tests。

**Regression test**：`query_ready=false` 与 `raw_text_included=true` 均无 cards、状态不是
`ENABLED`、原因可读，且不阻断 authoring；purpose/card-family 隔离测试通过。

**Final status**：`PASS`。

## Issue F — machine bundle identity 覆盖实际 retrieval 输入

**Previous behavior**：只用 `corpus-package.json` 的 `package_hash` 表示 Corpus identity，
修改 `cards.jsonl` 可能不会改变 snapshot identity。

**Root cause**：package semantic identity、cards 和 retrieval dependencies 没有形成一个
机器 bundle identity。

**Fix**：compile/query 计算 canonical `machine_bundle_hash`，覆盖 semantic package identity、
`cards.jsonl` 和 retrieval dependencies；忽略无关的 `generated_at` 变化。保留 legacy
`package_hash`，但 snapshot seal 使用 machine bundle identity。

**Files changed**：`src/novel_authoring/reference_corpus/semantic.py`、
`src/novel_authoring/reference_corpus/query.py`、对应 tests。

**Regression test**：package 不变只修改 cards 时 machine bundle hash 改变；只修改
`generated_at` 时 machine bundle hash 不变。

**Final status**：`PASS`。

## Issue G — Snapshot read 自校验 hash

**Previous behavior**：读取已有 snapshot 只做 model validation，手工修改 compact card 并
保留旧 `snapshot_hash` 可能不被发现。

**Root cause**：没有统一的严格 loader 和 canonical hash re-computation。

**Fix**：`load_reference_context_snapshot()` 统一执行 strict schema validation、canonical
hash 重算和 stored hash 比对；所有 Draft、Revision、Original replay 读取路径复用该 loader。
篡改抛出 `ReferenceContextIntegrityError`/`ReferenceContextConflict`，不静默覆盖旧快照。

**Files changed**：`src/novel_authoring/reference_corpus/context.py`、Draft/Original/
Revision consumers 及 tests。

**Regression test**：freeze → 修改 compact guidance → 不更新 hash → reload 必须失败；
相同内容 hash 稳定，machine bundle 变化产生新的 snapshot identity。

**Final status**：`PASS`。

## Issue H — Revision PROSE scene function 使用实际章节

**Previous behavior**：`revision_kind` 默认映射可能把 style rewrite 等类型固定成 ACTION，
没有优先使用目标章节真实功能。

**Root cause**：Revision PROSE context 没有记录 scene-function 来源，也没有把 chapter
features/rhythm/Strategy/explicit policy/fallback 排成明确优先级。

**Fix**：优先目标 chapter features，其次 rhythm snapshot，再用 RevisionStrategy 的
actual scene functions，其次显式 policy，最后才是 revision-kind fallback；task 保存
`scene_functions` 和 `scene_function_source`。PLANNING 不把这些 prose-only functions 当作
mechanism/contrast 检索过滤条件。

**Files changed**：`src/novel_authoring/revision/service.py`、Revision Draft task tests、
`.agents/skills/revise-novel/SKILL.md`。

**Regression test**：target chapter 的 relationship feature 产生 `DIALOGUE`/
`RELATIONSHIP_SHIFT`，task source 为 `target_chapter_features`；无 feature 时分别覆盖
Strategy、explicit policy 和 revision-kind fallback。

**Final status**：`PASS（代码与 disposable Revision Draft task）`。

## 运行边界与未宣称项

- `REFERENCE_ONLY`、raw source anti-copy projection、Canon/Approval boundary 保持不变。
- Reference failure（`DISABLED`、`UNAVAILABLE`、`ZERO_RESULTS`、`CORRUPT` 或 not-ready）只
  产生 warning/knowledge gap，不阻断作者任务；hard authority 仍由现有 Story Engine 负责。
- `NOVEL_REFERENCE_CORPUS_ROOT` 当前未配置，production machine package 未做 live proof。
- 当前会话没有 browser control 工具，`REAL_BROWSER=BLOCKED`；不能把 TestClient 或离线
  fixture 写成 browser PASS。

## Revision chain evidence

本轮 disposable run 的可复核 ID 链保存在
[`REVISION_CHAIN_EVIDENCE.json`](REVISION_CHAIN_EVIDENCE.json)：

`Impact IDs`
→ `reference-context_45662941db81297e24515ba9`
→ `contrast-closure`、`mechanism-closure`
→ `RevisionStrategy.reference_card_ids_used`
→ `revision-draft-task_7e926de609ca60b9000ba4eb`
→ `reference-context_90648b466e91223b0969a9c6`

其中 Strategy 的结构动作来自两张 selected planning card，Draft task 同时保存
`RevisionUnit`、PLANNING provenance、Strategy、PROSE snapshot 和 scene-function source；
这证明 cards 改变了 Revision 的 HOW，而不是只作为未消费 metadata 存在。该 evidence
仍明确标记为 disposable，不代表 production Corpus 或 browser proof。
