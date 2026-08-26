我将使用本地 `tgn-system-steward` skill，按其“最早语义坍缩点—最小可归因修复”的方法做只读审计。先读取该 skill 与必要的既有记忆索引，然后严格限定在你列出的 Git、两份文档和四份 artifact；不编辑文件。技能方法已加载；记忆索引只用于确认本仓库的审计边界，没有采用任何旧结论替代当前 artifact。下一步按指定顺序读取 Git 状态/最近提交，再读取这六个当前文件；不会搜索其他实验目录。结论：最早剩余的语义坍缩主要发生在 Outline 编译，不在 World / Power / Human / Character / Story Program。不要重开已经验证的上游 authority。

最小修复只有一刀：

> 将 Outline 编译契约改为“具体 Story Anchors + 相对本块起点的可选 `Block Delta`”；未发生的维度直接省略，不再要求每个 block 都填写核心幻想推进、一级成长、收益、代价、世界扩张等字段。

证据：

- 产品文档已经明确：成长是纵向不变量，不是每阶段或每 block 的填表税；Outline 只编译具体 Story Anchors 和真实变化。[MVP_PRODUCT_DIRECTION.md](C:/dev/tgn-story-mvp/docs/MVP_PRODUCT_DIRECTION.md:179)
- 当前 Story Program 已经允许不发生 Power 增长的完整阶段。阶段 5 的 Delta 只有 Possession、Relationship、Identity、World 等真实变化。[STORY_PROGRAM_CURRENT_PRODUCTION.md](C:/dev/tgn-story-mvp/books/real-exp-private-prototype-upstream-20260826-traditional-v1/STORY_PROGRAM_CURRENT_PRODUCTION.md:124)
- Stage 5 probe 也明确写出“不结算新的 Power / Capability Delta”，但仍有选择、损失、关系和世界后果。[OUTLINE_STAGE5_BLOCK_TAX_PROBE.md](C:/dev/tgn-story-mvp/books/real-exp-private-prototype-upstream-20260826-traditional-v1/OUTLINE_STAGE5_BLOCK_TAX_PROBE.md:17)
- 反而是当前 Outline 仍在每个剧情块重复输出“核心幻想推进、一级成长变化、收益与反哺、世界扩张、代价”等固定栏目，说明编译层仍残留 stage/block tax。[OUTLINE_CURRENT.md](C:/dev/tgn-story-mvp/books/real-exp-private-prototype-upstream-20260826-traditional-v1/OUTLINE_CURRENT.md:241)

应保持冻结：

- World Vision、Power Seed、Human Seed、deterministic Character composition。
- 已批准的 Story Program、成长语法、Core Fantasy 和真实 Stage Delta。
- Human 私有 prototype 仍只是显式、局部、实验性输入，不得成为默认全局 Human prior。[SPLIT_CHARACTER_AUTHORITY.md](C:/dev/tgn-story-mvp/docs/SPLIT_CHARACTER_AUTHORITY.md:221)

最便宜的因果 A/B：

- A：当前 Outline 编译提示。
- B：只增加一条编译约束：`Block Delta` 只写真实变化，所有未变化栏目省略，不为完成表单制造升级、掉宝、权限或地图。
- 固定同一 World、Character、T0、Story Program、模型和参数，比较 Stage 5 的无 Power block，再加一个确实有 Power 变化的 block。
- 直接人工检查：B 是否在 Stage 5 保留冲突、选择、损失和后果，同时在有真实成长的 block 保留能力变化。

这刀不能解决：

- World 是否足够独立；
- Human prototype 本身是否优秀；
- 当前 `STORY_PROGRAM_CURRENT_PRODUCTION` 与 `STORY_PROGRAM_FIRST_PRINCIPLES` 两种开场顺序的作者选择。后者确实不同，但不是上游 authority 已失效的证据；若要采用它，应由作者明确重开 Story Program，再使下游失效。[STORY_PROGRAM_FIRST_PRINCIPLES.md](C:/dev/tgn-story-mvp/books/real-exp-private-prototype-upstream-20260826-traditional-v1/STORY_PROGRAM_FIRST_PRINCIPLES.md:80)

因此当前不应新增 Agent、Reviewer、Scorer 或 Hard Gate，也不应重开上游；先把 Outline 编译从“固定栏目生成器”收缩成“事实锚点 + 可选 Block Delta”。
