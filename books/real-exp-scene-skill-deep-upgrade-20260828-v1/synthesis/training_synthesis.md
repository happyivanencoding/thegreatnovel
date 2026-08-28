我会使用 `tgn-system-steward`，因为这项任务是在现有 TGN 训练/顿悟/突破/展示语义上做只读架构判断；同时我会查找并读取现有 `Selection Prose DNA` 与 `training_wudao` 证据，区分单书证据和跨书已建立技法。先做定向检索：它会检测真实文件位置、已有边界和证据链；若结果为空，我会改用项目约定的 PowerShell 搜索方式，而不是据此臆测不存在。本次检查的具体失败判据是：如果“训练/顿悟/突破/展示”在现有产物里没有清楚分工，或 `Selection Prose DNA` 把单书技巧误写成跨书规则，我会在结论中指出最早的语义坍缩层，并决定是深化现有 skill 还是拆分；如果边界和证据已经足够，我会明确说“不需要新 skill”。下面只读检查工作树、近期冻结状态、记忆索引和相关文件，不修改生产代码。工作树有大量用户/其他 agent 的未提交实验文件，我不会触碰它们。定向结果确认了本次相关产物集中在 `books/real-exp-scene-skill-deep-upgrade-20260828-v1`，并存在四个场景 skill、`training_wudao` evidence 以及 selection synthesis；下一步只读取这些文件和精确命中的 `Selection Prose DNA`，不把其他实验目录当作当前结论。证据边界已经收敛：`training_wudao` 是单书《武道宗师》的 16 个窗口，足以提出“可调用性分层、导师有边界退场、首次成功不等于稳定、训练准入与环境可纠正性”等候选规则，但不能单独升级为跨书 established craft。现有 Selection Prose DNA 的跨书稳定部分是“状态节点优先、具体承载物、因果/知识停点、反应改变下一拍、节奏跟随 beat”；它不提供训练专门证据。结论倾向于深化四张现有 skill，不拆新 skill，也不恢复独立 payoff utility。# Existing Coverage

结论：不拆新 skill，深化现有四张；不新增独立 `mentor`、`transferability` 或 `demonstration_payoff` skill。

- `training_learning` 已覆盖“具体偏差 → 调整 → 比较结果”、重复压缩，以及“不把练熟自动写成突破”。[training_learning.md](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/training_learning.md:3)
- `comprehension_insight` 已覆盖旧模型、反例、工作模型修正与最低现实反馈。[comprehension_insight.md](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/comprehension_insight.md:3)
- `breakthrough_advancement` 已覆盖旧上限、新状态与首次真实体验。[breakthrough_advancement.md](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/breakthrough_advancement.md:3)
- `showcase_evaluation` 已覆盖比较基准、立场化反应和现实后果。[showcase_evaluation.md](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/showcase_evaluation.md:3)
- 现有跨书 Selection DNA 已稳定支持：状态节点优先、具体承载物、因果/知识停点、反应改变下一拍、节奏跟随 beat；但它是 evidence/reference 层，不是训练专门规则。[GBRAIN_PROSE_CRAFT_V1.md](C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md:250)

# New Judgments

以下明确区分证据层级：

| 判断 | 证据等级 | 应如何处理 |
|---|---|---|
| 反馈应落在身体、对手、空间或数据暴露的具体偏差上 | 跨书 Selection 原则；《武道宗师》训练窗强化 | 深化 `training_learning` |
| 重复压缩条件不是“练了很多次”，而是错误—修法—结果关系不再变化 | 《武道宗师》单书强证据 | 作为训练 skill 的 stop rule，不宣称跨书定律 |
| “做得出”不等于“压力下可调用” | 《武道宗师》单书证据 | 加入可用性 ruler，不能直接写成完整战力 |
| 导师应从诊断纠正，转为交付前提、锚点和回问边界，最后否决错误目标 | 《武道宗师》单书证据 | 深化 mentor boundary，不拆 mentor skill |
| 首次成功 ≠ 稳定能力；还需间隔保持、压力调用或迁移证明 | 《武道宗师》单书证据 | 作为可选 proof ladder，不设强制四阶段 |
| 局部成功必须同时留下限制、代价和下一验证目标 | 单书训练证据 + 跨书 payoff/result-stop 原则 | 深化现有 payoff realization；不恢复独立 payoff Control |
| “能教会别人”是比“自己能发动”更高的迁移 ruler | 《武道宗师》单书、单窗偏强证据 | 暂作 optional advanced ruler，不能生产化为默认要求 |

