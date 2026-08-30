# Verdict

**PARTIAL PASS；不冻结实现为 production。**

来源分层、稳定 ID/slot、显式 `from_state`、unsupported bypass、`human_clause` 禁止等旧风险已在“诚实调用路径”上修正；但仍存在可运行的 false-safe：伪造 Frozen artifact、伪造 provenance、局部替换改变段落拓扑、自由文本双语义，以及 schema/runtime 不一致。

# Fixed Risks Confirmed

- Builder 拒绝裸 `AuthorityFact` 与 self-labelled fragment。[代码](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:706)
- Entity ID、stable slot、unknown dependency、cycle、same-slot conflict、显式 `from_state` 均有实现和测试覆盖。
- Curator 使用正确的 `CURATOR_LOCATION_HINT` 时不会扩大 editable window。
- Preservation Map 与 Contract hash 分离；paragraph hash 可以 JSON round-trip。
- Unsupported contract 不进入 Atomic gate；supported Full 有重新 gate 的路由枚举。[代码](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1205)
- `human_clause` 被拒绝，`surface_note` 不进入 Mission 或 Contract hash。[代码](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:1814)
- 三种自由文本 Sidecar 的否决结论成立：verbose、compact、micro 均不应冻结。

# Remaining Formal Risks

1. **Frozen artifact 不是可信边界。** `FrozenAuthorityArtifact` 可由外部直接实例化；只验证 artifact ID 前缀、SHA 字符串格式和 fact source，不重新计算 digest。[代码](C:/dev/tgn-story-mvp/temps/atomic_authority_ir_v1.py:533)

2. **Registry provenance 只是非空字符串。** `authority_refs=("curator.fake",)` 会被接受；`EntityRegistry.from_dict()` 也不强制校验 `schema_version` 或拒绝额外字段。

3. **Provenance 是可伪造标签。** 调用者把 Curator binding 标成 `PRIMARY_REALIZATION`，即可扩大 editable window。当前代码没有能力边界区分“谁提交的 binding”。

4. **局部编辑没有验证 patch 后拓扑。** replace/delete/insert 可以增加、删除或移动段落，导致原本 locked 的正文整体后移；校验仍可能返回 PASS。

5. **空 fragment 是无效保护。** `exact_fragment=""` 满足 Python 的 `"" in payload`，因此保护条件恒真。

6. **Map 与 Contract 的关联没有被强制验证。** `validate_primary_preservation()` 不接收 Contract，也不检查 `preservation.contract_hash` 是否等于当前 Contract。

7. **Structured Decision 仍有非 typed 语义源。** `narrative_function` 和 `specialty_suggestions` 会进入人类 Mission，却不进入 Frozen Mission facts/hash。它们可以与 typed clauses 矛盾。

8. **ActionSurfaceRegistry 也可产生语义漂移。** 任意 template 都能把 typed action 渲染成相反含义；当前没有固定 registry 的真实性约束。

9. **Schema 与代码不是等价合同。**

   - schema 要求 `specialty_suggestions`，代码允许缺失；
   - schema 禁止额外字段，代码允许额外顶层字段；
   - schema 要求每个 clause 的完整字段，代码大量使用默认值；
   - schema 允许任意 field/kind 组合，代码会拒绝非法组合；
   - schema 不表达 protagonist actor、entity existence、dependency cycle、from-state 等运行时语义。

# False-Safe Counterexamples

- 伪造 Hard source：

  ```python
  fake = FrozenAuthorityArtifact(
      source=AuthoritySource.CANON,
      artifact_id="canon:forged",
      revision_sha256="0" * 64,
      facts=(canon_fact,),
  )
  builder.add_artifact(fake)
  builder.build().preflight_eligible  # True
  ```

- Curator 伪造 Primary provenance：

  ```python
  FactEvidenceBinding(
      fact_id="FACT_PROTECT_ROUTE",
      paragraph_ids=(3,),
      provenance=PRIMARY_REALIZATION,
  )
  ```

  结果会把 P3 加入 editable window。

