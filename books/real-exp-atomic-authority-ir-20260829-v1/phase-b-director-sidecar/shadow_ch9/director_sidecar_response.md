触发事件：合影归体后，两边的撞击、抓伤与疲劳同时回流，顾临川在峡外临时营地短暂失去行动力；陆绾处理他的伤势，顾斜阳核对两条撤离线的经过。

推动事件的人：陆绾推动伤势与分影代价的摊牌；顾斜阳推动对顾临川真实选择的确认；顾临川决定是否承认自己的双重动机。

主角行动：顾临川接受陆绾处理伤口，并承认自己既想拿到乌沉短兵，也不想让陆绾死在石城里，没有把救人包装成纯粹无私。

对手或世界反应：陆绾明确拒绝再把影身当成可以随便送进危险处的替代品；顾斜阳从三名弟子的叙述中确认，两条撤离线都存在顾临川真实的临场选择。

直接结果：顾临川的伤口得到处理，但行动仍受回传伤势影响；他的取兵欲望与救人意愿同时成为确定事实，不能再被归结为单纯的救援行为。

状态变化：陆绾对分影的态度从好奇转为理解其代价、同时保留明确边界；顾斜阳开始把顾临川视为有具体欲望、却不能简单归类的竞争者。

叙事功能：把分影的伤势共同结算从能力设定转化为关系边界、人物自我暴露与竞争者重新判断。

结尾推动力：铜羽领队整理撤离记录时，发现同一段时间内两条行动路线都留下了有效结果，无法用普通一名二阶护卫解释；下一章必须重新评估顾临川的身份与用法。

## 专项建议

Dialogue：启用；理由：本章的核心变化来自陆绾划定边界、顾临川承认动机、顾斜阳完成判断，治疗过程应压缩。

## ATOMIC AUTHORITY IR

```json
{
  "schema_version": "atomic-mission-ir-v1",
  "chapter_id": "SHADOW:CH009",
  "protagonist_id": "PROTAGONIST_001",
  "facts": [
    {
      "fact_id": "CH9_MERGE_INJURY_COLLAPSE",
      "slot_id": "chapter9_injury_return",
      "source_ref": "director.触发事件.0",
      "kind": "event",
      "mode": "must_hold",
      "phase": "during_chapter",
      "actor_id": "PROTAGONIST_001",
      "action_id": "suffer_merged_injury_return",
      "object_ids": [
        "ABILITY_SHADOW_CLONE_001",
        "STATE_INJURY_001"
      ],
      "counterparty_ids": [],
      "from_state": "影身已归体",
      "to_state": "两边伤势与疲劳同时回流，顾临川短暂失去行动力",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH9_INJURY_TREATED_WITH_LIMIT",
      "slot_id": "chapter9_injury_treatment",
      "source_ref": "director.直接结果.0",
      "kind": "direct_result",
      "mode": "must_hold",
      "phase": "chapter_end",
      "actor_id": "CHAR_PARTNER_001",
      "action_id": "treat_returned_injury",
      "object_ids": [
        "STATE_INJURY_001"
      ],
      "counterparty_ids": [
        "PROTAGONIST_001"
      ],
      "from_state": "伤势未处理并影响行动",
      "to_state": "伤口得到处理，但回传伤势仍影响顾临川行动",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH9_MERGE_INJURY_COLLAPSE"
      ],
      "metadata": {}
    },
    {
      "fact_id": "CH9_PARTNER_SUBSTITUTE_BOUNDARY",
      "slot_id": "relationship_partner_shadow_cost",
      "source_ref": "director.状态变化.0",
      "kind": "relationship_transition",
      "mode": "must_hold",
      "phase": "chapter_end",
      "actor_id": "CHAR_PARTNER_001",
      "action_id": "set_shadow_cost_boundary",
      "object_ids": [
        "ABILITY_SHADOW_CLONE_001"
      ],
      "counterparty_ids": [
        "PROTAGONIST_001"
      ],
      "from_state": "对分影保持好奇",
      "to_state": "理解分影代价，并拒绝将影身视为可随意投入危险的替代品",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH9_MERGE_INJURY_COLLAPSE"
      ],
      "metadata": {}
    },
    {
      "fact_id": "CH9_MOTIVE_DUALITY_ADMITTED",
      "slot_id": "protagonist_dual_motive",
      "source_ref": "director.主角行动.0",
      "kind": "action",
      "mode": "must_hold",
      "phase": "chapter_end",
      "actor_id": "PROTAGONIST_001",
      "action_id": "admit_dual_motive",
      "object_ids": [
        "ITEM_UMBRA_WEAPON_001",
        "CHAR_PARTNER_001"
      ],
      "counterparty_ids": [
        "CHAR_PARTNER_001",
        "CHAR_RIVAL_001"
      ],
      "from_state": "",
      "to_state": "顾临川承认自己既想取得乌沉短兵，也不想让陆绾死在石城里",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH9_TWO_ROUTE_CHOICE_CONFIRMED",
      "slot_id": "public_two_route_choice",
      "source_ref": "director.对手或世界反应.1",
      "kind": "public_proof",
      "mode": "must_hold",
      "phase": "chapter_end",
      "actor_id": "CHAR_RIVAL_001",
      "action_id": "confirm_two_real_choices",
      "object_ids": [
        "PROTAGONIST_001",
        "ABILITY_SHADOW_CLONE_001"
      ],
      "counterparty_ids": [
        "PROTAGONIST_001"
      ],
      "from_state": "两条撤离线的真实选择尚未被确认",
      "to_state": "顾斜阳确认两条撤离线都包含顾临川的真实临场选择",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    },
    {
      "fact_id": "CH9_RIVAL_RECLASSIFIED",
      "slot_id": "relationship_rival_reclassification",
      "source_ref": "director.状态变化.1",
      "kind": "relationship_transition",
      "mode": "must_hold",
      "phase": "chapter_end",
      "actor_id": "CHAR_RIVAL_001",
      "action_id": "reclassify_protagonist",
      "object_ids": [
        "PROTAGONIST_001"
      ],
      "counterparty_ids": [
        "PROTAGONIST_001"
      ],
      "from_state": "保持警惕但尚未完成判断",
      "to_state": "将顾临川视为有具体欲望、却不能简单归类的竞争者",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH9_TWO_ROUTE_CHOICE_CONFIRMED",
        "CH9_MOTIVE_DUALITY_ADMITTED"
      ],
      "metadata": {}
    },
    {
      "fact_id": "CH9_ESCORT_RECORD_DUAL_ROUTE_ANOMALY",
      "slot_id": "ending_escort_record_anomaly",
      "source_ref": "director.结尾推动力.0",
      "kind": "ending",
      "mode": "terminal",
      "phase": "chapter_end",
      "actor_id": "ORG_COPPER_FEATHER_001",
      "action_id": "detect_dual_route_anomaly",
      "object_ids": [
        "RECORD_ESCORT_001"
      ],
      "counterparty_ids": [
        "PROTAGONIST_001"
      ],
      "from_state": "普通单线护卫撤离记录",
      "to_state": "记录显示两条有效行动路线，无法用普通一名二阶护卫解释",
      "value": null,
      "terminal": true,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [
        "CH9_TWO_ROUTE_CHOICE_CONFIRMED"
      ],
      "metadata": {}
    }
  ]
}
```
