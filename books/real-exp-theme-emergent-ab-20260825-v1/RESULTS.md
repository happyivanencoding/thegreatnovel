# Theme Emergent A/B 三书实验报告（Clean Pass 2）

## 结论

**B 在清洗后的正式对照中再次 3/3 全胜。** 独立 GPT-5.6 Luna high 盲评平均：A **4.57/10**，B **8.63/10**。

这次结果支持上游诊断：当前 production 的主要问题不是“文字用了抽象词”，而是 **Fantasy Seed semantic escalation → World 的能力/世界同构 → Story Program 的 same-meaning-bigger-scale** 共同形成“抽象意义提纯器”。

B 没有新增 Reviewer、Hard Gate、scorer 或模型调用，只重新划分三个生成阶段的职责：

- Seed：优先“我想拥有什么、怎么玩、得到什么”，远期仍推具体用法、目标、地图和获得，不寻找终极意义；
- World：先让没有主角的世界自己成立，再寻找核心优势的切口；
- Coordinate：固定参考只允许 reader-facing `POWER / TECHNIQUE / THREAT / STATUS / VALUE / WORLD`，不让 `ACTION_SPACE / EXPECTATION_LADDER / IMPACT / MYSTERY_DEPTH` 变成世界材质；
- Program：阶段由具体人物、资源、功法、兵器、位置、地图、敌人和机会发动，不逐级证明同一个抽象命题。

## 冻结条件

- 三个作者粗方向在生成前冻结，不包含哲学主题或指定金手指。
- A = 当前 production `Seed → World → Program`。
- B = experiment-only Theme Emergent projection；**没有在实验前修改 production creative prompts**。
- 每本 A/B 都固定继续 Candidate 1，不事后挑选。
- Seed：GPT-5.6 Luna high，GBrain OFF。
- World：GPT-5.6 Luna high，GBrain ON，固定 Coordinate + creative inspirations。
- Program：GPT-5.6 Sol high，GBrain ON。
- Blind Judge：GPT-5.6 Luna high，X/Y 顺序预先打乱。

## 实验卫生：为什么有 Clean Pass 2

第一次 Story Program 与盲评完成后，交付检查发现部分 ACP World 输出末尾自动附带 `<oai-mem-citation>` 辅助元数据，其中包含“避免后台概念进入世界”等摘要。它不是小说正文，但由于 5/6 World 带有且内容不完全相同，会造成轻微不对称污染。

因此：

1. Seed 与 World **不重生成**，保持同一真实模型结果；
2. 从 materialized World 中统一剥离全部 `<oai-mem-citation>`；
3. 确认 6 个 clean Program prompts 中此标记命中数为 **0**；
4. 用原模型、原 GBrain、原 Seed/World 重新跑全部 6 个 Sol Program；
5. 从 clean Program 重建 X/Y，再重新跑 3 个独立盲评。

Pass1 全部保留为 `*_pass1_with_world_meta.*` 审计材料，不作为最终分数。Clean Pass 2 仍然 3/3 选择 B，因此主要结论没有依赖该辅助元数据。

## 三组正式结果

| Book | A | B | A score | B score | Winner |
|---|---|---|---:|---:|---|
| 1 | 《立界成律》 | 《战器回响》 | 4.1 | 8.8 | B |
| 2 | 《荒律狩身》 | 《战痕锻身》 | 4.1 | 8.6 | B |
| 3 | 《夺势者》 | 《败者战痕》 | 5.5 | 8.5 | B |

### Book 1

A：`雨线至山门 → 无籍入城 → 古战场换印 → 裂域开门 → 无光异天 → 诸天之间，自界初成`。

B：`雨夜断枪 → 外门夺兵 → 霜墙血战 → 沉城退潮 → 澜河夺炉 → 九兵破冢 → 坠星兵城`。

盲评根因：A 把哲学命题当世界生成器；B 把金手指作为进入一个本来就有资源、欲望与利益的世界的工具。

### Book 2

A：`盐驿之外，第一次夺路 → 深荒争猎，谁有资格带走机会 → 古灾过境，移动的禁地 → 众势围荒，谁能决定生路属于谁 → 古域逐生，普通生命是否有资格进入 → 边壳之外，新的生命可能`。

B：`断刀归手 → 古兵冢夺胚 → 雷翼断河 → 赤沉复战 → 六兵葬原 → 古战区星坠`。

