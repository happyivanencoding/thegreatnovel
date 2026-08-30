# tgn-system-steward 0.3.27 Reviser No-Op Held-out Smoke

> Bounded read-only smoke; no repository mutation by the auditor.

VERDICT: PASS

WHY: 该报告的结论与当前 Steward 实验纪律一致。Candidate 2 的 Story 提升不能证明 Primary 已达到可替代 Full Reviser 的水平，因为其 exact no-op 为 0/8、编辑块增加，且 Authority 与 Hard problems 均恶化。Final Story 较好而 Final Authority 较差，正确归类应是 attention placement 正信号、authority closure 负信号，不能据此跳过 Reviser。Luna-medium 虽节省约 55% Reviser wall 且 Story 守住，但 Authority 57.5 低于 high 的 61.875、Hard problems 为 9 对 3，因此是失败的速度筛选，不能 productionize。两部小说均在 Treatment 冻结及哈希固定后才生成，并使用连续前四章、未按结果挑章，顺序正确地防止了旧 case overfitting。Candidate 1 失败后没有回调它再使用同一 held-out，而是冻结 Candidate 2 后生成全新第二本小说，也符合 held-out 纪律。medium 仅在已完成正式判定的 held-out2 样本上作为 derivation speed screen，并在输给 high 后停止、不再进入第三本找“容易样本”，停线正确。现有证据支持保留 Full Reviser 的必要性边界，不支持把任何单次 Story、相似度或节点 wall 指标外推为生产路由改变。

FREEZE:

- “旧书只作 derivation；Treatment 先冻结并哈希；新小说连续章节作正式 held-out”的方法论。
- Reviser-no-op / effort downgrade 必须同时看 Story 与 Authority gap、Hard problems、edit blocks、exact no-op、独立重复和完整 critical path。
- Story attention 与 Authority closure 必须分开判定；速度候选 Authority 落后 high 即停止。
- 当前 Full Authority Reviser 在被重复证明趋近 no-op 前不得移除或降档。

DO_NOT_FREEZE:

- Candidate 1 自查、Candidate 2 Final Facts Projection，或 Luna-medium Reviser 的任何 production 实现。
- “Primary 可以直接成为 Final”“Full Reviser 可跳过”“medium 可上线”。
- 55.27% 的节省数字作为生产节省承诺，或“Projection 总会伤 Authority”“medium 永远不可用”等永久结论。

NEXT:

保持现有 high 路由不变。若继续研究，只针对 medium 相对 high 重复遗漏的少数 Authority failure family，在 derivation 样本先证明接近 high 后冻结极短 deterministic Watch，再以第三本全新 held-out 验证。

- wall_seconds: 72.616
- model: gpt-5.6-terra
- effort: high
