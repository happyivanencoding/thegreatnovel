---
name: process-novel-handoff
description: 在 Windows Codex 桌面端按 Python 冻结的 Local File Handoff contract 执行业务 Skill；不启动 Codex 子进程、API 或 shell。
---

# Process Novel Handoff

Codex 桌面端是唯一 LLM 执行者。Python workflow layer 决定路由、冻结输入、状态和完成验证；本 Skill 不维护任务类型路由表，也不重新推导已经冻结的协议事实。

## Deterministic start

执行指令会明确提供当前 Web 配置的绝对 `library_root`。必须原样使用该值；不得通过当前工作目录、搜索 `library/`、搜索 `state.sqlite3`、项目 root 或 `MEMORY.md` 推断数据库位置。

对一个已知 `handoff_id`，先运行复制指令提供的 PowerShell 命令：

```powershell
uv run --no-sync novel workflow start --library-root "<复制指令提供的绝对路径>" --book-id "<book-id>" --handoff-id "<handoff-id>"
```

只有命令成功返回 `status=RUNNING` 时才继续。返回中的 `executor_skill` 是唯一业务 Skill 路由，`business_input_files` 是本次业务允许读取的输入。失败返回 `STALE`、`BUSY` 或 `INVALID` 时停止，不自行修复或重算协议。

Python 已在 start 中完成 READY_FOR_CODEX 检查、原子 claim、冻结文件完整性和漂移检查，并保留 `CLAIMED`、`RUNNING` 两个事件。不要再次逐文件计算 hash、比较 projection/registry/config/edition、检查 Canon 数量或推断 allowed paths。

## Business execution

读取 `task.json`，只读取其中列出的 `business_input_files`，然后执行冻结的 `executor_skill`。业务 Skill 负责语义工作、业务 artifact 和业务 result 字段；本 Skill 不执行任何业务语义，也不自行选择另一个 Skill。

业务 `result.json` 只需提交 `completed_stage`、`artifact_paths`、业务结果 ID / 数量以及 Skill 合同要求的其他业务字段。`handoff_id`、`handoff_type`、`book_id`、`edition_id`、`requested_stage`、`status`、`base_event_seq`、`base_projection_hash`、`canon_committed` 和 `edition_activated` 属于 Python 协议事实，由 workflow complete 注入；不得要求业务 Skill 重抄。

不得修改 `book/`、批准正史、批准改写 Campaign、启用 Edition、删除历史草稿或绕过 Validator。业务结果必须停在对应 Skill 合同允许的 Proposal、Validated Draft、Validated Campaign、Source State 或 Reference-only 边界。

## Deterministic complete

业务 Skill 将结果写入 start 返回的 `result_target`（result JSON 路径），然后运行：

```powershell
uv run --no-sync novel workflow complete --library-root "<复制指令提供的绝对路径>" --book-id "<book-id>" --handoff-id "<handoff-id>" --claim-token "<workflow start 返回的 claim_token>" --result-path "<workflow start 返回的 result_target>"
```

complete 一次完成 deterministic envelope 注入、result schema、artifact、运行期间漂移、结果持久化、状态和 `COMPLETED` event。成功结果就是完成权威，不需要再运行 post-verifier。START 的 Frozen Task Integrity 与 COMPLETE 的 Runtime Boundary Drift 是两个不同边界，均由 Python 执行，不能由 LLM 复算。

若 complete 返回 `RESULT_INVALID` 或 result schema / artifact 错误，修正当前 `result.json` 或 artifact，使用同一个 `claim_token` 再次运行 complete；不要重新 start、重新 claim 或创建 handoff。此时 handoff 仍为 `RUNNING`。若返回 `STALE`、`BUSY` 或 invalid input blocker，则按 Python blocker 停止，不自行修复协议状态。

## Protocol boundary

结果只能写入冻结任务目录；业务边界、Canon、Edition、作者批准和 artifact 语义由冻结的
executor Skill 与 Python complete 合同负责，本 Skill 不重复解释或判断。
