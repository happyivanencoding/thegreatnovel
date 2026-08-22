# Frozen Chapter 3 State Delta Inputs

记录时间：2026-08-22T21:02:05.3788505+02:00
工作目录：C:\dev\tgn-story-mvp
分支：principal_dev_new_sys
HEAD：cae0ca6a96cdf9837a099841815b451fc4505f6a

## 输入路径

- BOOK 起点：books/real-exp-opening-reader-first-fresh-v1/runs/chapter-0002/BOOK_after_state_delta.md
- Director response：books/real-exp-human-reaction-ch3-v1/after-v2/director_response.md
- Primary raw / 正文 / 摘要容器：books/real-exp-human-reaction-ch3-v1/after-v2/primary_response.md
- Primary 正式正文：books/real-exp-human-reaction-ch3-v1/after-v2/final_formal_prose.md
- 指定 Primary 事实摘要：books/real-exp-human-reaction-ch3-v1/after-v2/chapter_fact_summary.md（文件不存在）
- 实际使用的事实摘要：books/real-exp-human-reaction-ch3-v1/after-v2/primary_response.md 的 `# Primary Fact Summary` 区块，逐字提取；未补写事实
- CHAPTER_PLANS 第3章：books/real-exp-human-reaction-ch3-v1/CHAPTER_PLANS.md 的 `## 第3章：升院考核` 区块（含 Frozen Event Facts）
- Prompt 生成代码：src/story_mvp/prompts.py 的 `generate_prompt`
- State Delta 解析代码：src/story_mvp/prompts.py 的 `parse_state_delta_v2`
- BOOK 应用代码：src/story_mvp/storage.py 的 `apply_state_delta_to_book`

## 精确生成参数

使用当前代码调用：

`generate_prompt(mode='state_delta', template='', book_content=BOOK起点, current_outline='', chapter_number=3, chapter_prose=final_formal_prose, chapter_fact_summary=Primary response 内嵌 Primary Fact Summary, current_state=BOOK起点状态区, recent_summaries=BOOK起点 RECENT SUMMARIES, current_chapter_plan=CHAPTER_PLANS 第3章)`

Director response 已读取用于上下文核对，但按当前 `state_delta` 实现不作为输入块传入；`current_outline` 保持空字符串。当前实现的 State Delta 分支只渲染章节号、Canon Index、正式正文和事实摘要，因此传入的 `current_chapter_plan` 不会出现在生成的 prompt 中。

## 输出路径

- 原样生成的 prompt：books/real-exp-human-reaction-ch3-v1/after-v2/state_delta_prompt.md
- 单次 State Delta response：books/real-exp-human-reaction-ch3-v1/after-v2/state_delta_response.md
- 应用后的 BOOK：books/real-exp-human-reaction-ch3-v1/after-v2/BOOK_after_state_delta.md

## 字段核对

- Prompt：包含 State Delta 模板要求的五个一级输出标题，以及当前章节编号、Canon Index、正式正文、Writer 事实摘要四个输入块；未注入完整 BOOK Contract、完整计划、GBrain、Reference Programs 或前两章正文。
- `chapter_fact_summary`：指定文件缺失；使用 `primary_response.md` 内嵌 `# Primary Fact Summary` 的原文作为确定性替代，缺失项已记录。
- Response：`parse_state_delta_v2` 成功解析 `audit`、`active_scene_state`、`persistent_canon`、`chapter_summary`、`open_promises` 五个字段；未包含 AUTHOR NOTES 标题。
- 应用结果：`apply_state_delta_to_book(book_content, 3, response)` 成功；状态区为“当前已完成第3章”，并由代码逐字保留起点 BOOK 的 AUTHOR NOTES。
- 事实边界：仅写入公开升院合格、尚未正式入内门、内门报到和后续资源未发生、回身卸力步已使用并消失、许照确认守约、周既明成为公开竞争者；未写成正式入内门，未生成或规划 Chapter 4。
- 授权范围：本 worker 只写本目录的 `state_delta_prompt.md`、`state_delta_response.md`、`BOOK_after_state_delta.md`、`STATE_INPUTS.md`；未修改 src/tests/docs 或起点 BOOK。
