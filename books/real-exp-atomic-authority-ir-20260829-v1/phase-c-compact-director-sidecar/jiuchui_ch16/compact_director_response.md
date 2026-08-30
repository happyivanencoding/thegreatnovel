触发事件：提前涌入的地潮同时冲击第三座新潮井、粮道、撤离通道与砺骨部水路，第一辆粮车被卡住，三座井和迁徙人群都将失去通行窗口。

推动事件的人：顾停舟。他判断回潮楔残压未散，不能再次用来硬顶整股潮势，必须主动选择保住粮道、新井与水路的组合。

主角行动：顾停舟让成炉本体稳定粮队与主水路；分身只携带“定住”，把回潮楔固定在第二个潮压节点，使回潮楔承住并改向本会冲垮新井的潮势，将其导向旧关外层。

对手或世界反应：地潮沿新的受力方向爆发，旧关外层被彻底冲毁；粮队、三座新潮井和砺骨部水路承受住这一轮冲击，但原有外层道路与居住区不再可用。

直接结果：粮道保住，三座新潮井没有被毁；砺骨部获得这一轮可以实际通过的迁徙取水窗口；旧关外层彻底毁弃。回潮楔完成一次完整释放后仍归顾停舟所有。

状态变化：顾停舟第一次用“借身＋回潮楔”改变公共资源与迁徙路线，而非单纯救援；回潮楔再次使用前必须先散尽本次释放后的残压。旧关内侧观测点因外层毁弃而暴露，照域潮谱仍在其中；地潮提前的原因仍未解决。

叙事功能：完成复合能力从个人危机处置到公共局势改道的第一次换挡，同时让顾停舟以独立承运人的选择承担真实的公共后果，并完成本轮地潮已造成不可逆变化的阶段结算。

结尾推动力：外层毁弃后，旧关内侧观测点暴露；若顾停舟不进入观测点取得照域潮谱，下一轮潮势将直接冲向撤离队伍，因此下一章必须转入观测点行动。本章不提前进入或结算观测点内容。

## 专项建议

Opening：启用；直接从粮车卡死、井口喷涌与人群受阻切入，避免重复解释上一章分工。

Action：启用；重点呈现本体与分身分别承担两个关键位置，以及潮势被改向后造成的不可逆公共结果。

## AAIR1

