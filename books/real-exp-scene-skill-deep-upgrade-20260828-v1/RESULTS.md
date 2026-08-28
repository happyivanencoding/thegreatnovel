# Scene Skill Deep Upgrade v2 — Final Results

## Verdict

**PASS — productionized.**

本轮不是把 Scene Skill 变成更长的 Writer Prompt，而是完成了一个更深的离线 Scene Craft 研究层，并把章节 Runtime 收窄：

`经典原著 bounded evidence → Fidelity Audit → cross-book source-blind Deep Craft → Curator compact Catalog → 2–4 句 Scene Prose Projection / NONE → Terra Primary → Luna Authority Reviser（仅少数短 Revision Watch）`

raw GBrain、原著书名、locator、完整 Generation/Revision Lens 均不进入章节 Writer / Reviser。

## Research Scope

- **64 条 source-first research lanes**，覆盖 **26 本经典长篇**。
- Combat 获得最高 craft resolution；同时补深 Dialogue / Relationship / Horror / Exploration / Training / Showcase / Chase / Stealth / Survival / Hunt / Resource / Crafting / Recovery / Trial / Breakthrough / Departure / Reunion / Identity / Sacrifice 等高频 family。
- 八组正式 Fidelity 报告合计记录 **857 次 bounded-window 审核**；其中 **21 个 DROP_WINDOW**，其余通过或仅需真实短 anchor / locator / observation 收窄。
- Combat 审计：175 windows，17 drop；整包无法可靠复核的来源直接退出正式证据，不为保结论硬留。
- Event 第一轮审计：129 windows，4 drop。
- 其它主要批次（218 + 81 + 80 + 81 + 67 + 26 windows）没有整窗 drop，主要处理 anchor / title / observation hygiene。

## Taxonomy Decision

### Production Primary

保持 **24 个 Primary Scene Skills**。没有因为研究预算高、某类场景重要，就机械增加大量新 Primary。

### Combat Family

`combat` 被显著深化，但最终**不拆成十几个 production Primary**。以下作为同一 Combat Core 的条件化 posture：

- 势均力敌；
- 弱打强；
- 碾压兑现；
- 已暴露能力后的适应反制；
- 保护 / 守点；
- 团队 / 大战局部 POV；
- 规则 / 远程条件战。

保护战 candidate 的 A/B 证明它有独特注意力价值，但 compact conditional 已能承载，因此没有 promotion 成独立 Primary。

### Shared Reference Lenses

新增 3 个**不进入 Primary Router**的跨场景研究镜头：

- `character_voice_pressure`
- `world_entry_lived_texture`
- `desire_temptation`

它们用于深化现有 Skill / Curator projection，不形成每章配额或额外 Agent。

## Runtime Decision

### 1. Deep Craft stays deep

每张 `scenes/*.md` 可以保留详细：

- Primary Reading Question
- Generation Lens
- Revision Lens
- Failure Patterns
- Stop / Handoff

这些是研究/维护层，不直接进入 Primary。

### 2. Curator gets narrow bandwidth

Catalog 只暴露：

`skill_id + Reading Question + 一行 Projection Guidance`

Curator 只有在 Mission / Canon 仍存在真实 realization 缺口时，才编译 **2–4 句** `Scene Prose Projection`；当前场景已经清楚时输出 `NONE`。

### 3. Primary no longer consumes full Scene Skill

Terra Primary 只消费 Curator 已编译的短 Projection，不读取完整 Skill、书名、source evidence 或 locator。

### 4. Reviser gets even narrower bandwidth

冻结 Primary Draft 的 Revision A/B 表明：完整 Revision Lens 常驻会让 Reviser 过度修改。

因此 production 只有两张 Scene Skill 目前开放短 `Revision Watch`：

- `social_bargain_decision`
- `relationship`

其余 **22/24 = NONE**。没有对应失败时 Reviser 完全忽略 Watch，继续 Preservation First。

## A/B Findings

### Full Deep Lens → Primary

结果是**混合**而不是单调提升。部分场景改善，但多个场景出现更长动作链、更多技术步骤或大面积重新采样。

结论：Deep Craft 有新增判断能力，但**全文直灌 Primary 是 bandwidth failure**。

### Compact Projection A/B

Luna / Sol 独立盲评共同支持：

> `Deep Research → Curator Short Projection → Primary`

可以保住真正有价值的 scene judgment，同时降低流程化和 Prompt 负担。没有发现必须让 Primary 读取完整 Scene Skill 才能稳定获得的不可替代 craft。

### Real Production Chain

最终用真实 Luna Curator + 当前 v2 Catalog + Terra Primary 跑了 10 个冻结场景。

