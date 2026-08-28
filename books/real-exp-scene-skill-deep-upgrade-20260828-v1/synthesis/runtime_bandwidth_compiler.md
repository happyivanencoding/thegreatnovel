我会先读取本任务对应的 Scene Skill / TGN 审计规则，并定位实验里的 candidate、各 synthesis 与 24 个 current skills；随后只做证据约束下的字段编译，不修改任何 skill 内容或文件。此次检查只用于发现“字段是否越权、是否超过字符预算、是否有 A/B 依据支持 Revision Watch”，若发现问题会在输出表中直接收敛到 `NONE` 或最小 stop 检查。本任务明确落在 `novel-scene-skills` 的“Scene Skill 只控制场景落成、不规划故事、不改 Canon”边界内；同时会用 `tgn-system-steward` 的最小归因审计原则来判断哪些字段有证据、哪些必须保持 `NONE`。我也已做了轻量记忆检索，确认本项目要求保留 `UNKNOWN`、不把计划当 Canon，并压缩已成立结果后的重复。现在读取两份技能规范及其要求的直接参考。已确认实验目录为 `books/real-exp-scene-skill-deep-upgrade-20260828-v1`。它包含候选 skill、指定 synthesis、两组 Projection/Primary A/B，以及 current 24 个场景 skill；当前工作树有大量既有未提交实验文件，我不会触碰。下一步只读取用户列明的材料，并把 A/B 证据限定为能直接支持局部修复的结果。材料结论已收敛：Projection Guidance 可以覆盖每个目标 skill，但都写成“缺口触发、盯住状态/尺/停点、已清楚则 NONE”；Revision Watch 只保留对白/关系及 relationship_final 已验证的离开、重逢、第三方授权牺牲局部失败，combat、protect、training 不设常驻完整 watch。现在做一次有界字符预算检查；它只检测字段是否超长，超长就直接压缩，不改变语义。字符检查通过：16 个目标字段均在预算内，Projection Guidance 最长 51 字，Revision Watch 最长 42 字。最终表将按你列出的 16 个 skill 输出；`combat_protect_hold` 不在覆盖名单中，因此不额外增行，但其 A/B 结论已用于不设 combat 常驻 watch 的判断。已按覆盖清单编译 16 个 skill；字段均通过字符预算检查，未修改文件。

| skill | Projection Guidance | Revision Watch | confidence | reason |
|---|---|---|---|---|
| combat | 仅当胜负尺、对手回应或资源后果不清时，盯住目标/位置/行动许可的变化与停止点；已清楚则NONE。 | NONE | high | 跨书战斗规则充分；本轮常驻修订收益不足。 |
| social_bargain_decision | 仅当谁要什么或本轮结算不清时，盯住条件、信息边界、发言资格与下一行动；已清楚则NONE。 | 仅修连续对白无结算或角色可互换：保留原决定与筹码，合并重复回合或补已有反应。 | high | 对白结算与局部保留修订均有直接支持。 |
| relationship | 仅当关系如何改写选择不清时，盯住具体欲望、对方回应与新边界/路线落点；已清楚则NONE。 | 仅修关系被命名却无行为后果，或单方付出被写成双向确认；保留既有边界与责任，局部补删。 | high | 关系 A/B 与跨书判断均支持最小修复。 |
| comedy_banter | 仅当笑点靶子或后果不清时，盯住面子/风险/任务偏移及现实回压停止点；已清楚则NONE。 | 仅修笑点未改变面子/任务/风险或越过现实后果：保留已成立后果，删重复梗或补已有回压。 | medium | 有对白跨书证据；修订范围需保持间接、局部。 |
| horror_anomaly | 仅当正常标尺、单一违例或可行动后果不清时，盯住规则失效与风险迁移；转生存/调查即停，已清楚则NONE。 | NONE | high | 异常判断清楚，但没有 Authority Reviser 直接 A/B。 |
| exploration | 仅当行动地图缺口出现时，盯住入口/路线/风险边界、发现后的选择与交接停止点；已清楚则NONE。 | NONE | high | 行动地图与交接边界明确；仅有生成对照。 |
| investigation | 仅当未知或证据层级不清时，盯住可检验问题、假设收缩与下一行动；证据足够即停，已清楚则NONE。 | NONE | high | 调查与推理的边界稳定，缺少直接修订证据。 |
| deduction_reveal | 仅当事实连接或行动后果不清时，盯住解释约束与一次改判/行动；结论成立即停，已清楚则NONE。 | NONE | high | 事实重组规则充分，但未证明常驻局部修订收益。 |
| training_learning | 仅当目标、偏差或可重复性缺口不清时，盯住可观察偏差、修法结果与可用性停点；已清楚则NONE。 | NONE | high | 本轮训练修订收益不足，避免常驻完整 watch。 |
| comprehension_insight | 仅当旧模型到新模型的连接不清时，盯住反例、暂定解释与一次预测/行动反馈；已清楚则NONE。 | NONE | high | 理解、训练、突破边界清楚；无直接修订 A/B。 |
| showcase_evaluation | 仅当新尺度或现实后果不清时，盯住基准、代表性用途与重新估价后的待遇/行动；已清楚则NONE。 | NONE | high | 尺度—用途—估价链稳定，修订安全性不足。 |
| breakthrough_advancement | 仅当旧门槛与新状态差异不清时，盯住首次可观察体验、限制与状态成立停点；已清楚则NONE。 | NONE | high | 门槛与首次体验边界明确，无直接修订证据。 |
| departure_vacancy | 仅当缺席变化不清时，盯住离开前基线、首个不能照旧完成的事与新责任；已清楚则NONE。 | 仅修缺席无前后基线或告别无行动变化：保留离开/失联状态与既有责任，局部删补。 | medium | 已验证离开前基线、首个缺口与行动化。 |
| reunion_reentry | 仅当辨认后关系位置不清时，盯住当前不匹配与新的共同动作/边界；共同位置成立即停，已清楚则NONE。 | 仅修辨认被写成旧关系复原或无共同动作：保留当前不匹配与现实限制，局部删补。 | medium | 已验证辨认后共同位置；防止自动复原。 |
| sacrifice_convergence | 仅当牺牲的授权或接手缺口不清时，盯住独立意志、授权链、现场缺口与幸存者接手；已清楚则NONE。 | 仅修第三方牺牲缺授权链：保留独立意志、现场缺口与幸存者责任，不补复活/奖励。 | medium | 仅第三方授权链获验证，其余维度不扩展。 |
| identity_reveal | 仅当揭露后的行动权不清时，盯住知识席位、证明物与有限权限变化；已清楚则NONE。 | NONE | medium | 身份揭露仍属 provisional，不能设常驻修订 watch。 |

注：`combat_protect_hold` 不在本轮明确覆盖名单中，故未另列；其 A/B 结果已用于 combat 的 `NONE` 判断。
