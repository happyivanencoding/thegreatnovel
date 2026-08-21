# Efficiency report

Hybrid token fields are actual runtime values when available; this run returned no token usage, so input/output/total tokens remain `UNKNOWN`. Character counts are observations and are not token estimates.

| lane | chapter | calls | executed nodes | skipped nodes | actual tokens | prompt chars | response chars | final source |
|---|---:|---:|---|---|---|---:|---:|---|
| Hybrid · 《炉藏万象》 | 1 | 5 | director, chapter_prep, curator, primary, state_delta | integrator | UNKNOWN | 32403 | 13297 | primary |
| Hybrid · 《炉藏万象》 | 2 | 5 | director, chapter_prep, curator, primary, state_delta | integrator | UNKNOWN | 88160 | 16770 | primary |
| Hybrid · 《炉藏万象》 | 3 | 5 | director, chapter_prep, curator, primary, state_delta | integrator | UNKNOWN | 102994 | 15528 | primary |
| Single Control · 《炉藏万象》 | 1—3 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 17709（三章正文合计） | Single Control |
| Hybrid · 《掌中天工》 | 1 | 8 | director, chapter_prep, curator, primary, opening, action, integrator, state_delta | 无 | UNKNOWN | 62720 | 18693 | integrator |
| Hybrid · 《掌中天工》 | 2 | 8 | director, chapter_prep, curator, primary, dialogue, action, integrator, state_delta | 无 | UNKNOWN | 126863 | 24357 | integrator |
| Hybrid · 《掌中天工》 | 3 | 7 | director, chapter_prep, curator, primary, action, integrator, state_delta | 无 | UNKNOWN | 137308 | 27614 | integrator |
| Single Control · 《掌中天工》 | 1—3 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 16531（三章正文合计） | Single Control |

Single Control 的旧实验没有可核验的真实 token/call manifest，因此 token、calls 和 prompt chars 严格写 `UNKNOWN`；没有把字符数换算成 token。
