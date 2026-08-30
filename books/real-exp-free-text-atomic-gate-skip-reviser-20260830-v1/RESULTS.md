# Rich Free-text Director + Atomic Primary Bypass Gate｜最终实验报告

> 日期：2026-08-30
> 状态：**实验完成；Production 不变**
> 样本：2 本书 × 4 章 × 2 次 fresh repeat

## 0. Verdict

这条假设分成两半，结果不同：

1. **保留 rich free-text Director 是对的。** 相比上一轮 Native Structured Director，Primary 明显更接近可直接交付状态。
2. **“Atomic Authority Gate PASS → 直接跳过 Full Authority Reviser”这一简单路由，当前失败。**

最终冻结后的两次 fresh E2E：

- 8 次章节尝试；
- 4 次属于当前 deterministic Gate 的 supported shape；
- **0/8 Gate PASS，0 次真正 bypass**；
- Control：2457.403s / 8 章；
- Treatment：2457.424s / 8 章；
- 实际节省：**-0.021s，总体慢约 0.000855%**；
- 单章：307.175s → 307.178s，等于**没有加速**。

更重要的是，后续匿名 Primary-vs-Reviser 双盲证明：即便有一个“完美 Authority Gate”，**Authority 安全也不足以证明可以跳 Reviser**。Full Reviser 在当前系统里仍然提供可观的 Reader/Story 与 Authority 价值，不是纯固定税。

因此当前 production 继续：

```text
rich free-text Director
→ Curator
→ Primary
→ Full Authority Reviser
→ State
```

本实验代码和 Gate 保持 research-only，不接 production。

---

## 1. 被测试的真实路线

Treatment：

```text
rich free-text Director
→ Curator
→ Primary
→ deterministic Atomic bypass Gate
    ├─ PASS → Primary 直接 Final
    └─ FAIL / UNSUPPORTED → 当前 Full Authority Reviser → Final
```

Control 与 Treatment **共享同一次** fresh Director / Curator / Primary。为了做匿名比较，即使 Gate PASS，实验也会 shadow-run 一次 Full Reviser；但 shadow Reviser wall 不计入 Treatment critical path。

这样速度差只来自：

```text
跳过的 Full Reviser wall
-
Gate 自身 wall
```

不会被上游随机延迟冒充成加速。

State 不在本轮计时终点；State 路线没有改变。

---

## 2. 为什么先做 pre-freeze calibration

上一轮 Native Structured Primary 只有 2/8 被严格 Authority Oracle 判为可直接 Final。

为了判断“保留 rich Mission”是否改变这个前提，本轮正式 fresh 生成前，先拿此前**未参与本轮生成**的 rich free-text `fresh-control-3/4` Primary 做 feasibility audit：

- strict Authority Oracle：5/8 `PASS_DIRECT_FINAL`；
- deterministic Gate：4/8 PASS；
- Gate false-safe：0；
- safe false-fallback：1；
- 10 类定点 Hard Fact mutation：10/10 被阻断。

这证明值得继续实验，但这些历史样本**不进入最终速度结论**。

随后冻结：

- supported sample family；
- Gate 规则；
- 模型 / effort；
- 样本；
- Judge 标准。

从第一轮 fresh Director 调用后不再追着结果修改 Gate。

完整冻结协议见 `PROTOCOL_FREEZE_V1.md`。

---

## 3. Deterministic Gate 的范围

这不是复活旧中文关键词 Obligation Parser。

当前只允许两个预注册、窄范围 realization adapter：

### SUPPORTED：九垂原 Ch14

验证：

- 回潮楔一次完整用法；
- Public Ruler；
- 所有权 / 自主使用；
- 个人矿利；
- 砺骨部水路不并入矿权；
- 固定报酬 + 损失边界的独立合作；
- 残压冷却；
- 十二日地潮前旧关 deadline；
- 并阻断错误到账 / 转移所有权。

