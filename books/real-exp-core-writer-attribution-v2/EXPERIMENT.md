# Core Writer Attribution v2 — Validity-Corrected Experiment

本轮是上一轮 Core Writer Attribution 的最小有效性修正，不覆盖 v1，也不重新运行 clean b3/c2。旧 snapshot-01 因 BOOK Canon 已经越过目标章节而正式排除；新增《炉藏万象》Chapter 2 replacement，并修正盲读外层标题污染。

## Arms

- Single：正式 `mode="chapter"`，1 次 content call。
- Primary-Fallback：正式 `mode="primary_writer"`，`curator_response=""`、`curated_context=""`，触发生产 fallback，1 次 content call。
- Curator-Primary：正式 `context_curator` 1 次，再将原始 Curator Response 传给正式 `primary_writer` 1 次。

replacement 新增 4 次 content calls；b3/c2 不重跑。完成后仅新增 3 次 corrected blind Reader calls。

## Validity policy

先完成 `VALIDITY_AUDIT.md` 中的 CONTENT_SCOPE_MISMATCH 审计，再对 blind option 确定性剥离单个外层章节标题。Raw body、Prompt 和 Response 原样保留；标题剥离只作用于 blind packaging，不能掩盖上下文污染。

## Provenance

- branch：`principal_dev_new_sys`
- code audit base：`d8f0a43219986cbe758647d65665062f8f8be66a`
- generation source：clean v2 historical Git tree `d4e2dd6f3377f967d8930480016f15a450b74e1b`
- 生产 backend、Prompt、frontend：本轮均未修改。
