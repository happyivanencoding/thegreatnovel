# Overall Verdict

结论：`PARTIAL PASS`，不能作为 production formal safety freeze。

现有 30 个单元测试通过，但主要验证正向路径；源码探针确认仍有多个 fail-open：

- 缺失 `from_state` 时仍可 preflight eligible；
- `RepairTarget` 可直接打开任意段落、任意半径；
- Preservation Map 不验证传入底稿是否仍是原底稿；
- Curator evidence binding 可间接扩大 edit window；
- structured human clause 可与 typed fact 不一致；
- second Frozen Mission 防护可被大小写绕过；
- 依赖只检查存在，不检查自循环、环、语义一致性；
- 来源是自报字符串，不是真正的 Frozen Authority provenance。

因此，当前架构分层可冻结为实验设计；实现安全性和 native structured response 仍必须实验。

# Source Purity Audit

相关规范见 [ARCHITECTURE.md:7](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/ARCHITECTURE.md:7)、[PROTOCOL.md:63](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/PROTOCOL.md:63)。

- 已成立：diagnostic 不能制造 hard fact/conflict/hash。

  风险：低。

  最小反例：`builder.add_diagnostic("似乎存在冲突")`。

  当前代码：diagnostics 只进入 `diagnostics` 列表，不参与 `conflicts`、`preflight_eligible` 或 `contract_hash`。[atomic_authority_ir_v1.py:443](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:443)

  是否需要修复：否。

- 问题：source purity 依赖调用方自报 `source`，不是实际 Authority provenance。

  风险：高。

  最小反例：Curator 提交：

  ```python
  {"source": "canon", "facts": [{"fact_id": "F", ...}]}
  ```

  当前代码：只要 source 标签是 `canon`、`world_authority` 等允许值，就会被接受；`authority_refs` 也只检查非空，不检查其真实来源。[atomic_authority_ir_v1.py:291](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:291)、[atomic_authority_ir_v1.py:432](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:432)

  是否需要修复：是。否则只能说“来源标签纯”，不能说 Hard Contract 真正只来自 Frozen Authority。

- 已成立：Primary、Curator、Writer 等显式 source 名称会被拒绝。

  风险：无。

  最小反例：`source="primary"`。

  当前代码：`SourcePurityError`。[atomic_authority_ir_v1.py:293](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:293)

  是否需要修复：否，但它不能弥补上一条的 provenance spoofing。

- 问题：第二个 Frozen Mission 防护大小写敏感。

  风险：高。

  最小反例：

  ```python
  authority_fragments=({"source": "FROZEN_MISSION", "facts": [...]},)
  ```

  当前代码：`DirectorStructuredDecision.build_contract()` 只比较精确字符串 `"frozen_mission"`；后续 `add_fragment()` 会统一转小写并接受。[atomic_authority_ir_v1.py:1464](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1464)、[atomic_authority_ir_v1.py:432](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:432)

  是否需要修复：是。

- 已成立：Curator diagnostic、Preservation Map、ProtectionHint 不进入 Contract hash。

  风险：无。

  当前代码：hash 只使用 chapter、registry、facts、conflicts、unsupported。[atomic_authority_ir_v1.py:384](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:384)

  是否需要修复：否。

# Entity / Identity Audit

相关规范见 [ARCHITECTURE.md:95](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/ARCHITECTURE.md:95)、[PROTOCOL.md:90](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/PROTOCOL.md:90)。

- 已成立：Hard Fact 使用 entity ID，Primary 名字不会反向改变 protagonist identity。

  风险：低。

  当前代码：`resolve_surface()` 只返回匹配 ID 集合，不修改 Registry；Hard Fact 的 actor/object/counterparty 仍使用 ID。[atomic_authority_ir_v1.py:219](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:219)、[atomic_authority_ir_v1.py:253](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:253)

  是否需要修复：否。

- 已成立：未知 entity ID 在 Contract build 时 fail closed。

  风险：无。

  当前代码：进入 `unsupported`，使 `preflight_eligible=False`。[atomic_authority_ir_v1.py:459](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:459)

  是否需要修复：否。

- 问题：micro handle 可以把 `P` 映射为 rival。

  风险：高。

  最小反例：

  ```python
  handles = {"P": "RIVAL_001"}
  A|P|act|ROUTE_001|-
  ```

  当前代码：只检查映射后的 ID 是否存在，不检查 `P` 是否必须等于 Registry 的 protagonist。[atomic_authority_ir_v1.py:1180](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1180)

  是否需要修复：是。

