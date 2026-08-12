# Progression / World State 验收

`ChapterWorldStateView` 仍是唯一章节状态入口。新增 `progression_state`、`world_expansion`、`opportunity_surface`、`payoff_readiness`、`anticipation` 都是 Projection only。

验收事实：

- 每次必须传真实 `chapter_id`；Progression API 对不存在章节返回 404，不静默回退 latest。
- 早期章节看不到后章才获得的资源或能力。
- 缺阶段证据时 `current_stage=null`、readiness=`UNKNOWN`，不显示伪百分比。
- Opportunity 不会进入“已拥有资源”。
- 无 Effective Progression Contract 的旧书仍可读、可编辑、可使用既有 World State。
- 生成导入小说建议合同与逐项确认均不新增 Event、Canon Commit 或 Author Truth。

测试：`tests/integration/test_story_world_workbench_v2_2.py`。
