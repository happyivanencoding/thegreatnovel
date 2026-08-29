我将按当前 `tgn-system-steward` Skill 执行只读审计，并严格把项目证据限定在你列出的六组读取范围内；先读取该 Skill 的完整操作规程，再按清单取证，不修改任何文件。取证边界已确定。接下来运行的检查分别用于：识别并行改动与最近冻结点；定位方法论文档的开篇架构段；读取三份实验报告/审计结果；以及仅在记忆索引中确认是否有本实验的既有上下文。若发现冲突，我会以本轮指定 artifact 和当前文档为准，不扩大扫描。首轮读取确认了一个关键边界：下游 C2 已通过多条 authority 隔离，但其 Privilege 出现了“借壳”到“双躯并行”的语义变形；这不是把 isolation 误判成创意成功的理由。我正在补取被终端总输出截断的开篇架构、候选定义和最近提交，仍只读取清单内文件与已授权的 Skill/记忆索引。证据方向已经稳定：根因在 Authority 冻结前的 Premise Search 缺口；最小候选是“单次完整前提生成 → 作者选择 → 确定性拆 lane”，不是把四个高电压组件再交给一个碰撞器。最后补取三份指定报告的关键行号，用于把分数、changed-verb 和 C2 的语义漂移精确落到证据上。结论：当前 TGN 反复生成“完整但安全”的前提，最早不是 Writer 或 Story Program 的问题，而是 Authority 冻结前缺少一个“完整货架前提”的搜索层。最小候选是：

`Single-Agent Premise Forge → 作者选择 → deterministic lane compiler → 现有 World / Power / Human 分权链`

这是 `DIRECTIONAL PASS / Experimental Candidate`，不是已经替换 production 的结论。

## 三类判断

| 类型 | 当前判断 |
|---|---|
| Stable Principle | 先修最早语义/搜索坍缩；读者欲望优先；authority isolation 能防泄漏，但不会自动增加创意 |
| Current Default | `作者方向 → protagonist-blind World → Split Power/Human → Character → Story Program`，当前 production 不变 |
| Experimental Candidate | 一次生成完整 S1–S3，作者选一张，再确定性拆 lane；不增加第四 Authority |

方法论文档已经明确：现有分权链能避免旧 Fantasy Seed 的后验合理化，但当前链路没有在 World、Power、Human 生成前搜索高风险完整前提。[PIPELINE…](C:/dev/tgn-story-mvp/docs/PIPELINE_METHODOLOGY_AND_VALUES.md:7)

## 为什么会安全化

现有系统解决了旧问题：防止一个 Fantasy Seed 同时替世界、能力、Biography 和人生意义做统一解释。但代价是，搜索从多个局部 lane 开始。每个 lane 都擅长生成“合理、完整、可长期运行”的答案，却没有一个非 Canon Agent 先押注：

- 主角到底是什么非标准存在；
- 第一章必须发生什么高电压事实；
- 主角反复会做什么普通修士不会做的动作；
- 这些动作怎样改变社会关系和价格。

因此最早坍缩点是：

> `Premise Search`，发生在 Authority freeze 之前，而不是 Character Collision、Outline 或正文。

候选文档也明确指出：问题不是素材不足，而是搜索空间在 Authority 冻结前已经收窄。[PREMISE…](C:/dev/tgn-story-mvp/docs/PREMISE_APERTURE_EXPERIMENTAL_CANDIDATE.md:11)

一个真正改变动词的例子是“活脏”：主角杀死目标后移植其最强器官，身体能力和外形真实变化；这会持续产生“杀死—移植—变形”的阅读动作，而不是把“分析、维护、规划”换个职业名。[PREMISE…](C:/dev/tgn-story-mvp/docs/PREMISE_APERTURE_EXPERIMENTAL_CANDIDATE.md:94)

盲评支持搜索扩容而非下游加门禁：

- Single-Agent S pool：`85.1`
- 当前 baseline B0：`75.8`
- 四轴碰撞 C pool：`71.7`
- 预注册 S2 相对 C2：三题材合并 `+16.3`。[blind REPORT](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/blind_panel_casewise/synthesis/REPORT.md:72)

## 四个候选分别怎么判

| 候选 | 判断 | 原因 |
|---|---|---|
| Single-Agent Premise Forge | 推荐作为可选实验候选 | S pool 三题材均高于 B0；一次形成完整 Promise，避免四个局部好点子争夺主轴 |
| 四轴完整碰撞 | 拒绝加入 production | C pool `71.7` 低于 B0 `75.8`；常见失败是多核心承诺、解释负担和 Collision 后验粘合 |
| Two-Bet Voltage Budget | 仅 research-only | V `77.3` 高于 C `70.5`，修复了部分清晰度、独立性和过载，但仍低于 S `86.7`，Payoff / Long 也较弱。[voltage REPORT](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/voltage_panel_casewise/synthesis/REPORT.md:62) |
| 自动 selector | 拒绝 | 最优强度随题材变化：普通玄幻最高是 S2，快节奏和副本流最高是 S3；自动选择会夺走作者对大胆程度和商业方向的控制 |

