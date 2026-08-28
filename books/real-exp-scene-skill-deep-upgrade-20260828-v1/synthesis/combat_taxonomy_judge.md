我会按 `tgn-system-steward` 做独立只读裁决：先读完整 Skill 与相关历史索引，再定位本实验的 combat skills、taxonomy/selection outputs、`combat_preliminary.md` 和全部证据。这个任务可拆成独立证据审计，我会先确认并发配置；若允许，将让只读 worker 分别核对“Primary 候选”和“variants / lens 风险”，主线程负责统一判准、复核与最终裁决。不会搜索或推断 Luna final synthesis。已确认当前配置没有把并发线程锁为 1；工作树存在大量并行实验文件和 3 个已修改 production 文件，本次严格只读，不会触碰它们。`tgn-system-steward` 要求把受控实验与 production default 分开，所以我会把“跨书稳定差异”作为升级门槛，而不是把高预算或候选命名本身当作证据。现在并行核对两组原始 combat 书证与一组 production/selection/preliminary。第一轮交叉读已经暴露一个关键冲突：`combat_preliminary.md` 把 `protect_hold` 判成新 Primary，但当前 production `combat.md` 本来就把“保护对象、目标控制权、目标得失”纳入状态与停止条件。也就是说，真正要证明的不是“守护战很重要”，而是它是否稳定改变 beat loop 到短 Modifier 无法表达。接下来我正在回到各书原始 evidence 的 posture、state-changing exchange、ruler 与 stop point 核对这件事，同时单独检验团队战与局部战场是否真的越过现有 Core。目前的独立判断已经接近收敛：13 书证据足以证明“不同战斗要追踪的局部状态不同”，但还没有证明“必须靠 taxonomy 字段而不是一段条件化 Core 指令”才能表达。尤其三份实验输出彼此并不一致：一份主张 `protect_hold` 新 Primary，另一份主张 `team_coordination / battlefield_local` Pilot Variant，preliminary 又把后者合成未准入 Pilot。这种分类不稳定本身就是暂缓 promotion 的证据，不是坏事。正在等三路逐书审计回传做最后反证。原始证据的反证方向也已确认：`protect_hold` 的确跨《全球高武》《将夜》《永夜君王》《遮天》稳定改变胜利尺，但这些变化仍可压成“保护对象/覆盖位置/路线或时间窗/敌方换目标/安全或失守即停”这一小段条件化差量；团队战同样可压成“职责动作暴露限制、局部目标兑现后换问、支线结果回流主线”。目前没有发现必须新增 Primary 或字段才能保住这些差异的证据。最后只剩并行审计的逐书行号汇总；我已要求它们停止扩读并立即收敛。主判断暂未被反证：可 promotion 的是少量 Combat Core 深化；`protect_hold`、团队协同、局部战场和其余姿态都应先接受“compact conditional / existing composition 能否同等表达”的反事实 A/B，不能因证据预算高就直接升级 taxonomy。Lens 分离则是另一个结论：分离原则可进入 production 设计，但富内容 Lens 仍需单独 A/B。结论：这批 13 本书的高预算证据足以支持“深化现有 Combat Core”，不足以支持任何新的 production Combat Primary、Variant 字段或 Variant 枚举。证据证明了姿态差异存在，却没有证明短条件化 Modifier、Scene Prose Projection 或现有 Skill composition 表达不了这些差异。

我没有搜索、读取或推断 Luna final synthesis。

## 候选裁决

| 候选 | Verdict | 裁决理由 |
|---|---|---|
| deepen combat core only | **通过** | 跨书稳定新增的是：先明确当前胜利条件/可见阈值；旧方案失效必须改变行动空间；资源、伤势必须改变实际职责或选择；Stop 前检查敌人尚未支付的逃生、恢复、转移或反击资源。这些是同一 Combat Engine 的深化。 |
| add optional variant field | **暂缓，不进 production** | 当前 Runtime 只解析 `Primary/Secondary`，没有 Variant/Modifier 通道；现有 Scene Prose Projection 已能承载短条件化差量。证据尚未证明新增字段比一句 Modifier 更有效。[scene_skills.py](/C:/dev/tgn-story-mvp/src/story_mvp/scene_skills.py:99) [prompts.py](/C:/dev/tgn-story-mvp/src/story_mvp/prompts.py:621) |
| new `combat_protect_hold` Primary | **否决为 Primary；保留实验 Lens** | 守护戏确实跨《全球高武》《将夜》《永夜君王》《遮天》稳定改变状态变量，但现有 Combat 已包含保护对象、目标控制权、退路和目标得失 Stop。其差量可压成“保护对象/覆盖位置/路线或时间窗/敌方换目标/安全或失守即停”，没有改变底层 action→response→state loop。[combat.md](/C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/combat.md:5) [combat_quanqiu_evidence.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_quanqiu_evidence.md:310) |
| `team_coordination` variant | **不升级** | 职责动作暴露限制、队友获得窗口、局部目标接力、支线结果回流主线，跨书成立；但现有 Combat 已明确覆盖分工、救援、视野与局部目标。用短 Modifier 足够。[combat_quanzhi_evidence.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_quanzhi_evidence.md:263) |
| `battlefield_local` variant | **不升级** | “远景压力→局部节点→人员/弹药/阵地结算”在《永夜君王》《遮天》等书稳定存在，但这是尺度与 POV 控制，不是新发动机；现有 Combat 已要求大型战争使用局部 POV。[combat_yongye_evidence.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_yongye_evidence.md:297) [combat_zhetian_evidence.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_zhetian_evidence.md:417) |
| parity | **短 Modifier** | 改变初始力量关系和反制资源，不改变主问题、循环或 Stop。 |
| underdog | **短 Modifier** | 具体化弱方的窄窗口、成本与可争目标；可与 `chase_escape`、`survival_endurance`、保护目标组合。 |
| dominance | **短 Modifier / `combat + showcase_evaluation`** | 战斗负责剥夺对手有效选项，Showcase 负责社会重新定价；无需独立 Variant。[combat_dasheng_findings.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_dasheng_findings.md:28) |
| adaptation | **并入 Core** | 对手依据已见信息改目标、站位、距离或成功条件，是“真实回应”的基本要求；另设 Variant 等于把“写好 Combat”重复分类。 |
| ambush | **`stealth_infiltration → combat` + 短 Modifier** | 接触前主要追问是暴露；第一次有效接触后转 Combat。只有首次接触点和有限信息需要额外强调。[combat_sirenjing_evidence.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_sirenjing_evidence.md:147) |
| rule-condition | **Core 条件句 / 必要时 Handoff** | 条件、媒介、行动许可和打断点跨书成立；若读者主要追问变成“规则究竟是什么”，应转 `deduction_reveal`、`comprehension_insight` 或 `trial_challenge`，不造规则战 Variant。[combat_guimi_findings.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_guimi_findings.md:30) |
| ranged exposure | **武器域 Modifier，暂不升级** | 《永夜君王》证据很强，但跨书稳定性明显较弱；距离、暴露、死角、装填、过热本质仍是位置与资源变量。[combat_yongye_findings.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/combat_yongye_findings.md:21) |

