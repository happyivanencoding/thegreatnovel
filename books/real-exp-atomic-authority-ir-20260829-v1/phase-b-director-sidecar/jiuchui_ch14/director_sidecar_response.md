触发事件：炉钟响起，顾停舟在入口封闭前进入百炉会开炉试。唐绾完成铸潮展示，顾停舟必须让修复后的回潮楔接受一次真实检验。

推动事件的人：唐绾完成展示；阮青蜃以高价买断回潮楔、免除部分契约追索施压；少东家提出固定报酬、明确损失边界的独立粮路合作。

主角行动：顾停舟让回潮楔只完成一次“锁潮—改向—释放”，不把它演示成可连续复制的武器。展示后，他拒绝阮青蜃的买断，接受少东家的独立合作。

对手或世界反应：懂行者确认，普通成炉者只能在自身附近稳定重压，而回潮楔能够改变一整段潮势方向，顾停舟因此被重新定价。阮青蜃转为公开提出买断，少东家则以合作方而非雇主身份与他议价。

直接结果：回潮楔仍归顾停舟所有，使用自主权没有被买断。首批矿脉的独家标记不再被承认为阮青蜃的完整矿权；顾停舟取得公开确认的个人矿利份额，砺骨部水路不被矿权吞并。

状态变化：回潮楔完成一次真实改向后进入残压待散状态，未散尽前不能连续硬压。顾停舟与少东家由主从关系变为有价合作关系；顾停舟开始主动选择粮路作为下一条财富与自由入口，阮青蜃仍保持公开追索立场。

叙事功能：完成古器、矿脉权益和旧关系的第一次公共重估，让顾停舟从“保住已有东西”推进到“选择自己要走的路”。

结尾推动力：独立粮路合作的首批货必须在下一次十二日地潮前送到旧关。章末顾停舟随队出发，下一章必然进入这次运输及其风险。

## 专项建议

Opening：启用；入口封闭与阮青蜃当面追索能立即建立本章压力。

Dialogue：启用；两种报价的差异必须通过具体议价与顾停舟的选择落地。

## ATOMIC AUTHORITY IR

