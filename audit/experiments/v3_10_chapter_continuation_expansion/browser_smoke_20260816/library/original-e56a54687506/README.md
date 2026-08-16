# 折叠塔顶的回声

此目录由 Novel Authoring System 的 Book Library 管理。
此原创项目从 premise 与 Story Foundation 开始，不要求来源正文；机器运行数据位于 `_system/`，请勿手工覆盖数据库或 Canon。

- book_id: `original-e56a54687506`
- layout: `library-v1`
- active edition: `base`
- book kind: `AUTHOR`
- creation mode: `ORIGINAL`
- original state: `FOUNDATION_READY`
- database: `_system/state.sqlite3`
- readiness: `FOUNDATION_READY`
- source files: 0
- latest chapter: `1`
- current Atlas: `unknown`
- current initialization: `unknown`
- latest export: `editions/base/exports/latest`

## 入口

- `book.yaml`: 书库注册元数据
- `source/`: 只读来源副本
- `editions/<edition_id>/`: edition-scoped analysis、writing、operations 和 exports
- `editions/<edition_id>/exports/latest/`: 当前 Portable Snapshot Bundle（如已生成）

## 常用命令

- `novel library paths --book-id original-e56a54687506`
- `novel atlas export-snapshot --book-id original-e56a54687506`
- `novel library cleanup --book-id original-e56a54687506 --dry-run`

## 下一步

先核对当前 edition、Atlas readiness 和指标覆盖，再由作者决定是否创建下一次 handoff。
