# TheGreatNovel Curator → Primary 长篇连续稳定性测试

实验对象：`《炉藏万象》`，Chapter 4—10。

本实验验证 Opening Contract 结束后的简化核心链：

`Director → Chapter Prep → Context Curator → Primary Writer → adopt Primary → State Delta`

## 冻结边界

- 开发分支固定为 `principal_dev_new_sys`，不创建新分支。
- Chapter 1—3 使用历史 v2 clean tree 的 `candidate-b`，不重新生成。
- 生产 Prompt、Writer runtime、状态/存储/ledger、OpenAI executor、前端和前端 tests 不修改。
- 只运行 `《炉藏万象》`，不运行 `candidate-c/《掌中天工》`。
- Chapter 4—10 每章每个核心节点单次调用；不运行 Opening、Dialogue、Action、Emotion Specialist、Integrator、Reviewer-as-generator 或 Primary-Fallback generation。
- 不重写 Future 10；不人工润色、修正文、补对白或改变下一章输入。
- State Delta 只更新本实验副本的 `candidate-b/BOOK.md`。

## Frozen input

输入来自 `SOURCE_MANIFEST.json` 指定的历史 commit `d4e2dd6f3377f967d8930480016f15a450b74e1b`。该 tree 的 Chapter 3 已完成 Curator → Primary 运行，`final_source=primary`，Specialists 与 Integrator skipped，State Delta 已应用。

## 运行与证据

每章保存 Director、Chapter Prep、Curator、Primary、State Delta 的 prompt/response、正文、事实摘要、State Delta 后 BOOK 和 `execution.json`。`tools/experiment_runtime.py` 只负责调用当前 `src/story_mvp` 的正式 prompt、正文解析、ledger 和 storage 函数；它不调用模型，模型响应由隔离的真实 `luna_worker` 单次写入 `_operation/` 后原样接入。

正常预算是 7 × 5 = 35 个 content calls。actual token 在当前 executor/worker 证据不可得时记为 `UNKNOWN`，不从字符数推算。

## 停止条件

Chapter 10 完成并且两个独立后验 Reader、逐章审计和 FINAL_REPORT 完成后停止。不得生成 Chapter 11，不得修改生产默认值或 Prompt。
