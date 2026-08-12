---
name: initialize-existing-novel
description: 按 capability-specific readiness 初始化已有长篇；优先为当前动作准备 Source Structure、Continuation Boundary 和所需依赖，不修改 book 或 Canon。
---

# Initialize Existing Novel

这是已有长篇进入本系统时的初始化流程。`ingest` 只建立不可变源、章节和 source spans；它不代表理解已经完成。新任务必须使用 `library/<book_id>/editions/<edition_id>/initialization/<initialization_id>/`，路径统一由 `BookLayout` 解析；旧 `workspace/` 只允许 legacy 读取。初始化冻结 source manifest、effective edition、content hashes、输出 schema 和作者指令 hash。

## 初始化深度

- `QUICK`：全书结构索引，并按当前任务选择有限的边界窗口。
- `BALANCED`：在 QUICK 之上优先当前 Arc、活跃依赖和当前续写所需的历史依赖；默认推荐。
- `FULL`：所有有效章节与 Arc 的严格全量语义、综合、指标和图谱；只有 FULL 要求完整历史就绪。

三种深度都必须完整建立全书结构索引。结构候选、Recall Hint 和未分析章节没有事实权威，必须保持 `information_status=null` / `UNKNOWN`。QUICK/BALANCED + `CONTINUE` 只需让当前请求的 capability 达到 `CONTINUE_READY`，即可继续；剩余历史保持 `UNKNOWN` / `NOT_ANALYZED` / pending hydration。不要为了 `FULL` readiness 阻塞当前 handoff。升级时复用可验证的 Arc 输出并只创建缺失任务。

## 阶段

执行 `initialization_manifest.json` 和 `arc_manifest.json` 中真正 scheduled 的阶段，并在 `status.json`、`events.jsonl` 和报告中留下证据。普通 `BALANCED` continuation 初始化的最小顺序是：

`Source Structure -> Current Boundary Window -> Current Arc -> Active Dependencies -> Current protagonist/resource/ability/knowledge/thread -> required synthesis -> CONTINUE_READY`

只有 `FULL` 或任务明确要求时，才继续补齐全书 Arc、Entity Resolution、Cross-Arc Synthesis、Narrative DNA、Semantic Metrics 等历史理解。Visual Rendering 只在显式 `atlas render/export-visuals` 请求时执行。

Python 负责完整章节覆盖、唯一 Arc 归属、边界、hash、schema、稳定 ID、CANON source-span 校验、阈值和状态。Codex 桌面端负责章节/Arc 语义观察、实体别名解释、跨 Arc 关系、Narrative DNA、当前世界模型、未知、反证和未来可能性空间。不得启动 Codex subprocess、API、shell executor 或任何远程模型。

## Arc 合同

从 `arc_manifest.json` 的 `operation_input_path` 读取 `input.md`、`source_manifest.json`、`chapters/`、`output_schema.json` 和 `status.json`。每个有效章节必须恰好属于一个 Arc；默认 Arc 不超过 20 章和配置字符上限。输出写到对应 Operation Workspace 的 `output/output.json`；legacy 初始化才使用初始化目录下的 `arc_outputs/<arc_id>/output.json`。不能覆盖 `book/`。

`CANON` 记录必须包含真实 `source_span_ids`。`INFERENCE` 必须包含 `reasoning_summary`、`confidence`、`counter_evidence` 和 `unknown_boundary`。不确定的别名、冲突和世界规则保持未知或 unresolved，不得用相似字符串自动合并。

## 就绪门槛

- `READY`：仅 FULL 可用；章节 100% 覆盖、Arc 100% 完成、CANON 证据达标、主角与当前边界确认、当前核心图谱齐全且无阻断冲突。
- `CONTINUE_READY`：QUICK/BALANCED 的 CONTINUE capability 已满足当前主角、资源/能力、知识边界、主线程和下一章 boundary；非当前历史缺口不阻塞本次 handoff。
- `READY_WITH_GAPS`：至少 95% 章节覆盖、当前核心图谱齐全；只剩次要实体、远期路线或非核心语义缺口。
- `BLOCKED`：主角状态、当前核心规则/能力边界、主线程、续写边界、Edition/Source hash 或关键 Arc 缺失/冲突。

未来可能性可以不完整，但不得被伪装成当前 Canon。QUICK/BALANCED 可按续写或改写动作创建定向补齐任务；这不等于 FULL 就绪。不得产生 Canon Commit、批准草稿或启用 Edition。

## 输出

至少保留 `initialization_manifest.json`、`source_coverage.json`、`structural_index.json`、`arc_manifest.json`、`status.json`、`events.jsonl`、Operation Workspace、`entity_resolution/`、`synthesis/`、`metrics/`、`visuals/` 和 `reports/`。初始化 handoff 结果只需返回当前 requested stage 的 `initialization_id`、`readiness` 和实际完成/失败的 Arc；无关计数和 `generated_visuals` 可省略。Visual 为空不是失败。始终固定 `canon_committed=false`、`edition_activated=false`。

## Handoff Mode

`workflow start` 成功且当前 handoff 为 `RUNNING` 后，只读取 `task.json` 指定的业务输入，
按 manifest/arc manifest 中的 scheduled tasks 执行。不得自行把 QUICK/BALANCED 改成 Atlas-first
全流水线，也不得重建已冻结的 source、boundary、rhythm 或 metrics。Direct maintenance 模式
才按需补建缺失证据；所有 semantic 缺口保持 UNKNOWN，不用视觉导出填充 readiness。
