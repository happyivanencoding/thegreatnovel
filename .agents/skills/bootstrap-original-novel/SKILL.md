---
name: bootstrap-original-novel
description: 为 creation_mode=ORIGINAL 且无来源正文的新小说，依次生成 Core Innovation、Story Foundation 与选定 Foundation 的 Development Proposal；只写 Proposal artifact，不创建章节或 Canon。
---

# Bootstrap Original Novel

此 Skill 只处理 `ORIGINAL_BOOK_BOOTSTRAP` 本地文件 handoff。它负责三个明确阶段：

1. `CORE_INNOVATION_PROPOSAL`：在作者已经确认的 Reader Experience / Narrative Drive / Creative Semantics 边界内，解决最高杠杆的开放创作问题，生成恰好三个核心玩法候选。
2. `STORY_FOUNDATION_PROPOSAL`：读取作者已经选择并冻结的核心玩法，在同一生成机制下生成三个故事基础承载方案。
3. `FOUNDATION_DEVELOPMENT_PROPOSAL`：只针对作者已经选择的一个 Story Foundation，生成长期成长、扩张、兑现、第一阶段、画像、路线与三个首章候选。

它不替作者选择、不批准、不生成首章正文，也不把 Proposal 写入 Canon。

## 输入

Prerequisite：`novel workflow start` 已成功返回 `status=RUNNING`，且 `executor_skill=bootstrap-original-novel`。本 Skill 不承担协议领取，不重算冻结 hash，也不复核状态协议。

读取 `task.json`，只读取其中 `business_input_files` 列出的 `original_request.json` 与 `proposal_schema.json`。Python 的 workflow complete 会负责通用 `output_schema.json`、artifact、漂移和状态校验。

`premise` 是唯一必填作者输入。类型、文风、视角、篇幅、must include、forbidden 与抽象 reference traits 都是约束；reference traits 不得被复制为来源小说的人物、设定或情节。

`original_request.json.progression_kernel` 中的 Reader Experience、Primary Narrative Drive、Secondary Drive mix、Creative Semantics 与作者 hard constraints 是冻结边界。必须原样带回 `kernel_contracts`，不得用题材或关键词替换它们。`creative_semantics.repeatable_reader_loop` 必须一路增强和具体化，不得被后续阶段悄悄替换。

在 Foundation 与 Development 阶段，`progression_kernel.core_innovation` 是唯一允许使用的 Core Innovation Intent。Development 阶段还必须原样使用 `selected_story_foundation`，并使用 Python 冻结的 `kernel_contract_ids`。它们是作者意图，不是 Canon；不得自行改写、替换或合并。

## CORE_INNOVATION_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/core_innovation/proposal.json`：

- `information_status` 必须为 `PROPOSAL`。
- `kernel_contracts` 必须原样复制冻结的 `progression_kernel`。
- `innovation_candidates` 必须恰好三个，且 `innovation_id` 不重复。
- 三个候选必须共享 Core Reader Promise、Primary Narrative Drive、Creative Semantics、作者 premise hard constraints、must_include 与 forbidden。
- Core 的职责是解决 `creative_semantics.open_design_space` 中最高杠杆的未决问题，不是固定要求再发明一个核心机制。
- 当 `existing_signature_mechanism` 已明确描述足以持续生成故事的机制时，三个候选都必须保留该机制，不得替换、稀释、重新定义或用第二套系统夺取主机制位置；候选差异必须来自未决设计选择，例如选择如何产生、成长如何持续、兑现如何变化、已有能力如何组合、重复如何避免或问题空间如何扩大。
- 当 `existing_signature_mechanism` 为空或语义上不足以独立产生长期内容时，三个候选仍可真正提出不同的高杠杆生成机制。这个判断由 LLM 阅读完整 Seed 与 Creative Semantics 后作出，不得由 Python 分类、关键词或题材路由完成。
- 三个候选必须在 unresolved design choices 上有实质差异；不能只是换人物、地点、反派、开场事故或表面设定，也不能为了制造差异强造第二套系统。
- 每个候选必须具体回答 schema 中的 `core_mechanism`、`protagonist_special_rule`、`choice_generation`、`progression_generation`、`payoff_generation`、`limitation`、`expansion_grammar`、`long_form_capacity`、`novelty_source`、`repetition_risk` 与 `fit_with_reader_promise`。
- 每个候选还必须给出 `plain_language_pitch`、`concrete_example`、`reader_anticipation` 与 `unresolved_design_choices`。前两者用作者第一次看就能理解的动作、场景和结果解释怎么玩；`concrete_example` 必须明确只是 NON_CANON illustrative example，不是 Foundation、Canon 或必然发生的未来事件；`reader_anticipation` 直接回答读者为什么期待下一次；`unresolved_design_choices` 只列本候选实际解决的开放设计问题，不重复既有 Signature Mechanism。author-facing 字段避免无必要的系统术语和抽象名词。
- 每个候选必须说明如何增强已确认的 `repeatable_reader_loop`，不得用新循环替换它。
- Core Innovation 是开放语义空间。不得创建或使用固定 Innovation Type、Family、Registry、Template、Archetype、关键词路由、Genre 映射或固定 Expansion stage 列表；本任务中的任何文学例子都不是产品答案。
- 只写该 Proposal artifact，不生成 Story Foundation、主角、世界、路线、第一阶段或章节。

