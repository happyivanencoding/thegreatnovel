# 通用连续创作质量内核：实验与证据

日期：2026-08-17

这份 artifact 只记录本轮通用内核的可复现证据，不把任何一本实验小说写入生产规则。

## 1. Current Seed 回归

输入是已有的隔离 Seed artifact：

`audit/experiments/v3_10_chapter_continuation_expansion/browser_smoke_20260816`

本轮只读 rehydrate 了 `_system/state.sqlite3`，没有修改其中的 Canon 或正文：

| 检查 | 结果 |
|---|---:|
| `CANON_COMMITTED` drafts | 10 |
| 保留的非 Canon `DRAFT` | 2 |
| Canon commits | 10 |
| validation reports | 120 |
| DraftOutput 新 schema rehydrate | 10/10 |
| ChapterContract 新 schema rehydrate | 10/10 |
| schema failures | 0 |

原实验的盲读报告仍然指出：中段存在“测量—记录—回撤”的体验同构、可见状态矛盾、数量跳变和正文缩水。本轮没有手写第 11 章大纲；这些问题由新增的 ReaderVisibleClaim、ProgressionDelta、结构 portfolio 和 realization baseline fixture 覆盖为可判定的通用失败类型。

## 2. Configured-horizon cross-family vertical slice

运行时从 `config/default.yaml` 读取 `continuation_quality.serial_experience.horizons.SHORT=12`。每个 family 生成 13 个 generic `ChapterExperienceSignature`，并把 `current_chapter` 设为 14，因而实际跨过配置的 near/short horizon 后再多一章。

| family | signatures | SHORT | MID | UNKNOWN | repeated structural pairs |
|---|---:|---:|---:|---:|---:|
| survival/resource | 13 | 12 | 1 | 0 | 78 |
| combat/cultivation | 13 | 12 | 1 | 0 | 78 |
| mystery/relationship | 13 | 12 | 1 | 0 | 78 |

三类数据使用同一个 `build_serial_experience_portfolio`、同一个 `structural_overlap` 和同一个 Usage/Progression 质量函数；生产代码没有 family 分支。78 对重复结构是该合成输入故意保持同一核心方法、回报和结尾动作后的诊断，不是普遍硬门。

## 3. 参数化质量结果

- survival/resource：`RESOURCE_GATED`、数量变化、资源门和行动范围字段通过同一模型。
- combat/cultivation：`COMBAT_SCENE`、技能复用、掌握/升级/突破差异通过同一模型。
- mystery/relationship：`ONE_TIME`、知识/关系轴和结构变化通过同一模型，不要求资源或战力字段。
- 另有 `DAILY` 参数化测试；章节边界不会隐式 reset，合法 reset event 才能解除次数限制。
- Reference provenance 能区分 `UNAVAILABLE`、`ZERO_RESULTS`、`NOT_OFFERED`、`OFFERED`、`APPLIED`、`OFFERED_NOT_APPLIED` 与冲突拒绝；仅 offered 不增加创新奖励。

## 4. Blind reading boundary

本轮没有重新生成一批新的匿名盲读正文，因此不伪造新的盲读结论。可引用的原 Seed 盲读结果在上面的既有 artifact 中，且只作为暴露问题的回归证据；本轮新增的是确定性发现与跨家族结构 fixture，不是“盲读总分”。

## 5. UI evidence

`tests/integration/test_continuation_quality_web.py` 验证了：无 CSRF 返回 `CSRF_INVALID`；带有效 CSRF 但草稿不存在时返回 `WORKFLOW_ERROR` 且 event 数量不变；Original 与 continuation 页面共同加载 `approval.js`，全静态脚本无 `window.confirm`。
