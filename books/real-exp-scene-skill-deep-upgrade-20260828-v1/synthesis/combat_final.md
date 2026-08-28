我会使用 `tgn-system-steward`，因为这是一次 TGN Combat Scene Skill 的证据边界审计与 v2 演化设计；同时先做一次轻量 memory 检索，确认当前项目的既有约束。全程只读，不改 production。memory 中与本任务直接相关的既有约束是：场景 skill 通常应保持一个 Primary、必要时一个 Secondary，并区分 Canon/未知/计划；另有对 combat 证明后应转入下一现实行动、避免重复演示的记录。我现在开始以仓库文件为准核对，不把 memory 当作本次证据。接下来这组只读检查分别用于三件事：确认不能覆盖的未提交改动、确认最近冻结状态、精确定位用户点名的 skill/evidence/selection 文件。若发现 dirty worktree，我会只读其内容并避免把它当成 production 结论。工作树确实很脏，包含当前分支上的既有修改和大量未跟踪实验目录；我不会触碰它们。最近 HEAD 是 `feat(story): add authority revision pass`，因此本次 synthesis 会把当前文件内容与实验产物分开读取，不把未跟踪 candidate 当 production。`rg` 不可用，我改用 PowerShell 的文件名过滤做有界定位。现有 `combat.md` 已明确：主动权、状态变量、对手回应、团队/战争局部 POV 与 stop；因此 shared core 只能保留“净新增”，不能把这些旧表述换词重写。初步 synthesis 还提出了六条候选新增判断，但它的 taxonomy 结论仍是 provisional；我会逐份回读 evidence 来验证，尤其检查 `protect-hold`、团队/战场、规则条件是否达到不同 beat engine 的门槛。选择/taxonomy 输出共同指向一个关键门槛：只有当“主要阅读问题、状态向量、beat 选择、stop rule”同时改变，才升为 Primary；否则并入 Core/Modifier/既有 skill。现在进入证据正文回读，分批读取 13 份 `combat_*_evidence.md`，每批控制输出大小，避免截断。目前证据已显示四条跨书稳定链：①先固定本拍可判断的胜负尺，②旧方案失效后新动作必须由已变化的行动空间产生，③每次资源/伤势/能力组合都要转成具体行动许可，④达到结果后按“逃、反击、复原、继续控制”检查是否真的闭合。接下来补完剩余四份 evidence，并特别核对是否有足够跨书证据把这些链放进 shared core，而不是只做某一书的变体。13 份 evidence 包与全部指定输出已完成回读。最终判断会比 preliminary 更收敛：只保留一个真正的新增 Primary（protect-hold）；`team_coordination` 只进入受控 Variant Pilot，`battlefield-local` 不升 Variant；其余 posture 作为 Core sublens、Modifier 或既有 skill 组合。现在整理成 source-blind 草案，不会把书名、作者或 locator 带入运行时设计。# Final Verdict

候选版本应收敛为：

- Shared Combat Core：补 6 条净新增判断。
- `combat_protect_hold`：唯一新增 Primary 候选。
- `team_coordination`：值得做受控 Variant Pilot，但不作默认。
- `battlefield_local`：只作 Modifier，不升 Variant。
- 其余 posture：并入 Core、Modifier 或现有 Skill 组合。
- 不进入 production；本稿是 source-blind Final Candidate Design。

# Evidence-Backed Shared Core

以下每条都由至少 5 个以上独立 evidence 包、跨不同战斗姿态反复支持，且不是当前 `combat.md` 的充分表达。

1. 胜利机制先于命中判断
   先确定对手真正依靠什么继续作战：护甲、真身、共享资源、撤离通道、复原能力或条件媒介。命中只有在该机制被关闭后才等于阶段胜利。

2. 阈值先行，机制后置
   先让读者看到一次防御失效、身体异常、位置变化或行动许可丧失，再补足本拍所需的局部规则。未知可以保留，但不能遮蔽“刚才哪一步失效”。

3. 旧方案失效 → 行动空间变化 → 新动作
   新动作必须利用已经发生的地形、距离、资源、阵势、气机或攻防限制。不能用“更大的招”跳过中间因果。

4. 展开功能链，不展开技能目录
   每个重要动作承担一个主要变化：暴露、限制、破防、牵制、终结或收束。后一步必须吃到前一步留下的状态。

