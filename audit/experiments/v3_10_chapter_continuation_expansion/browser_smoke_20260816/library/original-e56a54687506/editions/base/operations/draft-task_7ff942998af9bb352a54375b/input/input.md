# 章节正文任务 `draft-task_7ff942998af9bb352a54375b`

revision: 1

严格依据下面的 Boundary Packet 与 Chapter Contract 写正文。
正文不得声明新事实已自动进入正史；state_changes 只声明正文实际发生的状态变化。
不要填写 contract_evidence、evidence_quotes、character_fit_inputs、style_fit_inputs、structure_tags、RealizedKernelTrace 或系统评分；这些由 Python 编译。
按 Chapter Contract 中冻结的 InnovationControl 执行；它只改变创作距离，不改变 Canon、Timeline、Knowledge、Capability、Resource、Approval 或 Edition hard gates。
Creative-distance guidance：在 Fidelity 与 Creativity 之间平衡；三个 Lens 都应有真实发挥空间，新人物、关系、地点、威胁、交易、世界信息或规则表现必须由当前因果引入。
Lens tendency：CONTINUITY_ACTIVE_THREAD ≈ EARNED_OPPORTUNITY ≈ FORWARD_EXPANSION；不得把它写成 Score Bonus。
Canon、Timeline、Knowledge、Capability、Resource 与 Approval 的硬约束由系统内核、Chapter Contract 和 Validator 负责；正文只写人物如何感知、选择、行动及其后果，不解释这些治理规则。
本章至少让一个重要状态发生可读的改变；未知可以保留，但若核心谜团继续悬置，必须推进或兑现另一条 SHORT/MID 线程。
Reveal Agenda 由系统保留；reveal_trace.planned 可省略或只记录本次实际采用的计划，realized 只记录正文真正发生的线索或揭示，且 evidence_quote 必须出现在正文中。KEEP_HIDDEN 的 Truth 只能约束行为，不能被旁白、对话或解释直接说破；HINT 必须留下读者可感知线索，但不能确认完整答案。
系统会从正文、实际 StateChange、Chapter Contract、Reveal 与 promises自动编译实际 trace；不要把 Expected Kernel Trace 或系统审计字段写进正文输出。
避免连续使用‘谨慎试探—暂不下结论—保留退路—撤回’的审计型叙事，除非当前 Narrative Portfolio 明确需要这种节奏。
只写 output.json，不要修改 book；系统会把合法正文导入 drafts。

## Chapter Realization Brief（soft guidance）

以下范围只用于调节场景展开，不是最低字数硬门；可以用更短或更长的自然场景，但不得用摘要跳过关键动作、反应与后果。允许 realization-only micro-event，不得改变 Contract、Canon、Knowledge、Resource 或 Capability。
```json
{
  "adaptive": true,
  "dramatization_targets": [
    "第一件普通物品永久获得跨局部重排保持空间关系的异常能力，沈砚从此拥有一条不能被旧地图解释的路线证据。",
    "重排结束后，测距带两端仍指向同一面墙，但那面墙上多出一扇原本不存在的门，广播从门内报出沈砚尚未说出口的楼层。"
  ],
  "micro_event_rule": "允许只改变人物感知、动作或场面反应的 realization-only micro-event；不得改变 Contract、Canon、Knowledge、Resource 或 Capability。",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "target_scene_count": 1,
  "target_word_range": [
    1800,
    3200
  ]
}
```

## Novel Prose Realization Protocol（Normal Draft / Revision Draft shared）

Novel Prose Realization 只控制表达层；Chapter Contract、Canon、Boundary、人物事实、资源、知识边界、事件顺序、payoff 与结尾状态保持不变。
```json
{
  "authority": "Chapter Contract > Canon > Current Scene Context > Prose Controls",
  "controls_may_change": [
    "句法、段落节奏、信息呈现、对话自然度、描写与场景收束"
  ],
  "controls_must_not_change": [
    "Chapter Contract、Boundary、Canon、事件顺序、人物选择、资源、知识边界、事实、payoff、不可逆改变或结尾状态"
  ],
  "shared_with": "Revision Draft Novel Prose Realization",
  "thin_scene_repair": {
    "maximum_attempts": 1,
    "must_not_change": [
      "state_changes、abilities、resources、Chapter Contract 或 ending_state"
    ],
    "scope": "REALIZATION_ONLY"
  }
}
```

## Continuation Boundary Packet

# Continuation Boundary Packet `boundary_259d824b858568b09c2a05fd`

- book_id: `original-e56a54687506`
- base_event_seq: 0
- projection_sha256: `0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448`
- current_position: {"last_canon_chapter": 0, "next_chapter": 1}

## 最近完整章节