## STORY_FOUNDATION_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/story_foundation/proposal.json`：

- `information_status` 必须为 `PROPOSAL`。
- `kernel_contracts` 必须原样复制冻结的 `progression_kernel`，并且 `core_innovation_intent` 必须与 `progression_kernel.core_innovation` 的作者选择完全一致。
- 恰好三个有意义的 Story Foundation；每个都要包含作者可读的具体 pitch、主角能力与弱点、欲望、开局、世界承载、第一阶段目标、典型选择、风险、社会与资源结构，以及它如何发挥已选 Core Innovation。
- Foundation 的职责是让已确认的核心生成机制变得具体、可写且富有叙事空间：谁来承载、反复做什么、资源与机会如何获得、危险如何施压、机制在哪些场景兑现、人际关系如何进入、规模如何自然扩大。它不负责再创造一个同等级核心卖点。
- Foundation Diversity 优先来自 repeated story activity、pressure structure、resource loop、social configuration、spatial/world carrier、mechanism payoff environment 与 expansion direction。主角职业可以不同，但换职业本身不构成有效差异，除非 Seed 明确把职业能力作为主要幻想。
- 每个候选都必须检查 `creative_semantics.novelty_focus`、`complexity_boundaries` 与 selected Core Intent；若新增世界规则足以独立成为另一部小说的核心卖点，只有 Seed、Creative Semantics 或 Core 真正需要时才可保留。
- `innovation_fit` 必须明确回答这个 Foundation 如何让已确认 Core Mechanism 更好玩，而没有创造竞争性的第二核心机制。
- Foundation 必须把 `creative_semantics.repeatable_reader_loop` 落成具体、可变化的故事活动。
- 不得要求三个 Foundation 使用不同 Narrative Engine；不得改变 Reader Promise、Primary Narrative Drive、Core Innovation 或 premise hard constraints。
- 不得把“避免竞争性新奇度”误写成“世界必须简单”。如果 Seed、Creative Semantics 与 Core 要求丰富奇幻世界、多文明、多地域、复杂社会或政治，Foundation 可以充分承载；禁止的只是没有语义必要的竞争性第二核心。
- 此阶段不得生成 progression / expansion / payoff grammar、路线、画像、First Phase 或首章候选。

## FOUNDATION_DEVELOPMENT_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/foundation_development/proposal.json`：