所以，不应添加四个独立高电压 Agent。应添加的最多是一个开书阶段的完整 Premise Forge，而且必须可跳过、作者选择、不进入每章链。

## Isolation 和 composition 不是一回事

- `Authority isolation` 解决的是“谁不该知道什么”：World 不看主角和 Power，Human 不看特殊能力和未来 Story，Power 不发明 Biography。
- `Creative composition` 解决的是“整本书到底押注哪一个核心 Promise”。

四个 Agent 可以把信息隔离做得很好，却同时生成四个互相竞争的 Promise。C2 的下游审计正说明了这一点：World、Human、Interface 和隔离都通过，但 Power 把“意识进入宿主、铜像留在原地”扩成了“铜躯与宿主同时自主行动”的“双躯并行”。[C2 AUDIT](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/fast_multiworld/downstream_C2/AUDIT.md:11)

这也是为什么 `lane-safe` 不等于 `premise-safe`。

## 旧 Fantasy Seed 是否恢复

不恢复。

这不是因为当前实验直接证明旧 Fantasy Seed 分数低，而是因为它违反了当前已验证的 authority 边界：它容易把世界、能力、人物和主题提前语义统一，再由下游把统一解释伪装成自然生成。Premise Aperture 明确不是旧 Fantasy Seed 的复活版，也不生成 World / Power / Human Canon。[PREMISE…](C:/dev/tgn-story-mvp/docs/PREMISE_APERTURE_EXPERIMENTAL_CANDIDATE.md:24)

旧 Fantasy Seed 可以作为历史反例保留在研究记录里，但不应恢复为 production 路径。

## 必须继续作者门控、保持非 Canon 的内容

以下内容都不能由模型自动晋升为 Canon：

- Forge 生成的 S1–S3；
- 完整 Premise Card；
- 模型或 Judge 对候选的自动排序、自动选择；
- 未经作者确认的高电压核心、标志画面、核心新动词和第一次兑现；
- Premise Aperture 本身作为“第四 Authority”。

作者选中后，它最多成为更具体的 Author Direction；World、Power、Human 仍各自独立生成和批准，Story 只有在这些 Authority 批准后才第一次看到完整碰撞。[PREMISE…](C:/dev/tgn-story-mvp/docs/PREMISE_APERTURE_EXPERIMENTAL_CANDIDATE.md:37)

## 最小下游语义保真检查

不用新增 Reviewer、Scorer 或 Hard Gate。实验阶段做一次窄的结构化审计即可：

1. 对照 Premise 的 World、Ontology/Human、Privilege、Interface；
2. 检查第一章至前五章是否保留核心新动词、标志画面、第一次不公平兑现和社会后果；
3. 确认 World 仍 protagonist-blind、Human 没偷看 Power/Future Story、Power 没发明 Biography；
4. 检查下游有没有静默增强、削弱或替换核心边界。

C2 的结果是 `CONDITIONAL PASS`：主轴、世界、人物处境和社会后果都保留，但“双躯并行”改变了原始 Privilege。最小修复是恢复“铜像不再自主行动、只保留原位置和后果”；若保留双躯，则必须重新取得作者对“转形 C2”的明确冻结。[C2 AUDIT](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/fast_multiworld/downstream_C2/AUDIT.md:45)

## 应保持冻结的部分

- 当前 production 分权链；
- protagonist-blind World；
- Power / Human authority separation；
- Character Collision 之后的 Story Program 链；
- 旧 Fantasy Seed 不恢复；
- 不增加常驻 Reviewer / Scorer / Hard Gate；
- Premise Aperture 只作为可选开书阶段，不进入章节 Runtime。

## 这个候选没有解决什么

它没有证明某个 S 候选适合所有题材，也没有解决自动选择、下游语义漂移、正文质量、章节速度或 Runtime 质量；它还没有证明每个强 baseline 都需要 Premise Aperture，也没有证明百章后不会重复放大同一个核心动作。以上仍属于 Story Program / Outline 和后续实验问题。[PREMISE…](C:/dev/tgn-story-mvp/docs/PREMISE_APERTURE_EXPERIMENTAL_CANDIDATE.md:160)

本次为只读审计，未修改文件；现有 worktree 的未提交状态保持不变。
