# real-exp-002：GBrain Novel-First Retrieval v1

- 实验性质：非 Canon Retrieval 实验记录
- 日期：2026-08-19
- 模式：`outline`
- 使用查询：`books/real-exp-002/runs/outline.md` 中保存的同一份 Outline Retrieval Brief
- 目的：验证小说来源过滤是否发生在 `RAW_RESULT_LIMIT` 截断之前；不评价 real-exp-002 的小说质量
- 未执行：没有重新生成 Outline、章节或 Prompt；没有修改 `BOOK.md`、`PROPOSAL.md`、五个 chapter 文件或 Canon Index

## CLI scope 判断

当前 `gbrain query --help` 只提供 `--limit`、`--offset`、`--expand`、`--detail`，Hermes 的 `query` operation 也只有 `query`、`limit`、`offset`、`expand`、`detail` 参数，没有 path、namespace、category、collection 或 scope 过滤。

因此本版本采用一次宽召回后确定性过滤：

```text
一次 query（请求 24 条）
→ 按当前 mode 的 MODE_ALLOWED_CATEGORIES 过滤
→ 最多检查 8 条小说候选（RAW_RESULT_LIMIT）
→ 完整页面 / abstract / BOOK compatibility
→ outline 最多返回 5 条 Inspiration
```

没有修改 Hermes，也没有增加第二套索引、重试或 reranker。

## Raw hits 对比

两次查询实际都返回 20 条；下表记录完整的 score/slug 命中顺序。修改前 CLI 请求上限是 8，但当前 CLI 实际返回 20 条；修改后请求上限是 24，实际仍返回 20 条。

| rank | 修改前 | 修改后 |
| ---: | --- | --- |
| 1 | 0.8350 `30_education/01_math/l2s4-td8` | 0.8350 `30_education/01_math/l2s4-td8` |
| 2 | 0.8204 `30_education/01_math/applications` | 0.8204 `30_education/01_math/applications` |
| 3 | 0.8076 `30_education/01_math/graph-theory-ultimate` | 0.8076 `30_education/01_math/graph-theory-ultimate` |
| 4 | 0.7955 `99_system/templates` | 0.7955 `99_system/templates` |
| 5 | 0.7849 `99_system/templates` | 0.7849 `99_system/templates` |
| 6 | 0.7738 `20_knowledge/03_ai_ml/index` | 0.7738 `20_knowledge/03_ai_ml/index` |
| 7 | 0.7616 `arcs/rcv0-29-xuanhuan-guimi-zhi-zhu-arc-01-threshold-to-social-engine` | 0.7616 `arcs/rcv0-29-xuanhuan-guimi-zhi-zhu-arc-01-threshold-to-social-engine` |
| 8 | 0.7517 `20_knowledge/moc` | 0.7517 `20_knowledge/moc` |
| 9 | 0.7419 `99_system/2026-04-19-vault` | 0.7419 `99_system/2026-04-19-vault` |
| 10 | 0.7324 `arcs/candidate-loophole-to-jurisdiction` | 0.7324 `arcs/candidate-loophole-to-jurisdiction` |
| 11 | 0.7237 `20_knowledge/moc` | 0.7237 `20_knowledge/moc` |
| 12 | 0.7152 `prose-dna/rcv0-28-xuanhuan-jiangye` | 0.7152 `prose-dna/rcv0-28-xuanhuan-jiangye` |
| 13 | 0.7067 `99_system/index` | 0.7067 `99_system/index` |
| 14 | 0.6986 `docs/reference_corpus_v0_plan` | 0.6986 `docs/reference_corpus_v0_plan` |
| 15 | 0.6908 `rcv0-29-xuanhuan-guimi-zhi-zhu/reference_programs_search_projection` | 0.6908 `rcv0-29-xuanhuan-guimi-zhi-zhu/reference_programs_search_projection` |
| 16 | 0.6831 `99_system/templates/filename` | 0.6831 `99_system/templates/filename` |
| 17 | 0.6757 `observations/rcv0-05-xuanhuan-feisheng-zhihou-obs-04` | 0.6757 `observations/rcv0-05-xuanhuan-feisheng-zhihou-obs-04` |
| 18 | 0.6683 `30_education/01_math/applications` | 0.6683 `30_education/01_math/applications` |
| 19 | 0.6613 `prose-dna/rcv0-15-youxi-kuicheng-shoufu` | 0.6613 `prose-dna/rcv0-15-youxi-kuicheng-shoufu` |
| 20 | 0.6541 `50_research/2` | 0.6541 `50_research/2` |

> 注：第 20 行的 score/slug 按本次 `gbrain` 原始输出记录；完整原始 stdout 仍保留在 `runs/outline.md`。本表用于比较候选位置，不把 snippet 当作完整卡片内容。

## 修改前

证据来源：`books/real-exp-002/runs/outline.md` 的原始 stdout 与“接受与拒绝结果”，以及 `books/real-exp-002/EXPERIMENT.md` 的 Outline Retrieval 记录。

- `raw_count`: 20；请求上限：8。
- 旧逻辑先执行 `parsed[:8]`，再过滤来源类别。
- 实际进入小说候选检查的只有 rank 7 的 `arcs/rcv0-29-xuanhuan-guimi-zhi-zhu-arc-01-threshold-to-social-engine`。
- rank 10 的 `arcs/candidate-loophole-to-jurisdiction` 被记录为“超过原始数量上限”，没有读取完整页面。
- accepted：1；Outline Inspiration：1。
- rejected：19，其中 12 条“超过原始数量上限”，7 条是 mode 不允许的非小说来源。
- 完整 GBrain 页面读取：1 条。

## 修改后

本次重新执行的是同一份 Outline Retrieval Brief，结果由当前生产代码真实调用 GBrain CLI 得到。

- `raw_count`: 20；CLI 请求上限：24。
- `novel_candidate_count`: 2；两条均来自 outline 允许的 `arcs/`：
  - `arcs/rcv0-29-xuanhuan-guimi-zhi-zhu-arc-01-threshold-to-social-engine`（0.7616）
  - `arcs/candidate-loophole-to-jurisdiction`（0.7324）
- `RAW_RESULT_LIMIT`: 8；本次只有 2 条小说候选，因此两条都进入完整页面检查。
- accepted：2；两张卡片均通过抽象区块提取与当前 BOOK compatibility，没有因为玄幻来源标签被拒绝。
- rejected：18；全部是当前 outline mode 不自动使用的非小说或非创作来源类别，没有任何“超过小说候选数量上限”的记录。
- 完整 GBrain 页面读取：2 条，实际读取 slug 只有上述两条 Arc；数学、AI、system、research、prose-dna、docs 等页面均未调用 `get_gbrain()`。
- Outline Inspiration：2 条，仍低于现有 final limit 5；增加的第 2 条正是旧实现被截掉的小说 Arc，没有无关 Prompt 扩张。

## 验收结论

1. 数学、AI、system 内容不再占用 novel candidate slot；它们只留下来源过滤拒绝记录。
2. 原先位于原始 Top 8 之后的 `arcs/candidate-loophole-to-jurisdiction` 进入了小说候选和完整页面检查。
3. BOOK compatibility 仍在完整页面抽象提取之后执行；本次两个 Arc 都没有触发当前 BOOK 的表层硬冲突。
4. 页面读取从 1 条变为 2 条，增加来自恢复一个真实小说候选，而不是读取无关页面。
5. 本实验只验证 Retrieval，不把新的 Inspiration 写回 BOOK、Outline、章节或 Canon。
