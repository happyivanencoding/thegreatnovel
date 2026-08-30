# Progressive Canonization｜Two-Cycle E2E Final Results

状态：**PASS / FROZEN / PRODUCTION**
日期：2026-08-30

## 结论

TGN 可以正式支持一种此前没有合法表达的长篇创作状态：**作者自己暂时也不知道长期 Mystery 的答案**。

系统不再把“作者未知”视为设定缺失，也不按章数、伏笔年龄或大纲完整度催作者补终极答案。只有当**作者批准的下一段具体故事事件已经无法在不决定某一小层答案的情况下成立**时，才触发一次低频 Progressive Canonization：

`AUTHOR OPEN → Decision Surface → DEFER / DECISION NEEDED → Reframe R1/R2/R3/D0 → 作者选择 → Independent Compiler → AUTHOR FIXED HIDDEN → Story/World Planning → reader-facing Reveal Event → State/Canon → 更深 AUTHOR OPEN`

这轮两次完整循环均成功，且最终再次回到 `DEFER`。

## 预注册与真实结果

| Checkpoint | 预期 | 真实结果 |
|---|---|---|
| 正确 Chapter 1 后 | DEFER | **DEFER** |
| 作者明确要求第3章真实跨过异常入口 | DECISION NEEDED | **DECISION NEEDED** |
| Cycle 1 候选 | 固定 R2 | **R2，无换候选** |
| Cycle 1 Compiler V2 | PASS | **PASS** |
| Human A/B | 保留不同选择 | **PASS** |
| Chapter 2 pre-reveal | 无 Hidden Truth 泄漏 | **PASS** |
| Chapter 3 Reveal 1 | 事件兑现且不越界 | **PASS** |
| 作者要求第4章做双向同物争夺 | DECISION NEEDED | **DECISION NEEDED** |
| Cycle 2 候选 | 固定 R3 | **R3，无换候选** |
| Cycle 2 Compiler V2 | PASS | **PASS** |
| Chapter 4 Reveal 2 | 事件兑现且不越界 | **PASS** |
| 两次 Reveal 后 | DEFER | **DEFER** |

完整结构化结果见 `EXTENSION_RUN_SUMMARY.json`。

## 第一轮定真

作者下一步明确想看：第3章主角必须亲自穿过异常入口，在另一侧真实行动；不能用梦境、黑暗空间或“看一眼”规避。

系统因此只要求决定：**另一侧最低属于什么可进入、可持续行动的现实类别？**

预注册 R2：另一侧是同一现实中的异常实体夹层，会对进入者与携入物产生持续现实影响。

仍未知：夹层来源、物件生成/经过/转移方式、影响可逆性、两枚钥牌关系、哥哥是否进入、回影井为何吐物。

Reader Reveal 没有告诉读者“异常实体夹层”。第3章只让主角进去追回短刀，回来后伤口血线和刀面水痕仍逆向流动。独立审计：

- Raw Hidden Truth Exposed：NO
- Allowed Reveal Realized：YES
- Still-Open Boundary Preserved：YES

State 随后把“活人可进入并返回 + 携入物可带回持续物理异常”写成普通 Canon。

## 第二轮定真

第一次 Reveal 后，同一个 Mystery 自动重新成为更深 `AUTHOR OPEN`。

作者下一步明确想看：第4章要利用两处现实之间的关系做一次双向同物争夺。

系统只要求决定：**两处现实最低是什么关系，才能让同一物件被两侧同时作用？**

预注册 R3：特定物件可以短暂处于两处现实之间的同一“叠位”；两侧接触的是同一个实体，而非复制品。

Reader Reveal 仍没有使用“叠位”这一后台词。第4章只写：主角始终握着黑柄短刀，另一侧铁钩敲中刀背，同一个缺口当场出现在他手中的刀上。

独立审计再次 PASS；石道来源、两侧本体关系、适用范围、触发/解除条件、钥牌来源、哥哥等继续未知。

最终 Decision Surface 再次返回 **DEFER**：后续可以先写兵坊争夺、收益/家人风险和物证后果，不需要继续解释终极来源。

## Character Authority Invariance

同一 World + 同一 Fixed Point 下：

- Human A：钱、占有、好胜优先；拒绝安全高价退出，保留钥牌与入口的独占/溢价可能。
- Human B：妹妹安全优先；先拿较低定金把妹妹移出旧井区，主动放弃第一轮最高报价和市场先手，再回来争入口。

独立审计：**PASS / Meaningful Divergence = YES**。

因此 Mystery 机制没有把不同人物压成同一种“理性调查员”。

## 三个真实失败与修正

### 1. INVALID：实验 helper 串章

早期 `extract_chapter_plan()` 把 Future-10 多章一起吞入，导致所谓 Chapter 1 实际执行后续事件。相关旧 `chapter1/` 与依赖它的 Decision1 全部标记 INVALID，保留 provenance，不计成绩。修正后确定性验证第1章只返回第1章。

