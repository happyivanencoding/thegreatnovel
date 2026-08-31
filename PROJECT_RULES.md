# TheGreatNovel 项目总执行规则

> 本文件是 TGN 项目执行规则的**唯一长期权威**。ChatGPT Project Prompt 只保留本文件路径与“每次 TGN 任务先读取并遵守”的入口指令，不再复制整份规则。

## 1. 权威与维护

- 本轮用户明确要求 > 当前 production code / tests / runtime > 本文件 > current docs > 历史实验。
- 本文件只保存**当前规则**，过时内容直接替换，不累积历史说明。
- 当架构、阶段职责、默认模型/GBrain 路由、审批流、Git/ACP/GBrain 工具边界、审计协议或 docs 权威发生稳定变化时，必须在同一任务更新本文件。
- 单次实验、单个 candidate、临时模型比较或不改变行为的内部重构，不更新本文件。

## 2. Repo / Git / ACP

- Repo：`C:\dev\tgn-story-mvp`
- 唯一开发分支：`principal_dev_new_sys`
- 普通代码、Prompt、测试、文件、Git 任务由当前 ChatGPT 直接完成，不为方便调用 ACP。
- 有效修改后测试、提交并推送；不碰无关 untracked 实验文件。
- **`principal_dev_new_sys` 是内部开发权威；`main` 是 public production freeze，不承载内部方法论。** 向 `main` 发布时不得 fast-forward / merge 整条 dev 历史；必须以当前 `origin/main` 为父节点构造 clean release commit，只同步已冻结 production code、必要 runtime skill、构建配置与可公开测试。`docs/`、`DEEP_CONTEXT_HANDOFF*`、`PROJECT_RULES.md`、`tgn-system-steward`、`temps/`、`CURRENT_NOVEL_FOR_REVIEW.txt` 和新内部实验 provenance 不得进入 main；必要 runtime Scene Skill 可保留。main release 前做敏感路径树检查、独立测试并打 freeze tag。
- 所有 TGN commit 的 Author / Committer 固定为 `happyivanencoding <jingxuan.ivan@gmail.com>`；不得使用 Codex、Agent 或本地占位身份。提交前若仓库 Git identity 不一致，先修正再提交。
- 只有真实 LLM / Coding Agent 执行才调用 ACP，例如小说生成、模型 A/B、正文质量实验、GBrain 原著蒸馏或跨书 synthesis。
- ACP：`C:\Users\jingx\AppData\Roaming\npm\codex-acp.ps1`；ChatGPT 登录，不使用 API Key；默认 read-only。
- ACP 访问 GBrain：TGN 为主工作目录 + `additionalDirectories(GBrain root)`；不复制原著，不默认 full access。
- ACP 失败不切换认证方式；无法继续时给出可直接交给 Codex 的完整 Prompt。

## 3. 系统审计协议

当用户说“审计 / 系统审计 / 审计一下”时：

1. 自动使用当前激活的 `tgn-system-steward` 做一次**独立审计**；
2. 当前 ChatGPT 同时独立复核实际 code / docs / artifact；
3. 审计区分 Stable Principle / Current Default / Experimental Hypothesis，不把当前实现伪装成永恒原则；
4. 最终只输出两者综合后的结论；若有实质分歧，明确列出分歧与证据；
5. 审计默认只读；用户明确要求修复/执行时，才在统一诊断后实施最小根因修复；
6. Steward 不进入小说 production pipeline，不成为常驻 Reviewer / Gate。

### 什么时候更新 Steward

只在**审计方法本身**发生稳定变化时更新，例如：Stable Principle、root-cause layering、source hierarchy、authority 判断、因果 A/B 方法、GBrain governance/retrieval 审计方法、repo safety，或跨样本确认的新系统性模型偏置。

不要因为 production 新增/删除阶段、模型/价格/GBrain 条数变化、单次实验、字段名/UI/局部 Prompt 修改而更新 Steward；这些由 live discovery 获取。

更新流程：递增版本 → `skill-authoring` lint → package validate → install/activate → bounded read-only smoke audit → PASS 后提交推送。

## 4. 当前 Production 创意链

`作者方向 →（可选）Non-Canon Premise Forge S1/S2/S3 → Independent Premise Authority Compiler → 作者选择并批准 / 显式跳过 → protagonist-blind World Vision → POWER_BASELINE / LIFE_CONTEXT → 独立 Power Seed + Human Seed → 作者一次批准 Character → deterministic CHARACTER.md → Story Program（第一次完整 Collision）→ 作者批准 → Outline / Future-10 → Full Deterministic 4—6章 Authority Packet（默认5）→ Terra Batch Primary → Sol Batch Authority Delta → 整批采用 → State Extraction逐章落盘`

长篇到达真实 `World Horizon` 后使用低频 forward loop：`Story Program Handoff → protagonist-blind World Expansion →（仅长期证据足够时）Human Development → deterministic CURRENT_CHARACTER.md → Sol Story Refresh / Re-Collision → 作者批准刷新后的 Story Program → Outline → 后续章节`。开书 World / Power / Human 是稳定 Origin，不要求一次写完 500 章所有具体世界与能力。

长期 Mystery 允许使用低频 **Progressive Canonization / 渐进定真**：`AUTHOR OPEN → Mystery Decision Surface → DEFER / DECISION NEEDED → Non-Canon Reframe R1/R2/R3/D0 → 作者选择 → Independent Mystery Compiler → AUTHOR FIXED HIDDEN → Story/World Planning → reader-facing Reveal Event → State/Canon → 更深 AUTHOR OPEN`。触发条件不是章节数、伏笔年龄或“大纲应该完整”，而是**作者已批准的下一段具体故事需求已经无法在不决定某一小层答案的情况下成立**；还能继续写好故事就必须允许 `DEFER`。

