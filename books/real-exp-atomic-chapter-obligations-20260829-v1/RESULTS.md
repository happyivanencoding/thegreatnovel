# Atomic Chapter Obligations｜v0.3 Final Experiment Report

> Date: 2026-08-29  
> Status: **PARTIAL / Experimental Method Pass; Production Route Fail**  
> Production runtime changed: **No**

## 0. Final Verdict

Atomic Chapter Obligations 的**判断方法成立**：把 Frozen Authority 编译为 typed obligations，再用代码检查完整最终正文，比“让另一个 LLM 判断这章安不安全”更可信。它能明确表达并检查：

- `actor → action → object`；
- Direct Result / State Change / Ending；
- ownership / transfer / copy / custody；
- money / entitlement / payment / loss；
- time window；
- stable power position / battle scale / cooldown；
- Public Proof；
- Reader Release；
- unresolved facts；
- named relationship transition；
- triggered Human cue；
- Primary 已存在的 desire / relationship / reward / surprise / social repricing；
- 全文既有的未授权历史回指。

但当前 v0.3 **不能进入 production**：

1. 第二本书 5/5 preflight fail closed，说明当前词表和 typed grammar 仍高度领域化；
2. 20章 shadow 只有 10/20 进入可判定区；
3. 两次四章真实 Delta 路线都只有2章采用、1章回退、1章 Full Reviser 后仍 residual failure；
4. 采用后的 Delta 仍不稳定：原始 Delta 只有 1/4 完全一致；最终 route 3/4 一致主要因为 fallback/full 把两次结果收敛，唯一持续采用的第9章仍不一致；
5. 当前 Gate 能证明“已知义务闭合”，不能证明 prose 已达到顶级男频；有效 Blind 中 Reader 对采用稿是 Atomic 1 / Control 1，Authority 是 Atomic 2。

因此当前只冻结：**Boundary Specification、校准方法、fail-closed 原则、Full fallback 后再验证原则。** 不冻结自动快路，不修改五节点 production 链。

## 1. Boundary Decision Table

| Boundary | Safe interpretation | Unsafe interpretation | Gate |
|---|---|---|---|
| Actor identity | Current Mission actor outranks stale Human/Book name; explicit current Primary is fallback only when Mission is generic. | Remote Human Seed silently replaces current protagonist; nearby pronoun repairs explicit wrong actor. | HARD / fail closed |
| Actor → Action → Object | Same bounded action domain binds actor, verb and object. | Body replaces clone; ally A performs ally B action; chapter-wide keyword stitching. | HARD |
| Direct Result / State / Ending | Each terminal result is separately true by chapter end. | Can / prepares / basis / qualification / future pressure used as completion. | HARD |
| Ownership / copy / custody | Original, copy, possession, custody, use right and title remain distinct. | Official receives original when only copy was authorized; possession upgraded to title. | HARD |
| Money / payment | received ≠ entitlement ≠ pending ≠ lost ≠ disputed; authorized partial stays partial. | First payment satisfies full settlement; invented amount/unit; entitlement becomes cash. | HARD |
| Time window | Deadline remains a boundary unless current Mission requires completion now. | Before next low tide is rewritten as already completed; preparation becomes departure. | HARD |
| Power position | Stable tier, battle output, temporary composite effect and cooldown remain separate. | Higher-scale resistance becomes stable breakthrough; cooldown becomes terminal dissipation or vice versa. | HARD |
| Public Proof | Same protagonist/topic has performance → qualified ruler → behavioral repricing. | Three unrelated paragraphs are combined; unrelated commodity repricing counts as protagonist proof. | HARD when triggered |
| Reader Release | Only scheduled fact is clearly released once. | Unscheduled encyclopedia becomes quota; terminology without reader-understandable fact counts. | HARD when scheduled |
| Unresolved fact | No-invention boundary; silence is allowed. | Unknown old history becomes certain; “do not invent” is misclassified as source conflict. | HARD negative boundary |
| Human cue | Same named person + direct contact/treatment + approved Human authority. | Generic humanity, attraction, scent or body detail becomes chapter quota. | CONDITIONAL |
| Relationship state | Explicit transition binds the named counterpart. | Cooperation with one person satisfies a different relationship transition. | CONDITIONAL / terminal when specified |
| Commercial value | Desire, relationship, reward, surprise and repricing are protected only if Primary already has them and Delta touches them. | Every chapter must add payoff/surprise; ordinary object inspection replaces a surprise turn. | PRESERVE_IF_PRESENT |
| Prior-dialogue history | A line framed as previously spoken already exists in Frozen Authority. | Primary/Delta invents “he had said …” and fast gate preserves it because Delta did not create it. | HARD whole-draft scan |
| Source conflict | Two incompatible authoritative states fail preflight. | Missing detail / keep unknown / missing repetition context is treated as conflict. | DIAGNOSTIC; true conflict only |
| Full fallback | Full Reviser output passes the same gate. | Expensive model ran, therefore output is automatically safe. | HARD post-fallback gate |


