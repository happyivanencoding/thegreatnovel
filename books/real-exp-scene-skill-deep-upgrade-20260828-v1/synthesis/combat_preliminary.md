我会按你限定的文件范围做只读合成：先读取 `novel-scene-skills` 的总规则，再逐份读取 combat/chase/survival/showcase/stealth 与 selection/taxonomy 文件，最后只输出跨书净新增判断、taxonomy 裁决和 provisional v2 结构，不改 production 文件。已确认 evidence 与 scene skill 文件存在；`selection/...` 不在 `.agents/skills/novel-scene-skills` 下，我会只定位仓库内同名的三份 selection 文件，不扩展读取范围。接下来先提取各文件的标题、规则段和 evidence ID，再回读支撑具体判断的原文片段。# Shared Core

先给结论：现有 `combat.md` 的核心已经正确，不需要重写成另一套战斗流程。它已经覆盖：

- 主要阅读问题：谁占优势、为什么、下一拍如何改变胜负关键；
- 主动权、位置、资源、伤势、保护对象、退路、目标控制权；
- 对手真实回应、压缩重复交换；
- 团队分工与大型战场的局部 POV；
- 胜负、撤退、目标得失和转场式 Stop。

跨书新增的不是这些名词，而是以下判断层：

1. **先锁定当前胜利机制，再判断命中是否等于胜利。**
   “护甲仍在、真身未锁、共享力量仍可转移、敌人仍能逃”必须先被废除，才允许收束。
   证据：`combat_doupo_evidence.md: CD-02/CD-08/CD-09/CD-12`；`combat_xianni_evidence.md: XI-CX-06/XI-CX-12/XI-CX-15`；`combat_zhetian_evidence.md: E03/E04/E11`；`combat_tunshi_evidence.md: CT-03/CT-06/CT-13`。

2. **Threshold-first：先给可见阈值，再补机制。**
   一次防御失效、身体异常、空间反应或策略转向，足以先建立危险尺；不要先输出能力说明书。
   证据：`combat_xianni_evidence.md: XI-CX-02/XI-CX-05/XI-CX-07/XI-CX-16`；`combat_doupo_evidence.md: CD-04/CD-08/CD-09`；`combat_tunshi_evidence.md: CT-01/CT-10/CT-12`。

3. **旧方案失效 → 行动空间变化 → 新动作。**
   新招必须利用已经发生的地形、阵法、气机、位置或攻防限制；不能把“更大的招”当作因果。
   证据：`combat_yishizhizun_evidence.md: E02/E05/E07/E10`；`combat_doupo_evidence.md: CD-02/CD-08/CD-10`；`combat_xianni_evidence.md: XI-CX-08/XI-CX-14`。

4. **每个展开拍只改变一个可追踪变量。**
   多能力、多装备和团队配合应按“暴露、限制、破防、牵制、终结、收束”的因果接力写，而不是按技能名称罗列。
   证据：`combat_yishizhizun_evidence.md: E01/E07/E10`；`combat_tunshi_evidence.md: CT-07/CT-09/CT-13`；`combat_quanqiu_evidence.md: CQ-02/CQ-09/CQ-11`。

5. **资源和伤势必须转化为行动条件。**
   资源要买到承伤次数、撤离时间、攻击窗口或下一阶段资格；伤势要改变职责、站位或撤离优先级。
   证据：`combat_quanqiu_evidence.md: CQ-01/CQ-02/CQ-03/CQ-06/CQ-10/CQ-11`；`combat_xianni_evidence.md: XI-CX-01/XI-CX-09/XI-CX-11`；`combat_doupo_evidence.md: CD-02/CD-07/CD-10`。

6. **Stop 要检查未支付的逃生资源和无解边界。**
   目标仍有一次性法器、援手、空间出口或代价转移时，不能因“已经重伤”直接写死；角色确认无解时，也可以以撤退、保存选择权或既有世界机制收束。
   证据：`combat_xianni_evidence.md: XI-CX-06/XI-CX-08/XI-CX-12/XI-CX-16`；`combat_yishizhizun_evidence.md: E04/E11/E12`；`combat_doupo_evidence.md: CD-07/CD-09/CD-12`。

# Cross-Book New Judgments

## Source-specific observation 合成

