# tgn-system-steward 0.3.29 Exact-Input Receipt Narrow Smoke

VERDICT: PASS

KNOWLEDGE_CLASS: CURRENT DEFAULT（仅限 exact-input stale-recovery 正确性）

WHY: Receipt 不绕过 conservative stale graph，而是在节点被判 stale 后重新构建 bounded Prompt。只有新 UTF-8 Prompt 的 SHA-256 与旧 receipt 一致，且磁盘 Response 的 SHA-256 与 receipt 一致，才允许复用。缺 receipt、失败状态、任一摘要不一致或作者明确 retry/resample 时均 fail closed 重跑。命中后直接使用相同 Response bytes，UI/API 路径实际为 0 次 LLM 调用，因此不存在生成差异或 Reader/Authority A/B 差异。6 个核心 negative/positive tests、API/UI tests 和 full suite 447 passed 支持该实现闭环。真实 author-edit stale case 还验证了 D/C/P 的 exact Prompt 重建、3/3 Response 保持和 0 calls。由此，receipt 作为字节级恢复机制可以冻结为 Current Default，其收益应归类为增量恢复收益。

FREEZE: 保留“先 stale、后 exact Prompt 校验、再 Response 校验、失败即重跑”的 fail-closed 链路；不得把 receipt 节省计入首次生成加速。

SEPARATE_UNPROVEN: 不判断跨书命中率与收益频率；不据此证明正常首次生成的 wall-clock 或成本改善；bounded projection 是否完整属于独立的 projection correctness 问题，不由 receipt 负责。

- wall_seconds: 75.197