## 更早章节摘要

```json
[]
```

## FTS5 相关原文片段

```json
[]
```

## 当前正史

```json
{}
```

## 人物状态

```json
{}
```

## 人物知识边界

```json
{}
```

## 活跃线程

```json
[
  {
    "book_id": "original-e56a54687506",
    "created_at": "2026-08-16T16:22:26.798563+00:00",
    "dependencies_json": "[]",
    "edition_id": "base",
    "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
    "importance": 1.0,
    "introduced_chapter": null,
    "last_advanced_chapter": null,
    "payload_json": "{\"foundation_candidate_id\": \"foundation-folded-tower\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"route_id\": \"route-space-reading\", \"stakes\": \"建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
    "phase": "setup",
    "progress": 0.0,
    "reader_visibility": 1.0,
    "source_span_id": null,
    "stakes": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
    "status": "APPROVED_OUTLINE",
    "target_payoff_max": null,
    "target_payoff_min": null,
    "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
    "version": 1
  }
]
```

## 承诺与悬念

```json
{}
```

## 资源

```json
{}
```

## 能力

```json
{}
```

## 关系

```json
{}
```

## 最近爽点

```json
{}
```

## 最近结构

```json
[]
```

## 文风样本

```json
[]
```

## 作者指令与禁忌

```json
[
  {
    "book_id": "original-e56a54687506",
    "content": "整体紧张、具体、克制，但每次明确的能力验证要给出可感知的爽点。",
    "created_at": "2026-08-16T16:22:26.798563+00:00",
    "directive_id": "directive-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-preference-1",
    "directive_type": "preference",
    "edition_id": "base",
    "mode": "persistent",
    "priority": 100,
    "source": "AUTHOR_CONFIRMED_FOUNDATION",
    "status": "ACTIVE",
    "version": 1
  }
]
```

## 章节节奏特征

```json
[]
```

## 长跨度节奏诊断

```json
{
  "analyzer_versions": {
    "deterministic": "rhythm-deterministic-v1",
    "semantic": "rhythm-semantic-v1"
  },
  "as_of_chapter": 0,
  "as_of_event_seq": 0,
  "book_id": "original-e56a54687506",
  "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
  "created_at": "2026-08-16T16:22:43.816794+00:00",
  "edition_id": "base",
  "ending_mode_streak": {
    "count": 0,
    "mode": null,
    "severity": "NONE"
  },
  "ending_similarity": {
    "matching_chapters": [],
    "max_similarity_last_4": 0.0,
    "severity": "NONE"
  },
  "evidence": [],
  "high_emotion_streak": {
    "bands": [],
    "climax_bonus": 2,
    "count": 0,
    "severity": "NONE"
  },
  "hooks": {
    "advance_due": [],
    "overdue": [],
    "resolve_due": []
  },
  "opening_similarity": {
    "matching_chapters": [],
    "max_similarity_last_4": 0.0,
    "severity": "NONE"
  },
  "projection_hash": "0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448",
  "same_function_streak": {
    "count": 0,
    "function": null,
    "severity": "NONE",
    "source": "planned_primary_function"
  },
  "snapshot_id": "rhythm-snapshot_aaf105266066ce01400a3c7c",
  "title_repetition": {
    "exact_duplicates": [],
    "matching_chapters": [],
    "max_similarity_last_20": 0.0,
    "series_markers": [],
    "severity": "NONE"
  }
}
```

## 伏笔动作队列

```json
{
  "advance_due": [],
  "as_of_chapter": 0,
  "book_id": "original-e56a54687506",
  "edition_id": "base",
  "hold": [],
  "overdue": [],
  "queues": {
    "ADVANCE": [],
    "HOLD": [],
    "OVERDUE": [],
    "RESOLVE": []
  },
  "resolve_due": []
}
```

## Story Atlas anchor

```json
{}
```

## Batch anchor

```json
{}
```

## Active Author Truths

```json
[
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
```

## Chapter Reveal Agenda

```json
{
  "book_id": "original-e56a54687506",
  "chapter_ordinal": 1,
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
}
```

## Innovation Control

```json
{
  "focus": [
    "auto"
  ],
  "level": "medium"
}
```

## Innovation diagnostics

