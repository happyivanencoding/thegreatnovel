# Reviser No-Op Upstream Held-out Research｜Final Report

> Date: 2026-08-30
> Status: **COMPLETE / NO PRODUCTION CHANGE**
> Goal: 在不削弱 rich free-text Director 的前提下，把少量 Reviser 价值前移到 Primary，验证 Full Authority Reviser 是否真正趋近 no-op；正式判断使用全新小说 held-out，禁止根据 held-out 调 Treatment。

## 0. Final Verdict

这轮连续测试了三层假设：

1. **Candidate 1｜5行 Final-Draft Readiness Watch**：在旧两书归因后冻结，再生成全新 held-out 小说1。**FAIL for no-op**。
2. **Candidate 2｜Runtime deterministic Final Facts Projection**：在 held-out1 失败归因后冻结，再生成第二部全新 held-out 小说。**FAIL for no-op；Story 正信号、Authority 负信号。**
3. **Candidate 2 + Luna-medium Reviser screen**：只在 held-out2 已成为 derivation evidence 后做速度屏幕。Reviser wall 从 133.275s 降到 59.608s，潜在节省 **73.667s/章（55.27% Reviser wall）**，Story 守住；但 Authority 明显弱于 high，因此按预先规则**停止，不进入第三本 held-out**。

最终 production 决策：

> **保留 Terra-high Primary + Luna-high Authority Reviser。当前没有证据允许删除 Reviser、把它降到 medium，或让 Primary 直接成为 Final。**

本轮没有修改 `src/` production runtime、默认模型、ACP runner、前端或 State 路由。

---

## 1. Overfitting Control

用户明确要求使用新小说避免 case overfitting，因此实验采用顺序冻结：

```text
旧两书 Primary→Reviser pairs
        ↓ 只用于 derivation
冻结 Candidate 1
        ↓ hash 固定
全新 Held-out Novel 1
        ↓ 结果出来后 Candidate 1 不再修改
归因失败原因
        ↓
冻结 Candidate 2
        ↓ SHA-256 固定
全新 Held-out Novel 2
```

Candidate 2 protocol SHA-256：

`E11BEFFE12F5016CA1DFB362631D3145212437A21C20BCA360B7D540C5E692E4`

Held-out Novel 1：烬星洲 / 星力阶 / 顾沉舟 / “远身”兵器第二战斗位置。
Held-out Novel 2：骨鸣世界 / 鸣阶1—100 / 陆野渡 / “借境成身”环境适配变身。

两本 held-out 都由当时 production World → Power/Human → Story Program → Outline 自行生成；正式取前4个连续章节，没有读结果后挑章。

---

## 2. Candidate 1｜5-line Primary Self-check

冻结 Treatment 只提醒 Primary 在提交前确认：

- Chapter Mission / Direct Result / State Change / Ending 真正发生；
- money / ownership / reward 不降成资格或暗示；
- Power hard limit 不被当前动作偷换；
- 已经写得好的 desire / relationship / payoff 不因修事实消失；
- 不新增计划/Canon 没有的旧对话、数字、伤势、物件状态。

### 2.1 Held-out Novel 1｜2 repeats × 4 chapters

| Metric | Control | Candidate 1 |
|---|---:|---:|
| Primary wall mean | 36.872s | 36.087s |
| Reviser wall mean | 96.362s | 113.519s |
| Primary→Final edit blocks | 2.75 | 2.75 |
| Primary→Final similarity | 0.9465 | 0.9141 |
| Exact Reviser no-op | 1/8 | **0/8** |
| Story Primary | **85.000** | 83.375 |
| Authority Primary | 69.750 | **71.625** |
| Primary hard problems | 16 | **11** |
| Story Final | 81.000 | **83.875** |
| Authority Final | 77.875 | **84.000** |
| Final hard problems | 9 | **4** |

Candidate 1 的确让 Primary Authority 稍好，也让 Luna-high Reviser 得到更好的原料；但它没有把 Reviser 变成 no-op。Control Authority `Reviser − Primary = +8.125`，Treatment 反而为 **+12.375**。也就是说 Luna 在 Treatment 后仍需做更多有价值的 Authority recovery。

