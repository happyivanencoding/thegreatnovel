# Outline Eventization Fix v1 + Paired Blind Validation

## 实验性质

本目录验证一次已经提交的 Outline 层最小事件化修正。Creative Chain 已冻结；本轮不修改 Fantasy Seed、Compounding、World Vision、Story Program 或其它生产层。Control 是上一轮真实冻结 Outline，Treatment 只改变正式 `OUTLINE_TEMPLATE`。

## 生产修改边界

- Frozen Creative Prompt baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`。
- Outline-only fix commit：`2be35340b36aa05588c85324ffd5e2e1bfa6d951`。
- 只修改 `OUTLINE_TEMPLATE` 四处：具体发生说明、收益与反哺说明、长期关系连续性说明、10/30/100 事件化说明。
- 未修改 `FANTASY_SEED_TEMPLATE`、`COMPOUNDING_GROWTH_DIRECTION`、`WORLD_VISION_TEMPLATE`、`STORY_PROGRAM_TEMPLATE`、GBrain、Growth Genome、Review Prompt、Director、Chapter Prep、Writer、Canon、State Delta 或其它生产模块。

## 输入与 Control

只使用上一轮 Candidate A/B 的冻结 Creative Chain：

- Candidate A：`《偷走明天的人》`。
- Candidate B：`《掌中天工》`。

每个候选的 INPUT、Fantasy Seed、World Vision、Story Program 和 Control Outline 均从 `books/real-exp-outline-eventization-v1/` 逐字复制并通过 SHA-256 校验；不重新生成 Creative Chain 或 Control。

## Treatment 边界

Treatment 使用相同的 INPUT、Fantasy Seed、World Vision、Story Program、模型/Agent 类型和输出边界，只使用当前修改后的正式 `OUTLINE_TEMPLATE`。上一轮未单独记录 temperature/sampling 参数，本轮不猜测；使用相同 `luna_worker` Agent 类型，具体记录见冻结快照。

每个候选只生成一次 Treatment。完整 rendered prompt 必须先保存到 `treatment_outline_prompt.md`，再与当前 `generate_prompt(mode="outline", ...)` 逐字校验；校验成功后才启动 Treatment Agent。若 prompt 保存/校验失败，停止该 Candidate，不继续调用模型。

## Blind Pair Review

每个候选独立 Reviewer 读取 Frozen Creative Chain 和两个匿名 Outline X/Y，不读取 Prompt、实验说明、上一轮评价或映射。映射只在 Review 完成后揭示：

- Candidate A：X = Treatment，Y = Control。
- Candidate B：X = Control，Y = Treatment。

Review 比较具体人物行动、对手反制、不可逆事件、资产事件化、关系连续性、社会反馈、10/30/100、未来十章和 A/B 专项；不使用数值评分、权重、排名或平均分。

## 接受边界

Cross-Candidate 最终只能给出：

- Compounding：`COMPOUNDING_PRESERVED` 或 `COMPOUNDING_WEAKENED`。
- A：`A_EVENTIZATION_IMPROVED`、`A_NO_MATERIAL_CHANGE` 或 `A_WORSE`。
- B：`B_HEALTH_PRESERVED`、`B_MINOR_DEGRADATION` 或 `B_DAMAGED`。
- Outline：`OUTLINE_FIX_VALIDATED`、`OUTLINE_FIX_MIXED`、`OUTLINE_FIX_NO_EFFECT` 或 `OUTLINE_FIX_REJECT`。

只有 `OUTLINE_FIX_VALIDATED` 才建议保留新 Outline Prompt 并记录 `OUTLINE_FROZEN`。本轮无论结果如何不自动回退、不自动继续修、不进入正文。

## 执行结果

- A/B Frozen Creative Chain：零修改，复制 hash 全部一致。
- Control：直接复制上一轮冻结 Outline，未重新生成。
- Treatment：A/B 各使用修改后的正式 Outline Prompt 生成一次；rendered prompt 在模型调用前已保存并逐字校验。
- Blind Pair Review：A/B 各一个独立 Reviewer，完成后才揭示 mapping。
- Attribution：A `A_EVENTIZATION_IMPROVED`；B `B_HEALTH_PRESERVED`；`COMPOUNDING_PRESERVED`。
- `LOCAL_FIX_GLOBAL_DAMAGE`：未发现。
- 最终：`OUTLINE_FIX_VALIDATED`。
- 正式冻结：`OUTLINE_FROZEN` + `CREATIVE_CHAIN_FROZEN`。
- 本轮不进入正文，不自动修改任何 Prompt。