- 问题：structured `protagonist_action` 也不要求 actor 是 protagonist。

  风险：高。

  最小反例：将该 clause 的 `actor_id` 改为 `RIVAL_001`，仍是合法 character ID。

  当前代码：只验证 actor ID 存在，不验证与 `protagonist_id` 相等。[atomic_authority_ir_v1.py:1339](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1339)

  是否需要修复：是。

- 边界：alias resolver 本身不产生身份，但也没有强制调用方对多重匹配 fail closed。

  风险：中。

  当前代码：文档说 ambiguous alias 返回全部 ID；模块没有后续消费者来保证 `len(matches) != 1` 时拒绝。[atomic_authority_ir_v1.py:219](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:219)

  是否需要修复：集成层需要明确拒绝规则；不需要新增中文关键词 parser。

# Conflict and Dependency Audit

相关代码见 [atomic_authority_ir_v1.py:453](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:453)。

- 已成立：同一 `slot + phase` 的不兼容事实会 conflict。

  风险：低。

  当前代码：按 slot/phase 分组并比较 canonical signature。[atomic_authority_ir_v1.py:487](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:487)

  是否需要修复：否。注意这不是“同 slot 跨 phase 全部冲突”；当前规范明确的是 `slot + phase`。

- 已成立：未知 fact dependency、未知 stable slot 会 fail closed。

  风险：无。

  当前代码：分别进入 `unsupported`。[atomic_authority_ir_v1.py:470](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:470)、[atomic_authority_ir_v1.py:476](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:476)

  是否需要修复：否。

- 问题：缺失 `from_state` 时 fail open。

  风险：高。

  最小反例：只有一个 `POWER_TRANSITION`，声明 `from_state="TIER_002"`，但没有任何 pre-chapter state。

  当前代码：只有 `current` 存在且不相等时才 conflict；`current=None` 直接放行。[atomic_authority_ir_v1.py:517](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:517)

  是否需要修复：是。未知起始状态应阻断 transition。

- 问题：dependency 只检查存在，不检查环、自循环或依赖语义。

  风险：高。

  最小反例：

  ```python
  fact.slot_id = "S"
  fact.depends_on_slots = ("S",)
  ```

  当前代码：`S` 已在 `known_slots` 中，因此 preflight eligible。fact-ID 依赖也没有环检测。[atomic_authority_ir_v1.py:476](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:476)

  是否需要修复：是。至少要拒绝 self/cycle；stable slot 解析也不能只做字符串存在性检查。

- 问题：`UNKNOWN_BOUNDARY` 没有强制 `MUST_REMAIN_UNKNOWN`。

  风险：高。

  最小反例：`kind="unknown_boundary", mode="terminal"`。

  当前代码：compact/micro 都允许任意合法 FactMode；Contract 仍可 eligible。[atomic_authority_ir_v1.py:936](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:936)、[atomic_authority_ir_v1.py:1174](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1174)

  是否需要修复：是。

- 问题：`value`、`metadata`、slot 名称仍是任意数据，没有真正的 typed semantic boundary。

  风险：中。

  最小反例：在一个 `DIRECT_RESULT` 中放入任意未批准的 nested `value`，Contract 仍可通过。

  当前代码：`value` 是 `Any`，metadata 直接进入 canonical signature/hash。[atomic_authority_ir_v1.py:259](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:259)、[atomic_authority_ir_v1.py:337](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:337)

  是否需要修复：是，否则“typed IR”仍保留未约束事实容器。

# Preservation Map Audit

相关规范见 [ARCHITECTURE.md:41](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/ARCHITECTURE.md:41)。

- 已成立：ProtectionHint 本身不能解锁 locked paragraph，也不改变 Contract hash。

  风险：无。

  当前代码：hint 只验证片段存在；不在 editable window 时仅记录 diagnostic。[atomic_authority_ir_v1.py:673](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:673)

  是否需要修复：否。

- 问题：Curator 的 `FactEvidenceBinding` 可以间接扩大 edit window。

  风险：高。

  最小反例：Curator 将已有 hard fact 绑定到 P39：

  ```python
  FactEvidenceBinding(
      fact_id="FACT_PROTECT_ROUTE",
      paragraph_ids=(39,),
      provenance=CURATOR_LOCATION_HINT,
  )
  ```

  再以该 fact 作为 `RepairTarget`。P39 会进入 editable。

  当前代码：binding 的 provenance 不参与 locality 计算，所有 evidence location 一律进入 `fact_evidence`。[atomic_authority_ir_v1.py:632](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:632)

  是否需要修复：是。

