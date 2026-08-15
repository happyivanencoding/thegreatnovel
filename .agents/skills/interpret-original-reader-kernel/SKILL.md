---
name: interpret-original-reader-kernel
description: 对无来源正文的 ORIGINAL 小说执行一次 Semantic First Read，从冻结的作者原始请求提出完整 Reader Experience、Narrative Drive、Progression Engine、Creative Semantics 与市场语义 Proposal；只用于 ORIGINAL_READER_INTERPRETATION handoff，不生成 Core Innovation、Foundation、长期语法或章节。
---

# Interpret Original Reader Kernel

只处理 `ORIGINAL_READER_INTERPRETATION` 本地文件 handoff。真正阅读作者 seed，而不是按关键词分类或返回 generic defaults。

## 输入

Prerequisite：`novel workflow start` 已成功返回 `status=RUNNING`，且 `executor_skill=interpret-original-reader-kernel`。

读取 `task.json` 的冻结合同；业务内容只读取 `business_input_files` 中唯一的 `original_request.json`。综合理解：

- premise
- genre metadata
- tone_style 与 pov
- expected_length
- must_include 与 forbidden
- reference_traits（只取抽象特征，不模仿命名作品）

`original_request.json.generation_mode` 决定本次任务：

- `INITIAL`：首次 Semantic First Read，只依据 Seed 推断完整 Proposal。
- `REGENERATION`：同一项目的作者修正后重新提案。除原 Seed 外，还必须读取
  `current_ai_proposal`、`author_overrides` 与 `author_instruction`。

重新生成时，语义优先级依次为：显式 `author_overrides`、其中已经冻结的作者控制项、
Seed 的明确约束、AI 对其余字段的重新推断。`current_ai_proposal` 只是帮助理解作者改了
什么的上下文，不是高于 Seed 或 Author Overrides 的权威。只对 override 中实际出现的
字段保持原值；未出现的字段必须允许根据 Seed 与新上下文重新判断。`author_instruction`
只约束本轮重新生成，不得写回或改写 premise/Seed。

使用 `task.json.original_reader_interpretation.contract_ids` 的三个 ID，不自行发明基础设施 ID；
输出 `schema_version`、字段结构与 enum 值必须严格遵循
`task.json.original_reader_interpretation.proposal_schema`；不得自行选择、升级、降级或兼容 schema version，
也不得额外打开源码或业务文件。如果 frozen proposal schema 与本 Skill
要求的 Creative Semantics 出现矛盾，立即停止并报告 blocker，不得把缺失字段塞进
`summary`、删改字段或猜测兼容方案。

## 语义任务

分别回答：

1. Reader Experience：读者为什么会持续追读？为现有全部 20 个 `ReaderExperience` 维度给出有区分度的 Proposal 强度。
2. Narrative Drive：什么机制会反复推动故事进入新状态？提出一个 Primary Drive 与最多四个 Secondary Drives。
3. Progression Engine：是否需要持续扩大主体行动可能性的成长结构？该布尔判断独立于 Primary Drive。
4. Market metadata：描述作品面向作者的市场语义，不把题材标签当作 Drive 路由。
5. Creative Semantics：用开放文本说明作者已经定义的核心幻想与生成机制、仍然开放的设计空间、兑现质感、新奇度焦点、现实锚点、复杂度边界、可重复阅读循环与防漂移边界。

`creative_semantics` 必须逐项回答：

- `signature_fantasy`：读者真正购买的核心幻想。
- `existing_signature_mechanism`：Seed 是否已经明确给出能反复生成选择、成长、兑现和新问题的核心机制；有则准确描述，没有或不足则留空或明确写尚未确定。
- `open_design_space`：作者尚未决定、后续核心玩法真正可以创新的问题。
- `payoff_texture`：读者获得兑现时应有的具体感觉。
- `novelty_focus`：主要新奇感应该集中在哪里。
- `realism_anchors`：哪些部分应保持直观、可信或相对简单；如果世界本身就是主要幻想来源，也应如实说明。
- `complexity_boundaries`：哪些额外独立机制虽然逻辑成立，却会抢走核心体验。
- `repeatable_reader_loop`：最简单、可重复且可变化的追读循环；它不是章节模板。
- `anti_drift`：哪些合理结果已经不是作者要写的这本书。

这些字段只允许自然语言 string / list[string]，不得创建 taxonomy、enum、数值分数、创新预算、类型到机制映射、关键词路由或预设故事模板。`semantic_evidence` 必须引用 premise，并只引用作者实际提供的非空 genre、tone_style、expected_length、must_include、forbidden、reference_traits 以及 Reader Experience / Narrative Drive 中真实存在的语义关系；未提供的字段只能记录为未知，不得补写证据。genre 为空仍需分析 premise；不得以“信息不足”返回全部 MEDIUM/NORMAL。若 `CUSTOM` 是最合适的 Drive，必须给出真实语义理由。

