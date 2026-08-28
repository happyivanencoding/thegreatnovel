我将使用 `novel-scene-skills`，因为本次任务正是对 Scene Skill 分类、运行时边界和场景实现契约做审查。严格限定读取你列出的文件；先读技能规范与 provisional matrix，再读 prose craft 和指定的十个 prose-dna 参考，不修改任何文件。已确认 matrix 中有 8 个 Combat 候选，以及 5 个其它新 skill 候选/方向。指定的十张 prose-dna 分散在两个 `temps/.../prose-dna` 目录中；我只定位并读取对应十张文件，不把其它参考库纳入范围。接下来会按每张 DNA 的可观察条件、选择逻辑和停点提取跨书共性。结论：provisional matrix 对 Combat 明显过拆。8 个候选中，只有 `combat_protect_hold` 的读者问题、状态模型、beat 选择和 stop rule 足以支撑独立 Primary；其余应合并为 Combat 参数、Modifier 或现有 Skill 组合。其它 3 个 proposed new skills 也不应新增 Primary。

本次判断基于指定的 [provisional matrix](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/selection/PROVISIONAL_RESEARCH_MATRIX.md)、[Scene Skill 规范](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/SKILL.md)、全部现有 scenes、[GBRAIN Prose Craft](C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md) 和指定十张 Selection Prose DNA。matrix 中提到但未列入本次范围的《武道宗师》《一世之尊》《吞噬星空》《永夜君王》不计入证据权重。

## Combat candidates

| Candidate | 判定 | 理由 |
|---|---|---|
| `combat_parity_duel` | MERGE | “双方都能赢”只是初始力量关系；状态仍是主动权、距离、资源和对手回应，beat 仍是“作用→应对→新变量”，stop 仍是胜负/撤退/脱离。并入 Combat 的 `counterplay` 或 `power_parity` 参数。 |
| `combat_underdog_upset` | MERGE | “窄窗口”是力量差、资源、位置和时间约束，不是新场景发动机。Trial 的外部判定线也不存在。并入 Combat 的 `power_asymmetry/window` Modifier。 |
| `combat_dominance_payoff` | MERGE | 核心问题已经是“新实力如何被最少交换证明并重新定价”，属于 `combat + showcase_evaluation`。早停和社会重新估值已有 Showcase / shared result-stop 承担。 |
| `combat_adaptation_counterplay` | MERGE | 对手试探、适应、封锁和利用暴露弱点已经是现有 Combat 的核心契约，不应把“写好战斗”再拆成技能。可作为 `counterplay` beat 标记。 |
| `combat_protect_hold` | **KEEP** | 唯一有实质差异者：读者持续追问的是“保护对象/门/时间窗口能否守住”，不是“谁个人占优”；状态模型变成保护对象完整度、覆盖范围、路线、时间和敌方换目标；beat 是拦截、换位、转移、牺牲和封锁；stop 是对象安全、对象丢失、时间到或转战。建议保留为唯一新增 Primary 候选。 |
| `combat_ambush_assassination` | MERGE | 接触前是 `stealth_infiltration` 的暴露状态，接触后回到 Combat。短接触、先手和不可逆结果可作为 `surprise_contact` Modifier，不需新 Primary。 |
| `combat_multi_actor_melee` | MERGE | 多人只改变状态变量数量，不改变核心发动机。现有 Combat 已要求跟踪分工、救援、视野和局部目标；来源 DNA 也明确反对 roster bookkeeping。 |
| `combat_large_scale_local_pov` | REJECT | 这是尺度与 POV 约束，不是 Scene Skill。真正的 live question 仍是局部目标和局部因果；保留为 `scale-anchored-wonder` / `spatially-traceable-causality` 的上下文 Modifier。 |

跨十张 DNA 的共同证据是：战斗都优先保留会改变目标、位置、接触、资源、伤势、保护范围、敌方反应或下一选择的细节；差异主要是变量配置，不是独立发动机。`遮天`、`斗破`、`大圣传`、`仙逆`、`死人经`、`全球高武`和`诡秘`的动作观察都回到同一条因果链：位置/条件 → 作用 → 对手或环境回应 → 新约束。

## 其它 proposed new skills