`training_wudao` 自身也明确把这些列为现有 skill 的缺口，同时承认它们来自单书窗口；其 cross-window 结论不能自动等同于跨书 established craft。[training_wudao_evidence.md](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/training_wudao_evidence.md:367)

# Generation Lens

- `training_learning`：先写可观察目标；保留会改变练法的偏差；让下一次执行可比较；达到当前所需稳定度就停。
- 训练升级前，检查动作是否能隔次保持、错误是否会被新形式放大、现场是否可观察和止损。[training_wudao_evidence.md](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/training_wudao_evidence.md:435)
- `comprehension_insight`：先呈现旧模型，再呈现无法解释的反例；新理解必须改变一次预测、试验或选择，不继续讲完整理论。
- 导师：给前提、辨认锚点、边界和回问阈值，然后退出；不能全讲，也不能只说“自己悟”。[training_wudao_evidence.md](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/training_wudao_evidence.md:456)
- `breakthrough_advancement`：只有旧门槛真的失效、行动范围或身体状态发生新差异时才成立；一次局部效果不够。
- `showcase_evaluation`：只有当问题变成“别人必须怎样重新估价”时才进入；用最低充分证明触发待遇、价格、资格、策略或行动空间变化。
- Selection DNA 只作为条件化 Projection：已有事件链自然清楚时允许 `NONE`，不为满足 DNA 强行增加解释、反应或细节。[GBRAIN_PROSE_CRAFT_V1.md](C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md:127)

# Revision Lens

优先做以下修订：

- 把“悟性不足、练得不够、感觉不对”改成可定位的身体/注意/节奏/承载偏差。
- 合并不改变错误模型、练法或读者判断的连续尝试。
- 把一次成功降级为“局部功能”：补限制、代价和下一验证目标，不把它改成失败，也不升级成稳定能力。[training_wudao_evidence.md](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/training_wudao_evidence.md:449)
- 删除导师教程化讲解；保留足够让人物知道“不能照抄什么、该观察什么、何时求助”。
- 若旁观者只是重复“好强”，压缩为一个会改变判断或待遇的反应。
- 若展示已经完成功能证明，却继续测试同一层级，停止，不再追加炫技。

# Boundary With Comprehension/Breakthrough/Showcase

| 场景 | 核心问题 | 停止点 |
|---|---|---|
| `training_learning` | 能否把动作做得更稳定、可重复、可调用 | 当前情节所需的稳定度成立 |
| `comprehension_insight` | 是否形成了能改变判断或试验的工作模型 | 新模型获得最低现实反馈 |
| `breakthrough_advancement` | 是否跨过旧能力/身份/生命状态门槛 | 新状态通过真实体验或权限成立 |
| `showcase_evaluation` | 他人和读者是否必须重新估价 | 估价改变并产生现实后果 |

同一条能力链可以发生转换，但不是强制阶梯：

`想明白 → 练得稳 → 首次局部成功 → 压力调用 → 外部展示`

其中“首次成功、稳定能力、公共证明”必须保持不同语义；不能用展示替代训练，也不能用突破标签替代理解或稳定性。

# Evidence Needed

目前最需要的是跨书验证，而不是新建 skill：

- 为 `training_learning` 补《吞噬星空》《斗罗大陆》《全球高武》等训练、试炼、首次稳定复用窗口。
- 为 `comprehension_insight` 补《凡人修仙传》《灭运图录》《修真四万年》等反例、换模、试验反馈窗口。[selection_architect.md](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/selection/selection_architect.md:96)
- 每个窗口继续记录：反馈选择、被压缩的重复、ruler、下一拍、导师是否退场、首次成功与间隔后表现、是否迁移给他人、反证边界。[selection_architect.md](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/selection/selection_architect.md:213)
- 若同一判断在至少多个不同书籍、不同人物和不同训练条件下重复出现，才可升级为 cross-book established craft；若仍只有《武道宗师》支持，就保留为单书 evidence / pilot rule。
- 当前最小生产动作：深化 `training_learning` 的可用性、准入和压缩判断；深化 `comprehension_insight` 的导师边界；让 `breakthrough_advancement` 与 `showcase_evaluation` 明确接收 proof level，但不增加 Primary 数量。
