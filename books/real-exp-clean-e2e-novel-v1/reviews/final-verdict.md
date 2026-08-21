# Clean End-to-End Novel Test v1 — Final Verdict

## 0. 审查范围

本报告只依据本轮列出的源产物与 Reviewer 结果，根目录为：

`C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-novel-v1`

未读取工作区其他文件、历史实验、GBrain、Reference Programs 或其他小说内容。

## 1. Branch / HEAD / Git status

以下信息直接取自 `FREEZE_SNAPSHOT.md`，未猜测当前 Git 状态，也未执行额外 Git 检查。

- Branch：`principal_dev_new_sys`
- HEAD：`5992f62d11e8014c3cf783bf993589e1cb881585`
- Status：clean；记录为 `git status --short` 无输出
- HEAD subject：`docs: record dynamic pacing freeze verdict`
- Freeze 时间：2026-08-21，Europe/Paris

## 2. Frozen production baseline 与有效 Prompt source

本轮冻结的有效生产 Prompt source：

`src/story_mvp/prompts.py`

有效模板记录：

- `DEFAULT_DIRECTOR_TEMPLATE`：line 108
- `FANTASY_SEED_TEMPLATE`：line 484
- `WORLD_VISION_TEMPLATE`：line 535
- `STORY_PROGRAM_TEMPLATE`：line 599，并通过 `DEFAULT_PROMPT_TEMPLATES["idea"]` 注册
- `OUTLINE_TEMPLATE`：line 669
- `DEFAULT_STATE_DELTA_TEMPLATE`：line 835
- Writer 当前正式模板：`DEFAULT_PROMPT_TEMPLATES["chapter"]`，由 `generate_prompt(mode="chapter", ...)` 追加 `PROSE_REALIZATION_CONTRACT`
- Chapter Prep 当前正式模板：`DEFAULT_PROMPT_TEMPLATES["chapter_prep"]`

Freeze 记录的相关 Prompt 提交包括：

- `2c1e3434b6d68043ba0aac556e63d7912ba23368` — Long-Form Pacing
- `2be35340b36aa05588c85324ffd5e2e1bfa6d951` — Outline Eventization
- `e2e3bac29039afa075a60d48b31abe1d0d9ff3f2` — compounding growth engine
- `b6828961e9e4939577e66264cc0b9a62de1ade95` — first-payoff moral default neutralization
- `a6e551460f1f13a8d42c44d43e8961b4f552958e` — Fantasy-First production prompt neutralization
- `bb5361519929c996aa386672897bc98756e02a51` — Fantasy-First Story System v1

`EXPERIMENT.md` 明确记录：本轮不修改生产 Prompt、runtime、GBrain、Schema、UI 或其他生产代码。

## 3. 唯一作者 INPUT

唯一作者输入：

`INPUT.md`

其要求是：

- 创作成熟中文男频玄幻修仙成长长篇；
- 主角具有持续、可感知的一级成长；
- 主角拥有普通人难以复制的非对称优势；
- 故事可长期发展，持续产生新的行动空间、机会、冲突、人物关系和世界扩张；
- 具体世界、力量体系、主角身份、人物、敌人、资源、题材玩法、价值观和终局由系统自行创造；
- 不预先分配题材类型。

`FREEZE_SNAPSHOT.md` 与 `EXPERIMENT.md` 均确认：本轮生成阶段不读取 GBrain、Reference Programs、旧 BOOK、Growth Genome 旧实例、历史候选、旧 Reviewer、旧评价或其他小说正文。

## 4. Fantasy Seed、四个候选与 Blind Selection

### 原始 Fantasy Seed response

路径：

`seed/fantasy_seed_response.md`

这是一次 Fantasy Seed 原始 response，包含四个候选，每个候选都覆盖核心幻想、主角欲望、力量体验、第一次奇观、长期增长发动机、非对称优势、第一次兑现、早期兑现、稳定循环、中期里程碑、远期升格和世界扩张。

### 四个候选

