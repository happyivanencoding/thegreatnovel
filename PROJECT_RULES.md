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

`作者方向 → protagonist-blind World Vision → POWER_BASELINE / LIFE_CONTEXT → 独立 Power Seed + Human Seed → 作者一次批准 Character → deterministic CHARACTER.md → Story Program（第一次完整 Collision）→ 作者批准 → Outline → Director → Curator → Primary Writer → State Extraction`

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
| Curator | GPT-5.6 Luna | high | raw GBrain OFF；Scene Skills ON |
| Primary Writer | **GPT-5.6 Terra** | high | raw GBrain OFF；Scene Skills ON |
| State Extraction | GPT-5.6 Luna | low | OFF |

默认章节链：`Luna Director → Luna Curator → Terra Primary → Luna State`。

低延迟：Director 可切 Terra high；Curator 可切 Terra medium。只想让 Curator 更短、更克制时优先只切 Curator。

模型判断必须分开看：`生成质量 ≠ wall-clock ≠ 实际成本`。Luna 单价最低；Terra 通常最快且更克制；Sol 最贵且通常最慢，但长期结构最强，默认只放 Story Program / Deep Planning。

## 6. GBrain

GBrain 根目录：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库`

- GBrain 是 Optional Inspiration，不是 Canon、创意权威、Hard Gate 或原作模板。
- **公共治理、资源分配、维护职责、责任升级不得作为 production GBrain 的通用可迁移创作机制**；来源作品确有此内容时只保留为研究证据，并退出 active inspiration。
- 主要路径：`GBrain → World / Power / Human / Story Program / Outline → Approved Story`；以及 `GBrain 离线蒸馏 → Scene Skills → Curator / Primary`。
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
- Human：**经历是背景，不是人格证明**；允许多重动机、稳定选择偏向与现场变化。
- Collision 可补少量非奠基性过去，让关系/选择更自然；不得自动悲情化、不得用过去证明整个人、不得自动变主线或一次性倾倒。
- Growth 是全书纵向不变量，不是 stage / block / ten-chapter tax。
- **Power Seed 生成 Power Asymmetry，不强制世界内合法例外**：World Power Normal 是比较尺，不是来源限制；非对称优势可来自世界内稀有异常、唯一奇物/际遇、外来知识/经验、外挂、极端正常天赋或少量优势叠加。默认故意偏强：Core Power 至少一个维度让同层普通人/天才明显羡慕，必要时提前拥有通常更高层才有的局部特权；Permanent Boundary 防万能但不做对称成本抵消。Novelty Spark 负责不同，不负责削弱强度。
- **Power Asymmetry 长期形成优势栈**：开局 Core Asymmetry 持续成长，但全书不能只把同一能力放大；后续应通过真实故事获得新的非对称优势，并让新旧优势产生单项做不到的复合效应。它是全书纵向要求，不是每阶段新增能力税；Power Seed 只定义开局核心，Story Program 负责后续获得与复合。
- **非对称优势显露本身可以是爽点**：首次显露新优势、新层级或意外复合时，若现场有人见证，用已有懂行者/对手/同伴的短反应完成超标比较与惊讶；不凭空加围观者、不反复群体吹捧。只有重新估价会改变后续行动或关系时才让态度转变进入剧情，否则惊讶/确认后即可停止。
- **世界前台尺是长期读者坐标，也是信息压缩器**：力量、战绩、价值、天赋/适配、技熟、装备、排名、身份与世界层级都可作尺；当前事件碰到哪把就校准哪把。World 对当前常用少数档位/价值对象提供 1—2 个可感知 benchmark；下游优先用一次已批准比较替代多轮验证，不临时发明冲突标准，也不建战力数据库。
- **Proof 后推进 State**：一个事实经动作结果 + 一次足够 ruler 校准成立后，不换证据继续证明；社会确认只在改变机会、敌意、关系、身份、资源或行动时继续。重大选择的选项与代价已清楚后尽快选择，让后续篇幅进入 Consequence；Supporting Skill 只保留足以改变判断的关键细节，决定后的普通实施默认压缩。
- **高价值 Orientation ≠ 低价值解释**：开篇先建立最低安全 / 社会 / 移动坐标；重要势力、地点、身份、资源或生活方式第一次真正影响选择时，允许 1—3 个短直接旁白回答“是什么 / 为什么重要 / 普通人或当前 POV 怎么看”，随后回到动作。Orientation 只占解释预算，不新增 Prelude 章、不延迟既定 payoff。World 提供事实，Outline 调度首次释放，Curator 只选已批准事实，Writer 只表达、不补隐藏原因；不做百科或每章说明配额。
- **Plot Pace ≠ Tier Pace**：事件、关系、发现、敌人策略、获得和玩法可以快速推进，但不因此自动升境界/等级；同一层级仍有丰富故事空间时允许承载多个完整剧情块，保持长期力量尺纵深。
- **主人公连续升格，不是字段变化集合**：长期应让主角不断进入第一章时没有资格进入的力量层、人物圈层、世界层、真相层与选择层，并尽量形成“力量/身体变化 → 被重新估价 → 新关系/身份/入口 → 新世界与新认知 → 新欲望/敌人/选择 → 再成长”的因果螺旋；不逐阶段填 KPI，同一等级可以充分生活，不用升阶替代升格。
- 长篇应保留**震撼式长期重释**：重要旧事实在后续出现足够意外、回看又成立的新解释，并立刻改变力量、身份、关系或世界格局；不强制隐藏身世，也不做每阶段配额。
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
