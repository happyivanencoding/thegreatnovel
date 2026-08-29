VERDICT: NEEDS_FIX

- 必须文件缺失：`RESULTS.md`、`EVIDENCE_INDEX.json`、`METRICS_SUMMARY.json`、`phase-g-independent-audits/formal_audit.md`、`story_audit.md`均不存在；当前只有草稿、prompt 和 ACP JSON。正式报告不可验收。[RESULTS_DRAFT.md](C:/dev/tgn-story-mvp/books/real-exp-atomic-chapter-obligations-20260829-v1/RESULTS_DRAFT.md:13)

- 20 章数字错误。报告称 phase-g2 为 `9/20 eligible、11/20 fail closed、4 pass、16 blocked`，但实际 phase-g2 summary 是 `10/20、10/20、5 pass、15 blocked`。[RESULTS_DRAFT.md](C:/dev/tgn-story-mvp/books/real-exp-atomic-chapter-obligations-20260829-v1/RESULTS_DRAFT.md:84) [summary.json](C:/dev/tgn-story-mvp/books/real-exp-atomic-chapter-obligations-20260829-v1/phase-g2-all20-shadow-corrected/summary.json:4)

- fallback 成本账不完整：`phase-e-atomic-full-fallback` 的 `242.205s` 有效路径、`-101.22%` 相对速度未纳入报告；full20 与 cross-book 也没有 wall 字段，报告应明确写“未测”，不能让读者误以为已覆盖。

- Reader/Authority 口径仍需明确标注来源：corrected phase-i key 支持各为 Delta 2、Control 1、Mixed 1，但 `story_audit_acp.json` 的叙述使用了不同票数口径。报告虽提及早期冲突，却未把两套分母和最终采用依据完整列出。

- cross-book unsupported 数字应按章节映射；报告写成 `3、3、4、5、6`，实际顺序为 Ch1=6、Ch4=3、Ch6=3、Ch8=5、Ch10=4，当前表述容易误读。

- 正确项：hard obligation 与 `preserve_if_present` 边界基本正确；报告没有声称 production 已提速或替换 Full Reviser，也没有建议新增 LLM classifier。对应边界规范明确保持 fail-closed、不得替换 Full Reviser、不得以 LLM classifier 作为 adoption gate。[BOUNDARY_SPEC.md](C:/dev/tgn-story-mvp/books/real-exp-atomic-chapter-obligations-20260829-v1/BOUNDARY_SPEC.md:231)

本轮只读，未修改文件。

<oai-mem-citation>
<citation_entries>
MEMORY.md:1111-1112|note=[用于核对Reader优先级、已批准权威优先级与冲突显式化原则]
</citation_entries>
<rollout_ids>
</rollout_ids>
</oai-mem-citation>
