你是只读的 TGN 形式化架构审计员。不要修改文件。

读取：
- C:\dev\tgn-story-mvp\PROJECT_RULES.md
- C:\dev\tgn-story-mvp\temps\atomic_authority_ir_v1.py
- C:\dev\tgn-story-mvp\temps\test_atomic_authority_ir_v1.py
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\ARCHITECTURE.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\PROTOCOL.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\RESULTS.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\EVIDENCE_INDEX.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\phase-f-schema-validation\summary.json

这是修正后版本。重点检查旧风险是否已真正解决：
1. Hard Contract 是否只能接受可信 FrozenAuthorityArtifact，Primary/Curator 是否还能伪造 hard source/conflict/identity；
2. Entity ID / stable slot / provenance / dependency cycle / from-state；
3. Primary Preservation Map 是否完全独立，Curator hint 能否扩窗，paragraph hash 是否可序列化/恢复；
4. unsupported chapter bypass 与 supported Full re-gate；
5. `DirectorStructuredDecision` 是否仍有双语义源；Schema是否与代码一致；
6. 还有哪些 false-safe、false-fallback 或手工 fixture 自证问题；
7. 静态4章、40 tests、20 schema checks、三种Sidecar失败，足以证明什么、不足以证明什么。

请给最小反例；不要建议中文关键词parser或LLM classifier。
严格输出：
# Verdict
# Fixed Risks Confirmed
# Remaining Formal Risks
# False-Safe Counterexamples
# False-Fallback Counterexamples
# Evidence Limitations
# Freeze / Do Not Freeze
# Next Smallest Experiment