- 单段替换生成新段落：

  ```python
  replace(P2, "新P2\n\n注入P2")
  ```

  当前结果：`pass=True`，但锁定的 P3 被推到 P4。

- 空保护片段：

  ```python
  ProtectionHint(paragraph_id=2, exact_fragment="")
  ```

  可删除原有商业价值而仍通过保护检查。

- typed action 是“修复粮路”，但：

  ```python
  narrative_function = "主角放弃粮路并立即撤离"
  ```

  人类 Mission 改变，Contract hash 不变。

- 路由只信布尔值：

  ```python
  ContractGateResult(supported=True, pass_=True)
  ```

  即可得到 `ADOPT_DELTA`；没有检查 gate 是否属于同一 Contract、同一正文或同一 chapter。

# False-Fallback Counterexamples

目前没有发现已实现的 unsupported routing 分支把合法 Full 错误拦截；该部分原则是正确的。

但存在接口级 schema/runtime false-fallback：

- 一个 schema-valid、但 field/kind 不合法的 Director payload，会先通过 schema，随后被 Python runtime 拒绝。
- `AtomicAuthorityContract.to_dict()` 的扁平 Contract 输出不能直接被 `load_contract_payload()` 重新加载；二者不是同一序列化合同。
- `PrimaryPreservationMap.from_dict()` 的运行时校验弱于 schema，导致同一 payload 在 schema 与代码之间出现不同结论。

# Evidence Limitations

- 四章静态 fixture 只证明：这四个手工选择的样本可以表达、合并并执行局部校验；不能证明长篇自动生成 Registry、自动抽取事实或真实跨书采用。
- 40 tests 是 40 个 focused test function，未覆盖上述 artifact 伪造、provenance 重标、patch 拓扑、空 fragment、自由字段矛盾、surface template 矛盾。
- 20 schema checks 是 bounded Draft 2020-12 子集检查，不是完整语义验证；不能证明 `Schema valid = runtime valid = story valid`。
- `summary.json` 的“20/20”是检查结果，不代表 20 个正向 artifact；其中包含 3 个 expected-invalid probe。
- Sidecar 的三种失败只证明该批 4 样本中第二份自由语义输出不可接受，不证明原生 structured-output 模型的 Story quality、延迟或最终正文表现。
- `jiuchui_ch16` 的 `historical_delta_locality_pass=false` 与总表“4/4 locality pass”并列存在；这看起来是“预期阻止的非法 mutation”与“pass”字段命名混用，证据应拆成 expected-reject 与 unexpected-failure。

# Freeze / Do Not Freeze

可以冻结：

- Contract 与 Preservation Map 分离；
- stable Entity ID / slot / dependency；
- explicit pre-state，不猜状态；
- unsupported chapter bypass；
- 禁止中文关键词 parser、LLM classifier 与自由文本 Sidecar；
- production pipeline 当前不变。

不要冻结：

- “dataclass 类型即 trusted artifact”；
- 当前 Registry provenance；
- 当前 patch locality 实现；
- `DirectorStructuredDecision` 已经只有一个语义源；
- schema 与 runtime 已一致；
- Native Structured Director 已具备模型证据；
- Atomic fast route 或 Full Reviser 可删除。

# Next Smallest Experiment

先做一个**纯确定性的 adversarial closure test**，不调用 LLM、不改 production：

1. 直接伪造 artifact、篡改 digest、修改 frozen fact 内部 value；
2. 伪造 Registry provenance；
3. 将 Curator binding 重标为 Primary；
4. 测试 replace/delete/insert 改变段落数量；
5. 测试空 fragment；
6. 改写 `narrative_function`、`specialty_suggestions`、surface template；
7. 让 schema-valid payload 逐个经过 runtime。

只有这些边界全部得到明确的 fail-closed 或被正式降级为非权威诊断后，才进入下一步真实 Native Structured Director → Curator → Primary → Full Reviser 实验。