- 问题：`RepairTarget.explicit_paragraph_ids` 与 `locality_radius` 可绕过 authority locality。

  风险：高。

  最小反例：

  ```python
  RepairTarget(
      fact_ids=(),
      explicit_paragraph_ids=(1,),
      locality_radius=999,
  )
  ```

  当前代码：显式段落直接 editable，radius 只做非负裁剪，没有上界。[atomic_authority_ir_v1.py:647](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:647)

  是否需要修复：是。当前代码无法证明 RepairTarget 只代表当前 blocker。

- 问题：`paragraph_hashes` 没有被验证，底稿漂移可无操作通过。

  风险：高。

  最小反例：Map 用 `P1 original` 构建，验证时传入 `P1 CHANGED`，operations 为空。

  当前代码：`validate_primary_preservation()` 不比较当前 paragraph hashes；该反例返回 pass。[atomic_authority_ir_v1.py:744](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:744)

  是否需要修复：是。

- 问题：exact fragment 是全局查找，不保证仍在原 paragraph。

  风险：中。

  最小反例：同一 fragment 同时存在于 locked P1 与 editable P2；删除 P2 版本后，候选正文仍因 P1 含该片段而通过。

  当前代码：使用 `if hint.exact_fragment not in candidate`，没有按 paragraph 定位。[atomic_authority_ir_v1.py:753](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:753)

  是否需要修复：是。

- 实验反证：Phase A 的普通 locality 指标通过，但 `jiuchui_ch16` 的 historical locality 仍失败，P71、P86、P96 触碰 locked paragraphs。[summary.json:53](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/phase-a-static-ir/summary.json:53)

  是否需要修复：需要修正实验结论或实现；不能用 top-level `locality_allowed_pass=4` 宣称 locality 已整体证明。

# Routing Audit

相关代码见 [atomic_authority_ir_v1.py:779](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:779)，规范见 [PROTOCOL.md:127](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/PROTOCOL.md:127)。

- 已成立：Contract preflight 不 eligible 时，走当前 Full Reviser ungated。

  风险：无。

  当前代码：`preflight()` 返回 `CURRENT_FULL_REVISER_UNGATED`；`after_full()` 也返回 ungated final。[atomic_authority_ir_v1.py:782](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:782)

  是否需要修复：否。

- 已成立：supported Full 才会进入 post-gate。

  风险：低。

  当前代码：supported contract + supported gate 才返回 `FINAL_AFTER_SUPPORTED_FULL`。[atomic_authority_ir_v1.py:805](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:805)

  是否需要修复：否。

- 边界问题：`ContractGateResult.supported=False` 在 `after_delta()` 中仍路由到 Full 后 supported gate。

  风险：中。

  最小反例：contract preflight eligible，但 gate 报 `supported=False`。

  当前代码：返回 `FULL_REVISER_THEN_SUPPORTED_GATE`。[atomic_authority_ir_v1.py:791](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:791)

  是否需要修复：取决于字段含义。如果它表示“Atomic Delta 不支持但 Full 支持”，当前行为正确；如果它表示“该章节不支持 Atomic”，则违反 ungated bypass。当前 API 没有区分这两种状态。

  是否需要修复：是，至少应拆分语义或明确调用约定。

- 当前仅验证 policy enum，没有真实 Full Reviser、post-gate、State closure 的调用链。

  风险：中。

  是否需要修复：是，production 前必须做真实 routing E2E。

# Director Structured Decision Audit

相关代码见 [atomic_authority_ir_v1.py:1268](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1268)。

- 实验结论：三种自由文本附加格式足以否决“直接追加到 Director prompt”的当前方案。

  - verbose：parse 3/4，merged eligible 2/4，wall +205.83%。[phase-b summary:3](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/phase-b-director-sidecar/summary.json:3)
  - compact：parse 3/4，merged eligible 1/4，wall +147.41%。[phase-c summary:3](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/phase-c-compact-director-sidecar/summary.json:3)
  - micro：parse 0/4，merged eligible 0/4，wall +146.45%。[phase-d summary:3](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/phase-d-micro-director-sidecar/summary.json:3)

  风险：对这三种已测试格式，否决结论充分。

  是否需要修复：否。应保留为实验否决结论。

