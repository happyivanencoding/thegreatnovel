# 全新玄幻修仙盲测：`real-exp-xianxia-blind-v1`

## 当前状态

- 阶段：`CHAPTERS_1_5_COMPLETE / WAITING_AUTHOR_NEXT_STEP`。
- 书名：`《留火成器》`
- 主角：许砺。
- 选择来源：独立 Blind Concept Selector 选择 Idea 候选二；选择理由保存在 `runs/idea/selection.md`。
- 题材：玄幻修仙；没有预设凡人流、系统流、无敌流、固定境界、固定宗门或固定金手指。
- 章节默认模式：`hybrid_selective`。

## 五章结果

- 第 1—5 章正式正文均已保存；每章 manifest `run_status=completed`、`final_source=integrator`。
- Specialist 选择依次为：第1章 Opening+Action；第2章 Dialogue+Action；第3章 Opening+Action；第4章 Opening+Action；第5章 Dialogue+Action。
- 第 5 章首次真实收益到账：赤栈旧账清零、退役独立炉心到手、临时接单牌到手，并留下下一笔外单入口。
- Blind Reader 与 Runtime Review 分别保存在 `runs/blind-reader-review.md`、`runs/runtime-review.md`；原始独立报告以 `*-agent.md` 保留。
- 单节点恢复演示保存在 `runs/recovery-demo/`，不改正式正文或正式 manifest。
- 当前已知格式缺口：第 4 章模型 State Delta Response 缺少 `# State Delta Audit`；原始响应和 `state_delta_format_error.md` 保留，未自动重跑。当前代码已把该标题列为必需项。

## GBrain 边界

- Idea 查询保存于 `runs/genre-prior/`，接受 2 张 Genre Prior 和 3 张具体书籍蒸馏材料。
- Outline 查询保存于 `runs/outline/gbrain_*`，接受 1 张主题材 Genre Prior 和 4 张具体材料。
- Genre Prior 只服务 Idea/Outline；原卡不进入章节 Prompt、BOOK Contract 或 Canon。

## 章节停止条件

第 1—5 章严格串行。每章依次保存 Director、Curator、Primary、作者选中的 0—2 个 Specialist、有效 Patch 时的 Integrator、正式正文来源和 State Delta v2。State Delta 需要作者批准后才应用；Ledger 不自动写 BOOK 或章节。

五章完成后只生成 Blind Reader Review、Runtime Review、恢复演示和效率记录；不生成第 6 章，不根据盲测正文反向改代码或重写前五章。
