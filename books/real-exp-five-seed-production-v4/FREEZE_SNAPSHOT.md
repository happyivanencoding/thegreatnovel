# v4 Freeze Snapshot

冻结时间：2026-08-20T13:11:34.4706762Z

## Git

- 分支：`principal_dev_new_sys`
- 生成开始时 HEAD：`b6828961e9e4939577e66264cc0b9a62de1ade95`
- 实际生产 Prompt commit：`b6828961e9e4939577e66264cc0b9a62de1ade95`
- 生成与冻结期间未修改生产源码、生产 Prompt 或 GBrain。
- 冻结范围：仅 `books/real-exp-five-seed-production-v4/`。

## Generation call

- 唯一 Fantasy Seed 生成调用 ID：`01a01f44-5b7c-7e20-aead-bcad87fe4838`
- 调用方式：一个真实 Agent、一次 request、一次 response、五个完整候选。
- 生成代理只读取 `INPUT.md` 与 `fantasy_seed_prompt.md`。
- 没有调用 GBrain、其它生成代理、World Vision、Story Program、Mainline、Outline 或章节。
- 原始 response：`fantasy_seed_response.md`
- 实际正式 Prompt 快照：`fantasy_seed_prompt.md`

## Frozen artifacts and sizes

以下为文件字节数；不是质量指标。

| 文件 | 字节数 |
|---|---:|
| `INPUT.md` | 876 |
| `fantasy_seed_prompt.md` | 3,071 |
| `fantasy_seed_response.md` | 23,960 |
| `candidates/candidate-01.md` · 未成之身 | 4,951 |
| `candidates/candidate-02.md` · 余烬最后一式 | 4,801 |
| `candidates/candidate-03.md` · 影中有路 | 4,306 |
| `candidates/candidate-04.md` · 欠天一笔 | 4,997 |
| `candidates/candidate-05.md` · 万物不肯沉默 | 4,905 |

## Split verification

- response 中恰有五个有序的 `## 候选N：` 原始标题。
- 五个候选文件均从 response 对应标题开始机械切片。
- 五个候选文件与对应 response 原文切片逐字一致；没有摘要、重写、补标题、语义修复、合并、去重或重排。
- 冻结后 Reviewer 不得修改以上候选、response、INPUT 或 Prompt 快照。
