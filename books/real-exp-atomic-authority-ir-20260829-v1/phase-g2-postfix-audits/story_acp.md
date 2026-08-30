# Verdict

**架构可冻结，生产路线不可冻结。**  
Atomic Authority Contract 与 Primary Preservation Map 的拆分，已在静态层真正隔离“事实权威”和“正文保存权”；但 Native Structured Director、真实 Delta 路由、跨书最终正文、完整 fallback-adjusted 成本均未测量。Full Reviser 仍是当前生产默认，不能降为 fallback。

# Creative Ownership Boundary

拆分是对创作权的有效保护：

- Hard Contract 只接收已冻结的 Mission / Canon / World / Power / Human / Reader Release；Curator、Primary 不得创建 Fact、Conflict、Identity。
- Preservation Map 只给出事实落点、可编辑段落与窄片段保护，不能把“这段很爽/很有关系张力”升级为上游事实。
- 升级、奖励、亲密、反转、公开证明、关系转向，仍由 Story Program → Outline → Director 决定；Atomic 只检查这些已批准决定没有在最终稿中被偷换。

静态四章全部 source-pure、均可 preflight，且 Curator/Primary 未进入 Hard Source。这证明边界设计成立，不证明模型已能稳定生产这种边界。

# Edit Locality Strengths and Failure Cases

Edit Locality 比 Desire / Surprise / Relationship detector 更稳，原因不是它“更懂故事”，而是它默认**不给模型触碰正文其余部分的权限**。四个静态样本平均只开放 3.11% 段落；4/4 窗口内修改通过、4/4 窗口外修改被挡。Ch16 中 Delta 想顺手改 P71、P86、P96，均被阻止，正是它该拦的越权修辞漂移。

失败边界也必须保留：

- 若事实证据绑定错段，Locality 会精确地锁错地方。
- editable 段落本身承载爽点、关系或反转时，只有既存 exact-fragment hint 能保护；它不能理解或补造商业价值。
- 它保护“不被碰”，不证明局部替换后仍写得好，也不证明 blocker 被自然修复。
- 因此它适合做默认权限边界，不能冒充商业质量检测器。

# Why Sidecars Hurt Story

Compact Sidecar 在 authority blind 中以 **3:1** 胜出，control 在 story blind 中也以 **3:1** 胜出；这不是矛盾，而是同一 Director 的注意力被第二份语义任务挤占。

Sidecar 迫使 Director 同时做故事取舍、八字段表达、实体复制、事实分类、slot/dependency 维护和格式自检。它更容易明确“什么事实必须留下”，却把章节从“这一章最值得看什么”拉向合同摘要、执行状态与制度化结果。四样本中已经出现“已冻结结果被写成机构裁定”“迁徙窗口被扩成资源归属”等越权具体化。

更短的格式也没解决问题：verbose / compact / micro 的 Director wall 分别约增加 205.83%、147.41%、146.45%；micro 仍 0/4 可解析。这是职责冲突，不只是 token 问题。

# Native Structured Director Risks

原生 typed Director 是合理的下一假设，但仍可能变成“填表器”：

- 模型为了填满 clause / actor / action / object，把尚应留给场景的暧昧、势能与关系动作过早压成行政事实。
- `ActionSurfaceRegistry` 若变成动作菜单，会反向塑造 Director 只选择“容易编码”的故事，而非最有欲望的故事。
- 一个 canonical typed object 虽消除了双语义源，却可能把“可投影”为唯一成功标准，压缩高价值的选择、代价、反应与悬念。
- schema valid 只能证明对象合规；不能证明 Director 没有因结构负担失去章节抓力。

这些是待验证风险，不是现有失败结论；当前证据只到 schema/unit-ready。

# Commercial Value Boundary

以下内容**绝不能仅因“商业价值高”进入 Hard Contract**：

- 主角欲望的味道、贪心、面子、偏心、身体注意；
- 惊喜的节奏与揭示方式；
- 群体震动、反应强度、行文气口；
- 关系化学反应、暧昧、对白张力；
- 爽点密度、反程序感、续读拉力与文风。

例外是：上游已经明确批准为状态事实的“关系承诺/转变”“公开结果”“资源归属”等，才以其**事实本体**入 Contract；其文学实现与商业强度仍不入 Hard Contract。

# Production Readiness

**未就绪。**

已证明：source-pure 静态合同、实体/slot/conflict 规则、Locality、40 项 focused tests、20 项 schema/artifact checks，以及自由文本 Sidecar 不可用。

尚未证明：

- 真实 Director 的 native structured output 不损失故事；
- 跨书、真实 Curator → Primary → 最终正文链路；
- Normal Delta 的真实采用率与 Gate 后 blocker-only repair；
- unsupported chapter 的真实绕过；
- independent repeat；
- 包含 Delta 丢弃、Full fallback、残余修复、State 的完整关键路径成本；
- Full Reviser 被替换后的 Reader 与 Authority 结果。

所以现有证据不足以把 Full Reviser 从固定税降成 fallback。

# Freeze / Do Not Freeze

冻结：

- Contract 与 Preservation Map 的彻底分权；
- Frozen Authority 是唯一 Hard Fact 来源；
- Entity ID / stable slot 由 Runtime 掌握；
- Edit Locality 为默认保护；
- Primary 不知道 Atomic；
- Normal Delta → supported Gate → 仅暴露 blocker → Full/Residual Repair；
- unsupported 章节直接走当前 Full，且不得被不支持的 Atomic Gate 阻断；
- 禁止 free-text Sidecar、中文关键词 parser、LLM safety classifier。

不冻结：

- Native Structured Director 的生产采用；
- 自动 Entity/Fact registry 长篇覆盖；
- Atomic fast route；
- 任何“Full 可删”或加速数字；
- “schema 合法即正文合格”。

# Next Experiment

只做一个单变量实验：真实 structured-output Director 仅返回 `DirectorStructuredDecision`，Runtime 从同一对象投影八字段 Mission 与 Frozen Mission；对照当前 Director。

至少覆盖两本书、不同的力量/资源/关系事实族，并完整接回 Curator → Primary → Full Reviser。以独立重复的 Story Blind、Authority Blind、最终正文人工审读和完整 fallback-adjusted critical path 为验收；未支持的 typed family 明确 bypass。若 Structured 在故事质量不降、权威不退、且完整路径有真实收益前，绝不进入 Delta 快路，更不触动 Full Reviser。
