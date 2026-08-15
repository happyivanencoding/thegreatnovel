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
