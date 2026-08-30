触发事件：百炉会开炉试正式开始。唐绾完成铸潮展示，顾停舟在公开试场中让修复后的回潮楔只完成一次真实改向；阮青蜃与少东家分别提出不同条件，逼他当场选择回潮楔和矿路的归属方式。

推动事件的人：唐绾推动开炉展示；阮青蜃提出高价买断并减免部分契约追索；少东家提出独立粮路合作。三方条件共同迫使顾停舟作出选择。

主角行动：顾停舟让回潮楔完成一次锁潮、改向、释放，不追加第二次硬压；在懂行者确认其价值后，拒绝阮青蜃买断回潮楔，接受少东家的独立粮路合作，保留回潮楔的自主使用权。

对手或世界反应：现场比较确认，普通成炉者只能在自身附近稳定重压，回潮楔却能改变一整段潮势方向，顾停舟因此被重新定价。阮青蜃的买断与追索方案被拒，少东家则以固定报酬和明确损失边界建立合作条件。

直接结果：回潮楔没有被出售，首批矿脉的独家标记不再被承认为阮青蜃的完整矿权；顾停舟取得一份公开确认的个人矿利份额，砺骨部水路不被矿权吞并，并确定接受少东家的粮路合作。

状态变化：顾停舟从“保住手中东西”进入主动选择财富与自由路径的阶段；他与少东家从主从关系变为有价合作关系，与阮青蜃形成公开的利益竞争。回潮楔完成一次改向后仍须散尽残压，不能立即连续硬压。

叙事功能：完成古器、矿脉与旧关系的第一次公共重估；兑现回潮楔的独有生活价值与公共议价价值，同时把顾停舟的身份从被追索者推进为拥有公开矿利、能够自主选择合作对象的独立承揽人。

结尾推动力：少东家合作的第一批粮路货必须在下一次十二日地潮前送到旧关，时间窗口已经确定。顾停舟随队出发，下一章必须处理这次运输及其现实风险，但本章不提前结算送达结果。

## 专项建议

Opening：不启用；炉钟、试场和三方报价已经提供直接入口，无需另设铺垫。

Dialogue：启用；买断、拒绝与独立合作是本章核心选择，谈判条件必须具体落地。

## AAIR1

