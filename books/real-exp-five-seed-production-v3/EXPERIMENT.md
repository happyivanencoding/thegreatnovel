# Production-Mode Five-Seed Diversity Test v3

## 实验目的

只验证当前真实生产模式下，正式 Fantasy Seed Prompt 在同一次调用中生成五个候选时，是否自然产生足够不同的故事设计。

## 固定边界

- 仓库：`happyivanencoding/thegreatnovel`
- 分支：`principal_dev_new_sys`
- 生产 Prompt commit：`a6e551460f1f13a8d42c44d43e8961b4f552958e`
- v3 开始时 HEAD：`f979ced25ce24b3d856f71d1f6ca77b56a6d3aad`
- 不修改生产 Prompt、源码、GBrain 或旧实验目录。
- 不调用 GBrain，不读取 Reference Programs、BOOK、Growth Genome 或其它旧资料。
- 只进行一次 Fantasy Seed 生成调用；同一 response 内完整输出五个候选。
- 不生成 World Vision、Story Program、Mainline、Outline 或章节。

## 输入与调用

生成代理只读取 `INPUT.md` 与 `fantasy_seed_prompt.md`。调用前不分配候选类型，不提示反偏置，不读取旧实验或审查。

生成后立即保存完整原始 response 并机械拆分五份候选；冻结后才启动盲审。

## 审查顺序

1. 独立 Blind Diversity Reviewer 只读取五份冻结后的候选。
2. Blind Review 完成后，独立 Meta Reviewer 才读取 v2 Seed、v2 盲审结论、v3 Seed 与 v3 盲审，完成 Seed-only comparison。

## 停止点

只报告实验事实与三档产品判断：有效、部分有效、效果不足。不自动选择候选，不修改系统，不开始下一实验。