**Verdict：FAIL for Reviser-no-op。**

### 2.2 根因

Primary 与 Reviser 的 source visibility 不对称。Primary 有 Mission / Curator / compressed Authority，但 Reviser 重新拿到高显著度的：

- full Frozen Power Core；
- Frozen Human Core；
- safe World Authority；
-逐条 Reader Release；
- Canon Index；
- Primary Draft。

要求 Terra “提交前自己检查”不能替代它没有同等显著度拿到的事实。

---

## 3. Candidate 2｜Deterministic Final Facts Projection

Candidate 2 不再要求 Primary 自审，也不增加 LLM。Runtime 只在 Primary Prompt 尾部重新摆放已经冻结的少量事实：

```text
Direct Result
State Change
Ending
Scheduled Reader Release
Core Power 一句话
Permanent Power Boundary
```

所有字段来自 exact label / exact bounded section；没有中文 NLP、classifier、Curator/Primary fact creation，也没有第二个 Reviewer。平均投影只有 **468.25 chars/章**。

### 3.1 Held-out Novel 2｜2 generation repeats × 4 chapters

| Engineering | Control | Candidate 2 |
|---|---:|---:|
| Primary chars mean | 2236 | 2282 |
| Primary wall mean | 64.248s | **58.981s** |
| Reviser wall mean | **123.540s** | 133.275s |
| Primary + Reviser | **187.788s** | 192.256s |
| Edit blocks | **2.750** | 4.875 |
| Similarity | 0.9700 | 0.9737 |
| Exact Reviser no-op | **1/8** | 0/8 |

Candidate 2 的 Primary 自身快约 5.27s，但 Reviser 慢约 9.74s，组合反而**慢 4.47s/章**。修改块明显更多，也没有产生一次 exact no-op。

### 3.2 Double four-way blind｜32 judge rows

| Candidate | Story | Story #1 | Authority | Authority #1 | Hard problems |
|---|---:|---:|---:|---:|---:|
| Control Primary | 82.438 | 3 | **29.750** | 1 | **32** |
| Candidate 2 Primary | **85.250** | **6** | 27.625 | 0 | 41 |
| Control High Final | 80.438 | 2 | **33.625** | **9** | **15** |
| Candidate 2 High Final | **85.250** | 5 | 33.312 | 6 | 22 |

Candidate 2 对 Story 有真实正作用：Primary 比 Control **+2.812**，16次直接对比中 11胜5负。它把欲望、奖励、升级/路线选择等高价值故事结果提高到生成注意力前景。

但 Authority 反向恶化：Primary **-2.125**，Hard problems **32 → 41**；而 Luna-high 的 Authority 增益从 Control 的 **+3.875** 扩大为 Treatment 的 **+5.688**。因此 Reviser 在事实层不是更像 no-op，而是更必要。

### 3.3 典型失败

Candidate 2 在 held-out2 的真实错误包括：

- 漏掉精确 Reader Release（例如鸣阶6—9 / 10—18）；
- 给幼兽新增左后腿伤势；
- 提前把幼兽命名/关系写成已确定的“沉角”；
- 新增“能听见别人听不到的乱响地声音”等未批准能力；
- 把低阶兽核、纯鸣砂写成主角已持有，来源/归属越界；
- 新增未批准旧史、时间数字、资源消耗；
- 用“痕迹/暗线”替代必须明确兑现的不可消除永久骨痕。

这说明：

> **把 Fact 放得更近，会改变模型注意力，但不会自动把自然语言 realization 变成 Authority closure。**

**Verdict：FAIL for Reviser-no-op；Story-attention DIRECTIONAL POSITIVE。**

---

## 4. Candidate 2 + Luna-medium Reviser Screen

因为 Candidate 2 的 Story 很强，而问题集中在 Authority，进一步只做一个 derivation screen：同一 8 份 Treatment Primary、同一 Reviser Prompt，只把 Luna effort 从 high → medium。