1. `seed/candidate-01.md` — 《炉藏万象》

   主角能从毁灭或毁坏之物中取出其最后仍能完成的一件事，并将残响铸成可复用道器。核心增长是从断镐、废炉、残兵，逐步发展到炉场、炉城、星辰和文明法则。

2. `seed/candidate-02.md` — 《把天地带在身上》

   主角把活着的天地折叠成界种，种入自身气海，逐渐拥有可生产、可迁徙、可扩张的移动内世界。

3. `seed/candidate-03.md` — 《万物归名》

   主角能听见被抹去或篡改之物的真实名字，并通过恢复名字使人、城、功法和历史重新获得权利与行动资格。

4. `seed/candidate-04.md` — 《把未发生的路带回来》

   主角能看见现实选择时被舍弃的因果支流，并把未发生的道路、技艺、机会和结果带回当下。

### Blind Selector

路径：

`seed/blind-selection.md`

选择结果：候选 1《炉藏万象》。

Selector 给出的理由是：该候选的核心幻想占有欲最强，主角主动进入毁灭现场，把废墟转化为可复用、可组合、持续升级的道器体系；长篇增长、世界扩张和追读发动机最清楚。

### Selected Candidate

路径：

`seed/selected_candidate.md`

内容为候选 1《炉藏万象》的完整选定版本，与 `candidate-01.md` 对应。

重要边界：本轮使用独立 Blind Selector 替代作者人工选择；后续 World Vision、Story Program 和 Outline 使用的是本轮渲染进程中的内存审批夹具，不代表真实作者批准，也未写入生产 Creative State。

## 5. World Vision、Story Program、Dynamic Outline

### World Vision

路径：

`world/world_vision_response.md`

关键结果：

- 核心不变量是“毁灭之物仍可能完成最后一次具体行动”；
- 主角必须亲自推动该行动，才能把残响铸成道器、炉法、路线、关系或生产能力；
- 重铸不是无条件占有，也不是把过去原样复原；
- 主角沈燧从无法储灵的“漏空炉体”，成长为残器铸造者、炉主、炉城核心，最终成为能够为新秩序提供承载方式的开炉者；
- 主要冲突来自玄烬仙宗、归寂一派、焚墟猎团，以及被救对象自身的选择；
- 第一决定性兑现是断镐凿路；
- 早期兑现是废弃炼器窟点燃炉心、铸成第一件真正属于沈燧的下品道器；
- 中期里程碑是赤垣城铸成移动炉城；
- 远期方向是为失去支撑的山河、星辰、神骸和断代文明创造新的法则载体。

### Story Program

路径：

`story/story_program_response.md`

关键结果：

- 主角确定为沈燧，出生于黑炉矿镇；
- 初始危机是玄烬仙宗将在三日后把矿脉、炉火和居民一起炼成废炉；
- 长期循环被明确为：

  `进入毁灭现场 → 辨认最后用途 → 亲自推动完成 → 留下资产 → 进入下一处更高价值现场`

- 成长阶段为：

  `借响 → 铸器 → 合炉 → 无旧器造新器 → 载城与载法`

- 关键人物包括阮青禾、裴照川、晏归尘；
- 故事长期阶段依次为封炉求生、废窟开炉、残兵成阵、兵库开门、边城铸心、无星天路、神骸断代与天地开炉；
- 第一次完整兑现位于废弃炼器窟；
- 重要净收益包括裂路器、火鳞器、私人炉场、残兵炉阵、无门舟、移动炉城和天路炉。

### Dynamic Outline

路径：

`outline/outline_response.md`

本轮 `EXPERIMENT.md` 明确规定 Dynamic Outline 只调用一次。因此：

- Outline N：可确认的是本轮唯一一次 Dynamic Outline，按调用计数为 `N=1`；
- 文件本身未记录独立的语义版本号，不对其猜测其他版本编号；
- 规划范围：预计第 1—76 章；
- 该范围是动态规划值，不是章节合同。

### 当前规划窗口终点

窗口终点是：

