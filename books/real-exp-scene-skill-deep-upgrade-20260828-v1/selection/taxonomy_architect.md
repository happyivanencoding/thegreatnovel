我会按只读方式完成这次架构审计，并使用 `novel-scene-skills` 理解现行 Scene Skill 契约；同时查阅项目记忆索引，避免遗漏已定下的 TGN 权限边界。任务可拆为三块独立证据，我会并行审计：现有 Skill/Runtime、Prose DNA/Controls、小说 corpus；最终由主线程交叉验证并收敛成一套简洁可执行的 taxonomy。所有检查只服务于判断“某项应成为 Variant、Modifier 还是 Reference”，不修改任何文件。目前已确认一个关键基线：现行 v1.1 的核心原则是“按读者主要追问选一个 Primary，最多一个必要 Secondary”，而已有 A/B/C 证据只证明了短 Skill 注入有增益，并没有证明“继续增加 Skill 数量”会更好。接下来我会重点核对两件事：实际 Runtime 是否已能表达 Variant/Modifier，以及 Reviser 目前到底接收了哪些 craft 内容。这次不是单纯补一张 Scene 卡，而是在判断 taxonomy 的“最早语义坍缩点”和最小演化边界，因此我还会按 `tgn-system-steward` 的审计方法复核：重点看分类何时从“叙事发动机”退化成题材标签，以及哪一层修正最小。它不会改变只读边界。已找到 taxonomy 的最早问题：不是 Curator “不会选”，而是库的类型系统已经失真。入口文档仍把 `identity_reveal / sacrifice` 写成 Modifier，并列出 20 个 Primary；实际 production runtime 与测试却把 `identity_reveal / departure_vacancy / sacrifice_convergence / reunion_reentry` 当成 24 个平级 Primary。与此同时，Utility/Modifier 只有文字说明，没有可执行加载与解析；`combat(mode=war)` 也没有 Runtime 参数通道。所以下一步应先修“类型与投影结构”，而不是继续往平面 ID 列表加卡。架构已经基本收敛：保留现有“按主要阅读问题选发动机”的正确核心；取消含混的 `Secondary` 叠加语义，改为“同场 Variant/Modifier”或“明确状态锚点后的 Handoff”。Combat 只按信息拓扑拆：默认单局对抗、小队协同、局部战场；不按兵器、Boss、比赛、伏击、复仇等题材名继续拆。最后我正在等三份并行审计回传，主要用于反证是否还有第二个 family 达到 Variant 准入线。## 结论

建议冻结现有 Scene Core，不扩大平面 Skill 数量；下一版采用：

> 共享 Core + 24 个明确 Primary + Combat 的少量 PILOT Variant + 横切 Modifier + 边界 Utility + 派生 Revision Lens。

最早的问题在 taxonomy/runtime：入口文档仍列 20 个 Primary，并把 `identity_reveal / sacrifice` 归为 Modifier；production 实际已加载 24 个平级 Primary。[SKILL.md](/C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/SKILL.md:17) 与 [scene_skills.py](/C:/dev/tgn-story-mvp/src/story_mvp/scene_skills.py:13) 已漂移。Utility、Modifier 和 `combat(mode=war)` 目前也没有可执行解析通道。

## 五层分工

| 层 | 职责 | Runtime 规则 |
|---|---|---|
| Core | 全库共享的动作→响应→状态变化、承重细节、结果停点 | 只注入一次，不可选择 |
| Primary Skill | 定义本场主要阅读问题、状态变量和发动机 | 每个 Route 恰好一个 |
| Variant | 阅读问题不变，但状态拓扑和下一拍生成逻辑实质不同 | 仅少数 family 可选，默认无 |
| Modifier | 改变公开性、压力、情绪或 payoff，不改变发动机 | 最多一个；如 `public_proof / competition / urgency / reversal` |
| Utility | 处理进入、过渡、余波、兑现、仪式、转移 | 只挂在 Route 边缘，不与 Primary 竞争 |
| Revision Lens | 检查既有稿件是否出现特定失败，并规定最小修复 | 不由 Curator另选；由已选 craft 确定性派生给 Reviser |

`identity_reveal / departure_vacancy / sacrifice_convergence / reunion_reentry` 应继续作为 Primary，不降为 relationship Variant。跨书证据证明它们分别处理重新分类、空位换挡、牺牲合流和重新入场，阅读问题确实不同。[cross-scene-synthesis](</C:/GoogleDrive/笔记/卡片盒子/20_Knowledge/修仙小说素材库/reference-corpus/operations/gbrain-story-craft-v3/pilot/cross-scene-synthesis.md:14>)

## Combat 为什么值得拆

当前 [combat.md](/C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/combat.md:3) 一张卡同时容纳单挑、小队协同和战争局部 POV。三者的胜负问题相同，但信息拓扑不同，因此 Combat 是目前唯一有强理由获得 Variant 分辨率的 family。

建议拆到这里停止：

- `combat` 默认 Core：局部双方围绕目标交换主动权。
- `team_coordination`，PILOT：角色分工、局部视野、救援/干扰会改变队友下一步可做之事。
- `battlefield_local`，PILOT：通信延迟、多战线和局部行动必须共同承载整体战局。

