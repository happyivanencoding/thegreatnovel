# Opening Contract 默认生产执行链验证：Final Report

## 交付与基线

- 目标仓库：`happyivanencoding/thegreatnovel`
- 起始基线：`origin/principal_dev_new_sys`
- 起始 principal_dev_new_sys full SHA：`56dae5f6f94fc45899520071fb3c9117c5e4ce32`
- 实验分支：`opening-pipeline-comparison-v1`
- 实验产物提交 full SHA：`<INITIAL_EXPERIMENT_COMMIT_SHA>`（提交后回填）
- pushed：`<PUSH_RESULT>`（push 后回填）
- 本轮没有修改生产代码、生产 Prompt、`RunRequest.writer_mode` 或 UI 默认 Writer Mode。

## 冻结输入与对照

只使用两本：

- candidate-b：《炉藏万象》；
- candidate-c：《掌中天工》。

Hybrid lane 的 Fantasy Seed、World Vision、Story Program 和已验证 Outline/Future 10 直接来自 `real-exp-opening-three-chapter-hook-v1`；旧 Single 三章正文也来自该目录对应 candidate 的 `chapters/chapter-0001..0003.md`。

启动 BOOK 使用冻结 source 的设计区块，并复原旧 Single Pilot Chapter 1 Prompt 已证实的 clean state（故事尚未开始、无已完成摘要）；没有把旧实验正文状态喂给 Hybrid。

## Hybrid 实际执行

每章链路为：`Director → Chapter Prep → Context Curator → Primary Writer → 0—2 个实际 Specialist → Integrator（有有效 Patch 时）→ State Delta`。每个模型节点一次调用；token 无真实返回时严格写 `UNKNOWN`，不以字符数伪装。

| Lane / 章 | Specialist 实际选择 | Integrator | 最终来源 | 模型调用 |
|---|---|---|---|---:|
| 《炉藏万象》 / 1 | 无；四个 Specialist skipped | skipped | Primary | 5 |
| 《炉藏万象》 / 2 | declared=[]；实际有 dialogue、action，selection mismatch | adopted | Integrator | 8 |
| 《炉藏万象》 / 3 | action、emotion | adopted | Integrator | 8 |
| 《掌中天工》 / 1 | opening、action | adopted | Integrator | 8 |
| 《掌中天工》 / 2 | dialogue、action | adopted | Integrator | 8 |
| 《掌中天工》 / 3 | dialogue、action | adopted | Integrator | 8 |

两本三章的 input/output/total token 均为 `UNKNOWN`；每个节点的 `prompt_chars`、`response_chars` 见对应 `runs/chapter-NNNN/execution.json`。

candidate-b Chapter 2 的 Specialist/Integrator artifact 在 Ledger 同步前已由并行工作写入，Director declared selection 仍为空；其 Integrator 正文与 Primary Draft 完全相同。该事实保留在 `evidence/parallel-artifacts/candidate-b-chapter-0002-selection.md`，成本按实际 8 次调用记录，未删除或伪装为 clean selective 分支。

candidate-c 原路径下曾有一个早于当前 Integrator 的并行 Chapter 2 正文版本，已可逆归档至 `evidence/parallel-artifacts/candidate-c/chapter-0002.md`；当前正式正文与当前 Integrator/State Delta 保持一致。

## 盲读结果

盲读包去除了 Single/Hybrid 标签、路径、Prompt、Run、Review 和版本信息，并交叉放置 A/B；映射只在 `reviews/blind-reader-input/blind-reader-key.md`。

- 《炉藏万象》：`SINGLE_BETTER`。Single 在第一章钩子、人物取舍、对话/NPC 自主性、解释克制和整体连读感胜出；Hybrid 在异能首秀冲击与空间细节上有局部优势。
- 《掌中天工》：`HYBRID_BETTER`。Hybrid 在异能展示、对话/NPC、动作空间连续性和第三章资产/行动空间清晰度上胜出；Single 在主角算计感、解释克制和整体顶级开局感上胜出。

## System Review 后验结论

- Opening Contract 多节点放大：两本都观察到异能/反差/能力边界的重复强化；candidate-c 的 Hybrid 还明显增加护腕外部供能与限制解释。未发现 Specialist 将重复世界说明稳定写入正文；未发现 Integrator 把 result-stop 明显重新展开。
- 人物质感：candidate-b Hybrid 的 scene realization/空间连续性有局部提升，但人物与整体质量没有胜过 Single；candidate-c Hybrid 的对话、NPC 和 scene realization 提升更明显，但整体顶级开局感仍由 Single 获得。
- AI 解释：两本 Hybrid 都比 Single 增加解释；优势是机制更易复原，代价是发现感和自然度部分下降。
- 能力透支：两本均有累积透支；Hybrid 没有把能力完全写成无成本高光，但反复边界说明更明显。
- Chapter 4：未出现。两本正式 lane 只存在 Chapter 1—3。

System Reviewer 最终四选一：

`MIXED_NEEDS_LONGER_TEST`

两本方向相反，且 candidate-b Chapter 2 存在并行 selection mismatch，当前证据不足以改变默认 Writer Mode。本轮没有修改默认值，也没有进入十章实验。

## 验证

- 实验前完整测试：`164 passed in 0.96s`。
- 实验后完整测试：`168 passed in 0.77s`。
- 实验脚本 `py_compile`：通过。
- 六个 Hybrid run：manifest `run_status=completed`。
- `BOOK.md` 与每章 `BOOK_after_state_delta.md`：一致。
- 正式章节与当前 `final_formal_prose.md`：一致。
- Chapter 4 路径：不存在。

## Git

本报告生成时工作树包含本实验 v1 和同一分支并行新增的 v2；按作者明确指示最终使用 `git add -A` 一并提交并 push。最终 clean status 与 push 结果在提交后回填本文件。
