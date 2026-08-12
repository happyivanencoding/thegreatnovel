# Narrative Drive Kernel 验收

## 结论

Chinese Serialized Webnovel Kernel 已作为轻量通用层落在 Progression Engine 之上。它不把中文长篇等同于力量升级小说；同时没有削弱 PWK 已完成的阶段、资源、能力、验证、世界扩张、Debt、Payoff、Scheduler 与 Candidate 深度。

## Market Category 与 Narrative Drive

`MarketCategoryMetadata` 只存主/副市场分类及展示标签，用于书库、检索、推荐和统计。Universal Scheduler 的函数签名不接收 Market Category；`HISTORY` 不会自动推出战争或朝堂，`URBAN` 也不会自动推出财富或职业情节。

`NarrativeDriveContract` 冻结一个 Primary Drive 和最多四个 Secondary Drives，以及 priority、promise、state、payoff mapping、debt mapping、fatigue risk 与 author override。Reader Experience 回答“读者为什么追”，Drive Contract 回答“靠什么长期兑现”，Engine 回答“该领域如何投影、建议与验证”。

## Engine Registry

| Engine | 当前深度 | 权威边界 |
|---|---|---|
| Progression | `DEEP` | 复用 PWK 合同和章节投影 |
| Mystery / Reveal | `NOT_IMPLEMENTED_DEEPLY` | 后续复用 Author Truth / Knowledge / Reveal / Secret Board |
| Career / Mastery | `NOT_IMPLEMENTED_DEEPLY` | 当前仅合同与扩展点 |
| Strategy / State-Building | `NOT_IMPLEMENTED_DEEPLY` | 当前仅合同与扩展点 |
| Competitive Skill | `NOT_IMPLEMENTED_DEEPLY` | 当前仅合同与扩展点 |
| Survival / Resource | `NOT_IMPLEMENTED_DEEPLY` | 当前仅合同与扩展点 |
| Relationship / Life | `NOT_IMPLEMENTED_DEEPLY` | 当前仅合同与扩展点 |
| Team / Faction Growth | `NOT_IMPLEMENTED_DEEPLY` | 当前仅合同与扩展点 |

Registry 不为浅实现生成假的状态页。`ProgressionNarrativeEngineAdapter` 的 `build_state` 直接消费 chapter-pinned `progression_state`，缺失时返回 UNKNOWN；其 Debt/Payoff/Candidate 方法只映射现有结构。

## Universal Scheduler

每个 Engine 输出 `EngineIntentRecommendation`：engine、drive、intent、priority、why-now、debt、reader promise、risk 与 evidence。Scheduler 按已确认 Drive Priority 聚合为一个 Primary 和最多两个 Secondary Intent；作者 Override、Author Task、即时余波与恢复需求仍优先。未列入 Effective Drive Mix 的 Engine 推荐被忽略。

## Candidate、Debt 与 Drift

现有 Candidate 和 Chapter Contract 增加 `narrative_drive_alignment`，但继续保留专用 `progression_impact`。现有 Narrative Debt / Payoff 仅增加 `drive_type`、`engine_type`、`associated_drive` 引用；没有新表、新分数或第二套账本。

`NarrativeDriveDriftDiagnostic` 区分单章软缺席、连续 Primary Miss、Secondary Replacement、长期失衡、明确冲突和 Author Evolution。作者显式更新 Drive Contract 后不再按漂移处理。

## Existing Novel 与 Canon 边界

已有书从 Chapter World State 的能力、资源、关系、势力、地点、规则、Thread/Promise 生成 `INFERRED_PROPOSAL`。新增 Market 与 Narrative Drive 建议仍逐项确认；推断与确认均不增加 Event、Canon Commit 或 Author Truth。没有合同的旧项目继续使用原工作台。

## Corpus Phase

454 本参考只作为 `WebnovelCorpusEntry` 目录来源。当前仅允许标题、规范标题、别名、Market Category、来源、格式、分析和人工审阅状态；Drive、Progression、Payoff、Arc、文风和关系标签必须来自人工确认、Distillation、Source Analysis 或 Proposal。生产代码没有具体书名分支。

## 证据

- 合同与分类：`src/novel_authoring/serial_kernel/models.py`、`classification.py`。
- Engine Protocol / Registry：`serial_kernel/engines.py`。
- Universal Scheduler：`progression/scheduler.py`。
- Drive Drift：`serial_kernel/diagnostics.py`。
- 合成分类：`tests/unit/test_narrative_drive_contracts.py`。
- 聚合与边界：`tests/unit/test_universal_serial_scheduler.py`、`test_narrative_drive_alignment.py`。

## 最终验证

- 全量自动测试：`314 passed`。
- Ruff：通过。
- Mypy：179 个源文件通过。
- Compileall、`original.js`、`workbench.js`、`app.js` 语法检查：通过。
- `novel web doctor`：路由、模板、静态资源和 API health 全部通过，静态资源版本 `3.4.3`。
- 真实浏览器：Original Step 0、Drive Mix、Progression 专用合同、通用 Candidate Drive Alignment、Existing Novel Proposal 和 OOD Derived Adapter 均通过；证据位于 `benchmark/artifacts/progression_kernel_v1/`。
