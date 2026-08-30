# E2E Invalidation Note

本文件只标记实验脚本自身造成的无效证据，不修改或删除原始输出。

## Invalidated artifacts

以下旧 artifacts 因 `extract_chapter_plan()` 使用 DOTALL heading regex，把 Future-10 第1章到后续章节一起返回，随后字段 parser 实际读到较后章字段，导致所谓 Chapter 1 执行了错误时序事件：

- `chapter1/` 全部旧 runtime artifacts；
- `cycle1/DECISION1*`：其输入 Canon 来自上述错误时序 Chapter 1，因此不能作为正式 trigger 证据。

这些文件保留为 provenance，不计入 E2E 成绩，也不删除或覆盖。

## Still valid

- 21/21 deterministic Progressive Canon / Reveal Transport tests；
- `decision0/DECISION0*`；
- `open_phase/STORY_REFRESH_OPEN*`；
- `open_phase/OUTLINE_OPEN*`。

## Recovery rule

修正章节提取后，使用新的 `chapter1_v2/`、`cycle1_v2/` 等目录；已经有效的上游输出只允许 exact model/effort cache reuse，不重新抽样。
