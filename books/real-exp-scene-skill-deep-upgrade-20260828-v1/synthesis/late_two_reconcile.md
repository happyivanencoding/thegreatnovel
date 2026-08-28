我将使用 `novel-scene-skills`，因为任务要求按当前 Scene Skill 的 production 边界审理尾部 evidence。全程只读；本次读取用于判断“晚补证据是否改变已有跨书 production 结论”，若发现新增，我只输出最小 source-blind delta，不改 Skill 或 production。先读取该 Skill 的完整入口说明，并做一次与 TGN Scene/late evidence 相关的轻量记忆检索。入口规则已确认：尾部 evidence 默认先深化现有 Skill；只有阅读问题、持续 scene state、生成循环、Stop/Handoff 都不同且现有 modifier 不足，才考虑 taxonomy 变化。下面的只读检索重点核对既有“late evidence / scene skills / fidelity”决策，避免把已经定论的内容重复当成新增。此次检查若命中旧结论，我会用它来区分“强化”与“production delta”。记忆检索只命中与本任务直接相关的约束：source-first、保留反例/负证据、`GAP CONFIRMED / NO PROMOTION`、Projection 仅在真实 realization 缺口时使用，以及一个 Primary 加至多一个必要 Secondary。现在读取用户指定的 8 个 evidence/synthesis/scene 文件和可选 reference；我会保留行号，便于最终给出可复核的 production 判断。指定的 5 个 evidence/synthesis 文件和 `references/character_voice_pressure.md` 不在当前工作树的这些相对路径；这会直接影响能否判定 fidelity 与已有 synthesis。具体检查目的是确认它们是否只是目录层级不同；若能找到同名文件，我继续只读这些文件，若找不到则明确报告证据缺失，不用 Skill 文件臆补。已定位到唯一同名 evidence/synthesis 文件，均位于隔离实验目录 `books/real-exp-scene-skill-deep-upgrade-20260828-v1`；Skill 与 reference 位于当前 `.agents`。这符合“只读审理实验输入、不改 production”的范围。接下来读取完整内容并按三层区分：fidelity 允许的证据、synthesis 已有判断、当前 Deep Craft/Projection/Stop 是否已覆盖。完整输出被终端截断，不能据此下结论。我不会用截断内容审理；改为按文件和标题/关键字段分段读取，优先抓 `Fidelity`、`Interpretation`、`Transfer`、`Production`、反例与 stop 条件，再回读必要证据窗口。这样能检测并避免“把未读全的 synthesis 当成已确认”；若出现缺段，我会继续补读。核心对照已完成：`late_two_fidelity` 判定没有 DROP；对话 lane 仅有一个可修正锚点，全部窗口可保留；探索 lane 的 E04、E06 必须整窗排除，E08 仅替换锚点后可保留。初步差集显示：Dialogue 有一个可合并的新增 production 判断簇（误判校正/未和解资源结算/空间投影），Exploration 主要是已有判断的强化，唯一可能新增的是“可行动空间尺度 ruler”。我正在做最后一次逐项差集复核，并确认不把 Projection Guidance 拉长。差集复核结论已收敛：Dialogue 的新增不是新 Primary，而是可放进现有 `social_bargain_decision` Deep Craft 的一个最小闭环；Exploration 只保留“空间尺度 ruler”这一项新增，其余属于既有行动地图、价值/进入权、压缩与 handoff 判断的强化。按工作区惯例，我会发送一封仅含完成状态的简短 Gmail 通知，然后在本对话给出正式四段输出；不会写入任何 production 文件。Gmail 通知第一次因当前连接器实际 schema 不接受 `body.mime_type/charset` 失败；这不影响本次只读审理。按错误提示去掉这两个可选字段重发，若仍失败则不再扩大范围，并在结果中说明通知未送达。# Dialogue Delta

**YES，存在一个最小 production delta。**

- Fidelity：14 个窗口中 DXL-01 仅替换锚点后保留，其他均 PASS；无 NARROW、无 DROP。[late_two_fidelity.md:8-27](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/late_two_fidelity.md:8)
- 新增判断是：多人同压下，优先级差异必须落到资源、位置、路线或责任；误判被纠正后必须立刻重排行动；价值无法兼得时，以资源实际投向结算，不强行制造共识；对白结果应有最小空间投影。[dialogue_diyixulie_evidence.md:379-417](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/dialogue_diyixulie_evidence.md:379)

# Exploration Delta

**YES，但只有一个狭窄新增：空间尺度 ruler。**

- 严格排除 E04、E06 两个 NARROW 窗口；E08 替换锚点后保留，其余相关窗口有效。[late_two_fidelity.md:28-39](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/late_two_fidelity.md:28)
- 新增判断：首次面对会影响进入或选路的未知空间时，应选一个可复核尺度——距离、深度、视野、地标或身体承受——并让它改变靠近、绕行、分层或撤退中的一次选择。[exploration_zhetian_evidence.md:266-274](C:/dev/tgn-story-mvp/books/real-exp-scene-skill-deep-upgrade-20260828-v1/evidence/exploration_zhetian_evidence.md:266)

# No-Change Judgments

- “对白必须产生可追踪状态变化”已有跨书结论和 `social_bargain_decision` 覆盖。[dialogue_synthesis.md:3-11](C:/dev/tgn-story-mvp/books/real-exp-scene-deep-upgrade-20260828-v1/synthesis/dialogue_synthesis.md:3)
- 压力下的首保对象、注意对象、代价边界属于已有 `character_voice_pressure`，无新增。[character_voice_pressure.md:8-12](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/references/character_voice_pressure.md:8)
- 笑点命中硬变量、出现现实回压后停止，已有 `comedy_banter` 覆盖；本 lane 不产生 comedy delta。[comedy_banter.md:12-16](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/comedy_banter.md:12)
- 探索的行动地图改写、价值不等于进入权、同质移动压缩、转入新主问题，已有 synthesis 与 `exploration` 覆盖。[horror_exploration_synthesis.md:42-53](C:/dev/tgn-story-mvp/books/real-exp-scene-deep-upgrade-20260828-v1/synthesis/horror_exploration_synthesis.md:42)
- `investigation` 的证据分层与 `deduction_reveal` 的旧证据重组没有新增 production 判断。[investigation.md:12-16](C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/investigation.md:12)
- 不新增 Primary、Hard Gate、固定轮数，也不拉长 Runtime Projection Guidance。

# Exact Production Delta

只建议在 Deep Craft 中加入两段最小 source-blind 文字；本次未修改文件：

- `social_bargain_decision`：

  > 多人共同承压时，仅保留能落到资源、位置、路线或责任的优先级差异；若新信息推翻了会改变部署的误判，下一拍必须重排站位、通路、目标或授权；价值无法兼得时，以稀缺资源的实际投向结算，不补强行共识，并让最小空间结构显示谁承担风险、谁有执行权。

- `exploration`：

  > 首次面对会影响进入或选路的未知空间时，选一个可复核的尺度 ruler，并让它直接改变靠近、绕行、分层或撤退中的一次选择；选择成立后压缩同质移动。
