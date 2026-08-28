## 最终裁决

TGN production 应采用 **Z：Split Human Architecture**：

> **独立 World Expansion → 独立 Human Development → 确定性 Current Character → Story Refresh Re-Collision**

不采用单 Agent 全包，也不采用省略 Human Development 的 Y。冻结的是这套权力拓扑，不是 Z 某个具体阶段的契约主题或剧情结构。

### 实验证据

| 方案 | 实际架构 | 玄幻 Ch120 | 多世界 Ch80 |
|---|---|---:|---:|
| X | 单 Agent 同时扩世界、改人物、规划阶段 | 第 2 | 第 3 |
| Y | 独立 World，不设 Human Development | 第 3 | 第 1 |
| Z | 独立 World + 独立 Human Development | 第 1 | 第 2 |

两个 Case 的冠军具体内容不同，但冠军都来自独立 World 架构；X 从未获胜。映射可由实验的 [mono prompt](/C:/dev/tgn-story-mvp/books/real-exp-progressive-authority-20260828-v1/xuanhuan_ch120/mono_prompt.md:1)、[split no-human prompt](/C:/dev/tgn-story-mvp/books/real-exp-progressive-authority-20260828-v1/xuanhuan_ch120/split_no_human_prompt.md:1) 和 [split-human prompt](/C:/dev/tgn-story-mvp/books/real-exp-progressive-authority-20260828-v1/xuanhuan_ch120/split_human_prompt.md:1) 确认。

### 独立 World Agent：值得，而且必须

这是本轮证据最明确的结论。

单 Agent X 的 Prompt 明确允许“新的世界、机会、能力、人物关系与主角路线互相协调”。这恰好是错误源：Agent 一旦同时知道人物能力、人格缺口和下一阶段任务，就会自然制造钥匙、岗位、课程和结算闭环。

所以 X 虽然经常最完整、最自洽，却会稳定牺牲三样东西：

- 世界先于主角存在的感觉；
- 旁人真正不配合、误判或损害主角利益的可能；
- 连规划者自己也没有预先消解的碰撞。

这不是再加一句“保持惊喜”能修好的 Prompt 问题，而是信息可见性造成的因果泄漏。World Expansion 必须看不到 Current Character、Power Stack、Human 和未来 Story Program。

### 独立 Human Development Agent：值得，也应进入 production

两次 Human Agent 都正确输出了 `NONE`，见 [玄幻结果](/C:/dev/tgn-story-mvp/books/real-exp-progressive-authority-20260828-v1/xuanhuan_ch120/human.md:1) 与 [多世界结果](/C:/dev/tgn-story-mvp/books/real-exp-progressive-authority-20260828-v1/multiworld_ch80/human.md:1)。因此，Y/Z 的具体名次差不能被解释成 Human Agent 带来的质量增益——本轮对此没有因果识别。

但 production 仍然必须保留它。否则五百章长篇只剩两个坏选择：

- Human Origin 永久冻结，人物活了几百章却没有稳定发展；
- 让 Story Refresh 一边看到新世界，一边解释人物“现在变成了谁”，最终把人物发展改造成适配下一阶段的正确答案。

独立 Human Development Agent 解决的是一个真实且唯一的失败：**正文已经反复证明人物形成了新的稳定选择偏向，但未来规划仍只拿开书 Human Core 判断他。**一旦发现，下一步确实会不同——批准一个 forward-only Delta，更新未来人物权威。

它不是人物弧设计师，只是证据裁决者：

- 只读 Frozen Human Core 与已发生 Canon；
- 看不到未来世界、奖励和计划；
- 默认输出 `NONE`；
- 只记录高代价、跨情境、已经稳定成立的偏向变化；
- 输出仍须作者批准。

这种 Agent 不会削弱 Surprise；它阻止未来规划者为了自洽而改造人物。

### Production 冻结流程

1. **World Expansion Agent**
   - 只在真正进入新 World Horizon 时调用，不按固定章数交税。
   - 主角盲、能力盲、未来计划盲。
   - 输出 forward-only World Authority。

2. **Human Development Agent**
   - 同一刷新边界独立运行。
   - 只审已经发生的人物变化。
   - 可以并且多数时候应该输出 `NONE`。

3. **Deterministic Current Character Compiler**
   - 合并 Frozen Power/Human Origins、Canon 获得、关系、身份、知识以及批准的 Human Delta。
   - 不再增加一个 LLM Composer。

4. **Story Refresh Agent**
   - 第一次同时看到 Effective World 与 Current Character。
   - 职责只有：`Independent World × Current Character → Fresh Collision`。
   - 可以产生错失、偏航、部分胜利和新发动机，不得回写前两项权威。

5. **作者批准 → Outline**
   - Outline 只编译当前窗口。
   - 不再增加碰撞 Reviewer、Scorer、总协调 Agent 或 Hard Gate。

当前未提交实现已经准确表达了这条路线：[周期性分权 Prompt](/C:/dev/tgn-story-mvp/src/story_mvp/character_prompts.py:195) 与 [确定性 forward compiler](/C:/dev/tgn-story-mvp/src/story_mvp/long_form_evolution.py:1)。

最终 production 决定是：**上线 Z / `split_human`；淘汰 mono；不把 `split_no_human` 保留为 fallback。**单 Agent 全包确实用自洽换掉了惊喜，而真正的修复是权力隔离，不是再加审查条款。

<oai-mem-citation>
<citation_entries>
MEMORY.md:400-400|note=[用于坚持独立世界人物碰撞不得被解释成命定适配]
MEMORY.md:413-415|note=[用于判断阶段发动机应轮换且成长不是阶段字段税]
MEMORY.md:426-427|note=[用于识别过度闭合和能力奖励流水线的根因]
</citation_entries>
<rollout_ids>
01a03d1e-9911-7c51-a5e7-7ae26d56d034
01a03d65-9cae-7682-9685-bdaa2b584662
</rollout_ids>
</oai-mem-citation>
