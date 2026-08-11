---
name: bootstrap-original-novel
description: 为 creation_mode=ORIGINAL 且无来源正文的新小说，从 premise 生成严格的 Story Foundation Proposal；用于 ORIGINAL_BOOK_BOOTSTRAP handoff。只写 Proposal artifact，不创建章节或 Canon。
---

# Bootstrap Original Novel

此 Skill 只处理 `ORIGINAL_BOOK_BOOTSTRAP` 本地文件 handoff。它建立作者可以选择和编辑的
Story Foundation Proposal，不负责替作者确认，不生成“第 0 章”，也不运行已有小说的 Arc
Extraction 或 Story Atlas 初始化。

## 输入

1. 先按 `$process-novel-handoff` 领取任务并校验冻结文件。
2. 完整读取 `task.json`、`original_request.json`、`proposal_schema.json` 和
   `output_schema.json`。
3. `premise` 是唯一必填作者输入。类型、文风、视角、篇幅、must include、forbidden 与抽象
   reference traits 都是约束；reference traits 不得被复制为来源小说的人物、设定或情节。

## Proposal 合同

严格按 `proposal_schema.json` 写
`artifacts/story_foundation/proposal.json`，并满足：

- `information_status` 必须为 `PROPOSAL`。
- 恰好三个不同书名。
- 恰好三个结构上不同的 Story Foundation；每个都含阅读承诺、主角、目标、主冲突、世界
  机制、成长循环、长期可能性、风险以及与 premise 的关系。
- 给出主角目标、冲突、代价与成长，明确世界规则、人物和势力。
- 恰好三条未来路线，给出推荐路线和理由；三条路线是同一本书的可能方向，不创建 Book 或
  Edition。
- 给出第一阶段目标和 SHORT/MID/LONG Rolling Planning。LONG 只描述方向与可能性，不得写
  固定结局或逐章 FAR 大纲。
- 恰好三个结构上不同的第一章候选；每个都含开场情境、hook、本章目标、关键选择、冲突、
  主角行动、代价、不可逆改变、章末转折和差异说明。
- 明确开放问题、风险和需要避免的陈词滥调；未知保持开放，不猜成事实。

## 硬边界

不得修改 `book/`，不得建立 Source Manifest、假章节、Chapter 0、Canon Event、Canon Commit、
Edition、Author Truth、Book Profile 或 Planning Aggregate。不得替作者执行“确认基础框架”。

## 完成

校验 Proposal 后，按 `output_schema.json` 写 `result.json`：

- `handoff_type=ORIGINAL_BOOK_BOOTSTRAP`
- `requested_stage=ORIGINAL_BOOK_BOOTSTRAP`
- `completed_stage=FOUNDATION_PROPOSED`
- `candidate_ids` 与三个 Foundation 的 `candidate_id` 顺序完全一致
- `artifact_paths` 包含 `artifacts/story_foundation/proposal.json`
- `canon_committed=false`、`edition_activated=false`
- `next_action` 明确为作者审阅、编辑并显式确认基础框架

最后按 Local File Handoff 协议写状态和事件并进入 `COMPLETED`。
