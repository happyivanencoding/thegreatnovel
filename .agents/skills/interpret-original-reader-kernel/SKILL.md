---
name: interpret-original-reader-kernel
description: 对无来源正文的 ORIGINAL 小说执行一次 Semantic First Read，从冻结的作者原始请求提出完整 Reader Experience、Narrative Drive、Progression Engine 与市场语义 Proposal；只用于 ORIGINAL_READER_INTERPRETATION handoff，不生成 Core Innovation、Foundation、长期语法或章节。
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

使用 `task.json.original_reader_interpretation.contract_ids` 的三个 ID，不自行发明基础设施 ID；
输出结构与 enum 值以同一节点的 `proposal_schema` 为准，不额外打开源码或业务文件。

## 语义任务

分别回答：

1. Reader Experience：读者为什么会持续追读？为现有全部 20 个 `ReaderExperience` 维度给出有区分度的 Proposal 强度。
2. Narrative Drive：什么机制会反复推动故事进入新状态？提出一个 Primary Drive 与最多四个 Secondary Drives。
3. Progression Engine：是否需要持续扩大主体行动可能性的成长结构？该布尔判断独立于 Primary Drive。
4. Market metadata：描述作品面向作者的市场语义，不把题材标签当作 Drive 路由。

`semantic_evidence` 必须引用本次请求中的具体语义关系，说明为何提出这些体验与 Drive。genre 为空仍需分析 premise；不得以“信息不足”返回全部 MEDIUM/NORMAL。若 `CUSTOM` 是最合适的 Drive，必须给出真实语义理由。

## 输出

写 `artifacts/reader_kernel/proposal.json`，字段为：

- `schema_version=original-reader-kernel-v1`
- `information_status=PROPOSAL`
- `summary`
- `reader_experience`：复用 `ReaderExperienceContract`
- `market_category`：复用 `MarketCategoryMetadata`
- `narrative_drive`：复用 `NarrativeDriveContract`
- `semantic_evidence`
- `uncertainties`
- `author_attention_points`

三个结构的 `status` 必须为 `NEEDS_REVIEW`。Reader priorities 必须恰好覆盖全部现有 ReaderExperience。不得写 `EFFECTIVE`，不得写 Canon。

## 禁止越级

不得生成或决定：

- Core Innovation、外挂、升级树或完整资源经济
- Story Foundation、主角承载方案或第一阶段
- 长期世界阶段、固定剧情、首章候选或正文
- premise/genre 关键词路由、固定 creative taxonomy 或 named novel imitation

本任务只提出“读者期待、长期推进方式、是否需要成长引擎”。

## 完成

写业务 `result.json`：`completed_stage=READER_KERNEL_PROPOSED`，`artifact_paths` 包含 `artifacts/reader_kernel/proposal.json`；`validation_summary`、`warnings`、`next_action` 可按实际业务结果提供。随后使用复制指令给出的绝对 `library_root` 和 workflow start 返回的同一个 `claim_token` 运行 `novel workflow complete`。

不要手写 `handoff_id`、`handoff_type`、`book_id`、`edition_id`、`requested_stage`、`status`、`base_event_seq`、`base_projection_hash`、`canon_committed` 或 `edition_activated`；这些 deterministic envelope 字段由 Python complete 注入并验证。
