# Findings: Continuation Quality Generalization v1

## Scope and baseline

- 用户任务来自 `C:\Users\jingx\.codex\attachments\f05e82e5-32cd-4198-b5a6-860fe90f3418\pasted-text-1.txt`；它明确要求通用连续创作质量内核、非阻塞批准 UI、跨家族证据和分离提交。
- 当前工作树位于 `continuation-expansion-gbrain-v1`，与 `origin/continuation-expansion-gbrain-v1` 同步起点但存在大量未提交/未跟踪用户改动和运行产物；不能使用 reset/checkout/clean 处理。
- 现有 `.planning/continuation-expansion-gbrain-v1/` 记录上一项 continuation expansion/GBrain 工作已部分实现 Draft compiler、realization brief、experience signature 和 reference fallback，但本轮必须以 live code audit 验证，不能从旧记录推断全部满足。
- 目标分支 `continuation-quality-generalization-v1` 尚未在当前本地 branch 列表中出现；创建前必须审计 ancestry 与 dirty 内容。

## Initial read-only evidence

- 当前工作树根部 `AGENTS.md`、`Novel_Authoring_System_Constitution_V2.md`、`PLAN.md`、`README.md`、`pyproject.toml`、`uv.lock` 和 `findings.md`/`progress.md`/`task_plan.md` 显示为删除；`rg --files` 只在 `audit/final_continuation_report/audit_bundle/instructions/` 找到部分 instruction 副本。必须从 Git 版本、其他分支或审计 bundle 分辨权威来源，最终报告要声明缺失。
- 当前源代码与测试存在修改，且 `workspace/original-e56a54687506/` 等实验状态目录未跟踪；它们是用户既有工作/工件，不能纳入本轮提交。
- 当前可见旧计划中的定向/全量测试通过记录属于上一阶段，不等于本轮通用化验收；需要重新识别 live codepath 和覆盖缺口。

## Required architecture questions

待 Phase 1 用实际代码和历史文档补齐：

1. 读者正文事实在哪一层丢失？
2. 哪些字段由 LLM 创意语义产生，哪些由 Python/Projection 权威维护？
3. Character/Style 当前分数是否测量对应概念？
4. repetition 为什么识别不到换地点不换事件结构？
5. progression 如何区分能力复用与升级？
6. 周期性次数限制如何表达和结算？
7. Reference Corpus 如何证明实际采用？
8. approval UI 阻塞行为来自哪些共享/分支路径？
9. 如何不建立第二套数据库/workflow 修复？
10. 新抽象如何覆盖至少三类小说？

## Design constraints from task

- LLM only at creative/semantic edges; deterministic Python at the center.
- No current-story entities in production `src/`, config or generic templates.
- No fixed `chapter >= 10`/last-three logic; horizons come from Reader Experience, Serial Form, Story Atlas, Book Profile, project config or Scheduler Contract.
- No universal battle/power/loot growth formula; valid deltas may be capability, resource, identity, relationship, knowledge, agency, team, mystery or world scale.
- No embedding/vector database or second state/workflow system.
- Blocking Canon/Timeline/Knowledge conflicts remain hard gates; experience diagnostics are mode-dependent.

## Authority documents read from HEAD

- `AGENTS.md`: Constitution is the highest product specification; `book/` is immutable; new runtime data belongs under `library/<book_id>`; `INFERENCE`/`CANDIDATE`/`PROSE_ONLY`/`SOFT_REFERENCE` cannot silently become Canon; Draft defaults to `VALIDATED`; Python owns facts, state, evidence, hard gates, deterministic metrics, approval, projection and snapshots; LLM owns literary meaning, creativity, semantic proposals and prose; no duplicate Canon/World State/Score/Hard Gate/Payoff/Approval systems.
- `Novel_Authoring_System_Constitution_V2.md`: shared loop is source → canon → reader-state diagnosis → function → causal change → prose → validation → author-approved Canon; type-specific growth is configuration, not universal truth; repetition must compare structure; chapter contracts describe required state changes rather than lines; event store plus projection is the replayable authority; all ten validators and explicit approval remain part of the product boundary.
- `PLAN.md`: system is local/CLI-first, Python does not call remote LLMs, source `book/` is read-only, runtime state is SQLite/event/projection based, no cloud/vector DB/automatic approval, and the existing vertical path is expected to remain end-to-end.
- `DESIGN_VALUES.md` and `MVP_REWRITE_SPEC.md`: not found in current HEAD, Git history name search, or listed branches. This absence is a real audit finding and must be stated in the final report; do not invent their requirements.

