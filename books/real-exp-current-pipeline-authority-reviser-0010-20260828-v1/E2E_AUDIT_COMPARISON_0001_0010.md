# E2E Audit Comparison｜Current Production Pipeline｜Ch1—10

## 结论

本轮使用 current production：

`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`

并保持同一套已审计的 World / Power / Human / Character；Story Program 使用上一轮 current-production 已验证版本，Outline 用当前 Luna high + 当前 Outline retrieval 重新生成。

**总体判断：DIRECTIONAL PASS / 明显改善，但没有完全解决旧审计。**

旧 `SUBJECTIVE_AUDIT_0001_0010.md` 中最重要的 Reader Appetite、Human desire、Fantasy Possession、World desire、Ch10 程序化结算问题，大部分在新十章中有实质改善；但实验同时暴露三个仍需修的 production residual：

1. **Authority Reviser 没有稳定执行 Frozen Power > Curator / Primary 的事实优先级**：Ch2、Ch6 最终正文仍残留“分开期间实时共享另一具身体感觉/疼痛”的错误，而 Frozen Power 明确规定只有重新接触后才一次性回流经验、记忆与伤势。
2. **Stage Settlement 的 process bias 没彻底消失，只从旧 Ch10 部分前移到新 Ch9**：新 Ch10 已从“统一说明大会”变成阮青缨本人带四倍报酬短契上门，这是明显成功；但 Ch9 后段仍花较多篇幅写领队逐人登记、问路线、重写记录，再靠记录完成社会重新估价。
3. **Opening overcorrection**：为了更早兑现“一人同时过两份生活”，新 Outline 把外部公开高光推迟到 Ch3—4；旧版第一章就公开超标、被重新估价、很快进入钱/身份链。新开篇更独特，但商业爆点更慢，不是无条件优于 baseline。

此外，Authority Reviser 在若干章节会删除本来正确且有味道的 Core Fantasy / relationship microbeat；Preservation First 方向正确，但仍存在轻度“事实变准、文本变平”的风险。

---

## 实验设计

### Frozen upstream

- `WORLD_VISION.md`：与旧十章审计书相同。
- `POWER_SEED.md`：与旧十章审计书相同。
- `HUMAN_SEED.md` / `CHARACTER.md`：与旧十章审计书相同。
- Story Program：使用上一轮 current-production 已验证的 `STORY_TREATMENT` 版本，已经包含 Reader Appetite / Human desire / Fantasy Possession / Personal Myth / real-loss window 等 production 根修。
- Outline：当前 Luna high + 当前 Outline retrieval 新生成。

### Chapter runtime

每章真实执行：

1. Luna high Director
2. Luna high Curator
3. Terra high Primary Draft
4. Luna high Authority Reviser
5. adopt `authority_reviser` as `final_source`
6. Luna low State

raw GBrain 在章节 runtime OFF。

### State closure test

每章给 State API 的页面正文故意传入错误 marker；State 必须从 Run Ledger 重新读取 adopted final source。

结果：10 / 10 章 `final_source = authority_reviser`，10 / 10 `run_status = completed`，错误页面 marker 没有进入 State Prompt。

**State source closure：PASS。**

---

# 一、旧审计问题逐条复验

## 1. Core Fantasy 只兑现“同时做两件事”，没有真正兑现“两种人生”

### 结果：**PASS for reader experience；Authority consistency PARTIAL**

新 Ch1 就直接写：

- 一具身体留客舍记账、接待住客；
- 一具身体去武馆练刀；
- 重新合并后账目、收房、练刀手感一起回到顾临川；
- 双份疲劳也同时回收。

这比旧版前五章主要用分影“同时守两个位置 / 双打 / 取货”更接近本书真正独有的幻想：

> **别人一天活一天，顾临川可以在同一天经历两份生活。**

Ch6—8 又继续把分影推进到真正不同的两条行动线：本体护药队 / 影身找陆绾、进入石城；Ch8 两边分别救人、拿兵、带观日宗弟子撤离，最后合并结算。

### 但出现严重 authority residual

Frozen Power 明确：

> 分开期间，两具身体的经验不会互相干扰；重新接触后，经验、记忆、熟练与伤势一次性回流。

Primary 在 Ch2 写成分开期间本体能实时感觉武馆影身；Authority Reviser 改掉了部分错误，但最终仍保留：

> “客舍里顾临川能隔着一层薄薄联系听到武馆。”