### 4.1 Speed

| Metric | Luna high | Luna medium | Delta |
|---|---:|---:|---:|
| Reviser wall mean | 133.275s | **59.608s** | **-73.667s (55.27%)** |
| Primary + Reviser（同 Treatment Primary 均值） | 192.256s | **118.589s** | **-73.667s (38.32%)** |

速度潜力非常大。

### 4.2 Three-way blind｜8 Story + 8 Authority

| Candidate | Story | Story #1 | Authority | Authority #1 | Hard problems |
|---|---:|---:|---:|---:|---:|
| Candidate2 Primary | 83.625 | 3 | 55.500 | 0 | 16 |
| Luna medium Final | **84.625** | 2 | 57.500 | 2 | 9 |
| Luna high Final | 83.500 | 3 | **61.875** | **6** | **3** |

Medium 的 Story 完全守住，且确实修掉一部分 Primary Authority 问题；但 high 在 Authority 上仍显著更强，Hard problems 为 **3 vs medium 9**。

Medium 真实遗漏包括：

- 漏普通人鸣阶0 / 夜间公共危险说明；
- 替幼兽补“当然听不懂”的认知事实；
- 突破前错误写成“刚踏进鸣阶”；
- 漏明确永久骨痕；
- 擅自补低阶兽核/鸣砂来源；
- 补写过去的能力机制历史。

按预先协议：**medium 输 Authority即停止，不进入第三本 held-out。**

**Verdict：REJECT despite strong speed.**

---

## 5. What This Experiment Actually Proved

### 可以冻结的稳定判断

1. **用新小说 held-out 是必要的。** 旧两书能发现模式，但不能证明前移规则泛化；这轮两部独立新小说避免了 case overfitting。
2. **Generic Primary self-check 不会让 Full Reviser no-op。** 它可以轻微改善 Authority，却不能替代 Reviser 的远端 Authority recovery。
3. **Final Facts attention placement 能提高 Story，但可能恶化 Authority。** Story salience 与 factual closure 是不同坐标，不能用一个“更靠近输出”的投影同时优化。
4. **Reviser no-op 必须直接测 Primary→Reviser gap。** 不能用 Primary单独更好、Final更好、character similarity或低 wall 代替；至少同时看 Story gap、Authority gap、Hard problems、edit blocks、exact no-op 与 independent repeat。
5. **Luna medium 是真实速度候选，但当前 Authority 不够。** 不能因为约55% Reviser wall saving与Story不降就上线。

### 没有证明

- Primary 永远不能直接成为 Final；
- Luna medium 永远不能用于 Reviser；
- Final Facts Projection 对所有书都伤 Authority；
- Full Reviser 永远必须是 high。

只证明当前两个前移方案尚未达到“让 Full Reviser 变成稳定 no-op”的目标；medium 仍需要新的、独立的 Authority 解决方案才能重新测试。

---

## 6. Next Smallest Experiment

不要继续给 Primary 加第6/7条自查，也不要再复制更多完整 Authority。

下一候选应只针对 **medium 相对 high 反复漏掉的少数 Authority failure family** 做研究，例如：

- scheduled Reader Release exactness；
- permanent power/state milestone explicit naming；
- unresolved provenance / old-history no-invention；
- unapproved injury / number / object-state invention。

如果能从现有 Frozen Authority **确定性编译出极短 failure-triggered Revision Watch**，可测试：

```text
rich Director → Curator → Candidate2-like Story-positive Primary
                              ↓
                 Luna medium Reviser + tiny deterministic Watch
```

但必须先在 derivation 样本证明 medium Authority接近 high，再冻结 Watch，最后用**第三本全新 held-out 小说**验证。仍不允许中文 parser、LLM classifier或常驻新 Reviewer。

---

## 7. Production Decision

**No production change.**

当前保持：

`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`

当前实际可宣称节省：**0 秒/章**，因为没有 Candidate 达到采用标准。
