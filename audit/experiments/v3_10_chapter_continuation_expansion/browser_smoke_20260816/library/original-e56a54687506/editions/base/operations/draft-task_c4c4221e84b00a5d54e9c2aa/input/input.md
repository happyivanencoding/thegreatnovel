# 章节正文任务 `draft-task_c4c4221e84b00a5d54e9c2aa`

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
    "倒写标记与检修窗的方向关系被测距带记录为可复核的未知路径证据。",
    "倒写标记被记录为未知路线证据，门没有打开，测距带端点仍可返回。"
  ],
  "micro_event_rule": "允许只改变人物感知、动作或场面反应的 realization-only micro-event；不得改变 Contract、Canon、Knowledge、Resource 或 Capability。",
  "realization_scope": "CONTRACT_PLUS_MICRO_EVENTS",
  "target_scene_count": 3,
  "target_word_range": [
    841,
    1876
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

# Continuation Boundary Packet `boundary_279443cf5d5079c403f3b8c8`

- book_id: `original-e56a54687506`
- base_event_seq: 29
- projection_sha256: `ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31`
- current_position: {"last_canon_chapter": 4, "next_chapter": 5}

## 最近完整章节

### ## 第2章 窗缝之外

source_span_id: `canon-span_70e5d91133cdb192b7cfb599`

## 第2章 窗缝之外

墙里的声音先停了一拍。

沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。

随后，整层楼像有人从中间拧了一下。

瓷砖发出连续的脆响，脚下的地面先向左沉，再猛地抬起。沈砚肩膀撞上墙，手里的铝牌掉在地上，沿着墙角滑出半尺。远处传来广播，声音比刚才近，像贴在门缝里说话。

“十七层，天气晴。请沿东侧楼梯上行。”

他看向手表。表盘没有停，指针却在震。东侧原本是封死的储物间，第一章的重排之后，那面墙已经折到他身后。广播说得很肯定，建筑却没有给出任何能对上的东西。

一股冷风从脚边掠过。不是走廊尽头的穿堂风，而是从两块墙体之间挤出来的细风，带着湿冷的水泥味。沈砚蹲下去，把手掌贴在地面。地面仍是实的，风却从墙内穿出，断断续续，像外面有一片没有被楼层吞掉的空地。

墙角慢慢裂开一条缝。缝隙只有两指宽，另一边没有黑暗，反而透出一层发白的灰光。灰光一闪就灭，墙面又向内合拢。

他第一反应是去拿手电。手电可以照清缝里的边，水可以让他撑过下一次重排，铝牌能留下新的标记。三件东西都在手边，只有一件能在今天改变。

沈砚把手电按灭，又把半瓶水按回腰侧。他没有碰铝牌，只把测距带从腕上解下来。

如果那条缝只是建筑变形留下的空隙，照亮它没有用；如果缝的两端属于不同的墙面，铝牌也只能替他记住一个错误位置。测距带已经证明过一次关系可以留下来。现在需要确认的是，关系能不能穿过这条正在收拢的缝。

他在心里把今天的选择说清楚：测距带跨局部重排保持空间关系。

那句话落下的瞬间，带壳端的金属边缘传来一声极轻的鸣响。没有光，也没有突兀的热。测距带只是变得更沉，像里面多了一根看不见的骨头。它的刻度没有变化，带身贴过墙角时，却没有被墙体的错位带偏。

沈砚先伸出两根手指，量缝隙从哪一段开始。墙面正在移动，左侧瓷砖向下错了半格，右侧的水泥边却保持着原来的斜角。他把带钩端探进去，钩住另一边裸露的钢筋。

墙缝突然合拢。

带身绷紧，沈砚的手腕被拖得向前一沉。钩端没有脱落，带壳端也没有被拉进墙里。两端之间仍是二点九四米。不是刚才那面墙与断梯之间的旧数字，而是这一处新缝隙两端的关系。

他没有急着往里钻。先把钩端收回，再重新送入；第二次，墙面向外折了一寸，缝隙里出现一块锈蚀的百叶窗。百叶窗后面有风，风把灰尘吹成一条窄窄的斜线。

测距带在窄缝重排后仍保持两端对同一墙面的关系。沈砚盯着那条斜线，知道这不是一句解释，而是一个可以重复的结果。他把带壳端压在墙根，以带身的弧度记下角度，再将带钩端挂到百叶窗下方的固定孔。

这一次，窗框没有随墙面一起消失。

他侧身挤过去。肩胛骨擦过剥落的腻子，衣服被一根突出的铁丝勾住。窗后的空间并不宽，只够一个人半蹲着转身。墙外没有地面，只有两座被灰雾隔开的楼体。更远处的天空呈铅色，云层压得很低，风从两座楼之间穿过去，带动百叶片发出细碎的撞击声。

楼外的风是真的。灰光也是真的。

沈砚伸手摸到窗台。窗台上积着一层湿灰，指腹留下清楚的五道痕。他没有把手探得更远。相邻塔体之间看不见地面，下面像被一整块黑色的墙封住。这里能看见外面，却不是出口。

广播又响了。

“十七层，东侧楼梯，距离三十米。”

声音从窗外传来，又从他身后的走廊回了一遍。两个方向的尾音几乎同时结束。沈砚回头，看到走廊尽头的墙上多出一块蓝色标牌，牌面朝向他，写着一个被折断的数字。

他没有去追声音。测距带的带钩端还挂在窗下，带身从窗缝一直拉回原来的墙根。它把检修窗和室内的墙面连成一条可复核的向外路线。这个结果已经足够重要，重要到不需要再替广播证明它自己。

沈砚用铝牌在窗框内侧轻轻刮了一道，留下浅白的折返线。然后他把带钩端收回，重新测了一遍。两端之间仍是二点九四米。

检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。

他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。

沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。


### ## 第3章 没有地面的平台

source_span_id: `canon-span_b93129f324cb473a95a8a1b8`

## 第3章 没有地面的平台

检修窗只剩下一条黑线。

沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。

他没有去找声音。上一轮重排已经证明，能听见不等于能抵达。

楼层又开始移动。墙体先向后退，接着从窗缝的位置向外鼓起。黑线被拉成一道斜口，冷光从斜口上方落下来。沈砚压低身体，看到窗外原本悬空的灰雾里多出一块平台。它没有栏杆，边缘像被从另一座楼上硬生生撕下来，底部直接没进黑暗。

平台离窗台不远，近得像伸手就能摸到；但它和窗台之间的距离正在一寸一寸改变。沈砚先看自己的东西。半瓶水还在腰侧，手电的电量不多，铝牌上的折返线已经被磨得发白。测距带最稳，也最适合回答一个问题：这块平台究竟是不是一条会把人送进空中的假路。

他选择测距带。

带钩端甩出窗外，第一次只擦到平台的边。第二次，钩子卡住一处没有锈穿的孔。墙体立刻向上错动，平台跟着向右滑。带身绷成一条直线，带壳端却没有被窗框拖走。

测距带保持检修窗与外侧平台的相对关系。沈砚盯着刻度，等平台再动一次。窗台和平台边缘同时向前，间距没有消失，带身的弧度反而替他标出了下一次移动的方向。

这不是把平台钉在原地。平台仍会移动，风也仍会把他的衣角向外拽。测距带只保留两端之间的关系，给他一条能够回来的线。

沈砚先把一只脚探出去。鞋底碰到平台时，平台向下沉了一寸，黑暗从边缘翻上来。他没有再往前，先蹲下，用手摸平台表面。粗糙的水泥上有几道被雨水冲开的白痕，白痕朝着上方的风道延伸。

建筑把检修窗外的相邻塔体推近，外侧平台真正出现在灰雾里。沈砚在心里记住这个事实，却没有把它当成稳定的楼层。下一次重排可能让平台贴到别的墙，也可能让它彻底消失。

广播突然变得清晰。

“屋顶安全。向前三十米。”

平台尽头确实有一块蓝色标志，却是倒挂的。标志下方没有屋顶，只有一截被折断的风道。风从断口冲出来，把一小撮白灰吹到沈砚鞋面上。

他把测距带往前收了半米，测试平台边缘和窗框的关系是否还在。带钩端没有松，带壳端也没有滑。两端之间仍能被同一条线解释。沈砚这才挪出第二步，跨过平台上那道积水的裂缝。

裂缝下面没有楼层。远处两座塔体的墙皮在灰雾里互相遮挡，像两块缓慢合拢的门。沈砚看到更高处的风道里有一串白色脚印，脚印只出现了七步，到了断口便没有了。

他没有追过去。那不是已经确认的人，也不是可以调用的路线。它只是一种留在现场的未知痕迹。

平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。

窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。

测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。


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


## 更早章节摘要

```json
[
  {
    "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
    "heading": "## 第1章 第一章 墙还在，路没了",
    "ordinal": 1,
    "summary": "正文停在首章 VALIDATED 边界，未执行正史批准；广播来源、门后空间和建筑成因保持未知。"
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
    "last_advanced_chapter": "4",
    "payload_json": "{\"evidence\": \"沈砚退回窗边，仍能沿测距带找回走廊。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"escalation\", \"source_draft_id\": \"draft_bf2bb3f1e46011392b83b872\", \"source_span_id\": \"canon-span_6a551b7a462d002ea780f449\", \"stakes\": \"广播把无法保留回程的开口报成屋顶，错误进入会让测距带和回程一起被建筑夹断。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
    "phase": "escalation",
    "progress": 0.0,
    "reader_visibility": 0.5,
    "source_span_id": "canon-span_6a551b7a462d002ea780f449",
    "stakes": "广播把无法保留回程的开口报成屋顶，错误进入会让测距带和回程一起被建筑夹断。",
    "status": "CANON",
    "target_payoff_max": null,
    "target_payoff_min": null,
    "thread_id": "space-reading-route-evidence",
    "version": 4
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
  "as_of_chapter": 4,
  "as_of_event_seq": 29,
  "book_id": "original-e56a54687506",
  "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
  "created_at": "2026-08-16T17:11:11.759865+00:00",
  "edition_id": "base",
  "ending_mode_streak": {
    "count": 4,
    "mode": "unknown",
    "severity": "WARNING"
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
    },
    {
      "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 2
    },
    {
      "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 3
    },
    {
      "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
      "extractor_kind": "DETERMINISTIC",
      "ordinal": 4
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
  "projection_hash": "ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31",
  "same_function_streak": {
    "count": 0,
    "function": null,
    "severity": "NONE",
    "source": "planned_primary_function"
  },
  "snapshot_id": "rhythm-snapshot_11a27d6489b278d95c569ff0",
  "title_repetition": {
    "exact_duplicates": [],
    "matching_chapters": [],
    "max_similarity_last_20": 0.0,
    "series_markers": [
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
    "current_chapter": 4,
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
        "last_advanced": 4,
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
    "snapshot_id": "portfolio_ac8e781b331c3d3bcd8f7f85",
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
    2,
    3,
    4
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
  "action_space_delta_target": "获得一条可能来自幸存者的标记线索，但没有新增可安全进入的路线。",
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
  "boundary_packet_id": "boundary_279443cf5d5079c403f3b8c8",
  "candidate_id": "candidate_48e5f17529ba78e904f65934",
  "canon_constraints": [],
  "chapter": 5,
  "chapter_intent": "让潜在他者以物理痕迹进入故事，但继续遵守知识边界和回程压力。",
  "commit_updates": [
    "测距带记录倒写标记与检修窗的空间方向",
    "沈砚确认标记来自不同重排状态的可见痕迹",
    "陌生路径线索进入主线程但来源保持未知",
    "倒写标记与检修窗的方向关系被测距带记录为可复核的未知路径证据。"
  ],
  "continuation_boundary": {
    "base_event_seq": 29,
    "base_projection_hash": "ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31",
    "batch_anchor": {},
    "last_canon_chapter": 4,
    "story_atlas_anchor": {}
  },
  "contract_id": "contract_ef0a63f05b6211db32074bc4",
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
    "倒写标记与检修窗的方向关系被测距带记录为可复核的未知路径证据。",
    "倒写标记被记录为未知路线证据，门没有打开，测距带端点仍可返回。"
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
  "ending_state": "倒写标记被记录为未知路线证据，门没有打开，测距带端点仍可返回。",
  "experience_target": {
    "action_space_delta": "获得一条可能来自幸存者的标记线索，但没有新增可安全进入的路线。",
    "core_promise_delivery": "空间测量把未知关系变成证据，但不提前创建社会系统。",
    "emotional_outcome": "他第一次感到建筑里可能存在别人的路径，却只能把接触推迟。",
    "ending_mode": "CONSEQUENCE",
    "event_source": "竖口合拢后的墙面露出半扇倒写编号的门，门缝朝向已消失的平台。",
    "knowledge_delta": "确认标记在重排后仍可留下方向关系；其作者和意图未知。",
    "outcome_magnitude": "中等强度的未知关系推进",
    "protagonist_strategy": "先把陌生标记当作观察数据，不因为它像求救就越过证据边界。",
    "relationship_delta": "沈砚与潜在幸存者的关系从想象变成局部物理证据。",
    "risk_form": "门会在重排中反向闭合，打开它可能丢失窗边端点。",
    "scene_topology": "检修窗—闭合竖口—倒写标记—半扇门—旧平台方向。",
    "social_feedback": "广播在倒写门后短暂静音，沉默比错误播报更像一次回应。",
    "solution_method": "用测距带把反向标记与窗台关系固定，记录其方向变化，不打开无法保留回程的门。",
    "world_scale_delta": "建筑中可能存在的其他行动者获得第一处可复核痕迹。"
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
    "current_chapter": 4,
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
        "last_advanced": 4,
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
    "snapshot_id": "portfolio_ac8e781b331c3d3bcd8f7f85",
    "warnings": []
  },
  "novelty_provenance": [
    {
      "causal_source": "第四章闭合墙面和遗留的高处脚印",
      "conflicts_checked": [
        "不确认标记作者",
        "不打开门",
        "不建立幸存者阵营"
      ],
      "introduction_event": "第四章首次确认广播开口不能提供回程",
      "new_state_if_committed": "倒写标记成为未知路径证据",
      "novelty_boundary": "FORWARD_CANON_COMPATIBLE",
      "provenance": "FORWARD_NOVELTY",
      "retroactive_claim": false
    }
  ],
  "outcome_magnitude_target": "中等强度的未知关系推进",
  "payoff_channel_impact": [],
  "payoff_plan": {
    "causal_sources": [
      "canon capability measuring-tape-false-roof-relation",
      "canon fact false-roof-echo-observed-ch4",
      "canon thread space-reading-route-evidence"
    ],
    "must_change_behavior": [
      "测距带记录倒写标记与检修窗的空间方向",
      "沈砚确认标记来自不同重排状态的可见痕迹",
      "陌生路径线索进入主线程但来源保持未知",
      "倒写标记与检修窗的方向关系被测距带记录为可复核的未知路径证据。"
    ],
    "state_changes": [
      "测距带记录倒写标记与检修窗的空间方向",
      "沈砚确认标记来自不同重排状态的可见痕迹",
      "陌生路径线索进入主线程但来源保持未知"
    ]
  },
  "pressure": {
    "before": 77.0,
    "target_after": 83.0
  },
  "primary_function": "discovery",
  "primary_thread": "thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower",
  "progress": {
    "minimum_score": 25.0,
    "required_irreversible_change": "倒写标记与检修窗的方向关系被测距带记录为可复核的未知路径证据。"
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
  "reader_question": "墙后的反向标记是幸存者留下的路线，还是建筑自身的重复痕迹？",
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
    "reference_strategy_id": "planning-reference-strategy_b25692309649de81cafbfe4f",
    "reuse_reason": null,
    "selected_solutions": [
      "contrast-payoff-fatigue-1"
    ],
    "snapshot_hash": "a91367fd7151bd6e62dd96a20bb104b53cfde98060ab8fa9194ac45b3bcd23c4",
    "snapshot_id": "reference-context_0372f78568c5a130adac0e69",
    "usage": "REFERENCE_ONLY"
  },
  "required_cost": "放弃当天其他物品进化机会，并拒绝打开无法保留回程的门。",
  "required_irreversible_change": "倒写标记与检修窗的方向关系被测距带记录为可复核的未知路径证据。",
  "resource_opportunity_impact": [],
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
    "relationship_shift",
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
      "candidate_local_id": "reverse-mark",
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
        "EMOTION",
        "AFTERMATH",
        "DIALOGUE",
        "RELATIONSHIP_SHIFT"
      ],
      "card_id": "prose-control-emotion-consequence-and-silence",
      "card_type": "prose-control",
      "control_topic": "通过后果与沉默承载情绪",
      "failure_signals": [
        "把所有情绪都写成隐晦沉默，删除角色应有的明确表达。",
        "用诗性总结盖住合同要求落地的选择。"
      ],
      "guidance": "让情绪通过动作、身体反应、沉默、关系距离、信息不完整和选择后果落地；不把同一情绪连续翻译成多层同义总结。",
      "transfer_boundary": "只迁移情绪由可见后果承载的抽象控制，不迁移来源人物、场面、隐喻或情绪口吻。",
      "variants": [
        "亲密关系用目光、手势、等待和没有说出口的话。",
        "公共关系用称呼、礼序、位置和群体反应。",
        "回报余波回到生活、认可或新的选择，不强行升华。"
      ],
      "when_to_use": [
        "文字连续命名震惊、悲伤或复杂，却没有新的动作、信息或关系变化。",
        "需要让安静余波保留未解决感受时。"
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
  "selected_card_count": 4,
  "selected_card_ids": [
    "prose-control-action-before-interpretation",
    "prose-control-dialogue-relationship-and-information",
    "prose-control-emotion-consequence-and-silence",
    "prose-control-exposition-anchored-in-need"
  ],
  "selected_card_types": [
    "prose-control",
    "prose-control",
    "prose-control",
    "prose-control"
  ],
  "snapshot_hash": "23b0bb702f1bcfd55f3a286a380d5a42d9df20ec04e25b2805aae15a43eef550",
  "snapshot_id": "reference-context_dc1fdc18b12ab7218a123949",
  "snapshot_path": "C:\\dev\\小说续写系统\\audit\\experiments\\v3_10_chapter_continuation_expansion\\browser_smoke_20260816\\library\\original-e56a54687506\\editions\\base\\operations\\draft-task_c4c4221e84b00a5d54e9c2aa\\input\\reference_context_snapshot.json",
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
        "last_advanced_chapter": "4",
        "payload_json": "{\"evidence\": \"沈砚退回窗边，仍能沿测距带找回走廊。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"escalation\", \"source_draft_id\": \"draft_bf2bb3f1e46011392b83b872\", \"source_span_id\": \"canon-span_6a551b7a462d002ea780f449\", \"stakes\": \"广播把无法保留回程的开口报成屋顶，错误进入会让测距带和回程一起被建筑夹断。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "escalation",
        "progress": 0.0,
        "reader_visibility": 0.5,
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "stakes": "广播把无法保留回程的开口报成屋顶，错误进入会让测距带和回程一起被建筑夹断。",
        "status": "CANON",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "space-reading-route-evidence",
        "version": 4
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
    "base_event_seq": 29,
    "base_projection_hash": "ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31",
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
      }
    },
    "current_position": {
      "last_canon_chapter": 4,
      "next_chapter": 5
    },
    "earlier_summaries": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "heading": "## 第1章 第一章 墙还在，路没了",
        "ordinal": 1,
        "summary": "正文停在首章 VALIDATED 边界，未执行正史批准；广播来源、门后空间和建筑成因保持未知。"
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
        "current_chapter": 4,
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
            "last_advanced": 4,
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
        "snapshot_id": "portfolio_ac8e781b331c3d3bcd8f7f85",
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
        2,
        3,
        4
      ]
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 4,
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
          "last_advanced": 4,
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
      "snapshot_id": "portfolio_ac8e781b331c3d3bcd8f7f85",
      "warnings": []
    },
    "packet_id": "boundary_279443cf5d5079c403f3b8c8",
    "promises": {},
    "recent_full_chapters": [
      {
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "content": "## 第2章 窗缝之外\n\n墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。\n\n随后，整层楼像有人从中间拧了一下。\n\n瓷砖发出连续的脆响，脚下的地面先向左沉，再猛地抬起。沈砚肩膀撞上墙，手里的铝牌掉在地上，沿着墙角滑出半尺。远处传来广播，声音比刚才近，像贴在门缝里说话。\n\n“十七层，天气晴。请沿东侧楼梯上行。”\n\n他看向手表。表盘没有停，指针却在震。东侧原本是封死的储物间，第一章的重排之后，那面墙已经折到他身后。广播说得很肯定，建筑却没有给出任何能对上的东西。\n\n一股冷风从脚边掠过。不是走廊尽头的穿堂风，而是从两块墙体之间挤出来的细风，带着湿冷的水泥味。沈砚蹲下去，把手掌贴在地面。地面仍是实的，风却从墙内穿出，断断续续，像外面有一片没有被楼层吞掉的空地。\n\n墙角慢慢裂开一条缝。缝隙只有两指宽，另一边没有黑暗，反而透出一层发白的灰光。灰光一闪就灭，墙面又向内合拢。\n\n他第一反应是去拿手电。手电可以照清缝里的边，水可以让他撑过下一次重排，铝牌能留下新的标记。三件东西都在手边，只有一件能在今天改变。\n\n沈砚把手电按灭，又把半瓶水按回腰侧。他没有碰铝牌，只把测距带从腕上解下来。\n\n如果那条缝只是建筑变形留下的空隙，照亮它没有用；如果缝的两端属于不同的墙面，铝牌也只能替他记住一个错误位置。测距带已经证明过一次关系可以留下来。现在需要确认的是，关系能不能穿过这条正在收拢的缝。\n\n他在心里把今天的选择说清楚：测距带跨局部重排保持空间关系。\n\n那句话落下的瞬间，带壳端的金属边缘传来一声极轻的鸣响。没有光，也没有突兀的热。测距带只是变得更沉，像里面多了一根看不见的骨头。它的刻度没有变化，带身贴过墙角时，却没有被墙体的错位带偏。\n\n沈砚先伸出两根手指，量缝隙从哪一段开始。墙面正在移动，左侧瓷砖向下错了半格，右侧的水泥边却保持着原来的斜角。他把带钩端探进去，钩住另一边裸露的钢筋。\n\n墙缝突然合拢。\n\n带身绷紧，沈砚的手腕被拖得向前一沉。钩端没有脱落，带壳端也没有被拉进墙里。两端之间仍是二点九四米。不是刚才那面墙与断梯之间的旧数字，而是这一处新缝隙两端的关系。\n\n他没有急着往里钻。先把钩端收回，再重新送入；第二次，墙面向外折了一寸，缝隙里出现一块锈蚀的百叶窗。百叶窗后面有风，风把灰尘吹成一条窄窄的斜线。\n\n测距带在窄缝重排后仍保持两端对同一墙面的关系。沈砚盯着那条斜线，知道这不是一句解释，而是一个可以重复的结果。他把带壳端压在墙根，以带身的弧度记下角度，再将带钩端挂到百叶窗下方的固定孔。\n\n这一次，窗框没有随墙面一起消失。\n\n他侧身挤过去。肩胛骨擦过剥落的腻子，衣服被一根突出的铁丝勾住。窗后的空间并不宽，只够一个人半蹲着转身。墙外没有地面，只有两座被灰雾隔开的楼体。更远处的天空呈铅色，云层压得很低，风从两座楼之间穿过去，带动百叶片发出细碎的撞击声。\n\n楼外的风是真的。灰光也是真的。\n\n沈砚伸手摸到窗台。窗台上积着一层湿灰，指腹留下清楚的五道痕。他没有把手探得更远。相邻塔体之间看不见地面，下面像被一整块黑色的墙封住。这里能看见外面，却不是出口。\n\n广播又响了。\n\n“十七层，东侧楼梯，距离三十米。”\n\n声音从窗外传来，又从他身后的走廊回了一遍。两个方向的尾音几乎同时结束。沈砚回头，看到走廊尽头的墙上多出一块蓝色标牌，牌面朝向他，写着一个被折断的数字。\n\n他没有去追声音。测距带的带钩端还挂在窗下，带身从窗缝一直拉回原来的墙根。它把检修窗和室内的墙面连成一条可复核的向外路线。这个结果已经足够重要，重要到不需要再替广播证明它自己。\n\n沈砚用铝牌在窗框内侧轻轻刮了一道，留下浅白的折返线。然后他把带钩端收回，重新测了一遍。两端之间仍是二点九四米。\n\n检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。\n",
        "heading": "## 第2章 窗缝之外",
        "ordinal": 2,
        "source_span_id": "canon-span_70e5d91133cdb192b7cfb599"
      },
      {
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "content": "## 第3章 没有地面的平台\n\n检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。\n\n他没有去找声音。上一轮重排已经证明，能听见不等于能抵达。\n\n楼层又开始移动。墙体先向后退，接着从窗缝的位置向外鼓起。黑线被拉成一道斜口，冷光从斜口上方落下来。沈砚压低身体，看到窗外原本悬空的灰雾里多出一块平台。它没有栏杆，边缘像被从另一座楼上硬生生撕下来，底部直接没进黑暗。\n\n平台离窗台不远，近得像伸手就能摸到；但它和窗台之间的距离正在一寸一寸改变。沈砚先看自己的东西。半瓶水还在腰侧，手电的电量不多，铝牌上的折返线已经被磨得发白。测距带最稳，也最适合回答一个问题：这块平台究竟是不是一条会把人送进空中的假路。\n\n他选择测距带。\n\n带钩端甩出窗外，第一次只擦到平台的边。第二次，钩子卡住一处没有锈穿的孔。墙体立刻向上错动，平台跟着向右滑。带身绷成一条直线，带壳端却没有被窗框拖走。\n\n测距带保持检修窗与外侧平台的相对关系。沈砚盯着刻度，等平台再动一次。窗台和平台边缘同时向前，间距没有消失，带身的弧度反而替他标出了下一次移动的方向。\n\n这不是把平台钉在原地。平台仍会移动，风也仍会把他的衣角向外拽。测距带只保留两端之间的关系，给他一条能够回来的线。\n\n沈砚先把一只脚探出去。鞋底碰到平台时，平台向下沉了一寸，黑暗从边缘翻上来。他没有再往前，先蹲下，用手摸平台表面。粗糙的水泥上有几道被雨水冲开的白痕，白痕朝着上方的风道延伸。\n\n建筑把检修窗外的相邻塔体推近，外侧平台真正出现在灰雾里。沈砚在心里记住这个事实，却没有把它当成稳定的楼层。下一次重排可能让平台贴到别的墙，也可能让它彻底消失。\n\n广播突然变得清晰。\n\n“屋顶安全。向前三十米。”\n\n平台尽头确实有一块蓝色标志，却是倒挂的。标志下方没有屋顶，只有一截被折断的风道。风从断口冲出来，把一小撮白灰吹到沈砚鞋面上。\n\n他把测距带往前收了半米，测试平台边缘和窗框的关系是否还在。带钩端没有松，带壳端也没有滑。两端之间仍能被同一条线解释。沈砚这才挪出第二步，跨过平台上那道积水的裂缝。\n\n裂缝下面没有楼层。远处两座塔体的墙皮在灰雾里互相遮挡，像两块缓慢合拢的门。沈砚看到更高处的风道里有一串白色脚印，脚印只出现了七步，到了断口便没有了。\n\n他没有追过去。那不是已经确认的人，也不是可以调用的路线。它只是一种留在现场的未知痕迹。\n\n平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。\n",
        "heading": "## 第3章 没有地面的平台",
        "ordinal": 3,
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8"
      },
      {
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "content": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”\n\n声音很近，近得像贴着检修窗的铁皮说话。沈砚没有抬头去找。上一轮他看见过倒挂的蓝色标志，也看见过标志下面没有地面。广播说的是方向，不是证据。\n\n楼层开始重排。走廊地面先向左倾，墙根的灰线被拉成一条细长的弧。检修窗外没有平台，只有一块向后缩的墙面。墙面缩到一半，忽然裂开一道竖口，冷风从里面冲出来，带着湿水泥和很淡的铁锈味。\n\n脚步声就在竖口里，一步，停顿，再一步。广播又说了一遍屋顶安全，脚步却向下传，像有人在看不见的楼梯上往低处走。竖口上方露出一角蓝色标志，方向和声音都像真的；可标志的边缘没有固定的墙，随着建筑移动，它连同竖口一起向窗边滑来。\n\n沈砚先看手里的东西。水瓶还有一半，手电的光柱已经发黄，铝牌上的折返线刚好能指回走廊。今天的机会只有一次。他没有拿水瓶去赌一口水，也没有让手电替他照亮不存在的地面。\n\n他选择测距带。\n\n带钩端甩进竖口，钩住一片没有完全脱落的金属边。墙面立刻向后缩，带身绷紧。带钩端卡在孔里，带壳端却没有随着墙体后退。沈砚盯住两端之间的弧线，等第二次移动发生。\n\n开口与检修窗的距离在闭合前先缩短又恢复，广播的屋顶声音没有固定端点。他在铝牌上划下一道短线。不是距离变回去了，而是墙后那一段空间绕着窗框折了一次。竖口看起来向前，实际却把带钩端拖向下方。若他顺着蓝色标志踏进去，下一次重排很可能会把回程折到别处。\n\n沈砚把脚放到窗台边，半个身子探向竖口。冷风从衣领灌进去，墙后没有脚下的回声，只有一阵一阵往下坠的空气。声音还在说屋顶安全，脚步声却停在他看不见的地方。\n\n他没有进入。他先记录回声关系，再拒绝踏入无法保留回程的开口。带身的弧度把竖口和窗框之间的闭合关系留在铝牌的刻线上，测距带记录了一处广播回声与真实端点不一致的闭合关系。\n\n竖口开始合拢。沈砚用力向后收带，金属钩擦过墙边，带壳端仍压在窗台上。开口只剩一掌宽时，里面传来第三下脚步，随后声音和风一起被墙体夹断。\n\n他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。\n",
        "heading": "## 第4章 屋顶在墙后",
        "ordinal": 4,
        "source_span_id": "canon-span_6a551b7a462d002ea780f449"
      }
    ],
    "recent_payoffs": {},
    "recent_structures": [
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
    "rhythm_diagnostics": {
      "analyzer_versions": {
        "deterministic": "rhythm-deterministic-v1",
        "semantic": "rhythm-semantic-v1"
      },
      "as_of_chapter": 4,
      "as_of_event_seq": 29,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T17:11:11.759865+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 4,
        "mode": "unknown",
        "severity": "WARNING"
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
        },
        {
          "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 2
        },
        {
          "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 3
        },
        {
          "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 4
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
      "projection_hash": "ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_11a27d6489b278d95c569ff0",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.0,
        "series_markers": [
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
        "last_advanced_chapter": "4",
        "payload_json": "{\"evidence\": \"沈砚退回窗边，仍能沿测距带找回走廊。\", \"goal\": \"确认广播里反复出现的楼外天气是否真实，并找到一条自己能够掌握、而不是被声音牵着走的离开室内之路。\", \"phase\": \"escalation\", \"source_draft_id\": \"draft_bf2bb3f1e46011392b83b872\", \"source_span_id\": \"canon-span_6a551b7a462d002ea780f449\", \"stakes\": \"广播把无法保留回程的开口报成屋顶，错误进入会让测距带和回程一起被建筑夹断。\", \"status\": \"ADVANCED\", \"thread_id\": \"thread-original-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower\"}",
        "phase": "escalation",
        "progress": 0.0,
        "reader_visibility": 0.5,
        "source_span_id": "canon-span_6a551b7a462d002ea780f449",
        "stakes": "广播把无法保留回程的开口报成屋顶，错误进入会让测距带和回程一起被建筑夹断。",
        "status": "CANON",
        "target_payoff_max": null,
        "target_payoff_min": null,
        "thread_id": "space-reading-route-evidence",
        "version": 4
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
    "base_event_seq": 29,
    "base_projection_hash": "ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31",
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
      }
    },
    "current_position": {
      "last_canon_chapter": 4,
      "next_chapter": 5
    },
    "earlier_summaries": [
      {
        "chapter_id": "canon-chapter_96f6a1794bf43a1659c7fba2",
        "heading": "## 第1章 第一章 墙还在，路没了",
        "ordinal": 1,
        "summary": "正文停在首章 VALIDATED 边界，未执行正史批准；广播来源、门后空间和建筑成因保持未知。"
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
        "current_chapter": 4,
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
            "last_advanced": 4,
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
        "snapshot_id": "portfolio_ac8e781b331c3d3bcd8f7f85",
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
        2,
        3,
        4
      ]
    },
    "knowledge_boundaries": {},
    "narrative_portfolio": {
      "consecutive_deferrals": 0,
      "current_chapter": 4,
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
          "last_advanced": 4,
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
      "snapshot_id": "portfolio_ac8e781b331c3d3bcd8f7f85",
      "warnings": []
    },
    "packet_id": "boundary_279443cf5d5079c403f3b8c8",
    "promises": {},
    "recent_full_chapters": [
      {
        "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
        "content": "## 第2章 窗缝之外\n\n墙里的声音先停了一拍。\n\n沈砚没有动。上一章留下的那面灰墙还在他右手边，测距带的带壳端压在墙根，带钩端缠在腕上。半瓶水贴着腰侧，瓶里的水只剩下大半，却已经被他分成了两次吞咽的分量。手电还亮着，光柱里漂着细灰。\n\n随后，整层楼像有人从中间拧了一下。\n\n瓷砖发出连续的脆响，脚下的地面先向左沉，再猛地抬起。沈砚肩膀撞上墙，手里的铝牌掉在地上，沿着墙角滑出半尺。远处传来广播，声音比刚才近，像贴在门缝里说话。\n\n“十七层，天气晴。请沿东侧楼梯上行。”\n\n他看向手表。表盘没有停，指针却在震。东侧原本是封死的储物间，第一章的重排之后，那面墙已经折到他身后。广播说得很肯定，建筑却没有给出任何能对上的东西。\n\n一股冷风从脚边掠过。不是走廊尽头的穿堂风，而是从两块墙体之间挤出来的细风，带着湿冷的水泥味。沈砚蹲下去，把手掌贴在地面。地面仍是实的，风却从墙内穿出，断断续续，像外面有一片没有被楼层吞掉的空地。\n\n墙角慢慢裂开一条缝。缝隙只有两指宽，另一边没有黑暗，反而透出一层发白的灰光。灰光一闪就灭，墙面又向内合拢。\n\n他第一反应是去拿手电。手电可以照清缝里的边，水可以让他撑过下一次重排，铝牌能留下新的标记。三件东西都在手边，只有一件能在今天改变。\n\n沈砚把手电按灭，又把半瓶水按回腰侧。他没有碰铝牌，只把测距带从腕上解下来。\n\n如果那条缝只是建筑变形留下的空隙，照亮它没有用；如果缝的两端属于不同的墙面，铝牌也只能替他记住一个错误位置。测距带已经证明过一次关系可以留下来。现在需要确认的是，关系能不能穿过这条正在收拢的缝。\n\n他在心里把今天的选择说清楚：测距带跨局部重排保持空间关系。\n\n那句话落下的瞬间，带壳端的金属边缘传来一声极轻的鸣响。没有光，也没有突兀的热。测距带只是变得更沉，像里面多了一根看不见的骨头。它的刻度没有变化，带身贴过墙角时，却没有被墙体的错位带偏。\n\n沈砚先伸出两根手指，量缝隙从哪一段开始。墙面正在移动，左侧瓷砖向下错了半格，右侧的水泥边却保持着原来的斜角。他把带钩端探进去，钩住另一边裸露的钢筋。\n\n墙缝突然合拢。\n\n带身绷紧，沈砚的手腕被拖得向前一沉。钩端没有脱落，带壳端也没有被拉进墙里。两端之间仍是二点九四米。不是刚才那面墙与断梯之间的旧数字，而是这一处新缝隙两端的关系。\n\n他没有急着往里钻。先把钩端收回，再重新送入；第二次，墙面向外折了一寸，缝隙里出现一块锈蚀的百叶窗。百叶窗后面有风，风把灰尘吹成一条窄窄的斜线。\n\n测距带在窄缝重排后仍保持两端对同一墙面的关系。沈砚盯着那条斜线，知道这不是一句解释，而是一个可以重复的结果。他把带壳端压在墙根，以带身的弧度记下角度，再将带钩端挂到百叶窗下方的固定孔。\n\n这一次，窗框没有随墙面一起消失。\n\n他侧身挤过去。肩胛骨擦过剥落的腻子，衣服被一根突出的铁丝勾住。窗后的空间并不宽，只够一个人半蹲着转身。墙外没有地面，只有两座被灰雾隔开的楼体。更远处的天空呈铅色，云层压得很低，风从两座楼之间穿过去，带动百叶片发出细碎的撞击声。\n\n楼外的风是真的。灰光也是真的。\n\n沈砚伸手摸到窗台。窗台上积着一层湿灰，指腹留下清楚的五道痕。他没有把手探得更远。相邻塔体之间看不见地面，下面像被一整块黑色的墙封住。这里能看见外面，却不是出口。\n\n广播又响了。\n\n“十七层，东侧楼梯，距离三十米。”\n\n声音从窗外传来，又从他身后的走廊回了一遍。两个方向的尾音几乎同时结束。沈砚回头，看到走廊尽头的墙上多出一块蓝色标牌，牌面朝向他，写着一个被折断的数字。\n\n他没有去追声音。测距带的带钩端还挂在窗下，带身从窗缝一直拉回原来的墙根。它把检修窗和室内的墙面连成一条可复核的向外路线。这个结果已经足够重要，重要到不需要再替广播证明它自己。\n\n沈砚用铝牌在窗框内侧轻轻刮了一道，留下浅白的折返线。然后他把带钩端收回，重新测了一遍。两端之间仍是二点九四米。\n\n检修窗的边缘开始发出细响。建筑要把这条缝收回去了。沈砚先退回走廊，再用力拉紧测距带。窗框在他眼前向内折，百叶片一片片消失，最后只剩一道比头发粗不了多少的黑线。黑线外仍有风，风里带着楼外湿冷的味道。\n\n他在原地站了一会儿，直到手腕的酸痛提醒他放松。当天唯一的机会已经用掉，半瓶水没有增加，手电也没有变亮；但主线程从寻找广播方向推进为掌握一条向外的局部路线。\n\n沈砚低头看着窗框上留下的浅白折返线，听见广播在更深处报出相反的楼层。他没有抬头。测距带的第二个固定端点还在手里，楼外风向已经确认，只是相邻塔体之间没有地面。\n",
        "heading": "## 第2章 窗缝之外",
        "ordinal": 2,
        "source_span_id": "canon-span_70e5d91133cdb192b7cfb599"
      },
      {
        "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
        "content": "## 第3章 没有地面的平台\n\n检修窗只剩下一条黑线。\n\n沈砚把测距带缠回手腕，指腹还留着窗框上的湿冷。广播在走廊深处重复了三遍“东侧楼梯”，每一遍的尾音都从不同墙面弹回来。墙外的风却没有变，仍从那条黑线里钻进来，带着灰雾和很淡的铁锈味。\n\n他没有去找声音。上一轮重排已经证明，能听见不等于能抵达。\n\n楼层又开始移动。墙体先向后退，接着从窗缝的位置向外鼓起。黑线被拉成一道斜口，冷光从斜口上方落下来。沈砚压低身体，看到窗外原本悬空的灰雾里多出一块平台。它没有栏杆，边缘像被从另一座楼上硬生生撕下来，底部直接没进黑暗。\n\n平台离窗台不远，近得像伸手就能摸到；但它和窗台之间的距离正在一寸一寸改变。沈砚先看自己的东西。半瓶水还在腰侧，手电的电量不多，铝牌上的折返线已经被磨得发白。测距带最稳，也最适合回答一个问题：这块平台究竟是不是一条会把人送进空中的假路。\n\n他选择测距带。\n\n带钩端甩出窗外，第一次只擦到平台的边。第二次，钩子卡住一处没有锈穿的孔。墙体立刻向上错动，平台跟着向右滑。带身绷成一条直线，带壳端却没有被窗框拖走。\n\n测距带保持检修窗与外侧平台的相对关系。沈砚盯着刻度，等平台再动一次。窗台和平台边缘同时向前，间距没有消失，带身的弧度反而替他标出了下一次移动的方向。\n\n这不是把平台钉在原地。平台仍会移动，风也仍会把他的衣角向外拽。测距带只保留两端之间的关系，给他一条能够回来的线。\n\n沈砚先把一只脚探出去。鞋底碰到平台时，平台向下沉了一寸，黑暗从边缘翻上来。他没有再往前，先蹲下，用手摸平台表面。粗糙的水泥上有几道被雨水冲开的白痕，白痕朝着上方的风道延伸。\n\n建筑把检修窗外的相邻塔体推近，外侧平台真正出现在灰雾里。沈砚在心里记住这个事实，却没有把它当成稳定的楼层。下一次重排可能让平台贴到别的墙，也可能让它彻底消失。\n\n广播突然变得清晰。\n\n“屋顶安全。向前三十米。”\n\n平台尽头确实有一块蓝色标志，却是倒挂的。标志下方没有屋顶，只有一截被折断的风道。风从断口冲出来，把一小撮白灰吹到沈砚鞋面上。\n\n他把测距带往前收了半米，测试平台边缘和窗框的关系是否还在。带钩端没有松，带壳端也没有滑。两端之间仍能被同一条线解释。沈砚这才挪出第二步，跨过平台上那道积水的裂缝。\n\n裂缝下面没有楼层。远处两座塔体的墙皮在灰雾里互相遮挡，像两块缓慢合拢的门。沈砚看到更高处的风道里有一串白色脚印，脚印只出现了七步，到了断口便没有了。\n\n他没有追过去。那不是已经确认的人，也不是可以调用的路线。它只是一种留在现场的未知痕迹。\n\n平台开始回移。沈砚立刻退回窗边，拉紧测距带。钩子在孔里震动，平台边缘擦过窗台，水泥粉末落进黑暗。最后一刻，他把带钩端收回，平台从灰雾里向后退，像从未出现过。\n\n窗框内侧留下两道新的浅痕，一道在脚边，一道在平台消失前的高度。沈砚用铝牌轻轻刮过其中一道，记下折返方向。\n\n测距带的第二个固定端点还在手里。沈砚退回走廊，听见广播又把屋顶说成安全层。他低头看着鞋面上的白灰，知道外侧平台确实存在过，也知道那里没有地面。上方风道里的七步白印，比任何楼层编号都更接近下一条路。\n",
        "heading": "## 第3章 没有地面的平台",
        "ordinal": 3,
        "source_span_id": "canon-span_b93129f324cb473a95a8a1b8"
      },
      {
        "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
        "content": "## 第4章 屋顶在墙后\n\n检修窗只剩一条黑线，黑线外的风却比上一轮更近。沈砚把测距带绕在腕上，带壳端压住窗台，另一端留下的浅痕还在。平台已经消失，白色脚印停在断裂风道的边缘，像有人走到那里之后忽然被建筑抹掉。\n\n广播在墙后响起来。\n\n“屋顶安全，向前三十米。”\n\n声音很近，近得像贴着检修窗的铁皮说话。沈砚没有抬头去找。上一轮他看见过倒挂的蓝色标志，也看见过标志下面没有地面。广播说的是方向，不是证据。\n\n楼层开始重排。走廊地面先向左倾，墙根的灰线被拉成一条细长的弧。检修窗外没有平台，只有一块向后缩的墙面。墙面缩到一半，忽然裂开一道竖口，冷风从里面冲出来，带着湿水泥和很淡的铁锈味。\n\n脚步声就在竖口里，一步，停顿，再一步。广播又说了一遍屋顶安全，脚步却向下传，像有人在看不见的楼梯上往低处走。竖口上方露出一角蓝色标志，方向和声音都像真的；可标志的边缘没有固定的墙，随着建筑移动，它连同竖口一起向窗边滑来。\n\n沈砚先看手里的东西。水瓶还有一半，手电的光柱已经发黄，铝牌上的折返线刚好能指回走廊。今天的机会只有一次。他没有拿水瓶去赌一口水，也没有让手电替他照亮不存在的地面。\n\n他选择测距带。\n\n带钩端甩进竖口，钩住一片没有完全脱落的金属边。墙面立刻向后缩，带身绷紧。带钩端卡在孔里，带壳端却没有随着墙体后退。沈砚盯住两端之间的弧线，等第二次移动发生。\n\n开口与检修窗的距离在闭合前先缩短又恢复，广播的屋顶声音没有固定端点。他在铝牌上划下一道短线。不是距离变回去了，而是墙后那一段空间绕着窗框折了一次。竖口看起来向前，实际却把带钩端拖向下方。若他顺着蓝色标志踏进去，下一次重排很可能会把回程折到别处。\n\n沈砚把脚放到窗台边，半个身子探向竖口。冷风从衣领灌进去，墙后没有脚下的回声，只有一阵一阵往下坠的空气。声音还在说屋顶安全，脚步声却停在他看不见的地方。\n\n他没有进入。他先记录回声关系，再拒绝踏入无法保留回程的开口。带身的弧度把竖口和窗框之间的闭合关系留在铝牌的刻线上，测距带记录了一处广播回声与真实端点不一致的闭合关系。\n\n竖口开始合拢。沈砚用力向后收带，金属钩擦过墙边，带壳端仍压在窗台上。开口只剩一掌宽时，里面传来第三下脚步，随后声音和风一起被墙体夹断。\n\n他退回走廊，手掌被带身勒出红痕。广播没有停，已经改报“西侧楼梯”。同一面墙后，刚才的屋顶标志只剩一小块蓝色反光，像一枚贴错位置的标签。\n\n沈砚回头看检修窗。测距带的一端还在手里，另一端的刮痕留在窗台附近；可那道竖口已经没有任何缝隙。白色脚印仍停在更高处，既没有被证明属于人，也没有被证明属于建筑。\n\n他把铝牌翻过来，在新刻的短线旁写下一个很小的问号。屋顶没有被确认，路线也没有被摧毁。至少这一次，他知道哪一种声音不能带他回家。\n",
        "heading": "## 第4章 屋顶在墙后",
        "ordinal": 4,
        "source_span_id": "canon-span_6a551b7a462d002ea780f449"
      }
    ],
    "recent_payoffs": {},
    "recent_structures": [
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
    "rhythm_diagnostics": {
      "analyzer_versions": {
        "deterministic": "rhythm-deterministic-v1",
        "semantic": "rhythm-semantic-v1"
      },
      "as_of_chapter": 4,
      "as_of_event_seq": 29,
      "book_id": "original-e56a54687506",
      "config_hash": "c1261d246fb0e8f72174caa4174f70586d1839ee5c56f4eb7049518ffaf87d4a",
      "created_at": "2026-08-16T17:11:11.759865+00:00",
      "edition_id": "base",
      "ending_mode_streak": {
        "count": 4,
        "mode": "unknown",
        "severity": "WARNING"
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
        },
        {
          "chapter_id": "canon-chapter_70e5d91133cdb192b7cfb599",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 2
        },
        {
          "chapter_id": "canon-chapter_b93129f324cb473a95a8a1b8",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 3
        },
        {
          "chapter_id": "canon-chapter_6a551b7a462d002ea780f449",
          "extractor_kind": "DETERMINISTIC",
          "ordinal": 4
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
      "projection_hash": "ac3e2d937ecc3e9209b1af6d937e6c18f55c2a4b1a823b3999915fd435cedf31",
      "same_function_streak": {
        "count": 0,
        "function": null,
        "severity": "NONE",
        "source": "planned_primary_function"
      },
      "snapshot_id": "rhythm-snapshot_11a27d6489b278d95c569ff0",
      "title_repetition": {
        "exact_duplicates": [],
        "matching_chapters": [],
        "max_similarity_last_20": 0.0,
        "series_markers": [
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