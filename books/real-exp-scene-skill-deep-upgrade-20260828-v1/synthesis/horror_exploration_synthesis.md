我将使用 `tgn-system-steward`，因为这次任务要在现有 TGN 体系内做跨书证据审计、判断是新增 Skill 还是深化既有能力。先读取该 Skill 的完整规范，再只读检索 `horror_daogui`、`exploration_guimi`、`Selection Prose DNA` 与相关 evidence；不会改动生产文件。先做三项有界只读检查：`git status` 用来确认不误读或覆盖并行改动；最近提交用来确认当前冻结边界；记忆检索用来找 `horror_daogui`、`exploration_guimi` 与 Selection Prose DNA 的既有判断。若发现冲突，我会以本轮指定证据和当前仓库事实为准；若没有相关命中，就不扩大考古范围。工作树已有大量用户/并行实验改动，我会保持只读，不触碰这些文件。记忆中没有直接命中两个证据集的既有条目，只有一般性的“机制必须改变选择/风险/结果、避免把 supporting logic 变成故事引擎”原则；因此下面以仓库内真实 evidence 为主，不把记忆中的一般原则冒充本轮新证据。接下来定位证据文件与现有 Selection Prose DNA 的实际路径。已定位到本轮专用实验目录，并确认其中有两套目标 evidence 与对应 findings。下一步我会做“差集审计”：读取四个现有 Scene Skill、Selection 层已形成的 Prose DNA/选择结论，再对照两个 evidence 的窗口结论，过滤掉已有判断（如“环境取舍”“旧证据重组”），只保留真正新增的八个能力点。检查的具体目的，是判断新增内容应落在现有 skill 的规则深化，还是存在一个跨 skill 的独立运行时能力；不会据此修改 skill。# Cross-Book/Adjacent Judgments

结论：不新增独立 Skill。应深化现有 `horror_anomaly`、`exploration`、`investigation`、`deduction_reveal`；`handoff` 应成为共享的 Curator/Runtime 交接契约，而不是第五张 Skill。

已有 Selection Prose DNA 已覆盖：

- Attention：把字花在状态变化处。
- Knowledge：解释到当前行动阈值。
- Causal：结果—局部原因—选择—后果。
- Reaction：用身体、物件、对白和社会反应外化状态。
- Rhythm：展开条件、空间、转折；压缩判定和重复结果。

本轮真正新增的是这些“场景状态判断”：

1. `normal ruler`：先建立“本应如何运作”的具体日常标尺。
2. `single rule violation`：每一轮只打断一条清晰规则。
3. `evidence layers`：主观异感、身体残留、他人见证、制度记录分层使用。
4. `perception budget`：明确保留哪一种感知；更多信息可能降低行动能力。
5. `risk state migration`：风险不是“更吓人”，而是策略空间从未知、怀疑、验证、兑现到规避逐步收缩。
6. `knowledge permission`：事实、支持性推断、未知原因不能混写；知道不等于获准深入。
7. `discovery slow-down threshold`：只有发现改写路线、风险、目标或解释模型时才放慢。
8. `handoff`：交接行动地图、证据可信度和风险阶段，接收 Skill 不重新导览。

证据见[恐怖 findings](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/horror_daogui_findings.md:22)与[探索 findings](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/exploration_guimi_findings.md:26)。

# Horror v2

深化 `horror_anomaly`，不拆分子类。

核心链：

`normal ruler → one rule violation → evidence response → character action → risk migration / handoff`

- 先让读者知道安全、熟悉或可预测的结果，再破坏其中一条规则。
- 每个异常 beat 只保留一个硬违例；前一违例尚未结算前，不继续堆黑影、怪声和新名词。
- 身体反应只有在能与另一层动作、物件或空间形成可复核映射时，才算证据；否则只是情绪装饰。
- 至少区分“主观感到什么”和“什么在身体、他人或记录层面留下后果”，不要求每场强行凑齐四层。
- 感知越多不必越接近真相；应保留一个能行动的感知通道，并让过量感知产生具体代价。
- 普通解释已经覆盖关键因果时，警报必须结算；只有新的因果违例出现，恐怖才重新启动。
- 当异常已被多人共享、可预测、可组织利用，主问题转为生存、战斗、关系、资源或余波，不再继续写 Horror。

