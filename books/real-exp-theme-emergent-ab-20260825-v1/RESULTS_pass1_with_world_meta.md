# Theme Emergent A/B 三书实验报告

## 结论

**B 以 3/3 全胜通过这次 A/B。** 独立 Luna high 盲评平均分：A **4.53/10**，B **8.73/10**。

这次结果支持最初诊断：当前 production 的主要问题不是“设定词太抽象”，而是 **Fantasy Seed 的 semantic escalation → World 的能力/世界同构 → Story Program 的 same-meaning-bigger-scale** 共同形成了“抽象意义提纯器”。

B 没有靠增加 Reviewer、Hard Gate 或禁词表获胜，而是重新分配三个阶段职责：

- Seed：先找“我想拥有什么、怎么玩、得到什么”，远期仍推具体用法/目标/地图，不寻找终极意义；
- World：先建立没有主角也会运转的具体世界，再寻找核心优势切口；
- Coordinate：只允许 reader-facing `POWER / TECHNIQUE / THREAT / STATUS / VALUE / WORLD`，不让 `ACTION_SPACE / EXPECTATION_LADDER / IMPACT / MYSTERY_DEPTH` 成为世界主尺；
- Program：阶段由人物、资源、功法、兵器、位置、地图、敌人和机会发动，不把同一抽象命题逐层放大。

## 冻结条件

- 三个作者粗方向在生成前冻结；都没有提供哲学主题或具体金手指。
- A = 当前 production prompt。
- B = experiment-only projection；实验前没有修改 production creative prompts。
- 每组每本都固定继续 **Candidate 1**，不事后挑选。
- Seed：GPT-5.6 Luna high，GBrain OFF。
- World：GPT-5.6 Luna high，GBrain ON；固定 Coordinate + creative inspirations。
- Program：GPT-5.6 Sol high，GBrain ON。
- Blind Judge：GPT-5.6 Luna high；Book1/3 X=A Y=B，Book2 X=B Y=A。

## 三组结果

| Book | A | B | Blind score A | Blind score B | Winner |
|---|---|---|---:|---:|---|
| 1 | 《立界成律》 | 《战器回响》 | 4.0 | 8.6 | B |
| 2 | 《荒律狩身》 | 《战痕锻身》 | 3.8 | 8.8 | B |
| 3 | 《夺势者》 | 《败者战痕》 | 5.8 | 8.8 | B |

### Book 1

A 的长期阶段继续围绕：`谁有资格进门 → 强者也须先报条件 → 一条选择横跨异族 → 外来的可能不被抹去`。世界资源虽存在，但越来越像为“立律/选择/规则解释权”服务。

B 的阶段是：`黑石断枪 → 灵铜矿案 → 沉潮古城 → 霜原夺堡 → 九兵破冢 → 坠星兵城`。具体获得包括父亲旧刀、开脉功法、潮炉玄铁、潮纹战刀、军籍、寒髓、百战玄戈、星铁和本命战甲。金手指仍强，但世界不再是它的同义词。

### Book 2

A 从“在荒境活下来”继续升格到“世界无权预先决定什么生命可以行动”，最终阶段直接成为 `生命自定其路`；异兽、灾害、古域都逐渐被解释成同一个“生存定义”命题。

B 则由黑潮、渡口、古战场、灾兽围猎、古战区、九铸城与天外灾夜依次发动。人物争的是父刀、火种功法、兽核、渡炉、古兵胚、灾兽核心、战车、炉坊、陨骨和星兽遗骸。

### Book 3

A 从一击“夺势”推到多人行动、军阵、军权、古战场和 `天下争势`，最后仍在追“时代转向权”。

B 的阶段则围绕武馆债务、赤铜矿、北境粮道、九营军职、海上捕鲸、宗门/古战场与天门十战。奖励非常明确：五百两、武院入学令、赤铜心、重铸刀、军籍、战马、三百精骑、军功田、鲸髓、宗师长枪、父亲遗刀、武神遗迹。

