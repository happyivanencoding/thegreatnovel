# 章节正文任务 `draft-task_34d273bc851ea4fec36bb22f`

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
    "测距带永久获得跨窄缝保留相邻墙面关系的可验证进化，检修窗成为已确认但危险的向外路线。",
    "沈砚在检修窗上留下测距带的第二个固定端点，确认楼外风向真实，却看见相邻塔体之间没有地面。"
  ],
  "micro_event_rule": "允许只改变人物感知、动作或场面反应的 realization-only micro-event；不得改变 Contract、Canon、Knowledge、Resource 或 Capability。",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "target_scene_count": 3,
  "target_word_range": [
    1565,
    3491
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

# Continuation Boundary Packet `boundary_d7669388731f2eeb442716de`

- book_id: `original-e56a54687506`
- base_event_seq: 8
- projection_sha256: `65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050`
- current_position: {"last_canon_chapter": 1, "next_chapter": 2}

## 最近完整章节

### ## 第1章 第一章 墙还在，路没了

source_span_id: `canon-span_96f6a1794bf43a1659c7fba2`

## 第1章 第一章 墙还在，路没了

水声是从楼梯下面传上来的。

沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。

楼道深处的广播忽然响了。

先是一阵短促的电流声，接着，女人的声音隔着厚重的墙传出来，平平的，没有高低起伏。

“别相信蓝色楼层。”

声音断了。

下一秒，水声又响了一遍，比刚才清楚。就在他右手边那段本来应该通往下层的楼梯后面。

沈砚抬起手电。楼梯在四天前还是连续的，从二十层设备夹层往下，经过一个有消防窗的转角，再到十七层的空中连廊。现在中间少了两级，下面的半截楼梯横着嵌进另一面墙，扶手从缝里伸出来，像一根被硬掰弯的肋骨。

对面悬着一块蓝色标牌，边角已经磕掉，白色的十七两个数字斜在漆面上。标牌下方是一小块还没塌掉的平台，半瓶水和一块旧的铝制指示牌躺在灰尘里。

水瓶离他不到三米。中间却没有地面。

沈砚蹲下来，把手电放在膝边，摸出测距带。金属外壳上有一道贯穿的凹痕，是他在灾变后的第二天从门框里撬出来的。带钩的那一头还能正常弹回，卡扣也没有松。他把带子拉出两米，贴着脚边的台阶量了一次，又抬头看向对面。

两段楼梯的断口相隔一百九十七厘米。这个数字他记得很牢。昨天晚上，他曾用鞋底和墙缝反复核过，误差不会超过两厘米。今天缝隙变宽了，原来能碰到的扶手已经退到对面平台边缘。

广播没有再说话。水声从蓝色标牌后面持续传来，细而急，像有人把一只瓶子倒扣在铁盆里。

他先看了看手电。电量只剩最后一格，光线在墙上发虚。再看测距带，带身上的黑色刻度被灰尘填了一半，仍然能读。

那种说不清的感觉在掌心里出现了。不是发热，也不是麻，更像有一根看不见的细线从物品内部绷出来，等着他把手指按在某个决定上。

一天只能选一个。

如果选手电，落脚点会亮得更久，至少能看清对面平台有没有空洞；如果选测距带，他也许能留下这段错乱空间的关系。手电能让他看见下一步，测距带却可能让他记住下一次重排之后的这一步。

沈砚把手放在手电上，停了一会儿，又移向测距带。

金属外壳在他掌心里轻轻一震。

没有光，没有声音。带钩的薄片依旧是那副磨花的样子，刻度也没有增加。沈砚只觉得那道贯穿外壳的凹痕像被什么东西从里面重新压实了一遍。他没有等它给出更多动静，把带钩的一端扣进自己脚边墙角裸露的钢筋，带壳的一端压在身后的墙根。

他拉出三米。

带身横过断口，悬在两段楼梯之间。

“二点九四。”他低声报出读数，用指甲在墙面上刮出一道短痕。

水声突然停了。

楼体深处传来一声沉闷的错动，像大船在水下翻了个身。台阶先往下沉，再往上顶。沈砚的肩膀撞上墙，手电从膝边滚出去，光柱斜斜地照进断口。

第一道裂缝从蓝色标牌下方出现。对面的平台没有向后退，它朝他折了过来。墙上的瓷砖一块接一块错开，边缘擦出白色粉末；那块十七层的标牌被挤得翻转，蓝色的一面朝向他，像一只迟到的眼睛。

沈砚想收回测距带，带身却没有顺着缝隙缩短。

他握住外壳，感觉到另一头的钩子还扣在钢筋上。墙角正在移动，钢筋的位置已经不可能与原来的墙角重合，可带子的张力没有变。刻度线上，二点九四仍然对着他刚才刮下的那道痕。

楼梯在这时彻底断开。

他被挤到半级台阶上，脚下只剩一块三十厘米宽的水泥边。对面平台近了一瞬，又被墙面带着向侧方滑去。半瓶水沿着铝牌滚了两圈，停在平台边缘。

沈砚没有去追。手电的光照不到那里，身体也没有余力让他跳过去。他只把测距带绷紧，顺着带身确认两面墙的关系：身后的墙角在左，带钩的墙面在右；中间的距离仍是二点九四。空间在变，关系没有散。

这已经够了。

他收起手电，先用左脚探向对面。鞋底碰到的是平台外沿，不是空处。测距带在掌心里发出极轻的颤动，带钩那一端指向的墙面没有偏。沈砚慢慢伏低身体，胸口贴过断口，右手抓住翻起的扶手。

墙里传来细碎的摩擦声。仿佛整座楼正在把一张纸折成更小的形状，而他只是纸上的一粒砂。

他不敢抬头，沿着那条已经被测距带固定下来的关系一点点挪。膝盖先落地，肩膀再过去，最后才把腿拖上平台。水瓶就在手边。他抓住瓶颈，先拧开瓶盖，喝了一口。水是温的，带着塑料味，却让喉咙里那层干硬的砂纸软了下去。

他没有一口气喝完，只把剩下的半瓶水塞进外套内袋。

旧铝牌压在水瓶下面。沈砚把它翻过来，背面有几道被人用硬物刻出的线：一条直线，两次折返，末端钉着一个小小的圆点。圆点旁边还有一行已经磨掉一半的数字，看不出是十七还是一七。

他用袖口擦掉灰，把铝牌夹在腰侧。没有时间判断这些线是谁留下的，也没有时间猜它们指向哪里。至少它们能证明，刚才那段路不是他在黑暗里记错了。

身后的墙突然安静下来。

安静得太快。

沈砚抓住测距带，准备沿原路回去。带壳的一端仍压在他身后的墙根，带钩的一端却不再悬在断口对面。两端都贴着同一面灰墙，一左一右，之间隔着完整的二点九四米。刚才那两段互不相连的楼梯不见了，脚下只剩一块狭窄的楼面，墙面平整地立在前方。

那面墙上多了一扇门。

门框没有灰尘，像是刚从墙里长出来。没有猫眼，没有把手旁的编号，只有一条窄窄的黑缝，从门后漏出冷风。冷风里混着潮湿的土腥味，和他刚喝下去的水一样真实。

沈砚没有靠近。

广播就在门内响起。

电流声比之前更近，近得像有人把嘴贴在门板另一侧。

“十七层。”

他还没说出这个数字。

沈砚低头看着测距带。两端的刻度同时指向那面墙，二点九四没有改变。门却在墙上，门后有什么也没有给出解释。

他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。

门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。

这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。


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
{
  "post-rearrangement-door": {
    "_edition_id": "base",
    "_event_id": "event_1f1743812945cdf22326c4d3",
    "_event_seq": 4,
    "_source_id": "draft_8bb76c611125c76689997a74",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "description": "重排结束后，原本平整的墙面出现一扇没有编号的门；门内广播报出十七层。",
    "fact_id": "post-rearrangement-door",
    "knowledge_status": "UNKNOWN",
    "location_relation": "same_wall_as_measuring_tape",
    "object": "原本平整的墙面出现一扇没有编号的门，门内广播报出十七层。",
    "predicate": "observed_after_rearrangement",
    "source_draft_id": "draft_8bb76c611125c76689997a74",
    "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
    "status": "observed"
  }
}
```

## 人物状态

```json
{
  "protagonist-local-evidence-choice": {
    "_edition_id": "base",
    "_event_id": "event_a80ff58c44e66e2dc777f43a",
    "_event_seq": 6,
    "_source_id": "draft_8bb76c611125c76689997a74",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "change": "在缺乏完整证据时选择以测距带保留空间关系，放弃强化手电的即时照明收益。",
    "character_id": "protagonist",
    "cost": "手电在回程前耗尽，后续行动依靠已有电量和测距带提供的关系判断。",
    "source_draft_id": "draft_8bb76c611125c76689997a74",
    "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
    "state_id": "protagonist-local-evidence-choice"
  }
}
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
  },
  {
    "book_id": "original-e56a54687506",
    "created_at": "2026-08-16T16:39:36.675398+00:00",
    "dependencies_json": "[]",
    "edition_id": "base",
    "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
    "importance": 0.5,
    "introduced_chapter": "1",
    "last_advanced_chapter": "1",
    "payload_json": "{\"evidence\": \"沈砚获得测距带保留的墙面关系、取回饮水并带走刻有折返线的旧铝牌。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"setup\", \"source_draft_id\": \"draft_8bb76c611125c76689997a74\", \"source_span_id\": \"canon-span_96f6a1794bf43a1659c7fba2\", \"stakes\": \"建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
    "phase": "setup",
    "progress": 0.0,
    "reader_visibility": 0.5,
    "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
    "stakes": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
    "status": "CANON",
    "target_payoff_max": null,
    "target_payoff_min": null,
    "thread_id": "space-reading-route-evidence",
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
{
  "water-half-bottle-recovered": {
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
  }
}
```

## 能力

```json
{
  "measuring-tape-space-relation": {
    "_edition_id": "base",
    "_event_id": "event_0c50697347ecb8094273da84",
    "_event_seq": 2,
    "_source_id": "draft_8bb76c611125c76689997a74",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "capability_id": "measuring-tape-space-relation",
    "character_id": "protagonist",
    "description": "测距带在局部空间重排后仍保持两端对同一墙面的测量关系，已形成一条可复核的异常路线证据。",
    "evidence": "正文中二点九四米的两端关系在楼梯断开、墙面折叠和重排后仍保持。",
    "name": "测距带跨局部重排保持空间关系",
    "object_id": "measuring-tape",
    "owner_id": "protagonist",
    "source_draft_id": "draft_8bb76c611125c76689997a74",
    "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
    "status": "ACTIVE"
  }
}
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
[
  {
    "book_id": "original-e56a54687506",
    "candidate_id": "genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape",
    "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
    "created_at": "2026-08-16T16:39:36.675398+00:00",
    "edition_id": "base",
    "emotional_outcome": null,
    "ending_type": null,
    "event_source": null,
    "ordinal": 1,
    "payload_json": "{\"candidate_id\": \"genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape\", \"signature\": \"function:setup\", \"source_draft_id\": \"draft_8bb76c611125c76689997a74\", \"source_span_id\": \"canon-span_96f6a1794bf43a1659c7fba2\", \"structure_tags\": [\"function:setup\"], \"tag_id\": \"repetition_632fb4e8d7d6c1e533b6e361\"}",
    "payoff_type": null,
    "scene_topology": null,
    "solution_method": null,
    "status": "CANON",
    "tag_id": "repetition_632fb4e8d7d6c1e533b6e361",
    "version": 1
  }
]
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
[
  {
    "analyzer_version": "rhythm-deterministic-v1",
    "book_id": "original-e56a54687506",
    "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
    "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
    "created_at": "2026-08-16T16:39:36.727311+00:00",
    "edition_id": "base",
    "effective_content_sha256": "81b9f177e416edf8a46c35623764c76937a4fb7980d8b1b51b196ef49db80d95",
    "emotional_confidence": null,
    "emotional_intensity_band": "UNKNOWN",
    "ending_excerpt_prose": "他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。",
    "ending_excerpt_raw": "他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。",
    "ending_fingerprint_prose": "1924ea959863f00652dddd0c4c4d61a05784c50e5108db44be778d5151c3382e",
    "ending_fingerprint_raw": "1924ea959863f00652dddd0c4c4d61a05784c50e5108db44be778d5151c3382e",
    "ending_mode": "unknown",
    "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
    "extractor_kind": "DETERMINISTIC",
    "feature_id": "chapter-feature_2bb1dd243ed8a5483903dd99",
    "function_confidence": null,
    "invalidated_at": null,
    "normalized_title": "第一章 墙还在,路没了",
    "opening_excerpt_prose": "水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。\n\n楼道深处的广播忽然响了。",
    "opening_excerpt_raw": "## 第1章 第一章 墙还在，路没了\n\n水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。",
    "opening_fingerprint_prose": "618980928bd9e630059135a185a34a349f7832d8b8f4eaf99307404186ab6df6",
    "opening_fingerprint_raw": "75e306dff933f76d4672117946feace2a6259fe619374434e6c62b94e75d6f2e",
    "opening_mode": "unknown",
    "ordinal": 1,
    "planned_primary_function": null,
    "realized_primary_function": null,
    "status": "ACTIVE",
    "title_fingerprint": "aff139a5768f80cb9b1ad5b463db9b4619f825a589d771b2c72741effa1efefb",
    "title_raw": "## 第1章 第一章 墙还在，路没了",
    "version": 1
  }
]
```

## 长跨度节奏诊断

```json
{
  "analyzer_versions": {
    "deterministic": "rhythm-deterministic-v1",
    "semantic": "rhythm-semantic-v1"
  },
  "as_of_chapter": 1,
  "as_of_event_seq": 8,
  "book_id": "original-e56a54687506",
  "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
  "created_at": "2026-08-16T16:39:36.864621+00:00",
  "edition_id": "base",
  "ending_mode_streak": {
    "count": 1,
    "mode": "unknown",
    "severity": "NONE"
  },
  "ending_similarity": {
    "matching_chapters": [],
    "max_similarity_last_4": 0.0,
    "severity": "NONE"
  },
  "evidence": [
    {
      "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 1
    }
  ],
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
  "projection_hash": "65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050",
  "same_function_streak": {
    "count": 0,
    "function": null,
    "severity": "NONE",
    "source": "planned_primary_function"
  },
  "snapshot_id": "rhythm-snapshot_22d699e14337cc8178b4666f",
  "title_repetition": {
    "exact_duplicates": [],
    "matching_chapters": [],
    "max_similarity_last_20": 0.0,
    "series_markers": [
      null
    ],
    "severity": "NONE"
  }
}
```

## 伏笔动作队列

```json
{
  "advance_due": [],
  "overdue": [],
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
  "chapter_ordinal": 2,
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
    "current_chapter": 1,
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
      },
      {
        "debt_ids": [],
        "horizon": "MID",
        "last_advanced": 1,
        "lifecycle": "SETUP",
        "maturity": 0.0,
        "maturity_note": "",
        "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "opened_chapter": 1,
        "thread_id": "space-reading-route-evidence"
      }
    ],
    "narrative_debts": [],
    "overdue_debt_ids": [],
    "payoff_ready_thread_ids": [],
    "short_threads": [],
    "snapshot_id": "portfolio_dd13a40ba418bba06c0e6c4b",
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
  "recent_pattern_distance": "high",
  "recommendation": {
    "evidence": [
      "active_threads",
      "recent_structures",
      "earned_surface.available_payoffs"
    ],
    "pattern_distance": "high",
    "reason": [
      "最近窗口结构差异为 high，仅作为软规划信号",
      "当前存在 2 个活跃线程、0 个开放设置"
    ],
    "recommended_focus": [
      "character",
      "mechanism"
    ]
  },
  "repeated_patterns": [],
  "semantic_policy_leak": null,
  "window_chapters": [
    1
  ]
}
```

## 警告

```json
[]
```


## Chapter Contract

```json
{
  "action_space_delta_target": "从室内折返路线扩展到能观察楼外的检修窗，但无法直接离楼。",
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
  "boundary_packet_id": "boundary_d7669388731f2eeb442716de",
  "candidate_id": "candidate_081191a0e08eeba0e21fd5fa",
  "canon_constraints": [],
  "chapter": 2,
  "chapter_intent": "用一次可见的空间关系验证把第一章的测距带能力推进到楼外边界，同时保留广播身份与建筑成因未知。",
  "commit_updates": [
    "测距带在重排缝隙中保留第二种局部墙面关系",
    "沈砚确认一处可复核的楼外风光入口",
    "主线程从寻找广播方向推进为掌握一条向外的局部路线",
    "测距带永久获得跨窄缝保留相邻墙面关系的可验证进化，检修窗成为已确认但危险的向外路线。"
  ],
  "continuation_boundary": {
    "base_event_seq": 8,
    "base_projection_hash": "65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050",
    "batch_anchor": {},
    "last_canon_chapter": 1,
    "story_atlas_anchor": {}
  },
  "contract_id": "contract_c010403488e79542701e00d4",
  "declared_kernel_trace": {
    "anticipation_impact": [],
    "drive_drift": {},
    "genre_drift": {},
    "genre_evolution": {},
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
    "payoff_channel_impact": [],
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
    "resource_impact": [],
    "scheduler_alignment": {
      "alignment": "UNKNOWN",
      "anticipations_served": [],
      "candidate_primary_intent": null,
      "debts_served": [],
      "deviation_reason": "",
      "recommended_primary_intent": null,
      "risks": []
    },
    "world_expansion_impact": []
  },
  "dramatization_targets": [
    "测距带永久获得跨窄缝保留相邻墙面关系的可验证进化，检修窗成为已确认但危险的向外路线。",
    "沈砚在检修窗上留下测距带的第二个固定端点，确认楼外风向真实，却看见相邻塔体之间没有地面。"
  ],
  "effective_book_profile": {
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
  "ending_state": "沈砚在检修窗上留下测距带的第二个固定端点，确认楼外风向真实，却看见相邻塔体之间没有地面。",
  "experience_target": {
    "action_space_delta": "从室内折返路线扩展到能观察楼外的检修窗，但无法直接离楼。",
    "core_promise_delivery": "普通测量工具沿原功能质变，直接把无路处变成可验证的外向路线。",
    "emotional_outcome": "第一次看到不依赖广播的楼外灰光，获得可验证的前进方向，同时意识到窗口外还有更大的空间风险。",
    "ending_mode": "CONSEQUENCE",
    "event_source": "建筑再次重排，断梯边出现短暂的风压和窄缝；广播给出相反方向的楼层提示。",
    "knowledge_delta": "确认风和灰光来自真实外部空间；广播楼层提示仍不可信。",
    "outcome_magnitude": "中等范围的空间出口确认",
    "protagonist_strategy": "把可观察的风、光和距离放在广播之前，接受只验证一个空间缺口，不同时追声和取水。",
    "relationship_delta": "与广播的信任关系转为带证据的怀疑。",
    "risk_form": "缝隙会在下一次微重排前缩窄，测距带只能确认局部关系，不能保证人身安全或打开整栋楼的出口。",
    "scene_topology": "断梯边的封闭走廊—窄缝—检修窗—可返回的墙面关系，空间由内向外打开。",
    "social_feedback": "广播随即重复错误楼层提示，声音的可信度下降，但没有给出新的身份答案。",
    "solution_method": "让测距带沿原有测量功能保留墙面两端的关系，先验证缝隙，再把可返回的路线延伸到检修窗。",
    "world_scale_delta": "第一次把相邻建筑和楼外空间带入可行动范围。"
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
  "kernel_verification_status": "PARTIAL",
  "knowledge_constraints": [],
  "lens": "CONTINUITY_ACTIVE_THREAD",
  "mode": "constrained_innovation",
  "must_not_resolve": [
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-16",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-17",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-18",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-19",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-20",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-21",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-22",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-9",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-8",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-7",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-10",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-11",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-12",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-13",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-14",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-15",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-3",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-1",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-4",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-5",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-2",
    "KEEP_HIDDEN:truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-6"
  ],
  "narrative_debt": {
    "advance": [
      "anticipation-thread-1",
      "anticipation-world-earned-spatial-frontier"
    ],
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
    "current_chapter": 1,
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
      },
      {
        "debt_ids": [],
        "horizon": "MID",
        "last_advanced": 1,
        "lifecycle": "SETUP",
        "maturity": 0.0,
        "maturity_note": "",
        "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "opened_chapter": 1,
        "thread_id": "space-reading-route-evidence"
      }
    ],
    "narrative_debts": [],
    "overdue_debt_ids": [],
    "payoff_ready_thread_ids": [],
    "short_threads": [],
    "snapshot_id": "portfolio_dd13a40ba418bba06c0e6c4b",
    "warnings": []
  },
  "novelty_provenance": [
    {
      "causal_source": "第一章已确认的测距带空间关系能力与当前建筑重排压力",
      "conflicts_checked": [
        "不改变每日只能选择一件物品",
        "不把测距带变成万能工具",
        "不确认广播来源"
      ],
      "introduction_event": "第二章现场对窄缝两端的首次验证",
      "new_state_if_committed": "测距带可在局部窄缝变化后保留墙面相邻关系并确认检修窗路线",
      "novelty_boundary": "FORWARD_CANON_COMPATIBLE",
      "provenance": "FORWARD_NOVELTY",
      "retroactive_claim": false
    }
  ],
  "outcome_magnitude_target": "中等范围的空间出口确认",
  "payoff_channel_impact": [],
  "payoff_plan": {
    "causal_sources": [
      "canon capability measuring-tape-space-relation",
      "canon thread space-reading-route-evidence",
      "chapter-1 measured wall relation and recovered water"
    ],
    "must_change_behavior": [
      "测距带在重排缝隙中保留第二种局部墙面关系",
      "沈砚确认一处可复核的楼外风光入口",
      "主线程从寻找广播方向推进为掌握一条向外的局部路线",
      "测距带永久获得跨窄缝保留相邻墙面关系的可验证进化，检修窗成为已确认但危险的向外路线。"
    ],
    "state_changes": [
      "测距带在重排缝隙中保留第二种局部墙面关系",
      "沈砚确认一处可复核的楼外风光入口",
      "主线程从寻找广播方向推进为掌握一条向外的局部路线"
    ]
  },
  "pressure": {
    "before": 61.0,
    "target_after": 69.0
  },
  "primary_function": "discovery",
  "primary_thread": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
  "progress": {
    "minimum_score": 25.0,
    "required_irreversible_change": "测距带永久获得跨窄缝保留相邻墙面关系的可验证进化，检修窗成为已确认但危险的向外路线。"
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
  "reader_question": "建筑重排后，楼外的风和灰光是否能通过一条可复核的空间关系被确认？",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "recent_avoid_repetitions": [],
  "reference_provenance": {
    "application_summary": "按 reader_experiences、narrative_drives、payoff_channels、creative_problem_tags 从冻结卡片中选择 synth-category-05、synth-category-06、synth-category-01；仅迁移可复用机制，当前书事实、状态与最终选择仍由本次合同决定。",
    "card_ids_used": [
      "synth-category-05",
      "synth-category-06",
      "synth-category-01"
    ],
    "match_tier": "EXACT",
    "reference_strategy_id": "planning-reference-strategy_6825f856fb836998e6b614d0",
    "reuse_reason": null,
    "selected_solutions": [],
    "snapshot_hash": "c728ff7f1df54d897b10e5c8e6a78c249cc6493b358dc264b0e1215f66193fea",
    "snapshot_id": "reference-context_d91b3142c5ab62d022f58ee7",
    "usage": "REFERENCE_ONLY"
  },
  "required_cost": "失去当天让其他物品进化的机会，并暴露自己所在楼层与相邻空间的风险。",
  "required_irreversible_change": "测距带永久获得跨窄缝保留相邻墙面关系的可验证进化，检修窗成为已确认但危险的向外路线。",
  "resource_opportunity_impact": [],
  "reveal_agenda": {
    "book_id": "original-e56a54687506",
    "chapter_ordinal": 2,
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
  "secondary_functions": [
    "progress",
    "world_expansion"
  ],
  "style_constraints": {},
  "truth_reveal_commitments": {
    "reveal_impact": {
      "character_knowledge_delta": [],
      "full_reveals": [],
      "hints": [],
      "kept_hidden": [
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-1",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-10",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-11",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-12",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-13",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-14",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-15",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-16",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-17",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-18",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-19",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-2",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-20",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-21",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-22",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-3",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-4",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-5",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-6",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-7",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-8",
        "truth-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-9"
      ],
      "partial_reveals": [],
      "reader_knowledge_delta": [],
      "secrets_used": []
    },
    "rule": "Hidden Truth 只作为行为约束；未获 Agenda 授权不得向读者或角色揭示。",
    "truth_alignment": []
  },
  "verified_kernel_trace": {
    "drive_drift": {
      "evidence": [],
      "hard_failure": false,
      "reasons": [
        "本章未直接服务 Primary Drive；单章缺席不是硬失败"
      ],
      "status": "SOFT_MISS",
      "warning": false
    },
    "evidence_compilation": {
      "candidate_local_id": "route-window-gap",
      "completeness": "PARTIAL",
      "declared": {
        "anticipation_impact": [],
        "drive_drift": {},
        "genre_drift": {},
        "genre_evolution": {},
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
        "payoff_channel_impact": [],
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
        "resource_impact": [],
        "scheduler_alignment": {
          "alignment": "UNKNOWN",
          "anticipations_served": [],
          "candidate_primary_intent": null,
          "debts_served": [],
          "deviation_reason": "",
          "recommended_primary_intent": null,
          "risks": []
        },
        "world_expansion_impact": []
      },
      "differences": [],
      "hard_gate_compilation": {
        "author_constraint_violations": [],
        "canon_conflicts": [],
        "capability_violations": [],
        "knowledge_violations": [],
        "missing_causal_sources": [],
        "payoff_cooldown_violations": [],
        "timeline_conflicts": []
      },
      "soft_metric_compilation": {
        "candidate_score_overrides": {
          "components": {
            "agency_gain": {
              "completeness": "COMPLETE",
              "evidence": [],
              "score": 50.0,
              "source": "KERNEL_VERIFIED_EVIDENCE"
            },
            "debt_utility": {
              "completeness": "COMPLETE",
              "evidence": [],
              "formula": "existing:narrative_debt",
              "score": 0.0,
              "source": "FROZEN_NARRATIVE_DEBT"
            },
            "future_damage": {
              "completeness": "COMPLETE",
              "evidence": [],
              "score": 0.0,
              "source": "KERNEL_VERIFIED_EVIDENCE"
            },
            "progress_gain": {
              "completeness": "COMPLETE",
              "components": {
                "goal_advance": 70.0,
                "knowledge_change": 60.0,
                "permanent_growth": 0.0,
                "relationship_change": 0.0,
                "strategy_expansion": 50.0,
                "world_state_change": 0.0
              },
              "evidence": {
                "goal_advance": [],
                "knowledge_change": [],
                "permanent_growth": [
                  "no_verified_permanent_growth_change"
                ],
                "relationship_change": [
                  "no_verified_relationship_change_change"
                ],
                "strategy_expansion": [],
                "world_state_change": [
                  "no_verified_world_state_change_change"
                ]
              },
              "formula": "existing:progress",
              "score": 27.0,
              "source": "KERNEL_VERIFIED_EVIDENCE"
            },
            "risk_fit": {
              "completeness": "COMPLETE",
              "evidence": [],
              "score": 100.0,
              "source": "KERNEL_VERIFIED_EVIDENCE"
            },
            "thread_need_fit": {
              "completeness": "COMPLETE",
              "evidence": [
                "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower"
              ],
              "score": 100.0,
              "source": "FROZEN_ACTIVE_THREADS"
            }
          },
          "source": "KERNEL_EVIDENCE_COMPILER",
          "values": {
            "agency_gain": 50.0,
            "debt_utility": 0.0,
            "future_damage": 0.0,
            "progress_gain": 27.0,
            "risk_fit": 100.0,
            "thread_need_fit": 100.0
          }
        },
        "progress": {
          "completeness": "COMPLETE",
          "components": {
            "goal_advance": 70.0,
            "knowledge_change": 60.0,
            "permanent_growth": 0.0,
            "relationship_change": 0.0,
            "strategy_expansion": 50.0,
            "world_state_change": 0.0
          },
          "evidence": {
            "goal_advance": [],
            "knowledge_change": [],
            "permanent_growth": [
              "no_verified_permanent_growth_change"
            ],
            "relationship_change": [
              "no_verified_relationship_change_change"
            ],
            "strategy_expansion": [],
            "world_state_change": [
              "no_verified_world_state_change_change"
            ]
          },
          "formula": "existing:progress",
          "score": 27.0,
          "source": "KERNEL_VERIFIED_EVIDENCE"
        },
        "resource_pressure": {
          "completeness": "COMPLETE",
          "components": {
            "cost_income_imbalance": 0.0,
            "current_shortfall": 100.0,
            "near_future_demand": 100.0,
            "reader_salience": 100.0,
            "recently_blocked_actions": 100.0
          },
          "evidence": [
            "missing_resource:真实拥有的普通非生命物品",
            "missing_resource:可执行的现场问题",
            "missing_resource:可进入的现场",
            "missing_resource:足够观察结果的时间",
            "missing_resource:至少一件已验证的进化物品",
            "missing_resource:新的空间压力",
            "bottleneck:可用物品与当前空间缺口不匹配",
            "bottleneck:建筑变化快于主角能完成的现场验证",
            "bottleneck:同一物品的下一次进化需要新的问题而非简单重复"
          ],
          "formula": "existing:resource_pressure",
          "score": 80.0,
          "source": "KERNEL_VERIFIED_EVIDENCE"
        }
      },
      "verified": {
        "drive_drift": {
          "evidence": [],
          "hard_failure": false,
          "reasons": [
            "本章未直接服务 Primary Drive；单章缺席不是硬失败"
          ],
          "status": "SOFT_MISS",
          "warning": false
        },
        "genre_drift": {
          "evidence": [],
          "hard_failure": false,
          "penalty": 4.0,
          "reasons": [
            "移除表层专名后，成长资源、能力与世界层级均不影响因果"
          ],
          "status": "GENRE_SKIN_ONLY",
          "warning": true
        },
        "genre_evolution": {
          "core_promise_preserved": true,
          "evidence": [],
          "explanation": "未检测到需要单独标记的 Genre Evolution",
          "status": "CLEAR"
        },
        "narrative_drive_alignment": {
          "drive_balance": "UNKNOWN",
          "drive_conflicts": [],
          "drives_advanced": [],
          "drives_deferred": [],
          "drives_paid_off": [],
          "evidence": [],
          "primary_drive": "SURVIVAL_RESOURCE",
          "primary_drive_effect": "",
          "secondary_drive_effects": {}
        },
        "payoff_channels": [],
        "progression_impact": {
          "ability_showcases": [],
          "ability_unlocks": [],
          "axis_advanced": [],
          "growth_costs": [],
          "progression_delta_type": [],
          "resource_changes": [],
          "stage_change": null,
          "world_expansion": []
        },
        "reader_promise_alignment": [],
        "resource_impact": [],
        "scheduler_alignment": {
          "alignment": "UNKNOWN",
          "anticipations_served": [],
          "candidate_primary_intent": null,
          "debts_served": [],
          "deviation_reason": "",
          "recommended_primary_intent": null,
          "risks": []
        },
        "world_expansion_impact": []
      },
      "verified_anticipation_impact": [],
      "verified_drive_alignment": {
        "drive_balance": "UNKNOWN",
        "drive_conflicts": [],
        "drives_advanced": [],
        "drives_deferred": [],
        "drives_paid_off": [],
        "evidence": [],
        "primary_drive": "SURVIVAL_RESOURCE",
        "primary_drive_effect": "",
        "secondary_drive_effects": {}
      },
      "verified_progress_components": {
        "completeness": "COMPLETE",
        "components": {
          "goal_advance": 70.0,
          "knowledge_change": 60.0,
          "permanent_growth": 0.0,
          "relationship_change": 0.0,
          "strategy_expansion": 50.0,
          "world_state_change": 0.0
        },
        "evidence": {
          "goal_advance": [],
          "knowledge_change": [],
          "permanent_growth": [
            "no_verified_permanent_growth_change"
          ],
          "relationship_change": [
            "no_verified_relationship_change_change"
          ],
          "strategy_expansion": [],
          "world_state_change": [
            "no_verified_world_state_change_change"
          ]
        },
        "formula": "existing:progress",
        "score": 27.0,
        "source": "KERNEL_VERIFIED_EVIDENCE"
      },
      "verified_progression_impact": {
        "ability_showcases": [],
        "ability_unlocks": [],
        "axis_advanced": [],
        "growth_costs": [],
        "progression_delta_type": [],
        "resource_changes": [],
        "stage_change": null,
        "world_expansion": []
      },
      "verified_reader_promise_alignment": [],
      "verified_resource_impact": [],
      "verified_world_expansion_impact": [],
      "warnings": [
        "本候选未直接服务 CORE Reader Promise；单章缺席只记 Soft Miss。",
        "Primary Drive 没有可验证的结构推进；单章只记 Soft Miss。",
        "Candidate 未填写 Scheduler Alignment，保持 UNVERIFIED。"
      ]
    },
    "genre_drift": {
      "evidence": [],
      "hard_failure": false,
      "penalty": 4.0,
      "reasons": [
        "移除表层专名后，成长资源、能力与世界层级均不影响因果"
      ],
      "status": "GENRE_SKIN_ONLY",
      "warning": true
    },
    "genre_evolution": {
      "core_promise_preserved": true,
      "evidence": [],
      "explanation": "未检测到需要单独标记的 Genre Evolution",
      "status": "CLEAR"
    },
    "narrative_drive_alignment": {
      "drive_balance": "UNKNOWN",
      "drive_conflicts": [],
      "drives_advanced": [],
      "drives_deferred": [],
      "drives_paid_off": [],
      "evidence": [],
      "primary_drive": "SURVIVAL_RESOURCE",
      "primary_drive_effect": "",
      "secondary_drive_effects": {}
    },
    "payoff_channels": [],
    "progression_impact": {
      "ability_showcases": [],
      "ability_unlocks": [],
      "axis_advanced": [],
      "growth_costs": [],
      "progression_delta_type": [],
      "resource_changes": [],
      "stage_change": null,
      "world_expansion": []
    },
    "reader_promise_alignment": [],
    "resource_impact": [],
    "scheduler_alignment": {
      "alignment": "UNKNOWN",
      "anticipations_served": [],
      "candidate_primary_intent": null,
      "debts_served": [],
      "deviation_reason": "",
      "recommended_primary_intent": null,
      "risks": []
    },
    "world_expansion_impact": []
  },
  "world_expansion_impact": []
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
      },
      {
        "book_id": "original-e56a54687506",
        "created_at": "2026-08-16T16:39:36.675398+00:00",
        "dependencies_json": "[]",
        "edition_id": "base",
        "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "importance": 0.5,
        "introduced_chapter": "1",
        "last_advanced_chapter": "1",
        "payload_json": "{\"evidence\": \"沈砚获得测距带保留的墙面关系、取回饮水并带走刻有折返线的旧铝牌。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"setup\", \"source_draft_id\": \"draft_8bb76c611125c76689997a74\", \"source_span_id\": \"canon-span_96f6a1794bf43a1659c7fba2\", \"stakes\": \"建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "setup",
        "progress": 0.0,
        "reader_visibility": 0.5,
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "stakes": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
        "status": "CANON",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "space-reading-route-evidence",
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
    "base_event_seq": 8,
    "base_projection_hash": "65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050",
    "batch_anchor": {},
    "book_id": "original-e56a54687506",
    "canon_facts": {
      "post-rearrangement-door": {
        "_edition_id": "base",
        "_event_id": "event_1f1743812945cdf22326c4d3",
        "_event_seq": 4,
        "_source_id": "draft_8bb76c611125c76689997a74",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "重排结束后，原本平整的墙面出现一扇没有编号的门；门内广播报出十七层。",
        "fact_id": "post-rearrangement-door",
        "knowledge_status": "UNKNOWN",
        "location_relation": "same_wall_as_measuring_tape",
        "object": "原本平整的墙面出现一扇没有编号的门，门内广播报出十七层。",
        "predicate": "observed_after_rearrangement",
        "source_draft_id": "draft_8bb76c611125c76689997a74",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "status": "observed"
      }
    },
    "capabilities": {
      "measuring-tape-space-relation": {
        "_edition_id": "base",
        "_event_id": "event_0c50697347ecb8094273da84",
        "_event_seq": 2,
        "_source_id": "draft_8bb76c611125c76689997a74",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-space-relation",
        "character_id": "protagonist",
        "description": "测距带在局部空间重排后仍保持两端对同一墙面的测量关系，已形成一条可复核的异常路线证据。",
        "evidence": "正文中二点九四米的两端关系在楼梯断开、墙面折叠和重排后仍保持。",
        "name": "测距带跨局部重排保持空间关系",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_8bb76c611125c76689997a74",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "status": "ACTIVE"
      }
    },
    "character_states": {
      "protagonist-local-evidence-choice": {
        "_edition_id": "base",
        "_event_id": "event_a80ff58c44e66e2dc777f43a",
        "_event_seq": 6,
        "_source_id": "draft_8bb76c611125c76689997a74",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "在缺乏完整证据时选择以测距带保留空间关系，放弃强化手电的即时照明收益。",
        "character_id": "protagonist",
        "cost": "手电在回程前耗尽，后续行动依靠已有电量和测距带提供的关系判断。",
        "source_draft_id": "draft_8bb76c611125c76689997a74",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "state_id": "protagonist-local-evidence-choice"
      }
    },
    "current_position": {
      "last_canon_chapter": 1,
      "next_chapter": 2
    },
    "earlier_summaries": [],
    "edition_id": "base",
    "hook_diagnostics": {
      "advance_due": [],
      "overdue": [],
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
        "current_chapter": 1,
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
          },
          {
            "debt_ids": [],
            "horizon": "MID",
            "last_advanced": 1,
            "lifecycle": "SETUP",
            "maturity": 0.0,
            "maturity_note": "",
            "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
            "opened_chapter": 1,
            "thread_id": "space-reading-route-evidence"
          }
        ],
        "narrative_debts": [],
        "overdue_debt_ids": [],
        "payoff_ready_thread_ids": [],
        "short_threads": [],
        "snapshot_id": "portfolio_dd13a40ba418bba06c0e6c4b",
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
      "recent_pattern_distance": "high",
      "recommendation": {
        "evidence": [
          "active_threads",
          "recent_structures",
          "earned_surface.available_payoffs"
        ],
        "pattern_distance": "high",
        "reason": [
          "最近窗口结构差异为 high，仅作为软规划信号",
          "当前存在 2 个活跃线程、0 个开放设置"
        ],
        "recommended_focus": [
          "character",
          "mechanism"
        ]
      },
      "repeated_patterns": [],
      "semantic_policy_leak": null,
      "window_chapters": [
        1
      ]
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 1,
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
        },
        {
          "debt_ids": [],
          "horizon": "MID",
          "last_advanced": 1,
          "lifecycle": "SETUP",
          "maturity": 0.0,
          "maturity_note": "",
          "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
          "opened_chapter": 1,
          "thread_id": "space-reading-route-evidence"
        }
      ],
      "narrative_debts": [],
      "overdue_debt_ids": [],
      "payoff_ready_thread_ids": [],
      "short_threads": [],
      "snapshot_id": "portfolio_dd13a40ba418bba06c0e6c4b",
      "warnings": []
    },
    "packet_id": "boundary_d7669388731f2eeb442716de",
    "promises": {},
    "recent_full_chapters": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "content": "## 第1章 第一章 墙还在，路没了\n\n水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。\n\n楼道深处的广播忽然响了。\n\n先是一阵短促的电流声，接着，女人的声音隔着厚重的墙传出来，平平的，没有高低起伏。\n\n“别相信蓝色楼层。”\n\n声音断了。\n\n下一秒，水声又响了一遍，比刚才清楚。就在他右手边那段本来应该通往下层的楼梯后面。\n\n沈砚抬起手电。楼梯在四天前还是连续的，从二十层设备夹层往下，经过一个有消防窗的转角，再到十七层的空中连廊。现在中间少了两级，下面的半截楼梯横着嵌进另一面墙，扶手从缝里伸出来，像一根被硬掰弯的肋骨。\n\n对面悬着一块蓝色标牌，边角已经磕掉，白色的十七两个数字斜在漆面上。标牌下方是一小块还没塌掉的平台，半瓶水和一块旧的铝制指示牌躺在灰尘里。\n\n水瓶离他不到三米。中间却没有地面。\n\n沈砚蹲下来，把手电放在膝边，摸出测距带。金属外壳上有一道贯穿的凹痕，是他在灾变后的第二天从门框里撬出来的。带钩的那一头还能正常弹回，卡扣也没有松。他把带子拉出两米，贴着脚边的台阶量了一次，又抬头看向对面。\n\n两段楼梯的断口相隔一百九十七厘米。这个数字他记得很牢。昨天晚上，他曾用鞋底和墙缝反复核过，误差不会超过两厘米。今天缝隙变宽了，原来能碰到的扶手已经退到对面平台边缘。\n\n广播没有再说话。水声从蓝色标牌后面持续传来，细而急，像有人把一只瓶子倒扣在铁盆里。\n\n他先看了看手电。电量只剩最后一格，光线在墙上发虚。再看测距带，带身上的黑色刻度被灰尘填了一半，仍然能读。\n\n那种说不清的感觉在掌心里出现了。不是发热，也不是麻，更像有一根看不见的细线从物品内部绷出来，等着他把手指按在某个决定上。\n\n一天只能选一个。\n\n如果选手电，落脚点会亮得更久，至少能看清对面平台有没有空洞；如果选测距带，他也许能留下这段错乱空间的关系。手电能让他看见下一步，测距带却可能让他记住下一次重排之后的这一步。\n\n沈砚把手放在手电上，停了一会儿，又移向测距带。\n\n金属外壳在他掌心里轻轻一震。\n\n没有光，没有声音。带钩的薄片依旧是那副磨花的样子，刻度也没有增加。沈砚只觉得那道贯穿外壳的凹痕像被什么东西从里面重新压实了一遍。他没有等它给出更多动静，把带钩的一端扣进自己脚边墙角裸露的钢筋，带壳的一端压在身后的墙根。\n\n他拉出三米。\n\n带身横过断口，悬在两段楼梯之间。\n\n“二点九四。”他低声报出读数，用指甲在墙面上刮出一道短痕。\n\n水声突然停了。\n\n楼体深处传来一声沉闷的错动，像大船在水下翻了个身。台阶先往下沉，再往上顶。沈砚的肩膀撞上墙，手电从膝边滚出去，光柱斜斜地照进断口。\n\n第一道裂缝从蓝色标牌下方出现。对面的平台没有向后退，它朝他折了过来。墙上的瓷砖一块接一块错开，边缘擦出白色粉末；那块十七层的标牌被挤得翻转，蓝色的一面朝向他，像一只迟到的眼睛。\n\n沈砚想收回测距带，带身却没有顺着缝隙缩短。\n\n他握住外壳，感觉到另一头的钩子还扣在钢筋上。墙角正在移动，钢筋的位置已经不可能与原来的墙角重合，可带子的张力没有变。刻度线上，二点九四仍然对着他刚才刮下的那道痕。\n\n楼梯在这时彻底断开。\n\n他被挤到半级台阶上，脚下只剩一块三十厘米宽的水泥边。对面平台近了一瞬，又被墙面带着向侧方滑去。半瓶水沿着铝牌滚了两圈，停在平台边缘。\n\n沈砚没有去追。手电的光照不到那里，身体也没有余力让他跳过去。他只把测距带绷紧，顺着带身确认两面墙的关系：身后的墙角在左，带钩的墙面在右；中间的距离仍是二点九四。空间在变，关系没有散。\n\n这已经够了。\n\n他收起手电，先用左脚探向对面。鞋底碰到的是平台外沿，不是空处。测距带在掌心里发出极轻的颤动，带钩那一端指向的墙面没有偏。沈砚慢慢伏低身体，胸口贴过断口，右手抓住翻起的扶手。\n\n墙里传来细碎的摩擦声。仿佛整座楼正在把一张纸折成更小的形状，而他只是纸上的一粒砂。\n\n他不敢抬头，沿着那条已经被测距带固定下来的关系一点点挪。膝盖先落地，肩膀再过去，最后才把腿拖上平台。水瓶就在手边。他抓住瓶颈，先拧开瓶盖，喝了一口。水是温的，带着塑料味，却让喉咙里那层干硬的砂纸软了下去。\n\n他没有一口气喝完，只把剩下的半瓶水塞进外套内袋。\n\n旧铝牌压在水瓶下面。沈砚把它翻过来，背面有几道被人用硬物刻出的线：一条直线，两次折返，末端钉着一个小小的圆点。圆点旁边还有一行已经磨掉一半的数字，看不出是十七还是一七。\n\n他用袖口擦掉灰，把铝牌夹在腰侧。没有时间判断这些线是谁留下的，也没有时间猜它们指向哪里。至少它们能证明，刚才那段路不是他在黑暗里记错了。\n\n身后的墙突然安静下来。\n\n安静得太快。\n\n沈砚抓住测距带，准备沿原路回去。带壳的一端仍压在他身后的墙根，带钩的一端却不再悬在断口对面。两端都贴着同一面灰墙，一左一右，之间隔着完整的二点九四米。刚才那两段互不相连的楼梯不见了，脚下只剩一块狭窄的楼面，墙面平整地立在前方。\n\n那面墙上多了一扇门。\n\n门框没有灰尘，像是刚从墙里长出来。没有猫眼，没有把手旁的编号，只有一条窄窄的黑缝，从门后漏出冷风。冷风里混着潮湿的土腥味，和他刚喝下去的水一样真实。\n\n沈砚没有靠近。\n\n广播就在门内响起。\n\n电流声比之前更近，近得像有人把嘴贴在门板另一侧。\n\n“十七层。”\n\n他还没说出这个数字。\n\n沈砚低头看着测距带。两端的刻度同时指向那面墙，二点九四没有改变。门却在墙上，门后有什么也没有给出解释。\n\n他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。\n",
        "heading": "## 第1章 第一章 墙还在，路没了",
        "ordinal": 1,
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
      }
    ],
    "recent_payoffs": {},
    "recent_structures": [
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape",
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "created_at": "2026-08-16T16:39:36.675398+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 1,
        "payload_json": "{\"candidate_id\": \"genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape\", \"signature\": \"function:setup\", \"source_draft_id\": \"draft_8bb76c611125c76689997a74\", \"source_span_id\": \"canon-span_96f6a1794bf43a1659c7fba2\", \"structure_tags\": [\"function:setup\"], \"tag_id\": \"repetition_632fb4e8d7d6c1e533b6e361\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_632fb4e8d7d6c1e533b6e361",
        "version": 1
      }
    ],
    "relationships": {},
    "relevant_source_spans": [],
    "resources": {
      "water-half-bottle-recovered": {
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
      }
    },
    "reveal_agenda": {
      "book_id": "original-e56a54687506",
      "chapter_ordinal": 2,
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
      "as_of_chapter": 1,
      "as_of_event_seq": 8,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T16:39:36.864621+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 1,
        "mode": "unknown",
        "severity": "NONE"
      },
      "ending_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "evidence": [
        {
          "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 1
        }
      ],
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
      "projection_hash": "65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_22d699e14337cc8178b4666f",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.0,
        "series_markers": [
          null
        ],
        "severity": "NONE"
      }
    },
    "rhythm_features": [
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T16:39:36.727311+00:00",
        "edition_id": "base",
        "effective_content_sha256": "81b9f177e416edf8a46c35623764c76937a4fb7980d8b1b51b196ef49db80d95",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。",
        "ending_excerpt_raw": "他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。",
        "ending_fingerprint_prose": "1924ea959863f00652dddd0c4c4d61a05784c50e5108db44be778d5151c3382e",
        "ending_fingerprint_raw": "1924ea959863f00652dddd0c4c4d61a05784c50e5108db44be778d5151c3382e",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_2bb1dd243ed8a5483903dd99",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "第一章 墙还在,路没了",
        "opening_excerpt_prose": "水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。\n\n楼道深处的广播忽然响了。",
        "opening_excerpt_raw": "## 第1章 第一章 墙还在，路没了\n\n水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。",
        "opening_fingerprint_prose": "618980928bd9e630059135a185a34a349f7832d8b8f4eaf99307404186ab6df6",
        "opening_fingerprint_raw": "75e306dff933f76d4672117946feace2a6259fe619374434e6c62b94e75d6f2e",
        "opening_mode": "unknown",
        "ordinal": 1,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "aff139a5768f80cb9b1ad5b463db9b4619f825a589d771b2c72741effa1efefb",
        "title_raw": "## 第1章 第一章 墙还在，路没了",
        "version": 1
      }
    ],
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
      },
      {
        "book_id": "original-e56a54687506",
        "created_at": "2026-08-16T16:39:36.675398+00:00",
        "dependencies_json": "[]",
        "edition_id": "base",
        "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "importance": 0.5,
        "introduced_chapter": "1",
        "last_advanced_chapter": "1",
        "payload_json": "{\"evidence\": \"沈砚获得测距带保留的墙面关系、取回饮水并带走刻有折返线的旧铝牌。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"setup\", \"source_draft_id\": \"draft_8bb76c611125c76689997a74\", \"source_span_id\": \"canon-span_96f6a1794bf43a1659c7fba2\", \"stakes\": \"建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "setup",
        "progress": 0.0,
        "reader_visibility": 0.5,
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "stakes": "建筑把上下关系周期性打乱，广播又给出互相矛盾的提示；每次进化只能解决一个空间缺口，追声、找水、保留退路不能同时满足。",
        "status": "CANON",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "space-reading-route-evidence",
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
    "base_event_seq": 8,
    "base_projection_hash": "65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050",
    "batch_anchor": {},
    "book_id": "original-e56a54687506",
    "canon_facts": {
      "post-rearrangement-door": {
        "_edition_id": "base",
        "_event_id": "event_1f1743812945cdf22326c4d3",
        "_event_seq": 4,
        "_source_id": "draft_8bb76c611125c76689997a74",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "重排结束后，原本平整的墙面出现一扇没有编号的门；门内广播报出十七层。",
        "fact_id": "post-rearrangement-door",
        "knowledge_status": "UNKNOWN",
        "location_relation": "same_wall_as_measuring_tape",
        "object": "原本平整的墙面出现一扇没有编号的门，门内广播报出十七层。",
        "predicate": "observed_after_rearrangement",
        "source_draft_id": "draft_8bb76c611125c76689997a74",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "status": "observed"
      }
    },
    "capabilities": {
      "measuring-tape-space-relation": {
        "_edition_id": "base",
        "_event_id": "event_0c50697347ecb8094273da84",
        "_event_seq": 2,
        "_source_id": "draft_8bb76c611125c76689997a74",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-space-relation",
        "character_id": "protagonist",
        "description": "测距带在局部空间重排后仍保持两端对同一墙面的测量关系，已形成一条可复核的异常路线证据。",
        "evidence": "正文中二点九四米的两端关系在楼梯断开、墙面折叠和重排后仍保持。",
        "name": "测距带跨局部重排保持空间关系",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_8bb76c611125c76689997a74",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "status": "ACTIVE"
      }
    },
    "character_states": {
      "protagonist-local-evidence-choice": {
        "_edition_id": "base",
        "_event_id": "event_a80ff58c44e66e2dc777f43a",
        "_event_seq": 6,
        "_source_id": "draft_8bb76c611125c76689997a74",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "在缺乏完整证据时选择以测距带保留空间关系，放弃强化手电的即时照明收益。",
        "character_id": "protagonist",
        "cost": "手电在回程前耗尽，后续行动依靠已有电量和测距带提供的关系判断。",
        "source_draft_id": "draft_8bb76c611125c76689997a74",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2",
        "state_id": "protagonist-local-evidence-choice"
      }
    },
    "current_position": {
      "last_canon_chapter": 1,
      "next_chapter": 2
    },
    "earlier_summaries": [],
    "edition_id": "base",
    "hook_diagnostics": {
      "advance_due": [],
      "overdue": [],
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
        "current_chapter": 1,
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
          },
          {
            "debt_ids": [],
            "horizon": "MID",
            "last_advanced": 1,
            "lifecycle": "SETUP",
            "maturity": 0.0,
            "maturity_note": "",
            "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
            "opened_chapter": 1,
            "thread_id": "space-reading-route-evidence"
          }
        ],
        "narrative_debts": [],
        "overdue_debt_ids": [],
        "payoff_ready_thread_ids": [],
        "short_threads": [],
        "snapshot_id": "portfolio_dd13a40ba418bba06c0e6c4b",
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
      "recent_pattern_distance": "high",
      "recommendation": {
        "evidence": [
          "active_threads",
          "recent_structures",
          "earned_surface.available_payoffs"
        ],
        "pattern_distance": "high",
        "reason": [
          "最近窗口结构差异为 high，仅作为软规划信号",
          "当前存在 2 个活跃线程、0 个开放设置"
        ],
        "recommended_focus": [
          "character",
          "mechanism"
        ]
      },
      "repeated_patterns": [],
      "semantic_policy_leak": null,
      "window_chapters": [
        1
      ]
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 1,
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
        },
        {
          "debt_ids": [],
          "horizon": "MID",
          "last_advanced": 1,
          "lifecycle": "SETUP",
          "maturity": 0.0,
          "maturity_note": "",
          "name": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
          "opened_chapter": 1,
          "thread_id": "space-reading-route-evidence"
        }
      ],
      "narrative_debts": [],
      "overdue_debt_ids": [],
      "payoff_ready_thread_ids": [],
      "short_threads": [],
      "snapshot_id": "portfolio_dd13a40ba418bba06c0e6c4b",
      "warnings": []
    },
    "packet_id": "boundary_d7669388731f2eeb442716de",
    "promises": {},
    "recent_full_chapters": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "content": "## 第1章 第一章 墙还在，路没了\n\n水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。\n\n楼道深处的广播忽然响了。\n\n先是一阵短促的电流声，接着，女人的声音隔着厚重的墙传出来，平平的，没有高低起伏。\n\n“别相信蓝色楼层。”\n\n声音断了。\n\n下一秒，水声又响了一遍，比刚才清楚。就在他右手边那段本来应该通往下层的楼梯后面。\n\n沈砚抬起手电。楼梯在四天前还是连续的，从二十层设备夹层往下，经过一个有消防窗的转角，再到十七层的空中连廊。现在中间少了两级，下面的半截楼梯横着嵌进另一面墙，扶手从缝里伸出来，像一根被硬掰弯的肋骨。\n\n对面悬着一块蓝色标牌，边角已经磕掉，白色的十七两个数字斜在漆面上。标牌下方是一小块还没塌掉的平台，半瓶水和一块旧的铝制指示牌躺在灰尘里。\n\n水瓶离他不到三米。中间却没有地面。\n\n沈砚蹲下来，把手电放在膝边，摸出测距带。金属外壳上有一道贯穿的凹痕，是他在灾变后的第二天从门框里撬出来的。带钩的那一头还能正常弹回，卡扣也没有松。他把带子拉出两米，贴着脚边的台阶量了一次，又抬头看向对面。\n\n两段楼梯的断口相隔一百九十七厘米。这个数字他记得很牢。昨天晚上，他曾用鞋底和墙缝反复核过，误差不会超过两厘米。今天缝隙变宽了，原来能碰到的扶手已经退到对面平台边缘。\n\n广播没有再说话。水声从蓝色标牌后面持续传来，细而急，像有人把一只瓶子倒扣在铁盆里。\n\n他先看了看手电。电量只剩最后一格，光线在墙上发虚。再看测距带，带身上的黑色刻度被灰尘填了一半，仍然能读。\n\n那种说不清的感觉在掌心里出现了。不是发热，也不是麻，更像有一根看不见的细线从物品内部绷出来，等着他把手指按在某个决定上。\n\n一天只能选一个。\n\n如果选手电，落脚点会亮得更久，至少能看清对面平台有没有空洞；如果选测距带，他也许能留下这段错乱空间的关系。手电能让他看见下一步，测距带却可能让他记住下一次重排之后的这一步。\n\n沈砚把手放在手电上，停了一会儿，又移向测距带。\n\n金属外壳在他掌心里轻轻一震。\n\n没有光，没有声音。带钩的薄片依旧是那副磨花的样子，刻度也没有增加。沈砚只觉得那道贯穿外壳的凹痕像被什么东西从里面重新压实了一遍。他没有等它给出更多动静，把带钩的一端扣进自己脚边墙角裸露的钢筋，带壳的一端压在身后的墙根。\n\n他拉出三米。\n\n带身横过断口，悬在两段楼梯之间。\n\n“二点九四。”他低声报出读数，用指甲在墙面上刮出一道短痕。\n\n水声突然停了。\n\n楼体深处传来一声沉闷的错动，像大船在水下翻了个身。台阶先往下沉，再往上顶。沈砚的肩膀撞上墙，手电从膝边滚出去，光柱斜斜地照进断口。\n\n第一道裂缝从蓝色标牌下方出现。对面的平台没有向后退，它朝他折了过来。墙上的瓷砖一块接一块错开，边缘擦出白色粉末；那块十七层的标牌被挤得翻转，蓝色的一面朝向他，像一只迟到的眼睛。\n\n沈砚想收回测距带，带身却没有顺着缝隙缩短。\n\n他握住外壳，感觉到另一头的钩子还扣在钢筋上。墙角正在移动，钢筋的位置已经不可能与原来的墙角重合，可带子的张力没有变。刻度线上，二点九四仍然对着他刚才刮下的那道痕。\n\n楼梯在这时彻底断开。\n\n他被挤到半级台阶上，脚下只剩一块三十厘米宽的水泥边。对面平台近了一瞬，又被墙面带着向侧方滑去。半瓶水沿着铝牌滚了两圈，停在平台边缘。\n\n沈砚没有去追。手电的光照不到那里，身体也没有余力让他跳过去。他只把测距带绷紧，顺着带身确认两面墙的关系：身后的墙角在左，带钩的墙面在右；中间的距离仍是二点九四。空间在变，关系没有散。\n\n这已经够了。\n\n他收起手电，先用左脚探向对面。鞋底碰到的是平台外沿，不是空处。测距带在掌心里发出极轻的颤动，带钩那一端指向的墙面没有偏。沈砚慢慢伏低身体，胸口贴过断口，右手抓住翻起的扶手。\n\n墙里传来细碎的摩擦声。仿佛整座楼正在把一张纸折成更小的形状，而他只是纸上的一粒砂。\n\n他不敢抬头，沿着那条已经被测距带固定下来的关系一点点挪。膝盖先落地，肩膀再过去，最后才把腿拖上平台。水瓶就在手边。他抓住瓶颈，先拧开瓶盖，喝了一口。水是温的，带着塑料味，却让喉咙里那层干硬的砂纸软了下去。\n\n他没有一口气喝完，只把剩下的半瓶水塞进外套内袋。\n\n旧铝牌压在水瓶下面。沈砚把它翻过来，背面有几道被人用硬物刻出的线：一条直线，两次折返，末端钉着一个小小的圆点。圆点旁边还有一行已经磨掉一半的数字，看不出是十七还是一七。\n\n他用袖口擦掉灰，把铝牌夹在腰侧。没有时间判断这些线是谁留下的，也没有时间猜它们指向哪里。至少它们能证明，刚才那段路不是他在黑暗里记错了。\n\n身后的墙突然安静下来。\n\n安静得太快。\n\n沈砚抓住测距带，准备沿原路回去。带壳的一端仍压在他身后的墙根，带钩的一端却不再悬在断口对面。两端都贴着同一面灰墙，一左一右，之间隔着完整的二点九四米。刚才那两段互不相连的楼梯不见了，脚下只剩一块狭窄的楼面，墙面平整地立在前方。\n\n那面墙上多了一扇门。\n\n门框没有灰尘，像是刚从墙里长出来。没有猫眼，没有把手旁的编号，只有一条窄窄的黑缝，从门后漏出冷风。冷风里混着潮湿的土腥味，和他刚喝下去的水一样真实。\n\n沈砚没有靠近。\n\n广播就在门内响起。\n\n电流声比之前更近，近得像有人把嘴贴在门板另一侧。\n\n“十七层。”\n\n他还没说出这个数字。\n\n沈砚低头看着测距带。两端的刻度同时指向那面墙，二点九四没有改变。门却在墙上，门后有什么也没有给出解释。\n\n他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。\n",
        "heading": "## 第1章 第一章 墙还在，路没了",
        "ordinal": 1,
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
      }
    ],
    "recent_payoffs": {},
    "recent_structures": [
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape",
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "created_at": "2026-08-16T16:39:36.675398+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 1,
        "payload_json": "{\"candidate_id\": \"genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape\", \"signature\": \"function:setup\", \"source_draft_id\": \"draft_8bb76c611125c76689997a74\", \"source_span_id\": \"canon-span_96f6a1794bf43a1659c7fba2\", \"structure_tags\": [\"function:setup\"], \"tag_id\": \"repetition_632fb4e8d7d6c1e533b6e361\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_632fb4e8d7d6c1e533b6e361",
        "version": 1
      }
    ],
    "relationships": {},
    "relevant_source_spans": [],
    "resources": {
      "water-half-bottle-recovered": {
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
      }
    },
    "reveal_agenda": {
      "book_id": "original-e56a54687506",
      "chapter_ordinal": 2,
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
      "as_of_chapter": 1,
      "as_of_event_seq": 8,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T16:39:36.864621+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 1,
        "mode": "unknown",
        "severity": "NONE"
      },
      "ending_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "evidence": [
        {
          "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 1
        }
      ],
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
      "projection_hash": "65fa4bb87a62264ad891e732809effa8a882d105d2d4fc1a502b5f7435328050",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_22d699e14337cc8178b4666f",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.0,
        "series_markers": [
          null
        ],
        "severity": "NONE"
      }
    },
    "rhythm_features": [
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T16:39:36.727311+00:00",
        "edition_id": "base",
        "effective_content_sha256": "81b9f177e416edf8a46c35623764c76937a4fb7980d8b1b51b196ef49db80d95",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。",
        "ending_excerpt_raw": "他把手电的开关按了一下。光柱闪烁两次，彻底暗下去。\n\n门内的声音没有再催促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距带，把铝牌和水瓶重新压稳，站在那条旧地图无法解释的关系上。\n\n这一次，他记住了回来的方向。门后是不是出口，等下一次再判断。",
        "ending_fingerprint_prose": "1924ea959863f00652dddd0c4c4d61a05784c50e5108db44be778d5151c3382e",
        "ending_fingerprint_raw": "1924ea959863f00652dddd0c4c4d61a05784c50e5108db44be778d5151c3382e",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_2bb1dd243ed8a5483903dd99",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "第一章 墙还在,路没了",
        "opening_excerpt_prose": "水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。\n\n楼道深处的广播忽然响了。",
        "opening_excerpt_raw": "## 第1章 第一章 墙还在，路没了\n\n水声是从楼梯下面传上来的。\n\n沈砚停在半级台阶上，手电的光贴着混凝土墙面扫过去。光柱里没有水，只有一层被潮气泡白的乳胶漆，漆皮从墙角往上卷，像一排没来得及收起的鳞片。",
        "opening_fingerprint_prose": "618980928bd9e630059135a185a34a349f7832d8b8f4eaf99307404186ab6df6",
        "opening_fingerprint_raw": "75e306dff933f76d4672117946feace2a6259fe619374434e6c62b94e75d6f2e",
        "opening_mode": "unknown",
        "ordinal": 1,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "aff139a5768f80cb9b1ad5b463db9b4619f825a589d771b2c72741effa1efefb",
        "title_raw": "## 第1章 第一章 墙还在，路没了",
        "version": 1
      }
    ],
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