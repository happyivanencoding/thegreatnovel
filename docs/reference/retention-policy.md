# 保留与安全清理

`config/retention.yaml` 是当前分类说明。source、数据库、Metric Observation/Evidence、
Canon、注册 Atlas 版本和批准历史永远不进入自动清理候选。

```powershell
novel library cleanup --book-id <id> --dry-run
novel library retention --library-root <root> --book-id <id> --dry-run
```

dry-run 会输出候选、分类、大小、引用和精确 confirmation。apply 只把合格的
`REGENERABLE`/`ARCHIVE` 目标移入 `.archive`，不永久删除；archive 和 `exports/latest` 不会
被 retention 自动删除。

这条限制只约束自动 retention/cleanup。作者在 Web 书库中明确确认“永久删除”时，系统会删除
所选的整个 `library/<book_id>/` 项目；IMPORTED 项目的 `book/` 原文及 Library 外部来源文件
始终不在删除范围内。