以及：

> “能感觉到影身退让时那一下发沉的脚步。”

Ch6 最终正文再次出现：

> “远处追入峡谷的影身也跟着顿了一下。”

和：

> “药车右侧的伤口和撞击感正不断从另一边传来。”

这与 Frozen Power 直接冲突。

因此：

- Core Fantasy realization：**PASS**
- Authority Reviser 对 Power truth 的 correction：**PARTIAL / 未解决**

---

## 2. 顾临川 / 陆绾被净化成理性、负责、成熟协作者

### 结果：**PASS on matched scenes，明显改善**

新十章中私人欲望不再只停留在 Human Seed。

### Ch4

顾临川刚拿到契约和第一笔钱后主动让陆绾看见分影；场景保留：

> 夜里的药草气味顺风飘来，清苦里带一点凉意。

不是只剩“药队职责 / 工作边界”。

### Ch5

陆绾坚持继续去折日峡时，正文明确写：

> 她不回头等谁替她做决定；药草气味被晨风吹过来。

顾临川的路线选择因此不是纯护送责任。

### Ch8

顾临川把陆绾从错影里拉出来时：

> 她身上药粉、风尘和晒热布料的气味贴过来。

这是 Frozen Human 中原本被旧正文净化掉的具体 attraction cue。

### Ch9

陆绾近身处理伤势时：

> 她靠得很近，发梢乱着，身上仍带药粉、风尘和晒热布料的味道。

顾临川还明确承认：

> “短兵值钱，也够利。我想要。”

以及：

> “你被拖进断门的时候，我也不想看着你死在里面。”

他没有把自己包装成“责任 / 大义优先”的正确人物。

词面辅助也支持直接阅读结论：旧十章 `气味` 0 次，新十章 3 次；`想要` 1 次，新十章 4 次。

### Residual

人物对话仍偏清楚、成熟、边界感强；例如 Ch9 的“进危险地方先告诉你”“别拿影身当不用算代价的命”仍有一些关系协议感。

所以本项对“私人欲望被完全净化”的问题已经 **PASS**，但“人物声音 / 情欲张力 / 非平均表达”尚未完全到顶级。

---

## 3. 世界只有危险，不够让读者想进去、想拿东西

### 结果：**PASS in this sample**

旧 Ch6 最大问题是观日宗 / 顾斜阳 / 古代石城第一次进入，却被药车、窄坡、撤退路线抢走。

新结构把层次重新分配：

- Ch6 负责分影两线正式分开 + 找到石城 / 陆绾；
- **Ch7 才正式承担观日宗 / 传承 / 顾斜阳 / 兵室的 Reader Appetite。**

Ch7 直接说明：

- 观日宗公开传授影术，但石城里的失落传承不是对外武馆那套；
- 顾斜阳就是为了宗门失落传承守在石室门外；
- 兵室里一对乌沉短兵只是擦过顾斜阳，就划开其影甲；
- 顾临川马上理解：**这东西能破二阶影甲，而且是一对。**

章节直接停在：

> 往左，是短兵。往右，是陆绾。

这里读者已经先馋上东西，选择才有重量。

Ch10 下一层世界入口也具体：

- 沉昼城；
- 无影正午正在扩大；
- 阮青缨亲自来找；
- **四倍普通护卫报酬**；
- 足以租独立小院、留自由钱。

世界从“更危险”明显升级成“更危险，但也更想进去”。

本项：**PASS。**

---

## 4. 前十章 Access / Identity 多，Fantasy Possession 少

### 结果：**PASS**

旧十章主要拿到：

- 契券；
- 钱；
- 正式护卫身份；
- 外围试学资格；
- 下一层组织入口。

新十章 Ch7 先建立兵器价值，Ch8 主角真正取得：

> **一对能切开二阶影甲的乌沉短兵。**

而且不是“拿到后以后再证明”，是当场切开异兽甲片、救人、撤出石城。

同时 Ch8 合并后正式踏入二阶。

这使十章内的升格不再只是“别人给我一张资格牌”，而是：

> **我本人已经更强，而且腰间真的多了别人会眼馋的东西。**

辅助文本也很明显：旧十章几乎没有这种物件，新十章 `短兵` 出现 35 次，说明它已经成为实际故事对象而非后台 Reward label。

本项：**PASS。**

---

## 5. 第10章阶段结算退化成统一说明 / 报告 / 责任记录

