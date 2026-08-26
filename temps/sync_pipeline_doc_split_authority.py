from pathlib import Path

path = Path(r"docs/PIPELINE_METHODOLOGY_AND_VALUES.md")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "`Fantasy + Gameplay → Independent World + Desire Economy → Relationship / Plot Reconfiguration → Narrative Compounding → Story Anchors → Chapter Execution`",
    "`Independent World → Split Power / Human Authority → Character Collision → Long-Form Causality → Story Anchors → Chapter Execution`",
    1,
)
text = text.replace(
    "`作者粗方向 → Fantasy Seed → World Vision → Story Program → Outline → Director → Curator → Primary Writer → State Extraction`",
    "`作者方向 → protagonist-blind World Vision → POWER_BASELINE / LIFE_CONTEXT → 独立 Power Seed + Human Seed → deterministic Character → Story Program / Collision → Outline → Director → Curator → Primary Writer → State Extraction`",
    1,
)
needle = "### 2.1 Fantasy First\n\n先回答“读者最想亲自拥有什么”，再回答世界、资源、势力和规则怎样承载它。"
replacement = "### 2.1 Fantasy First\n\nFantasy First 是读者价值优先级，不再是 production 阶段。系统仍先保护“读者最想亲自拥有什么、主角本人怎样真正变强”的承诺，但创意 authority 由 protagonist-blind World、Power Seed 与 Human Seed 分拆承担，避免一个 Seed 同时预先决定世界、能力、Biography 与人生意义。"
text = text.replace(needle, replacement, 1)
text = text.replace(
    "同时遵守 **Narrative Appetite Before Defensive Balance**：创作顺序先寻找最让人眼馋、兴奋、好奇、痛快、恼火或非看不可的东西，再补维持长篇所需的最小边界。Seed 不负责证明所有失控风险已经被堵住；World 才补最小可信边界，Program 再处理长期变异、后果与复利。允许局部明显过量、偏心、不均衡，只要这种“放纵”真正增加本书的独占性阅读欲望，而不是把合理性检查做完以后才看还剩多少爽点。",
    "同时遵守 **Narrative Appetite Before Defensive Balance**：先保护最让人眼馋、兴奋、好奇、痛快、恼火或非看不可的东西，再补维持长篇所需的最小边界。World 负责世界事实，Power 负责力量幻想，Human 负责人本身；Story Program 再处理它们碰撞后的长期变异、后果与复利。允许局部明显过量、偏心、不均衡，只要这种“放纵”真正增加本书的独占性阅读欲望，而不是把合理性检查做完以后才看还剩多少爽点。",
    1,
)

