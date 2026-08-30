# Native DirectorStructuredDecision → Final Draft｜最终实验报告

> 日期：2026-08-30
> 样本：2本书 × 4章 × 2次独立 Treatment + 2次相邻 Fresh Control
> 最终判定：**FAIL AS PRODUCTION REPLACEMENT / Atomic backend remains research-valid**

## 0. 结论

这轮没有证明 Native `DirectorStructuredDecision` 能节约章节生成时间。

实际测得：

| 指标 | 当前 Free-text Director Control | Native Structured Treatment | 差值 |
|---|---:|---:|---:|
| 4章完整 Final Draft 链均值 | 1370.605s | 1406.264s | **Native 慢 35.659s** |
| 单章均值 | 342.651s | 351.566s | **Native 慢 8.915s** |
| 百分比 | — | — | **慢 2.60%** |
| Director 节点均值／4章 | 128.795s | 148.272s | **Native Director 慢 15.12%** |

换算为单章：

> 当前 Control 约 **342.7秒／章（5分42.7秒）**；Native 约 **351.6秒／章（5分51.6秒）**。

所以“时间究竟节约多少”的答案是：

> **没有节约。当前最佳点估计是每章反而多花约8.9秒。**

并且结果波动很大：相邻配对一轮慢13.41%，另一轮快7.78%。这不是可复现的速度增益。

质量也不是等价交换：Native 最终正文的 Story Blind 略强，但 Authority Blind 明显下降。因此不能用“Story更好”掩盖会污染后续 Canon 的事实退化。

Production 五节点、模型、ACP runner、前端均保持不变。

---

## 1. 实验设计

### Control

```text
Free-text Luna-high Director
→ Luna-high Curator
→ Terra-high Primary
→ Luna-high Authority Reviser
→ Final Draft
```

### Treatment

```text
Luna-high Native DirectorStructuredDecision
        ↓
Runtime deterministic dual projection
        ├─ human-readable Mission
        └─ Atomic Authority Contract
        ↓
Luna-high Curator
→ Terra-high Primary
→ Luna-high Authority Reviser
→ Final Draft
```

两条路线冻结：

- 同一章的 Story / Outline / Canon / World / Power / Human / Reader Release；
- 相同模型与 reasoning；
- 相同 Curator、Primary、Authority Reviser Prompt；
- 相同四章样本；
- Control 与 Treatment 都重新真实调用，未用历史缓存时间替代 Fresh Control；
- 盲评完全匿名，统一去除模型元数据、citation尾巴与 `# 正式正文` 标题。

V1 首次运行暴露跨书 Surface 污染：九垂原关系事实被错误渲染成“确认分影后同行”。该批结果全部标为 invalid，不进入最终数字。只允许修正 deterministic projection 根因，随后冻结 V2 哈希，运行 Run4 / Run5；盲评后不再调模板。

---

## 2. Story Blind 与 Authority Blind

四路匿名混排：Native Run4、Native Run5、Fresh Control3、Fresh Control4。每章分别做：

- Director Mission Story Blind；
- Director Mission Authority Blind；
- Final Draft Story Blind；
- Final Draft Authority Blind。

共16次独立 Judge 调用。

| Blind | Native均分 | Control均分 | 差值 | Native获第一 | Control获第一 |
|---|---:|---:|---:|---:|---:|
| Mission Story | 7.537 | 8.825 | **-1.288** | 0/4 | 4/4 |
| Mission Authority | 5.688 | 8.400 | **-2.712** | 0/4 | 4/4 |
| Final Story | 8.387 | 7.825 | **+0.562** | 3/4 | 1/4 |
| Final Authority | 6.250 | 8.100 | **-1.850** | 1/4 | 3/4 |

### 关键分裂

Native 的 human Mission 太短、太抽象：

- Story Mission 比 Control 低1.288分；
- Authority Mission 比 Control 低2.713分；
- 4章中没有一章 Mission 被 Story 或 Authority Judge选为第一。

但这种压缩减少了下游“把策划摘要全部演一遍”的倾向，因此 Final Story 反而高0.563分，4章里Native拿到3次第一。

问题是它用 Authority 换来的：Final Authority 低1.850分。它更好读，但更容易：

- 漏关键动作边界；
- 漏具体状态变化；
- 自行补金额、力量尺度或契约条款；
- 改变关系发生地点和时序；
- 提前结算下一章待遇；
- 让 Authority Reviser无法恢复Human Mission中已被压掉的信息。

因此这不是质量等价优化，而是：

> **更少规划信息 → 更自由、更顺的正文 → 更高事实漂移。**

