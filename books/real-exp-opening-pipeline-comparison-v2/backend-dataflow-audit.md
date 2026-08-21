# Backend dataflow audit

审计基线：`origin/principal_dev_new_sys` / `bf5259c91e9ea2c007fd049f4b0500117121c290`；只读审计 `src/story_mvp/run_ledger.py`、`src/story_mvp/prompts.py`、`src/story_mvp/hybrid_runtime.py`、`src/story_mvp/app.py` 及生产前端已有的 Specialist 选择 helper。本文件不改变生产代码。

## 真实 Run Ledger 节点

`RUN_NODES` 固定为：

`director → curator → primary → opening/dialogue/action/emotion → integrator → state_delta`

- Director 是 Run Ledger 节点，具有 Prompt、Response、attempts 和 status。
- Context Curator、Primary Writer、四个 Specialist、Integrator、State Delta 也是固定 Ledger 节点。
- Chapter Prep 不是 Run Ledger 节点。它是独立的 Prompt mode，页面/实验编排器把 `chapter_prep_prompt.md` 与 response 保存到 Run 目录，但不会出现在 `manifest.nodes` 中。
- `RunRequest` 默认 `writer_mode=hybrid_selective`；创建 manifest 时所有固定节点建立，未选 Specialist 初始为 `skipped`。

## Hybrid Selective 的实际选择

- Director response 先被保存，再由当前实验编排器读取 `Opening/Dialog/Action/Emotion：启用` 行，按固定顺序取前两个。
- 生产 UI 的 `selectedSpecialistNames()` 对 `hybrid_selective` 也只返回已勾选 Specialist 的前两个；随后调用 `set_selected_specialists`。
- `run_ledger.set_selected_specialists` 负责把未选 Specialist 标记为 `skipped`、把选中的 Specialist 置为 `pending`；后端 API 本身不额外强制“最多两个”，因此本轮以真实生产调用方传入的集合为准，并在 execution evidence 中逐章记录。

## 必跑、可能跳过与最终正文

- Director、Curator、Primary 是本轮 Hybrid lane 的必跑节点；Chapter Prep 是章节生成前的独立必需输入，但不计入 Ledger 节点集合。
- 选中的 Specialist 单次执行；未选 Specialist 按生产逻辑保持 `skipped`。
- `should_run_integrator()` 只检查 Specialist response 中是否存在 `## Patch N`。没有有效 Patch 时，`skip_integrator_if_no_patches()` 将 Integrator 标为 `skipped`；本轮不强行执行。
- 有有效 Patch 时，Integrator Prompt 接收 Primary Draft 与四个 Specialist 的局部 Patch 投影，且只允许显式采用局部改动。
- 最终来源必须由显式 `adopt_final_source(root, chapter, source)` 选择 `primary` 或 `integrator`。无 Patch 的生产路径采用 Primary；有 Patch 的路径只有在 Integrator response 合同解析成功并显式 adopt 后才采用 Integrator。

## State Delta 的事实来源

State Delta 不是章节门禁。它的 Prompt 使用当前已保存的正式正文与章节事实摘要；实验编排器在 `finalize` 后把最终正文写入实验章节，再生成 State Delta Prompt。State Delta v2 解析成功后，实验副本才通过 `apply_state_delta_to_book` 更新 BOOK 状态区。它不读取或改写 Single Control。

## Opening Contract 的节点可见范围

`generate_prompt()` 在 Chapter 1—3 为以下 Prompt mode 注入同一份 `Opening Three Chapter Contract`：

- Director；
- Chapter Prep；
- Context Curator；
- Primary Writer；
- 每个已选 Specialist；
- Integrator；
- 单 Writer `chapter` 路径。

State Delta 不接收 Opening Contract；它只根据正式正文、事实摘要和 Canon 状态做书记员式更新。因此本轮放大检查的对象是 Director/Prep/Curator/Primary/Specialist/Integrator，而不是 State Delta。

## 本轮观测重点

每章保留每个实际节点的 Prompt、Response、status、是否执行、字符数和最终来源；token usage 若运行返回则记录真实值，无法取得时严格写 `UNKNOWN`。后验只判断：能力 payoff 重复、解释重复、未来升级前置、人物工具化，以及 Integrator 是否破坏 result-stop。