其余不拆：

- 预判、备用手段、短暂反击窗口：Combat Core。
- 能量/时间窗口：Core 状态变量，必要时加 `urgency`。
- 公开证明、身份重新估价：Modifier。
- 追逐、潜入、生存：已有独立 Primary。
- Boss、比赛、伏击、守城、复仇、兵器和境界：题材或目标条件，不是 Variant。
- 规则破解若成为主要追问，应切换或交接到 `deduction_reveal / comprehension_insight`，不造 `puzzle_combat`。

现有 A/B 也支持这种克制：空间因果控制在复杂行动中有增益，却在简单一对一中明显负收益；因此不能升级为所有 Combat 默认规则。[GBRAIN_PROSE_CRAFT_V1.md](/C:/dev/tgn-story-mvp/docs/GBRAIN_PROSE_CRAFT_V1.md:217)

## Skill 文档稳定字段

每份生产 Skill 统一保留：

1. `ID / Kind / Family / Maturity`
2. `Primary Reading Question`
3. `Use When / Do Not Use When`
4. `State Vector / Reader-visible Success`
5. `Beat Engine`
6. `Expand / Compress`
7. `Stop / Handoff`
8. `Revision Lens`
   - Failure signals
   - Minimum repair
   - Preserve
9. `Evidence / Transfer Boundary`——仅研究视图读取

同一文档生成三种投影：

- Router：Question、Use/Do Not Use、Variant switch cue。
- Terra Primary：Core + Beat Engine + Expand/Compress + Stop；只加已选 Variant/Modifier 的差量。
- Luna Reviser：Reader-visible Success + Failure signals + Minimum repair + Preserve；不含 Beat Engine、完整 Guidance、原著证据或研究解释。

## Reviser 输入

当前 [build_authority_reviser_context](/C:/dev/tgn-story-mvp/src/story_mvp/hybrid_runtime.py:649) 会把整份 Curator 原样交给 Reviser；因此真实 Curator 输出中的 Skill 标签、Opening Strategy、Inspiration 等都会再次出现。[prompts.py](/C:/dev/tgn-story-mvp/src/story_mvp/prompts.py:2039)

建议确定性拆成：

```text
安全 Authority
冻结 Chapter Mission
Curator Authority Projection
Reader Release
Frozen Power / Human
Canon Index / Tail
Selected Craft Revision Lens
Primary Draft
```

`Selected Craft Revision Lens` 只回答：

```text
本场应让什么变得可读？
底稿出现什么具体失败才允许改？
最小修复跨度是什么？
哪些正确内容必须保留？
何时停止修改？
```

完整研究卡、Writer Beat Engine、未选择 Variant、source locator 都不进入 Reviser。这样 Luna 是校正者，不会收到第二套正文生成指令。

## Selection Router

直接淘汰含混的 `Primary / Secondary` 双行协议，不保留兼容层。`Secondary` 当前混合了“同时叠加”和“后续换场”两种语义。

改为 question-first：

```text
Question: 杜衡逼近后，哪个动作会重新分配主动权？
Route: combat + public_proof
Handoff: 胜负成立后 -> identity_reveal
```

规则：

- 先用自然语言写主要阅读问题，再选 Primary。
- 同场差异用 Variant/Modifier。
- 第二个发动机只有在 Mission 已存在明确状态锚点时才写为 `Handoff`。
- 最多两个 Route；不要求把每个字段填满。
- Variant 选择若需要评分表或大量标签才能解释，说明候选尚不适合 production。
- Curator 只看紧凑目录；Primary 和 Reviser 均不看全库。

## 不值得拆的 family

- Relationship 不按爱情、亲情、师徒、友情拆。
- Bargain/Resource 不按拍卖、朝堂、宗门、商会拆。
- Exploration/Hunt 不按秘境、城市、荒野、遗迹拆。
- Training/Crafting/Breakthrough 不按功法、职业、材料、等级拆。
- Trial/Showcase 不按比赛、考核、排名拆。
- Horror/Comedy 不按怪物类型或笑点类型拆。
- Entry、Travel、Aftermath、Payoff、Ritual 永远保持 Utility。

## A/B 准入

采用两轮近单变量实验：

1. `Core` 对 `Core + 完整候选`
   - 若不能稳定改善主要阅读问题、动作响应和状态变化，留 Reference。
2. `Core + compact Modifier` 对 `Core + Variant`
   - Modifier 已能取得同等增益：定为 Modifier。
   - 只有完整 Variant 能稳定改变 beat loop，且跨不同场景仍有效：升 Production Variant。
   - 若候选改变了主要阅读问题：它应是 Primary，而不是 Variant。

盲读真实文本，重点判断具体变化、事实越权、模板化和无必要扩写，不用综合评分表代替判断。Reviser Lens 另做 `Authority-only` 对 `Authority + Lens`：只有提高目标修复、同时不增加无谓改写，才进入 production。

实施顺序应是：先统一 typed manifest 与文档事实源；再增加三种投影 renderer；直接移除 Secondary；最后只对两个 Combat PILOT Variant 做 A/B。此次只读研究未修改任何文件。
