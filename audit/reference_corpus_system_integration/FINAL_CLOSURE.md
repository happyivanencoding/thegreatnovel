# FINAL REFERENCE CORPUS CLOSURE

日期：2026-08-15
分支：`reference-corpus-semantic-v1`
本轮范围：完成最终 closure 的 bounded selector、machine seal、Original prompt projection 与回归审计；
没有修改 `book/`、Canon 或作者输入。

## 总状态

`PASS_DISPOSABLE / PRODUCTION_NOT_CONFIGURED`

- Disposable machine package：`TESTED`。测试 fixture 位于 pytest `tmp_path`，不是生产 Corpus。
- Production Corpus：`NOT_CONFIGURED`。当前进程没有 `NOVEL_REFERENCE_CORPUS_ROOT`。
- Seal contract：`PASS`（valid、missing seal、cards/dependencies mutation、`generated_at`-only 均有覆盖）。
- Revision bounded selector：现有 revision-plan task 已提供 bounded options；selector 输出经
  `import_revision_strategy_selection()` 严格导入后，Unit1 使用 `A+B/B.solution_2`，Unit2 使用
  `C`，并由 draft task 消费同一 Strategy。

## Runtime diagnostic

使用 source checkout 运行：

```text
{'status': 'DISABLED', 'configured_root': None, 'query_ready': False,
 'machine_bundle_hash': None, 'bundle_seal_valid': False, 'card_count': 0,
 'warnings': ['soft-fail：Reference Corpus 未启用或未配置'],
 'knowledge_gaps': ['当前没有可用的 Reference Corpus machine package/path']}
```

这只说明 production path 未配置，不把 disposable package 的 `ENABLED` 结果冒充 production 运行证据。

## Issue 1 — bounded RevisionUnit selector 与 Strategy → Draft chain

### Previous behavior

上一轮 closure 证明了 selected cards 可以进入 Revision 相关产物，但没有证明两个
`RevisionUnit` 会做有界、不同的消费选择，也没有排除 Unit1 默认等于全部 selected ids。
当前 `build_revision_plan` 先生成 per-unit selector input 和 frozen planning snapshot，
再由现有 revision-plan task 接收 selector output；Python 只在导入边界校验并冻结结果。

### Root cause

旧缺口是 selector 输出没有接到 `RevisionStrategy` consumer；因此旧运行曾退回空 Strategy。

### Fix

本 Worker 新增严格 disposable contract：

- frozen planning snapshot selected `[A, B, C]`；
- Unit1 必须使用 `A+B`，且只使用 `B.solution_2`；
- Unit1 不得出现 `C`、`B.solution_1`、`B.solution_3`；
- Unit2 必须使用 `C` 或明确的无 card fallback，且两个 unit 结果必须不同；
- 所有 card/solution id 必须回到 frozen snapshot；
- `prepare_revision_draft_task` 必须携带同一 strategy、snapshot id/hash、PROSE snapshot 和 scene function provenance。

主 Agent 在同一 `revision-plan` stage 增加 typed selector-output importer：它逐 unit 调用
现有 `_build_revision_strategy(selector_output=...)`，校验 campaign/edition/task/snapshot、
card 子集、Contrast solution 存在性和 `REFERENCE_ONLY`，再更新 plan/task；没有新增 planner。

### Files

- [test_reference_corpus_final_closure.py](../../tests/integration/test_reference_corpus_final_closure.py)
- [REVISION_CHAIN_EVIDENCE.json](REVISION_CHAIN_EVIDENCE.json)

### Tests

```text
uv run --no-sync pytest -q tests/integration/test_reference_corpus_final_closure.py --tb=short
6 passed
```

测试证明 `selected [A,B,C] → selector output [A,B]/B.solution_2 → imported RevisionStrategy →
两个 Revision Draft task`，且 `C/B.solution_1/B.solution_3` 未进入 Unit1 Strategy。

### Evidence

[REVISION_CHAIN_EVIDENCE.json](REVISION_CHAIN_EVIDENCE.json) 显式记录：selected
`[A,B,C]`、contract used `[A,B]`、`B.solution_2`、not used
`[C,B.solution_1,B.solution_3]`、`prepare_revision_draft_task`、PROSE snapshot/cards、
`ACTION/PAYOFF` 与 `revision_kind_fallback`，并记录 selector output 的导入路径。

### Status

`PASS_DISPOSABLE / PRODUCTION_UNVERIFIED`。Production Corpus 未配置，因此只把 disposable
workflow 作为代码级集成证据。

## Issue 2 — machine package seal 与稳定性

### Previous behavior

上一轮 closure 有 machine bundle hash 计算证据，但没有把缺失 seal、cards/dependencies
mutation 和 `generated_at`-only 变更作为 query/runtime diagnostic 的最终 contract 逐项锁定。

### Root cause

需要把“可查询”与“package seal 仍对应 cards/dependencies”分开验证，否则 stale 或未重新
compile 的 machine bundle 可能继续以 `ENABLED` 进入 workflow。

### Fix

新测试通过公开 `query_reference_corpus` 与 `reference_corpus_runtime_diagnostic` 验证：

- valid seal → `ENABLED`；
- 缺少 `machine_bundle_hash` → `UNAVAILABLE`，warning 含 `RECOMPILE_REQUIRED`；
- cards 或 dependencies 变化而 seal 未更新 → `CORRUPT`，warning 含
  `MACHINE_BUNDLE_HASH_MISMATCH`；