start = text.index("## 3. 每一层到底负责什么")
end = text.index("### Growth Genome：整理，不创造", start)
new_section = r'''## 3. 每一层到底负责什么

### World Vision：先创造一个没有主角也成立的世界

World Vision 是 protagonist-blind：不知道未来主角是谁，也不知道未来 Power Exception 是什么。它仍是一轮 Luna high，不新增 World Reviewer。

#### 负责

- 普通人的生活、上升与失败路径；
- 力量体系的正常值、稀缺度、境界/能力的可观察差距；
- 宗门、王朝、家族、商盟、种族等怎样真实影响人生；
- 世界里真正值钱、值得人物争夺和羡慕的东西；
- 3—6 件即使主角从未出生也会推进的人物行动、战争、迁徙、竞争或灾难；
- 真正值得进入的地点、奇观、危险与未知；
- 普通人 / 专业人士 / 顶层势力各自知道什么。

#### 不负责

- 主角 Biography、欲望、关系原点；
- Core Power / Legal Exception；
- 为未来能力预留“钥匙孔”；
- 主角第一次兑现与终局使命；
- 为证明世界独立而补完整政治经济模拟。

健康判断只问：**没有主角，世界是不是仍有具体的人在做事、具体地方想去、具体东西值得争？** 不再为这个问题增加 production 正交删除测试、Reviewer 或 scorer。

---

### Power Seed：决定“世界正常力量里，主角合法例外在哪里”

Power Seed 只读 deterministic `POWER_BASELINE` 与少量 Power GBrain craft，不读 Human Biography，也不读 named Story Opportunities。

核心语法：

`World Power Normal → Legal Exception → Core Fantasy → Growth Compatibility`

#### 负责

- 一句话能理解、能想拥有的 Core Fantasy；
- 正常修炼轴：世界本来的成长怎样真实增强主角本人；
- Exception mastery：异常掌握怎样扩大具体能力；
- High-Tier Mutation：高阶发生什么真正质变；
- Permanent Boundary：高阶也不会自动消失的边界；
- Legendary Power State：力量体验上限。

#### 不负责

- 谁会得到这个能力；
- 童年、家庭、人格、关系和人生使命；
- Story Opportunities；
- 把能力自然职业化成维修、诊断、运输、审核、构筑或流程管理。

关键原则：**Power Seed = growth grammar。** 它决定“能够怎样成长”，不决定“第几阶段发生”。

---

### Human Seed：决定“这个人原本是谁”

Human Seed 只读 deterministic `LIFE_CONTEXT` 与 Human GBrain craft，不看 Power，也不看 named Story Opportunities。

当前结构：

`Lived Facts → Competing Motives → Stable Choice Bias under conflict → Person-specific Relationships`

#### 负责

- 世界中的初始位置与具体生活事实；
- 2—4 股会长期进入选择、可能互相冲突的私人动机；
- Stable Choice Bias + Variable Realization；
- 能真实改变去留、风险、时间、暴露和机会牺牲的具体关系；
- T0 当前私人欲望（只进入 Mutable State）；
- Audition Hook（非 Canon）。

#### 不负责

- 逐条用 Biography 证明人格；
- 把一生统一成一个 `Core Obsession + Excess`；
- 把人净化成理性、责任、自主、反控制的标准优等生；
- 猜未来 Power 或为外挂预留主题化童年。

**Biography is context, not proof。** 同样的生活事实本来就可能长出不同的人。人物辨识度来自多股动机冲突时反复暴露的选择偏向，而不是漂亮的人生哲学。

---

### Character：确定性组合，不做后验合理化

`CHARACTER.md` 由已冻结 Power Core 与 Human Core deterministic compose，没有 Character Composer LLM。

它只保留两个 authority 并列，不解释“为什么这段童年注定得到这种能力”。World / Power / Human 之间的不协调是后续 Collision 的故事材料，不是需要抹平的错误。

---

### Story Program：Collision + Long-Form Causality Designer

Story Program 是第一次同时看到完整 World 与 Character 的阶段，也是当前默认使用 Sol high 的最高杠杆规划节点。

核心身份不是“小说总体产品经理”，而是：

> **这些已经存在的人、力量与世界，接下来怎样互相改变。**

第一原则：

> **Growth is a longitudinal invariant, not a per-stage form requirement。**
>
> **成长是全书纵向不变量，不是每阶段必填表单。**

#### Authority ≠ Scheduling

- Power Seed 决定 growth grammar；
- Human Seed 决定人物长期选择偏向与 competing motives；
- World Vision 决定世界事实与独立人物行动；
- Story Program 不能重写以上 authority；
- Story Program 必须决定这些已批准潜力在什么故事因果中真正变成现实。

因此：**Power Seed = growth grammar；Story Program = growth realization through story。**

#### 全书级责任

- 5—7 个自然大型阶段；
- 清楚的 **全书成长与 Core Fantasy 兑现脊柱**：4—6 次可观察质变，分布在早期、中期、高阶多个自然阶段；
- 早期第一次成立、中期更强/更不同的新玩法、高阶真实质变必须都可复述；
- 每次成长写成具体事实：以前打不过谁、去不了哪里、做不到什么，现在具体能怎样战斗、移动、探索或使用 Core Fantasy；
- 如果 5—7 个阶段从头到尾都没有真实 Power / Capability progression，即使人物关系很好，也不符合成熟男频成长长篇；
- Core Fantasy 必须周期性重新证明“为什么这项力量仍值得追”，但不要求每阶段升级。

#### 大型阶段发动机

阶段可以主要由任意一种发动：

- **Life**：私人欲望、关系、人生去留、旧后果；
- **Fantasy**：力量、战斗、获得、探索、新玩法；
- **World**：世界本来就在发生的人物行动与大事。

三者不平均配额。一个阶段可以没有境界突破、没有新装备、没有新技能；只要故事因果与 Stage Delta 成立，就可以完整。

#### 当前轻量阶段合同

每个阶段只回答：

1. **为什么现在发生**；
2. **谁想要什么**；
3. **主角的关键选择与行动**；Power 若介入，直接写它怎样改变行动和结果，不单列能力税；
4. **这一阶段真正的阅读满足**；
5. **Stage Delta**：只写真实改变的维度，可包括 Power / Capability、Possession、Relationship、Identity / Access、Knowledge、Enemy State、World State；某维度没变就不写；
6. **下一阶段为何自然发生**。

#### High-Value Acquisition 与 Compounding

二者保留，但从固定 stage schema 降级为纵向 reader-appetite / continuity 原则：

- **High-Value Acquisition**：世界自然出现真正让人想要的剑、功法、身份、同伴、洞府、飞舟、名额或其它高价值对象时，让人物真实争取、占有、使用和可能失去；没有自然机会就不制造；
- **Compounding**：过去得到的力量、物件、关系、身份、知识与入口一旦成立，就必须继续改变后续行动、选择、敌人应对或世界局面；不要每阶段填 `Compounding Growth`，也不要让旧获得写完即消失。

#### 不负责

- 重新定义 Power / Human / World；
- 每阶段强制 `核心优势参与 / 一级成长 / 关键获得 / High-Value Acquisition / Compounding Growth / 净新增`；
- 把 Life / World 事件重新解释成“更好的升级路线”；
- 把同一 Plot Engine 换地图重复六遍；
- 为维持长篇发明未批准的新力量层。

健康的 Program 让读者同时看到：**这个人仍然是这个人；世界仍然大于外挂；主角确实越来越强；过去发生的事情继续改变现在。**

---

'''
text = text[:start] + new_section + text[end:]