### 结果：**PARTIAL PASS；Ch10 修好，但 process bias 前移到 Ch9**

### 新 Ch10：明显成功

旧 Ch10 的主体是：

- 谁说明什么；
- 谁承担什么；
- 纸上怎么记录；
- 通过报告获得资格。

新 Ch10 变成：

> 阮青缨本人驾黑篷车到营地 → 直接重新估价顾临川 → 拿出沉昼城短契 → 四倍普通护卫报酬 → “你已经不是铜羽随手能替换的临时护卫” → 新世界欲望。

这正是旧审计要求的：

> **少写责任说明，多写升格本身。**

文本辅助：旧十章 `报告` 3 次，新十章 0；`统一说明` 1 → 0；`责任` 1 → 0；`契券` 26 → 13。

### 但 Ch9 仍有明显 process carrier

Ch9 后段仍写了：

- 领队蹲在营地中央逐人记册；
- 先记药车、药箱、伤员；
- 三名弟子分别说石城路线；
- 领队确认“两边同时”；
- 划掉原行、重新写一页；
- “这份记录我会带回去”；
- 章末用“记录已经不再把他当普通护卫”结算社会重新估价。

虽然比旧 Ch10 短，而且前面已经有陆绾关系与顾斜阳 Rival 场景，但这仍是同一个模型偏置的残留：

> **Social Repricing → record / procedure。**

因此不能判完全解决。

本项：**PARTIAL PASS。**

---

## 6. Personal Myth / delayed recontextualization 太弱

### 结果：**DIRECTIONAL PASS in Story Program；Ch1—10 不能证明正文兑现**

当前 Story Program 已经规划：

- 早年陌生护卫留下的普通铜扣；
- 黑峡关旧影中再次出现同类扣件；
- 多年后确认它只是古建筑常见扣件，不是命定信物；
- 到无光海，它能暂时固定错位旧门，真正改变当前行动；
- 使用后彻底断裂。

这是符合本轮目标的 protagonist-level recontext：普通旧物后来有分量，但不做隐藏血统 / 命定继承。

但新 Ch1—10 正文里铜扣没有出现，也还没到 delayed recontext 的时间尺度。

所以本轮最多能证明**长期规划层已修**，不能证明正文 100+ 章会稳定回收。

本项：**DIRECTIONAL PASS。**

---

# 二、其它旧审计重点

## Rival / 顾斜阳作为 Reader Ruler

### 结果：**DIRECTIONAL PASS / 仍不够硬**

新 Ch7—9 比旧版明显更有分量：

- 顾斜阳持长剑；
- 能让影甲覆住双腿、腰腹、手臂；
- 正面抗住石甲异兽；
- 短兵擦过他的影甲，读者立刻知道这对兵器有多值；
- 他拥有宗门传承的正当争夺目标；
- Ch9 会直接对刚进二阶、重伤的顾临川说“你还敢跟我说这话？”

但正文仍没有明确告诉读者：

- 顾斜阳自己究竟几阶；
- 在观日宗年轻一代的名次；
- 一个可直接记住的公开战绩。

所以他已经比旧版更像 Ruler，但还没完全达到“看到他就知道主角还差多远”。

**DIRECTIONAL PASS。**

---

## Prose 辨识度 / 模型平均手势

### 结果：**NOT SOLVED**

旧审计提到：

- “看了一眼”
- “没有立刻回答”
- “点了点头”
- “声音很平 / 沉下来”

新 Pipeline 主要解决 authority / attention / omitted realization，没有针对通用 prose voice 做根修。

辅助计数甚至没有改善：

- `看了一眼`：15 → 17
- `沉默`：1 → 7
- `点了点头`：2 → 4

这不是说新正文更差，而是证明 Authority Reviser **不是 prose-style humanizer**，也不应该被要求承担这个职责。

本项：**FAIL / 未解决。**

---

# 三、Authority Reviser 本身的真实表现

## 明显成功

### 1. State closure

10 / 10 final source 都是 `authority_reviser`，10 / 10 State 都以 adopted final prose 为来源。

**PASS。**

### 2. Mission correction

Ch2 Primary 把 Mission 写反：Primary 让本体去武馆、影身留客舍；Frozen Mission 要求本体留客舍、影身去武馆。

Reviser 把整段改回正确角色分工。

**Mission Preservation：PASS。**

### 3. Reader / Human recovery

Ch8 revision 明确加入了 Human Authority 支持的：

