# Core Writer Attribution Final Report

## Git / freeze

- branch：`principal_dev_new_sys`
- BASE_SHA：`c405b7d1b6d7ad89fc7a41ce1a4da4126aa4dc42`
- EXPERIMENT_ARTIFACT_COMMIT：`91eb1f9`（完整实验产物提交）
- FINAL_SHA：以最终主分支 handoff 为准
- pushed：以最终主分支 handoff 为准
- Experiment generation base：`d4e2dd6f3377f967d8930480016f15a450b74e1b`
- production backend modified：`no`
- frontend modified by this task：`no`
- Prompt modified：`no`
- Specialist/Integrator：`not run`
- Chapter 4 / continuous lane：`not generated`

## Snapshot sources

- snapshot-01：`candidate-b / Chapter 1`，使用 v2 `candidate-b/BOOK.md`、Chapter 1 Prep、Chapter 1 plan、无前文正文。
- snapshot-02：`candidate-b / Chapter 3`，使用 v2 `candidate-b/runs/chapter-0002/BOOK_after_state_delta.md`、Chapter 1—2 previous prose、Chapter 3 Prep/plan。
- snapshot-03：`candidate-c / Chapter 2`，使用 v2 `candidate-c/runs/chapter-0001/BOOK_after_state_delta.md`、Chapter 1 previous prose、Chapter 2 Prep/plan。

所有输入均从 frozen v2 Git tree 读取并复制到各 snapshot 的 `frozen-input/`，未恢复旧实验目录到 principal 工作树。

## Calls

共 12 次 content call：每个 snapshot 的 Single、Primary-Fallback、Curator、Curated Primary 各 1 次。模型为真实独立 `gpt-5.6-luna` subagent；实际 input/output token 和 sampling 参数均为 `UNKNOWN`，未用 chars 冒充 token。原始 Prompt/Response 全部保留。

snapshot-01 Primary-Fallback 出现正文标题 `第四章` 与目标 Chapter 1 不一致；snapshot-01 Single/Curated Primary、snapshot-02 Curated Primary 还出现正文缺少 Markdown 章节标题的格式现象。均保留原始 evidence，不重试、不修正文；格式 notes 在 `results.json`。

## Blind Reader mapping

盲位 key 单独保存在 `blind/blind-key.md`。三份 Reader 只读取 A/B/C 正文，整体判断都为 `MIXED`；下面的 pairwise 是主审计根据 Reader 十项选择解码后的方法级判断，不是把 Reader 未知来源的策略栏伪装成已知结论。

| snapshot | Single vs Primary-Fallback | Primary-Fallback vs Curator-Primary | Single vs Curator-Primary | overall |
|---|---|---|---|---|
| 01 | `PRIMARY_FALLBACK`：Primary 在动作/空间、对白、NPC、正确判断密度和商业节奏上占优；Single 在 payoff/资产清晰度占优 | `PRIMARY_FALLBACK`：Primary 的整体场景推进更稳定；Curator 在主角具体性/解释克制局部占优 | `MIXED` | `MIXED` |
| 02 | `MIXED`：Single 的动作/NPC/解释克制/商业整体与 Primary 的对白、行为指纹、资产清晰度各有胜负 | `MIXED`：Curator 在解释克制、payoff、续读上占优，Primary 在对白/行为/资产上占优 | `MIXED` | `MIXED` |
| 03 | `MIXED`：Primary 的行为指纹/资产清晰度与 Single 的 NPC/payoff 各有优势 | `CURATOR_PRIMARY`：Curator 在动作、对白、正确判断、续读和商业整体上占优 | `CURATOR_PRIMARY`：但 Single 仍在 NPC/payoff 上占优 | `MIXED` |

## Cross-snapshot quality

### Single

Single 没有在三个 snapshot 形成稳定 overall 优势。它的可复用优势主要是部分章节的 payoff/资产清晰度、主角行为指纹或 NPC 具体性，但这些优势在另两个 snapshot 被其他 Arm 分别取得或抵消。

### Primary Writer

Primary-Fallback 在 snapshot-01 的动作推进、对白、NPC 和商业节奏上最强；在 snapshot-02/03 仍有行为指纹或资产清晰度优势，但没有稳定压过 Single 或 Curator。它显示出比 Single 更紧凑的 Reader-First 执行方式的潜力，但证据不足以支持无 Curator 的核心链。

### Curator

Curator-Primary 在 snapshot-03 对动作/空间、对白、正确判断密度、续读和商业整体的改善最集中；snapshot-02 在解释克制、payoff 和章末续读上有局部贡献；snapshot-01 只在主角具体性/解释克制局部占优，overall 仍混合。Curator 的贡献是选择性聚焦，不是稳定全面提升。

### Curator losses / costs

- Curator 额外增加一次 LLM call，三组都无 token usage 可核验。
- 最终 Curated Primary Prompt 在 snapshot-02/03 分别比 Primary-Fallback 少 9,341/9,384 chars，但 snapshot-01 反而多 1,013 chars。
- 完整 Curator chain 的总 Prompt 输入在三个 snapshot 都高于 Primary-Fallback；详见 `context-cost-audit.md`。
- 没有证据证明 Curator 稳定减少解释、稳定提高 NPC autonomy 或稳定提高人物行为指纹。

## Q1：Primary Writer 是否比 Single 更适合作为正式正文核心？

结论：本三 snapshot 不能支持稳定结论。Primary-Fallback 在 snapshot-01 有明显优势，但 snapshot-02/03 是混合；Primary 的优势不足以满足“稳定优于或不弱于 Single”的核心链定义。

## Q2：Curator 是否值得额外一次 LLM call？

结论：本三 snapshot 不能支持 Curator 成为核心必跑节点。Curator-Primary 只在 snapshot-03 对 Primary-Fallback 形成较明确优势，snapshot-01 由 Primary-Fallback 占优，snapshot-02 混合；同时 Curator 增加一次调用和总上下文成本。

## Architecture verdict

`MIXED_NO_CORE_CHANGE`

三个 snapshot 的方向不一致：Primary 在 snapshot-01 占优、snapshot-02 混合、snapshot-03 与 Curator 竞争；Curator 在 snapshot-03 占优、snapshot-02 局部改善、snapshot-01 没有整体胜出；Single 也没有稳定 overall 胜出。现有 3 个局部 snapshot 不足以改变核心 Writer 架构。

## Next recommendation

本轮不修改生产架构。保留当前 Single、Primary、Curator 路径作为可审计候选；下一轮若继续，应扩大同样严格的 snapshot 数量，并预先定义如何处理正文格式错误；不要把 Curator 的上下文压缩直接当成质量增益，也不要把任一 snapshot 的局部胜负升级为默认 Writer Mode 决策。

## Validation

- `prepare_core_writer_experiment.py`：通过；正式 `generate_prompt()` 渲染。
- `package_core_writer_results.py`：通过；现有正文提取函数、A/B/C 盲位包装通过。
- `py_compile`：通过。
- Reader：3 个真实独立 subagents，分别完成一个 snapshot 的盲读；不参与 content generation。
