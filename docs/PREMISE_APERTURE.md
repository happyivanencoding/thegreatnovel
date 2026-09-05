# Premise Aperture｜Production Contract

状态：`FROZEN / OPTIONAL / OPERATOR-FROZEN`

证据：`books/real-exp-premise-aperture-20260829-v1/RESULTS.md`

## 1. 职责

Premise Aperture 是任何创意 Authority 冻结前的**可跳过开书阶段**。它解决的是完整货架前提过早收敛，而不是替代 World、Power、Human 或 Story：

```text
用户方向
  → Single-Agent Premise Forge：S1 / S2 / S3
  → Independent Premise Authority Compiler
  → TGN operator 选择 / 处理冲突 / 跳过
  → deterministic lane-specific frozen contracts
  → World / Power / Human / Story 现有分权链
```

从未开始或 operator 跳过时，原 Split Authority 开书路径保持可用；一旦保存候选，必须 Freeze 或跳过后才能生成、保存或 Freeze 下游创意 Authority。Automatic Production Run 默认由 operator 完成，不要求用户逐项点击。

## 2. 冻结边界

### Forge

- 一次生成三张完整候选；S1、S2、S3 代表不同激进程度，不自动排名或选择。
- 每张卡必须有一句话货架承诺、World-only、protagonist Ontology、T0 Origin、精确尺位置、Power trigger/coverage/carrier/boundary、Story Interface、第一章画面、Changed Verbs、第一次兑现、20章与百章展开。
- 候选均为 Non-Canon；当前实现默认 Luna high，GBrain OFF。

### Compiler

- fresh context 独立复核 trigger、目标、真实载体、出口、见证者、T0 尺位、Interface 因果与远期复合。
- 只返回 `PASS / CONDITIONAL PASS / FAIL`；不评分、不替 operator 选择、不修稿，也不因设定激进或主角占便宜大而否决。
- 当前实现默认 Terra high，GBrain OFF。
- 只有 strict `PASS` 可以 Freeze；`CONDITIONAL PASS / FAIL` 返回 TGN operator。没有自动 Repair Loop。
- 系统在生成 batch / selected Compiler Prompt 的当下写入 `PREMISE_COMPILER_INPUT.md`；报告保存不能改写这个 snapshot。卡片在 Prompt 发出后继续变化时，即使旧报告返回 strict PASS，也会因 snapshot 与当前卡片不一致而阻止 Freeze，并要求 selected-card recompile；不用哈希。

### Operator Freeze

- Forge 与 Compiler 不能自选 S1 / S2 / S3，也不能自动偏向最安全或“最高分”候选；选择属于已获整项任务授权的 TGN operator。
- Automatic Production Run 可以按用户方向、当前 AGGRESSIVE 审美与运行前明确的选择原则做一次 bounded operator selection；这不是额外常驻 Judge / Scorer，也不能覆盖 Compiler strict PASS。
- operator 可以在 Premise 从未开始时直接走旧链，也可以跳过；跳过会清除未 Freeze 候选、选择与 Compiler 结果。
- World Vision 一旦 Freeze，Premise 决定冻结，不得再修改或改为跳过。

## 3. Deterministic Lane Contracts

Freeze 时，代码把所选卡确定性拆成四份：

| Lane | 只能看到 |
|---|---|
| World | World-only + protagonist-blind public Interface |
| Power | literal Ontology + Initial Scale Position + trigger / target coverage / action / carrier / root boundary |
| Human | literal Ontology + exact T0 Origin + Initial Scale Position；看不到特殊 Power 与未来 Story |
| Story | Authorities Freeze 后第一次读取完整 Promise / Interface / 不可磨平项 |

无法同时成立时，下游必须返回 `PREMISE-AUTHORITY CONFLICT`，不能静默削弱、增强、恢复标准人形、移动出生地或改写 trigger/coverage。

`PREMISE_CONTRACT.md` 是 Workflow 中唯一正式 Premise artifact。搜索候选、选择卡与 Compiler Report 只是 operator / 高级工作区文件，不成为 Authority 节点。

## 4. Runtime 边界

- World / Power / Human 各自只消费自己的 lane contract。
- Story Program 第一次、也是最后一次读取完整 Story contract。
- Outline、Director、Curator、Primary、Authority Reviser、State 与章节 Runtime 不读取 raw Premise Card。
- Story Program 与其它 Authority Freeze 后，后续只携带它们已经实现的事实；Premise 不是第四 Authority。
- 该阶段不新增章节期 Reviewer、Scorer、Hard Gate 或 repair agent。

## 5. 持久文件与 UI

```text
PREMISE_CANDIDATES.md
SELECTED_PREMISE.md
PREMISE_COMPILER_INPUT.md
PREMISE_COMPILER_REPORT.md
PREMISE_SKIPPED.md
PREMISE_CONTRACT.md
PREMISE_WORLD_CONTRACT.md
PREMISE_POWER_CONTRACT.md
PREMISE_HUMAN_CONTRACT.md
PREMISE_STORY_CONTRACT.md
```

手工 Author Workspace 继续支持：生成三张候选、保存候选、批量 Compiler、手工选择/编辑、单卡复编、保存报告、Freeze 或跳过；它是高级干预面。默认 Automatic Production Run 不要求用户操作这些按钮。

## 6. 已拒绝 / 未冻结

- 四个独立高电压 Agent 的完整正交碰撞：拒绝；概念竞争、认知负担和调用数更高，质量低于完整 premise 一次形成。
- Two-Bet Voltage Budget：research-only。
- 通用 Judge / 打分器替作者偏向“最安全候选”：继续拒绝。已获任务授权的 bounded operator selection 属于自动 Production 编排，不是这个被拒绝的评分层。
- Selected Premise 自动 Repair：一次预注册测试漏掉受保护 Changed Verbs，research-only，不形成循环。
- 旧统一 Fantasy Seed：拒绝恢复。

## 7. 维护检查

修改该阶段时至少验证：

1. 未开始/operator 跳过仍可走原链；开始未 Freeze 不能绕过；
2. strict PASS 与 exact input snapshot 才能 Freeze；
3. 四条 lane 无交叉泄漏；
4. 编辑后必须复编；
5. World Freeze 后不可再改 Premise；
6. raw card 不进入 Outline 或章节；
7. `premise.contract` 变化使已存在的下游 Authority / Plan / Run stale；
8. 不新增常驻评分 selector、repair loop 或章节期 agent；bounded operator selection 不能绕过 strict PASS。
