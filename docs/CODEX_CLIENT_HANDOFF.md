# Codex Client Handoff

用户使用 Windows Codex 桌面客户端，并通过 ChatGPT Pro 账户登录。本系统不需要 OpenAI API Key，不调用 Responses API，不使用 token 计费模型，也不使用 Codex CLI 作为执行入口。

## Local File Handoff Protocol

Web 创建 `library/<book_id>/editions/<edition_id>/operations/<handoff_id>/`，包含 `input/task.json`、`input/prompt.md`、`input/metric_context.json`、`input/context_manifest.json`、`input/output_schema.json`、`status.json`、`events.jsonl`、`output/result.json` 和 `artifacts/`。所有 hash 在创建时冻结；source manifest、effective content、projection、registry、config、edition status、Atlas/Horizon 或 Planning Aggregate 漂移会使 READY/CLAIMED 任务 STALE，不能覆盖原任务。旧 `workspace/.../handoffs/` 只作为兼容读取路径。

作者在 Codex 桌面端复制 Web 给出的固定指令，先加载 `$process-novel-handoff` 并运行 `workflow start`。当前 start 返回的 `executor_skill`、`business_input_files`、`result_target` 和 `claim_token` 是本次执行事实；Codex 动态调用该 executor，写回业务结果与 artifacts，再运行 `workflow complete`。Python workflow 负责协议、持久化、状态转换和完成验证，Agent 不维护第二份业务路由或 handoff 状态机。Web 只读取 SQLite、状态文件、事件日志和结果文件；SSE（如启用）只传输已有状态，不能控制 Codex，也不能假装知道模型是否仍在思考。没有 heartbeat 时只显示“Codex 客户端可能已停止或等待用户操作”。

项目级 `.codex/agents/novel-handoff-runner.toml` 只提供执行上下文隔离：调用方显式传入绝对 `library_root`、`book_id` 和 `handoff_id`，一次 invocation 恰好处理一个 handoff，随后向父会话返回紧凑摘要并停止。Skill 是持续演化的执行知识与合同，Agent 是上下文边界，Python workflow 是确定性状态权威；业务语义仍完全属于 start 动态返回的 `executor_skill`。

原创小说先使用 `ORIGINAL_READER_INTERPRETATION`：业务输入只有
`original_request.json`，调用 `$interpret-original-reader-kernel` 对 premise 与作者元数据做
Semantic First Read，输出待作者确认的 Reader Experience、Market Category、Narrative Drive
与 Progression Engine Proposal；它不生成 Core Innovation、Foundation 或章节。

作者确认 Reader Kernel 后，再使用 `ORIGINAL_BOOK_BOOTSTRAP`：冻结
`original_request.json` 和 `proposal_schema.json`，调用 `$bootstrap-original-novel`。它依次支持三个 Proposal-only
stage：`CORE_INNOVATION_PROPOSAL` 写三个开放语义机制，作者选择后
`STORY_FOUNDATION_PROPOSAL` 只写三个故事承载方案，作者再选择后
`FOUNDATION_DEVELOPMENT_PROPOSAL` 才写选定承载方案的长期成长、第一阶段、画像、路线与
三个首章候选。三个阶段分别写入 `artifacts/core_innovation/`、
`artifacts/story_foundation/` 与 `artifacts/foundation_development/`，都保持
`PROPOSAL`；Development 还输出复用现有模型的结构化 Kernel Contract Proposals。导入、作者
选择与最终 Genesis 确认是独立动作，只有最终确认才使这些 Contract 成为 `EFFECTIVE`。

业务 `result.json` 必须符合当前 handoff 冻结的 `input/output_schema.json` 与 executor Skill 合同；普通 workflow envelope 由 `workflow complete` 根据冻结协议事实补齐。COMPLETED 还要通过 artifact、edition/hash anchor 和 `status.json` 一致性检查。需要作者决定时，Codex 写 `waiting_for_user.json` 并进入 `WAITING_FOR_USER`；Web 只新增 `handoff_user_response.json`，不修改冻结的 `task.json`。

续写最终停在 `VALIDATED_DRAFT`，改写停在 `VALIDATED_CAMPAIGN` 或 requested stage；`canon_committed` 和 `edition_activated` 必须为 `false`。批准和激活仍由作者显式执行。
