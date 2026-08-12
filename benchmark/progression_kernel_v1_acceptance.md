# Progression Webnovel Kernel V1 验收报告

## 1. 交付结论

V1 已形成从 Reader Experience 作者确认，到 Genre / Progression / World Expansion / Payoff Contract Proposal，再到章节只读投影、可解释 Scheduler、Candidate 扩展、Genre Drift / Evolution 诊断和 Workbench“成长”页面的闭环。

增补后，PWK 被明确放在 Chinese Serialized Webnovel Kernel 下作为首个、最成熟的 Specialized Narrative Engine。顶层增加 Market Category、Narrative Drive Mix、Engine Protocol、Universal Scheduler 与 Drive Drift；非成长主驱动不创建虚假的 Progression Contract。详见 [Narrative Drive 验收](narrative_drive_kernel_acceptance.md)。

权威边界保持不变：Source / Canon / Author Truth 仍拥有事实；九维 Profile 是 Craft Layer；Preset / Adapter 只产生默认 Proposal；Effective Contract 只从作者确认的 boundary 起约束未来；所有成长状态与期待面均为 Projection。

## 2. 新模型与现有职责

| 新能力 | 复用的现有 Authority | 写权限 |
|---|---|---|
| Reader / Genre / Progression Contract | Original Proposal lifecycle、Author confirmation | 版本化合同表；不写 Canon |
| Progression State | `build_story_game_state` | 无，章节派生 |
| World Expansion / Opportunity | Chapter World State + Atlas soft reference | 无，规划投影 |
| Anticipation | 既有 Debt、Reveal、Thread、Opportunity | 无，投影 |
| Universal Scheduler | 已确认 Drive Mix、Engine 建议、既有 Debt / Author Task / Anticipation | 只保存作者 Override |
| Candidate Progression Impact | 既有 CandidateProposal / ChapterContract | Candidate 层 |
| Genre Promise Reward | 既有 Innovation Reward 的硬门后入口 | 不绕过 Gate |
| Narrative Drive | 同一版本化 Contract 生命周期 | 不按 Market Category 调度 |

没有新增第二套 Candidate、World State、Narrative Debt、Payoff Score、Innovation Reward、Reveal 或 Author Truth 引擎。

## 3. Preset / Adapter / Contract / Runtime

Preset 是作者可覆盖默认值；Adapter 或 DerivedAdapterSpec 把成长语法编译为结构能力；Proposal 等作者确认；Effective Contract 带 `effective_from_boundary`；Runtime 只读 capability 和合同字段，不按 Adapter / Profile 名称安排剧情。

九维 Profile 继续回答“怎样表现”，不能覆盖 Reader Contract 回答的“为什么值得追”。Theme 只能通过成长选择、资源竞争、代价、关系、冲突与世界扩张落地；未经作者改变，不能替换核心 Promise。

## 4. 已知家族与 OOD

四个已知 seed 分别编译为 Cultivation、Team Ability、Cosmic、Occult Sequence；均进入同一种 `ProgressionContract`，但 axis type、topology、resource economy、payoff channel 不同。

三个 OOD seed 均生成 DerivedAdapterSpec：失去未来是 Branching / Sacrifice / Lock-out；城市是 Settlement / Network；灭亡语言是 Knowledge / Mystery / World Expansion，且 Combat Priority 为 Off。完整证据见 [benchmark README](progression_kernel_v1/README.md) 和 [OOD 报告](custom_progression_ood_acceptance.md)。

## 5. 近未来体修 A/B

新流程在 Foundation 前先让作者确认：近未来是 Setting Skin，体修蜕变与战斗验证是发动机，成长与世界扩张为高优先，社会议题为辅助。三个 Foundation 必须原样共享冻结合同，同时在成长来源、资源经济、世界入口、冲突与人物动力上分化。详见 [A/B 报告](genre_drift_ab.md)。

## 6. Topology / Anticipation / Scheduler

Topology 支持 Linear、Multi-axis、Branching、Network、Transformative、Accumulative、Tradeoff，以及 Sacrifice / Lock-out / Rebuild / Transform delta；不要求数字等级或固定“境界”。

Anticipation Surface 只聚合现有期待来源；Scheduler 最多推荐 1 个 primary + 2 个 secondary Intent，并解释 why-now、支持证据、风险和替代。作者 Override 持久化。详见 [Anticipation 报告](anticipation_surface_acceptance.md) 和 [Scheduler 报告](progression_scheduler_acceptance.md)。

## 7. 导入小说与历史章节

导入书从最新可见 ChapterWorldState 中的能力、资源、关系、地点、规则和线程生成保守 `INFERRED_PROPOSAL`；不足字段保持 Unknown。建议合同逐项接受，旧书无合同时仍可正常工作。历史章节严格按 chapter id 投影，不回退 latest，不倒灌未来能力。详见 [World State 报告](progression_world_state_acceptance.md)。

## 8. Browser Acceptance

真实浏览器验收覆盖：Original Step 0、作者调整、合同卡、Topology / World / Resource / State / Anticipation、Candidate Impact / Drift / Evolution、Occult / Team / Imported / Derived OOD。共17张截图在 `benchmark/artifacts/progression_kernel_v1/`，均来自 127.0.0.1:8877 的本地实际 Web 页面；验收专用服务已关闭，用户原有 8766 服务未被中断。

## 9. Tests 与工程门禁

确定性测试覆盖模型验证、Adapter compose、Derived grammar、非人物主体、历史投影、资源证据、非战斗展示债、Anticipation 无 Canon、Scheduler Override、Drift/Evolution、Candidate reward moderation、Legacy Proposal 无 Canon，以及 built-in / OOD benchmark。

最终门禁结果：`314 passed in 272.40s`；Ruff 通过；Mypy 对 179 个源文件通过；compileall 通过；`original.js`、`workbench.js`、`app.js` 的 `node --check` 通过；`novel --help` 和 `novel web doctor` 通过。CI 不运行昂贵的真实 Codex 语义生成。

## 10. 已知限制

1. 原创 Foundation 的真正文学多样性仍依赖 Local File Handoff 与作者人工审阅；确定性层只能验证共享合同、结构字段、数量与边界。
2. Existing Novel discovery 当前复用 ChapterWorldState 的保守截面，不冒充全文最终体系；更完整语义需要 Atlas-first 初始化与 Source State coverage。
3. 当前 Progression State 在没有证据化 axis observation 时显示 UNKNOWN；这是刻意边界，而不是缺省等级。
4. Contract 的可视化编辑器 V1 以逐项确认和 forward boundary 为主；影响历史仍必须进入 Edition Revision。
