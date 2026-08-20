# Freeze Snapshot

## 仓库与生产基线

- branch：`principal_dev_new_sys`
- experiment start HEAD：`5992f62d11e8014c3cf783bf993589e1cb881585`
- frozen upstream baseline：`CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2`
- Long-Form Pacing production baseline：`2c1e3434b6d68043ba0aac556e63d7912ba23368`
- 本快照建立时生产源码未修改；本轮只允许新增实验产物。

## Frozen Upstream

- 书名：`《掌中天工》`
- 选择：`books/real-exp-dynamic-pacing-v1/candidate-b/`
- 版本：Dynamic Pacing Treatment
- Fantasy Seed：`legacy_seed.md`
- World Vision：`treatment_world_vision.md`
- Story Program：`treatment_story_program.md`
- Frozen Outline：`treatment_outline.md`
- Control Outline：明确排除，不读取、不复制进运行输入。
- Frozen Future 10：直接使用 `treatment_outline.md` 中的 `# 未来十章逐章小纲`，不重新生成。

## Runtime 初始状态

- 运行书目录：`books/real-exp-prose-execution-v1/`
- 运行模式：`hybrid_selective`
- Creative State：三份上游产物均标记为 `author_approved`，仅用于满足当前工作台的批准边界；没有把模型生成或普通保存当成批准。
- 正文、State Delta 和 Canon 在实验开始前均为空/未完成；前三章之前不读取其它实验的正文或 Reviewer 结论。
- GBrain、Inspiration Results、Reference Programs：空。

## 运行纪律

1. 每个 Director、Chapter Prep、Writer 及其真实 Hybrid 节点先渲染并落盘完整 Prompt。
2. Chapter 1 完成 State Delta/Canon 应用后，才生成 Chapter 2；Chapter 3 同理。
3. 不因内容质量重试、不手工润色、不让 Reviewer 指导下一章、不换模型、不挑选多个结果。
4. 三章全部完成后才开始 Blind Reader、Execution Fidelity、World Engine、AI味和 Cross-Chapter 审查。
