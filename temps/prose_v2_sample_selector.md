你是 TGN Prose Projection A/B 的样本选择器。只读，不修改文件，不生成正文。

从以下候选中为四个 Scene Family 各选 1 个最干净的现有样本：ENTRY_EXPLORATION、COMPLEX_ACTION、DISCOVERY_REVEAL、EMOTION_RELATIONSHIP。

候选目录：
- books/real-exp-curator-primary-longform-v1/candidate-b/runs/chapter-0010
- books/real-exp-clean-e2e-scene-skill-v11-10ch/chapter-0006
- books/real-exp-clean-e2e-scene-skill-v11-10ch/chapter-0003
- books/real-exp-clean-e2e-scene-skill-v11-10ch/chapter-0008
- books/real-exp-prose-execution-v1/runs/chapter-0001
- books/real-exp-xianxia-blind-v1/runs/chapter-0002
- books/real-exp-opening-reader-first-fresh-v1/runs/chapter-0001
- books/real-exp-opening-reader-first-fresh-v1/runs/chapter-0002
- books/real-exp-human-reaction-ch3-v1/runs/chapter-0003

每个目录读取 curator_prompt.md / curator_response.md / primary_prompt.md（存在时），只判断：
1. 主要 prose problem 是否接近单一 Scene Family；
2. Chapter Mission / Canon / BOOK Prose Profile 是否足够完整，可以冻结 A/B；
3. 是否会把 Dialogue/Payoff/工程流程等其它主问题混进来；
4. Complex Action 必须真的有多位置/追逐/多人/路线变化，简单一对一不算；
5. Emotion 必须主要是关系/私人余波，不是战斗后顺带一个反应；
6. Reveal 必须有证据→局部判断→仍保留未知的空间。

输出很短：
# Sample Selection
- ENTRY_EXPLORATION: <path> — <1-2句理由>
- COMPLEX_ACTION: <path> — <理由>
- DISCOVERY_REVEAL: <path> — <理由>
- EMOTION_RELATIONSHIP: <path> — <理由>
## Reject Notes
只列最容易误选的 2-4 个候选及原因。
