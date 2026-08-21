# Core Writer Attribution Experiment

## 目标

在完全相同的冻结章节事实、事件合同、Canon、计划和前文下，比较：

- Arm A：Single Writer，`mode="chapter"`；
- Arm B：Primary Writer without Curator，`mode="primary_writer"`，`curator_response=""`、`curated_context=""`，由正式生产代码进入显式 fallback；
- Arm C：Curator→Primary，先运行一次正式 `context_curator`，再把原始 Response 同时作为 `curator_response` / `curated_context` 传入正式 `primary_writer`。

本轮不运行 Specialist/Integrator，不生成连续小说，不修改生产代码、Prompt、默认 Writer Mode 或前端。

## Git / provenance

- branch：`principal_dev_new_sys`
- BASE_SHA / code audit base：`c405b7d1b6d7ad89fc7a41ce1a4da4126aa4dc42`
- experiment generation base：`d4e2dd6f3377f967d8930480016f15a450b74e1b`
- generation source：历史 Git tree `books/real-exp-opening-pipeline-comparison-v2/`
- formal Prompt source：当前 checkout 的 `src/story_mvp/prompts.py`；与 generation base 的 backend diff 为 none。

## Snapshots

1. `snapshot-01`：candidate-b《炉藏万象》Chapter 1，Opening、第一异能高光、世界→主角收缩。
2. `snapshot-02`：candidate-b《炉藏万象》Chapter 3，资产复利、人物协作、空间和下一阶段入口。
3. `snapshot-03`：candidate-c《掌中天工》Chapter 2，动作、机械空间、对白、能力第二次应用。

每个 snapshot 独立读取同一 BOOK snapshot、current outline、current long block、chapter plan、previous prose、recent summaries、prose profile 和 optional inspiration；不把一个 Arm 的结果喂给另一个 Arm。详细 source path 在 `SOURCE_MANIFEST.json`。

## 调用边界

每个 snapshot 正好 4 次 content call：Single 1、Primary-Fallback 1、Curator 1、Curated Primary 1；共 12 次。所有调用均为单次，不重试文学结果，不人工改正文。Reader 在全部 content call 完成后才运行，不参与生成。

## 结果处理

Prompt 由正式 `story_mvp.prompts.generate_prompt()` 渲染；正文由现有 `hybrid_runtime` 提取函数解析。原始 Prompt、Response、frozen input、提取 body、fact summary、blind A/B/C 和 key 均保留。无法获得的 token/sampling 信息严格记录为 `UNKNOWN`。
