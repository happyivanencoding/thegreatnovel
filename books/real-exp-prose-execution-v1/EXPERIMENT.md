# Frozen Upstream + 3-Chapter Execution & World Engine Test v1

## 实验目标

在不重新设计上游、不修改生产 Prompt 或运行时的前提下，使用《掌中天工》candidate-b 的 Dynamic Pacing Treatment 作为冻结输入，顺序执行前三章，观察正文是否把上游承诺转成可继续阅读的实际事件；同时只对前三章给出 `WORLD_ENGINE_OBSERVATION` 的 Early Signal。

## 冻结边界

- 本目录是本轮唯一写入目标；生产源码、生产 Prompt 注册、GBrain、Growth Genome、Frozen 上游和正式 Canon 不在修改范围内。
- 不查询 GBrain，不注入 Inspiration Results，不读取 Reference Programs。
- 不生成 Candidate A，不重新生成 Future 10，不在正文生成前优化任何章节局部。
- Chapter 1、2、3 严格串行；每章只执行一次。只有基础设施失败才允许用完全相同的已保存 Prompt 重试。
- 三章全部冻结后才运行审查；审查只读正文或指定的上游/运行产物，不修改正文、State Delta 或 Canon。
- 本轮完成后停止，不进入第 4 章。

## 冻结来源

正式来源位于 `source/`：

- `fantasy_seed.md` ← `books/real-exp-dynamic-pacing-v1/candidate-b/legacy_seed.md`
- `world_vision.md` ← `books/real-exp-dynamic-pacing-v1/candidate-b/treatment_world_vision.md`
- `story_program.md` ← `books/real-exp-dynamic-pacing-v1/candidate-b/treatment_story_program.md`
- `outline.md` ← `books/real-exp-dynamic-pacing-v1/candidate-b/treatment_outline.md`

`outline.md` 是 Dynamic Outline；`control_outline.md` 不进入本实验。根目录 `BOOK.md`、`FANTASY_SEED.md`、`WORLD_VISION.md`、`PROPOSAL.md` 是供当前真实生产 Prompt 工作台读取的对应运行副本。

## 真实执行链

本轮使用当前分支的正式 Prompt 渲染函数、Run Ledger、章节保存和 State Delta/Canon 应用逻辑。每章保留实际运行节点：

`Frozen Future 10 → Chapter Prep / Director → Context Curator → Primary Writer → 0—2 个作者选择的 Specialist → Revision Integrator（有有效 Patch 时）→ 正式正文 → State Delta / Canon`

`PROMPTS.md` 由当前分支的默认 Prompt 注册生成；每次模型调用前先保存完整 rendered prompt，再把同一文本交给对应的真实独立子代理。各子代理只接收自己的生产输入，不接收本实验的审查标准、实验解释或后续 Reviewer 输出。

## 产物边界

- `runs/chapter-000N/` 使用当前正式 Run Ledger 文件名，记录节点 Prompt、Response、manifest 和最终来源。
- `chapters/chapter-000N.md` 只保存正式正文。
- `reviews/` 只在三章正文和 State/Canon 连续性冻结后写入。
- `_operation/` 仅用于真实子代理的隔离中间输出，不作为正文、Canon 或 Reviewer 输入。
