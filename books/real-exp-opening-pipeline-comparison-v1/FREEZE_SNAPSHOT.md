# Freeze Snapshot

本实验输入直接来自 `books/real-exp-opening-three-chapter-hook-v1/`，不读取其旧正文作为 Hybrid 生成上下文。

| 本实验 lane | 书名 | 初始 BOOK | Fantasy Seed | World Vision | Story Program | Frozen Outline / Future 10 | Single 对照 |
|---|---|---|---|---|---|---|---|
| `candidate-b` | 《炉藏万象》 | `candidate-b/BOOK.md`（由 `source/BOOK_after_old_experiment.md` 的设计区块加 clean state 生成） | `candidate-b/source/fantasy_seed.md` | `candidate-b/source/world_vision.md` | `candidate-b/source/story_program.md` | `candidate-b/outline/outline_response.md` | `../real-exp-opening-three-chapter-hook-v1/candidate-b/chapters/chapter-0001..0003.md` |
| `candidate-c` | 《掌中天工》 | `candidate-c/BOOK.md`（由 `source/BOOK_after_old_experiment.md` 的设计区块加 clean state 生成） | `candidate-c/source/fantasy_seed.md` | `candidate-c/source/world_vision.md` | `candidate-c/source/story_program.md` | `candidate-c/outline/outline_response.md` | `../real-exp-opening-three-chapter-hook-v1/candidate-c/chapters/chapter-0001..0003.md` |

`BOOK_after_old_experiment.md` 是冻结上游设计与旧状态证据；它包含旧实验状态，不能直接作为本轮 Canon。旧 Single Pilot 的 Chapter 1 Prompt 明确记录 clean state：“故事尚未开始”“当前尚无已完成正文或已批准章节摘要”，因此本实验只保留 source 的设计区块并复原该状态。旧 Pilot 当前的 `BOOK.md` 和 `runs/` 不复制为 Hybrid 的初始状态，以避免把 Single 已发生的三章偷偷喂给 Hybrid。旧 Pilot 的正文只在后验去标识盲读阶段读取。

本实验固定输入校验：

- 只有 candidate-b、candidate-c；
- 每个 lane 只允许出现 Chapter 1—3；
- `source/` 与 `outline/` 在实验运行后不得被修改；
- 新正文只写入本目录自己的 `chapters/` 和 `runs/`。
