---
name: bootstrap-original-novel
description: 为 creation_mode=ORIGINAL 且无来源正文的新小说，依次生成 Core Innovation、Story Foundation 与选定 Foundation 的 Development Proposal；只写 Proposal artifact，不创建章节或 Canon。
---

# Bootstrap Original Novel

此 Skill 只处理 `ORIGINAL_BOOK_BOOTSTRAP` 本地文件 handoff。它负责三个明确阶段：

1. `CORE_INNOVATION_PROPOSAL`：在作者已经确认的 Reader Experience / Narrative Drive 边界内，生成恰好三个开放语义的高杠杆核心创意。
2. `STORY_FOUNDATION_PROPOSAL`：读取作者已经选择并冻结的 Core Innovation，在同一创意引擎下生成三个故事基础承载方案。
3. `FOUNDATION_DEVELOPMENT_PROPOSAL`：只针对作者已经选择的一个 Story Foundation，生成长期成长、扩张、兑现、第一阶段、画像、路线与三个首章候选。

它不替作者选择、不批准、不生成首章正文，也不把 Proposal 写入 Canon。

## 输入

Prerequisite：`novel workflow start` 已成功返回 `status=RUNNING`，且 `executor_skill=bootstrap-original-novel`。本 Skill 不承担协议领取，不重算冻结 hash，也不复核状态协议。

读取 `task.json`，只读取其中 `business_input_files` 列出的 `original_request.json` 与 `proposal_schema.json`。Python 的 workflow complete 会负责通用 `output_schema.json`、artifact、漂移和状态校验。

`premise` 是唯一必填作者输入。类型、文风、视角、篇幅、must include、forbidden 与抽象 reference traits 都是约束；reference traits 不得被复制为来源小说的人物、设定或情节。

`original_request.json.progression_kernel` 中的 Reader Experience、Primary Narrative Drive、Secondary Drive mix 与作者 hard constraints 是冻结边界。必须原样带回 `kernel_contracts`，不得用题材或关键词替换它们。

在 Foundation 与 Development 阶段，`progression_kernel.core_innovation` 是唯一允许使用的 Core Innovation Intent。Development 阶段还必须原样使用 `selected_story_foundation`。它们是作者意图，不是 Canon；不得自行改写、替换或合并。

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
- 恰好三个有意义的 Story Foundation；每个都要包含作者可读的具体 pitch、主角能力与弱点、欲望、开局、世界承载、第一阶段目标、典型选择、风险、社会与资源结构，以及它如何发挥已选 Core Innovation。
- Foundation Diversity 只比较同一创意引擎下的不同故事承载方式：主角身份与能力、开局处境、世界入口、地理空间、第一阶段目标、关系、风险和资源组合可以不同。
- 不得要求三个 Foundation 使用不同 Narrative Engine；不得改变 Reader Promise、Primary Narrative Drive、Core Innovation 或 premise hard constraints。
- 此阶段不得生成 progression / expansion / payoff grammar、路线、画像、First Phase 或首章候选。

## FOUNDATION_DEVELOPMENT_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/foundation_development/proposal.json`：

- `information_status` 必须为 `PROPOSAL`；`kernel_contracts`、`core_innovation_intent` 与 `selected_foundation_id` 必须与冻结输入一致。
- 只发展 `selected_story_foundation.selected_candidate`，不得换主角承载、Foundation、Primary Narrative Drive 或 Core Innovation。
- 生成 protagonist refinement、world rules / social configuration、Progression Grammar、Expansion Grammar、Payoff Grammar、Growth & Long-Term、First Phase、Rolling Planning、Book Profile Draft、开放路线和恰好三个首章候选。
- `first_phase.selected_foundation_id` 必须等于冻结选择，并回答 opening pressure、具体目标、资源瓶颈、成长机会、第一次兑现、第一次有意义升级、阶段高潮和高潮后变化。
- 长期语法回答“为什么可以持续成长、扩大问题空间、分阶段兑现”，不得固定第 N 章、卷数、地图频率、层数或结局。
- 首章候选只描述主动选择、代价、不可逆改变、后续空间和风险；不生成正文，不运行评分引擎。

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
- Development stage：`requested_stage=FOUNDATION_DEVELOPMENT_PROPOSAL`、`completed_stage=FOUNDATION_DEVELOPED`、`artifact_paths` 包含 `artifacts/foundation_development/proposal.json`。
- 三个阶段都必须 `canon_committed=false`、`edition_activated=false`，并明确下一步是作者审阅/选择/确认。

最后按 Local File Handoff 协议写状态和事件并进入 `COMPLETED`；需要作者决定时进入 `WAITING_FOR_USER`。