---

## 3. 具体正文例子

### 3.1 Native Final Story 为什么更顺

九垂原第14章 Native Run4 把能力展示、报价与拒售连在同一条收益链中，Story Judge认为主角“从被人定价到自己定价”的转折更直接。

Shadow第9章 Native Run5 保留了顾临川的混合欲望：

> “我想要那对短兵。”
>
> “我也不想看着你死在里面。”

它没有把救人净化成无私，因此人物和关系更有吸引力。

### 3.2 但 Authority 发生硬退化

九垂原第16章 Native Run4 写：

> “整辆粮车被他硬生生往前抬起半尺。”

这把已批准的复合位置能力改写成了未经批准的肉身蛮力。它还没有明确让分身携带并使用“定住”，并漏掉照域潮谱与下一股潮势的Ending边界。

同章 Native Run5 写：

> “顾停舟松开按住井圈的手。”

再次把本体能力扩成直接压井圈，而Control则明确写出：

> “定住。”
>
> “被分身定住的潮压……拐了个弯。”

九垂原第14章 Native Run5 将已冻结的固定报酬改成：

> “按你实际出手的次数和结果结价。”

并自行增加五百、八百潮铢。Story上更热闹，但它改变了Money Authority。

Shadow第4章 Native Run5 让陆绾在试场现场看见分影；冻结计划要求在试场结束后回到客舍再揭示。这改变了关系场景的时序、私密性与Canon落点。

Shadow第9章 Native Run4 写：

> “他两边都看见了。”

它越过了“影身远离本体时不能直接获知另一处所见”的能力边界，并让领队提前重算护卫价格。

这些都说明：当前 Full Authority Reviser 不是一个足以修复“上游human Mission已丢事实”的万能保险。

---

## 4. Director wall

| 节点 | Control四章均值 | Native四章均值 | Native变化 |
|---|---:|---:|---:|
| Director | 128.795s | 148.272s | **慢15.12%** |
| Curator | 500.509s | 470.774s | 快5.94% |
| Primary | 213.298s | 222.967s | 慢4.53% |
| Reviser | 528.004s | 564.250s | 慢6.86% |

Runtime双投影本身中位数只有约1.7ms，几乎免费。真正变慢的是模型必须在Director节点同时完成：

- 故事取舍；
- Entity选择；
- Action ID选择；
- Fact kind / field分类；
- actor / object / counterparty绑定；
- transition from/to state；
- JSON schema自校验。

即使输出更短，认知任务更难，因此Native Director平均更慢。

Curator偶尔变快不代表结构优势；两轮间波动很大，且Primary/Reviser反向变慢。完整critical path必须看总和，而不是挑最快子节点。

---

## 5. 完整 fallback-adjusted E2E

V2共8个Native尝试：

```text
8/8 native accepted
0 fallback
```

路由实现会在Native parse / Contract / projection失败时记录：

```text
discarded Native Director wall
+
full free-text Director fallback wall
+
完整 Curator / Primary / Reviser
```

所以最终计时是fallback-aware的；但本批次没有触发fallback，因此本批次的fallback-adjusted wall等于直接Native wall。

V1曾真实触发1次fallback，证明代码会把两次Director成本都计入；但V1存在跨书Surface污染，不能拿它估计production fallback率。

更重要的是：当前Registry与Action Catalog是人工准备的。真实长篇自动Registry覆盖尚未证明，production fallback率很可能高于本次0/8。因此不能把0/8外推成“以后不付fallback税”。

---

## 6. 跨书 Registry coverage

V2结果：

| 指标 | 结果 |
|---|---:|
| 书 | 2 |
| 章 | 4 |
| 独立Native尝试 | 8 |
| Preflight接受 | 8/8 |
| 已知Hard Fact覆盖 | 58/58 |
| Runtime normalization | 0 |
| Entity实例 | 38 |
| Entity类型 | 13 |
| Contract Fact实例 | 64 |
| Fact类型 | 13 |
| Unique Action IDs | 44 |

覆盖的类型包括character、manifestation、item、resource、contract、route、location、organization、power tier、ability、mystery、event与group。

这证明：

> 同一typed grammar可以承载两本不同小说的战斗、资源、所有权、关系、能力边界、Public Proof、Deadline和Mystery。

但它没有证明：

- Entity Registry可从任意新书自动生成；
- 44个Action ID足以覆盖长篇；
- 自动Fact→Paragraph evidence定位可靠；
- 新世界出现未登记动作时不会大量fallback。