text = text.replace(
    "`作者明确要求 > 已批准 Fantasy Seed > 已批准 World Vision > 已批准 Story Program > Outline > Director > Writer`",
    "`作者明确要求 > 已批准 World Vision > 已批准 Power / Human（Character）> 已批准 Story Program > Outline > Director > Writer`",
    1,
)
text = text.replace(
    "参考库从“少量创作提醒”升级成创意权威，导致不同书越来越像同一套蒸馏模板，或 raw reference 继续泄漏到 Writer。Fantasy Seed 默认保持 GBrain OFF；World / Story Program / Outline 只读少量 focused inspiration；章节 Runtime 不直接读取 raw GBrain。",
    "参考库从“少量创作提醒”升级成创意权威，导致不同书越来越像同一套蒸馏模板，或 raw reference 继续泄漏到 Writer。World / Power / Human / Story Program / Outline 只读各自职责内的少量 focused inspiration；章节 Runtime 不直接读取 raw GBrain。",
    1,
)
text = text.replace(
    "`Fantasy Seed → World Vision → Story Program → Outline → Director → Curator → Writer`",
    "`World Vision → Power / Human → Character → Story Program → Outline → Director → Curator → Writer`",
    1,
)

old_table = '''| 阶段 | 默认模型 | GBrain | 说明 |
|---|---|---|---|
| Fantasy Seed | GPT-5.6 Luna high | **OFF** | 保持核心幻想先由作者方向与模型自身产生，避免参考库过早锚定创意 |
| World Vision | GPT-5.6 Luna high | **ON，固定 1 条 Coordinate Reference + 最多 3 条 creative inspiration** | Coordinate Reference 同时保留世界前台尺（Power/Technique/Threat/Status/Value/World）与作者侧读者体验尺（Action Space/Expectation/Mystery/Impact）；后者必须投影成具体故事事实，不作为世界内部命名尺度；固定参考不占 creative 名额 |
| Story Program | GPT-5.6 Sol high | **ON，最多 3 条 focused inspiration** | 当前最值得使用 Sol 的位置：玩法换挡、长线生态、人物自治、敌人策略、高价值获得 |
| Outline | GPT-5.6 Luna high | **ON，通常 4 条，最多 5 条** | 把正确的长期 Program 展开成连续故事锚点、Thread Collision、身份揭露、Reward Recontextualization |
| Director | GPT-5.6 Luna high | 章节相关精选上下文 | 当前 Balanced 默认；与 Terra high 质量接近但成本显著更低，若优先最低延迟可切 Terra high |
| Curator | GPT-5.6 Luna high | Index-first 后的少量相关材料 | Balanced 默认；应继续压短输出合同。若优先最短延迟与更克制输出，可切 Terra medium |
| Primary Writer | GPT-5.6 Terra high | 只读 Curator 输出/Scene Skills | 正文 A/B 中更克制、较少 procedural expansion、更愿意在章节合同位置停下；这是质量/行为选择，不是成本选择 |
| State Extraction | GPT-5.6 Luna low | 不需要创作型 GBrain | 当前成本优先默认；只抽取已发生事实，不需要高级创作推理 |'''
new_table = '''| 阶段 | 默认模型 | GBrain | 说明 |
|---|---|---|---|
| World Vision | GPT-5.6 Luna high | **ON，最多 3 条 focused inspiration** | protagonist-blind World；先让世界自身成立，不读取未来 Power/Human |
| Power Seed | GPT-5.6 Luna high | **ON，Power lane，小 bundle** | 只看 POWER_BASELINE；决定 growth grammar，不看 Human/Story Opportunities |
| Human Seed | GPT-5.6 Luna high | **ON，Human lanes，最多 3 条** | Appetite / Behavior / Relationship 各最多 1 条；不看 Power/named Story Opportunities |
| Story Program | GPT-5.6 Sol high | **ON，最多 3 条 focused inspiration** | Collision + long-form causality；最高杠杆长期结构节点 |
| Outline | GPT-5.6 Luna high | **ON，通常 4 条，最多 5 条** | 把批准 Program 编译成中期故事锚点与 Future 10 |
| Director | GPT-5.6 Luna high | 章节相关精选上下文 | Balanced 默认；若优先最低延迟可切 Terra high |
| Curator | GPT-5.6 Luna high | raw GBrain OFF；Index-first / Scene Skills | Balanced 默认；若优先更短、更克制可切 Terra medium |
| Primary Writer | GPT-5.6 Terra high | raw GBrain OFF；Scene Skills | 正文更克制、较少 procedural expansion |
| State Extraction | GPT-5.6 Luna low | OFF | 只抽取已发生事实 |'''
if old_table not in text:
    raise SystemExit("model table block not found")
text = text.replace(old_table, new_table, 1)

path.write_text(text, encoding="utf-8")
print("PIPELINE_METHODOLOGY_AND_VALUES.md synced to split authority")
