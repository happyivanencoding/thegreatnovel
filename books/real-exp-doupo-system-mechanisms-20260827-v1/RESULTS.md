# 《斗破苍穹》机制 → TGN production A/B 结果

日期：2026-08-27

## 目的

验证三项来自《斗破苍穹》全文研究、但可能改变 TGN Story Program 行为的候选机制：

1. Audience Knowledge Distribution：新圈层按各自真实掌握的信息判断主角，而非默认全知或降智轻视。
2. Strong Secondary Fantasy Axis：炼药/炼器等只有本身就是可欲望的强者道路时，才从 Supporting Logic 升格为第二幻想轴。
3. Adjudicable Payoff Debt：少量长期承诺具有具体对象与至少一个可观察结算条件。

同时验证 Character Authority Invariance：结构机制不能把不同 Human 全部推成同一种成长最优/关系最优路线。

## Protocol

- Frozen World / Power。
- 三种明显不同的 Human：
  - power_first：力量、胜负与强者认可优先；
  - relationship_first：具体关系可真实改变成长取舍；
  - mixed_status：认可、新鲜感、审美/器物与力量混合。
- 每项机制 A/B；模型 GPT-5.6 Sol high。
- 第一轮：3 mechanisms × 3 Human × A/B = 18 outputs。
- Secondary Axis 因 mixed_status treatment 仍略有“学徒→考试→升品”职业流程感，再跑 B2 × 3 Human，专门压缩普通流程、只保留作品/胜负/稀有创造/强者判断与不可替代机会。
- Luna high 独立 cross-output synthesis 作为辅助 Judge；最终仍以真实输出为准。

## 1. Audience Knowledge Distribution

结论：**PASS / DIRECTIONAL PASS，适合最小 production 化。**

Treatment 稳定产生：

`局部旧信息 → 合理初始报价/试探 → 最低充分证明 → 不同观察者分别更新待遇、敌意、合作或挑战规格`。

它没有要求新圈层无脑嘲讽，也没有让所有人知道主角全部旧战绩与最新底牌。

Human invariance 保留：

- power_first 仍主动争更高规格公开验证；
- relationship_first 仍会为沈禾放弃不可补发的秘境机会；
- mixed_status 仍会在公开漂亮胜负、稀有门槛和懂行认可之间偏航。

边界：不要建 reputation database；不要把每次关系选择翻译成“信誉价格变化”；同一事实不要求所有观察者同步更新。

## 2. Strong Secondary Fantasy Axis

第一轮结论：**PASS / DIRECTIONAL PASS，但需要去职业流程化。**

第一轮 B 已证明：当炼药拥有独立强弱、顶层人物、公开竞争、高价值成果与社会价格时，它不再只是“省钱/赚钱/做补给”，而能成为第二种强者幻想；但 mixed_status 输出仍有明显“学徒→资格→品级→丹会”的职业阶梯感。

### B2

结论：**PASS。**

B2 不要求连续考试/升品，而强调：

- 真正有分量的作品；
- 稀有材料/灵火；
- 懂行强者判断；
- 独立胜负与不可替代机会；
- 普通练习/制作步骤/重复考核压缩；
- 同一品级也可承载不同故事；
- 副轴可以暂时放下。

三种 Human 仍明显不同：

- power_first：先拿确定破境收益；确认副轴真实成立后仍可在关键冲突中优先主力量路线；
- relationship_first：即使已投入灵火/作品机会，沈禾的不可逆事件仍能让他退出，并真实失去收益；
- mixed_status：会为了稀有作品、漂亮器物和懂行认可改变比赛/修炼选择，但不自动成为职业型炼药师。

第一性原则：

> **Bad Occupation = 能力/专业生成可重复工作流程。**
> **Secondary Fantasy Axis = 这条路本身就让读者想看主角成为顶尖。**

不要求每本书有副职；是否投入由 Human 决定。

## 3. Adjudicable Payoff Debt

结论：**PASS，本轮最稳定。**

相比 generic Open Promise，Treatment 用“对象 + 至少一个可观察结算条件”形成清晰长期距离：例如六个月后的天榜换榜日、双方仍有登台资格时正式再战。

收益：

- 中间成长有明确参照，不需要每阶段倒计时；
- 正式结算能清楚回答“债有没有还”；
- 其它关系、秘境、世界线仍可以中途改路；
- 主角可以错过、失效、延期、输掉或主动放弃。

Human invariance 保留：

- power_first 会主动把公开再战当成强者证明；
- relationship_first 即使债务存在，仍先处理沈禾不可逆事件，并承担真实成长损失；
- mixed_status 不围着约战生活，仍会被新鲜机会、具体关系和漂亮公开胜负吸引。

边界：不要把所有 Promise 债务化；不要保证主角一定赴约、追回或获胜；长期对手仍要有自己的后续人生，而不是结账后变成已完成任务。

## 4. Character Authority Invariance

结论：**PASS，适合作为结构机制 A/B 的默认实验 protocol。**

以后凡新机制可能影响人物取舍：

1. 至少冻结 2—3 个动机排序明显不同的 Human；
2. 分开判断 Treatment 是否产生目标结构增益；
3. 再判断关键选择是否仍随 Human 改变；
4. 如果不同 Human 被推成同一种成长最优、关系最优或道德最优路线，即使结构更整齐，也应 FAIL / 降级。

这不是 production Agent / Gate，只是实验验收方法。

## Production 状态

本轮实验执行时发现，另一并行任务已在 commit `a9dcafa fix(outline): separate opening life orientation` 中将三项**最小原则**与 Character Authority Invariance 写入当前 production，并已推送到 `origin/principal_dev_new_sys`：

- `PROTAGONIST_ASCENSION_TRAJECTORY`：新圈层局部认知与独立更新；
- `SECONDARY_FANTASY_AXIS_DIRECTION`；
- `ADJUDICABLE_PAYOFF_DEBT_DIRECTION`；
- PROJECT_RULES 实验 protocol：Character Authority Invariance。

当前实现与 B2 结论一致：没有 reputation database、PayoffDebt schema、副职配额或新 Agent/Hard Gate。因此本轮不再重复修改 Prompt，只把实验作为对该 production change 的事后因果验证。

## Regression

当前工作树（含其它并行本地改动）全量：**294 tests passed**。

## Final Verdict

- Audience Knowledge Distribution：**PASS / DIRECTIONAL PASS → 已最小冻结**。
- Strong Secondary Fantasy Axis：**B2 PASS → 已最小冻结**。
- Adjudicable Payoff Debt：**PASS → 已最小冻结**。
- Character Authority Invariance：**PASS → 已冻结为实验 protocol**。

What This Did Not Solve：

- 不证明每本书都应该有第二幻想轴；
- 不证明所有长期承诺都应该可判定；
- 不证明新圈层必须低估主角；
- 不证明副轴必须采用等级/考试/榜单；
- 不处理具体正文如何写得更像《斗破》的情绪与场面节奏，那属于独立 prose/story-feel 研究。