沈燧完成从矿镇求生、废窟开炉、古战场取残兵、兵库造新器到赤垣城铸心的成长循环。赤垣城在天火中铸成城心、脱离原有灵脉并成为移动炉城后，故事从个人逃亡自然跃迁到社会整体继续行动，并打开死星、无星天路和上界文明矿海。

这不是前三章已经发生的事实，而是规划中的窗口终点。

### Future 10

以下均为计划，不是前三章已发生事实：

1. `第1章：三日封炉`  
   建立封炉令、漏空炉体、矿镇危机和主动求生目标。

2. `第2章：断镐最后想做的事`  
   沈燧第一次借入断镐残响，理解其最后用途是凿路救人。

3. `第3章：一击凿生路`  
   断镐完成一次不可逆的凿路，矿工获得出口。

4. `第4章：把废铁留住`  
   收集断镐锋意、粗铁、断链和残火，尝试保存一次性力量。

5. `第5章：裂路器`  
   将锋意铸成可重复打开短裂隙的粗本道器。

6. `第6章：废窟黑门`  
   进入废弃炼器窟，发现未完成炉心与高温区域。

7. `第7章：最后一传`  
   让烧毁火脉完成“把火传给下一座炉”的最后用途。

8. `第8章：炉监夺火`  
   裴照川和回收队争夺炉火与器胚。

9. `第9章：自己的炉火`  
   沈燧建立初步个人炉心，火鳞器成形。

10. `第10章：火鳞出炉`  
    完成第一件真正属于自己的下品道器，取得私人炉场和稳定退路。

## 6. BOOK 与当前实验执行上下文

路径：

`BOOK.md`

本轮 `BOOK.md` 是实验执行上下文，不是生产书库。前三章完成后，它记录了：

- 当前 Active Scene State；
- Persistent Canon；
- 三章 Recent Summaries；
- Open Promises；
- 尚未确认的粗铁、断链、残火回收；
- 尚未完成的沈燧脱身；
- 尚未兑现的裂路器、废窟炉心、古战场路线。

因此，Chapter 3 的未完成资产回收是当前叙事状态，不应直接写成生成失败。

## 7. Chapter 1—3 与完整执行链路径

| 章节 | Director | Chapter Prep | Writer / 正文 | State / Canon |
|---|---|---|---|---|
| Chapter 1 | `chapter-01/director_prompt.md` → `chapter-01/director_response.md` | `chapter-01/chapter_prep_prompt.md` → `chapter-01/chapter_prep_response.md` | `chapter-01/writer_prompt.md` → `chapter-01/writer_response.md` → `chapter-01/chapter.md` | `chapter-01/state_delta_prompt.md` → `chapter-01/state_delta.md` → `chapter-01/canon_after.md` |
| Chapter 2 | `chapter-02/director_prompt.md` → `chapter-02/director_response.md` | `chapter-02/chapter_prep_prompt.md` → `chapter-02/chapter_prep_response.md` | `chapter-02/writer_prompt.md` → `writer_response_attempt-1.md`（技术截断）→ `retry_log.md` → `writer_response_retry-2.md` / `writer_response.md` → `chapter-02/chapter.md` | `chapter-02/state_delta_prompt.md` → `chapter-02/state_delta.md` → `chapter-02/canon_after.md` |
| Chapter 3 | `chapter-03/director_prompt.md` → `chapter-03/director_response.md` | `chapter-03/chapter_prep_prompt.md` → `chapter-03/chapter_prep_response.md` | `chapter-03/writer_prompt.md` → `chapter-03/writer_response.md` → `chapter-03/chapter.md` | `chapter-03/state_delta_prompt.md` → `chapter-03/state_delta.md` → `chapter-03/canon_after.md` |

章节结果：

