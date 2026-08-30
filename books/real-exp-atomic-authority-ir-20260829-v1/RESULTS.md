# Atomic Authority IR v1｜最终实验报告

> 日期：2026-08-29  
> 最终分类：**Architecture PASS / Static Implementation PASS / Free-text Sidecar FAIL / Production unchanged**

## 0. Final Verdict

用户提出的清理是正确的，而且解决了旧 Atomic v0.3 最根本的来源混乱。

最终架构不是一个 `AtomicObligationPack`，而是两个彼此独立、权限完全不同的产物：

```text
A. Atomic Authority Contract
   只来自 Frozen Authority typed IR

B. Primary Preservation Map
   只来自 Primary realization location
   + optional Curator location/protection hint
```

结论表：

| 层级 | 结论 | 冻结状态 |
|---|---|---|
| Hard Contract 与 Preservation Map 彻底拆分 | PASS | 冻结为稳定架构原则 |
| Hard Contract 只接受 Frozen Authority artifact | PASS | 冻结 |
| Curator / Primary 不能制造 Hard Fact、Conflict、Identity | PASS | 冻结 |
| Entity ID / stable slot 替代名字优先级与中文反解析 | PASS | 冻结 |
| Edit Locality 默认保护正文 | PASS | 冻结 |
| Unsupported chapter 绕过 Atomic，直接走当前 Full | PASS | 冻结路由原则 |
| verbose / compact / micro 自由文本 Sidecar | FAIL | 明确否决 |
| Native `DirectorStructuredDecision` | Schema / unit ready only | 继续实验，不进 production |
| Atomic fast route / 删除 Full Reviser 固定税 | 未证明 | 不进 production |

Production 仍然是：

```text
Luna high Director
→ Luna high Curator
→ Terra high Primary
→ Luna high Authority Reviser
→ Luna low State
```

本轮没有修改 production 模型、effort、ACP runner、前端或 Direct API executor。

---

## 1. 两个产物必须彻底分开

### 1.1 Atomic Authority Contract

来源只能是：

- Frozen Mission；
- Canon；
- World Authority；
- Power Authority；
- Human Authority；
- Reader Release；
- 它们共同引用的 Entity Registry。

```text
Entity Registry
Frozen Mission IR
Canon IR
World IR
Power IR
Human IR
Reader Release IR
        ↓ trusted Runtime merge
Atomic Authority Contract
```

它只记录已经被创作层决定的机器事实：

- actor → action → object；
- Direct Result；
- State Change；
- Ending；
- ownership / transfer / custody；
- resource / money state；
- time / deadline；
- stable power transition / ability boundary；
- scheduled Reader Release；
- named relationship transition；
- concrete unknown boundary；
- 被 Authority 明确标为 state-bearing 的历史事实。

它不记录：

- 哪一段写得漂亮；
- 主角贪财反应是否有味道；
- 男女之间的一点身体注意；
- Surprise 是否精彩；
- “全场突然安静”是否值得保留；
- Curator 认为哪段更有商业价值。

### 1.2 Primary Preservation Map

```text
Primary Draft
+ fact → paragraph realization bindings
+ optional Curator location/protection hints
+ current blocker fact IDs
        ↓
Primary Preservation Map
```

它只回答：

- Hard Fact 在 Primary 的哪些段落实现；
- 当前 blocker 允许改哪些段落；
- 哪些段落完全锁定；
- editable window 内是否有一个具体 fragment 必须保留。

它没有资格：

- 创建 Fact；
- 创建 Entity ID；
- 创建 Source Conflict；
- 改变 Contract hash；
- 把一个“漂亮反应”升级成 Authority；
- 因为 Curator 写了“无法判断”就让章节 fail closed；
- 扩大可编辑窗口。

因此最干净的名字正式固定为：

> **Atomic Authority Contract + Primary Preservation Map**

不再把 Primary-derived preservation 叫 Atomic Hard Obligation。

---

## 2. Curator 不再是隐藏的 Authority classifier

旧 v0.3 的风险是：`compile_obligations()` 同时读取 `authority_prompt + curator_response + primary_body`；Curator Audit 写一句“无法判断”，代码可能制造 `SOURCE_CONFLICT = HARD`。

v1 改为可信 artifact：

```text
freeze_mission_artifact()
freeze_canon_artifact()
freeze_world_artifact()
freeze_power_artifact()
freeze_human_artifact()
freeze_reader_release_artifact()
```

