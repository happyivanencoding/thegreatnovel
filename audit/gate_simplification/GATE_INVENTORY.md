# Gate Simplification v1：门禁盘点

本清单以 `Novel_Authoring_System_Constitution_V2.md`、当前代码和当前测试为准。
`KEEP_HARD` 只表示失败会改变事实、状态、权限或作者批准动作；评分、完整度、风格
与诊断字段不因为“看起来重要”而升级为硬门。

## 处置规则

| 处置 | 含义 |
| --- | --- |
| `KEEP_HARD` | 失败时阻止当前业务动作，并保留可解释的修复路径。 |
| `AUTO_DERIVE` | 从已经冻结或可验证的事实编译，不让执行器重复提交。 |
| `NORMALIZE` | 只消除同一事实的表示差异；不忽略作者选择、身份或合同内容。 |
| `DOWNGRADE_WARNING` | 保留观察与排名影响，但不阻止规划、草稿或批准。 |
| `REMOVE_REDUNDANT` | 删除没有独立消费者、且不会改变下一步动作的重复校验。 |
| `MOVE_EARLIER` | 把当前阶段才发现的输入/身份问题移到更早的边界。 |

## 当前门禁与目标处置

| 当前代码路径 | 当前行为 | 失败真正阻止的动作 | 处置 | 目标行为 / 验收证据 |
| --- | --- | --- | --- | --- |
| `planning.candidates.prepare_candidate_task` | 读取不到恰好六项指标就抛 `PlanningError` | 规划任务生成 | `DOWNGRADE_WARNING` | 指标 bundle 记录 `COMPLETE/PARTIAL/MISSING`；没有伪造数值；任务仍可生成。 |
| `planning.models.CandidateOutput` | `candidates` 必须恰好 3 个 | 候选导入 | `NORMALIZE` | 目标 3；2 个有效候选即可通过；第 3 个无效不拖垮导入；少于 2 个才失败。 |
| `planning.candidates.import_candidate_output` | 每对候选至少 3 个结构维度不同 | 候选导入 | `DOWNGRADE_WARNING` | 多样性进入诊断/排序；不把软重复变成普遍硬失败。 |
| `planning.candidates._validate_author_control_trace` | LLM 必须提交完整 trace | 候选导入 | `AUTO_DERIVE` | 任务与冻结作者意图由 Python 编译命中/未使用；语义缺失保留为 warning。 |
| `planning.candidates._profile_constraint_failures` | 画像九维和约束检查由 LLM 回写 | 候选导入 | `AUTO_DERIVE` | 画像硬约束仍硬；软契合由系统计算，未知为 `UNKNOWN`。 |
| `planning.candidates._truth_reveal_failures` | 候选必须回写全部 `truth_alignment` 和 `kept_hidden` | 候选导入 | `AUTO_DERIVE` | 从冻结 Truth/Agenda 计算 effective hidden；只对实际越权揭示保留硬门。 |
| `metrics.gates.evaluate_hard_gates` | character 低于配置 minimum 即 `passed=False` | 候选排名/选择 | `DOWNGRADE_WARNING` | character fit 是 warning/排名信号；底线冲突、事实冲突仍硬。 |
| `validation.validators.validate_character` | character fit 低分为 ERROR | Draft `VALIDATED` | `DOWNGRADE_WARNING` | 低分为 WARNING；`character_bottom_line_violations` 仍 FATAL。 |
| `validation.validators.validate_style` | 输入错误/边界字段可阻断 | Draft `VALIDATED` | `DOWNGRADE_WARNING` | 自然度、重复和软风格为 WARNING；作者明确 hard ban 仍硬。 |
| `validation.validators.validate_repetition` | 最近结构完全重复为 ERROR | Draft `VALIDATED` | `DOWNGRADE_WARNING` | 诊断与排序惩罚，不阻止；合同明确 `forbidden_repetitions` 仍硬。 |
| `validation.validators.validate_debt` | 新增重大 hook 超过软计数为 ERROR | Draft `VALIDATED` | `DOWNGRADE_WARNING` | explicit required payoff/advance 仍硬；hook overload 为 warning。 |
| `validation.validators.validate_payoff` | MAJOR payoff 固定要求 4 个 aftershock 和 cooldown 证据 | Draft `VALIDATED` | `DOWNGRADE_WARNING` | payoff 本身及其声明的因果来源仍硬；余波数量/cooldown 是 warning。 |
| `validation.validators._quotes_in_prose` | 引用必须逐字 substring | Draft `VALIDATED` | `NORMALIZE` | Unicode、全/半角标点、空白、引号规范化；唯一命中可通过；多命中 `AMBIGUOUS`；StateChange `NOT_FOUND` 仍硬。 |
| `validation.validators._validate_realized_kernel_trace` | LLM trace 必填，预计/实际软差异可 ERROR | Draft `VALIDATED` | `AUTO_DERIVE` + `DOWNGRADE_WARNING` | Python 从 prose、StateChange、Contract 和 reveal/promise 事件编译 realized trace；LLM trace 只作 hint；非法 StateChange、引用、合同身份仍硬。 |
| `planning.contracts` / `drafting.service` | contract 与 draft 身份由多个阶段重复提交 | Contract/Draft 导入 | `AUTO_DERIVE` | 当前 handoff/task/DB identity 为唯一来源；业务结果不重复提交 task/path。 |
| `planning.candidates._truth_reveal_failures` | KEEP_HIDDEN 由候选回写并比较 | 候选导入 | `AUTO_DERIVE` | `frozen_hidden - actually_revealed` 为 effective hidden；实际 breach 仍硬。 |
| `workflows.handoffs.HANDOFF_DEPENDENCIES` | CONTINUATION/REVISION 把 `metrics` 作为 hard freshness | handoff claim/start | `REMOVE_REDUNDANT` | Canon/projection/source/edition/author choice 仍 hard；metrics snapshot frozen 但刷新不 stale。 |
| `metrics.service.MetricsService._stale_planning` | 作者指标观察会 stale candidate/contract/handoff/aggregate | 已冻结规划/handoff | `REMOVE_REDUNDANT` | 指标重算只刷新 metrics；不改变 Canon/projection 的 handoff 继续有效。 |
| `workflows.handoffs.complete_handoff` / CLI | executor 必须传 result path | workflow complete | `AUTO_DERIVE` | 默认使用 frozen `result.json`；`--result-path` 仅高级显式参数，解析后仍必须等于冻结目标。 |
| `workflows.handoffs.validate_handoff_result` | 业务结果含大量 system-owned IDs/paths | workflow complete | `AUTO_DERIVE` | system 根据 authority envelope 推导 task/candidate/contract/draft/artifact 路径；业务 artifact schema 仍在完成前校验。 |
| `web` Candidate→Contract→Draft action | 旧状态/错误候选可触发后续动作 | 写作任务准备 | `MOVE_EARLIER` | 先验证当前 active planning task 与 selected candidate，再生成 Contract，再 `prepare_draft_task`；身份不一致 hard。 |
| `validation.aliases.resolve_projection_alias` | 资源/实体名称只按 ID 精确匹配，别名可能误报或静默指向错误对象 | Draft 状态校验 | `AUTO_DERIVE` + `KEEP_HARD` | 有可比对 Canon/Projection 时，唯一别名自动映射；无匹配、多匹配或精确/别名冲突明确硬失败；Projection 为空的既有开放集流程保持 `UNKNOWN`。 |
| `workflows.handoffs` runner status | 只有 started time，长任务无 progress heartbeat | runner 回收 | `MOVE_EARLIER` | `heartbeat/last_progress/current_phase` 写入已有 handoff event/state；五分钟无 heartbeat、无产物、无事件才 `STALE_RUNNER_TIMEOUT`；heartbeat 不被回收。 |
| `drafting` / `validation.service` | 手工/元数据修复与正文变更边界不够明确 | 未批准 Draft 修复 | `NORMALIZE` | 仅 prose hash 未变时可修 metadata；清 validation reports、回 `DRAFT`、记录 expected hash/audit；approved/Canon 不可改。 |
| `reference_corpus.semantic.validate_machine_package` | 已有 machine bundle hash 校验 | Reference Corpus enable | `KEEP_HARD` | stored hash 与 cards/dependencies 重算不一致为 CORRUPT；保留现有实现并加回归测试。 |
| `reference_corpus` prompt projection | snapshot 含 provenance，prompt 应只含创作控制 | LLM prompt | `KEEP_HARD` | Full snapshot 只作 audit；executor 只收到脱敏 projection；现有 Original/Revision selector 测试继续通过。 |
| `revision.service` per-unit selector | 已按 unit 暴露 bounded options 并校验 selected IDs | Revision planning | `KEEP_HARD` | 不拼接整套 cards；没有 selector 时才走无 reference fallback；现有 closure tests 作为 PASS 证据。 |

## 不改变的硬边界

以下失败会改变事实、权限或正史，因此不因本轮“软化”而降级：Canon 冲突、静默
retcon、时间线倒置/未知 predecessor、Knowledge 越界、资源守恒/负数/无来源增加、
Capability 越界、作者明确 hard constraint、实际 KEEP_HIDDEN breach、Candidate/Contract/
Draft identity、base event/projection mismatch、必需 artifact 无法解析、Source integrity、
Author Approval、Edition/Revision authority，以及实际 `StateChange` 没有正文证据。

`WARNING` 不是自动批准；Draft 默认仍停在 `VALIDATED`，Canon Commit 仍必须经过作者当前
明确批准。本清单不引入第二套 Canon、评分、Narrative Debt、Payoff、Embedding 或
compatibility layer。
