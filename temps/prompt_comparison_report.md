# Chapter Prompt 对比报告：Chapter Runtime Lite v1（修改前 vs 修改后）

- 仓库/分支：c:\dev\tgn-story-mvp / principal_dev_new_sys；Python 3.13.13（.venv）
- 采集脚本：修改前 temps/gen_baseline_prompt.py；修改后 temps/gen_after_prompt.py（由基线脚本复制，仅输出文件名不同，**10 项固定输入逐字一致，无任何输入变化**，`generate_prompt(mode="chapter", ...)` 签名未变，无需微调）
- 产物：temps/baseline_chapter_prompt.md（修改前）、temps/after_chapter_prompt.md（修改后）
- 度量脚本：temps/measure_prompt_blocks.py（区块级字符数均为该脚本实测）

## a. 字符数总量

| | 字符数 len()（Unicode） | 相对基线 |
|---|---|---|
| 修改前（baseline） | 19746 | 100.0% |
| 修改后（after） | 18900 | 95.7% |
| 差值 | **-846** | **-4.3%** |

净差值小的原因：删除的重复职责约 2400+ 字符，但同时新增了权威标签区块（AUTHORITY 365、CHAPTER MISSION 重组 +166、OPTIONAL INSPIRATION 声明等），且两份 Prompt 的主体正文上下文（前两章正文 4868、十章计划 2254、GBrain/Reference 5052、BOOK 画像 §0—§10 2912）按任务要求**逐字保留、未做任何机械截断**。

## b. 删除的重复职责（均为基线实测字符占比）

| # | 删除项 | 基线字符数 | 占基线 | 说明 |
|---|---|---|---|---|
| 1 | `## 串行写作协议`：Writer A→B→C 串行调度、SUBAGENT_MODE actual/simulated 报告规则、A/B/C 各自职责段 | 1212 | 6.1% | 整块删除；其中三标题输出合同部分被改写为单 Writer 版本保留（见 c） |
| 2 | 合同 `## Writers`：Writer A — Scene Draft / B — Continuity / C — Prose Realization 三份职责定义（与 #1 中 A/B/C 分工构成双份复述） | 402 | 2.0% | 删除；职责压缩为 CHAPTER MISSION 中一句「单 Writer 职责：…直接写出可提交的正式正文，不把小纲扩写成更长概述」 |
| 3 | 合同 `## Scene controls`（通用场景控制段） | 307 | 1.6% | 删除；与模板「连续性优先/选择性展开」及 BOOK prose profile 重复 |
| 4 | 合同 `## Diction and sentence realization`（通用遣词造句段） | 390 | 2.0% | 删除；表达控制统一由 BOOK §7—§10 prose profile 承担 |
| 5 | 合同开篇段对权威层级 + 八字段清单的复述（「已批准的前文正文是已发生事实的最高来源…八个字段——触发事件、…」） | 282→约150 | 1.4% | 删除复述；权威层级改为 AUTHORITY 区块只注入一次，八字段只在 CHAPTER MISSION 投影一次 |
| 6 | SUBAGENT_MODE / provenance 分离条款（基线出现 2 处：串行协议 + Output boundary） | 随 #1、#7 删除 | — | 修改后 0 处 |
| 7 | `## Output boundary` 中「遵守调用方已有的 chapter response contract：…SUBAGENT_MODE 和 provenance 分离」 | 207→234 | 1.0% | 多 Writer 条款删除，改写为单 Writer 三标题合同（区块本身保留） |

合计纯删除约 2311 字符（#1—#4，占基线 11.7%）+ 合同开篇缩减约 130 字符。

说明（如实呈现）：「不自动修改 BOOK」在基线中只出现 1 处（合同 Output boundary），模板中的「不要替作者写入文件」是另一职责表述，修改后两处均保留，本项无重复可删；「连续性优先」「选择性展开」在模板与合同 Continuity 段仍存在轻度重叠，本次未做删除。

