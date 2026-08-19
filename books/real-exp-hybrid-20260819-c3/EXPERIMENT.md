# 《我给怪物装上第二条进化路》Hybrid Multi-Agent 实验记录

## 当前状态

- 状态：`CHAPTERS_1_5_COMPLETE / WAITING_AUTHOR_NEXT_STEP`
- 设计来源：作者批准的 `runs/growth-benefit-hierarchy-v1/revised_design_profile.md`
- 当前 BOOK：已应用批准的成长重平衡设计、重排后的百章/十章计划和第1—5章 State Delta；修正版设计仍属于 Proposal，不改变其 Proposal 身份。
- 旧计划：原有计划材料保留；旧计划在成长重平衡期间标记为 `STALE_PENDING_GROWTH_REBALANCE`，未被覆盖或删除。
- 下一步边界：本实验已停止在第5章；未生成第6章、未来新正文或新的计划。

## 真实子代理链路

第1—5章均按以下独立子代理链路完成：

`Director → Context Curator → Primary Writer → Opening Specialist / Dialogue Specialist / Action Specialist / Emotion Specialist → Revision Integrator → State Delta`

四个专项 Agent 互不读取彼此结果；主代理保存各自返回、统一提供给 Integrator，并执行有限事实审查。第1章另有一次独立 single control，只用于对照，不写入 Canon。

本轮共调用 46 次真实子代理：45 次五章 Hybrid 主链，1 次第1章 single control；无结构重试、自动拒绝、自动重写或自动重跑。

## 关键产物

- BOOK：`BOOK.md`
- Proposal：`PROPOSAL.md`
- 第1—5章：`chapters/chapter-0001.md` 至 `chapters/chapter-0005.md`
- 每章运行记录：`runs/chapter-0001/` 至 `runs/chapter-0005/`
- 第1章对照：`runs/chapter-0001/comparison.md`
- 效率记录：`runs/efficiency.md`
- 成长重平衡记录：`runs/growth-benefit-hierarchy-v1/`

## Canon 边界

- 第1—5章已由主代理按 State Delta 提案更新 BOOK 当前状态区。
- State Delta 未修改 BOOK Contract、成长基因图、百章计划或十章计划。
- 第1章 single control、Primary 中间稿、专项 Patch 和 Integrator 运行说明不是额外 Canon。
- 本记录不宣称旧《断点值守》为 Canon；旧控制实验仍为 `REJECTED CONCEPT / NON-CANONICAL CONTROL`。
