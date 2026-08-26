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