- Chapter 1：封炉令落下，沈燧拒绝等死，进入下层矿道并触到断镐，但尚未真正握住或借响。
- Chapter 2：沈燧真正握住断镐，首次借响，打开仅容一人通过的临时裂口，开始转移矿工并收集粗铁、断链和残火。
- Chapter 2 Writer：第一次响应缺少 `# 章节事实摘要`，按技术截断规则用完全相同 Prompt 重试一次并成功；原因与两次响应已记录在 `chapter-02/retry_log.md`。
- Chapter 3：沈燧顺着断镐残响凿穿封壁，冷风和微光进入，矿工开始沿上坡风槽撤离；断镐碎裂，碎铁仍有锋意，但沈燧尚未确认脱身，粗铁、完整断链和最终出口也尚未确认。

## 8. Reviewer 汇总

| Reviewer | 结果 | 已证实与主要观察 |
|---|---|---|
| Blind Reader | `CLEAN_E2E_PROMISING` | 会继续点击第四章。三章有明确危机、主角主动行动、能力边界、章尾推进和长期追读问题。唯一报告代码为 `OWNERSHIP_PAYOFF_WEAK`：资产回收已主动成立，但第三章末尚未完成拥有与复用。 |
| Execution Fidelity | `EXECUTION_PIPELINE_MIXED` | 最早真实损失发生在 Chapter 1 Director：提前把“第一次借响”写入第一章，而 Outline 将其安排在第二章。Chapter 1 Prep 随后回正，正文按回正结果生成。另有一次 Chapter 2 Writer 技术截断，按相同 Prompt 重试成功；没有发现由此产生的创意回归。 |
| World Engine | `EARLY_WORLD_ENGINE_HEALTHY` | 封炉令、阵纹、巡炉队、矿工互救和居民依赖显示世界不会只围绕主角运转；资源存在控制、依赖和争夺；阮青禾、裴照川和矿工有主角之外的行动计划；规则已产生职业、权力和生存后果。市场交易、更广势力网络和长期 NPC 目标尚未展示，但尚未达到失败阈值。 |
| AI Prose | 三章整体可读，存在中度明显的设计化/AI 高级感 | 物理现场充分，重量、灰尘、伤口、声音和空间变化真实；不是 `REACTION_WITHOUT_CONSEQUENCE`。主要问题是动作后重复解释意义、对白承担设定教学、主题词过早盖章、章尾出现任务清单式收束。`ABSTRACT_PAYOFF` 整体未成立，但第一章能力初显有局部风险。 |
| State / Continuity | 通过 | Chapter 1 → 2、Chapter 2 → 3 均连续；未发现 `STATE_RECAP_LEAK`。断镐、旧矿图、伤势、残火、粗铁和断链的正文状态基本连续。 |
| Cross-Layer | 核心承诺保留、节奏早期健康 | Seed → World Vision → Story Program → Outline → 三章正文链条一致；没有发现整体历史 attractor 复现；没有冻结上游重开理由。 |

### State Reviewer 必须保留的注意项

`chapter-01/canon_after.md` 没有列出正文已经出现的粗铁、断链和残火。State Reviewer 将其判定为 Canon 快照记录不完整，而不是正文连续性断裂，因为后续章节正文仍有直接承接依据。

另有两项较小记录注意：

- Chapter 1 Canon 记录了沈燧手背擦伤，后续没有单独追踪，但没有证据表明形成矛盾；
- Chapter 3 Director response 将粗铁、断链、残火概括为“被保住”，但正文与正式 Canon 仍显示粗铁未拔出、断链仅部分进入风槽、最终出口未确认。应以正文和正式状态为准。

## 9. CORE_PROMISE 状态

`CORE_PROMISE_PRESERVED`

理由：

- 沈燧不是被动获得奇遇，而是主动进入封闭矿道、救援矿工；
- 断镐残响被具体化为方向、重量和凿击落点；
- Chapter 3 完成了第一次不可逆的核心行动：凿穿封壁，让矿工获得继续行动的路径；
- “最后用途 → 亲自完成 → 留下可复用资产”的后续链条仍然开放，没有被替换成普通逃生或泛化力量。

核心承诺尚未完整结算为裂路器，但这是 Outline 明确安排在第 4—6 章的后续阶段，不构成承诺丢失。

## 10. Long-Form Pacing Early Signal

`EARLY_PACING_HEALTHY`

前三章并非重复拖延：

