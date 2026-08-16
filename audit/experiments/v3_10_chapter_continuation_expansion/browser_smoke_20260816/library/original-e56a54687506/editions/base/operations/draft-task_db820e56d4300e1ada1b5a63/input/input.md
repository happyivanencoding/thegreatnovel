# 章节正文任务 `draft-task_db820e56d4300e1ada1b5a63`

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
    "上方风道与无回声空段的关系被测距带固定为可复核方向证据。",
    "风道位置被记录，七步脚印后的灰白边缘成为新的未知上方线索。"
  ],
  "micro_event_rule": "允许只改变人物感知、动作或场面反应的 realization-only micro-event；不得改变 Contract、Canon、Knowledge、Resource 或 Capability。",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "target_scene_count": 3,
  "target_word_range": [
    526,
    1174
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

# Continuation Boundary Packet `boundary_7fe2796cdce6dd838a397b46`

- book_id: `original-e56a54687506`
- base_event_seq: 43
- projection_sha256: `2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c`
- current_position: {"last_canon_chapter": 6, "next_chapter": 7}

## 最近完整章节

### ## 第4章 屋顶在墙后

source_span_id: `canon-span_6a551b7a462d002ea780f449`

## 第4章 屋顶在墙后

检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。

广播在墙后响起来。

“屋顶安全，向前三十米。”

声音很近，近得像贴着检修窗的铁皮说话。沈砚没有抬头去找。上一轮他看见过倒挂的蓝色标志，也看见过标志下面没有地面。广播说的是方向，不是证据。

楼层开始重排。走廊地面先向左倾，墙根的灰线被拉成一条细长的弧。检修窗外没有平台，只有一块向后缩的墙面。墙面缩到一半，忽然裂开一道竖口，冷风从里面冲出来，带着湿水泥和很淡的铁锈味。

脚步声就在竖口里，一步，停顿，再一步。广播又说了一遍屋顶安全，脚步却向下传，像有人在看不见的楼梯上往低处走。竖口上方露出一角蓝色标志，方向和声音都像真的；可标志的边缘没有固定的墙，随着建筑移动，它连同竖口一起向窗边滑来。

沈砚先看手里的东西。水瓶还有一半，手电的光柱已经发黄，铝牌上的折返线刚好能指回走廊。今天的机会只有一次。他没有拿水瓶去赌一口水，也没有让手电替他照亮不存在的地面。

他选择测距带。

带钩端甩进竖口，钩住一片没有完全脱落的金属边。墙面立刻向后缩，带身绷紧。带钩端卡在孔里，带壳端却没有随着墙体后退。沈砚盯住两端之间的弧线，等第二次移动发生。

开口与检修窗的距离在闭合前先缩短又恢复，广播的屋顶声音没有固定端点。他在铝牌上划下一道短线。不是距离变回去了，而是墙后那一段空间绕着窗框折了一次。竖口看起来向前，实际却把带钩端拖向下方。若他顺着蓝色标志踏进去，下一次重排很可能会把回程折到别处。

沈砚把脚放到窗台边，半个身子探向竖口。冷风从衣领灌进去，墙后没有脚下的回声，只有一阵一阵往下坠的空气。声音还在说屋顶安全，脚步声却停在他看不见的地方。

他没有进入。他先记录回声关系，再拒绝踏入无法保留回程的开口。带身的弧度把竖口和窗框之间的闭合关系留在铝牌的刻线上，测距带记录了一处广播回声与真实端点不一致的闭合关系。

竖口开始合拢。沈砚用力向后收带，金属钩擦过墙边，带壳端仍压在窗台上。开口只剩一掌宽时，里面传来第三下脚步，随后声音和风一起被墙体夹断。

他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。

沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。

他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。


### ## 第5章 倒着写的门

source_span_id: `canon-span_527cd52fb85756bbad483200`

## 第5章 倒着写的门

广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。

他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。

楼层开始移动。墙根向外鼓起，倒写的痕迹被拉长，半扇门的轮廓从粉痕后显出来。门缝朝向窗外，门把手却在墙里。沈砚把测距带的带壳端压住窗台，带钩端轻轻碰到门缝上方的金属边。

门没有开，距离先变了。

带身向右绷直，门缝却向左退。沈砚盯着刻度，确认那不是门在墙上滑动，而是墙后的空间绕着窗台换了一面。倒写标记与检修窗的方向关系被测距带留在铝牌上：它来自另一个重排状态，并且在当前状态仍能被复核。

门后传来很轻的一声敲击。

一下，停顿，再一下。

他想起高处风道里的七步白印，却没有把敲击和脚印接在一起。现在能确认的只有声音、痕迹和一条不稳定的关系。门把手仍在墙里，门缝下面没有可见的地面；只要再向前半步，带钩端就会被门框夹住。

沈砚把铝牌翻过来，写下倒着的方向。他先把陌生标记当作观察数据，不因为它像求救就越过证据边界。广播突然停了，墙后的敲击也跟着消失。沉默没有回答他，却让门缝显得比刚才更近。

他没有开门。

建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。

倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？


### ## 第6章 没有回声的楼梯

source_span_id: `canon-span_307f36eeb3ff4ba659fb82a0`

## 第6章 没有回声的楼梯

沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。

这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。

他没有先听楼梯通向哪里，而是听自己的呼吸。声音贴着窗框返回，台阶上的声音却没有回来。沈砚捏紧测距带，把带壳端压在窗台，带钩端碰向第三节扶手。

钩子没有钩住实体。

它穿过扶手下方的黑暗，落在更低处。带身先向下绷，随后又在同一刻度上松开。沈砚盯着刻度变化，确认那不是楼梯延长，而是楼梯下方存在一段没有回声、也没有可见地面的空段。测距带记录了无回声楼梯与窗台的空段关系。

广播突然从远处响起：“西侧楼梯安全。”

沈砚没有回答。刚才这截楼梯就在西侧墙后，声音却像从它下面传来。安全两个字没有重量，只有他的带钩端和窗台还在同一条线上。

他把身体探出半步。冷气沿台阶向上涌，第三节以下的黑暗没有回风。手电光落下去，像被一层没有反射的水吞掉。那里可能有地面，也可能只有建筑重排后留下的空白；当前没有任何证据允许他选择其中一个解释。

他只记录空段，不进入没有回声和地面的楼梯。

墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。

广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。

他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。


## 更早章节摘要

```json
[
  {
    "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
    "heading": "## 第1章 第一章 墙还在，路没了",
    "ordinal": 1,
    "summary": "正文停在首章 VALIDATED 边界，未执行正史批准；广播来源、门后空间和建筑成因保持未知。"
  },
  {
    "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
    "heading": "## 第2章 窗缝之外",
    "ordinal": 2,
    "summary": "正文只推进楼外风光的局部可验证事实；广播来源、建筑成因与其他幸存者规则保持未知。"
  },
  {
    "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
    "heading": "## 第3章 没有地面的平台",
    "ordinal": 3,
    "summary": "白色脚印、建筑成因、广播身份与相邻塔体关系保持未知。"
  }
]
```

## FTS5 相关原文片段

```json
[
  {
    "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
    "excerpt": "…促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距…",
    "ordinal": 1,
    "raw_heading": "## 第1章 第一章 墙还在，路没了",
    "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
  }
]
```

## 当前正史

```json
{
  "external-platform-seen-ch3": {
    "_edition_id": "base",
    "_event_id": "event_60e4f30cd8ae63966f62202a",
    "_event_seq": 18,
    "_source_id": "draft_78fbd961bd5cc5becb7a897f",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "description": "重排后的检修窗外出现一块没有地面支撑的外侧平台，平台连接上方断裂风道。",
    "fact_id": "external-platform-seen-ch3",
    "knowledge_status": "UNKNOWN",
    "location_relation": "outside_external_vent_window",
    "object": "没有地面支撑的外侧平台",
    "predicate": "external_platform_observed",
    "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
    "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
    "status": "observed"
  },
  "external-vent-window-observed": {
    "_edition_id": "base",
    "_event_id": "event_b8b0234db2cdefd55535c2a5",
    "_event_seq": 11,
    "_source_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "description": "重排后的断梯边出现一扇没有编号的检修窗，窗外有真实风和灰光。",
    "fact_id": "external-vent-window-observed",
    "knowledge_status": "UNKNOWN",
    "location_relation": "same_wall_as_measuring_tape",
    "object": "没有编号的检修窗",
    "predicate": "external_window_observed",
    "source_draft_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
    "source_span_id": "canon-span_70e5d91133cdb192b7cfb599",
    "status": "observed"
  },
  "false-roof-echo-observed-ch4": {
    "_edition_id": "base",
    "_event_id": "event_a5868c8ee939d0f9a8ff989c",
    "_event_seq": 25,
    "_source_id": "draft_bf2bb3f1e46011392b83b872",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "description": "广播指向的屋顶开口与检修窗之间的相对距离发生闭合错位，声音没有可固定的真实端点。",
    "fact_id": "false-roof-echo-observed-ch4",
    "knowledge_status": "UNKNOWN",
    "location_relation": "behind_external_vent_window",
    "object": "广播回声与竖向开口",
    "predicate": "false_roof_echo_closed",
    "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
    "source_span_id": "canon-span_6a551b7a462d002ea780f449",
    "status": "observed"
  },
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
  },
  "reverse-mark-observed-ch5": {
    "_edition_id": "base",
    "_event_id": "event_2c6c0ae01e2b0d646a3e7029",
    "_event_seq": 32,
    "_source_id": "draft_d12d36ba1bc35e24b20a4570",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "description": "检修窗附近出现一条指向已消失平台的倒写门框标记，标记在重排后仍留下可复核的方向关系。",
    "fact_id": "reverse-mark-observed-ch5",
    "knowledge_status": "UNKNOWN",
    "location_relation": "behind_external_vent_window",
    "object": "倒写门框粉痕",
    "predicate": "reverse_mark_observed",
    "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
    "source_span_id": "canon-span_527cd52fb85756bbad483200",
    "status": "observed"
  },
  "silent-stair-gap-observed-ch6": {
    "_edition_id": "base",
    "_event_id": "event_08d62929d8697d2cbc7a7060",
    "_event_seq": 39,
    "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "description": "检修窗外短暂出现一截向下楼梯，台阶下存在没有回声和可见地面的空段。",
    "fact_id": "silent-stair-gap-observed-ch6",
    "knowledge_status": "UNKNOWN",
    "location_relation": "behind_external_vent_window",
    "object": "无回声楼梯与黑暗空段",
    "predicate": "silent_stair_gap_observed",
    "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
    "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
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
  },
  "protagonist-local-evidence-choice-2": {
    "_edition_id": "base",
    "_event_id": "event_7c276de06aa34b363c3479b3",
    "_event_seq": 13,
    "_source_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "change": "在不完整证据下先验证风、光和距离，选择测距带而不是追随广播。",
    "character_id": "protagonist",
    "cost": "失去当天让其他物品进化的机会，并暴露自己所在楼层与相邻空间的风险。",
    "source_draft_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
    "source_span_id": "canon-span_70e5d91133cdb192b7cfb599",
    "state_id": "protagonist-local-evidence-choice-2"
  },
  "protagonist-local-evidence-choice-3": {
    "_edition_id": "base",
    "_event_id": "event_bd6e09071d9a0d44ecae5ecb",
    "_event_seq": 20,
    "_source_id": "draft_78fbd961bd5cc5becb7a897f",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "change": "沈砚先用测距带确认平台与检修窗的关系，再踏入没有地面的外侧空间。",
    "character_id": "protagonist",
    "cost": "再次消耗当天唯一进化机会，并暴露在平台下方没有地面的外侧边缘。",
    "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
    "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
    "state_id": "protagonist-local-evidence-choice-3"
  },
  "protagonist-local-evidence-choice-4": {
    "_edition_id": "base",
    "_event_id": "event_604b0534399e0008ca0c542e",
    "_event_seq": 27,
    "_source_id": "draft_bf2bb3f1e46011392b83b872",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "change": "他先记录回声关系，再拒绝踏入无法保留回程的开口。",
    "character_id": "protagonist",
    "cost": "再次消耗当天唯一进化机会，并放弃沿广播进入屋顶的可能。",
    "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
    "source_span_id": "canon-span_6a551b7a462d002ea780f449",
    "state_id": "protagonist-local-evidence-choice-4"
  },
  "protagonist-local-evidence-choice-5": {
    "_edition_id": "base",
    "_event_id": "event_d4824e51ab28c95960782fb6",
    "_event_seq": 34,
    "_source_id": "draft_d12d36ba1bc35e24b20a4570",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "change": "沈砚把陌生标记当作观察数据，不因为它像求救就越过证据边界。",
    "character_id": "protagonist",
    "cost": "再次消耗当天唯一进化机会，并放弃打开可能通向他人的门。",
    "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
    "source_span_id": "canon-span_527cd52fb85756bbad483200",
    "state_id": "protagonist-local-evidence-choice-5"
  },
  "protagonist-local-evidence-choice-6": {
    "_edition_id": "base",
    "_event_id": "event_45e32139060151cd07153647",
    "_event_seq": 41,
    "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "change": "沈砚接受局部证据也可能没有答案，只记录空段，不追入无回声楼梯。",
    "character_id": "protagonist",
    "cost": "再次消耗当天唯一进化机会，并放弃追入楼梯获取即时答案。",
    "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
    "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
    "state_id": "protagonist-local-evidence-choice-6"
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
    "last_advanced_chapter": "6",
    "payload_json": "{\"evidence\": \"沈砚只记录空段，不进入没有回声和地面的楼梯，随后沿测距带退回窗边。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"escalation\", \"source_draft_id\": \"draft_5021c9974e2cd8b3253d0ef4\", \"source_span_id\": \"canon-span_307f36eeb3ff4ba659fb82a0\", \"stakes\": \"无回声楼梯可能通向空白空间，进入会让测距带和回程一起被墙体吞掉。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
    "phase": "escalation",
    "progress": 0.0,
    "reader_visibility": 0.5,
    "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
    "stakes": "无回声楼梯可能通向空白空间，进入会让测距带和回程一起被墙体吞掉。",
    "status": "CANON",
    "target_payoff_max": null,
    "target_payoff_min": null,
    "thread_id": "space-reading-route-evidence",
    "version": 6
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
  "measuring-tape-false-roof-relation": {
    "_edition_id": "base",
    "_event_id": "event_3abb8e5a7dfebd1198e3c4ea",
    "_event_seq": 24,
    "_source_id": "draft_bf2bb3f1e46011392b83b872",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "capability_id": "measuring-tape-false-roof-relation",
    "character_id": "protagonist",
    "description": "测距带记录检修窗与广播回声开口之间的闭合关系，能够把假屋顶路线固定为可复核的排除证据。",
    "evidence": "带钩端卡在孔里，带壳端却没有随着墙体后退。",
    "name": "测距带记录闭合回声关系",
    "object_id": "measuring-tape",
    "owner_id": "protagonist",
    "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
    "source_span_id": "canon-span_6a551b7a462d002ea780f449",
    "status": "ACTIVE"
  },
  "measuring-tape-reverse-mark-ch5": {
    "_edition_id": "base",
    "_event_id": "event_8eadaf620e6f52459c6d4351",
    "_event_seq": 31,
    "_source_id": "draft_d12d36ba1bc35e24b20a4570",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "capability_id": "measuring-tape-reverse-mark-ch5",
    "character_id": "protagonist",
    "description": "测距带记录倒写标记与检修窗的方向关系，能把跨重排留下的陌生路线痕迹固定为可复核证据。",
    "evidence": "倒写标记与检修窗的方向关系被测距带留在铝牌上。",
    "name": "测距带记录跨重排标记方向",
    "object_id": "measuring-tape",
    "owner_id": "protagonist",
    "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
    "source_span_id": "canon-span_527cd52fb85756bbad483200",
    "status": "ACTIVE"
  },
  "measuring-tape-silent-gap-ch6": {
    "_edition_id": "base",
    "_event_id": "event_519903c0a062e0f98b32254d",
    "_event_seq": 38,
    "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "capability_id": "measuring-tape-silent-gap-ch6",
    "character_id": "protagonist",
    "description": "测距带记录无回声楼梯与检修窗之间的空段关系，保留一处不可见但可复核的建筑断层。",
    "evidence": "测距带记录了无回声楼梯与窗台的空段关系。",
    "name": "测距带记录无回声空段",
    "object_id": "measuring-tape",
    "owner_id": "protagonist",
    "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
    "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
    "status": "ACTIVE"
  },
  "measuring-tape-space-relation": {
    "_edition_id": "base",
    "_event_id": "event_f09aece7643886d7552d9888",
    "_event_seq": 17,
    "_source_id": "draft_78fbd961bd5cc5becb7a897f",
    "_source_kind": "AUTHOR_APPROVED_DRAFT",
    "capability_id": "measuring-tape-space-relation",
    "character_id": "protagonist",
    "description": "测距带在外侧平台重排后保持检修窗与平台边缘的相对关系，形成可返回的向上端点。",
    "evidence": "带身绷成一条直线，带壳端却没有被窗框拖走。",
    "name": "测距带跨局部重排保持空间关系",
    "object_id": "measuring-tape",
    "owner_id": "protagonist",
    "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
    "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
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
    "candidate_id": "candidate_980e32ba72d173223796f9b0",
    "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
    "created_at": "2026-08-16T17:18:02.984825+00:00",
    "edition_id": "base",
    "emotional_outcome": null,
    "ending_type": null,
    "event_source": null,
    "ordinal": 6,
    "payload_json": "{\"candidate_id\": \"candidate_980e32ba72d173223796f9b0\", \"signature\": \"function:aftershock|secondary:discovery|secondary:pressure_build\", \"source_draft_id\": \"draft_5021c9974e2cd8b3253d0ef4\", \"source_span_id\": \"canon-span_307f36eeb3ff4ba659fb82a0\", \"structure_tags\": [\"function:aftershock\", \"secondary:discovery\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_bdc502221baa5834db8b1eaf\"}",
    "payoff_type": null,
    "scene_topology": null,
    "solution_method": null,
    "status": "CANON",
    "tag_id": "repetition_bdc502221baa5834db8b1eaf",
    "version": 1
  },
  {
    "book_id": "original-e56a54687506",
    "candidate_id": "candidate_48e5f17529ba78e904f65934",
    "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
    "created_at": "2026-08-16T17:15:02.145598+00:00",
    "edition_id": "base",
    "emotional_outcome": null,
    "ending_type": null,
    "event_source": null,
    "ordinal": 5,
    "payload_json": "{\"candidate_id\": \"candidate_48e5f17529ba78e904f65934\", \"signature\": \"function:discovery|secondary:pressure_build|secondary:relationship_shift\", \"source_draft_id\": \"draft_d12d36ba1bc35e24b20a4570\", \"source_span_id\": \"canon-span_527cd52fb85756bbad483200\", \"structure_tags\": [\"function:discovery\", \"secondary:relationship_shift\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_6e3a6a47500dc4c5fcfb5e50\"}",
    "payoff_type": null,
    "scene_topology": null,
    "solution_method": null,
    "status": "CANON",
    "tag_id": "repetition_6e3a6a47500dc4c5fcfb5e50",
    "version": 1
  },
  {
    "book_id": "original-e56a54687506",
    "candidate_id": "candidate_0f95654d1507f487a9bd8248",
    "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
    "created_at": "2026-08-16T17:11:11.616879+00:00",
    "edition_id": "base",
    "emotional_outcome": null,
    "ending_type": null,
    "event_source": null,
    "ordinal": 4,
    "payload_json": "{\"candidate_id\": \"candidate_0f95654d1507f487a9bd8248\", \"signature\": \"function:choice|secondary:pressure_build|secondary:reversal\", \"source_draft_id\": \"draft_bf2bb3f1e46011392b83b872\", \"source_span_id\": \"canon-span_6a551b7a462d002ea780f449\", \"structure_tags\": [\"function:choice\", \"secondary:reversal\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_f77c3e62a0116a351e2ae3b8\"}",
    "payoff_type": null,
    "scene_topology": null,
    "solution_method": null,
    "status": "CANON",
    "tag_id": "repetition_f77c3e62a0116a351e2ae3b8",
    "version": 1
  },
  {
    "book_id": "original-e56a54687506",
    "candidate_id": "candidate_051342de3b8c0ae8359c27dd",
    "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
    "created_at": "2026-08-16T17:04:03.392995+00:00",
    "edition_id": "base",
    "emotional_outcome": null,
    "ending_type": null,
    "event_source": null,
    "ordinal": 3,
    "payload_json": "{\"candidate_id\": \"candidate_051342de3b8c0ae8359c27dd\", \"signature\": \"function:discovery|secondary:progress|secondary:world_expansion\", \"source_draft_id\": \"draft_78fbd961bd5cc5becb7a897f\", \"source_span_id\": \"canon-span_b93129f324cb473a95a8a1b8\", \"structure_tags\": [\"function:discovery\", \"secondary:progress\", \"secondary:world_expansion\"], \"tag_id\": \"repetition_3df29368be78dc1d7d27cdfd\"}",
    "payoff_type": null,
    "scene_topology": null,
    "solution_method": null,
    "status": "CANON",
    "tag_id": "repetition_3df29368be78dc1d7d27cdfd",
    "version": 1
  },
  {
    "book_id": "original-e56a54687506",
    "candidate_id": "candidate_081191a0e08eeba0e21fd5fa",
    "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
    "created_at": "2026-08-16T16:57:52.366725+00:00",
    "edition_id": "base",
    "emotional_outcome": null,
    "ending_type": null,
    "event_source": null,
    "ordinal": 2,
    "payload_json": "{\"candidate_id\": \"candidate_081191a0e08eeba0e21fd5fa\", \"signature\": \"function:discovery|secondary:progress|secondary:world_expansion\", \"source_draft_id\": \"draft_e0ea2e9d4c6fcc2a2dd17a8f\", \"source_span_id\": \"canon-span_70e5d91133cdb192b7cfb599\", \"structure_tags\": [\"function:discovery\", \"secondary:progress\", \"secondary:world_expansion\"], \"tag_id\": \"repetition_810cda8e516278fba29449ea\"}",
    "payoff_type": null,
    "scene_topology": null,
    "solution_method": null,
    "status": "CANON",
    "tag_id": "repetition_810cda8e516278fba29449ea",
    "version": 1
  },
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
  },
  {
    "analyzer_version": "rhythm-deterministic-v1",
    "book_id": "original-e56a54687506",
    "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
    "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
    "created_at": "2026-08-16T16:57:52.415732+00:00",
    "edition_id": "base",
    "effective_content_sha256": "4892fca6d6b15ead6b6518832a391acc882dc02122c39b8c205fe0cd9a95f3d7",
    "emotional_confidence": null,
    "emotional_intensity_band": "UNKNOWN",
    "ending_excerpt_prose": "检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。",
    "ending_excerpt_raw": "检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。",
    "ending_fingerprint_prose": "202375d42408da1c7f3704a30670301311b3df097c6a5360566d3dd2c8f28696",
    "ending_fingerprint_raw": "202375d42408da1c7f3704a30670301311b3df097c6a5360566d3dd2c8f28696",
    "ending_mode": "unknown",
    "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
    "extractor_kind": "DETERMINISTIC",
    "feature_id": "chapter-feature_f63b3b68d21785f664d891ae",
    "function_confidence": null,
    "invalidated_at": null,
    "normalized_title": "窗缝之外",
    "opening_excerpt_prose": "墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。\n\n随后，整层楼像有人从中间拧了一下。",
    "opening_excerpt_raw": "## 第2章 窗缝之外\n\n墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。",
    "opening_fingerprint_prose": "62677b421c3d4b76e93491a6e5b5b25cd9792398320efbf0a06c1c7fb1ea62b2",
    "opening_fingerprint_raw": "3400e2328a1287094ea73f425bce301fee76ade56fa8922fd9034725f325cc69",
    "opening_mode": "unknown",
    "ordinal": 2,
    "planned_primary_function": null,
    "realized_primary_function": null,
    "status": "ACTIVE",
    "title_fingerprint": "d3b42681e372238628ef254933dd2066bfb00c6c45d13958f9d0a5107dc44ffb",
    "title_raw": "## 第2章 窗缝之外",
    "version": 1
  },
  {
    "analyzer_version": "rhythm-deterministic-v1",
    "book_id": "original-e56a54687506",
    "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
    "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
    "created_at": "2026-08-16T17:04:03.442907+00:00",
    "edition_id": "base",
    "effective_content_sha256": "abb972661019a6b28d6d2bce5f7a2ff5e8ebafc0b453a147a2730a1b43a62404",
    "emotional_confidence": null,
    "emotional_intensity_band": "UNKNOWN",
    "ending_excerpt_prose": "平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。",
    "ending_excerpt_raw": "平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。",
    "ending_fingerprint_prose": "a40420a27163522000a5784b2b2c58e737e55d1fa78278b26d3a2d0116af3cd3",
    "ending_fingerprint_raw": "a40420a27163522000a5784b2b2c58e737e55d1fa78278b26d3a2d0116af3cd3",
    "ending_mode": "unknown",
    "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
    "extractor_kind": "DETERMINISTIC",
    "feature_id": "chapter-feature_22c98fef73ca80e12cad58a0",
    "function_confidence": null,
    "invalidated_at": null,
    "normalized_title": "没有地面的平台",
    "opening_excerpt_prose": "检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。\n\n他没有去找声音。上一轮重排已经证明，能听见不等于能抵达。",
    "opening_excerpt_raw": "## 第3章 没有地面的平台\n\n检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。",
    "opening_fingerprint_prose": "6b415b3630e68541d03aa7d7cfd91c039697894555cd8467b7ae1675d7f27fb7",
    "opening_fingerprint_raw": "03440b87728b3b379fe5c1615da9c66dfd3d610845d3103ac707ad5fcbe16285",
    "opening_mode": "unknown",
    "ordinal": 3,
    "planned_primary_function": null,
    "realized_primary_function": null,
    "status": "ACTIVE",
    "title_fingerprint": "7c6ec4f560e414a122e511ae0bcd4ad97ec1a223bbdec0661328f39a4411d9a2",
    "title_raw": "## 第3章 没有地面的平台",
    "version": 1
  },
  {
    "analyzer_version": "rhythm-deterministic-v1",
    "book_id": "original-e56a54687506",
    "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
    "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
    "created_at": "2026-08-16T17:11:11.667876+00:00",
    "edition_id": "base",
    "effective_content_sha256": "694418b4e097fc8a3f7e05b6018ecc0538efcc39c68401145c8655bcf2128ed9",
    "emotional_confidence": null,
    "emotional_intensity_band": "UNKNOWN",
    "ending_excerpt_prose": "他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。",
    "ending_excerpt_raw": "他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。",
    "ending_fingerprint_prose": "4bf77d15cb59229f188cca1bb203b8f143a9906249f5c3b94553e5b8cea485c7",
    "ending_fingerprint_raw": "4bf77d15cb59229f188cca1bb203b8f143a9906249f5c3b94553e5b8cea485c7",
    "ending_mode": "unknown",
    "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
    "extractor_kind": "DETERMINISTIC",
    "feature_id": "chapter-feature_d444723ff53163b20bfc2ad1",
    "function_confidence": null,
    "invalidated_at": null,
    "normalized_title": "屋顶在墙后",
    "opening_excerpt_prose": "检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”",
    "opening_excerpt_raw": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。",
    "opening_fingerprint_prose": "256798bc41979d151f7dbdc28282f6f8d5d90f41d26e2d2cbe2cfe59849613cc",
    "opening_fingerprint_raw": "e3aa0c2fe8136e81140fb8de8f32556b6c426ef2502571e2b51b1b5415af7f92",
    "opening_mode": "unknown",
    "ordinal": 4,
    "planned_primary_function": null,
    "realized_primary_function": null,
    "status": "ACTIVE",
    "title_fingerprint": "915f92fe940f3c9fb834e85916087fbcd67051121b27ee5457dc6a143a213862",
    "title_raw": "## 第4章 屋顶在墙后",
    "version": 1
  },
  {
    "analyzer_version": "rhythm-deterministic-v1",
    "book_id": "original-e56a54687506",
    "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
    "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
    "created_at": "2026-08-16T17:15:02.201604+00:00",
    "edition_id": "base",
    "effective_content_sha256": "928d7d826af436eaba6641d82e729310623e88d5dea258d41a90fe8e96760f1f",
    "emotional_confidence": null,
    "emotional_intensity_band": "UNKNOWN",
    "ending_excerpt_prose": "他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？",
    "ending_excerpt_raw": "他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？",
    "ending_fingerprint_prose": "44d5b21ee92a771d4ba98e928b2ce760ac94e454f254ddcdbbf8c7c8fa0ac70a",
    "ending_fingerprint_raw": "44d5b21ee92a771d4ba98e928b2ce760ac94e454f254ddcdbbf8c7c8fa0ac70a",
    "ending_mode": "unknown",
    "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
    "extractor_kind": "DETERMINISTIC",
    "feature_id": "chapter-feature_e67265c5c5d8b3882ed3fec1",
    "function_confidence": null,
    "invalidated_at": null,
    "normalized_title": "倒着写的门",
    "opening_excerpt_prose": "广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。\n\n楼层开始移动。墙根向外鼓起，倒写的痕迹被拉长，半扇门的轮廓从粉痕后显出来。门缝朝向窗外，门把手却在墙里。沈砚把测距带的带壳端压住窗台，带钩端轻轻碰到门缝上方的金属边。",
    "opening_excerpt_raw": "## 第5章 倒着写的门\n\n广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。",
    "opening_fingerprint_prose": "9b387f3a5c735d26640c05d2d182e51ea7d4448af260d37d70108273a1038c28",
    "opening_fingerprint_raw": "8eb4d1adc79896ba9edfe128ae83666c18257f30696fdb364ca75b9fb77a54af",
    "opening_mode": "unknown",
    "ordinal": 5,
    "planned_primary_function": null,
    "realized_primary_function": null,
    "status": "ACTIVE",
    "title_fingerprint": "ffc80e9fb11d98908086955e5a1f8635af436a1ed07b0aefbe9133a1c7f7d06c",
    "title_raw": "## 第5章 倒着写的门",
    "version": 1
  },
  {
    "analyzer_version": "rhythm-deterministic-v1",
    "book_id": "original-e56a54687506",
    "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
    "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
    "created_at": "2026-08-16T17:18:03.040002+00:00",
    "edition_id": "base",
    "effective_content_sha256": "04a2f68169c24cce52fe0a7246716f12256dfb749fdd4ba1e6a6369957a5b9fd",
    "emotional_confidence": null,
    "emotional_intensity_band": "UNKNOWN",
    "ending_excerpt_prose": "墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。",
    "ending_excerpt_raw": "墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。",
    "ending_fingerprint_prose": "c444c5d301b9a5926752d65e558f408aa625a54cfcd1649b9de378451812c915",
    "ending_fingerprint_raw": "c444c5d301b9a5926752d65e558f408aa625a54cfcd1649b9de378451812c915",
    "ending_mode": "unknown",
    "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
    "extractor_kind": "DETERMINISTIC",
    "feature_id": "chapter-feature_959086a66d19d06ad6318d97",
    "function_confidence": null,
    "invalidated_at": null,
    "normalized_title": "没有回声的楼梯",
    "opening_excerpt_prose": "沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。\n\n他没有先听楼梯通向哪里，而是听自己的呼吸。声音贴着窗框返回，台阶上的声音却没有回来。沈砚捏紧测距带，把带壳端压在窗台，带钩端碰向第三节扶手。",
    "opening_excerpt_raw": "## 第6章 没有回声的楼梯\n\n沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。",
    "opening_fingerprint_prose": "5b76263d791128a26b6aa591918d161826f5818a6c3f06a3bd460f687ad7e510",
    "opening_fingerprint_raw": "42becc76407055ad1a939953acfa55350ec6c5f0c0463c635394a33049ce01b0",
    "opening_mode": "unknown",
    "ordinal": 6,
    "planned_primary_function": null,
    "realized_primary_function": null,
    "status": "ACTIVE",
    "title_fingerprint": "1a1ef62812ea1ea756b97366818550a7945675fda75b68457f0a5c425e2601e7",
    "title_raw": "## 第6章 没有回声的楼梯",
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
  "as_of_chapter": 6,
  "as_of_event_seq": 43,
  "book_id": "original-e56a54687506",
  "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
  "created_at": "2026-08-16T17:18:03.132406+00:00",
  "edition_id": "base",
  "ending_mode_streak": {
    "count": 6,
    "mode": "unknown",
    "severity": "STRONG_WARNING"
  },
  "ending_similarity": {
    "matching_chapters": [],
    "max_similarity_last_4": 0.0,
    "severity": "NONE"
  },
  "evidence": [
    {
      "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 3
    },
    {
      "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 4
    },
    {
      "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 5
    },
    {
      "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 6
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
  "projection_hash": "2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c",
  "same_function_streak": {
    "count": 0,
    "function": null,
    "severity": "NONE",
    "source": "planned_primary_function"
  },
  "snapshot_id": "rhythm-snapshot_db33faabaed0d4166bdfeea1",
  "title_repetition": {
    "exact_duplicates": [],
    "matching_chapters": [],
    "max_similarity_last_20": 0.08333333333333333,
    "series_markers": [
      null,
      null,
      null,
      null,
      null,
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
  "chapter_ordinal": 7,
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
    "current_chapter": 6,
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
        "last_advanced": 6,
        "lifecycle": "DEVELOPING",
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
    "snapshot_id": "portfolio_64050a44c81ad3419e33d481",
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
  "recent_pattern_distance": "low",
  "recommendation": {
    "evidence": [
      "active_threads",
      "recent_structures",
      "earned_surface.available_payoffs"
    ],
    "pattern_distance": "low",
    "reason": [
      "最近窗口结构差异为 low，仅作为软规划信号",
      "当前存在 2 个活跃线程、0 个开放设置"
    ],
    "recommended_focus": [
      "narrative_structure",
      "character"
    ]
  },
  "repeated_patterns": [],
  "semantic_policy_leak": null,
  "window_chapters": [
    4,
    5,
    6
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
  "action_space_delta_target": "获得上方风道定位，但没有新增可站立和可返回的路径。",
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
  "boundary_packet_id": "boundary_7fe2796cdce6dd838a397b46",
  "candidate_id": "candidate_3a004e02e85de59812e1d321",
  "canon_constraints": [],
  "chapter": 7,
  "chapter_intent": "用风向把内部空段连接到更高线索，继续让广播与物理证据产生压力。",
  "commit_updates": [
    "测距带记录上方风道与无回声空段的相对关系",
    "沈砚确认风向不能单独证明屋顶存在",
    "七步脚印后的灰白断层进入可定位线索",
    "上方风道与无回声空段的关系被测距带固定为可复核方向证据。"
  ],
  "continuation_boundary": {
    "base_event_seq": 43,
    "base_projection_hash": "2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c",
    "batch_anchor": {},
    "last_canon_chapter": 6,
    "story_atlas_anchor": {}
  },
  "contract_id": "contract_6e8e2538bbdf8a8e59bc27f8",
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
    "上方风道与无回声空段的关系被测距带固定为可复核方向证据。",
    "风道位置被记录，七步脚印后的灰白边缘成为新的未知上方线索。"
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
  "ending_state": "风道位置被记录，七步脚印后的灰白边缘成为新的未知上方线索。",
  "experience_target": {
    "action_space_delta": "获得上方风道定位，但没有新增可站立和可返回的路径。",
    "core_promise_delivery": "物品进化保留方向证据而不把方向直接变成出口。",
    "emotional_outcome": "他离屋顶更近，却第一次意识到上方也可能没有建筑。",
    "ending_mode": "CONSEQUENCE",
    "event_source": "无回声楼梯合拢后，风从墙内上方连续吹出，风道口露出七步脚印之后的灰白边缘。",
    "knowledge_delta": "确认风从空段上方来；屋顶和脚印来源仍未知。",
    "outcome_magnitude": "中等强度的高处线索推进",
    "protagonist_strategy": "把风当作方向反馈，不把风声当成屋顶存在的证明。",
    "relationship_delta": "广播的屋顶提示与可测量风向再次错位。",
    "risk_form": "风道会把测距带向上卷走，空段的边缘没有可站立地面。",
    "scene_topology": "检修窗—无回声空段—上方风道—灰白断层—退回端点。",
    "social_feedback": "广播说屋顶安全，风向却从屋顶下方的空层吹来。",
    "solution_method": "用测距带对照风向、空段长度和窗台端点，确认风道位置但不追入无法保留回程的上方断层。",
    "world_scale_delta": "内部空段与高处风道形成上下相连的未知边界。"
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
      "anticipation-thread-1"
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
    "current_chapter": 6,
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
        "last_advanced": 6,
        "lifecycle": "DEVELOPING",
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
    "snapshot_id": "portfolio_64050a44c81ad3419e33d481",
    "warnings": []
  },
  "novelty_provenance": [
    {
      "causal_source": "第六章可测量的空白距离与高处脚印",
      "conflicts_checked": [
        "不确认屋顶",
        "不追入无地面风道",
        "不改变每日一次选择"
      ],
      "introduction_event": "第六章无回声楼梯留下空段",
      "new_state_if_committed": "上方风道成为空段之后的可定位方向",
      "novelty_boundary": "FORWARD_CANON_COMPATIBLE",
      "provenance": "FORWARD_NOVELTY",
      "retroactive_claim": false
    }
  ],
  "outcome_magnitude_target": "中等强度的高处线索推进",
  "payoff_channel_impact": [],
  "payoff_plan": {
    "causal_sources": [
      "canon capability measuring-tape-silent-gap-ch6",
      "canon fact silent-stair-gap-observed-ch6",
      "canon thread space-reading-route-evidence"
    ],
    "must_change_behavior": [
      "测距带记录上方风道与无回声空段的相对关系",
      "沈砚确认风向不能单独证明屋顶存在",
      "七步脚印后的灰白断层进入可定位线索",
      "上方风道与无回声空段的关系被测距带固定为可复核方向证据。"
    ],
    "state_changes": [
      "测距带记录上方风道与无回声空段的相对关系",
      "沈砚确认风向不能单独证明屋顶存在",
      "七步脚印后的灰白断层进入可定位线索"
    ]
  },
  "pressure": {
    "before": 83.0,
    "target_after": 89.0
  },
  "primary_function": "discovery",
  "primary_thread": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
  "progress": {
    "minimum_score": 25.0,
    "required_irreversible_change": "上方风道与无回声空段的关系被测距带固定为可复核方向证据。"
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
  "reader_question": "屋顶风声来自真实高处，还是来自建筑空段的回声循环？",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "recent_avoid_repetitions": [],
  "reference_provenance": {
    "application_summary": "按 reader_experiences、narrative_drives、payoff_channels、creative_problem_tags 从冻结卡片中选择 contrast-payoff-fatigue、synth-category-01、synth-category-02；仅选对照方案 contrast-payoff-fatigue-1；仅迁移可复用机制，当前书事实、状态与最终选择仍由本次合同决定。",
    "card_ids_used": [
      "contrast-payoff-fatigue",
      "synth-category-01",
      "synth-category-02"
    ],
    "match_tier": "EXACT",
    "reference_strategy_id": "planning-reference-strategy_53515584ddca4eee3f0c881c",
    "reuse_reason": null,
    "selected_solutions": [
      "contrast-payoff-fatigue-1"
    ],
    "snapshot_hash": "67260aa7ef152aaeb0cf5bdf720473e2d083ececb9774a92ee256939ff18d75a",
    "snapshot_id": "reference-context_f903364848b38121b9c0f274",
    "usage": "REFERENCE_ONLY"
  },
  "required_cost": "再次消耗当天唯一进化机会，并放弃进入风道追踪脚印。",
  "required_irreversible_change": "上方风道与无回声空段的关系被测距带固定为可复核方向证据。",
  "resource_opportunity_impact": [],
  "reveal_agenda": {
    "book_id": "original-e56a54687506",
    "chapter_ordinal": 7,
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
    "avoid_repeated_ending_mode": "unknown",
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
    "world_expansion",
    "pressure_build"
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
      "candidate_local_id": "roof-wind-channel",
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
        "DIALOGUE",
        "EMOTION",
        "RELATIONSHIP_SHIFT",
        "EXPLORATION"
      ],
      "card_id": "prose-control-dialogue-relationship-and-information",
      "card_type": "prose-control",
      "control_topic": "对话改变关系或信息",
      "failure_signals": [
        "角色重复彼此已知的信息。",
        "所有角色共用同一套口语和回应节奏。"
      ],
      "guidance": "让对白承担欲望、试探、误解、命令、让步或关系距离变化；信息可以藏在称呼、回避、回应顺序和未说完的话里。",
      "transfer_boundary": "只迁移对话承载关系和信息的抽象控制，不迁移来源角色、专名、口癖或对话句式。",
      "variants": [
        "群聊或团队用短回合叠加反应和信息差。",
        "谈判或议事用长轮次承载立场与礼序，并让回合改变下一步。",
        "关系场景让停顿、称呼和不回答承载情绪。"
      ],
      "when_to_use": [
        "对话变成角色轮流讲设定。",
        "对话结束后现场、关系和信息都没有变化。"
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
    },
    {
      "applicable_scene_functions": [
        "PAYOFF",
        "ACTION",
        "AFTERMATH",
        "DIALOGUE"
      ],
      "card_id": "prose-control-payoff-through-observable-change",
      "card_type": "prose-control",
      "control_topic": "通过可观察变化兑现回报",
      "failure_signals": [
        "为了爽点清晰增加合同之外的新成本。",
        "为了避免总结删掉作者明确要求的回报。"
      ],
      "guidance": "先让能力改变结果、资源到手、权限打开、关系推进、同行反应或世界状态变化，再补必要解释和余波。",
      "transfer_boundary": "只迁移让回报由行动和后果可见的抽象控制，不迁移来源角色、事件、能力名称或句式。",
      "variants": [
        "即时能力让现场效果先于机制解释。",
        "关系回报让手势、等待、回应或态度改变先于情绪总结。",
        "延迟回报允许局势、记忆和余波在之后完成意义。"
      ],
      "when_to_use": [
        "Payoff 被旁白宣布但现场没有可见变化。",
        "回报之后立即用同义句再次总结同一结果。"
      ]
    }
  ],
  "knowledge_gaps": [],
  "machine_bundle_hash": "3120e088142f5d75ad3f2d1d18eca36f5b89251369228b4f73c7f63e796ff9f9",
  "package_schema_version": "reference-corpus-machine-package-v1",
  "purpose": "PROSE",
  "selected_card_count": 4,
  "selected_card_ids": [
    "prose-control-action-before-interpretation",
    "prose-control-dialogue-relationship-and-information",
    "prose-control-exposition-anchored-in-need",
    "prose-control-payoff-through-observable-change"
  ],
  "selected_card_types": [
    "prose-control",
    "prose-control",
    "prose-control",
    "prose-control"
  ],
  "snapshot_hash": "23d064d2a4abc34740fea5b11e4caa00ca623e9b25b76226e0053f2bdd20fc26",
  "snapshot_id": "reference-context_be77d1c77c35a6cdbda58aa7",
  "snapshot_path": "C:\\dev\\小说续写系统\\audit\\experiments\\v3_10_chapter_continuation_expansion\\browser_smoke_20260816\\library\\original-e56a54687506\\editions\\base\\operations\\draft-task_db820e56d4300e1ada1b5a63\\input\\reference_context_snapshot.json",
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
      },
      {
        "book_id": "original-e56a54687506",
        "created_at": "2026-08-16T16:39:36.675398+00:00",
        "dependencies_json": "[]",
        "edition_id": "base",
        "goal": "确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。",
        "importance": 0.5,
        "introduced_chapter": "1",
        "last_advanced_chapter": "6",
        "payload_json": "{\"evidence\": \"沈砚只记录空段，不进入没有回声和地面的楼梯，随后沿测距带退回窗边。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"escalation\", \"source_draft_id\": \"draft_5021c9974e2cd8b3253d0ef4\", \"source_span_id\": \"canon-span_307f36eeb3ff4ba659fb82a0\", \"stakes\": \"无回声楼梯可能通向空白空间，进入会让测距带和回程一起被墙体吞掉。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "escalation",
        "progress": 0.0,
        "reader_visibility": 0.5,
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "stakes": "无回声楼梯可能通向空白空间，进入会让测距带和回程一起被墙体吞掉。",
        "status": "CANON",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "space-reading-route-evidence",
        "version": 6
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
    "base_event_seq": 43,
    "base_projection_hash": "2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c",
    "batch_anchor": {},
    "book_id": "original-e56a54687506",
    "canon_facts": {
      "external-platform-seen-ch3": {
        "_edition_id": "base",
        "_event_id": "event_60e4f30cd8ae63966f62202a",
        "_event_seq": 18,
        "_source_id": "draft_78fbd961bd5cc5becb7a897f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "重排后的检修窗外出现一块没有地面支撑的外侧平台，平台连接上方断裂风道。",
        "fact_id": "external-platform-seen-ch3",
        "knowledge_status": "UNKNOWN",
        "location_relation": "outside_external_vent_window",
        "object": "没有地面支撑的外侧平台",
        "predicate": "external_platform_observed",
        "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
        "status": "observed"
      },
      "external-vent-window-observed": {
        "_edition_id": "base",
        "_event_id": "event_b8b0234db2cdefd55535c2a5",
        "_event_seq": 11,
        "_source_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "重排后的断梯边出现一扇没有编号的检修窗，窗外有真实风和灰光。",
        "fact_id": "external-vent-window-observed",
        "knowledge_status": "UNKNOWN",
        "location_relation": "same_wall_as_measuring_tape",
        "object": "没有编号的检修窗",
        "predicate": "external_window_observed",
        "source_draft_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "source_span_id": "canon-span_70e5d91133cdb192b7cfb599",
        "status": "observed"
      },
      "false-roof-echo-observed-ch4": {
        "_edition_id": "base",
        "_event_id": "event_a5868c8ee939d0f9a8ff989c",
        "_event_seq": 25,
        "_source_id": "draft_bf2bb3f1e46011392b83b872",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "广播指向的屋顶开口与检修窗之间的相对距离发生闭合错位，声音没有可固定的真实端点。",
        "fact_id": "false-roof-echo-observed-ch4",
        "knowledge_status": "UNKNOWN",
        "location_relation": "behind_external_vent_window",
        "object": "广播回声与竖向开口",
        "predicate": "false_roof_echo_closed",
        "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "status": "observed"
      },
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
      },
      "reverse-mark-observed-ch5": {
        "_edition_id": "base",
        "_event_id": "event_2c6c0ae01e2b0d646a3e7029",
        "_event_seq": 32,
        "_source_id": "draft_d12d36ba1bc35e24b20a4570",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "检修窗附近出现一条指向已消失平台的倒写门框标记，标记在重排后仍留下可复核的方向关系。",
        "fact_id": "reverse-mark-observed-ch5",
        "knowledge_status": "UNKNOWN",
        "location_relation": "behind_external_vent_window",
        "object": "倒写门框粉痕",
        "predicate": "reverse_mark_observed",
        "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
        "source_span_id": "canon-span_527cd52fb85756bbad483200",
        "status": "observed"
      },
      "silent-stair-gap-observed-ch6": {
        "_edition_id": "base",
        "_event_id": "event_08d62929d8697d2cbc7a7060",
        "_event_seq": 39,
        "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "检修窗外短暂出现一截向下楼梯，台阶下存在没有回声和可见地面的空段。",
        "fact_id": "silent-stair-gap-observed-ch6",
        "knowledge_status": "UNKNOWN",
        "location_relation": "behind_external_vent_window",
        "object": "无回声楼梯与黑暗空段",
        "predicate": "silent_stair_gap_observed",
        "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "status": "observed"
      }
    },
    "capabilities": {
      "measuring-tape-false-roof-relation": {
        "_edition_id": "base",
        "_event_id": "event_3abb8e5a7dfebd1198e3c4ea",
        "_event_seq": 24,
        "_source_id": "draft_bf2bb3f1e46011392b83b872",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-false-roof-relation",
        "character_id": "protagonist",
        "description": "测距带记录检修窗与广播回声开口之间的闭合关系，能够把假屋顶路线固定为可复核的排除证据。",
        "evidence": "带钩端卡在孔里，带壳端却没有随着墙体后退。",
        "name": "测距带记录闭合回声关系",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "status": "ACTIVE"
      },
      "measuring-tape-reverse-mark-ch5": {
        "_edition_id": "base",
        "_event_id": "event_8eadaf620e6f52459c6d4351",
        "_event_seq": 31,
        "_source_id": "draft_d12d36ba1bc35e24b20a4570",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-reverse-mark-ch5",
        "character_id": "protagonist",
        "description": "测距带记录倒写标记与检修窗的方向关系，能把跨重排留下的陌生路线痕迹固定为可复核证据。",
        "evidence": "倒写标记与检修窗的方向关系被测距带留在铝牌上。",
        "name": "测距带记录跨重排标记方向",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
        "source_span_id": "canon-span_527cd52fb85756bbad483200",
        "status": "ACTIVE"
      },
      "measuring-tape-silent-gap-ch6": {
        "_edition_id": "base",
        "_event_id": "event_519903c0a062e0f98b32254d",
        "_event_seq": 38,
        "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-silent-gap-ch6",
        "character_id": "protagonist",
        "description": "测距带记录无回声楼梯与检修窗之间的空段关系，保留一处不可见但可复核的建筑断层。",
        "evidence": "测距带记录了无回声楼梯与窗台的空段关系。",
        "name": "测距带记录无回声空段",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "status": "ACTIVE"
      },
      "measuring-tape-space-relation": {
        "_edition_id": "base",
        "_event_id": "event_f09aece7643886d7552d9888",
        "_event_seq": 17,
        "_source_id": "draft_78fbd961bd5cc5becb7a897f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-space-relation",
        "character_id": "protagonist",
        "description": "测距带在外侧平台重排后保持检修窗与平台边缘的相对关系，形成可返回的向上端点。",
        "evidence": "带身绷成一条直线，带壳端却没有被窗框拖走。",
        "name": "测距带跨局部重排保持空间关系",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
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
      },
      "protagonist-local-evidence-choice-2": {
        "_edition_id": "base",
        "_event_id": "event_7c276de06aa34b363c3479b3",
        "_event_seq": 13,
        "_source_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "在不完整证据下先验证风、光和距离，选择测距带而不是追随广播。",
        "character_id": "protagonist",
        "cost": "失去当天让其他物品进化的机会，并暴露自己所在楼层与相邻空间的风险。",
        "source_draft_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "source_span_id": "canon-span_70e5d91133cdb192b7cfb599",
        "state_id": "protagonist-local-evidence-choice-2"
      },
      "protagonist-local-evidence-choice-3": {
        "_edition_id": "base",
        "_event_id": "event_bd6e09071d9a0d44ecae5ecb",
        "_event_seq": 20,
        "_source_id": "draft_78fbd961bd5cc5becb7a897f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "沈砚先用测距带确认平台与检修窗的关系，再踏入没有地面的外侧空间。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并暴露在平台下方没有地面的外侧边缘。",
        "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
        "state_id": "protagonist-local-evidence-choice-3"
      },
      "protagonist-local-evidence-choice-4": {
        "_edition_id": "base",
        "_event_id": "event_604b0534399e0008ca0c542e",
        "_event_seq": 27,
        "_source_id": "draft_bf2bb3f1e46011392b83b872",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "他先记录回声关系，再拒绝踏入无法保留回程的开口。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并放弃沿广播进入屋顶的可能。",
        "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "state_id": "protagonist-local-evidence-choice-4"
      },
      "protagonist-local-evidence-choice-5": {
        "_edition_id": "base",
        "_event_id": "event_d4824e51ab28c95960782fb6",
        "_event_seq": 34,
        "_source_id": "draft_d12d36ba1bc35e24b20a4570",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "沈砚把陌生标记当作观察数据，不因为它像求救就越过证据边界。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并放弃打开可能通向他人的门。",
        "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
        "source_span_id": "canon-span_527cd52fb85756bbad483200",
        "state_id": "protagonist-local-evidence-choice-5"
      },
      "protagonist-local-evidence-choice-6": {
        "_edition_id": "base",
        "_event_id": "event_45e32139060151cd07153647",
        "_event_seq": 41,
        "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "沈砚接受局部证据也可能没有答案，只记录空段，不追入无回声楼梯。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并放弃追入楼梯获取即时答案。",
        "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "state_id": "protagonist-local-evidence-choice-6"
      }
    },
    "current_position": {
      "last_canon_chapter": 6,
      "next_chapter": 7
    },
    "earlier_summaries": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "heading": "## 第1章 第一章 墙还在，路没了",
        "ordinal": 1,
        "summary": "正文停在首章 VALIDATED 边界，未执行正史批准；广播来源、门后空间和建筑成因保持未知。"
      },
      {
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "heading": "## 第2章 窗缝之外",
        "ordinal": 2,
        "summary": "正文只推进楼外风光的局部可验证事实；广播来源、建筑成因与其他幸存者规则保持未知。"
      },
      {
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "heading": "## 第3章 没有地面的平台",
        "ordinal": 3,
        "summary": "白色脚印、建筑成因、广播身份与相邻塔体关系保持未知。"
      }
    ],
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
        "current_chapter": 6,
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
            "last_advanced": 6,
            "lifecycle": "DEVELOPING",
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
        "snapshot_id": "portfolio_64050a44c81ad3419e33d481",
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
      "recent_pattern_distance": "low",
      "recommendation": {
        "evidence": [
          "active_threads",
          "recent_structures",
          "earned_surface.available_payoffs"
        ],
        "pattern_distance": "low",
        "reason": [
          "最近窗口结构差异为 low，仅作为软规划信号",
          "当前存在 2 个活跃线程、0 个开放设置"
        ],
        "recommended_focus": [
          "narrative_structure",
          "character"
        ]
      },
      "repeated_patterns": [],
      "semantic_policy_leak": null,
      "window_chapters": [
        4,
        5,
        6
      ]
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 6,
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
          "last_advanced": 6,
          "lifecycle": "DEVELOPING",
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
      "snapshot_id": "portfolio_64050a44c81ad3419e33d481",
      "warnings": []
    },
    "packet_id": "boundary_7fe2796cdce6dd838a397b46",
    "promises": {},
    "recent_full_chapters": [
      {
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "content": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”\n\n声音很近，近得像贴着检修窗的铁皮说话。沈砚没有抬头去找。上一轮他看见过倒挂的蓝色标志，也看见过标志下面没有地面。广播说的是方向，不是证据。\n\n楼层开始重排。走廊地面先向左倾，墙根的灰线被拉成一条细长的弧。检修窗外没有平台，只有一块向后缩的墙面。墙面缩到一半，忽然裂开一道竖口，冷风从里面冲出来，带着湿水泥和很淡的铁锈味。\n\n脚步声就在竖口里，一步，停顿，再一步。广播又说了一遍屋顶安全，脚步却向下传，像有人在看不见的楼梯上往低处走。竖口上方露出一角蓝色标志，方向和声音都像真的；可标志的边缘没有固定的墙，随着建筑移动，它连同竖口一起向窗边滑来。\n\n沈砚先看手里的东西。水瓶还有一半，手电的光柱已经发黄，铝牌上的折返线刚好能指回走廊。今天的机会只有一次。他没有拿水瓶去赌一口水，也没有让手电替他照亮不存在的地面。\n\n他选择测距带。\n\n带钩端甩进竖口，钩住一片没有完全脱落的金属边。墙面立刻向后缩，带身绷紧。带钩端卡在孔里，带壳端却没有随着墙体后退。沈砚盯住两端之间的弧线，等第二次移动发生。\n\n开口与检修窗的距离在闭合前先缩短又恢复，广播的屋顶声音没有固定端点。他在铝牌上划下一道短线。不是距离变回去了，而是墙后那一段空间绕着窗框折了一次。竖口看起来向前，实际却把带钩端拖向下方。若他顺着蓝色标志踏进去，下一次重排很可能会把回程折到别处。\n\n沈砚把脚放到窗台边，半个身子探向竖口。冷风从衣领灌进去，墙后没有脚下的回声，只有一阵一阵往下坠的空气。声音还在说屋顶安全，脚步声却停在他看不见的地方。\n\n他没有进入。他先记录回声关系，再拒绝踏入无法保留回程的开口。带身的弧度把竖口和窗框之间的闭合关系留在铝牌的刻线上，测距带记录了一处广播回声与真实端点不一致的闭合关系。\n\n竖口开始合拢。沈砚用力向后收带，金属钩擦过墙边，带壳端仍压在窗台上。开口只剩一掌宽时，里面传来第三下脚步，随后声音和风一起被墙体夹断。\n\n他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。\n",
        "heading": "## 第4章 屋顶在墙后",
        "ordinal": 4,
        "source_span_id": "canon-span_6a551b7a462d002ea780f449"
      },
      {
        "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
        "content": "## 第5章 倒着写的门\n\n广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。\n\n楼层开始移动。墙根向外鼓起，倒写的痕迹被拉长，半扇门的轮廓从粉痕后显出来。门缝朝向窗外，门把手却在墙里。沈砚把测距带的带壳端压住窗台，带钩端轻轻碰到门缝上方的金属边。\n\n门没有开，距离先变了。\n\n带身向右绷直，门缝却向左退。沈砚盯着刻度，确认那不是门在墙上滑动，而是墙后的空间绕着窗台换了一面。倒写标记与检修窗的方向关系被测距带留在铝牌上：它来自另一个重排状态，并且在当前状态仍能被复核。\n\n门后传来很轻的一声敲击。\n\n一下，停顿，再一下。\n\n他想起高处风道里的七步白印，却没有把敲击和脚印接在一起。现在能确认的只有声音、痕迹和一条不稳定的关系。门把手仍在墙里，门缝下面没有可见的地面；只要再向前半步，带钩端就会被门框夹住。\n\n沈砚把铝牌翻过来，写下倒着的方向。他先把陌生标记当作观察数据，不因为它像求救就越过证据边界。广播突然停了，墙后的敲击也跟着消失。沉默没有回答他，却让门缝显得比刚才更近。\n\n他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？\n",
        "heading": "## 第5章 倒着写的门",
        "ordinal": 5,
        "source_span_id": "canon-span_527cd52fb85756bbad483200"
      },
      {
        "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
        "content": "## 第6章 没有回声的楼梯\n\n沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。\n\n他没有先听楼梯通向哪里，而是听自己的呼吸。声音贴着窗框返回，台阶上的声音却没有回来。沈砚捏紧测距带，把带壳端压在窗台，带钩端碰向第三节扶手。\n\n钩子没有钩住实体。\n\n它穿过扶手下方的黑暗，落在更低处。带身先向下绷，随后又在同一刻度上松开。沈砚盯着刻度变化，确认那不是楼梯延长，而是楼梯下方存在一段没有回声、也没有可见地面的空段。测距带记录了无回声楼梯与窗台的空段关系。\n\n广播突然从远处响起：“西侧楼梯安全。”\n\n沈砚没有回答。刚才这截楼梯就在西侧墙后，声音却像从它下面传来。安全两个字没有重量，只有他的带钩端和窗台还在同一条线上。\n\n他把身体探出半步。冷气沿台阶向上涌，第三节以下的黑暗没有回风。手电光落下去，像被一层没有反射的水吞掉。那里可能有地面，也可能只有建筑重排后留下的空白；当前没有任何证据允许他选择其中一个解释。\n\n他只记录空段，不进入没有回声和地面的楼梯。\n\n墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。\n",
        "heading": "## 第6章 没有回声的楼梯",
        "ordinal": 6,
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0"
      }
    ],
    "recent_payoffs": {},
    "recent_structures": [
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_980e32ba72d173223796f9b0",
        "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
        "created_at": "2026-08-16T17:18:02.984825+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 6,
        "payload_json": "{\"candidate_id\": \"candidate_980e32ba72d173223796f9b0\", \"signature\": \"function:aftershock|secondary:discovery|secondary:pressure_build\", \"source_draft_id\": \"draft_5021c9974e2cd8b3253d0ef4\", \"source_span_id\": \"canon-span_307f36eeb3ff4ba659fb82a0\", \"structure_tags\": [\"function:aftershock\", \"secondary:discovery\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_bdc502221baa5834db8b1eaf\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_bdc502221baa5834db8b1eaf",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_48e5f17529ba78e904f65934",
        "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
        "created_at": "2026-08-16T17:15:02.145598+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 5,
        "payload_json": "{\"candidate_id\": \"candidate_48e5f17529ba78e904f65934\", \"signature\": \"function:discovery|secondary:pressure_build|secondary:relationship_shift\", \"source_draft_id\": \"draft_d12d36ba1bc35e24b20a4570\", \"source_span_id\": \"canon-span_527cd52fb85756bbad483200\", \"structure_tags\": [\"function:discovery\", \"secondary:relationship_shift\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_6e3a6a47500dc4c5fcfb5e50\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_6e3a6a47500dc4c5fcfb5e50",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_0f95654d1507f487a9bd8248",
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "created_at": "2026-08-16T17:11:11.616879+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 4,
        "payload_json": "{\"candidate_id\": \"candidate_0f95654d1507f487a9bd8248\", \"signature\": \"function:choice|secondary:pressure_build|secondary:reversal\", \"source_draft_id\": \"draft_bf2bb3f1e46011392b83b872\", \"source_span_id\": \"canon-span_6a551b7a462d002ea780f449\", \"structure_tags\": [\"function:choice\", \"secondary:reversal\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_f77c3e62a0116a351e2ae3b8\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_f77c3e62a0116a351e2ae3b8",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_051342de3b8c0ae8359c27dd",
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "created_at": "2026-08-16T17:04:03.392995+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 3,
        "payload_json": "{\"candidate_id\": \"candidate_051342de3b8c0ae8359c27dd\", \"signature\": \"function:discovery|secondary:progress|secondary:world_expansion\", \"source_draft_id\": \"draft_78fbd961bd5cc5becb7a897f\", \"source_span_id\": \"canon-span_b93129f324cb473a95a8a1b8\", \"structure_tags\": [\"function:discovery\", \"secondary:progress\", \"secondary:world_expansion\"], \"tag_id\": \"repetition_3df29368be78dc1d7d27cdfd\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_3df29368be78dc1d7d27cdfd",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_081191a0e08eeba0e21fd5fa",
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "created_at": "2026-08-16T16:57:52.366725+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 2,
        "payload_json": "{\"candidate_id\": \"candidate_081191a0e08eeba0e21fd5fa\", \"signature\": \"function:discovery|secondary:progress|secondary:world_expansion\", \"source_draft_id\": \"draft_e0ea2e9d4c6fcc2a2dd17a8f\", \"source_span_id\": \"canon-span_70e5d91133cdb192b7cfb599\", \"structure_tags\": [\"function:discovery\", \"secondary:progress\", \"secondary:world_expansion\"], \"tag_id\": \"repetition_810cda8e516278fba29449ea\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_810cda8e516278fba29449ea",
        "version": 1
      },
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
    "relevant_source_spans": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "excerpt": "…促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距…",
        "ordinal": 1,
        "raw_heading": "## 第1章 第一章 墙还在，路没了",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
      }
    ],
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
      "chapter_ordinal": 7,
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
      "as_of_chapter": 6,
      "as_of_event_seq": 43,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T17:18:03.132406+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 6,
        "mode": "unknown",
        "severity": "STRONG_WARNING"
      },
      "ending_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "evidence": [
        {
          "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 3
        },
        {
          "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 4
        },
        {
          "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 5
        },
        {
          "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 6
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
      "projection_hash": "2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_db33faabaed0d4166bdfeea1",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.08333333333333333,
        "series_markers": [
          null,
          null,
          null,
          null,
          null,
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
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T16:57:52.415732+00:00",
        "edition_id": "base",
        "effective_content_sha256": "4892fca6d6b15ead6b6518832a391acc882dc02122c39b8c205fe0cd9a95f3d7",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。",
        "ending_excerpt_raw": "检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。",
        "ending_fingerprint_prose": "202375d42408da1c7f3704a30670301311b3df097c6a5360566d3dd2c8f28696",
        "ending_fingerprint_raw": "202375d42408da1c7f3704a30670301311b3df097c6a5360566d3dd2c8f28696",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_f63b3b68d21785f664d891ae",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "窗缝之外",
        "opening_excerpt_prose": "墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。\n\n随后，整层楼像有人从中间拧了一下。",
        "opening_excerpt_raw": "## 第2章 窗缝之外\n\n墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。",
        "opening_fingerprint_prose": "62677b421c3d4b76e93491a6e5b5b25cd9792398320efbf0a06c1c7fb1ea62b2",
        "opening_fingerprint_raw": "3400e2328a1287094ea73f425bce301fee76ade56fa8922fd9034725f325cc69",
        "opening_mode": "unknown",
        "ordinal": 2,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "d3b42681e372238628ef254933dd2066bfb00c6c45d13958f9d0a5107dc44ffb",
        "title_raw": "## 第2章 窗缝之外",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:04:03.442907+00:00",
        "edition_id": "base",
        "effective_content_sha256": "abb972661019a6b28d6d2bce5f7a2ff5e8ebafc0b453a147a2730a1b43a62404",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。",
        "ending_excerpt_raw": "平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。",
        "ending_fingerprint_prose": "a40420a27163522000a5784b2b2c58e737e55d1fa78278b26d3a2d0116af3cd3",
        "ending_fingerprint_raw": "a40420a27163522000a5784b2b2c58e737e55d1fa78278b26d3a2d0116af3cd3",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_22c98fef73ca80e12cad58a0",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "没有地面的平台",
        "opening_excerpt_prose": "检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。\n\n他没有去找声音。上一轮重排已经证明，能听见不等于能抵达。",
        "opening_excerpt_raw": "## 第3章 没有地面的平台\n\n检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。",
        "opening_fingerprint_prose": "6b415b3630e68541d03aa7d7cfd91c039697894555cd8467b7ae1675d7f27fb7",
        "opening_fingerprint_raw": "03440b87728b3b379fe5c1615da9c66dfd3d610845d3103ac707ad5fcbe16285",
        "opening_mode": "unknown",
        "ordinal": 3,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "7c6ec4f560e414a122e511ae0bcd4ad97ec1a223bbdec0661328f39a4411d9a2",
        "title_raw": "## 第3章 没有地面的平台",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:11:11.667876+00:00",
        "edition_id": "base",
        "effective_content_sha256": "694418b4e097fc8a3f7e05b6018ecc0538efcc39c68401145c8655bcf2128ed9",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。",
        "ending_excerpt_raw": "他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。",
        "ending_fingerprint_prose": "4bf77d15cb59229f188cca1bb203b8f143a9906249f5c3b94553e5b8cea485c7",
        "ending_fingerprint_raw": "4bf77d15cb59229f188cca1bb203b8f143a9906249f5c3b94553e5b8cea485c7",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_d444723ff53163b20bfc2ad1",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "屋顶在墙后",
        "opening_excerpt_prose": "检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”",
        "opening_excerpt_raw": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。",
        "opening_fingerprint_prose": "256798bc41979d151f7dbdc28282f6f8d5d90f41d26e2d2cbe2cfe59849613cc",
        "opening_fingerprint_raw": "e3aa0c2fe8136e81140fb8de8f32556b6c426ef2502571e2b51b1b5415af7f92",
        "opening_mode": "unknown",
        "ordinal": 4,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "915f92fe940f3c9fb834e85916087fbcd67051121b27ee5457dc6a143a213862",
        "title_raw": "## 第4章 屋顶在墙后",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:15:02.201604+00:00",
        "edition_id": "base",
        "effective_content_sha256": "928d7d826af436eaba6641d82e729310623e88d5dea258d41a90fe8e96760f1f",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？",
        "ending_excerpt_raw": "他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？",
        "ending_fingerprint_prose": "44d5b21ee92a771d4ba98e928b2ce760ac94e454f254ddcdbbf8c7c8fa0ac70a",
        "ending_fingerprint_raw": "44d5b21ee92a771d4ba98e928b2ce760ac94e454f254ddcdbbf8c7c8fa0ac70a",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_e67265c5c5d8b3882ed3fec1",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "倒着写的门",
        "opening_excerpt_prose": "广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。\n\n楼层开始移动。墙根向外鼓起，倒写的痕迹被拉长，半扇门的轮廓从粉痕后显出来。门缝朝向窗外，门把手却在墙里。沈砚把测距带的带壳端压住窗台，带钩端轻轻碰到门缝上方的金属边。",
        "opening_excerpt_raw": "## 第5章 倒着写的门\n\n广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。",
        "opening_fingerprint_prose": "9b387f3a5c735d26640c05d2d182e51ea7d4448af260d37d70108273a1038c28",
        "opening_fingerprint_raw": "8eb4d1adc79896ba9edfe128ae83666c18257f30696fdb364ca75b9fb77a54af",
        "opening_mode": "unknown",
        "ordinal": 5,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "ffc80e9fb11d98908086955e5a1f8635af436a1ed07b0aefbe9133a1c7f7d06c",
        "title_raw": "## 第5章 倒着写的门",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:18:03.040002+00:00",
        "edition_id": "base",
        "effective_content_sha256": "04a2f68169c24cce52fe0a7246716f12256dfb749fdd4ba1e6a6369957a5b9fd",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。",
        "ending_excerpt_raw": "墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。",
        "ending_fingerprint_prose": "c444c5d301b9a5926752d65e558f408aa625a54cfcd1649b9de378451812c915",
        "ending_fingerprint_raw": "c444c5d301b9a5926752d65e558f408aa625a54cfcd1649b9de378451812c915",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_959086a66d19d06ad6318d97",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "没有回声的楼梯",
        "opening_excerpt_prose": "沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。\n\n他没有先听楼梯通向哪里，而是听自己的呼吸。声音贴着窗框返回，台阶上的声音却没有回来。沈砚捏紧测距带，把带壳端压在窗台，带钩端碰向第三节扶手。",
        "opening_excerpt_raw": "## 第6章 没有回声的楼梯\n\n沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。",
        "opening_fingerprint_prose": "5b76263d791128a26b6aa591918d161826f5818a6c3f06a3bd460f687ad7e510",
        "opening_fingerprint_raw": "42becc76407055ad1a939953acfa55350ec6c5f0c0463c635394a33049ce01b0",
        "opening_mode": "unknown",
        "ordinal": 6,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "1a1ef62812ea1ea756b97366818550a7945675fda75b68457f0a5c425e2601e7",
        "title_raw": "## 第6章 没有回声的楼梯",
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
        "last_advanced_chapter": "6",
        "payload_json": "{\"evidence\": \"沈砚只记录空段，不进入没有回声和地面的楼梯，随后沿测距带退回窗边。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"escalation\", \"source_draft_id\": \"draft_5021c9974e2cd8b3253d0ef4\", \"source_span_id\": \"canon-span_307f36eeb3ff4ba659fb82a0\", \"stakes\": \"无回声楼梯可能通向空白空间，进入会让测距带和回程一起被墙体吞掉。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "escalation",
        "progress": 0.0,
        "reader_visibility": 0.5,
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "stakes": "无回声楼梯可能通向空白空间，进入会让测距带和回程一起被墙体吞掉。",
        "status": "CANON",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "space-reading-route-evidence",
        "version": 6
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
    "base_event_seq": 43,
    "base_projection_hash": "2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c",
    "batch_anchor": {},
    "book_id": "original-e56a54687506",
    "canon_facts": {
      "external-platform-seen-ch3": {
        "_edition_id": "base",
        "_event_id": "event_60e4f30cd8ae63966f62202a",
        "_event_seq": 18,
        "_source_id": "draft_78fbd961bd5cc5becb7a897f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "重排后的检修窗外出现一块没有地面支撑的外侧平台，平台连接上方断裂风道。",
        "fact_id": "external-platform-seen-ch3",
        "knowledge_status": "UNKNOWN",
        "location_relation": "outside_external_vent_window",
        "object": "没有地面支撑的外侧平台",
        "predicate": "external_platform_observed",
        "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
        "status": "observed"
      },
      "external-vent-window-observed": {
        "_edition_id": "base",
        "_event_id": "event_b8b0234db2cdefd55535c2a5",
        "_event_seq": 11,
        "_source_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "重排后的断梯边出现一扇没有编号的检修窗，窗外有真实风和灰光。",
        "fact_id": "external-vent-window-observed",
        "knowledge_status": "UNKNOWN",
        "location_relation": "same_wall_as_measuring_tape",
        "object": "没有编号的检修窗",
        "predicate": "external_window_observed",
        "source_draft_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "source_span_id": "canon-span_70e5d91133cdb192b7cfb599",
        "status": "observed"
      },
      "false-roof-echo-observed-ch4": {
        "_edition_id": "base",
        "_event_id": "event_a5868c8ee939d0f9a8ff989c",
        "_event_seq": 25,
        "_source_id": "draft_bf2bb3f1e46011392b83b872",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "广播指向的屋顶开口与检修窗之间的相对距离发生闭合错位，声音没有可固定的真实端点。",
        "fact_id": "false-roof-echo-observed-ch4",
        "knowledge_status": "UNKNOWN",
        "location_relation": "behind_external_vent_window",
        "object": "广播回声与竖向开口",
        "predicate": "false_roof_echo_closed",
        "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "status": "observed"
      },
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
      },
      "reverse-mark-observed-ch5": {
        "_edition_id": "base",
        "_event_id": "event_2c6c0ae01e2b0d646a3e7029",
        "_event_seq": 32,
        "_source_id": "draft_d12d36ba1bc35e24b20a4570",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "检修窗附近出现一条指向已消失平台的倒写门框标记，标记在重排后仍留下可复核的方向关系。",
        "fact_id": "reverse-mark-observed-ch5",
        "knowledge_status": "UNKNOWN",
        "location_relation": "behind_external_vent_window",
        "object": "倒写门框粉痕",
        "predicate": "reverse_mark_observed",
        "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
        "source_span_id": "canon-span_527cd52fb85756bbad483200",
        "status": "observed"
      },
      "silent-stair-gap-observed-ch6": {
        "_edition_id": "base",
        "_event_id": "event_08d62929d8697d2cbc7a7060",
        "_event_seq": 39,
        "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "description": "检修窗外短暂出现一截向下楼梯，台阶下存在没有回声和可见地面的空段。",
        "fact_id": "silent-stair-gap-observed-ch6",
        "knowledge_status": "UNKNOWN",
        "location_relation": "behind_external_vent_window",
        "object": "无回声楼梯与黑暗空段",
        "predicate": "silent_stair_gap_observed",
        "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "status": "observed"
      }
    },
    "capabilities": {
      "measuring-tape-false-roof-relation": {
        "_edition_id": "base",
        "_event_id": "event_3abb8e5a7dfebd1198e3c4ea",
        "_event_seq": 24,
        "_source_id": "draft_bf2bb3f1e46011392b83b872",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-false-roof-relation",
        "character_id": "protagonist",
        "description": "测距带记录检修窗与广播回声开口之间的闭合关系，能够把假屋顶路线固定为可复核的排除证据。",
        "evidence": "带钩端卡在孔里，带壳端却没有随着墙体后退。",
        "name": "测距带记录闭合回声关系",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "status": "ACTIVE"
      },
      "measuring-tape-reverse-mark-ch5": {
        "_edition_id": "base",
        "_event_id": "event_8eadaf620e6f52459c6d4351",
        "_event_seq": 31,
        "_source_id": "draft_d12d36ba1bc35e24b20a4570",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-reverse-mark-ch5",
        "character_id": "protagonist",
        "description": "测距带记录倒写标记与检修窗的方向关系，能把跨重排留下的陌生路线痕迹固定为可复核证据。",
        "evidence": "倒写标记与检修窗的方向关系被测距带留在铝牌上。",
        "name": "测距带记录跨重排标记方向",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
        "source_span_id": "canon-span_527cd52fb85756bbad483200",
        "status": "ACTIVE"
      },
      "measuring-tape-silent-gap-ch6": {
        "_edition_id": "base",
        "_event_id": "event_519903c0a062e0f98b32254d",
        "_event_seq": 38,
        "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-silent-gap-ch6",
        "character_id": "protagonist",
        "description": "测距带记录无回声楼梯与检修窗之间的空段关系，保留一处不可见但可复核的建筑断层。",
        "evidence": "测距带记录了无回声楼梯与窗台的空段关系。",
        "name": "测距带记录无回声空段",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "status": "ACTIVE"
      },
      "measuring-tape-space-relation": {
        "_edition_id": "base",
        "_event_id": "event_f09aece7643886d7552d9888",
        "_event_seq": 17,
        "_source_id": "draft_78fbd961bd5cc5becb7a897f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "capability_id": "measuring-tape-space-relation",
        "character_id": "protagonist",
        "description": "测距带在外侧平台重排后保持检修窗与平台边缘的相对关系，形成可返回的向上端点。",
        "evidence": "带身绷成一条直线，带壳端却没有被窗框拖走。",
        "name": "测距带跨局部重排保持空间关系",
        "object_id": "measuring-tape",
        "owner_id": "protagonist",
        "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
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
      },
      "protagonist-local-evidence-choice-2": {
        "_edition_id": "base",
        "_event_id": "event_7c276de06aa34b363c3479b3",
        "_event_seq": 13,
        "_source_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "在不完整证据下先验证风、光和距离，选择测距带而不是追随广播。",
        "character_id": "protagonist",
        "cost": "失去当天让其他物品进化的机会，并暴露自己所在楼层与相邻空间的风险。",
        "source_draft_id": "draft_e0ea2e9d4c6fcc2a2dd17a8f",
        "source_span_id": "canon-span_70e5d91133cdb192b7cfb599",
        "state_id": "protagonist-local-evidence-choice-2"
      },
      "protagonist-local-evidence-choice-3": {
        "_edition_id": "base",
        "_event_id": "event_bd6e09071d9a0d44ecae5ecb",
        "_event_seq": 20,
        "_source_id": "draft_78fbd961bd5cc5becb7a897f",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "沈砚先用测距带确认平台与检修窗的关系，再踏入没有地面的外侧空间。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并暴露在平台下方没有地面的外侧边缘。",
        "source_draft_id": "draft_78fbd961bd5cc5becb7a897f",
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8",
        "state_id": "protagonist-local-evidence-choice-3"
      },
      "protagonist-local-evidence-choice-4": {
        "_edition_id": "base",
        "_event_id": "event_604b0534399e0008ca0c542e",
        "_event_seq": 27,
        "_source_id": "draft_bf2bb3f1e46011392b83b872",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "他先记录回声关系，再拒绝踏入无法保留回程的开口。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并放弃沿广播进入屋顶的可能。",
        "source_draft_id": "draft_bf2bb3f1e46011392b83b872",
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "state_id": "protagonist-local-evidence-choice-4"
      },
      "protagonist-local-evidence-choice-5": {
        "_edition_id": "base",
        "_event_id": "event_d4824e51ab28c95960782fb6",
        "_event_seq": 34,
        "_source_id": "draft_d12d36ba1bc35e24b20a4570",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "沈砚把陌生标记当作观察数据，不因为它像求救就越过证据边界。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并放弃打开可能通向他人的门。",
        "source_draft_id": "draft_d12d36ba1bc35e24b20a4570",
        "source_span_id": "canon-span_527cd52fb85756bbad483200",
        "state_id": "protagonist-local-evidence-choice-5"
      },
      "protagonist-local-evidence-choice-6": {
        "_edition_id": "base",
        "_event_id": "event_45e32139060151cd07153647",
        "_event_seq": 41,
        "_source_id": "draft_5021c9974e2cd8b3253d0ef4",
        "_source_kind": "AUTHOR_APPROVED_DRAFT",
        "change": "沈砚接受局部证据也可能没有答案，只记录空段，不追入无回声楼梯。",
        "character_id": "protagonist",
        "cost": "再次消耗当天唯一进化机会，并放弃追入楼梯获取即时答案。",
        "source_draft_id": "draft_5021c9974e2cd8b3253d0ef4",
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0",
        "state_id": "protagonist-local-evidence-choice-6"
      }
    },
    "current_position": {
      "last_canon_chapter": 6,
      "next_chapter": 7
    },
    "earlier_summaries": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "heading": "## 第1章 第一章 墙还在，路没了",
        "ordinal": 1,
        "summary": "正文停在首章 VALIDATED 边界，未执行正史批准；广播来源、门后空间和建筑成因保持未知。"
      },
      {
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "heading": "## 第2章 窗缝之外",
        "ordinal": 2,
        "summary": "正文只推进楼外风光的局部可验证事实；广播来源、建筑成因与其他幸存者规则保持未知。"
      },
      {
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "heading": "## 第3章 没有地面的平台",
        "ordinal": 3,
        "summary": "白色脚印、建筑成因、广播身份与相邻塔体关系保持未知。"
      }
    ],
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
        "current_chapter": 6,
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
            "last_advanced": 6,
            "lifecycle": "DEVELOPING",
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
        "snapshot_id": "portfolio_64050a44c81ad3419e33d481",
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
      "recent_pattern_distance": "low",
      "recommendation": {
        "evidence": [
          "active_threads",
          "recent_structures",
          "earned_surface.available_payoffs"
        ],
        "pattern_distance": "low",
        "reason": [
          "最近窗口结构差异为 low，仅作为软规划信号",
          "当前存在 2 个活跃线程、0 个开放设置"
        ],
        "recommended_focus": [
          "narrative_structure",
          "character"
        ]
      },
      "repeated_patterns": [],
      "semantic_policy_leak": null,
      "window_chapters": [
        4,
        5,
        6
      ]
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 6,
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
          "last_advanced": 6,
          "lifecycle": "DEVELOPING",
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
      "snapshot_id": "portfolio_64050a44c81ad3419e33d481",
      "warnings": []
    },
    "packet_id": "boundary_7fe2796cdce6dd838a397b46",
    "promises": {},
    "recent_full_chapters": [
      {
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "content": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”\n\n声音很近，近得像贴着检修窗的铁皮说话。沈砚没有抬头去找。上一轮他看见过倒挂的蓝色标志，也看见过标志下面没有地面。广播说的是方向，不是证据。\n\n楼层开始重排。走廊地面先向左倾，墙根的灰线被拉成一条细长的弧。检修窗外没有平台，只有一块向后缩的墙面。墙面缩到一半，忽然裂开一道竖口，冷风从里面冲出来，带着湿水泥和很淡的铁锈味。\n\n脚步声就在竖口里，一步，停顿，再一步。广播又说了一遍屋顶安全，脚步却向下传，像有人在看不见的楼梯上往低处走。竖口上方露出一角蓝色标志，方向和声音都像真的；可标志的边缘没有固定的墙，随着建筑移动，它连同竖口一起向窗边滑来。\n\n沈砚先看手里的东西。水瓶还有一半，手电的光柱已经发黄，铝牌上的折返线刚好能指回走廊。今天的机会只有一次。他没有拿水瓶去赌一口水，也没有让手电替他照亮不存在的地面。\n\n他选择测距带。\n\n带钩端甩进竖口，钩住一片没有完全脱落的金属边。墙面立刻向后缩，带身绷紧。带钩端卡在孔里，带壳端却没有随着墙体后退。沈砚盯住两端之间的弧线，等第二次移动发生。\n\n开口与检修窗的距离在闭合前先缩短又恢复，广播的屋顶声音没有固定端点。他在铝牌上划下一道短线。不是距离变回去了，而是墙后那一段空间绕着窗框折了一次。竖口看起来向前，实际却把带钩端拖向下方。若他顺着蓝色标志踏进去，下一次重排很可能会把回程折到别处。\n\n沈砚把脚放到窗台边，半个身子探向竖口。冷风从衣领灌进去，墙后没有脚下的回声，只有一阵一阵往下坠的空气。声音还在说屋顶安全，脚步声却停在他看不见的地方。\n\n他没有进入。他先记录回声关系，再拒绝踏入无法保留回程的开口。带身的弧度把竖口和窗框之间的闭合关系留在铝牌的刻线上，测距带记录了一处广播回声与真实端点不一致的闭合关系。\n\n竖口开始合拢。沈砚用力向后收带，金属钩擦过墙边，带壳端仍压在窗台上。开口只剩一掌宽时，里面传来第三下脚步，随后声音和风一起被墙体夹断。\n\n他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。\n",
        "heading": "## 第4章 屋顶在墙后",
        "ordinal": 4,
        "source_span_id": "canon-span_6a551b7a462d002ea780f449"
      },
      {
        "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
        "content": "## 第5章 倒着写的门\n\n广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。\n\n楼层开始移动。墙根向外鼓起，倒写的痕迹被拉长，半扇门的轮廓从粉痕后显出来。门缝朝向窗外，门把手却在墙里。沈砚把测距带的带壳端压住窗台，带钩端轻轻碰到门缝上方的金属边。\n\n门没有开，距离先变了。\n\n带身向右绷直，门缝却向左退。沈砚盯着刻度，确认那不是门在墙上滑动，而是墙后的空间绕着窗台换了一面。倒写标记与检修窗的方向关系被测距带留在铝牌上：它来自另一个重排状态，并且在当前状态仍能被复核。\n\n门后传来很轻的一声敲击。\n\n一下，停顿，再一下。\n\n他想起高处风道里的七步白印，却没有把敲击和脚印接在一起。现在能确认的只有声音、痕迹和一条不稳定的关系。门把手仍在墙里，门缝下面没有可见的地面；只要再向前半步，带钩端就会被门框夹住。\n\n沈砚把铝牌翻过来，写下倒着的方向。他先把陌生标记当作观察数据，不因为它像求救就越过证据边界。广播突然停了，墙后的敲击也跟着消失。沉默没有回答他，却让门缝显得比刚才更近。\n\n他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？\n",
        "heading": "## 第5章 倒着写的门",
        "ordinal": 5,
        "source_span_id": "canon-span_527cd52fb85756bbad483200"
      },
      {
        "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
        "content": "## 第6章 没有回声的楼梯\n\n沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。\n\n他没有先听楼梯通向哪里，而是听自己的呼吸。声音贴着窗框返回，台阶上的声音却没有回来。沈砚捏紧测距带，把带壳端压在窗台，带钩端碰向第三节扶手。\n\n钩子没有钩住实体。\n\n它穿过扶手下方的黑暗，落在更低处。带身先向下绷，随后又在同一刻度上松开。沈砚盯着刻度变化，确认那不是楼梯延长，而是楼梯下方存在一段没有回声、也没有可见地面的空段。测距带记录了无回声楼梯与窗台的空段关系。\n\n广播突然从远处响起：“西侧楼梯安全。”\n\n沈砚没有回答。刚才这截楼梯就在西侧墙后，声音却像从它下面传来。安全两个字没有重量，只有他的带钩端和窗台还在同一条线上。\n\n他把身体探出半步。冷气沿台阶向上涌，第三节以下的黑暗没有回风。手电光落下去，像被一层没有反射的水吞掉。那里可能有地面，也可能只有建筑重排后留下的空白；当前没有任何证据允许他选择其中一个解释。\n\n他只记录空段，不进入没有回声和地面的楼梯。\n\n墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。\n",
        "heading": "## 第6章 没有回声的楼梯",
        "ordinal": 6,
        "source_span_id": "canon-span_307f36eeb3ff4ba659fb82a0"
      }
    ],
    "recent_payoffs": {},
    "recent_structures": [
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_980e32ba72d173223796f9b0",
        "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
        "created_at": "2026-08-16T17:18:02.984825+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 6,
        "payload_json": "{\"candidate_id\": \"candidate_980e32ba72d173223796f9b0\", \"signature\": \"function:aftershock|secondary:discovery|secondary:pressure_build\", \"source_draft_id\": \"draft_5021c9974e2cd8b3253d0ef4\", \"source_span_id\": \"canon-span_307f36eeb3ff4ba659fb82a0\", \"structure_tags\": [\"function:aftershock\", \"secondary:discovery\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_bdc502221baa5834db8b1eaf\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_bdc502221baa5834db8b1eaf",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_48e5f17529ba78e904f65934",
        "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
        "created_at": "2026-08-16T17:15:02.145598+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 5,
        "payload_json": "{\"candidate_id\": \"candidate_48e5f17529ba78e904f65934\", \"signature\": \"function:discovery|secondary:pressure_build|secondary:relationship_shift\", \"source_draft_id\": \"draft_d12d36ba1bc35e24b20a4570\", \"source_span_id\": \"canon-span_527cd52fb85756bbad483200\", \"structure_tags\": [\"function:discovery\", \"secondary:relationship_shift\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_6e3a6a47500dc4c5fcfb5e50\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_6e3a6a47500dc4c5fcfb5e50",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_0f95654d1507f487a9bd8248",
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "created_at": "2026-08-16T17:11:11.616879+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 4,
        "payload_json": "{\"candidate_id\": \"candidate_0f95654d1507f487a9bd8248\", \"signature\": \"function:choice|secondary:pressure_build|secondary:reversal\", \"source_draft_id\": \"draft_bf2bb3f1e46011392b83b872\", \"source_span_id\": \"canon-span_6a551b7a462d002ea780f449\", \"structure_tags\": [\"function:choice\", \"secondary:reversal\", \"secondary:pressure_build\"], \"tag_id\": \"repetition_f77c3e62a0116a351e2ae3b8\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_f77c3e62a0116a351e2ae3b8",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_051342de3b8c0ae8359c27dd",
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "created_at": "2026-08-16T17:04:03.392995+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 3,
        "payload_json": "{\"candidate_id\": \"candidate_051342de3b8c0ae8359c27dd\", \"signature\": \"function:discovery|secondary:progress|secondary:world_expansion\", \"source_draft_id\": \"draft_78fbd961bd5cc5becb7a897f\", \"source_span_id\": \"canon-span_b93129f324cb473a95a8a1b8\", \"structure_tags\": [\"function:discovery\", \"secondary:progress\", \"secondary:world_expansion\"], \"tag_id\": \"repetition_3df29368be78dc1d7d27cdfd\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_3df29368be78dc1d7d27cdfd",
        "version": 1
      },
      {
        "book_id": "original-e56a54687506",
        "candidate_id": "candidate_081191a0e08eeba0e21fd5fa",
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "created_at": "2026-08-16T16:57:52.366725+00:00",
        "edition_id": "base",
        "emotional_outcome": null,
        "ending_type": null,
        "event_source": null,
        "ordinal": 2,
        "payload_json": "{\"candidate_id\": \"candidate_081191a0e08eeba0e21fd5fa\", \"signature\": \"function:discovery|secondary:progress|secondary:world_expansion\", \"source_draft_id\": \"draft_e0ea2e9d4c6fcc2a2dd17a8f\", \"source_span_id\": \"canon-span_70e5d91133cdb192b7cfb599\", \"structure_tags\": [\"function:discovery\", \"secondary:progress\", \"secondary:world_expansion\"], \"tag_id\": \"repetition_810cda8e516278fba29449ea\"}",
        "payoff_type": null,
        "scene_topology": null,
        "solution_method": null,
        "status": "CANON",
        "tag_id": "repetition_810cda8e516278fba29449ea",
        "version": 1
      },
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
    "relevant_source_spans": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "excerpt": "…促，只留下短促的回声，沿着新出现的楼道向更深处传去。沈砚握紧测距…",
        "ordinal": 1,
        "raw_heading": "## 第1章 第一章 墙还在，路没了",
        "source_span_id": "canon-span_96f6a1794bf43a1659c7fba2"
      }
    ],
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
      "chapter_ordinal": 7,
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
      "as_of_chapter": 6,
      "as_of_event_seq": 43,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T17:18:03.132406+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 6,
        "mode": "unknown",
        "severity": "STRONG_WARNING"
      },
      "ending_similarity": {
        "matching_chapters": [],
        "max_similarity_last_4": 0.0,
        "severity": "NONE"
      },
      "evidence": [
        {
          "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 3
        },
        {
          "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 4
        },
        {
          "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 5
        },
        {
          "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 6
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
      "projection_hash": "2e67e6270dd1a7d21ed3e4552fb2926e105ead9874af996b93f35a1e09486f9c",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_db33faabaed0d4166bdfeea1",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.08333333333333333,
        "series_markers": [
          null,
          null,
          null,
          null,
          null,
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
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T16:57:52.415732+00:00",
        "edition_id": "base",
        "effective_content_sha256": "4892fca6d6b15ead6b6518832a391acc882dc02122c39b8c205fe0cd9a95f3d7",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。",
        "ending_excerpt_raw": "检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。",
        "ending_fingerprint_prose": "202375d42408da1c7f3704a30670301311b3df097c6a5360566d3dd2c8f28696",
        "ending_fingerprint_raw": "202375d42408da1c7f3704a30670301311b3df097c6a5360566d3dd2c8f28696",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_f63b3b68d21785f664d891ae",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "窗缝之外",
        "opening_excerpt_prose": "墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。\n\n随后，整层楼像有人从中间拧了一下。",
        "opening_excerpt_raw": "## 第2章 窗缝之外\n\n墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。",
        "opening_fingerprint_prose": "62677b421c3d4b76e93491a6e5b5b25cd9792398320efbf0a06c1c7fb1ea62b2",
        "opening_fingerprint_raw": "3400e2328a1287094ea73f425bce301fee76ade56fa8922fd9034725f325cc69",
        "opening_mode": "unknown",
        "ordinal": 2,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "d3b42681e372238628ef254933dd2066bfb00c6c45d13958f9d0a5107dc44ffb",
        "title_raw": "## 第2章 窗缝之外",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:04:03.442907+00:00",
        "edition_id": "base",
        "effective_content_sha256": "abb972661019a6b28d6d2bce5f7a2ff5e8ebafc0b453a147a2730a1b43a62404",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。",
        "ending_excerpt_raw": "平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。",
        "ending_fingerprint_prose": "a40420a27163522000a5784b2b2c58e737e55d1fa78278b26d3a2d0116af3cd3",
        "ending_fingerprint_raw": "a40420a27163522000a5784b2b2c58e737e55d1fa78278b26d3a2d0116af3cd3",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_22c98fef73ca80e12cad58a0",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "没有地面的平台",
        "opening_excerpt_prose": "检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。\n\n他没有去找声音。上一轮重排已经证明，能听见不等于能抵达。",
        "opening_excerpt_raw": "## 第3章 没有地面的平台\n\n检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。",
        "opening_fingerprint_prose": "6b415b3630e68541d03aa7d7cfd91c039697894555cd8467b7ae1675d7f27fb7",
        "opening_fingerprint_raw": "03440b87728b3b379fe5c1615da9c66dfd3d610845d3103ac707ad5fcbe16285",
        "opening_mode": "unknown",
        "ordinal": 3,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "7c6ec4f560e414a122e511ae0bcd4ad97ec1a223bbdec0661328f39a4411d9a2",
        "title_raw": "## 第3章 没有地面的平台",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:11:11.667876+00:00",
        "edition_id": "base",
        "effective_content_sha256": "694418b4e097fc8a3f7e05b6018ecc0538efcc39c68401145c8655bcf2128ed9",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。",
        "ending_excerpt_raw": "他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。",
        "ending_fingerprint_prose": "4bf77d15cb59229f188cca1bb203b8f143a9906249f5c3b94553e5b8cea485c7",
        "ending_fingerprint_raw": "4bf77d15cb59229f188cca1bb203b8f143a9906249f5c3b94553e5b8cea485c7",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_d444723ff53163b20bfc2ad1",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "屋顶在墙后",
        "opening_excerpt_prose": "检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”",
        "opening_excerpt_raw": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。",
        "opening_fingerprint_prose": "256798bc41979d151f7dbdc28282f6f8d5d90f41d26e2d2cbe2cfe59849613cc",
        "opening_fingerprint_raw": "e3aa0c2fe8136e81140fb8de8f32556b6c426ef2502571e2b51b1b5415af7f92",
        "opening_mode": "unknown",
        "ordinal": 4,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "915f92fe940f3c9fb834e85916087fbcd67051121b27ee5457dc6a143a213862",
        "title_raw": "## 第4章 屋顶在墙后",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_527cd52fb85756bbad483200",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:15:02.201604+00:00",
        "edition_id": "base",
        "effective_content_sha256": "928d7d826af436eaba6641d82e729310623e88d5dea258d41a90fe8e96760f1f",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？",
        "ending_excerpt_raw": "他没有开门。\n\n建筑再次重排，粉痕从中间断开，半扇门向墙内折去。沈砚向后收带，带钩端擦过门边，带壳端仍压在窗台。等最后一线缝隙闭上，他退回走廊，掌心留下细细的白粉。\n\n倒写标记还在铝牌上，门却不在了。沈砚知道楼里可能存在别人的路径，却不能把一条痕迹写成一个人。他把铝牌收进衣袋，重新看向西侧楼梯的方向。下一次重排前，他至少保住了一个问题：是谁在不同的建筑状态里，试图留下同一条路？",
        "ending_fingerprint_prose": "44d5b21ee92a771d4ba98e928b2ce760ac94e454f254ddcdbbf8c7c8fa0ac70a",
        "ending_fingerprint_raw": "44d5b21ee92a771d4ba98e928b2ce760ac94e454f254ddcdbbf8c7c8fa0ac70a",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_e67265c5c5d8b3882ed3fec1",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "倒着写的门",
        "opening_excerpt_prose": "广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。\n\n楼层开始移动。墙根向外鼓起，倒写的痕迹被拉长，半扇门的轮廓从粉痕后显出来。门缝朝向窗外，门把手却在墙里。沈砚把测距带的带壳端压住窗台，带钩端轻轻碰到门缝上方的金属边。",
        "opening_excerpt_raw": "## 第5章 倒着写的门\n\n广播改报西侧楼梯后，检修窗外的风没有立刻停。沈砚把铝牌上的新刻短线压在窗台边，测距带仍绕在腕上。上一轮竖口已经合拢，墙面看起来完整，只有一块灰白色粉痕从墙脚反向爬上去，像有人把门框倒着写在墙上。\n\n他没有马上靠近。粉痕离窗台三步，方向却指向已经消失的平台。广播又说了一次屋顶安全，声音比刚才更远，尾音被墙体切成两段。沈砚蹲下，用手电照那道痕。灰白线条不是新鲜粉笔，边缘被潮气泡过，里面还压着细小的水泥颗粒。",
        "opening_fingerprint_prose": "9b387f3a5c735d26640c05d2d182e51ea7d4448af260d37d70108273a1038c28",
        "opening_fingerprint_raw": "8eb4d1adc79896ba9edfe128ae83666c18257f30696fdb364ca75b9fb77a54af",
        "opening_mode": "unknown",
        "ordinal": 5,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "ffc80e9fb11d98908086955e5a1f8635af436a1ed07b0aefbe9133a1c7f7d06c",
        "title_raw": "## 第5章 倒着写的门",
        "version": 1
      },
      {
        "analyzer_version": "rhythm-deterministic-v1",
        "book_id": "original-e56a54687506",
        "chapter_id": "canon-chapter_307f36eeb3ff4ba659fb82a0",
        "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
        "created_at": "2026-08-16T17:18:03.040002+00:00",
        "edition_id": "base",
        "effective_content_sha256": "04a2f68169c24cce52fe0a7246716f12256dfb749fdd4ba1e6a6369957a5b9fd",
        "emotional_confidence": null,
        "emotional_intensity_band": "UNKNOWN",
        "ending_excerpt_prose": "墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。",
        "ending_excerpt_raw": "墙体开始收拢。楼梯第一节向上折，扶手擦过测距带，金属声短促地响了一下。沈砚向后收带，带壳端仍压在窗台；当楼梯只剩两级时，带钩端终于滑脱，黑暗和台阶一起被墙面抹平。\n\n广播继续报着西侧楼梯，声音越来越远。沈砚看着测距带上的一段空白刻度，那是刚才没有回声的距离。它没有告诉他楼梯通向哪里，却证明建筑里确实存在一块无法用声音填满的空间。\n\n他把空白距离写在铝牌背面，和倒写标记并排放好。下一次重排前，他要先找到能让这段空白出现第二次的端点。",
        "ending_fingerprint_prose": "c444c5d301b9a5926752d65e558f408aa625a54cfcd1649b9de378451812c915",
        "ending_fingerprint_raw": "c444c5d301b9a5926752d65e558f408aa625a54cfcd1649b9de378451812c915",
        "ending_mode": "unknown",
        "evidence_json": "{\"ending_paragraph_count\": 3, \"opening_paragraph_count\": 3, \"title_series_marker\": null}",
        "extractor_kind": "DETERMINISTIC",
        "feature_id": "chapter-feature_959086a66d19d06ad6318d97",
        "function_confidence": null,
        "invalidated_at": null,
        "normalized_title": "没有回声的楼梯",
        "opening_excerpt_prose": "沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。\n\n他没有先听楼梯通向哪里，而是听自己的呼吸。声音贴着窗框返回，台阶上的声音却没有回来。沈砚捏紧测距带，把带壳端压在窗台，带钩端碰向第三节扶手。",
        "opening_excerpt_raw": "## 第6章 没有回声的楼梯\n\n沈砚把铝牌收进衣袋时，墙后的敲击声又响了一次。\n\n这一次没有门，也没有广播。检修窗外的墙面向内折，露出一截向下的楼梯。楼梯只有六级，台阶边缘全是灰，像从一座被水泡过的旧楼里截出来。沈砚把手电照下去，光柱落在第五级，那里没有墙，也没有底。",
        "opening_fingerprint_prose": "5b76263d791128a26b6aa591918d161826f5818a6c3f06a3bd460f687ad7e510",
        "opening_fingerprint_raw": "42becc76407055ad1a939953acfa55350ec6c5f0c0463c635394a33049ce01b0",
        "opening_mode": "unknown",
        "ordinal": 6,
        "planned_primary_function": null,
        "realized_primary_function": null,
        "status": "ACTIVE",
        "title_fingerprint": "1a1ef62812ea1ea756b97366818550a7945675fda75b68457f0a5c425e2601e7",
        "title_raw": "## 第6章 没有回声的楼梯",
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