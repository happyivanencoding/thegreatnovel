# Experiment Protocol

TGN 的实验不是为了“证明我们喜欢的方案正确”，而是为了把系统问题从文学直觉变成可归因证据。

## 1. 先写 Hypothesis

实验前用一句话写清：

> 如果只改变 X，那么 Y 应该怎样变化；如果 Y 不变，说明 X 不是主要原因。

避免一轮同时改变 World、Prompt、GBrain、模型、Schema 和 Selector。

## 2. Freeze Baseline

保存：

- baseline artifact；
- prompt；
- model / reasoning；
- GBrain snapshot（Pages / Chunks / Embedded）；
- retrieval bundle；
- 关键输入 hash（必要时）；
- 当前 git commit。

如果 baseline 本身已经不可复现，先承认实验只能做 directional evidence。

## 3. One Main Variable

优先单变量：

- same World, different Human GBrain；
- same Character, different Story Program field schema；
- same Scene, Prose Control OFF vs ON；
- same Prompt, different model；
- same source evidence, different retrieval allocator。

如果必须有两个变量，说明为何不可分，并把结论限定为组合效果。

## 4. Fresh Context for Causal Isolation

测试 authority independence / rationalization 时：

- 新 session；
- 不带上游隐藏信息；
- 不允许模型通过 prompt history 猜另一个 seed；
- deterministic projection 优先；
- 不让后续 Composer 回头重新合理化。

### Premise Search / Creative Voltage Test

测试“系统为什么想不出大胆设定”时，不要只把 World Prompt 写得更激进，也不要默认多 Agent 发散更好。最低证据链：

1. 冻结同一批 2—3 个作者方向与既有 production baseline；
2. A：一个 fresh-context 模型一次生成 3 个完整 premise candidates；
3. B：多个隔离轴分别生成组件，再由代码预注册配对；
4. 模型、effort、作者方向和评价问题一致；不把 benchmark 作品的角色、专名或具体能力喂给模型；
5. 预注册一个同位候选做真实 downstream preservation，同时报告整个 pool，不在看完结果后只挑最好的一张；
6. 先人工读 `Shelf Promise / Changed Verbs / First-Chapter Image / Immediate Payoff / Long-Form Runway / Cognitive Load`，需要汇总再做独立 casewise blind review；不要把多个 case 放进同一 Judge 上下文造成串扰；
7. treatment 通过上游后，必须接回真实 `World → Power / Human → Character → Story → Outline`，分别审 lane isolation 与 semantic fidelity；出生、Power coverage、root boundary 或 stable interface 被静默增强/削弱，不能 PASS；
8. 候选在作者选择前必须提供 `Authority-Compilation Trace`，但同一 Forge 的自我证明不能视为证据；再用 fresh-context Premise Compiler 逐项重查开篇动作的来源、trigger、目标／载体／出口／见证者、Interface 因果、T0 公共尺与远期复合。Compiler 只审可满足性，不评分、不排名、不改稿、不自动 selector；激进或主角占便宜大本身不是错误。预注册候选若 FAIL，应在 World 前停止并如实报告，不能换更好样本冒充 downstream PASS；
9. 如果 direction-only projection 漂移，只做近单变量修复：对同一已选 candidate 使用 lane-specific frozen contract，重跑最早失败链；不要换一个更好 candidate 冒充修复；
10. Frozen contract 仍不是第四 Authority：World 只见 World + protagonist-blind interface，Power 只见 Ontology + Initial Scale Position + trigger/target/action/carrier/boundary，Human 只见 Ontology + T0 origin + Initial Scale Position，Story 在 Authorities 批准后才见完整 Promise。无法同时成立时必须 fail loud；这证明边界有效，不自动证明候选可上线。Outline 不再读取 raw card。
11. Compiler FAIL 默认停止并把精确冲突交给作者，不自动启动 repair loop。若单独研究 Selected Premise Repair，只允许预注册候选的一次近单变量修复；代码逐字锁定标题、Shelf Promise、literal Ontology、Changed Verbs 与不可磨平项。先过 deterministic protected-core validation，再允许 fresh Compiler；失败不补字段、不换候选、不进入 downstream。
12. 冻结为 production 前追加状态机回归：`not_started / skipped` 允许原链；保存候选后所有下游 Authority 必须阻塞；batch / selected Compiler Prompt 生成时立即保存 exact Input snapshot，报告保存不得重新取当前文本；strict PASS + snapshot 与当前 selected card 完全一致 + author approval 才能生成四条 lane contract；编辑后必须 selected recompile；World 批准后不可改 Premise；Workflow 只登记 `premise.contract`；raw card 不进入 Outline / chapter / State。

