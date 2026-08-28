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

`作者方向 → protagonist-blind World Vision → POWER_BASELINE / LIFE_CONTEXT → 独立 Power Seed + Human Seed → 作者一次批准 Character → deterministic CHARACTER.md → Story Program（第一次完整 Collision）→ 作者批准 → Outline → Director → Curator → Primary Writer → Authority Reviser → State Extraction`

- **没有 production Fantasy Seed。**
- **没有 Character Composer LLM。** Power/Human 不做后验主题化调和。
- 批准点保持紧凑：World Vision → Character（Power + Human 一次批准）→ Story Program。

## 5. 默认模型与 GBrain 路由

| 阶段 | 默认模型 | Reasoning | GBrain |
|---|---|---:|---|
| World Vision | GPT-5.6 Luna | high | ON：固定 1 条 Reader Coordinates Reference + 最多 3 条 creative inspiration |
| Power Seed | GPT-5.6 Luna | high | ON：Power lane，小 bundle |
| Human Seed | GPT-5.6 Luna | high | ON：Appetite / Behavior / Relationship 各最多 1 条，总计最多 3 条 |
| Story Program | **GPT-5.6 Sol** | high | ON：最多 3 条 focused inspiration |
| Outline | GPT-5.6 Luna | high | ON：通常 4 条、最多 5 条 |
| Director | GPT-5.6 Luna | high | raw GBrain OFF |
| Curator | GPT-5.6 Luna | high | raw GBrain OFF；Scene Skill v2 Catalog + short Projection compile |
| Primary Writer | **GPT-5.6 Terra** | high | raw GBrain OFF；只吃 Curator 的短 `Scene Prose Projection`，不吃完整 Scene Skill |
| Authority Reviser | GPT-5.6 Luna | **high** | raw GBrain **OFF**；safe Authority + Curator + Primary；仅追加已验证的短 `Revision Watch` |
| State Extraction | GPT-5.6 Luna | low | OFF |

默认章节链：`Luna Director → Luna Curator → Terra Primary Draft → Luna high Authority Reviser → Luna State`。Primary 在 `curator_primary` 中只是第一版，不可直接成为 `final_source`；State 只读取已采用的 Authority Revision，或显式 repair 后的 Integrator 最终稿。

低延迟：Director 可切 Terra high；Curator 可切 Terra medium。只想让 Curator 更短、更克制时优先只切 Curator。

模型判断必须分开看：`生成质量 ≠ wall-clock ≠ 实际成本`。Luna 单价最低；Terra 通常最快且更克制；Sol 最贵且通常最慢，但长期结构最强，默认只放 Story Program / Deep Planning。

## 6. GBrain