```json
{
  "v": "AAIR1",
  "chapter": "JIUCHUI:CH016",
  "protagonist": "PROTAGONIST_001",
  "actions": [
    {
      "slot": "event:JIUCHUI:CH016:stabilize_public_routes",
      "actor": "PROTAGONIST_001",
      "verb": "stabilize",
      "objects": [
        "ROUTE_GRAIN_001",
        "ROUTE_WATER_001",
        "RESOURCE_WELLS_001"
      ],
      "counterparties": []
    },
    {
      "slot": "event:JIUCHUI:CH016:fix_second_pressure_node",
      "actor": "CLONE_001",
      "verb": "fix",
      "objects": [
        "ITEM_RETURN_TIDE_WEDGE_001",
        "LOCATION_SECOND_PRESSURE_NODE_001"
      ],
      "counterparties": []
    },
    {
      "slot": "event:JIUCHI:CH016:redirect_tide_to_outer_pass",
      "actor": "PROTAGONIST_001",
      "verb": "redirect",
      "objects": [
        "ITEM_RETURN_TIDE_WEDGE_001",
        "LOCATION_OUTER_PASS_001"
      ],
      "counterparties": []
    }
  ],
  "results": [
    {
      "slot": "resource:ROUTE_GRAIN_001",
      "kind": "resource_transition",
      "actor": "PROTAGONIST_001",
      "verb": "preserve",
      "objects": [
        "ROUTE_GRAIN_001"
      ],
      "counterparties": [],
      "from": "blocked",
      "to": "usable",
      "value": null,
      "terminal": true,
      "depends": [
        "event:JIUCHI:CH016:stabilize_public_routes"
      ],
      "meta": {}
    },
    {
      "slot": "resource:RESOURCE_WELLS_001",
      "kind": "resource_transition",
      "actor": "PROTAGONIST_001",
      "verb": "preserve",
      "objects": [
        "RESOURCE_WELLS_001"
      ],
      "counterparties": [],
      "from": "under_tide_impact",
      "to": "not_destroyed",
      "value": null,
      "terminal": true,
      "depends": [
        "event:JIUCHI:CH016:redirect_tide_to_outer_pass"
      ],
      "meta": {}
    },
    {
      "slot": "resource:ROUTE_WATER_001",
      "kind": "resource_transition",
      "actor": "PROTAGONIST_001",
      "verb": "open",
      "objects": [
        "ROUTE_WATER_001"
      ],
      "counterparties": [],
      "from": "threatened",
      "to": "usable_migration_window",
      "value": null,
      "terminal": true,
      "depends": [
        "event:JIUCHI:CH016:redirect_tide_to_outer_pass"
      ],
      "meta": {}
    },
    {
      "slot": "result:JIUCHI:CH016:outer_pass_destroyed",
      "kind": "direct_result",
      "actor": "PROTAGONIST_001",
      "verb": "sacrifice",
      "objects": [
        "LOCATION_OUTER_PASS_001"
      ],
      "counterparties": [],
      "from": "standing",
      "to": "destroyed",
      "value": null,
      "terminal": true,
      "depends": [
        "event:JIUCHI:CH016:redirect_tide_to_outer_pass"
      ],
      "meta": {}
    }
  ],
  "states": [
    {
      "slot": "ability:ITEM_RETURN_TIDE_WEDGE_001:reuse_requires_dissipation",
      "kind": "ability_boundary",
      "actor": "PROTAGONIST_001",
      "verb": "require_dissipation",
      "objects": [
        "ITEM_RETURN_TIDE_WEDGE_001"
      ],
      "counterparties": [],
      "from": "released_once",
      "to": "reuse_blocked_until_dissipation",
      "value": null,
      "terminal": true,
      "depends": [
        "event:JIUCHI:CH016:redirect_tide_to_outer_pass"
      ],
      "meta": {}
    }
  ],
  "ending": [
    {
      "slot": "ending:JIUCHI:CH016:observation_point_exposed",
      "kind": "ending",
      "actor": "PROTAGONIST_001",
      "verb": "expose",
      "objects": [
        "LOCATION_OBSERVATION_POINT_001"
      ],
      "counterparties": [],
      "from": "concealed",
      "to": "exposed",
      "value": null,
      "terminal": true,
      "depends": [
        "result:JIUCHI:CH016:outer_pass_destroyed"
      ],
      "meta": {}
    },
    {
      "slot": "ending:JIUCHI:CH016:next_tide_threatens_evacuees",
      "kind": "deadline",
      "actor": "PROTAGONIST_001",
      "verb": "require_entry",
      "objects": [
        "LOCATION_OBSERVATION_POINT_001"
      ],
      "counterparties": [],
      "from": "not_entered",
      "to": "required_before_next_tide",
      "value": null,
      "terminal": true,
      "depends": [
        "ending:JIUCHI:CH016:observation_point_exposed"
      ],
      "meta": {}
    }
  ],
  "boundaries": [
    {
      "slot": "ability:ITEM_RETURN_TIDE_WEDGE_001:reuse_boundary",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "actor": "PROTAGONIST_001",
      "verb": "remain_blocked_until_dissipation",
      "objects": [
        "ITEM_RETURN_TIDE_WEDGE_001"
      ],
      "counterparties": [],
      "from": "released_once",
      "to": "not_ready_for_immediate_reuse",
      "value": null,
      "depends": [
        "ability:ITEM_RETURN_TIDE_WEDGE_001:reuse_requires_dissipation"
      ],
      "meta": {}
    },
    {
      "slot": "mystery:MYSTERY_EARLY_TIDE_001",
      "kind": "unknown_boundary",
      "mode": "must_remain_unknown",
      "actor": "",
      "verb": "remain_unresolved",
      "objects": [
        "MYSTERY_EARLY_TIDE_001"
      ],
      "counterparties": [],
      "from": "unresolved",
      "to": "unresolved",
      "value": null,
      "depends": [],
      "meta": {}
    }
  ]
}
```