## 2. Calibration and Coverage

### 2.1 Controlled boundary tests

- Focused tests: **33 passed**.
- Known-bad historical mutations: **12/12 detected**, 0 missed.
- These mutations measure recall only; they do not prove safe precision.

### 2.2 Historical Full Reviser is not gold

20章 shadow：

- preflight eligible: **10/20**；
- fail closed: **10/20**；
- historical Full passed current Gate: **5/20**；
- historical Full blocked: **15/20**。

这不能直接解读为“15章 Full 都错”，因为其中包含 unsupported grammar、缺失 Authority、真冲突和可能的保守误报。它证明的是：**不能拿历史 Full 输出反向定义 Gate 的正确答案，也不能因为 Full 已运行就跳过 closure。**

### 2.3 Cross-book coverage

第二本书 5 个样本：

- preflight eligible: **0/5**；
- fail closed: **5/5**；
- Delta adoptable: **0/5**。

Fail closed 比误放行安全，但也明确证明当前 compiler 不是 production-general schema compiler。

## 3. Real Delta Route

### 3.1 Final v0.3 routing

| Chapter | Run 1 | Run 2 | Meaning |
|---:|---|---|---|
| 2 | Full fallback | Full fallback | Primary/Delta 保留未授权的旧对话回指；Full 删除后通过 |
| 9 | Adopt Delta | Adopt Delta | Reader 与 Authority 都偏 Atomic；两次 Delta 文本仍不同 |
| 14 | Adopt Delta | Adopt Delta | Public Proof 在同一表现链中闭合；Reader 偏 control、Authority 偏 Atomic |
| 16 | Residual failure | Residual failure | Delta 与历史 Full 都未闭合 actor/object；显式 fallback 仍漏 cooldown |

Run 1 的 observed cost through detection：

- control Full total: **554.409s**；
- Atomic route through detection: **346.032s**；
- nominal fallback-adjusted reduction: **37.59%**。

Run 2：

- control Full total: **554.409s**；
- Atomic route through detection: **327.254s**；
- nominal reduction: **40.97%**。

这些不是可交付 production speedup：第16章停在 `FULL_REVISER_RESIDUAL_FAILURE`，若继续修复还需额外调用，必须另计成本。

### 3.2 Effective blind

只统计 v0.3 实际会采用、且最终正文 hash 与原匿名盲评选项完全一致的章节：

- Reader: Atomic **1** / Control **1**；
- Authority: Atomic **2** / Control **0**。

样本只有第9、14章，不能据此生产化。

## 4. Boundary Findings with Concrete Examples

### 4.1 Current Mission actor must beat stale Human Seed

旧编译器会从远端 Human Seed 提取主角名。若当前 Mission 已换成顾停舟、远端卡仍写顾临川，actor-action-object 可能整章绑定错人。v0.3 改为：

`Current Mission explicit actor > explicit current Primary fallback > remote Human seed`。