- **没有 production Fantasy Seed。** Premise Aperture 是可丢弃的 Non-Canon 搜索与编译阶段，不是第四 Authority。
- Premise 从未开始或作者显式跳过时，原 Split Authority 路径保持可用；一旦保存候选，World / Power / Human / Story 的生成、保存与批准必须等待 strict `PASS` + 作者批准，不能静默绕过。Compiler Input 必须在 Prompt 生成当下落盘，报告保存不能重绑到后来编辑的文本；snapshot 与当前 selected card 不一致时必须重新编译。World Vision 一旦批准，Premise 决定冻结。
- Forge 一次生成 S1/S2/S3，不自动排名或选择；Independent Compiler 只审 trigger、载体、T0 尺位、Interface 因果与远期复合，不评分、不改稿、不偏向保守。`CONDITIONAL PASS / FAIL` 返回作者；没有自动 selector 或 Repair Loop。
- 作者批准后由代码确定性拆成 World / Power / Human / Story 四条 lane contract；Story Program 第一次读取完整 Promise，Outline 与章节 Runtime 不再读取 raw Premise Card。无法同时成立时必须 fail loud `PREMISE-AUTHORITY CONFLICT`。
- **没有 Character Composer LLM。** Power/Human 不做后验主题化调和。
- 批准点保持紧凑：（可选）Premise → World Vision → Character（Power + Human 一次批准）→ Story Program。
- Forward Authority 仍需显式采用：World Expansion 候选只有作者批准后生效；Human Development 可返回 `NONE`，只有作者批准的真实 Delta 才进入长期人物权威；Story Refresh 复用 Story Program 的现有保存/批准流程。模型生成不自动成为 Authority。
- **作者未知本身是合法状态**：`AUTHOR OPEN` 表示作者当前也没有答案，不是待模型补齐的缺陷；`AUTHOR FIXED HIDDEN` 才表示作者已决定、但读者/人物尚未知。Decision Surface 不给答案；Reframe 不自动选择；Compiler 只允许回答当次 `Smallest Decision`，候选自己的 `What Remains Unknown` 成为新的保护边界。Compiler FAIL 返回作者，没有自动 Repair Loop。
- Mystery Compiler Prompt 生成时必须把**当前 Thread + selected candidate + Decision Surface + author planning need + 当前 BOOK/Canon 原文**作为 exact input snapshot 落进 `MYSTERY_CONTROL.json`；`adopt` 只接受与 snapshot 完全一致且 strict `PASS` 的候选。候选、Thread 或 BOOK/Canon 任一变化，旧 Compiler Report 立即 stale，必须重新编译；不使用 hash 代替直接文本比较。API 不能直接 PUT `FIXED_HIDDEN` 绕过 Compiler + adopt。
- Hidden Fixed Point 固定保存在 runtime-blind `MYSTERY_CONTROL.json`，不得进入 BOOK / AUTHOR NOTES / 普通 Outline / Reveal 前章节。对应 `story` / `world` route 只在 Story Refresh / World Expansion planning 层可见；Story Refresh 若安排本轮 Reveal，只把 `Reveal Boundary` 编译成 reader-facing `MYSTERY REVEAL CONTRACT`。保存 Story Program 时 Contract 被确定性剥离并单独保存；Outline 只得到 `第N章 + [MYSTERY-REVEAL:ID]` 的无答案调度标记；只有 Reveal 章才确定性注入 Event Atom / State Residue / Still Open，raw Fixed Point 永不进入 Writer。
- Reveal 必须通过动作、物证、环境变化或人物可验证观察成为 Reader Fact；State 才把这一层写成 Canon。Reveal 后显式 advance 将该 Mystery 重新打开为更深 `AUTHOR OPEN`，允许以后再次局部定真或长期继续 `DEFER`。不新增每章 Mystery Agent / Reviewer / Gate，也不要求所有 Open Promise 使用这套机制。

## 5. 默认模型与 GBrain 路由

| 阶段 | 默认模型 | Reasoning | GBrain |
|---|---|---:|---|
| Premise Forge（可选开书） | GPT-5.6 Luna | high | **OFF**；一次生成 S1/S2/S3，Non-Canon |
| Premise Authority Compiler | GPT-5.6 Terra | high | **OFF**；fresh context，只审可满足性，不评分/选择/修稿 |
| World Vision | GPT-5.6 Luna | high | ON：固定 1 条 Reader Coordinates Reference + 最多 3 条 creative inspiration |
| World Expansion | GPT-5.6 Luna | high | ON：World-only craft + Coordinate Reference；protagonist-blind |
| Power Seed | GPT-5.6 Luna | high | ON：固定 1 条 Naming Craft Reference + Power lane 小 bundle |
| Human Seed | GPT-5.6 Luna | high | ON：Appetite / Behavior / Relationship 各最多 1 条，总计最多 3 条 |
| Human Development | GPT-5.6 Luna | high | **OFF**；低频，只看 Frozen Human + 已发生 Canon，可 `NONE` |
| Current Character | deterministic | — | OFF；不调用 LLM |
| Mystery Decision Surface（低频） | GPT-5.6 Luna | high | **OFF**；只判断 DEFER / 最小必须定真层，不给答案 |
| Mystery Reframe Forge（低频） | GPT-5.6 Luna | high | **OFF**；R1/R2/R3/D0，Non-Canon，不自动选择 |
| Mystery Canonization Compiler（低频） | GPT-5.6 Terra | high | **OFF**；只审局部兼容性/Still-Open，不评分、不修稿 |
| Story Program | **GPT-5.6 Sol** | high | ON：最多 3 条 focused inspiration |
| Story Refresh | **GPT-5.6 Sol** | high | ON：最多 3 条 focused inspiration；Effective World × Current Character；如有 AUTHOR FIXED HIDDEN 可 planning-only 编译 Reveal Contract |
| Outline | GPT-5.6 Luna | high | ON：通常 4 条、最多 5 条 |
| Batch Packet | deterministic | — | OFF；直接抽取 Approved Future-10 当前4—6章（默认5），并复用现有 Chapter Context compiler 叠加 Frozen Power/Human、safe World、Reader Release、Protected RSE、Book Contract、BOOK Prose Profile、starting Canon 与 active Long Block；不调用 LLM 重规划 |
| Batch Primary Writer | **GPT-5.6 Terra** | high | raw GBrain OFF；Frozen Power/Human + safe World/Reader Release + Approved Future-10；一次写完整 Batch |
| Batch Authority Delta | **GPT-5.6 Sol** | **high** | raw GBrain OFF；完整 Batch + safe Authority；只输出 exact local patch / upstream conflicts，不输出全文 |
| State Extraction | GPT-5.6 Luna | low | OFF；整批 prose final 后逐章落盘 |
| 单章 Director / Curator / Full Reviser | GPT-5.6 Luna | high | raw GBrain OFF；仅兼容 fallback / 专项实验，不是默认 Batch 链 |

默认章节链：`Approved Future-10 → Full Deterministic Authority Packet → Terra high Batch Primary → Sol high Batch Authority Delta → 整批采用 → Luna low State 逐章落盘`，默认 5 章、支持 4—6 章。**Batch 中途不更新 State / Canon**：Primary 先连续完成整批，Reviser 再一次看到整批与远端 Authority，避免“第1章修订后第2—5章预写稿全部 stale”。Reviser 只返回 exact `OLD→NEW` Delta；同一事实域冲突必须跨章扫清。若修复需要新增传送/追踪、世界机制、重大胜负、奖励或身份，返回 `upstream_conflicts`，整批不得采用，回 Story / Outline 修最早根因。单章 `curator_primary` 的 Luna Director → Luna Curator → Terra Primary → Luna Full Reviser → State 保留为 fallback；其一次 Outcome/RSE repair 规则继续只作用于这条 fallback。

