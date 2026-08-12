# Multi-Engine 原创 Seed 分类

所有测试输入均为原创合成 Seed；生产代码没有作品标题、人物、地名、境界或专名分支。

| Seed | Primary Drive | Secondary Drives | Progression Contract | 结果 |
|---|---|---|---|---|
| 失去超凡能力的矿工，用废矿声音重塑身体 | POWER_PROGRESSION | RESOURCE_OPPORTUNITY、WORLD_EXPLORATION | 有 | 完整 Progression Engine |
| 县城外科医生重建区域创伤救治体系 | CAREER_MASTERY | TEAM_GROWTH、STATUS_RISE | 无 | 无境界、突破、能量、战斗验证 |
| 地方官三年恢复边城人口、粮食与防御 | STATE_BUILDING | POLITICAL_STRATEGY、TERRITORY_FACTION | 无 | 不转化为个人战力升级 |
| 五名弃将组成电竞队冲击最高联赛 | COMPETITIVE_SKILL | COMPETITIVE_RANK、TEAM_GROWTH、CAREER_MASTERY | 无 | 技能、排名与团队驱动 |
| 午夜旧公寓多出房间并夺走人物记忆 | MYSTERY_INVESTIGATION | SURVIVAL_RESOURCE、MYSTERY_REVELATION | 无 | 不强制功法与战力阶段 |
| 城市职业存在禁忌晋升，顶层侵蚀身份 | KNOWLEDGE_PROGRESSION | MYSTERY_REVELATION、IDENTITY_PRESSURE | 有 | Progression + Mystery 接口并存 |

额外回归覆盖四个已知成长家族和三个 OOD 成长语法：团队能力槽、宇宙能量、城市集体主体、灭亡语言知识入口、不可逆选择与未来权柄均仍编译为同一个 adapter-neutral `ProgressionContract`，但使用不同主体、轴、拓扑、资源、验证和 Payoff Channel。

分类结果是 Proposal，不是 Truth 或 Canon。作者可以确认、提高辅助 Drive、逐项确认已有书建议或保持未确认；未确认状态不阻断 Legacy 工作流。

自动验收由 `tests/unit/test_narrative_drive_contracts.py` 的六组参数化原创 Seed 覆盖。职业、历史治理、电竞和灵异谜团的结果均不含力量境界、突破资源或战斗验证合同；只有包含 Progression Drive 的 Seed 会启用完整 Progression Engine。