## Implications for this implementation

- New continuity claims must be a projection/validation seam over existing Draft/StateChange/Event Store, not a second fact database.
- Any replacement of Character/Style scores must preserve the Constitution's hard-gate intent while making unsupported semantic values explicit as edge review evidence or `UNKNOWN`.
- Horizons such as Constitution's `SHORT/MID/LONG` and user task's `NEAR/MID/ARC` must be resolved from current Book Profile/Serial Form/contract/config, not copied as fixed chapter counts into Python.
- Approval UI can remove a browser confirmation prompt only if the existing explicit author action, server-side stale validation, transaction and Canon boundary remain intact.

## Production anti-overfitting baseline

- `rg` over `src` and `config` found no current experiment identifiers, title, character, prop names, measurement phrase, or book id matches from the task.
- The first fixed-window search found no direct `chapter >= 3/10/50`, `last_three`, or equivalent literal horizon match in production/config. This is only a baseline search; horizon behavior still needs code-path inspection because a fixed value can be hidden behind constants or model defaults.
- The source tree already contains generic-looking `progression`, `serial_kernel`, `planning`, `drafting`, `reference_corpus`, `validation`, and `workflows/approval` modules. The audit must determine whether they are authoritative or partially wired before adding anything.

## Approval UI audit

- `src/novel_authoring/workflows/approval.py::approve_draft` is the shared server-side Canon boundary. It requires the exact approval phrase, `VALIDATED` status, a current validation bundle, contract readiness/ordinal match, immutable source verification, draft content hash match, projection/boundary freshness and a transaction before appending committed events/materializing state.
- `src/novel_authoring/original/service.py::approve_original_first_chapter` delegates to that shared function, then updates Original state/registry. This is the correct semantic path to preserve.
- `src/novel_authoring/web/static/original.js` still has six `window.confirm` calls across reselection, foundation confirmation, proposal replacement and first-chapter approval. The first-chapter approval button calls the shared Original endpoint but blocks before the request.
- `src/novel_authoring/web/static/workbench.js` still blocks edition activation with `window.confirm`; this is not a chapter Canon approval but violates the global no-blocking-dialog search target and should become inline/direct action with the existing server check.
- `src/novel_authoring/web/templates/draft_review.html` explicitly says it has no approval button and only displays a CLI command. Therefore ordinary continuation currently lacks a page-native author click path even though the shared approval service exists.
- There is no general Web POST route for `approve_draft`; only Original first-chapter approval and draft content/metadata writes are exposed. This is the minimum route/UI gap for continuation approval.

## Canon、声明与验证边界

