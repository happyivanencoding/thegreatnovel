# FINAL REPORT：Curator → Primary 长篇连续稳定性测试

实验对象：`《炉藏万象》`，Chapter 4—10。最终 verdict：

`CURATOR_PRIMARY_LONGFORM_SUPPORTED_WITH_SELECTIVE_REPAIR`

## Git

- branch = `principal_dev_new_sys`
- BASE_SHA = `5ecda7d48354dca629bc184c2eb60d4cdbb5022c`
- FINAL_SHA = `36bf66c5fcda7df681b94153b597137f495b032d`（包含全部实验产物的 artifact commit）
- pushed = yes；已推送至 `origin/principal_dev_new_sys`
- report metadata follow-up = 本次仅更新 Git 字段的报告提交；最终 HEAD 以 handoff 中的 `git rev-parse HEAD` 为准
- no new branch = yes
- production backend / frontend / Prompt diff = no（除实验目录外）

## Freeze

- production backend modified = no
- frontend modified = no
- Prompt modified = no
- 前端 tests / UX/UI files modified = no
- 生产默认 writer mode、RunRequest、UI default、Run Ledger nodes 未修改

## Execution

- Chapter 4—10 complete = yes
- Chapter 11 not generated = yes；chapters/runs 目录均只到 `chapter-0010`
- 每章实际节点：Director → Chapter Prep → Curator → Primary adopted → State Delta
- Chapter 4—10：每章 5 calls，共 35 content calls
- Specialists：Opening / Dialogue / Action / Emotion 全部 skipped
- Integrator：全部 skipped
- Primary-Fallback：只做 deterministic render，0 model calls
- actual token：全部 `UNKNOWN`
- final source：Chapter 4—10 全部 `primary`

## Opening Contract

Chapter 4—10 的 Director、Chapter Prep、Curator、Primary 实际 prompt 均不含 `Opening Three Chapter Contract`：yes。Chapter 4 的四份 prompt 已在 PRE_FLIGHT 中逐一记录；后续章节也逐章 exact-match 检查为 0。

## Long-form findings

- Growth compounding：成立。裂路器、火鳞器、未完成炉心、炉工/矿工、旧矿图和三炉退路持续进入下一章；Chapter 10 落地固定炉腹＋移动炉匣的第一次生产循环。
- Character stability：成立但主角内在长期欲望仍偏隐性；沈燧的风险偏好、资源态度、克制与修正稳定可见。
- NPC autonomy：成立。阮青禾、炉工、矿工/居民和裴照川都做出不能由沈燧单独替代的判断；炉工个体差异仍弱。
- Ability repetition：局部重复，不是系统停滞。Ch4—6、Ch9 的“旧裂—剥离—接火”动作语法带来疲劳，Reader A 建议 ACTION 局部 repair。
- Event Budget：Ch4—9 `ON_BUDGET`，Ch10 `ADAPTED_BUT_VALID`；没有多章 `UNDER_COMPLETED` / `OVER_COMPLETED`。
- Future10 alignment：Ch4—9 `ALIGNED`，Ch10 `ADAPTED`，无 `DRIFTED`。
- Canon stability：总体稳定。伤势、器物边界、炉心承托、关系和已兑现 promise 持续更新；Ch9/10 门状态和 Ch10 残图/战旗归属是局部可见性疑点。
- Context growth：显著增长。总 prompt 84,723→224,242 chars；主要来自 previous prose、BOOK/Canon、计划和当前上下文。Curator 对 Primary 仍有压缩价值，但没有优化。
- Curator compression：Primary/Fallback prompt 观测比率 Ch4—10 为 0.99、0.78、0.80、0.82、0.85、0.86、0.87；没有调用 fallback 模型。
- Repair opportunity frequency：不是章章需要；主要是 Ch4—6 ACTION、Ch7 DIALOGUE（低优先级）、Ch9 EMOTION/AFTERMATH（低优先级）、Ch10 OPENING/ENTRY + ACTION，Ch8 NONE。

## Readers

- Commercial Reader：追读欲持续，核心幻想从个人开路扩大为多人炉路、移动炉场；Ch4—6 与 Ch9 有动作重复疲劳；Chapter 10 行动空间明显大于 Chapter 3；局部 repair 以 ACTION 和轻微 EMOTION/AFTERMATH 为主。详见 `reviews/commercial-reader.md`。
- Continuity Reader：Ch4—9 Future10 `ALIGNED`，Ch10 `ADAPTED`；因果、资产和伤势连续；高置信疑点是 Ch9 已开总门与 Ch10 再开残余封锁的状态语义，另有第 1 章十三名矿工后续清点粒度下降。详见 `reviews/continuity-reader.md`。

## Verdict rationale

核心链已完成一次真正的 7 章连续运行，35 个有效 content calls 全部完成，且没有系统性人物工具化、成长停止、Future10 漂移或 Canon 丢失。因此不是 `CURATOR_PRIMARY_LONGFORM_UNSTABLE`，也不是 `CANON_CONTEXT_SYSTEM_UNSTABLE`。

同时，两个独立 Reader 都指出少数局部缺口：重复的器物动作语法、兑现后的情绪余波偏短，以及第 9/10 章门状态入口需要澄清。这些与 `SPECIALIST_INTEGRATOR_SELECTIVE_VALUE` 的 selective repair 结论一致，所以最终采用：

`CURATOR_PRIMARY_LONGFORM_SUPPORTED_WITH_SELECTIVE_REPAIR`

实验到此停止，等待作者审核。未生成 Chapter 11，未修改 Prompt、生产 Writer Mode、前端或 Specialist/Integrator 实现。