# Exploration v2

深化 `exploration`，并把部分规则同步到 `investigation` 与 `deduction_reveal`。

- 发现只有在改写行动地图时才放慢：
  `观察差异 → 暂定判断 → 环境/他人回应 → 新选择`。
- 仅增加奇观、地点名或背景资料，不改变路线、风险、目标、资源或解释模型时，压缩。
- 风险推进必须表现为策略变化：能否继续、是否要绕行、谁承担失败、是否还能撤离，而不是形容词升级。
- 高价值地点不等于当前拥有进入权限；能力、情报和失败代价不足时，延迟进入本身就是有效行动。
- 调查中每条信息标为：直接观察、当前可支持推断、仍未知原因。下一步只能使用前两者支持的最小结论。
- 旧证据重释必须接入新的时间、位置、对象或规则约束，并改变调查对象或验证动作；这部分是深化 `deduction_reveal`，不是新增能力。
- 当风险状态稳定、规则已可预测，退出 Exploration/Horror，转入 `survival_endurance`、`combat`、`investigation` 或 `aftermath`。

# Handoff Rules

`handoff` 是共享场景转换契约：

1. 交出当前行动地图：人物在哪里、哪些入口/路线仍可用。
2. 交出证据层级：已观察事实、可用推断、可信度和仍未知的原因。
3. 交出风险阶段：未知、怀疑、验证、兑现、规避，以及策略空间剩余多少。
4. 明确接收 Skill 的新主问题。

接收方只消费这组状态，不重新介绍地点、不重演已经完成的探索、不重复上一 Skill 的语气。

当前库允许同章切换 Skill，但 Runtime 实际仍主要渲染一个 Primary 与一个 Secondary；因此缺的是交接状态，而不是新 Primary。[现有选择规则](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/SKILL.md:17)；[Runtime 渲染边界](C:/dev/tgn-story-mvp/src/story_mvp/scene_skills.py:99)。

# Generation Lens

生成时只问：

- 这里的 `normal ruler` 是什么？
- 当前只坏了哪一条规则？
- 哪一层证据真正改变了行动？
- 人物还保留哪一种可靠感知？
- 风险是否发生了状态迁移，策略是否变少？
- 发现是否越过“改写路线/风险/目标/解释”的放慢阈值？
- 当前已经转入哪个新主问题，是否需要 handoff？

# Revision Lens

优先删改以下失败：

- 用“阴森、诡异、不可名状”代替具体规则违例。
- 一次堆多个异常，却没有人物判断和行动。
- 身体疼痛没有对应动作或后果，只承担气氛。
- 信息过量导致空间不可追踪，或纯模糊导致危险无方向。
- 反复写“更危险”，但路线、撤离权、目标或代价没有变化。
- 把证人猜测写成事实，把未知原因写成机制全貌。
- 发现段写成导览，没有产生下一选择。
- Skill 切换后重新介绍同一地点，或继续使用已退出 Skill 的叙事发动机。

# Evidence Gaps

- 目前新增判断来自两个有界研究 lane，不能升级为所有 Horror/Exploration 的普遍定律。
- 没有生产级 A/B 证明 v2 规则稳定提升正文，因此应先作为 Scene Projection / Pilot，不直接冻结为强门禁。
- `evidence layers` 的具体层数不是硬模板；不同场景可能只需要身体层加一层外部验证。
- `perception budget` 没有固定数量阈值，只能作为场景局部的感知取舍。
- `discovery slow-down threshold` 是条件判断，不应量化成字数、段落数或固定 beat 数。
- 当前 Runtime 尚无真实 handoff artifact 的验证证据；后续应先做一个 Exploration→Investigation 或 Horror→Survival 的最小 A/B。