5. 资源与伤势必须行动化
   资源要换来承伤次数、攻击窗口、撤离时间、路线控制或下一阶段资格；伤势要改变持武、移动、职责、站位、接班或撤离优先级。

6. Stop 必须检查未支付条件
   结果成立前，检查对手是否仍能逃、挡、复原、转移代价、召援或继续控制。若角色已确认无解，应允许撤退、保存选择权或接受既有世界机制，不强造翻盘。

# Posture Decisions

| Posture | 裁决 | Reader live question / State vector / Beat engine / Stop |
|---|---|---|
| parity duel | Core sublens | 问题是“双方哪项反制资源先断”。状态是反制权、节奏、准备、体力、位置。动作→回应→保留反制→某项资源断裂。反制权消失或胜负成立即停。 |
| underdog | Modifier | 问题是“弱方还能买到哪一个窄窗口”。状态是力量差、资源、地形、时间与退路。只在存在可信窗口时启用；窗口关闭、变成撤退或目标改变即停。 |
| dominance | Existing Skill Composition | 默认是 `combat` 的选项剥夺；若需要社会重估，则组合 `combat + showcase_evaluation`。不要求反转。对手失去承伤、反击、逃跑或复原中的关键选项，并产生现实后果后停止。 |
| adaptive counterplay | Core sublens | 问题是“对手看见什么后如何改写成功条件”。状态是已暴露规则、目标、站位、资源和反制角度。识别→改打节点→新角度暴露。对手没有信息或执行条件时不强加适应。 |
| protect-hold | New Primary | 问题从“谁赢”变成“什么必须守住”。状态是保护对象完整度、覆盖位置、敌方目标、路线/时间窗口、资源与接班能力。敌方换目标→拦截/换位/转移/牺牲/封锁→保护状态更新。对象安全、丢失、窗口耗尽或转入新主问题即停。 |
| ambush | Existing Skill Composition | 接触前属于 `stealth_infiltration`，接触后回到 `combat`；可附 `surprise_contact` Modifier。第一次有效接触改变身体、目标、位置或退路后停止，不要求二次反转。 |
| team coordination | Variant，PILOT | 值得测试。状态拓扑从双方交换变为角色职责、支援线、接班和局部目标接力。甲限制/承伤→乙获得窗口→敌方打断链条→队伍换位或改序。职责链不再改变下一拍时降回 Core。 |
| battlefield-local | Modifier；Reject 为独立 Variant/Primary | 它改变的是尺度、通信、可达性和镜头边界，主要阅读问题仍是局部目标。只有当远景信息实际改变人物选择时才启用；否则保持局部 POV。 |
| rule-condition | Existing Skill Composition | 规则发现交给 `comprehension_insight` / `deduction_reveal`；外部判定线交给 `trial_challenge`；条件作为战斗对象时才保留在 `combat` 的 condition-first sublens。不要新增 puzzle-combat Primary。 |
| ranged exposure | Modifier | 修改距离、视线、暴露、弹药、冷却与掩体的权重。若主问题是“隐藏身份/位置并完成射击”，组合 `stealth_infiltration → combat`；若主问题是守住射界或撤离，则分别组合 `protect_hold` 或 `chase_escape`。 |

# Candidate Runtime Schema

```yaml
schema_version: scene-skill.v2-candidate

route:
  primary: combat | combat_protect_hold | ...
  variant: null | team_coordination
  modifiers:
    - power_asymmetry_window
    - dominance_repricing
    - battlefield_scale_local
    - ranged_exposure
    - condition_first
  handoff: null | chase_escape | stealth_infiltration | trial_challenge | comprehension_insight

generation_payload:
  authority:
    - chapter_mission
    - canon
    - current_knowledge
    - current_state
  shared_combat_core: ...
  selected_primary_generation_lens: ...
  selected_variant_generation_delta: ...
  selected_modifier_delta: ...

revision_payload:
  authority:
    - chapter_mission
    - canon
    - draft
  primary_revision_lens: ...
  selected_variant_revision_delta: ...
```

规则：

- Primary 只接收 source-blind 的 Core、当前 Primary Lens、已选 Variant/Modifier 差量。
- Primary 不接收 evidence、书籍来源、作者信息、locator、未选择候选或完整研究卡。
- Reviser 的 craft 输入只有 `Revision Lens + selected variant revision delta`。
- Reviser 不接收 Generation Lens、原始 evidence、未选 Variant 或第二套正文指导。
- `Secondary` 不再同时表示并场叠加和后续换场；并场用 Variant/Modifier，换主问题用 Handoff。

