# Five-Chapter Blind Test Efficiency

- 章节链路调用：35 次（每章 Director、Curator、Primary、2 Specialist、Integrator、State Delta）。
- 旧 Full Hybrid 主链：45 次；本轮减少 10 次，减少 22.2%。旧第1章 single control 不计入主链。
- Prompt 总字符：沈砚旧五章 Hybrid 主链 500,839；本轮 282,036；相对减少 43.7%。若把旧第1章 single control 也计入旧实验总量 516,020，则减少 45.3%；single control 不属于旧 Hybrid 主链。
- Response 总字符：旧 Full Hybrid 81,068；本轮 77,500；相对变化 -4.4%。
- Specialist Patch 总数：20；Integrator 运行 5/5；Primary 直接采用 0/5；State Delta 应用 5 次，其中当前 v2 格式复核通过 4/5，第4章原始 Response 缺少 State Delta Audit。
- 首次真实收益到账：第5章；旧账清零、退役独立炉心、临时接单牌和下一笔外单入口均已在正文与 Canon 中出现。

| 章 | 调用 | Prompt | Response | Specialist | Patch | 正文字符 | 段落 |
|---:|---:|---:|---:|---|---:|---:|---:|
| 1 | 7 | 37,640 | 10,720 | opening, action | 1 | 2,661 | 53 |
| 2 | 7 | 54,595 | 13,829 | dialogue, action | 4 | 2,626 | 81 |
| 3 | 7 | 57,556 | 14,926 | opening, action | 5 | 3,503 | 80 |
| 4 | 7 | 61,650 | 16,667 | opening, action | 5 | 3,889 | 132 |
| 5 | 7 | 70,595 | 21,358 | dialogue, action | 5 | 5,476 | 160 |

## Context Interpretation

本轮主链 Prompt 随前文正文增长而逐章变长，不能声称“跨五章单调缩小”。但与旧 Full Hybrid 同章基线相比，五章 Prompt 总量均明显更小；Primary 使用上一章全文与上上章章末投影，Specialist 只取职责片段，Integrator 只取有效 Patch。Runtime Reviewer 的“没有单调缩小”结论保留为限制，而不是把它误报成全链路压缩已证明。

## Recovery

`runs/recovery-demo/` 是明确标注的演示副本：第3章 Action 从 completed 标为 failed，复用 action_prompt.md 重试，attempts 从1到2；Director/Curator/Primary 保持 completed，Integrator 与 State Delta 标为 stale；正式 chapter-0003.md 和正式 manifest 未改。