- `information_status` 必须为 `PROPOSAL`；`kernel_contracts`、`core_innovation_intent` 与 `selected_foundation_id` 必须与冻结输入一致。
- 只发展 `selected_story_foundation.selected_candidate`，不得换主角承载、Foundation、Primary Narrative Drive 或 Core Innovation。
- 生成 protagonist refinement、world rules / social configuration、Progression Grammar、Expansion Grammar、Payoff Grammar、Growth & Long-Term、First Phase、Rolling Planning、Book Profile Draft、开放路线和恰好三个首章候选。
- 同时生成 `kernel_contract_proposals`，严格复用现有 `GenreContract`、`ProgressionContract`、`WorldExpansionContract`、`PayoffChannelProfile`；全部为 `NEEDS_REVIEW`，ID 必须匹配 `kernel_contract_ids`。若冻结的 `progression_engine_enabled=false`，`progression` 必须为 `null`。
- `first_phase.selected_foundation_id` 必须等于冻结选择，并回答 opening pressure、具体目标、资源瓶颈、成长机会、第一次兑现、第一次实质性局势升级、阶段高潮和高潮后变化。
- Progression Grammar、Expansion Grammar、Payoff Grammar 与 First Phase 必须把已确认的 `repeatable_reader_loop` 转化为可持续语法和具体活动，但不得变成固定章节模板。
- 长期语法回答“为什么可以持续成长、扩大问题空间、分阶段兑现”，并依据 `expected_length`、Reader Promise、Signature Mechanism、Progression Engine、Creative Semantics 与选定 Foundation 调整容量；不得使用固定章数阈值、长篇 preset、固定 arc、卷数、地图频率、层数、结局或完整全书大纲。
- 较短且闭环的作品可以控制扩张和长期承诺，形成有限但完整的阶段兑现；超长成长型作品可以支持多阶段能力、人物、团队、组织、地域、世界、资源、身份、谜团与阶段高潮。两者使用同一开放架构，由语义需求决定，不进入 genre-specific branch。
- 超长篇持续冻结全部 Creative Semantics，以及 Reader Promise、Primary Narrative Drive、Signature Mechanism、Progression / Payoff / Expansion Grammar、关键世界 invariant 与作者 hard constraints；人物、地图、组织、具体阶段目标、冲突、支线和 arc 由 Rolling Planning 逐步展开。
- 首章候选只描述主动选择、代价、不可逆改变、后续空间和风险；不生成正文，不运行评分引擎。

## 共同硬边界

- `book/` 永久只读。
- 不建立 Source Manifest、假章节、Chapter 0、Canon Event、Canon Commit、Edition、Author Truth、Book Profile 或 Planning Aggregate。
- 不替作者确认 Core Innovation、Foundation、路线、真相或首章。
- 不把 `INFERENCE`、`CANDIDATE`、`PROSE_ONLY` 或 `SOFT_REFERENCE` 静默升级为 Canon。
- 不创建固定 Narrative Engine taxonomy、创新评分、复杂度评分、创新预算、长篇能力评分、genre-specific branch、关键词路由、命名作品 preset、固定 arc 模板或第二套节奏系统。

## 完成

按 `task.json` 冻结的阶段合同写 `result.json`，然后运行 `novel workflow complete`：

- Core stage：`requested_stage=CORE_INNOVATION_PROPOSAL`、`completed_stage=CORE_INNOVATION_PROPOSED`、`innovation_ids` 与三个候选顺序一致、`artifact_paths` 包含 `artifacts/core_innovation/proposal.json`。
- Foundation stage：`requested_stage=STORY_FOUNDATION_PROPOSAL`、`completed_stage=FOUNDATION_PROPOSED`、`candidate_ids` 与三个 Foundation 顺序一致、`artifact_paths` 包含 `artifacts/story_foundation/proposal.json`。
- Development stage：`requested_stage=FOUNDATION_DEVELOPMENT_PROPOSAL`、`completed_stage=FOUNDATION_DEVELOPED`、`artifact_paths` 包含 `artifacts/foundation_development/proposal.json`。
- 三个阶段都必须 `canon_committed=false`、`edition_activated=false`，并明确下一步是作者审阅/选择/确认。
- 后续 Final Confirm 必须使用同一份已冻结 Creative Semantics、作者选择的 Core、Foundation 与 Development snapshot；本 Skill 不重新生成它们，也不改变现有显式确认和 Genesis 原子事务。

最后按 Local File Handoff 协议写状态和事件并进入 `COMPLETED`；需要作者决定时进入 `WAITING_FOR_USER`。