每个 artifact：

- 有固定 source 类型；
- 有 source-specific artifact ID；
- 有 normalized facts 的 SHA-256；
- 只能由 Runtime 的 source-specific constructor 创建。

`AtomicAuthorityContractBuilder`：

- 拒绝 raw `add_fact()`；
- 拒绝 self-labelled `source=canon` 普通字典；
- 拒绝 `primary / curator / writer / reviser / judge` source；
- Curator diagnostic 只能进入非权威 diagnostics；
- diagnostic 不进入 Contract hash，也不创建 conflict。

受控测试：同一 Hard Contract 追加：

> Curator says: 无法判断，似乎存在冲突。

结果：

- Contract hash 不变；
- facts 不变；
- conflicts 不变；
- preflight eligibility 不变。

真正的 conflict 只由 Authority artifacts 自己比较产生，例如：

```text
Canon：power:PROTAGONIST_001 = TIER_002
Power Authority：同一 pre-chapter slot = TIER_003
```

或：

```text
Canon pre-state = not_paid
Mission transition.from_state = already_received
```

---

## 3. Entity ID 取代“哪个名字优先”

不再冻结：

```text
Mission name > Primary fallback > Human Seed
```

这确实会形成验证循环：Primary 正是待审稿对象，不能反过来决定 canonical protagonist。

v1 使用稳定 Entity Registry：

```yaml
entity_id: PROTAGONIST_001
kind: character
display_name: 顾停舟
aliases: [他, 本体, 少年]
```

Mission Fact：

```yaml
actor_id: PROTAGONIST_001
action_id: defeat
object_ids: [RIVAL_003]
```

正文中的：

```text
顾停舟 / 他 / 少年 / 本体
```

只用于 realization evidence mapping，不反向定义 Identity。

如果 Mission 引用：

```text
PROTAGONIST_999
```

正确结果是：

```text
preflight unsupported
```

而不是猜顾停舟、顾临川谁优先。

两本书静态实验使用相同 `PROTAGONIST_001`、相同 Fact schema，只替换 display name 与 Authority refs；顾停舟与顾临川都可由同一架构表达。

---

## 4. Stable Slot 与 Runtime-owned Fact ID

Director 不应自由创造 persistent fact ID。

跨源依赖引用稳定 slot：

```text
ownership:CONTRACT_ESCORT_001
resource:RESOURCE_PREPAYMENT_001
relationship:PROTAGONIST_001:CHAR_PARTNER_001
power:PROTAGONIST_001
```

Runtime 决定：

- persistent fact ID；
- source / source_ref；
- stable slot；
- mode / phase 默认值；
- cross-source dependency resolution。

Builder 目前验证：

- unknown Entity ID；
- unknown Fact dependency；
- unknown stable slot；
- self-dependency；
- dependency cycle；
- 同 slot / phase 不兼容事实；
- transition `from_state` 与明确 Canon pre-state 不一致；
- 需要 `from_state` 却没有可验证 pre-state。

第一版 Sidecar 已经证明自由 ID 不可靠：Director 为契约结果起一个 ID，Reader Release fixture 引用另一个 ID，两个语义事实其实一致，却因模型 ID 不稳定而 merge 失败。

---

## 5. Story Program、Outline、Director 与 Atomic 的边界

最终责任链：

```text
Story Program
    ↓ 决定长期故事承诺
Outline
    ↓ 决定承诺在哪章兑现
Director
    ↓ 冻结当前章事件和取舍
Runtime
    ↓ 合并已经冻结的 typed Authority
Atomic
    ↓ 验证最终正文没有把决定偷偷写没或写错
```

Atomic 不决定：

- 本章要不要升级；
- 是否得到神器；
- 是否亲女主；
- 是否牺牲某资源；
- 是否震惊所有人；
- 是否发生 Surprise；
- 是否改变关系。

这些仍属于 Story Program / Outline / Director。

Atomic 只知道：

> 既然创作层已经决定了，那么最终正文不要把它偷换成资格、准备、暗示、另一个行动者、另一件物品或未批准结果。

---

## 6. Edit Locality 取代复杂 Commercial Value Detector

默认保护机制不是：

```text
Desire Detector
Relationship Detector
Surprise Detector
Social Repricing Detector
```

而是：