# combat v2 draft

```md
# combat

Kind: Primary
Maturity: candidate

Primary Reading Question:
当前真正决定胜负的条件是什么，双方下一次行动会怎样让它失效、转手或重新成立？

Use When:
双方或多方正在围绕一个可观察的目标、位置、行动许可、资源窗口或退出条件发生即时冲突。

Do Not Use When:
主问题已经是潜入、追逃、生存维持、外部考核、规则推理或保护对象本身；此时切换或选择对应 Skill。

Core:
先锁定一个读者可见的胜负尺，并明确命中不等于胜利时还剩什么条件。
先展示阈值或失败结果，再补本拍必须知道的局部规则；不要预先罗列完整能力。
每个展开拍通常只承担一个主要变化：
动作 → 对手/环境真实回应 → 状态更新 → 新动作只能利用已改变的行动空间。
资源、伤势、距离、位置、视野和能力只在改变实际行动许可时展开。
多能力、多装备和多人配合按功能链呈现，不按名称清点。
重复交换、同功能动作和没有新结果的旁观反应压缩。

Opponent:
对手可以试探、改目标、换位置、封锁、撤退或利用刚暴露的弱点。
只有对手已有信息、资源和执行条件时，才写适应与反制。

Stop:
胜负、撤退、目标得失、关键行动许可消失、无解边界成立，或新的高优先级目标接管时停止。
停止前检查对手是否仍有逃生、复原、援助、转移代价或继续控制的真实资源。
结果成立后先落到身体、位置、目标、关系或行动空间；不追加同义高潮。

Optional Variant: team_coordination
只在角色职责、支援、接班或并行局部目标真正改变下一拍时启用。
甲的限制、承伤或暴露必须给乙创造具体窗口；敌方打断该链条时，队伍必须改序、换位或改目标。
不逐人记账，不要求每名成员都有独立高光。

Optional Modifiers:
power_asymmetry_window / dominance_repricing / battlefield_scale_local / ranged_exposure / condition_first
```

# new skill draft if any

```md
# combat_protect_hold

Kind: Primary
Maturity: candidate / pilot only

Primary Reading Question:
保护对象、阵地、出口或时间窗口能否在敌方持续施压下守住？

Use When:
保护目标的存续、完整、撤离或延迟本身就是本场首要胜负标准。

Do Not Use When:
保护只是普通战斗中的一个附带限制，或主问题已经变成单纯击败对手、追逃、生存或规则推理。

State Vector:
- protectee_or_asset_integrity
- coverage_position
- enemy_target_and_access_route
- time_or_exit_window
- usable_resources
- injury_and_handoff_capacity
- collateral_or_exposure_boundary

Beat Engine:
敌方改变目标、路线或施压方式
→ 保护者拦截、换位、转移、承伤、牺牲或封锁
→ 敌方真实回应并可能再次换目标
→ 保护对象、覆盖范围、资源或窗口发生可见变化
→ 下一拍围绕最接近失守的条件展开。

Expand:
- 保护目标第一次暴露或位置改变
- 敌方第一次换目标
- 保护结构第一次断裂
- 资源/伤势第一次改变职责或接班
- 保护成功、失败或撤离窗口成立

Compress:
- 不改变保护态势的重复攻击
- 没有新结果的移动与喊话
- 已经成立的普通护卫动作
- 与当前保护问题无关的外围战线

Stop / Handoff:
保护成功、保护失败、窗口耗尽、对象进入稳定撤离/救治，或主问题转为 combat、chase_escape、survival_endurance 等其它 Skill 时停止。

Revision Lens:
- 检查读者是否知道保护什么、谁在保护、失败会造成什么。
- 检查敌方是否能真实换目标，而不是只攻击当前防守者。
- 检查每个前景动作是否改变保护状态、路线、窗口、职责或代价。
- 检查伤势和资源是否改变实际职责，而非只留下疼痛或数量。
- 删除无因果的招式流水账、强制牺牲、强制反转和结果后的重复守护。
- 不新增未经授权的目标、敌方策略、代价或保护对象。
- 保护状态、失败后果和下一行动清楚后停止修改。
```

# Primary vs Reviser