### 2. Compiler V1 语义悖论

旧 Compiler 把 AUTHOR OPEN 的 `Still Open` 当成“永远不可回答”，同时看不到触发本次定真的作者 Future Direction，于是产生悖论：Decision Surface 说“现在必须决定 X”，Compiler 却因为 X 以前未知而拒绝任何答案。

V2 冻结语义：

- 旧 AUTHOR OPEN / Still Open = 决策前未知池；
- Decision Surface 的 `Smallest Decision` = 当前唯一获准定真的一层；
- 候选自己的 `What Remains Unknown` = 采用后的新保护边界；
- Author-Approved Future Direction 可以授权未来事件，不等于倒写成过去 Canon。

同一个预注册 R2 在 V2 strict PASS，没有重抽候选。

### 3. INVALID：Outline 重复审批 self-gate

模型把 `CURRENT CHARACTER｜Forward Authority` 误解成新的待批准 Character，主动请求二次作者批准。production 代码本来已完成批准门禁。

修正只是把既有事实说清：**Character Authority 已批准；CURRENT_CHARACTER 是 deterministic forward snapshot，不产生第二次批准点。** V2 正常生成 Outline。

## Production 冻结边界

正式 production 只冻结以下机制，不冻结实验样本或 Prompt 字数：

1. `AUTHOR OPEN` 与 `AUTHOR FIXED HIDDEN` 是合法、不同的作者状态。
2. Decision trigger 由**作者批准的下一具体故事需求**触发，不由章节数/谜团年龄触发；能继续不知道就 `DEFER`。
3. Reframe 只在 `DECISION NEEDED` 后给 R1/R2/R3/D0；作者是唯一选择门。
4. Compiler V2 只检查局部定真与旧 Canon / 新 Still-Open 边界；不评分、不改稿、不自动选候选。
5. Hidden Fixed Point 存在 runtime-blind `MYSTERY_CONTROL.json`；不进入 BOOK、AUTHOR NOTES、普通 Outline 或 Reveal 前章节。
6. Story / World planning 可以读取对应 route 的 planning-only Hidden Truth。
7. Story Refresh 在需要时把 Reveal Boundary 编译为 reader-facing `MYSTERY REVEAL CONTRACT`；保存 Story Program 时 Contract 被确定性剥离并单独保存。
8. Outline 只得到 `第N章 + [MYSTERY-REVEAL:ID]` 的无答案调度标记。
9. 只有 Reveal 章 runtime 才确定性获得 Event Atom / State Residue / Still Open；raw Fixed Point 不进入 Writer。
10. Reveal 发生并经 State 成为 Canon 后，显式 advance 把该 Mystery 重新打开为更深 AUTHOR OPEN。
11. 不新增每章 Mystery Agent / Reviewer / Gate；不自动 Repair；不自动生成终极答案。

Production 接线另外补了一条采用安全边界：Mystery Compiler Prompt 生成时保存当前 Thread、selected candidate、Decision Surface、author planning need 与当前 BOOK/Canon 的**精确原文 snapshot**；`adopt` 只接受同一 snapshot 下的 strict `PASS`。候选、Thread 或 BOOK/Canon 任一变化，旧报告自动 stale，必须重新编译。这里直接比较文本，不增加 hash/checksum；普通 PUT 也不能直接创建 `FIXED_HIDDEN` 绕过 Compiler + adopt。

最终 production validation：Progressive Canon 专项 **31/31 PASS**；全仓 **440/440 PASS**；Steward **0.3.28** lint/package/install/activate/bounded smoke 全部 PASS。机器可读记录见 `production-freeze-validation/PRODUCTION_VALIDATION.json` 与 `SKILL_INSTALL_VALIDATION.json`。

## What This Did Not Solve

- 不保证某个 Mystery 最终一定需要终极答案；作者可以长期继续 `DEFER`。
- 不自动判断作者应该选择 R1/R2/R3 中哪一个。
- 不自动 Repair Compiler FAIL；冲突交还作者。
- 不把所有悬念升级为 Progressive Canonization；普通 Open Promise 仍走现有 State / Story 路径。
- 本轮冻结的是 backend / authority / runtime 方法；专门的可视化 Mystery 面板不是本轮必要条件。

## 真实调用成本

见 `USAGE_SUMMARY.json`。

有效 Extension 路径（排除 INVALID Outline1 与 Compiler V1）：

- 32 次真实 ACP
- Luna 20 / Terra 9 / Sol 3
- total tokens：1,778,806
- 累计调用 wall：3,635.855 秒

这是研究验证成本。Production 不增加每章 LLM 调用；Decision / Reframe / Compiler 只在作者关键定真点低频运行，Reveal 合同复用现有 Story Refresh，章节侧仅做 deterministic transport。

## 最终判定

> **PASS：冻结 Progressive Canonization 核心机制，并接入 production。**
>
> 核心原则：**Mystery can be a question before it is an answer. Canonize only the smallest answer the next story has actually earned.**