若完整 premise pool 稳定胜出，而多轴碰撞产生概念竞争，结论应是“搜索需要完整承诺 + 作者门控 + 后置 frozen contract”，不是“取消 Authority separation”。各题材最优强度不同时保留作者选择，不建立自动 conservative selector。

## 5. Cheapest Adequate Model

模型不是越强越好。

- 用 Luna 做大量上游候选与 A/B；
- Terra 用于正文、fidelity 或高精度 bounded extraction；
- Sol 只用于真正需要长期多线程结构整合的高杠杆节点；
- Judge 不是默认必需。

如果实验问题只靠 deterministic code 能回答，不调用 LLM。

## 6. Direct Reading Before Metrics

先读具体输出，问：

- 到底哪里变了？
- 变好来自哪一句/哪一结构？
- 有没有新的副作用？
- 是否只是更长、更会解释？

自动指标只辅助验证，例如：

- leakage hit；
- abstract-term density；
- tool/professional vocabulary；
- repetition；
- schema completion；
- token/cost。

指标不能替代文学判断。

## 7. Judge Only When Needed

以下情况可用 blind judge：

- 两版都成立，细微 prose quality 难人工稳定判断；
- 多场景比较需要汇总；
- 需要隔离作者知道 treatment 的偏见。

以下情况不需要 Judge：

- 明显 named hook leakage；
- Schema 越权；
- Power 与 Biography 逐项押韵；
- 一版直接缺关键剧情；
- 两边输入完全相同。

## 8. No Cherry-Pick

如果一批生成4个 candidate：

- 不因为最好的一张很好就宣布 generator PASS；
- 也不因为一张普通就宣布架构 FAIL。

分别判断：

- architecture 是否允许健康分布；
- distribution 是否坍缩；
- candidate 本身是否商业上值得选。

“架构 PASS，候选4较弱”是健康结论。

## 9. Character Authority Invariance

当 Treatment 可能改变主角取舍、路线优先级或长期效用函数时，不只测一个人物。

默认冻结至少 2—3 个动机排序明显不同的 Human，例如力量第一、具体关系可改路、认可/新鲜感混合型，并对每个 Human 做同一 A/B。

分别验收两件事：

1. Treatment 是否真的产生目标结构增益；
2. 关键选择是否仍随 Human 改变。

如果不同 Human 被 Treatment 推成同一种“成长最优”“关系最优”“道德最优”路线，即使结构更整齐，也应 FAIL 或降级。反过来，保留人物差异本身也不能证明机制有效；结构增益与 Character Authority Invariance 必须分开判断。

## 10. Matched Decision Point

要验证 `Personality → Choice → Route`，先让不同冻结 Human 面对**同一个具体诱惑 / 冲突 / 机会**，只比较选择是否随 Human 分叉；再放开 Story Program，观察不同选择是否长期长成不同路线。

对每个被测 Human，决策点都应至少包含两个具有真实私人价值、且不能同时完整取得的方向；价值来源与强弱可以不同。选择之后，未选路线的主要机会成本必须真实保留；不能马上用隐藏奖励、事后证明“其实这条路更赚”或等价补偿把代价抹掉。否则测试到的只是伪选择，不足以证明 Character Authority。

如果人物、触发事件和机会池同时变化，只能证明“生成结果不同”，不能把差异纯归因于人格。Matched Decision Point 只用于因果识别，不要求 production 把所有人物放进同一剧情。


## 11. Information Release / Realization Causal Trace

当实验目标是“世界信息进入正文”或“压缩实施细节”，不要直接做一轮大而混的全文 rewrite。优先逐层冻结：

1. 同 World / Story / Canon，先比较 release scheduling 是否正确；
2. 冻结 Outline / chapter result，检查 runtime 是否真的传入当章 safe world fact；
3. 冻结 Director，比较 Curator 是否保留 public fact、是否把已成立 Supporting Skill 降到结果级；
4. 最后才在同 Curator 输入下比较 Primary realization。

某一层失败就保留该产物为 evidence，不继续让下游“救”。如果 Writer 仍扩写，再把残余明确归因到 realization，而不是回头重写 World。

对 reveal 单独做泄漏检查：**World 已知但 Future Plan 仍安排后续发现的答案，在揭晓前不得因为 Reader Orientation 被提前投放。**