- 《斗破》最强的是胜利机制、底牌递进、公开重估和碾压边界：命中不等于结束，底牌必须改变敌方选择。
- 《仙逆》补上阈值先行、追逃机会账户、准备期/交战期分层和残余逃生资源。
- 《遮天》补上尺度迁移、策略被迫转换、局部战场与旁观者功能。
- 《全球高武》最清楚地展示资源行动化、伤势改职责、保护目标重画战场拓扑。
- 《死人经》补上有限视野、首次接触点、误判重估和多方混战骨架。
- 《吞噬星空》补上大尺度 ruler、能力束因果折叠、dominance 的选项剥夺和团战反证明。
- 《一世之尊》补上单变量拍、行动空间因果、诱导翻盘门槛、功能接力和诚实无解出口。

## 具体 taxonomy 判断

| 候选 | reader live question | state model / beat engine / stop | 暂定结论 |
|---|---|---|---|
| duel / parity | 双方如何围绕当前优势互相改写胜负？ | 仍是主动权、距离、资源、回应；`作用→应对→新变量`；胜负/脱离即停 | **Core 条件**，加 `power_parity`，不独立 |
| underdog | 弱方如何利用窄窗口改变胜负？ | 力量差、资源、位置、时间仍是 Core 变量；窗口关闭即停 | **Modifier**：`power_asymmetry_window` |
| dominance | 对手还有哪些有效选项，如何逐项失效？ | 仍是剥夺承伤、反击、逃跑、复原等选项；最后进入处置/重估 | **Modifier**，通常组合 `combat + showcase_evaluation` |
| adaptive counterplay | 对手看见什么后，如何改写成功条件？ | 信息来源→识别节点→改变目标/站位/防御→暴露新角度 | **Combat Core 深化**，不是新 Skill |
| protect / hold | 保护对象、阵地或时间窗口能否守住？ | 保护完整度、覆盖位置、敌方目标、路线/倒计时、接班资源；拦截→换位→转移→牺牲→封锁；对象安全/丢失/窗口耗尽/转战即停 | **唯一达到新 Primary 门槛的候选**：`combat_protect_hold` |
| ambush | 首次接触是否在低信息下产生不可逆结果？ | 暴露风险、距离、接触点、第一击后果；接触前后状态改变即停或转战 | `stealth_infiltration → combat`，加 `surprise_contact` |
| multi-actor | 局部战中谁的行动改变了谁的下一拍？ | 角色职责、援救、视野、支线兑换主线时间/地利/退路；控制权或撤离权改变即停 | 普通多人战并入 Core；最多保留一个受控 Variant 候选 |
| battlefield local POV | 大尺度局势如何被局部人物实际感知和改变？ | 尺度、通信、支援、局部后果；局部目标或行动权改变即停 | **不是独立 Skill**，是 `scale_anchored_local_pov` Modifier |

保护/守点之所以是 Primary，而不是 Variant，是因为它改变了主要阅读问题：从“谁赢”变成“什么必须守住”。其余候选要么只改变变量配置，要么只改变展示尺度。

多角色与局部战场可以合并成一个未来的 `combat_local_coordination` **PILOT Variant**，但目前不进入 production 判定。它只有在通信延迟、职责接力、局部支线兑换主线资源真正改变 beat loop 时才成立。
证据：`combat_quanqiu_evidence.md: CQ-03/CQ-06/CQ-09/CQ-11`；`combat_zhetian_evidence.md: E07/E09/E10/E12`；`combat_tunshi_evidence.md: CT-03/CT-09/CT-11`；`combat_sirenjing_evidence.md: SE-06/SE-07/SE-09`。

# Taxonomy Decisions

- `combat_parity_duel`：MERGE → `combat + power_parity`
- `combat_underdog_upset`：MERGE → `power_asymmetry_window`
- `combat_dominance_payoff`：MERGE → `dominance`，需要时组合 `showcase_evaluation`
- `combat_adaptation_counterplay`：MERGE → Combat Core 的 `counterplay lifecycle`
- `combat_protect_hold`：KEEP，作为新的 Primary 候选，而不是 Combat Variant
- `combat_ambush_assassination`：MERGE → `stealth_infiltration → combat` + `surprise_contact`
- `combat_multi_actor_melee`：不单列；普通情况仍是 Combat Core
- `combat_large_scale_local_pov`：REJECT 为独立 Skill；保留为尺度/POV Modifier
- `public_proof`：`combat + showcase_evaluation`
- `wounded_survival`：`combat + survival_endurance` 或 `chase_escape`，不单列
- `rule solving`：若成为主要问题，交接 `deduction_reveal / comprehension_insight`

现有 `Secondary` 不应继续同时表示“同场叠加”和“后续换场”。后续应明确区分：

