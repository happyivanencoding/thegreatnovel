# RESULTS｜State Advance + Reader Ruler + Ascension Regression

## Verdict

**总体：DIRECTIONAL PASS / 值得保留 production 修改。**

这轮最重要的成功不是“章节更短”，而是：**低价值的重复证明被压缩，高价值的新状态、力量比较、人物选择与下一场事件更早进入；同时 Story Program 开始把成长写成连续升格，而不是只消费猎阶。**

未完全解决：Primary 仍会把首次出现的支撑性实施过程写得偏完整；另外新版把幼年王种正式揭晓推到第6章，导致前五章暂时少了一次旧版已有的价值尺兑现。

## 实验设计

Baseline：`real-exp-private-prototype-asymmetry-novel-20260826-v2`。

冻结 Author Direction / World / Power / Human / Character 与 GBrain bundles；重跑 Sol Story Program → Luna Outline → 5章 `Luna Director → Luna Curator → Terra Primary → Luna low State`。

Treatment：production commits `4344ef1` + `2325ca1`：

- `Ruler = Compression, not Exposition`
- World reusable benchmarks
- `State Advance After Proof`
- `Choice → Consequence`
- `Discriminative Detail Only`
- `Plot Pace ≠ Tier Pace`
- Protagonist Ascension Trajectory

另跑一次 protagonist-blind World-only smoke 验证 benchmark；该 World 不进入正文 authority，因此正文 A/B 仍冻结原 World。

## 1. Reader Ruler / World Benchmark：PASS

World-only smoke 主动给出少量可复用、可感知基准，例如：

- 一形：可独立猎杀普通荒兽，短爆发可翻院墙、折断粗木；
- 二形：可单独击杀大型猛兽，普通十人围攻也很难困住；
- 三形：可正面击穿披甲队列，或压住数头二阶异兽。

它没有建立公斤/米数数据库，也没有给每阶机械填指标，符合“benchmark authority 在 World”。

正文中 Ruler 也真正承担了压缩功能。新版第2章只需桑照一次检查并一句比较：二阶异兽已发动的扑击本应压倒无阶者，闻野舟却让它当场偏移；随后直接给出限期入场牌。旧版第二章则用了多种痕迹、多人判断和反复询问证明同一异常。

值得注意：新版前五章的 `二阶` 等尺度词出现次数反而低于旧版；说明目标不是“多播报等级”，而是**一次比较承担更多信息**。

## 2. State Advance After Proof：PASS

最强 A/B 在 Chapter 2：

| 章节 | Baseline | Treatment | 变化 |
|---|---:|---:|---:|
| Ch1 | 1912 | 1725 | -9.8% |
| Ch2 | 4155 | 1532 | **-63.1%** |
| Ch3 | 1945 | 1606 | -17.4% |
| Ch4 | 2923 | 3603 | +23.3% |
| Ch5 | 3075 | 2039 | -33.7% |
| 合计 | 14010 | 10505 | **-25.0%** |

Ch2 的减少主要来自删除重复 Verification，而不是删掉结果：

`一次现场校准 → 桑照认可 → 黑铁入场牌实际到手 → 猎队首领记住闻野舟 → 顾晚禾提出三日后南行的新冲突`。

这已经符合：**Proof once → Calibrate once → Consequence immediately.**

## 3. Choice → Consequence：PASS

新版 Ch3 不再把“留镇还是同行”反复想一整章。

闻野舟较早明确选择跟顾晚禾走；后续篇幅直接进入：三日准备被压缩 → 商队出镇 → 南路被边军封锁。

人物选择仍然有重量，但不再靠重复内心论证证明“这符合他的人格”。行动本身承担 Character Proof。

## 4. Plot Pace ≠ Tier Pace：DIRECTIONAL PASS

Baseline Story Program 的明显等级节点包括：三阶 → 五阶 → 七阶 → 八阶。

Treatment 开始允许“故事升格但猎阶不升”：

- Stage 2：进入二阶；
- Stage 3：**没有新能力或更高猎阶**，但从无名者变成各宗门私下打听的异常猎手；
- Stage 4：能力结构发展到可独立应付多数四阶猎物；
- Stage 5：明确写 **猎阶没有显著上升**，但身体、顾晚禾关系、韩青禾关系、反生林认知与世界局面同时改变；
- 后期才进入七阶、八阶。

