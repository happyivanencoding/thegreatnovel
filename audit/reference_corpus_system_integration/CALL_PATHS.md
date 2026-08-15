# Reference Corpus 真实调用链

所有业务调用都经过 `src/novel_authoring/reference_corpus/query.py` 的
`query_reference_corpus()`；业务层不读取 Corpus Markdown、GBrain DB 或 raw source。

## Original PLANNING

```text
Original request / confirmed Reader Kernel + Narrative Drive
  → prepare_original_core_innovation()
  → prepare_original_bootstrap()
  → prepare_original_foundation_development()
  → _original_reference_planning_context()
  → ReferenceCorpusQueryRequest(purpose="PLANNING")
  → query_reference_corpus()
  → freeze_reference_context()
  → original_request.json / Genesis planning task
  → current Original workflow + author selection
```

卡片只作为 Core、Foundation、Genesis candidate 的参考；作者选择和现有 Genesis/Kernel
流程仍决定最终结果。

## Continuation PLANNING

```text
Canon + Boundary Packet + Planning Aggregate + effective Reader/Drive/Payoff
  → prepare_candidate_task()
    或 prepare_handoff_candidate_task()
  → _continuation_reference_planning_context()
  → ReferenceCorpusQueryRequest(purpose="PLANNING")
  → query_reference_corpus()
  → freeze_reference_context()
  → input/reference_context_snapshot.json
  → task.json + input.md compact planning context
  → existing Candidate hard gates / ranking / contract
```

Reference context 不创建资源、不改变知识边界、不绕过 Boundary，也不自动选择 Candidate。

## Revision PLANNING

```text
RevisionSpec
  → deterministic impact scan
  → semantic impact audit / Impact Packet
  → build_revision_plan()
  → _revision_reference_context(purpose="PLANNING")
  → query_reference_corpus()
  → freeze_reference_context()
  → plan operation/reference_context_snapshot.json
  → revision_plan.json + plan task.json
```

Impact 阶段不调用 Reference Corpus；Corpus 只回答“可迁移的结构/表达解法”，不回答
“哪些作品事实必须修改”。

## Normal Draft PROSE

```text
Chapter Contract + Boundary + runtime context
  → prepare_draft_task()
  → _reference_prose_context()
  → ReferenceCorpusQueryRequest(purpose="PROSE")
  → query_reference_corpus()
  → freeze_reference_context()
  → task/reference_context_snapshot.json
  → task.json.reference_prose_context + input.md
  → continue-novel executor
  → novel-prose-realization
  → Draft → Naturalness Audit → existing Validation
```

PROSE projection 仅包含 prose-control 字段；planning mechanism/contrast/synthesis 不会
进入 prose context。

## Revision Draft PROSE

```text
Impact Packet + Revision Plan + RevisionUnit
  → prepare_revision_draft_task()
  → _revision_reference_context(purpose="PROSE")
  → query_reference_corpus()
  → freeze_reference_context()
  → draft operation/reference_prose_context_snapshot.json
  → task.json + input.md
  → revise-novel executor
  → same novel-prose-realization skill/protocol
  → REVISION_DRAFT → Revision validators
```

Revision prose controls不能改变 `required_changes`、`must_preserve`、事件顺序、人物
选择、资源、知识边界或 `expected_after_state`。
