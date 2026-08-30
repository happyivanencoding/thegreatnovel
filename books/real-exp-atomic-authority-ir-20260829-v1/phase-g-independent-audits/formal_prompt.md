你是 TGN Atomic Authority IR v1 的独立形式化架构审计员。只读，不修改项目文件。

读取：
- C:\dev\tgn-story-mvp\PROJECT_RULES.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\ARCHITECTURE.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\PROTOCOL.md
- C:\dev\tgn-story-mvp\temps\atomic_authority_ir_v1.py
- C:\dev\tgn-story-mvp\temps\test_atomic_authority_ir_v1.py
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\phase-a-static-ir\summary.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\phase-b-director-sidecar\summary.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\phase-c-compact-director-sidecar\summary.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\phase-d-micro-director-sidecar\summary.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-authority-ir-20260829-v1\phase-f-schema-validation\summary.json

审计目标：
1. Hard Contract 是否真的只有 Frozen Authority；Curator/Primary是否还能通过diagnostic、entity resolver、evidence binding、contract hash或repair target偷渡hard fact/conflict/identity。
2. Entity ID是否消除了Primary fallback验证循环；别名是否只用于realization evidence。
3. same-slot conflict、from-state、unknown entity、fact/slot dependency是否正确fail closed。
4. Primary Preservation Map是否只控制edit locality；Curator hint能否扩窗、创造fact、改变hash。
5. Unsupported chapter是否确实绕过Atomic并走当前Full ungated；supported Full才做post-gate。
6. ordinary history vs state-bearing critical history边界是否干净。
7. DirectorStructuredDecision能否作为单一structured source双投影human mission和hard facts，避免double write。
8. verbose/compact/micro sidecar失败是否足以否决prompt附加格式，还是还有遗漏解释。

每个问题给：风险等级、最小反例、当前代码如何处理、是否需要修复。不要建议扩中文关键词parser，不要建议新增LLM classifier。

严格输出：
# Overall Verdict
# Source Purity Audit
# Entity / Identity Audit
# Conflict and Dependency Audit
# Preservation Map Audit
# Routing Audit
# Director Structured Decision Audit
# Remaining False-Safety Risks
# What Can Freeze
# What Must Remain Experimental
