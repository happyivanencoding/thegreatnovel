# Compounding Growth + Narrative Momentum Downstream Survival Test v1

## 实验性质

本目录是一次冻结 Creative Prompt 的诊断实验，不是 Prompt 优化。生成完成并审查后停止，作者决定是否进行后续修改。

## 开始时的生产基线

- branch：`principal_dev_new_sys`
- 开始时 HEAD：`c99f2d668de45f77a04b14b78cc0d23aa1f71781`
- Compounding Growth Engine 提交：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- Clean Compounding Seed Test 提交：`32eba11bbec102e05562e24861e0cea8506c8f7a`
- `e2e3bac` 是当前 HEAD 的祖先；该提交修改 `src/story_mvp/prompts.py` 中的生产创意 Prompt，并由后续 `32eba11`、`c99f2d6` 延续。
- 开始时 Git status：工作树干净。

## 不可修改边界

本轮不修改 `FANTASY_SEED_TEMPLATE`、`WORLD_VISION_TEMPLATE`、`STORY_PROGRAM_TEMPLATE`、`COMPOUNDING_GROWTH_DIRECTION`、Outline Prompt、Review Prompt、Chapter Prompt、GBrain、Canon、State Delta、Growth Genome 或其它生产代码。

## 实验问题

1. Personal / Future Asset、Production Asset、World / Territory Asset 三种不同增长家族，能否完整穿过 Fantasy Seed → World Vision → Story Program，并在大型阶段之间形成真实复用、净新增和反哺。
2. 在不把 Narrative Momentum 告知生成代理的情况下，当前 Story Program 是否自然产生主角行为指纹、跨阶段关系变化和会制造后续事件的社会反馈。

## 候选与输入隔离

本轮只使用上一轮真实作者方向和 `real-exp-five-seed-production-v5` 中已冻结的三个 Seed：

- Candidate A：`《偷走明天的人》`，Personal / Future Asset。
- Candidate B：`《掌中天工》`，Production Asset。
- Candidate C：`《吞界行舟》`，World / Territory Asset。

World Vision 代理只能读取 `INPUT.md`、本候选 `fantasy_seed.md` 和当前正式 `WORLD_VISION_TEMPLATE`。Story Program 代理只能读取 `INPUT.md`、本候选 `fantasy_seed.md`、本候选 `world_vision_response.md` 和当前正式 `STORY_PROGRAM_TEMPLATE`。Reviewer 只在全部生成冻结后读取三份本候选产物，不读取 Prompt。

本轮不调用 GBrain，不读取 Reference Programs、其它候选、历史实验、Outline、Canon、State Delta 或 Growth Genome。每个生成阶段每个候选只调用一次，不自动重生成。

## 完成顺序

1. 固化作者方向和三个逐字 Frozen Seed。
2. 三个独立 World Vision Agent 各生成一次，并立即冻结。
3. 三个独立 Story Program Agent 各生成一次，并立即冻结。
4. 三份 Story Program 全部冻结后，分别启动 Compounding Reviewer 与 Narrative Momentum Reviewer。
5. 由主 Agent 依据冻结产物完成 Cross-Candidate Review、Final Verdict 和提交复核。

## 验收边界

审查只报告实际文本中能找到的因果、资产复用、人物行动、关系变化和社会后果；不能用 Seed 理论推演补足 Story Program 中缺失的事件。最终分别给出 Compounding 判定、Narrative 判定和 Story Program 修改档位，不执行任何 Prompt 修改。

## 执行结果

- 三个独立 World Vision Agent：各 1 次生成，已冻结。
- 三个独立 Story Program Agent：各 1 次生成，已冻结。
- 三个 Compounding Reviewer、三个 Narrative Momentum Reviewer、一个 Cross-Candidate Reviewer：均已完成。
- Compounding：A/B/C 均 `SURVIVES_DOWNSTREAM`。
- Narrative：A `NARRATIVE_THIN`，B/C `NARRATIVE_HEALTHY`；总体 `NARRATIVE_HEALTHY`，未形成 `NARRATIVE_SYSTEMIC_GAP`。
- Story Program 修改档位：`NO_CHANGE_NEEDED`。
- 生产源码和测试无 diff；本轮只产生本目录 26 个实验文件。
- 生成结束后停止，不自动修改系统。