- Chapter 1 建立封炉危机和能力发现；
- Chapter 2 完成首次借响并打开临时通路；
- Chapter 3 引入巡炉队反制并完成更高难度的贯通行动；
- 资产、残火、断链和碎铁形成后续行动空间。

如果后续继续重复“窄缝收缩—再凿一下”，却不完成脱身或铸器，才会形成 `PACING_FIX_OVERDELAY` 证据。当前尚无该证据。

## 11. 历史 attractor

未出现整体历史 attractor，不报告 `HISTORICAL_ATTRACTOR_RECURRED`。

说明：

- “废弃炼器窟”“炉心”“铸器”属于本轮已选定的《炉藏万象》核心链条；
- “身份权柄”仅作为世界力量来源之一出现，没有发展成《万物归名》的名字权柄主发动机；
- “偷未来、吞世界、唯一现实、败世”等其他候选或历史模式没有在选定链条及前三章形成整体复现。

## 12. Reader Verdict

`CLEAN_E2E_PROMISING`

前三章实际可读，开场问题清楚，沈燧的行动指纹明确，核心能力可理解且不可被普通理性主角无损替代。当前最明显的保留项是长期资产尚未完全交付，以及 prose 仍偏设计化。

## 13. Execution Verdict

`EXECUTION_PIPELINE_MIXED`

`NEAREST_FAILURE_LAYER: Director（第1章，已被 Prep 回正）`

这是执行层边界漂移，不是上游设计回归：

- Outline 将 Chapter 1 设为触摸断镐、Chapter 2 设为第一次借响；
- Chapter 1 Director 提前写成短暂借入断镐最后一击；
- Chapter 1 Prep 将其回正为“触摸但尚未真正握住”；
- Chapter 1 正文遵循回正后的边界；
- Chapter 2 才完成首次借响。

因此应记录为执行链混合，而不是 `EXECUTION_PIPELINE_REGRESSION`。

## 14. World Engine Verdict

`EARLY_WORLD_ENGINE_HEALTHY`

这是早期健康信号，不代表长篇世界引擎已经全部验证。当前已经看到资源控制、社会依赖、制度流程、NPC 独立行动和规则造成的社会后果。

## 15. 系统层判断

`EXECUTION_LAYER_FIX_NEEDED`

原因是：

- Frozen 上游承诺已经进入正文；
- World Vision、Story Program、Outline 与前三章核心推进一致；
- 但 Chapter 1 Director 出现了真实的章节边界漂移，之后由 Prep 和正文回正。

所以不应选择 `UPSTREAM_REGRESSION_FOUND`。需要关注的是执行层的章节边界保持，而不是重新打开 Fantasy Seed、World Vision、Story Program 或 Outline。

## 16. 是否有足够证据重新打开 Frozen 上游

否。

当前证据反而支持继续保留 Frozen 上游：

- 核心幻想在正文中已成立；
- 主要世界规则已具体化；
- 长期发动机已转化为事件循环；
- 三章真实可读；
- World Engine 早期信号健康；
- 历史 attractor 未整体复现；
- Chapter 3 的未完成资产回收属于当前场景的开放状态；
- Chapter 1 Canon 资产记录不完整是状态快照问题，不足以推翻上游设计；
- Chapter 1 Director 漂移已经被 Prep 和正文纠正，属于执行层问题。

## 17. 对总问题的清晰回答

能。

当前冻结 TheGreatNovel 在脱离历史实验和 GBrain 后，已经证明它可以从极简方向独立长出一部前三章实际可读、核心承诺保留、具备成熟男频长篇潜力的新小说；但当前结论是 `PROMISING`，不是已经完成对整部长篇成熟度的最终证明。后续需要继续观察资产是否兑现、一级成长是否持续由主角本人承担、世界规模扩大后是否仍保持主角行动性，以及 prose 是否能降低设计化解释。

## 18. 本轮边界声明

本轮没有生成 Chapter 4，没有自动修 Prompt/章节/Canon，没有把 Reviewer 意见反馈回正文。