- 唯一发布链为 `DraftStateChange -> validation validators -> workflows.approval.approve_draft -> EventStore/materialize_change -> Projection`；Projection 是查询物化面，不能再建一套 claim/world-state 存储。
- `MATERIALIZATION_REQUIRED_FIELDS` 已覆盖 fact/timeline/character_state/knowledge/relationship/resource/capability/thread/promise；usage constraint 应作为现有 resource/capability 状态变化的结构化 payload，由同一事件链验证和物化。
- `DraftCreativeOutput` 目前允许 prose、state_changes、knowledge/reveal/promises；适合新增显式 `reader_visible_claims`，由 Python 编译 evidence 和验证状态，而不是从散文猜 Canon。
- `ProgressionImpact` 目前只有旧的 `progression_delta_type` 列表，缺少 before/after 和读者可见变化；应增加通用 delta 记录，保留现有合同字段以免破坏当前已用的候选/合同数据。
- 参考库当前已冻结 snapshot/card/solution provenance，但没有 `OFFERED/APPLIED` 语义；仅有 selected card 不能证明候选应用了结构，必须在候选/合同生成时记录状态。
- `ChapterExperienceSignature` 当前只做字段完全相等计数；它不含 opposition source、primary subject、choice/cost/payoff/reader-visible/progression 维度，换名复用会漏报。
- `NarrativePortfolioSnapshot` 已有 SHORT/MID/LONG 线程与 debt 窗口；章节体验历史仍从 drafts 固定 `limit=5` 读取，Boundary 默认最近正文固定 3 章，需改为由配置/合同策略决定。
- 场景实现当前无历史时固定建议 `(1800, 3200)`，且 `diagnose_scene_realization` 只做 warning；应改为从健康 realization baseline/合同 scope 得到软指导，thin 不能成为审批硬门。

## 实现决策

- ReaderVisibleClaim、UsageConstraint、ProgressionDelta 都是声明/验证模型，不是新事实库；只有通过现有 StateChange/approval 边界的记录才会改变 Canon。
- `COMPILED_SOFT` 草稿不再填充伪造 Character/Style score；保留 deterministic measurements、contract evidence coverage 和 `semantic_review_status=UNKNOWN`。`STRICT_LEGACY` 手工 fixture 继续使用原有显式输入。
- usage period 只由显式 `reset_condition`/事件上下文复位；换章本身不复位。`RESOURCE_GATED` 不能超过当前 resource projection，`ONE_TIME` 不能被同一主体重复使用。
- structural similarity 只作为重复结构诊断/候选排序信号，不把一个相似字段变成硬门；真正的 Canon/资源/usage/claim 冲突仍走硬验证。
- 参考库无命中、不可用或冲突时如实记录 `ZERO_RESULTS`/`UNAVAILABLE`/`REJECTED_DUE_TO_CONFLICT`，不伪造 applied。

## Final live-code findings

- `ReaderVisibleClaim` now covers generic entity/state/quantity/location/ownership/capability/knowledge/relationship/temporal/world/agency claims, including `WORLD_STATE`. The validator emits high-confidence conflict findings for projection contradiction, missing subject, missing transition/event, quantity source gaps, depleted capability recovery, and claims outside the current Contract.
- Usage and progression are one shared model path. The parameterized suite proves DAILY, COMBAT_SCENE, RESOURCE_GATED and ONE_TIME behavior; `PERIODIC_USAGE_LIMIT_EXCEEDED` is independent of chapter boundaries.
- `STRUCTURAL_EXPERIENCE_FIELDS` now includes method, opposition, subject, choice, cost, payoff, social/relationship/knowledge/world deltas, scene topology and ending action. Portfolio history is all validated history by default, or an explicit settings/handoff policy; no hidden 3/10/50 window remains.
- `COMPILED_SOFT` output has empty Character/Style score inputs, `UNKNOWN` semantic review status, deterministic measurements and contract coverage. Existing strict hand-authored fixtures retain their explicit-input path only where the repository already supports it.
- Frozen Reference application is now evidence-bearing: selected cards/solutions produce `OFFERED`; candidate summary, valid structural dimensions, changed structure and evidence pointing into the frozen card set are required for `APPLIED`.
- Draft Review and Original first-chapter approval use the page-native shared `approval.js`; no browser confirmation call remains in the approval paths. The server still requires the exact approval phrase and all existing stale/validation/transaction/Canon checks.
- Healthy realization baseline excludes thin/underspecified/unaccepted samples. No-history briefs use `(0, 0)` and underspecified contracts return to planning rather than triggering a universal word-count repair.
- Cross-family unit tests and the configured-horizon experiment use the same production functions for survival/resource, combat/cultivation and mystery/relationship. No current experimental book identifiers were found in `src/` or `config/`.
