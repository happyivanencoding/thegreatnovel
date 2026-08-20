# Freeze Creative Chain + Outline Eventization Survival Test v1

## 实验性质

本轮是冻结 Creative Chain 后的 Outline 层诊断实验。只验证当前正式 `OUTLINE_TEMPLATE` 能否把已冻结的 Fantasy Seed、World Vision、Story Program 转成具体的 100 章剧情块和连续未来十章。生成和审查完成后停止，不修改 Prompt。

## 开始仓库快照

- branch：`principal_dev_new_sys`
- HEAD：`170da2221ca38948dce66fa0a48041cfeeede75b`
- 开始时 Git status：`## principal_dev_new_sys...origin/principal_dev_new_sys`，工作树干净。
- 当前生产 Prompt 基线：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`。
- `e2e3bac` 是当前 HEAD 的祖先；祖先链包含 `32eba11`、`c99f2d6`、`170da22`。
- 当前 `src/story_mvp/prompts.py` blob SHA-1：`43026d3fd7922eb8f1d4b52b1a570a690557c8c5`。

## Frozen Creative Baseline

本任务开始时正式冻结以下 Creative Chain：

- `FANTASY_SEED_TEMPLATE`
- `COMPOUNDING_GROWTH_DIRECTION`
- `WORLD_VISION_TEMPLATE`
- `STORY_PROGRAM_TEMPLATE`

来源均为 `src/story_mvp/prompts.py`，最后生产修改提交为 `e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`。除非以后出现新的、真实的、跨作品重复失败，本轮及后续不因理论猜测或单候选局部问题修改它们。

本轮同样禁止修改 GBrain、Growth Genome、Canon、State Delta、Chapter Prompt、Director、Chapter Prep、Writer、Review Prompt 和其它生产模块。本轮只测试正式 `OUTLINE_TEMPLATE`。

## 候选范围

只使用上一轮已冻结的两个候选：

- Candidate A：`《偷走明天的人》`，Personal / Future Asset；上一轮 Compounding 存活，Narrative 局部偏薄。
- Candidate B：`《掌中天工》`，Production Asset；上一轮 Compounding 和 Narrative 均存活。

不重新生成 Seed、World Vision 或 Story Program，不读取 Candidate C，不改变任何三层冻结创意产物。

## 输入隔离

`INPUT.md` 逐字沿用上一轮真实作者方向，不加入 Eventization、Narrative Momentum、人格诊断、社会反馈诊断、A 的薄点、B 的优点、GBrain、历史 reviewer 或本实验目标。

每个 Outline Agent 只能读取：`INPUT.md`、自己的 `fantasy_seed.md`、自己的 `world_vision.md`、自己的 `story_program.md` 和当前正式 `OUTLINE_TEMPLATE`。不得读取另一候选、reviewer、实验说明、GBrain、Reference Programs、历史实验、其它 BOOK、Chapter、Canon 或其它生产文件。

每个候选只生成一次；不自动重生成。Outline response 生成后立即冻结，reviewer 只读取冻结版本。

## 完整输出边界

Outline response 必须完整包含以下四个一级标题：

1. `# 小说总体设计画像`
2. `# 未来100章大型剧情块`
3. `# 未来十章逐章小纲`
4. `# 当前状态、未兑现承诺与作者备注`

不得停在总体设计画像，不手工补未来十章，不提前加入人物指纹、宿敌、名场面、社会反馈或事件化指导。

## 审查问题

Reviewer 只根据实际 Outline 检查：100 章剧情块是否事件化、旧资产是否进入具体事件、阶段净新增是否可见、社会反馈和关键关系是否进入情节、10/30/100 是否成为可复述事件、未来十章是否有逐章行动与直接因果、人物与资产是否耦合，以及 A/B 的专项回归标签。

## 完成后判定

跨候选审查使用：`OUTLINE_COMPOUNDING_SURVIVES` / `OUTLINE_COMPOUNDING_PARTIAL` / `OUTLINE_COMPOUNDING_COLLAPSES`；`OUTLINE_NARRATIVE_HEALTHY` / `OUTLINE_NARRATIVE_THIN` / `OUTLINE_NARRATIVE_COLLAPSES`；`EVENTIZATION_HEALTHY` / `EVENTIZATION_MIXED` / `DESIGN_DOC_REGRESSION`。

无论 Outline 结果如何，只要本轮没有发现 Seed / World Vision / Story Program 的共同回归问题，最终记录 `CREATIVE_CHAIN_FROZEN`。本轮不新增角色系统，不修改 Prompt。

## 执行结果

- A/B 冻结 Creative Chain：三层输入均逐字复制并通过 hash 校验。
- A/B Outline Agent：各真实生成 1 次；两个 response 均完整输出四个正式一级标题。
- Outline Reviewer：A/B 各 1 个独立 Reviewer；Cross-Candidate Reviewer：1 个独立 Reviewer。
- A：`OUTLINE_COMPOUNDING_SURVIVES` + `OUTLINE_NARRATIVE_THIN` + `EVENTIZATION_MIXED`。
- B：`OUTLINE_COMPOUNDING_SURVIVES` + `OUTLINE_NARRATIVE_HEALTHY` + `EVENTIZATION_HEALTHY`。
- 总体：`OUTLINE_COMPOUNDING_SURVIVES` + `OUTLINE_NARRATIVE_THIN` + `EVENTIZATION_MIXED`。
- Outline 修改档位：`SMALL_EVENTIZATION_FIX_NEEDED`；仅提出三条建议，不执行。
- Creative Chain：`CREATIVE_CHAIN_FROZEN`。
- 本轮未修改生产 Prompt 或生产代码；提交前生产源码/测试无 diff。
