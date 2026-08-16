# PLAN_ONLY 三候选任务 `plan_0aa91dd5699d47b90ec5353e`

正式 handoff：`handoff_977f8ed820e82fa86b95fa24`。先读取 handoff input 下全部冻结文件。
目标生成三个 Candidate，至少生成两个有效 Candidate；不生成正文、Chapter Contract 或 Canon Event。
候选 lens 可覆盖 CONTINUITY_ACTIVE_THREAD、EARNED_OPPORTUNITY、FORWARD_EXPANSION；结构多样性是诊断与排序信号，不是整批硬失败。
只填写创意决定。author control、画像、评分、证据和门禁由 Python 根据冻结输入编译。
所有事实必须来自 world_state_context.json 或 handoff 冻结证据；未来新增只能作为 CANDIDATE，并填写 novelty provenance。
不得引用任何未出现在 Author Goal、World State、Resource、Relationship、Knowledge Boundary、Active Threads 或 Kernel Context 中的人物、物品、能力或专名。
当前 provenance-aware 指标若为 INCOMPLETE，必须保留缺失，不得伪造分数或证据。

## 本次作者目标

（未提供）

## 冻结 Author Control

{
  "intents": [
    {
      "description": "在事实支持后判断变化建筑是否存在互联关系；逐步扩大物品进化能处理的空间尺度，同时保持原功能连续性；让楼外天气、全球灾变和其他幸存者规则保持多个候选解释，直到行动证据要求收敛",
      "horizon": "LONG",
      "intent_id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-long",
      "intent_type": "ROLLING_PLANNING",
      "payload": {
        "fixed_chapter_outline": false,
        "items": [
          "在事实支持后判断变化建筑是否存在互联关系",
          "逐步扩大物品进化能处理的空间尺度，同时保持原功能连续性",
          "让楼外天气、全球灾变和其他幸存者规则保持多个候选解释，直到行动证据要求收敛"
        ],
        "route_id": "route-space-reading"
      },
      "priority": 100,
      "status": "PLANNED",
      "subject_id": "foundation-folded-tower",
      "subject_type": "STORY_FOUNDATION",
      "target_chapter_id": null,
      "title": "长期可能性"
    },
    {
      "description": "比较测距带、照明物和标记物在不同楼层状态中的异常边界；在不建立稳定聚落的前提下交换一次路线与资源观测；追查广播是否会在建筑变化前后留下可验证的空间偏差",
      "horizon": "MID",
      "intent_id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-mid",
      "intent_type": "ROLLING_PLANNING",
      "payload": {
        "fixed_chapter_outline": false,
        "items": [
          "比较测距带、照明物和标记物在不同楼层状态中的异常边界",
          "在不建立稳定聚落的前提下交换一次路线与资源观测",
          "追查广播是否会在建筑变化前后留下可验证的空间偏差"
        ],
        "route_id": "route-space-reading"
      },
      "priority": 100,
      "status": "PLANNED",
      "subject_id": "foundation-folded-tower",
      "subject_type": "STORY_FOUNDATION",
      "target_chapter_id": null,
      "title": "中期方向"
    },
    {
      "description": "记录第一次提前重排的墙面、楼梯和广播位置；从手边物品中选择一次能验证断路关系的进化；取回饮水并保留一份能在重排后复核的现场证据",
      "horizon": "SHORT",
      "intent_id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-short",
      "intent_type": "ROLLING_PLANNING",
      "payload": {
        "fixed_chapter_outline": false,
        "items": [
          "记录第一次提前重排的墙面、楼梯和广播位置",
          "从手边物品中选择一次能验证断路关系的进化",
          "取回饮水并保留一份能在重排后复核的现场证据"
        ],
        "route_id": "route-space-reading"
      },
      "priority": 100,
      "status": "PLANNED",
      "subject_id": "foundation-folded-tower",
      "subject_type": "STORY_FOUNDATION",
      "target_chapter_id": null,
      "title": "近期方向"
    }
  ],
  "rule": "候选必须读取作者任务/意图；命中只作为可追溯规划输入，不改变评分硬门。",
  "target_hits": {
    "intent_count": 3,
    "intent_ids": [
      "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-long",
      "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-mid",
      "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-short"
    ],
    "priority_order": "priority asc, horizon, updated_at desc",
    "targets": [
      {
        "id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-long",
        "kind": "AUTHOR_INTENT",
        "title": "长期可能性"
      },
      {
        "id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-mid",
        "kind": "AUTHOR_INTENT",
        "title": "中期方向"
      },
      {
        "id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-short",
        "kind": "AUTHOR_INTENT",
        "title": "近期方向"
      }
    ],
    "task_count": 0,
    "task_ids": []
  },
  "tasks": [],
  "trace_contract": {
    "hard_gates_win": true,
    "required": [
      "author_task_hits",
      "author_intent_hits",
      "author_tasks_advanced",
      "author_intents_advanced",
      "author_goals_not_used",
      "unused_reasons"
    ]
  }
}

## Effective Global Book Profile

