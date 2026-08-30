# Atomic Authority IR v1｜实验协议

> 日期：2026-08-29  
> 状态：Experimental，不接 production。

## 1. 研究问题

验证以下分层是否比旧 Atomic v0.3 更干净、更通用：

```text
A. Atomic Authority Contract
   只来自 Frozen Authority typed IR

B. Primary Preservation Map
   只描述 Primary 如何实现事实、允许改哪些段落、哪些已有价值不能被局部修订擦掉
```

必须证明：

1. Curator / Primary 无法创建 Hard Fact、Entity Identity 或 Source Conflict；
2. 当前人物通过 Entity ID 绑定，不存在“Mission 名字优先还是 Primary 名字优先”的验证循环；
3. Primary Preservation Map 不改变 Hard Contract hash；
4. Edit Locality 能在不做 Desire / Surprise / Relationship 语义分类的情况下锁住绝大多数正文；
5. Unsupported chapter 直接走现有 Full Reviser，Atomic 不成为新的全球 Hard Gate；
6. 自由文本 Sidecar 是否可行；若不可行，是否应改成单一 canonical `DirectorStructuredDecision`，由 Runtime 双投影 Mission 与 Mission IR。

## 2. 架构

```text
Story Program
    ↓ story promises
Outline
    ↓ chapter allocation
Director
    ├─ Human-readable Frozen Mission
    └─ Machine Atomic Mission IR

Runtime deterministic merge
    ├─ Entity Registry
    ├─ Mission IR
    ├─ Canon IR
    ├─ World IR
    ├─ Power IR
    ├─ Human IR
    └─ Reader Release IR
           ↓
    Atomic Authority Contract
```

独立的 realization 路径：

```text
Primary Draft
+ optional Curator location/protection hints
        ↓
Primary Preservation Map
        ├─ fact → paragraph evidence location
        ├─ blocker edit windows
        ├─ locked paragraphs
        └─ optional exact fragments inside editable windows
```

## 3. Hard Contract 来源规则

只允许：

- Frozen Mission；
- Canon；
- World Authority；
- Power Authority；
- Human Authority；
- Reader Release。

禁止：

- Primary；
- Curator / Curator Audit；
- Reviser；
- Judge；
- Writer self-report。

Curator 可以写诊断或定位提示，但：

- 不创建 Fact；
- 不创建 Entity ID；
- 不创建 Source Conflict；
- 不改变 Contract hash；
- 不扩大可编辑窗口。

## 3.1 Trusted artifact and snapshot boundary

- Hard facts enter only through source-specific Runtime freezers with a private issuer and SHA-256 over normalized facts.
- Directly constructed or digest-tampered artifacts are rejected.
- Empty contracts are unsupported.
- Registry, Contract, nested Fact payload and Preservation Map are immutable snapshots.
- Serialized Contract reload reconstructs every source artifact, verifies fact membership and digest, rebuilds conflicts/unsupported state and compares the final Contract hash.
- Primary evidence bindings are Runtime-issued, bound to the Primary SHA-256 and cannot be manufactured by Curator.
- Preservation validation requires the same chapter and Contract hash; paragraph topology and all locked paragraph hashes must remain unchanged.

## 4. Entity ID

所有 Hard Fact 只引用稳定 ID：

```text
protagonist_id = PROTAGONIST_001
actor_id = PROTAGONIST_001
object_ids = [RIVAL_003]
```

正文中的名字、代词、称呼与本体/分身只用于 realization evidence mapping，不反向决定 canonical identity。

Mission 引用未知 ID，或同一 slot/phase 出现不兼容 Authority fact，均 preflight fail closed。

## 5. Primary Preservation Map

默认使用 Edit Locality，而不是复杂商业语义分类：

```text
AO-17 只修付款
→ evidence 位于 P42–P43
→ 只开放 P42–P43
→ P1–P41 与 P44–结尾全部锁定
```

