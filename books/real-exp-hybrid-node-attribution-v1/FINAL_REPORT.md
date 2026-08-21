# Hybrid Node Attribution Final Report

## Git / provenance

- branch：`principal_dev_new_sys`
- BASE_SHA / Code audit base：`53394ea356393c904e82d988e7b5ae634d2487f7`
- Experiment generation base：`d4e2dd6f3377f967d8930480016f15a450b74e1b`
- clean v2：历史 Git tree `books/real-exp-opening-pipeline-comparison-v2/`
- v1：历史 Git tree `books/real-exp-opening-pipeline-comparison-v1/`
- 两个 base 之间的 `src/story_mvp` 差异只有前端文件 `app.js`、`style.css`、`index.html`；backend `app.py`、`prompts.py`、`workflow_state.py`、`run_ledger.py`、`hybrid_runtime.py`、`storage.py`、`openai_executor.py` 无 diff。
- 本轮没有创建 freeze tag；没有生产代码修改，因此不需要新的代码冻结锚点。

## Scope and evidence

主归因只使用 clean v2 candidate-c《掌中天工》Chapter 1—3。每章独立比较同一章的 Primary Draft 与 Integrator Final；没有拼接不存在的 Primary-only 连续 lane。

clean v2 candidate-b《炉藏万象》三章 Integrator 均 skipped、final source 均为 Primary。它是控制证据，不伪造 Primary vs Integrator 对，也不能回答 Curator 是否必要。

v1 candidate-b Chapter 2 的 declared selection 与实际 Dialogue/Action/Integrator artifact 不一致；v1 candidate-c 还有旧的并行 Chapter 2 文件，以及旧 Reader label 与 system review 的内部冲突。本报告将这些标为 `EXCLUDED_FROM_CAUSAL_VERDICT` 或 `SUPPORTING_ONLY / REVIEW_LABEL_CONFLICT`，未读取它们替代本轮盲读，也未修改旧 raw evidence。

## Blind Reader results

盲位交叉为：Chapter 1 A=Primary/B=Final，Chapter 2 A=Final/B=Primary，Chapter 3 A=Primary/B=Final。三个 Reader 只读取各自 A/B 正文，输出保存在 `blind/chapter-XX/reader-review.md`。

| 章节 | Reader overall | 解码后的结果 | 主要优势 | 主要代价 |
|---:|---|---|---|---|
| 1 | A | `PRIMARY_BETTER` | 核心爽点、人物和钩子相同；Primary 救援动作更紧凑 | Final 补唐鹭脱身路径后又重复“四个人”总括，出现动作回叠 |
| 2 | A | `INTEGRATOR_BETTER` | Final 的对白让线索、唐鹭主动同行和协作边界闭合，章末行动更有牵引 | 机制/异常感知更显性；Primary 在解释克制上更好 |
| 3 | B | `INTEGRATOR_BETTER` | Final 补齐记录片、短锤来源和门框线路，前置—回收、空间与行动准备更清楚 | 对白没有改善；NPC 项为 MIXED |

逐问题结果没有形成全面横扫：Ch1 除商业整体项外大多 MIXED；Ch2 Final 在对白、人物、NPC、payoff、续读和商业连读上更强，Primary 在解释克制/正确判断密度上更强；Ch3 Final 在动作、人物具体性、解释清晰度、payoff 和续读上更强，Primary 只在对白上更顺。

## Deterministic diff

`metrics.json` 和 `diffs/` 使用同一脚本、同一 frozen source 确定性生成。字符 diff size 定义为非 equal opcode 中旧文本字符数与新文本字符数之和；changed paragraph count 定义为非 equal paragraph opcode 中旧/新段落数的较大值。

| 章节 | Primary chars | Final chars | textual diff size | changed paragraphs | Specialist calls | Integrator calls | accepted patches |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4524 | 4595 | 71 | 1 | 2 | 1 | 1 |
| 2 | 6629 | 6713 | 130 | 8 | 2 | 1 | 1 |
| 3 | 8023 | 8090 | 81 | 4 | 1 | 1 | 3 |

三章 Final 均与 Primary 不同，但都是局部修改：没有“完全相同”的 Integrator，也没有证据支持大规模重写。详细 Patch 与实际文本对应见 `patch-attribution.md`。

## Attribution findings

- Ch1：Action Patch 1 真正进入 Final，属于 action/spatial + continuity；它修补了唐鹭脱困路径，但留下重复总括句，导致 Primary 被盲读偏好。
- Ch2：Dialogue Patch 1 被拒绝且拒绝理由与动作连续性一致；Dialogue Patch 2 真正进入 Final，属于 dialogue/character + continuity/explanation；它改善协作关系和章末推动，但使异常线索更显性。
- Ch3：Action Patch 1/2/3 全部真实进入 Final，分别补齐记录片来源、短锤来源和空间线路；属于 continuity、action/spatial、explanation 的局部修复。

因此 Integrator 不是昂贵 copy，但也不是稳定的整体质量提升器。它最有价值的形态是对已存在、可定位的 continuity/action/dialogue 缺口做 selective repair；盲目采用每个 Patch 会损害节奏。

## Specialist / Integrator value

- 是否稳定增加解释：否。Ch2 有显性异常感知对白，Ch3 是空间措辞澄清，Ch1 主要是动作补写；没有三章稳定的解释膨胀，但 Ch2 确有“更说清楚、少留白”的代价。
- 是否稳定提高人物/NPC：否。Ch2 的唐鹭协作边界明显变强，Ch3 主角行动准备更具体，Ch1 人物差异不明显；不能称为稳定人物增益。
- 是否稳定提高 action/spatial/dialogue：否，但有选择性增益。Ch2 对白/关系、Ch3 动作/空间改善明确；Ch1 空间链补齐却造成节奏回叠。
- 是否只是昂贵 copy：否。三章均有真实局部 diff；但调用复杂度没有带来跨章、整体性或稳定质量保证。
- candidate-b control implication：三章没有 Specialist/Integrator 仍形成完整 Primary-only lane，说明质量信号可以在没有这些层时存在；它不能证明 Curator 必要，也不能把 candidate-b 的质量差异归因给 Specialist/Integrator。

## Architecture verdict

`SPECIALIST_INTEGRATOR_SELECTIVE_VALUE`

理由：candidate-c 三章中 2 章盲读明确偏好 Integrator Final，且增益集中在对白/协作、动作连续性、空间清晰度与行动准备；但第 1 章 Final 的局部修补产生节奏退化，第 2 章有解释显性化代价，且人物/NPC提升并不三章稳定。因此不满足 `SPECIALIST_INTEGRATOR_CLEAR_VALUE` 的稳定性要求，也没有证据支持 `NO_STABLE_VALUE` 或 `NEGATIVE_VALUE`。

## Next recommendation

保留 Specialist/Integrator 为可选 repair，不把它们视为普通章节的必需核心链。下一阶段先验证 `Curator → Primary` 是否值得成为核心链，再把 Specialist/Integrator 只用于有明确 action/dialogue/continuity 缺口的章节；不要修改生产代码或默认 Writer Mode 作为本审计的后续动作。

## Validation and Git handoff

- 生产 backend modified：`no`
- frontend modified by this task：`no`
- 新正文生成：`no`
- Chapter 4：`not generated`
- Reader agents：3 个真实独立 subagents，分别完成 Chapter 1—3 盲读；没有共享 key。
- 必要验证：确定性审计脚本运行成功；盲读文件存在；source path/metrics/diff/attribution 交叉核对完成。
- 提交路径：只允许 `books/real-exp-hybrid-node-attribution-v1/`。
