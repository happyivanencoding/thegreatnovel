我会按 TGN 系统审计技能执行这次只读 reconciliation；先读取技能规则，再严格限定在你列出的 audit、final、candidate 及 combat evidence 范围内。检查前的具体判定目标是：找出每条净新增 judgment 是否有至少 3 个不同 VALID source 包支持；若没有，就删除或降级，不扩 taxonomy、不把原著名带入 runtime。工作树存在大量与本任务无关的未提交改动，我不会触碰。`combat_final.md` 本身包含一次旧的综合草案，不能直接当验证结论；当前 `candidate combat.md` 才是待核对的 source-blind candidate。接下来我只读取 12 个非 tunshi 的 `combat_*_evidence.md`，并把 audit 标出的 DROP_WINDOW 整段排除；锚点替换只影响定位，不削弱对应 observation。# Validated Judgments（rule -> source file/evidence ids）

以下每条均有至少 3 个不同的非 tunshi、非 DROP_WINDOW source 包支持；anchor replacement 仅视为 locator hygiene。

- **Victory ruler / 命中不等于胜利**
  `combat_doupo_evidence.md -> CD-01, CD-07, CD-09, CD-12`；
  `combat_guimi_evidence.md -> CG-02, CG-04, CG-07, CG-13, CG-15`；
  `combat_zhetian_evidence.md -> E03, E04, E10, E11`

- **Threshold first / 先阈值、后最小规则**
  `combat_guimi_evidence.md -> CG-03, CG-05, CG-07, CG-09, CG-15`；
  `combat_xianni_evidence.md -> XI-CX-02, XI-CX-05, XI-CX-07, XI-CX-16`；
  `combat_quanzhi_evidence.md -> CQZ-02, CQZ-07, CQZ-10, CQZ-12`

- **State-changing chain / 旧方案失效 → 行动空间变化 → 新动作**
  `combat_yishizhizun_evidence.md -> E02, E05, E07, E10`；
  `combat_jiangye_evidence.md -> E02, M03, M05, M06`；
  `combat_doupo_evidence.md -> CD-02, CD-08, CD-09, CD-10`；
  `combat_guimi_evidence.md -> CG-06, CG-10, CG-11, CG-12`

- **Resource/injury actionization / 资源与伤势必须改变行动许可**
  `combat_quanqiu_evidence.md -> CQ-01, CQ-02, CQ-03, CQ-04, CQ-06, CQ-08, CQ-09, CQ-10, CQ-11`；
  `combat_yongye_evidence.md -> YY-E03, YY-M03, YY-M04, YY-M05, YY-L05`；
  `combat_jiangye_evidence.md -> E02, M02, M04, L04, L05`；
  `combat_dasheng_evidence.md -> DS-E04, DS-M02, DS-M03, DS-M05, DS-L02`

- **Opponent adaptation information discipline**
  `combat_doupo_evidence.md -> CD-02, CD-08, CD-09, CD-10`；
  `combat_guimi_evidence.md -> CG-03, CG-06, CG-08, CG-09, CG-12`；
  `combat_quanqiu_evidence.md -> CQ-01, CQ-05, CQ-09, CQ-11, CQ-12`；
  `combat_wudao_evidence.md -> CWM-03, CWM-05, CWM-12, CWM-13`

- **Parity conditional**
  `combat_wudao_evidence.md -> CWM-01, CWM-08, CWM-09, CWM-14`；
  `combat_doupo_evidence.md -> CD-04, CD-09`；
  `combat_yishizhizun_evidence.md -> E03, E05, E10`

- **Underdog conditional**
  `combat_jiangye_evidence.md -> E04, M04, M06, L01, L05`；
  `combat_xianni_evidence.md -> XI-CX-06, XI-CX-08, XI-CX-10, XI-CX-13, XI-CX-15`；
  `combat_dasheng_evidence.md -> DS-L02, DS-L03, DS-M02`

- **Dominance / dominance repricing**
  `combat_dasheng_evidence.md -> DS-E02, DS-E03, DS-R01, DS-R02`；
  `combat_doupo_evidence.md -> CD-06, CD-08, CD-11`；
  `combat_xianni_evidence.md -> XI-CX-10, XI-CX-13, XI-CX-15`

- **Team coordination conditional**
  `combat_guimi_evidence.md -> CG-01, CG-02, CG-03, CG-12, CG-13, CG-14`；
  `combat_quanqiu_evidence.md -> CQ-01, CQ-03, CQ-06, CQ-08, CQ-11`；
  `combat_quanzhi_evidence.md -> CQZ-03, CQZ-04, CQZ-05, CQZ-07, CQZ-08, CQZ-11, CQZ-12`

- **Battlefield-local conditional**
  `combat_yongye_evidence.md -> YY-E02, YY-M01, YY-M03, YY-L03, YY-L05`；
  `combat_zhetian_evidence.md -> E05, E07, E09, E10`；
  `combat_quanzhi_evidence.md -> CQZ-03, CQZ-08, CQZ-09, CQZ-10`

- **Rule-condition conditional**
  `combat_guimi_evidence.md -> CG-01, CG-02, CG-04, CG-07, CG-15`；
  `combat_quanzhi_evidence.md -> CQZ-02, CQZ-07, CQZ-10, CQZ-12`；
  `combat_yishizhizun_evidence.md -> E01, E02, E05, E07, E10, E12`

- **Ranged exposure conditional**
  `combat_yongye_evidence.md -> YY-E04, YY-E05, YY-M02, YY-L02, YY-L03`；
  `combat_sirenjing_evidence.md -> SE-02, SE-03, SE-05, SE-08, SE-11`；
  `combat_guimi_evidence.md -> CG-04, CG-06, CG-08, CG-10, CG-11`