## 辅助词面指标（只作方向证据，不当质量评分）

用固定词表统计三个 `Seed + World + Program`：

- 哲学/后台抽象词命中：A 平均 **29.0**，B 平均 **2.7**；B 约下降 **91%**。
- 具体世界/获得物词命中：A 平均 **198.3**，B 平均 **617.0**；B 约为 A 的 **3.1×**。

单本 raw counts：
- Book1 A `47 abstract / 192 concrete`；B `3 / 592`。
- Book2 A `24 / 145`；B `1 / 538`。
- Book3 A `16 / 258`；B `4 / 721`。

## 成本与 wall-clock

按当前 Codex credits 估算（Luna 5/0.5/30；Sol 125/12.5/750，input/cached/output per 1M）：

- A 三书完整生成约 **30.03 credits**。
- B 三书完整生成约 **29.85 credits**。

成本基本相同。B 并没有靠更贵模型获胜。

平均单阶段 wall-clock：

| Stage | A | B |
|---|---:|---:|
| Seed Luna high | 150.4s | 157.2s |
| World Luna high | 145.0s | 165.4s |
| Program Sol high | 354.8s | 486.9s |

B 的 Program 平均更慢，主要因为输出更具体、更长（B Program output tokens 合计 33857 vs A 28727）。所以 **质量提升不等于 wall-clock 改善**；这是需要接受或后续压缩的工程成本。

## 重要的新风险：B 的核心玩法类型仍有同质化

B 的三本分别是 `战器回响 / 战痕锻身 / 败者战痕`，虽然世界、长期事件和获得物已经明显不同，但金手指都落在“战斗痕迹 / 技法采集 / 回响”家族。

这不能忽略。它说明：

> 修掉“哲学同质化”以后，Seed 可能转而偏好最容易产生直接男频快感的“战斗技能采集”。

本实验的三个作者方向本身也都偏武斗，因此不能把它直接判断成新的 production bug。上线前/上线后应再用 **非战斗中心的三个方向** 做一次便宜 diversity regression，确认不会统一收敛到技能复制/采集。

正确处理方式不是重新加入抽象主题来制造差异，而是继续用已经存在的候选差异原则检查：**主角反复做什么、转化什么、获得什么、世界为什么扩大** 是否真正不同。

## Production 建议

实验结果足以支持 **Theme Should Be Emergent, Not Generative** 的上游修复方向，但 production 化时不应照抄 B 的额外字段，避免 Prompt/Schema 膨胀：

1. **Fantasy Seed**：重写现有 `远期升格方向 / 世界扩张欲望`，删除“终极意义推导”；保留原 schema。
2. **World Vision**：把“无主角也成立”和“具体价值物”合并进现有 `世界核心规则 / 世界资源利益 / 持续冲突`，不要长期新增两个一级区块。
3. **Coordinate Reference**：固定槽保留，但 production projection 只允许 reader-facing 尺；后台尺度不进入世界材质。
4. **Story Program**：不新增 `重要获得/占有/使用` 字段；把这层要求并入现有 `当前目标 / 阶段净新增 / 核心幻想兑现`。
5. **Theme**：后续 Outline 的 `## 11` 只能后验总结已经形成的故事；不明显时允许“暂不预设”，不得反向决定资源、敌人、世界 ontology 或终局。

也就是说，真正生产化应该是 **replacement / compression**，不是继续往 Prompt 上叠 Anti-Philosophy checklist。

## 独立盲评共同结论

三名独立 judge 都指出同一差异：

> A 让读者追随一个哲学机制不断放大；B 让读者不断想得到具体东西、使用具体东西、展示具体胜利，同时世界本身也在运转。

同时三次都提醒 B 的下一风险是：不要退化为“收集更多招式/兵器 → 打更强敌人”的刷图循环。这个风险应由现有 Plot Engine Diversity / Contestable Choice / Character autonomy 处理，不需要新增新的 Reviewer 或 Hard Gate。