Curator / Primary 可以补充：

- 该 Hard Fact 当前实现在哪些段落；
- editable window 内哪个具体 fragment 已经写得好，修订时应保留。

它们不能声明：

- “这一章必须增加 Surprise”；
- “这里是 Hard Relationship Fact”；
- “某人是 protagonist”；
- “Authority 有冲突”。

## 6. Routing

```text
Atomic preflight eligible?
        │
    ┌───┴───┐
    NO      YES
    ↓        ↓
Current Full  Normal Delta
Reviser       ↓
ungated      Supported Atomic Gate
              ├─ PASS → Final
              └─ FAIL → Full Reviser
                          ↓
                     Supported Gate
                       ├─ PASS → Final
                       └─ FAIL → Residual Failure
```

Atomic 不支持的章节直接走今天的 production Full Reviser，不再用同一个不支持该章节的 compiler 阻塞 Full。

## 7. Historical Claims

不建立“所有旧对白必须登记”的全局规则。

只有 Authority IR 明确标为 state-bearing critical history，才进入 Hard Contract，例如：

- money / resource commitment；
- relationship promise；
- mystery answer；
- current action basis；
- ownership transfer；
- active threat or obligation。

普通生活记忆、无状态影响的旧话不触发 Full fallback。

## 8. 实验阶段

### Phase A｜Source-pure static IR

使用两本书、四章，手工把已决定的 Frozen Authority 转写为同一套 ID/Fact schema：

- 九垂原第14章；
- 九垂原第16章；
- 分影原型第4章；
- 分影原型第9章。

验证 Contract source purity、Entity IDs、跨书 schema 与 Edit Locality。

### Phase B｜Director free-text Sidecar negative experiment

冻结原 Director prompt，追加 Entity Registry 与严格 JSON sidecar输出要求；使用 Luna high 同时生成：

- 原八字段 Mission；
- Mission IR sidecar。

比较：

- 原 Mission vs Sidecar Treatment Mission；
- Sidecar JSON/schema/entity validity；
- 与人工 authority fixture 的结构覆盖；
- Control / Treatment Director wall；
- 独立 Judge 对 Mission质量与 IR忠实度的判断。

另做 compact JSON 与 micro DSL。三者只用于验证“附加第二份机器语义”是否可行；失败后不得继续作为目标架构。

### Phase C｜Routing / locality mutation

受控测试：

- Curator/Primary source injection；
- unknown entity；
- same-slot Authority conflict；
- Canon from-state mismatch；
- P42–P43 locality；
- window外编辑；
- editable window内 exact-fragment preservation；
- unsupported chapter bypass；
- supported Full residual failure。

### Phase D｜Native structured decision schema

建立单一 `DirectorStructuredDecision`：模型只返回 typed clause；Runtime使用 `ActionSurfaceRegistry` 渲染八字段Mission，并确定性构建Frozen Mission artifact。

明确禁止第二份可自由表达相反语义的 `human_clause`。`surface_note` 仅为非权威诊断，不进入Mission事实或Contract hash。

本阶段只验证：

- schema；
- trusted provenance；
- Entity / slot / dependency / from-state；
- dual projection；
- negative probes。

没有原生structured-output模型运行时，不得声称Director模型行为已成功。

## 9. Production Gate

Atomic Authority IR v1 只有在以下条件全部满足后，才可继续做真实快速章节 E2E：

- source purity 100%；
- Entity ID 与 Authority merge 100% deterministic；
- cross-book schema 至少覆盖不同角色/能力/资源/关系类型；
- Native structured Director 的 Mission-level Story / Authority blind 不劣；
- Preservation平均编辑窗口足够小；
- unsupported chapter明确绕过 Atomic；
- 没有把 Primary/Curator realization 偷渡成 Hard Authority；
- 不新增 LLM safety classifier。

即使以上通过，也只说明 IR架构可进入下一实验，不等于 Full Reviser 已可删除。
