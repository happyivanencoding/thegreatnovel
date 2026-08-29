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

## 17. Atomic Chapter Obligations / Local Delta Protocol

当优化方案以局部 Delta 替代 Full Reviser 时，最低证据链为：

1. 从 Frozen Authority 确定性编译 typed obligations；禁止让同一个 Delta 模型自报“已经安全”。
2. Hard obligation 至少覆盖 actor-action-object、Direct Result、State Change、Ending、ownership/transfer、money/payment、time、power position/boundary、排程 Reader Release 与 unresolved boundary。
3. 条件义务（Human cue、Public Proof）必须先证明 trigger；未触发写 `NOT_TRIGGERED`，不能当漏项。
4. Commercial value 使用 `PRESERVE_IF_PRESENT`：只检查已有欲望、关系、Reward、Surprise、Social Repricing是否被磨平，不能要求新增。
5. `FAIL / UNKNOWN / CONFLICT / UNSUPPORTED` 任一出现即 full fallback；不得用相似度、修改段落少或模型自信覆盖。
6. 局部应用后必须扫全文闭合，特别检查原件/副本、持有人、付款状态、时间终态、主体换位与后文相反句。
7. calibration同时报告 safe false block 与 bad miss；至少做独立repeat、cross-book与完整fallback-adjusted wall。
8. Reader与Authority任一稳定偏control，都不能productionize。Authority全胜只能证明事实安全，不能证明人物和商业价值没有下降。
9. 当前 compiler若在新领域大量preflight fallback，只能判安全但domain-specific，不能以零漏报宣称泛化。
10. 下一步优先扩 typed compiler 与deterministic residual blocker repair，不新增LLM classifier。
