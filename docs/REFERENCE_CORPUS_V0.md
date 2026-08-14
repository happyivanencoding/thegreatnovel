# Reference Corpus V0

Reference Corpus 是一个独立的、仅供参考的创作决策知识层。它把作者确认的来源阅读经验整理为可查询的 `Book DNA`、`Arc Observation`、`Mechanism Card`、`Contrast Case`、`Corpus Synthesis` 与 `Author Taste`，服务于未来的 ORIGINAL Genesis、Candidate Planning、Revision Planning 和 innovation reasoning。

它不是 Canon、Author Intent、当前书 Runtime State、强制模板、自动评分权威，也不是来源小说仿写器。选择一本书进入 Corpus，不等于作者认可该书的全部做法。

## 长期本体与运行索引

长期知识与证据本体是 Google Drive 下的 Markdown + JSON：

- 原始小说：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集`，永久只读；
- 派生 Corpus：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus`；
- GBrain PGLite/Postgres：可重建的页面、chunk、embedding 和关系索引；
- TheGreatNovel：未来只读消费者。

原文不会复制到仓库、Corpus 派生根或 GBrain searchable pages。Corpus 的卡片只保存抽象判断与短证据定位，不保存大段原文、来源人物、专有设定或可直接替换的桥段。

## 知识等级与解析边界

`reference-book` 是一本来源小说的元数据页；`book-dna` 是单书整体观察；`arc-observation` 是单书篇章观察；`mechanism-card` 是跨书综合后的条件化机制；`contrast-card` 是相近问题的不同解法；`corpus-synthesis` 是类别或跨类别综合；`taste-note` 只接受作者显式写入的判断。

知识等级只有：

`BOOK_OBSERVATION`、`CROSS_BOOK_CONTRAST`、`CORPUS_SYNTHESIS`、`AUTHOR_TASTE`。

单书 Finding 不自动提升为 Mechanism；模型判断不自动冒充 Author Taste。每项来源性主张必须回指 `source_book_id`、chapter/segment/line locator。每个实际类别的主推荐最多保留两本，类别结论最多称为 `PILOT TWO-BOOK CONTRAST`；为达到 26 本目标而增加的 `supplemental-representative` 不改变类别对照样本，也不能宣称类型普遍规律。

## CLI

```text
novel corpus init --raw-root <read-only novels> --corpus-root <derived corpus>
novel corpus inventory --raw-root <read-only novels> --corpus-root <derived corpus>
novel corpus validate-selection --corpus-root <derived corpus>
novel corpus validate --corpus-root <derived corpus>
novel corpus status --corpus-root <derived corpus>
```

`inventory` 只扫描 raw root 的直接子目录为 category，使用已有 distill preparation 的支持格式和章节标题规则；它不计算新 hash，不写入 raw root。`inventory` 同时生成 26 本目标的 `PROPOSED` selection：先按实际类别取两本，再以真实来源类别中的下一本可解析代表书补位；补位不伪造缺失类别。selection 等待作者确认，不创建 `confirmed.yaml`，不启动语义蒸馏。

## GBrain topology

先审计本机实际 CLI、brain engine、active schema、sources、mounts 与路径重叠，再做 topology decision：

1. 如果 `卡片盒子` 已是父 source，且子目录会重复索引，不增加重叠 source；
2. 如果可以干净隔离，则候选 source id 是 `novel-reference-corpus`，`federated=false`，查询显式指定 source；
3. 只有 source/schema 隔离确实无法成立时，才另行提案独立 brain；本轮不自动创建。

GBrain 只索引派生抽象卡片。最终同步链必须是：

```bash
gbrain sync --repo <reference-corpus> && gbrain embed --stale
```

最终 smoke 还要验证 embedded chunk coverage、多个以创作问题为中心的 hybrid search，以及来源小说原文不在 searchable pages。keyword-only 不是成功状态。当前如果 Hermes/bun 持有 PGLite lock，只能记录 BLOCKED 并把命令留给稍后执行，不能杀进程、删除 lock、复制数据库或建临时 brain。

## 消费权威顺序

```text
Hard Canon / Source-established Facts
  > Explicit Author Intent
  > Current-book Self Understanding
  > Reference Corpus
  > Generic Model Prior
```

Corpus 不能改写 Canon、覆盖 Author Intent、改变 confirmed Reader Kernel/selected Core、替换 Continuity、批准 Candidate、写入正文或直接改变评分。ORIGINAL 的 Reader Kernel 确认前，Corpus 只能作为 proposal prior；确认后只能提供已确认创作问题下的不同解法。

## 后续阶段与 A/B gate

后续顺序是 4-book smoke、26-book per-book distillation、category synthesis、cross-category synthesis、GBrain retrieval、read-only query adapter，最后用至少五个 Seed 做 A/B。A/B 必须比较方案差异、爽点成熟度、长线潜力、世界扩张、套路感、来源泄漏、不同 Seed 是否被拉成同一模板，以及作者口味。没有 A/B 证据，不自动接入 Genesis、Candidate Planning 或 Revision。

## Rollback

确定性文件可从 raw root 重新生成；删去 proposal 或派生卡片不会影响原始小说。GBrain source 尚未注册前无需数据库回滚；已注册时只使用本机实际支持的 source remove 流程，不删除 PGLite 数据目录、不修改 lock、不建立第二个 brain。任何 semantic artifact 重新生成时，只标记依赖它的 synthesis 为 `STALE`，不全量重建无关 Corpus。
