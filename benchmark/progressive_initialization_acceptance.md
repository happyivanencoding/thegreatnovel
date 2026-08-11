# Progressive Initialization Acceptance

## Contract

- QUICK、BALANCED、FULL 都建立全书 Source Coverage、Arc 归属和 `structural_index.json`。
- Recall Hint、候选实体和未分析章节没有语义事实权威；未分析章节保持 `UNKNOWN`。
- `StudioReadinessView.ready` 仍只代表 FULL 严格门禁；渐进访问由独立 `StudioAccessView` 表达。
- 续写和改写缺少目标上下文时只创建本地补齐任务，不调用模型、不写 Canon、不批准草稿。
- 升级先恢复未完成初始化；只有已验证的旧结果可以复用，新增 Operation 只包含缺失章节。

## Deterministic fixture evidence

2026-08-11 在 30 章隔离 fixture 上执行三种任务打包；这里只测 Python 结构与文件合同，不冒充 Codex 语义执行。

| depth | 全书轻量索引 | 深读任务章节 | 明确未分析章节 | Python 打包耗时 |
|---|---:|---:|---:|---:|
| QUICK | 30 | 12 | 18 | 0.1031s |
| BALANCED | 30 | 19 | 11 | 0.1057s |
| FULL | 30 | 30 | 0 | 0.1084s |

运行时剩余时间不使用固定分钟数。`status.json.progress` 只有在出现本次实际完成 Arc 后，才根据已观察的 seconds-per-arc 生成估计；没有样本时保持 `null`。

## Automated acceptance

- 渐进初始化、升级复用、按操作补齐、越界 source span 拒绝、Library onboarding、现有初始化与 Metric Bootstrap：22 passed。
- Ruff：通过。
- `node --check src/novel_authoring/web/static/library_catalog.js`：通过。
- `novel initialize create --help` 和 `novel initialize upgrade --help`：通过。

## Semantic evidence boundary

本阶段没有声称完成任何真实长篇的 Codex 语义初始化。真实 Arc Extraction、Entity Resolution、World Model、指标和图谱仍必须由 Windows Codex 桌面端按 handoff 执行并通过现有严格校验；QUICK/BALANCED 不会因此被标为完整 READY。
