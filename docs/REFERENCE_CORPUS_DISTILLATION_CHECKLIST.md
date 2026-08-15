# Reference Corpus Semantic Distillation Checklist

这是覆盖镜头，不是 runtime taxonomy。每一项都要检查；没有证据可以写
`NOT_MATERIAL` 或 `UNKNOWN`，不能为了填表虚构。Checklist 不会把 cost、scarcity、
responsibility 或 governance 变成必需字段。

## A. Sampling / Evidence Coverage

- [ ] opening
- [ ] early stage
- [ ] middle stage
- [ ] late stage
- [ ] ending / current ending
- [ ] 至少一个 major payoff window
- [ ] 至少一个 major transition window
- [ ] 至少一个 high-novelty window
- [ ] 记录 `sampling_strategy`、`sample_window_count`、`coverage_stages`
- [ ] 仅纵向快照时明确 `coverage_mode: LONGITUDINAL_SNAPSHOT`

## B. Reader Promise / Reader Experience

- [ ] 主要期待
- [ ] 继续下一章的原因
- [ ] repeatable anticipation loop
- [ ] 最稳定的正向愉悦
- [ ] 辅助体验
- [ ] 中后期变化
- [ ] 使用既有 `ReaderExperience`，不新建 enum

## C. Payoff / Progression

- [ ] payoff、建立方式、立即可感知性
- [ ] payoff 是否改变行为方式或扩大 action space
- [ ] quantitative / qualitative growth
- [ ] pure-upside payoff
- [ ] delayed / status / discovery / emotional payoff
- [ ] power verification
- [ ] payoff 后可为 `NONE`、`REST`、`ENJOYMENT`、`NEW_OPTION`、`NEW_GOAL`、
      `NEW_MYSTERY`、`NEW_SCALE` 或 `NEW_PRESSURE`
- [ ] 没有默认添加 `NEW_COST`、`NEW_DEBT` 或 `NEW_SCARCITY`

## D. Advantage / World / Novelty

- [ ] protagonist-exclusive advantage
- [ ] positive abnormality / capability asymmetry
- [ ] impossible-before action
- [ ] spectacle / wonder
- [ ] visible advantage verification
- [ ] ceiling anticipation / rule exception / new affordance
- [ ] geography、exploration、mystery、knowledge、power layer、social/status layer
- [ ] faction、civilization、history、time、ontology、cosmic layer、institution/governance
- [ ] 新元素、旧机制新用途、组合、新鲜感、旧资产再激活
- [ ] 没有把换地图自动解释成治理

## E. Desire / Social / Resource

- [ ] private / immediate / self-chosen / imposed goal
- [ ] identity、status、curiosity、ambition、freedom、revenge、belonging、affection
- [ ] responsibility 仅在来源真正表现为核心结构时记录
- [ ] team、friendship、romance、family、mentor、rival、recognition、reputation、belonging
- [ ] scarcity、abundance、windfall、production、monopoly、exchange、ownership
- [ ] resource liberation / transformation / irrelevance / new tier

## F. Optional Constraints / Long Form / Fatigue

- [ ] hard boundary、resource requirement、opportunity cost、sacrifice、exposure/social cost
- [ ] depletion 或 `no meaningful cost`
- [ ] 成本是否真正改变人物选择；否则删除或写 `NOT_MATERIAL`
- [ ] 支撑 500+ / 1000+ 章的结构
- [ ] loop 如何换阶段、旧资产/人物如何继续有价值、结算后如何开新 phase
- [ ] `OBSERVED_REPETITION` / `OBSERVED_STRUCTURAL_WEAKNESS` / `INFERRED_RISK` 分开

## G. Anti-Bias Semantic Gates

- [ ] Payoff Removal Test：能一句话说出读者爽、期待或好奇在哪里
- [ ] Constraint Subtraction Test：删除 cost/constraint/scarcity/responsibility/governance/institution 后，DNA 仍有 payoff、ability、wonder、advantage、status、exploration、mystery、novelty、desire
- [ ] Professional Operations Replacement Test：修炼/魔法/超能力替换为设备/工厂/企业后，不能仍然几乎完全成立
- [ ] Governance Default Test：世界扩大不自动归因于 group → institution → governance
- [ ] Responsibility Default Test：主角变强不自动推出责任增加
- [ ] Cost Necessity Test：成本必须改变选择，否则不写
- [ ] Pure Upside Check：主动寻找完整奖励、能力碾压、新能力试玩、身份跃迁、财富释放、探索自由和纯享受窗口

## H. Arc / Observation

- [ ] Arc 的 `span_kind` 是 `CONTIGUOUS_ARC` 或 `LONGITUDINAL_TRAJECTORY`
- [ ] local problem、setup、promise、action、action-space change、progression、payoff、verification、novelty、aftermath、future opening
- [ ] optional pressure/cost 与 payoff 分开
- [ ] 每本 6–12 个高价值 atomic observations
- [ ] 每条 observation 只有一个发现，不重复 Book DNA
- [ ] 每条 source claim 有 `source_book_id`、`source_id`、`segment_id` 和行号

## I. Cross-book QA

- [ ] Creative problem explicit
- [ ] source count / category count / evidence scope / maturity explicit
- [ ] positive reader payoff / applicability / when-not-to-use explicit
- [ ] 至少一个 alternative solution 或 contrast case
- [ ] 没有来源身份泄漏、普遍化小样本、长引文或可检索正文
- [ ] 没有 mandatory cost / scarcity / governance / responsibility
- [ ] failure basis 标明 observed 或 inferred
- [ ] 所有 locator resolve
- [ ] Evidence 不足时写 Knowledge Gap，不制造 pattern

## J. Package / Publication

- [ ] Markdown frontmatter 符合 `reference-corpus-card-v1`
- [ ] machine/cards.jsonl、evidence.jsonl、dependencies.jsonl、corpus-package.json 存在
- [ ] manifests 按 26 个 source_book_id 存在
- [ ] stale 依赖传播只影响 reference cards，不升级为 Canon
- [ ] `canon_committed=false`、`edition_activated=false`
- [ ] 原文、book/、Canon、数据库未修改
- [ ] `novel corpus semantic-validate`、`compile`、`audit`、`stats` 和 targeted tests 实际运行并记录