语义层级必须保持清楚：`exceptional advantage` / `signature_fantasy` / `existing_signature_mechanism` 描述读者购买的正向特殊优势，`realism_anchors` 描述作者明确要求保持可信的局部摩擦、边界、代价与后果；二者不是同一条强弱轴。`realism_anchors` 不能把核心幻想平均化或替代，也不能把它过度现实化为普通人可复制的能力；`signature_fantasy` 也不能因为资源、运营或社会反应的现实摩擦而被削弱。两者必须同时保留：scope realism 只约束明确列出的局部范围，core fantasy salience 则保护异常优势、正向兑现与新增行动可能性。若 Seed 明确给出只有主角拥有、普通人无法复制、且会持续扩大行动可能性的规则，不能把它改写为职业技能、工程知识、管理能力或一般效率提升。特殊能力本身可以突破现实基线，除非 Seed 或作者明确要求能力也遵守现实物理上限。

`existing_signature_mechanism` 必须分别说明：特殊规则是什么、谁能使用、普通人为什么不能复制、它如何反复创造新的可行动可能性，以及哪些资源或社会代价只是能力的约束。不得把代价写成能力的替代物。若能力的超现实尺度没有被作者决定，必须把“是否允许沿原功能产生突破现实上限的质变”保留在 `open_design_space`、`uncertainties` 或 `author_attention_points` 中，不得把模型的保守假设伪装成 `realism_anchors`。

当 `signature_fantasy` 明确包含异常能力或特殊权限时，`anti_drift` 应包含反事实替代检查：如果拿掉该特殊机制，故事的主要活动、能力兑现和爽点不能基本保持不变；否则说明特殊幻想已经被普通职业能力稀释。

本 Skill 的 Creative Semantics 只冻结作者意图、读者体验和语义边界；不调用、不扩展 Taste/文学评分模块，不产生审美排名、文学分数或新的评分门槛，也不把 scope realism 或 core fantasy salience 变成评分指标。

Creative Semantics 只识别体验、既有机制、开放空间、创新焦点、边界与重复循环。即使 Seed 很具体，也不得在本阶段借机生成 Core 候选、主角职业、世界具体异常规则、敌人、地图、势力、能力清单、升级树、第一阶段、长期剧情或首章。

## 输出

写 `artifacts/reader_kernel/proposal.json`，字段为：

- `schema_version`：严格使用 frozen `proposal_schema` 要求的值
- `information_status=PROPOSAL`
- `summary`
- `reader_experience`：复用 `ReaderExperienceContract`
- `market_category`：复用 `MarketCategoryMetadata`
- `narrative_drive`：复用 `NarrativeDriveContract`
- `creative_semantics`：开放文本 `OriginalCreativeSemantics`
- `semantic_evidence`
- `uncertainties`
- `author_attention_points`

三个结构的 `status` 必须为 `NEEDS_REVIEW`。Reader priorities 必须恰好覆盖全部现有 ReaderExperience。不得写 `EFFECTIVE`，不得写 Canon。

`REGENERATION` 仍须输出完整、自洽的 `OriginalReaderKernelProposal`，包括 summary、
semantic evidence、uncertainties 与 author attention points；不得只改结构化标签而保留
与旧值冲突的解释。Author Overrides 是当前创作决策，不是供模型讨论或反驳的建议。

## 禁止越级

不得生成或决定：

- Core Innovation、外挂、升级树或完整资源经济
- Story Foundation、主角承载方案或第一阶段
- 长期世界阶段、固定剧情、首章候选或正文
- premise/genre 关键词路由、固定 creative taxonomy 或 named novel imitation

本任务只提出“读者期待、长期推进方式、是否需要成长引擎、作者已定义什么、哪里仍可创新以及如何防止漂移”。

无论 `INITIAL` 还是 `REGENERATION`，都不得创建 Core Innovation、Story Foundation、
剧情、章节或正文，也不得确认 Proposal 或推进到 Reader Kernel Review 之后的阶段。

## 完成

写业务 `result.json`：`completed_stage=READER_KERNEL_PROPOSED`，`artifact_paths` 包含 `artifacts/reader_kernel/proposal.json`；`validation_summary`、`warnings`、`next_action` 可按实际业务结果提供。随后使用复制指令给出的绝对 `library_root` 和 workflow start 返回的同一个 `claim_token` 运行 `novel workflow complete`。

不要手写 `handoff_id`、`handoff_type`、`book_id`、`edition_id`、`requested_stage`、`status`、`base_event_seq`、`base_projection_hash`、`canon_committed` 或 `edition_activated`；这些 deterministic envelope 字段由 Python complete 注入并验证。
