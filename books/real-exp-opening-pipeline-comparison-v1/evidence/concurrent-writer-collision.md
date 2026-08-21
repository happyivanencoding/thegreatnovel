# Concurrent writer collision evidence

本目录原本是有效未完成实验，但 Chapter 2 后半段出现了同一目录的并行写入冲突。主 lane 已确认 candidate-b Director 选择为空，并完成 Primary-only `finish`；随后 candidate-b 的同一 `runs/chapter-0002/` 与 `_operation/chapter-0002/` 又出现 Dialogue、Action、Integrator 文件，manifest 最终同时显示 `selected_specialists: []`、Specialist completed、`final_source: integrator`。

这些异常文件的正文角色仍属于《炉藏万象》（沈燧），不是 candidate-c 串书；问题是同一实验目录被两条执行流并行写入，不能作为可归因的 Single vs Hybrid 证据。没有删除、覆盖或修复 v1 产物。本轮从 v1 两本已完成且可核对的 Chapter 1 结果复制冻结输入到 `real-exp-opening-pipeline-comparison-v2`，从 Chapter 2 重新开始。
