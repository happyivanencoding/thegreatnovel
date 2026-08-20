# Five-World Fantasy Bias Blind Test v1

## 实验边界

- 仓库：`happyivanencoding/thegreatnovel`
- 分支：`principal_dev_new_sys`
- TheGreatNovel HEAD：`bb5361519929c996aa386672897bc98756e02a51`
- 基线：`133 passed`；`python -m compileall src/story_mvp` 通过；`node --check src/story_mvp/static/app.js` 通过。
- 本实验只生成五个 Fantasy Seed、五个 World Vision、五条世界观与故事主线，以及盲审报告。
- 不生成章节、第一章、逐章小纲、八字段、State Delta、Canon、Chapter Run Ledger 或正文。
- 不创建 BOOK.md、PROMPTS.md 或 chapters/。
- 不修改 TheGreatNovel 源码、旧实验书、章节、GBrain 数据库、GBrain 蒸馏 Prompt 或 Hermes CLI。

## GBrain 基线记录

- Hermes 工作目录：`C:\GoogleDrive\hermes\gbrain`
- Hermes Git HEAD：`708c8e0c03882c7f165f007b6dfe8901af3db735`
- Hermes 工作树：已有 `src/core/embedding.ts` 修改；已有未跟踪 `brain.pglite/` 与 `finance-history-300years.md`，均不属于本实验。
- CLI：`gbrain 0.18.1`
- 数据库：`C:\Users\jingx\.gbrain\brain.pglite`
- 当前 stats：Pages `3695`；Chunks `15623`；Embedded `15623`
- Doctor embedding：`100% coverage, 0 missing`
- 查询后只读复核 stats：Pages `3687`；Chunks `15611`；Embedded `15611`。本实验没有执行 sync/embed/import/put/delete 等写入命令；查询期间数据库状态发生漂移，无法仅凭本轮证据归因于并发状态还是 GBrain 查询过程，故按外部状态漂移记录。
- 偏向诊断报告：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus\operations\distillation-bias-correction-v1\bias_diagnosis.md`
- 最新旧/新比较记录：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus\operations\distillation-bias-correction-v1\old_new_comparison.md`

## 隔离规则

五个生成代理只接收 `INPUT.md` 和当前生产 Fantasy Seed/World Vision 模板，以及自己的上游产物。它们不读取其它候选、旧实验、Reference Programs、GBrain、Growth Genome、BOOK 或 Proposal。

World Vision 在实验中标记为 `EXPERIMENT_LOCKED_WORLD_VISION`，不等于作者正式批准。GBrain 只在五份 World Vision 完成后，以低权威灵感进入对应主线设计。

## 停止点

最终盲审完成后停止在作者审查点：不自动选择最终作品、不自动批准任何候选、不生成百章大纲或章节、不修改源码或 GBrain。

## 完成记录

五个 Fantasy Seed：

1. `candidates/candidate-01/fantasy_seed_response.md` · 《无终天火》
2. `candidates/candidate-02/fantasy_seed_response.md` · 《无名执天》
3. `candidates/candidate-03/fantasy_seed_response.md` · 《无坠之骨》
4. `candidates/candidate-04/fantasy_seed_response.md` · 《未尽之骨》
5. `candidates/candidate-05/fantasy_seed_response.md` · 《未尽天》

五个 World Vision 与五条主线已分别保存在每个候选目录；每个候选另有 `final_world_and_mainline.md` 汇总。五次 GBrain accepted 均为 0，query/raw/accepted/rejected 均已保存。

真实独立生成代理：

- Fantasy Architect 01—05：`01a01e8b-ecd7-7be1-917c-368092aaf305`、`01a01e8b-edff-7332-b1da-d07c8f15e721`、`01a01e8b-efb3-7583-bf4b-7e65990c9e7d`、`01a01e8b-f174-7f70-a3f6-7f1bb2bafc31`、`01a01e8b-f338-7b11-b59d-311d3b257a92`
- World Vision 01—05：`01a01e92-a810-7373-901b-904ddcad9a24`、`01a01e92-a936-7bc2-9130-362079e68972`、`01a01e92-ab01-7571-849c-c1b25d0ea81c`、`01a01e92-accf-7de1-91e1-fd1bdc5ca8f8`、`01a01e92-aea2-7290-a6ff-7a4d28215cc7`
- Story Mainline 01—05：`01a01ea3-6fe0-71a2-99b7-b36984ff1781`、`01a01ea3-7113-7090-bdac-fb12878f8d10`、`01a01ea3-72c3-7af1-8638-68c80ed89776`、`01a01ea3-7473-75d0-92a4-adc478153e96`、`01a01ea3-7617-7a11-beb6-e8e6d5cc8f93`

盲审文件：`reviews/system-bias-review.md`、`reviews/gbrain-distortion-review.md`、`reviews/male-fantasy-reader-review.md`、`reviews/diversity-review.md`、`reviews/final-comparison.md`。没有重复候选重生成；Candidate 04/05 保留为高重复风险样本。没有生成章节。
