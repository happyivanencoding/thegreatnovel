# Progression Webnovel Kernel V1 Benchmark

本目录只保存原创 seed、确定性合同输出与人工审阅摘要，不包含任何已有小说正文。

## 覆盖矩阵

| 组别 | Seed | 预期结构 |
|---|---|---|
| Built-in A | 被废修为，以万物残留火种重建成长 | `CULTIVATION_ESCALATION` |
| Built-in B | 七名失败者寻找第二能力槽 | `ABILITY_UNLOCK_TEAM` / 多主体多轴 |
| Built-in C | 吸收死亡恒星能量并听见活星呼吸 | `COSMIC_PROGRESSION` |
| Built-in D | 城市职业的禁忌晋升路线 | `OCCULT_SEQUENCE_MYSTERY` |
| OOD A | 失去的未来成为力量 | Branching + Sacrifice + Lock-out |
| OOD B | 城市共同解决问题后获得自然法则 | Settlement + Network |
| OOD C | 理解灭亡语言进入文明现实层 | Knowledge + Mystery + World Expansion |

## 可重复证据

- `tests/unit/test_progression_family_benchmark.py`：验证四个成熟家族通过同一个 `ProgressionContract` Runtime shape，同时保持轴、拓扑和资源语法差异。
- `tests/unit/test_custom_progression_ood_benchmark.py`：验证三个 OOD seed 都生成 `DerivedAdapterSpec`、合法合同、非传统 Payoff 与可解释 Scheduler Intent。
- `tests/integration/test_story_world_workbench_v2_2.py`：验证历史章投影、导入小说建议合同、逐项确认和 Canon 零变化。

## 人工审阅约束

1. 不把“出现题材名”当作 Genre Promise 对齐。
2. Remove-the-skin 检查成长门槛、资源、能力、世界入口是否真实改变因果。
3. Foundation Diversity 必须检查故事发动机、成长来源、资源经济、世界入口、冲突结构与人物动力，而不是只比较名词。
4. 当前 CI 不运行昂贵语义生成；真实 Foundation 文本仍需要 Local File Handoff 后人工审阅。