- 但这不足以证明 native structured response 已安全。

  风险：高。

  当前代码：Phase F 只报告 schema/artifact checks 17/17，通过的是结构与解析验证；`invalid_checks=0`，没有覆盖语义冲突、dependency、from-state、authority provenance 或 human/typed divergence。[phase-f summary:5](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/phase-f-schema-validation/summary.json:5)

  是否需要修复：是，必须保持实验状态并补 semantic negative tests。

- 问题：human clause 与 typed fact 不是同一语义投影。

  风险：高。

  最小反例：把 `direct_result` 的 `human_clause` 改成“主角已经拿到金矿所有权”，但 typed fields 不改。

  当前代码：human mission 使用 `human_clause`；Contract hash 不包含它。测试本身确认 human mission 可变化而 hash 不变。[test_atomic_authority_ir_v1.py:579](C:/dev/tgn-story-mvp/temps/test_atomic_authority_ir_v1.py:579)、[atomic_authority_ir_v1.py:1475](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1475)

  是否需要修复：是。否则这是同一 envelope 中的两次语义写入，而不是单一 structured source 双投影。

- 问题：structured decision 允许重复 field、无限 clause。

  风险：中。

  最小反例：提交两个 `protagonist_action` 或多个相同 slot 语义的 clause。

  当前代码：只要求八种 field 至少各出现一次，不限制重复数量。[atomic_authority_ir_v1.py:1409](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1409)

  是否需要修复：是。

- 问题：structured clause 的 `mode`、`terminal`、`value`、`metadata` 组合缺少语义一致性检查。

  风险：中。

  当前代码：允许例如 `ENDING + MUST_HOLD + terminal=False` 等组合。[atomic_authority_ir_v1.py:1315](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1315)

  是否需要修复：是。

# Remaining False-Safety Risks

- ordinary history 与 state-bearing critical history 的边界目前只是调用约定。

  风险：高。

  最小反例：用 `HISTORICAL_CLAIM_BOUNDARY` 标记普通生活旧话，或用任意 metadata 伪装成 `money`/`relationship` critical history。

  当前代码：类型存在，但没有 domain allowlist、criticality 约束或来源级验证；compact/direct path 都可以创建它。[atomic_authority_ir_v1.py:88](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:88)

  是否需要修复：是。应使用确定性的显式字段约束，不需要新增 LLM classifier 或中文关键词 parser。

- Phase C 文件名与协议阶段含义不完全一致。

  风险：中。

  `PROTOCOL.md` 把 Phase C 定义为 routing/locality mutation，[PROTOCOL.md:191](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/PROTOCOL.md:191)；实际提供的 Phase C summary 是 compact sidecar experiment。[phase-c summary:2](C:/dev/tgn-story-mvp/books/real-exp-atomic-authority-ir-20260829-v1/phase-c-compact-director-sidecar/summary.json:2)

  是否需要修复：是，修正实验索引，否则读者会误以为 routing/locality 已由该 phase summary 覆盖。

- schema valid 不等于 authority safe。

  风险：高。

  当前代码和 Phase F 都能证明 JSON 形状、字段和 artifact envelope，但不能证明来源、身份、事实依赖和语义边界。

  是否需要修复：是，必须补负例，而不是继续增加 schema syntax checks。

# What Can Freeze

可以冻结为“实验架构结论”：

- Hard Contract 与 Primary Preservation Map 的概念分离；
- diagnostic、ProtectionHint 不应成为 Hard Authority；
- Hard Fact 使用 Entity ID，alias 只用于 realization evidence；
- 基本 same-slot/same-phase conflict；
- unknown entity、unknown dependency、unknown slot 的基础 fail-closed；
- unsupported preflight 走当前 Full ungated；
- 三种已测自由文本 sidecar 不适合作为当前 prompt 附加格式；
- 不新增中文语义 parser，不新增 LLM safety classifier；
- Director native structured response 是合理的实验方向。

# What Must Remain Experimental

以下不能冻结为 production safety：

- “只有 Frozen Authority”这一强 provenance 结论；
- Preservation Map 的 edit locality gate；
- Curator evidence binding 与 RepairTarget 组合；
- `from_state`、dependency cycle、unknown boundary 的 fail-closed 语义；
- ordinary history / critical history 的自动边界；
- `DirectorStructuredDecision` 的 human mission 与 hard facts 双投影；
- structured response 的 semantic validity；
- `ContractGateResult.supported` 的 routing 语义；
- Phase F 的 17/17 schema validation 作为整体安全证明；
- 任何替代 Full Reviser 的 production rollout。

未修改任何项目文件。
