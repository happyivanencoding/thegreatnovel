# Core Writer Attribution v2 Final Report

## Git

- branch：`principal_dev_new_sys`
- BASE_SHA：`d8f0a43219986cbe758647d65665062f8f8be66a`
- FINAL_SHA：最终 handoff 回填
- pushed：最终 handoff 回填
- no new branch：确认未创建
- production backend modified：`no`
- frontend modified：`no`
- Prompt modified：`no`
- git status：最终 handoff 核对

## Validity

- old snapshot-01：`INVALID_CONTEXT_CONTAMINATION`，不进入 verdict。
- clean b3：旧 snapshot-02，《炉藏万象》Chapter 3。
- clean c2：旧 snapshot-03，《掌中天工》Chapter 2。
- replacement b2：新生成，《炉藏万象》Chapter 2。
- presentation-only 标题剥离只作用于 blind option；raw body 原样保留。

## New calls

- replacement b2：Single 1、Primary-Fallback 1、Curator 1、Curated Primary 1，共 4 次。
- b3/c2：不重跑，复用上一轮 raw body。
- corrected Reader：3 次，每个 clean snapshot 一次。
- 实际 tokens：全部 `UNKNOWN`。

## Corrected blind results

Blind key 独立保存；Reader 只读取 option A/B/C。主线程在 Reader 完成后解码来源。

| clean snapshot | A vs B | A vs C | B vs C | decoded Single vs Primary-Fallback | decoded Primary-Fallback vs Curator-Primary | decoded Single vs Curator-Primary | overall |
|---|---|---|---|---|---|---|---|
| b2 replacement | A | MIXED | C | `SINGLE` | `CURATOR_PRIMARY` | `MIXED` | `SINGLE` |
| b3 reused | A | MIXED | C | `MIXED` | `PRIMARY_FALLBACK` | `SINGLE` | `PRIMARY_FALLBACK` |
| c2 reused | MIXED | C | C | `MIXED` | `CURATOR_PRIMARY` | `CURATOR_PRIMARY` | `CURATOR_PRIMARY` |

## Attribution

### Primary Writer vs Single

Primary-Fallback 没有在至少 2/3 clean snapshot 明确胜 Single：b2 是 Single，b3/c2 是 MIXED。Primary 的局部优势不能升级为稳定核心链结论。

### Curator-Primary vs Primary-Fallback

Curator-Primary 在 b2 replacement 和 c2 明确胜 Primary-Fallback，b3 由 Primary-Fallback 胜出，因此达到 2/3 门槛。Curator 的优势主要体现在当前场景聚焦、动作/空间清晰、危险升级和章末推进；不是三章全维度横扫。

### Curator-Primary vs Single

Curator-Primary 在 c2 胜 Single，b2 为 MIXED，b3 由 Single 胜出；没有对 Single 的稳定退化。因此满足“相对 Single 没有稳定退化”的附加条件。

## Architecture Verdict

`CURATOR_PRIMARY_CORE_SUPPORTED`

这是一个有限的三 snapshot 结构性结论：Curator-Primary 相对 Primary-Fallback 达到 2/3 明确优势，且相对 Single 没有稳定退化。它不证明 Curator 每章都有效，也不改变生产默认 Writer Mode。

上一轮的 `SPECIALIST_INTEGRATOR_SELECTIVE_VALUE` 继续冻结；Specialist/Integrator 仍只是 optional repair，不在本轮重测或进入默认链。

## Stop boundary

完成 replacement b2、3 个 corrected Reader 和 b2/b3/c2 最终汇总后停止。未扩大 snapshot、未进入十章、未生成 Chapter 4、未修改生产代码、Prompt、前端或 Writer Mode。
