# 本轮修复的真实问题

## 1. 人类创作问题被当作 machine tag

- 症状：自然语言 `creative_problem` 会参与 exact metadata tag 匹配。
- 根因：Query contract 没有区分人类描述和机器字段。
- 责任层：Reference Query contract / semantic adapter。
- 修复：加入 `creative_problem_tags`；gateway 只把显式 tags（或安全的旧式 ASCII 单
  tag）传给 deterministic retrieval。
- 回归：`test_query_separates_human_problem_from_machine_tags_and_keeps_legacy_tag`。

## 2. Query 状态不可审计且 CORRUPT 容易退化成空结果

- 症状：未配置、路径缺失、package 损坏、zero result 没有有限状态区分。
- 根因：旧 Response 只有 cards/warnings。
- 责任层：Reference Query gateway。
- 修复：加入 `ENABLED / ZERO_RESULTS / UNAVAILABLE / CORRUPT / DISABLED` 和 package
  schema/hash；Revision 兼容旧 mock warning 时只在 response status 仍为 ENABLED 时映射，
  不覆盖真实 CORRUPT。
- 回归：`tests/unit/test_reference_corpus_query.py` 状态参数化用例、Draft/Revision workflow。

## 3. 操作没有不可变 Reference Context

- 症状：Corpus 更新后无法回答某个 task/plan 实际使用了哪些 card。
- 根因：Query response 没有 operation-level frozen artifact。
- 责任层：Reference context preparation / storage。
- 修复：新增 `ReferenceContextSnapshot`，写入 task/operation input，带 package identity、
  selected ids、count、warnings/gaps 和 hash；已有 task 复用合法 Snapshot，冲突不覆盖。
- 回归：`tests/unit/test_reference_context.py` 的稳定 hash、package 更新冲突、raw 字段拒绝，
  以及 Draft integration。

## 4. Revision 绕过 Novel Prose Realization

- 症状：Revision draft task 没有 Reference PROSE context，也没有共享 prose protocol。
- 根因：Revision draft preparation 只写旧 RevisionUnit/task schema。
- 责任层：Revision context preparation。
- 修复：Impact 完成后接入 PLANNING；Draft task 接入 PROSE；`input.md` 和 Skill 明确复用
  同一个 `novel-prose-realization`，不创建第二套 humanizer。
- 回归：`tests/integration/test_revision_workflow.py`。

## 5. rewrite_required 上游的依赖卡仍可被检索

- 症状：rewrite-required Book DNA 被排除，但活动 downstream card 仍可能返回。
- 根因：semantic retrieval 的 invalid closure 只传播 STALE。
- 责任层：deterministic semantic retrieval。
- 修复：将 `rewrite_required` 与 STALE 合并为 invalid upstream，并传播完整 dependency
  closure；readiness 也暴露 invalid cross-book 依赖。
- 回归：`test_rewrite_required_invalidates_all_dependents`，并保留原有 STALE 依赖测试。

## 6. Original Genesis planning context 被后续 Draft task 覆盖

- 症状：首章 Genesis task 先写入 planning context，随后普通 Draft task 写入同一 operation
  的 `task.json` 时丢失它。
- 根因：同一 operation input 文件有两个连续写入责任点，后写入未合并 planning context。
- 责任层：Original → Draft task handoff。
- 修复：从已确认 Foundation Development handoff 复用冻结 planning context，并在最终
  Draft task 写入后合并 sanitized planning projection。
- 回归：`test_first_chapter_uses_contract_validation_and_explicit_approval`。

## 7. 未配置 Corpus 时 Draft mock/重复 task 的边界不清

- 症状：未配置时 mock query 返回 ENABLED，Draft 误显示启用；同一 task 重准备会试图
  覆盖旧 Snapshot。
- 根因：调用方把 gateway 的可选配置边界完全交给可替换函数，且没有先复用 frozen artifact。
- 责任层：Draft context preparation。
- 修复：未配置时规范化为 DISABLED；已有合法 Snapshot 直接复用，不重查/不覆盖。
- 回归：`test_prepare_draft_reference_prose_context_is_optional_and_compact` 与 Snapshot tests。