## 11A. Progressive Canonization Experiment Protocol

当实验目标是验证“作者自己暂时不知道答案、到关键节点再逐层定真”，不要只测 Reframe Prompt 是否会想出漂亮答案。至少走一轮真实 `OPEN → decision → fixed-hidden → pre-reveal chapter → reveal chapter → State → deeper OPEN`；准备冻结 production 时优先做**同一 Mystery 两轮循环**。

最低实验纪律：

1. 使用一个没有参与规则形成的 holdout Mystery；discovery case 只用来提出 hypothesis，不再承担最终验证。
2. 预注册至少一个应 `DEFER` 的 checkpoint：当前具体故事即使作者不知道答案也能继续。若模型因为规划完整度、章数或“迟早要解释”要求定真，判方向错误。
3. 再预注册一个**作者批准的具体未来事件**，该事件如果没有某一最小答案就无法定义动作结果；这时 Decision Surface 才应 `DECISION NEEDED`，并只指出 `Smallest Decision`。
4. Reframe 候选 R1/R2/R3/D0 中提前固定一个 selected ID 做 preservation；Compiler FAIL 不换更容易通过的候选。若 Compiler 合同本身暴露语义悖论，可做近单变量修正，但必须对**同一候选**复验并保留旧失败 provenance。
5. Compiler 必须区分：旧 AUTHOR OPEN unknown pool、当前 Smallest Decision、候选的新 `What Remains Unknown`、已发生 Canon、Author-Approved Future Direction。Future Direction 授权未来事件，不等于过去已经发生。
6. Hidden Fixed Point 必须通过 runtime-blind transport。至少完整跑一个 pre-reveal `Director → Curator → Primary → Reviser → State`，独立审计 Prompt 与最终正文都没有 raw Hidden Truth / 等价答案泄漏。
7. Reveal 章也跑完整章节链；Writer 只能得到 reader-facing Event Atom / Residue / Still Open。独立审计同时要求：Allowed Reveal 真正发生、raw Hidden 未出现、更深 Still-Open 未被顺手回答。
8. State 必须只把 reader 已经历的一层写成 Canon；随后 deeper Mystery 重新 OPEN。第二轮局部定真不能推翻第一轮已揭事实，只能 backward-compatible reinterpretation / expansion。
9. 两轮之后再安排一个不依赖终极解释的现实后果阶段；如果仍能继续写，Decision Surface 应重新允许 `DEFER`。这证明机制不会沿解释惯性把整个宇宙一次补完。
10. 如果 Mystery treatment 可能改变人物路线，至少用两个 motive ordering 明显不同的 Frozen Human 做 matched Story Refresh；共同 Reveal 可以相同，但关键选择/机会成本必须随 Human 分叉。
11. 任何章节提取、时序、cache、审批 self-gate 等实验 helper 错误都会使其依赖产物 `INVALID`；保留原始 artifact 并从最近有效 checkpoint 恢复，不能把修正后的结果覆盖旧失败伪装成一次成功。

冻结时分别报告：Decision 命中、固定候选、Compiler、Human invariance、pre-reveal leak、Reveal realization、State Canon、第二轮兼容、final DEFER，以及研究调用总成本。Production 成本必须另算；低频 author-gated calls 不能被误报为每章税。

## 12. Verdict Vocabulary

### PASS
主要假设被真实输出支持，副作用可接受，可冻结/上线。

### DIRECTIONAL PASS
方向正确，但证据量、live treatment 或覆盖不足；可以保留机制，不应宣称问题完全解决。

### PARTIAL PASS
解决一个子问题，同时暴露独立残余问题。不要把残余重新归咎于已通过架构。

### FAIL
核心 treatment 没产生预期变化，或副作用抵消收益。

### INVALID / CONFOUNDED
实验变量不干净、输入不同、selector 偷选、GBrain 中途变化、baseline 不一致。不得用来冻结系统结论。

## 13. Always Record What It Did Not Solve

每个通过实验都写：

> What This Did Not Solve

例如：

- Split Seed 解决 Power↔Biography 合理化，不自动解决 Human appetite distribution；
- Private Appetite Continuity 减少职业化，不自动产生好胜/虚荣/战斗欲；
- lane cap 解决检索配额，不凭空创造 Behavior/Relationship ACTIVE craft；
- prose texture 改善场景质感，不修 Story Program 的剧情同质化。

