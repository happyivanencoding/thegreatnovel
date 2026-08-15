# Reference Corpus → Novel Studio P0–P6 集成报告

## 结论

本轮把 Reference Corpus Semantic V1 接入同一个 deterministic Query Gateway，并把
compact、可复现的 `REFERENCE_ONLY` context 接入 Original、Continuation、Revision
和 Draft task。没有引入 embedding、Vector DB、Taste Brain、Trajectory、RL、自动
Candidate/Draft approval 或 Canon 写入。

当前代码线：`reference-corpus-semantic-v1`。本地 Web/CLI import 使用当前 checkout，
但本轮没有把旧的 `小说续写_codex` 分支静默提升为 authoritative branch；最终分支和
commit 以交付时 Git 状态为准。

## P0–P6 状态

| 项目 | 状态 | 证据 |
|---|---|---|
| P0 Web/runtime 代码线 | PARTIAL | 当前 checkout 的 Draft/Original/Web imports 可到达新代码；TestClient 与工作流回归通过。真实浏览器三路径尚未执行，不能宣称 PASS。 |
| P1 唯一 Query Gateway | PASS | `query_reference_corpus()` 是业务消费者唯一入口；semantic retrieval 只由 gateway 调用。 |
| P2 PLANNING | PASS | Original、Continuation candidate、Revision plan 均冻结 planning context；Reference 不选择 candidate、不改 Canon。 |
| P3 Revision Prose | PASS（协议/任务接线） | Revision Draft 复用 `.agents/skills/novel-prose-realization/SKILL.md`，写入相同 authority protocol 和 PROSE snapshot。 |
| P4 Query contract | PASS | `creative_problem` 仅人类描述；`creative_problem_tags` 才参与 metadata 匹配；bounded deterministic retrieval、family、source diversity、STALE/rewrite closure 保留。 |
| P5 Snapshot | PASS | `reference-context-snapshot-v1`，操作级 hash、package identity、card provenance、warnings/gaps、immutable path conflict。 |
| P6 Soft fail/observability | PASS | `ENABLED / ZERO_RESULTS / UNAVAILABLE / CORRUPT / DISABLED` 在 query、task、plan、handoff artifact 可见；显式 card count 和 selected ids。 |

## 架构

```text
Reference Corpus machine package
            │
            ▼
query_reference_corpus(Request)
  ├─ PLANNING ──► Original / Continuation / Revision Plan
  └─ PROSE ─────► Normal Draft / Revision Draft
            │
            ▼
freeze_reference_context(Response)
            │
            ▼
immutable reference_context_snapshot.json
            │
            ├─ compact planning context → existing Planner / Candidate Gates
            └─ compact prose controls  → shared Novel Prose Realization

Canon / Author Truth / Boundary / RevisionSpec / Approval remain authoritative.
```

## Authority boundary

Reference Corpus 只提供可迁移机制、对照、抽象 prose controls 和 knowledge gaps。它不能
修改 Canon、Author Truth、Boundary、RevisionSpec、Resource、Knowledge Boundary，不能
选择或批准 Candidate，不能批准或提交 Draft，也不能触发 Canon Commit。

下游 task prompt 会删除 `source_refs` 和 `source_book_ids`；Snapshot 的 provenance
只保留 locator-level compact evidence，不保存来源正文、长引用、full Book DNA 或
full Prose DNA。

## 验证摘要

- Query / Snapshot / semantic retrieval 针对性测试通过。
- Draft、Original、Continuation planning、Revision workflow 回归通过。
- `ruff` 针对任务文件通过。
- 真实浏览器验证受当前工具能力限制，见 [WEB_SMOKE_TEST.md](WEB_SMOKE_TEST.md)。

## Closure addendum — 2026-08-15（Closure Fix）

本节为本轮 closure 的追加状态，不覆盖上面的 P0–P6 结论。当前进程
`NOVEL_REFERENCE_CORPUS_ROOT=<unset>`，新证据全部来自 pytest `tmp_path` 下的 disposable
machine package；没有 production Corpus 或 browser 证据。

本轮修复后的关键变化：

- Revision 的顺序固定为 `Impact/Audit → RevisionUnit → PLANNING → RevisionStrategy`；
  `Impact` 阶段的 Reference Query 调用数保持为 0。
- `selected_card_ids → RevisionStrategy.reference_card_ids_used → Revision Draft task`
  已成为有 typed contract、snapshot provenance 和 `REFERENCE_ONLY` 标记的真实消费链。
- PLANNING 不再把 prose-only `scene_functions` 当作 mechanism/contrast 检索过滤条件；
  目标章节 scene functions 保留在 planning inputs，并在 PROSE 阶段按真实章节/节奏/策略
  选择。
- Revision metadata 从 Effective Contract payload、target chapter/rhythm/payoff/debt 和
  Impact shape 自动构造；RevisionSpec 显式值只作 augment。Continuation 的 state-derived
  controlled tags、Original 的 payload extraction、machine readiness、bundle hash 和
  snapshot self-integrity 均有回归覆盖。

详细的 Issue A–H（按本轮 closure 请求的定义）逐项记录见
[CLOSURE_REVIEW.md](CLOSURE_REVIEW.md)。`REAL_BROWSER=BLOCKED` 仍保持不变，P0 继续不能
写成 FULL PASS；生产 Corpus 也继续不能由 disposable 证据代替。