⚠️ **附带误删（见 d 后「红牌项」）：基线模板中的命名规则（「前 3—10 章不要默认给所有功能角色正式名字…」，76 字符，占 0.4%）位于 `## 串行写作协议` 区块内，被 sanitize_chapter_template 随区块整体跳过而丢失。**

## c. 保留的权威信息（逐项确认）

| # | 权威信息 | 修改后位置 | 字符数 | 核对结果 |
|---|---|---|---|---|
| 1 | 权威层级与冲突处理 | `## AUTHORITY——权威层级与冲突处理（最小权威规则，仅此一份）`：CANON > PLAN > PROSE PROFILE > INSPIRATION 四级 + 冲突必须写入 Writer Audit | 365 | ✅ 比基线更结构化，且只注入一次 |
| 2 | 八字段事件合同投影 | `## CHAPTER MISSION——本章事件合同（PLAN）`：六项必须落实 + 「推动事件的人」为场景上下文 + 「叙事功能」为规划备注（planning note） | 476 | ✅ 八字段全部进入 prompt，职责分层更明确 |
| 3 | 前两章正文 CANON | `## CANON——前文正文（已发生事实的最高来源）`：第2章+第3章全文 | 4878（基线 4868，+10 为区块标签） | ✅ 正文逐字一致 |
| 4 | BOOK 设定 §0—§5（成长基因图、类型承诺、世界观、压力、主角、配角） | `## CANON——已确认设定、状态与摘要（已经发生，不得修改）` | 2306 | ✅ 逐字一致，且从「执行相关画像」升格为 CANON 标签 |
| 5 | 摘要/状态（当前状态与未兑现承诺 470 + 最近 1—3 章摘要 336） | 同上 CANON 区块 | 806 | ✅ 逐字一致 |
| 6 | prose profile §7—§10 | `## PROSE PROFILE——BOOK §7—§10 软表达控制` | 606 + 标签 | ✅ 逐字一致，与 CANON 分离并声明软控制地位 |
| 7 | 滚动计划（当前大型剧情块 271 + 当前十章计划 2254） | `## PLAN——滚动计划（尚未发生的当前意图）` | 2525 | ✅ 逐字一致 |
| 8 | GBrain Inspiration Results（8 条真实返回）+ 三个 VALIDATED Reference Programs | `## OPTIONAL INSPIRATION——可选参考（不得覆盖 CANON 或 PLAN）` + 可选参考声明 | 5194 | ✅ 内容逐字一致。注：chapter 模式 GBrain 上限 2 约束的是 retrieve_gbrain 检索路径；本固定输入按 baseline_inputs.md 第 8 项约定走作者 textarea 真实返回，不属于丢失 |
| 9 | 连续性优先 / 选择性展开 / 三标题输出合同（# Writer Audit、# 正式正文、# 章节事实摘要）/ 「不要替作者写入文件」 | 模板区（单 Writer 改写版三标题合同 + 运行期声明 SINGLE_WRITER_RUNTIME_NOTE） | — | ✅ 保留，三标题合同改为单 Writer 语义 |

## ⚠️ 红牌项：修改后丢失的基线权威信息

**【红牌】命名规则丢失。** 基线模板 `## 串行写作协议` 区块内的这一行在修改后 Prompt 中完全消失：

> 前 3—10 章不要默认给所有功能角色正式名字。只有会复现、会形成关系、会影响后续或作者明确保留的角色才命名；已经建立的重要角色不得被机械改成身份称呼。

- 原因：`sanitize_chapter_template` 遇到标题 `## 串行写作协议` 后整块跳过直到下一个同级/更高级标题，该行虽不含 Writer A/B/C 字样，仍被连带删除。
- 影响：当前书 real-exp-001 使用书级 PROMPTS.md 模板（本书模板中命名规则只存在于这一处），第 4 章起写作将失去该约束；生产默认 DEFAULT_PROMPT_TEMPLATES["chapter"] 虽含同款规则，但对该书不生效。
- 建议：把命名规则从被跳过的串行协议区块中抢救出来（例如在净化器跳过区块时保留该行，或把它移入模板「选择性展开」段/运行期合同），本报告不做代码修改，留待负责人处理。

