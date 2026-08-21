# Parallel artifact evidence

同一工作树上存在并行开发写入的实验产物。为保持当前 run 的响应、最终正文和连续上下文一致，发生冲突的旧文件只做可逆归档，不删除：

- `candidate-c/chapter-0002.md`：原路径文件早于当前 Chapter 2 Integrator 响应，正文末尾存在可见差异；已保留为冲突证据。

当前正式 lane 使用各自 `runs/chapter-0002/final_formal_prose.md` 与对应 State Delta；并行旧文件不再进入 Chapter 3 Prompt。