```text
blocker fact evidence = P42–P43
editable = P42–P43
locked = P1–P41 + P44–end
```

如果 P39 有漂亮关系戏，系统无需理解“这是 Relationship”，因为 Delta 根本无权碰它。

只有 blocker 所在段本身也承载商业价值时，才使用极窄的 exact-fragment hint：

```yaml
paragraph_id: 42
exact_fragment: 终于能自己决定怎么花
```

边界：

- hint 必须来自 Primary 已存在 fragment；
- 只能位于当前 editable window；
- 不能扩大编辑窗口；
- 不能创建 Hard Fact；
- 不能改变 Contract hash；
- 不能把 fragment 复制到无关段落来骗过 Preservation check；
- Preservation Map 保存 paragraph SHA-256，底稿发生变化则必须重建。

### 静态两书四章结果

| 样本 | 总段落 | Editable | 比例 |
|---|---:|---:|---:|
| 九垂原 Ch14 | 175 | 3 | 1.71% |
| 九垂原 Ch16 | 101 | 4 | 3.96% |
| 分影 Ch4 | 107 | 2 | 1.87% |
| 分影 Ch9 | 123 | 6 | 4.88% |
| 平均 | — | — | **3.11%** |

结果：

- 4/4 Hard Contract source-pure；
- 4/4 preflight eligible；
- 4/4 合法窗口内修改通过；
- 4/4 窗口外修改被阻止。

真实 Ch16 blocker：

```text
分身携带回潮楔进入第二潮压节点并固定
```

Evidence：

```text
P42 / P45 / P48 / P50
```

旧 Delta 却想顺手改：

```text
P71 / P86 / P96
```

三处全部被 Edit Locality 阻止。

---

## 7. Primary 与 Delta 应该看到什么

### Primary

Primary 正常走：

```text
Director → Curator → Primary
```

Primary 不需要知道 Atomic Contract 的存在，也不吃完整 Atomic Pack。

### Normal Delta

Normal Delta 不应收到十五项检查表；它只按原本的局部修订合同工作。

### Gate / blocker-only residual

```text
Normal Delta
    ↓ local apply
Supported Atomic Gate
    ├─ PASS → Final
    └─ FAIL → 只暴露具体 blocker
                   ↓
             Full / Residual Repair
                   ↓
             Supported Gate again
```

Blocker 示例：

```text
AO-17
Required: RESOURCE_PREPAYMENT_001 = received
Observed: entitlement_confirmed
Allowed locality: P42–P43
```

不把钱、关系、等级、Public Proof、欲望、Reward、Surprise 整包塞回模型。

---

## 8. Historical Claims：只硬化 state-bearing history

取消旧规则：

> 所有“以前说过”的对白都必须存在 Authority。

只有 Authority IR 明确标为 state-bearing critical history 时，才进入 Hard Contract：

- money / resource commitment；
- relationship promise；
- mystery answer；
- current action basis；
- ownership transfer；
- active threat / obligation。

普通生活记忆，例如：

> 母亲以前总说他吃饭太快。

若不改变钱、关系、谜底、所有权、当前行动依据或 active obligation，不要求登记，也不触发 Full fallback。

---

## 9. Routing：Atomic 是加速层，不是全球 Hard Gate

```text
Atomic Contract preflight eligible?
        │
    ┌───┴────┐
    NO       YES
    ↓         ↓
Current Full  Normal Delta
Reviser       ↓
(no Atomic    Supported Gate
post-gate)    ├─ PASS → Final
              └─ FAIL → Full Reviser
                           ↓
                      Supported Gate
                        ├─ PASS → Final
                        └─ FAIL → Residual Failure
```

关键边界：

- Unsupported chapter 直接走今天的 Full Reviser；
- 同一个“不理解本章”的 compiler 不得阻止 Full；
- 只有 preflight 完整支持的章节，Atomic Gate 才有权阻止 Delta / Full；
- supported Full 仍失败，才记录 `FULL_REVISER_RESIDUAL_FAILURE`。

这保证 Atomic 是可选加速层，不是让现有系统更脆弱的新全球 Hard Gate。

---

## 10. Free-text Director Sidecar 实验：明确失败

为了验证“在 Director 同次决策中顺手保存 IR”，测试了三种附加输出。

