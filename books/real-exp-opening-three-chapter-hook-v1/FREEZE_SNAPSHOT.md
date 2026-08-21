# Freeze Snapshot

| Candidate | 书名 | Fantasy Seed | World Vision | Story Program | Frozen long-form design | 旧前三章对照 |
|---|---|---|---|---|---|---|
| candidate-a | 《偷走明天的人》 | `real-exp-dynamic-pacing-v1/candidate-a/legacy_seed.md` | `real-exp-dynamic-pacing-v1/candidate-a/treatment_world_vision.md` | `real-exp-dynamic-pacing-v1/candidate-a/treatment_story_program.md` | `real-exp-dynamic-pacing-v1/candidate-a/treatment_outline.md`，N=60 | `real-exp-prose-execution-parallel-v1/candidate-a/chapter-01..03/formal_prose.md` |
| candidate-b | 《炉藏万象》 | `real-exp-clean-e2e-novel-v1/seed/selected_candidate.md` | `real-exp-clean-e2e-novel-v1/world/world_vision_response.md` | `real-exp-clean-e2e-novel-v1/story/story_program_response.md` | `real-exp-clean-e2e-novel-v1/outline/outline_response.md` | `real-exp-clean-e2e-novel-v1/chapter-01..03/chapter.md` |
| candidate-c | 《掌中天工》 | `real-exp-dynamic-pacing-v1/candidate-b/legacy_seed.md` | `real-exp-dynamic-pacing-v1/candidate-b/treatment_world_vision.md` | `real-exp-dynamic-pacing-v1/candidate-b/treatment_story_program.md` | `real-exp-dynamic-pacing-v1/candidate-b/treatment_outline.md`，N=96 | `real-exp-prose-execution-v1/chapters/chapter-0001..0003.md` |

复制到本目录后，冻结上游分别位于每个 candidate 的 `source/`；`source/frozen_outline.md` 只作为长期设计与旧输入证据，Pilot 仍重新生成 `outline/outline_response.md`，不重新生成前三份创意产物。

旧前三章只用于后验盲读，不进入新生成 Prompt。GBrain、Reference Programs、旧 Prompt、旧 Review 和另一候选内容均不进入本次生成上下文。

