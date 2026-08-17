# Reference Corpus Program-Deep V1

本分支只增加离线 Corpus 的结构化编排与验证，不改变当前逐章写作系统。

## 输入与输出

- 只读输入：
  - `C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus`
  - `C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus-operations`
  - 原始小说根仅作来源存在性与边界说明，不复制进输出。
- 持久输出：
  - `C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus-program-deep-v1`
- 旧 `reference-corpus` 与 `reference-corpus-operations` 永久只读。

## 阶段

`freeze inputs → locator skeleton → bounded semantic worker overlay → single-book audit → cross-book synthesis → machine compile`

每个 worker 只处理不重叠的 book/range，并写自己的隔离目录。worker 可以写语义观察，但不能写 Git 代码、旧 Corpus、原始小说、Canon 或当前 runtime。

## 结构化资产

```text
reference-corpus-program-deep-v1/
├── PROGRAM_DEEP_SPEC.md
├── manifest.yaml
├── books/<source_book_id>/
│   ├── chapter-ledger.jsonl
│   ├── arc-map.jsonl
│   ├── payoff-map.jsonl
│   ├── book-program-dna.yaml
│   └── evidence-index.jsonl
├── cross-book/
├── machine/
└── operations/
    ├── progress.json
    ├── validation.json
    └── PROGRAM_DEEP_AUDIT.md
```

每条 semantic ledger row 必须带 `source_book_id/source_id/distill_id/segment_id/line_start/line_end`。没有证据的判断写 `UNKNOWN`/`Knowledge Gap`，不使用模型记忆补齐。

合并前必须拒绝明显模板假阳性：如果一个 worker 的大量 `SEMANTIC_COMPLETE` 行复用同一条 `one_line_story`，该分片留在 worker 隔离目录并标记 rejected，不能进入最终 `books/` 或 machine package。行数覆盖不能替代语义证据。

## 反偏置规则

先记录主角得到什么、旧限制解除什么、行动空间如何扩大、谁看见、读者得到什么即时满足，再记录延迟压力。`cost`、`responsibility`、`governance`、`institution`、`scarcity`、`constraint` 都是 optional，不是 required，不是默认长篇终点。

不新增正文 hash、review hash、checksum 或 fingerprint；resume 依据 manifest、范围、文件存在性和 schema 可读性。

## 完成边界

只有 26 本的全量 canonical unit 语义覆盖、Arc/Payoff/Book Program DNA 和跨书证据都完成后，machine package 才能标记 `READY_FOR_RETRIEVAL_INTEGRATION`。在此之前必须如实标记 `IN_PROGRESS`，不得把 locator skeleton 当作文学完成。
