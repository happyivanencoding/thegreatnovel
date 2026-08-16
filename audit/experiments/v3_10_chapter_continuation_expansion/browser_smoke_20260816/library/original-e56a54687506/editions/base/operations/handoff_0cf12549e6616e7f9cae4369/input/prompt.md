$process-novel-handoff

处理 handoff_id=handoff_0cf12549e6616e7f9cae4369。

运行 deterministic workflow start；成功后信任其 RUNNING contract。
Python 已冻结 executor_skill=bootstrap-original-novel；调用 $bootstrap-original-novel Skill，严格执行该 Skill 的 requested_stage=STORY_FOUNDATION_PROPOSAL。
业务输入只读取 task.json 指定的 business_input_files=["original_request.json", "proposal_schema.json"]。



不得修改 book；不得批准写入正史；不得批准改写 Campaign；不得启用 Edition。
完成后将 result.json 写到任务输出目标，并运行 deterministic workflow complete；需要作者决定时写 waiting_for_user.json 并进入 WAITING_FOR_USER。

## Reference Corpus Prompt Projection（REFERENCE_ONLY）

以下内容只提供可迁移的抽象创作指导；Reference Corpus 保持 REFERENCE_ONLY，不得替代作者意图、Story Foundation、Canon 或事实状态。

```json
{
  "compact_cards": [
    {
      "card_id": "contrast-ability-rule",
      "card_type": "contrast-card",
      "category_ids": [
        "科幻",
        "玄幻"
      ],
      "creative_problem_tags": [
        "ability-rule"
      ],
      "evidence_scope": "MULTI_CATEGORY",
      "knowledge_level": "CROSS_BOOK_CONTRAST",
      "maturity": "PILOT",
      "metadata_match_fields": [
        "reader_experiences",
        "narrative_drives"
      ],
      "narrative_drives": [
        "POWER_PROGRESSION",
        "WORLD_EXPLORATION",
        "MYSTERY_REVELATION"
      ],
      "payoff_channels": [
        "POWER_BREAKTHROUGH",
        "DISCOVERY",
        "STATUS_RISE",
        "WORLD_EXPANSION"
      ],
      "reader_experiences": [
        "BREAKTHROUGH",
        "POWER_VERIFICATION",
        "EXPLORATION",
        "MYSTERY",
        "STATUS_RISE"
      ],
      "shared_creative_problem": "能力规则如何被读者读懂",
      "solutions": [
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "让规则从动作实验中被推导。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "实验验证",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-ability-rule-1",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        },
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "在对抗中显示可用范围与反制空间。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "战斗边界",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-ability-rule-2",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        },
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "让能否使用能力取决于身份、场所或关系。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "社会权限",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-ability-rule-3",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        }
      ],
      "status": "REFERENCE_ONLY",
      "transfer_boundary": "Contrast 只比较同一创作问题的解法，不表示 A 好、B 差，也不要求每种解法都有 cost。"
    },
    {
      "card_id": "contrast-opening-pressure",
      "card_type": "contrast-card",
      "category_ids": [
        "科幻",
        "玄幻",
        "都市"
      ],
      "creative_problem_tags": [
        "opening"
      ],
      "evidence_scope": "MULTI_CATEGORY",
      "knowledge_level": "CROSS_BOOK_CONTRAST",
      "maturity": "PILOT",
      "metadata_match_fields": [
        "reader_experiences",
        "narrative_drives"
      ],
      "narrative_drives": [
        "POWER_PROGRESSION",
        "WORLD_EXPLORATION",
        "MYSTERY_REVELATION"
      ],
      "payoff_channels": [
        "POWER_BREAKTHROUGH",
        "DISCOVERY",
        "STATUS_RISE",
        "WORLD_EXPANSION"
      ],
      "reader_experiences": [
        "BREAKTHROUGH",
        "POWER_VERIFICATION",
        "EXPLORATION",
        "MYSTERY",
        "STATUS_RISE"
      ],
      "shared_creative_problem": "第一次强期待如何建立",
      "solutions": [
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "先给出可感知的异常能力，再补齐世界规则。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "能力先行",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-opening-pressure-1",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        },
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "先制造身份、关系或时间断裂，再延迟解释逆转。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "身份断裂",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-opening-pressure-2",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        },
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "先把职业或生活难题写到必须马上处理，再以专业结果建立回报。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "日常专业问题",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-opening-pressure-3",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        }
      ],
      "status": "REFERENCE_ONLY",
      "transfer_boundary": "Contrast 只比较同一创作问题的解法，不表示 A 好、B 差，也不要求每种解法都有 cost。"
    },
    {
      "card_id": "synth-category-01",
      "card_type": "corpus-synthesis",
      "category_ids": [
        "玄幻"
      ],
      "creative_problem_tags": [
        "category-synthesis",
        "breakthrough",
        "world-expansion"
      ],
      "distinctive_mechanisms": [
        "同一创作问题在不同作品中通过能力、身份、资源、谜团或关系解决。"
      ],
      "evidence_scope": "MULTI_BOOK",
      "failure_fatigue_risks": [
        "INFERRED_RISK：当前样本数量有限，不可推广为类别规律。"
      ],
      "knowledge_level": "CORPUS_SYNTHESIS",
      "major_divergences": [
        "有的样本偏能力/探索，有的偏身份/关系或资源经营。",
        "成本、治理和责任并非每本书的主轴。"
      ],
      "maturity": "PILOT",
      "metadata_match_fields": [
        "reader_experiences",
        "narrative_drives"
      ],
      "narrative_drives": [
        "POWER_PROGRESSION",
        "WORLD_EXPLORATION"
      ],
      "payoff_channels": [
        "POWER_BREAKTHROUGH",
        "WORLD_EXPANSION",
        "DISCOVERY"
      ],
      "payoff_differences": [
        "纯收益、力量验证、认可、发现和关系回报的比例不同。"
      ],
      "progression_differences": [
        "量变、质变、知识、身份和组合式进阶并存。"
      ],
      "reader_experiences": [
        "PROGRESSION",
        "BREAKTHROUGH",
        "WORLD_EXPANSION"
      ],
      "shared_creative_problem": "当前玄幻样本如何持续提供读者回报",
      "shared_tendencies": [
        "样本都保留可识别的阶段推进和回报窗口。",
        "世界扩大与角色目标之间存在可追踪连接。"
      ],
      "status": "REFERENCE_ONLY",
      "synthesis_kind": "CATEGORY",
      "title": "当前玄幻样本中的结构对照",
      "transfer_boundary": "只迁移对照变量和适用条件，不迁移该类别的来源身份、情节或固定模板。",
      "what_sample_cannot_tell_us": [
        "不能由当前样本判断该类别所有作品的有效公式。"
      ],
      "world_expansion_differences": [
        "地理、知识、阵营、社会层、本体层各自可能成为入口。"
      ]
    },
    {
      "card_id": "synth-category-02",
      "card_type": "corpus-synthesis",
      "category_ids": [
        "仙侠"
      ],
      "creative_problem_tags": [
        "category-synthesis",
        "breakthrough",
        "world-expansion"
      ],
      "distinctive_mechanisms": [
        "同一创作问题在不同作品中通过能力、身份、资源、谜团或关系解决。"
      ],
      "evidence_scope": "MULTI_BOOK",
      "failure_fatigue_risks": [
        "INFERRED_RISK：当前样本数量有限，不可推广为类别规律。"
      ],
      "knowledge_level": "CORPUS_SYNTHESIS",
      "major_divergences": [
        "有的样本偏能力/探索，有的偏身份/关系或资源经营。",
        "成本、治理和责任并非每本书的主轴。"
      ],
      "maturity": "PILOT",
      "metadata_match_fields": [
        "reader_experiences",
        "narrative_drives"
      ],
      "narrative_drives": [
        "POWER_PROGRESSION",
        "WORLD_EXPLORATION"
      ],
      "payoff_channels": [
        "POWER_BREAKTHROUGH",
        "WORLD_EXPANSION",
        "DISCOVERY"
      ],
      "payoff_differences": [
        "纯收益、力量验证、认可、发现和关系回报的比例不同。"
      ],
      "progression_differences": [
        "量变、质变、知识、身份和组合式进阶并存。"
      ],
      "reader_experiences": [
        "PROGRESSION",
        "BREAKTHROUGH",
        "WORLD_EXPANSION"
      ],
      "shared_creative_problem": "当前仙侠样本如何持续提供读者回报",
      "shared_tendencies": [
        "样本都保留可识别的阶段推进和回报窗口。",
        "世界扩大与角色目标之间存在可追踪连接。"
      ],
      "status": "REFERENCE_ONLY",
      "synthesis_kind": "CATEGORY",
      "title": "当前仙侠样本中的结构对照",
      "transfer_boundary": "只迁移对照变量和适用条件，不迁移该类别的来源身份、情节或固定模板。",
      "what_sample_cannot_tell_us": [
        "不能由当前样本判断该类别所有作品的有效公式。"
      ],
      "world_expansion_differences": [
        "地理、知识、阵营、社会层、本体层各自可能成为入口。"
      ]
    },
    {
      "card_id": "synth-category-03",
      "card_type": "corpus-synthesis",
      "category_ids": [
        "都市"
      ],
      "creative_problem_tags": [
        "category-synthesis",
        "breakthrough",
        "world-expansion"
      ],
      "distinctive_mechanisms": [
        "同一创作问题在不同作品中通过能力、身份、资源、谜团或关系解决。"
      ],
      "evidence_scope": "MULTI_BOOK",
      "failure_fatigue_risks": [
        "INFERRED_RISK：当前样本数量有限，不可推广为类别规律。"
      ],
      "knowledge_level": "CORPUS_SYNTHESIS",
      "major_divergences": [
        "有的样本偏能力/探索，有的偏身份/关系或资源经营。",
        "成本、治理和责任并非每本书的主轴。"
      ],
      "maturity": "PILOT",
      "metadata_match_fields": [
        "reader_experiences",
        "narrative_drives"
      ],
      "narrative_drives": [
        "POWER_PROGRESSION",
        "WORLD_EXPLORATION"
      ],
      "payoff_channels": [
        "POWER_BREAKTHROUGH",
        "WORLD_EXPANSION",
        "DISCOVERY"
      ],
      "payoff_differences": [
        "纯收益、力量验证、认可、发现和关系回报的比例不同。"
      ],
      "progression_differences": [
        "量变、质变、知识、身份和组合式进阶并存。"
      ],
      "reader_experiences": [
        "PROGRESSION",
        "BREAKTHROUGH",
        "WORLD_EXPANSION"
      ],
      "shared_creative_problem": "当前都市样本如何持续提供读者回报",
      "shared_tendencies": [
        "样本都保留可识别的阶段推进和回报窗口。",
        "世界扩大与角色目标之间存在可追踪连接。"
      ],
      "status": "REFERENCE_ONLY",
      "synthesis_kind": "CATEGORY",
      "title": "当前都市样本中的结构对照",
      "transfer_boundary": "只迁移对照变量和适用条件，不迁移该类别的来源身份、情节或固定模板。",
      "what_sample_cannot_tell_us": [
        "不能由当前样本判断该类别所有作品的有效公式。"
      ],
      "world_expansion_differences": [
        "地理、知识、阵营、社会层、本体层各自可能成为入口。"
      ]
    },
    {
      "card_id": "synth-category-04",
      "card_type": "corpus-synthesis",
      "category_ids": [
        "科幻"
      ],
      "creative_problem_tags": [
        "category-synthesis",
        "breakthrough",
        "world-expansion"
      ],
      "distinctive_mechanisms": [
        "同一创作问题在不同作品中通过能力、身份、资源、谜团或关系解决。"
      ],
      "evidence_scope": "MULTI_BOOK",
      "failure_fatigue_risks": [
        "INFERRED_RISK：当前样本数量有限，不可推广为类别规律。"
      ],
      "knowledge_level": "CORPUS_SYNTHESIS",
      "major_divergences": [
        "有的样本偏能力/探索，有的偏身份/关系或资源经营。",
        "成本、治理和责任并非每本书的主轴。"
      ],
      "maturity": "PILOT",
      "metadata_match_fields": [
        "reader_experiences",
        "narrative_drives"
      ],
      "narrative_drives": [
        "POWER_PROGRESSION",
        "WORLD_EXPLORATION"
      ],
      "payoff_channels": [
        "POWER_BREAKTHROUGH",
        "WORLD_EXPANSION",
        "DISCOVERY"
      ],
      "payoff_differences": [
        "纯收益、力量验证、认可、发现和关系回报的比例不同。"
      ],
      "progression_differences": [
        "量变、质变、知识、身份和组合式进阶并存。"
      ],
      "reader_experiences": [
        "PROGRESSION",
        "BREAKTHROUGH",
        "WORLD_EXPANSION"
      ],
      "shared_creative_problem": "当前科幻样本如何持续提供读者回报",
      "shared_tendencies": [
        "样本都保留可识别的阶段推进和回报窗口。",
        "世界扩大与角色目标之间存在可追踪连接。"
      ],
      "status": "REFERENCE_ONLY",
      "synthesis_kind": "CATEGORY",
      "title": "当前科幻样本中的结构对照",
      "transfer_boundary": "只迁移对照变量和适用条件，不迁移该类别的来源身份、情节或固定模板。",
      "what_sample_cannot_tell_us": [
        "不能由当前样本判断该类别所有作品的有效公式。"
      ],
      "world_expansion_differences": [
        "地理、知识、阵营、社会层、本体层各自可能成为入口。"
      ]
    }
  ],
  "effective_query": {
    "creative_problem": "STORY_FOUNDATION_PROPOSAL：围绕作者 premise 与已确认阅读体验寻找可迁移的故事机制，只作为 Core/Foundation/Candidate 的参考候选。",
    "creative_problem_tags": [],
    "max_cards": 6,
    "narrative_drives": [
      "SURVIVAL_RESOURCE",
      "KNOWLEDGE_PROGRESSION",
      "ABILITY_PROGRESSION",
      "MYSTERY_INVESTIGATION",
      "WORLD_EXPLORATION"
    ],
    "payoff_channels": [],
    "reader_experiences": [
      "ARTIFACT_OR_ABILITY",
      "BREAKTHROUGH",
      "COMBAT",
      "EXPLORATION",
      "FACTION_CONFLICT",
      "KNOWLEDGE",
      "MYSTERY",
      "POWER_VERIFICATION",
      "PROGRESSION",
      "RELATIONSHIP",
      "RESOURCE_OPPORTUNITY",
      "REVEAL",
      "REVENGE",
      "ROMANCE",
      "SOCIAL_THEME",
      "STATUS_RISE",
      "SURVIVAL",
      "TEAM_GROWTH",
      "WEALTH",
      "WORLD_EXPANSION"
    ],
    "scene_functions": []
  },
  "knowledge_gaps": [],
  "machine_bundle_hash": "3120e088142f5d75ad3f2d1d18eca36f5b89251369228b4f73c7f63e796ff9f9",
  "match_tier": "EXACT",
  "original_query": {
    "creative_problem": "STORY_FOUNDATION_PROPOSAL：围绕作者 premise 与已确认阅读体验寻找可迁移的故事机制，只作为 Core/Foundation/Candidate 的参考候选。",
    "creative_problem_tags": [],
    "max_cards": 6,
    "narrative_drives": [
      "SURVIVAL_RESOURCE",
      "KNOWLEDGE_PROGRESSION",
      "ABILITY_PROGRESSION",
      "MYSTERY_INVESTIGATION",
      "WORLD_EXPLORATION"
    ],
    "payoff_channels": [],
    "reader_experiences": [
      "ARTIFACT_OR_ABILITY",
      "BREAKTHROUGH",
      "COMBAT",
      "EXPLORATION",
      "FACTION_CONFLICT",
      "KNOWLEDGE",
      "MYSTERY",
      "POWER_VERIFICATION",
      "PROGRESSION",
      "RELATIONSHIP",
      "RESOURCE_OPPORTUNITY",
      "REVEAL",
      "REVENGE",
      "ROMANCE",
      "SOCIAL_THEME",
      "STATUS_RISE",
      "SURVIVAL",
      "TEAM_GROWTH",
      "WEALTH",
      "WORLD_EXPANSION"
    ],
    "scene_functions": []
  },
  "purpose": "PLANNING",
  "relaxed_fields": [],
  "selected_card_count": 6,
  "selected_card_ids": [
    "contrast-ability-rule",
    "contrast-opening-pressure",
    "synth-category-01",
    "synth-category-02",
    "synth-category-03",
    "synth-category-04"
  ],
  "selected_card_knowledge_levels": [
    "CROSS_BOOK_CONTRAST",
    "CROSS_BOOK_CONTRAST",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS"
  ],
  "selected_card_types": [
    "contrast-card",
    "contrast-card",
    "corpus-synthesis",
    "corpus-synthesis",
    "corpus-synthesis",
    "corpus-synthesis"
  ],
  "snapshot_hash": "8d12809ea874f4f9e7baacd0d937cd6330f2c2b2780a8bf68255042ea8001efa",
  "snapshot_id": "reference-context_9d3153b9f283ee0997eb40c6",
  "status": "ENABLED",
  "usage": "REFERENCE_ONLY",
  "warnings": [],
  "zero_result_reason": null
}
```
