# Freeze Snapshot v2

上游冻结输入来自 `real-exp-opening-pipeline-comparison-v1` 的 `source/` 与 `outline/` 副本；这些文件在 v1 运行期间未作为响应写入目标。两本的 `BOOK.md`、Chapter 1 正文、Chapter 1 `runs/` 与 `_operation/` 来自 v1 已完成且 manifest/正文可核对的 Chapter 1 State Delta 之后状态。

v2 从 Chapter 2 开始，避免读取 v1 Chapter 2 的任何 Prompt、Response、manifest 或 BOOK 状态。`tools/experiment_runtime.py` 的实验根目录已指向 v2。

| lane | 书名 | Chapter 1 final source | v2 起始状态 |
|---|---|---|---|
| candidate-b | 《炉藏万象》 | primary | Chapter 1 State Delta 已应用 |
| candidate-c | 《掌中天工》 | integrator | Chapter 1 State Delta 已应用 |