- 同场影响：Variant / Modifier；
- 主要问题改变：Handoff；
- 保护目标本身成为主要问题：直接选 `combat_protect_hold`。

# Evidence Still Needed

当前证据足以做 Preliminary taxonomy，但不足以裁决所有 Pilot Variant。

- **《武道宗师》**：需要真正的同阶技术对决窗口，包含架势、节奏、预判、假动作和最小充分停点；同时需要公共竞技中裁判/观众/对手改变行动的窗口。否则不能把 parity 或 public proof 升级。
- **《永夜君王》**：需要保护/守点、伤势生存、伏击追击和大尺度局部 POV 的连续窗口，尤其要看到弹药、伤势、撤离窗口如何改变职责，而不是只证明“很危险”。
- **《诡秘之主》**：只有在回传窗口直接展示战斗中的信息边界、身份隐藏、规则发现和有限揭露，才可影响 Combat taxonomy；否则应归入 `exploration / horror / stealth`，不能用作战斗 Variant 证据。
- **《全职高手》**：需要团队协同窗口：角色职责、目标切换、通信/视野、接力和局部结果如何改变全队下一拍。重点不是人数，而是是否出现独立的 team beat loop。
- **《将夜》**：主要用于 Voice、World Entry、公共权威和社会定价。只有回传战斗窗口同时包含公开见证、身份/地位重估或大场面局部 POV，才可补强 Combat；不能仅凭作品印象迁移。

还需要一组同 Mission、同 Canon 的盲读 A/B：

1. `combat Core` vs `combat_protect_hold`；
2. `combat Core` vs `combat_local_coordination`；
3. `combat + compact Modifier` vs 完整 Variant。

只有 Variant 稳定改变 beat loop、减少具体失败，且不需要标签表，才有 production 资格。

# Primary vs Reviser Split

## Generation Lens

```yaml
generation_lens:
  reader_live_question: "本场读者现在最想知道什么？"
  current_condition:
    - current_win_condition
    - protected_object_or_exit_condition
    - visible_ruler
  state_model:
    - position_and_distance
    - resources_and_injury
    - opponent_options
    - information_boundary
    - protection_or_escape_state
  beat_engine:
    - "action -> opponent/environment response -> one state update"
    - "old plan fails -> action space changes -> new action"
  expansion:
    - first threshold
    - first failure
    - first counterplay
    - irreversible result
  compression:
    - repeated exchange
    - same-function abilities
    - nonfunctional spectator reaction
  stop_rule:
    - victory
    - retreat
    - target/protectee secured or lost
    - escape resource exhausted
    - new primary question established
```

`combat_protect_hold` 只替换 `reader_live_question`、保护状态和对应 beat engine；不复制整套 Combat 规则。

## Revision Lens

```yaml
revision_lens:
  preserve:
    - Chapter Mission / Canon
    - current knowledge boundary
    - authorized opponent capability
  inspect:
    - each foreground beat changes the selected state
    - opponent has an information-grounded response
    - resources and injuries affect actual duties
    - result lands in body, position, target, relation, or action space
    - stop occurs after the current question is answered
  reject:
    - skill-name bookkeeping
    - fake counterplay
    - unexplained bigger move
    - forced reversal
    - repeated "震惊/占上风"
    - post-result tactical continuation
  repair:
    - local compression
    - restore missing spatial/result link
    - clarify one threshold or one response
```

Source evidence、未选择的 Variant、完整研究卡不进入 Primary 或 Reviser。

# Risks

1. **工程化风险**：把“每拍一个变量”“三拍 counterplay”“三种 dominance 信号”写成硬模板，会让正文像战术日志。它们应主要作为适用条件和 Revision check，不是每场必做的流程。
2. **Protect-hold 过度泛化**：只有保护对象/阵地/窗口是首要问题时才选；普通救援不能自动升级 Primary。
3. **Dominance 强制反转**：dominance 的核心是剥夺选项，不是每场都制造势均力敌或二次逆转。
4. **Ambush 强制反转**：伏击只要求首次接触改变物理或信息状态，不要求每次都有新敌人、新底牌。
5. **Local POV 变成伪全知**：只有局部观察导致真实选择时才切回远景；否则保持局部身体和行动后果。
6. **Taxonomy 膨胀**：parity、underdog、dominance、public proof、wounded、ambush 都不应各自成为 Primary。
7. **证据越权**：当前结论只适用于上述七份 evidence；等待回传的五本书不能用作品印象提前补 Canon 或 taxonomy 证据。

本次仅做只读 Preliminary Synthesizer，未修改 production 文件。
