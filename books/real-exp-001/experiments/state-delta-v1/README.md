# State Delta 实验：真实第4章（state-delta-v1）

**NON_CANONICAL EXPERIMENT（非 Canon 实验）**

本实验仅为可审查的实验产物：

- 不写入、不修改 `books/real-exp-001/BOOK.md`（未自动应用 Proposal）；
- 不保存第4章为 Canon（未创建 `chapters/chapter-0004.md`）；
- 不生成第二版正文，不对 State Delta 做自动修正或重试（State Delta 只执行一次）；
- `proposed_canon_index.md` 即使经人工确认，也仅作为本实验目录下的实验产物，不回填 BOOK。

## 执行标识

- 执行代理：Qoder 子代理 Taylor（State Delta 实验）
- Prompt 生成：当前生产代码 `src/story_mvp/prompts.py` 的 `generate_prompt(mode="state_delta", ...)`，旧 Canon Index 由 `parse_canon_index` 确定性解析自 `BOOK.md` 的 `# 当前状态、未兑现承诺与作者备注` 区块。
- State Delta 执行：一次调用，无重试。

## 输入来源

| 输入 | 来源文件 |
| --- | --- |
| 第4章正式正文 | `temps/exp_ch4_writer_response.md`（`# 正式正文` 区块，按一级标题切分提取） |
| 章节事实摘要 | `temps/exp_ch4_writer_response.md`（`# 章节事实摘要` 区块，按一级标题切分提取） |
| 旧 Canon Index | `books/real-exp-001/BOOK.md`（状态区，`parse_canon_index` 解析） |
| 章节编号 | 4 |

未注入：GBrain、Reference Programs、BOOK CONTRACT（画像区块）、百章计划、十章计划、prose profile、前几章完整正文。

## 字符数统计

| 项目 | 字符数 |
| --- | --- |
| State Delta Prompt（`state_delta_prompt.md`） | 3788 |
| Proposed Canon Index（`proposed_canon_index.md`） | 1058 |
| 第4章正式正文（注入部分，参考） | 2036 |
| 章节事实摘要（注入部分，参考） | 181 |

## 产物清单

- `README.md`：本文件。
- `state_delta_prompt.md`：完整 State Delta Prompt 原文（生产代码生成）。
- `state_delta_response.md`：完整 State Delta 返回原文（`# State Delta Audit` + `# Proposed Canon Index`）。
- `proposed_canon_index.md`：单独提取的 `# Proposed Canon Index` 内容。
- `review.md`：以实验操作者身份完成的 7 项审查与总体结论。