### SUPPORTED：Shadow Ch9

验证：

- 伤势处理；
- 双重私人欲望；
- 影身受伤回本体；
- 关系风险边界；
- 顾斜阳重新估价；
- 伤势未恢复；
- 双线记录触发护卫价值重估；
- 并阻断远程感知与提前付款。

### UNSUPPORTED：九垂原 Ch16

需要可靠证明本体 / 分身 / 回潮楔的分布式 actor-action-object 与 unknown/ending，现有 deterministic prose bridge 不足，直接 Full。

### UNSUPPORTED：Shadow Ch4

需要区分“两胜”与“正式名次结算”，并验证回客舍后的私密分影 reveal timing，现有 bridge 不足，直接 Full。

Unsupported 不是失败；它是 fail-closed。

---

## 4. Final fresh E2E：Gate 一次都没敢放行

### Run 1

| Sample | Gate | Control s | Treatment s | 节省 |
|---|---|---:|---:|---:|
| jiuchui_ch14 | FALLBACK | 379.813 | 379.817 | -0.004s |
| jiuchui_ch16 | UNSUPPORTED → FULL | 288.554 | 288.554 | 0 |
| shadow_ch4 | UNSUPPORTED → FULL | 264.322 | 264.322 | 0 |
| shadow_ch9 | FALLBACK | 328.611 | 328.617 | -0.006s |

Run 1：1261.300s → 1261.310s。

### Run 2

| Sample | Gate | Control s | Treatment s | 节省 |
|---|---|---:|---:|---:|
| jiuchui_ch14 | FALLBACK | 345.144 | 345.149 | -0.005s |
| jiuchui_ch16 | UNSUPPORTED → FULL | 267.230 | 267.230 | 0 |
| shadow_ch4 | UNSUPPORTED → FULL | 318.185 | 318.185 | 0 |
| shadow_ch9 | FALLBACK | 265.544 | 265.550 | -0.006s |

Run 2：1196.103s → 1196.114s。

### 两轮合并

```text
Control      2457.403 s
Treatment    2457.424 s
Delta          +0.021 s
Per chapter    +0.0026 s
Speedup          0%
```

Gate 自身只花 **19.835ms / 8章**，平均 **2.479ms/章**。

所以问题不是 Gate 计算成本，而是：

> **Gate 的 usable recall = 0。**

---

## 5. 第一层根因：free prose → typed evidence 证明桥太脆

### 5.1 Run2 九垂原 Ch14：典型 lexical false fallback

Primary 明确写：

> 残压没散。

> 他把回潮楔收回掌中，没有再压第二次。

> “残压还在。”她说，“今天别再碰它。”

语义上已经满足 cooldown。

但冻结 Gate 的 cooldown pattern 没有把这组自然表达识别成同一 typed fact。

更典型的是，阮青蜃说：

> “顾停舟，把回潮楔交给我。”

这是**对手提出交易条件**，实际结果紧接着是顾停舟明确拒绝。

但 forbidden surface matcher 看见“回潮楔……交给我”，把**提议**误判成**所有权已经转移**。

这是安全 false fallback，不是 false-safe；但它说明：

> 中文自由正文里的 actor / negation / proposal / result，仅靠窄 lexical matcher 很难泛化。

### 5.2 Shadow Ch9：事实存在，但 realization wording 不稳定

两轮 Primary 都写出了：

- 两条撤离路线；
- 普通二阶无法解释；
- 铜羽领队明显重新评估顾临川。

但 Gate 要求的 `record anomaly → escort-value repricing` 证据组合过于表面化，因此两轮都 FAIL。

这再次说明：

> **Hard Contract 是 typed authority；Primary 是自由 prose。二者之间仍缺一个低成本、可信、非自报式 evidence binding。**

不能用扩一大套中文 regex 来解决，因为那只会回到旧 parser 路线。

---

