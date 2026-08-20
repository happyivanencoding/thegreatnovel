# v3 Freeze Snapshot

冻结时间：2026-08-20T14:37:42.3329317+02:00

## Git

- 分支：`principal_dev_new_sys`
- 生成开始时 HEAD：`f979ced25ce24b3d856f71d1f6ca77b56a6d3aad`
- 实际生产 Prompt commit：`a6e551460f1f13a8d42c44d43e8961b4f552958e`
- 生成与冻结期间未修改生产源码、生产 Prompt 或 GBrain。
- 冻结时工作树新增范围：仅 `books/real-exp-five-seed-production-v3/`。

## Generation call

- 唯一 Fantasy Seed 生成调用 ID：`01a01f27-6f7f-7902-8b47-bb720a202cf2`
- 调用方式：一次调用、一个 response、五个完整候选。
- 生成代理只读取 `INPUT.md` 与 `fantasy_seed_prompt.md`。
- 没有调用 GBrain、其它代理、World Vision、Story Program、Mainline、Outline 或章节。
- 原始 response：`fantasy_seed_response.md`
- 实际 Prompt 快照：`fantasy_seed_prompt.md`

## Frozen artifacts and sizes

以下为文件字节数；不是质量指标。

| 文件 | 字节数 |
|---|---:|
| `fantasy_seed_prompt.md` | 3,357 |
| `fantasy_seed_response.md` | 20,974 |
| `candidates/candidate-01.md` · 坠星入骨 | 4,357 |
| `candidates/candidate-02.md` · 百兽新身 | 4,312 |
| `candidates/candidate-03.md` · 缝天行 | 4,042 |
| `candidates/candidate-04.md` · 万器回春 | 4,264 |
| `candidates/candidate-05.md` · 噤雷开声 | 3,995 |

## Split verification

- response 中恰有五个 `## 候选N：` 原始标题。
- 五个候选文件均从 response 对应标题开始机械切片。
- 五个候选文件与对应原文切片一致；没有摘要、重写、补标题、语义修复、合并、去重或重排。
- 冻结后 Reviewer 不得修改以上候选。
