# Story MVP 产品方向

> 接手项目时，建议先阅读 `docs/PIPELINE_METHODOLOGY_AND_VALUES.md`。它解释 Fantasy Seed、World Vision、Story Program、Outline、Director、Curator、Primary Writer 与 State Extraction 的职责边界、方法论和常见退化模式；本文聚焦产品方向与创意权威边界。

## 一句话产品目标

Story MVP 先帮助作者确定一部成熟中文男频成长长篇最值得让读者幻想什么，再让世界观和长期结构承载这份幻想，最后才进入 Outline 与章节 Runtime。

创作顺序固定为：

`作者粗方向 → Fantasy Seed → 作者批准 → World Vision → 作者批准 → Story Program → 作者批准 → Outline 与 Growth Genome 整理 → 100章/十章 → 章节 Runtime`

模型生成、模型选择和作者编辑都只是 draft；作者明确批准才是创意权威。批准是作者权威边界，不是文学质量评分。

## Fantasy-First 读者承诺

- 先让读者明确想拥有主角的力量、自由、寿命、身份逆转、世界位置、探索机会或命运掌控。
- 主角本人越来越能做什么，是一级成长主轴。
- 财富、装备、身份、关系、势力、领地和世界入口是二级收益，服务于下一轮一级成长。
- 普通小胜允许明显净收益；阶段大胜通常收益明显大于当前成本。
- 冲突可以包含强敌、阶层、血脉、宗门、王朝、神明、天道、战争、秘境、异族、身份暴露或作者明确选择的制度矛盾。
- 内部因果必须可信，但玄幻、仙侠、奇幻、科幻和异世界优先使用本世界力量、资源、信仰、血脉、地域、种族、宗门、王朝、神明和超凡规则制造因果。

## Supporting Logic 边界

系统必须区分“让世界可信的支撑逻辑”和“这本书真正要让读者追着看的故事发动机”。核心准则是：**Supporting Logic Must Not Automatically Become Story Engine。**

- 世界复杂性不自动成为叙事前景；
- 对手的合理理由不自动成为作者结论，更不自动变成主角长期职责；
- 世界机制真实存在，不等于需要完整展示实施过程；
- 能力可以重复使用，不等于主角自然职业化成探路、检测、维护、搬运、生产或运营者；
- 能力需要可信，不等于单独安排反复测试与验证场景。

优先让机制在真实目标、冲突和风险中被证明。观察、分析、测试、验证、调整、实施若没有新的关键选择、冲突或反转，只保留支撑因果所需的最小部分。这个原则统一处理治理化、工程化、蓝领修仙和过度验证，不为它们分别新增 Reviewer、Hard Gate 或评分器。
## 累积成长与可组合成长

可组合只表示每本书可以选择自己的成长对象、玩法和世界承载方式，不表示主动回避成熟主干。无论采用力量、战斗、神通、技艺、生命层次、规则掌控还是其它个人能力，一级成长都应持续扩大主角的行动空间。

## Growth Genome 的位置

Growth Genome 只整理已经批准的 Fantasy Seed、World Vision 和 Story Program：

- 整理一级成长、二级收益、阶段升格、主循环、反哺关系和重复风险；
- 帮助已经选定的幻想长期运行到 100 章；
- 不选择核心幻想，不决定主角欲望，不决定力量是否令人向往；
- 不要求复杂转换网络、循环族、负反馈、公开验证、资格晋升或制度化故事；
- 不进入 State Delta、Canon Memory 或 Run Ledger 的核心状态决定。

## 成本节奏

默认顺序是：胜利或突破真正发生 → 外界反应 → 主角获得实际收益 → 收益改变行动空间 → 再决定是否需要代价或余波。

成本可以限制选择、迫使策略、制造长期风险或推动阶段换挡，但不能成为每次 Payoff 的固定税。成熟不等于每次胜利立即受伤、负债、被审查或承担新责任。

## Review 的作用

十章 Review 只调整未来计划，新增检查：核心幻想是否仍在兑现、一级成长是否仍是主轴、幻想盈余是否为正、冲突是否过度理性化、世界是否被程序化。它不得自动重写或否定已完成正文。

## 章节边界

ChapterContextPacket、Director 八字段、REQUIRED_OUTLINE_FIELDS、Context Curator、Primary Writer、Specialists、Integrator、Reader-First、Canon Memory v2、State Delta v2、Run Ledger、章节保存边界和防覆盖规则保持原样。章节 Runtime 只执行已批准规划，不参与决定核心幻想。

## GBrain 与模型默认路由

当前规划链采用“高推理成本集中在高杠杆节点”的策略，而不是整链统一最强模型：

- Fantasy Seed：Luna high，GBrain OFF；
- World Vision：Luna high，GBrain ON，最多 3 条 focused inspiration；
- Story Program：Sol high，GBrain ON，最多 3 条 focused inspiration；
- Outline：Luna high，GBrain ON，通常 4 条、最多 5 条；
- Director：Luna high；Curator：Terra high；Primary Writer 暂用 Luna high，等待正文专项 A/B；State Extraction 优先更快、更便宜的模型。

GBrain 蒸馏采用不同模型分工：Terra high 做事实与 evidence，Luna high 做 Book/World/Reward/Scene synthesis，Sol high 做 Longitudinal Threads、Thread Braid 与跨书 Story Program synthesis。

同 Seed 的 GBrain OFF/ON 实测表明：ON 的主要增益集中在 Story Program 和 Outline，能更稳定地产生 Plot Engine 换挡、人物自主线、长中短线与高价值获得；当前少量 focused inspiration 已足够，不应因为有效就扩大成大上下文。

详细理由、实验边界和模型特性见 `docs/PIPELINE_METHODOLOGY_AND_VALUES.md` 与 `docs/GBRAIN_STORY_CRAFT_V3.md`。
## Experiment Boundary

独立实验用于验证 Story MVP 自身的 Fantasy Seed 偏置。实验中的具体角色、能力、世界和章节不自动升级为产品默认，也不查询或修改外部灵感系统。
