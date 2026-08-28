---
name: novel-scene-skills
version: 0.2.0
description: >-
  在当前章事件与事实边界已经确定后，为中文商业长篇小说选择 Scene Primary，
  用 evidence-backed Deep Craft 帮 Curator 编译最小 Scene Prose Projection，并为 Authority Reviser
  提供极短、failure-triggered Revision Watch；不规划故事、不改 Canon、不把深研究直接塞给 Writer。
---

# Mission

本库只回答：

> 当前这场戏，读者持续追问的主要问题是什么；哪些状态变化值得获得笔墨；什么时候已经应该停？

它不是题材标签库，也不是 checklist。出现“比赛、战争、传承、拍卖、秘境、修炼”等名词，不自动产生 Skill。

# Runtime v2｜Deep Research, Narrow Runtime

Scene Skill 分三层带宽：

1. **Deep Craft**：`scenes/*.md` 保存完整、source-blind 的跨书判断、Generation Lens、Revision Lens、Failure Patterns 与 Stop；用于研究、维护和升级，不直接进入 production Primary。
2. **Projection Guidance**：Curator Catalog 只读取 `skill_id + Primary Reading Question + 一行 Projection Guidance`。Curator 只有在当前 Mission / Canon 仍存在真实 realization 缺口时，才把它编译成 2—4 句 `Scene Prose Projection`；已经清楚时写 `NONE`。
3. **Revision Watch**：Authority Reviser 只读取当前 Primary/Secondary 已验证安全的一行 `Revision Watch`。它只是 failure-triggered 检查，不是补写清单；没有对应失败时全部忽略，Preservation First。

因此：

- Terra Primary **不读取完整 Scene Skill 文档**；只消费 Curator 已编译的短 Projection。
- Luna Authority Reviser **不读取完整 Generation / Revision Lens**；只消费极短 Watch。
- 原著 evidence、书名、作者、locator、source-specific Prose DNA 永不进入章节 Runtime。
- raw GBrain 不因 Scene Skill v2 进入 Writer / Reviser。

# Selection Rule

每个场景选择 1 个 Primary Skill；必要时最多叠加 1 个 Secondary。Secondary 必须真的存在第二个同时工作的阅读问题，而不是为了“多用一个技能”。同章可按场景换 Skill。

Skill 只控制 HOW TO REALIZE，不得改变 Chapter Mission、Canon、人物决定、胜负、资源结果、State Change、Ending 或 UNKNOWN boundary。

## Primary Skills（24）

1. `social_bargain_decision`
2. `relationship`
3. `identity_reveal`
4. `departure_vacancy`
5. `sacrifice_convergence`
6. `reunion_reentry`
7. `comedy_banter`
8. `investigation`
9. `deduction_reveal`
10. `horror_anomaly`
11. `exploration`
12. `survival_endurance`
13. `stealth_infiltration`
14. `chase_escape`
15. `combat`
16. `hunt_acquisition`
17. `training_learning`
18. `comprehension_insight`
19. `trial_challenge`
20. `breakthrough_advancement`
21. `showcase_evaluation`
22. `resource_economy`
23. `crafting_creation`
24. `recovery_restoration`

具体 Deep Craft 见 `scenes/`。

# Shared Reference Lenses｜不进入 Primary Router

`references/` 保存跨场景、但不足以成为独立 Primary 的研究镜头：

- `character_voice_pressure`：人物声音来自压力下优先保护什么、愿为什么付代价，不来自口癖。
- `world_entry_lived_texture`：新世界通过准入边界、被使用/支付/承受的生活锚点和他人现实对待变得可生活。
- `desire_temptation`：欲望先改变注意、风险阈值与退出权，不自动变成占有、失控或推进。

它们用于升级 Scene Skills、校准 Curator / Human / World 投影，不作为可选 Primary/Secondary，也不形成每章配额。

# Taxonomy Promotion Rule

新证据首先用于**深化现有 Skill**。只有同时满足下列条件，才考虑新增 Primary：

- Primary Reading Question 真正不同；
- 需要持续追踪的 scene state 不同；
- 关键 beat 的生成循环不同；
- Stop / Handoff 条件不同；
- 且受控 A/B 证明一个短 conditional / modifier / existing composition 不能达到同等效果。

“经典书里这种场景很多”“研究预算很高”“规则很详细”都不是新增 taxonomy 的理由。战斗的势均、弱打强、碾压、适应、保护、团队、大战、规则/远程等优先作为 `combat` 内部 posture / conditional，而不是拆成十几个 Primary。

# Craft Rule

Deep Craft 的价值在**选择笔墨**，不是让正文更长：

- 展开会改变目标、关系、位置、行动许可、风险、资源、知识、身体功能或社会估值的 beat；
- 压缩无新信息的普通实施、重复证明、同功能动作、流程和解释；
- 技术细节只有在它改变下一选择时才前景化；
- 人物、对手、群体和环境必须按各自已知信息真实回应；
- 结果已经成立后，进入 consequence / handoff，不换证据继续确认。

# Source Boundary

本库由本地经典长篇的 source-first bounded windows 深读而来，经过 locator / anchor / observation Fidelity Audit 与跨书 synthesis。Source-specific evidence 可以很深，但 production 文件只保存 source-blind 可迁移判断。

禁止：复制原文、模仿作者声音、迁移角色口癖/专名/签名句法、把单书机制伪装成通用规则、让原著 evidence 直接进入 Writer。
