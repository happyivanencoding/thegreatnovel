# Hybrid Multi-Agent 实验效率与运行记录

## 运行范围

- 目标：在作者批准的重平衡设计与当前 BOOK 上，真实串行执行第1—5章 Hybrid Multi-Agent 运行，并保留第1章 single control 对照。
- 每章主链：Director → Context Curator → Primary Writer → Opening / Dialogue / Action / Emotion Specialist（四个专项互不读取彼此结果）→ Revision Integrator → State Delta。
- 第1章额外增加 1 次 single control；single 只保存实验记录，不写入 Canon。
- 未发生结构重试、自动重写、自动拒绝或专项 Agent 重跑；所有缺失/冲突均由主代理按边界处理。

## 调用总数

| 项目 | 次数 |
| --- | ---: |
| 五章 Hybrid 主链 | 45 |
| 第1章 single control | 1 |
| Agent 调用合计 | 46 |
| 结构重试 / 自动重跑 | 0 |

## 各章输入输出规模

| 运行 | Agent 数 | Prompt 字符合计 | Response 字符合计 |
| --- | ---: | ---: | ---: |
| 第1章 | 10 | 94,104 | 20,353 |
| 第2章 | 9 | 89,725 | 12,386 |
| 第3章 | 9 | 104,483 | 14,025 |
| 第4章 | 9 | 104,283 | 15,558 |
| 第5章 | 9 | 123,425 | 18,746 |
| 合计 | 46 | 516,020 | 81,068 |

## 第1—5章逐节点记录

| 运行 | 节点 | Prompt 字符 | Response 字符 | Patch 数 |
| --- | --- | ---: | ---: | ---: |
| 第1章 | Context Curator | 13,585 | 2,106 | 0 |
| 第1章 | Director | 13,425 | 420 | 0 |
| 第1章 | Revision Integrator | 11,029 | 5,516 | 0 |
| 第1章 | Primary Writer | 4,777 | 5,375 | 0 |
| 第1章 | single_control | 15,181 | 4,457 | 0 |
| 第1章 | Action Specialist | 7,181 | 57 | 0 |
| 第1章 | Dialogue Specialist | 7,281 | 484 | 2 |
| 第1章 | Emotion Specialist | 7,032 | 376 | 1 |
| 第1章 | Opening Specialist | 7,319 | 554 | 2 |
| 第1章 | State Delta | 7,294 | 1,008 | 0 |
| 第2章 | Context Curator | 15,776 | 1,767 | 0 |
| 第2章 | Director | 18,953 | 439 | 0 |
| 第2章 | Revision Integrator | 9,095 | 4,026 | 0 |
| 第2章 | Primary Writer | 10,193 | 3,939 | 0 |
| 第2章 | Action Specialist | 7,437 | 457 | 2 |
| 第2章 | Dialogue Specialist | 7,569 | 57 | 0 |
| 第2章 | Emotion Specialist | 7,299 | 345 | 1 |
| 第2章 | Opening Specialist | 7,544 | 57 | 0 |
| 第2章 | State Delta | 5,859 | 1,299 | 0 |
| 第3章 | Context Curator | 16,781 | 2,117 | 0 |
| 第3章 | Director | 23,617 | 413 | 0 |
| 第3章 | Revision Integrator | 10,975 | 4,203 | 0 |
| 第3章 | Primary Writer | 15,162 | 4,245 | 0 |
| 第3章 | Action Specialist | 7,739 | 460 | 2 |
| 第3章 | Dialogue Specialist | 7,793 | 246 | 1 |
| 第3章 | Emotion Specialist | 7,498 | 415 | 2 |
| 第3章 | Opening Specialist | 7,800 | 57 | 0 |
| 第3章 | State Delta | 7,118 | 1,869 | 0 |
| 第4章 | Context Curator | 16,383 | 2,397 | 0 |
| 第4章 | Director | 21,415 | 640 | 0 |
| 第4章 | Revision Integrator | 11,236 | 4,724 | 0 |
| 第4章 | Primary Writer | 13,453 | 4,812 | 0 |
| 第4章 | Action Specialist | 8,793 | 685 | 3 |
| 第4章 | Dialogue Specialist | 8,863 | 261 | 1 |
| 第4章 | Emotion Specialist | 8,482 | 57 | 0 |
| 第4章 | Opening Specialist | 8,733 | 57 | 0 |
| 第4章 | State Delta | 6,925 | 1,925 | 0 |
| 第5章 | Context Curator | 16,750 | 2,088 | 0 |
| 第5章 | Director | 22,572 | 619 | 0 |
| 第5章 | Revision Integrator | 21,342 | 6,147 | 0 |
| 第5章 | Primary Writer | 14,232 | 6,008 | 0 |
| 第5章 | Action Specialist | 10,060 | 393 | 2 |
| 第5章 | Dialogue Specialist | 10,044 | 386 | 2 |
| 第5章 | Emotion Specialist | 9,790 | 508 | 2 |
| 第5章 | Opening Specialist | 9,930 | 242 | 1 |
| 第5章 | State Delta | 8,705 | 2,355 | 0 |

## Single control

- 调用：1 次真实 single Writer 子代理。
- 文件：`runs/chapter-0001/single_control_prompt.md`、`single_control_response.md`、`single_control_formal_prose.md`。
- Prompt 字符数：15,181；Response 字符数：4,457；正式正文字符数：4,087。
- 使用第1章运行前 `f05f1bb^` 的 BOOK/CANON 快照与同一 Director 合同；未更新 BOOK、章节正文或 Canon。

## 成本与失败记录

- Prompt 体量最大的节点集中在 Curator、Primary、Integrator；Integrator 输入包含唯一 Primary Draft 和四条专项结果，因此是主链最重的整合节点。
- Specialist 返回通常很短；它们只提供局部 Patch，不承担全文重写，也没有拒绝权。
- Director、Curator、Primary、四专项、Integrator、State Delta 的提示与返回文件均成对存在；本次记录目录未发现 `tokens truncated` 标记。
- 第3章 State Delta 的原始结果曾含有重复旧状态尾巴，主代理只做了记录级清理后应用；未重跑 State Delta，原始返回仍保留。
- 第5章 Curator 纠正了“第一笔收益已领取”的潜在误读；正式正文只写核心与凭证到手，赏金、食物和路票留给后续巡猎所结算。

## 产物边界

- 第1—5章正文、每章运行 Prompt/Response、事实摘要、Proposed Canon Index 和 Review 均已保存。
- State Delta 只更新 BOOK 的当前状态区；Growth Genome、BOOK Contract、百章计划和十章计划没有被 State Delta 改写。
- 旧百章/十章计划此前已按 `STALE_PENDING_GROWTH_REBALANCE` 保存；本轮使用作者批准的重平衡计划，未覆盖旧计划文件。
