---
name: reference-corpus-distillation
description: TheGreatNovel Reference Corpus 的 Semantic Distillation V1 权威流程；输出仅为中文、可追溯、REFERENCE_ONLY 的创作决策先例。
---

# Reference Corpus Semantic Distillation V1

这是 TheGreatNovel 唯一权威的 Reference Corpus 语义蒸馏流程。它把小说阅读经验转成
可查询的创作决策先例，不把来源正文、来源人物、来源情节、来源句式或软理解写入
Canon。所有人类可读的语义内容默认使用中文；`source_book_id`、`source_id`、
`segment_id`、行号和既有技术枚举保留原样。

## 先读的文件

每一本书和每次 cross-book synthesis 开始前必须读取：

1. `docs/REFERENCE_CORPUS_DISTILLATION_CHECKLIST.md`
2. 当前 handoff 冻结的业务输入和 evidence locator
3. 当前 Corpus 的 `selection/corpus-sources-v0.confirmed.yaml`

如果本次是标准 Local File Handoff，必须先按
`.agents/skills/process-novel-handoff/SKILL.md` 执行 `workflow start`，只读取
`task.json` 列出的业务输入；不要重算 Python 已冻结的协议事实。

## Thin Harness + Fat Skill

Python / deterministic adapter 只负责：

- source identity、文件扫描、chapter/segment/line locator；
- `reference-corpus-card-v1` schema、Pydantic validation、source count；
- provenance、evidence resolution、dependency/stale propagation；
- Markdown → `machine/` package、metadata prefilter、retrieval diversity guard；
- raw-text leakage、schema drift、统计和报告。

Codex / LLM 负责：

- reader promise、repeatable anticipation loop、payoff 与 progression 判断；
- action-space、advantage、wonder、exploration、novelty、relationship、mystery；
- arc interpretation、contrast、mechanism、synthesis 与 applicability judgment；
- 失败风险的 `OBSERVED_REPETITION`、`OBSERVED_STRUCTURAL_WEAKNESS`、`INFERRED_RISK` 区分。

禁止添加 literary score、governance score、cost score、固定爽文公式、keyword-only
优劣 classifier 或新的创作 Hard Gate。

## 书级执行

对每本书检查 opening、early、mid、late、ending/current ending、major payoff、major
transition、high-novelty window。根据长度调整窗口；只能纵向快照时明确写
`LONGITUDINAL_SNAPSHOT`，不得冒充 exhaustive read。

优先回答“读者为什么继续读”和“突破后真正多了什么可能性”。主动检查 pure-upside
payoff、power verification、ability/artifact delight、status rise、relationship、
exploration、mystery/reveal 和 resource liberation。`cost`、`constraint`、`scarcity`、
`responsibility`、`governance` 都是可选镜头；没有证据时写 `NOT_MATERIAL`。

书级产物是 `book-dna`、`arc-observation` 和 6–12 个高价值 `observation`。Arc 必须
标明 `CONTIGUOUS_ARC` 或 `LONGITUDINAL_TRAJECTORY`；aftermath 不等于 debt，future
opening 可以是 `NONE`。

## 跨书执行

单书 Observation 不得自动升级为 Mechanism。Mechanism 至少需要 4 本 distinct books、
可说明的适用条件、至少一个不适用/对照案例和可解析 locator；Contrast 至少呈现 3 种
同一创作问题的不同解法。Category Synthesis 至少 2 本 validated source books；
Cross-category Synthesis 通常需要 4 本、3 个类别，证据不足就标记 `PILOT` 或保留为
Knowledge Gap。

现有 constraint/governance-heavy cards 只能重新定位为 `possible variant`，不能写成
一般规律。每张跨书卡都要列出 positive reader payoff、action-space effect、
when-not-to-use、failure basis 和 transfer boundary。

## 边界与发布

Corpus 是 `REFERENCE_ONLY`：不写 Canon、Reader Kernel、Core、Foundation、Draft、
Payoff Engine 或作者指令；不直接批准 Candidate；不把来源结构注入正文。发布/导入只能
通过显式流程完成，且不得激活 Edition。原小说目录永久只读，Corpus 只保留 paraphrase
与 locator，不建立 quote database。

GBrain 不是本 Skill 的前置条件。本阶段只需让 Markdown 和 machine package 可被
deterministic adapter 消费；不得升级、改数据库、删除 lock、建立临时 brain 或自行实现
embedding。没有 GBrain 时使用独立 metadata retrieval fixture 验证可消费性。

## 完成门槛

运行并记录实际结果：

```text
novel corpus semantic-validate --corpus-root <CORPUS_ROOT>
novel corpus compile --corpus-root <CORPUS_ROOT>
novel corpus audit --corpus-root <CORPUS_ROOT>
novel corpus stats --corpus-root <CORPUS_ROOT>
```

只有 semantic audit、lens audit、machine package、retrieval fixture 和相关测试都通过，
才能报告 `READY_FOR_RETRIEVAL_INTEGRATION`。不得报告
`READY_FOR_PRODUCTION_GENERATION`。
