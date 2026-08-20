# Clean Compounding Seed Test v1 · Freeze Snapshot

## 调用记录

- 生产 Prompt commit：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- 生成时 HEAD：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- 唯一有效模型生成：1 次
- Agent：1 个
- request：`request.md`，1 个
- response：`fantasy_seed_response.md`，1 个
- 模型：`gpt-5.6-luna`
- response id：`chatcmpl-EEz0gQ0Jx2JHXDabXmdH1jQUdLTRA`
- finish reason：`stop`
- response candidates：5 个
- GBrain：未调用
- World Vision / Story Program / Outline / 章节 / Canon / State Delta：未调用

## 传输备注

最初的 CLI 命令在模型生成前被 API 以 400 拒绝，因为旧 CLI 发送了该模型不支持的 `max_tokens`；它没有产生 response。随后未改变输入、Prompt、模型或候选数量，只改用模型支持的 `max_completion_tokens` 发出唯一有效生成请求。

## 冻结候选边界

| 候选 | 标题 | response 行区间 |
|---|---|---:|
| 1 | 偷走明天的人 | 1—76 |
| 2 | 万法遗骸 | 78—149 |
| 3 | 掌中天工 | 151—220 |
| 4 | 众生之名 | 222—303 |
| 5 | 吞界行舟 | 305—378 |

以上五个 Seed 是本次盲审唯一对象。冻结后不修改 response、不重生成、不进入后续创意阶段。
