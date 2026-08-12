# Serial Scheduler 验收

Scheduler 输出一个 Primary Intent、最多两个 Secondary Intent、why-now、支持它的 Debt / Anticipation / Thread、风险和替代选项。它不产生剧情事件，不规定章节编号，不把 Candidate Lens 合并为 Intent。

CSWK 增补后它成为 Universal Serial Scheduler：各 Engine 提供 `EngineIntentRecommendation`，Scheduler 再按 Effective Drive Mix 聚合。Market Category 不在函数输入中；未确认 Drive 的推荐会被忽略。Progression 仍是当前唯一 `DEEP` Engine。

确定性验收：

- Resource Debt → `RESOURCE_CONVERSION`。
- Knowledge Payoff → `MYSTERY_ADVANCE`。
- Team Payoff → `TEAM_GROWTH`。
- Discovery Payoff → `EXPLORATION`。
- 作者 Override 按 book / edition / chapter boundary 持久化并优先返回。
- 即时余波与恢复需求可合法优先于成长服务。
- 一个 Recovery / Aftermath 章节不服务 Core Promise 不是 Hard Error。
- POWER=82、MYSTERY=64、RELATIONSHIP=41 的合成输入按 Drive Priority 得到一个 Primary 与两个 Secondary，并保留来源、Debt、Promise 与风险。

测试：`tests/unit/test_progression_scheduler.py`、`tests/unit/test_custom_progression_ood_benchmark.py`。
