# Five-World Fantasy Blind Test v2

## 实验边界

- 仓库：`happyivanencoding/thegreatnovel`
- 分支：`principal_dev_new_sys`
- 本轮只到 Fantasy Seed、World Vision、Story Mainline，以及生成冻结后的三份盲审和一份 v1 ↔ v2 Meta Comparison。
- 不生成第一章、正文章节、逐章小纲、State Delta、Canon 或 Run Ledger。
- 不修改生产源码、旧实验目录或外部知识库。

## 生成输入边界

五个生成代理使用完全相同的 `INPUT.md` 和当前生产创意 Prompt。每个候选的三个阶段只读取自己的上游文件；生成阶段不读取其它候选、旧实验、旧审查、外部检索或其它灵感资料。

Seed、World Vision、Mainline 的原始 Prompt 与 Response 均保存在对应候选目录。五个候选全部结束后才生成 `final_world_and_mainline.md` 并冻结结果；盲审意见不回流候选。

## 候选目录

- `candidates/candidate-01/`
- `candidates/candidate-02/`
- `candidates/candidate-03/`
- `candidates/candidate-04/`
- `candidates/candidate-05/`

## 审查边界

- Blind Reviewer A：只读取五份最终方案，从男频读者角度审查，不数值评分。
- Blind Reviewer B：只读取五份最终方案，按实际故事结构审查主角驱动力、一级成长、非对称优势、高潮、限制收益、对手、终局收束。
- Blind Reviewer C：只读取五份最终方案，比较真实结构差异与同构。
- Meta Reviewer：盲审完成后才读取 v1 与 v2 的最终产物及三份盲审，形成对照。

## 停止点

不自动选择最终书，不自动批准任何候选，不根据审查结果修改生产系统。完成 Meta Comparison 后停止，等待作者判断。

## 完成记录

- TheGreatNovel commit：`a6e551460f1f13a8d42c44d43e8961b4f552958e`
- 实际生产 Prompt commit：`a6e551460f1f13a8d42c44d43e8961b4f552958e`
- 五个候选：`未生之身`、`借万古一刹`、`死人簿外`、`败相归我`、`借败成仙`。
- 五个候选的 Seed、World Vision、Mainline 原始 Prompt/Response 与修复后的 Final 均已保留。
- 正式盲审：`reviews/blind-reviewer-a-male-fantasy-reader.md`、`reviews/blind-reviewer-b-structure.md`、`reviews/blind-reviewer-c-diversity.md`。
- 正式 Meta：`reviews/meta-comparison-v1-v2.md`。
- 初次 Final 合并因终端大文件输出截断而产生污染；原始生成结果未被污染。污染版 Final、三份旧盲审和旧 Meta 已移入 `reviews/incident-truncated-final/`；修复后已用本地文件流重建 Final 并重新完成三份盲审与 Meta。
- 本轮没有查询 GBrain，没有读取 Reference Programs、旧 BOOK、旧候选或 Growth Genome；没有生成章节、逐章小纲、State Delta、Canon 或 Run Ledger。
- 本轮没有根据审查结果修改候选、生产 Prompt 或生产代码；停止等待作者判断。
