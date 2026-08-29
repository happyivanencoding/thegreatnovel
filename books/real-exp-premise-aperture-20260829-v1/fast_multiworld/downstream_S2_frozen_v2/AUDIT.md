# FROZEN PREMISE CONTRACT V2 AUDIT

## Verdict

- **Selected S2 downstream integration: FAIL.** The premise cannot legally reach Story Program without changing approved World / Power / Human facts.
- **Lane-specific frozen-contract behavior: PASS.** V2 fixed the three silent rewrites found in V1 and then failed loudly at the first remaining cross-authority contradiction instead of smoothing it.
- **Production freeze: NOT AUTHORIZED.** This one case proves the contract can preserve and stop; it does not prove the Forge consistently emits authority-compilable premises.

## Direction Preservation Table

| Direction | Result | Evidence |
|---|---|---|
| World-only | PRESERVED | 万言城、命令改变现实、声位秩序均进入 World。 |
| World Interface-only | PRESERVED | 公开重映成为对所有符合条件的命令事件都成立的 protagonist-blind 世界规则。 |
| Ontology-only | PRESERVED | 主角始终是会爬行的黑色活字，不恢复标准人形。 |
| Initial Origin-only | PRESERVED | Human 从公开处刑、死者喉中掉出“不跪”的 T0 开始；没有出生前训练、职业、关系或旧胜负。 |
| Power trigger / coverage / boundary | PRESERVED | Power 保留“真正击败 + 对方刚说过 + 字面执行 + 门/兵器/野兽/人体四类载体 + 载体毁则命令消失”。 |
| Full Story Promise | CONTRADICTED BY ITS OWN FROZEN RULES | Story Program returned `PREMISE-AUTHORITY CONFLICT` rather than inventing missing causal bridges. |

## V1 → V2 Delta

V1 的 lane isolation 虽然通过，却发生三项静默改写：出生被搬到旧训练场破旗；Power 从四类载体缩窄成只作用于活人；公开重映降成终局偶发演出。

V2 使用同一预注册 S2、同一 Power candidate 2、同一 Human candidate 2，只把作者选择编译成精确 lane payload。三项漂移全部消失。因此已经证明：

> lane-safe 不等于 premise-safe；作者选择必须进入现有 Authority 的 binding generation contract，而不是柔性 Direction。

## Remaining Cross-Authority Conflicts

Story Program 正确停止，原因有四项：

1. 开篇让全场跪者弹起、执行官反跪，超出 T0 仅能让自身“不跪”的权限，也发生在“真正击败并夺词”之前；
2. 开篇全城开门要求未批准的复制、塔网因果放大或共同载体；
3. World 主尺为声位 1—100，Human T0 却冻结为声位 0；没有 protagonist-blind 的 0级/未登记通用规则；
4. 终局一句“醒来”解除全城永久命令，假设了未定义的共同载体并扩写命令字面。

这些不是 Story Program 应该修的剧情小问题。任何继续生成都会重新走向两种错误之一：削弱标志性 Promise，或扩写 Frozen Power / World。

## Architecture Consequence

当前证据支持保留：

- Single-Agent 完整 premise 搜索；
- 作者选择；
- lane-specific frozen contract；
- 显式 `PREMISE-AUTHORITY CONFLICT`；
- Outline / chapter 不读取 raw Premise Card。

当前证据不支持直接冻结整条 production 接线。Forge 还需要在候选输出内部暴露 `Authority-Compilation Trace`，逐项证明第一章动作、T0 尺位置和远期复合由现有字段合法推出。它仍应由同一个 Forge 完成，不新增 Judge / Reviewer / Hard Gate。

## Runner Diagnostic

第一次 resume runner 曾把嵌在 ACP 推理前言末尾的 conflict token 漏掉，误开始准备 Outline 输入；没有生成 Outline。检测器现已改为：接受 token 后紧跟明确拒绝生成的形态，同时继续忽略“不触发 conflict”的否定提及，并加入回归测试。
