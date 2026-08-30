触发事件：首轮胜利后，顾临川立即被安排迎战杜衡；杜衡以陌生步法指出他“退得太习惯”，逼他在严重疲劳中重新应对临场变化。

推动事件的人：杜衡主动改变交手节奏并持续压迫；铜羽试场执事推动下一轮比试与最终记名；陆绾随后来客舍确认折日峡送药安排。

主角行动：顾临川不公开分影，凭两份训练回流后的刀感观察杜衡，改变退步与出刃时机，在疲劳和影形迟滞仍存在的情况下赢下交手；试场结束后，他主动让陆绾同时看见内院与后门的两个自己，并接受铜羽随队契约。

对手或世界反应：杜衡的陌生步法迫使顾临川不能重复武馆经验；试场执事与铜羽商盟确认他的连续实战稳定，将他从普通武馆弟子重新估价为正式一阶护卫候选；陆绾确认分影真实存在后，决定与药队同行。

直接结果：顾临川赢得本轮及本次公开试场的名次结算，取得铜羽随队契约与第一笔预付钱；陆绾成为第一个明确知道分影存在的人，并确定同行。

状态变化：顾临川公开身份从客舍家庭成员、武馆学徒，变为被铜羽商盟记住的正式一阶随队护卫候选；他与陆绾之间形成基于真实能力 disclosure 的同行关系；客舍事务已交回父母，顾临川不再默认同时承担家中稳定职责与外出机会。

叙事功能：完成“一镇两份日子”的阶段结算，让分影带来的战斗优势、公开名声、金钱、离乡资格和关系变化同时落地；同时明确疲劳回流与临场迟滞仍是现实边界。

结尾推动力：铜羽商队与药队次日出发，折日峡成为顾临川第一次离开熟悉城镇、必须用新身份承担风险的行动入口；本章不提前完成进入峡中的后续事件。

## 专项建议

Opening：不启用；本章已从上一轮比试的即时衔接开始，直接承接杜衡出场。

Action：启用；杜衡的陌生步法、顾临川的疲劳与不公开分影共同构成本章主要冲突。

## AAIR1

```json
{
  "v": "AAIR1",
  "chapter": "SHADOW:CH004",
  "protagonist": "PROTAGONIST_001",
  "actions": [
    {
      "slot": "event:SHADOW:CH004:win_du_heng",
      "actor": "PROTAGONIST_001",
      "verb": "win_public_match",
      "objects": ["CHAR_OPPONENT_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"]
    },
    {
      "slot": "event:SHADOW:CH004:disclose_shadow",
      "actor": "PROTAGONIST_001",
      "verb": "disclose_ability",
      "objects": ["ABILITY_SHADOW_CLONE_001"],
      "counterparties": ["CHAR_PARTNER_001"]
    },
    {
      "slot": "event:SHADOW:CH004:accept_escort_contract",
      "actor": "PROTAGONIST_001",
      "verb": "accept_contract",
      "objects": ["CONTRACT_ESCORT_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"]
    }
  ],
  "results": [
    {
      "slot": "result:SHADOW:CH004:public_match",
      "kind": "public_proof",
      "actor": "PROTAGONIST_001",
      "verb": "establish_public_first_tier_stability",
      "objects": ["TIER_FIRST_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"],
      "from": "unconfirmed",
      "to": "publicly_confirmed",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH004:win_du_heng"],
      "meta": {}
    },
    {
      "slot": "ownership:CONTRACT_ESCORT_001",
      "kind": "ownership_transition",
      "actor": "PROTAGONIST_001",
      "verb": "hold_contract",
      "objects": ["CONTRACT_ESCORT_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"],
      "from": "not_held",
      "to": "held",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH004:accept_escort_contract"],
      "meta": {}
    },
    {
      "slot": "resource:RESOURCE_PREPAYMENT_001",
      "kind": "resource_transition",
      "actor": "PROTAGONIST_001",
      "verb": "receive_prepayment",
      "objects": ["RESOURCE_PREPAYMENT_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"],
      "from": "not_received",
      "to": "first_prepayment_received",
      "value": null,
      "terminal": true,
      "depends": ["ownership:CONTRACT_ESCORT_001"],
      "meta": {"scope": "first_payment_only"}
    },
    {
      "slot": "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
      "kind": "relationship_transition",
      "actor": "PROTAGONIST_001",
      "verb": "establish_travel_partnership",
      "objects": ["ABILITY_SHADOW_CLONE_001", "GROUP_MEDICINE_CONVOY_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "partner_unaware_of_shadow",
      "to": "partner_knows_shadow_and_chooses_joint_travel",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH004:disclose_shadow"],
      "meta": {}
    }
  ],
  "states": [
    {
      "slot": "state:PROTAGONIST_001",
      "kind": "state_transition",
      "actor": "PROTAGONIST_001",
      "verb": "enter_escort_candidate_status",
      "objects": ["TIER_FIRST_001", "CONTRACT_ESCORT_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"],
      "from": "local_apprentice",
      "to": "public_formal_first_tier_escort_candidate",
      "value": null,
      "terminal": true,
      "depends": ["result:SHADOW:CH004:public_match", "ownership:CONTRACT_ESCORT_001"],
      "meta": {}
    },
    {
      "slot": "ability:ABILITY_SHADOW_CLONE_001:fatigue_return",
      "kind": "ability_boundary",
      "actor": "PROTAGONIST_001",
      "verb": "retain_shared_fatigue",
      "objects": ["ABILITY_SHADOW_CLONE_001"],
      "counterparties": [],
      "from": "fatigue_can_be_separated",
      "to": "fatigue_returns_on_reunion",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH004:win_du_heng"],
      "meta": {}
    },
    {
      "slot": "ability:ABILITY_SHADOW_CLONE_001:improvisation_delay",
      "kind": "ability_boundary",
      "actor": "PROTAGONIST_001",
      "verb": "retain_delayed_response",
      "objects": ["ABILITY_SHADOW_CLONE_001"],
      "counterparties": ["CHAR_OPPONENT_001"],
      "from": "shadow_handles_unfamiliar_change_normally",
      "to": "shadow_response_remains_delayed",
      "value": null,
      "terminal": true,
      "depends": ["event:SHADOW:CH004:win_du_heng"],
      "meta": {}
    }
  ],
  "ending": [
    {
      "slot": "ending:SHADOW:CH004:next_day_departure",
      "kind": "deadline",
      "actor": "PROTAGONIST_001",
      "verb": "depart_next_day",
      "objects": ["CONTRACT_ESCORT_001", "GROUP_MEDICINE_CONVOY_001", "ROUTE_CANYON_001"],
      "counterparties": ["ORG_COPPER_FEATHER_001"],
      "from": "not_departed",
      "to": "departure_due",
      "value": null,
      "terminal": true,
      "depends": ["ownership:CONTRACT_ESCORT_001", "relationship:PROTAGONIST_001:CHAR_PARTNER_001"],
      "meta": {}
    }
  ],
  "boundaries": [
    {
      "slot": "ability:ABILITY_SHADOW_CLONE_001:no_fatigue_cancellation",
      "kind": "ability_boundary",
      "mode": "must_not_hold",
      "actor": "PROTAGONIST_001",
      "verb": "cancel_shared_fatigue",
      "objects": ["ABILITY_SHADOW_CLONE_001"],
      "counterparties": [],
      "from": "",
      "to": "",
      "value": null,
      "depends": ["event:SHADOW:CH004:win_du_heng"],
      "meta": {}
    }
  ]
}
```