GBrain 根目录：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库`

- GBrain 是 Optional Inspiration，不是 Canon、创意权威、Hard Gate 或原作模板。
- **公共治理、资源分配、维护职责、责任升级不得作为 production GBrain 的通用可迁移创作机制**；来源作品确有此内容时只保留为研究证据，并退出 active inspiration。
- 主要路径：`GBrain → World / Power / Human / Story Program / Outline → Approved Story`；以及 `GBrain 离线深蒸馏 → source-blind Scene Deep Craft → Curator 短 Projection / Reviser 短 Watch`。
- raw GBrain 不直接进入章节 Writer Runtime。
- 蒸馏分工：Terra 看清事实/Fidelity；Luna 理解吸引力与中层 craft；Sol 理解长篇结构。
- Windows / Git Bash 使用 `~/.bun/bin/gbrain.exe`；新增、修改或删除页面后执行 `embed --stale`；交付前必须 `Embedded == Chunks`。
- 排障顺序：executable/path → environment/API key → stats → PGLite lock → process cleanup；不要先杀 `bun.exe`。

## 7. 系统级创作原则

始终遵守：

> **支撑性逻辑不得自动成为故事发动机。**

即：世界复杂度 ≠ 叙事焦点；对手有理由 ≠ 作品认同 ≠ 主角义务；机制真实 ≠ 展开实施细节；能力 ≠ 职业；可以验证 ≠ 验证过程就是故事。

同时：

- 修最早发生语义坍缩的节点；少深层规则 > 多 Hard Gate。
- Human：**经历是背景，不是人格证明**；允许多重动机、稳定选择偏向与现场变化。冻结 Human Core 高于最近几章的“负责/克制/救人”等行为归纳；下游不得把局部正确选择反推成新的道德人格。章节期从 `CHARACTER.md` 确定性投影 Frozen Human Core 给 Curator；Curator 不重复 Power Core。当前场景自然触发已批准的虚荣、钱、审美、身体吸引、享受、好奇、偏心等私人牵引时，应让它真实影响注意力、靠近/回避或选择，不统一净化成职责协作与成熟沟通。若 Frozen Human 已明确某个具体人会改变选择，而本章正发生近身照料、重逢、分别、私密靠近、嫉妒或邀请等关系现场，默认属于自然触发，保留一个克制 cue 即可，不要求改写主事件。
- **Primary 后固定 Authority Reviser 做 Preservation-First 的远端权威恢复，不做第二次创作**：Primary 为减负只吃近端压缩上下文，允许先完整实现一版；Reviser 再读取冻结 Mission、Curator、safe `WORLD AUTHORITY`、逐条 `Reader Release`、`CHARACTER.md` 的 Frozen Power + Human Core、Canon 与 Primary Draft。正确段落默认逐字保留，只删/压反复确认、重复证明、工程化/程序化实施和 Competence Filler，只补已批准但第一版遗漏的世界/人物/力量 realization；不得改变主要事件、人物选择、胜负、资源得失、Direct Result、State Change、Ending 或未知事实边界。删除前先确认不会丢失 State Change / Social Repricing / Reward / Relationship Change / New Desire / Next Opportunity。**同一维度若 Curator / Primary 与 Frozen Mission / Canon / safe World / Frozen Power / Frozen Human 冲突，Frozen Authority 必须胜出，并在最终稿做语义级全章清零；不能只修第一处。** 修冲突段落时逐句 salvage：本身被 Authority 支持、只因错误时点/因果而失效的 Core Fantasy / Relationship / Desire / Payoff / Surprise / Social Repricing 句，迁到最近合法位置；salvage 只保护高价值句，不保护周围报告、登记、路线或普通实施。raw GBrain 固定 OFF。Optional Specialist / Integrator repair 如显式启用，以 Authority Revision 而非 Primary 为底稿。
- **Scene Craft 研究可以很深，章节 Runtime 必须很窄**：原著 bounded evidence、书名、locator、完整 Generation/Revision Lens 不进入 Writer。Curator 只看 `skill_id + Reading Question + 一行 Projection Guidance`，有真实 realization 缺口时编译 2—4 句 `Scene Prose Projection`，已经清楚写 `NONE`；Terra Primary 只消费这份短 Projection。Authority Reviser 只拿经 A/B 证明安全的一行 failure-triggered `Revision Watch`，无对应失败时忽略。新增 Scene Primary 必须同时证明主要阅读问题、scene state、beat engine、Stop/Handoff 都不同，且 compact conditional / existing composition 的 A/B 不足；高预算 evidence 或“这种场景很重要”本身不授权扩 taxonomy。
- Collision 可补少量非奠基性过去，让关系/选择更自然；不得自动悲情化、不得用过去证明整个人、不得自动变主线或一次性倾倒。
- Growth 是全书纵向不变量，不是 stage / block / ten-chapter tax。
- **Power Seed 生成 Power Asymmetry，不强制世界内合法例外**：World Power Normal 是比较尺，不是来源限制；非对称优势可来自世界内稀有异常、唯一奇物/际遇、外来知识/经验、外挂、极端正常天赋或少量优势叠加。默认故意偏强：Core Power 至少一个维度让同层普通人/天才明显羡慕，必要时提前拥有通常更高层才有的局部特权；Permanent Boundary 防万能但不做对称成本抵消。Novelty Spark 负责不同，不负责削弱强度。**Reader-facing novelty = 熟悉语言 + 新作用**：World 基础力量、开局 Core 与后续新 Asymmetry 都先用普通话说明具体可观察效果，再决定是否需要短名；新词只压缩已经理解的对象，不靠新词互相定义证明原创。“全新”改变力量因果/玩法，不要求回避境界、功法、兵器、异兽等清楚题材词；若核心幻想本来是战斗、身体、移动、穿越、操控等直接能力，成长不能重新退化成结构分析、材料诊断、路线计算或验证流程。Legendary / Future Legend 不得绕过 Permanent Boundary。
- **Power Asymmetry 长期形成优势栈**：开局 Core Asymmetry 持续成长，但全书不能只把同一能力放大；后续应通过真实故事获得新的非对称优势，并让新旧优势产生单项做不到的复合效应。核心幻想兑现优先保留其独有的生活特权，不只复用最容易安排的战术用途。Access / Identity 可以是奖励，但当功法、兵器、身体变化、奇物或传承已成为主要欲望时，不能长期只用资格/名额/记录替代真正的占有、错失与距离。真实错失允许有空窗：刚因关键选择放弃一个已经建立欲望的高价值对象时，不为补爽点在同一结算窗口立刻塞分量/功能近似的替代奖励。它是全书纵向要求，不是每阶段新增能力税；Power Seed 只定义开局核心，Story Program 负责后续获得与复合。
- **非对称优势显露要反复完成社会校准，不只在开篇做一次**：首次显露新优势、新层级、新复合用法、进入更高圈层后第一次被更懂行者看见，或旧社会估值明显落后于当前能力时，若现场存在合适观察者，默认同时给 **Behavioral Repricing + Ruler Calibration**：至少一个关键观察者用可见动作改变（停手、站起、改口、试探、退距、加价、换战术等），并由最有资格者用短而明确的专业解释告诉读者“正常情况下能做到什么 → 这次具体超出哪里 → 为什么罕见/可能意味着什么”，持续校准力量尺和世界尺。两者都要有，不把专业解释压成只有动作，也不把动作压成只有设定旁白；可以有一个短群体 cue，但不凭空加围观者、不轮流写群众反应。若没有真正懂行者，不凭空造专家，可用最近的知情者或已批准直接旁白做最小 ruler 校准。短期爽点本身可以成立；只有 Repricing 继续改变后续行动、关系、资源、敌意或信息流时才升级为 Ripple / Canon。
- **世界前台尺是长期读者坐标，也是信息压缩器**：力量、战绩、价值、天赋/适配、技熟、装备、排名、身份与世界层级都可作尺；当前事件碰到哪把就校准哪把。World 对当前常用少数档位/价值对象提供 1—2 个可感知 benchmark；下游优先用一次已批准比较替代多轮验证，不临时发明冲突标准，也不建战力数据库。重要 World Entry / Rival / 传承或高价值机会第一次进入时，同时让读者知道**为什么值得靠近或争、它相对主角当前位置有多重**；若后续要放弃某个机会，先建立其具体价值，否则机会成本只存在于计划里。
- **Proof 后推进 State**：一个事实经动作结果 + 一次足够 ruler 校准成立后，不换证据继续证明；社会确认只在改变机会、敌意、关系、身份、资源或行动时继续。重大选择的选项与代价已清楚后尽快选择，让后续篇幅进入 Consequence；Supporting Skill 只保留足以改变判断的关键细节，决定后的普通实施默认压缩；非核心 Supporting Skill 即使承担关键实施，也写到效果级因果，不扩成新的小型解题场；若该技能已在前文成立，Director/Curator 默认只写它造成的结果，不重复方法，除非本章出现新边界、失败或质变。Outline 已给出的入口/邀请/名额/工作机会/奖励，不为“证明配得上”自行补试工、检查、考核或登记；低动作章也不为让主角显得能干而临时制造排车、维修、诊断、路线、清点等 **Competence Filler**。**阶段结算写 Consequence，不用程序承载戏剧**：事实已清楚时，报告、登记、责任说明、复盘、资格发放等只作一句/背景，前景放在重新估价、实际得失、Rival 换位和下一件更值得想要的机会。
- **Approved World Vision 是章节期一等世界事实权威**：BOOK §2 只是故事摘要，不能替代 World。Runtime 将 World Vision 确定性裁成不含 named 大事件 / 未解谜底的 `WORLD AUTHORITY`；Outline 用 `Reader Release Map` 只保存当前规划窗口里 timing-sensitive、且与该章实际事件相交的首次世界事实释放（不是每章 KPI）；未来仍作为 reveal 的答案不得提前进入 Map。**World Entry 在人物真正跨过门槛的当章释放**：正式上路、进入组织/内层、第一次实际使用身份入口时，就说明该入口为什么把第一章位置的人带进过去进不去的世界，不等下一章第一次遇险再补。Chapter Runtime 按章确定性读取并从 WORLD AUTHORITY bounded prefetch；Curator 只筛选/压缩，Writer 只表达、不自行选择或补造世界事实。已排程的 Reader Release 是 timing decision，Writer 必须用最短充分的直接旁白或场景表达兑现，不能把它当可选装饰；若同一事实还说明地点/势力/传承为什么值得争，应保留一个价值锚点。高价值 Orientation 不做百科、Prelude 或 Reader State 数据库；开篇生活定向与 Ruler 分工，单纯“无境界 / 打不过敌人”不能替代安全、生活或社会坐标。named 势力首次进入故事时，若 World 已知其公开类别，该类别应存在于安全 WORLD AUTHORITY，并由当章 Reader Release 一起排程进入正文；动机、隐藏关系和后续 reveal 不进入安全层。**长期历史未知边界**：Canon / Curated Context / Open Promise 已标为未知、未解释、真假未定或原因未明的旧事实，除非 Director 明确批准本章新增确定事实，否则 Writer 不得为完整感补造旧经历、旧对话、隐藏动机或世界机制；公共 Orientation 不授权 retrospective canon。
- **Plot Pace ≠ Tier Pace**：事件、关系、发现、敌人策略、获得和玩法可以快速推进，但不因此自动升境界/等级；同一层级仍有丰富故事空间时允许承载多个完整剧情块，保持长期力量尺纵深。
- **主人公连续升格，不是字段变化集合**：长期应让主角不断进入第一章时没有资格进入的力量层、人物圈层、世界层、真相层与选择层，并尽量形成“力量/身体变化 → 被重新估价 → 新关系/身份/入口 → 新世界与新认知 → 新欲望/敌人/选择 → 再成长”的因果螺旋；进入新圈层时，新人物只按自己真实知道的旧名声/战绩/底牌先判断，再因最低充分的新事实分别更新待遇、敌意或合作，不默认全知也不靠降智轻视；不逐阶段填 KPI，同一等级可以充分生活，不用升阶替代升格。
- **专业/副职只有本身就是强者幻想时才升格为第二幻想轴**：应有独立可比较的强弱、真正顶层人物、可见胜负/作品、稀有成果与社会价格；普通实施仍压缩，是否投入由 Human 决定，不给每本书强塞副职。
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
- `docs/MVP_PRODUCT_DIRECTION.md`
- `docs/SPLIT_CHARACTER_AUTHORITY.md`
- `docs/GBRAIN_STORY_CRAFT_V3.md`
- `docs/CHAPTER_RUNTIME_AND_STATE.md`
- `docs/NOVEL_PROSE_REALIZATION.md`
- `docs/AUTHOR_WORKSPACE_UI_SPEC.md`
