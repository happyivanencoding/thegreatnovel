---
name: bootstrap-original-novel
description: 为 creation_mode=ORIGINAL 且无来源正文的新小说，按冻结的 Reader Experience 与 Core Innovation 生成可审计的原创 Genesis Proposal；只写 Proposal artifact，不创建章节或 Canon。
---

# Bootstrap Original Novel

此 Skill 只处理 `ORIGINAL_BOOK_BOOTSTRAP` 本地文件 handoff。它负责两个明确阶段：

1. `CORE_INNOVATION_PROPOSAL`：在作者已经确认的 Reader Experience / Narrative Drive 边界内，生成恰好三个开放语义的高杠杆核心创意。
2. `STORY_FOUNDATION_PROPOSAL`：读取作者已经选择并冻结的 Core Innovation，在同一创意引擎下生成三个故事基础承载方案。

它不替作者选择、不批准、不生成首章正文，也不把 Proposal 写入 Canon。

## 输入

Prerequisite：`novel workflow start` 已成功返回 `status=RUNNING`，且 `executor_skill=bootstrap-original-novel`。本 Skill 不承担协议领取，不重算冻结 hash，也不复核状态协议。

读取 `task.json`，只读取其中 `business_input_files` 列出的 `original_request.json` 与 `proposal_schema.json`。Python 的 workflow complete 会负责通用 `output_schema.json`、artifact、漂移和状态校验。

`premise` 是唯一必填作者输入。类型、文风、视角、篇幅、must include、forbidden 与抽象 reference traits 都是约束；reference traits 不得被复制为来源小说的人物、设定或情节。

`original_request.json.progression_kernel` 中的 Reader Experience、Primary Narrative Drive、Secondary Drive mix、Genre / World / Payoff Proposal 与作者 hard constraints 是冻结边界。必须原样带回 `kernel_contracts`，不得用题材或关键词替换它们。

在 `STORY_FOUNDATION_PROPOSAL` 阶段，`progression_kernel.core_innovation` 是唯一允许使用的 Core Innovation Intent。它是作者意图，不是 Canon；不得自行改写、替换或合并为另一个机制。

## CORE_INNOVATION_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/core_innovation/proposal.json`：

- `information_status` 必须为 `PROPOSAL`。
- `kernel_contracts` 必须原样复制冻结的 `progression_kernel`。
- `innovation_candidates` 必须恰好三个，且 `innovation_id` 不重复。
- 三个候选必须共享 Core Reader Promise、Primary Narrative Drive、作者 premise hard constraints、must_include 与 forbidden。
- 三个候选必须在机制杠杆、选择结构、成长生成、兑现方式或长期扩张语法上有实质差异；不能只是换人物、地点、反派、开场事故或表面设定。
- 每个候选必须具体回答 schema 中的 `core_mechanism`、`protagonist_special_rule`、`choice_generation`、`progression_generation`、`payoff_generation`、`limitation`、`expansion_grammar`、`long_form_capacity`、`novelty_source`、`repetition_risk` 与 `fit_with_reader_promise`。
- Core Innovation 是开放语义空间。不得创建或使用固定 Innovation Type、Family、Registry、Template、Archetype、关键词路由、Genre 映射或固定 Expansion stage 列表；本任务中的任何文学例子都不是产品答案。
- 只写该 Proposal artifact，不生成 Story Foundation、主角、世界、路线、第一阶段或章节。

## STORY_FOUNDATION_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/story_foundation/proposal.json`：

- `information_status` 必须为 `PROPOSAL`。
- `kernel_contracts` 必须原样复制冻结的 `progression_kernel`，并且 `core_innovation_intent` 必须与 `progression_kernel.core_innovation` 的作者选择完全一致。
- 恰好三个有意义的 Story Foundation；每个都要包含作者可读的具体 pitch、主角、欲望、风险、开局画面、典型选择、主冲突、世界承载机制、成长循环以及它如何发挥已选 Core Innovation。
- Foundation Diversity 只比较同一创意引擎下的不同故事承载方式：主角身份与能力、开局处境、世界入口、地理空间、第一阶段目标、关系、风险和资源组合可以不同。
- 不得要求三个 Foundation 使用不同 Narrative Engine / Story Engine / Growth Engine；不得改变 Reader Promise、Primary Narrative Drive、确认的成长语法或 premise hard constraints。
- 必须提供开放语义的 `progression_grammar`、`expansion_grammar` 与 `payoff_grammar`。它们描述系统如何继续生成行动空间、问题空间与兑现，不是固定剧情、固定层数或固定章节节奏。
- `first_phase` 只描述第一卷或第一阶段的可写运行方式：开场压力、具体目标、资源瓶颈、成长机会、第一次兑现、第一次有意义的升级、阶段高潮和高潮后变化。短篇可以更快闭环；长篇只需说明生成能力，不得伪造精确容量分数、固定结局或逐章 FAR 大纲。
- 九维 `book_profile_draft`、路线、开放问题、幕后候选和三个首章候选都必须保持 Proposal 语义；未知保持开放，不猜成事实，不填写占位评分。
- 首章候选只描述主动选择、代价、不可逆改变、后续空间和风险；本任务不运行评分引擎。

## 共同硬边界

- `book/` 永久只读。
- 不建立 Source Manifest、假章节、Chapter 0、Canon Event、Canon Commit、Edition、Author Truth、Book Profile 或 Planning Aggregate。
- 不替作者确认 Core Innovation、Foundation、路线、真相或首章。
- 不把 `INFERENCE`、`CANDIDATE`、`PROSE_ONLY` 或 `SOFT_REFERENCE` 静默升级为 Canon。
- 不创建固定 Narrative Engine taxonomy、创新评分、长篇能力评分或第二套节奏系统。

## 完成

按 `task.json` 冻结的阶段合同写 `result.json`，然后运行 `novel workflow complete`：

- Core stage：`requested_stage=CORE_INNOVATION_PROPOSAL`、`completed_stage=CORE_INNOVATION_PROPOSED`、`innovation_ids` 与三个候选顺序一致、`artifact_paths` 包含 `artifacts/core_innovation/proposal.json`。
- Foundation stage：`requested_stage=STORY_FOUNDATION_PROPOSAL`、`completed_stage=FOUNDATION_PROPOSED`、`candidate_ids` 与三个 Foundation 顺序一致、`artifact_paths` 包含 `artifacts/story_foundation/proposal.json`。
- 两个阶段都必须 `canon_committed=false`、`edition_activated=false`，并明确下一步是作者审阅/选择/确认。

最后按 Local File Handoff 协议写状态和事件并进入 `COMPLETED`；需要作者决定时进入 `WAITING_FOR_USER`。