A 仍然逐渐把“荒境适应”扩大成“谁有资格规定什么生命能行动”；B 仍围绕猎兽、父刀、古战场、铸兵与具体边荒竞争运行。

### Book 3

A：`拒风关，逆行斩旗 → 战功不是卖身契 → 旧关无真门 → 万人改道 → 九州易势 → 断天开路`。

B：`雨巷夺令，郡城登台 → 外院夺首，山门争产 → 铁脊开炉，矿城夺火 → 雪关断粮，百骑夺旗 → 九营会武，王库夺枪 → 百舟猎鲸，沉潮铸槊 → 天门十战，古阵翻案`。

A 继续把一击“夺势”放大到战局、军权和天下方向；B 让战痕服务武馆、武院、矿争、战争、军职、远海与天下擂台。

## 辅助词面指标（方向证据，不是评分器）

固定词表统计每本 `Seed + World + Program`：

- 哲学/后台抽象词：A 平均 **23.7**，B **3.3**，B 约低 **86%**；
- 具体世界/获得物词：A 平均 **190.3**，B **637.7**，B 约为 A 的 **3.4×**。

单本 raw counts：
- Book1 A `28 abstract / 187 concrete`；B `5 / 575`；
- Book2 A `31 / 141`；B `1 / 558`；
- Book3 A `12 / 243`；B `4 / 780`。

## Final clean pass 成本与 wall-clock

按当前 Codex credits 估算（Luna input/cached/output = 5/0.5/30；Sol = 125/12.5/750 per 1M）：

- A 三书 clean chain：约 **32.75 credits**；
- B 三书 clean chain：约 **26.95 credits**；
- clean blind judges：约 **1.00 credits**。

平均单阶段 wall-clock：

| Stage | A | B |
|---|---:|---:|
| Seed Luna high | 150.4s | 157.2s |
| World Luna high | 145.0s | 165.4s |
| Program Sol high | 384.7s | 508.5s |

B 质量提升并不意味着更低 latency；本轮 B Program 仍明显更慢。成本差异也受 cache 命中影响，不能把一次结果外推为固定价格优势。

由于第一次 Program/盲评因元数据污染被作废但实际已经消耗，**本次整个实验真实估算消耗约 117.70 credits**；最终质量结论只使用 Clean Pass 2。

## B 仍存在的重要风险：核心玩法类型同质化

B 三本分别是 `战器回响 / 战痕锻身 / 败者战痕`。世界、人物目标和长期阶段已经显著不同，但金手指仍集中在“战斗痕迹 / 技法采集 / 回响”家族。

这不能被 3/3 胜利掩盖。三个冻结方向本身都偏战斗，所以还不能判定为新的 production bug。下一步生产化前后应使用 **三个非战斗中心方向** 做一次便宜 diversity regression，检查 Seed 是否会继续自动收敛到技能复制/采集。

正确处理不是重新加入抽象主题制造差异，而是继续使用已有候选差异原则：主角反复做什么、转化什么、获得什么、世界为何扩大，必须真正不同。

## Production 建议

结果足以支持 **Theme Should Be Emergent, Not Generative** 的系统修复方向，但上线时不应照搬 B 的实验附加字段：

1. **Fantasy Seed**：重写现有 `远期升格方向 / 世界扩张欲望`，切断“玩法 → 终极意义”，保持原 schema；
2. **World Vision**：把“世界无主角也成立”和“具体价值物”压回现有 `世界核心规则 / 世界资源利益 / 持续冲突`，不永久新增一级区块；
3. **Coordinate Reference**：固定槽保留，但 production projection 只允许 reader-facing 尺，后台尺度不得成为世界材质；
4. **Story Program**：不新增 `重要获得/占有/使用` permanent field；把语义合并进现有 `当前目标 / 阶段净新增 / 核心幻想兑现`；
5. **Outline Theme**：`## 11` 改为 derived/posthoc；没有自然主题时允许“暂不预设”，不得反向决定资源、敌人、world ontology 或终局。

即：**replacement / compression，不是再叠一层 Anti-Philosophy checklist。**

## 最终判断

这次 A/B 已经回答了核心问题：

> **“主题后验浮现”不是牺牲创意深度换俗气；它反而让金手指更想拥有、世界更像真实世界、长期故事更有可追的具体对象。**

但 B 还不是可以原样复制进 production 的 Prompt。应该生产化它的**职责分工**，同时继续约束 Prompt 膨胀，并用非战斗方向复验玩法多样性。