因此应写成“手工Registry下的跨书Schema coverage成功”，不能写成“通用Registry已成功”。

---

## 7. Independent repeat

Run4与Run5：

| 重复层 | 完全一致 |
|---|---:|
| Raw structured decision | 0/4 |
| Normalized decision | 0/4 |
| Artifact-level Contract hash | 2/4 |
| Semantic Hard Fact set | 3/4 |
| Human Mission | 3/4 |
| Curator | 0/4 |
| Primary | 0/4 |
| Final Draft | 0/4 |

58/58已知Hard Facts在两轮都被覆盖，但有一章额外语义不同：地潮触发事实的actor在一轮为空，另一轮绑定到Mystery Entity。说明“fixture recall 100%”不等于整个Contract完全稳定。

结论：

- 核心已知义务稳定；
- 整体typed decision并不deterministic；
- 下游文本自然不应要求逐字一致；
- 但Hard Contract若要成为自动Gate，语义集合3/4仍不足以冻结。

---

## 8. 时间到底节约多少

### 诚实答案

```text
节约：0秒
当前点估计：每章慢8.915秒
相对变化：慢2.60%
```

### 为什么不能拿最好一轮说“快7.78%”

因为同一冻结版本的另一轮慢13.41%。独立重复没有形成同方向结果。取两轮均值后是负数。

### 为什么不能只说Runtime投影几乎免费

因为真正成本在Director模型生成typed decision，而不是Python把它渲染成Mission。模型节点慢15.12%。

### 为什么不能说最终Story更好，所以值得上线

因为Final Authority低22.84%，而且存在会污染后续Canon的硬问题。用户要求的是“不明显降质量地加速”，不是用事实可靠性换更顺的单章阅读。

---

## 9. Production决策

### 可以保留

1. `Atomic Authority Contract ≠ Primary Preservation Map`架构；
2. Entity ID / stable slot / trusted Authority artifacts；
3. Native structured decision作为研究工具；
4. Runtime双投影的source-purity方法；
5. Edit Locality与blocker-only repair方向；
6. typed core与human Mission、Final Story、Final Authority必须分别审计的方法论。

### 不能进入production

1. 用当前Native structured human projection替换free-text Director Mission；
2. 宣称Native Director更快；
3. 宣称58/58 fixture coverage等于完整Authority fidelity；
4. 删除每章Full Authority Reviser；
5. 用当前手工Registry推断任意新书coverage；
6. 用Final Story的小幅提升掩盖Final Authority下降；
7. 继续给ActionSurface模板逐书打补丁并称为通用系统。

### 当前Production

```text
Luna-high free-text Director
→ Luna-high Curator
→ Terra-high Primary
→ Luna-high Authority Reviser
→ State
```

保持不变。

---

## 10. 下一步最有价值的实验

这轮证明：节省Director表达不是主要省时来源；章节大头仍是Curator与Authority Reviser，特别是Full Reviser固定税。

正确下一步不是继续把Native human Mission做得更复杂。复杂后它只会重新接近free-text Director，并继续增加Director wall。

更有价值的是：

```text
现有丰富 free-text Director Mission
+
后台 Atomic Authority Contract
        ↓
Primary / Reviser 正常写
        ↓
在完整支持的章节上测试：
Atomic Gate PASS → 跳过 Full Reviser
Atomic Gate FAIL → Full Reviser fallback
```

也就是保留Control Director的故事信息带宽，只把typed Contract用于后台验证和选择性免税。只有这一条路线才直接攻击当前最大耗时节点，同时不让Primary看Atomic Pack。

但在运行前还必须解决：

- Contract不能靠事后中文Parser产生；
- human Mission与Contract必须同源但不互相压缩；
- 自动Registry覆盖；
- prose evidence mapping；
- Gate precision；
- supported Full re-gate；
- cross-book fallback-adjusted E2E。

---

## 11. Final Classification

- Native `DirectorStructuredDecision`模型可执行性：**PASS**。
- Runtime双投影工程可行性：**PASS after deterministic bugfix**。
- 手工Registry跨书known-fact coverage：**PASS，58/58**。
- Independent Contract repeat：**PARTIAL，semantic 3/4**。
- Director Story Blind：**FAIL**。
- Director Authority Blind：**FAIL**。
- Final Story Blind：**DIRECTIONAL PASS**。
- Final Authority Blind：**FAIL**。
- Director wall：**FAIL，慢15.12%**。
- Complete Final Draft E2E：**FAIL，均值慢2.60%**。
- Production adoption：**FAIL**。

> **研究价值很高，Production价值当前为负。**
