# PREMISE APERTURE FREEZE SMOKE

## Verdict

PASS。

它已经成为正确的可选 production opening stage，不是只在文档中冻结。实现、状态机、作者门禁、lane contract、runtime cutoff 与 workflow authority 均一致。

UI 专项测试实际通过；`test_premise_production.py` 因当前沙箱无可写临时目录未能执行，不属于项目失败。

## Current Default Verified

Production 当前是：

- 可选 Premise Forge：一次生成 S1/S2/S3，Non-Canon。
- 独立 Compiler：只审可满足性，不评分、不选择、不修稿。
- 作者选择、编辑、批准或显式跳过。
- 批准后确定性生成 World / Power / Human / Story 四条 lane contract。
- 原 Split Authority 链继续负责 World → Character → Story → Outline → Chapter。

证据：[PROJECT_RULES.md:46-55](C:/dev/tgn-story-mvp-premise-freeze/PROJECT_RULES.md:46)、[PREMISE_APERTURE.md:9-20](C:/dev/tgn-story-mvp-premise-freeze/docs/PREMISE_APERTURE.md:9)。

仍为 research-only 的是四 Agent 正交碰撞、Two-Bet、自动 selector、自动 Repair、旧统一 Fantasy Seed。[PREMISE_APERTURE.md:84-90](C:/dev/tgn-story-mvp-premise-freeze/docs/PREMISE_APERTURE.md:84)

## State Machine Trace

| 状态 | 当前行为 |
|---|---|
| `not_started` | 不存在 Premise 文件；`ready_for_authority=True`，旧链可直接使用。 |
| `skipped` | 只保留作者 skip 标记，清除候选、选择、Compiler 与 contract；旧链恢复可用。 |
| started-unapproved | `candidates_ready`、`selected`、`compiled`、`compiler_blocked` 均设置 `started_unapproved=True`，阻止下游 Authority。 |
| strict PASS | 只有 selected verdict 为严格 `PASS` 且 Compiler snapshot 与当前选卡完全一致时，`can_approve=True`。 |
| edited-after-compiler | 当前选卡与 snapshot 不一致，批准被拒绝，要求重新独立编译。 |
| approved | 写入四条 lane contract 与 `PREMISE_CONTRACT.md`，状态为 `approved`。 |
| World-approved | 所有 Premise 修改、skip、Forge/Compiler prompt 生成均被冻结。 |

核心实现：[premise_workflow.py:175-259](C:/dev/tgn-story-mvp-premise-freeze/src/story_mvp/premise_workflow.py:175)、[premise_workflow.py:292-367](C:/dev/tgn-story-mvp-premise-freeze/src/story_mvp/premise_workflow.py:292)。

## Authority Visibility Trace

- World：只接收 World-only 与 protagonist-blind public Interface。
- Power：接收 Ontology、Scale、trigger、coverage、action、carrier、boundary。
- Human：接收 Ontology、T0、Scale；看不到特殊 Power 与 Story。
- Story Program：首次读取完整 Story contract。
- Outline：显式传入空 Premise contract。
- Chapter Runtime：不接收 raw Premise Card。

证据：[character_prompts.py:496-568](C:/dev/tgn-story-mvp-premise-freeze/src/story_mvp/character_prompts.py:496)、[character_prompts.py:615-677](C:/dev/tgn-story-mvp-premise-freeze/src/story_mvp/character_prompts.py:615)、[test_premise_production.py:355-433](C:/dev/tgn-story-mvp-premise-freeze/tests/test_premise_production.py:355)。

## Workflow / UI Trace

`premise.contract` 是唯一注册的正式 Premise artifact；候选、选卡、Compiler Input/Report 不进入 Workflow artifact 图。

Premise contract 变化会使 World、Power、Human、Character、Story、Plan 及未来 Run stale，并记录为 `premise.contract` 变更。[workflow_state.py:22-48](C:/dev/tgn-story-mvp-premise-freeze/src/story_mvp/workflow_state.py:22)、[workflow_state.py:539-553](C:/dev/tgn-story-mvp-premise-freeze/src/story_mvp/workflow_state.py:539)

UI 有作者选择、批准、跳过；没有自动 selector，也没有 repair loop。指定 Premise UI 测试实际通过：`1 passed`。[test_author_workspace_ui.py:84-106](C:/dev/tgn-story-mvp-premise-freeze/tests/test_author_workspace_ui.py:84)

## Findings

无会改变冻结结论的真实缺陷。当前实现不是“只文档冻结”，而是代码层面的 optional、author-gated、snapshot-bound production stage。

## Residual Risks

无新增的 freeze-blocking 产品风险。当前唯一限制是本次环境无法执行使用 `tmp_path` 的 Premise production 测试；这属于沙箱临时目录权限限制，不是代码行为缺陷。