| 方案 | Parse | Eligible | Structural coverage | Director wall change |
|---|---:|---:|---:|---:|
| Verbose JSON Sidecar | 3/4 | 2/4 | 41.52% | **+205.83%** |
| Compact JSON Sidecar | 3/4 | 1/4 | 47.92% | **+147.41%** |
| Micro DSL | 0/4 | 0/4 | 0% | **+146.45%** |

Micro DSL 平均只有399.5字符、7.25行，仍然很慢且0/4可解析。这证明瓶颈不是单纯输出 token，而是 Director 同时承担：

```text
故事选择
+ 八字段自然语言冻结
+ Entity复制
+ kind分类
+ slot设计
+ dependency维护
+ 格式自校验
```

错误包括：

- 漏 actor；
- 自由 fact ID 导致依赖失效；
- 近似但不存在的 Entity ID；
- stable slot 拼写错误；
- relationship transition 放错 category；
- 把示例句柄 `CP1` 当真实 ID；
- 漏 fenced block。

因此三种 Sidecar 都被否决。

---

## 11. Sidecar Mission 双盲

Compact Treatment 与当前 Control Director Mission：

| Judge | Control | Compact |
|---|---:|---:|
| Story / commercial | **3** | 1 |
| Authority / contract fidelity | 1 | **3** |

它再次证明：

> 机器合同任务提高 Authority 注意力，却挤占“本章最值得看什么”的故事注意力。

所以不能继续把 Sidecar Prompt 越写越短；正确方向必须是**一次原生 typed decision**，而不是同一个模型写两份语义近似的输出。

---

## 12. Native DirectorStructuredDecision

目标不是：

```text
八字段自然语言
+
第二份 Sidecar
```

而是一个 canonical typed object：

```json
{
  "schema_version": "director-structured-decision-v1",
  "chapter_id": "BOOK_A:CH001",
  "protagonist_id": "PROTAGONIST_001",
  "clauses": [
    {
      "field": "protagonist_action",
      "kind": "action",
      "actor_id": "PROTAGONIST_001",
      "action_id": "repair_under_pressure",
      "object_ids": ["ROUTE_001"],
      "surface_note": ""
    }
  ]
}
```

Runtime 从同一 typed object 双投影：

```text
DirectorStructuredDecision
    ├─ ActionSurfaceRegistry → 人类八字段 Mission
    └─ Runtime fact IDs / slots / defaults → Frozen Mission artifact
```

没有第二份自由语义 `human_clause`。否则 typed fields 与 human_clause 会变成两个可能互相冲突的事实源。

`surface_note` 是非权威提示：

- 不进入 Mission事实；
- 不进入 Contract hash；
- 不改变 Entity / slot / transition。

### 当前已证明

- 57项 focused tests 通过；
- trusted artifact issuer/digest、空合同拒绝、不可变Registry/Contract/Map、Entity provenance、slot/dependency cycle、from-state、Contract snapshot round-trip、Primary Evidence签发/底稿哈希、Contract↔Preservation绑定、paragraph topology、unknown boundary、routing、Edit Locality、stale Primary hash、Curator不可扩窗等均有负例；
- 4个 Schema definitions、13个正向 artifact/runtime checks 与5个 expected-invalid probes，共22/22 checks通过；
- stale `human_clause` 被 Schema拒绝；
- 缺 artifact provenance 被拒绝；
- Preservation Map 缺 paragraph hashes 被拒绝；
- 没有新增外部依赖。

### 当前没有证明

- 真实 Director 模型能原生输出该结构；
- Story质量不下降；
- Director wall不增加；
- Entity Registry可自动覆盖长篇；
- typed decision 接回 Curator/Primary后的最终正文质量；
- Atomic Delta真正跨书采用；
- Full Reviser固定税已经减少。

因此它是：

> **Schema/unit-ready experimental architecture，不是已成功的模型路线。**

---

## 13. What Can Freeze

可以冻结：

1. `Atomic Authority Contract ≠ Primary Preservation Map`；
2. Hard Contract只来自可信 Frozen Authority artifacts；
3. Curator/Primary不能创建Hard Fact、Source Conflict或Entity Identity；
4. Entity ID替代名字优先级；
5. Runtime掌握persistent fact ID、stable slot、dependency；
6. Edit Locality是默认商业价值保护方式；
7. Protection hint不能扩窗，也不能升级为Authority；
8. Critical state-bearing history才进入Hard Contract；
9. unsupported chapter绕过Atomic走当前Full；
10. supported Full才做post-gate；
11. Primary不看完整Atomic Pack；
12. Delta只看blocker与窄locality；
13. Native structured decision只保留一份typed语义，human Mission由Runtime投影；
14. Story Program / Outline / Director继续拥有升级、神器、爱情、Surprise、Public Proof等创作权。