这样下一轮不会回头破坏已经验证的层。

## 14. Code Experiment Safety

修改 production code 前：

- `git status`；
- 记录 protected uncommitted files；
- 不覆盖其他 agent 工作；
- 新实验优先放独立目录；
- 实现后 focused tests；
- full suite；
- `git diff --check`；
- stage 白名单或自己的 hunks；
- 再 commit/push。

不要因为旧测试失败就恢复已经明确废弃的架构。先判断测试是否属于 legacy expectation。

## 15. GBrain Experiment Safety

涉及 GBrain 时记录：

- before / after Pages；
- Chunks；
- Embedded；
- `Embedded == Chunks`；
- accepted / rejected cards；
- active vs reference-only；
- retrieval regression；
- unrelated negative queries。

如果蒸馏仍在跑，不把 staging / materialized 文件当 live GBrain treatment。

## 16. Latency / Cost Causal Audit

当用户说系统“慢、贵、调用太多、某节点像累赘”时，先做真实账目，不按 Prompt 长度、最终相似度或主观等待感直接删层。

必须分开记录：

1. **Adopted node wall**：最终采用链每个节点的 wall-clock；
2. **Actual batch elapsed**：废弃重跑、replan、周期 Review、repair、fallback、失败重试与中断都单列；
3. **Upstream amortization**：开书 World/Character/Program/Outline 等低频成本，不混成每章常态；
4. **Execution tax**：backend、cwd、独立 session 数、系统上下文、input/cache/output/thought tokens 与 queue 波动。

每个节点至少保存 model、effort、prompt chars、input/cache/output/thought、wall、adopted/fallback 状态。Cache 降低费用不代表消除串行推理；一次异常快/慢也不能直接归因于 Prompt。

先区分两类 treatment：

- **Deterministic removal**：文本自身已证明 stale、重复或越界的上下文，可以在最早边界删除并做结构测试；
- **Semantic route change**：降模型/effort、删节点、Patch-only、条件 skip、Slim contract 或新增 classifier，会改变判断能力，必须视为 Experimental Hypothesis。

语义路线 A/B 的最低标准：冻结上游与 Chapter Mission，只改一个变量；Treatment 接回正常 downstream；比较**最终正文**而非 Curator/Audit 中间包；至少同时做商业 Reader 与 Authority/Canon blind。高 Primary↔Reviser 相似度只说明多数句段被保留，不证明少数关键 Authority recovery 没价值。

对以下 treatment 追加更高证据要求：

- **随机稀疏修订 / Paragraph Delta**：同一冻结输入至少独立运行两次，报告修改段落与最终正文的 exact consensus；一次好结果不能替代 repeatability。
- **提前编译 / Attention Kernel / Pre-Curator**：既审编译包，也必须接回实时 Mission binder 与正常 Primary/Reviser；报告摊销后完整 critical path，而不是只报预编译节点。
- **跨章投机 / Speculative Scheduling**：以最终 State 后的 Canon 做 Authority Judge；完整计算 `previous State → current final draft` 的关键路径，并单列 treatment 反而变慢的章节。
- **高潜语义快路**：至少增加一套不同书/世界/人物结构的 cross-book frozen sample；Reader 赢而 Authority 输、或反之，均只能判 PARTIAL。
- **条件 fallback / adoption gate**：必须把前置失败调用、discard、full fallback 与双路并行的总 wall / cost 全部算入；不能只报命中时速度。
- **并行隐藏 polish**：即使不增加 wall，也要报告多次运行触发集合、跨书 NO_CHANGE 率与新增调用成本；低重复性的“偶尔有用”不自动成为常驻 Agent。

不要用新增 cheap Reviewer / classifier 为另一个 Reviewer 决定是否运行，除非它能由 deterministic explicit obligation 取代且总成本、漏报、fallback 已完整计入。优先顺序是：删确定性脏上下文 → 修矛盾合同 → 减少废弃重跑/恢复失败节点 → same prompt / same model 的 execution backend 减负 → 最后才考虑语义降档。

结论必须分别标记：质量结论、wall-clock 结论、成本结论。Direct API、ACP、不同 cwd 或不同 transport 的数字不得互相外推。

## 17. Stop Conditions

以下情况应停止继续加实验变量：

- treatment 没有改变实际输入；
- 已经找到清晰 root cause；
- 下一步只是重复验证同一结论；
- 剩余问题已经属于另一个层；
- 用户目标已达到。

