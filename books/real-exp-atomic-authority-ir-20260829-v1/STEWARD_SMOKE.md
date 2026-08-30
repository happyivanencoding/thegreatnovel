# tgn-system-steward 0.3.21 Atomic Authority IR Smoke

> Bounded read-only smoke; no repository file was modified by the audit agent.

VERDICT: PARTIAL

KNOWLEDGE_CLASS: Stable Principle + Current Default + Experimental Hypothesis

WHY: 物理拆分 Contract 与 Preservation Map、来源专属冻结、私有签发、摘要校验、不可变快照和 Runtime 证据绑定，已经有足够证据冻结为稳定架构原则。57/57 focused tests、22/22 schema/runtime checks、5 个 invalid probes，以及四章全通过，证明当前 IR 的信任边界和拒绝逻辑在 bounded fixture 范围内成立。Paragraph topology、locked hash、同一 Contract hash 和窗口外阻止，也足以冻结为 Preservation/Edit Locality 原则。可是 Registry、Authority fixture 和 fact-to-paragraph binding 仍由人工构建，不能证明自动长篇覆盖。Native DirectorStructuredDecision 只有 schema/unit 证据，没有真实模型 Story、latency、E2E 或独立重复证据。Verbose、compact、micro Sidecar 的性能退化和 compact blind 偏置，构成不应恢复 free-text Sidecar 的反证。Unsupported 章节绕过 Atomic、supported Full 经过 post-gate 的路由原则是安全的，但不等于 Atomic fast route 已被证明更快或可普遍采用。因此当前 IR 可作为受边界约束的 production safety substrate，native Director 与 Atomic fast route 尚不能作为 production 默认路径。

WHAT_CAN_FREEZE:

- Contract 与 Preservation Map 的物理分离。
- Hard Contract 只接受 Runtime source-specific Frozen Authority artifacts 与 Entity Registry；Curator/Primary 不得创建 Fact、Conflict、Identity。
- Private issuer、normalized-fact SHA-256、immutable snapshot、snapshot reload verification。
- Runtime 签发并绑定 Primary hash 的 evidence binding、Edit Locality、paragraph topology 与 locked hash。
- Entity/slot 边界，以及 unsupported Full bypass、supported Full post-gate 的路由原则。
- 不恢复 free-text verbose/compact/micro Sidecar。

WHAT_MUST_NOT_FREEZE:

- 手工 Entity Registry、四章手工 Authority fixture 或自动长篇 registry 能力。
- 自动 fact-to-paragraph locator。
- Native Director 的模型质量、延迟和 E2E 稳定性。
- Atomic fast route 的速度、覆盖率或默认生产路由地位。
- 移除 Full Reviser，或把 Atomic 变成全局 hard gate。

NEXT_SMALLEST_EXPERIMENT: 在不改生产五节点的隔离 runner 中，仅替换 Director 输入为真实 native `DirectorStructuredDecision`；用同一两本书四章、Story/Authority 分离上下文、至少三次独立重复，完整跑 `Director → Runtime Frozen Mission → Contract → Primary binding → Delta → Gate`，并与当前 Full baseline 比较 source-purity、eligible/fallback、最终正文 authority 变化和 fallback-adjusted complete-route wall。只有真实 E2E、跨书重复、自动 binding 成立且速度收益仍存在，才考虑 productionize fast route。

- wall_seconds: 101.671
- model: gpt-5.6-luna
- effort: high
