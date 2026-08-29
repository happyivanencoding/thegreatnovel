# TGN Chapter Latency Innovation｜实验协议

> 日期：2026-08-29

## 目标

不是单纯让模型更快，而是在不损失以下高价值语义的前提下缩短章节关键路径：

- 主角主动性与私人欲望；
- Power Asymmetry、精确力量尺与 Public Proof；
- Reward / Ownership / Money / Identity 真正到账；
- Actor → Action → Object；
- Direct Result / State Change / Ending；
- Reader Release 与未知边界；
- 关系变化、Surprise 与商业追读力；
- Canon、World、Power、Human Authority。

## 冻结输入

主样本：`real-exp-fast-world-20ch-20260828-v1`。

跨书样本：`real-exp-current-pipeline-authority-reviser-0010-20260828-v1`。

Control 为当前 production 五节点链：

`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`

每项实验尽量冻结其它模型、effort、Chapter Mission、Canon、World / Power / Human Authority、Reader Release、Primary Draft 或最终下游，只改变一个可归因变量。

## 测试路线

1. 并行化：Pre-Curator、Authority Watch、Speculative Director、State 并行、Reader Polish 并行。
2. Authority 前移：Authority Blueprint → Primary。
3. 输出协议变化：Paragraph Delta、Paragraph Manifest、Combined Reviser + State。
4. 模型替换：Full Curator Terra high、State Terra low。
5. 上下文预编译：Ten-Chapter Attention Kernel。
6. 基础设施：Persistent ACP process reuse。

## 证据要求

任何有语义影响的快路都必须：

1. 接回正常下游，比较**最终正文**，不能只看中间包；
2. 同时做匿名商业 Reader 与 Authority / Canon blind；
3. 计算完整 critical path，不只报某一节点；
4. 把 fallback、discard、并行双路与重跑成本算入；
5. 随机稀疏修改至少独立 repeat；
6. 高潜路线增加 cross-book；
7. Reader 赢而 Authority 输，或 Authority 赢而 Reader 输，只能判 PARTIAL；
8. 一个压力章出现 actor / object / result / ownership / power / ending hard violation，即阻止全局 production freeze。

## 速度口径

所有数字都是当前冻结样本上的 Codex ACP wall-clock；不是 Direct API SLA，也不能跨执行后端外推。相对速度与质量结论分开报告。

## Production Gate

只有当 Treatment：

- 无稳定 hard violation；
- Reader 与 Authority 同时不劣；
- repeat / cross-book 不退化；
- 完整关键路径有实质收益；
- 不新增一个成本接近收益的常驻 Agent；

才允许改变 production 默认。否则保留为 Experimental Hypothesis。
