# Clean Five-Seed Production Test v4

## 实验目的

冻结 `b6828961e9e4939577e66264cc0b9a62de1ade95` 中的生产 Prompt 后，在真实生产模式下用一次调用生成五个 Fantasy Seed 候选，观察首次主动兑现、个人一级成长、非对称收益、长篇玩法和世界扩张的自然分布。

本实验只停留在 Fantasy Seed 层。不生成 World Vision、Story Program、Mainline、Outline 或正文，不查询、修改或重蒸馏 GBrain。

## 生成代理边界

生成代理实际允许读取的文件只有：

- `INPUT.md`
- `fantasy_seed_prompt.md`

生成代理不得读取或提及 v1、v2、v3、GBrain、Reference Programs、BOOK、Growth Genome、任何 review、bias diagnosis、实验说明或本任务说明中的诊断词。`EXPERIMENT.md` 只供编排与验收使用，不进入生成代理的读取集合。

生成只能由一个真实 Agent 完成：一次 request、一次 response，response 内含五个完整候选。不得拆成五次采样、五个生成 Agent、续写、自动去重、自动重生成或预先分配候选类型。

## 冻结规则

生成完成后原样保存实际 Prompt 快照、完整 response、调用 ID，并从 response 中按五个原始 `## 候选N：` 标题做机械切片。候选文件不得摘要、改写、补内容、去重、重排或语义修复。

只有冻结完成后才能启动 Reviewer。Reviewer 只读取五份候选；它不知道 Prompt、INPUT、实验目的、历史实验或本次修改。Meta Reviewer 只能在 Blind Review 完成后读取 v3 与 v4 的 Seed 及各自盲审结果，并且只比较 Seed 层。

## 观察边界

Blind Review 只记录候选中实际出现的开局位置、最强欲望、核心优势、第一次使用的个人直接收益、第一次主动兑现、最大直接收益者、10/30/100章一级成长、重复玩法和世界扩张；不判断行为道德正确性。

另行观察残缺补偿、身体接口、自动成本和是否存在结构性道德证明，不把这些观察写回生产 Prompt。

## 停止点

无论结果如何，本实验在 Seed、Blind Review 与 v3↔v4 Meta Review 完成后停止，不自动继续修改系统或进入下游。