### 4.2 First payment is not full settlement

`首笔个人矿利已经到账` 只能满足明确允许 partial 的义务，不能满足“个人矿利全部结清”。Authority 未给金额时新增金额也失败；给出八百潮铢时，改成一千潮铢同样失败。

### 4.3 Public Proof must be one causal chain

第14章的有效链是：

> 顾停舟用回潮楔锁住并改动潮压方向；白须老人用成炉正常值和四十丈位移做校准；随后场内目光、报价、追索和个人矿利登记发生变化。

三部分距离可以跨多个短段，但必须是同一主角、同一器物/力量主题、同一结果的 `performance → ruler → repricing`。章内另一匹马或另一笔商品报价不能拼进来。

### 4.4 Unknown boundary is not source conflict

“乌合本人是否到场未知，不得补写”是 no-invention boundary；“Reader Release 第4章才允许落籍，但当前 Mission 第3章要求完成落籍”才是真冲突。把所有“无法判断”都当冲突，会制造安全幻觉：通过率很低，但不是判断更准。

### 4.5 Gate must inspect Primary defects that Delta did not create

第2章 Primary 已经写：

> 少东家那句“回去再算”。

Frozen Authority 并没有这句已发生旧话。Delta 只改低潮窗口，因此旧 Gate 会放行；Full Reviser删除了这句。v0.3 增加 whole-draft prior-dialogue scan，所以两次 Delta 都转为 Full fallback。

### 4.6 Full fallback may still fail

第16章 Delta 未闭合“分身携带回潮楔进入第二节点”的 actor/object。历史 Full 也仍未闭合；一次显式 Atomic-aware Full fallback 耗时95.865s后，仍漏“再次使用前必须散尽残压”的 cooldown boundary。该路线累计153.35s，对比原 Full 120.371s，**慢27.4%且仍不可保存**。

## 5. What Can Freeze

可以冻结为稳定方法论：

1. typed obligation family 与 mode：terminal / pending / conditional / must-remain-unknown / preserve-if-present；
2. Current Mission actor 优先于远端人物卡；
3. money / ownership / power / time 的状态格必须拆开；
4. Public Proof 三部分必须同题同人同因果链；
5. Unknown boundary 与 source conflict 分离；
6. protected commercial value 只保护 Primary 已有内容，不生成配额；
7. Gate 要扫描完整最终正文，也要捕捉 Primary 既有 Authority 错误；
8. Full fallback 后必须再次过 Gate；
9. known-bad recall、safe boundary tests、shadow control、repeat、cross-book、Reader+Authority 必须分开报告。

## 6. What Must Not Freeze

不得冻结：

- 当前 v0.3 词表/规则作为通用 production compiler；
- `Gate pass = 顶级男频质量`；
- `historical Full pass/fail = Gate gold label`；
- `Delta fail → Full 一定安全`；
- 以四章 nominal 37.59% / 40.97% 宣称生产加速；
- 新增 LLM classifier 替代 deterministic closure；
- 把欲望、Reward、Surprise、Public Proof 变成每章硬配额。

## 7. Next Smallest Experiment

下一步应先做**通用 Schema Compiler**，不是继续换 Prompt：

1. 从 Frozen Mission 的结构化字段直接生成 actor/action/object、terminal status、time、ownership、money、power，而不是依赖小说专名词表；
2. 把 Named Entity、Power Scale、Resource Type、Relationship Counterpart 从 Authority metadata 注入 typed registry；
3. 在第二本书达到可解释的 preflight coverage 后，再生成新 Delta；
4. residual blocker 只把失败义务交给 Full Reviser，修后再次过 Gate；
5. 重新做 repeat + cross-book + Reader/Authority + fallback-adjusted complete-route wall。

## 8. Production Decision

**Atomic Chapter Obligations：PARTIAL / Methodology and boundary spec pass.**  
**Atomic fast route：FAIL AS PRODUCTION DEFAULT.**  
**Production five-node chain：unchanged.**
