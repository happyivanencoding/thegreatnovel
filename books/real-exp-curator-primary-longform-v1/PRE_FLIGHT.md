# Pre-flight

状态：`PASS`

## Git

- branch: `principal_dev_new_sys`
- HEAD / `origin/principal_dev_new_sys`: `5ecda7d48354dca629bc184c2eb60d4cdbb5022c`
- frozen source tree: `d4e2dd6f3377f967d8930480016f15a450b74e1b`
- working tree 在实验目录创建前 clean。

## Frozen input checks

- A — Chapter 1—3 正文存在：PASS。复制的正文字符数分别为 293、367、427；目录中没有重新生成这三章。
- B — 起始 BOOK 是 Chapter 3 State Delta 后状态：PASS。`candidate-b/BOOK.md` 与复制的 `candidate-b/runs/chapter-0003/BOOK_after_state_delta.md` 原文一致，均为 515 chars。
- C — Future 10 有 Chapter 4—10：PASS。冻结 Outline 明确包含：第4章《火脉最后的方向》、第5章《把火传给下一炉》、第6章《炉监来收炉》、第7章《炉火先照见谁》、第8章《三座废炉的退路》、第9章《封炉印里的最后一道门》、第10章《黑炉镇外第一座炉》。
- D — Chapter 4 正文未被带入：PASS。历史 source tree 与新实验 candidate-b 在创建运行前均只有 Chapter 1—3 正文。
- E — Chapter 4 Director / Prep / Curator / Primary prompt 不含 Opening Three Chapter Contract：PASS。实际 render 的四个 prompt 均无该标题；字符观测为 Director 6,661、Prep 29,008、Curator 12,101、Primary 30,835（ledger prompt chars 分别为 6,429、27,655、11,726、29,507）。Chapter 4 已在该检查通过后完成唯一一次 Primary 生成。

## Freeze checks

`prompts.py`、`hybrid_runtime.py`、`chapter_context.py`、`run_ledger.py`、`workflow_state.py`、`storage.py`、`app.py`、`openai_executor.py` 以及前端静态/模板文件相对 base HEAD 均 clean。实验编排器只在本目录内，是历史 v2 工具的实验副本，不是生产代码。
