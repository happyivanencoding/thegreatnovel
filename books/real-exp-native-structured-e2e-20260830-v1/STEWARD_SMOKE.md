# tgn-system-steward 0.3.24 Native E2E Smoke

> Bounded read-only smoke; no repository files modified by the auditor.

VERDICT: FAIL

TIME_VERDICT: 未节约；完整 Final Draft 链平均每章慢 8.915 秒（-2.60%），Director 节点每章慢 4.869 秒（-15.12%）。

QUALITY_SPLIT: Mission Story -1.288、Mission Authority -2.712；Final Story +0.562，但 Final Authority -1.850，且已出现会污染 Canon 的硬退化。

WHAT_CAN_FREEZE:
- Atomic Authority Contract 与 Primary Preservation Map 的严格分离。
- 可信 Frozen Authority、Entity ID / stable slot、Runtime 签发 evidence binding、Edit Locality。
- unsupported 章节绕过 Atomic、回到当前 Full Reviser 的路由。
- typed core、human Mission、Final Story、Final Authority 分开验收的方法。
- Native structured decision 仅作为研究后端；生产默认继续使用 free-text Director。

WHAT_MUST_NOT_FREEZE:
- 当前 Native human Mission 替代 production free-text Director。
- “Native 更快”或“Runtime 投影近乎免费”等速度结论。
- 移除每章 Full Authority Reviser。
- 手工 Registry / Action Catalog 的长篇通用性、自动 paragraph locator、当前 ActionSurface 模板。
- 用 58/58 已知事实覆盖或 Final Story 小幅胜出掩盖 Authority 失败。

WHY: V2 在冻结 surface 后，以两本书四章、两次独立 Treatment、两次 Fresh Control 和 16 次清洗一致的匿名盲评完成，证据可用于本次裁决。完整关键路径均值为 Native 1406.264 秒、Control 1370.605 秒，因此替代路线没有速度收益。Runtime 双投影约 1.7ms 并非瓶颈，真正增加成本的是 Director 同时完成故事取舍、实体绑定、动作分类、状态转移和 schema 自校验。Native human Mission 在四章 Mission Story 与 Mission Authority 均未获第一，说明它压缩掉了下游必须保留的故事和事实带宽。Final Story 虽略有提升，但 Final Authority 明显下降，不能构成可接受的生产交换。实际硬退化包括未经授权的肉身蛮力、能力边界越界、固定报酬改为浮动结价、关系揭示时序改变，以及提前结算待遇。58/58 只证明手工 Registry 下已登记事实可覆盖，不证明长篇自动 Registry、完整语义 Contract 或正文事实保真。独立重复中 semantic Hard Fact set 仅 3/4 一致，而 V1 更直接证明“typed Contract 正确、human projection 仍可错误”。因此可冻结的是 Atomic 的信任与隔离架构，不是当前 Native human Mission 生产替代路线。

NEXT_SMALLEST_EXPERIMENT: 保持现有丰富的 free-text Director Mission 不变，后台并行生成 Atomic Authority Contract；Primary 正常写作，在完整支持章节上测试“Atomic Gate PASS 跳过 Full Reviser，FAIL 则 Full Reviser fallback 并 re-gate”的 fallback-adjusted 跨书 E2E。

- wall_seconds: 98.603
- model: gpt-5.6-terra
- effort: high