三份实验产物本身也尚未收敛：`focused_taxonomy` 主张新增 `protect_hold` Primary，而 `taxonomy_architect` 主张 `team_coordination / battlefield_local` Pilot，preliminary 又把后两者合并为未准入 Pilot。[focused_taxonomy.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/selection/focused_taxonomy.md:9) [taxonomy_architect.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/selection/taxonomy_architect.md:22) [combat_preliminary.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/synthesis/combat_preliminary.md:49)。这不是投票问题，而是说明同一证据仍可被较短的 Core/Modifier 解释，未达到 taxonomy promotion 门槛。

## Generation Lens / Revision Lens

**分离原则应 promotion，但不应同时 promotion 一套富内容 Variant Lens。**

建议冻结为确定性的可见性边界：

- Primary Generation Lens：只含 reader question、当前状态、beat 生成、展开/压缩和 Stop。
- Reviser Revision Lens：只含具体 failure signal、minimum repair、preserve 和修订 Stop。
- Reviser 不接收 Beat Engine、未选 Variant、原著证据或完整研究解释。

当前 Authority Reviser 会收到完整 Curator，其中包含 Scene Skill Selection、Opening Strategy、Projection 等生成期信息；这与其“不是第二个 Writer、默认保留正确正文”的职责存在张力。[hybrid_runtime.py](/C:/dev/tgn-story-mvp/src/story_mvp/hybrid_runtime.py:650) [prompts.py](/C:/dev/tgn-story-mvp/src/story_mvp/prompts.py:2039)

因此可以 promotion “分离边界”，但具体 Combat Revision Lens 仍须 A/B 后才能进入 production。

## 最大风险

最大风险是 **procedural combat**：把“每拍一个变量”“对手必须适应”“职责接力”“未支付资源检查”等观察硬化成固定流程，最终会生成战术日志。`combat_preliminary` 自己也已识别这一风险。[combat_preliminary.md](/C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/synthesis/combat_preliminary.md:173)

其余风险依次是：

- **over-routing**：同一窗口经常同时是伏击、保护、团队、远程和局部战场；多 Variant 会让标签而非主要阅读问题决定写法。
- **second-writer drift**：Reviser 若收到 Generation Lens，容易补造反制、逆转、伤势或第二阶段。
- **prompt bloat**：175 个窗口最终只收敛出少量稳定判断；把书别规则全部投影到运行时只会重复和稀释重点。

## 最小 production recommendation

只改深度，不改 taxonomy：

1. 保留唯一 `combat` Primary。
2. 在 `combat.md` 增加三条条件化软规则：
   - 首轮明确当前 victory ruler 或可见阈值；
   - 旧方案失效后，下一动作必须利用已经发生的空间、资源、伤势或信息变化；
   - Stop 前检查对手是否仍有已建立的逃生、恢复、转移、反击或条件完成能力。
3. 不新增 ID、Variant 字段、Router 分支或兼容层。
4. Generation/Revision Lens 分离作为独立架构实验，不与本次 Combat taxonomy 修改绑在一起。

## A/B Gate

先做近单变量生成实验：

- A：当前 `combat.md`。
- B：当前 Core + 上述三条 compact delta。
- 冻结同一 Mission、Canon、Human、Curator、模型与 effort。
- 样本覆盖守护、团队接力、局部战场、规则条件、远程暴露，并加入简单 dominance/单次接触作为负向样本。

只有 B 跨至少三种世界稳定修复同一种具体失败——读者不知道当前争什么、动作没有改变状态、敌方不回应或结果成立后仍续打——同时不增加事实、固定反转、战术说明和无必要篇幅，才更新 Core。

随后才测试 taxonomy 必要性：

- A：深化 Core + 一句 compact Modifier。
- B：深化 Core + 完整 Variant。
- 若 Modifier 达到同等效果，Variant 永久不 promotion。

Reviser 单独测试 `Authority-only` 对 `Authority + minimal Revision Lens`；只有它能修复目标局部、同时基本不碰已经正确的正文，Lens 内容才准入 production。

本次为只读裁决，未修改任何文件。