方向明显改善，但晚期仍从四阶附近较快进入七、八阶，因此这里只判 DIRECTIONAL PASS，不视为长期节奏已完全解决。

## 5. Protagonist Ascension Trajectory：DIRECTIONAL PASS

新 Story Program 已出现真正的因果螺旋，而不是把 `Power / Identity / Access / Relationship / Knowledge` 当平行字段：

`无阶杂工第一次让二阶力量失准`
→ 桑照记住名字、给限期入口
→ 主角带着入口主动离开
→ 二阶阶段通过越级资格战进入更高层视野
→ 即使没有升阶，各宗门也开始私下打听他
→ 桑照因共同夺回家传兵器，把蜕壳城内层名额分给他
→ 新世界入口带来古谱、新身体能力、旧关系损伤与更深世界真相
→ 后续强者开始研究并针对他的打法
→ 最终才进入军府/顶宗必须重新估价的强者圈。

这更接近“他已经不是第一章那个位置的人了”。

## 6. Core Power recurrence：改善

Baseline 前五章只有 Ch1 的第一次正式能力兑现。

Treatment Ch5 已经出现第二次真实「夺势」：闻野舟削掉白角兽冲车阵时最凶的一截冲势，救下顾晚禾与伤驮兽，同时让陶遂从“允许帮忙”改为把他当作可调用的现场战力。

这不是重复同一场景：第一次是猎市意外自救/救人；第二次是白角部冲击、阵营选择与外部世界冲突。

## 7. Discriminative Detail Only：PARTIAL PASS

Director 层明显成功：Ch4 合同只要求“观察白角部追踪某物 → 选择相信陶遂 → 商队被封锁 → 顾晚禾不满”，没有施工清单；Ch5 Director 甚至明确要求只保留一次决定局面的冲击，不展开稳车流程。

但 Primary Ch4 仍花了较多篇幅写车辆三排停放、药车居中、驮兽拴放、推车、缰绳、水囊等首次实施细节。

因此结论是：**专业技能过度展开明显减少，但“一个新决定之后的普通实施”仍可能被 Writer 扩写。** 当前不继续加新 Gate；若跨样本复现，再优先在现有 Reader-First / 选择性因果合同里做更小的 prose-level A/B，而不是新增 Agent。

## 8. Trade-off / What This Did Not Solve

- 新版把“幼年王种正式确认 + 高阶心核价值尺”安排到 Ch6；所以前五章没有旧版 Ch5 那种强价值尺度兑现。新版 Ch5 的替代物是第二次 Power payoff + 染血包裹里的幼叫。两者哪个更抓读者，需要更多样本，不应凭单本下结论。
- Ch2 / Ch3 分别约 1532 / 1606 字，说明压缩规则可能产生更短章节。当前样本内容完整，且 Ch4 能自然展开到 3603 字，因此没有出现“全书骨架化”；但后续仍应观察是否系统性低于目标平台的舒适章节体量。
- Protagonist Ascension 已开始形成连续轨迹，但认知升格仍主要依靠蜕壳城、反生林等世界秘密，主角早期人生/旧人物的重解释仍可更强；不因此强制隐藏身世或 Power Origin Mystery。

## 9. Integrity

- Canon / prose pipeline marker leakage：0。
- World benchmark smoke 与正文 A/B authority 分离，未把 smoke World 偷换进小说。
- 五章严格串行 State 落地后再写下一章。
- Chapter 1/2 因节奏压缩低于旧实验 runner 的 1800 字阈值；直接人工复核确认场景完整后保留原模型输出，没有为了过阈值重写灌水。实验 runner 下限降为仅防止明显不成章的 1000 字。
- `pytest -q`：291 passed。

## Final

**保留本轮 production 修改。**

最重要的新系统性表达可以压成两句：

> **一个结果一旦成立，就让它立刻造成下一件不可逆的事；当前事件碰到哪把尺，就用一次高价值比较替掉重复解释。**
>
> **长篇成长不是升级字段集合，而是主角凭成长不断进入过去没有资格进入的人物圈层、世界层和真相层，并因此获得过去没有资格作出的选择。**