```json
{
  "schema_version": "atomic-mission-ir-v1",
  "chapter_id": "JIUCHUI:CH014",
  "protagonist_id": "PROTAGONIST_001",
  "facts": [
    {
      "fact_id": "CH014_TRIAL_OPENS",
      "slot_id": "chapter_trial_entry",
      "source_ref": "director.trigger_event.0",
      "kind": "event",
      "mode": "terminal",
      "phase": "during_chapter",
      "actor_id": "",
      "action_id": "enter_furnace_trial",
      "object_ids": ["ORG_HUNDRED_FURNACE_001"],
      "counterparty_ids": [],
      "from_state": "入口即将封闭",
      "to_state": "顾停舟进入百炉会开炉试",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH014_WEDGE_SINGLE_REDIRECT",
      "slot_id": "wedge_trial_use",
      "source_ref": "director.protagonist_action.0",
      "kind": "action",
      "mode": "terminal",
      "phase": "during_chapter",
      "actor_id": "PROTAGONIST_001",
      "action_id": "perform_single_tide_redirection",
      "object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparty_ids": ["ORG_HUNDRED_FURNACE_001"],
      "from_state": "回潮楔已修复并可完成锁潮、改向、释放",
      "to_state": "回潮楔完成一次真实改向",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH014_PUBLIC_WEDGE_BENCHMARK",
      "slot_id": "public_power_repricing",
      "source_ref": "director.opponent_or_world_reaction.0",
      "kind": "public_proof",
      "mode": "terminal",
      "phase": "reader_knowledge",
      "actor_id": "",
      "action_id": "confirm_tide_direction_benchmark",
      "object_ids": ["ITEM_RETURN_TIDE_WEDGE_001", "PROTAGONIST_001"],
      "counterparty_ids": ["ORG_HUNDRED_FURNACE_001"],
      "from_state": "回潮楔的真实价值尚未在公开场合完成比较",
      "to_state": "普通成炉者只能在自身附近稳定重压；回潮楔可改变一整段潮势方向；顾停舟被重新定价",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_WEDGE_SINGLE_REDIRECT"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_RIVAL_BUYOUT_OFFER",
      "slot_id": "rival_buyout_pressure",
      "source_ref": "director.opponent_or_world_reaction.1",
      "kind": "event",
      "mode": "terminal",
      "phase": "during_chapter",
      "actor_id": "CHAR_RIVAL_001",
      "action_id": "offer_wedge_buyout",
      "object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparty_ids": ["PROTAGONIST_001"],
      "from_state": "阮青蜃继续追索回潮楔及相关损失",
      "to_state": "阮青蜃提出高价买断回潮楔并免除部分契约追索",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_PUBLIC_WEDGE_BENCHMARK"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_PARTNER_GRAIN_OFFER",
      "slot_id": "partner_independent_cooperation_offer",
      "source_ref": "director.opponent_or_world_reaction.2",
      "kind": "event",
      "mode": "terminal",
      "phase": "during_chapter",
      "actor_id": "CHAR_PARTNER_001",
      "action_id": "offer_independent_grain_cooperation",
      "object_ids": ["ROUTE_GRAIN_001"],
      "counterparty_ids": ["PROTAGONIST_001"],
      "from_state": "顾停舟与少东家仍有旧主从关系",
      "to_state": "少东家提出固定报酬、明确损失边界的独立粮路合作",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_PUBLIC_WEDGE_BENCHMARK"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_WEDGE_BUYOUT_REJECTED",
      "slot_id": "wedge_autonomy_choice",
      "source_ref": "director.protagonist_action.1",
      "kind": "ownership_transition",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "reject_wedge_buyout",
      "object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparty_ids": ["CHAR_RIVAL_001"],
      "from_state": "阮青蜃提出买断与部分追索豁免",
      "to_state": "回潮楔不出售，仍由顾停舟自主决定用途",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_RIVAL_BUYOUT_OFFER"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_GRAIN_COOPERATION_ACCEPTED",
      "slot_id": "grain_cooperation_status",
      "source_ref": "director.protagonist_action.2",
      "kind": "relationship_transition",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "accept_independent_grain_cooperation",
      "object_ids": ["ROUTE_GRAIN_001"],
      "counterparty_ids": ["CHAR_PARTNER_001"],
      "from_state": "顾停舟与少东家为旧主从关系",
      "to_state": "双方建立固定报酬、明确损失边界的有价合作关系",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_PARTNER_GRAIN_OFFER"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_PERSONAL_MINING_SHARE_CONFIRMED",
      "slot_id": "public_personal_mining_share",
      "source_ref": "director.direct_result.0",
      "kind": "resource_transition",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "retain_public_mining_share",
      "object_ids": ["RESOURCE_PERSONAL_MINING_SHARE_001"],
      "counterparty_ids": ["CHAR_RIVAL_001"],
      "from_state": "首批矿脉权益仍处于争议和重估中",
      "to_state": "顾停舟取得公开确认的个人矿利份额，阮青蜃不再被承认拥有完整矿权",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_WEDGE_BUYOUT_REJECTED"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_WEDGE_RESIDUAL_LIMIT",
      "slot_id": "wedge_residual_pressure_limit",
      "source_ref": "director.state_change.0",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "respect_residual_pressure_limit",
      "object_ids": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparty_ids": [],
      "from_state": "回潮楔完成一次锁潮、改向、释放",
      "to_state": "残压未散尽前不得连续硬压",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_WEDGE_SINGLE_REDIRECT"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_GRAIN_DELIVERY_DEADLINE",
      "slot_id": "next_tide_old_pass_deadline",
      "source_ref": "director.ending_drive.0",
      "kind": "deadline",
      "mode": "must_hold",
      "phase": "post_chapter",
      "actor_id": "PROTAGONIST_001",
      "action_id": "deliver_first_grain_batch_before_tide",
      "object_ids": ["ROUTE_GRAIN_001", "LOCATION_OLD_PASS_001", "EVENT_NEXT_TIDE_001"],
      "counterparty_ids": [],
      "from_state": "首批粮路货物尚未送达旧关",
      "to_state": "必须在下一次十二日地潮前送到旧关",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": ["CH014_GRAIN_COOPERATION_ACCEPTED"],
      "metadata": {}
    },
    {
      "fact_id": "CH014_DEPARTURE_WITH_GRAIN_TEAM",
      "slot_id": "chapter_end_departure",
      "source_ref": "director.ending_drive.1",
      "kind": "ending",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "depart_with_grain_team",
      "object_ids": ["ROUTE_GRAIN_001"],
      "counterparty_ids": ["CHAR_PARTNER_001"],
      "from_state": "粮路合作已接受但尚未出发",
      "to_state": "顾停舟随队出发，首批粮路运输开始",
      "value": null,
      "terminal": true,
      "condition_fact_ids": ["CH014_GRAIN_DELIVERY_DEADLINE"],
      "depends_on_fact_ids": ["CH014_GRAIN_COOPERATION_ACCEPTED"],
      "metadata": {}
    }
  ]
}
```
