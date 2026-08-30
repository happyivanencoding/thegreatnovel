触发事件：提前涌入的地潮继续冲击旧关外层，第三座新潮井喷涌、第一辆粮车卡住，粮道、三座井与砺骨部迁徙水路同时承压。

推动事件的人：顾停舟。他把“保住所有东西”的目标改成一次明确取舍：本体承担粮队与主水路的正面压力，分身只携带“定住”去第二个潮压节点固定回潮楔。

主角行动：顾停舟用成炉本体稳定粮道和主水路；分身将回潮楔固定在第二个潮压节点，在三座新井即将被潮势冲垮时，把其中一股潮势改向已经决定放弃的旧关外层。

对手或世界反应：潮势被改道后，旧关外层承受全部冲击并持续塌毁；顾沉戈继续守住三座新井，少东家让粮队沿保住的粮道脱离卡口，砺骨部前哨抓住重新出现的水路窗口。各方都必须接受外层被牺牲的结果。

直接结果：粮道保住，三座新潮井没有被毁，砺骨部获得一段可以实际通过的迁徙取水窗口；旧关外层被潮势彻底毁弃。本轮地潮冲击暂时过去。

状态变化：回潮楔完成一次完整释放，仍归顾停舟所有，但再次使用前必须散尽残压；顾停舟没有获得新的境界升级。外层毁弃后，旧关内侧观测点暴露，照域潮谱仍在其中；地潮提前的原因本章仍未查明。

叙事功能：第一次把“借身＋回潮楔”用于改写公共资源与迁徙路线，而不是重复完成一次救援；让顾停舟的核心优势同时改变粮道、供水与部族行动空间，并用外层毁弃锁定真实代价。

结尾推动力：观测点暴露后，顾停舟确认其中仍有照域潮谱。若不进入观测点，下一轮潮势将直接冲向撤离队伍；本章停在入口暴露处，不提前进入或取得潮谱。

## 专项建议

Opening：启用；直接承接第三井喷涌、粮车卡死与本体/分身的分工选择。

Action：启用；本章的主要兑现是双点承压、改道与外层牺牲，行动结果应持续推动取舍。

## ATOMIC AUTHORITY IR

