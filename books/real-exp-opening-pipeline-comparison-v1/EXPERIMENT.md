# Opening Contract 默认生产执行链验证

本实验只比较同一份 Opening Three Chapter Contract 在两条真实执行链中的结果：

- 对照：`books/real-exp-opening-three-chapter-hook-v1/` 中已经完成并验证的 Single Writer 三章；
- 实验：本目录中新建的 `hybrid_selective` 三章。

本轮只使用两本冻结样本：

- candidate-b：《炉藏万象》；
- candidate-c：《掌中天工》。

本轮不重新生成 Fantasy Seed、World Vision、Story Program 或 Outline，不修改旧 Pilot，不修改 `src/`、生产 Prompt、`RunRequest.writer_mode` 或 UI 默认 Writer Mode，不运行 Chapter 4。

## 执行边界

每本从与旧 Single Pilot 相同的 clean state 开始独立运行三章：

`Director → Chapter Prep → Context Curator → Primary Writer → 0—2 个实际选中的 Specialist → Integrator（有有效 Patch 时）→ State Delta`

Chapter Prep 是本实验的真实前置节点；其余章节节点使用当前 `hybrid_selective` 的正式 Prompt 与 `run_ledger`。每个节点只调用一次，不因文学质量重试，不人工改正文，不把 Single 版本正文、旧 Review 或 Reviewer 标准注入 Hybrid Prompt。

每章使用该 lane 自己上一章的正文、State Delta 应用后的 BOOK、Canon 和最近摘要；实验副本的 `BOOK.md` 与 `chapters/` 是唯一连续上下文来源。初始 `BOOK.md` 保留冻结 source 的设计区块，但把状态区复原为旧 Single Pilot 实际使用并在 Chapter 1 Prompt 中留下证据的 clean state。出现确定性生产错误时，保留原始错误证据并停止相关 lane。

`tools/experiment_runtime.py` 只做实验编排：渲染正式 Prompt、接收隔离响应、调用既有解析/保存函数、写出执行记录；不实现第二套 Runtime，也不调用模型。

## 成本记录

每章的 `runs/chapter-NNNN/execution.json` 记录实际节点、skipped 节点、Specialist 选择、Integrator 状态、最终来源、调用次数和字符数。当前子代理执行环境不返回模型 token 明细，因此所有 input/output/total token 字段严格记录为 `UNKNOWN`；`prompt_chars` 和 `response_chars` 只作为字符数观察值。

## 后验观察

只观察并记录 Opening Contract 是否被多节点重复放大：能力重复强化、已完成 payoff 被 Integrator 再解释、Specialist 重复世界说明、反差重复强调、第一章能力透支、主角被统一成正确执行器、或 result-stop 被后续节点重新展开。不写自动评分器或质量 Gate。

## 停止边界

两本各完成 Chapter 1—3、执行记录、去标识盲读材料和系统结论后停止。最终结论只能从任务规定的四个值中选择；本轮不据此修改默认 Writer Mode。
