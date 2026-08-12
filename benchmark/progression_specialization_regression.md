# Progression 专长回归

## 目标

通用 Narrative Drive 层不能把近未来体修重新稀释为制度听证、基础设施管理或社会政策讨论，也不能降低玄幻、仙侠、高武、科幻玄幻、末世进化与神秘学晋升的生产能力。

## 近未来体修

Seed：“近未来的气修修仙小说，体修成神的故事。”

- Market Category：仙侠 / 科幻。
- Primary Drive：POWER_PROGRESSION。
- Secondary：WORLD_EXPLORATION、RESOURCE_OPPORTUNITY、TERRITORY_FACTION。
- Reader：成长/突破/资源/世界扩张为高优先；社会议题为低优先。
- Genre：近未来是 Setting Skin；身体蜕变、资源门槛、能力验证与更大世界改变因果。
- Progression：`BODY_EVOLUTION`，`TRANSFORMATIVE + ACCUMULATIVE`，保留代价、门槛与验证。
- Scheduler：Progression Engine 的结构信号可成为 Primary Intent；Market Category 不参与打分。

结果没有回退到制度或基础设施主导。若候选连续多章只推进社会议题，Drive Drift 会产生 `SECONDARY_REPLACEMENT` 或 `PRIMARY_DRIVE_DRIFT`；若作者显式修改 Drive Contract，则标记 `AUTHOR_EVOLUTION` 而不是漂移。

## Progression 专用问答仍可回答

chapter-aware Progression State 继续给出当前轴/阶段、下一阶段可见性、缺少资源、能力来源、待验证能力、突破准备度、成长代价、世界扩张阶梯、机会面、期待表面与成长债务。Universal Kernel 不复制也不裁剪这些字段。

## 非成长保护

职业、历史治理、电竞和灵异 Seed 的编译结果 `progression=None`。Genre Contract 仍存在，但 capabilities 不伪装 progression axis；Wizard 明确显示“不强制力量体系”。只有 Drive Mix 包含 Power、Knowledge、Ability、Body、Sequence 或 Status Progression 时才创建完整 Progression Contract。

## 自动证据

- `test_near_future_body_progression_specialization_is_preserved`
- `test_four_built_in_families_compile_through_one_runtime_contract`
- `test_ood_grammar_compiles_and_runs_without_builtin_adapter_identity`
- `test_non_progression_reader_contract_does_not_compile_power_system`
- `test_synthetic_seeds_classify_drive_mix_without_forcing_progression`

## 浏览器证据

- `01-reader-experience-step.png`：Step 0 同时显示阅读体验、主/辅驱动力和成长核心开关。
- `02-reader-experience-adjusted.png`：近未来体修仍以体修成长为主，不出现制度听证主导。
- `10-candidate-progression-impact.png`：Candidate 同时展示专用 `progression_impact` 与通用 Drive Alignment。
- `13-occult-progression-contract.png`：神秘成长以禁忌知识、身份保存和职业权限组成非传统战力成长。
- `16-derived-custom-adapter.png`、`17-custom-progression-ood.png`：OOD 成长语法进入 Derived Adapter，不回退到具体作品或预置模板。

上述截图均位于 `benchmark/artifacts/progression_kernel_v1/`。
