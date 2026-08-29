你是 TGN Atomic Chapter Obligations 的独立形式化边界审计员。只读，不修改任何文件。

先读取：
- C:\dev\tgn-story-mvp\PROJECT_RULES.md
- C:\dev\tgn-story-mvp\temps\atomic_chapter_obligations.py
- C:\dev\tgn-story-mvp\temps\test_atomic_chapter_obligations.py
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\BOUNDARY_SPEC.md
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\phase-b-calibration\summary.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\phase-f-full20-audit\summary.json
- C:\dev\tgn-story-mvp\books\real-exp-atomic-chapter-obligations-20260829-v1\phase-e-crossbook-compile\summary.json

目标：找出会导致错误 ADOPT_DELTA 的 false negative、会导致无谓 full fallback 的 false positive、以及 compiler/domain overfit。重点逐项审计：
1. actor/action/object 与代词、别名、集合主体、被动句；
2. ownership vs possession vs title vs custody，original/copy，多次 transfer；
3. entitlement/quote/contracted/paid/received/refunded/lost/disputed；
4. deadline/window/cooldown/terminal state；
5. battle scale/pressure/result vs stable power transition；
6. Reader Release 的 timing 与一次可复述事实；
7. unresolved-fact 禁止揭示但允许新证据；
8. Human cue 的 named person + contact/treatment trigger；
9. Public Proof 的 result/ruler/repricing，不能成为三段 quota；
10. protected commercial value 不能成为逐句保留或禁止改写。

每个问题必须给：最小反例候选、当前代码预期会怎样判、正确判定、建议是 test / compiler / validator / fail-closed 哪一层处理。不要建议新增 LLM classifier。

严格输出：
# Overall Verdict
# Highest-Risk False Negatives
# Highest-Cost False Positives
# Domain Generalization Failures
# Missing Boundary Tests
# Recommended v0.2 Scope
# What Must Remain Fail-Closed