{
  "active_directives": [],
  "dimensions": [
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "末日废弃建筑不是静态背景，而是会把路线、资源和谜团重新排列的可行动世界。",
      "dimension": "worldbuilding",
      "draft": {
        "core_commitments": [
          "建筑变化必须持续制造可验证的生存问题",
          "异常尺度只围绕每日物品进化扩大"
        ],
        "open_questions": [
          "建筑变化的原因与其他使用者范围"
        ],
        "preferences": [
          "以具体空间关系承载中等神秘度",
          "世界扩张保持开放"
        ],
        "risks": [
          "规则说明压过现场行动",
          "世界规模扩张过快"
        ],
        "summary": "末日废弃建筑不是静态背景，而是会把路线、资源和谜团重新排列的可行动世界。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "worldbuilding.md",
      "label": "世界观",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "人物首先通过私人目标和选择行动，社会关系保持低中心度但能制造证据与资源压力。",
      "dimension": "characters",
      "draft": {
        "core_commitments": [
          "沈砚想掌握离开之路而非先经营组织",
          "人物弱点必须在验证与行动的迟疑中产生后果"
        ],
        "open_questions": [
          "广播声音和幸存者的真实动机"
        ],
        "preferences": [
          "角色以现场动作区分",
          "关系以局部交换和互相矛盾观测进入"
        ],
        "risks": [
          "把角色写成能力的说明工具",
          "群像抢走主角的唯一选择"
        ],
        "summary": "人物首先通过私人目标和选择行动，社会关系保持低中心度但能制造证据与资源压力。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "characters.md",
      "label": "人物",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "情节由建筑压力、当天选择、现场验证和新瓶颈连续推动，不冻结逐章大纲。",
      "dimension": "plot",
      "draft": {
        "core_commitments": [
          "每次兑现都改变可行动范围",
          "新问题在当前后果之后出现"
        ],
        "open_questions": [
          "路线之间何时发生交叉"
        ],
        "preferences": [
          "短期行动具体，长期谜团留有弹性"
        ],
        "risks": [
          "重复找路",
          "靠巧合解释资源和广播"
        ],
        "summary": "情节由建筑压力、当天选择、现场验证和新瓶颈连续推动，不冻结逐章大纲。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "plot.md",
      "label": "剧情",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "语言紧张、具体、克制，优先写触感、距离、声音、光线和行动结果。",
      "dimension": "style",
      "draft": {
        "core_commitments": [
          "第三人称限知",
          "异常结果先被看见再被理解"
        ],
        "open_questions": [
          "更高尺度的异常如何保持可读"
        ],
        "preferences": [
          "保留爽点但避免夸张说明",
          "让物品原功能可识别"
        ],
        "risks": [
          "说明书化",
          "抽象名词替代现场"
        ],
        "summary": "语言紧张、具体、克制，优先写触感、距离、声音、光线和行动结果。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "style.md",
      "label": "文风",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "核心叙事节奏是压力逼近、唯一选择、异常验证、纯收益兑现和更大问题。",
      "dimension": "narrative",
      "draft": {
        "core_commitments": [
          "生存资源保持第一驱动力",
          "知识与谜团必须回到下一次选择"
        ],
        "open_questions": [
          "不同阶段的回报密度"
        ],
        "preferences": [
          "可以用广播和回声延迟信息",
          "不预设固定回合长度"
        ],
        "risks": [
          "悬念长期不改变行动",
          "战斗变成主线"
        ],
        "summary": "核心叙事节奏是压力逼近、唯一选择、异常验证、纯收益兑现和更大问题。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "narrative.md",
      "label": "叙事",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "对话主要交换路线、资源和可信度，不承担大段世界设定讲解。",
      "dimension": "dialogue",
      "draft": {
        "core_commitments": [
          "广播提示必须与现场后果形成张力",
          "幸存者说法保留局部立场"
        ],
        "open_questions": [
          "广播是否由单一声音持续发出"
        ],
        "preferences": [
          "短句、具体指令和可核验细节"
        ],
        "risks": [
          "角色用台词直接公布真相",
          "关系戏脱离生存压力"
        ],
        "summary": "对话主要交换路线、资源和可信度，不承担大段世界设定讲解。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "dialogue.md",
      "label": "对话",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "每轮保持可感知的选择与结果，但兑现之后允许新的压力自然打开。",
      "dimension": "pacing",
      "draft": {
        "core_commitments": [
          "不把每日选择机械映射为固定章节模板",
          "能力验证要有实际后果"
        ],
        "open_questions": [
          "建筑变化的周期和不规则性"
        ],
        "preferences": [
          "在重排前压缩时间，在验证后给结果留出重量"
        ],
        "risks": [
          "每次都强行加伤亡或牺牲",
          "只有赶路没有回报"
        ],
        "summary": "每轮保持可感知的选择与结果，但兑现之后允许新的压力自然打开。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "pacing.md",
      "label": "节奏",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "主题只在具体选择中显现：有限资源如何改变人的判断，以及可复核的知识是否足以支撑行动。",
      "dimension": "themes",
      "draft": {
        "core_commitments": [
          "不把主题凌驾于生存和进化",
          "让选择后果自然形成主题"
        ],
        "open_questions": [
          "广播和其他幸存者是否形成更广的社会主题"
        ],
        "preferences": [
          "克制处理责任与信任"
        ],
        "risks": [
          "说教",
          "用宏大主题替代能力兑现"
        ],
        "summary": "主题只在具体选择中显现：有限资源如何改变人的判断，以及可复核的知识是否足以支撑行动。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "themes.md",
      "label": "主题 / 价值观",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    },
    {
      "author_edit_count": 0,
      "author_edits": [],
      "available": true,
      "content": "连续性依靠物品拥有关系、进化边界、建筑状态、路线证据和知识不确定性维持。",
      "dimension": "continuity",
      "draft": {
        "core_commitments": [
          "每次物品进化保留原功能与已验证边界",
          "局部样本不能自动升级为全局规则"
        ],
        "open_questions": [
          "连续进化如何累积",
          "建筑重排是否存在周期"
        ],
        "preferences": [
          "使用可追溯的现场记录",
          "允许已知与未知并存"
        ],
        "risks": [
          "忘记物品位置或能力边界",
          "把候选真相写成 Canon"
        ],
        "summary": "连续性依靠物品拥有关系、进化边界、建筑状态、路线证据和知识不确定性维持。"
      },
      "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
      "filename": "continuity.md",
      "label": "连续性",
      "source": "ORIGINAL_FOUNDATION_PROPOSAL"
    }
  ],
  "hard_constraints": {
    "must": [],
    "must_not": []
  },
  "profile_version_id": "book-profile-proposal-e39fee0d664e4e06923df0f31beee8eb",
  "version_number": 1
}

## Active Author Truth + 本章揭露计划

{
  "active_author_truths": [
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "沈砚，灾变前为城市旧楼做测绘和安全复核的自由接单人；他擅长记住墙体、回声、风向与转折关系，却没有强悍体力，也不擅长在不完整证据下相信别人。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "主角",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-1",
      "truth_type": "CHARACTER_IDENTITY",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "全球灾变后，幸存者被困在各自的废弃建筑中，建筑结构会周期性改变，旧路线和门后空间不能默认保持不变。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-10",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "主角每天只能从自己真正拥有并能接触到的普通非生命物品中选择一件，使它沿原有功能发生一次永久进化；同一物品可以继续进化。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-11",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "物品进化必须保留可辨认的原功能，并在具体行动中显示超出普通人能力范围的结果；不能用普通工程、职业知识或一般效率解释替代。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-12",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "一次选择不能同时进化多件物品，也不能远程选择不在主角手边的对象；错配会留下真实的机会与时间压力。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-13",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "建筑变化造成的空间、路线和资源后果必须能被第三人称限知视角观察和复核；建筑成因、广播来源和其他幸存者规则暂保持候选状态。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-14",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "每一次有效兑现先改变主角当下能做什么，再把更大的空间、资源或规则问题交给下一轮选择，不用同场景的维护或牺牲把收益抵消为无效。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-15",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "沈砚：主角，旧楼测绘与安全复核接单人；以空间记录为 supporting competence，特殊优势仍来自每日物品进化。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "CHARACTER",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-16",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "广播中的声音：持续提供互相矛盾的楼层提示，既可能是幸存者留下的路线，也可能正在利用建筑变化诱导行动；身份保持候选。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "CHARACTER",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-17",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "门后幸存者：在不同重排状态下留下水位、粉笔线、收音机和反向楼层编号，为沈砚提供局部观测，也可能争夺同一条安全路线。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "CHARACTER",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-18",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "楼外天气的目击者候选：只在沈砚进入更高空间后以可验证的物理痕迹进入故事，不预先确定其身份或可信度。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "CHARACTER",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-19",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "主角目标",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-2",
      "truth_type": "CHARACTER_GOAL",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "塔内临时幸存者小群体：围绕水、照明和安全层交换局部信息，规模与立场随事实发展。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "FACTION",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-20",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "广播维护者或信号来源：作为待辨认的压力节点，不预设为万能幕后组织。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "FACTION",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-21",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "其他变化建筑中的幸存者网络：在世界扩张后才由真实路线和资源交换形成，不提前固定政治结构。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "FACTION",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-22",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "主冲突",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-3",
      "truth_type": "PLOT_TRUTH",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "体力、饮水、照明和当日唯一进化机会会随位置与判断被消耗；这些是选择的现实后果，不预设每次能力兑现都必须牺牲某种叙事价值。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "主角代价",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-4",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "从只相信完整地图和充分证据的测绘者，成长为能在局部证据下作出唯一选择、让异常物品先打开行动可能，再用行动补足知识的人；他的上限表现为能处理更大、更不稳定的空间关系，而不是只拥有更多物资。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "主角成长空间",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-5",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "在下一次大幅重排前，用一次物品进化确认一条可返回的空间关系，取回饮水，并带走能复核路线的现场记录。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "第一阶段目标",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-6",
      "truth_type": "FUTURE_EVENT_PRECONDITION",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "主要故事承载是一座会把住宅层、商场中庭、地下设备层和封闭屋顶重新拼接的高层综合楼。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "WORLD_CARRIER",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-7",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "每日唯一的物品进化是主角反复改变行动可能的第一发动机，不建立脱离它的第二成长系统。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "SIGNATURE_RULE",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-8",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    },
    {
      "author_layer": "AUTHOR_TRUTH",
      "book_id": "original-e56a54687506",
      "compatibility_status": "COMPATIBLE_WITH_GAPS",
      "compatibility_summary": "原创项目从第一章起生效",
      "confidence": 1.0,
      "created_at": "2026-08-16T16:22:26.798563+00:00",
      "description": "",
      "edition_id": "base",
      "effective_from_chapter": 1,
      "effective_until_chapter": null,
      "introduced_by": "AUTHOR_CONFIRMED",
      "metadata": {
        "foundation_candidate_id": "foundation-folded-tower",
        "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
      },
      "must_remain_true": true,
      "object_id": null,
      "object_type": null,
      "requires_revision": false,
      "retroactive_scope": "FORWARD_ONLY",
      "statement": "使用第三人称限知，让物品结果、空间错位和广播可信度都通过主角能观察到的后果逐步确认。",
      "status": "ACTIVE_TRUTH",
      "subject_id": null,
      "subject_type": "STORY_FOUNDATION",
      "tags": [
        "ORIGINAL_GENESIS"
      ],
      "title": "NARRATIVE_FORM",
      "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-9",
      "truth_type": "CUSTOM",
      "updated_at": "2026-08-16T16:22:26.798563+00:00",
      "version": 1
    }
  ],
  "behavioral_rule": "Active Author Truth 可约束人物选择、资源部署与势力行动；只有 Reveal Agenda 授权的深度可以进入读者可见正文。KEEP_HIDDEN 不得直接说明答案。",
  "candidate_contract": {
    "hint_must_not_confirm_identity": true,
    "hint_requires_readable_clue": true,
    "keep_hidden_is_hard_boundary": true,
    "required_fields": [
      "truth_alignment",
      "reveal_impact"
    ]
  },
  "reveal_agenda": {
    "book_id": "original-e56a54687506",
    "chapter_ordinal": 5,
    "counts": {
      "keep_hidden": 22,
      "must_reveal": 0,
      "optional": 0,
      "should_hint": 0
    },
    "debt_integration": {
      "engine": "Narrative Debt / Promise",
      "secret_obligations": [],
      "separate_reveal_debt_engine": false
    },
    "edition_id": "base",
    "keep_hidden": [
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "沈砚：主角，旧楼测绘与安全复核接单人；以空间记录为 supporting competence，特殊优势仍来自每日物品进化。",
        "target_character_state": "UNKNOWN",
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-16",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "广播中的声音：持续提供互相矛盾的楼层提示，既可能是幸存者留下的路线，也可能正在利用建筑变化诱导行动；身份保持候选。",
        "target_character_state": "UNKNOWN",
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-17",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "门后幸存者：在不同重排状态下留下水位、粉笔线、收音机和反向楼层编号，为沈砚提供局部观测，也可能争夺同一条安全路线。",
        "target_character_state": "UNKNOWN",
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-18",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "楼外天气的目击者候选：只在沈砚进入更高空间后以可验证的物理痕迹进入故事，不预先确定其身份或可信度。",
        "target_character_state": "UNKNOWN",
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-19",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "塔内临时幸存者小群体：围绕水、照明和安全层交换局部信息，规模与立场随事实发展。",
        "target_character_state": "UNKNOWN",
        "title": "FACTION",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-20",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "广播维护者或信号来源：作为待辨认的压力节点，不预设为万能幕后组织。",
        "target_character_state": "UNKNOWN",
        "title": "FACTION",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-21",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "其他变化建筑中的幸存者网络：在世界扩张后才由真实路线和资源交换形成，不提前固定政治结构。",
        "target_character_state": "UNKNOWN",
        "title": "FACTION",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-22",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "使用第三人称限知，让物品结果、空间错位和广播可信度都通过主角能观察到的后果逐步确认。",
        "target_character_state": "UNKNOWN",
        "title": "NARRATIVE_FORM",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-9",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "每日唯一的物品进化是主角反复改变行动可能的第一发动机，不建立脱离它的第二成长系统。",
        "target_character_state": "UNKNOWN",
        "title": "SIGNATURE_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-8",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "主要故事承载是一座会把住宅层、商场中庭、地下设备层和封闭屋顶重新拼接的高层综合楼。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_CARRIER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-7",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "全球灾变后，幸存者被困在各自的废弃建筑中，建筑结构会周期性改变，旧路线和门后空间不能默认保持不变。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-10",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "主角每天只能从自己真正拥有并能接触到的普通非生命物品中选择一件，使它沿原有功能发生一次永久进化；同一物品可以继续进化。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-11",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "物品进化必须保留可辨认的原功能，并在具体行动中显示超出普通人能力范围的结果；不能用普通工程、职业知识或一般效率解释替代。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-12",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "一次选择不能同时进化多件物品，也不能远程选择不在主角手边的对象；错配会留下真实的机会与时间压力。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-13",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "建筑变化造成的空间、路线和资源后果必须能被第三人称限知视角观察和复核；建筑成因、广播来源和其他幸存者规则暂保持候选状态。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-14",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "每一次有效兑现先改变主角当下能做什么，再把更大的空间、资源或规则问题交给下一轮选择，不用同场景的维护或牺牲把收益抵消为无效。",
        "target_character_state": "UNKNOWN",
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-15",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
        "target_character_state": "UNKNOWN",
        "title": "主冲突",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-3",
        "truth_type": "PLOT_TRUTH"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "沈砚，灾变前为城市旧楼做测绘和安全复核的自由接单人；他擅长记住墙体、回声、风向与转折关系，却没有强悍体力，也不擅长在不完整证据下相信别人。",
        "target_character_state": "UNKNOWN",
        "title": "主角",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-1",
        "truth_type": "CHARACTER_IDENTITY"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "体力、饮水、照明和当日唯一进化机会会随位置与判断被消耗；这些是选择的现实后果，不预设每次能力兑现都必须牺牲某种叙事价值。",
        "target_character_state": "UNKNOWN",
        "title": "主角代价",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-4",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "从只相信完整地图和充分证据的测绘者，成长为能在局部证据下作出唯一选择、让异常物品先打开行动可能，再用行动补足知识的人；他的上限表现为能处理更大、更不稳定的空间关系，而不是只拥有更多物资。",
        "target_character_state": "UNKNOWN",
        "title": "主角成长空间",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-5",
        "truth_type": "CUSTOM"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "target_character_state": "UNKNOWN",
        "title": "主角目标",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-2",
        "truth_type": "CHARACTER_GOAL"
      },
      {
        "agenda_bucket": "KEEP_HIDDEN",
        "behavioral_constraint": true,
        "can_reveal": false,
        "keep_hidden": true,
        "must_hint": false,
        "must_reveal": false,
        "plan": null,
        "priority": 100,
        "reader_state": "UNKNOWN",
        "reveal_depth": null,
        "reveal_permission": false,
        "source": "DEFAULT_CONCEALMENT",
        "statement": "在下一次大幅重排前，用一次物品进化确认一条可返回的空间关系，取回饮水，并带走能复核路线的现场记录。",
        "target_character_state": "UNKNOWN",
        "title": "第一阶段目标",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-6",
        "truth_type": "FUTURE_EVENT_PRECONDITION"
      }
    ],
    "must_reveal": [],
    "optional": [],
    "reveal_budget": {
      "hard_gate": false,
      "hint_guideline": "1–3",
      "partial_or_full_guideline": "0–1",
      "planned_hints": 0,
      "planned_partial_or_full": 0,
      "status": "WITHIN_GUIDELINE"
    },
    "rule": "Hidden Truth 是行为约束，不等于揭示许可；拖动 Agenda 不改变任何 Knowledge。",
    "should_hint": []
  },
  "target_chapter_ordinal": 5
}

Hidden Truth 是行为约束，不是揭示许可。只填写实际 reveal_impact；KEEP_HIDDEN 由 Python 从冻结 Agenda 保留，不得泄露；HINT 必须有可读线索且不得直接确认。

## Frozen Kernel Planning Context

{
  "author_control": {
    "intents": [
      {
        "description": "在事实支持后判断变化建筑是否存在互联关系；逐步扩大物品进化能处理的空间尺度，同时保持原功能连续性；让楼外天气、全球灾变和其他幸存者规则保持多个候选解释，直到行动证据要求收敛",
        "horizon": "LONG",
        "intent_id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-long",
        "intent_type": "ROLLING_PLANNING",
        "payload": {
          "fixed_chapter_outline": false,
          "items": [
            "在事实支持后判断变化建筑是否存在互联关系",
            "逐步扩大物品进化能处理的空间尺度，同时保持原功能连续性",
            "让楼外天气、全球灾变和其他幸存者规则保持多个候选解释，直到行动证据要求收敛"
          ],
          "route_id": "route-space-reading"
        },
        "priority": 100,
        "status": "PLANNED",
        "subject_id": "foundation-folded-tower",
        "subject_type": "STORY_FOUNDATION",
        "target_chapter_id": null,
        "title": "长期可能性"
      },
      {
        "description": "比较测距带、照明物和标记物在不同楼层状态中的异常边界；在不建立稳定聚落的前提下交换一次路线与资源观测；追查广播是否会在建筑变化前后留下可验证的空间偏差",
        "horizon": "MID",
        "intent_id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-mid",
        "intent_type": "ROLLING_PLANNING",
        "payload": {
          "fixed_chapter_outline": false,
          "items": [
            "比较测距带、照明物和标记物在不同楼层状态中的异常边界",
            "在不建立稳定聚落的前提下交换一次路线与资源观测",
            "追查广播是否会在建筑变化前后留下可验证的空间偏差"
          ],
          "route_id": "route-space-reading"
        },
        "priority": 100,
        "status": "PLANNED",
        "subject_id": "foundation-folded-tower",
        "subject_type": "STORY_FOUNDATION",
        "target_chapter_id": null,
        "title": "中期方向"
      },
      {
        "description": "记录第一次提前重排的墙面、楼梯和广播位置；从手边物品中选择一次能验证断路关系的进化；取回饮水并保留一份能在重排后复核的现场证据",
        "horizon": "SHORT",
        "intent_id": "intent-proposal-e39fee0d664e4e06923df0f31beee8eb-short",
        "intent_type": "ROLLING_PLANNING",
        "payload": {
          "fixed_chapter_outline": false,
          "items": [
            "记录第一次提前重排的墙面、楼梯和广播位置",
            "从手边物品中选择一次能验证断路关系的进化",
            "取回饮水并保留一份能在重排后复核的现场证据"
          ],
          "route_id": "route-space-reading"
        },
        "priority": 100,
        "status": "PLANNED",
        "subject_id": "foundation-folded-tower",
        "subject_type": "STORY_FOUNDATION",
        "target_chapter_id": null,
        "title": "近期方向"
      }
    ],
    "profile": {
      "active_directives": [],
      "dimensions": [
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "末日废弃建筑不是静态背景，而是会把路线、资源和谜团重新排列的可行动世界。",
          "dimension": "worldbuilding",
          "draft": {
            "core_commitments": [
              "建筑变化必须持续制造可验证的生存问题",
              "异常尺度只围绕每日物品进化扩大"
            ],
            "open_questions": [
              "建筑变化的原因与其他使用者范围"
            ],
            "preferences": [
              "以具体空间关系承载中等神秘度",
              "世界扩张保持开放"
            ],
            "risks": [
              "规则说明压过现场行动",
              "世界规模扩张过快"
            ],
            "summary": "末日废弃建筑不是静态背景，而是会把路线、资源和谜团重新排列的可行动世界。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "worldbuilding.md",
          "label": "世界观",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "人物首先通过私人目标和选择行动，社会关系保持低中心度但能制造证据与资源压力。",
          "dimension": "characters",
          "draft": {
            "core_commitments": [
              "沈砚想掌握离开之路而非先经营组织",
              "人物弱点必须在验证与行动的迟疑中产生后果"
            ],
            "open_questions": [
              "广播声音和幸存者的真实动机"
            ],
            "preferences": [
              "角色以现场动作区分",
              "关系以局部交换和互相矛盾观测进入"
            ],
            "risks": [
              "把角色写成能力的说明工具",
              "群像抢走主角的唯一选择"
            ],
            "summary": "人物首先通过私人目标和选择行动，社会关系保持低中心度但能制造证据与资源压力。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "characters.md",
          "label": "人物",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "情节由建筑压力、当天选择、现场验证和新瓶颈连续推动，不冻结逐章大纲。",
          "dimension": "plot",
          "draft": {
            "core_commitments": [
              "每次兑现都改变可行动范围",
              "新问题在当前后果之后出现"
            ],
            "open_questions": [
              "路线之间何时发生交叉"
            ],
            "preferences": [
              "短期行动具体，长期谜团留有弹性"
            ],
            "risks": [
              "重复找路",
              "靠巧合解释资源和广播"
            ],
            "summary": "情节由建筑压力、当天选择、现场验证和新瓶颈连续推动，不冻结逐章大纲。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "plot.md",
          "label": "剧情",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "语言紧张、具体、克制，优先写触感、距离、声音、光线和行动结果。",
          "dimension": "style",
          "draft": {
            "core_commitments": [
              "第三人称限知",
              "异常结果先被看见再被理解"
            ],
            "open_questions": [
              "更高尺度的异常如何保持可读"
            ],
            "preferences": [
              "保留爽点但避免夸张说明",
              "让物品原功能可识别"
            ],
            "risks": [
              "说明书化",
              "抽象名词替代现场"
            ],
            "summary": "语言紧张、具体、克制，优先写触感、距离、声音、光线和行动结果。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "style.md",
          "label": "文风",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "核心叙事节奏是压力逼近、唯一选择、异常验证、纯收益兑现和更大问题。",
          "dimension": "narrative",
          "draft": {
            "core_commitments": [
              "生存资源保持第一驱动力",
              "知识与谜团必须回到下一次选择"
            ],
            "open_questions": [
              "不同阶段的回报密度"
            ],
            "preferences": [
              "可以用广播和回声延迟信息",
              "不预设固定回合长度"
            ],
            "risks": [
              "悬念长期不改变行动",
              "战斗变成主线"
            ],
            "summary": "核心叙事节奏是压力逼近、唯一选择、异常验证、纯收益兑现和更大问题。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "narrative.md",
          "label": "叙事",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "对话主要交换路线、资源和可信度，不承担大段世界设定讲解。",
          "dimension": "dialogue",
          "draft": {
            "core_commitments": [
              "广播提示必须与现场后果形成张力",
              "幸存者说法保留局部立场"
            ],
            "open_questions": [
              "广播是否由单一声音持续发出"
            ],
            "preferences": [
              "短句、具体指令和可核验细节"
            ],
            "risks": [
              "角色用台词直接公布真相",
              "关系戏脱离生存压力"
            ],
            "summary": "对话主要交换路线、资源和可信度，不承担大段世界设定讲解。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "dialogue.md",
          "label": "对话",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "每轮保持可感知的选择与结果，但兑现之后允许新的压力自然打开。",
          "dimension": "pacing",
          "draft": {
            "core_commitments": [
              "不把每日选择机械映射为固定章节模板",
              "能力验证要有实际后果"
            ],
            "open_questions": [
              "建筑变化的周期和不规则性"
            ],
            "preferences": [
              "在重排前压缩时间，在验证后给结果留出重量"
            ],
            "risks": [
              "每次都强行加伤亡或牺牲",
              "只有赶路没有回报"
            ],
            "summary": "每轮保持可感知的选择与结果，但兑现之后允许新的压力自然打开。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "pacing.md",
          "label": "节奏",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "主题只在具体选择中显现：有限资源如何改变人的判断，以及可复核的知识是否足以支撑行动。",
          "dimension": "themes",
          "draft": {
            "core_commitments": [
              "不把主题凌驾于生存和进化",
              "让选择后果自然形成主题"
            ],
            "open_questions": [
              "广播和其他幸存者是否形成更广的社会主题"
            ],
            "preferences": [
              "克制处理责任与信任"
            ],
            "risks": [
              "说教",
              "用宏大主题替代能力兑现"
            ],
            "summary": "主题只在具体选择中显现：有限资源如何改变人的判断，以及可复核的知识是否足以支撑行动。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "themes.md",
          "label": "主题 / 价值观",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        },
        {
          "author_edit_count": 0,
          "author_edits": [],
          "available": true,
          "content": "连续性依靠物品拥有关系、进化边界、建筑状态、路线证据和知识不确定性维持。",
          "dimension": "continuity",
          "draft": {
            "core_commitments": [
              "每次物品进化保留原功能与已验证边界",
              "局部样本不能自动升级为全局规则"
            ],
            "open_questions": [
              "连续进化如何累积",
              "建筑重排是否存在周期"
            ],
            "preferences": [
              "使用可追溯的现场记录",
              "允许已知与未知并存"
            ],
            "risks": [
              "忘记物品位置或能力边界",
              "把候选真相写成 Canon"
            ],
            "summary": "连续性依靠物品拥有关系、进化边界、建筑状态、路线证据和知识不确定性维持。"
          },
          "effective_source": "ORIGINAL_FOUNDATION_PROPOSAL",
          "filename": "continuity.md",
          "label": "连续性",
          "source": "ORIGINAL_FOUNDATION_PROPOSAL"
        }
      ],
      "hard_constraints": {
        "must": [],
        "must_not": []
      },
      "profile_version_id": "book-profile-proposal-e39fee0d664e4e06923df0f31beee8eb",
      "version_number": 1
    },
    "reveal_agenda": [
      {
        "keep_hidden": 22,
        "must_reveal": 0,
        "optional": 0,
        "should_hint": 0
      },
      {
        "hard_gate": false,
        "hint_guideline": "1–3",
        "partial_or_full_guideline": "0–1",
        "planned_hints": 0,
        "planned_partial_or_full": 0,
        "status": "WITHIN_GUIDELINE"
      },
      {
        "engine": "Narrative Debt / Promise",
        "secret_obligations": [],
        "separate_reveal_debt_engine": false
      }
    ],
    "tasks": [],
    "truths": [
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "沈砚，灾变前为城市旧楼做测绘和安全复核的自由接单人；他擅长记住墙体、回声、风向与转折关系，却没有强悍体力，也不擅长在不完整证据下相信别人。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "主角",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-1",
        "truth_type": "CHARACTER_IDENTITY",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "全球灾变后，幸存者被困在各自的废弃建筑中，建筑结构会周期性改变，旧路线和门后空间不能默认保持不变。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-10",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "主角每天只能从自己真正拥有并能接触到的普通非生命物品中选择一件，使它沿原有功能发生一次永久进化；同一物品可以继续进化。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-11",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "物品进化必须保留可辨认的原功能，并在具体行动中显示超出普通人能力范围的结果；不能用普通工程、职业知识或一般效率解释替代。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-12",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "一次选择不能同时进化多件物品，也不能远程选择不在主角手边的对象；错配会留下真实的机会与时间压力。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-13",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "建筑变化造成的空间、路线和资源后果必须能被第三人称限知视角观察和复核；建筑成因、广播来源和其他幸存者规则暂保持候选状态。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-14",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "每一次有效兑现先改变主角当下能做什么，再把更大的空间、资源或规则问题交给下一轮选择，不用同场景的维护或牺牲把收益抵消为无效。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-15",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "沈砚：主角，旧楼测绘与安全复核接单人；以空间记录为 supporting competence，特殊优势仍来自每日物品进化。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-16",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "广播中的声音：持续提供互相矛盾的楼层提示，既可能是幸存者留下的路线，也可能正在利用建筑变化诱导行动；身份保持候选。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-17",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "门后幸存者：在不同重排状态下留下水位、粉笔线、收音机和反向楼层编号，为沈砚提供局部观测，也可能争夺同一条安全路线。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-18",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "楼外天气的目击者候选：只在沈砚进入更高空间后以可验证的物理痕迹进入故事，不预先确定其身份或可信度。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "CHARACTER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-19",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "主角目标",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-2",
        "truth_type": "CHARACTER_GOAL",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "塔内临时幸存者小群体：围绕水、照明和安全层交换局部信息，规模与立场随事实发展。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "FACTION",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-20",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "广播维护者或信号来源：作为待辨认的压力节点，不预设为万能幕后组织。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "FACTION",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-21",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "其他变化建筑中的幸存者网络：在世界扩张后才由真实路线和资源交换形成，不提前固定政治结构。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "FACTION",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-22",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "主冲突",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-3",
        "truth_type": "PLOT_TRUTH",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "体力、饮水、照明和当日唯一进化机会会随位置与判断被消耗；这些是选择的现实后果，不预设每次能力兑现都必须牺牲某种叙事价值。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "主角代价",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-4",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "从只相信完整地图和充分证据的测绘者，成长为能在局部证据下作出唯一选择、让异常物品先打开行动可能，再用行动补足知识的人；他的上限表现为能处理更大、更不稳定的空间关系，而不是只拥有更多物资。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "主角成长空间",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-5",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "在下一次大幅重排前，用一次物品进化确认一条可返回的空间关系，取回饮水，并带走能复核路线的现场记录。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "第一阶段目标",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-6",
        "truth_type": "FUTURE_EVENT_PRECONDITION",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "主要故事承载是一座会把住宅层、商场中庭、地下设备层和封闭屋顶重新拼接的高层综合楼。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "WORLD_CARRIER",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-7",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "每日唯一的物品进化是主角反复改变行动可能的第一发动机，不建立脱离它的第二成长系统。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "SIGNATURE_RULE",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-8",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      },
      {
        "author_layer": "AUTHOR_TRUTH",
        "book_id": "original-e56a54687506",
        "compatibility_status": "COMPATIBLE_WITH_GAPS",
        "compatibility_summary": "原创项目从第一章起生效",
        "confidence": 1.0,
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "description": "",
        "edition_id": "base",
        "effective_from_chapter": 1,
        "effective_until_chapter": null,
        "introduced_by": "AUTHOR_CONFIRMED",
        "metadata": {
          "foundation_candidate_id": "foundation-folded-tower",
          "proposal_version_id": "proposal-e39fee0d664e4e06923df0f31beee8eb"
        },
        "must_remain_true": true,
        "object_id": null,
        "object_type": null,
        "requires_revision": false,
        "retroactive_scope": "FORWARD_ONLY",
        "statement": "使用第三人称限知，让物品结果、空间错位和广播可信度都通过主角能观察到的后果逐步确认。",
        "status": "ACTIVE_TRUTH",
        "subject_id": null,
        "subject_type": "STORY_FOUNDATION",
        "tags": [
          "ORIGINAL_GENESIS"
        ],
        "title": "NARRATIVE_FORM",
        "truth_id": "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-9",
        "truth_type": "CUSTOM",
        "updated_at": "2026-08-16T16:22:26.798563+00:00",
        "version": 1
      }
    ]
  },
  "coverage": {
    "blocking_gaps": [],
    "known": [
      "contract:GENRE",
      "contract:MARKET_CATEGORY",
      "contract:NARRATIVE_DRIVE",
      "contract:PAYOFF_CHANNEL",
      "contract:PROGRESSION",
      "contract:READER_EXPERIENCE",
      "contract:WORLD_EXPANSION",
      "progression_state"
    ],
    "partial": [
      "source_state"
    ],
    "unknown": []
  },
  "current_progression": {
    "axis": "owned-object-evolution",
    "bottlenecks": [
      "可用物品与当前空间缺口不匹配",
      "建筑变化快于主角能完成的现场验证",
      "同一物品的下一次进化需要新的问题而非简单重复"
    ],
    "growth_costs": [
      "每天唯一选择造成真实机会成本；错配、位置和时间压力会改变下一轮选择，但不自动取消当前兑现。"
    ],
    "missing_resources": [
      "真实拥有的普通非生命物品",
      "可执行的现场问题",
      "可进入的现场",
      "足够观察结果的时间",
      "至少一件已验证的进化物品",
      "新的空间压力"
    ],
    "next_stage_visibility": "UNKNOWN",
    "pending_ability_showcases": [],
    "readiness": "MISSING_RESOURCE",
    "stage": null
  },
  "knowledge_boundary": [],
  "narrative_debts": [],
  "narrative_drives": {
    "drive_priorities": {
      "ABILITY_PROGRESSION": 70,
      "KNOWLEDGE_PROGRESSION": 85,
      "MYSTERY_INVESTIGATION": 55,
      "SURVIVAL_RESOURCE": 100,
      "WORLD_EXPLORATION": 40
    },
    "primary_drive": "SURVIVAL_RESOURCE",
    "secondary_drives": [
      "KNOWLEDGE_PROGRESSION",
      "ABILITY_PROGRESSION",
      "MYSTERY_INVESTIGATION",
      "WORLD_EXPLORATION"
    ]
  },
  "reader_anticipation": [
    {
      "anticipation_id": "anticipation-thread-1",
      "evidence": [],
      "expected_horizon": "MID",
      "expected_payoff_channel": "CUSTOM",
      "last_served": null,
      "maturity": null,
      "risk_if_delayed": "读者期待继续积累",
      "source": "ACTIVE_THREAD",
      "source_reference_id": "thread-1",
      "status": "BUILDING",
      "subject": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
      "urgency": 3
    },
    {
      "anticipation_id": "anticipation-world-earned-spatial-frontier",
      "evidence": [
        "当前建筑中的能力兑现产生不可忽略的外部指向",
        "主角拥有能在新空间验证路线的物品或组合",
        "前一阶段的事实与作者后续确认共同支持更高空间",
        "新的行动可能由已确认的物品机制而非第二系统打开"
      ],
      "expected_horizon": "LONG",
      "expected_payoff_channel": "WORLD_EXPANSION",
      "last_served": null,
      "maturity": null,
      "risk_if_delayed": "世界长期没有打开新的可能性",
      "source": "WORLD_EXPANSION",
      "source_reference_id": "earned-spatial-frontier",
      "status": "BUILDING",
      "subject": "扩大可行动范围会把主角带到怎样的新规则和资源风险中？",
      "urgency": 3
    }
  ],
  "reader_experience_core_promises": [
    "每日唯一的进化选择必须在后续生存处境中产生可感知、可验证的行动优势或代价。",
    "建筑结构变化必须持续制造探索、路线和资源重组压力，而不是只作为背景设定。",
    "普通非生命物品沿原有功能发生的质变必须打开读者能理解并期待兑现的新行动可能性。",
    "选择的机会成本和失败后果不能被无限资源、无限次数或无代价多选抵消。",
    {
      "promise_id": "survival-resource-choice",
      "statement": "建筑变化把已有物品、储备和安全位置持续变成必须现场取舍的生存问题。",
      "strength": "CORE"
    },
    {
      "promise_id": "verified-object-evolution",
      "statement": "普通非生命物品的永久质变会在具体行动中打开普通人无法复制的新可能。",
      "strength": "CORE"
    }
  ],
  "resources_and_opportunities": {
    "opportunities": [],
    "owned_or_current": [
      {
        "attributes": [
          {
            "author_visible": false,
            "key": "amount",
            "label": "amount",
            "value": "half_bottle"
          },
          {
            "author_visible": false,
            "key": "change",
            "label": "change",
            "value": "recovered"
          },
          {
            "author_visible": false,
            "key": "evidence",
            "label": "evidence",
            "value": "沈砚从重排后的对面平台取回半瓶水并饮用一口。"
          },
          {
            "author_visible": false,
            "key": "owner_id",
            "label": "owner_id",
            "value": "protagonist"
          },
          {
            "author_visible": false,
            "key": "resource",
            "label": "resource",
            "value": "water"
          },
          {
            "author_visible": false,
            "key": "source_draft_id",
            "label": "source_draft_id",
            "value": "draft_8bb76c611125c76689997a74"
          },
          {
            "author_visible": false,
            "key": "source_span_id",
            "label": "source_span_id",
            "value": "canon-span_96f6a1794bf43a1659c7fba2"
          }
        ],
        "category": "resource",
        "changed_this_chapter": false,
        "layer": "CANON",
        "layer_label": "正史已确认",
        "name": "半瓶水",
        "raw": {
          "_edition_id": "base",
          "_event_id": "event_34aec5c02d27eedb1ffc9f6c",
          "_event_seq": 3,
          "_source_id": "draft_8bb76c611125c76689997a74",
          "_source_kind": "AUTHOR_APPROVED_DRAFT",
          "amount": "half_bottle",
          "change": "recovered",
          "character_id": "protagonist",
          "evidence": "沈砚从重排后的对面平台取回半瓶水并饮用一口。",
          "name": "半瓶水",
          "owner_id": "protagonist",
          "resource": "water",
          "resource_id": "water-half-bottle-recovered",
          "source_draft_id": "draft_8bb76c611125c76689997a74",
          "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
        },
        "record_id": "water-half-bottle-recovered",
        "statement": "",
        "status": "CANON",
        "status_label": "正史已确认"
      },
      {
        "attributes": [
          {
            "author_visible": false,
            "key": "amount",
            "label": "amount",
            "value": "half_bottle"
          },
          {
            "author_visible": false,
            "key": "change",
            "label": "change",
            "value": "recovered"
          },
          {
            "author_visible": false,
            "key": "evidence",
            "label": "evidence",
            "value": "沈砚从重排后的对面平台取回半瓶水并饮用一口。"
          },
          {
            "author_visible": false,
            "key": "owner_id",
            "label": "owner_id",
            "value": "protagonist"
          },
          {
            "author_visible": false,
            "key": "resource",
            "label": "resource",
            "value": "water"
          },
          {
            "author_visible": false,
            "key": "source_draft_id",
            "label": "source_draft_id",
            "value": "draft_8bb76c611125c76689997a74"
          },
          {
            "author_visible": false,
            "key": "source_span_id",
            "label": "source_span_id",
            "value": "canon-span_96f6a1794bf43a1659c7fba2"
          }
        ],
        "category": "resource",
        "changed_this_chapter": false,
        "layer": "CANON",
        "layer_label": "正史已确认",
        "name": "半瓶水",
        "owner_name": "protagonist",
        "raw": {
          "_edition_id": "base",
          "_event_id": "event_34aec5c02d27eedb1ffc9f6c",
          "_event_seq": 3,
          "_source_id": "draft_8bb76c611125c76689997a74",
          "_source_kind": "AUTHOR_APPROVED_DRAFT",
          "amount": "half_bottle",
          "change": "recovered",
          "character_id": "protagonist",
          "evidence": "沈砚从重排后的对面平台取回半瓶水并饮用一口。",
          "name": "半瓶水",
          "owner_id": "protagonist",
          "resource": "water",
          "resource_id": "water-half-bottle-recovered",
          "source_draft_id": "draft_8bb76c611125c76689997a74",
          "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
        },
        "record_id": "water-half-bottle-recovered",
        "statement": "",
        "status": "CANON",
        "status_label": "正史已确认"
      }
    ]
  },
  "scheduler_recommendation": {
    "alternatives": [
      "CONTINUITY_ADVANCE",
      "TRANSITION"
    ],
    "author_override_applied": false,
    "engine_recommendations": [
      {
        "debt_ids": [],
        "drive": "KNOWLEDGE_PROGRESSION",
        "engine_type": "PROGRESSION",
        "evidence": [],
        "intent": "RESOURCE_OPPORTUNITY",
        "priority": 72.0,
        "reader_promises": [
          "每日唯一的进化选择必须在后续生存处境中产生可感知、可验证的行动优势或代价。",
          "建筑结构变化必须持续制造探索、路线和资源重组压力，而不是只作为背景设定。",
          "普通非生命物品沿原有功能发生的质变必须打开读者能理解并期待兑现的新行动可能性。",
          "选择的机会成本和失败后果不能被无限资源、无限次数或无代价多选抵消。"
        ],
        "risks": [
          "资源门槛缺少证据，不能把机会写成已拥有"
        ],
        "why_now": [
          "下一成长门槛缺少已确认资源"
        ]
      },
      {
        "debt_ids": [],
        "drive": "ABILITY_PROGRESSION",
        "engine_type": "PROGRESSION",
        "evidence": [],
        "intent": "RESOURCE_OPPORTUNITY",
        "priority": 72.0,
        "reader_promises": [
          "每日唯一的进化选择必须在后续生存处境中产生可感知、可验证的行动优势或代价。",
          "建筑结构变化必须持续制造探索、路线和资源重组压力，而不是只作为背景设定。",
          "普通非生命物品沿原有功能发生的质变必须打开读者能理解并期待兑现的新行动可能性。",
          "选择的机会成本和失败后果不能被无限资源、无限次数或无代价多选抵消。"
        ],
        "risks": [
          "资源门槛缺少证据，不能把机会写成已拥有"
        ],
        "why_now": [
          "下一成长门槛缺少已确认资源"
        ]
      }
    ],
    "primary_intent": "RESOURCE_OPPORTUNITY",
    "reader_promises_served": [
      "每日唯一的进化选择必须在后续生存处境中产生可感知、可验证的行动优势或代价。",
      "建筑结构变化必须持续制造探索、路线和资源重组压力，而不是只作为背景设定。",
      "普通非生命物品沿原有功能发生的质变必须打开读者能理解并期待兑现的新行动可能性。",
      "选择的机会成本和失败后果不能被无限资源、无限次数或无代价多选抵消。"
    ],
    "risks": [
      "资源门槛缺少证据，不能把机会写成已拥有"
    ],
    "secondary_intents": [],
    "source_drive": "KNOWLEDGE_PROGRESSION",
    "supporting_anticipation_ids": [
      "anticipation-thread-1",
      "anticipation-world-earned-spatial-frontier"
    ],
    "supporting_debt_ids": [],
    "supporting_thread_ids": [
      "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
    ],
    "why_now": [
      "下一成长门槛缺少已确认资源"
    ]
  },
  "warnings": [],
  "why_this_book_is_worth_following": [
    "每日唯一的进化选择必须在后续生存处境中产生可感知、可验证的行动优势或代价。",
    "建筑结构变化必须持续制造探索、路线和资源重组压力，而不是只作为背景设定。",
    "普通非生命物品沿原有功能发生的质变必须打开读者能理解并期待兑现的新行动可能性。",
    "选择的机会成本和失败后果不能被无限资源、无限次数或无代价多选抵消。"
  ],
  "world_expansion": {
    "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
    "chapter_ordinal": 4,
    "current_stage": {
      "expansion_types": [
        "GEOGRAPHIC",
        "MYSTERY",
        "KNOWLEDGE"
      ],
      "faction_ceiling": "偶遇的幸存者和广播声音只形成局部压力，不成为阵营主轴。",
      "knowledge_ceiling": "能辨认若干先兆和重排后的局部规律，但不能据此宣称全局真相。",
      "known_map": [
        "沈砚当前可达的楼梯、门、设备层和至少一个高位缺口"
      ],
      "mystery_ceiling": "建筑为何变化、广播从何而来只允许保留现场可验证线索。",
      "name": "塔内可验证空间",
      "order": 1,
      "power_ceiling": "单件进化先改变局部记录、定位、照明或固定关系。",
      "reader_question": "下一次重排会把哪条路线和哪件资源变成新的选择？",
      "resource_ceiling": "水、照明、电池、绳索和记录工具仍是有限且可搬运的物资。",
      "stage_id": "current-known-space",
      "status": "AVAILABLE",
      "transition_conditions": [
        "完成一次能跨越局部重排的能力验证",
        "获得指向另一建筑或更大空间关系的现场证据"
      ],
      "world_scope": "一座会重排的高层综合楼内部：住宅层、商场中庭、设备层与封闭屋顶的局部关系可以被主角通过行动验证。"
    },
    "next_stage_candidates": [
      {
        "expansion_types": [
          "GEOGRAPHIC",
          "MYSTERY",
          "KNOWLEDGE",
          "POWER"
        ],
        "faction_ceiling": "不同幸存者的观测和资源交换可能造成局部竞争，但不抢走生存选择。",
        "knowledge_ceiling": "主角能够把局部样本拼成可测试的区域规则，但仍保留反例。",
        "known_map": [
          "由已验证物品和现场记录维持的若干连接关系"
        ],
        "mystery_ceiling": "建筑变化与全球灾变的关联出现可改变行动的证据。",
        "name": "互联建筑前沿",
        "order": 2,
        "power_ceiling": "既有物品的连续进化或组合可以处理更长距离、更大遮蔽和多入口关系。",
        "reader_question": "扩大可行动范围会把主角带到怎样的新规则和资源风险中？",
        "resource_ceiling": "资源机会来自空间重组和进入新区域，而不是无限供应。",
        "stage_id": "earned-spatial-frontier",
        "status": "AVAILABLE",
        "transition_conditions": [
          "当前建筑中的能力兑现产生不可忽略的外部指向",
          "主角拥有能在新空间验证路线的物品或组合"
        ],
        "world_scope": "多座变化建筑或建筑之间的异常连接成为可进入的前沿；路线、物资和先兆不再只属于一栋楼。"
      },
      {
        "expansion_types": [
          "GEOGRAPHIC",
          "MYSTERY",
          "ONTOLOGICAL"
        ],
        "faction_ceiling": "其他幸存者和更大范围的组织关系保持开放，不提前固定。",
        "knowledge_ceiling": "只能逐步把异常变成可检验问题，不允许一次性解释全部世界。",
        "known_map": [],
        "mystery_ceiling": "原因、制造者或建筑本体只作为候选真相，不等同于 Canon。",
        "name": "楼外未知边界",
        "order": 3,
        "power_ceiling": "更大尺度的空间关系和局部生存规则可能被既有物品原功能质变触及，具体上限不预建。",
        "reader_question": "当可行动空间超出这座塔，主角的每日选择还能改写什么？",
        "resource_ceiling": "新的资源类型只有在真实探索和现场后果中出现才可进入规划。",
        "stage_id": "higher-unknown-space",
        "status": "UNKNOWN",
        "transition_conditions": [
          "前一阶段的事实与作者后续确认共同支持更高空间",
          "新的行动可能由已确认的物品机制而非第二系统打开"
        ],
        "world_scope": "只保留方向和问题的更高空间：楼外天气、全球灾变尺度以及建筑存在方式可能被重新理解。"
      }
    ],
    "source_layer": "CONTRACT_PLUS_CHAPTER_WORLD_STATE",
    "stagnation_diagnostic": null,
    "transition_conditions": [
      "当前建筑中的能力兑现产生不可忽略的外部指向",
      "主角拥有能在新空间验证路线的物品或组合",
      "前一阶段的事实与作者后续确认共同支持更高空间",
      "新的行动可能由已确认的物品机制而非第二系统打开"
    ]
  }
}

不要填写 scheduler_alignment、评分、硬门或内部 provenance；Lens 与 Chapter Intent是创意决定，Python 会根据冻结输入计算 Debt / Anticipation 对齐。
Reader/Drive/Progression/Resource/World/Drift 字段只是 declared claims；Python 将依据 kernel_context.json 重新核验。

## Frozen Reference Corpus Planning Context

下列内容只提供 REFERENCE_ONLY 的可迁移机制和对照；不得复制来源人物、事件、设定或句式，也不得改变 Boundary、Canon、资源、知识边界或 Candidate 选择。
```json
{
  "compact_cards": [
    {
      "card_id": "contrast-payoff-fatigue",
      "card_type": "contrast-card",
      "category_ids": [
        "科幻",
        "UNKNOWN",
        "灵异"
      ],
      "creative_problem_tags": [
        "fatigue"
      ],
      "evidence_scope": "MULTI_CATEGORY",
      "knowledge_level": "CROSS_BOOK_CONTRAST",
      "maturity": "PILOT",
      "metadata_match_fields": [
        "creative_problem_tags",
        "reader_experiences",
        "narrative_drives",
        "payoff_channels"
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
      "shared_creative_problem": "重复回报疲劳的不同风险",
      "solutions": [
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "连续把能力验证写成同一类更高位对撞。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "同形对撞",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-payoff-fatigue-1",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        },
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "保留能力但改变场景和组合。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "旧机制换用途",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-payoff-fatigue-2",
          "tradeoffs": [
            "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
          ]
        },
        {
          "conditions": [
            "该解法在来源中有局部动作或结构证据。"
          ],
          "description": "把读者注意力转给新关系或未知发现。",
          "failure_risks": [
            "INFERRED_RISK：若没有后续变化，解法可能重复。"
          ],
          "label": "关系/探索转向",
          "reader_experience_differences": [
            "读者获得与其他解法不同的期待入口。"
          ],
          "solution_id": "contrast-payoff-fatigue-3",
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
        "creative_problem_tags",
        "reader_experiences",
        "narrative_drives",
        "payoff_channels"
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
        "creative_problem_tags",
        "reader_experiences",
        "narrative_drives",
        "payoff_channels"
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
    }
  ],
  "knowledge_gaps": [],
  "reference_strategy": {
    "application_summary": "按 reader_experiences、narrative_drives、payoff_channels、creative_problem_tags 从冻结卡片中选择 contrast-payoff-fatigue、synth-category-01、synth-category-02；仅选对照方案 contrast-payoff-fatigue-1；仅迁移可复用机制，当前书事实、状态与最终选择仍由本次合同决定。",
    "failure_modes": [],
    "match_tier": "EXACT",
    "reuse_reason": "复用近期卡片并未找到更合适的 bounded card",
    "selected_card_ids": [
      "contrast-payoff-fatigue",
      "synth-category-01",
      "synth-category-02"
    ],
    "selected_cards": [
      {
        "card_id": "contrast-payoff-fatigue",
        "card_type": "contrast-card",
        "category_ids": [
          "科幻",
          "UNKNOWN",
          "灵异"
        ],
        "creative_problem_tags": [
          "fatigue"
        ],
        "evidence_scope": "MULTI_CATEGORY",
        "knowledge_level": "CROSS_BOOK_CONTRAST",
        "maturity": "PILOT",
        "metadata_match_fields": [
          "creative_problem_tags",
          "reader_experiences",
          "narrative_drives",
          "payoff_channels"
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
        "shared_creative_problem": "重复回报疲劳的不同风险",
        "solutions": [
          {
            "conditions": [
              "该解法在来源中有局部动作或结构证据。"
            ],
            "description": "连续把能力验证写成同一类更高位对撞。",
            "failure_risks": [
              "INFERRED_RISK：若没有后续变化，解法可能重复。"
            ],
            "label": "同形对撞",
            "reader_experience_differences": [
              "读者获得与其他解法不同的期待入口。"
            ],
            "solution_id": "contrast-payoff-fatigue-1",
            "tradeoffs": [
              "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
            ]
          },
          {
            "conditions": [
              "该解法在来源中有局部动作或结构证据。"
            ],
            "description": "保留能力但改变场景和组合。",
            "failure_risks": [
              "INFERRED_RISK：若没有后续变化，解法可能重复。"
            ],
            "label": "旧机制换用途",
            "reader_experience_differences": [
              "读者获得与其他解法不同的期待入口。"
            ],
            "solution_id": "contrast-payoff-fatigue-2",
            "tradeoffs": [
              "会把注意力集中到该解法对应的体验，不能同时保证所有回报。"
            ]
          },
          {
            "conditions": [
              "该解法在来源中有局部动作或结构证据。"
            ],
            "description": "把读者注意力转给新关系或未知发现。",
            "failure_risks": [
              "INFERRED_RISK：若没有后续变化，解法可能重复。"
            ],
            "label": "关系/探索转向",
            "reader_experience_differences": [
              "读者获得与其他解法不同的期待入口。"
            ],
            "solution_id": "contrast-payoff-fatigue-3",
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
          "creative_problem_tags",
          "reader_experiences",
          "narrative_drives",
          "payoff_channels"
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
          "creative_problem_tags",
          "reader_experiences",
          "narrative_drives",
          "payoff_channels"
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
      }
    ],
    "selected_contrast_solutions": [
      "contrast-payoff-fatigue-1"
    ],
    "snapshot_hash": "a91367fd7151bd6e62dd96a20bb104b53cfde98060ab8fa9194ac45b3bcd23c4",
    "snapshot_id": "reference-context_0372f78568c5a130adac0e69",
    "strategy_id": "planning-reference-strategy_b25692309649de81cafbfe4f",
    "usage": "REFERENCE_ONLY"
  },
  "selected_card_count": 6,
  "selected_card_ids": [
    "contrast-payoff-fatigue",
    "synth-category-01",
    "synth-category-02",
    "synth-category-03",
    "synth-category-04",
    "synth-category-05"
  ],
  "selected_card_knowledge_levels": [
    "CROSS_BOOK_CONTRAST",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS",
    "CORPUS_SYNTHESIS"
  ],
  "selected_card_types": [
    "contrast-card",
    "corpus-synthesis",
    "corpus-synthesis",
    "corpus-synthesis",
    "corpus-synthesis",
    "corpus-synthesis"
  ],
  "snapshot_hash": "a91367fd7151bd6e62dd96a20bb104b53cfde98060ab8fa9194ac45b3bcd23c4",
  "snapshot_id": "reference-context_0372f78568c5a130adac0e69",
  "status": "ENABLED",
  "warnings": []
}
```

## Recent Chapter Experience Signatures（soft guidance）

重复体验模式只产生软提醒，不构成整批候选硬失败；请在创意摘要中保留变化或复用理由。
```json
[
  {
    "action_space_delta": "",
    "core_promise_delivery": "anticipation-thread-1",
    "emotional_outcome": "",
    "ending_mode": "CONSEQUENCE",
    "event_source": "capability;fact;thread;character_state",
    "knowledge_delta": "",
    "outcome_magnitude": "",
    "protagonist_strategy": "",
    "relationship_delta": "",
    "risk_form": "",
    "scene_topology": "DIALOGUE",
    "social_feedback": "",
    "solution_method": "",
    "world_scale_delta": ""
  },
  {
    "action_space_delta": "",
    "core_promise_delivery": "anticipation-thread-1;anticipation-world-earned-spatial-frontier",
    "emotional_outcome": "",
    "ending_mode": "CONSEQUENCE",
    "event_source": "capability;fact;thread;character_state",
    "knowledge_delta": "",
    "outcome_magnitude": "",
    "protagonist_strategy": "",
    "relationship_delta": "",
    "risk_form": "",
    "scene_topology": "DIALOGUE",
    "social_feedback": "",
    "solution_method": "",
    "world_scale_delta": ""
  },
  {
    "action_space_delta": "",
    "core_promise_delivery": "anticipation-thread-1;anticipation-world-earned-spatial-frontier",
    "emotional_outcome": "",
    "ending_mode": "CONSEQUENCE",
    "event_source": "capability;fact;thread;character_state",
    "knowledge_delta": "",
    "outcome_magnitude": "",
    "protagonist_strategy": "",
    "relationship_delta": "",
    "risk_form": "",
    "scene_topology": "DIALOGUE",
    "social_feedback": "",
    "solution_method": "",
    "world_scale_delta": ""
  },
  {
    "action_space_delta": "",
    "core_promise_delivery": "在第一次重排中获得一条可复核的空间关系并取回饮水。",
    "emotional_outcome": "",
    "ending_mode": "CONSEQUENCE",
    "event_source": "capability;resource;fact;thread;character_state",
    "knowledge_delta": "",
    "outcome_magnitude": "",
    "protagonist_strategy": "",
    "relationship_delta": "",
    "risk_form": "",
    "scene_topology": "DIALOGUE",
    "social_feedback": "",
    "solution_method": "",
    "world_scale_delta": ""
  }
]
```
