# Free-text Director + Atomic Primary Bypass Gate｜Protocol Freeze v1

日期：2026-08-30

## Hypothesis

保留当前 rich free-text Director Mission，不让 typed IR 替代 human Mission。Primary 之后运行后台 deterministic Atomic Gate：

```text
rich free-text Director → Curator → Primary
                              ↓
                    deterministic Atomic Gate
                    PASS → Primary 直接 Final
                    FAIL/UNSUPPORTED → Full Authority Reviser
```

## Matched control

每个样本的 Control 与 Treatment **共享同一次** fresh Director、Curator、Primary：

- Control Final = Full Authority Reviser output；
- Treatment Final = Gate PASS 时 Primary；Gate FAIL/UNSUPPORTED 时同一 Full Reviser output。

实验仍会为 Gate PASS 样本跑一个 shadow Full Reviser，以便匿名质量比较；该 shadow call 不计入 Treatment critical path。

## Frozen gate scope

- `jiuchui_ch14`：SUPPORTED；验证回潮楔单次完整用法、公开判尺、自主权、个人矿利、水路矿权排除、有价独立合作、残压冷却、旧关期限。
- `shadow_ch9`：SUPPORTED；验证伤势处理、混合欲望、影身伤势回流、关系风险边界、顾斜阳重新估价、伤势未愈、双线记录触发护卫价值重估，并拦截远程感知/提前付款。
- `jiuchui_ch16`：UNSUPPORTED；当前需要对“本体/分身/回潮楔”的分布式 actor-action-object 和 unknown/ending 语义做可靠证明，现有 deterministic adapter 不足。
- `shadow_ch4`：UNSUPPORTED；当前需要区分“公开两胜”与“公开名次结算”，并验证回客舍后的私密分影 reveal timing，现有 adapter 不足。

这不是恢复旧中文 Obligation parser，也不是 production classifier。它是两个预注册 typed realization adapter 的高 precision 实验；unsupported 必须 fallback。

## Pre-freeze calibration

在此前未参与本轮新生成的 `fresh-control-3/4` rich free-text Primary 上：

- strict Authority Oracle：5/8 可直接 Final；
- deterministic Gate：4/8 PASS；
- Gate false-safe：0/8；
- safe false-fallback：1/8；
- 10 个定点 hard-fact mutation 均被阻断。

这些数据只用于冻结 Gate；最终结论只看冻结后的 fresh runs。

## Final experiment

- 2 books × 4 chapters；
- 2 independent fresh repeats；
- models/effort：Director Luna high；Curator Luna high；Primary Terra high；Fallback/Shadow Reviser Luna high；
- Gate 不调用 LLM，实测自身 wall；
- 每个 Gate PASS Primary 用两个 fresh Authority Oracle 独立复核；任一 Oracle 判 FALLBACK 即记 false-safe/unsafe；
- Gate PASS 样本做匿名 Primary-vs-Reviser Story Blind + Authority Blind；
- 报告完整 per-chapter critical-path wall、skip rate、supported pass rate、false-safe、safe false-fallback、Reader/Authority、repeat；
- 不使用 Judge 参与实际路由。

## Freeze rule

从第一轮 fresh Director 调用开始，不再修改 Gate 规则、supported sample set、模型、effort、样本或 Judge 标准。若 Gate 暴露 false-safe，记录 FAIL，不追着样本改规则。