```json
{
  "open_novelty_debt": [],
  "portfolio_snapshot": {
    "consecutive_deferrals": 0,
    "current_chapter": 0,
    "long_threads": [],
    "mid_threads": [
      {
        "debt_ids": [],
        "horizon": "MID",
        "last_advanced": 0,
        "lifecycle": "SETUP",
        "maturity": 0.0,
        "maturity_note": "",
        "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "opened_chapter": 0,
        "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
      }
    ],
    "narrative_debts": [],
    "overdue_debt_ids": [],
    "payoff_ready_thread_ids": [],
    "short_threads": [],
    "snapshot_id": "portfolio_8e7be71c73960b621a0e2723",
    "warnings": []
  },
  "question_balance": {
    "answered": 0,
    "materially_advanced": 0,
    "newly_opened": 0,
    "over_deferred": false,
    "partially_paid": 0,
    "penalty": 0.0
  },
  "recent_pattern_distance": "medium",
  "recommendation": {
    "evidence": [
      "active_threads",
      "recent_structures",
      "earned_surface.available_payoffs"
    ],
    "pattern_distance": "medium",
    "reason": [
      "最近窗口结构差异为 medium，仅作为软规划信号",
      "当前存在 1 个活跃线程、0 个开放设置"
    ],
    "recommended_focus": [
      "world",
      "character"
    ]
  },
  "repeated_patterns": [],
  "semantic_policy_leak": null,
  "window_chapters": []
}
```

## 警告

```json
[]
```


## Chapter Contract

