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
- 如果冻结的 `signature_fantasy` 是主角独占且普通人无法复制的特殊规则，三个候选必须保留它的正向异常性、主角与普通人的能力不对称、可见的能力验证和质变行动空间。`protagonist_special_rule` 不能只有“每天一次、不能全知、不能自动战斗”等负面限制，还必须说明主角因此能做到什么普通人做不到的事情；`limitation` 只能描述代价与摩擦，不能把能力中和成普通效率提升。
- 当 `existing_signature_mechanism` 为空或语义上不足以独立产生长期内容时，三个候选仍可真正提出不同的高杠杆生成机制。这个判断由 LLM 阅读完整 Seed 与 Creative Semantics 后作出，不得由 Python 分类、关键词或题材路由完成。
- 三个候选必须在 unresolved design choices 上有实质差异；不能只是换人物、地点、反派、开场事故或表面设定，也不能为了制造差异强造第二套系统。
- 每个候选必须具体回答 schema 中的 `core_mechanism`、`protagonist_special_rule`、`choice_generation`、`progression_generation`、`payoff_generation`、`limitation`、`expansion_grammar`、`long_form_capacity`、`novelty_source`、`repetition_risk` 与 `fit_with_reader_promise`。
- 每个候选还必须给出 `plain_language_pitch`、`concrete_example`、`reader_anticipation` 与 `unresolved_design_choices`。前两者用作者第一次看就能理解的动作、场景和结果解释怎么玩；`concrete_example` 必须明确只是 NON_CANON illustrative example，不是 Foundation、Canon 或必然发生的未来事件；`reader_anticipation` 直接回答读者为什么期待下一次；`unresolved_design_choices` 只列本候选实际解决的开放设计问题，不重复既有 Signature Mechanism。author-facing 字段避免无必要的系统术语和抽象名词。
- 每个候选必须说明如何增强已确认的 `repeatable_reader_loop`，不得用新循环替换它。
- 每个候选必须通过 Fantasy Salience 自检：删除特殊机制后，候选的主要活动、能力兑现和读者期待是否会发生根本改变；如果不会，或候选把特殊能力降成普通职业技能的放大器，必须重写。现实资源、维护、人员和物流可以制造摩擦，但不能成为特殊能力的替代卖点。
- Core Innovation 是开放语义空间。不得创建或使用固定 Innovation Type、Family、Registry、Template、Archetype、关键词路由、Genre 映射或固定 Expansion stage 列表；本任务中的任何文学例子都不是产品答案。
- 只写该 Proposal artifact，不生成 Story Foundation、主角、世界、路线、第一阶段或章节。

## STORY_FOUNDATION_PROPOSAL 合同

严格按 `proposal_schema.json` 写 `artifacts/story_foundation/proposal.json`：

