# Evidence Integrity Audit

## Provenance separation

本任务有两个不同基线，不能混写：

- Experiment generation base：`d4e2dd6f3377f967d8930480016f15a450b74e1b` 的 `books/real-exp-opening-pipeline-comparison-v2/` Git tree。它承载已生成的 clean v2 小说实验产物。
- Code audit base：本轮开始时 `origin/principal_dev_new_sys`，full SHA 为 `53394ea356393c904e82d988e7b5ae634d2487f7`。本轮没有修改生产 backend 或 frontend。

v2 目录当前不在 principal 工作树的 checkout 中，但它完整存在于上述历史 Git tree；本审计通过 `git show <commit>:<path>` 读取，不把历史实验目录恢复到 principal，也不把旧报告中的分支名当作本轮开发分支。

## Evidence classification

| evidence | scope | status | use |
|---|---|---|---|
| v2 candidate-c Chapter 1—3 manifest/execution/Primary/Specialist/Integrator/Final | 《掌中天工》三章局部 revision | CLEAN | 主因果归因与三章 Primary vs Final 盲读 |
| v2 candidate-b Chapter 1—3 execution | 《炉藏万象》三章 Primary-only control | CLEAN | 说明没有 Specialist/Integrator 时仍可有质量信号；不做 Primary vs Integrator |
| v1 candidate-b Chapter 2 selection/mismatch | declared selection 为空，但 Dialogue/Action/Integrator 后写入同一目录 | EXCLUDED_FROM_CAUSAL_VERDICT | 只说明 v1 污染边界，不用于本轮 Specialist 价值结论 |
| v1 candidate-c 旧并行 Chapter 2 正文路径 | 早于当前 Integrator 的并行文件 | EXCLUDED_FROM_CAUSAL_VERDICT | 不与 v2 正式 lane 混用 |
| v1 candidate-c Reader final label 与 system review 的表述冲突 | 旧书级 Hybrid review | SUPPORTING_ONLY / REVIEW_LABEL_CONFLICT | 只记录旧证据冲突，不替代本轮三章盲读 |
| v1 其它旧 Single/Hybrid 书级盲读 | 上一轮全链路问题 | SUPPORTING_ONLY | 不重新回答 Single vs Hybrid 总胜负 |

## Why v2 candidate-c is causal enough for this audit

v2 从已核对的 Chapter 1 后状态重新开始 Chapter 2，且 candidate-c 三章每章均有自己的 Primary、实际选中的 Specialist、Integrator 和最终正式正文。每章比较只在同一章、同一前置上下文内进行；因此不会制造跨章 Primary-only 连续 lane。

## Known contamination retained

旧 v1 的原始 evidence 不删除、不修复。尤其是 candidate-b Chapter 2 的 declared selection 与实际 Specialist/Integrator artifact 不一致，以及 candidate-c 旧 Chapter 2 并行文件，均保留在历史 Git tree 中，并在本目录标记为排除证据。
