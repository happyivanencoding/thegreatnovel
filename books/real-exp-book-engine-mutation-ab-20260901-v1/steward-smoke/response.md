我会按 `tgn-system-steward 0.3.40` 做 bounded read-only 审计：先读取技能本体及当前仓库状态，再只核对目标 `STORY_PROGRAM_21_30.md` 与少量当前方法文档；不改文件、不扩展到整库重设计。重点会把局部结账、整本状态突变、人物决策张力和第20章回归后果分开判断。仓库当前有大量既存未提交改动，且目标文件位于 `books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/`；我会把它们视为他人/并行工作，绝不触碰。现有记忆还提示第16—20章交付曾标为“验收未确认”，所以本次只把用户给出的 21—30 Story Program 当审计对象，不把计划文字冒充已发生正文 Canon。结论：**总体 DIRECTIONAL PASS**。

- **World Engine：PASS**
- **Book Engine：DIRECTIONAL PASS**
- **主世界回归后果：当前 FAIL**
- **人物 Decision Vector：RSE-05 有真实激活，其余部分不足以自动判定为强人物张力**

这是对 Story Program 的审计，不等同于正文已经实现或 Canon 已经确认。

## 1. World Engine 与 Book Engine

### World Engine：成立

成立依据：

- 世界规则改变了主角的基本动作：同一记动作可以换载体继续，而非普通的换手、分身或控风。
- 规则有清楚边界：必须是真正开始的具体动作；不能传送人或固体；不补足力量、距离和破障能力；续接后仍可能失败。[STORY_PROGRAM_21_30.md:19-25](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:19)
- 世界由具体行动者推动，而不是机构任务板：岑非灯、贺乌衣、乔小满、陆停山各自有私人欲望，彼此在同一件刀、粮、河道和时间窗口上碰撞。[STORY_PROGRAM_21_30.md:29-33](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:29)
- 宁烬主动选择分事炉路线，且真实放弃了撤民、守河、追敌和其它资源路线。[STORY_PROGRAM_21_30.md:43-49](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:43)

这不是“新世界好看所以整本 PASS”；这里只能确认本 Horizon 的世界发动机有效。

### Book Engine：有真实突变，但回归传播不足

真正成立的 Book State Mutation 是：

- 宁烬永久获得“未尽续行”，以后改变他的进攻、逃脱、争夺和载体切换条件；
- 双真、风髓双口、未尽续行形成新的长期 Advantage Stack；
- 两处风髓骨口在高潮后再次恶化，未来行动成本和风险上升。[STORY_PROGRAM_21_30.md:71-85](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:71)

所以不能说本段只是“进入世界—拿能力—离开”。它确实多出了整本书以后不能按旧状态处理的新行动条件。

但第30章回归玄曜的设计明确写成：只看见已经见过的无墙宫殿和连续门扉，不新增人物、价格、策略、入口、关系或可行动事实。[STORY_PROGRAM_21_30.md:153-165](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_153-165.md:153)

因此 Book Engine 不是完全失败，而是有一个明确的回归传播缺口。

## 2. Local Closure 与 Book State Mutation

| 段落 | Local Closure / Canon retained | 真正的 Book State Mutation |
|---|---|---|
| RSE-04 | 宁烬选分事炉；贺乌衣暂得刀；岑非灯产生敌意；其它路线被放弃 | 暂无明确整本突变，主要是路线选择与局部关系建立 |
| RSE-05 | 分事炉冲突结账；三柄刀胚重新合成裂刀；贺乌衣失去铸成三刀的窗口 | 宁烬永久取得未尽续行；立即放弃三柄名兵这一具体收益，形成真实长期能力条件 |
| RSE-06 | 粮车过北门；岑父清白；乔小满失去渡口；陆停山认错并失势；贺乌衣失去炉锤和窗口；相关兵器停止北移 | 未尽续行首次与双真、风髓双口复合；两处骨口进一步恶化，未来使用条件改变 |
| Handoff | 玄曜仍是灵海4重；续事阶1位；旧人、旧线、旧谜团仍在；荒原其它兵事继续 | “续事阶1位”单独只是状态标签，不算突变；“旧线仍在”也只是 retained |
| 第30章回归 | 黑门骨再次显示已见过的宫殿和门扉；未知继续未知 | 没有新的主世界行动条件，因此 Return Consequence 没有成立 |

特别需要排除的“伪推进”：

- 商妩、鹿闻灯、贺沉骨“继续生活”；
- 裴照临仍然很强；
- 镜离、澜生仍在镜海；
- 黑门骨来源、诸界数量、宫殿内容继续未知；
- 盐路利润仍未兑现。

这些都是正确的保留或未知边界，但不是本 Horizon 对整本书的推进。

## 3. 是否强制召回旧人物、旧资产、Mystery？

**不应该强制召回。**