- `information_status` 必须为 `PROPOSAL`。
- `kernel_contracts` 必须原样复制冻结的 `progression_kernel`，并且 `core_innovation_intent` 必须与 `progression_kernel.core_innovation` 的作者选择完全一致。
- `CORE_INNOVATION_PROPOSAL` 可以在机制层发散；作者选择一个 Core 后，`STORY_FOUNDATION_PROPOSAL` 必须在 selected Core semantic identity 内收敛，只在故事体验和承载层发散。每个 Foundation 都是 `selected Core + story carrier`，不得重新生成未选择的 Core 路线。
- 作者选择后的 `progression_kernel.core_innovation.selected_candidate` 是一个整体 semantic identity，必须同时阅读并理解其中的 `core_mechanism`、`protagonist_special_rule`、`choice_generation`、`progression_generation`、`payoff_generation`、`novelty_source`、`fit_with_reader_promise`、`unresolved_design_choices` 与 `limitation`；不能把这些字段拆开后重新拼成另一个同等级核心玩法。
- 选择 Core 关闭的是不同 Core 之间的 CORE-LEVEL ROUTE DIVERGENCE，不是所有 Core-internal open questions。Foundation 可以把 selected Core 的未决细节具体化为人物、世界、活动、冲突或兑现环境中的答案，但不得改变其 semantic center；如果它重新回答了“这本书真正反复爽在哪里”，且答案不同于 selected Core，必须重写。
- 恰好三个有意义的 Story Foundation；每个都要包含作者可读的具体 pitch、主角能力与弱点、欲望、开局、世界承载、第一阶段目标、典型选择、风险、社会与资源结构，以及它如何发挥已选 Core Innovation。
- Foundation 的职责是让已确认的核心生成机制变得具体、可写且富有叙事空间：谁来承载、反复做什么、资源与机会如何获得、危险如何施压、机制在哪些场景兑现、人际关系如何进入、规模如何自然扩大。它不负责再创造一个同等级核心卖点。
- Foundation Diversity 首先要求三个候选共享同一 selected Core semantic identity，同时形成实质不同的故事体验；repeated story activity、pressure structure、resource loop、social configuration、spatial/world carrier、mechanism payoff environment 与 expansion direction 只是可选承载维度，不得成为唯一差异来源。开放语义差异应同时考虑主角私人欲望、特殊能力最令人期待的表达方式、主要冲突带来的情绪、普通人与主角的反差、世界的奇异感与谜团压力、能力展示、势力冲突、探索或身份变化；这些不是 taxonomy、preset、genre route 或固定候选类型。主角职业可以不同，但换职业本身不构成有效差异，除非 Seed 明确把职业能力作为主要幻想。
- Foundation 必须实际消费冻结的 Reader Experience 字段 primary_family、setting_skin、mysticism_level、explanation_style，以及 contract_proposals.MARKET_CATEGORY、contract_proposals.NARRATIVE_DRIVE 与 Creative Semantics 的 signature_fantasy、existing_signature_mechanism、repeatable_reader_loop、novelty_focus。这些是故事体验 authority，不是只供 UI 展示的标签；它们必须在 world_carrier、risk_structure、opening_situation 与故事可持续扩展空间中产生可感知体现。不得使用题材标签路由；世界异常只能服务于已确认的世界压力、谜团和想象空间，不得成为主角的竞争性第二核心或第二成长系统。
- Foundation 不只是 Story Carrier，也必须是 READER-PROMISE PAYOFF ENVIRONMENT：完整读取 confirmed Reader Experience、Creative Semantics 与 selected Core，判断本书高优先级阅读体验需要什么样的可重复兑现，再选择能让这些体验自然、高频、可升级地发生的世界状态、压力结构、机会结构、关系和冲突。这里是开放语义判断，不新增字段、enum、taxonomy、preset 或固定爽点公式；不同 Reader Kernel 可以需要能力验证、资源机会、身份变化、谜团揭示、关系兑现或其他不同的 payoff environment。
- protagonist_goal 必须先回答主角本人想要什么，并由私人欲望、关系、性格和处境产生；除非 Seed 明确如此，不得默认写成建立救援网络、维持运营或保障聚落，也不得为了方便使用 Core 而反推一个最合适的职业。职业只能是 supporting competence，不能替代人物欲望或 exceptional advantage。
- Foundation 必须在 author_facing_pitch、opening_situation 或 typical_choice 中给出一眼可见的故事钩子和第一次能力兑现：具体压力、具体普通对象、一次能力选择，以及一个可视化的不可能结果。每个候选都应有自己的核心图像，不能只是“升级设备解决瓶颈”。
- Foundation 必须关注优势如何扩大，而不只是问题如何解决：每轮有意义的兑现后，主角应比之前多出某种能力、资源、权限、位置、选择空间、关系筹码或影响力；现实代价可以制造下一轮更高的欲望和瓶颈，但不能把当前兑现解释到几乎没有作用。
- 兑现节奏应由当前 Reader Kernel 语义决定，并遵循“压力与选择产生有意义兑现，先让兑现产生实际后果，再引出新的代价或更高瓶颈”的方向。限制、燃料、维护、暴露和社会反应是后果与下一轮压力，不应在能力兑现刚发生时把它完全抵消；不得把这一原则硬编码成固定章节数或固定场景公式。
- author_facing_pitch、core_reading_promise、protagonist_goal、opening_situation 与 typical_choice 必须使用小说简介或场景语言；只有 innovation_fit 负责解释 Core、机制、能力兑现和约束。作者向字段不得出现“本候选”“Foundation”“Core Mechanism”“Reader Promise”“特殊机制如何成为主要兑现”等验收式 meta language；不要解释“主角不是普通人”，要直接展示能力造成的场景、反差和后果。
- 每个候选都必须通过能力移除自检：删除特殊能力后，主要活动、第一次兑现和读者期待应发生根本改变；如果删除每日升级后仍然只是一个完整的车队、避难所、工业探索或物流经营故事，就必须重写。现实资源、维护、人员和社会反应是摩擦与后果，不是特殊能力的替代卖点。
- 每个候选完成后必须在内部执行 Core Identity Self-Check：用一句话概括该 Foundation 实际反复兑现的机制，并与 selected Core 的 `core_mechanism`、`choice_generation`、`progression_generation`、`payoff_generation` 与 `novelty_source` 对照；如果 semantic center 已改变，或最大卖点变成 selected Core 未确认的新机制，必须重写。再执行 Core Replacement Test：如果换成另一种同等级 Core，主要故事玩法、成长和兑现几乎不需要改动，说明 Foundation 过于 generic，必须重写。不要把这些 audit reasoning 输出给作者。
- 每个候选都必须检查 `creative_semantics.novelty_focus`、`complexity_boundaries` 与 selected Core Intent；若新增世界规则足以独立成为另一部小说的核心卖点，只有 Seed、Creative Semantics 或 Core 真正需要时才可保留。
- `innovation_fit` 必须明确回答这个 Foundation 如何让已确认 Core Mechanism 和高优先级 Reader Promise 更好玩、如何依赖 selected Core semantic identity、如何允许 Core-internal open questions 具体化，以及如何避免创造竞争性的第二核心机制；这些设计审计说明不要复制到作者向字段。
- 当冻结的 `signature_fantasy` 是特殊规则时，`protagonist`、`protagonist_competence`、`core_reading_promise` 与 `innovation_fit` 必须共同回答：主角为什么明显不是普通人、特殊规则如何反复成为主要故事活动、第一次能力验证在哪里发生、能力如何打开以前不可能的行动，以及普通人和主角的能力反差如何出现。普通职业能力只能是 supporting competence，不能取代 exceptional advantage。
- 不得仅因“避免竞争性第二核心机制”就把主角写成普通后勤执行者、普通维护者或普通组织者；避免第二核心的意思是放大已确认的第一核心，而不是削弱它。现实锚点只约束作者明确要求可信的资源、反应、运输、代价和后果，不自动限制特殊机制的超现实尺度。
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