```json
{
  "action_space_delta_target": "",
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
  "anticipation_impact": [],
  "boundary_packet_id": "boundary_259d824b858568b09c2a05fd",
  "candidate_id": "genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape",
  "canon_constraints": [
    "全球灾变后，幸存者被困在各自的废弃建筑中，建筑结构会周期性改变，旧路线和门后空间不能默认保持不变。",
    "主角每天只能从自己真正拥有并能接触到的普通非生命物品中选择一件，使它沿原有功能发生一次永久进化；同一物品可以继续进化。",
    "物品进化必须保留可辨认的原功能，并在具体行动中显示超出普通人能力范围的结果；不能用普通工程、职业知识或一般效率解释替代。",
    "一次选择不能同时进化多件物品，也不能远程选择不在主角手边的对象；错配会留下真实的机会与时间压力。",
    "建筑变化造成的空间、路线和资源后果必须能被第三人称限知视角观察和复核；建筑成因、广播来源和其他幸存者规则暂保持候选状态。",
    "每一次有效兑现先改变主角当下能做什么，再把更大的空间、资源或规则问题交给下一轮选择，不用同场景的维护或牺牲把收益抵消为无效。"
  ],
  "chapter": 1,
  "chapter_intent": null,
  "commit_updates": [
    "thread_status:thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
    "character_state:protagonist"
  ],
  "continuation_boundary": {
    "base_event_seq": 0,
    "base_projection_hash": "0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448",
    "batch_anchor": {},
    "last_canon_chapter": 0,
    "story_atlas_anchor": {}
  },
  "contract_id": "contract_d1955693b3c1166033b242e9",
  "declared_kernel_trace": {},
  "dramatization_targets": [
    "第一件普通物品永久获得跨局部重排保持空间关系的异常能力，沈砚从此拥有一条不能被旧地图解释的路线证据。",
    "重排结束后，测距带两端仍指向同一面墙，但那面墙上多出一扇原本不存在的门，广播从门内报出沈砚尚未说出口的楼层。"
  ],
  "effective_book_profile": {
    "active_directives": [],
    "author_edits": [],
    "baseline": {
      "characters": {
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
        "filename": "characters.md",
        "label": "人物",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "continuity": {
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
        "filename": "continuity.md",
        "label": "连续性",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "dialogue": {
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
        "filename": "dialogue.md",
        "label": "对话",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "narrative": {
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
        "filename": "narrative.md",
        "label": "叙事",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "pacing": {
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
        "filename": "pacing.md",
        "label": "节奏",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "plot": {
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
        "filename": "plot.md",
        "label": "剧情",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "style": {
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
        "filename": "style.md",
        "label": "文风",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "themes": {
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
        "filename": "themes.md",
        "label": "主题 / 价值观",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      },
      "worldbuilding": {
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
        "filename": "worldbuilding.md",
        "label": "世界观",
        "source": "ORIGINAL_FOUNDATION_PROPOSAL"
      }
    },
    "book_id": "original-e56a54687506",
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
    "edition_id": "base",
    "hard_constraints": {
      "must": [],
      "must_not": []
    },
    "history": [
      {
        "changes": [],
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "profile_version_id": "book-profile-proposal-e39fee0d664e4e06923df0f31beee8eb",
        "reason": "作者确认故事基础方案",
        "version_number": 1
      }
    ],
    "inherited_from_edition_id": null,
    "profile_version_id": "book-profile-proposal-e39fee0d664e4e06923df0f31beee8eb",
    "proposals": [],
    "version_number": 1
  },
  "ending_state": "重排结束后，测距带两端仍指向同一面墙，但那面墙上多出一扇原本不存在的门，广播从门内报出沈砚尚未说出口的楼层。",
  "experience_target": {
    "action_space_delta": "",
    "core_promise_delivery": "",
    "emotional_outcome": "重排结束后，测距带两端仍指向同一面墙，但那面墙上多出一扇原本不存在的门，广播从门内报出沈砚尚未说出口的楼层。",
    "ending_mode": "CONSEQUENCE",
    "event_source": "沈砚在第一次提前重排中卡在两段互不相连的楼梯之间，半瓶水和一块能记录路线的旧标牌落在对面，门外的蓝色楼层标记却出现在不可能的位置。",
    "knowledge_delta": "",
    "outcome_magnitude": "",
    "protagonist_strategy": "把当天唯一机会用在让测距带保留墙面关系，还是用在让手电照亮危险落脚点。",
    "relationship_delta": "",
    "risk_form": "断梯、缺水、不断变化的空间和互相矛盾的广播同时逼近，任何选择都会放弃另一种即时保障。",
    "scene_topology": "沈砚在第一次提前重排中卡在两段互不相连的楼梯之间，半瓶水和一块能记录路线的旧标牌落在对面，门外的蓝色楼层标记却出现在不可能的位置。",
    "social_feedback": "用物品质变直接验证空间异常，首章回报是可走的路线和饮水，谜团只作为改变下一次选择的证据出现。",
    "solution_method": "沈砚选择测距带，让它沿测量功能在折叠后仍指向同一段墙面，随后以身体攀爬和逐点记录完成取水。",
    "world_scale_delta": ""
  },
  "forbidden_repetitions": [],
  "genre_alignment": [],
  "genre_drift_diagnostic": {},
  "genre_evolution_diagnostic": {},
  "innovation_commitments": {
    "expected_cross_horizon_synergies": [],
    "expected_element_synergies": [],
    "expected_future_options_opened": [],
    "expected_horizon_roles": {},
    "expected_innovation_elements": [],
    "expected_new_debts": [],
    "expected_payoffs": [],
    "hard_gate_exception": false,
    "minimum_meaningful_delta": null,
    "soft_contract": true
  },
  "innovation_control": {
    "focus": [
      "auto"
    ],
    "level": "medium"
  },
  "innovation_preview": null,
  "innovation_trace": null,
  "kernel_verification_status": "LEGACY_NO_EFFECTIVE_CONTRACT",
  "knowledge_constraints": [
    "不得让角色无依据知晓幕后设定"
  ],
  "lens": "CONTINUITY_ACTIVE_THREAD",
  "mode": "constrained_innovation",
  "must_not_resolve": [
    "不得在首章锁死长期路线或结局"
  ],
  "narrative_debt": {
    "advance": [],
    "fully_pay": [],
    "new_major_hooks_allowed": 1
  },
  "narrative_drive_alignment": {
    "drive_balance": "UNKNOWN",
    "drive_conflicts": [],
    "drives_advanced": [],
    "drives_deferred": [],
    "drives_paid_off": [],
    "evidence": [],
    "primary_drive": null,
    "primary_drive_effect": "",
    "secondary_drive_effects": {}
  },
  "narrative_drive_drift_diagnostic": {},
  "narrative_portfolio": {
    "consecutive_deferrals": 0,
    "current_chapter": 0,
    "long_threads": [],
    "mid_threads": [
      {
        "debt_ids": [],
        "horizon": "MID",
        "last_advanced": 0,
        "lifecycle": "SETUP",
        "maturity": 0.0,
        "maturity_note": "",
        "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "opened_chapter": 0,
        "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
      }
    ],
    "narrative_debts": [],
    "overdue_debt_ids": [],
    "payoff_ready_thread_ids": [],
    "short_threads": [],
    "snapshot_id": "portfolio_8e7be71c73960b621a0e2723",
    "warnings": []
  },
  "novelty_provenance": [],
  "outcome_magnitude_target": "",
  "payoff_channel_impact": [],
  "payoff_plan": {
    "causal_sources": [
      "作者确认的故事基础方案与创作起点"
    ],
    "must_change_behavior": [
      "thread_status:thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
      "character_state:protagonist"
    ],
    "state_changes": [
      "第一件普通物品永久获得跨局部重排保持空间关系的异常能力，沈砚从此拥有一条不能被旧地图解释的路线证据。",
      "重排结束后，测距带两端仍指向同一面墙，但那面墙上多出一扇原本不存在的门，广播从门内报出沈砚尚未说出口的楼层。"
    ]
  },
  "pressure": {
    "before": 0.0,
    "target_after": 35.0
  },
  "primary_function": "setup",
  "primary_thread": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
  "progress": {
    "minimum_score": 25.0,
    "required_irreversible_change": "第一件普通物品永久获得跨局部重排保持空间关系的异常能力，沈砚从此拥有一条不能被旧地图解释的路线证据。"
  },
  "progress_preview": null,
  "progression_debt_impact": [],
  "progression_impact": {
    "ability_showcase": [],
    "ability_unlock": [],
    "axis_advanced": [],
    "bottleneck_change": null,
    "branch_change": null,
    "future_progression_space": [],
    "growth_cost": [],
    "new_ceiling_visibility": [],
    "progression_delta_type": [],
    "resource_change": [],
    "stage_change": null
  },
  "reader_promise_alignment": [],
  "reader_question": "广播说“别相信蓝色楼层”，下一秒蓝色标牌后传来水声，而楼梯的墙面正在向内折。",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "recent_avoid_repetitions": [],
  "reference_provenance": {
    "application_summary": "",
    "card_ids_used": [
      "contrast-ability-rule",
      "contrast-opening-pressure",
      "synth-category-01",
      "synth-category-02",
      "synth-category-03",
      "synth-category-04"
    ],
    "match_tier": "EXACT",
    "reference_strategy_id": null,
    "reuse_reason": null,
    "selected_solutions": [],
    "snapshot_hash": "46df1603ebf368b65ffcc1382bc9720924f8a9e3589c14c1efc80d55908febdf",
    "snapshot_id": "reference-context_2105a33be35a92e8235574a9",
    "usage": "REFERENCE_ONLY"
  },
  "required_cost": "他放弃了当天强化手电的可能，回程只能依靠已有电量和测距带提供的关系判断。",
  "required_irreversible_change": "第一件普通物品永久获得跨局部重排保持空间关系的异常能力，沈砚从此拥有一条不能被旧地图解释的路线证据。",
  "resource_opportunity_impact": [],
  "reveal_agenda": {
    "book_id": "original-e56a54687506",
    "chapter_ordinal": 1,
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
  "rhythm_constraints": {
    "advance_due_promises": [],
    "resolve_due_promises": []
  },
  "scheduler_alignment": {
    "alignment": "UNKNOWN",
    "anticipations_served": [],
    "candidate_primary_intent": null,
    "debts_served": [],
    "deviation_reason": "",
    "recommended_primary_intent": null,
    "risks": []
  },
  "secondary_functions": [],
  "style_constraints": {
    "pov": "第三人称限知",
    "tone_style": "紧张、具体、克制但有爽点"
  },
  "truth_reveal_commitments": {
    "reveal_impact": {
      "character_knowledge_delta": [],
      "full_reveals": [],
      "hints": [],
      "kept_hidden": [],
      "partial_reveals": [],
      "reader_knowledge_delta": [],
      "secrets_used": []
    },
    "rule": "Hidden Truth 只作为行为约束；未获 Agenda 授权不得向读者或角色揭示。",
    "truth_alignment": []
  },
  "verified_kernel_trace": {},
  "world_expansion_impact": []
}
```