## FINAL CLOSURE addendum — 2026-08-15

本节追加最终 closure 审计，不覆盖上面的 P0–P6 和 Closure Fix 旧结论。当前 Reference
Corpus closure 状态为 `PASS_DISPOSABLE / PRODUCTION_NOT_CONFIGURED`：seal、Original
projection 与 Revision bounded selector 已通过 disposable corpus 锁定；clean checkout
CI 另有提交外的既有质量失败，单独记录为 `CI_BASELINE_FAILURE_OUT_OF_SCOPE`。

### Final closure evidence

- 新增 [test_reference_corpus_final_closure.py](../../tests/integration/test_reference_corpus_final_closure.py)。
- 更新 [REVISION_CHAIN_EVIDENCE.json](REVISION_CHAIN_EVIDENCE.json)：明确 selected `[A,B,C]`、
  bounded used `[A,B]`、`B.solution_2`、not used `[C,B.solution_1,B.solution_3]`、
  `prepare_revision_draft_task`、scene functions/source、PROSE snapshot/cards，以及 disposable/production status。
- 新增 [FINAL_CLOSURE.md](FINAL_CLOSURE.md)，按 Issue 1–4 记录 Previous behavior、Root cause、Fix、Files、Tests、
  Evidence、Status，并记录 source checkout runtime diagnostic。

### Status by issue

| Issue | 当前状态 | 证据 |
|---|---|---|
| 1. 两个 RevisionUnit 的 bounded selector、contrast solution、Strategy → Draft | `PASS_DISPOSABLE / PRODUCTION_UNVERIFIED` | `import_revision_strategy_selection()` 导入 Unit1=`A+B/B.solution_2`、Unit2=`C`，随后两个 Draft task 消费对应 Strategy；未选 solution 未进入 Strategy。 |
| 2. valid/missing/mutated/generated_at seal | `PASS_DISPOSABLE / PRODUCTION_UNVERIFIED` | valid=`ENABLED`；missing=`UNAVAILABLE/RECOMPILE_REQUIRED`；mutation=`CORRUPT/MACHINE_BUNDLE_HASH_MISMATCH`；generated_at-only hash stable。 |
| 3. Original supported handoff projection | `PASS_DISPOSABLE / PRODUCTION_UNVERIFIED` | 真实 `create_original_book → reader handoff → prepare_original_core_innovation`；snapshot provenance、creative guidance/ids/identity 存在，forbidden projection fields 缺失。 |
| 4. state tags / Impact zero query / family isolation / snapshot soft fail | `PASS_DISPOSABLE / PRODUCTION_UNVERIFIED` | 新测试回归通过；Impact query count 为 0，PLANNING/PROSE 隔离，tamper raises integrity error，missing path soft-fail。 |

### Validation result

```text
uv run --no-sync pytest -q tests/integration/test_reference_corpus_final_closure.py --tb=short
6 passed

uv run --no-sync pytest -q tests/integration/test_reference_corpus_final_closure.py -k "original_supported or continuation_tags"
2 passed, 4 deselected

uv run --no-sync pytest -q
510 passed

uv run --no-sync ruff check src tests
All checks passed!

uv run --no-sync mypy src
Success: no issues found in 197 source files

uv run --no-sync python -m compileall -q src tests
PASS

uv run --no-sync novel web doctor
ok=true
```

Final clean-checkout CI：GitHub Actions `quality-gates` run `31897807936` 在 Test 阶段失败，
共 `498 passed, 1 skipped, 5 failed`。失败项不属于本轮提交的 Reference Corpus 文件：

- `tests/integration/test_draft_approval.py::test_validation_rejects_missing_materialization_owner_before_approval`：依赖工作树未提交的 `canon/materialize.py` 与 `validation/validators.py`。
- `tests/unit/test_original_fantasy_salience_guidance.py::test_original_skills_preserve_exceptional_advantage_and_scope_realism`：依赖未提交的 Original semantic skill 文字。
- 3 个 `tests/unit/test_realized_kernel_trace.py` 用例：依赖未提交的 `validation/validators.py` 对缺失字段的既有修复。

因此本地工作树的 `510 passed` 不能写成 clean checkout CI 通过；本轮没有擅自合并这些无关
修改，working tree 状态也在最终报告中保留。

Production runtime diagnostic（使用当前 source checkout）为：`DISABLED`、
`configured_root=null`、`query_ready=false`、`bundle_seal_valid=false`，并提示未配置
Reference Corpus path。因此本追加段落不把 disposable `ENABLED` 结果写成 production PASS。

### Contract conflict note

旧的 `tests/integration/test_reference_corpus_closure.py` disposable fixture 已补齐最终
`machine_bundle_hash`，旧的“默认使用全部 cards”断言已改为显式 no-card fallback；全量
回归已通过。真实浏览器仍未执行，且本轮报告使用的是 source checkout 的 runtime diagnostic，
不是 production Corpus 证据。

代码级 Reference Corpus closure 已完成：
`REFERENCE_CORPUS_INFRASTRUCTURE = CLOSED_FOR_EXPERIMENT`。
下一阶段进入真实小说实验；不再扩展 Reference Corpus / GBrain 基础架构。
