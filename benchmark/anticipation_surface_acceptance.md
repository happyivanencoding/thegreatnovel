# Anticipation Surface 验收

Anticipation Surface 聚合现有 Narrative Debt、Opportunity、Reveal Agenda、Active Thread、World Expansion 与 Payoff Readiness。它只回答“读者当前可能最期待什么”，不创建 Promise、Truth、章节事实或 Canon。

示例：

| 来源 | 期待 | 调度用途 |
|---|---|---|
| POWER_SHOWCASE Debt | 新能力第一次真实改变解决方法 | Power Verification，可由救援、探索、谈判等非战斗事件偿还 |
| Resource Opportunity | 已铺垫资源何时被获得或转化 | Resource Opportunity / Conversion |
| Reveal Agenda | 前期遗迹或导师秘密何时给出线索 | Mystery Advance / Payoff |
| World Expansion | 下一次成长会打开什么空间 | World Expansion |

所有 item 保留 source、maturity、urgency、payoff channel、horizon、last served、delay risk 与 status。测试：`tests/unit/test_anticipation_surface.py`、`tests/unit/test_progression_debt.py`。
