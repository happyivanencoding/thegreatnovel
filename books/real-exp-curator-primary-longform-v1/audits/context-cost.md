# Prompt / Context 成本审计

Prompt chars 来自每章 `execution.json` 的正式节点记录；`fallback_prompt_chars` 来自仅 render 的 `primary_fallback_prompt.md`。Fallback 从未调用模型。

| 章 | Director | Prep | Curator | Curated Primary | State Delta | 总 prompt | Fallback Primary | Curator chain | Primary/Fallback |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 6,429 | 27,655 | 11,726 | 29,507 | 9,406 | 84,723 | 29,649 | 41,233 | 0.99 |
| 5 | 16,678 | 42,890 | 21,432 | 35,177 | 10,766 | 126,943 | 45,105 | 56,609 | 0.78 |
| 6 | 17,151 | 49,505 | 21,731 | 41,521 | 10,639 | 140,547 | 52,052 | 63,252 | 0.80 |
| 7 | 17,612 | 55,454 | 22,293 | 48,072 | 13,887 | 157,318 | 58,650 | 70,365 | 0.82 |
| 8 | 18,510 | 64,794 | 23,181 | 58,100 | 16,479 | 181,064 | 68,645 | 81,281 | 0.85 |
| 9 | 19,067 | 75,730 | 23,450 | 68,707 | 15,271 | 202,225 | 80,108 | 92,157 | 0.86 |
| 10 | 19,874 | 85,209 | 23,893 | 78,712 | 16,554 | 224,242 | 90,053 | 102,605 | 0.87 |

## 观察

- Chapter 4→10 总 prompt 从 84,723 增至 224,242 chars；七章合计 1,117,062 prompt chars。实际 response chars 合计 133,498；actual token counts 均为 `UNKNOWN`，没有用字符数冒充 token。
- Prep 是增长最大来源之一：27,655→85,209（3.081×）。实验编排器的 `previous_prose()` 会把既有章节正文传入生产 prompt；Chapter Prep 还把它作为连续性上下文，因而前文正文随章节累积是主要来源。
- Curated Primary 从 29,507→78,712（2.668×），deterministic fallback 从 29,649→90,053（3.037×）。增长来源还包括当前 BOOK/Canon、当前章计划、最近正文和 Curator/计划投影；本轮不优化这些输入。
- Curator chain（Curator prompt + Curated Primary prompt）从 41,233→102,605。实际 Primary 相对 fallback 的观测比率在 Ch5—10 为 0.78—0.87，说明 Curator 对最终 Writer Context 有压缩/筛选价值；Ch4 处在链条刚开始，比例为 0.99。
- State Delta prompt 也从 9,406 增至 16,554，但没有出现解析失败或 Canon 断裂。增长是压力测试发现，不是本轮的修复目标。

## 结论

上下文成本存在明显增长，应该进入后续 runtime 优化议题；但本轮没有无界增长导致的运行中断、关键事实丢失或多章状态错误，因此不判 `CANON_CONTEXT_SYSTEM_UNSTABLE`。不得把本轮 deterministic fallback render 误记为额外模型 call。