## 14. What Must Not Freeze

不得冻结：

- verbose / compact / micro Sidecar；
- 当前手工fixture作为production Authority；
- 当前Entity/Fact schema已自动覆盖长篇；
- `Schema valid = Story quality valid`；
- `Authority fidelity更好 = 可以上线`；
- Native structured Director已完成真实模型实验；
- Full Reviser已可删除；
- 任何production speedup数字；
- Curator/Primary的判断进入Hard Contract；
- 重新发展一个中文关键词/句法 Obligation Parser。

---

## 15. Native E2E Follow-up（2026-08-30）

原定下一实验已经完成：`DirectorStructuredDecision → Runtime双投影 → Curator → Primary → Authority Reviser → Final Draft`。

最终有效比较使用两本书四章、2次真正串联的Fresh Control与2次bugfix-freeze后的Native v2 Treatment；早期Sidecar、v1污染轮次与独立节点Control不进入最终速度结论。v2 8/8 Native accepted、手工expected fixture结构覆盖100%，但semantic Hard Contract repeat只有3/4，说明route可运行不等于语义完全稳定。

匿名纯正文Blind：Mission Story **6.99 vs 8.60**、Mission Authority **6.55 vs 8.41**，均明显输Control；下游将其重新小说化后Final Story **8.41 vs 7.88**方向性更好，但Final Authority **6.79 vs 8.04**仍明显退化。根因不是Runtime projection慢，而是typed core把Story Mission压得过薄：下游为了补回冲突、选择、Public Proof和具体利益关系重新获得了发明空间。

真实Final Draft wall：Control **325.954s/章**，Native **351.566s/章**，Native慢 **25.612s/章（7.86%）**。Primary research Oracle只有2/8足够安全可直接Final；即使假设一个完美且零成本的deterministic Gate，也只有理论 **1.68% / 5.466s每章**的节省。

因此新的decision model是：

1. `Atomic Authority Contract ≠ Story Mission`，就像它也不等于Primary Preservation Map；
2. Hard IR继续保持窄、typed、source-pure，但不负责承载“这一章为什么值得看”的全部Story realization；
3. 下一候选把money/ownership/power/relationship/Reader Release/unknown/Ending等Hard IR前移到Story/Outline/Runtime原本就作出这些决定的地方，不要求Director重新编码；
4. Director继续保留高故事密度human Mission；
5. 只有后台Gate在跨书真实正文上证明足够可靠后，才重新测试跳过Full Reviser；不新增LLM safety classifier。

完整证据：`books/real-exp-native-structured-e2e-20260830-v1/RESULTS.md`。

---

## 16. Production Decision

- **Source boundary cleanup / Atomic Authority Contract / Primary Preservation Map：PASS as architecture/backend research。**
- **Free-text Director Sidecar：FAIL。**
- **Current Native Structured Director as human Mission replacement：FAIL。**
- **Final Story signal：DIRECTIONAL PASS，但不能覆盖Final Authority退化。**
- **Latency：FAIL，完整Final Draft慢7.86%。**
- **Full Authority Reviser removal / Atomic fast route：NOT PRODUCTION。**
- **Current five-node production：unchanged。**


## 17. Validation

- Atomic Authority IR focused tests: **57 passed**.
- Full repository regression: **421 passed**.
- Atomic Authority IR experiment scripts compiled: **10**.
- Static two-book/four-chapter contracts: **4/4 eligible and 4/4 source-pure**; average editable ratio **3.11%**.
- Schema/runtime validation: **22/22 checks passed**; **5/5 expected-invalid probes rejected**.
- `git diff --check`: PASS.
- `tgn-system-steward 0.3.21`: validate / install / activate PASS; digest `sha256:b95296af5b5142e578a6385e2d44c655a924aac960118090439e9a90ba375bdd`.
- Post-install bounded smoke: `PARTIAL`, correctly freezing architecture/trust/locality principles while refusing native Director, automatic Registry/binding and Atomic fast route as production claims.
- Production five-node chain, models, ACP runner, frontend and Direct API executor: unchanged.

