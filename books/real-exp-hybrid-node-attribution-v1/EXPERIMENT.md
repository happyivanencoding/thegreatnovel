# Hybrid Node Attribution Audit

## 目标

本审计只回答：在已经生成好的 `hybrid_selective` 章节中，`Primary Draft → Specialist Patches → Integrator Final` 是否稳定改善正文。它不重新生成小说正文，不重跑任何章节节点，不比较新的 Single vs Hybrid 总胜负，也不修改生产代码。

## Git 与来源

- 工作分支：`principal_dev_new_sys`
- Code audit base：`53394ea356393c904e82d988e7b5ae634d2487f7`
- Experiment generation base：`d4e2dd6f3377f967d8930480016f15a450b74e1b`
- clean v2 Git tree：`books/real-exp-opening-pipeline-comparison-v2/`
- v1 Git tree：`books/real-exp-opening-pipeline-comparison-v1/`
- v2/v1 均通过 Git tree 只读读取；没有 checkout、覆盖或修改旧实验产物。

## 样本与边界

- 主归因样本：clean v2 `candidate-c`《掌中天工》Chapter 1—3。
- 每章独立比较该章自己的 Primary Draft 与 Integrator Final；不把三章 Primary 拼成不存在的连续 lane。
- 控制证据：clean v2 `candidate-b`《炉藏万象》Chapter 1—3；三章 Integrator 均 skipped、最终来源均为 Primary，因此不伪造 Primary vs Integrator 对。
- 不生成 Chapter 4，不调用 Director、Chapter Prep、Curator、Primary、Specialist、Integrator 或 State Delta。

## 方法

1. 从 frozen v2 Git tree 确定性提取 Primary Draft、Specialist Response、Integrator Response、manifest、execution 和最终正式正文。
2. 以交叉位置生成每章匿名 A/B pair；key 与 Reader 输入分离。
3. 由三个相互独立的盲读 Reader 分别阅读一章，只输出 A/B/MIXED，不打分。
4. 用字符级和段落级确定性 diff 记录 Primary→Final 变化，再结合 Specialist 原始 Patch 与 Integrator 实际 Final 做 attribution；不接受 Integrator Audit 的自我声称作为唯一证据。

## 产物

- `evidence-integrity-audit.md`：证据完整性与排除边界。
- `blind/`：三章匿名 A/B pair、独立 Reader review 与盲位 key。
- `metrics.json`：Primary/Final 长度、diff size、段落变化、调用和 proposed patch 观察值。
- `patch-attribution.md`：逐 Patch 的实际采用与最终文本变化。
- `FINAL_REPORT.md`：三章盲读、控制证据、归因结论和四选一架构 Verdict。
