# Canon Memory 压力测试

`canon_chars`、`recent_summaries_chars` 是对应 State Delta 后 BOOK 中各区正文字符数；`open_promises_count` 是该区的条目数，不是质量评分。

| State Delta 后 | BOOK 总 chars | Persistent Canon | Recent Summaries | Open Promises 条目 |
|---|---:|---:|---:|---:|
| Ch4 | 16,826 | 761 | 832 | 7 |
| Ch5 | 17,162 | 848 | 986 | 8 |
| Ch6 | 17,362 | 805 | 1,226 | 8 |
| Ch7 | 18,030 | 955 | 1,450 | 10 |
| Ch8 | 18,363 | 1,067 | 1,668 | 8 |
| Ch9 | 18,907 | 1,187 | 1,925 | 9 |
| Ch10 | 19,462 | 1,232 | 2,176 | 11 |

## 连续性结果

- 裂路器从 Ch2 铸成后持续存在，状态从可开路变为钝化、只能沿旧裂剥离；Ch10 的红黑补层没有被误写成恢复连续切割。
- 火鳞器从 Ch5 成器，Ch8—9 变暗，Ch10 只恢复有限承热；没有凭空消失、重复生成或被写成无代价全恢复。
- 未完成炉心从 Ch5 起始终由五名炉工托持，Ch10 经过侧炉/炉匣接合后才解除直接承托；实体炉心与沈燧体内热线没有混为一物。
- 右掌、右臂、肩伤和炉工承重伤势持续出现；没有旧伤突然消失。第 1 章的十三名矿工后来多以群体称呼出现，属于人员账本颗粒度下降，不能据此判定有人被遗忘或死亡。
- 阮青禾、炉工、矿工/居民和裴照川的位置、利益与行动均持续推进；Ch10 State Delta 还主动保留炉渣残图/半截战旗归属的正文歧义为 UNKNOWN，没有人工补齐。
- 已兑现 promise 在 Ch10 明确从 Open Promises 移除（侧炉安置、总门通行等），新的移动炉场、古战场、追收和长期稳定性 promise 被新增；没有发现已兑现 promise 在多章无理由长期挂起。

## 高置信问题

1. Ch9 正文已经说总门形成可通过门洞，Ch10 又使用“先开门/最后封锁”语汇。Ch10 Canon 将其解释为最后封炉锁/残余封锁熔断，但正文入口语义仍可能让读者误读成同一扇门重复开启；这是局部 continuity/OPENING 说明机会，不是 State Delta 丢失。
2. Prompt/Context 规模持续增长，详见 `context-cost.md`；当前 Canon 内容自身保持可读、状态有更新，尚不足以判为 `CANON_CONTEXT_SYSTEM_UNSTABLE`。

`candidate-b/BOOK.md` 与 `runs/chapter-0010/BOOK_after_state_delta.md` 原文一致；最终 BOOK 是最后一次 State Delta 后状态。
