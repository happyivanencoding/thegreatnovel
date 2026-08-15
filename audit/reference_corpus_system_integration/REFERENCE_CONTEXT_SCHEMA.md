# `reference-context-snapshot-v1`

实现：`src/novel_authoring/reference_corpus/context.py`。

## 字段

```text
schema_version = reference-context-snapshot-v1
snapshot_id
purpose = PLANNING | PROSE
book_id / edition_id / operation_id
creative_problem
creative_problem_tags
reader_experiences / narrative_drives / payoff_channels / scene_functions
max_cards
package_schema_version / package_hash
selected_card_ids / selected_card_count / selected_card_types
selected_card_knowledge_levels
metadata_match_fields
compact_cards
knowledge_gaps / warnings
status = ENABLED | ZERO_RESULTS | UNAVAILABLE | CORRUPT | DISABLED
usage = REFERENCE_ONLY
created_at
snapshot_hash
```

## 冻结规则

1. Snapshot 只接收已经经过 Query Gateway 的 compact response，不读取 raw Corpus。
2. `snapshot_hash` 对除时间戳和自身 hash 外的 canonical payload 计算，因此相同操作、
   相同 query、相同 package/card projection 的 hash 稳定。
3. 同一 output path 已存在且 hash 相同，返回已冻结 artifact；hash 不同则抛出
   `ReferenceContextConflict`，不覆盖旧 Snapshot。
4. `compact_cards` 重新通过 Query 的 closed union 校验；禁止 `observation_summary`、
   `source_quote`、`raw_text`、`source_prose`、`source_content`、`book_dna`、
   `prose_dna` 等字段。
5. provenance 只保留 source/segment/line locator；task prompt 在交给 executor 前
   进一步删除 source locator 和 source book ids。

## 与 Canon 的关系

Snapshot 是 operation/task input artifact，不是 Canon、Truth、Story Atlas 或事实投影。
它不会进入事件流、审批或 Edition activation。