- 只有 `generated_at` 变化 → 状态保持 `ENABLED` 且 machine bundle hash 不变。

### Files

- [test_reference_corpus_final_closure.py](../../tests/integration/test_reference_corpus_final_closure.py)
- seal 实现位于 `src/novel_authoring/reference_corpus/semantic.py`，Query 与 runtime
  diagnostic 共用 `validate_machine_package()`。

### Tests

seal 参数化测试 2 项与 `generated_at` 稳定性测试均通过，包含 runtime diagnostic 断言。

### Evidence

`REVISION_CHAIN_EVIDENCE.json.machine_bundle_seal` 记录了四种结果。生产运行 diagnostic
仍为 `DISABLED/NOT_CONFIGURED`，因为没有 production root。

### Status

`PASS_DISPOSABLE / PRODUCTION_UNVERIFIED`。

## Issue 3 — Original supported handoff projection boundary

### Previous behavior

上一轮 closure 主要检查 private planning adapter；没有用完整的真实 supported handoff
证明 full snapshot provenance 可以保留在审计 artifact，同时 `original_request` 与
executor task 的 projection 不携带来源正文或 full-DNA 字段。

### Root cause

Original 的 planning snapshot 与 Codex executor input 是不同 authority boundary；只测其中一层
无法证明 handoff 的输入投影没有越界。

### Fix

新测试走公开工作流：

`create_original_book → reader handoff completion/import/confirm → prepare_original_core_innovation`。

它验证了 A/B/C selected ids、snapshot id/hash、machine identity、compact creative guidance、
progression contract id 和 book/stage identity 存在；同时 `original_request` 与 executor
projection 都排除了 `source_refs`、`source_book_ids`、raw/full text、full DNA 等 forbidden fields，
并保留 `NO_CHAPTER_NO_CANON`。

### Files

- [test_reference_corpus_final_closure.py](../../tests/integration/test_reference_corpus_final_closure.py)
- [REVISION_CHAIN_EVIDENCE.json](REVISION_CHAIN_EVIDENCE.json)

### Tests

```text
uv run --no-sync pytest -q tests/integration/test_reference_corpus_final_closure.py -k "original_supported or continuation_tags"
2 passed, 4 deselected
```

### Evidence

测试读取真实 handoff 的 `input/original_request.json` 与 `input/task.json`，没有直接调用
private reference adapter 作为主证明。完整 snapshot provenance 只留在 handoff artifact；
executor task 仅得到允许的 projection。

### Status

`PASS_DISPOSABLE / PRODUCTION_UNVERIFIED`。

## Issue 4 — regressions: state tags, query boundary, family isolation, snapshot soft fail

### Previous behavior

上一轮 closure 分别覆盖了部分 Query/Snapshot/Continuation/Revision 路径；最终 closure 需要
把 state-derived tags、Impact zero query、PLANNING/PROSE family isolation 和 snapshot
integrity/soft-fail 放在同一份 disposable enabled corpus regression 中。

### Root cause

这些边界若只在单一 helper 或单一 query 测试中出现，无法证明 workflow consumer 仍沿用
同一 frozen snapshot 和 family boundary。

### Fix

新测试通过公开 candidate/task、query、freeze/load workflow 验证：

- Continuation query 收到非空 state-derived controlled tags；
- Revision Impact/Audit 的 Reference query 次数为 0；
- PLANNING 只得到 mechanism/contrast/synthesis family，PROSE 只得到 prose-control；
- compact card tamper 被 `ReferenceContextIntegrityError` 拒绝；
- missing corpus path soft-fail 为 `UNAVAILABLE`；
- PROSE snapshot cards 为 `[prose-control]`，scene functions 为 `[ACTION, PAYOFF]`，source 为 `revision_kind_fallback`。

### Files

- [test_reference_corpus_final_closure.py](../../tests/integration/test_reference_corpus_final_closure.py)

### Tests

上述回归均包含在最终 closure 文件中；Original/Continuation 子集为 `2 passed`，完整运行中
其余 3 项（seal 2 项、generated_at 1 项）也通过。

### Evidence

完整结果为 `6 passed`。详细 machine/prose/snapshot/strategy 字段见
[REVISION_CHAIN_EVIDENCE.json](REVISION_CHAIN_EVIDENCE.json)。

### Status

`PASS_DISPOSABLE / PRODUCTION_UNVERIFIED`。

## Validation and scope notes

- `uv run --no-sync ruff check tests/integration/test_reference_corpus_final_closure.py`：`PASS`。
- 未提交 Git；未执行 commit/push/reset/checkout。
- 旧的 `tests/integration/test_reference_corpus_closure.py` disposable fixture 已补齐最终 seal 字段，
  并更新旧的“默认使用全部 cards”断言为显式 no-card fallback；完整回归不再依赖旧的错误语义。
- `REAL_BROWSER` 未执行；本轮 closure 只提供本地 disposable workflow 证据。

## Closure decision

代码级 closure 已完成：Revision bounded selection、machine bundle seal、Snapshot integrity、
Original shared prompt projection、Continuation state-derived query、PLANNING/PROSE family
隔离和 soft-fail 均有通过的测试证据。Production Corpus 当前为 `NOT_CONFIGURED`，真实
Browser 为 `BLOCKED`；两者均未被 disposable/TestClient 结果冒充通过。

`REFERENCE_CORPUS_INFRASTRUCTURE = CLOSED_FOR_EXPERIMENT`

下一阶段应进入真实小说实验，不再继续扩展 Reference Corpus / GBrain 基础架构。