不要为了“实验完整”继续烧 quota。
## Creative Intensity Decision

当多个 treatment 都满足 hard authority / causality，仅在爽感强度、奖励丰富度或主角局部优势上存在 trade-off 时，不由 Steward/Judge 自动向保守版收敛。保留代表性真实输出，并把 AGGRESSIVE / MODERATE / CONSERVATIVE 的关键差异交给作者选择；当前 TGN 默认审美先验偏 AGGRESSIVE。只有事实矛盾、authority 越界、或即时近似补偿抹平真实牺牲可以直接淘汰。

## 17. Atomic Authority / Projection / Local Repair Protocol

当优化方案使用typed Contract、deterministic projection、局部Delta或选择性跳过Full Reviser时，最低证据链为：

1. `Atomic Authority Contract`只从可信Frozen Authority artifacts + Entity Registry构建；`Primary Preservation Map`只管理Runtime签发的evidence、Edit Locality和窄fragment hint，两者不得混成一个Pack。
2. Entity ID与stable slot由Runtime维护；Primary/Curator不能决定Identity、Hard Fact或Source Conflict。
3. 分开报告：registered known-fact recall、完整semantic Contract repeat（含extra facts）、human Mission Story/Authority、Final Story/Authority、cross-book Registry coverage和完整fallback-adjusted wall。
4. `58/58 fixture recall`之类数字只证明预登记事实被命中，不证明模型没有增加额外Hard Fact，也不证明human Mission保留了冲突、欲望、Public Proof、状态、时序和未知边界。
5. deterministic human projection必须单独做跨书Surface污染、内部ID、标点与信息带宽审计；typed Contract正确而Mission错误时，整条Treatment无效。
6. Blind候选必须对称清洗citation、标题和其它route metadata；Judge若能从格式识别路线，该blind无效并重跑。
7. Final Story赢而Final Authority输，或反之，均不能productionize；Full Reviser不能被假设为一定能恢复上游human Mission已经压掉的信息。
8. Native / fallback route必须计入废弃typed调用 + free-text fallback + 全部downstream；0次fallback只能说明当前手工样本，没有证明自动Registry下的production fallback率。
9. independent repeat至少区分raw decision、normalized decision、artifact hash、semantic Hard Fact set、human Mission与Final Draft；逐字不一致不是自动失败，但Hard semantic set不稳不能成为Gate Authority。
10. 速度结论用fresh adjacent Control、完整critical path和多轮均值；Runtime毫秒级投影不等于模型Director更快，单轮快而另一轮慢不能宣布节约。
11. 后续 rich-Mission bypass E2E 进一步否决“Authority Gate PASS即可跳Full”：冻结fresh route为0/8 bypass；对7组Oracle-safe Primary/Reviser pair做两轮匿名复核后，Story为Primary 4胜/Reviser 10胜，Authority为Primary 1胜/Reviser 8胜/5平，0/7稳定质量等价。**Contract closure ≠ Reviser necessity**；如果Full Reviser已在真实pair中证明同时增加Story与Authority，就必须先让Primary稳定达到其输出水平、使Reviser趋近no-op，再谈skip。
12. LLM Oracle只能做研究归因，不能成为production bypass classifier；本轮Oracle PASS仍漏掉旧价格、路线人员归属、Reader Release和actor-object chain等具体错误。不要新增中文Parser、LLM safety classifier或常驻Reviewer来修另一个Reviewer。
13. **Reviser-noop / effort downgrade 必须使用新小说 held-out。** 旧书Primary→Reviser pair只允许derivation；Treatment必须在held-out World/Power/Human/Story/Outline生成前冻结并保存hash。正式判断用新书连续章节，不读结果后挑章；若held-out失败，不得回头调Treatment再把同一本书继续叫held-out。
14. `Primary更好`、`Treatment Final更好`、字符similarity上升、或单个Reviser wall下降都不等于no-op。至少同时报告 `Primary→Reviser` 的Story signed gap/距0、Authority gap、Hard-problem count、edit blocks、exact no-op、independent repeat与Primary+Reviser完整wall。一个projection若Story升而Authority降，应诊断为**attention placement positive / closure negative**，不能productionize。
15. effort screen可以在derivation样本提前淘汰：若Luna medium等候选虽大幅降wall、Story不降，但Authority score / hard problems仍稳定弱于high，立即停止，不用第三本held-out“找容易样本”。只有derivation先接近high，才冻结新Watch/Projection并进入下一本全新held-out。