## Reference Corpus Prose Controls（REFERENCE_ONLY soft context）

以下内容只影响表达方式，不得改变 Chapter Contract、Canon、Boundary、状态、选择、事件顺序、线索、payoff、不可逆改变或结尾状态；发生冲突时丢弃 Prose Guidance。
当前书 Prose DNA 与作者明确风格意图优先于外部 Reference Corpus Prose Controls。

```json
{
  "controls": [
    {
      "applicable_scene_functions": [
        "ACTION",
        "OPENING",
        "EXPLORATION",
        "PAYOFF"
      ],
      "card_id": "prose-control-action-before-interpretation",
      "card_type": "prose-control",
      "control_topic": "动作先于解释",
      "failure_signals": [
        "技能名、境界、术语和抽象胜利宣告排成清单。",
        "为追求速度删除所有空间位置和反馈。"
      ],
      "guidance": "先让位置、目标、触发、操作、身体反应或环境反馈发生，再补当前场景真正需要的规则和意义。",
      "transfer_boundary": "只迁移动作承载信息的抽象变量，不迁移来源人物、事件、专名、句式或口吻。",
      "variants": [
        "战斗用距离、方向、出手、反制和伤害呈现过程。",
        "专业操作用观察、判断、指令、操作和结果呈现过程。",
        "调查、谈判和公共行动也要保留目标、反馈与后果链。"
      ],
      "when_to_use": [
        "读者只能复述能力名称或胜负结论，无法复述现场发生了什么。",
        "说明段开始脱离人物当下的操作、判断或风险。"
      ]
    },
    {
      "applicable_scene_functions": [
        "EXPOSITION",
        "DIALOGUE",
        "OPENING",
        "ACTION"
      ],
      "card_id": "prose-control-exposition-anchored-in-need",
      "card_type": "prose-control",
      "control_topic": "由场景需要锚定说明",
      "failure_signals": [
        "先把百科讲完，再寻找场景来承载它。",
        "以首先、其次、最后替代当前场景的真实因果顺序。"
      ],
      "guidance": "让规则、历史、世界、机构或专业知识由当前问题、门槛、任务、物件、报告、对话或身体反馈触发，并回到人物的选择、操作或认知变化。",
      "transfer_boundary": "只迁移让说明服从人物需要的抽象控制，不迁移来源世界、机构、术语、专名或解释段句式。",
      "variants": [
        "门槛型在角色需要通过资格、交易或规则时出现。",
        "物件型用器械、文件、资源或屏幕让抽象规则可见。",
        "专业型用病例、流程、数据或操作验证说明。"
      ],
      "when_to_use": [
        "背景段脱离 POV，读者不知道信息会改变什么。",
        "连续抽象名词没有回到人物当前的任务或风险。"
      ]
    }
  ],
  "knowledge_gaps": [],
  "machine_bundle_hash": "3120e088142f5d75ad3f2d1d18eca36f5b89251369228b4f73c7f63e796ff9f9",
  "package_schema_version": "reference-corpus-machine-package-v1",
  "purpose": "PROSE",
  "selected_card_count": 2,
  "selected_card_ids": [
    "prose-control-action-before-interpretation",
    "prose-control-exposition-anchored-in-need"
  ],
  "selected_card_types": [
    "prose-control",
    "prose-control"
  ],
  "snapshot_hash": "6a2054bd4b70c7dda3db2005989494cb890c3d20ab9c4e298d3a8c017d378dfc",
  "snapshot_id": "reference-context_1346dea5c0f982baf04d3a2c",
  "snapshot_path": "C:\\dev\\小说续写系统\\audit\\experiments\\v3_10_chapter_continuation_expansion\\browser_smoke_20260816\\library\\original-e56a54687506\\editions\\base\\operations\\draft-task_7ff942998af9bb352a54375b\\input\\reference_context_snapshot.json",
  "status": "ENABLED",
  "usage": "REFERENCE_ONLY",
  "warnings": []
}
```

