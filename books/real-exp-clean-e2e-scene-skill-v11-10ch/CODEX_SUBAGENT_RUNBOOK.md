# Codex Subagent Runbook

此文件是执行约定，不是额外 Prompt 层。

## LLM 执行方式

本实验所有 LLM 节点必须使用 Codex subagent。不要调用 OpenAI API、`openai_executor.py`、HTTP 模型服务或其它外部 provider。

每个节点：

1. 用当前生产 `generate_prompt()` 生成实际 Prompt；
2. 先把 Prompt 保存到实验目录；
3. 启动一个独立 subagent，只给它这个 Prompt；
4. 原样保存 Response；
5. 使用当前生产确定性 parser / storage 逻辑提取和应用结果；
6. 成功后进入下一节点。

不同节点不要让 subagent 读取其它实验组或 Reviewer 结论。

## 新书阶段

依当前生产审批/选择约束完成：

- Fantasy Seed
- World Vision
- Story Program / Idea
- Outline

如果某个生产节点需要“作者批准”才能继续，实验允许使用明确记录的实验审批夹具把该节点输出标记为本轮选定输入；不要把它描述成真实用户人工批准。不要额外调用 blind reviewer 反复挑选，除非当前生产流程本身必须如此。

## Chapter 1—10

对每章依次执行：

1. Director
2. Context Curator
3. 解析并记录 `Scene Skill Selection`
4. Primary Writer
5. 解析 `Primary Draft` / `Primary Fact Summary`
6. 保存正式 `chapter.md`
7. State Delta
8. 应用到实验 `BOOK.md`
9. 下一章

不要并行生成多个章节；Chapter N+1 必须使用 Chapter N 已应用后的 Canon / State。

## 重试

只允许执行级失败重试一次：subagent 报错、空返回、明显截断、写入失败或 parser 因截断无法得到要求区块。

以下情况不得重试：写得普通、Curator Skill 选择看起来不理想、人物反应不够强、剧情没有想象中爽、正文有真实质量缺点。

## 十章完成后

先运行 `verify_experiment.py` 获取确定性 trace，再由独立 Reviewer subagent 阅读十章正文和必要规划/状态，写 `FINAL_REPORT.md`。Reviewer 不自动重写任何章节。
