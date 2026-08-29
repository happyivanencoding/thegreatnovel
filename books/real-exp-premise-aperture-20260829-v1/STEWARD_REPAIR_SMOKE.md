我将按当前安装的 `tgn-system-steward` Skill 做只读审计。先读取该 Skill 的完整操作规范；随后严格限定在你列出的六类项目材料内，核验 V5 实际失败、保护字段与下游门禁，不编辑任何文件。Skill 已读取。它对本题的关键规则是：独立 Compiler 只审可满足性；FAIL 默认精确回传作者并停止；研究性 Repair 也必须逐字保护标题、货架句、literal Ontology、Changed Verbs 与不可磨平项，缺一项不得进入复检或下游。现在我做一次限定关键词的历史记忆检索，并开始读取指定实验材料。当前材料已确认一个关键事实：V5 不是“Compiler 复检后又判 FAIL”，而是更早被确定性 protected-core validator 拦截，随后 `compiler_calls=0`、downstream 未授权。因此我会继续逐字比对原选定 S2 与修复稿，确认缺失字段及修复是否越界，而不把 Prompt 的预期当成结果。原稿与修复稿的逐字阅读显示：原稿在第 173 行有完整的 `主角反复会做的新动作` 字段；修复稿从正文结构中确实没有该字段。修复稿虽补了真实门、过门条件、五名见证者及 1→9 的逐级结构，却同时扩写了 World 尺、Origin、Power 边界、Trace、开篇画面和 20 章路线，符合报告所说的“大范围重构”。我只再做一次针对该字段的存在性核验，避免把视觉阅读误当成验证结果。结论：应停止，并把精确冲突返回作者。不能自动修复、静默补字段，也不能自动换候选。作者可以手动拒绝 S2 或选择另一张候选，但那是新的作者选择，必须重新过独立 Compiler。

### 实际 V5 结果

V5 不是“Compiler 复检后失败”，而是在复检前就失败：

- protected-core validator：`passed=false`
- 缺失字段：`主角反复会做的新动作`
- `compiler_calls=0`
- `compiler_verdict=SKIPPED`
- `downstream_authorized=false`

证据见 [PROTECTED_CORE_VALIDATION.json:1-4](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/PROTECTED_CORE_VALIDATION.json:1) 和 [RUN_SUMMARY.json:1-10](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/RUN_SUMMARY.json:1)。

原选定稿确实有这个字段及其六项动作；修复稿没有该标题字段。见 [ORIGINAL_SELECTED_S2.md:173-180](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/ORIGINAL_SELECTED_S2.md:173)；实际核验也只在原稿找到该字段。

### V4 应返回作者的精确冲突

独立 Compiler 发现的不是“太怪”，而是具体因果未闭合：

1. 棚屋没有真实、完整地穿过门槛。
2. 原稿所称的“后墙门”并不存在。
3. 五名清醒见证者没有被真实建立。
4. 吞入界壳核心不能自动推出城壳尺 9，缺少逐级结构映射。

这些冲突见 [RESULTS.md:219-223](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/RESULTS.md:219)；V5 确实补写了这些因果，但同时漏掉了受保护动作字段，并把定点修复扩成大范围重构，见 [RESULTS.md:225-229](C:/dev/tgn-story-mvp/books/real-exp-premise-aperture-20260829-v1/RESULTS.md:225)。

### 三类判断

**Stable Principle**

- Independent Compiler 只检查可满足性，不判断商业强度，不替作者选择。
- Compiler FAIL 后默认 fail-loud，把精确冲突交给作者。
- 作者选择是创意门；不能由模型自动选保守候选。
- 保护字段必须由修复输出本身满足，不能事后从旧稿复制回来。

**Current Default**

- Production 开书链保持不变。
- Premise Aperture 即使启用，也只能是开书期、可跳过的入口，不进入章节 Runtime。
- V4 Compiler 应在昂贵 Authority 链之前运行；V5 在 protected-core 未通过时，Compiler 复检和 downstream 都不应运行。本次 `SKIPPED / unauthorized` 正是正确的短路结果。

**Experimental Candidate**

- Single-Agent 完整 Premise Forge：可保留为可选实验。
- Independent Premise Compiler：可保留为窄开书检查。
- Selected Premise 自动 Repair：本次真实测试 FAIL，只能 `RESEARCH_ONLY`。
- 具体 Prompt、模型、字数与 Repair 细节仍未冻结。

### 为什么这不否定 Forge 或 Compiler

Forge 的任务是生成有货架电压的大胆候选，不保证自身因果正确；S2 仍然保持“一间活房子吞入建筑”的核心异常和重复新动作。

独立 Compiler 反而完成了它的职责：在 World/Power/Human/Story 链启动前识别假桥梁。失败发生在后续 Repair 的保护字段保真，而不是 Forge 没生成大胆前提，也不是 Compiler 错误地惩罚了大胆性。

### Freeze 建议

现在冻结 F1—F5 的架构边界，但不要接成所有新书的不可跳过默认：

- 不自动 Selector。
- 不自动 Repair Loop。
- 不静默补回 protected fields。
- 不新增 per-chapter agent。
- V5 Repair 保持 research-only。
- 至少再完成两个题材的 `Compiler PASS → real downstream PASS`，再评估是否默认启用。

残余风险是：当前尚未证明自动 Repair 在其他题材可靠，也尚未证明同一 Changed Verb 经过百章仍能持续产生新玩法；而 production 暂不接入意味着原有的 premise 搜索缺口仍然存在。

未编辑任何文件。