```json
{
  "schema_version": "atomic-mission-ir-v1",
  "chapter_id": "JIUCHUI:CH016",
  "protagonist_id": "PROTAGONIST_001",
  "facts": [
    {
      "fact_id": "CH016_TIDE_PRESSURE_CONTINUES",
      "slot_id": "SLOT_TIDE_PRESSURE",
      "source_ref": "director.trigger_event.0",
      "kind": "event",
      "mode": "must_hold",
      "phase": "during_chapter",
      "actor_id": "",
      "action_id": "continue_tide_impact",
      "object_ids": [
        "LOCATION_OUTER_PASS_001",
        "RESOURCE_WELLS_001",
        "ROUTE_GRAIN_001",
        "ROUTE_WATER_001"
      ],
      "counterparty_ids": [],
      "from_state": "第三井喷涌、粮车卡住，三方通行空间同时受威胁",
      "to_state": "提前地潮继续冲击旧关外层并扩大多点危局",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_PROTAGONIST_SPLITS_PRESSURE_BURDEN",
      "slot_id": "SLOT_BURDEN_SPLIT",
      "source_ref": "director.driving_actor.0",
      "kind": "action",
      "mode": "must_hold",
      "phase": "during_chapter",
      "actor_id": "PROTAGONIST_001",
      "action_id": "split_pressure_burden",
      "object_ids": [
        "ROUTE_GRAIN_001",
        "ROUTE_WATER_001",
        "ITEM_RETURN_TIDE_WEDGE_001",
        "LOCATION_SECOND_PRESSURE_NODE_001"
      ],
      "counterparty_ids": [
        "CLONE_001"
      ],
      "from_state": "回潮楔残压未散，粮道与水路同时承压",
      "to_state": "本体与分身分别承担正面承压和节点固定",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH016_TIDE_PRESSURE_CONTINUES"
      ],
      "metadata": {}
    },
    {
      "fact_id": "CH016_BODY_STABILIZES_ROUTES",
      "slot_id": "SLOT_BODY_ROUTE_STABILITY",
      "source_ref": "director.protagonist_action.0",
      "kind": "action",
      "mode": "must_hold",
      "phase": "during_chapter",
      "actor_id": "PROTAGONIST_001",
      "action_id": "stabilize_grain_and_water_routes",
      "object_ids": [
        "ROUTE_GRAIN_001",
        "ROUTE_WATER_001"
      ],
      "counterparty_ids": [],
      "from_state": "粮道卡死，主水路受潮势冲击",
      "to_state": "粮队与主水路获得可持续通行的稳定窗口",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH016_PROTAGONIST_SPLITS_PRESSURE_BURDEN"
      ],
      "metadata": {}
    },
    {
      "fact_id": "CH016_CLONE_FIXES_WEDGE_AT_NODE",
      "slot_id": "SLOT_WEDGE_NODE_FIX",
      "source_ref": "director.protagonist_action.1",
      "kind": "action",
      "mode": "must_hold",
      "phase": "during_chapter",
      "actor_id": "CLONE_001",
      "action_id": "fix_wedge_at_second_node",
      "object_ids": [
        "ITEM_RETURN_TIDE_WEDGE_001",
        "LOCATION_SECOND_PRESSURE_NODE_001"
      ],
      "counterparty_ids": [],
      "from_state": "分身只携带定住，回潮楔尚未重新固定",
      "to_state": "回潮楔被固定在第二个潮压节点",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH016_PROTAGONIST_SPLITS_PRESSURE_BURDEN"
      ],
      "metadata": {}
    },
    {
      "fact_id": "CH016_TIDE_REDIRECTED_TO_OUTER_PASS",
      "slot_id": "SLOT_TIDE_REDIRECTION",
      "source_ref": "director.protagonist_action.2",
      "kind": "direct_result",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "CLONE_001",
      "action_id": "redirect_tide_to_outer_pass",
      "object_ids": [
        "ITEM_RETURN_TIDE_WEDGE_001",
        "RESOURCE_WELLS_001",
        "LOCATION_OUTER_PASS_001"
      ],
      "counterparty_ids": [],
      "from_state": "潮势即将冲垮三座新潮井",
      "to_state": "一股潮势被改向已经放弃的旧关外层",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_CLONE_FIXES_WEDGE_AT_NODE"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_GRAIN_ROUTE_PRESERVED",
      "slot_id": "SLOT_GRAIN_ROUTE",
      "source_ref": "director.direct_result.0",
      "kind": "direct_result",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "preserve_grain_route",
      "object_ids": [
        "ROUTE_GRAIN_001"
      ],
      "counterparty_ids": [],
      "from_state": "第一辆粮车在第三井前卡住",
      "to_state": "粮道保住，粮队脱离当前卡口并保有继续通行条件",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_BODY_STABILIZES_ROUTES",
        "CH016_TIDE_REDIRECTED_TO_OUTER_PASS"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_WELLS_SURVIVE",
      "slot_id": "SLOT_NEW_WELLS",
      "source_ref": "director.direct_result.1",
      "kind": "direct_result",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "preserve_new_wells",
      "object_ids": [
        "RESOURCE_WELLS_001"
      ],
      "counterparty_ids": [],
      "from_state": "第三井井口裂开并喷涌",
      "to_state": "三座新潮井没有被本轮潮势摧毁",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_TIDE_REDIRECTED_TO_OUTER_PASS"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_WATER_ROUTE_WINDOW_OPEN",
      "slot_id": "SLOT_MIGRATION_WATER_WINDOW",
      "source_ref": "director.direct_result.2",
      "kind": "direct_result",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "open_migration_water_window",
      "object_ids": [
        "ROUTE_WATER_001"
      ],
      "counterparty_ids": [],
      "from_state": "砺骨部迁徙水路因塌方无法通行",
      "to_state": "砺骨部获得可以实际通过的迁徙取水窗口",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_BODY_STABILIZES_ROUTES",
        "CH016_TIDE_REDIRECTED_TO_OUTER_PASS"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_OUTER_PASS_DESTROYED",
      "slot_id": "SLOT_OUTER_PASS",
      "source_ref": "director.state_change.0",
      "kind": "state_transition",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "",
      "action_id": "destroy_outer_pass",
      "object_ids": [
        "LOCATION_OUTER_PASS_001"
      ],
      "counterparty_ids": [],
      "from_state": "旧关外层承受被改道的潮势",
      "to_state": "旧关外层被彻底毁弃",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_TIDE_REDIRECTED_TO_OUTER_PASS"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_WEDGE_RELEASED_AND_COOLDOWN_REQUIRED",
      "slot_id": "SLOT_WEDGE_COOLDOWN",
      "source_ref": "director.state_change.1",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "phase": "post_chapter",
      "actor_id": "PROTAGONIST_001",
      "action_id": "require_wedge_pressure_dissipation",
      "object_ids": [
        "ITEM_RETURN_TIDE_WEDGE_001"
      ],
      "counterparty_ids": [],
      "from_state": "回潮楔残压未散，尚未再次使用",
      "to_state": "回潮楔完成一次完整释放，仍归顾停舟所有，再次使用前必须散尽残压",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [
        "CH016_TIDE_REDIRECTED_TO_OUTER_PASS"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_CURRENT_TIDE_PASSED",
      "slot_id": "SLOT_TIDE_WINDOW_PASSED",
      "source_ref": "director.state_change.2",
      "kind": "deadline",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "",
      "action_id": "complete_current_tide_passage",
      "object_ids": [
        "LOCATION_OUTER_PASS_001"
      ],
      "counterparty_ids": [],
      "from_state": "本轮地潮正在冲击旧关外层",
      "to_state": "本轮地潮冲击已经过去",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_OUTER_PASS_DESTROYED"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_OBSERVATION_POINT_EXPOSED",
      "slot_id": "SLOT_OBSERVATION_POINT_EXPOSED",
      "source_ref": "director.ending_drive.0",
      "kind": "ending",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "",
      "action_id": "expose_observation_point",
      "object_ids": [
        "LOCATION_OBSERVATION_POINT_001",
        "LOCATION_OUTER_PASS_001"
      ],
      "counterparty_ids": [],
      "from_state": "旧关内侧观测点被外层遮蔽",
      "to_state": "外层毁弃后观测点暴露，内部仍有照域潮谱",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [
        "CH016_OUTER_PASS_DESTROYED"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_NEXT_TIDE_THREATENS_RETREAT_ROUTE",
      "slot_id": "SLOT_NEXT_TIDE_THREAT",
      "source_ref": "director.ending_drive.1",
      "kind": "ending",
      "mode": "conditional",
      "phase": "post_chapter",
      "actor_id": "",
      "action_id": "threaten_retreat_route",
      "object_ids": [
        "LOCATION_OBSERVATION_POINT_001",
        "ROUTE_WATER_001"
      ],
      "counterparty_ids": [],
      "from_state": "观测点已暴露但尚未进入",
      "to_state": "若不进入观测点，下一轮潮势将直接冲向撤离队伍",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [
        "CH016_OBSERVATION_POINT_EXPOSED"
      ],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH016_EARLY_TIDE_CAUSE_UNKNOWN",
      "slot_id": "SLOT_EARLY_TIDE_CAUSE",
      "source_ref": "director.state_change.3",
      "kind": "unknown_boundary",
      "mode": "must_remain_unknown",
      "phase": "chapter_end",
      "actor_id": "",
      "action_id": "retain_early_tide_cause_unknown",
      "object_ids": [
        "MYSTERY_EARLY_TIDE_001"
      ],
      "counterparty_ids": [],
      "from_state": "地潮提前涌入旧关外层",
      "to_state": "本章结束时提前原因仍未查明",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    }
  ]
}
```