- **Stop unpaid options**
  `combat_doupo_evidence.md -> CD-07, CD-09, CD-12`；
  `combat_xianni_evidence.md -> XI-CX-06, XI-CX-08, XI-CX-12, XI-CX-15, XI-CX-16`；
  `combat_guimi_evidence.md -> CG-02, CG-04, CG-07, CG-13, CG-15`；
  `combat_yongye_evidence.md -> YY-E04, YY-E05, YY-M03, YY-M05, YY-L05`

# Downgraded or Removed

- 整个 `combat_tunshi` 包不计入任何 judgment。
- `DS-L01` 删除出 combat 支持集：无对手、无即时交换，只是身体/环境测试。
- `CQ-07` 删除出支持集：其余 `CQ-*` 已足够支持资源、适应与 stop。
- `XI-CX-14` 删除出支持集：战前布置，不能支撑交战期 combat 规则。
- `combat_yishizhizun` 的 `E11` 删除出支持集；无解边界仍由 `E12` 及其他 source 包支持。
- `team_coordination` 保留为 **pilot-only Variant**，不晋升默认 Primary。
- `battlefield-local` 保留为 Modifier，不晋升独立 Variant。
- `rule-condition` 与 `ranged exposure` 保留为 Modifier / handoff，不新增独立 taxonomy。
- `combat_protect_hold` 保留为 candidate/pilot，不视为 production 冻结。

# Validated combat.md（完整 source-blind candidate）

```md
# combat

**Primary Reading Question:** 当前真正决定胜负的条件是什么；双方下一次行动会怎样让它失效、转手或重新成立？

## Use When

双方或多方正在围绕一个可观察的目标、位置、行动许可、资源窗口或退出条件发生即时冲突。若首要问题已经变成守住具体人/物/门/时间窗口，优先 `combat_protect_hold`；若已经转成追逃、潜入、生存维持、规则推理或公开估价，交给对应 Skill。

## Generation Lens

当本拍的规则尚未完整可知，且首次失效会改变下一选择时，先锁定一个读者可见的胜负尺，再让阈值或失败结果出现，随后只补本拍必须知道的局部规则。命中不一定等于胜利：若对手仍能逃、挡、复原、转移代价、召援或继续控制目标，正文要让读者知道还缺哪一层。

每个值得展开的动作只需承担一个主要变化：暴露、限制、破防、牵制、终结或收束；下一拍必须吃到前一拍留下的身体、位置、资源、视野、规则或行动权限变化。无新信息的普通交换、同功能招式和重复旁观反应压缩。

资源与伤势只有转成实际行动才值得前景化：它们应改变承伤次数、攻击窗口、移动、持武、职责、接班、撤离或目标控制。多能力、多装备和多人配合按功能链呈现，不按名称清点。

对手会按自己真实知道的信息改变目标、位置、节奏或反制；没有观察、理解或执行条件时，不为了“聪明”强行适应。

按当前 posture 调整注意力，而不是改成另一套流程：

- 势均力敌：让双方保留可信反制，直到准备、体力、位置、节奏或关键资源真的断一项。
- 弱打强：先让读者看见弱方还能争的窄窗口；窗口关闭时允许撤退、换目标，不把弱者硬写成五五开。
- 碾压兑现：用代表性交换逐层剥掉对手的承伤、反击、逃跑或复原选项；差距已可见就尽快结束，社会重新估价交给 `showcase_evaluation`。
- 适应反制：只有旧打法已经暴露且对手具备条件时，让对手改成功条件；主角的新动作必须利用刚变化的行动空间。
- 团队/大战：只跟踪会改变局部目标的职责与支援链；远景只在改变本地援助、撤离、视野或时间时进入。
- 规则/远程：只给当前动作所需的条件、视线、暴露、射界、冷却或媒介，不展开完整能力说明。

## Revision Lens

Preservation First。只在第一版存在明确失败时局部修：

- 读者不知道本场真正的胜负尺，补一个已授权的可观察条件，不补新机制。
- 招式/装备很多但删掉也不改变下一拍，压缩同功能交换，只保留状态改变链。
- 资源、伤势、距离或空间只是报数/疼痛/景观，若 Canon 已支持其行动后果，把它恢复成一次职责、位置、路线或选择变化。
- 对手连续吃招/震惊却不反制：先确认他是否已经获得信息和执行条件；有则恢复一个最小真实反应，没有则不要补“聪明反制”。
- 正文先讲完整机制再打，改成可见阈值/失效 → 最短必要规则 → 下一行动。
- 已经胜负清楚还继续同层交换、吹捧或二次证明，删到结果第一次落在身体、目标、行动空间或现实后果处。
- 不新增第二阶段、强制逆转、伤势、旁观者、底牌或计划外胜负。

## Failure Patterns

逐招流水账；技能目录替代因果；弱打强无可信窗口；碾压战硬拖；强敌无信息就神奇看穿；大场面只增加破坏景观；伤势不改变动作；每拍都解释谁占优；结果成立后重复证明。

**Stop when:** 胜负、撤退、目标得失、关键行动许可消失、无解边界成立，或新的高优先级目标接管；继续交换已经不再改变当前胜负问题。
```

# Fidelity Verdict

**PASS（经上述排除与降级后的 source-fidelity 结论）。**

所有保留的净新增 judgment 都能由至少 3 个不同 VALID source 包支持；未使用任何 DROP_WINDOW 或 `combat_tunshi` 证据。当前结论仍是 candidate/pilot，不等于 production 冻结。
