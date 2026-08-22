---
name: novel-scene-skills
description: >-
  在当前章事件与事实边界已经确定后，为中文商业长篇小说的具体场景选择并注入最小、
  高密度的 Scene Skill。Scene Skill 只控制“这种戏怎样落成正文”，不规划故事、不改 Canon、
  不增加 Hard Gate，也不要求额外模型调用。
---

# Mission

本 Skill Library 只回答：

> 当前这场戏，读者持续追问的主要问题是什么？Writer 应按什么叙事发动机把它写成真正发生的场景？

它不是题材标签库，也不是 checklist。出现“比赛、宗门、战争、传承、拍卖、秘境”等名词，不自动产生新 Skill。

# Selection Rule

每个场景选择 1 个 Primary Skill；必要时最多叠加 1 个 Secondary Skill。Scene Entry、Travel、Ritual、Aftermath、Payoff 属于 Utility；Competition、Public Proof、Mystery、Horror、Comedy、Romance、Awe、Urgency、Sacrifice、Identity Reveal、Reversal 属于 Modifier。

同一章允许按场景切换 Skill。Skill 只改变“怎么写”，不得改变当前章事件合同、Canon 或已发生事实。

# Primary Skills

1. social_bargain_decision
2. relationship
3. comedy_banter
4. investigation
5. deduction_reveal
6. horror_anomaly
7. exploration
8. survival_endurance
9. stealth_infiltration
10. chase_escape
11. combat
12. hunt_acquisition
13. training_learning
14. comprehension_insight
15. trial_challenge
16. breakthrough_advancement
17. showcase_evaluation
18. resource_economy
19. crafting_creation
20. recovery_restoration

具体写法见 `scenes/`。

# Utilities

- scene_entry：把人物、地点、强者或新空间自然带入当前 Primary Scene。
- travel_transition：压缩没有新关系、信息、风险或选择的普通路程。
- aftermath：处理事件后的身体、关系、社会和行动余波。
- payoff_realization：让成长真正改变可做之事、资源、身份、生活与他人反应，而不只报数值。
- ritual_procedure：仪式作为晋升、恢复、献祭、召唤、继承等场景的执行方式时叠加。
- mission_frame：只提供 objective / constraints / reward / failure consequence / extraction condition。
- inheritance_transfer：只表示知识、身份、权限、资源或责任的转移。

# Composition Examples

- 猎取成长资源：hunt_acquisition → combat → breakthrough_advancement → showcase_evaluation
- 长期危险区域：survival_endurance + stealth_infiltration，局部切 combat / comprehension_insight
- 大赛：trial_challenge 或 combat + competition/public_proof/ranking
- 传承：trial_challenge → comprehension_insight → inheritance_transfer → payoff_realization
- 宗门建设：按实际场景使用 social_bargain_decision / resource_economy / showcase_evaluation / combat
- 战争：combat(mode=war)，战前联盟用 social_bargain_decision，战后利益用 resource_economy + payoff_realization

# Writer Contract

先确定 Primary Reading Question，再读取对应短 Skill。用人物当前欲望、知识、关系、能力与现场条件模拟场景，不扩写策划语言。每个重要动作应收到真实响应，下一拍由这个响应产生。结果已经被动作或对白表达后，不追加抽象总结；重大 payoff 可以继续通过体验、关系反应、社会反馈和实际收益停留。

# Source Boundary

本库由《超凡黎明》《斗罗大陆》《吞噬星空》等成熟中文男频长篇的场景结构抽象而来。只吸收 Scene Engine，不复制原文、不模仿作者声音、不迁移角色口癖、专名或签名句法。