- **Run Ledger Exact-Input Receipt**：依赖变化仍先按现有规则把未来节点标 `stale`；节点重新构建 Prompt 后，只有当 exact UTF-8 `prompt_sha256` 与已保存 Response 绑定的 Prompt digest 完全一致，且 Response 文件自身 SHA-256 仍与 receipt 一致时，才确定性恢复 `completed / adopted` 并跳过模型调用。Prompt 有任一字符变化、Response 被改、旧 manifest 没有 receipt、或作者显式 `retry` 时都不得复用。该机制只减少上游编辑后的无效增量重跑，不宣称降低首次章节生成 wall；不用 semantic hash，不建立通用 cache 框架。

低延迟优化优先做确定性上下文裁剪与失败恢复。2026-08-29 两轮实验已否决 Curator medium/Slim、Reviser medium/Patch-only/Safe route、Conditional/Speculative Director、Parallel Pre-Curator、Authority Blueprint、Attention Kernel 与 Reviser+State 合并作为质量等价 production 默认；任何模型、effort、输出合同、局部 Delta、提前编译或跨章投机只能显式 A/B，必须接回完整 downstream，同时报告 Reader + Authority、完整 critical path、独立 repeat、cross-book 与 fallback/丢弃成本后才可采用。本轮明确不修改 ACP runner 与前端。 Atomic 最终架构固定分成 `Atomic Authority Contract` 与 `Primary Preservation Map`：Hard Contract 只接受 Entity Registry + Frozen Mission / Canon / World / Power / Human / Reader Release 的可信结构化 artifact，Curator / Primary 只能提供 Runtime签发的 realization location、edit locality 与窄 protection hint，不能创建 Hard Fact、Source Conflict 或 Entity Identity。所有主体、物件、资源、力量与关系使用稳定 Entity ID / slot；不支持的章节直接走当前 Full Reviser，且同一不支持的 Gate 不得反向阻断 Full。禁止继续扩中文关键词 parser、禁止自由文本 Sidecar、禁止新增 LLM safety classifier。2026-08-30 的两书四章真实E2E先否决“当前 Native Structured Director 直接替代丰富 human Mission”：v2虽8/8 Native accepted且手工fixture结构覆盖100%，但Mission Story / Authority与Final Authority均退化，完整Final Draft慢7.86%。随后又冻结测试 `rich free-text Director → Primary → deterministic Atomic bypass Gate → PASS跳Full / FAIL回Full`：2次fresh共8章，4次supported但**0次PASS**，实际2457.403s→2457.424s，节省0%；更关键的是对7组“Oracle看似可直出”的Primary/Reviser做两轮匿名复核，Story共14票中Reviser 10胜、Primary 4胜，Authority为Reviser 8胜、Primary 1胜、5平，**0/7**稳定同时满足Story不降且无Primary Authority hard problem。结论：`Atomic Authority closure ≠ Reviser necessity`；该实验说明单章 Full Reviser 当时是 value-bearing stage，不能只因 Authority Gate PASS 就跳过。2026-08-31 的 Batch 实验没有绕过 Reviser，而是把它改成**整批可见、exact local Delta**：跨书 held-out 证明小说感与 Authority 可以同时优于逐章链；typed Contract 仍只作后台 Authority/repair 研究。禁止靠扩中文regex/parser或新增LLM safety classifier追求skip；只有先让Primary在真实pair中稳定达到Reviser后的Story + Authority水平、使Reviser趋近no-op，才重新测试bypass。随后用两部**全新held-out小说**连续前4章验证“把Reviser能力前移到Primary”：5行self-check虽略降Hard问题，却让Reviser Authority增益更大；确定性Final Facts Projection能明显提高Story，但Authority Hard问题反而增加，且两方案均0/8 Reviser exact no-op。进一步只在derivation样本测试 `Final Facts Projection + Luna-medium Reviser`：Reviser wall约133.3s→59.6s、Story守住，但Authority 57.5 vs high 61.875、Hard问题9 vs3，因此按预设规则淘汰。冻结新方法论：**no-op/降档候选必须在Treatment冻结后用新小说held-out验证，并直接比较Primary→Reviser的Story/Authority gap、Hard问题、edit blocks/exact no-op与完整wall；Story attention增益不能替代Authority closure，速度screen若Authority仍弱于high不得为追速度进入新held-out或Production。**

模型判断必须分开看：`生成质量 ≠ wall-clock ≠ 实际成本`。Luna 单价最低；Terra 通常最快且更克制；Sol 最贵且通常最慢。当前 Sol 默认用于 Story Program / Story Refresh 与 **Batch Authority Delta**；Max / Ultra 只有真实 Authority closure 相对 high 有补偿性增益时才可采用，不能按档位名自动升级。

## 6. GBrain

