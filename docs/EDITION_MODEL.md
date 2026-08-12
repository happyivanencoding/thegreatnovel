# Edition 数据模型

## 版本锚点

`editions` 为每本书保存一个不可单独删除的 `base` 和任意多个派生版本。派生版本创建时固定 `parent_edition_id`、父投影在当时的 `base_event_seq`、`base_projection_hash` 和不可变 source manifest SHA-256。父版本后来变化不会静默改变派生版本；显式 rebase 不在本版本范围内。作者明确永久删除整个 Library Project 时，项目内所有 Edition 会随 `library/<book_id>/` 一并删除；这不影响 IMPORTED 项目的外部来源文件。

生命周期状态为 `DRAFT → VALIDATED → ACTIVE → ARCHIVED`。同一本书最多一个 `ACTIVE`，`books.active_edition_id` 是默认续写入口。

生命周期不再承担版本用途。`edition_purpose` 独立区分：

- `SOURCE_BASE`：来源底稿；
- `AUTHOR_REVISION`：修订当前故事路线；
- `ALTERNATE_ROUTE`：从指定章节另开故事路线，必须记录 `fork_chapter_ordinal`。

`official_role` 独立表达作者关系：`CURRENT / CANDIDATE / ALTERNATE / ARCHIVED`。
实验、Benchmark、A/B 和盲测仍属于 Operation，不是 Edition。旧派生 Edition 无法可靠判断用途时，
迁移为 `AUTHOR_REVISION` 并标记 `purpose_review_required=true`，不会根据名称猜测平行路线。

## 投影隔离

EventStore 仍是唯一 append-only 哈希链。base 事件沿用 V1 头部格式；版本化事件携带 `edition_id`。派生 Canon Projection 重放父版本在冻结序列的投影，再叠加该 edition 的批准改写事件和后续章节事件。facts、人物状态、关系、知识边、线程、承诺、指标、boundary、contract、draft、validation、commit、snapshot 和 projection metadata 均带 edition scope；不可变 source documents、spans 和原始 chapters 可以共享。

## Chapter Variant

`chapter_variants` 是整章 replacement 载体。它保存稳定 `base_chapter_id`、`base_source_span_id`、原始内容 hash、替换正文 hash、campaign、superseded variant、批准时间和 revision commit。`(edition_id, base_chapter_id)` 上的 partial unique index 保证一个版本最多一个 active variant。投影和导出在稳定 chapter ID 上做替换，原始 `chapters.content` 永不更新。

## 改写审计关系

```text
revision_campaigns
  ├─ revision_impact_packets / revision_impact_items
  ├─ revision_units
  ├─ revision_drafts
  ├─ revision_validation_reports
  ├─ chapter_variants
  └─ revision_commits → edition snapshot / event range
```

实体改名通过 `edition_entity_overlays` 保留同一稳定 `entity_id`，旧名进入 aliases/historical aliases；对应的 overlay event 只进入目标 edition。事实替换使用 `supersedes_fact_id` 或 edition overlay，不会覆盖 base。

## 续写入口

V1 命令不传 `--edition-id` 时解析当前 ACTIVE，若无派生 ACTIVE 则使用 base。传入派生版本时，Boundary、plan、contract、draft、validation、approve、snapshot、rebuild 和 export 均从该 edition 的 variants、投影状态和最近章节读取，因此不会把 base 中已被替换的旧关系带回续写。

## 作者操作

“改写本章”必须先选择“修订当前路线”或“另开故事路线”，然后才创建对应用途的派生 Edition。
Revision Campaign 批准后，Edition 只进入 `VALIDATED`，并保持 `CANDIDATE` 或 `ALTERNATE`；
只有作者再次确认“设为当前正式版本”，系统才切换 `CURRENT`。批准改写和版本激活始终是两次操作。