```json
{
  "v": "AAIR1",
  "chapter": "JIUCHUI:CH014",
  "protagonist": "PROTAGONIST_001",
  "actions": [
    {
      "slot": "event:JIUCHUI:CH014:single_redirect",
      "actor": "PROTAGONIST_001",
      "verb": "use_once",
      "objects": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparties": ["ORG_HUNDRED_FURNACE_001"]
    },
    {
      "slot": "event:JIUCHUI:CH014:refuse_buyout",
      "actor": "PROTAGONIST_001",
      "verb": "refuse_buyout",
      "objects": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparties": ["CHAR_RIVAL_001"]
    },
    {
      "slot": "event:JIUCHUI:CH014:choose_grain_cooperation",
      "actor": "PROTAGONIST_001",
      "verb": "accept_cooperation",
      "objects": ["ROUTE_GRAIN_001"],
      "counterparties": ["CHAR_PARTNER_001"]
    }
  ],
  "results": [
    {
      "slot": "result:JIUCHUI:CH014:public_repricing",
      "kind": "public_proof",
      "actor": "PROTAGONIST_001",
      "verb": "secure_public_repricing",
      "objects": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparties": ["ORG_HUNDRED_FURNACE_001", "CHAR_RIVAL_001"],
      "from": "回潮楔价值未完成公共确认",
      "to": "回潮楔能改变一整段潮势方向并使顾停舟被重新定价",
      "value": null,
      "terminal": true,
      "depends": ["event:JIUCHUI:CH014:single_redirect"],
      "meta": {}
    },
    {
      "slot": "ownership:RESOURCE_PERSONAL_MINING_SHARE_001",
      "kind": "ownership_transition",
      "actor": "PROTAGONIST_001",
      "verb": "acquire",
      "objects": ["RESOURCE_PERSONAL_MINING_SHARE_001"],
      "counterparties": ["CHAR_RIVAL_001"],
      "from": "",
      "to": "公开确认的个人矿利份额",
      "value": null,
      "terminal": true,
      "depends": ["result:JIUCHUI:CH014:public_repricing"],
      "meta": {}
    },
    {
      "slot": "result:JIUCHUI:CH014:mine_rights_repriced",
      "kind": "direct_result",
      "actor": "PROTAGONIST_001",
      "verb": "secure",
      "objects": ["RESOURCE_PERSONAL_MINING_SHARE_001"],
      "counterparties": ["CHAR_RIVAL_001"],
      "from": "阮青蜃主张完整矿权",
      "to": "独家标记不再被承认为阮青蜃的完整矿权，砺骨部水路不被吞并",
      "value": null,
      "terminal": true,
      "depends": ["ownership:RESOURCE_PERSONAL_MINING_SHARE_001"],
      "meta": {}
    },
    {
      "slot": "result:JIUCHUI:CH014:independent_grain_cooperation",
      "kind": "direct_result",
      "actor": "PROTAGONIST_001",
      "verb": "accept",
      "objects": ["ROUTE_GRAIN_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "主从关系",
      "to": "有价独立合作关系",
      "value": null,
      "terminal": true,
      "depends": ["event:JIUCHUI:CH014:choose_grain_cooperation"],
      "meta": {}
    }
  ],
  "states": [
    {
      "slot": "relationship:PROTAGONIST_001:CHAR_PARTNER_001",
      "kind": "relationship_transition",
      "actor": "PROTAGONIST_001",
      "verb": "establish",
      "objects": ["ROUTE_GRAIN_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "雇主与被雇者",
      "to": "有价独立合作",
      "value": null,
      "terminal": true,
      "depends": ["result:JIUCHUI:CH014:independent_grain_cooperation"],
      "meta": {}
    },
    {
      "slot": "relationship:PROTAGONIST_001:CHAR_RIVAL_001",
      "kind": "relationship_transition",
      "actor": "PROTAGONIST_001",
      "verb": "oppose",
      "objects": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparties": ["CHAR_RIVAL_001"],
      "from": "公开追索",
      "to": "买断被拒后的公开利益竞争",
      "value": null,
      "terminal": true,
      "depends": ["event:JIUCHUI:CH014:refuse_buyout"],
      "meta": {}
    }
  ],
  "ending": [
    {
      "slot": "ending:JIUCHUI:CH014:grain_departure",
      "kind": "deadline",
      "actor": "PROTAGONIST_001",
      "verb": "depart_with",
      "objects": ["ROUTE_GRAIN_001", "LOCATION_OLD_PASS", "EVENT_NEXT_TIDE_001"],
      "counterparties": ["CHAR_PARTNER_001"],
      "from": "",
      "to": "随队出发，须在下一次十二日地潮前送到旧关",
      "value": null,
      "terminal": true,
      "depends": ["result:JIUCHUI:CH014:independent_grain_cooperation"],
      "meta": {}
    }
  ],
  "boundaries": [
    {
      "slot": "ability:ITEM_RETURN_TIDE_WEDGE_001:single_redirect",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "actor": "PROTAGONIST_001",
      "verb": "respect_limit",
      "objects": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparties": [],
      "from": "完成一次锁潮、改向、释放",
      "to": "使用后须散尽残压，不得立即连续硬压",
      "value": null,
      "depends": ["event:JIUCHUI:CH014:single_redirect"],
      "meta": {}
    },
    {
      "slot": "ability:ITEM_RETURN_TIDE_WEDGE_001:autonomous_use",
      "kind": "ability_boundary",
      "mode": "must_hold",
      "actor": "PROTAGONIST_001",
      "verb": "retain_autonomy",
      "objects": ["ITEM_RETURN_TIDE_WEDGE_001"],
      "counterparties": ["CHAR_RIVAL_001"],
      "from": "阮青蜃提出买断",
      "to": "顾停舟拒绝出售并自行决定用途",
      "value": null,
      "depends": ["event:JIUCHUI:CH014:refuse_buyout"],
      "meta": {}
    }
  ]
}
```