| Candidate | 判定 | 理由 |
|---|---|---|
| `character_voice_pressure` | MERGE / HOLD | “人物在压力下注意、保护、拒绝、误判什么”是真实高价值观察，但它横跨对白、关系、战斗和调查，不拥有独立 scene state 或 stop rule。并入角色反应/对白 Projection；保留研究候选，暂不 production promotion。 |
| `world_entry_lived_texture` | MERGE | 入口生活质感由 `scene_entry + exploration` 和已有 `action-anchored-grounding` 承担。它改变的是细节选择，不是新的读者问题或状态模型。 |
| `desire_temptation` | REJECT（作为独立 Skill） | 这是欲望压力 Modifier：可附着于 `hunt_acquisition`、`resource_economy`、`exploration` 或 `relationship`。没有独立 beat/stop；单列会把“值得冒险”误变成题材分类。 |

因此没有发现明显的其它 under-split。现有 `investigation / deduction_reveal`、`exploration / investigation`、`training_learning / comprehension_insight`、`relationship / social_bargain_decision` 的状态模型和停止点仍然不同。

## Runtime v2 文档 schema

持久文档可以这样组织：

```yaml
schema_version: scene-skill.v2
skill_id: combat_protect_hold
kind: primary
status: candidate

contract:
  primary_reading_question: "保护对象、门或时间窗口能否守住？"
  use_when:
    - "胜负标准首先是保护目标仍然存在或可撤离"
  do_not_use_when:
    - "核心问题已经变成单纯击败对手"
  failure_patterns:
    - "把所有动作写成伤害交换"
    - "忽略敌方换目标"
  composition:
    secondary_allowed: 1

generation_lens:
  reader_live_question: "当前哪一处保护条件最接近失守？"
  state_model:
    - protectee_or_asset_integrity
    - coverage_position
    - enemy_target
    - time_or_route_window
    - usable_resources
  beat_selection:
    foreground:
      - "敌方改变目标或路线"
      - "保护者换位、拦截、转移、牺牲或消耗资源"
      - "保护对象、空间或时间窗口的可见变化"
    compress:
      - "没有改变保护态势的重复攻击"
      - "无新结果的移动和招式"
  response_loop: "action -> opposing/environment response -> protection state update"
  knowledge_boundary: "只给当前保护选择所需的信息"
  realization_priority:
    - "空间关系"
    - "保护对象状态"
    - "身体或资源代价"
  stop_rule: "保护成功、保护失败、窗口耗尽，或主问题转为其它 Skill"

revision_lens:
  preserve:
    - "Chapter Mission / Canon 事实"
    - "保护目标及失败后果"
    - "人物当前知识边界"
  inspect:
    - "每个前景动作是否改变保护状态"
    - "敌方是否真实回应并可能换目标"
    - "读者是否知道谁在哪里、保护什么"
    - "结果是否落到对象、位置、身体或行动空间"
  reject:
    - "无因果的招式流水账"
    - "新增未经授权的敌方策略或代价"
    - "结果成立后重复解释"
  repair_policy:
    - "只做局部压缩、补足空间/结果链和删除重复解释"
  stop_rule: "保护状态、失败后果和下一行动已清楚；不继续做风格性重写"

research:
  model_visibility: excluded
  source_evidence:
    - source_book_id: "..."
      locator: "..."
```

模型投影必须是两个明确的 allowlist：

```yaml
primary_payload:
  scene_contract: ...
  current_state: ...
  generation_lens: ...
```

```yaml
authority_reviser_payload:
  scene_contract: ...
  draft: ...
  revision_lens: ...
```

`source_evidence` 只留在研究/审计层，不进入 Primary 或 Authority Reviser；两个模型也互不接收对方的 Lens。

## 最小高收益 production candidate list

1. `combat_protect_hold`：唯一值得新增的 Combat Primary 候选。
2. `spatially-traceable-causality-v1`：复杂追逐、多人行动、移动地形时优先启用。
3. `evidence-first-limited-reveal-v1`：发现、规则复验、身份信息边界。
4. `embodied-reaction-private-scale-v1`：关系变化和重大结果后的私人落地。
5. `action-anchored-grounding-v1`：仅在入口缺少即时动作与空间承重时启用。
6. 保持 `showcase_evaluation`、`combat`、`relationship` 等现有 Primary，不新增 dominance/public-proof/voice/temptation 专门技能。

本次仅做读取和审查，未修改任何文件。