除此之外未发现其它权威信息丢失。

## d. 普通章节主写作 pass 数

| | pass 数 | 依据 |
|---|---|---|
| 修改前（理想路径） | **3**（Writer A Scene Draft → B Continuity & Realization → C Prose Realization，串行不得并行） | 基线模板「## 串行写作协议」+ 合同「## Writers」 |
| 修改前（实验实况） | **6**（第一轮 A→B→C 因未把 GBrain/Reference 注入子代理作废，整轮 provenance correction pass 重做 A→B→C） | EXPERIMENT.md：「第一轮本次重跑的 A→B→C 消息没有把本次 GBrain/Reference 文本显式注入子代理…随后执行了 provenance correction pass」；第 1 章合计 6 个串行 pass，第 2—3 章同 task 六个串行 pass |
| 修改后 | **1**（单 Writer 直写） | 修改后模板首段「本次为单 Writer 直接写作…不模拟多 Writer 串行稿件」+ 运行期声明「任何多 Writer 协议已被本运行合同取代」+ CHAPTER MISSION「单 Writer 职责：…直接写出可提交的正式正文」 |

即理想 3→1（-67%），按实验实况 6→1（-83%）；同时消除「中间稿注入遗漏导致整轮重做」这类 provenance 返工的结构性诱因（上下文一次性注入权威标签区块，无需向多份子代理分别传递）。

## e. 结构差异摘要（区块级前后对照）

| 修改前区块（字符数） | 修改后区块（字符数） | 变化 |
|---|---|---|
| 系统角色开场（287） | 系统角色开场（287） | 逐字一致 |
| 连续性优先（188）+ 选择性展开（170） | 连续性优先（188）+ 选择性展开（170） | 逐字一致 |
| 串行写作协议（1212，含三标题合同与命名规则） | 单 Writer 三标题合同（约280）+ 运行期声明（约40） | 重写；命名规则误删（红牌） |
| 合同开篇段（282，复述权威+八字段） | 合同开篇段（约150，委托 AUTHORITY） | 去复述 |
| Authority and profile（266） | AUTHORITY（365）+ Prose profile 地位（304） | 拆分升格 |
| Writers（402） | —（并入 CHAPTER MISSION 单句） | 删除 |
| Scene controls（307）/ Diction（390） | — | 删除 |
| Output boundary（207） | Output boundary（234） | 去 SUBAGENT_MODE/provenance |
| 本书执行相关画像：§0—§5（2306）与 §7—§10（606）混排 | CANON——已确认设定（§0—§5 + 状态摘要 806）/ PROSE PROFILE（§7—§10，606） | 按权威分域贴标签 |
| 当前大型剧情块（271）+ 当前十章计划（2254） | PLAN——滚动计划（2525） | 内容逐字一致 |
| 当前章具体小纲（310，八字段平铺） | CHAPTER MISSION（476，六项合同+场景上下文+规划备注） | 重组升格 |
| 前两章正文（4868） | CANON——前文正文（4878） | 正文逐字一致 |
| 最近 1—3 章摘要（336）+ 当前状态（470） | CANON——已确认设定、状态与摘要 | 并入 CANON |
| GBrain Results（1358）+ 选中的 Reference Programs（3694） | OPTIONAL INSPIRATION（5194，含可选参考声明） | 内容逐字一致，降级声明为可选 |

结论：修改后 Prompt 在完全保留全部正文上下文与权威信息的前提下，删除了多 Writer 串行协议、三份重复 Writer 职责、通用 Scene controls / Diction 段与权威/八字段复述（约 2440 字符，12.4%），主写作 pass 从 3（实验实况 6）降为 1；唯一缺陷是净化器连带误删了模板中的命名规则一行（红牌，待修复）。
