# Web Author Control / Story Game State

这是 G1 的架构边界，面向作者工作台，不替代 Canon、Edition、Revision 或 Approval。

```text
Source / Authoritative Events
        ↓
Historical Canon Projection (chapter timepoint)
        ↓
Story Game State read model
        ↓
Workbench panels: character / world / faction / relationship / task

Workbench gesture
        ↓
AuthorStateCommand
        ↓
Author Control service
        ├─ Author Intent (future item / relationship goal / revision request)
        └─ Author Task (SHORT / MID / LONG)
```

## 读路径

章节选择只决定查询边界。只有存在对应 `canon_commits.event_end_seq` 时，状态面板才会调用 `projection_from_connection` 读取该章节的正史截面；读取不会调用持久化投影重建。没有章节事件锚点时显示“尚无正史时间点”，不使用最新状态填充历史章节。

人物、背包、装备、能力、知识和关系只来自该时间点的 Canon Projection。Runtime Baseline 是来源验证后的参考层；Story Atlas 角色、势力和关系是 `SOFT_REFERENCE`，在界面上明确标注，不会被合并成当前运行状态。

## 写路径

`author_control_intents`、`author_control_tasks` 和 `author_control_history` 是独立的作者控制层。Author Command 可以创建或移动它们，但不会追加 `events`、`canon_commits`，也不会修改 `projection_metadata`、`editions` 或 Approval 状态。

当前状态的背包/装备拖拽默认被拒绝，并返回 `REVISION_REQUIRED` 方向；不存在于历史状态的物品进入当前背包时返回 `CURRENT_ITEM_EVIDENCE_MISSING`，只允许选择未来意图或改写请求。

任务拖拽只提交 `MOVE_TASK_HORIZON`。SHORT、MID、LONG 是作者规划组合，不是固定逐章大纲，也不自动驱动续写。

## G1 有意不做的事

- 不生成 HP、MP、等级或其他原文没有的 RPG 数值。
- 不把 Atlas 软理解升级为 Canon。
- 不做 3D 图、复杂地图、全自动势力系统或拖拽即批准。
- 不从 Web 调用 Codex subprocess、OpenAI API 或审批流程。