> “药粉、风尘和晒热布料的气味贴了过来。”

同时保留救人和取兵主事件，没有升级成恋爱剧情。

**bounded Human recovery：PASS。**

### 4. Action compression

Ch8 Primary 3254 chars → Reviser 2615 chars，删掉大量重复动作说明和“这不是提前算好”式解释，但保留：

- 短兵第一次证明；
- 陆绾救出；
- 三名弟子撤离；
- 影身独立改路；
- 合并伤势；
- 二阶升级。

属于成功的 Attention Reallocation。

### 5. Ch10 Deletion Discipline

Ch10 Primary → Revision similarity 约 0.976，阮青缨招募、四倍报酬、沉昼城入口、章末决定全部保留，没有重演实验中“看到报告流程就把整个招募结尾一起删掉”的错误。

**Consequence Preservation：PASS on Ch10。**

---

## 真实残余

### A. Frozen Power correction 不彻底

这是本轮最重要的 Authority Reviser bug。

它能够修 Mission，却没稳定修掉 Primary / Curator 中与 Frozen Power 冲突的“实时共享另一具身体经验/疼痛”。

Ch2、Ch6 均有最终正文证据。

**判定：FAIL on strict Power Authority precedence。**

### B. Preservation First 仍偶尔 over-edit

10 章 Primary→Reviser 平均文本相似度约 0.906；多数章节很克制，但：

- Ch1 similarity ≈ 0.797；
- Ch8 similarity ≈ 0.814。

Ch8 大幅删减总体正确；Ch1 则暴露过删。

Primary Ch1 有一句非常好的 Core Fantasy realization：

> **“他比一个人多活了一段午后。”**

问题只是 Primary 把它放在两具身体尚未重合前、并混入实时共享体验，位置不合法。

理想 revision 应该：

> 删除“分开时实时共享”的假机制，**把“多活一段午后”迁到合并后的合法 realization 点。**

实际 Reviser 直接删除了这句，只留下“账册数字、收房动作、出刀手感一起沉回身体”。事实更准，但 Core Fantasy 的记忆点变弱。

Ch9 也删除了几处不明显违反 Authority、但有角色温度的句子，例如：

- “两件事都是真的。”
- “那句‘活着拿回来’落在耳里，比药粉还要烫一点。”

部分删除可能是为了避免过度浪漫化，但至少说明 Reviser 仍会把“局部校正”变成“顺手克制”。

**判定：Preservation First = PASS directionally, not perfect。**

### C. Reviser latency 很高

本轮 completed 10 章平均 wall-clock：

- Director：约 32.9s / 章
- Curator：约 87.9s / 章
- Terra Primary：约 53.1s / 章
- **Luna high Authority Reviser：约 137.8s / 章**
- State：约 23.5s / 章

Authority Reviser 是默认章节链里最慢节点，约为 Terra Primary 的 2.6× wall-clock。

这不是质量失败，但以后做产品 latency / 模型 effort A/B 时应单独考虑。

---

# 四、一个新的上游回归：Opening 变慢

这是本轮不能忽略的负面变化。

旧版：

> Ch1 公开招募 → 分影在众人面前第一次爆发 → 一边救场、一边击败对手 → 立即被重新估价。

旧版的优点是商业高光极早。

新版 Outline：

> Ch1 客舍 + 武馆，两份生活第一次成立  
> Ch2 双线账目 / 正式对练  
> Ch3 才进入公开试场  
> Ch4 连赢后拿随队契约 + 第一笔钱

新版更早让读者理解“一个人同时活两份人生”，这是旧审计最想补的幻想层；但同时把：

> **Core Power → Public Proof → Repricing → Money / Identity**

从第一章拉到了第三、四章。

这不是 Authority Reviser 的问题，而是 **Story Program / Outline 为了补 life privilege 发生 overcorrection**。

因此不能说“新十章全面优于旧十章”。更准确的是：

- Ch4—10 的 Reader Appetite / reward / world desire / relation 明显更成熟；
- Ch1—3 的独特幻想更好，但商业爆点更慢。

**Opening：PARTIAL / trade-off，不应冻结当前 exact pacing。**

---

# 五、逐章主观判定

