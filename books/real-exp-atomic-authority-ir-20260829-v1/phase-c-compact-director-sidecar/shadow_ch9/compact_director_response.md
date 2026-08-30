触发事件：合影回流的伤势在峡外临时营地集中发作，顾临川短暂失去行动力；药队尚未完全撤出，陆绾必须替他处理伤口，顾斜阳则从获救弟子口中核对两条撤离线的经过。

推动事件的人：陆绾主动处理伤势并划定分影风险边界；顾斜阳追问并确认双线行动；铜羽领队在章末整理撤离记录。

主角行动：顾临川接受陆绾处理伤口，不把伤势包装成无足轻重；他承认自己既想拿到乌沉短兵，也不想让陆绾死在石城里，不把救人说成单一的无私行为。

对手或世界反应：陆绾明确拒绝再把影身当成可以随便送进危险处的替代品；顾斜阳从三名弟子的证词中确认，顾临川在两条撤离线上都作出了临场选择，开始把他视为有具体取舍、不能简单归类的竞争者。

直接结果：顾临川的伤口得到处理，但合影回流造成的撞击与疲劳仍使他暂时无法行动；顾斜阳确认两条撤离线都真实发生过顾临川的独立选择。

状态变化：陆绾对分影的态度从好奇转为带边界的理解，并把影身伤势视为顾临川本人必须承担的风险；顾斜阳对顾临川的判断从警惕的陌生竞争者，变为有明确欲望与取舍的竞争者。

叙事功能：把分影的能力代价转化为关系边界、自我暴露与竞争者重新估价，确立“分影扩大行动可能，但不能无代价替主角承担危险”的人物事实。

结尾推动力：铜羽领队整理撤离记录时发现，两条行动路线无法用普通一名二阶解释。记录必须被重新上报和评估，下一章由此进入顾临川身份与待遇被重新定价的局面；本章不提前完成新的契约结果。

## 专项建议

Dialogue：启用；本章的关键变化依靠陆绾划界、顾临川承认双重动机，以及顾斜阳确认事实。

Emotion：启用；只跟随伤势与关系重新定价，不扩写成群体性惊叹。

## AAIR1
```json
{
  "v": "AAIR1",
  "chapter": "SHADOW:CH009",
  "protagonist": "PROTAGONIST_001",
  "actions": [
    {
      "slot": "event:SHADOW:CH009:accept_injury_treatment",
      "actor": "PROTAGONIST_001",
      "verb": "接受伤势处理",
      "objects": ["STATE_INJURY_001"],
      "counterparties": ["CHAR_PARTNER_001"]
    },
    {
      "slot": "event:SHADOW:CH009:admit_dual_choice",
      "actor": "PROTAGONIST_001",
      "verb": "承认救人与取兵并存",
      "objects": ["ITEM_UMBRA_WEAPON_001", "CHAR_PARTNER_001"],
      "counterparties": ["CHAR_PARTNER_001"]
    },
    {
      "slot": "event:SHADOW:CH009:confirm_two_routes",
      "actor": "CHAR_RIVAL_001",
      "verb": "确认双线真实选择",
      "objects": ["PROTAGONIST_001"],
      "counterparties": []
    }
  ],
  "results": [
    {
      "slot": "resource:STATE_INJURY_001",
      "kind": "resource_transition",
      "actor": "PROTAGONIST_001",
      "verb": "接受处理",
      "objects": ["STATE_INJURY_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "合影回流伤势未处理",
      "to": "伤势已处理但仍暂时失去行动力",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH009:accept_injury_treatment"],
      "meta": {}
    },
    {
      "slot": "result:SHADOW:CH009:dual_choice_admitted",
      "kind": "direct_result",
      "actor": "PROTAGONIST_001",
      "verb": "确认双重选择依据",
      "objects": ["ITEM_UMBRA_WEAPON_001", "CHAR_PARTNER_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "",
      "to": "救人与取兵同时成立",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH009:admit_dual_choice"],
      "meta": {}
    },
    {
      "slot": "result:SHADOW:CH009:two_route_confirmation",
      "kind": "direct_result",
      "actor": "CHAR_RIVAL_001",
      "verb": "确认双线选择",
      "objects": ["PROTAGONIST_001"],
      "counterparties": [],
      "from": "双线经过未被确认",
      "to": "两条撤离线均确认存在真实选择",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH009:confirm_two_routes"],
      "meta": {}
    }
  ],
  "states": [
    {
      "slot": "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
      "kind": "relationship_transition",
      "actor": "PROTAGONIST_001",
      "verb": "建立风险边界",
      "objects": ["ABILITY_SHADOW_CLONE_001", "STATE_INJURY_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "对分影保持好奇",
      "to": "带边界的理解并拒绝将影身视为可随意替代品",
      "value": null,
      "terminal": true,
      "depends": ["result:SHADOW:CH009:dual_choice_admitted"],
      "meta": {}
    },
    {
      "slot": "relationship:PROTAGONIST_001:CHAR_RIVAL_001",
      "kind": "relationship_transition",
      "actor": "PROTAGONIST_001",
      "verb": "重新定位竞争关系",
      "objects": ["PROTAGONIST_001"],
      "counterparties": ["CHAR_RIVAL_001"],
      "from": "警惕的陌生竞争者",
      "to": "有具体取舍且不能简单归类的竞争者",
      "value": null,
      "terminal": true,
      "depends": ["result:SHADOW:CH009:two_route_confirmation"],
      "meta": {}
    }
  ],
  "ending": [
    {
      "slot": "ending:SHADOW:CH009:route_record_anomaly",
      "kind": "ending",
      "actor": "ORG_COPPER_FEATHER_001",
      "verb": "发现双线记录异常",
      "objects": ["RECORD_ESCORT_001", "PROTAGONIST_001"],
      "counterparties": [],
      "from": "普通一名二阶可解释",
      "to": "无法按普通一名二阶解释",
      "value": null,
      "terminal": true,
      "depends": ["result:SHADOW:CH009:two_route_confirmation"],
      "meta": {}
    }
  ],
  "boundaries": [
    {
      "slot": "ability:ABILITY_SHADOW_CLONE_001:shared_injury",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "actor": "PROTAGONIST_001",
      "verb": "共享伤势回流",
      "objects": ["ABILITY_SHADOW_CLONE_001", "STATE_INJURY_001"],
      "counterparties": [],
      "from": "影身可独立行动",
      "to": "归体后伤势与疲劳共同回流并造成短暂失能",
      "value": null,
      "depends": ["resource:STATE_INJURY_001"],
      "meta": {}
    },
    {
      "slot": "ability:ABILITY_SHADOW_CLONE_001:not_disposable",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "actor": "PROTAGONIST_001",
      "verb": "承担分影代价",
      "objects": ["ABILITY_SHADOW_CLONE_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "可被视为危险替代品",
      "to": "不可无代价替代本体",
      "value": null,
      "depends": ["relationship:PROTAGONIST_001:CHAR_PARTNER_001"],
      "meta": {}
    },
    {
      "slot": "mystery:RECORD_ESCORT_001",
      "kind": "unknown_boundary",
      "mode": "must_remain_unknown",
      "actor": "",
      "verb": "保持异常原因未解",
      "objects": ["RECORD_ESCORT_001"],
      "counterparties": [],
      "from": "双线记录异常",
      "to": "异常原因尚未揭晓",
      "value": null,
      "depends": ["ending:SHADOW:CH009:route_record_anomaly"],
      "meta": {}
    }
  ]
}
```
