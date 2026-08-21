# Parallel 3-Chapter Execution Stress Test v1

## 实验性质

本目录是 Candidate A《偷走明天的人》与 Candidate C《吞界行舟》的冻结正文 execution 压力测试。只新增实验产物，不修改生产代码、Prompt、既有书、GBrain 或其它候选实验；Candidate B《掌中天工》完全不读取。

本轮测试两个跨类型风险：

- A：高概念“未来成果先拿走”能否在正文中保持直观、具体和有占便宜感。
- C：世界/领地/人口型资产进入正文后，能否仍以主角个人成长冒险为爽感中心，而不是治理模拟器。

## 生成边界

- A 直接使用 `real-exp-dynamic-pacing-v1/candidate-a/treatment_outline.md` 的冻结 Dynamic Outline。
- C 使用 `real-exp-compounding-narrative-downstream-v1/candidate-c/` 的冻结 Fantasy Seed、World Vision、Story Program；当前 checkout 没有 C 的 Frozen V2 Dynamic Outline，因此只补生成一次当前生产 Outline，随后冻结，不优化、不重生成。
- 两本各只生成 Chapter 1—3；不生成 Chapter 4。
- A/C 两条链彼此隔离；每本内部严格 `Director → Chapter Prep → Writer → experiment-local State Delta/Canon update` 顺序。
- GBrain OFF、Reference Programs OFF；生成节点不可见本实验诊断与 Reviewer 标准；Reviewer 只在结果冻结后读取规定范围。
- 每次 Director、Chapter Prep、Writer 和 State Delta 调用前先落盘完整 Prompt，再保存完整 response；除基础设施失败外不重试内容调用。

## 正史边界

`candidate-a/BOOK.md` 与 `candidate-c/BOOK.md` 是本实验的本地状态副本。State Delta 只更新这些副本和本目录的证据，不写入当前正式书籍或生产 Canon；本轮没有作者对正式 Canon 的批准动作。

## 评审边界

Reader Review、World Engine Review、Execution Fidelity Review 与 Cross-Candidate Review 均为后验诊断。它们不参与生成、不修改正文、不修改 Prompt、不添加角色卡、World Engine 或 prose checker。

## 执行结果

- A/C 各完成 Chapter 1—3，共六章；没有生成 Chapter 4。
- A：Reader=`A_PROMISING_BUT_TOO_ABSTRACT`；World Engine=`EARLY_WORLD_ENGINE_HEALTHY`；Execution=`EXECUTION_PIPELINE_MIXED`；最近失败层=`Chapter-03 Writer / formal_prose.md`。
- C：Reader=`C_PROMISING_BUT_GOVERNANCE_THIN`；World Engine=`EARLY_WORLD_ENGINE_HEALTHY`；Execution=`EXECUTION_PIPELINE_HEALTHY`；最近失败层=`NONE_OBSERVED`。
- 两本都显示 Director 主要是高保真展开器，但没有证据证明这本身造成质量回归；两本 `PREP_OVERLOAD=NO`。
- 跨类型共同纹理是规律化 AI 文风、局部 NPC 功能化、先诊断再行动和正文 recap；没有足够证据重新打开任何 Frozen 生产层。
- Candidate C 的 Outline 只生成一次并冻结，窗口终点 `N=30`；A 使用已冻结 `N=60` Dynamic Outline。
- 当前生产字段硬门曾暴露一个真实接口形状问题：Prep Prompt 把标签和值分行展示，而 `validate_current_outline` 只接受同一行。原始 response 保留，实验目录生成无损 `chapter_prep_for_writer.md` 投影；生产代码/Prompt 未改。
- 状态：`COMPLETE / STOPPED_AT_CHAPTER_3`。

## 交付结构

每本的 `chapter-01/`—`chapter-03/` 保存对应 Prompt、response、正文、事实摘要、State Delta 和状态快照；`reviews/` 保存该候选评审；根目录 `reviews/` 保存横向结论与 `comparison-ready-summary.md`。