| 章 | 当前判断 | 主要改善 / 问题 |
|---|---|---|
| Ch1 | **中上 / PARTIAL** | “一人两份生活”第一次直接成立；但外部高光被推迟，Reviser 删除了一句很强的 Core Fantasy realization |
| Ch2 | **中上 / PARTIAL** | 合并后把失败经验变成新动作很好；Reviser修正 Mission 分工，但仍保留违反 Frozen Power 的实时感知 |
| Ch3 | **强 / PASS** | 放下客舍一边、进入公开试场；公开成长正式开始，Reviser改动克制 |
| Ch4 | **强 / PASS** | 连胜 → ruler → 契约 → 第一笔钱；陆绾 Human cue 自然进入；但旧版同类 payoff 来得更早 |
| Ch5 | **中上 / PASS** | 真正离城、陆绾路线改变主角选择，私人气味保留；世界入口清楚 |
| Ch6 | **中上 / PARTIAL** | 双线正式分开，旧“观日宗被撤退路线抢戏”被结构拆开；但 Power 实时痛觉错误仍存在 |
| Ch7 | **强 / PASS** | 观日宗 / 传承 / 顾斜阳 / 兵室全部成为 Reader Desire；“左短兵 / 右陆绾”选择很清楚 |
| Ch8 | **强 / PASS** | 真正拿到一对短兵、现场证明、救陆绾与弟子、进入二阶；Reviser压缩总体有效 |
| Ch9 | **中上 / PARTIAL** | Human desire、Rival、伤势结算都比旧版好；但后段又回到记录/册子/逐人说明，且 Reviser删掉少量正确情绪质感 |
| Ch10 | **强 / PASS** | 彻底摆脱旧统一说明大会；阮青缨本人上门、四倍价钱、沉昼城入口、新欲望，非常接近旧审计期待的阶段升格 |

---

# 六、旧审计问题最终矩阵

| 旧审计问题 | 新十章结果 |
|---|---|
| Core Fantasy 没吃满“两种人生” | **PASS**，但 Frozen Power consistency **PARTIAL** |
| 人物被净化成负责成熟协作者 | **PASS on matched scenes** |
| 世界危险 > 世界诱惑 | **PASS** |
| Fantasy Possession 太少 | **PASS** |
| Ch10 / 阶段结算程序化 | **PARTIAL PASS**：Ch10 修好，Ch9 残留 |
| Personal Myth 弱 | **DIRECTIONAL PASS in Story Program；十章无法验证正文回收** |
| Rival 分量不足 | **DIRECTIONAL PASS** |
| Prose 作者味 / 通用手势 | **FAIL / 本轮未解决** |
| State final-source 闭环 | **PASS 10/10** |
| Authority Reviser Preservation First | **DIRECTIONAL PASS / 有 over-edit residual** |
| Authority Reviser strict Frozen Power correction | **FAIL / 需要修** |

---

# 七、最终判断

如果只问：

> **新的 Pipeline 有没有改善旧十章？**

答案是：**有，而且 Ch7—10 的改善很明显。**

尤其：

- 世界开始真的让人馋；
- 十章内终于有真正属于主角的超凡兵器；
- 陆绾和顾临川终于有身体 / 气味 / 私人欲望，不只剩职责；
- Ch10 从行政结算变成四倍报酬 + 高阶人物亲自招募 + 沉昼城新世界入口；
- State final source 的数据闭环真实生效。

如果问：

> **旧审计提到的问题是否已经全部解决？**

答案是：**没有。**

最该继续处理的不是再加更多审计规则，而是三个最小 residual：

1. **Authority precedence**：Frozen Power / Human / World 与 Curator / Primary 冲突时，Reviser 必须完成整章一致性修复，不能只修一半；本轮最明确的是“分开期间实时共享经验/疼痛”。
2. **Preserve high-value correct realization**：一个好句若只是位置依赖错误，应在最小范围内迁到合法点，而不是删除；特别保护 Core Fantasy / Relationship payoff。
3. **Outline settlement + opening balance**：阶段结算不把 process tax 从 Ch10 搬到 Ch9；同时把“一人两份生活”加入开篇时，不要牺牲原来 Ch1 的 Public Proof / Repricing 爆点。

当前版本可以评价为：

> **Reader Appetite / Human Desire / Fantasy Possession / Ch10 payoff 已跨过旧审计主要短板；Authority Reviser 架构是有效的，但还没有达到“远端 Authority 必修正、正确高价值正文必保留”的最终稳定态。**

因此本轮整体：**DIRECTIONAL PASS，不能直接宣告审计问题全部关闭。**