## 6. 第二层、更重要的根因：Authority PASS 也不等于可以跳 Reviser

如果问题只有 Gate recall，我们本可以继续优化 proof bridge。

但独立审计给出了更重要的反证。

### 6.1 Strict Authority Oracle 过于乐观

在 fresh supported Primary 上做两次独立 Luna-high Authority Oracle：

- Run1 J14：2/2 FALLBACK；
- Run1 Shadow9：2/2 PASS；
- Run2 J14：2/2 PASS；
- Run2 Shadow9：2/2 PASS。

对两个 unsupported family 额外做一次 strict Oracle，4/4 也判 PASS。

表面上看，8 份 fresh Primary 有 7 份像是可以直接 Final。

但这不能作为路由依据。

### 6.2 Primary-vs-Reviser Authority Blind 抓到了 Oracle 漏掉的具体错误

例如：

#### Run2 J14

Primary：

> “买断之价照旧”

Authority Blind 指出：Frozen Authority 只批准“高价买断”，没有批准一个此前已经存在的固定价格；“照旧”偷偷建立了过去价格 Canon。

两个 Oracle 都漏了。

#### Run1 Shadow9

Primary 把另一条路线概括为：

> “陆绾和药队的人”

但实际是陆绾与三名观日宗弟子的两条行动线；药队仍未完成撤离。

两个 Oracle 同样都漏了。

#### Shadow Ch4

Primary 出现过：

- “薄木牌”与“随队契券”对象摇摆；
- Reader Release 缺掉跨城“交易”入口。

#### Run2 Ch16

第二次 Authority Blind 发现：Primary 让分身“只携一点力量”，随后却没有闭合“分身如何持有回潮楔并固定第二节点”的 object chain。

所以：

> **LLM Oracle PASS 也不能替代真实 Authority 证据。**

这进一步否决“再加一个 LLM safety classifier”作为解决方案。

---

## 7. Full Reviser 不是纯 Authority 税

Full Reviser 在本轮 Control 中总 wall：

```text
1050.407 s / 8章
= 131.301 s / 章
= Control critical path 的 42.74%
```

所以它当然是最值得攻击的延迟大头。

但 repeated anonymous Primary-vs-Reviser blind 表明，它不是纯固定税。

我们对最初被 strict Oracle 判为“可直出”的 7 对 Primary / Reviser 做了两轮独立匿名 Story + Authority Blind。

### Story Blind｜14 judgments

```text
Primary wins   4
Reviser wins  10
Tie             0
```

平均分：

```text
Primary  81.572
Reviser  83.214
```

Reviser 常见的真实增益不是“写得更漂亮”，而是：

- 删除 Primary 的替读者总结；
- 把公开证明落到更具体的可见结果；
- 压掉重复解释；
- 让奖励和下一章钩子更利落；
- 修正“任务简报 / 战后报告”的味道。

### Authority Blind｜14 judgments

```text
Primary wins   1
Reviser wins   8
Tie             5
```

更关键的是：Authority Blind 反复抓到 strict Oracle 未抓到的小但真实 Canon 错误。

### 稳定质量等价 bypass candidate

我们要求同一对在两轮 blind 中同时满足：

1. Primary 的 Story 不稳定输 Reviser；
2. Primary 没有具体 Authority hard problem。

结果：

```text
0 / 7
```

也就是说，本轮没有一个候选能稳定证明：

> “Full Reviser 在这里确实是无价值固定税，可以放心跳过。”

---

## 8. 为什么实际 Final Quality 没有下降

因为最终 frozen Gate：

```text
0/8 PASS
8/8 FALLBACK
```

所以 Treatment 的 8 篇 Final 与 Control 的 8 篇 Final **逐字相同**。

因此本轮实际路线：

- Story：与 Control 完全相同；
- Authority：与 Control 完全相同；
- 速度：与 Control 完全相同；
- 只多出约 2.5ms/章 Gate 税。