| 内容 | Primary 生成时 | Reviser 检查时 |
|---|---|---|
| 胜负尺 | 选择一个可读 ruler | 检查正文是否始终围绕它 |
| 每拍一个主要变化 | 作为压缩倾向，不是硬模板 | 检查是否出现流水账 |
| 阈值先行 | 选择首次必须让读者看到的失效 | 检查是否先讲百科、后补行动 |
| 对手适应 | 只使用当前已知事实与可执行能力 | 检查反制是否有信息来源 |
| 资源/伤势 | 纳入当前状态模型 | 检查是否真的改变行动或职责 |
| 复杂组合 | 按功能链规划 | 检查是否退化成技能清单 |
| Stop | 预设可能的结果出口 | 检查是否漏掉逃生、复原、援助或无解边界 |
| 保护对象 | 仅在 `protect_hold` 中作为主问题 | 检查是否被真正放在战场拓扑中心 |

不得作为 Primary 每拍流程的规则：

- 强制“三拍 counterplay”。
- 强制每拍都出现新招、反转、受伤或牺牲。
- 强制列出所有资源、技能、成员和战线。
- 强制出现旁观者、公开奖励或社会重估。
- 强制加入倒计时、数字阈值或固定回合数。
- 强制每次伤势都导致撤退。
- 强制每场伏击都有隐藏敌人。
- 强制每场规则战都解释完整规则。

这些只适合作为 Reviser 的失败检查或局部修复依据，不能变成战术日志。

# A-B Plan

最便宜的设计是固定同一 Chapter Mission、Canon、人物状态和模型，只替换 Combat Lens；每类先跑 1 对，只有出现方向性差异才增加反例对。

| 套件 | A | B | 因果验收 |
|---|---|---|---|
| parity duel | 当前 `combat.md` | `combat v2 + parity sublens` | B 是否保留双方可信反制，且不强行增加回合；优势是否由节奏、位置、准备或损耗改变。 |
| protect-hold | 当前 `combat.md` | `combat_protect_hold` | B 是否把保护对象/窗口置于中心，能否处理敌方换目标、接班与撤离；不应自动追加牺牲或击杀。 |
| team/multi | 当前 `combat.md` | `combat + team_coordination variant` | B 是否形成“限制→窗口→接力→敌方打断”的链条；若只是文字更长或角色更多，不算有效。 |
| rule-heavy | 当前 `combat.md` | `combat + condition_first`，必要时接 `comprehension_insight` | B 是否先给本拍必要规则、让失败生成新目标；若变成规则讲义，应淘汰。 |

Reviser 另做最小配对：

- 同一份故意存在战斗流水账、错误 Stop 或保护对象失焦的草稿。
- A：Authority-only。
- B：Authority + 对应 Revision Lens。
- 只有 B 能局部修复目标问题、保留正确事实且不扩大改写范围，才保留该 Lens。

晋升标准：

- `protect_hold`：在两个不同保护任务中都能改变主要 beat loop，且不增加事实漂移。
- `team_coordination`：必须优于一个紧凑 Modifier，而不只是优于空白；否则降为 Modifier。
- `battlefield_local`：若只改善尺度压缩，不证明独立 beat loop，保持 Modifier。
- `rule_condition`：若现有组合已达到同等效果，不新增 Skill。

# Non-Promoted Findings

- `parity duel`：不是新 Primary；它是 Combat 的 Core sublens。
- `underdog`：不是新 Primary；它只是力量差与窄窗口 Modifier。
- `dominance`：不是新 Primary；通常是 Combat 与 Showcase 的组合。
- `adaptive counterplay`：不是新 Primary；是 Combat Core 的深化。
- `ambush`：不是新 Primary；由潜入到战斗的组合已足够。
- `battlefield-local`：不值得独立 Variant；它是尺度/通信/可达性的 Modifier。
- `rule-condition`：不新增 puzzle-combat；交给现有理解、推理、Trial 与 Combat 组合。
- `ranged exposure`：不新增 ranged Primary；按距离、视线、掩体和暴露调整 Modifier 或组合现有追逃/潜入。
- 不推广“每次受伤都要撤退”“每次伏击都要反转”“每次碾压都要公开定价”“每次大规模战都要远景切镜”。
- 具体兵器、法术、境界、血脉、舰队、阵法、职业名称均不属于可迁移 Runtime 规则。
- 当前唯一值得继续验证的新增结构是：`combat_protect_hold` Primary，以及 `team_coordination` Variant Pilot。

本次仅完成只读综合，没有修改 production 或实验文件。