GBrain 根目录：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库`

- GBrain 是 Optional Inspiration，不是 Canon、创意权威、Hard Gate 或原作模板。
- **公共治理、资源分配、维护职责、责任升级不得作为 production GBrain 的通用可迁移创作机制**；来源作品确有此内容时只保留为研究证据，并退出 active inspiration。
- 主要路径：`GBrain → World / World Expansion / Power / Human / Story Program / Story Refresh / Outline → Approved Story`；以及 `GBrain 离线深蒸馏 → source-blind 固定 Reference / Scene Deep Craft → 对应规划层或 Curator/Reviser 的窄带宽输入`。当前 World/World Expansion 固定读 Reader Coordinates，Power 固定读 1 条由经典跨书蒸馏得到的 Naming Craft Reference；Human Development 固定 GBrain OFF。World Expansion 的 retrieval 同样必须 protagonist-blind，不能通过 BOOK/Character/Story 间接泄漏主角形状。
- raw GBrain / Reference Program 在 Hybrid Chapter Runtime 的 Prompt 真源处 fail closed；即使旧调用方误传，也不得进入 Curator、Primary、Authority Reviser 或 Specialist。章节只消费已批准上游、safe Authority 与 source-blind Scene Skill。
- 蒸馏分工：Terra 看清事实/Fidelity；Luna 理解吸引力与中层 craft；Sol 理解长篇结构。
- Windows / Git Bash 使用 `~/.bun/bin/gbrain.exe`；新增、修改或删除页面后执行 `embed --stale`；交付前必须 `Embedded == Chunks`。
- 排障顺序：executable/path → environment/API key → stats → PGLite lock → process cleanup；不要先杀 `bun.exe`。

## 7. 系统级创作原则

始终遵守：

> **支撑性逻辑不得自动成为故事发动机。**
>
> **主角永远不是协调员。**

即：世界复杂度 ≠ 叙事焦点；对手有理由 ≠ 作品认同 ≠ 主角义务；机制真实 ≠ 展开实施细节；能力 ≠ 职业；可以验证 ≠ 验证过程就是故事。主角可以命令、拒绝、抢夺、交易、保护、结盟和作决定，但不得把聪明/成熟/负责写成替多方协调利益、分配责任、优化公共资源、安排所有人位置或替世界收拾残局；公共资源冲突只保留改变大局的关键选择与直接后果，其余实施由各方按自己的欲望继续处理。

同时：

- 修最早发生语义坍缩的节点；少深层规则 > 多 Hard Gate。
- Human：**经历是背景，不是人格证明**；允许多重动机、稳定选择偏向与现场变化。候选期现有 `Audition Metadata / 人物钩子` 固定用一次短 **Action Audition** 检验“这个人有没有戏”：只使用候选已成立的动机/关系，在与未来 Power/主线无关的小现场里让至少两项私人价值相撞，人物必须做出可见选择并留下一个真实小代价；不解释人格、不新增过去/未来事实、不把这次做法固化成固定招式。Audition 全部 Non-Canon，作者选定后继续由现有 parser 与 Human Core / Initial State 分离。冻结 Human Core 高于最近几章的“负责/克制/救人”等行为归纳；下游不得把局部正确选择反推成新的道德人格。人物长期允许真实发展，但只能通过低频 `Human Development Delta` 基于已发生长期历史 forward-only 更新，且允许 `NONE`；该阶段看不到未来 World/Story。章节期仍从 `CHARACTER.md` 确定性投影 Frozen Human Core：默认 Batch Packet 直接携带；单章 fallback 才交给 Curator，Curator 不重复 Power Core。当前场景自然触发已批准的虚荣、钱、审美、身体吸引、享受、好奇、偏心等私人牵引时，应让它真实影响注意力、靠近/回避或选择，不统一净化成职责协作与成熟沟通。若 Frozen Human 已明确某个具体人会改变选择，而本章正发生近身照料、重逢、分别、私密靠近、嫉妒或邀请等关系现场，默认属于自然触发，保留一个克制 cue 即可，不要求改写主事件。
- **Human Occupational Trait Ceiling**：除非作者明确选择职业/制度/经营题材，责任、精确、审计、边界、路线、损失归因、职业伦理等只能是低权重局部习惯，不能成为 Human 最强牵引、Story Program 多阶段主题或反复解题语法；私人欲望、胜负、钱、审美、身体吸引、享受、面子、自由、野心、报复、偏心与具体关系优先拥有前景。**Character relevance ≠ Story Engine authorization。**
- **Major Reward Anchor / Big Direction First**：世界若天然充满粮道、水源、迁徙、矿权、治理或其它 supporting conflict，Story Program / Outline 仍先锁定当前大型阶段真正让主角和读者想追的少数具体对象/结果——想拿什么、赢谁、进哪里、变成什么、和谁靠近/对抗、哪个 Mystery 非看不可——并尽早说明为什么值、谁也想要。奖励方向提前锁，但兑现强度不预先克制；大胜只要因果成立，可同时得到主奖励 + 钱/资源 + 名声/招揽/入口 + Bonus Surprise。公共资源协调只留改变大局的方向选择与直接后果，不拆成连续小戏。
- **Post-Primary Authority Recovery 必须 Preservation-First，不做第二次创作**：默认 Batch 中由 Sol-high 一次读取完整 4—6 章 Primary + Future-10 + Frozen Power/Human + safe `WORLD AUTHORITY` + `Reader Release` + Protected RSE + Book Contract + starting Canon，只返回 exact local Delta；未触碰正文逐字保留。同一事实域出现冲突时必须跨章扫清所有依赖位置。若修复需要新增传送/追踪、世界机制、重大胜负、奖励或身份，必须返回 `upstream_conflicts`，整批不得采用，回 Story / Outline 修最早根因。单章 fallback 的 Full Authority Reviser 继续使用原 Preservation-First 规则。两条路径都不得把远端欲望/可能性升级成事实，也不得把“重新接触 / 合并”等条件扩成远程召回或跨距离回收。raw GBrain 固定 OFF。
- **Chapter Plan Authority 不允许跨章偷跑、静默丢结果或删除即时因果**：Future 10 的当前章条目由 runtime 确定性拆成 `本章唯一可执行事件预算` 与 `章末 Handoff Reservation`；Long Block 只作阶段背景，不能授权 Director 把下一章付款、身份、获得、升级或其它结算提前完成。反向同样成立：上一章正式正文若结束在对手堵路/拔刀、追杀未停、攻击已落下、人物正坠落/被困、门正在关闭或必须当场回应的交易/选择等**即时未解局面**，该事实自动成为下一章的 continuity debt；Outline / Review 的下一章 `具体剧情` 必须从它继续或明确桥接，Director 也必须先用最低充分动作让它结束、被打断或转化，不能直接跳成次日、另一地点或“已经进城”。桥接必须至少写出一个可落正文的具体动作因果，不能用“趁乱脱身 / 成功进入 / 摆脱追兵 / 冲突结束”代替；它不授权新增重大胜负、奖励、关系翻转或资源结果；若 Plan 与 Canon 真冲突，仍用现有 `[PLAN OUTCOME ADJUSTMENT]` 最小处理。Runtime 只保留文本自身明确覆盖当前章的 Long Block；显式范围已经过期时直接丢弃，找不到合法块也不得回退整份旧长纲。当前章已批准的 `结果 / 状态变化` 同时确定性并入 Frozen Mission 的 `状态变化`，Director 静默省略不构成取消；Canon 真冲突时仍以已发生 Canon 为准。已批准的力量/身份跨档进入 Frozen Mission 后，不能只用“打出该级战绩 / 接近 / 获得资格”替代。若已发生 Canon 真使原结果不可能，Director 只能用 `[PLAN OUTCOME ADJUSTMENT]` 显式记录最小调整。若最终 Authority Revision 仍漏掉这种**显式里程碑**，Run Ledger 只允许同一 Reviser 一次 Preservation-First Outcome Repair retry；retry 只补最小因果与一次直称，不改事件、胜负、资源、伤势、关系、Ending 或未知边界；第二次仍失败就停止，不形成自重试循环。
- **Access Provenance 跨章节仍是因果债务**：如果前文已经明确某扇门/桥/世界裂口/封锁关闭、拒绝或把某人物留在另一侧，而后两三章又要求该人物出现在边界另一侧，Story / Outline 必须在再次出现前给出已有 Authority 支持的到达因果，或把它明确保留为可见 Mystery；不能因为不是相邻章节就无解释瞬移。Director / Reviser 不得为补洞自行发明第二扇门、剑意追踪、秘密接引、远程召回等新机制；上游没授权时必须返回最早规划层。
- **Premise Identity 要在第一自然 Horizon 结束前至少完整兑现一次**：若本书真正卖点是“跨世界带走并复合世界可能性 / 永久保存极限 / 吞并规则”等区别于普通掉宝的长期动作，第一世界/第一自然阶段结束前应让读者亲眼看见这项区别本身成立一次；钱、宝物、地图、资格可以一起爽，但不能一直替代核心操作。第一次不要求解释最终上限，也不让 NPC 偷知隐藏机制。
- **强世界规则必须至少改变一条人物生活因果，不只服务玩法**：如果一个世界最独特的规则只用于战斗解题、追逐机关或赌局漏洞，长期会退化成换皮关卡。World / Story 至少让一个具体人物欲望、关系、身份或命运只有在这条规则存在时才成立；不因此强行哲学化、制度化或写百科。
- **Trait Saturation**：稳定人格是选择偏向，不是固定口癖。爱钱、好胜、嘴硬等已经通过少量高记忆点选择/台词成立后，后续只有它真的改变新选择时才再次前景化；不持续用“值多少钱 / 这才叫买卖 / 我不喜欢亏”等同义句提醒读者。允许 Frozen Human 里其它真实牵引、具体关系、面子、冲动、审美、身体反应与不够理性的偏爱自然进入现场。
- **Reader-Facing Story Event ≠ State；Authority Fact ≠ Backstage Wording**：Story Program 只在确有必要时列 0—4 个 `RSE-xx`，保护“若被压成 State / 摘要会明显改变本书身份”的 Premise / Meta Grammar / Surprise / Long-Horizon Promise 等现场事件；普通转折不得进入。Outline 必须把 Event Atom / State Residue / Timing Boundary / Reader Anchors 原样注册，只负责排章；BOOK 保存时缺失、改写、重复字段或明确章次未排程都 fail loud。Runtime 只把**本章已引用的 RSE**确定性注入当前 Batch Packet；单章 fallback 继续注入 Director 的唯一事件预算与 Frozen Mission。完整 Registry 不 raw 进入章节 Agent，未来 RSE 不提前泄漏。State Residue 永远不能替代 Event Atom。**Event Atom 冻结事实与因果，不把后台原句锁成正文：会直接显示给人物/读者的 Meta/UI、任务、退出或携带规则优先用一眼能懂的“还剩多久 / 出口在哪里 / 离开能带走什么 / 失败会怎样”等具体事实；后台的合法性、归属状态、资格等精确术语可留在 State Residue。Reader Anchors 只锁 reader-safe 的专名、数字、地点/物件名或确实必须照字出现的世界内短名，不锁策划抽象词。**
- **Scene Craft 研究可以很深，章节 Runtime 必须很窄**：原著 bounded evidence、书名、locator、完整 Generation/Revision Lens 不进入 Writer。当前默认 Batch 链不调用 Curator / Scene Skill Router；它以 BOOK Prose Profile + Full Deterministic Authority Packet 直接进入 Terra Batch Primary。现有 `Scene Prose Projection` 与短 `Revision Watch` 继续保留在单章 fallback / 专项修订；只有独立 Batch-compatible A/B 同时守住小说感、Authority 与 wall 后，才允许重新接入默认 Batch。不得为“功能齐全”临时增加 Batch Curator。新增 Scene Primary 仍必须证明主要阅读问题、scene state、beat engine、Stop/Handoff 都不同，不能因高预算 evidence 或场景重要就扩 taxonomy。
- Collision 可补少量非奠基性过去，让关系/选择更自然；不得自动悲情化、不得用过去证明整个人、不得自动变主线或一次性倾倒。
- Growth 是全书纵向不变量，不是 stage / block / ten-chapter tax。
- **Stable Origins, Evolving Authorities**：开书 World Root / Power Origin / Human Origin 稳定；后续 World Expansion、Power Delta、Human Development 只向未来追加。`CURRENT_CHARACTER.md` 由 Frozen Origins + 已发生 Canon/Delta 确定性编译，不新增 Composer。World Expansion 与 Current Character 必须先独立，只有 Story Refresh 做 fresh Re-Collision；不要让单 Agent 预先把新世界、人物发展和奖励调成主角钥匙孔。**World Independence ≠ World Amnesia**：Expansion 不读取 Current Character / 私有 Power / Human / 关系，但必须读取 `PERSISTENT CANON → World State` 中已经成为世界事实的后果；主角或其他行动者若已公开改变跨地区战力估值、势力行动、市场/迁徙、警戒、传闻、联盟或公共入口，这些“世界上的凹痕”在传播成立时继续影响新 Horizon。只继承世界已怎样改变，不从结果反推隐藏能力、私人欲望、关系或 Build；已传播的少量姓名/公开力量位置/越级战绩只有在会改变新区域 actor 行动时保留其分量，不要求所有人知道或重复旧战绩。
- **Story Program 只具体规划当前 World Horizon；Local Apex ≠ Final Apex**：非终局 Horizon 接近自然边界时输出普通 `World Horizon Handoff`，只定义 trigger、`macro/instance` scope、为什么该扩、carry-forward 与 orchestration；Handoff 不注入 World Agent。若当前 Approved World / Canon 已存在具体外缘信号，可在 Handoff 前最后 1—2 章让读者看见一次“当前世界并非全部”的尺度冲击；只复用已批准旧事实/旧未知，不为钩子提前发明下一世界答案。**若作者明确当前就是小说最终 Horizon / 不再 World Expansion / 正在规划真正结局，则同一 Handoff 第一行固定 `FINAL NOVEL END`，不再输出 Expansion orchestration：主角进入最终公开力量最高可见圈层，并在最后决定性胜负/生存/世界选择中用长期 Advantage Stack 证明同档的决定性 Asymmetry Dominance。** Rival 可同级、可活着、可保留某个专业第一，不要求主角清空所有副轴榜单；终局可以保留未解释世界余白，但不得把它们继续登记成未来主线/调查/Expansion obligation，远期追逐项结束。Outline / Review 不得越过普通 Handoff 发明未知下一世界，也不得越过 `FINAL NOVEL END` 再造更高地图。
- **两层 Power**：Frozen Power Origin + `PERSISTENT CANON → Power / Capability` 的 Current Power Portfolio；后期神兵/传承/新 Asymmetry 不回写 Seed。**三层 Human**：Frozen Origin + Current State + 可选 Human Development Delta。
- **精确力量主尺强制存在，并与 Public Proof 三线共用**：每个 production World Root 必须冻结一把能写出唯一当前位置的公开主尺，只允许 `连续数字`、`大境界+数字子级`、`数字序列` 三种简单 Grammar；Human T0 固定一个精确数字位置，State 在 `Power / Capability` 持续维护 `Current Power Position`。macro World Expansion 只能向上延展同一主尺可见范围，不得改计数语法；独立 instance 必须有自己的本地精确尺，但不回写全局主尺。精确尺是 Reader Ruler，不是战斗公式，不建总战力分；越级仍由技能、装备、经验、环境与 Power Asymmetry 决定。重大 Public Proof 若与主力量相关，**群体震动 + 懂行者 Ruler Calibration + 关键人物 Behavioral Repricing**三条线共同使用精确位置：读者应知道主角/对手到底几级、几星、几重、差多少，以及这个超标怎样改变现场和社会价格；越级胜利不得反推成等级自动提升。
- **World 力量优先 Small Grammar, Large Variation**：如果主流力量已经能用 1—3 句普通话讲清，且现有一到少数互补操作轴已经有辨识度，就保护它，不为了“统一”泛化成元能量/总机制。Small Grammar 不等于 Small World：后续要主动把 Variation 预算花在新招式/战斗姿态、身体/物种、兵器/奇物、异兽/伴生物、会改变玩法的环境、组合、强度与稀有例外；只有旧语法承载不了一个长期值得追的新幻想时才新增底层机制。**World Possibility Ecology 是因果分布，不是能力数量**：高价值“变强/变得不一样”的来源应自然分散在不同 Living Actors、地点、承诺、季节/时间窗口与长期路线，结果可以落到不同身体、器物、传承、伙伴/异兽、环境特权或知识；不要让一个最显眼机制成为所有路线都会经过的 universal upgrade trunk，也不按类别配额凑能力。World 同时主动寻找 0—1 条真正成熟的 Optional Secondary Fantasy Road；没有足够好的创意就不造，也不预设主角一定会走。
- **World Independence = Living Actors，不是机构在运转**：`世界正在发生的大事` 优先由具体人物、生物或小群体的私人目标与下一步可见动作发动；机构、战争、市场和资源格局负责放大后果，不默认替代人物成为发动机。至少若干事件应能回答“谁现在想要什么 → 马上准备做什么 → 没有主角也会改变谁/哪件东西/哪个地方”；允许钱、赢、爱、嫉妒、占有、好奇、报复、舍不得、证明自己等驱动。多线自然碰撞优先来自争同一具体人/物/地点、抢先抵达、带走/毁掉某物或互相追杀，不为此新增 Actor schema / Event table / 每世界冲突配额。
- **Power Seed 生成 Power Asymmetry，不强制世界内合法例外**：World Power Normal 是比较尺，不是来源限制；非对称优势可来自世界内稀有异常、唯一奇物/际遇、外来知识/经验、外挂、极端正常天赋或少量优势叠加。默认故意偏强：Core Power 至少一个维度让同层普通人/天才明显羡慕，必要时提前拥有通常更高层才有的局部特权；Permanent Boundary 防万能但不做对称成本抵消。Novelty Spark 负责不同，不负责削弱强度。Power 另接一小池 **Optional Lexique Primitive Spark**：对象×变化只负责偶尔找到更具体的身体/器物/空间载体或新玩法，每个 Candidate 最多借 0—1 个且可以全部忽略，不得改写既有触发、覆盖、代价、Boundary，也不得长成第二系统。**Reader-facing novelty = 熟悉语言 + 新作用**：World 基础力量、开局 Core 与后续新 Asymmetry 都先用普通话说明具体可观察效果，再决定是否需要短名；命名固定参考来自 source-blind Naming Craft；**首读语义准确高于世界气味**，只有不牺牲准确时才优先复用 World 已有具体词根，lexique 只作次级气味，也可以不用；已有普通短名已经准确时不为“更独特”强改，名字不能反向授权新机制。“全新”改变力量因果/玩法，不要求回避境界、功法、兵器、异兽等清楚题材词；若核心幻想本来是战斗、身体、移动、穿越、操控等直接能力，成长不能重新退化成结构分析、材料诊断、路线计算或验证流程。Legendary / Future Legend 不得绕过 Permanent Boundary。
- **AGGRESSIVE Fantasy / Payoff 是当前默认审美偏置**：LLM 天然过度谨慎，当前因果已经让高价值奖励、胜利、奇遇或占有成立时，不主动少给、晚给或降成资格。大胜可以自然同时带来主奖品 + 钱/资源 + 招揽/入口；秘境可有主目标外的小惊喜；大型阶段可同时结算据点、队伍、产业、商路份额或长期收入。奖励数量本身不是缺陷，只禁止两类硬问题：剧情明确没拿到/拒付却无新因果凭空到账；以及人物刚作出高价值真实牺牲，同一窗口立刻用近似替代物把牺牲抹平。
- **Power Asymmetry 长期形成优势栈；Protagonist Asymmetry Dominance**：开局 Core Asymmetry 持续成长，但全书不能只把同一能力放大；后续应通过真实故事获得新的非对称优势，并让新旧优势产生单项做不到的复合效应。**这种连续获得新高价值 Asymmetry、再递归复合成越来越难复制的 Advantage Stack，默认是被作者选中主角的长期叙事特权。** NPC / Rival 仍可正常修炼、阶段性比主角强、拥有主角没有的神兵/异兽/体质/绝技、拿走主角错失的 signature reward，甚至在某个专业长期第一；不要为了让普通长期 Rival“永远同档”就在主角每次新增优势后也自动给它补一个新异常/奇物/复合，写成第二主角。只有极少数由 Story Program 明确设计成镜像宿敌、共同成长极或最终 Boss 的角色可例外，而且必须来自它自己的因果路线。核心幻想兑现优先保留其独有的生活特权，不只复用最容易安排的战术用途。Access / Identity 可以是奖励，但当功法、兵器、身体变化、奇物或传承已成为主要欲望时，不能长期只用资格/名额/记录替代真正的占有、错失与距离。真实错失允许有空窗：刚因关键选择放弃一个已经建立欲望的高价值对象时，不为补爽点在同一结算窗口立刻塞分量/功能近似的替代奖励。**Route-Bound Acquisition + No Universal World Tour**：新优势先来自 Human 已真实走入的路线；与其选择冲突的 World 高价值窗口可以由 NPC 继续推进、signature reward 归别人、关闭或改变形态，Story Program 不为“把 World 都用上”让主角稍后依次打卡全部大会/矿塔/大战/秘境。新的独立因果仍允许路线回流；同一真实来源让不同 Human 获得相同能力完全合法，不做人格→外挂配额。它是全书纵向要求，不是每阶段新增能力税；Power Seed 只定义开局核心，Story Program 负责后续获得与复合。
- **Persistent Power Reader Proof 必须寄生于 Story**：对“永久留下 / 累积 / 储存 / 复用”这类私有持续性优势，第一次 State 成立后优先让读者在**本来就因宝物、敌人、逃生、关系或世界目标而必须发生**的后续事件里，亲眼看见上次拼命才做到的峰值已经可以直接使用；没有自然事件就延后，不为证明能力新增训练、复测、搬运/护火、工作任务或路边小危险。主角亲自确认复利后，若当前本来就值得追的目标自然要求新的更高极限，且 Frozen Human 的好胜、贪欲、好奇、野心等会被它诱惑，Outline 应让“这个新极限成功后也会成为我的东西”真实参与既有选择，形成目标奖励 + 新永久极限的双重诱惑；不得为了刷能力凭空制造更危险路线，也不得把这层动机只留在人物总结或 Block Delta。
- **非对称优势显露要反复完成 Public Proof，不只在开篇做一次；Public Proof ≠ Hidden Mechanism Knowledge**：首次显露新优势、新层级、新复合用法、进入更高圈层后第一次被更懂行者看见，或旧社会估值明显落后于当前能力时，按现场条件允许三条**并列、没有高低之分**的爽点同时成立：① 有真实观众时的 Collective Shock / 全场鸦雀无声 / 所有人明显震惊 / 喧哗骤停；② 最有资格者短而明确的 **Ruler Calibration**，说明“正常同层能做到什么 → 这次具体超出哪里 → 为什么罕见”；③ 至少一个关键人物通过改口、加价、退距、换战术、招揽、敌视、保护或改变准入完成 **Behavioral Repricing**。大型 Public Proof 可以三路一起吃满，不以“克制/避免吹捧”为由自动削减；**观察者只能知道现场可观察表现、公开力量尺、伤势/器物效果和 World/Canon 已知现象；不能因为他是高手或亲眼见证，就自动知道 Power Asymmetry 的隐藏因果、永久性、私有触发、内部计数或只有主角/Meta Authority 知道的状态。私有 Power 真相优先由 POV 体验、之后自然复用或已授权 Meta Authority 给读者确认。** 只避免凭空造围观者、让所有群众轮流说同一套专业解释，或对普通重复使用反复演同层震惊。短期群体震动本身可以成立；只有 Repricing 继续改变后续行动、关系、资源、敌意或信息流时才升级为 Ripple / Canon。
- **世界前台尺是长期读者坐标，也是信息压缩器**：力量、战绩、价值、天赋/适配、技熟、装备、排名、身份与世界层级都可作尺；当前事件碰到哪把就校准哪把。World 对当前常用少数档位/价值对象提供 1—2 个可感知 benchmark；下游优先用一次已批准比较替代多轮验证，不临时发明冲突标准，也不建战力数据库。**本章若真实跨过前文已说明的公开力量/身份档位，结果处直接命名新档位一次**，不让读者从“凝影了 / 被记名 / 通过了”等现象自己换算。重要 World Entry / Rival / 传承或高价值机会第一次进入时，同时让读者知道为什么值得靠近或争、它相对主角当前位置有多重；若后续要放弃某个机会，先建立其具体价值，否则机会成本只存在于计划里。
- **Public World Knowledge = Clarity；Unknown World = Mystery**：普通人/当前 POV 从小就知道、且会帮助读者理解眼前故事的公共常识——主流力量、粗略强弱尺、当前/下一档现实含义、会改变日常生活的危险规则、常见上升入口与价值物——在明显陌生/架空世界开篇若 World 与前3章确实提供多类相关事实，Outline 默认拆成 2—3 条不同功能的 Reader Release；下一档若有现实 benchmark，同时写能力效果与社会含义。Primary 用 1—3 个短说明段普通话讲清，不让读者靠火盆、服装、站位、专名或隐喻自己猜。**具名机会价值走 Story/Plan 链**：Story Program / 当前剧情块已批准某试场、选拔、招募、契约的名字与公开价值，而 Future 10 单章条目只剩“试场前训练 / 争取机会”等压缩措辞时，Director runtime 只在当章已指向同一机会的条件下，从当前剧情块确定性恢复一条“具体机会名 + 当前已知价值”；不生成新回报、不提前承诺成功、不从未来章偷事实。细节负责让画面活，不能替代基础答案；来源、隐藏原因、幕后关系、未来 reveal 和当前人物不知道的事实继续保持未知；不因此新增 Prelude、百科章、每章 exposition 配额或 Reviewer。
- **Proof 后推进 State**：一个事实经动作结果 + 一次足够 ruler 校准成立后，不换证据继续证明；社会确认只在改变机会、敌意、关系、身份、资源或行动时继续。重大选择的选项与代价已清楚后尽快选择，让后续篇幅进入 Consequence；Supporting Skill 只保留足以改变判断的关键细节，决定后的普通实施默认压缩；非核心 Supporting Skill 即使承担关键实施，也写到效果级因果，不扩成新的小型解题场；若该技能已在前文成立，Director/Curator 默认只写它造成的结果，不重复方法，除非本章出现新边界、失败或质变。Outline 已给出的入口/邀请/名额/工作机会/奖励，不为“证明配得上”自行补试工、检查、考核或登记；低动作章也不为让主角显得能干而临时制造排车、维修、诊断、路线、清点等 **Competence Filler**。**阶段结算写 Consequence，不用程序承载戏剧**：事实已清楚时，报告、登记、责任说明、复盘、资格发放等只作一句/背景，前景放在重新估价、实际得失、Rival 换位和下一件更值得想要的机会。
- **Effective World 是章节期一等世界事实权威**：BOOK §2 只是故事摘要，不能替代 World。Runtime 组合 `WORLD_VISION.md` Root + 当前章 active Forward Expansions，再确定性裁成安全 `WORLD AUTHORITY`；Expansion 只投影公共现实、力量/身份/价值尺度、公开地点/势力和具体价值物，人物隐藏行动与未知边界不直接泄漏给 Writer。`scope=instance` 只在自己的章节窗口生效，离开后 Local World 退场，跨世界 consequence 留在 Canon。Outline 用 `Reader Release Map` 只保存当前规划窗口里 timing-sensitive、且与该章实际事件相交的首次世界事实释放（不是每章 KPI）；未来仍作为 reveal 的答案不得提前进入 Map。**World Entry 在人物真正跨过门槛的当章释放**：正式上路、进入组织/内层、第一次实际使用身份入口时，就说明该入口为什么把第一章位置的人带进过去进不去的世界，不等下一章第一次遇险再补。Chapter Runtime 按章确定性读取并从 WORLD AUTHORITY bounded prefetch；Curator 只筛选/压缩，Writer 只表达、不自行选择或补造世界事实。已排程的 Reader Release 是 timing decision，Writer 必须用最短充分的直接旁白或场景表达兑现，不能把它当可选装饰；若同一事实还说明地点/势力/传承为什么值得争，应保留一个价值锚点。高价值 Orientation 不做百科、Prelude 或 Reader State 数据库；开篇生活定向与 Ruler 分工，单纯“无境界 / 打不过敌人”不能替代安全、生活或社会坐标。named 势力首次进入故事时，若 World 已知其公开类别，该类别应存在于安全 WORLD AUTHORITY，并由当章 Reader Release 一起排程进入正文；动机、隐藏关系和后续 reveal 不进入安全层。**长期历史未知边界**：Canon / Curated Context / Open Promise 已标为未知、未解释、真假未定或原因未明的旧事实，除非 Director 明确批准本章新增确定事实，否则 Writer 不得为完整感补造旧经历、旧对话、隐藏动机或世界机制；公共 Orientation 不授权 retrospective canon。
- **Plot Pace ≠ Tier Pace**：事件、关系、发现、敌人策略、获得和玩法可以快速推进，但不因此自动升境界/等级；同一层级仍有丰富故事空间时允许承载多个完整剧情块，保持长期力量尺纵深。
- **高速成长必须由主角优势承担因果**：如果作者明确要求异常快升阶，Core Asymmetry / Advantage Stack 至少有一条直接改变学习效率、资源效率、实战反馈、风险收益或可接触机会的可观察因果，让读者能回答“为什么偏偏他能这么快”；不能只靠 Outline 逐章递送刚好的材料/传承/危机。
- **Mystery 不急着资源化；对手学习必须有效**：真正有阅读牵引的遗迹、反常地理、古器来源、未知生物或历史谜团可以跨多个事件继续悬着，不因出现矿权/归属/价格就立刻结算成资源题；长期 Rival 在亲眼见证/调查后若更新策略，至少一次要真实改变主角的选择、路线、资源、暴露、关系或战局，否则“他学会了”只是无效旁白。
- **主人公连续升格，不是字段变化集合**：长期应让主角不断进入第一章时没有资格进入的力量层、人物圈层、世界层、真相层与选择层，并尽量形成“力量/身体变化 → 被重新估价 → 新关系/身份/入口 → 新世界与新认知 → 新欲望/敌人/选择 → 再成长”的因果螺旋；进入新圈层时，新人物只按自己真实知道的旧名声/战绩/底牌先判断，再因最低充分的新事实分别更新待遇、敌意或合作，不默认全知也不靠降智轻视；不逐阶段填 KPI，同一等级可以充分生活，不用升阶替代升格。
- **专业/副职只有本身就是强者幻想时才升格为第二幻想轴**：World 主动寻找 0—1 条候选；Story Program 主动检查 Approved World 中已经成立的副轴，不因它不是 Core Power 就忽略。它应有独立可比较的强弱、真正顶层人物、可见胜负/作品、稀有成果与社会价格；普通实施仍压缩。主角是否投入、投入多深由 Human 决定；Human 不想走时，让它继续属于世界或配角，不给每本书强塞副职。
- **少量长期承诺可以成为可判定兑现债务**：具体对象 + 至少一个可观察结算条件，让读者知道离结账还有多远；不把所有 Open Promise 债务化，不机械倒计时，也不保证主角一定赴约、追回或获胜。
- 长篇应保留**震撼式长期重释**：重要旧事实在后续出现足够意外、回看又成立的新解释，并立刻改变力量、身份、关系或世界格局；不要让所有高价值重释都只发生在世界层，当 Power / Character / 已批准旧人旧物旧关系自然提供锚点时，也保留主角级重释纵深；不为制造 Personal Myth 凭空补隐藏身世或未批准旧史，也不做每阶段配额。
- 正文：**Story-bearing Texture > Decorative Density**；克制但不干，丰富但不腻。
- 不为治理化、工程化、蓝领职业化、过度验证分别新增 Reviewer / Agent / Scorer / Hard Gate。

## 8. 实验规则

- 冻结**被测阶段之前的全部已批准上游 authority**，并尽量冻结模型、reasoning、retrieval bundle 与其它输入；一次只改变一个主要变量。
- 测 authority isolation 使用 fresh context；能 deterministic 就不加 LLM Composer。
- 候选选择规则预先规定，不 cherry-pick。
- 先直接读真实输出，再用指标/Judge；明显结构性问题不需要 Judge。
- 至少记录：质量、工程/程序化倾向、Plot Engine、人物自主性、合同稳定性、tokens、wall-clock、credits/成本。
- 结论区分 PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL / INVALID，并记录 **What This Did Not Solve**；单本书或单个 candidate 不直接升级为 production 结论。
- 快速大规模 A/B 可用 Terra high，但不替代默认高质量规划路由。
- **Character Authority Invariance**：凡结构机制可能改变主角取舍，默认用至少 2—3 个动机排序明显不同的冻结 Human 做同一 A/B；Treatment 除了产生目标结构增益，还必须保留 Human-specific 选择差异。若不同 Human 被推成同一种“成长最优/关系最优/道德最优”路线，即使结构更整齐也判失败或降级。
- **Creative Intensity Decision**：当多版都通过 Canon / authority / 基本因果边界，主要差异只是“更 aggressive、更爽、更富 vs 更 conservative、更稳、更少给”时，Steward/Judge **不得自动替作者选择更保守版**。必须保存并向作者并列展示有代表性的真实输出差异，由作者决定冻结强度；当前作者默认审美明显倾向 AGGRESSIVE。只有事实矛盾、authority 越界、真实牺牲被即时等价抹平等硬错误可以直接淘汰，而不能把“奖励较多/主角占便宜较大”本身当成失败。
- **Aggressive Variant Must Be Shown When Over-Restraint Is Suspected**：当问题本身就是 LLM 过度克制、少给、弱化社会反应、把欲望降成资格或把主角写得过于理性时，只要 authority / Canon / 因果允许，实验必须至少包含一个**明显更激进**的真实 Treatment；必要时再加 Extreme Treatment。不得先由系统/Judge替作者把“太爽、奖励太多、反应太大、主角太占便宜”裁掉；保存真实输出并由作者判断是否过头。
- **Matched Decision Point**：要证明‘Personality → Choice → Route’时，先让不同冻结 Human 面对同一个具体诱惑/冲突/机会；对每个被测 Human 都应至少有两个具真实私人价值且不能同时完整取得的方向；价值强弱不必相等，选择后的主要机会成本必须保留，不能被隐藏奖励立即抵消。先验证选择本身是否随 Human 分叉，再放开长期 Story Program；若触发事件与机会池同时变化，长期差异不能纯归因于人格。

## 9. Docs 自动维护

实质改变以下内容时，同一任务同步 current docs：架构/阶段职责、Prompt 核心原则、章节 Runtime、模型路由、GBrain 边界、Canon/State/Ledger、Scene Skills/Prose Runtime、产品工作流/UI。

原则：

- 代码/runtime 是实现事实；docs 只描述**当前有效状态**，不把历史迁移过程混进当前规范。
- 每次更新优先**替换/删除过时文字**，不要只在文末继续追加；同义内容合并，一个概念尽量只有一个主要权威出处。
- 文档必须保持**言简意赅**：只保留理解职责、边界、当前默认和关键原因所必需的内容；实验过程、长证据、旧方案移到实验目录或 `docs/research/`。
- 优先更新已有权威文档，不因一次改动新建 md；若某段已被 `PROJECT_RULES.md` 或另一权威文档完整覆盖，只保留必要引用，不重复抄写。
- 提交前同时检查：过时描述、相互冲突、重复段落和可删除的历史说明；能删旧解决时不要新增解释。

当前主要权威：

- `docs/PIPELINE_METHODOLOGY_AND_VALUES.md`
- `docs/PREMISE_APERTURE.md`
- `docs/MVP_PRODUCT_DIRECTION.md`
- `docs/SPLIT_CHARACTER_AUTHORITY.md`
- `docs/GBRAIN_STORY_CRAFT_V3.md`
- `docs/CHAPTER_RUNTIME_AND_STATE.md`
- `docs/NOVEL_PROSE_REALIZATION.md`
- `docs/AUTHOR_WORKSPACE_UI_SPEC.md`