这是一个安全失败，而不是质量事故。

---

## 9. 这轮真正证明了什么

### 可以冻结

1. **Rich free-text Director 必须保留。** 上一轮把 human Mission 压进 Hard IR 是错误方向。
2. **Atomic Authority Contract 适合后台 Authority / repair 边界，不适合承担 Story Mission。**
3. **Unsupported → Full Reviser 的 fail-closed 路由正确。** 本轮没有 false-safe 进入实际 Final。
4. **Full Reviser 是 value-bearing stage，不是纯 fixed tax。** 当前它同时承担 Authority recovery 与一部分 Reader/Story realization improvement。
5. **Contract closure 不能单独作为 skip-Reviser 条件。** 即使 Authority Oracle 看似 PASS，Primary 仍可能有 Canon 小错；即使 Authority 真等价，Reviser 仍可能明显改善 Story。
6. **LLM Oracle / classifier 不应成为 production Gate。** 本轮两个独立 Oracle 仍漏掉真实 Authority 问题；新增一个语义 Judge 既不可靠，也会吞掉 latency savings。

### 不可以冻结

- 当前 deterministic prose Gate；
- 当前两个手工 realization adapter 作为通用 compiler；
- `Authority Gate PASS → Primary Final`；
- Full Reviser 删除；
- 任何基于“Reviser 占 42.74% wall，所以应该能省 42%”的速度结论；
- 扩中文 regex / synonym / negation parser 去追求 recall。

---

## 10. 对下一步的判断

这轮说明真正的问题已经不是：

> “怎样写一个更聪明的 Authority Gate？”

而是：

> **怎样让 Primary 本身稳定达到 Reviser 后的 Story + Authority 水平，使 Reviser 真的变成 no-op，之后才有资格跳。**

也就是说，合理的下一实验顺序应该是：

```text
冻结同一批 Primary / Reviser pair
        ↓
归因 Reviser 稳定增加了什么 reader-facing value / 修了什么 recurrent failure
        ↓
只把真正重复出现、可上移的少量能力前移到 Primary / Curator
        ↓
重新生成 Primary
        ↓
Primary vs Reviser 是否开始稳定 TIE / Primary win？
        ↓
只有那时再测试 deterministic skip
```

这比继续扩大 Gate parser 更符合第一性原则。

注意：这不是建议把完整 Reviser Prompt 再塞给 Primary。目标仍然是**最小迁移**，只迁移可证明的 recurrent cause；否则只是把 131 秒的工作搬到 Primary 里，既不快也会增加 Prompt bloat。

---

## 11. Production Decision

**FAIL AS CURRENT BYPASS ROUTE。**

Production 不变：

```text
Luna rich free-text Director
→ Luna Curator
→ Terra Primary
→ Luna-high Full Authority Reviser
→ Luna State
```

没有修改 production `src/`、模型路由、ACP runner、frontend 或 State。

完整机器结果：

- `FINAL_METRICS.json`
- `TIMING_TABLE.csv`
- `ORACLE_AND_BLIND_AUDIT.json`
- `fresh-gate-1/summary.json`
- `fresh-gate-2/summary.json`

## 12. Validation

- Gate calibration / mutation focused tests：**2 passed**。
- Atomic + Native + Gate focused regression：**65/65 passed**。
- Full repository regression：**425/425 passed**。
- Final artifact JSON/CSV parse + invariants：PASS。
- `git diff --check`：PASS。
- `tgn-system-steward 0.3.26`：validate / install / activate PASS；digest `sha256:b82f9d0b742a384f1fcd09c1ec778ae820077bfb14a48a0f417cda25abbfb6a4`。
- Bounded read-only Steward smoke：PASS；正确判定 `Contract closure ≠ Reviser necessity`，并拒绝新增 LLM necessity classifier。
- Production `src/` / model routing / frontend / ACP runner / State：未修改。