## Runtime Context Router（hard boundary + earned surface + soft controls）

```json
{
  "baseline_recall_candidates": [],
  "book_id": "original-e56a54687506",
  "character_voice_profiles": [],
  "continuity_candidates": [],
  "craft_controls": [],
  "distill_reference": null,
  "distillation_soft_context": null,
  "earned_surface": null,
  "edition_id": "base",
  "effective_runtime_state": null,
  "hard_boundary": {
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
    "active_threads": [
      {
        "book_id": "original-e56a54687506",
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "dependencies_json": "[]",
        "edition_id": "base",
        "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "importance": 1.0,
        "introduced_chapter": null,
        "last_advanced_chapter": null,
        "payload_json": "{\"foundation_candidate_id\": \"foundation-folded-tower\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"route_id\": \"route-space-reading\", \"stakes\": \"建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "setup",
        "progress": 0.0,
        "reader_visibility": 1.0,
        "source_span_id": null,
        "stakes": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
        "status": "APPROVED_OUTLINE",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
        "version": 1
      }
    ],
    "author_directives": [
      {
        "book_id": "original-e56a54687506",
        "content": "整体紧张、具体、克制，但每次明确的能力验证要给出可感知的爽点。",
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "directive_id": "directive-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-preference-1",
        "directive_type": "preference",
        "edition_id": "base",
        "mode": "persistent",
        "priority": 100,
        "source": "AUTHOR_CONFIRMED_FOUNDATION",
        "status": "ACTIVE",
        "version": 1
      }
    ],
    "base_event_seq": 0,
    "base_projection_hash": "0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448",
    "batch_anchor": {},
    "book_id": "original-e56a54687506",
    "canon_facts": {},
    "capabilities": {},
    "character_states": {},
    "current_position": {
      "last_canon_chapter": 0,
      "next_chapter": 1
    },
    "earlier_summaries": [],
    "edition_id": "base",
    "hook_diagnostics": {
      "advance_due": [],
      "as_of_chapter": 0,
      "book_id": "original-e56a54687506",
      "edition_id": "base",
      "hold": [],
      "overdue": [],
      "queues": {
        "ADVANCE": [],
        "HOLD": [],
        "OVERDUE": [],
        "RESOLVE": []
      },
      "resolve_due": []
    },
    "innovation_control": {
      "focus": [
        "auto"
      ],
      "level": "medium"
    },
    "innovation_diagnostics": {
      "open_novelty_debt": [],
      "portfolio_snapshot": {
        "consecutive_deferrals": 0,
        "current_chapter": 0,
        "long_threads": [],
        "mid_threads": [
          {
            "debt_ids": [],
            "horizon": "MID",
            "last_advanced": 0,
            "lifecycle": "SETUP",
            "maturity": 0.0,
            "maturity_note": "",
            "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
            "opened_chapter": 0,
            "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
          }
        ],
        "narrative_debts": [],
        "overdue_debt_ids": [],
        "payoff_ready_thread_ids": [],
        "short_threads": [],
        "snapshot_id": "portfolio_8e7be71c73960b621a0e2723",
        "warnings": []
      },
      "question_balance": {
        "answered": 0,
        "materially_advanced": 0,
        "newly_opened": 0,
        "over_deferred": false,
        "partially_paid": 0,
        "penalty": 0.0
      },
      "recent_pattern_distance": "medium",
      "recommendation": {
        "evidence": [
          "active_threads",
          "recent_structures",
          "earned_surface.available_payoffs"
        ],
        "pattern_distance": "medium",
        "reason": [
          "最近窗口结构差异为 medium，仅作为软规划信号",
          "当前存在 1 个活跃线程、0 个开放设置"
        ],
        "recommended_focus": [
          "world",
          "character"
        ]
      },
      "repeated_patterns": [],
      "semantic_policy_leak": null,
      "window_chapters": []
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 0,
      "long_threads": [],
      "mid_threads": [
        {
          "debt_ids": [],
          "horizon": "MID",
          "last_advanced": 0,
          "lifecycle": "SETUP",
          "maturity": 0.0,
          "maturity_note": "",
          "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
          "opened_chapter": 0,
          "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
        }
      ],
      "narrative_debts": [],
      "overdue_debt_ids": [],
      "payoff_ready_thread_ids": [],
      "short_threads": [],
      "snapshot_id": "portfolio_8e7be71c73960b621a0e2723",
      "warnings": []
    },
    "packet_id": "boundary_259d824b858568b09c2a05fd",
    "promises": {},
    "recent_full_chapters": [],
    "recent_payoffs": {},
    "recent_structures": [],
    "relationships": {},
    "relevant_source_spans": [],
    "resources": {},
    "reveal_agenda": {
      "book_id": "original-e56a54687506",
      "chapter_ordinal": 1,
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
    "rhythm_diagnostics": {
      "analyzer_versions": {
        "deterministic": "rhythm-deterministic-v1",
        "semantic": "rhythm-semantic-v1"
      },
      "as_of_chapter": 0,
      "as_of_event_seq": 0,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T16:22:43.816794+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 0,
        "mode": null,
        "severity": "NONE"
      },
      "ending_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "evidence": [],
      "high_emotion_streak": {
        "bands": [],
        "climax_bonus": 2,
        "count": 0,
        "severity": "NONE"
      },
      "hooks": {
        "advance_due": [],
        "overdue": [],
        "resolve_due": []
      },
      "opening_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "projection_hash": "0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_aaf105266066ce01400a3c7c",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.0,
        "series_markers": [],
        "severity": "NONE"
      }
    },
    "rhythm_features": [],
    "story_atlas_anchor": {},
    "style_profiles": [],
    "warnings": []
  },
  "hard_constraints": {
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
    "active_threads": [
      {
        "book_id": "original-e56a54687506",
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "dependencies_json": "[]",
        "edition_id": "base",
        "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "importance": 1.0,
        "introduced_chapter": null,
        "last_advanced_chapter": null,
        "payload_json": "{\"foundation_candidate_id\": \"foundation-folded-tower\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"route_id\": \"route-space-reading\", \"stakes\": \"建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "setup",
        "progress": 0.0,
        "reader_visibility": 1.0,
        "source_span_id": null,
        "stakes": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
        "status": "APPROVED_OUTLINE",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
        "version": 1
      }
    ],
    "author_directives": [
      {
        "book_id": "original-e56a54687506",
        "content": "整体紧张、具体、克制，但每次明确的能力验证要给出可感知的爽点。",
        "created_at": "2026-08-16T16:22:26.798563+00:00",
        "directive_id": "directive-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-preference-1",
        "directive_type": "preference",
        "edition_id": "base",
        "mode": "persistent",
        "priority": 100,
        "source": "AUTHOR_CONFIRMED_FOUNDATION",
        "status": "ACTIVE",
        "version": 1
      }
    ],
    "base_event_seq": 0,
    "base_projection_hash": "0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448",
    "batch_anchor": {},
    "book_id": "original-e56a54687506",
    "canon_facts": {},
    "capabilities": {},
    "character_states": {},
    "current_position": {
      "last_canon_chapter": 0,
      "next_chapter": 1
    },
    "earlier_summaries": [],
    "edition_id": "base",
    "hook_diagnostics": {
      "advance_due": [],
      "as_of_chapter": 0,
      "book_id": "original-e56a54687506",
      "edition_id": "base",
      "hold": [],
      "overdue": [],
      "queues": {
        "ADVANCE": [],
        "HOLD": [],
        "OVERDUE": [],
        "RESOLVE": []
      },
      "resolve_due": []
    },
    "innovation_control": {
      "focus": [
        "auto"
      ],
      "level": "medium"
    },
    "innovation_diagnostics": {
      "open_novelty_debt": [],
      "portfolio_snapshot": {
        "consecutive_deferrals": 0,
        "current_chapter": 0,
        "long_threads": [],
        "mid_threads": [
          {
            "debt_ids": [],
            "horizon": "MID",
            "last_advanced": 0,
            "lifecycle": "SETUP",
            "maturity": 0.0,
            "maturity_note": "",
            "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
            "opened_chapter": 0,
            "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
          }
        ],
        "narrative_debts": [],
        "overdue_debt_ids": [],
        "payoff_ready_thread_ids": [],
        "short_threads": [],
        "snapshot_id": "portfolio_8e7be71c73960b621a0e2723",
        "warnings": []
      },
      "question_balance": {
        "answered": 0,
        "materially_advanced": 0,
        "newly_opened": 0,
        "over_deferred": false,
        "partially_paid": 0,
        "penalty": 0.0
      },
      "recent_pattern_distance": "medium",
      "recommendation": {
        "evidence": [
          "active_threads",
          "recent_structures",
          "earned_surface.available_payoffs"
        ],
        "pattern_distance": "medium",
        "reason": [
          "最近窗口结构差异为 medium，仅作为软规划信号",
          "当前存在 1 个活跃线程、0 个开放设置"
        ],
        "recommended_focus": [
          "world",
          "character"
        ]
      },
      "repeated_patterns": [],
      "semantic_policy_leak": null,
      "window_chapters": []
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 0,
      "long_threads": [],
      "mid_threads": [
        {
          "debt_ids": [],
          "horizon": "MID",
          "last_advanced": 0,
          "lifecycle": "SETUP",
          "maturity": 0.0,
          "maturity_note": "",
          "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
          "opened_chapter": 0,
          "thread_id": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
        }
      ],
      "narrative_debts": [],
      "overdue_debt_ids": [],
      "payoff_ready_thread_ids": [],
      "short_threads": [],
      "snapshot_id": "portfolio_8e7be71c73960b621a0e2723",
      "warnings": []
    },
    "packet_id": "boundary_259d824b858568b09c2a05fd",
    "promises": {},
    "recent_full_chapters": [],
    "recent_payoffs": {},
    "recent_structures": [],
    "relationships": {},
    "relevant_source_spans": [],
    "resources": {},
    "reveal_agenda": {
      "book_id": "original-e56a54687506",
      "chapter_ordinal": 1,
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
    "rhythm_diagnostics": {
      "analyzer_versions": {
        "deterministic": "rhythm-deterministic-v1",
        "semantic": "rhythm-semantic-v1"
      },
      "as_of_chapter": 0,
      "as_of_event_seq": 0,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T16:22:43.816794+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 0,
        "mode": null,
        "severity": "NONE"
      },
      "ending_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "evidence": [],
      "high_emotion_streak": {
        "bands": [],
        "climax_bonus": 2,
        "count": 0,
        "severity": "NONE"
      },
      "hooks": {
        "advance_due": [],
        "overdue": [],
        "resolve_due": []
      },
      "opening_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "projection_hash": "0abb455305413d32981f6981a8fc510c98cdecdbe70c6861dda1b79c6e3f1448",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_aaf105266066ce01400a3c7c",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.0,
        "series_markers": [],
        "severity": "NONE"
      }
    },
    "rhythm_features": [],
    "story_atlas_anchor": {},
    "style_profiles": [],
    "warnings": []
  },
  "literary_arcs": [],
  "observations": [],
  "request": {
    "chapter_range": null,
    "dimensions": [],
    "include_runtime_state": true,
    "purpose": "draft",
    "reference_scope": null,
    "related_entity_ids": [],
    "runtime_uses": [],
    "subject_ids": []
  },
  "runtime_state_enabled": true,
  "theme_questions": [],
  "warnings": [
    "当前 Edition 没有 Distill Package；仅提供 hard boundary/earned surface"
  ]
}
```

本次是 Full Runtime Draft：Runtime 只能影响角色行动和规划兑现，不得把工程字段写进小说正文。