本文件不召回商妩、鹿闻灯、贺沉骨、镜离、澜生，也没有提前解决黑门骨和无墙宫殿，这一点是对的。长期线可以休眠，不能因为“证明 Book Engine”就收取旧人回访税。

真实推进应表现为：

- 旧人物真的改变策略；
- 旧资产到账、涨价、引发争夺或带来限制；
- 旧关系改变主角下一次选择；
- 旧身份改变入口、待遇或敌意；
- Mystery 出现新的可行动物证；
- 新的债务、伤势、时间窗口或敌方行动迫使主角改变路线。

本文件里，贺乌衣、乔小满、陆停山的变化首先是本地结账；只有后续真的改变宁烬的选择，才升级为 Book Mutation。不能仅因他们的状态被保存，就自动算整本推进。

## 4. Behavior Signature 是否自动等于人物张力？

**不等于。**

宁烬的“贪、好胜、好奇、不肯让别人替奇物定价、不愿只隔着人群看热闹”已经足以解释他的路线选择。[STORY_PROGRAM_21_30.md:5-11](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:5)

但这只是 Behavior Signature：他通常怎样去要。

判断 Decision Vector 是否真的被激活，要看：

1. 两个私人价值是否都真实存在；
2. 现场是否不能同时拿满；
3. 选择是否改变路线、对象、暴露、代价或谁承担后果；
4. 是否没有一个无损第三解。

本文件中：

- **RSE-05 最接近真实张力**：已许诺的三柄名兵，是立即、具体、不可替代的收益；未尽续行则是更长期、更异常的可能性。宁烬放弃前者，夺取后者。[STORY_PROGRAM_21_30.md:51-59](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:51)
- **RSE-04 主要是 Signature 驱动的路线选择**：撤孩子、守河、追敌是否属于宁烬已经成立的私人价值，文档没有证明。因此不能倒推成“他在正义与贪欲之间痛苦抉择”。
- **RSE-06 的张力仍不充分**：他不立即退回玄曜、要亲手证明新能力有效，但文档没有把自保、伤势、证明欲或其它私人价值明确构成不能兼得的现场冲突。

不需要补童年创伤，也不需要每个 Horizon 复制“钱 vs 人”或“安全 vs 自主”。

## 5. 主世界回归只确认能力、再开下一门，如何判？

文内实际把回归节点写成了**第30章**；如果你说的“第20章”指这个 Horizon 的回归节点，判定相同：

> 只确认能力仍在，再打开下一扇门，属于 **Return Consequence Collapse**。

它不自动抹掉一般 Book Mutation。两者关系是：

- **一般 Book State Mutation**：范围更大，只要结账后整本书多了不可逆的行动条件即可。这里“未尽续行”和伤势恶化已经满足。
- **Main-World Return Consequence**：是多世界小说中特别具体的一种传播检查，要求副本所得跨回主世界后，让既有社会、Rival、价格、关系、入口或 Mystery 产生真实行动变化。

所以可以出现：

- 一般 Book Mutation：PASS；
- 主世界回归后果：FAIL。

当前文件正是这个情况。无墙宫殿继续未知是正确的，但“没有任何新人物、价格、策略、入口或可行动事实”使回归变成了纯转场。[STORY_PROGRAM_21_30.md:161-163](C:/dev/tgn-story-mvp/books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1/STORY_PROGRAM_21_30.md:161)

## 6. 最早根因与最小修法

最早根因不是 World、Power，也不是 Writer，而是：

> **Story Program / World Horizon Handoff 把回归设计成“确认能力 + 开下一门”，并主动禁止回归产生新后果。**

最小修法不需要新增任何系统。只需在已有 Canon 能合法支持的范围内，让回归时至少有一个具体后果发生：

- 某个已有主世界观察者改变行动；
- 某个已有价格、入口或待遇发生变化；
- 某个已有 Rival 形成新策略；
- 某个已有资产、关系或债务真正到账或引祸。

如果当前已批准材料没有足够因果支撑，就应上报 upstream conflict，不能临时发明传送、追踪、奖励、身份或新机制。

人物部分最多只需保证 RSE-05 在正文里清楚呈现“立即三刀收益”和“长期未尽续行”不可兼得；不需要 Thread DB、Relationship Portfolio、Reviewer、Scorer，也不需要固定旧线回访税。

## 7. 最终判定

- **World Engine：PASS**
- **Local Closure：PASS**
- **一般 Book State Mutation：PASS**
- **旧线召回策略：PASS**
- **宁烬 Behavior Signature：成立**
- **Decision Vector：RSE-05 局部成立，RSE-04/RSE-06 不能过度推断**
- **Main-World Return Consequence：FAIL**
- **整体：DIRECTIONAL PASS**

原因是：本段已经有真正的长期能力突变和代价突变，不能判 FAIL；但回归后果被明确留空，距离完整的多世界 Book Engine 仍缺一个小而具体的传播动作。

未修改任何文件。
