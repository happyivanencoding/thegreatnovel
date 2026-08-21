# TheGreatNovel 后端章节执行链验证最终报告

## Git

- BASE_SHA：`bf5259c91e9ea2c007fd049f4b0500117121c290`
- branch：`backend-opening-pipeline-comparison-v1`
- final commit(s)：`d8d9858`、`8c07bff` + 本次状态修正 commit（HEAD）
- pushed：yes
- 实验主目录：`books/real-exp-opening-pipeline-comparison-v2/`
- v1 处理：`real-exp-opening-pipeline-comparison-v1` 保留为原始证据；因 Chapter 2 被并行执行流竞争写入，未作为最终比较结果。

## Backend freeze

- `src/story_mvp/prompts.py` modified：no
- `src/story_mvp/workflow_state.py` modified：no
- `src/story_mvp/run_ledger.py` modified：no
- `src/story_mvp/openai_executor.py` modified：no
- `src/story_mvp/storage.py` modified：no
- 前端 `app.js` / `style.css` / `index.html`：本轮未修改

Opening Pilot 基线回归核对：`OPENING_THREE_CHAPTER_CONTRACT`、`DIRECTOR_CHAPTER_BUDGET_RULE`、`RESULT_STOP_RULE`、`parse_outline_fields` 与 `6a0ef8a961a64cb6d4f22ae4cdfb8fb1c1017a89` 逐项 PASS；`prompts.py` 相对该实验版本无 diff。

## Real production dataflow

真实固定 Ledger 节点：

`Director → Context Curator → Primary Writer → selected Specialist(s) → Integrator（有有效 Patch 时）→ State Delta`

Chapter Prep 是正式 Prompt mode，但不是 Run Ledger 节点；本实验单独保存其 Prompt/Response 并作为后续章节节点输入。`hybrid_selective` 的生产调用方最多选择前两个 Specialist；本轮真实结果为：

- 《炉藏万象》：三章均无 Specialist，Integrator 均 skipped，最终来源均为 Primary。
- 《掌中天工》：Chapter 1 = opening/action，Chapter 2 = dialogue/action，Chapter 3 = action；三章 Integrator 均执行并被采用。

Integrator 是否执行由真实 `should_run_integrator()` 的 `## Patch N` 检查决定；没有有效 Patch 时不强行运行。State Delta 只读取最终正式正文和事实摘要更新实验 BOOK 状态，不修改正文。

详细审计见 `backend-dataflow-audit.md`。

## Experiment

- 《炉藏万象》：Hybrid Chapter 1—3 完整，最终来源 `primary`，无 Chapter 4。
- 《掌中天工》：Hybrid Chapter 1—3 完整，最终来源 `integrator`，无 Chapter 4。
- Single Control：直接使用 `real-exp-opening-three-chapter-hook-v1` 对应两本已完成 Chapter 1—3，不重新生成、不修改。
- Hybrid：复用冻结 Fantasy Seed、World Vision、Story Program、Outline/Future 10、Chapter 1 后连续 BOOK/Canon；每章消费自身上一章正文与 State Delta。
- 所有 Hybrid LLM 内容节点均单次调用；未做文学重试、人工改正文、自动评分或 Chapter 4。

## Efficiency

Hybrid 实际调用数/Prompt chars/Response chars 和 token `UNKNOWN` 见 `efficiency-report.md`。摘要：

- 《炉藏万象》每章 5 次：Director、Prep、Curator、Primary、State Delta；Integrator skipped。
- 《掌中天工》Chapter 1/2 各 8 次，Chapter 3 7 次；分别包含 2/2/1 个 Specialist、Integrator 和 State Delta。
- Hybrid Chapter 3 Prompt chars：炉藏万象 102,994；掌中天工 137,308。
- Single 旧实验缺少真实 token/call manifest，严格记录 `UNKNOWN`，未用字符数伪装 token。

## Context bloat

Chapter 3 审计见 `context-bloat-audit.md`。两条 Hybrid lane 的 Director、Prep、Curator、Primary、Specialist/Integrator 都实际看到 Opening Contract；State Delta 不看到 Opening Contract。成本主要集中在连续 Canon/前文、BOOK/PLAN、Curator 输出、Primary Draft 和 Specialist/Integrator 输入的重复携带，而不是 State Delta。

## Blind quality

盲读材料和 key 分离保存在 `blind-reader-materials/`；两个独立 Reviewer 均未读取 key：

- 《炉藏万象》：`HYBRID_BETTER`。Hybrid 的第一章翻页力、现场对白/动作更强；Single 的能力边界、人格/NPC、少解释和资产复利更清楚。
- 《掌中天工》：`HYBRID_BETTER`。Hybrid 的能力落地、对白/动作与商业推进更强；Single 的人物指纹、NPC 独立性、少解释和长期资产清晰度更强。

两份最终偏好一致，但逐问题不是全面横扫。

## Opening Contract amplification

- payoff：两本都出现跨章递进调用同一核心能力的重复风险，但不是同一结果机械复播。
- 重复解释：candidate-c 的 Primary→Specialist→Integrator 可见正文没有重复解释；candidate-b 无 Specialist/Integrator，结果为 `UNKNOWN`。
- 过度前置：两本均未在前三章正式结算后续火鳞/炉心/长期升级。
- 人物工具化：主角未被工具化；两本都有匿名矿工/伤者局部功能化风险，candidate-c Chapter 2 还真实出现“让一车矿奴承担第二次能力验证风险”的局部问题。
- result-stop：两本均未观察到 Integrator 破坏 Primary 的 result-stop；后续内容是必要余波、敌方反应、关系变化或新入口。

详见 `opening-amplification-review-candidate-b.md` 与 `opening-amplification-review-candidate-c.md`。

## Cross-book Review

Hybrid 的稳定改善集中在开篇翻页、动作/空间、对白和能力落地；Single 的稳定优势集中在具体人格、NPC 主体性、解释克制、判断不工整和资产复利清晰度。上游规划已冻结，因此差异归因于 Writer realization 与多 Agent revision，不归因于 Creative upstream。

## Final verdict

`QUALITY_TIE_SINGLE_MORE_EFFICIENT`

理由：两个书级盲读都偏向 Hybrid，但质量维度是混合而非明确横扫；Hybrid 的调用/上下文复杂度明显更高，且本轮没有真实 token usage 或 Single 成本 manifest 支持更强的收益结论。该结论只提交证据，不修改默认 Writer Mode、不删除 Hybrid、不删除 Single。