- 5 个场景 Curator 正确生成具体 short Projection；
- 5 个场景正确输出 `NONE`；
- 覆盖 training / combat / dialogue / hunt / relationship / sacrifice / showcase / reunion / survival / chase。

这证明 `NONE` 不是理论边界，而是 production Curator 能真实执行的正常结果。

### Production Coherence Audit

最终独立审计：**PASS / Must Fix = 无**。

确认：

- 24 Primary Reading Question 无明显同义重复；
- Combat posture 没有不存在的 production variant 引用；
- Deep Craft 没有泄漏进 Primary；
- Revision Watch 只有 2 张；
- 3 个 shared references 没进 Router；
- 没有 source name / author / locator / evidence id 泄漏；
- Runtime closure 成立。

## Important Craft Upgrades

本轮新增/强化的判断包括但不限于：

- Combat：胜负尺、状态改变 exchange、信息支持的对手适应、资源/伤势必须改变动作、不同 posture 的笔墨选择与 stop。
- Dialogue：条件/信息/发言权/行动结算；群体共同承压时误判纠正后立即重排行动与资源落点。
- Relationship：关系必须改变风险/路线/边界；单方行动不能被写成双向确认。
- Exploration：行动地图、进入权与价值分离；新增可复核空间尺度 ruler，并让尺度改变一次选择。
- Chase：功能距离、追踪置信度、安全窗来源与失效点。
- Stealth：具体核验界面、凭证分层、退出权、异常顺利也是信息。
- Survival：先击穿原行动前提；资源必须重新配置行动；群体职责拓扑与承担者校准时间窗。
- Hunt / Resource / Crafting：搜索/筛选/取得分层；资源价值落到选择权；制作只展开阶段门与不可逆选择，避免工程日志。
- Recovery / Trial / Breakthrough：状态层级、资格/权利层级、阶段判定与同一 ruler；防止状态栏和流程化。
- Departure / Reunion / Identity / Sacrifice：生活基线→旧动作失灵；认出≠接纳≠重新入位；知识席位→行动权；独立意志→有限授权→不可逆转移→残余缺口。

## Production Files

核心实现：

- `.agents/skills/novel-scene-skills/SKILL.md`
- `.agents/skills/novel-scene-skills/scenes/*.md`（24）
- `.agents/skills/novel-scene-skills/references/*.md`（3）
- `src/story_mvp/scene_skills.py`
- `src/story_mvp/prompts.py`
- `tests/test_reader_first_runtime.py`

同步权威：

- `PROJECT_RULES.md`
- `docs/CHAPTER_RUNTIME_AND_STATE.md`
- `docs/NOVEL_PROSE_REALIZATION.md`
- `docs/PIPELINE_METHODOLOGY_AND_VALUES.md`
- `docs/GBRAIN_STORY_CRAFT_V3.md`
- `DEEP_CONTEXT_HANDOFF_FINAL.md`
- `.agents/skills/novel-prose-realization/SKILL.md`
- `.agents/skills/tgn-system-steward/SKILL.md`
- `.agents/skills/tgn-system-steward/references/stable-principles.md`

## Validation

- focused Scene Skill Runtime tests: PASS
- final full pytest: **310 passed**
- `git diff --check`: PASS
- `novel-scene-skills` lint: **0 error / 0 warning**
- `novel-prose-realization` lint: **0 error / 0 warning**
- `tgn-system-steward` lint: **0 error / 0 warning**
- 三个 Skill package validate: PASS
- 三个 Skill 已安装并激活为 **0.2.0**
- active `skill://` 内容已回读验证

## What This Did Not Solve

- 没有证明每一种 Scene Family 在每一本新书中都必然优于旧版；Skill 是条件化 craft，不是质量保证器。
- 不是每个 Primary 都有独立冻结 Reviser A/B，因此除 Dialogue / Relationship 外，Revision Watch 暂时关闭是刻意选择。
- 团队大战等极复杂战斗仍值得未来继续加 evidence，但现阶段证据不足以证明必须新增 production Primary。
- 一次最终“大而全 Sol architecture synthesis”运行超时，**其未完成输出没有用于 production 结论**。最终 promotion 依赖完成的 Fidelity、跨书 synthesis、Combat taxonomy judge、Luna/Sol 双盲、真实链路和 production coherence audit。

## Final Principle

> **Scene Craft 研究可以越来越深；章节 Runtime 应越来越窄。**
>
> 研究层负责学会“什么值得写”；Curator 负责决定“这一章是否真的需要”；Primary 只看最短充分投影；Reviser 只在明确失败时做局部手术。
