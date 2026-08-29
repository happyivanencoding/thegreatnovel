你是 TGN Atomic Chapter Obligations 实验的最终证据综合员。只读，不修改项目文件。

读取：
- C:\dev\tgn-story-mvp\PROJECT_RULES.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\BOUNDARY_SPEC.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\PROTOCOL.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\EVIDENCE_INDEX.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\METRICS_SUMMARY.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\phase-g-independent-audits\formal_audit.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\phase-g-independent-audits\story_audit.md
- 需要时读取相关 chapter 的 obligation_pack.json、atomic_gate.json、route_final_body.md 与 production control。

写一份面向作者的中文最终报告。必须：
1. 先给生产决策：区分“边界方法是否成立”“compiler/gate是否可冻结”“Paragraph Delta route是否可 productionize”。
2. 以表格详细说明每类 obligation 的：正状态、负状态、模糊状态、正确边界、fallback规则、反例。
3. 报告 calibration confusion matrix、20章覆盖率、cross-book覆盖率、first/repeat/gate-only/residual的真实 fallback-adjusted wall、repeat exact consensus、Reader/Authority blind。
4. 明确一个 hard obligation 失败为什么必须阻止采用；soft/protected value为什么不能成为 prose quota。
5. 用具体正文例子解释 actor/body-vs-clone、money entitlement-vs-cash、original-vs-copy、battle-scale-vs-stable-tier、deadline-vs-terminal、Reader Release、Human cue、Public Proof、protected commercial value。
6. 不因 Authority胜出忽略 Reader；不因 Reader喜欢忽略 Authority；解释二者分裂。
7. 明确 current v0.1 的领域过拟合与 fail-closed性质。
8. 给出 v0.2 最小下一步，不建议新增 LLM classifier。
9. 不能声称 production 已提速；不能声称已替换 Full Reviser。
10. 只引用证据中存在的数字；若证据缺失，写“未证明”。

结构：
# Atomic Chapter Obligations 实验最终报告
## Final Verdict
## 核心架构
## Obligation 边界总表
## Calibration 与覆盖率
## Runtime / Repeatability / Blind
## 详细正文例子
## Independent Audit Findings
## Production Decision
## v0.2 最小实验
## Evidence Paths
## Validation Checklist
